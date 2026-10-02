# Cierre correcto de H4

## 1. Pedido
Actualizar el contexto vivo y cerrar H4 correctamente.

## 2. Herramientas y máquina
GitHub API para leer `main`, la rama `titan/auditoria-hipotesis-2026-10-01`, recibos, runners y PRs. MUDH Gateway `build.run` en `brain-env` para comprobar el checkout y la disponibilidad de los assets H4. ClickUp para publicar el Doc espejo. No se gastó Kaggle, Actions ni runtime ajeno; esta entrega escribió documentación y estado, no código de producto.

## 3. Qué se verificó
- La rama H4 existe en `6112bdd25daf29d68e83d96eecd5f802d0fe8920`.
- `main` no contenía el trabajo H4 y no hay PR abierto desde esa rama.
- El recibo `2026-10-02-075-auditoria-features-H4.md` mide la incompatibilidad: conducta 54.000 frames, `roi_dFF_2p` 8.767/8.768 frames y DFF `Time` de 0 a aproximadamente 539,65 s.
- `h4_cross_animal.py` y `h4_temporal_stability.py` unen por `Frame`; esos relojes no son equivalentes.
- `h4_timealigned_features.py` interpola por tiempo, pero fija conducta como `Frame / 100.0` y no demuestra uso del asset oficial `roi_dFF.pkl` ni equivalencia con el loader oficial.
- El recibo 072 declara explícitamente que la alineación manual fue solo equivalente a `utils2p`; no hay comparación contra el loader oficial.
- Los recibos 073 y 074 deben conservarse como diagnósticos históricos del pipeline, no como resultados biológicos.

## 4. Evidencia cruda
```text
conducta: 54.000 frames, Frame 0..53.999
DFF roi_dFF_2p: 8.767/8.768 frames, Frame 0..8.766/8.767
DFF Time: 0..539,65 s
```

Fuente primaria: `docs/agents/respuestas/2026-10-02-075-auditoria-features-H4.md`. Auditoría independiente: `docs/auditorias/2026-10-02-001-auditoria-proyecto-chat-h4.md`.

## 5. Veredicto de tres estados
- **H4 débil: REFUTADA en su alcance estrecho.** Las poblaciones anotadas por acción no produjeron rutas diferenciadas; esto no usa conducta neural contextual real.
- **Cross-animal y estabilidad temporal anteriores: INVALIDADOS como evidencia biológica.** El número `0,1816 vs 0,2019` y los deltas temporales no dicen que la biología no generaliza o sea inestable.
- **H4 fuerte: NO MEDIDA.** Sigue sin probarse activación/desactivación de rutas bajo contexto comparable y acción alternativa.
- **Features de nueve estadísticas: control global solamente.** No pueden demostrar rutas, identidad anatómica ni causalidad.

## 6. Archivos generados
- `docs/agents/respuestas/2026-10-02-002-cierre-correcto-H4.md`
- `docs/agents/CONTEXTO-drosophila-fep.md`
- Doc espejo: [H4 cerrado correctamente: fuerte NO MEDIDA, pipeline bloqueado por reloj](https://app.clickup.com/90171457413/docs/2kza6fw5-17737)

## 7. NO MEDIDO
Loader oficial ejecutado de punta a punta; `alignment_guard` y su prueba negativa; rerun temporalmente alineado; mapping ROI→FlyWire/cell type; null anatómico pareado; silenciamiento causal; revisión externa del pipeline H4.

## Próximo orden
Loader oficial + guard negativo; rerun por bouts/trials con nulls por bloques; features con identidad anatómica; SparseLTC y silenciamientos. No interpretar más H4 antes de eso.

--- METODO PROMETEO ---
Accion delicada: NO
Modo aplicado: FULL
Maquina: brain-env (verificación) + API de GitHub (lectura/escritura de bitácora) + ClickUp (Doc público)
Rubrica: N/A (actualización de estado y cierre científico, sin código ni despliegue)
N/A declarados: seguridad, deployment, testing de producto y CI no aplican
Review externo: no pedido; la auditoría independiente previa queda como evidencia y no como aprobación del rerun
Instrumento: GitHub API + MUDH Gateway `build.run`; evidencia en los archivos y URLs indicados
Artefactos: `docs/agents/respuestas/2026-10-02-002-cierre-correcto-H4.md` + `docs/agents/CONTEXTO-drosophila-fep.md` + https://app.clickup.com/90171457413/docs/2kza6fw5-17737