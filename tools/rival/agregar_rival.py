#!/usr/bin/env python3
"""Agregador de H_RIVAL (respuesta 2026-10-14-033). Aplica tools/rival/SELLO-RIVAL.md (05a574c) tal cual.

Lee rival_c0.json a rival_c5.json y controles_015.json. Primaria: d = W_elegida - rival por celda y semilla de prueba
(12 a 21); D = media; bootstrap de las 10 semillas de prueba con el mismo remuestreo para las 6 celdas y los 3 rivales
(B = 20.000, semilla 2031); percentiles 1,667 y 98,333 (90% con Bonferroni por 3 rivales); margen 0,01.
SUPERA_POR_MARGEN si el piso pasa 0,01; NO_SUPERA si el techo queda debajo de 0,01; si no, SIN_DECIDIR.
H_RIVAL: SOSTENIDA si supera a los tres; REFUTADA si no supera a alguno; si no, SIN_DECIDIR. H_TAU_JUSTO: REGLA_TAU.
Secundaria, solo descriptiva: W del factorial 3 (tau 0 a 9, pruebas 2 a 11), bootstrap en dos vias (semilla 2032).
Cualquier control fallido o archivo faltante: INVALIDO. Con --cotejar A B compara dos agregados (dos maquinas).
"""
import argparse
import json
import os
import sys

import numpy as np

RIVALES = ("RIDGE", "MLP", "REGLA_TAU")
PRIMARIA = list(range(12, 22))
SECUNDARIA = list(range(2, 12))
TAUS = list(range(10))
NCEL = 6
B = 20000
SEM_P, SEM_S = 2031, 2032
ALFA, MARGEN = 0.10, 0.01
Q_LO = 100.0 * ALFA / len(RIVALES) / 2.0
Q_HI = 100.0 - Q_LO


def pr(s):
    print(s, flush=True)


def etiqueta(lo, hi):
    if lo > MARGEN:
        return "SUPERA_POR_MARGEN"
    if hi < MARGEN:
        return "NO_SUPERA"
    return "SIN_DECIDIR"


def veredictos(et):
    if all(et[r] == "SUPERA_POR_MARGEN" for r in RIVALES):
        h = "SOSTENIDA"
    elif any(et[r] == "NO_SUPERA" for r in RIVALES):
        h = "REFUTADA"
    else:
        h = "SIN_DECIDIR"
    tj = {"SUPERA_POR_MARGEN": "SOSTENIDA", "NO_SUPERA": "REFUTADA"}.get(et["REGLA_TAU"], "SIN_DECIDIR")
    return h, tj


def conteos(idx, n):
    c = np.zeros((idx.shape[0], n))
    filas = np.repeat(np.arange(idx.shape[0]), idx.shape[1])
    np.add.at(c, (filas, idx.ravel()), 1.0)
    return c


def resumen(d, bs):
    lo, hi = float(np.percentile(bs, Q_LO)), float(np.percentile(bs, Q_HI))
    return dict(D=float(np.mean(d)), lo=lo, hi=hi, etiqueta=etiqueta(lo, hi), pierde=bool(hi < 0))


def boot_primaria(D):
    """D[r]: (celdas, 10 pruebas)."""
    idx = np.random.default_rng(SEM_P).integers(0, len(PRIMARIA), (B, len(PRIMARIA)))
    c = conteos(idx, len(PRIMARIA))
    out = {}
    for r in RIVALES:
        d = np.asarray(D[r], float)
        out[r] = resumen(d, c @ d.sum(0) / (d.shape[0] * d.shape[1]))
    return out


def boot_secundaria(D2):
    """D2[r]: (celdas, 10 semillas de tau, 10 pruebas); tau y prueba se remuestrean por separado."""
    rng = np.random.default_rng(SEM_S)
    it = rng.integers(0, len(TAUS), (B, len(TAUS)))
    ip = rng.integers(0, len(SECUNDARIA), (B, len(SECUNDARIA)))
    ct, cp = conteos(it, len(TAUS)), conteos(ip, len(SECUNDARIA))
    out = {}
    for r in RIVALES:
        d = np.asarray(D2[r], float)
        bs = np.einsum("bi,ij,bj->b", ct, d.sum(0), cp) / (d.shape[0] * d.shape[1] * d.shape[2])
        out[r] = resumen(d, bs)
    return out


def media(filas, c, k):
    return float(np.mean([filas[c][p][k] for p in PRIMARIA]))


def agregar(carpeta):
    nombres = ["rival_c%d.json" % c for c in range(NCEL)] + ["controles_015.json"]
    faltan = [x for x in nombres if not os.path.exists(os.path.join(carpeta, x))]
    res = dict(experimento="H_RIVAL", faltan=faltan)
    if faltan:
        pr("FALTAN " + " ".join(faltan))
        res.update(valido=False, H_RIVAL="INVALIDO", H_TAU_JUSTO="INVALIDO")
        pr("VEREDICTO H_RIVAL=INVALIDO H_TAU_JUSTO=INVALIDO (faltan archivos)")
        return res
    cel = [json.load(open(os.path.join(carpeta, "rival_c%d.json" % c))) for c in range(NCEL)]
    c15 = json.load(open(os.path.join(carpeta, "controles_015.json")))
    ctrl = {}
    for c, j in enumerate(cel):
        ctrl["c%d" % c] = bool(j.get("valido") is True and j.get("humo") is False and j.get("ci") == c)
        pr("CONTROLES c%d %s %s" % (c, j.get("celda"), " ".join("%s=%s" % kv for kv in sorted(j.get("controles", {}).items()))))
    ctrl["CONTROL_MLP_005"] = bool(cel[0].get("controles", {}).get("CONTROL_MLP_005") is True)
    ctrl["CONTROL_RIDGE_015"] = bool(c15.get("valido") is True and c15.get("humo") is False)
    for f in c15.get("filas", []):
        pr("CONTROL_RIDGE_015 celda=%s acierto=%.4f esperado=%.4f -> %s" % (f["celda"], f["acierto"], f["esperado"], f["ok"]))
    todas = sorted(SECUNDARIA + PRIMARIA)
    plan = all(sorted(f["prueba"] for f in j.get("filas", [])) == todas and
               all(r in f for f in j["filas"] for r in RIVALES) for j in cel)
    ctrl["PLAN_COMPLETO"] = bool(plan)
    valido = all(ctrl.values())
    res.update(controles=ctrl, valido=valido)
    pr("CHEQUEO " + " ".join("%s=%s" % kv for kv in ctrl.items()) + " -> " + ("VALIDO" if valido else "INVALIDO"))
    if not plan:
        res.update(H_RIVAL="INVALIDO", H_TAU_JUSTO="INVALIDO")
        pr("VEREDICTO H_RIVAL=INVALIDO H_TAU_JUSTO=INVALIDO (plan incompleto)")
        return res
    filas = [{f["prueba"]: f for f in j["filas"]} for j in cel]
    D = {r: [[filas[c][p]["W_elegida"] - filas[c][p][r] for p in PRIMARIA] for c in range(NCEL)] for r in RIVALES}
    D2 = {r: [[[filas[c][p]["W_f3"][str(t)] - filas[c][p][r] for p in SECUNDARIA] for t in TAUS] for c in range(NCEL)]
          for r in RIVALES}
    for c in range(NCEL):
        pr("CELDA c%d %s W_elegida=%.4f RIDGE=%.4f MLP=%.4f REGLA_TAU=%.4f regla_propia=%.4f (media de las pruebas 12 a 21)" % (
            c, cel[c]["celda"], media(filas, c, "W_elegida"), media(filas, c, "RIDGE"), media(filas, c, "MLP"),
            media(filas, c, "REGLA_TAU"), media(filas, c, "regla_propia")))
    prim = boot_primaria(D)
    for r in RIVALES:
        x = prim[r]
        pr("PRIMARIA rival=%s D=%+.4f IC=[%+.4f, %+.4f] margen=%.2f -> %s%s" % (
            r, x["D"], x["lo"], x["hi"], MARGEN, x["etiqueta"], " (PIERDE: el techo es menor que 0)" if x["pierde"] else ""))
    sec = boot_secundaria(D2)
    for r in RIVALES:
        x = sec[r]
        pr("SECUNDARIA (descriptiva, no decide) rival=%s D2=%+.4f IC=[%+.4f, %+.4f] -> %s" % (
            r, x["D"], x["lo"], x["hi"], x["etiqueta"]))
    h, tj = veredictos({r: prim[r]["etiqueta"] for r in RIVALES})
    if not valido:
        h, tj = "INVALIDO", "INVALIDO"
    pr("VEREDICTO H_RIVAL=%s H_TAU_JUSTO=%s" % (h, tj))
    res.update(primaria=prim, secundaria=sec, H_RIVAL=h, H_TAU_JUSTO=tj,
               aciertos={str(c): {r: [filas[c][p][r] for p in SECUNDARIA + PRIMARIA] for r in RIVALES} for c in range(NCEL)})
    return res


def cotejar(pa, pb):
    A, Bb = json.load(open(pa)), json.load(open(pb))
    if "primaria" not in A or "primaria" not in Bb:
        pr("COTEJO imposible: falta la primaria en algun agregado")
        pr("VEREDICTO_COTEJADO H_RIVAL=INVALIDO H_TAU_JUSTO=INVALIDO")
        return 3
    et = {}
    for r in RIVALES:
        ea, eb = A["primaria"][r]["etiqueta"], Bb["primaria"][r]["etiqueta"]
        et[r] = ea if ea == eb else "SIN_DECIDIR"
        dif = [abs(x - y) for c in range(NCEL) for x, y in zip(A["aciertos"][str(c)][r], Bb["aciertos"][str(c)][r])]
        pr("COTEJO rival=%s etiqueta %s / %s -> %s | aciertos iguales %d/%d max_dif=%.4f" % (
            r, ea, eb, "IGUAL" if ea == eb else "NO_SE_REPLICA", sum(x == 0 for x in dif), len(dif), max(dif)))
    if A.get("valido") is True and Bb.get("valido") is True:
        h, tj = veredictos(et)
    else:
        h, tj = "INVALIDO", "INVALIDO"
    pr("VEREDICTO_COTEJADO H_RIVAL=%s H_TAU_JUSTO=%s" % (h, tj))
    return 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", default=None, help="carpeta con rival_c0..c5.json y controles_015.json")
    ap.add_argument("--cotejar", nargs=2, default=None, help="dos agregado.json")
    a = ap.parse_args()
    if a.cotejar:
        return cotejar(*a.cotejar)
    res = agregar(a.dir)
    with open(os.path.join(a.dir, "agregado.json"), "w") as f:
        json.dump(res, f, indent=1)
    pr("escrito agregado.json")
    return 0


if __name__ == "__main__":
    sys.exit(main())
