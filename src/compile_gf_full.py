#!/usr/bin/env python3
"""Compile the complete Giant Fibre input circuit, with sign, and ablate it.

Version 1 of the library entry for this circuit reported a temporal selectivity
of 1.04x, that is none, and concluded that topology fixes routing and gain but
not selectivity.  That measurement was made on the excitatory visual afferents
only: 299 of the 962 input connections and none of the inhibition.  This script
tests whether the conclusion survives the complete circuit.

The subgraph is every neuron presynaptic to the Giant Fibre plus the Giant
Fibre itself, and every connection among those neurons.  It is strongly
recurrent, so the central and inhibitory partners are driven by the visual
afferents rather than left silent, which is what makes the comparison
meaningful.

Four arms, identical model, identical stimulus, identical seed:
  FULL        every internal connection, signed
  NO_INHIB    inhibitory connections removed
  NO_CENTRAL  connections from central partners removed
  CUT_V1      only the direct visual afferent connections onto the Giant
              Fibre, no recurrence: the recipe of version 1

Dynamics, one step per unit time, from the engine of this repository:

    z <- (1 - tau) * z + tau * tanh(W' z + s)

with W column-normalised over the retained edges of each arm and scaled to a
fixed spectral bound, so an arm cannot win by having more total weight.

Guards, each able to fail:
  1. Stimulus energy is matched between profiles to machine precision.
  2. An amplitude control that MUST separate, proving the readout can resolve
     a difference at all.
  3. A sign-shuffled ensemble, so a selectivity value can be compared against
     what the same wiring gives with sign scrambled.

Usage:
  python3 compile_gf_full.py --conn <parquet> --ann <tsv> [--steps 200]
                            [--shuffles 20] [--out results.json]
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd
import pyarrow.parquet as pq

TARGET_TYPE = "DNp01"
DRIVEN_TYPES = ["LC4", "LPLC2"]
TAU = 0.119
SPECTRAL_BOUND = 0.99


def log(*a: object) -> None:
    """Print immediately so a backgrounded run can be polled with tail."""
    print(*a, flush=True)


def build_subgraph(conn: Path, ann: Path) -> dict:
    """Every neuron presynaptic to the target, plus every edge among them."""
    a = pd.read_csv(ann, sep="\t", low_memory=False)
    d = pq.read_table(conn, columns=[
        "Presynaptic_ID", "Postsynaptic_ID", "Connectivity", "Excitatory"
    ]).to_pandas()

    target = set(a.loc[a["cell_type"] == TARGET_TYPE, "root_id"])
    partners = set(d.loc[d["Postsynaptic_ID"].isin(target), "Presynaptic_ID"])
    nodes = sorted(partners | target)
    index = pd.Index(nodes)

    inside = d[d["Presynaptic_ID"].isin(nodes)
               & d["Postsynaptic_ID"].isin(nodes)]
    src = index.get_indexer(inside["Presynaptic_ID"].values)
    dst = index.get_indexer(inside["Postsynaptic_ID"].values)
    weight = inside["Connectivity"].values.astype(np.float64)
    sign = np.where(inside["Excitatory"].values > 0, 1.0, -1.0)

    meta = a.set_index("root_id")
    super_class = pd.Series(index.values).map(
        meta["super_class"]).fillna("NA").values
    cell_type = pd.Series(index.values).map(
        meta["cell_type"]).fillna("NA").values

    return {
        "index": index,
        "n": len(nodes),
        "src": src,
        "dst": dst,
        "weight": weight,
        "sign": sign,
        "target": np.isin(index.values, np.fromiter(target, dtype=np.int64)),
        "driven": np.isin(cell_type, DRIVEN_TYPES),
        "central": super_class == "central",
        "super_class": super_class,
    }


def matrix(g: dict, arm: str, sign: np.ndarray | None = None) -> np.ndarray:
    """Dense signed weight matrix for one arm, column-normalised and scaled.

    Column normalisation makes every postsynaptic neuron receive unit total
    input weight, so an arm cannot gain amplitude merely by retaining more
    connections.  The spectral scaling then fixes the recurrent gain, so the
    arms differ in their wiring pattern and not in their overall drive.
    """
    signs = g["sign"] if sign is None else sign
    keep = np.ones(g["src"].size, dtype=bool)
    if arm == "NO_INHIB":
        keep &= signs > 0
    elif arm == "NO_CENTRAL":
        keep &= ~g["central"][g["src"]]
    elif arm == "CUT_V1":
        keep &= g["driven"][g["src"]] & g["target"][g["dst"]] & (signs > 0)
    elif arm != "FULL":
        raise ValueError(f"unknown arm {arm!r}")

    w = np.zeros((g["n"], g["n"]), dtype=np.float64)
    np.add.at(w, (g["src"][keep], g["dst"][keep]),
              g["weight"][keep] * signs[keep])
    column_total = np.abs(w).sum(axis=0)
    column_total[column_total == 0] = 1.0
    w /= column_total
    radius = np.abs(np.linalg.eigvals(w)).max()
    if radius > 0:
        w *= SPECTRAL_BOUND / radius
    return w, int(keep.sum())


def profiles(steps: int, onset: int, duration: int) -> dict:
    """Stimulus profiles, all scaled to exactly the same total energy.

    'looming' expands, 'receding' is its exact time reverse, 'constant' is
    flat, and 'double' is a looming ramp at twice the energy: the positive
    control.  Without that last one a null result could not be distinguished
    from a readout that resolves nothing.
    """
    t = np.arange(duration, dtype=np.float64)
    ramp = (t + 1) / duration
    out = {
        "looming": ramp,
        "receding": ramp[::-1].copy(),
        "constant": np.full(duration, ramp.mean()),
    }
    reference = float(np.sum(out["looming"] ** 2))
    for name, wave in out.items():
        energy = float(np.sum(wave ** 2))
        out[name] = wave * np.sqrt(reference / energy)
    out["double_energy"] = out["looming"] * np.sqrt(2.0)

    series = {}
    for name, wave in out.items():
        full = np.zeros(steps, dtype=np.float64)
        full[onset:onset + duration] = wave
        series[name] = full
    return series


def simulate(w: np.ndarray, g: dict, stim: np.ndarray) -> dict:
    """Run the dynamics and read the target's response."""
    z = np.zeros(g["n"], dtype=np.float64)
    driven = g["driven"]
    trace = np.zeros(stim.size, dtype=np.float64)
    for step, amplitude in enumerate(stim):
        s = np.zeros(g["n"], dtype=np.float64)
        s[driven] = amplitude
        z = (1.0 - TAU) * z + TAU * np.tanh(w.T @ z + s)
        trace[step] = float(z[g["target"]].mean())
    return {
        "peak": float(np.max(np.abs(trace))),
        "final": float(trace[-1]),
        "integral": float(np.sum(np.abs(trace))),
        "trace_tail": [round(float(x), 6) for x in trace[-5:]],
    }


def main(argv: list | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--conn", type=Path, required=True)
    parser.add_argument("--ann", type=Path, required=True)
    parser.add_argument("--steps", type=int, default=200)
    parser.add_argument("--onset", type=int, default=20)
    parser.add_argument("--duration", type=int, default=60)
    parser.add_argument("--shuffles", type=int, default=20)
    parser.add_argument("--out", type=Path, default=Path("gf_full.json"))
    args = parser.parse_args(argv)

    started = time.time()
    g = build_subgraph(args.conn, args.ann)
    log(f"nodes {g['n']} internal_edges {g['src'].size} "
        f"synapses {int(g['weight'].sum())}")
    log("driven neurons (LC4+LPLC2) " + str(int(g["driven"].sum()))
        + "  target " + str(int(g["target"].sum()))
        + "  central partners " + str(int(g["central"].sum())))
    log("edges into target "
        + str(int(g["target"][g["dst"]].sum()))
        + "  inhibitory share of internal edges "
        + str(round(float((g["sign"] < 0).mean()), 4)))

    stim = profiles(args.steps, args.onset, args.duration)
    energies = {k: round(float(np.sum(v ** 2)), 10) for k, v in stim.items()}
    log("GUARD stimulus energies " + json.dumps(energies))
    matched = abs(energies["looming"] - energies["receding"]) < 1e-9 \
        and abs(energies["looming"] - energies["constant"]) < 1e-9
    log("GUARD energy matched to 1e-9: "
        + ("MATCHED_OK" if matched else "MISMATCH_FAIL"))
    log("GUARD double_energy differs on purpose: "
        + ("DIFFERS_OK" if energies["double_energy"] > energies["looming"]
           else "SAME_FAIL"))

    results = {}
    for arm in ("FULL", "NO_INHIB", "NO_CENTRAL", "CUT_V1"):
        w, kept = matrix(g, arm)
        responses = {name: simulate(w, g, series)
                     for name, series in stim.items()}
        selectivity = (responses["looming"]["peak"]
                       / responses["receding"]["peak"]
                       if responses["receding"]["peak"] else None)
        control = (responses["double_energy"]["peak"]
                   / responses["looming"]["peak"]
                   if responses["looming"]["peak"] else None)
        results[arm] = {
            "edges_kept": kept,
            "responses": responses,
            "selectivity_looming_over_receding":
                round(selectivity, 4) if selectivity else None,
            "selectivity_looming_over_constant":
                round(responses["looming"]["peak"]
                      / responses["constant"]["peak"], 4)
                if responses["constant"]["peak"] else None,
            "positive_control_double_over_single":
                round(control, 4) if control else None,
        }
        log("ARM " + arm + " " + json.dumps(results[arm]))

    # Sign-shuffled ensemble on the full wiring: what does this circuit give
    # when the excitatory/inhibitory assignment carries no information?
    shuffled = []
    for i in range(args.shuffles):
        rng = np.random.default_rng(1000 + 7 * i)
        signs = rng.permutation(g["sign"])
        w, _ = matrix(g, "FULL", sign=signs)
        loom = simulate(w, g, stim["looming"])["peak"]
        rec = simulate(w, g, stim["receding"])["peak"]
        shuffled.append(loom / rec if rec else np.nan)
        if (i + 1) % 10 == 0:
            log(f"  sign shuffle {i + 1}/{args.shuffles}")
    values = np.array([x for x in shuffled if np.isfinite(x)], dtype=float)
    observed = results["FULL"]["selectivity_looming_over_receding"]
    summary = {
        "n": int(values.size),
        "mean": round(float(values.mean()), 4) if values.size else None,
        "sd": round(float(values.std()), 4) if values.size else None,
        "min": round(float(values.min()), 4) if values.size else None,
        "max": round(float(values.max()), 4) if values.size else None,
        "shuffles_ge_observed": int((values >= observed).sum())
        if observed else None,
    }
    log("SIGN_SHUFFLE " + json.dumps(summary))

    args.out.write_text(json.dumps({
        "nodes": g["n"],
        "internal_edges": int(g["src"].size),
        "edges_into_target": int(g["target"][g["dst"]].sum()),
        "tau": TAU,
        "spectral_bound": SPECTRAL_BOUND,
        "stimulus_energies": energies,
        "arms": results,
        "sign_shuffle": summary,
        "sign_shuffle_raw": [round(float(x), 6) for x in shuffled],
    }, indent=1))
    log(f"DONE in {round(time.time() - started, 1)} s -> {args.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
