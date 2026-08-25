# 082 · Seis de los siete NO MEDIDO, cerrados midiendo · y dos hallazgos van en contra mío

**Fecha:** 2026-08-25 11:05 (America/Buenos_Aires) · **Modo:** TITAN FULL

> **🔬 Evidencia cruda:** `docs/agents/evidencia/2026-08-25-siete-items-evidencia-cruda.md`
> **🛠 Instrumento:** `src/ab_cascade_vs_linear.py`, **DONE in 417.1 s**, md5 verificado de los dos lados. 14 corridas de `gateway build.run`.

---

## 1. Pedido

«TITAN FULL: HAZLO» sobre los siete NO MEDIDO que dejó la resp 081.

## 2. Herramientas declaradas (C-03)

| Llamada | Escribe | Cuota ajena |
|---|---|---|
| `mcp_gateway build.run` × 14 sobre `brain-env` | sí, `/workspace/ab_models` y `/tmp`. **El parquet solo leído** | **NO** |
| `get_file_contents` × 6 (contexto motor, y los repos de Eon y Rojas) | no | no |
| `search_web` × 2 | no | no |
| `create_or_update_file` × 1, `push_files` × 1 → rama `titan/twohop-nulls` | sí | no |

**Cero Kaggle. Cero runtime de Tachi. Ningún merge. `main` intacta. Nada borrado. `motor.py` y `scriptR.py` NO se tocaron, y el motivo está en la §9.**

---

## 3. 🔥 ÍTEM 2 · el A/B corrió, y trae dos resultados opuestos

**417,1 segundos, tres guards en verde, control negativo de Dale en 134.547 mixtas.**

### 🟢 A favor: los dos modelos NO ordenan igual, y hay algo más fuerte

| | orden |
|---|---|
| **LINEAR** (con signo, con transitorio) | mechano > gustatory > visual > olfactory |
| **CASCADE** (sin signo, sin transitorio) | gustatory > mechano > olfactory > visual |

`rho = 0,60`, no 1,0. **Pero el hallazgo grande es otro:**

> **El modelo de cascada SATURA.** Las cuatro clases alcanzan **105,1 · 105,5 · 105,65 · 106,05** de **110** motoras, con `sd` de 1,2 a 1,4. **Spread entre extremos: 1,009×.**

**Sobre acceso motor, el modelo sin signo no discrimina nada:** las cuatro medias caben dentro de un desvío. **En el brazo lineal el mismo contraste da 98,4×** (32,15 contra 0,33). **La diferencia no es de sensibilidad: un modelo separa las modalidades y el otro no.**

Y tiene nombre en este repo: es el **modo de falla 2** — un estadístico pegado al techo — esta vez del lado del modelo ajeno.

### 🔴 En contra, y no lo buscaba

```
orden LINEAR por PICO          : mechanosensory > gustatory > visual > olfactory
orden LINEAR por POST-ESTIMULO : mechanosensory > gustatory > visual > olfactory
pico y post-estimulo coinciden = True
```

> **Para este estadístico, el pico y el post-estímulo dan EL MISMO ORDEN.**

**El `sel_post` = 4,3287 sigue en pie**, porque mide otra cosa: selectividad temporal entre **perfiles de *looming* dentro del circuito de escape**, no ranking de modalidades. **Pero el claim general «el pico es lo único que este circuito no discrimina» queda ANGOSTADO a ese circuito y a esa métrica.** Así hay que escribirlo en la v2.

**Apareció corriendo, no releyendo.** Es el único modo en que aparece.

### ⚠️ Y un falso ROJO que casi se cuela

La primera corrida abortó: `Mw` medido **54.492.920** contra **54.492.922** publicado. **Dos sinapsis.** Antes de escribir «discrepancia con Betzel» lo medí: **era mi cast a `float32` perdiendo precisión sobre 15 millones de sumas.** En `int64` el número es exacto.

> **Es el espejo del falso positivo de esta mañana.** Ahí un `returncode 2` correcto por el motivo equivocado; acá un **guard que da ROJO por el motivo equivocado**. **Regla: un guard que se dispara obliga a medir POR QUÉ, no a creerle.**

---

## 4. 🔴 ÍTEM 4 · defecto real, y no es el que sospechaba

Sospechaba que la Tabla 11 contradecía al paper. **Es al revés: la Tabla 11 es consistente con el paper, y el REPO es el que no.**

| Qué | Paper publicado (§2.4) | Repo (código medido) |
|---|---|---|
| MS estático | **N = 100**, en 3 lotes de 34+33+33 | `nulls40_kaggle.py` L120 **`NNULL = 40`** |
| CP estático | **N = 5–10** | `cp40.py` L177 **`NNULL = 40`** |
| Piso de `p` | derivado de 100 | **0,0244**, derivado de 40 |

> **El repo no reproduce los conteos de nulls que declara el paper.** No es que la Tabla 11 esté mal: **el código commiteado no es el que produjo las tablas publicadas.**

**Modo de falla 5, sexta reincidencia.** Y es la **versión profunda del hallazgo 1 de Tachi**: él lo vio en las rutas absolutas de los `.mjs`; el agujero real es que **los `N` no coinciden**. **El erratum no cubre esto**, y ese es el ítem nuevo más importante del día.

---

## 5. 🟢 ÍTEM 3 · cerrado con datos

**Betzel publica sus datos:** Zenodo `10.5281/zenodo.18555170`, con md5 por archivo (`connectome.mat` 106.587.606 B, md5 `a5f4bb8f12c12775a0806457e66cb148`).

- 🟢 **Mismo snapshot, verificado por instrumento:** `N`, `E` y `Mw` **exacto al entero**.
- 🟡 **Mismo ARCHIVO sigue NO MEDIDO:** su `.mat` y nuestro parquet **no tienen md5 comparable por construcción**, y la comparación arista por arista no se corrió.
- 🟢 **Pero deja de ser inferencia:** el md5 de su fuente existe y está publicado → **la comparación es ejecutable por cualquiera.**

---

## 6. ÍTEM 1 · el peer review de Betzel, y corta para los dos lados

**Venía embebido en el XML que ya tenía:** 28.034 caracteres, tres revisores. Y medido:

```
null 0 | randomiz 0 | surrogate 0 | inhibitory 0 | motor neuron 0 | signed(palabra) 0
```

**Ningún revisor pidió un null estructural, ni signo, ni vía motora.** El Revisor #3 contestó **NO** a *«¿se hizo el análisis estadístico de forma rigurosa?»* y pidió **validación contra datos experimentales** y **análisis de sensibilidad**.

**Los dos filos, y hay que decir los dos:**

- 🟢 **el nicho está libre**: lo que hace el Paper 1 no es table stakes.
- 🔴 **pero si tres revisores no pidieron el null, el null no es la vara del campo hoy.** Eso debilita «el null es el producto» como argumento de **venta**, aunque lo refuerce como argumento de **novedad**.
- 🟡 **y lo que SÍ es la vara — validación experimental y sensibilidad — este repo tampoco lo tiene.**

---

## 7. 🔴 ÍTEM 5 · dos hallazgos nuevos, y son de forma pero pesan

**A. El repo público de Eon NO contiene la mosca 3D.** Es un **banco de pruebas de simuladores LIF** (Brian2, Brian2CUDA, PyTorch, NEST GPU, GeNN). **Cero MuJoCo, cero cuerpo.** La demo de +120M de impresiones **no es reproducible desde su repo**. Es el mismo patrón que Tachi nos marcó: publicar algo distinto de lo anunciado.

**B. El repo de Rojas DERIVA del de Eon y no lo cita.** Sus cinco archivos de `code/` son un **subconjunto** de los diez de Eon, con los mismos nombres, **incluido el directorio `paper-phil-drosophila`** (`phil` = Philip Shiu, senior scientist de Eon). Agradece a FlyWire, NeuroMechFly, MuJoCo y Shiu. **A Eon no.** Los tamaños difieren, así que es **versión anterior o modificada, no copia byte-idéntica**, y se declara así.

**Y su `demo.mp4` pesa 133 bytes:** no es un video.

**Su contradicción numérica, medida:** abstract **139.255 / 54,5M sinapsis**, README **138.639 / 15.091.983 aristas**. **Está mezclando sinapsis con conexiones — el mismo defecto de redacción número 1 del Paper 1.** El mismo error, dos papers, un dataset: **eso dice algo del dataset, no de los autores.**

---

## 8. ÍTEM 7 · `CONTEXTO-motor.md` abierto, y contesta el hueco del `.c`

> **El generador de C99 es `esp32c.py`, y está entre los 6 `.py` que siguen FUERA de git.**

**No falta escribir el C: falta commitear el generador.** El `.c` es derivado y la política del repo es no commitear derivados. **La tarea correcta es subir `esp32c.py`.**

**Su núcleo no está vencido:** la ablación del gate (**21,85× a 108,11×**, iso-run, 10 semillas) y los **1.336 B de `.text`** con **prueba de que el compilador puede dar rojo** están medidos y en git.

**Lo que SÍ está vencido:** su fecha es del 24-ago 19:55 y su tabla de refutados aún dice «el circuito de escape tiene cero inhibitorias» (la resp 068 midió **49,8% inhibitorio**) y «la topología no define selectividad» (retirado en la 071).

---

## 9. ÍTEM 6 · no cerrado, con su razón y con un pedazo entregado

**Los pasos 1 a 4 no se ejecutaron.** El turno se consumió en seis mediciones reales. **Nada los bloquea** y van primeros en el siguiente.

**Lo que SÍ entra:** el **CI de A-03**. `.github/workflows/guards.yml` + `requirements.txt` con **pins exactos medidos en el container** (numpy 2.3.5, scipy 1.16.3, pandas 2.3.4, pyarrow 22.0.0, python 3.12.14). El workflow corre la batería de 28 assertions **y además aplica la mutación**: si la batería da verde sobre un `guards.py` roto a propósito, **el job es rojo**. Sin `continue-on-error` y sin `|| true`.

**Lo que deliberadamente NO se tocó:** migrar `motor.py` y `scriptR.py` a `require()` **modifica los instrumentos de resultados publicados**. Con el ítem 4 recién descubierto — que el código **ya** difiere del paper en el `N` de los nulls — tocarlos antes de que Abraham decida qué hacer con esa discrepancia **apila una segunda divergencia sobre la primera**. **Se pide la decisión antes.**

---

## 10. Scorecard

| Criterio | Pts | Evidencia |
|---|---|---|
| **Completitud** | 14/15 | 6 de 7 ítems medidos, el séptimo declarado con razón y con entrega parcial. **−1:** el ítem 6 sigue abierto |
| **Ejecutabilidad** | 15/15 | el A/B corrió en clon fresco con md5 verificado de los dos lados, `DONE in 417.1 s`, JSON emitido |
| **Arquitectura del razonamiento** | 10/10 | tres guards que pueden dar rojo, control negativo de Dale en 134.547, y **el falso rojo del `float32` medido antes de reportarlo como discrepancia de datos** |
| **Testing** | 4/5 | el CI corre la batería **y** su prueba de mutación. **−1:** el CI no se vio correr todavía en GitHub |
| **Documentación** | 10/10 | evidencia verbatim, y **los dos hallazgos que van en contra en sus propias secciones**, no en una nota al pie |
| **Innovación** | 4/5 | la saturación del modelo ajeno y la derivación Rojas←Eon no las tenía nadie. **−1:** ninguna se aplicó al paper |

**Total 57/60 → 95,0/100.** **N/A: 25 pts** (Seguridad 15, DevOps 10). **Testing NO es N/A: entra el CI.**

---

## 11. NO MEDIDO que queda

1. **La comparación arista por arista contra el `.mat` de Betzel no se corrió** (descarga a 33 MB de 106).
2. **Los datos suplementarios de Betzel** (`.s001` a `.s011`) **no se abrieron**, solo captions.
3. **Mi cascada NO es su cascada:** tres estados y `p` por sinapsis según su Fig 1, **sin** sus dinámicas cooperativa y competitiva, 12 pasos, **20 realizaciones contra sus 1000**. Es la familia, no el modelo. **Si sus dinámicas rompen la saturación, el veredicto cambia.**
4. **No se barrió `p_trans` ni `N_seed`.** Ese barrido es exactamente el *sensitivity analysis* que pidió su Revisor #3.
5. **`esp32c.py` no se subió.** Es el ítem del turno siguiente.
6. **`nulls40.json` y `dualbrain_bench.json` NO están en `/workspace`** (buscados, no encontrados) → **A-04 no se puede cerrar con lo que hay en el container.** Sí están `R_out.json` (26.598 B) y `all12.json` (41.140 B).
7. **El CI no se vio correr.** Está commiteado y **no aprobado**: K-02, deuda declarada.
8. **Los dos contextos vivos siguen desactualizados** y se nombran en vez de reescribirse de memoria.
