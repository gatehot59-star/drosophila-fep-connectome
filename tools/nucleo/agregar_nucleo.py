#!/usr/bin/env python3
"""Agregador del nucleo conservado (H_CONSENSO y H_CABLEADO_NUCLEO; respuesta 2026-10-14-002). Sellado antes de correr.

Junta los json de tools/nucleo/nucleo_mosca.py (60 de grilla y 20 de nulos) con los de R2 del factorial 3
(results/factorial3_2026-10-13, en git) y decide con reglas fijadas antes de ver datos:
  PRIMARIA    E[t, p, c] = acierto del nucleo menos acierto de R2 entero en la misma semilla de tau, de prueba y celda
              (mismos ensayos y misma regla). Media; bootstrap de dos vias (tau y prueba) como el del factorial 4,
              B = 20.000, semilla 2030, percentiles 0,05 y 0,95; margen M = 0,01. Es de no inferioridad: el nucleo no
              puede perder mas de 1 punto. lo > -M -> NO_PIERDE; hi < -M -> PIERDE; si no, INDETERMINADO. Por celda, el
              mismo bootstrap con alfa 0,05/6 (descriptivo).
  NULOS       el nucleo real (tau 0, prueba 2, celda 0,3|0,15) contra 50 SL y 50 T del nucleo; p = (1 + iguales o
              mejores) / (n + 1); Holm sobre los dos. H_CABLEADO_NUCLEO SOSTENIDA si los dos quedan bajo 0,05.
  H_CONSENSO  SOSTENIDA si la primaria da NO_PIERDE y H_CABLEADO_NUCLEO queda SOSTENIDA; REFUTADA si da PIERDE o si
              H_CABLEADO_NUCLEO queda REFUTADA; SIN_DECIDIR en el resto.
  DESCRIPTIVO el nucleo contra su regla propia (como la primaria del factorial 3, semilla 2031) y por semilla de tau.
Chequeos que invalidan: 60 json de grilla (10 taus x 6 celdas) y las 600 corridas; 50 + 50 nulos sin repetir; todos
validos y sin humo; md5 del instrumento sellado y de sus modulos en todos; el mismo nucleo sellado (aristas,
inhibitorias y huella) en todos; regla propia igual a la del factorial 3 en las 60 combinaciones de prueba y celda
(acierto y prediccion por ensayo); las mismas tau de las descendentes y las mismas descendentes que el 3; REAL_IGUAL:
el nucleo real de los nulos da lo mismo que la grilla en tau 0, prueba 2, 0,3|0,15.
Uso: python3 tools/nucleo/agregar_nucleo.py <carpeta del nucleo> <carpeta del factorial 3> [--humo]
Salida: EXIT_AGREGADO=0 si el veredicto global es VALIDO; 1 si no.
"""
import glob
import json
import os
import sys

import numpy as np

CELDAS = ["0.0|0.15", "0.0|0.45", "0.3|0.15", "0.3|0.45", "0.6|0.15", "0.6|0.45"]
TAUS = list(range(10))
PRUEBAS = list(range(2, 12))
M = 0.01
B = 20000
N_NULOS = 50
MD5_NUCLEO = "4697c81d994de841f167698562924caa"
PIN = {"factorial2": "798a824cd47808155fa12adb9e652dac", "nulos_r2": "c4f1c4d39c99f07cb9ad7977b6f3b01a",
       "modulo015": "40d64e074d9163753439307c5be4ac5e", "conn": "3d802fd542b5d18570ba1ba0bb0abed9",
       "annot": "719904abad876c68ace1b5690c9b9b63"}
NUCLEO = (603219, 260173, "69255109562f8a93270c435acdde2239")


def pr(s):
    print(s, flush=True)


def bootstrap(D, alfa, rng):
    nt, npb = D.shape
    bs = np.empty(B)
    for b in range(B):
        bs[b] = D[np.ix_(rng.integers(0, nt, nt), rng.integers(0, npb, npb))].mean()
    return float(D.mean()), float(np.quantile(bs, alfa)), float(np.quantile(bs, 1 - alfa))


def no_inferior(lo, hi):
    if lo > -M:
        return "NO_PIERDE"
    if hi < -M:
        return "PIERDE"
    return "INDETERMINADO"


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
    for r in sorted(glob.glob(os.path.join(carpeta, "**", patron), recursive=True)):
        with open(r) as f:
            out.append((r, json.load(f)))
    return out


def tablas(grilla):
    """W por (tau, prueba, celda); la regla por (prueba, celda) como conjunto, porque aparece en los 10 json de tau."""
    W, RP, PRP, taudn, dns, dup = {}, {}, {}, {}, set(), 0
    for _, r in grilla:
        dns.add(tuple(r["dns_root"]))
        for st, v in r["tau_DN"].items():
            taudn.setdefault(st, set()).add(tuple(v))
        for x in r["corridas"]:
            k = (x["tau"], x["prueba"], x["celda"])
            dup += k in W
            W[k] = x["W"]
            RP.setdefault((x["prueba"], x["celda"]), set()).add(x["regla_propia"])
        for x in r.get("reglas", []):
            PRP.setdefault((x["prueba"], x["celda"]), set()).add(x["pred_regla_propia"])
    return W, RP, PRP, taudn, dns, dup


def cubo(f):
    return np.array([[[f(t, p, c) for c in CELDAS] for p in PRUEBAS] for t in TAUS], dtype=np.float64)


def main():
    d, d3 = sys.argv[1], sys.argv[2]
    humo = "--humo" in sys.argv
    g = leer(d, "nucleo_grilla_*.json")
    nl = leer(d, "nulos_nucleo_*.json")
    g3 = leer(d3, "factorial2_R2_CON_TASA_*.json")
    pr("JSON grilla=%d nulos=%d | factorial 3 grilla=%d" % (len(g), len(nl), len(g3)))
    todos = [r for _, r in g + nl]
    ok_val = bool(todos) and all(r.get("valido") is True for r in todos)
    sin_humo = bool(todos) and all(not r.get("humo") for r in todos)
    ok_md5 = bool(todos) and all(r.get("md5", {}).get("script") == MD5_NUCLEO and
                                 all(r.get("md5", {}).get(k) == v for k, v in PIN.items()) for r in todos)
    ok_nuc = bool(todos) and all((r.get("nucleo", {}).get("aristas"), r.get("nucleo", {}).get("inhibitorias"),
                                  r.get("nucleo", {}).get("huella")) == NUCLEO for r in todos)
    pr("CHEQUEO VALIDOS -> %s | SIN_HUMO -> %s | MD5 instrumento=%s y pines -> %s | NUCLEO_SELLADO -> %s" % (
        ok_val, sin_humo, MD5_NUCLEO[:8], ok_md5, ok_nuc))
    W4, RP4, PRP4, taudn4, dns4, dup4 = tablas(g)
    W3, RP3, PRP3, taudn3, dns3, dup3 = tablas(g3)
    falt = [(t, p, c) for t in TAUS for p in PRUEBAS for c in CELDAS if (t, p, c) not in W4]
    falt3 = [(t, p, c) for t in TAUS for p in PRUEBAS for c in CELDAS if (t, p, c) not in W3]
    ok_plan = (not falt and len(g) == 60 and dup4 == 0) or humo
    pr("CHEQUEO PLAN_GRILLA json=%d corridas=%d faltan=%d repetidas=%d | factorial 3 faltan=%d repetidas=%d -> %s" % (
        len(g), len(W4), len(falt), dup4, len(falt3), dup3, ok_plan and not falt3))
    comb = sorted(PRP4)
    iguales = sum(1 for k in comb if k in PRP3 and len(PRP4[k]) == 1 and PRP3[k] == PRP4[k] and
                  len(RP4.get(k, ())) == 1 and RP3.get(k) == RP4.get(k))
    regla_ok = bool(comb) and iguales == len(comb) and (len(comb) == len(PRUEBAS) * len(CELDAS) or humo)
    tau3_ok = bool(taudn4) and all(len(v) == 1 for v in taudn4.values()) and all(
        taudn3.get(st) == v for st, v in taudn4.items())
    dn3_ok = len(dns4) == 1 and dns4 == dns3
    pr("CHEQUEO REGLA_IGUAL_F3 combinaciones=%d iguales=%d -> %s" % (len(comb), iguales, regla_ok))
    pr("CHEQUEO TAU_DN_IGUAL_F3 -> %s | DN_IGUAL_F3 -> %s" % (tau3_ok, dn3_ok))
    acc, ks, dup, reales = {"SL": [], "T": []}, {"SL": set(), "T": set()}, 0, []
    for _, r in nl:
        t = r.get("tipo")
        if t not in acc:
            continue
        for x in r.get("nulos", []):
            dup += x["k"] in ks[t]
            ks[t].add(x["k"])
            acc[t].append(x["acierto"])
        if r.get("real") is not None:
            reales.append(r["real"])
    plan_nulos = (all(len(acc[t]) == N_NULOS for t in acc) and dup == 0) or humo
    pr("CHEQUEO PLAN_NULOS SL=%d T=%d repetidos=%d -> %s" % (len(acc["SL"]), len(acc["T"]), dup, plan_nulos))
    real_g = W4.get((0, 2, "0.3|0.15"))
    real_ok = bool(reales) and real_g is not None and all(abs(x - real_g) < 1e-12 for x in reales)
    pr("CHEQUEO REAL_IGUAL grilla=%s script_de_nulos=%s -> %s" % (real_g, reales, real_ok))
    valido = (ok_val and ok_plan and not falt3 and regla_ok and tau3_ok and dn3_ok and plan_nulos and ok_nuc and
              (humo or (sin_humo and ok_md5 and real_ok)))
    if humo:
        pr("# HUMO: no se exigen el plan completo, SIN_HUMO, MD5 ni REAL_IGUAL; numeros sin valor")
    ver = "NO_EVALUABLE"
    if not falt and not falt3:
        E = cubo(lambda t, p, c: W4[(t, p, c)] - W3[(t, p, c)])
        rng = np.random.default_rng(2030)
        est, lo, hi = bootstrap(E.mean(2), 0.05, rng)
        ver = no_inferior(lo, hi)
        pr("PRIMARIA NUCLEO_menos_R2 W_nucleo=%.4f W_R2=%.4f dif=%+.4f IC90=[%+.4f, %+.4f] corridas=%d -> %s" % (
            cubo(lambda t, p, c: W4[(t, p, c)]).mean(), cubo(lambda t, p, c: W3[(t, p, c)]).mean(), est, lo, hi, E.size,
            ver))
        for j, c in enumerate(CELDAS):
            e2, l2, h2 = bootstrap(E[:, :, j], 0.05 / 6, rng)
            pr("  CELDA %s dif=%+.4f IC=[%+.4f, %+.4f] -> %s" % (c, e2, l2, h2, no_inferior(l2, h2)))
        pr("PRIMARIA corridas nucleo>R2=%d iguales=%d nucleo<R2=%d" % (int((E > 0).sum()), int((E == 0).sum()),
                                                                     int((E < 0).sum())))
        D = cubo(lambda t, p, c: W4[(t, p, c)] - min(RP4[(p, c)]))
        e4, l4, h4 = bootstrap(D.mean(2), 0.05, np.random.default_rng(2031))
        pr("DESCRIPTIVO nucleo_menos_regla dif=%+.4f IC90=[%+.4f, %+.4f] -> %s (no decide)" % (e4, l4, h4,
                                                                                            veredicto(l4, h4)))
        for i, t in enumerate(TAUS):
            pr("DESCRIPTIVO TAU %d nucleo-R2=%+.4f nucleo-regla=%+.4f" % (t, E[i].mean(), D[i].mean()))
    ps = {}
    real = real_g if real_g is not None else float("nan")
    for t in ("SL", "T"):
        a = np.array(acc[t], dtype=np.float64)
        k = int((a >= real).sum()) if len(a) else 0
        ps[t] = (1 + k) / (len(a) + 1) if len(a) else 1.0
        pr("NULOS %s n=%d media=%.4f max=%.4f W=%.4f iguales_o_mejores=%d p_sup=%.4f" % (
            t, len(a), a.mean() if len(a) else float("nan"), a.max() if len(a) else float("nan"), real, k, ps[t]))
    orden = sorted(ps, key=lambda x: ps[x])
    holm, prev = {}, 0.0
    for i, t in enumerate(orden):
        prev = max(prev, min(1.0, (len(orden) - i) * ps[t]))
        holm[t] = prev
    pr("NULOS Holm SL=%.4f T=%.4f" % (holm["SL"], holm["T"]))
    cab = "SOSTENIDA" if all(v < 0.05 for v in holm.values()) else "REFUTADA"
    if not valido:
        h_con, cab = "NO_EVALUABLE", "NO_EVALUABLE"
    elif ver == "PIERDE" or cab == "REFUTADA":
        h_con = "REFUTADA"
    elif ver == "NO_PIERDE" and cab == "SOSTENIDA":
        h_con = "SOSTENIDA"
    else:
        h_con = "SIN_DECIDIR"
    pr("HIPOTESIS H_CABLEADO_NUCLEO -> %s" % cab)
    pr("HIPOTESIS H_CONSENSO -> %s" % h_con)
    pr("VEREDICTO_GLOBAL -> %s | primaria=%s" % ("VALIDO" if valido else "INVALIDO", ver))
    pr("EXIT_AGREGADO=%d" % (0 if valido else 1))
    return 0 if valido else 1


if __name__ == "__main__":
    sys.exit(main())
