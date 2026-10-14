#!/usr/bin/env python3
"""Prueba del agregador de H_TAU con datos sinteticos (respuesta 2026-10-14-002): cada caso tiene que dar lo esperado.

Casos: GANA (+3 puntos: SOSTENIDA), EMPATA (0: REFUTADA), ROZA (+1,05 con ruido: SIN_DECIDIR), FALTA_CELDA (5 json:
NO_EVALUABLE e INVALIDO), REPRO_FALSO (INVALIDO), MD5_DISTINTO (INVALIDO).
Uso: python3 tools/htau/prueba_agregar_htau.py   Salida: 0 si pasan todos.
"""
import contextlib
import io
import json
import os
import sys
import tempfile

import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import agregar_htau as ag  # noqa: E402


def escribir(carpeta, dif, ruido, falta=None, repro_ok=True, md5=None, semilla=0):
    rng = np.random.default_rng(semilla)
    for k, c in enumerate(ag.CELDAS):
        if c == falta:
            continue
        corr = []
        for p in ag.PRUEBAS:
            rp = 0.92 + 0.002 * k
            we = round((rp + dif + ruido * rng.standard_normal()) * 2000) / 2000
            corr.append(dict(prueba=p, W_elegida=we, W_peor=rp - 0.02, regla_propia=rp, regla40=rp - 0.03,
                             pred_elegida="0", pred_peor="0", pred_regla_propia="0"))
        j = dict(experimento="H_TAU", celda=c, candidatas=ag.CANDIDATAS, pruebas=ag.PRUEBAS, pliegues=ag.PLIEGUES,
                 humo=False, valido=True, dns_root=[1, 2, 3, 4, 5, 6], corridas=corr, elegida=10 + k, peor=19,
                 validacion={str(s): 0.9 for s in ag.CANDIDATAS},
                 md5=dict(script=md5 or ag.MD5_HTAU, **ag.PIN),
                 repro=(dict(W=0.9465, regla_propia=0.9375, regla40=0.9235, igual=repro_ok) if c == "0.3|0.15" else None))
        with open(os.path.join(carpeta, "htau_c%d.json" % k), "w") as f:
            json.dump(j, f)


def correr(**kw):
    with tempfile.TemporaryDirectory() as d:
        escribir(d, **kw)
        buf = io.StringIO()
        sys.argv = ["agregar_htau.py", d]
        with contextlib.redirect_stdout(buf):
            rc = ag.main()
        out = buf.getvalue()
    hip = [x for x in out.splitlines() if x.startswith("HIPOTESIS H_TAU")][0].split("-> ")[1]
    glob_ = [x for x in out.splitlines() if x.startswith("VEREDICTO_GLOBAL")][0].split("-> ")[1].split(" ")[0]
    return rc, hip, glob_


CASOS = [
    ("GANA", dict(dif=0.03, ruido=0.004), (0, "SOSTENIDA", "VALIDO")),
    ("EMPATA", dict(dif=0.0, ruido=0.002), (0, "REFUTADA", "VALIDO")),
    ("ROZA", dict(dif=0.0105, ruido=0.02), (0, "SIN_DECIDIR", "VALIDO")),
    ("FALTA_CELDA", dict(dif=0.03, ruido=0.004, falta="0.6|0.45"), (1, "NO_EVALUABLE", "INVALIDO")),
    ("REPRO_FALSO", dict(dif=0.03, ruido=0.004, repro_ok=False), (1, "NO_EVALUABLE", "INVALIDO")),
    ("MD5_DISTINTO", dict(dif=0.03, ruido=0.004, md5="0" * 32), (1, "NO_EVALUABLE", "INVALIDO")),
]


def main():
    ok = 0
    for nombre, kw, esperado in CASOS:
        got = correr(**kw)
        bien = got == esperado
        ok += bien
        print("CASO %s esperado=%s obtenido=%s -> %s" % (nombre, esperado, got, "PASA" if bien else "FALLA"))
    print("PRUEBA_AGREGADOR_HTAU %s %d/%d" % ("PASA" if ok == len(CASOS) else "FALLA", ok, len(CASOS)))
    return 0 if ok == len(CASOS) else 1


if __name__ == "__main__":
    sys.exit(main())
