# 2026-10-14-056 · En criollo: con nuestra neurona el cableado de la mosca da el mapa, pero MN9 sale sólo con la de Shiu, que acumula y dispara; sigue el cotejo de H_LECTOR y sellar una celda propia que acumule

**Fecha:** 2026-10-16, 20:40 (America/Buenos_Aires)
**Doc:** https://app.clickup.com/90171457413/docs/2kza6fw5-23777

## Pedido

«En criolonque lograste y que sigue» (Abraham, 16-oct 20:22), después de la 055. Síntesis sin corridas nuevas: qué logramos en la línea de la mosca entera (045 a 055) y qué sigue.

## Veredicto primero

- **[MEDIDO] Lo que logramos, en cuatro pasos y siempre con sello antes de mirar:**
  1. **Pusimos el cerebro entero de la mosca al lado del modelo de Shiu** (Nature 2024): 138.639 neuronas y 15 millones de conexiones, sin recortes. Usamos su mismo archivo, su mismo código, su estímulo (azúcar) y su lectura (MN9, la motora que estira la trompa). Lo reprodujimos dos veces: MN9 dispara en 30 de 30 ensayos (049 y 055), y la segunda vez prendió las mismas 321 neuronas más 6.
  2. **El mapa sale con nuestra neurona.** SparseLTC prende 172 de las 321 neuronas que prende Shiu (J 0,366); ninguno de 80 barajados pasa de 103. Salió SOSTENIDO sin umbral y con umbral (049 y 051).
  3. **La motora no sale con nuestra neurona.** MN9 dio REFUTADA en la 049 (18 de 80 barajados la igualaban o superaban). Con ganancia igual (049) y con umbral (051) quedó SIN_DECIDIR, frenada en los dos casos por un solo barajado de 80, el k32.
  4. **Hoy (055) se cerró el porqué.** El modelo de Shiu, con esos mismos 40 barajados, no llega a MN9 en ninguno: ni una espiga en 400 ensayos, k32 incluido. k32 tiene una conexión directa de exactamente 11 sinapsis del azúcar a MN9, que habíamos calculado antes de mirar. Nuestra neurona la suma y la pone arriba del real; la de Shiu la filtra (según la cuenta del sello, esas 11 sinapsis le dan 1,5 mV de los 7 que necesita para disparar).
- **[CONCLUSION] En criollo:** el cableado de la mosca decide a quién recluta el azúcar, y eso nuestra neurona lo agarra en buena parte (más de la mitad, y ningún barajado se le acerca). La decisión motora fina (MN9 sí o no) salió sólo con la neurona de Shiu, que va acumulando y dispara al pasar un umbral. La nuestra, de tasa, deja pasar entradas chicas. Ni la compuerta líquida (049) ni un umbral global (051) lo arreglaron.
- **[CONCLUSION] Por qué es un buen resultado aunque sea negativo:** el problema quedó ubicado. No es el cableado: el real les gana a sus 80 barajados en el mapa y, con el modelo de Shiu, también en la motora (0 de 20 barajados de pesos en la 049 y 0 de 40 de destinos en la 055). Tampoco es el barajado: el modelo de Shiu lo pasa limpio. Queda el tipo de neurona, que por ahora es lectura: la prueba directa es el paso 2 de lo que sigue. Y se predijo antes de ver: las siete apuestas del sello 054 salieron.
- **[CONCLUSION] Cómo entra en los papers** (sigue lo de la 052): el Paper 2 tiene ahora el material completo para el capítulo de la mosca entera (mapa sí, motora no, y por qué), todavía sin escribir. El Paper 1 gana una vara externa sin cambiar números. El Paper 3 lo toca de costado: MN9 es una motora de la boca.
- **[MEDIDO] Deudas al día de hoy:**
  - Este parche pone el CONTEXTO al día con la 055, que había quedado pendiente, y con esta.
  - La réplica de H_LECTOR terminó en brain-env (6 de 6 celdas, todas con EXIT_RUN=0, sin procesos vivos), pero el cotejo no está hecho, y es condición para Zenodo.
  - El token de Zenodo sigue sin revocar (034).
- **Qué sigue, en el orden que te propongo (opinión):**
  1. **El cotejo de la réplica de H_LECTOR.** Es barato y destraba Zenodo.
  2. **Sellar una neurona de SparseLTC que acumule en el tiempo, con umbral y reinicio**, contra los mismos 80 barajados. Si llega a MN9 sólo en el real, cerramos la distancia con Shiu con una celda propia; si no, MN9 queda fuera de lo que nuestra celda puede destilar, por ahora.
  3. **Escribir el capítulo de la mosca entera en el Paper 2**, con estos números tal como están.
  4. **Revocar el token de Zenodo.**
  5. Lo demás sigue en espera: PR #26, BANC, Paper 3 y H_DEBILES.

## Herramientas y máquina

- Conector GitHub: commits de `main` y de la rama. No hay nada nuevo desde 642b0df ni desde bd37336.
- brain-env: estado de la réplica de H_LECTOR (logs y procesos), grep de la 049 y la 051 en un clon de `main`, anclas del CONTEXTO y prueba del parche en una copia.
- Sandbox de ClickUp: redacción de esta respuesta y del parche.
- Actions: nada corrió.

## Fuentes

Respuestas 2026-10-14-049 (REPRO_SHIU, H_ENTERA_CONJUNTO y H_ENTERA_MN9), 051 (H_ENTERA_UMBRAL), 052 (síntesis anterior), 053 (contra Shiu y Lappalainen), 054 (sello H_LIF_SHUFG) y 055 (medición). En la rama: `results/lif_shufg_2026-10-16/actions_correr/agregado_lif_shufg.log` (md5 9b8634f483904b6d627715335b538058).

Parche del CONTEXTO, probado en una copia del de `main` (642b0df) en brain-env: `md5 antes a14d0c5fe8bc89486dd3291ea46376b0`, cinco anclas con 1 aparición cada una, `md5 despues 2da204c6a3982aea4c448f6d466c8efe`; la segunda pasada da `ANCLA apariciones=0` y `ABORTA: ancla no unica`, con el md5 sin cambios. Incluye la entrada de la 055, que esa respuesta había dejado pendiente.

## Archivos

| Archivo | Dónde | md5 |
|---|---|---|
| `docs/agents/respuestas/2026-10-14-056-en-criollo-que-logramos-y-que-sigue.md` | `main` | este archivo |
| `tools/contexto/actualizar_contexto_2026-10-14-056.py` | `main` | 908489d2e9b390e56ef888ea17954fbe |
| `.github/workflows/contexto-2026-10-14-056.yml` | `main`, se borra solo al aplicar | 32499a6d6a14b0ea4323ae4ebefe1344 |

## NO MEDIDO

- La neurona que acumula en el tiempo: es la propuesta, sin sellar ni correr.
- El cotejo de la réplica de H_LECTOR.
- Validación contra moscas vivas: Shiu la tiene (optogenética de 106 tipos); nosotros no.
- El camino concreto por el que el real llega a MN9 sin arista directa.

## Antes de firmar

| Afirmación | Instrumento | ¿Podía dar rojo? | Veredicto |
|---|---|---|---|
| Los números citados son los de 049 a 055 | 049 y 051 releídas con grep en un clon de `main` (642b0df) antes de firmar; 055 desde su log | Sí: un número mal copiado se ve contra el log | medido (copia) |
| «MN9 sale sólo con la de Shiu» | 049, 051 y 055 | Sí: MN9 en algún SHUF_G con el LIF, o el real sin MN9, lo tumbaba | medido, entre las dos neuronas probadas |
| La réplica de H_LECTOR terminó | 6 logs con EXIT_RUN=0 y ningún proceso vivo en brain-env | Sí | medido |
| Nada nuevo en git desde la 055 | `list_commits` de `main` y de la rama | Sí | medido |
| «El problema es el tipo de neurona» | lectura sellada de la 054, aplicada en la 055 | No: es lectura | CONCLUSION |
| El orden de lo que sigue | ninguno | No | opinión |
| El parche del CONTEXTO aplica | copia del de `main` en brain-env; la segunda pasada aborta | Sí | medido |

--- METODO PROMETEO ---
Rol: síntesis (chica). Delicado: no.
Máquinas: conector GitHub, brain-env (estado y parche), sandbox de ClickUp (redacción). Actions: nada.
Archivo: `docs/agents/respuestas/2026-10-14-056-en-criollo-que-logramos-y-que-sigue.md` en `main`.
Doc: https://app.clickup.com/90171457413/docs/2kza6fw5-23777
