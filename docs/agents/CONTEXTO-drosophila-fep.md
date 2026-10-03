# CONTEXTO VIVO · conectoma / FEP / H4

**Última actualización:** 2026-10-03 (búsqueda pública 2P agotada; decisión de unidad pendiente)  
**Estado canónico de `main`:** auditado en `a4f5a8e9143173bf609eff430bcca3d5d8699c48`.

## Veredicto operativo

**H4 fuerte: NO MEDIDA.** La cadena de instrumentos H4 está materializada y auditada, pero no demuestra mapping anatómico ni causalidad. H4 débil queda refutada solo en su alcance estrecho de poblaciones anotadas.

**Paso 1 anatómico: `NO_MAPPED_ROIS`.** El origen de `DFF_dic.p` fue localizado y la búsqueda pública del raw 2P se agotó. El dataset R65D11 publicado no conserva máscaras, centros, coordenadas, imágenes 2P ni registro funcional contra confocal/FlyWire.

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
- Dataverse search `R65D11`: exactamente dos datasets, `DVN/YU1N1A` y `DVN/KTQT27`.
- `DVN/YU1N1A`: catálogo con `file_count=56`, sin `roi_centers`, `mean_green.tif`, `crop_parameters.csv`, máscaras o stacks 2P en los archivos publicados.
- `DVN/KTQT27`: confocal LSM MCFO; referencia morfológica separada, no mapping funcional.
- Preprocessing original: exige `2p/roi_centers.txt`, `2p/crop_parameters.csv`, `2p/warped_green.tif` y `2p/denoised_green.tif` para extraer parches DFF de `3x2`.
- Inventario H4 inspeccionado: 104 archivos, ningún candidato de geometría espacial.
- H5: solo `AI`, `CI`, `DI`, `Global`; no identidad anatómica.
- Gate: `schema=h4-roi-anatomy-map/v1`, `verdict=BIEN`, `mapping_verdict=NO_MAPPED_ROIS`, `mapped_rois=0`, `unmapped_rois=2`, `annotation_rows=139248`.
- Snapshot FlyWire: annotations MD5 `719904abad876c68ace1b5690c9b9b63`.

La tabla explícita está en `docs/agents/evidencia/2026-10-03-002-r65d11-roi-mapping.tsv`; el manifest en `docs/agents/evidencia/2026-10-03-002-r65d11-roi-manifest.json`. Ningún `root_id` fue asignado.

## Decisión anatómica actual

`ROI_0` y `ROI_1` quedan con:

- `roi_unit=UNKNOWN`;
- `mapping_status=UNMAPPED`;
- `evidence_kind=unmapped`;
- `confidence=0`;
- `root_id=null`.

No se adoptó todavía una unidad alternativa. La decisión pendiente es:

- **A:** adoptar unidad `ROI_COMPARTMENT/POPULATION` y continuar solo con claims descriptivos y un futuro null regional/poblacional;
- **B:** recuperar una copia no pública del directorio 2P y mantener abierto el mapping celular.

La recomendación operativa es A si el objetivo es avanzar con el dataset público; B requiere una fuente del operador o del directorio original que no está publicado.

## Estado de producto y ciencia

SparseLTC, DualBrain y DBC3 son trabajo propio de Abraham. SparseLTC→DBC3 sobre señal biológica real, mapping ROI→FlyWire/cell type/neuropilo, null anatómico pareado y silenciamiento causal siguen **NO MEDIDOS**. ComplexVectorLTC queda experimental hasta demostrar una tarea donde fase/acoplamiento IQ sean necesarios.

## Próximo paso bloqueado por decisión

1. Elegir A o B para fijar la unidad de análisis.
2. Si A: diseñar contrato `ROI_COMPARTMENT/POPULATION`, preservar `animal_id`, `trial_id`, `roi_name`, y mantener bloqueada toda lectura celular.
3. Si B: cargar los archivos originales de 2P y reconstruir `roi_centers`, máscaras, crop y registro.
4. Solo después diseñar null anatómico regional/poblacional o celular, respectivamente.

## Fuentes

- `docs/auditorias/2026-10-02-004-auditoria-main-final-34-contratos.md`
- `docs/agents/respuestas/2026-10-02-011-h4-exact-distribution-published.md`
- `docs/agents/respuestas/2026-10-02-012-h4-trial-generalization.md`
- `docs/agents/respuestas/2026-10-02-013-h4-temporal-halves.md`
- `docs/agents/respuestas/2026-10-03-001-paso-1-identidad-experimental-roi.md`
- `docs/agents/respuestas/2026-10-03-002-paso-1-no-mapped-rois.md`
- `docs/agents/respuestas/2026-10-03-003-busqueda-publica-2p-agotada.md`
- `docs/agents/evidencia/2026-10-03-002-r65d11-roi-mapping.tsv`
- `docs/agents/evidencia/2026-10-03-002-r65d11-roi-manifest.json`

## NO MEDIDO

- Correspondencia funcional ROI→confocal.
- Mapping anatómico ROI→root_id/cell type/neuropilo.
- Si cada ROI es individual, axonal o poblacional.
- Registro espacial reproducible.
- Existencia de una copia privada accesible del raw 2P.
- Null anatómico regional/poblacional o celular.
- Corrida biológica end-to-end post-merge.
- Equivalencia SparseLTC→DBC3 sobre señal real.
- Review externo del pipeline; silencio no es aprobación.

--- METODO PROMETEO ---
Accion delicada: NO
Modo aplicado: PROMETEO FULL
Rubrica: N/A (actualizacion de contexto y decision pendiente)
N/A declarados: deployment, producto, testing de código y causalidad no aplican
Review externo: no solicitado; silencio no es aprobación
Instrumento: GitHub API, Dataverse API, MUDH Gateway `build` en brain-env y búsqueda web; evidencia en `docs/agents/respuestas/2026-10-03-003-busqueda-publica-2p-agotada.md`
Maquina: brain-env + GitHub API + Dataverse API
Artefactos: `docs/agents/CONTEXTO-drosophila-fep.md` + [Doc público](https://app.clickup.com/90171457413/docs/2kza6fw5-18717)
NO MEDIDO: mapping funcional ROI→confocal, ROI→root_id, unidad individual/poblacional, raw 2P privado, null anatómico y causalidad