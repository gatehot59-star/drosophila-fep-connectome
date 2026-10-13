#!/usr/bin/env python3
"""Corrige F01, F06 y F07 de la auditoria de Tao en la v2.0 (respuesta 2026-10-13-006).

F01. El ensemble de neuropilo permuta destinos solo entre conexiones del mismo bloque: el multiconjunto de destinos
     se conserva en cada bloque y por lo tanto en total, asi que preserva todo in-degree exacto (medido en el
     conectoma entero en la 2026-10-13-001: 138.639 neuronas, 478 bloques, in-degree global exacto). La seccion 3.4,
     la limitacion 7 y la seccion de dos saltos decian que solo lo preserva dentro de los bloques.
F06. Con N = 5 realizaciones CP el p de permutacion mas chico posible, (r + 1)/(N + 1), es 1/6: la limitacion 2 no
     puede decir "Sufficient for Z = +14.8 sigma". El "Sufficient" ya estaba en la v1.0 (v1.0.txt, linea 449), asi que
     entra como cambio 15. El numero +14,8 sigma no se toca: es F05 y espera a Abraham.
F07. El control uniforme rompe el in-degree en 138.140 neuronas en la corrida que produjo las Tablas 5b y 5c
     (evidencia cruda del 2026-08-25, twohop_nulls.py, "nodes_with_in_degree_broken_by_uniform": 138140) y en 138.142
     en otra extraccion (default_rng(7), log de la 061). El texto citaba solo la segunda.
Cada reemplazo exige exactamente una aparicion. Uso: python3 fix_v2_2026-10-13.py <raiz del clon>
"""
import hashlib
import json
import os
import sys

raiz = sys.argv[1]
P = "docs/v2/paper1-v2.0.md"
S = "docs/SECCION-V2-DOS-SALTOS.md"
Z = "docs/v2/zenodo-v2.0-metadata.json"

R = [
    (P, "F01 seccion 3.4",
     "preserving the number of connections between every ordered pair of neuropils in addition to out-degree. It belongs "
     "to the same family as the NPC model of Lin et al. [2024]; it differs in assigning each neuron a single dominant "
     "neuropil rather than assigning individual synapses, and it preserves in-degree only within blocks.",
     "preserving the number of connections between every ordered pair of neuropils in addition to out-degree. Because "
     "targets are only permuted among connections of the same block, the multiset of targets is conserved within every "
     "block and therefore globally, so every in-degree is preserved exactly as well: the ensemble preserves degree and "
     "neuropil-pair counts simultaneously. It belongs to the same family as the NPC model of Lin et al. [2024]; it "
     "differs in assigning each neuron a single dominant neuropil rather than assigning individual synapses."),
    (P, "F07 seccion 3.4",
     "whereas drawing targets uniformly breaks it for 138,142 of 138,639 neurons.",
     "whereas drawing targets uniformly breaks it for 138,140 of 138,639 neurons in the run that produced Tables 5b and "
     "5c (138,142 in a second, independent draw)."),
    (P, "F06 limitacion 2",
     "2. ***N* = 5 for temporal CP.** Sufficient for *Z* = +14.8σ, but tighter intervals would require *N* ≥ 20.",
     "2. ***N* = 5 for temporal CP.** With five realizations the smallest attainable permutation *p*-value, "
     "(*r* + 1)/(*N* + 1), is 1/6 ≈ 0.17, so this test cannot reach conventional significance on its own; *Z* = +14.8σ "
     "rests on a normal approximation whose variance is estimated from five values. An empirical *p* below 0.05 "
     "requires *N* ≥ 20, and below 0.01 requires *N* ≥ 100."),
    (P, "F01 limitacion 7",
     "one dominant neuropil per neuron rather than per-synapse assignment, in-degree preserved within blocks only, no "
     "combined degree-and-neuropil ensemble, no distance-based (NND) ensemble,",
     "one dominant neuropil per neuron rather than per-synapse assignment, no distance-based (NND) ensemble,"),
    (P, "F06 cambio 15",
     "14. Limitations expanded from four to thirteen items.",
     "14. Limitations expanded from four to thirteen items.\n15. Limitation 2: v1.0 called five community-preserving "
     "realizations sufficient for *Z* = +14.8σ; with five realizations the smallest attainable permutation *p*-value "
     "is 1/6."),
    (S, "F01 seccion de dos saltos, ensemble",
     "preserving the number of connections between every ordered pair of neuropils in addition to out-degree. It belongs "
     "to the same family as the neuropil-connection (NPC) model of Lin et al. (2024); it differs in assigning each "
     "neuron a single dominant neuropil rather than assigning individual synapses, and it preserves in-degree only "
     "within blocks.",
     "preserving the number of connections between every ordered pair of neuropils in addition to out-degree. Because "
     "targets are only permuted among connections of the same block, the multiset of targets is conserved within every "
     "block and therefore globally, so every in-degree is preserved exactly as well. It belongs to the same family as "
     "the neuropil-connection (NPC) model of Lin et al. (2024); it differs in assigning each neuron a single dominant "
     "neuropil rather than assigning individual synapses."),
    (S, "F07 seccion de dos saltos",
     "an alternative construction drawing targets uniformly breaks it for 138,142 of 138,639 neurons.",
     "an alternative construction drawing targets uniformly breaks it for 138,140 of 138,639 neurons in the run that "
     "produced the tables (138,142 in a second, independent draw)."),
    (S, "F01 seccion de dos saltos, limitacion",
     "> **In-degree is preserved exactly only in the degree ensemble.** Within the neuropil ensemble it is preserved "
     "within blocks and not globally, so a residual effect measured against it may reflect degree rather than anatomy. "
     "A combined ensemble preserving both simultaneously was not constructed, and is the appropriate next control.",
     "> **In-degree is preserved exactly in both ensembles.** The neuropil ensemble permutes targets only among "
     "connections of the same block, so the multiset of targets is conserved within every block and therefore "
     "globally: it preserves every in-degree and out-degree together with the neuropil-pair counts, and is already a "
     "combined degree-and-neuropil ensemble. A residual effect measured against it is therefore not explained by the "
     "degree sequence."),
]

textos = {}
for ruta in (P, S, Z):
    with open(os.path.join(raiz, ruta), encoding="utf-8") as f:
        textos[ruta] = f.read()
    print("ANTES", ruta, hashlib.md5(textos[ruta].encode("utf-8")).hexdigest())

for ruta, nombre, viejo, nuevo in R:
    n = textos[ruta].count(viejo)
    print("REEMPLAZO", nombre, "apariciones=%d" % n)
    if n != 1:
        sys.exit("FALLA: '%s' aparece %d veces en %s" % (nombre, n, ruta))
    textos[ruta] = textos[ruta].replace(viejo, nuevo)

for ruta in (P, S):
    with open(os.path.join(raiz, ruta), "w", encoding="utf-8") as f:
        f.write(textos[ruta])
    print("DESPUES", ruta, hashlib.md5(textos[ruta].encode("utf-8")).hexdigest())

# Controles: las frases viejas ya no estan, las nuevas si, y los metadatos no traian ninguna de las tres
for ruta, nombre, viejo, nuevo in R:
    assert viejo not in textos[ruta] or viejo in nuevo, nombre
    assert nuevo in textos[ruta], nombre
for ruta in (P, S):
    assert "in-degree only within blocks" not in textos[ruta], ruta
    assert "breaks it for 138,142 of" not in textos[ruta], ruta
assert "Sufficient for" not in textos[P]
assert "preserved within blocks only" not in textos[P]
assert "no combined degree-and-neuropil ensemble" not in textos[P]
for frase in ("within blocks", "138,142", "Sufficient"):
    assert frase not in textos[Z], frase
json.loads(textos[Z])
print("PARCHE OK: 8 reemplazos (5 en el manuscrito, 3 en la seccion de dos saltos); metadatos sin cambios")
