# Párrafo pivote de reciprocidad · listo para pegar en la v2 del Paper 1

**Escrito:** 2026-08-24 · **Corregido:** 2026-08-24 23:15 tras la verificación de la resp 057.
**Fuente de los números:** `docs/agents/CONTEXTO-drosophila-fep.md` §§2.bis y 3, resp 045, 050, 052, 053b, **057**.

> ## 🔴 CORRECCIÓN v2 · la versión anterior de este archivo afirmaba algo FALSO
>
> Decía que la descomposición de reciprocidad por circuito es propia porque *«las publicaciones de análisis de red la reportan solo como una cifra global»*. **Es falso y se verificó el 24-ago (resp 057).**
>
> Lin et al. (2024) **descomponen reciprocidad**, y no en un suplementario: en la **Fig. 5c** del cuerpo (*«Reciprocity within each neuropil subnetwork»*), en la **Extended Data Fig. 6c** (*«Reciprocity **normalized by connection density** for all 78 neuropils»*, o sea **la versión por región del 36×**), en la **Fig. 5h** (mapa de pares recíprocos entre neuropilos) y con una población de **NSRNs** (neuronas altamente recíprocas específicas de neuropilo).
>
> **Lo que sobrevive, medido:** cero coocurrencias de `reciproc` con `super class`, `cell class`, `sensory neuron`, `motor neuron` o `descending` en el cuerpo de Lin. **Su partición es anatómica (78 neuropilos); la de la Table 7 es funcional y dirigida.** Son ortogonales, y así hay que decirlo. La novedad **no** es «descomponer»: es **sobre qué eje**.
>
> **BANC no reporta reciprocidad como estadístico** (2 menciones en prosa, 0 en el suplementario, contra `influence`=132 como control positivo). Pero sí dice que los módulos con alta influencia sobre efectores están unidos en *«a nearly all-to-all pattern of reciprocal connectivity»*, y eso conviene citarlo.

**Por qué existe este archivo.** El abstract publicado dice «massive reciprocity (36× over density expectation)». Ese 36× es el **mismo overflow de `int32`** que rompió la densidad (`0,266 / 0,00739526 = 35,97`), y además, corregido o no, **la magnitud global no es distintiva**: Lin et al. (2024) la encuentran comparable en **cinco** conectomas. El pivote no es aritmético. Es cambiar **qué se reclama**: de «es enorme» a **«está distribuida sobre un eje funcional, y esa distribución predice el ruteo»**.

---

## A · Versión corta, para el Abstract

Reemplaza la frase del 36×:

> Reciprocal connectivity in this connectome is high relative to degree-preserving randomizations (26.60% of edges; 20.59× the community-preserving null expectation, 0/40 nulls exceeding the observed value), but its **global magnitude is not distinctive**: applying the field-standard 5-synapse threshold yields 13.98%, in agreement with previously reported values for this and other nervous systems (Lin et al., 2024). We therefore report reciprocity **resolved along a functional axis**, over directed pairs of sensory, central, descending and motor cell classes, which spans an order of magnitude (41.3% within motor populations to 0.0% from optic lobes to motor targets) and covaries with the modality-dependent motor access described below. This axis is **complementary to the anatomical decomposition by neuropil** reported by Lin et al. (2024).

---

## B · Versión larga, para Results / Discussion

> **Reciprocity: from global excess to functionally resolved structure.**
> Across all 15,091,983 connections, 26.60% participate in reciprocal pairs (4,014,518 reciprocal edges), a value 20.59× the expectation of a community-preserving degree-matched null model, with 0 of 40 null realizations reaching the observed value. However, this global excess should not be interpreted as a distinctive feature of the *Drosophila* connectome. First, it is threshold-dependent: under the 5-synapse connection criterion adopted by Lin et al. (2024) and by Bates et al. (2026), reciprocity falls to 13.98%, closely matching the 13.8% reported by Lin et al. for snapshot v630, and mean synapses per connection falls to 12.647, matching the 12.6 reported by Dorkenwald et al. (2024). Second, and more importantly, Lin et al. (2024) show that reciprocity and clustering are **comparable across five nervous systems** of widely differing sparsity, and that over-representation of reciprocal connections in brains is well established. The informative quantity is therefore not the aggregate ratio but the **axis along which it is resolved**.
>
> **Relation to the existing decomposition.** Lin et al. (2024) already resolve reciprocity **anatomically**, reporting it within each of 78 neuropil subnetworks (their Fig. 5c), normalised by connection density per neuropil (their Extended Data Fig. 6c), and as a map of reciprocal pairs between neuropils (their Fig. 5h). We do not claim novelty for decomposing reciprocity. The decomposition reported here is **orthogonal to theirs**: it is defined over **directed pairs of functional cell classes** rather than over anatomical subnetworks, and therefore addresses a different question, namely how recurrence varies along the sensory-to-motor axis rather than across brain regions.
>
> Resolved by circuit type, reciprocity spans more than an order of magnitude: 41.3% within motor populations, 36.9% within centrifugal visual pathways, 32.0% within optic lobes, 30.7% within sensory populations, 24.2% from sensory to central circuits, 8.7% from sensory to descending neurons, 3.6% from sensory to motor targets, and 0.0% from optic lobes to motor targets. The ordering is specific: **reciprocity decreases as connections approach the motor output**, and vanishes on the pathway that our propagation analysis identifies as most strongly depleted in motor access. Recurrence is thus concentrated where signals are held and recombined, and absent where they are committed to action. A consistent ordering is recovered independently by spectral random-walk analysis in Lin et al. (2024), whose attractors localize to gnathal regions connected to the ventral nerve cord and whose repellers localize to antennal lobes and medullae, i.e. to the olfactory and visual periphery.
>
> **Relation to prior and concurrent work.** The community-preserving null used here belongs to the same family as the neuropil-connection (NPC) model of Lin et al. (2024), which constrains randomization by measured inter-neuropil connection probabilities; ours constrains by functional super-class rather than anatomical neuropil, and we do not claim the construction as novel. Bates et al. (2026) subsequently applied a linear signal-propagation model with input-fraction normalization to the combined brain and nerve-cord connectome, validating this class of method at whole-nervous-system scale (R² = 0.94 over 94,278 pairs on FAFB v783); that work reports reciprocal connectivity between high-influence CNS networks as a qualitative all-to-all pattern rather than as a network statistic, and reports a **steady-state, unsigned** influence measure. The contributions retained here are therefore the properties that such a measure cannot express: **signed propagation** with per-neuron excitatory/inhibitory identity, **transient post-stimulus dynamics**, depth-dependent inhibitory cancellation, the functionally resolved reciprocity distribution reported above, and the differential multi-hop motor coverage reported in §2.

---

## C · Qué hay que borrar cuando se pega esto

1. **«massive reciprocity (36× over density expectation)»** del Abstract. El 36× es el overflow.
2. **`Density = 0.0074`** en §2.1 → **7,85197×10⁻⁴**.
3. Cualquier frase que presente el **null CP como aporte metodológico propio** en §2.4 → angostar y citar el NPC.
4. La palabra **«motor»** sin calificar cuando la población es mayoritariamente descendente → «descending bottleneck access» o equivalente.
5. **🔴 Y en `docs/ERRATUM.md`, ítem 3:** la frase *«which the published network analyses report only as a single global figure»*. **Es falsa y ese archivo va a Zenodo.** Sin corregir al 24-ago 23:15.

## D · Referencias que este párrafo obliga a agregar

- **Lin, A., Yang, R., et al. (2024).** *Network statistics of the whole-brain connectome of Drosophila.* Nature **634**:153–165. → citar **Fig. 5c, ED Fig. 6c, Fig. 5h** para la descomposición anatómica, y el NPC model para el null.
- **Dorkenwald, S., Matsliah, A., et al. (2024).** *Neuronal wiring diagram of an adult brain.* Nature **634**:124–138.
- **Bates, A. S., et al. (2026).** Nature, doi:10.1038/s41586-026-10735-w.

## E · NO MEDIDO, que este párrafo asume y no prueba

1. **No leí la Fig. 5c ni la ED Fig. 6c de Lin fila por fila.** Sé qué miden por el pie de figura y por el texto; **no tengo sus valores**. Si algún neuropilo de Lin coincide funcionalmente con un circuito de la Table 7, el solapamiento es peor que «ortogonal».
2. Los ocho valores por circuito de la Table 7 **son con el criterio sin umbral**. No se recomputaron con umbral ≥5, así que la tabla y el 13,98% **no son directamente comparables entre sí**.
3. La palabra «specific» sobre el orden describe lo observado; **no se corrió un test de tendencia**.
4. La covariación entre reciprocidad por circuito y acceso motor **no está cuantificada** (sin correlación, sin null).
5. **No verifiqué si Lin publica la tabla numérica** de reciprocidad por neuropilo como Supplementary Data descargable. Si la publica, se puede cruzar directo y conviene hacerlo antes de mandar.
