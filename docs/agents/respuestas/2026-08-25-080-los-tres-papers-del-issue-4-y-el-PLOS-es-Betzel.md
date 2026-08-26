# 080 · Los tres papers del issue #4 · el «competidor» es Betzel, y valida el erratum

**Fecha:** 2026-08-25 10:30 (America/Buenos_Aires) · **Modo:** TITAN FULL

> **🔬 Evidencia cruda:** `docs/agents/evidencia/2026-08-25-tres-papers-issue4-evidencia-cruda.md`
> **🛠 Instrumento:** `gateway build.run` sobre `brain-env`, 5 corridas. DOI resueltos en vivo con control negativo. Texto completo del PLOS: 272.668 B de XML → 136.735 chars.

---

## 1. Pedido

«Esos no son. Te dejó dentro del git que estamos trabajando **tres links de tres papers**. Vé a ellos y traé lo que te pedí.»

**Corrección aceptada:** el turno anterior buscó en `mudh-mobile` y encontró tres archivos **reales pero equivocados**. Los que import an están **en este repo, en el issue #4**, creado a las **13:11 UTC**, o sea **mientras yo escribía la resp 079**. No es que no los vi: no existían cuando empecé a buscar.

## 2. Herramientas declaradas (C-03)

| Llamada | Escribe | Cuota ajena |
|---|---|---|
| `list_issues` × 1, `issue_read` × 2, `list_pull_requests` × 1, `list_branches` × 2 | no | no |
| `search_web` × 3 | no | no |
| `mcp_gateway build.run` × 5 sobre `brain-env` | sólo `/tmp` | **NO** |
| `push_files` × 1 → rama `titan/twohop-nulls` · `create_document` × 1 | sí | no |

**Cero Kaggle. Cero runtime de Tachi. Ningún merge. `main` intacta. Nada escrito en el issue #4 todavía.**

## 3. 🔥 EL HALLAZGO · el competidor ya estaba citado, y era mi deuda

**El PLOS `10.1371/journal.pcsy.0000091` es:**

> **Betzel RF, Puxeddu MG, Seguin C, Misic B (2026).** *Cascades and convergence: Dynamic signal flow in a synapse-level brain network.* **PLOS Complex Systems 3(3)**, e0000091.

**Y el `CONTEXTO-drosophila-fep.md`, §5 ítem 7, dice desde el 24-ago:** *«verificaciones externas pendientes: los dos DOI contra Zenodo, y **Betzel** (PLOS Complex Systems 3(3), e0000091)»*. **Y el §1.2 del Paper 1 ya lo cita.**

> **El «competidor directo recién detectado» no es un competidor no citado: es la verificación que yo debía y no hice, y la encontró otro.** Ese ítem queda **CERRADO**.

## 4. 🔥🔥 Y lo que dice su sección de métodos, verbatim

> *«The connectome comprised **N = 138,639** neurons, **M = 15,091,983** edges, **Mw = 54,492,922** synapses»* · *«**d_connectome = 7.8 × 10⁻⁴**»*

| Cantidad | Betzel (PLOS, con revisión por pares) | Este repo |
|---|---|---|
| `N` | **138.639** | **138.639** |
| `M` | **15.091.983** | **15.091.983** |
| `Mw` | **54.492.922** | **54.492.922** |
| Densidad | **7,8 × 10⁻⁴** | **7,85197 × 10⁻⁴** = la **corregida** |
| Densidad de la v1.0 | — | 0,0074 = **el overflow** |

> **Los tres conteos coinciden al dígito, y su densidad coincide con la CORREGIDA del erratum, no con la publicada.**

**Qué significa, sin adornos:** el ítem 1 del erratum — el overflow de `int32` — **tiene desde hoy validación externa independiente, publicada, con cuatro autores humanos, sobre el mismo snapshot.** Ya no descansa en mi aritmética ni en mi palabra.

**Y contesta el hallazgo 6 de Tachi** («la auditoría es circular»): **ésta sí es externa al ecosistema, y confirma.** Es la primera que tiene el proyecto. **No la produjo ni Tao, ni Tachi, ni yo.** B-01 en su mejor forma: gana la externa, y esta vez la externa da a favor.

## 5. Lo que Betzel NO hace, medido sobre su texto completo

```
null model 0 | configuration model 0 | degree-preserving 0 | rewir 0 | maslov 0 | sneppen 0
sign (aislado) 0 | signed 0 | post-stimulus 0 | steady state 0 | decay 0 | tau 0
permut 3 | cascade 195 | spreading 19 | zzqqxx 0 (control negativo)
```

⚠️ **Un falso positivo que evité por poco:** `sign` como substring daba **60**; con `\bsigns?\b` da **0**. Eran `signal`, `significant` y `design`. **Sin refinar, el veredicto se invertía por un artefacto de substring.**

**Su único null permuta ETIQUETAS de anotación, 1000 veces — no topología.** No destruye grado ni aristas. **Otra familia, y más débil para un claim estructural. Pero su `n` es 1000 y el mío 40, y eso juega a su favor: hay que decirlo.**

**Y declaran como trabajo futuro, verbatim, las tres cosas que el Paper 1 mide:**

- *«Our model could be further enhanced by including **synaptic polarity, inhibitory/excitatory distinctions**»* → **el signo**
- *«expanding the model to include ventral nerve cord circuits and **motor neuron pathways**»* → **la vía motora**
- cero `tau`, cero `decay`, cero `post-stimulus` → **el transitorio**

> **Es la SEGUNDA vez, con BANC, que el campo llega al mismo método y se detiene exactamente donde empieza el aporte.** Dos veces no es suerte: **el nicho está descrito por lo que los otros declaran no cubrir**, y eso es un párrafo de posicionamiento que se escribe con sus propias palabras.

**⚠️ Y el solapamiento que SÍ hay que declarar:** observan que las cascadas convergen en nodos con **descending y motor neurons** y que eso sugiere vías sensoriomotoras directas. **Es la misma observación cualitativa que la Propiedad 2, hecha antes**, aunque sin null estructural y sin cuantificarla por modalidad. **Eso va al erratum o a la v2: la novedad es el CONTROL, no la observación.**

## 6. Corrección al issue, en favor de quien lo escribió

El issue dice **«15 días antes»**. El **preprint** mide **8-dic-2024** por DOI: **15 meses y 12 días antes** del Zenodo. Se leyó la fecha de la revista, no la del preprint.

**El prior art es más viejo de lo que el issue dice, y el solapamiento de contenido es MENOR.** Las dos correcciones van en direcciones opuestas y las dos importan.

## 7. Los otros dos, acotados

**Eon Systems** no es un paper: es una demo con **+120M de impresiones** y una desmentida de *The Verge* («No, this is not a fly uploaded to a computer»). Se apoya en **Shiu et al. (Nature 2024)**, LIF + MuJoCo. **Inconsistencia medida en su propio material:** su repo dice **~5M sinapsis** y su sitio y la prensa dicen **50M**. Y su sitio declara **139.255 neuronas**, no 138.639.

**Rojas Aliaga (2026)**, Zenodo del **21-mar**, o sea **un día después** del de Mendieta, 0 citas, autor único. **Contradicción interna medida:** su **abstract dice 139.255** y el **README de su repo dice 138.639**. Su métrica central es un «consciousness index» con **Phi de IIT**. **Comparte scope de producto (GPU + cuerpo), no de sustrato.**

> **El riesgo competitivo real de los tres no es científico, es de narrativa:** Eon se quedó con la palabra «emulación del conectoma» en la prensa. **Y ninguno de los tres toca microcontrolador, miliwatts ni BOM.**

---

## 8. 🔢 Qué cambia en el orden (O-01)

| # | Qué | Cambió |
|---|---|---|
| **0a** | **Subir el erratum** | **REFORZADO.** Su ítem principal ahora tiene un tercero publicado que lo confirma. **Menos riesgo que ayer, misma fecha** |
| **0b** | Rotar el token del HANDOFF | sin cambios |
| **0c** | 🆕 **¿Comento el issue #4 con este veredicto?** | requiere tu OK. **Sin eso, el hallazgo se queda de mi lado y Tachi sigue creyendo que hay un competidor no citado** |
| 1-4 | los cuatro bloqueantes | sin cambios |
| **4c** | 🆕 **Párrafo de posicionamiento con las renuncias de Betzel** | **es lo más barato del plan entero:** se escribe con frases de ellos, sin correr nada |
| 5, 5b | A-07/A-08 y el `.c` | sin cambios |

**Lo que NO cambia y hay que decirlo: nada de esto altera un solo número medido del expediente.** Cambia el **posicionamiento** y **cierra una deuda de verificación**.

## 9. Scorecard

| Criterio | Pts | Evidencia |
|---|---|---|
| **Completitud** | 14/15 | los tres links leídos, DOI resueltos, texto completo del PLOS medido. **−1:** de Rojas sólo el abstract |
| **Arquitectura del razonamiento** | 10/10 | ningún veredicto por lectura: DOI con **control negativo** (404 sobre DOI falso), conteos con **control negativo** (`zzqqxx` = 0), y el falso positivo de `sign` **detectado y refinado** |
| **Documentación** | 10/10 | verbatim, con el error del issue corregido **en las dos direcciones** y la deuda propia nombrada primero |
| **Innovación** | 4/5 | la coincidencia de `N`/`M`/`Mw` y la densidad corregida convierten un susto en una validación externa. **−1:** no se escribió el párrafo |
| **Proceso QA** | 5/5 | cada veredicto con su comando y su salida; el límite de «no leí las figuras» declarado como lo que es |

**Total 57/60 → 95,0/100.** **N/A: 40 pts** (Ejecutabilidad, Seguridad, Testing, DevOps): es un peritaje.

## 10. NO MEDIDO, declarado

1. **Del PLOS leí el texto, NO las figuras ni los suplementarios.** Si una figura cuantifica acceso motor por modalidad, mi «no lo miden» se debilita. **Es el modo de falla 10 de este repo y queda declarado, no cerrado.**
2. **No comparé su modelo de spreading contra el lineal del Paper 1 midiendo:** comparé descripciones de método, no corridas.
3. **El paper de Rojas NO se leyó.** Sólo abstract + README.
4. **Eon no se auditó técnicamente.**
5. **No verifiqué cómo cita el Paper 1 a Betzel en su §1.2:** el PDF no se abrió. **Sé que lo cita porque lo dice mi propia nota**, y si la cita está incompleta eso es el modo de falla 9 sin medir.
6. **La coincidencia de `N`/`M`/`Mw` no prueba mismo archivo**, sólo mismo snapshot y mismo criterio. **No se compararon md5.**
7. **Nada escrito en el issue #4.** Espera OK.
8. **Los pasos 1 a 4 siguen sin ejecutarse:** dos turnos consecutivos de lectura por pedido explícito. **Van en el siguiente.**
9. **`CONTEXTO-motor.md` sigue sin abrirse**, sexto turno.
10. **El contexto vivo acumula cinco líneas viejas** y las nombro en vez de reescribirlo de memoria: la «072», A-10, A-01/A-02, la palabra «externa» sobre Tao, y ahora **Betzel, que pasa de NO MEDIDO a verificado**.
