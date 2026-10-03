# Auditoría independiente de `main` final contra los 34 contratos H4

**Fecha:** 2026-10-02 ART / 2026-10-03 UTC  
**Sujeto:** `gatehot59-star/drosophila-fep-connectome`, rama `main`  
**SHA auditado:** `216ee5c39b775457502755a7194b0e26eee26c14`  
**SHA de la regresión ejecutada antes del merge:** `646c0343c7b8aa28d7ee6d2395e2e34465a07b92`

## Veredicto ejecutivo

**La estructura de los 34 contratos está en `main` y los 34 pasaron en el head del PR que introdujo el workflow. Pero no puedo firmar “34 tests ejecutados sobre el SHA final de `main`”: el SHA final tiene `0` check-runs propios.**

La diferencia no es cosmética. El head probado era el `main` anterior más un workflow de 41 líneas; el merge squash también agrega solo ese workflow. Eso permite confirmar equivalencia de contenido para esta entrega, pero el proceso no ejecutó el workflow después del merge. `main` queda **CONFIRMADO estructuralmente, NO MEDIDO como corrida directa post-merge**.

## Evidencia primaria

- Commit final de `main`: [`216ee5c`](https://github.com/gatehot59-star/drosophila-fep-connectome/commit/216ee5c39b775457502755a7194b0e26eee26c14), cuyo único archivo agregado es `.github/workflows/h4-integrated-regression.yml` con 41 líneas.
- Commit probado antes del merge: [`646c034`](https://github.com/gatehot59-star/drosophila-fep-connectome/commit/646c0343c7b8aa28d7ee6d2395e2e34465a07b92), también con el único archivo agregado de 41 líneas.
- Check-runs del head probado: dos ejecuciones `integrated-contracts`, ambas `completed / success`, sobre `646c0343`.
- Check-runs del SHA final `216ee5c`: `total_count=0`.
- Workflow final: `.github/workflows/h4-integrated-regression.yml`; su disparador `push` solo incluye `titan/**`, no `main`.

## Conteo estructural de los 34 contratos

| Suite | Archivo | Tests | Qué cubre |
|---|---|---:|---|
| Alignment | `tests/test_h4_alignment_guard.py` | 7 | caso válido, `Frame`, timebase, identidad faltante, monotonía, duración y overlap |
| Loader | `tests/test_h4_official_loader.py` | 6 | ROI iguales, ROI truncada, DFF vacío, `Frame`, identidad y gaps |
| Features | `tests/test_h4_aligned_features.py` | 7 | interpolación, extrapolación, cobertura, longitudes ROI, bouts, identidad ROI y longitudes |
| Block-null | `tests/test_h4_block_null.py` | 5 | `Frame`, animales mezclados, estadístico acotado, reproducibilidad y longitudes de bloques |
| Generalización | `tests/test_h4_trial_generalization.py` | 4 | centroides, `Frame`, animales mezclados y reproducibilidad/null pooled |
| Temporal | `tests/test_h4_temporal_halves.py` | 5 | `Frame`, animales mezclados, repetibilidad, score acotado y preservación por segmento |
| **Total** | 6 archivos | **34** | **7 + 6 + 7 + 5 + 4 + 5** |

Los seis archivos existen en `main`; sus contratos negativos pueden dar rojo por diseño. El workflow los invoca explícitamente con `python3 -S`, checkout pinneado y permisos `contents: read`.

## Hallazgos

### A1 · CONFIRMADO: el workflow cubre las seis suites

El archivo integrado invoca exactamente los seis runners y no depende de una etiqueta textual de resultado. El conteo de métodos `test_` en las fuentes da 34 y coincide con lo ejecutado en los dos check-runs del head del PR.

### A2 · CONFIRMADO: el head probado corresponde al contenido que entró

La comparación de commits muestra que tanto el head probado `646c0343` como el merge final `216ee5c` agregan únicamente el workflow integrado de 41 líneas. No hubo cambio de código de instrumentos ni de tests entre la corrida verde y el merge.

### A3 · ROJO DE PROCESO: `main` no tiene check propio post-merge

`GET /commits/216ee5c/check-runs` devuelve `total_count=0`. El motivo visible en el workflow es que el evento `push` solo escucha `titan/**`. Por eso la frase correcta es “34 contratos pasaron en el head pre-merge equivalente”, no “main final pasó 34 tests”.

### A4 · ROJO DOCUMENTAL: el contexto vivo quedó atrás del main final

`docs/agents/CONTEXTO-drosophila-fep.md` todavía enumera PRs #7/#8/#9 y dice que el código nuevo espera merge humano, aunque `main` ya contiene el pipeline integrado y el commit `216ee5c`. También conserva el estado de una fase anterior. El contexto no es una fuente confiable para el estado operativo actual hasta actualizarlo.

### A5 · ROJO DE HIGIENE: quedan PRs H4 supersedidos abiertos

Los PRs #10 y #11 siguen abiertos contra `main`, aunque sus reemplazos limpios #18 y #19 ya fueron mergeados y el tren terminó en #21. No rompe el árbol final, pero mantiene dos líneas falsas de trabajo vivo y puede inducir a auditar o mergear el objeto equivocado.

### A6 · NO MEDIDO: la regresión no es una validación biológica end-to-end

Los 34 contratos son suites de fixtures sintéticos y contratos de instrumentos. No ejecutan los ocho assets Aymanns reales, no prueban mapping `ROI → FlyWire/cell type/neuropilo`, no prueban null anatómico pareado, silenciamiento causal ni `SparseLTC → DBC3` sobre señal biológica. H4 fuerte permanece **NO MEDIDA**.

## Qué no se midió y era importante

1. Corrida directa de `integrated-contracts` sobre `main` SHA `216ee5c`.
2. Rerun biológico sobre los ocho trials reales desde el workflow final.
3. Mapping anatómico y null anatómico pareado.
4. Causalidad por silenciamiento y equivalencia SparseLTC/DBC3 sobre señal real.
5. Revisión externa del workflow; el silencio de review no es aprobación.

## Corrección prioritaria

1. Cambiar el disparador del workflow para incluir `main` en `push` o ejecutar un `workflow_dispatch` sobre el SHA final, y exigir un check directo del commit.
2. Actualizar `CONTEXTO-drosophila-fep.md` al SHA `216ee5c` y al estado real del tren H4.
3. Cerrar los PRs #10 y #11 como superseded, preservando sus reemplazos mergeados.
4. Mantener separado el claim de contratos verdes del claim científico: el pipeline está protegido; H4 fuerte no está confirmada.

## Scorecard del auditor

| Criterio | Puntos | Evidencia |
|---|---:|---|
| Completitud | 13/15 | main, workflow, seis suites, check-runs, contexto y PRs auditados; sin rerun local |
| Razonamiento | 10/10 | se separan head probado, SHA final, contratos y biología |
| Documentación | 9/10 | SHAs, conteos, hallazgos y límites explícitos; el archivo aún debe entrar a main |
| Proceso QA | 4/5 | API de commits/check-runs y lectura directa de fuentes; no hubo review externo ni corrida local |
| **Total** | **36/40 = 90/100** | **Auditoría aprobada con deuda; `main` no firmado como post-merge ejecutado** |

--- METODO TITAN ---
Accion delicada: NO
Modo aplicado: TITAN FULL
Rubrica: 36/40 -> 90/100
N/A declarados: seguridad, deployment y producto no aplican a esta auditoría del pipeline
Review externo: no pedido; deuda K-02 declarada
Instrumento: GitHub API (commits, árboles, archivos, PRs y check-runs), fuentes de seis suites y contexto vivo; no se ejecutó runtime local
Evidencia cruda: SHAs `216ee5c`, `646c034`, `total_count=0` en main y dos `success` en el head probado
NO MEDIDO: corrida directa post-merge, runtime local, rerun biológico, mapping anatómico, causalidad y review externo
