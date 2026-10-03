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

## Veredicto

**NO EVIDENCIA DE GENERALIZACIÓN ENTRE TRIALS** dentro de este animal. Esto no refuta H4 fuerte: mide decodificación entre sesiones, no selección anatómica ni causalidad. H4 fuerte permanece **NO MEDIDA**.
