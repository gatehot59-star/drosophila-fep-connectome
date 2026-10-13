# 2026-10-13-001 · La auditoría de Tao llegó a destiempo y sus hallazgos del paper siguen vivos (13-oct, 01:11 a 01:35)

Sigue a la 2026-10-12-019. Rama de evidencia: `titan/revision-auditoria-tao-2026-10-13` @ `e0bc638`.

**Veredicto primero.**

- [MEDIDO] **A destiempo, con fecha y hora.** El único commit de Tao (`dd9da1c`, PR #28) es de las 00:17:41 del 13-oct y audita `main` en `51e183c` (la 017, commit de las 22:48 del 12). Su encabezado dice "re-verificación contra HEAD vivo: 00:30", una hora posterior a su propio commit. A las 00:18:59 entró la 018 (`cf9caef`), a las 00:20:59 el CONTEXTO al día (`e0d5779`) y a la 01:08 la 019 (`c4f1457`). Él mismo declara que no auditó las respuestas 014 a 017 del 12-oct y que las cifras de sus bloques 2.4 a 2.6 vienen de lecturas del 12 que no reabrió.
- [MEDIDO] **Lo que no vio.** La corrida completa de la 015: el cableado real les gana a 300 SL y 300 T en 6 de 6 celdas, y la regla a mano va adelante en 4 y empata en 2. La 018: esa regla es el diseño de la mosca idealizado, no control clásico, y el motivo trae el 2,18 % de la entrada de sus seis descendentes y nada de su inhibición (36,3 %). La 019: el factorial sellado.
- [MEDIDO] **Lo que sigue vivo en el texto de la v2 hoy** (`f19a9c7`, cabeza del PR #27, sin cambios desde las 00:12): F01 en la línea 175 y en la limitación 7 (línea 345); F05, Z_CP = +14,8σ, en las líneas 13, 259, 289, 293, 355 y 401; F06, "N = 5 ... Sufficient for Z = +14.8σ", en la línea 340; F07, "138,142", en la línea 177. **No depositar la v2 sigue siendo lo correcto.**
- [MEDIDO] **F01 medido en el conectoma entero**, lo que Tao dejó como needs-runtime. La `neuropil_permutation` de agosto (blob `9b0bd4a`) preserva el in-degree global exacto en 138.639 neuronas y 15.091.983 aristas (478 bloques, 15.071.287 destinos cambiados), y el control uniforme lo rompe en 138.142. Tao tiene razón: el docstring, la §3.4 y la limitación 7 dicen lo contrario de lo que hace el código, y el nulo de neuropilo ya es el ensemble combinado grado y neuropilo.
- [MEDIDO] **F07 es más fino de lo que dice.** No es un error de tipeo: 138.142 es exactamente lo que da el control uniforme con `default_rng(7)` (reproducido hoy, y coincide con el log impreso en la 061 de agosto); 138.140 es otra corrida, la evidencia cruda archivada junto a `twohop_nulls.json`. La corrección es citar la corrida que produjo las tablas (138.140) o nombrar las dos.
- [MEDIDO] **Dos "contradicciones" ya estaban declaradas en los propios archivos.** La 2026-10-11-015 reporta en su Q3 que las semillas 0 a 3 dan 0/69 cada una, y la 2026-10-12-004 dice "una sola semilla de DBC3 llega a 0,743". Lo que vale de su crítica es el nombre ("SOLO LA SEMILLA 0" se lee mal) y el diseño (topología mezclada con semilla en la 012 a 014), no un dato escondido.
- [MEDIDO] **Robótica, se sostiene.** `adc_to_q15` multiplica `(int32_t)adc * 65536` y `q15_to_pwm` multiplica `(q + 32768) * (pwm_max - pwm_min)` en int32; los dos desbordan con `uint16_t` completos. `test_swarm.c` tiene 0 assert, abort, exit(1) o return 1. Su `recompute.py` corre igual en brain-env: exit 0, RESULTADO TODO PASS, sha256 `2dbc8e4a...` idéntico al de su informe.
- [CONCLUSIÓN] Para el paper y la robótica la auditoría vale y hay que aplicarla. Para la línea de la mosca está vieja: su P1 "reflejo contra control clásico con la misma interfaz" ya corrió en la 015, y la 018 mostró que el rival era la mosca idealizada. Su P1 "topología por semilla" sigue abierta y no es lo que mide la 019, que no entrena nada.
- [MEDIDO] **Factorial.** La corrida 1 en Actions (run 38345876729) murió en los 9 trabajos con `ModuleNotFoundError: No module named 'torch'`: el módulo de la 003 lo importa arriba y brain-env lo tiene, por eso el humo no lo vio. Reintento con torch 2.14.1+cpu en el workflow (`7534dd2`), instrumento sin cambios: run 38346117181 en curso. M46_TASA, M46_LIQ y M46_LIF terminaron OK; las seis de R1 seguían corriendo a las 04:27 UTC. El resultado va en la 2026-10-13-002.

## Pedido
"PRIMERO REVISA ELA AUDITORIa de tao. esta en destiempo . la hizo con datos de hace 3 horas. luego corre el factorial" (13-oct, 01:11).

## Herramientas y máquina
- ClickUp: búsqueda y lectura del Doc de Tao, de su DM a Abraham (00:19) y de la tarea 86e3p74xa. Sin escrituras salvo el Doc de esta respuesta.
- GitHub MCP: lectura del PR #28 y del informe (blob `d2fe97c`); commits de main; rama nueva `titan/revision-auditoria-tao-2026-10-13` (`e0bc638`); `CORRER` y arreglo del workflow en `titan/factorial-mosca-2026-10-13` (`283c52b`, `7534dd2`); este archivo en main.
- brain-env: seis clones a profundidad 1 (main `c4f1457`, PR #27 `f19a9c7`, agosto `4fc50c5`, escape `cc531e7`, swarm `e72f21d`, PR #28 `dd9da1c`); cotejo de texto; F01 en el conectoma entero (31,4 s); recompute de Tao; vigía de Actions por API pública. Sin GPU.
- Actions x64: dos runs del factorial (repo público, cuota 0).

## Hallazgo por hallazgo, contra el estado vivo

| Tao | Lo que dijo a las 00:17 | Estado medido a la 01:25 | Veredicto |
|---|---|---|---|
| F01 | el nulo de neuropilo preserva el in-degree global; el texto dice que no | texto igual en f19a9c7 (175, 345); el código hace lo que él dice; medido en 138.639 neuronas | Tao tiene razón; abierto |
| F02 a F04 | corregidos en ed7c3ac | siguen corregidos en f19a9c7 | cerrados en la 018 |
| F05 | Z_CP +14,8σ central sin Tabla 8 reproducible | 6 apariciones en f19a9c7 | abierto; decide Abraham, como dijo la 018 |
| F06 | con N = 5 el piso de p es 1/6 | la línea 340 dice "Sufficient" | Tao tiene razón; abierto |
| F07 | 138.142 no coincide con el log (138.140) | 138.142 sale de default_rng(7) y del log de la 061; 138.140 de la evidencia archivada | parcial: son dos corridas; citar la de las tablas |
| 011 | el p agrupado no generaliza entre semillas | sin cambios | de acuerdo; angostar |
| 012 a 014 | la firma mezcla topología y semilla | sin cambios | de acuerdo; es su P1 y sigue abierta |
| 2026-10-11-015 | la etiqueta "solo la semilla 0" está contradicha | el propio archivo dice 0/69 para las semillas 0 a 3 (Q3) | nombre malo, dato declarado; renombrar |
| 2026-10-12-004 | "nadie aprende" exagera | el propio archivo dice "una sola semilla de DBC3 llega a 0,743" | titular exagerado, dato declarado; angostar |
| P1 rival clásico | comparar con la misma interfaz | corrió en la 015; la 018 mostró que el rival es la mosca idealizada | superado; la pregunta nueva es la 019 |
| swarm | overflow int32 y test sin asserts | código leído; 0 asserts | Tao tiene razón |
| recompute | 11 PASS | 11 PASS en brain-env, sha256 igual | reproduce en otra máquina; mismo instrumento, no independiente |

## Antes de ver el factorial: lo que la auditoría le pega a la 019
Declarado antes de que exista ningún resultado de R1. Ninguno cambia el script sellado.
1. **Una sola tirada de τ y un solo set de prueba.** W y sus nulos comparten τ (semilla 0) y la prueba (semilla 2). La comparación W contra nulos no mezcla topología con semilla, pero no dice nada de otras semillas.
2. **El contraste RECORTE cambia dos cosas.** τ se reparte con la misma semilla sobre el orden de cada sujeto: las 6 descendentes reciben las posiciones 40 a 45 en M46 y 1498 a 1503 en R1. Es el mismo tipo de mezcla que Tao marca en la 014, en chico.
3. **IGUALA no es equivalencia.** El veredicto sellado llama IGUALA a "ninguna celda distinta tras Holm". Con 2000 ensayos por celda es un empate medido, pero sin margen pre-registrado no prueba equivalencia. En el humo (40 ensayos) las 9 dieron IGUALA justamente por eso.

## Evidencia cruda
Fechas (API de GitHub):
```
PR #28 created_at 2026-10-13T03:18:05Z, commits 1, head dd9da1c (commit 2026-10-13T00:17:41-03:00), base 51e183c
51e183c respuesta(2026-10-12-017) 2026-10-13T01:48:12Z
cf9caef respuesta(2026-10-12-018) 2026-10-13T03:18:59Z
e0d5779 contexto(2026-10-12-018) 2026-10-13T03:20:59Z
c4f1457 respuesta(019) 2026-10-13T04:08:21Z
```
Cotejo sobre f19a9c7 (`docs/v2/paper1-v2.0.md`):
```
175: ... The neuropil-preserving ensemble ... and it preserves in-degree only within blocks. ...
345: 7. The neuropil-preserving ensemble approximates the NPC model ... in-degree preserved within blocks only, no combined degree-and-neuropil ensemble ...
340: 2. N = 5 for temporal CP. Sufficient for Z = +14.8σ, but tighter intervals would require N ≥ 20.
177: ... whereas drawing targets uniformly breaks it for 138,142 of 138,639 neurons.
13, 259, 289, 293, 355, 401: Z_CP = +14.8
```
Código (`src/twohop_nulls.py`, blob 9b0bd4ae6d13ebdbd082eed616b4a5c95eae05e8, rama de agosto):
```
169:    is no longer preserved exactly, only within each block.
178:            permuted[block] = g.dst[rng.permutation(block)]
```
Agosto:
```
evidencia/2026-08-24-null-anatomico-evidencia-cruda.md:52:  "nodes_with_in_degree_broken_by_uniform": 138140,
respuestas/2026-08-24-061-null-de-grado-sobre-los-2-saltos.md:71:  nodos con in-degree roto por el uniforme: 138142 de 138639
```
F01 en el conectoma entero (`results/revision_tao_2026-10-13/f01_real.log`, md5 24f9b2f050349eff3ca23337b573fc10):
```
SUJETO neuronas=138639 aristas=15091983 etiquetas=25
F01 in_degree_global_preservado_exacto=True destinos_cambiados=15071287 de 15091983
F01 conteo_por_par_de_bloques_preservado=True bloques_no_vacios=478
CONTROL uniforme rompe in_degree en 138142 de 138639 -> el chequeo puede dar rojo=True
# duracion_s=31.4
```
Archivos del 11 y del 12:
```
2026-10-11-015:20: VEREDICTO_FIRMA = SOLO LA SEMILLA 0. No se firma como regla general.
2026-10-11-015:24: Q3 (descriptivo): semillas 0 a 3 (0,9802 / 0,9844 / 0,9812 / 0,9844): 0/69 cada una; semillas 4 a 7 (...): 14, 25, 20 y 5 de 69.
2026-10-12-004:10: ... DBC3 y LSTM quedan entre 0,658 y 0,672 (una sola semilla de DBC3 llega a 0,743), contra un techo sin memoria de 2/3.
```
Swarm (`swarm/swarm_drone.h`, rama e72f21d):
```
174:    int32_t v = ((int32_t)adc * 65536) / (int32_t)(adc_max + 1) - 32768;
179:    int32_t v = ((int32_t)(q + 32768) * (pwm_max - pwm_min)) / 65536 + pwm_min;
asserts: 0   (grep -c -E "assert|abort|exit\(1|return 1" swarm/test_swarm.c)
```
Recompute de Tao en brain-env (`results/revision_tao_2026-10-13/recompute_brainenv.log`, md5 e55f71299cf4af405e027189603c3dc8):
```
exit=0
RESULTADO TODO PASS
2dbc8e4af98e4f96a703c77347bc2e37f84ed0f50bc66a89d702f1b5e8536254  recompute.py
```
Factorial, corrida 1 (`results/factorial_2026-10-13/factorial_M46_TASA.log` en 5d9d59d, igual en los 9):
```
  File ".../tools/escape_aterrizaje/escape_aterrizaje_dbc3.py", line 21, in <module>
    import torch
ModuleNotFoundError: No module named 'torch'
```
Factorial, corrida 2 (vigía, 04:27 UTC):
```
RUN 38346117181 7534dd2 in_progress
JOB correr (M46_TASA) completed success 04:22:22 04:23:22
JOB correr (M46_LIQ) completed success 04:22:22 04:23:46
JOB correr (M46_LIF) completed success 04:22:22 04:24:34
JOB correr (R1_CON_TASA | R1_CON_LIQ | R1_CON_LIF | R1_SIN_TASA | R1_SIN_LIQ | R1_SIN_LIF) in_progress
```
Humo 2 del sello (brain-env, 04:12 UTC): 9/9 `CHEQUEO INSTRUMENTO ... -> VALIDO`, agregado `CHEQUEO INSTRUMENTO_GLOBAL ancla_M46_TASA_valida=True configuraciones_validas=9/9 -> VALIDO`.

## Archivos
- Este archivo.
- Rama `titan/revision-auditoria-tao-2026-10-13` @ `e0bc638`, md5 verificados en clon limpio: `tools/revision_tao/clonar.sh` 46b622d8..., `cotejo_texto.sh` 320640ae..., `cotejo_texto_2.sh` 28cec349..., `f01_neuropilo_conectoma_entero.py` e8b67754..., `vigia_actions.py` f3305d1e...; `results/revision_tao_2026-10-13/f01_real.log` 24f9b2f0..., `recompute_brainenv.log` e55f7129....
- Rama `titan/factorial-mosca-2026-10-13`: `283c52b` (CORRER), `5d9d59d` (el bot commiteó los logs de la corrida 1 fallida), `7534dd2` (workflow con torch y CORRER del reintento).

## NO MEDIDO
- F01 con la asignación real de neuropilo dominante: el archivo no está en brain-env; medí con otra partición. La propiedad no depende de la partición, pero no es la corrida del paper.
- Swarm con UBSan: no compilé ni corrí `swarm_probe.c`; leí el código.
- Tabla 8, los 34 contratos de H4 y el nombre TOPO: no los toqué.
- El resultado del factorial: corriendo.
- CONTEXTO sin actualizar en esta respuesta: va con la 002.
- No comenté en el PR #28 ni le escribí a Tao: es mensaje a otro y espera el visto bueno de Abraham.

## Antes de firmar
| Afirmación | Instrumento | Podía dar rojo |
|---|---|---|
| Tao leyó estado viejo | fechas de commit por API | sí |
| F01 cierto en el conectoma | bincount antes y después, más control uniforme | sí: el uniforme rompe 138.142 |
| F05 a F07 abiertos | grep sobre f19a9c7 | sí: si el texto hubiera cambiado, no aparecía |
| F07 son dos corridas | default_rng(7) reproduce 138.142 | sí: podía dar otro número |
| recompute reproduce | exit y sha256 | sí |
| el factorial corre | API de Actions | sí: la corrida 1 dio rojo |

--- METODO PROMETEO ---
Accion delicada: no (lecturas, una rama titan de evidencia, un arreglo de workflow en rama titan; nada mergeado)
Maquina: brain-env | Actions x64
Artefactos: docs/agents/respuestas/2026-10-13-001-la-auditoria-de-tao-llego-a-destiempo-y-sus-hallazgos-del-paper-siguen-vivos.md + Doc de ClickUp 2026-10-13-001
