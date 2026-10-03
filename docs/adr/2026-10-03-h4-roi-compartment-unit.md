# ADR: ROI-compartimento/población como unidad cuando falta geometría celular

**Fecha:** 2026-10-03 ART  
**Estado:** aceptada para el dataset público R65D11; mapping celular sigue bloqueado.

## Contexto

El dataset público R65D11 conserva dos trazas por trial en `DFF_dic.p`, `ROI_0` y `ROI_1`, con 1.067 muestras cada una. El pipeline original de Aymanns extraía esas trazas desde parches alrededor de `2p/roi_centers.txt`, pero esos centros, máscaras, stacks y crop no están publicados junto al dataset R65D11 que tenemos. El gate celular v1 cerró con `NO_MAPPED_ROIS` para las dos ROI.

## Decisión

Para análisis descriptivo sobre el dataset público, la unidad será `ROI_COMPARTMENT/POPULATION`, no neurona individual.

El contrato `h4-roi-compartment-map/v1` admite tres estados explícitos:

- `UNMAPPED`: compartimento funcional sin identidad regional/celular; habilita solo análisis descriptivo.
- `REGION_MAPPED`: compartimento asignado a una región, sin afirmar célula ni root ID.
- `POPULATION_MAPPED`: compartimento representado por varios `root_id` con pesos positivos que suman 1, sin afirmar que la ROI sea una sola neurona.

El contrato exige conservar `animal_id`, `trial_id` y `roi_name` por separado. Prohíbe usar el índice de la ROI, correlación de señal o una etiqueta de neuropilo como identidad celular.

## Alternativas descartadas

1. **Seguir llamando neurona a cada ROI:** descartado porque no hay evidencia de que el parche funcional sea una sola célula.
2. **Inventar o inferir un root ID:** descartado por el gate fail-closed y porque el atlas no contiene la correspondencia experimental.
3. **Detener todo H4:** descartado; todavía es válido medir separación ROI-label descriptiva dentro del animal, con alcance limitado.
4. **Descargar imágenes confocales y tratarlas como mapping:** descartado; son otra adquisición y falta transformación funcional→confocal→FlyWire.

## Consecuencias

- H4 descriptiva puede continuar con unidad ROI/compartimento.
- H4 anatómica fuerte, null anatómico celular, ruta causal y SparseLTC→DBC3 biológico siguen bloqueados.
- Un futuro null debe conservar la unidad declarada: regional o poblacional, no celular por defecto.
- Si aparecen los archivos originales 2P, el contrato celular v1 puede volver a usarse como evidencia adicional; este ADR no borra esa vía.

## Interface contract

El TSV usa exactamente estas columnas:

```text
animal_id	trial_id	roi_name	roi_unit	mapping_status	region_label	root_ids	root_weights	evidence_kind	confidence	notes
```

Para `UNMAPPED`: `root_ids` y `root_weights` vacíos, `region_label` vacío, `evidence_kind=unmapped`, `confidence=0`.  
Para `REGION_MAPPED`: `roi_unit=REGION`, `region_label` y evidencia regional obligatorios, sin root IDs.  
Para `POPULATION_MAPPED`: `roi_unit=POPULATION` o `ROI_COMPARTMENT`, listas semicolon-separated de root IDs y pesos alineados, positivos y con suma 1, y todos los IDs presentes en la snapshot de annotations.

## Flujo

```text
DFF_dic.p + animal_id + trial_id + roi_name
        |
        v
h4_roi_compartment_manifest.py
        |
        +--> UNMAPPED --------> análisis descriptivo ROI-label
        |
        +--> REGION_MAPPED ---> análisis regional, sin claim celular
        |
        +--> POPULATION_MAPPED -> agregación ponderada, sin claim de neurona única
```

La frontera de confianza es la snapshot de annotations: solo los `root_id` declarados en un manifest poblacional cruzan esa frontera. Ninguna señal DFF puede crear un ID.

## Riesgos y mitigaciones

- **Riesgo:** volver a interpretar `ROI_0` como neurona. **Mitigación:** `roi_unit` obligatorio y tests que rechazan contratos inválidos.
- **Riesgo:** pesos poblacionales mal normalizados. **Mitigación:** parser fail-closed y suma 1 con tolerancia `1e-6`.
- **Riesgo:** root ID inexistente. **Mitigación:** pertenencia obligatoria a annotations.
- **Riesgo:** mezclar trials o animales. **Mitigación:** pareja `(trial_id, roi_name)` única y `animal_id` obligatorio.
- **Riesgo:** análisis causal sobre señal descriptiva. **Mitigación:** limitaciones explícitas del manifest y ADR.

## Verificación

El instrumento y sus tests se ejecutan con:

```text
python3 -m unittest discover -s tests -p 'test_h4_roi_compartment_manifest.py' -v
```

El dataset público actual debe producir 16 filas `UNMAPPED` para 8 trials × 2 ROI. Ese resultado no prueba anatomía: prueba que la falta de anatomía quedó representada sin inferencia.

--- METODO PROMETEO ---
Accion delicada: NO
Modo aplicado: PROMETEO FULL
Rubrica: N/A (ADR y contrato, sin merge ni cambio de contrato existente)
N/A declarados: deployment y producto no aplican; testing del instrumento sí se adjunta
Review externo: no solicitado; silencio no es aprobación
Instrumento: contrato Python y tests versionados; ejecución queda en evidencia del recibo asociado
Maquina: brain-env + GitHub API
Artefactos: `tools/h4_roi_compartment_manifest.py`, `tests/test_h4_roi_compartment_manifest.py`, este ADR y Doc de ClickUp
NO MEDIDO: mapping funcional nuevo, root IDs nuevos, null anatómico y causalidad
