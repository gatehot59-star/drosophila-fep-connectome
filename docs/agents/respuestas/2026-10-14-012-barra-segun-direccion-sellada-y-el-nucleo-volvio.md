# 2026-10-14-012 · La barra según su dirección quedó sellada y espera su CORRER; el núcleo volvió: le gana a sus barajados pero pierde 4,6 puntos contra R2

**Pedido.** 14-oct 13:05: ClickKit `topo_nuevo_barra_011`. Antes de sellar avisé que la barra ya estaba en la tarea de la 015. 13:07: «Dale con la barra según su dirección».

## Veredicto primero
- **[MEDIDO, lectura del código sellado] La barra sola no era nueva.** En `tarea_mosca.generar` (40d64e07), `y[vuelo & ((est == 1) | (est == 3))] = 2`: la barra (est 3, `direc = -1`, de adelante hacia atrás) ya era «aterrizar» en vuelo. En `sintonias`, `lplc4 = ba + ...`. Sellarla como nueva no podía dar rojo.
- **[SELLADO, sin correr] H_TOPO_NUEVO con la barra según su dirección.** Rama `titan/topo-barra-dir-2026-10-14`, en un orden verificable:
  - A, la tarea (`42d2f60`, `tarea_barra_dir.py` d2515357);
  - B, el programa (`2deb335`, `aterrizaje_dir.topo` 0122a4ce);
  - C, el banco (`8c7cf1b`, `banco_barra_dir.py` c033f214, workflows 758715aa y c1d05b78);
  - el sello (`afc2585`, `tools/topo_barra/SELLO-BARRA-DIR.md`).
  - Los md5 se verificaron en un clon limpio.
- **[LITERATURA] La etiqueta nueva** (en vuelo, barra de atrás hacia adelante → girar alejándose) tiene fuente indirecta:
  - Ache 2019, Supp Fig 5d: las descendentes de aterrizaje tienen sintonía de dirección, y otras direcciones son «less effective».
  - Kim 2023: LPLC2 «stronger responses to back-to-front motion than to front-to-back motion for both bars and spots», y DNp06 es selectiva a la dirección de la barra.
  - La conducta exacta no está medida como número: queda declarado.
- **[MEDIDO] La tarea pasa sus chequeos:**
  - SINTONIAS_015_IGUAL exacto en las 3 amplitudes;
  - 24 condiciones con 100 ensayos cada una;
  - dirección con A = 0,3: LPLC4 AA 0,704 > AD 0,207; LPLC1 AD 0,690 > AA 0,352; LPLC2 AD 0,207 > AA 0,106.
- **[MEDIDO] Humo del banco en brain-env** (3 nulos, 600/400): REPRODUCE_M46 True, guardas True, EXIT_RUN=0, 40,8 s; log md5 `55761c49`.
  - El veredicto de humo es REFUTADA, mecánicamente: con 3 nulos el p mínimo es 0,25. No vale.
  - Vi sus números antes de sellar y no cambié nada.
- **[NO MEDIDO]** El humo en Actions ya está disparado (`HUMO`). La corrida completa espera `results/topo_barra_2026-10-14/CORRER`.
- **[MEDIDO] El núcleo volvió** (bot `a522bc4`, `results/nucleo_2026-10-14/agregado.log`): VEREDICTO_GLOBAL VALIDO, con todos los chequeos en True (plan 600/600, 50 + 50, REGLA_IGUAL_F3 60/60, REAL_IGUAL 0,9135).
  - **H_CONSENSO REFUTADA.** Núcleo menos R2 = −4,59 puntos (0,8894 contra 0,9353), IC90 [−5,07; −4,10]. PIERDE en las 6 celdas (−2,97 a −5,93) y en 600 de 600 corridas.
  - **H_CABLEADO_NUCLEO SOSTENIDA.** 0,9135 contra 50 SL (media 0,5913, máximo 0,7570) y 50 T (media 0,6869, máximo 0,7680). Ninguno iguala al real; Holm 0,0392 en los dos.
  - **Descriptivo:** el núcleo pierde −3,74 puntos contra la regla con los mismos sensores.
- **[CONCLUSIÓN]** Lo que se repite entre moscas es cableado específico (le gana a sus barajados), pero no carga el reflejo solo: las conexiones débiles ponen unos 4,6 puntos. Es el segundo de los dos desenlaces que el Paper 2 dejó escritos de antemano (§3.6). La lectura completa, por tau y qué aristas pesan, está pendiente.

## Herramientas y máquina
- Web: Ache 2019 (*Nature Neuroscience*, texto completo y Supp Fig 5) y Kim 2023 (*Current Biology*).
- brain-env (CPU): la tarea, el programa y el banco, sus chequeos y el humo; clon limpio para los md5; lectura del agregado del núcleo; prueba del parche.
- GitHub (conector): una rama nueva y cuatro commits en orden; esta respuesta en main.
- Actions: solo el humo de la barra. La corrida completa no se disparó.

## Archivos
- Rama `titan/topo-barra-dir-2026-10-14`: `tools/topo_barra/{tarea_barra_dir.py, aterrizaje_dir.topo, banco_barra_dir.py, SELLO-BARRA-DIR.md}`, `.github/workflows/barra-dir-{mosca,humo}.yml`, `results/topo_barra_2026-10-14_humo/HUMO`.
- Esta respuesta.
- `tools/contexto/actualizar_contexto_2026-10-14-012.py` (md5 `16bc2c32`; probado en copia: b110345f → 34073659; la segunda aplicación aborta).
- `.github/workflows/contexto-2026-10-14-012.yml`.
- Doc público: https://app.clickup.com/90171457413/docs/2kza6fw5-22297

## NO MEDIDO
- La corrida completa de H_TOPO_NUEVO.
- El humo en Actions de la barra.
- H_TAU.
- La lectura completa del núcleo.
- El nulo BANC.
- El supuesto más débil de la tarea: que LPLC4 responde 0,3 a la barra de atrás hacia adelante.

## Antes de firmar
| Afirmación | Instrumento | ¿Podía dar rojo? | Veredicto |
|---|---|---|---|
| La barra sola no era nueva | Lectura de `generar` y `sintonias` sellados | Sí, si la barra no estuviera etiquetada | PASA |
| El programa se escribió después de la tarea y antes de los datos | Orden de commits A, B y C; el humo corrió después de C | Sí: el orden de git lo mostraría | PASA. Lo escribí yo, que también diseñé la tarea; queda declarado |
| El banco no puede dar SOSTENIDA por construcción | En humo dio REFUTADA; la regla y W son funciones distintas (Topo contra `tm.simular`) | Sí | PASA |
| H_CONSENSO REFUTADA | Agregado sellado del bot, con chequeos en True | Sí: con el núcleo dentro de 1 punto hubiera dado otra cosa | PASA |

--- METODO PROMETEO ---
Accion delicada: sí para el humo en Actions (disparado; es corto y sin valor). La corrida completa no se disparó: espera el CORRER de Abraham.
Maquina: brain-env CPU + web + conector GitHub + Actions (humo).
Artefactos: `titan/topo-barra-dir-2026-10-14` `afc2585`; esta respuesta en main; Doc https://app.clickup.com/90171457413/docs/2kza6fw5-22297
