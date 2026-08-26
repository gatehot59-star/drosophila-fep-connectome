# 104 · Sí, ya había terminado. Y el test global me refuta.

**Fecha:** 2026-08-26 · **Pregunta de Abraham:** ¿fuiste a ver lo que dejaste corriendo? ¿ya había terminado?

**Sí. Terminó a las 05:36 UTC (02:36 ART), o sea hace casi 6 horas, y yo no volví a mirar.**

Había puesto un recordatorio a las 02:55 para que me pinches. **Confié en el recordatorio en vez de chequear.** Eso es exactamente lo mismo que hice con Kaggle: los 4 shards estuvieron `complete` toda la noche mientras yo decía que no los podía ver.

---

## 1. Lo bueno: W-01 cerrado con el epsilon del doble

**390,5 minutos, cero tests en rojo, JSON de 121.099 B.**

El cruce contra los 4 shards de GPU, ahora con **precisión completa** (antes estaba limitado por el redondeo del log):

| | |
|---|---|
| comparaciones | **468** (39 nulls x 12 métricas) |
| desvio maximo | **3,747e-15** |
| desvio tipico | ~1e-16 |
| brazo REAL | **identico o a 5,5e-16** en las 12 |

Eso es **el epsilon del doble**. Dos maquinas distintas, dos backends distintos (scipy en CPU contra cupy en Tesla P100), el mismo numero hasta el ultimo bit representable. **Ya no soy el unico testigo, y no por un argumento: por 468 comparaciones.**

Corrige mi propio cruce anterior: el "4,975e-05" que reporte era **el redondeo del log**, no el desvio. Media mi instrumento, no el fenomeno.

---

## 2. Lo que me refuta, y es el titular

### El TEST GLOBAL da `significant: false`, p = 0,25

```
S_real=239.0  S_null_mean=183.1  sd=45.2  n_above=4/39  p_two_sided=0.25
p_floor_reachable=true   significant=FALSE
```

**Y `p_floor_reachable: true` es la parte que no deja escapar:** el experimento **si** tenia potencia para dar significativo con 39 nulls. No dio. **Es un resultado negativo, no una muestra chica.**

### Por que los "0 de 39" no alcanzan

En la respuesta 101 celebre que `rdi_t100` y `rdi_t149` daban **0/39**. Sigue siendo cierto. Lo que faltaba decir es que **el motor agrega los 9 estadisticos en un solo `S`**, y ahi:

- **6 de 9** dan el piso de 0,05, pero **en direcciones opuestas**: tres con 0/39 y tres con 39/39.
- **3 de 9** (todo el brazo `W`) dan **0,35, 0,45 y 0,35**: ruido.

Un agregado que suma seis extremos que se cancelan y tres nulos **no puede dar significativo**. El diseno del agregado esta castigando el resultado, y con razon: **es la correccion por multiples comparaciones que yo declare como pendiente, aplicada por el propio motor**. El motor v2 hizo lo que le pedi que hiciera.

### Los 9 son TESTEABLE

Ninguno se cayo por tautologia ni por NaN. **Los guards no taparon nada: el resultado es el resultado.**

---

## 3. Que sobrevive y que no, honesto

| afirmacion | estado |
|---|---|
| el conectoma real separa modalidades a t=100 y t=149 | **sobrevive como observacion**: 0/39 en las dos |
| …y eso es significativo | **NO**: el test global da 0,25 |
| el efecto es del grafo | **falso**: en t=50 el real queda **debajo** de los 39 nulls |
| la ventaja de tau es un mecanismo | **falso como mecanismo**: cambia de signo entre t=50 y t=100 |
| la aritmetica compleja en `W` aporta | **refutado**: 0,35 / 0,45 / 0,35 |

**Lo unico solido que queda es el cruce de signo entre t=50 y t=100.** Ahi hay un tiempo caracteristico en el que el conectoma empieza a separar, y **ese numero no esta medido**: hay 3 snapshots, no una curva. Es el experimento que sigue, y ahora cuesta minutos en GPU.

---

## 4. Y mate el proceso trabado

El `motor.py --null-kind ms` de mi sandbox llevaba **2 h 45 min al 99,7%** de un nucleo. Es el cuelgue patologico del null de Maslov-Sneppen que documente el 25-ago: **no estaba lento, estaba trabado**. `kill -TERM`, no respondio, `kill -KILL`. Load bajo de 1,48 a 1,01.

---

## 5. NO MEDIDO

- **No auditue la construccion del estadistico agregado `S`.** Se reporta lo que el motor calculo. Si el agregado esta mal disenado, el p=0,25 tambien lo esta, y eso **no lo verifique**.
- `phase_jitter` sigue sin barrerse.
- `null_maslov_sneppen` no corrio sobre el grafo real.
- El tiempo entre t=50 y t=100 sigue sin barrer.
- CPU y GPU comparten semilla: el 3,7e-15 valida **aritmetica**, no la eleccion del null.

```
--- METODO ---
Accion delicada: SI, una. Se mato un proceso (kill -KILL 3352) en MI sandbox,
                 no en el de Abraham. Es un cuelgue documentado, se declaro la
                 intencion en el turno anterior y no hubo objecion. Cero
                 procesos de brain-env tocados.
Instrumento:     tools/cierre_cpu_gpu_precision_completa.py, corrido antes de
                 commitearse. gateway build.run sobre brain-env.
Falsador:        el propio motor v2. Su test global agregado refuta la lectura
                 celebratoria que yo publique en la respuesta 101 con los mismos
                 numeros. El instrumento que escribi para no autoengañarme
                 funciono en mi contra, que es para lo que estaba.
Evidencia:       docs/agents/evidencia/2026-08-26-104-cierre-39-nulls-y-test-global.md
```
