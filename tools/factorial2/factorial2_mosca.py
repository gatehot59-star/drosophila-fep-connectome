#!/usr/bin/env python3
"""Factorial 2 de la tarea de la mosca: la revancha justa (respuesta 2026-10-13-004).

Pregunta. En el factorial 1 (019, corrido en Actions, leido en la 2026-10-13-002) el recorte R1 (1.504 neuronas)
le gano a la regla a mano de 40 entradas, pero el chequeo post-hoc mostro que la regla con las mismas 418 entradas
sintonizadas de R1 lo alcanza (IGUALA 6/6 con TASA y LIQ). El sellado confundia cableado con cantidad de sensores,
usaba una sola semilla de tau (0) y una sola de prueba (2), y no tenia margen de equivalencia. Este experimento
repite la comparacion con la regla sobre LAS MISMAS entradas que recibe cada red, con 10 semillas de tau y 10 de
prueba, un margen de equivalencia declarado antes de correr, y suma el recorte R2 (33.489 neuronas).

Cambios contra el factorial 1 (declarados antes de correr):
  1. Regla propia: la regla a mano promedia las MISMAS entradas que recibe la red (40 en M46, 418 en R1, todas las
     sintonizadas de R2). La regla de 40 se sigue calculando como referencia.
  2. tau por root_id: tau_i = 0,06 + 0,12 u, con u de default_rng([semilla_tau, root_id]). Asi una neurona tiene el
     mismo tau en M46, R1 y R2 (en el factorial 1 las descendentes cambiaban de tau al cambiar el recorte).
  3. Ruido por root_id: cada entrada recibe ruido de default_rng([semilla_ruido, root_id]); 101 en entrenamiento y
     1000 + semilla_prueba en prueba. Un mismo sensor ve el mismo ruido en los tres recortes.
  4. Semillas: tau 0..9 (R2: 0, 1, 2); prueba 2..11 (R2: 2..6); entrenamiento fijo (generar semilla 1).
  5. R2 = R1 + las presinapticas con 5 sinapsis o mas sobre alguna neurona de R1 (definicion de la 018), con
     todas las aristas entre ellas y su signo; radio espectral por ARPACK (eigs) porque la matriz densa no entra.
  6. Sin nulos SL y T (ya medidos en el factorial 1) y sin LIF (dano en el factorial 1 y es lo mas lento).
Lo que NO cambia: tarea, sintonias, lector (lineas, umbrales FA 0,05, carrera), radio 0,9, neurona TASA y LIQ
(g = 1,0) del factorial 1, insumos con el mismo pin de md5.

Configuraciones (--config): ANCLA_015 (el camino exacto de la 015: tau por orden semilla 0, ruido 101/102, prueba
2; debe reproducir sus 12 aciertos), M46_TASA, M46_LIQ, R1_CON_TASA, R1_CON_LIQ, R1_SIN_TASA, R1_SIN_LIQ,
R2_CON_TASA. Cada corrida puede tomar un subconjunto de semillas de tau (--taus) y de celdas (--celdas) para
repartir el trabajo en trabajos paralelos; el agregador junta los json.

Primaria y contrastes: tools/factorial2/agregar_factorial2.py (diferencia W menos regla propia, margen 0,01,
bootstrap de dos vias sobre semillas de tau y de prueba, Bonferroni sobre 7 configuraciones).
Controles por corrida: pin de md5; tamano de R1 (1.504 / 91.484, 418 entradas) y de R2 (33.489 / 4.031.897,
contiene R1); SIN sin aristas negativas; SIM_IGUAL (M46: la simulacion de este script da lo mismo que la del modulo
de la 015, 1e-12); DISPERSA_IGUAL (R1: dispersa contra densa en 8 ensayos, 1e-10); TROZOS_IGUAL (R1: por trozos
contra entera, exacto); RADIO (R1: eigs contra densa, relativo 1e-6); REPRODUCE_015 (solo ANCLA_015, tolerancia
0,001 y bandera de exacto). Salida: 0 completo; 2 insumos distintos del pin; 3 control fallido.
"""
import argparse
import json
import os
import platform
import sys
import time

import numpy as np
import pandas as pd
import scipy.sparse as sp
import scipy.sparse.linalg as sla

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(AQUI, "..", "escape_aterrizaje"))
import tarea_mosca as tm  # noqa: E402  sello de la 015 (57d094a), sin cambios

base = tm.base
MD5_TM = "40d64e074d9163753439307c5be4ac5e"
CONFIGS = ("ANCLA_015", "M46_TASA", "M46_LIQ", "R1_CON_TASA", "R1_CON_LIQ", "R1_SIN_TASA", "R1_SIN_LIQ",
           "R2_CON_TASA")
CELDAS = [(A, s) for A in tm.AMPLITUDES for s in tm.RUIDOS]
G_LIQ = 1.0
SEM_RUIDO_TR, SEM_GEN_TR = 101, 1
REPRO_015 = {(0.0, 0.15): (0.9005, 0.9195), (0.0, 0.45): (0.8805, 0.8705), (0.3, 0.15): (0.9125, 0.9325),
             (0.3, 0.45): (0.8915, 0.8935), (0.6, 0.15): (0.8680, 0.9315), (0.6, 0.45): (0.8580, 0.9120)}
R1_ESPERADO, R1_ENTRADAS = (1504, 91484), 418
R2_ESPERADO = (33489, 4031897)
TROZO = 400


def pr(s):
    print(s, flush=True)


def clave(A, s):
    return "%.1f|%.2f" % (A, s)


def sujeto(conn_p, annot_p, recorte, inhib):
    sel, ar46 = tm.construir(conn_p, annot_p)
    nv46 = len(sel) - 6
    m46 = [s[0] for s in sel]
    if recorte == "M46":
        return dict(ids=m46, tipos=[s[1] for s in sel], lados=["L" if s[2] == "left" else "R" for s in sel],
                    aristas=ar46, n_ent=nv46, nv46=nv46, n_inh_crudo=0)
    a = pd.read_csv(annot_p, sep="\t", dtype=str, usecols=["root_id", "cell_type", "side"])
    a["root_id"] = a.root_id.astype(np.int64)
    c = pd.read_parquet(conn_p, columns=["Presynaptic_ID", "Postsynaptic_ID", "Connectivity", "Excitatory"])
    dns = m46[nv46:]
    c5 = c[c.Connectivity >= 5]
    U1 = set(dns) | set(int(x) for x in c5[c5.Postsynaptic_ID.isin(dns)].Presynaptic_ID.unique())
    U = U1
    if recorte == "R2":
        U = U1 | set(int(x) for x in c5[c5.Postsynaptic_ID.isin(list(U1))].Presynaptic_ID.unique())
    del c5
    tipo = {int(r): (t if isinstance(t, str) else "") for r, t in zip(a.root_id, a.cell_type)}
    lado = {int(r): (s if isinstance(s, str) else "") for r, s in zip(a.root_id, a.side)}
    resto = sorted(U - set(m46))
    extra = [r for r in resto if tipo.get(r, "") in tm.TIPOS and lado.get(r, "") in ("left", "right")]
    sx = set(extra)
    otros = [r for r in resto if r not in sx]
    ids = m46[:nv46] + extra + otros + dns
    ix = pd.Series(np.arange(len(ids)), index=np.array(ids, dtype=np.int64))
    Ul = list(U)
    sub = c[c.Presynaptic_ID.isin(Ul) & c.Postsynaptic_ID.isin(Ul)]
    del c
    p = ix[sub.Presynaptic_ID.values].values
    q = ix[sub.Postsynaptic_ID.values].values
    w = (sub.Connectivity.values * sub.Excitatory.values).astype(np.float64)
    n_ar_crudo = len(sub)
    n_inh = int((w < 0).sum())
    if inhib == "SIN":
        m = w > 0
        p, q, w = p[m], q[m], w[m]
    cod = {"left": "L", "right": "R"}
    tipos = [tipo.get(r, "") for r in ids]
    lados = [cod.get(lado.get(r, ""), "C") for r in ids]
    for s in sel:
        tipos[ids.index(s[0])] = s[1]
    return dict(ids=ids, tipos=tipos, lados=lados, aristas=(p, q, w), n_ent=nv46 + len(extra), nv46=nv46,
                n_inh_crudo=n_inh, contiene_m46=set(m46) <= U, contiene_r1=U1 <= U, n_U=len(U),
                n_ar_crudo=n_ar_crudo)


def matriz(n, ar, densa_ok):
    p, q, w = ar
    W = sp.coo_matrix((w, (q, p)), shape=(n, n)).tocsr()
    if densa_ok:
        r = float(np.abs(np.linalg.eigvals(W.toarray())).max())
    else:
        r = float(np.abs(sla.eigs(W, k=1, which="LM", return_eigenvectors=False, tol=1e-10, maxiter=100000)).max())
    return (W * (base.RHO / r)).tocsr(), r


def sim(W, tau, n_ent, chan, d, liq, idx=None):
    """TASA o LIQ; misma cuenta que el factorial 1, sin armar la matriz x entera (sumar 0,0 no cambia nada)."""
    n_tr = len(d["y"]) if idx is None else len(idx)
    sel = slice(None) if idx is None else idx
    N = W.shape[0]
    t0 = base.DT / tau
    z = np.zeros((n_tr, N))
    out = np.zeros((n_tr, tm.T, 6))
    dr, ru = d["drive"][sel], d["ruido"][sel]
    for t in range(tm.T):
        u = (W @ z.T).T if sp.issparse(W) else z @ W.T
        u[:, :n_ent] += dr[:, t, :][:, chan] + ru[:, t, :]
        tt = np.minimum(1.0, t0[None, :] * (1.0 + G_LIQ * np.abs(u))) if liq else t0
        z = (1 - tt) * z + tt * np.tanh(u)
        out[:, t, :] = z[:, N - 6:]
    return out


def sim_trozos(W, tau, n_ent, chan, d, liq, trozo=TROZO):
    n_tr = len(d["y"])
    return np.concatenate([sim(W, tau, n_ent, chan, d, liq, idx=np.arange(i, min(n_tr, i + trozo)))
                           for i in range(0, n_tr, trozo)], axis=0)


def ruido_por_root(ids_ent, n_tr, semilla):
    Z = np.empty((n_tr, tm.T, len(ids_ent)))
    for k, r in enumerate(ids_ent):
        Z[:, :, k] = np.random.default_rng([semilla, int(r)]).standard_normal((n_tr, tm.T))
    return Z


def tau_por_root(ids, semilla):
    return np.array([0.06 + 0.12 * np.random.default_rng([semilla, int(r)]).random() for r in ids])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--conn", required=True)
    ap.add_argument("--annot", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--config", required=True, choices=CONFIGS)
    ap.add_argument("--taus", default="0,1,2,3,4,5,6,7,8,9")
    ap.add_argument("--pruebas", default="2,3,4,5,6,7,8,9,10,11")
    ap.add_argument("--celdas", default="todas", help="todas o lista A|ruido separada por coma, p. ej. 0.0|0.15")
    ap.add_argument("--etiqueta", default="", help="sufijo del json cuando una configuracion va en varios trabajos")
    ap.add_argument("--humo", action="store_true", help="corrida corta de humo: numeros sin valor")
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    t_ini = time.time()
    pr("# maquina: %s | %s | Python %s | numpy %s | pandas %s" % (platform.node(), platform.platform(),
       platform.python_version(), np.__version__, pd.__version__))
    pr("# md5 script = " + base.md5(os.path.abspath(__file__)))
    mt = base.md5(os.path.abspath(tm.__file__))
    mc, ma = base.md5(a.conn), base.md5(a.annot)
    pr("# md5 modulo 015 = %s | md5 conn = %s | md5 annot = %s" % (mt, mc, ma))
    if mc != base.MD5_CONN or ma != base.MD5_ANNOT or mt != MD5_TM:
        pr("ABORTA: insumos distintos del pin")
        pr("EXIT_RUN=2")
        return 2
    humo = a.humo
    if humo:
        pr("# HUMO: corrida corta, estos numeros no valen")
    n_train, n_test = (120, 80) if humo else (tm.N_TRAIN, tm.N_TEST)
    ancla = a.config == "ANCLA_015"
    if ancla:
        recorte, inhib, neurona = "M46", "CON", "TASA"
        taus, pruebas = [0], [2]
    else:
        partes = a.config.split("_")
        recorte, neurona = partes[0], partes[-1]
        inhib = partes[1] if recorte != "M46" else "CON"
        taus = [int(x) for x in a.taus.split(",")]
        pruebas = [int(x) for x in a.pruebas.split(",")]
    celdas = CELDAS if a.celdas == "todas" else [tuple(float(v) for v in x.split("|")) for x in a.celdas.split(",")]
    liq = neurona == "LIQ"
    pr("# config: %s (recorte %s, inhibicion %s, neurona %s) taus=%s pruebas=%s celdas=%s etiqueta=%s" % (
        a.config, recorte, inhib, neurona, taus, pruebas, [clave(*c) for c in celdas], a.etiqueta or "-"))

    S = sujeto(a.conn, a.annot, recorte, inhib)
    ids, tipos, lados = S["ids"], S["tipos"], S["lados"]
    n, n_ent, nv46 = len(ids), S["n_ent"], S["nv46"]
    guardas = {}
    if recorte == "M46":
        W = base.matriz(n, S["aristas"])[0]
        n_ar = len(S["aristas"])
        n_neg = sum(1 for _, _, w in S["aristas"] if w < 0)
        guardas["sin_negativas"] = n_neg == 0
        radio = None
    else:
        esperado = R1_ESPERADO if recorte == "R1" else R2_ESPERADO
        ok = (S["n_U"], S["n_ar_crudo"]) == esperado and S["contiene_m46"] and S["contiene_r1"]
        if recorte == "R1":
            ok = ok and n_ent == R1_ENTRADAS
        guardas["%s_tamano" % recorte] = bool(ok)
        pr("SUJETO %s neuronas=%d aristas_crudas=%d inhibitorias_crudas=%d entradas=%d contiene_M46=%s contiene_R1=%s "
           "esperado=%s -> %s" % (recorte, S["n_U"], S["n_ar_crudo"], S["n_inh_crudo"], n_ent, S["contiene_m46"],
                                  S["contiene_r1"], esperado, ok))
        n_ar = len(S["aristas"][2])
        n_neg = int((S["aristas"][2] < 0).sum())
        if inhib == "SIN":
            guardas["sin_negativas"] = n_neg == 0
        tr = time.time()
        W, radio = matriz(n, S["aristas"], densa_ok=(recorte == "R1"))
        pr("RADIO crudo=%.6f metodo=%s | %.1f s" % (radio, "densa" if recorte == "R1" else "eigs", time.time() - tr))
        if recorte == "R1":
            p_, q_, w_ = S["aristas"]
            r_e = float(np.abs(sla.eigs(sp.coo_matrix((w_, (q_, p_)), shape=(n, n)).tocsr(), k=1, which="LM",
                                        return_eigenvectors=False, tol=1e-10, maxiter=100000)).max())
            guardas["RADIO"] = bool(abs(r_e - radio) / radio < 1e-6)
            pr("CHEQUEO RADIO densa=%.9f eigs=%.9f -> %s" % (radio, r_e, guardas["RADIO"]))
    pr("SUJETO neuronas=%d con_entrada=%d aristas=%d inhibitorias=%d" % (n, n_ent, n_ar, n_neg))
    for t in tm.TIPOS:
        pr("SUJETO tipo=%s con_entrada_por_lado=(%d,%d)" % (t, sum(1 for i in range(n_ent) if tipos[i] == t and lados[i] == "L"),
                                                         sum(1 for i in range(n_ent) if tipos[i] == t and lados[i] == "R")))
    chan = np.array([(0 if lados[i] == "L" else 1) * tm.NT + tm.TIPOS.index(tipos[i]) for i in range(n_ent)])

    etr = tm.generar(n_train, SEM_GEN_TR)
    ytr, vtr = etr["y"], etr["vuelo"]
    if ancla:
        Ztr = np.random.default_rng(101).standard_normal((n_train, tm.T, nv46))
    else:
        Ztr = ruido_por_root(ids[:n_ent], n_train, SEM_RUIDO_TR)

    def prueba(sem):
        e = tm.generar(n_test, sem)
        if ancla:
            Z = np.random.default_rng(102).standard_normal((n_test, tm.T, nv46))
        else:
            Z = ruido_por_root(ids[:n_ent], n_test, 1000 + sem)
        return e, Z

    def simular(tau, d):
        if ancla:
            return tm.simular(W, tau, chan, d, nv46)
        if recorte == "R2":
            return sim_trozos(W, tau, n_ent, chan, d, liq)
        return sim(W, tau, n_ent, chan, d, liq)

    def media(X, ld, ts, k):
        m = np.array([lados[i] == ld and tipos[i] in ts for i in range(k)])
        return X[:, :, m].mean(2)

    def lc(d, k):
        X = d["drive"][:, :, chan[:k]] + d["ruido"][:, :, :k]
        return np.stack([media(X, "L", ("LC4", "LPLC2"), k), media(X, "R", ("LC4", "LPLC2"), k),
                         media(X, "L", ("LPLC4",), k), media(X, "R", ("LPLC4",), k),
                         media(X, "L", ("LPLC1", "LPLC2"), k), media(X, "R", ("LPLC1", "LPLC2"), k)], axis=2)

    def regla(dtr, dte, vte, k):
        th = tm.umbrales(tm.lineas(lc(dtr, k)), ytr, vtr)
        return tm.carrera(tm.lineas(lc(dte, k)), th, vte)

    # controles de la simulacion (antes de medir)
    A0, s0 = celdas[0]
    dchk = dict(y=ytr[:16], drive=tm.sintonias(etr, A0)[:16], ruido=s0 * Ztr[:16])
    tau0 = 0.06 + 0.12 * np.random.default_rng(0).random(n) if ancla else tau_por_root(ids, taus[0])
    if recorte == "M46" and not liq:
        d1 = np.abs(sim(W, tau0, n_ent, chan, dchk, False) - tm.simular(W, tau0, chan, dchk, nv46)).max()
        guardas["SIM_IGUAL"] = bool(d1 < 1e-12)
        pr("CHEQUEO SIM_IGUAL max_dif=%.3g -> %s" % (d1, guardas["SIM_IGUAL"]))
    if recorte == "R1":
        d8 = dict(y=dchk["y"][:8], drive=dchk["drive"][:8], ruido=dchk["ruido"][:8])
        d2 = np.abs(sim(W, tau0, n_ent, chan, d8, liq) - sim(W.toarray(), tau0, n_ent, chan, d8, liq)).max()
        guardas["DISPERSA_IGUAL"] = bool(d2 < 1e-10)
        d3 = np.abs(sim_trozos(W, tau0, n_ent, chan, dchk, liq, trozo=7) - sim(W, tau0, n_ent, chan, dchk, liq)).max()
        guardas["TROZOS_IGUAL"] = bool(d3 == 0.0)
        pr("CHEQUEO DISPERSA_IGUAL max_dif=%.3g -> %s | TROZOS_IGUAL max_dif=%.3g -> %s" % (
            d2, guardas["DISPERSA_IGUAL"], d3, guardas["TROZOS_IGUAL"]))
    tau_s = {}
    for st in taus:
        tau_s[st] = 0.06 + 0.12 * np.random.default_rng(0).random(n) if ancla else tau_por_root(ids, st)
    res = dict(config=a.config, recorte=recorte, inhibicion=inhib, neurona=neurona, humo=humo, etiqueta=a.etiqueta,
               taus=taus, pruebas=pruebas, celdas=[clave(*c) for c in celdas], n_ent=n_ent, radio_crudo=radio,
               dns_root=[int(r) for r in ids[n - 6:]],
               tau_DN={str(st): [float(x) for x in tau_s[st][n - 6:]] for st in taus},
               corridas=[], reglas=[])
    pr("DATOS entrenamiento=%d prueba=%d entradas_regla_propia=%d entradas_regla40=%d" % (n_train, n_test, n_ent, nv46))
    repro = []
    for A, s in celdas:
        tc = time.time()
        dtr = dict(y=ytr, drive=tm.sintonias(etr, A), ruido=s * Ztr)
        th = {st: tm.umbrales(tm.lineas(simular(tau_s[st], dtr)), ytr, vtr) for st in taus}
        for sem in pruebas:
            ete, Zte = prueba(sem)
            yte, vte = ete["y"], ete["vuelo"]
            dte = dict(y=yte, drive=tm.sintonias(ete, A), ruido=s * Zte)
            pP, p40 = regla(dtr, dte, vte, n_ent), regla(dtr, dte, vte, nv46)
            aP, a40 = float((pP == yte).mean()), float((p40 == yte).mean())
            res["reglas"].append(dict(celda=clave(A, s), prueba=sem, regla_propia=aP, regla40=a40,
                                      pred_regla_propia="".join(map(str, pP.tolist()))))
            for st in taus:
                pW = tm.carrera(tm.lineas(simular(tau_s[st], dte)), th[st], vte)
                aW = float((pW == yte).mean())
                b, c_, pm = base.mcnemar(pW == yte, pP == yte)
                res["corridas"].append(dict(celda=clave(A, s), tau=st, prueba=sem, W=aW, regla_propia=aP, regla40=a40,
                                            mcnemar_W=b, mcnemar_regla=c_, mcnemar_p=pm,
                                            pred_W="".join(map(str, pW.tolist()))))
                pr("CORRIDA celda=%s tau=%d prueba=%d W=%.4f regla_propia=%.4f regla40=%.4f dif=%+.4f" % (
                    clave(A, s), st, sem, aW, aP, a40, aW - aP))
                if ancla:
                    repro.append((abs(aW - REPRO_015[(A, s)][0]) <= 0.001 + 1e-9 and
                                  abs(a40 - REPRO_015[(A, s)][1]) <= 0.001 + 1e-9,
                                  (round(aW, 4), round(a40, 4)) == REPRO_015[(A, s)]))
        pr("CELDA %s lista | %.1f s" % (clave(A, s), time.time() - tc))
    if ancla:
        guardas["REPRODUCE_015"] = bool(all(r[0] for r in repro)) if not humo else True
        pr("CHEQUEO REPRODUCE_015 tolerancia=%s exacto=%s -> %s" % (
            "no aplica en humo" if humo else [r[0] for r in repro],
            "no aplica en humo" if humo else [r[1] for r in repro], guardas["REPRODUCE_015"]))
    valido = all(guardas.values())
    res["guardas"], res["valido"] = guardas, valido
    pr("CHEQUEO INSTRUMENTO %s -> %s" % (" ".join("%s=%s" % kv for kv in guardas.items()), "VALIDO" if valido else "INVALIDO"))
    ruta = os.path.join(a.out, "factorial2_%s%s.json" % (a.config, ("_" + a.etiqueta) if a.etiqueta else ""))
    with open(ruta, "w") as f:
        json.dump(res, f)
    pr("escrito %s md5=%s" % (os.path.basename(ruta), base.md5(ruta)))
    pr("# duracion_s=%.1f" % (time.time() - t_ini))
    rc = 0 if valido else 3
    pr("EXIT_RUN=%d" % rc)
    return rc


if __name__ == "__main__":
    sys.exit(main())
