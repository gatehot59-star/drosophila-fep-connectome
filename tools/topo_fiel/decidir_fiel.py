#!/usr/bin/env python3
"""Regla de decision de H_TOPO_FIEL (respuesta 2026-10-14-021, paso B del sello). Sin torch, para poder probarla sola.

conteos: una fila por celda, [ensayos donde el programa A falla y B acierta, ensayos iguales, A acierta y B falla].
d = (sum mas - sum menos) / total = acierto A - acierto B en los mismos ensayos.
IC90 por bootstrap estratificado por celda (multinomial por celda, como banco_barra_dir.py de la 012).
No inferioridad con margen M: SOSTENIDA si el limite inferior > -M; REFUTADA si el superior < -M; si no, SIN_DECIDIR.
"""
import numpy as np

MARGEN = 0.01


def decidir(conteos, b, semilla, margen=MARGEN):
    rb = np.random.default_rng(semilla)
    tot = float(sum(sum(x) for x in conteos))
    if tot <= 0:
        raise ValueError("sin ensayos")
    suma = np.zeros(b)
    obs = 0.0
    for cm, c0, cp in conteos:
        m = cm + c0 + cp
        if m == 0:
            continue
        obs += cp - cm
        draw = rb.multinomial(m, [cm / m, c0 / m, cp / m], size=b)
        suma += draw[:, 2] - draw[:, 0]
    d = obs / tot
    lo, hi = np.quantile(suma / tot, [0.05, 0.95])
    if lo > -margen:
        v = "SOSTENIDA"
    elif hi < -margen:
        v = "REFUTADA"
    else:
        v = "SIN_DECIDIR"
    return dict(d=float(d), ic90=[float(lo), float(hi)], veredicto=v)


def contar(ca, cb):
    """ca, cb: aciertos booleanos de A y B en los mismos ensayos. Devuelve [menos, iguales, mas]."""
    dd = np.asarray(ca).astype(int) - np.asarray(cb).astype(int)
    return [int((dd == -1).sum()), int((dd == 0).sum()), int((dd == 1).sum())]


def final(h_fiel, h_control):
    """El control cruzado tiene que salir REFUTADA; si no, el banco no puede dar rojo y nada vale."""
    if h_control != "REFUTADA":
        return "INVALIDO"
    return h_fiel
