# 2026-10-14-002 · BANC conserva las conexiones fuertes de R2 (92,4 % con 20 sinapsis o más); el núcleo quedó aparte y sellado; H_TAU sellado

**Pedido.** 14-oct 08:18: «SELLA EL H_TAU Y CONSERVA POR APARTE EL NUCLEO, BAJAR BANC». 10:51: ClickKit `terminar_sellos_002` («Terminar los sellos»).

## Veredicto primero
- **[MEDIDO] BANC está bajado y verificado.** `banc_888_meta.feather` (57.503.026 bytes, md5 `8c2b93a6`) y `banc_888_edgelist_simple_v3.feather` (359.161.658 bytes, md5 `08542b07`, 13.620.865 aristas) dan el mismo md5 que publica el bucket. Las aristas usan los IDs `root_888`, no `root_id`.
- **[MEDIDO] Las 6 descendentes del banco tienen pareja del mismo tipo en BANC** (DNp01, DNp07 y DNp06, izquierda y derecha). De las 564 entradas, 291 (51,6 %) tienen pareja única por `fafb_match` y 363 (64,4 %) por alguna vía. De las 33.489 neuronas de R2, 9.510 (28,4 %).
- **[MEDIDO] Lo que se repite entre las dos moscas son las conexiones fuertes.** De las 782.453 aristas de R2 que se pueden evaluar (19,4 %), el 39,8 % está en BANC. Por fuerza en FlyWire: 1 a 4 sinapsis 28,9 %; 5 a 9 60,0 %; 10 a 19 77,2 %; 20 o más **92,4 %**. El núcleo de Schlegel se conserva **77,0 %** contra **32,7 %** del resto (con 5 sinapsis o más en BANC: 51,1 % contra 6,1 %).
- **[MEDIDO] El núcleo quedó como pieza aparte:** 603.219 de 4.031.897 aristas (**14,96 %**) cargan **9.668.248 de 16.971.919 sinapsis (56,97 %)**; 6/6 descendentes con entrada y 563/564 entradas con salida. Huella `69255109`, igual en brain-env (dos veces) y en Actions.
- **[SELLADO, sin correr] H_TAU** y **[SELLADO, sin correr] H_CONSENSO + H_CABLEADO_NUCLEO**, cada uno con instrumento, agregador probado 6/6, humo en Actions y SELLO propio. Corren solo cuando Abraham pushee su `CORRER`.
- **[CONCLUSIÓN]** Es la primera medición a favor de la «fábrica de partes» (2026-10-13-018): la parte fuerte del cableado es la que se repite en otra mosca. Todavía sin nulo de parejas al azar, y sin saber si esa parte carga el reflejo: eso lo decide H_CONSENSO.

## Herramientas y máquina
- brain-env (CPU, sin GPU): descarga de BANC por HTTPS del bucket público, `tools/banc/emparejar_banc.py` y `tools/nucleo/nucleo_mosca.py --modo construir`.
- GitHub Actions x64: humo de los dos sellos (rama `titan/htau-nucleo-banc-2026-10-14`).
- Sandbox de ClickUp: escritura de los instrumentos y prueba de los agregadores.

## Qué se midió
1. BANC: descarga y md5 contra `x-goog-hash` del bucket.
2. Parejas FlyWire → BANC (`fafb_match` y `fafb_nblast_match`, solo 1 a 1) de las 6 DN, las 564 entradas y R2.
3. Presencia en BANC de las aristas de R2 con las dos puntas emparejadas, por tramo de fuerza y núcleo contra resto.
4. El núcleo de Schlegel de R2 como pieza suelta (huella).
5. El humo de H_TAU y del núcleo en Actions.

## Evidencia cruda
- `results/banc_2026-10-14/emparejar_banc.log` (`b39df7f9`), `emparejar_banc.json` (`84c5e42c`), `nucleo_construir.log` (`66e62422`), `nucleo_R2_resumen.json` (`1e1580e8`).
- Corrección en el camino: la primera corrida empareó las aristas con `root_id` y dio 20,8 %. Un chequeo mostró que los 169.078 IDs de la lista de aristas están todos en `root_888` y solo 153.161 en `root_id`. Con `root_888` dio 39,8 %. Esa primera corrida no vale.
- `fafb_match` es en parte por tipo: 13.173 IDs de FlyWire apuntan a más de una neurona de BANC (hasta 120). Por eso solo se usan las parejas únicas (25.492).
- Humo en Actions: H_TAU (bot `0cffc8d`) REPRO_R2 a tamaño real **True** (0,9465 / 0,9375 / 0,9235, exacto el factorial 3), corrida corta VÁLIDA, agregador 6/6. Núcleo (bot `fb54d9f`) NUCLEO_tamano **True** en Actions, grilla y nulos cortos VÁLIDOS con guardas True, agregador 6/6. Velocidad: R2 0,146 s por ensayo, núcleo 0,045 s.

## Archivos
- Rama `titan/htau-nucleo-banc-2026-10-14`: `tools/htau/` (`htau_mosca.py` `2006cfef`, `agregar_htau.py` `0baa11d8`, `prueba_agregar_htau.py` `36237b44`, `SELLO-HTAU.md`); `tools/nucleo/` (`nucleo_mosca.py` `4697c81d`, `agregar_nucleo.py` `cb8a797b`, `prueba_agregar_nucleo.py` `34f671ec`, `SELLO-NUCLEO.md`); `tools/banc/emparejar_banc.py` (`0c7a0dbf`); los workflows `htau-humo`, `htau-mosca`, `nucleo-humo` y `nucleo-mosca`; `results/banc_2026-10-14/`, `results/htau_2026-10-14_humo/` y `results/nucleo_2026-10-14_humo/`.
- Commits en la rama: `c566784` (H_TAU), `41deb02` (núcleo y BANC), `fb54d9f` y `0cffc8d` (humo, del bot), `4f4e672` (los dos SELLO). Todos los md5 verificados desde un clon fresco.
- Doc de ClickUp: https://app.clickup.com/90171457413/docs/2kza6fw5-22097

## NO MEDIDO
- H_TAU, H_CONSENSO y H_CABLEADO_NUCLEO: sellados, sin correr.
- Nulo del emparejado BANC (parejas al azar con el mismo grado): sin él, el 39,8 % solo se compara entre tramos.
- Emparejado por tipo de célula (solo hay por neurona individual con pareja única).
- El banco corrido sobre el cableado de BANC (H_OTRA_MOSCA).
- El bucket es mutable; no se usó la copia con DOI de Dataverse (doi:10.7910/DVN/7WTH1N).
- El núcleo de Schlegel es una aproximación dentro de FlyWire, no un consenso real entre moscas.

## Antes de firmar
| afirmación | instrumento | ¿podía dar rojo? | veredicto |
|---|---|---|---|
| BANC bajado entero | md5 local contra el md5 del bucket | sí, un byte cambiado lo rompe | verde |
| 6/6 DN con pareja | `fafb_match` único y tipo en BANC | sí, podían faltar o venir de otro tipo | verde |
| las aristas fuertes se conservan más | presencia por tramo, mismo emparejado | sí, podía dar plano | verde, sin nulo |
| el emparejado de aristas usa el ID correcto | chequeo `root_888` contra `root_id` | sí, y dio rojo con `root_id` | corregido |
| el núcleo es reproducible | huella en 3 corridas y 2 máquinas | sí, la huella cambia con una arista | verde |
| los agregadores deciden bien | 6 casos sintéticos cada uno, con casos inválidos | sí, el de regla distinta falló primero y se arregló | verde |
| H_TAU sellado | REPRO_R2 a tamaño real en Actions | sí, otro número lo invalida | verde (exacto) |
| núcleo sellado | NUCLEO_tamano en Actions | sí | verde |

--- METODO PROMETEO ---
Accion delicada: no (no se corrió ningún experimento ni se mergeó nada; los dos `CORRER` esperan a Abraham).
Maquina: brain-env (CPU) + GitHub Actions x64 + sandbox de ClickUp.
Artefactos: docs/agents/respuestas/2026-10-14-002-banc-conserva-las-conexiones-fuertes-nucleo-aparte-y-dos-sellos.md + rama titan/htau-nucleo-banc-2026-10-14 + Doc de ClickUp https://app.clickup.com/90171457413/docs/2kza6fw5-22097
