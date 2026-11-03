# 2026-11-02-011 · Rectificación de alcance: la auditoría de Topo no había leído directamente tus tres papers

**Fecha:** 2 de noviembre de 2026, America/Buenos_Aires. **Rol:** revisión documental y rectificación de alcance, no nueva auditoría experimental.

**Pedido de Abraham:** «que extraño, viste funtes externas, pero viste mi paper publicado y corregido mas los dos borradores de paaper que le siguen que todavia no publique?»

## 1. Respuesta y responsabilidad

**No: en la auditoría anterior no había contrastado directamente esos tres textos.** Había leído los seis adjuntos de Topo, archivos del proyecto, evidencia numérica y literatura externa. Leer referencias a los papers en el contexto no equivale a leer los manuscritos.

La comparación del aporte de Topo contra la trayectoria propia quedó incompleta. Es una omisión mía, no una carencia de tu proyecto. La lectura hecha después de tu señalamiento no se atribuye retroactivamente a aquella auditoría.

Esta nota es adicional. No reescribe el informe previo para disimular su alcance, ni modifica tus papers, 009, su sello, su generador o 009-A1.

## 2. Qué leí directamente después de tu señalamiento

### Paper 1 corregido y su erratum

- **Signal Propagation Properties in the Drosophila melanogaster Connectome: Intermodal Isolation, Differential Motor Access, and Non-Trivial Temporal Amplification**, versión 2.0. Fuente completa: `docs/v2/paper1-v2.0.md`, en el commit `153694da13e41122efa7666f637a5e925a619a37`; blob `5c590f1e82b0233adbe520f8860f220ead050df1`.
- Erratum completo: `docs/ERRATUM.md`, en el mismo commit; blob `ce57657757c27dbc6f38299f39354aba30e644ba`.
- [Registro público v2.0](https://zenodo.org/record/23393412), DOI `10.5281/zenodo.23393412`. El texto se identifica como preprint, no revisado por pares. Publicado no equivale a validado por revisión de pares.

### Sucesor funcional de octubre, identificado como Paper 2

- **The connectome as a blueprint: a sealed functional benchmark of the Drosophila looming-escape pathway across three scales and two flies**.
- Texto completo leído: `docs/paper2/paper2-esqueleto.md`, rama `titan/paper2-esqueleto-2026-10-14`, commit `4652c8138c52333ae04b5ed91b026ee758385e5e`, blob `a1c02c4a4ef6a6f6685d834554d6b53422f0ccab`.
- El propio archivo se rotula **SKELETON, not a draft for submission**. No lo presento como manuscrito terminado ni aseguro haber localizado una versión posterior más desarrollada.

### Sucesor estructural de octubre, identificado como Paper 3

- **Who drives the outputs of the fly brain? A null-controlled input map of descending, motor and neurosecretory neurons in FlyWire v783**.
- Texto completo leído: `docs/paper3/paper3-esqueleto.md`, rama `titan/paper3-esqueleto-2026-10-14`, commit `c4c8549e67359cedda1943fb56e314a85ed901ef`, blob `d74220f80b3ef418c14f27cfb4510eab1c619daa`.
- También se rotula **SKELETON, not a draft for submission**.

La identificación de los dos sucesores se apoya en la [organización de los tres papers de octubre](https://app.clickup.com/90171457413/docs/2kza6fw5-22197/2kza6fw5-24937) y en la [revisión posterior a la publicación de la v2](https://app.clickup.com/90171457413/docs/2kza6fw5-22937/2kza6fw5-25677), además de los propios archivos. Esos documentos históricos sirven para identificar textos, no para tratar sus pendientes de octubre como estado experimental actual.

## 3. Qué cambia en la comparación

1. **La diferenciación frente a otros trabajos no empieza en mi auditoría.** El Paper 1 ya tiene una comparación con estudios concurrentes en §4.4 y Tabla 11. Su línea incluye propagación con signo, dinámica transitoria, cancelación inhibitoria y controles sobre el acceso a las salidas. El erratum también acota la novedad, separa clases funcionales de regiones anatómicas y declara resultados no reproducidos o no firmados. No corresponde vender esas distinciones como ideas nuevas aportadas por mí.
2. **La pregunta funcional ya estaba planteada en Paper 2.** El archivo pregunta si el cableado exacto carga función más allá de los barajados y de una regla con los mismos sensores, y si la parte relevante se conserva en otra mosca. Sus resultados y pendientes son los que declara ese archivo; no ejecuté de nuevo su banco ni actualicé su estado con este turno.
3. **La pregunta sobre quién alimenta las salidas ya estaba planteada en Paper 3.** El texto distingue tamaño, ubicación y conectividad mediante familias de nulos y corrección múltiple. No corresponde confundir contar conexiones con establecer un exceso respecto de la oportunidad anatómica.
4. **Topo y 009-A1 deben ubicarse dentro de esa trayectoria.** La interpretación propuesta es una continuación hacia mecanismos recurrentes D→X y cortes selectivos en el modelo, conectada con las preguntas funcional y estructural anteriores. Esto no demuestra por sí mismo novedad global, transferencia a otra mosca ni causalidad biológica.

La corrección concreta es de atribución y alcance: primero reconocer lo que tu propia línea ya formuló; después separar qué agrega realmente un experimento nuevo y qué todavía no está demostrado.

## 4. Qué no queda invalidado automáticamente

La omisión de lectura no vuelve falsos por sí sola los cálculos que sí se ejecutaron sobre datos y resultados archivados. En particular, la [auditoría anterior](https://app.clickup.com/90171457413/docs/2kza6fw5-26317/2kza6fw5-29457) distingue:

- La conservación de los 17 relevos bajo el nulo condicional del subgrafo pesado que se probó, no bajo cualquier nulo imaginable.
- El 7/7 del predictor como ajuste descriptivo reproducido, no como validación predictiva reservada ni identificación del mecanismo.
- Los errores concretos de transcripción, definición de colaterales y construcción del nulo que se diagnosticaron.

No repito ni amplío esos ensayos aquí. Tampoco concluyo que leer los papers ahora demuestra que sus resultados científicos sean correctos.

El **45/45 documental de 009-A1** evaluaba la coherencia de ese protocolo, con 55 puntos no aplicables. No certificaba la cobertura de todo tu corpus, la ejecución del runner, la originalidad de tu programa ni sus conclusiones experimentales. Esta rectificación no recibe un nuevo puntaje que sustituya la evidencia.

## 5. Verificación de versión publicada realizada en este turno

Consulta independiente del recibo local, a `2026-11-03T01:55:41.912918+00:00` (2 de noviembre en Argentina):

- La [API pública de Zenodo](https://zenodo.org/api/records/23393412) devolvió HTTP 200, registro `23393412`, DOI `10.5281/zenodo.23393412`, versión `2.0` y el título del Paper 1.
- PDF principal: `Mendieta2026_Paper1_v2.0.pdf`, 332.607 bytes, checksum publicado `md5:6e849bf2caffa540165edd826df102ed`.
- PDF del erratum: `Mendieta2026_Paper1_Erratum_v1.0.pdf`, 191.172 bytes, checksum publicado `md5:05052e6e7e0dd79cee584c9d285b1b93`.
- Ambos coinciden con los metadatos de `docs/v2/archivos-deposito-v2.0.json` ya leído.
- Fuente del paper: 57.238 bytes; MD5 `a4d09d2c345dca03faca4d9bccf236d7`, coincidente con la fuente declarada en el manifiesto; SHA-256 `57bc19d5dd4ed10eeabbf546dfbc3e0e8642dd3964bb6e8ab3fd935436c313c3`.
- Fuente del erratum: 41.121 bytes; MD5 `f2ad05072086258a8ce76b9d650ed26d`, coincidente con la fuente declarada en el manifiesto; SHA-256 `11b591e94f09031e366ebdd902a45fa6a0014c818212c0c118a378a8f815a2db`.

**Límite exacto:** leí los Markdown completos y consulté los metadatos públicos. No descargué de nuevo los dos PDF para cotejar su texto renderizado. Coincidencia con el manifiesto no es una nueva auditoría de la conversión Markdown→PDF ni de los resultados del paper. La consulta y los hashes se ejecutaron con salida 0 y stderr vacío, sin simulaciones ni escritura en el repositorio de trabajo.

La primera apertura del registro mediante otro lector había agotado su tiempo de respuesta; la consulta posterior a la API sí resolvió la comprobación pública. No quedó pendiente por un fallo de acceso.

## 6. Ambigüedad histórica que no voy a esconder

En agosto se usó también «Paper 2» para **Topological Retention and Selective Convergence**, el texto FEP, y se registró por separado un paper embedded/DualBrain. Leí los índices históricos que los describen, **no esos dos manuscritos completos en este turno**.

Por eso esta nota identifica por título, ruta y versión los dos sucesores de octubre. Si Abraham se refiere a versiones más desarrolladas u otros dos manuscritos, esa cobertura todavía no está establecida. No se reemplaza un texto por otro porque compartan el número «2».

## 7. Estado y límites

- **PASS documental:** lectura directa actual del Paper 1 v2.0, su erratum y los dos archivos de octubre identificados arriba; comprobación pública de versión y coincidencia de las fuentes con el manifiesto de depósito.
- **FAIL de alcance anterior:** la comparación externa previa no incluyó lectura directa de esos tres textos propios antes de emitirse.
- **NO MEDIDO:** exactitud experimental de los papers en una nueva réplica; novedad global; manuscritos posteriores más completos; lectura directa actual de los textos FEP y embedded históricos; capacidad funcional o biológica nueva.
- **Sin cambios de objeto:** ningún manuscrito, diseño original, sello, generador, protocolo 009-A1 o resultado histórico se modifica con esta nota. No hay merge, publicación de los borradores, despliegue, nuevas simulaciones ni mensajes a terceros.

La consulta se cierra con esta rectificación, no con otra promesa de que todo el corpus quedó auditado.
