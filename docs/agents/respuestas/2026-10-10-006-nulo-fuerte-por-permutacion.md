# 2026-10-10-006 · Nulo fuerte por permutación de etiquetas para la 005 (R = 10.000)

**Veredicto (F-01): medido, `VEREDICTO_NULO PASS`.** Dos nulos de 10.000 permutaciones cada uno (el pedido era 500 o más), en los dos umbrales. La 005 se sostiene en lo grueso, pero el central gana por menos: ×1,63 / ×1,86 / ×2,29 sobre neuronas del mismo tamaño (sin umbral; descendentes / motoras / neurosecretoras), contra ×2,58 / ×2,75 / ×3,13 con la permutación plana. Descendentes → motoras ×20, intacto; ascendentes → neurosecretoras ×10; la insulina (IPC) se cae; la proyección visual llega a las descendentes por debajo del azar (×0,68 / ×0,64) y lo sensorial a las descendentes es exactamente azar (×0,96 / ×1,04). La primera corrida dio FAIL por un chequeo mío mal armado (z infinito con desvío 0), no por el nulo; la segunda, con las mismas semillas, da los mismos resultados y PASS.

## 1. Pedido

"Run the stronger 500+ permutation null" (Abraham, 2026-10-10). Es el nulo por permutación de etiquetas de origen que la 005 dejó NO MEDIDO: el nulo de destinos al azar de la 005 marcaba ~3% de falsos (8/242 y 6/231).

## 2. Herramientas

- **brain-env** (gateway `build/run`): tests, las dos corridas completas (778–779 s cada una), diagnóstico de falsos, md5 y verificación de cada push con `git fetch` + `md5sum`.
- **Sandbox de Brain:** escritura y tests del código antes de tocar datos reales.
- **GitHub MCP:** rama `titan/tabla7-reconstruida-2026-10-10` (commit `c99494fd9f0cf20d30ac37061b069361b2d222ba`, PR #26, sin merge) y este archivo en `main`.
- **ClickUp:** Doc público https://app.clickup.com/90171457413/docs/2kza6fw5-20897

## 3. Qué se midió

D1(C,O) = media, sobre las neuronas del conjunto de salida O, de la fracción de sus sinapsis de entrada que vienen de la clase C (la misma cantidad de la 005). D2 = lo mismo a través de un intermediario. 22 conjuntos: 3 de nivel 1 (descending, motor, endocrine) y 19 finos (subclases motoras y tipos endocrinos). Se calcula con u1 = A·t_O, u2 = A·u1 y D = one-hot(etiquetas)·U: barajar etiquetas no toca el grafo.

Dos nulos, R = 10.000 cada uno, semilla 20261011, flag con p ≤ 0,001:

- **perm:** barajado plano de las etiquetas de clase (conserva el tamaño de cada clase).
- **estr (el fuerte):** barajado dentro de estratos de fuerza de salida hacia neuronas que no son de salida, de ancho igual en log1p (ancho = log1p(máx)/100): 86 estratos sin umbral y 80 con ≥5 (factor ×1,12 por estrato). Una clase de neuronas grandes no gana por ser grande.

Chequeos, todos en el log: CRUCE_005 (D1 y D2 reproducen la 005, error ≤ 1e-12); conteos y estratos conservados en cada permutación; MEDIA_NULO (z contra la esperanza exacta con la varianza exacta de permutación, ≤ 6); VARIANZA_NULO (mediana de var empírica / var exacta entre 0,9 y 1,1); CONTROL_NEGATIVO (20 etiquetados falsos sacados del mismo nulo, flags ≤ máx(3, 3 × esperado)); R_PEDIDO_500 (R < 500 da INCOMPLETO).

### Resultado (nulo estr; × = D1 / media del nulo; sin umbral / ≥5; ▲ SOBRE, ▼ BAJO)

| clase | descending | motor | endocrine |
|---|---|---|---|
| central | ×1,63 ▲ / ×1,53 ▲ | ×1,86 ▲ / ×1,72 ▲ | ×2,29 ▲ / ×2,03 ▲ |
| descending | ×15,09 ▲ / ×13,97 ▲ | ×19,96 ▲ / ×20,01 ▲ | ×4,92 azar / ×5,00 azar |
| ascending | ×5,61 ▲ / ×5,15 ▲ | ×3,45 ▲ / ×2,80 ▲ | ×10,24 ▲ / ×10,48 ▲ |
| sensory_ascending | ×10,87 ▲ / ×7,21 ▲ | ×7,85 ▲ / ×5,90 azar | ×9,52 azar / ×8,50 azar |
| sensory | ×0,96 azar / ×1,04 azar | ×0,60 ▼ / ×0,68 azar | ×1,10 azar / ×1,56 azar |
| visual_projection | ×0,68 ▼ / ×0,64 ▼ | ×0,15 ▼ / ×0,16 ▼ | ×0,05 ▼ / ×0,02 ▼ |
| visual_centrifugal | ×0,47 ▼ / ×0,34 ▼ | ×0,03 ▼ / ×0,01 ▼ | ×0,00 ▼ / ×0,00 azar |
| optic | ×0,01 ▼ / ×0,01 ▼ | ×0,00 ▼ / ×0,00 ▼ | ×0,00 ▼ / ×0,00 ▼ |

La columna sin umbral está verbatim abajo (líneas 13–51 de `run.log`). La columna ≥5 sale de las líneas 134–227 de `run.log`, que no copio acá; el archivo está en la rama con md5 verificado. Media del nulo estr para el central: 37,04 / 34,64 / 31,82% sin umbral (40,79 / 38,09 / 33,36% con ≥5).

### Qué cambió respecto de la 005

- Sin umbral: se mantienen 60 flags, cambian 10 y aparecen 44. Con ≥5: 38, 9 y 26.
- Se caen a azar: descending → endocrine (×4,92 / ×5,00); ascending → IPC (×7,72 / ×8,08); central → lNSC (sin umbral, ×2,11); motor → motor:sin_subclase (sin umbral) y motor → motor (≥5); endocrine → Hugin-RG (sin umbral).
- Se dan vuelta con ≥5: visual_projection → descending pasa de ▲ a ▼; sensory → descending pasa de ▲ a azar.
- Los ▼ de visual_centrifugal pasan a azar en conjuntos chicos (5 sin umbral, 4 con ≥5).
- Nuevos y firmes en los dos umbrales: central → motoras de antena, ojo y haustelo; descending → motoras del ojo (×13,78 / ×14,04) y del haustelo (×11,78 / ×9,63); ascending → motoras de antena (×6,48 / ×6,98); sensory → motoras de ingestión (×4,65 / ×4,20); optic y visual_projection ▼ en los conjuntos chicos de la zona subesofágica.

### La primera corrida dio FAIL, y era culpa del chequeo

La v1 (mismas semillas) terminó `VEREDICTO_NULO FAIL` por `media_perm_>=1=False`: z = inf. La z usaba el desvío empírico del nulo, que fue 0 en un evento raro (sin_anotacion → ITP: un solo presináptico; ninguna de las 10.000 permutaciones lo tocó). Arreglo: varianza exacta de permutación, chequeo VARIANZA_NULO nuevo y test de regresión `test_evento_raro_no_da_infinito`. El diff v1 → v2 del log tiene sólo 8 líneas distintas (11, 12, 132, 133 y 246–249): tiempos y chequeos; las 241 restantes son idénticas. Antes de tocar datos reales, una primera versión de estratos por cuantiles falló el test de confusión por tamaño (juntaba fuerza 3 con 25) y la cambié a ancho igual en log.

Que perm y estr den el mismo número de falsos en el control negativo (7 y 4) es casualidad: `diag_falsos` mide 0 etiquetados idénticos y 38,51% de etiqueta compartida, igual al azar (38,48%).

## 4. Evidencia cruda verbatim

`run.log`, líneas 1–60:

```text
== output_control_permutation_null.py :: nulo por permutacion de etiquetas para la 005 ==
ENTORNO python=3.12.14 numpy=2.5.3 scipy=1.18.1 maquina=brain-env
PARAMETROS seed=20261011 r=10000 n_falsos=20 n_estratos=100 p_flag=0.001 z_max=6 factor_control=3
INPUT parquet /workspace/connectivity.parquet md5=3d802fd542b5d18570ba1ba0bb0abed9 pin_ok=True
INPUT annotations /workspace/annotations.tsv md5=719904abad876c68ace1b5690c9b9b63 pin_ok=True
INPUT json_005 results/output_control_2026-10-10/output_control_by_class.json md5=6f76578ab8f8e1ed5f1da005f559118e
GRAFO n_nodos=138639 n_aristas=15091983 mapeo_biyectivo=True sinapsis_total=54492922
CLASES ascending=1736 central=32379 descending=1299 endocrine=76 motor=110 optic=77530 sensory=16352 sensory_ascending=581 visual_centrifugal=524 visual_projection=8038 sin_anotacion=14
CONJUNTOS 22 (nivel1 3 + finos 19) neuronas_de_salida=1485
== VARIANTE >=1 | conjuntos_con_entrada=22/22 | estratos=86 tam_min=1 tam_max=7710 fuerza_max=99864 ancho_log=0.1151 factor=1.122 ==
NULO [>=1] perm R=10000 segundos=184.4 conteos_ok=True estratos_ok=True media_max_z=3.64 var_ratio_mediana=0.9990
NULO [>=1] estr R=10000 segundos=183.0 conteos_ok=True estratos_ok=True media_max_z=2.81 var_ratio_mediana=1.0000
-- NIVEL1 descending [>=1] | con_entrada=1299
clase                   D1% 005     perm%   enrP perm    estr%   enrE estr      D2% 005_2  enrE2 estr2
ascending             12.98 SOBRE    1.25  10.35 SOBRE    2.31   5.61 SOBRE   12.71 SOBRE   5.21 SOBRE
central               60.23 SOBRE   23.34   2.58 SOBRE   37.04   1.63 SOBRE   59.77 SOBRE   1.51 SOBRE
descending            15.17 SOBRE    0.94  16.19 SOBRE    1.01  15.09 SOBRE   10.47 SOBRE  10.72 SOBRE
endocrine              0.01 azar     0.06   0.22 azar     0.01   1.12 azar     0.02 SOBRE   3.00 azar 
motor                  0.06 azar     0.08   0.72 azar     0.04   1.50 azar     0.09 SOBRE   2.67 azar 
optic                  0.45 BAJO    55.92   0.01 BAJO    46.96   0.01 BAJO     3.64 BAJO    0.08 BAJO 
sensory                4.28 azar    11.80   0.36 BAJO     4.46   0.96 azar     4.91 azar    1.41 SOBRE
sensory_ascending      1.62 SOBRE    0.42   3.87 SOBRE    0.15  10.87 SOBRE    1.54 SOBRE  13.66 SOBRE
visual_centrifugal     0.58 BAJO     0.38   1.54 azar     1.25   0.47 BAJO     0.95 BAJO    0.57 BAJO 
visual_projection      4.61 azar     5.80   0.79 BAJO     6.77   0.68 BAJO     5.75 SOBRE   0.83 BAJO 
sin_anotacion          0.00 azar     0.01   0.00 azar     0.00   0.01 azar     0.00 azar    0.70 azar 
-- NIVEL1 motor [>=1] | con_entrada=110
clase                   D1% 005     perm%   enrP perm    estr%   enrE estr      D2% 005_2  enrE2 estr2
ascending              6.92 SOBRE    1.26   5.50 SOBRE    2.01   3.45 SOBRE   10.55 SOBRE   4.31 SOBRE
central               64.34 SOBRE   23.40   2.75 SOBRE   34.64   1.86 SOBRE   62.56 SOBRE   1.55 SOBRE
descending            21.48 SOBRE    0.93  23.03 SOBRE    1.08  19.96 SOBRE   15.01 SOBRE  14.29 SOBRE
endocrine              0.15 azar     0.06   2.68 azar     0.01  10.85 SOBRE    0.10 SOBRE  12.58 SOBRE
motor                  1.03 SOBRE    0.08  12.78 SOBRE    0.05  22.86 SOBRE    0.86 SOBRE  21.66 SOBRE
optic                  0.00 BAJO    55.86   0.00 BAJO    48.50   0.00 BAJO     0.37 BAJO    0.01 BAJO 
sensory                3.57 azar    11.80   0.30 BAJO     5.95   0.60 BAJO     7.41 azar    2.02 SOBRE
sensory_ascending      1.48 azar     0.42   3.52 azar     0.19   7.85 SOBRE    1.31 azar   11.33 SOBRE
visual_centrifugal     0.03 BAJO     0.38   0.07 azar     0.79   0.03 BAJO     0.32 BAJO    0.24 BAJO 
visual_projection      1.01 BAJO     5.81   0.17 BAJO     6.79   0.15 BAJO     1.35 BAJO    0.20 BAJO 
sin_anotacion          0.00 azar     0.01   0.00 azar     0.00   0.00 azar     0.00 BAJO    0.02 azar 
-- NIVEL1 endocrine [>=1] | con_entrada=73
clase                   D1% 005     perm%   enrP perm    estr%   enrE estr      D2% 005_2  enrE2 estr2
ascending             15.93 SOBRE    1.25  12.74 SOBRE    1.56  10.24 SOBRE   11.40 SOBRE   5.88 SOBRE
central               73.03 SOBRE   23.32   3.13 SOBRE   31.82   2.29 SOBRE   73.30 SOBRE   2.02 SOBRE
descending             4.37 SOBRE    0.93   4.71 azar     0.89   4.92 azar     6.69 SOBRE   6.75 SOBRE
endocrine              0.69 SOBRE    0.05  12.74 azar     0.01 116.11 SOBRE    1.02 SOBRE 126.82 SOBRE
motor                  0.02 azar     0.08   0.26 azar     0.03   0.79 azar     0.03 azar    0.93 azar 
optic                  0.00 BAJO    55.92   0.00 BAJO    53.59   0.00 BAJO     0.16 BAJO    0.00 BAJO 
sensory                4.27 azar    11.82   0.36 BAJO     3.90   1.10 azar     5.41 azar    1.69 azar 
sensory_ascending      1.31 azar     0.43   3.05 azar     0.14   9.52 azar     1.16 azar   10.33 SOBRE
visual_centrifugal     0.00 BAJO     0.38   0.00 azar     0.65   0.00 BAJO     0.13 BAJO    0.13 BAJO 
visual_projection      0.37 BAJO     5.80   0.06 BAJO     7.41   0.05 BAJO     0.72 BAJO    0.10 BAJO 
sin_anotacion          0.00 azar     0.01   0.00 azar     0.00   0.00 azar     0.00 BAJO    0.00 azar 
-- FINAS [>=1] (D1, top 3; flags 005 / perm / estr; x = D1 / media estr) --
FINA [>=1] motor:ingestion_motor_neuron             con_entrada=  28 : central 83.66% 005=SOBRE perm=SOBRE estr=SOBRE x1.91 | descending 6.38% 005=SOBRE perm=SOBRE estr=SOBRE x5.71 | sensory 6.03% 005=azar perm=azar estr=SOBRE x4.65
FINA [>=1] motor:neck_motor_neuron                  con_entrada=  26 : central 40.15% 005=azar perm=SOBRE estr=SOBRE x1.69 | descending 39.96% 005=SOBRE perm=SOBRE estr=SOBRE x37.31 | ascending 9.98% 005=SOBRE perm=SOBRE estr=SOBRE x6.32
FINA [>=1] motor:proboscis_motor_neuron             con_entrada=  24 : central 68.85% 005=SOBRE perm=SOBRE estr=SOBRE x1.78 | descending 24.72% 005=SOBRE perm=SOBRE estr=SOBRE x22.31 | ascending 4.04% 005=azar perm=azar estr=azar x1.96
FINA [>=1] motor:antennal_motor_neuron              con_entrada=  10 : central 50.52% 005=azar perm=SOBRE estr=SOBRE x1.67 | descending 32.06% 005=SOBRE perm=SOBRE estr=SOBRE x34.31 | ascending 13.41% 005=azar perm=SOBRE estr=SOBRE x6.48
FINA [>=1] motor:crop_motor_neuron                  con_entrada=   8 : central 86.42% 005=SOBRE perm=SOBRE estr=SOBRE x2.42 | sensory 12.42% 005=azar perm=azar estr=azar x7.12 | motor 0.77% 005=azar perm=azar estr=azar x42.73
FINA [>=1] motor:eye_motor_neuron                   con_entrada=   4 : central 78.09% 005=azar perm=SOBRE estr=SOBRE x2.12 | descending 13.63% 005=azar perm=SOBRE estr=SOBRE x13.78 | ascending 3.82% 005=azar perm=azar estr=azar x1.69
FINA [>=1] motor:haustellum_motor_neuron            con_entrada=   4 : central 74.46% 005=azar perm=SOBRE estr=SOBRE x2.32 | descending 12.10% 005=azar perm=SOBRE estr=SOBRE x11.78 | ascending 8.53% 005=azar perm=azar estr=azar x5.98
FINA [>=1] motor:sin_subclase                       con_entrada=   4 : ascending 42.45% 005=SOBRE perm=SOBRE estr=SOBRE x20.96 | descending 28.08% 005=SOBRE perm=SOBRE estr=SOBRE x18.31 | central 20.11% 005=azar perm=azar estr=azar x0.85
```

`run.log`, líneas 126–133 y 228–232:

```text
RESUMEN [>=1] D1 tests=242 | 005 SOBRE=40 BAJO=30 | perm SOBRE=44 BAJO=49 | estr SOBRE=55 BAJO=49 | 005->estr se_mantienen=60 cambian=10 nuevos=44
RESUMEN [>=1] D2 tests=242 | 005 SOBRE=49 BAJO=48 | perm SOBRE=65 BAJO=66 | estr SOBRE=85 BAJO=62
CRUCE_005 [>=1] PASS max_dif=6.5503158452884236e-15 faltan=0 n_con_entrada_distinto=0
CONTROL_NEGATIVO [>=1] perm flags=7/4840 esperado=9.68 tope=29.04 OK=True
CONTROL_NEGATIVO [>=1] estr flags=7/4840 esperado=9.68 tope=29.04 OK=True
== VARIANTE >=5 | conjuntos_con_entrada=21/22 | estratos=80 tam_min=1 tam_max=9777 fuerza_max=92952 ancho_log=0.1144 factor=1.121 ==
NULO [>=5] perm R=10000 segundos=184.2 conteos_ok=True estratos_ok=True media_max_z=2.77 var_ratio_mediana=0.9985
NULO [>=5] estr R=10000 segundos=182.4 conteos_ok=True estratos_ok=True media_max_z=3.24 var_ratio_mediana=1.0024
RESUMEN [>=5] D1 tests=231 | 005 SOBRE=29 BAJO=18 | perm SOBRE=33 BAJO=36 | estr SOBRE=33 BAJO=32 | 005->estr se_mantienen=38 cambian=9 nuevos=26
RESUMEN [>=5] D2 tests=231 | 005 SOBRE=34 BAJO=40 | perm SOBRE=50 BAJO=56 | estr SOBRE=58 BAJO=56
CRUCE_005 [>=5] PASS max_dif=2.6645352591003757e-15 faltan=0 n_con_entrada_distinto=0
CONTROL_NEGATIVO [>=5] perm flags=4/4620 esperado=9.24 tope=27.72 OK=True
CONTROL_NEGATIVO [>=5] estr flags=4/4620 esperado=9.24 tope=27.72 OK=True
```

`run.log`, líneas 237–239 y 242–249 (las 234–236, 240 y 241 son largas y están completas en el archivo):

```text
QUE_CONTROLA_FIRME endocrine: SOBRE: ninguna | BAJO nivel1: ninguna
QUE_CONTROLA_FIRME motor: SOBRE: motor:ingestion_motor_neuron x91.81/x67.05 (D1 2.60/2.32%) | BAJO nivel1: ninguna
QUE_CONTROLA_FIRME optic: SOBRE: ninguna | BAJO nivel1: descending, motor, endocrine
QUE_CONTROLA_FIRME visual_centrifugal: SOBRE: ninguna | BAJO nivel1: descending, motor
QUE_CONTROLA_FIRME visual_projection: SOBRE: ninguna | BAJO nivel1: descending, motor, endocrine
QUE_CONTROLA_FIRME sin_anotacion: SOBRE: ninguna | BAJO nivel1: ninguna
R_PEDIDO_500 r=10000 ok=True
CHEQUEOS mapeo=True conteos_perm_>=1=True estratos_perm_>=1=True media_perm_>=1=True varianza_perm_>=1=True control_perm_>=1=True conteos_estr_>=1=True estratos_estr_>=1=True media_estr_>=1=True varianza_estr_>=1=True control_estr_>=1=True conteos_perm_>=5=True estratos_perm_>=5=True media_perm_>=5=True varianza_perm_>=5=True control_perm_>=5=True conteos_estr_>=5=True estratos_estr_>=5=True media_estr_>=5=True varianza_estr_>=5=True control_estr_>=5=True
JSON results/output_control_permnull_2026-10-10/output_control_permutation_null.json md5=ec64172711d7d18040f6f09335d7521b
VEREDICTO_NULO PASS
FIN_NULO segundos=778.0
```

Diff `run_v1_media_inf.log` → `run.log` (salida completa de `diff`):

```text
11,12c11,12
< NULO [>=1] perm R=10000 segundos=183.6 conteos_ok=True estratos_ok=True media_max_z=inf
< NULO [>=1] estr R=10000 segundos=182.4 conteos_ok=True estratos_ok=True media_max_z=2.84
---
> NULO [>=1] perm R=10000 segundos=184.4 conteos_ok=True estratos_ok=True media_max_z=3.64 var_ratio_mediana=0.9990
> NULO [>=1] estr R=10000 segundos=183.0 conteos_ok=True estratos_ok=True media_max_z=2.81 var_ratio_mediana=1.0000
132,133c132,133
< NULO [>=5] perm R=10000 segundos=186.6 conteos_ok=True estratos_ok=True media_max_z=5.92
< NULO [>=5] estr R=10000 segundos=184.6 conteos_ok=True estratos_ok=True media_max_z=4.13
---
> NULO [>=5] perm R=10000 segundos=184.2 conteos_ok=True estratos_ok=True media_max_z=2.77 var_ratio_mediana=0.9985
> NULO [>=5] estr R=10000 segundos=182.4 conteos_ok=True estratos_ok=True media_max_z=3.24 var_ratio_mediana=1.0024
246,249c246,249
< CHEQUEOS mapeo=True conteos_perm_>=1=True estratos_perm_>=1=True media_perm_>=1=False control_perm_>=1=True conteos_estr_>=1=True estratos_estr_>=1=True media_estr_>=1=True control_estr_>=1=True conteos_perm_>=5=True estratos_perm_>=5=True media_perm_>=5=True control_perm_>=5=True conteos_estr_>=5=True estratos_estr_>=5=True media_estr_>=5=True control_estr_>=5=True
< JSON results/output_control_permnull_2026-10-10/output_control_permutation_null.json md5=5e4abc205d7acf11510b5e9bad149b1e
< VEREDICTO_NULO FAIL
< FIN_NULO segundos=779.4
---
> CHEQUEOS mapeo=True conteos_perm_>=1=True estratos_perm_>=1=True media_perm_>=1=True varianza_perm_>=1=True control_perm_>=1=True conteos_estr_>=1=True estratos_estr_>=1=True media_estr_>=1=True varianza_estr_>=1=True control_estr_>=1=True conteos_perm_>=5=True estratos_perm_>=5=True media_perm_>=5=True varianza_perm_>=5=True control_perm_>=5=True conteos_estr_>=5=True estratos_estr_>=5=True media_estr_>=5=True varianza_estr_>=5=True control_estr_>=5=True
> JSON results/output_control_permnull_2026-10-10/output_control_permutation_null.json md5=ec64172711d7d18040f6f09335d7521b
> VEREDICTO_NULO PASS
> FIN_NULO segundos=778.0
```

`tests.log`:

```text
TEST test_u_igual_fuerza_bruta_y_005 -> D1 y D2 por vectores u == fuerza bruta == medir() de la 005 (3 grafos x 2 umbrales)
TEST test_permutador_conserva_conteos_y_los_brazos_difieren -> perm conserva clases; estr conserva clases por estrato; perm NO conserva estratos
TEST test_esperanza_exacta_y_control_negativo -> media y varianza del nulo == formulas exactas (max z 2.73 / 1.66); 5% de error en la media o 50% en la varianza lo ponen en rojo; control OK
TEST test_evento_raro_no_da_infinito -> clase de 2 neuronas y un solo presinaptico: el nulo nunca lo toca y z = 0.28 (antes daba infinito)
TEST test_plantado_sobre_en_los_dos_nulos -> clase 0 que alimenta sola a O: SOBRE con perm y con estr
TEST test_confusion_por_tamano_perm_cae_estr_no -> neuronas grandes con destinos al azar: perm=SOBRE, estr=azar
TEST test_extremo_a_extremo_contra_la_005 -> extremo a extremo: cruce con la 005 PASS, R=300 da INCOMPLETO, un D1 movido 1e-6 da FAIL
TESTS_OK 7
```

`diag_falsos.log`:

```text
DIAG_FALSOS umbral=1 falsos=20 identicos_perm_estr=0 misma_etiqueta perm-estr=0.3851 perm-real=0.3850 estr-real=0.4655 esperado_al_azar=0.3848
DIAG_FALSOS umbral=5 falsos=20 identicos_perm_estr=0 misma_etiqueta perm-estr=0.3847 perm-real=0.3852 estr-real=0.4354 esperado_al_azar=0.3848
```

## 5. Archivos

En la rama `titan/tabla7-reconstruida-2026-10-10`, commit `c99494fd9f0cf20d30ac37061b069361b2d222ba`. Verificado en brain-env con `git fetch` + `git show FETCH_HEAD:<archivo> | md5sum`: md5 remoto igual al local en los 6.

| archivo | md5 |
|---|---|
| `tools/output_control_permutation_null.py` | `393300a4ff47bcc14111d33d56b6dbb3` |
| `tests/test_output_control_permutation_null.py` | `382047c7540322fdb828e3c316ed8b80` |
| `results/output_control_permnull_2026-10-10/run.log` | `171be90d0f2aa2632a0a12a069d987b1` |
| `results/output_control_permnull_2026-10-10/tests.log` | `7da86bfd8837fa477fd5e4ccaa433270` |
| `results/output_control_permnull_2026-10-10/diag_falsos.py` | `1a7f3003bb428f2fe2333eb5f06f4e1c` |
| `results/output_control_permnull_2026-10-10/diag_falsos.log` | `6c8f38a19879a5e38963c963b4dd5c28` |

Sólo en brain-env (`/workspace/dfc-t7/results/output_control_permnull_2026-10-10/`), no subidos:

| archivo | bytes | md5 |
|---|---|---|
| `output_control_permutation_null.json` | 495.177 | `ec64172711d7d18040f6f09335d7521b` |
| `output_control_permutation_null_v1.json` | 494.758 | `5e4abc205d7acf11510b5e9bad149b1e` |
| `run_v1_media_inf.log` | 32.227 | `0402321cd62286f024489e63a47bcb00` |
| `tests_v1.log` | 773 | `0e25d64882c872cf832945a0b2a30f21` |
| `progress.log` | 1.701 | `62a0151a4514db1136b70b9e7700a888` |
| `progress_v1.log` | 1.701 | `2b94d58edde5418b5d16c557fa7962d2` |

En `main`: este archivo y `docs/agents/CONTEXTO-drosophila-fep.md`.

## 6. NO MEDIDO

- Un nulo que además conserve el lugar (región o neuropilo de origen). estr controla el tamaño, no la geografía: el ▼ del óptico y de la proyección visual puede ser distancia a la zona subesofágica.
- Corrección por comparaciones múltiples: p ≤ 0,001 por test sin corrección global; se esperan ~0,5 flags falsos por umbral y por nulo en 242 / 231 tests.
- La columna ≥5 de la tabla de la sección 3 no está copiada verbatim en este archivo (está en `run.log`, líneas 134–227).
- Lo que ya estaba abierto en la 005: qué hace cada descendente en el cuerpo (el cordón ventral no está en FlyWire), el signo fisiológico real y la causalidad.

```text
--- METODO PROMETEO ---
Máquina:     brain-env (2 núcleos; Python 3.12.14, numpy 2.5.3, scipy 1.18.1), 2 corridas de 778–779 s; tests también en el sandbox
Artefactos:  docs/agents/respuestas/2026-10-10-006-nulo-fuerte-por-permutacion.md + Doc https://app.clickup.com/90171457413/docs/2kza6fw5-20897
Código/logs: rama titan/tabla7-reconstruida-2026-10-10, commit c99494fd9f0cf20d30ac37061b069361b2d222ba (PR #26, sin merge)
```
