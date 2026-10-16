# 067 · El Cell Type Explorer de FAFB publica la tabla entera

**Fecha:** 2026-08-25 01:30 (America/Buenos_Aires) · **Modo:** TITAN FULL

> **📄 Doc de ClickUp:** «LEÍ EL EXPLORER · y es peor de lo que pensaba»

---

## 1. Pedido

«Leé el Cell Type Explorer de LC9 ahora.» Era el ítem 1 de los NO MEDIDO de la resp 066, el que yo mismo marqué como capaz de tumbar lo que quedaba.

## 2. Herramientas declaradas (C-03)

| Llamada | Escribe | Cuota ajena |
|---|---|---|
| `fetch_website` × 4 (`reiserlab.github.io`) | no | no |
| `search_web` × 2 | no | no |
| `githubmcp_create_or_update_file` × 2 | sí, rama `titan/twohop-nulls` | no |
| `create_document` × 1 | sí, ClickUp | no |

**Cero mediciones locales, cero Kaggle, nada a Zenodo.**

---

## 3. Lo primero que encontré: el que buscaba NO era el correcto

El que apareció en el barrido de la resp 066 es el del **macho**, `male-drosophila-visual-system-connectome`, suplemento de **Nern et al. (2025), Nature**, doi:10.1038/s41586-025-08746-0, archivado en Zenodo 10891950.

**Ese NO tenía lo que yo temía.** Leí sus páginas de LC9 y de LC4 y el cerebro central aparece **como un solo compartimento agregado**:

```
LC9 (macho):  | central brain |  0 | 563.7  |  1 | 161.4 |
LC4 (macho):  | central brain |  0 | 276.8  |  1 | 316.6 |
```

Y su sección de conectividad se titula **«Optic Lobe Connectivity»**. **No enumera socios descendentes.** Así que ese no era prior art de mi tabla.

### 🔴 Pero buscando ese encontré otro, y ese sí

> **Female Adult Fly Brain – Cell Type Explorer**
> `reiserlab.github.io/celltype-explorer-drosophila-female-adult-fly-brain`

Su página de inicio, verbatim:

> *«Comprehensive neuron type catalog for the **flywire-fafb:v783b** dataset… For each neuron type in the dataset, we show morphological information, **connectivity patterns**, and spatial distributions. Data represents a temporal snapshot generated on **2026-05-18 23:51 from neuPrint**.»*

**`flywire-fafb:v783b` es exactamente mi dataset.** Y el catchísimo: mi `annotations.tsv` y mi `connectivity.parquet` son del mismo v783.

---

## 4. 🔥 La prueba: la página del Giant Fiber publica su lista de entradas completa

`DNp01_R.html`, verbatim de su encabezado:

```
DNp01(R)
2 Neurons · Right: 1 | Left: 1
16,400 Synapses · Post: 14,069 | Pre: 2,331
12,984 Connections · Upstream: 11,761 | Downstream: 1,223
```

**Sus DOS neuronas coinciden con mis dos.** Y su tabla de **Inputs**, primeras filas verbatim:

```
upstream partner        #    NT     conns    %In    CV
LC4 (R)                 50   ACh    1,679    14.3%  0.2
LPLC2 (R)               96   ACh      750     6.4%  0.6
DNp01 (R)                1   Unk      570     4.8%  0.0
JO-A5 (R)               15   5-HT     468     4.0%  0.4
DNp70 (R)                1   ACh      462     3.9%  0.0
PVLP122b (R)             2   ACh      290     2.5%  0.1
PVLP010 (R)              1   Glu      260     2.2%  0.0
```

**Y ahora lo que importa: barrí la lista entera de entradas del Giant Fiber, que tiene más de 300 filas y llega hasta socios con UNA sola conexión.**

| Tipo | ¿Aparece como entrada de DNp01? |
|---|---|
| **LC4** | **SÍ**, 1º de la lista, 14,3% |
| **LPLC2** | **SÍ**, 2º, 6,4% |
| **LC6** | **NO. Ni una sola fila.** |
| **LPLC1** | **NO. Ni una sola fila.** |
| **LC9** | **NO. Ni una sola fila.** |

**La lista baja hasta socios de 1 conexión e incluye `LCe04 (R)` con 1.** Si LC6 tuviera aunque sea una conexión con el Giant Fiber, estaría. **No está.**

> **Mi resultado de anoche — LC4 y LPLC2 sí, LC6 y LPLC1 no — está publicado como recurso navegable, sobre el mismo snapshot v783b, desde un catálogo hecho por el Reiser Lab.**

### Y la página de LC9 confirma que el catálogo cubre los descendentes

`LC9_R.html`, verbatim:

```
LC9(R)
179 Neurons · Right: 92 | Left: 87
```

**179. Es exactamente el número que medí yo con `cell_type == 'LC9'`.**

Y en su tabla de **entradas** aparecen descendentes con nombre propio: `DNp09 (R)`, `DNp11 (R)`, `DNp27 (R)`, `DNp71 (R)`, `DNp70 (R)`, `DNa11 (R)`, `DNpe024 (R)`, `DNpe031 (R)`, `DNg34 (R)`. **El catálogo enumera socios descendentes por tipo, uno por uno.**

---

## 5. El veredicto, sin atenuantes

**La tabla de ruteo visual→descendente NO es un hallazgo. Está publicada tres veces y de tres formas distintas:**

| Fuente | Qué publica |
|---|---|
| **Wu 2016 / von Reyn 2017 / Ache 2019 / Morimoto 2020** | la biología: LC4 y LPLC2 son las entradas del GF, con electrofisiología y genética; y adónde sí va LC6 |
| **Kind et al. 2024** (bioRxiv / eLife RP 99277) | la matriz VPN→DN **desde FAFB**, con las ausencias de LC6→DNp01 y LPLC1→DNp01 |
| **🆕 FAFB Cell Type Explorer** (`flywire-fafb:v783b`) | **la lista completa de socios de cada tipo, sobre MI mismo snapshot**, hasta socios de una sola conexión |

**Y el último es el que cierra la puerta:** no es un paper que analizó un subconjunto, es un catálogo exhaustivo del dataset entero. **Cualquier par que yo mida en v783b ya está ahí.**

### Lo que esto le hace a mi turno anterior

- ❌ **«Apareció una tabla de ruteo cruzado»** → **retirado por completo.** No apareció: la leí de otra forma.
- ❌ **«LC9 está cableado al otro canal» como hallazgo** → **retirado.** Está en el catálogo.
- ✅ **Mis números son correctos**, y ahora con **validación externa triple**: 2 neuronas de DNp01, 179 de LC9, y el patrón de presencia/ausencia. **B-01: cuando hay medición externa gana la externa, y acá coincide.** Eso es lo único bueno del turno y no es poco: **mi instrumento mide bien.**

---

## 6. 🟡 Qué sigue en pie, y es chico pero es real

Seis búsquedas y seis lecturas, y **esto no apareció en ninguna fuente**:

**1 · El null que preserva neuropilos aplicado a pares VPN→DN.** El Explorer publica **conteos**, no expectativas: no dice si un cero es sorprendente. Kind et al. barajan **identidades de sinapsis sobre la dendrita**, que es topografía, no existencia de conexión.

**2 · La métrica de oportunidad.** El dato de que **LC6 comparte 5.335 sitios sinápticos con el Giant Fiber contra 4.523 de LC4** no está en ninguna parte. El Explorer da innervación por ROI de cada tipo por separado (`PVLP_R` 41,8% de la entrada de LC9, etc.), **pero no cruza la de la fuente con la del blanco.**

**3 · La distinción entre los dos tipos de cero.** Que `LC6→GF` sobreviva el null anatómico y `LPLC1→GF` **no** lo sobreviva es una diferencia que solo existe si corés el null. **Ese es el aporte, y es de método.**

**En una línea:** el campo publicó **qué** está conectado. Lo que no publicó es **cuánto de eso es sorprendente**.

---

## 7. 🔥 Y un hallazgo lateral que SÍ sirve, y es sobre el motor

Leyendo la lista de entradas del Giant Fiber encontré esto, que no buscaba:

```
JO-A5 (R)      15  5-HT   468  4.0%   <- organo de Johnston, MECANOSENSORIAL
JO-B1_a (R)    21  ACh    121  1.0%
JO-B1_c (R)    10  Unk    109  0.9%
AMMC-A1 (L)     2  Unk     88  0.7%
JO-CA1 (R)      4  Unk     12  0.1%
JO-DA (R)       6  ACh     10  0.1%
```

Y su innervación por región: **`AMMC_R` es el 33,5% de toda su entrada**, más que `PVLP_R` con 30,7%.

> **El Giant Fiber no es un circuito visual: recibe MÁS entrada del neuropilo mecanosensorial-auditivo (AMMC) que del visual (PVLP).**

**Eso le hace algo directo a la entrada de la biblioteca**, que yo escribí como «fan-in de 314 detectores visuales → 2 actuadores». **Es falso por omisión: falta toda la rama mecanosensorial.** Y explica algo que medí compilando y no supe interpretar: el circuito **no discrimina perfiles temporales (1,04×) y responde a flicker (1,12×)** porque **no es un detector de aproximación visual, es un integrador multimodal de urgencia.**

**Esa corrección vale más que la tabla que perdí**, y salió de leer prior art en vez de medir.

---

## 8. La regla que sale, y es dura

**Antes de medir un par en un conectoma público, buscar si existe un catálogo navegable de ese snapshot.** No un paper: un **catálogo**. Los conectomas grandes vienen con explorers exhaustivos, y **cualquier conteo de pares que yo haga sobre v783b está ahí por construcción.**

Y el corolario, que reformula el objetivo del proyecto entero: **medir un conteo sobre un conectoma público no puede ser el aporte, porque el conteo ya está publicado.** El aporte solo puede estar en **la expectativa contra la que se compara ese conteo**. O sea: **el null es el producto, no el número.**

---

## 9. NO MEDIDO, declarado

1. **NO leí la tabla de SALIDAS de LC9.** La página se corta después de las entradas. **No verifiqué directamente que `LC9 → DNp09` figure ahí**, aunque el catálogo enumera descendentes y por sim etría debe estar. **Apoyado, no establecido.**
2. **No piné la cita exacta del Explorer de FAFB.** El del **macho** es Nern et al. 2025 (Zenodo 10891950); **el de FAFB no declara su publicación en la home**, solo el snapshot de neuPrint. Antes de citarlo hay que resolverlo.
3. **Las unidades del Explorer no son las mías.** Su `conns` para LC4→DNp01 es **1.679** y yo medí **104 aristas**; su tabla es **por hemisferio** y probablemente cuenta sinapsis. **La coincidencia está verificada en presencia/ausencia y en conteo de neuronas, NO en magnitud.**
4. **No barrí el Explorer buscando si publican expectativas o nulls** en alguna otra página.
5. **El hallazgo de la §7 (AMMC 33,5% > PVLP 30,7%) sale de su tabla de ROI, no de medición propia.** No lo re-medí sobre mi parquet, **y hay que hacerlo antes de escribirlo en ninguna parte.**
6. **La entrada de biblioteca sigue diciendo «fan-in de 314 visuales»** y eso es falso por omisión. **Sin corregir.**
7. **Los contextos siguen sin actualizar** con las resp 065, 066 y 067.
