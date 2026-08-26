#!/usr/bin/env python3
"""Sign-shuffle null for the post-stimulus selectivity of the Giant Fibre.

The complete Giant Fibre circuit separates an expanding stimulus from its exact
time reverse by a factor of 4.3287 in the integral of the response *after* the
stimulus ends, against 1.0631 at the peak.  That post-stimulus figure was
reported without a control, and a ratio without a null is not a result.

This script supplies the control, and fixes a second defect that was declared
rather than solved: the earlier sign-shuffle was measured with fixed tau only,
so comparing it against a dispersed-tau arm mixed two conditions.  Here the
ensembles are computed **at every spread**, so no comparison crosses conditions.

Three ensembles per point, because one cannot separate the two candidate causes:

  SIGN   the excitatory/inhibitory assignment is permuted across edges, so the
         multiset of signs and every weight is preserved and only the pairing
         of sign to edge changes
  TOPO   the weights are permuted while each edge keeps its own sign, so the
         sign pattern is preserved and the weight pattern is destroyed
  BOTH   sign and weight are permuted together, as the loosest control

If the observed value survives SIGN but not TOPO, the effect comes from where
the weight sits and not from the excitatory/inhibitory pattern, which is the
opposite of what a sign-based explanation would predict.  Reporting only SIGN
would leave that ambiguity open.

Both metrics are measured in the same run, so the contrast between peak and
post-stimulus selectivity is paired by construction.

Usage:
  python3 signshuffle_selpost.py --conn <parquet> --ann <tsv>
                                [--spreads 1 8 30] [--nulls 40]
                                [--out signshuffle.json]
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
TAU_CENTRE = 0.119
TAU_MIN, TAU_MAX = 1e-4, 0.95
SPECTRAL_BOUND = 0.99


def log(*a: object) -> None:
    """Print immediately so a backgrounded run can be polled with tail."""
    print(*a, flush=True)


def ratio(a: float, b: float):
    """Quotient, or None when the denominator carries no signal."""
    return a / b if b else None


def load(conn: Path, ann: Path) -> dict:
    """Edge list of the subgraph presynaptic to the target, plus the target."""
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
    cell_type = pd.Series(index.values).map(
        a.set_index("root_id")["cell_type"]).fillna("NA").values

    return {
        "n": len(nodes),
        "src": index.get_indexer(inside["Presynaptic_ID"].values),
        "dst": index.get_indexer(inside["Postsynaptic_ID"].values),
        "weight": inside["Connectivity"].values.astype(np.float64),
        "sign": np.where(inside["Excitatory"].values > 0, 1.0, -1.0),
        "target": np.isin(index.values, np.fromiter(target, dtype=np.int64)),
        "driven": np.isin(cell_type, DRIVEN_TYPES),
    }


def matrix(g: dict, weight: np.ndarray, sign: np.ndarray) -> np.ndarray:
    """Column-normalised signed matrix scaled to a fixed spectral radius.

    Both normalisations are applied to every arm, so an ensemble member cannot
    differ from the observed circuit in total input weight or in recurrent
    gain: only the pattern differs.
    """
    w = np.zeros((g["n"], g["n"]), dtype=np.float64)
    np.add.at(w, (g["src"], g["dst"]), weight * sign)
    total = np.abs(w).sum(axis=0)
    total[total == 0] = 1.0
    w /= total
    radius = float(np.abs(np.linalg.eigvals(w)).max())
    if radius > 0:
        w *= SPECTRAL_BOUND / radius
    return w


def profiles(steps: int, onset: int, duration: int) -> dict:
    """Expanding ramp, its exact reverse, and a flat profile at equal energy."""
    ramp = (np.arange(duration, dtype=np.float64) + 1) / duration
    waves = {"looming": ramp, "receding": ramp[::-1].copy(),
             "constant": np.full(duration, ramp.mean())}
    reference = float(np.sum(waves["looming"] ** 2))
    series = {}
    for name in waves:
        scaled = waves[name] * np.sqrt(
            reference / float(np.sum(waves[name] ** 2)))
        full = np.zeros(steps, dtype=np.float64)
        full[onset:onset + duration] = scaled
        series[name] = full
    return series


def draw_tau(n: int, spread: float, rng: np.random.Generator) -> np.ndarray:
    """Log-uniform time constants with geometric mean TAU_CENTRE."""
    if spread <= 1.0:
        return np.full(n, TAU_CENTRE, dtype=np.float64)
    half = np.log(spread) / 2.0
    return np.clip(TAU_CENTRE * np.exp(rng.uniform(-half, half, n)),
                   TAU_MIN, TAU_MAX)


def response(w: np.ndarray, g: dict, tau: np.ndarray, stim: np.ndarray,
             offset: int) -> tuple:
    """Peak and post-stimulus integral of the target's response."""
    z = np.zeros(g["n"], dtype=np.float64)
    s = np.zeros(g["n"], dtype=np.float64)
    trace = np.zeros(stim.size, dtype=np.float64)
    for step in range(stim.size):
        s[g["driven"]] = stim[step]
        z = (1.0 - tau) * z + tau * np.tanh(w.T @ z + s)
        trace[step] = float(z[g["target"]].mean())
    return (float(np.max(np.abs(trace))),
            float(np.sum(np.abs(trace[offset:]))))


def measure(w: np.ndarray, g: dict, tau: np.ndarray, stim: dict,
            offset: int) -> dict:
    """Both selectivity ratios for one matrix and one tau vector."""
    peak, post = {}, {}
    for name, series in stim.items():
        peak[name], post[name] = response(w, g, tau, series, offset)
    return {
        "sel_peak": ratio(peak["looming"], peak["receding"]),
        "sel_post": ratio(post["looming"], post["receding"]),
        "post_looming": post["looming"],
    }


def rank(observed: float, values: np.ndarray) -> dict:
    """Ensemble moments plus the rank of the observed value in both tails."""
    if values.size == 0 or observed is None:
        return {"n": 0}
    mean, sd = float(values.mean()), float(values.std())
    return {
        "observed": round(observed, 4),
        "null_mean": round(mean, 4),
        "null_sd": round(sd, 4),
        "null_min": round(float(values.min()), 4),
        "null_max": round(float(values.max()), 4),
        "nulls_ge_observed": int((values >= observed).sum()),
        "nulls_le_observed": int((values <= observed).sum()),
        "ratio": round(observed / mean, 4) if mean else None,
        "z": round((observed - mean) / sd, 2) if sd > 0 else None,
        "sd_zero_reason": (None if sd > 0 else
                           "conserved" if mean == observed else "saturated"),
    }


def main(argv: list | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--conn", type=Path, required=True)
    parser.add_argument("--ann", type=Path, required=True)
    parser.add_argument("--steps", type=int, default=200)
    parser.add_argument("--onset", type=int, default=20)
    parser.add_argument("--duration", type=int, default=60)
    parser.add_argument("--spreads", type=float, nargs="+",
                        default=[1.0, 8.0, 30.0])
    parser.add_argument("--nulls", type=int, default=40)
    parser.add_argument("--out", type=Path, default=Path("signshuffle.json"))
    args = parser.parse_args(argv)

    started = time.time()
    g = load(args.conn, args.ann)
    offset = args.onset + args.duration
    stim = profiles(args.steps, args.onset, args.duration)
    log("nodes " + str(g["n"]) + " edges " + str(g["src"].size)
        + " driven " + str(int(g["driven"].sum()))
        + " target " + str(int(g["target"].sum())))
    energies = {k: round(float(np.sum(v ** 2)), 10) for k, v in stim.items()}
    log("GUARD energies " + json.dumps(energies))
    log("GUARD matched: " + ("MATCHED_OK" if
        abs(energies["looming"] - energies["receding"]) < 1e-9
        else "MISMATCH_FAIL"))

    observed_matrix = matrix(g, g["weight"], g["sign"])
    results = {}

    for spread in args.spreads:
        tau = draw_tau(g["n"], spread, np.random.default_rng(4242))
        obs = measure(observed_matrix, g, tau, stim, offset)
        log("OBSERVED spread=" + ("%g" % spread) + " " + json.dumps(
            {k: (round(v, 4) if isinstance(v, float) else v)
             for k, v in obs.items()}))

        for family in ("SIGN", "TOPO", "BOTH"):
            rows = []
            for i in range(args.nulls):
                rng = np.random.default_rng(1000 + 7 * i)
                sign = (rng.permutation(g["sign"]) if family in ("SIGN", "BOTH")
                        else g["sign"])
                weight = (rng.permutation(g["weight"])
                          if family in ("TOPO", "BOTH") else g["weight"])
                rows.append(measure(matrix(g, weight, sign), g, tau, stim,
                                    offset))
                if (i + 1) % 20 == 0:
                    log("    spread=" + ("%g" % spread) + " " + family
                        + " " + str(i + 1) + "/" + str(args.nulls))

            key = "spread_" + ("%g" % spread) + "_" + family
            results[key] = {
                metric: rank(obs[metric], np.array(
                    [r[metric] for r in rows
                     if r[metric] is not None and np.isfinite(r[metric])],
                    dtype=float))
                for metric in ("sel_peak", "sel_post", "post_looming")
            }
            log("RESULT " + key + " " + json.dumps(results[key]))

    args.out.write_text(json.dumps({
        "nodes": g["n"],
        "edges": int(g["src"].size),
        "nulls": args.nulls,
        "tau_centre": TAU_CENTRE,
        "window": {"steps": args.steps, "onset": args.onset,
                   "duration": args.duration, "post_from": offset},
        "stimulus_energies": energies,
        "results": results,
    }, indent=1))
    log("DONE in " + str(round(time.time() - started, 1)) + " s -> "
        + str(args.out))
    return 0


if __name__ == "__main__":
    sys.exit(main())
