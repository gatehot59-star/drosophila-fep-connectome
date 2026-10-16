#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Tests de tools/output_control_region_correction.py. Cada uno puede dar rojo."""
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
import output_control_region_correction as cc  # noqa: E402
import output_control_region_null as rn  # noqa: E402
from test_output_control_permutation_null import _datos_chicos  # noqa: E402


def _bh_referencia(p):
    m = len(p)
    o = sorted(range(m), key=lambda i: p[i])
    q = np.empty(m)
    for r, i in enumerate(o):
        q[i] = min(1.0, min(p[o[j]] * m / (j + 1) for j in range(r, m)))
    return q


def _maxt_referencia(t, Z):
    R, m = Z.shape
    o = sorted(range(m), key=lambda i: -t[i])
    p = np.empty(m)
    prev = 0.0
    for r, i in enumerate(o):
        resto = o[r:]
        cnt = sum(1 for k in range(R) if max(Z[k, j] for j in resto) >= t[i])
        prev = max(prev, (1.0 + cnt) / (R + 1.0))
        p[i] = prev
    ss = np.array([(1.0 + sum(1 for k in range(R) if Z[k].max() >= t[i])) / (R + 1.0) for i in range(m)])
    return p, ss


def test_bh_y_by_contra_la_definicion():
    assert np.allclose(cc.bh(np.array([0.01, 0.04, 0.03, 0.005])), [0.02, 0.04, 0.04, 0.02])
    rng = np.random.default_rng(3)
    for _ in range(50):
        p = rng.random(int(rng.integers(1, 40))) ** 3
        p[rng.random(len(p)) < 0.2] = p[0]
        ref = _bh_referencia(p)
        assert np.allclose(cc.bh(p), ref)
        c = sum(1.0 / i for i in range(1, len(p) + 1))
        assert np.allclose(cc.by(p), np.minimum(1.0, ref * c))
    return "BH = definicion q_i = min_{j>=i} m p_(j) / j en 50 casos con empates; BY = BH x c(m)"


def test_maxt_contra_fuerza_bruta():
    rng = np.random.default_rng(4)
    for _ in range(20):
        m = int(rng.integers(1, 9))
        R = int(rng.integers(5, 60))
        Z = np.abs(rng.normal(size=(R, m)))
        t = np.abs(rng.normal(size=m)) * 1.5
        t[rng.random(m) < 0.2] = t[0]
        sd, ss = cc.maxt_stepdown(t, Z)
        rsd, rss = _maxt_referencia(t, Z)
        assert np.allclose(sd, rsd) and np.allclose(ss, rss), (sd, rsd, ss, rss)
        assert np.all(sd <= ss + 1e-15)
    return "step-down y single-step = fuerza bruta en 20 casos con empates; step-down <= single-step"


def test_maxt_controla_fwer_con_dependencia_y_tiene_poder():
    rng = np.random.default_rng(5)
    m, R, reps = 12, 400, 400
    L = rng.normal(size=(m, m)) / 3 + np.eye(m)
    malos = 0
    poder = 0
    for _ in range(reps):
        X = rng.normal(size=(R + 1, m)) @ L.T
        X = X - X.mean(axis=1, keepdims=True)
        sd = X.std(axis=0)
        Z = np.abs(X[1:]) / sd
        p, _ = cc.maxt_stepdown(np.abs(X[0]) / sd, Z)
        malos += int((p <= 0.05).any())
        x0 = X[0].copy()
        x0[0] += 8.0 * sd[0]
        p2, _ = cc.maxt_stepdown(np.abs(x0) / sd, Z)
        poder += int(p2[0] <= 0.05)
    fwer = malos / reps
    assert fwer <= 0.085, fwer
    assert poder / reps >= 0.95, poder / reps
    return ("FWER empirico %.3f (tope 0,085) con 12 tests correlacionados que suman cero; un efecto de 8 sd se"
            " detecta en el %.0f%%" % (fwer, 100.0 * poder / reps))


def test_resolucion_de_holm():
    assert not cc.holm_puede(5000, 242)
    assert cc.holm_puede(5000, 100)
    assert cc.holm_puede(100000, 242)
    return "con R = 5.000 y 242 tests Holm no puede rechazar nada (0,0004 > 0,05/242); con 100 tests o R = 100.000 si"


def test_familia_excluye_degenerados_y_detecta_lo_plantado():
    rng = np.random.default_rng(6)
    n, K = 600, 3
    cls = np.array([0] * 150 + [1] * 350 + [2] * 100, dtype=np.int8)
    est = np.concatenate([rng.integers(0, 5, 500), np.full(100, 5)]).astype(np.int64)
    U = rng.random((n, 2)) * 0.01
    U[:150, 0] *= 3.0
    D1 = pn.Sumador(n, K)(cls, U)
    nul, _, _, _ = rn.correr_nulo_rapido(cls, est, U, K, 2000, [6, 1])
    E = pn.esperanza(cls, est, U, K, "estr")
    V = pn.varianza_exacta(cls, est, U, K, "estr")
    fam = cc.corregir_familia(D1, nul, E, V, np.array([True, True]))
    assert fam["m"] == 4 and not fam["testeable"][2].any() and fam["testeable"][:2].all()
    for mt in cc.METODOS:
        d = fam["decision"][mt]
        assert d[0, 0] == "SOBRE" and d[1, 0] == "BAJO" and (d[2] == "-").all(), (mt, d)
    assert all(fam["consistencia"].values())
    return ("la clase sin mezcla queda afuera de la familia (m = 4 de 6); el efecto plantado sale SOBRE y su"
            " vecina BAJO con maxT, BH y BY")


def test_extremo_a_extremo_007_a_008():
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
            o7 = os.path.join(d, "o7_" + r)
            cp = subprocess.run([sys.executable, os.path.join(HERR, "output_control_region_null.py"),
                                 "--parquet", pqp, "--annotations", tsv, "--json-006", j6, "--out", o7,
                                 "--r", r, "--n-falsos", "5", "--k-regiones", "3,5", "--n-tam", "4"],
                                capture_output=True, text=True)
            assert cp.returncode == 0, cp.stdout[-2500:] + cp.stderr[-2500:]
            cp = subprocess.run([sys.executable, os.path.join(HERR, "output_control_region_correction.py"),
                                 "--parquet", pqp, "--annotations", tsv, "--json-007",
                                 os.path.join(o7, "output_control_region_null.json"), "--out",
                                 os.path.join(d, "o8_" + r)], capture_output=True, text=True)
            assert cp.returncode == 0, cp.stdout[-2500:] + cp.stderr[-2500:]
            salidas[r] = cp.stdout
        for marca in ("CRUCE_007 PASS", "CONSISTENCIA PASS", "VEREDICTO_CORRECCION PASS", "FAMILIA [>=1] reg3 m=",
                      "FAMILIA [>=5] reg5 m=", "RESOLUCION r=600", "CONTROL_NEGATIVO maxT=", "RESUMEN firmes_007="):
            assert marca in salidas["600"], marca
        assert "VEREDICTO_CORRECCION INCOMPLETO" in salidas["300"]
        j7 = os.path.join(d, "o7_600", "output_control_region_null.json")
        malo = json.load(open(j7))
        malo["variantes"][">=1"]["por_conjunto"]["descending"]["por_clase"]["central"]["reg3"]["ps"] += 1e-6
        j7m = os.path.join(d, "malo.json")
        json.dump(malo, open(j7m, "w"))
        cp = subprocess.run([sys.executable, os.path.join(HERR, "output_control_region_correction.py"),
                             "--parquet", pqp, "--annotations", tsv, "--json-007", j7m, "--out",
                             os.path.join(d, "o8m")], capture_output=True, text=True)
        assert cp.returncode == 1 and "CRUCE_007 FAIL" in cp.stdout and "VEREDICTO_CORRECCION FAIL" in cp.stdout
    return ("extremo a extremo: 005 -> 006 -> 007 -> 008, el nulo regenerado da los mismos p, R=300 da INCOMPLETO"
            " y un p movido 1e-6 en el JSON de la 007 da FAIL")


if __name__ == "__main__":
    tests = [test_bh_y_by_contra_la_definicion, test_maxt_contra_fuerza_bruta,
             test_maxt_controla_fwer_con_dependencia_y_tiene_poder, test_resolucion_de_holm,
             test_familia_excluye_degenerados_y_detecta_lo_plantado, test_extremo_a_extremo_007_a_008]
    ok = 0
    for t in tests:
        print("TEST", t.__name__, "->", t())
        ok += 1
    print("TESTS_OK", ok)
