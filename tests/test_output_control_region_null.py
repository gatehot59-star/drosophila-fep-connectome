#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Tests de tools/output_control_region_null.py. Cada uno puede dar rojo."""
import json
import os
import subprocess
import sys
import tempfile

import numpy as np
import pandas as pd

AQUI = os.path.dirname(os.path.abspath(__file__))
HERR = os.path.join(AQUI, "..", "tools")
for d in (HERR, AQUI):
    if d not in sys.path:
        sys.path.insert(0, d)
import output_control_permutation_null as pn  # noqa: E402
import output_control_region_null as rn  # noqa: E402
from test_output_control_permutation_null import _datos_chicos  # noqa: E402


def test_permutador_rapido_conserva_estratos_y_es_uniforme():
    rng = np.random.default_rng(1)
    n = 600
    cls = rng.integers(0, 4, n).astype(np.int8)
    est = rng.integers(0, 25, n).astype(np.int64)
    P = rn.PermutadorRapido(cls, est)
    ref = np.bincount(cls.astype(np.int64) * 25 + est, minlength=100)
    movidas = 0
    for _ in range(200):
        lab = P(rng)
        assert np.array_equal(np.bincount(lab.astype(np.int64) * 25 + est, minlength=100), ref)
        movidas += int((lab != cls).sum())
    assert movidas > 0
    cls3 = np.array([0, 1, 2], dtype=np.int8)
    P3 = rn.PermutadorRapido(cls3, np.zeros(3, dtype=np.int64))
    cuenta = np.zeros((3, 3))
    vistas = {}
    for _ in range(6000):
        lab = P3(rng)
        cuenta[np.arange(3), lab] += 1
        vistas[tuple(lab)] = vistas.get(tuple(lab), 0) + 1
    frac = cuenta / 6000
    assert np.all(np.abs(frac - 1 / 3) < 0.03), frac
    assert len(vistas) == 6 and all(abs(v / 6000 - 1 / 6) < 0.03 for v in vistas.values()), vistas
    return "conserva clase x estrato en 200 permutaciones; las 6 permutaciones de 3 salen ~1/6 cada una"


def test_rapido_coincide_con_formulas_exactas():
    rng = np.random.default_rng(2)
    n, K, m = 400, 3, 3
    cls = rng.integers(0, K, n).astype(np.int8)
    est = rng.integers(0, 12, n).astype(np.int64)
    U = rng.random((n, m))
    nul, okc, oke, _ = rn.correr_nulo_rapido(cls, est, U, K, 4000, [3, 4])
    assert okc and oke
    esp = pn.esperanza(cls, est, U, K, "estr")
    var = pn.varianza_exacta(cls, est, U, K, "estr")
    zmax, ratio = pn.chequeo_momentos(nul.mean(axis=0), nul.std(axis=0, ddof=1), esp, var, 4000, np.arange(m))
    assert zmax < 5 and 0.9 <= ratio <= 1.1, (zmax, ratio)
    return "media y varianza del permutador rapido == formulas exactas de la 006 (z max %.2f, cociente %.3f)" % (
        zmax, ratio)


def test_kmedias_recupera_tres_grupos():
    rng = np.random.default_rng(5)
    centros = np.array([[0, 0, 0], [100, 0, 0], [0, 100, 50]], dtype=float)
    X = np.vstack([c + rng.normal(0, 5, (200, 3)) for c in centros])
    verdad = np.repeat(np.arange(3), 200)
    lab, info = rn.kmedias(X, 3, [7, 3])
    asign = [set(lab[verdad == gg].tolist()) for gg in range(3)]
    assert info["convergio"]
    assert all(len(s) == 1 for s in asign) and len(set().union(*asign)) == 3, asign
    lab2, _ = rn.kmedias(X, 3, [7, 3])
    assert np.array_equal(lab, lab2)
    return "k-medias recupera 3 grupos separados, converge en %d iteraciones y es determinista" % info["iteraciones"]


def test_mezcla_y_flag_efectivo():
    cls = np.array([0] * 10 + [1] * 10, dtype=np.int8)
    assert np.allclose(rn.mezcla(cls, np.zeros(20, dtype=np.int64), 2), [0.5, 0.5])
    assert np.allclose(rn.mezcla(cls, np.array([0] * 10 + [1] * 10, dtype=np.int64), 2), [0.0, 0.0])
    fl = np.array([["azar", "SOBRE"], ["azar", "BAJO"]])
    fe = rn.flag_efectivo(fl, np.array([0.05, 0.5]))
    assert fe.tolist() == [["NM", "SOBRE"], ["azar", "BAJO"]], fe
    return "mezcla = 1 - n_C/N con un estrato y 0 con clases separadas; azar con mezcla < 0,10 pasa a NM"


def _grafo_region(rng, salidas_por_clase):
    """Region A = neuronas 0..199 (clase 0: 0..99, clase 1: 100..199); region B = 200..599.
    Todas mandan 10 aristas a no salidas; las de A ademas mandan a O segun su clase."""
    n = 600
    cls = np.array([0] * 100 + [1] * 200 + [2] * 300, dtype=np.int8)
    salida = np.arange(560, 600)
    pre, post = [], []
    for i in range(n):
        dst = rng.choice(np.arange(560), 10, replace=False)
        pre.extend([i] * 10)
        post.extend(dst.tolist())
        if i < 200:
            k = salidas_por_clase[int(cls[i])]
            o = rng.choice(salida, k, replace=False)
            pre.extend([i] * k)
            post.extend(o.tolist())
    pre = np.array(pre, dtype=np.int32)
    post = np.array(post, dtype=np.int32)
    S = np.ones(len(pre), dtype=np.int32)
    es = np.zeros(n, dtype=bool)
    es[salida] = True
    reg = np.array([1] * 200 + [0] * 400, dtype=np.int64)
    return n, cls, pre, post, S, es, salida, reg


def _flags_estr_y_region(n, cls, pre, post, S, es, salida, reg, semilla):
    V = pn.vectores_u(pre, post, S, n, 1, {"O": salida})
    _, tam, _ = pn.estratos_por_fuerza(V["p"], V["q"], V["s"], n, es, 5)
    U1 = np.ascontiguousarray(V["U"][:, :1])
    D = pn.Sumador(n, 3)(cls, U1)
    res = {}
    for nombre, est in (("estr", tam), ("region", rn.combinar(reg, tam))):
        nul, _, _, _ = rn.correr_nulo_rapido(cls, est, U1, 3, 2000, semilla)
        res[nombre] = str(pn.evaluar_nulo(D, nul)["flag"][0, 0])
    return res


def test_geografia_engana_a_estr_y_no_a_region():
    rng = np.random.default_rng(13)
    lejos = _flags_estr_y_region(*_grafo_region(rng, {0: 3, 1: 3}), [8, 9])
    assert lejos["estr"] == "SOBRE" and lejos["region"] == "azar", lejos
    rng = np.random.default_rng(14)
    real = _flags_estr_y_region(*_grafo_region(rng, {0: 3, 1: 1}), [8, 9])
    assert real["estr"] == "SOBRE" and real["region"] == "SOBRE", real
    return ("clase que solo esta cerca de O: estr=%s, region=%s; clase que le habla mas que sus vecinas:"
            " estr=%s, region=%s" % (lejos["estr"], lejos["region"], real["estr"], real["region"]))


def test_extremo_a_extremo_contra_la_006():
    with tempfile.TemporaryDirectory() as d:
        pqp, tsv = _datos_chicos(d)
        a = pd.read_csv(tsv, sep="\t", dtype=str)
        rng = np.random.default_rng(21)
        for c, hi in (("pos_x", 200000), ("pos_y", 100000), ("pos_z", 7000)):
            a[c] = rng.integers(1000, hi, len(a)).astype(float).astype(str)
        a.to_csv(tsv, sep="\t", index=False)
        o5 = os.path.join(d, "o5")
        cp = subprocess.run([sys.executable, os.path.join(HERR, "output_control_by_class.py"), "--parquet", pqp,
                             "--annotations", tsv, "--cruce-tabla7", "", "--out", o5, "--r-nulo", "300",
                             "--r-control", "200"], capture_output=True, text=True)
        assert cp.returncode == 0, cp.stdout[-1500:] + cp.stderr[-1500:]
        o6 = os.path.join(d, "o6")
        cp = subprocess.run([sys.executable, os.path.join(HERR, "output_control_permutation_null.py"),
                             "--parquet", pqp, "--annotations", tsv, "--json-005",
                             os.path.join(o5, "output_control_by_class.json"), "--out", o6, "--r", "600",
                             "--n-falsos", "5", "--n-estratos", "10"], capture_output=True, text=True)
        assert cp.returncode == 0, cp.stdout[-1500:] + cp.stderr[-1500:]
        j6 = os.path.join(o6, "output_control_permutation_null.json")
        salidas = {}
        for r in ("600", "300"):
            cp = subprocess.run([sys.executable, os.path.join(HERR, "output_control_region_null.py"),
                                 "--parquet", pqp, "--annotations", tsv, "--json-006", j6, "--out",
                                 os.path.join(d, "o7_" + r), "--r", r, "--n-falsos", "5", "--k-regiones", "3,5",
                                 "--n-tam", "4"], capture_output=True, text=True)
            assert cp.returncode == 0, cp.stdout[-2500:] + cp.stderr[-2500:]
            salidas[r] = cp.stdout
        for marca in ("CRUCE_006 [>=1] PASS", "CRUCE_006 [>=5] PASS", "VEREDICTO_NULO PASS",
                      "R_PEDIDO_500 r=600 ok=True", "QUE_CONTROLA_REGION central", "MEZCLA [>=1] central"):
            assert marca in salidas["600"], marca
        assert "VEREDICTO_NULO INCOMPLETO" in salidas["300"]
        malo = json.load(open(j6))
        malo["variantes"][">=1"]["por_conjunto"]["descending"]["por_clase"]["central"]["d1"] += 1e-6
        j6m = os.path.join(d, "malo.json")
        json.dump(malo, open(j6m, "w"))
        cp = subprocess.run([sys.executable, os.path.join(HERR, "output_control_region_null.py"),
                             "--parquet", pqp, "--annotations", tsv, "--json-006", j6m, "--out",
                             os.path.join(d, "o7m"), "--r", "600", "--n-falsos", "5", "--k-regiones", "3,5",
                             "--n-tam", "4"], capture_output=True, text=True)
        assert cp.returncode == 1 and "CRUCE_006 [>=1] FAIL" in cp.stdout and "VEREDICTO_NULO FAIL" in cp.stdout
    return "extremo a extremo: 005 -> 006 -> 007, cruce PASS, R=300 da INCOMPLETO, un D1 movido 1e-6 da FAIL"


if __name__ == "__main__":
    tests = [test_permutador_rapido_conserva_estratos_y_es_uniforme, test_rapido_coincide_con_formulas_exactas,
             test_kmedias_recupera_tres_grupos, test_mezcla_y_flag_efectivo,
             test_geografia_engana_a_estr_y_no_a_region, test_extremo_a_extremo_contra_la_006]
    ok = 0
    for t in tests:
        print("TEST", t.__name__, "->", t())
        ok += 1
    print("TESTS_OK", ok)
