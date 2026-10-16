#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
output_control_by_class.py :: que salida controla cada clase (FlyWire v783).

Pedido 2026-10-10 (Abraham): "Medi que salida controla cada clase".

Salidas del cerebro = super_class eferentes de FlyWire:
  descending  al cordon ventral por el conectivo cervical (nerve=CV),
  motor       motoneuronas del cerebro, partidas por cell_sub_class
              (ingestion, neck, proboscis, antennal, crop, eye, haustellum, salivary),
  endocrine   neurosecretoras, partidas por cell_type (IPC, ITP, DH44, DH31, CRZ, DMS...).

Para cada clase de origen C y cada salida O, con S[i,j] = sinapsis i->j,
entrada_j = sum_i S[i,j] y A[i,j] = S[i,j] / entrada_j:
  D1(C,O)  media sobre j en O (con entrada > 0) de sum_{i en C} A[i,j]
           = fraccion de la entrada de una neurona de O que viene de C.
  D2(C,O)  lo mismo con A@A: influencia a traves de exactamente una intermedia.
  nulo     la misma media sobre conjuntos de destinos al azar del mismo tamano
           (neuronas con entrada > 0, con reposicion, R sorteos, semilla fija).
  enr      D / media del nulo. flag SOBRE o BAJO si el p unilateral <= P_FLAG.
  fila%    % de las sinapsis salientes de C que caen directo en O.
  cobert%  % de las neuronas de O con al menos una arista desde C.
  exc%     % de las sinapsis de C hacia O con presinaptico excitatorio
           (columna Excitatory del parquet: prediccion de neurotransmisor, no fisiologia).
  domina   neuronas de O cuya mayor entrada (en sinapsis) viene de C; empates aparte.
Variantes: sin umbral (>=1 sinapsis) y >=5 sinapsis por arista.

Controles que pueden dar rojo:
  CRUCE_TABLA7      aristas clase x clase identicas a las del JSON de
                    tools/table7_reciprocity_by_class.py (otro codigo, mismo dato).
  SUMA_D1           sum_C D1(C, j) = 1 para toda neurona con entrada.
  CONTROL_NEGATIVO  etiquetas de origen permutadas: los flags deben caer a <= 5% de los tests.
"""
import argparse
import hashlib
import json
import os
import platform
import time

import numpy as np
import pandas as pd
import pyarrow
import pyarrow.parquet as pq
import scipy
import scipy.sparse as sp

SALIDAS = ("descending", "motor", "endocrine")
SIN_ANOT = "sin_anotacion"
SEED = 20261010
R_NULO = 10000
R_CONTROL = 2000
P_FLAG = 0.001
TOL_CONTROL = 0.05
CHUNK = 200
PIN_PARQUET_MD5 = "3d802fd542b5d18570ba1ba0bb0abed9"
PIN_ANNOT_MD5 = "719904abad876c68ace1b5690c9b9b63"
ERRATUM_ITEM5_ARISTAS_UMBRAL5 = 2700513
CAMPOS = ("fila", "d1", "nulo1", "enr1", "ps1", "pb1", "flag1",
          "d2", "nulo2", "enr2", "ps2", "pb2", "flag2", "cov", "exc", "syn", "domina")


def md5_archivo(path, bloque=1 << 20):
    h = hashlib.md5()
    with open(path, "rb") as f:
        for b in iter(lambda: f.read(bloque), b""):
            h.update(b)
    return h.hexdigest()


def leer_grafo(parquet):
    """Lee el parquet columna por columna. Devuelve pre, post, S, exc, id_of, info."""
    pf = pq.ParquetFile(parquet)

    def col(nombre):
        return pf.read(columns=[nombre]).column(nombre).to_numpy()

    pre = col("Presynaptic_Index")
    post = col("Postsynaptic_Index")
    if min(int(pre.min()), int(post.min())) < 0:
        raise SystemExit("ERROR indice negativo en el parquet")
    n = int(max(int(pre.max()), int(post.max()))) + 1
    if n >= 2 ** 31:
        raise SystemExit("ERROR demasiados nodos para int32")
    pre = pre.astype(np.int32)
    post = post.astype(np.int32)
    id_of = np.full(n, -1, dtype=np.int64)
    pid = col("Presynaptic_ID")
    id_of[pre] = pid
    ok_pre = bool(np.array_equal(id_of[pre], pid))
    del pid
    qid = col("Postsynaptic_ID")
    previo = id_of[post]
    asig = previo >= 0
    ok_cruce = bool(np.array_equal(previo[asig], qid[asig]))
    del previo, asig
    id_of[post] = qid
    ok_post = bool(np.array_equal(id_of[post], qid))
    del qid
    S = col("Connectivity")
    if int(S.min()) < 1:
        raise SystemExit("ERROR Connectivity < 1")
    S = S.astype(np.int32)
    exc = col("Excitatory").astype(np.int8)
    asignados = id_of >= 0
    vals, cnts = np.unique(exc, return_counts=True)
    info = {
        "n_nodos": n,
        "n_aristas": int(len(S)),
        "nodos_sin_id": int((~asignados).sum()),
        "ids_unicos": int(np.unique(id_of[asignados]).size),
        "mapeo_biyectivo": bool(ok_pre and ok_cruce and ok_post and asignados.all()
                                and np.unique(id_of).size == n),
        "indice_es_rango_ordenado": bool(asignados.all() and np.all(np.diff(id_of) > 0)),
        "autolazos": int((pre == post).sum()),
        "sinapsis_total": int(S.astype(np.int64).sum()),
        "excitatory_valores": {str(int(v)): int(c) for v, c in zip(vals, cnts)},
    }
    return pre, post, S, exc, id_of, info


def _texto(v):
    if v is None:
        return None
    try:
        if pd.isna(v):
            return None
    except (TypeError, ValueError):
        pass
    s = str(v)
    return s if s != "" else None


def leer_anotaciones(path, id_of):
    cols = ["root_id", "super_class", "cell_class", "cell_sub_class", "cell_type"]
    a = pd.read_csv(path, sep="\t", dtype=str, usecols=cols, low_memory=False)
    filas = int(len(a))
    rid = a["root_id"].astype("int64").to_numpy()
    dup_mask = pd.Index(rid).duplicated(keep="first")
    dup = int(dup_mask.sum())
    if dup:
        a = a[~dup_mask]
        rid = rid[~dup_mask]
    pos = pd.Index(rid).get_indexer(id_of)
    n = len(id_of)
    m = pos >= 0

    def tomar(c):
        v = a[c].to_numpy(dtype=object)
        out = np.empty(n, dtype=object)
        out[:] = None
        out[m] = v[pos[m]]
        return np.array([_texto(x) for x in out], dtype=object)

    sc = tomar("super_class")
    sub = tomar("cell_sub_class")
    ct = tomar("cell_type")
    sin_fila = int((~m).sum())
    sc_vacia = int(sum(1 for x, ok in zip(sc, m) if ok and x is None))
    sc = np.array([SIN_ANOT if x is None else x for x in sc], dtype=object)
    return {"filas": filas, "duplicados": dup, "sin_fila": sin_fila,
            "super_class_vacia": sc_vacia, "super_class": sc,
            "cell_sub_class": sub, "cell_type": ct}


def codificar_clases(sc):
    presentes = set(sc.tolist())
    nombres = sorted(presentes - {SIN_ANOT})
    if SIN_ANOT in presentes:
        nombres.append(SIN_ANOT)
    cod = {c: i for i, c in enumerate(nombres)}
    cls = np.array([cod[x] for x in sc], dtype=np.int8)
    return nombres, cls


def conjuntos_salida(sc, sub, ct):
    n1 = {s: np.flatnonzero(sc == s).astype(np.int64) for s in SALIDAS}
    finas = {}
    for j in n1["motor"]:
        finas.setdefault("motor:" + (sub[j] or "sin_subclase"), []).append(int(j))
    for j in n1["endocrine"]:
        finas.setdefault("endocrine:" + (ct[j] or "sin_tipo"), []).append(int(j))
    n2 = {"descending": n1["descending"]}
    orden = sorted(finas, key=lambda L: (0 if L.startswith("motor:") else 1, -len(finas[L]), L))
    for lab in orden:
        n2[lab] = np.array(finas[lab], dtype=np.int64)
    return n1, n2


def por_variante(pre, post, S, exc, cls, n, K, umbral):
    """Matrices por neurona destino x clase de origen, y F (1 salto) y F2 (2 saltos)."""
    if umbral > 1:
        m = S >= umbral
        p, q, s, e = pre[m], post[m], S[m], exc[m]
        del m
    else:
        p, q, s, e = pre, post, S, exc
    sw = s.astype(np.float64)
    key = q.astype(np.int64) * K + cls[p].astype(np.int64)
    Ssyn = np.bincount(key, weights=sw, minlength=n * K).reshape(n, K)
    Sexc = np.bincount(key, weights=sw * (e > 0), minlength=n * K).reshape(n, K)
    Ned = np.bincount(key, minlength=n * K).reshape(n, K)
    del key
    ent = Ssyn.sum(axis=1)
    con = ent > 0
    F = np.zeros_like(Ssyn)
    F[con] = Ssyn[con] / ent[con, None]
    val = sw / ent[q]
    del sw
    AT = sp.csr_matrix((val, (q, p)), shape=(n, n))
    del val
    F2 = np.asarray(AT @ F)
    del AT
    return {"umbral": umbral, "n_aristas": int(len(s)),
            "sinapsis": int(s.astype(np.int64).sum()),
            "Ssyn": Ssyn, "Sexc": Sexc, "Ned": Ned, "ent": ent, "con": con,
            "F": F, "F2": F2, "p": p, "q": q, "s": s}


def medir(V, K, conjuntos):
    tot_out = V["Ssyn"].sum(axis=0)
    res = {}
    for nombre, idx in conjuntos.items():
        idx = np.asarray(idx, dtype=np.int64)
        idx_in = idx[V["con"][idx]]
        if len(idx_in):
            d1 = V["F"][idx_in].mean(axis=0)
            d2 = V["F2"][idx_in].mean(axis=0)
            sub = V["Ssyn"][idx_in]
            mx = sub.max(axis=1)
            unico = (sub == mx[:, None]).sum(axis=1) == 1
            dom = np.bincount(sub.argmax(axis=1)[unico], minlength=K)
            emp = int((~unico).sum())
        else:
            d1 = np.full(K, np.nan)
            d2 = np.full(K, np.nan)
            dom = np.zeros(K, dtype=np.int64)
            emp = 0
        syn = V["Ssyn"][idx].sum(axis=0)
        excs = V["Sexc"][idx].sum(axis=0)
        with np.errstate(invalid="ignore", divide="ignore"):
            fila = np.where(tot_out > 0, syn / tot_out, np.nan)
            excp = np.where(syn > 0, excs / syn, np.nan)
        cov = (V["Ned"][idx] > 0).mean(axis=0) if len(idx) else np.full(K, np.nan)
        res[nombre] = {"n": int(len(idx)), "n_con_entrada": int(len(idx_in)),
                       "sinapsis_entrada": float(V["ent"][idx].sum()),
                       "d1": d1, "d2": d2, "suma_d2": float(np.nansum(d2)),
                       "fila": fila, "exc": excp, "cov": cov, "syn": syn,
                       "domina": dom, "empates": emp}
    return res


def nulo_media(Fs, pob, n, R, semilla):
    """Medias de n filas sorteadas con reposicion de pob, R veces, para cada matriz de Fs."""
    rng = np.random.default_rng(semilla)
    K = Fs[0].shape[1]
    outs = [np.empty((R, K)) for _ in Fs]
    for a in range(0, R, CHUNK):
        b = min(R, a + CHUNK)
        idx = pob[rng.integers(0, len(pob), size=(b - a, n))]
        for F, o in zip(Fs, outs):
            o[a:b] = F[idx].mean(axis=1)
    return outs


def banderas(real, nul, p_flag=P_FLAG):
    R = nul.shape[0]
    media = nul.mean(axis=0)
    fin = np.isfinite(real)
    with np.errstate(invalid="ignore", divide="ignore"):
        enr = np.where(media > 0, real / media, np.nan)
    ps = (1 + (nul >= real[None, :]).sum(axis=0)) / (R + 1)
    pb = (1 + (nul <= real[None, :]).sum(axis=0)) / (R + 1)
    ps = np.where(fin, ps, np.nan)
    pb = np.where(fin, pb, np.nan)
    fl = np.where(ps <= p_flag, "SOBRE", np.where(pb <= p_flag, "BAJO", "azar"))
    fl = np.where(fin, fl, "NA")
    enr = np.where(fin, enr, np.nan)
    return media, enr, ps, pb, fl


def evaluar(V, K, conjuntos, R, semilla):
    res = medir(V, K, conjuntos)
    pob = np.flatnonzero(V["con"])
    cache = {}
    for nombre, r in res.items():
        n = r["n_con_entrada"]
        if n == 0:
            vacio = np.full(K, np.nan)
            na = np.array(["NA"] * K)
            for k in ("nulo1", "enr1", "ps1", "pb1", "nulo2", "enr2", "ps2", "pb2"):
                r[k] = vacio.copy()
            r["flag1"] = na.copy()
            r["flag2"] = na.copy()
            continue
        if n not in cache:
            cache[n] = nulo_media([V["F"], V["F2"]], pob, n, R, [semilla, V["umbral"], n])
        n1, n2 = cache[n]
        r["nulo1"], r["enr1"], r["ps1"], r["pb1"], r["flag1"] = banderas(r["d1"], n1)
        r["nulo2"], r["enr2"], r["ps2"], r["pb2"], r["flag2"] = banderas(r["d2"], n2)
    return res


def control_negativo(pre, post, S, cls, n, K, umbral, conjuntos, R, semilla):
    """Permuta las etiquetas de ORIGEN; deja los destinos reales. Debe quedar sin senal."""
    rng = np.random.default_rng([semilla, 7, umbral])
    clsp = rng.permutation(cls)
    if umbral > 1:
        m = S >= umbral
        p, q, s = pre[m], post[m], S[m]
    else:
        p, q, s = pre, post, S
    key = q.astype(np.int64) * K + clsp[p].astype(np.int64)
    Ssyn = np.bincount(key, weights=s.astype(np.float64), minlength=n * K).reshape(n, K)
    del key
    ent = Ssyn.sum(axis=1)
    con = ent > 0
    F = np.zeros_like(Ssyn)
    F[con] = Ssyn[con] / ent[con, None]
    pob = np.flatnonzero(con)
    flags, tests, det = 0, 0, []
    for nombre, idx in conjuntos.items():
        idx_in = idx[con[idx]]
        if not len(idx_in):
            continue
        real = F[idx_in].mean(axis=0)
        (nul,) = nulo_media([F], pob, len(idx_in), R, [semilla, 8, umbral, len(idx_in)])
        _, enr, _, _, fl = banderas(real, nul)
        for c in range(K):
            tests += 1
            if fl[c] in ("SOBRE", "BAJO"):
                flags += 1
                det.append([nombre, int(c), str(fl[c]), float(enr[c])])
    return {"flags": flags, "tests": tests, "detalle": det}


def matriz_aristas(V, cls, K):
    """Aristas por (clase presinaptica, clase postsinaptica)."""
    M = np.zeros((K, K), dtype=np.int64)
    for c in range(K):
        M[:, c] = V["Ned"][cls == c].sum(axis=0)
    return M


def cruce_tabla7(path, nombres, M1, M5, conteos):
    if not path or not os.path.exists(path):
        return {"estado": "NO_MEDIDO", "motivo": "sin JSON de tabla 7"}
    with open(path) as f:
        j = json.load(f)
    orden = list(j["sin_umbral"]["clases_orden"])
    if sorted(orden) != sorted(nombres):
        return {"estado": "FAIL", "motivo": "clases distintas", "orden_json": orden}
    perm = [orden.index(c) for c in nombres]
    T1 = np.array(j["sin_umbral"]["matriz_aristas"], dtype=np.int64)[np.ix_(perm, perm)]
    T5 = np.array(j["umbral_5"]["matriz_aristas"], dtype=np.int64)[np.ix_(perm, perm)]
    ok1 = bool(np.array_equal(T1, M1))
    ok5 = bool(np.array_equal(T5, M5))
    okc = {c: int(j["clases"].get(c, -1)) for c in nombres} == conteos
    return {"estado": "PASS" if (ok1 and ok5 and okc) else "FAIL",
            "sin_umbral_igual": ok1, "umbral_5_igual": ok5, "clases_igual": okc,
            "max_dif_sin_umbral": int(np.abs(T1 - M1).max()),
            "max_dif_umbral_5": int(np.abs(T5 - M5).max()),
            "json": path, "json_md5": md5_archivo(path)}


def top_tipos_dn(V, cls, K, idx_dn, ct, nombres, top=3):
    es_dn = np.zeros(len(cls), dtype=bool)
    es_dn[idx_dn] = True
    m = es_dn[V["q"]]
    q = V["q"][m]
    p = V["p"][m]
    s = V["s"][m].astype(np.float64)
    tipos = np.array([ct[j] or "sin_tipo" for j in idx_dn], dtype=object)
    uniq, tcod_dn = np.unique(tipos, return_inverse=True)
    tcod = np.full(len(cls), -1, dtype=np.int64)
    tcod[idx_dn] = tcod_dn
    T = len(uniq)
    key = cls[p].astype(np.int64) * T + tcod[q]
    M = np.bincount(key, weights=s, minlength=K * T).reshape(K, T)
    tam = np.bincount(tcod_dn, minlength=T)
    out = {}
    for c in range(K):
        tot = M[c].sum()
        orden = np.argsort(-M[c], kind="stable")[:top]
        out[nombres[c]] = [[str(uniq[t]), int(tam[t]), int(M[c, t]),
                            float(M[c, t] / tot) if tot > 0 else None]
                           for t in orden if M[c, t] > 0]
    return out


def a_py(x):
    if isinstance(x, dict):
        return {str(k): a_py(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)):
        return [a_py(v) for v in x]
    if isinstance(x, np.ndarray):
        return a_py(x.tolist())
    if isinstance(x, np.bool_):
        return bool(x)
    if isinstance(x, np.integer):
        return int(x)
    if isinstance(x, np.floating):
        x = float(x)
    if isinstance(x, float):
        return x if np.isfinite(x) else None
    if isinstance(x, np.str_):
        return str(x)
    return x


def serial(res, nombres):
    out = {}
    for nombre, r in res.items():
        d = {k: r[k] for k in ("n", "n_con_entrada", "sinapsis_entrada", "suma_d2", "empates")}
        d["por_clase"] = {cn: {k: r[k][c] for k in CAMPOS if k in r} for c, cn in enumerate(nombres)}
        out[nombre] = d
    return a_py(out)


def _p(x):
    return "    nan" if x is None or not np.isfinite(x) else "%7.2f" % (100.0 * x)


def _x(x):
    return "   nan" if x is None or not np.isfinite(x) else "%6.2f" % x


def imprimir_nivel1(etq, res, nombres):
    for nombre, r in res.items():
        print("-- SALIDA %s [%s] | n=%d | con_entrada=%d | sinapsis_entrada=%d | suma_D2=%.4f | empates=%d"
              % (nombre, etq, r["n"], r["n_con_entrada"], r["sinapsis_entrada"], r["suma_d2"], r["empates"]))
        print("%-19s %7s %7s %7s %6s %-5s %7s %7s %6s %-5s %7s %7s %6s"
              % ("clase", "fila%", "D1%", "nulo1%", "enr1", "flag1", "D2%", "nulo2%", "enr2", "flag2",
                 "cobert%", "exc%", "domina"))
        for c, cn in enumerate(nombres):
            print("%-19s %s %s %s %s %-5s %s %s %s %-5s %s %s %6d"
                  % (cn, _p(r["fila"][c]), _p(r["d1"][c]), _p(r["nulo1"][c]), _x(r["enr1"][c]),
                     r["flag1"][c], _p(r["d2"][c]), _p(r["nulo2"][c]), _x(r["enr2"][c]),
                     r["flag2"][c], _p(r["cov"][c]), _p(r["exc"][c]), r["domina"][c]))


def imprimir_nivel2(etq, res, nombres, top=3):
    print("-- QUIEN CONTROLA CADA SALIDA FINA [%s] (D1, top %d; enr = D1/nulo) --" % (etq, top))
    for nombre, r in res.items():
        d1 = np.nan_to_num(r["d1"], nan=-1.0)
        orden = np.argsort(-d1, kind="stable")[:top]
        partes = ["%s %s%% x%s %s" % (nombres[c], _p(r["d1"][c]).strip(), _x(r["enr1"][c]).strip(), r["flag1"][c])
                  for c in orden]
        print("FINA [%s] %-40s n=%4d con_entrada=%4d : %s"
              % (etq, nombre, r["n"], r["n_con_entrada"], " | ".join(partes)))


def resumen_por_clase(etq, res1, res2, nombres, top=4):
    print("-- QUE SALIDA CONTROLA CADA CLASE [%s] (salidas finas con D1 SOBRE el azar, por enr) --" % etq)
    lineas = {}
    for c, cn in enumerate(nombres):
        sobre = [(float(r["enr1"][c]), nombre, float(r["d1"][c]))
                 for nombre, r in res2.items() if r["flag1"][c] == "SOBRE" and np.isfinite(r["enr1"][c])]
        sobre.sort(key=lambda t: -t[0])
        txt = ", ".join("%s x%.2f (D1 %.2f%%)" % (nm, e, 100 * d) for e, nm, d in sobre[:top]) \
            if sobre else "ninguna sobre el azar"
        votos = [(float(r["d1"][c]), nombre) for nombre, r in res2.items() if np.isfinite(r["d1"][c])]
        voto = max(votos) if votos else (float("nan"), "NA")
        a_sal = sum(float(res1[s]["fila"][c]) for s in SALIDAS if np.isfinite(res1[s]["fila"][c]))
        n1 = ", ".join("%s %s" % (s, res1[s]["flag1"][c]) for s in SALIDAS)
        linea = ("QUE_CONTROLA [%s] %s: %s | mayor_voto: %s (D1 %.2f%%) | nivel1: %s | a_salidas %.2f%% de sus sinapsis"
                 % (etq, cn, txt, voto[1], 100 * voto[0], n1, 100 * a_sal))
        print(linea)
        lineas[cn] = linea
    return lineas


def main(argv=None):
    ap = argparse.ArgumentParser(description="Que salida controla cada clase (FlyWire v783)")
    ap.add_argument("--parquet", default="/workspace/connectivity.parquet")
    ap.add_argument("--annotations", default="/workspace/annotations.tsv")
    ap.add_argument("--cruce-tabla7",
                    default="results/table7_reconstruida_2026-10-10/table7_reciprocity_by_class.json")
    ap.add_argument("--out", default="results/output_control_2026-10-10")
    ap.add_argument("--seed", type=int, default=SEED)
    ap.add_argument("--r-nulo", type=int, default=R_NULO)
    ap.add_argument("--r-control", type=int, default=R_CONTROL)
    ap.add_argument("--maquina", default="brain-env")
    args = ap.parse_args(argv)
    t0 = time.time()
    os.makedirs(args.out, exist_ok=True)

    print("== output_control_by_class.py :: que salida controla cada clase ==")
    entorno = {"python": platform.python_version(), "numpy": np.__version__, "pandas": pd.__version__,
               "pyarrow": pyarrow.__version__, "scipy": scipy.__version__, "maquina": args.maquina}
    print("ENTORNO " + " ".join("%s=%s" % kv for kv in entorno.items()))
    print("PARAMETROS seed=%d r_nulo=%d r_control=%d p_flag=%g tol_control=%g"
          % (args.seed, args.r_nulo, args.r_control, P_FLAG, TOL_CONTROL))
    md5p = md5_archivo(args.parquet)
    md5a = md5_archivo(args.annotations)
    inputs = {"parquet": args.parquet, "parquet_bytes": os.path.getsize(args.parquet), "parquet_md5": md5p,
              "parquet_md5_pin_ok": md5p == PIN_PARQUET_MD5, "annotations": args.annotations,
              "annotations_bytes": os.path.getsize(args.annotations), "annotations_md5": md5a,
              "annotations_md5_pin_ok": md5a == PIN_ANNOT_MD5}
    print("INPUT parquet %s bytes=%d md5=%s pin_ok=%s" % (args.parquet, inputs["parquet_bytes"], md5p,
                                                          inputs["parquet_md5_pin_ok"]))
    print("INPUT annotations %s bytes=%d md5=%s pin_ok=%s" % (args.annotations, inputs["annotations_bytes"],
                                                              md5a, inputs["annotations_md5_pin_ok"]))

    pre, post, S, exc, id_of, ginfo = leer_grafo(args.parquet)
    print("GRAFO " + " ".join("%s=%s" % (k, v) for k, v in ginfo.items()))
    anot = leer_anotaciones(args.annotations, id_of)
    print("ANOTACION filas=%d duplicados=%d nodos_sin_fila=%d super_class_vacia=%d"
          % (anot["filas"], anot["duplicados"], anot["sin_fila"], anot["super_class_vacia"]))
    nombres, cls = codificar_clases(anot["super_class"])
    K = len(nombres)
    n = len(id_of)
    conteos = {cn: int((cls == c).sum()) for c, cn in enumerate(nombres)}
    print("CLASES " + " ".join("%s=%d" % kv for kv in conteos.items()))
    n1, n2 = conjuntos_salida(anot["super_class"], anot["cell_sub_class"], anot["cell_type"])
    print("SALIDAS " + " ".join("%s=%d" % (k, len(v)) for k, v in n1.items()))
    print("SALIDAS_FINAS " + " ".join("%s=%d" % (k, len(v)) for k, v in n2.items()))
    conj_ctrl = dict(n1)
    conj_ctrl.update({k: v for k, v in n2.items() if k not in n1})

    resultado = {"schema": "output_control_by_class/v1", "inputs": inputs, "entorno": entorno,
                 "parametros": {"seed": args.seed, "r_nulo": args.r_nulo, "r_control": args.r_control,
                                "p_flag": P_FLAG, "tol_control": TOL_CONTROL},
                 "grafo": ginfo, "anotacion": {k: anot[k] for k in ("filas", "duplicados", "sin_fila",
                                                                     "super_class_vacia")},
                 "clases": conteos, "clases_orden": nombres,
                 "salidas": {k: len(v) for k, v in n1.items()},
                 "salidas_finas": {k: len(v) for k, v in n2.items()}, "variantes": {}}
    matrices = {}
    chequeos = {}
    for umbral, etq in ((1, ">=1"), (5, ">=5")):
        tv = time.time()
        V = por_variante(pre, post, S, exc, cls, n, K, umbral)
        print("== VARIANTE %s sinapsis | aristas=%d | sinapsis=%d | neuronas_con_entrada=%d =="
              % (etq, V["n_aristas"], V["sinapsis"], int(V["con"].sum())))
        dev = float(np.abs(V["F"][V["con"]].sum(axis=1) - 1.0).max()) if V["con"].any() else float("nan")
        chequeos["suma_d1_max_desvio_" + etq] = dev
        matrices[umbral] = matriz_aristas(V, cls, K)
        res1 = evaluar(V, K, n1, args.r_nulo, args.seed)
        res2 = evaluar(V, K, n2, args.r_nulo, args.seed)
        imprimir_nivel1(etq, res1, nombres)
        imprimir_nivel2(etq, res2, nombres)
        lineas = resumen_por_clase(etq, res1, res2, nombres)
        dn = top_tipos_dn(V, cls, K, n1["descending"], anot["cell_type"], nombres)
        if umbral == 5:
            print("-- TIPOS DE DESCENDENTES MAS ALIMENTADOS POR CADA CLASE [%s] (top 3 por sinapsis) --" % etq)
            for cn in nombres:
                print("DN_TOP [%s] %-19s: %s" % (etq, cn, " ; ".join(
                    "%s(%dn) %d sin %.2f%%" % (t, k, sy, 100 * (sh or 0)) for t, k, sy, sh in dn[cn]) or "-"))
        reales = 0
        tests_reales = 0
        for nombre in conj_ctrl:
            r = res1[nombre] if nombre in res1 else res2[nombre]
            for c in range(K):
                if r["flag1"][c] != "NA":
                    tests_reales += 1
                    reales += int(r["flag1"][c] in ("SOBRE", "BAJO"))
        ctrl = control_negativo(pre, post, S, cls, n, K, umbral, conj_ctrl, args.r_control, args.seed)
        ctrl["ok"] = bool(ctrl["flags"] <= TOL_CONTROL * ctrl["tests"])
        ctrl["flags_reales_mismos_tests"] = reales
        ctrl["tests_reales"] = tests_reales
        resultado["variantes"][etq] = {"n_aristas": V["n_aristas"], "sinapsis": V["sinapsis"],
                                       "neuronas_con_entrada": int(V["con"].sum()),
                                       "nivel1": serial(res1, nombres), "nivel2": serial(res2, nombres),
                                       "que_controla": lineas, "dn_top": dn, "control_negativo": ctrl,
                                       "matriz_aristas": matrices[umbral], "segundos": time.time() - tv}
        chequeos["control_" + etq] = ctrl
        del V, res1, res2
    cruce = cruce_tabla7(args.cruce_tabla7, nombres, matrices[1], matrices[5], conteos)
    resultado["cruce_tabla7"] = cruce
    u5 = resultado["variantes"][">=5"]["n_aristas"]
    print("CHEQUEO mapeo_biyectivo=%s indice_es_rango_ordenado=%s autolazos=%d"
          % (ginfo["mapeo_biyectivo"], ginfo["indice_es_rango_ordenado"], ginfo["autolazos"]))
    print("CRUCE_TABLA7 %s %s" % (cruce["estado"], " ".join("%s=%s" % (k, v) for k, v in cruce.items()
                                                          if k not in ("estado",))))
    suma_ok = all(v < 1e-9 for k, v in chequeos.items() if k.startswith("suma_d1"))
    print("SUMA_D1 max_desvio_>=1=%.3e max_desvio_>=5=%.3e OK=%s"
          % (chequeos["suma_d1_max_desvio_>=1"], chequeos["suma_d1_max_desvio_>=5"], suma_ok))
    print("UMBRAL5_ARISTAS %d erratum_item5=%d igual=%s" % (u5, ERRATUM_ITEM5_ARISTAS_UMBRAL5,
                                                            u5 == ERRATUM_ITEM5_ARISTAS_UMBRAL5))
    ctrl_ok = True
    for etq in (">=1", ">=5"):
        c = chequeos["control_" + etq]
        ctrl_ok = ctrl_ok and c["ok"]
        print("CONTROL_NEGATIVO [%s] flags_permutado=%d/%d tolerancia=%.1f flags_reales=%d/%d OK=%s"
              % (etq, c["flags"], c["tests"], TOL_CONTROL * c["tests"], c["flags_reales_mismos_tests"],
                 c["tests_reales"], c["ok"]))
    if cruce["estado"] == "PASS" and suma_ok and ctrl_ok and ginfo["mapeo_biyectivo"]:
        ver = "PASS"
    elif cruce["estado"] == "NO_MEDIDO" and suma_ok and ctrl_ok and ginfo["mapeo_biyectivo"]:
        ver = "INCOMPLETO"
    else:
        ver = "FAIL"
    resultado["veredicto"] = {"medicion": ver, "suma_d1_ok": suma_ok, "control_ok": ctrl_ok,
                              "cruce_tabla7": cruce["estado"]}
    resultado["segundos"] = time.time() - t0
    salida = os.path.join(args.out, "output_control_by_class.json")
    with open(salida, "w") as f:
        json.dump(a_py(resultado), f, indent=1, ensure_ascii=False)
        f.write("\n")
    print("JSON %s md5=%s" % (salida, md5_archivo(salida)))
    print("VEREDICTO_MEDICION %s" % ver)
    print("FIN_SALIDAS segundos=%.1f" % (time.time() - t0))
    return 0 if ver in ("PASS", "INCOMPLETO") else 1


if __name__ == "__main__":
    raise SystemExit(main())
