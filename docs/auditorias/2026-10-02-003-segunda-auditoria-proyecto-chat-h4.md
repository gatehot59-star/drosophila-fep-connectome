# Segunda auditoría independiente del proyecto de este chat

**Fecha:** 2026-10-02 14:25 ART  
**Sujeto:** estado completo del chat H4 después del cierre y actualización de contexto  
**Rama científica:** `titan/auditoria-hipotesis-2026-10-01`, HEAD `6112bdd25daf29d68e83d96eecd5f802d0fe8920`  
**GitHub main auditado:** `ccf59eb8e359edf92539476bb81c8e1f0fd56752`  
**Auditoría anterior:** `docs/auditorias/2026-10-02-001-auditoria-proyecto-chat-h4.md`

## Veredicto

**El cierre científico de H4 es correcto, pero el proyecto sigue NO APROBADO como pipeline reproducible.** H4 fuerte queda **NO MEDIDA**; H4 débil queda **REFUTADA solo en su alcance estrecho**. No apareció ninguna medición nueva que permita subir esos estados.

La auditoría repetida confirma los rojos anteriores y encuentra uno operativo nuevo: **el checkout de `brain-env` está atrasado respecto de GitHub `main`**. El taller local está en `08b3b01`, mientras GitHub `main` ya está en `ccf59eb`; el archivo local de auditoría no existe y el contexto local todavía dice 2026-08-24. Por lo tanto, una corrida desde ese checkout no verifica el estado público actual.

## Hallazgos

### A1 · CONFIRMADO: el veredicto científico no fue inflado

GitHub `main` contiene el recibo `2026-10-02-002-cierre-correcto-H4.md` y el contexto actualizado. El texto mantiene la separación correcta:

- H4 débil: **REFUTADA en alcance estrecho**.
- Cross-animal y estabilidad temporal: **INVALIDADOS como evidencia biológica**.
- H4 fuerte: **NO MEDIDA**.

No hay evidencia nueva que autorice una conclusión más fuerte.

### A2 · CONFIRMADO: los instrumentos H4 siguen en una rama separada

La rama H4 existe y conserva HEAD `6112bdd`. No hay PR abierto cuyo head sea `titan/auditoria-hipotesis-2026-10-01`. Los PR #1, #2 y #3 son históricos y no convierten automáticamente los resultados H4 en una entrega pública reproducible.

### A3 · ROJO NUEVO: `brain-env` no está sincronizado con GitHub main

Medición en el checkout real:

```text
local HEAD:       08b3b01bc0a6c678ae09fe6adeabadfe6cd94b63
origin/main ref:  08b3b01bc0a6c678ae09fe6adeabadfe6cd94b63
audit file local: 0  (no existe)
context local:    Última actualización 2026-08-24 23:45
```

Medición en GitHub:

```text
main HEAD:        ccf59eb8e359edf92539476bb81c8e1f0fd56752
context SHA:      af0f02f0987727e3d2b55837ae9e65677d3bcd7f
```

El `origin/main` local también está atrasado, así que el checkout no es una copia fresca. Esto viola el criterio práctico de auditar el estado actual contra el repositorio y la máquina al mismo tiempo: el taller y la fuente pública describen proyectos distintos.

### A4 · ROJO CONFIRMADO: el error de reloj sigue sin reparación

El recibo 075 y los runners muestran conducta de 54.000 frames frente a `roi_dFF_2p` de 8.767/8.768 frames, con DFF `Time` de 0 a ~539,65 s. `h4_cross_animal.py` y `h4_temporal_stability.py` unen por el entero `Frame`. Los resultados `0,1816 vs 0,2019` y los deltas temporales siguen retirados como biología.

### A5 · ROJO DE DISEÑO: las features no responden H4 fuerte

Las nueve estadísticas globales destruyen identidad ROI, signo, fase y localización anatómica. Aunque el reloj se arregle, una clasificación positiva sería evidencia de señal decodificable, no de rutas activadas/desactivadas ni causalidad.

### A6 · NO MEDIDO: la equivalencia oficial sigue sin demostrarse

`h4_timealigned_features.py` usa interpolación parcial y `Frame / 100.0`; no prueba el asset oficial íntegro `roi_dFF.pkl`, ni compara contra el loader oficial, ni tiene `alignment_guard` con prueba negativa.

### A7 · NO MEDIDO: no hay H4 fuerte ejecutada correctamente

Siguen faltando contexto/estímulo compartido, acción alternativa bien balanceada, mapping ROI→FlyWire/cell type, null anatómico pareado, SparseLTC sobre el subgrafo real y silenciamientos cruzados.

### A8 · ROJO DE ENTREGA: no hay release reproducible de H4

La bitácora y el contexto están en `main`, pero los instrumentos científicos y recibos H4 permanecen en una rama no integrada y sin PR. Esto es una entrega documental correcta, no una release científica ejecutable.

## Qué no se midió y era importante

1. Sincronización del checkout de `brain-env` con el `main` público actual.
2. Loader oficial completo y comparación manual versus oficial.
3. Guard negativo contra merge por relojes incompatibles.
4. Rerun cross-animal/temporal con datos alineados.
5. Features anatómicamente comparables.
6. Nulls por bloques/bouts y controles de autocorrelación.
7. Causalidad de rutas mediante silenciamiento.
8. Revisión externa del pipeline H4.

## Orden obligatorio

Primero sincronizar o reconstruir el checkout desde el SHA público que se vaya a auditar. Después ejecutar loader oficial y `alignment_guard` negativo. Luego repetir por bouts/trials con nulls temporales. Solo después mapear anatomía, correr SparseLTC y probar silenciamientos. Hasta entonces, no interpretar H4 fuerte.

## Scorecard

| Criterio | Puntos | Evidencia |
|---|---:|---|
| Completitud | 11/15 | Se reauditaron estado público, rama H4, PRs, runners y checkout; faltan datos oficiales íntegros |
| Razonamiento | 10/10 | Se separan estados biológicos, validez del instrumento y entrega pública |
| Documentación | 9/10 | Evidencia cruda, SHAs y rutas; sin verificación del rerun |
| Proceso QA | 4/5 | Se cruzaron GitHub y `brain-env`; no hubo review externo del pipeline |
| **Total** | **34/40 = 85/100** | **NO APROBADA** |

--- METODO PROMETEO ---
Accion delicada: NO
Modo aplicado: FULL
Maquina: brain-env + GitHub API + ClickUp
Rubrica: 34/40 -> 85/100
N/A declarados: seguridad, deployment y testing de producto no aplican a esta auditoría científica; no entran al denominador
Review externo: no pedido; deuda K-02 declarada
Instrumento: GitHub branches, commits, archivos y PRs; `build.run` sobre `/workspace/drosophila-fep-connectome`; evidencia cruda en este archivo
Artefactos: `docs/auditorias/2026-10-02-003-segunda-auditoria-proyecto-chat-h4.md` + [Segunda auditoría H4: GitHub main correcto, brain-env atrasado](https://app.clickup.com/90171457413/docs/2kza6fw5-17757)
NO MEDIDO: loader oficial, rerun alineado, mapping anatómico, causalidad y sincronización del checkout