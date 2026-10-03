# Paso 1 cerrado: origen de `DFF_dic.p` localizado, ROI sin mapping anatómico

**Doc público asociado:** [Paso 1 cerrado: origen de DFF_dic localizado, ROI_0 y ROI_1 sin mapping anatómico](https://app.clickup.com/90171457413/docs/2kza6fw5-18637)

## Pedido

Ejecutar las decisiones del paso uno: localizar el pipeline que generó `DFF_dic.p`, buscar máscaras y metadata espacial, mantener separados animal/trial/ROI, congelar FlyWire v783, registrar descartes y cerrar como `NO_MAPPED_ROIS` si no aparece el puente experimental.

## Veredicto

**Paso uno cerrado como `NO_MAPPED_ROIS`.** Se localizó el pipeline y se inspeccionó el dataset público completo disponible para R65D11. Hay dos series de calcio, pero no hay máscara, centro, coordenada, imagen 2P, registro espacial ni root ID experimental. Las dos filas quedan explícitamente `UNMAPPED`; H4 fuerte continúa `NO MEDIDA` y el null anatómico celular queda bloqueado.

## Evidencia medida

### Pipeline

El código público de NeLy-EPFL usa la ruta `2p/output/GC6_auto/final/DFF_dic.p`. `get_rois()` devuelve `sorted(list(dff.keys()))` y `get_trace()` recupera una clave como un vector NumPy. El repositorio `DN_population_analysis` lista los ocho trials R65D11 y su función `load_R65D11_data()` vuelve a enumerar las claves ordenadas como índice de análisis `ROI`; no agrega una asignación anatómica.

Repositorios inspeccionados:

- `NeLy-EPFL/Ascending_neuron_screen_analysis_pipeline`, commit `1dd7cbdc347f5484e22ff4ab1a5f4f132b397c76`.
- `NeLy-EPFL/DN_population_analysis`, commit `2374d51722612d3250b1ac81feeedd65e13ab330`.

### DFF real

```text
type=dict
keys=['ROI_0', 'ROI_1']
ROI_0: ndarray shape=(1067,) dtype=float64
ROI_1: ndarray shape=(1067,) dtype=float64
sha256=16a43af5a0ae1cc5c91ef4b573e16361f92bd44268be48400ab1e6aa8969389d
```

Los 16 pickles inspeccionados, ocho de `all_dff` y ocho de `dff_by_trial`, tienen esas dos claves y 1.067 muestras por clave.

### Inventario del lago H4

```text
total_files 104
candidate_geometry []
```

No aparecen `roi_centers`, `mean_green.tif`, `crop_parameters`, `ROI_mask`, TIFF de imagen 2P, coordenadas, centroides, labels de segmentación ni archivos de registro.

### H5 de adquisición

```text
ROOT ['AI', 'CI', 'DI', 'Global']
AI ['Piezo Monitor']
CI ['Frame Counter']
DI ['Basler', 'CO2_Stim', 'Capture On', 'Frame out', 'OpFlow']
Global ['GCtr']
```

El H5 conserva ThorSync; no conserva una identidad FlyWire por ROI.

### Metadata

`Experiment.xml` aporta geometría de adquisición y `timepoints=1067`, pero no una máscara celular. `Pockels` aparece con `maskEnable=0` y `maskPath=""`.

`capture_metadata.json` aporta el recorte de las siete cámaras de conducta:

```text
FPS=30
Number of Frames=7440 por cámara
ROI Width=960 Height=480 OffX=512 OffY=392
```

Ese `ROI` pertenece a las cámaras, no a las dos trazas de calcio. Se descartó como fuente de mapping.

### Fuente pública R65D11

El dataset Dataverse `doi:10.7910/DVN/YU1N1A` contiene, para los ocho trials, DFF, H5, XML, metadata de cámaras, post-processing y predicciones; no contiene los archivos de geometría que el pipeline de población usa en otros datasets.

Existe un dataset separado `doi:10.7910/DVN/KTQT27` con imágenes confocales LSM de morfología MCFO de R65D11. Se registra como fuente anatómica de referencia, pero no como mapping: es otra adquisición y no trae la transformación desde la imagen funcional de cada trial a FlyWire.

### Gate fail-closed

Se ejecutó el instrumento versionado `tools/h4_roi_anatomy_manifest.py` con una tabla de dos filas `UNMAPPED` y la snapshot de annotations en `brain-env`.

Salida cruda:

```text
{"counts": {"annotation_rows": 139248, "mapped_rois": 0, "roi_count": 2, "unmapped_rois": 2}, "mapping_verdict": "NO_MAPPED_ROIS", "out": "/tmp/r65d11_roi_manifest.json", "verdict": "BIEN"}
```

```text
annotations bytes=31718505
annotations md5=719904abad876c68ace1b5690c9b9b63
mapping md5=51c5b0e4d4781645480193ef7df18512
schema=h4-roi-anatomy-map/v1
```

`BIEN` aquí significa que la tabla explícita es coherente y el gate no infirió anatomía. No significa que H4 esté probada.

## Tabla final

| animal_id | trial_id | roi_name | roi_unit | mapping_status | root_id | motivo |
|---|---:|---|---|---|---|---|
| R65D11-tdTomGC6fopt-fly1 | 1..8 | ROI_0 | UNKNOWN | UNMAPPED | ninguno | no hay máscara, centro, coordenada ni ID experimental |
| R65D11-tdTomGC6fopt-fly1 | 1..8 | ROI_1 | UNKNOWN | UNMAPPED | ninguno | no hay máscara, centro, coordenada ni ID experimental |

`animal_id`, `trial_id` y `roi_name` permanecen separados. `ROI_0` y `ROI_1` no se convierten en identidades globales.

## Error de ejecución y recuperación

La primera tabla temporal se escribió con las secuencias literales `\\t`, por lo que el gate devolvió `MAL: mapping missing columns`. Se corrigió el TSV usando separadores tab reales y se repitió la misma validación: `exit=0`, `verdict=BIEN`, `mapping_verdict=NO_MAPPED_ROIS`. La salida roja inicial era un defecto del instrumento de transferencia, no un resultado científico.

## Prohibiciones respetadas

- No `ROI_0 → root_id 0`.
- No `ROI_1 → root_id 1`.
- No mapping por orden de claves.
- No mapping por correlación de DFF.
- No mapping por neuropilo, etiqueta conductual o línea Gal4.
- No null anatómico celular.
- No causalidad.

## Próximo movimiento

El siguiente intento debe buscar el directorio original de 2P y, en particular, `roi_centers.txt`, `mean_green.tif`, `crop_parameters.csv`, máscaras y anotaciones del operador. Si no aparece esa fuente, el paso uno queda cerrado como `NO_MAPPED_ROIS`; cualquier continuación debe cambiar formalmente la unidad de análisis a población/región o buscar una fuente experimental mejor.

## NO MEDIDO

- Correspondencia funcional ROI→confocal.
- Correspondencia ROI→root_id FlyWire.
- Si cada ROI es una neurona, axón, soma o población.
- Registro espacial reproducible.
- Null anatómico pareado.
- Silenciamiento causal.

--- METODO TITAN ---
Accion delicada: NO
Modo aplicado: TITAN FULL
Rubrica: N/A (medición de provenance y cierre de gate, sin merge ni cambio de contrato)
N/A declarados: deployment, producto y causalidad no aplican; el gate anatómico sí fue ejecutado
Review externo: no solicitado; silencio no es aprobación
Instrumento: MUDH Gateway `build` en `brain-env`, GitHub API, GitHub code search, Dataverse API y búsqueda web; evidencia cruda en este archivo y manifest asociado
Maquina: brain-env + GitHub API + Dataverse API
Artefactos: `docs/agents/respuestas/2026-10-03-002-paso-1-no-mapped-rois.md` + `docs/agents/evidencia/2026-10-03-002-r65d11-roi-mapping.tsv` + `docs/agents/evidencia/2026-10-03-002-r65d11-roi-manifest.json` + [Doc público](https://app.clickup.com/90171457413/docs/2kza6fw5-18637)
NO MEDIDO: correspondencia funcional ROI→confocal, ROI→root_id, ROI individual frente a poblacional, null anatómico pareado y causalidad