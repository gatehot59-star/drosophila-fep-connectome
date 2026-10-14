#!/usr/bin/env python3
"""Pruebas de Topo v0.2 con entradas sinteticas (respuesta 2026-10-14-026). Sin datos reales.

1 PARSEA: escape_dif.topo tiene 2 internas, 2 comparadores y compiten 6, en orden.
2 PARIDAD_ESCAPE: escape_dif en v0.2 da exactamente las mismas predicciones y umbrales que escape.topo en v0.
3 PARIDAD_V0: un programa sin interna ni compara da en v0.2 exactamente lo mismo que en v0.
4 PUEDE_DAR_ROJO: con el comparador invertido, las predicciones cambian.
5 SIN_COMPARADOR_DIFIERE: escape_fiel.topo (sin resta ni comparador) no da lo mismo que escape_dif.
6 a 9 ERRORES: comparador sobre una linea inexistente, sobre una linea no interna, con A igual a B, y una interna sin
  comparador: los cuatro tienen que fallar con ErrorTopo.
Sale 0 si pasan todas.
"""
import os
import sys

import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
HERR = os.path.dirname(AQUI)
sys.path.insert(0, AQUI)
import topo_v02 as tv  # noqa: E402
topo = tv.topo


def leer(r):
    return open(r, encoding="utf-8").read()


def datos(semilla=5, n=800, T=25):
    rng = np.random.default_rng(semilla)
    tipos, lados = [], []
    for t in ("LC4", "LPLC2", "LPLC4", "LPLC1"):
        for s in ("L", "R"):
            tipos += [t, t]
            lados += [s, s]
    k = len(tipos)
    X = rng.standard_normal((n, T, k)).cumsum(1) * 0.2
    y = rng.integers(0, 5, n)
    y[rng.random(n) < 0.4] = 0
    e = rng.integers(0, 2, n)
    return X, y, e, tipos, lados


def correr(mod, p, semilla_tr=5, semilla_te=6):
    Xtr, ytr, etr, ti, la = datos(semilla_tr)
    Xte, _, ete, _, _ = datos(semilla_te)
    return mod.ejecutar_regla(p, Xtr, ytr, etr, Xte, ete, ti, la)


def falla(texto):
    try:
        tv.parsear(texto)
    except tv.ErrorTopo as e:
        return True, str(e)
    return False, "no fallo"


def main():
    res = []

    def chk(nombre, ok, extra=""):
        res.append(bool(ok))
        print("PRUEBA %s %s %s" % (nombre, "PASA" if ok else "FALLA", extra))

    tdif = leer(os.path.join(AQUI, "escape_dif.topo"))
    tesc = leer(os.path.join(HERR, "topo", "escape.topo"))
    tfiel = leer(os.path.join(HERR, "topo_fiel", "escape_fiel.topo"))
    pd_ = tv.parsear(tdif)
    nombres = [c["nombre"] for c in tv.compiten(pd_)]
    chk("PARSEA", len(pd_["internas"]) == 2 and len(pd_["compara"]) == 2 and nombres == [
        "DNp01@L", "DNp01@R", "DNp07@L", "DNp07@R", "GIRO_DER", "GIRO_IZQ"], nombres)

    yv, thv, _ = correr(topo, topo.parsear(tesc))
    yd, thd, _ = correr(tv, pd_)
    chk("PARIDAD_ESCAPE", np.array_equal(yv, yd) and np.array_equal(thv, thd),
        "iguales=%d de %d, umbrales iguales=%s" % (int((yv == yd).sum()), len(yv), np.array_equal(thv, thd)))

    y2, th2, _ = correr(tv, tv.parsear(tesc))
    chk("PARIDAD_V0", np.array_equal(yv, y2) and np.array_equal(thv, th2))

    tinv = tdif.replace("GIRO_DER = DNp06@L - DNp06@R", "GIRO_DER = DNp06@R - DNp06@L").replace(
        "GIRO_IZQ = DNp06@R - DNp06@L", "GIRO_IZQ = DNp06@L - DNp06@R")
    yi, _, _ = correr(tv, tv.parsear(tinv))
    chk("PUEDE_DAR_ROJO", tinv != tdif and not np.array_equal(yi, yd), "distintas=%d" % int((yi != yd).sum()))

    yf, _, _ = correr(topo, topo.parsear(tfiel))
    chk("SIN_COMPARADOR_DIFIERE", not np.array_equal(yf, yd), "distintas=%d" % int((yf != yd).sum()))

    casos = [
        ("ERROR_LINEA_INEXISTENTE", tdif.replace("GIRO_DER = DNp06@L - DNp06@R", "GIRO_DER = DNp09@L - DNp06@R")),
        ("ERROR_NO_INTERNA", tdif.replace("GIRO_DER = DNp06@L - DNp06@R", "GIRO_DER = DNp07@L - DNp06@R")),
        ("ERROR_A_IGUAL_B", tdif.replace("GIRO_DER = DNp06@L - DNp06@R", "GIRO_DER = DNp06@L - DNp06@L")),
        ("ERROR_INTERNA_SIN_USO", tdif.replace("linea DNp07@L = media(LPLC4@L) en vuelo -> aterrizar",
                                               "linea DNp07@L = media(LPLC4@L) en vuelo -> interna")),
    ]
    for nombre, txt in casos:
        ok, msg = falla(txt)
        chk(nombre, ok and txt != tdif, msg)
    print("RESUMEN %d/%d" % (sum(res), len(res)))
    return 0 if all(res) else 1


if __name__ == "__main__":
    sys.exit(main())
