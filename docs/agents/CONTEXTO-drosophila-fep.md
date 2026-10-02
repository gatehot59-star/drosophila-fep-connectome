# CONTEXTO VIVO · conectoma / FEP / H4

**Última actualización:** 2026-10-02 16:xx (America/Buenos_Aires)  
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

**No se cierra H4 como descubrimiento biológico.** Se cerró el bloqueo de alineación, no la hipótesis.

## 1. Qué queda validado

- La auditoría de features identificó correctamente el error principal del pipeline.
- Los ocho trials Aymanns aportan actividad neural y conducta con acciones alternativas descriptivas.
- El loader oficial ThorSync-equivalente pasó **8/8 trials reales** con el mismo contrato.
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

## 4. Resultado del alignment gate real

Animal: `R65D11-tdTomGC6fopt-fly1`. Timebase: `thor_sync_seconds`. Join: `Time`.

- 8/8 manifests `BIEN`.
- Cada trial: 7.440 frames de cámara, 1.067 frames 2P y 7.440 labels; 2 ROI.
- Error relativo de duración: `0,0029859–0,0030378`.
- Cobertura neural: `0,9969621–0,9970141`; cobertura conductual aproximadamente `1,0`.
- Etiquetas sin pareja: `0/8`.
- ROI con longitud incorrecta: `0/8`.
- Pérdidas de borde explícitas: 1 o 0 frames neurales antes del solapamiento y 4 después; nunca se ocultaron truncando.

El resumen versionado está en [`results/h4_all_trials_manifest_summary.json`](https://github.com/gatehot59-star/drosophila-fep-connectome/blob/titan/h4-official-loader-2026-10-02/results/h4_all_trials_manifest_summary.json). El recibo completo está en [`2026-10-02-006-h4-loader-all-trials.md`](https://github.com/gatehot59-star/drosophila-fep-connectome/blob/titan/h4-official-loader-2026-10-02/docs/agents/respuestas/2026-10-02-006-h4-loader-all-trials.md).

## 5. Features: límite de categoría

Las nueve estadísticas globales por frame sirven como control de señal global, pero eliminan identidad ROI, signo individual, fase, posición anatómica y módulo causal. Una clasificación positiva con ellas solo demostraría señal decodificable, no activación/desactivación de rutas.

Las labels DAART son predicciones, no una anotación manual independiente. `co2_off` es un contexto amplio. Frames consecutivos no son observaciones independientes y el shuffle simple no preserva bouts, transiciones ni autocorrelación.

## 6. Bloqueos que quedan antes de interpretar H4

1. Rehacer features conservando identidad ROI y, si existe, cell type/neuropilo.
2. Repetir cross-animal y temporal por bouts/trials, con nulls por bloques temporales y balance de clases.
3. Mapear ROIs a FlyWire/cell type o declarar explícitamente el resultado como señal global.
4. Construir null anatómico pareado con grado, neuropilo, distancia y signo.
5. Solo después ejecutar SparseLTC sobre el subgrafo real y hacer silenciamientos cruzados.

## 7. Estado de publicación y ramas

- Rama científica H4 histórica: `titan/auditoria-hipotesis-2026-10-01`, HEAD `6112bdd25daf29d68e83d96eecd5f802d0fe8920`.
- Rama de materialización base: `titan/materializacion-h4-guard-main-2026-10-02`.
- PR #7: alignment guard fail-closed, 2 checks verdes.
- PR #8: [loader oficial y manifest por trial](https://github.com/gatehot59-star/drosophila-fep-connectome/pull/8), encadenado sobre PR #7; contracts CI verde.
- El código nuevo sigue esperando decisión humana de merge.

## 8. Fuentes canónicas de esta fase

- [`recibo 002 de cierre`](https://github.com/gatehot59-star/drosophila-fep-connectome/blob/main/docs/agents/respuestas/2026-10-02-002-cierre-correcto-H4.md)
- [`recibo 004 informe maestro`](https://github.com/gatehot59-star/drosophila-fep-connectome/blob/main/docs/agents/respuestas/2026-10-02-004-informe-maestro-historial-conectoma.md)
- [`recibo 005 trial 7`](https://github.com/gatehot59-star/drosophila-fep-connectome/blob/titan/h4-official-loader-2026-10-02/docs/agents/respuestas/2026-10-02-005-h4-loader-trial7.md)
- [`recibo 006 ocho trials`](https://github.com/gatehot59-star/drosophila-fep-connectome/blob/titan/h4-official-loader-2026-10-02/docs/agents/respuestas/2026-10-02-006-h4-loader-all-trials.md)
- [`resumen de ocho manifests`](https://github.com/gatehot59-star/drosophila-fep-connectome/blob/titan/h4-official-loader-2026-10-02/results/h4_all_trials_manifest_summary.json)

## 9. NO MEDIDO

- Rerun biológico cross-animal/temporal con las alineaciones válidas.
- Features con identidad ROI/cell type/neuropilo.
- Null por bloques temporales y null anatómico pareado.
- Equivalencia manual versus loader oficial más allá de la reproducción del procedimiento ThorSync-equivalente.
- Causalidad por silenciamiento de rutas.
- SparseLTC sobre subgrafos observados.
- H4 fuerte como fenómeno biológico.
- Merge humano del PR #8 y de su base PR #7.

## 10. Entorno

El checkout de `brain-env` fue sincronizado y verificado antes de medir:

```text
HEAD=8bd12dca7bf1ca29bf8e98c101b053692077c31b
origin/main=8bd12dca7bf1ca29bf8e98c101b053692077c31b
```

Toda medición nueva debe declarar primero el SHA exacto del checkout y compararlo con la fuente pública que pretende verificar.

## 11. Regla de cierre

Hasta que los bloqueos de la sección 6 tengan evidencia commiteada, **no se debe afirmar que H4 fue confirmada, refutada, generalizable o estable**. Estado correcto: **alignment verificado en 8/8 trials; H4 fuerte NO MEDIDA; siguiente paso: features con identidad y nulls por bloques.**
