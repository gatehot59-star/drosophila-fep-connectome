# EVIDENCIA CRUDA · 2026-08-26 · extras: semilla, jitter, escala y RSS

**Instrumento:** kernel privado de Kaggle `titan-cierre-extras-semilla-jitter-escala-rss`,
backend **CPU** (declarado: su costo dominante es CPU y las 4 sesiones GPU estaban
ocupadas por los shards del A/B). Fuentes verificados por md5 al arrancar.

---

## 1. DISTRIBUCION de la semilla de fase — el punto se vuelve intervalo

12 realizaciones con `jitter=0.1`, sobre el conectoma real.

```
  cantidad       media           sd            min           max           rango/media %
  rho_pre        2153.755894     0.566233      2152.635549   2154.527216   0.0878%
  rdi_t50        0.021868        0.000047      0.021794      0.021965      0.7785%
  rdi_t100       0.758566        0.001037      0.757182      0.760590      0.4494%
  rdi_t149       0.606678        0.000705      0.605482      0.607891      0.3971%
```

**Lo que cierra:** en la respuesta 106 el «0,0472%» era **un punto**, la diferencia entre
dos realizaciones. Ahora es un **intervalo medido**: el rango completo de `rho` sobre 12
semillas es **0,0878%**, con `sd = 0,566`. El 0,0472% que yo reporte cae **dentro** de esa
dispersion, o sea que era una realizacion tipica y no un caso raro.

Y la escala importa: la dispersion del `rdi` por semilla de fase es de **0,4 a 0,8%**,
mientras que el efecto que el experimento persigue (real 0,6642 contra media null 0,1340)
es de **396%**. **El ruido de fase es dos ordenes de magnitud mas chico que el efecto.**

---

## 2. BARRIDO de phase_jitter — y aparece algo NO MONOTONO

```
  jitter    rho_pre         rdi_t50   rdi_t100  rdi_t149
  0.00      2164.292805     0.021787  0.758431  0.607364
  0.02      2163.825335     0.021781  0.758192  0.607370
  0.04      2162.423518     0.021784  0.757996  0.607333
  0.06      2160.089123     0.021796  0.757847  0.607259
  0.08      2156.825095     0.021817  0.757745  0.607156
  0.10      2152.635549     0.021849  0.757692  0.607032
  0.20      2118.029248     0.022157  0.758128  0.606228
```

**`rho` baja de forma monotona** con el jitter, y eso es esperable: mas dispersion de fase
hace que las multi-aristas se cancelen mas al fundirse, y el radio espectral cae. De 0 a
0,20 la caida es de **2,14%**.

**Pero los `rdi` NO son monotonos, y eso es un hallazgo:**

- `rdi_t50` **baja** hasta jitter 0,02 (0,021787 -> 0,021781) y despues **sube** hasta
  0,022157 en 0,20. Hay un minimo alrededor de 0,02-0,04.
- `rdi_t100` **baja** hasta 0,10 (0,758431 -> 0,757692) y despues **sube** a 0,758128.
- `rdi_t149` es el unico casi monotono: baja siempre, 0,607364 -> 0,606228.

**Por que importa:** si el jitter fuera solo ruido aditivo, los `rdi` se moverian en una
sola direccion o se quedarian planos. Que tengan un minimo interior significa que
`phase_jitter` **no es un parametro de ruido: es un parametro del modelo** que interactua
con la separacion de modalidades. El peritaje 092 marco que «`phase_jitter = 0,1` nunca se
barrio» y lo llamo «injustificado, no mal elegido». Medido: 0,1 **no** es un optimo ni un
extremo, esta en la mitad de una curva con estructura.

**Magnitud, para no inflarlo:** el rango completo de `rdi_t50` en todo el barrido es de
**1,7%** de su valor. Es estructura real y es chica.

---

## 3. ESCALA hasta el n REAL — y la extrapolacion de la 106 era PESIMISTA

Sub-muestreando el grafo real, no sinteticos.

```
  n         aristas     pesos v2/v1            normaliz. v2/v1        propagate v2/v1
  17329     234502      0.0361/0.0276 = 1.31   1.6769/0.3054 = 5.49   0.0581/0.0578 = 1.01
  34659     941471      0.1587/0.1132 = 1.40   6.9167/1.3095 = 5.28   0.2026/0.2096 = 0.97
  69319     3730187     0.6619/0.4978 = 1.33   30.0133/5.7903 = 5.18  0.8157/0.8277 = 0.99
  138639    15091983    3.1862/2.2320 = 1.43   48.4124/22.6452 = 2.14 3.6444/3.6517 = 1.00
```

**Tres cosas, y una me corrige:**

1. **`propagate` da 0,97 a 1,01 en los cuatro tamanos.** El nucleo no se toco a ninguna
   escala, ahora medido tambien sobre el grafo real y hasta 15 millones de aristas.

2. **El cociente de `normalizacion` CAE al llegar al n real: 5,49 -> 5,28 -> 5,18 -> 2,14.**
   La respuesta 106 dijo «queda plano en ~4,5-5,5x» sobre sinteticos hasta n=64.000. **En
   el grafo real completo es 2,14.** Mi extrapolacion era **pesimista por 2,4 veces**.
   La causa probable es que a 15M de aristas el costo del SpMV domina sobre el costo fijo
   de correr dos instrumentos espectrales, pero **eso es una hipotesis, no esta medido**.

3. **`pesos` se mantiene en 1,31-1,43**, sin la tendencia creciente clara que sugeria el
   barrido sintetico (1,57 -> 2,12). Sobre el grafo real el cociente es **mas bajo y mas
   estable** que sobre sinteticos del mismo tamano.

**Leccion de metodo:** el barrido sintetico de la 106 predijo mal las dos tendencias. Un
grafo sintetico con la misma cantidad de nodos **no es** un modelo del conectoma para
medir performance, porque la estructura de la matriz cambia el comportamiento del solver.

---

## 4. RSS REAL — y tracemalloc estaba exagerando

`ru_maxrss` del proceso hijo, que si ve los buffers de BLAS/ARPACK y el heap de numpy.

```
  n         etapa   v1 pico          v2 pico          v2/v1
  64000     pesos   2445.9           2475.0           1.012
  64000     norm    2446.4           2496.6           1.021
  138639    pesos   2639.9           2731.4           1.035
  138639    norm    2639.9           2731.4           1.035
```

**La 106 reporto `normalize_spectral` en 2,079x con tracemalloc. El RSS real da 1,021x.**

Los dos numeros son correctos y miden cosas distintas: `tracemalloc` ve **solo las
allocaciones de Python** en el intervalo, y ahi la copia extra de v2 es una fraccion
grande de lo poco que se asigna. El RSS ve **todo el proceso**, donde esa copia es una
fraccion chica de 2,6 GB. **Para decidir si la memoria es un limite, manda el RSS.**

**Y el numero absoluto es el que importa: 2,7 GB de pico sobre los 7,99 GB del container.**
Un tercero. No es un limite hoy, y con dos corridas en paralelo si lo seria.

---

## 5. NO MEDIDO

- Este kernel corrio en **CPU**, no en GPU. Los cocientes de `propagate` son CPU-vs-CPU.
- Las 12 semillas son de `jitter=0.1` **unicamente**: no se midio la dispersion a otros
  valores de jitter.
- El barrido de jitter es de **una** semilla (42) por punto. La no monotonia de los `rdi`
  esta **por encima** de la dispersion por semilla en `rdi_t50` (rango 1,7% contra sd
  0,22%) pero **por debajo** en `rdi_t100`. O sea: **la no monotonia de t50 sobrevive al
  ruido de semilla y la de t100 NO esta establecida.**
- La causa de la caida del cociente de normalizacion a n real (2,14) **es una hipotesis**:
  no se perfilo donde se va el tiempo.
- El sub-muestreo del grafo real toma los nodos con indice menor a nn, o sea que **no es
  un sub-grafo aleatorio**: hereda el orden de los indices del conectoma.
- El RSS se midio con grafos sinteticos en el proceso hijo, no con el conectoma real.
