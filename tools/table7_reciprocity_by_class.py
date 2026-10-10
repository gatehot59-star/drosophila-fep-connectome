#!/usr/bin/env python3
"""Tabla 7 reconstruida: reciprocidad por clase funcional (super_class) del conectoma FlyWire v783.

El script original de marzo-2026 no esta en ningun archivo conocido. Lo que sobrevive es su SALIDA:
el bloque "L3: ANALISIS DE RECIPROCIDAD" que Abraham pego en el chat de Gemini e26fcf246e9f0dad
(turno G-T13, paginas 10-11 del PDF "Analisis de Conectoma de Drosophila FEP"). Esta reconstruccion
reimplementa la definicion desde cero y compara contra esa salida, numero por numero.

Definicion (paper v1.0 seccion 3.5 + Methods: "Static analyses use W unnormalized"; sin umbral):
  - arista = par ordenado (pre, post) presente en el parquet de Eon (Connectivity_783), sin umbral.
  - clase de cada neurona = super_class de la anotacion de FlyWire, mapeada por root_id.
  - para clases (A, B): E_AB = aristas i->j con i en A y j en B; R_AB = las de E_AB cuyo reverso
    j->i tambien existe; reciprocidad = R_AB / E_AB. Intra-clase: A = B.
  - global: aristas con reciproca / aristas. Los autolazos (i->i) no cuentan como reciprocos.

Instrumento que puede dar ROJO: la comparacion es por igualdad EXACTA de enteros (aristas y
reciprocas) y del porcentaje formateado igual que en marzo. Incluye un control negativo con
etiquetas permutadas que DEBE dar rojo, y la variante con umbral >= 5 sinapsis (criterio del campo),
que el erratum declara no calculada para la Tabla 7.
"""
import argparse
import hashlib
import json
import os
import platform
import sys
import time
from datetime import datetime, timedelta, timezone
from decimal import ROUND_HALF_UP, Decimal

import numpy as np
import pandas as pd
import pyarrow
import pyarrow.parquet as pq

MD5_PARQUET_PIN = "3d802fd542b5d18570ba1ba0bb0abed9"
MD5_ANNOT_PIN = "719904abad876c68ace1b5690c9b9b63"
ANNOT_SHA_PIN = "17fc57722002e1a7d38cdd0c89ac382bf92718da"

# Salida L3 de marzo-2026, verbatim (G-T13). Pct impreso con 2 decimales.
REF_GLOBAL = (15091983, 4014518, "26.60")
REF_INTER = [
    ("sensory", "descending", 24327, 2104, "8.65"),
    ("sensory", "motor", 1178, 42, "3.57"),
    ("sensory", "central", 159360, 38554, "24.19"),
    ("optic", "descending", 3069, 285, "9.29"),
    ("optic", "motor", 6, 0, "0.00"),
    ("optic", "central", 5345, 269, "5.03"),
]
REF_INTRA = [
    ("ascending", 14627, "21.43"),
    ("central", 4586059, "26.00"),
    ("descending", 38742, "22.40"),
    ("motor", 509, "41.26"),
    ("optic", 6201151, "31.98"),
    ("sensory", 34111, "30.66"),
    ("sensory_ascending", 1315, "32.09"),
    ("visual_centrifugal", 7490, "36.90"),
    ("visual_projection", 346021, "29.73"),
]
# Tabla 7 publicada (v1.0, zenodo.19136948), 1 decimal.
REF_TABLE7 = [
    ("motor", "motor", "41.3"),
    ("visual_centrifugal", "visual_centrifugal", "36.9"),
    ("optic", "optic", "32.0"),
    ("sensory", "sensory", "30.7"),
    ("sensory", "central", "24.2"),
    ("sensory", "descending", "8.7"),
    ("sensory", "motor", "3.6"),
    ("optic", "motor", "0.0"),
]
UNMAPPED = "sin_anotacion"
T0 = time.time()


def log(msg):
    print("[" + format(time.time() - T0, "7.1f") + "s] " + str(msg), flush=True)


def md5_file(path):
    h = hashlib.md5()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def pct(r, e, nd):
    return format(100.0 * r / e, "." + str(nd) + "f") if e else "nan"


def read_column(path, name):
    return pq.read_table(path, columns=[name]).column(name).to_numpy()


def load_edges(path):
    pre = read_column(path, "Presynaptic_Index").astype(np.int32)
    post = read_column(path, "Postsynaptic_Index").astype(np.int32)
    syn = read_column(path, "Connectivity").astype(np.int32)
    preid = read_column(path, "Presynaptic_ID").astype(np.int64)
    postid = read_column(path, "Postsynaptic_ID").astype(np.int64)
    return pre, post, syn, preid, postid


def build_mapping(pre, post, preid, postid):
    """root_id -> indice segun los pares (ID, Index) del propio parquet; verifica biyeccion."""
    allid = np.concatenate([preid, postid])
    allix = np.concatenate([pre.astype(np.int64), post.astype(np.int64)])
    order = np.lexsort((allix, allid))
    allid, allix = allid[order], allix[order]
    pair_first = np.ones(allid.shape[0], dtype=bool)
    pair_first[1:] = (allid[1:] != allid[:-1]) | (allix[1:] != allix[:-1])
    pid, pix = allid[pair_first], allix[pair_first]
    uid, counts = np.unique(pid, return_counts=True)
    ids_with_many_indices = int((counts > 1).sum())
    first = np.searchsorted(pid, uid)
    uix = pix[first]
    indices_with_many_ids = int(uix.shape[0] - np.unique(uix).shape[0])
    rank_equal = bool(np.array_equal(uix, np.arange(uix.shape[0])))
    return uid, uix, {"ids": int(uid.shape[0]), "ids_con_varios_indices": ids_with_many_indices,
                      "indices_con_varios_ids": indices_with_many_ids, "indice_eon_igual_rank_ordenado": rank_equal}


def load_classes(annot_path, uid, uix, n):
    ann = pd.read_csv(annot_path, sep="\t", usecols=["root_id", "super_class"], dtype={"root_id": "int64"})
    rid = ann["root_id"].to_numpy(dtype=np.int64)
    sc = ann["super_class"].astype(object).where(ann["super_class"].notna(), "nan").astype(str).to_numpy()
    pos = np.minimum(np.searchsorted(uid, rid), uid.shape[0] - 1)
    hit = uid[pos] == rid
    names = sorted(set(sc[hit].tolist())) + [UNMAPPED]
    code = {c: i for i, c in enumerate(names)}
    cls = np.full(n, code[UNMAPPED], dtype=np.int16)
    target = uix[pos[hit]]
    cls[target] = np.array([code[c] for c in sc[hit]], dtype=np.int16)
    dup_rows = int(hit.sum() - np.unique(target).shape[0])
    info = {"filas_tsv": int(ann.shape[0]), "filas_mapeadas": int(hit.sum()), "filas_mapeadas_duplicadas": dup_rows,
            "neuronas_sin_anotacion": int((cls == code[UNMAPPED]).sum())}
    return names, cls, info


def reciprocal_mask(pre, post, n):
    """True en la arista i->j si j->i existe (i != j). Devuelve tambien unicas y autolazos."""
    nn = np.int64(n)
    keys = pre.astype(np.int64) * nn + post.astype(np.int64)
    ks = np.sort(keys)
    n_unique = int(ks.shape[0] - int((ks[1:] == ks[:-1]).sum()))
    del keys
    rk = post.astype(np.int64) * nn + pre.astype(np.int64)
    pos = np.searchsorted(ks, rk)
    np.minimum(pos, ks.shape[0] - 1, out=pos)
    has = ks[pos] == rk
    del ks, rk, pos
    selfloop = pre == post
    n_self = int(selfloop.sum())
    has &= ~selfloop
    return has, n_unique, n_self


def pair_tables(cls, pre, post, has, k):
    cell = cls[pre].astype(np.int64) * k + cls[post].astype(np.int64)
    e = np.bincount(cell, minlength=k * k).reshape(k, k)
    r = np.bincount(cell[has], minlength=k * k).reshape(k, k)
    return e, r


def compare(names, e, r, glob_e, glob_r):
    ix = {c: i for i, c in enumerate(names)}
    rows = []
    ok_glob = (glob_e == REF_GLOBAL[0]) and (glob_r == REF_GLOBAL[1]) and (pct(glob_r, glob_e, 2) == REF_GLOBAL[2])
    rows.append({"fila": "global", "ref": list(REF_GLOBAL), "obs": [glob_e, glob_r, pct(glob_r, glob_e, 2)], "exacta": ok_glob})
    for a, b, re_, rr, rp in REF_INTER:
        if a in ix and b in ix:
            oe, orr = int(e[ix[a], ix[b]]), int(r[ix[a], ix[b]])
            obs = [oe, orr, pct(orr, oe, 2)]
            ok = oe == re_ and orr == rr and obs[2] == rp
        else:
            obs, ok = None, False
        rows.append({"fila": a + "->" + b, "ref": [re_, rr, rp], "obs": obs, "exacta": ok})
    for a, re_, rp in REF_INTRA:
        if a in ix:
            oe, orr = int(e[ix[a], ix[a]]), int(r[ix[a], ix[a]])
            obs = [oe, orr, pct(orr, oe, 2)]
            ok = oe == re_ and obs[2] == rp
        else:
            obs, ok = None, False
        rows.append({"fila": "intra " + a, "ref": [re_, None, rp], "obs": obs, "exacta": ok})
    t7 = []
    for a, b, rp in REF_TABLE7:
        if a in ix and b in ix:
            ee, rr = int(e[ix[a], ix[b]]), int(r[ix[a], ix[b]])
            obs1 = pct(rr, ee, 1)
            obs2 = pct(rr, ee, 2)
            dr = str(Decimal(obs2).quantize(Decimal("0.1"), rounding=ROUND_HALF_UP)) if obs2 != "nan" else "nan"
        else:
            obs1, obs2, dr = None, None, None
        exacto, doble = obs1 == rp, dr == rp
        t7.append({"fila": a + "->" + b, "publicado": rp, "obs_1d": obs1, "obs_2d": obs2, "obs_doble_redondeo": dr,
                   "coincide": exacto or doble, "solo_por_doble_redondeo": (not exacto) and doble})
    return rows, t7


def print_rows(title, rows, t7):
    log(title)
    for x in rows:
        log("  " + ("EXACTA " if x["exacta"] else "DIFIERE") + "  " + x["fila"].ljust(30) + " ref=" + str(x["ref"]) + "  obs=" + str(x["obs"]))
    for x in t7:
        nota = "  <- solo por doble redondeo (" + str(x["obs_2d"]) + " -> " + str(x["obs_doble_redondeo"]) + "; exacto a 1 decimal: " + str(x["obs_1d"]) + ")" if x["solo_por_doble_redondeo"] else ""
        log("  " + ("COINCIDE" if x["coincide"] else "DIFIERE ") + "  T7 " + x["fila"].ljust(40) + " publicado=" + x["publicado"] + "%  obs_1d=" + str(x["obs_1d"]) + "%  obs_2d=" + str(x["obs_2d"]) + "%" + nota)
    n_ok = sum(1 for x in rows if x["exacta"])
    n_t7 = sum(1 for x in t7 if x["coincide"])
    return n_ok, n_t7


def run(parquet, annot, out_dir, seed):
    os.makedirs(out_dir, exist_ok=True)
    res = {"schema": "table7-reciprocity-by-class/v1", "inputs": {}, "entorno": {}}
    res["entorno"] = {"python": sys.version.split()[0], "numpy": np.__version__, "pandas": pd.__version__,
                      "pyarrow": pyarrow.__version__, "host": platform.node(),
                      "utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
                      "art": datetime.now(timezone(timedelta(hours=-3))).isoformat(timespec="seconds")}
    mp, ma = md5_file(parquet), md5_file(annot)
    res["inputs"] = {"parquet": parquet, "parquet_bytes": os.path.getsize(parquet), "parquet_md5": mp,
                     "parquet_md5_pin_ok": mp == MD5_PARQUET_PIN, "annotations": annot,
                     "annotations_bytes": os.path.getsize(annot), "annotations_md5": ma,
                     "annotations_md5_pin_ok": ma == MD5_ANNOT_PIN, "annotations_sha_pin": ANNOT_SHA_PIN}
    log("md5 parquet     = " + mp + ("  OK pin" if mp == MD5_PARQUET_PIN else "  DISTINTO del pin"))
    log("md5 anotaciones = " + ma + ("  OK pin" if ma == MD5_ANNOT_PIN else "  DISTINTO del pin"))

    pre, post, syn, preid, postid = load_edges(parquet)
    n = int(max(pre.max(), post.max())) + 1
    log("N=" + format(n, ",") + "  filas=" + format(pre.shape[0], ",") + "  sinapsis=" + format(int(syn.astype(np.int64).sum()), ","))
    uid, uix, minfo = build_mapping(pre, post, preid, postid)
    del preid, postid
    log("mapeo root_id->indice: " + json.dumps(minfo))

    names, cls, cinfo = load_classes(annot, uid, uix, n)
    k = len(names)
    counts = np.bincount(cls, minlength=k)
    res["mapeo"] = minfo
    res["anotacion"] = cinfo
    res["clases"] = {names[i]: int(counts[i]) for i in range(k)}
    log("anotacion: " + json.dumps(cinfo))
    log("neuronas por super_class en el grafo: " + json.dumps(res["clases"]))

    has, n_unique, n_self = reciprocal_mask(pre, post, n)
    glob_e, glob_r = int(pre.shape[0]), int(has.sum())
    dens_num, dens_den = glob_e, n * (n - 1)
    res["grafo"] = {"N": n, "aristas": glob_e, "aristas_unicas": n_unique, "autolazos": n_self,
                    "aristas_con_reciproca": glob_r, "reciprocidad_pct": pct(glob_r, glob_e, 4),
                    "densidad_exacta": dens_num / dens_den, "cociente_vs_densidad_solo_continuidad": (glob_r / glob_e) / (dens_num / dens_den)}
    log("global: aristas=" + format(glob_e, ",") + "  unicas=" + format(n_unique, ",") + "  autolazos=" + str(n_self) + "  con_reciproca=" + format(glob_r, ",") + "  (" + pct(glob_r, glob_e, 2) + "%)")
    log("densidad exacta = " + format(dens_num / dens_den, ".9f") + "  (marzo imprimio 0.007395: overflow int32 ya documentado en el erratum)")

    e, r = pair_tables(cls, pre, post, has, k)
    rows, t7 = compare(names, e, r, glob_e, glob_r)
    n_ok, n_t7 = print_rows("=== SIN UMBRAL contra la salida L3 de marzo (16 filas) y la Tabla 7 publicada (8 filas) ===", rows, t7)
    res["sin_umbral"] = {"comparacion_L3": rows, "comparacion_tabla7": t7, "filas_L3_exactas": n_ok, "filas_tabla7_coinciden": n_t7,
                         "matriz_aristas": e.tolist(), "matriz_reciprocas": r.tolist(), "clases_orden": names}
    if "endocrine" in names:
        ie = names.index("endocrine")
        log("intra endocrine (no figura en L3): aristas=" + format(int(e[ie, ie]), ",") + "  pct=" + pct(int(r[ie, ie]), int(e[ie, ie]), 2))
        res["sin_umbral"]["intra_endocrine"] = [int(e[ie, ie]), int(r[ie, ie])]

    rng = np.random.default_rng(seed)
    cls_perm = cls.copy()
    rng.shuffle(cls_perm)
    ep, rp_ = pair_tables(cls_perm, pre, post, has, k)
    rows_p, t7_p = compare(names, ep, rp_, glob_e, glob_r)
    n_ok_p, n_t7_p = print_rows("=== CONTROL NEGATIVO: super_class permutada (seed=" + str(seed) + "), tiene que DIFERIR ===", rows_p, t7_p)
    res["control_negativo"] = {"seed": seed, "filas_L3_exactas": n_ok_p, "filas_tabla7_coinciden": n_t7_p}

    m5 = syn >= 5
    pre5, post5 = pre[m5], post[m5]
    has5, n_unique5, n_self5 = reciprocal_mask(pre5, post5, n)
    e5, r5 = pair_tables(cls, pre5, post5, has5, k)
    g5e, g5r = int(pre5.shape[0]), int(has5.sum())
    log("=== UMBRAL >= 5 sinapsis (criterio Lin 2024 / Dorkenwald 2024) ===")
    log("global >=5: aristas=" + format(g5e, ",") + "  con_reciproca=" + format(g5r, ",") + "  (" + pct(g5r, g5e, 2) + "%)  [erratum item 5: 2,700,513 y 13.98%]")
    thr_rows = []
    for a, b, _ in REF_TABLE7:
        if a not in names or b not in names:
            thr_rows.append({"fila": a + "->" + b, "aristas": None})
            continue
        ia, ib = names.index(a), names.index(b)
        thr_rows.append({"fila": a + "->" + b, "aristas": int(e5[ia, ib]), "reciprocas": int(r5[ia, ib]), "pct_1d": pct(int(r5[ia, ib]), int(e5[ia, ib]), 1),
                         "sin_umbral_pct_1d": pct(int(r[ia, ib]), int(e[ia, ib]), 1), "pct_2d": pct(int(r5[ia, ib]), int(e5[ia, ib]), 2)})
        log("  T7 >=5  " + (a + "->" + b).ljust(40) + " aristas=" + format(int(e5[ia, ib]), ",").rjust(10) + "  reciprocas=" + format(int(r5[ia, ib]), ",").rjust(9) + "  pct=" + thr_rows[-1]["pct_1d"] + "%  (sin umbral " + thr_rows[-1]["sin_umbral_pct_1d"] + "%)")
    res["umbral_5"] = {"aristas": g5e, "aristas_unicas": n_unique5, "autolazos": n_self5, "aristas_con_reciproca": g5r,
                       "reciprocidad_pct": pct(g5r, g5e, 4), "tabla7": thr_rows, "matriz_aristas": e5.tolist(), "matriz_reciprocas": r5.tolist()}

    exacta = n_ok == len(rows)
    publicada = n_t7 == len(t7)
    dobles = [x["fila"] for x in t7 if x["solo_por_doble_redondeo"]]
    rojo = n_ok_p < len(rows_p) and n_t7_p < len(t7_p)
    res["veredicto"] = {"L3_exacta": exacta, "filas_L3_exactas": str(n_ok) + "/" + str(len(rows)),
                        "tabla7_publicada": publicada, "filas_tabla7": str(n_t7) + "/" + str(len(t7)),
                        "tabla7_filas_solo_por_doble_redondeo": dobles,
                        "control_negativo_dio_rojo": rojo, "minutos": round((time.time() - T0) / 60.0, 2)}
    with open(os.path.join(out_dir, "table7_reciprocity_by_class.json"), "w") as f:
        json.dump(res, f, indent=1, sort_keys=True)
    log("VEREDICTO_L3_EXACTA=" + ("SI" if exacta else "NO") + " (" + str(n_ok) + "/" + str(len(rows)) + " filas exactas)")
    log("VEREDICTO_TABLA7_PUBLICADA=" + ("SI" if publicada else "NO") + " (" + str(n_t7) + "/" + str(len(t7)) + ")  solo_por_doble_redondeo=" + json.dumps(dobles))
    log("CONTROL_NEGATIVO_DIO_ROJO=" + ("SI" if rojo else "NO") + " (" + str(n_ok_p) + "/" + str(len(rows_p)) + " exactas, " + str(n_t7_p) + "/" + str(len(t7_p)) + " T7)")
    log("FIN_TABLA7")
    return res


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--parquet", default="/workspace/connectivity.parquet")
    ap.add_argument("--annotations", default="/workspace/annotations.tsv")
    ap.add_argument("--out", default="results/table7_reconstruida")
    ap.add_argument("--seed", type=int, default=20261010)
    a = ap.parse_args()
    run(a.parquet, a.annotations, a.out, a.seed)


if __name__ == "__main__":
    main()
