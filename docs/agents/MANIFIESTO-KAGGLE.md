# MANIFIESTO KAGGLE · los 40 kernels de las dos cuentas

**Medido:** 2026-08-24 17:25 (America/Buenos_Aires) · **Fuente:** API de Kaggle v1, `kernels/list` paginado, autenticación `Bearer`. **Se re-mide, no se recuerda.**

**Por qué existe:** hasta hoy el corpus se creía de **29 notebooks**, porque eran los 29 `CODE__*.txt` que había en `/workspace/kaggle/`. La fuente dice **40**. Los 11 que faltaban son **los kernels de agosto**, y su ausencia hizo que la resp 044 declarara un barrido «cerrado» sobre 29 de 40.

**Nota de autenticación:** los tokens llevan prefijo `KGAT_` y **solo funcionan con `Authorization: Bearer <token>`**. Las otras cinco formas probadas dan `401` en las dos cuentas. El helper `kauth.mjs` usa `Basic` y por eso falla; `klib.mjs` usa `Bearer` y funciona. **Un 401 de `kauth.mjs` NO significa que las credenciales expiraron.**

---

## La partición: 29 de Abraham (feb-marzo) + 11 míos (agosto), cero solapamiento

| | cantidad | quién | ¿en el container? |
|---|---|---|---|
| feb-marzo 2026 | **29** | Abraham | sí, `kaggle/CODE__*.txt` |
| agosto 2026 | **11** | BRAIN | **no** → bajados hoy a `kaggle_ago/AGO__*.txt` |
| **total** | **40** | | |

---

## Los 11 kernels de agosto, con su gemelo local y su md5

| Kernel | Última corrida | bytes | md5 | Archivo local | ¿git? |
|---|---|---|---|---|---|
| `abrahammendieta/titan-nulls19-conectoma-real` | 2026-08-22 22:19 | 11.805 | `17a08b3ac119657ab4a56d985f995436` | `nulls19b.py` | no |
| `fabiomurillohot/titan-esp32-c-inferencia` | 2026-08-22 22:45 | 40.175 | `87a95ebda97a64321b6d360316684173` | `esp32c.py` | no |
| `abrahammendieta/titan-nulls40-estructural` | 2026-08-23 06:40 | 7.912 | `465cb76a58978fba37b707b7745f2275` | `nulls40_kaggle.py` | **SÍ** |
| `abrahammendieta/titan-nulls21-global12` | 2026-08-23 12:37 | 57.157 | `fdb64199dfdfcfb036927806cbf5e66d` | `n21.py` | no |
| `abrahammendieta/titan-cp40-estructural` | 2026-08-23 13:50 | 12.332 | `11ca727ca266e3d91c504872304850d0` | `cp40.py` = `cp.py` | **SÍ** |
| `abrahammendieta/titan-motor-ltc-complejo` | 2026-08-23 15:06 | 30.644 | `480539069ec00f317eec525e6fa81324` | `motor.py` | **SÍ** |
| `fabiomurillohot/titan-hm-sweep-multicue` | 2026-08-23 15:30 | 17.479 | `4131462d21475e85773cd6c0504f5685` | `hm_sweep.py` | **SÍ** |
| `abrahammendieta/titan-tres-brazos` | 2026-08-23 15:45 | 17.805 | `73196d78e8d8290fa8feaa0caf883e82` | `tres_brazos.py` = `src.py` | no |
| `abrahammendieta/titan-brazo-w` | 2026-08-23 18:44 | 22.517 | `a2ac2a4416126d428227c7f87197c3e3` | `brazo_w.py` | no |
| `fabiomurillohot/titan-paper-dualbrain` | 2026-08-23 00:06 | 20.122 | `8a42246b54157cbee67fe99110a7be40` | `paper_db.py` = `dualbrain_src.py` | no |
| `fabiomurillohot/notebook723c6c247a` | 2026-08-24 02:47 | 1.946 | `ba347dab22a44145414da71af0229e42` | **ninguno** | no |

**10 de 11 son byte-idénticos a un archivo del container.**

### ✅ Los cuatro que están en git son byte-idénticos a lo que corrió

```
480539069ec00f317eec525e6fa81324  src/motor.py           = titan-motor-ltc-complejo
11ca727ca266e3d91c504872304850d0  src/cp40.py            = titan-cp40-estructural
465cb76a58978fba37b707b7745f2275  src/nulls40_kaggle.py  = titan-nulls40-estructural
4131462d21475e85773cd6c0504f5685  src/hm_sweep.py        = titan-hm-sweep-multicue
```

**Consecuencia (W-01):** los resultados de esos cuatro kernels son **recomputables por un tercero desde git**, sin intermediarios. No es «una versión del código»: es el mismo archivo, bit por bit, verificado desde los dos lados.

### El huérfano está resuelto y es nada

`notebook723c6c247a` (24-ago 02:47, 1.946 B) es **la plantilla vacía de Kaggle**: `import numpy`, `import pandas`, el `os.walk('/kaggle/input')` de ejemplo y un `kagglehub.dataset_download` comentado. `isInternetEnabled: false`, sin acelerador. **Creado por accidente. No es un resultado perdido.**

---

## 🔴 DEUDA: 6 archivos corrieron en Kaggle y NO están en git

| Archivo | Kernel | md5 | bytes |
|---|---|---|---|
| `brazo_w.py` | `titan-brazo-w` | `a2ac2a4416126d428227c7f87197c3e3` | 22.517 |
| `n21.py` | `titan-nulls21-global12` | `fdb64199dfdfcfb036927806cbf5e66d` | 57.157 |
| `esp32c.py` | `titan-esp32-c-inferencia` | `87a95ebda97a64321b6d360316684173` | 40.175 |
| `tres_brazos.py` | `titan-tres-brazos` | `73196d78e8d8290fa8feaa0caf883e82` | 17.805 |
| `nulls19b.py` | `titan-nulls19-conectoma-real` | `17a08b3ac119657ab4a56d985f995436` | 11.805 |
| `paper_db.py` | `titan-paper-dualbrain` | `8a42246b54157cbee67fe99110a7be40` | 20.122 |

**Total: 169.586 B.** Con estos md5 la subida deja de depender de la palabra de nadie: se verifica contra Kaggle **y** contra el container.

---

## Los 29 de febrero-marzo (Abraham)

Están íntegros en `/workspace/kaggle/CODE__*.txt`. **Cero kernels de Kaggle ausentes del container en esta franja**, o sea que ese lado del corpus sí estaba completo.

**Los tres que contienen el overflow de `int32`:**

| Notebook | línea | md5 |
|---|---|---|
| `abrahammendieta/notebook2f910c646f` | 482 | `77183226dde616cc6b68d988ed76b033` |
| `fabiomurillohot/notebook57386e9dd2` | 512 | `c5cfdc8d339f02ae1da96b171b4ff451` |
| `fabiomurillohot/notebook2e0ceb4908` | 833 | `e6b011b7e9c3d92826eda5ad19afaa9f` |

Los tres hacen `density = W.nnz / (N * (N - 1))` con `N` de tipo `numpy.int32`. El tercero **es el Script V-K**, el verificador que el manuscrito cita.

---

## El barrido del overflow, con el denominador correcto

| Franja | Kernels | Con overflow | Por qué |
|---|---|---|---|
| feb-marzo (Abraham) | 29 | **3** | `N * (N - 1)` con `N` en `int32` |
| agosto (BRAIN) | 11 | **0** | castea: `float(N) * float(N - 1)` |
| **total** | **40** | **3** | |

**El overflow vive exclusivamente en el pipeline de marzo. Ninguna medición de agosto lo hereda.**

---

## NO MEDIDO

- **No se leyó la SALIDA de ningún kernel**, solo la fuente. Los logs de `titan-paper-dualbrain` y `notebookceb82767da` (928 KB) siguen sin leer.
- **Un solo patrón de overflow barrido** (`N*(N-1)`). No se barrieron `N**2` ni otros productos de enteros grandes.
- **No se verificó que los 3 notebooks con overflow sean los que produjeron el paper publicado.** Los tres se declaran descendientes del «pipeline original».
- **No se midió la cuota restante** de ninguna de las dos cuentas.
- **No se listaron datasets ni modelos** de las dos cuentas, solo kernels.

```
--- METODO TITAN ---
Accion delicada: NO. API de Kaggle en solo lectura. Cero kernels lanzados, cero
                 cuota consumida, ninguna credencial rotada ni movida.
Modo aplicado:   TITAN FULL
Rubrica:         emitida en la respuesta 045, 45/45 -> 100/100.
Review externo:  el falsador fue Kaggle: su inventario (40) contra el corpus
                 local (29). El denominador de un barrido no se lee en la copia,
                 se mide en la fuente.
Instrumento:     gateway build.run sobre brain-env. kernels/list paginado y
                 kernels/pull x 11 con Bearer. md5sum sobre los 11 bajados y
                 cruce por hash contra /workspace/*.py y /workspace/*/*.py.
                 Evidencia cruda verbatim en respuestas/2026-08-24-045.
```
