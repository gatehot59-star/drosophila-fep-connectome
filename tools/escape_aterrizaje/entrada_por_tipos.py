#!/usr/bin/env python3
"""Entrada visual por tipo de neurona: el cableado de FlyWire contra sus barajados (2026-10-12-005).

Sujeto: el motivo de la 003 (28 neuronas, 73 aristas; por lado las 4 LC4 y las 4 LPLC2 con mas sinapsis
sobre DNp01 y las 4 LPLC4 con mas sinapsis sobre DNp07, mas DNp01 y DNp07 de cada lado), construido con
el modulo de la 003 importado sin cambios y con su dinamica SparseLTC:
  z <- (1 - t) z + t tanh(W z + x),  t = dt / tau,  tau fija heterogenea en [0.06, 0.18], W con rho 0.9.
Lo unico nuevo es la entrada (etapa E1): cada tipo visual recibe su propia sintonia.
  LC4   velocidad angular de expansion, saturada (von Reyn 2017; Ache 2019 Curr Biol).
  LPLC2 gaussiana del tamano angular mientras hay expansion (Ache 2019 Curr Biol; Klapoetke 2017) y
        respuesta al punto que se traslada (Kim 2023), con amplitud 0.6 (supuesto).
  LPLC4 sin fisiologia publicada encontrada: tres variantes declaradas, COMO_LPLC2, SILENCIOSA y
        MOVIMIENTO (movimiento sin selectividad: expansion o traslacion).
Tarea de robot inspirada en la mosca (no es una afirmacion sobre la conducta de la mosca): amenaza rapida
(l/v 10 a 30 ms), acercamiento lento (l/v 150 a 300 ms) u objeto que pasa sin acercarse, por un lado.
  vuelo: amenaza -> escapar hacia el otro lado (1 de la izq, 2 de la der); acercamiento -> aterrizar (3);
         pasa -> nada (0).
  piso:  amenaza -> escapar (1, 2); acercamiento -> nada (0); pasa -> nada (0).
El estado de vuelo lo da lo clasico (decision de la 004): un lector por estado.
Lector primario I1: ridge sobre la serie temporal de las 4 descendentes (160 rasgos). Secundario I2: MLP.
Nulos: SL (destinos barajados conservando grado y lado, funcion de la 003) y T (cableado intacto,
sintonias barajadas entre las visuales del mismo lado). Rivales clasicos: ridge y MLP sobre las 24
entradas crudas (las mismas que recibe el motivo). Control negativo: con entrada AGNOSTICA (igual para los
tres tipos) T tiene que dar exactamente lo mismo que W. Control positivo: ridge sobre los 28 estados.
Parte C (antes del sellado): calibracion del ruido sobre el rival crudo, que no depende del cableado: el
ruido dificil es el mas alto de la grilla con rival ridge crudo medio >= 0.90 (dio 0.45). No toca el motivo
ni los nulos. Parte A: primario (tau semilla 0, ruido 0.15 y 0.45, 300 SL y 300 T, Holm sobre 12 pruebas
por cola), controles y rivales. Parte B (descriptiva): robustez con tau semillas 1 y 2 (100 SL y 100 T) e
I2 (MLP sobre las 4 descendentes, ruido 0.15, 30 SL y 30 T).
Salida: 0 completo; 2 insumos distintos del pin; 3 instrumento invalido.
"""
import argparse
import json
import os
import platform
import sys
import time

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import escape_aterrizaje_dbc3 as base  # noqa: E402  modulo de la 003, sin cambios
import torch  # noqa: E402
import torch.nn as nn  # noqa: E402
import torch.nn.functional as F  # noqa: E402

MD5_BASE = "4d40477d87406c31672acfb6e6e8f5a2"
T = base.T
TIPOS = ("LC4", "LPLC2", "LPLC4")
DNS = ("DNp01", "DNp07")
VARIANTES = ("COMO_LPLC2", "SILENCIOSA", "MOVIMIENTO")
RUIDOS = (0.15, 0.45)  # 0.45 = ruido dificil de la calibracion (parte C)
SEMILLAS_TAU_ROB = (1, 2)
N_TRAIN, N_TEST = 2400, 1800  # 200 y 150 por condicion
N_NULO, N_NULO_ROB, N_NULO_MLP, N_NULO_AGN = 300, 100, 30, 30
SEMILLAS_MLP_W = (0, 1, 2)
TH_MAX, V_REF, TH_P, TH_S = 100.0, 15.0, 50.0, 20.0
F_PUNTO, F_LC4_PUNTO = 0.6, 0.1
LAMBDAS = (1e-4, 1e-3, 1e-2, 1e-1, 1.0)
C_POS = 0.75
ALFA = 0.05
CLASES = {True: np.array([0, 1, 2, 3]), False: np.array([0, 1, 2])}
ESTIMULOS = ("AMENAZA", "ACERCAMIENTO", "PASA")


def pr(s):
    print(s, flush=True)


# ---------------- entrada por tipo (E1) ----------------
def generar_estimulo(n, seed):
    """12 condiciones balanceadas: estado (vuelo, piso) x estimulo (amenaza, acercamiento, pasa) x lado.
    Angulos en grados; un paso = 20 ms."""
    rng = np.random.default_rng(seed)
    cond = np.arange(n) % 12
    rng.shuffle(cond)
    vuelo = cond < 6
    est = (cond % 6) // 2          # 0 amenaza, 1 acercamiento, 2 pasa
    lado = cond % 2                # 0 izq, 1 der
    y = np.where(est == 0, 1 + lado, np.where((est == 1) & vuelo, 3, 0))
    th = np.zeros((n, T))
    thd = np.zeros((n, T))
    punto = np.zeros((n, T))
    tt = np.arange(T).astype(float)
    for i in range(n):
        te = int(rng.integers(26, 35))          # ultimo paso de la expansion o del paso del objeto
        t_on = te - int(rng.integers(12, 21))   # primer paso visible
        vis = (tt >= t_on) & (tt <= te)
        if est[i] < 2:
            r = rng.uniform(0.5, 1.5) if est[i] == 0 else rng.uniform(7.5, 15.0)   # l/v en pasos
            tc = te + r / np.tan(np.radians(TH_MAX / 2.0))
            with np.errstate(divide="ignore", invalid="ignore"):
                ang = np.degrees(2.0 * np.arctan(r / (tc - tt)))
                ang_prev = np.degrees(2.0 * np.arctan(r / (tc - tt + 1.0)))
            th[i] = np.where(vis, ang, 0.0)
            thd[i] = np.where(vis, ang - ang_prev, 0.0)
        else:
            th[i] = np.where(vis, rng.uniform(15.0, 40.0), 0.0)
            punto[i] = np.where(vis, rng.uniform(0.4, 1.0), 0.0)
    return dict(y=y, vuelo=vuelo, est=est, lado=lado, th=th, thd=thd, punto=punto)


def sintonias(e, variante):
    """Entrada por lado y tipo: (n, T, 6), canal = lado * 3 + tipo (LC4, LPLC2, LPLC4)."""
    expande = e["thd"] > 0.05
    hay_punto = e["punto"] > 0
    g = np.exp(-((e["th"] - TH_P) ** 2) / (2.0 * TH_S ** 2))
    vel = np.clip(e["thd"] / V_REF, 0.0, 1.0)
    lc4 = vel + F_LC4_PUNTO * e["punto"]
    lplc2 = np.where(expande, g, 0.0) + np.where(hay_punto, F_PUNTO * g, 0.0)
    if variante == "COMO_LPLC2":
        lplc4 = lplc2
    elif variante == "SILENCIOSA":
        lplc4 = np.zeros_like(lplc2)
    elif variante == "MOVIMIENTO":
        lplc4 = np.clip(vel + e["punto"], 0.0, 1.0)
    elif variante == "AGNOSTICA":
        lc4 = lplc2 = lplc4 = np.maximum(lc4, lplc2)
    else:
        raise ValueError(variante)
    n = len(e["y"])
    drive = np.zeros((n, T, 6))
    for k, u in enumerate((lc4, lplc2, lplc4)):
        for s in (0, 1):
            drive[:, :, s * 3 + k] = np.where((e["lado"] == s)[:, None], u, 0.0)
    return drive


def simular_todo(W, tau, idx, d):
    """Igual que base.simular (mismas operaciones), pero devuelve los 28 estados."""
    n_neur = W.shape[0]
    n = len(d["y"])
    t_ = base.DT / tau
    z = np.zeros((n, n_neur))
    out = np.zeros((n, T, n_neur))
    nv = len(idx)
    for t in range(T):
        x = np.zeros((n, n_neur))
        x[:, :nv] = d["drive"][:, t, :][:, idx] + d["ruido"][:, t, :]
        z = (1 - t_) * z + t_ * np.tanh(z @ W.T + x)
        out[:, t, :] = z
    return out


# ---------------- lectores ----------------
def _ridge_fit(A, Y, lams):
    am, ym = A.mean(0), Y.mean(0)
    Ac, Yc = A - am, Y - ym
    ev, U = np.linalg.eigh(Ac.T @ Ac)
    R = U.T @ (Ac.T @ Yc)
    out = []
    for lam in lams:
        Wl = U @ (R / (ev + lam * len(A))[:, None])
        out.append((Wl, ym - am @ Wl))
    return out


def ridge(Xtr, ytr, Xte, clases):
    """Ridge a one-hot; lambda elegido por validacion (80/20 del entrenamiento), empate al mas grande."""
    mu, sd = Xtr.mean(0), Xtr.std(0) + 1e-6
    A, B = (Xtr - mu) / sd, (Xte - mu) / sd
    yi = np.searchsorted(clases, ytr)
    Y = np.eye(len(clases))[yi]
    nf = int(0.8 * len(A))
    sols = _ridge_fit(A[:nf], Y[:nf], LAMBDAS)
    accs = [float(((A[nf:] @ Wl + b).argmax(1) == yi[nf:]).mean()) for Wl, b in sols]
    j = max(range(len(LAMBDAS)), key=lambda k: (accs[k], LAMBDAS[k]))
    Wl, b = _ridge_fit(A, Y, (LAMBDAS[j],))[0]
    return clases[(B @ Wl + b).argmax(1)], LAMBDAS[j]


def ridge_mux(Ftr, ytr, vtr, Fte, vte):
    pred = np.zeros(len(Fte), dtype=np.int64)
    lams = {}
    for estado in (True, False):
        mtr, mte = vtr == estado, vte == estado
        pred[mte], lams[estado] = ridge(Ftr[mtr], ytr[mtr], Fte[mte], CLASES[estado])
    return pred, lams


def mlp_mux(Ftr, ytr, vtr, Fte, vte, seed, iters, h=32, lr=1e-2, batch=256):
    pred = np.zeros(len(Fte), dtype=np.int64)
    for estado in (True, False):
        mtr, mte = vtr == estado, vte == estado
        cl = CLASES[estado]
        X = Ftr[mtr]
        mu, sd = X.mean(0), X.std(0) + 1e-6
        A = torch.from_numpy(((X - mu) / sd).astype(np.float32))
        B = torch.from_numpy(((Fte[mte] - mu) / sd).astype(np.float32))
        Y = torch.from_numpy(np.searchsorted(cl, ytr[mtr]).astype(np.int64))
        torch.manual_seed(seed)
        net = nn.Sequential(nn.Linear(A.shape[1], h), nn.Tanh(), nn.Linear(h, len(cl)))
        opt = torch.optim.Adam(net.parameters(), lr=lr, weight_decay=1e-4)
        rng = np.random.default_rng(5000 + seed)
        for _ in range(iters):
            b = torch.from_numpy(rng.integers(0, len(Y), batch))
            loss = F.cross_entropy(net(A[b]), Y[b])
            opt.zero_grad()
            loss.backward()
            opt.step()
        with torch.no_grad():
            pred[mte] = cl[net(B).argmax(1).numpy()]
    return pred


# ---------------- estadistica ----------------
def p_rango(w, nulos):
    nulos = np.asarray(nulos, float)
    m = len(nulos)
    return (1 + int((nulos >= w).sum())) / (m + 1), (1 + int((nulos <= w).sum())) / (m + 1)


def holm(ps):
    ps = np.asarray(ps, float)
    m = len(ps)
    adj = np.empty(m)
    run = 0.0
    for r, i in enumerate(np.argsort(ps, kind="stable")):
        run = max(run, min(1.0, (m - r) * ps[i]))
        adj[i] = run
    return adj


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--conn", required=True)
    ap.add_argument("--annot", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--parte", choices=("A", "B", "C"), required=True)
    ap.add_argument("--humo", action="store_true", help="corrida corta de humo: numeros sin valor")
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    torch.set_num_threads(1)
    t0 = time.time()
    pr("# maquina: %s | %s | Python %s | numpy %s | torch %s" % (platform.node(), platform.platform(),
       platform.python_version(), np.__version__, torch.__version__))
    pr("# md5 script = " + base.md5(os.path.abspath(__file__)))
    mb = base.md5(os.path.abspath(base.__file__))
    pr("# md5 modulo 003 = " + mb)
    pr("# fecha: " + time.strftime("%Y-%m-%d %H:%M:%S %z"))
    pr("# parte = " + a.parte)
    mc, ma = base.md5(a.conn), base.md5(a.annot)
    pr("# md5 conn = %s | md5 annot = %s" % (mc, ma))
    if mc != base.MD5_CONN or ma != base.MD5_ANNOT or mb != MD5_BASE:
        pr("ABORTA: insumos distintos del pin")
        pr("EXIT_RUN=2")
        return 2
    humo = a.humo
    if humo:
        pr("# HUMO: corrida corta, estos numeros no valen")
    n_train, n_test = (600, 400) if humo else (N_TRAIN, N_TEST)
    n_nulo = 3 if humo else N_NULO
    n_rob = 2 if humo else N_NULO_ROB
    n_mlp = 2 if humo else N_NULO_MLP
    n_agn = 3 if humo else N_NULO_AGN
    it_mlp = 20 if humo else 300

    sel, aristas = base.construir_motivo(a.conn, a.annot)
    n = len(sel)
    nv = n - 4
    lados = ["L" if s[2] == "left" else "R" for s in sel]
    tipos = [s[1] for s in sel]
    assert all(t in TIPOS for t in tipos[:nv]) and tipos[nv:] == ["DNp01", "DNp01", "DNp07", "DNp07"]
    assert lados[nv:] == ["L", "R", "L", "R"]
    W, rho0 = base.matriz(n, aristas)
    pr("MOTIVO neuronas=%d visuales=%d aristas=%d sinapsis=%d inhibitorias=%d ipsilaterales=%d rho_crudo=%.4f" % (
        n, nv, len(aristas), int(sum(abs(w) for _, _, w in aristas)), sum(w < 0 for _, _, w in aristas),
        sum(lados[p] == lados[q] for p, q, _ in aristas), rho0))
    tab = {}
    for p, q, w in aristas:
        c = tab.setdefault((tipos[p], tipos[q]), [0, 0.0])
        c[0] += 1
        c[1] += abs(w)
    for (tp, tq), (na, ns) in sorted(tab.items()):
        pr("TIPOS pre=%s post=%s aristas=%d sinapsis=%d" % (tp, tq, na, int(ns)))

    def cod(i, tipo):
        return (0 if lados[i] == "L" else 1) * 3 + TIPOS.index(tipo)
    idx_W = np.array([cod(i, tipos[i]) for i in range(nv)])

    # nulo SL (funcion de la 003) y nulo T (sintonias barajadas dentro de cada lado, cableado intacto)
    rng = np.random.default_rng(7)
    gi0, go0 = base.grados(n, aristas)
    par0 = sorted((p, q) for p, q, _ in aristas)
    sl, guard_sl = [], True
    for k in range(n_nulo):
        ar = base.barajar_sl(aristas, lados, rng)
        gi, go = base.grados(n, ar)
        ok = bool((gi == gi0).all() and (go == go0).all() and sorted((p, q) for p, q, _ in ar) != par0
                  and all(lados[p] == lados[q] for p, q, _ in ar))
        guard_sl &= ok
        sl.append((ar, base.matriz(n, ar)[0]))
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

    def composicion(ar):
        c = {(d, t): 0.0 for d in DNS for t in TIPOS}
        for p, q, w in ar:
            if tipos[q] in DNS and tipos[p] in TIPOS:
                c[(tipos[q], tipos[p])] += abs(w)
        return c

    def fracs(c, d):
        tot = sum(c[(d, t)] for t in TIPOS)
        return [c[(d, t)] / tot if tot else 0.0 for t in TIPOS]
    cW = composicion(aristas)
    cS = [composicion(ar) for ar, _ in sl]
    for d in DNS:
        fw = fracs(cW, d)
        fs = np.mean([fracs(c, d) for c in cS], axis=0)
        pr("COMPOSICION dn=%s fraccion_de_sinapsis(LC4,LPLC2,LPLC4) W=(%.3f,%.3f,%.3f) SL_media=(%.3f,%.3f,%.3f)" % (
            d, fw[0], fw[1], fw[2], fs[0], fs[1], fs[2]))

    # datos: entrenamiento semilla 1, prueba semilla 2 (como la 003); ruido con numeros comunes
    etr, ete = generar_estimulo(n_train, 1), generar_estimulo(n_test, 2)
    ytr, yte = etr["y"], ete["y"]
    Ztr = np.random.default_rng(101).standard_normal((n_train, T, nv))
    Zte = np.random.default_rng(102).standard_normal((n_test, T, nv))
    maj = {s: int(np.bincount(ytr[etr["vuelo"] == s]).argmax()) for s in (True, False)}
    azar = float((np.where(ete["vuelo"], maj[True], maj[False]) == yte).mean())
    pr("DATOS entrenamiento=%d prueba=%d clases_prueba(nada,esc_izq,esc_der,aterr)=%s azar_mayoria_por_estado=%.4f" % (
        n_train, n_test, ",".join(str(int((yte == k).sum())) for k in range(4)), azar))
    for v in VARIANTES + ("AGNOSTICA",):
        drv = sintonias(etr, v)
        for c, nom in enumerate(ESTIMULOS):
            m = etr["est"] == c
            filas = []
            for k in range(3):
                ch = np.where(etr["lado"][m] == 0, k, 3 + k)
                x = drv[m][np.arange(int(m.sum())), :, ch]
                filas.append((float(x.max(1).mean()), float((x > 0.05).sum(1).mean())))
            pr("ENTRADA variante=%s estimulo=%s pico_medio(LC4,LPLC2,LPLC4)=(%.3f,%.3f,%.3f) pasos_activos=(%.1f,%.1f,%.1f)" % (
                v, nom, filas[0][0], filas[1][0], filas[2][0], filas[0][1], filas[1][1], filas[2][1]))

    def prep(variante, sigma):
        """Entrenamiento y prueba juntos en una sola simulacion (filas independientes)."""
        drive = np.concatenate([sintonias(etr, variante), sintonias(ete, variante)])
        return dict(y=np.concatenate([ytr, yte]), drive=drive, ruido=sigma * np.concatenate([Ztr, Zte]))

    def dn_rasgos(Wm, tau, idx, d):
        out = base.simular(Wm, tau, idx, d).reshape(n_train + n_test, -1)
        return out[:n_train], out[n_train:]

    def pred_ridge(Wm, tau, idx, d):
        Ftr, Fte = dn_rasgos(Wm, tau, idx, d)
        return ridge_mux(Ftr, ytr, etr["vuelo"], Fte, ete["vuelo"])[0]

    def acc(p):
        return float((p == yte).mean())

    def celda(variante, sigma, tau, m, etiqueta):
        tc = time.time()
        d = prep(variante, sigma)
        pW = pred_ridge(W, tau, idx_W, d)
        aW = acc(pW)
        a_sl = [acc(pred_ridge(Ws, tau, idx_W, d)) for _, Ws in sl[:m]]
        a_t = [acc(pred_ridge(W, tau, ix, d)) for ix in perms[:m]]
        ps_sl, pi_sl = p_rango(aW, a_sl)
        ps_t, pi_t = p_rango(aW, a_t)
        por = [float((pW[yte == k] == k).mean()) for k in range(4)]
        r = dict(W=aW, por_clase=por, SL=a_sl, T=a_t, p_sup_SL=ps_sl, p_inf_SL=pi_sl, p_sup_T=ps_t,
                 p_inf_T=pi_t, dur_s=time.time() - tc)
        pr("CELDA %s variante=%s ruido=%.2f W=%.4f por_clase(nada,esc_izq,esc_der,aterr)=%s | SL media=%.4f max=%.4f "
           "igualan=%d/%d p_sup=%.4f p_inf=%.4f | T media=%.4f max=%.4f igualan=%d/%d p_sup=%.4f p_inf=%.4f | %.1f s" % (
               etiqueta, variante, sigma, aW, ",".join("%.3f" % x for x in por), np.mean(a_sl), np.max(a_sl),
               sum(x >= aW for x in a_sl), m, ps_sl, pi_sl, np.mean(a_t), np.max(a_t), sum(x >= aW for x in a_t), m,
               ps_t, pi_t, r["dur_s"]))
        return r, pW

    res = {"parte": a.parte, "humo": humo, "guarda_SL": guard_sl, "guarda_T": guard_t, "azar": azar}
    if a.parte == "A":
        tau0 = 0.06 + 0.12 * np.random.default_rng(0).random(n)
        prim, pW_c = {}, {}
        for v in VARIANTES:
            for s in RUIDOS:
                prim[(v, s)], pW_c[(v, s)] = celda(v, s, tau0, n_nulo, "PRIMARIA tau_semilla=0")
        claves = [(v, s, nul) for v in VARIANTES for s in RUIDOS for nul in ("SL", "T")]
        adj_sup = holm([prim[(v, s)]["p_sup_" + nul] for v, s, nul in claves])
        adj_inf = holm([prim[(v, s)]["p_inf_" + nul] for v, s, nul in claves])
        for (v, s, nul), x, y_ in zip(claves, adj_sup, adj_inf):
            prim[(v, s)]["holm_sup_" + nul] = float(x)
            prim[(v, s)]["holm_inf_" + nul] = float(y_)

        # controles del instrumento
        d = prep("COMO_LPLC2", 0.15)
        todo = simular_todo(W, tau0, idx_W, d)
        paridad = bool(np.array_equal(todo[:, :, nv:nv + 4], base.simular(W, tau0, idx_W, d)))
        del todo
        repro = bool(np.array_equal(pred_ridge(W, tau0, idx_W, d), pW_c[("COMO_LPLC2", 0.15)]))
        dA = prep("AGNOSTICA", 0.15)
        pA = pred_ridge(W, tau0, idx_W, dA)
        iguales = [bool(np.array_equal(pred_ridge(W, tau0, ix, dA), pA)) for ix in perms[:n_agn]]
        c_neg = all(iguales)
        aA = acc(pA)
        a_sl_A = [acc(pred_ridge(Ws, tau0, idx_W, dA)) for _, Ws in sl[:n_rob]]
        psA, piA = p_rango(aA, a_sl_A)
        pr("CONTROL_NEGATIVO entrada=AGNOSTICA W=%.4f T_identicos=%d/%d -> %s | SL descriptivo (como la 003) media=%.4f "
           "max=%.4f igualan=%d/%d p_sup=%.4f p_inf=%.4f" % (aA, sum(iguales), len(iguales), c_neg, np.mean(a_sl_A),
                                                             np.max(a_sl_A), sum(x >= aA for x in a_sl_A), len(a_sl_A), psA, piA))
        res["agnostica"] = dict(W=aA, T_identicos=sum(iguales), n_T=len(iguales), SL=a_sl_A, p_sup_SL=psA, p_inf_SL=piA)

        # control positivo (28 estados) y rivales clasicos (24 entradas crudas)
        riv = {}
        for v in VARIANTES:
            for s in RUIDOS:
                d = prep(v, s)
                todo = simular_todo(W, tau0, idx_W, d).reshape(n_train + n_test, -1)
                p28 = ridge_mux(todo[:n_train], ytr, etr["vuelo"], todo[n_train:], ete["vuelo"])[0]
                del todo
                X = (d["drive"][:, :, idx_W] + d["ruido"]).reshape(n_train + n_test, -1)
                pRL = ridge_mux(X[:n_train], ytr, etr["vuelo"], X[n_train:], ete["vuelo"])[0]
                pRM = mlp_mux(X[:n_train], ytr, etr["vuelo"], X[n_train:], ete["vuelo"], 0, it_mlp)
                del X
                pW = pW_c[(v, s)]
                b1, c1, p1 = base.mcnemar(pW == yte, pRL == yte)
                h3 = "MEJOR" if (b1 > c1 and p1 < ALFA) else ("PEOR" if (c1 > b1 and p1 < ALFA) else "EMPATE")
                riv[(v, s)] = dict(control_positivo_28=acc(p28), rival_ridge_crudo=acc(pRL), rival_mlp_crudo=acc(pRM),
                                   H3_gana_W=b1, H3_gana_rival=c1, H3_p=p1, H3=h3)
                pr("RIVAL variante=%s ruido=%.2f W_ridge_4DN=%.4f control_positivo_ridge_28=%.4f rival_ridge_crudo_24=%.4f "
                   "rival_mlp_crudo_24=%.4f | H3 W contra ridge crudo %d contra %d p=%.3g -> %s" % (
                       v, s, acc(pW), acc(p28), acc(pRL), acc(pRM), b1, c1, p1, h3))

        c_pos = all(riv[(v, 0.15)]["control_positivo_28"] >= C_POS for v in VARIANTES)
        valido = bool(guard_sl and guard_t and paridad and repro and c_neg and c_pos)
        pr("CHEQUEO INSTRUMENTO guarda_SL=%s guarda_T=%s paridad_simulacion=%s reproduce_ridge=%s "
           "control_negativo(T identico con entrada AGNOSTICA)=%s control_positivo(ridge 28 estados >= %.2f con ruido "
           "0.15)=%s -> %s" % (guard_sl, guard_t, paridad, repro, c_neg, C_POS, c_pos,
                               "VALIDO" if valido else "INVALIDO"))

        ver_v = {}
        for v in VARIANTES:
            vc = []
            for s in RUIDOS:
                c = prim[(v, s)]
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
                pr("VEREDICTO_CELDA variante=%s ruido=%.2f holm_sup(SL,T)=(%.4f,%.4f) holm_inf(SL,T)=(%.4f,%.4f) -> %s" % (
                    v, s, c["holm_sup_SL"], c["holm_sup_T"], c["holm_inf_SL"], c["holm_inf_T"], x))
            ver_v[v] = "GANA" if all(x == "GANA" for x in vc) else ("PIERDE" if "PIERDE" in vc else "EMPATE")
            pr("VEREDICTO_VARIANTE %s -> %s" % (v, ver_v[v]))
        ng = sum(x == "GANA" for x in ver_v.values())
        glob = "PAGA EL CABLEADO POR TIPOS" if ng == len(VARIANTES) else ("DEPENDE DE LPLC4" if ng else "NO PAGA")
        pierde = [v for v in VARIANTES if ver_v[v] == "PIERDE"]
        if pierde:
            glob += " (PIERDE en %s)" % ",".join(pierde)
        pr("VEREDICTO_GLOBAL -> %s" % glob)
        pr("BYTES lector_ridge_4DN=%d floats lector_ridge_crudo_24=%d floats motivo=%d tau y %d aristas" % (
            (4 * T + 1) * 7, (nv * T + 1) * 7, n, len(aristas)))
        res.update(primaria={"%s|%.2f" % k: x for k, x in prim.items()},
                   rivales={"%s|%.2f" % k: x for k, x in riv.items()},
                   controles=dict(paridad=paridad, reproduce_ridge=repro,
                                  control_negativo=c_neg, control_positivo=c_pos),
                   veredicto_variante=ver_v, veredicto_global=glob, valido=valido)
    elif a.parte == "C":
        grilla = (0.15, 0.30, 0.45, 0.60, 0.90, 1.20)
        medias = {}
        for s in grilla:
            accs = []
            for v in VARIANTES:
                d = prep(v, s)
                X = (d["drive"][:, :, idx_W] + d["ruido"]).reshape(n_train + n_test, -1)
                accs.append(acc(ridge_mux(X[:n_train], ytr, etr["vuelo"], X[n_train:], ete["vuelo"])[0]))
                del X
            medias[s] = float(np.mean(accs))
            pr("CALIBRACION ruido=%.2f rival_ridge_crudo(COMO_LPLC2,SILENCIOSA,MOVIMIENTO)=(%.4f,%.4f,%.4f) media=%.4f" % (
                s, accs[0], accs[1], accs[2], medias[s]))
        ok = [s for s in grilla if medias[s] >= 0.90]
        elegido = max(ok) if ok else grilla[0]
        pr("CALIBRACION ruido_dificil=%.2f (el mas alto de la grilla con rival ridge crudo medio >= 0.90)" % elegido)
        res.update(calibracion={"%.2f" % k: x for k, x in medias.items()}, ruido_dificil=elegido)
        valido = True
    else:
        rob = {}
        for st in SEMILLAS_TAU_ROB:
            tau = 0.06 + 0.12 * np.random.default_rng(st).random(n)
            for v in VARIANTES:
                for s in RUIDOS:
                    rob["%d|%s|%.2f" % (st, v, s)] = celda(v, s, tau, n_rob, "ROBUSTEZ tau_semilla=%d" % st)[0]
        tau0 = 0.06 + 0.12 * np.random.default_rng(0).random(n)
        # I2: MLP sobre las 4 descendentes, ruido 0.15, tau semilla 0
        mlp, repro_mlp = {}, True
        for v in VARIANTES:
            tc = time.time()
            d = prep(v, 0.15)
            Ftr, Fte = dn_rasgos(W, tau0, idx_W, d)
            aW, p0 = [], None
            for sd in SEMILLAS_MLP_W:
                p = mlp_mux(Ftr, ytr, etr["vuelo"], Fte, ete["vuelo"], sd, it_mlp)
                aW.append(acc(p))
                if sd == SEMILLAS_MLP_W[0]:
                    p0 = p
            repro_mlp &= bool(np.array_equal(mlp_mux(Ftr, ytr, etr["vuelo"], Fte, ete["vuelo"], SEMILLAS_MLP_W[0], it_mlp), p0))
            a_sl, a_t = [], []
            for k in range(n_mlp):
                Ftr, Fte = dn_rasgos(sl[k][1], tau0, idx_W, d)
                a_sl.append(acc(mlp_mux(Ftr, ytr, etr["vuelo"], Fte, ete["vuelo"], 100 + k, it_mlp)))
                Ftr, Fte = dn_rasgos(W, tau0, perms[k], d)
                a_t.append(acc(mlp_mux(Ftr, ytr, etr["vuelo"], Fte, ete["vuelo"], 200 + k, it_mlp)))
            ps_sl, pi_sl = p_rango(aW[0], a_sl)
            ps_t, pi_t = p_rango(aW[0], a_t)
            mlp[v] = dict(W=aW, SL=a_sl, T=a_t, p_sup_SL=ps_sl, p_inf_SL=pi_sl, p_sup_T=ps_t, p_inf_T=pi_t)
            pr("I2_MLP variante=%s ruido=0.15 W(semillas 0,1,2)=%s | SL media=%.4f max=%.4f igualan_W0=%d/%d p_sup=%.4f "
               "p_inf=%.4f | T media=%.4f max=%.4f igualan_W0=%d/%d p_sup=%.4f p_inf=%.4f | %.1f s" % (
                   v, ",".join("%.4f" % x for x in aW), np.mean(a_sl), np.max(a_sl), sum(x >= aW[0] for x in a_sl),
                   n_mlp, ps_sl, pi_sl, np.mean(a_t), np.max(a_t), sum(x >= aW[0] for x in a_t), n_mlp, ps_t, pi_t,
                   time.time() - tc))

        valido = bool(guard_sl and guard_t and repro_mlp)
        pr("CHEQUEO INSTRUMENTO (parte B, descriptiva) guarda_SL=%s guarda_T=%s reproduce_mlp=%s -> %s" % (
            guard_sl, guard_t, repro_mlp, "VALIDO" if valido else "INVALIDO"))
        res.update(robustez=rob, i2_mlp=mlp, valido=valido)
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
