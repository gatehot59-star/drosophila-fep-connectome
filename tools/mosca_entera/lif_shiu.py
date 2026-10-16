#!/usr/bin/env python3
"""H_MOSCA_ENTERA, brazo LIF_SHIU (respuesta 2026-10-14-047).

Corre el model.py de Shiu et al. 2024 sin cambios (philshiu/Drosophila_brain_model en 91bdd1e7, blob 5ba7083c) con
default_params salvo r_poi = 100 Hz, sobre nuestro parquet (el mismo blob que su Connectivity_783.parquet) o sobre
un nulo SHUF_W (los pesos permutados entre aristas, con la misma funcion nulo() de liq_entera.py).
Uso:
  python3 lif_shiu.py --shiu DIR --conn C --comp K --out D --modo real --n-run 30
  python3 lif_shiu.py --shiu DIR --conn C --comp K --out D --modo shuf --k0 0 --n 10 --n-run 10
"""
import argparse
import hashlib
import json
import os
import sys
import time

import numpy as np
import pandas as pd

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import liq_entera as le  # noqa: E402

BLOB_MODEL = "5ba7083cf55bf6092967f8d9065e86cd677efed1"
UMBRAL_HZ = 1.0


def pr(s):
    print(s, flush=True)


def blob(ruta):
    d = open(ruta, "rb").read()
    return hashlib.sha1(b"blob %d" % len(d) + bytes(1) + d).hexdigest()


def resumir(ruta_spk, ids, estim_ids, mn9, n_run, t_run_s):
    """De los spikes de Shiu (t, trial, flywire_id) a: ensayos con espiga de MN9, tasa de MN9 y S_LIF."""
    df = pd.read_parquet(ruta_spk) if os.path.exists(ruta_spk) else pd.DataFrame(columns=["t", "trial", "flywire_id"])
    ens_mn9 = int(df.loc[df["flywire_id"] == mn9, "trial"].nunique())
    cuenta = df.groupby("flywire_id").size()
    tasa = cuenta / (n_run * t_run_s)
    excl = set(int(x) for x in estim_ids)
    s_lif = sorted(int(f) for f, v in tasa.items() if v >= UMBRAL_HZ and int(f) not in excl)
    pos = {int(f): i for i, f in enumerate(ids)}
    return {"ensayos_mn9": ens_mn9, "n_run": n_run, "tasa_mn9": float(tasa.get(mn9, 0.0)),
            "espigas": int(len(df)), "activas": int(len(cuenta)), "S_LIF_ids": s_lif,
            "S_LIF_idx": [pos[f] for f in s_lif], "K": len(s_lif)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--shiu", required=True, help="carpeta con el model.py de Shiu")
    ap.add_argument("--conn", required=True)
    ap.add_argument("--comp", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--modo", choices=("real", "shuf"), required=True)
    ap.add_argument("--k0", type=int, default=0)
    ap.add_argument("--n", type=int, default=1)
    ap.add_argument("--n-run", type=int, default=30)
    ap.add_argument("--t-run-ms", type=float, default=1000.0)
    ap.add_argument("--n-proc", type=int, default=-1)
    ap.add_argument("--sin-pin", action="store_true", help="solo para la prueba con grafos chicos")
    ap.add_argument("--estim", default="", help="ids a estimular (solo prueba); por defecto el azucar de Shiu")
    ap.add_argument("--leer", default="", help="id a leer (solo prueba); por defecto MN9")
    ap.add_argument("--humo", action="store_true")
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    t_ini = time.time()
    ruta_model = os.path.join(a.shiu, "model.py")
    b = blob(ruta_model)
    pr("== lif_shiu.py :: H_MOSCA_ENTERA, brazo LIF_SHIU (2026-10-14-047) ==")
    pr("MODEL blob=%s esperado=%s -> %s" % (b, BLOB_MODEL, b == BLOB_MODEL))
    if b != BLOB_MODEL:
        pr("ABORTA: model.py no es el de Shiu en 91bdd1e7")
        raise SystemExit(3)
    sys.path.insert(0, a.shiu)
    import brian2  # noqa: E402
    from brian2 import Hz, ms  # noqa: E402
    import model as shiu  # noqa: E402
    pr("ENTORNO brian2=%s numpy=%s pandas=%s" % (brian2.__version__, np.__version__, pd.__version__))
    if not a.sin_pin:
        mc = le.md5(a.conn)
        pr("PIN conn=%s -> %s" % (mc, mc == le.MD5["conn"]))
        if mc != le.MD5["conn"]:
            pr("ABORTA: pin del parquet")
            raise SystemExit(3)
    ids = pd.read_csv(a.comp, index_col=0).index.to_numpy(dtype=np.int64)
    presentes = set(ids.tolist())
    estim_ids = [int(x) for x in a.estim.split(",")] if a.estim else [f for f in le.SUGAR if f in presentes]
    leer = int(a.leer) if a.leer else le.MN9
    pr("ESTIMULO %d neuronas a 100 Hz, lectura %d, n_run=%d, t_run=%.0f ms" % (len(estim_ids), leer, a.n_run,
                                                                            a.t_run_ms))
    params = dict(shiu.default_params)
    params["r_poi"] = 100 * Hz
    params["n_run"] = a.n_run
    params["t_run"] = a.t_run_ms * ms
    res = {"version": "2026-10-14-047", "humo": a.humo, "modo": a.modo, "model_blob": b, "brian2": brian2.__version__,
           "estim_ids": estim_ids, "leer": leer, "n_run": a.n_run, "t_run_ms": a.t_run_ms, "corridas": {}}
    if a.modo == "real":
        trabajos = [("real", a.conn)]
    else:
        df = pd.read_parquet(a.conn)
        trabajos = []
        for k in range(a.k0, a.k0 + a.n):
            pre = df["Presynaptic_Index"].to_numpy()
            post = df["Postsynaptic_Index"].to_numpy()
            w = df["Excitatory x Connectivity"].to_numpy()
            _, _, w2 = le.nulo(pre, post, w, "SHUF_W", k)
            d2 = pd.DataFrame({"Presynaptic_Index": pre, "Postsynaptic_Index": post,
                               "Excitatory x Connectivity": w2})
            ruta = os.path.join(a.out, "shufW_%03d.parquet" % k)
            d2.to_parquet(ruta)
            trabajos.append(("SHUF_W_%d" % k, ruta))
        del df
    for nombre, ruta_con in trabajos:
        t1 = time.time()
        shiu.run_exp(exp_name=nombre, neu_exc=estim_ids, path_res=a.out, path_comp=a.comp, path_con=ruta_con,
                     params=params, n_proc=a.n_proc, force_overwrite=True)
        r = resumir(os.path.join(a.out, nombre + ".parquet"), ids, estim_ids, leer, a.n_run, a.t_run_ms / 1000.0)
        r["segundos"] = time.time() - t1
        res["corridas"][nombre] = r
        pr("CORRIDA %s ensayos_con_espiga_lectura=%d de %d tasa_lectura=%.2f Hz espigas=%d activas=%d K=%d | %.1f s" % (
            nombre, r["ensayos_mn9"], a.n_run, r["tasa_mn9"], r["espigas"], r["activas"], r["K"], r["segundos"]))
        if ruta_con != a.conn:
            os.remove(ruta_con)
    res["segundos"] = time.time() - t_ini
    nombre = "lif_real" if a.modo == "real" else "lif_shufW_k%03d" % a.k0
    with open(os.path.join(a.out, nombre + ".json"), "w") as f:
        json.dump(res, f, indent=1)
    pr("JSON %s md5=%s" % (nombre + ".json", le.md5(os.path.join(a.out, nombre + ".json"))))
    pr("FIN segundos=%.1f" % res["segundos"])


if __name__ == "__main__":
    main()
