#!/usr/bin/env python3
"""Sweep heterogeneous time constants on the complete Giant Fibre circuit.

The finding that this circuit shows no temporal selectivity (1.0631, below a
sign-shuffled ensemble at 1.1131 +/- 0.0185) was obtained with a single time
constant, tau = 0.119, shared by all 864 neurons.  The engine of this
repository uses heterogeneous tau, and a spread of time constants is the one
parameter that could plausibly create selectivity for a temporal profile.  If
the finding does not survive this sweep it has to be withdrawn.

What makes the sweep falsifiable is not the spread but the assignment:

  RANDOM      time constants drawn independently per neuron
  STRUCTURED  fast constants to optic and visual neurons, slow ones to central
              neurons, matching the regional measurement in this repository
              (optic 0.2689 against mushroom body 0.0180, a factor of 15)
  REVERSED    the same constants with that assignment inverted, as falsifier

Selectivity appearing under RANDOM would be a property of dispersion alone and
would say nothing about the wiring.  Selectivity appearing under STRUCTURED but
not REVERSED would mean the pairing of time constant to cell class carries the
effect, and the original claim would have to be narrowed.  Without both arms
the sweep cannot separate those cases.

Time constants are drawn log-uniformly with a fixed geometric mean of 0.119, so
the spread changes while the central value does not: no arm can win by being
globally faster or slower.  The spread of 1 is an internal control and must
reproduce the homogeneous result.

The weight matrix is built once, because tau enters the update rule and not the
matrix, so the spectral scaling is computed a single time.

Usage:
  python3 sweep_tau_hetero.py --conn <parquet> --ann <tsv>
                             [--spreads 1 2 4 8 15 30] [--draws 20]
                             [--out tau_sweep.json]
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
FAST_CLASSES = ["visual_projection", "visual_centrifugal", "optic"]


def log(*a: object) -> None:
    """Print immediately so a backgrounded run can be polled with tail."""
    print(*a, flush=True)


def ratio(a: float, b: float):
    """Quotient, or None when the denominator carries no signal."""
    return a / b if b else None


def build(conn: Path, ann: Path) -> dict:
    """Subgraph of every neuron presynaptic to the target, plus the target."""
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
    signed = (inside["Connectivity"].values.astype(np.float64)
              * np.where(inside["Excitatory"].values > 0, 1.0, -1.0))

    n = len(nodes)
    w = np.zeros((n, n), dtype=np.float64)
    np.add.at(w, (src, dst), signed)
    column_total = np.abs(w).sum(axis=0)
    column_total[column_total == 0] = 1.0
    w /= column_total
    radius = float(np.abs(np.linalg.eigvals(w)).max())
    w *= SPECTRAL_BOUND / radius

    meta = a.set_index("root_id")
    super_class = pd.Series(index.values).map(
        meta["super_class"]).fillna("NA").values
    cell_type = pd.Series(index.values).map(
        meta["cell_type"]).fillna("NA").values

    return {
        "n": n,
        "w": w,
        "edges": int(src.size),
        "radius_before_scaling": round(radius, 6),
        "target": np.isin(index.values, np.fromiter(target, dtype=np.int64)),
        "driven": np.isin(cell_type, DRIVEN_TYPES),
        "fast": np.isin(super_class, FAST_CLASSES),
    }


def profiles(steps: int, onset: int, duration: int) -> dict:
    """Stimulus profiles at matched energy, plus a doubled positive control."""
    ramp = (np.arange(duration, dtype=np.float64) + 1) / duration
    waves = {
        "looming": ramp,
        "receding": ramp[::-1].copy(),
        "constant": np.full(duration, ramp.mean()),
    }
    reference = float(np.sum(waves["looming"] ** 2))
    for name in list(waves):
        waves[name] = waves[name] * np.sqrt(
            reference / float(np.sum(waves[name] ** 2)))
    waves["double_energy"] = waves["looming"] * np.sqrt(2.0)

    series = {}
    for name, wave in waves.items():
        full = np.zeros(steps, dtype=np.float64)
        full[onset:onset + duration] = wave
        series[name] = full
    return series


def draw_tau(g: dict, spread: float, mode: str,
             rng: np.random.Generator) -> np.ndarray:
    """Time constants with geometric mean TAU_CENTRE and the given spread.

    ``spread`` is the ratio between the largest and smallest possible value.
    A spread of 1 reproduces the homogeneous case exactly, which is the
    internal control: if that arm does not reproduce the published value the
    whole sweep is invalid.
    """
    if spread <= 1.0:
        return np.full(g["n"], TAU_CENTRE, dtype=np.float64)

    half = np.log(spread) / 2.0
    values = TAU_CENTRE * np.exp(rng.uniform(-half, half, g["n"]))
    values = np.clip(values, TAU_MIN, TAU_MAX)
    if mode == "RANDOM":
        return values

    # Structured assignment: the largest constants, meaning the shortest
    # memory, go to the optic and visual populations and the smallest to the
    # central ones, following the regional measurement in this repository.
    ordered = np.sort(values)[::-1]
    out = np.empty(g["n"], dtype=np.float64)
    fast_first = np.argsort(~g["fast"], kind="stable")
    if mode == "STRUCTURED":
        out[fast_first] = ordered
    elif mode == "REVERSED":
        out[fast_first] = ordered[::-1]
    else:
        raise ValueError("unknown mode " + repr(mode))
    return out


def simulate(g: dict, tau: np.ndarray, stim: np.ndarray,
             offset: int) -> dict:
    """Run the dynamics and read the target, during and after the stimulus."""
    w, driven, target = g["w"], g["driven"], g["target"]
    z = np.zeros(g["n"], dtype=np.float64)
    s = np.zeros(g["n"], dtype=np.float64)
    trace = np.zeros(stim.size, dtype=np.float64)
    for step in range(stim.size):
        s[driven] = stim[step]
        z = (1.0 - tau) * z + tau * np.tanh(w.T @ z + s)
        trace[step] = float(z[target].mean())
    return {
        "peak": float(np.max(np.abs(trace))),
        "post_integral": float(np.sum(np.abs(trace[offset:]))),
    }


def evaluate(g: dict, tau: np.ndarray, stim: dict, offset: int) -> dict:
    """Selectivity ratios and the amplitude control for one tau vector."""
    r = {name: simulate(g, tau, series, offset)
         for name, series in stim.items()}
    return {
        "sel_peak": ratio(r["looming"]["peak"], r["receding"]["peak"]),
        "sel_post": ratio(r["looming"]["post_integral"],
                          r["receding"]["post_integral"]),
        "sel_constant": ratio(r["looming"]["peak"], r["constant"]["peak"]),
        "control_double": ratio(r["double_energy"]["peak"],
                                r["looming"]["peak"]),
        "peak_looming": r["looming"]["peak"],
    }


def summarise(values: list) -> dict:
    """Mean, spread and range of a list of ratios, ignoring undefined ones."""
    clean = np.array([v for v in values if v is not None and np.isfinite(v)],
                     dtype=float)
    if clean.size == 0:
        return {"n": 0}
    return {
        "n": int(clean.size),
        "mean": round(float(clean.mean()), 4),
        "sd": round(float(clean.std()), 4),
        "min": round(float(clean.min()), 4),
        "max": round(float(clean.max()), 4),
    }


def main(argv: list | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--conn", type=Path, required=True)
    parser.add_argument("--ann", type=Path, required=True)
    parser.add_argument("--steps", type=int, default=200)
    parser.add_argument("--onset", type=int, default=20)
    parser.add_argument("--duration", type=int, default=60)
    parser.add_argument("--spreads", type=float, nargs="+",
                        default=[1.0, 2.0, 4.0, 8.0, 15.0, 30.0])
    parser.add_argument("--draws", type=int, default=20)
    parser.add_argument("--out", type=Path, default=Path("tau_sweep.json"))
    args = parser.parse_args(argv)

    started = time.time()
    g = build(args.conn, args.ann)
    offset = args.onset + args.duration
    log("nodes " + str(g["n"]) + " internal_edges " + str(g["edges"])
        + " spectral_radius_before_scaling "
        + str(g["radius_before_scaling"]))
    log("driven " + str(int(g["driven"].sum()))
        + "  target " + str(int(g["target"].sum()))
        + "  fast-class neurons " + str(int(g["fast"].sum())))

    stim = profiles(args.steps, args.onset, args.duration)
    energies = {k: round(float(np.sum(v ** 2)), 10) for k, v in stim.items()}
    log("GUARD energies " + json.dumps(energies))
    matched = (abs(energies["looming"] - energies["receding"]) < 1e-9
               and abs(energies["looming"] - energies["constant"]) < 1e-9)
    log("GUARD comparable profiles matched: "
        + ("MATCHED_OK" if matched else "MISMATCH_FAIL"))

    results = {}
    for spread in args.spreads:
        for mode in ("RANDOM", "STRUCTURED", "REVERSED"):
            if spread <= 1.0 and mode != "RANDOM":
                continue
            draws = 1 if spread <= 1.0 else args.draws
            rows = [evaluate(g, draw_tau(g, spread, mode,
                                         np.random.default_rng(1000 + 7 * i)),
                             stim, offset)
                    for i in range(draws)]
            key = "spread_" + ("%g" % spread) + "_" + mode
            results[key] = {
                metric: summarise([row[metric] for row in rows])
                for metric in ("sel_peak", "sel_post", "sel_constant",
                               "control_double", "peak_looming")
            }
            log("RESULT " + key + " " + json.dumps(results[key]))

    args.out.write_text(json.dumps({
        "nodes": g["n"],
        "internal_edges": g["edges"],
        "tau_centre": TAU_CENTRE,
        "spectral_bound": SPECTRAL_BOUND,
        "stimulus_energies": energies,
        "sweep": results,
    }, indent=1))
    log("DONE in " + str(round(time.time() - started, 1)) + " s -> "
        + str(args.out))
    return 0


if __name__ == "__main__":
    sys.exit(main())
