#!/usr/bin/env python3
"""Agregador del factorial 3 de la mosca: R2 con 10 x 10 semillas y sus barajados (respuesta 2026-10-13-008).
Sellado antes de correr.

Uso: python3 agregar_factorial3.py <carpeta del factorial 3> <carpeta del factorial 2> [--humo]

Primaria (una sola configuracion, R2_CON_TASA, sin correccion entre configuraciones):
  d = acierto de W menos acierto de la regla propia (las 564 entradas sintonizadas de R2), por semilla de tau (0..9),
  semilla de prueba (2..11) y celda (6). Estimador: la media. Intervalo: bootstrap de dos vias (tau y prueba por
  separado), B = 20.000, semilla 2026, percentiles 0,05 y 0,95 (TOST al 5 % por lado). Margen M = 0,01, el mismo del
  factorial 2. Veredictos: SUPERA si lo > +M; PIERDE si hi < -M; EQUIVALENTE si -M < lo y hi < +M; NO_INFERIOR si
  lo > -M y hi >= +M; NO_SUPERIOR si hi < +M y lo <= -M; INDETERMINADO si no. Por celda, descriptivo, con 0,05/6.
Nulos (secundaria confirmatoria): en la celda A 0,3 ruido 0,15, tau 0, prueba 2, el acierto de W (de la grilla)
  contra 50 SL y 50 T; p = (1 + #nulos >= W) / (N + 1); Holm sobre los dos.
Hipotesis pre-registradas:
  H_SUPERA_R2 "R2 le gana a su diseno por mas de un punto": SOSTENIDA si SUPERA; REFUTADA si hi < +M (EQUIVALENTE,
    NO_SUPERIOR o PIERDE); SIN_DECIDIR si no.
  H_CABLEADO_R2 "lo que paga es el cableado real": SOSTENIDA si los dos p ajustados por Holm son < 0,05; si no, NO
    SOSTENIDA.
Controles: ANCLA_015 valido y exacto; todos los json validos; plan completo (600 corridas y 50 + 50 nulos con k
  distintos); TAU_DN_IGUAL entre trabajos; REPRODUCE_F2: las 90 corridas que comparte con el factorial 2 (tau 0..2,
  prueba 2..6) dan el mismo acierto de W y de la regla con tolerancia 0,001 (se informa tambien si son exactas);
  REAL_IGUAL: el acierto real medido por el script de nulos coincide con el de la grilla (tolerancia 0,001).
"""
import glob
import json
import os
import sys

import numpy as np

M, B = 0.01, 20000
TAUS, PRUEBAS = list(range(10)), list(range(2, 12))
CELDAS = ["0.0|0.15", "0.0|0.45", "0.3|0.15", "0.3|0.45", "0.6|0.15", "0.6|0.45"]
CELDA_NULOS, TAU_N, PRUEBA_N, N_NULOS = "0.3|0.15", 0, 2, 50


def pr(s):
    print(s, flush=True)


def bootstrap(D, alfa, rng):
    nt, npb = D.shape
    bs = np.empty(B)
    for b in range(B):
        bs[b] = D[np.ix_(rng.integers(0, nt, nt), rng.integers(0, npb, npb))].mean()
    return float(D.mean()), float(np.quantile(bs, alfa)), float(np.quantile(bs, 1 - alfa))


def veredicto(lo, hi):
    if lo > M:
        return "SUPERA"
    if hi < -M:
        return "PIERDE"
    if lo > -M and hi < M:
        return "EQUIVALENTE"
    if lo > -M:
        return "NO_INFERIOR"
    if hi < M:
        return "NO_SUPERIOR"
    return "INDETERMINADO"


def leer(carpeta, patron):
    out = []
    for ruta in sorted(glob.glob(os.path.join(carpeta, "**", patron), recursive=True)):
        with open(ruta) as f:
            out.append((os.path.basename(ruta), json.load(f)))
    return out


def main():
    d3, d2 = sys.argv[1], sys.argv[2]
    humo = "--humo" in sys.argv
    grilla = [(n, r) for n, r in leer(d3, "factorial2_R2_CON_TASA_*.json")]
    ancla = [r for n, r in leer(d3, "factorial2_ANCLA_015.json")]
    nulos = leer(d3, "nulos_R2_*.json")
    validos = {n: r["valido"] for n, r in grilla + nulos}
    pr("JSON grilla=%d nulos=%d ancla=%d validos=%s" % (len(grilla), len(nulos), len(ancla), all(validos.values())))
    ok_ancla = bool(ancla) and ancla[0]["valido"] and not ancla[0]["humo"]
    pr("CHEQUEO ANCLA_015 -> %s" % ok_ancla)
    W, RP, taudn = {}, {}, {}
    for n, r in grilla:
        for st, v in r["tau_DN"].items():
            taudn.setdefault(st, set()).add(tuple(v))
        for x in r["corridas"]:
            W[(x["tau"], x["prueba"], x["celda"])] = x["W"]
            RP[(x["prueba"], x["celda"])] = x["regla_propia"]
    tau_ok = all(len(v) == 1 for v in taudn.values())
    pr("CHEQUEO TAU_DN_IGUAL semillas=%d -> %s" % (len(taudn), tau_ok))
    taus, pruebas = TAUS, PRUEBAS
    if humo:
        taus = sorted(set(k[0] for k in W))
        pruebas = sorted(set(k[1] for k in W))
    celdas = CELDAS if not humo else sorted(set(k[2] for k in W))
    falt = [(t, p, c) for t in taus for p in pruebas for c in celdas if (t, p, c) not in W]
    pr("CHEQUEO PLAN_GRILLA corridas=%d faltan=%d" % (len(W), len(falt)))
    # reproduccion del factorial 2
    rep_tol, rep_ex, n_rep = True, True, 0
    for n, r in leer(d2, "factorial2_R2_CON_TASA_*.json"):
        for x in r["corridas"]:
            k = (x["tau"], x["prueba"], x["celda"])
            if k in W:
                n_rep += 1
                rep_tol &= abs(W[k] - x["W"]) <= 0.001 + 1e-9 and abs(RP[k[1:]] - x["regla_propia"]) <= 0.001 + 1e-9
                rep_ex &= W[k] == x["W"] and RP[k[1:]] == x["regla_propia"]
    rep_ok = rep_tol and (n_rep == 90 or humo)
    pr("CHEQUEO REPRODUCE_F2 corridas_comparadas=%d tolerancia=%s exacto=%s -> %s" % (n_rep, rep_tol, rep_ex, rep_ok))
    # nulos
    acc = {"SL": {}, "T": {}}
    reales = []
    for n, r in nulos:
        for x in r["nulos"]:
            acc[r["tipo"]][x["k"]] = x["acierto"]
        if r["real"] is not None:
            reales.append(r["real"])
    kW = (TAU_N, PRUEBA_N, CELDA_NULOS)
    W0 = W.get(kW)
    real_ok = W0 is not None and bool(reales) and all(abs(x - W0) <= 0.001 + 1e-9 for x in reales)
    pr("CHEQUEO REAL_IGUAL grilla=%s script_de_nulos=%s -> %s" % (W0, reales, real_ok))
    n_ok = all(len(acc[t]) == N_NULOS for t in acc) or humo
    pr("CHEQUEO PLAN_NULOS SL=%d T=%d -> %s" % (len(acc["SL"]), len(acc["T"]), n_ok))
    valido = all(validos.values()) and tau_ok and not falt and n_ok and (humo or (ok_ancla and rep_ok and real_ok))
    if humo:
        pr("# HUMO: ancla, reproduccion y plan completo no se exigen; numeros sin valor")
    rng = np.random.default_rng(2026)
    if falt:
        ver = "NO_EVALUABLE"
        pr("PRIMARIA R2_CON_TASA -> NO_EVALUABLE")
    else:
        D = np.array([[[W[(t, p, c)] - RP[(p, c)] for c in celdas] for p in pruebas] for t in taus])
        mw = np.mean([[[W[(t, p, c)] for c in celdas] for p in pruebas] for t in taus])
        mr = np.mean([[RP[(p, c)] for c in celdas] for p in pruebas])
        est, lo, hi = bootstrap(D.mean(2), 0.05, rng)
        ver = veredicto(lo, hi)
        pr("PRIMARIA R2_CON_TASA W=%.4f regla_propia=%.4f dif=%+.4f IC90=[%+.4f, %+.4f] corridas=%d -> %s" % (
            mw, mr, est, lo, hi, D.size, ver))
        for j, c in enumerate(celdas):
            e2, l2, h2 = bootstrap(D[:, :, j], 0.05 / 6, rng)
            pr("  CELDA %s dif=%+.4f IC=[%+.4f, %+.4f] -> %s" % (c, e2, l2, h2, veredicto(l2, h2)))
    ps = {}
    for t in ("SL", "T"):
        v = np.array(list(acc[t].values()))
        if W0 is None or not len(v):
            ps[t] = 1.0
            pr("NULOS %s -> NO_EVALUABLE" % t)
            continue
        ps[t] = (1 + int((v >= W0).sum())) / (len(v) + 1)
        pr("NULOS %s n=%d media=%.4f max=%.4f W=%.4f iguales_o_mejores=%d p_sup=%.4f" % (
            t, len(v), v.mean(), v.max(), W0, int((v >= W0).sum()), ps[t]))
    orden = sorted(ps, key=ps.get)
    adj, prev = {}, 0.0
    for i, t in enumerate(orden):
        prev = max(prev, min(1.0, ps[t] * (len(orden) - i)))
        adj[t] = prev
    pr("NULOS Holm %s" % " ".join("%s=%.4f" % (t, adj[t]) for t in ("SL", "T")))
    if ver == "SUPERA":
        h1 = "SOSTENIDA"
    elif ver in ("EQUIVALENTE", "NO_SUPERIOR", "PIERDE"):
        h1 = "REFUTADA"
    elif ver == "NO_EVALUABLE":
        h1 = "NO_EVALUABLE"
    else:
        h1 = "SIN_DECIDIR"
    h2 = "SOSTENIDA" if all(adj[t] < 0.05 for t in ("SL", "T")) else "NO SOSTENIDA"
    pr("HIPOTESIS H_SUPERA_R2 -> %s" % h1)
    pr("HIPOTESIS H_CABLEADO_R2 -> %s" % h2)
    pr("VEREDICTO_GLOBAL -> %s | primaria=%s" % ("VALIDO" if valido else "INVALIDO", ver))
    pr("EXIT_AGREGADO=%d" % (0 if valido else 3))
    return 0 if valido else 3


if __name__ == "__main__":
    sys.exit(main())
