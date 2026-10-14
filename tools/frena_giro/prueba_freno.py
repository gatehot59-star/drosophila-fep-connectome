#!/usr/bin/env python3
"""Prueba de freno_mosca.calcular con grafos de juguete (respuesta 2026-10-14-023). Sin datos reales.

E1 CONTRA: una interneurona inhibitoria alimentada por LPLC1 del otro lado frena al objetivo -> M3_CONTRA CANDIDATO,
   M4/M5/M6 DESCARTADO, DNp07 directo solo de un lado -> ASIMETRICO, H_FRENO SOSTENIDA.
E2 IPSI: la misma interneurona alimentada por LPLC1 del MISMO lado y sin DNp07 -> M3 DESCARTADO, H_FRENO REFUTADA.
E3 SIN_POSITIVO: sin LPLC1 directo sobre el objetivo -> INVALIDO.
E4 BILATERAL: interneurona que recibe de LPLC2 de los dos lados -> M6 CANDIDATO, y tambien M3 (no son excluyentes).
E5 OBJETIVO_INEXISTENTE -> None.
Sale 0 si pasan todas.
"""
import os
import sys

import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import freno_mosca as fm  # noqa: E402


def armar(contra=True, dnp07=True, positivo=True, bilateral=False):
    n, e = [], []

    def neu(rid, t, s, sc, nt):
        n.append(dict(root_id=rid, cell_type=t, side=s, super_class=sc, top_nt=nt))

    neu(1, "DNx", "left", "descending", "acetylcholine")
    neu(2, "DNx", "right", "descending", "acetylcholine")
    dns = [(1, "left"), (2, "right")]
    for k in range(20):
        for j, s in enumerate(fm.LADOS):
            rid = 100 + 2 * k + j
            neu(rid, "DNo%d" % k, s, "descending", "acetylcholine")
            dns.append((rid, s))
    for j, s in enumerate(fm.LADOS):
        neu(300 + j, "DNp07", s, "descending", "acetylcholine")
        neu(310 + j, "DNp01", s, "descending", "acetylcholine")
        dns += [(300 + j, s), (310 + j, s)]
    tipos = ("LPLC1", "LPLC2", "LPLC4", "LC4")
    vid = {}
    for i, t in enumerate(tipos):
        for j, s in enumerate(fm.LADOS):
            vid[(t, s)] = 400 + 2 * i + j
            neu(vid[(t, s)], t, s, "visual_projection", "acetylcholine")
    neu(501, "Z", "left", "central", "gaba")
    neu(502, "Z", "right", "central", "gaba")
    neu(503, "Y", "left", "central", "acetylcholine")
    neu(601, "GC", "left", "central", "gaba")
    neu(602, "GC", "right", "central", "gaba")
    neu(701, "GB", "left", "central", "glutamate")
    neu(702, "GB", "right", "central", "glutamate")
    for rid, s in dns:
        z = 501 if s == "left" else 502
        e.append((z, rid, 50 if rid in (1, 2) else 150, -1))
        e.append((503, rid, 150, 1))
    for rid, s, gc, gb in ((1, "left", 601, 701), (2, "right", 602, 702)):
        o = fm.OPUESTO[s]
        if positivo:
            e.append((vid[("LPLC1", s)], rid, 100, 1))
        e.append((vid[("LPLC1", o if contra else s)], gc, 10, 1))
        e.append((gc, rid, 50, -1))
        if bilateral:
            e.append((vid[("LPLC2", "left")], gb, 10, 1))
            e.append((vid[("LPLC2", "right")], gb, 10, 1))
            e.append((gb, rid, 40, -1))
    if dnp07:
        e.append((300, 1, 10, -1))
    a = pd.DataFrame(n)
    c = pd.DataFrame(e, columns=["Presynaptic_ID", "Postsynaptic_ID", "Connectivity", "Excitatory"])
    return a, c


def main():
    res = []

    def chk(nombre, ok, extra=""):
        res.append(bool(ok))
        print("PRUEBA %s %s %s" % (nombre, "PASA" if ok else "FALLA", extra))

    r = fm.calcular(*armar(), "DNx")
    v = {m: r["mecanismos"][m]["veredicto"] for m in r["mecanismos"]}
    chk("E1_CONTRA", v["M3_CONTRA"] == "CANDIDATO" and v["M4_LPLC4"] == "DESCARTADO" and v["M5_DNP07"] == "DESCARTADO"
        and v["M6_BILATERAL"] == "DESCARTADO" and v["M1_DNP07"] == "ASIMETRICO" and v["M1_DNP01"] == "AUSENTE"
        and v["M2_OPUESTA"] == "AUSENTE" and r["control_positivo"]["pasa"] and r["H_FRENO"] == "SOSTENIDA",
        "%s %s" % (v, r["H_FRENO"]))
    cl = r["mecanismos"]["M3_CONTRA"]["por_lado"]["left"]
    chk("E1_CUOTA_EXACTA", cl["sinapsis"] == 50 and cl["inhibitorias_totales"] == 110 and abs(cl["cuota"] - 50 / 110.0) < 1e-12
        and cl["percentil"] == 1.0, cl)
    r = fm.calcular(*armar(contra=False, dnp07=False), "DNx")
    v = {m: r["mecanismos"][m]["veredicto"] for m in r["mecanismos"]}
    chk("E2_IPSI_REFUTADA", v["M3_CONTRA"] == "DESCARTADO" and r["H_FRENO"] == "REFUTADA", "%s %s" % (v, r["H_FRENO"]))
    r = fm.calcular(*armar(positivo=False), "DNx")
    chk("E3_SIN_POSITIVO_INVALIDO", r["H_FRENO"] == "INVALIDO" and not r["control_positivo"]["pasa"], r["H_FRENO"])
    r = fm.calcular(*armar(contra=False, dnp07=False, bilateral=True), "DNx")
    v = {m: r["mecanismos"][m]["veredicto"] for m in r["mecanismos"]}
    chk("E4_BILATERAL", v["M6_BILATERAL"] == "CANDIDATO" and v["M3_CONTRA"] == "CANDIDATO" and r["H_FRENO"] == "SOSTENIDA",
        "%s %s" % (v, r["H_FRENO"]))
    chk("E5_OBJETIVO_INEXISTENTE", fm.calcular(*armar(), "DNnada") is None)
    print("RESUMEN %d/%d" % (sum(res), len(res)))
    return 0 if all(res) else 1


if __name__ == "__main__":
    sys.exit(main())
