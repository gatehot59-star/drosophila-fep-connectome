# CONTEXTO VIVO · conectoma / FEP / H4

**Última actualización:** 2026-10-02 16:31 (America/Buenos_Aires)  
**Estado canónico:** este archivo se sobreescribe, no se acumula. La bitácora append-only vive en `docs/agents/respuestas/`.  
**Protocolo:** `docs/agents/00-PROTOCOLO-BITACORA-DE-RESPUESTAS.md`.  
**Auditoría anterior:** [docs/auditorias/2026-10-02-001-auditoria-proyecto-chat-h4.md](https://github.com/gatehot59-star/drosophila-fep-connectome/blob/main/docs/auditorias/2026-10-02-001-auditoria-proyecto-chat-h4.md).  
**Segunda auditoría:** [docs/auditorias/2026-10-02-003-segunda-auditoria-proyecto-chat-h4.md](https://github.com/gatehot59-star/drosophila-fep-connectome/blob/main/docs/auditorias/2026-10-02-003-segunda-auditoria-proyecto-chat-h4.md).  
**Plan de materialización:** [docs/PLAN-MATERIALIZACION-2026-10-02.md](https://github.com/gatehot59-star/drosophila-fep-connectome/blob/main/docs/PLAN-MATERIALIZACION-2026-10-02.md).  
**Doc público de cierre:** [H4 cerrado correctamente: fuerte NO MEDIDA, pipeline bloqueado por reloj](https://app.clickup.com/90171457413/docs/2kza6fw5-17737).  
**Doc público de segunda auditoría:** [Segunda auditoría H4: GitHub main correcto, brain-env atrasado](https://app.clickup.com/90171457413/docs/2kza6fw5-17757).  
**Doc público de materialización:** [Materialización H4: guard de alineación temporal y plan de producto](https://app.clickup.com/90171457413/docs/2kza6fw5-17817).

## 0. Veredicto operativo

**H4 fuerte queda NO MEDIDA.** No está confirmada ni refutada. La pregunta fuerte es: bajo contexto/estímulo comparable y con acciones alternativas, ¿la red activa y desactiva rutas distintas?

**H4 débil queda REFUTADA en su alcance estrecho:** el runner sobre poblaciones anotadas de escape, grooming y feeding produjo perfiles casi idénticos entre condiciones. Eso no usa conducta neural contextual real y no decide H4 fuerte.

**No se cierra H4 como descubrimiento biológico.** Se cerraron alineación y materialización de features, no la hipótesis.

## 1. Qué queda validado

- La auditoría de features identificó correctamente el error principal del pipeline.
- Los ocho trials Aymanns aportan actividad neural y conducta con acciones alternativas descriptivas.
- El loader oficial ThorSync-equivalente pasó **8/8 trials reales** con el mismo contrato.
- El materializador ROI/contexto/bouts pasó **8/8 trials**; trials 1 y 2 descartaron explícitamente un frame conductual fuera de cobertura neural.
- Los hallazgos anatómicos previos del conectoma siguen siendo evidencia de capacidad/restricción estructural, no de selección contextual dinámica.

## 2. Qué queda invalidado o retirado

No son evidencia biológica y no deben citarse como tales:

- cross-animal `balanced accuracy 0,1816` frente a shuffle `0,2019`;
- estabilidad temporal `early_to_late` y `late_to_early`;
- cualquier conclusión de que la representación no generaliza entre animales o es temporalmente inestable.

La causa está medida: el pipeline anterior usó `roi_dFF_2p.pkl` y unió por el entero `Frame`, mezclando conducta `54.000` frames con DFF `8.767/8.768` frames y un desfase aproximado de `6,16x`.

## 3. Estado de los instrumentos

| Instrumento | Estado | Veredicto |
|---|---|---|
| `h4_actions.py` | ejecutado sobre conectoma/anotaciones | H4 débil refutada en su alcance estrecho |
| `h4_neural_behavior_all.py` | ocho trials | screening descriptivo; no H4 fuerte |
| `h4_cross_animal.py` | merge por `Frame` incompatible | resultados biológicos invalidados |
| `h4_temporal_stability.py` | merge por `Frame` incompatible | resultados biológicos invalidados |
| `h4_timealigned_features.py` | interpolación parcial | no concluyente; no loader oficial |
| `h4_alignment_guard.py` | branch de materialización + CI | verde: 7 tests y mutación negativa detectada |
| `h4_official_loader.py` | brain-env, 8 trials reales | **8/8 BIEN, pérdidas explícitas y hashes** |
| `h4_aligned_features.py` | PR #9, 8 trials reales | **8/8 BIEN, ROI/contexto/bouts, CI verde** |

## 4. Resultado del alignment gate real

Animal: `R65D11-tdTomGC6fopt-fly1`. Timebase: `thor_sync_seconds`. Join: `Time`.

- 8/8 manifests `BIEN`.
- Cada trial: 7.440 frames de cámara, 1.067 frames 2P y 7.440 labels; 2 ROI.
- Error relativo de duración: `0,0029859–0,0030378`.
- Cobertura neural: `0,9969621–0,9970141`; cobertura conductual aproximadamente `1,0`.
- Etiquetas sin pareja: `0/8`.
- ROI con longitud incorrecta: `0/8`.
- Pérdidas de borde explícitas: nunca se ocultaron truncando.

## 5. Features materializadas, límite y siguiente prueba

Los ocho trials tienen JSONL derivados persistentes en `brain-env`, con:

- `ROI_0` y `ROI_1` preservadas por frame;
- CO2 `co2_on/co2_off` reconstruido sobre la cámara ThorSync;
- `bout_id`, posición y longitud por cambios de label/contexto;
- trials 1 y 2: `7.439` registros porque se descartó 1 frame conductual fuera de cobertura neural;
- trials 3 a 8: `7.440` registros;
- bouts: 69, 70, 82, 89, 94, 96, 102 y 106 respectivamente;
- cada JSONL tiene SHA-256 versionado en `results/h4_aligned_features_all_trials_summary.json`.

Esto **no es un clasificador** y no demuestra H4. Reemplaza las nueve estadísticas globales como instrumento principal porque conserva identidad ROI y deja construir nulls por bloques.

Las labels DAART son predicciones, no una anotación manual independiente. `co2_off` es un contexto amplio. Frames consecutivos no son observaciones independientes.

## 6. Bloqueos que quedan antes de interpretar H4

1. Repetir cross-animal y temporal por bouts/trials, con nulls por bloques y balance de clases.
2. Mapear ROIs a FlyWire/cell type o declarar explícitamente el resultado como señal global.
3. Construir null anatómico pareado con grado, neuropilo, distancia y signo.
4. Solo después ejecutar SparseLTC sobre el subgrafo real y hacer silenciamientos cruzados.

## 7. Estado de publicación y ramas

- Rama científica H4 histórica: `titan/auditoria-hipotesis-2026-10-01`, HEAD `6112bdd25daf29d68e83d96eecd5f802d0fe8920`.
- Rama de materialización base: `titan/materializacion-h4-guard-main-2026-10-02`.
- PR #7: alignment guard fail-closed, 2 checks verdes.
- PR #8: [loader oficial y manifest por trial](https://github.com/gatehot59-star/drosophila-fep-connectome/pull/8), contracts CI verde.
- PR #9: [features con identidad ROI, contexto y bouts](https://github.com/gatehot59-star/drosophila-fep-connectome/pull/9), contracts CI verde.
- El código nuevo sigue esperando decisión humana de merge.

## 8. Fuentes canónicas de esta fase

- [`recibo 002 de cierre`](https://github.com/gatehot59-star/drosophila-fep-connectome/blob/main/docs/agents/respuestas/2026-10-02-002-cierre-correcto-H4.md)
- [`recibo 004 informe maestro`](https://github.com/gatehot59-star/drosophila-fep-connectome/blob/main/docs/agents/respuestas/2026-10-02-004-informe-maestro-historial-conectoma.md)
- [`recibo 005 trial 7`](https://github.com/gatehot59-star/drosophila-fep-connectome/blob/titan/h4-official-loader-2026-10-02/docs/agents/respuestas/2026-10-02-005-h4-loader-trial7.md)
- [`recibo 006 ocho trials`](https://github.com/gatehot59-star/drosophila-fep-connectome/blob/titan/h4-official-loader-2026-10-02/docs/agents/respuestas/2026-10-02-006-h4-loader-all-trials.md)
- [`recibo 007 features trial 7`](https://github.com/gatehot59-star/drosophila-fep-connectome/blob/titan/h4-aligned-features-2026-10-02/docs/agents/respuestas/2026-10-02-007-h4-aligned-features-trial7.md)
- [`recibo 008 features ocho trials`](https://github.com/gatehot59-star/drosophila-fep-connectome/blob/titan/h4-aligned-features-2026-10-02/docs/agents/respuestas/2026-10-02-008-h4-aligned-features-all-trials.md)
- [`resumen de features ocho trials`](https://github.com/gatehot59-star/drosophila-fep-connectome/blob/titan/h4-aligned-features-2026-10-02/results/h4_aligned_features_all_trials_summary.json)

## 9. NO MEDIDO

- Rerun biológico cross-animal/temporal con las features válidas.
- Null por bloques temporales y null anatómico pareado.
- Equivalencia manual versus loader oficial más allá de la reproducción del procedimiento ThorSync-equivalente.
- Causalidad por silenciamiento de rutas.
- SparseLTC sobre subgrafos observados.
- H4 fuerte como fenómeno biológico.
- Merge humano de PR #9 y de sus PR base #8/#7.

## 10. Entorno

El checkout de `brain-env` fue sincronizado y verificado antes de medir:

```text
HEAD=8bd12dca7bf1ca29bf8e98c101b053692077c31b
origin/main=8bd12dca7bf1ca29bf8e98c101b053692077c31b
```

Toda medición nueva debe declarar primero el SHA exacto del checkout y compararlo con la fuente pública que pretende verificar.

## 11. Regla de cierre

Hasta que los bloqueos de la sección 6 tengan evidencia commiteada, **no se debe afirmar que H4 fue confirmada, refutada, generalizable o estable**. Estado correcto: **alignment verificado en 8/8 trials; features ROI/bouts verificadas en 8/8; H4 fuerte NO MEDIDA; siguiente paso: nulls por bloques y rerun biológico.**
