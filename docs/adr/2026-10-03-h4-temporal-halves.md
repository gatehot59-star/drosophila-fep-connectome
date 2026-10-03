# ADR: estabilidad temporal por mitades de bouts

**Fecha:** 2026-10-03 UTC / 2026-10-02 ART  
**Rama de origen:** `titan/h4-temporal-halves-2026-10-02`

## Decisión

Medir la estabilidad temporal de la representación ROI separando cada trial en dos mitades cronológicas en el límite de bout completo más cercano al 50% de los frames del contexto `co2_off`. La dirección temprana→tardía y la inversa se promedian por trial; el null mezcla únicamente las etiquetas entre slots dentro de cada mitad y segmento `co2_off`.

## Corrección auditada

La primera versión local mezclaba tokens entre segmentos; la primera versión publicada además podía dejar metadata de longitud inconsistente con el vector del slot. El falsador reprodujo el mismatch. La corrección baraja solo labels dentro de cada segmento, preservando longitud y vector ROI de cada slot.

## Instrumento y resultado

`tools/h4_temporal_halves.py` y `tests/test_h4_temporal_halves.py`, 5 contratos en esta entrega. La corrida real de 8 trials, 999 permutaciones y seed `20261002` produjo `observed=0.5327595514498719`, `null_mean=0.5018239610724393`, `p=0.055`, `z=1.588344413918904`, con raw SHA-256 `c2c0e2f2093bc85650daa6bb487b8dcd4bf1ae38278d64de24fd040abb202d98`.

## Veredicto

El instrumento está BIEN, pero el resultado pooled es **NO EVIDENCIA ROBUSTA** al umbral one-sided 0.05. Es sugestivo, no positivo. H4 fuerte sigue NO MEDIDA; estos ocho trials son de un solo animal y no prueban anatomía ni causalidad.
