# EVIDENCIA CRUDA · los tres papers del issue #4

**Fecha:** 2026-08-25 10:30 (America/Buenos_Aires)
**Instrumento:** `gateway build.run` sobre `brain-env`, 5 corridas. `search_web` × 3. Lectura del issue #4 vía integración.
**Sujetos:** issue #4 de este repo (creado 25-ago 13:11 UTC) y su único comentario (13:12 UTC).

---

## 0. Dónde estaban, y por qué los busqué mal la primera vez

El turno anterior buscó «tres documentos de Tachi» en `mudh-mobile` y encontró tres archivos reales (HANDOFF + dos versiones de un informe). **Eran otros.** Los que Abraham señalaba están **en este repo, en el issue #4**, que se creó a las **13:11 UTC**, o sea **mientras yo escribía la resp 079**.

**Barrido antes de dar por buena la ubicación:**

```
diff de arboles de archivos entre ramas:
  main 113   auditoria 136   twohop 148
  SOLO EN RAMA AUDITORIA: docs/agents/respuestas/2026-08-25-072-auditoria-integra-titan.md
  (ningun archivo nuevo con links de papers en ninguna rama)

issues del repo: totalCount = 1
  #4  OPEN  2026-08-25T13:11:30Z  "Competidor directo detectado: PLOS Cascades and convergence..."
      comments = 1   updated 13:12:58Z
```

**Los tres links: el PLOS en el cuerpo, y Eon Systems + Rojas Aliaga en el comentario.**

---

## 1. 🔥 DOI resueltos en vivo, con control negativo

```
=== DOI 1: el PLOS que el issue llama competidor ===
HTTP=200
TITULO: Cascades and convergence: Dynamic signal flow in a synapse-level brain network
REVISTA: PLOS Complex Systems
VOL 3 ISSUE 3 ART None
AUTORES: Betzel R, Puxeddu M, Seguin C, Misic B
PUBLICADO: [[2026, 3, 5]]
CITAS_CROSSREF: 0

=== DOI 2: el preprint del mismo paper ===
HTTP=200
TITULO: Cascades and convergence: dynamic signal flow in a synapse-level brain network
TIPO: posted-content
POSTED: [[2024, 12, 8]]  CREATED: 2024-12-08T23:50:12Z

=== DOI 3: Rojas Aliaga ===
HTTP=200  (devuelve HTML del record de Zenodo, no JSON de Crossref)

=== CONTROL NEGATIVO: un DOI que NO existe ===
HTTP_doi_falso=404
```

**El control discrimina** (404 sobre `10.1371/journal.pcsy.9999999`), así que los 200 valen.

> ## 🔴 **`Betzel R, Puxeddu M, Seguin C, Misic B` + `PLOS Complex Systems 3(3)` = la referencia que el `CONTEXTO` tenía en NO MEDIDO ítem 7 desde el 24-ago:** *«verificaciones externas pendientes: … y **Betzel** (PLOS Complex Systems 3(3), e0000091)»*. **Y el `§1.2` del Paper 1 YA LO CITA.**
>
> **El «competidor directo recién detectado» es una verificación que yo debía y no hice.**

**Y la fecha:** el preprint es del **8-dic-2024**, no del 5-mar-2026. **15 meses y 12 días antes** del Zenodo del 20-mar-2026, no 15 días. El issue leyó la fecha de la revista.

---

## 2. 🔥🔥 Su sección de métodos, verbatim, y es el hallazgo del turno

Texto completo bajado: **272.668 bytes de XML → 136.735 caracteres de texto.**

```
---[v783] ...used the connectome of a single adult female Drosophila melanogaster (publicly
available through https://codex.flywire.ai/ ; all analyses were carried out on the v783
connectome) [35]. The connectome comprised N = 138 , 639 neurons, M = 15 , 091 , 983 edges,
M w = 54,492,922 synapses. The connectome is, by construction, di...

---[binar] ...We extracted the 16349 x 16349 subgraph comprising all synaptic connections between
sensory neurons (Fig 2a). This subgraph was notably sparse, with a binary connection density
of d_sensory = 1.3 x 10-4 - approximately six times lower than the full connectome's density
( d_connectome = 7.8 x 10-4...
```

| Cantidad | Betzel et al. (PLOS, revisado por pares) | El Paper 1 / este repo |
|---|---|---|
| Neuronas `N` | **138.639** | **138.639** |
| Aristas `M` | **15.091.983** | **15.091.983** |
| Sinapsis `Mw` | **54.492.922** | **54.492.922** |
| Densidad | **7,8 × 10⁻⁴** | **7,85197 × 10⁻⁴** (la **corregida** del erratum) |
| Densidad publicada en v1.0 | — | 0,0074 (**el overflow**) |

> **Los tres conteos coinciden AL DÍGITO, y la densidad de Betzel coincide con la CORREGIDA, no con la publicada.**

**Consecuencia para el erratum:** el ítem 1 (densidad 0,0074 → 7,85×10⁻⁴ por overflow de `int32`) **tiene validación externa independiente, publicada, con revisión por pares y cuatro autores humanos, sobre el mismo snapshot.** Ya no depende de que alguien crea mi aritmética.

**Y responde el hallazgo 6 de Tachi** («la auditoría es circular, el auditor es del mismo ecosistema»): **esta sí es externa al ecosistema, y confirma.** Es la primera. No la produjo ni Tao, ni Tachi, ni yo.

---

## 3. Lo que Betzel NO hace · conteos sobre su texto completo

```
  TERMINO             CONTEO
  null model              0
  configuration model     0
  degree-preserving       0
  rewir                   0
  maslov                  0
  sneppen                 0
  permut                  3
  z-score                 4
  sign (aislado)          0        <- refinado con \bsigns?\b
  signed                  0
  inhibitor               2
  excitator               4
  gaba                    2
  neurotransmitter       10
  transient               1
  post-stimulus           0
  steady state            0
  steady-state            0
  decay                   0
  tau                     0
  motor neuron            2
  descending              4
  reciproc                1
  flywire                 7
  v783                    1
  threshold              15
  binary                  5
  synaptic weight         1
  unweighted              0
  spreading              19
  cascade               195
  zzqqxx                  0        <- CONTROL NEGATIVO
```

**El control negativo da 0 y los positivos dan alto**, así que el conteo mide.

⚠️ **Refinamiento que evitó un falso positivo:** `sign` como substring daba **60**, y con `\bsigns?\b` da **0**. Los 60 eran `signal`, `significant` y `design`. **Sin ese refinamiento, el veredicto «sin signo» se habría invertido por un artefacto de substring.** Es el modo de falla 6 en versión `grep`.

### Su único null, verbatim

```
---[permut] ...standardized against a null distribution obtained by permuting labels (Fig 4i)...
---[permut] ...We then randomly permuted the annotation labels (keeping the total number constant)
and calculated the new mean. We repeated this procedure 1000 times, generated a null
distribution o...
```

**Permuta ETIQUETAS DE ANOTACIÓN, no topología.** Es un null de **atributos**, no de estructura: no destruye ni el grado ni las aristas. **Familia distinta a los 40 nulls de este repo, y más débil para el claim estructural.** Tienen 1000 realizaciones y este repo tiene 40; **la comparación de `n` es a favor de ellos y hay que decirlo.**

### Y las tres renuncias que declaran como trabajo futuro, verbatim

```
---[excitatory] ...Our model could be further enhanced by including synaptic polarity,
inhibitory/excitatory distinctions, and transmitter-specific dynamics. For instance,
connectome-informed weight estimates often disagree with simply assuming synapse count
correspon...

---[motor neuron] ...expanding the model to include ventral nerve cord circuits and motor neuron
pathways would better approximate the full sensorimotor axis...

---[motor neuron] ...cascades - initially modality-specific - rapidly converge onto overlapping sets of
secondary nodes, many located in the central complex and involving descending and motor
neurons. This proximity between sensors and effectors is consistent with behavioral
observations and suggests streamlined sensorimotor pathways. Of course, the simpli...
```

| Lo que el Paper 1 mide | Betzel |
|---|---|
| **Signo** (cancelación GABAérgica) | **0 menciones aisladas.** Declarado como mejora futura |
| **Transitorio post-estímulo** | **0 menciones.** Sin `tau`, sin `decay`, sin `steady state` |
| **Vía motora diferencial** | **declarada como trabajo futuro** verbatim |
| **Nulls que destruyen topología** | **0.** Su null permuta etiquetas |

> **Es la SEGUNDA vez, con BANC, que el campo llega al mismo método y se detiene exactamente donde empieza el aporte propio.** Dos veces no es suerte: **el nicho está descrito por lo que los otros declaran no cubrir.**

**⚠️ Y el solapamiento que SÍ existe y hay que declarar:** su tercera frase de arriba dice que las cascadas convergen en nodos con **descending y motor neurons**, y que eso sugiere vías sensoriomotoras «streamlined». **Es la misma observación cualitativa que la Propiedad 2**, hecha antes, aunque **sin null estructural y sin cuantificar por modalidad contra un control.**

---

## 4. Los otros dos, medidos y acotados

### Eon Systems · la «mosca 3D»

- **No es un paper:** es una demo con cobertura de prensa (9-16 mar 2026, +120M impresiones), y **The Verge publicó una desmentida de framing** (*«No, this is not a fly uploaded to a computer»*, 16-mar).
- **Se apoya en Shiu et al. (Nature 2024)**, un modelo **LIF** del cerebro completo, más cuerpo en **MuJoCo**. Repo `eonsystemspbc/fly-brain`, 330 estrellas, creado **5-mar-2026**.
- **Inconsistencia de ellos, medida:** el repo dice **«~138k neuronas, ~5M sinapsis»** y la prensa y su propio sitio dicen **50M**. Factor 10 entre su README y su comunicación.
- **Su sitio declara 139.255 neuronas**, no 138.639: **otro snapshot o otro criterio de inclusión.**

### Rojas Aliaga (2026) · «Embodied Drosophila»

- Zenodo, **21-mar-2026** (**un día después** del Zenodo de Mendieta), **0 citas**. Autor único: Enrique Manuel Rojas Aliaga, USMP, Lima.
- **Contradicción interna medida:** el **abstract dice 139.255 neuronas y 54,5M sinapsis**; el **README de su repo dice 138.639**. **Dos números distintos para el mismo grafo en la misma entrega.**
- Su métrica central es un **«consciousness index»** que combina **Phi de IIT**, global workspace y complejidad, con «peak CI de 0,31». **Eso ubica el rigor**, y no hay revisión por pares.
- **Comparte scope de producto** (LIF + GPU + cuerpo biomecánico), **no de sustrato**: no hay embebido ni consumo.

---

## 5. NO MEDIDO, declarado

1. **Del PLOS leí el texto completo pero NO sus figuras ni sus suplementarios.** Los conteos de términos cubren el cuerpo; **si una figura cuantifica acceso motor por modalidad, el veredicto «no lo miden» se debilita.** Es exactamente el modo de falla 10 de este repo, y queda **declarado, no cerrado**.
2. **No se comparó su modelo de spreading contra el modelo lineal del Paper 1 midiendo.** La comparación es de descripción de métodos, no de dos corridas.
3. **El paper de Rojas Aliaga NO se leyó**: sólo su abstract y el README de su repo. Su contradicción de `N` sale de comparar esos dos, no de leer su código.
4. **Eon no se auditó técnicamente:** no se leyó su repo ni se corrió nada. La inconsistencia 5M/50M sale de su propio README contra su propio sitio.
5. **No se verificó cómo cita el Paper 1 a Betzel en su §1.2**: el PDF no se abrió en este turno. **Sé que lo cita porque lo dice el contexto, que es mi propia nota.** Si la cita está incompleta o mal atribuida, **eso es el modo de falla 9 y no está medido.**
6. **No se abrió ningún comentario en el issue #4.** Cerrar el lazo con Tachi requiere el OK de Abraham.
7. **La coincidencia de N, M y Mw no prueba que usen el mismo archivo**, sólo el mismo snapshot público con el mismo criterio de inclusión. **No se compararon md5.**
