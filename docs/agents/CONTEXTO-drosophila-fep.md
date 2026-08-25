# CONTEXTO VIVO · conectoma / FEP / papers

**Última actualización:** 2026-08-25 08:45 (America/Buenos_Aires) · **Se sobreescribe, no se acumula.**

Leer esto **antes** de responder cualquier cosa de este proyecto. Protocolo: `00-PROTOCOLO-BITACORA-DE-RESPUESTAS.md`. Hermano: `CONTEXTO-motor.md` (**⚠️ VENCIDO: no se abrió el 25-ago, no recibe veredicto de vigencia**). Índice de Docs: `INDICE-REAL-POR-ENUMERACION.md` (**parcial, 46 de ~65**). Entorno: `CONTEXTO-ENTORNO.md` §13 (**se re-mide, no se recuerda**). Kaggle: `MANIFIESTO-KAGGLE.md` (**40 kernels, no 29**).

**Rama de trabajo: `titan/twohop-nulls`.** Respuestas al día: **074** (no existe una 072). Este archivo cubre hasta la **resp 075**.

---

## 0. 🚨 EL RELOJ · el erratum vence el 30-ago y el texto ya está escrito

**Fuente: doc `6117`, «PLAN MAESTRO 10 SEMANAS · 24-ago al 8-nov 2026».** Hoy es el **25-ago**: día 2 de la **S1**.

| # | El número que decide el éxito | Umbral | Estado |
|---|---|---|---|
| 1 | **Erratum en Zenodo** | **antes del 30-ago (5 días)** | ✅ **texto listo en `docs/ERRATUM.md`**, 9 ítems, claim falso retirado, Bates citado. **Falta la acción de Abraham** |
| 2 | Motivos con 0/40 en la biblioteca | ≥ 3 (hoy hay **1**) | sin avance |
| 3 | Nulls del motor complejo | **40** (piso de `p` 0,20 → 0,0488) | hoy 9 |
| 4 | Papers subidos | ≥ 2 antes del 8-nov | 0 |

**El erratum NO está en riesgo por la auditoría externa:** ninguno de los 13 hallazgos toca sus nueve ítems, y Tao lo confirma explícitamente.

**🔴 Y hay un conflicto de cronograma abierto, que es decisión de Abraham:** la reparación de infraestructura que dictaminó la auditoría son **días**, y **no estaba en ninguno de los cinco entregables del plan**. O se corre el plan, o se mata un entregable.

**Deadlines externos — ✅ VERIFICADOS EN VIVO el 24-ago contra `arcprize.org/competitions/2026`:**

```
- March 25, 2026 - Competition starts
- June 30, 2026 - ARC-AGI-3 Milestone #1
- September 30, 2026 - ARC-AGI-3 Milestone #2
- November 2, 2026 - Submissions due
- November 8, 2026 - Papers due
- December 4, 2026 - Results announced
```

Premios: **Paper Prize $450K** (Top Paper $75K garantizado: 1º $50K, 2º $20K, 3º $5K; pozo de **$375K** para papers > 4,5 en la rúbrica) · **ARC-AGI-3 $850K**. **Ganar ARC no es el objetivo.**

**🔑 Dato que el `6117` NO tenía y ahorra una semana:** son **TRES tracks**. Verbatim de `arcprize.org/competitions/2026/paper`: *«Paper submissions must be linked to a Kaggle code submission (**ARC-AGI-2 or ARC-AGI-3** track)… The code submission **need not achieve a high score**»*. **La S7 asume construir el agente interactivo de ARC-AGI-3 y puede no ser necesaria.** *Discrepancia menor: una página de Kaggle dice 9-nov; gana `arcprize.org`.*

**Las 10 semanas:** S1 cerrar lo público · S2 los nulls que faltan · S3 dos o tres motivos más · S4 mecanismo de aprendizaje · **S5 P1** · **S6 P2** · S7 agente ARC · S8 P4 · S9 revisión externa · S10 cerrar y subir.

**Los 5 papers:** **P1** auditoría de connectomíca dinámica · **P2** el 0,41% blindado · P3 biblioteca (**1 de 3-4 motivos**) · P4 ARC · P5 Paper 2 como negativo.

**El riesgo real no es técnico:** cinco entregables en diez semanas de **una persona**. El orden **es** la protección. **Y la auditoría propuso un orden mejor que el mío:** *«primero lo que vuelve confiable al testigo; después lo que amplía el claim»*.

---

## 1. Son TRES papers más un motor. No mezclarlos nunca más

| Nombre | Qué es | Estado |
|---|---|---|
| **PAPER 1** | *Signal Propagation Properties in the Drosophila melanogaster Connectome: Intermodal Isolation, Differential Motor Access, and Non-Trivial Temporal Amplification*, Mendieta 2026a. **7 páginas, leído completo el 24-ago** | Zenodo 20-mar-2026. **DOI placeholder `XXXXXXX` literal en el header** |
| **PAPER 2** | *Topological Retention and Selective Convergence* — FEP, Markov blanket, Script R | Borrador. Va como resultado **negativo** (P5) o no va |
| **PATENTE** provisional | Congelada antes del erratum. Doc `5717`: **la patente tiene razón, el FALSIFIED es un artefacto** | En pausa |
| **Motor** | SparseLTC / DualBrain, C99 + ESP32 | **El activo real.** Ver `CONTEXTO-motor.md`, **vencido** |

**El producto en tres capas:** (1) la **fuente de calibración** = el conectoma medido y sus priors · (2) el **motor** = de 15M aristas a **1.336 B de código medidos en ESP32** y 704 B de RAM todavía solo en x86 · (3) **la biblioteca = el activo**, hoy con **un** motivo. **No se vende como «derivado del cerebro de la mosca»: se venden microsegundos, miliwatts y BOM.**

---

## 2. Lo que dice el PDF publicado, leído verbatim (24-ago, 7 páginas)

- **§2.1:** `Density = 0.0074`. Y `E/I = 1.50`, 9.059.302 excitatorias (60,0%), 6.032.681 inhibitorias.
- **Abstract:** «E = 15,091,983 **synapses**» · «reciprocity (**36×** over density expectation)» · «**four** parameter-free neural models» · «7/10 sensory classes» · «τm ≈ 8.4 ms, **center** of the physiological range».
- **§2.1 dice «connections» para el mismo 15.091.983.** → la ambigüedad **existe** y es defecto de redacción, **pero NO es la causa del número**.
- **La tabla de RDI es la Table 8**, con columnas `Real | CP | Z_CP | MS | Z_MS`, **sin columna Ratio**. **La Table 7 es reciprocidad por circuito** (intra-motor 41,3% … optic→motor 0,0%). ⚠️ **El doc `6017` llamó «Tabla 7» a lo que es la Tabla 8.**
- **El 1.559× NO EXISTE en el PDF.** Y la **Table 1 es la tabla de poblaciones**, sin un solo ratio.
- **§2.4 ya declara y deriva el guard de tautología del CP.**
- **§2.5 y la Limitación 3 ya dicen TRES modelos compatibles.** El «four» queda **solo en el Abstract**.
- **§2.3:** *«10 canonical sensory classes with N >= 10»*, y la **Tabla 5 muestra 9 filas**. Falta una y **no está establecido cuál**.
- **§7 Data Availability:** URL `github.com/Mendieta-Architect/drosophila-connectome-**propagation**`, licencia **AGPL v3**.
- **Tabla 4 suma 90.101** donde 85.821 + 4.281 = **90.102**.
- **§1.1 cita a Dorkenwald et al. [2024]**. **§1.2 cita a Betzel et al. [2026]**. **Y NO cita a Lin et al.** ni a Bates et al., ver §2.bis.
- Nulls declarados: MS `N = 100` estático y `N = 5` temporal; CP `N = 10` estático y `N = 5` temporal. **Tasa de swap 100%**, no alcanzable: la medida es 98,5%.

---

## 2.bis 📚 LAS REFERENCIAS EXTERNAS, completas y verificadas

**Por qué esta sección existe:** hasta el 24-ago 21:00 este archivo decía **«Lin» a secas** en cinco lugares, sin autor completo, sin año, sin revista y sin páginas. **Una referencia incompleta se completa mal en el turno siguiente.**

| Referencia | Qué es | Páginas | De ahí sale |
|---|---|---|---|
| **Dorkenwald, S., Matsliah, A., et al. + FlyWire Consortium (2024).** *Neuronal wiring diagram of an adult brain.* Nature | **634:124–138** | el paper de **DATOS** | **12,6 sinapsis por conexión** · grado medio 20,5 |
| **Lin, A., Yang, R., et al. (2024).** *Network statistics of the whole-brain connectome of Drosophila.* Nature | **634:153–165** | el paper de **ANÁLISIS DE RED** | **densidad 0,000161** · **reciprocidad 0,138** · clustering 0,0463 · rich club · **y la reciprocidad POR NEUROPILO** |
| **Bates, A. S., Phelps, J. S., Kim, M., Yang, H. H., et al. (2026).** *Distributed control circuits across a brain-and-cord connectome.* Nature | doi:10.1038/s41586-026-10735-w | **cerebro + cordón**, publicado **8-jun-2026**, preprint **31-jul-2025**, **188.259 neuronas** | métrica de **influence** lineal, `R² = 0,94` en 94.278 pares |
| **Kind, E., et al. (2024)** + **Cell Type Explorer de `flywire-fafb:v783b`** | 🔴 **publican la tabla de ruteo del sistema visual** que yo iba a medir. Ver §4 | — | resp 066-067 |

**Verificado el 24-ago** contra `nature.com`, PMC (`PMC11446825`, `PMC11446842`, `PMC12324551`) y bioRxiv.

**Los parámetros de Lin:** snapshot **v630** (no v783), **umbral de 5 sinapsis por conexión**, 127.978 neuronas, 2.613.129 conexiones.

**Otros números de Lin:** rich club de **30%** con cutoff de grado 37 y probabilidad interna 0,000870 = **5,4×** la global · small-worldness **SΔ = 141** · SCC gigante 93,3% · WCC 98,8% · camino dirigido medio **4,42 saltos**, todos alcanzables en 13 · **77.607 de 127.978** neuronas participan de al menos una conexión recíproca · **1.863 NSRNs** · cuatro nulls: **ER, CFG (grado), NPC (neuropilos) y NND (distancia)**.

**Su Table 2, leída fila por fila:** reciprocidad 0,138 = **×858 vs ER, ×43,8 vs CFG, ×45,9 vs NND, ×7,22 vs NPC**. Clustering 0,0463 = ×144 / ×7,57 / ×10,9 / ×2,88.

> **🔑 La calibración de expectativas, y el 25-ago se quedó CORTA:** pasar de un null de **grado** (CFG, ×43,8) a uno **anatómico** (NPC, ×7,22) se come el **84%** del efecto en Lin. **En mis propios 2 saltos se comió el 100% y encima dio vuelta tres signos.** Cualquier resultado propio medido solo contra grado está **NO TESTEADO**, no «establecido».

### 🔴 Lo que Lin le hace al framing del Paper 1

**Lin compara contra CINCO conectomas** y concluye, verbatim: *«the values of reciprocity and clustering coefficient **are comparable across all five datasets**»*. Y: *«the over-representation of reciprocal connections in brains is **well established**»*, con seis citas, dos en Drosophila.

**Consecuencia:** alta contra controles randomizados, **normal contra otros sistemas nerviosos medidos**. **El 36× no se arregla corrigiendo el número: hay que bajar el claim.**

### 🔴🔴 Y LIN TAMBIÉN DESCOMPONE LA RECIPROCIDAD · verificado el 24-ago (resp 057)

Verbatim de Lin:

> *«Computing the reciprocity in each neuropil (Fig. 5c and Extended Data Fig. 6c), we found regions with **high reciprocity probabilities**, including the central complex (FB, EB and noduli (NO)) and the ALs.»*

| Dónde | Qué es |
|---|---|
| **Fig. 5c** | *«Reciprocity within each neuropil subnetwork»* |
| **Extended Data Fig. 6c** | *«Reciprocity **normalized by connection density** for all 78 neuropils»* ← **la versión por región del 36×** |
| **Extended Data Fig. 6d** | reciprocal strength normalizada por unidirectional strength, en los 78 |
| **Fig. 5h** | mapa de pares recíprocos **entre** neuropilos |
| **Fig. 5g / ED Fig. 7d** | **NSRNs**, 1.863, predominantemente inhibitorias (54% GABA) |

**Está en el CUERPO del paper, no en un suplementario.**

**Lo que SÍ sobrevive, y es un claim más chico pero verdadero:** medido, **cero coocurrencias** de `reciproc` con `super class`, `cell class`, `cell categor`, `sensory neuron`, `motor neuron` o `descending` en los 131.712 caracteres del cuerpo de Lin. **Su eje es ANATÓMICO (78 neuropilos). El de la Table 7 es FUNCIONAL Y DIRIGIDO.** Ejes ortogonales. **La novedad no es «descomponer»: es sobre qué eje.**

### 🟢 Y una CONVERGENCIA INDEPENDIENTE, que sigue siendo lo mejor y no está en el paper

Lin, por **random walk espectral**: **attractors** (3% de neuronas, 61,2% de las visitas) *«often make connections in the **gnathal ganglia**… contains many connections to the **ventral nerve cord**»* → la salida motora. **repellers** (3%, 42,4%) *«include many with synapses in the **antennal lobes (AL) and medullae (ME)**»* → periferia olfatoria y visual.

Y el Paper 1, **por conteo de aristas contra nulls que preservan grado**, mide que **olfactory y visual son las más depletadas** en acceso motor. **Dos métodos que no comparten nada llegando al mismo ruteo.** Va como *«consistente con la estructura de atractores y repulsores reportada independientemente por Lin et al. (2024)»*. **NO MEDIDO: la convergencia es cualitativa, el solapamiento no está cuantificado.** ⚠️ **Y ojo: el null anatómico del 25-ago sugiere que esa coincidencia puede ser co-localización en los dos métodos.**

### 🔴 El null CP tiene PRIOR ART: el NPC model de Lin

Verbatim: *«an extension of the CFG model in which we constrain the random network by **enforcing the measured connection probabilities between the 78 neuropils**»*. **Misma familia:** grado **y** matriz de bloques. Diferencia: granularidad (78 neuropilos anatómicos vs 10 super-clases funcionales). Lin tiene además el **NND** por distancia física. **Hay que citarlo y angostar el claim.** A favor: que Nature use esa familia **valida que era el control correcto**. **NO MEDIDO: no se implementaron lado a lado.**

### 🟡 BANC: NO reporta reciprocidad como estadístico, y eso es medido

```
BANC-main   bytes=230596  reciproc=2   clustering coefficient=0  rich club=0  influence=132  ZZQQXX=0
BANC-supp   bytes=28003   reciproc=0   clustering coefficient=0  rich club=0  influence=10   ZZQQXX=0
LIN-main    bytes=131712  reciproc=125 clustering coefficient=16  rich club=26  influence=0    ZZQQXX=0
```

**Control negativo `ZZQQXX` = 0 en los tres; positivo alto en los tres.** El guard puede dar rojo.

Sus 2 menciones son prosa. **Una importa y hay que citarla:** *«The CNS networks with a high influence on effectors are directly linked in a **nearly all-to-all pattern of reciprocal connectivity** (Fig. 6c,d)»*. Reciprocidad **entre módulos**, cualitativa, sin ratio y sin null.

### BANC valida el método y salva el aporte

Verbatim: *«a linear dynamical systems description of signal propagation… injecting a sustained signal into the source neurons… the weighted sum of its inputs… as a fraction of the total synaptic input of the postsynaptic cell»*, validado sobre **FAFB v783** con `R² = 0,94` en **94.278 pares**. **Es el modelo lineal del Paper 1 con normalización por columna: el campo eligió el mismo método.**

Y declara **dos renuncias**: *«we take its **steady-state response**»* y *«adjusted influence is an **unsigned quantity**»*. **Sin signo** no hay cancelación GABAérgica → Propiedad 1 invisible. **Sin transitorio** no hay post-estímulo → Propiedad 3 también. **El campo llegó al método y se detuvo donde empieza el aporte, y el 25-ago ese hueco pasó a ser el activo principal (ver §3).**

**Y dos frases más de BANC que conviene tener:** que las regiones cognitivas son *«supervisory but not essential for action»* (apoya el framing del 0,41% encerrado), y que los efectores *«are primarily influenced by sensory neurons in the **same body part**»* ← **esta explicación rival GANÓ a granularidad de neuropilo el 25-ago. Ver §3.bis.**

### El veredicto de relación: **SECUENCIALES**

Lin: estructura. Paper 1: primera película dinámica. BANC: institucionalización del baseline lineal a escala grande. **Y BANC no te tomó: su preprint es de jul-2025, tu preprint de mar-2026. Es convergencia metodológica.**

---

## 3. ⭐ EL ACTIVO PRINCIPAL, y cambió el 25-ago

> **La topología de este circuito define selectividad temporal en el TRANSITORIO POST-ESTÍMULO, no en la amplitud de pico.**

**Doble instrumento, misma corrida, y el contraste está pareado por construcción (resp 070-071, `src/signshuffle_selpost.py` md5 `5a292cbc4f0a6b2d445405ad5c86ad80`; null que respeta Dale en `src/signshuffle_dale.py` md5 `d6f43b30050d192c6f3ae32956d92858`):**

| Medición | Número |
|---|---|
| `sel_post` observado | **4,3287** |
| null de **topología** (permuta pesos, conserva signo) | 1,1896 ± 0,0173 → **z = +181,4**, **0/40** |
| null de **signo por arista** | 1,9101 ± 0,3242 → **z = +7,46**, 0/40 |
| null de **signo que PRESERVA DALE** (por neurona presináptica) | 1,7983 ± 0,401 → **z = +6,31**, 0/40 |
| `sel_peak` en la misma corrida | **DEBAJO** de su null (z = −2,41), en 6 de 7 configuraciones |
| actividad post-estímulo **absoluta** (`post_looming`) | **2,77 contra 16,09** del null → el circuito **resuena 5,8× MENOS y 3,6× más diferencial** |

**Se repite a spread de τ 8 y 30: 0/40 en 7 de 7 configuraciones.**

**Por qué vale, y es el argumento del paper:** es cualitativa y cuantitativamente **la Propiedad 3 del Paper 1** (RDI post-estímulo, `z = 197` medido en el conectoma, doc `5977`). **Dos instrumentos independientes, mismo fenómeno.** Y es exactamente el territorio que **BANC declara no cubrir** (steady-state y sin signo).

**Lo que este hallazgo mató, y era mío:** «la topología define ruteo y ganancia, **no** selectividad» (el 1,04× del escape compilado). **Medí `sel_peak` seis días, y el pico es lo único que este circuito NO discrimina.**

---

## 3.bis 🔴 EL NULL ANATÓMICO · la refutación más caras del expediente (resp 063)

**El dato existía a una llamada:** Zenodo `10676866`, v783.0, `per_neuron_neuropil_count_pre/post_783.feather`, **79 etiquetas de neuropilo**, solo 283 neuronas sin neuropilo de salida y 495 sin entrada sobre 138.639. **El ítem que decía «no es testeable» era un límite de UN archivo (`annotations.tsv`), no del entorno.**

**El ensemble:** permuta destinos **solo dentro de grupos de aristas que comparten el par (neuropilo de origen, neuropilo de destino)**. Familia del **NPC de Lin**. 40 realizaciones, semillas `1000 + 7i`. Instrumento: `src/twohop_nulls.py` md5 `a3d52df61a2bc2ccbb332a01c1353dba`.

### `P2` (caminos de 2 saltos hasta motoras de cabeza), umbral 1

| Clase | Null de GRADO | Null de NEUROPILO | ¿Cambia el signo? |
|---|---|---|---|
| **olfactory** | 0,0228× (z −51,8, 40/40) | **0,368×** (z −4,44, 40/40) | no, pero el efecto se divide por **16** |
| **visual** | 0,0606× (z −54,0, 40/40) | **1,531×** (z **+4,10**, 0/40) | 🔴 **SÍ: pasa a ENRIQUECIDA** |
| **mechanosensory** | 7,365× (z +342, 0/40) | **0,803×** (z **−20,6**, 40/40) | 🔴 **SÍ: pasa a DEPLETADA** |
| **gustatory** | 6,545× (z +249, 0/40) | **0,632×** (z **−37,2**, 40/40) | 🔴 **SÍ: pasa a DEPLETADA** |
| **CTRL arbitrario** | 0,652× | **1,010×** | 🔴 **el piso desaparece** |

**Umbral 5, mismo patrón:** olfactory 0,121× · visual **4,872× (z +10,9)** · mechano 0,974× (z −1,59, **38/40, no significativo**) · gustatory 0,376× · CTRL 1,147×.

**El spread de 323× colapsa a 2,4×** (1,531 / 0,632) y **el orden entre clases se invierte con los dos umbrales.**

### POR QUÉ, medido: las cuatro clases NO eran «igual de locales»

```
SALIDA_DOMINANTE_MOTORAS {'GNG': 89, 'PRW': 15, 'IPS_L': 3, 'IPS_R': 2, 'FLA_R': 1}
SALIDA_DOM olfactory      {'AL_L': 1295, 'AL_R': 981}
SALIDA_DOM visual         {'LA_L': 4250, 'LA_R': 3836, 'ME_R': 1315, 'ME_L': 1307}
SALIDA_DOM mechanosensory {'GNG': 1712, 'SAD': 468, 'AMMC_R': 242, 'AMMC_L': 164}
SALIDA_DOM gustatory      {'GNG': 353, 'PRW': 52, 'SAD': 3}
```

**DOS clases son locales al neuropilo motor y DOS son locales a neuropilos sensoriales. Eso es el efecto entero.** El argumento «la localidad no explica 323× entre poblaciones todas locales» **no era débil: era falso**, y a granularidad de neuropilo **gana BANC**.

### 🟢 Y lo que sobrevive es mejor: el blindaje está del otro lado

Acceso motor directo (`R1`) contra el null anatómico:

| Clase | Observado | Lo que predice su co-localización | z | nulls ≥ real |
|---|---|---|---|---|
| **gustatory** | **10** | **101,6 ± 1,2** | **−78,9** | 40/40 |
| **mechanosensory** | **64** | **98,6 ± 1,6** | **−21,7** | 40/40 |
| olfactory | 0 | 1,0 ± 0,9 | −1,2 | 40/40 |
| visual | 0 | 0,03 ± 0,16 | −0,2 | 40/40 |

A umbral 5: gustativa **2 contra 91,0**; mechano **33 contra 89,2**; olfatoria y visual, el null predice **exactamente 0,0**.

> **El enunciado correcto es el inverso del que tenía:** el cero de olfatorio y visual **no es blindaje, es geometría que el null predice exactamente**. El blindaje real está en las clases que **SÍ comparten neuropilo con las motoras**: gustativa entra al mismo neuropilo y conecta con **10 de 110** donde su co-localización predice **102**.

**⚠️ Salvedad que NO rescata el claim viejo:** para `R1` de olfatorio y visual el null **conserva la cantidad medida** (media ≈ 0) → esas dos filas son **NO TESTEABLES**, no refutadas. Para `P2` el null se mueve (`sd` 349 sobre media 2.451) y ahí el test es válido.

**Y el umbral de 5 arregla un artefacto:** sin umbral `R2` daba `sd = 0,0` (los 40 nulls al techo de 110); a umbral 5 el `sd` es **1,04** y el reach es estimable: olfatorio **1 de 109** contra 107,3 ± 1,0 (**z = −102**), visual **8** contra 107,3 (**z = −96**). Retención del umbral: **2.700.513 de 15.091.983 aristas (17,89%)**, 134.181 nodos, 109 de 110 motoras.

---

## 3.ter VALIDADO · el resto de la tabla

| Hallazgo | Número | Instrumento |
|---|---|---|
| Densidad real del grafo | **7,85197×10⁻⁴** · la publicada, 0,0074, es un **overflow de `int32`** reproducido a 8 cifras | resp 043 |
| **Reciprocidad** | 26,60% · 4.014.518 aristas · **rank 1º de 41, 20,59× vs CP, 0/40** · 47,27× vs MS. **La MAGNITUD no es distintiva y el desglose tiene prior art anatómico** | 40 nulls CP (`6057`) |
| **Tabla 5 recomputada** | **4 enriquecidas, 4 depletadas, 1 ≈esperada** (el paper dice 0 y 7) | resp 043 + 046 |
| Sensorial → KC directo | **0** en el real, 40/40 nulls MS dan 1.533–2.640 | nulls MS |
| Fracción plástica | 4,045% neuronas · 0,41% conexiones · 0,47% sinapsis | conteo puro |
| Ley de Dale | **0 mixtas de 138.005** (96.672 exc. puras, 41.333 inh. puras) | conteo puro |
| **`KC→MBON`** | 62.261 · **7,81× vs CP, 0/40** ← sobrevive **contra mi predicción** | 40 nulls CP |
| **`DAN→KC`** | 47.404 · **8,71× vs CP, 0/40** → firma presináptica. Es 23,5× `DAN→MBON` | 40 nulls CP |
| **`KC→KC`** | 293.762 · **7,26× vs CP, 0/40** | 40 nulls CP |
| `ALPN→KC` | 27.848 · 1,70× vs CP (débil pero 0/40) | 40 nulls CP |
| Script R completo | **30/30 valores** reproducidos, máx. 5×10⁻⁵. ⚠️ **A-10: si el mapeo `id2i` está mal, esto reproduce un bug** | 4 instrumentos |
| **`LC6→GF` = 0 CONTRA EL NULL ANATÓMICO** | el null predice **17,2 ± 3,1** socios, hay **0**, **z = −5,6** ← **este cero SÍ es una prohibición, no geometría** | resp 065 |
| Escape compilado | ganancia **40×** vs detector vecino no cableado | motor propio |
| **Los 40 nulls sobre las 12 clases** | **0/40 en 12/12.** El centro de aprendizaje está **BLINDADO** | doc `5937` |
| **RDI dinámico** | **z = 197**, y es el mismo fenómeno que el `sel_post` de §3 | doc `5977` |
| **La brecha con Lin, CERRADA** | con umbral ≥5: reciprocidad **13,98%** vs su 13,8% (1,30%) · sinapsis/conexión **12,647** vs 12,6 (0,37%) · densidad 1,405e-4 vs 1,61e-4 (12,7%, v783 vs v630) | resp 045 |
| Replicación cruzada JS/Python | 46,88× vs 47,27×; el 0,8% lo explica la convención de swaps | doc `5977` |
| **Priors medidos** | peso **lognormal(0,7034 , 0,8883)** · `inh_frac` de **0,068** a **0,513** · grado entrante CV 1,469 · fuerza CV 2,402 · **tabla de 95 pares de bloques** | doc `6057` |
| **C99 embebido en target** | **1.336 B de `.text` a `-Os`** en ESP32/ESP32-S3 | resp 039 |
| **2 saltos contra 40 nulls de GRADO** | 0/40 y 40/40 en las cuatro clases, spread 323,2×. **Los NÚMEROS se reproducen con código independiente; LA INTERPRETACIÓN se cayó (§3.bis)** | resp 061 + 063 |

### ✅ El 105 vs 110 está CERRADO (resp 061)

```
110 (super_class == 'motor')  =  105 brain_motor_neuron  +  1 neck_motor_neuron  +  4 sin cell_class
las 110 estan TODAS en el grafo (fuera = 0)
nerve: {'PhN': 40, 'MxLbN': 26, 'CV': 20, 'AN': 14, 'ON': 10}
status: 101 sin status, 9 'outlier_seg'
```

**La Tabla 5 con las poblaciones REALES del paper** (`cell_class`, `motor_n = 1485` exacto, `p_exc = 0,600272`):

```
clase         N_paper   N_mio   obs_exc   r_paper  r_ovf    ratio_OK    veredicto
mechano.         2659    2656     23010     1.300  1.314    12.378  ENRIQUECIDO
unk. sensory      131     131      1179     1.400  1.365    12.858  ENRIQUECIDO
AN                495    2231     27857     0.600  1.894    17.839  NO REPRODUCIBLE
gustatory         408     408      1280     0.500  0.476     4.482  ENRIQUECIDO
hygrosen.          74      74        13     0.030  0.027     0.251    DEPLETADO
thermosen.         29      29        14     0.070  0.073     0.690    ~ESPERADO
olfactory        2279    2279        80     0.005  0.005     0.050    DEPLETADO
visual          10853   10855       137     0.002  0.002     0.018    DEPLETADO
vis. optic      77521   77530      1679     0.003  0.003     0.031    DEPLETADO
```

**8 de 9 filas reproducen el ratio publicado con la densidad overflowed** → la fórmula y las poblaciones están **establecidas, no inferidas**.

---

## 4. 🔴 LAS OCHO AUTORREFUTACIONES DEL 24/25-ago, y todas tienen la misma forma

1. el **desglose de reciprocidad** era prior art de Lin (Fig. 5c, ED Fig. 6c)
2. el **cero de motoras de cabeza** era **geometría**, no prohibición
3. **«las cuatro clases son igual de locales» era FALSO** (104 de 110 motoras viven en GNG/PRW, y mechano y gustativa también)
4. el **piso de 0,652×** era anatomía, no propiedad del conectoma (contra neuropilos: 1,010×)
5. la **tabla de ruteo del sistema visual ya estaba publicada**, y **desde mi mismo snapshot** (Kind 2024 + Cell Type Explorer de `flywire-fafb:v783b`, resp 066-067)
6. el **«0 inhibitorias» del GF describía un recorte del 20%**: el GF es **67,6% central y 49,8% inhibitorio** (resp 068)
7. el **AMMC al 33,5%** era **localización de sinapsis**, no origen de señal; la real es **2,0%** (resp 068)
8. medí **`sel_peak` seis días**, y el pico es **lo único que este circuito no discrimina** (resp 070-071)

> **La forma común: medí bien y después afirmé sobre la NOVEDAD o la CAUSA sin medir eso. Las mediciones no fallaron nunca.**

**Las dos reglas que salen, y son las más caras:**
- **Buscar el prior art ANTES de medir.** El barrido de literatura costó menos que la corrida que lo precedió.
- **Antes de medir un par en un conectoma público, buscar si existe un CATÁLOGO NAVEGABLE de ese snapshot.** El conteo ya está publicado por construcción: **el null es el producto, no el número.**

**Y una refutación más, del 25-ago:** compilar **las 962** neuronas refutó mi predicción — el recorte **sobreestimaba** la selectividad de pico (resp 069). **τ heterogénea no rescata nada** (resp 070).

---

## 4.bis REFUTADO / NO TESTEABLE / RETIRADO · el resto

| Claim | Qué lo tumbó |
|---|---|
| **«la magnitud de la reciprocidad es distintiva de este conectoma»** | **🔴 NO SOSTENIDA (resp 050).** Lin la encuentra comparable en CINCO conectomas |
| **«el desglose de reciprocidad por circuito es propio»** | **🔴 FALSO Y RETIRADO (resp 057-059).** Queda **el EJE**, no la existencia del desglose |
| **«el null CP es aporte propio»** (§2.4) | **🔴 PRIOR ART: el NPC model de Lin et al. 2024** |
| **«1.652× con la densidad de Lin»** (doc `5117`) | **🔴 RETIRADO (resp 045).** Comparación cruzada; pareada da 995×, el publicable es 20,59× |
| **«jerarquía de ruteo: 283,2× y listo»** | **NO TESTEABLE contra el null fuerte:** `sd = 0,0` y 40/40 = cantidad conservada. Arreglo: null de **tripartición**, sin correr |
| **«el spread de 323× a 2 saltos es el resultado central de la v2»** | **🔴 REFUTADO por el null anatómico (resp 063): colapsa a 2,4× y tres signos se invierten.** `docs/SECCION-V2-DOS-SALTOS.md` **NO se publica como está** |
| **«la topología define ruteo y ganancia, no selectividad»** | **🔴 RETIRADO (resp 071): define selectividad POST-ESTÍMULO.** El 1,04× era la métrica equivocada |
| **«el erratum corrige un 1.559× que aparece 9 veces»** | **🔴 RETIRADO (resp 046):** el 1.559 **no existe en el PDF** |
| **«el desfasaje de un paso explica la discrepancia a t=60»** | **REFUTADO leyendo el código:** eran **dos métricas con el mismo nombre** |
| **«hay una discrepancia sin resolver entre 105 y 110 motoras»** | ✅ **CERRADO (resp 061):** conjuntos anidados |
| «el Paper 1 evita la densidad contaminada» | falso: §2.1 dice `Density = 0.0074` |
| «el guard de tautología es aporte propio» | §2.4 del paper ya lo declara |
| «0 clases enriquecidas / 7 depletadas» (el paper) | con la densidad correcta: **4 / 4 / 1** |
| «reciprocidad 36×» | **el MISMO overflow**: `0,266/0,00739526 = 35,97` |
| «τ_m = 8,4 ms, centro del rango» | el centro de 5-20 es **12,5**, y la derivación correcta es `-1/ln(1-τ) = 7,89` (error 6,47%) |
| «R = 1,31, retención selectiva» | cruza 1 en las tres modalidades según normalización |
| col-norm «respeta la varianza local» | lleva el CV de 2,402 a **cero** |
| **Tabla 8 reproducible** | **4 particiones con la definición EXACTA y ninguna reproduce la FORMA.** Los 6 valores no existen en los 40 notebooks: **falta el instrumento** |
| «hace falta una SNN para latencias» | la métrica al 10% del pico da mechano 4 < gust 5 < visual 6 < olf 10 |
| «el control lineal descarta saturación» | clipea: `max h = 2,0000` exacto en 2 de 3 modalidades |
| «la entropía baja distingue biología» | los nulls bajan más: dH −9,79 vs −2,88. **La FORMA sí, 7/12** |
| «visual es la vía con menos acceso motor» | **a 1 salto es olfactory.** Y contra neuropilos **visual pasa a enriquecida** |
| «sinapsis vs conexiones» explica el bug | existe como defecto de redacción, **la causa es el overflow** |
| «Therianos me refuta» | **retirado:** Lin mide 13,8% en adulto, Therianos usa conectoma **larval** |
| «el `temporal RDI` es frágil» | **error de eje.** El eje es CONTRA QUÉ NULL |
| «KC→MBON cae contra CP» (predicción mía) | **refutada: sobrevive con 7,81×, 0/40** |

---

## 5. 🔴 LA AUDITORÍA EXTERNA DE TAO · 62/100, RECHAZADO como release

**Rama `titan/auditoria-integra-2026-08-25`, PR #3.** 13 hallazgos, **13 aceptados, 0 rechazados** (resp 073). Verifiqué tres independientemente (A-02, A-06, A-09) y los tres dieron **CONFIRMADO**. A-06 era **peor** que su texto: mi shuffle por arista dejaba **862 de 864 neuronas mixtas** donde el grafo real tiene 0. **Corrí el null correcto y el `sel_post` sobrevivió.**

**Su diagnóstico, verbatim, y es el mejor resumen del estado real:**

> *«El problema no es que el proyecto no tenga resultados; es que **la rama pública, el ejecutor y el testigo no están alineados**.»*

**Los cinco bloqueantes, todos de INFRAESTRUCTURA:**

| # | Qué |
|---|---|
| **A-01** | los guards **imprimen rojo y salen con 0** |
| **A-02** | `src/guards.py` de `main` **confunde conservación con saturación** |
| **A-03** | no hay entorno reproducible: sin pins, sin lockfile, sin CI |
| **A-04** | los JSON chicos (191 KB y 31 KB) no están en `results/` |
| **A-05** | el clon fresco **no corre**: rutas `/workspace/` absolutas |

**El que más puede doler y NO verifiqué: A-10.** Si el mapeo `id2i` de `scriptR.py` no coincide con el índice real del parquet, **los 30/30 valores reproducidos reproducen un bug. Prioridad técnica máxima.**

**Lo que más vale de su auditoría, y no es un hallazgo:** mis ocho autorrefutaciones son **todas científicas**; sus cinco bloqueantes son **todos de infraestructura**, porque yo nunca miré ahí. **Es el sesgo de selección que un instrumento propio no cubre.**

---

## 6. NO MEDIDO / pendiente, declarado

1. **A-10: el mapeo `id2i` sin verificar.** Lo primero de la lista técnica.
2. **A-01 y A-02:** falta un `require()` único que aborte y tests negativos con exit ≠ 0. **Ya hay un ejemplo funcionando en `src/signshuffle_dale.py`** (returncode 2 verificado con `subprocess`, porque **el `$?` de este shell miente**).
3. **A-03:** pins, lockfile, CI mínimo. **A-04:** commitear los JSON chicos con su SHA-256. **A-05:** rutas por argumento — **los cinco scripts nuevos ya lo hacen, los dos `.mjs` del release no.**
4. **A-07 y A-08:** baseline **pareado en grado** y null anatómico **por sinapsis** en vez de neuropilo dominante.
5. **El neuropilo dominante es una aproximación.** El NPC de Lin asigna **por sinapsis**; este ensemble es de la **misma familia, no idéntico**, y **no se comparó midiendo**.
6. **No se corrió el NND** (distancia física). Las posiciones están en `annotations.tsv` (`pos_x/y/z`, `soma_x/y/z`) y **no se usaron**.
7. **El ensemble de neuropilos no preserva el grado entrante exacto**, solo dentro de bloque, y **los dos nulls no se combinaron**.
8. **No se midió la pureza de los bloques** (qué fracción de las aristas de cada bloque es de la clase medida) → no sé cuánto margen de movimiento le queda al null.
9. **El hallazgo de gustativa (10 contra 102) no tiene control de tripartición ni de distancia, y NO se barrió literatura.** Es el mismo error de la §4 si lo doy por propio.
10. **Del claim `sel_post`:** falta barrer la **ventana de integración** (integra 120 pasos cuando la memoria efectiva es ~8) y **τ compleja**, el banco de osciladores del motor real.
11. **La décima clase de la Tabla 5** (§2.3 declara 10, la tabla muestra 9): **no establecido cuál**. **La fila AN no es reproducible.** **Si los `p` usan `p_edge_exc`: no establecido.**
12. **El script de la Tabla 8 no está en el corpus.** Cero de 6 valores en 40 notebooks.
13. **Null de tripartición: no corrió.** **Faltan 21 nulls** para el test global de los 12 pares (~30 min, doc `5957`).
14. **Verificaciones externas pendientes:** los dos **DOI** contra Zenodo y **Betzel** (PLOS Complex Systems 3(3), e0000091). ✅ Lin, Dorkenwald, Bates y ARC verificados.
15. **Los valores de la Fig. 5c y la ED Fig. 6c de Lin NO se leyeron fila por fila**, y no busqué si publican la tabla numérica como Supplementary Data. **De Lin leí el cuerpo, no su Discussion ni sus Methods. No leí Dorkenwald.**
16. **`P2` cuenta caminos con multiplicidad y sin excluir intermediarios motores**; el null de grado genera **317 self-loops**; ignora signo y peso; **9 de las 110 motoras son `outlier_seg`** y no se midió excluirlas; **no se corrieron 3 saltos**.
17. **El barrido de Docs está al 71%:** 46 de ~65. **9 IDs pendientes** (`6157 6177 6197 6217 6237 6257 6277 6317 6337`), ~15 en icca-engine, ~50 entre `3637` y `4717`, MUDH/AURA sin tocar.
18. **Los dos JSON grandes van por md5:** `nulls40.json` (191.443 B, `38bf1fcadaf37a3b125f83d22b6f4d8e`) y `dualbrain_bench.json` (31.527 B, `1025d60b4e9521d7e4a21ed282935049`). **Los 6 `.py` de deuda siguen fuera de git** (`MANIFIESTO-KAGGLE.md`).
19. **Las tres figuras de 2 saltos no están commiteadas** (política del repo): `fig_twohop_a_pathcount.svg` `8a1806e9b16db8c4d3210523d51622ef` · `_b_reach.svg` `c420213caa112be0db40bb7049fc81a9` · `_c_normalised.svg` `6ffc18be441974d6fbe7239c6daef572`. **El generador es determinista y sí está commiteado.**
20. **El C99 embebido está medido a medias:** 1.336 B de `.text`, **sin `.elf`, sin RAM en target**, no corrió en hardware.
21. **`README.md` y `docs/METHODS.md` NO tienen la evidencia de las resp 053b, 057, 061, 063, 065 ni 071**, y sigue pendiente la reclasificación del `temporal RDI`.
22. **No corrió el review automático** sobre los archivos nuevos. **K-02: deuda declarada, no aprobación.**
23. **`CONTEXTO-motor.md` NO se abrió el 25-ago:** A-12 está cerrado **a la mitad** y ese archivo **no recibe veredicto de vigencia** (modo de falla 4).

---

## 7. Decisiones esperando a Abraham

1. **🔴 SUBIR EL ERRATUM A ZENODO antes del 30-ago.** `docs/ERRATUM.md`, 9 ítems, cero placeholders. **W-01: soy el único testigo de que la corrección está bien; leelo una vez.**
2. **🔴 EL CRONOGRAMA.** La infraestructura son días y no estaba en los cinco entregables. **O se corre el plan, o se mata un entregable.**
3. **¿Abro los 13 issues de la auditoría?** Son 5+ escrituras. Sin issues, los hallazgos son **deuda sin dueño**.
4. **Mergear o partir el PR #2** (nueve respuestas y siete scripts) y **cerrar o retargetear el PR #1**, que está viejo.
5. **Reclasificar el `temporal RDI` del `README`**, que hoy lo llama «negative methodological result» cuando **es lo único que BANC no cubre**.
6. **¿Adoptar el umbral de 5 sinapsis?** Los tres papers de referencia lo usan **y es técnicamente mejor**: destapó un estadístico que sin él no se podía usar.
7. **Reescribir `docs/SECCION-V2-DOS-SALTOS.md` con el veredicto invertido** (el blindaje de gustativa) en vez de con el spread de 323×.
8. **Bajar el 36× y el «massive reciprocity» del abstract** y poner el eje funcional (texto en `docs/PIVOTE-RECIPROCIDAD.md`). **Citar a Lin, el NPC y Bates como prior art.** **Agregar el párrafo de convergencia attractor/repeller** (lo más barato del plan).
9. **Los bugs del Script R viven DENTRO del verificador V-K** (doc `5637`), que **comparte el overflow**. Es el ítem 9 del erratum.
10. **¿ARC-AGI-2 en vez de ARC-AGI-3** para la elegibilidad? Ahorra la S7 entera.
11. **¿Arreglo las rutas absolutas de los dos `.mjs`?** **¿Subo los 6 `.py` y los dos JSON?**
12. **El barrido de Docs: ¿los 9 IDs del conectoma u otras zonas?** Org `Mendieta-Architect` o aceptar `gatehot59-star` en el erratum.
13. **¿Unifico también `CONTEXTO-motor.md`?** Es el otro medio A-12 y sale en un turno.

---

## 8. Estado de git y del entorno

**Rama de trabajo `titan/twohop-nulls`.** PRs abiertos: **#1** (viejo), **#2** (nueve respuestas + siete scripts), **#3** (la auditoría de Tao, rama `titan/auditoria-integra-2026-08-25`). **`main` intacta.**

**Ya en el repo:** `docs/ERRATUM.md` (9 ítems) · `docs/PIVOTE-RECIPROCIDAD.md` · `docs/SECCION-V2-DOS-SALTOS.md` (**a reescribir**) · `README.md` · `LICENSE` · `docs/METHODS.md` · `src/` (incluye `twohop_nulls.py`, `signshuffle_selpost.py`, `signshuffle_dale.py`) · `results/` con 5 logs · `docs/agents/` con los contextos, el índice, el manifiesto, la evidencia y **75 respuestas**.

**Verificado por md5 desde los dos lados (resp 045):** `motor.py`, `cp40.py`, `nulls40_kaggle.py` y `hm_sweep.py` son **byte-idénticos** al código que corrió en Kaggle.

**Entorno (medido el 24-ago, `CONTEXTO-ENTORNO.md` §13 · SE RE-MIDE, NO SE RECUERDA):** el container **no es efímero** (uptime 3,2 días), `git` no está instalado y todo pasa por la integración de GitHub, `nexus.db` no existe. Python 3.12.14, Node 24.18.0, R 4.5.3. `pypdf` se instala con `pip` (hay red). **Los Docs son ENUMERABLES:** IDs de página secuenciales **paso 20**, prefijo `2kza6fw5-`. Límite medido: **5 Docs completos no entran en una ventana.**

**🔴 El shell del gateway NO acepta saltos de línea ni heredocs:** un `python3 -c` multilínea llega con los `\n` literales y tira `SyntaxError`. **Todo script va en UNA línea con `;` y comprensiones**, o se lanza con `nohup … &` a un log y se polea con `tail`. **El timeout de una llamada está entre 45 y 75 s**: una corrida de 288-292 s **va al fondo**. Y `sep='\t'` no sobrevive: usar `sep=chr(9)`.

**Datos:** `/workspace/connectivity.parquet` (100.804.642 B, 15.091.983 filas, md5 `3d802fd542b5d18570ba1ba0bb0abed9`) y `/workspace/annotations.tsv` (31.718.505 B, md5 `719904abad876c68ace1b5690c9b9b63`). **31 columnas de anotación y ninguna es neuropilo** → los neuropilos vienen de **Zenodo `10676866` v783.0** (`per_neuron_neuropil_count_pre/post_783.feather`, 79 etiquetas).

---

## 9. Modos de falla propios de esta línea, y cada uno ya costó

**1 · Una lista hecha de lo que está a mano solo contiene lo que está a mano.** El `INDICE-DE-ENLACES.md` cosechado del chat, y el corpus de Kaggle (**29 archivos locales contra 40 kernels reales**). **El denominador se mide en la fuente, no en la copia.**

**2 · Un null cuyos invariantes incluyen la cantidad medida no es un control, es un espejo.** **Si `sd(null) == 0`, reportar NO TESTEABLE.** Antídoto aplicado (resp 061): meter una cantidad conservada **a propósito** (`_EDGES_INTO_MOT`, sd 0,0, 40/40) en la misma corrida. **Su primo:** `sd = 0` por **SATURACIÓN** no es espejo, es **censura** — la dirección vale, el tamaño no. **Y el 25-ago se descubrió que la censura de `R2` era un artefacto de no usar umbral.**

**3 · Una explicación que encaja no es una explicación medida.** Y su versión más caras: **dar por cerrado un problema porque UNA herramienta no lo resuelve.** El null anatómico se declaró no testeable durante días y el dato estaba en Zenodo, **a una llamada**.

**4 · Un archivo que no abrí en este turno no recibe veredicto de vigencia.**

**5 · Comparar dos cantidades medidas con criterios distintos. CINCO veces.**

**6 · Un test que no puede dar rojo no es un test. CUATRO veces.** El `$?` sobre una compilación fallida, un `grep -c` con falso cero por la coma de miles, un «clon limpio» que leía rutas absolutas, y un `grado_check_in` que comparaba `bincount(dst)` **contra sí mismo**, cometido **en el mismo turno en que se citaba este modo de falla**. Antídotos que funcionaron: **control negativo con nombre** (`ZZQQXX`) y **un método alternativo que DEBE romper el invariante** (el `dst` uniforme rompió el grado en 138.142 de 138.639 nodos).

**7 · Lo que no está commiteado se pierde justo cuando más falta hace.**

**8 · Un erratum aritmético no arregla un problema de framing.**

**9 · Una referencia incompleta se completa mal en el turno siguiente.** Corolario: **antes de afirmar que una cita está mal, verificar EN QUÉ está mal.**

**10 · Un claim de novedad se verifica contra las FIGURAS del trabajo previo, no contra su abstract.**

**11 · Verificar el sujeto no alcanza: hay que verificar la ESCALA a la que la explicación rival es cierta.** Y el 25-ago este modo **volvió a cobrar**: escribí «las cuatro clases son igual de locales» **sin medir dónde vive cada una**, y cuando lo medí, la rival explicaba el efecto entero.

**12 · Un ratio contra un null necesita saber cuánto da un sujeto CUALQUIERA contra ese mismo null.** El control arbitrario dio **0,652×** contra grado **y 1,010× contra neuropilos**: el «piso del conectoma» era anatomía. **El control barato es un sujeto al azar, y se corre ANTES de citar un ratio.**

**13 · 🆕 Buscar el prior art ANTES de medir.** Tres claims de novedad murieron por barridos de literatura que costaron menos que la corrida que los precedió.

**14 · 🆕 Antes de contar un par en un conectoma público, buscar si existe un CATÁLOGO NAVEGABLE de ese snapshot.** El Cell Type Explorer de `flywire-fafb:v783b` publica la tabla entera. **El conteo ya está publicado por construcción: el null es el producto, no el número.**

**15 · 🆕 Un instrumento propio no cubre el sesgo de selección de su dueño.** Mis ocho autorrefutaciones son todas **científicas**; los cinco bloqueantes de la auditoría externa son todos de **infraestructura**, porque yo nunca miré ahí. **W-01 no es burocracia: es el único modo de encontrar la clase de error que no busco.**
