# Recibo 008: features H4 alineadas, ocho trials

## 1. Pedido

Continuar la materialización después del trial 7: ejecutar el materializador ROI/contexto/bouts sobre los otros siete trials y cerrar el bloque con pérdidas explícitas.

## 2. Herramientas y máquina

- MUDH Gateway `build.run` en `brain-env` persistente.
- `tools/h4_aligned_features.py` desde la rama `titan/h4-aligned-features-2026-10-02`.
- `subprocess.run`, `PYTHONDONTWRITEBYTECODE=1`; no se aceptaron estados del shell como exit code.
- No se usó Kaggle, Actions fuera del check del PR ni runtime ajeno.

## 3. Resultado aggregate

```text
schema=h4-aligned-features-all-trials/v1
animal=R65D11-tdTomGC6fopt-fly1
n_trials=8
n_success=8
all_verdicts=BIEN
ROI=ROI_0, ROI_1
```

| trial | registros | bouts | frames de conducta descartados por fuera de cobertura | JSONL SHA-256 |
|---:|---:|---:|---:|---|
| 1 | 7.439 | 69 | 1 | `9a49e3868b09e002519f8e9d90470589ad5c095cf3d51d1d3dafed645a55f6de` |
| 2 | 7.439 | 70 | 1 | `0167afad445b81899871c7222ddc0531195aad9432c8cc988a9e2c9d1b52246e` |
| 3 | 7.440 | 82 | 0 | `4a979cac64fccbbe9a2137fa5629f79bd9017f84834a0cec103e29f5a35d80f6` |
| 4 | 7.440 | 89 | 0 | `a4fdcb20ced75b06576672daf0085a830d5ad4fe0e20f34286c39a93432c4b49` |
| 5 | 7.440 | 94 | 0 | `06b47ddc84091f520dd517f8d1d7e9e4836df71836cd1d65f5c35fd4c526a68f` |
| 6 | 7.440 | 96 | 0 | `5f2381b78c01bd0c07c9139cab8f3af2e09daa621c0699d00223b443d07914c0` |
| 7 | 7.440 | 102 | 0 | `32f06e564f4fc723df846d420bf8eb77f68190aafb04600a334cc385152672e9` |
| 8 | 7.440 | 106 | 0 | `1adba72ce248e7866eaffbe6733a03ca54f0a265214e14ef68bbcef6b19ed1cd` |

Todos los trials conservaron dos ROI, contexto CO2 reconstruido en el reloj común y bouts por cambios de label/contexto. En trials 1 y 2 se descartó explícitamente un frame conductual fuera de cobertura neural; no se extrapoló.

## 4. Corrección durante la medición

El primer barrido detectó un defecto del contrato: el summary no llevaba `verdict`, y el proceso se detuvo en trial 3. Se corrigió el contrato y se relanzó. Luego apareció el caso real de borde en trials 1 y 2; el materializador se cambió a `overlap_indices` y registró la pérdida en lugar de inventar una extrapolación. El rerun final dio 7/7 nuevos trials y 8/8 aggregate.

## 5. Qué significa

Ahora todo el dataset Aymanns disponible para este animal tiene una representación alineada que conserva ROI y bloques temporales. Esto habilita el rerun por bouts/trials y nulls bloqueados. **No demuestra H4 fuerte.**

## 6. NO MEDIDO

- Nulls por bloques ya ejecutados.
- Rerun cross-animal/temporal con las features válidas.
- Mapping ROI→FlyWire/cell type/neuropilo.
- Null anatómico pareado.
- SparseLTC sobre subgrafos observados.
- Silenciamiento causal.
- H4 fuerte.

--- METODO PROMETEO ---
Accion delicada: NO
Modo aplicado: FULL
Maquina: brain-env para ocho trials; Actions x64 para contratos
Rubrica: N/A (instrumento + resultados derivados, sin deployment)
N/A declarados: causalidad, mapping anatómico y producto final no aplican a este bloque
Review externo: pendiente; silencio no es aprobación
Instrumento: contrato unittest, materializador real vía subprocess y SHA-256 de cada JSONL
Artefactos: `results/h4_aligned_features_all_trials_summary.json` + este recibo + JSONL derivados persistentes en brain-env
