# Estado vivo del repo · 2026-09-22

## Pedido
Revisar el estado actual del proyecto entrando al repositorio real.

## Herramientas declaradas
Lectura GitHub en vivo sobre `gatehot59-star/drosophila-fep-connectome`: árbol de `main`, `README.md`, `00-ENTORNOS-Y-CAPACIDADES.md`, `docs/agents/CONTEXTO-motor.md`, `docs/agents/CONTEXTO-drosophila-fep.md`, listado de ramas, commits recientes, PRs abiertos, detalles y check runs.

## Estado medido

### `main`
- HEAD: `08b3b01bc0a6c678ae09fe6adeabadfe6cd94b63`.
- Último commit: incorporó a `main` el inventario de entornos y corrigió la falsa lectura de que `brain-env` no tenía toolchain Android, wrapper Gradle ni git montado.
- Ramas visibles: `main`, `titan/initial-release`, `titan/twohop-nulls`, `titan/auditoria-integra-2026-08-25`.
- `main` no está protegida.
- La raíz de `main` no muestra `.github/workflows/`; el propio inventario declara que el CI de guards vive en una rama de trabajo, no en `main`.

### PRs abiertos, ninguno mergeado
1. PR #1, release inicial: 15 archivos, sin check runs. Está basado en un `main` viejo (`55aeba4...`).
2. PR #2, null anatómico: 140 archivos, 23.111 altas y 210 bajas; abierto contra `main` en `39ce869...`. Su resultado cambia el veredicto de dos saltos: el spread 323× colapsa a 2,4× y tres signos se invierten. Tiene 2 check runs `success` de la batería de guards.
3. PR #3, auditoría integral: un archivo, abierto contra la rama del PR #2, no contra `main`. Declara 62,2/100 y rechaza el release como reproducible. Tiene 0 check runs.

### Divergencia crítica
`main` todavía contiene el contexto anterior al null anatómico: declara ese control como no medido y conserva el resultado de 2 saltos contra grado. El PR #2 ya lo corrió y lo refutó. Por lo tanto, hoy no existe una única versión canónica del veredicto: `main` y la rama de dos saltos cuentan historias distintas.

### Motor / DualBrain
El contexto vigente del motor sí tiene los números recientes: la ablación gate/no-gate gana 21,85× a 108,11× en 4/4 tareas; el gate vectorial contra escalar solo gana 2/4 y empata 2/4; el C99 mide 1.336 B de `.text` en ESP32 a `-Os`; la hipótesis del 96% fijo sigue `NO MEDIDO` sobre SparseLTC. La línea sigue mezclada en el mismo repo, pero el contexto la separa correctamente de los papers.

## Evidencia cruda mínima
```text
main = 08b3b01bc0a6c678ae09fe6adeabadfe6cd94b63
PR #2 checks = 2, ambos success
PR #3 checks = 0
PR #1 checks = 0
PR #2 state = open, merged = false
PR #3 state = open, merged = false
main protected = false
```

## Veredicto
**El proyecto tiene resultados científicos fuertes, pero el repositorio no está en estado release.** El bloqueo principal no es falta de datos: es divergencia entre `main` y los PRs, ausencia de CI en la rama pública principal y reproducibilidad incompleta, exactamente como señala el PR #3. No conviene mergear PR #2 o #3 a ciegas: primero hay que decidir cuál es el veredicto canónico y actualizar contexto, README y workflows contra esa decisión.

## NO MEDIDO
- No leí el texto de los logs de Actions, solo sus check runs y conclusiones.
- No verifiqué un clone fresco ni ejecuté nuevamente los 1.280 s del null anatómico.
- No comprobé si el estado actual de Zenodo ya recibió la v2 del erratum.
- No pedí review automático nuevo; un check `success` de guards no equivale a aprobación externa.

--- METODO TITAN ---
Accion delicada: NO
Modo aplicado: TITAN FULL
Rubrica: N/A (lectura de estado, sin código ni merge)
N/A declarados: todos los criterios de implementación, seguridad, testing de producto, deploy e innovación; no aplica a un reporte de estado
Review externo: no pedido; K-02 no se interpreta como aprobación
Instrumento: GitHub MCP, lectura en vivo; HEAD y ramas verificados contra la API, check runs consultados por PR
