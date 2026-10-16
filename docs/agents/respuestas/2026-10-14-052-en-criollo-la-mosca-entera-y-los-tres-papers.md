# 2026-10-14-052 · En criollo: la mosca entera con SparseLTC prende lo mismo que el modelo validado de Shiu y sus barajados no; la motora de la trompa queda sin decidir, y el lugar natural es el Paper 2

**Fecha:** 2026-10-16, 11:55 (America/Buenos_Aires)
**Doc:** https://app.clickup.com/90171457413/docs/2kza6fw5-23617

## Pedido

«En criollo que logramos. Como se relaciona con los tres papaer y las aplicaciomes» (Abraham, 16-oct 11:41), justo después de la 051. Lo leo así: «logramos» es la línea de la mosca entera con líquidas, de la 045 a la 051 (tu intuición del 15-oct a las 23:01). El resto del laboratorio entra sólo donde se cruza.

## Veredicto primero

- **[MEDIDO] Qué logramos.** Corrimos el cerebro entero de la mosca (138.639 neuronas, 15.091.983 conexiones) con la ecuación SparseLTC del laboratorio y lo pusimos al lado de una vara de afuera: el modelo LIF de Shiu et al. (Nature 2024), validado con optogenética en moscas. Primero lo reprodujimos exacto: MN9 dispara en 30 de 30 ensayos con el cableado real y en 0 de 20 barajados (049).
- **[MEDIDO] El mapa sí.** Con azúcar, SparseLTC prende 172 de las 321 neuronas que prende el LIF (J 0,366); el mejor de 80 barajados llega a 103 y un rival sin dinámica, a 131 (049). Con el umbral de la 051, J 0,332 contra 0,182 del mejor barajado. Dos corridas, dos veces SOSTENIDA.
- **[MEDIDO] La salida fina, todavía no.** MN9 es una motora de ingestión (nervio faríngeo, según las anotaciones de FlyWire). Sin umbral queda REFUTADA: se ahoga entre 48.407 neuronas encendidas y 18 de 80 barajados la igualan (049). Con el umbral que deja el presupuesto del LIF entra en el puesto 269 de 321 y queda en cero en 79 de 80 barajados; el que llega es el mismo nulo k32 en las dos corridas: SIN_DECIDIR (051).
- **[MEDIDO] Lo que no paga.** La compuerta líquida cae en el mismo punto fijo que la tasa (REFUTADA_DEGENERADA, 049) y el umbral no mejora el conjunto (GANA REFUTADA, 051). El resultado lo carga el cableado con sus pesos y signos, no la neurona líquida.
- **[CONCLUSION] Letra chica.** Todo es coincidencia con un modelo validado, no con la mosca viva: Shiu validó MN9 y algunas neuronas, no las 321. Y la destilación (sacar el subgrafo mínimo y empaquetarlo) sigue cerrada, porque pedía MN9 firme.
- **[CONCLUSION] Paper 1 (publicado).** Ningún número cambia. Le suma una vara de afuera a su tipo de simulación (cerebro entero, sin entrenar, SparseLTC): la propagación prende el conjunto del LIF validado y los barajados no. No dice nada de la amplificación temporal del título, porque acá la lectura es el punto fijo.
- **[CONCLUSION] Paper 2 (a reescribir).** Es donde entra. Es el segundo reflejo, después del escape, en que el cableado exacto le gana a sus barajados, y el primero contra un modelo validado en moscas. Encaja con la reescritura alrededor de H_LECTOR y H_TAU_LIBRE: el cableado es necesario; la salida fina y el mejor lector no los resuelve.
- **[CONCLUSION] Paper 3 (estructural).** Lo toca de costado: MN9 es una motora de la boca, justo la salida donde el Paper 3 encontró el plus propio del cerebro central (×1,31 y ×1,16; aguanta FDR, no FWER). Que el camino azúcar a MN9 pase por el central es NO MEDIDO.
- **[CONCLUSION, opinión] Aplicaciones.** Aparece una nueva: un simulador barato de «qué se prende» con un estímulo, para elegir qué neuronas mirar o silenciar antes de un experimento (unos 3,7 s por corrida del cerebro entero en un runner gratis, 2,25 GB). El banco sellado se fortalece como servicio de evaluación: esta vez se midió contra un modelo de afuera, el humo le encontró dos fallas al sello y mi apuesta escrita falló, o sea que puede dar rojo. Compresión, reflejo de choque y portero sensorial quedan donde estaban.

## Qué aporta a cada paper

| Paper | Qué es hoy | Qué le suma la mosca entera | Qué no le suma |
|---|---|---|---|
| 1 | v2.0 publicada (10.5281/zenodo.23393412): cómo viaja la señal por el cerebro entero sin entrenar | Una vara externa para su tipo de simulación | La amplificación temporal; si su configuración de SparseLTC es esta, NO MEDIDO |
| 2 | Esqueleto, a reescribir alrededor de H_LECTOR y H_TAU_LIBRE | Un capítulo: segundo reflejo, cerebro entero, vara validada; CONJUNTO dos veces SOSTENIDA, MN9 SIN_DECIDIR | Ni el lector ni la salida fina; nada en moscas vivas |
| 3 | Esqueleto estructural: quién alimenta cada salida, con nulo regional y la réplica en BANC propuesta | Un ejemplo funcional sobre una motora de ingestión | Ningún número |

## Aplicaciones (las de la 009, frente a la 045 a 051)

| Aplicación | ¿Cambia? |
|---|---|
| Simulador barato de reclutamiento | Nueva: J 0,33 a 0,37 contra el LIF; 3,7 s por corrida y 2,25 GB en Actions |
| Banco de evaluación sellado | Más fuerte: primera vez contra un modelo externo validado |
| Nulos que conservan grado y zona (Paper 1) | Igual |
| Subgrafo mínimo (compresión) | Sigue hipótesis: la destilación no se habilitó |
| Reflejo de choque, portero sensorial, aviso por vibración | Igual: salen del escape (R2 y la regla), y el cerebro entero ya daba lo mismo que R2 (factorial 4) |
| SparseLTC para el borde | Matiz: para «qué se prende» alcanza la tasa; la compuerta líquida no cambia la lectura |

## Herramientas y máquina

- **Conector GitHub:** CONTEXTO en `e187648` (md5 e76ac427d210230dcf4101cd3ea41b30) y las respuestas 2026-10-14-007, 009, 035, 049 y 051.
- **brain-env:** anotaciones de FlyWire pinneadas (`/tmp/annotations.tsv`, md5 719904ab): MN9 es `motor`, `brain_motor_neuron`, `ingestion_motor_neuron`, nervio `PhN`; prueba del parche del CONTEXTO sobre una copia.
- **Actions:** los tiempos son los de la 051 (CORRER, run 38912718970). Sin corridas nuevas.

## Archivos

| Archivo | md5 |
|---|---|
| `tools/contexto/actualizar_contexto_2026-10-14-052.py` (`main`) | 80943db8309c4f7885a9d1fa857fe985 |
| CONTEXTO antes y después del parche (copia en brain-env; la segunda pasada aborta) | e76ac427d210230dcf4101cd3ea41b30 y 84908d5339f30a6116c7ce40c16ec8ea |

## NO MEDIDO

- Nada fuera de simulación.
- Paridad con el runtime SparseLTC de Mojo/C++: todo esto es numpy disperso.
- Si la configuración de SparseLTC del Paper 1 es la de la 049 y la 051.
- Que el camino azúcar a MN9 pase por el cerebro central.
- El costo contra el LIF de Shiu en las mismas condiciones.

## Antes de firmar

| Afirmación | Instrumento | ¿Podía dar rojo? | Veredicto |
|---|---|---|---|
| Los números son los de git | agregados de la 049 y la 051 (md5 verificados en la 051) y CONTEXTO en `e187648` | Sí | PASA |
| MN9 es una motora de ingestión | anotaciones de FlyWire pinneadas (`17fc577`) | Sí: podía ser otra clase | medido |
| Qué aporta a cada paper | lectura de los esqueletos citada en la 007 y la 035 | Parcial: es interpretación | CONCLUSION |
| Aplicaciones | opinión sobre resultados medidos | No | OPINION declarada |
| El parche del CONTEXTO aplica | copia de `main` en brain-env; segunda pasada aborta | Sí | medido |

--- METODO PROMETEO ---
Rol: síntesis (chica). Delicado: no.
Máquinas: conector GitHub, brain-env (anotaciones y parche).
Archivo: `docs/agents/respuestas/2026-10-14-052-en-criollo-la-mosca-entera-y-los-tres-papers.md` en `main`.
Doc: https://app.clickup.com/90171457413/docs/2kza6fw5-23617
