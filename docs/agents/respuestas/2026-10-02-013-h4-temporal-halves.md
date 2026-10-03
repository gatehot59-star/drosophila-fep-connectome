# Recibo 013: estabilidad temporal H4 por mitades

## Medición

Se ejecutó sobre ocho trials del animal `R65D11-tdTomGC6fopt-fly1`, usando bouts completos, dos ROI, contexto `co2_off`, 999 permutaciones y seed `20261002`.

```text
observed=0.5327595514498719
null_mean=0.5018239610724393
null_sd=0.019476626168946264
p_greater_equal=0.055
z=1.588344413918904
raw_sha256=c2c0e2f2093bc85650daa6bb487b8dcd4bf1ae38278d64de24fd040abb202d98
```

## Veredicto

**NO EVIDENCIA ROBUSTA DE ESTABILIDAD TEMPORAL POOLED**. Es sugestivo, no positivo. H4 fuerte permanece NO MEDIDA. El mapping anatómico, null anatómico pareado, causalidad y SparseLTC→DBC3 sobre señal real siguen pendientes.

## Corrección

El falsador reprodujo un defecto: la versión anterior mezclaba `label+length` pero conservaba el vector ROI del slot, una metadata inconsistente. Ahora solo se barajan labels; cada slot conserva length y vector.
