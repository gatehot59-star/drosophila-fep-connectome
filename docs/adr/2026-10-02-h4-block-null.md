# ADR: null por bouts para la primera repetición H4 alineada

**Fecha:** 2026-10-02  
**Estado:** aceptada para medición descriptiva, no para cerrar H4

## Contexto

El loader y las features ROI-preserving ya pasan los ocho trials de Aymanns. Los ocho pertenecen al mismo animal `R65D11-tdTomGC6fopt-fly1`. El siguiente instrumento no puede volver a tratar frames consecutivos como observaciones independientes ni mezclar `Frame` de relojes diferentes.

## Decisión

Implementar `tools/h4_block_null.py` con un estadístico descriptivo de separación entre labels de conducta en el espacio de las ROI, calculado sobre medias por bout. El null permuta tokens completos `(label, longitud)` dentro de cada segmento contiguo de `co2_off` de cada trial.

El contrato conserva:

- identidad de animal y trial;
- límites y cantidad de frames de cada segmento de contexto;
- multiconjunto exacto de longitudes de bouts;
- cantidad de bouts y frames por label;
- valores ROI y orden temporal de la señal.

El null destruye el orden original de bouts y la alineación label-señal, que es la cantidad que se quiere falsar. La métrica es eta-cuadrado multivariado, con cada bout como unidad de peso igual y ROI normalizadas por la distribución completa del trial.

## Alternativas descartadas

1. **Shuffle por frame:** descartado porque rompe autocorrelación, tamaños de bout y transición temporal.
2. **Shuffle global entre trials:** descartado porque confunde trial y animal, y los ocho trials no son ocho animales.
3. **Permutar solo nombres de label y conservar longitud del destino:** descartado porque cambia la cantidad de frames por label y deja un null que no conserva la estructura observada.
4. **Clasificador como veredicto principal:** descartado en esta fase; una accuracy positiva sería decodificación, no selección causal de rutas.
5. **Mapping anatómico dentro de este PR:** descartado porque todavía no existe el mapping ROI→cell type/FlyWire verificable.

## Límites

Este instrumento solo mide separación descriptiva a nivel ROI, dentro de un animal y entre trials. No demuestra H4 fuerte, no prueba cross-animal, no identifica rutas anatómicas y no ejecuta silenciamiento causal. Un resultado positivo conserva el estado **H4 fuerte: NO MEDIDA** hasta superar null anatómico y causal gate.

## Verificación

```text
python3 -S tests/test_h4_block_null.py
python3 -S tools/h4_block_null.py \
  --input <trial-1.jsonl> ... --input <trial-8.jsonl> \
  --context co2_off \
  --labels walking,resting,head_grooming,foreleg_grooming,hind_grooming \
  --min-bouts 2 --permutations 999 --seed 20261002 \
  --out results/h4_block_null_co2_off_8_trials.json
```

El resultado crudo completo incluye hashes de los ocho JSONL, todos los scores nulos y la tabla de preservación. El workflow CI no se modifica en esta decisión: cambiar workflows requiere aprobación separada; el contrato se ejecuta localmente en `brain-env` y queda pendiente incorporar el test al CI.
