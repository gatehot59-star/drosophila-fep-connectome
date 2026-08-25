# Evidencia cruda · null de signo y de topología sobre `sel_post`

**Corrida:** 2026-08-25 10:46 UTC en adelante
**Instrumento:** `src/signshuffle_selpost.py`, md5 `5a292cbc4f0a6b2d445405ad5c86ad80`

```
python3 signshuffle_selpost.py \
  --conn /workspace/connectivity.parquet --ann /workspace/annotations.tsv \
  --spreads 1 8 30 --nulls 40 --out /tmp/run/signshuffle.json
```

**Tres ensembles × tres spreads × 40 realizaciones**, semillas `1000 + 7i`. Los tres ensembles existen porque **uno solo no separa las dos causas candidatas**:

| Ensemble | Qué permuta | Qué conserva |
|---|---|---|
| **SIGN** | la asignación excitatorio/inhibitorio entre aristas | el multiconjunto de signos **y todos los pesos** |
| **TOPO** | los pesos entre aristas | **el patrón de signos** de cada arista |
| **BOTH** | signo y peso juntos | solo el conteo de aristas |

Y el sign-shuffle se corre **a cada spread de tau**, que era el modo de falla 5 declarado en la resp 070: la comparación ya nunca mezcla condiciones.

---

## 1. Setup y guards, verbatim

```
nodes 864 edges 45687 driven 293 target 2
GUARD energies {"looming": 20.5027777778, "receding": 20.5027777778, "constant": 20.5027777778}
GUARD matched: MATCHED_OK
```

---

## 2. Los valores observados, verbatim

```
OBSERVED spread=1  {"sel_peak": 1.0631, "sel_post": 4.3287, "post_looming": 2.7742}
OBSERVED spread=8  {"sel_peak": 1.1142, "sel_post": 5.2563, "post_looming": 1.9645}
OBSERVED spread=30 {"sel_peak": 1.1684, "sel_post": 5.4134, "post_looming": 1.6226}
```

**⚠️ `spread=1` reproduce 1,0631 y 4,3287 exactos**, los valores de las dos corridas anteriores, con un tercer código distinto. **Control cruzado en verde.**

---

## 3. 🔥 Los resultados, verbatim y sin recortar

```
RESULT spread_1_SIGN {"sel_peak": {"observed": 1.0631, "null_mean": 1.1154, "null_sd": 0.0169, "null_min": 1.0598, "null_max": 1.1413, "nulls_ge_observed": 39, "nulls_le_observed": 1, "ratio": 0.9531, "z": -3.09, "sd_zero_reason": null}, "sel_post": {"observed": 4.3287, "null_mean": 1.9101, "null_sd": 0.3242, "null_min": 1.2162, "null_max": 2.6086, "nulls_ge_observed": 0, "nulls_le_observed": 40, "ratio": 2.2662, "z": 7.46, "sd_zero_reason": null}, "post_looming": {"observed": 2.7742, "null_mean": 3.9799, "null_sd": 2.9746, "null_min": 1.3077, "null_max": 14.648, "nulls_ge_observed": 20, "nulls_le_observed": 20, "ratio": 0.697, "z": -0.41, "sd_zero_reason": null}}

RESULT spread_1_TOPO {"sel_peak": {"observed": 1.0631, "null_mean": 1.0749, "null_sd": 0.0052, "null_min": 1.0667, "null_max": 1.0867, "nulls_ge_observed": 40, "nulls_le_observed": 0, "ratio": 0.9891, "z": -2.26, "sd_zero_reason": null}, "sel_post": {"observed": 4.3287, "null_mean": 1.1896, "null_sd": 0.0173, "null_min": 1.164, "null_max": 1.2539, "nulls_ge_observed": 0, "nulls_le_observed": 40, "ratio": 3.6387, "z": 181.38, "sd_zero_reason": null}, "post_looming": {"observed": 2.7742, "null_mean": 16.0933, "null_sd": 2.2477, "null_min": 9.8533, "null_max": 21.7608, "nulls_ge_observed": 40, "nulls_le_observed": 0, "ratio": 0.1724, "z": -5.93, "sd_zero_reason": null}}

RESULT spread_1_BOTH {"sel_peak": {"observed": 1.0631, "null_mean": 1.0931, "null_sd": 0.0576, "null_min": 0.9391, "null_max": 1.3029, "nulls_ge_observed": 30, "nulls_le_observed": 10, "ratio": 0.9726, "z": -0.52, "sd_zero_reason": null}, "sel_post": {"observed": 4.3287, "null_mean": 1.739, "null_sd": 0.3783, "null_min": 1.1972, "null_max": 2.9038, "nulls_ge_observed": 0, "nulls_le_observed": 40, "ratio": 2.4891, "z": 6.84, "sd_zero_reason": null}, "post_looming": {"observed": 2.7742, "null_mean": 5.6581, "null_sd": 3.19, "null_min": 0.8583, "null_max": 14.7506, "nulls_ge_observed": 32, "nulls_le_observed": 8, "ratio": 0.4903, "z": -0.9, "sd_zero_reason": null}}

RESULT spread_8_SIGN {"sel_peak": {"observed": 1.1142, "null_mean": 1.1535, "null_sd": 0.0226, "null_min": 1.1046, "null_max": 1.2162, "nulls_ge_observed": 37, "nulls_le_observed": 3, "ratio": 0.966, "z": -1.74, "sd_zero_reason": null}, "sel_post": {"observed": 5.2563, "null_mean": 1.8532, "null_sd": 0.3396, "null_min": 1.1913, "null_max": 2.6319, "nulls_ge_observed": 0, "nulls_le_observed": 40, "ratio": 2.8364, "z": 10.02, "sd_zero_reason": null}, "post_looming": {"observed": 1.9645, "null_mean": 3.7672, "null_sd": 2.9011, "null_min": 1.0565, "null_max": 14.077, "nulls_ge_observed": 31, "nulls_le_observed": 9, "ratio": 0.5215, "z": -0.62, "sd_zero_reason": null}}

RESULT spread_8_TOPO {"sel_peak": {"observed": 1.1142, "null_mean": 1.1005, "null_sd": 0.0079, "null_min": 1.0881, "null_max": 1.1246, "nulls_ge_observed": 2, "nulls_le_observed": 38, "ratio": 1.0125, "z": 1.75, "sd_zero_reason": null}, "sel_post": {"observed": 5.2563, "null_mean": 1.1648, "null_sd": 0.0152, "null_min": 1.1447, "null_max": 1.2228, "nulls_ge_observed": 0, "nulls_le_observed": 40, "ratio": 4.5128, "z": 269.35, "sd_zero_reason": null}, "post_looming": {"observed": 1.9645, "null_mean": 15.8959, "null_sd": 2.2479, "null_min": 9.6815, "null_max": 21.6731, "nulls_ge_observed": 40, "nulls_le_observed": 0, "ratio": 0.1236, "z": -6.2, "sd_zero_reason": null}}

RESULT spread_8_BOTH {"sel_peak": {"observed": 1.1142, "null_mean": 1.1173, "null_sd": 0.0727, "null_min": 0.8838, "null_max": 1.2719, "nulls_ge_observed": 24, "nulls_le_observed": 16, "ratio": 0.9972, "z": -0.04, "sd_zero_reason": null}, "sel_post": {"observed": 5.2563, "null_mean": 1.6764, "null_sd": 0.3663, "null_min": 0.9609, "null_max": 2.8428, "nulls_ge_observed": 0, "nulls_le_observed": 40, "ratio": 3.1354, "z": 9.77, "sd_zero_reason": null}, "post_looming": {"observed": 1.9645, "null_mean": 5.405, "null_sd": 3.2249, "null_min": 0.8144, "null_max": 14.8343, "nulls_ge_observed": 34, "nulls_le_observed": 6, "ratio": 0.3635, "z": -1.07, "sd_zero_reason": null}}

RESULT spread_30_SIGN {"sel_peak": {"observed": 1.1684, "null_mean": 1.1916, "null_sd": 0.0267, "null_min": 1.137, "null_max": 1.2632, "nulls_ge_observed": 33, "nulls_le_observed": 7, "ratio": 0.9805, "z": -0.87, "sd_zero_reason": null}, "sel_post": {"observed": 5.4134, "null_mean": 1.6696, "null_sd": 0.2729, "null_min": 1.1459, "null_max": 2.3927, "nulls_ge_observed": 0, "nulls_le_observed": 40, "ratio": 3.2423, "z": 13.72, "sd_zero_reason": null}, "post_looming": {"observed": 1.6226, "null_mean": 3.6784, "null_sd": 2.7672, "null_min": 0.9774, "null_max": 13.1117, "nulls_ge_observed": 34, "nulls_le_observed": 6, "ratio": 0.4411, "z": -0.74, "sd_zero_reason": null}}
```

---

## 4. La tabla del veredicto

### `sel_post` · **0 de 40 en las 7 configuraciones**

| Configuración | Observado | Null ± sd | Ratio | z | nulls ≥ real |
|---|---|---|---|---|---|
| spread 1 · SIGN | 4,3287 | 1,9101 ± 0,3242 | **2,27×** | **+7,46** | **0/40** |
| spread 1 · TOPO | 4,3287 | 1,1896 ± 0,0173 | **3,64×** | **+181,4** | **0/40** |
| spread 1 · BOTH | 4,3287 | 1,7390 ± 0,3783 | **2,49×** | **+6,84** | **0/40** |
| spread 8 · SIGN | 5,2563 | 1,8532 ± 0,3396 | **2,84×** | **+10,02** | **0/40** |
| spread 8 · TOPO | 5,2563 | 1,1648 ± 0,0152 | **4,51×** | **+269,4** | **0/40** |
| spread 8 · BOTH | 5,2563 | 1,6764 ± 0,3663 | **3,14×** | **+9,77** | **0/40** |
| spread 30 · SIGN | 5,4134 | 1,6696 ± 0,2729 | **3,24×** | **+13,72** | **0/40** |

### `sel_peak` · en el mismo circuito y la misma corrida

| Configuración | Observado | Null ± sd | z | nulls ≥ real |
|---|---|---|---|---|
| spread 1 · SIGN | 1,0631 | 1,1154 ± 0,0169 | **−3,09** | 39/40 |
| spread 1 · TOPO | 1,0631 | 1,0749 ± 0,0052 | **−2,26** | **40/40** |
| spread 1 · BOTH | 1,0631 | 1,0931 ± 0,0576 | −0,52 | 30/40 |
| spread 8 · SIGN | 1,1142 | 1,1535 ± 0,0226 | −1,74 | 37/40 |
| spread 8 · TOPO | 1,1142 | 1,1005 ± 0,0079 | +1,75 | 2/40 |
| spread 8 · BOTH | 1,1142 | 1,1173 ± 0,0727 | −0,04 | 24/40 |
| spread 30 · SIGN | 1,1684 | 1,1916 ± 0,0267 | −0,87 | 33/40 |

**El contraste es el resultado: `sel_post` por encima de su null en 7 de 7, `sel_peak` en o por debajo del suyo en 6 de 7.** Las dos métricas, el mismo circuito, la misma corrida, el mismo ensemble.

---

## 5. 🆕 El hallazgo lateral, que no buscaba y explica el mecanismo

`post_looming` es la **actividad post-estímulo absoluta**, no el cociente:

| Configuración | Observado | Null TOPO | nulls ≥ real |
|---|---|---|---|
| spread 1 · TOPO | **2,7742** | **16,0933 ± 2,2477** | **40/40** (z = −5,93) |
| spread 8 · TOPO | **1,9645** | **15,8959 ± 2,2479** | **40/40** (z = −6,20) |

**El circuito real tiene 5,8 veces MENOS actividad post-estímulo total que un circuito con los mismos signos y los pesos barajados, y al mismo tiempo 3,6 veces MÁS selectividad post-estímulo.**

> **No es que el circuito real resuene más tiempo. Resuena MENOS, y lo poco que resuena depende mucho más del perfil temporal del estímulo.**

Eso es una afirmación mecánica y no una metáfora: la topología real **suprime** la reverberación genérica y **preserva** la diferencial.

---

## 6. Defectos declarados de esta corrida

1. **🔴 Faltan 2 de 9 configuraciones:** `spread_30_TOPO` y `spread_30_BOTH` no habían cerrado al commitear. **Las 7 completas son unánimes, pero «faltan dos» es un estado y hay que decirlo.**
2. **Los puntos de spread 8 y 30 usan UN solo sorteo de tau** (semilla 4242), no el promedio de 20 del barrido anterior. **Por eso el 5,2563 de spread 8 no es comparable con el 3,5189 que reportó el barrido:** ese era una media de 20 sorteos y este es un sorteo. **Comparar los dos sería el modo de falla 5 otra vez.**
3. **El null de topología permuta pesos entre TODAS las aristas**, así que no preserva el grado ni el peso total por neurona. Es un control **suelto**, y sin embargo es el que da el z más grande.
4. **Ningún ensemble preserva la estructura de módulos ni los neuropilos.** Este es un experimento de dinámica, no de anatomía, y no hereda el control anatómico del resto del repo.
5. **La ventana sigue sin barrer:** `sel_post` integra del paso 80 al 200 y esa elección es mía. **Es el claim C-08c de la orden de Tao y sigue abierto.**
6. **Solo se estimula LC4+LPLC2**, escalar, sin campo receptivo espacial ni entrada multimodal, cuando la entrada 01 dice que el circuito es 67,6% central.
7. **`tau` real, no compleja.** El motor usa `Im(tau)`, banco de osciladores, y **eso es justamente lo que más podría afectar una métrica de resonancia post-estímulo.** Sin barrer.
8. **La métrica es el promedio de las 2 neuronas blanco.** Sin umbral de disparo, que es lo que decide un escape real.
