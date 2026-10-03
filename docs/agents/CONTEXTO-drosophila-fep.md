# CONTEXTO VIVO · conectoma / FEP / H4

**Última actualización:** 2026-10-03 (unidad ROI-compartimento materializada)  
**Estado canónico de `main`:** auditado en `a4f5a8e9143173bf609eff430bcca3d5d8699c48`.

## Veredicto operativo

**H4 fuerte: NO MEDIDA.** La cadena de instrumentos H4 está materializada y auditada, pero no demuestra mapping anatómico ni causalidad. H4 débil queda refutada solo en su alcance estrecho de poblaciones anotadas.

**Paso 1 anatómico:** `NO_MAPPED_ROIS` a nivel celular; por decisión del usuario, la unidad pública pasa a ser `ROI_COMPARTMENT/POPULATION` para análisis descriptivo, sin llamar neurona individual a ninguna ROI.

## Estado confirmado en main

- Alignment guard: 7 contratos.
- Loader oficial: 6 contratos; 8/8 trials Aymanns reales con manifests `BIEN` en la corrida original.
- Features ROI/contexto/bouts: 7 contratos; 8/8 trials materializados en la corrida original.
- Null por bouts: 5 contratos; distribución pooled exacta de 999 scores publicada.
- Generalización intra-animal: 4 contratos; `balanced accuracy=0.5018855395873556`, `p=0.623`, sin evidencia de generalización entre trials.
- Estabilidad temporal: 5 contratos; `observed=0.5327595514498719`, `p=0.055`, sugestivo pero no positivo.
- Regresión integrada: 34 contratos pasaron en el head pre-merge `646c0343c7b8aa28d7ee6d2395e2e34465a07b92`.
- Auditoría main final: `docs/auditorias/2026-10-02-004-auditoria-main-final-34-contratos.md`, score 36/40.

## Paso 1 medido

- Animal: `R65D11-tdTomGC6fopt-fly1`.
- Trials: 1 a 8, separados.
- `DFF_dic.p`: `ROI_0` y `ROI_1`, 1.067 muestras `float64` cada una.
- Dataset público R65D11: 56 archivos catalogados; no incluye centros, máscaras, stacks o crop 2P.
- Preprocessing original exige `2p/roi_centers.txt`, `2p/crop_parameters.csv`, `2p/warped_green.tif` y `2p/denoised_green.tif`.
- Inventario H4: 104 archivos, ningún candidato de geometría espacial.
- Gate celular: `mapping_verdict=NO_MAPPED_ROIS`, `mapped_rois=0`, `unmapped_rois=2`.
- Snapshot FlyWire: annotations MD5 `719904abad876c68ace1b5690c9b9b63`.

## Contrato ROI-compartimento materializado

Archivos:

- `tools/h4_roi_compartment_manifest.py`.
- `tests/test_h4_roi_compartment_manifest.py`.
- `docs/adr/2026-10-03-h4-roi-compartment-unit.md`.
- `docs/agents/evidencia/2026-10-03-004-r65d11-compartment-manifest.json`.
- `docs/agents/respuestas/2026-10-03-004-unidad-roi-compartimento-materializada.md`.

Tests: `Ran 6 tests in 0.011s`, `OK`. El dataset público produce 16 filas: 8 trials × 2 ROI, todas `UNMAPPED`; `row_count=16`, `unmapped_rows=16`, `region_rows=0`, `population_rows=0`, `verdict=BIEN`.

La tabla conserva `animal_id`, `trial_id` y `roi_name`. `UNMAPPED` tiene `root_ids=[]`, `root_weights=[]`, `evidence_kind=unmapped` y `confidence=0`. El contrato futuro permite `REGION_MAPPED` o `POPULATION_MAPPED`, pero no los afirma hoy.

## Decisión científica

La unidad actual es un compartimento funcional de imagen. H4 puede continuar con claims ROI-label descriptivos. H4 anatómica celular, null regional/poblacional real, causalidad y SparseLTC→DBC3 sobre señal biológica permanecen bloqueados.

No se asignó ningún `root_id`, región o peso. Las imágenes confocales R65D11 siguen siendo referencia morfológica separada, no mapping funcional.

## Próximo paso, sin saltar el orden

1. Diseñar el null compatible con `ROI_COMPARTMENT/POPULATION`, todavía sin afirmar una región.
2. Mantener la etiqueta `UNMAPPED` hasta que aparezca evidencia regional o poblacional.
3. Ejecutar solo análisis descriptivo ROI-label mientras no exista esa evidencia.
4. Si aparece una copia privada del raw 2P, se puede reabrir el camino celular sin invalidar este contrato.

## Fuentes

- `docs/agents/respuestas/2026-10-03-001-paso-1-identidad-experimental-roi.md`
- `docs/agents/respuestas/2026-10-03-002-paso-1-no-mapped-rois.md`
- `docs/agents/respuestas/2026-10-03-003-busqueda-publica-2p-agotada.md`
- `docs/agents/respuestas/2026-10-03-004-unidad-roi-compartimento-materializada.md`
- `docs/agents/evidencia/2026-10-03-002-r65d11-roi-manifest.json`
- `docs/agents/evidencia/2026-10-03-004-r65d11-compartment-manifest.json`

## NO MEDIDO

- Región real de `ROI_0` y `ROI_1`.
- Root IDs y pesos poblacionales reales.
- Null anatómico regional/poblacional.
- Correspondencia funcional ROI→confocal.
- Causalidad.
- Corrida biológica end-to-end post-merge.
- Equivalencia SparseLTC→DBC3 sobre señal real.
- Review externo del pipeline; silencio no es aprobación.

--- METODO PROMETEO ---
Accion delicada: NO
Modo aplicado: PROMETEO FULL
Rubrica: N/A (actualizacion de contexto tras decision del usuario)
N/A declarados: deployment, producto, causalidad y merge no aplican; contrato y tests sí
Review externo: no solicitado; silencio no es aprobación
Instrumento: GitHub API y MUDH Gateway `build` en brain-env; tests 6/6 y manifest 16 filas
Maquina: brain-env + GitHub API
Artefactos: `docs/agents/CONTEXTO-drosophila-fep.md` + [Doc público](https://app.clickup.com/90171457413/docs/2kza6fw5-18737)
NO MEDIDO: región real, root IDs/pesos reales, null anatómico regional/poblacional, causalidad y SparseLTC→DBC3 biológico