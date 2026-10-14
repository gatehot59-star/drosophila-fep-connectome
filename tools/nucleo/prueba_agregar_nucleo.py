#!/usr/bin/env python3
"""Prueba del agregador del nucleo con datos sinteticos (respuesta 2026-10-14-002): cada caso tiene que dar lo esperado.

Casos: IGUAL (el nucleo como R2 y mejor que sus nulos: SOSTENIDA), PIERDE (-3 puntos: REFUTADA), ROZA (-0,95 con
ruido: SIN_DECIDIR), NULOS_GANAN (10 SL iguales o mejores: REFUTADA), REGLA_DISTINTA (INVALIDO), FALTA_JSON (INVALIDO).
Uso: python3 tools/nucleo/prueba_agregar_nucleo.py   Salida: 0 si pasan todos.
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
import agregar_nucleo as ag  # noqa: E402


def escribir(dn, d3, dif, ruido, nulos_arriba=0, regla_mal=False, falta=False, semilla=0):
    rng = np.random.default_rng(semilla)
    taudn = {str(t): [0.1 + 0.001 * t] * 6 for t in ag.TAUS}
    md5 = dict(script=ag.MD5_NUCLEO, **ag.PIN)
    nuc = dict(aristas=ag.NUCLEO[0], inhibitorias=ag.NUCLEO[1], huella=ag.NUCLEO[2])
    real = None
    for t in ag.TAUS:
        for k, c in enumerate(ag.CELDAS):
            c3, c4, r3, r4 = [], [], [], []
            for p in ag.PRUEBAS:
                rp = 0.92 + 0.001 * k
                w3 = round((rp + 0.01 + 0.004 * rng.standard_normal()) * 2000) / 2000
                w4 = round((w3 + dif + ruido * rng.standard_normal()) * 2000) / 2000
                if (t, p, c) == (0, 2, "0.3|0.15"):
                    real = w4
                c3.append(dict(celda=c, tau=t, prueba=p, W=w3, regla_propia=rp, regla40=rp - 0.02, pred_W="0"))
                c4.append(dict(celda=c, tau=t, prueba=p, W=w4, regla_propia=rp, regla40=rp - 0.02, pred_W="0"))
                pred = "0101"
                r3.append(dict(celda=c, prueba=p, regla_propia=rp, regla40=rp - 0.02, pred_regla_propia=pred))
                r4.append(dict(celda=c, prueba=p, regla_propia=rp, regla40=rp - 0.02,
                               pred_regla_propia=("0111" if (regla_mal and (t, p, c) == (3, 5, "0.6|0.15")) else pred)))
            j3 = dict(config="R2_CON_TASA", taus=[t], celdas=[c], dns_root=[1, 2, 3, 4, 5, 6],
                      tau_DN={str(t): taudn[str(t)]}, corridas=c3, reglas=r3, valido=True, humo=False)
            with open(os.path.join(d3, "factorial2_R2_CON_TASA_t%dc%d.json" % (t, k)), "w") as f:
                json.dump(j3, f)
            if falta and (t, k) == (9, 5):
                continue
            j4 = dict(modo="grilla", humo=False, valido=True, nucleo=nuc, md5=md5, dns_root=[1, 2, 3, 4, 5, 6],
                      taus=[t], tau_DN={str(t): taudn[str(t)]}, corridas=c4, reglas=r4)
            with open(os.path.join(dn, "nucleo_grilla_t%dc%d.json" % (t, k)), "w") as f:
                json.dump(j4, f)
    for tipo in ("SL", "T"):
        for k0 in range(0, 50, 5):
            nul = []
            for kk in range(k0, k0 + 5):
                arriba = tipo == "SL" and kk < nulos_arriba
                nul.append(dict(k=kk, acierto=(real + 0.001) if arriba else 0.70 + 0.001 * kk, guarda=True))
            j = dict(modo="nulos", humo=False, valido=True, nucleo=nuc, md5=md5, tipo=tipo, ks=list(range(k0, k0 + 5)),
                     nulos=nul, real=(real if k0 == 0 else None))
            with open(os.path.join(dn, "nulos_nucleo_%s_k%03d.json" % (tipo, k0)), "w") as f:
                json.dump(j, f)


def correr(**kw):
    with tempfile.TemporaryDirectory() as dn, tempfile.TemporaryDirectory() as d3:
        escribir(dn, d3, **kw)
        buf = io.StringIO()
        sys.argv = ["agregar_nucleo.py", dn, d3]
        with contextlib.redirect_stdout(buf):
            rc = ag.main()
        out = buf.getvalue()
    hip = [x for x in out.splitlines() if x.startswith("HIPOTESIS H_CONSENSO")][0].split("-> ")[1]
    glob_ = [x for x in out.splitlines() if x.startswith("VEREDICTO_GLOBAL")][0].split("-> ")[1].split(" ")[0]
    return rc, hip, glob_


CASOS = [
    ("IGUAL", dict(dif=0.0, ruido=0.002), (0, "SOSTENIDA", "VALIDO")),
    ("PIERDE", dict(dif=-0.03, ruido=0.002), (0, "REFUTADA", "VALIDO")),
    ("ROZA", dict(dif=-0.0095, ruido=0.012), (0, "SIN_DECIDIR", "VALIDO")),
    ("NULOS_GANAN", dict(dif=0.0, ruido=0.002, nulos_arriba=10), (0, "REFUTADA", "VALIDO")),
    ("REGLA_DISTINTA", dict(dif=0.0, ruido=0.002, regla_mal=True), (1, "NO_EVALUABLE", "INVALIDO")),
    ("FALTA_JSON", dict(dif=0.0, ruido=0.002, falta=True), (1, "NO_EVALUABLE", "INVALIDO")),
]


def main():
    ok = 0
    for nombre, kw, esperado in CASOS:
        got = correr(**kw)
        bien = got == esperado
        ok += bien
        print("CASO %s esperado=%s obtenido=%s -> %s" % (nombre, esperado, got, "PASA" if bien else "FALLA"))
    print("PRUEBA_AGREGADOR_NUCLEO %s %d/%d" % ("PASA" if ok == len(CASOS) else "FALLA", ok, len(CASOS)))
    return 0 if ok == len(CASOS) else 1


if __name__ == "__main__":
    sys.exit(main())
