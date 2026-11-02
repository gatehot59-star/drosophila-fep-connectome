#!/usr/bin/env python3
"""H_MECANISMO, instrumento de intervenciones (respuesta 2026-11-02-002).

Corre el LIF de Shiu et al. 2024 SIN CAMBIOS (model.py de philshiu/Drosophila_brain_model en 91bdd1e7, blob
5ba7083c): usa create_model() y poi() tal cual, con default_params salvo r_poi, n_run y t_run. Cada intervencion es una
edicion de pesos sinapticos ANTES de correr, hecha sobre syn.w_ con mascaras (pre, post) sobre los conjuntos S, X y D
de conjuntos_flywire.json (sha256 fijado en el sello). Silenciar con mascara es identico a silence() de Shiu: lo prueba
prueba_mecanismo.py.

Condiciones: C0 intacto; C1 silenciar X; C2 cortar S->X; C3 cortar X->D; C4 cortar S->D; R1 X conserva solo X->D;
R2 X recibe solo desde S; R3 S conserva solo S->D; R4 S conserva solo S->D y S->X; M5 X glutamatergicas -> D pasan a
excitatorias; K silenciar inhibicion no del motivo, reclutada y emparejada (regla en elegir_k).
Semillas: brian2.seed(20261102 + t) antes de cada ensayo t, iguales en todas las condiciones (numeros aleatorios
comunes). Esto mide causalidad DEL MODELO, no de la mosca.
Uso: python3 intervenir.py --shiu DIR --conn C --comp K --conjuntos J --celda NOMBRE --out D [--n-proc 3]
"""
import argparse
import gc
import hashlib
import json
import os
import sys
import time

import numpy as np
import pandas as pd

VERSION = "2026-11-02-002"
BLOB_MODEL = "5ba7083cf55bf6092967f8d9065e86cd677efed1"
MD5_CONN = "3d802fd542b5d18570ba1ba0bb0abed9"
MD5_COMP = "031a4b6eac490bda17c75b65ccaa7906"
SHA_CONJ = "f3e8602a6bcf3daefc3b83965f7793a2648f59a22bf8df6209d09ed19e0a3c2d"
SEMILLA0 = 20261102
T_TEMPRANO_MS = 50.0
SUGAR = [720575940624963786, 720575940630233916, 720575940637568838, 720575940638202345, 720575940617000768,
         720575940630797113, 720575940632889389, 720575940621754367, 720575940621502051, 720575940640649691,
         720575940639332736, 720575940616885538, 720575940639198653, 720575940620900446, 720575940617937543,
         720575940632425919, 720575940633143833, 720575940612670570, 720575940628853239, 720575940629176663,
         720575940611875570]
MN9 = 720575940660219265
TODAS = ("C0", "C1", "C2", "C3", "C4", "R1", "R2", "R3", "R4", "M5", "K")
BASICAS = ("C0", "C1", "C2", "C3", "C4")
ESTIM = ("LC4", "LPLC2", "LPLC1", "LPLC4")


def _celdas():
    c = {}
    for e in ESTIM:
        c["p_%s_right" % e] = {"estimulo": e + "_right", "hz": 50.0, "conds": list(TODAS), "n_run": 20}
        c["t20_%s_right" % e] = {"estimulo": e + "_right", "hz": 20.0, "conds": ["C0", "C1"], "n_run": 20}
        c["t150_%s_right" % e] = {"estimulo": e + "_right", "hz": 150.0, "conds": ["C0", "C1"], "n_run": 20}
        c["i_%s_left" % e] = {"estimulo": e + "_left", "hz": 50.0, "conds": list(BASICAS), "n_run": 20}
    c["ctrl_mn9"] = {"estimulo": "SUGAR", "hz": 100.0, "conds": ["C0"], "n_run": 10}
    return c


CELDAS = _celdas()


def pr(s):
    print(s, flush=True)


def md5(ruta):
    h = hashlib.md5()
    with open(ruta, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def sha256(ruta):
    h = hashlib.sha256()
    with open(ruta, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def blob(ruta):
    b = open(ruta, "rb").read()
    return hashlib.sha1(b"blob " + str(len(b)).encode() + b"\0" + b).hexdigest()


def mascara(i, j, n, op):
    """op = (accion, pre, pre_negado, post, post_negado); un conjunto None es 'cualquiera'."""
    _, ps, pn, qs, qn = op
    m = np.ones(len(i), dtype=bool)
    if ps is not None:
        b = np.zeros(n, dtype=bool)
        b[np.asarray(ps, dtype=np.int64)] = True
        m &= ~b[i] if pn else b[i]
    if qs is not None:
        b = np.zeros(n, dtype=bool)
        b[np.asarray(qs, dtype=np.int64)] = True
        m &= ~b[j] if qn else b[j]
    return m


def editar_pesos(w, i, j, n, ops):
    """Devuelve una copia de w con las ediciones: 'cero' pone 0; 'abs' pasa a |w| (signo excitatorio)."""
    w = np.array(w, dtype=np.float64, copy=True)
    for op in ops:
        m = mascara(i, j, n, op)
        if op[0] == "cero":
            w[m] = 0.0
        elif op[0] == "abs":
            w[m] = np.abs(w[m])
        else:
            raise ValueError(op[0])
    return w


def operaciones(cond, S, X, D, Xglu, K):
    """Las ediciones de cada condicion, sobre indices de Shiu."""
    DX = sorted(set(D) | set(X))
    return {
        "C0": [],
        "C1": [("cero", X, False, None, False)],
        "C2": [("cero", S, False, X, False)],
        "C3": [("cero", X, False, D, False)],
        "C4": [("cero", S, False, D, False)],
        "R1": [("cero", X, False, D, True)],
        "R2": [("cero", S, True, X, False)],
        "R3": [("cero", S, False, D, True)],
        "R4": [("cero", S, False, DX, True)],
        "M5": [("abs", Xglu, False, D, False)],
        "K": [("cero", K, False, None, False)] if K else [],
    }[cond]


def tocadas(i, j, w, n, ops):
    """Cuantas filas con peso no nulo cambian y cuanto peso absoluto se mueve (en unidades del parquet)."""
    w2 = editar_pesos(w, i, j, n, ops)
    d = w2 != w
    return {"filas": int(d.sum()), "peso_abs": float(np.abs(w - w2)[d].sum())}


def ensayo(model_dir, comp, conn, params, exc, seed, ops, mirar, d_idx, target):
    """Un ensayo: red nueva de Shiu (create_model + poi sin cambios), ediciones, semilla, 1 corrida."""
    if model_dir not in sys.path:
        sys.path.insert(0, model_dir)
    import brian2
    import model as shiu
    if target:
        brian2.prefs.codegen.target = target
    gc.collect()
    brian2.seed(int(seed))
    neu, syn, mon = shiu.create_model(comp, conn, params)
    pois, neu = shiu.poi(neu, exc, [], params)
    if ops:
        i = np.asarray(syn.i[:], dtype=np.int64)
        j = np.asarray(syn.j[:], dtype=np.int64)
        syn.w_[:] = editar_pesos(np.asarray(syn.w_[:]), i, j, len(neu), ops)
        del i, j
    net = brian2.Network(neu, syn, mon, *pois)
    t1 = time.time()
    net.run(duration=params["t_run"])
    cnt = np.asarray(mon.count[:], dtype=np.int64)
    ii = np.asarray(mon.i[:], dtype=np.int64)
    tt = np.asarray(mon.t_[:], dtype=np.float64) * 1000.0
    md = np.isin(ii, np.asarray(d_idx, dtype=np.int64))
    td = tt[md]
    out = {"seed": int(seed), "cuentas": cnt[np.asarray(mirar, dtype=np.int64)].tolist(),
           "D_primera_ms": float(td.min()) if len(td) else None,
           "D_temprano": int((td < T_TEMPRANO_MS).sum()), "espigas": int(len(ii)),
           "activas": int((cnt > 0).sum()), "seg_run": time.time() - t1}
    del net, neu, syn, mon, pois
    gc.collect()
    return out


def correr_cond(a, params, exc, ops, mirar, d_idx, n_run, Hz, ms):
    from joblib import Parallel, delayed, parallel_backend
    seeds = [SEMILLA0 + t for t in range(n_run)]
    with parallel_backend("loky", n_jobs=a.n_proc):
        res = Parallel()(delayed(ensayo)(a.shiu, a.comp, a.conn, params, exc, s, ops, mirar, d_idx, a.target)
                         for s in seeds)
    return res


def elegir_k(pool, drive_pool, drive_x):
    """Regla K: el pool en orden de impulso efectivo descendente (empates por indice), solo impulso > 0, hasta
    igualar o superar el impulso de X. Devuelve (elegidos, impulso acumulado, alcanzo)."""
    orden = sorted(((-float(d), int(p)) for p, d in zip(pool, drive_pool) if d > 0))
    ele, acc = [], 0.0
    for nd, p in orden:
        if acc >= drive_x:
            break
        ele.append(p)
        acc += -nd
    return ele, acc, bool(acc >= drive_x and drive_x > 0)


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
    ap.add_argument("--sin-pin", action="store_true", help="solo prueba con grafos sinteticos")
    a = ap.parse_args()
    t_ini = time.time()
    os.makedirs(a.out, exist_ok=True)
    sys.path.insert(0, a.shiu)
    ruta_model = os.path.join(a.shiu, "model.py")
    pines = {"model": blob(ruta_model) == BLOB_MODEL, "conn": md5(a.conn) == MD5_CONN,
             "comp": md5(a.comp) == MD5_COMP, "conjuntos": sha256(a.conjuntos) == SHA_CONJ}
    pr("== intervenir.py :: H_MECANISMO (%s) celda=%s ==" % (VERSION, a.celda))
    pr("PINES %s sin_pin=%s" % (json.dumps(pines, sort_keys=True), a.sin_pin))
    if not pines["model"]:
        pr("ABORTA: model.py no es el de Shiu en 91bdd1e7")
        raise SystemExit(3)
    if not a.sin_pin and not all(pines.values()):
        pr("ABORTA: pin")
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
    c = df["Connectivity"].to_numpy(dtype=np.float64)
    w = df["Excitatory x Connectivity"].to_numpy(dtype=np.float64)
    del df
    gc.collect()
    pr("GRAFO n=%d filas=%d indices_ok=%s" % (n, len(i), indices_ok))
    if not indices_ok:
        pr("ABORTA: los indices del parquet no son la posicion en Completeness")
        raise SystemExit(3)
    res = {"version": VERSION, "celda": a.celda, "def": cel, "n_run": n_run, "t_run_ms": a.t_run_ms,
           "pines": pines, "sin_pin": a.sin_pin, "brian2": brian2.__version__, "numpy": np.__version__,
           "pandas": pd.__version__, "target": a.target or str(brian2.prefs.codegen.target), "conds": {},
           "guardas": {}}
    if cel["estimulo"] == "SUGAR":
        faltan = [f for f in SUGAR if f not in f2i]
        S = [f2i[f] for f in SUGAR if f in f2i]
        X, D, Xglu, desc = [], [f2i[MN9]], [], []
        res["guardas"]["sugar_faltan"] = faltan
    else:
        e = conj["estimulos"][cel["estimulo"]]
        todos = e["S"] + e["X"] + e["D"]
        faltan = [f for f in todos if f not in f2i]
        res["guardas"]["faltan_ids"] = faltan
        if faltan:
            pr("ABORTA: %d ids de S, X o D no estan en Completeness" % len(faltan))
            raise SystemExit(3)
        S = [f2i[f] for f in e["S"]]
        X = [f2i[f] for f in e["X"]]
        D = [f2i[f] for f in e["D"]]
        Xglu = [f2i[f] for f, nt in zip(e["X"], e["X_nt"]) if nt == "glutamate"]
        dset = set(D)
        desc = [f2i[f] for f in conj["descendentes"]["root"] if f in f2i and f2i[f] not in dset]
        res["desc_tipo"] = [t for f, t in zip(conj["descendentes"]["root"], conj["descendentes"]["tipo"])
                            if f in f2i and f2i[f] not in dset]
        res["D_tipo"] = e["D_tipo"]
        res["X_tipo"] = e["X_tipo"]
    bX = np.zeros(n, dtype=bool)
    bX[X] = True
    x_inh = bool(np.all(w[bX[i]] < 0)) if X else True
    res["guardas"]["X_inhibitoria"] = x_inh
    bD = np.zeros(n, dtype=bool)
    bD[D] = True
    inh = np.zeros(n, dtype=bool)
    inh[i[w < 0]] = True
    syn_d = np.bincount(i[bD[j]], weights=c[bD[j]], minlength=n)
    excl = set(S) | set(X) | set(D)
    pool = [int(p) for p in np.flatnonzero(inh & (syn_d >= 5)) if int(p) not in excl] if X else []
    mirar = list(dict.fromkeys(S + X + D + desc + pool))
    n_nucleo = len(S) + len(X) + len(D)  # S, X y D van primero en mirar; son disjuntos (conjuntos.py lo exige)
    pos = {m: k for k, m in enumerate(mirar)}
    res["conjuntos"] = {"S": len(S), "X": len(X), "D": len(D), "X_glu": len(Xglu), "desc": len(desc),
                        "pool": len(pool)}
    res["indices"] = {"S": S, "X": X, "D": D, "X_glu": Xglu, "desc": desc, "pool": pool, "mirar": mirar,
                      "n_nucleo": n_nucleo}
    pr("CONJUNTOS %s X_inhibitoria=%s" % (json.dumps(res["conjuntos"]), x_inh))
    params = dict(shiu.default_params)
    params["r_poi"] = float(cel["hz"]) * Hz
    params["n_run"] = n_run
    params["t_run"] = a.t_run_ms * ms
    K = []
    for cond in cel["conds"]:
        if cond == "K":
            c0 = res["conds"]["C0"]["ensayos"]
            media = np.mean([r["cuentas"] for r in c0], axis=0)
            drive_x = float(sum(media[pos[x]] * syn_d[x] for x in X))
            drive_pool = [float(media[pos[p]] * syn_d[p]) for p in pool]
            K, acc, alcanzo = elegir_k(pool, drive_pool, drive_x)
            res["K"] = {"drive_x": drive_x, "drive_k": acc, "alcanzo": alcanzo, "n": len(K), "indices": K,
                        "syn_d_x": float(syn_d[X].sum()), "syn_d_k": float(syn_d[K].sum()) if K else 0.0}
            pr("K drive_x=%.1f drive_k=%.1f n=%d alcanzo=%s" % (drive_x, acc, len(K), alcanzo))
        ops = operaciones(cond, S, X, D, Xglu, K)
        toc = tocadas(i, j, w, n, ops)
        t1 = time.time()
        ens = correr_cond(a, params, S, ops, mirar, D, n_run, Hz, ms)
        sumD = [int(sum(r["cuentas"][pos[d]] for d in D)) for r in ens]
        sumX = [int(sum(r["cuentas"][pos[x]] for x in X)) for r in ens]
        if cond not in ("C0", "C1"):  # descendentes y pool solo hacen falta en C0 y C1
            for r in ens:
                r["cuentas"] = r["cuentas"][:n_nucleo]
        res["conds"][cond] = {"tocadas": toc, "ensayos": ens, "D": sumD, "X": sumX, "seg": time.time() - t1}
        pr("COND %s tocadas=%d D=%s X=%s | %.1f s" % (cond, toc["filas"], sumD, sumX, time.time() - t1))
        tmp = os.path.join(a.out, "celda_%s.json.tmp" % a.celda)
        res["segundos"] = time.time() - t_ini
        with open(tmp, "w") as f:
            json.dump(res, f)
        os.replace(tmp, os.path.join(a.out, "celda_%s.json" % a.celda))
    pr("FIN celda=%s %.1f s" % (a.celda, time.time() - t_ini))


if __name__ == "__main__":
    main()
