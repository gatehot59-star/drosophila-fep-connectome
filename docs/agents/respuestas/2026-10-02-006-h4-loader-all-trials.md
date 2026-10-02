# Recibo 006: loader oficial H4, ocho trials

## 1. Pedido

Escalar el loader oficial después de que el trial 7 pasara el alignment gate, sin interpretar todavía la biología.

## 2. Herramientas y máquina

- MUDH Gateway `build.run` en `brain-env` persistente.
- `tools/h4_official_loader.py` ejecutado secuencialmente sobre los ocho pares H5/capture/DFF/behavior.
- Cada proceso usó `PYTHONDONTWRITEBYTECODE=1` y `subprocess.run`; no se usó `$?` del shell.
- No se gastó Kaggle, Actions ni runtime ajeno.

## 3. Qué se midió

Resultado aggregate versionado en `results/h4_all_trials_manifest_summary.json`:

```text
schema=h4-all-trials-summary/v1
animal=R65D11-tdTomGC6fopt-fly1
n_trials=8
n_success=8
all_verdicts=BIEN
join_key=Time
timebase=thor_sync_seconds
```

Resumen por trial:

| trial | Basler | cámara | 2P | labels | ROI | error duración | cobertura neural | manifest SHA-256 |
|---:|---:|---:|---:|---:|---:|---:|---:|---|
| 1 | 7469 | 7440 | 1067 | 7440 | 2 | 0.0030348454 | 0.9969650205 | `f3cb556b9683a1158c626ea205decbf1b1fecee4ef6845dd748e8fa13c7a0345` |
| 2 | 7470 | 7440 | 1067 | 7440 | 2 | 0.0030377950 | 0.9969620709 | `479a404071547ab99e448db9b020d8188be7a8d1b12cf977be8b4451861ed018` |
| 3 | 7469 | 7440 | 1067 | 7440 | 2 | 0.0029931551 | 0.9970068449 | `1d6f030d0db053c33d3d14360f5e0472ad7f71c4db474239d851855e1c81c32c` |
| 4 | 7469 | 7440 | 1067 | 7440 | 2 | 0.0029885976 | 0.9970114024 | `9b9ed50c5011aad86ee5c4d01a06706f68178ce271e4d9509319c20ce3fe89de` |
| 5 | 7469 | 7440 | 1067 | 7440 | 2 | 0.0029859162 | 0.9970140838 | `bf7a0d6bd2953f0e4988b55328838fa98d97b8280e839e5f5aa722788bb72a5b` |
| 6 | 7469 | 7440 | 1067 | 7440 | 2 | 0.0029889994 | 0.9970110006 | `8e41342730d4b64ba50a7fc6be5aa0a525642904549b46add9285369f27d07d4` |
| 7 | 7469 | 7440 | 1067 | 7440 | 2 | 0.0029898041 | 0.9970101959 | `a5142a7b3271d71cc812ca3a60ce15614a046b522d71b56af02c9641052cb272` |
| 8 | 7469 | 7440 | 1067 | 7440 | 2 | 0.0029904740 | 0.9970095260 | `07ff3bc860ca8e0ab85ac4cb078e4d0a3b74664cf4c1c256c8f20fffd45a5087` |

Pérdidas:

- `behavior_labels_unpaired = 0` en los 8 trials.
- `roi_arrays_with_wrong_length = 0` en los 8 trials.
- Los trials 1 y 2 tienen 1 frame conductual antes del solapamiento y 4 neurales después.
- Los trials 3 a 8 tienen 1 frame neural antes y 4 después, sin frames conductuales fuera del solapamiento.

## 4. Qué significa

El alignment gate ya no es solo una prueba sintética: pasa sobre los ocho assets reales disponibles. El instrumento común encuentra el mismo patrón temporal, con error de duración entre `0.0029859` y `0.0030378`, y cobertura neural entre `0.9969621` y `0.9970141`.

Esto habilita el siguiente bloque: construir features conservando identidad ROI/anatomía y repetir el análisis por bouts/trials con nulls de bloques. **No habilita todavía una conclusión sobre H4.**

## 5. NO MEDIDO

- Rerun biológico cross-animal/temporal.
- Features ROI→cell type/neuropilo.
- Null por bloques temporales.
- Null anatómico pareado.
- SparseLTC sobre subgrafos observados.
- Silenciamiento causal.
- H4 fuerte como fenómeno biológico.
- Merge humano del PR #8 y de su base PR #7.

--- METODO PROMETEO ---
Accion delicada: NO
Modo aplicado: FULL
Maquina: brain-env para ocho mediciones; Actions x64 para contratos
Rubrica: N/A (instrumento + evidencia, sin deployment)
N/A declarados: causalidad, seguridad de producto y deployment no aplican
Review externo: pendiente; silencio no es aprobación
Instrumento: loader oficial con `subprocess.run`, manifests SHA-256 y resumen agregado versionado
Artefactos: `results/h4_all_trials_manifest_summary.json` + este recibo + manifests completos persistentes en brain-env
