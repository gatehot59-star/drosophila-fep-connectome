# 2026-10-10-003 · Hacia dónde vamos: el cableado manda, la neurona líquida no paga; toca cerrar, no abrir

**Veredicto en criollo:** con el conectoma vamos a **cerrar el paper** sobre el cableado: la reciprocidad cae a medida que la señal se acerca a la salida motora, y eso sobrevive al umbral de 5 sinapsis. Con las células líquidas vamos a **dejar de inventar neuronas** y quedarnos con lo único que dio positivo: la memoria compacta de DBC3. Lo medido hasta hoy dice que el cableado hace el trabajo y que la no linealidad de la célula no agrega nada en las tareas probadas.

## 1. Pedido

"EN CRIOLLO ACIA DONDE VAMOS CON EL CONECTOMA Y LAS CELULAS LIQUIDAS"

## 2. Herramientas declaradas

- Lectura GitHub en `drosophila-fep-connectome`: `docs/agents/CONTEXTO-drosophila-fep.md`, `docs/PLAN-MATERIALIZACION-2026-10-02.md`, `docs/PIVOTE-RECIPROCIDAD.md` y la respuesta 002 de hoy.
- Lectura GitHub en `mojo-absoluto`: `respuestas/2026-10-03-20-estado-proyecto-y-proximos-gates.md`, `respuestas/2026-10-01-31-decision-arquitectura-post-benchmark.md` y los cuerpos de los PR #17, #18 y #19.
- Lectura ClickUp: "Revisión integral 2026-10-06", "Por qué comparamos SparseLTC: objeto, evidencia y dirección" y "Mojo Absoluto: benchmark reproducible IQ/radar y estado de CI".
- Escritura: esta respuesta, `docs/agents/CONTEXTO-drosophila-fep.md` actualizado (estaba al 03-oct y no tenía la Tabla 7) y un Doc público en ClickUp.
- Sin brain-env, sin Kaggle, sin cuota ajena.

## 3. Qué se midió

Nada nuevo en este turno. Es una síntesis de mediciones ya commiteadas, cada una con su fuente.

**Conectoma**

- Tabla 7 reproducible (respuesta 002): reproduce la salida de marzo 16/16 y la tabla publicada 8/8. El 8,7% sensory→descending publicado es doble redondeo de 8,6488%.
- Gradiente hacia el motor, sin umbral: sensory→central 24,2; sensory→descending 8,6; sensory→motor 3,6; optic→motor 0,0 (6 aristas). Con ≥5 sinapsis: 13,8; 2,8; 1,3; optic→motor sin aristas. **El gradiente sobrevive al umbral.** Cambia la punta: intra-sensory 37,5 supera a intra-motor 35,0 (80 aristas).
- Global: 26,60% sin umbral y 13,98% con ≥5, en línea con Lin 2024: no es distintivo. El 36× era overflow int32.
- FEP: 9/12 predicciones FALSIFIED en el corpus de marzo (respuesta 001).
- H4 (el cableado predice actividad real): fuerte NO MEDIDA; generalización entre trials balanced accuracy 0,5019 con p=0,623; estabilidad temporal p=0,055 (CONTEXTO al 03-oct).

**Células líquidas (`mojo-absoluto`)**

- HC-2, PR #17: sobre FlyWire real (12 `root_id`, 12 seeds, 4 folds), SparseLTC empata con el control lineal en delayed-XOR y context-switch, 0/48 victorias y 48/48 empates. Sin estado temporal el modelo pierde (0,500 y 0,750) y con features permutadas cae a azar. El estado temporal importa; la no linealidad no ganó.
- Corpus de marzo (respuesta 001): el efecto es topológico y casi lineal (sin tanh R_vis=2,1288; 19 de 20 direcciones iguales con y sin tanh; max|h| cerca de 0,05).
- HC-3, PR #18: FAIL por techo, DBC3 1,000 contra LSTM 0,9996.
- HC-3b, PR #18: DBC3 AULC 0,823 contra 0,635 del mejor baseline; sin gate 0,829, así que la ventaja es de la celda de memoria. Una sola tarea.
- ComplexLTC: no ganó ninguna métrica principal en IQ/radar; queda experimental y congelada (ADR 2026-10-01).
- Piloto FlyWire→SparseLTC→DBC3 sobre 90 raíces: 90,00 / 91,11 / 90,00%. Valida la cañería, no conducta.

## 4. Evidencia cruda (verbatim, copiada de las fuentes)

PR #17, cuerpo, `titan/hc2-sparseltc-acceptance-2026-10-03`:

```text
delayed-XOR:
  SparseLTC:       1.000 ± 0.000
  linear control:  1.000 ± 0.000
  stateless input: 0.500 ± 0.000
  permuted nulls:  ~0.51

context-switch:
  SparseLTC:       1.000 ± 0.000
  linear control:  1.000 ± 0.000
  stateless input: 0.750 ± 0.000
  permuted nulls:  ~0.50
```

PR #18, cuerpo, `titan/hc3-dbc3-selective-memory-2026-10-04`:

```text
- AULC: DBC3 0.823 contra 0.635 del mejor baseline (`linear_recurrent@3e-3`). Δ = −0.188, IC 95% [−0.200, −0.177]. Null 0.516, stateless 0.490.
- `dbc3_no_gate` 0.829: la ventaja es de la celda de memoria, no del gate.
- **NO MEDIDO:** LSTM y GRU eligieron el LR del borde (1e-2); falta un chequeo post-hoc con 3e-2 y 1e-1.
3 seeds × 4 folds × 120 épocas: DBC3 1.000, LSTM 0.9996, IC del Δ [−0.0013, 0.0000]. Controles en azar.
```

PR #19, cuerpo, addendum `f214c8d`:

```text
- El DBC3 de HC-3 no inicializa como el `DBC3Motor` canónico (GELU exacta, init default, sesgo de tau default): tau inicial medido 0.4969 contra sigmoid(-2) = 0.119. Parámetros iguales (6318); GRU +2,6% y LSTM +6,2%.
```

`mojo-absoluto/respuestas/2026-10-01-31-decision-arquitectura-post-benchmark.md`:

```text
El benchmark usó 2048 muestras, tres escenarios, ruido IQ a 10 dB y seed `5572435191199257156`. `ComplexVectorLTC` no ganó ninguna métrica principal.
```

Respuesta 002, `run.log` de la Tabla 7 con anotaciones de marzo:

```text
[   58.1s] global >=5: aristas=2,700,513  con_reciproca=377,448  (13.98%)  [erratum item 5: 2,700,513 y 13.98%]
[   58.1s]   T7 >=5  motor->motor                             aristas=        80  reciprocas=       28  pct=35.0%  (sin umbral 41.3%)
[   58.1s]   T7 >=5  sensory->sensory                         aristas=     1,287  reciprocas=      482  pct=37.5%  (sin umbral 30.7%)
[   58.1s]   T7 >=5  sensory->central                         aristas=    33,508  reciprocas=    4,609  pct=13.8%  (sin umbral 24.2%)
[   58.1s]   T7 >=5  sensory->descending                      aristas=     4,786  reciprocas=      136  pct=2.8%  (sin umbral 8.6%)
[   58.1s]   T7 >=5  sensory->motor                           aristas=       373  reciprocas=        5  pct=1.3%  (sin umbral 3.6%)
[   58.1s]   T7 >=5  optic->motor                             aristas=         0  reciprocas=        0  pct=nan%  (sin umbral 0.0%)
```

`docs/PIVOTE-RECIPROCIDAD.md`, la frase que este gradiente sostiene:

```text
The ordering is specific: **reciprocity decreases as connections approach the motor output**
```

## 5. Archivos generados

- Esta respuesta.
- `docs/agents/CONTEXTO-drosophila-fep.md`, reescrito al 10-oct con la Tabla 7 y el orden de próximos pasos.
- Doc ClickUp: https://app.clickup.com/90171457413/docs/2kza6fw5-20837

## 6. NO MEDIDO

1. Nulo por circuito y test de tendencia de la Tabla 7. Sin eso, "decrece hacia el motor" es descriptivo (`docs/PIVOTE-RECIPROCIDAD.md` §E.3 y §E.4).
2. Cruce con la reciprocidad por neuropilo de Lin 2024 (§E.1 y §E.5).
3. HC-3b con LR 3e-2 y 1e-1 para LSTM/GRU, y si su DBC3 inicializa como el `DBC3Motor` canónico: la auditoría del PR #19 encontró que el de HC-3 no.
4. La no linealidad en una tarea no saturada y preregistrada.
5. H4 fuerte, conducta, causalidad, edge físico y producto.
6. Las `results/` de la Tabla 7 siguen sólo en el commit local `7117e45` de brain-env.

## Lectura propia (opinión, no medición)

El orden que propongo, con el criterio de cerrar lo que ya tiene resultado antes de abrir algo nuevo:

1. **Paper:** nulo por circuito y test de tendencia sobre la Tabla 7 en brain-env, con `src/cp40.py` y `tools/table7_reciprocity_by_class.py`. Después, la v2 del erratum (ítem 9 y el 8,6), que decide Abraham. Y no se toca más el paper.
2. **DBC3:** cerrar los dos NO MEDIDO de HC-3b. Si la ventaja sobrevive, ese es el resultado de las células líquidas.
3. **No linealidad:** una sola tarea preregistrada no saturada. Si vuelve a empatar, se usa la dinámica lineal y se retira la claim.
4. **Unificar** los PR #17 y #18 en una rama integrada antes de agregar arquitectura (P0 del PR #19).
5. **Estacionado:** ComplexLTC y H4.

Esta línea no paga directo: da credibilidad (paper corregido, repos reproducibles). La prioridad de ingresos de la revisión del 6-oct no cambia.

--- METODO PROMETEO ---
Máquina: ninguna en este turno; la Tabla 7 corrió en brain-env (respuesta 002).
Artefactos: este archivo + Doc https://app.clickup.com/90171457413/docs/2kza6fw5-20837
