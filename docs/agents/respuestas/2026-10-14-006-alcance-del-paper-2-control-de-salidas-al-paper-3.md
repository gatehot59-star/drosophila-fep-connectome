# 2026-10-14-006 · Alcance del Paper 2: el control de las salidas, LC6→GF y sel_post van a un Paper 3

**Pedido.** 14-oct 12:19, ClickKit `alcance_p3_005` («Control de salidas al Paper 3»), sobre la recomendación de la 2026-10-14-005.

## Veredicto primero
- **[DECIDIDO, Abraham]** El control de las salidas (2026-10-10-005 a 009), LC6→GF y sel_post salen del Paper 2 y van a un **Paper 3 estructural**.
- El Paper 2 queda con una sola pregunta: ¿el cableado exacto carga el reflejo más allá de su diseño y de sus barajados, y esa parte se conserva en BANC?
- **[HECHO]** La decisión está anotada en `docs/paper2/paper2-esqueleto.md`, rama `titan/paper2-esqueleto-2026-10-14`, commit `4652c81`. El diff contra `753d4d5` es de 1 archivo, 2 líneas: la nota de alcance y el ítem del checklist.
- **[CORRECCIÓN]** El parche de la 005 puso «12:40» en el encabezado del CONTEXTO; la 005 salió a las 12:18. Este parche lo deja en 12:25, con la 006.

## Herramientas y máquina
- GitHub (conector): dos `push_files` (el esqueleto en la rama titan; esta respuesta en main).
- brain-env (CPU): `git diff --stat` del esqueleto y la prueba del parche en una copia.

## Qué se midió
Nada del experimento. Se registró una decisión.

## Evidencia cruda
```
git diff 753d4d5 4652c81 --stat: docs/paper2/paper2-esqueleto.md | 4 ++-- (2 insertions, 2 deletions)
parche: md5 antes 5f3fbff6 -> despues 2cfe4814; segunda aplicacion ABORTA
```

## Archivos
- Esta respuesta.
- `tools/contexto/actualizar_contexto_2026-10-14-006.py` (md5 `b20fb91b`).
- `.github/workflows/contexto-2026-10-14-006.yml`.
- Doc público: https://app.clickup.com/90171457413/docs/2kza6fw5-22177

## NO MEDIDO
- Lo mismo que en la 005: H_CONSENSO, H_TAU, el nulo BANC, la literatura y las figuras.
- El Paper 3 no tiene esqueleto.

## Antes de firmar
| Afirmación | Instrumento | ¿Podía dar rojo? | Veredicto |
|---|---|---|---|
| El esqueleto solo cambió en el alcance | `git diff --stat` | Sí: mostraría más líneas o archivos | PASA (2 líneas) |
| El parche no rompe el CONTEXTO | Prueba en copia con md5 y doble aplicación | Sí: aborta si un ancla no es única | PASA |

--- METODO PROMETEO ---
Accion delicada: no (registro de una decisión de Abraham; nada corrido ni mergeado).
Maquina: conector GitHub + brain-env CPU.
Artefactos: `titan/paper2-esqueleto-2026-10-14` `4652c81`; esta respuesta en main; Doc https://app.clickup.com/90171457413/docs/2kza6fw5-22177
