# 2026-11-01-02 · Auditoría de H_REUSO_ESTRICTO: el veredicto aguanta; en FlyWire el exceso es de proporción y de reuso, no de cantidad, y el nulo no separa el signo del destino del cierre

Doc: https://app.clickup.com/90171457413/docs/2kza6fw5-26157 (sección 15)

**Pedido literal:** «AUDITA ESTE TRABSJO Y MEJORA» (Abraham, 1-nov-2026, 13:39 ART), con el Doc de Topo inverso seleccionado.

**Quién audita:** la misma instancia que ejecutó y publicó la 005. **No es una auditoría independiente (W-01).** El testigo es el instrumento de esta auditoría y su salida cruda, commiteados en `docs/auditorias/evidencia/2026-11-01-02/`. La elección de qué mirar sigue siendo mía y arrastra el mismo sesgo de selección que la 005.

## 0. Cómo interpreté el pedido

«Este trabajo» es la entrega H_REUSO_ESTRICTO completa: el sello `750f89a`, el instrumento y su workflow `5497aa5`, la salida del runner `0bc09b6`, el verificador `6db5d08`, la respuesta 005 (`a8348e3`) con su cierre anclado (`2bfd23e`), el CONTEXTO y la sección 14 del Doc.

«Mejora» es que BRAIN corrija lo que esta auditoría encuentra y mida el hueco más caro antes de G1, en una entrega aparte: la respuesta 2026-11-01-006. Si querías auditar toda la línea Topo inverso, de la 001 a la 005, pedí «AUDITÁ 001 A 005».

## 1. Veredicto

**El veredicto preregistrado se sostiene y el recibo es íntegro.** Bajé de nuevo los dos archivos crudos del runner, el verificador publicado y su log: los cuatro SHA256 coinciden. Re-ejecutado sobre esas copias, el verificador sale 0, rechaza los cuatro recibos corruptos y su salida es idéntica al bloque publicado. Las 400 filas cumplen T1 = n_pares_ffi / n_cab. Cada número de la 005, del CONTEXTO y de la sección 14 coincide con el JSON.

**Cuatro rojos:**

- **R1 · En FlyWire sobra proporción y reuso, no cantidad.** El grafo real tiene 880 pares con plantilla; los 200 nulos estrictos, entre 932 y 1.060. T1 sube porque el cableado directo real se concentra en 996 pares, contra 1.582 a 1.682 en todos los nulos. Las frases «no eliminó el exceso del motivo» y «más frecuente que en los barajados» dicen más de lo que el instrumento midió. E-01.
- **R2 · El no-invariante que decide G1 quedó sin dueño.** El nulo estricto no conserva el signo del destino dentro de cada clase. Si las proyecciones visuales prefieren destinos inhibitorios, una G0 por clase × signo podría reproducir el exceso sin cierre específico. La 005 lo declaró no conservado, pero no lo pasó a ningún pendiente y habilitó G1 antes de ese falsador, que es más barato. Pendiente sin dueño y O-01.
- **R3 · Ninguno de los turnos 001 a 005 cerró en el pizarrón.** La última línea de BRAIN en `reportes` es la 142, de las 03:19 ART, sobre el piloto OCR.
- **R4 · El QA de la 005 estaba inflado en dos puntos.** Documentación 10/10 no sobrevive a R1 y R2: con 8/10 queda 56/60 = 93,3/100. Sigue sobre el umbral; el número publicado no era ese.

**Lo que no se midió y importaba:** si las inhibitorias cierran justo los pares que están cableados, con el mismo denominador; si el signo del destino explica el exceso; una segunda implementación de T1 y T2 sobre los grafos reales; y la reproducción del ensemble desde sus semillas en otra máquina. Los cuatro pasan a la mejora (sección 7).

## 2. Qué corrí, dónde y con qué

- **brain-env, Python 3.12.14.** Descarga fresca desde `raw.githubusercontent.com` de `estricto.json` y `run.log` en `0bc09b6`, y de `verificar_estricto.py` y `verificacion.log` en `6db5d08`. Ejecución de `auditoria_estricto.py`: exige los cuatro SHA256, re-ejecuta el verificador como subproceso, compara su salida con la publicada y calcula los descriptivos. Control negativo del propio instrumento: un byte cambiado en el JSON da `MISMATCH` y exit 2.
- **API pública de GitHub.** Commits de main y de la rama estricta con sus fechas, y runs de Actions creados desde las 14:00 UTC.
- **Pizarrón `nexus.db` por su servicio `sqlite`, solo lectura.** Mensajes sin leer para BRAIN, `reportes`, `trabajos_vivos` y búsqueda de esta línea en `mensajes`. Listado de `docs/agents/` buscando órdenes `ORDEN-*`.
- **ClickUp.** Lectura completa del Doc de Topo inverso, secciones 1 a 14.
- Sin GPU ni Kaggle, sin tocar el ensayo ni sus ramas. No recalculé estadísticos desde los grafos: el taller tiene 2 núcleos y unos 1,9 GiB libres. Eso va a Actions en la mejora.

## 3. Afirmaciones auditadas

| # | Afirmación | Dónde | Instrumento | ¿Podía dar rojo? | Veredicto |
|---|---|---|---|---|---|
| 1 | Corrida VÁLIDA, 400/400 nulos con guardas aprobadas | 005 §1, CONTEXTO l.12 | JSON fresco y verificador re-ejecutado | Sí: plan incompleto o guarda apagada se rechazan | CONFIRMADO. Las banderas de guarda las escribió el productor; la mutación de clase prueba que podían fallar |
| 2 | Cero superaciones, p = 1/201, Holm = 4/201 | 005 §1 | conteo directo y verificador con fracciones exactas | Sí | CONFIRMADO |
| 3 | FlyWire: T1 88,35 % contra media 61,17 % y máximo 64,22 %; T2 698 contra 565,02 y 607 | 005, CONTEXTO, Doc §14 | JSON | Sí | CONFIRMADO |
| 4 | BANC: T1 82,60 % contra 35,68 % y 39,68 %; T2 419 contra 112,385 y 141 | 005, CONTEXTO, Doc §14 | JSON | Sí | CONFIRMADO |
| 5 | Denominadores nulos de 1.582 a 1.682 y de 877 a 937 | 005 l.29 | JSON | Sí | CONFIRMADO |
| 6 | Fracción movida mínima 0,99448 y 0,99502; 200 huellas distintas por serie | 005, Doc §14 | JSON | Sí | CONFIRMADO |
| 7 | X compartidas por superclase y `AN_multi_11` como `ascending` | 005 §2, CONTEXTO l.11 y l.14 | descriptivos del JSON | Sí, contra las sumas 698 y 419 | CONFIRMADO |
| 8 | 396,73 s y 2,907 GiB de RSS | 005, CONTEXTO l.15 | `seconds` y `maxrss_kib` del JSON | Sí | CONFIRMADO |
| 9 | Sello antes del instrumento y antes de mirar resultados | 005 l.13 | fechas de commit y de run; mtimes del taller | Sí para el orden; no para «mirar» | Orden CONFIRMADO: 15:13:01Z, 15:20:14Z, 15:20:16Z. «Sin mirar» queda NO MEDIDO más allá de que el taller no tiene salida real estricta antes de 15:28:10Z |
| 10 | Humo ciego, sin publicar métricas inferenciales | 005 l.55 | `run.log`, líneas 515 a 522 | Sí | CONFIRMADO: solo guardas y validez. El ciego no tuvo función de decisión, porque humo y corrida completa van en el mismo job, sin intervención humana |
| 11 | «No eliminó el exceso del motivo» | 005 l.9, CONTEXTO l.12, encabezado y §14 del Doc | conteo de `n_pares_ffi` y `n_x` en los 400 nulos | Sí | CONFIRMADO para T1 y T2 tal como se sellaron; REFUTADO como cantidad en FlyWire (R1) |
| 12 | «Más frecuente que en los barajados probados» | Doc §12 | mismo conteo | Sí | REFUTADO en FlyWire bajo el nulo estricto (R1) |
| 13 | El verificador no recalcula grafos | 005 y CONTEXTO l.15 | lectura del código | No aplica | CONFIRMADO: recuenta la inferencia. T1 y T2 reales salen de una sola implementación |
| 14 | Mi candidato: Doc §2, §5, §9 y §12 todavía con «pendiente» | Doc | lectura completa | Sí | REFUTADO: ya estaban actualizados en el cierre de la 005 |
| 15 | QA 58/60 = 96,7/100 | 005 §7 | re-puntuación con R1 y R2 | Sí | REFUTADO: 56/60 = 93,3/100 (R4) |

## 4. Los rojos, con números

### R1 · Proporción y reuso, no cantidad, en FlyWire

De la salida cruda (sección 8):

- **Pares con plantilla en FlyWire:** real 880. Nulos: media 994,28, mínimo 932 y máximo 1.060. **Los 200 nulos igualan o superan al real**, z = −5,28.
- **Pares cableados en FlyWire:** real 996; nulos de 1.582 a 1.682, z = −33,79.
- **X que participan en FlyWire:** real 1.118; media 1.100,3. **53 de los 200 nulos igualan o superan al real.**
- **T2 por X en FlyWire:** real 0,6243; máximo nulo 0,5552.
- **BANC:** 622 pares con plantilla contra máximo 361; 716 X contra máximo 329; T2 419 contra máximo 141. Ahí sobra todo.

Qué significa: en FlyWire, la proporción de pares cableados que tienen la plantilla es mucho mayor que en el azar estricto. Pero eso ocurre porque el grafo real concentra su cableado directo en menos pares, no porque tenga más plantillas. Lo que sí sobra en FlyWire, sin ambigüedad, es el **reuso**: más X sirven a dos o más tipos de descendente, y por X la proporción supera a todos los nulos. Ese resultado es conservador, porque los nulos tenían más pares cableados, o sea más oportunidades, y aun así quedaron debajo.

La 005 declaró que el denominador cambia. En su línea 29 dice: «Por eso T1 no es un contraste con el mismo número de pares en cada red». Pero no midió la consecuencia. Las frases de cabecera se leen como «hay más motivos que en el azar», y en FlyWire eso es falso como cantidad. Regla incumplida: E-01, la frase habla de un conteo y el instrumento medía una proporción.

Corrección que corresponde: «la plantilla aparece en una proporción mayor de los pares cableados y sus X se reusan más que en el azar; en FlyWire, el número absoluto de pares con plantilla es menor que en todos los nulos». Y medir T1 con el mismo denominador (sección 7).

### R2 · El signo del destino, declarado y sin dueño

La 005 lista entre lo no conservado la «composición inhibitoria dentro de cada clase», en su línea 39. Es el no-invariante que decide si G1 tiene algo que agregar.

El nulo estricto baraja las filas de cada S entre destinos inhibitorios y excitatorios de la misma superclase. Si las S prefieren destinos inhibitorios, una preferencia de primer orden, el nulo la destruye y baja por construcción los caminos S→X→D. Eso daría exceso en T1 y T2 sin que exista cierre específico sobre los pares cableados, que es lo de segundo orden. La dirección no está medida: si las S evitan las inhibitorias, el sesgo va al revés.

Ese hueco no pasó a ningún pendiente. La 005 §6 y el CONTEXTO l.20 nombran signos desconocidos, superclase, geometría, fuerza entrante, vecinos únicos y MOSCA_L, no el signo del destino. La decisión habilitada fue G0/G1, más cara que un nulo que conserve clase × signo. Patrón: pendiente declarado sin dueño, más O-01. Estado científico: NO MEDIDO, no REFUTADO.

### R3 · Turnos sin cierre en el pizarrón

`reportes` termina en la fila 142, de BRAIN, con fecha `2026-11-01 06:19:52` UTC (03:19 ART), sobre el piloto OCR. No hay filas de los turnos 001 a 005, que corrieron entre las 04:55 y las 12:37 ART. El ciclo de contexto pide una línea por turno. Es un rojo de proceso, chico, y su costo es que la próxima instancia reconstruya el estado desde git.

### R4 · QA inflado en dos puntos

La 005 dio Documentación 10/10. R1 y R2 son fallas de documentación del resultado: una consecuencia del denominador sin reportar, una frase de cabecera ambigua en cuatro lugares y un no-invariante decisivo sin pasar a pendientes. Con Documentación 8/10 quedan 15 + 15 + 14 + 8 + 4 = 56/60 = 93,3/100.

## 5. Patrones cazados sin rojo

- **Instrumento que no podía dar rojo:** no. La mutación de clase da 23/25 y exit 3, y el verificador exige esa evidencia en el log. El motivo ausente da REFUTADA. Los cuatro recibos corruptos se rechazan, y los vi rechazarse yo al re-ejecutar. Holm también podía fallar: con 200 nulos, la menor p ajustada solo pasa con una superación o ninguna.
- **Instrumento contaminado:** no. El JSON lo commiteó el bot de Actions (`0bc09b6`) con `github_run_id` 41320710194 y `source_sha256` igual al instrumento. Ningún valor estricto aparece en un mensaje de commit anterior al resultado.
- **Sujeto o momento equivocado:** no para el orden. Sello a las 15:13:01Z, instrumento a las 15:20:14Z, run creado a las 15:20:16Z. En el taller, el instrumento local tiene mtime 15:15:26Z, posterior al sello, y no hay salida real estricta antes de 15:28:10Z. El verificador final se escribió a las 15:27:40Z, después del resultado: es un recuento, no una elección de diseño.
- **Documento vencido:** mi candidato (Doc §2, §5, §9 y §12) quedó refutado. La línea 170 del CONTEXTO, en la cola histórica, sigue listando «sellar H_REUSO_ESTRICTO» en «Espera decisión de Abraham», pero la cubre la regla de precedencia de la línea 21. Sin rojo.
- **Canal sin leer:** 30 mensajes sin leer para BRAIN en el pizarrón, del 1-sep al 5-oct, todos de MUDH, SIAO, Custos y Outlier; ninguno de esta línea. No hay órdenes `ORDEN-*` en `docs/agents/` del conectoma. En `trabajos_vivos`, la fila 16 (reciprocidad y KC→MBON contra nulos CP) es de esta línea y sigue «propuesto y nunca lanzado», ajena a H_REUSO. Sin rojo para esta entrega.
- **Cadena de suministro:** acciones fijadas por SHA, versiones exactas, `contents: write` y timeout de 45 minutos. Connectivity baja de la rama `main` de su repo, que es mutable, pero el instrumento la exige por SHA256 y falla cerrado. pip instala sin `--require-hashes`. Riesgo bajo, sin rojo.
- **Workflows ajenos:** «H4 integrated regression» corrió en cada push de la rama estricta (`750f89a`, `5497aa5`, `6db5d08`), las tres veces success, y no escribió: la cabeza sigue en `6db5d08`. Sin rojo.

## 6. Lo que no pude auditar

- La verdad de las guardas más allá de lo que escribió el productor. Leí sus banderas; la mutación prueba que podían fallar, no que cada una sea cierta.
- T1 y T2 recalculados sobre los grafos reales con otra implementación, y la reproducción del ensemble. Necesitan los datos cargados: van a Actions en la mejora.
- La selección de qué medir por alguien que no escribió el código. Esta auditoría es de la misma instancia.
- Las líneas 001 a 004, fuera del sujeto declarado. La auditoría 2026-11-01-01 cubrió la primera versión de la 001.

## 7. Qué le toca a BRAIN

Criterio de orden (O-01): primero corregir lo publicado que hoy dice más de lo medido; después, el falsador más barato que podría quitarle a G1 su razón de ser.

1. **Corregir R1 donde se publicó:** CONTEXTO, Doc (encabezado, §12 y §14) y una respuesta nueva, la 006. La 005 es append-only: no se reescribe.
2. **Sellar y correr H_REUSO_CIERRE antes de su instrumento.** Filas S→D elegibles fijas, para que T1 tenga el mismo denominador que el real. Todas las demás se barajan conservando, para cada origen, filas y peso por lado, superclase, signo y rol del destino. Mismas T1 y T2, 200 nulos por conectoma, Holm. Responde R1 y R2 en una sola corrida, y se declara que la variante se eligió después de ver el estricto.
3. **En la misma corrida:** paridad de T1 y T2 con una implementación dispersa independiente sobre los grafos reales, y reproducción de las 400 huellas del estricto desde sus semillas.
4. **Cerrar el turno en el pizarrón (R3).**

G1 sigue sin diseño.

## 8. Evidencia cruda

Instrumento: [`auditoria_estricto.py`](evidencia/2026-11-01-02/auditoria_estricto.py), SHA256 `d5a2610e12d86e4bca7907af28fbfd0b100603deb12fe3f41c31c61b5a78b4c8`, 6.102 bytes. Salida íntegra: [`auditoria_estricto.log`](evidencia/2026-11-01-02/auditoria_estricto.log), SHA256 `6ddb11e35351ddde080338030e859262a14e0f860da7e171736d7c737be16c6a`, 3.590 bytes, exit 0 en la corrida real y exit 2 en el control negativo.

Líneas decisivas, tal cual:

```plain
verificador re-ejecutado: exit=0 stdout_bytes=2411 stdout_sha256=05cecf82e9090af595e1139908163dba0e0d94becf902796eab34313eaac7915 igual_al_bloque_publicado=True stderr_bytes=0
flywire n_cab real=996 media=1625.4550 sd=18.6296 min=1582 max=1682 nulos_ge_real=200 nulos_le_real=0 z=-33.79
flywire n_pares_ffi real=880 media=994.2800 sd=21.6586 min=932 max=1060 nulos_ge_real=200 nulos_le_real=0 z=-5.28
flywire t2 real=698 media=565.0200 sd=18.9578 min=515 max=607 nulos_ge_real=0 nulos_le_real=200 z=7.01
flywire n_x real=1118 media=1100.3250 sd=27.2410 min=1035 max=1182 nulos_ge_real=53 nulos_le_real=151 z=0.65
flywire t2_por_x real=0.624329 media=0.513565 min=0.475588 max=0.555246 nulos_ge_real=0
banc n_pares_ffi real=622 media=324.0800 sd=15.6739 min=283 max=361 nulos_ge_real=0 nulos_le_real=200 z=19.01
banc n_x real=716 media=285.3750 sd=15.5329 min=240 max=329 nulos_ge_real=0 nulos_le_real=200 z=27.72
```

Fechas, desde la API de GitHub:

```plain
750f89adb4b8710bd0d4d7105af1c7073296dd90 2026-11-01T15:13:01Z sello(reuso-estricto)
5497aa569450415b2101e2ea0f99680a3c540dbe 2026-11-01T15:20:14Z feat(reuso-estricto)
41320710194 reuso-estricto-2026-11-01 push 5497aa5 completed success created 2026-11-01T15:20:16Z
0bc09b6736e43b1ee66ac265a94f0fdfe91480f2 2026-11-01T15:27:23Z github-actions[bot] medicion(reuso-estricto)
6db5d089efa71199f775d1b6619b1cf9f790b7fe 2026-11-01T15:29:37Z medicion(reuso-estricto) verificador
41320087061 H4 integrated regression push 750f89a completed success
41320710155 H4 integrated regression push 5497aa5 completed success
41321493925 H4 integrated regression push 6db5d08 completed success
```

Pizarrón, servicio `sqlite`, solo lectura:

```plain
SELECT id, agente, turno, ts FROM reportes ORDER BY id DESC
142 brain 2026-11-01-cierre-cpu-sin-relanzar 2026-11-01 06:19:52
141 brain 2026-11-01-repiloto-cpu-a415b433 2026-11-01 05:31:34
140 brain 2026-11-01-auditoria-piloto-ocr 2026-11-01 04:36:01
leer_mensajes(para=brain, no_leidos=true) -> 30 mensajes, ids 148 a 246, del 2026-09-01T22:11:03Z al 2026-10-05 21:50:26
```

## 9. Rúbrica de esta auditoría

- **Completitud 8/10:** cubre todas las afirmaciones de estado de la entrega estricta y sus tres publicaciones. No recalcula los grafos.
- **Razonamiento 9/10:** R1 sale de conteos que cualquiera puede repetir con el JSON público; R2 queda como NO MEDIDO, sin inflarlo a refutación.
- **Documentación 8/10:** cada veredicto con línea, archivo o SHA.
- **Proceso 6/10:** misma instancia; el control negativo del instrumento propio solo prueba el pin, no los descriptivos.

Promedio 7,75/10. No es una auditoría independiente.

--- METODO PROMETEO ---
Rol: auditor (no BRAIN). Independencia: NO, misma instancia que ejecutó la 005.
Accion delicada: NO (auditoría y evidencia a main; no toca lo auditado).
Modo aplicado: FULL de auditoría.
Maquina: brain-env (Python 3.12.14; corrida real exit 0, control negativo exit 2), API pública de GitHub, nexus.db por el servicio sqlite (solo lectura), ClickUp (lectura del Doc).
Rubrica: completitud 8/10, razonamiento 9/10, documentación 8/10, proceso 6/10; promedio 7,75.
Review externo: no realizado.
Instrumento: docs/auditorias/evidencia/2026-11-01-02/auditoria_estricto.py, salida cruda auditoria_estricto.log en el mismo directorio.
Artefactos: docs/auditorias/2026-11-01-02-reuso-estricto-aguanta-flywire-es-proporcion-no-cantidad.md + https://app.clickup.com/90171457413/docs/2kza6fw5-26157
