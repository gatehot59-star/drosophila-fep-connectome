# Validación cross-animal antes de interpretar H4

## Pedido
Run cross-animal validation before interpreting H4.

## Diseño ejecutado
Usé el dataset público `Brain_only_GAL4_population_data` de Aymanns, que contiene cinco animales. Descargué un trial emparejado de cada uno: conducta `behaviour_predictions_daart.pkl` y `roi_dFF_2p.pkl`. Las cantidades de ROIs difieren por animal, así que no forcé una identidad ROI inexistente: construí nueve estadísticas por frame de la población neural (`mean`, `std`, `min`, `max`, `median`, `q10`, `q25`, `q75`, `q90`). Usé solo DFF `denoised`, cada décimo frame, y dejé un animal completo fuera del entrenamiento en cada ronda.

El modelo es LogisticRegression balanceado dentro de StandardScaler. La métrica es balanced accuracy, comparada contra diez barajados de etiquetas en el conjunto de entrenamiento para cada animal retenido.

## Evidencia cruda verbatim
```text
bytes 3917 md5 0f890523f6c4ef2f31cbe0db5d1f1c03
mean 0.18160032857235914 shuffle 0.20188559029418066
[('Fly1', 0.20459553800016472, 0.19688674461394715),
 ('Fly2', 0.16029976187870926, 0.1936440764072343),
 ('Fly3', 0.19061189699789727, 0.19992507286565647),
 ('Fly4', 0.19608884596813134, 0.20742746202642565),
 ('Fly5', 0.15640560001689296, 0.21154459555763983)]
```

Balanced accuracy de referencia para cinco clases es aproximadamente `0,20`. El promedio real quedó `0,1816`, por debajo del shuffle `0,2019`; solo Fly1 supera su shuffle local (`0,2046` vs `0,1969`).

## Veredicto
La representación resumida de población neural **no generaliza entre animales** en este test. Por lo tanto, no es válido interpretar el resultado anterior de los 8 trials de un solo fly como una propiedad H4 general de la especie.

Esto **no refuta H4 biológica**. El instrumento cross-animal deliberadamente colapsó ROIs a nueve estadísticas porque los identificadores ROI no son comparables entre animales. Antes de una conclusión biológica todavía hace falta una alineación anatómica común, por ejemplo mapping de ROIs/cell types a FlyWire, o una representación de población validada contra ese mapping. H4 fuerte queda NO MEDIDA.

## Consecuencia práctica
El resultado anterior `co2_off delta=0,01434` queda como señal intra-animal descriptiva, no evidencia generalizable. La próxima corrida debe mapear identidades, repetir leave-one-fly-out con features anatómicamente comparables y recién después contrastar rutas reales contra null anatómico y silenciamientos.

## Archivos
- Runner: `tools/h4_cross_animal.py`, commit `3793a6ed20ddc4b7dcda81b41e4b7ebd21d53f85`.
- Resultado local: `/workspace/h4_data/bo_cross/cross_animal.json`, 3.917 bytes, md5 `0f890523f6c4ef2f31cbe0db5d1f1c03`.
- Este recibo.

--- METODO TITAN ---
Accion delicada: NO
Modo aplicado: TITAN FULL
Rubrica: N/A (validacion cientifica)
N/A declarados: deployment/security/CI no aplican; mapping anatómico y causalidad quedan NO MEDIDOS
Review externo: no pedido
Instrumento: MUDH Gateway build.run; 5 animales, 5 behavior, 5 DFF; JSON y md5 arriba
