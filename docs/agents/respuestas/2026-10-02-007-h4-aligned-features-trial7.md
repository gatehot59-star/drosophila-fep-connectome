# Recibo 007: features H4 alineadas, trial 7

## 1. Pedido

Materializar el siguiente bloque después de alinear los ocho trials: conservar identidad ROI, reconstruir contexto CO2 con el mismo reloj y crear bouts explícitos para nulls por bloques.

## 2. Herramientas y máquina

- GitHub API para rama, código, tests, workflow, summary y PR #9.
- MUDH Gateway `build.run` en `brain-env` para tests y trial real.
- No se usó Kaggle, Actions fuera del check del PR ni runtime ajeno.

## 3. Qué se construyó

- `tools/h4_aligned_features.py`:
  - interpola cada ROI sobre `Time` sin extrapolar;
  - conserva `ROI_0`, `ROI_1`, etc.;
  - reconstruye `co2_on/co2_off` a partir de la cámara ThorSync;
  - crea `bout_id`, posición y longitud cuando cambia label o contexto;
  - emite JSONL derivado y summary hasheable;
  - no clasifica ni interpreta H4.
- `tests/test_h4_aligned_features.py`: 6 contratos positivos/negativos.
- workflow actualizado para ejecutar 7 tests de alignment, 6 del loader y 6 de features.

## 4. Evidencia cruda

```text
ALIGNMENT_GREEN
Ran 7 tests in 0.002s
OK
LOADER_GREEN
Ran 6 tests in 0.002s
OK
FEATURES_CONTRACT_GREEN
Ran 6 tests in 0.001s
OK

trial real:
{"n_bouts": 102, "n_records": 7440, "roi_names": ["ROI_0", "ROI_1"], "verdict": "BIEN"}
RETURN_CODE=0
ALL_FEATURE_TESTS_AND_REAL_TRIAL_GREEN
```

El check limpio del PR `contracts` también terminó `success`.

## 5. Trial 7 real

Identidad: `R65D11-tdTomGC6fopt-fly1`, trial `7`, `thor_sync_seconds`, join `Time`.

```text
records=7440
bouts=102
ROI=ROI_0, ROI_1
labels=background 37, foreleg 70, head 315, hind 20, resting 2046, walking 4952
JSONL bytes=2320599
JSONL SHA-256=32f06e564f4fc723df846d420bf8eb77f68190aafb04600a334cc385152672e9
```

El resumen versionado está en `results/h4_aligned_features_trial_7_summary.json`; el JSONL completo queda persistente en brain-env y no se commitea como dataset.

## 6. Qué significa

Ahora tenemos el primer dataset derivado que no aplasta la señal a nueve estadísticas globales: conserva identidad ROI y bloques label/contexto. Eso habilita el rerun por bouts/trials y nulls temporales sin volver al merge por `Frame`.

## 7. NO MEDIDO

- H4 fuerte.
- Rerun cross-animal/temporal sobre los ocho JSONL.
- Nulls por bloques ya ejecutados.
- Mapping ROI→FlyWire/cell type/neuropilo.
- Null anatómico pareado.
- SparseLTC sobre subgrafo observado.
- Silenciamiento causal.

--- METODO PROMETEO ---
Accion delicada: NO
Modo aplicado: FULL
Maquina: brain-env para medición real; Actions x64 para CI de contratos
Rubrica: N/A (instrumento + tests, sin deployment)
N/A declarados: causalidad y mapping anatómico no aplican a este bloque
Review externo: pendiente; silencio no es aprobación
Instrumento: unittest stdlib, workflow `contracts`, subprocess del materializador real y SHA-256 del JSONL
Artefactos: `tools/h4_aligned_features.py` + `tests/test_h4_aligned_features.py` + `.github/workflows/h4-official-loader.yml` + `results/h4_aligned_features_trial_7_summary.json`
