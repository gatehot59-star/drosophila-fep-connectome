# 020 · A/B gate escalar vs vectorial — diseño, smoke y job VIVO

**Fecha:** 2026-08-24 00:5x (America/Buenos_Aires)
**Estado:** CORRIENDO. `resultado_leido = 0`. Ver §7.

## 1. Pedido

"Corré el A/B gate escalar vs vectorial". Sale del NO MEDIDO que yo mismo declaré en la respuesta 019: el diff mostró que la única diferencia arquitectónica real entre el `DualBrain` de BICAMERALITY y el actual es `Linear(h_r+h_m, 1)` vs `Linear(h_r+h_m, h_m)`, y **nadie había medido si eso ayuda**.

## 2. Herramientas declaradas (C-03)

- `gateway build.run` (container `brain-env`, PC de Abraham). Escribe en `/workspace/ab_gate/`. **2 procesos python3 en background, ~2 h de CPU de tu máquina.** Cero cuota de Kaggle, cero red.
- `githubmcp_get_file_contents` + `githubmcp_create_or_update_file`.

## 3. El diseño, y los dos confundidos que separa

Un A/B ingenuo (cambiar `1` por `h_m` y comparar) mide **tres cosas a la vez** y no distingue cuál ganó:

1. la **forma** del gate (escalar vs vectorial),
2. el **presupuesto**: el gate vectorial agrega `(h_r+h_m)*h_m + h_m - (h_r+h_m) - 1` parámetros. Medido para `hr=26, hm=8`: **1399 vs 1154, o sea el vectorial tiene 21% más de parámetros entrenables**. Si gana así, ganó el presupuesto.
3. el **zero-init**: el actual hace `nn.init.zeros_` en peso y bias del gate, el viejo usa init por defecto. Eso arranca en `sigmoid(0)=0.5` exacto y no es lo mismo que arrancar al azar.

Así que van **6 brazos en 2 familias**, mismas 4 tareas verbatim del benchmark, mismas semillas, `STEPS=2000` (igual que la corrida publicada, para que los números sean comparables):

| Brazo | Gate | Init | (h_r,h_m) | Qué aisla |
|---|---|---|---|---|
| `V0_vector_zeroinit` | vectorial | zeros | calib vector | **el actual** |
| `Vr_vector_randinit` | vectorial | default | calib vector | efecto del zero-init |
| `S0_scalar_zeroinit_isoarch` | escalar | zeros | calib vector | forma del gate, **misma arquitectura** (menos params) |
| `Sr_scalar_randinit_isoarch` | escalar | default | calib vector | **BICAMERALITY-like** |
| `S0b_scalar_zeroinit_isobudget` | escalar | zeros | calib scalar | forma del gate, **mismo presupuesto ~1400** |
| `Srb_scalar_randinit_isobudget` | escalar | default | calib scalar | idem, init default |

ISO-BUDGET recalibra `(h_r,h_m)` para el escalar hasta volver a ~1400 parámetros. Es la comparación honesta y **es la que puede dar vuelta el resultado**, porque el escalar libera 245 parámetros que se re-invierten en `h_m`.

Métrica extra que agrego y no estaba: **`gate_disp_across_dims`** = desvío del gate **entre las 8 dimensiones**, promediado sobre batch y tiempo. Para el escalar es 0 por construcción. Es la medición directa de si el gate vectorial **usa** su libertad o colapsa a un escalar disfrazado. Si diera ~0, el vectorial sería decorativo.

## 4. Evidencia cruda — smoke (1 semilla, 60 steps, tarea Gated)

Corrido para dimensionar y para verificar que el instrumento no está roto. **No es el resultado**, con 60 steps nada converge.

```
nproc = 2
=== A/B GATE ESCALAR vs VECTORIAL ===
torch 2.13.0+cpu threads 4 seeds 1 steps 60

### TAREA Gated |x|*c rectificacion
   calib vector hr=26 hm=8 params=1399
   calib scalar hr=13 hm=16 params=1401
   V0_vector_zeroinit               p=1399 hr=26 hm= 8 MSE=0.044033 sd=0.000000 gmean=0.543 gdisp=0.0876 6s
   Vr_vector_randinit               p=1399 hr=26 hm= 8 MSE=0.044067 sd=0.000000 gmean=0.536 gdisp=0.1385 4s
   S0_scalar_zeroinit_isoarch       p=1154 hr=26 hm= 8 MSE=0.047081 sd=0.000000 gmean=0.578 gdisp=0.0000 4s
   Sr_scalar_randinit_isoarch       p=1154 hr=26 hm= 8 MSE=0.046113 sd=0.000000 gmean=0.607 gdisp=0.0000 4s
   S0b_scalar_zeroinit_isobudget    p=1401 hr=13 hm=16 MSE=0.029312 sd=0.000000 gmean=0.509 gdisp=0.0000 3s
   Srb_scalar_randinit_isobudget    p=1401 hr=13 hm=16 MSE=0.029485 sd=0.000000 gmean=0.564 gdisp=0.0000 4s
   TEST ISO-ARCH: forma del gate           ratio=  1.069x gana=V0_vector_zeroinit
   TEST ISO-BUDGET: forma del gate         ratio=  0.666x gana=S0b_scalar_zeroinit_isobudget
   TEST efecto del zero-init (vector)      ratio=  1.001x gana=V0_vector_zeroinit
   TEST efecto del zero-init (scalar)      ratio=  0.979x gana=Sr_scalar_randinit_isoarch
   TEST actual vs BICAMERALITY-like        ratio=  1.047x gana=V0_vector_zeroinit
MINUTOS 0.41
FIN_AB_GATE
```

Control de determinismo: repetida la misma celda con `THREADS=1` en vez de 4, el MSE sale **idéntico a 6 decimales** (`0.044033`, `0.044067`, `0.047081`). O sea que el número no depende del threading, y `THREADS=1` es además más rápido con modelos de este tamaño.

**Lo que el smoke ya insinúa, y hay que decirlo antes de tener el definitivo:** en ISO-ARCH el vectorial gana 1,069×, pero en **ISO-BUDGET el escalar gana 1,50×** (ratio 0,666). Con 60 steps y n=1 eso **no prueba nada** (`p` sale `nan`, un solo dato por brazo), pero es la dirección contraria a la que yo esperaba y queda escrita ANTES de ver el resultado real, para que no pueda acomodar la narrativa después.

## 5. Evidencia cruda — lanzamiento del definitivo

```
setsid env NSEEDS=6 STEPS=2000 THREADS=1 TAG=A TASKS=Gated,LinScale  nohup python3 /workspace/ab_gate/ab_gate.py > runA.log
setsid env NSEEDS=6 STEPS=2000 THREADS=1 TAG=B TASKS=CR,MultiCue     nohup python3 /workspace/ab_gate/ab_gate.py > runB.log

--- procesos ab_gate vivos ---
6
--- logA ---
=== A/B GATE ESCALAR vs VECTORIAL ===
torch 2.13.0+cpu threads 1 seeds 6 steps 2000
### TAREA Gated |x|*c rectificacion
   calib vector hr=26 hm=8 params=1399
   calib scalar hr=13 hm=16 params=1401
--- logB ---
=== A/B GATE ESCALAR vs VECTORIAL ===
torch 2.13.0+cpu threads 1 seeds 6 steps 2000
### TAREA CR x*cue, cue en +-1
   calib vector hr=30 hm=5 params=1401
   calib scalar hr=12 hm=16 params=1398
```

Dos correcciones de entorno medidas en el camino, que contradicen notas anteriores mías:

- **Los procesos en background SÍ sobreviven entre llamadas** en este container (verificado vía `/proc`, 6 coincidencias después de dos llamadas separadas). La nota vieja que decía lo contrario aplicaba a otro caso, no a este.
- **`ps` no existe** en el container. La liveness se mide con `grep -al <patron> /proc/[0-9]*/cmdline`.
- Primer lanzamiento falló: `cd X && ... &` backgroundea la cadena entera, así que el segundo proceso arrancó en `/` y murió con `can't open file /workspace/ab_gate.py`. Se relanzó con rutas absolutas. **El log del fallo está en esta sección a propósito.**

## 6. Archivos generados

- `/workspace/ab_gate/ab_gate.py` (237 líneas, md5 `11591eb654eb719ae941aa524c1f59fd`, `ast.parse` OK)
- `/workspace/ab_gate/ab_gate_smoke.json`, `ab_gate_smoke1t.json`
- `/workspace/ab_gate/ab_gate_A.json`, `ab_gate_B.json` — **guardado incremental brazo por brazo**, sobreviven si el proceso muere
- `/workspace/ab_gate/runA.log`, `runB.log`
- Este archivo.

## 7. TRABAJO VIVO — `resultado_leido = 0`

| Campo | Valor |
|---|---|
| Dónde | container `brain-env`, `/workspace/ab_gate/` |
| Qué | A/B gate escalar vs vectorial, 6 brazos × 4 tareas × 6 semillas × 2000 steps |
| Lanzado | 2026-08-24 ~00:50 (America/Buenos_Aires) |
| ETA | ~2 h (proceso A, `Gated`+`LinScale`) / ~1,2 h (proceso B, `CR`+`MultiCue`) |
| Cómo se lee | `tail -40 /workspace/ab_gate/runA.log` y `runB.log`, o los dos JSON |
| Estado | **CORRIENDO, SIN LEER** |

**Este es exactamente el fallo que Abraham me marcó con el brazo W** (una hora completo y sin leer). Queda registrado en git, no en la ventana del chat, así que si el contexto se corta el puntero sobrevive.

## 8. NO MEDIDO, declarado

- **El resultado definitivo no existe todavía.** Todo lo numérico de §4 es un smoke de 60 steps con n=1 y `p=nan`. **No citar como resultado.**
- **No comparé contra GRU/LSTM/MinGRU/LTC** en esta corrida. El A/B es interno al gate, no un benchmark de arquitecturas.
- **n=6 semillas**, no 10. Con dispersión alta el Welch va a quedar flojo; si el efecto sale chico habrá que subir n antes de afirmar nada.
- **No midí `LiquidRealCell` vs `LiquidCell`.** Sigue siendo la diferencia no auditada entre BICAMERALITY y la línea actual, y puede ser más grande que la del gate.
- **El A/B usa `LiquidCell` (la actual) en los seis brazos.** O sea que mide la forma del gate, **no** reproduce BICAMERALITY entero.

```
--- METODO TITAN ---
Accion delicada: NO en cuanto a datos (nada se borra, nada se mergea, cero cuota
                 ajena de Kaggle). SI en cuanto a recurso: ~2 h de CPU en la PC
                 de Abraham, 2 procesos en background. Declarado antes de lanzar.
Modo aplicado:   TITAN FULL
Rubrica:         pendiente. Se emite con el resultado, no ahora: puntuar un
                 experimento por su diseno antes de leer su salida es
                 exactamente el antipatron que persigue el Bloque 8.
N/A declarados:  pendiente
Review externo:  no pedido, sin PR asociado
Instrumento:     build.run sobre brain-env, python3 3.12 / torch 2.13.0+cpu,
                 nproc=2, THREADS=1, exit=0 en el smoke.
                 /workspace/ab_gate/ab_gate.py md5 11591eb654eb719ae941aa524c1f59fd
                 Salida cruda verbatim del smoke en la seccion 4 y del
                 lanzamiento en la seccion 5.
                 RESULTADO DEFINITIVO: NO MEDIDO TODAVIA (seccion 7).
```
