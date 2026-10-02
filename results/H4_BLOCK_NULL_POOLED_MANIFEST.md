# Manifest: distribución pooled íntegra del null H4

**Schema reconstruido:** `h4-block-null-pooled-distribution/v1`  
**Partes:** 4  
**Bytes reconstruidos:** 21930  
**SHA-256 reconstruido:** `eeca801431c440e3a0cb9ca6c3b1fc217408b662899d243ca3da65ffb937f176`

## Reconstrucción exacta

```sh
cat results/h4_block_null_co2_off_8_trials_pooled_distribution.json.part-* > /tmp/h4_block_null_co2_off_8_trials_pooled_distribution.json
sha256sum /tmp/h4_block_null_co2_off_8_trials_pooled_distribution.json
```

Debe devolver el SHA anterior. Validación estructural:

```sh
python3 -S -c 'import json; r=json.load(open("/tmp/h4_block_null_co2_off_8_trials_pooled_distribution.json")); assert r["schema"]=="h4-block-null-pooled-distribution/v1"; assert len(r["pooled"]["null_scores"])==999; assert r["pooled"]["p_greater_equal"]==0.001; print("OK",r["pooled"]["observed"],r["pooled"]["null_mean"],r["pooled"]["z"])'
```

## Hashes por parte

| parte | bytes | SHA-256 |
|---|---:|---|
| `part-01` | 6000 | `c5bd45144f2a66cbae1f2021cb566800529cbfbbd35ec3e3e8f7adb116824939` |
| `part-02` | 6000 | `6b7c811526e98efd149be99880dfbb5d93ec2dae0d7f36981351a68db865c9ee` |
| `part-03` | 6000 | `4ea8ae306f062dc50c25be7a64a9ffdd7c5d821bc8502829d54673b8c6e8dd01` |
| `part-04` | 3930 | `e30362838850a4da8902d8cb5a6b63cfefb1cbbf44844e880df880b0ee7b670f` |

## Contenido científico

- Animal: `R65D11-tdTomGC6fopt-fly1`.
- Trials: 8, todos del mismo animal.
- Contexto: `co2_off`.
- Permutaciones: 999, seed `20261002`.
- Unidad: bouts completos, permutados dentro de cada segmento de contexto.
- Score observado: `0.35831155721189717`.
- Null mean: `0.06104563938527175`.
- Null SD: `0.017371858516985278`.
- `p_greater_equal`: `0.001`.
- `z`: `17.11192372053771`.

La proyección publicada contiene la distribución pooled completa usada para el veredicto agregado. No convierte el resultado en causalidad ni en evidencia cross-animal.
