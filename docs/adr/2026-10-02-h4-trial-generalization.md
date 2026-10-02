# ADR: generalización H4 entre trials dentro de un animal

**Fecha:** 2026-10-02  
**Estado:** aceptada como medición descriptiva; no cierra H4 fuerte

## Decisión

Agregar `tools/h4_trial_generalization.py` para medir leave-one-trial-out sobre bouts de `ROI_0`/`ROI_1`, usando solo los ocho trials alineados del animal `R65D11-tdTomGC6fopt-fly1`. El clasificador es nearest-centroid y la métrica es balanced accuracy por bout para `walking` y `resting`, las acciones con soporte suficiente en todos los trials.

El null permuta tokens completos dentro de cada segmento `co2_off` del trial de prueba. Conserva identidad, contexto, longitudes de bouts, conteos por label y orden temporal de las ROI; destruye la correspondencia entre label y señal neural.

## Por qué no se llama cross-animal

Los ocho trials disponibles tienen el mismo animal. El instrumento falla cerrado si recibe más de un animal. Una buena predicción entre estos trials solo mide generalización intra-animal entre sesiones, no transferencia biológica entre individuos.

## Qué evita

- No une por `Frame`.
- No trata frames consecutivos como muestras independientes.
- No usa `roi_dFF_2p.pkl`.
- No convierte balanced accuracy en causalidad.
- No declara mapping anatómico; las ROI siguen sin cell type/FlyWire verificable.

## Próximo bloque

Después de esta medición: estabilidad temporal por mitades usando bouts completos, mapping ROI→anatomía, null pareado y silenciamientos cruzados.
