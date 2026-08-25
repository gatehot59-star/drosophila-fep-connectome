# 052 · La cronología se da vuelta, el pivote de reciprocidad, y por qué no citar es peor

**Fecha:** 2026-08-24 21:25 (America/Buenos_Aires) · **Modo:** TITAN FULL

> **📄 Doc de ClickUp:** *«La fecha se da VUELTA y hay que decirlo…»*

---

## 1. Pedido

Tres cosas: **«¿yo trabajé en marzo, ellos publican en junio o no?»**, **«lo de reciprocidad no está muerto, simplemente tomar sus datos y pivotar»**, y **«nombrarlos a esta fecha ¿no es contraproducente? Da a entender que yo me valgo de ellos para resolver lo mío»**.

---

## 2. Herramientas declaradas (C-03)

| Llamada | Escribe | Cuota ajena |
|---|---|---|
| `search_web` × 1 (cronología del preprint y del artículo) | no | no |
| Las cuatro lecturas web de la resp 050 | no | no |
| `create_document` + `create_or_update_file` | sí | no |

**Cero container, cero cuota de Kaggle, `gradlew` no ejecutado, nada publicado en Zenodo. Ningún contexto ni el erratum tocados en este turno**, a propósito: las dos correcciones que salen de acá tocan un texto destinado a un DOI y quedan pendientes de OK.

---

## 3. 🔴 La cronología: **Nature es ANTERIOR, no posterior**

| Hito de Lin et al. | Fecha | Fuente verificada |
|---|---|---|
| Charla en **APS March Meeting** | **6-7 marzo 2023** | `meetings.aps.org`, sesión A11.00010 |
| **Preprint en bioRxiv** | **29 julio 2023** | `biorxiv.org/…/2023.07.29.551086v1` · PMC10402125 · PubMed 37547019 |
| **Publicado en Nature** | **2 octubre 2024** | Nature **634(8032):153–165**, en `nature.com`, Springer, Janelia y Cambridge |
| **Paper 1 en Zenodo** | **20 marzo 2026** | el PDF |

**17 meses y medio antes** del depósito. El preprint, **32 meses antes**. La charla pública, **tres años antes**.

### El dato que cierra la pregunta de si se podía saber

**El Paper 1 cita a Dorkenwald et al. 2024 en su §1.1.** Los dos papers son **compañeros del mismo número de la misma revista** — 124-138 y 153-165, publicados **el mismo día** — y **Dorkenwald es coautor de los dos**.

**Consecuencia:** no citar el de análisis de red **no es «no lo podía saber»**: es una omisión de búsqueda bibliográfica. Y **no hay disputa de prioridad**: es prior art de casi tres años sobre el mismo dataset.

---

## 4. ✅ Reciprocidad: **Abraham tiene razón, y el pivote es más fuerte que el que escribí ayer**

La resp 050 dejaba el desglose por circuito **como consuelo**. Es mucho más: **los propios resultados de Lin sostienen el mecanismo.**

### 4.1 El pivote en su forma fuerte, usando a Lin como PREMISA

> Lin et al. establecen que la reciprocidad global es **comparable entre cinco sistemas nerviosos**. **Si el número global es genérico entre especies, el número global no es la pregunta interesante: la pregunta es dónde se concentra.** Y eso es exactamente lo que el Paper 1 mide.

**Su hallazgo no refuta al Paper 1: lo habilita.** Convierte la Table 7 en la continuación obvia de su trabajo, y ellos no la hicieron.

### 4.2 La Table 7, que Lin no tiene

```
Intra-motor                41,3%      Sensorial → central        24,2%
Intra-visual centrífugo    36,9%      Sensorial → descendente     8,7%
Intra-óptico               32,0%      Sensorial → motor           3,6%
Intra-sensorial            30,7%      Óptico → motor              0,0%
```

**Rango de 41 puntos y un cero exacto.** Lin reporta **un** número (0,138). **Ese promedio esconde esta distribución.**

### 4.3 🔥 Lo que no vi ayer: **Lin mide DOS cosas que la reverberación necesita**

Verbatim de Lin et al., y **ninguna de las dos está usada en el Paper 1**:

**Primera:** *«The average strength of edges participating in reciprocal connections is **higher** than the average strength of unidirectional connections.»*

**Las recíprocas son más FUERTES.** Reverberación sobre conexiones débiles se apaga; sobre fuertes se sostiene. **Es un dato de Nature que sostiene el mecanismo propio.**

**Segunda:** *«The most common reciprocal pairing is **ach–GABA**… Both of these reciprocal motifs are **excitatory–inhibitory**… By contrast, excitatory–excitatory **ach–ach pairs are under-represented**»*.

**La reciprocidad del cerebro es predominantemente E-I, no E-E.** Y el Paper 1 mide **cancelación GABAérgica por profundidad** (Tabla 6: mechano 0,04% → 135% → 953%; olfatorio 0,00% → 8,7% → 10,7%). **Son el mismo mecanismo desde dos ángulos**, y ninguno de los dos papers lo escribió.

**Tercera, de escala:** *«77,607 of 127,978 neurons participate in at least one reciprocal connection: approximately **2 in every 3**»*.

### 4.4 Lo que SÍ hay que sacar

El **«36×»** y la palabra **«massive»** del abstract. No porque el número esté mal (era el overflow), sino porque **comparar contra azar existiendo una comparación contra otros cerebros es elegir el rival débil**.

---

## 5. ¿Citarlos es contraproducente? **No, y la fecha lo invierte**

### 5.1 Lo que pasa si NO se los cita

Con Nature **17 meses antes** sobre **el mismo dataset**, y con el paper **ya citando al compañero**, un revisor tiene dos lecturas y **ninguna sirve**:

1. **No conoce la literatura de su propio dataset.** Es lo primero que se chequea.
2. **La conoce y la omitió.** Peor.

**No citar prior art no vuelve independiente a nadie: vuelve no leído.** Y en connectomíca el revisor conoce los tres papers compañeros de memoria.

### 5.2 Lo que pasa cuando SÍ se los cita

**Citar no es subordinarse: es ubicarse.** La forma que corresponde:

> *«Lin et al. (2024) caracterizaron la estadística estática de este conectoma y cerraron pidiendo modelos que exploren la relación entre actividad y estructura. Este trabajo hace eso.»*

**Eso no dice «me valí de ellos»: dice «contesto la pregunta que dejaron abierta»**, y es literalmente la última frase de su abstract. **Cuando dos trabajos están en secuencia, el segundo no es el subordinado: es el que avanza.**

### 5.3 Lo que SÍ sería valerse de ellos, y no está pasando

Valerse sería **usar su resultado como resultado propio**. No es el caso: se usa **su dataset**, que es público y está hecho para eso, y se mide **algo que ellos no midieron**.

**Lo único que se le parece es el null CP**, que resulta la misma familia que su NPC. **Y ahí la salida honesta es la que conviene:** «un null que preserva grado y estructura de bloques, en la familia del NPC de Lin et al., con super-clases funcionales en vez de neuropilos anatómicos». **Eso queda mejor que presentarlo como propio y que un revisor lo encuentre.**

### 5.4 Y el argumento que más conviene

**Un preprint en Zenodo sin citas al estado del arte es invisible; uno que dialoga con Nature entra en la conversación**, y se vuelve **buscable desde el suyo**. **No citarlos no protege: esconde.**

---

## 6. ⚠️ Y una corrección a mí mismo que la fecha obliga

La resp 050 llamó **«convergencia independiente»** a la coincidencia attractor/repeller. **Con Lin publicado 17 meses antes, el término hay que precisarlo:**

| Afirmable | **NO** afirmable |
|---|---|
| **los MÉTODOS son independientes**: random walk espectral contra conteo de aristas contra nulls | «descubrimiento independiente» o «llegamos a la vez» |
| la convergencia de dos métodos distintos **es evidencia**, sin importar el orden | que el resultado ajeno no se podía conocer |
| *«consistente con la estructura reportada por Lin et al. (2024)»* | *«coincidimos independientemente»* |

**Sigue siendo fuerte.** Lo que no está disponible es el crédito de simultaneidad, y **reclamarlo con la fecha en contra le regala al revisor el argumento para desconfiar del resto.**

---

## 7. Evidencia cruda verbatim

```
biorxiv.org/content/10.1101/2023.07.29.551086v1
  "Network Statistics of the Whole-Brain Connectome of Drosophila"
  published 2023-07-29 · Albert Lin, Runzhe Yang, Sven Dorkenwald,
  Arie Matsliah, Amy R. Sterling, Philipp Schlegel, Szi-chieh Yu,
  Claire E. McKellar, [...]
  PMC10402125 · PubMed 37547019

janelia.org/publication/network-statistics-of-the-whole-brain-connectome-of-drosophila
  "Nature. 2024 Oct 02;634(8032):153-165. doi: 10.1038/s41586-024-07968-y"
  Lin Albert, Yang Runzhe, Dorkenwald Sven, Matsliah Arie, Sterling Amy,
  Schlegel Philipp, Yu Szi-chieh, McKellar Claire, Costa Marta,
  Eichler Katharina, Bates Alexander, Eckstein Nils, Funke Jan,
  Jefferis Gregory, Murthy Mala

link.springer.com/article/10.1038/s41586-024-07968-y
  "Published: 02 October 2024 · Volume 634, pages 153-165 (2024)"

meetings.aps.org/Meeting/MAR23/Session/A11.10
  2023 APS March Meeting, March 6, Abstract A11.00010:
  "Network Properties the whole-brain Drosophila connectome"

meetings-archive.aps.org/mar/2024/pp02/1/
  March 7, 2024: "Publication: Neuronal wiring diagram of an adult brain
  (preprint, under review); Network Properties the whole-brain Drosophila
  connectome (preprint, under review)"

nature.com/articles/s41586-024-07968-y, leido verbatim:
  "The average strength of edges participating in reciprocal connections is
   higher than the average strength of unidirectional connections."
  "The most common reciprocal pairing is ach-GABA, and the second most common
   pairing is ach-glutamate. Both of these reciprocal motifs are
   excitatory-inhibitory [...] By contrast, excitatory-excitatory ach-ach
   pairs are under-represented, as are inhibitory-inhibitory GABA-GABA pairs."
  "Of the 127,978 neurons in the brain, 77,607 participate in at least one
   reciprocal connection: approximately 2 in every 3 neurons"
  "Despite differences in the sparsity of the different brain networks, the
   values of reciprocity and clustering coefficient are comparable across all
   five datasets."
```

**Recomputable y contradecible (W-01): si el DOI `10.1038/s41586-024-07968-y` no resolviera a un artículo de octubre de 2024, todo el §3 se cae.** Cuatro fuentes independientes lo confirman.

---

## 8. Archivos generados

| Archivo | Estado |
|---|---|
| El Doc de ClickUp | **nuevo** |
| `docs/agents/respuestas/2026-08-24-052-…md` | este archivo |

**Ningún contexto ni el erratum tocados**, a propósito. Las dos correcciones que salen de acá (la ubicación temporal de Lin, y reescribir «convergencia independiente») **tocan texto destinado a un DOI y esperan OK**.

---

## 9. NO MEDIDO, declarado

1. **La charla de APS 2023 tiene un título parecido y NO idéntico** al del paper (*«Network Properties»* contra *«Network Statistics»*). **No verifiqué que sea el mismo trabajo**, aunque el listado de APS 2024 lo menciona junto a los dos preprints.
2. **No leí el preprint de bioRxiv**, solo confirmé su fecha e identificadores.
3. **De Lin leí hasta la sección de reciprocidad**, no su Discussion ni sus Methods. **Las cuatro citas del §7 sí son verbatim.**
4. **No crucé entrada por entrada la bibliografía del Paper 1.** Que no cita a Lin sale de leer sus 7 páginas incluida la lista de referencias.
5. **La lista de 15 autores de Lin sale del listado de Janelia**, no del artículo.
6. **No cuantifiqué el solapamiento** attractor/repeller contra el ruteo medido. Sigue cualitativo.
7. **No verifiqué si Lin reporta reciprocidad por tipo de circuito** en su suplementario. **Si lo hiciera, se cae el pivote de §4.2.**

---

## 10. La regla que sale

**Antes de razonar sobre estrategia de publicación, medir la cronología.** La pregunta era «¿ellos publican después?», y la respuesta invierte dos de las tres conclusiones: con Nature **posterior**, no citarlos sería discutible; con Nature **17 meses anterior sobre el mismo dataset**, es indefendible. **Una decisión editorial que depende de una fecha se toma después de verificar la fecha, no antes.**

**Y el corolario, que es el que importa:** el reflejo de no citar para no parecer derivado **produce exactamente el efecto que quiere evitar**. Citar prior art es lo que distingue a un par de un aficionado, y es gratis.

```
--- METODO TITAN ---
Accion delicada: NO en este turno. Un search_web y dos escrituras de
                 documentacion. Ningun contexto ni el erratum tocados: las dos
                 correcciones que salen de aca esperan OK porque tocan texto
                 destinado a un DOI. Cero cuota, gradlew no ejecutado, nada
                 publicado en Zenodo.
Modo aplicado:   TITAN FULL
Rubrica:         45/45 -> 100/100. Aplicables: Completitud, Arquitectura del
                 razonamiento, Documentacion, Innovacion, Proceso QA.
                 N/A: 45 pts (Ejecutabilidad, Seguridad, Testing, DevOps).
N/A declarados:  45 pts
Review externo:  el falsador fue la CRONOLOGIA. Abraham pregunto si Nature
                 publico en junio; publico 17 meses y medio ANTES de su
                 deposito, con preprint 32 meses antes y charla publica tres
                 anos antes. Eso invierte dos de sus tres preguntas y obliga a
                 corregir un termino que yo mismo use en la resp 050.
Instrumento:     V-01. Verificado en vivo el 2026-08-24 en seis URLs, listadas
                 con su cita verbatim en la seccion 7: biorxiv (preprint
                 29-jul-2023), janelia y springer (Nature 2 oct 2024,
                 634(8032):153-165), aps 2023 y 2024, y nature.com para las
                 cuatro citas del pivote.
                 NO MEDIDO: la seccion 9, siete items.
```
