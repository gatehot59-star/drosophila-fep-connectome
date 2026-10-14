# 2026-10-14-014 · La barra según su dirección está corriendo; el primer humo en Actions falló por falta de torch y el arreglo no tocó el instrumento

**Pedido.** 14-oct 13:29: ClickKit `correr_barra_013` («Correr la barra según su dirección»).

## Veredicto primero
- **[MEDIDO] El humo 1 en Actions (`c425739`) falló antes de medir.**
  - `escape_aterrizaje_dbc3.py`, línea 21: `import torch` → `ModuleNotFoundError: No module named 'torch'`, `humo_exit=1`.
  - Los insumos llegaron con el md5 del pin (3d802fd5 y 719904ab).
- **[ARREGLO DECLARADO, `6e02d34`]** Se agrega `torch==2.14.1 --index-url https://download.pytorch.org/whl/cpu` a `barra-dir-mosca.yml` y a `barra-dir-humo.yml`, igual que en `htau-mosca.yml`.
  - La tarea, el programa y el banco no cambian: d2515357, 0122a4ce y c033f214, verificados en el log de Actions.
- **[MEDIDO] Humo 2 en Actions (`8e89e16`):** EXIT_RUN=0 en 5,6 s; REPRODUCE_M46 True y guardas True.
  - Las 15 líneas de resultados (CELDA, HOLM y H_) son idénticas byte a byte a las del humo de brain-env, comparadas sin el tiempo.
  - Esos números siguen sin valor.
- **[MEDIDO] Corrida completa disparada:**
  - `results/topo_barra_2026-10-14/CORRER` en `e416865`;
  - el workflow `barra-dir-mosca`, run 38598860081, estaba in_progress a las 16:31 UTC (13:31 en Buenos Aires).
- **[CONCLUSIÓN] Llegada estimada hacia las 14:15**, a partir de la velocidad del humo en Actions. NO MEDIDO.

## Herramientas y máquina
- brain-env: lectura de los logs de humo y comparación con `cmp`; prueba del parche.
- GitHub (conector): el arreglo, el `CORRER` y esta respuesta.
- API pública de Actions: estado del run.
- Actions x64: los dos humos y la corrida completa.

## NO MEDIDO
- El resultado de H_TOPO_NUEVO.
- H_TAU.
- La lectura completa del núcleo.

## Antes de firmar
| Afirmación | Instrumento | ¿Podía dar rojo? | Veredicto |
|---|---|---|---|
| El arreglo no tocó el instrumento | md5 del banco, la tarea y el programa en el log de Actions | Sí | PASA |
| Actions da lo mismo que brain-env | `cmp` de las 15 líneas de resultados | Sí: con el humo 1 dio vacío y falló | PASA |
| La corrida arrancó | API de Actions, run con `head_sha` e416865 | Sí | PASA (el final, NO MEDIDO) |

--- METODO PROMETEO ---
Accion delicada: sí (disparo de un experimento sellado, autorizado por Abraham con `correr_barra_013`; arreglo de entorno declarado antes de disparar).
Maquina: brain-env CPU + conector GitHub + Actions x64.
Artefactos: `titan/topo-barra-dir-2026-10-14` `e416865`; esta respuesta en main; Doc https://app.clickup.com/90171457413/docs/2kza6fw5-22337
