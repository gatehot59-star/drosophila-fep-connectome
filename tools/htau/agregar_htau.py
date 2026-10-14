#!/usr/bin/env python3
"""Agregador de H_TAU (respuesta 2026-10-14-002). Sellado antes de correr.

Junta los 6 json de tools/htau/htau_mosca.py (uno por celda) y decide H_TAU con reglas fijadas antes de ver datos.
  PRIMARIA     D[p, c] = acierto de la semilla elegida menos el de la regla propia, por semilla de prueba (12 a 21) y
               celda (6). Media; bootstrap sobre las semillas de prueba (las celdas quedan fijas, porque la eleccion
               es por celda), B = 20.000, semilla 2028, percentiles 0,05 y 0,95; margen M = 0,01. Veredicto y paso a
               hipotesis iguales a los de tools/factorial4/agregar_factorial4.py: SUPERA -> SOSTENIDA; EQUIVALENTE,
               NO_SUPERIOR o PIERDE -> REFUTADA; NO_INFERIOR o INDETERMINADO -> SIN_DECIDIR. Por celda, el mismo
               bootstrap con alfa 0,05/6 (descriptivo).
  DIAGNOSTICO  no decide: elegida menos peor (semilla 2029); en cuantas celdas se elige la misma semilla; validacion
               y entrenamiento de cada candidata.
Chequeos que invalidan: 6 json validos, uno por celda, sin humo; candidatas 10 a 19, pruebas 12 a 21 y 5 pliegues en
todos; md5 del instrumento sellado (MD5_HTAU), de factorial2_mosca.py, del modulo 015 y de los insumos iguales en
todos; REPRO_R2 medido y verdadero en la celda 0,3|0,15; las mismas 6 descendentes; 10 corridas por celda.
Uso: python3 tools/htau/agregar_htau.py <carpeta con los json> [--humo]
Salida: EXIT_AGREGADO=0 si el veredicto global es VALIDO; 1 si no.
"""
import glob
import json
import os
import sys

import numpy as np

CELDAS = ["0.0|0.15", "0.0|0.45", "0.3|0.15", "0.3|0.45", "0.6|0.15", "0.6|0.45"]
CANDIDATAS = list(range(10, 20))
PRUEBAS = list(range(12, 22))
PLIEGUES = 5
M = 0.01
B = 20000
MD5_HTAU = "2006cfef6eaffc023086fd35fbe20f64"
PIN = {"factorial2": "798a824cd47808155fa12adb9e652dac", "modulo015": "40d64e074d9163753439307c5be4ac5e",
       "conn": "3d802fd542b5d18570ba1ba0bb0abed9", "annot": "719904abad876c68ace1b5690c9b9b63"}


def pr(s):
    print(s, flush=True)


def veredicto(lo, hi):
    if lo > M:
        return "SUPERA"
    if hi < -M:
        return "PIERDE"
    if lo > -M and hi < M:
        return "EQUIVALENTE"
    if lo > -M:
        return "NO_INFERIOR"
    if hi < M:
        return "NO_SUPERIOR"
    return "INDETERMINADO"


def hipotesis(ver):
    if ver == "SUPERA":
        return "SOSTENIDA"
    if ver in ("EQUIVALENTE", "NO_SUPERIOR", "PIERDE"):
        return "REFUTADA"
    if ver == "NO_EVALUABLE":
        return "NO_EVALUABLE"
    return "SIN_DECIDIR"


def bootstrap(D, alfa, rng):
    """D tiene las semillas de prueba en la primera dimension; se remuestrean solo ellas."""
    npb = D.shape[0]
    bs = np.empty(B)
    for b in range(B):
        bs[b] = D[rng.integers(0, npb, npb)].mean()
    return float(D.mean()), float(np.quantile(bs, alfa)), float(np.quantile(bs, 1 - alfa))


def main():
    d = sys.argv[1]
    humo = "--humo" in sys.argv
    rutas = [r for r in sorted(glob.glob(os.path.join(d, "**", "htau_c*.json"), recursive=True))
             if not r.endswith("_repro.json")]
    js = []
    for r in rutas:
        with open(r) as f:
            js.append(json.load(f))
    por = {}
    for j in js:
        por.setdefault(j.get("celda"), []).append(j)
    pr("JSON htau=%d celdas=%s" % (len(js), sorted(k for k in por if k)))
    ok_celdas = sorted(k for k in por if k) == sorted(CELDAS) and all(len(v) == 1 for v in por.values())
    ok_val = bool(js) and all(j.get("valido") is True for j in js)
    sin_humo = bool(js) and all(not j.get("humo") for j in js)
    pr("CHEQUEO CELDAS una_por_celda -> %s" % ok_celdas)
    pr("CHEQUEO VALIDOS -> %s | SIN_HUMO -> %s" % (ok_val, sin_humo))
    ok_plan = bool(js) and all(j.get("candidatas") == CANDIDATAS and j.get("pruebas") == PRUEBAS and
                               j.get("pliegues") == PLIEGUES for j in js)
    pr("CHEQUEO PLAN candidatas=10..19 pruebas=12..21 pliegues=5 -> %s" % ok_plan)
    ok_md5 = bool(js) and all(j.get("md5", {}).get("script") == MD5_HTAU and
                              all(j.get("md5", {}).get(k) == v for k, v in PIN.items()) for j in js)
    pr("CHEQUEO MD5 instrumento=%s y pines -> %s" % (MD5_HTAU[:8], ok_md5))
    rep = [(j.get("celda"), j.get("repro")) for j in js if j.get("repro")]
    ok_repro = len(rep) == 1 and rep[0][0] == "0.3|0.15" and rep[0][1].get("igual") is True
    pr("CHEQUEO REPRO_R2 %s -> %s" % ([(c, r.get("W"), r.get("regla_propia"), r.get("regla40"), r.get("igual"))
                                      for c, r in rep], ok_repro))
    ok_dn = len({tuple(j.get("dns_root", [])) for j in js}) == 1
    pr("CHEQUEO DN_IGUAL -> %s" % ok_dn)
    ok_corr = bool(js) and all(sorted(x["prueba"] for x in j.get("corridas", [])) == PRUEBAS for j in js)
    pr("CHEQUEO CORRIDAS 10_por_celda -> %s" % ok_corr)
    valido = ok_celdas and ok_val and ok_plan and ok_dn and ok_corr and (humo or (sin_humo and ok_md5 and ok_repro))
    if humo:
        pr("# HUMO: no se exigen SIN_HUMO, MD5 ni REPRO; numeros sin valor")
    for c in CELDAS:
        if c in por:
            j = por[c][0]
            v = j.get("validacion", {})
            pr("ELECCION celda=%s elegida=%s peor=%s validacion=[%s]" % (
                c, j.get("elegida"), j.get("peor"),
                " ".join("%s:%.4f" % (k, v[k]) for k in sorted(v, key=int))))
    ver = "NO_EVALUABLE"
    if ok_celdas and ok_corr:
        def tabla(campo):
            return np.array([[next(x for x in por[c][0]["corridas"] if x["prueba"] == p)[campo] for c in CELDAS]
                             for p in PRUEBAS], dtype=np.float64)

        WE, WP, RP = tabla("W_elegida"), tabla("W_peor"), tabla("regla_propia")
        D = WE - RP
        rng = np.random.default_rng(2028)
        est, lo, hi = bootstrap(D.mean(1), 0.05, rng)
        ver = veredicto(lo, hi)
        pr("PRIMARIA H_TAU W_elegida=%.4f regla_propia=%.4f dif=%+.4f IC90=[%+.4f, %+.4f] corridas=%d -> %s" % (
            WE.mean(), RP.mean(), est, lo, hi, D.size, ver))
        for k, c in enumerate(CELDAS):
            e2, l2, h2 = bootstrap(D[:, k], 0.05 / 6, rng)
            pr("  CELDA %s elegida=%s dif=%+.4f IC=[%+.4f, %+.4f] -> %s" % (c, por[c][0].get("elegida"), e2, l2, h2,
                                                                          veredicto(l2, h2)))
        pr("PRIMARIA corridas elegida>regla=%d iguales=%d elegida<regla=%d" % (
            int((D > 0).sum()), int((D == 0).sum()), int((D < 0).sum())))
        Edg = WE - WP
        e3, l3, h3 = bootstrap(Edg.mean(1), 0.05, np.random.default_rng(2029))
        pr("DIAGNOSTICO elegida_menos_peor W_peor=%.4f dif=%+.4f IC90=[%+.4f, %+.4f] (no decide)" % (WP.mean(), e3, l3, h3))
        el = [por[c][0].get("elegida") for c in CELDAS]
        pr("DIAGNOSTICO semilla_elegida_por_celda=%s distintas=%d (no decide)" % (el, len(set(el))))
    hip = hipotesis(ver) if valido else "NO_EVALUABLE"
    pr("HIPOTESIS H_TAU -> %s" % hip)
    pr("VEREDICTO_GLOBAL -> %s | primaria=%s" % ("VALIDO" if valido else "INVALIDO", ver))
    pr("EXIT_AGREGADO=%d" % (0 if valido else 1))
    return 0 if valido else 1


if __name__ == "__main__":
    sys.exit(main())
