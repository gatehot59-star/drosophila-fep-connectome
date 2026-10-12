# Párrafo pivote de reciprocidad · listo para pegar en la v2 del Paper 1

**Escrito:** 2026-08-24 · **Corregido:** 2026-08-24 23:15 tras la verificación de la resp 057.
**Actualizado:** 2026-10-12 para la v2.0 (respuesta 2026-10-12-007): sensory→descending es 8,6 y no 8,7; la Tabla 7 ya está con umbral ≥5; el orden hacia la salida queda descriptivo; el acceso motor por modalidad es co-localización tras el null anatómico. **Integrado** en `docs/v2/paper1-v2.0.md`, abstract y §3.6.
**Fuente de los números:** `docs/agents/CONTEXTO-drosophila-fep.md` §§2.bis y 3, resp 045, 050, 052, 053b, **057**; Tabla 7 con el pin `17fc577` (respuesta 2026-10-10-002, json md5 `6e395935…`).

> ## 🔴 CORRECCIÓN v2 · la versión anterior de este archivo afirmaba algo FALSO
>
> Decía que la descomposición de reciprocidad por circuito es propia porque *«las publicaciones de análisis de red la reportan solo como una cifra global»*. **Es falso y se verificó el 24-ago (resp 057).**
>
> Lin et al. (2024) **descomponen reciprocidad**, y no en un suplementario: en la **Fig. 5c** del cuerpo (*«Reciprocity within each neuropil subnetwork»*), en la **Extended Data Fig. 6c** (*«Reciprocity **normalized by connection density** for all 78 neuropils»*, o sea **la versión por región del 36×**), en la **Fig. 5h** (mapa de pares recíprocos entre neuropilos) y con una población de **NSRNs** (neuronas altamente recíprocas específicas de neuropilo).
>
> **Lo que sobrevive, medido:** cero coocurrencias de `reciproc` con `super class`, `cell class`, `sensory neuron`, `motor neuron` o `descending` en el cuerpo de Lin. **Su partición es anatómica (78 neuropilos); la de la Table 7 es funcional y dirigida.** Son ortogonales, y así hay que decirlo. La novedad **no** es «descomponer»: es **sobre qué eje**.
>
> **BANC no reporta reciprocidad como estadístico** (2 menciones en prosa, 0 en el suplementario, contra `influence`=132 como control positivo). Pero sí dice que los módulos con alta influencia sobre efectores están unidos en *«a nearly all-to-all pattern of reciprocal connectivity»*, y eso conviene citarlo.

> ## 🟠 CORRECCIÓN 2026-10-12 · dos frases de la versión anterior no aguantan
>
> 1. *«The ordering is specific»*: el test de tendencia se corrió (nulo por circuito, respuesta 2026-10-11-003) y su instrumento dio FAIL en el control negativo. La lectura preliminar es que el nulo CP reproduce la caída. **El orden se reporta como descriptivo.**
> 2. *«covaries with the modality-dependent motor access described below»*: la covariación nunca se cuantificó, y el orden del acceso motor por modalidad resultó ser co-localización de neuropilo (null anatómico, resp 063 de la rama). **Sale del abstract.**

**Por qué existe este archivo.** El abstract publicado dice «massive reciprocity (36× over density expectation)». Ese 36× es el **mismo overflow de `int32`** que rompió la densidad (`0,266 / 0,00739526 = 35,97`), y además, corregido o no, **la magnitud global no es distintiva**: Lin et al. (2024) la encuentran comparable en **cinco** conectomas. El pivote no es aritmético. Es cambiar **qué se reclama**: de «es enorme» a **«está resuelta sobre un eje funcional»**, sin reclamar que ese orden sea específico mientras el nulo por circuito no esté firmado.

---

## A · Versión corta, para el Abstract

Reemplaza la frase del 36×:

> Reciprocal connectivity (26.60% of connections; 13.98% under the field-standard five-synapse threshold, matching published values) exceeds a degree- and block-preserving null 20.59-fold (0 of 40 nulls), but its global magnitude is not distinctive across nervous systems; we report it resolved over directed pairs of functional cell classes.

---

## B · Versión larga, para Results / Discussion

> **Reciprocity: from global excess to functionally resolved structure.**
> Across all 15,091,983 connections, 26.60% participate in reciprocal pairs (4,014,518 reciprocal connections). Against 40 realizations preserving in-degree, out-degree and community block structure, the observed value ranks first of 41 (20.59× the ensemble mean; none of the 40 reaches it); against the Maslov–Sneppen ensemble the ratio is 47.27×. However, this global excess should not be interpreted as a distinctive feature of the *Drosophila* connectome. First, it is threshold-dependent: under the 5-synapse connection criterion adopted by Lin et al. (2024) and by Bates et al. (2026), reciprocity falls to 13.98%, closely matching the 13.8% reported by Lin et al. for snapshot v630, and mean synapses per connection falls to 12.647, matching the 12.6 reported by Dorkenwald et al. (2024). Second, and more importantly, Lin et al. (2024) show that reciprocity and clustering are **comparable across five nervous systems** of widely differing sparsity, and that over-representation of reciprocal connections in brains is well established.
>
> **Relation to the existing decomposition.** Lin et al. (2024) already resolve reciprocity **anatomically**, reporting it within each of 78 neuropil subnetworks (their Fig. 5c), normalised by connection density per neuropil (their Extended Data Fig. 6c), and as a map of reciprocal pairs between neuropils (their Fig. 5h). We do not claim novelty for decomposing reciprocity. The decomposition reported here is **complementary to theirs**: it is defined over **directed pairs of functional cell classes** rather than over anatomical subnetworks, and the two sets of values have not been compared region by region.
>
> Resolved by circuit type, reciprocity spans more than an order of magnitude under both criteria: without threshold, 41.3% within motor populations, 36.9% within centrifugal visual pathways, 32.0% within optic lobes, 30.7% within sensory populations, 24.2% from sensory to central circuits, 8.6% from sensory to descending neurons, 3.6% from sensory to motor targets and 0.0% from optic lobes to motor targets; under the five-synapse threshold, 35.0% (over 80 connections), 23.4%, 17.1%, 37.5%, 13.8%, 2.8% and 1.3%, with no optic-to-motor connection. Along the rows that originate in sensory neurons, reciprocity declines toward the output under both criteria. **This ordering is reported descriptively**: a per-circuit comparison against the community-preserving null was run, its preliminary reading is that the null reproduces the decline, and the instrument failed its own negative control, so no conclusion is drawn in either direction.
>
> **Relation to prior and concurrent work.** The community-preserving null used here belongs to the same family as the neuropil-connection (NPC) model of Lin et al. (2024), which constrains randomization by measured inter-neuropil connection probabilities; ours constrains by functional super-class rather than anatomical neuropil, and we do not claim the construction as novel. Bates et al. (2026) subsequently applied a linear signal-propagation model with input-fraction normalization to the combined brain and nerve-cord connectome, validating this class of method at whole-nervous-system scale (R² = 0.94 over 94,278 pairs on FAFB v783); that work reports reciprocal connectivity between high-influence CNS networks as a qualitative all-to-all pattern rather than as a network statistic, and reports a **steady-state, unsigned** influence measure. The contributions retained here are therefore the properties that such a measure cannot express: **signed propagation** with per-neuron excitatory/inhibitory identity, **transient post-stimulus dynamics**, depth-dependent inhibitory cancellation, the functionally resolved reciprocity distribution reported above, and multi-hop motor access tested against an anatomical null.

---

## C · Qué hay que borrar cuando se pega esto

1. **«massive reciprocity (36× over density expectation)»** del Abstract. El 36× es el overflow. **Hecho en la v2.0.**
2. **`Density = 0.0074`** en §2.1 → **7,85197×10⁻⁴**. **Hecho en la v2.0.**
3. Cualquier frase que presente el **null CP como aporte metodológico propio** en §2.4 → angostar y citar el NPC. **Hecho en la v2.0.**
4. La palabra **«motor»** sin calificar cuando la población es mayoritariamente descendente → **«motor output»** (1.299 descendentes, 110 motoras, 76 endocrinas). **Hecho en la v2.0.**
5. ~~**🔴 Y en `docs/ERRATUM.md`, ítem 3:** la frase *«which the published network analyses report only as a single global figure»*.~~ **Hecho:** el ítem 3 del erratum la retracta explícitamente.

## D · Referencias que este párrafo obliga a agregar

- **Lin, A., Yang, R., et al. (2024).** *Network statistics of the whole-brain connectome of Drosophila.* Nature **634**:153–165. → citar **Fig. 5c, ED Fig. 6c, Fig. 5h** para la descomposición anatómica, y el NPC model para el null.
- **Dorkenwald, S., Matsliah, A., et al. (2024).** *Neuronal wiring diagram of an adult brain.* Nature **634**:124–138.
- **Bates, A. S., et al. (2026).** *Distributed control circuits across a brain-and-cord connectome.* Nature **656**:957–970, doi:10.1038/s41586-026-10735-w.

## E · NO MEDIDO, que este párrafo asume y no prueba

1. **No leí la Fig. 5c ni la ED Fig. 6c de Lin fila por fila.** Sé qué miden por el pie de figura y por el texto; **no tengo sus valores**. Si algún neuropilo de Lin coincide funcionalmente con un circuito de la Table 7, el solapamiento es peor que «complementario».
2. ~~Los ocho valores por circuito de la Table 7 son con el criterio sin umbral.~~ **Resuelto (2026-10-10-002 y 2026-10-12-007):** la Tabla 7 está con los dos criterios y la v2.0 imprime las dos columnas.
3. **El orden «hacia la salida» no está firmado:** el nulo por circuito se corrió (respuesta 2026-10-11-003) y su instrumento dio FAIL en el control negativo; la lectura preliminar es que el nulo CP lo reproduce. Por eso la v2.0 lo reporta descriptivo.
4. **La covariación entre reciprocidad por circuito y acceso motor no está cuantificada**, y ya no se afirma: el orden del acceso motor por modalidad es co-localización de neuropilo.
5. **No verifiqué si Lin publica la tabla numérica** de reciprocidad por neuropilo como Supplementary Data descargable. Si la publica, se puede cruzar directo y conviene hacerlo antes de una v3.
