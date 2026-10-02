# Recibo 010: distribución pooled íntegra publicada y deuda reproducible cerrada

## Pedido

Publicar la distribución íntegra del rerun H4 y cerrar la deuda reproducible declarada en el recibo 009.

## Qué se hizo

La distribución pooled completa de 999 scores quedó publicada en cuatro fragmentos ordenados, con manifiesto, hashes por parte, SHA-256 del JSON reconstruido y comando de validación. No se publicó un resumen que parezca la distribución: están los 999 valores.

## Medición publicada

```text
schema=h4-block-null-pooled-distribution/v1
animal=R65D11-tdTomGC6fopt-fly1
n_trials=8
context=co2_off
permutations=999
seed=20261002
observed=0.35831155721189717
null_mean=0.06104563938527175
null_sd=0.017371858516985278
p_greater_equal=0.001
z=17.11192372053771
```

JSON reconstruido:

```text
bytes=21930
sha256=eeca801431c440e3a0cb9ca6c3b1fc217408b662899d243ca3da65ffb937f176
```

## Evidencia cruda

El comando y `EXIT_CODE=0` están en `results/h4_block_null_run.log`. La distribución completa y sus hashes están en `results/H4_BLOCK_NULL_POOLED_MANIFEST.md` y en `results/h4_block_null_co2_off_8_trials_pooled_distribution.json.part-01` a `part-04`.

## Veredicto

**Deuda reproducible cerrada para el estadístico pooled reportado.** Cualquiera puede concatenar las cuatro partes, verificar el SHA y recalcular `p=0.001` desde los 999 scores.

Esto sigue siendo un resultado descriptivo dentro de un único animal y dos ROI. **H4 fuerte permanece NO MEDIDA** hasta mapping anatómico, null anatómico pareado y silenciamiento causal.

## NO MEDIDO

- Las distribuciones por trial individuales del JSON completo original no se publican en este cierre; sí está publicada la distribución pooled que sostiene el veredicto agregado.
- El workflow CI del instrumento aún no fue modificado ni ejecutado en Actions.
- El merge de los PRs sigue siendo decisión humana.

--- METODO PROMETEO ---
Accion delicada: NO
Modo aplicado: FULL
Maquina: brain-env para la medición; GitHub MCP para publicación en la rama del PR
Rubrica: N/A (publicación de evidencia, no deployment)
N/A declarados: seguridad de producto, CI de workflow, mapping anatómico y causalidad fuera de este cierre
Review externo: pendiente; silencio no es aprobación
Instrumento: `python3 -S tools/h4_block_null.py`, 5 tests, mutación negativa y 999 permutaciones; `results/h4_block_null_run.log`
Artefactos: `results/H4_BLOCK_NULL_POOLED_MANIFEST.md` + `results/h4_block_null_co2_off_8_trials_pooled_distribution.json.part-*` + este recibo
