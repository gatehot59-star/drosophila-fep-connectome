# ADR: estabilidad temporal por mitades de bouts

**Fecha:** 2026-10-03 UTC / 2026-10-02 ART  
**Rama:** `titan/h4-temporal-halves-2026-10-02`

## Decisión

Medir la estabilidad temporal de la representación ROI separando cada trial en dos mitades cronológicas en el límite de bout completo más cercano al 50% de los frames del contexto `co2_off`. La dirección temprana→tardía y la inversa se promedian por trial; el null mezcla únicamente las etiquetas entre slots dentro de cada mitad y segmento `co2_off`.

## Por qué

Los datos tienen siete segmentos `co2_off` disjuntos por trial. Un null que mezclara tokens entre segmentos cambiaría el contexto experimental y sería demasiado permisivo. La primera versión local hizo exactamente eso y quedó descartada.

La primera versión publicada todavía tenía un defecto de contrato: barajaba pares `label+length` pero dejaba el vector ROI del slot intacto. Eso podía producir un registro cuyo metadata declaraba una longitud distinta de la usada para calcular su vector. El falsador reprodujo el mismatch. La corrección baraja solo labels dentro de cada segmento, preservando la longitud y el vector de cada slot, y destruyendo únicamente la alineación label→ROI.

## Instrumento y QA

- `tools/h4_temporal_halves.py`
- `tests/test_h4_temporal_halves.py`
- seis contratos totales: rechazo de `Frame`, rechazo de animales mezclados, reproducibilidad, bouts completos, preservación por segmento y preservación de longitud/vector por slot;
- suite completa: 7 alignment + 6 loader + 7 features + 5 block-null + 4 generalization + 5 temporal = **34 tests OK**;
- corrida real en `brain-env`, 8 trials, `walking/resting`, `co2_off`, 999 permutaciones, seed `20261002`;
- repetición real byte a byte idéntica.

## Resultado corregido

```text
animal=R65D11-tdTomGC6fopt-fly1
n_trials=8
observed_bidirectional_transfer=0.5327595514498719
null_mean=0.5018239610724393
null_sd=0.019476626168946264
p_greater_equal=0.055
z=1.588344413918904
raw_result_sha256=c2c0e2f2093bc85650daa6bb487b8dcd4bf1ae38278d64de24fd040abb202d98
```

El número no cambió porque el defecto anterior alteraba metadata que el score no consultaba; eso no lo hacía aceptable. Ahora el contrato y la ejecución coinciden.

## Veredicto y límites

El instrumento está **BIEN**, pero el resultado pooled es **NO EVIDENCIA ROBUSTA** por encima del null al umbral one-sided 0.05: `p=0.055`. Es sugestivo, no positivo; no refuta H4 y tampoco confirma H4 fuerte. Los ocho trials son del mismo animal. Esto mide transferencia descriptiva de features ROI, no mapping anatómico, selección de ruta ni causalidad.

La alineación sigue fail-closed: `Frame` es rechazado y ningún bout se corta. H4 fuerte sigue **NO MEDIDA** hasta mapping anatómico, null anatómico pareado y silenciamiento causal.
