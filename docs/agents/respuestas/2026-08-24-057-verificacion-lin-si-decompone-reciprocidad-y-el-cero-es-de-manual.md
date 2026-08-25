# 057 · Verificación: Lin SÍ descompone reciprocidad, y mi "descubrimiento" del cero era anatomía de manual

**Fecha:** 2026-08-24 23:10 (America/Buenos_Aires)

> **📄 Doc de ClickUp:** «VERIFICADO · Lin sí descompone reciprocidad, BANC no, y mi cero era medio de manual»

## 1. Pedido

«Verificá si Lin o BANC reportan reciprocidad por circuito en sus suplementarios. Y si el cero visual/olfatorio→motoras de cabeza ya lo publicó alguien.»

## 2. Herramientas declaradas (C-03)

| Llamada | Escribe | Cuota ajena |
|---|---|---|
| `search_web` × 5 | no | no |
| `fetch_website` × 4 (Nature Lin, PMC Lin, bioRxiv Lin, Nat Comms grooming) | no | no |
| `gateway build.run` × 6 sobre `brain-env` | `/tmp` únicamente | **NO** |
| `githubmcp_create_or_update_file` | sí, `main` | no |

**Cero Kaggle. Nada a Zenodo. `/workspace` solo leído, nada creado ni borrado ahí.**

---

## 3. VEREDICTO 1 · Lin SÍ descompone la reciprocidad. El claim se cae y hay que angostarlo

**Sí. Y no está escondido en un suplementario: está en la Fig. 5 del cuerpo principal.**

Verbatim de Lin et al. (2024), Nature 634:153–165:

> *«Computing the reciprocity in each neuropil (Fig. 5c and Extended Data Fig. 6c), we found regions with **high reciprocity probabilities**, including the central complex (FB, EB and noduli (NO)) and the ALs.»*

Y los pies de figura, verbatim:

| Dónde | Qué es |
|---|---|
| **Fig. 5c** | *«Reciprocity within each neuropil subnetwork»* |
| **Extended Data Fig. 6c** | *«**Reciprocity normalized by connection density** for all 78 neuropils»* |
| **Extended Data Fig. 6d** | *«Average reciprocal connection strength normalized by average unidirectional connection strength in all neuropils»* |
| **Fig. 5h** | *«Map of the total number of reciprocal pairs **between** different neuropils»* |
| **Fig. 5g / ED Fig. 7d** | **NSRNs**: neuronas altamente recíprocas específicas de neuropilo, **1.863** en el texto (704 en la Table 1) |

**El ítem que más duele es Extended Data Fig. 6c.** Es reciprocidad **normalizada por densidad**, por región. O sea: **la versión por región del 36× del abstract, ya publicada en Nature en 2024.**

### Lo que igual sobrevive, y es menos de lo que dije

Medido, no razonado: **cero coocurrencias** de `reciproc` con `super class`, `cell class`, `cell categor`, `sensory neuron`, `motor neuron` o `descending` en las 131.712 caracteres del cuerpo de Lin.

**La partición de Lin es ANATÓMICA** (78 neuropilos, o sea dónde caen las sinapsis). **La de la Table 7 es FUNCIONAL Y DIRIGIDA** (sensorial→motor, sensorial→descendente, intra-motor, óptico→motor). Son particiones distintas y la segunda no está en Lin.

### 🔴 Consecuencia inmediata, y es sobre el entregable del 30-ago

La frase que hay que **borrar de los dos lados**, porque es falsa:

> ~~*«which the published network analyses report only as a single global figure»*~~

Está en **`docs/ERRATUM.md` ítem 3** (el que va a Zenodo) y en **`docs/PIVOTE-RECIPROCIDAD.md` parte B**. Un erratum que le atribuye a Nature un defecto que Nature no tiene es exactamente el error del ítem 4 del propio erratum, cometido de nuevo.

**El claim correcto es:** *«Lin et al. (2024) report reciprocity resolved by anatomical neuropil (Fig. 5c) and normalized by connection density per neuropil (Extended Data Fig. 6c). The decomposition reported here is orthogonal to theirs: it is defined over directed pairs of functional cell classes rather than over anatomical subnetworks.»*

---

## 4. VEREDICTO 2 · BANC NO reporta reciprocidad como estadístico

Medido sobre el cuerpo de BANC en PMC (230.596 caracteres) y sobre las 10 páginas del suplementario (28.003 caracteres, md5 del PDF descargado de springernature):

```
BANC-main   bytes=230596  reciproc=2   clustering coefficient=0  rich club=0  motif=4   influence=132  ZZQQXX=0
BANC-supp   bytes=28003   reciproc=0   clustering coefficient=0  rich club=0  motif=0   influence=10   ZZQQXX=0
LIN-main    bytes=131712  reciproc=125 clustering coefficient=16 rich club=26 motif=90  influence=0    ZZQQXX=0
```

**Control negativo `ZZQQXX` = 0 en los tres. Control positivo: `influence`=132 en BANC y `reciproc`=125 en Lin.** El guard puede dar rojo, así que el cero de BANC es un cero medido y no un falso cero de coma de miles (modo de falla 6).

### Las 2 menciones de BANC, verbatim, y una importa

> *«these motor neurons form a tight **reciprocal feedback loop** with local sensory neurons (Fig. 2f)»* — prosa, sobre faringe.
>
> *«The CNS networks with a high influence on effectors are directly linked in a **nearly all-to-all pattern of reciprocal connectivity** (Fig. 6c,d, Extended Data Fig. 5f)»*

**La segunda es reciprocidad ENTRE MÓDULOS**, cualitativa, sin ratio y sin null. **No es prior art del desglose, pero es adyacente y hay que citarla** o un revisor la usa para decir que la idea ya estaba.

---

## 5. VEREDICTO 3 · El cero no lo publicó nadie, PERO mi framing estaba mal

### Nadie publicó ese cero como resultado

Barrí y no aparece. Lo más cercano:

- **Miroschnikow et al. 2018** (eLife, citado por BANC): sensorial→motor **monosináptico SÍ existe** en el conectoma de alimentación de la **larva**. Es el único `monosynap` en todo BANC, y está en la bibliografía.
- **Hampel 2015, Eichler 2024, Calle-Schuler 2026, Nat Commun abr-2026**: los circuitos de grooming de la cabeza son **multicapa** (sensorial → interneuronas → premotoras/DNs). El campo ya trabaja asumiendo que es indirecto, pero **como supuesto, no como cero medido**.

### 🔴 Pero el cero es anatomía establecida desde hace 25 años, y eso me tumba el framing

Las **ORN proyectan exclusivamente a 50 glomérulos clase-específicos del lóbulo antenal**; los fotorreceptores, a lámina y médula. Eso es literatura de 2000-2004, no un hallazgo.

Y se ve en los datos. Medido hoy, destinos a 1 salto:

```
olfactory   N=2279  socios=3184   -> sensory 2157, central 1017, descending 9, ascending 1, motor 0
visual      N=10855 socios=21019  -> optic 17503, sensory 2906, visual_projection 552,
                                     visual_centrifugal 53, descending 4, motor 0
```

**La salida de olfatorio y visual casi no sale de su propio territorio.** Entonces el cero **SÍ tiene explicación de localidad**: no a escala de «parte del cuerpo» como dijo BANC, sino a escala de **neuropilo**. 

**Mi resp 053b dijo «esto refuta la explicación de localidad de BANC». Eso se degrada:** refuta la localidad a granularidad de parte del cuerpo, y **confirma** la localidad a granularidad de neuropilo. Que es justamente la familia del NPC model de Lin. **E-01 otra vez: verifiqué el sujeto pero no la ESCALA a la que la explicación rival era cierta.**

Y hay un dato que le da la razón a BANC donde sí hay solapamiento: **gustatory llega a 10 motoras de cabeza a 1 salto**, consistente con el bucle recíproco de faringe que BANC describe. Las que tienen el arbor en el mismo lugar, conectan.

### 🟢 El rescate, medido hoy: a 2 SALTOS la asimetría sobrevive, y ahí sí no es anatomía

```
clase             alcance_2saltos   motoras_de_cabeza_alcanzadas (de 110)
visual                    95.160                 15
mechanosensory            68.471                110
gustatory                 26.535                107
olfactory                 22.940                 23
```

**Visual alcanza 95.160 nodos, más que cualquier otra clase, y llega a 15 de 110 motoras de cabeza. Mechanosensory alcanza 68.471, menos, y llega a las 110.**

A 2 saltos el arbor ya no es excusa: las cuatro clases salieron de su territorio, decenas de miles de nodos cada una. **La diferencia de acceso persiste cuando la restricción anatómica trivial ya no aplica.** Eso es la versión publicable del resultado, y es más fuerte que el cero: no es «no llegan», es **«llegan a todas partes menos ahí»**.

---

## 6. Evidencia cruda verbatim

```
motoras_cerebro= 110   descendentes= 1299
nervios: {'PhN': 40, 'MxLbN': 26, 'CV': 20, 'AN': 14, 'ON': 10}

olfactory | N= 2279 | socios_1salto= 3184 | a_motorasCabeza_1salto= 0
  | top_destinos= [('sensory',2157),('central',1017),('descending',9),('ascending',1)]
  || alcance_2saltos= 22940 | motorasCabeza_2saltos= 23 de 110
visual | N= 10855 | socios_1salto= 21019 | a_motorasCabeza_1salto= 0
  | top_destinos= [('optic',17503),('sensory',2906),('visual_projection',552),
                   ('visual_centrifugal',53),('descending',4),('NA',1)]
  || alcance_2saltos= 95160 | motorasCabeza_2saltos= 15 de 110
mechanosensory | N= 2656 | socios_1salto= 5601 | a_motorasCabeza_1salto= 64
  | top_destinos= [('central',2501),('sensory',2195),('descending',484),
                   ('ascending',310),('motor',64),('visual_centrifugal',30)]
  || alcance_2saltos= 68471 | motorasCabeza_2saltos= 110 de 110
gustatory | N= 408 | socios_1salto= 1793 | a_motorasCabeza_1salto= 10
  | top_destinos= [('central',1132),('sensory',359),('ascending',112),
                   ('descending',96),('sensory_ascending',80),('motor',10)]
  || alcance_2saltos= 26535 | motorasCabeza_2saltos= 107 de 110
```

Instrumento: `annotations.tsv` (31.718.505 B) y `connectivity.parquet` (100.804.642 B, 15.091.983 filas), Python 3.12.14 con pandas. Población motora = `super_class == 'motor'` intersectada con el grafo. Recomputable: **si `super_class=='motor'` no diera 110, o si visual a 2 saltos no diera 15, el veredicto 3 se cae.**

---

## 7. 🔴 Una discrepancia con mi propia resp 053b, sin resolver

| Cantidad | resp 053b | hoy |
|---|---|---|
| motoras de cabeza | **105** | **110** |
| nervio CV | 19 | 20 |
| nervio ON | **6** | **10** |
| PhN / MxLbN / AN | 40 / 26 / 14 | 40 / 26 / 14 |

La 053b usó un filtro que llamé `brain_motor_neuron` y hoy usé `super_class == 'motor'`. **Los dos no son el mismo conjunto y no establecí cuál corresponde a la población del paper.** Los conteos de 1 salto (0, 0) no cambian, así que el cero se sostiene con las dos definiciones, pero **el denominador de «de 110» está sin fijar** y eso hay que cerrarlo antes de publicar cualquier fracción.

---

## 8. NO MEDIDO, declarado

1. **No leí la Fig. 5c ni la ED Fig. 6c fila por fila.** Sé que existen y qué miden por el pie de figura y por el texto, **no tengo sus valores**. Si algún neuropilo de Lin coincide con un circuito de la Table 7, el solapamiento es peor de lo que digo.
2. **No verifiqué si Lin publica la tabla numérica** de reciprocidad por neuropilo en un Supplementary Data descargable. Si la publica, se puede cruzar directo.
3. **El test de solapamiento de neuropilo NO se pudo correr:** el `annotations.tsv` local **no tiene columna de neuropilo**. La explicación anatómica del cero está **apoyada por literatura y por la distribución de destinos a 1 salto, no medida sobre neuropilos**.
4. **Los conteos de 2 saltos no tienen null.** Que visual llegue a 15 de 110 y mechano a 110 de 110 es un contraste crudo; **sin null preservando grado no es un resultado, es una observación**.
5. **El alcance a 2 saltos ignora signo y peso.** Cuenta existencia de camino, no influencia.
6. **No barrí la literatura del cero exhaustivamente.** Cinco búsquedas, no una revisión sistemática. Que nadie lo haya publicado está **apoyado, no establecido**.
7. **La discrepancia 105 vs 110 de la §7 está sin resolver.**
8. **Ni el `ERRATUM.md`, ni el `PIVOTE-RECIPROCIDAD.md`, ni los contextos están corregidos todavía en este archivo.** Son los commits que siguen.
