#!/usr/bin/env python3
"""H_PARES_DATOS: instrumento del sello tools/pares/SELLO-PARES-DATOS.md (commit 0d30190). Respuesta 2026-10-14-059.

La curva de datos de la mosca contra sus pares artificiales, con el mismo lector L y los mismos ensayos etiquetados.
  W        la mosca sin ejemplos de accion: trazas de las 6 descendentes con tau t (20 a 29), tm.lineas, tm.umbrales
           (los ensayos sin evento del entrenamiento) y tm.carrera, sin cambios.
  MOSCA_L  L sobre esas trazas (40 pasos por 6, 240 rasgos).
  CRUDO    L sobre las 564 entradas crudas por 40 pasos (22.560 rasgos); con n = 2.400 es el RIDGE de H_RIVAL.
  PCA_L    L sobre las 240 primeras componentes principales, ajustadas con los ensayos de entrenamiento sin etiquetas.
  PROY_L   L sobre 10 proyecciones gaussianas de 240 rasgos (default_rng([2061, k]), k = 0 a 9).
L es lm.lector (el RIDGE de H_RIVAL) linea por linea, con una sola guarda: un estado sin ensayos en el conjunto de
ajuste queda sin modelo y sus ensayos se predicen como clase 0. Subconjuntos anidados: sort(perm(r)[:n]) con
perm(r) = default_rng([2059, r]).permutation(2400), r = 0 a 19; en n = 2.400, todos.
Modos:
  --mosca --celda A|ruido --taus 20,21   W, W_n y MOSCA_L con cada tau; en n = 2.400, REPRO_TAULIBRE.
  --crudo --celda A|ruido                CRUDO, PCA_L y PROY_L; en n = 2.400, REPRO_CRUDO.
  --humo    ciego: REPRO_TAULIBRE (primera tau) o REPRO_CRUDO a tamano completo, que reproducen resultados ya
            publicados, y las rutas de la curva con 600 y 200 ensayos en la semilla 99, sin aciertos.
  --local   prueba de codigo en una maquina chica: todo con 600 y 200 en la semilla 99; los REPRO quedan NO_APLICA,
            los aciertos van al json marcado local y no se imprimen; nunca decide.
Salida: 0 completo; 2 insumos distintos del pin; 3 control fallido.
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
RAIZ = os.path.abspath(os.path.join(AQUI, "..", ".."))
sys.path.insert(0, os.path.join(RAIZ, "tools", "taulibre"))
import taulibre_mosca as tl  # noqa: E402  instrumento de H_TAU_LIBRE (c65bebe2), sin cambios

lm, rv, f2, tm = tl.lm, tl.rv, tl.f2, tl.tm
NL = chr(10)
MD5_TAULIBRE = "c65bebe270da1e0526a212cff29830fd"
MD5_TSUMS = "89ebc30bdf307e9c071168fb3584379f"
DIR_TAULIBRE = os.path.join(RAIZ, "results", "taulibre_2026-10-15")
TAUS = list(range(20, 30))
CELDAS = (2, 5)
PRUEBA = 12
NS = (6, 12, 24, 48, 96, 192, 384, 768, 2400)
REPS = 20
SEM_SUB = 2059
SEM_PROY = 2061
N_PROY = 10
ANCHO = 240
TOL_ORTO = 1e-8
CHICO_REPS = 2


def pr(s):
    print(s, flush=True)


# ---------------- pines y publicados ----------------
def pines(conn, annot):
    ok = tl.pines(conn, annot)
    ok["md5_taulibre_mosca.py"] = bool(rv.md5(os.path.abspath(tl.__file__)) == MD5_TAULIBRE)
    sums = os.path.join(DIR_TAULIBRE, "MD5SUMS.txt")
    ok["md5_taulibre_MD5SUMS"] = bool(rv.md5(sums) == MD5_TSUMS)
    lista = {}
    for x in open(sums).read().split(NL):
        partes = x.split()
        if len(partes) == 2 and partes[1].startswith("reales_c") and partes[1].endswith(".json"):
            lista[partes[1]] = partes[0]
    ok["taulibre_4_reales"] = bool(len(lista) == 4 and
                                   all(rv.md5(os.path.join(DIR_TAULIBRE, k)) == v for k, v in lista.items()))
    return ok


def publicados(ci):
    """Las 10 taus reales de H_TAU_LIBRE en la celda (json pineados por su MD5SUMS)."""
    por_tau = {}
    for t0 in (20, 25):
        d = json.load(open(os.path.join(DIR_TAULIBRE, "reales_c%d_t%d.json" % (ci, t0))))
        if d.get("valido") is True and d.get("ci") == ci:
            for r in d["reales"]:
                por_tau[int(r["tau"])] = r
    return por_tau


# ---------------- subconjuntos ----------------
def ns_de(ntr):
    return [n for n in NS if n < ntr] + [ntr]


def subconjuntos(ntr, reps):
    perms = [np.random.default_rng([SEM_SUB, r]).permutation(ntr) for r in range(reps)]
    sub = {}
    for n in ns_de(ntr):
        sub[n] = [np.arange(ntr)] if n == ntr else [np.sort(p[:n]) for p in perms]
    return sub


def huella(sub):
    h = {}
    for n in sorted(sub):
        m = hashlib.md5()
        for s in sub[n]:
            m.update(np.asarray(s, dtype=np.int64).tobytes())
        h[str(n)] = m.hexdigest()
    return h


def anidados(sub, ntr):
    ok = True
    for n in sorted(sub):
        for s in sub[n]:
            ok = ok and len(s) == n and len(np.unique(s)) == n and int(s.min()) >= 0 and int(s.max()) < ntr
    chicos = [n for n in sorted(sub) if n < ntr]
    for a, b in zip(chicos[:-1], chicos[1:]):
        ok = ok and all(bool(np.isin(sa, sb).all()) for sa, sb in zip(sub[a], sub[b]))
    return bool(ok)


# ---------------- el lector L, con la guarda ----------------
def ajustar(F, y, v, idx, lams):
    """rv.ridge_ajustar linea por linea; un estado sin ensayos en idx queda sin modelo."""
    mods = {}
    for s in (True, False):
        ii = idx[v[idx] == s]
        if len(ii) == 0:
            continue
        cl = tm.CLASES[s]
        A = F[ii]
        mu, sd = A.mean(0), A.std(0) + 1e-6
        A -= mu
        A /= sd
        Y = np.eye(len(cl))[np.searchsorted(cl, y[ii])]
        mods[s] = (mu, sd, cl) + tuple(rv._dual(A, Y, lams))
    return mods


def predecir(mods, F, v, idx, nl):
    """rv.ridge_predecir linea por linea; los ensayos de un estado sin modelo quedan en la clase 0."""
    P = np.zeros((nl, len(idx)), dtype=np.int64)
    for s, (mu, sd, cl, Ac, am, ym, alfas) in mods.items():
        sel = np.where(v[idx] == s)[0]
        if len(sel) == 0:
            continue
        Bm = F[idx[sel]]
        Bm -= mu
        Bm /= sd
        Bm -= am
        G = Bm @ Ac.T
        for k, al in enumerate(alfas):
            P[k, sel] = cl[(G @ al + ym).argmax(1)]
    return P


def validar(F, y, v, pl, lams):
    """rv.cv_ridge linea por linea, con la guarda."""
    acc = np.zeros((len(pl), len(lams)))
    for j, (ia, it) in enumerate(pl):
        mods = ajustar(F, y, v, ia, lams)
        acc[j] = (predecir(mods, F, v, it, len(lams)) == y[it][None, :]).mean(1)
        del mods
    return acc.mean(0), acc


def lector(F, y, v):
    """lm.lector con la guarda: eleccion por validacion de 5 pliegues y reajuste con todos los ensayos dados."""
    n = len(y)
    cv, _ = validar(F, y, v, rv.pliegues(n), rv.LAMBDAS_R)
    j = max(range(len(rv.LAMBDAS_R)), key=lambda k: (cv[k], rv.LAMBDAS_R[k]))
    lam = rv.LAMBDAS_R[j]
    return lam, cv, ajustar(F, y, v, np.arange(n), (lam,))


def leer(mod, F, v):
    return predecir(mod, F, v, np.arange(len(v)), 1)[0]


def curva(Ftr, ytr, vtr, Fte, yte, vte, sub):
    """Para cada n y repeticion: L con validacion y reajuste solo dentro del subconjunto; acierto en la prueba."""
    ntr = len(ytr)
    out, pfull, rutas = {}, None, True
    for n in sorted(sub):
        accs, lams = [], []
        for S in sub[n]:
            if n == ntr:
                lam, _, mod = lector(Ftr, ytr, vtr)
            else:
                lam, _, mod = lector(Ftr[S], ytr[S], vtr[S])
            p = leer(mod, Fte, vte)
            rutas = rutas and lm.en_clases(p, vte) and len(p) == len(yte)
            accs.append(float((p == yte).mean()))
            lams.append(lam)
            if n == ntr:
                pfull = p
            del mod
        out[str(n)] = dict(acc=accs, lam=lams)
    return out, pfull, bool(rutas)


def negativo(Ftr, ytr, vtr, Fte, yte, vte):
    """El control negativo de H_LECTOR: etiquetas permutadas dentro de cada estado (semilla 2043), n completo."""
    rng = np.random.default_rng(lm.SEM_PERM)
    yperm = ytr.copy()
    for st in (True, False):
        ii = np.where(vtr == st)[0]
        yperm[ii] = ytr[ii][rng.permutation(len(ii))]
    lam, _, mod = lector(Ftr, yperm, vtr)
    pn = leer(mod, Fte, vte)
    maj = {st: int(np.bincount(yte[vte == st]).argmax()) for st in (True, False)}
    azar = float((np.where(vte, maj[True], maj[False]) == yte).mean())
    an = float((pn == yte).mean())
    return dict(acierto=an, azar=azar, lam=lam, ok=bool(an <= azar + lm.MARGEN_NEG))


# ---------------- la mosca ----------------
def trazas_de(W, t, R, chan, D):
    tau = f2.tau_por_root(R["ids"], t)
    Ttr = lm.trazas(W, tau, R, chan, D["dtr"])
    Tte = lm.trazas(W, tau, R, chan, D["dte"])
    return Ttr.reshape(D["ntr"], -1), Tte.reshape(D["nte"], -1), tm.lineas(Ttr), tm.lineas(Tte)


def w_n(Ltr, ytr, vtr, Lte, yte, vte, S):
    """W con los umbrales de los ensayos sin evento que caen en S; None si falta fondo de algun estado."""
    m0 = ytr[S] == 0
    if not bool((m0 & vtr[S]).any()) or not bool((m0 & ~vtr[S]).any()):
        return None
    th = tm.umbrales(Ltr[S], ytr[S], vtr[S])
    return float((tm.carrera(Lte, th, vte) == yte).mean())


def repro_mosca(p, yte, lam, pub):
    return bool(pub is not None and rv.a_str(p) == pub["pred_WL"] and float((p == yte).mean()) == pub["WL"] and
                lam == pub["lam"])


def mosca(a, A, s, ci, R):
    C = {}
    taus = [int(x) for x in a.taus.split(",")]
    chico = bool(a.humo or a.local)
    res = dict(experimento="H_PARES_DATOS", modo="mosca", celda=rv.clave(A, s), ci=ci, taus=taus, humo=bool(a.humo),
               local=bool(a.local), md5_script=rv.md5(os.path.abspath(__file__)), filas=[], repro=None)
    C["R2_TAMANO"] = R["ok"]
    C["PLAN_MOSCA"] = bool(ci in CELDAS and len(taus) > 0 and len(set(taus)) == len(taus) and
                           all(t in TAUS for t in taus))
    W, radio = f2.matriz(R["n"], R["aristas"], densa_ok=False)
    chan = lm.chan_de(R, R["tipos"][:R["n_ent"]])
    pub = publicados(ci)
    C["PUBLICADOS"] = bool(sorted(pub) == TAUS)
    pr("RED radio_crudo=%.6f | taus=%s | taus publicadas por H_TAU_LIBRE=%d" % (radio, taus, len(pub)))
    if a.humo:
        tc = time.time()
        Dg = tl.juego(R, A, s, False)
        t = taus[0]
        Ftr, Fte, _, _ = trazas_de(W, t, R, chan, Dg)
        lam, _, mod = lector(Ftr, Dg["ytr"], Dg["vtr"])
        p = leer(mod, Fte, Dg["vte"])
        C["REPRO_TAULIBRE"] = repro_mosca(p, Dg["yte"], lam, pub.get(t))
        res["repro"] = dict(tau=t, lam=lam, igual=C["REPRO_TAULIBRE"])
        pr("REPRO_TAULIBRE tau=%d n=%d lambda=%g (H_TAU_LIBRE %s) predicciones_iguales=%s -> %s | %.1f s" % (
            t, Dg["ntr"], lam, pub[t]["lam"] if t in pub else "falta",
            bool(t in pub and rv.a_str(p) == pub[t]["pred_WL"]), C["REPRO_TAULIBRE"], time.time() - tc))
        del Dg, Ftr, Fte, mod
    D = tl.juego(R, A, s, chico)
    ntr, nte = D["ntr"], D["nte"]
    ytr, vtr, yte, vte = D["ytr"], D["vtr"], D["yte"], D["vte"]
    sub = subconjuntos(ntr, CHICO_REPS if chico else REPS)
    C["SUBCONJUNTOS"] = anidados(sub, ntr)
    C["GUARDA_FUGA"] = tl.guarda_fuga(ntr)
    res.update(prueba=D["prueba"], ntr=ntr, nte=nte, ns=sorted(sub), reps=len(sub[sorted(sub)[0]]),
               subconjuntos_md5=huella(sub))
    pr("CURVA entrenamiento=%d prueba=%d (semilla %d) n=%s repeticiones=%d anidados=%s" % (
        ntr, nte, D["prueba"], sorted(sub), res["reps"], C["SUBCONJUNTOS"]))
    rutas, rep, neg_ok = True, [0, 0], None
    for j, t in enumerate(taus):
        tc = time.time()
        Ftr, Fte, Ltr, Lte = trazas_de(W, t, R, chan, D)
        th = tm.umbrales(Ltr, ytr, vtr)
        pW = tm.carrera(Lte, th, vte)
        cur, pfull, ok_r = curva(Ftr, ytr, vtr, Fte, yte, vte, sub)
        wn = {str(n): [w_n(Ltr, ytr, vtr, Lte, yte, vte, S) for S in sub[n]] for n in sorted(sub) if n < ntr}
        rutas = bool(rutas and ok_r and lm.en_clases(pW, vte) and len(pW) == nte)
        fila = dict(tau=t)
        if j == 0:
            neg = negativo(Ftr, ytr, vtr, Fte, yte, vte)
            neg_ok = neg["ok"]
            res["control_negativo"] = dict(tau=t, **neg)
            pr("CONTROL_NEGATIVO MOSCA_L tau=%d n=%d acierto=%.4f azar=%.4f tope=%.4f -> %s" % (
                t, ntr, neg["acierto"], neg["azar"], neg["azar"] + lm.MARGEN_NEG, neg["ok"]))
        if not chico:
            fila["repro_taulibre"] = repro_mosca(pfull, yte, cur[str(ntr)]["lam"][0], pub.get(t))
            rep[0] += int(fila["repro_taulibre"])
            rep[1] += 1
        if a.humo:
            pr("TAU %d rutas_en_clases=%s (humo: sin aciertos) | %.1f s" % (t, rutas, time.time() - tc))
        else:
            fila.update(W=float((pW == yte).mean()), MOSCA_L=cur, W_n=wn, pred_W=rv.a_str(pW),
                        pred_MOSCA_L_completo=rv.a_str(pfull))
            if a.local:
                pr("TAU %d rutas_en_clases=%s (local: aciertos solo en el json) | %.1f s" % (t, rutas, time.time() - tc))
            else:
                pr("TAU %d W=%.4f MOSCA_L(n=%d)=%.4f lambda=%g repro_taulibre=%s | %.1f s" % (
                    t, fila["W"], ntr, cur[str(ntr)]["acc"][0], cur[str(ntr)]["lam"][0], fila["repro_taulibre"],
                    time.time() - tc))
                for n in sorted(sub):
                    ac = cur[str(n)]["acc"]
                    wv = [x for x in wn.get(str(n), []) if x is not None]
                    pr("CURVA MOSCA_L celda=%s tau=%d n=%d media=%.4f min=%.4f max=%.4f | W_n media=%s (%d de %d)" % (
                        rv.clave(A, s), t, n, float(np.mean(ac)), float(np.min(ac)), float(np.max(ac)),
                        ("%.4f" % float(np.mean(wv))) if wv else "-", len(wv), len(wn.get(str(n), []))))
        res["filas"].append(fila)
        del Ftr, Fte, Ltr, Lte
    if not chico:
        C["REPRO_TAULIBRE"] = bool(rep[0] == rep[1] == len(taus))
        pr("CHEQUEO REPRO_TAULIBRE iguales=%d/%d -> %s" % (rep[0], rep[1], C["REPRO_TAULIBRE"]))
    elif a.local:
        C["REPRO_TAULIBRE"] = None
        pr("CHEQUEO REPRO_TAULIBRE: NO_APLICA (local)")
    C["CONTROL_NEGATIVO"] = bool(neg_ok)
    C["RUTAS_EN_CLASES"] = bool(rutas)
    return res, C


# ---------------- los pares artificiales ----------------
def pca(Xtr, k):
    """PCA centrada, sin escalar, por la matriz de Gram de los ensayos de entrenamiento (sin etiquetas)."""
    m = Xtr.mean(0)
    Xc = Xtr - m
    e, U = np.linalg.eigh(Xc @ Xc.T)
    total = float(e.sum())
    o = np.argsort(e)[::-1][:k]
    e, U = e[o], U[:, o]
    V = (Xc.T @ U) / np.sqrt(e)
    del Xc
    orto = float(np.abs(V.T @ V - np.eye(k)).max())
    return m, V, float(e.sum() / total), orto


def proyeccion(k, d):
    return np.random.default_rng([SEM_PROY, k]).standard_normal((d, ANCHO))


def repro_crudo(p, yte, lam, fila, lam_rival):
    return bool(fila is not None and rv.a_str(p) == fila["pred_RIDGE"] and float((p == yte).mean()) == fila["RIDGE"] and
                lam == lam_rival)


def resumen(nombre, A, s, cur):
    for n in sorted(cur, key=int):
        ac = cur[n]["acc"]
        pr("CURVA %s celda=%s n=%s media=%.4f min=%.4f max=%.4f" % (
            nombre, rv.clave(A, s), n, float(np.mean(ac)), float(np.min(ac)), float(np.max(ac))))


def crudo(a, A, s, ci, R):
    C = {}
    chico = bool(a.humo or a.local)
    res = dict(experimento="H_PARES_DATOS", modo="crudo", celda=rv.clave(A, s), ci=ci, humo=bool(a.humo),
               local=bool(a.local), md5_script=rv.md5(os.path.abspath(__file__)), repro=None)
    C["R2_TAMANO"] = R["ok"]
    C["PLAN_CRUDO"] = bool(ci in CELDAS)
    chan = lm.chan_de(R, R["tipos"][:R["n_ent"]])
    rj = json.load(open(os.path.join(lm.DIR_RIVAL, "rival_c%d.json" % ci)))
    rf = {f["prueba"]: f for f in rj["filas"]}
    C["RIVAL_CELDA"] = bool(rj["celda"] == rv.clave(A, s) and rj["valido"] is True and rj["humo"] is False and
                            PRUEBA in rf and "pred_RIDGE" in rf[PRUEBA])
    lam_rival = rj["rivales"]["RIDGE"]["elegida"]
    if a.humo:
        tc = time.time()
        Dg = tl.juego(R, A, s, False)
        Xtr, Xte = lm.crudas(Dg["dtr"], chan), lm.crudas(Dg["dte"], chan)
        lam, _, mod = lector(Xtr, Dg["ytr"], Dg["vtr"])
        p = leer(mod, Xte, Dg["vte"])
        C["REPRO_CRUDO"] = repro_crudo(p, Dg["yte"], lam, rf.get(PRUEBA), lam_rival)
        res["repro"] = dict(lam=lam, igual=C["REPRO_CRUDO"])
        pr("REPRO_CRUDO prueba=%d n=%d lambda=%g (H_RIVAL %g) predicciones_iguales=%s -> %s | %.1f s" % (
            PRUEBA, Dg["ntr"], lam, lam_rival, bool(PRUEBA in rf and rv.a_str(p) == rf[PRUEBA]["pred_RIDGE"]),
            C["REPRO_CRUDO"], time.time() - tc))
        del Dg, Xtr, Xte, mod
    D = tl.juego(R, A, s, chico)
    ntr, nte = D["ntr"], D["nte"]
    ytr, vtr, yte, vte = D["ytr"], D["vtr"], D["yte"], D["vte"]
    sub = subconjuntos(ntr, CHICO_REPS if chico else REPS)
    C["SUBCONJUNTOS"] = anidados(sub, ntr)
    C["GUARDA_FUGA"] = tl.guarda_fuga(ntr)
    res.update(prueba=D["prueba"], ntr=ntr, nte=nte, ns=sorted(sub), reps=len(sub[sorted(sub)[0]]),
               subconjuntos_md5=huella(sub))
    Xtr, Xte = lm.crudas(D["dtr"], chan), lm.crudas(D["dte"], chan)
    del D
    pr("CURVA entrenamiento=%d prueba=%d rasgos=%d n=%s repeticiones=%d anidados=%s" % (
        ntr, nte, Xtr.shape[1], sorted(sub), res["reps"], C["SUBCONJUNTOS"]))
    tc = time.time()
    cur, pfull, rutas = curva(Xtr, ytr, vtr, Xte, yte, vte, sub)
    neg = negativo(Xtr, ytr, vtr, Xte, yte, vte)
    res["control_negativo"] = neg
    C["CONTROL_NEGATIVO"] = neg["ok"]
    pr("CONTROL_NEGATIVO CRUDO n=%d acierto=%.4f azar=%.4f tope=%.4f -> %s" % (
        ntr, neg["acierto"], neg["azar"], neg["azar"] + lm.MARGEN_NEG, neg["ok"]))
    if not chico:
        C["REPRO_CRUDO"] = repro_crudo(pfull, yte, cur[str(ntr)]["lam"][0], rf.get(PRUEBA), lam_rival)
        pr("CHEQUEO REPRO_CRUDO prueba=%d lambda=%g (H_RIVAL %g) -> %s" % (
            PRUEBA, cur[str(ntr)]["lam"][0], lam_rival, C["REPRO_CRUDO"]))
    elif a.local:
        C["REPRO_CRUDO"] = None
        pr("CHEQUEO REPRO_CRUDO: NO_APLICA (local)")
    pr("BRAZO CRUDO rutas_en_clases=%s | %.1f s" % (rutas, time.time() - tc))
    brazos = {"CRUDO": cur}
    tc = time.time()
    m, V, var, orto = pca(Xtr, ANCHO)
    C["PCA_ORTONORMAL"] = bool(orto < TOL_ORTO)
    res["pca"] = dict(componentes=ANCHO, varianza=var, error_ortonormal=orto)
    curP, _, ok_r = curva((Xtr - m) @ V, ytr, vtr, (Xte - m) @ V, yte, vte, sub)
    rutas = bool(rutas and ok_r)
    brazos["PCA_L"] = curP
    pr("BRAZO PCA_L componentes=%d varianza=%.4f error_ortonormal=%.2e -> %s | %.1f s" % (
        ANCHO, var, orto, C["PCA_ORTONORMAL"], time.time() - tc))
    del V
    brazos["PROY_L"] = []
    for k in range(N_PROY):
        tc = time.time()
        P = proyeccion(k, Xtr.shape[1])
        curK, _, ok_r = curva(Xtr @ P, ytr, vtr, Xte @ P, yte, vte, sub)
        rutas = bool(rutas and ok_r)
        brazos["PROY_L"].append(curK)
        pr("BRAZO PROY_L k=%d | %.1f s" % (k, time.time() - tc))
        del P
    C["RUTAS_EN_CLASES"] = bool(rutas)
    if not a.humo:
        res["brazos"] = brazos
        res["pred_CRUDO_completo"] = rv.a_str(pfull)
    if not chico:
        resumen("CRUDO", A, s, cur)
        resumen("PCA_L", A, s, curP)
        for n in sorted(curP, key=int):
            v = [float(np.mean(b[n]["acc"])) for b in brazos["PROY_L"]]
            pr("CURVA PROY_L celda=%s n=%s media=%.4f min_k=%.4f max_k=%.4f" % (
                rv.clave(A, s), n, float(np.mean(v)), float(np.min(v)), float(np.max(v))))
    return res, C


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--conn", required=True)
    ap.add_argument("--annot", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--celda", required=True, help="A|ruido, p. ej. 0.3|0.15")
    ap.add_argument("--mosca", action="store_true")
    ap.add_argument("--crudo", action="store_true")
    ap.add_argument("--taus", default="20")
    ap.add_argument("--humo", action="store_true")
    ap.add_argument("--local", action="store_true")
    a = ap.parse_args()
    if bool(a.mosca) == bool(a.crudo) or (a.humo and a.local):
        pr("ABORTA: pedir --mosca o --crudo (uno solo), y --humo o --local (a lo sumo uno)")
        pr("EXIT_RUN=2")
        return 2
    os.makedirs(a.out, exist_ok=True)
    t0 = time.time()
    pr("# maquina: %s | %s | Python %s | numpy %s" % (platform.node(), platform.platform(), platform.python_version(),
                                                      np.__version__))
    pr("# md5 script = " + rv.md5(os.path.abspath(__file__)))
    if a.humo:
        pr("# HUMO: ciego, sin aciertos nuevos")
    if a.local:
        pr("# LOCAL: prueba de codigo con %d y %d ensayos, no decide nada" % (tl.CHICO_TR, tl.CHICO_TE))
    A, s = (float(x) for x in a.celda.split("|"))
    ci = lm.celda_de(A, s)
    pin = pines(a.conn, a.annot)
    pr("PIN " + " ".join("%s=%s" % kv for kv in sorted(pin.items())))
    if not all(pin.values()):
        pr("ABORTA: insumos distintos del pin")
        pr("EXIT_RUN=2")
        return 2
    tc = time.time()
    R = lm.red(a.conn, a.annot)
    pr("SUJETO R2 neuronas=%d entradas=%d -> %s | %.1f s" % (R["n"], R["n_ent"], R["ok"], time.time() - tc))
    if a.mosca:
        res, C = mosca(a, A, s, ci, R)
        etiqueta = "mosca_c%d_t%d" % (ci, res["taus"][0])
    else:
        res, C = crudo(a, A, s, ci, R)
        etiqueta = "crudo_c%d" % ci
    C["PIN"] = True
    if a.humo:
        etiqueta = "humo_" + etiqueta
    if a.local:
        etiqueta = "local_" + etiqueta
    res["controles"] = C
    valido = all(v is not False for v in C.values())
    res["valido"] = bool(valido and not a.local)
    pr("CHEQUEO INSTRUMENTO %s -> %s" % (" ".join("%s=%s" % (k, "NO_APLICA" if v is None else v) for k, v in C.items()),
                                         "VALIDO" if valido else "INVALIDO"))
    ruta = os.path.join(a.out, etiqueta + ".json")
    with open(ruta, "w") as f:
        json.dump(res, f)
    pr("escrito %s md5=%s" % (os.path.basename(ruta), rv.md5(ruta)))
    pr("# duracion_s=%.1f" % (time.time() - t0))
    rc = 0 if valido else 3
    pr("EXIT_RUN=%d" % rc)
    return rc


if __name__ == "__main__":
    sys.exit(main())
