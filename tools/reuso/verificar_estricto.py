#!/usr/bin/env python3
"""tools/reuso/verificar_estricto.py: recompute inference from the published raw draws.

This verifier does not import the experimental module. It checks exact rational
T1 comparisons, Holm correction, coverage, guards, and the independent log copy.
Usage: python verificar_estricto.py --json estricto.json --log run.log
"""
from __future__ import annotations
import argparse
import copy
from fractions import Fraction
import hashlib
import json
import math
from pathlib import Path
from typing import Any

SOURCE = "a0d35aa1810e6513bbacaba36ce17b768c3792132cf86b20012ae2d754588083"
COMMIT = "5497aa569450415b2101e2ea0f99680a3c540dbe"
SEAL = "08987f3208aa395421766bc15043ddb82b4da429"
EXPECTED = {"flywire": (996, 880, 698, 1118, 12029), "banc": (753, 622, 419, 716, 12030)}
INPUT_PINS = {
    "connectivity.parquet": (100804642, "3d802fd542b5d18570ba1ba0bb0abed9", "efeb23fb99098e9c390f6869969b2a121a2ee92c833cfc45ecb2c1d8e1af0347"),
    "annotations.tsv": (31718505, "719904abad876c68ace1b5690c9b9b63", "9a4f8b2f843196074431ebd7cd883536afa1be86c8a4ce90970441e8be81d1be"),
    "banc_888_meta.feather": (57503026, "8c2b93a608c7163ec9d94d68e0756ff4", "86ccf5df0c67419f8c5f43e93a7ed38d23a080e9f7fde26737290252f3780098"),
    "banc_888_edgelist_simple_v3.feather": (359161658, "08542b0771db7418ed474be60dc9886c", "8c296e946f3c69a8c7222f30ad75fa8a98eeb189124fec6df829c9125f4be64b"),
}


def require(condition: bool, label: str) -> None:
    """Raise a labelled failure rather than returning a partial green."""
    if not condition:
        raise ValueError(label)


def verify(result: dict[str, Any], log: str) -> dict[str, Any]:
    """Validate complete real-data evidence and derive inference without the producer."""
    require(result["status"] == "VALID" and result["mode"] == "full" and result["exit_code"] == 0, "run not valid/full")
    env = result["environment"]
    require(env["source_sha256"] == SOURCE and env["github_sha"] == COMMIT and env["seal_blob"] == SEAL, "source or seal mismatch")
    require(result["selftest"]["passed"] == result["selftest"]["total"] == 25, "selftests incomplete")
    require(set(result["inputs"]) == set(INPUT_PINS), "input population mismatch")
    for name, expected in INPUT_PINS.items():
        got = result["inputs"][name]
        require((got["bytes"], got["md5"], got["sha256"]) == expected, "input identity mismatch")
    lines = log.splitlines()
    starts = [i for i, line in enumerate(lines) if line.startswith("ENVIRONMENT ") and json.loads(line[12:]) == env]
    require(len(starts) == 1, "real run environment missing or duplicated in log")
    raw = {name: [] for name in EXPECTED}
    for line in lines[starts[0] + 1:]:
        if line.startswith("NULL "):
            row = json.loads(line[5:])
            name = row.pop("connectome")
            require(name in raw, "unexpected connectome in log")
            raw[name].append(row)
    ps: list[Fraction] = []
    out: dict[str, Any] = {"scope": "two fixed connectomes, 200 strict nulls each", "connectomes": {}}
    for name, (nc, nf, t2, nx, seed) in EXPECTED.items():
        g = result["connectomes"][name]
        o, rows = g["observed"], g["nulls"]
        require(g["seed"] == seed and g["count_expected"] == 200, "seed or count mismatch")
        require(len(rows) == 200 and [r["draw"] for r in rows] == list(range(200)), "incomplete plan")
        require(len({r["targets_sha256"] for r in rows}) == 200, "duplicate target vector")
        require(raw[name] == rows, "JSON and verbatim log disagree")
        require((o["n_cab"], o["n_pares_ffi"], o["t2"], o["n_x"]) == (nc, nf, t2, nx), "baseline changed")
        require(o["t1"] == nf / nc, "observed T1 mismatch")
        require(g["control"]["passed"] and g["fixed_arrays_unchanged"], "control/fixed arrays failed")
        smoke = result["smoke"][name]
        require(smoke["seed"] == seed + 900000 and len(smoke["guards"]) == 2 and smoke["fixed_arrays_unchanged"], "smoke plan failed")
        require(all(r["ok"] for r in smoke["guards"]), "smoke guard failed")
        for r in rows:
            require(r["guard"]["ok"] and all(r["guard"]["checks"].values()), "failed invariant")
            require(all(r["guard"]["moved"][k] > .5 for k in ("all", "SD", "SX", "XD")), "mixing failed")
            require(r["n_cab"] > 0 and r["t1"] == r["n_pares_ffi"] / r["n_cab"], "null T1 mismatch")
        require(rows[0]["guard"]["budget_recomputed"] and rows[-1]["guard"]["budget_recomputed"], "budget check failed")
        require(all(any(r[k] != o[k] for r in rows) for k in ("t1", "t2")), "statistic fixed at observed")
        exceed = [sum(r["n_pares_ffi"] * nc >= nf * r["n_cab"] for r in rows), sum(r["t2"] >= t2 for r in rows)]
        p = [Fraction(1 + value, 201) for value in exceed]
        require([float(x) for x in p] == g["p"], "producer p does not recompute")
        ps.extend(p)
        summaries = {k: {"observed": o[k], "mean": math.fsum(r[k] for r in rows) / 200,
                          "min": min(r[k] for r in rows), "max": max(r[k] for r in rows)} for k in ("t1", "t2", "n_cab")}
        class_counts = g["control"]["descriptive"]["shared_X_by_superclass"]
        require(sum(x["count"] for x in class_counts) == t2, "descriptive class counts do not sum to T2")
        out["connectomes"][name] = dict(nulls=200, distinct_targets=200, guards_pass=200, exceed=exceed,
            p=[str(x) for x in p], summaries=summaries,
            min_moved={k: min(r["guard"]["moved"][k] for r in rows) for k in ("all", "SD", "SX", "XD")},
            descriptive=g["control"]["descriptive"], seconds=g["seconds"], neurons=g["neurons"], rows=g["rows"], strata=g["strata"])
    order = sorted(range(4), key=lambda i: ps[i])
    adjusted = [Fraction(0) for _ in ps]
    previous = Fraction(0)
    for rank, i in enumerate(order):
        previous = max(previous, min(Fraction(1), (4 - rank) * ps[i]))
        adjusted[i] = previous
    require([float(x) for x in ps] == result["p"], "global p mismatch")
    require([float(x) for x in adjusted] == result["holm"], "Holm mismatch")
    labels = []
    for offset in (0, 2):
        label = ("SOSTENIDA" if all(x < Fraction(1, 20) for x in adjusted[offset:offset+2]) else
                 "REFUTADA" if all(x >= Fraction(1, 20) for x in ps[offset:offset+2]) else "PARCIAL")
        labels.append(label)
    final = ("SOSTENIDA" if labels == ["SOSTENIDA", "SOSTENIDA"] else
             "REFUTADA" if labels[0] == "REFUTADA" else
             "NO_SE_REPLICA" if labels == ["SOSTENIDA", "REFUTADA"] else "SIN_DECIDIR")
    require(labels[0] == result["H_REUSO_ESTRICTO_FLYWIRE"] and labels[1] == result["H_REUSO_ESTRICTO_BANC"]
            and final == result["H_REUSO_ESTRICTO"], "verdict mismatch")
    out.update(holm=[str(x) for x in adjusted], per_connectome=labels, verdict=final,
               seconds=result["seconds"], maxrss_gib=result["maxrss_kib"] / (1024 ** 2))
    return out


def main() -> int:
    """Verify the real files, then prove rejection of four corrupted receipts."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", type=Path, required=True)
    parser.add_argument("--log", type=Path, required=True)
    args = parser.parse_args()
    jb, lb = args.json.read_bytes(), args.log.read_bytes()
    result, text = json.loads(jb), lb.decode()
    out = verify(result, text)
    require("MUTATION_PROCESS_EXIT 3" in text and '"name": "class_swap_rejected", "ok": false' in text,
            "workflow mutation evidence missing")
    require("E2E_POSITIVE_AND_NEGATIVE_PASS" in text, "workflow positive/negative end-to-end missing")
    for mode in ("missing_draw", "changed_p", "guard_disabled", "wrong_source"):
        broken = copy.deepcopy(result)
        if mode == "missing_draw": broken["connectomes"]["flywire"]["nulls"].pop()
        if mode == "changed_p": broken["holm"][0] = 0.75
        if mode == "guard_disabled": broken["connectomes"]["banc"]["nulls"][0]["guard"]["ok"] = False
        if mode == "wrong_source": broken["environment"]["source_sha256"] = "changed"
        try:
            verify(broken, text)
        except ValueError as exc:
            print("NEGATIVE_REJECTED", mode, str(exc))
        else:
            raise AssertionError("verifier accepted " + mode)
    print("RAW_JSON_SHA256", hashlib.sha256(jb).hexdigest(), "BYTES", len(jb))
    print("RAW_LOG_SHA256", hashlib.sha256(lb).hexdigest(), "BYTES", len(lb))
    print("RECOMPUTED", json.dumps(out, ensure_ascii=False, sort_keys=True))
    print("VERIFY_PASS 400/400 nulls; exact rational p; Holm; log parity; four negative controls")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
