#!/usr/bin/env python3
"""Nulos SL y T de R2 para el factorial 3 de la mosca (respuesta 2026-10-13-008). Sellado antes de correr.

Pregunta. En el factorial 2 (2026-10-13-007) R2 (33.489 neuronas) le gano a la regla con sus mismos sensores por
+1,28 puntos (IC [+0,79; +1,77]) con 3 x 5 semillas. Falta saber si eso es del cableado real o de cualquier red de ese
tamano: este script mide R2 contra sus barajados, en la celda de nulos del factorial 1 (A 0,3, ruido 0,15), con la
semilla de tau 0 y la de prueba 2 (las mismas del trabajo t0c2 de la grilla).
  SL: permuta los destinos entre aristas del mismo bloque (lado pre, lado post), como base.barajar_sl: conserva el
      grado de entrada y de salida de cada neurona, el lado de cada arista y su peso. Semilla default_rng([7, k]).
  T:  permuta los tipos sintonizados entre las entradas de cada lado (como en el factorial 1), con el cableado real.
      Semilla default_rng([11, k]).
Cada nulo k tiene su propia semilla, asi que repartir los k entre trabajos no cambia ningun numero.
La simulacion, el lector y los datos son los de tools/factorial2/factorial2_mosca.py (sellado en 9442fdf, md5
798a824c), importado sin cambios.
Controles: pin de md5 (insumos, modulo 015 y factorial2_mosca.py); R2_tamano; SL_IGUAL_MODULO (en R1, la version
numpy da exactamente lo mismo que base.barajar_sl con la misma semilla); por nulo SL, grados de entrada y salida
iguales, lado de cada arista igual y al menos un destino cambiado; por nulo T, la cuenta de tipos por lado igual y al
menos un tipo cambiado. Con --real (lo corren los trabajos que empiezan en k = 0) mide tambien el cableado real con
el mismo camino, para que el agregador lo compare con la grilla (REAL_IGUAL).
Salida: 0 completo; 2 insumos distintos del pin; 3 control fallido.
"""
import argparse
import json
import os
import platform
import sys
import time

import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(AQUI, "..", "factorial2"))
import factorial2_mosca as f2  # noqa: E402  sellado en 9442fdf, sin cambios

tm, base = f2.tm, f2.base
MD5_F2 = "798a824cd47808155fa12adb9e652dac"
CELDA, TAU, PRUEBA = (0.3, 0.15), 0, 2
SEM_SL, SEM_T = 7, 11


def pr(s):
    print(s, flush=True)


def codigos(lados):
    m = {"L": 0, "R": 1, "C": 2}
    return np.array([m.get(x, 3) for x in lados], dtype=np.int64)


def barajar_sl_np(p, q, lc, rng):
    """Lo mismo que base.barajar_sl sobre arreglos: bloques en orden de primera aparicion, aristas en orden."""
    clave = lc[p] * 4 + lc[q]
    uniq, primero = np.unique(clave, return_index=True)
    qn = q.copy()
    for b in uniq[np.argsort(primero)]:
        ks = np.flatnonzero(clave == b)
        perm = rng.permutation(len(ks))
        qn[ks] = q[ks][perm]
    return qn


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--conn", required=True)
    ap.add_argument("--annot", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--tipo", required=True, choices=("SL", "T"))
    ap.add_argument("--k0", type=int, required=True)
    ap.add_argument("--n", type=int, required=True)
    ap.add_argument("--real", action="store_true", help="medir tambien el cableado real por el mismo camino")
    ap.add_argument("--humo", action="store_true", help="corrida corta de humo: numeros sin valor")
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    t_ini = time.time()
    pr("# maquina: %s | %s | Python %s | numpy %s" % (platform.node(), platform.platform(), platform.python_version(),
                                                      np.__version__))
    pr("# md5 script = " + base.md5(os.path.abspath(__file__)))
    m2, mt = base.md5(os.path.abspath(f2.__file__)), base.md5(os.path.abspath(tm.__file__))
    mc, ma = base.md5(a.conn), base.md5(a.annot)
    pr("# md5 factorial2_mosca = %s | md5 modulo 015 = %s | md5 conn = %s | md5 annot = %s" % (m2, mt, mc, ma))
    if mc != base.MD5_CONN or ma != base.MD5_ANNOT or mt != f2.MD5_TM or m2 != MD5_F2:
        pr("ABORTA: insumos distintos del pin")
        pr("EXIT_RUN=2")
        return 2
    humo = a.humo
    if humo:
        pr("# HUMO: corrida corta, estos numeros no valen")
    n_train, n_test = (120, 80) if humo else (tm.N_TRAIN, tm.N_TEST)
    ks = list(range(a.k0, a.k0 + a.n))
    pr("# nulos tipo=%s k=%s celda=%s tau=%d prueba=%d real=%s" % (a.tipo, ks, CELDA, TAU, PRUEBA, a.real))
    guardas = {}

    # control del barajado contra el modulo, en R1
    S1 = f2.sujeto(a.conn, a.annot, "R1", "CON")
    p1, q1, w1 = S1["aristas"]
    lc1 = codigos(S1["lados"])
    ar1 = list(zip(p1.tolist(), q1.tolist(), w1.tolist()))
    ref = base.barajar_sl(ar1, S1["lados"], np.random.default_rng([SEM_SL, 0]))
    mio = barajar_sl_np(p1, q1, lc1, np.random.default_rng([SEM_SL, 0]))
    guardas["SL_IGUAL_MODULO"] = bool(np.array_equal(np.array([x[1] for x in ref]), mio) and
                                      np.array_equal(np.array([x[0] for x in ref]), p1))
    pr("CHEQUEO SL_IGUAL_MODULO (R1, %d aristas, semilla [%d, 0]) -> %s" % (len(p1), SEM_SL, guardas["SL_IGUAL_MODULO"]))
    del S1, ar1, ref

    S = f2.sujeto(a.conn, a.annot, "R2", "CON")
    ids, tipos, lados = S["ids"], S["tipos"], S["lados"]
    n, n_ent = len(ids), S["n_ent"]
    p, q, w = S["aristas"]
    guardas["R2_tamano"] = bool((S["n_U"], S["n_ar_crudo"]) == f2.R2_ESPERADO and S["contiene_m46"] and S["contiene_r1"])
    pr("SUJETO R2 neuronas=%d aristas=%d entradas=%d -> %s" % (S["n_U"], S["n_ar_crudo"], n_ent, guardas["R2_tamano"]))
    lc = codigos(lados)
    tau = f2.tau_por_root(ids, TAU)
    etr = tm.generar(n_train, f2.SEM_GEN_TR)
    ytr, vtr = etr["y"], etr["vuelo"]
    Ztr = f2.ruido_por_root(ids[:n_ent], n_train, f2.SEM_RUIDO_TR)
    ete = tm.generar(n_test, PRUEBA)
    yte, vte = ete["y"], ete["vuelo"]
    Zte = f2.ruido_por_root(ids[:n_ent], n_test, 1000 + PRUEBA)
    A, s = CELDA
    dtr = dict(y=ytr, drive=tm.sintonias(etr, A), ruido=s * Ztr)
    dte = dict(y=yte, drive=tm.sintonias(ete, A), ruido=s * Zte)

    def chan_de(tp):
        return np.array([(0 if lados[i] == "L" else 1) * tm.NT + tm.TIPOS.index(tp[i]) for i in range(n_ent)])

    def acierto(W, ch):
        th = tm.umbrales(tm.lineas(f2.sim_trozos(W, tau, n_ent, ch, dtr, False)), ytr, vtr)
        pW = tm.carrera(tm.lineas(f2.sim_trozos(W, tau, n_ent, ch, dte, False)), th, vte)
        return float((pW == yte).mean())

    chan_real = chan_de(tipos[:n_ent])
    W_real = None
    if a.real or a.tipo == "T":
        W_real, r_real = f2.matriz(n, (p, q, w), densa_ok=False)
        pr("RADIO real crudo=%.6f" % r_real)
    res = dict(tipo=a.tipo, ks=ks, celda="%.1f|%.2f" % CELDA, tau=TAU, prueba=PRUEBA, humo=humo, nulos=[],
               real=None, n_ent=n_ent)
    if a.real:
        tc = time.time()
        res["real"] = acierto(W_real, chan_real)
        pr("REAL W=%.4f | %.1f s" % (res["real"], time.time() - tc))
    gi0, go0 = np.bincount(q, minlength=n), np.bincount(p, minlength=n)
    ok_nulos = True
    for k in ks:
        tc = time.time()
        if a.tipo == "SL":
            qn = barajar_sl_np(p, q, lc, np.random.default_rng([SEM_SL, k]))
            g = bool(np.array_equal(np.bincount(qn, minlength=n), gi0) and np.array_equal(np.bincount(p, minlength=n), go0)
                     and np.array_equal(lc[qn], lc[q]) and int((qn != q).sum()) > 0)
            Wk, rk = f2.matriz(n, (p, qn, w), densa_ok=False)
            ak = acierto(Wk, chan_real)
            res["nulos"].append(dict(k=k, acierto=ak, radio_crudo=rk, destinos_cambiados=int((qn != q).sum()), guarda=g))
            pr("NULO SL k=%d acierto=%.4f radio=%.4f destinos_cambiados=%d guarda=%s | %.1f s" % (
                k, ak, rk, int((qn != q).sum()), g, time.time() - tc))
            del Wk
        else:
            rng = np.random.default_rng([SEM_T, k])
            tp = list(tipos[:n_ent])
            for ld in ("L", "R"):
                ix = [i for i in range(n_ent) if lados[i] == ld]
                vals = [tp[i] for i in ix]
                for i, j in zip(ix, rng.permutation(len(ix))):
                    tp[i] = vals[j]
            g = bool(tp != list(tipos[:n_ent]) and all(
                sorted(tp[i] for i in range(n_ent) if lados[i] == ld) ==
                sorted(tipos[i] for i in range(n_ent) if lados[i] == ld) for ld in ("L", "R")))
            ak = acierto(W_real, chan_de(tp))
            cambiados = sum(1 for i in range(n_ent) if tp[i] != tipos[i])
            res["nulos"].append(dict(k=k, acierto=ak, tipos_cambiados=cambiados, guarda=g))
            pr("NULO T k=%d acierto=%.4f tipos_cambiados=%d guarda=%s | %.1f s" % (k, ak, cambiados, g, time.time() - tc))
        ok_nulos &= g
    guardas["nulos_%s" % a.tipo] = bool(ok_nulos)
    valido = all(guardas.values())
    res["guardas"], res["valido"] = guardas, valido
    pr("CHEQUEO INSTRUMENTO %s -> %s" % (" ".join("%s=%s" % kv for kv in guardas.items()), "VALIDO" if valido else "INVALIDO"))
    ruta = os.path.join(a.out, "nulos_R2_%s_k%03d.json" % (a.tipo, a.k0))
    with open(ruta, "w") as f:
        json.dump(res, f)
    pr("escrito %s md5=%s" % (os.path.basename(ruta), base.md5(ruta)))
    pr("# duracion_s=%.1f" % (time.time() - t_ini))
    rc = 0 if valido else 3
    pr("EXIT_RUN=%d" % rc)
    return rc


if __name__ == "__main__":
    sys.exit(main())
