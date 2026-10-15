#!/usr/bin/env python3
"""Prueba del agregador de H_TAU_LIBRE con datos sinteticos (respuesta 2026-10-14-040). Incluye un rojo a proposito.

Salida 0 si todos los casos dan lo esperado.
"""
import io
import json
import os
import sys
import tempfile
from contextlib import redirect_stdout

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import agregar_taulibre as ag  # noqa: E402

RES = []


def chequeo(nombre, ok):
    RES.append(bool(ok))
    print("PRUEBA %s -> %s" % (nombre, "OK" if ok else "FALLA"), flush=True)


def armar(carpeta, real, nulo, humo_en=None, faltar=None, repro=True, tau_mal=False):
    """real(c, tau) y nulo(f, c, k) devuelven WL."""
    for c, t0 in ag.REALES:
        taus = list(range(t0, t0 + 5))
        d = dict(valido=True, humo=(humo_en == "reales"), local=False, md5_script="x", taus=taus,
                 controles=dict(PIN=True, REPRO_LECTOR=repro) if t0 == 20 else dict(PIN=True),
                 reales=[dict(tau=t, WL=real(c, t)) for t in taus], repro=dict(WL=0.99) if t0 == 20 else None)
        json.dump(d, open(os.path.join(carpeta, "reales_c%d_t%d.json" % (c, t0)), "w"))
    for f in ag.FAMILIAS:
        for c in ag.CELDAS:
            for k0 in ag.K0S:
                ns = [dict(k=k, tau=ag.tau_de_k(k) + (1 if tau_mal and k == 3 else 0), WL=nulo(f, c, k))
                      for k in range(k0, k0 + 10)]
                d = dict(valido=True, humo=False, local=False, md5_script="x", controles=dict(PIN=True), nulos=ns)
                json.dump(d, open(os.path.join(carpeta, "nulos_%s_c%d_k%03d.json" % (f, c, k0)), "w"))
    if faltar:
        os.remove(os.path.join(carpeta, faltar))


def caso(**kw):
    with tempfile.TemporaryDirectory() as d:
        armar(d, **kw)
        buf = io.StringIO()
        with redirect_stdout(buf):
            r = ag.agregar(d)
    return r


def main():
    # tau_de_k: cada tau fresca la usan exactamente 4 nulos
    cuenta = {t: sum(1 for k in range(40) if ag.tau_de_k(k) == t) for t in ag.TAUS}
    chequeo("TAU_DE_K 4 nulos por tau", all(v == 4 for v in cuenta.values()) and sorted(cuenta) == list(range(20, 30)))
    r = caso(real=lambda c, t: 0.99, nulo=lambda f, c, k: 0.90)
    chequeo("CASO_SOSTENIDA", r["veredicto"] == "SOSTENIDA" and all(x["p"] == 1 / 41 for x in r["combinaciones"].values()))
    r = caso(real=lambda c, t: 0.99, nulo=lambda f, c, k: 0.985)
    chequeo("CASO_MARGEN refuta (delta medio punto)", r["veredicto"] == "REFUTADA")
    r = caso(real=lambda c, t: 0.99, nulo=lambda f, c, k: 0.995 if (f, c, k) == ("SL", 2, 7) else 0.90)
    chequeo("CASO_UN_NULO_IGUAL p=2/41 supera", r["veredicto"] == "SOSTENIDA" and
            abs(r["combinaciones"]["SL_c2"]["p"] - 2 / 41) < 1e-12)
    r = caso(real=lambda c, t: 0.99, nulo=lambda f, c, k: 0.995 if (f, c) == ("T", 5) and k in (1, 2) else 0.90)
    chequeo("CASO_DOS_NULOS p=3/41 sin decidir", r["veredicto"] == "SIN_DECIDIR")
    # apareo: con tau 20 el real cae a 0,95 y sus 4 nulos dan 0,96; sin aparear el real medio igual le ganaria
    r = caso(real=lambda c, t: 0.95 if t == 20 else 0.99,
             nulo=lambda f, c, k: 0.96 if ag.tau_de_k(k) == 20 else 0.90)
    chequeo("CASO_APAREO p=5/41 refuta (el apareo cuenta)", r["veredicto"] == "REFUTADA" and
            all(abs(x["p"] - 5 / 41) < 1e-12 for x in r["combinaciones"].values()))
    r = caso(real=lambda c, t: 0.99, nulo=lambda f, c, k: 0.90, faltar="nulos_T_c5_k030.json")
    chequeo("CASO_FALTA invalido", r["veredicto"] == "INVALIDO")
    r = caso(real=lambda c, t: 0.99, nulo=lambda f, c, k: 0.90, humo_en="reales")
    chequeo("CASO_HUMO invalido", r["veredicto"] == "INVALIDO")
    r = caso(real=lambda c, t: 0.99, nulo=lambda f, c, k: 0.90, repro=False)
    chequeo("CASO_REPRO_FALSO invalido", r["veredicto"] == "INVALIDO")
    r = caso(real=lambda c, t: 0.99, nulo=lambda f, c, k: 0.90, tau_mal=True)
    chequeo("CASO_TAU_MAL invalido", r["veredicto"] == "INVALIDO")
    # rojo a proposito: este caso deberia dar REFUTADA; si el chequeo lo diera por bueno, la prueba estaria rota
    r = caso(real=lambda c, t: 0.99, nulo=lambda f, c, k: 0.985)
    rojo = r["veredicto"] == "SOSTENIDA"
    print("PRUEBA ROJO_A_PROPOSITO (se espera FALLA) -> %s" % ("OK" if rojo else "FALLA"), flush=True)
    chequeo("ROJO_A_PROPOSITO detectado", not rojo)
    n_ok = sum(RES)
    print("PRUEBA_TAULIBRE %d/%d -> %s" % (n_ok, len(RES), "OK" if n_ok == len(RES) else "FALLA"), flush=True)
    return 0 if n_ok == len(RES) else 1


if __name__ == "__main__":
    sys.exit(main())
