# Paso 1 agotado: no existe fuente pública de geometría 2P para R65D11

**Doc público asociado:** [Paso 1 agotado: no existe fuente pública de geometría 2P para R65D11](https://app.clickup.com/90171457413/docs/2kza6fw5-18717)

## Pedido

Continuar el paso uno después del cierre `NO_MAPPED_ROIS`: buscar el directorio original 2P, máscaras, centros, crop y anotaciones antes de decidir cómo seguir.

## Veredicto

Se agotaron las fuentes públicas razonables para recuperar el puente `DFF_dic.p → geometría experimental → anatomía`. No apareció `roi_centers.txt`, `mean_green.tif`, `crop_parameters.csv`, máscara, imagen 2P, coordenada o registro funcional contra confocal/FlyWire.

`ROI_0` y `ROI_1` permanecen `UNMAPPED`; H4 fuerte continúa `NO MEDIDA`. No se corrió ningún null anatómico.

## Evidencia medida

La búsqueda oficial de Dataverse por `R65D11` devolvió exactamente dos datasets:

```text
doi:10.7910/DVN/YU1N1A  R65D11 two-photon recording data
doi:10.7910/DVN/KTQT27  Confocal images
```

El catálogo del primero reportó `file_count=56`. Sus archivos son DFF, H5 ThorSync, XML, metadata de cámaras, post-processing y predicciones; no hay nombres de geometría 2P. El segundo contiene imágenes LSM de morfología MCFO, pero es otra adquisición y no contiene una transformación desde cada ROI funcional a una célula o root ID.

El repositorio `NeLy-EPFL/DN_population_analysis` lista los ocho trials R65D11 y su preprocessing original. `extraction_from_ROIs.py` exige:

```text
2p/roi_centers.txt
2p/crop_parameters.csv
2p/warped_green.tif
2p/denoised_green.tif
```

Extrae DFF de parches de `3x2` alrededor de cada centro y escribe `2p/roi_dFF.pkl`. Esa geometría existía en la fuente original de trabajo, pero no está en el dataset R65D11 publicado que tenemos.

El pipeline público que lee `DFF_dic.p` solo conserva claves ordenadas y vectores. El nombre `ROI_0`/`ROI_1` no es una identidad anatómica.

En `brain-env` el inventario persistente de `/workspace/h4_data/aymanns` dio:

```text
total_files 104
candidate_geometry []
```

La inspección del raw H5 dio:

```text
ROOT ['AI', 'CI', 'DI', 'Global']
AI ['Piezo Monitor']
CI ['Frame Counter']
DI ['Basler', 'CO2_Stim', 'Capture On', 'Frame out', 'OpFlow']
Global ['GCtr']
```

## Decisión pendiente

Hay dos caminos técnicamente honestos:

### A: adoptar unidad ROI-compartimento/población

Tratar cada serie como un compartimento funcional de imagen, posiblemente axonal o poblacional; mantener H4 como análisis descriptivo ROI-label; diseñar luego un null anatómico regional/poblacional; no asignar `root_id` individual ni llamar neurona a `ROI_0` o `ROI_1`.

### B: recuperar la fuente original 2P no pública

Obtener el directorio original o archivos del operador y recuperar `roi_centers.txt`, stacks, crop, máscaras y anotaciones. Solo entonces intentar registro espacial y mapping explícito.

La opción A es la recomendada para avanzar con el dataset público. No la aplico en silencio porque cambia la unidad científica del análisis.

## Qué no se modificó

No se tocó `main`, no se cambió el contrato anatómico v1, no se descargaron binarios grandes, no se asignó ningún ID y no se ejecutó inferencia anatómica.

## NO MEDIDO

- mapping funcional ROI→confocal;
- mapping ROI→root ID;
- si cada ROI es célula, axón o población;
- existencia de una copia privada accesible del raw 2P;
- null anatómico regional/poblacional;
- causalidad.

--- METODO PROMETEO ---
Accion delicada: NO
Modo aplicado: PROMETEO FULL
Rubrica: N/A (informe de búsqueda y decisión pendiente, sin cambio de contrato)
N/A declarados: deployment, producto, testing de código y causalidad no aplican
Review externo: no solicitado; silencio no es aprobación
Instrumento: GitHub API, Dataverse API, MUDH Gateway `build` en `brain-env` y búsqueda web; evidencia citada arriba
Maquina: brain-env + GitHub API + Dataverse API
Artefactos: `docs/agents/respuestas/2026-10-03-003-busqueda-publica-2p-agotada.md` + [Doc público](https://app.clickup.com/90171457413/docs/2kza6fw5-18717)
NO MEDIDO: mapping funcional ROI→confocal, ROI→root_id, unidad ROI individual/poblacional, raw 2P privado, null anatómico y causalidad