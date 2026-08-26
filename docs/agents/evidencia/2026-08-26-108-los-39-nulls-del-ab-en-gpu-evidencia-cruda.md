# EVIDENCIA CRUDA · 2026-08-26 · los 39 nulls del A/B v1 vs v2, en Kaggle GPU

**Instrumento:** 4 kernels privados de Kaggle con GPU Tesla P100-PCIE-16GB.
**Fuentes:** embebidos en base64 en cada kernel y **verificados por md5 al arrancar**.
Si un md5 no coincidia, el kernel abortaba.

---

## 1. Cabecera verbatim del shard 0

```
escrito motor.py  30644 B  md5 480539069ec00f317eec525e6fa81324  VERIFICADO
escrito motor_v2.py  65543 B  md5 8f7ad4740727478bf62b7cd0663fb341  VERIFICADO
escrito ab39_core.py  16748 B  md5 3d7c2d1bf0f3fd6228905ec795f53f24  VERIFICADO
MODO=ab SHARD=0/4 NULLS=39
[    0.0s] motor.py     md5=480539069ec00f317eec525e6fa81324  30644 B
[    0.0s] motor_v2.py  md5=8f7ad4740727478bf62b7cd0663fb341  65543 B
[    1.7s] los dos motores importados como modulos
[    3.2s] GPU: Tesla P100-PCIE-16GB
[1.5s]   descargando connectivity.parquet
[3.3s]   descargando annotations.tsv
[4.5s]   OK    md5_parquet: 3d802fd542b5d18570ba1ba0bb0abed9
[4.5s]   OK    md5_annotations: 719904abad876c68ace1b5690c9b9b63  (SHA 17fc5772)
[11.5s]   anotaciones: 138625 de 139248 matchean un nodo; 623 NO matchean y quedan SIN region (declarado, no oculto)
[   13.2s] grafo: n=138639  e=15091983  md5=3d802fd542b5d18570ba1ba0bb0abed9
[   13.2s] modalidades=['visual', 'olfactory', 'mechanosensory']  pasos=150  snapshots=[50, 100, 149]
[   13.2s] ########## VERIFICACION GPU contra la CPU de CADA motor ##########
[   74.2s]   mv1  desvio relativo maximo = 2.866e-16   OK
[   76.8s]   mv2  desvio relativo maximo = 2.866e-16   OK
[   76.8s]   BACKEND EFECTIVO: GPU (misma propagate inyectada en los dos)
[   76.8s] backend=GPU
```

**La GPU se verifico contra la CPU de CADA motor por separado**, no contra uno solo:
2,866e-16 en los dos. Sin eso, inyectar la misma `propagate` en ambos habria sido un
supuesto en vez de una medicion.

## 2. Veredicto por shard, verbatim

```
shard 0: peor desvio sobre 10 nulls = 1.665335e-16  -> IDENTICOS   (420.2 s)
shard 1: peor desvio sobre 10 nulls = 1.457168e-16  -> IDENTICOS   (327.6 s)
shard 2: peor desvio sobre 10 nulls = 1.110223e-16  -> IDENTICOS   (327.3 s)
shard 3: peor desvio sobre  9 nulls = 2.220446e-16  -> IDENTICOS   (294.6 s)
```

## 3. Consolidacion (`tools/ab39_consolidar.py`)

```
[1] GUARD: los md5 de los tres fuentes, por shard
  shard-0-de-4   motor=480539069ec0  motor_v2=8f7ad4740727  backend=GPU  Tesla P100-PCIE-16GB
  shard-1-de-4   motor=480539069ec0  motor_v2=8f7ad4740727  backend=GPU  Tesla P100-PCIE-16GB
  shard-2-de-4   motor=480539069ec0  motor_v2=8f7ad4740727  backend=GPU  Tesla P100-PCIE-16GB
  shard-3-de-4   motor=480539069ec0  motor_v2=8f7ad4740727  backend=GPU  Tesla P100-PCIE-16GB
  firmas distintas: 1 -> MISMO SUJETO

[2] GUARD: la particion de los 39 nulls
  indices asignados: 39   unicos: 39
  nulls con resultado: 39   faltan: ninguno

[3] A/B v1 vs v2 SOBRE LOS 39 NULLS MEDIDOS (jitter=0)
  null   d_rho         d_rdi_t50     d_rdi_t100    d_rdi_t149    v1 convergio veredicto
  0      0.000e+00     0.000e+00     0.000e+00     8.327e-17     True        identico
  1      0.000e+00     8.327e-17     0.000e+00     6.939e-17     True        identico
  2      0.000e+00     0.000e+00     1.110e-16     0.000e+00     True        identico
  3      0.000e+00     0.000e+00     1.110e-16     1.110e-16     True        identico
  4      0.000e+00     0.000e+00     0.000e+00     0.000e+00     True        identico
  5      0.000e+00     0.000e+00     0.000e+00     5.551e-17     True        identico
  6      0.000e+00     0.000e+00     0.000e+00     2.776e-17     True        identico
  7      0.000e+00     5.551e-17     1.110e-16     6.939e-17     True        identico
  8      0.000e+00     0.000e+00     0.000e+00     1.665e-16     True        identico
  9      0.000e+00     0.000e+00     1.110e-16     8.327e-17     True        identico
  10     0.000e+00     0.000e+00     0.000e+00     5.551e-17     True        identico
  11     0.000e+00     0.000e+00     1.110e-16     1.110e-16     True        identico
  12     0.000e+00     0.000e+00     0.000e+00     1.665e-16     True        identico
  13     0.000e+00     0.000e+00     0.000e+00     2.776e-17     True        identico
  14     0.000e+00     2.776e-17     1.110e-16     1.110e-16     True        identico
  15     0.000e+00     1.110e-16     0.000e+00     1.110e-16     True        identico
  16     0.000e+00     0.000e+00     1.110e-16     2.776e-17     True        identico
  17     0.000e+00     0.000e+00     0.000e+00     2.776e-17     True        identico
  18     0.000e+00     0.000e+00     0.000e+00     1.110e-16     True        identico
  19     0.000e+00     0.000e+00     1.110e-16     2.220e-16     True        identico
  20     0.000e+00     0.000e+00     0.000e+00     0.000e+00     True        identico
  21     0.000e+00     0.000e+00     1.110e-16     1.457e-16     True        identico
  22     0.000e+00     5.551e-17     0.000e+00     0.000e+00     True        identico
  23     0.000e+00     2.776e-17     0.000e+00     5.551e-17     True        identico
  24     0.000e+00     0.000e+00     0.000e+00     0.000e+00     True        identico
  25     0.000e+00     0.000e+00     0.000e+00     8.327e-17     True        identico
  26     0.000e+00     0.000e+00     0.000e+00     2.776e-17     True        identico
  27     0.000e+00     0.000e+00     1.110e-16     4.163e-17     True        identico
  28     0.000e+00     0.000e+00     0.000e+00     0.000e+00     True        identico
  29     0.000e+00     0.000e+00     0.000e+00     0.000e+00     True        identico
  30     0.000e+00     0.000e+00     1.110e-16     6.939e-17     True        identico
  31     0.000e+00     1.110e-16     0.000e+00     1.110e-16     True        identico
  32     0.000e+00     0.000e+00     0.000e+00     0.000e+00     True        identico
  33     0.000e+00     2.776e-17     0.000e+00     5.551e-17     True        identico
  34     0.000e+00     8.327e-17     0.000e+00     6.939e-17     True        identico
  35     0.000e+00     0.000e+00     1.110e-16     8.327e-17     True        identico
  36     0.000e+00     8.327e-17     1.110e-16     2.776e-17     True        identico
  37     0.000e+00     0.000e+00     0.000e+00     8.327e-17     True        identico
  38     0.000e+00     0.000e+00     0.000e+00     7.633e-17     True        identico

  peor desvio global: 2.220446e-16
  nulls donde la iteracion de potencia de v1 NO convergio: 0 -> ninguno
  nulls que difieren por encima de 1e-9: 0 -> ninguno
  ATRIBUCION: no hay nada que atribuir, los 39 son identicos

  el grafo REAL:  d_rho=0.000e+00   d_t50=0.000e+00  d_t100=0.000e+00  d_t149=1.110e-16
```

**156 comparaciones** (39 nulls x 4 cantidades) mas las 4 del grafo REAL.
**Peor desvio: 2,220446e-16**, el epsilon del doble.

---

## 4. El riesgo que el smoke test encontro, y que NO se materializa

Antes de gastar GPU, el arnes se probo sobre un grafo sintetico de 3.000 nodos. Ahi
**uno de tres nulls difirio en 1,3e-04**, con esta linea en el log:

```
  AVISO: el radio espectral no convergio en 200 iteraciones. rho=6.922380e+00 es un
         limite inferior, no una medicion.
  v1 NULL g0 [NO CONVERGIO]      rho=      6.9224  ...
  v2 NULL g0                     rho=      6.9222  ...
     null g0    d_rho=1.309e-04  d_t20=4.036e-06 d_t29=1.055e-05
  null g1    d_rho=1.776e-15  (los otros dos, identicos)
```

**La causa es real y esta en el codigo:** `normalize_spectral` de v1 usa `n_iter=200` y
la de v2 `n_iter=500`. Cuando la iteracion de potencia NO converge, los dos estiman un
`rho` distinto, escalan la matriz por factores distintos, **y la dinamica cambia**.
O sea: la identidad de v1 y v2 **no es incondicional**, vale donde la iteracion converge.

**Y sobre el conectoma real NO se materializa:** la columna `v1 convergio` da `True` en
los **39** nulls y en el grafo real. La condicion se cumple siempre en este grafo.

Esto es mejor que un "identicos" a secas, porque dice **por que** podrian no serlo y
**mide** que no pasa. Un resultado sin su condicion de validez es un resultado a medias.

---

## 5. Costo

| | |
|---|---|
| 4 shards en P100 | 294 a 420 s cada uno, en paralelo |
| equivalente en CPU | la corrida de 39 nulls del 26-ago tardo **390,5 min** |
| cuota antes de lanzar | 28,0 h y 29,5 h libres (refresh 2026-08-29) |
| limite que aparecio | **2 sesiones GPU simultaneas por cuenta**, por eso 4 shards en 2 cuentas y el 5o kernel sin GPU |

---

## 6. NO MEDIDO

- El A/B corrio con **la misma `propagate` de GPU inyectada en los dos motores**. Es una
  decision de diseno declarada: la identidad de `propagate` ya estaba medida a escala
  real con desvio 0.000000e+00 (respuesta 106). Lo que este A/B mide es
  `build_weights` + `normalize_spectral` + metricas.
- Se midio **un brazo** (`Wc`, `tauC`) y **3 modalidades**, no el 2x2 completo.
- La convergencia se leyo del flag que reporta cada motor; **no** se cruzo contra ARPACK
  en los 39 (v1 no tiene ARPACK).
- `phase_jitter=0` en todo el A/B: es la condicion donde la identidad tiene que valer.
  Con jitter distinto de 0 los dos difieren por construccion.
