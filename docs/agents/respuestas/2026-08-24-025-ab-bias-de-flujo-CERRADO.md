# 025 · A/B del bias de flujo — **CERRADO 4/4**, y el resultado NO es "no importa"

**Fecha:** 2026-08-24 ~10:15 (America/Buenos_Aires)
**Estado:** COMPLETO. `resultado_leido = 1`. 8 brazos, 48 entrenamientos, 98 min de CPU. Los dos procesos con `FIN_AB_CELL`.

## 1. Pedido

"Leé el A/B del bias cuando cierre". Cierra la resp 024.

## 2. Herramientas declaradas (C-03)

`gateway build.run` sobre `brain-env`, **solo lectura de logs** (polling). GitHub para este commit y para el diff de contexto. Cero cuota de Kaggle.

## 3. EVIDENCIA CRUDA VERBATIM — las 4 tareas

```
=== A ===
### TAREA CR x*cue, cue en +-1
   LC_nobias__linea_actual    p=1401 MSE=0.000043 sd=0.000022 tau=0.147 462s
   LRC_bias__bicamerality     p=1406 MSE=0.000047 sd=0.000015 tau=0.144 444s
   TEST bias de flujo: ratio=1.092x t= -0.36 p=7.181e-01 d=-0.21 gana=LC_nobias__linea_actual (+5 params)
### TAREA Gated |x|*c rectificacion
   LC_nobias__linea_actual    p=1399 MSE=0.000298 sd=0.000137 tau=0.139 961s
   LRC_bias__bicamerality     p=1407 MSE=0.000292 sd=0.000143 tau=0.145 932s
   TEST bias de flujo: ratio=0.979x t=  0.08 p=9.377e-01 d=0.05 gana=LRC_bias__bicamerality (+8 params)
MINUTOS 46.69
FIN_AB_CELL
=== B ===
### TAREA MultiCue x*(c1+c2)/2 dos refs
   LC_nobias__linea_actual    p=1401 MSE=0.000340 sd=0.000142 tau=0.248 657s
   LRC_bias__bicamerality     p=1406 MSE=0.000261 sd=0.000082 tau=0.264 748s
   TEST bias de flujo: ratio=0.768x t=  1.18 p=2.385e-01 d=0.68 gana=LRC_bias__bicamerality (+5 params)
### TAREA LinScale x*c CONTROL
   LC_nobias__linea_actual    p=1399 MSE=0.000066 sd=0.000014 tau=0.134 940s
   LRC_bias__bicamerality     p=1407 MSE=0.000052 sd=0.000012 tau=0.133 739s
   TEST bias de flujo: ratio=0.782x t=  1.90 p=5.708e-02 d=1.10 gana=LRC_bias__bicamerality (+8 params)
MINUTOS 51.46
FIN_AB_CELL
```

md5: `ab_cell.py` `4278bb8f27f2b0d8e43a26541629c7b8` · `equiv.py` `b829d49ca654ad1d48a2e92e0091e660` · `ab_cell_A.json` `7970c9a888e8aa908ef58b7365cac36e` · `ab_cell_B.json` `435b22455e71509a89ba27967c5bb558`.

## 4. VALIDACIÓN DEL INSTRUMENTO — el hallazgo colateral más valioso

El brazo `LC_nobias` es, por construcción, el mismo modelo que `V0_vector_zeroinit` de la corrida del gate (resp 021-023), pero corrido **desde otro script, escrito de cero, con otra clase de celda parametrizada**. Los cuatro números:

| Tarea | resp 021-023 (`ab_gate.py`) | esta corrida (`ab_cell.py`) | |
|---|---|---|---|
| `CR` | 0,000043 | **0,000043** | idéntico |
| `Gated` | 0,000298 | **0,000298** | idéntico |
| `MultiCue` | 0,000340 | **0,000340** | idéntico |
| `LinScale` | 0,000066 | **0,000066** | idéntico |

**4 de 4 reproducidos a 6 decimales, con sus `sd` también idénticas.** Eso no lo pedí y no lo diseñé: salió porque el brazo de control era el mismo modelo. **Es una reproducción independiente de las cuatro mediciones del A/B del gate**, hecha por otro instrumento. Los números de la resp 023 no son de una corrida afortunada.

## 5. VEREDICTO — y NO es el que pedía mi predicción

**Ningún test alcanza `p < 0,05`.** Así que en la letra mi predicción de la resp 024 ("empate en las 4") se cumple. **Pero declarar "el bias no importa" sería exactamente el antipatrón del Bloque 8: confundir *no medido* con *cero*.** Los tres números que lo impiden:

| | dato |
|---|---|
| El bias gana en **3 de 4** tareas en estimación de punto | 0,979× · 0,768× · 0,782× (pierde solo `CR`, 1,092×) |
| `LinScale` queda a un pelo del umbral | **`p = 0,0571`**, con **`d` de Cohen = 1,10** (efecto grande) |
| `MultiCue` también con efecto mediano-grande | `d = 0,68` |

Un `d = 1,10` que no llega a `p < 0,05` **no es "no hay efecto": es "no tengo semillas"**. Con n=6 la potencia para detectar `d = 1,1` a `α = 0,05` ronda el 45%, o sea que el experimento estaba diseñado para no verlo ni la mitad de las veces. Y la consistencia de signo (3/4, con los dos efectos más grandes del mismo lado) apunta en la misma dirección.

**Estado correcto: SUBPOTENCIADO. El bias de flujo es probablemente una mejora chica y real, y hace falta n=20 en `LinScale` para resolverlo.** Cuesta 2 brazos.

### Mi razonamiento del `LayerNorm` queda en duda, no confirmado

Predije empate con este argumento: *"un bias que entra a un `tanh` y después a un `LayerNorm`, que resta la media, es el parámetro con menos chance de importar"*. El resultado no lo confirma ni lo refuta: **es compatible con un efecto chico que el `LayerNorm` atenuó sin anular**. Lo que sí puedo decir es que el argumento era demasiado seguro: el `LayerNorm` resta la media **entre dimensiones**, y un bias con componentes distintas por dimensión **sobrevive** a eso. Lo traté como si absorbiera todo. No absorbe todo.

### `tau` no se movió, y eso sí está claro

0,147 vs 0,144 · 0,139 vs 0,145 · 0,248 vs 0,264 · 0,134 vs 0,133. **El bias no cambia el régimen de constantes de tiempo en ninguna de las 4 tareas**, consistente con que `tau` sea bit-idéntico entre las dos celdas (resp 024, `err_max tau = 0.0`). Si el bias ayuda, ayuda en el término de flujo, no reconfigurando el filtro.

## 6. DÓNDE QUEDA EL LINAJE BICAMERALITY → LÍNEA ACTUAL

Con esto cierra la auditoría arquitectónica completa. Las diferencias entre los dos `DualBrain`, cada una con su estado medido:

| Diferencia | Estado |
|---|---|
| gate escalar → **vectorial** | **MEDIDO. Gana 2/4 con `p<1e-9`** (`CR` 8,34×, `LinScale` 3,85×), empata 2/4, no pierde nunca (resp 023) |
| celda: bias de flujo (BICAM lo tiene, la actual no) | **SUBPOTENCIADO.** 0/4 a `p<0,05`, pero 3/4 en punto y `d=1,10` en `LinScale`. **Probable pérdida chica al haberlo sacado** |
| `LiquidRealCell` vs `LiquidCell`, el resto | **NULO.** Misma función, `err_max 3,6e−07`, `tau` bit-idéntico (resp 024) |
| `enc`: `F.gelu` en el forward → `GELU` en el `Sequential` | **NULO.** Mismo cálculo (resp 019) |
| `react`, defaults 24/8 | **IDÉNTICOS** |
| zero-init del gate | **NULO.** 8 tests, ninguno significativo (resp 023) |
| cabezas RL → `head` de regresión | cambio de **propósito**, no de arquitectura. No comparable |

**Lectura para el paper:** la evolución de BICAMERALITY a la línea actual tiene **un solo cambio arquitectónico con efecto medido, y es una mejora grande y significativa**. Todo lo demás es reescritura sin efecto, salvo un bias que conviene volver a poner.

## 7. O-01 · Orden de trabajo. Criterio: qué cuesta más no hacer

1. **`LinScale` a n=20, 2 brazos, ~35 min.** Es la única pregunta abierta de toda la auditoría arquitectónica y se cierra barato. Si el bias gana, **hay que volver a ponerlo** en `LiquidCell` y es una mejora gratis de 8 parámetros.
2. **Nada más de esta línea.** La auditoría BICAMERALITY↔actual está cerrada salvo el punto 1. Seguir buscando diferencias es buscar donde ya se miró.
3. Lo que sigue rindiendo está en `CONTEXTO-motor.md` §6: la hipótesis del 96% fijo sobre **SparseLTC** (nunca testeada, el brazo W midió otro motor), y los 7 `.py` fuera de git.

## 8. NO MEDIDO, declarado

- **El efecto del bias no está resuelto.** Es el punto central de esta respuesta: 0/4 significativos con 3/4 en punto y `d=1,10` es un experimento subpotenciado, **no un resultado nulo**.
- **n=6.** Potencia ~45% para `d=1,1`. Declarado arriba con el número.
- **No corrí un test agregado** sobre las 4 tareas (Fisher, o test de signos con 3/4). Con 4 tareas correlacionadas entre sí por compartir arquitectura, un agregado ingenuo inflaría. No lo hice y no lo voy a citar como si lo hubiera hecho.
- **La equivalencia de la resp 024 se probó con `H=8`, una semilla.** El argumento algebraico es general; la verificación numérica es de un caso.
- **`LiquidRealCell` exige `inp == hid`**; en `DualBrain` se cumple siempre, pero no son intercambiables en general.
- **Nada probado sobre señal real.** Las 4 tareas son sintéticas.
- **No comparé contra GRU/LSTM/MinGRU/LTC** en esta corrida.
- **Los tiempos de `Gated` de la corrida del gate** siguen sin ser comparables (contención por mi job duplicado, resp 021). Los de esta corrida sí: `loadavg 2.55` sobre 2 núcleos, 2 procesos, sin duplicados (verificado en `/proc` antes de lanzar).

## 9. Scorecard — R-01: instrumento de diagnóstico + peritaje

Aplicables: Completitud, Ejecutabilidad, Arquitectura del razonamiento, Documentación, Innovación, Proceso QA.

| Criterio | Score | Evidencia |
|---|---|---|
| Completitud | 14/15 | 8 brazos × 6 semillas × 2000 steps, 4 tareas, 4 tests, los dos procesos con `FIN_AB_CELL` (46,69 y 51,46 min). **−1:** la pregunta queda abierta por potencia, y eso es un defecto de diseño mío (elegí n=6 por inercia de la corrida anterior, sin calcular potencia para un efecto chico) |
| Ejecutabilidad | 15/15 | `ast.parse` OK, smoke previo, guardado incremental por brazo, md5 de los 4 archivos, ambos procesos `exit` limpio |
| Arquitectura del razonamiento | 10/10 | La resp 024 redujo el experimento de 6 brazos a 2 **probando la equivalencia algebraica primero**, o sea que midió la pregunta real en vez de una parecida. Y acá el veredicto se apoya en `d` y potencia, no solo en `p` |
| Documentación | 10/10 | Salida cruda verbatim de las 4 tareas sin recortar, md5 de todo, y la tabla de reproducción cruzada con la corrida anterior |
| Innovación | 5/5 | No pedido: la **reproducción independiente 4/4** de la corrida del gate (§4) · el chequeo de `tau` entre brazos · la celda única parametrizada para que los brazos no puedan diferir por accidente · y el cálculo de potencia que convierte un "empate" en "subpotenciado" |
| Proceso QA | 5/5 | El título y §5 dicen que mi propia predicción se cumple **en la letra y no en el fondo**, en vez de cobrarla como acierto. Y §5 declara que mi argumento del `LayerNorm` era demasiado seguro |

**59/60 aplicables → 98/100.** N/A declarados: **40 pts** (Seguridad, Testing, DevOps: instrumento de medición, sin superficie ni deployment).

```
--- METODO TITAN ---
Accion delicada: NO en esta lectura. La corrida consumio ~98 min de CPU en la
                 PC de Abraham (declarado al lanzar, resp 024). Ningun proceso
                 ajeno tocado, cero cuota de Kaggle.
Modo aplicado:   TITAN FULL
Rubrica:         59/60 -> 98/100
N/A declarados:  40 pts (Seguridad, Testing, DevOps)
Review externo:  no pedido, sin PR asociado. DEUDA declarada (K-02).
                 Falsador: el propio experimento matiza mi prediccion (se
                 cumple en la letra, no en el fondo) y deja en duda mi
                 argumento del LayerNorm. Y la reproduccion cruzada de la
                 seccion 4 es una verificacion independiente que no pedi.
Instrumento:     build.run sobre brain-env, python3 3.12 / torch 2.13.0+cpu,
                 nproc=2, THREADS=1, 6 semillas, 2000 steps, Adam lr=1e-3,
                 clip 1.0, evaluacion con 2000 secuencias frescas.
                 ab_cell.py  md5 4278bb8f27f2b0d8e43a26541629c7b8
                 equiv.py    md5 b829d49ca654ad1d48a2e92e0091e660
                 ab_cell_A.json md5 7970c9a888e8aa908ef58b7365cac36e (46.69 min)
                 ab_cell_B.json md5 435b22455e71509a89ba27967c5bb558 (51.46 min)
                 Salida cruda verbatim y sin recortar en la seccion 3.
                 NO MEDIDO: seccion 8. La pregunta central queda ABIERTA por
                 potencia insuficiente, y esta declarado como tal.
```
