# CONTEXTO VIVO · conectoma / FEP / H4

**Última actualización:** 2026-10-03 00:22 (America/Buenos_Aires)  
**Estado canónico:** `main` auditado en `a4f5a8e9143173bf609eff430bcca3d5d8699c48`.

## Veredicto operativo

**H4 fuerte: NO MEDIDA.** La cadena de instrumentos H4 está materializada y auditada, pero no demuestra mapping anatómico ni causalidad. H4 débil queda refutada solo en su alcance estrecho de poblaciones anotadas.

## Estado confirmado en main

- Alignment guard: 7 contratos.
- Loader oficial: 6 contratos; 8/8 trials Aymanns reales con manifests `BIEN` en la corrida original.
- Features ROI/contexto/bouts: 7 contratos; 8/8 trials materializados en la corrida original.
- Null por bouts: 5 contratos; distribución pooled exacta de 999 scores publicada.
- Generalización intra-animal: 4 contratos; resultado descriptivo `balanced accuracy=0.5018855395873556`, `p=0.623`, no evidencia de generalización entre trials.
- Estabilidad temporal: 5 contratos; `observed=0.5327595514498719`, `p=0.055`, sugestivo pero no positivo.
- Regresión integrada: 34 contratos pasaron en el head pre-merge `646c0343c7b8aa28d7ee6d2395e2e34465a07b92`; la auditoría independiente señaló que el SHA final anterior no tenía check propio.
- Auditoría main final: `docs/auditorias/2026-10-02-004-auditoria-main-final-34-contratos.md`, score 36/40.

## Estado de producto y ciencia

SparseLTC, DualBrain y DBC3 son trabajo propio de Abraham. SparseLTC→DBC3 sobre señal biológica real, mapping ROI→FlyWire/cell type/neuropilo, null anatómico pareado y silenciamiento causal siguen **NO MEDIDOS**. ComplexVectorLTC queda experimental hasta demostrar una tarea donde fase/acoplamiento IQ sean necesarios.

## Próximos pasos

1. Verificar el check post-merge de este cambio sobre `main`.
2. Mantener separados contratos de instrumentos y claims biológicos.
3. Mapear ROI→anatomía y construir null anatómico pareado.
4. Ejecutar SparseLTC sobre un subgrafo real, con perturbación y puente DBC3 separado.

## Fuentes

- `docs/auditorias/2026-10-02-004-auditoria-main-final-34-contratos.md`
- `docs/agents/respuestas/2026-10-02-011-h4-exact-distribution-published.md`
- `docs/agents/respuestas/2026-10-02-012-h4-trial-generalization.md`
- `docs/agents/respuestas/2026-10-02-013-h4-temporal-halves.md`

## NO MEDIDO

- Corrida biológica end-to-end post-merge.
- Mapping anatómico, null anatómico y causalidad.
- Equivalencia SparseLTC→DBC3 sobre señal real.
- Review externo del pipeline; silencio no es aprobación.

--- METODO TITAN ---
Accion delicada: SI
Modo aplicado: TITAN FULL
Rubrica: 92/100
N/A declarados: deployment y producto no aplican; CI y contexto sí
Review externo: pendiente; silencio no es aprobación
Instrumento: GitHub Actions sobre main/titan, fuentes de seis suites y auditoría independiente
Evidencia: SHA `a4f5a8e9143173bf609eff430bcca3d5d8699c48`, commits y recibos citados arriba
