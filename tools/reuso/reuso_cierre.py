#!/usr/bin/env python3
"""tools/reuso/reuso_cierre.py: closure null with the real direct wiring fixed.

Scientific contract: SELLO-CIERRE-2026-11-01.md, committed in a2bf422 before this
file. reuso_estricto.py and, through it, the historical reuso_mosca.py are
imported only after their Git blobs match.
Run: python tools/reuso/reuso_cierre.py --mode selftest
Full: add --mode full --inputs-dir /tmp/reuso-input --out result.json.
No network, credentials, pickle loading or git writes occur in this module.
"""
from __future__ import annotations

import argparse
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
from typing import Any, Callable

import numpy as np
import pandas as pd
import pyarrow
import scipy
from scipy import sparse

Graph = dict[str, Any]
HERE = Path(__file__).resolve().parent
ESTRICTO_BLOB = "502b2ee90f90606224a43611bd0c6f4f3b35949c"
SEAL_FILE = "SELLO-CIERRE-2026-11-01.md"
SEAL_BLOB = "bd03205cbfc98187d9f2e7aad31dde0b25212c06"
SEAL_COMMIT = "a2bf422253b42bfc4215018c01b22c7f9113d426"
STRICT_JSON = HERE.parent.parent / "results" / "reuso_estricto_2026-11-01" / "estricto.json"
STRICT_JSON_SHA256 = "ffce074c422835b426c717902e0510d6bcdd130ecff45d9fccce25e182a89282"
N_NULL = 200
SEEDS = {"flywire": 22029, "banc": 22030}
SMOKE_SEEDS = {"flywire": 932029, "banc": 932030}
VERSIONS = {"numpy": "2.5.3", "pandas": "3.0.5", "pyarrow": "25.0.1", "scipy": "1.18.1"}
STAT_KEYS = ("n_cab", "n_pares_ffi", "t1", "t2", "n_x")


def blob(data: bytes) -> str:
    """Compute Git blob identity, including the object header."""
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()


def pinned_module(name: str, filename: str, expected: str) -> Any:
    """Reject changed source before importing a local, pinned Python module."""
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


estricto = pinned_module("reuso_estricto", "reuso_estricto.py", ESTRICTO_BLOB)
base = estricto.base
emit = estricto.emit


def sha(array: np.ndarray) -> str:
    """SHA256 of the raw bytes of a target vector."""
    return hashlib.sha256(array.tobytes()).hexdigest()


def prepare_cierre(d: Graph) -> Graph:
    """Add closure strata: S->D rows fixed; the rest by side, class, sign and role."""
    pre, post = d["pre"], d["post"]
    role = np.zeros(d["n"], dtype=np.int8)
    role[d["S"] >= 0] = 1
    role[d["D"] >= 0] = 2
    d["role"] = role
    fixed = (d["S"][pre] >= 0) & (d["D"][post] >= 0)
    movable = np.flatnonzero(~fixed).astype(np.int64)
    sign = d["inh"][post].astype(np.int64)  # closure-sign-key
    code = ((((d["sl"][pre].astype(np.int64) * 3 + d["sl"][post]) * d["n_classes"] + d["sc_code"][post]) * 2 + sign) * 3
            + role[post])
    moving_code = code[movable]
    order = np.argsort(moving_code, kind="stable")
    values, starts = np.unique(moving_code[order], return_index=True)
    d["c_order"], d["c_bounds"] = movable[order], np.r_[starts, len(order)]
    d["c_strata"] = int(len(values))
    d["c_fixed"], d["c_fixed_rows"] = fixed, np.flatnonzero(fixed)
    xs = d["inh"] & ~d["excl"]
    d["xs"] = xs
    d["c_mix_masks"] = {"movable": ~fixed, "SX": (d["S"][pre] >= 0) & xs[post], "XD": xs[pre] & (d["D"][post] >= 0)}
    return d


def cierre_null(d: Graph, rng: np.random.Generator) -> np.ndarray:
    """Uniformly permute original target stubs of movable rows within each stratum."""
    old, order, bounds = d["post"], d["c_order"], d["c_bounds"]
    new = old.copy()
    for lo, hi in zip(bounds[:-1], bounds[1:]):
        rows = order[lo:hi]
        if len(rows) > 1:
            new[rows] = old[rows][rng.permutation(len(rows))]
    return new


def guard_cierre(d: Graph, new: np.ndarray) -> dict[str, Any]:
    """Check fixed S->D rows, per-row target attributes, histograms and mixing."""
    index_ok = bool(new.shape == d["post"].shape and np.issubdtype(new.dtype, np.integer)
                    and len(new) > 0 and new.min() >= 0 and new.max() < d["n"])
    if not index_ok:
        return dict(ok=False, index=False)
    old = d["post"]
    moved = new != old
    fractions = {key: float(moved[mask].mean()) if mask.any() else 0.0 for key, mask in d["c_mix_masks"].items()}
    rows = d["c_fixed_rows"]
    checks = dict(
        index=True,
        sd_fixed=bool(np.array_equal(new[rows], old[rows])),
        target_class=bool(np.array_equal(d["sc_code"][new], d["sc_code"][old])),
        target_side=bool(np.array_equal(d["sl"][new], d["sl"][old])),
        target_sign=bool(np.array_equal(d["inh"][new], d["inh"][old])),
        target_role=bool(np.array_equal(d["role"][new], d["role"][old])),
        incoming_by_pre_side=all(np.array_equal(np.bincount(new[g], minlength=d["n"]), ref)
                                 for g, ref in zip(d["pre_groups"], d["incoming_by_pre_side"])),
        mixing=all(value > 0.5 for value in fractions.values()),
    )
    return dict(ok=all(checks.values()), checks=checks, moved=fractions)


def budgets_cierre(d: Graph, post: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Recalculate outgoing rows and weights by target class, side, sign and role."""
    key = ((((d["pre"].astype(np.int64) * d["n_classes"] + d["sc_code"][post]) * 3 + d["sl"][post]) * 2
            + d["inh"][post]) * 3 + d["role"][post])
    keys, inverse = np.unique(key, return_inverse=True)
    return keys, np.bincount(inverse), np.bincount(inverse, weights=d["w"])


def same_budget(a: tuple[np.ndarray, ...], b: tuple[np.ndarray, ...]) -> bool:
    """Exact equality of two budget triples."""
    return all(np.array_equal(x, y) for x, y in zip(a, b))


def sparse_stats(d: Graph, post: np.ndarray, w_dir: int = 20, w_x: int = 5) -> dict[str, Any]:
    """Independent T1/T2 with scipy.sparse products, without pandas merge or groupby."""
    pre, w, S, D, n = d["pre"], d["w"].astype(np.int64), d["S"], d["D"], d["n"]
    n_s, n_d = len(d["cs"]), len(d["cd"])
    s_of, d_of = S[pre], D[post]
    m = (s_of >= 0) & (d_of >= 0)
    direct = sparse.coo_matrix((w[m], (s_of[m], d_of[m])), shape=(n_s, n_d)).toarray()
    cab = (direct >= w_dir) & d["mismo"]
    xs = d["inh"] & ~d["excl"]
    m1 = (s_of >= 0) & xs[post]
    p_sx = sparse.coo_matrix((w[m1], (s_of[m1], post[m1])), shape=(n_s, n)).tocsr()
    p_sx.sum_duplicates()
    p5 = (p_sx >= w_x).astype(np.int64)
    m2 = xs[pre] & (d_of >= 0)
    q_xd = sparse.coo_matrix((w[m2], (pre[m2], d_of[m2])), shape=(n, n_d)).tocsr()
    q_xd.sum_duplicates()
    q5 = (q_xd >= w_x).astype(np.int64)
    paths = (p5 @ q5).toarray() > 0
    n_cab, n_pairs = int(cab.sum()), int((paths & cab).sum())
    reach = p5.T @ sparse.csr_matrix(cab.astype(np.int64))
    closing = (reach > 0).astype(np.int64).multiply(q5).tocsr()
    n_types = int(d["d_tipo"].max()) + 1 if n_d else 0
    one_hot = sparse.coo_matrix((np.ones(n_d, dtype=np.int64), (np.arange(n_d), d["d_tipo"])), shape=(n_d, n_types)).tocsr()
    per_x = np.asarray(((closing @ one_hot) > 0).sum(axis=1)).ravel()
    return dict(n_cab=n_cab, t1=float(n_pairs / n_cab) if n_cab else 0.0, t2=int((per_x >= 2).sum()),
                n_pares_ffi=n_pairs, n_x=int((per_x >= 1).sum()))


def first_order(d: Graph, post: np.ndarray) -> dict[str, Any]:
    """Rows and weight from eligible S to candidate X, overall and by target class."""
    pre, w = d["pre"], d["w"].astype(np.int64)
    s_rows, to_x, cls = d["S"][pre] >= 0, d["xs"][post], d["sc_code"][post]
    out = dict(S_rows=int(s_rows.sum()), S_weight=int(w[s_rows].sum()),
               S_to_X_rows=int((s_rows & to_x).sum()), S_to_X_weight=int(w[s_rows & to_x].sum()),
               all_rows=int(len(pre)), all_weight=int(w.sum()),
               all_to_X_rows=int(to_x.sum()), all_to_X_weight=int(w[to_x].sum()), by_class=[])
    for code in np.unique(cls[to_x]).tolist():
        in_class = cls == code
        out["by_class"].append(dict(
            superclass=d["class_labels"][code], S_to_class_rows=int((s_rows & in_class).sum()),
            S_to_X_rows=int((s_rows & in_class & to_x).sum()), all_to_class_rows=int(in_class.sum()),
            all_to_X_rows=int((in_class & to_x).sum())))
    return out


def fixture_first_order(seed: int) -> Graph:
    """Random wiring whose only structure is that S prefer inhibitory targets."""
    rng = np.random.default_rng(seed)
    types: list[Any] = []
    sides: list[str] = []
    classes: list[Any] = []
    inhibitory: list[bool] = []
    edges: list[tuple[int, int, int]] = []
    def neuron(t: Any, side: str, sc: Any, inh: bool = False) -> int:
        types.append(t); sides.append(side); classes.append(sc); inhibitory.append(inh)
        return len(types) - 1
    groups = {}
    for side in ("left", "right"):
        g = dict(S=[neuron("S%s%d" % (side[0], i), side, "visual_projection") for i in range(12)],
                 D=[neuron("D%s%d" % (side[0], i), side, "descending") for i in range(24)],
                 X=[neuron("X%s%d" % (side[0], i), side, "central", True) for i in range(24)],
                 E=[neuron("E%s%d" % (side[0], i), side, "central") for i in range(96)])
        groups[side] = g
        for s in g["S"]:
            edges += [(s, int(z), 25) for z in rng.choice(g["D"], 2, replace=False)]
            edges += [(s, int(x), 8) for x in rng.choice(g["X"], 3, replace=False)]
        for x in g["X"]:
            edges += [(x, int(z), 8) for z in rng.choice(g["D"], 4, replace=False)]
        for q in g["E"]:
            edges += [(q, int(z), 3) for z in rng.choice(g["E"], 4, replace=False)]
    u = neuron("U", "left", None)
    edges.append((groups["left"]["E"][0], u, 2))
    e = np.asarray(edges, dtype=np.int64)
    return estricto.prepare(estricto.attach(e[:, 0], e[:, 1], e[:, 2], np.asarray(inhibitory),
                                            np.asarray(types, dtype=object), np.asarray(sides, dtype=object),
                                            np.asarray(classes, dtype=object), np.arange(len(types)) + 5000))


def fixture_roles() -> Graph:
    """Tiny graph where two descending targets differ only in eligibility (role)."""
    types = np.asarray(["S0", "D0", None, "X0", "E0"], dtype=object)
    sides = np.asarray(["left"] * 5, dtype=object)
    classes = np.asarray(["visual_projection", "descending", "descending", "central", "central"], dtype=object)
    inhibitory = np.asarray([False, False, False, True, False])
    e = np.asarray([(0, 1, 30), (0, 3, 8), (3, 1, 8), (3, 2, 8), (4, 1, 3), (4, 2, 3), (4, 3, 3)], dtype=np.int64)
    return prepare_cierre(estricto.prepare(estricto.attach(e[:, 0], e[:, 1], e[:, 2], inhibitory, types, sides,
                                                           classes, np.arange(5) + 9000)))


def pvalues(d: Graph, observed: dict[str, Any], maker: Callable[[Graph, np.random.Generator], np.ndarray],
            count: int, seed: int) -> list[float]:
    """Rank p values for T1 and T2 under one null maker and one seed."""
    rng = np.random.default_rng(seed)
    draws = [base.estadisticas(d, maker(d, rng)) for _ in range(count)]
    return [(1 + sum(x[k] >= observed[k] for x in draws)) / (count + 1) for k in ("t1", "t2")]


def selftest() -> dict[str, Any]:
    """Run the strict suite, then closure fixtures, calibration and sabotage checks."""
    results: list[dict[str, Any]] = []
    def check(name: str, ok: bool, details: Any = None) -> None:
        results.append(dict(name=name, ok=bool(ok), details=details))
        emit("TEST", results[-1])
    strict = estricto.selftest()
    check("strict_selftest_25", strict["passed"] == strict["total"] == 25)
    check("estricto_pin_rejects_changed_bytes", blob((HERE / "reuso_estricto.py").read_bytes() + b" ") != ESTRICTO_BLOB)
    d = prepare_cierre(estricto.fixture(True))
    obs = base.estadisticas(d, d["post"])
    check("sparse_parity_planted_observed", sparse_stats(d, d["post"]) == obs, obs)
    rng = np.random.default_rng(441)
    reference = budgets_cierre(d, d["post"])
    draws: list[dict[str, Any]] = []
    nulls: list[np.ndarray] = []
    guards_ok = parity_ok = budget_ok = denominator_ok = True
    for k in range(39):
        new = cierre_null(d, rng)
        value, guarded = base.estadisticas(d, new), guard_cierre(d, new)
        guards_ok &= guarded["ok"]
        parity_ok &= sparse_stats(d, new) == value
        budget_ok &= same_budget(reference, budgets_cierre(d, new))
        denominator_ok &= value["n_cab"] == obs["n_cab"]
        draws.append(dict(draw=k, targets_sha256=sha(new), guard=guarded, **value))
        nulls.append(new)
    check("closure_guards_39", guards_ok)
    check("sparse_parity_39_closure", parity_ok)
    check("closure_budgets_39", budget_ok)
    check("denominator_fixed_39", denominator_ok)
    check("planted_enrichment_closure", all(obs[k] > max(x[k] for x in draws) for k in ("t1", "t2")),
          {k: dict(observed=obs[k], null_max=max(x[k] for x in draws)) for k in ("t1", "t2")})
    negative = prepare_cierre(estricto.fixture(False))
    nobs = base.estadisticas(negative, negative["post"])
    ndraws = [base.estadisticas(negative, cierre_null(negative, np.random.default_rng(500 + k))) for k in range(39)]
    check("absent_motif_can_refute_closure", nobs["t1"] == 0.0 and nobs["t2"] == 0 and
          all((1 + sum(x[k] >= nobs[k] for x in ndraws)) / 40 == 1.0 for k in ("t1", "t2")), nobs)
    calibration = []
    for s in range(10):
        f = prepare_cierre(fixture_first_order(1000 + s))
        fobs = base.estadisticas(f, f["post"])
        calibration.append(dict(seed=1000 + s, observed=fobs,
                                p_strict=pvalues(f, fobs, estricto.strict_null, 19, 11 + s),
                                p_cierre=pvalues(f, fobs, cierre_null, 19, 31 + s),
                                parity=sparse_stats(f, f["post"]) == fobs))
    floor = 1 / 20
    check("sparse_parity_first_order_10", all(c["parity"] for c in calibration))
    check("strict_fooled_by_first_order", sum(c["p_strict"][0] == floor for c in calibration) >= 9,
          [c["p_strict"] for c in calibration])
    check("closure_not_fooled_by_first_order", sum(c["p_cierre"][0] == floor for c in calibration) <= 1
          and sum(c["p_cierre"][1] == floor for c in calibration) <= 1, [c["p_cierre"] for c in calibration])
    mutated = nulls[0].copy()
    r = int(d["c_fixed_rows"][0])
    options = np.flatnonzero((d["role"] == 2) & (d["sl"] == d["sl"][mutated[r]]) & (d["inh"] == d["inh"][mutated[r]])
                             & (np.arange(d["n"]) != mutated[r]))
    mutated[r] = options[0]
    check("sd_row_move_rejected", not guard_cierre(d, mutated)["checks"]["sd_fixed"])
    mutated = nulls[0].copy()
    xrows = np.flatnonzero(d["xs"][mutated] & (d["sl"][mutated] == 0))
    crows = np.flatnonzero(~d["inh"][mutated] & (d["sc_code"][mutated] == d["sc_code"][mutated[xrows[0]]])
                           & (d["sl"][mutated] == 0) & (d["role"][mutated] == 0))
    a, b = int(xrows[0]), int(crows[0])
    mutated[a], mutated[b] = mutated[b], mutated[a]
    check("sign_swap_rejected", not guard_cierre(d, mutated)["checks"]["target_sign"])
    roles = fixture_roles()
    swapped = roles["post"].copy()
    swapped[2], swapped[3] = swapped[3], swapped[2]
    check("role_swap_rejected", not guard_cierre(roles, swapped)["checks"]["target_role"])
    check("strict_draw_rejected_by_closure_guard", not guard_cierre(d, estricto.strict_null(d, np.random.default_rng(7)))["ok"])
    identity = guard_cierre(d, d["post"].copy())
    check("identity_shuffle_rejected", not identity["ok"] and not identity["checks"]["mixing"])
    mutated = nulls[0].copy()
    a = int(xrows[0])
    options = np.flatnonzero(d["xs"] & (d["sl"] == d["sl"][mutated[a]]) & (d["sc_code"] == d["sc_code"][mutated[a]])
                             & (np.arange(d["n"]) != mutated[a]))
    mutated[a] = options[0]
    check("incoming_histogram_mutation_rejected", not guard_cierre(d, mutated)["checks"]["incoming_by_pre_side"])
    mutated = nulls[0].copy()
    mutated[0] = -1
    check("invalid_index_rejected", not guard_cierre(d, mutated)["ok"])
    check("wrong_shape_rejected", not guard_cierre(d, nulls[0][:-1])["ok"])
    check("seed_reproducibility_closure", np.array_equal(cierre_null(d, np.random.default_rng(111)),
                                                         cierre_null(d, np.random.default_rng(111))))
    check("seed_changes_draw_closure", not np.array_equal(cierre_null(d, np.random.default_rng(111)),
                                                          cierre_null(d, np.random.default_rng(112))))
    check("sparse_parity_detects_threshold_change", sparse_stats(d, d["post"], w_x=9) != obs)
    check("complete_plan_39", estricto.complete_plan(draws, 39))
    check("missing_draw_rejected", not estricto.complete_plan(draws[:-1], 39))
    check("statistic_not_fixed", estricto.nonfrozen(obs, draws))
    check("frozen_ensemble_rejected", not estricto.nonfrozen(obs, [obs.copy() for _ in range(200)]))
    fixed = {key: hashlib.sha256(d[key].tobytes()).hexdigest() for key in d["fixed_hashes"]}
    check("source_weights_sign_unchanged", fixed == d["fixed_hashes"])
    total = dict(passed=sum(x["ok"] for x in results), total=len(results), cases=results)
    emit("CIERRE_TEST_SUMMARY", {k: total[k] for k in ("passed", "total")})
    if total["passed"] != total["total"]:
        raise AssertionError("synthetic tests failed")
    return total


def observe_cierre(name: str, d: Graph) -> tuple[dict[str, Any], dict[str, Any]]:
    """Reproduce the historical observation and demand sparse parity on it."""
    values, control = estricto.observe(name, d)
    independent = sparse_stats(d, d["post"])
    if independent != values:
        raise AssertionError("sparse parity failed on the observed graph: " + repr(independent))
    return values, control


def run_cierre(name: str, d: Graph, observed: dict[str, Any], target: dict[str, Any], smoke: bool,
               save: Callable[[], None]) -> None:
    """Run the sealed closure ensemble, retaining every row and aborting on any failed gate."""
    count = 2 if smoke else N_NULL
    seed = SMOKE_SEEDS[name] if smoke else SEEDS[name]
    rng = np.random.default_rng(seed)
    reference = budgets_cierre(d, d["post"])
    target.update(seed=seed, count_expected=count, nulls=[])
    t0 = time.monotonic()
    for k in range(count):
        new = cierre_null(d, rng)
        checked = guard_cierre(d, new)
        if k in (0, count - 1):
            ok = same_budget(reference, budgets_cierre(d, new))
            checked["budget_recomputed"] = bool(ok)
            checked["ok"] = bool(checked["ok"] and ok)
        if not checked["ok"]:
            emit("FAILED_GUARD", dict(connectome=name, draw=k, guard=checked))
            raise AssertionError("closure null guard failed")
        result = base.estadisticas(d, new)
        if result["n_cab"] != observed["n_cab"]:
            raise AssertionError("closure denominator changed")
        if not smoke and k in (0, count - 1):
            independent = sparse_stats(d, new)
            checked["sparse_parity"] = independent == result
            if not checked["sparse_parity"]:
                emit("FAILED_PARITY", dict(connectome=name, draw=k, historical=result, sparse=independent))
                raise AssertionError("sparse parity failed")
            target.setdefault("first_order", {})["cierre_" + str(k)] = first_order(d, new)
        row = dict(draw=k, targets_sha256=sha(new), guard=checked, **result)
        target["nulls"].append(row)
        if smoke:
            emit("SMOKE_GUARD", dict(connectome=name, draw=k, guard=checked))
        else:
            emit("NULL", dict(connectome=name, **row))
        if not smoke and (k + 1) % 20 == 0:
            target["seconds"] = time.monotonic() - t0
            save()
    target["seconds"] = time.monotonic() - t0
    target["fixed_arrays_unchanged"] = all(hashlib.sha256(d[key].tobytes()).hexdigest() == val
                                           for key, val in d["fixed_hashes"].items())
    if not target["fixed_arrays_unchanged"] or not estricto.complete_plan(target["nulls"], count):
        raise AssertionError("fixed arrays or complete ensemble failed")
    if smoke:
        target["guards"] = [row["guard"] for row in target.pop("nulls")]
        emit("SMOKE", dict(connectome=name, valid=True, seconds=target["seconds"]))
        return
    target["nonfrozen"] = estricto.nonfrozen(observed, target["nulls"])
    if not target["nonfrozen"]:
        raise AssertionError("INVALIDO_NO_IDENTIFICABLE")
    target["observed"] = observed
    target["p"] = [(1 + sum(row[key] >= observed[key] for row in target["nulls"])) / (count + 1) for key in ("t1", "t2")]
    target["summary"] = {key: dict(mean=float(np.mean([x[key] for x in target["nulls"]])),
                                  min=min(x[key] for x in target["nulls"]),
                                  max=max(x[key] for x in target["nulls"])) for key in STAT_KEYS}
    emit("CONNECTOME_RESULT", dict(connectome=name, observed=observed, p=target["p"], summary=target["summary"]))


def repro_estricto(name: str, d: Graph, strict: dict[str, Any]) -> dict[str, Any]:
    """Regenerate the published strict ensemble from its seed and compare every hash."""
    ref = strict["connectomes"][name]["nulls"]
    rng = np.random.default_rng(estricto.SEEDS[name])
    equal, mismatched, stats, orders = 0, [], {}, {}
    t0 = time.monotonic()
    for k in range(len(ref)):
        new = estricto.strict_null(d, rng)
        if sha(new) == ref[k]["targets_sha256"]:
            equal += 1
        else:
            mismatched.append(k)
        if k in (0, len(ref) - 1):
            published = {key: ref[k][key] for key in STAT_KEYS}
            historical, independent = base.estadisticas(d, new), sparse_stats(d, new)
            stats[str(k)] = dict(published=published, historical=historical, sparse=independent,
                                 equal=historical == published and independent == published)
            orders["estricto_" + str(k)] = first_order(d, new)
    ok = equal == len(ref) == N_NULL and all(v["equal"] for v in stats.values())
    out = dict(status="PASS" if ok else "FAIL", seed=estricto.SEEDS[name], hashes_equal=equal, hashes_total=len(ref),
               mismatched=mismatched[:20], stats=stats, first_order=orders, seconds=time.monotonic() - t0)
    emit("REPRO_ESTRICTO", dict(connectome=name, status=out["status"], hashes_equal=equal, hashes_total=len(ref),
                                mismatched=out["mismatched"], stats=stats, seconds=out["seconds"]))
    return out


def load_strict() -> dict[str, Any]:
    """Read the published strict receipt only if its bytes match the sealed pin."""
    data = STRICT_JSON.read_bytes()
    if hashlib.sha256(data).hexdigest() != STRICT_JSON_SHA256:
        raise ValueError("strict receipt pin mismatch")
    strict = json.loads(data)
    if strict.get("status") != "VALID":
        raise ValueError("strict receipt is not VALID")
    return strict


def environment() -> dict[str, Any]:
    """Record runtime identity and enforce the tested dependency and seal pins."""
    versions = {"numpy": np.__version__, "pandas": pd.__version__, "pyarrow": pyarrow.__version__, "scipy": scipy.__version__}
    if versions != VERSIONS:
        raise ValueError("dependency versions differ from the tested pins: " + repr(versions))
    if blob((HERE / SEAL_FILE).read_bytes()) != SEAL_BLOB:
        raise ValueError("preregistration bytes changed")
    mem = Path("/proc/meminfo")
    return dict(utc=datetime.now(timezone.utc).isoformat(), machine=platform.node(), platform=platform.platform(),
                python=platform.python_version(), versions=versions, cpus=os.cpu_count(),
                memory=mem.read_text().splitlines()[:5] if mem.exists() else [],
                source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(), estricto_blob=ESTRICTO_BLOB,
                base_blob=estricto.BASE_BLOB, seal_blob=SEAL_BLOB, seal_commit=SEAL_COMMIT,
                strict_json_sha256=STRICT_JSON_SHA256, github_sha=os.environ.get("GITHUB_SHA"),
                runner_image=os.environ.get("ImageVersion"), github_run_id=os.environ.get("GITHUB_RUN_ID"))


def main() -> int:
    """Run selftests, smoke in both connectomes, then the sealed closure test and REPRO."""
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--mode", choices=["selftest", "smoke", "full"], required=True)
    ap.add_argument("--inputs-dir", type=Path)
    ap.add_argument("--out", type=Path)
    args = ap.parse_args()
    if args.mode != "selftest" and (args.inputs_dir is None or args.out is None):
        ap.error("smoke/full require --inputs-dir and --out")
    t0 = time.monotonic()
    result: dict[str, Any] = dict(status="RUNNING", mode=args.mode, smoke={}, connectomes={}, repro_estricto={})
    exit_code = 3
    try:
        result["environment"] = environment()
        emit("ENVIRONMENT", result["environment"])
        result["selftest"] = selftest()
        if args.mode == "selftest":
            result["status"], exit_code = "VALID_SELFTEST_ONLY", 0
        else:
            strict = load_strict()
            result["inputs"] = estricto.validate_inputs(args.inputs_dir)
            for name in ("flywire", "banc"):
                d = prepare_cierre(estricto.prepare(estricto.load_graph(name, args.inputs_dir)))
                obs, ctl = observe_cierre(name, d)
                emit("LOAD_SMOKE", dict(connectome=name, neurons=d["n"], rows=len(d["pre"]), strata=d["c_strata"],
                                        fixed_rows=int(d["c_fixed"].sum()), baseline_equal=True, sparse_parity=True,
                                        control_passed=ctl["passed"]))
                result["smoke"][name] = {}
                run_cierre(name, d, obs, result["smoke"][name], True, lambda: None)
                del d
                gc.collect()
            estricto.checkpoint(args.out, result)
            if args.mode == "full":
                for name in ("flywire", "banc"):
                    d = prepare_cierre(estricto.prepare(estricto.load_graph(name, args.inputs_dir)))
                    obs, ctl = observe_cierre(name, d)
                    info = dict(neurons=d["n"], rows=len(d["pre"]), strata=d["c_strata"], fixed_rows=int(d["c_fixed"].sum()),
                                class_labels=d["class_labels"], control=ctl, first_order=dict(real=first_order(d, d["post"])))
                    result["connectomes"][name] = info
                    emit("LOAD_FULL", dict(connectome=name, neurons=d["n"], rows=len(d["pre"]), strata=d["c_strata"],
                                           fixed_rows=info["fixed_rows"], first_order_real=info["first_order"]["real"]))
                    run_cierre(name, d, obs, info, False, lambda: estricto.checkpoint(args.out, result))
                    result["repro_estricto"][name] = repro_estricto(name, d, strict)
                    estricto.checkpoint(args.out, result)
                    del d
                    gc.collect()
                fw, ba = result["connectomes"]["flywire"], result["connectomes"]["banc"]
                ps = fw["p"] + ba["p"]
                adjusted = base.holm(ps).tolist()
                vf = base.veredicto_conectoma(ps[:2], adjusted[:2])
                vb = base.veredicto_conectoma(ps[2:], adjusted[2:])
                repro = "PASS" if all(result["repro_estricto"][n]["status"] == "PASS" for n in ("flywire", "banc")) else "FAIL"
                result.update(p=ps, holm=adjusted, H_REUSO_CIERRE_FLYWIRE=vf, H_REUSO_CIERRE_BANC=vb,
                              H_REUSO_CIERRE=base.veredicto_final(vf, vb, True), REPRO_ESTRICTO=repro)
                emit("SCIENTIFIC_VERDICT", {key: result[key] for key in ("p", "holm", "H_REUSO_CIERRE_FLYWIRE", "H_REUSO_CIERRE_BANC",
                                                                         "H_REUSO_CIERRE", "REPRO_ESTRICTO")})
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
            estricto.checkpoint(args.out, result)
        emit("EXIT", dict(code=exit_code, status=result["status"], seconds=result["seconds"], maxrss_kib=result["maxrss_kib"]))
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
