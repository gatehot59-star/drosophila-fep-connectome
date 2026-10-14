#!/usr/bin/env python3
"""Suaviza F05 de la auditoria de Tao en la v2.0 (respuesta 2026-10-13-014, pedido de Abraham 18:17).

F05. El resumen, la lista de contribuciones, la seccion 3.7, la discusion de las tres propiedades, las conclusiones y
     los metadatos de Zenodo usaban Z_CP = +14,8 sigma como firme ("survives the community-preserving control",
     "requires specific wiring"). Pero la Tabla 8 no se reproduce con el codigo archivado (limitacion 5) y con cinco
     realizaciones CP el p de permutacion mas chico es 1/6 (limitacion 2). El numero se conserva, la Tabla 8 queda
     igual y cambian las frases: pasa a ser una observacion contra cinco realizaciones, sin reproducir. Entra como
     cambio 16.
Cada reemplazo exige exactamente una aparicion. Uso: python3 fix_v2_f05_2026-10-13.py <raiz del clon>
"""
import hashlib
import json
import os
import sys

raiz = sys.argv[1]
P = "docs/v2/paper1-v2.0.md"
Z = "docs/v2/zenodo-v2.0-metadata.json"

R = [
    (P, "resumen, propiedad 1",
     "post-stimulus amplification requires specific wiring (*Z*~CP~ = +14.8σ). **(2)",
     "post-stimulus, Real stays far above the mean of five community-preserving realizations (reported *Z*~CP~ = +14.8σ, a normal "
     "approximation over five values; not reproduced from the archived code). **(2)"),
    (P, "resumen, propiedad 3",
     "an effect that survives the community-preserving control (*Z*~CP~ = +14.8σ); the linear model",
     "well above the mean of five community-preserving realizations (0.83 against 0.30; not reproduced, *N* = 5); the linear model"),
    (P, "contribuciones, item 3",
     "3. **Non-trivial temporal amplification** that survives the community-preserving control.",
     "3. **Non-trivial temporal amplification**, well above the mean of five community-preserving realizations in Table 8, which has "
     "not been reproduced from the archived code."),
    (P, "seccion 3.7",
     "The difference (*Z*~CP~ = +14.8σ) shows that generic modularity is insufficient.",
     "The difference (*Z*~CP~ = +14.8σ, a normal approximation over five realizations; Section 5, items 2 and 5) suggests "
     "that generic modularity is insufficient; with five realizations it cannot be established by permutation."),
    (P, "discusion, propiedad 1",
     "Post-stimulus amplification is non-trivial (*Z*~CP~ = +14.8σ).",
     "Post-stimulus amplification is well above the mean of five CP realizations (*Z*~CP~ = +14.8σ; not reproduced, *N* = 5)."),
    (P, "discusion, propiedad 3",
     "It requires fine wiring (*Z*~CP~ = +14.8σ) and quasi-linear",
     "It appears to require fine wiring (*Z*~CP~ = +14.8σ against five CP realizations, not reproduced) and quasi-linear"),
    (P, "conclusiones, item 1",
     "1. **Intermodal isolation:** during-stimulus separation is modular; post-stimulus amplification requires specific "
     "wiring (*Z*~CP~ = +14.8σ).",
     "1. **Intermodal isolation:** during-stimulus separation is modular; post-stimulus amplification is well above the mean of five "
     "CP realizations (*Z*~CP~ = +14.8σ), pending a reproduction of Table 8 with *N* ≥ 20."),
    (P, "cambio 16",
     "15. Limitation 2: v1.0 called five community-preserving realizations sufficient for *Z* = +14.8σ; with five "
     "realizations the smallest attainable permutation *p*-value is 1/6.",
     "15. Limitation 2: v1.0 called five community-preserving realizations sufficient for *Z* = +14.8σ; with five "
     "realizations the smallest attainable permutation *p*-value is 1/6.\n"
     "16. Post-stimulus amplification (Table 8, *Z*~CP~ = +14.8σ) is no longer stated as surviving the "
     "community-preserving control or as requiring specific wiring. The abstract, the list of contributions, Section 3.7, "
     "the discussion of the three properties and the conclusions now report it as an observation over five realizations "
     "that has not been reproduced from the archived code."),
    (Z, "metadatos de Zenodo",
     "post-stimulus amplification requires specific wiring, Z_CP = +14.8 sigma)",
     "post-stimulus amplification well above the mean of five community-preserving realizations, reported Z_CP = +14.8 sigma, not "
     "reproduced)"),
]

textos = {}
for ruta in (P, Z):
    with open(os.path.join(raiz, ruta), encoding="utf-8") as f:
        textos[ruta] = f.read()
    print("ANTES", ruta, hashlib.md5(textos[ruta].encode("utf-8")).hexdigest())

for ruta, nombre, viejo, nuevo in R:
    n = textos[ruta].count(viejo)
    print("REEMPLAZO", nombre, "apariciones=%d" % n)
    if n != 1:
        sys.exit("FALLA: '%s' aparece %d veces en %s" % (nombre, n, ruta))
    textos[ruta] = textos[ruta].replace(viejo, nuevo)

# Controles antes de escribir: las frases firmes ya no estan, las nuevas si, el json parsea
for ruta, nombre, viejo, nuevo in R:
    assert viejo not in textos[ruta] or viejo in nuevo, nombre
    assert nuevo in textos[ruta], nombre
for frase in ("survives the community-preserving control", "requires specific wiring", "It requires fine wiring",
              "shows that generic modularity is insufficient", "amplification is non-trivial ("):
    assert frase not in textos[P], frase
assert "requires specific wiring" not in textos[Z]
json.loads(textos[Z])
assert textos[P].count("| 195 | Post + 135 | 0.833 | 0.299 | +14.8 | 0.001 | +2842 |") == 1, "Tabla 8 intacta"

for ruta in (P, Z):
    with open(os.path.join(raiz, ruta), "w", encoding="utf-8") as f:
        f.write(textos[ruta])
    print("DESPUES", ruta, hashlib.md5(textos[ruta].encode("utf-8")).hexdigest())
print("PARCHE OK: 9 reemplazos (8 en el manuscrito, 1 en los metadatos); la Tabla 8 queda igual")
