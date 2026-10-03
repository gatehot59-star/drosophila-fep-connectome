# CONTEXTO VIVO · conectoma / FEP / H4

**Última actualización:** 2026-10-03 (cierre del paso 1, `NO_MAPPED_ROIS`)  
**Estado canónico de `main`:** auditado en `a4f5a8e9143173bf609eff430bcca3d5d8699c48`.

## Veredicto operativo

**H4 fuerte: NO MEDIDA.** La cadena de instrumentos H4 está materializada y auditada, pero no demuestra mapping anatómico ni causalidad. H4 débil queda refutada solo en su alcance estrecho de poblaciones anotadas.

**Paso 1 anatómico: cerrado como `NO_MAPPED_ROIS`.** El origen de `DFF_dic.p` fue localizado, pero el dataset público R65D11 no conserva máscaras, centros, coordenadas, imágenes 2P ni un registro que permita asignar `ROI_0` o `ROI_1` a una célula o root ID.

## Estado confirmado en main

- Alignment guard: 7 contratos.
- Loader oficial: 6 contratos; 8/8 trials Aymanns reales con manifests `BIEN` en la corrida original.
- Features ROI/contexto/bouts: 7 contratos; 8/8 trials materializados en la corrida original.
- Null por bouts: 5 contratos; distribución pooled exacta de 999 scores publicada.
- Generalización intra-animal: 4 contratos; `balanced accuracy=0.5018855395873556`, `p=0.623`, sin evidencia de generalización entre trials.
- Estabilidad temporal: 5 contratos; `observed=0.5327595514498719`, `p=0.055`, sugestivo pero no positivo.
- Regresión integrada: 34 contratos pasaron en el head pre-merge `646c0343c7b8aa28d7ee6d2395e2e34465a07b92`; la auditoría independiente señaló que el SHA final anterior no tenía check propio.
- Auditoría main final: `docs/auditorias/2026-10-02-004-auditoria-main-final-34-contratos.md`, score 36/40.

## Paso 1 medido

- Pipeline público: `NeLy-EPFL/Ascending_neuron_screen_analysis_pipeline`, commit `1dd7cbdc347f5484e22ff4ab1a5f4f132b397c76`.
- Análisis público R65D11: `NeLy-EPFL/DN_population_analysis`, commit `2374d51722612d3250b1ac81feeedd65e13ab330`.
- Animal: `R65D11-tdTomGC6fopt-fly1`.
- Trials: 1 a 8, mantenidos separados.
- `DFF_dic.p`: dos claves, `ROI_0` y `ROI_1`, 1.067 muestras `float64` cada una.
- Inventario H4 inspeccionado: 104 archivos, ningún candidato de geometría espacial.
- H5: solo `AI`, `CI`, `DI`, `Global`; no identidad anatómica.
- Gate: `schema=h4-roi-anatomy-map/v1`, `verdict=BIEN`, `mapping_verdict=NO_MAPPED_ROIS`, `mapped_rois=0`, `unmapped_rois=2`, `annotation_rows=139248`.
- Snapshot FlyWire: annotations MD5 `719904abad876c68ace1b5690c9b9b63`.

La tabla explícita se encuentra en `docs/agents/evidencia/2026-10-03-002-r65d11-roi-mapping.tsv`; el manifest en `docs/agents/evidencia/2026-10-03-002-r65d11-roi-manifest.json`. Ningún `root_id` fue asignado.

## Decisión anatómica

`ROI_0` y `ROI_1` quedan con:

- `roi_unit=UNKNOWN`;
- `mapping_status=UNMAPPED`;
- `evidence_kind=unmapped`;
- `confidence=0`;
- `root_id=null`.

El campo `ROI` dentro de `capture_metadata.json` se descartó porque describe el recorte de las siete cámaras de conducta (`960x480`, offsets `512,392`), no la segmentación del calcio. `Experiment.xml` aporta parámetros de adquisición, pero `Pockels maskEnable=0` y `maskPath=""`; no hay una máscara celular.

Existe un dataset separado de confocal R65D11 (`doi:10.7910/DVN/KTQT27`) con morfología MCFO. Es referencia anatómica, no mapping funcional: falta registrar cada imagen funcional de trial contra esa muestra y contra FlyWire.

## Estado de producto y ciencia

SparseLTC, DualBrain y DBC3 son trabajo propio de Abraham. SparseLTC→DBC3 sobre señal biológica real, mapping ROI→FlyWire/cell type/neuropilo, null anatómico pareado y silenciamiento causal siguen **NO MEDIDOS**. ComplexVectorLTC queda experimental hasta demostrar una tarea donde fase/acoplamiento IQ sean necesarios.

## Próximo paso, sin saltar el orden

1. Buscar el directorio original de 2P y, si existe, `roi_centers.txt`, `mean_green.tif`, `crop_parameters.csv`, máscaras y anotaciones del operador.
2. Si no aparece, elegir formalmente una fuente experimental mejor o cambiar la unidad de análisis a población/región.
3. Solo con geometría y provenance reproducibles diseñar el mapping y el null anatómico pareado.
4. Mantener bloqueado SparseLTC→DBC3 sobre señal real hasta que exista una unidad anatómica o poblacional defendible.

## Fuentes

- `docs/auditorias/2026-10-02-004-auditoria-main-final-34-contratos.md`
- `docs/agents/respuestas/2026-10-02-011-h4-exact-distribution-published.md`
- `docs/agents/respuestas/2026-10-02-012-h4-trial-generalization.md`
- `docs/agents/respuestas/2026-10-02-013-h4-temporal-halves.md`
- `docs/agents/respuestas/2026-10-03-001-paso-1-identidad-experimental-roi.md`
- `docs/agents/respuestas/2026-10-03-002-paso-1-no-mapped-rois.md`
- `docs/agents/evidencia/2026-10-03-002-r65d11-roi-mapping.tsv`
- `docs/agents/evidencia/2026-10-03-002-r65d11-roi-manifest.json`

## NO MEDIDO

- Correspondencia funcional ROI→confocal.
- Mapping anatómico ROI→root_id/cell type/neuropilo.
- Si cada ROI es individual, axonal o poblacional.
- Registro espacial reproducible.
- Null anatómico pareado.
- Corrida biológica end-to-end post-merge.
- Equivalencia SparseLTC→DBC3 sobre señal real.
- Review externo del pipeline; silencio no es aprobación.

--- METODO TITAN ---
Accion delicada: NO
Modo aplicado: TITAN FULL
Rubrica: N/A (actualizacion de contexto y estado de medicion)
N/A declarados: deployment, producto y causalidad no aplican; provenance y gate anatómico sí
Review externo: no solicitado; silencio no es aprobación
Instrumento: MUDH Gateway `build` en brain-env, GitHub API, Dataverse API, gate `h4_roi_anatomy_manifest.py`; evidencia cruda en `docs/agents/respuestas/2026-10-03-002-paso-1-no-mapped-rois.md` y `docs/agents/evidencia/`
Maquina: brain-env + GitHub API + Dataverse API
Artefactos: `docs/agents/CONTEXTO-drosophila-fep.md` + [Doc público](https://app.clickup.com/90171457413/docs/2kza6fw5-18637)
NO MEDIDO: correspondencia funcional ROI→confocal, ROI→root_id, unidad individual/poblacional, null anatómico pareado y causalidad