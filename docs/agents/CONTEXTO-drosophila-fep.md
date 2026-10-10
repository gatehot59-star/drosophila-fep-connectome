# CONTEXTO VIVO · conectoma / paper / H4

**Última actualización:** 2026-10-10, tarde (America/Buenos_Aires), con la respuesta 006  
**Estado canónico:** `main` con las respuestas 002 a 006 del 10-oct. H4 auditado en `a4f5a8e9143173bf609eff430bcca3d5d8699c48`.

## Veredicto operativo

- **Paper, reciprocidad:** la Tabla 7 ya es reproducible (script reconstruido, PR #26 sin merge). El gradiente hacia el motor sobrevive al umbral ≥5, y el embudo de salida entero tiene poca vuelta. Falta el nulo por circuito y el test de tendencia para que el pivote deje de ser descriptivo.
- **Quién controla las salidas (005 y 006):** el central pone el 60–73% de la entrada de las tres salidas; las descendentes, el 21–22% de la de las motoras; las ascendentes, el 16–20% de la de las neurosecretoras; el óptico, menos del 0,5%. Con el nulo fuerte de la 006 (10.000 permutaciones de etiquetas dentro de estratos de tamaño) se sostiene, pero el central gana por menos: ×1,5–2,3 sobre neuronas del mismo tamaño. Descendentes → motoras ×20; ascendentes → neurosecretoras ×10; la insulina (IPC) se cae; la proyección visual llega a las descendentes por debajo del azar (×0,64–0,68) y lo sensorial a las descendentes es azar (×0,96–1,04).
- **H4 fuerte: NO MEDIDA.** La cadena de instrumentos H4 está materializada y auditada, pero no demuestra mapping anatómico ni causalidad. H4 débil queda refutada sólo en su alcance estrecho de poblaciones anotadas.

## Paper y Tabla 7 (respuestas 002, 004, 005 y 006)

- Script: `tools/table7_reciprocity_by_class.py` en `titan/tabla7-reconstruida-2026-10-10` (commit `1f66456`), PR #26.
- Con las anotaciones vivas en marzo (`c03ad46`): L3 16/16 exactas y Tabla 7 publicada 8/8. Con el pin `17fc577`: 10/16, por recambio de `root_id` (14 y 18), con 0 cambios de `super_class`.
- El 8,7% sensory→descending publicado es doble redondeo: 2.104/24.327 = 8,6488%, o sea 8,6.
- Umbral ≥5: 2.700.513 aristas y 13,98% (igual al ítem 5 del erratum). Tabla 7 con ≥5: intra-sensory 37,5; intra-motor 35,0 (80 aristas); intra-visual centrifugal 23,4; intra-optic 17,1; sensory→central 13,8; sensory→descending 2,8; sensory→motor 1,3; optic→motor sin aristas.
- Embudo de salida (respuesta 004): 1.485 neuronas (1,07%; descending, motor y endocrine) reciben el 2,37% de los cables, el 61% de lo que llega a las descendentes viene del central, y lo que les llega tiene 13,19 / 9,83 / 3,58% de vuelta contra 26,60% global. Con ≥5, descending→motor: 2 de 1.569 (0,13%). Descriptivo, sin nulo.
- Qué salida controla cada clase (respuesta 005, `tools/output_control_by_class.py`, commit `7e75cde`). D1 es la fracción de la entrada en sinapsis, sin umbral / ≥5:
  - central → descendentes 60,23 / 62,42%, → motoras 64,34 / 65,54%, → neurosecretoras 73,03 / 67,88%;
  - descendentes → motoras 21,48 / 21,89% (cuello 40–43%, antena 32%, proboscis 25%);
  - ascendentes → neurosecretoras 15,93 / 20,31%;
  - óptico → descendentes 0,45 / 0,33%.
  - Cruce exacto con la Tabla 7. El nulo de destinos al azar da ~3% de falsos con etiquetas permutadas: se firma sólo lo que lo supera.
- Nulo fuerte por permutación (respuesta 006, `tools/output_control_permutation_null.py`, commit `c99494f`): dos nulos de R = 10.000, plano y estratificado por fuerza de salida, PASS en los dos umbrales. Calibrado: el control negativo da 7/4.840 y 4/4.620 flags contra 9,7 y 9,2 esperados (el nulo de destinos de la 005 daba ~3%). La primera corrida dio FAIL por un chequeo mío (z infinito con desvío 0); con la varianza exacta, mismos resultados y PASS.
- Espera decisión de Abraham: pasar el ítem 9 y el 8,6 a `docs/ERRATUM.md` y a `docs/PIVOTE-RECIPROCIDAD.md`.
- Las `results/` de la Tabla 7 y los JSON de la 005 y la 006 están sólo en brain-env (commit local `7117e45` y worktree `/workspace/dfc-t7`), que no tiene credencial de push para este repo. Los logs de la 004, la 005 y la 006 sí están en la rama.

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

1. Nulo por circuito (CP/MS) y test de tendencia sobre la Tabla 7 y el embudo de salida, en brain-env con `src/cp40.py` y el script de la Tabla 7.
2. Para la 006: un nulo de etiquetas que además conserve la región de origen, y corrección por comparaciones múltiples.
3. Con eso, la v2 del erratum: ítem 9, el 8,6 y el gradiente bajo umbral. Decide Abraham.
4. Subir las `results/` de la Tabla 7 por la integración de GitHub o con una credencial propia de este repo.
5. H4 estacionada: mapping ROI→anatomía y null anatómico pareado recién después de cerrar el paper.
6. Mantener separados los contratos de instrumentos y los claims biológicos.

## Fuentes

- `docs/agents/respuestas/2026-10-10-006-nulo-fuerte-por-permutacion.md`
- `docs/agents/respuestas/2026-10-10-005-que-salida-controla-cada-clase.md`
- `docs/agents/respuestas/2026-10-10-002-tabla7-reconstruida.md`
- `docs/agents/respuestas/2026-10-10-003-hacia-donde-vamos-conectoma-y-celulas-liquidas.md`
- `docs/agents/respuestas/2026-10-10-004-que-hay-al-final-de-cada-cable.md`
- `docs/auditorias/2026-10-02-004-auditoria-main-final-34-contratos.md`
- `docs/agents/respuestas/2026-10-02-011-h4-exact-distribution-published.md`
- `docs/agents/respuestas/2026-10-02-012-h4-trial-generalization.md`
- `docs/agents/respuestas/2026-10-02-013-h4-temporal-halves.md`

## NO MEDIDO

- Nulo por circuito y test de tendencia de la Tabla 7 y del embudo de salida.
- Nulo de etiquetas que además conserve la región de origen (la 006 conserva sólo el tamaño).
- Corrección por comparaciones múltiples en la 006 (~0,5 flags falsos esperados por umbral y por nulo).
- Signo real (fisiológico) por par de clases. La 005 midió sólo el signo predicho por neurotransmisor hacia las salidas.
- Cruce con la reciprocidad por neuropilo de Lin 2024.
- Corrida biológica end-to-end post-merge.
- Mapping anatómico, null anatómico y causalidad.
- Equivalencia SparseLTC→DBC3 sobre señal real.
- Review externo del pipeline; silencio no es aprobación.

--- METODO PROMETEO ---
Máquina: brain-env para la Tabla 7, el embudo, las salidas y el nulo fuerte; esta actualización es lectura.
Artefactos: `docs/agents/respuestas/2026-10-10-006-nulo-fuerte-por-permutacion.md` + Doc https://app.clickup.com/90171457413/docs/2kza6fw5-20897
