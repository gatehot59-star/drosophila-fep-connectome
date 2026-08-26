# EVIDENCIA CRUDA · 2026-08-26 · cierre de los 39 nulls y el TEST GLOBAL

**Instrumento:** `gateway build.run` sobre `brain-env`. **Sujeto:** `/workspace/motor_v2_real/motor_resultados.json` (121.099 B, escrito 08-26 05:36 UTC) y los 4 `shard_N.json` de Kaggle.

---

## 1. La corrida CPU TERMINÓ sola

```
[23430.1s]   ventaja_W_t149          real=+0.00212  null_mu=-0.00358  sd=0.00523  n_ge=6/39  p2=0.3500
[23430.1s]
[23430.1s]   TEST GLOBAL sobre 9 de 9 estadisticos
[23430.1s]     S_real=239.0  S_null_mu=183.1  sd=45.2  min=95.0
[23430.1s]     nulls por debajo=35/39  p dos colas=0.2500  piso=0.0500  significativo=False  piso alcanzable=True
[23430.2s]
[23430.2s] FIN  tests en rojo=0  minutos=390.5  salida=/workspace/motor_v2_real/motor_resultados.json
FINMOTOR
```

```
-rw-r--r--  1 root root 121099 08-26_05:36 motor_resultados.json
```

**390,5 minutos = 6 h 30 min. Cero tests en rojo. `tests_en_rojo: []`.**

---

## 2. Cruce CPU contra GPU, PRECISIÓN COMPLETA, las 12 métricas

```
[0] ESTRUCTURA DEL JSON CPU
    claves raiz: meta, tests_en_rojo, real, nulls, test_global
    nulls en el JSON CPU : 39
    real  en el JSON CPU : si

[1] CRUCE CPU vs GPU · PRECISION COMPLETA · las 12 metricas
    metrica                pares     desvio_max     desvio_medio   veredicto
    rdi_Wc_tauC_t50        39        2.220e-16      6.547e-17      IDENTICO
    ventaja_tau_t50        39        2.776e-16      8.825e-17      IDENTICO
    ventaja_W_t50          39        1.665e-16      7.544e-17      IDENTICO
    interaccion_t50        39        3.886e-16      1.381e-16      IDENTICO
    rdi_Wc_tauC_t100       39        5.551e-16      1.153e-16      IDENTICO
    ventaja_tau_t100       39        2.776e-16      1.267e-16      IDENTICO
    ventaja_W_t100         39        7.772e-16      1.793e-16      IDENTICO
    interaccion_t100       39        4.441e-16      1.324e-16      IDENTICO
    rdi_Wc_tauC_t149       39        2.165e-15      7.005e-16      IDENTICO
    ventaja_tau_t149       39        6.661e-16      1.633e-16      IDENTICO
    ventaja_W_t149         39        3.747e-15      1.055e-15      IDENTICO
    interaccion_t149       39        1.166e-15      3.130e-16      IDENTICO

[2] EL BRAZO REAL, los dos lados
    rdi_Wc_tauC_t50        CPU=+0.431096409940  GPU=+0.431096409940  |dif|=0.000e+00
    ventaja_tau_t50        CPU=+0.001996503325  GPU=+0.001996503325  |dif|=5.551e-17
    ventaja_W_t50          CPU=+0.000021979679  GPU=+0.000021979679  |dif|=5.551e-17
    interaccion_t50        CPU=-0.000014964461  GPU=-0.000014964461  |dif|=0.000e+00
    rdi_Wc_tauC_t100       CPU=+0.718421849625  GPU=+0.718421849625  |dif|=0.000e+00
    ventaja_tau_t100       CPU=-0.022790310268  GPU=-0.022790310268  |dif|=0.000e+00
    ventaja_W_t100         CPU=-0.000666360155  GPU=-0.000666360155  |dif|=2.220e-16
    interaccion_t100       CPU=-0.000262912462  GPU=-0.000262912462  |dif|=5.551e-16
    rdi_Wc_tauC_t149       CPU=+0.664217539946  GPU=+0.664217539946  |dif|=0.000e+00
    ventaja_tau_t149       CPU=+0.005992133869  GPU=+0.005992133869  |dif|=2.220e-16
    ventaja_W_t149         CPU=+0.002117679902  GPU=+0.002117679902  |dif|=4.441e-16
    interaccion_t149       CPU=+0.003250988366  GPU=+0.003250988366  |dif|=4.441e-16

[4] VEREDICTO DEL CONTROL DE INSTRUMENTO
    Las dos maquinas dan resultados IDENTICOS a 1e-9 en las 12 metricas.
```

**El desvio maximo global es 3,747e-15**, o sea **el epsilon del doble**, sobre 468 comparaciones (39 nulls x 12 metricas). Dos maquinas, dos backends (scipy CPU vs cupy sobre Tesla P100), el mismo numero hasta el ultimo bit representable.

---

## 3. 🚨 EL TEST GLOBAL, verbatim: **NO SIGNIFICATIVO**

```
"global": {
  "S_real": 239.0,
  "S_null_mean": 183.10256410256412,
  "S_null_sd": 45.20351341246949,
  "S_null_min": 95.0,
  "n_below": 35,
  "n_above": 4,
  "p_two_sided": 0.25,
  "floor": 0.05,
  "alpha": 0.05,
  "p_floor_reachable": true,
  "significant": false,
  "k_usable": 9,
  "k_total": 9
}
```

**`significant: false` con `p_floor_reachable: true`.** O sea: el experimento **si** tenia potencia para dar significativo con 39 nulls, y **no dio**. No es "falta n": es un resultado negativo.

### Los 9 estadisticos, uno por uno

```
estadistico            veredicto       real   null_mu   n_ge   n_le   p_two
rdi_Wc_tauC_t50        TESTEABLE     0.4311    0.4411     39      0  0.0500
ventaja_tau_t50        TESTEABLE     0.0020   -0.0014      0     39  0.0500
ventaja_W_t50          TESTEABLE     0.0000   -0.0001      6     33  0.3500
rdi_Wc_tauC_t100       TESTEABLE     0.7184    0.4163      0     39  0.0500
ventaja_tau_t100       TESTEABLE    -0.0228   -0.0115     39      0  0.0500
ventaja_W_t100         TESTEABLE    -0.0007   -0.0003     31      8  0.4500
rdi_Wc_tauC_t149       TESTEABLE     0.6642    0.1340      0     39  0.0500
ventaja_tau_t149       TESTEABLE     0.0060   -0.0564      0     39  0.0500
ventaja_W_t149         TESTEABLE     0.0021   -0.0036      6     33  0.3500
```

**Los 9 son TESTEABLE: ninguno se cayo por tautologia ni por NaN.** Seis dan el piso de 0,05 (extremos, 0/39 o 39/39) y **los tres del brazo `W` dan 0,35, 0,45 y 0,35.**

---

## 4. NO MEDIDO

- **El estadistico agregado `S` es un rank sum sobre los 9.** No se audito su construccion en este turno: se reporta lo que el motor calculo.
- El brazo REAL sigue siendo **una** corrida determinista, no una distribucion.
- `phase_jitter` **sigue sin barrerse**.
- `null_maslov_sneppen` no corrio sobre el grafo real (la corrida usa CP).
- CPU y GPU comparten semilla y algoritmo del null: el cruce valida el **backend**, no la eleccion del null. El 3,7e-15 mide aritmetica, no diseno.
- **No se barrio el tiempo entre t=50 y t=100**, donde esta el cruce de signo.
