# Estabilidad temporal dentro de cada animal

## Pedido
Medir estabilidad temporal dentro de cada animal.

## Diseño
Usé los cinco animales del dataset Brain-only. Para cada uno entrené con la primera mitad temporal y probé con la segunda (`early_to_late`), y repetí al revés (`late_to_early`). No se mezclaron frames entre mitades. Las features son las mismas nueve estadísticas de población DFF `denoised` usadas en el cross-animal; stride 10.

## Evidencia cruda verbatim
```text
bytes 3896 md5 f3eca028f56485ac69426ac66b436e52
early_late [-0.034276094276094266, 0.056899931868506226, -0.0755029996831949, 0.04574524835394403, 0.053210596609332084] mean 0.009215336574498634 sd 0.06044116776710123
late_early [-0.047944194488271974, 0.2648038475154688, 0.014278673384538976, 0.054485335636230786, -0.037759667625439475] mean 0.04957279888450543 sd 0.12721117905878546
positive_counts 3 3
```

## Veredicto
La estabilidad temporal es **débil e inconsistente** con estas features: solo 3/5 animales tienen delta positivo en cada dirección. `early_to_late` promedia `+0,0092` con SD `0,0604`; `late_to_early` promedia `+0,0496` con SD `0,1272`, dominado por Fly2 (`+0,2648`). No hay una señal robusta de representación estable.

Esto no refuta H4 biológica. Refuta la interpretación fácil de que la señal neural resumida, sin mapping anatómico, sea estable dentro de cada animal. El resultado refuerza el orden correcto: primero features anatómicamente comparables y controles temporales; después interpretar rutas o acción.

## Archivos
- Runner: `tools/h4_temporal_stability.py`, commit `0c02ff183f2cb1c65345947dd98ff2cb3de3b8e7`.
- Resultado local: `/workspace/h4_data/bo_cross/temporal_stability.json`, 3.896 bytes, md5 `f3eca028f56485ac69426ac66b436e52`.
- Este recibo.

--- METODO TITAN ---
Accion delicada: NO
Modo aplicado: TITAN FULL
Rubrica: N/A (medición científica)
N/A declarados: deployment/security/CI no aplican; mapping anatómico, causalidad y robustez con más sesiones quedan NO MEDIDOS
Review externo: no pedido
Instrumento: MUDH Gateway build.run; 5 animales, mitades cronológicas, JSON y md5 arriba
