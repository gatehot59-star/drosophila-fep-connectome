# EVIDENCIA CRUDA · 2026-08-26 · cierre de los 6 NO MEDIDO de la respuesta 105

**Instrumento:** `gateway build.run` sobre `brain-env`. Los dos motores se importan como
módulos y se llaman sus funciones reales (E-01: el sujeto son los archivos).

---

## 1. A/B CONTROLADO sobre el conectoma real (`tools/ab_controlado_v1_vs_v2_real.py`)

Duración total: **1.185 s (19,7 min)**. Todo fijo salvo el archivo.

```
[    0.8s] modulos cargados
[0.5s]   OK    md5_parquet: 3d802fd542b5d18570ba1ba0bb0abed9
[0.5s]   OK    md5_annotations: 719904abad876c68ace1b5690c9b9b63  (SHA 17fc5772)
[77.5s]   anotaciones: 138625 de 139248 matchean un nodo; 623 NO matchean y quedan SIN region (declarado, no oculto)
[   79.0s] conectoma: n=138639  e=15091983  md5_parquet=3d802fd542b5d18570ba1ba0bb0abed9
[   79.0s] modalidades disponibles: ['visual', 'olfactory', 'mechanosensory', 'gustatory']  tamanos=[10854, 2279, 2656, 408]
[   79.0s] A/B controlado: modalidades=['visual', 'olfactory', 'mechanosensory']  pasos=150  snapshots=[50, 100, 149]
[   79.1s] tau: Re=0.119000  |Im| medio=0.080051  (el MISMO para los dos)

[   79.1s] ########## CONDICION A: phase_jitter = 0.0  (la hipotesis fuerte) ##########
[  252.4s]   v1 REAL jitter=0.0         rho_pre=   2164.2928  nnz=15091983  rdi=t50=0.021787 t100=0.758431 t149=0.607364  (173.3 s)
[  477.5s]   v2 REAL jitter=0.0         rho_pre=   2164.2928  nnz=15091983  rdi=t50=0.021787 t100=0.758431 t149=0.607364  (225.1 s)

[  477.5s]   VEREDICTO de la condicion A, sobre el conectoma real:
[  477.5s]     d(rho_pre)  = 0.000000e+00
[  477.5s]     d(rdi t50 ) = 0.000000e+00   (v1=0.021786820861  v2=0.021786820861)
[  477.5s]     d(rdi t100) = 0.000000e+00   (v1=0.758430739727  v2=0.758430739727)
[  477.5s]     d(rdi t149) = 0.000000e+00   (v1=0.607363543913  v2=0.607363543913)
[  477.5s]     -> IDENTICOS a escala real: la fisica de v1 y v2 es la misma.

[  477.5s] ########## CONDICION B: phase_jitter = 0.1  (el default) ##########
[  644.0s]   v1 REAL jitter=0.1         rho_pre=   2153.6528  nnz=15091983  rdi=t50=0.021918 t100=0.759222 t149=0.605532  (166.4 s)
[  903.7s]   v2 REAL jitter=0.1         rho_pre=   2152.6355  nnz=15091983  rdi=t50=0.021849 t100=0.757692 t149=0.607032  (259.7 s)

[  903.7s]   Cuanto vale el RUIDO DE FASE a escala real:
[  903.7s]     d(rho_pre) = 1.017266   (0.0472% de 2153.6528)
[  903.7s]     d(rdi t50 ) = 0.000070   (v1=0.021918  v2=0.021849)  -> 0.32% del valor
[  903.7s]     d(rdi t100) = 0.001530   (v1=0.759222  v2=0.757692)  -> 0.20% del valor
[  903.7s]     d(rdi t149) = 0.001500   (v1=0.605532  v2=0.607032)  -> 0.25% del valor

[  903.7s] ########## CONDICION C: UN NULL con la MISMA semilla, jitter=0.0 ##########
[  908.5s]   null CP seed=1000 generado (el MISMO array para los dos)
[ 1035.3s]   v1 NULL seed1000 j=0       rho_pre=    655.4540  nnz=14942716  rdi=t50=0.148728 t100=0.537760 t149=0.111000  (126.8 s)
[ 1184.9s]   v2 NULL seed1000 j=0       rho_pre=    655.4540  nnz=14942716  rdi=t50=0.148728 t100=0.537760 t149=0.111000  (149.5 s)
[ 1184.9s]     d(rho_pre)  = 0.000000e+00
[ 1184.9s]     d(rdi t50 ) = 0.000000e+00
[ 1184.9s]     d(rdi t100) = 0.000000e+00
[ 1184.9s]     d(rdi t149) = 0.000000e+00

[ 1184.9s] ########## PERFORMANCE A ESCALA REAL (n=138.639) ##########
[ 1184.9s]   etapa                  v1 (s)         v2 (s)         v2/v1
[ 1184.9s]   pesos+normaliz.        59.27          112.28         1.894
[ 1184.9s]   dinamica x3 mods       114.03         112.86         0.990
[ 1184.9s]   TOTAL                  173.30         225.14         1.299
[ 1184.9s]   fraccion del tiempo en la dinamica:  v1=65.8%   v2=50.1%

[ 1184.9s] FIN. escrito /workspace/ab_real.json
FINAB
```

### Las cuatro cosas que esto cierra

**1. La hipótesis fuerte se sostiene a escala real.** Con `phase_jitter=0` los dos motores
dan **`0.000000e+00`** de diferencia en `rho` y en los **tres** `rdi`, sobre 138.639 nodos
y 15.091.983 aristas. No es «casi igual»: es el mismo número. La 105 mostró esto sobre un
sintético de 4.000 nodos; ahora está medido donde importa.

**2. Cada versión reprodujo su propio número archivado, en una TERCERA máquina.**

| | archivado | re-medido hoy | diferencia |
|---|---|---|---|
| v1, Kaggle CPU, 23-ago | `rho = 2153.6528` | `rho = 2153.6528` | **0** |
| v2, Kaggle GPU P100, 26-ago | `rho = 2152.6355` | `rho = 2152.6355` | **0** |

Dos versiones, tres máquinas, dos backends. **Reproducibilidad medida, no afirmada.**

**3. La predicción numérica de la 105 se cumplió.** Ahí escribí que el delta de rho de
1,0173 entre las dos corridas archivadas «es exactamente el orden que explica el jitter».
Medido hoy en condiciones controladas: **`d(rho) = 1.017266`**. No del mismo orden: **el
mismo número**.

**4. Cierra también los nulls**, que habían quedado fuera: con la misma semilla y sin
jitter, el null da `0.000000e+00` en las cuatro cantidades.

---

## 2. Escala, rankdata, memoria y contratos

(`tools/cierre_escala_rankdata_memoria_contratos.py`, máquina libre)

```
========================================================================================================
RESOLUCION DE LOS NO MEDIDO  ·  escala, rankdata, memoria y contratos
========================================================================================================

[2] BARRIDO DE ESCALA (min de 3, perf_counter)
    n         aristas   | pesos v1    pesos v2    v2/v1   | normal. v1  normal. v2  v2/v1   | propag. v1  propag. v2  v2/v1
    1000      14900     | 0.0031      0.0049      1.57    | 0.0203      0.0894      4.41    | 0.0157      0.0158      1.01
    4000      59896     | 0.0108      0.0179      1.65    | 0.0363      0.1998      5.50    | 0.0577      0.0539      0.93
    16000     239878    | 0.0461      0.0841      1.82    | 0.2548      1.2188      4.78    | 0.2273      0.2267      1.00
    64000     959882    | 0.2486      0.5270      2.12    | 1.5715      7.1556      4.55    | 1.1715      1.1649      0.99

    tendencia del cociente v2/v1 al crecer n:
      pesos          n=1000:1.57  n=4000:1.65  n=16000:1.82  n=64000:2.12
      normalizacion  n=1000:4.41  n=4000:5.50  n=16000:4.78  n=64000:4.55
      propagate      n=1000:1.01  n=4000:0.93  n=16000:1.00  n=64000:0.99

[3] DIAGNOSTICO del rankdata de v2
    La v2 se documenta 'vectorizado', pero tiene un loop de Python sobre los
    valores UNICOS con una asignacion de slice de numpy por iteracion:
        for u, c in zip(uniq, counts): ranks_sorted[start:start+c] = avg
    Prediccion falsable: si el costo es el loop sobre unicos, entonces con POCOS
    unicos (muchos empates) v2 tiene que GANAR, y con TODOS unicos tiene que PERDER.

    caso                         unicos   v1 (s)      v2 (s)      v2/v1     sin-loop    v2/sin-loop
    5k todos unicos              5000     0.01179     0.04765     4.04      0.00095     50.11
    5k con 10 valores            10       0.00681     0.00084     0.12      0.00070     1.20
    5k con 2 valores             2        0.00607     0.00064     0.10      0.00060     1.06
    50k todos unicos             50000    0.14782     0.47518     3.21      0.00919     51.71
    50k con 100 valores          100      0.09405     0.00784     0.08      0.00615     1.27

    Y las tres implementaciones tienen que dar el MISMO resultado:
      v1              = [4.  1.5 1.5 3.  6.  6.  6. ]
      v2 vectorizada  = [4.  1.5 1.5 3.  6.  6.  6. ]
      v2 naive        = [4.  1.5 1.5 3.  6.  6.  6. ]
      sin-loop        = [4.  1.5 1.5 3.  6.  6.  6. ]

[5] MEMORIA (tracemalloc, pico por llamada)
    grafo n=16000  aristas=239878
    etapa                    v1 (MB)        v2 (MB)        v2/v1
    build_weights            14.05          21.07          1.500
    normalize_spectral       9.74           20.25          2.079
    propagate 60 pasos       6.34           6.34           1.000

[6] TABLA DE CONTRATOS: cuantos valores devuelve cada funcion
    funcion                  v1 devuelve                    v2 devuelve                    compatible?
    build_weights            2: ['csr_matrix', 'ndarray']   3: ['csr_matrix', 'ndarray',   NO  <<< desempaquetar por posicion ROMPE
    normalize_spectral       3: ['csr_matrix', 'float', 'b  2: ['csr_matrix', 'dict']      NO  <<< desempaquetar por posicion ROMPE
    propagate                2: ['dict', 'ndarray']         3: ['dict', 'ndarray', 'dict'  NO  <<< desempaquetar por posicion ROMPE
    make_tau                 2: ['ndarray', 'float']        2: ['ndarray', 'float']        SI
    rdi                      3: ['float', 'int', 'int']     3: ['float', 'int', 'int']     SI
```

### Lo que cada bloque cierra

**Escala (NO MEDIDO #2):** el cociente `v2/v1` **no es constante**. En `pesos` **crece con
n** (1,57 → 2,12): el costo del `coalesce_edges` que declara las multi-aristas escala con
el número de aristas. En `normalizacion` se queda plano en ~4,5-5,5×: es el costo fijo de
correr **dos** instrumentos espectrales en vez de uno. Y en `propagate` es **~1,00 en los
cuatro tamaños**, o sea que el núcleo no se tocó a ninguna escala.

**rankdata (NO MEDIDO #3): la predicción se cumplió en 5 de 5 casos.**

- todos únicos → v2 pierde **4,04×** (5k) y **3,21×** (50k)
- 10 valores → v2 **gana 8,3×**
- 2 valores → v2 **gana 10×**

El costo es **el loop de Python sobre los valores únicos**, con una asignación de slice de
numpy por iteración. Y la versión **sin loop** (`np.unique(return_index)` + `np.repeat`) es
**50,11× más rápida que la de v2** con datos todos-únicos, dando el mismo resultado.

La función se documenta «vectorizado» y está vectorizada **solo en el sort**. Es el
patrón 2 del Bloque 8 en versión performance: un docstring que promete algo que el código
no hace.

**Alcance real del defecto, para no inflarlo:** `rankdata` se usa en `global_rank_test`
sobre vectores de `n_nulls + 1 = 40` elementos. A ese tamaño el costo es despreciable.
**Es un defecto de código real y de impacto nulo en el experimento actual**, y las dos
cosas hay que decirlas juntas.

**Memoria (NO MEDIDO #5):** `propagate` es **1,000×**, idéntico otra vez.
`normalize_spectral` es **2,08×** porque guarda dos copias para cruzar ARPACK con la
iteración de potencia, y `build_weights` **1,50×** por los arrays del `coalesce`. Los picos
son de **21 MB** sobre un container con 7,99 GB: no es un límite operativo.

**Contratos (NO MEDIDO #6):** **3 de 5 funciones con el mismo nombre devuelven distinta
cantidad de valores.** El `IndexError` no fue un descuido puntual: es una propiedad
estructural del par v1/v2. Regla que sale: nunca desempaquetar por posición el retorno de
un motor sin chequear `len()` primero.

---

## 3. NO MEDIDO que QUEDA (los nuevos, honestos)

- El A/B controlado usó **un solo null** (seed 1000), no los 39. El claim «idénticos sin
  jitter» está medido sobre el REAL y sobre **un** null, no sobre la distribución entera.
- Las diferencias de la condición B son de **una realización** de la semilla de fase, no de
  una distribución de realizaciones. «0,0472%» es un punto, no un intervalo.
- El barrido de escala llega a **n=64.000**, la mitad del conectoma real. La extrapolación
  a 138.639 se apoya en la corrida real del A/B (1,894× en pesos), que es un solo punto.
- La memoria se midió con `tracemalloc`, que ve **allocaciones de Python**; no mide el RSS
  real ni la memoria de los buffers internos de BLAS/ARPACK.
- No se barrió `phase_jitter` entre 0 y 0,1: solo los dos extremos.
- La versión `sin-loop` de `rankdata` **no se commiteó dentro de `motor_v2.py`**. Está en
  la herramienta como referencia de medición. Cambiar el motor es otra entrega y necesita
  su propio test.
