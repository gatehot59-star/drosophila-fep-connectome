#!/usr/bin/env python3
"""Escape-circuit specificity against a neuropil-preserving null.

The giant-fibre escape pathway of *Drosophila* receives strong input from two
visual projection cell types, LC4 and LPLC2, and no input at all from LC6, a
neighbouring type that also detects objects.  Whether that zero reflects an
active exclusion or merely the absence of a physical opportunity cannot be
decided by a degree-preserving null, which randomises targets across the whole
brain and therefore predicts connections between populations whose arbours
never meet.

This script decides it in two steps:

1. **Opportunity.**  Where does each population place its presynaptic sites,
   and where does the target receive its postsynaptic sites?  If the source's
   output neuropils do not overlap the target's input neuropils, the zero is
   geometry and no statistical test is needed.

2. **Specificity.**  If they do overlap, permute edge targets *within* groups
   of edges sharing the same ordered pair of (source neuropil, target
   neuropil).  Connections between any two neuropils are then conserved
   exactly, so a deficit measured against this ensemble cannot be explained by
   anatomical locality.  Same family as the neuropil-connection model of
   Lin et al. (2024).

Controls, all measured in the same run:
  - LC9 and LPLC1, further visual projection types not reported as escape
    inputs, to establish that the ensemble does not flag every LC type.
  - DNp09, the second descending channel, whose input the escape circuit does
    reach, as a positive control that the ensemble can return an excess.
  - A quantity conserved by construction, to show the statistics of interest
    are not conserved and therefore are testable.

Usage:
  python3 escape_neuropil_null.py --conn <parquet> --ann <tsv>
                                  --pre <feather> --post <feather>
                                  [--nulls 40] [--out results.json]
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

SOURCES = ["LC4", "LPLC2", "LC6", "LC9", "LPLC1"]
TARGETS = {"GF": "DNp01", "DNp09": "DNp09"}


def log(*a: object) -> None:
    """Print immediately so a backgrounded run can be polled with tail."""
    print(*a, flush=True)


def site_distribution(path: Path, id_column: str, populations: dict,
                      top: int = 6) -> dict:
    """Synapse sites per neuropil for each population, largest first.

    Returns the full distribution as well as the truncated view, because the
    overlap test needs every neuropil, not only the dominant ones.
    """
    table = feather.read_feather(path, columns=[id_column, "neuropil", "count"])
    out = {}
    for name, ids in populations.items():
        subset = table[table[id_column].isin(ids)]
        totals = subset.groupby("neuropil")["count"].sum().sort_values(
            ascending=False)
        out[name] = {
            "total_sites": int(totals.sum()),
            "neuropils": int(len(totals)),
            "top": {str(k): int(v) for k, v in totals.head(top).items()},
            "all": {str(k): int(v) for k, v in totals.items()},
        }
    return out


def opportunity(out_sites: dict, in_sites: dict, source: str,
                target: str) -> dict:
    """Shared neuropils between a source's output and a target's input.

    ``shared_min_sites`` is the limiting quantity: for a connection to be
    possible in a neuropil, both partners need sites there, so the smaller of
    the two counts bounds the opportunity.
    """
    src = out_sites[source]["all"]
    dst = in_sites[target]["all"]
    shared = sorted(set(src) & set(dst),
                    key=lambda k: -min(src[k], dst[k]))
    return {
        "shared_neuropils": len(shared),
        "top_shared": {k: {"source_output_sites": src[k],
                           "target_input_sites": dst[k]}
                       for k in shared[:5]},
        "shared_min_sites": int(sum(min(src[k], dst[k]) for k in shared)),
    }


def blocks_from_sites(root_ids: np.ndarray, pre: Path, post: Path) -> tuple:
    """Dominant output and input neuropil per neuron, as integer codes.

    Neurons with no recorded sites receive an explicit 'unassigned' code
    rather than being dropped, so no edge is silently discarded.
    """
    def dominant(path: Path, id_column: str) -> pd.Series:
        table = feather.read_feather(
            path, columns=[id_column, "neuropil", "count"])
        table = table.sort_values("count", ascending=False)
        table = table.drop_duplicates(subset=[id_column], keep="first")
        return pd.Series(table["neuropil"].values,
                         index=table[id_column].values)

    out_np, in_np = dominant(pre, "pre_pt_root_id"), dominant(post, "post_pt_root_id")
    labels = pd.Index(sorted(set(out_np.unique()) | set(in_np.unique())))
    code = {name: i for i, name in enumerate(labels)}
    unassigned = len(labels)

    def codes(series: pd.Series) -> np.ndarray:
        return np.array([code.get(v, unassigned)
                         for v in series.reindex(root_ids).values],
                        dtype=np.int32)

    return codes(out_np), codes(in_np), len(labels)


def pair_counts(src: np.ndarray, dst: np.ndarray, source_masks: dict,
                target_masks: dict) -> dict:
    """Edge count for every (source population, target population) pair."""
    out = {}
    for s_name, s_edges in source_masks.items():
        for t_name, t_nodes in target_masks.items():
            out[f"{s_name}->{t_name}"] = int((s_edges & t_nodes[dst]).sum())
    return out


def main(argv: list | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--conn", type=Path, required=True)
    parser.add_argument("--ann", type=Path, required=True)
    parser.add_argument("--pre", type=Path, required=True)
    parser.add_argument("--post", type=Path, required=True)
    parser.add_argument("--nulls", type=int, default=40)
    parser.add_argument("--threshold", type=int, default=1)
    parser.add_argument("--out", type=Path, default=Path("escape_null.json"))
    args = parser.parse_args(argv)

    started = time.time()
    a = pd.read_csv(args.ann, sep="\t", low_memory=False)
    pops = {n: set(a.loc[a["cell_type"] == n, "root_id"]) for n in SOURCES}
    pops.update({k: set(a.loc[a["cell_type"] == v, "root_id"])
                 for k, v in TARGETS.items()})
    log("populations " + json.dumps({k: len(v) for k, v in pops.items()}))

    # Step 1: opportunity, which can settle the question without any null.
    out_sites = site_distribution(args.pre, "pre_pt_root_id", pops)
    in_sites = site_distribution(args.post, "post_pt_root_id", pops)
    log("output sites " + json.dumps(
        {k: v["top"] for k, v in out_sites.items()}))
    log("input sites " + json.dumps(
        {k: v["top"] for k, v in in_sites.items()}))

    opportunities = {}
    for s in SOURCES:
        for t in TARGETS:
            opportunities[f"{s}->{t}"] = opportunity(out_sites, in_sites, s, t)
    log("opportunity " + json.dumps(opportunities))

    # Step 2: the null, restricted to neuropil blocks.
    edges = pq.read_table(args.conn, columns=[
        "Presynaptic_ID", "Postsynaptic_ID", "Connectivity"]).to_pandas()
    if args.threshold > 1:
        edges = edges[edges["Connectivity"].values >= args.threshold]
    pre_ids = edges["Presynaptic_ID"].values
    post_ids = edges["Postsynaptic_ID"].values
    roots = pd.Index(np.union1d(np.unique(pre_ids), np.unique(post_ids)))
    src = roots.get_indexer(pre_ids).astype(np.int32)
    dst = roots.get_indexer(post_ids).astype(np.int32)
    n = len(roots)
    log(f"graph nodes {n} edges {len(src)}")

    node = {k: np.isin(roots.values, np.fromiter(v, dtype=np.int64))
            for k, v in pops.items()}
    log("populations in graph " + json.dumps(
        {k: int(v.sum()) for k, v in node.items()}))
    source_masks = {s: node[s][src] for s in SOURCES}
    target_masks = {t: node[t] for t in TARGETS}

    out_code, in_code, n_labels = blocks_from_sites(roots.values, args.pre,
                                                    args.post)
    log(f"neuropil labels {n_labels} "
        f"unassigned_out {int((out_code == n_labels).sum())} "
        f"unassigned_in {int((in_code == n_labels).sum())}")

    span = int(in_code.max()) + 1
    key = out_code[src].astype(np.int64) * span + in_code[dst]
    order = np.argsort(key, kind="stable")
    boundaries = np.flatnonzero(np.diff(key[order])) + 1
    blocks = [b for b in np.split(order, boundaries) if b.size > 1]
    log(f"blocks with more than one edge {len(blocks)}")

    observed = pair_counts(src, dst, source_masks, target_masks)
    observed["_MIRROR_edges_into_GF"] = int(node["GF"][dst].sum())
    log("observed " + json.dumps(observed))

    runs = []
    for i in range(args.nulls):
        rng = np.random.default_rng(1000 + 7 * i)
        permuted = dst.copy()
        for block in blocks:
            permuted[block] = dst[rng.permutation(block)]
        counts = pair_counts(src, permuted, source_masks, target_masks)
        counts["_MIRROR_edges_into_GF"] = int(node["GF"][permuted].sum())
        runs.append(counts)
        if (i + 1) % 10 == 0:
            log(f"  null {i + 1}/{args.nulls}")

    summary = {}
    for pair, value in observed.items():
        values = np.array([r[pair] for r in runs], dtype=float)
        mean, sd = float(values.mean()), float(values.std())
        summary[pair] = {
            "observed": int(value),
            "null_mean": round(mean, 3),
            "null_sd": round(sd, 3),
            "null_min": int(values.min()),
            "null_max": int(values.max()),
            "nulls_ge_observed": int((values >= value).sum()),
            "nulls_le_observed": int((values <= value).sum()),
            "ratio": round(value / mean, 4) if mean else None,
            "z": round((value - mean) / sd, 2) if sd > 0 else None,
            "sd_zero_reason": (
                None if sd > 0
                else "conserved" if mean == value else "saturated"),
        }
        log("RESULT " + pair + " " + json.dumps(summary[pair]))

    args.out.write_text(json.dumps({
        "threshold": args.threshold,
        "nulls": args.nulls,
        "populations": {k: len(v) for k, v in pops.items()},
        "output_sites": out_sites,
        "input_sites": in_sites,
        "opportunity": opportunities,
        "summary": summary,
        "raw": runs,
    }, indent=1))
    log(f"DONE in {round(time.time() - started, 1)} s -> {args.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
