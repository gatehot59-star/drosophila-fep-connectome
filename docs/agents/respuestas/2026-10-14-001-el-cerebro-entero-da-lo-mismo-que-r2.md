# 2026-10-14-001 · El cerebro entero da lo mismo que R2

**En una línea:** con las 138.639 neuronas de FlyWire v783 el banco da lo mismo que con R2 (33.489 neuronas): la misma predicción en el 99,913 % de 1.200.000 ensayos. Le sigue ganando a sus 100 barajados y sigue empatando con su regla, y lo que decide si le gana a la regla es la semilla de tau, no el tamaño.

Doc de ClickUp: [El cerebro entero da lo mismo que R2 (99,9 % de los ensayos iguales) (14-oct, 001)](https://app.clickup.com/90171457413/docs/2kza6fw5-22077) · Resultados en la rama: [`results/factorial4_2026-10-13/`](https://github.com/gatehot59-star/drosophila-fep-connectome/tree/titan/factorial4-cerebro-entero-2026-10-13/results/factorial4_2026-10-13)

## Veredicto

- [MEDIDO] **Factorial 4 VÁLIDO.** Los dos kernels de Kaggle (T4 ×2, cuenta `abrahammendieta`) terminaron con rc 0 y los 22 trabajos también. Todos los chequeos del agregador sellado (`agregar_factorial4.py` `96396793`, sello `431b7bd`) dan True.
- [MEDIDO] **H_ESCALA REFUTADA: el cerebro entero da lo mismo que R2.** CE − R2 = +0,01 puntos, IC90 [−0,01; +0,04], EQUIVALENTE en las seis celdas. Ensayo por ensayo, la misma predicción en 1.198.955 de 1.200.000 (99,913 %); 147 de las 600 corridas son idénticas en sus 2.000 ensayos y la que más difiere lo hace en 7.
- [MEDIDO] **H_SUPERA_CE SIN_DECIDIR.** Contra su regla de 564 entradas: 0,9355 contra 0,9268, +0,86 puntos, IC90 [+0,11; +1,51], NO_INFERIOR (le falta para pasar el margen de 1 punto). Es el mismo empate técnico que R2 en el factorial 3 (+0,85).
- [MEDIDO] **H_CABLEADO_CE SOSTENIDA.** 0,9465 contra 50 SL (media 0,6488, máx 0,7935) y 50 T (media 0,7596, máx 0,8395): ninguno igual o mejor; p 0,0196 cada uno, Holm 0,0392.
- [MEDIDO] **Se recomputa desde git.** `releer_factorial4_desde_csv.py` rehace la primaria, la escala y los nulos desde `corridas.csv` y `nulos.csv` con el bootstrap sellado: 18 de 18 líneas iguales a `agregado.log`. Con una sola corrida tocada da 4 líneas distintas y sale con 1: puede dar rojo.
- [MEDIDO, post-hoc, no sellado] **El margen contra la regla lo decide la semilla de tau.** En 8 de las 10 semillas el cerebro entero le gana a su regla en 58 a 60 de sus 60 corridas (+1,28 a +1,71 puntos). En la semilla 5 no le gana en ninguna (−2,30) y en la 7 le gana en 6 de 60 (−0,85). R2 hace lo mismo semilla por semilla. Es una tabla mirada después de los datos: describe, no prueba.
- [CONCLUSIÓN] En esta tarea, las 105.150 neuronas que están fuera de R2 no mueven lo que leen las descendentes. La pieza útil es R2 o menos: juega a favor de la fábrica de partes (piezas chicas y separables) y en contra de «más cerebro, mejor». Lo abierto no es el tamaño sino las constantes de tiempo: **H_TAU**, candidata, sin sellar.

## 1. Pedido

Abraham, 14-oct 07:43: «revisa». Se lee como revisar el factorial 4, el banco con el cerebro entero en Kaggle, disparado a las 00:13 UTC a su pedido (ClickKit `correr_factorial4_015`, respuesta 2026-10-13-016).

## 2. Herramientas y máquina

- **Kaggle, `abrahammendieta`:** en este turno solo lectura (`kaggle kernels status` y `kaggle kernels output` de `f4-ce-a-2026-10-13` y `f4-ce-b-2026-10-13`). La corrida de anoche usó 11.755 s + 13.519 s de sesión T4 ×2 (unas 7,0 h). Cuota restante: NO MEDIDO.
- **brain-env:** descarga de las dos salidas (1,1 MB cada una), `agregar_factorial4.py` sellado, `compactar_factorial4.py` (`d0ac6cac`) y `releer_factorial4_desde_csv.py` (`045caf9e`), los dos nuevos y post-hoc; `md5sum -c`; clones frescos (la rama en `13ff7e8` y en `87be763`, main en `9888625`) y la prueba del parche del CONTEXTO sobre una copia. Nada instalado. No se tocó lo de la otra instancia (la descarga de Ghidra).
- **GitHub, por MCP:** tres commits a la rama `titan/factorial4-cerebro-entero-2026-10-13` (`6385633`, `13ff7e8`, `87be763`) y este a main, con la respuesta, el parche del CONTEXTO y su workflow (Actions x64 lo aplica y se retira). Nada mergeado ni borrado.
- **ClickUp:** un Doc público con este contenido.

## 3. Qué se midió

| Qué | Número | Instrumento |
|---|---|---|
| La corrida | 2 kernels rc 0, 22 de 22 trabajos rc 0; a 11.755 s, b 13.519 s | recibos de Kaggle, chequeados por el agregador |
| Validez | VALIDO, todos los chequeos True | `agregar_factorial4.py` `96396793` |
| Primaria (CE contra su regla) | 0,9355 contra 0,9268: +0,86 puntos, IC90 [+0,11; +1,51], NO_INFERIOR; 6 de 6 celdas NO_INFERIOR | bootstrap de dos vías (tau y prueba), B 20.000, semilla 2026, margen 1 punto |
| Escala (CE contra R2) | +0,01 puntos, IC90 [−0,01; +0,04], EQUIVALENTE; 6 de 6 celdas; 226 corridas CE>R2, 209 iguales, 165 CE<R2 | el mismo bootstrap, semilla 2027 |
| Ensayo por ensayo | misma predicción en 1.198.955 de 1.200.000 (99,913 %); 147 de 600 corridas idénticas; la peor difiere en 7 de 2.000 | `compactar_factorial4.py` sobre los json de Kaggle |
| Cableado contra barajados | 0,9465 contra SL 0,6488 (máx 0,7935) y T 0,7596 (máx 0,8395); 0 de 100 iguales o mejores; p 0,0196, Holm 0,0392 | el agregador sellado |
| Recomputable desde git | 18 de 18 líneas iguales; con una corrida tocada, 4 distintas y salida 1 | `releer_factorial4_desde_csv.py` |
| Post-hoc por semilla de tau | 8 de 10 semillas a favor (+1,28 a +1,71; 58 a 60 de 60 corridas); semilla 5 −2,30 (0 de 60); semilla 7 −0,85 (6 de 60); R2 igual | la misma relectura, tabla no sellada |
| Lo commiteado | 5 de 5 archivos con el md5 esperado en `13ff7e8` y 2 de 2 en `87be763`; 50 de 50 salidas OK contra `MD5SUMS.txt` | clones frescos y `md5sum -c` |

### Por semilla de tau (post-hoc, puntos porcentuales, 60 corridas por fila)

| Semilla | CE − regla | R2 − regla | CE − R2 | Corridas con CE > regla |
|---|---|---|---|---|
| 0 | +1,40 | +1,42 | −0,01 | 59 de 60 |
| 1 | +1,28 | +1,31 | −0,03 | 59 de 60 |
| 2 | +1,55 | +1,58 | −0,03 | 60 de 60 |
| 3 | +1,34 | +1,38 | −0,04 | 59 de 60 |
| 4 | +1,33 | +1,30 | +0,04 | 60 de 60 |
| **5** | **−2,30** | **−2,40** | +0,11 | **0 de 60** |
| 6 | +1,54 | +1,54 | +0,00 | 60 de 60 |
| **7** | **−0,85** | **−0,87** | +0,03 | **6 de 60** |
| 8 | +1,61 | +1,58 | +0,03 | 60 de 60 |
| 9 | +1,71 | +1,69 | +0,03 | 58 de 60 |

Por prueba, en cambio, no hay nada raro: entre 45 y 52 de 60 a favor en las diez, que son las mismas 12 corridas de las semillas 5 y 7 perdiendo en cada una.

### En criollo

- **Tamaño.** Pasar de un cuarto del cerebro (R2) al cerebro entero no cambia nada que se pueda medir: las 105.150 neuronas de más no llegan a mover lo que leen las descendentes. Para un robot es la mejor noticia posible: la pieza que sirve es chica y separable, y no hace falta cargar 15 millones de conexiones.
- **Contra la regla a mano.** El cableado sigue empatando técnicamente con su propia regla (+0,86 puntos, sin pasar el margen de 1), igual que R2.
- **Contra los barajados.** El cableado real sigue siendo mejor que cualquiera de sus 100 versiones desordenadas, ahora también con el cerebro entero.
- **Lo nuevo.** El empate con la regla no es parejo: en 8 de las 10 semillas de constantes de tiempo la red le gana a la regla casi siempre, y en dos pierde. Si un experimento sellado lo confirma, el paso siguiente no es más neuronas sino mejores constantes de tiempo.

### H_TAU, candidata (sin sellar)

- **Qué afirmaría:** con las constantes de tiempo elegidas o aprendidas usando solo los ensayos de entrenamiento, el cableado le gana a su regla por más de 1 punto en la prueba.
- **Falsador:** si con la semilla (o las constantes) elegida en entrenamiento el IC90 contra la regla no queda entero arriba de +0,01 en la prueba, H_TAU queda refutada. Elegir mirando la prueba está prohibido: es justo el sesgo que esta tabla post-hoc no puede descartar.
- **Dónde:** R2 da lo mismo que el cerebro entero y corre en CPU, así que va a Actions, gratis y sin gastar GPU.

## 4. Evidencia cruda

### 4.1 La rama, desde clones frescos

Comando: `git clone -q --depth 1 --single-branch --branch titan/factorial4-cerebro-entero-2026-10-13 https://github.com/gatehot59-star/drosophila-fep-connectome.git verif001`, después `git rev-parse HEAD`, `md5sum` y `wc -c`.

```
13ff7e8f1117f59116f703b6228720b532d8dcc8
7f39675790c5022316a7ea356881a763  results/factorial4_2026-10-13/MD5SUMS.txt
539733b907978ff1734d28a8210e7e62  results/factorial4_2026-10-13/agregado.log
b58be3087b09dc7b634491287d31c4fb  results/factorial4_2026-10-13/corridas.csv
9481136377900112fcdbb9d45db81650  results/factorial4_2026-10-13/nulos.csv
d0ac6cac6f6829390d7d69abb6caabe1  tools/factorial4/compactar_factorial4.py
 4075 results/factorial4_2026-10-13/MD5SUMS.txt
 2308 results/factorial4_2026-10-13/agregado.log
23418 results/factorial4_2026-10-13/corridas.csv
 1193 results/factorial4_2026-10-13/nulos.csv
```

Después del commit de la relectura (otro clon fresco, `verif001b`):

```
87be7634649026d317b8f775654379ab92e2857f
045caf9e29bf3a9090bf2cd06c0bd508  tools/factorial4/releer_factorial4_desde_csv.py
a778e608d062d17e4c068907b98c11ba  results/factorial4_2026-10-13/relectura_desde_csv.log
a778e608d062d17e4c068907b98c11ba  /workspace/f4cerebro_2026-10-13/relectura_clon2.log
POSITIVO_RC_CERO
```

La última línea de md5 es la salida de correr la relectura en ese clon: igual byte a byte a la commiteada. `md5sum -c MD5SUMS.txt` en la carpeta bajada de Kaggle: 50 líneas `: OK` de 50.

### 4.2 `agregado.log` (verbatim)

```
JSON grilla=12 nulos=10 verificar=0 recibos=2 validos=True sin_humo=True | factorial 3 grilla=60
RECIBO f4-ce-a-2026-10-13 rc=0 head=ace8fe7 instrumento=OK insumos=True n_gpu=2 duracion_s=11755.4 -> True
RECIBO f4-ce-b-2026-10-13 rc=0 head=ace8fe7 instrumento=OK insumos=True n_gpu=2 duracion_s=13518.8 -> True
CHEQUEO RECIBOS -> True
CHEQUEO INTEGRIDAD archivos_con_md5=22/22 huerfanos=0 -> True
CHEQUEO TAU_DN_IGUAL semillas=10 -> True
CHEQUEO PLAN_GRILLA corridas=600 faltan=0
CHEQUEO REPRO_R2 trabajos=4 valores=[0.9465, 0.9465, 0.9465, 0.9465] -> True
CHEQUEO REAL_IGUAL grilla=0.9465 script_de_nulos=[0.9465] -> True
CHEQUEO PLAN_NULOS SL=50 T=50 repetidos=0 -> True
CHEQUEO REPRODUCE_PRIMARIA_F3 dif=+0.0085 IC90=[+0.0008, +0.0151] -> True
PRIMARIA CE_CON_TASA W=0.9355 regla_propia=0.9268 dif=+0.0086 IC90=[+0.0011, +0.0151] corridas=600 -> NO_INFERIOR
  CELDA 0.0|0.15 dif=+0.0108 IC=[-0.0028, +0.0202] -> NO_INFERIOR
  CELDA 0.0|0.45 dif=+0.0118 IC=[+0.0010, +0.0202] -> NO_INFERIOR
  CELDA 0.3|0.15 dif=+0.0094 IC=[-0.0034, +0.0184] -> NO_INFERIOR
  CELDA 0.3|0.45 dif=+0.0106 IC=[+0.0003, +0.0181] -> NO_INFERIOR
  CELDA 0.6|0.15 dif=+0.0042 IC=[-0.0084, +0.0129] -> NO_INFERIOR
  CELDA 0.6|0.45 dif=+0.0052 IC=[-0.0049, +0.0128] -> NO_INFERIOR
CHEQUEO REGLA_IGUAL_F3 combinaciones=60 iguales=60 -> True
CHEQUEO TAU_DN_IGUAL_F3 -> True
CHEQUEO DN_IGUAL_F3 -> True
ESCALA CE_menos_R2 W_CE=0.9355 W_R2=0.9353 dif=+0.0001 IC90=[-0.0001, +0.0004] corridas=600 -> EQUIVALENTE
  CELDA 0.0|0.15 dif=+0.0000 IC=[-0.0006, +0.0007] -> EQUIVALENTE
  CELDA 0.0|0.45 dif=-0.0001 IC=[-0.0006, +0.0004] -> EQUIVALENTE
  CELDA 0.3|0.15 dif=+0.0001 IC=[-0.0001, +0.0005] -> EQUIVALENTE
  CELDA 0.3|0.45 dif=+0.0004 IC=[+0.0000, +0.0008] -> EQUIVALENTE
  CELDA 0.6|0.15 dif=-0.0000 IC=[-0.0002, +0.0003] -> EQUIVALENTE
  CELDA 0.6|0.45 dif=+0.0002 IC=[-0.0001, +0.0006] -> EQUIVALENTE
ESCALA corridas CE>R2=226 iguales=209 CE<R2=165
NULOS SL n=50 media=0.6488 max=0.7935 W=0.9465 iguales_o_mejores=0 p_sup=0.0196
NULOS T n=50 media=0.7596 max=0.8395 W=0.9465 iguales_o_mejores=0 p_sup=0.0196
NULOS Holm SL=0.0392 T=0.0392
HIPOTESIS H_SUPERA_CE -> SIN_DECIDIR
HIPOTESIS H_ESCALA -> REFUTADA
HIPOTESIS H_CABLEADO_CE -> SOSTENIDA
VEREDICTO_GLOBAL -> VALIDO | primaria=NO_INFERIOR | escala=EQUIVALENTE
EXIT_AGREGADO=0
```

### 4.3 `compactar_factorial4.py`, re-corrido desde el clon fresco (verbatim)

Comando: `python3 tools/factorial4/compactar_factorial4.py /workspace/f4cerebro_2026-10-13/resultados/factorial4_2026-10-13 results/factorial3_2026-10-13 /workspace/f4cerebro_2026-10-13/compacto_verif`

```
CORRIDAS CE=600 R2=600 pareadas=600
REGLA igual en CE y R2: 600 de 600 corridas
MEDIAS (pandas) W_CE=0.9355 regla=0.9268 W_R2=0.9353 | CE-regla=+0.0086 | CE-R2=+0.00012
DIFERENCIA CE-R2 por corrida: max=0.0035 | en ensayos (de 2000): max=7 | corridas con |dif|<=0.001: 535
ENSAYOS con la misma prediccion en CE y R2: 1198955 de 1200000 (99.913 %)
CORRIDAS con las 2000 predicciones identicas: 147 de 600
NULOS SL n=50 media=0.6488 max=0.7935 T n=50 media=0.7596 max=0.8395
MD5SUMS archivos=50
escrito corridas.csv md5=b58be3087b09dc7b634491287d31c4fb bytes=23418
escrito nulos.csv md5=9481136377900112fcdbb9d45db81650 bytes=1193
escrito MD5SUMS.txt md5=7f39675790c5022316a7ea356881a763 bytes=4075
```

Los tres archivos salen con el mismo md5 que los commiteados. El `rc=0` que imprimió el shell después no cuenta como instrumento: en brain-env el `$?` se expande antes de correr. Las salidas de este turno se prueban con `&& echo … || echo …`.

### 4.4 `relectura_desde_csv.log` (verbatim) y su control negativo

```
CHEQUEO AGREGADOR_SELLADO md5=96396793 -> True
CSV corridas=600 unicas=600 taus=10 pruebas=10 celdas=6 B=20000
IGUAL PRIMARIA CE_CON_TASA W=0.9355 regla_propia=0.9268 dif=+0.0086 IC90=[+0.0011, +0.0151] corridas=600 -> NO_INFERIOR
IGUAL   CELDA 0.0|0.15 dif=+0.0108 IC=[-0.0028, +0.0202] -> NO_INFERIOR
IGUAL   CELDA 0.0|0.45 dif=+0.0118 IC=[+0.0010, +0.0202] -> NO_INFERIOR
IGUAL   CELDA 0.3|0.15 dif=+0.0094 IC=[-0.0034, +0.0184] -> NO_INFERIOR
IGUAL   CELDA 0.3|0.45 dif=+0.0106 IC=[+0.0003, +0.0181] -> NO_INFERIOR
IGUAL   CELDA 0.6|0.15 dif=+0.0042 IC=[-0.0084, +0.0129] -> NO_INFERIOR
IGUAL   CELDA 0.6|0.45 dif=+0.0052 IC=[-0.0049, +0.0128] -> NO_INFERIOR
IGUAL ESCALA CE_menos_R2 W_CE=0.9355 W_R2=0.9353 dif=+0.0001 IC90=[-0.0001, +0.0004] corridas=600 -> EQUIVALENTE
IGUAL   CELDA 0.0|0.15 dif=+0.0000 IC=[-0.0006, +0.0007] -> EQUIVALENTE
IGUAL   CELDA 0.0|0.45 dif=-0.0001 IC=[-0.0006, +0.0004] -> EQUIVALENTE
IGUAL   CELDA 0.3|0.15 dif=+0.0001 IC=[-0.0001, +0.0005] -> EQUIVALENTE
IGUAL   CELDA 0.3|0.45 dif=+0.0004 IC=[+0.0000, +0.0008] -> EQUIVALENTE
IGUAL   CELDA 0.6|0.15 dif=-0.0000 IC=[-0.0002, +0.0003] -> EQUIVALENTE
IGUAL   CELDA 0.6|0.45 dif=+0.0002 IC=[-0.0001, +0.0006] -> EQUIVALENTE
IGUAL ESCALA corridas CE>R2=226 iguales=209 CE<R2=165
IGUAL NULOS SL n=50 media=0.6488 max=0.7935 W=0.9465 iguales_o_mejores=0 p_sup=0.0196
IGUAL NULOS T n=50 media=0.7596 max=0.8395 W=0.9465 iguales_o_mejores=0 p_sup=0.0196
IGUAL NULOS Holm SL=0.0392 T=0.0392
CHEQUEO RECOMPUTA_DESDE_CSV lineas=18 iguales=18 -> True
# POSTHOC: no estaba en el plan sellado; describe, no decide
POSTHOC TAU 0 CE-regla=+0.0140 R2-regla=+0.0142 CE-R2=-0.0001 CE>regla=59/60
POSTHOC TAU 1 CE-regla=+0.0128 R2-regla=+0.0131 CE-R2=-0.0003 CE>regla=59/60
POSTHOC TAU 2 CE-regla=+0.0155 R2-regla=+0.0158 CE-R2=-0.0003 CE>regla=60/60
POSTHOC TAU 3 CE-regla=+0.0134 R2-regla=+0.0138 CE-R2=-0.0004 CE>regla=59/60
POSTHOC TAU 4 CE-regla=+0.0133 R2-regla=+0.0130 CE-R2=+0.0004 CE>regla=60/60
POSTHOC TAU 5 CE-regla=-0.0230 R2-regla=-0.0240 CE-R2=+0.0011 CE>regla=0/60
POSTHOC TAU 6 CE-regla=+0.0154 R2-regla=+0.0154 CE-R2=+0.0000 CE>regla=60/60
POSTHOC TAU 7 CE-regla=-0.0085 R2-regla=-0.0087 CE-R2=+0.0003 CE>regla=6/60
POSTHOC TAU 8 CE-regla=+0.0161 R2-regla=+0.0158 CE-R2=+0.0003 CE>regla=60/60
POSTHOC TAU 9 CE-regla=+0.0171 R2-regla=+0.0169 CE-R2=+0.0003 CE>regla=58/60
POSTHOC PRUEBA 2 CE-regla=+0.0044 CE>regla=48/60
POSTHOC PRUEBA 3 CE-regla=+0.0118 CE>regla=48/60
POSTHOC PRUEBA 4 CE-regla=+0.0116 CE>regla=48/60
POSTHOC PRUEBA 5 CE-regla=+0.0016 CE>regla=45/60
POSTHOC PRUEBA 6 CE-regla=+0.0056 CE>regla=47/60
POSTHOC PRUEBA 7 CE-regla=+0.0147 CE>regla=52/60
POSTHOC PRUEBA 8 CE-regla=+0.0052 CE>regla=48/60
POSTHOC PRUEBA 9 CE-regla=+0.0063 CE>regla=47/60
POSTHOC PRUEBA 10 CE-regla=+0.0145 CE>regla=49/60
POSTHOC PRUEBA 11 CE-regla=+0.0106 CE>regla=49/60
POSTHOC corridas CE>regla=481 iguales=2 CE<regla=117
POSTHOC taus con CE-regla>0: 8 de 10; media en esos=+0.0147; en los otros=-0.0157
EXIT_RELECTURA=0
```

Control negativo, en una copia (`ctrl_neg001`) con la primera corrida tocada (W_CE 0,949 pasado a 0,959 con `sed`):

```
0.0|0.15,0,2,0.959,0.95,0.9385,0.9085
NEGATIVO_RC_NO_CERO
4
DISTINTA PRIMARIA CE_CON_TASA W=0.9355 regla_propia=0.9268 dif=+0.0087 IC90=[+0.0011, +0.0151] corridas=600 -> NO_INFERIOR
DISTINTA   CELDA 0.0|0.15 dif=+0.0109 IC=[-0.0028, +0.0203] -> NO_INFERIOR
DISTINTA   CELDA 0.0|0.15 dif=+0.0001 IC=[-0.0005, +0.0008] -> EQUIVALENTE
DISTINTA ESCALA corridas CE>R2=227 iguales=209 CE<R2=164
CHEQUEO RECOMPUTA_DESDE_CSV lineas=18 iguales=14 -> False
EXIT_RELECTURA=1
```

Sensibilidad: un punto en una sola de las 600 corridas ya cambia 4 líneas. Un cambio más chico que el redondeo a 4 decimales de las medias podría pasar por las líneas de media, pero no por los conteos.

### 4.5 Recibos

Kernel a: rc 0, head `ace8fe7`, instrumento OK, insumos OK, 2 GPU, 11.755,4 s (00:13:14 a 03:29:09 UTC). Kernel b: rc 0, head `ace8fe78093a9109c20235746d867f2b168290d2`, `md5_instrumento` OK, insumos `719904abad876c68ace1b5690c9b9b63` y `3d802fd542b5d18570ba1ba0bb0abed9`, 2 GPU, 13.518,8 s (00:13:23 a 03:58:42 UTC). md5 de los recibos: a `7b6dd265f7b1d110ccbd2b1a681ecde8`, b `70c10cbee646c1c23e80dd3870d38432`.

| Trabajo (kernel b) | GPU | rc | Inicio UTC | Fin UTC | s |
|---|---|---|---|---|---|
| grilla_c3h1 | 1 | 0 | 00:14:17 | 01:06:43 | 3146,3 |
| grilla_c0h1 | 0 | 0 | 00:14:17 | 01:07:14 | 3177,0 |
| grilla_c4h1 | 1 | 0 | 01:06:43 | 01:58:43 | 3119,9 |
| grilla_c1h1 | 0 | 0 | 01:07:14 | 02:03:29 | 3375,1 |
| grilla_c5h1 | 1 | 0 | 01:58:43 | 02:50:50 | 3126,4 |
| grilla_c2h1 | 0 | 0 | 02:03:29 | 03:05:54 | 3744,9 |
| nulos_t_k030 | 1 | 0 | 02:50:50 | 03:11:24 | 1234,1 |
| nulos_sl_k030 | 0 | 0 | 03:05:54 | 03:31:53 | 1558,5 |
| nulos_t_k040 | 1 | 0 | 03:11:24 | 03:31:56 | 1232,4 |
| nulos_sl_k040 | 0 | 0 | 03:31:53 | 03:58:42 | 1609,0 |

### 4.6 El parche del CONTEXTO, probado sobre una copia de main (`9888625`)

```
d665dc3c2fe6b5a8f09576b51afdc463  actualizar_contexto_2026-10-14-001.py
5ccf0ba1fbdc044896374fa2e2262155  ctx.md
md5 antes 5ccf0ba1fbdc044896374fa2e2262155
ANCLA apariciones=1 :: **Última actualización:** 2026-10-13, 21:15 (America/Buenos_
ANCLA apariciones=1 :: ## Madrugada y mañana del 13-oct (019 a 2026-10-13-016) · ma
ANCLA apariciones=1 :: - **Factorial 4 sellado en Kaggle (2026-10-13-015) y dispara
ANCLA apariciones=1 ::   - La salida grande (unos 1,6 MB de json con la predicción 
ANCLA apariciones=1 :: - **Corriendo:** kernels `f4-ce-a-2026-10-13` y `f4-ce-b-202
ANCLA apariciones=1 :: - **Espera decisión de Abraham:** merge del PR #27 (la v2 ya
md5 despues 972998cafbe963de1b45fa82e6680ac5
PARCHE OK
972998cafbe963de1b45fa82e6680ac5  ctx.md
461 ctx.md
```

## 5. Archivos

En la rama `titan/factorial4-cerebro-entero-2026-10-13`:

| Archivo | md5 | Commit |
|---|---|---|
| `results/factorial4_2026-10-13/agregado.log` | `539733b9` | `6385633` |
| `results/factorial4_2026-10-13/nulos.csv` | `94811363` | `6385633` |
| `results/factorial4_2026-10-13/MD5SUMS.txt` | `7f396757` | `6385633` |
| `tools/factorial4/compactar_factorial4.py` | `d0ac6cac` | `6385633` |
| `results/factorial4_2026-10-13/corridas.csv` | `b58be308` | `13ff7e8` |
| `tools/factorial4/releer_factorial4_desde_csv.py` | `045caf9e` | `87be763` |
| `results/factorial4_2026-10-13/relectura_desde_csv.log` | `a778e608` | `87be763` |

En main, en este commit: esta respuesta; `tools/contexto/actualizar_contexto_2026-10-14-001.py` (`d665dc3c`); `.github/workflows/contexto-2026-10-14-001.yml` (`db5b913e`, se retira solo después de aplicar).

Fuera de git, por md5 en `MD5SUMS.txt`: los 12 json de la grilla (unos 131 KB cada uno, 1,58 MB), los 10 json de nulos, los 20 logs de trabajo, los 4 logs de kernel y los 2 recibos. Están en brain-env (`/workspace/f4cerebro_2026-10-13/resultados/factorial4_2026-10-13/`) y en la salida de los kernels privados de `abrahammendieta`.

## 6. NO MEDIDO

- **Por qué pierden las semillas 5 y 7.** No se miró qué constantes de tiempo las separan de las otras ocho; a ojo, las de las DN no lo explican (post-hoc).
- **H_TAU:** candidata, sin sellar ni correr.
- **El 99,913 % no se recomputa desde git:** sale de los json por ensayo, que quedaron por md5. Se recomputa bajando la salida de los kernels (privados, de `abrahammendieta`) y corriendo `compactar_factorial4.py`.
- **Si una pieza más chica que R2 da lo mismo:** no se midió en este factorial.
- **Si se sostiene en otra tarea u otro conectoma** (BANC, el macho): NO MEDIDO.
- **Cuota de GPU que le queda a `abrahammendieta`:** la CLI no la muestra.
- **Que el bot aplicó el CONTEXTO:** al escribir esto, no; se espera `972998ca` en main.

## Antes de firmar

| Afirmación | Instrumento | ¿Podía dar rojo? | Veredicto |
|---|---|---|---|
| El factorial 4 es VÁLIDO | `agregar_factorial4.py` sellado sobre las 50 salidas | sí: cada chequeo da False si falta un archivo, un md5, un recibo o una corrida | medido, bien |
| Lo commiteado es lo medido | md5 desde clones frescos de `13ff7e8` y `87be763` | sí | medido, bien (7 de 7) |
| Las salidas agregadas son las bajadas de Kaggle | `md5sum -c MD5SUMS.txt` | sí | medido, bien (50 de 50) |
| La lectura se recomputa desde git | `releer_factorial4_desde_csv.py` | sí: con una corrida tocada dio 4 distintas y salida 1 | medido, bien (18 de 18) |
| CE y R2 predicen lo mismo en el 99,913 % | `compactar_factorial4.py` sobre los json | sí | medido; recomputable solo con los json |
| H_ESCALA REFUTADA | bootstrap sellado, semilla 2027 | sí | medido |
| La semilla de tau decide | tabla post-hoc de la relectura | no como hipótesis: se miró después de ver los datos | NO MEDIDO como hipótesis; descriptivo |
| El bot aplicó el CONTEXTO | md5 del CONTEXTO en main tras el workflow | sí | NO MEDIDO al escribir esto |
| `rc=0` del compactador | `echo rc=$?` en brain-env | no: el `$` se expande antes | NO MEDIDO; vale el md5 de lo que escribió |

```
--- METODO PROMETEO ---
Accion delicada: no (lectura de resultados; commits en la rama titan y documentacion en main; nada mergeado ni borrado)
Maquina: Kaggle T4 x2 (2 kernels, unas 7,0 h de sesion, ya corridos) | brain-env (descarga, agregado, compactado, relectura, prueba del parche) | Actions x64 (aplica el CONTEXTO)
Artefactos: docs/agents/respuestas/2026-10-14-001-el-cerebro-entero-da-lo-mismo-que-r2.md + Doc de ClickUp https://app.clickup.com/90171457413/docs/2kza6fw5-22077
```
