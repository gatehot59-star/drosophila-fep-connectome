#!/usr/bin/env python3
"""tools/reuso/reuso_estricto.py: null conditioned on target superclass.

Scientific contract: SELLO-ESTRICTO-2026-11-01.md, committed before this file.
The historical statistics are imported unchanged after checking their bytes.
Run: python tools/reuso/reuso_estricto.py --mode selftest
Full: add --mode full --inputs-dir /tmp/reuso-input --out result.json.
No network, credentials, pickle loading, or git writes occur in this module.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from datetime import datetime, timezone
import gc
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import platform
import resource
import sys
import time
import traceback
from typing import Any

import numpy as np
import pandas as pd
import pyarrow

Graph = dict[str, Any]
HERE = Path(__file__).resolve().parent
BASE_BLOB = "37b358353ccac46c4b84766f1a63df556dfe531d"
TEST_BLOB = "c56be19ab3fe1637c3836c1abe451fadab569192"
SEAL_BLOB = "08987f3208aa395421766bc15043ddb82b4da429"
SEAL_COMMIT = "750f89adb4b8710bd0d4d7105af1c7073296dd90"
N_NULL = 200
SEEDS = {"flywire": 12029, "banc": 12030}
SMOKE_SEEDS = {"flywire": 912029, "banc": 912030}
VERSIONS = {"numpy": "2.5.3", "pandas": "3.0.5", "pyarrow": "25.0.1"}
PINS = {
    "connectivity.parquet": (100804642, "3d802fd542b5d18570ba1ba0bb0abed9", "efeb23fb99098e9c390f6869969b2a121a2ee92c833cfc45ecb2c1d8e1af0347"),
    "annotations.tsv": (31718505, "719904abad876c68ace1b5690c9b9b63", "9a4f8b2f843196074431ebd7cd883536afa1be86c8a4ce90970441e8be81d1be"),
    "banc_888_meta.feather": (57503026, "8c2b93a608c7163ec9d94d68e0756ff4", "86ccf5df0c67419f8c5f43e93a7ed38d23a080e9f7fde26737290252f3780098"),
    "banc_888_edgelist_simple_v3.feather": (359161658, "08542b0771db7418ed474be60dc9886c", "8c296e946f3c69a8c7222f30ad75fa8a98eeb189124fec6df829c9125f4be64b"),
}
BASELINE = {
    "flywire": dict(n_cab=996, n_pares_ffi=880, t1=880 / 996, t2=698, n_x=1118),
    "banc": dict(n_cab=753, n_pares_ffi=622, t1=622 / 753, t2=419, n_x=716),
}


def blob(data: bytes) -> str:
    """Compute Git blob identity, including the object header."""
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()


def pinned_module(name: str, filename: str, expected: str) -> Any:
    """Reject changed source before importing the local, pinned Python module."""
    path = HERE / filename
    if blob(path.read_bytes()) != expected:
        raise ValueError("source pin mismatch: " + filename)
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise ImportError(filename)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


base = pinned_module("reuso_mosca", "reuso_mosca.py", BASE_BLOB)


def emit(label: str, value: Any) -> None:
    """Print a structured measurement, without trimming its contents."""
    print(label + " " + json.dumps(value, ensure_ascii=False, sort_keys=True, allow_nan=False), flush=True)


def checkpoint(path: Path, result: dict[str, Any]) -> None:
    """Atomically retain progress; incomplete results are never labelled valid."""
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(result, indent=2, ensure_ascii=False, allow_nan=False) + "\n", encoding="utf-8")
    temporary.replace(path)


def metadata(path: Path) -> dict[str, Any]:
    """Hash an actual input by streaming its bytes; missing files fail loudly."""
    md5, sha = hashlib.md5(), hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 22), b""):
            md5.update(chunk)
            sha.update(chunk)
    return dict(bytes=path.stat().st_size, md5=md5.hexdigest(), sha256=sha.hexdigest())


def validate_inputs(directory: Path) -> dict[str, Any]:
    """Require all four complete byte pins, not merely the historical prefixes."""
    observed = {}
    for filename, expected in PINS.items():
        got = metadata(directory / filename)
        ok = (got["bytes"], got["md5"], got["sha256"]) == expected
        emit("INPUT", dict(file=filename, **got, ok=ok))
        if not ok:
            raise ValueError("input pin mismatch: " + filename)
        observed[filename] = got
    return observed


def attach(pre: np.ndarray, post: np.ndarray, w: np.ndarray, inh: np.ndarray,
           types: np.ndarray, sides: np.ndarray, classes: np.ndarray, ids: np.ndarray) -> Graph:
    """Build the unchanged historical graph while retaining aligned identities."""
    if len(ids) != len(types) or len(set(ids.tolist())) != len(ids):
        raise ValueError("nonunique or misaligned neuron IDs")
    if len(pre) == 0 or len(pre) != len(post) or len(pre) != len(w):
        raise ValueError("empty or misaligned edge arrays")
    if min(int(pre.min()), int(post.min())) < 0 or max(int(pre.max()), int(post.max())) >= len(ids):
        raise ValueError("edge endpoint outside metadata")
    if not np.all(w > 0) or not np.all(w == w.astype(np.int64)) or int(w.max()) > np.iinfo(np.int32).max:
        raise ValueError("weights must be positive int32 integers")
    if int(np.sum(w, dtype=np.int64)) >= 2 ** 53:
        raise ValueError("weighted bincount would exceed exact integer float64 range")
    d = base.armar(pre.astype(np.int32), post.astype(np.int32), w, inh, types, sides, classes)
    d["ids"], d["sc"] = np.asarray(ids), np.asarray(classes, dtype=object)
    return d


def load_graph(name: str, directory: Path) -> Graph:
    """Read exactly the columns and ID alignment used by the historical loaders."""
    if name == "flywire":
        a = pd.read_csv(directory / "annotations.tsv", sep=chr(9), dtype=str,
                        usecols=["root_id", "cell_type", "side", "super_class"])
        a["root_id"] = a.root_id.astype(np.int64)
        c = pd.read_parquet(directory / "connectivity.parquet",
                            columns=["Presynaptic_ID", "Postsynaptic_ID", "Connectivity", "Excitatory"])
        ids, inv = np.unique(np.concatenate([c.Presynaptic_ID.to_numpy(), c.Postsynaptic_ID.to_numpy()]),
                             return_inverse=True)
        count = len(c)
        pre, post = inv[:count].astype(np.int32), inv[count:].astype(np.int32)
        inh = np.zeros(len(ids), dtype=bool)
        inh[pre[c.Excitatory.to_numpy() < 0]] = True
        weights = c.Connectivity.to_numpy().copy()
        del c, inv
        a = a.drop_duplicates("root_id").set_index("root_id").reindex(ids)
        return attach(pre, post, weights, inh, a.cell_type.to_numpy(), a.side.to_numpy(), a.super_class.to_numpy(), ids)
    if name != "banc":
        raise ValueError("unknown connectome: " + name)
    m = pd.read_feather(directory / "banc_888_meta.feather",
                        columns=["root_888", "side", "super_class", "cell_type", "fafb_cell_type", "neurotransmitter_predicted"])
    m = m.drop_duplicates("root_888").reset_index(drop=True)
    edges = pd.read_feather(directory / "banc_888_edgelist_simple_v3.feather", columns=["pre", "post", "count"])
    ix = pd.Index(m.root_888.astype(str))
    pre = ix.get_indexer(edges.pre.astype(str)).astype(np.int32)
    post = ix.get_indexer(edges.post.astype(str)).astype(np.int32)
    weights = edges["count"].to_numpy().copy()
    del edges
    inh = m.neurotransmitter_predicted.isin(["gaba", "glutamate"]).to_numpy()
    types = m.fafb_cell_type.where(m.fafb_cell_type.notna(), m.cell_type).to_numpy()
    return attach(pre, post, weights, inh, types, m.side.to_numpy(), m.super_class.to_numpy(), ix.to_numpy())


def prepare(d: Graph) -> Graph:
    """Construct target-class/side strata and immutable reference invariants."""
    classes, names = pd.factorize(d["sc"], sort=True, use_na_sentinel=True)
    d["sc_code"] = (classes + 1).astype(np.int32)
    d["class_labels"] = [None] + [str(x) for x in names]
    d["n_classes"] = len(names) + 1
    pre, post, side = d["pre"], d["post"], d["sl"]
    code = (side[pre].astype(np.int32) * 3 + side[post]) * d["n_classes"] + d["sc_code"][post]
    order = np.argsort(code, kind="stable").astype(np.int32)
    values, starts = np.unique(code[order], return_index=True)
    d["strict_order"], d["strict_bounds"] = order, np.r_[starts, len(order)]
    d["strata"] = int(len(values))
    d["pre_groups"] = [np.flatnonzero(side[pre] == s).astype(np.int32) for s in range(3)]
    d["incoming_by_pre_side"] = [np.bincount(post[g], minlength=d["n"]) for g in d["pre_groups"]]
    xs = d["inh"] & ~d["excl"]
    d["mix_masks"] = {
        "SD": (d["S"][pre] >= 0) & (d["D"][post] >= 0),
        "SX": (d["S"][pre] >= 0) & xs[post],
        "XD": xs[pre] & (d["D"][post] >= 0),
    }
    for key in ("pre", "post", "w", "inh"):
        d[key].setflags(write=False)
    d["fixed_hashes"] = {key: hashlib.sha256(d[key].tobytes()).hexdigest() for key in ("pre", "w", "inh")}
    return d


def strict_null(d: Graph, rng: np.random.Generator) -> np.ndarray:
    """Uniformly permute original target stubs independently within each stratum."""
    old, order, bounds = d["post"], d["strict_order"], d["strict_bounds"]
    new = old.copy()
    for lo, hi in zip(bounds[:-1], bounds[1:]):
        rows = order[lo:hi]
        if len(rows) > 1:
            new[rows] = old[rows][rng.permutation(len(rows))]
    return new


def guard(d: Graph, new: np.ndarray) -> dict[str, Any]:
    """Check actual shuffled endpoints, including a separate mixing gate per arm."""
    index_ok = bool(new.shape == d["post"].shape and np.issubdtype(new.dtype, np.integer)
                    and len(new) > 0 and new.min() >= 0 and new.max() < d["n"])
    if not index_ok:
        return dict(ok=False, index=False)
    old = d["post"]
    moved = new != old
    fractions = {"all": float(moved.mean())}
    for key, mask in d["mix_masks"].items():
        fractions[key] = float(moved[mask].mean()) if mask.any() else 0.0
    checks = dict(
        index=True,
        target_class=bool(np.array_equal(d["sc_code"][new], d["sc_code"][old])),
        target_side=bool(np.array_equal(d["sl"][new], d["sl"][old])),
        incoming_by_pre_side=all(np.array_equal(np.bincount(new[g], minlength=d["n"]), ref)
                                 for g, ref in zip(d["pre_groups"], d["incoming_by_pre_side"])),
        mixing=all(value > 0.5 for value in fractions.values()),
    )
    return dict(ok=all(checks.values()), checks=checks, moved=fractions)


def budgets(d: Graph, post: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """Independently recalculate outgoing row counts and weights by target class/side."""
    key = (d["pre"].astype(np.int64) * d["n_classes"] + d["sc_code"][post]) * 3 + d["sl"][post]
    length = d["n"] * d["n_classes"] * 3
    return np.bincount(key, minlength=length), np.bincount(key, weights=d["w"], minlength=length)


def nonfrozen(observed: dict[str, Any], draws: list[dict[str, Any]]) -> bool:
    """Reject a statistic fixed at the observed value in the entire measured ensemble."""
    return bool(draws) and all(any(row[key] != observed[key] for row in draws) for key in ("t1", "t2"))


def complete_plan(draws: list[dict[str, Any]], count: int) -> bool:
    """Require every draw exactly once, with a distinct target vector and valid guards."""
    return (len(draws) == count and [row["draw"] for row in draws] == list(range(count))
            and len({row["targets_sha256"] for row in draws}) == count
            and all(row["guard"]["ok"] for row in draws))


def naive_stats(d: Graph, post: np.ndarray) -> dict[str, Any]:
    """Independent small-graph oracle using dictionaries and explicit path enumeration."""
    sd, sx, xd = defaultdict(int), defaultdict(int), defaultdict(int)
    xs = d["inh"] & ~d["excl"]
    for a, b, w in zip(d["pre"].tolist(), post.tolist(), d["w"].tolist()):
        s, z = int(d["S"][a]), int(d["D"][b])
        if s >= 0 and z >= 0:
            sd[s, z] += w
        if s >= 0 and xs[b]:
            sx[s, b] += w
        if xs[a] and z >= 0:
            xd[a, z] += w
    cables = {(s, z) for (s, z), w in sd.items() if w >= 20 and d["cs"][s][1] == d["cd"][z][1]}
    pairs, per_x = set(), defaultdict(set)
    for s, z in cables:
        for x in np.flatnonzero(xs).tolist():
            if sx[s, x] >= 5 and xd[x, z] >= 5:
                pairs.add((s, z))
                per_x[x].add(d["cd"][z][0])
    return dict(n_cab=len(cables), n_pares_ffi=len(pairs), t1=len(pairs) / len(cables) if cables else 0.0,
                t2=sum(len(t) >= 2 for t in per_x.values()), n_x=len(per_x))


def fixture(positive: bool = True) -> Graph:
    """Create matched-degree/class synthetic graphs with planted or absent FFI reuse."""
    types, sides, classes, inhibitory, edges = [], [], [], [], []
    def neuron(t: str, side: str, sc: str | None, inh: bool = False) -> int:
        types.append(t); sides.append(side); classes.append(sc); inhibitory.append(inh)
        return len(types) - 1
    ss, dd, xx, cc = [], [], [], []
    for i in range(24):
        side = "left" if i % 2 == 0 else "right"
        ss.append(neuron("S" + str(i), side, "visual_projection"))
        dd.append([neuron("D" + str(i) + suffix, side, "descending") for suffix in ("a", "b")])
        xx.append(neuron("X" + str(i), side, "central", True))
        cc.append(neuron("C" + str(i), side, "central"))
    for i in range(24):
        edges.extend((ss[i], z, 30) for z in dd[i])
        edges.append((ss[i], xx[i], 8))
        target = i if positive else (i + 2) % 24
        edges.extend((xx[i], z, 8) for z in dd[target])
        edges.extend([(xx[i], cc[i], 8), (cc[i], xx[i], 8)])
    u = neuron("U", "left", None)
    v = neuron("V", "left", None)
    edges.extend([(cc[0], u, 3), (cc[2], v, 4)])
    e = np.asarray(edges, dtype=np.int64)
    return prepare(attach(e[:, 0], e[:, 1], e[:, 2], np.asarray(inhibitory), np.asarray(types, dtype=object),
                          np.asarray(sides, dtype=object), np.asarray(classes, dtype=object), np.arange(len(types)) + 1000))


def selftest() -> dict[str, Any]:
    """Execute historical regression plus strict-null fixtures and deliberate mutations."""
    results = []
    def check(name: str, ok: bool, details: Any = None) -> None:
        results.append(dict(name=name, ok=bool(ok), details=details))
        emit("TEST", results[-1])
    regression = pinned_module("prueba_reuso", "prueba_reuso.py", TEST_BLOB)
    check("historical_seven_tests", regression.main() == 0)
    check("source_pin_rejects_changed_bytes", blob((HERE / "reuso_mosca.py").read_bytes() + b" ") != BASE_BLOB)
    d = fixture()
    check("ids_and_missing_classes_retained", len(set(d["ids"])) == d["n"] and int((d["sc_code"] == 0).sum()) == 2)
    obs = base.estadisticas(d, d["post"])
    check("independent_oracle_observed", obs == naive_stats(d, d["post"]), obs)
    check("planted_exact", obs["t1"] == 1.0 and obs["t2"] == 24)
    rng = np.random.default_rng(441)
    draws, nulls, guard_ok, oracle_ok, budget_ok = [], [], True, True, True
    reference_budget = budgets(d, d["post"])
    for k in range(39):
        new = strict_null(d, rng)
        value, guarded = base.estadisticas(d, new), guard(d, new)
        guard_ok &= guarded["ok"]
        oracle_ok &= value == naive_stats(d, new)
        budget_ok &= all(np.array_equal(a, b) for a, b in zip(reference_budget, budgets(d, new)))
        draws.append(dict(draw=k, targets_sha256=hashlib.sha256(new.tobytes()).hexdigest(), guard=guarded, **value))
        nulls.append(new)
    check("independent_oracle_39_nulls", oracle_ok)
    check("strict_guards_39_nulls", guard_ok)
    check("outgoing_counts_and_weights_39_nulls", budget_ok)
    check("planted_enrichment_both_metrics", all(obs[k] > max(x[k] for x in draws) for k in ("t1", "t2")),
          {k: dict(observed=obs[k], null_max=max(x[k] for x in draws)) for k in ("t1", "t2")})
    negative = fixture(False)
    nobs = base.estadisticas(negative, negative["post"])
    ndraws = [base.estadisticas(negative, strict_null(negative, np.random.default_rng(500 + k))) for k in range(39)]
    check("absent_motif_can_refute", nobs["t1"] == 0.0 and nobs["t2"] == 0 and
          all((1 + sum(x[k] >= nobs[k] for x in ndraws)) / 40 == 1.0 for k in ("t1", "t2")), nobs)
    check("statistic_not_fixed", nonfrozen(obs, draws))
    check("frozen_ensemble_rejected", not nonfrozen(obs, [obs.copy() for _ in range(200)]))
    check("complete_plan_39", complete_plan(draws, 39))
    check("missing_draw_rejected", not complete_plan(draws[:-1], 39))
    duplicate = [dict(x) for x in draws]
    duplicate[-1]["targets_sha256"] = duplicate[0]["targets_sha256"]
    check("duplicate_draw_rejected", not complete_plan(duplicate, 39))
    check("seed_reproducibility", np.array_equal(strict_null(d, np.random.default_rng(111)), strict_null(d, np.random.default_rng(111))))
    check("seed_changes_draw", not np.array_equal(strict_null(d, np.random.default_rng(111)), strict_null(d, np.random.default_rng(112))))
    identity = guard(d, d["post"].copy())
    check("identity_shuffle_rejected", not identity["ok"] and not identity["checks"]["mixing"])
    old_null = guard(d, base.nulo(d, np.random.default_rng(7)))
    check("old_SL_null_rejected", not old_null["ok"] and not old_null["checks"]["target_class"])
    mutated = nulls[0].copy()
    a = int(np.flatnonzero((d["sl"][mutated] == 0) & (d["sc_code"][mutated] == d["sc_code"][d["post"][0]]))[0])
    b = int(np.flatnonzero((d["sl"][mutated] == 0) & (d["sc_code"][mutated] != d["sc_code"][mutated[a]]))[0])
    mutated[a], mutated[b] = mutated[b], mutated[a]
    check("class_swap_rejected", not guard(d, mutated)["checks"]["target_class"])
    mutated = nulls[0].copy()
    a, b = int(np.flatnonzero(d["sl"][mutated] == 0)[0]), int(np.flatnonzero(d["sl"][mutated] == 1)[0])
    mutated[a], mutated[b] = mutated[b], mutated[a]
    check("side_swap_rejected", not guard(d, mutated)["checks"]["target_side"])
    mutated = nulls[0].copy()
    a = 0
    options = np.flatnonzero((d["sc_code"] == d["sc_code"][mutated[a]]) & (d["sl"] == d["sl"][mutated[a]]) & (np.arange(d["n"]) != mutated[a]))
    mutated[a] = options[0]
    check("incoming_histogram_mutation_rejected", not guard(d, mutated)["checks"]["incoming_by_pre_side"])
    mutated = nulls[0].copy(); mutated[0] = -1
    check("invalid_index_rejected", not guard(d, mutated)["ok"])
    check("wrong_shape_rejected", not guard(d, nulls[0][:-1])["ok"])
    fixed = {key: hashlib.sha256(d[key].tobytes()).hexdigest() for key in d["fixed_hashes"]}
    check("source_weights_sign_unchanged", fixed == d["fixed_hashes"])
    total = dict(passed=sum(x["ok"] for x in results), total=len(results), cases=results)
    emit("STRICT_TEST_SUMMARY", {k: total[k] for k in ("passed", "total")})
    if total["passed"] != total["total"]:
        raise AssertionError("synthetic tests failed")
    return total


def observe(name: str, d: Graph) -> tuple[dict[str, Any], dict[str, Any]]:
    """Reproduce the historical observed statistics and biological spot controls."""
    obs = base.estadisticas(d, d["post"], detalle=True)
    values = {key: obs[key] for key in BASELINE[name]}
    if values != BASELINE[name]:
        raise AssertionError("historical baseline mismatch: " + repr(values))
    passed, control = base.control(d, obs["j"], obs["cab"], name == "flywire")
    if not passed:
        raise AssertionError("historical control failed")
    shared = obs["j"].groupby("x").dt.nunique()
    shared_ids = shared[shared >= 2].index.to_numpy(dtype=np.int64)
    counts = Counter(None if pd.isna(d["sc"][i]) else str(d["sc"][i]) for i in shared_ids)
    descriptions = dict(shared_X_by_superclass=[dict(superclass=k, count=v) for k, v in sorted(counts.items(), key=lambda x: str(x[0]))],
                        AN_multi_11_superclasses=sorted(set(str(x) for x in d["sc"][d["tipo"] == "AN_multi_11"])))
    del obs
    return values, dict(passed=True, details=control, descriptive=descriptions)


def run_draws(name: str, d: Graph, observed: dict[str, Any], target: dict[str, Any],
              smoke: bool, save: Any) -> None:
    """Run the fixed ensemble, retaining every result and aborting on failed invariants."""
    count = 2 if smoke else N_NULL
    seed = SMOKE_SEEDS[name] if smoke else SEEDS[name]
    rng = np.random.default_rng(seed)
    reference_budget = budgets(d, d["post"])
    target.update(seed=seed, count_expected=count, nulls=[])
    t0 = time.monotonic()
    for k in range(count):
        new = strict_null(d, rng)
        checked = guard(d, new)
        if k in (0, count - 1):
            ok = all(np.array_equal(a, b) for a, b in zip(reference_budget, budgets(d, new)))
            checked["budget_recomputed"] = bool(ok)
            checked["ok"] &= bool(ok)
        if not checked["ok"]:
            emit("FAILED_GUARD", dict(connectome=name, draw=k, guard=checked))
            raise AssertionError("strict null guard failed")
        result = base.estadisticas(d, new)
        row = dict(draw=k, targets_sha256=hashlib.sha256(new.tobytes()).hexdigest(), guard=checked, **result)
        target["nulls"].append(row)
        if smoke:
            emit("SMOKE_GUARD", dict(connectome=name, draw=k, guard=checked))
        else:
            emit("NULL", dict(connectome=name, **row))
        if not smoke and (k + 1) % 20 == 0:
            target["seconds"] = time.monotonic() - t0
            save()
    target["seconds"] = time.monotonic() - t0
    target["fixed_arrays_unchanged"] = all(hashlib.sha256(d[key].tobytes()).hexdigest() == val for key, val in d["fixed_hashes"].items())
    if not target["fixed_arrays_unchanged"] or not complete_plan(target["nulls"], count):
        raise AssertionError("fixed arrays or complete ensemble failed")
    if smoke:
        target["guards"] = [row["guard"] for row in target.pop("nulls")]
        emit("SMOKE", dict(connectome=name, valid=True, blind=True, seconds=target["seconds"]))
        return
    target["nonfrozen"] = nonfrozen(observed, target["nulls"])
    if not target["nonfrozen"]:
        raise AssertionError("INVALIDO_NO_IDENTIFICABLE")
    target["observed"] = observed
    target["p"] = [(1 + sum(row[key] >= observed[key] for row in target["nulls"])) / (count + 1)
                   for key in ("t1", "t2")]
    target["summary"] = {key: dict(mean=float(np.mean([x[key] for x in target["nulls"]])),
                                  min=min(x[key] for x in target["nulls"]),
                                  max=max(x[key] for x in target["nulls"])) for key in ("t1", "t2", "n_cab")}
    emit("CONNECTOME_RESULT", dict(connectome=name, observed=observed, p=target["p"], summary=target["summary"]))


def environment() -> dict[str, Any]:
    """Record actual runtime identity and enforce the tested dependency pins."""
    versions = {"numpy": np.__version__, "pandas": pd.__version__, "pyarrow": pyarrow.__version__}
    if versions != VERSIONS:
        raise ValueError("dependency versions differ from the tested pins: " + repr(versions))
    seal = HERE / "SELLO-ESTRICTO-2026-11-01.md"
    if blob(seal.read_bytes()) != SEAL_BLOB:
        raise ValueError("preregistration bytes changed")
    mem = Path("/proc/meminfo")
    return dict(utc=datetime.now(timezone.utc).isoformat(), machine=platform.node(), platform=platform.platform(),
                python=platform.python_version(), versions=versions, cpus=os.cpu_count(),
                memory=mem.read_text().splitlines()[:5] if mem.exists() else [],
                source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(), base_blob=BASE_BLOB,
                seal_blob=SEAL_BLOB, seal_commit=SEAL_COMMIT,
                github_sha=os.environ.get("GITHUB_SHA"), runner_image=os.environ.get("ImageVersion"),
                github_run_id=os.environ.get("GITHUB_RUN_ID"))


def main() -> int:
    """Run selftests, blinded smoke in both connectomes, then the authorized full test."""
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--mode", choices=["selftest", "smoke", "full"], required=True)
    ap.add_argument("--inputs-dir", type=Path)
    ap.add_argument("--out", type=Path)
    args = ap.parse_args()
    if args.mode != "selftest" and (args.inputs_dir is None or args.out is None):
        ap.error("smoke/full require --inputs-dir and --out")
    t0 = time.monotonic()
    result: dict[str, Any] = dict(status="RUNNING", mode=args.mode, smoke={}, connectomes={})
    exit_code = 3
    try:
        result["environment"] = environment()
        emit("ENVIRONMENT", result["environment"])
        result["selftest"] = selftest()
        if args.mode == "selftest":
            result["status"], exit_code = "VALID_SELFTEST_ONLY", 0
        else:
            result["inputs"] = validate_inputs(args.inputs_dir)
            for name in ("flywire", "banc"):
                d = prepare(load_graph(name, args.inputs_dir))
                obs, ctl = observe(name, d)
                emit("LOAD_SMOKE", dict(connectome=name, neurons=d["n"], rows=len(d["pre"]), strata=d["strata"], baseline_equal=True, control_passed=ctl["passed"]))
                result["smoke"][name] = {}
                run_draws(name, d, obs, result["smoke"][name], True, lambda: None)
                del d
                gc.collect()
            checkpoint(args.out, result)
            if args.mode == "full":
                for name in ("flywire", "banc"):
                    d = prepare(load_graph(name, args.inputs_dir))
                    obs, ctl = observe(name, d)
                    info = dict(neurons=d["n"], rows=len(d["pre"]), strata=d["strata"],
                                class_labels=d["class_labels"], control=ctl)
                    result["connectomes"][name] = info
                    emit("LOAD_FULL", dict(connectome=name, neurons=d["n"], rows=len(d["pre"]), strata=d["strata"], control=ctl))
                    run_draws(name, d, obs, info, False, lambda: checkpoint(args.out, result))
                    del d
                    gc.collect()
                fw, ba = result["connectomes"]["flywire"], result["connectomes"]["banc"]
                ps = fw["p"] + ba["p"]
                adjusted = base.holm(ps).tolist()
                vf = base.veredicto_conectoma(ps[:2], adjusted[:2])
                vb = base.veredicto_conectoma(ps[2:], adjusted[2:])
                result.update(p=ps, holm=adjusted, H_REUSO_ESTRICTO_FLYWIRE=vf, H_REUSO_ESTRICTO_BANC=vb,
                              H_REUSO_ESTRICTO=base.veredicto_final(vf, vb, True))
                emit("SCIENTIFIC_VERDICT", {key: result[key] for key in ("p", "holm", "H_REUSO_ESTRICTO_FLYWIRE", "H_REUSO_ESTRICTO_BANC", "H_REUSO_ESTRICTO")})
                result["status"] = "VALID"
            else:
                result["status"] = "VALID_SMOKE_ONLY"
            exit_code = 0
    except Exception as exc:
        result.update(status="INVALIDO", error=type(exc).__name__ + ": " + str(exc))
        emit("INVALIDO", result["error"])
        traceback.print_exc()
    finally:
        result["seconds"] = time.monotonic() - t0
        result["maxrss_kib"] = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        result["exit_code"] = exit_code
        if args.out is not None:
            checkpoint(args.out, result)
        emit("EXIT", dict(code=exit_code, status=result["status"], seconds=result["seconds"], maxrss_kib=result["maxrss_kib"]))
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
