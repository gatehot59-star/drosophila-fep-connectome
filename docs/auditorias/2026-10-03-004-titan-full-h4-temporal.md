# TITAN FULL: auditoría del proyecto y corrección H4 temporal

**Fecha:** 2026-10-03 UTC / 2026-10-02 ART  
**Rama auditada:** `titan/h4-temporal-halves-2026-10-02`  
**Base científica:** `titan/h4-generalization-2026-10-02`  
**Objeto exacto:** pipeline H4 alineado, null temporal, evidencia y estado del producto conectoma→SparseLTC→DBC3.

## Veredicto ejecutivo

El proyecto tiene un pipeline H4 mucho más confiable que el histórico, pero todavía no tiene H4 fuerte demostrada. La auditoría encontró y corrigió un defecto real en el null temporal: mezclaba `label+length` sin recomputar el vector ROI del slot. El instrumento ahora permuta solo labels dentro de cada segmento y conserva exactamente la longitud y el vector de cada slot.

La corrección no cambió el número porque el score no consumía el metadata de longitud; eso no salva el defecto. El estado correcto es: **instrumento BIEN, estabilidad temporal sugestiva pero NO EVIDENCIA ROBUSTA, H4 fuerte NO MEDIDA**.

## Estado medido por capa

| Capa | Estado | Evidencia |
|---|---|---|
| Provenance/alignment | BIEN en los 8 trials; `Frame` rechazado | loader, features y guard; checks verdes |
| Null por bouts | BIEN; 999 permutaciones publicadas para el bloque previo | `h4_block_null.py` y recibos 009-011 |
| Generalización entre trials | NO EVIDENCIA, `p=0.623` | `h4_trial_generalization.py`, recibo 012 |
| Estabilidad temporal corregida | NO EVIDENCIA ROBUSTA, `p=0.055` | `h4_temporal_halves.py`, recibo 013 |
| Mapping anatómico ROI→FlyWire/cell type/neuropilo | NO MEDIDO | deuda abierta |
| Null anatómico pareado | NO MEDIDO | deuda abierta |
| Silenciamiento causal | NO MEDIDO | deuda abierta |
| SparseLTC→DBC3 sobre señal biológica real | NO MEDIDO | deuda abierta |

## Medición temporal corregida

```text
animal=R65D11-tdTomGC6fopt-fly1
trials=8
context=co2_off
labels=walking,resting
permutations=999
seed=20261002
observed=0.5327595514498719
null_mean=0.5018239610724393
null_sd=0.019476626168946264
p_greater_equal=0.055
z=1.588344413918904
raw_sha256=c2c0e2f2093bc85650daa6bb487b8dcd4bf1ae38278d64de24fd040abb202d98
```

El resultado es descriptivo, intra-animal y no causal. `p=0.055` queda arriba del umbral one-sided 0.05: no se vende como confirmación.

## Correcciones ejecutadas

1. El null deja de cambiar la longitud declarada de un slot sin cambiar el vector que lo representa.
2. El null preserva límites de los 7 segmentos `co2_off` por trial.
3. El falsador verifica por segmento: conteos de labels, longitudes por slot y vectores por slot.
4. La suite completa pasa: 34 tests, repartidos 7+6+7+5+4+5.
5. El rerun real se repite byte a byte.
6. Se actualizan summary, recibo, ADR y contexto público del PR.

## Scorecard TITAN aplicable

Tipo de entrega: instrumento científico + auditoría + workflow. N/A: deployment, ABI y performance de producto.

| Criterio | Score | Evidencia |
|---|---:|---|
| Completitud | 14/15 | instrumento, tests, workflow, summary, log, ADR, recibo y auditoría presentes en el PR |
| Ejecutabilidad | 15/15 | 34 tests OK y corrida real de 999 permutaciones en brain-env |
| Seguridad | 13/15 | fail-closed ante `Frame`, animales mezclados y schema inválido; no hay superficie de red; falta revisión externa del diseño estadístico |
| Testing | 14/15 | positivos, negativos, reproducibilidad y falsador del defecto; falta CI con datos reales, no apropiado para el runner público |
| Arquitectura | 9/10 | separación loader/alignment/features/null/temporal; falta separar explícitamente split temporal por segmentos si se cambia la pregunta biológica |
| DevOps | 8/10 | workflow limpio y checks GitHub verdes; evidencia grande completa sigue retenida en brain-env por checksum |
| Documentación | 10/10 | ADR, recibo, contexto y auditoría con límites explícitos |
| Innovación | 4/5 | falsador específico de metadata-vector, null segment-preserving y cierre reproducible |
| Proceso QA | 5/5 | defecto reproducido antes de corregir; checksum, repetición y salida cruda publicados |

**Total: 92/100. APROBADO con deuda científica explícita.**

## Deudas que bloquean el claim biológico

- mapear las dos ROIs a identidad anatómica real;
- construir null que preserve grado, neuropilo, distancia y signo;
- definir una tarea sensoriomotora independiente de las labels DAART;
- ejecutar silenciamientos cruzados y comparar rutas activas contra actividad difusa;
- correr SparseLTC sobre subgrafos observados y medir el puente a DBC3;
- agregar otro animal antes de cualquier lenguaje cross-animal.

## Método

```text
--- METODO TITAN ---
Accion delicada: SI, se modificó evidencia pública y workflow en un PR; no se tocó main ni se mergeó.
Modo aplicado: TITAN FULL
Rubrica: 92/100 sobre 100 aplicables a instrumento/auditoría/workflow
N/A declarados: deployment, ABI y performance de producto no aplican
Review externo: checks GitHub verdes; review de Copilot pendiente/no medido
Instrumento: brain-env vía build; Python stdlib; 34 tests; rerun 999; raw checksum commiteado
```
