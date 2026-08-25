#!/usr/bin/env python3
"""Sign-shuffle null that preserves Dale's law, for the Giant Fibre circuit.

An external audit (finding A-06) established that the sign shuffle used in
``compile_gf_full.py`` and ``signshuffle_selpost.py`` permutes sign **per
edge**.  That fabricates neurons whose outputs are part excitatory and part
inhibitory, while this same repository measured **zero mixed neurons out of
138,005** with outputs.  The control was therefore biologically implausible,
and the conclusion drawn from it was stronger than the control supported.

This script supplies the control the audit asked for.  The excitatory or
inhibitory identity is permuted **across presynaptic neurons**, so every neuron
remains purely one sign and the count of neurons of each sign is conserved
exactly.  What is destroyed is only which neuron carries which identity, which
is the biologically meaningful randomisation.

The per-edge shuffle is kept as a secondary loose control, so the two can be
compared in the same run.  Reporting only one would leave open how much of the
verdict came from the implausible ensemble.

A guard counts mixed-sign neurons before and after and **aborts with a non-zero
exit status** if an ensemble that claims to preserve Dale's law does not.  That
also closes finding A-01 for this script: a red state stops the process instead
of being printed.

Usage:
  python3 signshuffle_dale.py --conn <parquet> --ann <tsv> [--nulls 40]
                             [--out signshuffle_dale.json]
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


class GuardFailure(RuntimeError):
    """Raised when a stated invariant does not hold, so the run stops."""


def require(condition: bool, message: str) -> None:
    """Abort the run when a stated invariant is violated.

    A guard that only prints cannot govern a pipeline: the process exits zero
    and a caller reads the run as valid.  This raises instead.
    """
    if not condition:
        raise GuardFailure(message)
    print("GUARD_OK " + message, flush=True)


def log(*a: object) -> None:
    """Print immediately so a backgrounded run can be polled with tail."""
    print(*a, flush=True)


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


def mixed_neurons(src: np.ndarray, sign: np.ndarray, n: int) -> int:
    """Count presynaptic neurons emitting both signs, which Dale's law forbids."""
    positive = np.bincount(src, weights=(sign > 0).astype(float), minlength=n)
    negative = np.bincount(src, weights=(sign < 0).astype(float), minlength=n)
    return int(((positive > 0) & (negative > 0)).sum())


def neuron_signs(src: np.ndarray, sign: np.ndarray, n: int) -> np.ndarray:
    """Sign of each neuron's outputs, or zero when it has none."""
    out = np.zeros(n, dtype=np.float64)
    np.add.at(out, src, sign)
    return np.sign(out)


def shuffle_dale(src: np.ndarray, per_neuron: np.ndarray,
                 rng: np.random.Generator) -> np.ndarray:
    """Permute excitatory/inhibitory identity across neurons, not edges.

    Only neurons that emit edges take part, so the number of excitatory and of
    inhibitory neurons is conserved exactly and every neuron stays pure.
    """
    emitting = np.flatnonzero(per_neuron != 0)
    shuffled = per_neuron.copy()
    shuffled[emitting] = per_neuron[rng.permutation(emitting)]
    return shuffled[src]


def matrix(g: dict, weight: np.ndarray, sign: np.ndarray) -> np.ndarray:
    """Column-normalised signed matrix scaled to a fixed spectral radius."""
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
    """Expanding ramp and its exact reverse, at identical energy."""
    ramp = (np.arange(duration, dtype=np.float64) + 1) / duration
    waves = {"looming": ramp, "receding": ramp[::-1].copy()}
    reference = float(np.sum(waves["looming"] ** 2))
    series = {}
    for name in waves:
        scaled = waves[name] * np.sqrt(
            reference / float(np.sum(waves[name] ** 2)))
        full = np.zeros(steps, dtype=np.float64)
        full[onset:onset + duration] = scaled
        series[name] = full
    return series


def measure(w: np.ndarray, g: dict, stim: dict, offset: int) -> dict:
    """Peak and post-stimulus selectivity for one matrix."""
    peak, post = {}, {}
    for name, series in stim.items():
        z = np.zeros(g["n"], dtype=np.float64)
        s = np.zeros(g["n"], dtype=np.float64)
        trace = np.zeros(series.size, dtype=np.float64)
        for step in range(series.size):
            s[g["driven"]] = series[step]
            z = (1.0 - TAU) * z + TAU * np.tanh(w.T @ z + s)
            trace[step] = float(z[g["target"]].mean())
        peak[name] = float(np.max(np.abs(trace)))
        post[name] = float(np.sum(np.abs(trace[offset:])))
    return {
        "sel_peak": peak["looming"] / peak["receding"] if peak["receding"]
        else None,
        "sel_post": post["looming"] / post["receding"] if post["receding"]
        else None,
        "post_looming": post["looming"],
    }


def rank(observed, values: np.ndarray) -> dict:
    """Ensemble moments and rank, distinguishing conserved from saturated.

    A zero spread means two different things and the audit found that this
    project's shared helper conflated them: when the ensemble equals the
    observed value the statistic cannot be tested, but when it differs the
    direction is valid and only the effect size is censored.
    """
    if observed is None or values.size == 0:
        return {"n": 0}
    mean, sd = float(values.mean()), float(values.std())
    verdict = None
    if sd == 0.0:
        verdict = "CONSERVED_NOT_TESTABLE" if mean == observed \
            else "SATURATED_DIRECTION_VALID_SIZE_CENSORED"
    return {
        "observed": round(float(observed), 4),
        "null_mean": round(mean, 4),
        "null_sd": round(sd, 4),
        "null_min": round(float(values.min()), 4),
        "null_max": round(float(values.max()), 4),
        "nulls_ge_observed": int((values >= observed).sum()),
        "ratio": round(float(observed) / mean, 4) if mean else None,
        "z": round((float(observed) - mean) / sd, 2) if sd > 0 else None,
        "sd_zero_verdict": verdict,
    }


def main(argv: list | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--conn", type=Path, required=True)
    parser.add_argument("--ann", type=Path, required=True)
    parser.add_argument("--steps", type=int, default=200)
    parser.add_argument("--onset", type=int, default=20)
    parser.add_argument("--duration", type=int, default=60)
    parser.add_argument("--nulls", type=int, default=40)
    parser.add_argument("--out", type=Path,
                        default=Path("signshuffle_dale.json"))
    args = parser.parse_args(argv)
    require(args.nulls > 0, "nulls must be positive, got "
            + str(args.nulls))

    started = time.time()
    g = load(args.conn, args.ann)
    offset = args.onset + args.duration
    stim = profiles(args.steps, args.onset, args.duration)
    log("nodes " + str(g["n"]) + " edges " + str(g["src"].size))

    observed_mixed = mixed_neurons(g["src"], g["sign"], g["n"])
    require(observed_mixed == 0,
            "observed graph obeys Dale's law, mixed neurons = "
            + str(observed_mixed))
    per_neuron = neuron_signs(g["src"], g["sign"], g["n"])
    counts = {"excitatory": int((per_neuron > 0).sum()),
              "inhibitory": int((per_neuron < 0).sum())}
    log("neurons by sign " + json.dumps(counts))

    obs = measure(matrix(g, g["weight"], g["sign"]), g, stim, offset)
    log("OBSERVED " + json.dumps(
        {k: round(v, 4) for k, v in obs.items() if v is not None}))

    results = {}
    for family in ("DALE", "PER_EDGE"):
        rows, mixed_seen = [], []
        for i in range(args.nulls):
            rng = np.random.default_rng(1000 + 7 * i)
            if family == "DALE":
                sign = shuffle_dale(g["src"], per_neuron, rng)
            else:
                sign = rng.permutation(g["sign"])
            mixed_seen.append(mixed_neurons(g["src"], sign, g["n"]))
            rows.append(measure(matrix(g, g["weight"], sign), g, stim, offset))
            if (i + 1) % 20 == 0:
                log("    " + family + " " + str(i + 1) + "/"
                    + str(args.nulls))

        worst = max(mixed_seen)
        if family == "DALE":
            require(worst == 0,
                    "Dale ensemble preserves Dale's law, worst mixed = "
                    + str(worst))
        else:
            require(worst > 0,
                    "per-edge ensemble does break Dale's law as expected,"
                    " worst mixed = " + str(worst))

        results[family] = {
            "mixed_neurons_worst_case": worst,
            "mixed_neurons_mean": round(float(np.mean(mixed_seen)), 1),
            **{metric: rank(obs[metric], np.array(
                [r[metric] for r in rows
                 if r[metric] is not None and np.isfinite(r[metric])],
                dtype=float))
               for metric in ("sel_peak", "sel_post", "post_looming")},
        }
        log("RESULT " + family + " " + json.dumps(results[family]))

    args.out.write_text(json.dumps({
        "nodes": g["n"], "edges": int(g["src"].size),
        "nulls": args.nulls, "tau": TAU,
        "neurons_by_sign": counts,
        "observed_mixed_neurons": observed_mixed,
        "window": {"steps": args.steps, "onset": args.onset,
                   "duration": args.duration, "post_from": offset},
        "observed": obs, "results": results,
    }, indent=1))
    log("DONE in " + str(round(time.time() - started, 1)) + " s -> "
        + str(args.out))
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except GuardFailure as failure:
        print("GUARD_FAILED " + str(failure), file=sys.stderr, flush=True)
        sys.exit(2)
