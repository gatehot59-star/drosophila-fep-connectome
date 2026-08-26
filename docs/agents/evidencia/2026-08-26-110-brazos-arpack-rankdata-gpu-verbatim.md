# EVIDENCIA CRUDA · 2026-08-26 · brazos, ARPACK y rankdata en GPU

**Instrumento:** 5 kernels privados de Kaggle con **Tesla P100-PCIE-16GB**, repartidos
2+2 en las dos cuentas (mas uno suelto). Fuentes verificados por md5 al arrancar.

**Contexto:** Abraham pregunto si el limite de la corrida anterior no se resolvia con la
segunda cuenta. Tenia razon en el principio y mi diagnostico habia sido incompleto: la
**cuota nunca fue el limite** (27,89 h y 29,31 h libres), el limite es de **2 sesiones GPU
simultaneas POR CUENTA**, y los 4 shards del A/B ya ocupaban las 4 que existen con dos
cuentas. Ahora que estaban libres, se usaron para lo que si requeria GPU.

---

## 1. GUARD: el mismo sujeto en los 4 shards

```
  titan-nm-brazos-arpack-shard-0-de-4   motor=480539069ec0 motor_v2=22f9904bcae8 backend=GPU Tesla P100-PCIE-16GB
  titan-nm-brazos-arpack-shard-1-de-4   motor=480539069ec0 motor_v2=22f9904bcae8 backend=GPU Tesla P100-PCIE-16GB
  titan-nm-brazos-arpack-shard-2-de-4   motor=480539069ec0 motor_v2=22f9904bcae8 backend=GPU Tesla P100-PCIE-16GB
  titan-nm-brazos-arpack-shard-3-de-4   motor=480539069ec0 motor_v2=22f9904bcae8 backend=GPU Tesla P100-PCIE-16GB
  firmas distintas: 1 -> MISMO SUJETO
  modalidades=['visual', 'olfactory', 'mechanosensory', 'gustatory']  pares de RDI=6  (antes: 3 mods, 3 pares)
```

**Nota que importa:** estos kernels corren `motor_v2` **POST-fix** (`22f9904bcae8`),
mientras los del A/B de los 39 nulls corrieron el **pre-fix** (`8f7ad4740727`). O sea que
esta corrida es tambien una verificacion cruzada de que el fix del `rankdata` no cambio
ningun resultado.

Y la verificacion GPU contra la CPU de **cada** motor, verbatim del shard 1:

```
[   13.1s] ########## VERIFICACION GPU contra la CPU de CADA motor ##########
[   70.8s]   mv1 desvio relativo = 2.866e-16  OK
[   73.3s]   mv2 desvio relativo = 2.866e-16  OK
[   73.3s]   BACKEND EFECTIVO: GPU
```

---

## 2. Los DOS brazos de tau, 4 modalidades, 6 pares

```
  grafo      d_rho         d_vent_t50    d_vent_t100   d_vent_t149   veredicto
  REAL       0.000e+00     0.000e+00     2.220e-16     0.000e+00     identico
  null_0     0.000e+00     0.000e+00     5.551e-17     4.163e-17     identico
  null_1     0.000e+00     0.000e+00     0.000e+00     8.327e-17     identico
  null_2     0.000e+00     5.551e-17     1.665e-16     1.665e-16     identico
  null_3     0.000e+00     0.000e+00     5.551e-17     5.551e-17     identico
  null_4     0.000e+00     0.000e+00     5.551e-17     2.776e-17     identico
  null_5     0.000e+00     1.665e-16     1.110e-16     8.327e-17     identico
  null_6     0.000e+00     0.000e+00     0.000e+00     2.776e-17     identico
  null_7     0.000e+00     0.000e+00     0.000e+00     1.110e-16     identico
  null_8     0.000e+00     0.000e+00     0.000e+00     0.000e+00     identico
  null_9     0.000e+00     5.551e-17     0.000e+00     5.551e-17     identico
  null_10    0.000e+00     1.110e-16     0.000e+00     1.665e-16     identico
  null_11    0.000e+00     0.000e+00     5.551e-17     2.776e-17     identico

  grafos medidos: 13   peor desvio: 2.220446e-16
```

**El `d_rho` es CERO EXACTO en los 13.** La identidad de v1 y v2 ya no descansa en un
brazo y 3 modalidades: vale con **los dos brazos que v1 tiene** y con la rejilla completa
de 4 modalidades y 6 pares.

**Lo que sigue siendo imposible, y hay que decirlo:** el 2x2 **completo** no se puede en
v1, porque v1 **no tiene** modo de peso real (`WEIGHT_REAL` no existe ahi, medido en la
respuesta 105). Lo que se cerro es el 2x1 que v1 si puede.

---

## 3. CRUCE ARPACK: la convergencia deja de depender del flag del motor

v1 **no tiene ARPACK**, asi que su convergencia venia solo de su propio flag. Aca se mide
el radio espectral POSTERIOR de la matriz de **cada** motor con el instrumento de v2.

```
  grafo      motor    flag convergio     rho_post ARPACK    brecha rel     coincide 0.99?
  REAL       v1       True               0.989999999        1.015e-09      SI
  REAL       v2       True               0.989999999        1.100e-09      SI
  null_0     v1       True               0.990000000        8.846e-11      SI
  null_0     v2       True               0.990000000        2.759e-11      SI
  null_1     v1       True               0.990000000        4.353e-11      SI
  null_1     v2       True               0.990000000        4.349e-11      SI
  null_2     v1       True               0.990000002        2.181e-09      SI
  ...
  null_9     v2       True               0.990000000        7.627e-11      SI

  discrepancias ARPACK: 0 -> ninguna
```

**26 de 26** (13 grafos x 2 motores) coinciden con el target 0,99, con brechas relativas
entre **2,05e-11 y 2,18e-09**. El flag de v1 decia `True` y **un segundo instrumento
independiente lo confirma**. Eso cierra el item: la convergencia ya no es un
auto-reporte.

---

## 4. La VENTAJA DE TAU con 6 pares — y el cruce de signo REPLICA

```
  grafo      vent_t50         vent_t100        vent_t149
  REAL            +0.002011        -0.022527        +0.002741
  null_0          +0.000166        -0.012548        -0.056820
  null_1          -0.001691        -0.019350        -0.052700
  null_2          -0.002274        -0.008250        -0.038973
  null_3          -0.001103        -0.008651        -0.081925
  null_4          -0.000871        -0.008822        -0.011541
  null_5          -0.001942        -0.010725        -0.064301
  null_6          +0.000392        -0.012202        -0.122271
  null_7          -0.002573        -0.013563        -0.106290
  null_8          -0.000329        -0.014717        -0.012775
  null_9          -0.004437        -0.012534        -0.031404
  null_10         -0.001166        -0.012692        -0.020879
  null_11         -0.001163        -0.009783        -0.025126

  TEST DE SIGNO: el REAL contra los nulls medidos
    t=50   real=+0.002011   nulls: min=-0.004437 max=+0.000392 media=-0.001416   nulls>=real: 0 de 12
    t=100  real=-0.022527   nulls: min=-0.019350 max=-0.008250 media=-0.011986   nulls>=real: 12 de 12
    t=149  real=+0.002741   nulls: min=-0.122271 max=-0.011541 media=-0.052084   nulls>=real: 0 de 12
```

**Este es el resultado cientifico del turno.** La corrida de los 39 nulls con **1 brazo y
3 modalidades** dio `ventaja_tau`: 0/39 en t50, 39/39 en t100, 0/39 en t149. Con **2 brazos,
4 modalidades y 6 pares**, sobre 12 nulls: **0/12, 12/12, 0/12.**

**El patron de inversion de signo en t=100 replica exactamente al cambiar la rejilla de
medicion.** No es un artefacto de haber medido 3 pares.

Y el REAL es el **unico positivo** en t50 y t149 entre 13 grafos, con los 12 nulls
negativos. Con 12 nulls el piso del p a una cola es 1/13 = 0,077, o sea que **esto no
alcanza para significancia**: es replicacion del signo, no un test nuevo.

---

## 5. rankdata en GPU — dos hallazgos de portabilidad

### 5.1 El fix NO es portable a cupy tal cual

El primer intento, dentro del shard 0, **murio**:

```
[  287.7s] ########## rankdata: la version parcheada contra cupy ##########
Traceback (most recent call last):
  File "nm_core.py", line 194, in rankdata_gpu
    rs = cp.repeat(i0 + (cnt - 1) / 2.0 + 1.0, cnt)
ValueError: cupy.ndaray cannot be specified as `repeats` argument.
```

**`cupy.repeat` NO acepta un array de device como `repeats`; `numpy.repeat` SI.** La
version parcheada del motor usa exactamente eso. **El fix funciona en CPU y revienta en
GPU**, y eso solo aparece corriendo.

Nota: el kernel murio **despues** de medir sus 4 grafos, asi que su JSON parcial se bajo
igual. `status: error` no significa `sin datos`.

### 5.2 Las dos reescrituras, y la rapida DIFIERE con NaN

```
[   2.0s] ########## CONTROL: la version del intento anterior TIENE que fallar ##########
[   4.6s]   FALLA como se esperaba: ValueError: cupy.ndaray cannot be specified as `repeats` argument.

  caso                   n        |A-cpu|       |B-cpu|       cpu (s)     A gpu (s)   B gpu (s)   A vs cpu
  40 (el uso real)       40       0.000e+00     0.000e+00     0.000037    0.000889    0.001827    0.04x
  5k sin empates         5000     0.000e+00     0.000e+00     0.000521    0.000942    0.088864    0.55x
  200k sin empates       200000   0.000e+00     0.000e+00     0.034260    0.001617    3.211519    21.19x
  2M sin empates         2000000  0.000e+00     0.000e+00     0.410728    0.011231    31.755881   36.57x
  200k con 100 valores   200000   0.000e+00     0.000e+00     0.016131    0.001568    0.003553    10.29x
  todos iguales, 10k     10000    0.000e+00     0.000e+00     0.000167    0.001054    0.001417    0.16x
  con infinitos          5        0.000e+00     0.000e+00     0.000045    0.000865    0.001170    0.05x
```

- **A** (cumsum + searchsorted, todo en device): **36,57x mas rapida** que la CPU a 2M
  elementos, y **mas lenta** hasta ~5k. El cruce esta entre 5k y 200k.
- **B** (repeat con los counts traidos a host): **catastrofica sin empates** — 31,7 s
  contra 0,41 s de la CPU a 2M. La sincronizacion device->host por grupo la mata.
- En el tamano real de uso (**40 elementos**) las dos son **peores** que la CPU: 0,04x.
  **El fix de CPU es el correcto para este motor y la GPU no aporta nada ahi.**

### 5.3 Y el hallazgo que el propio test predijo

```
########## el caso que el motor NO ESPECIFICA: NaN ##########
  cpu del motor  -> [3.  4.5 1.  4.5 2. ]
  gpu A          -> [3. 4. 1. 5. 2.]
  gpu B          -> [3.  4.5 1.  4.5 2. ]
```

**La version A DIFIERE de la CPU con NaN.** La causa: A detecta grupos de empates con
`sa[1:] != sa[:-1]`, y **`NaN != NaN` es verdadero**, asi que cada NaN queda como su
propio grupo (rangos 4 y 5). `np.unique` en cambio los **agrupa** y promedia (4,5 y 4,5).

Las dos son defendibles y **ninguna esta especificada por el motor**. Lo que no es
defendible es no saberlo: una version que es 36x mas rapida y que difiere en un caso que
nadie especifico es precisamente como entra un bug silencioso.

**Consecuencia: la version A NO se propone para el motor.** Queda medida y declarada.

---

## 6. NO MEDIDO

- El test de signo con 6 pares usa **12 nulls**, no 39. Piso del p a una cola: 1/13 =
  0,077. **Es replicacion del signo, no un test de significancia.**
- El 2x2 **completo** sigue imposible en v1 por falta de `WEIGHT_REAL`.
- El cruce ARPACK se hizo sobre la matriz **posterior** a la normalizacion, no sobre la
  original: mide que el escalado llego al target, no que el `rho_pre` de v1 fuera exacto.
- Las reescrituras GPU del `rankdata` **no se integraron al motor** y no tienen la suite
  de 14 casos x 3 referencias que si tiene la de CPU.
- El comportamiento con NaN **no esta especificado** por el motor: se reporta lo que hace,
  no se declara correcto.
- El cronometro de GPU incluye la transferencia host->device en cada llamada, que es lo
  honesto para el uso real, pero **no separa** transferencia de computo.
