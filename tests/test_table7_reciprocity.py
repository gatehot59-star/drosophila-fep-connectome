#!/usr/bin/env python3
"""Tests de la reconstruccion de la Tabla 7. Cada test puede fallar: compara contra fuerza bruta o contra un caso armado a mano."""
import json
import os
import sys
import tempfile

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "tools"))
import table7_reciprocity_by_class as t7  # noqa: E402


def brute(pre, post, cls, k):
    s = set(zip(pre.tolist(), post.tolist()))
    e = np.zeros((k, k), dtype=np.int64)
    r = np.zeros((k, k), dtype=np.int64)
    for i, j in zip(pre.tolist(), post.tolist()):
        e[cls[i], cls[j]] += 1
        if i != j and (j, i) in s:
            r[cls[i], cls[j]] += 1
    return e, r


def test_reciprocity_matches_brute_force():
    rng = np.random.default_rng(7)
    n, k = 60, 5
    pairs = set()
    while len(pairs) < 500:
        pairs.add((int(rng.integers(n)), int(rng.integers(n))))
    pairs |= {(3, 3), (10, 10)}
    pre = np.array([p[0] for p in pairs], dtype=np.int32)
    post = np.array([p[1] for p in pairs], dtype=np.int32)
    cls = rng.integers(0, k, n).astype(np.int16)
    has, n_unique, n_self = t7.reciprocal_mask(pre, post, n)
    e, r = t7.pair_tables(cls, pre, post, has, k)
    eb, rb = brute(pre, post, cls, k)
    assert n_unique == len(pairs)
    assert n_self == sum(1 for a, b in pairs if a == b)
    assert np.array_equal(e, eb) and np.array_equal(r, rb)
    assert int(r.sum()) % 2 == 0


def test_mapping_detects_non_rank_index():
    pre = np.array([0, 1, 2], dtype=np.int32)
    post = np.array([1, 2, 0], dtype=np.int32)
    preid = np.array([300, 100, 200], dtype=np.int64)
    postid = np.array([100, 200, 300], dtype=np.int64)
    uid, uix, info = t7.build_mapping(pre, post, preid, postid)
    assert uid.tolist() == [100, 200, 300] and uix.tolist() == [1, 2, 0]
    assert info["indice_eon_igual_rank_ordenado"] is False
    assert info["ids_con_varios_indices"] == 0 and info["indices_con_varios_ids"] == 0
    preid2 = np.array([100, 200, 300], dtype=np.int64)
    postid2 = np.array([200, 300, 100], dtype=np.int64)
    _, _, info2 = t7.build_mapping(pre, post, preid2, postid2)
    assert info2["indice_eon_igual_rank_ordenado"] is True


def test_comparator_can_go_red():
    names = sorted({x for a, b, *_ in t7.REF_INTER for x in (a, b)} | {a for a, *_ in t7.REF_INTRA}) + [t7.UNMAPPED]
    k = len(names)
    ix = {c: i for i, c in enumerate(names)}
    e = np.zeros((k, k), dtype=np.int64)
    r = np.zeros((k, k), dtype=np.int64)
    for a, b, re_, rr, _ in t7.REF_INTER:
        e[ix[a], ix[b]], r[ix[a], ix[b]] = re_, rr
    for a, re_, rp in t7.REF_INTRA:
        e[ix[a], ix[a]] = re_
        r[ix[a], ix[a]] = int(round(float(rp) / 100.0 * re_))
    rows, t7rows = t7.compare(names, e, r, t7.REF_GLOBAL[0], t7.REF_GLOBAL[1])
    assert all(x["exacta"] for x in rows), [x for x in rows if not x["exacta"]]
    assert all(x["coincide"] for x in t7rows), [x for x in t7rows if not x["coincide"]]
    dobles = [x["fila"] for x in t7rows if x["solo_por_doble_redondeo"]]
    assert dobles == ["sensory->descending"], dobles
    r[ix["sensory"], ix["motor"]] += 1
    rows2, _ = t7.compare(names, e, r, t7.REF_GLOBAL[0], t7.REF_GLOBAL[1] - 2)
    bad = [x["fila"] for x in rows2 if not x["exacta"]]
    assert bad == ["global", "sensory->motor"], bad


def test_end_to_end_tiny_files():
    rng = np.random.default_rng(11)
    n = 40
    ids = rng.permutation(np.arange(10**15, 10**15 + n)).astype(np.int64)
    pairs = sorted({(int(rng.integers(n)), int(rng.integers(n))) for _ in range(300)})
    pre = np.array([p[0] for p in pairs], dtype=np.int64)
    post = np.array([p[1] for p in pairs], dtype=np.int64)
    df = pd.DataFrame({"Presynaptic_ID": ids[pre], "Postsynaptic_ID": ids[post], "Presynaptic_Index": pre,
                       "Postsynaptic_Index": post, "Connectivity": rng.integers(1, 12, len(pairs)),
                       "Excitatory": np.ones(len(pairs), dtype=np.int64), "Excitatory x Connectivity": np.ones(len(pairs), dtype=np.int64)})
    classes = np.array(["optic", "sensory", "central", "motor", "descending", "endocrine"])[rng.integers(0, 6, n)]
    ann = pd.DataFrame({"root_id": ids, "super_class": classes, "flow": "intrinsic"}).iloc[:-2]
    with tempfile.TemporaryDirectory() as d:
        pq_path, tsv_path = os.path.join(d, "c.parquet"), os.path.join(d, "a.tsv")
        df.to_parquet(pq_path)
        ann.to_csv(tsv_path, sep="\t", index=False)
        res = t7.run(pq_path, tsv_path, os.path.join(d, "out"), 1)
        saved = json.load(open(os.path.join(d, "out", "table7_reciprocity_by_class.json")))
    assert res["veredicto"]["L3_exacta"] is False
    assert saved["anotacion"]["neuronas_sin_anotacion"] == 2
    assert saved["grafo"]["aristas"] == len(pairs)
    e, r = brute(pre, post, np.zeros(n, dtype=np.int64), 1)
    assert saved["grafo"]["aristas_con_reciproca"] == int(r.sum())


if __name__ == "__main__":
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    for fn in tests:
        fn()
        print("PASS", fn.__name__, flush=True)
    print("TESTS_OK", len(tests))
