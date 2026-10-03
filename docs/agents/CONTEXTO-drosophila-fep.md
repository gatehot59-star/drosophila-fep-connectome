# CONTEXTO VIVO · conectoma / FEP / H4

**Última actualización:** 2026-10-03 (anatomía confocal R65D11 medida)  
**Estado canónico de `main`:** auditado en `a4f5a8e9143173bf609eff430bcca3d5d8699c48`.

## Veredicto operativo

**H4 fuerte: NO MEDIDA.** La cadena H4 está materializada y auditada, pero no demuestra mapping anatómico funcional ni causalidad. H4 débil queda refutada solo en su alcance estrecho de poblaciones anotadas.

**Paso anatómico:** el gate celular cerró `NO_MAPPED_ROIS`; la unidad pública pasa a `ROI_COMPARTMENT/POPULATION` para análisis descriptivo. El stress test regional pasó 10/10 y permanece fail-closed.

**Anatomía nueva:** se midió la geometría física de los stacks confocales R65D11, pero siguen sin existir una transformación funcional 2P→confocal ni un mapping de `ROI_0`/`ROI_1` a región o `root_id`.

## Estado H4 confirmado

- Pipeline corregido: 41 contratos.
- Animal: `R65D11-tdTomGC6fopt-fly1`; trials 1 a 8 separados.
- Null ROI-label por bouts: observado `0.35831155721189717`, null mean `0.06104563938527175`, `p=0.001`, `z=17.11192372053771`; es descriptivo dentro de un animal.
- Generalización leave-one-trial-out: balanced accuracy `0.5018855395873556`, `p=0.623`; sin evidencia de generalización.
- Estabilidad temporal: observado `0.5327595514498719`, `p=0.055`; sugestivo, no positivo.
- Manifiesto público: 16 filas `UNMAPPED`, 0 regionales, 0 poblacionales.
- Stress regional: `case_count=10`, `passed_cases=10`, `failed_cases=0`, `PASS_FAIL_CLOSED`.

## Anatomía confocal medida

Dataset público: `doi:10.7910/DVN/KTQT27`, licencia CC0 1.0.

- Brain 40x: `352×2×1024×1024`, voxel `0.142084×0.142084×0.330 µm`, campo `145.494×145.494×116.160 µm`.
- VNC 40x: `353×2×1024×1024`, voxel `0.312585×0.312585×0.330 µm`, campo `320.087×320.087×116.490 µm`.
- Herramienta: `tools/h4_anatomy_measure.py`; tests: 3/3 OK.
- Evidencia: `docs/agents/evidencia/2026-10-03-006-r65d11-confocal-anatomy-geometry.json`.
- Respuesta: `docs/agents/respuestas/2026-10-03-006-anatomia-confocal-medida.md`.

Esto mide anatomía de la muestra GAL4, no identidad funcional individual. La segmentación completa por canal, bounding boxes, registro 2P→confocal, región real, root IDs, null anatómico y causalidad siguen `NO MEDIDO`.

## Conectoma y motor

FlyWire v783: aproximadamente 138.639 neuronas, 15.091.983 aristas dirigidas agregadas y 54.492.922 contactos. SparseLTC corre sobre CSR y estados temporales; el adaptador SparseLTC→DBC3 compila, pero el end-to-end con señal biológica real y pesos DBC3 reales sigue pendiente.

## Próximo orden

1. Mantener `UNMAPPED`; no fabricar mapping anatómico con confocal.
2. Ejecutar SparseLTC→DBC3 sobre señal real con comparadores.
3. Cerrar benchmarks DBC3-live: pesos reales, receptores heterogéneos, pérdida, delay, replay y deriva.
4. Medir latencia, memoria, bytes y energía en Actions x64/arm64 y hardware real.
5. Reabrir mapping solo con raw 2P privado o provenance experimental explícita.

## NO MEDIDO

Mapping ROI→root_id/cell_type/neuropilo; null anatómico real; causalidad; SparseLTC→DBC3 biológico end-to-end; backend DBC3 histórico completo; hardware edge, energía y adopción; revisión externa. `ComplexVectorLTC` y `CanonicalComplexLTCBatch` siguen experimentales.

--- METODO PROMETEO ---
Accion delicada: NO
Modo: actualización de contexto y cierre de medición anatómica, sin merge
Instrumento: GitHub API, navegador público, tifffile en brain-env y tests 3/3
Maquina: brain-env + GitHub API + navegador público
Artefactos: este contexto + `docs/agents/evidencia/2026-10-03-006-r65d11-confocal-anatomy-geometry.json` + `docs/agents/respuestas/2026-10-03-006-anatomia-confocal-medida.md` + [Doc público](https://app.clickup.com/90171457413/docs/2kza6fw5-18837)
NO MEDIDO: mapping funcional, causalidad, null anatómico y hardware edge