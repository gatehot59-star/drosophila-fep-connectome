# CONTEXTO VIVO · conectoma / paper / H4

**Última actualización:** 2026-10-12, mañana (America/Buenos_Aires), con la respuesta 2026-10-12-006 (en criollo: qué tenemos, si tiene potencial y hacia dónde vamos; síntesis sin corrida nueva: la mosca sirve de mapa y de reflejo chico, no de cerebro entrenable). La 005 (entrada visual por tipo de neurona) dio NO PAGA: con lector entrenado sobre las 4 descendentes el cableado de la mosca nunca le gana a SL, pierde contra las sintonías barajadas si LPLC4 es muda y el rival clásico crudo le gana en 6 de 6; incluye el resumen de la 004 y la 005. La 004 mostró que ni DBC3 ni LSTM sostienen el estado de vuelo 90 pasos y que la máquina de estados les gana. La 003 corrió el primer acople SparseLTC → DBC3 (en el techo, empate con LSTM y con el barajado). La 002 armó el catálogo de circuitos (corregida por la 003 en LC9 y DNp10). La 001 fijó la arquitectura por etapas (diseño). La 016 respondió cómo operan las 26. La 015 firmó la 014 sólo para la semilla 0.
**Estado canónico:** `main`, con las respuestas del 10, 11 y 12 de octubre. H4 auditado en `a4f5a8e9143173bf609eff430bcca3d5d8699c48`.
**Base vigente del paper:** `docs/ERRATUM.md` (9 ítems) con anotaciones pinneadas a `17fc577`. **Zenodo tiene sólo la v1.0** (20-mar): la v2 con el erratum no está depositada.

## Mapa del repo (respuesta 2026-10-11-004)

- main tiene 182 archivos en `02da943` y hay 27 ramas además de main (la 006 corrigió los 180 archivos y las 28 ramas de la 004). La unión de todas las refs da 464 pares ruta-blob.
- **El expediente de agosto vive en ramas sin mergear:** las respuestas 063 a 124, 47 evidencias y unos 44 scripts. Lo esencial está en `titan/twohop-nulls`, contenida en `titan/auditoria-hipotesis-2026-10-01`, contenida en `titan/materializacion-h4-guard-2026-10-02`. Incluye:
  - el null anatómico;
  - LC6→GF;
  - sel_post;
  - los 39 nulos en GPU y el test global;
  - la auditoría de Tao;
  - Betzel.
- **Otras ramas con contenido propio:**
  - `titan/auditoria-integra-2026-08-25`: disputa del DOI y scripts de nulos;
  - `titan/initial-release`: manifest y logs de nulos;
  - `titan/paso-1-identidad-roi-2026-10-03`: H4 ROI.
- **Abiertos en GitHub:**
  - PR #1, #2, #3, #12, #25 y #26;
  - issues #4, #5 y #13 a #15.
- **`docs/SECCION-V2-DOS-SALTOS.md` de main es la versión anterior al null anatómico** (323× contra el null de grado). La de la rama dice que el 323× era co-localización: el spread cae a 2,4× y queda la depleción gustativa (10 contra 101,6, z = −78,9).
- En el PDF, la Tabla 7 es la de reciprocidad por circuito y la de RDI es la Tabla 8. El `reproduce_table7` del release inicial es de la trayectoria de RDI y no la reproduce.

## Veredicto operativo

- **Paper, reciprocidad:**
  - La Tabla 7 es reproducible: 8/8 con el pin `17fc577` (respuesta 003). El script está reconstruido en el PR #26, sin merge.
  - El nulo CP propio reproduce el del erratum: media de 194.890,4 contra 194.974,2, o sea 20,60× con 0/100.
  - **Con ese nulo, la caída de la reciprocidad hacia la salida motora queda explicada por el nulo:** el exceso es 4,30× / 3,67× / 5,55× con ≥1 y 5,11× / 9,57× / 3,94× con ≥5, sin orden. Pero el instrumento dio FAIL (control negativo de la prueba secundaria, 8/20 con CP y ≥1) y **no se firma**.
- **Quién controla las salidas (005 a 009):** el central pone el 60–73% de la entrada de las tres salidas; las descendentes, el 21–22% de la de las motoras; las ascendentes, el 16–20% de la de las neurosecretoras; el óptico, menos del 0,5%.
  - **Nulo fuerte (006**, etiquetas barajadas entre neuronas del mismo tamaño): se sostiene, con el central en ×1,5–2,3.
  - **Nulo de región (007**, además de la misma zona del cerebro): sólo las descendentes siguen mandando fuerte, → motoras ×3,69 / ×3,21 y → descendentes ×3,29 / ×2,61.
    - El dominio del central sobre descendentes y neurosecretoras era ubicación (×1,07 / ×1,01 y ×1,09 / ×1,03). Su plus propio va a las motoras (×1,31 / ×1,16), sobre todo a las de la boca.
    - Las ascendentes caen a azar en las tres salidas, lo sensorial queda por debajo de sus vecinas (×0,33 a ×0,62) y la proyección visual hacia las descendentes pasa a azar.
  - **Corrección múltiple de la 007 (008):** BY deja 31 de las 33 afirmaciones firmes y max-T deja 5: descendentes → descendentes, → motoras, → cuello y → antena, y óptico ▼ descendentes. El plus del central hacia las motoras aguanta FDR pero no FWER.
  - **Corrección múltiple de la 006 (009):** las 41 afirmaciones firmes aguantan BY, 34 aguantan Holm y 11 max-T. A la 006 le fallaba la ubicación, no la cantidad de tests.
  - **FWER con los dos nulos:** descendentes → descendentes, → motoras, → cuello y → antena, y óptico ▼ descendentes.
- **H4 fuerte: NO MEDIDA.** La búsqueda pública de ROI 2P está agotada (16/16 sin mapear, rama ROI). H4 débil queda refutada sólo en su alcance estrecho.

## Paper y Tabla 7 (respuestas 002 a 009 del 10-oct y 003 y 004 del 11-oct)

- **Script:** `tools/table7_reciprocity_by_class.py` en `titan/tabla7-reconstruida-2026-10-10`, PR #26.
- **Anotaciones:**
  - con las de marzo (`c03ad46`): L3 16/16 y Tabla 7 8/8;
  - con el pin `17fc577`: L3 10/16 por recambio de `root_id`, y Tabla 7 8/8 a un decimal, lo que confirma el «What has not changed» del erratum.
- **El 8,7% sensory→descending es doble redondeo:** 2.104/24.327 = 8,6488%, o sea 8,6.
- **Umbral ≥5:** 2.700.513 aristas y 13,98%, igual al ítem 5 del erratum.
  - intra-sensory 37,5; intra-motor 35,0 (80 aristas); intra-visual centrifugal 23,4; intra-optic 17,1;
  - sensory→central 13,8; sensory→descending 2,8; sensory→motor 1,3; optic→motor sin aristas.
- **Nulo por circuito y tendencia (003), `tools/table7_circuit_null.py`, en brain-env sin push:**
  - cruces con la 002 PASS en los dos umbrales; Tabla 7 8/8; nulo CP del erratum reproducido a 0,04%; conservación PASS;
  - con CP, la tendencia es EXPLICADO_POR_EL_NULO en los dos umbrales;
  - con CM no vale, porque el seudoconteo domina;
  - **veredicto de instrumento FAIL** por el control negativo.
- **Embudo de salida (004):** 1.485 neuronas (1,07%; descending, motor y endocrine) reciben el 2,37% de los cables. Lo que les llega tiene 13,19 / 9,83 / 3,58% de vuelta, contra 26,60% global. Descriptivo, sin nulo.
- **Control de las salidas:** 005 (`7e75cde`), 006 (`c99494f`), 007 (`f436f21`), 008 (`2093d57`) y 009 (`95e8d6c`), en la rama de la Tabla 7. Los números están en el veredicto operativo.
- **Espera decisión de Abraham:**
  - pasar el ítem 9 y el 8,6 a `docs/ERRATUM.md` y a `docs/PIVOTE-RECIPROCIDAD.md`;
  - consolidar en main el expediente de ramas (PR #1, #2, #3) y la SECCION-V2 corregida.
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
    - **Lectura:** con lector entrenado, en esta tarea, E2 va con lo clásico (regla de la 001). El cableado por tipos podría pagar como líneas etiquetadas (cada descendente con su umbral dispara una acción): NO MEDIDO. Si el reparto de la mosca fuera bueno para un lector así, LPLC4 tendría que responder al movimiento: hipótesis, no medida.
    - Instrumento: `tools/escape_aterrizaje/entrada_por_tipos.py` en `titan/entrada-por-tipos-2026-10-12` (md5 `e060c4bf…`, pre-registro `75ca27c`, logs `f7844be`, md5 4/4 en clon fresco), brain-env, 60,0 y 53,5 min en paralelo, sin PR.
  - `docs/agents/CONTEXTO-motor.md` está vencido desde el 24-ago: dice que nadie linkeó DualBrain, y en la rama de materialización hay un ELF linkeado de 44.292 B (no flasheable) y un arnés de 512 pasos contra el oráculo numpy. El estado de robótica vive acá hasta reescribirlo. Sus §1, §4 y §6.2 (el brazo W «nunca testeó» la hipótesis y el diseño W/S) quedan superados por la 008 y la 010 a la 015.
  - **Espera decisión de Abraham:** aplicar el parche de lectura en `swarm/` y corregir el «Correcto» de su README; adoptar BEEC v2 como norte de la línea de robótica; **en L2, τ líquida plena entrenada sobre el cableado fijo (1.378 parámetros, unos 5,5 KB en float32; costo en ESP32 NO MEDIDO), que reemplaza a la diagonal de la 012**, o probar antes la líquida nativa de SparseLTC (016); **adoptar la arquitectura por etapas con su regla de reparto, y sacar antimisiles del roadmap (2026-10-12-001)**; **tras la 004 el estado de vuelo quedó en lo clásico; tras la 005: probar líneas etiquetadas contra SL y T con la misma entrada por tipos, o dar por cerrado que en esa tarea E2 va con lo clásico**; **el orden de la 006: la v2 del paper (token de Zenodo), líneas etiquetadas en Actions y, si pagan, el reflejo en C99/Q15**.

## Próximos pasos

1. **Consolidar git:** el linaje de ramas a main (PR #1, #2, #3) o un PR sólo de documentos, y la SECCION-V2 posterior al null anatómico. Decide Abraham.
2. **Cerrar el 003:**
   - sacar el seudoconteo de la media del nulo o subir K;
   - explicar el 8/20 del control CP con ≥1;
   - volver a correr y firmar;
   - subir el script, los tests y los logs a la rama.
3. **v2 depositable:**
   - erratum, Tabla 7 con ≥5 y 8,6, reciprocidad como rango;
   - dos saltos post-null anatómico, LC6→GF y sel_post;
   - control de las salidas, con BY y lo que aguanta FWER marcado.

   Depositar en Zenodo lo hace Abraham: es una llamada de API con un token `deposit:write` (inventario §7 y §8).
4. **Abiertos para la v2:** NPC por sinapsis o null combinado de grado y neuropilo; ventana y tau de sel_post; Lin región por región; Betzel arista por arista; fila AN y décima clase de la Tabla 5.
5. **La 007:** con R = 10.000 para Holm; D2 con el nulo de región.
6. H4 estacionada.
7. **Robótica (015, 016 y 2026-10-12-001 a 006; orden propuesto en la 006, decide Abraham):** ~~el catálogo de circuitos~~ **hecho (002)**; ~~escape o aterrizaje según vuelo~~ **hecho (003), en el techo**; ~~memoria dura~~ **hecha (004), nadie aprende**; ~~entrada por tipos visuales~~ **hecha (005), NO PAGA**; **1) líneas etiquetadas** (cada descendente con su umbral dispara una acción) contra SL y T con la misma entrada, **en Actions** (repo público: gratis, 11,6× más rápido y VM limpia; instalar numpy con `setup-python`); **2) si pagan, el reflejo en C99/Q15** con paridad contra numpy, `.text` y latencia en Actions x64 y arm64, y tamaño para ESP32 con `xtensa-esp32-elf-gcc` del taller (ninguna placa figura en el inventario; un emulador de Espressif NO MEDIDO); **3) arreglar el dron** (parche de lectura, un test que afirme y giróscopo en vez de «altitud» en el haltere) y montarle el reflejo; **estacionado:** DBC3 contra LSTM con entrenamiento largo o por etapas (la máquina de estados ya gana); siguen abiertos: la líquida nativa de SparseLTC (tau_gain, 26 parámetros) en el escape contra su control; revisar LC9 → DNp09; el lector del rumbo (camino de EPG a descendentes); nulos para las fracciones del catálogo; DBC3 en C con el `dbc3_motor.h` reconstruido de brain-env y paridad contra el `DBC3Motor` de torch; el cordón nervioso en MANC o BANC para la etapa E5; en el escape, SL con varias semillas cada una y la plena sobre S, condiciones fuera de las entrenadas y el otro modelo de entrada.
8. **Brazo S (respuestas 008, 010 a 015):** MultiCue con 50 semillas para decidir la tendencia 0,42×; un S que conserve Dale por neurona en motivos con inhibición; reescribir `CONTEXTO-motor.md`; PR de `titan/brazo-s-recurrente-2026-10-11`, `titan/swarm-lazo-cerrado-2026-10-11`, `titan/escape-motivo-2026-10-11`, `titan/catalogo-circuitos-2026-10-12`, `titan/escape-aterrizaje-2026-10-12`, `titan/memoria-dura-2026-10-12` y `titan/entrada-por-tipos-2026-10-12`, y review.

## Fuentes

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
- `docs/ERRATUM.md` y `docs/PIVOTE-RECIPROCIDAD.md`
- `00-ENTORNOS-Y-CAPACIDADES.md` (raíz; foto medida el 26 y 27-ago; leído en `5405f03` para la 006).
- En `mojo-absoluto` `main` (`613bf49`): `include/mojo_abs/connectome_ltc.hpp` y `docs/adr/2026-10-01-sparseltc-dbc3-adapter.md`.
- `README.md` de `dualbrain` (`main`) y el Doc de ClickUp del 3-oct «Mojo Absoluto Compiler: DualBrain/DBC3, SparseLTC e hipótesis de desarrollo» (https://app.clickup.com/90171457413/docs/2kza6fw5-19197/2kza6fw5-21757).
- En brain-env: `/workspace/dbc3_lib.py` (md5 `39566d9a…`, `DBC3Motor` del notebook DBC3-v3) y `/workspace/dbc3_motor.h` (md5 `6199c452…`, reconstrucción en C sin pesos).
- Literatura verificada en la 002: Ache 2019 (Nat Neurosci, aterrizaje), Braun 2024 (Nature, redes de descendentes), Sapkal 2024 (Nature, oDN1 y BDN2), Simpson 2023 (Curr Opin Neurobiol, revisión de descendentes).
- Literatura verificada en la 005: von Reyn 2017 (Neuron, LC4 velocidad), Ache 2019 (Curr Biol, LPLC2 tamaño y suma en el GF), Klapoetke 2017 (Nature, LPLC2 ultraselectiva), Kim 2023 (Curr Biol, LPLC2 y el punto que se traslada), Dombrovski 2025 (Nature, entradas visuales del GF); LPLC4 sin fisiología encontrada.
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
Máquina: brain-env para el escape (010 a 015), la Tabla 7, las salidas, los nulos, la 003, el inventario de ramas, el motivo de la 008, el catálogo (2026-10-12-002), escape o aterrizaje con DBC3 (2026-10-12-003), memoria dura (2026-10-12-004) y entrada por tipos (2026-10-12-005), con torch CPU; Actions x64 para el brazo S (008); sandbox de ClickUp para el instrumento de `swarm/` (007) y para escribir los scripts del 010 al 015 y del 2026-10-12-002 al 005; lectura de código en brain-env y GitHub para la 016; ninguna corrida para la 2026-10-12-001 (diseño) ni para la 2026-10-12-006 (síntesis; lecturas en GitHub).
Artefactos: `docs/agents/respuestas/2026-10-12-006-en-criollo-la-mosca-sirve-de-mapa-y-de-reflejo-chico-no-de-cerebro-entrenable.md` + https://app.clickup.com/90171457413/docs/2kza6fw5-21417
