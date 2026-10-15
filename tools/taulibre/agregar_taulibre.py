#!/usr/bin/env python3
"""Agregador de H_TAU_LIBRE (sello tools/taulibre/SELLO-TAU-LIBRE.md, fec8472). Respuesta 2026-10-14-040.

Lee los json de taulibre_mosca.py (reales_c2_t20, reales_c2_t25, reales_c5_t20, reales_c5_t25 y nulos_{SL,T}_c{2,5}
_k{000,010,020,030}). Por familia f y celda c, cada nulo k se compara con la red real de su misma tau,
r(k) = WL_real(c, 20 + k mod 10): p = (1 + nulos con WL_nulo >= r) / 41; delta = media de (r - WL_nulo).
SUPERA si p <= 0,05 y delta > 0,01. H_TAU_LIBRE: SOSTENIDA si SUPERA en las 4; REFUTADA si algun delta < 0,01 o
algun p > 0,10; SIN_DECIDIR si no. Si falta un archivo o falla un control: INVALIDO y sin descriptivos.
Uso: python3 agregar_taulibre.py --dir results/taulibre_2026-10-15
"""
import argparse
import json
import os
import sys

TAUS = list(range(20, 30))
CELDAS = (2, 5)
FAMILIAS = ("SL", "T")
K0S = (0, 10, 20, 30)
N_NULOS = 40
REALES = [(2, 20), (2, 25), (5, 20), (5, 25)]
P_MAX, P_REF, MARGEN = 0.05, 0.10, 0.01


def pr(s):
    print(s, flush=True)


def tau_de_k(k):
    return TAUS[0] + (k % 10)


def combinacion(rk, wn):
    """rk: WL del real apareado por nulo; wn: WL de cada nulo (mismo orden)."""
    n = len(wn)
    ge = sum(1 for r, w in zip(rk, wn) if w >= r)
    p = (1 + ge) / (n + 1)
    delta = sum(r - w for r, w in zip(rk, wn)) / n
    return dict(p=p, delta=delta, iguales_o_mas=ge, supera=bool(p <= P_MAX and delta > MARGEN))


def veredicto(com):
    if all(c["supera"] for c in com.values()):
        return "SOSTENIDA"
    if any(c["delta"] < MARGEN or c["p"] > P_REF for c in com.values()):
        return "REFUTADA"
    return "SIN_DECIDIR"


def invalido(motivo):
    pr("VEREDICTO H_TAU_LIBRE=INVALIDO (%s)" % motivo)
    return dict(experimento="H_TAU_LIBRE", veredicto="INVALIDO", motivo=motivo)


def agregar(carpeta):
    faltan = []
    nombres = ["reales_c%d_t%d.json" % x for x in REALES]
    nombres += ["nulos_%s_c%d_k%03d.json" % (f, c, k0) for f in FAMILIAS for c in CELDAS for k0 in K0S]
    J = {}
    for nom in nombres:
        ruta = os.path.join(carpeta, nom)
        if os.path.exists(ruta):
            J[nom] = json.load(open(ruta))
        else:
            faltan.append(nom)
    if faltan:
        pr("FALTAN " + " ".join(faltan))
        return invalido("faltan archivos")
    ctrl = {}
    for nom, d in J.items():
        ok = bool(d.get("valido") is True and d.get("humo") is False and d.get("local") is False and
                  all(v is not False for v in d.get("controles", {}).values()))
        ctrl[nom] = ok
        pr("CONTROLES %s valido=%s %s" % (nom, ok, " ".join("%s=%s" % kv for kv in sorted(d.get("controles", {}).items()))))
    scripts = set(d.get("md5_script") for d in J.values())
    ctrl["MISMO_SCRIPT"] = bool(len(scripts) == 1)
    rep = [J["reales_c%d_t20.json" % c].get("controles", {}).get("REPRO_LECTOR") for c in CELDAS]
    ctrl["REPRO_LECTOR"] = bool(all(r is True for r in rep))
    WLr = {c: {} for c in CELDAS}
    for c, t0 in REALES:
        for e in J["reales_c%d_t%d.json" % (c, t0)]["reales"]:
            WLr[c][int(e["tau"])] = float(e["WL"])
    ctrl["PLAN_REALES"] = bool(all(sorted(WLr[c]) == TAUS for c in CELDAS))
    WLn, plan_n = {}, True
    for f in FAMILIAS:
        for c in CELDAS:
            por_k = {}
            for k0 in K0S:
                for e in J["nulos_%s_c%d_k%03d.json" % (f, c, k0)]["nulos"]:
                    k = int(e["k"])
                    plan_n &= bool(int(e["tau"]) == tau_de_k(k) and "WL" in e and k not in por_k)
                    por_k[k] = float(e.get("WL", -1.0))
            plan_n &= bool(sorted(por_k) == list(range(N_NULOS)))
            WLn[(f, c)] = por_k
    ctrl["PLAN_NULOS"] = bool(plan_n)
    todo = all(ctrl.values())
    pr("CHEQUEO %s -> %s" % (" ".join("%s=%s" % (k, v) for k, v in ctrl.items() if not k.endswith(".json")) +
                             " json_validos=%d/%d" % (sum(1 for k, v in ctrl.items() if k.endswith(".json") and v), len(J)),
                             "VALIDO" if todo else "INVALIDO"))
    if not todo:
        return invalido("control fallido")
    com = {}
    for f in FAMILIAS:
        for c in CELDAS:
            ks = list(range(N_NULOS))
            rk = [WLr[c][tau_de_k(k)] for k in ks]
            wn = [WLn[(f, c)][k] for k in ks]
            com["%s_c%d" % (f, c)] = cc = combinacion(rk, wn)
            pr("NULOS %s c%d real_medio=%.4f nulo_medio=%.4f delta=%+.4f iguales_o_mas=%d p=%.4f -> %s" % (
                f, c, sum(rk) / len(rk), sum(wn) / len(wn), cc["delta"], cc["iguales_o_mas"], cc["p"],
                "SUPERA" if cc["supera"] else "NO_SUPERA"))
    v = veredicto(com)
    desc = {}
    for c in CELDAS:
        vals = [WLr[c][t] for t in TAUS]
        rep10 = J["reales_c%d_t20.json" % c].get("repro") or {}
        w10 = rep10.get("WL")
        arriba = sum(1 for x in vals if w10 is not None and x < w10)
        desc["c%d" % c] = dict(min=min(vals), max=max(vals), tau10=w10, frescas_debajo_de_tau10=arriba)
        pr("DESCRIPTIVO c%d WL_real taus 20 a 29: min=%.4f max=%.4f | tau 10 (H_LECTOR)=%s, frescas debajo=%d/10" % (
            c, min(vals), max(vals), "%.4f" % w10 if w10 is not None else "NA", arriba))
        for f in FAMILIAS:
            por_t = []
            for t in TAUS:
                ws = [WLn[(f, c)][k] for k in range(N_NULOS) if tau_de_k(k) == t]
                por_t.append("%d:%+.4f" % (t, WLr[c][t] - sum(ws) / len(ws)))
            pr("DESCRIPTIVO %s c%d delta por tau %s" % (f, c, " ".join(por_t)))
    pr("VEREDICTO H_TAU_LIBRE=%s" % v)
    return dict(experimento="H_TAU_LIBRE", veredicto=v, combinaciones=com, controles=ctrl, descriptivos=desc,
                reales={str(c): {str(t): WLr[c][t] for t in TAUS} for c in CELDAS})


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", required=True)
    a = ap.parse_args()
    res = agregar(a.dir)
    with open(os.path.join(a.dir, "agregado.json"), "w") as f:
        json.dump(res, f)
    pr("escrito agregado.json")
    return 0


if __name__ == "__main__":
    sys.exit(main())
