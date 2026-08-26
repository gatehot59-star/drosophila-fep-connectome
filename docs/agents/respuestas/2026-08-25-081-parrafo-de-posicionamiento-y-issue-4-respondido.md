# 081 · Párrafo de posicionamiento escrito, issue #4 respondido, y el paper ya los distinguía

**Fecha:** 2026-08-25 10:40 (America/Buenos_Aires) · **Modo:** TITAN FULL

> **📄 Entregables:** `docs/POSICIONAMIENTO-VS-CONCURRENTES.md` + [comentario en el issue #4](https://github.com/gatehot59-star/drosophila-fep-connectome/issues/4#issuecomment-5411308325)
> **🔬 Evidencia cruda:** `docs/agents/evidencia/2026-08-25-tres-papers-issue4-evidencia-cruda.md`
> **🛠 Instrumento:** `gateway build.run` sobre `brain-env`, 9 corridas. PDF de Zenodo con **md5 `c7cb36a261182f6ce895057ebe26e505`**, coincidente con el declarado.

---

## 1. Pedido

«Hacé lo que solicitás en el documento *El competidor es Betzel*.»

Las dos acciones que esperaban OK en la resp 080 eran: **(a)** comentar el issue #4 con el veredicto, y **(b)** escribir el párrafo de posicionamiento con las renuncias de Betzel. **Las dos hechas.**

## 2. Herramientas declaradas (C-03)

| Llamada | Escribe | Cuota ajena |
|---|---|---|
| `mcp_gateway build.run` × 4 nuevas sobre `brain-env` (captions, suplementarios, PDF de Zenodo) | sólo `/tmp` | **NO** |
| `push_files` × 1 → `docs/POSICIONAMIENTO-VS-CONCURRENTES.md` | sí | no |
| **`add_issue_comment` × 1 → issue #4** | **sí** | no |
| `create_or_update_file` × 1 (este archivo) · `create_document` × 1 | sí | no |

**Cero Kaggle. Cero runtime de Tachi. Ningún merge. `main` intacta. Nada borrado.** El comentario al issue es una escritura pública en el repo y **estaba autorizada explícitamente**.

## 3. 🔴 Antes de escribir cerré los dos NO MEDIDO, y los dos cambiaron el texto

**Si escribía el párrafo sin esto, lo escribía mal.**

### (a) El PDF publicado YA los distingue, y con tabla

Bajé el PDF de Zenodo y verifiqué el md5 contra el que declara la API: **`c7cb36a261182f6ce895057ebe26e505` en los dos lados.** 7 páginas, 23.025 caracteres.

- **§1.2 Related Work**, verbatim: *«Betzel et al. [2026] demonstrated convergence of sensory cascades on shared integration nodes in the Drosophila connectome.»*
- **§4.4 Comparison with Concurrent Work** contiene la **Tabla 11**, *«Comparison with concurrent studies»*, comparando **Shiu · Betzel · This** fila por fila.
- **Y cita `Shiu, P.K., et al. (2024)`, Nature 634, 210-219** — que es **el modelo sobre el que se construye la demo de Eon Systems**.

> **Dos de los tres «competidores» del issue ya estaban citados y diferenciados en el paper publicado desde marzo.** La acción 3 del issue («dejar constancia de en qué se distingue») **no estaba pendiente**.

**Esto cierra el NO MEDIDO 5 de la resp 080**, donde declaré que no había verificado cómo cita el Paper 1 a Betzel. **La cita es completa y correcta:** autores, año, título, revista, volumen, artículo y DOI.

### (b) «Cero signo» era demasiado grueso, y lo corrijo

Leí las **19 captions** y los **11 suplementarios**. Su **S6 Fig** sí desglosa por neurotransmisor, verbatim:

> *«we parse contributions made by six distinct synapse types (based on neurotransmitter). They include acetylcholine (ACH), dopamine (DA), **gabaergic (GABA)**, glutamate (GLUT), octopamine (OCT), and seratonin (SER). … we tracked how frequently synapses associated with different neurotransmitter types **successfully activated their post-synaptic partner**.»*

**La distinción exacta, y es más fina y más defendible que la que escribí ayer:** ellos **etiquetan** las sinapsis por neurotransmisor para medir **quién transporta la cascada**. Pero en su modelo **una sinapsis GABAérgica igual ACTIVA al postsináptico**: el neurotransmisor es una etiqueta descriptiva, no un **signo** en la dinámica. **No hay cancelación.** Por eso su propia Discussion pide «synaptic polarity» como mejora futura **después** de haber hecho la S6.

**Y lo que sí se sostiene, medido sobre las 19 captions:** `motor` 0 · `descending` 0 · `effector` 0 · `efferent` 0. Y **`signed` como palabra completa: 0** en todo el paper (los dos aciertos por substring eran `assigned`).

## 4. 🔴 Y apareció un defecto en el paper publicado

La fila `Null model` de la **Tabla 11** dice que Betzel usa **«Comm. only»**.

**Medido:** su único control es *«we randomly permuted the annotation labels … 1000 times»*, y su análisis de comunidades usa un **nested SBM para DETECTAR** comunidades, no un null que las preserve.

> **Describirlo como «community null» es impreciso, y está en un documento con DOI.** Es el **modo de falla 10** (afirmar sobre el método de un tercero sin verificarlo), cometido en la dirección contraria a la habitual: **describiendo mal al otro en la misma fila donde se lo subestima**.
>
> **Redacción correcta:** *Betzel = label permutation (n = 1000); no graph null.*
>
> **NO se corrige solo:** es texto publicado y la decisión es de Abraham.

**Y la honestidad que va con eso:** su `n` es **1000** y el de este trabajo es **40**. En número de realizaciones **ellos están mejor**. La ventaja propia es **qué** se permuta, no cuántas veces, y así está escrito en el párrafo.

## 5. 🟢 El párrafo entregado, y por qué está armado así

`docs/POSICIONAMIENTO-VS-CONCURRENTES.md`, en **inglés (para pegar) y español (para la bitácora)**. Su regla de construcción:

> **No afirma que los otros no supieron. Cita lo que ellos mismos declaran no cubrir.** Cada comilla lleva su fuente, así que un revisor puede verificar cada una abriendo el paper.

**El eje, que es medido y no retórico:**

| Renuncia declarada | Quién la declara |
|---|---|
| *«synaptic polarity, inhibitory/excitatory distinctions»* como mejora futura | **Betzel et al. (2026)**, PLOS |
| *«motor neuron pathways would better approximate the full sensorimotor axis»* | **Betzel et al. (2026)**, PLOS |
| *«we take its **steady-state response**»* | **Bates et al. (2026)**, Nature (BANC) |
| *«adjusted influence is an **unsigned quantity**»* | **Bates et al. (2026)**, Nature (BANC) |

> **Dos grupos independientes, en dos revistas distintas, declaran ausentes las MISMAS dos propiedades: el signo y el transitorio.** No es una coincidencia afortunada: **es la definición del hueco, escrita por quienes lo dejaron.**

**Y contiene el párrafo del erratum que convierte una autocorrección en un hecho de tercero:** la densidad corregida `7,85 × 10⁻⁴` contra el `7,8 × 10⁻⁴` de Betzel, con los tres conteos de población idénticos. **Un revisor no tiene que confiar en la aritmética del autor.**

**Además declara el solapamiento real**, antes que un revisor: la observación cualitativa de que las cascadas convergen en poblaciones motoras y descendentes **es prior art**. Lo nuevo es **el control** que distingue un cero que la anatomía predice de uno que no.

## 6. Recomendación emitida, sin hedge

**No citar a Eon Systems ni a Rojas Aliaga en la v2.** Una demo sin revisión por pares (con desmentida de framing de *The Verge*) y un preprint **posterior** con contradicciones internas medidas (139.255 vs 138.639 neuronas entre su abstract y su repo) **no son prior art, y citarlos los eleva.**

**Sí mantener la cita de Shiu et al. (2024)**, que ya está en el paper, porque es el trabajo real que hay debajo de la demo. **Es la forma correcta de cubrir a Eon: citando su fuente, no su prensa.**

## 7. Archivos generados en este turno

| Archivo | Qué |
|---|---|
| `docs/POSICIONAMIENTO-VS-CONCURRENTES.md` | el párrafo, en dos idiomas, con la corrección de la Tabla 11 y las fuentes de cada comilla |
| `docs/agents/respuestas/2026-08-25-081-...md` | este |
| comentario en el issue #4 | el veredicto completo, con la corrección de fecha y las dos correcciones a mi propio veredicto anterior |

## 8. Scorecard

| Criterio | Pts | Evidencia |
|---|---|---|
| **Completitud** | 14/15 | las dos acciones ejecutadas, y los dos NO MEDIDO de la 080 cerrados **antes** de escribir. **−1:** el paper de Rojas sigue sin leerse completo |
| **Arquitectura del razonamiento** | 10/10 | el párrafo no se apoya en opinión: cada exclusión es una **cita de la renuncia propia del otro**, verificable. El md5 del PDF se comprobó contra el declarado antes de citarlo |
| **Documentación** | 10/10 | dos idiomas, fuente por comilla, y **tres correcciones a veredictos propios** (el «cero signo», la fila de la Tabla 11 y el NO MEDIDO 5) en sus propias secciones |
| **Innovación** | 4/5 | el par Betzel+BANC declarando la misma ausencia es un argumento de posicionamiento que no existía. **−1:** no se aplicó a la v2, sólo se dejó listo |
| **Proceso QA** | 5/5 | cada afirmación con su comando y su salida; el falso positivo de `sign` declarado; el defecto del paper propio declarado y **no** corregido unilateralmente |

**Total 57/60 → 95,0/100.** **N/A: 40 pts** (Ejecutabilidad, Seguridad, Testing, DevOps): la entrega es texto.

## 9. NO MEDIDO, declarado

1. **No se abrieron los datos suplementarios de Betzel ni su `Response_to_Reviewers.pdf`.** Se leyeron los 11 suplementarios **por su caption**, no su contenido. Si una tabla suplementaria cuantifica acceso motor por modalidad, la §5 del párrafo se angosta.
2. **No se compararon los dos modelos midiendo** (cascada probabilística vs propagación lineal con `tanh`): se compararon descripciones de método, no corridas sobre el mismo grafo.
3. **La coincidencia de `N`/`M`/`Mw` no prueba el mismo archivo**, sólo el mismo snapshot con el mismo criterio. **No hay md5 publicado del lado de Betzel.**
4. **🔴 La fila `This = MS+CP (N=100)` de la Tabla 11 no se verificó contra el código.** El repo publica **40** nulls como titular y `METHODS` declara MS `N=100` estático. **Puede ser un sexto caso del modo de falla 5 y queda SIN MEDIR.** Es la deuda más barata que deja este turno.
5. **El paper de Rojas Aliaga no se leyó** (abstract + README). **Eon no se auditó técnicamente.**
6. **El párrafo no lo revisó nadie más que su autor.** K-02 declarado.
7. **Los pasos 1 a 4 de la reparación siguen sin ejecutarse:** tres turnos consecutivos de lectura y redacción por pedido explícito. **Van en el siguiente.**
8. **`CONTEXTO-motor.md` sigue sin abrirse**, séptimo turno. Sin veredicto de vigencia.
9. **El contexto vivo acumula seis líneas viejas** y las nombro en vez de reescribirlo de memoria: la «072», A-10, A-01/A-02, la palabra «externa» sobre Tao, Betzel (que pasa de NO MEDIDO a **verificado y a favor**), y el defecto nuevo de la Tabla 11.
