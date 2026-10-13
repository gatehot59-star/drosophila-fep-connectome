#!/usr/bin/env python3
"""Agrega los 9 json de factorial_mosca.py y dicta los veredictos sellados (respuesta 2026-10-12-019).

Por configuracion: H3 (W contra la regla a mano) por celda con Holm sobre las 6 celdas; PIERDE si alguna celda
PEOR, SUPERA si ninguna PEOR y alguna MEJOR, IGUALA si ninguna; INVALIDA si fallo algun control.
Contrastes de factor (McNemar por celda entre los aciertos de W de las dos configuraciones, Holm sobre 6):
AYUDA si alguna MEJOR y ninguna PEOR, DANA al reves, MIXTO si las dos, EMPATE si ninguna; NO_EVALUABLE si una
de las dos es invalida.
Global: ALGUN FACTOR CIERRA LA BRECHA si al menos una configuracion valida IGUALA o SUPERA; NINGUNA CIERRA LA
BRECHA si no. Falsador pre-registrado: NINGUNA CIERRA LA BRECHA. Instrumento global VALIDO solo si M46_TASA es
valida (REPRODUCE_015). Uso: python3 agregar_factorial.py <directorio con los json>
"""
import json
import os
import sys

import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(AQUI, "..", "escape_aterrizaje"))
sys.path.insert(0, AQUI)
import tarea_mosca as tm  # noqa: E402
import factorial_mosca as fm  # noqa: E402

base, ept = tm.base, tm.ept
CONTRASTES = (
    ("RECORTE_TASA", "R1_CON_TASA", "M46_TASA"), ("RECORTE_LIQ", "R1_CON_LIQ", "M46_LIQ"),
    ("RECORTE_LIF", "R1_CON_LIF", "M46_LIF"), ("INHIB_TASA", "R1_CON_TASA", "R1_SIN_TASA"),
    ("INHIB_LIQ", "R1_CON_LIQ", "R1_SIN_LIQ"), ("INHIB_LIF", "R1_CON_LIF", "R1_SIN_LIF"),
    ("LIQ_M46", "M46_LIQ", "M46_TASA"), ("LIF_M46", "M46_LIF", "M46_TASA"),
    ("LIQ_R1", "R1_CON_LIQ", "R1_CON_TASA"), ("LIF_R1", "R1_CON_LIF", "R1_CON_TASA"),
)


def clase(b, c, p_adj):
    if b > c and p_adj < tm.ALFA:
        return "MEJOR"
    if c > b and p_adj < tm.ALFA:
        return "PEOR"
    return "EMPATE"


def main():
    d = sys.argv[1]
    R = {}
    for c in fm.CONFIGS:
        ruta = os.path.join(d, "factorial_%s.json" % c)
        if os.path.exists(ruta):
            with open(ruta) as f:
                R[c] = json.load(f)
            print("JSON %s md5=%s valido=%s humo=%s" % (c, base.md5(ruta), R[c]["valido"], R[c]["humo"]))
        else:
            print("JSON %s FALTA" % c)
    claves = ["%.1f|%.2f" % k for k in fm.CELDAS]
    n_test = len(next(iter(R.values()))["celdas"][claves[0]]["pred_W"]) if R else 0
    yte = tm.generar(n_test, 2)["y"]
    ver = {}
    for c in fm.CONFIGS:
        if c not in R or not R[c]["valido"]:
            ver[c] = "INVALIDA"
            print("CONFIG %s -> INVALIDA" % c)
            continue
        ce = R[c]["celdas"]
        adj = ept.holm([ce[k]["H3_p"] for k in claves])
        cl = [clase(ce[k]["H3_W"], ce[k]["H3_regla"], a) for k, a in zip(claves, adj)]
        ver[c] = "PIERDE" if "PEOR" in cl else ("SUPERA" if "MEJOR" in cl else "IGUALA")
        print("CONFIG %s W=%s regla=%s H3_holm=%s -> %s | contra el diseno %s" % (
            c, ",".join("%.4f" % ce[k]["W"] for k in claves), ",".join("%.4f" % ce[k]["regla"] for k in claves),
            ",".join("%s(%.3g)" % (x, a) for x, a in zip(cl, adj)), ver[c], "PIERDE" if ver[c] == "PIERDE" else ver[c]))
        nu = R[c]["nulos"]
        print("NULOS_DESCRIPTIVO %s W=%.4f SL media=%.4f p_sup=%.4f T media=%.4f p_sup=%.4f" % (
            c, nu["W"], np.mean(nu["SL"]), nu["p_sup_SL"], np.mean(nu["T"]), nu["p_sup_T"]))
    for nom, ca, cb in CONTRASTES:
        if ver.get(ca) == "INVALIDA" or ver.get(cb) == "INVALIDA":
            print("CONTRASTE %s %s contra %s -> NO_EVALUABLE" % (nom, ca, cb))
            continue
        bs, cs, ps = [], [], []
        for k in claves:
            oka = np.array(R[ca]["celdas"][k]["pred_W"]) == yte
            okb = np.array(R[cb]["celdas"][k]["pred_W"]) == yte
            b, c_, p = base.mcnemar(oka, okb)
            bs.append(b); cs.append(c_); ps.append(p)
        adj = ept.holm(ps)
        cl = [clase(b, c_, a) for b, c_, a in zip(bs, cs, adj)]
        v = "MIXTO" if ("MEJOR" in cl and "PEOR" in cl) else ("AYUDA" if "MEJOR" in cl else ("DANA" if "PEOR" in cl else "EMPATE"))
        print("CONTRASTE %s %s contra %s celdas=%s -> %s" % (nom, ca, cb, ",".join("%d/%d(%.3g)" % (b, c_, a) for b, c_, a in zip(bs, cs, adj)), v))
    validas = [c for c in fm.CONFIGS if ver.get(c) not in (None, "INVALIDA")]
    cierran = [c for c in validas if ver[c] in ("IGUALA", "SUPERA")]
    ancla = ver.get("M46_TASA") not in (None, "INVALIDA")
    medias = {c: float(np.mean([R[c]["celdas"][k]["W"] for k in claves])) for c in validas}
    if medias:
        mejor = max(medias, key=medias.get)
        print("DESCRIPTIVO mejor_config_por_media=%s %.4f | medias=%s" % (mejor, medias[mejor], ",".join("%s %.4f" % kv for kv in medias.items())))
    print("CHEQUEO INSTRUMENTO_GLOBAL ancla_M46_TASA_valida=%s configuraciones_validas=%d/9 -> %s" % (
        ancla, len(validas), "VALIDO" if ancla else "INVALIDO"))
    glob = ("ALGUN FACTOR CIERRA LA BRECHA (%s)" % ",".join(cierran)) if cierran else "NINGUNA CIERRA LA BRECHA"
    print("VEREDICTO_GLOBAL -> %s" % glob)
    return 0 if ancla else 3


if __name__ == "__main__":
    sys.exit(main())
