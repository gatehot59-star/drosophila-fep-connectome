#!/usr/bin/env python3
"""Multi-hop motor access in the FAFB connectome, against degree-preserving
and neuropil-preserving null ensembles.

Produces every number and every figure panel of the two-hop section of
Mendieta (2026a) v2.  Single instrument: recomputes from the raw data, dumps
the full per-realization output as JSON, and writes the SVG panels.

Inputs (paths are CLI arguments, no absolute paths are hard-coded):
  connectivity.parquet   columns Presynaptic_ID, Postsynaptic_ID, Connectivity
  annotations.tsv        columns root_id, super_class, cell_class
  pre.feather            columns pre_pt_root_id, neuropil, count   (optional)
  post.feather           columns post_pt_root_id, neuropil, count  (optional)

The two neuropil files are the per-neuron neuropil synapse counts of the
FlyWire 783 release (Zenodo record 10676866).  When both are supplied a
neuropil-preserving ensemble is computed in addition to the degree-preserving
one; when they are absent that ensemble is reported as not measured rather
than silently skipped.

Statistics per sensory class:
  R1  distinct motor neurons receiving a one-hop connection
  R2  distinct motor neurons receiving a two-hop path
  P2  number of two-hop paths into the motor population
  H1  distinct neurons reached at one hop (context, not a test)

Usage:
  python3 twohop_nulls.py --conn <parquet> --ann <tsv> [--pre <f> --post <f>]
                          [--nulls 40] [--thresholds 1 5] [--outdir .]
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd
import pyarrow.feather as feather
import pyarrow.parquet as pq

CLASSES = ["olfactory", "visual", "mechanosensory", "gustatory"]
CONTROL = "CTRL_arbitrary"
MIRROR = "_MIRROR_edges_into_motor"
CONTROL_SEED = 4242


def log(*a: object) -> None:
    """Print immediately so a backgrounded run can be polled with tail."""
    print(*a, flush=True)


class Graph:
    """Edge list of the connectome indexed by contiguous integers."""

    def __init__(self, pre: np.ndarray, post: np.ndarray,
                 root_ids: np.ndarray) -> None:
        self.roots = pd.Index(root_ids)
        self.src = self.roots.get_indexer(pre).astype(np.int32)
        self.dst = self.roots.get_indexer(post).astype(np.int32)
        if (self.src < 0).any() or (self.dst < 0).any():
            raise ValueError("edge endpoint missing from the node index")
        self.n = len(self.roots)

    def mask_of(self, ids: set) -> np.ndarray:
        """Boolean node mask for a set of root ids."""
        return np.isin(self.roots.values, np.fromiter(ids, dtype=np.int64))

    def in_degree(self, dst: np.ndarray | None = None) -> np.ndarray:
        """In-degree of every node under the given target vector."""
        return np.bincount(self.dst if dst is None else dst, minlength=self.n)


def statistics(g: Graph, dst: np.ndarray, motor: np.ndarray,
               src_masks: dict) -> dict:
    """Compute R1, R2, P2 and H1 for every class under one edge assignment.

    ``dst`` is the (possibly randomised) target vector; every other input is
    held fixed, so out-degree is preserved by construction and in-degree is
    preserved whenever ``dst`` is a permutation of the observed targets.
    """
    motor_edge = motor[dst]
    into_motor = np.bincount(g.src[motor_edge], minlength=g.n).astype(np.int64)
    out = {}
    for name, edge_mask in src_masks.items():
        reached = np.bincount(dst[edge_mask], minlength=g.n)
        hop1 = reached > 0
        out[name] = {
            "R1": int((hop1 & motor).sum()),
            "R2": int(np.unique(dst[motor_edge & hop1[g.src]]).size),
            "P2": int(reached.astype(np.int64) @ into_motor),
            "H1": int(hop1.sum()),
        }
    out[MIRROR] = {"R1": 0, "R2": 0, "P2": int(motor_edge.sum()), "H1": 0}
    return out


def degree_guard(g: Graph, seed: int = 1000) -> dict:
    """Positive and negative control on the degree-preserving construction.

    A permutation must reproduce the observed in-degree vector exactly; an
    alternative construction drawing targets uniformly must not.  Without the
    negative control the check cannot fail and therefore measures nothing.
    """
    observed = g.in_degree()
    permuted = np.random.default_rng(seed).permutation(g.dst)
    uniform = np.random.default_rng(seed + 1).choice(g.n, g.dst.size)
    return {
        "permutation_preserves_in_degree":
            bool((g.in_degree(permuted) == observed).all()),
        "uniform_preserves_in_degree":
            bool((g.in_degree(uniform) == observed).all()),
        "nodes_with_in_degree_broken_by_uniform":
            int((g.in_degree(uniform) != observed).sum()),
        "nodes_total": int(g.n),
        "edges_retargeted_by_permutation": int((permuted != g.dst).sum()),
        "self_loops_observed": int((g.src == g.dst).sum()),
        "self_loops_permuted": int((g.src == permuted).sum()),
    }


def neuropil_blocks(g: Graph, pre_path: Path, post_path: Path) -> tuple:
    """Assign each neuron its dominant output and input neuropil.

    The dominant neuropil is the one holding the largest number of that
    neuron's presynaptic (respectively postsynaptic) sites.  Neurons with no
    recorded sites fall into a single explicit 'unassigned' block rather than
    being dropped, so no edge is silently discarded.
    """
    def dominant(path: Path, id_column: str) -> pd.Series:
        table = feather.read_feather(
            path, columns=[id_column, "neuropil", "count"])
        table = table.sort_values("count", ascending=False)
        table = table.drop_duplicates(subset=[id_column], keep="first")
        return pd.Series(table["neuropil"].values, index=table[id_column].values)

    out_np = dominant(pre_path, "pre_pt_root_id")
    in_np = dominant(post_path, "post_pt_root_id")
    labels = pd.Index(sorted(set(out_np.unique()) | set(in_np.unique())))
    code = {name: i for i, name in enumerate(labels)}
    unassigned = len(labels)

    def codes(series: pd.Series) -> np.ndarray:
        mapped = series.reindex(g.roots.values)
        return np.array([code.get(v, unassigned) for v in mapped.values],
                        dtype=np.int32)

    out_code, in_code = codes(out_np), codes(in_np)
    meta = {
        "neuropils": int(len(labels)),
        "neurons_without_output_neuropil": int((out_code == unassigned).sum()),
        "neurons_without_input_neuropil": int((in_code == unassigned).sum()),
        "labels": [str(x) for x in labels],
    }
    return out_code, in_code, meta


def neuropil_permutation(g: Graph, out_code: np.ndarray, in_code: np.ndarray,
                         rng: np.random.Generator) -> np.ndarray:
    """Permute targets only within groups of edges sharing the same
    (source neuropil, target neuropil) pair.

    This preserves the number of connections between every ordered pair of
    neuropils exactly, in addition to out-degree, and belongs to the same
    family as the neuropil-connection model of Lin et al. (2024).  In-degree
    is no longer preserved exactly, only within each block.
    """
    span = int(in_code.max()) + 1
    key = out_code[g.src].astype(np.int64) * span + in_code[g.dst]
    order = np.argsort(key, kind="stable")
    boundaries = np.flatnonzero(np.diff(key[order])) + 1
    permuted = g.dst.copy()
    for block in np.split(order, boundaries):
        if block.size > 1:
            permuted[block] = g.dst[rng.permutation(block)]
    return permuted


def ensemble(g: Graph, motor: np.ndarray, src_masks: dict, n_nulls: int,
             kind: str, out_code=None, in_code=None) -> list:
    """Realisations of one null family, seeds 1000 + 7i for reproducibility."""
    runs = []
    for i in range(n_nulls):
        rng = np.random.default_rng(1000 + 7 * i)
        if kind == "degree":
            dst = rng.permutation(g.dst)
        elif kind == "neuropil":
            dst = neuropil_permutation(g, out_code, in_code, rng)
        else:
            raise ValueError("unknown null family " + repr(kind))
        runs.append(statistics(g, dst, motor, src_masks))
        if (i + 1) % 10 == 0:
            log("    " + kind + " null " + str(i + 1) + "/" + str(n_nulls))
    return runs


def summarise(real: dict, runs: list) -> dict:
    """Observed value, ensemble moments, rank and ratio for every statistic.

    A zero standard deviation is labelled with its cause: 'conserved' when the
    ensemble equals the observed value, in which case the statistic cannot be
    tested at all, and 'saturated' when it does not, in which case the
    direction is valid but the effect size is not estimable.
    """
    out = {}
    for name in real:
        out[name] = {}
        for stat in real[name]:
            values = np.array([r[name][stat] for r in runs], dtype=float)
            observed = float(real[name][stat])
            mean, sd = float(values.mean()), float(values.std())
            out[name][stat] = {
                "observed": observed,
                "null_mean": round(mean, 3),
                "null_sd": round(sd, 3),
                "null_min": float(values.min()),
                "null_max": float(values.max()),
                "nulls_ge_observed": int((values >= observed).sum()),
                "ratio": round(observed / mean, 6) if mean else None,
                "z": round((observed - mean) / sd, 2) if sd > 0 else None,
                "sd_zero_reason": (
                    None if sd > 0
                    else "conserved" if mean == observed else "saturated"),
            }
    return out


def analyse(conn: Path, ann: Path, threshold: int, n_nulls: int,
            pre: Path | None, post: Path | None) -> dict:
    """One complete analysis at a given synapse threshold."""
    log("=== threshold " + str(threshold) + " ===")
    edges = pq.read_table(
        conn, columns=["Presynaptic_ID", "Postsynaptic_ID", "Connectivity"]
    ).to_pandas()
    total = len(edges)
    if threshold > 1:
        edges = edges[edges["Connectivity"].values >= threshold]
    log("  edges " + str(len(edges)) + " of " + str(total)
        + " (" + str(round(len(edges) / total, 4)) + " retained)")

    pre_ids = edges["Presynaptic_ID"].values
    post_ids = edges["Postsynaptic_ID"].values
    g = Graph(pre_ids, post_ids,
              np.union1d(np.unique(pre_ids), np.unique(post_ids)))
    log("  nodes " + str(g.n))

    a = pd.read_csv(ann, sep="\t", low_memory=False)
    motor110 = g.mask_of(set(a.loc[a["super_class"] == "motor", "root_id"]))
    motor105 = g.mask_of(
        set(a.loc[a["cell_class"] == "brain_motor_neuron", "root_id"]))
    log("  motor in graph: 110-definition " + str(int(motor110.sum()))
        + ", 105-definition " + str(int(motor105.sum())))

    node_masks = {c: g.mask_of(set(a.loc[a["cell_class"] == c, "root_id"]))
                  for c in CLASSES}
    control = np.zeros(g.n, dtype=bool)
    size = min(int(node_masks["visual"].sum()), g.n)
    control[np.random.default_rng(CONTROL_SEED).choice(
        g.n, size, replace=False)] = True
    node_masks[CONTROL] = control
    src_masks = {k: v[g.src] for k, v in node_masks.items()}
    log("  class sizes "
        + json.dumps({k: int(v.sum()) for k, v in node_masks.items()}))

    result = {
        "threshold": threshold,
        "edges": int(len(edges)),
        "edges_total": int(total),
        "nodes": int(g.n),
        "n_nulls": n_nulls,
        "motor_110": int(motor110.sum()),
        "motor_105": int(motor105.sum()),
        "class_sizes": {k: int(v.sum()) for k, v in node_masks.items()},
        "class_out_edges": {k: int(v.sum()) for k, v in src_masks.items()},
        "guard": degree_guard(g),
        "observed": statistics(g, g.dst, motor110, src_masks),
        "observed_105": statistics(g, g.dst, motor105, src_masks),
    }
    log("  guard " + json.dumps(result["guard"]))
    log("  observed " + json.dumps(result["observed"]))

    degree_runs = ensemble(g, motor110, src_masks, n_nulls, "degree")
    result["degree_null"] = summarise(result["observed"], degree_runs)
    result["degree_null_raw"] = degree_runs

    if (pre is not None and post is not None
            and pre.exists() and post.exists()):
        out_code, in_code, meta = neuropil_blocks(g, pre, post)
        result["neuropil_meta"] = meta
        log("  neuropil blocks " + json.dumps(
            {k: v for k, v in meta.items() if k != "labels"}))
        np_runs = ensemble(g, motor110, src_masks, n_nulls, "neuropil",
                           out_code, in_code)
        result["neuropil_null"] = summarise(result["observed"], np_runs)
        result["neuropil_null_raw"] = np_runs
    else:
        result["neuropil_null"] = None
        result["neuropil_null_raw"] = None
        result["neuropil_meta"] = {
            "status": "NOT MEASURED: neuropil files not supplied"}
        log("  neuropil ensemble NOT MEASURED (files absent)")

    for name in result["degree_null"]:
        log("  DEGREE " + name + " " + json.dumps(result["degree_null"][name]))
    if result["neuropil_null"]:
        for name in result["neuropil_null"]:
            log("  NEUROPIL " + name + " "
                + json.dumps(result["neuropil_null"][name]))
    return result


PALETTE = {
    "olfactory": "#b5651d",
    "visual": "#2f6f9f",
    "mechanosensory": "#3f7d3f",
    "gustatory": "#8a4b8a",
    CONTROL: "#8a8a8a",
}
PRETTY = {"olfactory": "Olfactory", "visual": "Visual",
          "mechanosensory": "Mechanosensory", "gustatory": "Gustatory",
          CONTROL: "Arbitrary control"}


def figures(runs: dict, outdir: Path) -> list:
    """Write the three SVG panels of the two-hop section."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    plt.rcParams.update({"font.size": 8, "svg.fonttype": "none",
                         "axes.spines.top": False,
                         "axes.spines.right": False})
    written = []
    names = CLASSES + [CONTROL]
    ordered = sorted(runs.items())

    # Panel a: observed two-hop path count against the ensembles.
    fig, axes = plt.subplots(1, len(ordered), figsize=(3.4 * len(ordered), 3.6),
                             squeeze=False)
    for ax, (threshold, res) in zip(axes[0], ordered):
        jitter = np.random.default_rng(1)
        for i, name in enumerate(names):
            for raw, shade, dx in ((res["degree_null_raw"], 0.40, -0.13),
                                   (res["neuropil_null_raw"], 0.85, 0.13)):
                if raw is None:
                    continue
                values = np.array([r[name]["P2"] for r in raw], dtype=float)
                ax.scatter(i + dx + jitter.normal(0, 0.035, values.size),
                           np.maximum(values, 0.6), s=5, alpha=shade,
                           color=PALETTE[name], edgecolors="none")
            observed = max(res["observed"][name]["P2"], 0.6)
            ax.scatter([i], [observed], marker="_", s=520,
                       color=PALETTE[name], linewidths=2.4, zorder=5)
        ax.set_yscale("log")
        ax.set_xticks(range(len(names)))
        ax.set_xticklabels([PRETTY[n] for n in names], rotation=40, ha="right")
        ax.set_title("threshold " + str(threshold) + " synapse"
                     + ("s" if threshold > 1 else "")
                     + "  (left degree, right neuropil)", fontsize=7)
        ax.set_ylabel("two-hop paths to motor neurons")
    fig.suptitle("a  Observed two-hop path count (dash) against 40 null "
                 "realizations (dots)", x=0.01, ha="left", fontsize=9)
    fig.tight_layout(rect=(0, 0, 1, 0.94))
    path = outdir / "fig_twohop_a_pathcount.svg"
    fig.savefig(path)
    plt.close(fig)
    written.append(path)

    # Panel b: reach at one and two hops, observed against the ensemble.
    fig, axes = plt.subplots(1, len(ordered), figsize=(3.4 * len(ordered), 3.6),
                             squeeze=False)
    for ax, (threshold, res) in zip(axes[0], ordered):
        width = 0.36
        for i, name in enumerate(names):
            for k, (stat, dx) in enumerate((("R1", -width / 2),
                                            ("R2", width / 2))):
                values = np.array([r[name][stat]
                                   for r in res["degree_null_raw"]], dtype=float)
                ax.bar(i + dx, values.mean(), width, yerr=values.std(),
                       color=PALETTE[name], alpha=0.25 if k == 0 else 0.5,
                       edgecolor="none", error_kw={"lw": 0.7})
                ax.scatter([i + dx], [res["observed"][name][stat]], s=18,
                           color=PALETTE[name], zorder=5,
                           marker="o" if k == 0 else "D")
        ax.axhline(res["motor_110"], ls=":", lw=0.8, color="k")
        ax.set_xticks(range(len(names)))
        ax.set_xticklabels([PRETTY[n] for n in names], rotation=40, ha="right")
        ax.set_ylabel("motor neurons reached")
        ax.set_title("threshold " + str(threshold)
                     + "  bars null, points observed;"
                     " circle 1 hop, diamond 2 hops", fontsize=7)
    fig.suptitle("b  Reach at one and two hops; dotted line is the whole motor "
                 "population", x=0.01, ha="left", fontsize=9)
    fig.tight_layout(rect=(0, 0, 1, 0.94))
    path = outdir / "fig_twohop_b_reach.svg"
    fig.savefig(path)
    plt.close(fig)
    written.append(path)

    # Panel c: ratios normalised by the arbitrary-control baseline.
    fig, ax = plt.subplots(figsize=(5.0, 3.6))
    marks = {1: "o", 5: "s"}
    for threshold, res in ordered:
        for family, key, edge in (("degree", "degree_null", "k"),
                                  ("neuropil", "neuropil_null", "#cc0000")):
            table = res.get(key)
            if not table:
                continue
            baseline = table[CONTROL]["P2"]["ratio"]
            dx = -0.16 if family == "degree" else 0.16
            for i, name in enumerate(CLASSES):
                ratio = table[name]["P2"]["ratio"] / baseline
                ax.scatter([i + dx], [max(ratio, 1e-4)], s=46,
                           color=PALETTE[name],
                           marker=marks.get(threshold, "^"),
                           edgecolors=edge, linewidths=0.8)
    ax.axhline(1.0, color="k", lw=0.8)
    ax.set_yscale("log")
    ax.set_xticks(range(len(CLASSES)))
    ax.set_xticklabels([PRETTY[n] for n in CLASSES], rotation=40, ha="right")
    ax.set_ylabel("two-hop path ratio, baseline-normalised")
    ax.set_title("circle threshold 1, square threshold 5; "
                 "black edge degree null, red edge neuropil null", fontsize=7)
    fig.suptitle("c  Enrichment relative to the arbitrary-neuron baseline",
                 x=0.01, ha="left", fontsize=9)
    fig.tight_layout(rect=(0, 0, 1, 0.94))
    path = outdir / "fig_twohop_c_normalised.svg"
    fig.savefig(path)
    plt.close(fig)
    written.append(path)
    return written


def main(argv: list | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--conn", type=Path, required=True)
    parser.add_argument("--ann", type=Path, required=True)
    parser.add_argument("--pre", type=Path, default=None)
    parser.add_argument("--post", type=Path, default=None)
    parser.add_argument("--nulls", type=int, default=40)
    parser.add_argument("--thresholds", type=int, nargs="+", default=[1, 5])
    parser.add_argument("--outdir", type=Path, default=Path("."))
    args = parser.parse_args(argv)

    args.outdir.mkdir(parents=True, exist_ok=True)
    started = time.time()
    results = {t: analyse(args.conn, args.ann, t, args.nulls, args.pre,
                          args.post) for t in args.thresholds}

    summary = {str(t): {k: v for k, v in r.items() if not k.endswith("_raw")}
               for t, r in results.items()}
    (args.outdir / "twohop_nulls.json").write_text(
        json.dumps(summary, indent=1))
    (args.outdir / "twohop_nulls_raw.json").write_text(json.dumps(
        {str(t): {"degree": r["degree_null_raw"],
                  "neuropil": r.get("neuropil_null_raw")}
         for t, r in results.items()}))

    for path in figures(results, args.outdir):
        log("figure written " + str(path))
    log("DONE in " + str(round(time.time() - started, 1)) + " s")
    return 0


if __name__ == "__main__":
    sys.exit(main())
