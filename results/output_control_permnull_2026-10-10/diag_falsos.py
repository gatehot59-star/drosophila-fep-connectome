# Diagnostico: los etiquetados falsos del control negativo de perm y estr son distintos?
# (las dos corridas dieron el mismo numero de flags: 7/4840 en >=1 y 4/4620 en >=5)
import sys
import numpy as np
sys.path.insert(0, "/workspace/dfc-t7/tools")
import output_control_by_class as oc
import output_control_permutation_null as pn

pre, post, S, exc, id_of, g = oc.leer_grafo("/workspace/connectivity.parquet")
del exc
anot = oc.leer_anotaciones("/workspace/annotations.tsv", id_of)
nombres, cls = oc.codificar_clases(anot["super_class"])
n = len(id_of)
n1, n2 = oc.conjuntos_salida(anot["super_class"], anot["cell_sub_class"], anot["cell_type"])
es = np.zeros(n, dtype=bool)
for s_ in oc.SALIDAS:
    es[n1[s_]] = True
for umbral in (1, 5):
    if umbral > 1:
        m = S >= umbral
        p, q, s = pre[m], post[m], S[m]
    else:
        p, q, s = pre, post, S
    _, est, ancho = pn.estratos_por_fuerza(p, q, s, n, es, pn.N_ESTRATOS)
    labs = {}
    for mi, modo in enumerate(pn.MODOS):
        rng = np.random.default_rng([pn.SEED, umbral, mi, 99])
        P = pn.Permutador(cls, est, modo)
        labs[modo] = [P(rng) for _ in range(pn.N_FALSOS)]
    iguales = sum(int(np.array_equal(a, b)) for a, b in zip(labs["perm"], labs["estr"]))
    f_pe = float(np.mean([np.mean(a == b) for a, b in zip(labs["perm"], labs["estr"])]))
    f_pr = float(np.mean([np.mean(a == cls) for a in labs["perm"]]))
    f_er = float(np.mean([np.mean(a == cls) for a in labs["estr"]]))
    azar = float(np.sum((np.bincount(cls) / n) ** 2))
    print("DIAG_FALSOS umbral=%d falsos=%d identicos_perm_estr=%d misma_etiqueta perm-estr=%.4f perm-real=%.4f"
          " estr-real=%.4f esperado_al_azar=%.4f" % (umbral, pn.N_FALSOS, iguales, f_pe, f_pr, f_er, azar))
