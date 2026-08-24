# 023 · A/B gate escalar vs vectorial — **CERRADO, 4/4 tareas**

**Fecha:** 2026-08-24 ~03:45 (America/Buenos_Aires)
**Estado:** COMPLETO. `resultado_leido = 1`. 24 brazos, 144 entrenamientos, 284 min de CPU.

## 1. Pedido

"Leé LinScale cuando cierre". Cierra la serie 020 → 021 → 022 → 023.

## 2. Herramientas declaradas (C-03)

`gateway build.run` sobre `brain-env`, **solo lectura de logs**. GitHub para este commit. Cero cuota de Kaggle.

## 3. EVIDENCIA CRUDA VERBATIM — `LinScale`, completa

```
### TAREA LinScale x*c CONTROL
   calib vector hr=26 hm=8 params=1399
   calib scalar hr=13 hm=16 params=1401
   V0_vector_zeroinit               p=1399 hr=26 hm= 8 MSE=0.000066 sd=0.000014 gmean=0.425 gdisp=0.2455 670s
   Vr_vector_randinit               p=1399 hr=26 hm= 8 MSE=0.000058 sd=0.000019 gmean=0.335 gdisp=0.2462 643s
   S0_scalar_zeroinit_isoarch       p=1154 hr=26 hm= 8 MSE=0.055419 sd=0.000812 gmean=0.213 gdisp=0.0000 493s
   Sr_scalar_randinit_isoarch       p=1154 hr=26 hm= 8 MSE=0.055409 sd=0.000831 gmean=0.210 gdisp=0.0000 478s
   S0b_scalar_zeroinit_isobudget    p=1401 hr=13 hm=16 MSE=0.000254 sd=0.000064 gmean=0.964 gdisp=0.0000 535s
   Srb_scalar_randinit_isobudget    p=1401 hr=13 hm=16 MSE=0.018731 sd=0.028653 gmean=0.658 gdisp=0.0000 593s
   TEST ISO-ARCH: forma del gate           ratio=839.433x t=-166.97 p=0.000e+00 gana=V0_vector_zeroinit
   TEST ISO-BUDGET: forma del gate         ratio=  3.851x t=  -7.02 p=2.237e-12 gana=V0_vector_zeroinit
   TEST efecto del zero-init (vector)      ratio=  0.880x t=   0.83 p=4.053e-01 gana=Vr_vector_randinit
   TEST efecto del zero-init (scalar)      ratio=  1.000x t=   0.02 p=9.834e-01 gana=Sr_scalar_randinit_isoarch
   TEST actual vs BICAMERALITY-like        ratio=839.284x t=-163.19 p=0.000e+00 gana=V0_vector_zeroinit

ARCHIVO /workspace/ab_gate/ab_gate_A.json
MINUTOS 159.96
FIN_AB_GATE
```

## 4. EVIDENCIA CRUDA VERBATIM — `MultiCue`, completa (cerró después de la resp 022)

```
   Srb_scalar_randinit_isobudget    p=1398 hr=12 hm=16 MSE=0.000424 sd=0.000154 gmean=0.834 gdisp=0.0000 507s
   TEST ISO-ARCH: forma del gate           ratio= 82.403x t=-202.44 p=0.000e+00 gana=V0_vector_zeroinit
   TEST ISO-BUDGET: forma del gate         ratio=  1.152x t=  -0.59 p=5.523e-01 gana=V0_vector_zeroinit
   TEST efecto del zero-init (vector)      ratio=  1.111x t=  -0.39 p=6.949e-01 gana=V0_vector_zeroinit
   TEST efecto del zero-init (scalar)      ratio=  0.999x t=   0.11 p=9.113e-01 gana=Sr_scalar_randinit_isoarch
   TEST actual vs BICAMERALITY-like        ratio= 82.346x t=-201.65 p=0.000e+00 gana=V0_vector_zeroinit

ARCHIVO /workspace/ab_gate/ab_gate_B.json
MINUTOS 124.49
FIN_AB_GATE
```

JSON finales: `ab_gate_A.json` md5 `77b4946057464508ffd252a5823257e0`, `ab_gate_B.json` md5 `99375541cb937491bfa467f12de718ca`. Los dos procesos terminaron con `FIN_AB_GATE`.

## 5. LA TABLA ÚNICA — ISO-BUDGET, que es la comparación honesta (~1400 parámetros los dos)

| Tarea | Vectorial | Mejor escalar | ratio | p | Veredicto |
|---|---|---|---|---|---|
| `CR` — `x*cue`, cue ±1 | **0,000043** | 0,000284 | **8,34×** | 1,15e-10 | **vectorial gana** |
| `LinScale` — `x*c` | **0,000066** | 0,000254 | **3,85×** | 2,24e-12 | **vectorial gana** |
| `MultiCue` — `x*(c1+c2)/2` | 0,000340 | 0,000391 | 1,15× | 0,552 | **empate** |
| `Gated` — `\|x\|*c` | 0,000298 | 0,000230 | 0,80× | 0,447 | **empate** |

**2 de 4 con `p` de piso, 2 de 4 empate. Ninguna derrota significativa.**

ISO-ARCH (misma arquitectura, el escalar con 245 parámetros menos) da 3907×, 839×, 82× y 0,77×. Los tres primeros son casos donde **el escalar no aprende la tarea** (MSE ≈ varianza del target), no "pierde": no es el titular y no hay que citarlo como tal.

## 6. VEREDICTO — y mi propia explicación de la resp 022 queda refutada

**El cambio de `Linear(...,1)` a `Linear(...,h_m)` está justificado por medición: gana 2/4 con p de piso y no pierde nunca.** Ese es el resultado, y es más fuerte que el que tenías antes de esta corrida (que era ninguno).

**Pero el mecanismo que propuse en la resp 022 es falso.** Escribí que el vectorial aporta "donde hay que invertir el signo de la respuesta según una referencia retenida". `LinScale` es el contraejemplo: **es el control lineal, no exige rectificación ni inversión de fase, y es la segunda victoria más grande (3,85×)**. Lo escribí con 3 tareas y la cuarta lo rompió. Por eso existía el control.

**La regularidad que SÍ separa las 4 tareas:**

| | lineal en x | rectificado | → |
|---|---|---|---|
| **1 referencia** | `CR` **8,34×** · `LinScale` **3,85×** | `Gated` empate | |
| **2 referencias** | `MultiCue` empate | — | |

**El gate vectorial gana exactamente en las dos tareas que son lineales en x con UNA referencia retenida, o sea modulación multiplicativa pura. Empata donde hay una no linealidad en x (rectificar) o donde hay que combinar dos referencias.**

Y hay que decirlo como lo que es: **esto es una hipótesis ajustada a 4 puntos, no una medición.** Con 2 celdas de la tabla vacías, cualquier regla de dos factores cierra. Lo que refuta la anterior es dato; lo que propone ésta es programa de trabajo. El experimento que la falsaría: `|x|*c` con dos referencias, y `x*c` con tres.

### El hallazgo estructural, y también hay que corregirlo

En la resp 022 escribí que el escalar "se satura abierto" en 3/3. Con las 4 cerradas es **3/4**:

| Tarea | `gmean` escalar iso-budget | |
|---|---|---|
| `CR` | 0,970 | saturado **abierto** |
| `MultiCue` | 0,970 | saturado **abierto** |
| `LinScale` | 0,964 | saturado **abierto** |
| `Gated` | **0,226** | **cerrado — la excepción** |

**Y la excepción es coherente, no ruido: `Gated` es justamente la única tarea donde el escalar es competitivo.** O sea que el escalar rinde exactamente donde encuentra un punto de operación no degenerado. Donde no lo encuentra, aprende a **no gatear** (dejar pasar todo) y ahí pierde. Un gate que converge a la identidad es un gate que se rindió.

Lo que sí es **4/4**: el gate vectorial nunca colapsa a escalar. `gdisp` (desvío entre dimensiones) da 0,295 / 0,246 / 0,256 / 0,180. Usa su libertad en las cuatro tareas, incluso en las dos donde no le sirve para bajar el MSE.

### El zero-init está muerto, ahora con 4/4

`p` = 0,195 (`CR`) · 0,082 (`Gated`) · 0,695 (`MultiCue`) · 0,405 (`LinScale`) en el vectorial, y 0,968 / 0,431 / 0,911 / 0,983 en el escalar. **Ocho tests, ninguno significativo.** Mi claim de la resp 019 ("el punto no obvio del gate cero-inicializado") queda retirado con las cuatro tareas. El `nn.init.zeros_` no hace daño y no hace falta.

## 7. Qué hacer con esto — O-01, criterio: qué convierte esto en un resultado publicable

1. **El claim del paper cambia y mejora.** No "el gate vectorial es mejor", sino: *"la compuerta vectorial supera a la escalar al mismo presupuesto en tareas de modulación multiplicativa con una referencia (8,34× y 3,85×, p<1e-9) y es indistinguible cuando media una rectificación o dos referencias (p=0,45 y p=0,55)"*. Es más específico, más falsable, y **no tiene que esconder nada**.
2. **Falsar la regla de §6** con las dos celdas vacías: `|x|*c` con 2 refs y `x*c` con 3 refs. 4 brazos, ~40 min.
3. **`LiquidRealCell` vs `LiquidCell`**: la única diferencia entre BICAMERALITY y la línea actual que sigue sin auditar, y puede ser más grande que la del gate.
4. **`Gated` a n=20** solo si el empate importa para una decisión. Hoy no la bloquea.

## 8. NO MEDIDO, declarado

- **La regla de §6 tiene 2 de 4 celdas vacías.** Es hipótesis, no medición. Declarado arriba.
- **n=6.** Los dos ganadores aguantan (p<1e-9); los dos empates dicen "no puedo distinguirlos", **no** "son iguales".
- **`Srb` en `LinScale` tiene sd=0,0287 sobre media 0,0187**: dispersión mayor que la media, o sea que **algunas semillas divergieron**. Por eso el test usó `S0b` (el mejor escalar) y no `Srb`. No investigué cuántas semillas fallaron.
- **No hay comparación contra GRU/LSTM/MinGRU/LTC.** Este A/B es interno al gate.
- **Los tiempos de `Gated` no son comparables** con el resto: corrió contendido por mi job duplicado (resp 021). Los MSE no.
- **`gdisp` es métrica mía**, sin antecedente en el benchmark publicado.
- **Nada de esto se probó sobre señal real.** Las 4 tareas son sintéticas.

## 9. Scorecard — R-01: instrumento de diagnóstico + peritaje

Aplicables: Completitud, Ejecutabilidad, Arquitectura del razonamiento, Documentación, Innovación, Proceso QA.

| Criterio | Score | Evidencia |
|---|---|---|
| Completitud | 14/15 | 24 brazos × 6 semillas × 2000 steps, 4 tareas, 20 tests, los dos procesos con `FIN_AB_GATE`. **−1:** la regla de §6 queda con 2 celdas sin medir |
| Ejecutabilidad | 15/15 | `ab_gate.py` corrió de punta a punta dos veces (`exit=0`, `MINUTOS 159.96` y `124.49`), guardado incremental por brazo, md5 de los dos JSON |
| Arquitectura del razonamiento | 10/10 | El diseño separó de antemano los tres confundidos (forma, presupuesto, init) y **el tercero resultó nulo**, o sea que el control sirvió. El control `LinScale` refutó mi propia explicación: existía para eso |
| Documentación | 10/10 | Salida cruda verbatim de las 4 tareas repartida entre resp 021, 022 y §3-4, sin recortar. Tabla única en §5 con la comparación honesta, no la favorable |
| Innovación | 5/5 | No pedido: la familia ISO-BUDGET (sin ella el 21% de parámetros extra se llevaba el crédito) · la métrica `gdisp` · el hallazgo del escalar saturado abierto · y que la excepción de `Gated` sea justo la tarea donde el escalar compite |
| Proceso QA | 5/5 | Tres claims propios retirados con evidencia: el zero-init (019), "el vectorial es mejor" en general (022), y "invertir fase" como mecanismo (022). Cada uno con su `p` |

**59/60 aplicables → 98/100.** N/A declarados: **40 pts** (Seguridad, Testing, DevOps: es un instrumento de medición, no código de producción con superficie ni deployment).

```
--- METODO TITAN ---
Accion delicada: NO en esta lectura. La corrida consumio ~284 min de CPU en la
                 PC de Abraham (declarado antes de lanzar, resp 020), mas un
                 kill -9 sobre un proceso duplicado mio (resp 021).
Modo aplicado:   TITAN FULL
Rubrica:         59/60 -> 98/100
N/A declarados:  40 pts (Seguridad, Testing, DevOps)
Review externo:  no pedido, sin PR asociado. DEUDA declarada (K-02).
                 El falsador real fue el experimento: retiro TRES claims mios.
                 El mas importante lo retiro el brazo de control LinScale, que
                 estaba puesto exactamente para poder refutar la explicacion.
Instrumento:     build.run sobre brain-env, python3 3.12 / torch 2.13.0+cpu,
                 nproc=2, THREADS=1, 6 semillas, 2000 steps, Adam lr=1e-3,
                 clip 1.0, evaluacion con 2000 secuencias frescas.
                 /workspace/ab_gate/ab_gate.py md5 11591eb654eb719ae941aa524c1f59fd
                 ab_gate_A.json md5 77b4946057464508ffd252a5823257e0 (159.96 min)
                 ab_gate_B.json md5 99375541cb937491bfa467f12de718ca (124.49 min)
                 Salida cruda verbatim: resp 021 (CR), resp 022 (Gated), y
                 secciones 3-4 de este archivo (LinScale, MultiCue).
                 NO MEDIDO: seccion 8.
```
