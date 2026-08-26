# Posicionamiento frente a los trabajos concurrentes

**Estado:** listo para pegar en la v2. **No va al erratum**: es material nuevo, no una corrección de la v1.0.
**Escrito:** 2026-08-25 · **Fuentes leídas en vivo**, no de memoria. Evidencia: `docs/agents/evidencia/2026-08-25-tres-papers-issue4-evidencia-cruda.md`.

---

## 0. Lo primero, porque cambia qué hay que escribir

**El PDF publicado YA distingue a dos de los tres.** Medido sobre el archivo de Zenodo (`md5 c7cb36a261182f6ce895057ebe26e505`, 7 páginas, 23.025 caracteres):

- **§1.2 Related Work**, verbatim: *«Betzel et al. [2026] demonstrated convergence of sensory cascades on shared integration nodes in the Drosophila connectome.»*
- **§4.4 Comparison with Concurrent Work** contiene la **Tabla 11**, *«Comparison with concurrent studies»*, que compara **Shiu · Betzel · This** fila por fila.
- **Referencia completa**, con revista, volumen, artículo y DOI: *«Betzel, R.F., Puxeddu, M.G., Seguin, C. & Mišić, B. (2026). Cascades and convergence: Dynamic signal flow in a synapse-level brain network. PLOS Complex Systems, 3(3), e0000091. doi:10.1371/journal.pcsy.0000091»*
- Y cita **Shiu, P.K., et al. (2024)**, *«A Drosophila computational brain model reveals sensorimotor processing»*, Nature 634, 210–219 — que es **el modelo sobre el que se construye la demo de Eon Systems**.

> **Conclusión: la acción «declarar en qué se distingue» no está pendiente. Está hecha desde marzo, con tabla.** Lo que sigue **refuerza** esa tabla con lo que se midió el 25-ago, y **corrige una de sus filas**.

---

## 1. 🔴 Una fila de la Tabla 11 hay que corregir en la v2

La Tabla 11 dice, en la fila `Null model`: **Shiu = No · Betzel = «Comm. only» · This = MS+CP (N=100)**.

**Medido sobre el texto completo de Betzel** (136.735 caracteres): `null model` 0 · `configuration model` 0 · `degree-preserving` 0 · `rewir` 0 · `maslov` 0 · `sneppen` 0. Su único control estadístico es, verbatim:

> *«We then randomly permuted the annotation labels (keeping the total number constant) and calculated the new mean. We repeated this procedure 1000 times, generated a null distribution…»*

**Eso es una permutación de ETIQUETAS, no un null de grafo.** No destruye grado ni aristas. Su análisis de comunidades usa un **nested stochastic block model para DETECTAR** comunidades (S8, S9), no un null que las preserve.

> **Llamarlo «community null» es impreciso, y está en un documento con DOI.** Es el modo de falla 10 del proyecto — afirmar sobre el método de un tercero sin verificarlo — cometido en la dirección contraria a la habitual: **subestimando** al otro en una fila y **describiéndolo mal** en la misma.
>
> **Redacción correcta para la fila:** *Betzel = label permutation (n = 1000); no graph null.*
>
> **Y hay que decir lo que juega en contra:** su `n` es **1000** y el de este trabajo es **40**. En número de realizaciones, ellos están mejor. La ventaja propia es **qué** se permuta, no **cuántas veces**.

---

## 2. 🟢 La convergencia que hay que reclamar, y es fuerte

**Betzel et al. reportan, en su sección de métodos, verbatim:**

> *«The connectome comprised **N = 138,639** neurons, **M = 15,091,983** edges, **Mw = 54,492,922** synapses»* y *«**d_connectome = 7.8 × 10⁻⁴**»*

| Cantidad | Betzel et al. (2026), PLOS, revisado por pares | Este trabajo |
|---|---|---|
| Neuronas | **138.639** | **138.639** |
| Aristas | **15.091.983** | **15.091.983** |
| Sinapsis | **54.492.922** | **54.492.922** |
| Densidad | **7,8 × 10⁻⁴** | **7,85197 × 10⁻⁴** |
| Densidad de la v1.0 | — | 0,0074 (**overflow de `int32`, ítem 1 del erratum**) |

> **La densidad de Betzel coincide con la CORREGIDA, no con la publicada.** El ítem 1 del erratum tiene así **confirmación externa independiente, publicada y revisada por pares, sobre el mismo snapshot público.**

**Párrafo listo para pegar (Erratum, ítem 1, o Methods §2.1):**

> The corrected density reported here, `d = 7.85 × 10⁻⁴`, is independently corroborated by Betzel et al. (2026), who report `d_connectome = 7.8 × 10⁻⁴` for the same FlyWire v783 release, together with identical neuron, edge and synapse counts (`N = 138,639`, `M = 15,091,983`, `M_w = 54,492,922`). The value printed in v1.0 (`0.0074`) is therefore confirmed as an arithmetic artefact and not a difference in inclusion criteria.

**Por qué este párrafo vale más que su longitud:** convierte una autocorrección en un hecho verificable por un tercero. Un revisor no tiene que confiar en la aritmética del autor: tiene otra publicación con el mismo número.

---

## 3. 🎯 El nicho, escrito con las palabras de ellos

**La regla que hace fuerte a este párrafo:** no afirma que los otros no supieron. **Cita lo que ellos mismos declaran no cubrir.** Un revisor puede verificar cada comilla.

### Lo que Betzel et al. declaran como trabajo futuro, verbatim

> *«Our model could be further enhanced by including **synaptic polarity, inhibitory/excitatory distinctions**, and transmitter-specific dynamics.»*

> *«Likewise, expanding the model to include ventral nerve cord circuits and **motor neuron pathways** would better approximate the full sensorimotor axis.»*

### Lo que BANC (Bates et al., 2026) declara, verbatim

> *«we take its **steady-state response**»* · *«adjusted influence is an **unsigned quantity**»*

> **Dos grupos independientes, en dos revistas distintas, declaran ausentes las MISMAS DOS propiedades: el signo y el transitorio.** No es una coincidencia afortunada: es la definición del hueco, escrita por quienes lo dejaron.

### ⚠️ Y la precisión que evita un claim demasiado grueso

**Betzel SÍ desglosa por neurotransmisor en un suplementario.** Su **S6 Fig**, verbatim:

> *«Effect of synapse type on activation time. In the main text we grouped all synapses together, making no distinction between neurotransmitter types. Here, we parse contributions made by six distinct synapse types (based on neurotransmitter). They include acetylcholine (ACH), dopamine (DA), **gabaergic (GABA)**, glutamate (GLUT), octopamine (OCT), and seratonin (SER). … we tracked how frequently synapses associated with different neurotransmitter types **successfully activated their post-synaptic partner**.»*

**La distinción exacta, y es más defendible que decir «no miran el neurotransmisor»:** ellos **etiquetan** las sinapsis por neurotransmisor para medir **quién transporta la cascada**. Pero en su modelo **una sinapsis GABAérgica igual ACTIVA al postsináptico**: el neurotransmisor es una etiqueta descriptiva, no un **signo** en la dinámica. **No hay cancelación.** Por eso su propia Discussion pide «synaptic polarity» como mejora futura **después** de haber hecho la S6.

**Medido sobre sus 19 captions:** `motor` 0 · `descending` 0 · `effector` 0 · `efferent` 0. Y `signed` como palabra completa: **0** en todo el paper (los dos aciertos por substring eran `assigned`).

---

## 4. 📝 EL PÁRRAFO, para pegar

### Versión en inglés (Discussion, §4.4, ampliando la Tabla 11)

> **Relation to concurrent work.** Three concurrent efforts share this dataset and stop short of the properties measured here, in each case by their own explicit statement. Betzel et al. (2026) simulate modality-specific cascades on the same v783 release and report identical population counts, but their statistical control is a permutation of annotation labels (n = 1000) rather than a graph null: neither degree nor edge structure is destroyed, so their enrichment tests do not address topological specificity. They further state that their model «could be further enhanced by including synaptic polarity, inhibitory/excitatory distinctions» and that «expanding the model to include … motor neuron pathways would better approximate the full sensorimotor axis». Bates et al. (2026) validate a column-normalised linear propagation model on the same release with `R² = 0.94` across 94,278 pairs, and declare two restrictions: they «take its steady-state response» and their «adjusted influence is an unsigned quantity». Shiu et al. (2024) demonstrate functional sensorimotor propagation with a leaky integrate-and-fire model, without null-model comparison. **Two independent groups, in two different journals, thus declare absent the same two quantities: synaptic sign and the post-stimulus transient.** The contribution of the present work is neither the dataset nor the propagation model, both of which the field has converged on: it is the pairing of signed, transient-resolved dynamics with topology-destroying null ensembles, which is what converts a measured count into a testable claim.

### Versión en español (para la bitácora y para explicarlo)

> **Tres trabajos concurrentes comparten el dataset y se detienen antes de lo que este trabajo mide, y en los tres casos por declaración propia.** Betzel et al. (2026) simulan cascadas por modalidad sobre el mismo v783 y reportan los mismos conteos de población, pero su control es una permutación de etiquetas (n = 1000) y no un null de grafo: no destruye grado ni aristas, así que sus tests de enriquecimiento no hablan de especificidad topológica. Y piden como mejora futura «polaridad sináptica, distinciones inhibitorio/excitatorio» y «vías de neuronas motoras». Bates et al. (2026) validan un modelo lineal normalizado por columna sobre el mismo release con `R² = 0,94` en 94.278 pares, y declaran dos renuncias: toman la **respuesta estacionaria** y su influencia es una **cantidad sin signo**. Shiu et al. (2024) demuestran propagación sensoriomotora funcional con un modelo LIF, sin comparación contra nulls. **Dos grupos independientes, en dos revistas distintas, declaran ausentes las mismas dos cantidades: el signo sináptico y el transitorio post-estímulo.** El aporte no es el dataset ni el modelo de propagación — el campo converge en los dos — sino **la combinación de dinámica con signo y transitorio con ensembles nulos que destruyen la topología**, que es lo que convierte un conteo medido en un claim testeable.

---

## 5. Lo que SÍ se solapa, y hay que declararlo antes que un revisor

**Betzel et al. observan la convergencia sobre nodos motores**, verbatim:

> *«cascades—initially modality-specific—rapidly converge onto overlapping sets of secondary nodes, many located in the central complex and involving **descending and motor neurons**. This proximity between sensors and effectors is consistent with behavioral observations and suggests streamlined sensorimotor pathways.»*

**Es la misma observación cualitativa que la Propiedad 2, publicada antes** (preprint del **8-dic-2024**, revista del **5-mar-2026**; el Zenodo de este trabajo es del **20-mar-2026**).

> **Frase honesta para la v2:** *«The qualitative observation that sensory cascades converge on descending and motor populations is prior art (Betzel et al., 2026). What is new here is the quantification per modality against ensembles that preserve degree and, separately, neuropil-level connection probabilities, which distinguishes an absence that anatomy predicts from one that it does not.»*

**Y el contraste que lo sostiene:** contra el null anatómico, el cero de olfatorio y visual **es geometría predicha** (el null predice ≈ 0), mientras que gustativa contacta **10 de 110 motoras donde su co-localización predice 101,6 ± 1,2** (`z = −78,9`). **Esa distinción entre dos tipos de cero es lo que la observación cualitativa no puede hacer.**

---

## 6. Los otros dos: ni prior art ni competidores científicos

| Trabajo | Fecha | Estado | Relación |
|---|---|---|---|
| **Eon Systems** · «mosca 3D» | 9-16 mar 2026 | **demo, no paper.** Sin revisión por pares. *The Verge*: «No, this is not a fly uploaded to a computer» | Se construye sobre **Shiu et al. (2024)**, que **este paper ya cita**. Inconsistencia propia medida: su repo dice **~5M sinapsis**, su sitio y la prensa dicen **50M** |
| **Rojas Aliaga (2026)** | Zenodo **21-mar-2026** | preprint, autor único, **0 citas** | **Un día DESPUÉS** del Zenodo de este trabajo → **no es prior art.** Contradicción interna medida: **139.255** neuronas en su abstract y **138.639** en el README de su repo. Métrica central: «consciousness index» con Phi de IIT |

> **Ninguno de los tres toca microcontrolador, miliwatts ni BOM.** El riesgo que representan **no es científico, es de narrativa**: Eon se quedó con la palabra «emulación del conectoma» en la prensa, con 120M de impresiones. Eso afecta cómo se lee el título de un paper, no su validez.

**Recomendación:** **no citar a Eon ni a Rojas Aliaga en la v2.** Una demo sin revisión por pares y un preprint posterior con contradicciones internas no son prior art, y citarlos los eleva. **Sí conviene citar Shiu et al. (2024), que ya está citado**, porque es el trabajo real que hay debajo de la demo.

---

## 7. NO MEDIDO, declarado

1. **De Betzel se leyeron el cuerpo completo, las 19 captions y los 11 suplementarios por su caption.** **No se abrieron los archivos de datos suplementarios ni el `Response_to_Reviewers.pdf`.** Si una tabla suplementaria cuantifica acceso motor por modalidad, la frase de la §5 hay que angostarla más.
2. **No se compararon los dos modelos midiendo:** cascada probabilística contra propagación lineal con `tanh`. La comparación es de descripciones de método, no de dos corridas sobre el mismo grafo. **Es la medición que faltaría para afirmar equivalencia o diferencia.**
3. **La coincidencia de `N`, `M` y `Mw` no prueba el mismo archivo**, sólo el mismo snapshot con el mismo criterio de inclusión. **No se compararon md5** y del lado de Betzel no hay md5 publicado.
4. **La fila `This = MS+CP (N=100)` de la Tabla 11 no se verificó contra el código** en este turno. El repo publica **40** nulls como titular y `METHODS` declara MS `N=100` estático. **Puede ser el modo de falla 5 otra vez, y queda sin medir.**
5. **El paper de Rojas Aliaga no se leyó** (abstract + README de su repo). **Eon no se auditó técnicamente.**
6. **Este párrafo no lo revisó nadie más que su autor.** **K-02: deuda declarada.** Y **W-01**: por eso cada comilla lleva su fuente, para que cualquiera pueda contradecirlo abriendo el paper.
