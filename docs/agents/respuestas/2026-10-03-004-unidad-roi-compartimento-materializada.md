# Unidad ROI-compartimento/población materializada

**Doc público asociado:** [Unidad ROI-compartimento materializada: 16 registros UNMAPPED y contrato poblacional](https://app.clickup.com/90171457413/docs/2kza6fw5-18737)

**Pedido:** ejecutar la elección A y avanzar con `ROI_COMPARTMENT/POPULATION`, sin tratar `ROI_0` ni `ROI_1` como neuronas.

## Veredicto

Contrato materializado y probado. El dataset público R65D11 produce **16 filas `UNMAPPED`**, correspondientes a 8 trials × 2 ROI; eso habilita análisis descriptivo y bloquea cualquier claim celular.

## Archivos generados

- `tools/h4_roi_compartment_manifest.py`: parser fail-closed para `UNMAPPED`, `REGION_MAPPED` y `POPULATION_MAPPED`.
- `tests/test_h4_roi_compartment_manifest.py`: 6 tests de contrato.
- `docs/adr/2026-10-03-h4-roi-compartment-unit.md`: decisión, alternativas y límites.
- `docs/agents/evidencia/2026-10-03-004-r65d11-compartment-manifest.json`: resultado reproducible de los 16 registros.

## Medición de tests

```text
Ran 6 tests in 0.011s
OK
```

Casos cubiertos: compartimentos no mapeados, región explícita, población con pesos normalizados, pesos inválidos, root ID ausente y pareja trial/ROI faltante.

## Medición del dataset público

```text
{"counts": {"annotation_rows": 139248, "population_rows": 0, "region_rows": 0, "row_count": 16, "unmapped_rows": 16}, "mapping_verdict": "UNMAPPED", "out": "/tmp/r65d11_compartment_manifest.json", "verdict": "BIEN"}
```

Snapshot FlyWire usada:

```text
annotations bytes=31718505
annotations md5=719904abad876c68ace1b5690c9b9b63
```

La primera invocación pública falló porque el shell `sh` preexpandió una variable de argumentos y omitió `--trial`; se repitió con argumentos explícitos y terminó `exit=0`. Los seis tests sí pasaron antes de esa falla de transporte.

## Contrato

`UNMAPPED` exige `root_ids` y `root_weights` vacíos, evidencia `unmapped` y confianza `0`. `REGION_MAPPED` exige etiqueta regional, pero no root IDs. `POPULATION_MAPPED` exige IDs declarados, pesos positivos alineados y suma 1, además de pertenencia a annotations.

Esto no crea mapping anatómico. Solo evita que una ROI funcional sin geometría vuelva a interpretarse como neurona individual.

## Próximo gate

Diseñar el null regional/poblacional sobre esta unidad, pero antes decidir qué región o población puede declararse con evidencia. Mientras no exista esa evidencia, el resultado correcto sigue siendo descriptivo ROI-label, no anatómico.

## NO MEDIDO

- Región anatómica real de `ROI_0` y `ROI_1`.
- Conjunto real de `root_id` y pesos.
- Null anatómico regional/poblacional.
- Causalidad.
- SparseLTC→DBC3 sobre señal biológica.
- CI del PR, porque la rama aún no está mergeada.

--- METODO PROMETEO ---
Accion delicada: NO
Modo aplicado: PROMETEO FULL
Rubrica: N/A (contrato fail-closed y tests, sin merge ni cambio del main)
N/A declarados: deployment y producto no aplican; testing sí fue ejecutado
Review externo: no solicitado; silencio no es aprobación
Instrumento: GitHub API para escritura; MUDH Gateway `build` en brain-env para unittest y manifest público; evidencia cruda en este archivo
Maquina: brain-env + GitHub API
Artefactos: `tools/h4_roi_compartment_manifest.py` + `tests/test_h4_roi_compartment_manifest.py` + `docs/adr/2026-10-03-h4-roi-compartment-unit.md` + `docs/agents/evidencia/2026-10-03-004-r65d11-compartment-manifest.json` + este archivo + [Doc público](https://app.clickup.com/90171457413/docs/2kza6fw5-18737)
NO MEDIDO: mapping regional real, población root_id real, null anatómico regional/poblacional, causalidad y SparseLTC→DBC3 biológico