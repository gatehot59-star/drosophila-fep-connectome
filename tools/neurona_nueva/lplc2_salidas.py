#!/usr/bin/env python3
"""LPLC2 y LC4 en FlyWire v783: a que descendentes llegan (respuesta 2026-10-12-013).
Pregunta que puede dar rojo: si LPLC2 tambien habla con DNp06 (la descendente del giro evasivo de Kim 2023)
y cuanto, comparado con DNp01 (GF), DNp07 y DNp10 (aterrizaje). Y cuantas LPLC2 y LC4 hay por lado
(el motivo de la 003 usa 4 de cada una por lado). Sinapsis sumadas, sin umbral y con umbral >= 5 por par.
"""
import hashlib, os, platform, sys, time
import numpy as np
import pandas as pd
import pyarrow.parquet as pq

CONN = "/workspace/connectivity.parquet"
ANNOT = "/workspace/annotations.tsv"
MD5_CONN = "3d802fd542b5d18570ba1ba0bb0abed9"
MD5_ANNOT = "719904abad876c68ace1b5690c9b9b63"
PRE = ("LPLC2", "LC4", "LPLC4")
DNS = ("DNp01", "DNp06", "DNp07", "DNp10", "DNp11", "DNp02", "DNp04")


def md5(p):
    h = hashlib.md5()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def main():
    t0 = time.time()
    print("# maquina: %s | %s | numpy %s | pandas %s" % (platform.node(), platform.platform(), np.__version__, pd.__version__))
    print("# md5 script = " + md5(os.path.abspath(__file__)))
    print("# fecha: " + time.strftime("%Y-%m-%d %H:%M:%S %z"))
    mc, ma = md5(CONN), md5(ANNOT)
    print("# md5 conn = %s | md5 annot = %s" % (mc, ma))
    if mc != MD5_CONN or ma != MD5_ANNOT:
        print("ABORTA: datos distintos del pin")
        return 2
    a = pd.read_csv(ANNOT, sep="\t", dtype=str, usecols=["root_id", "cell_type", "side"])
    a["root_id"] = a.root_id.astype(np.int64)
    for t in PRE + DNS:
        s = a[a.cell_type == t].side.value_counts().to_dict()
        print("CUENTA tipo=%s por_lado=%s" % (t, s))
    dn_ids = a.root_id[a.cell_type.isin(list(DNS))].tolist()
    c = pq.read_table(CONN, columns=["Presynaptic_ID", "Postsynaptic_ID", "Connectivity", "Excitatory"],
                      filters=[("Postsynaptic_ID", "in", dn_ids)]).to_pandas()
    tipo = dict(zip(a.root_id, a.cell_type))
    lado = dict(zip(a.root_id, a.side))
    c["pre_t"] = c.Presynaptic_ID.map(tipo)
    c["post_t"] = c.Postsynaptic_ID.map(tipo)
    c["ipsi"] = [lado.get(p) == lado.get(q) for p, q in zip(c.Presynaptic_ID, c.Postsynaptic_ID)]
    tot_in = c.groupby("post_t").Connectivity.sum()
    for pre in PRE:
        for umbral in (1, 5):
            d = c[(c.pre_t == pre) & (c.Connectivity >= umbral)]
            for dn in DNS:
                e = d[d.post_t == dn]
                if len(e) == 0:
                    print("SALIDA pre=%s umbral>=%d dn=%s sinapsis=0 pares=0" % (pre, umbral, dn))
                    continue
                syn = int(e.Connectivity.sum())
                print("SALIDA pre=%s umbral>=%d dn=%s sinapsis=%d (%.1f%% de la entrada de %s) pares=%d presinapticas=%d ipsilaterales=%.3f" % (
                    pre, umbral, dn, syn, 100.0 * syn / tot_in[dn], dn, len(e), e.Presynaptic_ID.nunique(),
                    float(e[e.ipsi].Connectivity.sum()) / syn))
    print("# duracion_s=%.1f" % (time.time() - t0))
    print("EXIT_RUN=0")
    return 0


if __name__ == "__main__":
    sys.exit(main())
