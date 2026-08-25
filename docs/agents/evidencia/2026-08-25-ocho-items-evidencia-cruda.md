# EVIDENCIA CRUDA · los ocho NO MEDIDO + el trabajo de Tachi sobre DualBrain

**Fecha:** 2026-08-25 11:45 (America/Buenos_Aires)
**Instrumento:** `gateway build.run` sobre `brain-env`, 22 corridas · integración GitHub · sandbox propio
**Datos:** `/workspace/connectivity.parquet`, `/workspace/annotations.tsv`, `betzel_connectome.mat` de Zenodo

---

## 0. 🔥 PRIMERO: el trabajo de Tachi sobre DualBrain, y refuta un hallazgo mío

**Encontrado en `gatehot59-star/mudh-mobile`, rama `titan/esp32-inferencia-c-dualbrain`, commit `99808d45`, del 22-ago 22:51 UTC:**

```
feat(firmware): inferencia DualBrain en C99, verificada contra PyTorch
  docs/campo/resultados/2026-08-22-esp32-c/RECIBO-kaggle-gcc.log   261 lineas
  firmware/dualbrain/README.md                                     161
  firmware/dualbrain/dualbrain.c                                   248
  firmware/dualbrain/dualbrain.h                                   109
  firmware/dualbrain/test/db_test.c                                237
  total 1016 adiciones
```

**Su nota de commit, verbatim en lo que importa:**

> *«El claim de que el modelo corre en un microcontrolador no tenia ni una linea de C. … El compilador es el testigo, no yo. gcc 11.4 con -Wall -Wextra -Wpedantic -Wconversion -Wshadow -Wstrict-prototypes -Wdouble-promotion … acepta dualbrain.c con CERO advertencias en las tres variantes. -Wdouble-promotion es el que importa: verifica que no hay un solo double, en vez de que yo lo afirme.»*

> *«Contra PyTorch, 512 pasos de secuencia y el vector de autoprueba embebido: error maximo **8.94e-08** en la salida y **1.34e-07** en el estado … La Pade sin libm da el MISMO error y corre **1.64x** mas rapido.»*

> *«Siete casos negativos, y uno de ellos **encontro un bug en mi propio test**: al correr el puntero para probar el guard de alineacion se rompia primero el magic, asi que la rama del guard era inalcanzable y el test medía otra cosa.»*

> *«Lo que sigue NO MEDIDO y va escrito: **nada de esto corrio en un ESP32.** Sin hardware no hay numero de hardware. Lo que queda medido son los **3440 MAC por paso**, los **2496 bytes de .text** y los **704 de RAM**.»*

**Y su `dualbrain.h` (leído completo) declara la arquitectura, las dimensiones por `#define` y nueve códigos de retorno que distinguen los tres estados**, incluido `DB_ERR_SELFTEST` y `DB_ERR_ALIGN`.

### 🔴 Lo que esto le hace a mi propio hallazgo de la resp 079

Escribí, confirmando a Tachi: *«113 archivos y **cero** `.c`. El activo comercial no está en el repo.»*

**La medición era correcta y el enunciado estaba mal.** El correcto:

> **El motor SÍ está en git.** Está en **otro repo** (`mudh-mobile`), en una **rama sin mergear**, y ese repo es **PRIVADO** (medido: HTTP 404 sin credencial). **El problema no es que no exista: es que está donde nadie que compre la licencia puede verlo.**

**Y corrige mi ítem 7 de la resp 082**, donde dije que la tarea era subir `esp32c.py`. **No hay que escribir C ni generar nada.** Hay que decidir si esos cinco archivos se mueven al repo público. **Eso mueve trabajo entre dos ejecutores, así que es decisión de Abraham y NO se tocó nada.**

**⚠️ Y una discrepancia de números que NO es un error:** Tachi mide **2496 B de `.text`** y el `CONTEXTO-motor` dice **1336 B**. Los dos son ciertos: 2496 es `gcc` de x86, 1336 es `xtensa-esp32-elf-gcc -Os`. El factor 1,87× ya estaba declarado en el contexto. **Se verifica aquí que las dos mediciones existen y no se contradicen.**

**NO MEDIDO:** los tres archivos **no se compilaron en este turno**. Se intentó bajarlos al container y `raw.githubusercontent` devolvió **HTTP 404** en los tres, porque `mudh-mobile` es privado. El `xtensa-esp32-elf-gcc` **sí está en el container** (`/opt/xtensa-esp-elf/bin/`, verificado con `which`), así que la compilación es posible **en cuanto los archivos estén accesibles**.

---

## 1. 🔥🔥 ÍTEM 3 · el grafo es EL MISMO, arista por arista

```
BYTES 106587606
BYTES_PUBLICADOS 106587606
md5_bajado    a5f4bb8f12c12775a0806457e66cb148
md5_publicado a5f4bb8f12c12775a0806457e66cb148
COINCIDE True

CLAVES: ['W']
   W ndarray (1,1) [('ACH','O'),('DA','O'),('GABA','O'),('GLUT','O'),('OCT','O'),('SER','O'),('TOT','O')]
```

```
=== ITEM 3: COMPARACION ARISTA POR ARISTA contra el .mat de Betzel ===
CAMPOS: ('ACH', 'DA', 'GABA', 'GLUT', 'OCT', 'SER', 'TOT')
TOT tipo csc_array shape (138639, 138639)
BETZEL_TOT  shape (138639, 138639) nnz 15091983 suma 54492922
NUESTRO     shape (138639, 138639) nnz 15091983 suma 54492922

ARISTAS_DIFERENTES 0 de 15091983
SUMA_ABS_DIFERENCIA 0
IDENTICO_ARISTA_POR_ARISTA True

CONTROL NEGATIVO: contra la traspuesta, DEBE diferir
  aristas diferentes vs traspuesta 25206682
DONE
```

> **No es «mismo snapshot con el mismo criterio». Es EL MISMO GRAFO: cero aristas distintas de 15.091.983, y la suma absoluta de la diferencia es 0.**

**El control negativo discrimina** (25.206.682 diferencias contra la traspuesta), así que el comparador **podía dar rojo** y no lo dio.

**Consecuencia para el erratum:** el ítem 1 queda validado por un tercero publicado **sobre datos idénticos**, no equivalentes. Es la forma más fuerte que ese ítem puede tener.

### 🎯 Y un dato lateral que refina el posicionamiento

**Su `.mat` trae los campos `ACH, DA, GABA, GLUT, OCT, SER, TOT`.** O sea que **Betzel PUBLICA la descomposición por neurotransmisor como datos** y no la usa como **signo** en la dinámica.

> **El nicho no es que no tengan el dato: es que no lo usan así.** Esa frase es más precisa y más defendible que la del párrafo de posicionamiento, y hay que corregirla ahí.

---

## 2. 🔴 ÍTEM 6 · el CI corrió y dio ROJO cuatro veces. Las tres causas son mías

**Medido con los CHECK RUNS del commit, no con el estado combinado:**

```
HTTP=200
total_count 2
   bateria de guards (debe poder dar rojo) | completed | failure
   bateria de guards (debe poder dar rojo) | completed | failure

--- workflow runs del repo ---
total_count 6
   guards | titan/twohop-nulls | completed | failure   (x5 listados)
```

### v1 · heredoc indentado dentro de un `run:` de YAML

**Reproducido en el sandbox, verbatim:**

```
  File "<stdin>", line 1
    path = "src/guards.py"
IndentationError: unexpected indent
exit del heredoc: 1
```

Bash pasa las líneas al stdin de python **con la indentación del YAML**, y el `EOF` indentado con espacios tampoco cierra el heredoc (`<<-` solo ignora tabs). **Dos bugs en el mismo bloque, y el paso fallaba por un bug del paso, no por lo que mide.**

**⚠️ Y en esa misma reproducción:** `echo "exit del heredoc: $?"` dio **1** y la línea siguiente imprimió `EXIT_TOTAL=0`, porque el `$?` era el del pipe a `head`. **Séptima vez que el `$?` de un shell miente en este proyecto.**

### v2 · los cuatro pins que declaré MEDIDOS estaban INVENTADOS

**Verificado en vivo contra PyPI y contra el intérprete:**

```
=== V-01: EXISTEN esas versiones en PyPI? Verificacion en vivo ===
  numpy     pin 2.3.5     EXISTE   ultima=2.5.2
  scipy     pin 1.16.3    EXISTE   ultima=1.18.1
  pandas    pin 2.3.4     NO EXISTE EN PYPI   ultima=3.0.5
  pyarrow   pin 22.0.0    EXISTE   ultima=25.0.1

=== y lo que REALMENTE tiene el container ===
  python  3.12.14
  numpy   2.5.2
  scipy   1.18.1
  pandas  3.0.5
  pyarrow 25.0.1
```

> **`pandas 2.3.4` no existe, así que `pip` abortaba y el job moría antes de correr un test. Pero el rojo es el síntoma: el defecto es que escribí CUATRO versiones de memoria bajo la etiqueta «MEDIDAS en el container».** Es la prohibición **V-01** literal, y el patrón del Bloque 8: **un mapa incompleto presentado como el mapa.**

**Segundo bug del mismo YAML**, encontrado al releerlo con la causa del primero en la mano: el paso 3 escribía `mutado.log` en el directorio de trabajo y el paso 6 exigía árbol limpio con `git status --porcelain`. **El paso 6 iba a fallar SIEMPRE por el archivo que el paso 3 crea.** Un guard que no puede dar **verde** es tan inútil como uno que no puede dar rojo.

### v4 · medir el sujeto en vez de pelear con el síntoma

```
=== QUE IMPORTA REALMENTE LA BATERIA? ===
src/guards.py:66:import math
src/guards.py:67:import sys
src/test_guards_negativo.py:16:import subprocess
src/test_guards_negativo.py:17:import sys
src/test_guards_negativo.py:18:import os
src/test_guards_negativo.py:21:import guards
src/ci_mutate_guards.py:25:import sys
src/ci_mutate_guards.py:26:import os
src/ci_mutate_guards.py:27:import shutil

=== corre con python DESNUDO, sin numpy/scipy/pandas/pyarrow? ===
con -S (sin site-packages) returncode = 0
ultima linea: TODOS VERDES, y los controles negativos demuestran que podian dar rojo

=== y el mutador tambien? ===
MUTACION_APLICADA sobre src/guards.py
  mutate -S rc=0
  bateria mutada -S rc=1 (espera !=0)
RESTAURADO src/guards.py desde el respaldo
  restore -S rc=0
954815935545435ced0d1a26865c0859  src/guards.py
```

> **Todo es stdlib. `pip install` no aportaba NADA y era la única fuente de fragilidad.** Los tres rojos vinieron de la infraestructura que instalaba dependencias inútiles.

**La lección, y no la apliqué tres veces seguidas:** antes de arreglar por qué falla una instalación, **preguntar si la instalación hace falta.** Es **E-01** aplicado a un workflow.

### Ciclo completo verificado antes de commitear, los siete pasos

```
1 bateria intacta             rc=0
2 mutate                      rc=0
3 bateria mutada              rc=1  con 3 lineas FAIL
4 restore                     rc=0
5 bateria otra vez verde      rc=0
6 CTRL NEG ancla inexistente  rc=2
7 md5 restaurado == original   954815935545435ced0d1a26865c0859 en los dos lados
```

**🟡 ESTADO HONESTO DEL ÍTEM 6:** la **cuarta** versión del workflow **no se pudo verificar**: la API pública devolvió **HTTP 403 por rate limit** en los dos intentos siguientes. **Queda CORRIENDO Y SIN LEER, declarado así.** No se declara verde.

---

## 3. ÍTEM 5 / A-04 · qué JSON existen, con su SHA-256

```
R_out.json                             26598  sha256:f87a214ec4a9d40eeccd820bf8d0c0409e1266b2b81b042a8934d733967b5655
all12.json                             41140  sha256:349284d553e13510115f5e08f1ea088d62c4a56239bcb868c07f555dc81f5fc9
ab_gate/ab_gate_A.json                 11734  sha256:b01f01e53865bd8773b171718786553ec448643e2cd09b8edfeb85af1e927f88
ab_gate/ab_gate_B.json                 11633  sha256:ab75b34f2bfbc69df6ab1857c5d683407c293a72351a103f2c19ba0432ee58a9
ab_cell/merge_n20.json                  1321  sha256:f018a9b75ca2765fa9411033ea00fd3089d697e1cbffc00f138f3f6cb8087b7f
ab_models/ab_models_out.json            1575  sha256:b1d64f6fa1e88c9d939169c8f2aef51bad89205d2e0c7b3170f326bcee82edc9
nulls40.json                       NO_EXISTE_EN_EL_CONTAINER
dualbrain_bench.json               NO_EXISTE_EN_EL_CONTAINER
```

**A-04 no se cierra entero con lo que hay**, y ahora se sabe **exactamente** qué falta: los dos que el README referencia por md5 **no están en el container**. Los seis que sí están quedan con su SHA-256 medido.

---

## 4. ÍTEMS 1 y 2 · CORRIENDO Y SIN LEER, con parcial declarado

**Instrumento commiteado:** `src/cascade_sensitivity.py`, md5 `74a6a2261e87e8683147364cc9227c20` verificado de los dos lados. Guards en verde:

```
N=138639  E=15091983  Mw=54492922
G1 los tres conteos coinciden con Betzel 2026: OK
  pob visual           n=10855  descartadas=536
  pob olfactory        n=2279  descartadas=3
  pob mechanosensory   n=2656  descartadas=12
  pob gustatory        n=408  descartadas=0
  pob motor            n=110  descartadas=0
  pob ZZQQXX_AZAR      n=256  (control negativo, nodos al azar del grafo)
```

**Los 7 primeros puntos de 30, verbatim:**

```
  p=0.0001 seed=  1  vis=  0.00  olf=  0.00  mec=  0.00  gus=  0.00  | AZAR=  0.00  spread=    inf  no-sat
  p=0.0001 seed=  4  vis=  0.00  olf=  0.00  mec=  0.00  gus=  0.00  | AZAR=  0.05  spread=    inf  no-sat
  p=0.0001 seed= 16  vis=  0.00  olf=  0.00  mec=  0.00  gus=  0.00  | AZAR=  0.05  spread=    inf  no-sat
  p=0.0001 seed= 64  vis=  0.00  olf=  0.00  mec=  0.00  gus=  0.03  | AZAR=  0.12  spread=    inf  no-sat
  p=0.0001 seed=256  vis=  0.00  olf=  0.00  mec=  0.07  gus=  0.10  | AZAR=  0.30  spread=    inf  no-sat
  p=0.0010 seed=  1  vis=  0.00  olf=  0.10  mec=  0.30  gus=  0.75  | AZAR=  1.48  spread=    inf  no-sat
  p=0.0010 seed=  4  vis=  0.00  olf=  3.92  mec=  0.65  gus=  6.40  | AZAR=  5.42  spread=    inf  no-sat
```

**Lo que ya se ve, declarado como PARCIAL y no como veredicto:**

1. **Con `p_trans = 0.0001` la cascada MUERE:** 0,00 motoras en las cuatro clases. **El régimen bajo no es informativo, es vacío.**
2. **🔴 Y en `p=0.001, seed=4` el CONTROL NEGATIVO AL AZAR alcanza 5,42 motoras contra 0,00 de visual y 0,65 de mechanosensorial.** O sea que en el régimen bajo el estadístico **sí separa clases, pero el azar le gana a dos de las cuatro**. **Eso puede angostar el veredicto de la resp 082 y hay que reportarlo cuando el barrido cierre.**

**Estado: 7 de 30 puntos. NO se emite veredicto.**

---

## 5. ÍTEM 4 · los suplementarios · **NO CERRADO, con la causa nombrada**

Dos vías intentadas, las dos fallaron:

```
via 1 (bucle de shell):  s HTTP=404 BYTES=49018 TYPE=text/html   x11
     -> y ademas la variable $i no se expandio: el shell del gateway rompe el for
via 2 (urllib):          HTTPError en el primer intento
```

**El patrón de URL de PLOS para suplementarios no es el que usé.** Los `xlink:href` del XML los nombran como `info:doi/10.1371/journal.pcsy.0000091.s001` a `.s011`, que es un identificador interno, no una URL descargable. **Queda NO MEDIDO con la causa identificada**, y lo que SÍ se leyó en el turno anterior son sus **11 captions**.

---

## 6. NO MEDIDO que queda, declarado

1. **El barrido de los 30 puntos está CORRIENDO Y SIN LEER** (7 de 30). Ningún veredicto de los ítems 1 y 2.
2. **La cuarta versión del CI no se verificó** (HTTP 403 por rate limit). No se declara verde.
3. **Los tres archivos de firmware de Tachi NO se compilaron:** `mudh-mobile` es privado y `raw.githubusercontent` da 404. El `xtensa-esp32-elf-gcc` sí está en el container.
4. **No se copió nada de `mudh-mobile`.** Mover trabajo entre repos de dos ejecutores es decisión de Abraham.
5. **Los suplementarios de Betzel siguen sin abrirse.**
6. **`nulls40.json` y `dualbrain_bench.json` no existen en el container**, así que A-04 queda parcial.
7. **La comparación arista por arista se hizo sobre el campo `TOT`.** Los seis campos por neurotransmisor (`ACH`, `DA`, `GABA`, `GLUT`, `OCT`, `SER`) **no se compararon** contra nuestra columna `Excitatory`, y esa comparación **podría validar o refutar la asignación de signo del Paper 1**. Es la deuda más valiosa que deja este turno.
