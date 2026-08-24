# 048 · `CONTEXTO-motor.md` con los dos hallazgos, y dos más que aparecieron al escribirlo

**Fecha:** 2026-08-24 19:55 (America/Buenos_Aires) · **Modo:** TITAN FULL

---

## 1. Pedido

«Actualizá `CONTEXTO-motor.md` con los dos hallazgos.» Los dos de la resp 047, que salieron de **leer `results/dualbrain_bench.log`** al subirlo a git.

---

## 2. Herramientas declaradas (C-03)

| Llamada | Escribe | Cuota ajena |
|---|---|---|
| `get_file_contents` · `CONTEXTO-motor.md` (leído **completo**, SHA `ae64ce4`) | no | no |
| `create_or_update_file` × 2 (el contexto + este archivo) | **sí, al repo** | no |
| `create_document` | sí, ClickUp | no |

**Ninguna corrida nueva.** Los cuatro puntos salen del log ya commiteado. **Cero Kaggle, cero cuota, `gradlew` no ejecutado, nada publicado en Zenodo.**

---

## 3. Los dos hallazgos pedidos

### 3.1 La salvedad cross-run estaba SOBRE-GENERALIZADA

El archivo decía que el hallazgo «el brazo más congelado le gana a `DualNoGate` por 3,2× a 35×» es **cross-run en las cuatro tareas**. Medido contra el log:

| Tarea | `DualNoGate` en el bench | brazo C en `tres_brazos` | ¿misma arquitectura? |
|---|---|---|---|
| `Gated` | `h_r=26 h_m=8` | `h_r=26 h_m=8` | **SÍ** |
| `LinScale` | `h_r=26 h_m=8` | `h_r=26 h_m=8` | **SÍ** |
| `MultiCue` | `h_r=30 h_m=5` | `h_r=26 h_m=8` | no |
| `CR` | `h_r=30 h_m=5` | `h_r=26 h_m=8` | no |

**Iso-arquitectura en 2 de 4, cross-arquitectura en 2 de 4.** Sigue siendo **entre corridas** en las cuatro (kernels distintos), así que el brazo `D` **sigue haciendo falta**, pero en `Gated` y `LinScale` lo único que cambia es la corrida.

### 3.2 La ablación del gate es el resultado más limpio de la línea, y estaba SIN NUMERAR

El archivo listaba «gate multiplicativo: ayuda en **4 de 4** tareas» **sin un solo número ni un solo `p`**. Los números están en el log:

```
  Gated     con_gate=0.000236  sin_gate=0.025539  AYUDA 108.11x  p=1.56e-105
  LinScale  con_gate=0.000055  sin_gate=0.001192  AYUDA  21.85x  p=3.36e-16
  MultiCue  con_gate=0.000326  sin_gate=0.019235  AYUDA  58.97x  p=4.91e-03
  CR        con_gate=0.000054  sin_gate=0.001979  AYUDA  36.72x  p=1.38e-31
```

**Y su diseño no tiene los defectos del otro hallazgo:** es **iso-run** (mismo kernel), **iso-arquitectura** (mismos `h_r`/`h_m` por tarea, presupuesto 1399 o 1401), **iso-celda**, **iso-encoder**, 10 semillas. La única variable manipulada es `g*h_m` contra `h_m`.

**No necesita ningún brazo nuevo: es publicable hoy.** Entra al contexto como **§0.bis**, arriba, porque es el claim con menos objeciones posibles de todo el expediente.

**Nota de prioridad que quedó escrita en el ítem 3 de NO MEDIDO:** si lo que hace falta es un claim sobre **el gate**, §0.bis ya lo tiene y cuesta cero. El brazo `D` sirve para el claim sobre **estructura congelada**, que es otra pregunta.

---

## 4. Dos hallazgos NUEVOS, que aparecieron al escribir el archivo

### 4.1 El 1,18× y el 4× en contra son EL MISMO MODELO en dos puntos de la misma curva

El contexto tenía, en «medido a favor»: *«óptimo interior h_m=10 / h_r=22 → **1,18× sobre LSTM**»*. Y el log dice, en `MultiCue`:

```
  MultiCue   DualBrain MSE=0.000326
   vs GRU     MSE=0.000138  ratio=0.42x  p=1.13e-06  gana=GRU
   vs LSTM    MSE=0.000081  ratio=0.25x  p=3.27e-11  gana=LSTM
   vs MinGRU  MSE=0.000191  ratio=0.59x  p=6.17e-04  gana=MinGRU
```

**No son dos mediciones independientes: son la misma curva vista desde `h_m=10` y desde `h_m=5`.** El 1,18× es del **barrido en su óptimo**; el bench corre `h_r=30 h_m=5`, y ahí la brecha con LSTM es **4× EN CONTRA** (0,000326 contra 0,000081).

**El archivo las listaba como si fueran independientes**, una en «medido a favor» y la otra en ninguna parte. Ahora:

- **Refuerza el óptimo interior**, que ya estaba medido: el reparto react/memoria **decide si DualBrain gana o pierde** en la tarea de dos referencias.
- **El claim sobre `MultiCue` tiene que llevar el reparto.** «Queda 1,18× sobre LSTM» es cierto **solo en el óptimo**, y un revisor que corra la configuración del bench **mide lo contrario**.
- Entra a §4 como «INCOMPLETO», no como refutado: el número es correcto, la calificación faltaba.

**Y define el nicho, que ahora está escrito en §5:** DualBrain gana con **una referencia** (`CR` 1,40× a 9,49× sobre todos, `LinScale` 3,72× a 501×) y **pierde con dos**. **El nicho es modulación por una referencia retenida, no fusión multi-referencia.** Venderlo como lo segundo es venderlo donde mide peor.

### 4.2 El spread de τ de 31,2× figuraba como «medición propia» sin archivo

Estaba en «medido a favor» con el instrumento **«medición propia»**, que no es un instrumento: es un placeholder. **Sale de la sección Bode de este mismo log**, con sus cortes a −3 dB por dimensión (`0.0504`, `0.0035` ×3, `0.0074`, `0.0020`, `0.0194`, `0.0610` ciclos/muestra) y su rango de 0,00195 a 0,06102. **Ahora tiene archivo en git.**

Y el log declara **para qué sirve el número**, que el contexto no decía: *«si el factor fuera ~1, las dimensiones serían el MISMO filtro y el banco sería decorativo»*. O sea que el 31,2× **es el test de que el banco de τ no es adorno**, no una curiosidad.

### 4.3 Y una corrección de estado

El ítem 6 de NO MEDIDO decía *«log de `titan-paper-dualbrain` (complete 00:06Z): sin leer»*. **Ya se leyó: es `results/dualbrain_bench.log`**, en git desde la resp 047, y de ahí salieron los cuatro puntos de este turno. Sigue sin leer `notebookceb82767da` (928 KB).

---

## 5. Evidencia cruda verbatim

Todo sale de `results/dualbrain_bench.log`, **commiteado en el repo** (98,3 min de CPU, 6 modelos, 4 tareas, 10 semillas). Los presupuestos por tarea:

```
TAREA Gated / LinScale     DualBrain 1399 {'h_r': 26, 'h_m': 8}
                           DualNoGate 1399 {'h_r': 26, 'h_m': 8}
TAREA MultiCue / CR        DualBrain 1401 {'h_r': 30, 'h_m': 5}
                           DualNoGate 1401 {'h_r': 30, 'h_m': 5}

Corte a -3dB por dimension de h_m (ciclos/muestra):
  ['0.0504','0.0035','0.0035','0.0035','0.0074','0.0020','0.0194','0.0610']
  rango 0.00195 a 0.06102  ->  factor 31.2x

ABLACION DEL GATE
  Gated     108.11x  p=1.56e-105
  LinScale   21.85x  p=3.36e-16
  MultiCue   58.97x  p=4.91e-03
  CR         36.72x  p=1.38e-31

MultiCue, DualBrain contra los competidores
  vs GRU 0.42x  vs LSTM 0.25x  vs MinGRU 0.59x   (pierde con los tres)
```

**Recomputable y contradecible (W-01):** el log está en git. **Si `DualNoGate` en `Gated` no usara `h_r=26 h_m=8`, el §3.1 se cae. Si la ablación no fuera del mismo kernel, el §3.2 se cae.**

**Y una limitación del log, ahora declarada en el ítem 14:** el log trae **media y `sd`**, no la serie. **Las 10 semillas individuales viven en `dualbrain_bench.json`** (31.527 B, md5 `1025d60b4e9521d7e4a21ed282935049`), que **no está commiteado**. O sea que el veredicto es recomputable **desde los agregados**, no desde los datos crudos.

---

## 6. Archivos generados o modificados

| Archivo | Estado |
|---|---|
| `docs/agents/CONTEXTO-motor.md` | **modificado.** Nueva §0.bis; §3 con la tabla de arquitecturas y el resultado en contra; §4 con dos filas nuevas; §5 con el nicho medido; §6 con los ítems 3, 6, 9, 10, 11 y 14 corregidos; §7 con dos lecciones nuevas |
| `docs/agents/respuestas/2026-08-24-048-...md` | este archivo |

**Cero filas borradas** de las tablas de medido a favor o refutado.

---

## 7. NO MEDIDO, declarado

1. **Ninguna corrida nueva en este turno.** Los cuatro puntos son **lectura de un log commiteado**, no medición propia.
2. **No leí `dualbrain_bench.json`.** Las 10 semillas individuales de cada celda están ahí y **no las verifiqué**: tomo media, `sd` y `p` del log.
3. **No recomputé ningún `p` del log.** Los `t` de Welch y los `d` de Cohen vienen calculados por el kernel.
4. **El brazo `D` sigue sin correr** (~25 min), y sin él el hallazgo de §3 de ese archivo no se cita.
5. **El brazo `W`/`S` sigue sin correr** (~90 min). Es la deuda más vieja.
6. **`notebookceb82767da` (928 KB) sigue sin leer.** Puede tener otro resultado enterrado, como este.
7. **No verifiqué que el `DualNoGate` del bench y el brazo `C` de `tres_brazos` sean la misma clase.** Comparo sus hiperparámetros, no su código. Si difieren en algo más, la tabla de §3.1 mide menos de lo que parece.
8. **Los 6 `.py` de deuda siguen fuera de git**, con su manifiesto en `MANIFIESTO-KAGGLE.md`.

---

## 8. Las dos lecciones que salen

**1 · Un log sin leer es un resultado sin usar, y puede ser el mejor que hay.** El `dualbrain_bench.log` figuró como «sin leer» **dos días** en un ítem de NO MEDIDO, y contenía: la medición **más limpia** de la línea, un resultado **en contra** que el contexto no tenía, y la **fuente** de un número que figuraba sin archivo. **Se leyó solo porque había que subirlo a git**, o sea por un trámite, no por una decisión de método.

**2 · Dos números de la misma curva no son dos mediciones independientes.** El 1,18× y el 4× en contra son el mismo modelo en `h_m=10` y en `h_m=5`. **Citar uno sin el reparto es elegir el punto favorable**, y es la cuarta variante del mismo patrón que ya aparecía tres veces en el otro contexto: **comparar cantidades medidas con criterios distintos.**

```
--- METODO TITAN ---
Accion delicada: SI. Se sobrescribe un contexto vivo. Mitigacion: se leyo el
                 archivo COMPLETO antes de escribir, se paso el sha
                 ae64ce46027a553d6199fb973e333396c0f2c601 para que un cambio
                 concurrente aborte la escritura, y no se borro ninguna fila de
                 las tablas de medido a favor ni de refutado: lo que cambia son
                 calificaciones y agregados con su fuente. Cero corridas, cero
                 cuota, gradlew no ejecutado, nada en Zenodo.
Modo aplicado:   TITAN FULL
Rubrica:         45/45 -> 100/100. Aplicables: Completitud, Arquitectura del
                 razonamiento, Documentacion, Innovacion, Proceso QA.
                 N/A: 45 pts (Ejecutabilidad, Seguridad, Testing, DevOps: es
                 actualizacion de documentacion, no codigo).
N/A declarados:  45 pts
Review externo:  el falsador fue el propio log, que estuvo dos dias en git
                 sin leerse. Contradijo dos afirmaciones de este contexto (la
                 salvedad sobre-generalizada y el 1,18x sin calificar) y aporto
                 el resultado mas limpio de la linea, que el contexto tenia
                 escrito SIN UN SOLO NUMERO.
Instrumento:     ninguno nuevo, y va declarado. Los cuatro puntos son lectura
                 de results/dualbrain_bench.log, commiteado en la resp 047.
                 Evidencia cruda verbatim en la seccion 5.
                 NO MEDIDO: la seccion 7, ocho items.
```
