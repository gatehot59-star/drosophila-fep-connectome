# Auditoría TAO del laboratorio de circuitos de la mosca

**Encargo:** tarea ClickUp 86e3p74xa, pedido versionado en `docs/auditorias/2026-10-12-pedido-auditoria-tao-laboratorio.md` (main `47d940e`).
**Auditor:** TITÁN Tao. **Fecha de lectura:** 2026-10-12. **Re-verificación contra HEAD vivo:** 2026-10-13 00:30 (America/Buenos_Aires).
**Modo:** solo auditoría. Esta rama agrega tres archivos bajo `docs/auditorias/` y no toca instrumentos, resultados, manuscrito ni `main`.

## 0. Qué se leyó y en qué SHA

| Objeto | SHA auditado | SHA vivo al re-verificar |
|---|---|---|
| `main` | `0c6722b8a4ff8f552a872baddbf62c1865e2f21a` | `51e183c4580a61969996f893434c5aaf296eb4a6` (agrega respuestas 2026-10-12-014 a 017, no auditadas) |
| PR #27, `titan/v2-cierre-2026-10-12` | `554f7d99be81f27da331dc5e736b89c5e704e8c2` | `f19a9c7bd7309a6b08eef72b29da4ab93b5a6bde` (incluye `ed7c3ac`, respuesta 018) |
| PR #26, `titan/tabla7-reconstruida-2026-10-10` | `95e8d6c47cd4eea5cd20432d3fab6146e5d31ed2` | sin cambios |
| Expediente de agosto, `titan/materializacion-h4-guard-2026-10-02` | `4fc50c58a1f34a7ab6c125c6f675f3fecf1a017c` | sin cambios |
| `titan/escape-motivo-2026-10-11` | `cc531e785f8c481472dba66ae8980d8739c15265` | sin cambios |
| `titan/brazo-s-recurrente-2026-10-11` | `947385215606df7f25c6168f023a70a740cb3fee` | sin cambios |
| `swarm/swarm_drone.h` | blob `f18b87611ecaa795be4b2c3f7a3697210c8700c0` | mismo blob en `titan/swarm-lazo-cerrado-2026-10-11` `e72f21d` |
| `src/twohop_nulls.py` | blob `9b0bd4ae6d13ebdbd082eed616b4a5c95eae05e8` | mismo blob |

Manuscrito v2.0 leído completo en `554f7d9` y otra vez completo en `f19a9c7`.

**Lo que no se hizo, dicho antes que nada.** No reproduje FlyWire ni PyTorch: no tengo el parquet de 100 MB ni brain-env. No corrí vuelo, hardware, render de PDF ni la suite H4 completa. Leer código y logs y recomputar desde conteos no equivale a correr los experimentos originales. Las respuestas posteriores a 2026-10-12-006 que no tocan la v2.0 (014 a 017 en `main`) no entran en esta auditoría.

## 1. Hallazgos que cambian el manuscrito

| Id | Afirmación | Veredicto en `554f7d9` | Estado en `f19a9c7` |
|---|---|---|---|
| F01 | §3.4 y limitación 7: el nulo de neuropilo "preserva in-degree solo dentro de bloques" y "no hay ensemble combinado grado y neuropilo" | **FAIL** | **abierto** |
| F02 | §3.4: "el spread de 323 colapsa a 2,4" | **FAIL** | corregido: 4,2 sin umbral y 40 con umbral 5 |
| F03 | §3.4: el cero de olfato y visión es invariante bajo el nulo de neuropilo | **FAIL** | corregido: z −1,2 y −0,2 sin umbral; sin varianza solo con umbral 5 |
| F04 | §2.5, limitación 3: amplificación validada en tres modelos | **FAIL** | corregido: dos de tres; LIF-soft decae 0,253 → 0,002 |
| F05 | Tabla 8 sostiene la conclusión central aunque su productor no está archivado | **FAIL** | **abierto** |
| F06 | Limitación 2: "N = 5 suficiente para Z = +14,8σ" | **FAIL** | **abierto** |
| F07 | §3.4: control negativo uniforme rompe 138.142 nodos | **FAIL menor** | **abierto** |

Las correcciones de `ed7c3ac` coinciden con F02, F03 y F04 y las recomputé (sección 4). Es una medición externa a favor de esos tres hallazgos. F01, F05, F06 y F07 siguen en el texto vivo.

### F01. El nulo de neuropilo es más fuerte de lo que el paper dice

`src/twohop_nulls.py` (blob `9b0bd4a`), función `neuropil_permutation`: `permuted[block] = g.dst[rng.permutation(block)]`. Dentro de cada bloque (neuropilo origen, neuropilo destino) los destinos se reordenan entre las mismas aristas, así que el multiconjunto de destinos de cada bloque se conserva. La unión de multiconjuntos conservados es el multiconjunto global conservado: **el in-degree global se preserva exactamente por multiplicidad**, junto con el out-degree (fuentes fijas) y el conteo por par de neuropilos. El docstring de la propia función dice lo contrario ("In-degree is no longer preserved exactly, only within each block") y de ahí lo heredan §3.4 y la limitación 7.

Recomputo: cuerpo transcrito sin cambios de lógica, 100 grafos sintéticos de 50 nodos y 700 aristas, 6 neuropilos al azar. 100/100 preservan in-degree, 100/100 cambian destinos; control negativo uniforme rompe in-degree en 100/100.

Consecuencia: el ensemble de neuropilo **es** el ensemble combinado grado más neuropilo que la limitación 7 dice que falta. La conclusión de §3.4 sale más fuerte, no más débil. Quedan como límites reales: admite autoconexiones y aristas repetidas, y el bloque es por neuropilo dominante, no por sinapsis. No lo verifiqué sobre el conectoma completo ni con asignación por sinapsis.

**Corrección propuesta:** en §3.4 reemplazar "it preserves in-degree only within blocks" por "it also preserves every in-degree exactly, since the multiset of targets within each block, and hence globally, is conserved"; en la limitación 7 quitar "in-degree preserved within blocks only, no combined degree-and-neuropil ensemble" y agregar "self-loops and repeated connections admitted"; corregir el docstring de `neuropil_permutation`.

### F02. El cociente entre extremos

De Tabla 5b del propio paper: (1413/922,850)/(901/2450,650) = 4,1645 sin umbral, y 4,871795/0,120950 = 40,28 con umbral 5. El "2,4" de `554f7d9` era visual sobre gustativo (2,42), no el cociente entre extremos. La inversión de signos es real, pero no desaparece toda la estructura residual. Corregido en `ed7c3ac` y verificado en el log `docs/v2/fix-v2-018.log`.

### F03. El cero de olfato y visión

Sin umbral, el nulo de neuropilo da medias 1,025 y 0,025 con SD de ~0,9 y ~0,16 para R1: no es invariante, el cero está dentro de la dispersión. Solo con umbral 5 la media es exactamente 0. Además, 40/40 realizaciones mayores o iguales al observado con empates no permite calcular una cola inferior. R2 tampoco satura en toda clase ni todo nulo. Corregido en `ed7c3ac`.

### F04. Compatibilidad no es replicación

Tabla 9: LIF-soft cae de 0,253 a 0,002 entre t = 60 y t = 180 (Δ = −0,251). Eso es incompatible con "amplificación validada en tres modelos". Corregido en `ed7c3ac`.

### F05. Tabla 8 sostiene la conclusión y no es reproducible

La limitación 5 confiesa que el productor de la Tabla 8 no está archivado y que cuatro particiones candidatas no reproducen la trayectoria. Pero el abstract, puntos (1) y (3), la §4.1 y el "Central finding" de §6 siguen apoyándose en Z_CP = +14,8σ, que sale de esa tabla. Un resultado que el propio autor no puede reproducir no puede ser el hallazgo central. **Opciones:** recuperar el productor y su log, o marcar la Tabla 8 como histórica no reproducida y sacar Z_CP del abstract y de las conclusiones.

### F06. Cinco nulos no dan una p chica

Con 5 realizaciones CP el mínimo p empírico es 1/6 = 0,1667. Un z de +14,8 con N = 5 mide qué tan lejos queda el observado de cinco puntos, no una probabilidad de cola. La limitación 2 dice "suficiente para Z = +14,8σ": hay que decir que con N = 5 no hay p empírica por debajo de 0,1667.

### F07. Conteo del control negativo

§3.4 dice 138.142 nodos rotos por el control uniforme; el log crudo de `2026-08-24-null-anatomico` en el expediente de agosto dice 138.140. Diferencia de dos: menor, pero es la cifra del control que hace al instrumento capaz de dar rojo y debe coincidir con su log.

## 2. Tabla por afirmación, los siete bloques del encargo

Columnas: respuesta, afirmación, instrumento, ¿podía dar rojo?, recomputado, veredicto, evidencia.

### 2.1 Paper 1 v2.0 (PR #27)

| Resp. | Afirmación | Instrumento | ¿Rojo? | Recomputado | Veredicto | Evidencia |
|---|---|---|---|---|---|---|
| 007 | Tabla 5: esperados y cocientes de 8 filas | fórmula N_clase × 1485 × densidad × P(exc) | sí | sí, 8/8 | PASS | `docs/v2/paper1-v2.0.md` §3.3 en `f19a9c7` |
| 007 | p termosensorial 0,094 e higrosensorial 1,3e−10 | binomial cola inferior | sí | sí: 0,09378 y 1,3071e−10 | PASS | `recompute.py`, `table5()`; mi primer chequeo bilateral difería y el error era mío |
| 007 | Tabla 7, 7 filas × 2 umbrales | conteos | sí | sí, todas coinciden; 2104/24326 = 8,649% → 8,6 | PASS | `recompute.py`, `table7()` |
| 007 | Tabla 10, constantes efectivas | −1/ln(1−τ) | sí | 19,4957; 7,8928; 4,4814; 2,8037 ms | PASS | `recompute.py`, `tau()` |
| 007 | Rango fisiológico 5 a 20 ms | cita Gouwens & Wilson 2009 | n/a | no | NO MEDIDO | la cita trata neuronas de proyección antenal; limitación 12 ya lo declara |
| 007 | Nulo de neuropilo solo preserva in-degree por bloque | `neuropil_permutation` | sí | sí, 100/100 | **FAIL (F01)** | blob `9b0bd4a` |
| 007 | Spread 323 → 2,4 | Tabla 5b | sí | 4,16 y 40,28 | FAIL, corregido en `ed7c3ac` (F02) | `fix-v2-018.log` |
| 007 | Cero olfato/visión invariante | Tabla 5c | sí | medias 1,025/0,025 | FAIL, corregido en `ed7c3ac` (F03) | §3.4 en `f19a9c7` |
| 007 | Amplificación en tres modelos | Tabla 9 | sí | Δ LIF-soft −0,251 | FAIL, corregido en `ed7c3ac` (F04) | §2.5 en `f19a9c7` |
| 007 | Z_CP = +14,8σ como hallazgo central | Tabla 8, productor no archivado | no se sabe | no reproducible | **FAIL (F05)** | limitación 5 contra abstract y §6 |
| 007 | N = 5 CP suficiente | 5 nulos | no para p < 0,1667 | piso 1/6 | **FAIL (F06)** | limitación 2 |
| 007 | Render determinista | pandoc + typst | sí | no | NO MEDIDO por mí | `docs/v2/render-v2.0.log` existe; no lo re-corrí |

### 2.2 Tabla 7 y control de las salidas (PR #26, respuestas 2026-10-10-002 a 009)

| Resp. | Afirmación | Instrumento | ¿Rojo? | Recomputado | Veredicto | Evidencia |
|---|---|---|---|---|---|---|
| 002 a 009 | Tabla 7 8/8 y 8,6 | script reconstruido | sí | aritmética desde conteos, no desde parquet | PASS | `recompute.py`, `table7()` |
| 002 a 009 | Salida regional: 31/33 por BY, 5 por max-T; fuerte: 41 BY, 34 Holm, 11 max-T | logs de permutación | sí | no: los logs no traen los arrays para recomputar íntegro | NO MEDIDO | logs de PR #26 en `95e8d6c` |
| 002 a 009 | La primera prueba Holm bloquea | 5000 permutaciones, 242 pruebas | sí | piso bilateral 2/5001 = 0,00040 > 0,05/242 = 0,00021 | PASS de la explicación | `recompute.py`, `holm_floor()`: el bloqueo es de resolución, no de ausencia de efecto |

### 2.3 Nulo por circuito (respuesta 2026-10-11-003)

| Resp. | Afirmación | Instrumento | ¿Rojo? | Recomputado | Veredicto | Evidencia |
|---|---|---|---|---|---|---|
| 003 | FAIL de instrumento, lectura preliminar sin firmar | nulo CP por circuito | sí, y dio rojo en su control negativo | no | PASS de la declaración | §3.6 en `f19a9c7` mantiene la Tabla 7 descriptiva; no concluir que el nulo explica el descenso |

### 2.4 Brazo S y escape (respuestas 2026-10-11-007 a 016)

| Resp. | Afirmación | Instrumento | ¿Rojo? | Recomputado | Veredicto | Evidencia |
|---|---|---|---|---|---|---|
| 010 | La mosca gana por lateralidad | McNemar exacto | sí | p = 2,84e−10 (1/37) | PASS | `recompute.py`, `mcnemar()`; rama `cc531e7` |
| 011 | La mosca gana por cableado fino | McNemar exacto | sí | p = 1,31e−59 (252/12) y 3,57e−34 (169/15) | PASS, angostar | `control_parametros.py` agrupa 4 semillas que reutilizan los mismos estímulos: el p agrupado no demuestra generalización entre semillas |
| 010, 011 | Tasas de fallo del escape | conteos | sí | 7/201 = 0,0348; 2/201 = 0,0100; 1/201 = 0,0050 | PASS | logs de `cc531e7` |
| 012 a 014 | La líquida plena gana contra su control | `firmar_plena_sl.py` | sí | firma semilla 0: 1/70 = 0,0143; peor semilla 26/70 = 0,371 | **FAIL de diseño** | compara 8 entrenamientos de 1W contra 69 topologías SL entrenadas solo con semilla 0: mezcla variación de topología con variación de semilla |
| 015 | "La firma vale solo para la semilla 0" | misma | sí | semillas 0 a 3 superan las 69 SL | **FAIL de la etiqueta** | la pregunta 1 (¿gana a cada SL?) pasa en 4 semillas; la pregunta 2 (¿gana con la varianza de semilla controlada?) es la que falla |
| 012 a 015 | md5 del pre-registro coincide con el script del log | md5 | sí | cadenas cotejadas: difícil `2c95e63b`, plena `45bad2a8`, firma `df15f3da` | PASS | no rehice el hash byte a byte de cada archivo |
| 007 a 009 | Brazo S recurrente: sin ventaja W vs shuffle | 10 semillas × 4 tareas, Holm | sí | no | PASS, angostar | solo A/F MultiCue sobrevive Holm (0,0044); W recurrente peor que B feedforward en 3/4. No significación no es equivalencia; tampoco prueba causalidad de la sparsity. Rama `9473852` |
| swarm | Lazo cerrado de enjambre | `swarm/test_swarm.c` | **no**: imprime y retorna 0, sin assertions | no | **FAIL de instrumento** | blob `f18b876`; el test no puede dar rojo |
| swarm | Helpers de hardware seguros | `adc_to_q15`, `q15_to_pwm` | sí | UBSan: dos overflows int32 | **FAIL latente** | `swarm_probe.c`: `65535 * 65536` y `65535 * 65535` desbordan `int`; con 12 bits el control da exit 0 (adc 32752, pwm 4094) |

Sobre el swarm: la API acepta `uint16_t` completos, así que el overflow es alcanzable por contrato. No afirmo que el hardware real use ese rango. Observación lateral: con 12 bits `q15_to_pwm(32767, 0, 4095)` da 4094, nunca el máximo. No simulé el vuelo de forma independiente.

### 2.5 Circuitos y DBC3 (respuestas 2026-10-12-001 a 006)

| Resp. | Afirmación | Instrumento | ¿Rojo? | Recomputado | Veredicto | Evidencia |
|---|---|---|---|---|---|---|
| 001 | Catálogo 10/10 | consulta de aristas | sí: positivo LC4→GF 757, negativo LC6→GF 0 | no | PASS como existencia de aristas | `titan/catalogo-circuitos-2026-10-12` `bb68d7f`. Confirma aristas, no función; la unión DNp07 o DNp10 no demuestra cada miembro |
| 002 | Motivo de escape | 28 nodos, 73 aristas, 665 sinapsis | sí | no | PASS, angostar | sin inhibición ipsilateral; es un motivo, no un cerebro |
| 003 | DBC3 en el techo | escape y aterrizaje | **no discrimina** | no | PASS del techo | DBC3 perfecto en 4 semillas, LSTM 0,999 a 1, 14/16 SL perfectas. La tarea satura: no sirve para rankear |
| 004 | Nadie aprende 90 pasos | memoria dura | sí | no | **FAIL, angostar** | DBC3 media 0,68025, LSTM 0,66425, máquina de estados 0,7663; DBC3 semilla 2 = 0,743 > nivel sin memoria ~0,655. Pooled 1153/961, p = 3,23e−5, concuerda. Umbral 0,80 → 0,75 tras el humo y antes de la corrida, declarado |
| 005 | La entrada por tipos NO PAGA | Holm sobre 12 pruebas por cola | sí | sí: movimiento 0,1196 y 0,1462 no pasan; silenciosa 0,0399 pierde, 0,0731 no | PASS, angostar | `titan/entrada-por-tipos-2026-10-12` `f7844be`. Ridge con 24 entradas vence al lector de 4 DN en seis condiciones, pero son interfaces distintas |
| 006 | Mapa y reflejo chico, no cerebro entrenable | síntesis | n/a | n/a | PASS como lectura | coincide con esta auditoría |

### 2.6 Expediente de agosto (`titan/materializacion-h4-guard-2026-10-02`, respuestas 063 a 124)

| Resp. | Afirmación | Instrumento | ¿Rojo? | Recomputado | Veredicto | Evidencia |
|---|---|---|---|---|---|---|
| 063 a 124 | Null anatómico | `twohop_nulls.py` | sí | ver F01 a F03 | PASS con F01, F02, F03 | `4fc50c5` |
| 063 a 124 | LC6→GF | catálogo | sí | no | PASS | 0 sinapsis, sirve de control negativo |
| 063 a 124 | sel_post y sign-shuffle | 7/9 configuraciones en el fichero, 0/40 suprimidos | sí | piso 1/41 = 0,0244 | PASS, angostar | el z = 181 no es gaussiano; reportar rango 0/40, no z. No afirmo que las otras 2 configuraciones nunca terminaron |
| 063 a 124 | TOPO prueba la topología | permutación | sí | no | **FAIL de nombre** | TOPO permuta pesos sobre las mismas aristas, no la adyacencia: es asignación de pesos |
| 063 a 124 | 39 nulos, p global 0,25 | 4 arriba, 35 abajo | sí | piso 0,05 alcanzable | NO MEDIDO (potencia) | que el piso sea alcanzable no acredita potencia |

### 2.7 H4 en `main`

| Resp. | Afirmación | Instrumento | ¿Rojo? | Recomputado | Veredicto | Evidencia |
|---|---|---|---|---|---|---|
| H4 | 34 contratos | suite H4 | sí | leí 4 contratos; no corrí la suite | NO MEDIDO | el conteo de 34 no está certificado por mí |
| H4 | Generalización intra-animal p = 0,623 | `results/h4_trial_generalization_summary.json` | sí | no | PASS como negativo acotado | 8 trials de un animal (R65D11-tdTomGC6fopt-fly1), BA 0,50188554 contra nulo 0,50815546. Es generalización entre trials, no entre animales; el código rechaza animales mezclados |
| H4 | Mitades temporales | mismo | sí | no | PASS | BA 0,53275955, p = 0,055 |
| H4 | Etiquetas | DAART | n/a | no | angostar | no son anotación humana independiente |
| CI | Hay CI vivo | Actions | sí | sí | PASS | check `integrated-contracts` de PR #27 corre 7 scripts H4, no el paper ni el render. El inventario de agosto "sin workflows" está obsoleto |

## 3. Qué retirar o angostar

1. **Retirar** de §3.4, limitación 7 y docstring de `neuropil_permutation` que el nulo de neuropilo no preserva in-degree global (F01). Decir que sí lo preserva.
2. **Retirar** Z_CP = +14,8σ del abstract y del "Central finding" mientras la Tabla 8 no tenga productor archivado, o recuperarlo (F05).
3. **Angostar** la limitación 2: con N = 5 no hay p empírica bajo 0,1667 (F06).
4. **Corregir** 138.142 → el valor del log, 138.140 (F07).
5. **Angostar** la 011 y la 014: el p agrupado no generaliza entre semillas y la firma mezcla fuentes de variación.
6. **Reescribir** la etiqueta de la 015: no es "solo la semilla 0"; es "gana a cada SL en 4 semillas, sin control de varianza de semilla".
7. **Angostar** la 004: "nadie aprende" es excesivo; ningún modelo llega al umbral, y DBC3 semilla 2 supera el nivel sin memoria.
8. **Renombrar** TOPO como permutación de pesos, no de topología.
9. **Retirar** cualquier z gaussiano de nulos con empates o con piso 1/41; reportar rangos.
10. **Marcar** `swarm/test_swarm.c` como demo, no test, hasta que tenga assertions.
11. **No vender** el laboratorio como cerebro robótico validado. Toda la robótica es simulación, sin hardware.

Lo que no hay que hacer: tirar el valor anatómico, ni generalizar estos negativos a toda computación con conectomas.

## 4. Recomputo corrido

`docs/auditorias/2026-10-12-tao-recompute/recompute.py`, Python 3.12, numpy, scipy. Salida en el sandbox de ClickUp el 2026-10-13, exit 0:

```
PASS F01 nulo neuropilo preserva in-degree global :: 100/100 grafos preservan in-degree; 100/100 cambian destinos
PASS F01 control negativo uniforme rompe in-degree :: 100/100
PASS F02 cociente extremos neuropilo sin umbral ~4.2 (no 2.4) :: 4.1645448578
PASS F02 cociente extremos neuropilo umbral5 ~40 :: 40.279413
PASS Tabla5 p cola inferior thermosensory :: exp=20.30 p=0.0937782455 publicado=0.094
PASS Tabla5 p cola inferior hygrosensory :: exp=51.79 p=1.307080965e-10 publicado=1.3e-10
PASS Tabla7 siete filas x dos umbrales :: porcentajes recomputados coinciden
PASS Tabla7 conectoma entero :: 26.600335% / 13.97689994%
PASS Tabla10 constante efectiva :: 0.05:19.4957, 0.119:7.8928, 0.2:4.4814, 0.3:2.8037
PASS Salidas: piso bilateral 2/5001 supera alfa Holm 0.05/242 :: 0.0003999 > 0.0002066: la primera prueba Holm no puede pasar por resolucion
PASS F04 LIF-soft no amplifica :: delta RDI t60->t180 = -0.251
INFO McNemar exacto 1/37: p=2.83762e-10
INFO McNemar exacto 252/12: p=1.31476e-59
INFO McNemar exacto 169/15: p=3.56859e-34
INFO piso p empirico con 5 nulos CP: 1/6 = 0.1666667
INFO piso con 40 nulos: 1/41 = 0.0243902
RESULTADO TODO PASS
```

`docs/auditorias/2026-10-12-tao-recompute/swarm_probe.c`, GCC 12.2.0, `-std=c99 -Wall -Wextra -Werror -fsanitize=undefined -fno-sanitize-recover=all`:

```
./swarm_probe control  -> adc12=32752 pwm12=4094, exit 0
./swarm_probe adc      -> runtime error: signed integer overflow: 65535 * 65536 cannot be represented in type 'int', exit 1
./swarm_probe pwm      -> runtime error: signed integer overflow: 65535 * 65535 cannot be represented in type 'int', exit 1
```

SHA-256: `recompute.py` `2dbc8e4af98e4f96a703c77347bc2e37f84ed0f50bc66a89d702f1b5e8536254`; `swarm_probe.c` `d28c8d9bbb8a18b68f32a4f4e79d41640c710c778f6f175a1d1cd1423b88042c`.

Nota de precisión: la p termosensorial da 0,0937782 con densidad exacta; con la densidad redondeada a 7,85197e−4 da 0,0937777. Ambas redondean a 0,094.

## 5. Cómo sacarle más provecho al laboratorio

La lectura que sostiene la evidencia: **la mosca sirve de mapa y de reflejo chico y fijo**. Como cerebro entrenable mejor que lo clásico, hasta hoy, no. La hipótesis de BRAIN de 2026-10-12-006 aguanta. Las cinco propuestas, por prioridad:

| P | Propuesta | Falsador | Costo | Máquina |
|---|---|---|---|---|
| P0 | Cerrar la v2.0: aplicar F01, F05, F06 y F07; recuperar el productor de la Tabla 8 o marcarla histórica; archivar arrays de las salidas y un manifiesto de md5 | si el productor recuperado no reproduce la Tabla 8, Z_CP sale del paper | medio día de edición; 1 a 2 días si hay que recuperar y correr | BRAIN en brain-env; render en Actions |
| P0 | Antes de cualquier hardware: enteros seguros en `swarm_drone.h` (producto en `int64_t` o `uint32_t`), `test_swarm.c` con assertions y mutaciones de signo y monotonía | UBSan limpio en el rango completo de `uint16_t`, y que cada mutación haga fallar el test | 0,5 a 1 día | Tao para C portable; Tachi para UBSan en device |
| P1 | Factorial topología × semilla con igual presupuesto, test bloqueado y margen pre-registrado | si la interacción topología × semilla explica la ventaja, la firma de la 014 cae | 1 a 3 días humanos; GPU por medir | BRAIN en brain-env |
| P1 | Reflejo etiquetado contra ridge, control clásico y máquina de estados con las mismas entradas y los mismos límites | si el rival clásico iguala con la misma interfaz, el reflejo de la mosca no paga como controlador | 1 a 2 días de banco; device aparte | BRAIN para banco; Tachi para device |
| P2 | Catálogo reproducible: anotaciones, filtros, signos, citas y negativos versionados por circuito | si un circuito no se reproduce desde el pin de anotaciones, sale del catálogo | 1 a 2 días más curación | BRAIN |

Sobre las cuatro ideas de BRAIN: el Paper 2 con control de salidas es viable solo con lo que aguanta FWER y con los arrays archivados (P0); la tubería motivo → nulos S, SL, T → rival clásico es exactamente P1 y P2 juntas; las líneas etiquetadas en Actions encajan como banco de P1; el cordón en BANC es lo correcto para la etapa motora (limitación 9 del paper) pero va después de P0.

Son propuestas con falsador. No son tareas asignadas ni trabajo ejecutado.

## 6. Hipótesis de BRAIN, contradichas o no

| Hipótesis | Veredicto |
|---|---|
| Mapa y reflejo chico, no cerebro entrenable | **se sostiene** |
| La v2.0 corregida es lo más sólido | **parcial**: tras `ed7c3ac` mejoró, pero F01, F05, F06 y F07 siguen abiertos; no depositar todavía |
| El catálogo, como existencia de aristas | **se sostiene** |
| El escape a lazo cerrado (010 y 011) | **se sostiene con angostamiento**: el p agrupado no generaliza entre semillas |
| La líquida plena contra su control (013 y 014) | **no se sostiene como está**: el diseño mezcla fuentes de variación |
| La firma de la 014 vale solo para la semilla 0 (015) | **contradicha**: gana a cada SL en semillas 0 a 3; el problema es el diseño, no la semilla |
| La 003, la 004 y la 005 son lo más flojo | **parcial**: 003 está bien declarada; 004 exagera; 005 es correcta con interfaces distintas |
| Toda la robótica es simulación | **se sostiene**, y además el test del swarm no puede dar rojo y los helpers desbordan |

## 7. Scorecard TITAN, tipo auditoría

Criterios aplicables: Completitud, Arquitectura del razonamiento, Documentación, Innovación, Proceso QA (45 pts). **N/A: 55 pts** (Ejecutabilidad 15, Seguridad 15, Testing 15, DevOps 10), porque la entrega es un informe, no código de producción; los scripts de recomputo son instrumentos de diagnóstico y corrieron.

| Criterio | Pts | Evidencia |
|---|---|---|
| Completitud | 12/15 | siete bloques más swarm; sin reproducción FlyWire ni PyTorch, sin suite H4, sin respuestas 014 a 017 |
| Arquitectura del razonamiento | 9/10 | F01 a F04 verificados por recomputo y tres confirmados por `ed7c3ac`; parte de las cifras de los bloques 2.4 a 2.6 viene de lecturas del 2026-10-12 citadas por SHA, no re-abiertas el 13 |
| Documentación | 9/10 | cada fila con SHA, archivo o función; falta número de línea en algunas |
| Innovación | 4/5 | F01 da vuelta una limitación en fortaleza; propuestas con falsador |
| Proceso QA | 4/5 | recomputo re-corrido y estado re-verificado contra HEAD vivo; review automático pedido al abrir el PR |
| **Total** | **38/45 = 84,4 %** | |

Bajo el umbral de 90 sobre los aplicables. Lo que falta es ejecutar (parquet, suite H4, productor de Tabla 8), no reescribir texto, así que no itero: **aprobado con deuda técnica**.

**Deuda técnica, propuesta como issues (no abiertos sin acuerdo):** F01 en §3.4, limitación 7 y docstring; F05 productor de la Tabla 8; F06 piso de N = 5; F07 conteo 138.140; overflow de `swarm_drone.h`; `test_swarm.c` sin assertions; diseño factorial de la firma de la 014; suite H4 corrida y conteo de 34 certificado.

## 8. Errores propios, registrados

- Mi primer chequeo de p de la Tabla 5 fue bilateral y difería del paper. El paper usaba cola inferior unilateral y estaba bien: el error era mío.
- En el turno del 2026-10-12 frené lecturas y recálculos esperando una confirmación que solo correspondía a las escrituras. Eso demoró la entrega.
- El borrador del 2026-10-12 (21.532 bytes) se perdió con el sandbox; este informe se reconstruyó desde mis notas y se re-verificó contra el HEAD vivo. Las cifras de los bloques 2.4 a 2.6 no se re-leyeron el 13.
- Mi scorecard del borrador daba 41/45; al re-verificar bajé Arquitectura y Proceso porque parte de la evidencia no se re-abrió.
