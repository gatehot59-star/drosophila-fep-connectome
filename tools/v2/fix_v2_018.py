#!/usr/bin/env python3
"""Corrige las tres inconsistencias de la v2.0 confirmadas en la 2026-10-12-010 (respuesta 2026-10-12-018).

1. Seccion 3.4: el '2.4-fold' era visual/gustatory, no el cociente entre extremos (sin umbral: 4.2x).
2. Seccion 2.5 y siguientes: 'validated across three compatible models' con LIF-soft que decae en la Tabla 9.
3. Seccion 3.4: 'not testable' sin precisar umbral (sin umbral el nulo tiene varianza; con umbral es 0.0 exacto).
Cada reemplazo exige exactamente una aparicion. Uso: python3 fix_v2_018.py <raiz del clon>
"""
import hashlib, os, sys

raiz = sys.argv[1]

# Cocientes sin redondear de docs/agents/evidencia/2026-08-24-null-anatomico-evidencia-cruda.md
# (rama titan/materializacion-h4-guard-2026-10-02), lineas 104-107, 114-117, 130-133 y 140-143.
deg = {"olf": 0.022797, "vis": 0.060614, "mec": 7.364619, "gus": 6.544870}
neu = {"olf": 0.367658, "vis": 1.531126, "mec": 0.803276, "gus": 0.632312}
deg5 = {"olf": 0.001505, "vis": 0.046469, "mec": 5.811884, "gus": 2.619469}
neu5 = {"olf": 0.120950, "vis": 4.871795, "mec": 0.974171, "gus": 0.375856}
for nom, d in (("grado", deg), ("neuropilo", neu), ("grado_umbral5", deg5), ("neuropilo_umbral5", neu5)):
    mx, mn = max(d, key=d.get), min(d, key=d.get)
    print("COCIENTE_EXTREMOS %s max=%s %.6f min=%s %.6f -> %.4f" % (nom, mx, d[mx], mn, d[mn], d[mx] / d[mn]))
print("COCIENTE_DEL_2.4 visual/gustatory neuropilo = %.4f" % (neu["vis"] / neu["gus"]))
assert round(deg["mec"] / deg["olf"]) == 323
assert round(neu["vis"] / neu["olf"], 1) == 4.2
assert round(deg5["mec"] / deg5["olf"]) == 3862
assert round(neu5["vis"] / neu5["olf"]) == 40
assert round(neu["vis"] / neu["gus"], 1) == 2.4

P = "docs/v2/paper1-v2.0.md"
E = "docs/ERRATUM.md"
S = "docs/SECCION-V2-DOS-SALTOS.md"
Z = "docs/v2/zenodo-v2.0-metadata.json"

R = [
 (P, "P1 abstract (3)",
  "**(3) Non-trivial temporal amplification.** Under graded dynamics, cosine RDI rises from 0.63 to 0.83 post-stimulus, an effect that survives the community-preserving control (*Z*~CP~ = +14.8σ).",
  "**(3) Non-trivial temporal amplification.** Under SparseLTC dynamics, cosine RDI rises from 0.63 to 0.83 post-stimulus, an effect that survives the community-preserving control (*Z*~CP~ = +14.8σ); the linear model reproduces it and LIF-soft does not, so the amplification is model-dependent."),
 (P, "P2 seccion 1.3",
  "Three propagation properties, validated with three compatible neural models and four null-model families:",
  "Three propagation properties, examined with three metric-compatible neural models and four null-model families (temporal amplification appears in two of the three models; Section 3.7):"),
 (P, "P3 seccion 2.5",
  "Temporal amplification is therefore validated across three compatible models (SparseLTC, Linear, LIF-soft), and LIF-hard is reported as metric-incompatible rather than omitted.",
  "Three models are therefore metric-compatible (SparseLTC, Linear, LIF-soft), and LIF-hard is reported as metric-incompatible rather than omitted. Compatibility is not replication: temporal amplification appears under SparseLTC (cosine RDI 0.630 at step 60, 0.832 at step 180) and Linear (0.623, 0.835), whereas under LIF-soft cosine RDI decays from 0.253 to 0.002 (Table 9)."),
 (P, "P4 seccion 3.4 cociente entre extremos",
  "The 323-fold spread collapses to 2.4-fold, and the 0.652 baseline of the arbitrary control, which under a degree-preserving ensemble looks like a global property of the connectome, becomes 1.010:",
  "Without threshold, the ratio between extremes falls from 323-fold under the degree-preserving ensemble (mechanosensory 7.36 over olfactory 0.023) to 4.2-fold under the neuropil-preserving one (visual 1.531 over olfactory 0.368); under the threshold it falls from 3,862-fold (mechanosensory 5.81 over olfactory 0.0015) to 40-fold (visual 4.87 over olfactory 0.121). The 0.652 baseline of the arbitrary control, which under a degree-preserving ensemble looks like a global property of the connectome, becomes 1.010:"),
 (P, "P5 seccion 3.4 cero de olfato y vision",
  "First, the absence of olfactory and visual connections onto brain motor neurons is predicted by the anatomy and carries no additional information: for these two classes the neuropil-preserving ensemble reproduces the observed value, so the statistic is not testable against it, and an interpretation of the zero as a structural exclusion is not supported.",
  "First, the absence of olfactory and visual connections onto brain motor neurons is predicted by the anatomy and carries no additional information. Without threshold the neuropil-preserving ensemble expects 1.0 ± 0.9 and 0.03 ± 0.16 contacts (Table 5c), so the observed zero lies within its spread (*z* = −1.2 and −0.2) and is not a significant depletion; under the five-synapse threshold the ensemble predicts exactly 0.0 with no variance, and only in that regime is the statistic not testable. In neither regime is an interpretation of the zero as a structural exclusion supported."),
 (P, "P6 nota de la Tabla 9",
  "SparseLTC ≈ Linear: the dynamics are quasi-linear, and in this regime the eigenvalue spectrum of *W* governs the amplification.",
  "SparseLTC ≈ Linear: the dynamics are quasi-linear, and in this regime the eigenvalue spectrum of *W* governs the amplification. LIF-soft does not amplify: its cosine RDI decays from 0.253 to 0.002, so the amplification holds under quasi-linear graded dynamics, not under every graded model."),
 (P, "P7 seccion 4.1",
  "It requires fine wiring (*Z*~CP~ = +14.8σ) and graded dynamics, in a quasi-linear regime, with a physiologically plausible τ.",
  "It requires fine wiring (*Z*~CP~ = +14.8σ) and quasi-linear graded dynamics (SparseLTC and Linear; it does not appear under LIF-soft), with a physiologically plausible τ."),
 (P, "P8 limitacion 3",
  "3. **Model dependence.** Only graded models replicate amplification, and LIF-hard is metric-incompatible. Amplification is not a purely topological property.",
  "3. **Model dependence.** Of the three metric-compatible models, only the quasi-linear ones (SparseLTC and Linear) show the amplification; LIF-soft, also graded, decays from 0.253 to 0.002, and LIF-hard is metric-incompatible. Amplification is not a purely topological property."),
 (P, "P9 cambios desde la v1.0, item 6",
  "6. Models: \"four parameter-free neural models\" replaced by three compatible models, with LIF-hard reported as metric-incompatible [7].",
  "6. Models: \"four parameter-free neural models\" replaced by three compatible models, with LIF-hard reported as metric-incompatible; temporal amplification is stated for the two that show it (SparseLTC and Linear), not for LIF-soft [7]."),
 (E, "E1 item 7, replicacion entre modelos",
  "body of the paper and is corrected to **three compatible models** (SparseLTC, Linear,\nLIF-soft), with the fourth reported as metric-incompatible rather than omitted.\n",
  "body of the paper and is corrected to **three compatible models** (SparseLTC, Linear,\nLIF-soft), with the fourth reported as metric-incompatible rather than omitted.\n\n**Replication across models.** Section 2.5 of v1.0 states that *\"temporal amplification\nresults are validated across three compatible models (SparseLTC, Linear, LIF-soft)\"*, and\nLimitation 3 that *\"temporal amplification is thus validated across three of four models\"*.\nTable 9 of v1.0 shows otherwise for LIF-soft: its cosine RDI decays from 0.253 at step 60\nto 0.002 at step 180. The amplification appears in two of the three compatible models\n(SparseLTC and Linear); LIF-soft, although graded, does not amplify. v2.0 states the\nproperty for the two models that show it.\n"),
 (E, "E2 revision antes de depositar",
  "- Item 7: the tau_m column of Table 10 follows the corrected derivation.\n",
  "- Item 7: the tau_m column of Table 10 follows the corrected derivation; the replication of\n  temporal amplification across models corrected to two of the three compatible models.\n"),
 (S, "S1 cociente entre extremos",
  "The 323-fold spread collapses to 2.4-fold, and the 0.652 baseline of the arbitrary control, which under a degree-preserving ensemble appears to be a global property of the connectome, becomes 1.010:",
  "Without threshold, the ratio between extremes falls from 323-fold under the degree-preserving ensemble (mechanosensory 7.36 over olfactory 0.023) to 4.2-fold under the neuropil-preserving one (visual 1.531 over olfactory 0.368); under the threshold it falls from 3,862-fold (mechanosensory 5.81 over olfactory 0.0015) to 40-fold (visual 4.87 over olfactory 0.121). The 0.652 baseline of the arbitrary control, which under a degree-preserving ensemble appears to be a global property of the connectome, becomes 1.010:"),
 (S, "S2 cero de olfato y vision",
  "for these two classes the neuropil-preserving ensemble reproduces the observed value, so the statistic is not testable against it and the earlier interpretation of the zero as a structural exclusion is withdrawn.",
  "without threshold the neuropil-preserving ensemble expects 1.0 ± 0.9 and 0.03 ± 0.16 contacts, so the observed zero lies within its spread (*z* = −1.2 and −0.2) and is not a significant depletion; under the five-synapse threshold the ensemble predicts exactly 0.0 with no variance, and only there is the statistic not testable. In neither regime does the zero support a structural exclusion, and the earlier interpretation is withdrawn."),
 (S, "S3 nota de conservacion",
  "**For olfactory and visual direct access the neuropil ensemble conserves the measured quantity** (predicted means 1.0 and 0.03 against an observed 0). Those two rows are therefore reported as not testable against that ensemble rather than as explained by it; the reason the ensemble conserves them is that the anatomy already accounts for the observation, which is why the conclusion is a withdrawal and not a confirmation.",
  "**For olfactory and visual direct access the neuropil ensemble is compatible with the measured quantity, not invariant under it** (predicted means 1.0 ± 0.9 and 0.03 ± 0.16 without threshold, against an observed 0). Without threshold those two rows are reported as not significant against that ensemble; under the five-synapse threshold the ensemble predicts exactly 0.0 and they are not testable. In both regimes the anatomy already accounts for the observation, which is why the conclusion is a withdrawal and not a confirmation."),
 (Z, "Z1 descripcion de Zenodo",
  "and non-trivial temporal amplification (cosine RDI from 0.63 to 0.83 post-stimulus).",
  "and non-trivial temporal amplification (cosine RDI from 0.63 to 0.83 post-stimulus under SparseLTC dynamics; reproduced by the linear model, not by LIF-soft)."),
]

textos = {}
for ruta in (P, E, S, Z):
    with open(os.path.join(raiz, ruta), encoding="utf-8") as f:
        textos[ruta] = f.read()
    print("ANTES", ruta, hashlib.md5(textos[ruta].encode("utf-8")).hexdigest())

for ruta, nombre, viejo, nuevo in R:
    n = textos[ruta].count(viejo)
    print("REEMPLAZO", nombre, "apariciones=%d" % n)
    if n != 1:
        sys.exit("FALLA: '%s' aparece %d veces en %s" % (nombre, n, ruta))
    textos[ruta] = textos[ruta].replace(viejo, nuevo)

for ruta in (P, E, S, Z):
    with open(os.path.join(raiz, ruta), "w", encoding="utf-8") as f:
        f.write(textos[ruta])
    print("DESPUES", ruta, hashlib.md5(textos[ruta].encode("utf-8")).hexdigest())

# Control: las frases viejas ya no estan y las nuevas si (positivo y negativo del parche)
for ruta, nombre, viejo, nuevo in R:
    assert viejo not in textos[ruta] or viejo in nuevo, nombre
    assert nuevo in textos[ruta], nombre
for ruta in (P, S):
    assert "2.4-fold" not in textos[ruta], ruta
assert "validated across three compatible models" not in textos[P]
import json
json.loads(textos[Z])
print("PARCHE OK: 15 reemplazos, sin '2.4-fold' en manuscrito ni seccion, metadatos JSON validos")
