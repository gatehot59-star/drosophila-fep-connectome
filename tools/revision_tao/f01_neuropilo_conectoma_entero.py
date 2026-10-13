#!/usr/bin/env python3
"""F01 de Tao sobre el conectoma completo: neuropil_permutation (blob 9b0bd4a) preserva el in-degree global?

La propiedad no depende de las etiquetas: permutar destinos dentro de cualquier particion de las aristas conserva el
multiconjunto global de destinos. Como en brain-env no esta el archivo de neuropilo dominante por neurona, los bloques
se arman con una etiqueta por neurona de las anotaciones pineadas (super_class|side): mismo algoritmo, otra particion.
Control negativo: destinos uniformes (semilla 7), que tienen que romper el in-degree.
"""
import sys
import time
import types

import numpy as np
import pandas as pd

sys.path.insert(0, "/workspace/tm_2026-10-12/rev_tao/titan_materializacion-h4-guard-2026-10-02/src")
import twohop_nulls as tn  # noqa: E402

t0 = time.time()
c = pd.read_parquet("/workspace/connectivity.parquet", columns=["Presynaptic_ID", "Postsynaptic_ID"])
pre = c.Presynaptic_ID.values
post = c.Postsynaptic_ID.values
del c
ids = np.unique(np.concatenate([pre, post]))
src = np.searchsorted(ids, pre).astype(np.int64)
dst = np.searchsorted(ids, post).astype(np.int64)
del pre, post
n = len(ids)
a = pd.read_csv("/workspace/annotations.tsv", sep="\t", dtype=str, usecols=["root_id", "super_class", "side"])
lab = pd.Series((a.super_class.fillna("NA") + "|" + a.side.fillna("NA")).values, index=a.root_id.astype(np.int64).values)
codes = pd.Categorical(lab.reindex(ids).fillna("SIN_ANOTACION").values).codes.astype(np.int64)
L = int(codes.max()) + 1
print("SUJETO neuronas=%d aristas=%d etiquetas=%d" % (n, len(dst), L), flush=True)
g = types.SimpleNamespace(src=src, dst=dst)
perm = tn.neuropil_permutation(g, codes, codes, np.random.default_rng(1000))
indeg = np.bincount(dst, minlength=n)
indeg_p = np.bincount(perm, minlength=n)
outdeg_ok = True
print("F01 in_degree_global_preservado_exacto=%s destinos_cambiados=%d de %d" % (
    bool((indeg == indeg_p).all()), int((perm != dst).sum()), len(dst)), flush=True)
k0 = np.bincount(codes[src] * L + codes[dst], minlength=L * L)
k1 = np.bincount(codes[src] * L + codes[perm], minlength=L * L)
print("F01 conteo_por_par_de_bloques_preservado=%s bloques_no_vacios=%d" % (bool((k0 == k1).all()), int((k0 > 0).sum())), flush=True)
u = np.random.default_rng(7).integers(0, n, len(dst))
rotos = int((np.bincount(u, minlength=n) != indeg).sum())
print("CONTROL uniforme rompe in_degree en %d de %d -> el chequeo puede dar rojo=%s" % (rotos, n, rotos > 0), flush=True)
print("# duracion_s=%.1f" % (time.time() - t0))
