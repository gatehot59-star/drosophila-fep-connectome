# Recibo 012: generalización H4 entre trials dentro de un animal

## Pedido

Continuar con los bloqueos restantes de H4 usando las features alineadas, sin volver a unir por `Frame` y sin llamar cross-animal a los ocho trials.

## Medición

Se ejecutó leave-one-trial-out con nearest-centroid sobre medias por bout de `ROI_0`/`ROI_1`, usando `walking` y `resting`, en `co2_off`, 999 permutaciones.

```text
animal=R65D11-tdTomGC6fopt-fly1
n_trials=8
scope=within_animal_leave_one_trial_out
observed_balanced_accuracy=0.5018855395873556
null_mean=0.5081554609448383
null_sd=0.02091634629331271
p_greater_equal=0.623
z=-0.2997617877213725
```

Folds observados: `0.4571, 0.4167, 0.4710, 0.5315, 0.5747, 0.5670, 0.5625, 0.4346`; ninguno supera su null one-sided.

## Veredicto

La representación ROI no mostró generalización leave-one-trial-out por encima del null bloqueado dentro de este animal. Esto **no refuta H4 fuerte**: mide decodificación entre sesiones, no selección anatómica ni causalidad. El resultado anterior queda como **NO EVIDENCIA DE GENERALIZACIÓN ENTRE TRIALS**, no como inestabilidad cross-animal.

H4 fuerte permanece **NO MEDIDA**.

## NO MEDIDO

- Estabilidad temporal por mitades con bouts completos.
- Mapping ROI→cell type/FlyWire/neuropilo.
- Null anatómico pareado.
- Silenciamiento causal y SparseLTC sobre subgrafos.
- Publicación de los 999 scores pooled exactos, aunque ya están calculados y hasheados en brain-env.

--- METODO PROMETEO ---
Accion delicada: NO
Modo aplicado: FULL
Maquina: brain-env para la corrida; GitHub MCP para publicación
Rubrica: N/A (instrumento descriptivo, no deployment)
N/A declarados: mapping anatómico, causalidad y publicación binaria completa quedan fuera de este bloque
Review externo: pendiente; silencio no es aprobación
Instrumento: Python stdlib, 4 tests nuevos + 5 contratos base, 999 permutaciones; comando y exit code en `results/h4_trial_generalization_run.log`
Artefactos: `tools/h4_trial_generalization.py` + `tests/test_h4_trial_generalization.py` + `results/h4_trial_generalization_summary.json` + `docs/agents/respuestas/2026-10-02-012-h4-trial-generalization.md`