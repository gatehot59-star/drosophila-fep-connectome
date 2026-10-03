# Paso 1: identidad experimental de `ROI_0` y `ROI_1`

**Estado:** diseño del paso y contrato de decisión. No es todavía un mapping biológico.

**Doc público asociado:** [Paso 1: identidad experimental de ROI_0 y ROI_1, decisiones y contrato](https://app.clickup.com/90171457413/docs/2kza6fw5-18617)

## Veredicto corto

Este paso no consiste en inventar dos `root_id` para dos nombres de columnas. Consiste en demostrar qué objeto físico representa cada ROI en el experimento y recién después establecer si ese objeto puede vincularse de manera reproducible con FlyWire.

El estado honesto hoy es **identidad anatómica de `ROI_0` y `ROI_1`: NO MEDIDA**. El pipeline conoce dos series de calcio, pero el material inspeccionado no contiene por sí mismo `root_id`, tipo celular, neuropilo, máscara espacial ni coordenadas. El atlas FlyWire está validado como atlas independiente; eso no asigna ninguna de sus neuronas a las ROI.

La recomendación fuerte es: **no correr todavía el null anatómico y no ampliar H4**. Primero se reconstruye la provenance de las ROI. Si esa provenance no existe, se cierra este paso como `NO_MAPPED_ROIS`, que es un resultado válido, no un fracaso maquillable.

## 1. Qué hay que distinguir

Hay tres identidades distintas y no se deben mezclar:

1. **Identidad experimental:** qué fue segmentado o medido en el microscopio: una célula, un soma, una prolongación, una región de neuropilo o una mezcla de células.
2. **Identidad anatómica:** qué unidad del atlas corresponde a esa entidad: un `root_id`, un conjunto de `root_id` o solamente una región/población.
3. **Identidad funcional:** la serie DFF y su relación con una etiqueta conductual. Que una señal discrimine una etiqueta no identifica por sí mismo una célula anatómica.

El error que este paso evita es saltar de la identidad funcional a la anatómica.

## 2. Evidencia disponible ahora

- `DFF_dic.p` del trial inspeccionado contiene únicamente `ROI_0` y `ROI_1`, con 1.067 muestras neurales cada una.
- El H5 del trial conserva señales ThorSync (`AI`, `CI`, `DI`, `Global`), no una identidad FlyWire por ROI.
- El conjunto Aymanns usado para H4 corresponde a un solo animal, `R65D11-tdTomGC6fopt-fly1`; por eso cualquier mapping que aparezca debe quedar ligado explícitamente a ese animal y a sus trials.
- El atlas FlyWire v783 tiene sus propios conteos y checksums validados, pero ninguna fila del atlas es automáticamente `ROI_0` ni `ROI_1`.
- El gate actual acepta solo una declaración explícita por ROI: `MAPPED` con `root_id` positivo, evidencia `direct_root_id` o `manual_roi_to_cell`, confianza finita en `[0,1]` y notas de provenance. También acepta `UNMAPPED`, pero lo convierte en `PARTIAL` o `NO_MAPPED_ROIS`, nunca en anatomía implícita.

**Consecuencia:** el nombre de la columna, el orden de las filas, la correlación de la señal y el neuropilo no alcanzan como identidad celular.

## 3. Decisiones que hay que tomar, en este orden

### 3.1 Qué representa cada ROI

Cada ROI debe clasificarse como una de estas unidades:

- `CELL`: célula individual con resolución suficiente.
- `SOMA`: soma segmentado, posiblemente vinculado a una célula completa del atlas.
- `DENDRITE_AXON`: prolongación o señal parcial; no equivale automáticamente a un `root_id` completo.
- `NEUROPIL`: región anatómica, no célula.
- `POPULATION`: señal agregada de varias células.
- `MIXED`: mezcla conocida de unidades.
- `UNKNOWN`: la metadata no permite decidir.

**Decisión recomendada:** si no hay máscara o metadata de segmentación, usar `UNKNOWN`, no `CELL`. Una ROI llamada “ROI” no demuestra resolución celular.

### 3.2 Qué granularidad de mapping corresponde

Hay tres contratos posibles:

- **Uno a uno:** una ROI experimental ↔ un `root_id` FlyWire. Es el contrato actual del gate v1.
- **Uno a varios:** una ROI ↔ conjunto de `root_id` con pesos de contribución o máscara de pertenencia. Es el contrato correcto si la ROI es una población.
- **Región solamente:** la ROI puede ubicarse en un neuropilo o clase anatómica, pero no en una célula. Eso permite una descripción regional, no un null celular ni una afirmación de ruta individual.

**Decisión recomendada:** no forzar el contrato uno a uno. Si la evidencia muestra población o mezcla, hay que ampliar el esquema a un manifest v2 con `root_ids`, pesos, método de contribución y regla de agregación. Un único ID elegido “porque es el más probable” sería falsa precisión.

### 3.3 Qué evidencia se considera suficiente

Orden de fuerza:

1. `direct_root_id`: el archivo experimental ya trae el `root_id` o una correspondencia inequívoca emitida por el pipeline.
2. `manual_roi_to_cell`: mapping manual documentado a partir de máscara, coordenadas, plano, registro y snapshot del atlas.
3. Registro espacial reproducible: máscara/centroide más transformación explícita hacia el atlas, con validación independiente.
4. Etiqueta de neuropilo o población: suficiente para identidad regional, insuficiente para identidad celular.
5. Correlación de DFF, orden de columnas, superclase o prominencia de señal: **no aceptable** como identidad anatómica.

El gate actual acepta solo los dos primeros como `MAPPED`. El tercero puede servir para construir una evidencia manual reproducible, pero no debe entrar como `MAPPED` hasta que el procedimiento y la procedencia estén documentados.

### 3.4 Cuál es la fuente de verdad

La fuente primaria debe buscarse en este orden:

1. archivo o notebook que creó `DFF_dic.p`;
2. máscaras binarias o labels de segmentación de las ROI;
3. coordenadas de imagen, plano, zoom, orientación y metadata del microscopio;
4. registro del animal, trial y preparación;
5. transformación o landmarks usados para registrar la imagen contra el atlas;
6. anotación manual y su evidencia visual;
7. snapshot FlyWire v783 y sus manifests de checksums.

El DFF es el resultado de extracción, no necesariamente la fuente de identidad. Si solo aparece el DFF, el mapping queda `UNMAPPED`.

### 3.5 Qué nivel de confianza se informa

La confianza no reemplaza la evidencia. Debe responder “qué tan reproducible es la asignación declarada”, no “qué tan plausible parece”.

- `1.0` no debe usarse por comodidad; requiere una correspondencia directa y auditable.
- Una asignación manual debe conservar operador, fecha, fuente, criterio y notas.
- Una inferencia basada solo en señal debe quedar fuera del campo `MAPPED`, aunque parezca muy convincente.
- Si no se puede defender la confianza con la provenance, la fila es `UNMAPPED`.

### 3.6 Qué alcance experimental se quiere sostener

Antes de medir, hay que elegir qué claim se pretende habilitar:

- **Identidad descriptiva:** “esta señal proviene de esta unidad o población”.
- **Comparación anatómica:** “esta distribución difiere de un null que conserva estructura”.
- **Ruta causal:** “silenciar esta unidad cambia la conducta o la dinámica”.

El paso uno solo puede habilitar el primer claim. No convierte un mapping en causalidad. Para H4 fuerte todavía harán falta perturbaciones y un null anatómico pareado.

## 4. Procedimiento exacto

1. **Localizar el origen del DFF.** Encontrar el notebook, script o pipeline que creó `DFF_dic.p`; registrar path, commit, input y hash.
2. **Inspeccionar el objeto anterior al DFF.** Determinar si existían máscaras, centroides, labels, planos o IDs que se perdieron durante la exportación.
3. **Clasificar cada ROI.** No clasificar el par completo por defecto: `ROI_0` y `ROI_1` pueden tener distinta calidad o granularidad.
4. **Reconstruir provenance espacial.** Recuperar animal, trial, plano, escala, orientación, coordenadas y cualquier transformación aplicada.
5. **Buscar una correspondencia anatómica independiente.** Priorizar un `root_id` declarado o un mapping manual documentado; no derivarlo de la señal DFF.
6. **Congelar la versión del atlas.** Usar la snapshot FlyWire v783 ya manifestada, con hashes de conectividad y annotations.
7. **Escribir una fila por ROI.** Si una ROI mezcla células, no escribir un único `root_id`; declarar la necesidad de un manifest poblacional.
8. **Ejecutar el gate fail-closed.** El instrumento debe poder rechazar duplicados, IDs inexistentes, confianza inválida, evidencia ausente y conjuntos de ROI incompletos.
9. **Cerrar con uno de tres estados:** `COMPLETE`, `PARTIAL` o `NO_MAPPED_ROIS`.
10. **Actualizar la hipótesis, no solo el archivo.** Si no hay mapping, H4 fuerte sigue `NO MEDIDA`; no se convierte la ausencia de datos en un resultado anatómico.

## 5. Contrato de provenance recomendado

El manifest debe conservar, como mínimo:

| Campo | Decisión que captura |
|---|---|
| `animal_id` | evita mezclar animales o asumir cross-animal |
| `trial_id` | liga la ROI con la corrida concreta |
| `roi_name` | `ROI_0` o `ROI_1`, sin renombrar silenciosamente |
| `roi_unit` | célula, soma, población, neuropilo, mezcla o desconocida |
| `source_file` | archivo original de segmentación/extracción |
| `source_sha256` | integridad del input |
| `mask_file` / `mask_sha256` | evidencia espacial de la ROI |
| `plane`, `x`, `y`, `z`, escala y orientación | geometría experimental disponible |
| `registration_method` | cómo se relaciona imagen y atlas |
| `registration_transform` | transformación exacta o `UNMAPPED` si no existe |
| `atlas_name` / `atlas_version` | snapshot anatómica usada |
| `root_ids` | uno o varios IDs, nunca inventados |
| `root_weights` | contribución si la ROI es poblacional |
| `evidence_kind` | directa, manual o no mapeada |
| `confidence` | valor finito y justificado |
| `operator` / `date` | quién y cuándo produjo la asignación |
| `notes` | límites, decisiones y procedencia legible |
| `status` | `MAPPED`, `UNMAPPED` o estado poblacional explícito |

El gate v1 actual cubre el caso uno-a-uno. Si la inspección demuestra una población, el trabajo correcto es ampliar el contrato, no esconder la población dentro de un `root_id`.

## 6. Árbol de decisión

- **Existe `root_id` directo y verificable:** registrar `MAPPED`, conservar el archivo fuente y validar que el ID vive en annotations.
- **No existe `root_id`, pero sí máscara, coordenadas y registro reproducible:** producir un mapping manual documentado; no usar la intuición del operador como única evidencia.
- **Existe solo neuropilo o clase celular:** registrar identidad regional/poblacional; no declarar identidad celular.
- **La ROI mezcla varias células:** registrar conjunto de IDs y pesos, o dejar `UNMAPPED` hasta tener ese contrato.
- **Solo existe DFF y nombres de columnas:** registrar `UNMAPPED`.
- **Una ROI se puede mapear y la otra no:** estado `PARTIAL`; no presentar H4 fuerte como confirmada y no seleccionar el resultado conveniente.

## 7. Criterios de éxito y de aborto

### Éxito

El paso termina bien si cada ROI tiene una descripción experimental, una provenance reproducible y un mapping cuya granularidad coincide con el objeto observado. “Completo” significa dos ROI resueltas, no solamente dos filas que pasan sintaxis.

### Resultado válido pero limitado

`PARTIAL` es válido cuando una ROI está mapeada y la otra no, o cuando solo existe identidad regional. Sirve para planificar, no para sostener el claim anatómico completo.

### Aborto honesto

`NO_MAPPED_ROIS` es el resultado correcto si no aparecen máscaras, coordenadas, IDs o un registro manual defendible. En ese caso se conserva H4 como señal ROI-label descriptiva dentro del animal y se deja explícito que anatomía y causalidad siguen sin medir.

## 8. Sugerencias concretas

- Empezar por el pipeline que generó `DFF_dic.p`, no por el atlas. El atlas ya está; lo que falta es el puente experimental.
- Buscar primero máscaras y metadata de microscopía. Sin geometría, cualquier mapping celular sería una conjetura elegante.
- Mantener separados `animal_id`, `trial_id` y `roi_name`; nunca usar el nombre de ROI como identidad global.
- Congelar desde el comienzo la snapshot FlyWire v783 y todos sus hashes para que el mapping no cambie porque cambió el atlas.
- Guardar también los casos descartados y el motivo del descarte. Eso evita que una asignación refutada vuelva meses después como “dato histórico”.
- Si no aparece el origen espacial, cerrar rápido como `NO_MAPPED_ROIS` y pasar a buscar un segundo animal o una fuente experimental mejor, en vez de gastar otro ciclo en correlaciones inválidas.

## 9. Qué queda expresamente prohibido

- `ROI_0 → root_id 0` o `ROI_1 → root_id 1`.
- Mapear por orden de filas, orden de columnas o posición en un pickle.
- Mapear por correlación entre DFF y actividad simulada.
- Mapear por superclase, neuropilo o etiqueta conductual como si fueran una célula.
- Declarar que el mapping prueba causalidad.
- Ejecutar un null anatómico con `UNMAPPED` y presentarlo como evidencia de H4.
- Tratar una ROI poblacional como una neurona individual.

## 10. Handoff al paso 2

El paso 2 solo debe arrancar cuando exista una de estas dos condiciones:

1. **Mapping completo y explícito** de las dos ROI, con la granularidad correcta; o
2. **Decisión formal de cambiar la unidad de análisis** de célula a población/región, con un null anatómico diseñado para esa unidad.

La opción que no existe es “seguir igual y asumir que ROI_0 y ROI_1 son dos neuronas”. Esa vía sería exactamente el error que el gate fue creado para bloquear.

## Instrumentos y alcance de esta entrega

Se leyó en vivo el contexto canónico del conectoma, el último recibo H4, el inventario de capacidades y el contrato/ADR del gate desde `main` del repositorio `gatehot59-star/drosophila-fep-connectome`. Se creó una rama de documentación; no se ejecutó una nueva corrida biológica, no se inspeccionó nuevamente el data lake y no se declaró ningún mapping.

### NO MEDIDO

- qué unidad física representa `ROI_0`;
- qué unidad física representa `ROI_1`;
- existencia de máscaras espaciales utilizables;
- coordenadas y transformación hacia FlyWire;
- cualquier `root_id` experimental;
- si una ROI es individual o poblacional;
- mapping cross-animal;
- null anatómico pareado y causalidad.

**Conclusión:** el trabajo del paso uno es recuperar o demostrar la ausencia de la cadena `ROI experimental → geometría → identidad anatómica`. Hasta que esa cadena exista, el producto tiene un atlas y un motor propios, pero no una asignación anatómica verificable de estas dos señales H4.

--- METODO TITAN ---
Accion delicada: NO
Modo aplicado: TITAN FULL
Rubrica: N/A (briefing de diseño, sin código, merge ni despliegue)
N/A declarados: ejecutabilidad, seguridad, testing de producto, deployment e innovación de código no aplican
Review externo: no solicitado; no equivale a aprobación
Instrumento: GitHub API, lectura de `main`; no se ejecutó brain-env en esta entrega
Maquina: GitHub API; brain-env no utilizado para una corrida nueva
Artefactos: `docs/agents/respuestas/2026-10-03-001-paso-1-identidad-experimental-roi.md` + [Doc público](https://app.clickup.com/90171457413/docs/2kza6fw5-18617)
NO MEDIDO: mapping biológico nuevo, origen de máscaras, registro espacial, root IDs, null anatómico y causalidad