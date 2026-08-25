# CONTEXTO VIVO · conectoma / FEP / papers

**Última actualización:** 2026-08-24 21:05 (America/Buenos_Aires) · **Se sobreescribe, no se acumula.**

Leer esto **antes** de responder cualquier cosa de este proyecto. Protocolo: `00-PROTOCOLO-BITACORA-DE-RESPUESTAS.md`. Hermano: `CONTEXTO-motor.md`. Índice de Docs: `INDICE-REAL-POR-ENUMERACION.md` (**parcial, 46 de ~65**). Entorno: `CONTEXTO-ENTORNO.md` §13. Kaggle: `MANIFIESTO-KAGGLE.md` (**40 kernels, no 29**).

---

## 0. 🚨 EL RELOJ · el erratum vence el 30-ago, y el texto ya está escrito

**Fuente: doc `6117`, «PLAN MAESTRO 10 SEMANAS · 24-ago al 8-nov 2026».** Hoy es el 24-ago: **la S1 es esta semana.**

| # | El número que decide el éxito | Umbral | Estado |
|---|---|---|---|
| 1 | **Erratum en Zenodo** | **antes del 30-ago** | ✅ **texto listo y en git**; falta subirlo, y eso es de Abraham |
| 2 | Motivos con 0/40 en la biblioteca | ≥ 3 (hoy hay **1**) | sin avance |
| 3 | Nulls del motor complejo | **40** (piso de `p` 0,20 → 0,0488) | hoy 9 |
| 4 | Papers subidos | ≥ 2 antes del 8-nov | 0 |

**Deadlines externos — ✅ VERIFICADOS EN VIVO el 24-ago contra `arcprize.org/competitions/2026`, y el `6117` acertó:**

```
- March 25, 2026 - Competition starts
- June 30, 2026 - ARC-AGI-3 Milestone #1
- September 30, 2026 - ARC-AGI-3 Milestone #2
- November 2, 2026 - Submissions due
- November 8, 2026 - Papers due
- December 4, 2026 - Results announced
```

Premios: **Paper Prize $450K** (Top Paper $75K garantizado: 1º $50K, 2º $20K, 3º $5K; pozo de **$375K** para papers > 4,5 en la rúbrica) · **ARC-AGI-3 $850K** (Grand Prize $700K, Top Score $75K). **Ganar ARC no es el objetivo.**

**🔑 Y un dato que el `6117` NO tenía, y ahorra una semana entera:** son **TRES tracks** (ARC-AGI-3 interactivo, ARC-AGI-2 estático, y el paper track). Verbatim de `arcprize.org/competitions/2026/paper`: *«Paper submissions must be linked to a Kaggle code submission (**ARC-AGI-2 or ARC-AGI-3** track)… The code submission **need not achieve a high score**»*. **La S7 del plan asume construir el agente interactivo de ARC-AGI-3, que es la semana más caras, y puede no ser necesaria:** un notebook mínimo sobre ARC-AGI-2 cumple la elegibilidad. *Discrepancia menor: una página de Kaggle dice 9-nov; gana `arcprize.org`.*

**Las 10 semanas:** S1 cerrar lo público · S2 los nulls que faltan · S3 dos o tres motivos más · S4 mecanismo de aprendizaje · **S5 P1** · **S6 P2** · S7 agente ARC · S8 P4 · S9 revisión externa · S10 cerrar y subir. Cada actividad tiene **criterio de aborto** escrito.

**Los 5 papers:** **P1** auditoría de connectomíca dinámica (evidencia **completa**) · **P2** el 0,41% blindado (evidencia **completa**) · P3 biblioteca (**1 de 3-4 motivos**) · P4 ARC (depende de P1 y P2) · P5 Paper 2 como negativo. **P1 y P2 están en S5-S6 a propósito: si todo lo demás falla, esos dos salen igual.**

**El riesgo real no es técnico:** son cinco entregables en diez semanas de **una persona**. El orden **es** la protección.

---

## 1. Son TRES papers más un motor. No mezclarlos nunca más

| Nombre | Qué es | Estado |
|---|---|---|
| **PAPER 1** | *Signal Propagation Properties in the Drosophila melanogaster Connectome: Intermodal Isolation, Differential Motor Access, and Non-Trivial Temporal Amplification*, Mendieta 2026a. **7 páginas, leído completo el 24-ago** | Zenodo 20-mar-2026. **DOI placeholder `XXXXXXX` literal en el header** |
| **PAPER 2** | *Topological Retention and Selective Convergence* — FEP, Markov blanket, Script R | Borrador. Va como resultado **negativo** (P5) o no va |
| **PATENTE** provisional | Congelada antes del erratum. Doc `5717`: **la patente tiene razón, el FALSIFIED es un artefacto** | En pausa |
| **Motor** | SparseLTC / DualBrain, C99 + ESP32 | **El activo real.** Ver `CONTEXTO-motor.md` |

**El título real termina en «Non-Trivial Temporal Amplification»**, confirmado contra el PDF.

**El producto en tres capas:** (1) la **fuente de calibración** = el conectoma medido y sus priors · (2) el **motor** = de 15M aristas a **1.336 B de código medidos en ESP32** y 704 B de RAM todavía solo en x86 · (3) **la biblioteca = el activo**, hoy con **un** motivo. **No se vende como «derivado del cerebro de la mosca»: se venden microsegundos, miliwatts y BOM.**

---

## 2. Lo que dice el PDF publicado, leído verbatim (24-ago, 7 páginas)

- **§2.1:** `Density = 0.0074`. Y `E/I = 1.50`, 9.059.302 excitatorias (60,0%), 6.032.681 inhibitorias.
- **Abstract:** «E = 15,091,983 **synapses**» · «reciprocity (**36×** over density expectation)» · «**four** parameter-free neural models» · «7/10 sensory classes» · «τm ≈ 8.4 ms, **center** of the physiological range».
- **§2.1 dice «connections» para el mismo 15.091.983.** → la ambigüedad **existe** y es defecto de redacción, **pero NO es la causa del número**.
- **La tabla de RDI es la Table 8**, con columnas `Real | CP | Z_CP | MS | Z_MS`, **sin columna Ratio**. **La Table 7 es reciprocidad por circuito** (intra-motor 41,3% … optic→motor 0,0%). ⚠️ **El doc `6017` llamó «Tabla 7» a lo que es la Tabla 8:** su hallazgo se sostiene, el nombre estaba mal.
- **El 1.559× NO EXISTE en el PDF.** Leí las 7 páginas. Y la **Table 1 es la tabla de poblaciones**, sin un solo ratio.
- **§2.4 ya declara y deriva el guard de tautología del CP** («Net RDI at 1-hop is exactly invariant under CP null, sigma = 0»).
- **§2.5 y la Limitación 3 ya dicen TRES modelos compatibles.** El «four» queda **solo en el Abstract**.
- **§2.3:** *«For the density analysis, **10 canonical sensory classes** with N >= 10»*, y la **Tabla 5 muestra 9 filas**. Falta una y **no está establecido cuál**.
- **§7 Data Availability:** URL `github.com/Mendieta-Architect/drosophila-connectome-**propagation**`, licencia **AGPL v3**, resultados en Zenodo CC BY 4.0.
- **Tabla 4 suma 90.101** donde 85.821 + 4.281 = **90.102**.
- **§1.1 cita a Dorkenwald et al. [2024]** por el conectoma. **§1.2 cita a Betzel et al. [2026]** correctamente en el texto. **Y NO cita a Lin et al. en ninguna parte**, ver §2.bis.
- Nulls declarados: MS `N = 100` estático y `N = 5` temporal; CP `N = 10` estático y `N = 5` temporal. **Tasa de swap 100%**, que no es alcanzable con las restricciones declaradas (la medida es 98,5%).

---

## 2.bis 📚 LAS REFERENCIAS EXTERNAS, completas y verificadas

**Por qué esta sección existe:** hasta el 24-ago 21:00 este archivo decía **«Lin» a secas** en cinco lugares distintos, sin autor completo, sin año, sin revista y sin páginas. **Una referencia incompleta se completa mal en el turno siguiente**, y de ahí salió que un borrador atribuyera números de un paper al otro. Van completas, una sola vez, y se citan desde acá.

> **⚠� Corrección de un reclamo propio (resp 050 → 051).** La resp 050 afirmó que este contexto «cita a Lin con las páginas de Dorkenwald». **Falso: no citaba ninguna página.** El defecto era una referencia **incompleta**, no una **miscitada**. Es E-01 otra vez, ahora sobre un reclamo propio: verificar el sujeto exacto **antes** de afirmar que está mal, porque afirmar que está mal de una forma en que no está también es un error.

**Son DOS papers distintos, del mismo número de la misma revista, y es fácil confundirlos:**

| Referencia | Qué es | Páginas | De ahí sale |
|---|---|---|---|
| **Dorkenwald, S., Matsliah, A., et al. + FlyWire Consortium (2024).** *Neuronal wiring diagram of an adult brain.* Nature | **634:124–138** | el paper de **DATOS**: el conectoma, 139.255 neuronas revisadas | **12,6 sinapsis por conexión** · grado medio 20,5 |
| **Lin, A., Yang, R., et al. (2024).** *Network statistics of the whole-brain connectome of Drosophila.* Nature | **634:153–165** | el paper de **ANÁLISIS DE RED** | **densidad 0,000161** · **reciprocidad 0,138** · clustering 0,0477 · rich club |

**Verificado el 24-ago** contra `nature.com/articles/s41586-024-07968-y` y `link.springer.com` (*«Volume 634, pages 153–165 (2024)»*).

**Los parámetros con los que Lin mide, que hay que citar junto a sus números:** snapshot **v630** (no v783), **umbral de 5 sinapsis por conexión**, 127.978 neuronas, 2.613.129 conexiones.

**Otros números de Lin, medidos y útiles:** rich club de **30%** del conectoma con cutoff de grado 37 y probabilidad interna 0,000870 = **5,4×** la global · small-worldness **SΔ = 141** · SCC gigante 93,3% · WCC 98,8% · camino dirigido medio **4,42 saltos**, todos alcanzables en 13 · **77.607 de 127.978** neuronas participan de al menos una conexión recíproca · cuatro nulls: **ER, CFG (grado), NPC (neuropilos) y NND (distancia)**.

### 🔴 Lo que Lin le hace al framing del Paper 1, y NO se arregla con aritmética

**Lin compara reciprocidad y clustering contra CINCO conectomas** (esta mosca, *C. elegans* hermafrodita y macho, hindbrain de pez cebra larval, corteza visual de ratón) y concluye, verbatim:

> *«Despite differences in the sparsity of the different brain networks, **the values of reciprocity and clustering coefficient are comparable across all five datasets**.»*

Y agrega: *«the over-representation of reciprocal connections in brains is **well established**»*, con seis citas, **dos en Drosophila**.

**Consecuencia:** la reciprocidad de este conectoma es alta **contra controles randomizados** pero **normal contra otros sistemas nerviosos medidos**. El Paper 1 compara contra **azar** (sale enorme); Lin compara contra **otros cerebros** (sale del montón). **Las dos son correctas, pero la segunda es la que va a hacer un revisor.** El «massive reciprocity» y el 36× del abstract **no se arreglan corrigiendo el número: hay que bajar el claim.**

**Lo que SÍ queda propio: la Table 7, reciprocidad DESGLOSADA por tipo de circuito** (intra-motor 41,3% · intra-visual centrífugo 36,9% · intra-óptico 32,0% · intra-sensorial 30,7% · sensorial→central 24,2% · sensorial→descendente 8,7% · sensorial→motor 3,6% · óptico→motor 0,0%). **Lin da un número global; el Paper 1 da la distribución.**

### 🔴 El null CP tiene PRIOR ART: el NPC model de Lin

La §2.4 del Paper 1 presenta el community-preserving como aporte metodológico. Lin, verbatim:

> *«we constructed an extension of the CFG model in which we constrain the random network by **enforcing the measured connection probabilities between the 78 neuropils**… this NPC model implicitly contains mesoscale spatial information.»*

**Misma familia:** preservar grado **y** la matriz de bloques. Diferencia: granularidad (78 neuropilos anatómicos vs 10 super-clases funcionales). Lin tiene además el **NND** por distancia física, que el Paper 1 no tiene. **Hay que citarlo y angostar el claim de novedad.** A favor: que Nature use esa familia **valida que era el control correcto**. **NO MEDIDO: los dos nulls no se implementaron lado a lado para ver si dan ensembles equivalentes.**

### 🟢 Y una CONVERGENCIA INDEPENDIENTE, que es lo mejor de todo y no está en el paper

Lin, por **random walk espectral** (un método que no comparte nada con el nuestro):

> **attractors** (3% de neuronas, 61,2% de las visitas): *«often make connections in the **gnathal ganglia**… contains many connections to the **ventral nerve cord**»* → **la salida motora**.
>
> **repellers** (3%, 42,4%): *«include many with synapses in the **antennal lobes (AL) and medullae (ME)**, brain regions close to the **olfactory and visual** periphery»*.

Y el Paper 1, **por conteo de aristas contra nulls que preservan grado**, mide que **olfactory y visual son las más depletadas** en acceso motor, y que llegan al músculo mechano, gustatory y ascendentes.

**Dos métodos que no comparten nada llegando al mismo ruteo.** Va como *«consistente con la estructura de atractores y repulsores reportada independientemente por Lin et al. (2024)»*, **no** como «coincidimos con Nature». **Cuesta un párrafo y es lo más barato que hay para subir el paper de categoría.** **NO MEDIDO: la convergencia es cualitativa, coinciden las regiones, no un número; el solapamiento no está cuantificado.**

### El veredicto de relación: **SECUENCIALES**, ni paralelos ni opuestos

La última frase del abstract de Lin, verbatim: *«These data products… **should serve as a foundation for models and experiments exploring the relationship between neural activity and anatomical structure**.»* **Eso es exactamente lo que hace el Paper 1, y Lin no propaga nada:** su análisis es motifs, rich club, componentes, reciprocidad, clustering, small-worldness y un random walk. **Cero dinámica temporal, cero modelos neuronales.** El Paper 1 empieza donde el suyo termina.

---

## 3. VALIDADO

| Hallazgo | Número | Instrumento |
|---|---|---|
| Densidad real del grafo | **7,85197×10⁻⁴** · y la publicada, 0,0074, es un **overflow de `int32`** reproducido a 8 cifras | resp 043 |
| **Reciprocidad** | 26,60% · 4.014.518 aristas · **rank 1º de 41, 20,59× vs CP, 0/40** ← **lo publicable** · 47,27× vs MS. **Pero ver §2.bis: la MAGNITUD no es distintiva entre cerebros** | 40 nulls CP (`6057`) |
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
| **RDI dinámico** | **z = 197.** El resultado **más fuerte** del expediente, **y el único territorio que no se pisa con Lin** | doc `5977` |
| **La brecha con Lin, CERRADA** | con umbral ≥5 sinapsis: reciprocidad **13,98%** vs su 13,8% (1,30%) · sinapsis/conexión **12,647** vs 12,6 de Dorkenwald (0,37%) · densidad 1,405e-4 vs 1,61e-4 (12,7%, v783 vs v630) | resp 045 |
| Replicación cruzada JS/Python | 46,88× vs 47,27×; el 0,8% lo explica la convención de swaps | doc `5977` |
| **Priors medidos** | peso **lognormal(0,7034 , 0,8883)** · `inh_frac` de **0,068** a **0,513** · grado entrante CV 1,469 · fuerza CV 2,402 · **tabla de 95 pares de bloques** | doc `6057` |
| **C99 embebido en target** | **1.336 B de `.text` a `-Os`** en ESP32/ESP32-S3 | resp 039 |

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
| **«la magnitud de la reciprocidad es distintiva de este conectoma»** | **🔴 NO SOSTENIDA (resp 050).** Lin et al. la encuentra **comparable en CINCO conectomas**. Es alta contra controles, normal contra otros cerebros. **No se arregla con aritmética: hay que bajar el claim del abstract.** Ver §2.bis |
| **«el null CP es aporte propio»** (§2.4 del paper) | **🔴 PRIOR ART: el NPC model de Lin et al. 2024.** Misma familia, otra granularidad. Hay que citarlo. Ver §2.bis |
| **«1.652× con la densidad de Lin»** (doc `5117`) | **🔴 RETIRADO (resp 045).** **Comparación cruzada**: nuestra reciprocidad **SIN** umbral (0,266) sobre la densidad de Lin **CON** umbral (1,61e-4). Pareada da **995×**, y el publicable es **20,59× contra 40 nulls CP** |
| **«jerarquía de ruteo: 283,2× y listo»** | **NO TESTEABLE contra el null fuerte** (doc `6057`): `sd = 0,0` exacto y 40/40. Es **cantidad conservada** bajo CP porque el null baraja destinos dentro de bloques de super_class y el grupo MOTOR está definido por la misma super_class. **El 283,2× es contra grado.** Arreglo: null de **tripartición**, sin correr |
| **«el desfasaje de un paso explica la discrepancia a t=60»** (mío) | **REFUTADO por lectura del código** (doc `6017`): `res[t] = h.copy()` va **después** del update en los dos loops. La causa real eran **dos métricas con el mismo nombre** (3 vs 6 pares) |
| **«el erratum corrige un 1.559× que aparece 9 veces»** (borrador) | **🔴 RETIRADO (resp 046):** el 1.559 **no existe en el PDF**, y la «Table 1 con ratios» es acá **la tabla de poblaciones**. **Un erratum que corrige un claim que el paper no hizo es él mismo un error** |
| **«el contexto cita a Lin con las páginas de Dorkenwald»** (mío, resp 050) | **🔴 IMPRECISO (resp 051).** **No citaba ninguna página:** decía «Lin» a secas. El defecto era una referencia **incompleta**, no **miscitada**. E-01 sobre un reclamo propio |
| **«el erratum está listo / no está listo / no existe en git»** | **CERRADO: `docs/ERRATUM.md` existe en git, 9 ítems, cero placeholders.** Falta **subirlo a Zenodo**, y eso es de Abraham |
| «el Paper 1 evita la densidad contaminada» | falso: §2.1 dice `Density = 0.0074` y el Abstract dice 36× |
| «el guard de tautología es aporte propio» | §2.4 del paper ya lo declara y lo deriva |
| «0 clases enriquecidas / 7 depletadas» (el paper) | con la densidad correcta: **4 enriquecidas, 4 depletadas, 1 ≈esperada** |
| «**4 de 9 clases pasan a enriquecidas**», retirado por el `5177` | **🔄 EL RETIRO SE REVIERTE (resp 043).** El `5177` usó el **85.821 de la Tabla 4, que es una SUMA DE PESOS**, como conteo de aristas; el real es **23.010**, y con ése `23010/1859 = 12,378` y `23010/17520 = 1,313 ≈ 1,3` publicado. **La expectativa SÍ es de densidad y el «4 y 4» es correcto** |
| «reciprocidad 36×» | **es el MISMO overflow**: `0,266/0,00739526 = 35,97`. Una línea de código, dos números publicados |
| «τ_m = 8,4 ms, centro del rango» | **dos defectos distintos:** el centro de 5-20 es **12,5** (y 3,3 está **debajo** del rango), **y** la derivación correcta es `-1/ln(1-τ) = 7,89`, error 6,47% |
| «R = 1,31, retención selectiva» | cruza 1 en las tres modalidades según normalización (visual 1,878 → 0,811) |
| col-norm «respeta la varianza local» | lleva el CV de 2,402 a **cero**; la global lo preserva entero |
| **Tabla 8 reproducible** (la que el `6017` llamaba Tabla 7) | **4 particiones con la definición EXACTA del código y ninguna reproduce la FORMA.** Y los 6 valores **no existen en ninguno de los 40 notebooks**: falta el instrumento |
| «hace falta una SNN para latencias» | la métrica al 10% del pico da mechano 4 < gust 5 < visual 6 < olf 10 |
| «el control lineal descarta saturación» | clipea: `max h = 2,0000` exacto en 2 de 3 modalidades |
| «la topología explica la función» | el escape compilado da selectividad temporal 1,04× |
| «la entropía baja distingue biología» | los nulls bajan más: dH −9,79 vs −2,88. Doc `5777`: **la FORMA sí, 7/12** |
| «visual es la vía con menos acceso motor» | **no sobrevive**: es **olfactory** (doc `5937`) |
| «sinapsis vs conexiones» explica el bug de densidad | **existe como defecto de redacción pero NO es la causa**: la causa es el overflow. Sinapsis reales: 54.492.922, media **3,61** por conexión sin umbral y **12,647** con umbral ≥5 |
| «Therianos me refuta» | **retirado:** Lin mide 13,8% en el adulto y Therianos usa conectoma **larval** (doc `5117`) |
| «el `temporal RDI` es frágil» (mío) | **error de eje** (doc `5977`). **El eje no es estático vs dinámico: es CONTRA QUÉ NULL** |
| «KC→MBON cae contra CP» (predicción mía) | **refutada: sobrevive con 7,81×, 0/40** |

---

## 5. NO MEDIDO / pendiente, declarado

1. **La décima clase de la Tabla 5.** §2.3 declara 10, la tabla muestra 9. **Cuál falta: no establecido.**
2. **La fila AN no es reproducible.** `N=495` no sale de ningún filtro consistente con las otras ocho (`cell_class == 'AN'` da 2.231, ratio 1,894× y no 0,6×). Declarada así en el erratum, **no corregida**.
3. **Si los `p` de la Tabla 5 usan `p_edge_exc`** u otra probabilidad.
4. **El script de la Tabla 8: no está en el corpus.** Cero de 6 valores en 40 notebooks.
5. **Null de tripartición: no corrió.** Sin él la jerarquía de ruteo no se publica contra modularidad.
6. **Faltan 21 nulls** para que el test global de los 12 pares llegue a `p<0,05`. ~30 min (doc `5957`).
7. **Verificaciones externas pendientes:** los dos **DOI** contra Zenodo, y **Betzel** (PLOS Complex Systems 3(3), e0000091) contra el artículo. **Lin ya está verificado** (§2.bis). ✅ Las fechas de ARC también.
8. **De Lin leí hasta la sección de reciprocidad**, no su Discussion ni sus Methods. **La Table 2 (los cinco conectomas) la conozco por la descripción del texto, no fila por fila.** Y **no leí Dorkenwald et al.**
9. **Si Lin reporta reciprocidad por tipo de circuito** en su suplementario: **si lo hiciera, se cae el único pedazo de reciprocidad que queda propio.**
10. **NPC vs CP no se compararon midiendo.** «Misma familia» sale de su descripción, no de implementar los dos.
11. **Los tres notebooks con overflow se declaran descendientes** de un «pipeline original» que **no está en el corpus**. Que sean los que produjeron el paper está **apoyado** por reproducir 8 de 9 ratios, **no establecido**.
12. **Un solo patrón de overflow barrido** (`N*(N-1)`). No barrí `N**2` ni otros productos de enteros grandes.
13. **El barrido de Docs está al 71%:** 46 de ~65. **9 IDs pendientes** (`6157 6177 6197 6217 6237 6257 6277 6317 6337`), ~15 en icca-engine, ~50 entre `3637` y `4717`, MUDH/AURA sin tocar.
14. **Los dos `.mjs` del release no corren en un clon ajeno:** leen `/workspace/...` con ruta absoluta. **Declarado en el README y en METHODS, no parcheado.** Mi test de «clon limpio» dio un **falso verde** (resp 047).
15. **Los dos JSON grandes van por md5**, no commiteados: `nulls40.json` (191.443 B, `38bf1fcadaf37a3b125f83d22b6f4d8e`) y `dualbrain_bench.json` (31.527 B, `1025d60b4e9521d7e4a21ed282935049`).
16. **Los 6 `.py` de deuda siguen fuera de git.** Manifiesto en `MANIFIESTO-KAGGLE.md`.
17. **El C99 embebido está medido a medias:** 1.336 B de `.text` en target, pero **no hay `.elf`, no hay RAM en target** y no corrió en hardware.
18. **No corrí el review automático** sobre los archivos nuevos del repo. **K-02: deuda declarada.**

---

## 6. Decisiones esperando a Abraham

1. **🔴 SUBIR LA v2 A ZENODO antes del 30-ago.** El texto está en **`docs/ERRATUM.md`**, 9 ítems, cero placeholders. **Falta solo tu acción.**
2. **Re-verificar los dos DOI contra Zenodo** antes de pegarlos.
3. **🔴 SUBIÓ DE PRIORIDAD con el peritaje de Lin (resp 050): el `README.md` público clasifica los resultados dinámicos como «negative methodological result»**, y **lo dinámico es el único territorio que no se pisa con Nature**. Si el único territorio propio está archivado como negativo, el paper se queda sin nada que reclamar. **Le puse un bloque «Pending revision» que pide no citarlo como veredicto; reclasificarlo es tu decisión.**
4. **Bajar el 36× y el «massive reciprocity» del abstract**, y subir en su lugar la **Table 7** (reciprocidad por circuito), que sí es propia. Ver §2.bis.
5. **Citar a Lin et al. y el NPC model como prior art** en la v2. Ya está escrito en el erratum §8 y en Outstanding verification 7.
6. **Agregar el párrafo de convergencia** attractor/repeller. Cuesta un párrafo y es lo más barato del plan.
7. **¿Adoptar el umbral de 5 sinapsis** como criterio declarado, o declarar por qué no?
8. **⭐ Los bugs del Script R viven DENTRO del verificador V-K** (doc `5637`), que además **comparte el overflow** (resp 044). **Es el ítem 9 del erratum.** Parchear antes de publicar, o publicar declarando la limitación.
9. **Buscar el script de la Tabla 8.** Si aparece, se corre en una hora.
10. **¿ARC-AGI-2 en vez de ARC-AGI-3** para la elegibilidad del paper? Ahorra la S7 entera. Ver §0.
11. **Mergear el PR #1**, o decir qué le falta. Review automático sin hallazgos = **NO MEDIDO, no aprobación**.
12. **¿Arreglo las rutas absolutas de los dos `.mjs`?** Es tocar código que produjo figuras publicadas.
13. **El barrido de Docs: ¿sigo con los 9 IDs del conectoma o abro las otras zonas?**
14. **Subir los 6 `.py` de deuda y los dos JSON grandes.**
15. Org `Mendieta-Architect` o aceptar la URL `gatehot59-star` en el erratum.

---

## 7. Estado de git y del entorno, medido

**Ya en el repo:** `docs/ERRATUM.md` (**9 ítems**) · `README.md` · `LICENSE` · `docs/METHODS.md` · `src/` con 8 archivos · `results/` con 5 logs · `docs/agents/` con los cuatro contextos, el índice, el manifiesto de Kaggle, la evidencia y 50 respuestas.

**Verificado por md5 desde los dos lados (resp 045):** cuatro archivos de `src/` son **byte-idénticos** al código que corrió en Kaggle (`motor.py`, `cp40.py`, `nulls40_kaggle.py`, `hm_sweep.py`). **Esos resultados son recomputables por un tercero desde git.**

**Entorno:** el container **no es efímero** (uptime 3,2 días medido), `git` no está instalado y todo pasa por la integración de GitHub, `nexus.db` **no existe**. Python 3.12.14, Node 24.18.0, R 4.5.3. **Los Docs son ENUMERABLES:** IDs de página secuenciales **paso 20**, prefijo `2kza6fw5-`. Límite medido: **5 Docs completos no entran en una ventana**. **El resto se re-mide, no se recuerda:** `CONTEXTO-ENTORNO.md` §13.

---

## 8. Modos de falla propios de esta línea, y cada uno ya costó

**1 · Una lista hecha de lo que está a mano solo contiene lo que está a mano.** Dos veces: el `INDICE-DE-ENLACES.md` cosechado del chat (30 de los citados, no 30 de 30), y el corpus de Kaggle (**29 archivos locales contra 40 kernels reales**, lo que invalidó el denominador de un barrido declarado cerrado). **El denominador se mide en la fuente, no en la copia.**

**2 · Un null cuyos invariantes incluyen la cantidad medida no es un control, es un espejo.** **Si `sd(null) == 0`, reportar NO TESTEABLE**, no `1,000×`. Cuatro líneas, 22,2 minutos de cuota.

**3 · Una explicación que encaja no es una explicación medida.** El «desfasaje» se escribió en un documento destinado a un DOI **sin leer el código que explicaba**. Y la **causa** del overflow apareció solo al **ejecutar**: `numpy` emitió el warning, ninguna relectura lo iba a producir.

**4 · Un archivo que no abrí en este turno no recibe veredicto de vigencia.** «Sigue vigente» es una medición, no un default.

**5 · Comparar dos cantidades medidas con criterios distintos. CUATRO veces.** El `5177` (suma de pesos como conteo de aristas), el `5117` (reciprocidad sin umbral contra densidad con umbral), el borrador del erratum (un valor de otro documento), y el `1,18× sobre LSTM` contra el `4× en contra` del motor (dos puntos de la misma curva). **Antes de dividir o contrastar dos números, verificar que midan lo mismo.**

**6 · Un test que no puede dar rojo no es un test. TRES en un día.** El `$?` del shell reportando `exit=0` sobre una compilación fallida, un `grep -c` con falso cero por la coma de miles, y un «clon limpio» que corrió leyendo una ruta absoluta.

**7 · Lo que no está commiteado se pierde justo cuando más falta hace.** El entregable del 30-ago vivía en un solo directorio sin versionar y cuatro documentos lo daban por subido. **Hoy está en git.**

**8 · Un erratum aritmético no arregla un problema de framing.** Los tres números que se solapaban con Nature ya estaban corregidos cuando apareció el hallazgo más grave: **no es que el número estuviera mal, es que el número no era notable.** Eso solo se ve **comparando contra el estado del arte**, no contra un null. **Antes de poner un número en un abstract, buscar quién midió lo mismo en otro sistema.**

**9 · Una referencia incompleta se completa mal en el turno siguiente.** Este archivo decía «Lin» a secas en cinco lugares, y de ahí salió que un borrador atribuyera sus números al otro paper del mismo número de la misma revista. **Una cita se escribe completa la primera vez, o se convierte en una fuente de error propia.** Y el corolario, que también costó: **antes de afirmar que una cita está mal, verificar EN QUÉ está mal** (resp 050 → 051).
