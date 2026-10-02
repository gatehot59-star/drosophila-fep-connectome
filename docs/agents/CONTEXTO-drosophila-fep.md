# CONTEXTO VIVO · conectoma / FEP / H4

**Última actualización:** 2026-10-02 14:25 (America/Buenos_Aires)  
**Estado canónico:** este archivo se sobreescribe, no se acumula. La bitácora append-only vive en `docs/agents/respuestas/`.  
**Protocolo:** `docs/agents/00-PROTOCOLO-BITACORA-DE-RESPUESTAS.md`.  
**Auditoría anterior:** [docs/auditorias/2026-10-02-001-auditoria-proyecto-chat-h4.md](https://github.com/gatehot59-star/drosophila-fep-connectome/blob/main/docs/auditorias/2026-10-02-001-auditoria-proyecto-chat-h4.md).  
**Segunda auditoría:** [docs/auditorias/2026-10-02-003-segunda-auditoria-proyecto-chat-h4.md](https://github.com/gatehot59-star/drosophila-fep-connectome/blob/main/docs/auditorias/2026-10-02-003-segunda-auditoria-proyecto-chat-h4.md).  
**Doc público de cierre:** [H4 cerrado correctamente: fuerte NO MEDIDA, pipeline bloqueado por reloj](https://app.clickup.com/90171457413/docs/2kza6fw5-17737).  
**Doc público de segunda auditoría:** [Segunda auditoría H4: GitHub main correcto, brain-env atrasado](https://app.clickup.com/90171457413/docs/2kza6fw5-17757).

## 0. Veredicto operativo

**H4 fuerte queda NO MEDIDA.** No está confirmada ni refutada. La pregunta fuerte es: bajo contexto/estímulo comparable y con acciones alternativas, ¿la red activa y desactiva rutas distintas?

**H4 débil queda REFUTADA en su alcance estrecho:** el runner sobre poblaciones anotadas de escape, grooming y feeding produjo perfiles casi idénticos entre condiciones. Eso no usa conducta neural contextual real y no decide H4 fuerte.

**No se cierra H4 como descubrimiento biológico. Se cierra el expediente de esta fase con el estado correcto y un bloqueo técnico explícito.**

## 1. Qué queda validado

- La auditoría de features identificó correctamente el error principal del pipeline.
- Los ocho trials Aymanns aportan actividad neural y conducta con acciones alternativas descriptivas.
- La señal intra-animal anterior es solo descriptiva hasta corregir el reloj, el diseño de features y los nulls.
- Los hallazgos anatómicos previos del conectoma siguen siendo evidencia de capacidad/restricción estructural, no de selección contextual dinámica.

## 2. Qué queda invalidado o retirado

Los siguientes resultados no son evidencia biológica y no deben citarse como tales:

- cross-animal `balanced accuracy 0,1816` frente a shuffle `0,2019`;
- estabilidad temporal `early_to_late` y `late_to_early`;
- cualquier conclusión de que la representación no generaliza entre animales o es temporalmente inestable.

La causa está medida: los runners `h4_cross_animal.py` y `h4_temporal_stability.py` de la rama H4 usaron `roi_dFF_2p.pkl` y unieron por el entero `Frame`.

```text
conducta:       54.000 frames, Frame 0..53.999
roi_dFF_2p:       8.767/8.768 frames, Frame 0..8.766/8.767
DFF Time:         0..539,65 s
```

Eso mezcla el reloj de 2P con el reloj conductual y produce un desfase aproximado de 6,16x. **No demuestra biología inestable; demuestra un instrumento mal alineado.**

## 3. Estado de los instrumentos

| Instrumento | Estado | Veredicto |
|---|---|---|
| [`h4_actions.py`](https://github.com/gatehot59-star/drosophila-fep-connectome/blob/titan/auditoria-hipotesis-2026-10-01/tools/h4_actions.py) | ejecutado sobre conectoma/anotaciones | H4 débil refutada en su alcance estrecho |
| [`h4_neural_behavior_all.py`](https://github.com/gatehot59-star/drosophila-fep-connectome/blob/titan/auditoria-hipotesis-2026-10-01/tools/h4_neural_behavior_all.py) | ocho trials Aymanns | screening descriptivo; no H4 fuerte |
| [`h4_cross_animal.py`](https://github.com/gatehot59-star/drosophila-fep-connectome/blob/titan/auditoria-hipotesis-2026-10-01/tools/h4_cross_animal.py) | merge por `Frame` incompatible | resultados biológicos invalidados |
| [`h4_temporal_stability.py`](https://github.com/gatehot59-star/drosophila-fep-connectome/blob/titan/auditoria-hipotesis-2026-10-01/tools/h4_temporal_stability.py) | merge por `Frame` incompatible | resultados biológicos invalidados |
| [`h4_timealigned_features.py`](https://github.com/gatehot59-star/drosophila-fep-connectome/blob/titan/auditoria-hipotesis-2026-10-01/tools/h4_timealigned_features.py) | interpolación parcial | no concluyente; no equivale al loader oficial |

## 4. Features: límite de categoría

Las nueve estadísticas globales por frame (media, desviación, mínimo, máximo, mediana y cuantiles) sirven como control de señal global, pero eliminan identidad ROI, signo individual, fase, posición anatómica y módulo causal. Una clasificación positiva con estas features solo demostraría señal decodificable, no activación/desactivación de rutas.

Las labels DAART son predicciones, no una anotación manual independiente. `co2_off` es un contexto amplio. Los frames consecutivos no son observaciones independientes y el shuffle simple no preserva bouts, transiciones ni autocorrelación.

## 5. Bloqueos que deben cerrarse antes de interpretar H4

1. Usar `roi_dFF.pkl` o el loader oficial Aymanns, no `roi_dFF_2p.pkl` para el cruce directo.
2. Implementar `alignment_guard` para animal, trial, reloj, monotonía de `Time`, cobertura y pérdidas.
3. Agregar prueba negativa: un merge por `Frame` con relojes incompatibles debe fallar con exit distinto de cero.
4. Repetir cross-animal y temporal por bouts/trials, con nulls por bloques temporales y balance de clases.
5. Conservar identidad anatómica y mapear ROIs a FlyWire/cell type o declarar el resultado como señal global.
6. Solo después ejecutar SparseLTC sobre el subgrafo real, null anatómico pareado y silenciamientos cruzados.

## 6. Estado de publicación y ramas

- Rama de trabajo H4: `titan/auditoria-hipotesis-2026-10-01`.
- HEAD auditado: `6112bdd25daf29d68e83d96eecd5f802d0fe8920`.
- `main` conserva la bitácora, la auditoría y este contexto actualizado, pero no incorpora la rama científica H4.
- No hay PR abierto desde la rama H4. Los PR existentes son históricos y no deben tratarse como entrega H4.
- La auditoría independiente está en `main`; los instrumentos y recibos H4 están anclados arriba a la rama auditada.

## 7. Fuentes canónicas de esta fase

- [`recibo 072`](https://github.com/gatehot59-star/drosophila-fep-connectome/blob/titan/auditoria-hipotesis-2026-10-01/docs/agents/respuestas/2026-10-02-072-falsador-neural-8-trials-Aymanns.md)
- [`recibo 073`](https://github.com/gatehot59-star/drosophila-fep-connectome/blob/titan/auditoria-hipotesis-2026-10-01/docs/agents/respuestas/2026-10-02-073-validacion-cross-animal-H4.md)
- [`recibo 074`](https://github.com/gatehot59-star/drosophila-fep-connectome/blob/titan/auditoria-hipotesis-2026-10-01/docs/agents/respuestas/2026-10-02-074-estabilidad-temporal-intra-animal.md)
- [`recibo 075`](https://github.com/gatehot59-star/drosophila-fep-connectome/blob/titan/auditoria-hipotesis-2026-10-01/docs/agents/respuestas/2026-10-02-075-auditoria-features-H4.md)
- [`recibo 002 de cierre`](https://github.com/gatehot59-star/drosophila-fep-connectome/blob/main/docs/agents/respuestas/2026-10-02-002-cierre-correcto-H4.md)

## 8. NO MEDIDO

- asset `roi_dFF.pkl` íntegro y loader oficial ejecutado de punta a punta;
- equivalencia manual versus loader oficial;
- `alignment_guard` y prueba negativa;
- rerun corregido cross-animal/temporal;
- mapping ROI→FlyWire/cell type;
- null anatómico pareado;
- causalidad por silenciamiento de rutas;
- robustez con más trials, bouts y controles de autocorrelación;
- review externo del pipeline H4.

## 9. Regla de cierre

Hasta que todos los bloqueos de la sección 5 tengan evidencia commiteada, **no se debe afirmar que H4 fue confirmada, refutada, generalizable o estable**. El único cierre correcto hoy es: **H4 fuerte NO MEDIDA; el pipeline anterior no es evidencia biológica; siguiente paso: alineación oficial con guard negativo.**

## 10. Rojo operativo agregado por la segunda auditoría

El checkout de `brain-env` no está sincronizado con GitHub `main` y no debe usarse para verificar el estado público actual hasta reconstruirse o sincronizarse desde el SHA público:

```text
checkout local HEAD: 08b3b01bc0a6c678ae09fe6adeabadfe6cd94b63
origin/main local:   08b3b01bc0a6c678ae09fe6adeabadfe6cd94b63
main GitHub:         ccf59eb8e359edf92539476bb81c8e1f0fd56752
```

El checkout local no contiene la auditoría 001, la auditoría 003 ni el recibo 002; su contexto todavía era de agosto. Toda medición nueva debe declarar primero el SHA exacto del checkout y compararlo con la fuente pública que pretende verificar.