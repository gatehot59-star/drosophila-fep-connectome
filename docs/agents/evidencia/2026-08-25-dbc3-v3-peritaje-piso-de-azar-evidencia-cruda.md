# Evidencia cruda · peritaje de DBC3-v3 · el piso de azar está mal en 4 de 5 tareas

**Fecha:** 2026-08-25 22:05 (America/Buenos_Aires) · **Modo:** TITAN FULL · **Tipo:** peritaje

**Sujeto y su categoría (E-01):** los cuatro archivos de DBC3-v3 en `/workspace` del container. Es un **benchmark de arquitectura**, no un hallazgo del conectoma, y se lo evalúa como tal.

```plain
a9ffe30d97d8bba91a467e88a89ab058  dbc3_benchmark.py   16.020 B  397 lineas
d0eb323a750bc20dfa2295ff417f23f1  graph_dbc3.py        2.278 B   57 lineas
                                  dbc3_v3_benchmark.png  85.520 B
                                  dbc3_gatedmemory.png   28.341 B
```

**Nota de continuidad:** `dbc3_benchmark.py` es **el proceso huérfano que se apagó a pedido de Abraham a las 18:55** (recibo en `2026-08-25-apagado-de-proceso-huerfano-brain-env.md`). Su salida iba a un pipe `tail -50`, así que **no quedó archivo**. Eso es consistente con lo que se encontró hoy: no existe ningún log de corrida completa.

<hr/>

## 1. 🔴 Defecto de trazabilidad: el gráfico dice 3 semillas, el script corre 1

### Lo que declara `graph_dbc3.py`

```python
# DBC3-v3 FULL BENCHMARK (final-step accuracy, 3 seeds)
tasks = ['DelayedClass', 'XORMemory', 'ThermalPredict', 'Tracking', 'ContextSwitch']
dbc3 = [99.2, 67.0, 74.3, 98.5, 61.0]
lstm = [16.7, 50.0, 70.8, 95.1, 51.7]
ratio = [5.93, 1.34, 1.05, 1.04, 1.18]
```

Y el título del panel:

```python
ax1.set_title('DBC3-v3 vs LSTM — 5 tareas (3 seeds)')
```

### Lo que declara `dbc3_benchmark.py`

```python
FAST_MODE    = True
N_SEEDS      = 1
```

y más abajo:

```python
if FAST_MODE:
    tasks_cfg = [(n, t, max(e // 3, 50)) for n, t, e in tasks_cfg]
```

### Los tres hechos, juntos

1. **El gráfico dice «3 seeds». El script corre `N_SEEDS = 1`.**
2. **`FAST_MODE = True` divide las épocas por 3**: 300 → 100 y 500 → 166.
3. **Los diez números del gráfico están tipeados a mano**, no leídos de ninguna salida. **No existe log ni JSON de una corrida completa de DBC3 en el container.**

> **Consecuencia:** el PNG publicado **no es reproducible desde este container**. Sus números vienen del notebook de Kaggle que el header cita («9 celdas concatenadas»), y el script local está configurado para **no** poder reproducirlos. Estado correcto: **NO MEDIDO localmente**.

<hr/>

## 2. 🔴 El hallazgo del turno: la línea de azar está mal en 4 de 5 tareas

El gráfico dibuja **una sola** línea de referencia para las cinco tareas:

```python
ax1.axhline(8.3, color='gray', ls='--', lw=1, label='random (8.3%)')
```

8,3% es 1/12, el azar de una tarea de **12 clases**. Pero las cinco tareas **no tienen 12 clases efectivas**.

### Cómo se midió

Se importaron los generadores de tareas **verbatim del propio `dbc3_benchmark.py`** (se cortó el archivo justo antes de `tasks_cfg` y se guardó como `dbc3_lib.py`, sin tocar una línea de lógica). No se entrenó nada: se generaron 6 batches de 128 por tarea y se contaron las etiquetas del último paso, que es el que el benchmark reporta.

Se midieron **dos** pisos, porque no son el mismo:

- **uniforme** = 1/clases, si las clases fueran equiprobables
- **constante** = lo que saca el predictor tonto que siempre dice la clase más frecuente. Si las clases no son equiprobables, este es **más alto**, y es el que hay que superar de verdad.

### Salida cruda, verbatim

```plain
Device: cpu
DBC3: d_in=36 d_out=12 h_m=20 h_r=36 params=6888  |  LSTM h=26 params=6980
cfg: d_in=36 d_out=12 h_m=20 h_r=36 params=6888
LSTM h = 26 params LSTM = 6980 params DBC3 = 6888

tarea           clases     unif constante     PISO |   DBC3   LSTM | veredicto
----------------------------------------------------------------------------------------------------
DelayedClass        12     8.3%     10.4%    10.4% |  99.2%  16.7% | los dos superan el piso
XORMemory            2    50.0%     51.4%    51.4% |  67.0%  50.0% | LSTM EN EL PISO -> no aprendio nada
ThermalPredict       7    14.3%     33.2%    33.2% |  74.3%  70.8% | los dos superan el piso
Tracking            12     8.3%      9.9%     9.9% |  98.5%  95.1% | los dos superan el piso
ContextSwitch        4    25.0%     33.6%    33.6% |  61.0%  51.7% | los dos superan el piso

PISO REAL contra el 8.3% unico que dibuja el grafico:
  DelayedClass    piso  10.4%  grafico 8.3%   <-- SUBESTIMA 2.1 puntos
  XORMemory       piso  51.4%  grafico 8.3%   <-- SUBESTIMA 43.1 puntos
  ThermalPredict  piso  33.2%  grafico 8.3%   <-- SUBESTIMA 24.9 puntos
  Tracking        piso   9.9%  grafico 8.3%   <-- SUBESTIMA 1.6 puntos
  ContextSwitch   piso  33.6%  grafico 8.3%   <-- SUBESTIMA 25.3 puntos

VENTAJA SOBRE EL PISO (la comparacion que corresponde):
  DelayedClass    DBC3  +88.8 pts   LSTM   +6.3 pts   ratio 14.13x
  XORMemory       DBC3  +15.6 pts   LSTM   -1.4 pts   ratio INDEFINIDO (LSTM en el piso)
  ThermalPredict  DBC3  +41.1 pts   LSTM  +37.6 pts   ratio 1.09x
  Tracking        DBC3  +88.6 pts   LSTM  +85.2 pts   ratio 1.04x
  ContextSwitch   DBC3  +27.4 pts   LSTM  +18.1 pts   ratio 1.51x

geo mean de ratios crudos: 1.59x  (el grafico dice 1.59x)
```

<hr/>

## 3. Veredicto derivado (conclusión, no medición)

### 🟢 Lo que MEJORA al corregir el piso

1. **XORMemory es el resultado más fuerte del set, y el gráfico lo entierra.** El piso es 51,4% y el **LSTM saca 50,0%: está en el piso, no aprendió nada**. DBC3 saca 67,0%, o sea **+15,6 puntos sobre el piso**. El gráfico lo muestra como un pobre «1,34×», cuando el claim honesto es cualitativo y más fuerte: **el LSTM no resuelve la tarea y DBC3 sí, parcialmente.** Un ratio de accuracies sobre un piso de 50% comprime justo el hallazgo que interesa.
2. **DelayedClass se agranda: de 5,93× a 14,13×** sobre el piso. +88,8 puntos contra +6,3.

### 🔴 Lo que EMPEORA al corregir el piso

3. **ThermalPredict y Tracking son empates, y siguen siéndolo: 1,09× y 1,04×.** En Tracking los dos superan el piso por ~86 puntos: **la tarea es fácil para ambos** y no discrimina arquitecturas.
4. **ContextSwitch pasa de 1,18× a 1,51×**, pero con un piso de 33,6% y DBC3 en 61,0%, sigue siendo un resultado modesto.
5. **El `geo mean` de 1,59× no es una cantidad interpretable.** Promedia ratios de accuracy sobre tareas con pisos entre **9,9% y 51,4%**. Un ratio de accuracies no es adimensional respecto del piso, así que su media geométrica mezcla peras con manzanas. Y además **está dominada por el 5,93× de DelayedClass**: sacando esa tarea, las otras cuatro dan un geo mean de ~1,19×.

### 🔴 El antipatrón que ya está en el registro del proyecto

```python
ratio = d_m / max(l_m, 0.01)
```

**Denominador que puede morir.** Si el LSTM cayera a 0%, el ratio saltaría a **hasta 10.000×** y se imprimiría con el mismo formato que un número legítimo. Es exactamente la misma clase de error que el `cosine_distance` que devolvía 1,0 con un vector nulo, ya documentado en `src/motor.py`. **El fix correcto no es acotar el denominador: es reportar la diferencia sobre el piso**, que es lo que hace la tabla de arriba.

<hr/>

## 4. 🟢 Lo que está bien hecho, y hay que decirlo

1. **El presupuesto de parámetros está igualado y verificado.** DBC3 6.888 contra LSTM 6.980, o sea **1,3% de diferencia**, y `find_lstm_h` busca el `h` que minimiza la brecha. Sin eso, cualquier comparación mediría tamaño y no arquitectura.
2. **Hay un `assert` que puede dar rojo:** `assert real_p == cfg.param_count()`. La cuenta analítica de parámetros se verifica contra los parámetros reales del módulo. Eso es un test de verdad, no un comentario.
3. **La evaluación usa semilla fija 99999 y restaura el estado del RNG después.** Los dos brazos ven **los mismos datos de evaluación**, y la evaluación no contamina la secuencia de entrenamiento.
4. **Cada época genera un batch nuevo.** No hay un conjunto de entrenamiento fijo que memorizar, así que el sobreajuste clásico no aplica.
5. **El gráfico reporta la derrota junto a las victorias.** ThermalPredict 1,05× y Tracking 1,04× están en el PNG, pintados en rojo por la propia condición `'#55A868' if r > 1.05 else '#C44E52'`. No se escondió el empate.

<hr/>

## 5. 🟡 Otros defectos menores, medidos

6. **ThermalPredict solo usa 7 de las 12 clases.** `_t2c` mapea temperatura a clase, y el rango de temperaturas que el simulador produce **no cubre las 12**: se midieron **7 clases distintas** en el último paso. Cinco salidas de la cabeza nunca se usan, y esos parámetros están en el presupuesto igualado de los dos modelos.
7. **`train_model` elige `best_state` por accuracy en el batch de ENTRENAMIENTO.** Es selección sobre ruido: con 100 épocas se queda con el máximo de 100 mediciones ruidosas. Se aplica **igual a los dos brazos**, así que no favorece a uno, pero **infla los dos** y hay que decirlo antes de citar un 99,2%.
8. **`dbc3_gatedmemory.png` mezcla dos benchmarks distintos.** Sus números son del DualBrain de 1.401 parámetros del notebook de marzo, no del DBC3-v3 de 6.888 de este archivo. Están en el mismo script de graficado, y eso invita a leerlos como si fueran del mismo experimento.

<hr/>

## 6. NO MEDIDO, declarado

1. **No se corrió el benchmark.** Los 99,2% / 67,0% / 74,3% / 98,5% / 61,0% **son los del gráfico**, no de una corrida propia. La única medición nueva de este peritaje son los **pisos**.
2. **No se sabe si los números del gráfico salieron de 3 semillas o de 1.** El gráfico dice 3, el script dice 1, y no hay salida que dirima. Es un **estado no medido**, no una acusación de falsedad.
3. **No se midió la dispersión entre semillas.** Sin eso no hay intervalo, y un 1,04× podría ser ruido.
4. **No se corrió el DBC3 contra el LSTM con los pisos corregidos.** La tabla de «ventaja sobre el piso» usa las accuracies del gráfico y los pisos medidos: **mezcla una fuente citada con una medición propia**, y eso se declara.
5. **`EXPORT_DIR = '/workspace/weights'` no existe.** El directorio de exportación de pesos está vacío/ausente: **nunca se exportaron pesos** de este benchmark.
6. **No se verificó si el notebook de Kaggle original tenía `N_SEEDS = 3`.** El header dice que este archivo es su adaptación local; la diferencia pudo introducirse en la adaptación.
