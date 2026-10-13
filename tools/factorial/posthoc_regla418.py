#!/usr/bin/env python3
"""Chequeo POST-HOC de la 2026-10-13-002 (no sellado): la regla a mano con las mismas 418 entradas de R1.

En el factorial sellado la regla usa las 40 entradas de la 015 y R1 recibe 418 neuronas sintonizadas, cada una con
su ruido independiente. Si R1 le gana a la regla solo por promediar mas sensores, la regla sobre las 418 entradas
tiene que alcanzarlo. Mismos datos, mismas semillas (101/102 y 103/104), mismo lector y umbrales de la 015.
Primero reproduce la regla de 40 contra el json (guarda), despues compara W de R1 contra la regla de 418.
"""
import json
import os
import sys

import numpy as np

F = "/workspace/tm_2026-10-12/clon_fact_res"
sys.path.insert(0, F + "/tools/factorial")
sys.path.insert(0, F + "/tools/escape_aterrizaje")
import factorial_mosca as fm  # noqa: E402

tm, base, ept = fm.tm, fm.base, fm.ept
S = fm.sujeto("/workspace/connectivity.parquet", "/workspace/annotations.tsv", "R1", "CON")
tipos, lados, n_ent, nv46 = S["tipos"], S["lados"], S["n_ent"], S["nv46"]
chan = np.array([(0 if lados[i] == "L" else 1) * tm.NT + tm.TIPOS.index(tipos[i]) for i in range(n_ent)])
etr, ete = tm.generar(tm.N_TRAIN, 1), tm.generar(tm.N_TEST, 2)
ytr, yte, vtr, vte = etr["y"], ete["y"], etr["vuelo"], ete["vuelo"]
Ztr = np.concatenate([np.random.default_rng(101).standard_normal((tm.N_TRAIN, tm.T, nv46)),
                      np.random.default_rng(103).standard_normal((tm.N_TRAIN, tm.T, n_ent - nv46))], axis=2)
Zte = np.concatenate([np.random.default_rng(102).standard_normal((tm.N_TEST, tm.T, nv46)),
                      np.random.default_rng(104).standard_normal((tm.N_TEST, tm.T, n_ent - nv46))], axis=2)
print("SUJETO R1 con_entrada=%d (de la 015: %d)" % (n_ent, nv46), flush=True)


def regla(dtr, dte, k):
    def media(X, ld, ts):
        m = np.array([lados[i] == ld and tipos[i] in ts for i in range(k)])
        return X[:, :, m].mean(2)

    def lc(d):
        X = d["drive"][:, :, chan[:k]] + d["ruido"][:, :, :k]
        return np.stack([media(X, "L", ("LC4", "LPLC2")), media(X, "R", ("LC4", "LPLC2")),
                         media(X, "L", ("LPLC4",)), media(X, "R", ("LPLC4",)),
                         media(X, "L", ("LPLC1", "LPLC2")), media(X, "R", ("LPLC1", "LPLC2"))], axis=2)
    th = tm.umbrales(tm.lineas(lc(dtr)), ytr, vtr)
    return tm.carrera(tm.lineas(lc(dte)), th, vte)


R = {}
for c in ("R1_CON_TASA", "R1_CON_LIQ", "R1_SIN_LIQ"):
    with open(os.path.join(F, "results/factorial_2026-10-13/factorial_%s.json" % c)) as f:
        R[c] = json.load(f)
ps = {c: [] for c in R}
guarda = True
for A, s in fm.CELDAS:
    key = "%.1f|%.2f" % (A, s)
    dtr = dict(y=ytr, drive=tm.sintonias(etr, A), ruido=s * Ztr)
    dte = dict(y=yte, drive=tm.sintonias(ete, A), ruido=s * Zte)
    p40, p418 = regla(dtr, dte, nv46), regla(dtr, dte, n_ent)
    a40, a418 = float((p40 == yte).mean()), float((p418 == yte).mean())
    g = abs(a40 - R["R1_CON_TASA"]["celdas"][key]["regla"]) < 1e-12
    guarda &= g
    linea = "CELDA A=%.1f ruido=%.2f regla40=%.4f (json %.4f, igual=%s) regla418=%.4f" % (
        A, s, a40, R["R1_CON_TASA"]["celdas"][key]["regla"], g, a418)
    for c in R:
        pW = np.array(R[c]["celdas"][key]["pred_W"])
        b, cc, p = base.mcnemar(pW == yte, p418 == yte)
        ps[c].append((b, cc, p))
        linea += " | %s W=%.4f %d/%d p=%.3g" % (c, R[c]["celdas"][key]["W"], b, cc, p)
    print(linea, flush=True)
for c in R:
    adj = ept.holm([x[2] for x in ps[c]])
    cl = ["MEJOR" if b > cc and a < 0.05 else ("PEOR" if cc > b and a < 0.05 else "EMPATE") for (b, cc, _), a in zip(ps[c], adj)]
    v = "PIERDE" if "PEOR" in cl else ("SUPERA" if "MEJOR" in cl else "IGUALA")
    print("POSTHOC %s contra regla418: %s -> %s" % (c, ",".join("%s(%.3g)" % t for t in zip(cl, adj)), v), flush=True)
print("CHEQUEO regla40_reproduce_json=%s" % guarda)
