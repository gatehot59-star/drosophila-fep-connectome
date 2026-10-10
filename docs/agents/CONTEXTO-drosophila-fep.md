# CONTEXTO VIVO · conectoma / paper / H4

**Última actualización:** 2026-10-10 10:15 (America/Buenos_Aires)  
**Estado canónico:** `main` con las respuestas 002 y 003 del 10-oct. H4 auditado en `a4f5a8e9143173bf609eff430bcca3d5d8699c48`.

## Veredicto operativo

- **Paper, reciprocidad:** la Tabla 7 ya es reproducible (script reconstruido, PR #26 sin merge). El gradiente hacia el motor sobrevive al umbral ≥5. Falta el nulo por circuito y el test de tendencia para que el pivote deje de ser descriptivo.
- **H4 fuerte: NO MEDIDA.** La cadena de instrumentos H4 está materializada y auditada, pero no demuestra mapping anatómico ni causalidad. H4 débil queda refutada sólo en su alcance estrecho de poblaciones anotadas.

## Paper y Tabla 7 (respuesta 002)

- Script: `tools/table7_reciprocity_by_class.py` en `titan/tabla7-reconstruida-2026-10-10` (commit `1f66456`), PR #26.
- Con las anotaciones vivas en marzo (`c03ad46`): L3 16/16 exactas y Tabla 7 publicada 8/8. Con el pin `17fc577`: 10/16, por recambio de `root_id` (14 y 18), con 0 cambios de `super_class`.
- El 8,7% sensory→descending publicado es doble redondeo: 2.104/24.327 = 8,6488%, o sea 8,6.
- Umbral ≥5: 2.700.513 aristas y 13,98% (igual al ítem 5 del erratum). Tabla 7 con ≥5: intra-sensory 37,5; intra-motor 35,0 (80 aristas); intra-visual centrifugal 23,4; intra-optic 17,1; sensory→central 13,8; sensory→descending 2,8; sensory→motor 1,3; optic→motor sin aristas.
- Espera decisión de Abraham: pasar el ítem 9 y el 8,6 a `docs/ERRATUM.md` y a `docs/PIVOTE-RECIPROCIDAD.md`.
- Las `results/` de la Tabla 7 están sólo en el commit local `7117e45` de brain-env, que no tiene credencial de push para este repo.

## Estado confirmado en main (H4)

- Alignment guard: 7 contratos.
- Loader oficial: 6 contratos; 8/8 trials Aymanns reales con manifests `BIEN` en la corrida original.
- Features ROI/contexto/bouts: 7 contratos; 8/8 trials materializados en la corrida original.
- Null por bouts: 5 contratos; distribución pooled exacta de 999 scores publicada.
- Generalización intra-animal: 4 contratos; resultado descriptivo `balanced accuracy=0.5018855395873556`, `p=0.623`, no evidencia de generalización entre trials.
- Estabilidad temporal: 5 contratos; `observed=0.5327595514498719`, `p=0.055`, sugestivo pero no positivo.
- Regresión integrada: 34 contratos pasaron en el head pre-merge `646c0343c7b8aa28d7ee6d2395e2e34465a07b92`; la auditoría independiente señaló que el SHA final anterior no tenía check propio.
- Auditoría main final: `docs/auditorias/2026-10-02-004-auditoria-main-final-34-contratos.md`, score 36/40.

## Estado de producto y ciencia

SparseLTC, DualBrain y DBC3 son trabajo propio de Abraham. Medido en `mojo-absoluto`: en HC-2, SparseLTC empata 48/48 con el control lineal sobre FlyWire real (la no linealidad no ganó); en HC-3b, DBC3 aprende más rápido (AULC 0,823 contra 0,635) en una tarea, con el LR del borde de LSTM/GRU NO MEDIDO. SparseLTC→DBC3 sobre señal biológica real, mapping ROI→FlyWire/cell type/neuropilo, null anatómico pareado y silenciamiento causal siguen **NO MEDIDOS**. ComplexVectorLTC queda experimental y congelada: no ganó ninguna métrica IQ/radar.

## Próximos pasos

1. Nulo por circuito (CP/MS) y test de tendencia sobre la Tabla 7, en brain-env con `src/cp40.py` y el script de la Tabla 7.
2. Con eso, la v2 del erratum: ítem 9, el 8,6 y el gradiente bajo umbral. Decide Abraham.
3. Subir las `results/` de la Tabla 7 por la integración de GitHub o con una credencial propia de este repo.
4. H4 estacionada: mapping ROI→anatomía y null anatómico pareado recién después de cerrar el paper.
5. Mantener separados los contratos de instrumentos y los claims biológicos.

## Fuentes

- `docs/agents/respuestas/2026-10-10-002-tabla7-reconstruida.md`
- `docs/agents/respuestas/2026-10-10-003-hacia-donde-vamos-conectoma-y-celulas-liquidas.md`
- `docs/auditorias/2026-10-02-004-auditoria-main-final-34-contratos.md`
- `docs/agents/respuestas/2026-10-02-011-h4-exact-distribution-published.md`
- `docs/agents/respuestas/2026-10-02-012-h4-trial-generalization.md`
- `docs/agents/respuestas/2026-10-02-013-h4-temporal-halves.md`

## NO MEDIDO

- Nulo por circuito y test de tendencia de la Tabla 7.
- Cruce con la reciprocidad por neuropilo de Lin 2024.
- Corrida biológica end-to-end post-merge.
- Mapping anatómico, null anatómico y causalidad.
- Equivalencia SparseLTC→DBC3 sobre señal real.
- Review externo del pipeline; silencio no es aprobación.

--- METODO PROMETEO ---
Máquina: ninguna en esta actualización (lectura); la Tabla 7 corrió en brain-env.
Artefactos: `docs/agents/respuestas/2026-10-10-003-hacia-donde-vamos-conectoma-y-celulas-liquidas.md` + Doc https://app.clickup.com/90171457413/docs/2kza6fw5-20837
