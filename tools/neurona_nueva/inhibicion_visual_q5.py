#!/usr/bin/env python3
"""Q5 (respuesta 2026-10-12-011): de la entrada inhibitoria de las 4 descendentes del motivo de la 003
(DNp01 y DNp07 de cada lado), cuanta viene de neuronas que a su vez reciben de LC4, LPLC2 o LPLC4, o sea
a dos saltos de la misma entrada visual del motivo. Si es poca, el recorte de 28 neuronas no deja afuera
inhibicion visual y la tarea de solo vision no la necesitaria; si es mucha, el recorte la saco.
Umbrales de entrada visual sumada por neurona: 1, 5 y 20 sinapsis. No entrena nada.
Salida: 0 completo; 2 md5 de datos distinto del pin.
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
VIS = ("LC4", "LPLC2", "LPLC4")
DNS = ("DNp01", "DNp07")


def md5(p):
    h = hashlib.md5()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


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
    a = pd.read_csv(ANNOT, sep="\t", dtype=str, usecols=["root_id", "cell_type", "side", "top_nt"])
    a["root_id"] = a.root_id.astype(np.int64)
    tipo = dict(zip(a.root_id, a.cell_type))
    lado = dict(zip(a.root_id, a.side))
    nt = dict(zip(a.root_id, a.top_nt))
    dn_ids = a.root_id[a.cell_type.isin(list(DNS))].tolist()
    vis_ids = set(a.root_id[a.cell_type.isin(list(VIS))].tolist())
    print("DN=%d VISUALES_LC4_LPLC2_LPLC4=%d" % (len(dn_ids), len(vis_ids)))
    cdn = pq.read_table(CONN, columns=["Presynaptic_ID", "Postsynaptic_ID", "Connectivity", "Excitatory"],
                        filters=[("Postsynaptic_ID", "in", dn_ids)]).to_pandas()
    inh = cdn[cdn.Excitatory < 0]
    inh_pre = sorted(set(inh.Presynaptic_ID.tolist()))
    print("INHIBITORIAS_PRESINAPTICAS_A_LAS_4_DN=%d sinapsis=%d" % (len(inh_pre), int(inh.Connectivity.sum())))
    c1 = pq.read_table(CONN, columns=["Presynaptic_ID", "Postsynaptic_ID", "Connectivity"],
                       filters=[("Postsynaptic_ID", "in", inh_pre)]).to_pandas()
    entrada_total = c1.groupby("Postsynaptic_ID").Connectivity.sum()
    entrada_vis = c1[c1.Presynaptic_ID.isin(vis_ids)].groupby("Postsynaptic_ID").Connectivity.sum()
    entrada_vis = entrada_vis.reindex(entrada_total.index).fillna(0)
    for umbral in (1, 5, 20):
        driven = set(entrada_vis[entrada_vis >= umbral].index)
        for dn in sorted(dn_ids, key=lambda r: (str(tipo[r]), str(lado[r]))):
            d = inh[inh.Postsynaptic_ID == dn]
            tot = int(d.Connectivity.sum())
            dd = d[d.Presynaptic_ID.isin(driven)]
            drv = int(dd.Connectivity.sum())
            print("Q5 umbral_vis>=%d DN %s %s inhibitoria=%d de_inhibitorias_con_entrada_visual=%d (%.1f%%) neuronas=%d" % (
                umbral, tipo[dn], lado[dn], tot, drv, 100.0 * drv / tot if tot else 0.0, dd.Presynaptic_ID.nunique()))
        print("Q5 umbral_vis>=%d TAMANO_MOTIVO_AMPLIADO 28 + %d inhibitorias = %d neuronas" % (
            umbral, len(driven), 28 + len(driven)))
    top = inh.groupby("Presynaptic_ID").Connectivity.sum().sort_values(ascending=False).head(12)
    for pre, s in top.items():
        tv, tt = float(entrada_vis.get(pre, 0)), float(entrada_total.get(pre, 0))
        print("Q5 TOP_INHIBITORIA %s (%s, %s) a_las_DN=%d entrada_desde_LC4_LPLC2_LPLC4=%d de %d (%.1f%%)" % (
            tipo.get(pre), nt.get(pre), lado.get(pre), int(s), int(tv), int(tt), 100.0 * tv / tt if tt else 0.0))
    print("# duracion_s=%.1f" % (time.time() - t0))
    print("EXIT_RUN=0")
    return 0


if __name__ == "__main__":
    sys.exit(main())
