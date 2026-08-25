# EVIDENCIA CRUDA · los siete NO MEDIDO, uno por uno

**Fecha:** 2026-08-25 11:05 (America/Buenos_Aires)
**Instrumento:** `gateway build.run` sobre `brain-env`, 14 corridas · integración GitHub · `search_web` × 2
**Datos:** `/workspace/connectivity.parquet`, `/workspace/annotations.tsv`. `/workspace` solo leído salvo `/workspace/ab_models`.

---

## ÍTEM 2 · comparar los dos modelos MIDIENDO

**Instrumento:** `src/ab_cascade_vs_linear.py`, bajado del raw de GitHub a `/workspace/ab_models` y verificado por md5 de los dos lados (`d3fa410bd70a7d5920c136cf471a24b0`).

### Salida cruda, verbatim y sin recortar

```
=== AB CASCADE vs LINEAR  ---  item 2 de la deuda declarada ===
parquet = /workspace/connectivity.parquet
annot   = /workspace/annotations.tsv
N=138639  E=15091983  Mw=54492922
G1 los tres conteos coinciden con Betzel 2026 y con el Paper 1: OK
G2 neuronas con salidas MIXTAS en el grafo real = 0
G3 CONTROL NEGATIVO, shuffle por arista -> mixtas = 134547
G3 el guard de Dale PUEDE dar rojo: OK
  pob visual           n=10855  descartadas=536
  pob olfactory        n=2279  descartadas=3
  pob mechanosensory   n=2656  descartadas=12
  pob gustatory        n=408  descartadas=0
  pob motor            n=110  descartadas=0

=== BRAZO LINEAR  (Paper 1: CON signo, CON transitorio) ===
  visual           peak=0.140174  post_sum=3.555585
  olfactory        peak=0.007077  post_sum=0.326817
  mechanosensory   peak=1.566994  post_sum=32.154654
  gustatory        peak=0.304953  post_sum=7.881427

=== BRAZO CASCADE  (Betzel: SIN signo, SIN transitorio) ===
  visual           motoras alcanzadas = 105.100 +/- 1.446  [102,107]
  olfactory        motoras alcanzadas = 105.500 +/- 1.204  [104,109]
  mechanosensory   motoras alcanzadas = 105.650 +/- 1.352  [103,109]
  gustatory        motoras alcanzadas = 106.050 +/- 1.244  [104,108]

=== EL VEREDICTO: los dos modelos ordenan igual? ===
  orden LINEAR  por post-estimulo : mechanosensory > gustatory > visual > olfactory
  orden CASCADE por motoras       : gustatory > mechanosensory > olfactory > visual
  ORDEN IDENTICO = False
  spearman rho = 0.6000   (n=4: el p NO es interpretable y no se usa)
  orden LINEAR por PICO           : mechanosensory > gustatory > visual > olfactory
  pico y post-estimulo coinciden  = True

DONE in 417.1 s -> /workspace/ab_models/ab_models_out.json
```

```
exit real medido con subprocess: JSON existe = True
"identical_post_vs_cascade": false
"identical_peak_vs_post": true
"spearman_rho": 0.6000000000000001
```

### 🟢 Lo que sale a favor

**Los dos modelos NO ordenan igual** (`rho = 0,60`, no 1,0). Y hay algo más fuerte que el desorden:

> **El modelo de cascada SATURA.** Las cuatro clases alcanzan **105,1 · 105,5 · 105,65 · 106,05** de **110** motoras. **Spread entre extremos: 1,009×.**

**Sobre acceso motor, el modelo sin signo no discrimina nada:** su `sd` es de 1,2 a 1,4 y las cuatro medias caben dentro de un desvío. Es exactamente el **modo de falla 2** que este repo tiene documentado — un estadístico pegado al techo — pero esta vez del lado del modelo ajeno.

**En el brazo lineal el mismo contraste da 98,4×** entre mechanosensorial (32,15) y olfatoria (0,33). **La diferencia no es de sensibilidad: es que un modelo puede separar las modalidades y el otro no.**

### 🔴 Y lo que sale EN CONTRA, que no buscaba

```
  orden LINEAR por PICO           : mechanosensory > gustatory > visual > olfactory
  orden LINEAR por POST-ESTIMULO  : mechanosensory > gustatory > visual > olfactory
  pico y post-estimulo coinciden  = True
```

> **Para ESTE estadístico — acceso motor por modalidad — el pico y el post-estímulo dan EL MISMO ORDEN.**

**El `sel_post` = 4,3287 sigue en pie**, porque mide otra cosa: **selectividad temporal entre perfiles de *looming* dentro del circuito de escape**, no ranking de modalidades. **Pero el claim general «el pico es lo único que este circuito no discrimina» queda ANGOSTADO a ese circuito y a esa métrica**, y así hay que escribirlo.

**Apareció corriendo, no releyendo.** Es el único modo en que aparece.

---

## ⚠️ EL FALSO ROJO, y va documentado porque es el más peligroso del turno

**Primera corrida, el guard G1 abortó:**

```
N=138639  E=15091983  Mw=54492920
GUARD_FAILED Mw esperado 54492922, medido 54492920
```

**Dos sinapsis de menos.** Antes de escribir «discrepancia con Betzel», lo medí:

```
dtype_original int64
SUMA_int64        54492922
SUMA_float64      54492922.0
SUMA_float32      54492920.0
PUBLICADO_BETZEL  54492922
DIFF_int64        0
DIFF_float32      -2.0
CONTROL: max 2405  min 1  n 15091983
```

> **No era una discrepancia de datos: era mi propio cast a `float32` perdiendo precisión sobre 15.091.983 sumas.** En `int64` el número es **exacto**.

**Es el espejo del falso positivo de esta mañana** (un `returncode 2` correcto por archivo inexistente): acá un **guard que da ROJO por el motivo equivocado**. La regla que sale: **un guard que se dispara obliga a medir POR QUÉ se disparó, no a creerle.** Corregido a `int64`, guard en verde, y el número publicado confirmado.

---

## ÍTEM 3 · ¿mismo archivo o solo mismo snapshot? · **CERRADO CON DATOS**

**Betzel SÍ publica sus datos.** Su Data Availability, verbatim:

> *«all data used to reproduce the results reported in the main text and in the Supporting Information are available publicly at https://codex.flywire.ai/?dataset=fafb . **Postprocessed data are also available here https://doi.org/10.5281/zenodo.18555170**»*

```
HTTP=200
TITULO: Flywire Female Adult Fly Brain Drosophila Derivatives
FECHA:  2026-02-09
AUTORES: Betzel, Richard
ARCHIVOS: 3
   coordinates.mat   bytes= 1885835     md5:c55f622a86be58ea5c5b7c9fcb9ee24a
   connectome.mat    bytes= 106587606   md5:a5f4bb8f12c12775a0806457e66cb148
   annotations.mat   bytes= 574256      md5:0d2be44229cd13bc2544e972397503ed
```

**Estado correcto del ítem, con los tres estados separados:**

- 🟢 **Mismo snapshot, con los tres conteos verificados por instrumento:** `N`, `E` y **`Mw` exacto al entero** (54.492.922 = 54.492.922, `diff 0`).
- 🟡 **Mismo ARCHIVO: sigue NO MEDIDO.** Su `connectome.mat` (106.587.606 B) está en formato MATLAB y el nuestro es parquet (100.804.642 B): **los md5 no son comparables por construcción**. La descarga quedó a mitad (33.255.424 B de 106.587.606) y **la comparación arista por arista no se corrió**.
- 🟢 **Pero el ítem ya no es una inferencia:** el md5 de su fuente **existe y está publicado**, así que la comparación es **ejecutable por cualquiera**, que era el punto.

---

## ÍTEM 4 · la fila `MS+CP (N=100)` de la Tabla 11 · **DEFECTO REAL, y no es el que sospechaba**

**Sospechaba que la Tabla 11 contradecía al paper. Es al revés: la Tabla 11 es consistente con el paper, y el REPO es el que no.**

**El PDF publicado, §2.4, verbatim:**

> *«Maslov–Sneppen (MS). Preserves degree distribution; destroys modularity. Factor 3×, rate 100%. **N=100 for static analyses; N=5 for temporal.** The 100 controls were generated in **3 parallel batches (34+33+33)** with independent seeds»* · *«Community-Preserving (CP)… N=5–10»*

Y su Table 3 dice literalmente *«Net RDI modality → motor (**N=100 MS controls**)»*.

**El código del repo, medido:**

```
=== src/nulls40_kaggle.py ===
  L1:   # TITAN v5.4 - 40 nulls Maslov-Sneppen sobre el conectoma real de Drosophila
  L120: NNULL = 40
  L121: SWF = 3
=== src/cp40.py ===
  L1:   # TITAN v5.4 - 40 nulls COMMUNITY-PRESERVING sobre la capa estructural.
  L177: NNULL = 40
=== docs/METHODS.md ===
  L90:  Double-edge swap, 3E target swaps per null, 40 nulls, seeds 4200 + 17i for i in 0..39.
  L96:  in-degree of all 138,639 nodes: 0 mismatches in 40 of 40 nulls
=== README.md ===
  L39:  `p = 0.0244` is the permutation floor with n = 40
```

| Qué | Paper publicado | Repo |
|---|---|---|
| MS estático | **N = 100** (en 3 lotes de 34+33+33) | **NNULL = 40** |
| CP estático | **N = 5–10** | **NNULL = 40** |
| Piso de `p` | derivado de 100 | **0,0244**, derivado de 40 |

> **El repo NO reproduce los conteos de nulls que declara el paper.** No es que la Tabla 11 esté mal: es que **el código commiteado no es el que produjo las tablas publicadas.**

**Es el modo de falla 5, sexta reincidencia**, y es la **versión profunda del hallazgo 1 de Tachi** («la reproducción está rota»): él lo vio en las rutas absolutas de los dos `.mjs`; el agujero real es que **los `N` no coinciden**. **El erratum no cubre esto.**

---

## ÍTEM 1 · suplementarios y `Response_to_Reviewers` · **CERRADO**

**El peer review completo viene EMBEBIDO en el XML que ya tenía**, desde el offset 108.701:

```
PEER_REVIEW_EMBEBIDO = True en offset 108701
chars_de_peer_review 28034
  null               = 0
  randomiz           = 0
  surrogate          = 0
  signed             = 1     <- el unico acierto es "assigned"
  inhibitory         = 0
  motor neuron       = 0
  limitation         = 0
  major              = 3
  minor              = 3
  reject             = 0
  accept             = 8
```

**Los tres revisores, verbatim:**

> **Revisor #1:** *«This is a nicely done paper, I enjoyed reading it. The model is elegant and insightful. I think all my comments can be considered minor, there are just many of them!»*

> **Revisor #2:** *«I congratulate the authors on technically sound work with a very interesting dataset… I have no major concerns but offer a list of minor comments.»*

> **Revisor #3:** *«several aspects need clarification and improvement before publication: 1. Model justification… 2. **Validation**: It would strengthen the paper to compare the simulation results to experimental data… 3. **Robustness**: A sensitivity analysis or discussion of parameter effects would help show whether the findings are stable.»*

Y a la pregunta del formulario *«¿se hizo el análisis estadístico de forma apropiada y rigurosa?»*: **Revisor #1 Yes · Revisor #2 Yes · Revisor #3 No.**

### La lectura, con los dos filos, porque tiene dos

- 🟢 **A favor:** **ningún revisor pidió un null que destruya topología, ni signo, ni vía motora.** Cero menciones de `null`, `randomiz`, `surrogate`, `inhibitory`, `motor neuron` en 28.034 caracteres de revisión. **El nicho está libre y no es table stakes.**
- 🔴 **En contra, y hay que decirlo:** si **tres** revisores de un paper de propagación de señal sobre este conectoma **no pidieron** el null estructural, entonces **el null no es la vara que el campo usa hoy**. Eso **debilita «el null es el producto» como argumento de venta**, aunque lo refuerce como argumento de **novedad**. Son dos cosas distintas.
- 🟡 **Lo que SÍ pidió el Revisor #3 y este proyecto tampoco tiene:** **validación contra datos experimentales** y **análisis de sensibilidad de parámetros**. **Eso sí es la vara, y este repo está igual de descubierto ahí.**

**Y las 19 captions, medidas:** `motor` 0 · `descending` 0 · `effector` 0 · `efferent` 0 · `neurotransmitter` 7 · `signed` como palabra completa **0** (los 2 aciertos por substring eran `assigned`). **NO se abrieron los tres archivos de datos suplementarios** (`.s001` a `.s011`), solo sus captions.

---

## ÍTEM 5 · Rojas y Eon, auditados técnicamente · **DOS HALLAZGOS NUEVOS**

### 🔴 A. El repo público de Eon NO contiene la mosca 3D

```
RAIZ de eonsystemspbc/fly-brain:
  .gitattributes 66 | .gitignore 452 | README.md 16926
  environment-brian2genn.yml 270 | environment.yml 382 | main.py 7924
  code/ | data/ | scripts/
```

**Su `README` describe un BANCO DE PRUEBAS de simuladores LIF:** Brian2, Brian2CUDA, PyTorch, NEST GPU, GeNN, Brian2GeNN. Las manipulaciones son *«activation»* y *«silencing»* de neuronas arbitrarias. **Cero MuJoCo. Cero cuerpo. Cero comportamiento.**

> **La demo de los +120M de impresiones no es reproducible desde su repo público.** Lo público es un benchmark de simuladores sobre el modelo de **Shiu et al. (2024)**, que **el Paper 1 ya cita**.

**Y es el mismo patrón que Tachi nos marcó a nosotros:** publicar algo distinto de lo que se anuncia. **La diferencia es de escala de la promesa, no de tipo.**

### 🔴 B. El repo de Rojas Aliaga DERIVA del de Eon, y no lo cita

```
code/ de EON                        code/ de ROJAS
  benchmark.py            19369      benchmark.py            10972
  compare_backend_to_brian2.py 12773   --
  compare_ground_truth.py  9425       --
  compare_spike_outputs.py 10712      --
  paper-phil-drosophila/   (dir)     paper-phil-drosophila/   (dir)   <---
  run_brian2_cuda.py      21114      run_brian2_cuda.py      18322
  run_brian2_genn.py      18664       --
  run_genn.py             23109       --
  run_nestgpu.py          23541      run_nestgpu.py          15399
  run_pytorch.py          22859      run_pytorch.py          19180
```

> **Los cinco archivos de Rojas son un subconjunto de los diez de Eon, con los mismos nombres, incluido el directorio `paper-phil-drosophila`.** `phil` = **Philip Shiu**, senior scientist de Eon. **Ese nombre de directorio es un artefacto específico de Eon.**

Sus **Acknowledgments** citan FlyWire, NeuroMechFly, MuJoCo y Shiu et al. **A Eon Systems no.** Los tamaños difieren, así que es una versión anterior o modificada, **no una copia byte-idéntica** — y eso queda declarado, no afirmado como plagio.

### Y sus números se contradicen, medido

| Fuente | Neuronas | Sinapsis / aristas |
|---|---|---|
| Abstract en Zenodo | **139.255** | **54,5 millones de sinapsis** |
| README de su repo | **138.639** | **15.091.983 aristas dirigidas** |

> **Está mezclando sinapsis con conexiones**, que es exactamente el **defecto de redacción número 1 del propio Paper 1** («E = 15,091,983 synapses» en el Abstract contra «connections» en el §2.1). **El mismo error, en dos papers distintos, sobre el mismo dataset.** Eso dice algo sobre el dataset, no sobre los autores.

**Y un detalle de forma:** su `demo.mp4` pesa **133 bytes**. No es un video: es un puntero de LFS o un stub. La demo que el README muestra **no está en el repo**.

---

## ÍTEM 7 · `CONTEXTO-motor.md` · **ABIERTO, séptimo turno**

**Leído completo. Y contesta el hallazgo más grave de Tachi:**

> **El generador de C99 es `esp32c.py`, y está en la lista de los 6 `.py` que siguen FUERA de git** (`§6` ítem 9: `brazo_w.py`, `n21.py`, **`esp32c.py`**, `tres_brazos.py`, `nulls19b.py`, `paper_db.py`, 169.586 B en total).

**No falta escribir el C: falta commitear el generador.** El `.c` es **derivado**, y la política del repo es no commitear derivados. **La tarea correcta es subir `esp32c.py`**, no escribir C a mano. Eso cambia el ítem 5b del plan.

**Y su núcleo NO está vencido:** los dos resultados más fuertes de la línea están medidos y en git.

```
ABLACION DEL GATE (DualBrain vs DualNoGate) - iso-run, iso-arquitectura, 10 semillas
  Gated     con_gate=0.000236  sin_gate=0.025539  AYUDA 108.11x  p=1.56e-105
  LinScale  con_gate=0.000055  sin_gate=0.001192  AYUDA  21.85x  p=3.36e-16
  MultiCue  con_gate=0.000326  sin_gate=0.019235  AYUDA  58.97x  p=4.91e-03
  CR        con_gate=0.000054  sin_gate=0.001979  AYUDA  36.72x  p=1.38e-31

xtensa-esp32-elf-gcc -std=c99 -Os -I. -c dualbrain.c  ->  COMPILA_OK_exit0
  text 1336  data 0  bss 0  dec 1336
PRUEBA DE QUE EL INSTRUMENTO PUEDE DAR ROJO:
  printf 'int x = "roto";' | xtensa-esp32-elf-gcc -> error int-conversion, DIO_ROJO_OK
```

**Lo que SÍ está vencido en ese archivo:** su fecha dice **24-ago 19:55** y no tiene nada de las resp 063 a 081. **Su tabla de refutados sigue diciendo «el circuito de escape tiene cero inhibitorias», que la resp 068 midió como 49,8% inhibitorio.** Y sigue diciendo «la topología define ruteo y ganancia, no selectividad», retirado en la resp 071.

---

## ÍTEM 6 · los pasos 1 a 4 · **NO CERRADO, y se declara**

**No se ejecutaron.** Este turno se consumó en seis mediciones reales. **No hay nada bloqueándolos**: van primeros en el siguiente turno, y el orden no cambia.

**Lo que SÍ entra de ese ítem:** el **CI de A-03** (`.github/workflows/guards.yml` + `requirements.txt` con pins exactos), que es puramente aditivo y hace que la batería de 28 assertions **corra sola** en vez de a mano.

**Lo que deliberadamente NO se tocó, y el motivo:** migrar `motor.py` y `scriptR.py` a `require()` **modifica los instrumentos de resultados ya publicados**. Con el ítem 4 recién descubierto — que el código del repo **ya** difiere del paper en el `N` de los nulls — tocar esos dos archivos antes de que Abraham decida qué hacer con esa discrepancia **agrega una segunda capa de divergencia sobre la primera**. Se pide la decisión antes.

---

## NO MEDIDO que queda, declarado

1. **La comparación arista por arista contra el `connectome.mat` de Betzel NO se corrió.** La descarga quedó en 33.255.424 B de 106.587.606. Los `md5` no son comparables entre `.mat` y parquet.
2. **Los archivos de datos suplementarios de Betzel** (`.s001` a `.s011`) **no se abrieron**, solo sus captions.
3. **El A/B usa 20 realizaciones de cascada, no 1000** como Betzel. **El piso de `p` a 20 es peor que el suyo**, y el veredicto se apoya en el **spread de 1,009×** y en el orden, no en un `p`.
4. **Mi cascada no es su cascada:** implementa tres estados y `p` por sinapsis según su Fig 1, **sin** sus dinámicas cooperativa y competitiva, y con 12 pasos. **Es la familia, no el mismo modelo.** Si sus dinámicas rompen la saturación, el veredicto cambia.
5. **No se midió si la saturación de la cascada depende de `p_trans` o de `N_seed`.** Un barrido de esos dos parámetros es exactamente el *sensitivity analysis* que pidió su Revisor #3, y **no se corrió**.
6. **`esp32c.py` no se subió** en este turno: está en `/workspace` según el manifiesto, y subirlo es el ítem del turno siguiente.
7. **`nulls40.json` y `dualbrain_bench.json` NO están en `/workspace`** (buscados, no encontrados). **A-04 no se puede cerrar con lo que hay en el container.** Sí está `R_out.json` (26.598 B) y `all12.json` (41.140 B).
8. **El contexto vivo del conectoma acumula seis líneas viejas y el del motor está vencido desde el 24-ago 19:55.** Se nombran, no se reescriben de memoria.
