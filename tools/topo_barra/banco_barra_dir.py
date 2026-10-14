#!/usr/bin/env python3
"""Banco de H_TOPO_NUEVO: la barra segun su direccion (respuesta 2026-10-14-012, paso C del sello).

Orden del sello: A la tarea (42d2f60), B el programa Topo nuevo (2deb335), C este banco. Nada corrio sobre la tarea
nueva antes de A y B.

Sujeto: el cableado que baja aterrizaje_dir.topo (identico al motivo de 46 neuronas de la 015; se verifica), con la
dinamica sellada de la 015 (tarea_mosca.simular, tau fija heterogenea semilla 0, rho 0,9) y sus lineas sin entrenar.
Rivales sobre la tarea nueva (tarea_barra_dir.py), 6 celdas (A x ruido), 2400 de entrenamiento y 2000 de prueba:
  W: el cableado real; 300 SL (destinos barajados por bloque de lados, semilla 7) y 300 T (sintonias barajadas por
  lado, semilla 11), como en la 015; la regla del programa nuevo (backend regla de Topo); la regla vieja (escape.topo).

Hipotesis pre-registradas (margen 0,01, alfa 0,05):
  H_TN_CABLEADO: W le gana a SL y a T en acierto en las 6 celdas. p = (1 + #nulos >= W)/(N + 1), Holm sobre las 12
    pruebas. SOSTENIDA si las 12 dan Holm < 0,05; si no, REFUTADA.
  H_TN_REGLA: d = acierto de la regla nueva menos acierto de W, sobre los 12.000 ensayos de prueba; bootstrap
    estratificado por celda, B = 20.000, IC al 90 %. SOSTENIDA si el limite inferior es > -0,01 (no pierde mas de un
    punto); REFUTADA si el superior es < -0,01; si no, SIN_DECIDIR.
  H_TOPO_NUEVO: SOSTENIDA si las dos lo estan; REFUTADA si alguna lo esta; si no, SIN_DECIDIR.
Descriptivo, sin veredicto: la regla vieja contra la nueva y contra W; aciertos en barras AA y AD en vuelo.
Controles: md5 de todo; la tarea pasa sus chequeos; REPRODUCE_M46; guardas de SL y T.
Salida: 0 completo; 2 insumos distintos del pin; 3 instrumento invalido. Con --humo: 3 nulos, 600/400, B = 2000; esos
numeros no valen (con 3 nulos el p minimo es 0,25 y el veredicto sale REFUTADA por construccion).
"""
import argparse
import hashlib
import json
import os
import platform
import sys
import time

import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
HERR = os.path.dirname(AQUI)
sys.path.insert(0, os.path.join(HERR, "escape_aterrizaje"))
sys.path.insert(0, os.path.join(HERR, "topo"))
sys.path.insert(0, AQUI)
import escape_aterrizaje_dbc3 as base  # noqa: E402
import tarea_mosca as tm  # noqa: E402
import topo  # noqa: E402
import tarea_barra_dir as tbd  # noqa: E402

MD5 = {
    "escape_aterrizaje/tarea_mosca.py": "40d64e074d9163753439307c5be4ac5e",
    "escape_aterrizaje/escape_aterrizaje_dbc3.py": "4d40477d87406c31672acfb6e6e8f5a2",
    "escape_aterrizaje/entrada_por_tipos.py": "e060c4bffb685aa550dadc19eda3dd02",
    "topo/topo.py": "9abefe9d620e9f94f4a68ed75108d6be",
    "topo/escape.topo": "dae4967da0085f4bedcb4365f87127b0",
    "topo_barra/tarea_barra_dir.py": "d25153570edff8dfc249945c88cd7d4c",
    "topo_barra/aterrizaje_dir.topo": "0122a4ce64884010e8bb741bb57f2e29",
}
CONN_MD5, ANNOT_MD5 = "3d802fd542b5d18570ba1ba0bb0abed9", "719904abad876c68ace1b5690c9b9b63"
N_TRAIN, N_TEST, N_NULO, B = 2400, 2000, 300, 20000
MARGEN, ALFA = 0.01, 0.05
CELDAS = [(A, s) for A in tm.AMPLITUDES for s in tm.RUIDOS]


def md5(p):
    return hashlib.md5(open(p, "rb").read()).hexdigest()


def pr(s):
    print(s, flush=True)


def holm(ps):
    ps = np.asarray(ps, dtype=float)
    orden = np.argsort(ps)
    m = len(ps)
    adj = np.zeros(m)
    acc = 0.0
    for r, i in enumerate(orden):
        acc = max(acc, min(1.0, (m - r) * ps[i]))
        adj[i] = acc
    return adj


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--conn", required=True)
    ap.add_argument("--annot", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--humo", action="store_true")
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    t0 = time.time()
    pr("# maquina: %s | %s | Python %s | numpy %s" % (platform.node(), platform.platform(), platform.python_version(),
                                                     np.__version__))
    pr("# md5 banco = " + md5(os.path.abspath(__file__)))
    pr("# fecha: " + time.strftime("%Y-%m-%d %H:%M:%S %z"))
    ok_md5 = True
    for f, m in MD5.items():
        got = md5(os.path.join(HERR, f))
        pr("# md5 %s = %s -> %s" % (f, got, got == m))
        ok_md5 = ok_md5 and got == m
    mc, ma = md5(a.conn), md5(a.annot)
    pr("# md5 conn = %s | md5 annot = %s" % (mc, ma))
    if not ok_md5 or mc != CONN_MD5 or ma != ANNOT_MD5:
        pr("ABORTA: insumos o modulos distintos del pin")
        pr("EXIT_RUN=2")
        return 2
    humo = a.humo
    if humo:
        pr("# HUMO: corrida corta, estos numeros no valen")
    n_nulo = 3 if humo else N_NULO
    n_train, n_test = (600, 400) if humo else (N_TRAIN, N_TEST)
    b_boot = 2000 if humo else B

    if tbd.chequeos() != 0:
        pr("ABORTA: la tarea no pasa sus chequeos")
        pr("EXIT_RUN=3")
        return 3
    Pn = topo.parsear(open(os.path.join(AQUI, "aterrizaje_dir.topo"), encoding="utf-8").read())
    Po = topo.parsear(open(os.path.join(HERR, "topo", "escape.topo"), encoding="utf-8").read())
    sel, aristas = topo.bajar_cableado(Pn, a.conn, a.annot)
    sel15, ar15 = tm.construir(a.conn, a.annot)
    rep = bool(sel == sel15 and aristas == ar15)
    pr("CHEQUEO REPRODUCE_M46 neuronas=%d aristas=%d -> %s" % (len(sel), len(aristas), rep))
    if not rep:
        pr("EXIT_RUN=3")
        return 3
    n = len(sel)
    nv = n - 6
    lados = ["L" if s[2] == "left" else "R" for s in sel]
    tipos = [s[1] for s in sel]
    W, rho0 = base.matriz(n, aristas)

    def cod(i, tipo):
        return (0 if lados[i] == "L" else 1) * tm.NT + tm.TIPOS.index(tipo)
    idx_W = np.array([cod(i, tipos[i]) for i in range(nv)])

    rng = np.random.default_rng(7)
    gi0, go0 = base.grados(n, aristas)
    par0 = sorted((p, q) for p, q, _ in aristas)
    sl, guard_sl = [], True
    for k in range(n_nulo):
        ar = base.barajar_sl(aristas, lados, rng)
        gi, go = base.grados(n, ar)
        ok = bool((gi == gi0).all() and (go == go0).all() and sorted((p, q) for p, q, _ in ar) != par0
                  and all((lados[p], lados[q]) == (lados[p0], lados[q0]) for (p, q, _), (p0, q0, _) in zip(ar, aristas)))
        guard_sl &= ok
        sl.append(base.matriz(n, ar)[0])
    rng_t = np.random.default_rng(11)
    perms, guard_t = [], True
    for k in range(n_nulo):
        tp = list(tipos[:nv])
        for ld in ("L", "R"):
            ix = [i for i in range(nv) if lados[i] == ld]
            vals = [tp[i] for i in ix]
            for i, j in zip(ix, rng_t.permutation(len(ix))):
                tp[i] = vals[j]
        ok = tp != tipos[:nv] and all(
            sorted(tp[i] for i in range(nv) if lados[i] == ld) == sorted(tipos[i] for i in range(nv) if lados[i] == ld)
            for ld in ("L", "R"))
        guard_t &= ok
        perms.append(np.array([cod(i, tp[i]) for i in range(nv)]))
    pr("NULOS SL=%d guarda=%s T=%d guarda=%s rho_crudo=%.4f" % (len(sl), guard_sl, len(perms), guard_t, rho0))
    if not (guard_sl and guard_t):
        pr("EXIT_RUN=3")
        return 3

    etr, ete = tbd.generar(n_train, 1), tbd.generar(n_test, 2)
    ytr, yte, vtr, vte = etr["y"], ete["y"], etr["vuelo"], ete["vuelo"]
    Ztr = np.random.default_rng(101).standard_normal((n_train, tm.T, nv))
    Zte = np.random.default_rng(102).standard_normal((n_test, tm.T, nv))
    tau0 = 0.06 + 0.12 * np.random.default_rng(0).random(n)
    aa = vte & (ete["est"] == 3)
    ad = vte & (ete["est"] == 5)
    pr("DATOS entrenamiento=%d prueba=%d clases_prueba=%s barras_AA_vuelo=%d barras_AD_vuelo=%d" % (
        n_train, n_test, ",".join(str(int((yte == k).sum())) for k in range(5)), int(aa.sum()), int(ad.sum())))

    def pred(Wm, idx, dtr, dte):
        th = tm.umbrales(tm.lineas(tm.simular(Wm, tau0, idx, dtr, nv)), ytr, vtr)
        return tm.carrera(tm.lineas(tm.simular(Wm, tau0, idx, dte, nv)), th, vte)

    def regla(P, dtr, dte):
        Xtr = dtr["drive"][:, :, idx_W] + dtr["ruido"]
        Xte = dte["drive"][:, :, idx_W] + dte["ruido"]
        return topo.ejecutar_regla(P, Xtr, ytr, vtr.astype(int), Xte, vte.astype(int), tipos[:nv], lados[:nv])[0]

    celdas, ps, conteos = [], [], []
    for A, s in CELDAS:
        dtr = dict(y=ytr, drive=tbd.sintonias(etr, A), ruido=s * Ztr)
        dte = dict(y=yte, drive=tbd.sintonias(ete, A), ruido=s * Zte)
        pw = pred(W, idx_W, dtr, dte)
        pn, po = regla(Pn, dtr, dte), regla(Po, dtr, dte)
        cw, cn, co = (pw == yte), (pn == yte), (po == yte)
        acc_sl = np.array([float((pred(Wk, idx_W, dtr, dte) == yte).mean()) for Wk in sl])
        acc_t = np.array([float((pred(W, pk, dtr, dte) == yte).mean()) for pk in perms])
        aw = float(cw.mean())
        p_sl = (1 + int((acc_sl >= aw).sum())) / (len(sl) + 1.0)
        p_t = (1 + int((acc_t >= aw).sum())) / (len(perms) + 1.0)
        ps += [p_sl, p_t]
        dd = cn.astype(int) - cw.astype(int)
        conteos.append([int((dd == -1).sum()), int((dd == 0).sum()), int((dd == 1).sum())])
        c = dict(A=A, ruido=s, W=aw, regla_nueva=float(cn.mean()), regla_vieja=float(co.mean()),
                 SL_media=float(acc_sl.mean()), SL_max=float(acc_sl.max()), T_media=float(acc_t.mean()),
                 T_max=float(acc_t.max()), p_SL=p_sl, p_T=p_t,
                 barra_AA=dict(W=float(cw[aa].mean()), nueva=float(cn[aa].mean()), vieja=float(co[aa].mean())),
                 barra_AD=dict(W=float(cw[ad].mean()), nueva=float(cn[ad].mean()), vieja=float(co[ad].mean())))
        celdas.append(c)
        pr("CELDA A=%.1f ruido=%.2f W=%.4f regla_nueva=%.4f regla_vieja=%.4f | SL media=%.4f max=%.4f p=%.4f | "
           "T media=%.4f max=%.4f p=%.4f | barra_AA W=%.3f nueva=%.3f vieja=%.3f | barra_AD W=%.3f nueva=%.3f "
           "vieja=%.3f | %.1f s" % (A, s, aw, c["regla_nueva"], c["regla_vieja"], c["SL_media"], c["SL_max"], p_sl,
                                   c["T_media"], c["T_max"], p_t, c["barra_AA"]["W"], c["barra_AA"]["nueva"],
                                   c["barra_AA"]["vieja"], c["barra_AD"]["W"], c["barra_AD"]["nueva"],
                                   c["barra_AD"]["vieja"], time.time() - t0))

    adj = holm(ps)
    for i, c in enumerate(celdas):
        c["holm_SL"], c["holm_T"] = float(adj[2 * i]), float(adj[2 * i + 1])
        pr("HOLM A=%.1f ruido=%.2f SL=%.4f T=%.4f -> %s" % (c["A"], c["ruido"], c["holm_SL"], c["holm_T"],
                                                       "GANA" if max(c["holm_SL"], c["holm_T"]) < ALFA else "NO_GANA"))
    h_cab = "SOSTENIDA" if bool((adj < ALFA).all()) else "REFUTADA"

    rb = np.random.default_rng(2026)
    tot = float(sum(sum(x) for x in conteos))
    suma = np.zeros(b_boot)
    obs = 0.0
    for cm, c0, cp in conteos:
        m = cm + c0 + cp
        obs += cp - cm
        draw = rb.multinomial(m, [cm / m, c0 / m, cp / m], size=b_boot)
        suma += draw[:, 2] - draw[:, 0]
    d_obs = obs / tot
    lo, hi = np.quantile(suma / tot, [0.05, 0.95])
    if lo > -MARGEN:
        h_reg = "SOSTENIDA"
    elif hi < -MARGEN:
        h_reg = "REFUTADA"
    else:
        h_reg = "SIN_DECIDIR"
    pr("H_TN_REGLA d(regla_nueva - W)=%+.4f IC90=[%+.4f; %+.4f] margen=-%.2f -> %s" % (d_obs, lo, hi, MARGEN, h_reg))
    pr("H_TN_CABLEADO 12 pruebas, Holm < %.2f en todas -> %s" % (ALFA, h_cab))
    if "REFUTADA" in (h_cab, h_reg):
        h = "REFUTADA"
    elif h_cab == h_reg == "SOSTENIDA":
        h = "SOSTENIDA"
    else:
        h = "SIN_DECIDIR"
    pr("H_TOPO_NUEVO -> %s%s" % (h, " (HUMO, sin valor)" if humo else ""))
    res = dict(humo=humo, n_train=n_train, n_test=n_test, n_nulo=n_nulo, B=b_boot, celdas=celdas, conteos_d=conteos,
               H_TN_REGLA=dict(d=d_obs, ic90=[float(lo), float(hi)], veredicto=h_reg), H_TN_CABLEADO=h_cab,
               H_TOPO_NUEVO=h, segundos=time.time() - t0)
    json.dump(res, open(os.path.join(a.out, "barra_dir.json"), "w"), indent=1)
    pr("EXIT_RUN=0 | %.1f s" % (time.time() - t0))
    return 0


if __name__ == "__main__":
    sys.exit(main())
