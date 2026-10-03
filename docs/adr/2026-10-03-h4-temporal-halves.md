# ADR: estabilidad temporal por mitades de bouts

**Fecha:** 2026-10-03 UTC / 2026-10-02 ART  
**Rama:** `titan/h4-temporal-halves-2026-10-02`

## Decisión

Medir la estabilidad temporal de la representación ROI separando cada trial en dos mitades cronológicas en el límite de bout completo más cercano al 50% de los frames del contexto `co2_off`. La dirección temprana→tardía y la inversa se promedian por trial; el null permuta tokens completos de label+longitud dentro de cada mitad de cada segmento `co2_off`.

## Por qué

Los datos tienen siete segmentos `co2_off` disjuntos por trial. Un null que mezclara tokens entre segmentos cambiaría el contexto experimental y sería demasiado permisivo. La primera versión local hizo exactamente eso; el smoke test lo detectó y quedó descartada. La versión publicada conserva límites, multiconjunto de longitudes y conteos label+longitud por medio segmento.

## Instrumento

- `tools/h4_temporal_halves.py`
- `tests/test_h4_temporal_halves.py`
- cinco contratos, incluido rechazo de `Frame`, rechazo de animales mezclados, reproducibilidad, bouts completos y preservación de tokens por segmento;
- corrida real en `brain-env`, 8 trials, `walking/resting`, `co2_off`, 999 permutaciones, seed `20261002`;
- repetición real byte a byte idéntica.

## Resultado

```text
animal=R65D11-tdTomGC6fopt-fly1
n_trials=8
observed_bidirectional_transfer=0.5327595514498719
null_mean=0.5018239610724393
null_sd=0.019476626168946264
p_greater_equal=0.055
z=1.588344413918904
```

Los límites por trial fueron:

| trial | early frames | late frames | early bouts | late bouts |
|---:|---:|---:|---:|---:|
| 1 | 3777 | 3433 | 33 | 29 |
| 2 | 3236 | 3974 | 26 | 38 |
| 3 | 3643 | 3568 | 35 | 40 |
| 4 | 3537 | 3674 | 40 | 38 |
| 5 | 3644 | 3567 | 45 | 37 |
| 6 | 3561 | 3650 | 45 | 39 |
| 7 | 3536 | 3675 | 40 | 49 |
| 8 | 3599 | 3612 | 43 | 50 |

## Veredicto y límites

El instrumento está **BIEN**, pero el resultado pooled es **NO EVIDENCIA ROBUSTA** por encima del null al umbral one-sided 0.05: `p=0.055`. Es sugestivo, no positivo; no refuta H4 y tampoco confirma H4 fuerte. Los ocho trials son del mismo animal. Esto mide transferencia descriptiva de features ROI, no mapping anatómico, selección de ruta ni causalidad.

La alineación sigue fail-closed: `Frame` es rechazado y ningún bout se corta. H4 fuerte sigue `NO MEDIDA` hasta mapping anatómico, null anatómico pareado y silenciamiento causal.
