#!/usr/bin/env python3
"""Chequeo de la neurona DCMT contra los datos reales del pipeline (respuesta 2026-10-12-011).

No entrena nada. Cuatro preguntas, cada una puede dar rojo:
  Q1. Que signo le pone el parquet del pipeline a cada neurotransmisor (top_nt de las anotaciones).
  Q2. Cuantas neuronas presinapticas, aristas y sinapsis cambiarian de signo con el mapeo de la DCMT
      (ACh, Glu, DA y 5HT excitatorias; GABA y glicina inhibitorias; la octopamina no figura).
  Q3. Si los datos del pipeline traen con que asignar compartimentos dendriticos
      (columna de neuropilo o de coordenadas en el parquet).
  Q4. En el motivo de 28 neuronas de la 003 y la 005 (misma seleccion): aristas inhibitorias, y cuanta
      entrada inhibitoria reciben esas 4 descendentes en el cerebro entero (lo que el recorte dejo afuera).
Salida: 0 completo; 2 md5 de datos distinto del pin; 3 el motivo no reproduce el de la 003.
"""
import hashlib, os, platform, sys, time
import numpy as np
import pandas as pd
import pyarrow
import pyarrow.parquet as pq

CONN = "/workspace/connectivity.parquet"
ANNOT = "/workspace/annotations.tsv"
MD5_CONN = "3d802fd542b5d18570ba1ba0bb0abed9"
MD5_ANNOT = "719904abad876c68ace1b5690c9b9b63"
K = 4
NORM = {"acetylcholine": "ACh", "ach": "ACh", "glutamate": "Glu", "glut": "Glu", "glu": "Glu",
        "gaba": "GABA", "dopamine": "DA", "da": "DA", "serotonin": "5HT", "ser": "5HT", "5ht": "5HT",
        "octopamine": "OA", "oct": "OA", "oa": "OA", "glycine": "Gly", "gly": "Gly", "histamine": "HA"}
DCMT = {"ACh": 1, "Glu": 1, "DA": 1, "5HT": 1, "GABA": -1, "Gly": -1}
VIS = ("LC4", "LPLC2", "LPLC4")


def md5(p):
    h = hashlib.md5()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def seleccion_motivo(a, c):
    """Copia literal de la seleccion de construir_motivo (escape_aterrizaje_dbc3.py, md5 4d40477d...)."""
    sel = []
    for tipo, blanco in (("LC4", "DNp01"), ("LPLC2", "DNp01"), ("LPLC4", "DNp07")):
        bl = a.root_id[a.cell_type == blanco]
        for lado in ("left", "right"):
            v = a[(a.cell_type == tipo) & (a.side == lado)].copy()
            m = c.Presynaptic_ID.isin(v.root_id) & c.Postsynaptic_ID.isin(bl)
            s = c[m].groupby("Presynaptic_ID").Connectivity.sum()
            v["s"] = v.root_id.map(s).fillna(0)
            v = v.sort_values(["s", "root_id"], ascending=[False, True]).head(K)
            sel += [(int(r), tipo, lado, float(x)) for r, x in zip(v.root_id, v.s)]
    for tipo in ("DNp01", "DNp07"):
        for lado in ("left", "right"):
            r = a[(a.cell_type == tipo) & (a.side == lado)].root_id
            assert len(r) == 1, (tipo, lado, len(r))
            sel.append((int(r.iloc[0]), tipo, lado, 0.0))
    ids = [s[0] for s in sel]
    sub = c[c.Presynaptic_ID.isin(ids) & c.Postsynaptic_ID.isin(ids)]
    return sel, sub


def main():
    t0 = time.time()
    print("# maquina: %s | %s | Python %s | numpy %s | pandas %s | pyarrow %s" % (
        platform.node(), platform.platform(), platform.python_version(), np.__version__,
        pd.__version__, pyarrow.__version__))
    print("# md5 script = " + md5(os.path.abspath(__file__)))
    print("# fecha: " + time.strftime("%Y-%m-%d %H:%M:%S %z"))
    mc, ma = md5(CONN), md5(ANNOT)
    print("# md5 conn = %s | md5 annot = %s" % (mc, ma))
    if mc != MD5_CONN or ma != MD5_ANNOT:
        print("ABORTA: datos distintos del pin")
        print("EXIT_RUN=2")
        return 2

    # Q3: con que se podrian asignar compartimentos
    sch = pq.read_schema(CONN)
    cols_a = pd.read_csv(ANNOT, sep="\t", nrows=0).columns.tolist()
    print("Q3 PARQUET_COLUMNAS " + ",".join(sch.names))
    print("Q3 ANNOT_COLUMNAS " + ",".join(cols_a))
    esp = [x for x in sch.names if any(k in x.lower() for k in ("neuropil", "roi", "pos", "coord", "_x", "loc"))]
    print("Q3 COLUMNAS_ESPACIALES_EN_PARQUET " + (",".join(esp) if esp else "NINGUNA"))

    ntcol = next((x for x in ("top_nt", "known_nt", "nt_type", "nt") if x in cols_a), None)
    print("Q1 COLUMNA_NT " + str(ntcol))
    usar = ["root_id", "cell_type", "side"] + ([ntcol] if ntcol else [])
    a = pd.read_csv(ANNOT, sep="\t", dtype=str, usecols=usar)
    a["root_id"] = a.root_id.astype(np.int64)
    a["nt"] = a[ntcol].fillna("NA").str.lower().map(lambda s: NORM.get(s, s)) if ntcol else "SIN_NT"
    print("ANNOT filas=%d" % len(a))

    # Q1 y Q2: signo del pipeline por neurona presinaptica
    t = pq.read_table(CONN, columns=["Presynaptic_ID", "Excitatory", "Connectivity"])
    print("CONN filas=%d" % t.num_rows)
    g = t.group_by(["Presynaptic_ID", "Excitatory"]).aggregate(
        [("Connectivity", "sum"), ("Connectivity", "count")]).to_pandas()
    del t
    g = g.rename(columns={"Presynaptic_ID": "pre", "Excitatory": "exc",
                          "Connectivity_sum": "syn", "Connectivity_count": "edges"})
    nun = g.groupby("pre").exc.nunique()
    print("Q1 PRESINAPTICAS=%d con_signo_mixto=%d" % (len(nun), int((nun > 1).sum())))
    g = g.merge(a[["root_id", "nt"]], left_on="pre", right_on="root_id", how="left")
    g["nt"] = g.nt.fillna("SIN_ANOTACION")
    g["s"] = np.sign(g.exc.astype(float)).astype(int)
    tab = g.groupby(["nt", "s"]).agg(neuronas=("pre", "nunique"), aristas=("edges", "sum"),
                                       sinapsis=("syn", "sum")).reset_index()
    for r in tab.itertuples(index=False):
        print("Q1 NT=%s signo_pipeline=%+d neuronas=%d aristas=%d sinapsis=%d" % (
            r.nt, r.s, r.neuronas, r.aristas, r.sinapsis))
    g["dcmt"] = g.nt.map(DCMT)
    sin_clase = g.dcmt.isna()
    flip = (~sin_clase) & (g.s != g.dcmt)
    tn, te, ts = g.pre.nunique(), int(g.edges.sum()), int(g.syn.sum())
    fn, fe, fs = g.loc[flip, "pre"].nunique(), int(g.loc[flip, "edges"].sum()), int(g.loc[flip, "syn"].sum())
    print("Q2 DCMT_CAMBIA_SIGNO neuronas=%d/%d (%.2f%%) aristas=%d/%d (%.2f%%) sinapsis=%d/%d (%.2f%%)" % (
        fn, tn, 100.0 * fn / tn, fe, te, 100.0 * fe / te, fs, ts, 100.0 * fs / ts))
    for nt, sub in g[flip].groupby("nt"):
        print("Q2 CAMBIA nt=%s neuronas=%d aristas=%d sinapsis=%d" % (
            nt, sub.pre.nunique(), int(sub.edges.sum()), int(sub.syn.sum())))
    for nt, sub in g[sin_clase].groupby("nt"):
        print("Q2 SIN_CLASE_EN_DCMT nt=%s neuronas=%d aristas=%d sinapsis=%d" % (
            nt, sub.pre.nunique(), int(sub.edges.sum()), int(sub.syn.sum())))

    # Q4: el motivo de la 003 y la entrada que el recorte deja afuera
    dn_ids = a.root_id[a.cell_type.isin(["DNp01", "DNp07"])].tolist()
    vis_ids = a.root_id[a.cell_type.isin(list(VIS))].tolist()
    c = pq.read_table(CONN, columns=["Presynaptic_ID", "Postsynaptic_ID", "Connectivity", "Excitatory"],
                      filters=[("Postsynaptic_ID", "in", dn_ids + vis_ids)]).to_pandas()
    sel, sub = seleccion_motivo(a, c)
    inh = int((sub.Excitatory < 0).sum())
    print("Q4 MOTIVO neuronas=%d aristas=%d inhibitorias=%d sinapsis=%d" % (
        len(sel), len(sub), inh, int(sub.Connectivity.sum())))
    nts_motivo = a.set_index("root_id").loc[[s[0] for s in sel], "nt"].value_counts()
    print("Q4 MOTIVO_NT " + ",".join("%s=%d" % (k, v) for k, v in nts_motivo.items()))
    reproduce = len(sel) == 28 and len(sub) == 73 and inh == 0
    print("Q4 REPRODUCE_003 (28 neuronas, 73 aristas, 0 inhibitorias) -> %s" % reproduce)
    tipo = dict(zip(a.root_id, a.cell_type))
    lado = dict(zip(a.root_id, a.side))
    ntd = dict(zip(a.root_id, a.nt))
    cdn = c[c.Postsynaptic_ID.isin(dn_ids)].copy()
    cdn["pre_tipo"] = cdn.Presynaptic_ID.map(tipo).fillna("SIN_TIPO")
    cdn["pre_nt"] = cdn.Presynaptic_ID.map(ntd).fillna("SIN_ANOTACION")
    ids_motivo = set(s[0] for s in sel)
    for dn in sorted(dn_ids, key=lambda r: (str(tipo[r]), str(lado[r]))):
        d = cdn[cdn.Postsynaptic_ID == dn]
        tot = int(d.Connectivity.sum())
        dinh = d[d.Excitatory < 0]
        i_syn = int(dinh.Connectivity.sum())
        en_motivo = int(d[d.Presynaptic_ID.isin(ids_motivo)].Connectivity.sum())
        vis = int(d[d.pre_tipo.isin(list(VIS))].Connectivity.sum())
        print("Q4 DN %s %s entrada_total=%d inhibitoria=%d (%.1f%%) de_las_neuronas_del_motivo=%d (%.1f%%) "
              "de_tipos_LC4_LPLC2_LPLC4=%d (%.1f%%) presinapticas=%d" % (
                  tipo[dn], lado[dn], tot, i_syn, 100.0 * i_syn / tot, en_motivo, 100.0 * en_motivo / tot,
                  vis, 100.0 * vis / tot, d.Presynaptic_ID.nunique()))
        top = dinh.groupby(["pre_tipo", "pre_nt"]).Connectivity.sum().sort_values(ascending=False).head(5)
        print("Q4 DN %s %s top_inhibitorias " % (tipo[dn], lado[dn]) +
              "; ".join("%s(%s)=%d" % (k[0], k[1], v) for k, v in top.items()))
    print("# duracion_s=%.1f" % (time.time() - t0))
    rc = 0 if reproduce else 3
    print("EXIT_RUN=%d" % rc)
    return rc


if __name__ == "__main__":
    sys.exit(main())
