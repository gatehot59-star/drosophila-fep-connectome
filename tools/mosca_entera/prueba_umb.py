#!/usr/bin/env python3
"""Prueba del instrumento de H_ENTERA_UMBRAL (respuesta 2026-10-14-051). Grafos chicos, numeros plantados.

Sello: tools/mosca_entera/SELLO-UMBRAL-050.md (868ded6). Siete pruebas: la dinamica contra una cuenta densa
aparte, el umbral en una neurona sola contra la cuenta cerrada, la regla de calibracion, el estimulo del humo, los
nulos de la 049, las bandas con numeros plantados y el agregado de punta a punta.
Uso: python3 prueba_umb.py [--exigir]
"""
import argparse
import json
import os
import sys
import tempfile

import numpy as np
import pandas as pd
import scipy.sparse as sp

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import agregar_umb as au  # noqa: E402
import liq_entera as le  # noqa: E402
import umb_entera as ue  # noqa: E402

OK = []
ESPERADAS = 7


def test(nombre, desc):
    def deco(f):
        def g(*a, **k):
            f(*a, **k)
            OK.append(nombre)
            print("TEST %s -> %s" % (nombre, desc), flush=True)
        return g
    return deco


def grafo_chico(n=60, m=400, semilla=7):
    rng = np.random.default_rng(semilla)
    pre = rng.integers(0, n, m)
    post = rng.integers(0, n, m)
    w = rng.integers(1, 20, m).astype(np.float64) * rng.choice([-1.0, 1.0], m, p=[0.3, 0.7])
    return pre, post, w


@test("umb_contra_cuenta_densa", "simular_umb == una cuenta densa escrita aparte, con theta 0 y 0,2 (1e-12)")
def t_densa():
    n = 60
    pre, post, w = grafo_chico(n)
    W, _ = le.matriz(n, pre, post, w)
    Wd = W.toarray()
    tau = le.tau_por_root(np.arange(720575940600000000, 720575940600000000 + n), 30)
    estim = np.arange(5)
    x = np.zeros(n)
    x[estim] = 1.0
    for th in (0.0, 0.2):
        z = np.zeros(n)
        acum = np.zeros(n)
        for t in range(200):
            z = z + (le.DT / tau) * (np.tanh(np.clip(Wd.dot(z) + x - th, 0.0, None)) - z)
            if t >= 150:
                acum = acum + z
        r = ue.simular_umb(W, tau, estim, th)
        assert float(np.abs(r - acum / 50).max()) <= 1e-12, th
        assert (r >= 0).all() and ue.activas(r, estim) > 0
    r0 = ue.simular_umb(W, tau, estim, 0.0)
    rt, _ = le.simular(W, tau, estim, False)
    assert float(np.abs(r0 - rt).max()) > 1e-3, "con theta 0 UMB no es TASA: corta los negativos"


@test("umbral_neurona_sola", "una neurona: theta 1,5 la deja en 0 exacto; theta 0,5 da la cuenta cerrada")
def t_sola():
    W1 = sp.csr_matrix((1, 1))
    tau1 = np.array([0.1])
    assert ue.simular_umb(W1, tau1, np.array([0]), 1.5)[0] == 0.0
    r = ue.simular_umb(W1, tau1, np.array([0]), 0.5)[0]
    th = le.DT / 0.1
    esp = np.mean([np.tanh(0.5) * (1 - (1 - th) ** t) for t in range(151, 201)])
    assert abs(r - esp) <= 1e-12, (r, esp)


@test("calibracion_regla_del_sello", "theta = el mas chico probado con Activas <= N; NO_ALCANZA, NO_BAJA y conteo")
def t_calib():
    n = 300
    pre, post, w = grafo_chico(n, 3000, 11)
    W, _ = le.matriz(n, pre, post, w)
    tau = le.tau_por_root(np.arange(720575940600000000, 720575940600000000 + n), 30)
    estim = np.arange(10)
    a0 = ue.activas(ue.simular_umb(W, tau, estim, 0.0), estim)
    obj = a0 // 3
    c = ue.calibrar(W, tau, estim, objetivo=obj, tol=max(1, obj // 10))
    validos = [th for th, a in c["probados"] if a <= obj]
    assert c["theta"] == min(validos) and c["activas"] <= obj, c["probados"]
    assert c["activas"] == ue.activas(ue.simular_umb(W, tau, estim, c["theta"]), estim)
    n_hi = 0
    for th, _ in c["probados"][1:]:
        if th in (1.0, 2.0, 4.0, 8.0):
            n_hi += 1
        else:
            break
    assert len(c["probados"]) == 1 + n_hi + 24, (len(c["probados"]), n_hi)
    assert c["estado"] in ("OK", "FUERA")
    c2 = ue.calibrar(W, tau, estim, objetivo=a0 + 5)
    assert c2["estado"] == "NO_ALCANZA" and c2["theta"] == 0.0 and len(c2["probados"]) == 1
    fijo = lambda W_, t_, e_, th: np.ones(W_.shape[0])
    c3 = ue.calibrar(W, tau, estim, objetivo=5, sim=fijo)
    assert c3["estado"] == "NO_BAJA" and c3["theta"] == 8.0, c3["probados"]


@test("estimulo_del_humo", "20 no sensoriales al azar con semilla 99, sin azucar ni MN9, siempre las mismas")
def t_humo():
    with tempfile.TemporaryDirectory() as d:
        ids = np.array(le.SUGAR[:13] + le.SUGAR[14:] + [le.MN9] + list(range(720575940000000000,
                                                                              720575940000000000 + 200)))
        sc = ["sensory"] * 20 + ["motor"] + ["sensory"] * 30 + ["central"] * 170
        pd.DataFrame({"root_id": ids, "super_class": sc, "otra": 1}).to_csv(os.path.join(d, "a.tsv"), sep=chr(9),
                                                                          index=False)
        e1 = ue.estimulo_humo(ids, os.path.join(d, "a.tsv"))
        e2 = ue.estimulo_humo(ids, os.path.join(d, "a.tsv"))
        assert np.array_equal(e1, e2) and len(e1) == 20 and len(set(e1.tolist())) == 20
        assert all(sc[i] == "central" for i in e1), [sc[i] for i in e1]


@test("nulos_de_la_049", "los nulos son nulo() y matriz_g1() de liq_entera: la misma matriz que la 049, bit a bit")
def t_nulos():
    n = 60
    pre, post, w = grafo_chico(n)
    for tipo, k in (("SHUF_W", 3), ("SHUF_G", 32)):
        p2, q2, w2 = le.nulo(pre, post, w, tipo, k)
        Wa, ra = le.matriz_g1(n, p2, q2, w2, 0.01)
        Wb = (sp.coo_matrix((w2, (q2, p2)), shape=(n, n)).tocsr() * 0.01).tocsr()
        assert abs(Wa - Wb).max() == 0.0
    import inspect
    fuente = inspect.getsource(ue.main)
    assert "le.nulo(pre, post, w, a.tipo, k)" in fuente and "le.matriz_g1(n, p2, q2, w2, c)" in fuente


@test("bandas_y_controles", "MN9, CONJUNTO y GANA con numeros plantados; un control en rojo deja todo NO_MEDIDO")
def t_bandas():
    n40 = lambda v: {"SHUF_W": [v] * 40, "SHUF_G": [v] * 40}
    v = au.veredictos(True, 0.5, n40(0.0), 0.6, n40(0.2), 0.5)
    assert (v["MN9"], v["CONJUNTO"], v["GANA"]) == ("SOSTENIDA", "SOSTENIDA", "SOSTENIDA"), v
    assert "destilacion" in au.lectura(v, 0.5)
    v = au.veredictos(True, 0.0, n40(0.0), 0.6, n40(0.2), 0.6)
    assert v["MN9"] == "REFUTADA" and v["GANA"] == "REFUTADA" and au.lectura(v, 0.0).startswith("MN9 no entra")
    cinco = {"SHUF_W": [0.9] * 5 + [0.0] * 35, "SHUF_G": [0.0] * 40}
    v = au.veredictos(True, 0.5, cinco, 0.6, n40(0.2), 0.58)
    assert v["MN9"] == "REFUTADA" and v["GANA"] == "SIN_DECIDIR" and "no es especifico" in au.lectura(v, 0.5)
    uno = {"SHUF_W": [0.9] + [0.0] * 39, "SHUF_G": [0.0] * 40}
    v = au.veredictos(True, 0.5, uno, 0.6, n40(0.7), 0.5)
    assert v["MN9"] == "SIN_DECIDIR" and v["CONJUNTO"] == "REFUTADA" and "no lo resuelven" in au.lectura(v, 0.5)
    v = au.veredictos(False, 0.5, n40(0.0), 0.6, n40(0.2), 0.5)
    assert all(v[h] == "NO_MEDIDO" for h in ("MN9", "CONJUNTO", "GANA")), v
    pin = {"conn": au.MD5["conn"], "annot": au.MD5["annot"], "lif": au.MD5["lif"]}
    base = {"md5": pin, "activas": 330, "estado": "OK", "J_tasa": au.J_TASA_049}
    assert au.controles(base, [{"md5": pin}])["ok"]
    assert not au.controles(dict(base, activas=360), [{"md5": pin}])["ok"]
    assert not au.controles(dict(base, J_tasa=au.J_TASA_049 + 1e-8), [{"md5": pin}])["ok"]
    assert not au.controles(base, [{"md5": dict(pin, conn="x")}])["ok"]


@test("agregado_punta_a_punta", "carpeta plantada -> agregar_umb main: lee todo y escribe veredictos y lectura")
def t_agregado():
    with tempfile.TemporaryDirectory() as d:
        s_lif = list(range(100, 421))
        lif = os.path.join(d, "lif_real.json")
        json.dump({"corridas": {"real": {"S_LIF_idx": s_lif}}}, open(lif, "w"))
        pin = {"conn": au.MD5["conn"], "annot": au.MD5["annot"], "lif": au.MD5["lif"]}
        tasa = np.array(s_lif[:172] + list(range(1000, 1149)))
        umb = np.array(s_lif[:250] + list(range(2000, 2071)))
        json.dump({"md5": pin, "theta": 0.01, "activas": 321, "estado": "OK", "mn9_umb": 0.3, "rango_mn9": 7,
                   "J_tasa": 0.0}, open(os.path.join(d, "umb_real.json"), "w"))
        np.savez(os.path.join(d, "umb_real_top.npz"), UMB=umb, TASA=tasa)
        for tipo in ("SHUF_W", "SHUF_G"):
            for k0 in range(0, 40, 10):
                nul = {str(k): {"mn9": 0.0, "estado": "OK", "mn9_fijo": 0.0, "activas_fijo": 50, "theta": 0.001}
                       for k in range(k0, k0 + 10)}
                json.dump({"md5": pin, "tipo": tipo, "nulos": nul},
                          open(os.path.join(d, "umb_%s_k%03d.json" % (tipo, k0)), "w"))
                np.savez(os.path.join(d, "umb_%s_k%03d_top.npz" % (tipo, k0)),
                         **{"%s_%d" % (tipo, k): np.arange(5000, 5321) for k in range(k0, k0 + 10)})
        viejo = sys.argv
        sys.argv = ["agregar", "--dir", d, "--lif", lif]
        try:
            esperado_tasa = 172 / (642 - 172)
            au.J_TASA_049 = esperado_tasa
            au.MD5["lif"] = au.md5(lif)
            for p in [os.path.join(d, "umb_real.json")] + sorted(
                    os.path.join(d, x) for x in os.listdir(d) if x.startswith("umb_SHUF") and x.endswith(".json")):
                j = json.load(open(p))
                j["md5"]["lif"] = au.MD5["lif"]
                json.dump(j, open(p, "w"))
            au.main()
        finally:
            sys.argv = viejo
            au.J_TASA_049 = 0.3659574468085106
            au.MD5["lif"] = "f6383d18a0e05efb65696175949df9fa"
        log = open(os.path.join(d, "agregado_umb.log")).read()
        for linea in ("CONTROL PIN PASA", "CONTROL CALIB_REAL PASA", "CONTROL TASA_049 PASA",
                      "VEREDICTO H_UMB_MN9 SOSTENIDA", "VEREDICTO H_UMB_CONJUNTO SOSTENIDA",
                      "VEREDICTO H_UMB_GANA SOSTENIDA"):
            assert linea in log, linea
        e = json.load(open(os.path.join(d, "agregado_umb.json")))
        assert abs(e["J_umb"] - 250 / 392) < 1e-12 and abs(e["veredictos"]["GANA_d"] - (250 / 392 - 172 / 470)) < 1e-12


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--exigir", action="store_true")
    a = ap.parse_args()
    t_densa()
    t_sola()
    t_calib()
    t_humo()
    t_nulos()
    t_bandas()
    t_agregado()
    esperadas = ESPERADAS if a.exigir else len(OK)
    print("TESTS_OK %d de %d" % (len(OK), esperadas), flush=True)
    if len(OK) != esperadas:
        print("FALLA: faltan pruebas exigidas", flush=True)
        raise SystemExit(1)


if __name__ == "__main__":
    main()
