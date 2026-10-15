#!/usr/bin/env python3
"""Prueba de reuso_mosca con grafos de juguete (respuesta 2026-10-14-029). Sin datos reales.

1 EXACTO: en un grafo a mano, pares cableados, T1 y T2 dan lo calculado.
2 OTRO_LADO: un sensor que le da 30 sinapsis a la descendente del otro lado no forma par.
3 UMBRAL_X: una inhibitoria con 4 sinapsis no hace la plantilla.
4 GUARDA_NULO: el nulo conserva aristas de llegada por neurona y el lado del destino, y cambia mas de la mitad.
5 PUEDE_DAR_ROJO: con 10 piezas compartidas plantadas sobre ruido, T2 supera a los 30 nulos; sin ninguna pieza
  plantada (ni X0), no.
6 VEREDICTOS y 7 HOLM: tablas de decision.
Sale 0 si pasan todas.
"""
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import reuso_mosca as rm  # noqa: E402


def grafo(plantar=0, otro_lado=False, x_debil=False, ruido=0, semilla=0, con_x0=True):
    tipo, lado, sc, inh = [], [], [], []

    def neu(t, s, c, i=False):
        tipo.append(t)
        lado.append(s)
        sc.append(c)
        inh.append(i)
        return len(tipo) - 1
    ids = {}
    for t in ("A", "B"):
        for s in rm.LADOS:
            ids[(t, s)] = neu(t, s, "visual_projection")
    for t in ("P", "Q", "R"):
        for s in rm.LADOS:
            ids[(t, s)] = neu(t, s, "descending")
    e = []
    e.append((ids[("A", "left")], ids[("P", "left")], 30))
    e.append((ids[("A", "left")], ids[("Q", "left")], 30))
    e.append((ids[("B", "left")], ids[("R", "left")], 30))
    x0 = neu("X0", "left", "central", True)
    if con_x0:
        e += [(ids[("A", "left")], x0, 10), (x0, ids[("P", "left")], 10), (x0, ids[("Q", "left")], 10)]
    if otro_lado:
        e.append((ids[("A", "left")], ids[("P", "right")], 30))
    if x_debil:
        xd = neu("XD", "left", "central", True)
        e += [(ids[("B", "left")], xd, 4), (xd, ids[("R", "left")], 10)]
    for k in range(plantar):
        xk = neu("XP%d" % k, "left", "central", True)
        e += [(ids[("B", "left")], xk, 8), (xk, ids[("R", "left")], 8), (xk, ids[("P", "left")], 8)]
    if plantar:
        e.append((ids[("B", "left")], ids[("P", "left")], 30))
    if ruido:
        rng = np.random.default_rng(semilla)
        for k in range(ruido):
            neu("F%d" % k, rm.LADOS[k % 2], "central", bool(k % 3 == 0))
        todos = np.arange(len(tipo))
        for _ in range(ruido * 12):
            a, b = rng.choice(todos, 2, replace=False)
            e.append((int(a), int(b), int(rng.integers(1, 9))))
    e = np.array(e)
    return rm.armar(e[:, 0].astype(np.int32), e[:, 1].astype(np.int32), e[:, 2], np.array(inh),
                    np.array(tipo, dtype=object), np.array(lado, dtype=object), np.array(sc, dtype=object))


def p_t2(d, n_nulo=30, semilla=1):
    obs = rm.estadisticas(d, d["post"])["t2"]
    rng = np.random.default_rng(semilla)
    nul = [rm.estadisticas(d, rm.nulo(d, rng))["t2"] for _ in range(n_nulo)]
    return obs, max(nul), (1 + sum(x >= obs for x in nul)) / (n_nulo + 1.0)


def main():
    res = []

    def chk(nombre, ok, extra=""):
        res.append(bool(ok))
        print("PRUEBA %s %s %s" % (nombre, "PASA" if ok else "FALLA", extra))

    d = grafo()
    e = rm.estadisticas(d, d["post"])
    chk("EXACTO", e["n_cab"] == 3 and abs(e["t1"] - 2 / 3.0) < 1e-12 and e["t2"] == 1, e)
    d = grafo(otro_lado=True)
    e2 = rm.estadisticas(d, d["post"])
    chk("OTRO_LADO", e2["n_cab"] == 3, e2)
    d = grafo(x_debil=True)
    e3 = rm.estadisticas(d, d["post"])
    chk("UMBRAL_X", e3["n_pares_ffi"] == 2 and abs(e3["t1"] - 2 / 3.0) < 1e-12, e3)
    d = grafo(ruido=300, semilla=3)
    nuevo = rm.nulo(d, np.random.default_rng(5))
    chk("GUARDA_NULO", rm.guarda_nulo(d, nuevo))
    o1, m1, p1 = p_t2(grafo(plantar=10, ruido=300, semilla=3))
    o0, m0, p0 = p_t2(grafo(plantar=0, ruido=300, semilla=3, con_x0=False))
    chk("PUEDE_DAR_ROJO", o1 > m1 and p1 < 0.05 and p0 >= 0.05,
        "plantado obs=%d max_nulo=%d p=%.3f | sin plantar obs=%d max_nulo=%d p=%.3f" % (o1, m1, p1, o0, m0, p0))
    vc = rm.veredicto_conectoma
    vf = rm.veredicto_final
    ok6 = (vc([0.001, 0.002], [0.004, 0.006]) == "SOSTENIDA" and vc([0.2, 0.5], [0.4, 0.5]) == "REFUTADA" and
           vc([0.01, 0.3], [0.04, 0.3]) == "PARCIAL" and vf("SOSTENIDA", "SOSTENIDA", True) == "SOSTENIDA" and
           vf("REFUTADA", "SOSTENIDA", True) == "REFUTADA" and vf("SOSTENIDA", "REFUTADA", True) == "NO_SE_REPLICA" and
           vf("SOSTENIDA", "PARCIAL", True) == "SIN_DECIDIR" and vf("SOSTENIDA", "SOSTENIDA", False) == "INVALIDO")
    chk("VEREDICTOS", ok6)
    h = rm.holm([0.01, 0.04, 0.03, 0.005])
    chk("HOLM", np.allclose(h, [0.03, 0.06, 0.06, 0.02]), h)
    print("RESUMEN %d/%d" % (sum(res), len(res)))
    return 0 if all(res) else 1


if __name__ == "__main__":
    sys.exit(main())
