# CONTEXTO VIVO · motor / DualBrain / línea embebida

**Última actualización:** 2026-08-24 19:55 (America/Buenos_Aires) · **Se sobreescribe, no se acumula.**

Protocolo: `00-PROTOCOLO-BITACORA-DE-RESPUESTAS.md`. Hermano: `CONTEXTO-drosophila-fep.md` (**leer su §0: el erratum vence el 30-ago y su texto ya está en git**). Entorno **medido**: `CONTEXTO-ENTORNO.md`, §13 al 24-ago 14:05. Kaggle: `MANIFIESTO-KAGGLE.md` (**40 kernels, no 29**).

**Por qué este archivo existe aparte:** el motor es el activo monetizable y se lo trató como apéndice de los papers durante 24 h. Los papers son el test suite del motor, no al revés.

---

## 0. LO ÚLTIMO CERRADO · auditoría arquitectónica BICAMERALITY ↔ línea actual

Se midió, brazo por brazo, **qué cambió de verdad** entre el `DualBrain` de BICAMERALITY (`bicam/cell1.py`, v5.6) y el actual (`tres_brazos.py`). Resultado: **un solo cambio con efecto**.

| Diferencia | Estado medido | Dónde |
|---|---|---|
| gate escalar `Linear(...,1)` → **vectorial** `Linear(...,h_m)` | **GANA 2/4 con `p<1e-9`**: `CR` 8,34× (`p=1,15e-10`), `LinScale` 3,85× (`p=2,24e-12`). Empata `Gated` (`p=0,45`) y `MultiCue` (`p=0,55`). **No pierde nunca** | resp 021-023 |
| celda: bias en el término de flujo | **CERRADO en EMPATE a n=20: `d`=−0,082, `p`=0,797.** Con n=6 daba `p=0,0571` y `d`=1,10; al subir la potencia el efecto **desapareció**. No hay que volver a poner el bias | resp 025 → **030** |
| `LiquidRealCell` vs `LiquidCell`, el resto | **NULO. Son la misma función.** `W_flow([x;h]) ≡ W_in(x)+W_res(h)+b`. Transplante: `err_max h = 3,58e−07`, **`err_max tau = 0.0` exacto** | resp 024 |
| `enc`: `F.gelu` en el forward → `GELU` en el `Sequential` | **NULO.** Mismo cálculo, otro lugar | resp 019 |
| zero-init del gate | **NULO.** 8 tests, ninguno significativo | resp 023 |
| `react`, defaults `h_r=24 / h_m=8` | **IDÉNTICOS** | resp 019 |
| cabezas `actor`/`critic`/`log_std` → `head` | cambio de **propósito** (RL → regresión), no de arquitectura | resp 019 |

**El claim para el paper, con su forma correcta:** *la compuerta vectorial supera a la escalar al mismo presupuesto (~1400 params) en modulación multiplicativa de UNA referencia (8,34× y 3,85×, `p<1e-9`) y es indistinguible cuando media una rectificación o dos referencias (`p=0,45` y `p=0,55`)*.

**Regularidad propuesta, HIPÓTESIS ajustada a 4 puntos:** el gate vectorial gana donde la tarea es **lineal en x con una referencia**; empata con no linealidad en x o dos referencias. La falsaría: `|x|*c` con 2 refs, y `x*c` con 3 refs.

**Hallazgo estructural, 3/4:** el gate **escalar se satura abierto** (`gmean` 0,970 / 0,970 / 0,964), o sea aprende a **no gatear**. La excepción es `Gated` (0,226), la única tarea donde compite. **4/4:** el vectorial nunca colapsa a escalar.

**Validación del instrumento:** los 4 brazos de control de `ab_cell.py` reprodujeron los 4 MSE de `ab_gate.py` **a 6 decimales, con sus `sd`**, desde un script escrito de cero.

**Peritaje de originalidad (resp 028-029):** la celda es LTC de Hasani (MIT, AAAI-21) y la RNN de valores complejos es de 2012-2015. Lo propio **no es la matemática**: es de dónde salen los pesos (conectoma medido + Dale en la fase) y que **no entrena**. Y el motor complejo es un **INSTRUMENTO** (su línea 2 dice «implementación de referencia»), no un hallazgo.

---

## 0.bis 🔥 EL RESULTADO MÁS LIMPIO DE LA LÍNEA, y estaba sin numerar: la ablación del gate

**Salió de leer `results/dualbrain_bench.log` al subirlo a git (resp 047).** Este archivo listaba «gate multiplicativo: ayuda en 4 de 4 tareas» **sin un solo número**. Los números están, y son el resultado con menos objeciones posibles de todo el expediente:

```
  ABLACION DEL GATE (DualBrain vs DualNoGate)
  Mismos parametros, misma celda, mismo encoder.
  La unica diferencia: g*h_m contra h_m.

  Gated     con_gate=0.000236  sin_gate=0.025539  AYUDA 108.11x  p=1.56e-105
  LinScale  con_gate=0.000055  sin_gate=0.001192  AYUDA  21.85x  p=3.36e-16
  MultiCue  con_gate=0.000326  sin_gate=0.019235  AYUDA  58.97x  p=4.91e-03
  CR        con_gate=0.000054  sin_gate=0.001979  AYUDA  36.72x  p=1.38e-31
```

**Por qué es el más limpio:** es **iso-run** (mismo kernel), **iso-arquitectura** (mismos `h_r`/`h_m` en cada tarea, mismo presupuesto de 1399 o 1401 params), **iso-celda** y **iso-encoder**. La única variable manipulada es `g*h_m` contra `h_m`. **10 semillas por celda.** No hay comparación entre corridas, no hay diferencia de presupuesto, no hay ajuste de hiperparámetros.

**Y no necesita ningún brazo nuevo: es publicable hoy.** Eso lo distingue del hallazgo de §3, que sigue esperando el brazo `D`.

**El claim exacto que soporta:** *la compuerta multiplicativa sobre la vía de memoria mejora el error entre 21,9× y 108,1× a presupuesto, arquitectura y semilla igualadas, en las cuatro tareas.* Nada sobre el conectoma, nada sobre biología: es una medición de arquitectura.

---

## 1. Los tres motores, y NO son el mismo

| Motor | Archivo | Qué es | ¿Entrena? |
|---|---|---|---|
| **SparseLTC** | `src/motor.py` (702 líneas, md5 `480539069ec00f317eec525e6fa81324`), `src/scriptR.py` | 138.639 neuronas reales, τ por neurona, esparsa | **NO. Cero torch, cero Adam, cero backward** |
| **`LiquidCell` denso** | `src/hm_sweep.py`, `tres_brazos.py`, brazo W, `ab_gate.py`, `ab_cell.py` | 8 unidades, densa, Adam | Sí |
| **DualBrain embebido** | `esp32c.py` genera C99 (`c/dualbrain.c`, `c/dualbrain.h`) | **704 B de RAM en x86** · **1.336 B de `.text` en ESP32/ESP32-S3 a `-Os`**, medido · dos vías + gate | Vía lenta sí, vía rápida no |

**Número nuevo, y ya no es "pendiente de hardware":**

```
xtensa-esp32-elf-gcc -std=c99 -Os -I. -c dualbrain.c  ->  COMPILA_OK_exit0
xtensa-esp-elf-size /tmp/db_os.o
  text data bss dec hex
  1336    0   0 1336 538

xtensa-esp32-elf-gcc -std=c99 -O2 -I. -c dualbrain.c  ->  1796 B
xtensa-esp32s3-elf-gcc -std=c99 -Os -I. -c dualbrain.c -> 1336 B exactos
```

**Consecuencias medibles:**

- El código en el target real es **1,87× más chico** que los **2.496 B** medidos con gcc de x86.
- **`-Os` le gana a `-O2` por 460 B (34%)**. La flag correcta deja de ser supuesto.
- **ESP32 y ESP32-S3 dan el mismo tamaño exacto** para este objeto.
- El `.h` que `CONTEXTO-ENTORNO.md` §10 declaraba faltante **existía desde el 22-ago**. Lo único que faltaba era `-I.` porque el include usa `<dualbrain.h>`.

**Lo que este número NO es:** no hay `.elf`, no hay linkeo, no hay **RAM en target** medida todavía, y **704 B** sigue siendo el número de x86. El throughput sigue derivado del conteo de MAC: **no corrió en hardware**.

**Prueba de que el instrumento puede dar ROJO (W-01):**

```
printf 'int x = "roto";\n' > /tmp/roto.c
xtensa-esp32-elf-gcc -std=c99 -c /tmp/roto.c
  -> error de int-conversion, DIO_ROJO_OK
```

**Consecuencia grave:** el brazo W congela una submatriz de 26 nodos dentro del motor **denso**, no dentro de SparseLTC, y **no congela τ**. Su veredicto «0/4, se retira la analogía del 96% fijo» **no refuta la hipótesis: nunca la testeó.** Estado correcto: **NO MEDIDO**.

**Y ojo con el nombre:** SparseLTC **no está dentro de `motor.py`** (`grep -c` = 0). El motor complejo y SparseLTC son **padre e hijo**, misma ecuación, y la comparación **ya corre** dentro de `motor.py` como brazo `tau_r`, con veredicto global `p = 0,6000` (resp 027).

---

## 2. La especificación de SparseLTC, verbatim del código

```
z ← (1−τ)·z + τ·f(Wᵗz + s)
```

1. **Pesos complejos:** `|w|` del conectoma, `arg(w)` = signo E/I **por neurona presináptica, no por arista**. Es la ley de Dale y en este conectoma es exacta: **0 de 138.005** neuronas con salidas de los dos signos (96.672 excitatorias puras, 41.333 inhibitorias puras). Jitter de fase 0,1. Normaliza a radio espectral 0,99.
2. **τ compleja heterogénea:** `Re(τ)=0,119` fijo, `Im(τ) ~ U(0,01 · 0,15)` distinto por neurona → **banco de osciladores**, no un oscilador.
3. **Guard derivado, no tuneado:** `|Im(τ)| < sqrt(1 − (1−Re)²)` = **0,473116**. `validate_tau` levanta excepción antes de correr.
4. **Activación:** `bounded_complex_tanh` acota el módulo y **preserva la fase**. La tanh cruda explota a 10¹¹ (medido: 9,998×10¹¹).
5. **τ regional:** `SparseLTCRegional` guarda τ por región. Cuerpo fungiforme 0,0180 (56 pasos de memoria) vs óptica 0,2689 (3,7 pasos), **factor 15×**: la zona más lenta es justo el 4% plástico. **PERO las 11 τ están hardcodeadas en `CFG` y las regiones suman 139.255 contra 139.244 reales: es andamio sintético, no medición.**

**De dónde salieron los puntos 3 y 4, y es un dato de procedencia (doc `6077`):** de **auditar un Complex-valued LTC ajeno**. Ese código usa `complex_tanh` como **default**, que es holomorfa y por eso mismo **tiene polos** (medido: `|tanh(z)| = 1e8` a `1e-8` del polo en `i·π/2`), y **no valida el rango de τ** aunque el umbral sea exacto y calculable. Los dos guards del motor propio nacieron de ahí. Bonus de esa auditoría: **el null CP de ese proyecto destruye el grado entrante en 188 de 200 nodos** (`rng.choice` uniforme en vez de permutar los destinos existentes), y su generador sintético usa `reciprocity_factor=36.0` y `density_intra=0.02`, o sea **está calibrado contra el error pre-erratum**.

---

## 3. Medido a favor

| Qué | Número | Instrumento |
|---|---|---|
| Tests del motor complejo | **8 en verde, 0 en rojo**, incluido el control del control (el método uniforme rompe el grado en 106.948 nodos) | `results/motor_ltc_complejo.log` |
| **Gate vectorial vs escalar, mismo presupuesto** | **8,34× (`CR`) y 3,85× (`LinScale`), `p<1e-9`**, 24 brazos, 6 semillas | resp 023, `ab_gate_A/B.json` |
| **⭐ Ablación del gate, iso-run e iso-arquitectura** | **21,85× a 108,11× en 4/4 tareas**, `p` de 4,9e−3 a 1,56e−105, 10 semillas | **`results/dualbrain_bench.log`, ya en git.** Ver §0.bis |
| Spread de τ heterogénea | **31,2×** entre la dimensión más lenta y la más rápida (cortes a −3 dB de 0,00195 a 0,06102 ciclos/muestra) | **`results/dualbrain_bench.log`, sección Bode** |
| Óptimo interior de reparto react/memoria | h_m=10 / h_r=22 → **1,18× sobre LSTM en el óptimo del barrido**. El 4,05× publicado es el **peor punto** de la curva. Mejora 3,44×, Welch `p = 8,59×10⁻¹⁰` | `results/hm_sweep.log`, 10 semillas por punto |
| Escape compilado | ganancia **40×** vs detector vecino no cableado (LC4+LPLC2 = 0,704 · LC6 = 0,017) | motor propio |
| **DualBrain C99 en target real** | **1.336 B de `.text` a `-Os`** en ESP32/ESP32-S3 · `-O2` da 1.796 B | `xtensa-esp32-elf-gcc` 16.1.0 + `xtensa-esp-elf-size`, resp 039 |

### ⚠️ El hallazgo cross-run, con su alcance CORREGIDO (resp 047)

Este archivo decía que *«el brazo más congelado (42,5% entrenable) le gana a un modelo 100% entrenado sin estructura por 3,2× a 35×, 4/4 tareas»* es **cross-run en las cuatro tareas**. Leído el log, es **más preciso que eso**:

| Tarea | `DualNoGate` en el bench | brazo C en `tres_brazos` | ¿misma arquitectura? |
|---|---|---|---|
| `Gated` | `h_r=26 h_m=8` | `h_r=26 h_m=8` | **SÍ** |
| `LinScale` | `h_r=26 h_m=8` | `h_r=26 h_m=8` | **SÍ** |
| `MultiCue` | `h_r=30 h_m=5` | `h_r=26 h_m=8` | no |
| `CR` | `h_r=30 h_m=5` | `h_r=26 h_m=8` | no |

**La comparación es ISO-ARQUITECTURA en 2 de 4 y cross-arquitectura en 2 de 4.** Sigue siendo **entre corridas** en las cuatro (son kernels distintos, así que el brazo `D` **sigue haciendo falta**), pero la salvedad estaba **sobre-generalizada**: en `Gated` y `LinScale` lo único que cambia es la corrida, no la arquitectura.

**Hasta que corra el brazo `D`, no se cita como resultado.** Y **si lo que se necesita es un claim publicable hoy sobre el gate, el de §0.bis ya está limpio** y no depende de ninguna corrida nueva.

### 🔻 Y un resultado EN CONTRA que este archivo no tenía (resp 047)

En el mismo log, **en `MultiCue` el DualBrain PIERDE** contra tres competidores a presupuesto igualado:

```
  MultiCue  (x*(c1+c2)/2, lineal, 2 refs)   DualBrain MSE=0.000326
   vs GRU     MSE=0.000138  ratio=0.42x  p=1.13e-06  gana=GRU
   vs LSTM    MSE=0.000081  ratio=0.25x  p=3.27e-11  gana=LSTM
   vs MinGRU  MSE=0.000191  ratio=0.59x  p=6.17e-04  gana=MinGRU
```

**Esto NO contradice el 1,18× sobre LSTM: son dos configuraciones distintas, y el archivo las mezclaba.** El 1,18× es del **barrido de `h_m` en su óptimo** (`h_m=10 h_r=22`); esta corrida usa `h_r=30 h_m=5`, donde la brecha con LSTM es **4× EN CONTRA** (0,000326 contra 0,000081).

**La lectura correcta, y refuerza el óptimo interior:** el reparto react/memoria **decide si DualBrain gana o pierde** en la tarea de dos referencias. En `h_m=5` pierde 4×; en `h_m=10` queda 1,18× arriba. **Es la misma curva vista desde dos puntos**, y citar uno sin el otro es elegir el favorable.

**Consecuencia para el paper:** el claim sobre `MultiCue` **tiene que llevar el reparto**. «DualBrain queda 1,18× sobre LSTM» es cierto **solo en el óptimo del barrido**, y un revisor que corra la configuración del bench mide lo contrario.

---

## 4. Refutado, y los dos falsos refutados

| Claim | Estado |
|---|---|
| **«la ventaja de τ compleja es del cableado»** | **NO SOSTENIDA.** El test global sobre los 6 estadísticos da **p = 0,6000** (8/9 nulls por debajo), piso 0,20. El `+0,196 vs −0,027, 0/9` es **solo el snapshot t=199**; en t=120 la ventaja real es **negativa** (−0,02973) y en t=60 los 9 nulls superan al real. **Con 9 nulls el estado correcto es NO CONCLUYENTE, no negativo** (resp 029) |
| «la vía reactiva no necesita entrenarse» | **REFUTADO 4/4** (empeora 2,19× a 14,26×, `p` de 5,0e−3 a 1,3e−20) **pero mal medido**: congeló pesos **aleatorios**, no cableados. Midió el **null** de la hipótesis. Y ese error tiene lectura a favor: si congelar ruido hubiera dado igual, **el conectoma no habría hecho falta para nada** — declarado post-hoc (doc `6137`) |
| «el brazo W retira la analogía del 96% fijo» | **NO MEDIDO, no refutado.** W congela 26 nodos dentro del motor **denso** y **no congela τ** |
| «con más memoria DualBrain gana en MultiCue» | refutado: no gana, y hay **óptimo interior** en h_m=10. Refuta también la explicación del paper. **Y el bench lo confirma desde el otro lado:** en `h_m=5` DualBrain **pierde** contra GRU, LSTM y MinGRU en esa tarea (resp 047) |
| «DualBrain queda 1,18× sobre LSTM en MultiCue» (mío, sin calificar) | **INCOMPLETO.** Es cierto **solo en el óptimo del barrido** (`h_m=10 h_r=22`). En la configuración del bench (`h_m=5 h_r=30`) la brecha es **4× en contra**. El claim requiere declarar el reparto (resp 047) |
| «el circuito de escape detecta aproximación» | refutado: selectividad temporal **1,04×**. Es un integrador con exclusión. 13.026 aristas y **cero inhibitorias** — y eso **explica** por qué no discrimina: un motivo que discrimine necesita signo negativo |
| «la topología explica la función» | refutado para este circuito: define **ruteo y ganancia**, no selectividad |
| «el gate vectorial es mejor» (mío, genérico) | **refutado como claim general**: gana 2/4, empata 2/4. Depende de la tarea. **Ojo con no confundirlo con la ablación de §0.bis:** ahí lo que se compara es **gate contra NO gate**, y eso gana 4/4. Vectorial vs escalar es otra pregunta |
| «el zero-init del gate es el punto no obvio» (mío) | **refutado**, 8 tests sin significancia |
| «`LiquidRealCell` puede pesar más que el gate» (mío) | **refutado en 20 segundos**: misma función salvo un bias de 8 params sobre 1400 |
| «el bias entra a un `tanh` y un `LayerNorm`, no puede importar» (mío) | **CONFIRMADO a n=20 por la vía aburrida:** el efecto es **nulo** (`d`=−0,082, `p`=0,797). El `d`=1,10 con n=6 era muestra chica |
| «`motor.py` implementa los cinco estados del producto» (mío) | **refutado**: `grep` de los cinco estados = **0**. Sí tiene las métricas del paper (`rdi`, `region_profile`, `phase_coherence`). Mezclé producto y paper |

**El motor nunca falló en ninguna corrida.** Las fallas fueron de interpretación, normalización, estimador o diseño de métrica.

---

## 5. El producto, en una línea

**Que el motor deje de necesitar entrenamiento para funcionar.** Topología cableada de fábrica: vía rápida por estructura (reflejo, sin memoria), vía lenta con τ heterogénea acumulando contexto, gate decidiendo cuál manda. Funciona **el primer día, sin dataset**, con **1.336 B de código medidos en ESP32** y **704 B de RAM todavía medidos solo en x86**.

- **Es cedible:** un motor con pesos entrenados necesita quien sepa entrenarlo; uno cuya vía rápida es estructura necesita un compilador y una tabla de priors. Lo mantiene un aprendiz.
- **Escala por unidades, no por parámetros.** Lo que hay que escalar es **el compilador**.
- **El activo final no es el motor: es la biblioteca** de circuitos con función verificada (la hoja de datos de los 74xx). Hoy tiene **1** entrada de las 3-4 que hacen falta, y cada entrada dice qué hace **y qué no**.
- **Competidor medido:** Liquid AI (Hasani, 293 M USD, 97 empleados). Su producto más chico es LFM2.5-230M en Raspberry Pi. Ellos **entrenan**; abajo del teléfono no entran. **No es el mismo mercado.** Citar: complex-valued RNN (2016), echo state networks, «When Learning Hurts: Fixed-Pole RNN» (arXiv 2026).
- **Y hay un proyecto hermano que inventa lo que acá está medido** (doc `6057`): su `n_syn = sqrt(size_src × size_dst)` se equivoca **316.852×** entre el mejor y el peor par de bloques (media geométrica del cociente 0,694: **ni centrado**). Existe una tabla medida de **95 pares de bloques** que reemplaza la heurística entera, más los priors de `CONTEXTO-drosophila-fep.md` §3.
- **Lo que el bench dice sobre el nicho, y conviene tenerlo escrito:** DualBrain gana con **una referencia** (`CR` 1,40× a 9,49× sobre todos, `LinScale` 3,72× a 501×) y **pierde con dos** (`MultiCue`, contra GRU, LSTM y MinGRU en la configuración del bench). **El nicho es modulación por una referencia retenida**, no fusión multi-referencia. Venderlo como lo segundo es venderlo donde mide peor.

---

## 6. NO MEDIDO / pendiente

1. **RESUELTO (resp 030):** `LinScale` a n=20 cerró el bias de flujo en **empate**. Se deja el ítem para que no se re-lance el mismo experimento.
2. **⭐ La hipótesis del 96% fijo sigue sin testear** sobre SparseLTC, y es la deuda más vieja del proyecto. **El diseño completo ya está escrito (doc `6137`)** y le falta el brazo que lo hace falsable:

   | Brazo | `react` | Qué aísla |
   |---|---|---|
   | A | denso aleatorio entrenado | el techo |
   | B | denso aleatorio congelado | **ya medido: 3,76× a 14,26× peor** |
   | **W** | máscara del conectoma + τ heterogénea, congelado | si el **cableado** congelado alcanza |
   | **S** | máscara **shuffle** (mismo grado, misma sparsity), congelado | **¿es el conectoma, o cualquier grafo disperso?** |

   **Sin el brazo `S` no es un experimento, es una demo:** un `W` que funcione se explica igual por «menos parámetros efectivos regularizan». **Criterio de aborto ya escrito: si `W` no le gana a `B` en al menos 3 de 4 tareas, la analogía del 96% se retira del paper** y se reemplaza por el hallazgo de §3, que es más chico pero medido. **No se corren más variantes para rescatarla.** Costo ~90 min de CPU, 4 brazos, 10 semillas. El único trabajo nuevo es la máscara desde el parquet, que ya está cargado y verificado.
3. **El brazo `D`** (`DualNoGate` en la misma corrida, `h_r=26 h_m=8`): **~25 min**, y sin él el hallazgo cross-run de §3 no se cita. **Nota de prioridad:** si el objetivo es un claim sobre el gate, **§0.bis ya lo tiene y no cuesta nada**; el brazo `D` sirve para el claim sobre **estructura congelada**, que es otra cosa.
4. Con 9 nulls el piso de `p` a dos colas es **0,20**. Para que la ventaja compleja sea publicable hacen falta **40** (piso 0,0488), y el test global ya dio no significativo con 9. **Es el umbral #3 del plan de 10 semanas.** Semillas: `1000 + 7·i` desde i=9.
5. **El punto h_m=16 del barrido NO está pareado en presupuesto:** 1593 parámetros contra 1400 (+13,8%). Tiene más parámetros y rinde peor, lo que **refuerza** el óptimo interior, pero no se cita en la misma tabla sin la aclaración. Los cinco puntos limpios (5, 6, 8, 10, 13) bastan.
6. **El log de `titan-paper-dualbrain` ya se leyó** (es `results/dualbrain_bench.log`, en git desde la resp 047). **Sigue sin leer `notebookceb82767da`** (928 KB).
7. Las 11 τ regionales: hardcodeadas, sin medición que las respalde.
8. Regla de tres factores (KC × MBON × dopamina, mayormente **depresión**): diseñada con 4 brazos, **no lanzada**. Base medida: `DAN→KC` es 23,5× `DAN→MBON`, **8,71× sobre CP, 0/40** → la modulación llega al lado de la **entrada**, que es la firma de una regla presináptica. **Limitación declarada antes de correr: una regla de aprendizaje se testea sobre una tarea, y el conectoma no trae ninguna.** La tarea es una **elección nuestra**, no un dato, y va declarada o un revisor la encuentra. **Aborto: si el brazo sin DA aprende igual, el tercer factor es decorativo y se cierra ahí. No se ajustan constantes hasta que funcione.**
9. **6 `.py` siguen fuera de git**, ya identificados uno por uno con su kernel y su md5 desde los dos lados: `brazo_w.py`, `n21.py`, `esp32c.py`, `tres_brazos.py`, `nulls19b.py`, `paper_db.py` (169.586 B en total). Tabla en `MANIFIESTO-KAGGLE.md`.
10. **Nada de las 4 tareas del benchmark se probó sobre señal real.** Son sintéticas. **El barrido de Bode SÍ está hecho** y da el spread de 31,2× (§3), pero sobre senoidales inyectadas, no sobre señal de un sensor.
11. **Resuelto:** el duplicado `paper_db.py` / `dualbrain_src.py` es **copia byte-idéntica** (md5 `8a42246b54157cbee67fe99110a7be40`), y ahora se sabe **de qué kernel salen**: `titan-paper-dualbrain`.
12. **Línea embebida, desbloqueada y medida a medias:** `xtensa-esp32-elf-gcc 16.1.0` **compila** (exit=0), y el C99 real da **1.336 B de `.text` en target**. **Nadie lo linkeó ni lo corrió todavía.** La RAM en target sigue sin medir.
13. **Motivos nuevos para la biblioteca: cero avance.** Hacen falta ≥ 3 con 0/40 y hay **1**. Candidatos con inhibición: lateral del cuerpo fungiforme (APL), coordinación del complejo central. **Aborto del plan: si en su semana no hay al menos dos con 0/40, P3 sale de las 10 semanas.**
14. **`dualbrain_bench.json` (31.527 B, md5 `1025d60b4e9521d7e4a21ed282935049`) no está commiteado**, va referenciado por md5. Su evidencia verbatim **sí** está en `results/dualbrain_bench.log`. Las **10 semillas individuales** de cada celda viven en ese JSON, no en el log: **el log trae media y `sd`, no la serie**.

---

## 7. Instrumentos disponibles

| Archivo | Qué hace |
|---|---|
| `/workspace/ab_gate/ab_gate.py` | A/B de la forma del gate. 6 brazos ISO-ARCH e ISO-BUDGET, métrica `gdisp`. md5 `11591eb654eb719ae941aa524c1f59fd` |
| `/workspace/ab_cell/equiv.py` | Prueba de equivalencia por **transplante de pesos**. Reutilizable para cualquier «¿son la misma función?». md5 `b829d49ca654ad1d48a2e92e0091e660` |
| `/workspace/ab_cell/ab_cell.py` | A/B con **celda única parametrizada**: los brazos no pueden diferir por accidente. md5 `4278bb8f27f2b0d8e43a26541629c7b8` |
| `results/dualbrain_bench.log` | **En git.** 6 modelos, 4 tareas, 10 semillas, barrido de Bode y ablación del gate. 98,3 min de CPU |

**Lecciones de método, todas con su costo medido:**

1. **Antes de lanzar un A/B, probar si los dos brazos son la misma función.** Costó 20 segundos y bajó el experimento de 6 brazos a 2.
2. **Antes de lanzar un brazo de control, escribir en una línea qué afirmación exacta cambia según su resultado.** Si la afirmación no menciona la propiedad que el brazo manipula, el brazo está mal armado. La afirmación decía «cableado» y el brazo manipulaba «entrenado sí/no»: **se veía en una lectura y costó 69,8 minutos de cuota**.
3. **Si `sd(null) == 0`, el null conserva la cantidad y el test no puede fallar.** Reportar **NO TESTEABLE**, no `1,000×`. Cuatro líneas, 22,2 minutos ahorrados.
4. **Este archivo estuvo una hora vencido** (resp 036), citó un resultado **cross-run como concluyente** hasta la resp 038, y **sobre-generalizó su propia salvedad** hasta la resp 047. La acumulación se actualiza sola; el estado vivo no.
5. **En este shell, `echo "$?"` dio `exit=0` sobre una compilación fallida.** El guard válido es `if <cmd>; then ... else ... fi` (resp 039).
6. **El `.h` no faltaba: faltaba leer el include.** La medición vieja declaró una ausencia que se cerraba con `ls -l c/` y una lectura de línea 8 (`#include <dualbrain.h>`). Otro caso de sujeto equivocado.
7. **Un log sin leer es un resultado sin usar, y puede ser el mejor que hay.** El `dualbrain_bench.log` figuró como «sin leer» durante dos días y contenía **la medición más limpia de toda la línea** (§0.bis), más un resultado en contra que el contexto no tenía, más la fuente del 31,2× que figuraba como «medición propia» sin archivo. **Se leyó solo porque había que subirlo a git.**
8. **Dos números de la misma curva no son dos mediciones independientes.** El 1,18× sobre LSTM y el 4× en contra son el mismo modelo en `h_m=10` y en `h_m=5`. Citar uno sin el reparto es elegir el punto favorable.
9. El polling de logs con `sleep 45-58` funciona; el timeout del gateway está entre 45 y 75 s. `ps` no existe: liveness con `grep -al <patrón> /proc/[0-9]*/cmdline`.
