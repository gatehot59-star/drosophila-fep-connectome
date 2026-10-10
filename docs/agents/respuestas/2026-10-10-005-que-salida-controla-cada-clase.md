# 2026-10-10-005 · Qué salida controla cada clase

**Veredicto (F-01): MEDIDO, instrumento PASS.** Sobre FlyWire v783 real (138.639 neuronas, 15.091.983 aristas, 54.492.922 sinapsis):

- **El central controla las tres salidas.** Pone el 60,23% / 62,42% (sin umbral / ≥5) de la entrada de las descendentes, el 64,34% / 65,54% de las motoras y el 73,03% / 67,88% de las neurosecretoras: 2,3 a 2,9 veces lo que le da a un destino al azar. Es la entrada mayor de 1.051 de 1.299 descendentes, 90 de 110 motoras y 62 de 73 neurosecretoras.
- **Las descendentes controlan las motoras de la cabeza:** 21,48% / 21,89% de la entrada motora (x20,7 / x26,5). Por subclase: cuello 39,96% / 43,07%, antena 32,06% / 32,26%, proboscis 24,72% / 25,12%.
- **Las ascendentes (el cuerpo) controlan sobre todo a las neurosecretoras:** 15,93% / 20,31% (x8,6 / x11,7). Además ponen 12,98% / 13,62% de las descendentes y 6,92% / 6,62% de las motoras.
- **El óptico no controla ninguna salida:** 0,45% / 0,33% de la entrada de las descendentes y 0,00% de motoras y neurosecretoras (x0,01 o menos). A dos saltos, 3,64% / 2,71%.
- **Lo sensorial directo es marginal:** entre 3,15% y 6,16% de cada salida, sin diferencia firme con el azar.
- **Signo (predicción del parquet, no fisiología):** central → motoras 43,72% / 43,81% excitatorio, o sea mayoría freno; sensorial → descendentes 99,58% / 99,54%.

Lectura estadística: con etiquetas permutadas, el nulo de destinos al azar da ~3% de falsos (8/242 y 6/231). Se firman sólo los patrones que superan al permutado. Las subclases de 2 a 14 neuronas valen como porcentaje, no como significancia.

## 1. Pedido

"Medí qué salida controla cada clase", después de la respuesta 004. Luego "REPITE TU RESPUESTA?": la medición no había llegado a correr. Esta respuesta la corre y, al final, repite la 004 en corto.

## 2. Herramientas y máquina

- **brain-env** (gateway `build.run`): sondeo de las columnas de anotación y de la columna `Excitatory`; tests (`TESTS_OK 5`); corrida real (58,8 s); verificación md5 después del push. Escribió sólo en el worktree `/workspace/dfc-t7` y en `/tmp`. Sin runtime ni cuota ajena.
- **Sandbox propio:** escritura del script y de los tests contra fuerza bruta (`TESTS_OK 5`).
- **GitHub (integración):** push de código, tests y logs a `titan/tabla7-reconstruida-2026-10-10` (commit `7e75cde`, PR #26 sin merge), y de esta respuesta y el CONTEXTO a `main`.
- **ClickUp:** Doc público en el Space.
- Sin Kaggle ni Actions.

## 3. Qué se midió

Salidas: `descending` (1.299), `motor` (110, partidas por `cell_sub_class`) y `endocrine` (76, partidas por `cell_type`). Para cada clase de origen C y cada salida O, con A[i,j] = S[i,j] / entrada_j:

- **D1(C,O):** media, sobre las neuronas de O con entrada, de la fracción de su entrada (en sinapsis) que viene de C. Suma 1 sobre C.
- **D2(C,O):** lo mismo con A·A, o sea a través de una neurona intermedia cualquiera.
- **Nulo:** la misma media sobre conjuntos de destinos al azar del mismo tamaño (R = 10.000, con reposición, semilla 20261010). `enr` = D / media del nulo. Flag `SOBRE` o `BAJO` si el p unilateral es ≤ 0,001.
- **cobertura:** % de neuronas de O con al menos una arista desde C.
- **exc%:** % de las sinapsis C→O con presináptico excitatorio según `Excitatory` (±1).
- **domina:** neuronas de O cuya mayor entrada viene de C, sin contar empates.
- Variantes: sin umbral y con ≥5 sinapsis por arista.

### D1 por clase y salida (%, sin umbral / ≥5)

| clase | descendentes | motoras | neurosecretoras |
|---|---|---|---|
| central | 60,23 / 62,42 | 64,34 / 65,54 | 73,03 / 67,88 |
| descending | 15,17 / 14,43 | 21,48 / 21,89 | 4,37 / 4,31 |
| ascending | 12,98 / 13,62 | 6,92 / 6,62 | 15,93 / 20,31 |
| sensory | 4,28 / 3,43 | 3,57 / 3,15 | 4,27 / 6,16 |
| visual_projection | 4,61 / 4,37 | 1,01 / 1,08 | 0,37 / 0,11 |
| sensory_ascending | 1,62 / 0,88 | 1,48 / 1,03 | 1,31 / 1,24 |
| motor | 0,06 / 0,00 | 1,03 / 0,68 | 0,02 / 0,00 |
| endocrine | 0,01 / 0,01 | 0,15 / 0,00 | 0,69 / 0,00 |
| visual_centrifugal | 0,58 / 0,51 | 0,03 / 0,01 | 0,00 / 0,00 |
| optic | 0,45 / 0,33 | 0,00 / 0,00 | 0,00 / 0,00 |

La 004 contaba aristas; esta pesa por sinapsis y normaliza por neurona destino. Por eso lo sensorial directo da 4,28% acá y 7,32% en la 004.

### Quién domina cada neurona de salida (sin umbral / ≥5)

- descendentes (1.299 / 1.262 con entrada): central 1.051 / 1.000, descending 121 / 125, ascending 54 / 81, sensory 41 / 32, resto y empates 32 / 24.
- motoras (110 / 109): central 90 / 88, descending 17 / 17, ascending 2 / 3, sensory_ascending 1 / 1.
- neurosecretoras (73 / 69): central 62 / 54, ascending 7 / 10, sensory 4 / 4, empates 0 / 1.

### Lectura firme y lectura descriptiva (post hoc, declarada)

El control negativo permuta las etiquetas de origen y deja los destinos reales. Dio 8/242 y 6/231 flags, contra 70/242 y 47/231 reales. Pasó la tolerancia congelada (≤5%), pero muestra que el nulo de destinos independientes es optimista donde las neuronas de salida comparten entradas.

- Los flags permutados `SOBRE` cayeron sólo en clases chicas (del tamaño de 110 y de 1.736 neuronas). Los `BAJO` cayeron entre x0,00 y x0,83. Ninguna clase grande permutada dio `SOBRE`.
- **Se firma:** central `SOBRE` en las tres salidas; óptico `BAJO` en las tres (x0,01 o menos, contra x0,20 del permutado más bajo en clases grandes); descending → motor x20,7 / x26,5; ascending → descending x7,0 / x7,9, → motor x3,7 / x3,9 y → endocrine x8,6 / x11,7 (ahí el permutado llegó a x4,16: margen de 2×); sensory_ascending → descending x6,7 / x7,6.
- **Sólo descriptivo:** visual_projection → descending (x1,18 / x1,40) y sensory → descending (x1,25 / x1,43), porque el permutado ya dio x1,29 en descendentes. Tampoco se firma ninguna significancia en subclases de 2 a 14 neuronas (CRZ, Hugin-RG, lNSC, DH31...).

## 4. Evidencia cruda verbatim

Comandos en brain-env, dentro de `/workspace/dfc-t7`:

```
python3 tests/test_output_control_by_class.py > results/output_control_2026-10-10/tests.log 2>&1
nohup python3 tools/output_control_by_class.py > results/output_control_2026-10-10/run.log 2>&1 &
```

md5 de lo que corrió. Los cuatro primeros son iguales en la rama, verificado con `git show FETCH_HEAD:<ruta> | md5sum`:

```
5c6a6accd3b1d06e4a9c19cf65348ee3  tools/output_control_by_class.py
18251a01d46f9b2a010a990af5f669c0  tests/test_output_control_by_class.py
60d9a6d51997bab40f84c957f65cc3b3  results/output_control_2026-10-10/run.log
53794d14e99d13bb55d95670486432cb  results/output_control_2026-10-10/tests.log
6f76578ab8f8e1ed5f1da005f559118e  results/output_control_2026-10-10/output_control_by_class.json  (285283 B, sólo en brain-env)
```

Líneas del log. El log completo, de 177 líneas, está en la rama:

```
== output_control_by_class.py :: que salida controla cada clase ==
ENTORNO python=3.12.14 numpy=2.5.3 pandas=3.0.5 pyarrow=25.0.1 scipy=1.18.1 maquina=brain-env
PARAMETROS seed=20261010 r_nulo=10000 r_control=2000 p_flag=0.001 tol_control=0.05
INPUT parquet /workspace/connectivity.parquet bytes=100804642 md5=3d802fd542b5d18570ba1ba0bb0abed9 pin_ok=True
INPUT annotations /workspace/annotations.tsv bytes=31718505 md5=719904abad876c68ace1b5690c9b9b63 pin_ok=True
GRAFO n_nodos=138639 n_aristas=15091983 nodos_sin_id=0 ids_unicos=138639 mapeo_biyectivo=True indice_es_rango_ordenado=True autolazos=0 sinapsis_total=54492922 excitatory_valores={'-1': 6032681, '1': 9059302}
ANOTACION filas=139248 duplicados=0 nodos_sin_fila=14 super_class_vacia=0
CLASES ascending=1736 central=32379 descending=1299 endocrine=76 motor=110 optic=77530 sensory=16352 sensory_ascending=581 visual_centrifugal=524 visual_projection=8038 sin_anotacion=14
SALIDAS descending=1299 motor=110 endocrine=76
== VARIANTE >=1 sinapsis | aristas=15091983 | sinapsis=54492922 | neuronas_con_entrada=137090 ==
-- SALIDA descending [>=1] | n=1299 | con_entrada=1299 | sinapsis_entrada=2213351 | suma_D2=0.9984 | empates=8
clase                 fila%     D1%  nulo1%   enr1 flag1     D2%  nulo2%   enr2 flag2 cobert%    exc% domina
ascending             18.36   12.98    1.86   6.97 SOBRE   12.71    1.92   6.63 SOBRE   98.85   59.94     54
central                6.94   60.23   25.18   2.39 SOBRE   59.77   23.95   2.50 SOBRE   99.69   50.83   1051
descending            34.65   15.17    1.03  14.78 SOBRE   10.47    0.97  10.83 SOBRE   99.08   59.44    121
endocrine             13.96    0.01    0.00   4.80 azar     0.02    0.00   6.16 SOBRE    2.77  100.00      0
motor                  4.89    0.06    0.01   4.85 azar     0.09    0.02   5.81 SOBRE   19.32   78.23      0
optic                  0.03    0.45   61.60   0.01 BAJO     3.64   59.93   0.06 BAJO    12.39   35.46      1
sensory                7.67    4.28    3.43   1.25 azar     4.91    5.23   0.94 azar    41.42   99.58     41
sensory_ascending     10.61    1.62    0.24   6.69 SOBRE    1.54    0.21   7.16 SOBRE   32.49   78.16     14
visual_centrifugal     0.88    0.58    2.74   0.21 BAJO     0.95    3.17   0.30 BAJO    46.42   53.01      0
visual_projection      3.77    4.61    3.90   1.18 azar     5.75    4.28   1.34 SOBRE   60.12   80.62      9
sin_anotacion          0.21    0.00    0.00   0.04 azar     0.00    0.00   1.18 azar     0.08    0.00      0
-- SALIDA motor [>=1] | n=110 | con_entrada=110 | sinapsis_entrada=244929 | suma_D2=0.9983 | empates=0
clase                 fila%     D1%  nulo1%   enr1 flag1     D2%  nulo2%   enr2 flag2 cobert%    exc% domina
ascending              0.91    6.92    1.87   3.69 SOBRE   10.55    1.92   5.48 SOBRE   84.55   65.41      2
central                0.83   64.34   25.18   2.55 SOBRE   62.56   23.96   2.61 SOBRE  100.00   43.72     90
descending             5.85   21.48    1.04  20.67 SOBRE   15.01    0.97  15.45 SOBRE   92.73   57.66     17
endocrine              1.54    0.15    0.00  65.25 azar     0.10    0.00  36.60 SOBRE    4.55  100.00      0
motor                 28.87    1.03    0.01  82.62 SOBRE    0.86    0.02  55.08 SOBRE   93.64   55.87      0
optic                  0.00    0.00   61.57   0.00 BAJO     0.37   59.91   0.01 BAJO     3.64    0.00      0
sensory                0.59    3.57    3.45   1.03 azar     7.41    5.24   1.41 azar    77.27   86.74      0
sensory_ascending      4.79    1.48    0.25   6.00 azar     1.31    0.22   6.00 azar    37.27   63.16      1
visual_centrifugal     0.00    0.03    2.74   0.01 BAJO     0.32    3.17   0.10 BAJO    14.55   80.60      0
visual_projection      0.04    1.01    3.89   0.26 BAJO     1.35    4.26   0.32 BAJO    24.55   57.23      0
sin_anotacion          0.00    0.00    0.00   0.00 azar     0.00    0.00   0.03 BAJO     0.00     nan      0
-- SALIDA endocrine [>=1] | n=76 | con_entrada=73 | sinapsis_entrada=24045 | suma_D2=0.9999 | empates=0
clase                 fila%     D1%  nulo1%   enr1 flag1     D2%  nulo2%   enr2 flag2 cobert%    exc% domina
ascending              0.21   15.93    1.86   8.57 SOBRE   11.40    1.91   5.95 SOBRE   93.42   51.55      7
central                0.09   73.03   25.15   2.90 SOBRE   73.30   23.93   3.06 SOBRE   96.05   54.67     62
descending             0.17    4.37    1.02   4.30 SOBRE    6.69    0.96   6.94 SOBRE   64.47   50.89      0
endocrine              7.70    0.69    0.00 289.17 SOBRE    1.02    0.00 369.60 SOBRE   50.00  100.00      0
motor                  0.04    0.02    0.01   1.80 azar     0.03    0.02   1.81 azar     6.58  100.00      0
optic                  0.00    0.00   61.64   0.00 BAJO     0.16   59.98   0.00 BAJO     0.00     nan      0
sensory                0.08    4.27    3.44   1.24 azar     5.41    5.22   1.04 azar    27.63  100.00      4
sensory_ascending      0.75    1.31    0.25   5.33 azar     1.16    0.22   5.34 azar    38.16   19.63      0
visual_centrifugal     0.00    0.00    2.74   0.00 BAJO     0.13    3.17   0.04 BAJO     0.00     nan      0
visual_projection      0.00    0.37    3.89   0.10 BAJO     0.72    4.27   0.17 BAJO    13.16  100.00      0
sin_anotacion          0.00    0.00    0.00   0.00 azar     0.00    0.00   0.00 BAJO     0.00     nan      0
== VARIANTE >=5 sinapsis | aristas=2700513 | sinapsis=34153566 | neuronas_con_entrada=125192 ==
-- SALIDA descending [>=5] | n=1299 | con_entrada=1262 | sinapsis_entrada=1808864 | suma_D2=0.9473 | empates=8
clase                 fila%     D1%  nulo1%   enr1 flag1     D2%  nulo2%   enr2 flag2 cobert%    exc% domina
ascending             19.00   13.62    1.72   7.90 SOBRE   12.67    1.92   6.60 SOBRE   82.68   58.07     81
central                8.38   62.42   26.97   2.31 SOBRE   58.40   24.54   2.38 SOBRE   95.15   50.39   1000
descending            39.27   14.43    0.82  17.52 SOBRE    9.82    0.76  12.89 SOBRE   75.90   57.58    125
endocrine             32.49    0.01    0.00   5.69 azar     0.01    0.00   4.17 azar     0.15  100.00      0
motor                  0.95    0.00    0.00   0.99 azar     0.02    0.01   4.56 SOBRE    0.77   51.58      0
optic                  0.03    0.33   61.55   0.01 BAJO     2.71   57.53   0.05 BAJO     4.46   12.70      0
sensory                7.07    3.43    2.40   1.43 SOBRE    3.82    5.46   0.70 BAJO    23.63   99.54     32
sensory_ascending      8.00    0.88    0.12   7.55 SOBRE    0.70    0.11   6.35 SOBRE    8.55   75.56      5
visual_centrifugal     1.03    0.51    3.28   0.16 BAJO     0.89    3.48   0.26 BAJO    12.78   52.89      0
visual_projection      5.20    4.37    3.13   1.40 SOBRE    5.68    4.01   1.42 SOBRE   36.72   79.83     11
sin_anotacion          0.00    0.00    0.00   0.00 azar     0.00    0.00   2.93 azar     0.00     nan      0
-- SALIDA motor [>=5] | n=110 | con_entrada=109 | sinapsis_entrada=223047 | suma_D2=0.9551 | empates=0
clase                 fila%     D1%  nulo1%   enr1 flag1     D2%  nulo2%   enr2 flag2 cobert%    exc% domina
ascending              0.93    6.62    1.72   3.86 SOBRE    9.19    1.92   4.78 SOBRE   70.91   63.55      3
central                1.12   65.54   27.04   2.42 SOBRE   62.93   24.59   2.56 SOBRE   97.27   43.81     88
descending             7.21   21.89    0.83  26.45 SOBRE   14.10    0.76  18.46 SOBRE   80.91   56.72     17
endocrine              0.00    0.00    0.00   0.00 azar     0.00    0.00   0.39 azar     0.00     nan      0
motor                 35.38    0.68    0.00 144.89 SOBRE    0.57    0.01 103.45 SOBRE   29.09   50.37      0
optic                  0.00    0.00   61.47   0.00 BAJO     0.27   57.46   0.00 BAJO     0.00     nan      0
sensory                0.70    3.15    2.41   1.30 azar     6.15    5.48   1.12 azar    53.64   84.74      0
sensory_ascending      4.83    1.03    0.12   8.81 azar     0.66    0.11   6.00 azar    16.36   49.81      1
visual_centrifugal     0.00    0.01    3.28   0.00 BAJO     0.29    3.48   0.08 BAJO     3.64  100.00      0
visual_projection      0.06    1.08    3.13   0.35 azar     1.35    4.00   0.34 BAJO    14.55   52.69      0
sin_anotacion          0.00    0.00    0.00   0.00 azar     0.00    0.00   0.04 azar     0.00     nan      0
-- SALIDA endocrine [>=5] | n=76 | con_entrada=69 | sinapsis_entrada=16410 | suma_D2=0.9316 | empates=1
clase                 fila%     D1%  nulo1%   enr1 flag1     D2%  nulo2%   enr2 flag2 cobert%    exc% domina
ascending              0.21   20.31    1.73  11.71 SOBRE   11.83    1.93   6.14 SOBRE   72.37   49.01     10
central                0.08   67.88   27.00   2.51 SOBRE   66.46   24.55   2.71 SOBRE   86.84   51.87     54
descending             0.16    4.31    0.83   5.21 SOBRE    7.33    0.76   9.61 SOBRE   35.53   48.04      0
endocrine              0.00    0.00    0.00   0.00 azar     2.33    0.00 614.45 SOBRE    0.00     nan      0
motor                  0.00    0.00    0.00   0.00 azar     0.00    0.01   0.00 azar     0.00     nan      0
optic                  0.00    0.00   61.49   0.00 BAJO     0.01   57.49   0.00 BAJO     0.00     nan      0
sensory                0.10    6.16    2.39   2.57 azar     3.95    5.47   0.72 azar    15.79  100.00      4
sensory_ascending      0.86    1.24    0.12  10.63 azar     0.79    0.11   7.08 azar    13.16   12.59      0
visual_centrifugal     0.00    0.00    3.28   0.00 BAJO     0.01    3.48   0.00 BAJO     0.00     nan      0
visual_projection      0.00    0.11    3.14   0.04 BAJO     0.44    4.01   0.11 BAJO     5.26  100.00      0
sin_anotacion          0.00    0.00    0.00   0.00 azar     0.00    0.00   0.00 azar     0.00     nan      0
CHEQUEO mapeo_biyectivo=True indice_es_rango_ordenado=True autolazos=0
CRUCE_TABLA7 PASS sin_umbral_igual=True umbral_5_igual=True clases_igual=True max_dif_sin_umbral=0 max_dif_umbral_5=0 json=results/table7_reconstruida_2026-10-10/table7_reciprocity_by_class.json json_md5=6e395935380145ad429924957c09d649
SUMA_D1 max_desvio_>=1=2.220e-16 max_desvio_>=5=2.220e-16 OK=True
UMBRAL5_ARISTAS 2700513 erratum_item5=2700513 igual=True
CONTROL_NEGATIVO [>=1] flags_permutado=8/242 tolerancia=12.1 flags_reales=70/242 OK=True
CONTROL_NEGATIVO [>=5] flags_permutado=6/231 tolerancia=11.6 flags_reales=47/231 OK=True
JSON results/output_control_2026-10-10/output_control_by_class.json md5=6f76578ab8f8e1ed5f1da005f559118e
VEREDICTO_MEDICION PASS
FIN_SALIDAS segundos=58.8
```

Detalle de los flags del control negativo, leído del JSON. El segundo campo es el índice de la clase permutada en `clases_orden` (0 ascending, 1 central, 2 descending, 3 endocrine, 4 motor, 5 optic, 6 sensory, 7 sensory_ascending, 8 visual_centrifugal, 9 visual_projection, 10 sin_anotacion):

```
>=1 ['descending', 0, 'SOBRE', 1.2884625933827005]
>=1 ['descending', 3, 'BAJO', 0.404234265386786]
>=1 ['motor', 8, 'BAJO', 0.10748208441724631]
>=1 ['endocrine:lNSC_unknown', 1, 'BAJO', 0.5924346353432439]
>=1 ['endocrine:lNSC_unknown', 2, 'BAJO', 0.0]
>=1 ['endocrine:DH44', 6, 'BAJO', 0.2408000280872199]
>=1 ['endocrine:Hugin-RG', 0, 'SOBRE', 23.151707763210233]
>=1 ['endocrine:Hugin-RG', 6, 'BAJO', 0.19645570064897075]
>=5 ['descending', 8, 'BAJO', 0.3831241749094223]
>=5 ['descending', 9, 'BAJO', 0.8292643655812163]
>=5 ['endocrine', 0, 'SOBRE', 4.161764760419726]
>=5 ['endocrine:IPC', 1, 'BAJO', 0.2727705441110765]
>=5 ['endocrine:lNSC_unknown', 0, 'SOBRE', 19.708969394606235]
>=5 ['endocrine:DH31', 4, 'SOBRE', 150.91263780899212]
```

Tests (`results/output_control_2026-10-10/tests.log`):

```
TEST test_vectorizado_igual_fuerza_bruta -> vectorizado == fuerza bruta (3 grafos x 2 umbrales, D1 D2 cobertura fila exc domina empates)
TEST test_matriz_aristas_contra_conteo_directo -> matriz clase x clase == conteo directo, y una arista de mas la pone en rojo
TEST test_banderas_plantado_y_plano -> nulo plano -> azar x3; plantado -> SOBRE/BAJO/BAJO; NaN -> NA
TEST test_control_negativo_sin_senal_y_real_con_senal -> plantado clase0->O da SOBRE; con etiquetas permutadas flags=0/3
TEST test_extremo_a_extremo -> extremo a extremo con parquet y TSV chicos, 2 nodos sin anotar, D1 == fuerza bruta
TESTS_OK 5
```

## 5. Archivos generados

- Rama `titan/tabla7-reconstruida-2026-10-10`, commit `7e75cde988dad221f3194e64247ee9d833ee7a05`:
  - `tools/output_control_by_class.py`
  - `tests/test_output_control_by_class.py`
  - `results/output_control_2026-10-10/run.log`
  - `results/output_control_2026-10-10/tests.log`
- Sólo en brain-env: `results/output_control_2026-10-10/output_control_by_class.json` (285.283 B, md5 arriba). No se sube: es un derivado grande, y brain-env no tiene credencial de push para este repo.
- `main`: esta respuesta y el diff de `docs/agents/CONTEXTO-drosophila-fep.md`.
- Doc de ClickUp: https://app.clickup.com/90171457413/docs/2kza6fw5-20877

## 6. NO MEDIDO

- Nulo por permutación de etiquetas de origen con R ≥ 500. Es el que corrige el ~3% de falsos del nulo de destinos al azar.
- Qué hace cada descendente en el cuerpo: el cordón ventral no está en FlyWire. Los tipos más alimentados por cada clase están en el log (`DN_TOP`); su función es literatura, no medición.
- Signo real: `Excitatory` es ±1 por neurotransmisor predicho, según el modelo de origen. Moduladores y glutamato no se distinguen.
- Tres saltos o más, dinámica y causalidad.
- Significancia en subclases de 2 a 14 neuronas.

## La 004, en corto (lo que pediste repetir)

- El 1% de las neuronas (1.485: descendentes, motoras y neurosecretoras) recibe el 2,37% de los cables: el 97,6% del cableado queda adentro del cerebro.
- El central da el 61% de lo que les llega a las descendentes.
- La ida y vuelta está donde se procesa (intra-óptico 31,98%, intra-central 26,00%) y casi no en la salida: descendente → motora con ≥5 tiene 2 recíprocas en 1.569 (0,13%).
- El cuerpo vuelve por las ascendentes: 1.736 neuronas, el 68% de sus cables al central.
- Archivo: `docs/agents/respuestas/2026-10-10-004-que-hay-al-final-de-cada-cable.md`; Doc: https://app.clickup.com/90171457413/docs/2kza6fw5-20857

--- METODO PROMETEO ---
Máquina:     brain-env (corrida real, tests y verificación md5 post-push); sandbox para escribir y testear
Artefactos:  docs/agents/respuestas/2026-10-10-005-que-salida-controla-cada-clase.md + https://app.clickup.com/90171457413/docs/2kza6fw5-20877
