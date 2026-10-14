#!/usr/bin/env python3
"""POST HOC (respuesta 2026-10-14-024), despues de ver H_FRENO REFUTADA: de que lado vienen y a que lado van las dos
primeras entradas inhibitorias de DNp06 (LHAD1g1, GABA; PVLP010, glutamato). Descriptivo, sin veredicto.
Uso: python3 posthoc_lhad1g1.py CONN ANNOT
"""
import sys

import numpy as np
import pandas as pd

a = pd.read_csv(sys.argv[2], sep=chr(9), dtype=str, usecols=["root_id", "cell_type", "side", "top_nt"])
a["root_id"] = a.root_id.astype(np.int64)
c = pd.read_parquet(sys.argv[1], columns=["Presynaptic_ID", "Postsynaptic_ID", "Connectivity", "Excitatory"])
T = dict(zip(a.root_id, a.cell_type))
S = dict(zip(a.root_id, a.side))
VIS = ["LPLC2", "LPLC1", "LC4", "LPLC4"]
for t in ("LHAD1g1", "PVLP010"):
    for x in a.root_id[a.cell_type == t]:
        o = c[c.Presynaptic_ID == x]
        o = o[o.Postsynaptic_ID.map(T) == "DNp06"]
        out = {S[p]: int(w) for p, w in o.groupby("Postsynaptic_ID").Connectivity.sum().items()}
        i = c[c.Postsynaptic_ID == x]
        i = i.assign(t=i.Presynaptic_ID.map(T), s=i.Presynaptic_ID.map(S))
        vis = {"%s_%s" % k: int(w) for k, w in i[i.t.isin(VIS)].groupby(["t", "s"]).Connectivity.sum().items()}
        print("POSTHOC %s root=%d lado=%s a_DNp06=%s entrada_visual=%s entrada_total=%d" % (
            t, x, S[x], out, vis, int(i.Connectivity.sum())))
