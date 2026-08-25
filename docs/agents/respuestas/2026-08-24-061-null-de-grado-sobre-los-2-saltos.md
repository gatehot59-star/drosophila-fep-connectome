# 061 · Null de grado sobre los 2 saltos: la asimetría sobrevive, y por goleada

**Fecha:** 2026-08-24 23:40 (America/Buenos_Aires)

> **📄 Doc de ClickUp:** «EL NULL DE GRADO CERRÓ · el acceso motor a 2 saltos sobrevive, y el 105 vs 110 se resolvió»

## 1. Pedido

«Corré el null de grado sobre los 2 saltos». Era el ítem 11 de la §5 de `CONTEXTO-drosophila-fep.md`: sin él, el rescate de la Propiedad 2 era una observación cruda y no un resultado.

## 2. Herramientas declaradas (C-03)

| Llamada | Escribe | Cuota ajena |
|---|---|---|
| `gateway build.run` × 6 sobre `brain-env` | solo `/tmp` (`null2h.log`, `guard.log`) | **NO** |
| `githubmcp_create_or_update_file` × 3 | sí, `main` | no |
| `create_document` × 1 | sí, ClickUp | no |

**Cero Kaggle. Nada publicado en Zenodo. `/workspace` solo leído: nada creado, movido ni borrado ahí.** CPU: **292,7 s** de una sola corrida, más ~40 s del guard.

---

## 3. ✅ DEUDA CERRADA PRIMERO: el 105 vs 110 ya no es un misterio

Era el ítem 12 de la §5. Medido:

```
nodos_en_grafo 138639
super_class==motor: total 110 en_grafo 110 fuera 0
cell_class que contienen motor: [('brain_motor_neuron', 105, 105), ('neck_motor_neuron', 1, 1)]
cell_class de las motoras: {'brain_motor_neuron': 105, nan: 4, 'neck_motor_neuron': 1}
flow de las motoras: {'efferent': 106, 'intrinsic': 4}
nerve EN grafo: {'PhN': 40, 'MxLbN': 26, 'CV': 20, 'AN': 14, 'ON': 10}
status EN grafo: {nan: 101, 'outlier_seg': 9}
```

**Los dos conjuntos son anidados y la diferencia son 5 neuronas exactas:**

```
110 (super_class == 'motor')  =  105 brain_motor_neuron
                               +   1 neck_motor_neuron
                               +   4 sin cell_class  (los 4 'intrinsic' del flow)
```

**La resp 053b usó `cell_class == 'brain_motor_neuron'` (105) y la 057 usó `super_class == 'motor'` (110).** Ninguna estaba mal: eran dos poblaciones distintas y no lo dije. **Los dos denominadores quedan medidos en paralelo en todo lo que sigue**, así que el resultado no depende de la elección. Y **las 110 están todas en el grafo**, o sea que no hay pérdida por intersección. **9 de las 110 tienen `status = outlier_seg`**, que es una salvedad nueva y va declarada.

---

## 4. El diseño, y por qué hay DOS estadísticos

**El null:** permutación global del vector de destinos. Preserva **exactamente** el grado de salida de cada nodo (el vector de orígenes no se toca) y **exactamente** el grado de entrada de cada nodo (el multiconjunto de destinos se conserva). Es la familia configuración / Maslov-Sneppen. **40 nulls, semillas `1000 + 7i`.**

**Y dos estadísticos, porque el primero no alcanza:**

| Estadístico | Qué cuenta | Problema |
|---|---|---|
| **R2** | cuántas motoras distintas se alcanzan a 2 saltos | **se satura**: el null llega a 110 de 110 siempre |
| **P2** | **cuántos caminos de 2 saltos** hay hasta motoras | **graduado, no se satura, y es el que responde al grado** |

`P2 = suma sobre v de (aristas de la clase hacia v) × (aristas de v hacia motoras)`. Es la cantidad que un null de grado **debería** predecir bien si la anatomía no importara, y por eso es el test.

---

## 5. Los guards, y este sí puede dar rojo

**Primero, un error propio declarado:** en la corrida grande imprimí un `grado_check_in` que compara `bincount(dst)` **contra sí mismo**. Da `True` siempre. **Es un test que no puede fallar, o sea el modo de falla 6 de este proyecto, cometido de nuevo y en el mismo turno en que lo estoy citando.** Lo corrí aparte y bien:

```
GUARD in-degree permutacion vs real: IGUAL_OK
CONTROL NEGATIVO dst uniforme (DEBE romper grado): DISTINTO_OK_el_guard_puede_dar_rojo
  nodos con in-degree roto por el uniforme: 138142 de 138639
aristas que cambiaron destino: 15091661 de 15091983
self-loops: real 0 null 317
```

**La permutación preserva el grado entrante exacto; el método uniforme lo rompe en 138.142 de 138.639 nodos.** El guard distingue los dos casos, así que puede dar rojo.

**Segundo, un control positivo que es un espejo A PROPÓSITO.** Metí en la misma corrida una cantidad que el null **debe** conservar por construcción, el total de aristas que entran a motoras:

```
RESULTADO _EDGES_INTO_MOT real (0, 0, 19860, 0, 0)
  nullmean [.., .., 19860.0, .., ..]  nullsd [.., .., 0.0, .., ..]
  nulls_ge_real [.., .., 40, .., ..]  min 19860  max 19860
```

**`sd = 0,0` exacto y 40/40 iguales al real.** Eso es el modo de falla 2 en vivo: si el estadístico principal se hubiera comportado así, el veredicto correcto era **NO TESTEABLE**. **No se comportó así**, y ahora está demostrado en la misma corrida en vez de argumentado.

---

## 6. 🔥 EL RESULTADO

### Evidencia cruda verbatim, sin recortar

Formato de cada tupla: `(R1_de_110, R2_de_110, P2_caminos, R1_de_105, R2_de_105)`

```
nodos 138639 aristas 15091983 carga_s 4.6
motoras110 110 motoras105 105
tam_clases {'olfactory': 98036, 'visual': 57764, 'mechanosensory': 98782,
            'gustatory': 25624, 'CTRL_random_10855': 1187513}
REAL {'olfactory': (0, 23, 901, 0, 23), 'visual': (0, 15, 1413, 0, 15),
      'mechanosensory': (64, 110, 293022, 64, 105),
      'gustatory': (10, 107, 67439, 10, 102),
      'CTRL_random_10855': (110, 110, 312457, 105, 105),
      '_EDGES_INTO_MOT': (0, 0, 19860, 0, 0)}

RESULTADO olfactory real (0, 23, 901, 0, 23)
  nullmean [71.325, 110.0, 39522.55, 70.225, 105.0]
  nullsd [4.628, 0.0, 745.663, 4.629, 0.0]
  nulls_ge_real [40, 40, 40, 40, 40]
  min [56, 110, 37882, 55, 105]  max [80, 110, 40879, 78, 105]

RESULTADO visual real (0, 15, 1413, 0, 15)
  nullmean [52.275, 110.0, 23311.55, 51.45, 105.0]
  nullsd [5.234, 0.0, 405.338, 5.186, 0.0]
  nulls_ge_real [40, 40, 40, 40, 40]
  min [43, 110, 22461, 42, 105]  max [68, 110, 24303, 67, 105]

RESULTADO mechanosensory real (64, 110, 293022, 64, 105)
  nullmean [70.65, 110.0, 39787.8, 69.4, 105.0]
  nullsd [4.922, 0.0, 740.236, 4.758, 0.0]
  nulls_ge_real [35, 40, 0, 35, 40]
  min [57, 110, 38474, 57, 105]  max [79, 110, 41334, 77, 105]

RESULTADO gustatory real (10, 107, 67439, 10, 102)
  nullmean [27.45, 109.95, 10304.1, 27.2, 105.0]
  nullsd [4.213, 0.218, 229.68, 4.142, 0.0]
  nulls_ge_real [40, 40, 0, 40, 40]
  min [17, 109, 9870, 17, 105]  max [36, 110, 10753, 36, 105]

RESULTADO CTRL_random_10855 real (110, 110, 312457, 105, 105)
  nullmean [109.0, 110.0, 479029.575, 104.625, 105.0]
  nullsd [0.975, 0.0, 7188.54, 0.484, 0.0]
  nulls_ge_real [15, 40, 40, 25, 40]
  min [106, 110, 462576, 104, 105]  max [110, 110, 494719, 105, 105]

FIN t= 292.7
```

### La tabla del veredicto, sobre P2 (caminos de 2 saltos)

| Clase | Real | Null μ | Null sd | Ratio | z | nulls ≥ real |
|---|---|---|---|---|---|---|
| **olfactory** | 901 | 39.522,6 | 745,7 | **0,0228×** (43,9× depletado) | **−51,8** | **40/40** |
| **visual** | 1.413 | 23.311,6 | 405,3 | **0,0606×** (16,5× depletado) | **−54,0** | **40/40** |
| **mechanosensory** | 293.022 | 39.787,8 | 740,2 | **7,37× enriquecido** | **+342,1** | **0/40** |
| **gustatory** | 67.439 | 10.304,1 | 229,7 | **6,54× enriquecido** | **+248,8** | **0/40** |

**Los cuatro son extremos del ensemble, en las dos direcciones, con `p` de una cola ≤ 1/41 = 0,0244.** El spread entre extremos es **323,2×**, y eso es notable por sí solo: **el 1 salto contra nulls de grado daba 283×**. Dos mediciones independientes, dos profundidades distintas, mismo orden de magnitud.

### 🆕 Y el control aleatorio destapó un piso que yo no tenía en cuenta

```
CTRL_random_10855   real 312.457   null 479.029,6   ratio 0,652×   40/40 nulls >= real
```

**Un conjunto de 10.855 nodos elegidos al azar TAMBIÉN está por debajo de su propia expectativa de grado, 0,652×.** O sea: **el conectoma real tiene menos caminos de 2 saltos que un grafo de configuración en general**, no solo para las clases sensoriales. Hay un factor de compresión global de ~0,65 que **no** es específico de nada.

**Consecuencia directa: los ratios crudos están inflados y hay que leerlos contra 0,652, no contra 1,0.**

| Clase | Ratio crudo | **Ratio normalizado por el piso** |
|---|---|---|
| olfactory | 0,0228× | **0,0350×** → 28,6× depletado |
| visual | 0,0606× | **0,0929×** → 10,8× depletado |
| mechanosensory | 7,37× | **11,29×** |
| gustatory | 6,54× | **10,03×** |

**El spread no cambia (323,2×): es invariante a la normalización.** Pero los ratios individuales sí, y **si esto no se declara, un revisor que corra su propio control lo encuentra.** Ese control lo agregué porque quería un piso, y terminó corrigiendo mis propios números hacia abajo en el lado depletado y hacia arriba en el enriquecido.

### El cero de 1 salto queda MUCHO más fuerte que antes

Hasta hoy el cero era «cero». Ahora tiene expectativa:

| Clase | Motoras alcanzadas a 1 salto | Null μ | z |
|---|---|---|---|
| **olfactory** | **0** | **71,3 ± 4,6** | **−15,4** |
| **visual** | **0** | **52,3 ± 5,2** | **−10,0** |

**El grado solo predice que olfatorio debería tocar ~71 de las 110 motoras, y toca 0.** Ningún null bajó de 56 (olfatorio) ni de 43 (visual). **Eso es lo más limpio del turno.**

### Y R2 está CENSURADO, no invalidado

R2 da `sd = 0,0` porque **los 40 nulls llegan al techo de 110**. **No es el espejo del modo de falla 2** (ahí el null **iguala** al real; aquí el null da 110 y el real 15). El real cae fuera del rango completo del ensemble, así que **la dirección es válida y el tamaño de efecto NO es estimable**. Se reporta como **censurado por techo**, y se usa P2 para cuantificar. Lo mismo con los 105: R2 del null es 105,0 con sd 0.

---

## 7. 🔴 Lo que este null NO controla, y es la limitación que decide si se publica

**Un null de grado destruye la anatomía entera.** Baraja destinos por todo el cerebro sin respetar neuropilos ni distancia. Entonces **por construcción va a predecir conexiones entre poblaciones que físicamente no se tocan**, y contra eso cualquier restricción espacial se ve como un efecto enorme.

**Y esa es exactamente la explicación rival que quedó viva ayer (resp 057):** las ORN proyectan solo al lóbulo antenal y los fotorreceptores solo a lámina y médula, y **17.503 de los 21.019 socios de visual a 1 salto son del propio lóbulo óptico**.

**El null correcto para matar esa rival es de la familia espacial, y Lin et al. (2024) ya tiene los dos:** el **NPC** (probabilidades medidas entre 78 neuropilos) y el **NND** (probabilidad según distancia física entre árboles). Contra el NPC, **la reciprocidad de Lin baja de ×43,8 (CFG) a ×7,22**, o sea que ese null se come **el 84% del efecto** de un null de grado. **No hay razones para suponer que acá sea distinto.**

**Estado correcto, entonces, y es el mismo que el erratum ya usa para la jerarquía de ruteo:**

> **Establecido contra grado. NO testeado contra anatomía.** Y **no es testeable con los datos locales**: `annotations.tsv` tiene 31 columnas y **ninguna es neuropilo**. Hace falta bajar la asignación de sinapsis a neuropilos, o las posiciones para un NND.

**Lo que SÍ aguanta la explicación anatómica, y por eso el turno no fue en vano:** la comparación **entre clases**. Mechanosensorial y gustativa también tienen árboles localizados y también entran por nervios de la cabeza, y sin embargo dan **+7,37× y +6,54×** donde visual y olfatoria dan **0,02× y 0,06×**. **La localidad no explica una diferencia de 323× entre cuatro poblaciones que son todas locales.** Eso es el argumento que hay que escribir, y no necesita el NPC.

---

## 8. Archivos generados

- `docs/agents/respuestas/2026-08-24-061-null-de-grado-sobre-los-2-saltos.md` (este)
- `docs/agents/CONTEXTO-drosophila-fep.md` (diff: §3, §5 ítems 11-12, §6)
- Logs en el container, **no commiteados** (son reproducibles desde el comando): `/tmp/null2h.log`, `/tmp/guard.log`. **Toda su salida está verbatim en la §6 de este archivo.**

Instrumento: Python 3.12.14 con pandas/numpy/pyarrow sobre `connectivity.parquet` (md5 `3d802fd542b5d18570ba1ba0bb0abed9`, 15.091.983 filas) y `annotations.tsv` (md5 `719904abad876c68ace1b5690c9b9b63`). **Recomputable: si `super_class=='motor'` no da 110, o si P2 real de visual no da 1.413, el turno entero se cae.**

---

## 9. NO MEDIDO, declarado

1. **🔴 No hay null anatómico.** Es la §7 y es la limitación principal. No testeable con los datos locales: falta la columna de neuropilo.
2. **El control aleatorio no está pareado en grado:** 1.187.513 aristas contra 57.764–98.782 de las clases. **El piso de 0,652× es un orden de magnitud, no una corrección calibrada.** Un control pareado por grado de salida está sin correr.
3. **P2 cuenta caminos con multiplicidad de aristas, e incluye intermediarios de cualquier tipo**, también motoras y miembros de la propia clase. No excluye caminos que pasan por otra motora.
4. **El null genera self-loops (317) y aristas múltiples.** Es la familia configuración, no un Maslov-Sneppen con rechazo. **No verifiqué cuánto sesga P2 hacia arriba**, aunque el sesgo va **en contra** de los enriquecidos y **a favor** de los depletados, o sea que el lado depletado está ligeramente sobreestimado.
5. **P2 ignora signo y peso sináptico.** Cuenta caminos, no señal. Un camino inhibitorio pesa igual que uno excitatorio.
6. **Sin umbral de sinapsis.** Los tres papers de referencia usan ≥5. Este barrido usa el grafo completo, así que **no es comparable con nada de Lin ni de Bates** hasta re-correrlo.
7. **9 de las 110 motoras tienen `status = outlier_seg`.** No medí si excluirlas cambia algo.
8. **No corrí 3 saltos.** No sé a qué profundidad visual alcanza las motoras que le faltan, ni si alguna vez lo hace.
9. **El `grado_check_in` de la corrida grande era un test que no podía fallar** (§5). El guard válido corrió aparte. **Queda declarado como error del turno, no como detalle.**
10. **Nada de esto está en el paper, ni en el erratum, ni en el README.** El erratum ya está cerrado para el 30-ago y **este resultado no es una corrección de v1.0: es material nuevo para la v2 del paper.**
