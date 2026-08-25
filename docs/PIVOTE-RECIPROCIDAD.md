# Párrafo pivote de reciprocidad · listo para pegar en la v2 del Paper 1

**Escrito:** 2026-08-24 · **Fuente de los números:** `docs/agents/CONTEXTO-drosophila-fep.md` §§2.bis y 3, resp 045, 050, 052, 053b.

**Por qué existe este archivo.** El abstract publicado dice «massive reciprocity (36× over density expectation)». Ese 36× es el **mismo overflow de `int32`** que rompió la densidad (`0,266 / 0,00739526 = 35,97`), y además, corregido o no, **la magnitud global no es distintiva**: Lin et al. (2024) la encuentran comparable en **cinco** conectomas. El pivote no es aritmético. Es cambiar **qué se reclama**: de «es enorme» a **«está distribuida de forma no uniforme, y esa distribución predice el ruteo»**.

---

## A · Versión corta, para el Abstract

Reemplaza la frase del 36×:

> Reciprocal connectivity in this connectome is high relative to degree-preserving randomizations (26.60% of edges; 20.59× the community-preserving null expectation, 0/40 nulls exceeding the observed value), but its **global magnitude is not distinctive**: applying the field-standard 5-synapse threshold yields 13.98%, in agreement with previously reported values for this and other nervous systems (Lin et al., 2024). We therefore report reciprocity **not as a global excess but as a circuit-resolved distribution**, which spans an order of magnitude across circuit classes (41.3% within motor populations to 0.0% from optic lobes to motor targets) and covaries with the modality-dependent motor access described below.

---

## B · Versión larga, para Results / Discussion

> **Reciprocity: from global excess to circuit-resolved structure.**
> Across all 15,091,983 connections, 26.60% participate in reciprocal pairs (4,014,518 reciprocal edges), a value 20.59× the expectation of a community-preserving degree-matched null model, with 0 of 40 null realizations reaching the observed value. However, this global excess should not be interpreted as a distinctive feature of the *Drosophila* connectome. First, it is threshold-dependent: under the 5-synapse connection criterion adopted by Lin et al. (2024) and by Bates et al. (2026), reciprocity falls to 13.98%, closely matching the 13.8% reported by Lin et al. for snapshot v630, and mean synapses per connection falls to 12.647, matching the 12.6 reported by Dorkenwald et al. (2024). Second, and more importantly, Lin et al. (2024) show that reciprocity and clustering are **comparable across five nervous systems** of widely differing sparsity, and that over-representation of reciprocal connections in brains is well established. The informative quantity is therefore not the aggregate ratio but its **distribution over circuit classes**, which to our knowledge has not been reported.
>
> Resolved by circuit type, reciprocity spans more than an order of magnitude: 41.3% within motor populations, 36.9% within centrifugal visual pathways, 32.0% within optic lobes, 30.7% within sensory populations, 24.2% from sensory to central circuits, 8.7% from sensory to descending neurons, 3.6% from sensory to motor targets, and 0.0% from optic lobes to motor targets. This gradient is monotonic in a specific sense: **reciprocity decreases as connections approach the motor output**, and vanishes exactly on the pathway that our propagation analysis identifies as most strongly depleted in motor access. Recurrence is thus concentrated where signals are held and recombined, and absent where they are committed to action. The same ordering is recovered independently by spectral random-walk analysis in Lin et al. (2024), whose attractors localize to gnathal regions connected to the ventral nerve cord and whose repellers localize to antennal lobes and medullae, i.e. to the olfactory and visual periphery.
>
> **Relation to prior and concurrent work.** The community-preserving null used here belongs to the same family as the neuropil-constrained (NPC) model of Lin et al. (2024), which constrains randomization by measured inter-neuropil connection probabilities; ours constrains by functional super-class rather than anatomical neuropil, and we do not claim the construction as novel. Bates et al. (2026) subsequently applied a linear signal-propagation model with input-fraction normalization to the combined brain and nerve-cord connectome, validating this class of method at whole-nervous-system scale (R² = 0.94 over 94,278 pairs on FAFB v783). That work explicitly reports a **steady-state, unsigned** influence measure. The contributions retained here are therefore the properties that such a measure cannot express: **signed propagation** with per-neuron excitatory/inhibitory identity, **transient post-stimulus dynamics**, depth-dependent inhibitory cancellation, the circuit-resolved reciprocity distribution reported above, and the exact structural exclusions reported in §2 (zero sensory→Kenyon-cell connections; zero visual and olfactory connections onto head motor neurons, despite 14 of those motor neurons projecting through the antennal nerve shared with olfactory afferents).

---

## C · Qué hay que borrar cuando se pega esto

1. **«massive reciprocity (36× over density expectation)»** del Abstract. El 36× es el overflow.
2. **`Density = 0.0074`** en §2.1 → **7,85197×10⁻⁴**.
3. Cualquier frase que presente el **null CP como aporte metodológico propio** en §2.4 → angostar y citar el NPC.
4. La palabra **«motor»** sin calificar cuando la población es 1.303 descendentes + 110 motoras → «descending bottleneck access» o equivalente.

## D · Referencias que este párrafo obliga a agregar

- **Lin, A., Yang, R., et al. (2024).** *Network statistics of the whole-brain connectome of Drosophila.* Nature **634**:153–165.
- **Dorkenwald, S., Matsliah, A., et al. (2024).** *Neuronal wiring diagram of an adult brain.* Nature **634**:124–138.
- **Bates, A. S., et al. (2026).** Nature, doi:10.1038/s41586-026-10735-w.

## E · NO MEDIDO, que este párrafo asume y no prueba

1. **Si Lin reporta reciprocidad por tipo de circuito en su suplementario.** Si lo hiciera, se cae el pedazo propio de la parte B. **Sin verificar.**
2. **Si BANC reporta reciprocidad por circuito.** Sin verificar.
3. Los ocho valores por circuito de la Table 7 **son con el criterio sin umbral**. No se recomputaron con umbral ≥5, así que la tabla y el 13,98% **no son directamente comparables entre sí**.
4. La palabra «monotonic» describe el orden observado; **no se corrió un test de tendencia**.
5. La covariación entre reciprocidad por circuito y acceso motor **no está cuantificada** (sin correlación, sin null).
6. «to our knowledge has not been reported» es una afirmación de ausencia **no barrida en la literatura**.
