# 2026-10-14-054 · Sellado: el LIF de Shiu contra los 40 barajados de destinos va a decir si el freno de MN9 en k32 es del barajado o de nuestra neurona; nada corrido

**Fecha:** 2026-10-16, 13:10 (America/Buenos_Aires)
**Doc:** https://app.clickup.com/90171457413/docs/2kza6fw5-23657

## Pedido

«Seal the SHUF_G LIF comparison» (Abraham, 16-oct 12:40), sobre la pregunta con la que cerró la 053: correr el modelo de Shiu contra los 40 barajados de destinos (SHUF_G); si su propio modelo también llega a MN9 en ese barajado, el problema es el barajado y no nuestra neurona. Pidió sellar: no se escribió instrumento ni corrió nada.

## Veredicto primero

- **[MEDIDO] Sellado en git antes de cualquier instrumento.** `tools/mosca_entera/SELLO-LIF-SHUFG-054.md` en la rama `titan/mosca-entera-2026-10-15`, commit 307db84 (12:54), md5 9e7e25f7f7e4ca8bbd031f6484eefe54, verificado desde un clon fresco en brain-env. Nada corrió.
- **Qué se va a medir.** El LIF de Shiu sin cambios, el mismo de la 049, sobre los mismos 40 SHUF_G que frenaron a H_ENTERA_MN9_G1 y H_UMB_MN9, con 10 ensayos cada uno, más el real de 30 ensayos como control.
- **Cómo se decide.** Con las mismas bandas que frenaron a nuestra celda (las de H_UMB_MN9): ningún nulo arriba, SOSTENIDA; 5 o más, REFUTADA; de 1 a 4, SIN_DECIDIR. Dos criterios por nulo: el de Shiu (MN9 dispara en 5 o más de 10 ensayos, H_LIF_G_SHIU) y el nuestro (tasa de MN9 igual o mayor que la del real, H_LIF_G_VARA). k32 va aparte (H_LIF_K32), con su lectura fijada en cuatro casos: no llega (el freno es de nuestra neurona), llega desbocado (actividad global), llega con tasa igual o mayor que el real (el freno es del barajado, también para Shiu) y llega con tasa menor (el camino es del barajado y a nuestra celda le falta contraste).
- **[MEDIDO] Controles que pueden dar rojo.** CTRL_REAL: MN9 en 27 o más de 30 ensayos reales. NULO_MISMO: cada nulo tiene que tener el radio crudo que registró la 049, con tolerancia relativa 1e-6. Hoy los 40 radios de la 049 y de la 051 coinciden entre sí a 3,1e-11 (medido en brain-env).
- **[CONCLUSION] No cambia veredictos sellados.** H_UMB_MN9 y H_ENTERA_MN9_G1 siguen SIN_DECIDIR pase lo que pase; esto sólo atribuye el freno de k32.
- **[CONCLUSION] Expectativa escrita antes de ver: k32 no llega (80%).** En las tres lecturas de nuestra tasa, la entrada neta de MN9 en k32 da lo mismo, 0,00348: G1 0,00348; UMB 0,00158 más su θ 0,00190; con el θ del real, 0,00306 más 0,00042. Con el factor G1 eso tiene la forma de unas 11 sinapsis directas desde el azúcar. En el LIF de Shiu, 11 sinapsis desde presinápticas a 100 Hz dan en promedio 1,5 mV de los 7 que faltan para disparar. Si sale así, el freno es de nuestra neurona de tasa, que deja pasar una entrada chica que el umbral del LIF filtra.
- **Siguiente paso, no hecho:** el instrumento (`lif_shufg.py`, agregado y prueba) con prueba y humo en Actions, y después CORRER. Si SHUF_G cuesta como SHUF_W, son unas 1,6 h de trabajo en 8 trabajos, unos 15 min de pared (estimado, NO MEDIDO).

## Herramientas y máquina

- Conector GitHub: lectura de `lif_shiu.py`, del workflow de CORRER de la 049, de los sellos 046 y 050 y de los logs y JSON de la 049 y la 051; push del sello a la rama. `liq_entera.py`, desde la copia del sandbox (md5 ae3c1a2d, la misma de la rama).
- brain-env (clon x051 en c5f2960, clones frescos m054 de `main` y s054 de la rama): md5 de lo citado, radios de los 40 SHUF_G en la 049 y en la 051, θ y MN9 de k32, tiempos y activas de los 20 SHUF_W del LIF, prueba del parche del CONTEXTO.
- Web: `model.py` de Shiu en `91bdd1e7` (parámetros por defecto, entrada de Poisson y conexión de sinapsis).
- Sandbox de ClickUp: redacción del sello, de esta respuesta y del parche.
- Actions: nada corrió.

## Evidencia cruda

Salida de `/tmp/v054.py` en brain-env (lee los JSON de la 049 y la 051 en el clon x051):

```
UMB_SHUF_G_mn9_pos [(32, 0.0015808510058579572, 0.0030619625939455096, 372.81323741511756)]
UMB_SHUF_G_fijo_pos [(32, 0.0030619625939455096, 914)]
UMB_SHUF_W_mn9_pos []
G1_SHUF_G_top3 [(0.00347771563856435, 32), (6.357639516265737e-05, 39), (2.2149137893606765e-05, 38)]
LIF_SHUF_W n 20 activas 41 59 K 12 33 ensayos_mn9_max 0 seg 91.6 193.6 suma_seg 2918.9
radios n049 40 n051 40 max_dif_rel 3.1376147480894003e-11 k32 372.81323741506026 372.81323741511756
radios_min_max 235.8919874025899 1092.1151439821376
LIF_REAL 30 61.63333333333333 393 321 268896
```

k32 en `umb_SHUF_G_k030.json` de la 051 (θ, MN9, activas, estado, MN9 y activas con θ del real fijo, θ del real, factor G1):

```
k32 0.0018976330757141113 0.0015808510058579572 321 OK 0.0030619625939455096 914 0.00041681528091430664 0.00041584022230338366
```

md5 en el clon x051:

```
55bc4c76657e35f341300d0e082c7ebe  tools/mosca_entera/SELLO-MOSCA-ENTERA.md
022dbbdd87ce206e9f33efc62d8e7ee7  tools/mosca_entera/ENMIENDA-048.md
680abca839bd6c80367c9b434af7d800  tools/mosca_entera/SELLO-UMBRAL-050.md
88c8459eb87ed328de9f65f38337f8b4  tools/mosca_entera/lif_shiu.py
ae3c1a2dd85a6faecfbfe76d71b0072f  tools/mosca_entera/liq_entera.py
05bedf6fc250ed8c053d99236f3052bf  results/mosca_entera_2026-10-15/actions_correr/liq_SHUF_G_k000.json
62982026c51da6756caba9ba49f91eae  results/mosca_entera_2026-10-15/actions_correr/liq_SHUF_G_k020.json
dddfaeb2957cd40a2b202a39d931cf51  results/mosca_umbral_2026-10-16_humo/actions_humo/umb_SHUF_G_k099.json
```

Del `model.py` de Shiu en `91bdd1e7`, textual: `'v_0' : -52 * mV`, `'v_th' : -45 * mV`, `'t_mbr' : 20 * ms`, `'tau' : 5 * ms`, `'w_syn' : .275 * mV`, `'f_poi' : 250`, `neu[i].rfc = 0 * ms # no refractory period for Poisson targets`, `syn.connect(i=i_pre, j=i_post)`.

Cuenta de la expectativa: 100 Hz × 11 sinapsis × 0,275 mV × 0,005 s = 1,51 mV de entrada media; el umbral está 7 mV arriba del reposo. 0,00348 / (0,00041584 × tanh(1)) = 11,0 sinapsis.

Sello desde el clon fresco s054: `307db84`, `9e7e25f7f7e4ca8bbd031f6484eefe54  tools/mosca_entera/SELLO-LIF-SHUFG-054.md`, commit 2026-10-16T12:54:51-03:00.

Parche del CONTEXTO sobre una copia del de `main` (a99ac4f): `md5 antes 5aef709ef3f6cc84d375f61ea09dcf97`, cinco anclas con 1 aparición cada una, `md5 despues a14d0c5fe8bc89486dd3291ea46376b0`; la segunda pasada da `ANCLA apariciones=0` y `ABORTA: ancla no unica`, con el md5 sin cambios.

## Archivos

| Archivo | Dónde | md5 |
|---|---|---|
| `tools/mosca_entera/SELLO-LIF-SHUFG-054.md` | rama `titan/mosca-entera-2026-10-15`, 307db84 | 9e7e25f7f7e4ca8bbd031f6484eefe54 |
| `docs/agents/respuestas/2026-10-14-054-sello-lif-de-shiu-contra-shuf-g.md` | `main` | este archivo |
| `tools/contexto/actualizar_contexto_2026-10-14-054.py` | `main` | b1eff038d57ce9b04d75c4957fc56387 |
| `.github/workflows/contexto-2026-10-14-054.yml` | `main`, se borra solo al aplicar | 4b18de20d6cb5b209a48b3de565187e8 |

## NO MEDIDO

- El resultado entero: no existe todavía ningún número del LIF sobre SHUF_G.
- El costo de un SHUF_G en el LIF: el estimado sale de los SHUF_W de la 049; lo mide el humo.
- Que k32 tenga una arista directa de azúcar a MN9: es inferencia desde tres lecturas de la tasa; lo mide n1 en el instrumento.
- El nulo exacto de los suplementos de Shiu (no leídos).
- El cotejo de la réplica de H_LECTOR en brain-env sigue pendiente.

## Antes de firmar

| Afirmación | Instrumento | ¿Podía dar rojo? | Veredicto |
|---|---|---|---|
| El sello está en git antes del instrumento | push a la rama y md5 desde un clon fresco | Sí: el md5 o el commit podían no coincidir | medido |
| k32 es el único de 80 nulos por encima del real en G1 y en UMB | JSON de la 049 y la 051 leídos en brain-env | Sí | medido |
| Los 40 SHUF_G de la 049 y la 051 son los mismos grafos | radios crudos comparados, máximo 3,1e-11 | Sí: un nulo distinto da otro radio | medido |
| Parámetros del LIF que usa la expectativa | `model.py` de Shiu en 91bdd1e7, leído textual | Sí | medido |
| La entrada de MN9 en k32 son unas 11 sinapsis directas desde el azúcar | aritmética sobre tres lecturas de la tasa | Parcial: supone despreciable el resto de la entrada de MN9 | CONCLUSION; la mide n1 |
| Expectativas con porcentaje | ninguno: son apuestas escritas antes de ver | No | expectativa, no medición |
| El parche del CONTEXTO aplica | copia del de `main` en brain-env; la segunda pasada aborta | Sí | medido |

--- METODO PROMETEO ---
Rol: sello. Delicado: no.
Máquinas: conector GitHub, brain-env (lectura y parche), web (`model.py` de Shiu), sandbox de ClickUp (redacción). Actions: nada.
Archivo: `docs/agents/respuestas/2026-10-14-054-sello-lif-de-shiu-contra-shuf-g.md` en `main`.
Sello: `tools/mosca_entera/SELLO-LIF-SHUFG-054.md` en `titan/mosca-entera-2026-10-15` (307db84).
Doc: https://app.clickup.com/90171457413/docs/2kza6fw5-23657
