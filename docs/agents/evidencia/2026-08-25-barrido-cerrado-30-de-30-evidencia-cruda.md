# EVIDENCIA CRUDA · el barrido cerrado (30/30) y qué es el motor del ESP32

**Fecha:** 2026-08-25 16:10 (America/Buenos_Aires)
**Instrumento:** `src/cascade_sensitivity.py` md5 `74a6a2261e87e8683147364cc9227c20`, **`DONE in 15376.5 s`**, `out.json` de 19.828 B

---

## 1. 🟢 EL BARRIDO CERRÓ · 30 de 30

### Los últimos 13 puntos, verbatim

```
  p=0.0100 seed=  4  vis= 52.62  olf=105.62  mec= 92.00  gus=105.30  | AZAR=105.62  spread=  2.007  SATURADO
  p=0.0100 seed= 16  vis= 94.62  olf=105.22  mec=105.53  gus=105.88  | AZAR=105.78  spread=  1.119  SATURADO
  p=0.0100 seed= 64  vis=105.35  olf=105.70  mec=105.38  gus=105.45  | AZAR=105.50  spread=  1.003  SATURADO
  p=0.0100 seed=256  vis=105.60  olf=105.58  mec=105.53  gus=105.10  | AZAR=105.30  spread=  1.005  SATURADO
  p=0.0300 seed=  1  vis= 51.60  olf= 89.47  mec= 64.88  gus=105.65  | AZAR= 94.78  spread=  2.047  SATURADO
  p=0.0300 seed=  4  vis= 91.90  olf=108.33  mec=108.38  gus=108.38  | AZAR=108.25  spread=  1.179  SATURADO
  p=0.0300 seed= 16  vis=108.28  olf=108.47  mec=108.22  gus=108.15  | AZAR=108.10  spread=  1.003  SATURADO
  p=0.0300 seed= 64  vis=108.22  olf=108.08  mec=108.35  gus=108.53  | AZAR=108.10  spread=  1.004  SATURADO
  p=0.0300 seed=256  vis=107.85  olf=108.15  mec=108.35  gus=108.38  | AZAR=108.33  spread=  1.005  SATURADO
  p=0.1000 seed=  1  vis= 57.50  olf=106.85  mec= 96.08  gus=109.60  | AZAR=106.85  spread=  1.906  SATURADO
  p=0.1000 seed=  4  vis=106.92  olf=109.62  mec=109.53  gus=109.72  | AZAR=109.72  spread=  1.026  SATURADO
  p=0.1000 seed= 16  vis=109.58  olf=109.67  mec=109.72  gus=109.65  | AZAR=109.50  spread=  1.001  SATURADO
  p=0.1000 seed= 64  vis=109.67  olf=109.62  mec=109.70  gus=109.65  | AZAR=109.58  spread=  1.001  SATURADO
  p=0.1000 seed=256  vis=109.65  olf=109.70  mec=109.75  gus=109.75  | AZAR=109.72  spread=  1.001  SATURADO
```

### Veredicto 1 · la saturación es REAL y es del parámetro, no de mi código

```
  puntos con alguna clase >= 99 (90% de 110): 14 de 30
  puntos donde TODAS estan >= 99:              9 de 30
  puntos con spread entre clases < 1.05:      10 de 30
```

**Con `p_trans >= 0.03` y `N_seed >= 16` las cuatro clases dan 108 y el spread es 1,003×.** El modelo **no distingue nada** ahí.

### 🔴 Veredicto 2 · el control al azar, y ANGOSTA lo que reporté con 16 filas

```
  visual   azar gana en 24 de 30   azar pierde en  5
  olfat    azar gana en 20 de 30   azar pierde en  7
  mecano   azar gana en 21 de 30   azar pierde en  8
  gustat   azar gana en 11 de 30   azar pierde en 17

  a las CUATRO a la vez: 8
  ultimo (peor que las 4): 3
```

> **Con 16 puntos dije «el azar le gana a las vías reales». Con 30 hay que angostarlo: le gana a TRES de las cuatro. Gustativa le gana al azar en 17 de 30.**
>
> **Tercera vez hoy que un dato nuevo angosta un claim mío, y las tres veces en la misma dirección: menos fuerte de lo que dije.** El enunciado correcto es *«el azar le gana a tres de las cuatro clases en la mayoría del rango»*.

### 🟢 Veredicto 3 · VISUAL es la única especificidad robusta

```
  visual es la MAS BAJA de las cuatro en 26 de 30
  visual por debajo del azar en          24 de 30
```

**Eso sobrevive el barrido entero.** Y coincide en dirección con lo que el modelo lineal con signo mide, aunque el lineal separa 98× y la cascada 2×.

---

## 2. 🔥 ÍTEM 1 CERRADO · las dinámicas que faltaban, y dan el hallazgo más fino

```
  --- COOPERATIVE ---
    gustatory+mechanosensory         total=105.70 +/- 1.36   gust= 42.02   mech= 23.70
    visual+olfactory                 total=105.35 +/- 1.26   visu=  0.15   olfa=102.55
    mechanosensory+visual            total=105.55 +/- 1.24   mech=104.62   visu=  0.17
  --- COMPETITIVE ---
    gustatory+mechanosensory         total=105.70 +/- 1.03   gust= 60.20   mech= 45.50
    visual+olfactory                 total=105.67 +/- 1.19   visu=  1.50   olfa=104.17
    mechanosensory+visual            total=105.65 +/- 1.17   mech=105.47   visu=  0.17
```

> ### 🎯 **Cuando dos modalidades compiten por el mismo nodo, VISUAL PIERDE CASI SIEMPRE.**
>
> `visual + olfactory`: **1,50 contra 104,17**. `mechano + visual`: **105,47 contra 0,17**, o sea **620×**.
>
> **El total alcanzado es el mismo (105,7) pero el reparto es de 1 a 70.** Esa asimetría **el modo unimodal no puede verla**, porque ahí cada clase corre sola y llega al techo igual. **Es la mejor cosa que salió de implementar las dinámicas que le faltaban a mi réplica**, y es exactamente el ítem 1 de la deuda.

**Y `gustatory + mechanosensory` reparte 60/45**, o sea que **entre esas dos sí hay competencia real.** La asimetría no es general: es contra visual.

---

## 3. 🔴 EL HALLAZGO INCÓMODO · el motor del ESP32 **no es** el del conectoma

Leído el `CONTEXTO-motor`, sección *«Los tres motores, y NO son el mismo»*, verbatim:

| Motor | Qué es | ¿Entrena? |
|---|---|---|
| **SparseLTC** | **138.639 neuronas reales**, τ por neurona, esparsa | **NO. Cero torch, cero Adam** |
| `LiquidCell` denso | 8 unidades, densa, Adam | Sí |
| **DualBrain embebido** | genera C99, **704 B de RAM**, dos vías + gate | **vía lenta SÍ entrena** |

> **Todo lo que compilé, linkeé y verifiqué hoy en xtensa es DualBrain embebido: un controlador de 3.553 parámetros con 12 entradas y 1 salida. NO contiene el conectoma.**
>
> **El puente entre el conectoma medido y el código que corre en el chip NO está construido.** Y eso **no aparece en ningún NO MEDIDO de mis últimas cuatro respuestas**: estuve reportando «el motor» sin aclarar cuál de los tres, cuatro turnos seguidos. **Es tapar por omisión el hueco más importante del proyecto.**

---

## 4. Las partes del motor, medidas del header

```
  entradas por paso  : 12 floats
  salidas por paso   : 1 float
  memoria (h_m)      : 16 floats  <- lo UNICO que persiste entre pasos
  via reactiva (h_r) : 32 floats  <- se recalcula de cero cada paso

  react capa 1           416    11.7%
  react capa 2          1056    29.7%
  encoder                208     5.9%
  W_in (memoria)         256     7.2%
  W_res (memoria)        256     7.2%
  tau_learner            528    14.9%
  gate                   784    22.1%
  head (salida)           49     1.4%
  TOTAL                 3553   -> 14.212 B en flash

  via REACTIVA (reflejo, sin memoria): 1472  41.4%
  via LENTA (memoria con tau)        : 1248  35.1%
  el GATE que decide cual manda      :  784  22.1%
  la salida                          :   49   1.4%
```

**El `tau_learner` (528 parámetros, 14,9%) es la pieza que hace esto distinto de una RNN común:** no hay una constante de tiempo fija, la red **decide por dimensión y por paso** cuánto olvidar. Y **el gate se lleva el 22%** para una sola decisión: cuál de las dos vías manda.

---

## 5. Cómo escala, medido

```
  duplicando UNIDADES:
    x1  HR=32  HM=16   MAC=  3440 (1.0x)   params=  3553   flash= 14212 B   RAM=  704 B
    x2  HR=64  HM=32   MAC= 12512 (3.6x)   params= 12737   flash= 50948 B   RAM= 1408 B
    x4  HR=128 HM=64   MAC= 47552 (13.8x)  params= 48001   flash=192004 B   RAM= 2816 B
    x8  HR=256 HM=128  MAC=185216 (53.8x)  params=186113   flash=744452 B   RAM= 5632 B

  duplicando ENTRADAS (sensores):
    OBS= 12  MAC=3440 (1.00x)   OBS= 24  MAC=4016 (1.17x)
    OBS= 48  MAC=5168 (1.50x)   OBS= 96  MAC=7472 (2.17x)
```

> **Cuadrático en unidades, lineal en sensores.** Duplicar las unidades cuesta **3,6×** de cómputo; multiplicar por 8 los sensores cuesta **2,17×**. **Agregar sensores es barato; agregar capacidad de cómputo interno es caro.** Eso decide en qué dirección conviene crecer.

### El presupuesto en un ESP32-WROOM-32 (520 KB SRAM, 4 MB flash)

```
  codigo (.text)      1492 B
  pesos (flash)      14212 B
  RAM total modulo     800 B

  fraccion de la SRAM : 0.150%
  fraccion del flash  : 0.374%
  caben por RAM       : 665 instancias
  caben por flash     : 267 instancias
```

### Y la comparación con el competidor que el contexto cita

```
  LFM2.5-230M de Liquid AI:  230M params = 877 MB a float32, 219 MB en int8
  este motor              :  3.553 params = 13,9 KB
  ratio                   :  64.734x
  el ESP32 tiene 0,5 MB de RAM -> el de 230M no entra ni en int8
```

---

## 6. Throughput: **una cota, NO una medición**

```
  ESP32 a 240 MHz, 3440 MAC por paso:
    si un MAC cuesta  1 ciclo  ->  69767 pasos/s  ( 14.3 us por paso)
    si un MAC cuesta  3 ciclos ->  23256 pasos/s  ( 43.0 us por paso)
    si un MAC cuesta  6 ciclos ->  11628 pasos/s  ( 86.0 us por paso)
    si un MAC cuesta 10 ciclos ->   6977 pasos/s  (143.3 us por paso)
```

**⚠️ Los cuatro son COTAS, no mediciones.** El costo real en ciclos por MAC en xtensa **no se midió**. Lo único medido de tiempo es el de Tachi en **host x86** (3.488 ns por paso con Pade), y él lo etiqueta correctamente como host.

---

## 7. NO MEDIDO, declarado

1. **El puente conectoma → chip NO existe.** El motor del ESP32 tiene 3.553 parámetros y **no contiene** las 138.639 neuronas. **Es el hueco principal y estuvo sin declarar cuatro turnos.**
2. **Nada corrió en un ESP32 real.** El throughput son cotas aritméticas.
3. **El `.elf` no es flasheable** (sin startup).
4. **La vía lenta de DualBrain SÍ entrena**, según el propio contexto. Así que el claim «funciona el primer día sin dataset» **aplica a la vía rápida, no al motor completo**, y eso hay que decirlo cuando se vende.
5. **Las 4 tareas del benchmark son sintéticas.** Nada se probó sobre señal de un sensor real.
6. **El desbalance de tamaño del control del barrido sigue sin corregir:** 256 nodos contra pools de 408 a 10.855.
7. **Los 12 pasos de cascada son elección mía**, no de Betzel.
