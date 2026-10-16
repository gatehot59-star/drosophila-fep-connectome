# 2026-10-14-051 · H_ENTERA_UMBRAL medida: con el presupuesto del LIF el azúcar llega a MN9 en el cableado real y no en 79 de 80 barajados; queda SIN_DECIDIR por un solo nulo, el mismo k32 de la 049

**Fecha:** 2026-10-16, 11:35 (America/Buenos_Aires)
**Rama:** `titan/mosca-entera-2026-10-15`. Instrumento `1f40beb`, disparo `44df969`, medición del bot `c5f2960` (run 38912718970).
**Sello:** `tools/mosca_entera/SELLO-UMBRAL-050.md` (`868ded6`, md5 680abca839bd6c80367c9b434af7d800), sin cambios.
**Doc:** https://app.clickup.com/90171457413/docs/2kza6fw5-23597

## Pedido

«Implementá el instrumento UMB» (Abraham, 16-oct 10:37), en respuesta a mi pregunta de si seguía con el código, la prueba corta y la corrida completa sin volver a preguntarle. Lo tomé como sí a las tres: instrumento, prueba y humo en Actions, y CORRER apenas el humo salió limpio.

## Veredicto primero

- **[MEDIDO] Los tres controles pasan.** PIN (md5 de conectividad, anotaciones, completitud y LIF en los 9 trabajos), CALIB_REAL (el real quedó con 321 activas justas, θ = 0,000416815) y TASA_049 (J = 0,3659574468, el de la 049 a 10 cifras).
- **[MEDIDO] H_UMB_MN9 SIN_DECIDIR.** Con el umbral que deja 321 activas, MN9 entra en el real: r = 0,000145, puesto 269 de 321. En los 40 SHUF_W queda en cero. En SHUF_G, 39 de 40 en cero y uno solo por encima: k32, con 0,00158. La banda sellada pide cero nulos iguales o mayores en cada familia para SOSTENIDA y 5 o más en alguna para REFUTADA; uno solo deja SIN_DECIDIR.
- **[MEDIDO] Es el mismo nulo de la 049.** En H_ENTERA_MN9_G1 el único nulo por encima del real también fue SHUF_G k32 (0,00348). El radio G1 coincide a 12 cifras en las dos corridas (0,155030739524): es el mismo grafo.
- **[MEDIDO] H_UMB_CONJUNTO SOSTENIDA.** J = 0,332 contra máximos de 0,182 (SHUF_W) y 0,006 (SHUF_G); ningún nulo igual o mayor.
- **[MEDIDO] H_UMB_GANA REFUTADA.** J(UMB) − J(TASA) = −0,034: el umbral no mejora el conjunto; la TASA sola da 0,366.
- **[MEDIDO] Secundaria, no decide.** Con el θ del real fijo en los 80 nulos, los SHUF_W se apagan (mediana 134 activas) y MN9 queda en cero en los 40; los SHUF_G se encienden (mediana 924) y MN9 sólo aparece en k32 (0,00306).
- **[CONCLUSION] Lectura sellada (sección 6): SIN_DECIDIR.** 80 nulos no lo resuelven y no se agregan nulos después de ver. La destilación no queda habilitada: pedía MN9 y CONJUNTO SOSTENIDAS.
- **[CONCLUSION] Mi expectativa falló.** Aposté H_UMB_MN9 REFUTADA con r = 0 (70%) y MN9 sí entra entre las 321 del real. Acerté CONJUNTO SOSTENIDA (85%); GANA, que dejé al 50%, salió REFUTADA.
- **[CONCLUSION] Qué dice, sin estirarlo.** En la 049 la tasa sin umbral prendía 48.407 neuronas, MN9 quedaba en 0,00203 y 18 de 80 nulos a radio 0,9 la igualaban o superaban. Con el presupuesto de actividad del LIF y la misma ganancia por sinapsis en todos los grafos, el camino azúcar a MN9 aparece en el real y desaparece cuando se barajan los pesos sobre el mismo cableado (0 de 40 SHUF_W). Contra esa familia la banda queda limpia; lo que impide SOSTENIDA es un nulo de SHUF_G que ya había aparecido en la 049. Apunta a que el reflejo depende de qué sinapsis pesan cuánto y no sólo de quién se conecta con quién, pero el veredicto sellado es SIN_DECIDIR y así queda.
- **[MEDIDO] Descriptivo, no es el criterio sellado:** con la cuenta de permutación (b + 1)/(m + 1), SHUF_W da 1/41 ≈ 0,024 y SHUF_G 2/41 ≈ 0,049. Lo dejo para que se vea cuán cerca quedó; no cambia nada.

## Números de CORRER

| Grafo | θ | Activas | r MN9 | J contra S_LIF |
|---|---|---|---|---|
| Real (radio 0,9) | 0,000416815 | 321 | 0,000145 (puesto 269) | 0,332 (TASA: 0,366) |
| 40 SHUF_W (G1) | mediana 0,0000637 | 40 OK | 0 en los 40 | máx 0,182 |
| 40 SHUF_G (G1) | mediana 0,00190 | 40 OK | 0 en 39; k32: 0,00158 | máx 0,006 |

SHUF_W permuta los pesos entre aristas (mismo cableado); SHUF_G permuta el destino de cada arista (mismos grados de entrada y salida, cada arista con su peso). Los dos con el factor del real (G1).

## Herramientas y máquina

- **Sandbox de ClickUp:** código, 7 de 7 y extremo a extremo sintético (real, nulos y agregado).
- **brain-env:** prueba 7 de 7; md5 desde clones nuevos del instrumento (`1f40beb`) y de la medición (`c5f2960`, 30 de 30 OK).
- **GitHub Actions (4 núcleos, 16 GB):** prueba (run 38910983238, bot `990f446`, TESTS_OK 7 de 7), humo (run 38910983991, bot `4afa6a8`, 12 de 12 md5 OK), CORRER (run 38912718970, 14:03:39 a 14:24:02 UTC, unos 20 min de pared; el real tardó 103 s con 26 θ probados y un pico de 2,25 GB; cada nulo, unos 103 s).
- **GitHub MCP:** los pushes.

## Archivos

| Archivo | md5 |
|---|---|
| `tools/mosca_entera/umb_entera.py` | b9581ae42f938495e07f453097426257 |
| `tools/mosca_entera/agregar_umb.py` | ada5b143f8abe7108c0026e1cd350cf8 |
| `tools/mosca_entera/prueba_umb.py` | 456e02241c65b7a96125d9fcf44b5001 |
| `.github/workflows/umb-prueba.yml` | a0da2586b6891a04a4c133704a97daf6 |
| `.github/workflows/umb-humo.yml` | 4ec0601b537c9278281e122c8389c3bc |
| `.github/workflows/umb-correr.yml` | 5a314f522d7c84a32659e2cc2eaf6ebf |
| `results/mosca_umbral_2026-10-16_humo/actions_prueba/prueba.log` | 505d34be980ca0856ba21e0f9b3f14d3 |
| `results/mosca_umbral_2026-10-16_humo/actions_humo/agregado_umb.log` | 4bf7503b45b68192d27cefb79a8ff9e2 |
| `results/mosca_umbral_2026-10-16/CORRER` | e37774377a80264810a6f052d1c3bee7 |
| `results/mosca_umbral_2026-10-16/actions_correr/MD5SUMS.txt` (30 archivos) | 509bacb8f612ae399b3c54f531147292 |
| `results/mosca_umbral_2026-10-16/actions_correr/agregado_umb.log` | 75dbd329fd3b2dd46aa7e9bb6c59727a |
| `results/mosca_umbral_2026-10-16/actions_correr/agregado_umb.json` | 50127c1b62bd3bb21d0bf767a7a4a9ec |
| `results/mosca_umbral_2026-10-16/actions_correr/umb_real.json` | 8baf4da9f797304525d5fa53ef16be51 |
| `tools/contexto/actualizar_contexto_2026-10-14-051.py` (`main`) | 92566ab7ea7c4868bed8162ca11b3757 |

Los `*_top.npz` quedaron en los artefactos del run, no en git.

## NO MEDIDO

- Paridad con el runtime SparseLTC de Mojo/C++ del compilador: todo esto es la ecuación en numpy disperso.
- Sensibilidad a N*: MN9 está en el puesto 269 de 321; con un presupuesto más chico podría quedar afuera. No se corrió otro N*.
- Por qué SHUF_G k32 llega a MN9 (qué aristas reubicadas abren el camino): no mirado.
- Que la ventana de UMB sea punto fijo: se corrió sólo τ 30, como pide el sello.
- Espigas y temporización: UMB es tasa con umbral; nada de esto dice que reproduzca los tiempos del LIF.
- Otros estímulos, otros reflejos y la réplica en BANC.
- Monotonía de Activas(θ): los 81 grafos calibraron dentro de ±32, pero no se probó que sea monótona.

## Antes de firmar

| Afirmación | Instrumento | ¿Podía dar rojo? | Veredicto |
|---|---|---|---|
| Los controles pasan | `agregar_umb.py` sobre los JSON de los 9 trabajos | Sí: un md5 distinto, activas fuera de 289 a 353 o un J corrido | medido, PASA |
| TASA_049 prueba que nada derivó | el mismo código de la 049 corrido otra vez | Sí por deriva de datos o código; no por un error común a las dos corridas (W-01) | medido, con ese alcance |
| H_UMB_MN9 SIN_DECIDIR | `banda_nulos` de la 046, probada en `prueba_umb.py` | Sí: r ≤ 0 o 5 nulos daban REFUTADA; 0 nulos, SOSTENIDA | medido |
| MN9 entra entre las 321 del real | `umb_real.json` (rango_mn9 269, r > 0) | Sí: con r = 0 quedaba fuera | medido |
| k32 es el mismo nulo de la 049 | índice 32 en las dos listas y radio G1 a 12 cifras | Sí: otro grafo da otro radio | medido |
| El brazo real con azúcar no se vio antes de CORRER | log del humo: estímulo de 20 no sensoriales, semilla 99; nulos k 99 | Sí: el log dice qué estímulo usó | medido |
| La medición en git es la del runner | `md5sum -c` desde un clon nuevo en brain-env, 30 de 30 | Sí para la integridad del commit; no prueba la corrida, que la escribió el mismo runner | medido, con ese alcance |
| El parche del CONTEXTO aplica | no se probó sobre una copia antes del push; lo aplica el bot en Actions | No al firmar | NO MEDIDO al firmar |

La aplicación del parche por el bot se verifica después del push, desde un clon nuevo.

--- METODO PROMETEO ---
Rol: implementa y mide. Delicado: no.
Máquinas: sandbox de ClickUp, brain-env (prueba y md5), GitHub Actions (prueba, humo y CORRER).
Archivo: `docs/agents/respuestas/2026-10-14-051-umbral-medido-mn9-sin-decidir-por-el-nulo-k32-y-el-conjunto-pasa.md` en `main`.
Doc: https://app.clickup.com/90171457413/docs/2kza6fw5-23597
