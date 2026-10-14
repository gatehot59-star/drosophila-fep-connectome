#!/usr/bin/env python3
"""Tarea de la barra segun su direccion (respuesta 2026-10-14-012, paso A del sello de H_TOPO_NUEVO).

Se escribe y se commitea ANTES del programa Topo nuevo y antes de cualquier corrida del banco con esta tarea.
Extiende la tarea sellada de la 2026-10-12-015 (tarea_mosca.py, md5 40d64e07) con una sexta clase de estimulo:
la barra oscura que va de ATRAS HACIA ADELANTE (BARRA_AD). La barra de la 015 va de adelante hacia atras (BARRA_AA).

Etiquetas (24 condiciones balanceadas: estado x 6 estimulos x lado):
  posada: LOOM_LATERAL o LOOM_FRONTAL -> despegar; PUNTO, BARRA_AA, BARRA_AD, NADA -> nada (como en la 015).
  vuelo:  LOOM_FRONTAL o BARRA_AA -> aterrizar (Ache 2019, Nat Neurosci, como en la 015).
          LOOM_LATERAL o PUNTO -> girar alejandose (Kim 2023, como en la 015).
          BARRA_AD -> girar alejandose. NUEVA. Fuentes: Ache 2019, Supp Fig 5d (las descendentes de aterrizaje
          DNp07 y DNp10 responden mas a la barra de adelante hacia atras; otras direcciones son menos efectivas) y
          Kim 2023 (LPLC2 y DNp06 median giros evasivos ante objetos que se mueven de costado; DNp06 es selectivo a
          la direccion de la barra, como LPLC2). La conducta exacta ante BARRA_AD en vuelo no esta medida como numero
          en lo leido: es etiqueta de trabajo con fuente indirecta, declarada.

Modelo de entrada nuevo para las barras (supuestos declarados, no numeros medidos):
  LPLC2: responde a la barra con la misma amplitud A de la celda que al punto; mas a la de atras hacia adelante
         (1) que a la de adelante hacia atras (F_DIR = 0,5, la constante de la 015). Kim 2023: "LPLC2 neurons also
         exhibit stronger responses to back-to-front motion than to front-to-back motion for both bars and spots".
  LPLC1: responde a la barra de atras hacia adelante (1) mas que a la de adelante hacia atras (F_DIR). Kim 2023,
         citando su ref. 34: "LPLC1 neurons responded more strongly to the back-to-front motion".
  LPLC4: responde a la barra de adelante hacia atras (1, como en la 015) y menos a la de atras hacia adelante
         (F4_AD = 0,3). Inferido de la sintonia de DNp07, cuya primera entrada es LPLC4 (2026-10-12-014).
  LC4:   igual que con el punto (F_LC4_PUNTO = 0,1), sin direccion.
Con bar_lplc=False y sin barras AD, sintonias() da exactamente lo mismo que tarea_mosca.sintonias (chequeo).
"""
import os
import sys

import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(AQUI), "escape_aterrizaje"))
import tarea_mosca as tm  # noqa: E402

T = tm.T
ESTIMULOS = ("LOOM_LATERAL", "LOOM_FRONTAL", "PUNTO", "BARRA_AA", "NADA", "BARRA_AD")
F4_AD = 0.3
N_COND = 24


def generar(n, seed):
    """Como tarea_mosca.generar, con 6 estimulos (est 0 a 5; 4 es NADA y 5 es BARRA_AD)."""
    rng = np.random.default_rng(seed)
    cond = np.arange(n) % N_COND
    rng.shuffle(cond)
    vuelo = cond < N_COND // 2
    est = (cond % (N_COND // 2)) // 2
    lado = cond % 2
    direc = np.zeros(n, dtype=int)
    th = np.zeros((n, T))
    thd = np.zeros((n, T))
    punto = np.zeros((n, T))
    barra = np.zeros((n, T))
    barra_ad = np.zeros((n, T))
    tt = np.arange(T).astype(float)
    for i in range(n):
        te = int(rng.integers(26, 35))
        t_on = te - int(rng.integers(12, 21))
        vis = (tt >= t_on) & (tt <= te)
        if est[i] <= 1:
            r = rng.uniform(0.5, 4.0)
            tc = te + r / np.tan(np.radians(tm.TH_MAX / 2.0))
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
        elif est[i] == 5:
            barra_ad[i] = np.where(vis, rng.uniform(0.4, 1.0), 0.0)
            direc[i] = 1
    y = np.zeros(n, dtype=int)
    y[~vuelo & (est <= 1)] = 1
    y[vuelo & ((est == 1) | (est == 3))] = 2
    gira = vuelo & ((est == 0) | (est == 2) | (est == 5))
    y[gira] = 3 + lado[gira]
    return dict(y=y, vuelo=vuelo, est=est, lado=lado, direc=direc, th=th, thd=thd, punto=punto, barra=barra,
                barra_ad=barra_ad)


def sintonias(e, A, bar_lplc=True):
    """Entrada (n, T, 2 * NT), canal = lado * NT + tipo (LC4, LPLC2, LPLC4, LPLC1), como tarea_mosca.sintonias."""
    expande = e["thd"] > 0.05
    g = np.exp(-((e["th"] - tm.TH_P) ** 2) / (2.0 * tm.TH_S ** 2))
    vel = np.clip(e["thd"] / tm.V_REF, 0.0, 1.0)
    pu, ba = e["punto"], e["barra"]
    bd = e["barra_ad"] if "barra_ad" in e else np.zeros_like(pu)
    d = np.where(e["direc"] == 1, 1.0, tm.F_DIR)[:, None]
    frontal = (e["est"] == 1)[:, None]
    lc4 = vel + tm.F_LC4_PUNTO * (pu + ba + bd)
    lplc2 = np.where(expande, g, 0.0) + A * d * pu
    lplc1 = pu.copy()
    if bar_lplc:
        lplc2 = lplc2 + A * (bd + tm.F_DIR * ba)
        lplc1 = lplc1 + (bd + tm.F_DIR * ba)
    lplc4 = ba + F4_AD * bd + tm.F4_PUNTO * pu * (e["direc"] == -1)[:, None] + vel * np.where(frontal, 1.0, tm.F4_LAT)
    us = [lc4, lplc2, lplc4, lplc1]
    n = len(e["y"])
    en_lado = np.stack([(e["lado"] == s) | (e["est"] == 1) for s in (0, 1)], axis=1)
    drive = np.zeros((n, T, 2 * tm.NT))
    for k, u in enumerate(us):
        for s in (0, 1):
            drive[:, :, s * tm.NT + k] = np.where(en_lado[:, s][:, None], u, 0.0)
    return drive


def chequeos():
    ok = True
    e15 = tm.generar(400, 3)
    for A in tm.AMPLITUDES:
        dif = float(np.abs(tm.sintonias(e15, A) - sintonias(e15, A, bar_lplc=False)).max())
        print("CHEQUEO SINTONIAS_015_IGUAL A=%.1f max_dif=%.3g -> %s" % (A, dif, dif == 0.0))
        ok = ok and dif == 0.0
    e = generar(2400, 1)
    nombres = ("nada", "despegar", "aterrizar", "girar_der", "girar_izq")
    cuenta = ",".join("%s=%d" % (nombres[k], int((e["y"] == k).sum())) for k in range(5))
    por_cond = np.bincount(e["vuelo"].astype(int) * 12 + e["est"] * 2 + e["lado"], minlength=24)
    bal = bool(por_cond.min() == por_cond.max() == 100)
    print("CHEQUEO CLASES %s condiciones_por_celda=%d..%d balanceado=%s" % (cuenta, por_cond.min(), por_cond.max(), bal))
    ok = ok and bal
    dr = sintonias(e, 0.3)
    pico = dr.max(axis=1)
    v = e["vuelo"]
    for k, tipo in enumerate(tm.TIPOS):
        canal = e["lado"] * tm.NT + k
        p = pico[np.arange(len(canal)), canal]
        aa = float(p[v & (e["est"] == 3)].mean())
        ad = float(p[v & (e["est"] == 5)].mean())
        print("DIRECCION A=0.3 tipo=%s barra_AA=%.4f barra_AD=%.4f" % (tipo, aa, ad))
        if tipo == "LPLC4":
            ok = ok and aa > ad
        if tipo in ("LPLC1", "LPLC2"):
            ok = ok and ad > aa
    print("VEREDICTO_TAREA -> %s" % ("VALIDA" if ok else "INVALIDA"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(chequeos())
