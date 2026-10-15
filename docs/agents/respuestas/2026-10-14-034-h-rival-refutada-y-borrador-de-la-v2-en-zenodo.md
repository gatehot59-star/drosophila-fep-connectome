# 2026-10-14-034 · H_RIVAL REFUTADA: con lector entrenado sobre las mismas 564 entradas, un ridge le gana a la mosca por 5 puntos; contra la regla con τ la ventaja es +1,19 y queda sin decidir; la v2 del Paper 1 quedó en borrador en Zenodo, sin publicar

## Pedido
- Abraham, 15-oct 07:36: «corre h rival completo en action o en kaggle. donde demore menos».
- 07:50: el token de Zenodo (no se reproduce en ningún archivo) y «carga los dos paper el v2 del paper 1 y el paper 2 y el paper 3, luego de la carga eliminaré este token».
- 08:06: «te pasé el token de zenodo».

## Veredicto primero
- [MEDIDO] **H_RIVAL REFUTADA en la máquina que decide.** Actions x64, run 38721794594, disparado por el `CORRER` (`000d486`, 07:39) y commiteado por el bot en `576fc4c` (07:48): 9 minutos. CHEQUEO VALIDO: en las 6 celdas pasan PIN, REPRO_REGLA, REPRO_W, REGLA_TAU_NULA, CONTROL_NEGATIVO, GUARDA_FUGA, F3_CELDA, HTAU_CELDA y R2_TAMANO; CONTROL_RIDGE_015 da 6/6 exacto (0,9935, 0,9595, 0,9935, 0,9575, 0,9940 y 0,9590) y CONTROL_MLP_005 pasa.
- [MEDIDO] **Acierto medio en las pruebas 12 a 21:**

| Celda (A · ruido) | Mosca (W elegida) | RIDGE | MLP | REGLA_TAU | Regla propia |
|---|---|---|---|---|---|
| 0,0 · 0,15 | 0,9463 | 0,9988 | 0,9957 | 0,9352 | 0,9267 |
| 0,0 · 0,45 | 0,9431 | 0,9924 | 0,9939 | 0,9311 | 0,9250 |
| 0,3 · 0,15 | 0,9466 | 0,9986 | 0,9933 | 0,9332 | 0,9287 |
| 0,3 · 0,45 | 0,9416 | 0,9899 | 0,9879 | 0,9308 | 0,9234 |
| 0,6 · 0,15 | 0,9467 | 0,9987 | 0,9911 | 0,9329 | 0,9289 |
| 0,6 · 0,45 | 0,9413 | 0,9894 | 0,9912 | 0,9310 | 0,9259 |

- [MEDIDO] **Primaria** (D = mosca menos rival; bootstrap de las 10 semillas de prueba, IC con Bonferroni por 3 rivales; margen de 1 punto, como dice el sello):
  - RIDGE: D = -0,0503 [-0,0516, -0,0488]: NO_SUPERA (pierde: el techo es menor que 0).
  - MLP: D = -0,0479 [-0,0494, -0,0465]: NO_SUPERA (pierde).
  - REGLA_TAU: D = +0,0119 [+0,0096, +0,0150]: SIN_DECIDIR. El piso queda 0,04 puntos debajo del margen.
  - **VEREDICTO H_RIVAL = REFUTADA; H_TAU_JUSTO = SIN_DECIDIR.**
- [MEDIDO, descriptivo, no decide] **Secundaria** (10 semillas de τ por 10 de prueba, F3): RIDGE -0,0590 [-0,0691, -0,0514]; MLP -0,0568 [-0,0671, -0,0491]; REGLA_TAU +0,0032 [-0,0068, +0,0106].
- [CONCLUSIÓN] **Qué dice.** Con un lector entrenado sobre las mismas 564 entradas crudas, un ridge común acierta entre 98,9 y 99,9%, y la mosca entre 94,1 y 94,7%. Para leer estas entradas, el cableado de la mosca no es el mejor camino: pierde por 5 puntos, y el MLP le gana por lo mismo. Contra la regla a mano, la ventaja de la mosca era de 1,78 puntos de media; si a la regla le damos un integrador con τ elegida igual que la de la mosca, baja a 1,19 (cuenta sobre las medias de la tabla). Con la variación entre redes (secundaria) queda en 0,32, con un IC que cruza el 0. Un tercio de la ventaja sobre la regla era elegir la τ, y lo que queda no llega al punto declarado.
- [CONCLUSIÓN] **Qué no dice.** No mide costo: tamaño, memoria, energía y latencia de cada lector en un microcontrolador quedan NO MEDIDOS. No toca H_REUSO, que es estructural (2026-10-14-030). Vale para esta tarea (`tarea_mosca`, 564 entradas, 6 celdas).
- [MEDIDO] **La v2 del Paper 1 quedó en borrador en Zenodo, sin publicar.** `tools/zenodo/depositar_v2.py --borrador` (el script del PR #27, mergeado el 14-oct), desde un clon limpio de main (`fe4a088`) y con `--verificar` PASS antes: metadatos 8/8 y los 2 PDF con su md5.
  - Nueva versión del concepto 10.5281/zenodo.19136947: borrador **23393412**, DOI reservado **10.5281/zenodo.23393412**, para revisar en https://zenodo.org/deposit/23393412.
  - Sacó el PDF heredado de la v1.0 («Paper1_SignalPropagation (1).pdf») y subió el manuscrito (18 páginas, 332.607 B) y el erratum (15 páginas, 191.172 B). El md5 que calculó Zenodo es el sellado: 6e849bf2 y 05052e6e.
  - Metadatos aceptados: el título de la v2, versión 2.0, preprint, CC BY 4.0, acceso abierto, fecha 2026-10-15.
  - Chequeo aparte, con otro script: el depósito da estado `unsubmitted`; el registro público 23393412 da 404; la v1.0 sigue publicada (200, versión 1.0).
- [NO HECHO, a propósito] **El Paper 2 y el Paper 3 no se subieron.** Son esqueletos: `docs/paper2/paper2-esqueleto.md` (rama `titan/paper2-esqueleto-2026-10-14`, 12.340 B, 3 NO MEDIDO y 5 PENDIENTE) y `docs/paper3/paper3-esqueleto.md` (rama `titan/paper3-esqueleto-2026-10-14`, 10.880 B, 3 NO MEDIDO y 1 PENDIENTE). No tienen manuscrito, PDF, metadatos ni script de depósito. Un DOI publicado no se borra, y H_RIVAL, el rival entrenado que pidió Fable, todavía no está en ninguno de los dos.
- [ABIERTO] **Antes de publicar la v2.** El título dice «Non-Trivial Temporal Amplification». Esa afirmación descansa, al menos en parte, en la Tabla 8, que el propio manuscrito declara no reproducible (Limitación 5: el script que la produjo no está en el archivo). Fable pidió reproducir Z_CP y la RDI con 100 realizaciones o más, o sacarlas del título y del resumen (2026-10-14-031); el resumen de los metadatos las nombra una vez cada una. En un borrador se cambian archivos y metadatos sin costo; publicado, no.
- [SEGURIDAD] **El token.** Se usó dos veces, como variable de entorno de un proceso (el borrador y el chequeo). No quedó en disco, en git, en los recibos ni en este archivo (medido: no existe `/workspace/.zenodo_token`; el recibo y la salida no contienen su valor). Quedó escrito en el chat: conviene revocarlo cuando termine el depósito.
- [NO MEDIDO] **La réplica en brain-env.** brain-env se detuvo a las 07:58 (código 255, sin marca de falta de memoria), 17 minutos después de empezar la réplica y todavía en CONTROL_RIDGE_015. Lo volví a levantar a las 08:11 (`docker start brain-env` en el host, nada más), guardé lo que había quedado en `out_brain_caida_0758` y relancé la réplica a las 08:18, en serie y con prioridad baja (`nice`): unas 9 horas. CONTROL_RIDGE_015 ya terminó en brain-env (137 s) y da 6 de 6 líneas iguales a Actions, sin contar los tiempos. El sello dice que si una etiqueta por rival difiere entre máquinas, pasa a SIN_DECIDIR (NO_SE_REPLICA): hasta el cotejo de las 6 celdas, REFUTADA es de Actions.
- [COSTO] Actions: 9 minutos (trabajos de 46 s a 8,5 min, en paralelo). Kaggle no se midió con este instrumento ni está en el sello; con el humo, Actions era la más rápida medida (c0: 83 s contra 688 s en brain-env).

## Herramientas y máquina
- **Actions x64.** Run 38721794594: 7 trabajos de medición y el agregado, todos bien.
- **brain-env.** Python 3.12.14, 2 núcleos. Clon limpio de main para el depósito (`depositar_v2.py --verificar` y `--borrador`) y `verif_borrador034.py` para el chequeo; clon limpio de la rama del rival para verificar `MD5SUMS.txt` (23 de 23); prueba del parche del CONTEXTO en copia; réplica relanzada con nohup.
- **Host, por el gateway.** `docker inspect` y `docker start brain-env`.
- **Zenodo, API de depósitos.** Lectura de la v1.0, nueva versión, archivos y metadatos del borrador. Publicar no se llamó.
- **GitHub.** Lectura de ramas y PRs; push de esta respuesta, el recibo, el parche y su workflow; md5 desde clon limpio.
- Acción delicada: el borrador en Zenodo. Es reversible (se puede descartar); publicar, no se hizo.

## Archivos
| Archivo | md5 |
|---|---|
| `results/rival_2026-10-15/CORRER` (`000d486`) | d141afa387efe1757a190ba57d07abdf |
| `results/rival_2026-10-15/agregado.log` (bot `576fc4c`) | 38d473cc7603ab3f9def1cd931042179 |
| `results/rival_2026-10-15/agregado.json` | 03c9d86c432c604f30d060354159091e |
| `results/rival_2026-10-15/MD5SUMS.txt` (23 de 23 OK desde clon limpio) | 78477d7a099e3399333309126a42ee6d |
| `docs/v2/recibo-borrador-v2.0.json` (main, este commit) | b8872a5cc9ab6887ff252fb0c473618f |
| `tools/zenodo/depositar_v2.py` (main `fe4a088`) | 2056570ec55fd6a5c621c9bb5a87caba |
| `docs/v2/zenodo-v2.0-metadata.json` | 3c2b0b36f967b691b516a12111db5b70 |
| `docs/v2/archivos-deposito-v2.0.json` | 0ed096b51792154aca992de2b625f133 |
| PDF del borrador (binarios, no se commitean) | 6e849bf2caffa540165edd826df102ed y 05052e6e7e0dd79cee584c9d285b1b93 |
| `tools/contexto/actualizar_contexto_2026-10-14-034.py` (main, este commit) | 56eb136ff1e9f2ed0e7f716530c20306 |
| `.github/workflows/contexto-2026-10-14-034.yml` (se borra al aplicarse) | 73488a0b55a20859e0e18c65f41c152e |
| CONTEXTO antes y después del parche (probado en copia; la segunda aplicación aborta) | 36480f72e75a1ae412b24ea1818735bd y e8b496276efc8eaaf45a818e45e9831f |

Doc de ClickUp: [034](https://app.clickup.com/90171457413/docs/2kza6fw5-22897).

## NO MEDIDO
- La réplica de las 6 celdas en brain-env y el cotejo de etiquetas entre máquinas (corre desde las 08:18).
- Costo, tamaño y latencia de cada lector en un microcontrolador.
- Los PDF a ojo: la maquetación se revisa en el borrador.
- Z_CP y la RDI con 100 realizaciones o más; la Tabla 8.
- W con 30 semillas de τ; la regla con ganancia o umbral por tipo.
- Kaggle con este instrumento.

## Antes de firmar
| Afirmación | Instrumento | ¿Podía dar rojo? |
|---|---|---|
| H_RIVAL REFUTADA | agregador sellado sobre las 6 celdas, con sus controles | Sí: con el ridge roto, CONTROL_RIDGE_015 no daría exacto; con otros ensayos, REPRO_REGLA y REPRO_W fallarían. Todo dio verde |
| No es cosa de una máquina | réplica en brain-env | Todavía no: NO MEDIDO, salvo CONTROL_RIDGE_015 (6 de 6 iguales) |
| El borrador tiene los PDF sellados | md5 que calcula Zenodo contra el sellado | Sí: lo calcula Zenodo, no el script |
| No se publicó nada | GET sin token al registro público 23393412 | Sí: daría 200 publicado; dio 404 |
| El token no quedó en archivos | búsqueda de su valor en el recibo y la salida; el archivo del token | Sí; ausente |
| Lo commiteado es lo probado | md5 desde clon limpio | Sí |

--- METODO PROMETEO ---
Correr lo sellado sin tocar el sello ni el instrumento, y leer primaria, secundaria y controles por separado. Depositar solo en borrador, con el script del PR #27 y un chequeo independiente; no publicar sin el sí de Abraham; no subir esqueletos. El token, solo en la memoria de un proceso.
Máquina: Actions x64, brain-env y el host (docker start). Artefactos: este archivo en main, el recibo del borrador y su Doc en ClickUp.
