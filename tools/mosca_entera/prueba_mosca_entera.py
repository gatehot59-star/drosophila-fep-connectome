#!/usr/bin/env python3
"""Prueba del instrumento de H_MOSCA_ENTERA (respuesta 2026-10-14-047). Grafos chicos, numeros plantados.

Uso: python3 prueba_mosca_entera.py [--ref DIR_8d305e9] [--shiu DIR_SHIU] [--exigir]
  --ref    worktree de titan/lector-2026-10-15 en 8d305e9: compara simular(), matriz() y tau_por_root() contra el
           factorial2_mosca.py sellado (md5 798a824cd47808155fa12adb9e652dac).
  --shiu   carpeta con el model.py de Shiu en 91bdd1e7: corre el LIF en un grafo de 10 neuronas.
  --exigir sin --ref o --shiu la prueba falla en vez de saltear (asi corre en Actions).
"""
import argparse
import hashlib
import json
import os
import sys
import tempfile

import numpy as np
import pandas as pd
import scipy.sparse as sp

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import agregar_mosca_entera as ag  # noqa: E402
import liq_entera as le  # noqa: E402

MD5_F2 = "798a824cd47808155fa12adb9e652dac"
OK = []


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


@test("celda_igual_factorial2", "simular(), matriz() y tau_por_root() == factorial2_mosca.py sellado (liq y tasa)")
def t_celda(ref):
    f2p = os.path.join(ref, "tools", "factorial2", "factorial2_mosca.py")
    assert hashlib.md5(open(f2p, "rb").read()).hexdigest() == MD5_F2, "factorial2_mosca.py no es el sellado"
    sys.path.insert(0, os.path.dirname(f2p))
    import factorial2_mosca as f2
    n, n_ent = 60, 5
    pre, post, w = grafo_chico(n)
    W1, r1 = le.matriz(n, pre, post, w)
    W2, r2 = f2.matriz(n, (pre, post, w), densa_ok=False)
    # eigs arranca de un vector al azar (ARPACK, sin v0) en las dos: el radio coincide a ~1e-11 relativo, no al bit
    assert abs(r1 - r2) <= 1e-8 * abs(r2) and abs(W1 - W2).max() <= 1e-8 * abs(W2).max(), (r1, r2)
    r_densa = float(np.abs(np.linalg.eigvals(sp.coo_matrix((w, (post, pre)), shape=(n, n)).toarray())).max())
    assert abs(r1 - r_densa) <= 1e-8 * r_densa, (r1, r_densa)
    ids = np.arange(720575940600000000, 720575940600000000 + n)
    tau1, tau2 = le.tau_por_root(ids, 30), f2.tau_por_root(ids, 30)
    assert np.array_equal(tau1, tau2)
    assert f2.base.DT == le.DT and f2.base.RHO == le.RHO and f2.G_LIQ == le.G_LIQ
    T = f2.tm.T
    d = {"y": np.zeros(1), "drive": np.full((1, T, 1), le.AMPLITUD), "ruido": np.zeros((1, T, n_ent))}
    chan = np.zeros(n_ent, dtype=int)
    for liq in (True, False):
        ref_out = f2.sim(W1, tau1, n_ent, chan, d, liq)[0]
        _, tray = le.simular(W1, tau1, np.arange(n_ent), liq, T=T, ventana=(0, T), registrar=np.arange(n - 6, n))
        dif = float(np.abs(ref_out - tray).max())
        assert dif <= 1e-12, "liq=%s dif=%g" % (liq, dif)
        assert float(np.abs(tray).max()) > 1e-3, "la senal no llega a las 6 ultimas: la prueba no prueba nada"
    _, ta = le.simular(W1, tau1, np.arange(n_ent), True, T=T, ventana=(0, T), registrar=np.arange(n))
    _, tb = le.simular(W1, tau1, np.arange(n_ent), False, T=T, ventana=(0, T), registrar=np.arange(n))
    assert float(np.abs(ta - tb).max()) > 1e-3, "LIQ y TASA dan lo mismo: los brazos serian la misma funcion"


@test("nulos_conservan_lo_que_dicen", "SHUF_W conserva topologia y pesos; SHUF_G conserva grados y pesos por arista; difieren")
def t_nulos():
    pre, post, w = grafo_chico()
    p1, q1, w1 = le.nulo(pre, post, w, "SHUF_W", 0)
    assert np.array_equal(p1, pre) and np.array_equal(q1, post) and np.array_equal(np.sort(w1), np.sort(w))
    assert not np.array_equal(w1, w)
    p2, q2, w2 = le.nulo(pre, post, w, "SHUF_G", 0)
    assert np.array_equal(p2, pre) and np.array_equal(w2, w) and not np.array_equal(q2, post)
    assert np.array_equal(np.bincount(q2, minlength=60), np.bincount(post, minlength=60))
    a, b, c = le.nulo(pre, post, w, "SHUF_W", 0)
    assert np.array_equal(c, w1), "no es determinista"
    assert not np.array_equal(le.nulo(pre, post, w, "SHUF_W", 1)[2], w1), "semillas distintas dan lo mismo"
    W0, _ = le.matriz(60, pre, post, w)
    Wa, _ = le.matriz(60, p1, q1, w1)
    Wb, _ = le.matriz(60, p2, q2, w2)
    assert abs(Wa - Wb).max() > 0 and abs(Wa - W0).max() > 0, "los nulos no cambian la matriz"


@test("prox_a_mano", "PROX en una cadena 0->1->2->3->4 == cuenta a mano")
def t_prox():
    w = {(1, 0): 0.5, (2, 1): -0.4, (3, 2): 0.3, (4, 3): 0.2}
    W = sp.csr_matrix((list(w.values()), ([k[0] for k in w], [k[1] for k in w])), shape=(5, 5))
    s = le.prox(W, np.array([0]))
    esp = [0.0, 0.5 * 0.5, 0.25 * 0.5 * 0.4, 0.125 * 0.5 * 0.4 * 0.3, 0.0625 * 0.5 * 0.4 * 0.3 * 0.2]
    assert np.allclose(s, esp, rtol=0, atol=1e-15), s


@test("top_y_jaccard", "top_positivos excluye estimuladas y no positivos, empates por indice; Jaccard a mano")
def t_top():
    r = np.array([5.0, -1.0, 3.0, 0.0, 3.0, 2.0])
    assert le.top_positivos(r, np.array([0]), 3).tolist() == [2, 4, 5]
    assert le.top_positivos(r, np.array([0]), 2).tolist() == [2, 4]
    assert le.top_positivos(r, np.array([0, 2, 4, 5]), 3).tolist() == []
    assert ag.jaccard([1, 2, 3], [2, 3, 4]) == 0.5 and ag.jaccard([1], [2]) == 0.0


@test("bandas_del_sello", "REPRO_SHIU, K_SANO, MN9, CONJUNTO, RIVAL y LIQ con numeros plantados dan lo que dice el sello")
def t_bandas():
    sh = lambda e: {"ensayos_mn9": e, "n_run": 10}
    real = {"ensayos_mn9": 27, "n_run": 30}
    assert ag.repro_shiu(real, [sh(5)] * 2 + [sh(4)] * 18)[0] == "PASA"
    assert ag.repro_shiu(real, [sh(5)] * 3 + [sh(4)] * 17)[0] == "FALLA"
    assert ag.repro_shiu({"ensayos_mn9": 26, "n_run": 30}, [sh(0)] * 20)[0] == "FALLA"
    assert ag.repro_shiu(real, [sh(0)] * 19)[0] == "INCOMPLETO"
    n40 = lambda v: {"SHUF_W": [v] * 40, "SHUF_G": [v] * 40}
    jl = {s: 0.5 for s in range(30, 40)}
    jt = {s: 0.47 for s in range(30, 40)}
    v = ag.veredictos("PASA", 100, 1.0, n40(0.5), 0.6, n40(0.2), 0.5, jl, jt)
    assert (v["MN9"], v["CONJUNTO"], v["RIVAL"], v["LIQ"]) == ("SOSTENIDA", "SOSTENIDA", "SOSTENIDA", "SOSTENIDA"), v
    uno = {"SHUF_W": [1.0] + [0.5] * 39, "SHUF_G": [0.5] * 40}
    assert ag.veredictos("PASA", 100, 1.0, uno, 0.6, n40(0.2), 0.6, jl, jl)["MN9"] == "SIN_DECIDIR"
    cinco = {"SHUF_W": [0.5] * 40, "SHUF_G": [2.0] * 5 + [0.5] * 35}
    assert ag.veredictos("PASA", 100, 1.0, cinco, 0.6, n40(0.2), 0.6, jl, jl)["MN9"] == "REFUTADA"
    assert ag.veredictos("PASA", 100, 0.0, n40(-1.0), 0.6, n40(0.2), 0.6, jl, jl)["MN9"] == "REFUTADA"
    corto = {"SHUF_W": [0.5] * 39, "SHUF_G": [0.5] * 40}
    assert ag.veredictos("PASA", 100, 1.0, corto, 0.6, n40(0.2), 0.6, jl, jl)["MN9"] == "INCOMPLETO"
    v = ag.veredictos("PASA", 100, 1.0, n40(0.5), 0.6, n40(0.2), 0.6, jl, jl)
    assert v["RIVAL"] == "REFUTADA" and v["LIQ"] == "REFUTADA", v
    v = ag.veredictos("PASA", 100, 1.0, n40(0.5), 0.6, n40(0.2), 0.57, {s: 0.51 for s in range(30, 40)}, jl)
    assert v["RIVAL"] == "SIN_DECIDIR" and v["LIQ"] == "SIN_DECIDIR", v
    v = ag.veredictos("PASA", 100, 1.0, n40(0.5), 0.6, n40(0.2), 0.5, {s: 0.5 for s in range(30, 39)}, jt)
    assert v["LIQ"] == "INCOMPLETO", v
    v = ag.veredictos("FALLA", 100, 1.0, n40(0.5), 0.6, n40(0.2), 0.5, jl, jt)
    assert all(v[h] == "NO_MEDIDO" for h in ("MN9", "CONJUNTO", "RIVAL", "LIQ")), v
    v = ag.veredictos("PASA", 5, 1.0, n40(0.5), 0.6, n40(0.2), 0.5, jl, jt)
    assert v["MN9"] == "SOSTENIDA" and all(v[h] == "NO_MEDIDO" for h in ("CONJUNTO", "RIVAL", "LIQ")), v


@test("lectura_y_mapeo", "leer_grafo lee el parquet y el Completeness de Shiu; un id cambiado pone el mapeo en rojo")
def t_lectura():
    with tempfile.TemporaryDirectory() as d:
        n = 60
        pre, post, w = grafo_chico(n)
        ids = np.arange(720575940600000000, 720575940600000000 + n)
        df = pd.DataFrame({"Presynaptic_ID": ids[pre], "Postsynaptic_ID": ids[post], "Presynaptic_Index": pre,
                           "Postsynaptic_Index": post, "Connectivity": np.abs(w).astype(int),
                           "Excitatory": np.sign(w).astype(int), "Excitatory x Connectivity": w.astype(int)})
        df.to_parquet(os.path.join(d, "c.parquet"))
        pd.DataFrame({"Completed": [True] * n}, index=pd.Index(ids, name="")).to_csv(os.path.join(d, "k.csv"))
        p2, q2, w2, ids2, ok = le.leer_grafo(os.path.join(d, "c.parquet"), os.path.join(d, "k.csv"))
        assert ok and np.array_equal(p2, pre) and np.array_equal(w2, w) and np.array_equal(ids2, ids)
        mal = ids.copy()
        mal[[int(pre[0]), int(post[0])]] = mal[[int(post[0]), int(pre[0])]] if pre[0] != post[0] else mal[[0, 1]]
        pd.DataFrame({"Completed": [True] * n}, index=pd.Index(mal, name="")).to_csv(os.path.join(d, "k2.csv"))
        assert not le.leer_grafo(os.path.join(d, "c.parquet"), os.path.join(d, "k2.csv"))[4]


@test("agregado_extremo_a_extremo", "carpeta plantada -> agregar_mosca_entera main: lee todo y escribe los veredictos")
def t_agregado():
    with tempfile.TemporaryDirectory() as d:
        s_lif = list(range(100, 200))
        json.dump({"corridas": {"real": {"ensayos_mn9": 30, "n_run": 30, "tasa_mn9": 12.0, "K": 100,
                                         "S_LIF_idx": s_lif}}}, open(os.path.join(d, "lif_real.json"), "w"))
        for j in range(2):
            json.dump({"corridas": {"SHUF_W_%d" % (10 * j + i): {"ensayos_mn9": 0, "n_run": 10} for i in range(10)}},
                      open(os.path.join(d, "lif_shufW_k%03d.json" % (10 * j)), "w"))
        tops = {"PROX": np.arange(150, 300)}
        liq = {"LIQ": {}, "TASA": {}, "PROX": {"mn9": 0.1}}
        for s in range(30, 40):
            tops["LIQ_%d" % s] = np.arange(110, 400)
            tops["TASA_%d" % s] = np.arange(120, 400)
            liq["LIQ"][str(s)] = {"mn9": 0.3}
            liq["TASA"][str(s)] = {"mn9": 0.2}
        json.dump(liq, open(os.path.join(d, "liq_real.json"), "w"))
        np.savez(os.path.join(d, "liq_real_top.npz"), **tops)
        for tipo in ("SHUF_W", "SHUF_G"):
            for k0 in range(0, 40, 10):
                nul = {str(k): {"mn9": 0.01} for k in range(k0, k0 + 10)}
                json.dump({"tipo": tipo, "nulos": nul}, open(os.path.join(d, "liq_%s_k%03d.json" % (tipo, k0)), "w"))
                np.savez(os.path.join(d, "liq_%s_k%03d_top.npz" % (tipo, k0)),
                         **{"%s_%d" % (tipo, k): np.arange(1000, 1100) for k in range(k0, k0 + 10)})
        viejo = sys.argv
        sys.argv = ["agregar", "--dir", d]
        try:
            ag.main()
        finally:
            sys.argv = viejo
        v = json.load(open(os.path.join(d, "agregado.json")))["veredictos"]
        assert v["REPRO_SHIU"] == "PASA" and v["MN9"] == "SOSTENIDA" and v["CONJUNTO"] == "SOSTENIDA", v
        assert abs(v["RIVAL_d"] - (90 / 110 - 50 / 150)) < 1e-12 and v["RIVAL"] == "SOSTENIDA", v
        assert abs(v["LIQ_mediana"] - (90 / 110 - 80 / 120)) < 1e-12 and v["LIQ"] == "SOSTENIDA", v
        assert "VEREDICTO MN9 SOSTENIDA" in open(os.path.join(d, "agregado.log")).read()


@test("lif_shiu_grafo_chico", "el model.py de Shiu corre en 10 neuronas: la cadena estimulada dispara, la aislada no")
def t_lif(shiu):
    import lif_shiu as ls
    with tempfile.TemporaryDirectory() as d:
        ids = np.arange(1001, 1011)
        ar = [(0, 2, 400), (1, 2, 400), (2, 3, 400)]
        df = pd.DataFrame({"Presynaptic_ID": [ids[a] for a, _, _ in ar], "Postsynaptic_ID": [ids[b] for _, b, _ in ar],
                           "Presynaptic_Index": [a for a, _, _ in ar], "Postsynaptic_Index": [b for _, b, _ in ar],
                           "Connectivity": [c for _, _, c in ar], "Excitatory": [1] * 3,
                           "Excitatory x Connectivity": [c for _, _, c in ar]})
        df.to_parquet(os.path.join(d, "c.parquet"))
        pd.DataFrame({"Completed": [True] * 10}, index=pd.Index(ids, name="")).to_csv(os.path.join(d, "k.csv"))
        out = os.path.join(d, "out")
        viejo = sys.argv
        base = ["lif", "--shiu", shiu, "--conn", os.path.join(d, "c.parquet"), "--comp", os.path.join(d, "k.csv"),
                "--out", out, "--n-run", "2", "--t-run-ms", "200", "--n-proc", "1", "--sin-pin",
                "--estim", "1001,1002", "--leer", "1004"]
        try:
            sys.argv = base + ["--modo", "real"]
            ls.main()
            sys.argv = base + ["--modo", "shuf", "--k0", "0", "--n", "1"]
            ls.main()
        finally:
            sys.argv = viejo
        r = json.load(open(os.path.join(out, "lif_real.json")))["corridas"]["real"]
        assert r["ensayos_mn9"] == 2 and 1003 in r["S_LIF_ids"] and 1004 in r["S_LIF_ids"], r
        assert 1005 not in r["S_LIF_ids"] and 1001 not in r["S_LIF_ids"], r
        s = json.load(open(os.path.join(out, "lif_shufW_k000.json")))["corridas"]["SHUF_W_0"]
        assert s["n_run"] == 2, s


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ref", default="")
    ap.add_argument("--shiu", default="")
    ap.add_argument("--exigir", action="store_true")
    a = ap.parse_args()
    t_nulos()
    t_prox()
    t_top()
    t_bandas()
    t_lectura()
    t_agregado()
    if a.ref:
        t_celda(a.ref)
    else:
        print("SALTEADA celda_igual_factorial2 (sin --ref)", flush=True)
    try:
        import brian2  # noqa: F401
        hay_brian2 = True
    except ImportError:
        hay_brian2 = False
    if a.shiu and hay_brian2:
        t_lif(a.shiu)
    else:
        print("SALTEADA lif_shiu_grafo_chico (shiu=%s brian2=%s)" % (bool(a.shiu), hay_brian2), flush=True)
    esperadas = 8 if a.exigir else len(OK)
    print("TESTS_OK %d de %d" % (len(OK), esperadas), flush=True)
    if len(OK) != esperadas:
        print("FALLA: faltan pruebas exigidas", flush=True)
        raise SystemExit(1)


if __name__ == "__main__":
    main()
