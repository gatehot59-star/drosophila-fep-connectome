# CONTEXTO VIVO · conectoma / paper / H4

**Última actualización:** 2026-10-15, 22:22 (America/Buenos_Aires), con la respuesta 2026-10-14-043. **La sección «Madrugada y mañana del 13-oct» manda sobre lo que choque en el resto del archivo; después, la de «Tarde y noche del 12-oct (010 a 018)»**, que sigue escrito al estado de la 009 (11:58).
**Estado canónico:** `main`, con las respuestas del 10, 11 y 12 de octubre. H4 auditado en `a4f5a8e9143173bf609eff430bcca3d5d8699c48`.
**Base vigente del paper:** en `main`, `docs/ERRATUM.md` anterior a la revisión; **la versión para depositar está en el PR #27** (erratum revisado, 9 ítems y 12 pendientes, anotaciones pinneadas a `17fc577`, y el manuscrito `docs/v2/paper1-v2.0.md`). **Zenodo tiene sólo la v1.0** (20-mar).

## Madrugada y mañana del 13-oct (019 a 2026-10-14-043) · manda sobre el resto

- **Factorial sellado (019) y corrido (2026-10-13-002): VÁLIDO 9/9.** Rama `titan/factorial-mosca-2026-10-13`: sello `552942f`, resultados del bot `5c4fbac`, post-hoc `19a508c`. El ancla reproduce la 015 exacta en brain-env y en Actions.
  - Veredicto sellado: ALGÚN FACTOR CIERRA LA BRECHA (R1_CON_TASA, R1_CON_LIQ, R1_SIN_LIQ). M46 pierde con las tres neuronas, como en la 015.
  - **Post-hoc, no sellado:** la regla con las mismas 418 entradas de R1 sube a 0,926-0,930, y R1_CON_TASA y R1_CON_LIQ la IGUALAN en 6/6. El «supera» sellado era tener más sensores.
  - El cableado paga dentro de R1: 0,937 contra 50 SL (media 0,774) y 50 T (0,742), p por rango 0,0196.
  - Factores: recorte AYUDA; inhibición AYUDA (en TASA y LIQ solo con amplitud 0,6); LIQ empata con TASA en R1; el LIF armado (corriente fija, paso de 1 ms) DAÑA.
  - **Lectura:** la brecha de la 015 era nuestro recorte. Con 1.504 neuronas reales, la mosca simulada alcanza a su diseño idealizado; no lo supera.
  - La primera corrida en Actions murió por falta de torch (el módulo de la 003 lo importa arriba); el workflow ahora lo instala (`7534dd2`).
- **Auditoría de Tao entregada y revisada (2026-10-13-001).** PR #28 (`dd9da1c`, 13-oct 00:17) y Doc en el Space. Leyó main en `51e183c`: no vio la 015 completa, la 018 ni la 019.
  - Siguen abiertos en el texto de la v2 (`f19a9c7`): F01 (el nulo de neurópilo sí preserva el in-degree global; medido en el conectoma entero, rama `titan/revision-auditoria-tao-2026-10-13`), F05 (Z_CP +14,8σ sin Tabla 8 reproducible), F06 (con N = 5 no hay p empírica bajo 1/6), F07 (138.142 y 138.140 son dos corridas del control uniforme; citar la de las tablas).
  - Robótica: `adc_to_q15` y `q15_to_pwm` desbordan int32 con `uint16_t` completos; `test_swarm.c` no puede dar rojo.
  - No se le comentó el PR ni se le escribió: espera el visto bueno de Abraham.
- **Síntesis en criollo (2026-10-13-003):** la mosca da el plano (qué tipo de sensor va a qué comando) y, con cableado real suficiente, su simulación lo alcanza; no es un cerebro mejor que su plano ni que la ingeniería.
- **Factorial 2 sellado (2026-10-13-004) y corrido (2026-10-13-007, abajo).** Rama `titan/factorial2-mosca-2026-10-13`, sello `9442fdf` (instrumento `798a824c…`, agregador `150b6f08…`, workflow `b497fe0d…`).
  - La regla usa las mismas entradas que la red (40 en M46, 418 en R1, 564 en R2).
  - τ y ruido por `root_id`: las DN tienen el mismo τ en los tres recortes.
  - Semillas: τ 0..9 × prueba 2..11 (R2: 3 × 5).
  - Margen 0,01, con bootstrap de dos vías y Bonferroni sobre 7.
  - R2 (33.489 neuronas, 4.031.897 aristas) va a Actions y no a Kaggle: 0,79 s por ensayo en brain-env, techo de 2,7 h por trabajo.
  - Humo 8/8 VÁLIDO y ancla exacta.
  - Se dispara pusheando `results/factorial2_2026-10-13/CORRER`.
- **Posicionamiento (2026-10-13-005): no hay neurona nueva.**
  - La líquida nativa de SparseLTC (τ / (1 + g·|drive|)) es de la familia LTC (Hasani et al., AAAI 2021).
  - La que ganó entrenada en el escape (t = sigmoid(b + Vx·x + Vh·z), z ← (1 − t)·z + t·tanh(·)) es la actualización de una GRU sin compuerta de reset (Cho et al., EMNLP 2014); en DualBrain lleva además LayerNorm.
  - Antecedentes directos: LTC sobre cableado inspirado en C. elegans (Lechner et al., Nat Mach Intell 2020) y τ entrenadas por tipo sobre 45.669 neuronas del sistema visual de la mosca (Lappalainen et al., Nature 2024).
  - Lo propio:
    - dinámica líquida sobre el cableado exacto de FlyWire;
    - el banco sellado (nulos SL y T, regla rival, ancla, réplica en Actions);
    - el resultado de que la líquida plena entrenada le gana a su control con los mismos parámetros (013 y 014).
  - Sin entrenar, la nativa empata con la de tasa en R1 (factorial 1).
  - El banco sólo corrió con FlyWire v783; otros conectomas NO MEDIDO (lee columnas de FlyWire).
  - Papers: el Paper 1 (v1.0 en Zenodo, v2.0 sin depositar) y el de DualBrain (feb 2026, `dualbrain/docs/01-paper-dualbrain.md`, depósito NO VERIFICADO; su README marca que faltan `dbc3_motor.h` y el script del benchmark DBC3-v3).
  - Aplicaciones medidas fuera de simulación: ninguna.
- **Factorial 2 corrido (2026-10-13-007): VÁLIDO, 29/29 trabajos, ancla exacta.** Corrida `38396946950`, resultados del bot `798ed97`, 55 min (R2 hasta 31,5 min por trabajo). Diferencia contra la regla con los mismos sensores, margen 0,01:
  - M46_TASA −0,62 puntos (NO_SUPERIOR); M46_LIQ −1,83 (PIERDE).
  - R1, las cuatro configuraciones, entre −1,02 y −1,48 puntos (NO_SUPERIOR); en R1_CON_LIQ y R1_SIN_TASA el intervalo excluye el cero. **Corrige la 002 y la 003:** con 100 corridas por configuración, R1 no alcanza a su diseño; queda alrededor de un punto abajo.
  - **R2_CON_TASA (33.489 neuronas): +1,28 puntos, IC [+0,79; +1,77], NO_INFERIOR**, positiva en las 6 celdas (SUPERA en amplitud 0, ruido 0,15). Es la primera vez que el cableado le gana a su diseño con los mismos sensores, pero por menos del margen: H_SUPERA no sostenida según lo sellado. R2 tiene 3 × 5 semillas.
  - Más sensores pagan: la regla de 418 le gana a la de 40 por +2,79 (AYUDA). R2 menos R1: +1,65 (NO_INFERIOR). LIQ: peor en M46 (−1,21) y equivalente en R1. Inhibición: sin efecto claro.
- **F01, F06 y F07 aplicados en el PR #27 (2026-10-13-006):** bot `1f4a2e0`, manuscrito `2fa575c4…`, sección de dos saltos `23db9cac…`; render de prueba PASS, 18 páginas, `a22515e9…`. **Cerrado en la 2026-10-13-012:** render desde `1f4a2e0` PASS (manuscrito 18 páginas `a22515e9…`, erratum 15 páginas `05052e6e…`, en `/workspace/v2cierre_2026-10-13/deposito_013/` de brain-env), json de depósito `55f3ec63…` y `--verificar` PASS en clon fresco de `e81a903`; con el PDF viejo da FAIL. En el PDF: «Sufficient» 1 → 0, «138,140» 0 → 1, «1/6» 0 → 2. **F05 suavizado en la 2026-10-13-014** (pedido de Abraham, 18:17): `tools/v2/fix_v2_f05_2026-10-13.py` (`da4ace2d…`, 9 reemplazos: resumen, contribuciones, 3.7, discusión, conclusiones, cambio 16 y metadatos de Zenodo), aplicado por el bot en `608bd41` (manuscrito `a4d09d2c…`, igual al de la prueba en brain-env); el +14,8σ y la Tabla 8 se conservan como observación sobre cinco realizaciones, sin reproducir. **La v2 queda lista para depositar:** PDF `6e849bf2…` (18 páginas), erratum `05052e6e…`, json `0ed096b5…`, `--verificar` PASS en clon fresco de `e7fd359` y FAIL con el PDF anterior; los PDF están en `/workspace/v2cierre_2026-10-13/deposito_f05/` de brain-env.
- **Factorial 3 sellado (2026-10-13-008), sin disparar.** Rama `titan/factorial3-mosca-2026-10-13`, sello `6a7b4cb`.
  - Grilla: R2_CON_TASA con τ 0..9 × prueba 2..11 × 6 celdas, con `factorial2_mosca.py` sin cambios (`798a824c…`).
  - Nulos: 50 SL y 50 T de R2 (`tools/factorial3/nulos_r2.py`, `c4f1c4d3…`) en A 0,3, ruido 0,15, τ 0, prueba 2.
  - Agregador `agregar_factorial3.py` (`2ec8cd03…`): margen 0,01, IC al 90 % (TOST); Holm sobre los dos nulos.
  - Hipótesis: H_SUPERA_R2 (gana por más de un punto) y H_CABLEADO_R2 (le gana a sus barajados).
  - Controles nuevos: REPRODUCE_F2 (las 90 corridas comunes con el factorial 2), REAL_IGUAL (el script de nulos reproduce la grilla) y SL_IGUAL_MODULO (el barajado numpy da lo mismo que `base.barajar_sl`).
  - Humo en brain-env: 3/3 VÁLIDO; REAL_IGUAL y SL_IGUAL_MODULO True. 81 trabajos; se estima unas 4 h en Actions.
- **Factorial 3 disparado (2026-10-13-009).** CORRER `cff2fce` en la rama titan, run 38420175126 de Actions, 81 trabajos (ancla success en 1 min); se estima unas 4 h. El bot commitea logs, json y `agregado.log` en `results/factorial3_2026-10-13/`.
- **Factorial 3 leído (2026-10-13-010): VÁLIDO, 81 de 81 trabajos.** Resultados del bot en `09ffbc1` (rama titan), MD5SUMS 163/163 OK.
  - Controles: ancla exacta, plan 600/600 y 50 + 50, TAU_DN_IGUAL, REPRODUCE_F2 exacto en las 90 corridas comunes con el factorial 2, REAL_IGUAL (0,9465).
  - Primaria: R2 0,9353 contra la regla con sus mismos sensores 0,9268; dif +0,85 puntos, IC90 [+0,08; +1,51]: NO_INFERIOR. H_SUPERA_R2 SIN_DECIDIR. Gana en 482 de 600 corridas. El +1,28 del factorial 2 (3 × 5) bajó a +0,85.
  - Nulos (A 0,3, ruido 0,15, τ 0, prueba 2): real 0,9465; SL media 0,666 (máx 0,796); T media 0,760 (máx 0,839); ninguno de los 100 iguala al real; p 0,0196 cada uno (el mínimo posible con 50), Holm 0,039: H_CABLEADO_R2 SOSTENIDA.
  - Lectura: el cableado real de R2 pesa mucho (19 a 28 puntos sobre el promedio de sus barajados, 11 a 15 sobre el mejor; el «15 a 28» de la 010 mezclaba las dos cosas, corregido en la 011) y alcanza a la regla con sus mismos sensores, con una ventaja chica (menos de un punto) que no pasa el margen.
- **Síntesis en criollo (2026-10-13-011), reemplaza a la 003.**
  - El cableado real pesa en las tres escalas: M46, R1 y R2 les ganan a sus barajados.
  - Contra el diseño de la mosca con los mismos sensores, M46 y R1 quedan abajo (−0,6 a −1,8 puntos) y sólo R2 (33.489 neuronas) lo alcanza (+0,85, sin pasar el margen). La 003 decía que alcanzaba con 1.504: lo corrigió la 007.
  - Para un robot conviene el plano (la regla tipo de sensor → comando), no el cableado completo: rinde casi lo mismo y es mucho más barato.
  - Posición frente a la literatura: Shiu et al. (Nature 2024, el mismo archivo de conectividad) y Lappalainen et al. (Nature 2024) predicen actividad y la validan; acá la pregunta es otra (el cableado contra su propio diseño) y no hay nada medido fuera de simulación.
  - Lo más cerca de cerrar es la v2 del Paper 1; las tres escalas son material para el Paper 2.
- **Informe detallado (2026-10-13-013):** logros, contraste con Shiu, Lappalainen, Costi, Suárez, Lechner, Vaxenburg y NeuroMechFly (doi en la respuesta), relevancia y escala.
  - Relevante en un nicho y por el método; para publicar: preprint de métodos (opinión, no medición).
  - Escala: el cerebro entero (138.639 neuronas, 15.091.983 conexiones) costaría unas 3,7 veces R2 si el costo sigue a las conexiones (estimación; el costo absoluto quedó medido en la 2026-10-13-015: 0,026 s por ensayo en una T4 de Kaggle y 3,2 s en brain-env); BANC trae `fafb_783_match_id` y es el segundo conectoma natural (NO MEDIDO).
  - La novedad («nadie comparó el cableado contra el plano del animal con los mismos sensores») es de búsqueda acotada: NO MEDIDO hasta una revisión sistemática.
- **Factorial 4 sellado en Kaggle (2026-10-13-015), disparado (2026-10-13-016) y leído (2026-10-14-001): VÁLIDO, el cerebro entero da lo mismo que R2:** el banco con el cerebro entero de FlyWire v783 (138.639 neuronas, 15.091.983 aristas, 6.032.681 inhibitorias, las mismas 564 entradas de R2). Rama `titan/factorial4-cerebro-entero-2026-10-13`: instrumento `ace8fe7` (`cerebro_mosca.py` `36a9f005…`, motor torch float64) y sello `431b7bd` (`tools/factorial4/SELLO-FACTORIAL4.md`).
  - Humo medido, todo VÁLIDO, en brain-env (CPU) y en tres sesiones T4 de Kaggle: paridad torch contra numpy de 4e-16 o menos en R1 y en el cerebro entero, y **REPRO_R2: la T4 reproduce exacto el 0,9465 de R2 del factorial 3**, en cada una de las dos GPU. 0,026 s por ensayo por T4, igual con dos procesos a la vez; 3,1 GB de GPU.
  - Plan: las 600 corridas del factorial 3 + 50 SL + 50 T; 2 kernels T4 x2 de `abrahammendieta`, 4 carriles, 22 trabajos; unas 3,6 h de reloj y 7 h de cuota de GPU (cuánta queda: NO MEDIDO).
  - Hipótesis pre-registradas: H_SUPERA_CE (contra su regla, margen 1 punto), H_ESCALA (CE contra R2 en los mismos ensayos) y H_CABLEADO_CE (50 SL y 50 T, Holm). Agregador probado 5/5 en clon fresco del sello.
  - **Leído (2026-10-14-001): VÁLIDO.** Los dos kernels terminaron con rc 0 (a 11.755 s, b 13.519 s: unas 7,0 h de sesión T4) y los 22 trabajos también; todos los chequeos del agregador sellado dan True (recibos, integridad 22/22, plan 600, REPRO_R2 0,9465 en los 4 carriles, REAL_IGUAL, 50 + 50 nulos, reproduce la primaria del factorial 3, misma regla y mismas DN que el 3).
  - **H_ESCALA REFUTADA: el cerebro entero da lo mismo que R2.** CE menos R2 +0,01 puntos, IC90 [−0,01; +0,04], EQUIVALENTE en las 6 celdas; la misma predicción en 1.198.955 de 1.200.000 ensayos (99,913 %). En esta tarea, las 105.150 neuronas que están fuera de R2 (33.489) no mueven la lectura de las descendentes.
  - **H_SUPERA_CE SIN_DECIDIR:** 0,9355 contra su regla 0,9268, +0,86 puntos, IC90 [+0,11; +1,51], NO_INFERIOR, y NO_INFERIOR en las 6 celdas: el mismo empate técnico de R2 en el factorial 3.
  - **H_CABLEADO_CE SOSTENIDA:** 0,9465 contra 50 SL (media 0,6488, máx 0,7935) y 50 T (media 0,7596, máx 0,8395); ninguno igual o mejor; p 0,0196 cada uno, Holm 0,0392.
  - **Post-hoc, no sellado: lo que decide si la red le gana a su regla es la semilla de tau, no el tamaño.** En 8 de 10 semillas CE le gana en 58 a 60 de las 60 corridas (+1,28 a +1,71 puntos); en la 5 no le gana en ninguna (−2,30) y en la 7 en 6 de 60 (−0,85); R2 hace lo mismo semilla por semilla. Candidata **H_TAU**, sin sellar: con las constantes de tiempo elegidas o aprendidas solo con el entrenamiento, ganarle a la regla por más de 1 punto en la prueba. R2 alcanza y corre en CPU: va a Actions sin gastar GPU.
  - En git quedó compacto, en la rama del factorial 4 (`87be763`): `results/factorial4_2026-10-13/` (`agregado.log` `539733b9`, `corridas.csv` `b58be308`, `nulos.csv` `94811363`, `MD5SUMS.txt` `7f396757` con las 50 salidas de Kaggle, `relectura_desde_csv.log` `a778e608`) y `tools/factorial4/releer_factorial4_desde_csv.py` (`045caf9e`), que rehace desde git la primaria, la escala y los nulos con el bootstrap sellado: 18 de 18 líneas iguales al agregado, y con una sola corrida tocada da 4 distintas y sale con 1. Los json por ensayo (unos 1,6 MB) y los dos recibos quedan por md5: sin un token para este repo no hay vía directa a git desde brain-env.
- **BANC bajado y medido; núcleo aparte; H_TAU y núcleo sellados (2026-10-14-002), rama `titan/htau-nucleo-banc-2026-10-14`:**
  - BANC v888 en brain-env (`/workspace/banc_888/`): meta md5 `8c2b93a6`, aristas v3 md5 `08542b07`, iguales al bucket público. Las aristas usan `root_888`, no `root_id`.
  - Las 6 DN tienen pareja del mismo tipo en BANC; entradas con pareja 291/564 (51,6 %) por `fafb_match`, 363 (64,4 %) por alguna vía.
  - De las aristas de R2 evaluables (782.453), el 39,8 % está en BANC: 28,9 % con 1 a 4 sinapsis, 60,0 % con 5 a 9, 77,2 % con 10 a 19 y 92,4 % con 20 o más. Núcleo de Schlegel 77,0 % contra 32,7 % del resto. Sin nulo de parejas al azar (NO MEDIDO).
  - Núcleo de Schlegel de R2 como pieza suelta: 603.219 aristas (14,96 %) con el 56,97 % de las sinapsis, 6/6 DN, 563/564 entradas; huella `69255109`.
  - H_TAU sellado (`tools/htau/SELLO-HTAU.md`): candidatas tau 10 a 19, elección por validación cruzada en el entrenamiento, pruebas nuevas 12 a 21, margen 0,01. 6 trabajos de Actions, unas 2,5 h. Se dispara con `results/htau_2026-10-14/CORRER`.
  - Núcleo sellado (`tools/nucleo/SELLO-NUCLEO.md`): H_CONSENSO (no perder más de 1 punto contra R2 y ganarle a 50 SL + 50 T). 80 trabajos de Actions, cerca de 1,5 h. Se dispara con `results/nucleo_2026-10-14/CORRER`.
- **v2 en main y los dos sellos corriendo (2026-10-14-004, ClickKit `merge_y_correr_004`, 11:28):**
  - PR #27 mergeado en main (`6785316`); la prueba de mezcla contra `7eec778` dio limpia. `tools/zenodo/depositar_v2.py --verificar` sobre main da PASS (PDF v2.0 `6e849bf2`, erratum v1.0 `05052e6e`).
  - `results/htau_2026-10-14/CORRER` y `results/nucleo_2026-10-14/CORRER` pusheados en `9545af4` (rama `titan/htau-nucleo-banc-2026-10-14`, nada sellado cambio). `htau-mosca` y `nucleo-mosca` arrancaron 14:30 UTC; estimado: nucleo hacia las 13:30 y H_TAU hacia las 14:30 de Buenos Aires (NO MEDIDO).
  - El deposito en Zenodo sigue esperando el token (borrador primero; publicar solo con el si de Abraham).
- **Esqueleto del Paper 2 (2026-10-14-005, ClickKit `esqueleto_paper2_004`):** `docs/paper2/paper2-esqueleto.md` en `titan/paper2-esqueleto-2026-10-14` (`753d4d5`), sin PR.
  - Una sola pregunta: si el cableado exacto carga el reflejo mas alla de su diseno y sus barajados, y si esa parte se conserva en BANC. Resultados 3.1 a 3.5 con numeros medidos (cotejo 73 de 74 en su fuente, el restante en el log de BANC); 3.6 H_CONSENSO y 3.7 H_TAU como huecos; 3.8 el negativo de lineas etiquetadas.
  - Bloquean un borrador: nulo del emparejado BANC, revision de literatura del hueco funcional, ecuacion exacta y figuras. Recomendacion: el control de salidas, LC6 a GF y sel_post van a un Paper 3, no a este.
- **Alcance del Paper 2 decidido (2026-10-14-006, Abraham, ClickKit `alcance_p3_005`, 12:19):** el control de las salidas (2026-10-10-005 a 009), LC6 a GF y sel_post van a un Paper 3 estructural. El Paper 2 queda con una sola pregunta. Anotado en el esqueleto (`4652c81`).
- **Topo v0, lenguaje topologico ejecutable (2026-10-14-011):** rama `titan/topo-lenguaje-2026-10-14` (`b34924d`), `tools/topo/` y `docs/topo/TOPO-v0.md`. Un reflejo se escribe como tipo x lado x signo -> comando, con dos backends: regla y cableado.
  - El escape en 18 renglones (`escape.topo`). Desde un clon limpio: EQUIV_REGLA PASA (12 de 12 casos exactos contra la regla sellada de los factoriales), CONTROL_NEGATIVO PASA (127 de 400 decisiones distintas con el aterrizaje mal escrito; 3 programas invalidos rechazados), REPRODUCE_M46 PASA (46 neuronas, 187 aristas, 1.149 sinapsis, igual a la 015). Registro md5 `f1008c67`.
  - Faltan, sin medir: H_TOPO_NUEVO (un reflejo nuevo escrito solo en Topo que pague en el banco), H_TOPO_C99 y H_TOPO_ESCALA. Antes, en la 2026-10-14-010, se evaluaron tres ideas: el lenguaje topologico es la mas fuerte, cerebelo de borde todavia no y protesis solo para avisar.
- **H_TOPO_NUEVO sellado con la barra segun su direccion (2026-10-14-012):** rama `titan/topo-barra-dir-2026-10-14`, orden verificable A tarea (`42d2f60`), B programa (`2deb335`), C banco (`8c7cf1b`), sello `afc2585` (`tools/topo_barra/SELLO-BARRA-DIR.md`).
  - La barra de adelante hacia atras ya estaba en la 015 (no era nueva); lo nuevo es la de atras hacia adelante en vuelo -> girar (fuente indirecta: Ache 2019 Supp Fig 5d, Kim 2023). Programa nuevo: aterrizar = LPLC4 - LPLC1.
  - Humo en brain-env VALIDO (numeros sin valor, vistos y declarados); humo en Actions disparado. La corrida completa espera `results/topo_barra_2026-10-14/CORRER`.
- **El nucleo volvio (bot `a522bc4`, agregado sellado):** VEREDICTO_GLOBAL VALIDO. H_CONSENSO REFUTADA: el nucleo pierde 4,59 puntos contra R2 (0,8894 contra 0,9353, IC90 [-5,07; -4,10]), pierde en las 600 corridas y en las 6 celdas. H_CABLEADO_NUCLEO SOSTENIDA: 0,9135 contra 50 SL (max 0,757) y 50 T (max 0,768), Holm 0,0392. Lectura completa pendiente.
- **H_TOPO_NUEVO corriendo (2026-10-14-014, ClickKit `correr_barra_013`, 13:29):** el humo 1 en Actions fallo antes de medir por falta de torch (lo importa el modulo sellado de la 003); arreglo declarado en los workflows (`6e02d34`), instrumento sin cambios. Humo 2 en Actions (`8e89e16`) igual a brain-env en 15 de 15 lineas. `CORRER` en `e416865`; run 38598860081 desde las 13:31.
- **Lectura del nucleo y dos veredictos nuevos (2026-10-14-015):**
  - Nucleo: pierde contra R2 en las 10 semillas de tau (-3,06 a -5,81 puntos) y mas con ruido 0,45 que con 0,15 en las 3 amplitudes (media -5,59 contra -3,59; post hoc). Con el 14,96 % de las aristas conserva cerca del 88 % de la ventaja de R2 sobre sus barajados SL (post hoc, cruza el factorial 3). Falta H_DEBILES: si las aristas debiles pesan por especificas o por cantidad.
  - H_TAU SOSTENIDA (bot `2d4dbfb`): con tau elegida por validacion cruzada (semilla 10 en las 6 celdas), R2 le gana a su regla por +1,78 puntos, IC90 [+1,45; +2,13], SUPERA en las 6 celdas y en 60 de 60 corridas. Primera vez que el cableado supera al diseno por el margen. Letra chica: el cableado tuvo 10 sorteos de tau para elegir y la regla ninguna perilla (H_TAU_JUSTO, sin sellar).
  - H_TOPO_NUEVO SOSTENIDA (bot `46929db`): el cableado le gana a 300 SL y 300 T en las 6 celdas (Holm 0,0399) y la regla nueva no pierde contra el cableado (+1,68 puntos, IC90 [+0,99; +2,38]). Letra chica (descriptivo): la regla vieja le gana a la nueva en 5 de 6 celdas; la nueva arregla la barra AD pero rompe el aterrizaje ante la barra AA.
- **H_DEBILES sellado, sin correr (2026-10-14-016):** rama `titan/debiles-2026-10-14`. La mezcla es R2 con el nucleo intacto y las 3.428.678 aristas debiles con destinos barajados por lado (mismos grados, pesos y signos). E1 = mezcla menos R2 decide H_DEBILES_ESPECIFICAS (importa cuales son) y E2 = mezcla menos nucleo decide H_DEBILES_SUMAN (importa cuantas son), pareadas corrida por corrida con el factorial 3 y con el nucleo, M 0,01. Instrumento `f28404c2`, agregador `c60fbbc6`, prueba del agregador 7 de 7. Los reales a tamano completo dieron exacto en Actions (bot `ca8221a`, 2026-10-14-017): R2 0,9465 y nucleo 0,9135, REAL_R2_IGUAL y REAL_NUCLEO_IGUAL True; la condicion del CORRER esta cumplida. Corre solo con `results/debiles_2026-10-14/CORRER`.
- **Sintesis en criollo (2026-10-14-018), reemplaza a la 2026-10-13-011:** tenemos un banco sellado que compara el cableado real contra sus barajados y contra el plano de la mosca con los mismos sensores. El cableado les gana a sus barajados en las cuatro escalas (M46, R1, R2 y cerebro entero); contra el plano empata (R2 +0,85, cerebro entero igual a R2) y lo supera solo con tau elegida por validacion cruzada (+1,78; falta H_TAU_JUSTO). El nucleo carga la mayor parte de la ventaja sobre los barajados (88 %, post hoc) pero solo pierde 4,59 puntos: falta H_DEBILES. Potencial: un resultado de nicho publicable por el metodo, Topo para escribir planos de reflejos baratos y el portero de choque como primera demo fuera de simulacion. Nada medido fuera de simulacion.
- **Paper 3 con esqueleto y estado de Topo (2026-10-14-019):** esqueleto en `titan/paper3-esqueleto-2026-10-14` (`5b2e5ee`, `docs/paper3/paper3-esqueleto.md`, sin PR). Una sola pregunta: que clases alimentan cada salida (descendentes, motoras, neurosecretoras) mas alla del tamano, la ubicacion y la cantidad de pruebas. Los 106 numeros estan en sus fuentes de git (`tools/paper3/cotejar_paper3.py` PASA; control negativo PASA). Lo que aguanta todo: descendentes a descendentes, a motoras, a cuello y a antena, y el optico casi no llega a las descendentes; el escape visual es el caso (la vista no tiene atajo a las motoras). Pendientes: PR #26 sin review, la discrepancia del nulo de LC6 a GF (5,8 contra 17,2 esperadas), la replica en BANC. Topo: v0 y H_TOPO_NUEVO hechos; falta el grafo chequeado contra el conectoma (paso 2 de la 2026-10-14-013) y la v2 del programa de la barra.
- **Topo v0.1 y H_DEBILES corriendo (2026-10-14-020, ClickKit `topo_y_debiles_019`, 17:53):** H_DEBILES disparado (`CORRER` en `84e225c`, run 38635900391, 64 trabajos, unas 3 h); los reales completos dieron exacto tambien en brain-env (0,9465 y 0,9135). Topo v0.1 en `titan/topo-grafo-2026-10-14` (`3d7010a`): `tools/topo/topo_grafo.py` dibuja cada programa como grafo (Mermaid) y chequea cada flecha contra FlyWire (CABLEADA, SIGNO_CONTRARIO, SIN_VIA_DIRECTA); pruebas 5 de 5, reproduce exacto los totales de la 2026-10-12-014. Descriptivo: en el escape las 10 flechas que suman estan cableadas y las 4 restas del giro no tienen via directa (a dos saltos, casi todo excitatorio); en el aterrizaje por direccion, la unica flecha nueva (restar LPLC1 en DNp07) no tiene via directa.
- **H_TOPO_FIEL sellado, sin correr (2026-10-14-021, ClickKit `sellar_topo_fiel_020`, 18:20):** rama `titan/topo-fiel-2026-10-14` (A `27fe098` programas, B `b3548c8` banco, sello `79b8c59`, `tools/topo_fiel/SELLO-TOPO-FIEL.md`). El programa fiel (`escape_fiel.topo`) es `escape.topo` sin la resta contralateral en el giro de DNp06; Topo v0.1 da CABLEADA=10. Se compara contra el que resta en la tarea de la 012 con semillas nuevas (12.000 ensayos, margen 0,01, IC90): SOSTENIDA si el fiel no pierde mas de un punto. Control cruzado (gira hacia el estimulo) tiene que salir REFUTADA; si no, INVALIDO. Prueba 8/8. Humo en brain-env (numeros sin valor, vistos y declarados): el fiel pierde unos 5 puntos, casi todo por el looming frontal en vuelo (sin la resta gira en vez de aterrizar), y gira igual o mejor; el control salio REFUTADA. La corrida completa no es ciega respecto del humo (mismas semillas, menor tamano). Humo en Actions en cola.
- **H_TOPO_FIEL REFUTADA en brain-env (2026-10-14-022, ClickKit `correr_topo_fiel_021`, 18:38):** `CORRER` en `0f83872`; Actions en cola detras de H_DEBILES, asi que el mismo instrumento sellado corrio completo en brain-env (81 s, log md5 5db97477). Todas las guardas en verde. El fiel pierde 5,41 puntos contra el que resta (IC90 [-5,92; -4,90]); el control cruzado REFUTADA (-27,97). Por subconjunto (descriptivo): ante el looming frontal en vuelo el fiel pierde 85 a 88 puntos (aterriza 6,5 a 7,1 por ciento contra 92 a 94), en el giro gana hasta 22 puntos con ruido alto. Lectura: la resta del programa cancela el looming frontal en el giro; en la mosca eso no pasa por via directa, asi que lo hace otro circuito (NO MEDIDO). Falta la confirmacion en Actions x64.
- **H_FRENO sellado, sin correr (2026-10-14-023, ClickKit `sellar_frena_giro_022`, 19:57):** rama `titan/frena-giro-2026-10-14` (instrumento `d59913c`, sello `2bad970`, `tools/frena_giro/SELLO-FRENO.md`). Pregunta: que frena el giro de DNp06 ante el looming frontal, si la resta no tiene via directa. Siete mecanismos pre-registrados antes de mirar DNp06: directos (DNp07, DNp01, la DNp06 opuesta) y a dos saltos por interneurona inhibitoria (LPLC1 y LPLC2 del otro lado, LPLC4, DNp07, detector bilateral). Cuota de la entrada inhibitoria y percentil contra las 927 unidades descendentes; control positivo con LPLC1 y LPLC2 del mismo lado. Prueba 6/6 (dio rojo una vez y se corrigio antes de datos reales). Humo con DNp01, DNp06 ciega. La corrida con DNp06 espera su `CORRER` (segundos).
- **H_FRENO REFUTADA en brain-env (2026-10-14-024, ClickKit `correr_freno_023`, 20:10):** `CORRER` en `d74eaf3`; el mismo instrumento sellado corrio en brain-env (19 s, log md5 c474e1f3, rama `d2240a6`). Control positivo PASA (percentil 0,981 y 0,982). Los 7 mecanismos dan DESCARTADO o AUSENTE: ni DNp07, ni DNp01, ni la DNp06 opuesta inhiben directo a DNp06; por interneurona, lo del otro lado aporta 0,4 a 0,9 por ciento de su inhibicion y el detector bilateral menos de 0,1. Post hoc (descriptivo): las dos primeras inhibitorias de DNp06 son LHAD1g1 (GABA, una por lado, 11 a 13 por ciento, alimentada por LPLC2 y LC4 del MISMO lado) y PVLP010 (glutamato, alimentada por LC4 del mismo lado): inhibicion de avance ipsilateral, que no distingue frente de costado. Lectura: a dos saltos en el cerebro no hay freno cableado del giro ante el looming frontal; queda en el cordon nervioso, en la dinamica o en que el looming frontal no excite a DNp06 en la mosca (supuesto del modelo de entrada, NO MEDIDO).
- **DNp06 responde a los dos ojos; el frente no esta medido (2026-10-14-025, ClickKit `frontal_dnp06_024`, 20:17, literatura):** Jang et al. 2023, J Exp Biol 226: jeb244790: con looming a +-45 grados, GF, DNp02 y DNp06 responden a los dos ojos aunque sus dendritas son de un solo lado; DNp06 con grandes despolarizaciones y espigas (un solo ensayo mostrado). La via contralateral es unidentified segun los autores. Kim et al. 2023, Curr Biol 33: 321: DNp06 responde a puntos que se mueven en el campo contralateral. El looming frontal sobre DNp06 no esta medido en lo leido. Lectura: la tercera salida de la 024 (el frente no enciende a DNp06) queda floja; la entrada contralateral de DNp06 en la mosca es EXCITATORIA, al reves que la resta del programa, y no aparece a dos saltos con sinapsis quimicas (FlyWire no tiene las electricas). Entonces el lado del giro se decide aguas abajo, comparando las dos DNp06 (u otras descendentes) en el cordon nervioso: la resta del programa seria esa comparacion, no una cuenta dentro de DNp06. NO MEDIDO.
- **Topo v0.2, salida diferencial (2026-10-14-026, ClickKit `topo_v02_diferencial_025`, 20:22):** rama `titan/topo-v02-2026-10-14` (`a817ad3`, `docs/topo/TOPO-v0.2-diferencial.md`). `topo_v02.py` envuelve topo.py y topo_grafo.py sin cambiarlos y agrega `linea ... -> interna` y `compara NOMBRE = A - B ... -> ACCION`. `escape_dif.topo`: las DNp06 leen su lado y el giro sale de comparar izquierda contra derecha; chequeo FlyWire CABLEADA=10 AGUAS_ABAJO=4 (el que resta daba SIN_VIA_DIRECTA=4). Pruebas 9/9, reproducidas desde un clon limpio: por linealidad escape_dif da exactamente lo mismo que escape.topo (800 de 800, umbrales bit a bit), asi que no se sella una prueba de banco (no podria dar rojo). El falsador queda en el cordon nervioso: H_COMPARADOR en BANC (salidas de DNp06 izquierda y derecha con signo opuesto sobre motoneuronas de vuelo de un lado), sin sellar.
- **Confirmado en Actions y sintesis en criollo (2026-10-14-027, 20:56):** H_TOPO_FIEL REFUTADA en Actions x64 igual que en brain-env (run 38641915842; 38 de 38 lineas iguales salvo maquina y tiempos). H_FRENO REFUTADA en Actions igual (run 38652439698; mecanismos, control y veredicto identicos); unica diferencia, descriptiva: dos tipos empatados en 98 sinapsis salen en otro orden en el top 10 (el orden de los empates no es estable). Cruce con la 2026-10-12-011: LHAD1g1 izquierda recibe 5,16 por ciento de su entrada desde LC4 y LPLC2, como el 5,2 de entonces. Sintesis: el cerebro de la mosca no decide de que lado girar ante un looming; manda las dos DNp06 encendidas (responden a los dos ojos) y la resta que el programa necesita no esta en el cerebro a dos saltos; Topo v0.2 la pone aguas abajo y el falsador es H_COMPARADOR en BANC. Para la demo camara a vibracion (2026-10-13-020): la pieza de mosca da peligro por lado y el lado lo decide una resta despues, que en el microcontrolador es una cuenta.
- **Idea de Abraham: la misma plantilla en distintas acciones, comparando conectomas (2026-10-14-028, 21:14):** comparar BANC con los otros conectomas para separar lo que es de la mosca de lo que es de un individuo, y buscar circuitos que se repiten para acciones distintas. Primer indicio medido (descriptivo, de los logs de la 023 y la 024): LHAD1g1 (GABA) y PVLP010 (glutamato) estan entre las inhibitorias mayores de DNp01 (despegue; 10,9 y 10,5 por ciento de su inhibicion) y de DNp06 (giro; 20,1 y 18,7): el mismo modulo de inhibicion de avance sirve a dos comandos. BANC 888 trae pareja de tipo con FlyWire para 64.789 neuronas, con MANC para 24.277 y con hemibrain para 6.768; MANC y hemibrain no estan bajados. Propuesta H_REUSO, sin sellar: una plantilla escrita antes de mirar (sensor a descendente del mismo lado, mas el mismo sensor a una inhibitoria que vuelve a esa descendente) aparece en mas pares sensor-descendente que en los nulos SL, en FlyWire y otra vez en BANC; falsador, no supera al nulo o no se replica. Topo v0.3 tendria plantillas: si el repertorio se escribe con pocas plantillas, la compresion es la medida del reuso.
- **H_REUSO sellado, sin correr (2026-10-14-029, ClickKit `sellar_reuso_028`, 21:20):** rama `titan/reuso-2026-10-14` (A `613317d`, sello `5ef2a63`, `tools/reuso/SELLO-REUSO.md`). Plantilla de inhibicion de avance: sensor visual a descendente del mismo lado con 20 sinapsis o mas, y una inhibitoria con 5 o mas desde ese sensor y 5 o mas sobre esa descendente. T1, fraccion de pares con la plantilla; T2, inhibitorias que la hacen para dos o mas tipos de descendente. 200 nulos SL por conectoma (destinos barajados por bloque de lados), Holm sobre 4 pruebas; SOSTENIDA si pasa en FlyWire y otra vez en BANC. Prueba 7/7 (dio rojo una vez por un error de la prueba, corregido antes de datos reales). Humo CIEGO en brain-env: controles y guardas PASAN (FlyWire 996 pares, BANC 753), sin ver T1 ni T2; de paso, LHAD1g1 tambien esta entre las X de LPLC2 a DNp06 en BANC. La corrida completa espera su `CORRER` (unos 40 minutos).
- **H_REUSO SOSTENIDA en FlyWire y otra vez en BANC (2026-10-14-030, ClickKit `correr_reuso_029`, 22:09):** CORRER `6bec7cf`; Actions, bot `f12c95a` (reuso.log 6e12152a); brain-env, `c74509a` (brain-env.log b008f8e9); 59 de 59 lineas iguales sin tiempos. FlyWire: T1 0,8835 contra nulo media 0,6823 (max 0,7462); T2, 698 inhibitorias que sirven a dos o mas tipos de descendente, contra 128,6 (max 154). BANC: T1 0,8260 contra 0,3472 (max 0,4744); T2 419 contra 11,0 (max 23). p 0,005 en las cuatro (el piso con 200 nulos), Holm 0,0199. Descriptivo: 203 tipos de X compartidos aparecen en los dos conectomas. Limite: el nulo SL baraja destinos entre todas las neuronas y no conserva cuanto le manda cada X a las descendentes como clase; el nulo que conserva la clase del destino es NO MEDIDO y es el falsador siguiente (H_REUSO_ESTRICTO). **H_DEBILES dio INVALIDO por infraestructura:** Actions perdio 2 de 60 celdas (t3c3, el runner perdio comunicacion; t8c0, el artefacto no subio) y el agregador freno la lectura como debia (bot `3bc5432`, agregado.log 634e762a); falta relanzar esas 2 celdas, y sus descriptivos no se citan.
- **Regla nueva: los descriptivos de una corrida INVALIDA no se citan como resultado (2026-10-14-031, aprobada por Abraham el 15-oct a las 00:17):** ni en papers, ni en Docs, ni en el chat; si hace falta nombrarlos, van con la palabra INVALIDA al lado. La auditoria externa de Fable 5.1 sobre el expediente de las 23:06 y su revision punto por punto contra el repo estan en la 2026-10-14-031 (commit de documentos `fb033b2`); lo que cambia de wording y el plan de cinco sellos estan ahi.
- **H_RIVAL y H_TAU_JUSTO sellados, sin script (2026-10-14-032, 15-oct 00:37):** rama `titan/rival-2026-10-15`, sello `05a574c` (solo `tools/rival/SELLO-RIVAL.md`, md5 ff79011b), anterior a cualquier script como pidio Abraham. Pregunta: si W, la red con tau elegida de H_TAU, le gana por mas de 1 punto a tres rivales entrenados con el mismo presupuesto (10 candidatas, 5 pliegues modulo 5, como tau) y las mismas 564 entradas. Rivales: RIDGE (10 lambdas, forma dual), el MLP de la 005 (semillas 0 a 9) y REGLA_TAU (la regla con integrador por canal, semillas 10 a 19; si W no le gana por el margen, H_TAU_JUSTO sale REFUTADA). Metrica: acierto por semilla de prueba (12 a 21); bootstrap de semillas, IC90 con Bonferroni por 3; margen 0,01. Control positivo: el ridge nuevo reproduce los 0,9935 de la 015 en las 6 celdas a 0,0010 o menos. Limitaciones declaradas: una red elegida por celda (el IC no cubre la variacion entre redes) y la secundaria del factorial 3 con 10 semillas de tau (con 30 seria mas fiable). El instrumento entra en un commit aparte; la corrida, solo con su `CORRER`.
- **Instrumento de H_RIVAL y humo ciego, sin aciertos de rivales (2026-10-14-033, ClickKit `instrumento_rival_034`, 01:28):** rama `titan/rival-2026-10-15`, instrumento `04d0635`, despues del sello `05a574c`: `rival_mosca.py` (md5 774232f5), `agregar_rival.py` (f66b2250), `prueba_rival.py` (b7b9d411) y los workflows `rival-humo` y `rival-mosca`. Ejecutado en brain-env antes de commitear. Prueba 18/18, con un rojo a proposito. Control positivo: el ridge nuevo reproduce exactos los seis valores de la 015 (0,9935, 0,9595, 0,9935, 0,9575, 0,9940 y 0,9590), con 0 predicciones distintas del ridge de ept. Humo en Actions (run 38684660391, bot `b964058`): las 6 celdas VALIDO, con REPRO_REGLA 20/20 y REPRO_W 110/110 por celda, CONTROL_MLP_005 480/480 y el negativo en 0,5000 contra un azar de 0,5000; brain-env da lo mismo en c0. Desvio declarado: `ept.mlp_mux` trae fijas las clases de la 005, asi que el MLP es su bucle linea por linea con las clases de `tm.CLASES`, controlado contra `ept.mlp_mux`. Ningun acierto de rival visto. La corrida completa espera el `CORRER` de Abraham: unos 10 minutos por celda en Actions; la replica en brain-env, unas 9 horas.
- **H_RIVAL REFUTADA en Actions y H_TAU_JUSTO SIN_DECIDIR (2026-10-14-034, aprobado por Abraham a las 07:36):** run 38721794594 desde el `CORRER` `000d486`, bot `576fc4c`, 9 minutos; `agregado.log` md5 38d473cc. CHEQUEO VALIDO: los controles de las 6 celdas en verde y CONTROL_RIDGE_015 6/6 exacto. Acierto medio en las pruebas 12 a 21: la mosca (W elegida) 0,9413 a 0,9467; RIDGE 0,9894 a 0,9988; MLP 0,9879 a 0,9957; REGLA_TAU 0,9308 a 0,9352; la regla propia 0,9234 a 0,9289. Primaria: contra RIDGE D = -0,0503 [-0,0516, -0,0488] y contra MLP D = -0,0479 [-0,0494, -0,0465], NO_SUPERA (pierde); contra REGLA_TAU D = +0,0119 [+0,0096, +0,0150], SIN_DECIDIR (el piso queda debajo del margen de 1 punto). Secundaria, descriptiva: contra REGLA_TAU +0,0032 [-0,0068, +0,0106]. Lectura: con lector entrenado sobre las mismas 564 entradas, un ridge le gana a la mosca por 5 puntos; darle a la regla la τ elegida baja la ventaja de la mosca de 1,78 a 1,19 puntos. La replica en brain-env se corto (el contenedor se detuvo a las 07:58) y se relanzo a las 08:18; si una etiqueta por rival difiere entre maquinas, pasa a SIN_DECIDIR (NO_SE_REPLICA).
- **Borrador de la v2 del Paper 1 en Zenodo, sin publicar (2026-10-14-034, pedido de Abraham a las 07:50):** `tools/zenodo/depositar_v2.py --borrador` desde un clon limpio de main (`fe4a088`), con `--verificar` PASS antes. Nueva version del concepto 10.5281/zenodo.19136947: borrador 23393412, DOI reservado 10.5281/zenodo.23393412; los dos PDF con el md5 que calculo Zenodo igual al sellado (6e849bf2 y 05052e6e); estado `unsubmitted` y el registro publico da 404. Recibo: `docs/v2/recibo-borrador-v2.0.json`. El token no quedo en disco, en git ni en los recibos (medido). El Paper 2 y el Paper 3 no se subieron: son esqueletos (`docs/paper2/paper2-esqueleto.md` y `docs/paper3/paper3-esqueleto.md`, en sus ramas), sin manuscrito, PDF ni metadatos.
- **La v2 del Paper 1 esta publicada (2026-10-14-035, ClickKit `v2_publicar_asi`, 09:41):** DOI 10.5281/zenodo.23393412, version 2.0 del concepto 10.5281/zenodo.19136947, publicada a las 09:42 con `depositar_v2.py --publicar` desde main (`06872d0`). Chequeo sin token: registro publico 200, los dos PDF con el md5 sellado (6e849bf2 y 05052e6e), ultima version del concepto. Va con el titulo que incluye la amplificacion temporal, como eligio Abraham. Recibo: `docs/v2/recibo-publicacion-v2.0.json`.
- **Auditoria del Paper 2 y el Paper 3 contra H_RIVAL (2026-10-14-035):** el Paper 2 no nombra el ridge entrenado que su propia fuente ya media (2026-10-12-015, 0,9475 a 0,9875, descriptivo), tiene viejos H_CONSENSO (REFUTADA) y H_TAU (SOSTENIDA, con H_TAU_JUSTO SIN_DECIDIR), y su titulo y su Discusion (fabrica de piezas, el modelo de sinapsis como culpable) no sobreviven a H_RIVAL. El Paper 3 es estructural: ningun numero cambia; solo hay que acotar en 3.5 y 4 que el embudo descendente no es el mejor lugar para leer la vision. Ninguno esta para Zenodo.
- **H_LECTOR sellado, sin script (2026-10-14-036, ClickKit `sellar_lector_mosca`, 09:52):** rama `titan/lector-2026-10-15`, sello `8e65e05` (`tools/lector/SELLO-LECTOR.md`, md5 6e587be6), solo el documento. Lector: el RIDGE de H_RIVAL sin cambios, sobre las trazas de las 6 descendentes de la red elegida de H_TAU (240 rasgos contra 22.560 del ridge crudo). H_LECTOR_CERCA: no pierde mas de 1 punto contra el ridge crudo. H_LECTOR_PAGA: supera por mas de 1 punto a las lineas sin entrenar. H_LECTOR_CABLEADO: con el mismo lector, el cableado real supera por mas de 1 punto a 40 SL y 40 T en c2 y c5 (prueba 12, interseccion-union). Expectativa declarada: CABLEADO probablemente REFUTADA (antecedente de la entrada por tipos). El encabezado del sello dice 10:00; el commit es de las 09:57 y manda el commit.
- **Instrumento y humo de H_LECTOR (2026-10-14-037, ClickKit `instrumento_lector_037` y `cerrar_037`):** rama `titan/lector-2026-10-15`, sello `8e65e05` sin editar. Instrumento: `tools/lector/lector_mosca.py` (5b7fb79e), `agregar_lector.py` (8b003a44), `prueba_lector.py` (d697ed32), workflows `lector-humo.yml`, `lector-mosca.yml` (22 trabajos, 612745d3) y `lector-prueba.yml`. Humo ciego en Actions (run 38752555880, bot `b1cb491`): las 6 celdas VALIDO con REPRO_W 10/10, REPRO_RIDGE 10/10 y CONTROL_NEGATIVO 0,5000 contra azar 0,5000; en c0 CONTROL_LECTOR_CRUDO 2000/2000 iguales al RIDGE de H_RIVAL (lambda 10); rutas de nulo SL (4.030.551 destinos cambiados) y T (423 tipos) VALIDO e iguales al factorial 3. La prueba cayo en ese run porque `prueba_lector.py` no estaba en el commit que disparo (error de orden de push, declarado) y se reintento sola: 13/13 OK en Actions (bot `c6b1a63`, log md5 a3b800b5, con los mismos md5 de los tres scripts). Ningun acierto de L se imprimio. Celdas de 50 a 60 min en Actions.
- **H_LECTOR medido en Actions (2026-10-14-038, ClickKit `correr_lector_038`, 13:50):** CORRER `2df0961`, bot `8d305e9` (`results/lector_2026-10-15/`, agregado.log md5 8f2f4392, MD5SUMS 68 de 68 OK). Todos los controles VALIDO. H_LECTOR_CERCA SOSTENIDA: D1 = WL - RIDGE = -0,0029 [-0,0038, -0,0020], con 240 rasgos contra 22.560. H_LECTOR_PAGA SOSTENIDA: D2 = WL - W = +0,0474 [+0,0454, +0,0493]. H_LECTOR_CABLEADO SOSTENIDA: el real le gana a los 40 nulos en las 4 combinaciones (p = 1/41 = 0,0244 en todas): SL c2 +0,0337, SL c5 +0,1194, T c2 +0,0450, T c5 +0,1111. Contra la expectativa declarada en el sello. Falta la replica de la primaria en brain-env (si difiere, NO_SE_REPLICA). Abierto para auditoria: la tau de semilla 10 se eligio en H_TAU sobre la red real y los nulos la heredan sin eleccion propia.
- **H_TAU_LIBRE sellado, sin script (2026-10-14-039, ClickKit `sellar_control_tau_039`, 18:41):** rama `titan/taulibre-2026-10-15` (desde `8d305e9`), sello `fec8472` (`tools/taulibre/SELLO-TAU-LIBRE.md`, md5 3886aa58), solo el documento. Controla la asimetria de la 038: la tau 10 la eligio H_TAU sobre la red real y los nulos la heredaron. Aca nadie elige: real y nulos con taus frescas 20 a 29, apareadas (nulo k con tau 20 + k mod 10), los mismos 40 nulos SL y T de H_LECTOR en c2 y c5, prueba 12, mismo lector L. SOSTENIDA si el real supera por mas de 1 punto en las 4 combinaciones (p apareado <= 0,05). Controles nuevos: REPRO_LECTOR, NULOS_IGUAL_LECTOR, TAU_FRESCA. Expectativa declarada: c5 probablemente sobrevive, c2 abierta.
- **Instrumento y humo de H_TAU_LIBRE (2026-10-14-040, ClickKit `instrumento_taulibre_040`, 18:47):** rama `titan/taulibre-2026-10-15`, sello `fec8472` sin editar. Instrumento en un solo commit con el disparo (`930f0d7`): `tools/taulibre/taulibre_mosca.py` (c65bebe2, importa `lector_mosca.py` sin cambios), `agregar_taulibre.py` (340dc41a), `prueba_taulibre.py` (9f74f63d), workflows `taulibre-humo.yml` y `taulibre-mosca.yml` (20 trabajos). Humo en Actions (run 38816081787, bot `c3e07cd`): todo VALIDO; REPRO_LECTOR reproduce el real de H_LECTOR caracter por caracter en c2 (0,9910, lambda 0,001) y c5 (0,9930, lambda 0,01); NULOS_IGUAL_LECTOR 40 de 40 grafos SL en c2 y 40 de 40 T en c5; TAU_FRESCA; CONTROL_NEGATIVO en el azar; prueba 11/11. Ningun acierto nuevo se imprimio.
- **H_TAU_LIBRE SOSTENIDA en Actions (2026-10-14-041, pedido de Abraham 19:38):** CORRER `291a2f2`, bot `e7ada46` (`results/taulibre_2026-10-15/`, agregado.log md5 64f17f1a, MD5SUMS 62 de 62 OK), 20 de 20 json VALIDO, REPRO_LECTOR exacto en c2 y c5. Con taus que nadie eligio (20 a 29) y cada nulo contra la red real de su misma tau, el real supera a los 40 nulos en las 4 combinaciones, ninguno lo iguala (p = 1/41): SL c2 +0,0362, SL c5 +0,1219, T c2 +0,0476, T c5 +0,1127. Descriptivo: con L la tau 10 no fue una ventaja, quedo por debajo de las 10 frescas en las dos celdas (c2 0,9910 contra 0,9930 a 0,9955; c5 0,9930 contra 0,9940 a 0,9955); el delta por tau mas chico es +0,0145 (SL c2, tau 26). La asimetria de la 038 queda descartada como explicacion. REPRO_LECTOR de c2 tambien exacto en brain-env (otra maquina).
- **H_RIVAL replicado en brain-env y replica de H_LECTOR lanzada (2026-10-14-042, pedido de Abraham 21:51):** la replica de H_RIVAL (6 celdas, de 4210 a 4365 s cada una, termino el 15-oct 15:56) coteja con Actions: H_RIVAL REFUTADA y H_TAU_JUSTO SIN_DECIDIR en las dos maquinas; RIDGE y REGLA_TAU con 120 de 120 aciertos iguales; MLP con 40 de 120 iguales y diferencia maxima 0,0045 (torch entre maquinas), misma etiqueta (agregado.log de brain-env md5 17168360). La replica de la primaria de H_LECTOR corre en brain-env desde el 15-oct 21:55 desde el clon de `8d305e9` (`lector_mosca.py` 5b7fb79e), dos celdas a la vez, en `/workspace/fable/rl041/out_brain`; al terminar, `agregar_lector.py --cotejar` contra el agregado de Actions (los nulos no se replican, limitacion del sello).
- **Paper 3 empujado (2026-10-14-043, pedido de Abraham 22:08):** la discrepancia del nulo de LC6 a GF eran dos nulos: el CP de la 060 (destinos barajados dentro de `super_class`) espera 5,8 y el que preserva neuropilo de la 065 (`src/escape_neuropil_null.py`, rama `titan/twohop-nulls`) espera 17,2 +- 3,1 (z -5,61, minima de 40 = 12); manda el segundo. A escala de neuropilo LC6 y la GF comparten PVLP (5.335 sitios, mas que LC4 con 104 aristas); la distancia entre arboles sigue NO MEDIDA. Los conteos ya estan publicados (Kind et al. 2024, eLife RP 99277, y el Cell Type Explorer de FAFB, respuestas 066 y 067): el aporte es la expectativa, no el conteo. Esqueleto en `titan/paper3-esqueleto-2026-10-14` (bot `7f8b331`, md5 a904026e), cotejo 127 de 127 y control 2 de 2, con copias verbatim de la 065, 066, 067 y 038. El vinculo con H_LECTOR en la Discusion queda pendiente del cotejo de la replica.
- **Espera decisión de Abraham:** revocar el token de Zenodo, que quedo escrito en el chat (2026-10-14-034); decidir el merge del PR #26 (codigo y logs de la 005 a la 009 del Paper 3) y si se sella la replica del mapa de salidas en BANC v888 en Actions (2026-10-14-043); si una v2.1 del Paper 1 reproduce Z_CP y la RDI o saca la amplificacion del titulo (la v2.0 ya esta publicada, 2026-10-14-035); la pregunta y el titulo del Paper 2 tras H_RIVAL y H_CONSENSO (2026-10-14-035); reescribir el Paper 2 alrededor de H_LECTOR y H_TAU_LIBRE; leer el cotejo de la replica de H_LECTOR en brain-env cuando termine (unas 12 h, sin medir), que es condicion para Zenodo (2026-10-14-042); relanzar las 2 celdas de H_DEBILES que perdio Actions (t3c3 y t8c0; el agregado dio INVALIDO, 2026-10-14-030); sellar H_COMPARADOR en BANC, el falsador de Topo v0.2 (2026-10-14-026; H_TOPO_FIEL y H_FRENO ya confirmadas en Actions, 2026-10-14-027); sellar H_REUSO_ESTRICTO, con el nulo que conserva la clase del destino (2026-10-14-030); una segunda versión del programa de la barra (2026-10-14-015; H_TAU_JUSTO dio SIN_DECIDIR, 2026-10-14-034); el nulo del emparejado BANC; responderle a Tao en su PR.

## Tarde y noche del 12-oct (010 a 018)

- **Paper 1 v2.0 (010 y 018):** la 010 retiró «lista para depositar» por tres inconsistencias internas del manuscrito del PR #27. **La 018 las corrigió** con `tools/v2/fix_v2_018.py`, aplicado en brain-env y en Actions con md5 iguales:
  - el «2.4-fold» era visual sobre gustatory; el cociente entre extremos es 4,2× sin umbral y baja de 3.862× a 40× con el umbral;
  - la amplificación temporal aparece con SparseLTC y Linear y no con LIF-soft (0,253 a 0,002); corregido también en el erratum, ítem 7, porque la v1.0 tenía el mismo error;
  - el cero de olfato y visión sin umbral es compatible con el nulo de neurópilo (1,0 ± 0,9 y 0,03 ± 0,16), no intesteable; sólo con el umbral el nulo es 0,0 exacto.
  - PDF nuevos en `/workspace/v2cierre_2026-10-12/deposito_018/`: manuscrito `d353cf0f…` (17 páginas) y erratum `05052e6e…` (15 páginas); render PASS y verificación PASS en clon fresco de `f19a9c7`.
  - **Falta:** la Tabla 8 (el resumen y el §4.1 usan +14,8σ como firme y no se reprodujo), el informe archivado de Tao (comunicó hallazgos a las 13:25 en su chat, 010), el merge y el token.
- **No es la neurona (011):** el motivo de 28 llevaba el 2,96% de la entrada de sus descendentes y nada de su inhibición; la DCMT como vino invierte el glutamato (17% del cerebro).
- **Líneas etiquetadas (012): NO PAGAN** con la tarea de la 005; lo que decidía era un supuesto de entrada (LPLC2 al punto).
- **Fisiología (013 y 014):** LPLC2 responde a objetos que pasan (Kim 2023) y la mosca esquiva en vuelo por DNp06, cuya mayor entrada es LPLC1 (1.023 sinapsis) y después LPLC2 (1.003); las barras de adelante hacia atrás piden aterrizaje (Ache 2019).
- **Tarea de la mosca (015 sellada, 016 corrida, 018 leída): PAGA LA TAREA DE LA MOSCA.** 46 neuronas, cinco acciones, líneas etiquetadas sin entrenar: W les gana a 300 SL y 300 T en 6/6 celdas (Holm 0,0399), instrumento VÁLIDO. Contra la regla a mano: PEOR en 4, EMPATE en 2, nunca MEJOR.
  - **La regla a mano es el mismo diseño de la mosca idealizado** (las etiquetas tipo → descendente de FlyWire sobre las entradas crudas): el diseño paga y nuestra simulación de sus sinapsis le resta.
  - Descriptivo: con LPLC4 muda W aguanta más que la regla (0,8030 contra 0,7680); con ruido 0,45 W gira mejor en 2 de 3 amplitudes.
  - Rama `titan/tarea-mosca-2026-10-12`: sello `57d094a`, log `bdf03c2` (md5 `ad8c94b4…`).
- **Qué le falta al modelo (018):** las 6 descendentes reciben 40.145 sinapsis; el motivo lleva 875 (2,18%) y 0 de las 14.576 inhibitorias (36,3%). R1 (con sus presinápticas de 5 sinapsis o más) tiene 1.504 neuronas; R2, 33.489. Rama `titan/que-falta-al-modelo-2026-10-12` (`3cf6332`).
- **Corrección a la 017:** «la mosca no reemplaza a la ingeniería» estaba mal planteado; lo que le ganó a nuestro modelo fue la mosca idealizada.
- **Máquinas (016 y 017):** para un script numpy sellado la máquina rápida es Actions (11,6×), no Kaggle con GPU; Kaggle sólo con un port a torch verificado contra numpy.
- **Esperaba decisión de Abraham (resuelto en la 019 y la 2026-10-13-002):** sellar el factorial de la 018 (recorte 46 / R1 / R2, neurona de tasa / LIF con signo / líquida plena, con y sin inhibición; misma tarea, mismos nulos, la regla idealizada como rival); la Tabla 8; el merge del PR #27 y el token de Zenodo.

## Mapa del repo (respuesta 2026-10-11-004)

- main tenía 182 archivos en `02da943` y hay 27 ramas además de main (la 006 corrigió los 180 archivos y las 28 ramas de la 004). La unión de todas las refs da 464 pares ruta-blob. La 007 sumó `titan/v2-cierre-2026-10-12`. Al 12-oct a las 11:56 hay 35 ramas además de main (medido en la 009).
- **El expediente de agosto vive en ramas sin mergear:** las respuestas 063 a 124, 47 evidencias y unos 44 scripts. Lo esencial está en `titan/twohop-nulls`, contenida en `titan/auditoria-hipotesis-2026-10-01`, contenida en `titan/materializacion-h4-guard-2026-10-02`. Incluye:
  - el null anatómico;
  - LC6→GF;
  - sel_post;
  - los 39 nulos en GPU y el test global;
  - la auditoría de Tao;
  - Betzel.
- **Otras ramas con contenido propio:**
  - `titan/auditoria-integra-2026-08-25`: disputa del DOI y scripts de nulos;
  - `titan/initial-release`: manifest, logs de nulos y `src/routing_hierarchy.mjs` (las 8 clases del null de grado);
  - `titan/paso-1-identidad-roi-2026-10-03`: H4 ROI.
- **Abiertos en GitHub:**
  - PR #1, #2, #3, #12, #25, #26 y **#27 (v2.0 del Paper 1)**;
  - issues #4, #5 y #13 a #15.
- **`docs/SECCION-V2-DOS-SALTOS.md` de main es la versión anterior al null anatómico** (323× contra el null de grado). La de la rama dice que el 323× era co-localización: el cociente entre extremos cae a 4,2× sin umbral (la v2.0 decía 2,4×, que era visual sobre gustatory: corregido en la 018) y queda la depleción gustativa (10 contra 101,6, z = −78,9). **El PR #27 la trae a main.**
- En el PDF, la Tabla 7 es la de reciprocidad por circuito y la de RDI es la Tabla 8. El `reproduce_table7` del release inicial es de la trayectoria de RDI y no la reproduce.

## Veredicto operativo

- **Paper 1, v2.0 (2026-10-12-007): lista para depositar en el PR #27.**
  - Render determinista PASS: manuscrito de 17 páginas, md5 `50df4ab9…`, y erratum de 14 páginas, md5 `28f7a21f…`.
  - El erratum cotejado contra el texto de la v1.0 tenía tres errores propios, ya corregidos:
    - el swap al revés (la v1.0 dice 100%);
    - la fila AN contada como cuarta enriquecida;
    - el 991× mezclado con un extremo de otras clases.
  - La v1.0 tiene cinco referencias con datos mal.
  - Falta el token de Zenodo y el merge. **Por pedido de Abraham (11:48), el depósito espera además la auditoría de Tao** (2026-10-12-009).
- **Paper, reciprocidad:**
  - La Tabla 7 es reproducible: 8/8 con el pin `17fc577` (respuesta 003). El script está reconstruido en el PR #26, sin merge.
  - El nulo CP propio reproduce el del erratum: media de 194.890,4 contra 194.974,2, o sea 20,60× con 0/100.
  - **Con ese nulo, la caída de la reciprocidad hacia la salida motora queda explicada por el nulo:** el exceso es 4,30× / 3,67× / 5,55× con ≥1 y 5,11× / 9,57× / 3,94× con ≥5, sin orden. Pero el instrumento dio FAIL (control negativo de la prueba secundaria, 8/20 con CP y ≥1) y **no se firma**. La v2.0 reporta el orden como descriptivo.
- **Quién controla las salidas (005 a 009):** el central pone el 60–73% de la entrada de las tres salidas; las descendentes, el 21–22% de la de las motoras; las ascendentes, el 16–20% de la de las neurosecretoras; el óptico, menos del 0,5%.
  - **Nulo fuerte (006**, etiquetas barajadas entre neuronas del mismo tamaño): se sostiene, con el central en ×1,5–2,3.
  - **Nulo de región (007**, además de la misma zona del cerebro): sólo las descendentes siguen mandando fuerte, → motoras ×3,69 / ×3,21 y → descendentes ×3,29 / ×2,61.
    - El dominio del central sobre descendentes y neurosecretoras era ubicación (×1,07 / ×1,01 y ×1,09 / ×1,03). Su plus propio va a las motoras (×1,31 / ×1,16), sobre todo a las de la boca.
    - Las ascendentes caen a azar en las tres salidas, lo sensorial queda por debajo de sus vecinas (×0,33 a ×0,62) y la proyección visual hacia las descendentes pasa a azar.
  - **Corrección múltiple de la 007 (008):** BY deja 31 de las 33 afirmaciones firmes y max-T deja 5: descendentes → descendentes, → motoras, → cuello y → antena, y óptico ▼ descendentes. El plus del central hacia las motoras aguanta FDR pero no FWER.
  - **Corrección múltiple de la 006 (009):** las 41 afirmaciones firmes aguantan BY, 34 aguantan Holm y 11 max-T. A la 006 le fallaba la ubicación, no la cantidad de tests.
  - **FWER con los dos nulos:** descendentes → descendentes, → motoras, → cuello y → antena, y óptico ▼ descendentes.
  - **Fuera de la v2.0** (recomendación de la 007, decide Abraham): va al Paper 2.
- **H4 fuerte: NO MEDIDA.** La búsqueda pública de ROI 2P está agotada (16/16 sin mapear, rama ROI). H4 débil queda refutada sólo en su alcance estrecho.

## v2.0 del Paper 1 (respuesta 2026-10-12-007)

- **Manuscrito:** `docs/v2/paper1-v2.0.md` en el PR #27.
  - Reconstruido en Markdown desde el texto del PDF v1.0 (185.471 B, md5 `c7cb36a2…`), porque no había fuente en Zenodo ni en el repo.
  - **Alcance:** v1.0 con el erratum aplicado, reciprocidad como rango (20,59× CP, 47,27× MS; 13,98% con ≥5, como Lin) y los dos saltos tras el null anatómico (§3.4, Tablas 5b y 5c), con prior art (Gordon & Scott 2009; Shiu et al. 2022).
  - Tabla 5 con p binomiales y la columna del null de grado; Tabla 7 con las dos columnas y 8,6; Tabla 10 con la constante efectiva.
  - «Motor» pasa a «motor output»: 1.299 descendentes, 110 motoras y 76 endocrinas.
- **Erratum revisado antes de depositar** (cotejado contra el PDF v1.0):
  - ítem 8: la v1.0 dice «rate 100%» y lo medido es 98,5% (`docs/METHODS.md`); el erratum lo tenía al revés;
  - ítem 2: 3 enriquecidas, 4 empobrecidas, 1 dentro y la AN aparte (antes contaba 4 con la AN);
  - el null de grado usó 8 clases: 7 reproducibles sin visual optic, más la AN completa de 2.231;
  - el 991× es sobre esas 8 y el rango sobre las 8 reproducibles es 713×;
  - calificación del null anatómico al ítem 2;
  - 8,6 como quinto problema de conteo;
  - Betzel verificado;
  - cinco referencias con datos mal: Gouwens & Wilson, Nagel & Wilson (que además no trata lo que se le atribuye), Tuthill & Wilson, Hasani y Schlegel;
  - pendiente 9 resuelto; pendientes 10 a 12 nuevos.
- **Render y verificación:**
  - `tools/v2/render_v2.py` (pandoc 3.10.2 + typst 0.15.0, fecha anulada): PASS, 19/19 cadenas y dos compilaciones iguales;
  - `tools/zenodo/depositar_v2.py --verificar`: PASS en clon fresco;
  - control negativo: 12 de 13 errores de la v1.0 ausentes en la v2.0 (el que aparece es una cita de la lista de cambios);
  - los PDF viven en `/workspace/v2cierre_2026-10-12/deposito/` de brain-env.
- **Depósito:**
  - `--borrador` crea la nueva versión sin publicar y `--publicar ID` es irreversible.
  - El token necesita `deposit:write` y `deposit:actions`; el inventario sólo nombraba el primero.
  - No hay token en brain-env (medido en la 007 y de nuevo en la 009: ni variable ni archivo).
  - **Token paso a paso (2026-10-12-009):** login en Zenodo con la cuenta dueña del registro; `https://zenodo.org/account/settings/applications/tokens/new/` (la ruta existe: 302 al login; una inventada da 404); nombre, los dos alcances y copiarlo (se muestra una sola vez); Abraham lo pasa y BRAIN lo guarda en `/workspace/.zenodo_token` con permisos 600 sin imprimirlo; `--borrador`; Abraham revisa y publica, o da el sí para `--publicar`; revocar el token.
  - **Orden pedido por Abraham (11:48):** auditoría de Tao → cotejo contra el repo → correcciones al PR #27 si caen → merge → token → borrador → publicación → revocar el token.
  - Los dos PDF del depósito siguen en brain-env con su md5 (2/2 contra `archivos-deposito-v2.0.json`, medido en la 009).
- **Espera decisión de Abraham:**
  - el «confirmo» a Tao, o auditar el bloque 1 con una instancia nueva de Brain;
  - el merge del PR #27;
  - el token;
  - el alcance (sin el control de las salidas);
  - la frase de licencia comercial en Conflict of interest;
  - el título igual al de la v1.0.

## Auditoría del laboratorio por TITÁN Tao (pedido 2026-10-12)

- **Tao es un Super Agent** (TITÁN Tao).
  - Disparadores: DM, mención y asignación.
  - Repo por defecto: `mudh-mobile`.
  - Tiene GitHub de lectura y escritura (rama y PR, nunca merge) y sandbox; no tiene el gateway de brain-env.
  - **Pregunta antes todo lote de 5 o más escrituras**, aunque el pedido lo detalle («un pedido detallado es el plan y no la confirmación»). Una auditoría con entrega en git y Doc siempre le pide una vuelta más.
- **Pedido:** `docs/auditorias/2026-10-12-pedido-auditoria-tao-laboratorio.md`.
  - Abarca el laboratorio entero: v2.0, Tabla 7 y salidas, nulo por circuito, brazo S y escape, circuitos y DBC3, expediente de agosto y H4.
  - Se audita contra los logs crudos, preguntando en cada afirmación si su instrumento podía dar rojo.
  - Pide propuestas para sacarle más provecho, con falsador y costo.
- **Enviado** el 2026-10-12 a las 11:36, a pedido de Abraham (lo pidió dos veces).
  - Tarea https://app.clickup.com/t/86e3p74xa en Pipeline TITAN; mención a Tao en el comentario https://app.clickup.com/t/86e3p74xa?comment=90170261435881.
  - **La asignación falló**: asignar agentes a tareas está apagado en el workspace. El disparador es la mención.
- **Entregada (2026-10-13-001):** PR #28 (`dd9da1c`, 13-oct 00:17) y Doc en el Space; la revisión contra el estado vivo está en la 2026-10-13-001. Lo que sigue en este bloque es el estado del 12 a las 11:56 y quedó superado.
- **Estado (medido en la 2026-10-12-009, 11:56): parado, esperando el «confirmo» de Abraham.**
  - Tao contestó a las 11:39:43 (https://app.clickup.com/t/86e3p74xa?comment=90170261436691): «Leí el alcance y confirmé el conectoma en 47d940e. Todavía no audité los logs ni emití conclusiones.» Pide «confirmo» para 7 escrituras: rama, archivo y PR en el conectoma; Doc en el Space; rama, `AGENT-TAO.md` y PR en `mudh-mobile`.
  - No hay rama `titan/auditoria-tao-laboratorio-2026-10-12`, ni PR nuevo en el conectoma ni en `mudh-mobile`, ni Doc suyo.
  - Actividad de Tao del 1 al 12-oct: 2 comentarios (3-oct, auditoría de DBC3-live, https://app.clickup.com/t/86e3jk397; 12-oct, 11:39).
  - **Créditos: NO MEDIDO para BRAIN.** Se ven en el perfil de Tao → Credits y en Settings → AI Usage → Activity. Según el Help Center, toda corrida de un Super Agent consume créditos aunque sólo conteste (100 a 300 estimados por uso, más con más acciones); Brain no consume créditos de IA.
  - **No reenviar el pedido.** Si Abraham confirma, BRAIN publica en el hilo la confirmación con la mención y le pide empezar por el bloque 1 (v2.0, PR #27).

## Paper y Tabla 7 (respuestas 002 a 009 del 10-oct y 003 y 004 del 11-oct)

- **Script:** `tools/table7_reciprocity_by_class.py` en `titan/tabla7-reconstruida-2026-10-10`, PR #26.
- **Anotaciones:**
  - con las de marzo (`c03ad46`): L3 16/16 y Tabla 7 8/8;
  - con el pin `17fc577`: L3 10/16 por recambio de `root_id`, y Tabla 7 8/8 a un decimal, lo que confirma el «What has not changed» del erratum.
- **El 8,7% sensory→descending es doble redondeo:** 2.104/24.327 = 8,6488% con las de marzo y 2.104/24.326 = 8,6492% con el pin, o sea 8,6.
- **Umbral ≥5:** 2.700.513 aristas y 13,98%, igual al ítem 5 del erratum.
  - intra-sensory 37,5 (482 de 1.287); intra-motor 35,0 (28 de 80); intra-visual centrifugal 23,4; intra-optic 17,1;
  - sensory→central 13,8; sensory→descending 2,8; sensory→motor 1,3 (5 de 373); optic→motor sin aristas.
- **Nulo por circuito y tendencia (003), `tools/table7_circuit_null.py`, en brain-env sin push:**
  - cruces con la 002 PASS en los dos umbrales; Tabla 7 8/8; nulo CP del erratum reproducido a 0,04%; conservación PASS;
  - con CP, la tendencia es EXPLICADO_POR_EL_NULO en los dos umbrales;
  - con CM no vale, porque el seudoconteo domina;
  - **veredicto de instrumento FAIL** por el control negativo.
- **Embudo de salida (004):** 1.485 neuronas (1,07%; descending, motor y endocrine) reciben el 2,37% de los cables. Lo que les llega tiene 13,19 / 9,83 / 3,58% de vuelta, contra 26,60% global. Descriptivo, sin nulo.
- **Control de las salidas:** 005 (`7e75cde`), 006 (`c99494f`), 007 (`f436f21`), 008 (`2093d57`) y 009 (`95e8d6c`), en la rama de la Tabla 7. Los números están en el veredicto operativo.
- **Hecho en el PR #27 (2026-10-12-007):** el ítem 9 y el 8,6 pasados a `docs/ERRATUM.md` y a `docs/PIVOTE-RECIPROCIDAD.md`, y la SECCION-V2 corregida traída a main.
- **Espera decisión de Abraham:** el merge del PR #27, y consolidar en main el expediente de ramas (PR #1, #2, #3).
- Los `results/` y JSON de la Tabla 7 y de la 003 a la 009 están sólo en brain-env, sin credencial de push. Los logs de la 004 a la 009 sí están en la rama.

## Estado confirmado en main (H4)

- Alignment guard: 7 contratos.
- Loader oficial: 6 contratos; 8/8 trials Aymanns reales con manifests `BIEN`.
- Features ROI, contexto y bouts: 7 contratos.
- Null por bouts: 5 contratos; distribución pooled exacta de 999 scores publicada.
- **Generalización intra-animal:** 4 contratos; `balanced accuracy=0.5018855395873556`, `p=0.623`. No hay evidencia de generalización.
- **Estabilidad temporal:** 5 contratos; `p=0.055`. Es sugestiva, no positiva.
- Regresión integrada: 34 contratos. Auditoría: `docs/auditorias/2026-10-02-004-auditoria-main-final-34-contratos.md`, 36/40.

## Estado de producto y ciencia

SparseLTC, DualBrain y DBC3 son trabajo propio de Abraham.

- **Medido en `mojo-absoluto`:**
  - HC-2: SparseLTC empata 48/48 con el control lineal sobre FlyWire real;
  - HC-3b: DBC3 aprende más rápido en una tarea (AULC 0,823 contra 0,635).
- **Medido en el expediente de ramas:**
  - sel_post sobrevive a los nulos de topología y de signo (z = +181 y +6,31; 0/40);
  - el efecto temporal global no sobrevive (39 nulos, p = 0,25);
  - la ventaja de tau compleja no se sostiene (p = 0,60).
- **Brazo S y la hipótesis de agosto (respuesta 008):**
  - **El brazo S ya había corrido** en sustrato feedforward (23-ago en Kaggle y 2-oct en brain-env, mismos números): W y S indistinguibles en 4/4. El «difieren» de LinScale era una p normal de 0,046; la t de Welch da 0,0646 y la permutación exacta 0,0570. La 007 decía que nunca se corrió: era falso, corregido en la 008 y en el Doc de la 007.
  - **Hoy corrió en el reservorio recurrente de SparseLTC** (motivo de escape de 26 neuronas, 88 aristas, 0 inhibitorias; ρ = 0,9; τ fija heterogénea en [0,06; 0,18]): RW contra RS empate 4/4, LW contra LS empate 4/4, RW contra RB 0/4. **En tareas genéricas paga la sparsity, no la mosca.** El reservorio fijo es peor que el react denso de agosto en 3/4 (Gated 15,7×).
  - **Neurona líquida:** A contra F (memoria de DualBrain con τ constante) gana sólo en MultiCue (0,263×, Holm 0,0044) y empata 3; la τ líquida sobre el cableado de la mosca, empate 4/4. **En el escape, entrenada, gana a la τ fija (012); contra un control con los mismos parámetros sólo aguanta la forma plena (013), también con optimización ajustada (014).**
  - **Tendencia sin firmar:** en MultiCue la mosca tiene 0,42× el error de su shuffle con τ fija y 0,65× con τ líquida (p 0,38 con 10 semillas).
  - **Hipótesis «conocimiento de existencia»** (Doc del 23-ago; `CONTEXTO-motor.md` §5): aprendizaje mínimo sostenido como anatomía; apagar y prender sostenido como ingeniería (compuerta, 21,85× a 108,11×) y NO MEDIDO en la mosca; «el conocimiento está en el cableado», sin señal funcional en tareas genéricas y **sostenido en su función: sin entrenar, como lateralidad (010) y como cableado fino fuera del techo (011); con la τ líquida diagonal entrenada se compensa (013); con la plena entrenada gana en promedio (88%, Mann-Whitney p 0,0002) pero no en cada entrenamiento (015); con entrada por tipo de neurona y lector entrenado no paga (2026-10-12-005)**; «la neurona líquida es necesaria», **sostenida en la forma plena contra su control de parámetros y con optimización ajustada (013 y 014)**; la diagonal ganaba por parámetros. **Esa forma es la de la LiquidCell de DualBrain aplicada por neurona; la líquida nativa de SparseLTC (τ / (1 + tau_gain·|drive|)) no se probó (016).**
  - Corrida: run de Actions `38143998992`, 37/37; resultado crudo en `results/brazo_s_recurrente_2026-10-11/` de la rama `titan/brazo-s-recurrente-2026-10-11` (`9473852`), sin PR.
- **Escape a lazo cerrado, el brazo S en la función propia del motivo (respuesta 010):**
  - El mismo motivo, sin entrenar, con looming por sus visuales (cada una por el ojo de su lado) y lectura sólo por los dos GF. **Las 88 aristas del motivo son ipsilaterales.**
  - **W contra S:** acierto 180/180 contra 0,5102 (7/200, p = 0,0398); supervivencia 180/180 contra 0,6605 (6/200, p = 0,0348). La mosca gana, por poco.
  - **W contra SL** (shuffle de grado exacto que conserva el lado): 0,9806 y 0,9983 (149 y 161 de 200 en el 100%): **empate. Paga la lateralidad.** El reflejo escrito a mano también saca 1,0/1,0.
  - **τ:** W saca 180/180 con τ fija heterogénea, uniforme, líquida y con el brazo lineal: todo en el techo.
  - Instrumento: `tools/escape_motivo/escape_motivo.py` en `titan/escape-motivo-2026-10-11` (pre-registro `445646a`, resultados `4afb8f9`), brain-env, 5,18 min, sin PR.
- **Escape fuera del techo (respuesta 011):**
  - Disparo por umbral calibrado con sólo ruido, escape balístico, amenazas a ±10° a ±90° con ruido 0,1 y 0,3 (480 ensayos) y un objeto que gira sin acercarse (80 ensayos, lo correcto es no disparar).
  - **Puntaje (supervivencia + rechazo) / 2:** W 0,8177 contra SL 0,6819 (6/200, p = 0,0348), S 0,5973 (p = 0,0100) y B 0,4023 (p = 0,0050). **Paga el cableado fino**: la mosca hace las dos cosas a la vez (80/80 de rechazo y 0,6354 de supervivencia); por separado no le gana a SL (p 0,21 y 0,22).
  - **τ líquida congelada al azar: peor.** En W, 0,5604 contra 0,6354 (1 contra 37, McNemar p < 0,0001); en 187 de 199 redes S y 186 de 199 SL. La τ uniforme 0,119 también pierde (0,5437; 6 contra 50). El lineal gana por poco (0,6500; 7 contra 0). ~~Paga la τ fija heterogénea.~~ **Corregido por la 012:** eso valía sólo contra la líquida congelada al azar; entrenada, la líquida gana.
  - **Letra chica:** el reflejo escrito a mano sin LC6 le gana a la mosca (0,9167; latencia 10 contra 14). El modelo de entrada se eligió para que LC6→GF importe (declarado).
  - Instrumento: `tools/escape_motivo/escape_dificil.py` (md5 sellado en `e030e19`, resultados en `7163c15`), brain-env, 7,16 min, sin PR.
- **τ líquida entrenada en el escape difícil (respuesta 012):**
  - Mismo sujeto, tarea y lectura de la 011; sólo se entrena la τ, los tres brazos arrancan en la τ fija heterogénea (guarda True). Estrategia evolutiva, 40 × 8 pares, 4 semillas; prueba con ruido separado.
  - **En prueba:** FIJA_ENT (26 parámetros) 0,8263; LIQ_DIAG (78) 0,9216; LIQ_PLENA (1.378) 0,9826; FIJA_HET sin entrenar 0,8240; reflejo a mano C+L 0,9062.
  - E1 DIAG contra FIJA_ENT 393 contra 7 (p 2,4e-106) y E2 PLENA contra FIJA_ENT 608 contra 3 (p 8,9e-177): **MEJOR, 4/4 semillas.** E3 FIJA_ENT contra FIJA_HET 271 contra 282 (p 0,67): **entrenar la τ fija no agrega nada.**
  - **LA LIQUIDA ENTRENADA PAGA** contra la τ fija entrenada. **Corregido por la 013:** contra un control con los mismos parámetros, la diagonal pierde y sólo la plena gana.
  - Instrumento: `tools/escape_motivo/liquida_entrenada.py` (md5 `0bb3f8f4…` sellado en `95a6d92`, resultados en `f042e6f`), brain-env, 12,50 min, sin PR.
- **Control de parámetros y de cableado (respuesta 013):**
  - Cada líquida contra un brazo no líquido con las mismas señales y los mismos parámetros metidos en la entrada (τ fija entrenable); mismo optimizador, datos y punto de partida (guarda True). La 012 se reproduce exacta.
  - **Diagonal (78):** no líquida 0,9443 contra líquida 0,9216; 149 contra 77 (p 1,9e-06): **la líquida PEOR.** La ventaja diagonal de la 012 era de parámetros.
  - **Plena (1.378):** líquida 0,9826 contra no líquida 0,9214; 252 contra 12 (p 1,3e-59), 4/4: **la líquida MEJOR.**
  - **Cableado con la líquida diagonal entrenada:** W 0,9521 contra 24 SL (media 0,8488, máx. 0,9573), 1/24 la iguala, p 0,08: **W NO GANA a SL.** Contra 8 S (descriptivo): media 0,7771, 0/8.
  - Instrumento: `tools/escape_motivo/control_parametros.py` (md5 `342069aa…` sellado en `d9cbdf9`, resultados en `d27edad`, md5 2/2 en clon fresco), brain-env, 2 procesos, 43,12 min, sin PR.
- **La plena con optimización ajustada y sobre SL (respuesta 014):**
  - Cada semilla de LIQ_PLENA y NOLIQ_PLENA con dos optimizadores (C1 σ 0,10 lr 0,05; C2 σ 0,03 lr 0,02), 60 iteraciones, elegido por entrenamiento.
  - **P3:** líquida 0,9854 (desvío 0,0041) contra no líquida 0,9453 (desvío 0,0506); 169 contra 15 (p 3,6e-34), 4/4: **LA PLENA GANA POR SER LIQUIDA.** Desempate no pre-registrado: con el mejor de los dos mirando la prueba, la no líquida saca 0,9729 y la líquida sigue arriba en 3 y empata en 1.
  - **Q_SL_PLENA:** W 0,9802 contra 24 SL (media 0,9090, máx. 0,9760), 0/24, p 0,04: W GANA. **Matizado por la 015:** vale para la semilla 0 y como tendencia de grupo, no para cada entrenamiento.
  - Instrumento: `tools/escape_motivo/control_plena.py` (md5 `45bad2a8…` sellado en `be292b0`, resultados en `f0d0c1c`, md5 2/2 en clon fresco), brain-env, 2 procesos, 48,79 min, sin PR.
- **Firma de la 014 con 69 SL y 8 semillas (respuesta 015):**
  - Protocolo exacto de la 012 y la 014; 45 SL nuevas más las 24 de la 014 (leídas de su json con md5); semillas 1 a 7 nuevas de W. REPRODUCE=True.
  - **Q1:** W semilla 0 (0,9802) contra 69 SL: 0/69, p 0,014, W GANA. **Q2:** la peor de 8 (0,9469): 25/69, p 0,37, W NO GANA. **VEREDICTO_FIRMA = SOLO LA SEMILLA 0.**
  - **Grupo:** semillas 0 a 3 por encima de las 69 SL; 4 a 7 no (14, 25, 20 y 5 de 69 las igualan). Mann-Whitney 8 W contra 69 SL: U 488 de 552 (88%), p 0,0002. SL media 0,9165, máx. 0,9781.
  - Instrumento: `tools/escape_motivo/firmar_plena_sl.py` (md5 `df15f3da…` sellado en `967fbb2`, resultados en `cc531e7`, md5 2/2 en clon fresco), brain-env, 2 procesos, 54,79 min, sin PR.
- **En criollo (015):** tenemos un reflejo de escape de 26 neuronas sacado de FlyWire que funciona en simulación desde el día cero y llega a 0,98 entrenando sólo la τ líquida plena. **Potencial:** reflejos de mosca compilados a microcontroladores (pocos KB), un resultado científico honesto y una receta repetible con otros circuitos. **Techo:** sólo simulación, un motivo, una tarea; el reflejo escrito a mano rinde 0,91 sin entrenar; cero hardware.
- **En criollo (2026-10-12-006, síntesis sin corrida):** la mosca sirve de **mapa** (catálogo, 10/10 predicciones) y de **reflejo chico y fijo** donde importan el lado y el cableado fino (010, 011, 014, 015); no sirve, hasta ahora, de **cerebro entrenable** mejor que lo clásico (008, 004, 005). Lo más maduro es el paper v2. DualBrain y DBC3 no se ganaron todavía un lugar en la cadena de la mosca. Orden propuesto: v2 (token de Zenodo de Abraham), líneas etiquetadas en Actions y, si pagan, el reflejo en C99/Q15 con paridad y `.text` en Actions y tamaño para ESP32 con el cross del taller.
- **Qué motor corre las 26 (respuesta 016, lectura de código):**
  - En el escape (010 a 015) corren con la ecuación de SparseLTC (`SparseConnectomeComplexLTC::step`, `mojo-absoluto` `main` `613bf49`) **reescrita en numpy**, con estado real, la matriz del motivo llevada a ρ 0,9 y entrada directa a las 20 visuales. Equivalencia: z + dt·(−z + tanh(drive))/τ_ef = (1 − t)·z + t·tanh(drive) con t = dt/τ_ef; con tau_gain = 0 es la FIJA_HET.
  - **La líquida que ganó (012 a 015) tiene la forma de la LiquidCell de DualBrain** (t = sigmoid(b + Vx·x + Vh·z)) aplicada a cada neurona; la nativa de SparseLTC es τ_ef = τ / (1 + tau_gain·|drive|) y no se probó.
  - **DualBrain entró sólo en la 008** (las 26 como vía react adentro de DualBrain, tareas genéricas). En el escape no hay memoria, compuerta ni cabeza de DualBrain.
  - El puente diseñado (ADR `docs/adr/2026-10-01-sparseltc-dbc3-adapter.md` de `mojo-absoluto`, «Propuesto»): SparseLTC → proyección a features → un solo DBC3 por flujo como lectura y controlador. **El primer acople real corrió en la 2026-10-12-003** (abajo).
- **Siguen NO MEDIDOS:** SparseLTC→DBC3 sobre señal biológica registrada (la 003, la 004 y la 005 usan estímulo simulado sobre cableado real), mapping ROI→FlyWire, null anatómico pareado y silenciamiento causal.
- **Robótica (respuesta 007):**
  - `swarm/` es el único robot de los repos y **no sale del conectoma**: 34 neuronas y 83 sinapsis escritas a mano con nombres de regiones de la mosca.
  - Con física de cuadricóptero X estándar, **el escape visual va hacia la amenaza en las 4 direcciones** (108/108 en la sensibilidad). Leer los motores con reflexión FL↔BR, FR↔BL lo da vuelta: 4/4 y 108/108 hacia afuera. Instrumento válido: reflejo físico 4/4 ALEJA y red nula 4/4 NEUTRO.
  - El test de `swarm/` no puede dar rojo (con los pesos en cero sale con 0) y la auditoría de `gen_swarm.py` devuelve `PASS` fijo con topologías mutadas.
  - Instrumento: `tools/swarm_lazo_cerrado.py` en la rama `titan/swarm-lazo-cerrado-2026-10-11`, sin PR.
  - **Idea mejorada (BEEC v2):** compilador de motivos certificados contra el nulo, interfaz por descendentes, cordón sintético con lazo de actitud, y entrenables la compuerta, la memoria DBC3, el readout y, en L2, la τ líquida plena (013 y 014). El falsador es el brazo S: en tareas genéricas empató (008); en la función propia gana por lateralidad (010), por cableado fino fuera del techo (011) y, con la líquida plena entrenada, en promedio contra SL (014 y 015); con entrada por tipo de neurona y lector entrenado no paga (2026-10-12-005). Cadena prevista (016): ojo → 26 en SparseLTC (reflejo) → DBC3 (memoria y compuerta) → descendentes → dron; **el tramo SparseLTC → DBC3 ya corrió en simulación (003 y 004)**.
  - **Arquitectura por etapas (2026-10-12-001, diseño, sin corrida):**
    - **Reparto:** E0 transducción con sensores comerciales («ser el transductor», con cámara de eventos y modelo de retina, queda para después); E1 rasgos sensoriales y E2 reflejos en **SparseLTC** sobre el cableado de FlyWire; E3 contexto y memoria en **DBC3**, una por flujo y nunca una por neurona (ADR, D1); E4 tabla descendente → orden; E5 lazo de actitud clásico o CPG (el cordón sintético); E6 carga, ESC y motores **clásicos y deterministas**, con el cerebro decidiendo sólo cuándo volver a cargar (una señal tipo hambre a la compuerta de DBC3). **El patrón DualBrain** (vía rápida, memoria y compuerta) une E2 y E3.
    - **Regla:** el cableado de la mosca entra donde gana en su función contra su barajado (S y SL) y contra un rival clásico entrenado; donde no, va lo clásico. **Aplicada en la 004:** el estado de vuelo (discreto) va a lo clásico. **Aplicada en la 005:** con entrada por tipos y lector entrenado, E2 va con lo clásico en esa tarea.
    - **«Todas las capacidades son reutilizables» queda como hipótesis:** contraejemplos medidos en la 008 y en la 005, y un solo circuito que paga en su función (010 a 015), con el reflejo a mano en 0,9167 (011).
    - **Dominios:** lo visual de movimiento relativo se traslada a cualquier plataforma; lo motor depende del cuerpo; el agua es mala para el flujo óptico.
    - **Antidrones** como detección y evasión, sí; interceptar es perseguir y las cazadoras no están en FlyWire. **Antimisiles:** recomendación de sacarlo del roadmap (velocidades, radar e infrarrojo, leyes de guiado, uso dual y control de exportaciones).
  - **Catálogo de circuitos en FlyWire v783 (2026-10-12-002, medido):**
    - Instrumento VÁLIDO (LC4 → DNp01 757 sinapsis; LC6 → DNp01 0) y **10 de 10 predicciones de literatura en el cableado** como aristas ≥ 5: LPLC2 → GF, LPLC4 → DNp07/DNp10 (Ache 2019), DNp09 → DNa02 excitatoria y MDN → DNa01 (Braun 2024), anillo EPG ↔ P-EN, HS → DNp15 y la vía olfativa. Vara baja: existencia, no fuerza ni función.
    - **Salida de la entrada a descendentes:** aterrizaje 22,8% (428 neuronas, 4.000 B), escape 15,6% (443, 3.520 B), flujo óptico 11,3% (55, 248 B), objetos chicos 1,1% (943, 8.648 B), olfato 0,5% (8.796, 428.106 B), rumbo 0% (93, 9.816 B). Giro (10 DN) y marcha (DNp09, MDN) tienen entrada repartida: sus 5 entradas mayores suman 9% y 21%. Descriptivo, sin nulo.
    - **Escape y aterrizaje:** 100% excitatorios y del mismo lado por dentro, y comparten entrada (LC4, LPLC2). ~~La entrada mayor de DNp01 y DNp09 es LC9, que no está en el motivo de 26.~~ **Corregido por la 003:** LC9 → DNp01 es 0; sus 1.167 sinapsis van a DNp09. A DNp01 le entran sobre todo LPLC2 (1.080) y LC4 (805). Y el aterrizaje visual es LPLC4 → DNp07 (1.448): DNp10 recibe 22 de LPLC4 y 0 de LC4 y LPLC2.
    - oDN1, BDN2 y LPLC3 no están con ese nombre en v783.
    - Instrumento: `tools/catalogo_circuitos/catalogo_circuitos.py` en `titan/catalogo-circuitos-2026-10-12` (md5 `4137ba5c…`, pre-registro `38baa15`, log `bb68d7f`, md5 2/2 en clon fresco), brain-env, 48,5 s, sin PR.
  - **Escape o aterrizaje según vuelo, primer acople SparseLTC → DBC3 (2026-10-12-003, medido):**
    - Sujeto: 28 neuronas (por lado 4 LC4 y 4 LPLC2 → DNp01, 4 LPLC4 → DNp07), 73 aristas, todas excitatorias e ipsilaterales; SparseLTC con τ fija heterogénea sin entrenar. Tarea: señal de vuelo o piso al principio, que se apaga; después looming por un lado u objeto que pasa; respuesta nada / escapar izq. / escapar der. / aterrizar. El lector ve sólo las 4 descendentes y la señal.
    - **DBC3 (4.696 parámetros, ecuaciones de `DBC3Motor` de `dbc3_lib.py`): 1,0000 en 4/4.** LSTM (4.564): 0,9990 a 1,0000, **EMPATE** (6 contra 0). Sin memoria: 0,672 (techo 2/3), **DBC3 MEJOR**. Regla a mano: 0,8143, **DBC3 MEJOR** contra un rival flojo. 16 SL con DBC3: 0,9997 a 1,0000, **W NO GANA** (p 0,38). VALIDO.
    - **Lectura:** la tubería anda de punta a punta y paga la memoria; la tarea quedó en el techo y la entrada no distingue tipos visuales, así que no separa DBC3 de LSTM ni la mosca del barajado.
    - En brain-env existe `/workspace/dbc3_motor.h` («clean-room reconstruction», sin pesos, md5 `6199c452…`); en el repo público `dualbrain` sigue faltando. No se usó.
    - Instrumento: `tools/escape_aterrizaje/escape_aterrizaje_dbc3.py` en `titan/escape-aterrizaje-2026-10-12` (md5 `4d40477d…`, pre-registro `d9f012d`, log `af4bea6`, md5 2/2 en clon fresco), brain-env, 59,4 min, sin PR.
  - **Memoria dura (2026-10-12-004, medido):**
    - Mismo sujeto y motor que la 003 (módulo importado sin cambios); 120 pasos, cambio de contexto en la mitad de los ensayos (entre los pasos 20 y 80), cuatro pulsos de engaño, estímulo entre los pasos 90 y 105. Dos presupuestos: canónico (DBC3 4.696, LSTM 4.564) y chico (808 contra 840). 400 pasadas de 128.
    - **Ninguna red aprende la memoria:** DBC3 0,658 a 0,664 (una semilla canónica 0,743), LSTM 0,658 a 0,672, sin memoria 0,655 a 0,657 (techo 2/3). **H1 EMPATE en los dos presupuestos.** H2: DBC3 MEJOR por poco en el canónico, EMPATE en el chico. **H3: la máquina de estados (0,7663) le gana a DBC3 en los dos.** VALIDO en los dos (el control positivo se bajó de 0,80 a 0,75 tras el humo, antes de correr, declarado).
    - **Lectura:** con este entrenamiento ninguna red cruza 90 pasos de espera; el estado de vuelo va a lo clásico. La ventaja de DBC3 en memoria diferida de sus benchmarks (25 pasos) no se ve acá. Queda abierto si es entrenamiento.
    - Instrumento: `tools/escape_aterrizaje/memoria_dura.py` en `titan/memoria-dura-2026-10-12` (md5 `c486e79f…`, pre-registro `f58cf8e`, logs `0431f35`, md5 3/3 en clon fresco), brain-env, 25,6 y 30,2 min en paralelo, sin PR.
  - **Entrada visual por tipo de neurona (2026-10-12-005, medido):**
    - Mismo motivo y motor que la 003 (módulo importado sin cambios). Cada tipo visual con su sintonía de literatura: LC4 velocidad de expansión (von Reyn 2017; Ache 2019), LPLC2 tamaño mientras hay expansión y punto que se traslada (Ache 2019; Klapoetke 2017; Kim 2023); LPLC4 sin fisiología encontrada, en tres variantes declaradas (COMO_LPLC2, SILENCIOSA, MOVIMIENTO). Tarea de robot: amenaza rápida → escapar al otro lado; acercamiento lento → aterrizar en vuelo, nada en el piso; objeto que pasa → nada. Estado de vuelo clásico (un lector ridge por estado sobre las 4 descendentes). Nulos SL y T (cableado intacto, sintonías barajadas dentro del lado), 300 cada uno; Holm sobre 12 por cola; ruido 0,15 y 0,45 (calibrado sobre el rival crudo antes del sellado).
    - **Cableado por tipo:** DNp01 recibe LC4 0,498 y LPLC2 0,502; DNp07, LPLC4 0,997. SL reparte (DNp01 0,21 / 0,31 / 0,49; DNp07 0,23 / 0,33 / 0,45).
    - **VEREDICTO_GLOBAL: NO PAGA (PIERDE en SILENCIOSA).** Contra SL la mosca nunca queda arriba (6/6 primarias, 12/12 de robustez, 3/3 con MLP). Contra T: muda pierde (300/300 y 299/300 la igualan o superan; Holm 0,0399 con ruido 0,15), MOVIMIENTO le gana sin pasar Holm (2/300 y 3/300; Holm 0,1196 y 0,1462; robustez 0 a 3 de 100; MLP 0/30) y COMO_LPLC2 empata.
    - **El rival clásico crudo (ridge sobre las 24 entradas) le gana en 6 de 6** (0,8750 a 0,9906 contra 0,6878 a 0,8628; p ≤ 1e-66). Los 28 estados conservan la información (0,8717 a 0,9867): lo que pierde es el embudo de 4 descendentes. Control negativo (AGNOSTICA) 30/30 idénticos; con esa entrada la mosca también queda debajo de SL (99/100, descriptivo).
    - **Lectura:** con lector entrenado, en esta tarea, E2 va con lo clásico (regla de la 001). El cableado por tipos podría pagar como líneas etiquetadas (cada descendente con su umbral dispara una acción): NO MEDIDO. Si el reparto de la mosca fuera bueno para un lector así, LPLC4 tendría que responder al movimiento: hipótesis, no medida. **Las líneas etiquetadas quedaron diseñadas en la 2026-10-12-008, sin sellar ni correr.**
    - Instrumento: `tools/escape_aterrizaje/entrada_por_tipos.py` en `titan/entrada-por-tipos-2026-10-12` (md5 `e060c4bf…`, pre-registro `75ca27c`, logs `f7844be`, md5 4/4 en clon fresco), brain-env, 60,0 y 53,5 min en paralelo, sin PR.
  - `docs/agents/CONTEXTO-motor.md` está vencido desde el 24-ago: dice que nadie linkeó DualBrain, y en la rama de materialización hay un ELF linkeado de 44.292 B (no flasheable) y un arnés de 512 pasos contra el oráculo numpy. El estado de robótica vive acá hasta reescribirlo. Sus §1, §4 y §6.2 (el brazo W «nunca testeó» la hipótesis y el diseño W/S) quedan superados por la 008 y la 010 a la 015.
  - **Espera decisión de Abraham:** aplicar el parche de lectura en `swarm/` y corregir el «Correcto» de su README; adoptar BEEC v2 como norte de la línea de robótica; **en L2, τ líquida plena entrenada sobre el cableado fijo (1.378 parámetros, unos 5,5 KB en float32; costo en ESP32 NO MEDIDO), que reemplaza a la diagonal de la 012**, o probar antes la líquida nativa de SparseLTC (016); **adoptar la arquitectura por etapas con su regla de reparto, y sacar antimisiles del roadmap (2026-10-12-001)**; **tras la 004 el estado de vuelo quedó en lo clásico; tras la 005: probar líneas etiquetadas contra SL y T con la misma entrada por tipos, o dar por cerrado que en esa tarea E2 va con lo clásico**; **el orden de la 006: la v2 del paper (lista en el PR #27, faltan el token y el merge: 007), líneas etiquetadas en Actions y, si pagan, el reflejo en C99/Q15**.

## Próximos pasos

1. **Consolidar git:** primero el PR #27 (v2.0); después el linaje de ramas a main (PR #1, #2, #3) o un PR sólo de documentos. Decide Abraham.
2. **Cerrar el 003:**
   - sacar el seudoconteo de la media del nulo o subir K;
   - explicar el 8/20 del control CP con ≥1;
   - volver a correr y firmar;
   - subir el script, los tests y los logs a la rama.
3. **v2.0: lista (007).** En el orden que pidió Abraham (009):
   - la auditoría de Tao del bloque 1 y su cotejo contra el repo, con las correcciones al PR #27 que caigan;
   - el merge del PR #27;
   - el token con `deposit:write` y `deposit:actions` (pasos en la 009);
   - correr `tools/zenodo/depositar_v2.py --borrador` en brain-env;
   - que Abraham revise el borrador en Zenodo;
   - publicar con su sí;
   - revocar el token.

   El control de las salidas (con BY y lo que aguanta FWER marcado), LC6→GF y sel_post pasan al **Paper 2** (recomendación, decide Abraham).
4. **Abiertos para una v2.1 o el Paper 2:** NPC por sinapsis o null combinado de grado y neuropilo; ventana y tau de sel_post; Lin región por región; Betzel arista por arista; fila AN y décima clase de la Tabla 5; Tabla 8 no reproducible; el rango de Gouwens & Wilson; barrido sistemático de literatura para la §3.4; el null anatómico sobre la población de salida de la Tabla 5.
5. **La 007:** con R = 10.000 para Holm; D2 con el nulo de región.
6. H4 estacionada.
7. **Robótica (015, 016 y 2026-10-12-001 a 006; orden propuesto en la 006, decide Abraham):**
   - **Hechos:** ~~el catálogo de circuitos~~ (002); ~~escape o aterrizaje según vuelo~~ (003, en el techo); ~~memoria dura~~ (004, nadie aprende); ~~entrada por tipos visuales~~ (005, NO PAGA).
   - **1) Líneas etiquetadas** (cada descendente con su umbral dispara una acción) contra SL y T con la misma entrada, **en Actions**: repo público, gratis, 11,6× más rápido y VM limpia; instalar numpy con `setup-python`. **Diseñadas en la 2026-10-12-008, sin sellar ni correr.**
   - **2) Si pagan, el reflejo en C99/Q15:**
     - paridad contra numpy;
     - `.text` y latencia en Actions x64 y arm64;
     - tamaño para ESP32 con `xtensa-esp32-elf-gcc` del taller;
     - ninguna placa figura en el inventario y un emulador de Espressif está NO MEDIDO.
   - **3) Arreglar el dron** (parche de lectura, un test que afirme y giróscopo en vez de «altitud» en el haltere) y montarle el reflejo.
   - **Estacionado:** DBC3 contra LSTM con entrenamiento largo o por etapas (la máquina de estados ya gana).
   - **Siguen abiertos:**
     - la líquida nativa de SparseLTC (tau_gain, 26 parámetros) en el escape contra su control;
     - revisar LC9 → DNp09;
     - el lector del rumbo (camino de EPG a descendentes);
     - nulos para las fracciones del catálogo;
     - DBC3 en C con el `dbc3_motor.h` reconstruido de brain-env, con paridad contra el `DBC3Motor` de torch;
     - el cordón nervioso en MANC o BANC para la etapa E5;
     - en el escape: SL con varias semillas cada una, la plena sobre S, condiciones fuera de las entrenadas y el otro modelo de entrada.
8. **Brazo S (respuestas 008, 010 a 015):**
   - MultiCue con 50 semillas para decidir la tendencia 0,42×;
   - un S que conserve Dale por neurona en motivos con inhibición;
   - reescribir `CONTEXTO-motor.md`;
   - PR y review de `titan/brazo-s-recurrente-2026-10-11`, `titan/swarm-lazo-cerrado-2026-10-11`, `titan/escape-motivo-2026-10-11`, `titan/catalogo-circuitos-2026-10-12`, `titan/escape-aterrizaje-2026-10-12`, `titan/memoria-dura-2026-10-12` y `titan/entrada-por-tipos-2026-10-12`.
9. **Auditoría de Tao:** arrancó y frenó (009): contestó a las 11:39 y espera el «confirmo» de Abraham. **No reenviar el pedido.** Con el sí, BRAIN publica la confirmación en el hilo; cuando Tao entregue su PR y su Doc, cotejar su auditoría contra el repo (no contra su Doc) y corregir lo que caiga, primero en el PR #27. Sin el sí, la alternativa es una instancia nueva de Brain sobre el bloque 1.

## Fuentes

- `docs/agents/respuestas/2026-10-12-009-tao-no-audito-pidio-confirmo-y-el-deposito-lo-espera.md`
- `docs/agents/respuestas/2026-10-12-008-lineas-etiquetadas-disenadas-sin-correr.md`
- `docs/agents/respuestas/2026-10-12-007-la-v2-del-paper-esta-lista-y-el-erratum-tenia-errores-sobre-la-v1.md`
- `docs/auditorias/2026-10-12-pedido-auditoria-tao-laboratorio.md`
- En el PR #27: `docs/V2-CIERRE.md`, `docs/v2/paper1-v2.0.md`, `docs/ERRATUM.md` revisado, `docs/v2/render-v2.0.log` y `docs/v2/verificar-v2.0.log`
- `docs/agents/respuestas/2026-10-12-006-en-criollo-la-mosca-sirve-de-mapa-y-de-reflejo-chico-no-de-cerebro-entrenable.md`
- `docs/agents/respuestas/2026-10-12-005-entrada-por-tipos.md`
- `docs/agents/respuestas/2026-10-12-004-memoria-dura-dbc3-contra-lstm.md`
- `docs/agents/respuestas/2026-10-12-003-escape-o-aterrizaje-con-dbc3.md`
- `docs/agents/respuestas/2026-10-12-002-catalogo-de-circuitos-en-flywire.md`
- `docs/agents/respuestas/2026-10-12-001-arquitectura-por-etapas.md`
- `docs/agents/respuestas/2026-10-11-016-como-operan-las-26-neuronas.md`
- `docs/agents/respuestas/2026-10-11-015-firma-de-la-014-y-en-criollo.md`
- `docs/agents/respuestas/2026-10-11-014-la-liquida-plena-aguanta-el-control.md`
- `docs/agents/respuestas/2026-10-11-013-control-de-la-liquida-mitad-parametros-y-sin-ventaja-del-cableado.md`
- `docs/agents/respuestas/2026-10-11-012-la-liquida-entrenada-paga-en-el-escape.md`
- `docs/agents/respuestas/2026-10-11-011-escape-dificil-paga-el-cableado-fino-y-la-liquida-empeora.md`
- `docs/agents/respuestas/2026-10-11-010-escape-en-lazo-cerrado-la-mosca-gana-a-su-shuffle-por-lateralidad.md`
- `docs/agents/respuestas/2026-10-11-009-en-lugar-de-la-neurona-liquida-tasa-con-fuga-y-tau-fija.md`
- `docs/agents/respuestas/2026-10-11-008-el-brazo-s-ya-habia-corrido-y-en-el-reservorio-recurrente-paga-la-sparsity-no-la-mosca.md`
- `docs/agents/respuestas/2026-10-11-007-mosca-a-robot-idea-mejorada-y-el-dron-que-escapa-hacia-la-amenaza.md`
- `docs/agents/respuestas/2026-10-11-006-traspaso-tecnico-del-conectoma.md`
- `docs/agents/respuestas/2026-10-11-004-el-repo-del-conectoma-de-punta-a-punta.md`
- `docs/agents/respuestas/2026-10-11-003-nulo-por-circuito-base-erratum-EN-CURSO.md`
- `docs/agents/respuestas/2026-10-10-009-correccion-multiple-del-nulo-fuerte.md`
- `docs/agents/respuestas/2026-10-10-008-correccion-multiple-del-nulo-regional.md`
- `docs/agents/respuestas/2026-10-10-007-nulo-que-conserva-la-region.md`
- `docs/agents/respuestas/2026-10-10-006-nulo-fuerte-por-permutacion.md`
- `docs/agents/respuestas/2026-10-10-005-que-salida-controla-cada-clase.md`
- `docs/agents/respuestas/2026-10-10-002-tabla7-reconstruida.md`
- `docs/agents/respuestas/2026-10-10-004-que-hay-al-final-de-cada-cable.md`
- `docs/ERRATUM.md` y `docs/PIVOTE-RECIPROCIDAD.md` (las versiones revisadas están en el PR #27)
- `00-ENTORNOS-Y-CAPACIDADES.md` (raíz; foto medida el 26 y 27-ago; leído en `5405f03` para la 006).
- En `mojo-absoluto` `main` (`613bf49`): `include/mojo_abs/connectome_ltc.hpp` y `docs/adr/2026-10-01-sparseltc-dbc3-adapter.md`.
- `README.md` de `dualbrain` (`main`) y el Doc de ClickUp del 3-oct «Mojo Absoluto Compiler: DualBrain/DBC3, SparseLTC e hipótesis de desarrollo» (https://app.clickup.com/90171457413/docs/2kza6fw5-19197/2kza6fw5-21757).
- En brain-env: `/workspace/dbc3_lib.py` (md5 `39566d9a…`, `DBC3Motor` del notebook DBC3-v3), `/workspace/dbc3_motor.h` (md5 `6199c452…`, reconstrucción en C sin pesos) y `/workspace/v2cierre_2026-10-12/` (PDF v1.0, su texto, los dos PDF del depósito y los clones).
- Literatura verificada en la 002: Ache 2019 (Nat Neurosci, aterrizaje), Braun 2024 (Nature, redes de descendentes), Sapkal 2024 (Nature, oDN1 y BDN2), Simpson 2023 (Curr Opin Neurobiol, revisión de descendentes).
- Literatura verificada en la 005: von Reyn 2017 (Neuron, LC4 velocidad), Ache 2019 (Curr Biol, LPLC2 tamaño y suma en el GF), Klapoetke 2017 (Nature, LPLC2 ultraselectiva), Kim 2023 (Curr Biol, LPLC2 y el punto que se traslada), Dombrovski 2025 (Nature, entradas visuales del GF); LPLC4 sin fisiología encontrada.
- Literatura verificada en la 007: Betzel 2026 (PLOS Complex Syst), Bates 2026 (Nature 656:957–970), Gouwens & Wilson 2009 (J Neurosci 29(19)), Nagel & Wilson 2011 (Nat Neurosci 14), Tuthill & Wilson 2016 (Curr Biol 26(20)), Hasani 2022 (Nat Mach Intell 4), Costi 2025 (Biomimetics), Yu 2026 (AGI 2025), Jin 2026 (arXiv), Gordon & Scott 2009 (Neuron 61), Shiu 2022 (eLife 11), FlyWire 2024 (Zenodo 10676866) y los alcances de token de developers.zenodo.org.
- Leído en la 009: el Help Center de ClickUp («How are AI Credits consumed?», «Track your Workspace's Brain AI usage», «ClickUp Brain AI feature availability and limits» y «Manage Super Agents and create templates») y la creación del token en developers.zenodo.org.
- En ramas: respuestas 063 a 124 de `titan/materializacion-h4-guard-2026-10-02` y respuestas 2026-09-22/23 de `titan/auditoria-integra-2026-08-25`.

## NO MEDIDO

- El nulo por circuito está corrido, pero no firmado (FAIL de instrumento).
- El embudo de salida, sin nulo.
- Un nulo por neuropilo de cada sinapsis.
- D2 con el nulo de región.
- La 007 con R = 10.000.
- FWER por rangos (min-P).
- Signo fisiológico por par de clases.
- El cruce con Lin 2024.
- 57 archivos de main y 73 rutas de ramas sin leer en la 004.
- Mapping anatómico, null anatómico pareado, causalidad y equivalencia SparseLTC→DBC3 sobre señal real.
- **v2.0 (2026-10-12-007):**
  - nadie miró los PDF a ojo (sólo extracción de texto);
  - metadatos sin probar contra la API real;
  - borrador, depósito y publicación;
  - lectura humana completa del manuscrito reconstruido contra la v1.0;
  - barrido sistemático de literatura para la §3.4;
  - el rango 5–20 ms de Gouwens & Wilson;
  - la página del token por dentro (009: sólo que la ruta existe y pide login).
  - El alcance sin el control de las salidas es una recomendación, no una decisión.
- **Auditoría de Tao (009):** la mención lo disparó y frenó en su pedido de confirmación; la auditoría no existe, así que nada se cotejó contra ella. Los créditos que gastó (por corrida y en el mes), si quedan créditos para la corrida completa y las corridas suyas que no dejan rastro en tareas (DMs), NO MEDIDOS para BRAIN.
- Líneas etiquetadas (2026-10-12-008): todo; sólo hay diseño.
- Robótica: hardware, la tabla descendente → orden, GF-01 compilado en Q15 y montado en el dron, la lectura por DNp09 y cualquier medición fuera de distribución.
- Arquitectura por etapas (2026-10-12-001): todo salvo E2 y el tramo E2 → E3 en simulación (003 a 005); DBC3 en C sobre un microcontrolador; el cordón (MANC, BANC); la cámara de eventos; la transferencia a marítimo y terrestre; cualquier medición de antidrones; la hipótesis «todas las capacidades son reutilizables».
- Catálogo (2026-10-12-002): fuerza y función de las conexiones (sólo existencia ≥ 5); nulo para las fracciones a descendentes; oDN1, BDN2 y LPLC3 por otra vía que el nombre; las entradas de más arriba en los bytes; el lector del rumbo; citas de lo «de memoria» (anillo de rumbo, HS y VS, LC10 y LC11, vía olfativa).
- Escape o aterrizaje (2026-10-12-003 y 004): ventaja de DBC3 sobre LSTM con entrenamiento largo o por etapas y esperas intermedias (en la 004 ninguno aprende con 400 pasadas); DBC3 en C y su paridad con torch; la líquida en este motivo; condiciones fuera de las entrenadas.
- Entrada por tipos (2026-10-12-005): líneas etiquetadas; fisiología de LPLC4 (la amplitud 0,6 del punto en LPLC2 es supuesto); otras sintonías y otros circuitos (LC6, LC9 → DNp09, LPLC1); DBC3 como lector con esta entrada; señal biológica; una segunda máquina.
- En criollo (2026-10-12-006): el inventario no se re-midió hoy (foto del 26 y 27-ago), incluido el cross de ESP32; ninguna placa figura en el inventario y un emulador de Espressif no se probó; el potencial de producto (bytes, latencia, energía en placa) es opinión, no medición.
- Brazo S (008): MultiCue con más semillas; un S que conserve Dale por neurona (este motivo no tiene aristas inhibitorias); SparseLTC completo como reservorio; la τ propia de DBC3 (el brazo F mide la `LiquidCell` de DualBrain); F con los mismos parámetros que A.
- Escape (010 a 016): la líquida nativa de SparseLTC (tau_gain); las 26 con estado complejo; las 26 con DBC3 como controlador; paridad numérica del numpy del escape contra el `step()` de C++; SL con varias semillas de entrenamiento cada una; la líquida plena sobre S; condiciones fuera de las entrenadas; la ventaja sobre SL con otro modelo de entrada; un controlador clásico entrenado como rival; la plena en Q15 sobre ESP32; reproducción en una segunda máquina; el modelo de entrada es de literatura, no medido.
- Review externo del pipeline. Silencio no es aprobación.

--- METODO PROMETEO ---
Máquina: brain-env para el escape (010 a 015), la Tabla 7, las salidas, los nulos, la 003, el inventario de ramas, el motivo de la 008, el catálogo (2026-10-12-002), escape o aterrizaje con DBC3 (2026-10-12-003), memoria dura (2026-10-12-004), entrada por tipos (2026-10-12-005) y la v2.0 (2026-10-12-007: PDF v1.0, json de la Tabla 7, grep de ramas, render y verificación en clon fresco), con torch CPU donde hizo falta; Actions x64 para el brazo S (008); sandbox de ClickUp para el instrumento de `swarm/` (007), para escribir los scripts del 010 al 015 y del 2026-10-12-002 al 005, y para la Tabla 5 de la 2026-10-12-007; lectura de código en brain-env y GitHub para la 016; ninguna corrida para la 2026-10-12-001 (diseño) ni para la 2026-10-12-006 (síntesis; lecturas en GitHub); ClickUp para la tarea y la mención a Tao (2026-10-12-007); ninguna corrida para la 2026-10-12-008 (diseño; clon de lectura en brain-env); brain-env (rutas de Zenodo, token y md5 de los PDF), ClickUp y GitHub (lecturas) para la 2026-10-12-009.
Artefactos: `docs/agents/respuestas/2026-10-12-009-tao-no-audito-pidio-confirmo-y-el-deposito-lo-espera.md` + https://app.clickup.com/90171457413/docs/2kza6fw5-21477
