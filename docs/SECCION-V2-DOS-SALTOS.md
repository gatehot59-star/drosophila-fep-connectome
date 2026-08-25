# Sección de acceso motor multi-salto · redactada para la v2 del Paper 1

**Escrito:** 2026-08-24 23:55 · **Fuente de todos los números:** resp 061, medido. Contexto: `docs/agents/CONTEXTO-drosophila-fep.md` §3.

> **⚠️ Esto NO va al erratum.** El erratum corrige v1.0; esto es **material nuevo** que v1.0 no contiene. Va como sección de la v2 del paper, y el erratum no lo menciona.

**Qué problema resuelve.** v1.0 mide acceso motor **a un salto** y reporta que las clases sensoriales están depletadas. Eso tiene una explicación rival barata: **las neuronas sensoriales periféricas casi no salen de su propio neuropilo**, así que no llegan a motoras porque no llegan a ningún lado. Medido: de los 21.019 socios postsinápticos de la clase visual a un salto, **17.503 son del propio lóbulo óptico**. Si eso es todo, el resultado es anatomía de manual y no un hallazgo.

**La sección de abajo lo desarma midiendo a dos saltos**, donde las cuatro clases ya salieron de su territorio por decenas de miles de nodos, y la asimetría **persiste** con un factor de 323 entre extremos.

---

## A · Para Methods

> **Multi-hop access to brain motor neurons.**
> Brain motor neurons were defined as `super_class == 'motor'`, yielding **110 neurons**, all of which appear in the connectivity graph. This population is nested: 105 carry `cell_class == 'brain_motor_neuron'`, one is annotated `neck_motor_neuron`, and four carry no `cell_class`. All statistics below are reported for both the 110-neuron and the 105-neuron definition; no conclusion depends on the choice. Nine of the 110 carry `status == 'outlier_seg'` and were retained. Their efferent nerves are the pharyngeal (40), maxillary-labial (26), cervical connective (20), antennal (14) and occipital (10).
>
> Two statistics were computed for each sensory class. **Reach** (`R_k`) is the number of distinct motor neurons receiving a directed path of length exactly *k* from any neuron of the class. **Path count** (`P_2`) is the number of distinct two-hop paths from the class to any motor neuron, computed as the sum over all intermediate neurons *v* of (edges from the class into *v*) multiplied by (edges from *v* into the motor population). Reach saturates at two hops under randomization and is therefore reported as a censored quantity (see below); path count does not saturate and is the statistic on which the inferential claim rests.
>
> The null ensemble is a degree-preserving configuration model: the vector of edge targets is randomly permuted while the vector of edge sources is held fixed. This preserves the out-degree of every neuron exactly, by construction, and the in-degree of every neuron exactly, since the multiset of targets is conserved. Forty realizations were generated with seeds 1000 + 7*i*, *i* = 0 to 39. The ensemble admits self-loops (317 in a representative realization, against 0 in the observed graph) and repeated edges; the resulting bias inflates path counts in the null and therefore acts **against** the enriched classes and **in favour** of the depleted ones, so the depleted effects reported below are conservative in this respect and the enriched ones are not.
>
> **Degree preservation was verified against a positive and a negative control.** The permutation reproduces the observed in-degree vector exactly; an alternative construction drawing targets uniformly at random breaks it for **138,142 of 138,639** neurons. The test therefore distinguishes the two cases and can fail.
>
> **A quantity conserved by construction was measured inside the same run as an internal control:** the total number of edges entering the motor population is 19,860 in the observed graph and 19,860 in all forty realizations, with standard deviation exactly zero. This is the signature of a statistic that the null cannot test, and it is reported here to establish that the statistics of interest do not behave that way.
>
> **A size-matched arbitrary control was included** to establish the ensemble baseline: 10,855 neurons drawn uniformly at random from the graph, matching the neuron count of the visual class.
>
> No synapse threshold was applied, consistent with the remainder of this work; see Limitations.

---

## B · Para Results

> **Modality-dependent motor access persists at two hops and is not explained by peripheral confinement.**
>
> At one hop, olfactory and visual neurons make no connection whatsoever onto brain motor neurons. Under the degree-preserving null these classes are expected to reach a substantial fraction of the population: **71.3 +/- 4.6** motor neurons for olfactory and **52.3 +/- 5.2** for visual, with no realization out of forty falling below 56 and 43 respectively. The observed value of zero corresponds to *z* = -15.4 and *z* = -10.0. Mechanosensory and gustatory neurons, by contrast, reach 64 and 10 motor neurons directly.
>
> Because both olfactory and visual afferents terminate almost entirely within their primary neuropils, a one-hop deficit admits a trivial explanation: these populations may fail to reach motor neurons because they fail to reach anything outside their own territory. This was tested by extending the analysis to two hops, at which point every class has left its primary territory by tens of thousands of neurons (visual reaches 95,160 distinct neurons, mechanosensory 68,471, gustatory 26,535, olfactory 22,940).
>
> **The asymmetry does not diminish; it becomes quantifiable.** Two-hop path counts to the motor population, against forty degree-preserving realizations:
>
> | Class | *N* | Observed *P*2 | Null mean +/- s.d. | Ratio | *z* | Realizations >= observed |
> |---|---|---|---|---|---|---|
> | Olfactory | 2,279 | 901 | 39,522.6 +/- 745.7 | 0.023 | -51.8 | 40/40 |
> | Visual | 10,855 | 1,413 | 23,311.6 +/- 405.3 | 0.061 | -54.0 | 40/40 |
> | Gustatory | 408 | 67,439 | 10,304.1 +/- 229.7 | 6.54 | +248.8 | 0/40 |
> | Mechanosensory | 2,656 | 293,022 | 39,787.8 +/- 740.2 | 7.37 | +342.1 | 0/40 |
>
> All four classes fall outside the full range of the ensemble, in both directions, giving a one-tailed *p* <= 1/41 = 0.024 in each case. The ratio between extremes is **323**.
>
> **The ensemble baseline is not unity, and the ratios above must be read against it.** A size-matched set of 10,855 arbitrarily chosen neurons yields 312,457 observed two-hop paths against 479,029.6 +/- 7,188.5 expected, a ratio of **0.652**. The observed connectome therefore supports fewer two-hop paths to motor neurons than a degree-matched random graph *in general*, independently of sensory identity, and this offset applies to every row of the table. Normalised by that baseline, olfactory access is depleted **28.6-fold** and visual **10.8-fold**, while mechanosensory and gustatory access are enriched **11.3-fold** and **10.0-fold**. The ratio between extremes is unchanged by this normalisation, since it is a quotient of two normalised quantities.
>
> **Reach at two hops is reported as censored rather than as an effect size.** Olfactory reaches 23 of 110 motor neurons and visual 15, against 110 of 110 in every realization of the ensemble; the null distribution is pinned at the ceiling with standard deviation zero. The direction of the effect is unambiguous, since the observed values lie outside the ensemble entirely, but the magnitude is not estimable from this statistic, which is why path count is used for quantification. Mechanosensory reaches all 110 and gustatory 107. Under the 105-neuron definition the corresponding values are 23, 15, 105 and 102, with the null again at the ceiling.
>
> **Interpretation.** The two-hop result separates two explanations that the one-hop result cannot. Peripheral confinement predicts that classes with spatially restricted arbours are cut off from distant targets; it does not predict that four classes, *all* of which have spatially restricted arbours and *all* of which enter the brain through cranial nerves, should differ from one another by a factor of 323 in access to the same 110 target neurons. Gustatory afferents in particular are the smallest of the four populations (*N* = 408) and yet achieve a ten-fold enrichment, while visual afferents are the largest (*N* = 10,855), reach more of the brain than any other class, and remain depleted. The organising variable is therefore not how far a modality projects, but **which targets it is permitted to influence**.
>
> This is consistent with the ordering reported in v1.0 at one hop and extends it: pathways that must drive movement within milliseconds hold direct and short indirect access to motor output, whereas pathways that must first construct a scene or an odour identity reach the same output only through longer routes. It is further consistent with two independent observations: that the giant-fibre escape pathway, which mediates the fastest visually driven behaviour in this animal, makes **no direct connection onto motor neurons** and reaches muscle exclusively through descending neurons; and that spectral random-walk analysis of the same connectome independently localises repeller nodes to the antennal lobes and medullae (Lin et al., 2024).

---

## C · Para Limitations

> **The result is established against degree and is not tested against anatomy.** A degree-preserving null randomises targets across the entire brain without regard to neuropil boundaries or physical distance, and therefore predicts connections between populations whose arbours do not overlap. Any spatial constraint will appear as a large effect against such a null. The appropriate controls are spatially constrained ensembles of the kind introduced by Lin et al. (2024), namely their neuropil-connection (NPC) and neuron-neuron-distance (NND) models. The magnitude of the correction such a null can impose is not hypothetical: for whole-brain reciprocity, moving from a degree-preserving to a neuropil-constrained ensemble reduces the reported over-representation from 43.8-fold to 7.22-fold, absorbing 84 per cent of the effect. No comparable reduction can be excluded here. Neither null could be constructed from the annotation table used in this work, which contains no neuropil assignment; the analysis requires synapse-to-neuropil assignments or arbour positions, neither of which was retrieved.
>
> **What does not depend on that control is the between-class comparison.** A spatial explanation must account for the ordering among four populations that are all spatially restricted and all cranial in origin, and no mechanism is offered by which locality alone produces a 323-fold spread among them. The absolute ratios in the table should be regarded as upper bounds; the ordering and the spread should not.
>
> **Further limitations of the statistic itself.** Path count is a count of routes, not of signal: it ignores synaptic sign and weight, so an inhibitory route is counted identically to an excitatory one, and this is a material omission in a network in which a substantial minority of neurons are inhibitory. It counts paths with edge multiplicity and does not exclude routes passing through another motor neuron. No synapse threshold was applied, so none of these figures is comparable with those of Lin et al. (2024) or Bates et al. (2026), all of which adopt a five-synapse criterion; recomputation under that criterion is required before any cross-study comparison. Paths of length three and above were not examined, so the depth at which visual access to motor neurons is completed, if it is completed, remains unknown. The arbitrary-neuron control establishing the 0.652 baseline is matched on neuron count but not on out-degree, and should be treated as an order of magnitude rather than a calibrated correction.
>
> **Finally, the target population is not muscle.** The brain motor neurons analysed here innervate head structures. Motor neurons for legs, wings, halteres and abdomen reside in the ventral nerve cord, which is absent from this dataset; a whole-nervous-system connectome including the cord has since become available (Bates et al., 2026) and is the appropriate substrate for extending this analysis to locomotor output.

---

## D · Qué figura y qué tabla hacen falta

| Elemento | Contenido | Estado |
|---|---|---|
| **Tabla nueva** | la tabla de *P*2 de la parte B, más la fila del control arbitrario | **los números están, la tabla no está formateada** |
| **Figura, panel a** | *P*2 observado contra la distribución de los 40 nulls, cuatro clases, eje log | **no generada** |
| **Figura, panel b** | reach a 1 y 2 saltos, observado contra null, mostrando el techo | **no generada** |
| **Figura, panel c** | los cuatro ratios normalizados por el 0,652, con la línea del baseline | **no generada** |
| **Suplementario** | las 40 realizaciones por clase, y el script | **el log está en el container, no commiteado; la salida verbatim está en la resp 061** |

## E · Referencias que esta sección obliga a citar

- **Lin, A., Yang, R., et al. (2024).** *Network statistics of the whole-brain connectome of Drosophila.* Nature **634**:153–165. → los modelos **NPC** y **NND** para las Limitations, el 43,8× → 7,22× como calibración, y los repellers en AL y ME para la Interpretation.
- **Bates, A. S., Phelps, J. S., Kim, M., Yang, H. H., et al. (2026).** *Distributed control circuits across a brain-and-cord connectome.* Nature, doi:10.1038/s41586-026-10735-w. → el cordón ausente, y su observación de que los efectores reciben influencia sobre todo de sensores de la misma parte del cuerpo, que es la explicación rival que esta sección acota.
- **Dorkenwald, S., Matsliah, A., et al. (2024).** *Neuronal wiring diagram of an adult brain.* Nature **634**:124–138. → el dataset y el criterio de cinco sinapsis.

## F · NO MEDIDO, que esta sección declara y no resuelve

1. **No hay null anatómico.** Es la Limitation principal y no es salvable con los datos locales.
2. **El control arbitrario no está pareado en grado de salida.**
3. **Sin umbral de ≥5 sinapsis:** nada de esto es comparable con Lin ni con Bates hasta re-correrlo.
4. **Sin 3 saltos.**
5. **`P2` ignora signo y peso.**
6. **No se midió si excluir las 9 `outlier_seg` cambia algo.**
7. **Las figuras no existen.**
8. **No se verificó si alguien ya publicó este análisis multi-salto por modalidad.** Cinco búsquedas el 24-ago no lo encontraron: apoyado, no establecido.
9. **La frase «which targets it is permitted to influence» es interpretación, no medición.** No hay evidencia de mecanismo de desarrollo ni funcional detrás de la palabra «permitted».
