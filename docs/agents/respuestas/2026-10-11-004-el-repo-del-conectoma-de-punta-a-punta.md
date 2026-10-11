# 2026-10-11-004 · El repo del conectoma de punta a punta: qué está resuelto, qué vive fuera de main y cómo seguir

**Fecha:** 2026-10-11, madrugada (America/Buenos_Aires).

## 1. Pedido

> «te decía que existe un repositorio distinto al de mojo absoluto donde ya había trabajado con el conectoma y se había resuelto bastante, inclusive se generó la fe de erratas del paper. revisá ese git, analizalo de punta a punta y verás que hay información suficiente para continuar»

El repo es `gatehot59-star/drosophila-fep-connectome`, público («Companion code and erratum to Mendieta (2026a)»). Es el mismo donde trabajé el 10 y 11 de octubre. Lo que no había leído era todo lo que vive **fuera de main**.

## 2. Herramientas

- **brain-env (`build.run`):** fetch de las 28 ramas e inventario por blob. El script es `/workspace/repo_inv.py` y la salida `/workspace/repo_inventory_2026-10-11.json`.
- **12 workers de lectura con GitHub**, sólo lectura, uno por partición.
- **Sandbox:** para juntar los registros y contarlos.
- **GitHub** para este commit y **ClickUp** para el Doc.
- Cero Kaggle. No escribí en ninguna rama ajena.

## 3. Qué se midió

### 3.1 Forma del repo (inventario en brain-env)

**main:** 180 archivos y 84 respuestas (64 de agosto, 20 de octubre).

**Fuera de main:** 28 ramas, con 273 rutas (282 versiones, 2,2 MB): 79 respuestas, 52 evidencias, unos 44 scripts y herramientas, logs y docs.

**El grueso está en un solo linaje:**

- `titan/twohop-nulls` está contenida en `titan/auditoria-hipotesis-2026-10-01`, que está contenida en `titan/materializacion-h4-guard-2026-10-02`.
- Esta última tiene 226 commits que main no tiene y 158 archivos nuevos.

**Aparte de ese linaje:**

| Rama | Commits fuera de main | Qué trae |
|---|---|---|
| `titan/auditoria-integra-2026-08-25` | 118 | disputa del DOI y 5 scripts de nulos |
| `titan/initial-release` | 14 | manifest y logs de nulos 19/21/40 |
| `titan/paso-1-identidad-roi-2026-10-03` | 24 | H4, identidad de ROI |

Se suman research de patentes, DBC3 staging y ramas chicas de H4 que ya tienen par en main.

**GitHub:**

- 21 PR: 6 abiertos, 5 cerrados sin merge y 10 mergeados. Los abiertos son #1 release inicial, #2 null anatómico, #3 auditoría TITAN, #12 H4 temporal, #25 DBC3 y #26 Tabla 7.
- 5 issues, todos abiertos: #4 Betzel/PLOS, #5 regla de tres factores, #13 a #15 gates de H4.

### 3.2 Cobertura de la lectura

Se leyeron completos **349 registros**:

- **main, 123 de 180 archivos:** todos los docs, contextos e índices, y las 84 respuestas. La 032-handoff quedó fuera del reparto y la leí yo.
- **Fuera de main, 200 de 273 rutas:** las respuestas del linaje, de la auditoría íntegra y de ROI; las 47 evidencias de agosto; los 44 scripts del linaje; el release inicial; research; DBC3.
- **GitHub:** 5 issues y 21 PR.

**Sin leer:**

- En main, los tests, workflows y resultados de H4 y 19 de los 21 archivos de `audit/bicamerality`.
- Fuera de main, versiones de rama de archivos chicos de H4: resultados partidos, workflows, 3 JSON de ROI y 8 respuestas H4 de ramas cortas que tienen par en main.

El índice de los 349 registros va adjunto al Doc como CSV (md5 `8c321994e42bef21c1deee83d431513a`).

### 3.3 Lo que el repo deja resuelto

**Paper 1 y erratum:**

- **Zenodo tiene sólo la v1.0** (20-mar, DOI 10.5281/zenodo.19136948). La disputa del DOI se cerró a favor de esa v1.0 pública (`titan/auditoria-integra-2026-08-25`, respuesta 2026-09-23-006).
- **La v2 con el erratum nunca se depositó** (evidencia 2026-08-26-115; informe maestro del 2-oct).
- **`docs/ERRATUM.md` en main tiene 9 ítems:**
  - densidad 0,0074 a 0,000785197, por overflow int32;
  - acceso motor corregido: 4 clases enriquecidas, 4 depletadas y 1 en expectativa; la clase AN no se puede reproducir;
  - el 36× se retira y la reciprocidad pasa a reportarse como rango contra CP (20,59×, 0/40) y MS (47,27×);
  - el 1.559× se retira;
  - con umbral ≥5 la reciprocidad global es 13,98%;
  - correcciones de conteos, tau y modelos;
  - anotaciones fijadas a `17fc577`;
  - el verificador tenía el mismo bug que lo verificado.
- **En el PDF, la Tabla 7 es la de reciprocidad por circuito y la de RDI es la Tabla 8** (respuesta 2026-08-23-007).
- **El `reproduce_table7` del release inicial reproduce la trayectoria de RDI, no la Tabla 7.** Tampoco la consigue: da 0,0043 … 0,7842 contra 0,6869 … 0,8328 publicados. Coincide con el pendiente del erratum «Table 8 no reproducible».

**Resultados que sobreviven controles** (casi todos fuera de main):

- **Null anatómico**, que conserva pares de neuropilos (aproximación NPC; respuesta 063): el spread de 323× del acceso motor a dos saltos cae a 2,4× y se invierten signos. Queda la depleción gustativa, 10 contra 101,6 ± 1,2 (z = −78,9), y la mecanosensorial.
- **LC6 → Giant Fiber:** 0 contra 17,2 ± 3,1 con el null anatómico, z = −5,61, 40/40 (respuesta 065, `docs/BIBLIOTECA-01-giant-fiber.md`).
- **Selectividad post-estímulo `sel_post`:** 4,3287, contra 1,1896 ± 0,0173 en el nulo de topología (z = +181) y 1,7983 ± 0,401 en el de signo con Dale (z = +6,31), 0/40 (respuestas 071 y 073).
- **Circuito de plasticidad contra CP:** KC→MBON 7,81×, DAN→KC 8,71×, KC→KC 7,26×, 0/40.
- **Control de las salidas** (10-oct, en main): descendentes → motoras, → descendentes, → cuello y → antena, y óptico ▼ descendentes aguantan el nulo de región y la corrección FWER.
- **Betzel** valida N, M, Mw y la densidad corregida (respuestas 080 y 081).

**Refutado o retirado:**

- el 36× (overflow) y el 1.559×;
- la jerarquía de 323×, que era co-localización;
- la tabla de ruteo como descubrimiento propio (ya había prior art);
- la entrada AMMC directa al GF;
- el efecto temporal global: con los 39 nulos en GPU, S_real = 239 contra 183,1 y p = 0,25 (respuesta 104);
- la ventaja de tau compleja (p = 0,60);
- la analogía del 96% fijo (H3, en la auditoría de hipótesis del 1-oct);
- H4 débil, en su alcance estrecho.

La auditoría de Tao al release dio 62/100, con 13 hallazgos aceptados (respuestas 072 y 073).

### 3.4 Lo que main hoy muestra mal

1. **La sección de dos saltos está vieja.** `docs/SECCION-V2-DOS-SALTOS.md` de main es la versión anterior al null anatómico: la de la respuesta 062, con el 323× contra el null de grado. La versión de la rama, reescrita después de la 063, dice que ese 323× era co-localización.
2. **El expediente que sostiene a main está en ramas.** Main no tiene las respuestas 063 a 124, la evidencia de agosto, la auditoría íntegra ni la disputa del DOI.
3. **El README mezcla dos métricas.** Agrupa la dinámica como resultado negativo y a la vez cita el RDI que sobrevive al null de grado más bloque (z = 197). El test global de los 39 nulos (p = 0,25) es de otra métrica. Hay que separarlas.

### 3.5 Lo que dio la prueba que estaba corriendo (003)

Verbatim de `results/table7_circuit_null_2026-10-11/run.log` en brain-env, sin el sello de tiempo inicial:

```
  TENDENCIA_PRINCIPAL CM delta=log(rho1/rho3)=3.0546 IC95=[2.4612, 3.9103] p_mas=0.0005 p_menos=1.0000 B=2000 rho=578.57x/252.42x/1358.05x ordenado=False -> PARCIAL_SIN_ORDEN
  CONTROL_NEGATIVO CM falsos=20 principal: rechazos=0 esperado=2.00 tope=6.00 | ensemble: rechazos=2 esperado=1.98 tope=5.94 -> PASS
  TENDENCIA_PRINCIPAL CP delta=log(rho1/rho3)=-0.2026 IC95=[-0.8201, 0.6345] p_mas=0.6767 p_menos=0.3238 B=2000 rho=4.30x/3.67x/5.55x ordenado=False -> EXPLICADO_POR_EL_NULO
  CONTROL_NEGATIVO CP falsos=20 principal: rechazos=0 esperado=2.00 tope=6.00 | ensemble: rechazos=8 esperado=1.98 tope=5.94 -> FAIL
CRUCE_INTERNO umbral=1 PASS: reciprocal_mask de la 002 y el conteo por sort coinciden en el eje
CRUCE_CP40 PASS media_CP=194890.4 erratum=194974.2 dif_rel=0.00043 ratio=20.60x n_ge=0 (erratum: 20.59x, 0/40)
  TENDENCIA_PRINCIPAL CM delta=log(rho1/rho3)=5.1003 IC95=[3.8122, 7.7194] p_mas=0.0005 p_menos=1.0000 B=2000 rho=880.96x/461.47x/219.02x ordenado=True -> MAS_ALLA_DEL_NULO
  CONTROL_NEGATIVO CM falsos=20 principal: rechazos=0 esperado=2.00 tope=6.00 | ensemble: rechazos=1 esperado=1.98 tope=5.94 -> PASS
  TENDENCIA_PRINCIPAL CP delta=log(rho1/rho3)=0.4968 IC95=[-0.7549, 3.0829] p_mas=0.1914 p_menos=0.8091 B=2000 rho=5.11x/9.57x/3.94x ordenado=False -> EXPLICADO_POR_EL_NULO
  CONTROL_NEGATIVO CP falsos=20 principal: rechazos=6 esperado=2.00 tope=6.00 | ensemble: rechazos=2 esperado=1.98 tope=5.94 -> PASS
CRUCE_INTERNO umbral=5 PASS: reciprocal_mask de la 002 y el conteo por sort coinciden en el eje
CHEQUEO CONSERVACION PASS mal_grado=0 mal_bloque=0
CHEQUEO CONTROL_NEGATIVO FAIL todos los umbrales y nulos
CHEQUEO CRUCE_002_umbral_1 PASS clases_iguales=True misma_base=True aristas_iguales=True reciprocas_iguales=True
CHEQUEO CRUCE_002_umbral_5 PASS clases_iguales=True misma_base=True aristas_iguales=True reciprocas_iguales=True
CHEQUEO CRUCE_CP40 PASS media_CP=194890.4 erratum=194974.2 dif_rel=0.00043 ratio=20.60x n_ge=0
CHEQUEO CRUCE_TABLA7 PASS tabla7=8/8 L3_marzo_exactas=10/16
CHEQUEO K_MINIMO PASS K=100 minimo=40
VEREDICTO_TENDENCIA umbral=1 principal: CM=PARCIAL_SIN_ORDEN CP=EXPLICADO_POR_EL_NULO | ensemble: CM=PARCIAL_SIN_ORDEN CP=EXPLICADO_POR_EL_NULO
VEREDICTO_TENDENCIA umbral=5 principal: CM=MAS_ALLA_DEL_NULO CP=EXPLICADO_POR_EL_NULO | ensemble: CM=MAS_ALLA_DEL_NULO CP=EXPLICADO_POR_EL_NULO
[ 2288.2s] VEREDICTO_INSTRUMENTO=FAIL
[ 2288.2s] FIN_CIRCUIT_NULL
EXIT_RUN=0
```

**Lectura:**

- **Mi nulo CP reproduce el del erratum:** media de 194.890,4 contra 194.974,2 (0,04%), 20,60×, ningún nulo por encima del observado.
- **Con el nulo del erratum, la caída hacia la salida queda explicada por el nulo** en los dos umbrales. El exceso sobre el nulo es 4,30× / 3,67× / 5,55× con ≥1 y 5,11× / 9,57× / 3,94× con ≥5, sin orden. La reciprocidad baja hacia la salida porque entre esas clases hay menos cables de vuelta, no porque el emparejamiento sea menos específico.
- **El instrumento dio FAIL y no se firma:**
  - el control negativo de la prueba secundaria rechazó 8 de 20 grafos falsos con CP y ≥1, contra un tope de 5,94;
  - con CP y ≥5, la prueba principal rechazó 6 de 20, justo el tope;
  - con el nulo de sólo grado (CM) cada nulo tiene casi cero recíprocas en sensory→motor, así que el seudoconteo domina y el δ de CM no vale.

**Errores míos:**

- El diseño no previó medias de nulo menores que el seudoconteo.
- El `EXIT_RUN=0` del lanzador no es confiable: con FAIL el script sale con 1.
- Antes de firmar hay que corregir las dos cosas.

## 4. Cómo seguir, en orden

1. **Consolidar git (decide Abraham).** Llevar a main el linaje de ramas (PR #1, #2 y #3). Si no se mergea, abrir un PR que sólo agregue las respuestas, la evidencia y la SECCION-V2 corregida. Sin eso, main contradice al expediente.
2. **Cerrar el 003.** Sacar el seudoconteo de la media del nulo (o subir K), entender por qué el control CP con ≥1 rechaza 8 de 20 y volver a correr. Si se confirma, el pivote cambia a: «la reciprocidad cae hacia la salida porque hay menos vuelta entre clases; por emparejamiento, el exceso es plano».
3. **Armar la v2 depositable:**
   - el erratum;
   - la Tabla 7 con ≥5 y el 8,6;
   - la reciprocidad como rango;
   - los dos saltos después del null anatómico;
   - LC6→GF y sel_post;
   - el control de las salidas.

   Depositar en Zenodo lo hace Abraham.
4. **Mediciones que siguen abiertas para la v2:**
   - NPC por sinapsis o null combinado de grado y neuropilo;
   - ventana y tau de sel_post;
   - Lin región por región;
   - Betzel arista por arista;
   - la fila AN y la décima clase de la Tabla 5.
5. **H4 queda estacionada:** la búsqueda pública de ROI 2P está agotada (16 de 16 sin mapear).

## 5. Archivos

- Este archivo y `docs/agents/CONTEXTO-drosophila-fep.md` actualizado, en este mismo commit.
- El índice de los 349 registros, como CSV adjunto al Doc. El JSONL completo y los 12 coverage quedan en el sandbox de esta sesión.
- El inventario por blob, en brain-env: `/workspace/repo_inventory_2026-10-11.json`.
- El script, los tests y los logs del 003 siguen en brain-env, sin push: herramienta md5 `2796d836…`, tests `9b2453d9…`, tests.log `d84a2e85…`.

## 6. NO MEDIDO

- 57 archivos de main y 73 rutas fuera de main sin leer (detalle en 3.2).
- Las dos SECCION-V2 no se compararon línea por línea. La conclusión se apoya en sus contenidos leídos por separado.
- Los resúmenes son de workers. Los números salen de sus registros y no los recomputé uno por uno.
- No se re-midió ningún resultado de las ramas. Este análisis dice qué está escrito y con qué evidencia, no lo vuelve a correr.
- El 003 no está firmado: FAIL de instrumento.

--- METODO PROMETEO ---
Máquina: brain-env (inventario de ramas y corrida del 003); GitHub de sólo lectura (12 workers); sandbox (consolidación).
Artefactos: `docs/agents/respuestas/2026-10-11-004-el-repo-del-conectoma-de-punta-a-punta.md` + Doc de ClickUp con el CSV.
