# Biblioteca de circuitos · Entrada 01

# El cuello de botella del escape (Giant Fiber / DNp01)

**Versión:** 2 · **Corregida:** 2026-08-25 01:30 · **Dataset:** FlyWire FAFB v783
**Instrumento:** `src/escape_neuropil_null.py` md5 `c04ddd4282ada4f9df462f87d84d85ba` + mediciones de la §7.

> ## 🔴 LA VERSIÓN 1 DE ESTA ENTRADA ERA FALSA POR OMISIÓN
>
> Decía: *«Fan-in exclusivo con doble canal. 314 detectores → 2 actuadores… 0 aristas inhibitorias de 13.026.»*
>
> **Medido sobre las 962 aristas de entrada reales del Giant Fiber:** la vía visual (LC4 + LPLC2) es el **20,0% de las sinapsis de entrada**, las neuronas **centrales** son el **67,6%**, y **el 49,8% de las sinapsis de entrada son INHIBITORIAS**.
>
> **El «0 inhibitorias» era cierto de un recorte del 20% que presenté como si fuera el circuito.** Y ese error explica el resultado funcional que no supe interpretar: el circuito compilado no discrimina perfiles temporales (**1,04×**) porque le había sacado la mitad inhibitoria y el 68% de sus entradas.
>
> **Y se retira también el claim de la resp 067** de que el GF recibe más del AMMC mecanosensorial que del PVLP visual. Ver §6.

---

## 1. Qué es, en una línea

**Un cuello de botella de 2 neuronas que integra entrada multimodal y la envía al cordón**, con la vía visual rápida como una de sus fuentes y no como su definición.

**No es un detector de aproximación.** No es un fan-in visual. Es un **integrador con umbral** cuyo diseño está dominado por control central e inhibición.

---

## 2. Presupuesto de entrada, medido (por sinapsis)

```
ENTRADAS TOTALES AL GF:  962 aristas  ·  9.474 sinapsis  ·  2 neuronas blanco

super_class            aristas   sinapsis    %
central                    567      6.403   67,6%
visual_projection          299      1.899   20,0%
descending                  32        831    8,8%
sensory                     39        187    2,0%
ascending                   19        127    1,3%
visual_centrifugal           6         27    0,3%
```

**La vía visual es un quinto del presupuesto. Dos tercios son control central.**

### Signo, y es el número que cambia el diseño

```
Excitatory     aristas   sinapsis
  +1              595      4.752   (50,2%)
  -1              367      4.722   (49,8%)
```

**Prácticamente mitad y mitad.** Las inhibitorias son menos aristas pero más pesadas por arista (12,9 sinapsis/arista contra 8,0).

---

## 3. Las entradas nombradas, top 10 por sinapsis

```
cell_type    aristas  sinapsis   qué es
LPLC2            189     1.080   proyección visual, detector de looming
LC4              104       805   proyección visual, velocidad angular
CB3707             8       633   central, GABA
DNp70              4       587   DESCENDENTE que alimenta a otra descendente
SAD014            12       292   central, GABA, en SAD
PVLP122b           8       281   central, ACh
LHAD1g1            2       254   central, GABA
PVLP010            2       250   central, Glu
CL038              4       249   central, Glu
CB0010             2       223   central, GABA
...
JO-A5             15        95   órgano de Johnston, MECANOSENSORIAL, 5-HT
JO-B1_a           21        65   órgano de Johnston, ACh
```

**Cuatro de las diez primeras son GABAérgicas.** Y **DNp70** es notable por sí solo: una descendente que aporta 587 sinapsis a otra descendente, más que cualquier socio central individual.

---

## 4. Ruteo de entrada visual, contra el null que preserva neuropilos

**40 realizaciones, permutando destinos solo dentro de cada par (neuropilo origen, neuropilo destino).** Familia del NPC model de Lin et al. (2024).

| Fuente | → Giant Fiber | → DNp09 |
|---|---|---|
| **LC4** | **104** · null 9,6 · **10,8×** · z +31,6 · 0/40 | **0** · null 5,0 · z −2,4 · 40/40 |
| **LPLC2** | **189** · null 19,4 · **9,8×** · z +39,0 · 0/40 | **32** · null 11,4 · **2,8×** · z +5,9 · 0/40 |
| **LC6** | **0** · null 17,2 · z **−5,6** · 40/40 | **1** · null 8,7 · z −3,0 · 40/40 |
| **LC9** | **0** · null 11,9 · z **−4,0** · 40/40 | **114** · null 15,1 · **7,6×** · z +28,5 · 0/40 |
| **LPLC1** | 0 · null 0,2 · **NO TESTEABLE** | **0** · null 16,8 · z **−4,9** · 40/40 |

**⚠️ La tabla de conectividad NO es un aporte de este trabajo.** Está publicada en **Kind et al. (2024)** desde el mismo dataset, en el **FAFB Cell Type Explorer** (`flywire-fafb:v783b`) como catálogo navegable, y su biología en **Wu (2016)**, **von Reyn (2017)**, **Ache (2019)** y **Morimoto (2020)**.

**Lo único propio de esta sección son las columnas de null**, y la distinción que habilitan:

| Cero | El null anatómico predice | Veredicto |
|---|---|---|
| **LC6 → GF** | **17,2 ± 3,1**, mínimo de 40 = 12 | 🟢 **exclusión**, no geometría |
| LC9 → GF | 11,9 ± 3,0 | 🟢 **exclusión** |
| LPLC1 → DNp09 | 16,8 ± 3,4 | 🟢 **exclusión** |
| **LPLC1 → GF** | **0,2 ± 0,4** | 🔴 **geometría.** El null conserva el cero: NO TESTEABLE |

### La medida de oportunidad que sostiene el veredicto de LC6

`shared_min_sites` = suma por neuropilo del mínimo entre sitios de salida de la fuente y sitios de entrada del blanco.

| Par | Sitios compartidos | Aristas reales |
|---|---|---|
| **LC6 → GF** | **5.335** | **0** |
| LC9 → GF | 5.335 | 0 |
| LPLC2 → GF | 5.075 | 189 |
| **LC4 → GF** | **4.523** | **104** |
| LPLC1 → GF | 4.478 | 0 |

**LC6 tiene más oportunidad que LC4 y conecta cero donde LC4 conecta 104.** Neuropilo dominante de salida de LC6: **PVLP** (68.082 sitios). Neuropilo dominante de entrada del GF: **PVLP** (4.085 sitios). Mismo territorio.

---

## 5. Comportamiento funcional, medido compilando

| Qué | Número | Cómo se midió |
|---|---|---|
| **Ganancia entrada cableada / no cableada** | **40×** (LC4+LPLC2 = 0,704 · LC6 = 0,017) | compilado en el motor propio |
| Convergencia de los dos detectores | LPLC2 sola 0,627 · LC4 solo 0,336 · juntos 0,704 | ídem |
| Especialización del segundo canal | LPLC2→DNp09 = 0,658 · LC4→DNp09 = 0,075 | ídem, **y predicho por el cableado** |
| **Selectividad temporal** | **1,04×** (looming 0,7034 · receding 0,6772) | ídem |
| Selectividad espacial | `looming / full = 0,993` | ídem |
| Respuesta a intermitencia | **1,12×** (flicker) | ídem |

**🔴 Y ahora se sabe por qué la selectividad da 1,04×:** lo compilado fue el **20% excitatorio** del circuito. **Le faltaba el 67,6% central y el 49,8% inhibitorio.** No es que la topología no genere selectividad: es que se compiló un recorte que no puede generarla.

**El experimento que falta y que ahora tiene sentido pedir:** compilar las 962 aristas con signo y ver si la selectividad temporal aparece. **Es la primera vez que este circuito tiene una predicción falsable propia.**

---

## 6. 🔴 Corrección de la resp 067: el AMMC no es lo que dije

La resp 067 afirmó, leyendo la tabla de ROI del Cell Type Explorer, que *«el Giant Fiber recibe MÁS entrada del neuropilo mecanosensorial-auditivo (AMMC, 33,5%) que del visual (PVLP, 30,7%)»*.

**Falso, y es E-01 otra vez, ahora sobre una tabla de terceros.** El 33,5% del Explorer es **dónde están LOCALIZADAS las sinapsis de entrada del GF**, no **quién se las da**. Medido sobre el parquet, cruzando neuropilo de origen del socio con su clase:

```
neuropilo    ascending  central  descending  sensory  vis_centrif  vis_proj    TOT
AVLP_R              22    1.385           4        0            0         1  1.412
PVLP_R               0      233           0        0           22     1.053  1.308
PVLP_L               1      446           0        0            2       832  1.281
AVLP_L              19      857          16        0            0         0    892
GOR_R                0      848           0        0            0         0    848
GNG                 83      283         380        0            0         0    746
AMMC_L               1      225         266       35            0         0    527
SAD                  1      350          52       16            0         0    419
AMMC_R              45      333 (agregado)                                    333
```

**De las 2.126 sinapsis que llegan desde AMMC, SAD, GNG y WED, solo 187 son sensoriales directas.** El resto entra por **interneuronas centrales** (CB0010 con 223, CB3877 con 80, SAD014 con 74…) y por **DNp70** con 587.

**El enunciado correcto:** el GF recibe entrada mecanosensorial **indirecta y sustancial** a través del AMMC y el SAD, pero la entrada **sensorial directa es el 2,0%**. La comparación «más AMMC que PVLP» mezcla **localización de sinapsis** con **origen de la señal** y se retira.

**Y esto es lo más incmómodo del día:** el turno anterior corrigió un claim mío leyendo prior art, y **al leerlo cometió el mismo tipo de error sobre la fuente nueva**, sin medirla. La regla ya estaba escrita.

---

## 7. Evidencia cruda de esta versión, verbatim

```
GF_neuronas 2
ENTRADAS_TOTALES_AL_GF aristas 962 sinapsis 9474

--- por super_class ---
                    aristas  sinapsis
central                 567      6403
visual_projection       299      1899
descending               32       831
sensory                  39       187
ascending                19       127
visual_centrifugal        6        27

--- por cell_class ---
                aristas  sinapsis
NA                  902      9158
mechanosensory       39       187
AN                   19       127
bilateral             1         1
ocellar               1         1

--- signo de las entradas ---
            aristas  sinapsis
Excitatory
-1              367      4722
 1              595      4752

--- quien aporta en AMMC/SAD/GNG/WED ---
DNp70        descending       587
CB0010       central          223
JO-A5        sensory           95
CB3877       central           80
AN_GNG_SAD_3 ascending         75
SAD014       central           74
CB3486       central           70
JO-B1_a      sensory           65
sinapsis totales desde esos neuropilos: 2126 de 9474
de esas, SENSORIALES directas: 187
```

Recomputable: **si las entradas al GF no dan 962 aristas y 9.474 sinapsis, o si la fracción inhibitoria no da 49,8%, esta entrada se cae.**

---

## 8. La ficha, como iría en una hoja de datos

> **GF-01 · Cuello de botella de escape, 2 salidas.**
>
> **Entrada:** 962 conexiones, 9.474 sinapsis. Central **67,6%** · proyección visual **20,0%** · descendente **8,8%** · sensorial directa **2,0%** · ascendente 1,3%.
> **Signo:** **49,8% de las sinapsis de entrada son inhibitorias.** No es un sumador excitatorio.
> **Salida:** 2 neuronas al cordón. **0 aristas a motoras del cerebro.**
> **Ruteo visual verificado contra null anatómico:** admite LC4 (10,8×) y LPLC2 (9,8×); **excluye LC6 (z −5,6) y LC9 (z −4,0)** teniendo más oportunidad que LC4. LPLC1 no aplica: su cero es geometría.
> **Ganancia medida compilando el recorte visual excitatorio:** 40× entre entrada cableada y excluida.
> **Selectividad temporal del recorte:** 1,04×, o sea ninguna. **No extrapolar al circuito completo: el recorte omite el 80% de la entrada.**
> **Prior art obligatorio:** Wu 2016 · von Reyn 2017 · Ache 2019 · Morimoto 2020 · Kind et al. 2024 · FAFB Cell Type Explorer v783b. **La conectividad es de ellos; el estatus estadístico de las ausencias es de este trabajo.**
> **Sin umbral de sinapsis.** No comparable con Lin, Bates ni el Explorer en magnitud.

---

## 9. NO MEDIDO

1. **Las 962 aristas no se compilaron.** Es el experimento que esta corrección habilita y no se corrió.
2. **`shared_min_sites` es una cota de oportunidad, no contacto.** No se midió distancia entre árboles.
3. **El null asigna un neuropilo dominante por neurona**, no reparte sinapsis: familia del NPC, no idéntico. **No preserva el grado entrante exacto**, solo dentro de bloque.
4. **Sin umbral de ≥5 sinapsis** en ninguna de estas cifras.
5. **Los pares →DNp09 usan `cell_type` (2 neuronas).** Con `hemibrain_type` son 4 y el conteo cambia (170 contra 32). **No re-corrido.**
6. **El `0 inhibitorias de 13.026` de la v1 no se re-verificó** sobre su propio subgrafo: se declaró fuera de alcance, no falso. Lo que está medido es que **el circuito completo sí tiene inhibición masiva**.
7. **No se midió qué hacen los 567 socios centrales.** Son dos tercios del circuito y siguen siendo una caja negra.
8. **DNp70 → GF (587 sinapsis) no se caracterizó.** Es la mayor entrada individual no visual y no sé qué hace.
9. **La entrada no está en el paper ni en el README.**
