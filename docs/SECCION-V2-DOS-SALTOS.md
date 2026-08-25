# Sección de acceso motor multi-salto · redactada para la v2 del Paper 1

**Escrito:** 2026-08-24 23:55 · **REESCRITO:** 2026-08-25 00:45 tras el null anatómico (resp 063).
**Fuente de todos los números:** `src/twohop_nulls.py` (md5 `a3d52df61a2bc2ccbb332a01c1353dba`), evidencia cruda verbatim en `docs/agents/evidencia/2026-08-24-null-anatomico-evidencia-cruda.md`.

> **⚠️ Esto NO va al erratum.** El erratum corrige v1.0; esto es **material nuevo**. Va como sección de la v2.

> ## 🔴 LA VERSIÓN ANTERIOR DE ESTE ARCHIVO ESTABA MAL, Y ASÍ SE ROMPIÓ
>
> Reclamaba un **spread de 323×** entre modalidades en acceso motor a dos saltos, y sostenía verbatim que *«la localidad no explica 323× entre cuatro poblaciones que son todas locales y todas craneales»*. Su propia sección de Limitations declaraba que faltaba el control anatómico y que en Lin ese control se come el 84% del efecto.
>
> **Se corrió el control. Se come el 100% y además da vuelta el signo.** Y el motivo se pudo medir: **104 de las 110 motoras de cabeza tienen su salida dominante en GNG o PRW, y mechanosensorial y gustativa también.** Olfatoria vive en el lóbulo antenal, visual en lámina y médula. **Las cuatro clases no eran «igual de locales»: dos son locales al neuropilo motor y dos no. Eso es el efecto entero.**
>
> **Lo que queda es el resultado inverso, y sobrevive al null más fuerte disponible.**

---

## A · Para Methods

> **Multi-hop access to brain motor neurons.**
> Brain motor neurons were defined as `super_class == 'motor'`, yielding **110 neurons**, all present in the connectivity graph (109 above the five-synapse threshold). The population is nested: 105 carry `cell_class == 'brain_motor_neuron'`, one is annotated `neck_motor_neuron`, and four carry no `cell_class`. All statistics are reported for both definitions; no conclusion depends on the choice. Nine carry `status == 'outlier_seg'` and were retained. Their efferent nerves are the pharyngeal (40), maxillary-labial (26), cervical connective (20), antennal (14) and occipital (10).
>
> Three statistics were computed per sensory class. **Reach** (`R1`, `R2`) is the number of distinct motor neurons receiving a directed path of length exactly one or two. **Path count** (`P2`) is the number of two-hop paths into the motor population, computed as the sum over intermediate neurons *v* of (edges from the class into *v*) multiplied by (edges from *v* into the motor population).
>
> Every analysis was run at **no synapse threshold** and at the **five-synapse threshold** adopted by Dorkenwald et al. (2024), Lin et al. (2024) and Bates et al. (2026). Thresholding retains 2,700,513 of 15,091,983 connections (17.9 per cent) over 134,181 neurons. **The threshold is not cosmetic here:** without it, `R2` is unusable because every null realization reaches the entire motor population and the ensemble standard deviation is exactly zero; under the threshold it is 1.04 and the statistic becomes estimable.
>
> **Two null families were used, and the comparison between them is the result.**
>
> The **degree-preserving** ensemble permutes the vector of edge targets while holding sources fixed, preserving the out-degree of every neuron by construction and the in-degree exactly, since the multiset of targets is conserved. It admits self-loops (317 at no threshold, against 0 observed) and repeated edges.
>
> The **neuropil-preserving** ensemble permutes targets only within groups of edges sharing the same ordered pair of (source neuropil, target neuropil), preserving the number of connections between every ordered pair of neuropils in addition to out-degree. It belongs to the same family as the neuropil-connection (NPC) model of Lin et al. (2024); it differs in assigning each neuron a single dominant neuropil rather than assigning individual synapses, and it preserves in-degree only within blocks. Neuropil assignments are the per-neuron neuropil synapse counts of the FlyWire 783 release (Zenodo 10676866), giving **79 labels**, with 283 of 138,639 neurons lacking an output assignment and 495 lacking an input assignment; these fall into an explicit unassigned block rather than being discarded.
>
> Forty realizations per family, seeds 1000 + 7*i*.
>
> **Degree preservation was verified against a positive and a negative control.** The permutation reproduces the observed in-degree vector exactly; an alternative construction drawing targets uniformly breaks it for 138,142 of 138,639 neurons. The test therefore distinguishes the two cases and can fail.
>
> **A quantity conserved by construction was measured inside the same run:** the total number of edges entering the motor population is 19,860 observed and 19,860 in all forty realizations, standard deviation zero. This is the signature of a statistic no permutation of targets can test, and it is reported to establish that the statistics of interest do not behave that way.
>
> **A size-matched arbitrary control** of 10,855 randomly drawn neurons establishes the ensemble baseline for each family.

---

## B · Para Results

> **Modality-dependent motor access is an expression of neuropil co-location, not of a routing hierarchy.**
>
> Against a degree-preserving ensemble the four sensory classes differ enormously in two-hop access to brain motor neurons. Olfactory and visual afferents fall far below expectation (ratios 0.023 and 0.061; *z* = −51.8 and −54.0; 40 of 40 realizations exceeding the observed value), while mechanosensory and gustatory afferents fall far above it (7.36 and 6.54; *z* = +342 and +249; 0 of 40). The ratio between extremes is 323. Direct access shows the same ordering: olfactory and visual reach no motor neuron at all, against 71.3 ± 4.6 and 52.3 ± 5.2 expected.
>
> **That entire pattern is accounted for by anatomy.** Under the neuropil-preserving ensemble the ordering inverts:
>
> | Class | *N* | Observed *P*2 | Degree null | Neuropil null | Sign |
> |---|---|---|---|---|---|
> | Olfactory | 2,279 | 901 | 0.023 (*z* −51.8, 40/40) | 0.368 (*z* −4.4, 40/40) | unchanged, 16-fold weaker |
> | Visual | 10,855 | 1,413 | 0.061 (*z* −54.0, 40/40) | **1.531 (*z* +4.1, 0/40)** | **inverted** |
> | Mechanosensory | 2,656 | 293,022 | 7.36 (*z* +342, 0/40) | **0.803 (*z* −20.6, 40/40)** | **inverted** |
> | Gustatory | 408 | 67,439 | 6.54 (*z* +249, 0/40) | **0.632 (*z* −37.2, 40/40)** | **inverted** |
> | Arbitrary control | 10,855 | 312,457 | 0.652 | **1.010** | baseline offset absorbed |
>
> The same inversion holds under the five-synapse threshold (olfactory 0.121, visual **4.87**, mechanosensory **0.974** and no longer significant at 38 of 40, gustatory **0.376**). The 323-fold spread collapses to 2.4-fold, and the 0.652 baseline of the arbitrary control, which under a degree-preserving ensemble appears to be a global property of the connectome, becomes 1.010: **it was the effect of connections respecting neuropil boundaries, and nothing else.**
>
> The mechanism is directly measurable. Taking each neuron's dominant neuropil by presynaptic site count, **104 of the 110 brain motor neurons lie in the gnathal ganglion or the prow**, and so do mechanosensory afferents (GNG 1,712; SAD 468) and gustatory afferents (GNG 353; PRW 52). Olfactory afferents lie in the antennal lobes (AL 2,276) and visual afferents in the lamina and medulla (LA 8,086; ME 2,622). Two of the four classes share an address with the motor population and two do not; no further explanation of the degree-null ordering is required. This is the neuropil-scale form of the observation of Bates et al. (2026) that effector neurons are principally influenced by sensory neurons of the same body part.
>
> **Once co-location is controlled for, the informative result is the opposite of the one the degree-preserving ensemble suggests.** Direct motor access, against the neuropil-preserving ensemble:
>
> | Class | Observed `R1` | Neuropil null | *z* | Realizations ≥ observed |
> |---|---|---|---|---|
> | Gustatory | **10** | 101.6 ± 1.2 | **−78.9** | 40/40 |
> | Mechanosensory | **64** | 98.6 ± 1.6 | **−21.7** | 40/40 |
> | Olfactory | 0 | 1.0 ± 0.9 | −1.2 | 40/40 |
> | Visual | 0 | 0.03 ± 0.16 | −0.2 | 40/40 |
>
> Under the five-synapse threshold the contrast sharpens: gustatory afferents contact 2 motor neurons where co-location predicts 91.0, mechanosensory 33 where it predicts 89.2, and the ensemble predicts exactly 0.0 for olfactory and visual.
>
> **Two conclusions follow, and they replace the previous framing.** First, the absence of olfactory and visual connections onto brain motor neurons is **predicted by the anatomy** and carries no additional information: for these two classes the neuropil-preserving ensemble reproduces the observed value, so the statistic is not testable against it and the earlier interpretation of the zero as a structural exclusion is withdrawn. Second, the classes that do share a neuropil with the motor population are **strongly depleted relative to that co-location**: gustatory afferents make an order of magnitude fewer direct motor contacts than proximity predicts. Sensory afferents entering the motor neuropil are therefore not wired to motor neurons wherever they can be; access is restricted even where geometry permits it, and that restriction, unlike the modality ordering, survives the strongest available control.

---

## C · Para Limitations

> **The neuropil-preserving ensemble is an approximation of the published one.** It assigns each neuron the single neuropil holding most of its synaptic sites, whereas the NPC model of Lin et al. (2024) constrains randomization using measured connection probabilities between neuropils at the level of individual synapses. A neuron arborising across several neuropils is therefore represented by one label. The two constructions have not been implemented side by side and compared, so they are described here as belonging to the same family rather than as equivalent.
>
> **In-degree is preserved exactly only in the degree ensemble.** Within the neuropil ensemble it is preserved within blocks and not globally, so a residual effect measured against it may reflect degree rather than anatomy. A combined ensemble preserving both simultaneously was not constructed, and is the appropriate next control.
>
> **A distance-based ensemble was not run.** The neuron-neuron-distance model of Lin et al. (2024) constrains connection probability by physical separation, and arbour coordinates are available in the annotation table; that ensemble remains unmeasured.
>
> **For olfactory and visual direct access the neuropil ensemble conserves the measured quantity** (predicted means 1.0 and 0.03 against an observed 0). Those two rows are therefore reported as not testable against that ensemble rather than as explained by it; the reason the ensemble conserves them is that the anatomy already accounts for the observation, which is why the conclusion is a withdrawal and not a confirmation.
>
> **Statistic-level limitations.** Path count is a count of routes, not of signal: it ignores synaptic sign and weight, so an inhibitory route counts identically to an excitatory one. It counts paths with edge multiplicity and does not exclude routes passing through another motor neuron. Paths of length three and above were not examined. The arbitrary-neuron control is matched on neuron count but not on out-degree. Block purity, that is, the fraction of each neuropil block's edges belonging to the class under test, was not measured, so the amount of freedom the neuropil ensemble retains for each class is not quantified.
>
> **Finally, the target population is not muscle.** These motor neurons innervate head structures; motor neurons for legs, wings, halteres and abdomen reside in the ventral nerve cord, absent from this dataset. A brain-and-cord connectome is now available (Bates et al., 2026) and is the appropriate substrate for extending the analysis to locomotor output.

---

## D · Las tres figuras

Generadas por `src/twohop_nulls.py`, determinista, **con los dos ensembles y los dos umbrales en cada panel**:

| Panel | Contenido | md5 |
|---|---|---|
| **a** | `P2` observado (guion) contra las 40 realizaciones (puntos); grado a la izquierda y neuropilos a la derecha de cada clase; eje log | `8a1806e9b16db8c4d3210523d51622ef` |
| **b** | reach a 1 y 2 saltos; barras del null con su `sd`, puntos del observado; línea de la población motora completa | `c420213caa112be0db40bb7049fc81a9` |
| **c** | ratios normalizados por el control arbitrario; círculo umbral 1, cuadrado umbral 5; borde negro grado, borde rojo neuropilos. **Acá se ve el cruce de signo** | `6ffc18be441974d6fbe7239c6daef572` |

No commiteadas, por la política del repo (nada de binarios derivados). El generador sí, y es determinista.

## E · Referencias que esta sección obliga a citar

- **Lin, A., Yang, R., et al. (2024).** *Network statistics of the whole-brain connectome of Drosophila.* Nature **634**:153–165. → los modelos **NPC** y **NND**, y el umbral de cinco sinapsis.
- **Dorkenwald, S., Matsliah, A., et al. (2024).** *Neuronal wiring diagram of an adult brain.* Nature **634**:124–138. → el dataset y el criterio de cinco sinapsis.
- **Bates, A. S., Phelps, J. S., Kim, M., Yang, H. H., et al. (2026).** *Distributed control circuits across a brain-and-cord connectome.* Nature, doi:10.1038/s41586-026-10735-w. → «same body part», que esta sección **confirma** a escala de neuropilo, y el cordón ausente.
- **FlyWire Consortium (2024).** *FlyWire Whole-brain Connectome Connectivity Data*, v783.0, Zenodo, doi:10.5281/zenodo.10676866. → la asignación a neuropilos por neurona.

## F · NO MEDIDO

1. **NPC exacto por sinapsis, no por neurona dominante.** Sin implementar.
2. **Ensemble combinado grado + neuropilo.** Sin construir; es el control que sigue.
3. **Ensemble por distancia (NND).** Sin correr, y los datos están.
4. **Pureza de bloque por clase.** Sin medir.
5. **`R1` de olfatorio y visual contra el null anatómico: NO TESTEABLE**, no refutado.
6. **El hallazgo de la depleción de gustativa y mechanosensorial no se barrió contra la literatura.** Si ya está publicado, pasa a prior art ajeno, y ese es exactamente el error que esta reescritura corrige.
7. **Sin 3 saltos. Sin signo. Sin peso.**
8. **Las nueve `outlier_seg`** siguen incluidas sin medir su efecto.
9. **Las figuras no están commiteadas**, van por md5.
