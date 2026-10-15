#!/usr/bin/env python3
"""Prueba de H_LECTOR (respuesta 2026-10-14-037): el lector es el RIDGE de H_RIVAL, el agregador aplica el sello, y
hay un chequeo hecho para dar rojo a proposito. Sin red: datos sinteticos. Salida 0 si pasan todas."""
import json
import os
import sys
import tempfile

import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import lector_mosca as lm  # noqa: E402
import agregar_lector as ag  # noqa: E402

rv, tm = lm.rv, lm.tm
RES = []


def chequeo(nombre, ok):
    RES.append(bool(ok))
    print("PRUEBA %s -> %s" % (nombre, "OK" if ok else "FALLA"), flush=True)


def sinteticos(n, d, sem):
    rng = np.random.default_rng(sem)
    v = rng.random(n) < 0.5
    y = np.where(v, rng.choice(tm.CLASES[True], n), rng.choice(tm.CLASES[False], n))
    F = rng.standard_normal((n, d))
    F[:, 0] += y
    F[:, 1] += 0.5 * y * v
    return F, y, v


# 1. el lector es el RIDGE de H_RIVAL
F, y, v = sinteticos(300, 40, 1)
Ft, yt, vt = sinteticos(200, 40, 2)
info, mod = lm.lector(F, y, v)
cv, _ = rv.cv_ridge(F, y, v, rv.pliegues(len(y)), rv.LAMBDAS_R)
j = max(range(len(rv.LAMBDAS_R)), key=lambda k: (cv[k], rv.LAMBDAS_R[k]))
ref = rv.ridge_predecir(rv.ridge_ajustar(F, y, v, np.arange(len(y)), (rv.LAMBDAS_R[j],)), Ft, vt, np.arange(len(yt)))[0]
chequeo("LECTOR_IGUAL_RIVAL", info["elegida"] == rv.LAMBDAS_R[j] and np.array_equal(lm.leer(mod, Ft, vt), ref)
        and np.allclose(info["validacion"], cv))
chequeo("LECTOR_NO_TOCA_F", np.array_equal(F, sinteticos(300, 40, 1)[0]))

# 2. rojo a proposito: con las lambdas al doble la validacion cambia, y la prueba lo nota
cv2, _ = rv.cv_ridge(F, y, v, rv.pliegues(len(y)), tuple(2 * x for x in rv.LAMBDAS_R))
chequeo("ROJO_A_PROPOSITO (lambdas al doble se notan)", not np.allclose(cv2, info["validacion"]))

# 3. agregador
PR = ag.PRIMARIA


def armar(carpeta, wl, ridge, w, nulo, real_igual=True, humo_c=None, faltar=None):
    pred = "01" * 10
    for c in range(ag.NCEL):
        filas = [dict(prueba=p, WL=wl, pred_WL=pred, RIDGE=ridge, W_elegida=w) for p in PR]
        j = dict(experimento="H_LECTOR", modo="celda", ci=c, celda="x", humo=(c == humo_c), local=False, valido=True,
                 controles=dict(CONTROL_LECTOR_CRUDO=True), filas=filas)
        json.dump(j, open(os.path.join(carpeta, "lector_c%d.json" % c), "w"))
    for f in ag.FAMILIAS:
        for c in ag.CELDAS_NULOS:
            for k0 in ag.K0S:
                nul = [dict(k=k, WL=nulo) for k in range(k0, k0 + 10)]
                real = dict(WL=wl, pred_WL=pred if real_igual else "10" * 10) if k0 == 0 else None
                j = dict(modo="nulos", tipo=f, ci=c, prueba=12, humo=False, local=False, valido=True, nulos=nul, real=real)
                json.dump(j, open(os.path.join(carpeta, "nulos_%s_c%d_k%03d.json" % (f, c, k0)), "w"))
    if faltar:
        os.remove(os.path.join(carpeta, faltar))


def caso(**kw):
    with tempfile.TemporaryDirectory() as t:
        armar(t, **kw)
        return ag.agregar(t)


r = caso(wl=0.95, ridge=0.95, w=0.93, nulo=0.80)
chequeo("CASO_CERCA_PAGA_CABLEADO", r["valido"] and r["H_LECTOR_CERCA"] == "SOSTENIDA" and
        r["H_LECTOR_PAGA"] == "SOSTENIDA" and r["H_LECTOR_CABLEADO"] == "SOSTENIDA")
r = caso(wl=0.94, ridge=0.99, w=0.94, nulo=0.94)
chequeo("CASO_LEJOS", r["valido"] and r["H_LECTOR_CERCA"] == "REFUTADA" and r["H_LECTOR_PAGA"] == "REFUTADA" and
        r["H_LECTOR_CABLEADO"] == "REFUTADA")
r = caso(wl=0.985, ridge=0.99, w=0.94, nulo=0.80)
chequeo("CASO_MEDIO_PUNTO_ES_CERCA", r["H_LECTOR_CERCA"] == "SOSTENIDA" and r["primaria"]["D1"]["lo"] < 0)
r = caso(wl=0.95, ridge=0.95, w=0.93, nulo=0.80, real_igual=False)
chequeo("CASO_REAL_DISTINTO_INVALIDO", r["valido"] is False and r["H_LECTOR_CERCA"] == "INVALIDO")
r = caso(wl=0.95, ridge=0.95, w=0.93, nulo=0.80, humo_c=3)
chequeo("CASO_HUMO_INVALIDO", r["valido"] is False and r["H_LECTOR_PAGA"] == "INVALIDO")
r = caso(wl=0.95, ridge=0.95, w=0.93, nulo=0.80, faltar="nulos_T_c5_k030.json")
chequeo("CASO_FALTA_INVALIDO", r["valido"] is False and r["H_LECTOR_CABLEADO"] == "INVALIDO")

# 4. la cuenta de los nulos
x = ag.cableado(0.95, [0.80] * 39 + [0.95])
chequeo("NULO_UNO_IGUAL p=2/41 supera", abs(x["p"] - 2 / 41) < 1e-12 and x["supera"])
x = ag.cableado(0.95, [0.80] * 38 + [0.96, 0.95])
chequeo("NULO_DOS_IGUALES p=3/41 sin decidir", abs(x["p"] - 3 / 41) < 1e-12 and not x["supera"] and not x["refuta"])
x = ag.cableado(0.95, [0.945] * 40)
chequeo("NULO_MEDIO_PUNTO refuta por margen", x["refuta"] and not x["supera"])
chequeo("PERCENTILES 2.5 y 97.5 (90 por ciento con Bonferroni por 2)", ag.Q_LO == 2.5 and ag.Q_HI == 97.5)

n_ok = sum(RES)
print("PRUEBA_LECTOR %d/%d -> %s" % (n_ok, len(RES), "OK" if n_ok == len(RES) else "FALLA"), flush=True)
sys.exit(0 if n_ok == len(RES) else 1)
