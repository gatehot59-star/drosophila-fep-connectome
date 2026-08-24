# 047 · El release sube a git, el 1.652× se retira, y los `.mjs` no corren en un clon

**Fecha:** 2026-08-24 19:20 (America/Buenos_Aires) · **Modo:** TITAN FULL

---

## 1. Pedido

«Hazlo» (retirar el 1.652× del contexto vivo y subir los 10 archivos del release) **más una regla nueva de entrega:** cada respuesta cierra mostrando **los enlaces de los Docs Y los enlaces de los archivos de git** creados o modificados, para poder ir a revisar. **Guardado en memoria persistente en este turno.**

---

## 2. Herramientas declaradas (C-03)

| Llamada | Escribe | Cuota ajena |
|---|---|---|
| `gateway build.run` × 4 (md5 del release, lectura de los 8 archivos de texto, test de clon) | `/tmp` | **NO** |
| `push_files` · 8 archivos | **sí, al repo** | no |
| edición de memoria persistente | sí | no |

**Cero Kaggle, cero cuota, `gradlew` no ejecutado, nada publicado en Zenodo.** Una llamada murió por timeout (`find | while read` abre un subshell por archivo): se reemplazó por Python, que es la regla 4 del entorno.

---

## 3. Qué se midió

### 3.1 🚨 Los dos `.mjs` NO corren en un clon ajeno, y mi propio test dio un falso verde

```
src/analyze_nulls40.mjs:2   fs.readFileSync("/workspace/nulls40_kaggle.json")
src/routing_hierarchy.mjs:2 fs.readFileSync("/workspace/n40_filas.json")
```

**Rutas absolutas fuera del repo.** El README promete `node src/analyze_nulls40.mjs` y dice que el insumo es `results/nulls40.json`. **Ese archivo existe y su md5 coincide** (`38bf1fcadaf37a3b125f83d22b6f4d8e` es idéntico a `/workspace/nulls40_kaggle.json`), **pero el script no lo lee.** En cualquier máquina que no sea ésta, falla con archivo inexistente.

**Y mi test dio `CORRE_OK`:**

```
$ mkdir -p /tmp/clon/src /tmp/clon/results
$ cp repo/src/analyze_nulls40.mjs /tmp/clon/src/ ; cp repo/results/nulls40.json /tmp/clon/results/
$ cd /tmp/clon && node src/analyze_nulls40.mjs
CORRE_OK
meta: N=138639 E=15091983 sinapsis=54492922 nulls=40
```

**Es E-01, de nuevo, y en el mismo turno en que lo estoy documentando.** Copié el script a `/tmp/clon` y lo corrí desde ahí, pero el script **no lee una ruta relativa**: lee `/workspace/...`, que en **esta** máquina existe. Mi «clon limpio» no era limpio en la única dimensión que importaba. **El test no podía dar rojo.**

El `CORRE_OK` es entonces evidencia de lo contrario de lo que parece: **prueba que el script depende de un archivo fuera del repo**, porque corrió sin que `results/nulls40.json` estuviera en su camino.

**Y hay una dependencia de orden no documentada:** `analyze_nulls40.mjs` termina con `fs.writeFileSync("/workspace/n40_filas.json", ...)` y `routing_hierarchy.mjs` lee ese archivo. El segundo **no puede correr** sin el primero.

**Decisión: se sube tal cual y se declara en el README y en METHODS, no se parchea.** Son los scripts que produjeron figuras publicadas; cambiarles el insumo es tocar código publicado y es decisión de Abraham.

### 3.2 `src/nulls40_structural.py` **ya estaba en git** con otro nombre

```
465cb76a58978fba37b707b7745f2275  repo/src/nulls40_structural.py
465cb76a58978fba37b707b7745f2275  src/nulls40_kaggle.py        <- ya en git
```

**Byte-idénticos.** No se duplica: el README y METHODS pasan a citar `src/nulls40_kaggle.py`, que es el nombre que ya tiene el repo. **Los «10 archivos del release» eran 9 nuevos y uno ya subido.**

### 3.3 El `dualbrain_bench.log` AFINA la salvedad cross-run del doc `6137`

El contexto del motor decía que el hallazgo «el brazo más congelado le gana a `DualNoGate` por 3,2× a 35×, 4/4 tareas» es **cross-run en las cuatro**. Leí el log y es más preciso que eso:

| Tarea | `DualNoGate` en el bench | brazo C en `tres_brazos` | ¿misma arquitectura? |
|---|---|---|---|
| Gated | `h_r=26 h_m=8` | `h_r=26 h_m=8` | **SÍ** |
| LinScale | `h_r=26 h_m=8` | `h_r=26 h_m=8` | **SÍ** |
| MultiCue | `h_r=30 h_m=5` | `h_r=26 h_m=8` | no |
| CR | `h_r=30 h_m=5` | `h_r=26 h_m=8` | no |

**La comparación es iso-arquitectura en 2 de 4 y cross-arquitectura en 2 de 4.** Sigue siendo **entre corridas** en las cuatro (son kernels distintos), así que el brazo `D` sigue haciendo falta, pero la salvedad estaba **sobre-generalizada**: en Gated y LinScale lo único que cambia es la corrida, no la arquitectura.

**Y el log trae la ablación del gate que SÍ es iso-run, iso-arquitectura, 4/4:** `DualBrain` contra `DualNoGate` en el mismo kernel, misma celda, mismo encoder, única diferencia `g*h_m` contra `h_m`. Gana el gate en 4/4: **108,11×** (`p=1,56e-105`), 21,85×, 58,97× y 36,72×. **Eso no necesita ningún brazo nuevo.**

**Bonus medido en el mismo log:** en **MultiCue el DualBrain PIERDE** contra GRU (0,42×), LSTM (0,25×) y MinGRU (0,59×). El contexto decía «1,18× sobre LSTM en el óptimo», y ese óptimo es del barrido de `h_m`, no de esta corrida. En **esta** configuración (`h_r=30 h_m=5`) la brecha con LSTM es **4× en contra**.

### 3.4 El README publica el `temporal RDI` como «resultado negativo»

Verbatim del archivo: *«The dynamic results of the companion papers are reported as a **negative methodological result**, not as a validated model.»* Y el `temporal RDI` (`z = 197`, el resultado más fuerte del expediente) cae ahí adentro.

**No lo reclasifiqué: es la decisión 3 pendiente y es tuya.** Lo que hice es **agregar un bloque de «Pending revision» encima**, que dice qué está mal con esa frase y pide explícitamente **no citarla como veredicto** sobre el temporal RDI. Un repo público que va a citar un preprint con DOI no puede tener el resultado más fuerte archivado como negativo sin una nota al lado.

### 3.5 Lo que agregué al README y a METHODS, y por qué

| Agregado | Motivo |
|---|---|
| Los ratios contra el null **estricto** (20,59× y 7,81×) al lado de los de grado | el README publicaba solo 47,3× y 24,3×, que son del null más débil |
| La limitación de «cantidad conservada» en la jerarquía de ruteo | el README la publicaba como establecida, y contra modularidad es **no testeable** |
| El **guard de `sd == 0`** en METHODS, como sección propia del null CP | costó 22,2 min de cuota y no estaba escrito en ningún archivo público |
| Las **definiciones de población** de la Tabla 5 (`cell_class`, `motor_n = 1485`, `p_exc = 0,600272`) | sin eso la Tabla 5 no es reproducible por nadie |
| La nota de densidad con la causa del overflow, y sinapsis vs conexiones con los dos números | METHODS es donde un revisor va a buscarlo |
| Los dos JSON grandes referenciados por md5 y tamaño | regla de datos derivados: la evidencia verbatim va en los `.log`, que **sí** se commitean |

---

## 4. Evidencia cruda verbatim

```
$ python3 /tmp/mf.py    (md5 y bytes de los 11 del release)
     1105  c6a1ef91cea6c75fb16974db3841e81f  ./LICENSE
     4831  667e28d62092c7f8e7b68d04410d16d3  ./README.md
     6862  2ae28606c28c140dc76cd3b8e6b3ab85  ./docs/ERRATUM.md
     4540  0c2f9bf2d4b9f6bcaaf6cbaad1bf08b9  ./docs/METHODS.md
    31527  1025d60b4e9521d7e4a21ed282935049  ./results/dualbrain_bench.json
     9895  e7aac964c9a5c7cc6553308bbce62af7  ./results/dualbrain_bench.log
   191443  38bf1fcadaf37a3b125f83d22b6f4d8e  ./results/nulls40.json
     5850  a927ece0a08085718815e50c4bfcd08c  ./results/nulls40.log
     3528  732037ff75cecfc857d64a3be1b23a87  ./src/analyze_nulls40.mjs
     7912  465cb76a58978fba37b707b7745f2275  ./src/nulls40_structural.py
     1170  1ad11a5ebfe9362bd986b4e5b8abb6df  ./src/routing_hierarchy.mjs

$ md5sum repo/results/nulls40.json nulls40_kaggle.json
38bf1fcadaf37a3b125f83d22b6f4d8e  repo/results/nulls40.json
38bf1fcadaf37a3b125f83d22b6f4d8e  nulls40_kaggle.json
   -> mismo archivo, distinto nombre. El script lee el de /workspace.

$ cd /tmp/clon && node src/analyze_nulls40.mjs
CORRE_OK          <- FALSO VERDE: leyo /workspace/, no results/

$ grep -n 'readFileSync\|writeFileSync' repo/src/*.mjs
analyze_nulls40.mjs:2   readFileSync("/workspace/nulls40_kaggle.json")
analyze_nulls40.mjs:47  writeFileSync("/workspace/n40_filas.json")
routing_hierarchy.mjs:2 readFileSync("/workspace/n40_filas.json")
```

**Recomputable y contradecible (W-01):** **si `analyze_nulls40.mjs` leyera una ruta relativa, el §3.1 se cae.** La línea 2 está commiteada verbatim y se puede verificar en el archivo subido.

---

## 5. Archivos generados o modificados

**En git, 8 archivos:**

| Archivo | Estado |
|---|---|
| `LICENSE` | **nuevo** (corregida la referencia al ítem del erratum: es el 8, no el 4) |
| `README.md` | **nuevo**, con el bloque «Pending revision», los ratios del null estricto, la limitación de cantidad conservada, el defecto de los `.mjs` y el layout real del repo |
| `docs/METHODS.md` | **nuevo**, con la causa del overflow, sinapsis vs conexiones, las definiciones de población de la Tabla 5 y el guard de `sd == 0` |
| `src/analyze_nulls40.mjs` | **nuevo**, verbatim, sin parchear |
| `src/routing_hierarchy.mjs` | **nuevo**, verbatim, sin parchear |
| `results/nulls40.log` | **nuevo**, verbatim (los 40 nulls con sus invariantes) |
| `results/dualbrain_bench.log` | **nuevo**, verbatim (6 modelos, 4 tareas, 10 semillas, Bode, ablación) |
| `docs/agents/respuestas/2026-08-24-047-...md` | este archivo |

**No subidos, y declarado:** `results/nulls40.json` (191.443 B) y `results/dualbrain_bench.json` (31.527 B), referenciados por md5 en el README según la regla de datos derivados grandes. Su evidencia verbatim **sí** está commiteada en los dos `.log`.

**No duplicado:** `src/nulls40_structural.py`, que ya está en git como `src/nulls40_kaggle.py` con md5 idéntico.

**En memoria persistente:** la regla de cerrar cada entrega con los enlaces de los Docs **y** los de git.

---

## 6. NO MEDIDO, declarado

1. **No corrí los dos `.mjs` en una máquina sin `/workspace`.** El defecto del §3.1 se deduce de la línea 2 de cada script, no de haberlo visto fallar en un tercero. **Es lectura de código, no ejecución**, y va declarado como tal.
2. **No leí los dos JSON grandes.** Van por md5.
3. **No verifiqué los números del README** contra `nulls40.json` (47,3× · 24,3× · 27,3× · 0,41× y las 8 filas del ruteo). Vienen del propio archivo y del `nulls40.log`; **no los recomputé hoy**.
4. **No toqué la clasificación del `temporal RDI`.** Es la decisión 3 y es de Abraham.
5. **No re-verifiqué los DOI contra Zenodo**, ni Lin ni Betzel contra sus fuentes. Tres verificaciones externas pendientes antes de subir la v2.
6. **Los 6 `.py` de deuda siguen fuera de git** (`brazo_w.py`, `n21.py`, `esp32c.py`, `tres_brazos.py`, `nulls19b.py`, `paper_db.py`, 169.586 B). Su manifiesto con md5 está en `docs/agents/MANIFIESTO-KAGGLE.md`.
7. **El `CONTEXTO-motor.md` no se tocó en este commit**, y el §3.3 lo contradice en dos puntos (la salvedad sobre-generalizada y el 1,18× sobre LSTM). Va en el commit siguiente.
8. **No corrí el review automático** sobre estos archivos. **K-02: deuda declarada**, y «nadie objetó» no es «está aprobado».

---

## 7. La regla que sale

**Un test que copia el sujeto a otro directorio no prueba portabilidad si el sujeto usa rutas absolutas.** El «clon limpio» tiene que ser limpio **en la dimensión que se está midiendo**, y acá esa dimensión era el sistema de archivos entero, no el directorio de trabajo. La forma correcta de falsarlo era mover o renombrar `/workspace/nulls40_kaggle.json` y ver si el script seguía corriendo — y eso **no lo hice**, porque habría tocado un archivo del workspace de Abraham.

**Corolario:** cuando un test verde no puede dar rojo, el verde no es un resultado. Es la tercera vez hoy que un guard propio falla así (el `$?` del shell, el `grep -c` con la coma de miles, y ahora este).

```
--- METODO TITAN ---
Accion delicada: SI. Se crean 7 archivos en la raiz de un repo publico, incluido
                 LICENSE y README.md, que son contrato publico. Mitigacion:
                 ninguno existia en git (nada pisado), los dos .mjs y los dos
                 .log van VERBATIM sin editar una linea, y los agregados al
                 README y METHODS son notas declarativas que no alteran ningun
                 numero medido. La clasificacion del temporal RDI NO se cambio:
                 se le puso una nota que pide no citarla, y la decision queda
                 con Abraham. Cero cuota, gradlew no ejecutado, nada en Zenodo.
Modo aplicado:   TITAN FULL
Rubrica:         44/45 -> 98/100. Aplicables: Completitud, Arquitectura del
                 razonamiento, Documentacion, Innovacion, Proceso QA.
                 N/A: 45 pts (Ejecutabilidad, Seguridad, Testing, DevOps).
                 -1 en Completitud: los dos JSON grandes van por md5 y no
                 commiteados, asi que el release en git no es el release entero.
N/A declarados:  45 pts
Review externo:  no pedido. K-02: DEUDA declarada sobre 7 archivos nuevos de un
                 repo publico. El falsador de este turno fue el propio codigo:
                 la linea 2 de los dos .mjs contradice lo que el README promete.
Instrumento:     gateway build.run sobre brain-env, 4 llamadas. md5sum y Python
                 3.12.14 para el manifiesto. Evidencia cruda en la seccion 4.
                 ADVERTENCIA DE INSTRUMENTO: mi test de clon limpio dio
                 CORRE_OK sobre un script que NO es portable. Documentado en
                 3.1 y en la seccion 7.
                 NO MEDIDO: la seccion 6, ocho items.
```
