#!/usr/bin/env python3
"""H_MECANISMO_DNp04, instrumento de intervenciones. Sello: tools/mecanismo/dnp04/SELLO-DNP04-2026-11-02.md (40969fb).

Reusa sin cambios las funciones de tools/mecanismo/intervenir.py, con su sha256 fijado en SHA_INTERVENIR: ensayo() y
correr_cond() para correr cada ensayo en un proceso nuevo, tocadas() para contar filas, operaciones() para C0 y C1, y
md5(), sha256() y blob() para los pines. Agrega solo las condiciones Q1 a Q6 sobre cuatro neuronas del lado derecho
fijadas por root_id en el sello. Mismo modelo, mismos conjuntos y mismas semillas que la corrida 2 (run 41459331354):
C0 y C1 tienen que salir identicos a los de esa corrida (guarda G1 del sello).
Condiciones: C0 intacto; C1 silenciar X; Q1 cortar DNp04->PVLP010; Q2 silenciar PVLP010; Q3 silenciar DNp04;
Q4 PVLP010 recibe solo de DNp04; Q5 silenciar LHAD1g1; Q6 silenciar AVLP080. Mide causalidad DEL MODELO.
Uso: python3 intervenir_dnp04.py --shiu DIR --conn C --comp K --conjuntos J --celda NOMBRE --out D [--n-proc 3]
"""
import argparse
import gc
import json
import os
import sys
import time

import numpy as np
import pandas as pd

AQUI = os.path.dirname(os.path.abspath(__file__))
MECANISMO = os.path.dirname(AQUI)
if MECANISMO not in sys.path:
    sys.path.insert(0, MECANISMO)
import intervenir as base  # noqa: E402

VERSION = "2026-11-02-006"
SHA_INTERVENIR = "e656d73eac31e4d955b0b78ec2345a65f67097de1c787f4617eb72048b699a2e"
NOMBRES = {"DNp04": 720575940629757036, "PVLP010": 720575940618932763,
           "LHAD1g1": 720575940631842360, "AVLP080": 720575940608545219}
ORDEN = ("DNp04", "PVLP010", "LHAD1g1", "AVLP080")
ESTIM = ("LC4", "LPLC2", "LPLC1", "LPLC4")
PARTE_A = ("C0", "C1", "Q1", "Q2")
PARTE_B = ("C0", "Q3", "Q4", "Q5", "Q6")
CELDAS = {}
for _e in ESTIM:
    CELDAS["q_%s_right_a" % _e] = {"estimulo": _e + "_right", "hz": 50.0, "conds": list(PARTE_A), "n_run": 20}
    CELDAS["q_%s_right_b" % _e] = {"estimulo": _e + "_right", "hz": 50.0, "conds": list(PARTE_B), "n_run": 20}


def operaciones(cond, S, X, D, N):
    """C0 y C1 salen de intervenir.operaciones sin cambios; Q1 a Q6 son las del sello, sobre indices de Shiu."""
    if cond in ("C0", "C1"):
        return base.operaciones(cond, S, X, D, [], [])
    dn, pv, lh, av = N["DNp04"], N["PVLP010"], N["LHAD1g1"], N["AVLP080"]
    return {
        "Q1": [("cero", [dn], False, [pv], False)],
        "Q2": [("cero", [pv], False, None, False)],
        "Q3": [("cero", [dn], False, None, False)],
        "Q4": [("cero", [dn], True, [pv], False)],
        "Q5": [("cero", [lh], False, None, False)],
        "Q6": [("cero", [av], False, None, False)],
    }[cond]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--shiu", required=True)
    ap.add_argument("--conn", required=True)
    ap.add_argument("--comp", required=True)
    ap.add_argument("--conjuntos", required=True)
    ap.add_argument("--celda", required=True)
    ap.add_argument("--celda-json", default="", help="solo prueba: definicion de celda propia")
    ap.add_argument("--out", required=True)
    ap.add_argument("--n-proc", type=int, default=3)
    ap.add_argument("--n-run", type=int, default=0, help="solo prueba: pisa n_run")
    ap.add_argument("--t-run-ms", type=float, default=1000.0)
    ap.add_argument("--target", default="", help="codegen de brian2; vacio = el de Brian2 por defecto")
    a = ap.parse_args()
    t_ini = time.time()
    os.makedirs(a.out, exist_ok=True)
    sys.path.insert(0, a.shiu)
    pines = {"model": base.blob(os.path.join(a.shiu, "model.py")) == base.BLOB_MODEL,
             "conn": base.md5(a.conn) == base.MD5_CONN, "comp": base.md5(a.comp) == base.MD5_COMP,
             "conjuntos": base.sha256(a.conjuntos) == base.SHA_CONJ,
             "intervenir": base.sha256(os.path.join(MECANISMO, "intervenir.py")) == SHA_INTERVENIR}
    base.pr("== intervenir_dnp04.py :: H_MECANISMO_DNp04 (%s) celda=%s ==" % (VERSION, a.celda))
    base.pr("PINES %s" % json.dumps(pines, sort_keys=True))
    if not all(pines.values()):
        base.pr("ABORTA: pin")
        raise SystemExit(3)
    import brian2
    import model as shiu
    from brian2 import Hz, ms
    cel = json.loads(a.celda_json) if a.celda_json else CELDAS[a.celda]
    n_run = a.n_run or cel["n_run"]
    conj = json.load(open(a.conjuntos))
    ids = pd.read_csv(a.comp, index_col=0).index.to_numpy(dtype=np.int64)
    n = len(ids)
    f2i = {int(f): k for k, f in enumerate(ids)}
    cols = ["Presynaptic_ID", "Postsynaptic_ID", "Presynaptic_Index", "Postsynaptic_Index", "Connectivity",
            "Excitatory x Connectivity"]
    df = pd.read_parquet(a.conn, columns=cols)
    i = df["Presynaptic_Index"].to_numpy(dtype=np.int64)
    j = df["Postsynaptic_Index"].to_numpy(dtype=np.int64)
    indices_ok = bool(np.array_equal(ids[i], df["Presynaptic_ID"].to_numpy(dtype=np.int64)) and
                      np.array_equal(ids[j], df["Postsynaptic_ID"].to_numpy(dtype=np.int64)))
    w = df["Excitatory x Connectivity"].to_numpy(dtype=np.float64)
    del df
    gc.collect()
    base.pr("GRAFO n=%d filas=%d indices_ok=%s" % (n, len(i), indices_ok))
    if not indices_ok:
        base.pr("ABORTA: los indices del parquet no son la posicion en Completeness")
        raise SystemExit(3)
    e = conj["estimulos"][cel["estimulo"]]
    faltan = [f for f in e["S"] + e["X"] + e["D"] + list(NOMBRES.values()) if f not in f2i]
    if faltan:
        base.pr("ABORTA: %d ids no estan en Completeness" % len(faltan))
        raise SystemExit(3)
    S = [f2i[f] for f in e["S"]]
    X = [f2i[f] for f in e["X"]]
    D = [f2i[f] for f in e["D"]]
    N = {k: f2i[NOMBRES[k]] for k in ORDEN}
    dset = set(D)
    desc = [f2i[f] for f in conj["descendentes"]["root"] if f in f2i and f2i[f] not in dset]
    mirar = list(dict.fromkeys(S + X + D + [N[k] for k in ORDEN] + desc))
    pos = {m: k for k, m in enumerate(mirar)}
    res = {"version": VERSION, "celda": a.celda, "def": cel, "n_run": n_run, "t_run_ms": a.t_run_ms,
           "pines": pines, "brian2": brian2.__version__, "numpy": np.__version__, "pandas": pd.__version__,
           "target": a.target or str(brian2.prefs.codegen.target), "conds": {},
           "guardas": {"faltan_ids": faltan, "indices_ok": indices_ok},
           "D_tipo": e["D_tipo"], "X_tipo": e["X_tipo"],
           "nombres": {k: {"root": NOMBRES[k], "indice": N[k], "en_S": N[k] in S, "en_X": N[k] in X,
                           "en_D": N[k] in D} for k in ORDEN},
           "indices": {"S": S, "X": X, "D": D, "desc": desc, "mirar": mirar}}
    base.pr("CONJUNTOS S=%d X=%d D=%d desc=%d mirar=%d NOMBRES %s" % (
        len(S), len(X), len(D), len(desc), len(mirar), json.dumps(res["nombres"], sort_keys=True)))
    params = dict(shiu.default_params)
    params["r_poi"] = float(cel["hz"]) * Hz
    params["n_run"] = n_run
    params["t_run"] = a.t_run_ms * ms
    for cond in cel["conds"]:
        ops = operaciones(cond, S, X, D, N)
        toc = base.tocadas(i, j, w, n, ops)
        t1 = time.time()
        ens = base.correr_cond(a, params, S, ops, mirar, D, n_run, Hz, ms)
        sumD = [int(sum(r["cuentas"][pos[d]] for d in D)) for r in ens]
        sumX = [int(sum(r["cuentas"][pos[x]] for x in X)) for r in ens]
        nom = {k: [int(r["cuentas"][pos[N[k]]]) for r in ens] for k in ORDEN}
        res["conds"][cond] = {"tocadas": toc, "ensayos": ens, "D": sumD, "X": sumX, "nombres": nom,
                              "seg": time.time() - t1}
        base.pr("COND %s tocadas=%d peso_abs=%.1f | %.1f s" % (cond, toc["filas"], toc["peso_abs"], time.time() - t1))
        tmp = os.path.join(a.out, "celda_%s.json.tmp" % a.celda)
        res["segundos"] = time.time() - t_ini
        with open(tmp, "w") as f:
            json.dump(res, f)
        os.replace(tmp, os.path.join(a.out, "celda_%s.json" % a.celda))
    base.pr("FIN celda=%s %.1f s" % (a.celda, time.time() - t_ini))


if __name__ == "__main__":
    main()
