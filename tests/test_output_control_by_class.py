#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Tests de tools/output_control_by_class.py. Cada uno puede dar rojo."""
import json
import os
import subprocess
import sys
import tempfile

import numpy as np
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq

AQUI = os.path.dirname(os.path.abspath(__file__))
HERR = os.path.join(AQUI, "..", "tools")
sys.path.insert(0, HERR)
import output_control_by_class as oc  # noqa: E402


def grafo_azar(seed, N=40, E=320, K=4):
    rng = np.random.default_rng(seed)
    pre = rng.integers(0, N, E)
    post = rng.integers(0, N, E)
    key = np.unique(pre * N + post)
    pre = (key // N).astype(np.int32)
    post = (key % N).astype(np.int32)
    S = rng.integers(1, 12, len(pre)).astype(np.int32)
    exc = rng.choice(np.array([-1, 1], dtype=np.int8), len(pre))
    cls = rng.integers(0, K, N).astype(np.int8)
    return pre, post, S, exc, cls, N, K


def fuerza_bruta(pre, post, S, exc, cls, N, K, umbral, idx):
    W = np.zeros((N, N))
    E = np.zeros((N, N))
    B = np.zeros((N, N))
    for i, j, s, e in zip(pre, post, S, exc):
        if s >= umbral:
            W[i, j] += s
            B[i, j] += 1
            if e > 0:
                E[i, j] += s
    inn = W.sum(axis=0)
    A = np.zeros_like(W)
    for j in range(N):
        if inn[j] > 0:
            A[:, j] = W[:, j] / inn[j]
    A2 = A @ A
    idx_in = [j for j in idx if inn[j] > 0]
    out = {k: np.zeros(K) for k in ("d1", "d2", "cov", "fila", "exc")}
    for C in range(K):
        src = [i for i in range(N) if cls[i] == C]
        out["d1"][C] = np.mean([A[src, j].sum() for j in idx_in]) if idx_in else np.nan
        out["d2"][C] = np.mean([A2[src, j].sum() for j in idx_in]) if idx_in else np.nan
        out["cov"][C] = np.mean([B[src, j].sum() > 0 for j in idx])
        syn = W[np.ix_(src, list(idx))].sum()
        tot = W[src, :].sum()
        out["fila"][C] = syn / tot if tot > 0 else np.nan
        out["exc"][C] = E[np.ix_(src, list(idx))].sum() / syn if syn > 0 else np.nan
    dom = np.zeros(K, dtype=int)
    emp = 0
    for j in idx_in:
        v = np.array([W[[i for i in range(N) if cls[i] == C], j].sum() for C in range(K)])
        if (v == v.max()).sum() == 1:
            dom[v.argmax()] += 1
        else:
            emp += 1
    out["dom"] = dom
    out["emp"] = emp
    return out


def test_vectorizado_igual_fuerza_bruta():
    for seed in (1, 2, 3):
        pre, post, S, exc, cls, N, K = grafo_azar(seed)
        idx = np.array(sorted(np.random.default_rng(seed + 10).choice(N, 9, replace=False)))
        for umbral in (1, 5):
            V = oc.por_variante(pre, post, S, exc, cls, N, K, umbral)
            r = oc.medir(V, K, {"O": idx})["O"]
            b = fuerza_bruta(pre, post, S, exc, cls, N, K, umbral, idx)
            for k in ("d1", "d2", "cov", "fila", "exc"):
                assert np.allclose(r[k], b[k], equal_nan=True, atol=1e-12), (seed, umbral, k, r[k], b[k])
            assert np.array_equal(r["domina"], b["dom"]), (seed, umbral, r["domina"], b["dom"])
            assert r["empates"] == b["emp"], (seed, umbral)
            con = V["con"]
            assert np.abs(V["F"][con].sum(axis=1) - 1).max() < 1e-12
    return "vectorizado == fuerza bruta (3 grafos x 2 umbrales, D1 D2 cobertura fila exc domina empates)"


def test_matriz_aristas_contra_conteo_directo():
    pre, post, S, exc, cls, N, K = grafo_azar(7)
    for umbral in (1, 5):
        V = oc.por_variante(pre, post, S, exc, cls, N, K, umbral)
        M = oc.matriz_aristas(V, cls, K)
        D = np.zeros((K, K), dtype=np.int64)
        for i, j, s in zip(pre, post, S):
            if s >= umbral:
                D[cls[i], cls[j]] += 1
        assert np.array_equal(M, D), (umbral, M, D)
        D[0, 0] += 1
        assert not np.array_equal(M, D)
    return "matriz clase x clase == conteo directo, y una arista de mas la pone en rojo"


def test_banderas_plantado_y_plano():
    pob = np.arange(200)
    plano = np.tile(np.array([0.25, 0.5, 0.25]), (200, 1))
    idx = np.arange(10)
    (nul,) = oc.nulo_media([plano], pob, len(idx), 2000, [1, 2])
    _, enr, ps, pb, fl = oc.banderas(plano[idx].mean(axis=0), nul)
    assert list(fl) == ["azar", "azar", "azar"], fl
    assert np.allclose(enr, 1.0)
    plant = np.tile(np.array([0.1, 0.45, 0.45]), (200, 1))
    plant[idx] = np.array([1.0, 0.0, 0.0])
    (nul,) = oc.nulo_media([plant], pob, len(idx), 2000, [1, 3])
    _, enr, ps, pb, fl = oc.banderas(plant[idx].mean(axis=0), nul)
    assert list(fl) == ["SOBRE", "BAJO", "BAJO"], fl
    _, _, _, _, fl = oc.banderas(np.array([np.nan, 0.5, 0.25]), nul)
    assert fl[0] == "NA", fl
    return "nulo plano -> azar x3; plantado -> SOBRE/BAJO/BAJO; NaN -> NA"


def test_control_negativo_sin_senal_y_real_con_senal():
    rng = np.random.default_rng(11)
    N, K = 400, 3
    cls = np.repeat(np.arange(K), N // K + 1)[:N].astype(np.int8)
    rng.shuffle(cls)
    salida = np.arange(30)
    fuentes = np.flatnonzero(cls == 0)
    pre, post = [], []
    for j in range(N):
        if j < 30:
            src = rng.choice(fuentes, 12, replace=False)
        else:
            src = rng.choice(N, 12, replace=False)
        pre.extend(src.tolist())
        post.extend([j] * len(src))
    pre = np.array(pre, dtype=np.int32)
    post = np.array(post, dtype=np.int32)
    S = rng.integers(1, 9, len(pre)).astype(np.int32)
    exc = np.ones(len(pre), dtype=np.int8)
    V = oc.por_variante(pre, post, S, exc, cls, N, K, 1)
    r = oc.evaluar(V, K, {"O": salida}, 2000, 5)["O"]
    assert r["flag1"][0] == "SOBRE", r["flag1"]
    c = oc.control_negativo(pre, post, S, cls, N, K, 1, {"O": salida}, 2000, 5)
    assert c["flags"] <= 1, c
    return "plantado clase0->O da SOBRE; con etiquetas permutadas flags=%d/%d" % (c["flags"], c["tests"])


def test_extremo_a_extremo():
    rng = np.random.default_rng(3)
    N = 120
    ids = np.sort(np.unique(rng.integers(0, 10 ** 9, 4 * N))[:N] + 10 ** 17).astype(np.int64)
    assert len(ids) == N
    pre = rng.integers(0, N, 900)
    post = rng.integers(0, N, 900)
    key = np.unique(pre * N + post)
    pre = key // N
    post = key % N
    S = rng.integers(1, 10, len(pre))
    exc = rng.choice([-1, 1], len(pre))
    t = pa.table({"Presynaptic_ID": ids[pre], "Postsynaptic_ID": ids[post],
                  "Presynaptic_Index": pre.astype(np.int64), "Postsynaptic_Index": post.astype(np.int64),
                  "Connectivity": S.astype(np.int64), "Excitatory": exc.astype(np.int64),
                  "Excitatory x Connectivity": (S * exc).astype(np.int64)})
    sc = np.array(["central"] * N, dtype=object)
    sc[:10] = "descending"
    sc[10:16] = "motor"
    sc[16:20] = "endocrine"
    sc[20:60] = "sensory"
    sub = np.array([None] * N, dtype=object)
    sub[10:13] = "neck_motor_neuron"
    sub[13:16] = "proboscis_motor_neuron"
    ct = np.array([None] * N, dtype=object)
    ct[:10] = ["DNa", "DNb"] * 5
    ct[16:18] = "IPC"
    ct[18:20] = "DH44"
    filas = pd.DataFrame({"root_id": ids[2:].astype(str), "super_class": sc[2:], "cell_class": None,
                          "cell_sub_class": sub[2:], "cell_type": ct[2:]})
    with tempfile.TemporaryDirectory() as d:
        pqp = os.path.join(d, "c.parquet")
        tsv = os.path.join(d, "a.tsv")
        pq.write_table(t, pqp)
        filas.to_csv(tsv, sep="\t", index=False)
        out = os.path.join(d, "out")
        cp = subprocess.run([sys.executable, os.path.join(HERR, "output_control_by_class.py"),
                             "--parquet", pqp, "--annotations", tsv, "--cruce-tabla7", "",
                             "--out", out, "--r-nulo", "300", "--r-control", "200"],
                            capture_output=True, text=True)
        assert cp.returncode == 0, cp.stdout[-2000:] + cp.stderr[-2000:]
        for marca in ("VEREDICTO_MEDICION INCOMPLETO", "FIN_SALIDAS", "CRUCE_TABLA7 NO_MEDIDO",
                      "QUE_CONTROLA [>=1] central", "FINA [>=5] motor:neck_motor_neuron"):
            assert marca in cp.stdout, marca
        with open(os.path.join(out, "output_control_by_class.json")) as f:
            j = json.load(f)
        assert j["clases"]["sin_anotacion"] == 2, j["clases"]
        nombres = j["clases_orden"]
        cls = np.array([nombres.index(x) for x in ["sin_anotacion"] * 2 + list(sc[2:])], dtype=np.int8)
        idx = np.arange(0, 10)
        idx = idx[np.isin(idx, np.flatnonzero(np.array([x == "descending" for x in sc]) & (np.arange(N) >= 2)))]
        b = fuerza_bruta(pre, post, S, exc, cls, N, len(nombres), 1, idx)
        d1 = [j["variantes"][">=1"]["nivel1"]["descending"]["por_clase"][cn]["d1"] for cn in nombres]
        d1 = np.array([np.nan if v is None else v for v in d1])
        assert np.allclose(d1, b["d1"], equal_nan=True), (d1, b["d1"])
    return "extremo a extremo con parquet y TSV chicos, 2 nodos sin anotar, D1 == fuerza bruta"


if __name__ == "__main__":
    tests = [test_vectorizado_igual_fuerza_bruta, test_matriz_aristas_contra_conteo_directo,
             test_banderas_plantado_y_plano, test_control_negativo_sin_senal_y_real_con_senal,
             test_extremo_a_extremo]
    ok = 0
    for t in tests:
        print("TEST", t.__name__, "->", t())
        ok += 1
    print("TESTS_OK", ok)
