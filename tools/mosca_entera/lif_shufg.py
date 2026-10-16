#!/usr/bin/env python3
"""H_LIF_SHUFG, instrumento (respuesta 2026-10-14-055).

Sello: tools/mosca_entera/SELLO-LIF-SHUFG-054.md (307db84, md5 9e7e25f7f7e4ca8bbd031f6484eefe54).
El LIF de Shiu sin cambios (model.py en 91bdd1e7, blob 5ba7083c; default_params salvo r_poi = 100 Hz) sobre el real
(30 ensayos, para CTRL_REAL) o sobre los nulos SHUF_G de la 049 y la 051 (nulo() de liq_entera.py con
default_rng([20261015, 2, k])), 10 ensayos cada uno. Por grafo guarda lo que da resumir() de lif_shiu.py (E_MN9 es
ensayos_mn9, F_MN9 es tasa_mn9; activas, espigas, K y S_LIF) y el atajo en el cableado (n1, D1+ y D2+). En cada nulo,
NULO_MISMO: el radio crudo del parquet que se le pasa al modelo de Shiu, releido, contra el que registro la 049 para
ese k (tolerancia relativa 1e-6); si no coincide, el nulo no se simula y queda NO_MEDIDO.
Importa lif_shiu.py (md5 88c8459e) y liq_entera.py (md5 ae3c1a2d) sin tocarlos.
Uso:
  real:  python3 lif_shufg.py --shiu DIR --conn C --comp K --out D --modo real --n-run 30
  nulos: python3 lif_shufg.py --shiu DIR --conn C --comp K --out D --modo nulos --k0 0 --n 5 --n-run 10 --ref R ...
"""
import argparse
import json
import os
import sys
import time

import numpy as np
import pandas as pd
import scipy
import scipy.sparse as sp

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import liq_entera as le  # noqa: E402
import lif_shiu as ls  # noqa: E402

VERSION = "2026-10-14-055"
MD5_COMP = "031a4b6eac490bda17c75b65ccaa7906"
BRIAN2 = "2.10.1"
TOL_RADIO = 1e-6
TIPO = "SHUF_G"
R_POI_HZ = 100.0
COLS = ("Presynaptic_Index", "Postsynaptic_Index", "Excitatory x Connectivity")
MD5_REF = {  # las fuentes de NULO_MISMO que cita el sello (049 para k 0 a 39, humo de la 051 para k 99)
    "liq_SHUF_G_k000.json": "05bedf6fc250ed8c053d99236f3052bf",
    "liq_SHUF_G_k020.json": "62982026c51da6756caba9ba49f91eae",
    "umb_SHUF_G_k099.json": "dddfaeb2957cd40a2b202a39d931cf51",
}


def pr(s):
    print(s, flush=True)


def leer_aristas(ruta):
    df = pd.read_parquet(ruta, columns=list(COLS))
    return tuple(df[c].to_numpy() for c in COLS)


def escribir_aristas(ruta, pre, post, w):
    pd.DataFrame({COLS[0]: pre, COLS[1]: post, COLS[2]: w}).to_parquet(ruta)


def hacer_nulo(pre, post, w, k):
    """El SHUF_G de la 049 y la 051, sin cambios: nulo() de liq_entera.py."""
    return le.nulo(pre, post, w, TIPO, k)


def radio(n, pre, post, w):
    """Radio espectral crudo con el eigs de liq_entera.py (W[post, pre], duplicados sumados)."""
    W = sp.coo_matrix((np.asarray(w, dtype=np.float64), (post, pre)), shape=(n, n)).tocsr()
    return le.radio_crudo(W)


def nulo_mismo(r, ref):
    """PASA si el radio releido coincide con el de la referencia (tolerancia relativa TOL_RADIO)."""
    if ref is None:
        return {"radio_crudo": r, "radio_ref": None, "dif_rel": None, "estado": "SIN_REF"}
    d = abs(r - ref) / abs(ref) if ref != 0 else (0.0 if r == 0 else float("inf"))
    return {"radio_crudo": r, "radio_ref": ref, "dif_rel": d, "estado": "PASA" if d <= TOL_RADIO else "FALLA"}


def atajo(n, pre, post, w, estim, lect):
    """Descriptivo del sello: n1 aristas directas de los estimulados a la lectura, D1+ su peso excitatorio y
    D2+ = (W+ (W+ e)) en la lectura, con W+ la parte positiva de W[post, pre] crudo y e el indicador del estimulo."""
    w = np.asarray(w, dtype=np.float64)
    pre = np.asarray(pre, dtype=np.int64)
    post = np.asarray(post, dtype=np.int64)
    es = np.zeros(n, dtype=bool)
    es[np.asarray(estim, dtype=np.int64)] = True
    sel = es[pre] & (post == lect)
    Wp = sp.coo_matrix((np.maximum(w, 0.0), (post, pre)), shape=(n, n)).tocsr()
    v1 = Wp @ es.astype(np.float64)
    v2 = Wp @ v1
    return {"n1": int(sel.sum()), "D1+": float(w[sel & (w > 0)].sum()), "D1+_matriz": float(v1[lect]),
            "D2+": float(v2[lect])}


def pin_modelo(ruta_model):
    b = ls.blob(ruta_model)
    pr("MODEL blob=%s esperado=%s -> %s" % (b, ls.BLOB_MODEL, b == ls.BLOB_MODEL))
    if b != ls.BLOB_MODEL:
        pr("ABORTA: model.py no es el de Shiu en 91bdd1e7")
        raise SystemExit(3)
    return b


def pin_ref(rutas, sin_pin):
    """Lee los radios de referencia; sin --sin-pin exige el md5 que cita el sello para cada archivo."""
    ref, md5s = {}, {}
    for r in rutas:
        m = le.md5(r)
        base = os.path.basename(r)
        md5s[base] = m
        pr("REF %s md5=%s esperado=%s -> %s" % (base, m, MD5_REF.get(base), MD5_REF.get(base) == m))
        if not sin_pin and MD5_REF.get(base) != m:
            pr("ABORTA: referencia de NULO_MISMO que no es la del sello")
            raise SystemExit(3)
        for k, v in json.load(open(r))["nulos"].items():
            ref[int(k)] = float(v["radio_crudo"])
    return ref, md5s


def pin_datos(conn, comp, sin_pin):
    mc, mk = le.md5(conn), le.md5(comp)
    pr("PIN conn=%s -> %s comp=%s -> %s" % (mc, mc == le.MD5["conn"], mk, mk == MD5_COMP))
    if not sin_pin and (mc != le.MD5["conn"] or mk != MD5_COMP):
        pr("ABORTA: pin de datos")
        raise SystemExit(3)
    return {"conn": mc, "comp": mk}


def guardar(out, nombre, res, t_ini):
    res["segundos"] = time.time() - t_ini
    tmp = os.path.join(out, nombre + ".json.tmp")
    with open(tmp, "w") as f:
        json.dump(res, f, indent=1)
    os.replace(tmp, os.path.join(out, nombre + ".json"))


def simular(shiu, nombre, estim_ids, a, ruta_con, params, ids, leer):
    t1 = time.time()
    shiu.run_exp(exp_name=nombre, neu_exc=estim_ids, path_res=a.out, path_comp=a.comp, path_con=ruta_con,
                 params=params, n_proc=a.n_proc, force_overwrite=True)
    r = ls.resumir(os.path.join(a.out, nombre + ".parquet"), ids, estim_ids, leer, a.n_run, a.t_run_ms / 1000.0)
    r["segundos"] = time.time() - t1
    pr("CORRIDA %s E_MN9=%d de %d F_MN9=%.2f Hz espigas=%d activas=%d K=%d | %.1f s" % (
        nombre, r["ensayos_mn9"], a.n_run, r["tasa_mn9"], r["espigas"], r["activas"], r["K"], r["segundos"]))
    return r


def correr(a, shiu, Hz, ms, meta):
    """Todo lo que no es PIN: grafo, nulos, NULO_MISMO, atajo, simulacion y JSON (parcial despues de cada nulo)."""
    t_ini = time.time()
    os.makedirs(a.out, exist_ok=True)
    ids = pd.read_csv(a.comp, index_col=0).index.to_numpy(dtype=np.int64)
    n = len(ids)
    presentes = set(ids.tolist())
    estim_ids = [int(x) for x in a.estim.split(",")] if a.estim else [f for f in le.SUGAR if f in presentes]
    leer = int(a.leer) if a.leer else le.MN9
    estim = le.indices(ids, estim_ids)
    i_lect = int(le.indices(ids, [leer])[0])
    params = dict(shiu.default_params)
    params["r_poi"] = R_POI_HZ * Hz
    params["n_run"] = a.n_run
    params["t_run"] = a.t_run_ms * ms
    pre, post, w = leer_aristas(a.conn)
    pr("GRAFO n=%d aristas=%d estimulo=%d lectura=%d (indice %d) n_run=%d t_run=%.0f ms r_poi=%.0f Hz" % (
        n, len(pre), len(estim), leer, i_lect, a.n_run, a.t_run_ms, R_POI_HZ))
    res = {"version": VERSION, "sello": "SELLO-LIF-SHUFG-054.md", "humo": a.humo, "sin_pin": a.sin_pin,
           "modo": a.modo, "model_blob": meta["model_blob"], "brian2": meta["brian2"], "md5": meta["md5"],
           "entorno": {"numpy": np.__version__, "pandas": pd.__version__, "scipy": scipy.__version__},
           "n": n, "aristas": int(len(pre)), "estim_ids": estim_ids, "leer": leer, "i_lect": i_lect,
           "n_run": a.n_run, "t_run_ms": a.t_run_ms, "r_poi_hz": R_POI_HZ}
    if a.modo == "real":
        nombre = "lif_shufg_real"
        res["atajo"] = atajo(n, pre, post, w, estim, i_lect)
        pr("ATAJO real n1=%d D1+=%.1f D2+=%.1f" % (res["atajo"]["n1"], res["atajo"]["D1+"], res["atajo"]["D2+"]))
        res["corrida"] = simular(shiu, "real", estim_ids, a, a.conn, params, ids, leer)
        guardar(a.out, nombre, res, t_ini)
    else:
        nombre = "lif_shufg_G_k%03d" % a.k0
        res.update({"tipo": TIPO, "k0": a.k0, "n_nulos": a.n, "nulos": {}})
        for k in range(a.k0, a.k0 + a.n):
            t1 = time.time()
            _, q2, _ = hacer_nulo(pre, post, w, k)
            ruta = os.path.join(a.out, "shufG_%03d.parquet" % k)
            escribir_aristas(ruta, pre, q2, w)
            del q2
            p3, q3, w3 = leer_aristas(ruta)  # lo mismo que va a leer el model.py de Shiu
            nm = nulo_mismo(radio(n, p3, q3, w3), meta["ref"].get(k))
            at = atajo(n, p3, q3, w3, estim, i_lect)
            del p3, q3, w3
            pr("NULO_MISMO k=%d radio=%.9f ref=%s dif_rel=%s -> %s" % (k, nm["radio_crudo"], nm["radio_ref"],
                                                                       nm["dif_rel"], nm["estado"]))
            pr("ATAJO k=%d n1=%d D1+=%.1f D2+=%.1f" % (k, at["n1"], at["D1+"], at["D2+"]))
            v = {"nulo_mismo": nm, "atajo": at, "corrida": None}
            if nm["estado"] == "PASA":
                v["corrida"] = simular(shiu, "SHUF_G_%d" % k, estim_ids, a, ruta, params, ids, leer)
            else:
                pr("NO_MEDIDO k=%d: NULO_MISMO %s, no se simula" % (k, nm["estado"]))
            os.remove(ruta)
            v["segundos"] = time.time() - t1
            res["nulos"][str(k)] = v
            guardar(a.out, nombre, res, t_ini)
    guardar(a.out, nombre, res, t_ini)
    pr("JSON %s md5=%s" % (nombre + ".json", le.md5(os.path.join(a.out, nombre + ".json"))))
    pr("FIN segundos=%.1f" % res["segundos"])
    return res


def argumentos(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--shiu", required=True, help="carpeta con el model.py de Shiu")
    ap.add_argument("--conn", required=True)
    ap.add_argument("--comp", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--modo", choices=("real", "nulos"), required=True)
    ap.add_argument("--k0", type=int, default=0)
    ap.add_argument("--n", type=int, default=1)
    ap.add_argument("--n-run", type=int, default=None, help="por defecto 30 en el real y 10 en los nulos")
    ap.add_argument("--t-run-ms", type=float, default=1000.0)
    ap.add_argument("--n-proc", type=int, default=-1)
    ap.add_argument("--ref", action="append", default=[], help="JSON con los radios crudos de referencia")
    ap.add_argument("--sin-pin", action="store_true", help="solo para la prueba con grafos chicos")
    ap.add_argument("--estim", default="", help="ids a estimular (solo prueba); por defecto el azucar de Shiu")
    ap.add_argument("--leer", default="", help="id a leer (solo prueba); por defecto MN9")
    ap.add_argument("--humo", action="store_true")
    a = ap.parse_args(argv)
    if a.n_run is None:
        a.n_run = 30 if a.modo == "real" else 10
    if a.modo == "nulos" and not a.ref:
        ap.error("--ref es obligatorio con --modo nulos")
    return a


def main(argv=None):
    a = argumentos(argv)
    os.makedirs(a.out, exist_ok=True)
    pr("== lif_shufg.py :: H_LIF_SHUFG (2026-10-14-055), sello SELLO-LIF-SHUFG-054.md ==")
    b = pin_modelo(os.path.join(a.shiu, "model.py"))
    ref, md5_ref = pin_ref(a.ref, a.sin_pin) if a.modo == "nulos" else ({}, {})
    md5s = pin_datos(a.conn, a.comp, a.sin_pin)
    md5s["ref"] = md5_ref
    sys.path.insert(0, a.shiu)
    import brian2  # noqa: E402
    from brian2 import Hz, ms  # noqa: E402
    pr("ENTORNO brian2=%s numpy=%s pandas=%s scipy=%s" % (brian2.__version__, np.__version__, pd.__version__,
                                                       scipy.__version__))
    if brian2.__version__ != BRIAN2:
        pr("ABORTA: brian2 %s, el sello fija %s" % (brian2.__version__, BRIAN2))
        raise SystemExit(3)
    import model as shiu  # noqa: E402
    return correr(a, shiu, Hz, ms, {"model_blob": b, "brian2": brian2.__version__, "md5": md5s, "ref": ref})


if __name__ == "__main__":
    main()
