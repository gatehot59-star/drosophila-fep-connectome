"""Relectura del factorial 4 desde git, sin los json de Kaggle (post-hoc, no sellado).

Lee results/factorial4_2026-10-13/corridas.csv y nulos.csv, recalcula la primaria, la escala y los nulos con las
funciones selladas de tools/factorial4/agregar_factorial4.py (md5 96396793, mismas semillas 2026 y 2027) y compara
cada linea con results/factorial4_2026-10-13/agregado.log. Si coinciden, la lectura del factorial 4 se recomputa desde
git sin bajar nada de Kaggle. Despues imprime tablas por semilla de tau y por prueba que el plan sellado no pedia: son
descriptivas y no deciden ninguna hipotesis.

Uso, desde la raiz del repo: python3 tools/factorial4/releer_factorial4_desde_csv.py
Sale con 0 solo si el agregador tiene su md5 sellado y todas las lineas recomputadas estan en agregado.log.
"""
import csv
import hashlib
import importlib.util
import os
import sys

import numpy as np

RES = os.path.join("results", "factorial4_2026-10-13")
AGR = os.path.join("tools", "factorial4", "agregar_factorial4.py")
MD5_AGR = "96396793da55400d5a1328e3877c9e2a"
CELDA_NULOS, TAU_NULOS, PRUEBA_NULOS = "0.3|0.15", 0, 2


def md5(p):
    with open(p, "rb") as f:
        return hashlib.md5(f.read()).hexdigest()


def holm(ps):
    orden = sorted(ps, key=lambda k: ps[k])
    m, prev, out = len(orden), 0.0, {}
    for i, k in enumerate(orden):
        prev = max(prev, min(1.0, (m - i) * ps[k]))
        out[k] = prev
    return out


def main():
    m_agr = md5(AGR)
    ok_agr = m_agr == MD5_AGR
    print("CHEQUEO AGREGADOR_SELLADO md5=%s -> %s" % (m_agr[:8], ok_agr))
    spec = importlib.util.spec_from_file_location("agregar_factorial4", AGR)
    agr = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(agr)
    filas = list(csv.DictReader(open(os.path.join(RES, "corridas.csv"))))
    taus = sorted({int(r["tau"]) for r in filas})
    pruebas = sorted({int(r["prueba"]) for r in filas})
    celdas = sorted({r["celda"] for r in filas}, key=lambda c: tuple(float(x) for x in c.split("|")))
    F = {(int(r["tau"]), int(r["prueba"]), r["celda"]): r for r in filas}
    print("CSV corridas=%d unicas=%d taus=%d pruebas=%d celdas=%d B=%d" % (
        len(filas), len(F), len(taus), len(pruebas), len(celdas), agr.B))

    def cubo(f):
        return np.array([[[f(F[(t, p, c)]) for c in celdas] for p in pruebas] for t in taus])

    w_ce = cubo(lambda r: float(r["W_CE"]))
    w_r2 = cubo(lambda r: float(r["W_R2"]))
    regla = cubo(lambda r: float(r["regla_propia"]))
    D, E, D2 = w_ce - regla, w_ce - w_r2, w_r2 - regla
    lineas = []
    rng = np.random.default_rng(2026)
    est, lo, hi = agr.bootstrap(D.mean(2), 0.05, rng)
    lineas.append("PRIMARIA CE_CON_TASA W=%.4f regla_propia=%.4f dif=%+.4f IC90=[%+.4f, %+.4f] corridas=%d -> %s" % (
        w_ce.mean(), regla.mean(), est, lo, hi, D.size, agr.veredicto(lo, hi)))
    for j, c in enumerate(celdas):
        e2, l2, h2 = agr.bootstrap(D[:, :, j], 0.05 / 6, rng)
        lineas.append("  CELDA %s dif=%+.4f IC=[%+.4f, %+.4f] -> %s" % (c, e2, l2, h2, agr.veredicto(l2, h2)))
    rng_e = np.random.default_rng(2027)
    est_e, lo_e, hi_e = agr.bootstrap(E.mean(2), 0.05, rng_e)
    lineas.append("ESCALA CE_menos_R2 W_CE=%.4f W_R2=%.4f dif=%+.4f IC90=[%+.4f, %+.4f] corridas=%d -> %s" % (
        w_ce.mean(), w_r2.mean(), est_e, lo_e, hi_e, E.size, agr.veredicto(lo_e, hi_e)))
    for j, c in enumerate(celdas):
        e2, l2, h2 = agr.bootstrap(E[:, :, j], 0.05 / 6, rng_e)
        lineas.append("  CELDA %s dif=%+.4f IC=[%+.4f, %+.4f] -> %s" % (c, e2, l2, h2, agr.veredicto(l2, h2)))
    lineas.append("ESCALA corridas CE>R2=%d iguales=%d CE<R2=%d" % (
        int((E > 0).sum()), int((E == 0).sum()), int((E < 0).sum())))
    real = float(F[(TAU_NULOS, PRUEBA_NULOS, CELDA_NULOS)]["W_CE"])
    nulos = list(csv.DictReader(open(os.path.join(RES, "nulos.csv"))))
    ps = {}
    for t in ("SL", "T"):
        acc = np.array([float(r["acierto"]) for r in nulos if r["tipo"] == t])
        k = int((acc >= real).sum())
        ps[t] = (1 + k) / (len(acc) + 1)
        lineas.append("NULOS %s n=%d media=%.4f max=%.4f W=%.4f iguales_o_mejores=%d p_sup=%.4f" % (
            t, len(acc), acc.mean(), acc.max(), real, k, ps[t]))
    hb = holm(ps)
    lineas.append("NULOS Holm SL=%.4f T=%.4f" % (hb["SL"], hb["T"]))
    log = open(os.path.join(RES, "agregado.log")).read().splitlines()
    iguales = 0
    for x in lineas:
        ok = x in log
        iguales += ok
        print("%s %s" % ("IGUAL" if ok else "DISTINTA", x))
    todo = ok_agr and iguales == len(lineas)
    print("CHEQUEO RECOMPUTA_DESDE_CSV lineas=%d iguales=%d -> %s" % (len(lineas), iguales, todo))
    print("# POSTHOC: no estaba en el plan sellado; describe, no decide")
    for i, t in enumerate(taus):
        print("POSTHOC TAU %d CE-regla=%+.4f R2-regla=%+.4f CE-R2=%+.4f CE>regla=%d/%d" % (
            t, D[i].mean(), D2[i].mean(), E[i].mean(), int((D[i] > 0).sum()), D[i].size))
    for i, p in enumerate(pruebas):
        print("POSTHOC PRUEBA %d CE-regla=%+.4f CE>regla=%d/%d" % (
            p, D[:, i].mean(), int((D[:, i] > 0).sum()), D[:, i].size))
    print("POSTHOC corridas CE>regla=%d iguales=%d CE<regla=%d" % (
        int((D > 0).sum()), int((D == 0).sum()), int((D < 0).sum())))
    gana = [i for i in range(len(taus)) if D[i].mean() > 0]
    otros = [i for i in range(len(taus)) if i not in gana]
    print("POSTHOC taus con CE-regla>0: %d de %d; media en esos=%+.4f; en los otros=%s" % (
        len(gana), len(taus), D[gana].mean(), ("%+.4f" % D[otros].mean()) if otros else "ninguno"))
    print("EXIT_RELECTURA=%d" % (0 if todo else 1))
    return 0 if todo else 1


if __name__ == "__main__":
    sys.exit(main())
