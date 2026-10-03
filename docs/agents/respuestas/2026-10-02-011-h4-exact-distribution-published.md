# Recibo 011: distribución pooled exacta publicada

## Pedido

Publicar la distribución íntegra y cerrar la deuda reproducible del rerun H4.

## Corrección importante

El primer intento de transporte en fragmentos JSON humanos quedó supersedido por un payload canónico binario exacto. No se debe usar `results/h4_block_null_co2_off_8_trials_pooled_distribution.json.part-*`; la fuente oficial es `results/h4_block_null_pooled_exact/`.

## Artefacto publicado

Se publicaron 999 scores pooled como 999 dobles IEEE-754 binary64, codificados en base64 y partidos en tres archivos. La reconstrucción es byte-exacta:

```text
raw_bytes=7992
raw_sha256=74eb80de8891a01660284e26fba0b4c4e3138d632359d0d34c836faf12a8f01f
count=999
observed=0.35831155721189717
null_mean=0.06104563938527175
null_sd=0.017371858516985278
p_greater_equal=0.001
z=17.11192372053771
```

## Veredicto

**Deuda reproducible cerrada para el estadístico pooled:** los 999 valores completos están públicos, con representación exacta, hash del payload y comando de reconstrucción. H4 fuerte sigue **NO MEDIDA**: esto es señal ROI descriptiva dentro de un animal, no mapping anatómico ni causalidad.

## NO MEDIDO

- Distribuciones nulas individuales por trial: no necesarias para el veredicto pooled publicado, no se presentan como publicadas.
- CI en Actions y merge humano del PR: pendientes.

--- METODO PROMETEO ---
Accion delicada: NO
Modo aplicado: FULL
Maquina: brain-env para la corrida; GitHub MCP para publicación
Rubrica: N/A (evidencia científica, no deployment)
N/A declarados: CI, mapping anatómico y causalidad fuera de este PR
Review externo: pendiente; silencio no es aprobación
Instrumento: `python3 -S tools/h4_block_null.py`, 999 permutaciones; payload f64 con SHA-256 y manifest en GitHub
Artefactos: `results/h4_block_null_pooled_exact/` + este recibo
