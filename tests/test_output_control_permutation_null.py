#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Tests de tools/output_control_permutation_null.py. Cada uno puede dar rojo."""
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
for d in (HERR, AQUI):
    if d not in sys.path:
        sys.path.insert(0, d)
import output_control_by_class as oc  # noqa: E402
import output_control_permutation_null as pn  # noqa: E402
from test_output_control_by_class import fuerza_bruta, grafo_azar  # noqa: E402


def test_u_igual_fuerza_bruta_y_005():
    for seed in (1, 2, 3):
        pre, post, S, exc, cls, N, K = grafo_azar(seed)
        idx = np.array(sorted(np.random.default_rng(seed + 10).choice(N, 9, replace=False)))
        for umbral in (1, 5):
            V = pn.vectores_u(pre, post, S, N, umbral, {"O": idx})
            D = pn.Sumador(N, K)(cls, V["U"])
            b = fuerza_bruta(pre, post, S, exc, cls, N, K, umbral, idx)
            r = oc.medir(oc.por_variante(pre, post, S, exc, cls, N, K, umbral), K, {"O": idx})["O"]
            if V["n_in"]["O"] == 0:
                assert np.all(D == 0) and np.all(np.isnan(b["d1"]))
                continue
            assert np.allclose(D[:, 0], b["d1"], atol=1e-12), (seed, umbral, D[:, 0], b["d1"])
            assert np.allclose(D[:, 1], b["d2"], atol=1e-12), (seed, umbral, D[:, 1], b["d2"])
            assert np.allclose(D[:, 0], r["d1"], atol=1e-12) and np.allclose(D[:, 1], r["d2"], atol=1e-12)
    return "D1 y D2 por vectores u == fuerza bruta == medir() de la 005 (3 grafos x 2 umbrales)"


def test_permutador_conserva_conteos_y_los_brazos_difieren():
    rng = np.random.default_rng(5)
    cls = rng.integers(0, 4, 500).astype(np.int8)
    est = rng.integers(0, 7, 500).astype(np.int64)
    ref_c = np.bincount(cls, minlength=4)
    ref_e = np.bincount(cls.astype(np.int64) * 7 + est, minlength=28)
    for modo in ("perm", "estr"):
        P = pn.Permutador(cls, est, modo)
        movidas = 0
        for _ in range(50):
            lab = P(rng)
            assert np.array_equal(np.bincount(lab, minlength=4), ref_c), modo
            if modo == "estr":
                assert np.array_equal(np.bincount(lab.astype(np.int64) * 7 + est, minlength=28), ref_e)
            movidas += int((lab != cls).sum())
        assert movidas > 0, modo
    lab = pn.Permutador(cls, est, "perm")(np.random.default_rng(9))
    assert not np.array_equal(np.bincount(lab.astype(np.int64) * 7 + est, minlength=28), ref_e)
    return "perm conserva clases; estr conserva clases por estrato; perm NO conserva estratos"


def test_esperanza_exacta_y_control_negativo():
    rng = np.random.default_rng(6)
    n, K, m = 300, 3, 4
    cls = rng.integers(0, K, n).astype(np.int8)
    est = rng.integers(0, 5, n).astype(np.int64)
    U = rng.random((n, m))
    zs = []
    for modo in ("perm", "estr"):
        nul, okc, oke, _ = pn.correr_nulo(cls, est, modo, U, K, 4000, [1, 2])
        assert okc and oke
        esp = pn.esperanza(cls, est, U, K, modo)
        var = pn.varianza_exacta(cls, est, U, K, modo)
        sd = nul.std(axis=0, ddof=1)
        zmax, ratio = pn.chequeo_momentos(nul.mean(axis=0), sd, esp, var, 4000, np.arange(m))
        assert zmax < 5, (modo, zmax)
        assert 0.9 <= ratio <= 1.1, (modo, ratio)
        assert np.all(np.abs(sd ** 2 / var - 1) < 0.2), (modo, sd ** 2 / var)
        zs.append(zmax)
        mal = esp.copy()
        mal[0, 0] *= 1.05
        zm, _ = pn.chequeo_momentos(nul.mean(axis=0), sd, mal, var, 4000, np.arange(m))
        assert zm > 6, (modo, zm)
        _, rm = pn.chequeo_momentos(nul.mean(axis=0), sd, esp, var * 1.5, 4000, np.arange(m))
        assert not (0.9 <= rm <= 1.1), (modo, rm)
        c = pn.control_negativo(cls, est, modo, U, K, nul, 20, [3, 4], np.arange(m))
        assert c["ok"], c
    return ("media y varianza del nulo == formulas exactas (max z %.2f / %.2f); 5%% de error en la media"
            " o 50%% en la varianza lo ponen en rojo; control OK" % tuple(zs))


def test_evento_raro_no_da_infinito():
    n, K = 5000, 3
    cls = np.array([0] * 2 + [1] * 2498 + [2] * 2500, dtype=np.int8)
    est = np.zeros(n, dtype=np.int64)
    U = np.zeros((n, 1))
    U[4000, 0] = 1.0
    nul, _, _, _ = pn.correr_nulo(cls, est, "perm", U, K, 200, [5, 5])
    media, sd = nul.mean(axis=0), nul.std(axis=0, ddof=1)
    esp = pn.esperanza(cls, est, U, K, "perm")
    var = pn.varianza_exacta(cls, est, U, K, "perm")
    assert sd[0, 0] == 0 and media[0, 0] == 0 and esp[0, 0] > 0
    zmax, _ = pn.chequeo_momentos(media, sd, esp, var, 200, np.arange(1))
    assert np.isfinite(zmax) and zmax < 6, zmax
    return "clase de 2 neuronas y un solo presinaptico: el nulo nunca lo toca y z = %.2f (antes daba infinito)" % zmax


def _grafo_plantado(seed):
    rng = np.random.default_rng(seed)
    N, K = 400, 3
    cls = np.repeat(np.arange(K), N // K + 1)[:N].astype(np.int8)
    rng.shuffle(cls)
    salida = np.arange(30)
    fuentes = np.flatnonzero(cls == 0)
    pre, post = [], []
    for j in range(N):
        src = rng.choice(fuentes, 12, replace=False) if j < 30 else rng.choice(N, 12, replace=False)
        pre.extend(src.tolist())
        post.extend([j] * len(src))
    pre = np.array(pre, dtype=np.int32)
    post = np.array(post, dtype=np.int32)
    S = rng.integers(1, 9, len(pre)).astype(np.int32)
    return pre, post, S, cls, N, K, salida


def test_plantado_sobre_en_los_dos_nulos():
    pre, post, S, cls, N, K, salida = _grafo_plantado(11)
    es = np.zeros(N, dtype=bool)
    es[salida] = True
    V = pn.vectores_u(pre, post, S, N, 1, {"O": salida})
    _, est, _ = pn.estratos_por_fuerza(V["p"], V["q"], V["s"], N, es, 10)
    D = pn.Sumador(N, K)(cls, V["U"])
    for modo in ("perm", "estr"):
        nul, _, _, _ = pn.correr_nulo(cls, est, modo, V["U"], K, 2000, [5, 6])
        fl = pn.evaluar_nulo(D, nul)["flag"]
        assert fl[0, 0] == "SOBRE", (modo, fl[:, 0])
    return "clase 0 que alimenta sola a O: SOBRE con perm y con estr"


def test_confusion_por_tamano_perm_cae_estr_no():
    rng = np.random.default_rng(12)
    n, K = 600, 3
    cls = np.array([0] * 100 + [1] * 200 + [2] * 300, dtype=np.int8)
    grande = np.zeros(n, dtype=bool)
    grande[:200] = True
    pre, post = [], []
    for i in range(n):
        k = 30 if grande[i] else 3
        dst = rng.choice(n, k, replace=False)
        pre.extend([i] * k)
        post.extend(dst.tolist())
    pre = np.array(pre, dtype=np.int32)
    post = np.array(post, dtype=np.int32)
    S = np.ones(len(pre), dtype=np.int32)
    salida = np.sort(rng.choice(n, 40, replace=False))
    es = np.zeros(n, dtype=bool)
    es[salida] = True
    V = pn.vectores_u(pre, post, S, n, 1, {"O": salida})
    _, est, _ = pn.estratos_por_fuerza(V["p"], V["q"], V["s"], n, es, 10)
    D = pn.Sumador(n, K)(cls, V["U"])
    res = {}
    for modo in ("perm", "estr"):
        nul, _, _, _ = pn.correr_nulo(cls, est, modo, V["U"], K, 2000, [7, 8])
        res[modo] = str(pn.evaluar_nulo(D, nul)["flag"][0, 0])
    assert res["perm"] == "SOBRE", res
    assert res["estr"] == "azar", res
    return "neuronas grandes con destinos al azar: perm=%s, estr=%s" % (res["perm"], res["estr"])


def _datos_chicos(d):
    rng = np.random.default_rng(3)
    N = 120
    ids = np.sort(np.unique(rng.integers(0, 10 ** 9, 4 * N))[:N] + 10 ** 17).astype(np.int64)
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
    pqp = os.path.join(d, "c.parquet")
    tsv = os.path.join(d, "a.tsv")
    pq.write_table(t, pqp)
    filas.to_csv(tsv, sep="\t", index=False)
    return pqp, tsv


def test_extremo_a_extremo_contra_la_005():
    with tempfile.TemporaryDirectory() as d:
        pqp, tsv = _datos_chicos(d)
        o5 = os.path.join(d, "o5")
        cp = subprocess.run([sys.executable, os.path.join(HERR, "output_control_by_class.py"), "--parquet", pqp,
                             "--annotations", tsv, "--cruce-tabla7", "", "--out", o5, "--r-nulo", "300",
                             "--r-control", "200"], capture_output=True, text=True)
        assert cp.returncode == 0, cp.stdout[-1500:] + cp.stderr[-1500:]
        j5 = os.path.join(o5, "output_control_by_class.json")
        salidas = {}
        for r in ("600", "300"):
            on = os.path.join(d, "on" + r)
            cp = subprocess.run([sys.executable, os.path.join(HERR, "output_control_permutation_null.py"),
                                 "--parquet", pqp, "--annotations", tsv, "--json-005", j5, "--out", on,
                                 "--r", r, "--n-falsos", "5", "--n-estratos", "10"],
                                capture_output=True, text=True)
            assert cp.returncode == 0, cp.stdout[-2000:] + cp.stderr[-2000:]
            salidas[r] = cp.stdout
        for marca in ("CRUCE_005 [>=1] PASS", "CRUCE_005 [>=5] PASS", "VEREDICTO_NULO PASS",
                      "R_PEDIDO_500 r=600 ok=True", "QUE_CONTROLA_FIRME central"):
            assert marca in salidas["600"], marca
        assert "VEREDICTO_NULO INCOMPLETO" in salidas["300"]
        assert "R_PEDIDO_500 r=300 ok=False" in salidas["300"]
        with open(os.path.join(d, "on600", "output_control_permutation_null.json")) as f:
            j = json.load(f)
        assert j["variantes"][">=1"]["cruce_005"]["max_dif"] <= 1e-12
        malo = json.load(open(j5))
        malo["variantes"][">=1"]["nivel1"]["descending"]["por_clase"]["central"]["d1"] += 1e-6
        j5m = os.path.join(d, "malo.json")
        json.dump(malo, open(j5m, "w"))
        cp = subprocess.run([sys.executable, os.path.join(HERR, "output_control_permutation_null.py"),
                             "--parquet", pqp, "--annotations", tsv, "--json-005", j5m, "--out",
                             os.path.join(d, "onm"), "--r", "600", "--n-falsos", "5", "--n-estratos", "10"],
                            capture_output=True, text=True)
        assert cp.returncode == 1 and "CRUCE_005 [>=1] FAIL" in cp.stdout and "VEREDICTO_NULO FAIL" in cp.stdout
    return "extremo a extremo: cruce con la 005 PASS, R=300 da INCOMPLETO, un D1 movido 1e-6 da FAIL"


if __name__ == "__main__":
    tests = [test_u_igual_fuerza_bruta_y_005, test_permutador_conserva_conteos_y_los_brazos_difieren,
             test_esperanza_exacta_y_control_negativo, test_evento_raro_no_da_infinito,
             test_plantado_sobre_en_los_dos_nulos,
             test_confusion_por_tamano_perm_cae_estr_no, test_extremo_a_extremo_contra_la_005]
    ok = 0
    for t in tests:
        print("TEST", t.__name__, "->", t())
        ok += 1
    print("TESTS_OK", ok)
