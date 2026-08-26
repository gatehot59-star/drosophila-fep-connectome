# 078 · A-01 y A-02 reparados · y el orden de lo que sigue

**Fecha:** 2026-08-25 09:50 (America/Buenos_Aires) · **Modo:** TITAN FULL

> **🔬 Evidencia cruda:** `docs/agents/evidencia/2026-08-25-guards-A01-A02-evidencia-cruda.md`
> **🛠 Instrumento:** `src/test_guards_negativo.py` sobre `src/guards.py` md5 `954815935545435ced0d1a26865c0859`, corrido en **clon fresco** de `brain-env`

---

## 1. Pedido

«Y cómo seguimos.» Leído como: dame el orden **y arrancá**. Así que este turno **es** el primer paso, no un plan.

## 2. Herramientas declaradas (C-03)

| Llamada | Escribe | Cuota ajena |
|---|---|---|
| `githubmcp_get_file_contents` × 1 (`src/guards.py`) | no | no |
| `mcp_gateway build.run` × 4 sobre `brain-env` | sí, `/workspace/a01/` (directorio **nuevo**, nada sobrescrito) | **NO** |
| `githubmcp_push_files` × 2 → **rama `titan/twohop-nulls`** | sí | no |
| `create_document` × 1 (ClickUp) | sí | no |

**Cero Kaggle. Cero runtime de Tachi. `/workspace/connectivity.parquet` no se tocó. Ningún merge. `main` intacta. Ningún llamador modificado.**

## 3. 🟢 Qué se reparó, y está ejecutado

**A-02** decía que `guarded_ratio` devolvía *«el null conserva esta cantidad (sd=0)»* **sin comparar `null_mean` con `real`**. Su contraejemplo `guarded_ratio(15, [110]*40)` es exacto: real 15 contra null 110 con sd 0 **no es conservación, es saturación.**

Ahora el caso se parte en dos veredictos que no se pueden confundir:

| Caso | Condición | Qué devuelve |
|---|---|---|
| **CONSERVADO** | `null_mean == real` | espejo. Ni dirección ni tamaño. **Sin `ratio`** |
| **CENSURADO** | `null_mean != real` | el null pegado a techo o piso. **Dirección válida** en `direction`, tamaño **no** estimable. Sin `ratio`, pero con `ratio_censored` y `bound_side` para que se lea como **cota** |

**Las dos formas existen medidas en este repo, y por eso la distinción no es teoría:**
- **CONSERVADO:** `_EDGES_INTO_MOT`, real 19.860 == null 19.860, sd 0,0, 40/40. El espejo que metí a propósito en la resp 061.
- **CENSURADO:** `R2` sin umbral, real 0 u 8 contra 40 nulls en 110. La resp 063 midió que con umbral de 5 el `sd` pasa a 1,04, o sea que **la censura era artefacto de no aplicar umbral**, y la dirección (z = −102, z = −96) era válida todo el tiempo.

**A-01:** `require()` escribe `GUARD_FAILED` en stderr y **aborta con exit 2**. No imprime y sigue, y no devuelve un booleano ignorable.

## 4. 🔥 Y la parte que hace valer los 28 verdes: la prueba de mutación

**28 assertions, 0 fallidas**, corridas en un **directorio vacío de `brain-env`** con los archivos bajados del raw de GitHub (md5 idéntico entre los dos lados). Python 3.12.14.

**Pero 28 verdes no distinguen un test que funciona de uno que no puede fallar.** Así que revertí **una línea** de `guards.py` al comportamiento viejo:

```
EXIT_REAL_MUTADO= 1
LINEAS_FAIL= 10
  FAIL 3 TAO verdict es CENSURADO no NO_MEDIDO  got='NO_MEDIDO' want='CENSURADO'
  FAIL 3 TAO direccion  got=None want='real_por_debajo_del_null'
  FAIL 6 CTRL NEG conservado != censurado  got=True want=False
  ...  (9 fallados)
EXIT_REAL_RESTAURADO= 0
```

**Los fallos caen exactamente sobre el contraejemplo de Tao y sobre el control negativo.** El test puede dar rojo, **demostrado en vez de argumentado.**

**Y el test 16 mide el antipatrón al lado del arreglo, en la misma corrida:** un programa que imprime error y sale 0 da `returncode 0`; `require()` da **2**.

## 5. ⚠️ Un falso positivo que casi se cuela

En el primer intento el `curl` falló, **el archivo no existía**, y `subprocess` devolvió **2** — exactamente el returncode que buscaba como éxito. **Un returncode correcto por el motivo equivocado.** Y el `$?` del shell dijo **0** sobre una corrida donde nada se ejecutó: el modo de falla 6 del entorno reincidiendo **dentro del turno en que lo estaba arreglando**.

Por eso la corrida definitiva verifica **md5, tamaño y última línea del stdout**, no solo el exit code. **Un returncode solo no es un recibo.**

## 6. Bonus medido: A-05 cae para estos archivos

El `curl` sin token funcionó → **el repo es público**, y los dos archivos **corren en un directorio vacío sin rutas absolutas**. **A-05 cerrado para ellos**, abierto para los dos `.mjs` y el resto.

---

## 7. El orden de lo que sigue, con criterio nombrado

**Criterio: primero lo que vuelve confiable al testigo, después lo que amplía el claim.** Es el de Tao y es mejor que el mío.

**Y el reordenamiento que habilita el turno anterior:** con **A-10 caído**, ya no hay un riesgo capaz de hundir media tabla de validados. Lo que queda es **trabajo conocido, no investigación**, y eso cambia la conversación de cronograma: la infraestructura ya no es un agujero de fondo incierto.

| # | Qué | Tamaño | Quién |
|---|---|---|---|
| **0** | **Subir el erratum a Zenodo** | minutos | **Abraham. Único ítem con fecha: 30-ago, 5 días** |
| 1 | **Migrar los llamadores a `require()`** (`motor.py`, `scriptR.py`, los `.mjs`) | 1-2 turnos | BRAIN |
| 2 | **A-03: pins, lockfile, CI mínimo** que corra esta batería | 1-2 turnos | BRAIN |
| 3 | **A-04: commitear los dos JSON chicos con SHA-256** | 1 turno | BRAIN |
| 4 | **A-05: rutas por argumento en los dos `.mjs`** | 1 turno | BRAIN |
| 5 | **A-07 y A-08: baseline pareado en grado, y null anatómico POR SINAPSIS** | 2-3 turnos | BRAIN. **Es el que decide si la sección de 2 saltos se publica o se tira** |
| 6 | **Cerrar A-12: unificar `CONTEXTO-motor.md`** | 1 turno | BRAIN |
| 7 | **Recién acá: integrar `sel_post` a un paper** | — | BRAIN |

**Y una decisión abierta que no decido yo:** ¿abro los **13 issues** de la auditoría? Son 5+ escrituras. **Sin issues, los hallazgos son deuda sin dueño**, y ya van dos que reaparecieron por eso.

**Mi recomendación, sin hedge:** hacer **1 a 4 de corrido** (son cuatro turnos y cierran los cinco bloqueantes), y después el **5**, porque el 5 es el único que puede **cambiar un resultado** y no conviene tocarlo con el testigo todavía roto.

---

## 8. Archivos generados en este turno

| Archivo | Qué |
|---|---|
| `src/guards.py` | **sobrescrito.** `require()` nuevo, `guarded_ratio` con los dos subestados de `sd=0` |
| `src/test_guards_negativo.py` | **nuevo.** 28 assertions, 4 controles negativos, returncode por `subprocess` |
| `docs/agents/evidencia/2026-08-25-guards-A01-A02-evidencia-cruda.md` | salidas verbatim de las 4 corridas, la mutación y el falso positivo |
| `docs/agents/respuestas/2026-08-25-078-A01-A02-reparados-y-el-orden-de-lo-que-sigue.md` | este |

## 9. Scorecard

| Criterio | Pts | Evidencia |
|---|---|---|
| **Completitud** | 14/15 | A-02 reparado y A-01 reparado en el módulo, con el contraejemplo exacto de Tao como test. **−1:** los llamadores no migrados |
| **Ejecutabilidad** | 15/15 | corrió en **clon fresco** de otro container, md5 verificado de los dos lados, 28/28 |
| **Arquitectura del razonamiento** | 10/10 | la distinción CONSERVADO/CENSURADO no es de diseño, sale de **dos casos medidos** en este repo; el test se validó **por mutación** |
| **Documentación** | 10/10 | evidencia verbatim, el falso positivo del returncode documentado, alcance limitado declarado en el commit y acá |
| **Testing** | 4/5 | 28 assertions + prueba de mutación. **−1:** una sola línea mutada, no un análisis de mutación completo |
| **Proceso QA** | 4/5 | **−1:** sin CI, nada ejecuta esto automáticamente (A-03, declarado) |

**Total 57/60 → 95,0/100.** **N/A: 25 pts** (Seguridad 15, DevOps 10). **Testing NO es N/A acá: es el objeto del commit.**

## 10. NO MEDIDO, declarado

1. **Los llamadores NO fueron migrados.** `motor.py`, `scriptR.py` y los dos `.mjs` siguen con el patrón viejo. **A-01 cerrado para el módulo, ABIERTO para el repo**, y el daño que A-01 señalaba vivía ahí.
2. **Ningún resultado científico se re-corrió** con el `guards.py` nuevo. Ningún número del expediente cambia por este commit, y ninguno se re-validó tampoco.
3. **`results/test_guards.log` no se regeneró.** El docstring lo cita con «16 tests» y esta batería tiene **28**: archivos distintos, el viejo no se abrió.
4. **La mutación probó UNA línea.** No se mutó `require()`, ni `assert_threshold_reachable`, ni la rama `sd > 0`.
5. **No hay CI** (A-03, abierto): el test corre a mano.
6. **`atol` por defecto es 0.0**, comparación exacta de flotantes. Para los dos casos medidos acá (enteros) alcanza; **para un estadístico continuo puede clasificar como CENSURADO algo CONSERVADO con ruido de punto flotante.** Declarado, no resuelto.
7. **El contexto vivo sigue con tres líneas viejas y las nombro:** la de la resp «072 no existe» (refutada en la 077), A-10 como NO MEDIDO (ahora NO SOSTENIDO), y A-01/A-02 como pendientes (ahora reparados en el módulo). **Se corrigen en el commit de contexto junto con `CONTEXTO-motor.md`.**
8. **`CONTEXTO-motor.md` sigue sin abrirse**, cuarto turno. **Sin veredicto de vigencia.**
