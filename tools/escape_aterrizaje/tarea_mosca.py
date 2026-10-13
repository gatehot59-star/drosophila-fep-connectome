#!/usr/bin/env python3
"""Tarea con las etiquetas de la mosca: lineas etiquetadas sobre el motivo con DNp06 (2026-10-12-015).

Diseno: respuestas 2026-10-12-013 y 2026-10-12-014. Pre-registro: este archivo se sella en una rama antes de
la corrida completa; cualquier cambio posterior se declara.

Sujeto: el motivo de la 003 (por lado, las 4 LC4 y las 4 LPLC2 con mas sinapsis sobre DNp01 y las 4 LPLC4
con mas sinapsis sobre DNp07; DNp01 y DNp07 de cada lado) mas DNp06 de cada lado y, por lado, las 4 LPLC1 y
las 4 LPLC2 con mas sinapsis sobre DNp06 (union: una LPLC2 ya elegida no se repite ni se reemplaza). Todas
las aristas de FlyWire v783 entre las elegidas, con el signo del pipeline; rho 0.9; SparseLTC con tau fija
heterogenea (semilla 0) y la dinamica de la 003 sin cambios:  z <- (1 - t) z + t tanh(W z + x),  t = dt/tau.

Tarea (un paso = 20 ms, 40 pasos). Estado (posada o en vuelo) x estimulo x lado: 20 condiciones balanceadas.
  LOOM_LATERAL  looming de un lado (l/v 10 a 80 ms)
  LOOM_FRONTAL  el mismo looming en los dos lados a la vez (aproximacion del looming frontal)
  PUNTO         punto oscuro chico que se traslada de un lado; direccion al azar
  BARRA         barra oscura ancha que va de adelante hacia atras de un lado
  NADA          sin estimulo (solo ruido)
Etiquetas (conducta de la mosca, respuestas 013 y 014):
  posada:   LOOM_LATERAL y LOOM_FRONTAL -> despegar (1)   [Ache 2019 Nat Neurosci]
            PUNTO, BARRA y NADA -> nada (0)               [PUNTO y BARRA: etiqueta de trabajo, sin fuente]
  en vuelo: LOOM_LATERAL y PUNTO -> girar alejandose: objeto a la izq -> girar a la der (3); a la der -> (4)
                                                          [Kim 2023; Ache 2019 Nat Neurosci, looming lateral]
            LOOM_FRONTAL y BARRA -> aterrizar (2)         [Ache 2019 Nat Neurosci]
            NADA -> nada (0)
Sintonias por tipo (supuestos declarados):
  LC4    velocidad de expansion saturada + 0.1 x (punto + barra), como la 005.
  LPLC2  gaussiana del tamano mientras se expande (50 y 20 grados, como la 005) + A x d x contraste del punto,
         d = 1 de atras hacia adelante y 0.5 de adelante hacia atras (Kim 2023: atras-adelante mayor; la razon
         0.5 es supuesto); 0 a la barra (Klapoetke 2017 y 2022). A barrida en {0, 0.3, 0.6}.
  LPLC1  PUNTO (primaria): contraste del punto, sin direccion (Kim 2023 la cuenta entre las sensibles al
         punto; su sintonia no esta leida). SILENCIOSA: descriptiva.
  LPLC4  PROGRESIVA (primaria): contraste de la barra + 0.3 x punto de adelante hacia atras + velocidad de
         expansion (x 1 frontal, x 0.3 lateral). Supuesto: LPLC4 es la entrada visual principal de DNp07 (1.448
         sinapsis) y DNp07 responde mas a barras de adelante hacia atras (Ache 2019). SILENCIOSA: descriptiva.
Lector E4 sin entrenar (lineas etiquetadas):
  DNp01 izq y der -> despegar (1), compiten solo posada. DNp07 izq y der -> aterrizar (2); DNp06 izq -> girar a
  la der (3); DNp06 der -> girar a la izq (4); compiten solo en vuelo (el estado es clasico, decision de la 004).
  Umbral de cada linea: cuantil 0.95 del maximo de esa linea en los ensayos de ENTRENAMIENTO cuyo estado deja
  competir a la linea y cuya respuesta correcta es nada (posada: PUNTO, BARRA y NADA; en vuelo: NADA).
  Gana la primera linea que cruza; empate en el mismo paso: mayor exceso maximo. Sin cruce: nada.
Nulos: SL (destinos barajados dentro de cada bloque de lados, conserva grados; funcion de la 003) y T (cableado
intacto, sintonias barajadas entre las visuales del mismo lado), 300 cada uno.
Rival: regla a mano con las mismas lineas sobre las entradas crudas (DNp01 del lado s: media de LC4 y LPLC2 de
ese lado; DNp06: media de LPLC1 y LPLC2; DNp07: media de LPLC4), mismos umbrales y misma carrera.
Descriptivo: ridge entrenado por estado sobre las entradas crudas (techo entrenado).
Celdas primarias: A en {0, 0.3, 0.6} x ruido en {0.15, 0.45}, con LPLC1 = PUNTO y LPLC4 = PROGRESIVA.
Pruebas: W contra SL y T, p por rango, Holm sobre 12 por cola. Celda: GANA si Holm sup < 0.05 contra SL y contra
T y ninguna inf < 0.05; PIERDE si alguna inf < 0.05 y ninguna sup; MIXTO si las dos; si no, EMPATE.
Por amplitud: GANA si gana con los dos ruidos; PIERDE si pierde con alguno; si no, EMPATE.
Global: PAGA LA TAREA DE LA MOSCA si las tres amplitudes ganan; DEPENDE DE LA AMPLITUD DE LPLC2 si una o dos;
NO PAGA si ninguna. H3: W contra la regla a mano, McNemar por celda.
Falsador pre-registrado: con las etiquetas de la mosca, W no le gana a SL ni a T (global NO PAGA).
Controles: guardas SL y T; reproduce (W dos veces identico); el sub-motivo de la 003 se reproduce (mismas 28
neuronas y mismas aristas); negativo: con entrada AGNOSTICA, 30 T dan predicciones identicas a W; positivo: la
regla a mano con A = 0.3 y ruido 0.15 supera al azar (mayoria por estado) por >= 0.10.
Descriptivo con A = 0.3 y ruido 0.15: LPLC1 SILENCIOSA y LPLC4 SILENCIOSA (W y regla, sin nulos).
Salida: 0 completo; 2 insumos distintos del pin; 3 instrumento invalido.
"""
import argparse
import json
import os
import platform
import sys
import time

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import escape_aterrizaje_dbc3 as base  # noqa: E402  modulo de la 003, sin cambios
import entrada_por_tipos as ept  # noqa: E402  modulo de la 005, sin cambios

MD5_BASE = "4d40477d87406c31672acfb6e6e8f5a2"
MD5_EPT = "e060c4bffb685aa550dadc19eda3dd02"
T = base.T
K = base.K
TIPOS = ("LC4", "LPLC2", "LPLC4", "LPLC1")
NT = len(TIPOS)
DNS = (("DNp01", "left"), ("DNp01", "right"), ("DNp07", "left"), ("DNp07", "right"),
       ("DNp06", "left"), ("DNp06", "right"))
ELECCION = (("LC4", "DNp01"), ("LPLC2", "DNp01"), ("LPLC4", "DNp07"), ("LPLC1", "DNp06"), ("LPLC2", "DNp06"))
ESTIMULOS = ("LOOM_LATERAL", "LOOM_FRONTAL", "PUNTO", "BARRA", "NADA")
CLASES = {True: np.array([0, 2, 3, 4]), False: np.array([0, 1])}
ACCION = np.array([1, 1, 2, 2, 3, 4])
COMPITE_VUELO = np.array([False, False, True, True, True, True])
AMPLITUDES = (0.0, 0.3, 0.6)
RUIDOS = (0.15, 0.45)
N_TRAIN, N_TEST = 2400, 2000
N_NULO, N_AGN = 300, 30
FA, ALFA, MARGEN_POS = 0.05, 0.05, 0.10
TH_MAX, V_REF, TH_P, TH_S = 100.0, 15.0, 50.0, 20.0
F_LC4_PUNTO, F_DIR, F4_PUNTO, F4_LAT = 0.1, 0.5, 0.3, 0.3


def pr(s):
    print(s, flush=True)


# ---------------- sujeto ----------------
def construir(conn, annot):
    a = pd.read_csv(annot, sep="\t", dtype=str, usecols=["root_id", "cell_type", "side"])
    a["root_id"] = a.root_id.astype(np.int64)
    c = pd.read_parquet(conn, columns=["Presynaptic_ID", "Postsynaptic_ID", "Connectivity", "Excitatory"])
    sel, vistos = [], set()
    for tipo, blanco in ELECCION:
        bl = a.root_id[a.cell_type == blanco]
        for lado in ("left", "right"):
            v = a[(a.cell_type == tipo) & (a.side == lado)].copy()
            m = c.Presynaptic_ID.isin(v.root_id) & c.Postsynaptic_ID.isin(bl)
            s = c[m].groupby("Presynaptic_ID").Connectivity.sum()
            v["s"] = v.root_id.map(s).fillna(0)
            v = v.sort_values(["s", "root_id"], ascending=[False, True]).head(K)
            for r, x in zip(v.root_id, v.s):
                if int(r) in vistos:
                    continue
                vistos.add(int(r))
                sel.append((int(r), tipo, lado, float(x), blanco))
    for tipo, lado in DNS:
        r = a[(a.cell_type == tipo) & (a.side == lado)].root_id
        assert len(r) == 1, (tipo, lado, len(r))
        sel.append((int(r.iloc[0]), tipo, lado, 0.0, ""))
    ids = [s[0] for s in sel]
    ix = {r: i for i, r in enumerate(ids)}
    sub = c[c.Presynaptic_ID.isin(ids) & c.Postsynaptic_ID.isin(ids)]
    aristas = [(ix[p], ix[q], float(w * e)) for p, q, w, e in sub.itertuples(index=False)]
    return sel, aristas


# ---------------- tarea ----------------
def generar(n, seed):
    rng = np.random.default_rng(seed)
    cond = np.arange(n) % 20
    rng.shuffle(cond)
    vuelo = cond < 10
    est = (cond % 10) // 2
    lado = cond % 2
    direc = np.zeros(n, dtype=int)
    th = np.zeros((n, T))
    thd = np.zeros((n, T))
    punto = np.zeros((n, T))
    barra = np.zeros((n, T))
    tt = np.arange(T).astype(float)
    for i in range(n):
        te = int(rng.integers(26, 35))
        t_on = te - int(rng.integers(12, 21))
        vis = (tt >= t_on) & (tt <= te)
        if est[i] <= 1:
            r = rng.uniform(0.5, 4.0)
            tc = te + r / np.tan(np.radians(TH_MAX / 2.0))
            with np.errstate(divide="ignore", invalid="ignore"):
                ang = np.degrees(2.0 * np.arctan(r / (tc - tt)))
                ang_prev = np.degrees(2.0 * np.arctan(r / (tc - tt + 1.0)))
            th[i] = np.where(vis, ang, 0.0)
            thd[i] = np.where(vis, ang - ang_prev, 0.0)
        elif est[i] == 2:
            punto[i] = np.where(vis, rng.uniform(0.4, 1.0), 0.0)
            direc[i] = 1 if rng.random() < 0.5 else -1
        elif est[i] == 3:
            barra[i] = np.where(vis, rng.uniform(0.4, 1.0), 0.0)
            direc[i] = -1
    y = np.zeros(n, dtype=int)
    y[~vuelo & (est <= 1)] = 1
    y[vuelo & ((est == 1) | (est == 3))] = 2
    gira = vuelo & ((est == 0) | (est == 2))
    y[gira] = 3 + lado[gira]
    return dict(y=y, vuelo=vuelo, est=est, lado=lado, direc=direc, th=th, thd=thd, punto=punto, barra=barra)


def sintonias(e, A, v1="PUNTO", v4="PROGRESIVA", agnostica=False):
    """Entrada (n, T, 2 * NT), canal = lado * NT + tipo (LC4, LPLC2, LPLC4, LPLC1)."""
    expande = e["thd"] > 0.05
    g = np.exp(-((e["th"] - TH_P) ** 2) / (2.0 * TH_S ** 2))
    vel = np.clip(e["thd"] / V_REF, 0.0, 1.0)
    pu, ba = e["punto"], e["barra"]
    d = np.where(e["direc"] == 1, 1.0, F_DIR)[:, None]
    frontal = (e["est"] == 1)[:, None]
    lc4 = vel + F_LC4_PUNTO * (pu + ba)
    lplc2 = np.where(expande, g, 0.0) + A * d * pu
    if v1 == "PUNTO":
        lplc1 = pu.copy()
    elif v1 == "SILENCIOSA":
        lplc1 = np.zeros_like(pu)
    else:
        raise ValueError(v1)
    if v4 == "PROGRESIVA":
        lplc4 = ba + F4_PUNTO * pu * (e["direc"] == -1)[:, None] + vel * np.where(frontal, 1.0, F4_LAT)
    elif v4 == "SILENCIOSA":
        lplc4 = np.zeros_like(pu)
    else:
        raise ValueError(v4)
    us = [lc4, lplc2, lplc4, lplc1]
    if agnostica:
        u = np.maximum.reduce(us)
        us = [u, u, u, u]
    n = len(e["y"])
    en_lado = np.stack([(e["lado"] == s) | (e["est"] == 1) for s in (0, 1)], axis=1)
    drive = np.zeros((n, T, 2 * NT))
    for k, u in enumerate(us):
        for s in (0, 1):
            drive[:, :, s * NT + k] = np.where(en_lado[:, s][:, None], u, 0.0)
    return drive


def simular(W, tau, idx, d, nv):
    """Mismas operaciones que base.simular; devuelve las 6 descendentes."""
    n_neur = W.shape[0]
    n = len(d["y"])
    t_ = base.DT / tau
    z = np.zeros((n, n_neur))
    out = np.zeros((n, T, 6))
    for t in range(T):
        x = np.zeros((n, n_neur))
        x[:, :nv] = d["drive"][:, t, :][:, idx] + d["ruido"][:, t, :]
        z = (1 - t_) * z + t_ * np.tanh(z @ W.T + x)
        out[:, t, :] = z[:, nv:nv + 6]
    return out


# ---------------- lector ----------------
def umbrales(S, y, vuelo):
    th = np.zeros(6)
    for k in range(6):
        m = (y == 0) & (vuelo == COMPITE_VUELO[k])
        th[k] = np.quantile(S[m].max(axis=1)[:, k], 1.0 - FA)
    return th


def carrera(S, th, vuelo):
    big = T + 1
    cruza = S > th[None, None, :]
    t_cruce = np.where(cruza.any(axis=1), cruza.argmax(axis=1), big)
    compite = np.where(vuelo[:, None], COMPITE_VUELO[None, :], ~COMPITE_VUELO[None, :])
    t_cruce = np.where(compite, t_cruce, big)
    exceso = (S - th[None, None, :]).max(axis=1)
    t_min = t_cruce.min(axis=1)
    score = np.where(t_cruce == t_min[:, None], exceso, -np.inf)
    gan = score.argmax(axis=1)
    return np.where(t_min >= big, 0, ACCION[gan])


def ridge_estado(Xtr, ytr, vtr, Xte, vte):
    pred = np.zeros(len(Xte), dtype=np.int64)
    for s in (True, False):
        mtr, mte = vtr == s, vte == s
        pred[mte] = ept.ridge(Xtr[mtr], ytr[mtr], Xte[mte], CLASES[s])[0]
    return pred


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--conn", required=True)
    ap.add_argument("--annot", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--humo", action="store_true", help="corrida corta de humo: numeros sin valor")
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    t0 = time.time()
    pr("# maquina: %s | %s | Python %s | numpy %s | pandas %s" % (platform.node(), platform.platform(),
       platform.python_version(), np.__version__, pd.__version__))
    pr("# md5 script = " + base.md5(os.path.abspath(__file__)))
    mb, me = base.md5(os.path.abspath(base.__file__)), base.md5(os.path.abspath(ept.__file__))
    pr("# md5 modulo 003 = %s | md5 modulo 005 = %s" % (mb, me))
    pr("# fecha: " + time.strftime("%Y-%m-%d %H:%M:%S %z"))
    mc, ma = base.md5(a.conn), base.md5(a.annot)
    pr("# md5 conn = %s | md5 annot = %s" % (mc, ma))
    if mc != base.MD5_CONN or ma != base.MD5_ANNOT or mb != MD5_BASE or me != MD5_EPT:
        pr("ABORTA: insumos distintos del pin")
        pr("EXIT_RUN=2")
        return 2
    humo = a.humo
    if humo:
        pr("# HUMO: corrida corta, estos numeros no valen")
    n_nulo = 3 if humo else N_NULO
    n_agn = 3 if humo else N_AGN
    n_train, n_test = (600, 400) if humo else (N_TRAIN, N_TEST)

    sel, aristas = construir(a.conn, a.annot)
    n = len(sel)
    nv = n - 6
    lados = ["L" if s[2] == "left" else "R" for s in sel]
    tipos = [s[1] for s in sel]
    assert all(t in TIPOS for t in tipos[:nv]) and [(s[1], s[2]) for s in sel[nv:]] == list(DNS)
    for s in sel:
        pr("MOTIVO root_id=%d tipo=%s lado=%s elegida_por=%s sinapsis_al_blanco=%d" % (s[0], s[1], s[2], s[4], s[3]))
    W, rho0 = base.matriz(n, aristas)
    pr("MOTIVO neuronas=%d visuales=%d aristas=%d sinapsis=%d inhibitorias=%d ipsilaterales=%d rho_crudo=%.4f" % (
        n, nv, len(aristas), int(sum(abs(w) for _, _, w in aristas)), sum(w < 0 for _, _, w in aristas),
        sum(lados[p] == lados[q] for p, q, _ in aristas), rho0))
    for t in TIPOS:
        pr("MOTIVO tipo=%s por_lado=(%d,%d)" % (t, sum(1 for i in range(nv) if tipos[i] == t and lados[i] == "L"),
                                             sum(1 for i in range(nv) if tipos[i] == t and lados[i] == "R")))
    for j, (dn, ld) in enumerate(DNS):
        q = nv + j
        comp = {t: int(sum(abs(w) for p, qq, w in aristas if qq == q and p < nv and tipos[p] == t)) for t in TIPOS}
        pr("COMPOSICION dn=%s lado=%s sinapsis_desde=%s" % (dn, ld, comp))
    bsel, bar = base.construir_motivo(a.conn, a.annot)
    bids = [s[0] for s in bsel]
    ids = [s[0] for s in sel]
    idx28 = list(range(24)) + list(range(nv, nv + 4))
    mis = [ids[i] for i in idx28]
    pos = {i: k for k, i in enumerate(idx28)}
    sub28 = sorted((mis[pos[p]], mis[pos[q]], w) for p, q, w in aristas if p in pos and q in pos)
    b28 = sorted((bids[p], bids[q], w) for p, q, w in bar)
    rep003 = bool(bids == mis and sub28 == b28)
    pr("CHEQUEO REPRODUCE_003 neuronas=%s aristas=%d contra %d -> %s" % (bids == mis, len(sub28), len(b28), rep003))

    def cod(i, tipo):
        return (0 if lados[i] == "L" else 1) * NT + TIPOS.index(tipo)
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
    pr("NULOS SL=%d guarda=%s T=%d guarda=%s" % (len(sl), guard_sl, len(perms), guard_t))

    etr, ete = generar(n_train, 1), generar(n_test, 2)
    ytr, yte, vtr, vte = etr["y"], ete["y"], etr["vuelo"], ete["vuelo"]
    Ztr = np.random.default_rng(101).standard_normal((n_train, T, nv))
    Zte = np.random.default_rng(102).standard_normal((n_test, T, nv))
    maj = {s: int(np.bincount(ytr[vtr == s]).argmax()) for s in (True, False)}
    azar = float((np.where(vte, maj[True], maj[False]) == yte).mean())
    pr("DATOS entrenamiento=%d prueba=%d clases_prueba(nada,despegar,aterrizar,girar_der,girar_izq)=%s "
       "azar_mayoria_por_estado=%.4f FA_por_linea=%.2f" % (
           n_train, n_test, ",".join(str(int((yte == k).sum())) for k in range(5)), azar, FA))
    tau0 = 0.06 + 0.12 * np.random.default_rng(0).random(n)

    def media(X, ld, ts):
        m = np.array([lados[i] == ld and tipos[i] in ts for i in range(nv)])
        return X[:, :, m].mean(2)

    def lineas_crudas(X):
        return np.stack([media(X, "L", ("LC4", "LPLC2")), media(X, "R", ("LC4", "LPLC2")),
                         media(X, "L", ("LPLC4",)), media(X, "R", ("LPLC4",)),
                         media(X, "L", ("LPLC1", "LPLC2")), media(X, "R", ("LPLC1", "LPLC2"))], axis=2)

    def datos(A, s, v1="PUNTO", v4="PROGRESIVA", agn=False):
        dtr = dict(y=ytr, drive=sintonias(etr, A, v1, v4, agn), ruido=s * Ztr)
        dte = dict(y=yte, drive=sintonias(ete, A, v1, v4, agn), ruido=s * Zte)
        return dtr, dte

    def pred(Wm, idx, dtr, dte):
        th = umbrales(simular(Wm, tau0, idx, dtr, nv), ytr, vtr)
        return carrera(simular(Wm, tau0, idx, dte, nv), th, vte), th

    def crudas(d):
        return d["drive"][:, :, idx_W] + d["ruido"]

    def regla(dtr, dte):
        th = umbrales(lineas_crudas(crudas(dtr)), ytr, vtr)
        return carrera(lineas_crudas(crudas(dte)), th, vte)

    def acc(p):
        return float((p == yte).mean())

    def por_condicion(p):
        return [float((p[(vte == v) & (ete["est"] == k)] == yte[(vte == v) & (ete["est"] == k)]).mean())
                for v in (False, True) for k in range(5)]

    def fmt(xs):
        return ",".join("%.3f" % x for x in xs)

    pr("ORDEN por_condicion = posada(%s) | vuelo(%s)" % (",".join(ESTIMULOS), ",".join(ESTIMULOS)))
    res = {"humo": humo, "guarda_SL": guard_sl, "guarda_T": guard_t, "reproduce_003": rep003, "azar": azar,
           "celdas": {}}
    prim, pW_c, regla_c = {}, {}, {}
    for A in AMPLITUDES:
        for s in RUIDOS:
            tc = time.time()
            dtr, dte = datos(A, s)
            pW, thW = pred(W, idx_W, dtr, dte)
            aW = acc(pW)
            a_sl = [acc(pred(Ws, idx_W, dtr, dte)[0]) for Ws in sl]
            a_t = [acc(pred(W, ix, dtr, dte)[0]) for ix in perms]
            ps_sl, pi_sl = ept.p_rango(aW, a_sl)
            ps_t, pi_t = ept.p_rango(aW, a_t)
            pR = regla(dtr, dte)
            aR = acc(pR)
            b1, c1, p1 = base.mcnemar(pW == yte, pR == yte)
            h3 = "MEJOR" if (b1 > c1 and p1 < ALFA) else ("PEOR" if (c1 > b1 and p1 < ALFA) else "EMPATE")
            pRidge = ridge_estado(crudas(dtr).reshape(n_train, -1), ytr, vtr, crudas(dte).reshape(n_test, -1), vte)
            c = dict(W=aW, W_por_condicion=por_condicion(pW), umbrales_W=thW.tolist(), SL=a_sl, T=a_t,
                     p_sup_SL=ps_sl, p_inf_SL=pi_sl, p_sup_T=ps_t, p_inf_T=pi_t, regla=aR,
                     regla_por_condicion=por_condicion(pR), H3_gana_W=b1, H3_gana_regla=c1, H3_p=p1, H3=h3,
                     ridge_crudo_entrenado=acc(pRidge), dur_s=time.time() - tc)
            prim[(A, s)], pW_c[(A, s)], regla_c[(A, s)] = c, pW, aR
            pr("CELDA A=%.1f ruido=%.2f W=%.4f por_condicion=%s umbrales=%s | SL media=%.4f max=%.4f igualan=%d/%d "
               "p_sup=%.4f p_inf=%.4f | T media=%.4f max=%.4f igualan=%d/%d p_sup=%.4f p_inf=%.4f | %.1f s" % (
                   A, s, aW, fmt(c["W_por_condicion"]), fmt(thW), np.mean(a_sl), np.max(a_sl),
                   sum(x >= aW for x in a_sl), len(a_sl), ps_sl, pi_sl, np.mean(a_t), np.max(a_t),
                   sum(x >= aW for x in a_t), len(a_t), ps_t, pi_t, c["dur_s"]))
            pr("RIVAL A=%.1f ruido=%.2f regla_a_mano=%.4f por_condicion=%s | H3 W contra regla %d contra %d p=%.3g -> %s"
               " | ridge_crudo_entrenado(descriptivo)=%.4f" % (A, s, aR, fmt(c["regla_por_condicion"]), b1, c1, p1, h3,
                                                              c["ridge_crudo_entrenado"]))

    claves = [(A, s, nul) for A in AMPLITUDES for s in RUIDOS for nul in ("SL", "T")]
    adj_sup = ept.holm([prim[(A, s)]["p_sup_" + nul] for A, s, nul in claves])
    adj_inf = ept.holm([prim[(A, s)]["p_inf_" + nul] for A, s, nul in claves])
    for (A, s, nul), x, y_ in zip(claves, adj_sup, adj_inf):
        prim[(A, s)]["holm_sup_" + nul] = float(x)
        prim[(A, s)]["holm_inf_" + nul] = float(y_)

    A0, s0 = 0.3, RUIDOS[0]
    dtr, dte = datos(A0, s0)
    repro = bool(np.array_equal(pred(W, idx_W, dtr, dte)[0], pW_c[(A0, s0)]))
    dA_tr, dA_te = datos(A0, s0, agn=True)
    pA = pred(W, idx_W, dA_tr, dA_te)[0]
    iguales = [bool(np.array_equal(pred(W, ix, dA_tr, dA_te)[0], pA)) for ix in perms[:n_agn]]
    c_neg = all(iguales)
    c_pos = regla_c[(A0, s0)] >= azar + MARGEN_POS
    pr("CONTROL_NEGATIVO entrada=AGNOSTICA W=%.4f T_identicos=%d/%d -> %s" % (acc(pA), sum(iguales), len(iguales), c_neg))
    pr("CONTROL_POSITIVO regla_a_mano A=%.1f ruido=%.2f = %.4f contra azar %.4f + %.2f -> %s" % (
        A0, s0, regla_c[(A0, s0)], azar, MARGEN_POS, c_pos))
    desc = {}
    for nom, v1, v4 in (("LPLC1_SILENCIOSA", "SILENCIOSA", "PROGRESIVA"), ("LPLC4_SILENCIOSA", "PUNTO", "SILENCIOSA")):
        dtr, dte = datos(A0, s0, v1, v4)
        pW = pred(W, idx_W, dtr, dte)[0]
        pR = regla(dtr, dte)
        desc[nom] = dict(W=acc(pW), W_por_condicion=por_condicion(pW), regla=acc(pR), regla_por_condicion=por_condicion(pR))
        pr("DESCRIPTIVO %s A=%.1f ruido=%.2f W=%.4f por_condicion=%s | regla=%.4f por_condicion=%s" % (
            nom, A0, s0, acc(pW), fmt(desc[nom]["W_por_condicion"]), acc(pR), fmt(desc[nom]["regla_por_condicion"])))
    valido = bool(guard_sl and guard_t and rep003 and repro and c_neg and c_pos)
    pr("CHEQUEO INSTRUMENTO guarda_SL=%s guarda_T=%s reproduce_003=%s reproduce=%s control_negativo=%s "
       "control_positivo=%s -> %s" % (guard_sl, guard_t, rep003, repro, c_neg, c_pos, "VALIDO" if valido else "INVALIDO"))

    ver_a = {}
    for A in AMPLITUDES:
        vc = []
        for s in RUIDOS:
            c = prim[(A, s)]
            sup_both = c["holm_sup_SL"] < ALFA and c["holm_sup_T"] < ALFA
            sup_any = c["holm_sup_SL"] < ALFA or c["holm_sup_T"] < ALFA
            inf_any = c["holm_inf_SL"] < ALFA or c["holm_inf_T"] < ALFA
            if sup_both and not inf_any:
                x = "GANA"
            elif inf_any and not sup_any:
                x = "PIERDE"
            elif inf_any and sup_any:
                x = "MIXTO"
            else:
                x = "EMPATE"
            c["veredicto"] = x
            vc.append(x)
            pr("VEREDICTO_CELDA A=%.1f ruido=%.2f holm_sup(SL,T)=(%.4f,%.4f) holm_inf(SL,T)=(%.4f,%.4f) -> %s" % (
                A, s, c["holm_sup_SL"], c["holm_sup_T"], c["holm_inf_SL"], c["holm_inf_T"], x))
        ver_a[A] = "GANA" if all(x == "GANA" for x in vc) else ("PIERDE" if "PIERDE" in vc else "EMPATE")
        pr("VEREDICTO_AMPLITUD A=%.1f -> %s" % (A, ver_a[A]))
    ng = sum(x == "GANA" for x in ver_a.values())
    glob = "PAGA LA TAREA DE LA MOSCA" if ng == len(AMPLITUDES) else ("DEPENDE DE LA AMPLITUD DE LPLC2" if ng else "NO PAGA")
    pierde = ["%.1f" % A for A in AMPLITUDES if ver_a[A] == "PIERDE"]
    if pierde:
        glob += " (PIERDE con A=%s)" % ",".join(pierde)
    pr("VEREDICTO_GLOBAL -> %s" % glob)
    res["celdas"] = {"%.1f|%.2f" % k: x for k, x in prim.items()}
    res.update(controles=dict(reproduce=repro, control_negativo=c_neg, control_positivo=c_pos),
               descriptivo=desc, veredicto_amplitud={"%.1f" % k: v for k, v in ver_a.items()},
               veredicto_global=glob, valido=valido)
    ruta = os.path.join(a.out, "resultados.json")
    with open(ruta, "w") as fh:
        json.dump(res, fh, indent=1, sort_keys=True, default=float)
    pr("escrito resultados.json md5=" + base.md5(ruta))
    pr("# duracion_s=%.1f" % (time.time() - t0))
    rc = 0 if valido else 3
    pr("EXIT_RUN=%d" % rc)
    return rc


if __name__ == "__main__":
    sys.exit(main())
