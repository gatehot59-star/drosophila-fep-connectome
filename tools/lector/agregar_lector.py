#!/usr/bin/env python3
"""Agregador de H_LECTOR (respuesta 2026-10-14-037). Aplica tools/lector/SELLO-LECTOR.md (8e65e05) tal cual.

Lee lector_c0.json a lector_c5.json y los nulos_{SL,T}_c{2,5}_k{000,010,020,030}.json.
Primaria: d1 = WL - RIDGE y d2 = WL - W_elegida por celda y prueba (12 a 21); D = media; bootstrap de las 10 pruebas
con el mismo remuestreo para las 6 celdas y las dos diferencias (B = 20.000, semilla 2041); percentiles 2,5 y 97,5.
  H_LECTOR_CERCA  SOSTENIDA si el piso de D1 pasa -0,01; REFUTADA si el techo queda debajo de -0,01.
  H_LECTOR_PAGA   SOSTENIDA si el piso de D2 pasa +0,01; REFUTADA si el techo queda debajo de +0,01.
Nulos: p = (1 + nulos con WL >= real) / 41 y delta = real - media, por familia y celda, con el real de la primaria
en la prueba 12. SUPERA si p <= 0,05 y delta > 0,01. H_LECTOR_CABLEADO: SOSTENIDA si SUPERA en las 4; REFUTADA si
en alguna delta < 0,01 o p > 0,10; si no, SIN_DECIDIR. Cualquier control fallido o archivo faltante: INVALIDO.
Con --cotejar A B compara dos agregados (dos maquinas; los nulos solo corren en Actions).
"""
import argparse
import json
import os
import sys

import numpy as np

PRIMARIA = list(range(12, 22))
NCEL = 6
CELDAS_NULOS = (2, 5)
FAMILIAS = ("SL", "T")
K0S = (0, 10, 20, 30)
N_NULOS = 40
B = 20000
SEM = 2041
Q_LO, Q_HI = 2.5, 97.5
MARGEN = 0.01
P_SUPERA, P_REFUTA = 0.05, 0.10
HIPS = ("H_LECTOR_CERCA", "H_LECTOR_PAGA", "H_LECTOR_CABLEADO")


def pr(s):
    print(s, flush=True)


def etiqueta(lo, hi, umbral):
    if lo > umbral:
        return "SOSTENIDA"
    if hi < umbral:
        return "REFUTADA"
    return "SIN_DECIDIR"


def conteos(idx, n):
    c = np.zeros((idx.shape[0], n))
    filas = np.repeat(np.arange(idx.shape[0]), idx.shape[1])
    np.add.at(c, (filas, idx.ravel()), 1.0)
    return c


def boot(D1, D2):
    idx = np.random.default_rng(SEM).integers(0, len(PRIMARIA), (B, len(PRIMARIA)))
    c = conteos(idx, len(PRIMARIA))
    out = []
    for d in (np.asarray(D1, float), np.asarray(D2, float)):
        bs = c @ d.sum(0) / (d.shape[0] * d.shape[1])
        out.append(dict(D=float(d.mean()), lo=float(np.percentile(bs, Q_LO)), hi=float(np.percentile(bs, Q_HI))))
    return out


def cableado(real, nul):
    """real: WL de la red real; nul: lista de 40 WL de nulos."""
    nul = np.asarray(nul, float)
    p = (1.0 + float((nul >= real).sum())) / (len(nul) + 1.0)
    delta = float(real - nul.mean())
    return dict(p=p, delta=delta, maximo=float(nul.max()), supera=bool(p <= P_SUPERA and delta > MARGEN),
                refuta=bool(delta < MARGEN or p > P_REFUTA))


def veredicto_cableado(com):
    if all(x["supera"] for x in com.values()):
        return "SOSTENIDA"
    if any(x["refuta"] for x in com.values()):
        return "REFUTADA"
    return "SIN_DECIDIR"


def invalido(res, motivo):
    pr("VEREDICTO " + " ".join("%s=INVALIDO" % h for h in HIPS) + " (%s)" % motivo)
    res.update(valido=False, **{h: "INVALIDO" for h in HIPS})
    return res


def agregar(carpeta):
    cel_n = ["lector_c%d.json" % c for c in range(NCEL)]
    nul_n = ["nulos_%s_c%d_k%03d.json" % (f, c, k) for f in FAMILIAS for c in CELDAS_NULOS for k in K0S]
    faltan = [x for x in cel_n + nul_n if not os.path.exists(os.path.join(carpeta, x))]
    res = dict(experimento="H_LECTOR", faltan=faltan)
    if faltan:
        pr("FALTAN " + " ".join(faltan))
        return invalido(res, "faltan archivos")
    cel = [json.load(open(os.path.join(carpeta, x))) for x in cel_n]
    ctrl = {}
    for c, j in enumerate(cel):
        ctrl["c%d" % c] = bool(j.get("valido") is True and j.get("humo") is False and j.get("local") is False and
                               j.get("ci") == c and j.get("modo") == "celda")
        pr("CONTROLES c%d %s %s" % (c, j.get("celda"), " ".join("%s=%s" % kv for kv in sorted(j.get("controles", {}).items()))))
    ctrl["CONTROL_LECTOR_CRUDO"] = bool(cel[0].get("controles", {}).get("CONTROL_LECTOR_CRUDO") is True)
    plan = all(sorted(f["prueba"] for f in j.get("filas", [])) == PRIMARIA for j in cel)
    nul = {}
    ok_nul = True
    for f in FAMILIAS:
        for c in CELDAS_NULOS:
            ws, ks, real = [], [], None
            for k0 in K0S:
                j = json.load(open(os.path.join(carpeta, "nulos_%s_c%d_k%03d.json" % (f, c, k0))))
                ok_nul = ok_nul and bool(j.get("valido") is True and j.get("humo") is False and j.get("local") is False
                                         and j.get("tipo") == f and j.get("ci") == c and j.get("prueba") == 12)
                for e in j.get("nulos", []):
                    ks.append(e["k"])
                    ws.append(e.get("WL"))
                if k0 == 0:
                    real = j.get("real")
            ok_nul = ok_nul and sorted(ks) == list(range(N_NULOS)) and all(w is not None for w in ws) and real is not None
            nul[(f, c)] = (ws, real)
    ctrl["NULOS"] = bool(ok_nul)
    ctrl["PLAN_COMPLETO"] = bool(plan and ok_nul)
    if not ctrl["PLAN_COMPLETO"]:
        res.update(controles=ctrl)
        pr("CHEQUEO " + " ".join("%s=%s" % kv for kv in ctrl.items()) + " -> INVALIDO")
        return invalido(res, "plan incompleto")
    filas = [{x["prueba"]: x for x in j["filas"]} for j in cel]
    real_ok = True
    for (f, c), (ws, real) in nul.items():
        real_ok = real_ok and real["pred_WL"] == filas[c][12]["pred_WL"]
    ctrl["REAL_EN_NULOS"] = bool(real_ok)
    valido = all(ctrl.values())
    res.update(controles=ctrl, valido=valido)
    pr("CHEQUEO " + " ".join("%s=%s" % kv for kv in ctrl.items()) + " -> " + ("VALIDO" if valido else "INVALIDO"))
    D1 = [[filas[c][p]["WL"] - filas[c][p]["RIDGE"] for p in PRIMARIA] for c in range(NCEL)]
    D2 = [[filas[c][p]["WL"] - filas[c][p]["W_elegida"] for p in PRIMARIA] for c in range(NCEL)]
    for c in range(NCEL):
        pr("CELDA c%d %s WL=%.4f RIDGE=%.4f W_elegida=%.4f (media de las pruebas 12 a 21)" % (
            c, cel[c]["celda"], *[float(np.mean([filas[c][p][k] for p in PRIMARIA])) for k in ("WL", "RIDGE", "W_elegida")]))
    b1, b2 = boot(D1, D2)
    cerca = etiqueta(b1["lo"], b1["hi"], -MARGEN)
    paga = etiqueta(b2["lo"], b2["hi"], MARGEN)
    pr("PRIMARIA WL-RIDGE D1=%+.4f IC=[%+.4f, %+.4f] umbral=-0.01 -> H_LECTOR_CERCA %s%s" % (
        b1["D"], b1["lo"], b1["hi"], cerca, " (GANA_AL_RIDGE: el piso pasa 0)" if b1["lo"] > 0 else ""))
    pr("PRIMARIA WL-W D2=%+.4f IC=[%+.4f, %+.4f] umbral=+0.01 -> H_LECTOR_PAGA %s" % (b2["D"], b2["lo"], b2["hi"], paga))
    com = {}
    for (f, c), (ws, real) in sorted(nul.items()):
        x = cableado(filas[c][12]["WL"], ws)
        com["%s_c%d" % (f, c)] = x
        pr("NULOS %s c%d real=%.4f media=%.4f max=%.4f delta=%+.4f p=%.4f -> %s" % (
            f, c, filas[c][12]["WL"], float(np.mean(ws)), x["maximo"], x["delta"], x["p"],
            "SUPERA" if x["supera"] else ("NO_SUPERA" if x["refuta"] else "SIN_DECIDIR")))
    cab = veredicto_cableado(com)
    v = dict(H_LECTOR_CERCA=cerca, H_LECTOR_PAGA=paga, H_LECTOR_CABLEADO=cab)
    if not valido:
        v = {h: "INVALIDO" for h in HIPS}
    pr("VEREDICTO " + " ".join("%s=%s" % (h, v[h]) for h in HIPS))
    res.update(primaria=dict(D1=b1, D2=b2), nulos=com, **v,
               aciertos={str(c): [filas[c][p]["WL"] for p in PRIMARIA] for c in range(NCEL)})
    return res


def cotejar(pa, pb):
    A, Bb = json.load(open(pa)), json.load(open(pb))
    if "primaria" not in A or "primaria" not in Bb:
        pr("COTEJO imposible: falta la primaria en algun agregado")
        return 3
    v = {}
    for h in ("H_LECTOR_CERCA", "H_LECTOR_PAGA"):
        v[h] = A[h] if A[h] == Bb[h] else "SIN_DECIDIR"
        pr("COTEJO %s %s / %s -> %s" % (h, A[h], Bb[h], "IGUAL" if A[h] == Bb[h] else "NO_SE_REPLICA"))
    dif = [abs(x - y) for c in range(NCEL) for x, y in zip(A["aciertos"][str(c)], Bb["aciertos"][str(c)])]
    pr("COTEJO aciertos iguales %d/%d max_dif=%.4f" % (sum(x == 0 for x in dif), len(dif), max(dif)))
    v["H_LECTOR_CABLEADO"] = A["H_LECTOR_CABLEADO"]
    if not (A.get("valido") is True and Bb.get("valido") is True):
        v = {h: "INVALIDO" for h in HIPS}
    pr("VEREDICTO_COTEJADO " + " ".join("%s=%s" % (h, v[h]) for h in HIPS) + " (CABLEADO: solo Actions)")
    return 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", default=None)
    ap.add_argument("--cotejar", nargs=2, default=None)
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
