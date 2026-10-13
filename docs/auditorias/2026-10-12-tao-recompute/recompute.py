#!/usr/bin/env python3
"""Recomputo de la auditoria TAO del laboratorio (2026-10-12/13).

Todo lo que corre aca sale de conteos publicados en el manuscrito o en los
logs commiteados; nada necesita el parquet de FlyWire. Imprime una linea
PASS/FAIL por chequeo y sale con codigo 1 si alguno falla.
"""
from __future__ import annotations

import math
import sys

import numpy as np
from scipy.stats import binom

FAILS: list[str] = []


def check(name: str, ok: bool, detail: str) -> None:
    print(("PASS " if ok else "FAIL ") + name + " :: " + detail)
    if not ok:
        FAILS.append(name)


def neuropil_permutation(src, dst, out_code, in_code, rng):
    """Cuerpo transcrito de src/twohop_nulls.py (blob 9b0bd4a), sin cambios
    de logica: permuta destinos dentro de cada bloque (np_origen, np_destino)."""
    span = int(in_code.max()) + 1
    key = out_code[src].astype(np.int64) * span + in_code[dst]
    order = np.argsort(key, kind="stable")
    boundaries = np.flatnonzero(np.diff(key[order])) + 1
    permuted = dst.copy()
    for block in np.split(order, boundaries):
        if block.size > 1:
            permuted[block] = dst[rng.permutation(block)]
    return permuted


def f01() -> None:
    n_graphs, n_nodes, n_edges = 100, 50, 700
    kept_in = changed = uniform_broke = 0
    for s in range(n_graphs):
        rng = np.random.default_rng(s)
        src = rng.integers(0, n_nodes, n_edges)
        dst = rng.integers(0, n_nodes, n_edges)
        out_code = rng.integers(0, 6, n_nodes)
        in_code = rng.integers(0, 6, n_nodes)
        perm = neuropil_permutation(src, dst, out_code, in_code,
                                    np.random.default_rng(1000 + s))
        indeg = np.bincount(dst, minlength=n_nodes)
        kept_in += int((np.bincount(perm, minlength=n_nodes) == indeg).all())
        changed += int((perm != dst).any())
        uni = np.random.default_rng(5000 + s).integers(0, n_nodes, n_edges)
        uniform_broke += int((np.bincount(uni, minlength=n_nodes) != indeg).any())
    check("F01 nulo neuropilo preserva in-degree global", kept_in == n_graphs,
          f"{kept_in}/{n_graphs} grafos preservan in-degree; {changed}/{n_graphs} cambian destinos")
    check("F01 control negativo uniforme rompe in-degree", uniform_broke == n_graphs,
          f"{uniform_broke}/{n_graphs}")


def f02() -> None:
    r0 = (1413 / 922.850) / (901 / 2450.650)
    r5 = 4.871795 / 0.120950
    check("F02 cociente extremos neuropilo sin umbral ~4.2 (no 2.4)",
          abs(r0 - 4.1645) < 1e-3, f"{r0:.10f}")
    check("F02 cociente extremos neuropilo umbral5 ~40", abs(r5 - 40.279) < 1e-2, f"{r5:.6f}")


def table5() -> None:
    density = 15_091_983 / (138_639 * 138_638)
    p_exc = 0.600272
    q = density * p_exc
    for name, n, obs, published in (("thermosensory", 29, 14, 0.094),
                                    ("hygrosensory", 74, 13, 1.3e-10)):
        trials = n * 1485
        exp = trials * q
        p = float(binom.cdf(obs, trials, q))
        ok = math.isclose(p, published, rel_tol=0.05)
        check(f"Tabla5 p cola inferior {name}", ok,
              f"exp={exp:.2f} p={p:.10g} publicado={published}")


def table7() -> None:
    rows = {
        "intra-motor": (509, 210, 41.3, 80, 28, 35.0),
        "intra-visual centrifugal": (7490, 2764, 36.9, 1324, 310, 23.4),
        "intra-optic": (6201390, 1983172, 32.0, 1069721, 183060, 17.1),
        "intra-sensory": (34107, 10460, 30.7, 1287, 482, 37.5),
        "sensory->central": (159316, 38549, 24.2, 33497, 4609, 13.8),
        "sensory->descending": (24326, 2104, 8.6, 4786, 136, 2.8),
        "sensory->motor": (1178, 42, 3.6, 373, 5, 1.3),
    }
    ok_all = True
    for k, (c0, r0, p0, c5, r5, p5) in rows.items():
        a, b = round(100 * r0 / c0, 1), round(100 * r5 / c5, 1)
        ok_all &= (a == p0 and b == p5)
    whole0 = 100 * 4_014_518 / 15_091_983
    whole5 = 100 * 377_448 / 2_700_513
    check("Tabla7 siete filas x dos umbrales", ok_all, "porcentajes recomputados coinciden")
    check("Tabla7 conectoma entero", round(whole0, 2) == 26.60 and round(whole5, 2) == 13.98,
          f"{whole0:.6f}% / {whole5:.8f}%")


def tau() -> None:
    vals = {0.05: 19.5, 0.119: 7.9, 0.2: 4.5, 0.3: 2.8}
    out = {t: -1 / math.log(1 - t) for t in vals}
    ok = all(round(out[t], 1) == v for t, v in vals.items())
    check("Tabla10 constante efectiva", ok, ", ".join(f"{t}:{out[t]:.4f}" for t in out))


def mcnemar() -> None:
    for b, c in ((1, 37), (252, 12), (169, 15)):
        n = b + c
        p = min(1.0, 2 * float(binom.cdf(min(b, c), n, 0.5)))
        print(f"INFO McNemar exacto {b}/{c}: p={p:.6g}")


def cp_floor() -> None:
    print(f"INFO piso p empirico con 5 nulos CP: 1/6 = {1/6:.7f}")
    print(f"INFO piso con 40 nulos: 1/41 = {1/41:.7f}")


def holm_floor() -> None:
    floor, first = 2 / 5001, 0.05 / 242
    check("Salidas: piso bilateral 2/5001 supera alfa Holm 0.05/242", floor > first,
          f"{floor:.7f} > {first:.7f}: la primera prueba Holm no puede pasar por resolucion")


def lif_soft() -> None:
    d = 0.002 - 0.253
    check("F04 LIF-soft no amplifica", d < 0, f"delta RDI t60->t180 = {d:.3f}")


if __name__ == "__main__":
    f01(); f02(); table5(); table7(); tau(); holm_floor(); lif_soft(); mcnemar(); cp_floor()
    print("RESULTADO", "FAIL " + ",".join(FAILS) if FAILS else "TODO PASS")
    sys.exit(1 if FAILS else 0)
