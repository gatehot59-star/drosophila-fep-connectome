# 2026-10-13-016 · Factorial 4 disparado: los dos kernels del cerebro entero están corriendo en Kaggle

## Veredicto

- **[MEDIDO] Disparado y corriendo.** `f4-ce-a-2026-10-13` y `f4-ce-b-2026-10-13` (cuenta `abrahammendieta`, T4 x2) quedaron RUNNING a las 00:14 UTC del 14-oct (21:14 en Buenos Aires).
- **[MEDIDO] Lo empujado es lo sellado.** Los dos kernels salieron de un clon fresco de `431b7bd` y dan los md5 de `SELLO-FACTORIAL4.md`.
- **[CONCLUSIÓN] Fin estimado entre 03:30 y 04:00 UTC** (00:30 a 01:00 en Buenos Aires). Sale de 0,026 s por ensayo medido en el humo.
- **[MEDIDO] Todavía no hay ningún resultado.**

## Pedido

Clic de Abraham en ClickKit `correr_factorial4_015` («Correrlo en Kaggle»), 21:12.

## Herramientas y máquina

- **brain-env:** `kaggle kernels push` de los dos kernels y `kaggle kernels status`.
- **Kaggle:** cuenta `abrahammendieta`, dos sesiones de GPU T4 x2. **Gasta unas 7 h de la cuota semanal de Abraham**, con su autorización.
- **GitHub:** este commit en `main`.

## Qué se midió

- HEAD del clon fresco: `431b7bd54a78a46e82c8e793135984204536d8f1`.
- md5 de los kernels empujados: iguales a los sellados.
- Estado en Kaggle a las 00:14:10 UTC: RUNNING los dos.

## Evidencia cruda

```
431b7bd54a78a46e82c8e793135984204536d8f1
d76dc6522aa773489a3505c73d96f9e5  f4-ce-a-2026-10-13/f4-ce-a-2026-10-13.py
fcc63f904baf3de4bdf874580a2048f1  f4-ce-a-2026-10-13/kernel-metadata.json
09ffa7743101c614cd5f511e87776917  f4-ce-b-2026-10-13/f4-ce-b-2026-10-13.py
700de6b29e1977f951efba26e69f2413  f4-ce-b-2026-10-13/kernel-metadata.json
Kernel version 1 successfully pushed.  Please check progress at https://www.kaggle.com/code/abrahammendieta/f4-ce-a-2026-10-13
Wed Oct 14 00:13:11 UTC 2026
Kernel version 1 successfully pushed.  Please check progress at https://www.kaggle.com/code/abrahammendieta/f4-ce-b-2026-10-13
Wed Oct 14 00:13:20 UTC 2026
abrahammendieta/f4-ce-a-2026-10-13 has status "KernelWorkerStatus.RUNNING"
abrahammendieta/f4-ce-b-2026-10-13 has status "KernelWorkerStatus.RUNNING"
Wed Oct 14 00:14:10 UTC 2026
```

Parche del CONTEXTO en copia (script `f49bef03`): `md5 antes 055a51a914fe2cf5cb7c286f29566923`, cuatro anclas con 1 aparición, `md5 despues 5ccf0ba1fbdc044896374fa2e2262155`, `PARCHE OK`.

## Archivos

- Esta respuesta, `tools/contexto/actualizar_contexto_2026-10-13-016.py` y su workflow, que se retira solo.

## NO MEDIDO

- Que los kernels pasen las etapas de entrada (pip, git en el SHA, md5 de instrumento e insumos): el CLI no deja leer el log mientras corre.
- Que terminen sin cortes, y cuánta cuota queda.
- Cualquier número del factorial 4.

## Antes de firmar

| afirmación | instrumento | ¿podía dar rojo? |
|---|---|---|
| lo empujado es lo sellado | md5 de los kernels rearmados desde clon fresco de `431b7bd` | sí: no se empujaba si no coincidían |
| están corriendo | `kaggle kernels status` | sí: puede dar QUEUED, ERROR o CANCEL |

```
--- METODO PROMETEO ---
Accion delicada: si (gasta unas 7 h de la cuota semanal de GPU de abrahammendieta; autorizado con el clic)
Maquina: brain-env | Kaggle T4 x2 (abrahammendieta)
Artefactos: docs/agents/respuestas/2026-10-13-016-factorial4-disparado-en-kaggle-corriendo.md + Doc de ClickUp 2026-10-13-015
```
