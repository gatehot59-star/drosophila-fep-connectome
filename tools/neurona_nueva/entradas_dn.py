#!/usr/bin/env python3
"""Entradas de DNp01, DNp06, DNp07 y DNp10 en FlyWire v783 (respuesta 2026-10-12-014).
Dos preguntas que pueden dar rojo:
 Q1. De donde salen las 67 sinapsis de diferencia en la entrada total de DNp01 entre la exploracion de la 003
     (9.407) y la 011 (9.474). Se recalcula la entrada total con filtros candidatos y se marca cual reproduce los
     totales de la 003 (DNp01 9.407, DNp07 8.715, DNp10 9.480). Si ninguno coincide, queda sin explicar.
 Q2. Que tipos le hablan a cada una (los 10 primeros por sinapsis, con su neurotransmisor mas frecuente),
     la fraccion inhibitoria de su entrada (signo del pipeline: Excitatory x Connectivity <= 0) y cuanto
     reciben de LPLC3, LC13 y LPLC1 (no medidos en la 013).
Solo lectura de los datos pinneados. Salida: 0 completo; 2 datos distintos del pin.
"""
import hashlib, os, platform, sys, time
import numpy as np
import pandas as pd
import pyarrow.parquet as pq

CONN = "/workspace/connectivity.parquet"
ANNOT = "/workspace/annotations.tsv"
MD5_CONN = "3d802fd542b5d18570ba1ba0bb0abed9"
MD5_ANNOT = "719904abad876c68ace1b5690c9b9b63"
DNS = ("DNp01", "DNp06", "DNp07", "DNp10")
TOTAL_003 = {"DNp01": 9407, "DNp07": 8715, "DNp10": 9480}
EXTRA = ("LPLC3", "LC13", "LPLC1", "LPLC2", "LC4", "LPLC4")
TOP = 10


def md5(p):
    h = hashlib.md5()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def marca(dn, s):
    if dn not in TOTAL_003:
        return ""
    return " COINCIDE_003" if s == TOTAL_003[dn] else " difiere_003(%+d)" % (s - TOTAL_003[dn])


def main():
    t0 = time.time()
    print("# maquina: %s | %s | numpy %s | pandas %s" % (platform.node(), platform.platform(), np.__version__, pd.__version__))
    print("# md5 script = " + md5(os.path.abspath(__file__)))
    print("# fecha: " + time.strftime("%Y-%m-%d %H:%M:%S %z"))
    mc, ma = md5(CONN), md5(ANNOT)
    print("# md5 conn = %s | md5 annot = %s" % (mc, ma))
    if mc != MD5_CONN or ma != MD5_ANNOT:
        print("ABORTA: datos distintos del pin")
        print("EXIT_RUN=2")
        return 2
    a = pd.read_csv(ANNOT, sep="\t", dtype=str, usecols=["root_id", "cell_type", "side", "top_nt"])
    a["root_id"] = a.root_id.astype(np.int64)
    print("ANNOT filas=%d root_id_unicos=%d cell_type_nulos=%d top_nt_nulos=%d" % (
        len(a), a.root_id.nunique(), int(a.cell_type.isna().sum()), int(a.top_nt.isna().sum())))
    for t in EXTRA:
        print("CUENTA tipo=%s por_lado=%s" % (t, a[a.cell_type == t].side.value_counts().to_dict()))
    tipo = dict(zip(a.root_id, a.cell_type))
    lado = dict(zip(a.root_id, a.side))
    nt = dict(zip(a.root_id, a.top_nt))
    anot = set(a.root_id.tolist())
    dn_ids = a.root_id[a.cell_type.isin(list(DNS))].tolist()
    c = pq.read_table(CONN, columns=["Presynaptic_ID", "Postsynaptic_ID", "Connectivity", "Excitatory",
                                     "Excitatory x Connectivity"],
                      filters=[("Postsynaptic_ID", "in", dn_ids)]).to_pandas()
    print("EXCITATORY valores=%s" % sorted(pd.unique(c.Excitatory).tolist()))
    c["post_t"] = c.Postsynaptic_ID.map(tipo)
    c["pre_t"] = c.Presynaptic_ID.map(tipo)
    c["pre_nt"] = c.Presynaptic_ID.map(nt)
    c["pre_lado"] = c.Presynaptic_ID.map(lado)
    c["pre_anot"] = c.Presynaptic_ID.isin(anot)
    c["inh"] = c["Excitatory x Connectivity"] <= 0
    for dn in DNS:
        d = c[c.post_t == dn]
        filtros = [
            ("todas", d),
            ("pre_en_anotaciones", d[d.pre_anot]),
            ("pre_con_cell_type", d[d.pre_t.notna()]),
            ("pre_con_top_nt", d[d.pre_nt.notna()]),
            ("pre_con_lado_left_right", d[d.pre_lado.isin(["left", "right"])]),
            ("sin_autapsis", d[d.Presynaptic_ID != d.Postsynaptic_ID]),
            ("sin_pre_del_mismo_tipo", d[d.pre_t != dn]),
        ]
        for nombre, f in filtros:
            s = int(f.Connectivity.sum())
            print("Q1 dn=%s filtro=%s sinapsis=%d aristas=%d%s" % (dn, nombre, s, len(f), marca(dn, s)))
        s = int(d.groupby("pre_t").Connectivity.sum().sum())
        print("Q1 dn=%s filtro=suma_de_groupby_por_tipo_con_dropna sinapsis=%d%s" % (dn, s, marca(dn, s)))
        st = d[d.pre_t.isna()]
        print("Q1 dn=%s pre_sin_cell_type sinapsis=%d neuronas=%d" % (dn, int(st.Connectivity.sum()), st.Presynaptic_ID.nunique()))
        tot = float(d.Connectivity.sum())
        print("Q2 dn=%s entrada_total=%d presinapticas=%d inhibitoria=%.1f%%" % (
            dn, int(tot), d.Presynaptic_ID.nunique(), 100.0 * d.Connectivity[d.inh].sum() / tot))
        top = d.assign(pre_t=d.pre_t.fillna("SIN_TIPO")).groupby("pre_t").agg(
            sinapsis=("Connectivity", "sum"), neuronas=("Presynaptic_ID", "nunique")).sort_values("sinapsis", ascending=False)
        for k, (t, r) in enumerate(top.head(TOP).iterrows()):
            nts = d[d.pre_t == t].pre_nt.value_counts()
            ntm = nts.index[0] if len(nts) else "NA"
            print("Q2 dn=%s top%d tipo=%s sinapsis=%d (%.1f%%) neuronas=%d nt=%s" % (
                dn, k + 1, t, int(r.sinapsis), 100.0 * r.sinapsis / tot, int(r.neuronas), ntm))
        for t in ("LPLC3", "LC13", "LPLC1"):
            e = d[d.pre_t == t]
            print("Q2 dn=%s de=%s sinapsis=%d (%.1f%%) neuronas=%d" % (
                dn, t, int(e.Connectivity.sum()), 100.0 * e.Connectivity.sum() / tot, e.Presynaptic_ID.nunique()))
    print("# duracion_s=%.1f" % (time.time() - t0))
    print("EXIT_RUN=0")
    return 0


if __name__ == "__main__":
    sys.exit(main())
