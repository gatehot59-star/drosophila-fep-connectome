#!/usr/bin/env python3
"""Prueba del agregador de H_DEBILES con datos sinteticos (respuesta 2026-10-14-016): cada caso tiene que dar lo
esperado.

Casos: PESA_CUALES (la mezcla cae al nucleo), PESA_CUANTAS (la mezcla da como R2), PESAN_LAS_DOS (la mezcla queda a
mitad de camino), ROZA (-0,95 puntos con ruido: SIN_DECIDIR, no se lee), MEZCLA_DISTINTA (dos huellas: INVALIDO),
REAL_MAL (R2 real distinto: INVALIDO), FALTA_JSON (INVALIDO).
Uso: python3 tools/debiles/prueba_agregar_debiles.py   Salida: 0 si pasan todos.
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
import agregar_debiles as ag  # noqa: E402


def q(x):
    return round(x * 2000) / 2000


def escribir(dd, d3, dn, f, dif=0.0, ruido=0.002, huella_mal=False, real_mal=False, falta=False, semilla=0):
    rng = np.random.default_rng(semilla)
    taudn = {str(t): [0.1 + 0.001 * t] * 6 for t in ag.TAUS}
    md5 = dict(script=ag.MD5_DEB, **ag.PIN)
    nuc = dict(aristas=ag.NUCLEO[0], inhibitorias=ag.NUCLEO[1], huella=ag.NUCLEO[2])
    dns = [1, 2, 3, 4, 5, 6]
    g0 = None
    for t in ag.TAUS:
        for k, c in enumerate(ag.CELDAS):
            cs = {"3": [], "n": [], "d": []}
            rs = []
            for p in ag.PRUEBAS:
                rp = 0.92 + 0.001 * k
                w3 = q(rp + 0.01 + 0.004 * rng.standard_normal())
                wn = q(w3 - 0.046 + 0.004 * rng.standard_normal())
                wd = q(wn + f * (w3 - wn) + dif + ruido * rng.standard_normal())
                if (t, p, c) == (0, 2, "0.3|0.15"):
                    g0 = wd
                for key, w in (("3", w3), ("n", wn), ("d", wd)):
                    cs[key].append(dict(celda=c, tau=t, prueba=p, W=w, regla_propia=rp, regla40=rp - 0.02, pred_W="0"))
                rs.append(dict(celda=c, prueba=p, regla_propia=rp, regla40=rp - 0.02, pred_regla_propia="0101"))
            comun = dict(dns_root=dns, taus=[t], tau_DN={str(t): taudn[str(t)]}, reglas=rs, valido=True, humo=False)
            with open(os.path.join(d3, "factorial2_R2_CON_TASA_t%dc%d.json" % (t, k)), "w") as fh:
                json.dump(dict(comun, config="R2_CON_TASA", corridas=cs["3"]), fh)
            with open(os.path.join(dn, "nucleo_grilla_t%dc%d.json" % (t, k)), "w") as fh:
                json.dump(dict(comun, modo="grilla", corridas=cs["n"]), fh)
            if falta and (t, k) == (9, 5):
                continue
            hu = "otra" if (huella_mal and (t, k) == (4, 2)) else "h0"
            with open(os.path.join(dd, "debiles_grilla_t%dc%d.json" % (t, k)), "w") as fh:
                json.dump(dict(comun, modo="grilla", nucleo=nuc, md5=md5, mezcla=dict(k=0, huella=hu),
                               corridas=cs["d"]), fh)
    for k0 in range(0, ag.N_MEZCLAS, 5):
        mz = [dict(k=kk, acierto=(g0 if kk == 0 else 0.90 + 0.001 * kk), guarda=True) for kk in range(k0, k0 + 5)]
        j = dict(modo="mezclas", humo=False, valido=True, nucleo=nuc, md5=md5, dns_root=dns, ks=list(range(k0, k0 + 5)),
                 mezclas=mz, real_R2=None, real_nucleo=None)
        if k0 == 0:
            j["real_R2"], j["real_nucleo"] = (0.9460 if real_mal else ag.REAL_R2), ag.REAL_NUCLEO
        with open(os.path.join(dd, "debiles_mezclas_k%03d.json" % k0), "w") as fh:
            json.dump(j, fh)


def linea(out, inicio):
    return [x for x in out.splitlines() if x.startswith(inicio)][0].split("-> ")[1].split(" ")[0]


def correr(**kw):
    with tempfile.TemporaryDirectory() as dd, tempfile.TemporaryDirectory() as d3, tempfile.TemporaryDirectory() as dn:
        escribir(dd, d3, dn, **kw)
        buf = io.StringIO()
        sys.argv = ["agregar_debiles.py", dd, d3, dn]
        with contextlib.redirect_stdout(buf):
            rc = ag.main()
        out = buf.getvalue()
    return (rc, linea(out, "HIPOTESIS H_DEBILES_ESPECIFICAS"), linea(out, "HIPOTESIS H_DEBILES_SUMAN"),
            linea(out, "LECTURA"), linea(out, "VEREDICTO_GLOBAL"))


CASOS = [
    ("PESA_CUALES", dict(f=0.05), (0, "SOSTENIDA", "REFUTADA", "PESA_CUALES", "VALIDO")),
    ("PESA_CUANTAS", dict(f=1.0), (0, "REFUTADA", "SOSTENIDA", "PESA_CUANTAS", "VALIDO")),
    ("PESAN_LAS_DOS", dict(f=0.5), (0, "SOSTENIDA", "SOSTENIDA", "PESAN_LAS_DOS", "VALIDO")),
    ("ROZA", dict(f=1.0, dif=-0.0095, ruido=0.012), (0, "SIN_DECIDIR", "SOSTENIDA", "NO_SE_LEE", "VALIDO")),
    ("MEZCLA_DISTINTA", dict(f=0.5, huella_mal=True), (1, "NO_EVALUABLE", "NO_EVALUABLE", "NO_SE_LEE", "INVALIDO")),
    ("REAL_MAL", dict(f=0.5, real_mal=True), (1, "NO_EVALUABLE", "NO_EVALUABLE", "NO_SE_LEE", "INVALIDO")),
    ("FALTA_JSON", dict(f=0.5, falta=True), (1, "NO_EVALUABLE", "NO_EVALUABLE", "NO_SE_LEE", "INVALIDO")),
]


def main():
    ok = 0
    for nombre, kw, esperado in CASOS:
        got = correr(**kw)
        bien = got == esperado
        ok += bien
        print("CASO %s esperado=%s obtenido=%s -> %s" % (nombre, esperado, got, "PASA" if bien else "FALLA"))
    print("PRUEBA_AGREGADOR_DEBILES %s %d/%d" % ("PASA" if ok == len(CASOS) else "FALLA", ok, len(CASOS)))
    return 0 if ok == len(CASOS) else 1


if __name__ == "__main__":
    sys.exit(main())
