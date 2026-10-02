# Falsador neural H4 sobre los ocho trials Aymanns

## Pedido
Run the neural falsifier across all eight selected trials.

## Instrumento
Runner `tools/h4_neural_behavior_all.py`, alineamiento equivalente a `utils2p` oficial: Basler/camera metadata, Frame Counter con `steps_per_frame=3`, tiempos ThorSync a 30 kHz, interpolación de DFF a frames de cámara. Se midieron por trial y por contexto CO2 (`co2_off`, `co2_on`) accuracy contra etiquetas barajadas y cosine entre centroides neurales de acción.

## Evidencia cruda verbatim
```text
bytes 31436 md5 3e1f32695176a48e1b66cc1254119416
[(trial, all_delta, co2_off_delta, co2_on_delta, n_on_pairs, n_on_frames)]
[(1, 0.007155412553614404, 0.007101319485232072, 0.004444444444444473, 1, 225),
 (3, 0.014268244022108578, 0.014718350072878361, -0.02666666666666684, 1, 225),
 (7, 0.017156687409894622, 0.016023312919161814, -0.08000000000000007, 1, 225),
 (4, 0.018795753156807926, 0.01938545721380691, 1.066666666666666e-01, 1, 225),
 (8, 0.00742987754804092, 0.00320266322440399, 0.01333333333333342, 1, 225),
 (5, 0.01973018657602832, 0.02132404181184666, 0.06777777777777783, 1, 223),
 (2, 0.012425588992098113, 0.012954393252647134, None, 0, 225),
 (6, 0.020332712499603445, 0.019995759117896528, 0.18222222222222206, 1, 225)]
off_delta_mean_sd 0.014338162137234184 0.006409328313052002 minmax 0.00320266322440399 0.02132404181184666
on_delta_mean_sd 0.03825396825396821 0.08778916274703832 minmax -0.08000000000000007 0.18222222222222206
off_cos_mean_minmax 0.938890552533269 0.5109270082806434 0.9999994646735276
on_cos_mean_minmax 0.9798442657558535 0.9312521063510031 0.9999844071088824
```

## Lectura
En `co2_off`, los 8 trials tienen señal pequeña y consistente sobre shuffle: delta medio `0,01434`, SD `0,00641`, rango `0,00320–0,02132`. Los centroides tienen cosine medio `0,93889`, rango `0,51093–0,999999`: algunas acciones separan la señal de dos ROIs, pero no hay una separación universal ni evidencia todavía de rutas topológicas distintas.

En `co2_on`, 7 trials tienen walking/resting alternativos y uno no. El delta medio es `0,03825`, pero SD `0,08779` y rango `−0,080–0,182`: es inestable y el contexto solo tiene 223–225 frames, por lo que no es un veredicto biológico. Los centroides siguen muy alineados: cosine medio `0,97984`, rango `0,93125–0,999984`.

## Veredicto
El falsador neural completo **no apoya H4 fuerte todavía**. Sí confirma que los ocho trials tienen actividad neural y conducta sincronizables y que el contexto `co2_off` ofrece acciones alternativas. La señal decodificable es pequeña; la variación `co2_on` es demasiado dependiente del trial y de una muestra de ~225 frames.

H4 fuerte queda **NO MEDIDA**, no refutada: faltan identidad anatómica de las ROIs, propagación SparseLTC sobre el subgrafo real, null anatómico pareado y silenciamientos cruzados. Decodificar acción no equivale a demostrar control dinámico de rutas.

## Archivos
- Runner: `tools/h4_neural_behavior_all.py`, commit `541dd0377eda83d389775969a52c05beaaf07dbd`.
- Resultado local: `/workspace/h4_data/aymanns/h4_neural_behavior_all.json`, 31.436 bytes, md5 `3e1f32695176a48e1b66cc1254119416`.
- Este recibo.

--- METODO TITAN ---
Accion delicada: NO
Modo aplicado: TITAN FULL
Rubrica: N/A (medición científica multi-trial)
N/A declarados: deployment/security/CI no aplican; mapping FlyWire, null topológico y causalidad quedan NO MEDIDOS
Review externo: no pedido
Instrumento: MUDH Gateway build.run; 8 H5, 8 metadata, 8 DFF y 8 behavior files; evidencia cruda y md5 arriba
