#!/usr/bin/env python3
"""Que le falta al modelo de la 015 (respuesta 2026-10-12-018).

Mide, para las 6 descendentes de la tarea de la mosca (DNp01, DNp07 y DNp06 de cada lado), cuanto de su
entrada real esta dentro del motivo de 46 neuronas y cuanto queda afuera, con el signo del pipeline
(columna Excitatory de connectivity.parquet), y el tamano de los dos recortes siguientes:
  R1 = las 6 DN + todas sus presinapticas con >= 5 sinapsis a alguna de ellas
  R2 = R1 + las presinapticas con >= 5 sinapsis a alguna neurona de R1
Descriptivo, sin nulo. Uso: python3 que_falta_al_modelo.py <connectivity.parquet> <annotations.tsv> <completa.log>
"""
import hashlib, re, sys
import numpy as np
import pandas as pd

conn_p, annot_p, log_p = sys.argv[1:4]

def md5(p):
    h = hashlib.md5()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()

print("# md5 conn=%s annot=%s log015=%s" % (md5(conn_p), md5(annot_p), md5(log_p)))
c = pd.read_parquet(conn_p, columns=["Presynaptic_ID", "Postsynaptic_ID", "Connectivity", "Excitatory"])
a = pd.read_csv(annot_p, sep="\t", usecols=["root_id", "super_class", "cell_class", "cell_type", "top_nt", "side"], low_memory=False)
print("DATOS aristas=%d sinapsis=%d neuronas_anotadas=%d" % (len(c), int(c.Connectivity.sum()), len(a)))
print("SIGNO valores_Excitatory=%s" % sorted(c.Excitatory.unique().tolist()))
c["inh"] = c.Excitatory <= 0
tipo = dict(zip(a.root_id, a.cell_type.fillna("(sin tipo)")))
super_ = dict(zip(a.root_id, a.super_class.fillna("(sin clase)")))

motivo, dns = [], []
for linea in open(log_p, encoding="utf-8"):
    m = re.match(r"MOTIVO root_id=(\d+) tipo=(\S+) lado=(\S+)", linea)
    if m:
        rid, t, ld = int(m.group(1)), m.group(2), m.group(3)
        motivo.append(rid)
        if t.startswith("DN"):
            dns.append((t, ld, rid))
M = set(motivo)
print("MOTIVO_015 neuronas=%d descendentes=%d" % (len(M), len(dns)))
assert len(M) == 46 and len(dns) == 6

entra = c[c.Postsynaptic_ID.isin([d[2] for d in dns])]
tot_all = tot_m = tot_inh = 0
for t, ld, rid in dns:
    e = entra[entra.Postsynaptic_ID == rid]
    s = int(e.Connectivity.sum())
    sm = int(e[e.Presynaptic_ID.isin(M)].Connectivity.sum())
    si = int(e[e.inh].Connectivity.sum())
    sim = int(e[e.inh & e.Presynaptic_ID.isin(M)].Connectivity.sum())
    npre = e.Presynaptic_ID.nunique()
    npre5 = int((e.groupby("Presynaptic_ID").Connectivity.sum() >= 5).sum())
    tot_all += s; tot_m += sm; tot_inh += si
    ei = e[e.inh].assign(tipo=lambda x: x.Presynaptic_ID.map(tipo).fillna("(sin anotar)"))
    top = ei.groupby("tipo").Connectivity.sum().sort_values(ascending=False).head(5)
    print("DN %s %s entrada_sinapsis=%d en_motivo=%d (%.2f%%) inhibitorias=%d (%.1f%%) inhibitorias_en_motivo=%d presinapticas=%d con_5_o_mas=%d" % (
        t, ld, s, sm, 100.0 * sm / s, si, 100.0 * si / s, sim, npre, npre5))
    print("DN %s %s top_inhibitorias_por_tipo=%s" % (t, ld, "; ".join("%s %d" % (k, v) for k, v in top.items())))
print("TOTAL_6DN entrada=%d en_motivo=%d (%.2f%%) inhibitorias=%d (%.1f%%)" % (
    tot_all, tot_m, 100.0 * tot_m / tot_all, tot_inh, 100.0 * tot_inh / tot_all))

c5 = c[c.Connectivity >= 5]
D = set(d[2] for d in dns)
U1 = D | set(c5[c5.Postsynaptic_ID.isin(D)].Presynaptic_ID)
U2 = U1 | set(c5[c5.Postsynaptic_ID.isin(U1)].Presynaptic_ID)
for nom, U in (("R1", U1), ("R2", U2)):
    sub = c[c.Presynaptic_ID.isin(U) & c.Postsynaptic_ID.isin(U)]
    sal = c[c.Presynaptic_ID.isin(U)].groupby("Presynaptic_ID").agg(s=("Connectivity", "sum"), si=("inh", "mean"))
    n_inh = int((sal.si > 0.5).sum())
    clases = pd.Series([super_[r] if r in super_ else "(sin anotar)" for r in U]).value_counts().head(6)
    print("RECORTE %s neuronas=%d aristas_internas=%d sinapsis_internas=%d neuronas_inhibitorias=%d (%.1f%%) contiene_motivo=%s clases=%s" % (
        nom, len(U), len(sub), int(sub.Connectivity.sum()), n_inh, 100.0 * n_inh / len(U), M <= U,
        "; ".join("%s %d" % (k, v) for k, v in clases.items())))
print("CEREBRO neuronas_en_aristas=%d aristas=%d" % (len(set(c.Presynaptic_ID) | set(c.Postsynaptic_ID)), len(c)))
print("FIN")
