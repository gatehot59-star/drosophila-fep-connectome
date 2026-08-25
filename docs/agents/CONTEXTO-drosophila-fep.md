# CONTEXTO VIVO · conectoma / FEP / papers

**Última actualización:** 2026-08-24 23:45 (America/Buenos_Aires) · **Se sobreescribe, no se acumula.**

Leer esto **antes** de responder cualquier cosa de este proyecto. Protocolo: `00-PROTOCOLO-BITACORA-DE-RESPUESTAS.md`. Hermano: `CONTEXTO-motor.md`. Índice de Docs: `INDICE-REAL-POR-ENUMERACION.md` (**parcial, 46 de ~65**). Entorno: `CONTEXTO-ENTORNO.md` §13. Kaggle: `MANIFIESTO-KAGGLE.md` (**40 kernels, no 29**).

---

## 0. 🚨 EL RELOJ · el erratum vence el 30-ago, y el texto ya está escrito Y CORREGIDO

**Fuente: doc `6117`, «PLAN MAESTRO 10 SEMANAS · 24-ago al 8-nov 2026».** Hoy es el 24-ago: **la S1 es esta semana.**

| # | El número que decide el éxito | Umbral | Estado |
|---|---|---|---|
| 1 | **Erratum en Zenodo** | **antes del 30-ago** | ✅ **texto listo, en git y con el claim falso retirado (resp 057-059)**; falta subirlo, y eso es de Abraham |
| 2 | Motivos con 0/40 en la biblioteca | ≥ 3 (hoy hay **1**) | sin avance |
| 3 | Nulls del motor complejo | **40** (piso de `p` 0,20 → 0,0488) | hoy 9 |
| 4 | Papers subidos | ≥ 2 antes del 8-nov | 0 |

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

**El riesgo real no es técnico:** son cinco entregables en diez semanas de **una persona**. El orden **es** la protección.

---

## 1. Son TRES papers más un motor. No mezclarlos nunca más

| Nombre | Qué es | Estado |
|---|---|---|
| **PAPER 1** | *Signal Propagation Properties in the Drosophila melanogaster Connectome: Intermodal Isolation, Differential Motor Access, and Non-Trivial Temporal Amplification*, Mendieta 2026a. **7 páginas, leído completo el 24-ago** | Zenodo 20-mar-2026. **DOI placeholder `XXXXXXX` literal en el header** |
| **PAPER 2** | *Topological Retention and Selective Convergence* — FEP, Markov blanket, Script R | Borrador. Va como resultado **negativo** (P5) o no va |
| **PATENTE** provisional | Congelada antes del erratum. Doc `5717`: **la patente tiene razón, el FALSIFIED es un artefacto** | En pausa |
| **Motor** | SparseLTC / DualBrain, C99 + ESP32 | **El activo real.** Ver `CONTEXTO-motor.md` |

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

**Son DOS papers distintos, del mismo número de la misma revista, más uno de 2026:**

| Referencia | Qué es | Páginas | De ahí sale |
|---|---|---|---|
| **Dorkenwald, S., Matsliah, A., et al. + FlyWire Consortium (2024).** *Neuronal wiring diagram of an adult brain.* Nature | **634:124–138** | el paper de **DATOS** | **12,6 sinapsis por conexión** · grado medio 20,5 |
| **Lin, A., Yang, R., et al. (2024).** *Network statistics of the whole-brain connectome of Drosophila.* Nature | **634:153–165** | el paper de **ANÁLISIS DE RED** | **densidad 0,000161** · **reciprocidad 0,138** · clustering 0,0463 · rich club · **y la reciprocidad POR NEUROPILO** |
| **Bates, A. S., Phelps, J. S., Kim, M., Yang, H. H., et al. (2026).** *Distributed control circuits across a brain-and-cord connectome.* Nature | doi:10.1038/s41586-026-10735-w | **cerebro + cordón**, publicado **8-jun-2026**, preprint **31-jul-2025**, **188.259 neuronas** | métrica de **influence** lineal, `R² = 0,94` en 94.278 pares |

**Verificado el 24-ago** contra `nature.com`, PMC (`PMC11446825`, `PMC11446842`, `PMC12324551`) y bioRxiv.

**Los parámetros de Lin:** snapshot **v630** (no v783), **umbral de 5 sinapsis por conexión**, 127.978 neuronas, 2.613.129 conexiones.

**Otros números de Lin:** rich club de **30%** con cutoff de grado 37 y probabilidad interna 0,000870 = **5,4×** la global · small-worldness **SΔ = 141** · SCC gigante 93,3% · WCC 98,8% · camino dirigido medio **4,42 saltos**, todos alcanzables en 13 · **77.607 de 127.978** neuronas participan de al menos una conexión recíproca · **1.863 NSRNs** · cuatro nulls: **ER, CFG (grado), NPC (neuropilos) y NND (distancia)**.

**Su Table 2, leída fila por fila, y hay que tenerla a mano:** reciprocidad 0,138 = **×858 vs ER, ×43,8 vs CFG, ×45,9 vs NND, ×7,22 vs NPC**. Clustering 0,0463 = ×144 / ×7,57 / ×10,9 / ×2,88.

> **🔑 El dato más útil de esa tabla, y hay que usarlo como calibración de expectativas:** pasar de un null de **grado** (CFG, ×43,8) a uno **anatómico** (NPC, ×7,22) **se come el 84% del efecto**. Cualquier resultado propio medido solo contra grado hay que leerlo sabiendo que un null espacial se lleva ese orden de magnitud.

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

Y el Paper 1, **por conteo de aristas contra nulls que preservan grado**, mide que **olfactory y visual son las más depletadas** en acceso motor. **Dos métodos que no comparten nada llegando al mismo ruteo.** Va como *«consistente con la estructura de atractores y repulsores reportada independientemente por Lin et al. (2024)»*. **NO MEDIDO: la convergencia es cualitativa, el solapamiento no está cuantificado.**

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

Y declara **dos renuncias**: *«we take its **steady-state response**»* y *«adjusted influence is an **unsigned quantity**»*. **Sin signo** no hay cancelación GABAérgica → Propiedad 1 invisible. **Sin transitorio** no hay post-estímulo → Propiedad 3 también. **El campo llegó al método y se detuvo donde empieza el aporte.**

**Y dos frases más de BANC que conviene tener:** que las regiones cognitivas son *«supervisory but not essential for action»* (apoya el framing del 0,41% encerrado), y que los efectores *«are primarily influenced by sensory neurons in the **same body part**»* (la explicación rival de localidad, ver §5.13).

### El veredicto de relación: **SECUENCIALES**

Lin: estructura. Paper 1: primera película dinámica. BANC: institucionalización del baseline lineal a escala grande. **Y BANC no te tomó: su preprint es de jul-2025, tu preprint de mar-2026. Es convergencia metodológica.**

---

## 3. VALIDADO

| Hallazgo | Número | Instrumento |
|---|---|---|
| Densidad real del grafo | **7,85197×10⁻⁴** · y la publicada, 0,0074, es un **overflow de `int32`** reproducido a 8 cifras | resp 043 |
| **Reciprocidad** | 26,60% · 4.014.518 aristas · **rank 1º de 41, 20,59× vs CP, 0/40** ← **lo publicable** · 47,27× vs MS. **Pero la MAGNITUD no es distintiva Y el desglose tiene prior art anatómico** | 40 nulls CP (`6057`) |
| **Tabla 5 recomputada** | **4 enriquecidas, 4 depletadas, 1 ≈esperada** (el paper dice 0 y 7) | resp 043 + 046 |
| Sensorial → KC directo | **0** en el real, 40/40 nulls MS dan 1.533–2.640 | nulls MS |
| Fracción plástica | 4,045% neuronas · 0,41% conexiones · 0,47% sinapsis | conteo puro |
| Ley de Dale | **0 mixtas de 138.005** (96.672 exc. puras, 41.333 inh. puras) | conteo puro |
| **`KC→MBON`** | 62.261 · **7,81× vs CP, 0/40** ← sobrevive **contra mi predicción** | 40 nulls CP |
| **`DAN→KC`** | 47.404 · **8,71× vs CP, 0/40** → firma presináptica. Es 23,5× `DAN→MBON` | 40 nulls CP |
| **`KC→KC`** | 293.762 · **7,26× vs CP, 0/40** | 40 nulls CP |
| `ALPN→KC` | 27.848 · 1,70× vs CP (débil pero 0/40) | 40 nulls CP |
| Script R completo | **30/30 valores** reproducidos, máx. 5×10⁻⁵ | 4 instrumentos |
| Circuito de escape | 9,1× LC4→GF · LC6→GF = 0 aristas · 0/40 | 40 nulls CP |
| Escape compilado | ganancia **40×** vs detector vecino no cableado | motor propio |
| **Los 40 nulls sobre las 12 clases** | **0/40 en 12/12.** El centro de aprendizaje está **BLINDADO** | doc `5937` |
| **RDI dinámico** | **z = 197.** El resultado **más fuerte** del expediente, **y el territorio que BANC declara no cubrir** | doc `5977` |
| **La brecha con Lin, CERRADA** | con umbral ≥5: reciprocidad **13,98%** vs su 13,8% (1,30%) · sinapsis/conexión **12,647** vs 12,6 (0,37%) · densidad 1,405e-4 vs 1,61e-4 (12,7%, v783 vs v630) | resp 045 |
| Replicación cruzada JS/Python | 46,88× vs 47,27×; el 0,8% lo explica la convención de swaps | doc `5977` |
| **Priors medidos** | peso **lognormal(0,7034 , 0,8883)** · `inh_frac` de **0,068** a **0,513** · grado entrante CV 1,469 · fuerza CV 2,402 · **tabla de 95 pares de bloques** | doc `6057` |
| **C99 embebido en target** | **1.336 B de `.text` a `-Os`** en ESP32/ESP32-S3 | resp 039 |
| **⭐ ACCESO MOTOR A 2 SALTOS CONTRA 40 NULLS DE GRADO** | ver el bloque de abajo. **0/40 y 40/40 en los cuatro, spread 323,2×** | **resp 061** |

### ⭐ El acceso motor a 2 saltos, con null · resp 061

**Estadístico: `P2` = cantidad de caminos de 2 saltos hasta motoras de cabeza.** R2 (motoras distintas alcanzadas) **se satura**: los 40 nulls dan 110 de 110, `sd = 0`, así que sirve la dirección pero **no el tamaño de efecto**. `P2` es graduado y es el que responde al grado.

| Clase | Real | Null μ | Null sd | Ratio crudo | **Ratio vs el piso 0,652** | z | nulls ≥ real |
|---|---|---|---|---|---|---|---|
| **olfactory** | 901 | 39.522,6 | 745,7 | 0,0228× | **0,0350×** (28,6× depletado) | **−51,8** | **40/40** |
| **visual** | 1.413 | 23.311,6 | 405,3 | 0,0606× | **0,0929×** (10,8× depletado) | **−54,0** | **40/40** |
| **mechanosensory** | 293.022 | 39.787,8 | 740,2 | 7,37× | **11,29×** | **+342,1** | **0/40** |
| **gustatory** | 67.439 | 10.304,1 | 229,7 | 6,54× | **10,03×** | **+248,8** | **0/40** |

**El spread entre extremos es 323,2× y es invariante a la normalización.** A 1 salto contra nulls de grado el spread daba **283×**: dos profundidades, dos mediciones independientes, mismo orden.

**El cero de 1 salto ahora tiene expectativa, y es lo más limpio:** motoras distintas alcanzadas a 1 salto, **olfactory 0 contra 71,3 ± 4,6 (z = −15,4)** y **visual 0 contra 52,3 ± 5,2 (z = −10,0)**. Ningún null bajó de 56 ni de 43.

**🆕 El piso de 0,652×, que corrige mis propios números:** un control de 10.855 nodos **al azar** da `P2` real 312.457 contra null 479.030 ± 7.189, o sea **0,652×**. El conectoma real tiene menos caminos de 2 saltos que un grafo de configuración **en general**, no solo para las sensoriales. **Los ratios crudos se leen contra 0,652, no contra 1,0**, o un revisor que corra su propio control lo encuentra. *Salvedad: el control no está pareado en grado (1.187.513 aristas contra 57.764–98.782), es un orden de magnitud.*

**Los dos guards, y los dos pueden dar rojo:**

```
GUARD in-degree permutacion vs real: IGUAL_OK
CONTROL NEGATIVO dst uniforme (DEBE romper grado): DISTINTO_OK_el_guard_puede_dar_rojo
  nodos con in-degree roto por el uniforme: 138142 de 138639
ESPEJO A PROPOSITO _EDGES_INTO_MOT: real 19860, null 19860, sd 0.0, 40/40
```

El segundo es una cantidad **conservada por construcción**, metida en la misma corrida: si el estadístico principal se hubiera comportado así, el veredicto era **NO TESTEABLE**. **No se comportó así, y ahora está demostrado en vez de argumentado.**

### ✅ Y el 105 vs 110 está CERRADO (resp 061)

```
110 (super_class == 'motor')  =  105 brain_motor_neuron  +  1 neck_motor_neuron  +  4 sin cell_class
las 110 estan TODAS en el grafo (fuera = 0)
nerve: {'PhN': 40, 'MxLbN': 26, 'CV': 20, 'AN': 14, 'ON': 10}
status: 101 sin status, 9 'outlier_seg'
```

La resp 053b usó `cell_class == 'brain_motor_neuron'` (105) y la 057 `super_class == 'motor'` (110). **Ninguna estaba mal: eran dos poblaciones anidadas y no se declaró.** La resp 061 mide **con los dos denominadores en paralelo** y el veredicto no cambia.

**La Tabla 5, con las poblaciones REALES del paper** (`cell_class`, `motor_n = 1485` **exacto**, `p_exc = 0,600272`):

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

**8 de 9 filas reproducen el ratio publicado con la densidad overflowed**, así que la fórmula y las poblaciones están **establecidas, no inferidas**.

---

## 4. REFUTADO / NO TESTEABLE / RETIRADO

| Claim | Qué lo tumbó |
|---|---|
| **«la magnitud de la reciprocidad es distintiva de este conectoma»** | **🔴 NO SOSTENIDA (resp 050).** Lin la encuentra **comparable en CINCO conectomas**. **Hay que bajar el claim del abstract** |
| **«el desglose de reciprocidad por circuito es propio porque Nature da solo una cifra global»** (mío, resp 052 + pivote v1) | **🔴 FALSO, VERIFICADO Y RETIRADO (resp 057).** Lin descompone reciprocidad **por neuropilo en la Fig. 5c**, y en la **ED Fig. 6c normalizada por densidad** en los 78. **Estaba en el `ERRATUM.md` ítem 3, que va a Zenodo.** Corregido en la resp 059. **Lo que queda: el EJE, no la existencia del desglose** |
| **«el cero visual/olfatorio→motoras de cabeza refuta la localidad de BANC»** (mío, resp 053b) | **🟡 SE DEGRADA (resp 057).** Refuta la localidad a escala de **parte del cuerpo**, y **confirma** la de **neuropilo**: las ORN proyectan solo al AL y los fotorreceptores solo a lámina/médula (literatura de 2000-2004), y **17.503 de los 21.019 socios de visual a 1 salto son del propio lóbulo óptico**. Encima **gustatory sí llega a 10 motoras a 1 salto**. **E-01 sobre la ESCALA de la explicación rival.** → **rescatado a 2 saltos con null, resp 061, ver §3 y §5.13** |
| **«el null CP es aporte propio»** (§2.4 del paper) | **🔴 PRIOR ART: el NPC model de Lin et al. 2024.** Misma familia, otra granularidad |
| **«1.652× con la densidad de Lin»** (doc `5117`) | **🔴 RETIRADO (resp 045).** **Comparación cruzada.** Pareada da **995×**, y el publicable es **20,59× contra 40 nulls CP** |
| **«jerarquía de ruteo: 283,2× y listo»** | **NO TESTEABLE contra el null fuerte** (doc `6057`): `sd = 0,0` exacto y 40/40. **Es cantidad conservada** bajo CP. Arreglo: null de **tripartición**, sin correr |
| **«el desfasaje de un paso explica la discrepancia a t=60»** (mío) | **REFUTADO por lectura del código** (doc `6017`). La causa eran **dos métricas con el mismo nombre** |
| **«el erratum corrige un 1.559× que aparece 9 veces»** (borrador) | **🔴 RETIRADO (resp 046):** el 1.559 **no existe en el PDF**. **Un erratum que corrige un claim que el paper no hizo es él mismo un error** ← **y esta misma falla se repitió apuntando a Nature** |
| **«el contexto cita a Lin con las páginas de Dorkenwald»** (mío, resp 050) | **🔴 IMPRECISO (resp 051).** El defecto era una referencia **incompleta**, no **miscitada** |
| **«el erratum está listo / no está listo / no existe en git»** | **CERRADO: `docs/ERRATUM.md` existe, 9 ítems, cero placeholders, claim falso retirado, Bates citado.** Falta **subirlo a Zenodo** |
| **«los 2 saltos son una observación cruda sin null»** | ✅ **CERRADO (resp 061): 40 nulls de grado, 0/40 y 40/40 en las cuatro clases, spread 323,2×.** Pero sigue **sin null anatómico** |
| **«hay una discrepancia sin resolver entre 105 y 110 motoras»** | ✅ **CERRADO (resp 061):** conjuntos anidados, la diferencia son 1 `neck_motor_neuron` + 4 sin `cell_class` |
| «el Paper 1 evita la densidad contaminada» | falso: §2.1 dice `Density = 0.0074` y el Abstract dice 36× |
| «el guard de tautología es aporte propio» | §2.4 del paper ya lo declara y lo deriva |
| «0 clases enriquecidas / 7 depletadas» (el paper) | con la densidad correcta: **4 enriquecidas, 4 depletadas, 1 ≈esperada** |
| «**4 de 9 clases pasan a enriquecidas**», retirado por el `5177` | **🔄 EL RETIRO SE REVIERTE (resp 043).** El `5177` usó el **85.821 de la Tabla 4, que es una SUMA DE PESOS**, como conteo de aristas; el real es **23.010** |
| «reciprocidad 36×» | **es el MISMO overflow**: `0,266/0,00739526 = 35,97` |
| «τ_m = 8,4 ms, centro del rango» | **dos defectos:** el centro de 5-20 es **12,5** (y 3,3 está **debajo**), **y** la derivación correcta es `-1/ln(1-τ) = 7,89`, error 6,47% |
| «R = 1,31, retención selectiva» | cruza 1 en las tres modalidades según normalización (visual 1,878 → 0,811) |
| col-norm «respeta la varianza local» | lleva el CV de 2,402 a **cero** |
| **Tabla 8 reproducible** | **4 particiones con la definición EXACTA del código y ninguna reproduce la FORMA.** Los 6 valores **no existen en ninguno de los 40 notebooks**: falta el instrumento |
| «hace falta una SNN para latencias» | la métrica al 10% del pico da mechano 4 < gust 5 < visual 6 < olf 10 |
| «el control lineal descarta saturación» | clipea: `max h = 2,0000` exacto en 2 de 3 modalidades |
| «la topología explica la función» | el escape compilado da selectividad temporal 1,04×. **Define ruteo y ganancia, no selectividad** |
| «la entropía baja distingue biología» | los nulls bajan más: dH −9,79 vs −2,88. Doc `5777`: **la FORMA sí, 7/12** |
| «visual es la vía con menos acceso motor» | **a 1 salto no: es olfactory** (doc `5937`, y confirmado en resp 061: olfactory 0,0228× contra visual 0,0606×). **A 2 saltos visual toca menos motoras (15 vs 23) pero está menos depletada en caminos.** Son dos preguntas distintas |
| «sinapsis vs conexiones» explica el bug de densidad | **existe como defecto de redacción pero NO es la causa**: es el overflow |
| «Therianos me refuta» | **retirado:** Lin mide 13,8% en el adulto y Therianos usa conectoma **larval** |
| «el `temporal RDI` es frágil» (mío) | **error de eje** (doc `5977`). **El eje es CONTRA QUÉ NULL** |
| «KC→MBON cae contra CP» (predicción mía) | **refutada: sobrevive con 7,81×, 0/40** |

---

## 5. NO MEDIDO / pendiente, declarado

1. **La décima clase de la Tabla 5.** §2.3 declara 10, la tabla muestra 9. **Cuál falta: no establecido.**
2. **La fila AN no es reproducible.** `N=495` no sale de ningún filtro consistente. Declarada así en el erratum.
3. **Si los `p` de la Tabla 5 usan `p_edge_exc`** u otra probabilidad.
4. **El script de la Tabla 8: no está en el corpus.** Cero de 6 valores en 40 notebooks.
5. **Null de tripartición: no corrió.**
6. **Faltan 21 nulls** para el test global de los 12 pares (~30 min, doc `5957`).
7. **Verificaciones externas pendientes:** los dos **DOI** contra Zenodo, y **Betzel** (PLOS Complex Systems 3(3), e0000091). ✅ Lin, Dorkenwald, Bates y las fechas de ARC están verificados.
8. **🔴 Los valores de la Fig. 5c y la ED Fig. 6c de Lin NO se leyeron fila por fila.** Sé qué miden por el pie de figura y el texto. **Si algún neuropilo corresponde funcionalmente a un circuito de la Table 7, «ortogonal» es demasiado generoso.** Y **no busqué si publican la tabla numérica como Supplementary Data**.
9. **De Lin leí el cuerpo, no su Discussion ni sus Methods.** La **Table 2 sí está leída fila por fila**. **No leí Dorkenwald et al.**
10. **NPC vs CP no se compararon midiendo.**
11. ✅ **CERRADO (resp 061): los 2 saltos ya tienen 40 nulls de grado.** Ver §3. **Lo que sigue abierto es la §5.13.**
12. ✅ **CERRADO (resp 061): el 105 vs 110.** Conjuntos anidados, diferencia de 5 neuronas identificadas.
13. **🔴 EL HUECO PRINCIPAL AHORA: no hay null ANATÓMICO, y no es testeable con los datos locales.** Un null de grado baraja destinos por todo el cerebro sin respetar neuropilos, así que **cualquier restricción espacial se ve como un efecto enorme**. Calibración de cuánto puede costar: en Lin, pasar de CFG (×43,8) a NPC (×7,22) **se come el 84% del efecto**. `annotations.tsv` tiene **31 columnas y ninguna es neuropilo**: hay que bajar la asignación de sinapsis a neuropilos, o posiciones para un NND. **Estado correcto: establecido contra grado, NO testeado contra anatomía.**
   **🟢 Lo que SÍ aguanta sin el NPC, y es el argumento a escribir:** la comparación **entre clases**. Mechanosensorial y gustativa **también** tienen árboles localizados y **también** entran por nervios de la cabeza, y dan **+7,37× y +6,54×** donde visual y olfatoria dan 0,02× y 0,06×. **La localidad no explica 323× entre cuatro poblaciones que son todas locales.**
14. **Del barrido de 2 saltos (resp 061), lo no medido:** `P2` cuenta caminos **con multiplicidad y sin excluir intermediarios motores**; el null genera **317 self-loops** y aristas múltiples (familia configuración, no MS con rechazo), sesgo que va **a favor** del lado depletado; **ignora signo y peso**; **sin umbral de ≥5 sinapsis**, o sea **no comparable con Lin ni Bates**; **9 de las 110 motoras son `outlier_seg`** y no se midió si excluirlas cambia algo; **no se corrieron 3 saltos**; y el control aleatorio **no está pareado en grado**.
15. **No barrí exhaustivamente si el cero ya está publicado.** Lo más cercano: **Miroschnikow et al. 2018** (eLife, citado por BANC) muestra sensorial→motor monosináptico **sí existe** en la **larva**; y los papers de grooming de cabeza (Hampel 2015, Eichler 2024, Calle-Schuler 2026, Nat Commun abr-2026) trabajan con circuitos multicapa **como supuesto, no como cero medido**. **Apoyado, no establecido.**
16. **Los tres notebooks con overflow se declaran descendientes** de un «pipeline original» que **no está en el corpus**. **Apoyado** por reproducir 8 de 9 ratios, **no establecido**.
17. **Un solo patrón de overflow barrido** (`N*(N-1)`). No barrí `N**2`.
18. **El barrido de Docs está al 71%:** 46 de ~65. **9 IDs pendientes** (`6157 6177 6197 6217 6237 6257 6277 6317 6337`), ~15 en icca-engine, ~50 entre `3637` y `4717`, MUDH/AURA sin tocar.
19. **Los dos `.mjs` del release no corren en un clon ajeno:** rutas absolutas `/workspace/...`. **Declarado en README y METHODS, no parcheado.** Mi test de «clon limpio» dio un **falso verde** (resp 047).
20. **Los dos JSON grandes van por md5**, no commiteados: `nulls40.json` (191.443 B, `38bf1fcadaf37a3b125f83d22b6f4d8e`) y `dualbrain_bench.json` (31.527 B, `1025d60b4e9521d7e4a21ed282935049`).
21. **Los 6 `.py` de deuda siguen fuera de git.** Manifiesto en `MANIFIESTO-KAGGLE.md`.
22. **El C99 embebido está medido a medias:** 1.336 B de `.text` en target, **sin `.elf`, sin RAM en target**, no corrió en hardware.
23. **No corrí el review automático** sobre los archivos nuevos. **K-02: deuda declarada.**
24. **El `README.md` y `docs/METHODS.md` NO tienen la evidencia nueva** de las resp 053b, 057 ni 061. Y sigue pendiente la reclasificación del `temporal RDI`.

---

## 6. Decisiones esperando a Abraham

1. **🔴 SUBIR LA v2 A ZENODO antes del 30-ago.** El texto está en **`docs/ERRATUM.md`**, 9 ítems, cero placeholders, **con el claim falso sobre Lin retirado y Bates citado**. **W-01: soy el único testigo de que la corrección es correcta; leerlo una vez antes de subir.**
2. **Re-verificar los dos DOI contra Zenodo** antes de pegarlos, y **verificar Betzel**.
3. **🔴 El `README.md` público clasifica los resultados dinámicos como «negative methodological result»**, y **lo dinámico es lo único que BANC declara no cubrir**. **Le puse un bloque «Pending revision»; reclasificarlo es tu decisión.**
4. **Bajar el 36× y el «massive reciprocity» del abstract**, y poner en su lugar el **eje funcional** de la Table 7. Texto listo en **`docs/PIVOTE-RECIPROCIDAD.md`**.
5. **Citar a Lin, el NPC model y Bates et al. como prior art** en la v2.
6. **Agregar el párrafo de convergencia** attractor/repeller. Lo más barato del plan.
7. **¿Adoptar el umbral de 5 sinapsis?** **Los TRES papers de referencia lo usan.** El Paper 1 es el único que no. **Y ahora también afecta al barrido de 2 saltos, que corrió sin umbral.**
8. **⭐ Los bugs del Script R viven DENTRO del verificador V-K** (doc `5637`), que **comparte el overflow** (resp 044). **Es el ítem 9 del erratum.**
9. **Buscar el script de la Tabla 8.** Si aparece, se corre en una hora.
10. **¿ARC-AGI-2 en vez de ARC-AGI-3** para la elegibilidad? Ahorra la S7 entera.
11. **Mergear el PR #1**, o decir qué le falta.
12. **¿Arreglo las rutas absolutas de los dos `.mjs`?**
13. **El barrido de Docs: ¿sigo con los 9 IDs del conectoma o abro las otras zonas?**
14. **Subir los 6 `.py` de deuda y los dos JSON grandes.**
15. Org `Mendieta-Architect` o aceptar la URL `gatehot59-star` en el erratum.
16. **🆕 El resultado de 2 saltos está listo para la v2 del paper y NO está escrito en ninguna parte del paper.** Es material nuevo, no una corrección de v1.0, así que **no va al erratum**. ¿Lo redacto como sección de la v2?
17. **🆕 ¿Consigo la asignación a neuropilos para poder correr el null anatómico?** Es lo único que separa el resultado de 2 saltos de «establecido contra grado» a «establecido, punto». Sin eso, la §5.13 queda como limitación declarada.

---

## 7. Estado de git y del entorno, medido

**Ya en el repo:** `docs/ERRATUM.md` (**9 ítems, corregido el 24-ago 23:15**) · `docs/PIVOTE-RECIPROCIDAD.md` (**corregido**) · `README.md` · `LICENSE` · `docs/METHODS.md` · `src/` con 8 archivos · `results/` con 5 logs · `docs/agents/` con los cuatro contextos, el índice, el manifiesto de Kaggle, la evidencia y **61 respuestas**.

**Verificado por md5 desde los dos lados (resp 045):** cuatro archivos de `src/` son **byte-idénticos** al código que corrió en Kaggle (`motor.py`, `cp40.py`, `nulls40_kaggle.py`, `hm_sweep.py`).

**Entorno:** el container **no es efímero** (uptime 3,2 días medido), `git` no está instalado y todo pasa por la integración de GitHub, `nexus.db` **no existe**. Python 3.12.14, Node 24.18.0, R 4.5.3. **`pypdf` no venía instalado y se instala con `pip` (hay red).** **Los Docs son ENUMERABLES:** IDs de página secuenciales **paso 20**, prefijo `2kza6fw5-`. Límite medido: **5 Docs completos no entran en una ventana**.

**🆕 El shell del gateway NO acepta saltos de línea ni heredocs:** un `python3 -c` multilínea llega con los `\n` literales y tira `SyntaxError`. **Todo script va en UNA línea con `;` y comprensiones**, o se lanza con `nohup ... &` redirigiendo a un log y se polea con `tail`. **El timeout de una llamada está entre 45 y 75 s**: una corrida de 292 s **hay que mandarla al fondo**. Y `sep='\t'` no sobrevive: usar `sep=chr(9)`.

**Datos:** `/workspace/connectivity.parquet` (100.804.642 B, 15.091.983 filas, md5 `3d802fd542b5d18570ba1ba0bb0abed9`) y `/workspace/annotations.tsv` (31.718.505 B, md5 `719904abad876c68ace1b5690c9b9b63`). **Columnas de anotación: 31, y NINGUNA es neuropilo** — por eso la §5.13.

---

## 8. Modos de falla propios de esta línea, y cada uno ya costó

**1 · Una lista hecha de lo que está a mano solo contiene lo que está a mano.** Dos veces: el `INDICE-DE-ENLACES.md` cosechado del chat, y el corpus de Kaggle (**29 archivos locales contra 40 kernels reales**). **El denominador se mide en la fuente, no en la copia.**

**2 · Un null cuyos invariantes incluyen la cantidad medida no es un control, es un espejo.** **Si `sd(null) == 0`, reportar NO TESTEABLE**, no `1,000×`. **Antídoto que ya se aplicó (resp 061): meter en la misma corrida una cantidad conservada A PROPÓSITO** (`_EDGES_INTO_MOT`, sd 0,0, 40/40) para demostrar que el estadístico principal **no** se comporta así. **Y su primo: un estadístico con `sd = 0` por SATURACIÓN (el null llega al techo) NO es un espejo** — ahí el null difiere del real, la dirección vale y lo que no es estimable es el **tamaño** del efecto. Se reporta **censurado**.

**3 · Una explicación que encaja no es una explicación medida.** El «desfasaje» se escribió en un documento destinado a un DOI **sin leer el código**. Y la **causa** del overflow apareció solo al **ejecutar**.

**4 · Un archivo que no abrí en este turno no recibe veredicto de vigencia.**

**5 · Comparar dos cantidades medidas con criterios distintos. CINCO veces.** El `5177`, el `5117`, el borrador del erratum, el `1,18× sobre LSTM` contra el `4× en contra`, **y la Table 7 sin umbral conviviendo con el 13,98% con umbral**.

**6 · Un test que no puede dar rojo no es un test. Y este es el que más reincide: CUATRO veces.** El `$?` reportando `exit=0` sobre una compilación fallida, un `grep -c` con falso cero por la coma de miles, un «clon limpio» que leía rutas absolutas, **y el 24-ago un `grado_check_in` que comparaba `bincount(dst)` contra SÍ MISMO** (resp 061), cometido **en el mismo turno en que se citaba este modo de falla**. **Antídotos que funcionaron: control negativo con nombre (`ZZQQXX` en los conteos de términos) y un método alternativo que DEBE romper el invariante** (el `dst` uniforme rompió el grado en 138.142 de 138.639 nodos, o sea el guard puede dar rojo).

**7 · Lo que no está commiteado se pierde justo cuando más falta hace.**

**8 · Un erratum aritmético no arregla un problema de framing.** **Antes de poner un número en un abstract, buscar quién midió lo mismo en otro sistema.**

**9 · Una referencia incompleta se completa mal en el turno siguiente.** Y el corolario: **antes de afirmar que una cita está mal, verificar EN QUÉ está mal**.

**10 · Un claim de novedad se verifica contra las FIGURAS del trabajo previo, no contra su abstract.** El erratum llegó a decir que Lin *«reporta solo una cifra global»* porque leí su abstract, su Table 2 y su sección de reciprocidad, **y no su lista de figuras**. **Un paper no anuncia en el abstract todo lo que midió.**

**11 · Verificar el sujeto no alcanza: hay que verificar la ESCALA a la que la explicación rival es cierta.** Refuté «localidad anatómica» a escala de parte del cuerpo y canté victoria, cuando a escala de **neuropilo** la localidad **explica** el cero. **Una explicación rival puede ser falsa a una granularidad y verdadera a otra: hay que decir a cuál.** **Antídoto que funcionó (resp 061): cuando no se puede construir el null que controla la rival, buscar el contraste que la rival NO puede explicar** — acá, que cuatro poblaciones **igual de locales** difieran 323×.

**12 · 🆕 Un ratio contra un null necesita saber cuánto da un sujeto CUALQUIERA contra ese mismo null.** El control aleatorio de la resp 061 dio **0,652×**, o sea que el grafo real tiene menos caminos de 2 saltos que un grafo de configuración **en general**. Sin ese control, los ratios crudos estaban inflados **en los dos sentidos** y el número «43,9× depletado» se publicaba cuando el correcto es **28,6×**. **El control barato es un sujeto al azar, y hay que correrlo ANTES de citar un ratio.**
