#!/usr/bin/env python3
"""Prueba del instrumento de H_LIF_SHUFG (respuesta 2026-10-14-055; sello SELLO-LIF-SHUFG-054.md, 307db84).

Grafos chicos y numeros plantados. Cada control del sello tiene que poder dar rojo: PIN (modelo, referencias y datos),
CTRL_REAL (26 de 30) y NULO_MISMO (un radio corrido 2e-6). Mas: el nulo es el de la 049, el parquet que lee Shiu es
el mismo grafo, el atajo a mano, las bandas con faltantes, la lectura de k32 y el extremo a extremo con un modelo
falso. Con --shiu y brian2, el model.py de Shiu corre en 12 neuronas (real, nulos y PIN integrado).
Uso: python3 prueba_lif_shufg.py [--shiu DIR_SHIU] [--exigir]
  --exigir  sin --shiu, brian2 o los JSON de referencia del repo, la prueba falla en vez de saltear (asi en Actions).
"""
import argparse
import copy
import json
import os
import sys
import tempfile

import numpy as np
import pandas as pd

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
sys.path.insert(0, AQUI)
import agregar_lif_shufg as ag  # noqa: E402
import lif_shufg as lg  # noqa: E402
import liq_entera as le  # noqa: E402

MD5_LIF_SHIU = "88c8459eb87ed328de9f65f38337f8b4"
MD5_LIQ = "ae3c1a2dd85a6faecfbfe76d71b0072f"
MD5_SELLO = "9e7e25f7f7e4ca8bbd031f6484eefe54"
REFS = ["results/mosca_entera_2026-10-15/actions_correr/liq_SHUF_G_k000.json",
        "results/mosca_entera_2026-10-15/actions_correr/liq_SHUF_G_k020.json"]
REF99 = "results/mosca_umbral_2026-10-16_humo/actions_humo/umb_SHUF_G_k099.json"
OK = []


def test(nombre, desc):
    def deco(f):
        def g(*a, **k):
            f(*a, **k)
            OK.append(nombre)
            print("TEST %s -> %s" % (nombre, desc), flush=True)
        return g
    return deco


def aborta(f, *a):
    try:
        f(*a)
    except SystemExit as e:
        return e.code
    return None


def grafo_chico(n=60, m=400, semilla=7):
    rng = np.random.default_rng(semilla)
    pre = rng.integers(0, n, m)
    post = rng.integers(0, n, m)
    w = rng.integers(1, 20, m).astype(np.int64) * rng.choice([-1, 1], m, p=[0.3, 0.7])
    return pre.astype(np.int64), post.astype(np.int64), w


def escribir_grafo(d, ids, pre, post, w, nombre="c.parquet"):
    df = pd.DataFrame({"Presynaptic_ID": ids[pre], "Postsynaptic_ID": ids[post], "Presynaptic_Index": pre,
                       "Postsynaptic_Index": post, "Connectivity": np.abs(w), "Excitatory": (w > 0).astype(int),
                       "Excitatory x Connectivity": w})
    df.to_parquet(os.path.join(d, nombre))
    pd.DataFrame({"Completed": [True] * len(ids)}, index=pd.Index(ids, name="")).to_csv(os.path.join(d, "k.csv"))
    return os.path.join(d, nombre), os.path.join(d, "k.csv")


def radio_049(n, pre, post, w, k):
    """El radio crudo como lo calculo la 049 en liq_entera.py: nulo() y matriz() sobre los arreglos en memoria."""
    _, q, _ = le.nulo(pre, post, np.asarray(w, dtype=np.float64), "SHUF_G", k)
    return le.matriz(n, pre, q, np.asarray(w, dtype=np.float64))[1]


@test("no_toca_lo_sellado", "lif_shiu.py y liq_entera.py con su md5, el sello con el suyo y las constantes del sello")
def t_sellado():
    assert le.md5(os.path.join(AQUI, "lif_shiu.py")) == MD5_LIF_SHIU
    assert le.md5(os.path.join(AQUI, "liq_entera.py")) == MD5_LIQ
    assert le.md5(os.path.join(AQUI, "SELLO-LIF-SHUFG-054.md")) == MD5_SELLO
    assert lg.TOL_RADIO == 1e-6 and lg.TIPO == "SHUF_G" and lg.R_POI_HZ == 100.0 and lg.BRIAN2 == "2.10.1"
    assert lg.MD5_COMP == "031a4b6eac490bda17c75b65ccaa7906" and lg.ls.BLOB_MODEL.startswith("5ba7083c")
    assert ag.LLEGA == 5 and ag.N_RUN_NULO == 10 and ag.N_RUN_REAL == 30 and ag.MIN_REAL == 27
    assert ag.DESBOCADO == 10 and ag.BANDA_REF == 5 and ag.KS == list(range(40)) and ag.FOCO == 32
    assert lg.MD5_REF["liq_SHUF_G_k000.json"].startswith("05bedf6f")
    assert lg.MD5_REF["liq_SHUF_G_k020.json"].startswith("62982026")
    assert lg.MD5_REF["umb_SHUF_G_k099.json"].startswith("dddfaeb2")


@test("nulo_es_el_de_la_049", "SHUF_G = nulo() de liq_entera.py con default_rng([20261015, 2, k]); conserva grados y pesos")
def t_nulo():
    pre, post, w = grafo_chico()
    n = 60
    for k in (0, 32, 99):
        p2, q2, w2 = lg.hacer_nulo(pre, post, w, k)
        p3, q3, w3 = le.nulo(pre, post, w, "SHUF_G", k)
        assert (p2 == p3).all() and (q2 == q3).all() and (w2 == w3).all()
        perm = np.random.default_rng([20261015, 2, k]).permutation(len(post))
        assert (q2 == post[perm]).all() and (p2 == pre).all() and (w2 == w).all()
        assert (np.bincount(q2, minlength=n) == np.bincount(post, minlength=n)).all()
        assert (np.bincount(p2, minlength=n) == np.bincount(pre, minlength=n)).all()
        assert not (q2 == post).all()


@test("ida_y_vuelta_parquet", "el parquet que se le pasa a Shiu releido da los mismos arreglos y tipos")
def t_parquet():
    pre, post, w = grafo_chico()
    with tempfile.TemporaryDirectory() as d:
        ruta = os.path.join(d, "g.parquet")
        lg.escribir_aristas(ruta, pre, post, w)
        p, q, x = lg.leer_aristas(ruta)
        assert (p == pre).all() and (q == post).all() and (x == w).all()
        assert p.dtype == pre.dtype and q.dtype == post.dtype and x.dtype == w.dtype


@test("radio_y_nulo_mismo", "radio() da el de la 049 y el exacto; NULO_MISMO pasa a 5e-7 y da rojo a 2e-6 y sin referencia")
def t_radio():
    pre, post, w = grafo_chico()
    n = 60
    for k in (0, 1, 2):
        _, q, _ = lg.hacer_nulo(pre, post, w, k)
        r = lg.radio(n, pre, q, w)
        r049 = radio_049(n, pre, post, w, k)
        dens = np.zeros((n, n))
        np.add.at(dens, (q, pre), w.astype(np.float64))
        exacto = np.abs(np.linalg.eigvals(dens)).max()
        assert abs(r - r049) / r049 < 1e-9 and abs(r - exacto) / exacto < 1e-8, (r, r049, exacto)
        assert lg.nulo_mismo(r, r049)["estado"] == "PASA"
        assert lg.nulo_mismo(r, r049 * (1 + 5e-7))["estado"] == "PASA"
        assert lg.nulo_mismo(r, r049 * (1 + 2e-6))["estado"] == "FALLA"
        assert lg.nulo_mismo(r, r049 * (1 - 2e-6))["estado"] == "FALLA"
    assert lg.nulo_mismo(1.0, None)["estado"] == "SIN_REF"
    ciclo = (np.array([0, 1, 2]), np.array([1, 2, 0]), np.array([50.0, 50.0, 50.0]))
    assert abs(lg.radio(6, *ciclo) - 50.0) < 1e-8


@test("atajo_a_mano", "n1, D1+ y D2+ en un grafo de 5 con multiarista y pesos negativos, contra la cuenta a mano")
def t_atajo():
    pre = np.array([0, 1, 0, 2, 1, 3, 0])
    post = np.array([4, 4, 2, 4, 3, 4, 4])
    w = np.array([3, -2, 5, 7, 4, -1, 2])
    at = lg.atajo(5, pre, post, w, [0, 1], 4)
    assert at["n1"] == 3 and at["D1+"] == 5.0 and at["D1+_matriz"] == 5.0, at
    assert at["D2+"] == 35.0, at
    at2 = lg.atajo(5, pre, post, w, [2], 4)
    assert at2["n1"] == 1 and at2["D1+"] == 7.0 and at2["D2+"] == 0.0, at2


@test("pin_rojo", "PIN aborta con 3: model.py ajeno, referencia ajena, parquet ajeno y Completeness ajeno")
def t_pin():
    with tempfile.TemporaryDirectory() as d:
        falso = os.path.join(d, "model.py")
        open(falso, "w").write("default_params = {}" + chr(10))
        assert aborta(lg.pin_modelo, falso) == 3
        r = os.path.join(d, "liq_SHUF_G_k000.json")
        json.dump({"nulos": {"0": {"radio_crudo": 1.0}}}, open(r, "w"))
        assert aborta(lg.pin_ref, [r], False) == 3
        ref, md5s = lg.pin_ref([r], True)
        assert ref == {0: 1.0}
        c = os.path.join(d, "c.parquet")
        k = os.path.join(d, "k.csv")
        open(c, "w").write("x")
        open(k, "w").write("y")
        assert aborta(lg.pin_datos, c, k, False) == 3
        assert lg.pin_datos(c, k, True)["conn"] == le.md5(c)


def fila(k, e, f, act, nm="PASA", n_run=10):
    return {"nulo_mismo": {"estado": nm, "radio_crudo": 1.0, "dif_rel": 0.0},
            "atajo": {"n1": 0, "D1+": 0.0, "D2+": 0.0},
            "corrida": {"ensayos_mn9": e, "tasa_mn9": f, "activas": act, "espigas": 10, "K": 5, "S_LIF_idx": [1, 2],
                        "n_run": n_run, "segundos": 1.0}}


def real_sint(e=30, f=61.6, act=393, n_run=30):
    return {"corrida": {"ensayos_mn9": e, "tasa_mn9": f, "activas": act, "espigas": 100, "K": 321,
                        "S_LIF_idx": [1, 2, 3], "n_run": n_run}, "atajo": {"n1": 1, "D1+": 9.0, "D2+": 3.0}}


@test("bandas_y_faltantes", "0 SOSTENIDA, 1 a 4 SIN_DECIDIR, 5 REFUTADA; un faltante que cambiaria la banda da NO_MEDIDO")
def t_bandas():
    assert ag.banda(0) == "SOSTENIDA" and ag.banda(1) == "SIN_DECIDIR" and ag.banda(4) == "SIN_DECIDIR"
    assert ag.banda(5) == "REFUTADA" and ag.banda(40) == "REFUTADA" and ag.banda(0, sost_ok=False) == "SIN_DECIDIR"
    assert ag.robusto(0, 0) == "SOSTENIDA" and ag.robusto(0, 1) == "NO_MEDIDO"
    assert ag.robusto(2, 2) == "SIN_DECIDIR" and ag.robusto(3, 2) == "NO_MEDIDO" and ag.robusto(5, 3) == "REFUTADA"
    ks = list(range(40))
    base = {k: fila(k, 0, 0.0, 50) for k in ks}
    for llegan, esperado in ((0, "SOSTENIDA"), (1, "SIN_DECIDIR"), (4, "SIN_DECIDIR"), (5, "REFUTADA")):
        nul = copy.deepcopy(base)
        for k in range(llegan):
            nul[k] = fila(k, 5, 1.0, 50)
        out, _ = ag.agregar(real_sint(), nul, [("x", True, "ok")], ks, 32, False)
        assert out["H_LIF_G_SHIU"] == esperado and out["H_LIF_G_VARA"] == "SOSTENIDA", (llegan, out["H_LIF_G_SHIU"])
    nul = copy.deepcopy(base)
    nul[3] = fila(3, 4, 61.6, 50)
    out, _ = ag.agregar(real_sint(), nul, [("x", True, "ok")], ks, 32, False)
    assert out["H_LIF_G_SHIU"] == "SOSTENIDA" and out["H_LIF_G_VARA"] == "SIN_DECIDIR" and out["ge_real"] == [3]
    nul = copy.deepcopy(base)
    del nul[7]
    nul[8] = fila(8, 9, 1.0, 50, nm="FALLA")
    out, _ = ag.agregar(real_sint(), nul, [("x", True, "ok")], ks, 32, False)
    assert out["faltan"] == 2 and out["H_LIF_G_SHIU"] == "NO_MEDIDO" and out["H_LIF_G_VARA"] == "NO_MEDIDO"
    nul = copy.deepcopy(base)
    nul[9] = fila(9, 10, 1.0, 50, n_run=9)
    out, _ = ag.agregar(real_sint(), nul, [("x", True, "ok")], ks, 32, False)
    assert out["faltan"] == 1 and out["nulos"]["9"]["estado"] == "NO_MEDIDO"


@test("ctrl_real_rojo", "CTRL_REAL: 27 de 30 pasa, 26 de 30 o 29 ensayos dan rojo y todo queda NO_MEDIDO")
def t_ctrl():
    ks = list(range(40))
    nul = {k: fila(k, 0, 0.0, 50) for k in ks}
    out, _ = ag.agregar(real_sint(e=27), nul, [("x", True, "ok")], ks, 32, False)
    assert out["CTRL_REAL"] == "PASA" and out["H_LIF_G_SHIU"] == "SOSTENIDA"
    for r in (real_sint(e=26), real_sint(e=29, n_run=29), None):
        out, _ = ag.agregar(r, nul, [("x", True, "ok")], ks, 32, False)
        assert out["CTRL_REAL"] == "FALLA", out["CTRL_REAL_motivo"]
        assert out["H_LIF_G_SHIU"] == out["H_LIF_G_VARA"] == out["H_LIF_K32"] == out["LECTURA_K32"] == "NO_MEDIDO"
    out, _ = ag.agregar(real_sint(e=2, n_run=2), nul, [("x", True, "ok")], ks, 32, True)
    assert out["CTRL_REAL"] == "PASA"
    out, _ = ag.agregar(real_sint(), nul, [("x", False, "md5")], ks, 32, False)
    assert out["PIN"] == "FALLA" and out["H_LIF_G_SHIU"] == "NO_MEDIDO"


@test("lectura_k32_y_desbocado", "los cuatro casos de la seccion 6, NO_MEDIDO sin k32 y desbocado a mas de 10 veces")
def t_k32():
    ks = list(range(40))
    casos = [(fila(32, 4, 9.0, 50), "NO_LLEGA", "NO_LLEGA"),
             (fila(32, 10, 99.0, 3931), "LLEGA_DESBOCADO", "LLEGA"),
             (fila(32, 10, 99.0, 3930), "LLEGA_IGUAL_O_MAS", "LLEGA"),
             (fila(32, 10, 61.6, 3930), "LLEGA_IGUAL_O_MAS", "LLEGA"),
             (fila(32, 5, 20.0, 400), "LLEGA_MENOS", "LLEGA")]
    for f32, lectura, h in casos:
        nul = {k: fila(k, 0, 0.0, 50) for k in ks}
        nul[32] = f32
        out, lineas = ag.agregar(real_sint(), nul, [("x", True, "ok")], ks, 32, False)
        assert out["LECTURA_K32"] == lectura and out["H_LIF_K32"] == h, (lectura, out["LECTURA_K32"])
        assert any(ag.TEXTO_K32[lectura] in s for s in lineas)
    nul = {k: fila(k, 0, 0.0, 50) for k in ks}
    del nul[32]
    out, _ = ag.agregar(real_sint(), nul, [("x", True, "ok")], ks, 32, False)
    assert out["H_LIF_K32"] == "NO_MEDIDO" and out["LECTURA_K32"] == "NO_MEDIDO"
    nul = {k: fila(k, 6, 0.0, 50) for k in ks}
    out, lineas = ag.agregar(real_sint(), nul, [("x", True, "ok")], ks, 32, False)
    assert out["H_LIF_G_SHIU"] == "REFUTADA" and any(ag.TEXTO_SHIU_REF in s for s in lineas)


class ShiuFalso:
    """Modelo falso para la prueba sin brian2: los estimulados disparan 100 veces por ensayo y cada neurona con
    entrada directa excitatoria de 10 o mas desde ellos, 5. Anota cada llamada."""

    def __init__(self):
        self.default_params = {"t_run": 1.0, "n_run": 30, "r_poi": 150.0}
        self.llamadas = []

    def run_exp(self, exp_name, neu_exc, path_res, path_comp, path_con, params, n_proc, force_overwrite):
        self.llamadas.append(exp_name)
        ids = pd.read_csv(path_comp, index_col=0).index.to_numpy()
        pos = {int(f): i for i, f in enumerate(ids)}
        df = pd.read_parquet(path_con)
        pre = df["Presynaptic_Index"].to_numpy()
        post = df["Postsynaptic_Index"].to_numpy()
        w = df["Excitatory x Connectivity"].to_numpy().astype(np.float64)
        est = np.zeros(len(ids), dtype=bool)
        est[[pos[int(f)] for f in neu_exc]] = True
        sel = est[pre] & (w > 0)
        d1 = np.bincount(post[sel], weights=w[sel], minlength=len(ids))
        filas = []
        for tr in range(params["n_run"]):
            for i in np.flatnonzero(est):
                filas += [(0.001 * j, tr, int(ids[i])) for j in range(100)]
            for i in np.flatnonzero((d1 >= 10) & ~est):
                filas += [(0.01 * j, tr, int(ids[i])) for j in range(5)]
        out = pd.DataFrame(filas, columns=["t", "trial", "flywire_id"])
        out["exp_name"] = exp_name
        out.to_parquet(os.path.join(path_res, exp_name + ".parquet"))


@test("extremo_a_extremo_falso", "real y 3 nulos con un modelo falso: el nulo con radio corrido no se simula, el agregado "
                                 "lee 2 de 3 y sin --sin-pin da PIN en rojo")
def t_e2e():
    pre, post, w = grafo_chico()
    ids = np.arange(3001, 3061, dtype=np.int64)
    pre = np.concatenate([pre, [0, 1]])
    post = np.concatenate([post, [10, 10]])
    w = np.concatenate([w, [20, 20]])
    with tempfile.TemporaryDirectory() as d:
        conn, comp = escribir_grafo(d, ids, pre, post, w)
        out = os.path.join(d, "out")
        refs = {str(k): {"radio_crudo": radio_049(60, pre, post, w, k) * (1.01 if k == 2 else 1.0)} for k in range(3)}
        rref = os.path.join(d, "liq_SHUF_G_k000.json")
        json.dump({"nulos": refs}, open(rref, "w"))
        estim = "3001,3002,3003,3004,3005"
        comun = ["--shiu", d, "--conn", conn, "--comp", comp, "--out", out, "--sin-pin", "--estim", estim,
                 "--leer", "3011"]
        falso = ShiuFalso()
        meta = {"model_blob": lg.ls.BLOB_MODEL, "brian2": "falso", "md5": {}, "ref": {}}
        a = lg.argumentos(comun + ["--modo", "real"])
        r = lg.correr(a, falso, 1.0, 0.001, meta)
        assert r["corrida"]["ensayos_mn9"] == 30 and r["corrida"]["n_run"] == 30 and r["atajo"]["n1"] >= 2
        a = lg.argumentos(comun + ["--modo", "nulos", "--k0", "0", "--n", "3", "--ref", rref])
        ref, _ = lg.pin_ref(a.ref, True)
        meta["ref"] = ref
        res = lg.correr(a, falso, 1.0, 0.001, meta)
        assert falso.llamadas == ["real", "SHUF_G_0", "SHUF_G_1"], falso.llamadas
        assert res["nulos"]["2"]["corrida"] is None and res["nulos"]["2"]["nulo_mismo"]["estado"] == "FALLA"
        for k in ("0", "1"):
            v = res["nulos"][k]
            assert v["nulo_mismo"]["estado"] == "PASA" and v["corrida"]["n_run"] == 10
            assert (v["corrida"]["ensayos_mn9"] == 10) == (v["atajo"]["D1+"] >= 10), v
        assert sorted(os.listdir(out)) == ["SHUF_G_0.parquet", "SHUF_G_1.parquet", "lif_shufg_G_k000.json",
                                           "lif_shufg_real.json", "real.parquet"], sorted(os.listdir(out))
        o = ag.main(["--dir", out, "--ks", "0,1,2", "--foco", "1", "--sin-pin"])
        assert o["PIN"] == "PASA" and o["CTRL_REAL"] == "PASA" and o["medidos"] == 2 and o["faltan"] == 1
        llegan = [k for k in (0, 1) if res["nulos"][str(k)]["atajo"]["D1+"] >= 10]
        assert o["llegan"] == llegan, (o["llegan"], llegan)
        assert o["H_LIF_K32"] == ("LLEGA" if 1 in llegan else "NO_LLEGA")
        assert os.path.exists(os.path.join(out, "agregado_lif_shufg.json"))
        o2 = ag.main(["--dir", out, "--ks", "0,1,2", "--foco", "1"])
        assert o2["PIN"] == "FALLA" and o2["H_LIF_G_SHIU"] == "NO_MEDIDO"


@test("referencias_del_sello", "los JSON de referencia del repo tienen el md5 del sello: k 0 a 39 (k32 = 372,813...) y k 99")
def t_refs():
    ref, _ = lg.pin_ref([os.path.join(RAIZ, r) for r in REFS], False)
    assert sorted(ref) == list(range(40)) and abs(ref[32] - 372.81323741506026) < 1e-9, ref.get(32)
    ref99, _ = lg.pin_ref([os.path.join(RAIZ, REF99)], False)
    assert list(ref99) == [99] and abs(ref99[99] - 319.61856064512546) < 1e-9


@test("lif_shiu_grafo_chico", "el model.py de Shiu corre en 12 neuronas: real, un nulo medido, uno con radio corrido sin "
                              "simular y el PIN integrado en rojo")
def t_lif(shiu):
    ids = np.arange(2001, 2013, dtype=np.int64)
    ar = [(0, 2, 400), (1, 2, 400), (2, 3, 400), (5, 6, 50), (6, 7, 50), (7, 5, 50), (8, 9, -30), (9, 8, 20),
          (10, 11, 5), (11, 10, 5)]
    pre = np.array([x for x, _, _ in ar], dtype=np.int64)
    post = np.array([y for _, y, _ in ar], dtype=np.int64)
    w = np.array([c for _, _, c in ar], dtype=np.int64)
    with tempfile.TemporaryDirectory() as d:
        conn, comp = escribir_grafo(d, ids, pre, post, w)
        out = os.path.join(d, "out")
        rref = os.path.join(d, "liq_SHUF_G_k000.json")
        json.dump({"nulos": {"0": {"radio_crudo": radio_049(12, pre, post, w, 0)},
                             "1": {"radio_crudo": radio_049(12, pre, post, w, 1) * 1.01}}}, open(rref, "w"))
        comun = ["--shiu", shiu, "--conn", conn, "--comp", comp, "--out", out, "--n-run", "2", "--t-run-ms", "200",
                 "--n-proc", "1", "--estim", "2001,2002", "--leer", "2004"]
        r = lg.main(comun + ["--modo", "real", "--sin-pin"])
        c = r["corrida"]
        assert c["ensayos_mn9"] == 2 and 2003 in c["S_LIF_ids"] and 2004 in c["S_LIF_ids"], c
        assert 2005 not in c["S_LIF_ids"] and 2001 not in c["S_LIF_ids"] and r["brian2"] == "2.10.1", c
        res = lg.main(comun + ["--modo", "nulos", "--k0", "0", "--n", "2", "--ref", rref, "--sin-pin"])
        assert res["nulos"]["0"]["nulo_mismo"]["estado"] == "PASA" and res["nulos"]["0"]["corrida"]["n_run"] == 2
        assert res["nulos"]["1"]["nulo_mismo"]["estado"] == "FALLA" and res["nulos"]["1"]["corrida"] is None
        assert aborta(lg.main, comun + ["--modo", "real"]) == 3


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--shiu", default="")
    ap.add_argument("--exigir", action="store_true")
    a = ap.parse_args()
    t_sellado()
    t_nulo()
    t_parquet()
    t_radio()
    t_atajo()
    t_pin()
    t_bandas()
    t_ctrl()
    t_k32()
    t_e2e()
    if all(os.path.exists(os.path.join(RAIZ, r)) for r in REFS + [REF99]):
        t_refs()
    else:
        print("SALTEADA referencias_del_sello (faltan los JSON de la 049 y la 051 en el repo)", flush=True)
    try:
        import brian2  # noqa: F401
        hay_brian2 = True
    except ImportError:
        hay_brian2 = False
    if a.shiu and hay_brian2:
        t_lif(a.shiu)
    else:
        print("SALTEADA lif_shiu_grafo_chico (shiu=%s brian2=%s)" % (bool(a.shiu), hay_brian2), flush=True)
    esperadas = 12 if a.exigir else len(OK)
    print("TESTS_OK %d de %d" % (len(OK), esperadas), flush=True)
    if len(OK) != esperadas:
        print("FALLA: faltan pruebas exigidas", flush=True)
        raise SystemExit(1)


if __name__ == "__main__":
    main()
