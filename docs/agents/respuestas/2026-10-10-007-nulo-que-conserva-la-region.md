# Respuesta 007 · nulo que conserva la región: las descendentes mandan por cableado, el central y las ascendentes ganaban por estar cerca

**Fecha:** 2026-10-10, tarde (America/Buenos_Aires) · **Máquina:** brain-env · **Rama:** `titan/tabla7-reconstruida-2026-10-10` (PR #26, sin merge), commit `f436f21ea704f12755f7c7ca3fa2a242c5112052`

**F-01, veredicto:** el instrumento da **PASS** (R = 5.000 por modo y umbral; los 21 chequeos, los dos cruces con la 006 y R ≥ 500 en verde; el control negativo no da flags de más). Con región y tamaño fijos, lo único que sigue mandando fuerte son las descendentes: → motoras ×3,69 / ×3,21 y → descendentes ×3,29 / ×2,61 (k = 40 / k = 120, umbral ≥1; igual con ≥5). El dominio del central sobre las descendentes (×1,07 / ×1,01) y sobre las neurosecretoras (×1,09 / ×1,03) era ubicación; su plus propio es chico y va a las motoras (×1,31 / ×1,16), sobre todo a las de la boca. Las ascendentes caen a azar en las tres salidas (o abajo con k = 40). Lo sensorial le habla a descendentes y motoras menos que sus vecinas (×0,33 a ×0,62 con ≥1). La proyección visual hacia las descendentes pasa de ▼ a azar: estaba lejos, no castigada.

## 1. Pedido

"Run a region-preserving null" (Abraham, 2026-10-10). Era el primer ítem abierto de la 006: un nulo de etiquetas que además conserve la región de origen.

## 2. Herramientas

- brain-env por el gateway (2 núcleos, 7,8 GB): tests, corrida completa (679,5 s), md5 y verificación de los push.
- Sandbox de Brain: escritura del script y de los tests, y reconstrucción del log (md5 igual al de brain-env antes de subir).
- GitHub MCP: push a la rama y a `main` (brain-env no tiene credencial de push para este repo).
- ClickUp: Doc público en el Space.

## 3. Qué se midió

- **Estadístico:** D1(C, O) de la 005, la fracción media de la entrada de las neuronas del conjunto de salida O que viene de la clase C, con los umbrales ≥1 y ≥5. 22 conjuntos (3 de nivel 1 y 19 finos) y 11 clases: 242 tests con ≥1 y 231 con ≥5 (ITP no tiene entrada con ≥5).
- **Región:** k-medias (Lloyd con arranque k-means++, semilla [20261012, k]) sobre `pos_x/y/z` de la anotación, pasado a µm (4 × 4 × 40 nm por vóxel). k = 40 convergió en 74 iteraciones (zonas de 1.850 a 5.412 neuronas); k = 120 no convergió en 100 (355 a 2.381), y una partición fija igual es un estratificado válido. Las 14 neuronas sin posición (sin_anotacion) van a una región aparte.
- **Tamaño:** estratos de ancho fijo en log(1 + fuerza de salida hacia no salidas), 30 pedidos (31 efectivos con ≥1 y 28 con ≥5).
- **Nulo:** permutación uniforme de las etiquetas dentro de cada estrato región × tamaño (935 y 2.389 estratos con ≥1; 816 y 2.268 con ≥5). R = 5.000 por modo y umbral, 20.000 en total; flag con p ≤ 0,001 de cada lado.
- **MEZCLA** por clase: fracción esperada de sus etiquetas que cae en otra clase al barajar. Si es menor a 0,10, un azar pasa a NM. El óptico tiene 0,09 a 0,14: casi sin poder.
- **Firme:** el mismo flag con k = 40, k = 120, ≥1 y ≥5.
- **Chequeos que pueden dar rojo:** cruce exacto con el D1 de la 006, conservación de conteos y estratos, media contra la esperanza exacta (z ≤ 6), varianza empírica sobre exacta (0,9 a 1,1), control negativo con 20 etiquetados falsos del mismo nulo (flags ≤ máx(3, 3 × esperado)) y R ≥ 500. El test extremo a extremo mueve un D1 de la 006 en 1e-6 y el cruce da FAIL.
- Todos los parámetros se fijaron en el script antes de correr, y hubo una sola corrida completa.

### Lectura

- **Cableado (firme en las cuatro condiciones):** descendentes → descendentes, motoras, cuello (×5,06 / ×3,74), proboscis (×4,37 / ×4,24) y antena (×5,34 / ×3,83); central → motoras, ingestión (×1,31 / ×1,20), proboscis (×1,48 / ×1,28), haustelo (×1,73 / ×1,61) y DH44 (×1,97 / ×1,20); motoras → motoras de ingestión (×20,35 / ×8,00).
- **Era ubicación (▲ en la 006, azar con región):** central → descendentes y → neurosecretoras, IPC incluida; ascendentes → las tres salidas; sensorial ascendente → motoras (y → descendentes pasa a ▼ con ≥5); motoras y neurosecretoras → motoras de nivel 1.
- **Abajo de sus vecinas (firme):** sensorial y visual centrífuga → descendentes y motoras; proyección visual → motoras. El óptico también, pero sin poder.
- **Cuánto esperaba el azar:** el central pone el 60,23% de la entrada de las descendentes. El nulo de tamaño de la 006 esperaba 37,04%; el de región espera 56,10% / 59,78%. Cualquier neurona de esa zona y de ese tamaño daría casi lo mismo.
- **Geografía no es artefacto:** que el central viva al lado de las salidas también es biología. Lo que dice este nulo es que la etiqueta de clase no agrega nada más allá de dónde está la neurona y cuánto manda.
- **Calibración:** el control negativo da 11 y 1 flags de 4.840 con ≥1, y 5 y 2 de 4.620 con ≥5, contra 9,68 y 9,24 esperados. Con k = 120 quedan muchas celdas que el nulo no puede mover, así que ahí es conservador.

### Errores propios

- Un loop de verificación con una variable de shell salió vacío porque el transporte del gateway expande `$`. Lo repetí con rutas explícitas: 4/4 md5 iguales. No tocó ningún archivo.

## 4. Evidencia cruda (verbatim)

`results/output_control_regionnull_2026-10-10/tests.log`:

```text
TEST test_permutador_rapido_conserva_estratos_y_es_uniforme -> conserva clase x estrato en 200 permutaciones; las 6 permutaciones de 3 salen ~1/6 cada una
TEST test_rapido_coincide_con_formulas_exactas -> media y varianza del permutador rapido == formulas exactas de la 006 (z max 1.15, cociente 0.995)
TEST test_kmedias_recupera_tres_grupos -> k-medias recupera 3 grupos separados, converge en 2 iteraciones y es determinista
TEST test_mezcla_y_flag_efectivo -> mezcla = 1 - n_C/N con un estrato y 0 con clases separadas; azar con mezcla < 0,10 pasa a NM
TEST test_geografia_engana_a_estr_y_no_a_region -> clase que solo esta cerca de O: estr=SOBRE, region=azar; clase que le habla mas que sus vecinas: estr=SOBRE, region=SOBRE
TEST test_extremo_a_extremo_contra_la_006 -> extremo a extremo: 005 -> 006 -> 007, cruce PASS, R=300 da INCOMPLETO, un D1 movido 1e-6 da FAIL
TESTS_OK 6
```

`results/output_control_regionnull_2026-10-10/run.log`, líneas 1 a 29 (encabezado, regiones, mezcla y nulos de ≥1):

```text
== output_control_region_null.py :: nulo que conserva region y tamano para la 005 y la 006 ==
ENTORNO python=3.12.14 numpy=2.5.3 scipy=1.18.1 pandas=3.0.5 maquina=brain-env
PARAMETROS seed=20261012 r=5000 n_falsos=20 k_regiones=40,120 n_tam=30 p_flag=0.001 mezcla_min=0.1 z_max=6 factor_control=3
INPUT parquet /workspace/connectivity.parquet md5=3d802fd542b5d18570ba1ba0bb0abed9 pin_ok=True
INPUT annotations /workspace/annotations.tsv md5=719904abad876c68ace1b5690c9b9b63 pin_ok=True
INPUT json_006 results/output_control_permnull_2026-10-10/output_control_permutation_null.json md5=ec64172711d7d18040f6f09335d7521b
GRAFO n_nodos=138639 n_aristas=15091983 mapeo_biyectivo=True sinapsis_total=54492922
CLASES ascending=1736 central=32379 descending=1299 endocrine=76 motor=110 optic=77530 sensory=16352 sensory_ascending=581 visual_centrifugal=524 visual_projection=8038 sin_anotacion=14
POSICIONES con_pos=138625 sin_pos=14 rango_um x=88.0-902.9 y=51.4-442.9 z=0.6-278.7
REGIONES k=40 iteraciones=74 convergio=True inercia_um2=2.249e+08 tam_min=1850 tam_mediana=3416 tam_max=5412 sin_posicion=14
REGIONES k=120 iteraciones=100 convergio=False inercia_um2=9.485e+07 tam_min=355 tam_mediana=1218 tam_max=2381 sin_posicion=14
CONJUNTOS 22 (nivel1 3 + finos 19) neuronas_de_salida=1485
== VARIANTE >=1 | conjuntos_con_entrada=22/22 | tamano: estratos=31 ancho_log=0.3837 factor=1.468 ==
ESTRATOS [>=1] reg40 n=935 unitarios=67 tam_max=1219
ESTRATOS [>=1] reg120 n=2389 unitarios=260 tam_max=616
MEZCLA [>=1] clase                    n   perm estr06  reg40 reg120
MEZCLA [>=1] ascending             1736  0.987  0.981  0.436  0.226
MEZCLA [>=1] central              32379  0.766  0.699  0.222  0.152
MEZCLA [>=1] descending            1299  0.991  0.986  0.873  0.766
MEZCLA [>=1] endocrine               76  0.999  0.990  0.712  0.324
MEZCLA [>=1] motor                  110  0.999  0.993  0.855  0.645
MEZCLA [>=1] optic                77530  0.441  0.402  0.126  0.092
MEZCLA [>=1] sensory              16352  0.882  0.529  0.250  0.190
MEZCLA [>=1] sensory_ascending      581  0.996  0.976  0.645  0.544
MEZCLA [>=1] visual_centrifugal     524  0.996  0.949  0.876  0.777
MEZCLA [>=1] visual_projection     8038  0.942  0.920  0.798  0.672
MEZCLA [>=1] sin_anotacion           14  1.000  0.999  0.000  0.000
NULO [>=1] reg40 R=5000 segundos=144.5 conteos_ok=True estratos_ok=True media_max_z=3.72 var_ratio_mediana=1.0028
NULO [>=1] reg120 R=5000 segundos=143.8 conteos_ok=True estratos_ok=True media_max_z=3.40 var_ratio_mediana=0.9998
```

Líneas 30 a 68 (nivel 1, ≥1):

```text
-- NIVEL1 descending [>=1] | con_entrada=1299
clase                   D1% estr06   enrE  reg40%    x40 f40   reg120%   x120 f120 
ascending             12.98 SOBRE    5.61   14.39   0.90 BAJO    13.31   0.98 azar 
central               60.23 SOBRE    1.63   56.10   1.07 SOBRE   59.78   1.01 azar 
descending            15.17 SOBRE   15.09    4.61   3.29 SOBRE    5.81   2.61 SOBRE
endocrine              0.01 azar     1.12    0.02   0.57 azar     0.02   0.62 azar 
motor                  0.06 azar     1.50    0.08   0.76 azar     0.09   0.64 azar 
optic                  0.45 BAJO     0.01    8.09   0.06 BAJO     5.95   0.08 BAJO 
sensory                4.28 azar     0.96    8.20   0.52 BAJO     6.89   0.62 BAJO 
sensory_ascending      1.62 SOBRE   10.87    2.09   0.77 BAJO     1.80   0.90 azar 
visual_centrifugal     0.58 BAJO     0.47    1.42   0.41 BAJO     1.55   0.37 BAJO 
visual_projection      4.61 BAJO     0.68    5.01   0.92 azar     4.79   0.96 azar 
sin_anotacion          0.00 azar     0.01    0.00   1.00 NM       0.00   1.00 NM   
-- NIVEL1 motor [>=1] | con_entrada=110
clase                   D1% estr06   enrE  reg40%    x40 f40   reg120%   x120 f120 
ascending              6.92 SOBRE    3.45   10.37   0.67 BAJO     7.20   0.96 azar 
central               64.34 SOBRE    1.86   49.02   1.31 SOBRE   55.60   1.16 SOBRE
descending            21.48 SOBRE   19.96    5.82   3.69 SOBRE    6.70   3.21 SOBRE
endocrine              0.15 SOBRE   10.85    0.09   1.75 azar     0.15   0.99 azar 
motor                  1.03 SOBRE   22.86    0.20   5.11 azar     0.37   2.81 azar 
optic                  0.00 BAJO     0.00   14.24   0.00 BAJO    10.99   0.00 BAJO 
sensory                3.57 BAJO     0.60   10.91   0.33 BAJO     9.11   0.39 BAJO 
sensory_ascending      1.48 SOBRE    7.85    2.36   0.63 azar     2.04   0.73 azar 
visual_centrifugal     0.03 BAJO     0.03    1.05   0.02 BAJO     1.27   0.02 BAJO 
visual_projection      1.01 BAJO     0.15    5.94   0.17 BAJO     6.58   0.15 BAJO 
sin_anotacion          0.00 azar     0.00    0.00    nan NM       0.00    nan NM   
-- NIVEL1 endocrine [>=1] | con_entrada=73
clase                   D1% estr06   enrE  reg40%    x40 f40   reg120%   x120 f120 
ascending             15.93 SOBRE   10.24   15.84   1.01 azar    13.49   1.18 azar 
central               73.03 SOBRE    2.29   66.90   1.09 azar    70.72   1.03 azar 
descending             4.37 azar     4.92    3.47   1.26 azar     3.48   1.25 azar 
endocrine              0.69 SOBRE  116.11    0.12   5.79 azar     0.30   2.30 SOBRE
motor                  0.02 azar     0.79    0.04   0.55 azar     0.13   0.16 azar 
optic                  0.00 BAJO     0.00    1.96   0.00 BAJO     1.80   0.00 BAJO 
sensory                4.27 azar     1.10    7.26   0.59 azar     6.45   0.66 azar 
sensory_ascending      1.31 azar     9.52    2.19   0.60 azar     1.94   0.68 azar 
visual_centrifugal     0.00 BAJO     0.00    0.67   0.00 BAJO     0.36   0.00 BAJO 
visual_projection      0.37 BAJO     0.05    1.54   0.24 azar     1.33   0.28 azar 
sin_anotacion          0.00 azar     0.00    0.00    nan NM       0.00    nan NM   
```

Líneas 89 a 101 (cambios de nivel 1, ≥1; los finos están en el log completo):

```text
INESTABLE [>=1] descending                               ascending           estr06=SOBRE reg40=BAJO  reg120=azar  D1 12.98% x0.90/x0.98
INESTABLE [>=1] descending                               central             estr06=SOBRE reg40=SOBRE reg120=azar  D1 60.23% x1.07/x1.01
NUEVO     [>=1] descending                               sensory             estr06=azar  -> region=BAJO  D1 4.28% x0.52/x0.62
INESTABLE [>=1] descending                               sensory_ascending   estr06=SOBRE reg40=BAJO  reg120=azar  D1 1.62% x0.77/x0.90
CAMBIA    [>=1] descending                               visual_projection   estr06=BAJO  -> region=azar  D1 4.61% x0.92/x0.96
INESTABLE [>=1] motor                                    ascending           estr06=SOBRE reg40=BAJO  reg120=azar  D1 6.92% x0.67/x0.96
CAMBIA    [>=1] motor                                    endocrine           estr06=SOBRE -> region=azar  D1 0.15% x1.75/x0.99
CAMBIA    [>=1] motor                                    motor               estr06=SOBRE -> region=azar  D1 1.03% x5.11/x2.81
CAMBIA    [>=1] motor                                    sensory_ascending   estr06=SOBRE -> region=azar  D1 1.48% x0.63/x0.73
CAMBIA    [>=1] endocrine                                ascending           estr06=SOBRE -> region=azar  D1 15.93% x1.01/x1.18
CAMBIA    [>=1] endocrine                                central             estr06=SOBRE -> region=azar  D1 73.03% x1.09/x1.03
INESTABLE [>=1] endocrine                                endocrine           estr06=SOBRE reg40=azar  reg120=SOBRE D1 0.69% x5.79/x2.30
CAMBIA    [>=1] endocrine                                visual_projection   estr06=BAJO  -> region=azar  D1 0.37% x0.24/x0.28
```

Líneas 179 a 199 (cierre de ≥1 y arranque de ≥5):

```text
RESUMEN [>=1] D1 tests=242 | estr06 SOBRE=55 BAJO=49 | reg40 SOBRE=21 BAJO=61 NM=22 | reg120 SOBRE=16 BAJO=41 NM=31 | acuerdo_reg40_reg120=198/242 | estr06->region se_mantienen=41 cambian=37 nuevos=9 inestables=44
CRUCE_006 [>=1] PASS max_dif=0.0 faltan=0 n_con_entrada_distinto=0
CONTROL_NEGATIVO [>=1] reg40 flags=11/4840 esperado=9.68 tope=29.04 OK=True
CONTROL_NEGATIVO [>=1] reg120 flags=1/4840 esperado=9.68 tope=29.04 OK=True
== VARIANTE >=5 | conjuntos_con_entrada=21/22 | tamano: estratos=28 ancho_log=0.3813 factor=1.464 ==
ESTRATOS [>=5] reg40 n=816 unitarios=43 tam_max=1130
ESTRATOS [>=5] reg120 n=2268 unitarios=136 tam_max=491
MEZCLA [>=5] clase                    n   perm estr06  reg40 reg120
MEZCLA [>=5] ascending             1736  0.987  0.981  0.439  0.236
MEZCLA [>=5] central              32379  0.766  0.709  0.227  0.155
MEZCLA [>=5] descending            1299  0.991  0.985  0.894  0.804
MEZCLA [>=5] endocrine               76  0.999  0.993  0.867  0.693
MEZCLA [>=5] motor                  110  0.999  0.993  0.918  0.779
MEZCLA [>=5] optic                77530  0.441  0.415  0.141  0.104
MEZCLA [>=5] sensory              16352  0.882  0.700  0.343  0.252
MEZCLA [>=5] sensory_ascending      581  0.996  0.982  0.680  0.580
MEZCLA [>=5] visual_centrifugal     524  0.996  0.960  0.902  0.814
MEZCLA [>=5] visual_projection     8038  0.942  0.925  0.804  0.681
MEZCLA [>=5] sin_anotacion           14  1.000  0.999  0.000  0.000
NULO [>=5] reg40 R=5000 segundos=145.5 conteos_ok=True estratos_ok=True media_max_z=3.10 var_ratio_mediana=0.9994
NULO [>=5] reg120 R=5000 segundos=145.6 conteos_ok=True estratos_ok=True media_max_z=2.43 var_ratio_mediana=0.9954
```

Líneas 200 a 238 (nivel 1, ≥5):

```text
-- NIVEL1 descending [>=5] | con_entrada=1262
clase                   D1% estr06   enrE  reg40%    x40 f40   reg120%   x120 f120 
ascending             13.62 SOBRE    5.15   14.75   0.92 azar    13.74   0.99 azar 
central               62.42 SOBRE    1.53   58.07   1.07 SOBRE   61.88   1.01 azar 
descending            14.43 SOBRE   13.97    4.31   3.35 SOBRE    5.37   2.69 SOBRE
endocrine              0.01 azar     1.03    0.01   0.60 azar     0.01   0.55 azar 
motor                  0.00 azar     0.15    0.04   0.12 azar     0.05   0.09 azar 
optic                  0.33 BAJO     0.01    7.31   0.04 BAJO     5.33   0.06 BAJO 
sensory                3.43 azar     1.04    7.10   0.48 BAJO     5.91   0.58 BAJO 
sensory_ascending      0.88 SOBRE    7.21    1.70   0.52 BAJO     1.41   0.63 BAJO 
visual_centrifugal     0.51 BAJO     0.34    1.55   0.33 BAJO     1.56   0.33 BAJO 
visual_projection      4.37 BAJO     0.64    5.15   0.85 azar     4.74   0.92 azar 
sin_anotacion          0.00 azar     0.00    0.00    nan NM       0.00    nan NM   
-- NIVEL1 motor [>=5] | con_entrada=109
clase                   D1% estr06   enrE  reg40%    x40 f40   reg120%   x120 f120 
ascending              6.62 SOBRE    2.80    9.80   0.68 BAJO     6.69   0.99 azar 
central               65.54 SOBRE    1.72   51.69   1.27 SOBRE   58.71   1.12 SOBRE
descending            21.89 SOBRE   20.01    5.94   3.69 SOBRE    6.73   3.25 SOBRE
endocrine              0.00 azar     0.00    0.01   0.00 azar     0.02   0.00 azar 
motor                  0.68 azar    18.24    0.09   7.26 azar     0.15   4.53 azar 
optic                  0.00 BAJO     0.00   12.69   0.00 BAJO    10.11   0.00 BAJO 
sensory                3.15 azar     0.68   10.78   0.29 BAJO     8.90   0.35 BAJO 
sensory_ascending      1.03 azar     5.90    2.01   0.51 azar     1.81   0.57 azar 
visual_centrifugal     0.01 BAJO     0.01    1.09   0.01 BAJO     1.27   0.01 BAJO 
visual_projection      1.08 BAJO     0.16    5.90   0.18 BAJO     5.61   0.19 BAJO 
sin_anotacion          0.00 azar     0.00    0.00    nan NM       0.00    nan NM   
-- NIVEL1 endocrine [>=5] | con_entrada=69
clase                   D1% estr06   enrE  reg40%    x40 f40   reg120%   x120 f120 
ascending             20.31 SOBRE   10.48   15.58   1.30 azar    15.85   1.28 azar 
central               67.88 SOBRE    2.03   66.18   1.03 azar    67.12   1.01 azar 
descending             4.31 azar     5.00    3.76   1.15 azar     3.33   1.29 azar 
endocrine              0.00 azar     0.00    0.02   0.00 azar     0.00   0.00 azar 
motor                  0.00 azar     0.00    0.05   0.00 azar     0.12   0.00 azar 
optic                  0.00 BAJO     0.00    1.46   0.00 BAJO     0.82   0.00 azar 
sensory                6.16 azar     1.56    8.60   0.72 azar     8.52   0.72 azar 
sensory_ascending      1.24 azar     8.50    2.68   0.46 azar     3.02   0.41 azar 
visual_centrifugal     0.00 azar     0.00    0.56   0.00 azar     0.46   0.00 azar 
visual_projection      0.11 BAJO     0.02    1.12   0.10 azar     0.75   0.15 azar 
sin_anotacion          0.00 azar     0.00    0.00    nan NM       0.00    nan NM   
```

Líneas 259 a 269 (cambios de nivel 1, ≥5):

```text
CAMBIA    [>=5] descending                               ascending           estr06=SOBRE -> region=azar  D1 13.62% x0.92/x0.99
INESTABLE [>=5] descending                               central             estr06=SOBRE reg40=SOBRE reg120=azar  D1 62.42% x1.07/x1.01
NUEVO     [>=5] descending                               sensory             estr06=azar  -> region=BAJO  D1 3.43% x0.48/x0.58
CAMBIA    [>=5] descending                               sensory_ascending   estr06=SOBRE -> region=BAJO  D1 0.88% x0.52/x0.63
CAMBIA    [>=5] descending                               visual_projection   estr06=BAJO  -> region=azar  D1 4.37% x0.85/x0.92
INESTABLE [>=5] motor                                    ascending           estr06=SOBRE reg40=BAJO  reg120=azar  D1 6.62% x0.68/x0.99
NUEVO     [>=5] motor                                    sensory             estr06=azar  -> region=BAJO  D1 3.15% x0.29/x0.35
CAMBIA    [>=5] endocrine                                ascending           estr06=SOBRE -> region=azar  D1 20.31% x1.30/x1.28
CAMBIA    [>=5] endocrine                                central             estr06=SOBRE -> region=azar  D1 67.88% x1.03/x1.01
INESTABLE [>=5] endocrine                                optic               estr06=BAJO  reg40=BAJO  reg120=azar  D1 0.00% x0.00/x0.00
CAMBIA    [>=5] endocrine                                visual_projection   estr06=BAJO  -> region=azar  D1 0.11% x0.10/x0.15
```

Líneas 317 a 337 (cierre):

```text
RESUMEN [>=5] D1 tests=231 | estr06 SOBRE=33 BAJO=32 | reg40 SOBRE=17 BAJO=38 NM=21 | reg120 SOBRE=11 BAJO=24 NM=21 | acuerdo_reg40_reg120=209/231 | estr06->region se_mantienen=27 cambian=30 nuevos=6 inestables=22
CRUCE_006 [>=5] PASS max_dif=0.0 faltan=0 n_con_entrada_distinto=0
CONTROL_NEGATIVO [>=5] reg40 flags=5/4620 esperado=9.24 tope=27.72 OK=True
CONTROL_NEGATIVO [>=5] reg120 flags=2/4620 esperado=9.24 tope=27.72 OK=True
-- QUE CONTROLA CADA CLASE CON REGION Y TAMANO (D1; firme = igual en reg40, reg120, >=1 y >=5) --
QUE_CONTROLA_REGION ascending: mezcla_min=0.226 con_poder | SOBRE: ninguna | BAJO: ninguna de nivel1 + 0 finos
QUE_CONTROLA_REGION central: mezcla_min=0.152 con_poder | SOBRE: motor x1.31/x1.16, motor:ingestion_motor_neuron x1.31/x1.20, motor:proboscis_motor_neuron x1.48/x1.28, motor:haustellum_motor_neuron x1.73/x1.61, endocrine:DH44 x1.97/x1.20 | BAJO: ninguna de nivel1 + 0 finos
QUE_CONTROLA_REGION descending: mezcla_min=0.766 con_poder | SOBRE: descending x3.29/x2.61, motor x3.69/x3.21, motor:neck_motor_neuron x5.06/x3.74, motor:proboscis_motor_neuron x4.37/x4.24, motor:antennal_motor_neuron x5.34/x3.83 | BAJO: ninguna de nivel1 + 0 finos
QUE_CONTROLA_REGION endocrine: mezcla_min=0.324 con_poder | SOBRE: ninguna | BAJO: ninguna de nivel1 + 0 finos
QUE_CONTROLA_REGION motor: mezcla_min=0.645 con_poder | SOBRE: motor:ingestion_motor_neuron x20.35/x8.00 | BAJO: ninguna de nivel1 + 0 finos
QUE_CONTROLA_REGION optic: mezcla_min=0.092 sin_poder | SOBRE: ninguna | BAJO: descending, motor + 6 finos
QUE_CONTROLA_REGION sensory: mezcla_min=0.190 con_poder | SOBRE: ninguna | BAJO: descending, motor + 4 finos
QUE_CONTROLA_REGION sensory_ascending: mezcla_min=0.544 con_poder | SOBRE: ninguna | BAJO: ninguna de nivel1 + 1 finos
QUE_CONTROLA_REGION visual_centrifugal: mezcla_min=0.777 con_poder | SOBRE: ninguna | BAJO: descending, motor + 1 finos
QUE_CONTROLA_REGION visual_projection: mezcla_min=0.672 con_poder | SOBRE: ninguna | BAJO: motor + 3 finos
QUE_CONTROLA_REGION sin_anotacion: mezcla_min=0.000 sin_poder | SOBRE: ninguna | BAJO: ninguna de nivel1 + 0 finos
R_PEDIDO_500 r=5000 ok=True
CHEQUEOS mapeo=True conteos_reg40_>=1=True estratos_reg40_>=1=True media_reg40_>=1=True varianza_reg40_>=1=True control_reg40_>=1=True conteos_reg120_>=1=True estratos_reg120_>=1=True media_reg120_>=1=True varianza_reg120_>=1=True control_reg120_>=1=True conteos_reg40_>=5=True estratos_reg40_>=5=True media_reg40_>=5=True varianza_reg40_>=5=True control_reg40_>=5=True conteos_reg120_>=5=True estratos_reg120_>=5=True media_reg120_>=5=True varianza_reg120_>=5=True control_reg120_>=5=True
JSON results/output_control_regionnull_2026-10-10/output_control_region_null.json md5=72427fdc69a583ca796f448f6aaae0a5
VEREDICTO_NULO PASS
FIN_NULO segundos=679.5
```

## 5. Archivos

| Archivo | Dónde | Bytes | md5 |
|---|---|---|---|
| `tools/output_control_region_null.py` | rama, `f436f21` | 26.070 | `cc4a494a53a3b8b27bd340ee268ff114` |
| `tests/test_output_control_region_null.py` | rama, `f436f21` | 9.358 | `596643b242b72a97ffa1aebd466b1cf2` |
| `results/output_control_regionnull_2026-10-10/run.log` | rama, `f436f21` | 41.407 | `10270929125d858343467acb3b67deaa` |
| `results/output_control_regionnull_2026-10-10/tests.log` | rama, `f436f21` | 882 | `c30ee44dace8ab7e1d9703293be48d7e` |
| `results/output_control_regionnull_2026-10-10/output_control_region_null.json` | sólo brain-env | 308.544 | `72427fdc69a583ca796f448f6aaae0a5` |
| `results/output_control_regionnull_2026-10-10/progress.log` | sólo brain-env | 878 | `33d9938ca7e53e23a3dd59569a7fccfe` |

Entradas: `connectivity.parquet` `3d802fd542b5d18570ba1ba0bb0abed9`, `annotations.tsv` (pin 17fc577) `719904abad876c68ace1b5690c9b9b63` y el JSON de la 006 `ec64172711d7d18040f6f09335d7521b`.

Verificación del push: `git show FETCH_HEAD:<archivo> | md5sum` contra el archivo de brain-env, 4/4 iguales.

Doc público: [Nulo regional: las descendentes mandan por cableado, el central y las ascendentes ganaban por estar cerca](https://app.clickup.com/90171457413/docs/2kza6fw5-20917).

## 6. NO MEDIDO

- **Neuropilo de cada sinapsis.** La región sale de un punto por neurona, no de dónde está la sinapsis. En ascendentes y sensoriales ese punto cae en su arborización del cerebro; en el central suele caer cerca del soma. "Misma región" no mide lo mismo en todas las clases, y la tabla por sinapsis no está en el parquet.
- D2 (vía un intermediario) con este nulo.
- Sensibilidad a otras k, a otra cantidad de estratos de tamaño y a regiones anatómicas en vez de k-medias.
- Corrección por comparaciones múltiples. Lo firme exige cuatro flags concordantes, pero no está corregido.
- Signo fisiológico, función de cada descendente en el cuerpo y causalidad.

--- METODO PROMETEO ---
Máquina: brain-env (2 núcleos), corrida de 679,5 s; tests 6/6 en sandbox y en brain-env.
Artefactos: `docs/agents/respuestas/2026-10-10-007-nulo-que-conserva-la-region.md` + Doc https://app.clickup.com/90171457413/docs/2kza6fw5-20917
