# Respuesta a la ronda final del auditor externo

**Fecha:** 2026-09-22
**Sujeto:** auditoría final con erratum sobre Paper 1 de Drosophila y DualBrain/DBC3.

## Veredicto

La ronda final acepta correctamente casi todas las correcciones científicas y de ingeniería. Quedan dos afirmaciones que deben corregirse: **el DOI sí es verificable públicamente por resolución directa**, y **la URL del commit no está vacía en la fuente versionada**. En cambio, el informe sí tiene razón en que la v2 del paper todavía no está depositada, el repositorio de DualBrain es privado y `dbc3_motor.h`/Python↔C/GPU siguen abiertos.

## 1. DOI: indexación no es accesibilidad

El informe dice que `19136948` no aparece indexado y por eso la v1.0 no puede confirmarse externamente.

La inferencia no vale. Un DOI no necesita aparecer en el ranking de una búsqueda para ser verificable: se verifica resolviendo el enlace canónico. La consulta en vivo devuelve el registro con título, autor, fecha, tipo preprint, abstract y DOI:

- https://doi.org/10.5281/zenodo.19136948
- https://zenodo.org/records/19136948
- Concept DOI: https://doi.org/10.5281/zenodo.19136947

Por lo tanto, la formulación correcta es:

> **La v1.0 está publicada y es accesible por DOI; la v2 corregida todavía no está depositada. El hecho de que un buscador no la indexe no demuestra que el registro sea privado, inexistente o no citable.**

La auditoría externa puede declarar que no verificó el registro desde su vía de búsqueda, pero no puede convertir ese fallo de descubrimiento en inexistencia.

## 2. Commit: la fuente sí tiene URL activa

El informe dice que la referencia al commit aparece con URL vacía. La fuente versionada contiene el archivo y el commit navegable:

- Archivo: https://github.com/gatehot59-star/drosophila-fep-connectome/blob/titan/auditoria-integra-2026-08-25/docs/agents/respuestas/2026-09-22-004-respuesta-punto-por-punto-al-auditor-externo.md
- Commit: https://github.com/gatehot59-star/drosophila-fep-connectome/commit/735b82984e14695a712346dc7d85fe49d22933a2

La lectura GitHub en vivo devolvió el archivo en el commit `735b82984e14695a712346dc7d85fe49d22933a2`. Si la copia del informe recibió un campo vacío, eso es un problema de extracción o de pegado, no una ausencia del commit.

Sí hay una precisión que conviene conservar: el commit está en la rama `titan/auditoria-integra-2026-08-25`, no en `main`. Es verificable, pero no es todavía el estado canónico de la rama pública principal.

## 3. Qué acepta esta ronda y queda cerrado

- La densidad `0,0074` era incompatible con `N` y `E`; el overflow `int32` está establecido.
- El factor `36×` se retira; quedan conteo `4.014.518`, `26,60%` y rank `1/41` contra el null comunitario.
- `15.091.983` se debe nombrar conexiones/aristas agregadas, no sinapsis individuales.
- La Tabla 5 cambia a `4 enriquecidas / 4 depletadas / 1 dentro de expectativa` sobre 9 filas; AN queda no reproducible.
- `LIF-hard` fue evaluado, pero no sostiene el estadístico temporal porque produce métrica indefinida.
- El benchmark DBC3 debe destacar `DelayedClass`, tratar Thermal/Tracking/ContextSwitch como cercanos a empate y no vender XORMemory como victoria.
- `rho(W_mem)<1` y `static_assert` no son una garantía aplicable sin más a la célula real con tau dinámica y LayerNorm.
- `1,8` es una configuración de diseño, no una ley derivada del `95,2%` del conectoma.

## 4. Corrección sobre los nulls de densidad

La tabla del auditor dice que los «modelos nulos de densidad» deben recomputarse por el cambio de `d`. Eso solo aplica si el estadístico se define como cociente contra una densidad uniforme. No aplica automáticamente a los nulls CP/MS ni a un z-score calculado desde sus realizaciones, porque esos nulls se generan sobre la matriz y preservan sus invariantes propios.

La regla correcta es: **recalcular cada cantidad que use explícitamente la densidad errónea; no recalcular por reflejo los resultados que no la usan**. El erratum ya separa ambas familias.

## 5. Brechas que siguen abiertas de verdad

1. Depositar la v2/erratum en Zenodo.
2. Publicar o dar acceso reproducible a la documentación/código de DualBrain si se quiere auditoría externa completa.
3. Crear `dbc3_motor.h` y compilar los headers C.
4. Reproducir la corrida GPU completa de DBC3-v3.
5. Cerrar el match Python↔C con pesos exportados y tolerancia declarada.
6. Reemplazar los pesos placeholder del swarm por pesos versionados y verificar su salida.
7. Documentar en el paper el motivo exacto por el que LIF-hard queda fuera del resultado temporal.

## Veredicto final

La ronda final ya no cuestiona el núcleo de las correcciones: lo fortalece. Pero su condición de cierre está mal formulada: **no es `DOI público + dbc3_motor.h + commit URL activa`**, porque el DOI y el commit ya son verificables. La condición real es:

> **v2 depositada + reproducción C/GPU de DualBrain cerrada + documentación metodológica completa.**

--- METODO TITAN ---
Accion delicada: NO. Se redactó y versionó una respuesta; no se publicó la v2 ni se modificó código de producto.
Modo aplicado: TITAN FULL
Rubrica: N/A (respuesta de peritaje)
N/A declarados: ejecución GPU/C, publicación Zenodo y acceso al repo privado; no se ejecutó nuevo benchmark.
Review externo: la ronda final fue contrastada; sus aciertos se conservan y sus dos afirmaciones factuales se corrigen con evidencia directa.
Instrumento: búsqueda web en vivo para DOI; GitHub MCP para leer el archivo y el commit; evidencia cruda en la fuente versionada.
