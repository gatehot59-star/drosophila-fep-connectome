# Recibo 013: estabilidad temporal por mitades

## Pedido

Reintentar la corrida usando GitHub como canal de transferencia después de que la transferencia directa al `brain-env` fallara.

## Canal y ejecución

- Instrumento transferido por GitHub a `titan/h4-temporal-halves-2026-10-02`.
- Rama base de transferencia: `titan/h4-generalization-2026-10-02`.
- Checkout del `brain-env` actualizado por `git fetch` y verificado en commit `1e6de6a3d5089481e552943ddabf857f19996604`.
- Tests de contrato: **5 OK**.
- Corrida real: 8 trials, un animal, `walking/resting`, `co2_off`, 999 permutaciones, seed `20261002`.
- Repetición real: mismo JSON byte a byte, SHA `01c5d9cf25112e84e4da772aa5fa70c1478aa20aa3555fcbccdc638ec0fec43e2`.

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

Early→late y late→early, por trial:

```text
1: 0.45833333333333337 -> 0.4375
2: 0.6625              -> 0.4375
3: 0.43333333333333335 -> 0.49090909090909096
4: 0.5580357142857143  -> 0.6390374331550802
5: 0.41964285714285715 -> 0.5735294117647058
6: 0.5138888888888888  -> 0.6196172248803828
7: 0.6216577540106951  -> 0.6333333333333333
8: 0.5445652173913043  -> 0.4807692307692308
```

## Veredicto

**NO EVIDENCIA ROBUSTA DE ESTABILIDAD TEMPORAL POOLED** al umbral one-sided 0.05: `p=0.055`. Es un resultado sugestivo, no una confirmación; no refuta H4 y no convierte los ocho trials de un solo animal en evidencia cross-animal.

## Corrección importante

El primer smoke test local fue descartado porque mezclaba tokens entre los siete segmentos `co2_off` de cada trial. El instrumento corregido permuta dentro de cada mitad de cada segmento y agrega un contrato específico para impedir esa mezcla.

## Evidencia publicada

- `tools/h4_temporal_halves.py`
- `tests/test_h4_temporal_halves.py`
- `results/h4_temporal_halves_summary.json`
- `results/h4_temporal_halves_run.log`
- `docs/adr/2026-10-03-h4-temporal-halves.md`

El JSON completo de 257247 bytes y la distribución pooled exacta quedan retenidos en `brain-env` bajo el SHA publicado en el summary; el summary y el recibo son la superficie pública actual. Mapping anatómico, null anatómico pareado, SparseLTC sobre subgrafos y silenciamiento causal siguen **NO MEDIDOS**.
