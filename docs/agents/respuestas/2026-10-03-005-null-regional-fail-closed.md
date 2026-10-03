# Stress test del null regional: fail-closed

**Doc público asociado:** [Regional null rechazado correctamente: 10/10 guards pasan, anatomía sigue NO MEDIDA](https://app.clickup.com/90171457413/docs/2kza6fw5-18777)

## 1. Pedido

Ejecutar el stress test del null regional sobre la unidad `ROI_COMPARTMENT/POPULATION`, sin transformar filas `UNMAPPED` en regiones anatómicas.

## 2. Herramienta y máquina

Se ejecutó `tools/h4_regional_null_stress.py` en `brain-env`, servicio `build`, sobre la rama `titan/paso-1-identidad-roi-2026-10-03`, commit de trabajo `c6aa3c361b6ddf0efe6afcf89495b799dede7aaf`.

## 3. Qué se midió

- 10 casos de frontera.
- 10/10 pasaron.
- El manifiesto público R65D11 tiene `row_count=16`, `unmapped_rows=16`, `region_rows=0`, `population_rows=0`.
- El manifiesto público fue **rechazado** para el null regional.
- El stress test quedó **PASS_FAIL_CLOSED**.
- El null regional biológico quedó **NO MEDIDO**.

## 4. Evidencia cruda verbatim

```text
exit_code=0
--- stdout ---
{"biological_regional_null": "NO_MEDIDO", "case_count": 10, "failed_cases": 0, "out": "/tmp/h4-regional-null-stress.json", "passed_cases": 10, "stress_verdict": "PASS_FAIL_CLOSED"}
--- stderr ---

```

El recibo JSON completo, con cada caso y su salida, está en [`docs/agents/evidencia/2026-10-03-005-regional-null-stress.json`](https://github.com/gatehot59-star/drosophila-fep-connectome/blob/titan/paso-1-identidad-roi-2026-10-03/docs/agents/evidencia/2026-10-03-005-regional-null-stress.json).

## 5. Casos cubiertos

1. Rechazo del manifiesto público sin filas `REGION_MAPPED`.
2. Aceptación de dos filas regionales con etiqueta y provenance explícitas.
3. Rechazo de región sin etiqueta.
4. Rechazo de región derivada de `ROI_0`.
5. Rechazo de evidencia basada solo en DFF.
6. Rechazo de una fila `UNMAPPED` que trae región.
7. Rechazo de pesos poblacionales que no suman 1.
8. Rechazo de `root_id` ausente de annotations.
9. Rechazo de pareja trial/ROI faltante.
10. Rechazo de pareja trial/ROI duplicada.

## 6. Veredicto e interpretación

El guard funciona: no deja correr un null regional con el dataset actual y no acepta inferencias por nombre de ROI, DFF, mezcla de estados, pesos inválidos ni IDs desconocidos. Esto valida el instrumento, no la anatomía: no se produjo p-value, z-score ni null biológico.

## 7. Archivos generados

- `tools/h4_regional_null_stress.py`.
- `docs/agents/evidencia/2026-10-03-005-regional-null-stress.json`.
- Este archivo.
- [Doc público](https://app.clickup.com/90171457413/docs/2kza6fw5-18777).

## 8. NO MEDIDO

Región anatómica real de `ROI_0` y `ROI_1`, null regional biológico, root IDs/pesos reales, causalidad y equivalencia SparseLTC→DBC3 sobre señal biológica.

--- METODO PROMETEO ---
Accion delicada: NO
Modo aplicado: PROMETEO FULL
Rubrica: N/A (instrumento de stress y evidencia, sin merge)
N/A declarados: deployment, producto y causalidad no aplican
Review externo: no solicitado; silencio no es aprobación
Instrumento: `brain-env` ejecutó el script; exit code 0; salida cruda en `docs/agents/evidencia/2026-10-03-005-regional-null-stress.json`
Maquina: brain-env + GitHub API
Artefactos: `tools/h4_regional_null_stress.py` + `docs/agents/evidencia/2026-10-03-005-regional-null-stress.json` + este archivo + [Doc público](https://app.clickup.com/90171457413/docs/2kza6fw5-18777)
NO MEDIDO: null regional biológico, anatomía real, causalidad y SparseLTC→DBC3 biológico
