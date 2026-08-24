# CONTEXTO VIVO · motor / DualBrain / línea embebida

**Última actualización:** 2026-08-24 12:45 (America/Buenos_Aires) · **Se sobreescribe, no se acumula.**

Protocolo: `00-PROTOCOLO-BITACORA-DE-RESPUESTAS.md`. Hermano: `CONTEXTO-drosophila-fep.md`. Entorno **medido** (no recordado): `CONTEXTO-ENTORNO.md`, §12 al 2026-08-24 12:15.

**Por qué este archivo existe aparte:** el motor es el activo monetizable y se lo trató como apéndice de los papers durante 24 h. Los papers son el test suite del motor, no al revés.

---

## 0. LO ÚLTIMO CERRADO (2026-08-24) · auditoría arquitectónica BICAMERALITY ↔ línea actual

Se midió, brazo por brazo, **qué cambió de verdad** entre el `DualBrain` de BICAMERALITY (`bicam/cell1.py`, v5.6) y el actual (`tres_brazos.py`). Resultado: **un solo cambio con efecto**, y la pregunta barata que quedaba **ya cerró en empate**.

| Diferencia | Estado medido | Dónde |
|---|---|---|
| gate escalar `Linear(...,1)` → **vectorial** `Linear(...,h_m)` | **GANA 2/4 con `p<1e-9`**: `CR` 8,34× (`p=1,15e-10`), `LinScale` 3,85× (`p=2,24e-12`). Empata `Gated` (`p=0,45`) y `MultiCue` (`p=0,55`). **No pierde nunca** | resp 021-023 |
| celda: bias en el término de flujo (BICAM lo tiene, la actual **no**) | **CERRADO en EMPATE a n=20: `d`=−0,082, `p`=0,797.** Se retira la advertencia del bias y se retira el estado SUBPOTENCIADO: con n=6 daba `p=0,0571` con `d`=1,10, y al subir la potencia el efecto **desapareció**. No hay que volver a poner el bias | resp 025 → **030** |
| `LiquidRealCell` vs `LiquidCell`, el resto | **NULO. Son la misma función.** `W_flow([x;h]) ≡ W_in(x)+W_res(h)+b`. Transplante de pesos: `err_max h = 3,58e−07`, **`err_max tau = 0.0` exacto** | resp 024 |
| `enc`: `F.gelu` en el forward → `GELU` en el `Sequential` | **NULO.** Mismo cálculo, otro lugar | resp 019 |
| zero-init del gate (`nn.init.zeros_`) | **NULO.** 8 tests, ninguno significativo. No hace daño y no hace falta | resp 023 |
| `react`, defaults `h_r=24 / h_m=8` | **IDÉNTICOS** | resp 019 |
| cabezas `actor`/`critic`/`log_std` → `head` | cambio de **propósito** (RL → regresión), no de arquitectura. No comparable | resp 019 |

**El claim para el paper, con su forma correcta:** *la compuerta vectorial supera a la escalar al mismo presupuesto (~1400 params) en modulación multiplicativa de UNA referencia (8,34× y 3,85×, `p<1e-9`) y es indistinguible cuando media una rectificación o dos referencias (`p=0,45` y `p=0,55`)*.

**Regularidad propuesta, y es HIPÓTESIS ajustada a 4 puntos, no medición:** el gate vectorial gana donde la tarea es **lineal en x con una referencia**; empata con no linealidad en x (`Gated`) o dos referencias (`MultiCue`). Dos celdas de la tabla están vacías. La falsaría: `|x|*c` con 2 refs, y `x*c` con 3 refs.

**Hallazgo estructural, 3/4:** el gate **escalar se satura abierto** (`gmean` 0,970 / 0,970 / 0,964), o sea aprende a **no gatear**. La excepción es `Gated` (0,226), justo la única tarea donde el escalar compite. **4/4:** el gate vectorial nunca colapsa a escalar (`gdisp` 0,18-0,30).

**Validación del instrumento, no pedida:** los 4 brazos de control de `ab_cell.py` reprodujeron los 4 MSE de `ab_gate.py` **a 6 decimales, con sus `sd`**, desde un script escrito de cero. Los números de la resp 023 no son de una corrida afortunada.

**Peritaje de originalidad (resp 028-029), porque cambia cómo se cita:** la celda es LTC de Hasani (MIT, AAAI-21) y la RNN de valores complejos es de 2012-2015. Lo propio **no es la matemática**: es de dónde salen los pesos (conectoma medido + ley de Dale en la fase) y que **no entrena**. Y el motor complejo es un **INSTRUMENTO** (su línea 2 dice «implementación de referencia»), no un hallazgo: evaluarlo con la rúbrica de un hallazgo fue error de categoría mío.

---

## 1. Los tres motores, y NO son el mismo

| Motor | Archivo | Qué es | ¿Entrena? |
|---|---|---|---|
| **SparseLTC** | `src/motor.py` (702 líneas, md5 `480539069ec00f317eec525e6fa81324`), `src/scriptR.py` | 138.639 neuronas reales, τ por neurona, esparsa | **NO. Cero torch, cero Adam, cero backward** |
| **`LiquidCell` denso** | `src/hm_sweep.py`, `tres_brazos.py`, brazo W, `ab_gate.py`, `ab_cell.py` | 8 unidades, densa, Adam | Sí |
| **DualBrain embebido** | `esp32c.py`, C99 | **704 B de RAM**, dos vías + gate | Vía lenta sí, vía rápida no |

**Consecuencia grave y ya registrada:** el brazo W congela una submatriz de 26 nodos dentro del motor **denso**, no dentro de SparseLTC, y **no congela τ**. Su veredicto «0/4, se retira la analogía del 96% fijo» **no refuta la hipótesis: nunca la testeó.** Estado correcto: **NO MEDIDO**.

**Y ojo con el nombre:** SparseLTC **no está dentro de `motor.py`** (`grep -c` = 0). El motor complejo y SparseLTC son **padre e hijo**, misma ecuación, y la comparación entre ambos **ya corre** dentro de `motor.py` como brazo `tau_r`, con veredicto global `p = 0,6000` (resp 027).

---

## 2. La especificación de SparseLTC, verbatim del código

```
z ← (1−τ)·z + τ·f(Wᵗz + s)
```

1. **Pesos complejos:** `|w|` del conectoma, `arg(w)` = signo E/I **por neurona presináptica, no por arista**. Es la ley de Dale y en este conectoma es exacta: **0 de 138.005** neuronas tienen salidas de los dos signos (96.672 excitatorias puras, 41.333 inhibitorias puras). Jitter de fase 0,1. Normaliza a radio espectral 0,99.
2. **τ compleja heterogénea:** `Re(τ)=0,119` fijo, `Im(τ) ~ U(0,01 · 0,15)` distinto por neurona → **banco de osciladores**, no un oscilador.
3. **Guard derivado, no tuneado:** `|Im(τ)| < sqrt(1 − (1−Re)²)` = **0,473116**. `validate_tau` levanta excepción antes de correr.
4. **Activación:** `bounded_complex_tanh` acota el módulo y **preserva la fase**. La tanh cruda explota a 10¹¹ (medido: 9,998×10¹¹).
5. **τ regional:** `SparseLTCRegional` guarda τ como vector por región. Cuerpo fungiforme 0,0180 (56 pasos de memoria) vs óptica 0,2689 (3,7 pasos), **factor 15×**: la zona más lenta es justo el 4% plástico. **PERO las 11 τ están hardcodeadas en `CFG` y las regiones suman 139.255 contra 139.244 reales: es andamio sintético, no medición.**

---

## 3. Medido a favor

| Qué | Número | Instrumento |
|---|---|---|
| Tests del motor complejo | **8 en verde, 0 en rojo**, incluido el control del control (el método uniforme rompe el grado en 106.948 nodos, o sea que el test del bueno mide) | `results/motor_ltc_complejo.log` |
| **Gate vectorial vs escalar, mismo presupuesto** | **8,34× (`CR`) y 3,85× (`LinScale`), `p<1e-9`**, 24 brazos, 6 semillas | resp 023, `ab_gate_A/B.json` |
| Spread de τ heterogénea | 31,2× entre la dimensión más lenta y la más rápida | medición propia |
| Gate multiplicativo | ayuda en **4 de 4** tareas | tres brazos |
| Óptimo interior de reparto react/memoria | h_m=10 / h_r=22 → **1,18× sobre LSTM**; el 4,05× publicado es el **peor punto** de la curva. Mejora 3,44×, Welch `p = 8,59×10⁻¹⁰` | `results/hm_sweep.log`, 10 semillas por punto |
| Brazo más congelado (42,5% entrenable) | le gana a un modelo 100% entrenado sin estructura por **3,2× a 35×**, 4/4 tareas | tres brazos |
| Escape compilado | ganancia **40×** vs detector vecino no cableado (LC4+LPLC2 = 0,704 · LC6 = 0,017) | motor propio |

---

## 4. Refutado, y los dos falsos refutados

| Claim | Estado |
|---|---|
| **«la ventaja de τ compleja es del cableado»** | **NO SOSTENIDA.** El test global sobre los 6 estadísticos da **p = 0,6000** (8/9 nulls por debajo), piso 0,20. El `+0,196 vs −0,027, 0/9` es **solo el snapshot t=199**; en t=120 la ventaja real es **negativa** (−0,02973, p2 = 1,0000) y en t=60 los 9 nulls superan al real. **Y con 9 nulls el estado correcto es NO CONCLUYENTE, no negativo** (resp 029) |
| «la vía reactiva no necesita entrenarse» (tres brazos) | **REFUTADO pero mal medido**: congeló pesos **aleatorios**, no cableados. Midió el null de la hipótesis, no la hipótesis |
| «el brazo W retira la analogía del 96% fijo» (0/4 vs ruido) | **NO MEDIDO, no refutado.** W congela 26 nodos dentro del motor **denso** y **no congela τ**: dos efectos mezclados |
| «con más memoria DualBrain gana en MultiCue» | refutado: no gana, y hay **óptimo interior** en h_m=10. Refuta también la explicación del paper |
| «el circuito de escape detecta aproximación» | refutado: selectividad temporal **1,04×**, o sea ninguna. Es un integrador con exclusión. 13.026 aristas y **cero inhibitorias** |
| «la topología explica la función» | refutado para este circuito: la topología define **ruteo y ganancia**, no selectividad |
| «el gate vectorial es mejor» (mío, genérico) | **refutado como claim general**: gana 2/4, empata 2/4. Depende de la tarea |
| «el zero-init del gate es el punto no obvio» (mío) | **refutado**, 8 tests sin significancia |
| «`LiquidRealCell` puede pesar más que el gate» (mío) | **refutado en 20 segundos**: es la misma función salvo un bias de 8 params sobre 1400 |
| «el bias entra a un `tanh` y un `LayerNorm`, no puede importar» (mío) | **CONFIRMADO a n=20, y por la vía aburrida:** el `LayerNorm` sí deja sobrevivir un bias por dimensión, pero el efecto medido es **nulo** (`d`=−0,082, `p`=0,797). El `d`=1,10 con n=6 era muestra chica |
| «`motor.py` implementa los cinco estados del producto» (mío) | **refutado**: `grep` de los cinco estados en `motor.py` = **0**. Sí tiene las métricas del paper (`rdi`, `region_profile`, `phase_coherence`). Mezclé producto y paper |

**El motor nunca falló en ninguna corrida.** Las fallas encontradas fueron de interpretación, normalización, estimador o diseño de métrica.

---

## 5. El producto, en una línea

**Que el motor deje de necesitar entrenamiento para funcionar.** Topología cableada de fábrica: vía rápida por estructura (reflejo, sin memoria), vía lenta con τ heterogénea acumulando contexto, gate decidiendo cuál manda. Funciona **el primer día, sin dataset**, en 704 B.

- **Es cedible:** un motor con pesos entrenados necesita quien sepa entrenarlo; uno cuya vía rápida es estructura necesita un compilador y una tabla de priors. Lo mantiene un aprendiz.
- **Escala por unidades, no por parámetros.** Lo que hay que escalar es **el compilador**.
- **El activo final no es el motor: es la biblioteca** de circuitos con función verificada (la hoja de datos de los 74xx). El motor es el intérprete.
- **Competidor medido:** Liquid AI (Hasani, 293 M USD, unicornio). Su producto más chico es LFM2.5-230M en Raspberry Pi. Ellos **entrenan**; abajo del teléfono no entran. Citar: complex-valued RNN (2016), echo state networks, «When Learning Hurts: Fixed-Pole RNN» (arXiv 2026).

---

## 6. NO MEDIDO / pendiente

1. **RESUELTO (resp 030):** `LinScale` a n=20 corrió y el bias de flujo cerró en **empate** (`d`=−0,082, `p`=0,797). Ya no hay pregunta abierta en la auditoría arquitectónica. Se deja el ítem para que no se re-lance el mismo experimento.
2. **La hipótesis del 96% fijo sigue sin testear** sobre SparseLTC, y es la deuda más vieja del proyecto. El experimento correcto congela matriz **y** τ, sobre `src/motor.py`. El brazo W midió el motor denso.
3. Con 9 nulls el piso de p a dos colas es **0,20**. Para que la ventaja compleja sea publicable hacen falta más nulls, y el test global ya dio no significativo con 9.
4. **El punto h_m=16 del barrido NO está pareado en presupuesto:** 1593 parámetros contra 1400 (+13,8%), porque `hr_for_hm` busca `h_r` desde 6 y ni el mínimo alcanza. Tiene más parámetros y rinde peor, lo que **refuerza** el óptimo interior, pero no se puede citar en la misma tabla sin la aclaración. Los cinco puntos limpios (5, 6, 8, 10, 13) bastan.
5. Log de `titan-paper-dualbrain` (complete 00:06Z) y `notebookceb82767da` (928 KB): sin leer.
6. Las 11 τ regionales: hardcodeadas, sin medición que las respalde.
7. Regla de tres factores (KC × MBON × dopamina, mayormente **depresión**) contra descenso de gradiente: diseñada, **no lanzada**. Base medida: `DAN→KC` es 23,5× `DAN→MBON`, 8,71× sobre CP, 0/40 → firma presináptica.
8. **7 de los 17 `.py` siguen fuera de git.** Orden pendiente en `respuestas/2026-08-23-006`.
9. **Nada de las 4 tareas del benchmark se probó sobre señal real.** Son sintéticas. El barrido de Bode sigue pendiente.
10. **Resuelto:** el duplicado `paper_db.py` / `dualbrain_src.py` es una **copia byte-idéntica** (md5 `8a42246b54157cbee67fe99110a7be40`, 478 líneas cada uno). No son dos instrumentos.
11. **Línea embebida, desbloqueada y sin usar:** el entorno tiene `xtensa-esp32-elf-gcc 16.1.0` que **compila** (exit=0), medido a las 12:15 (`CONTEXTO-ENTORNO.md` §12). El cruce al ESP32 no está bloqueado por el entorno. **Nadie lo cruzó todavía.**

---

## 7. Instrumentos nuevos disponibles (2026-08-24)

| Archivo | Qué hace |
|---|---|
| `/workspace/ab_gate/ab_gate.py` | A/B de la forma del gate. 6 brazos con familias ISO-ARCH e ISO-BUDGET, métrica `gdisp` (desvío del gate entre dimensiones). md5 `11591eb654eb719ae941aa524c1f59fd` |
| `/workspace/ab_cell/equiv.py` | Prueba de equivalencia por **transplante de pesos** entre dos parametrizaciones. Reutilizable para cualquier «¿son la misma función?». md5 `b829d49ca654ad1d48a2e92e0091e660` |
| `/workspace/ab_cell/ab_cell.py` | A/B del bias con **celda única parametrizada**: los brazos no pueden diferir por accidente. md5 `4278bb8f27f2b0d8e43a26541629c7b8` |

**Lección de método del día, y va a memoria:** antes de lanzar un A/B, **probar si los dos brazos son la misma función**. Costó 20 segundos y bajó el experimento de 6 brazos a 2. El polling de logs con `sleep 45-58` funciona; el timeout del gateway está entre 45 y 75 s. `ps` no existe: liveness con `grep -al <patrón> /proc/[0-9]*/cmdline`.

**Segunda lección, medida hoy:** este archivo estuvo **una hora vencido** afirmando abierta la pregunta del bias que ya había cerrado en la resp 030. La acumulación se actualizó y el estado vivo no. Corregido en la resp 036.
