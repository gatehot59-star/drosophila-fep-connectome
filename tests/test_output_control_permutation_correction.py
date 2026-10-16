#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Tests de tools/output_control_permutation_correction.py. Cada uno puede dar rojo."""
import json
import os
import subprocess
import sys
import tempfile

import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
HERR = os.path.join(AQUI, "..", "tools")
for d in (HERR, AQUI):
    if d not in sys.path:
        sys.path.insert(0, d)
import output_control_permutation_correction as pc  # noqa: E402
import output_control_permutation_null as pn  # noqa: E402
import output_control_region_correction as cc  # noqa: E402
from test_output_control_permutation_null import _datos_chicos  # noqa: E402


def _holm_referencia(p):
    m = len(p)
    o = sorted(range(m), key=lambda i: p[i])
    q = np.empty(m)
    for r, i in enumerate(o):
        q[i] = min(1.0, max((m - j) * p[o[j]] for j in range(r + 1)))
    return q


def test_holm_contra_la_definicion():
    assert np.allclose(pc.holm(np.array([0.01, 0.04, 0.03, 0.005])), [0.03, 0.06, 0.06, 0.02])
    rng = np.random.default_rng(7)
    for _ in range(50):
        p = rng.random(int(rng.integers(1, 40))) ** 3
        p[rng.random(len(p)) < 0.2] = p[0]
        h = pc.holm(p)
        assert np.allclose(h, _holm_referencia(p))
        assert np.all(h >= cc.bh(p) - 1e-15) and np.all(h <= np.minimum(1.0, len(p) * p) + 1e-15)
    return "Holm = definicion max_{j<=i} (m - j + 1) p_(j) en 50 casos con empates; BH <= Holm <= Bonferroni"


def test_holm_controla_fwer_y_resolucion():
    from scipy.stats import norm
    rng = np.random.default_rng(8)
    reps, m = 20000, 50
    L = rng.normal(size=(m, m)) / 3 + np.eye(m)
    Z = (rng.normal(size=(reps, m)) @ L.T) / np.sqrt((L * L).sum(axis=1))
    tasas = []
    for P in (rng.random((reps, m)), 2 * norm.sf(np.abs(Z))):
        tasas.append(float(np.mean([(pc.holm(P[i]) <= 0.05).any() for i in range(reps)])))
    assert max(tasas) <= 0.056, tasas
    piso = 2.0 / 10001.0
    assert pc.holm(np.full(250, piso)).max() <= 0.05 and pc.holm(np.full(251, piso)).min() > 0.05
    assert cc.holm_puede(10000, 250) and not cc.holm_puede(10000, 251)
    return ("FWER de Holm %.4f independientes y %.4f correlacionados en 20.000 repeticiones (tope 0,056); con"
            " R = 10.000 rechaza en el piso con 250 tests y no con 251" % tuple(tasas))


def test_corregir_agrega_holm_y_detecta_lo_plantado():
    rng = np.random.default_rng(9)
    n, K = 600, 3
    cls = np.array([0] * 150 + [1] * 350 + [2] * 100, dtype=np.int8)
    est = np.concatenate([rng.integers(0, 5, 500), np.full(100, 5)]).astype(np.int64)
    U = rng.random((n, 2)) * 0.01
    U[:150, 0] *= 3.0
    D = pn.Sumador(n, K)(cls, U)
    for mi, modo in enumerate(pn.MODOS):
        nul, _, _, _ = pn.correr_nulo(cls, est, modo, U, K, 2000, [9, mi])
        E = pn.esperanza(cls, est, U, K, modo)
        V = pn.varianza_exacta(cls, est, U, K, modo)
        fam = pc.corregir(D, nul, E, V, np.array([True, True]))
        assert all(fam["consistencia"].values()), fam["consistencia"]
        for mt in pc.METODOS:
            assert fam["decision"][mt][0, 0] == "SOBRE", (modo, mt, fam["decision"][mt])
        assert np.isfinite(fam["p_aj"]["Holm"][0, 0])
        if modo == "estr":
            assert fam["m"] == 4 and not fam["testeable"][2].any()
        else:
            assert fam["m"] == 6 and fam["testeable"].all()
    return ("con perm y con estr el efecto plantado sale SOBRE con max-T, Holm, BH y BY; la clase sin mezcla sale de"
            " la familia solo en estr (m = 4 contra 6)")


def test_regla_de_firmes_de_la_006():
    d1 = np.array([["SOBRE", "BAJO", "BAJO"], ["azar", "SOBRE", "SOBRE"]])
    d5 = np.array([["SOBRE", "BAJO", "BAJO"], ["SOBRE", "SOBRE", "azar"]])
    es_n1 = np.array([True, True, False])
    f = pc.firmes_regla_006(d1, d5, np.array([True, True, True]), es_n1)
    assert f.tolist() == [["SOBRE", "BAJO", "-"], ["-", "SOBRE", "-"]], f.tolist()
    f = pc.firmes_regla_006(d1, d5, np.array([True, False, True]), es_n1)
    assert f.tolist() == [["SOBRE", "-", "-"], ["-", "-", "-"]], f.tolist()
    return "SOBRE en los dos umbrales en cualquier conjunto, BAJO en los dos solo en nivel 1, nada sin entrada en los dos"


def test_extremo_a_extremo_006_a_009():
    with tempfile.TemporaryDirectory() as d:
        pqp, tsv = _datos_chicos(d)
        o5 = os.path.join(d, "o5")
        cp = subprocess.run([sys.executable, os.path.join(HERR, "output_control_by_class.py"), "--parquet", pqp,
                             "--annotations", tsv, "--cruce-tabla7", "", "--out", o5, "--r-nulo", "300",
                             "--r-control", "200"], capture_output=True, text=True)
        assert cp.returncode == 0, cp.stdout[-1500:] + cp.stderr[-1500:]
        salidas = {}
        for r in ("600", "300"):
            o6 = os.path.join(d, "o6_" + r)
            cp = subprocess.run([sys.executable, os.path.join(HERR, "output_control_permutation_null.py"),
                                 "--parquet", pqp, "--annotations", tsv, "--json-005",
                                 os.path.join(o5, "output_control_by_class.json"), "--out", o6, "--r", r,
                                 "--n-falsos", "5", "--n-estratos", "10"], capture_output=True, text=True)
            assert cp.returncode == 0, cp.stdout[-1500:] + cp.stderr[-1500:]
            cp = subprocess.run([sys.executable, os.path.join(HERR, "output_control_permutation_correction.py"),
                                 "--parquet", pqp, "--annotations", tsv, "--json-006",
                                 os.path.join(o6, "output_control_permutation_null.json"), "--out",
                                 os.path.join(d, "o9_" + r)], capture_output=True, text=True)
            assert cp.returncode == 0, cp.stdout[-2500:] + cp.stderr[-2500:]
            salidas[r] = cp.stdout
        for marca in ("CRUCE_006 PASS", "firmes=True", "CONSISTENCIA PASS", "VEREDICTO_CORRECCION PASS",
                      "FAMILIA [>=1] perm D1 m=", "FAMILIA [>=5] estr D2 m=", "RESOLUCION r=600",
                      "CONTROL_NEGATIVO maxT=", "RESUMEN firmes_006="):
            assert marca in salidas["600"], marca
        assert "VEREDICTO_CORRECCION INCOMPLETO" in salidas["300"]
        j6 = os.path.join(d, "o6_600", "output_control_permutation_null.json")
        for nombre, tocar in (("p", lambda j: j["variantes"][">=1"]["por_conjunto"]["descending"]["por_clase"]
                                ["central"]["estr"].__setitem__("ps1", j["variantes"][">=1"]["por_conjunto"]
                                                               ["descending"]["por_clase"]["central"]["estr"]
                                                               ["ps1"] + 1e-6)),
                              ("firmes", lambda j: j["que_controla_firme"].__setitem__(
                                  "central", j["que_controla_firme"]["central"] + " x"))):
            malo = json.load(open(j6))
            tocar(malo)
            j6m = os.path.join(d, "malo_%s.json" % nombre)
            json.dump(malo, open(j6m, "w"))
            cp = subprocess.run([sys.executable, os.path.join(HERR, "output_control_permutation_correction.py"),
                                 "--parquet", pqp, "--annotations", tsv, "--json-006", j6m, "--out",
                                 os.path.join(d, "o9m_" + nombre)], capture_output=True, text=True)
            assert cp.returncode == 1 and "CRUCE_006 FAIL" in cp.stdout and "%s=False" % nombre in cp.stdout, nombre
            assert "VEREDICTO_CORRECCION FAIL" in cp.stdout
    return ("extremo a extremo: 005 -> 006 -> 009, el nulo regenerado da los mismos p y las mismas firmes, R=300 da"
            " INCOMPLETO, y un p movido 1e-6 o una linea de firmes tocada en el JSON de la 006 dan FAIL")


if __name__ == "__main__":
    tests = [test_holm_contra_la_definicion, test_holm_controla_fwer_y_resolucion,
             test_corregir_agrega_holm_y_detecta_lo_plantado, test_regla_de_firmes_de_la_006,
             test_extremo_a_extremo_006_a_009]
    ok = 0
    for t in tests:
        print("TEST", t.__name__, "->", t())
        ok += 1
    print("TESTS_OK", ok)
