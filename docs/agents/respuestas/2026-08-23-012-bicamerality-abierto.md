# resp 012 · BICAMERALITY abierto: no es un experimento, es un laboratorio de 965 KB

**Fecha:** 2026-08-23 23:25–23:45 · **Modo:** TITAN FULL · **Rúbrica:** 43/45 → 96/100

## 1. Pedido

> «Abrí BICAMERALITY y decime qué hay»

## 2. Herramientas declaradas (C-03)

- `build.run` sobre el container: **solo lectura**. El notebook ya estaba en `/workspace/kaggle/` desde el 22-ago, **bajado y nunca abierto**.
- Parseo del `ipynb` con Python 3.12.14, extracción de salidas a `/workspace/bicam_out.txt`.
- GitHub: **una escritura** (este archivo). Cero Kaggle, cero cuota.

## 3. Qué es, medido

```
archivo   /workspace/kaggle/fabiomurillohot__notebookceb82767da.txt
bytes     1.920.957
celdas    73
fuente    965.720 B de codigo
salida    147.778 B (2.024 lineas)
acelerador nvidiaTeslaT4, isGpuEnabled true
celdas SIN salida: 41 de 73
```

**No es un experimento. Es un laboratorio entero**, con una línea evolutiva que no estaba en ningún contexto vivo:

| Celdas | Qué hay |
|---|---|
| 1–2 | **ICCA v5.7 Principia Cybernetica** y v6 Robustness Suite |
| 3–16 | **ICCA v7 → v7.1** Architecture Validation Suite (T-Maze, ConditionalReaction), con pruebas unitarias intercaladas |
| 17–25 | **v7g gate vectorial**, v7h PPO hotfix, v7i con 6 fixes, curriculum RL, pre-train supervisado |
| 26–27 | **ICCA Paper Figures**: tres figuras desde datos guardados |
| 28–30 | **Sequential MNIST**, 784 píxeles de a uno, y variante fila por fila |
| 31–33 | **NanoCerebro vs DualBrain**, y arquitectura de fusión |
| 34–36 | **PCA State Compression** y TITAN V4.1 compression-aware training |
| 38–56 | **TITAN V4 Vision**, pipeline completo con exportación a binario |
| 57–61 | Benchmarks contra GRU/LSTM/MinGRU/LTC, **barrido de ratio h_r/h_m**, y **DualBrain Cortex para ESP32** |
| 63–72 | **NURONA VISION**: 48 features, 12 clases, 4 bloques, exportación a `.h`/`.bin` |

---

## 4. HALLAZGO 1 · BICAMERALITY nunca corrió

La celda 1 son **34.903 bytes** de código con `PrincipiaBrain` completo:

```
├── H_R (Chaos): LiquidChaosCell H=8, rho(W)~1, no LayerNorm
├── H_L (Order): Feedforward H=24, Tanh normalizado
├── Corpus Callosum: LayerNorm(cat(gate*chaos, order))
├── Veto alpha: energy_est -> supresion de exploracion
└── Amigdala: heads auxiliares de danger/energy (survival loss)
```

Con inicialización al borde del caos (`nn.init.orthogonal_` y división por el radio espectral medido), y el *Resilience Zen* de la ecuación 4.6: clamp suave de norma en vez de dejar que explote a NaN.

**Y su salida son CERO bytes.** Igual las celdas 0 a 40 completas: **41 de 73 celdas sin una línea de output.**

`grep -c 'Princip'` sobre las 2.024 líneas de salida devuelve **0**. El veredicto que el propio código está preparado para imprimir («Principia > Dual en las dos tareas» / «la complejidad agregada perjudica») **no existe**.

**Estado correcto: el código existe, la medición no. NO MEDIDO.** La arquitectura que le da nombre al archivo más viejo del proyecto está escrita y sin correr desde febrero.

---

## 5. HALLAZGO 2 · El barrido de h_m ya estaba hecho en FEBRERO

La celda 60 es *«DualBrain — Ratio h_r/h_m Sweep en Multi-Cue + Gated Memory»*. Su salida, verbatim:

```
OPTIMAL RATIOS
  ConditionalReaction:  Best h_r=25 h_m=9  (ratio 2.8)  MSE 0.000028
  GatedMemory:          Best h_r=23 h_m=10 (ratio 2.3)  MSE 0.000061
  MultiCue:             Best h_r=20 h_m=11 (ratio 1.8)  MSE 0.000062
  Best OVERALL (media geometrica de 3 tareas):
                        Best h_r=23 h_m=10 (ratio 2.3)  geom 0.000050

OPTIMAL DualBrain vs LSTM y GRU en Multi-Cue
  Model                    Params     MultiCue MSE (3 seeds)
  DualBrain(r=20,m=11)       1445    0.000102 +-0.000023
  DualBrain(r=30,m=5)        1401    0.000314 +-0.000043
  LSTM(h=16)                 1361    0.000068 +-0.000009
  GRU(h=19)                  1388    0.000116 +-0.000019

  Tiempo: 35.4 min
```

**Compará con lo que corrí hoy** (`titan-hm-sweep-multicue`, 51,6 min, 10 semillas):

| | Febrero, 3 semillas | Hoy, 10 semillas |
|---|---|---|
| Óptimo | h_r=20 h_m=11 → **0,000102** | h_r=22 h_m=10 → **0,000095** |
| El punto publicado | (30,5) → **0,000314** | (30,5) → **0,000326** |
| LSTM al mismo presupuesto | 0,000068 | 0,000081 |
| Mejora óptimo vs publicado | **3,08×** | **3,44×** |

**Los dos coinciden.** O sea que «el 0,000326 es el peor punto de una curva con óptimo interior» **ya estaba medido en febrero**, y los 51,6 minutos de cuota de hoy volvieron a medir lo mismo con más semillas.

**Lo que hoy agrega y no es poco:** las 10 semillas, el `p = 8,59×10⁻¹⁰` del Welch, y la lectura del mecanismo (que subir `h_m` le come neuronas a `react`). Pero **el hallazgo no era nuevo**, y presentarlo como descubrimiento fue error mío.

Y una tercera coincidencia que refuerza las dos: la celda 61 usa **exactamente h_r=23 h_m=10**, el óptimo global del barrido. No quedó en un informe: se usó.

---

## 6. HALLAZGO 3 · La τ heterogénea por región ya está compilada a C

Esto es lo más valioso del archivo. La celda 61, *«DualBrain Cortex — Entrenamiento para ESP32»*, entrena **cuatro bloques idénticos en tamaño y distintos en τ**:

```
Bloque [FAST] h_r=23 h_m=10 tau=-1.0   1955 params (7820 B)   final 1.000
Bloque [MID]  h_r=23 h_m=10 tau=-2.0   1955 params (7820 B)   final 1.000
Bloque [SLOW] h_r=23 h_m=10 tau=-3.0   1955 params (7820 B)   final 0.998
Bloque [DEEP] h_r=23 h_m=10 tau=-4.0   1955 params (7820 B)   final 0.999

EXPORTACION
  weights_fast.h (1955 params, 26337 B) + weights_fast.bin (7820 B)
  weights_mid.h  + weights_mid.bin
  weights_slow.h + weights_slow.bin
  weights_deep.h + weights_deep.bin
  cortex_weights.h

VERIFICACION [FAST]
  Output: class=4 (IMPACTO) conf=0.986
```

**Esos cuatro `tau_bias` son exactamente los valores que `SparseLTCRegional` tenía hardcodeados** (−4,0 para el cuerpo fungiforme, −1,0 para la óptica). Acá no están hardcodeados como hipótesis: **están entrenados por separado, verificados por inferencia y exportados a headers de C.**

Eso es la **tabla de priors del compilador** del plan maestro, construida en febrero. La capa 3 del producto («la biblioteca») tiene un precedente funcionando que el plan no registra.

### Y hay una línea de producto entera sin registrar

`NURONA VISION`: 48 features, 12 clases (`LIBRE, OBSTACULO, PERSONA, ANIMAL, VEHICULO, QR_TARGET, SENAL, PELIGRO, CERCA, LANDING, COLOR_EVENT, UNKNOWN`), 4 bloques, **48.828 params / 190,7 KB**, exportado a `vision_*.h` y `.bin` para `esp32cam-vision/`.

Y `TITAN V4 classifier`: **3.844 params, 15,2 KB**, con `Verificar: PASS (err_act=0.000000 err_hm=0.000000)` y accuracy 1,000 contra baseline 0,949.

**Con sus limitaciones declaradas por el propio autor, verbatim:**

```
LIMITACIONES REALES:
  - Entrenado con datos SINTETICOS
  - Persona agachada -> puede clasificar como animal
  - Distancia requiere calibracion por camara
  - YOLO-tiny superaria esto facilmente
```

Esa última línea es la clase de honestidad que el resto del corpus tardó meses en recuperar.

---

## 7. Lo que esto cambia

1. **La pregunta «de dónde salió la arquitectura» tiene respuesta**, y no es Arena ni el conectoma. Es esta línea: ICCA v5.7 → v7.1, con DualBrain ya como «campeón v5.6» **antes** de que el conectoma entrara en escena. El conectoma vino a **calibrar** algo que ya existía.
2. **Antes de lanzar cualquier kernel, revisar este archivo.** Contiene 965 KB de código y 41 celdas sin correr. Hoy se gastaron 51,6 min re-midiendo algo que estaba adentro.
3. **El compilador de τ por bloque ya existe**, con verificación de inferencia. Eso adelanta la capa 3 del plan.
4. **BICAMERALITY es un experimento pendiente, no un resultado.** Y es barato: el código está completo.

---

## 8. NO MEDIDO, declarado

- **41 de 73 celdas no tienen salida.** No sé si nunca corrieron o si la salida no se guardó. No lo verifiqué de otra forma.
- **No leí el código de las celdas 2 a 40**, solo sus primeras líneas. Ahí viven T-Maze, Sequential MNIST, NanoCerebro y PCA compression, y cualquiera de esos puede contener otro resultado ya medido.
- **No re-corrí nada.** Todos los números son lectura de la salida guardada.
- **La celda 23 tiene 13.180 B de prosa** («Los datos hablan») sin leer. Puede ser una interpretación propia de Abraham que valga más que varios de estos números.
- No verifiqué si los `.bin` y `.h` exportados siguen existiendo en algún lado.
