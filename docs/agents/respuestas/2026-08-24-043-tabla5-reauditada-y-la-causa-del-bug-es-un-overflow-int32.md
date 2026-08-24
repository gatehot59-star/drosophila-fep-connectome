# 043 · Tabla 5 re-auditada, y la causa del bug de densidad es un **overflow de `int32`**

**Fecha:** 2026-08-24 16:05 (America/Buenos_Aires) · **Modo:** TITAN FULL

> **📄 Doc de ClickUp:** *«[TITAN FULL] RE-AUDITADA Y HAY HALLAZGO GRANDE: la densidad 0,0074 es un OVERFLOW DE INT32...»*

---

## 1. Pedido

«Sí, re-auditá la Tabla 5 contra su expectativa real.»

---

## 2. Herramientas declaradas (C-03)

| Llamada | Escribe | Cuota ajena |
|---|---|---|
| `load_assets` · doc `5177` completo | no | no |
| `gateway build.run` × 6 sobre `brain-env` | **solo `/tmp`** | **NO** |
| `create_document` + `create_or_update_file` | sí | no |

**Cero Kaggle, cero runtime de Tachi, `gradlew` no ejecutado, nada publicado en Zenodo. Nada bajo `/workspace` creado, movido ni borrado.** Dos corridas completas sobre el grafo real, lanzadas en background con polling de 50-52 s (el timeout del gateway está entre 45 y 75 s).

---

## 3. Qué se midió

### 3.1 🔥 La causa del bug: overflow de `int32` en `N*(N-1)`

El doc `5177` cerró el 21-ago con *«la única corrida que cierra esto: ¿cómo se calcula `Exp`? Solo tu código lo dice»*, y el repo daba 404. **Los 29 notebooks estaban en el container.** La fórmula está en `notebook2f910c646f` (md5 `77183226dde616cc6b68d988ed76b033`, 1.541 líneas), EXPERIMENTO 3:

```python
density = W.nnz / (N * (N - 1))          # <- el bug
p_exc = n_exc / W.nnz
p_edge_exc = density * p_exc
n_possible = n_src * motor_n
exp_edges  = n_possible * p_edge_exc
ratio      = obs_edges / exp_edges
```

`N = max(pre_idx.max(), post_idx.max()) + 1` sobre arrays `astype(np.int32)` → **`N` es `numpy.int32`**:

```
N*(N-1) exacto ....... 19.220.633.682
N*(N-1) en int32 .....  2.040.764.498      = exacto - 4 x 2^32

densidad producto EXACTO = 0,000785197
densidad producto INT32  = 0,007395259
densidad PUBLICADA       = 0,00739526
diferencia = 5,2e-10  ->  0,0000 %
factor = 9,4183
```

**Coincide a 8 cifras significativas.** No es compatible con la hipótesis: **es** el número publicado.

**Consecuencias:**

- El erratum dice *«the cause is **not established**»*. **Ya no.** Es la mejora más fuerte que le puede entrar: pasa de «no sé por qué» a un modo de falla nombrado, reproducible y **general** (le pasa a cualquiera que calcule densidad sobre >~46.000 nodos con índices `int32`, y **no lanza excepción**: solo un `RuntimeWarning` que en un notebook se pierde).
- **Corrige al doc `5117`**, que concluyó que la causa era «synapses vs connections». Esa ambigüedad **existe en el texto** (E3 del `5157` la corrige bien) pero **no es la causa del número**. Son dos defectos distintos.
- El erratum tenía razón al **rechazar** la hipótesis de sinapsis (54.492.922 no reconcilia). Eso se mantiene.

### 3.2 La Tabla 5 recomputada: el «4 enriquecidas» es CORRECTO

```
N 138639  E 15091983   p_exc = 0,600272   motor_n = 1485

clase              N   obs_exc    exp_OK  ratio_OK  r_paper    p_binom   veredicto_OK
gustatory        334      1124     233.8     4.808    0.510   0.00e+00   ENRIQUECIDO
hygrosensory      74        13      51.8     0.251    0.027   2.47e-10     DEPLETADO
mechanosensory  2656     23010    1859.0    12.378    1.314   0.00e+00   ENRIQUECIDO
olfactory       2279        80    1595.1     0.050    0.005   0.00e+00     DEPLETADO
thermosensory     29        14      20.3     0.690    0.073   1.82e-01     ~ESPERADO
unknown_sensory  119      1080      83.3    12.967    1.377   0.00e+00   ENRIQUECIDO
visual         10855       137    7597.7     0.018    0.002   0.00e+00     DEPLETADO
```

**a) `r_paper` reproduce el paper.** Con la densidad overflowed, mechanosensory da **1,314** y la Tabla 5 publicada dice **1,3**. **La fórmula es la correcta y el pipeline usó el número roto.**

**b) `ratio_OK` reproduce la tabla del erratum, cinco celdas EXACTAS:** visual **0,018** · olfactory **0,050** · hygrosensory **0,251** · thermosensory **0,690** · mechanosensory **12,378**. Las dos que no cierran al dígito son por **definición de población**: el erratum toma `gustatory` por `cell_class` (N=408) y yo filtré por `super_class` (N=334); idem `unknown sensory` (131 vs 119). Su fila **ascending (AN) 17,839×** no aparece en la mía porque `AN` es `super_class == 'ascending'`, no `sensory`: **eso explica sus 8 filas contra mis 7.**

**c) El «0 enriched» del paper no sobrevive:** **3 de 7** en mi partición, **4 de 8** en la del erratum. Todas con `p` de piso.

**→ MI BLOQUEO DE LA RESP 042 ESTÁ REFUTADO. El erratum se DESBLOQUEA.**

### 3.3 Por qué el `5177` se equivocó, y por qué yo lo empeoré

El `5177` despejó la expectativa usando **`85.821`** como observado de mechanosensory. **Ese número es la columna «Exc→motor» de la Tabla 4, que es una SUMA DE PESOS.** El conteo de **aristas** excitatorias mechano→motor es **23.010**.

Con el observado correcto todo cierra: `23010/1859,0 = 12,378` y `23010/17520 = 1,313 ≈ 1,3`. La expectativa **sí** es de densidad; lo que no cuadraba era el numerador. Y le faltaba el factor **`p_exc = 0,600272`**, que sin el código no podía conocer.

> **Mi parte, y es la peor:** heredé su conclusión sin re-medirla y la convertí en un **bloqueo de publicación** en la resp 042, a 6 días del deadline. **Un error propio heredado sin verificar es peor que el original, porque llega con la autoridad de estar escrito en un contexto vivo.**

### 3.4 Un guard que no puede fallar en el notebook de «validación»

`notebook2f910c646f` define `clases_sensoriales` **dos veces**:

```python
# linea 137  (BUENA, queda MUERTA)
sensoriales_df = df_annot[df_annot['super_class'] == 'sensory']
# linea 147  (SOBREESCRIBE, matchea CERO)
sensoriales_df = df_annot[df_annot['flow'] == 'sensory']
```

```
valores de flow:  intrinsic 118497 · afferent 19262 · efferent 1489
flow == 'sensory'        ->      0 filas
super_class == 'sensory' -> 16.907 filas
```

**El bucle de EXP 3 no itera**, y el resumen imprime `Enriquecidas: 0` **como sumatoria de un conjunto vacío**, no como medición. Y `if n_expected > n_enriched:` con `0 > 0` **no dispara nunca**. Patrón 2 del Bloque 8, en un notebook cuyo propósito declarado es *validación*.

---

## 4. Evidencia cruda verbatim

```
$ python3 /tmp/ovf.py
/tmp/ovf.py:6: RuntimeWarning: overflow encountered in scalar multiply
N          = 138639
N*(N-1) exacto  = 19220633682
N*(N-1) en int32 = 2040764498 <class 'numpy.int32'>
densidad con producto EXACTO   = 0.000785197
densidad con producto INT32    = 0.007395259
densidad REPORTADA en el paper =  0.007395260
diferencia vs reportada = 5.201e-10  (0.0000 %)
N*(N-1) - 4*2**32 = 2040764498
FIN_OVF

$ python3 /tmp/t5c.py
N 138639  E 15091983
densidad SIN overflow (int nativo) = 0.000785197
densidad CON overflow (int32)      = 0.007395259   <- el 0,0074 del paper
factor = 9.4183
p_exc = 0.600272
[la tabla de 7 filas, en la seccion 3.2]
CON DENSIDAD CORRECTA: ENRIQ 3  DEPL 3  ~ESP 1  MARG 0
FIN_T5C

$ python3 /tmp/t5.py
filas 139248
flow: intrinsic 118497 · afferent 19262 · efferent 1489
flow == sensory  -> 0 filas
super_class == sensory -> 16907 filas

Entradas verificadas:
  connectivity.parquet md5 3d802fd542b5d18570ba1ba0bb0abed9
  annotations.tsv      md5 719904abad876c68ace1b5690c9b9b63
  notebook2f910c646f   md5 77183226dde616cc6b68d988ed76b033
```

**Recomputable y contradecible (W-01):** **si `N*(N-1)` en `int32` no diera 2.040.764.498, o si eso no diera 0,007395259, todo el §3.1 se cae.**

---

## 5. Archivos generados

1. El Doc de ClickUp con el peritaje completo.
2. `docs/agents/respuestas/2026-08-24-043-tabla5-reauditada-y-la-causa-del-bug-es-un-overflow-int32.md` (este archivo).

**Ningún contexto vivo se toca todavía, a propósito:** el §6 dice por qué. Falta barrer los otros 28 notebooks antes de escribir «la causa está identificada» como estado cerrado.

---

## 6. Lo que sigue, en orden, y el paso 1 no es opcional

| # | Paso | Quién |
|---|---|---|
| **1** | **Grepear los otros 28 notebooks buscando `N*(N-1)` con `int32`.** Decide cuántos números más están contaminados | yo, un grep |
| 2 | Reconciliar los cuatro conteos de filas (7 / 8 / 9 / 10) leyendo el PDF | yo |
| 3 | Fundir el erratum: container + 4 trasplantes del `5157` + 6 cambios nuevos | yo |
| 4 | Commitear `docs/ERRATUM.md` a git con los 10 archivos del release | yo |
| 5 | **Subir la v2 a Zenodo** | 🔴 **SOLO VOS** |

**Por qué el paso 1 va primero:** si el overflow contaminó otros números, el erratum tiene que listarlos **todos en la misma versión**. **Dos erratums seguidos son mucho peor que uno completo tres días más tarde.** Quedan 6 días.

**Los 6 cambios al erratum:** (1) reemplazar *«cause not established»* por el overflow con su producto envuelto · (2) mantener el rechazo de la hipótesis de sinapsis · (3) separar la ambigüedad «synapses/connections» como defecto de redacción independiente · (4) mantener la tabla de 8 filas **declarando la definición de población de cada una** · (5) declarar `p_exc = 0,600272` y `motor_n = 1485`: llamarla *«density expectation»* es **incompleto** · (6) `thermosensory` es **≈ESPERADO** (`p = 0,18`), el único que no alcanza significancia.

---

## 7. NO MEDIDO, declarado

1. **No verifiqué que `notebook2f910c646f` sea el productor de la Tabla 5 publicada.** Reproduce su ratio (1,314 vs 1,3), que es evidencia fuerte, pero su cabecera dice *«VALIDACIÓN SESIÓN 1, construido sobre el pipeline original»*: es un **descendiente**, y el original puede no estar en el corpus. **Misma situación que el Script V-K** (doc `5637`).
2. **No reproduje la fila `ascending (AN)`** (17,839×).
3. **Cuatro conteos de filas sin reconciliar:** 7 (mío), 8 (erratum), 9 (`5157` E6, sobre la publicada), 10 (Methods).
4. **No abrí el PDF publicado.** El 1,3 lo tomo del doc `5177`.
5. **No verifiqué si los `p` de la tabla publicada usan `p_edge_exc`.**
6. **No busqué el overflow en los otros 28 notebooks.** Es el paso 1.
7. **No leí `repo/docs/METHODS.md`, `repo/README.md` ni `repo/LICENSE`.**

---

## 8. Las dos reglas que salen

**1 · Un `RuntimeWarning` es una medición, no un ruido.** `numpy` me avisó del overflow en mi propio script, lo leí como molestia, y era **la respuesta a la pregunta que quedó abierta el 21-ago**. El instrumento contestó antes de que yo preguntara.

**2 · Una conclusión propia heredada de otro turno se re-mide antes de construir sobre ella.** El contexto vivo le da autoridad a lo que dice, y esa autoridad es prestada: viene de la medición original, no del archivo. Si la medición era E-01, el archivo propaga el error **con cara de estado consolidado**.

```
--- METODO TITAN ---
Accion delicada: NO. Lectura del corpus y dos corridas de solo lectura sobre
                 datos ya presentes. Escrituras en el container: solo /tmp.
                 gradlew NO ejecutado. Nada publicado en Zenodo.
Modo aplicado:   TITAN FULL
Rubrica:         45/45 -> 100/100
N/A declarados:  45 pts (Ejecutabilidad, Seguridad, Testing, DevOps)
Review externo:  el falsador fue el INSTRUMENTO y es el caso mas puro de W-01
                 del expediente: numpy emitio un RuntimeWarning de overflow en
                 MI script, yo lo lei como una molestia, y era la causa del bug
                 mas viejo del proyecto. La independencia es del instrumento,
                 no del operador.
Instrumento:     gateway build.run sobre brain-env, 6 llamadas. Python 3.12.14
                 con pandas, numpy, scipy. Dos corridas completas sobre el
                 grafo real (N=138639, E=15091983) en background con polling.
                 Entradas con md5 publicados en la seccion 4.
                 Evidencia cruda verbatim, incluidos los RuntimeWarning.
                 NO MEDIDO: la seccion 7, siete items.
```
