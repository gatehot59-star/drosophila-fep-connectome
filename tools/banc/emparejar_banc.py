#!/usr/bin/env python3
"""BANC contra FlyWire para el banco de la mosca (respuesta 2026-10-14-002). Mide; no decide ninguna hipotesis.

Preguntas (las del paso 2 de la 2026-10-13-018):
  1. Cuantas de nuestras 564 entradas sintonizadas, de las 6 descendentes y de las 33.489 neuronas de R2 tienen
     pareja en BANC (materializacion 888).
  2. Cuantas aristas de R2 se pueden evaluar en BANC (las dos puntas con pareja unica) y cuantas estan tambien en
     BANC, segun la fuerza de la conexion en FlyWire; y si las del nucleo de Schlegel (tools/nucleo/nucleo_mosca.py:
     10 sinapsis o mas, o mas del 1 % de la entrada de la neurona post) se conservan mas que el resto.
Pareja: la columna fafb_match de banc_888_meta.feather (el ID de FlyWire 783 que el equipo de BANC emparejo con cada
neurona); como segunda via, fafb_nblast_match (por NBLAST). La neurona de BANC se identifica por root_888, que es el
ID que usa banc_888_edgelist_simple_v3.feather (root_id es el ID vivo y no siempre coincide). Solo cuentan las parejas unicas (un ID de FlyWire con
una sola neurona de BANC y al reves); las ambiguas se cuentan aparte y no entran en las aristas.
Insumos con md5 fijo: los de FlyWire del banco (connectivity.parquet 3d802fd5, annotations.tsv 719904ab) y los de BANC
del bucket publico gs://lee-lab_brain-and-nerve-cord-fly-connectome/compiled_data/banc_888/ (banc_888_meta.feather
8c2b93a6, banc_888_edgelist_simple_v3.feather 08542b07; el bucket da el md5 en x-goog-hash).
Uso: python3 tools/banc/emparejar_banc.py --conn ... --annot ... --banc_meta ... --banc_aristas ... --out carpeta
Salida: 0 completo; 2 insumos distintos del pin.
"""
import argparse
import json
import os
import sys
import time

import numpy as np
import pandas as pd
import pyarrow as pa
import pyarrow.compute as pc
import pyarrow.feather as pf

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(AQUI, "..", "nucleo"))
import nucleo_mosca as nm  # noqa: E402

f2, tm, base = nm.f2, nm.tm, nm.base
PIN_BANC = {"meta": "8c2b93a608c7163ec9d94d68e0756ff4", "aristas": "08542b0771db7418ed474be60dc9886c"}
COLS = ["root_888", "fafb_match", "fafb_nblast_match", "cell_type", "side", "super_class"]
TRAMOS = ((1, 4), (5, 9), (10, 19), (20, 10 ** 9))


def pr(s):
    print(s, flush=True)


def ids_validos(s):
    s = s.astype("string").fillna("").str.strip()
    ok = s.str.fullmatch(r"[0-9]{15,20}").fillna(False).to_numpy(dtype=bool)
    return s, ok


def parejas(fw, banc):
    """Parejas 1 a 1 entre IDs de FlyWire y de BANC; devuelve el dict y cuantas filas eran ambiguas."""
    d = pd.DataFrame({"fw": fw, "banc": banc}).drop_duplicates()
    cf, cb = d.fw.map(d.fw.value_counts()), d.banc.map(d.banc.value_counts())
    u = d[(cf == 1) & (cb == 1)]
    return dict(zip(u.fw.tolist(), u.banc.tolist())), int(((cf > 1) | (cb > 1)).sum())


def pct(a, b):
    return 100.0 * a / b if b else float("nan")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--conn", required=True)
    ap.add_argument("--annot", required=True)
    ap.add_argument("--banc_meta", required=True)
    ap.add_argument("--banc_aristas", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    t0 = time.time()
    pr("# md5 script = " + base.md5(os.path.abspath(__file__)) + " | md5 nucleo_mosca = " +
       base.md5(os.path.abspath(nm.__file__)))
    mc, ma, mm_, mb = base.md5(a.conn), base.md5(a.annot), base.md5(a.banc_meta), base.md5(a.banc_aristas)
    pr("# md5 conn = %s | annot = %s | banc_meta = %s | banc_aristas = %s" % (mc, ma, mm_, mb))
    if mc != base.MD5_CONN or ma != base.MD5_ANNOT or mm_ != PIN_BANC["meta"] or mb != PIN_BANC["aristas"]:
        pr("ABORTA: insumos distintos del pin")
        pr("EXIT_BANC=2")
        return 2
    S, mnuc, info = nm.sujeto_nucleo(a.conn, a.annot)
    ids = np.array(S["ids"], dtype=np.int64)
    tipos, lados = S["tipos"], S["lados"]
    n, n_ent = len(ids), S["n_ent"]
    p, q, w = S["aristas"]
    pr("FLYWIRE R2 neuronas=%d entradas=%d aristas=%d | nucleo de Schlegel aristas=%d (%.2f %%)" % (
        n, n_ent, len(w), info["aristas"], pct(info["aristas"], len(w))))
    meta = pf.read_table(a.banc_meta, columns=COLS).to_pandas()
    rs, rok = ids_validos(meta.root_888)
    pr("BANC meta filas=%d root_888_validos=%d (los IDs de la materializacion 888, los de la lista de aristas v3)" % (
        len(meta), int(rok.sum())))
    root = pd.to_numeric(rs.where(rok, "0")).to_numpy(dtype=np.int64)
    ctype = meta.cell_type.astype("string").fillna("").to_numpy()
    via = {}
    for col in ("fafb_match", "fafb_nblast_match"):
        s, ok = ids_validos(meta[col])
        otros = int(((s.str.len() > 0) & ~pd.Series(ok, index=s.index)).sum())
        fw = pd.to_numeric(s[ok]).to_numpy(dtype=np.int64)
        mp, amb = parejas(fw, root[ok])
        via[col] = mp
        pr("PAREJAS via=%s filas_con_ID=%d otros_formatos=%d unicas=%d ambiguas=%d" % (col, int(ok.sum()), otros,
                                                                                    len(mp), amb))
    ex, nb = via["fafb_match"], via["fafb_nblast_match"]
    tipo_banc = dict(zip(root.tolist(), ctype.tolist()))
    res = dict(pin=dict(conn=mc, annot=ma, banc_meta=mm_, banc_aristas=mb), nucleo=info, dn=[], entradas={},
               parejas={k: len(v) for k, v in via.items()})
    for i in range(n - 6, n):
        r = int(ids[i])
        e, b = ex.get(r), nb.get(r)
        res["dn"].append(dict(root_id=r, tipo=tipos[i], lado=lados[i], banc_fafb_match=e, banc_nblast=b,
                              tipo_banc=tipo_banc.get(e if e is not None else b, "")))
        pr("DN root=%d tipo=%s lado=%s pareja_fafb_match=%s pareja_nblast=%s tipo_en_BANC=%s" % (
            r, tipos[i], lados[i], e, b, tipo_banc.get(e if e is not None else b, "")))
    for t in tm.TIPOS:
        for ld in ("L", "R"):
            ix = [i for i in range(n_ent) if tipos[i] == t and lados[i] == ld]
            ce = sum(1 for i in ix if int(ids[i]) in ex)
            cn = sum(1 for i in ix if int(ids[i]) in nb)
            cu = sum(1 for i in ix if int(ids[i]) in ex or int(ids[i]) in nb)
            res["entradas"]["%s_%s" % (t, ld)] = dict(total=len(ix), fafb_match=ce, nblast=cn, alguna=cu)
            pr("ENTRADAS tipo=%s lado=%s total=%d con_pareja_fafb_match=%d nblast=%d alguna=%d" % (t, ld, len(ix), ce,
                                                                                               cn, cu))
    te = sum(v["total"] for v in res["entradas"].values())
    ee = sum(v["fafb_match"] for v in res["entradas"].values())
    ea = sum(v["alguna"] for v in res["entradas"].values())
    r2e = int(sum(1 for r in ids.tolist() if r in ex))
    r2a = int(sum(1 for r in ids.tolist() if r in ex or r in nb))
    pr("RESUMEN entradas con pareja fafb_match=%d/%d (%.1f %%) alguna=%d/%d (%.1f %%) | DN con pareja=%d/6 | neuronas "
       "de R2 con pareja fafb_match=%d/%d (%.1f %%) alguna=%d (%.1f %%)" % (
           ee, te, pct(ee, te), ea, te, pct(ea, te), sum(1 for d in res["dn"] if d["banc_fafb_match"] is not None),
           r2e, n, pct(r2e, n), r2a, pct(r2a, n)))
    res.update(entradas_total=te, entradas_fafb_match=ee, entradas_alguna=ea, r2_fafb_match=r2e, r2_alguna=r2a)
    # aristas: solo pareja unica por fafb_match en las dos puntas; se indexa por posicion (un ID de 18 cifras no entra
    # exacto en float64)
    vals = np.array(sorted(set(ex[r] for r in ids.tolist() if r in ex)), dtype=np.int64)
    pos = {int(b): i for i, b in enumerate(vals.tolist())}
    fw2i = {r: pos[ex[r]] for r in ids.tolist() if r in ex}
    ipre = pd.Series(ids[p]).map(fw2i).to_numpy(dtype=np.float64)
    ipost = pd.Series(ids[q]).map(fw2i).to_numpy(dtype=np.float64)
    ev = ~np.isnan(ipre) & ~np.isnan(ipost)
    t = pf.read_table(a.banc_aristas, columns=["pre", "post", "count"])
    bp = pc.cast(t["pre"], pa.int64()).to_numpy()
    bq = pc.cast(t["post"], pa.int64()).to_numpy()
    bc = t["count"].to_numpy()
    nb_ar = len(bp)
    del t
    sel = np.isin(bp, vals) & np.isin(bq, vals)
    K = np.int64(len(vals))
    kb = np.searchsorted(vals, bp[sel]).astype(np.int64) * K + np.searchsorted(vals, bq[sel]).astype(np.int64)
    kb5 = kb[bc[sel] >= 5]
    del bp, bq, bc
    kf = ipre[ev].astype(np.int64) * K + ipost[ev].astype(np.int64)
    hay1, hay5 = np.isin(kf, kb), np.isin(kf, kb5)
    sin = np.abs(w)[ev]
    nuc = mnuc[ev]
    pr("ARISTAS BANC total=%d entre neuronas de R2 con pareja=%d" % (nb_ar, int(sel.sum())))
    pr("ARISTAS R2 total=%d evaluables=%d (%.1f %%) | en BANC con 1 sinapsis o mas=%d (%.1f %%) | con 5 o mas=%d "
       "(%.1f %%)" % (len(w), int(ev.sum()), pct(int(ev.sum()), len(w)), int(hay1.sum()), pct(int(hay1.sum()), len(kf)),
                      int(hay5.sum()), pct(int(hay5.sum()), len(kf))))
    res["aristas"] = dict(total=int(len(w)), evaluables=int(ev.sum()), en_banc_1=int(hay1.sum()), en_banc_5=int(hay5.sum()),
                          banc_total=int(nb_ar), banc_entre_parejas=int(sel.sum()), tramos=[], nucleo=None, resto=None)
    for lo, hi in TRAMOS:
        mm = (sin >= lo) & (sin <= hi)
        res["aristas"]["tramos"].append(dict(desde=lo, hasta=hi, evaluables=int(mm.sum()), en_banc_1=int(hay1[mm].sum()),
                                             en_banc_5=int(hay5[mm].sum())))
        pr("TRAMO sinapsis_FlyWire=%d..%s evaluables=%d en_BANC_1=%.1f %% en_BANC_5=%.1f %%" % (
            lo, "inf" if hi >= 10 ** 9 else hi, int(mm.sum()), pct(int(hay1[mm].sum()), int(mm.sum())),
            pct(int(hay5[mm].sum()), int(mm.sum()))))
    for nombre, mm in (("nucleo", nuc), ("resto", ~nuc)):
        res["aristas"][nombre] = dict(evaluables=int(mm.sum()), en_banc_1=int(hay1[mm].sum()), en_banc_5=int(hay5[mm].sum()))
        pr("SCHLEGEL %s evaluables=%d en_BANC_1=%d (%.1f %%) en_BANC_5=%d (%.1f %%)" % (
            nombre, int(mm.sum()), int(hay1[mm].sum()), pct(int(hay1[mm].sum()), int(mm.sum())), int(hay5[mm].sum()),
            pct(int(hay5[mm].sum()), int(mm.sum()))))
    ruta = os.path.join(a.out, "emparejar_banc.json")
    with open(ruta, "w") as f:
        json.dump(res, f, indent=1, sort_keys=True)
    pr("escrito %s md5=%s" % (os.path.basename(ruta), base.md5(ruta)))
    pr("# duracion_s=%.1f" % (time.time() - t0))
    pr("EXIT_BANC=0")
    return 0


if __name__ == "__main__":
    sys.exit(main())
