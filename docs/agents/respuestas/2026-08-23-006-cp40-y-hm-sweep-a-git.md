# resp 006 · cp40.py y hm_sweep.py a git, y un punto fuera de presupuesto que nadie había visto

**Fecha:** 2026-08-23 21:07–21:25 (America/Buenos_Aires) · **Modo:** TITAN FULL · **Tipo:** entrega de código + evidencia

## 1. Pedido

> «Seguí con cp40.py y hm_sweep.py»

## 2. Herramientas declaradas (C-03)

- GitHub: lectura de `docs/agents/` y `src/` (paso 1 del lazo), y **un commit** con 5 archivos.
- `build.run`: lectura de `/workspace` (`sed`, `cat`, `md5sum`). Solo lectura.
- Cero Kaggle, cero kernels, cero cuota de cómputo ajeno.

## 3. Qué se subió

| Archivo | Líneas | md5 | Qué respalda |
|---|---|---|---|
| `src/cp40.py` | 283 | `11ca727ca266e3d91c504872304850d0` | los 40 nulls **community-preserving**: reciprocidad 20,6× (0/40), KC→MBON, DAN→KC, acceso motor |
| `src/hm_sweep.py` | 420 | `4131462d21475e85773cd6c0504f5685` | el barrido que encontró el **óptimo interior** en h_m=10 |
| `results/hm_sweep.log` | — | — | evidencia cruda verbatim del barrido (W-01) |

`cp40.py` es el archivo que cierra el hueco declarado desde ayer: reciprocidad y el circuito de aprendizaje estaban testeados **solo** contra nulls que preservan grado (Maslov-Sneppen). Este los testea contra nulls que preservan grado **y** modularidad, y además trae los valores MS hardcodeados para que las dos familias queden lado a lado en la misma tabla. Declara su propia limitación en el docstring: **el CP sí puede crear multi-aristas**, y las cuenta por null en vez de esconderlas.

## 4. HALLAZGO NUEVO: el punto h_m=16 no está pareado en presupuesto

Al commitear el log crudo y leer la **columna de parámetros**, que en mis reportes anteriores nunca cité, aparece esto:

| h_m | h_r | params | MSE | vs LSTM |
|---|---|---|---|---|
| 5 | 30 | 1401 | 0,000326 | 4,05× ← el publicado |
| 6 | 29 | 1424 | 0,000194 | 2,41× |
| 8 | 25 | 1368 | 0,000104 | 1,29× |
| 10 | 22 | 1427 | 0,000095 | **1,18× óptimo** |
| 13 | 13 | 1379 | 0,000131 | 1,62× |
| 16 | **6** | **1593** | 0,000183 | 2,27× |

Cinco puntos caen entre **1368 y 1427**, o sea dentro de ±2% del objetivo de 1400. **El sexto da 1593: un 13,8% por encima.** La causa está en el código, medida y no supuesta: `hr_for_hm` busca `h_r` en `range(6, 60)`, y con `h_m=16` **ni el mínimo de la grilla alcanza para bajar a 1400**. `h_r=6` está pegado al borde del rango.

**Qué le hace esto al resultado, en las dos direcciones:**

- **Lo refuerza:** el punto h_m=16 tiene **más parámetros** que todos los demás y rinde **peor** (2,27×). Si el problema fuera falta de capacidad, ese punto debería ganar. El óptimo interior no es un artefacto de presupuesto.
- **Lo debilita como comparación:** ese punto **no es parejo en parámetros**, así que su número no puede citarse en la misma tabla sin la aclaración. La curva sigue siendo no monótona con los cinco puntos limpios (5, 6, 8, 10, 13), que ya bastan para el argumento.

**Corrección al claim guardado:** el óptimo en h_m=10 y la mejora de 3,44× (`p = 8,59×10⁻¹⁰`) siguen en pie sobre puntos pareados. **La forma de la curva después de h_m=13 tiene un punto no pareado y hay que decirlo en el paper.**

## 5. Evidencia cruda (W-01)

```
$ md5sum cp40.py hm_sweep.py
11ca727ca266e3d91c504872304850d0  cp40.py
4131462d21475e85773cd6c0504f5685  hm_sweep.py

$ grep -n 'range(6, 60)' hm_sweep.py     # el limite que causa el desvio
def hr_for_hm(ind, outd, hm, target):
    best_hr, best_d, best_p = 8, 999999999, 0
    for hr in range(6, 60):

$ tail results/hm_sweep.log
  mejor punto: h_m=10  h_r=22  MSE=0.000095  vs LSTM=1.18x
  mejora contra el punto original: 3.44x
  Welch h_m=5 contra h_m=10: t=6.13  p=8.59e-10
  HIPOTESIS REFUTADA: ni con h_m=10 DualBrain alcanza al LSTM en MultiCue.
FIN  minutos=51.6
```

El log completo, verbatim, está en `results/hm_sweep.log`.

## 6. Archivos generados

`src/cp40.py` · `src/hm_sweep.py` · `results/hm_sweep.log` · este archivo · `docs/agents/CONTEXTO-motor.md` actualizado.

## 7. NO MEDIDO, declarado

**Estado de git: 5 de los 17 `.py` subidos, 7 pendientes, 5 descartados con criterio.**

Pendientes, por valor:

1. `n21.py` (398 líneas, 57,2 KB) — 21 nulls + test global. El más grande del corpus
2. `tres_brazos.py` (430 líneas, 17,8 KB)
3. `esp32c.py` (230 líneas, 40,2 KB) — la línea embebida C99
4. `hm_base.py` (269 líneas, 11,0 KB)
5. `paper_db.py` (478 líneas) — uno solo: `dualbrain_src.py` es byte-idéntico
6. `nulls19.py` (321) y `nulls19b.py` (308) — superados por las corridas de 40 nulls

Descartados **con criterio, no por olvido**: `dualbrain_src.py` (copia exacta), `scriptR_v1_buggy.py` (una línea de diff, documentada en resp 005), `chkmap.py`, `synchk.py`, `_t.py` (21 líneas en total, scratch sin valor de reproducibilidad).

Otros huecos: **no se corrió `cp40.py` en esta sesión**, se subió el código tal cual quedó tras su corrida del kernel; su log crudo **no está commiteado todavía** (solo el de `hm_sweep`). Sigue pendiente el log de `titan-paper-dualbrain`, `notebookceb82767da`, la hipótesis del 96% fijo sobre SparseLTC, y si el PR #1 entra en conflicto con `main`.
