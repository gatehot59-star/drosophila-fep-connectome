# Selector H4 sobre todos los trials Aymanns

## Pedido
Run the trial selector across all Aymanns sessions.

## Datos e instrumento
Se procesaron los 8 trials del dataset `R65D11 two-photon recording data` de Aymanns. Para cada trial se descargaron/verificaron los H5 ThorSync y `capture_metadata.json`, y se cruzaron con las etiquetas `behaviour_predictions_daart.pkl`.

El selector usa este gate operativo: mismo estado de CO2 (`co2_on` o `co2_off`), al menos dos clases de acción entre walking/resting/head grooming/foreleg grooming/hind grooming y al menos 100 frames etiquetados en ese contexto. Esto es un **selector de candidatos**, no todavía una falsación causal.

## Evidencia cruda verbatim
```text
bytes 5518 md5 8ea98e0687d9a94a5a0226e463e093d9
n_trials 8 eligible [1, 3, 7, 4, 8, 5, 2, 6]
co2_on_eligible [1, 3, 7, 4, 8, 5, 6]
```

Conteos bajo `co2_off`, que es el contexto con mayor diversidad:

```text
trial 1: foreleg=116, head=363, resting=1939, walking=4766
trial 2: foreleg=34, head=211, hind=96, resting=1204, walking=5633
trial 3: foreleg=124, head=276, hind=17, resting=933, walking=5784
trial 4: foreleg=35, head=444, hind=43, resting=1618, walking=5031
trial 5: foreleg=207, head=377, hind=22, resting=1339, walking=5230
trial 6: foreleg=222, head=370, hind=58, resting=1504, walking=5047
trial 7: foreleg=70, head=315, hind=20, resting=1961, walking=4812
trial 8: foreleg=102, head=319, hind=14, resting=2199, walking=4544
```

Bajo `co2_on`, 7 trials tienen walking+resting como mínimo; trial 2 solo tiene walking y por eso no entra como contexto CO2-on elegible.

## Veredicto del selector
- **8/8 trials** pasan el gate en `co2_off`.
- **7/8 trials** pasan también en `co2_on`.
- Los mejores candidatos para acción alternativa bajo un contexto explícito son los 7 trials con `co2_on` y walking/resting; para diversidad conductual amplia, los 8 trials en `co2_off` contienen grooming, resting y walking.

## Límite importante
`co2_off` es un contexto real, pero amplio: no equivale automáticamente a “mismo estímulo sensorial”. La selección habilita el siguiente análisis neural, no demuestra H4. Falta correr el falsador sincronizado por trial sobre los 8 candidatos, usar split por trial/animal y después mapear las ROIs a identidades anatómicas. La causalidad por silenciamiento sigue NO MEDIDA.

## Archivos
- Selector: `tools/h4_trial_selector.py`, commit `3ca59eeb13cf0edb5801e1cee84137bc6930ccc1`.
- Resultado local: `/workspace/h4_data/aymanns/h4_trial_selection.json`, 5.518 bytes, md5 `8ea98e0687d9a94a5a0226e463e093d9`.
- Este recibo.

--- METODO TITAN ---
Accion delicada: NO
Modo aplicado: TITAN FULL
Rubrica: N/A (selector científico)
N/A declarados: deployment/security/CI no aplican; causalidad, mapping FlyWire y falsación final quedan NO MEDIDOS
Review externo: no pedido
Instrumento: MUDH Gateway build.run; 8 H5 + 8 metadata + 8 behavior files; JSON y md5 arriba
