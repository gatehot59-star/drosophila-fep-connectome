#!/usr/bin/env python3
"""Prueba de H_TOPO_FIEL sin datos reales (respuesta 2026-10-14-021, paso B del sello).

1 a 4: la regla de decision con conteos sinteticos (igual, pierde 5 puntos, ambiguo, gana).
5: determinismo con la misma semilla.
6: final(): si el control no sale REFUTADA, el veredicto es INVALIDO.
7: PAR_MINIMO_FIEL: escape_fiel.topo es escape.topo salvo las dos lineas de giro, y esas leen solo el lado propio.
8: PAR_MINIMO_CRUZADO: escape_cruzado.topo es escape_fiel.topo salvo las acciones de giro, intercambiadas.
Sale 0 si pasan las 8.
"""
import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
HERR = os.path.dirname(AQUI)
sys.path.insert(0, os.path.join(HERR, "topo"))
sys.path.insert(0, AQUI)
import topo  # noqa: E402
import decidir_fiel as dfl  # noqa: E402


def leer(r):
    return topo.parsear(open(r, encoding="utf-8").read())


def sin_renglon(p):
    q = dict(p)
    q.pop("reflejo")
    q["lineas"] = [{k: v for k, v in ln.items() if k != "renglon"} for ln in p["lineas"]]
    return q


def main():
    res = []

    def chk(nombre, ok, extra=""):
        res.append(bool(ok))
        print("PRUEBA %s %s %s" % (nombre, "PASA" if ok else "FALLA", extra))

    r = dfl.decidir([[100, 1800, 100]] * 6, 4000, 1)
    chk("IGUAL_SOSTENIDA", r["veredicto"] == "SOSTENIDA" and abs(r["d"]) < 1e-12, r)
    r = dfl.decidir([[150, 1800, 50]] * 6, 4000, 1)
    chk("PIERDE5_REFUTADA", r["veredicto"] == "REFUTADA" and abs(r["d"] + 0.05) < 1e-12, r)
    r = dfl.decidir([[210, 1590, 200]] * 6, 4000, 1)
    chk("AMBIGUO_SIN_DECIDIR", r["veredicto"] == "SIN_DECIDIR" and r["ic90"][0] < -0.01 < r["ic90"][1], r)
    r = dfl.decidir([[50, 1800, 150]] * 6, 4000, 1)
    chk("GANA_SOSTENIDA", r["veredicto"] == "SOSTENIDA" and r["d"] > 0, r)
    r1 = dfl.decidir([[120, 1700, 180]] * 6, 3000, 7)
    r2 = dfl.decidir([[120, 1700, 180]] * 6, 3000, 7)
    chk("DETERMINISTA", r1 == r2)
    chk("FINAL_INVALIDO", dfl.final("SOSTENIDA", "SIN_DECIDIR") == "INVALIDO" and
        dfl.final("SOSTENIDA", "SOSTENIDA") == "INVALIDO" and dfl.final("REFUTADA", "REFUTADA") == "REFUTADA" and
        dfl.final("SIN_DECIDIR", "REFUTADA") == "SIN_DECIDIR")

    pv = sin_renglon(leer(os.path.join(HERR, "topo", "escape.topo")))
    pf = sin_renglon(leer(os.path.join(AQUI, "escape_fiel.topo")))
    px = sin_renglon(leer(os.path.join(AQUI, "escape_cruzado.topo")))
    igual_resto = all(pv[k] == pf[k] for k in pv if k != "lineas")
    dif = [i for i in range(len(pv["lineas"])) if pv["lineas"][i] != pf["lineas"][i]]
    ok7 = igual_resto and len(pv["lineas"]) == len(pf["lineas"]) == 6 and dif == [4, 5]
    for i in dif:
        lf, lv = pf["lineas"][i], pv["lineas"][i]
        lado = lf["nombre"].split("@")[1]
        ok7 = ok7 and lf["accion"] == lv["accion"] and lf["estado"] == lv["estado"] and len(lf["terminos"]) == 1
        ok7 = ok7 and lf["terminos"][0] == lv["terminos"][0] and all(ld == lado for _, ld in lf["terminos"][0][1])
    chk("PAR_MINIMO_FIEL", ok7, "lineas distintas=%s" % dif)
    dif2 = [i for i in range(6) if pf["lineas"][i] != px["lineas"][i]]
    ok8 = all(pf[k] == px[k] for k in pf if k != "lineas") and dif2 == [4, 5]
    for i in dif2:
        a, b = dict(pf["lineas"][i]), dict(px["lineas"][i])
        ok8 = ok8 and {a.pop("accion"), b.pop("accion")} == {"girar_der", "girar_izq"} and a == b
    chk("PAR_MINIMO_CRUZADO", ok8, "lineas distintas=%s" % dif2)
    print("RESUMEN %d/%d" % (sum(res), len(res)))
    return 0 if all(res) else 1


if __name__ == "__main__":
    sys.exit(main())
