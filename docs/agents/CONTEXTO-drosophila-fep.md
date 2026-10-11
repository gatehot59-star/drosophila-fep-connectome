# CONTEXTO VIVO · conectoma / paper / H4

**Última actualización:** 2026-10-11, madrugada (America/Buenos_Aires), con la respuesta 2026-10-11-007 (robótica: `swarm/` y la idea mejorada).
**Estado canónico:** `main`, con las respuestas del 10 y 11 de octubre. H4 auditado en `a4f5a8e9143173bf609eff430bcca3d5d8699c48`.
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
- **Siguen NO MEDIDOS:** SparseLTC→DBC3 sobre señal biológica, mapping ROI→FlyWire, null anatómico pareado y silenciamiento causal.
- **Robótica (respuesta 007):**
  - `swarm/` es el único robot de los repos y **no sale del conectoma**: 34 neuronas y 83 sinapsis escritas a mano con nombres de regiones de la mosca.
  - Con física de cuadricóptero X estándar, **el escape visual va hacia la amenaza en las 4 direcciones** (108/108 en la sensibilidad). Leer los motores con reflexión FL↔BR, FR↔BL lo da vuelta: 4/4 y 108/108 hacia afuera. Instrumento válido: reflejo físico 4/4 ALEJA y red nula 4/4 NEUTRO.
  - El test de `swarm/` no puede dar rojo (con los pesos en cero sale con 0) y la auditoría de `gen_swarm.py` devuelve `PASS` fijo con topologías mutadas.
  - Instrumento: `tools/swarm_lazo_cerrado.py` en la rama `titan/swarm-lazo-cerrado-2026-10-11`, sin PR.
  - **Idea mejorada (BEEC v2):** compilador de motivos certificados contra el nulo, interfaz por descendentes, cordón sintético con lazo de actitud, y entrenables sólo la compuerta, la memoria DBC3 y el readout. El falsador es el brazo S.
  - `docs/agents/CONTEXTO-motor.md` está vencido desde el 24-ago: dice que nadie linkeó DualBrain, y en la rama de materialización hay un ELF linkeado de 44.292 B (no flasheable) y un arnés de 512 pasos contra el oráculo numpy. El estado de robótica vive acá hasta reescribirlo.
  - **Espera decisión de Abraham:** aplicar el parche de lectura en `swarm/` y corregir el «Correcto» de su README; adoptar BEEC v2 como norte de la línea de robótica.

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

   Depositar en Zenodo lo hace Abraham.
4. **Abiertos para la v2:** NPC por sinapsis o null combinado de grado y neuropilo; ventana y tau de sel_post; Lin región por región; Betzel arista por arista; fila AN y décima clase de la Tabla 5.
5. **La 007:** con R = 10.000 para Holm; D2 con el nulo de región.
6. H4 estacionada.
7. **Robótica (respuesta 007 del 11-oct), en este orden:** arreglar el dron (parche de lectura, un test que afirme y giróscopo en vez de «altitud» en el haltere); primer motivo real, GF-01 → descendentes → dron; el brazo S, que no comparte archivos con lo anterior y puede correr en paralelo; edge en ESP32.

## Fuentes

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
- Robótica: hardware, la tabla descendente → orden, GF-01 compilado en Q15 y montado en el dron, el brazo S y cualquier medición fuera de distribución.
- Review externo del pipeline. Silencio no es aprobación.

--- METODO PROMETEO ---
Máquina: sandbox de ClickUp para el instrumento de `swarm/` (007); brain-env para la Tabla 7, las salidas, los nulos, la 003 y el inventario de ramas.
Artefactos: `docs/agents/respuestas/2026-10-11-007-mosca-a-robot-idea-mejorada-y-el-dron-que-escapa-hacia-la-amenaza.md` + https://app.clickup.com/90171457413/docs/2kza6fw5-21097
