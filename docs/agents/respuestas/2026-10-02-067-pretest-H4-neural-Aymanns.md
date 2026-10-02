# Pretest H4 con actividad neural y conducta: Aymanns

## Pedido
Continuar el falsador H4 usando datos conductuales y actividad neural reales.

## Datos medidos
Dataset público Harvard Dataverse, `R65D11 two-photon recording data`, Aymanns et al. Se adquirieron 8 trials del mismo fly/genotipo: etiquetas de conducta `behaviour_predictions_daart.pkl` y trazas `DFF_dic.p` con 2 ROIs por trial. Los archivos se verificaron por estructura y tamaño; el índice conductual contiene 7.440 frames por trial y las trazas 1.067 frames.

El repositorio de análisis de los autores fue leído: su alineación oficial usa señales de sincronización ThorSync, interpola DFF sobre frames de cámara y corrige `Trial = Trial - 2`.

## Instrumento ejecutado
Runner versionado: `tools/h4_neural_behavior.py`. El pretest interpola linealmente cada traza de 1.067 a 7.440 frames por trial, preserva el trial como unidad y mide clasificación de acción dentro de trial contra una permutación de etiquetas. Esto es una premedición, no la alineación ThorSync final.

## Evidencia cruda verbatim
```text
n_trials 8

deltas [0.001351, 0.014811, 0.018101, 0.019877, 0.00905, 0.01689, 0.00878, 0.024777]
acc [0.671887, 0.825248, 0.687019, 0.714171, 0.634472, 0.731948, 0.800081, 0.723942]
shuffle [0.670536, 0.810436, 0.668918, 0.694294, 0.625422, 0.715058, 0.791301, 0.699165]
pair_cosine_minmaxmean 0.03996797852409556 0.9999950347707683 0.9082213960227177
md5 97948ac6725a0714dc1bac4b37b1a1a6 bytes 16770
```

## Lectura correcta
La actividad de estos dos ROIs cambia entre algunas etiquetas, pero el resultado no es una falsación limpia: la ventaja sobre el shuffle es pequeña (`0.0014` a `0.0248`) y la accuracy cruda está dominada por el desbalance de clases. Las similitudes de centroides van de `0.03997` a `0.999995`, por lo que no hay una separación universal de rutas.

## Veredicto
Esto demuestra que el dataset sirve para el falsador fuerte y que contiene contexto conductual compartido dentro de trial con acciones alternativas. **H4 fuerte sigue NO MEDIDA**: falta usar la sincronización ThorSync exacta, incorporar más ROIs/neuronas, mapearlas a identidades FlyWire y correr el contraste topología real vs null, además de silenciados cruzados. No se debe llamar apoyada ni refutada por este pretest.

## Archivos
- Runner: `tools/h4_neural_behavior.py`, commit `959a4100a56f7e7e727d10859e48db61fee5cd83`.
- Resultado local no commiteado por ser derivado de datos externos: `/workspace/h4_data/aymanns/h4_neural_behavior.json`, md5 `97948ac6725a0714dc1bac4b37b1a1a6`.
- Este recibo.

--- METODO TITAN ---
Accion delicada: NO
Modo aplicado: TITAN FULL
Rubrica: N/A (instrumento científico y pretest)
N/A declarados: deployment, security, CI no aplican; mapping FlyWire y null topológico quedan NO MEDIDOS
Review externo: no pedido
Instrumento: MUDH Gateway build.run, salida cruda arriba; datos públicos Dataverse y repositorio de análisis de autores
