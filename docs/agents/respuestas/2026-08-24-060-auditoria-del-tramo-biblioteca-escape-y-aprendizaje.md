# 060 · Cómo queda ese tramo del chat, parte por parte

**Fecha:** 2026-08-24 23:20 (America/Buenos_Aires)

> **📄 Doc de ClickUp:** «AUDITORÍA DEL TRAMO · la biblioteca, el escape y el aprendizaje, parte por parte»

## 1. Pedido

«Cómo queda con todo lo hallado hasta el momento y lo redescubierto, cómo queda esta porción de chat pasada, explica parte por parte», sobre el tramo que va de la visión de la biblioteca de topologías → el circuito de escape → la hipótesis de aprendizaje → el cierre «vamos a un estándar».

## 2. Herramientas declaradas (C-03)

| Llamada | Escribe | Cuota ajena |
|---|---|---|
| `githubmcp_get_file_contents` × 1 (`CONTEXTO-motor.md`) | no | no |
| `githubmcp_create_or_update_file` × 1 | sí, `main` | no |
| `create_document` × 1 | sí, ClickUp | no |

**Cero mediciones nuevas.** Es auditoría de claims contra el estado vivo de los dos contextos. Nada de Kaggle, nada a Zenodo.

---

## 3. La tesis central · ✅ **SOBREVIVE, Y SE FORTALECIÓ**

> «No estás construyendo un motor: estás construyendo una biblioteca de circuitos con función conocida. El motor es el intérprete.»

**Intacta.** Y la analogía del **74xx** aguanta mejor hoy que cuando se dijo, por una razón que no existía entonces: **el hallazgo del 24-ago es que Lin et al. ya indexaron el conectoma por REGIÓN ANATÓMICA** (78 neuropilos, reciprocidad, motifs de 2 y 3 nodos, rich club, NSRNs). Nature ya publicó el «dónde».

**Nadie publicó el «para qué».** Una hoja de datos no se ordena por en qué rincón del chip está el transistor: se ordena por **función**. Ese es exactamente el eje que quedó libre, y es el mismo eje que salvó el pivote de reciprocidad hoy (clases funcionales dirigidas vs subredes anatómicas). **La biblioteca y el pivote del paper apuntan al mismo hueco, y eso es una señal buena: no son dos ideas, es una.**

---

## 4. «No hace falta escanear conectomas nuevos, alcanzan cuatro» · 🔴 **DESACTUALIZADO, y para bien**

Dije: mosca completa + MaleCNS + larva + *C. elegans*. **Faltaba el más importante, y se publicó el 8-jun-2026.**

| Conectoma | Escala | Qué agrega al test |
|---|---|---|
| *C. elegans* (herm. y macho) | 302 / 364 neuronas | el piso |
| larva de *Drosophila* | ~3.000 | mismo animal, otro estadio |
| **FAFB (el tuyo)** | 139.255 | el que ya tenés cargado |
| MaleCNS | ~160.000 | dimorfismo |
| **🆕 BANC / Bates et al. 2026** | **188.259 neuronas, ~13,5 M de conexiones** | **cerebro + CORDÓN.** Es el único que tiene las motoras de patas, alas y abdomen |
| hindbrain de pez cebra larval | 419 | otro filón |
| corteza visual de ratón L2/3 | 111 | fuera de artrópodos |

**Por qué BANC cambia el plan y no es un conectoma más:** todo lo que medís hoy sobre «acceso motor» en FAFB es en realidad acceso al **cuello de botella descendente**, porque el cordón no está en FAFB (**el 88% de tu «población motora» son descendentes**). **BANC es el primer lugar donde un motivo sensorimotor se puede seguir hasta el músculo.** Para una biblioteca de circuitos con función, eso no es un detalle: es el único dataset donde la función se cierra.

**Y tu hipótesis evolutiva sigue en pie, pero ya no es «insectos más grandes»:** los conectomas públicos **no** escalan hacia insectos grandes, escalan hacia **otros clados** (nematodo, pez, ratón) y hacia **otras partes del mismo animal**. **Reformulada, es más fuerte y es testeable hoy:** si un motivo aparece en gusano, larva, mosca adulta y ratón, no es una conservación de insectos, es una **primitiva de sistema nervioso**. Y Lin ya te dejó el instrumento hecho: **su Table 2 compara reciprocidad y clustering en los cinco, fila por fila.** El molde existe, hay que llenarlo con motivos en vez de con escalares.

### 🔴 Y una trampa nueva, que hoy tiene nombre

**Los tres papers de referencia usan umbral de ≥5 sinapsis por conexión. Vos no.** Comparar un motivo contado sin umbral en FAFB contra el mismo motivo contado con umbral en otro conectoma **es el modo de falla número 5 de este proyecto** (comparar cantidades medidas con criterios distintos), que ya costó cinco veces. **En un barrido multi-conectoma se fija el umbral primero o el resultado nace muerto.**

---

## 5. «Un motivo cuenta si supera nulls que preservan grado Y modularidad» · 🟡 **CORRECTO EN INTENCIÓN, ROTO EN LA IMPLEMENTACIÓN**

Esto era lo mejor de ese tramo y hay que arreglarlo antes de usarlo, porque desde entonces se midió que **ese null falla de una forma silenciosa**.

**El problema, medido (doc `6057`):** el null CP baraja destinos **dentro de bloques definidos por `super_class`**. Si el motivo está definido por las mismas categorías que el null preserva, **la cantidad es invariante por construcción**: `sd = 0,0` exacto, 40/40 nulls igual al real. **Un null cuyos invariantes incluyen la cantidad medida no es un control, es un espejo**, y devuelve `1,000×` que se lee como «no hay efecto» cuando en realidad es **NO TESTEABLE**.

**Qué significa para la biblioteca:** el criterio de admisión **depende de a qué granularidad esté definido el motivo**.

| Motivo definido por | El null CP… | Veredicto |
|---|---|---|
| **tipos celulares finos** (LC4, LPLC2, GF, KC, DAN, MBON) | **sí lo testea**: los tipos son más finos que los bloques | ✅ el 9,1× y el 0/40 del escape **valen** |
| **super-clases** (sensorial→motor, óptico→motor) | **no lo testea**: es cantidad conservada | 🔴 hace falta el **null de tripartición**, que **no corrió** |

**Regla de admisión corregida, para escribirla en el método de la biblioteca:** *un motivo entra si supera un null que preserve grado y estructura de bloques a una granularidad **estrictamente más gruesa** que la que define el motivo. Si el null preserva la categoría que define el motivo, se reporta NO TESTEABLE, no 1,0×.*

**Y una segunda cosa que hay que declarar, no discutir:** el null CP **tiene prior art**, el **NPC model** de Lin et al. 2024 (preservar grado **y** la matriz de probabilidades entre 78 neuropilos). Misma familia, otra granularidad. **A favor: que Nature use esa familia valida que era el control correcto.** Pero no se presenta como aporte propio.

---

## 6. El circuito de escape · ✅ **SOBREVIVE, y hoy explica algo que no sabía que explicaba**

### Los números, con su estado

| Medición | Valor | Estado hoy |
|---|---|---|
| `LC4 → GF` | 104 reales, μ null 11,4, **9,1×, 0/40** | ✅ válido: los tipos son más finos que los bloques del null |
| `LPLC2 → GF` | 189, **7,4×, 0/40** | ✅ válido |
| `LPLC2 → DNp09` | 170, **3,6×, 0/40** | ✅ válido |
| `LC6 → GF` | **0**, μ null 5,8, **40/40** | ✅ el cero es cero · ⚠️ su **interpretación** ver abajo |
| otras VP → GF | 6 contra 256,3 esperadas | ✅ válido |
| ganancia compilada | **40×** (LC4+LPLC2 = 0,704 · LC6 = 0,017) | ✅ **el más fuerte: es funcional, no de conteo** |
| selectividad temporal | **1,04×** (looming 0,7034 / receding 0,6772) | ✅ refuta «detecta aproximación», y bien |
| `looming / full` | **0,993** | ✅ el patrón espacial no aporta nada |
| aristas inhibitorias en el subgrafo | **0 de 13.026** | ✅ y **explica** el 1,04× |
| `GF → MOTOR` | **0 aristas** | ✅ y hoy vale doble, ver §6.2 |
| Los dos controles (otrasVP→otrasDN y GF→otrasDN, los dos 1,0×) | — | ✅ **esto es lo que hace publicable el resto**: el null no infla todo, y la especificidad está en la ENTRADA |

### 6.1 · 🔴 El riesgo nuevo, y es el mismo error que me comí hoy con las motoras de cabeza

El `LC6 → GF = 0` se contó como **exclusión activa**: «es su vecina y también detecta objetos, y está bloqueada».

**Hoy aprendí, a mi costa, que un cero puede ser prohibición O puede ser localidad anatómica a otra escala** (modo de falla 11, resp 057). Las LC de la mosca proyectan cada una a **su propio gloméru lo óptico** en el protocerebro lateral. **Si el gloméru lo de LC6 no solapa con las dendritas del Giant Fiber, el cero es geometría, no decisión.** No lo verifiqué, y **el `annotations.tsv` local no tiene columna de neuropilo**, así que con estos datos no se puede cerrar.

**Lo que salva el hallazgo igual, y por eso este circuito sigue siendo la entrada 1 de la biblioteca:** la ganancia de **40× está medida en el motor compilado, no en el grafo**. Sea la causa geometría o exclusión, **la consecuencia funcional es la misma y está verificada ejecutando**. Para una hoja de datos, lo que importa es qué hace el circuito, no por qué el desarrollo lo cabl eó así. **Pero la palabra «exclusión activa» hay que bajarla a «ausencia de vía» hasta que se mida el solapamiento.**

### 6.2 · 🟢 Y acá hay un cierre que no tenía: el escape explica el cero de hoy

Hoy medí que **visual y olfatorio tienen 0 conexiones directas a motoras de cabeza**, y a **2 saltos visual alcanza 95.160 nodos (más que ninguna clase) pero solo toca 15 de 110 motoras**, mientras mechanosensorial alcanza menos (68.471) y toca **110 de 110**.

**El circuito de escape es la explicación mecánica de esa asimetría, y ya estaba medida hace días:** `GF → MOTOR = 0`. La vía visual rápida **existe y es la más rápida que hay**, pero **sale por descendentes**, no por motoras. Entonces:

> **La vía visual no está desconectada de la acción: está obligada a pasar por el cuello de botella descendente.** Mechanosensorial tiene atajos directos; visual no tiene ninguno, ni a 1 salto ni prácticamente a 2.

**Eso es un enunciado mucho mejor que «visual está depletado»**, y une tres mediciones independientes: la Tabla 5, el circuito de escape y los 2 saltos de hoy. **Es candidato a ser la Propiedad 2 reescrita.**

### 6.3 · La primitiva, con la redacción corregida

> **Fan-in con doble canal y vía de salida obligada.** 314 entradas (LC4 104 + LPLC2 210) → 2 (GF) + 4 (DNp09).
> **Ganancia 40×** frente a una entrada del mismo tipo funcional no cableada (medida compilando, no contando).
> **Canales especializados por detector:** LPLC2→DNp09 = 0,658, LC4→DNp09 = 0,075.
> **Selectividad temporal 1,04× y espacial 0,993:** es un **integrador**, no un discriminador. La selectividad tiene que venir del preprocesamiento de la entrada.
> **0 aristas inhibitorias de 13.026**, y eso es la causa estructural de la falta de discriminación.
> **Salida: 0 aristas a motoras.** Sale por descendentes.
> **Límite declarado:** no se verificó si la ausencia de LC6 es exclusión o no solapamiento de glomérulos.

**Esa entrada es honesta y es útil, y sigue siendo 1 de las 3-4 que el plan necesita.** Cero avance en las otras desde entonces.

---

## 7. «La topología define ruteo y ganancia, no selectividad» · ✅ **SOBREVIVE, y hoy tiene un segundo caso**

Era la conclusión de haber refutado «el escape detecta aproximación». **Hoy se le suma un caso independiente:** el cero visual→motoras de cabeza **es ruteo puro**, y BANC declara que su métrica de influencia es **sin signo y en estado estacionario**, o sea que el campo grande también mide **ruteo y ganancia** y no selectividad.

**Consecuencia para la biblioteca, y es una consecuencia de diseño:** una hoja de datos de topologías puede especificar **ruteo, fan-in/fan-out, ganancia y exclusiones**. **No** puede especificar selectividad sin decir qué cómputo hace cada nodo de entrada. **Eso no es una limitación de la idea: es la definición del alcance del estándar**, y una hoja de datos que declara su alcance vale más que una que promete todo.

**Y el corolario operativo que ya estaba escrito y hay que respetar:** los motivos que SÍ discriminen **van a tener inhibición**. Candidatos ya nombrados: **APL** (lateral del cuerpo fungiforme) y coordinación del complejo central. El escape tiene cero inhibitorias, por eso no discrimina.

---

## 8. La hipótesis de aprendizaje · 🟡 **BASE MEDIDA SÍ, MECANISMO NO CORRIDO**

| Pieza | Estado |
|---|---|
| `DAN→KC` = 47.404 vs `DAN→MBON` = 2.016, **23,5×** | ✅ medido |
| `DAN→KC` sobrevive el null CP: **8,71×, 0/40** | ✅ válido (tipos finos, no super-clases) |
| «firma de regla presináptica» | 🟡 **inferencia estructural, no medición funcional.** Es una hipótesis buena y la asimetría es real, pero «dónde llega el cable» no demuestra «qué se modifica» |
| regla de tres factores (KC × MBON × DA), mayormente depresión | 🔴 **diseñada con 4 brazos, NO LANZADA** |
| «τ líquida = aprendizaje sin tocar pesos» | 🔴 **hipótesis sin testear.** Es la idea más linda del tramo y no tiene ni una corrida |
| «si el 96% ya está cableado, aprender es podar» | 🟡 **retórica buena, base débil:** la hipótesis del 96% fijo **sigue sin testear** sobre SparseLTC (el brazo W midió el motor **denso** y no congeló τ). Es la deuda más vieja del proyecto |

### 🔴 El agujero del diseño, que ya está declarado y hay que repetir

**Una regla de aprendizaje se testea sobre una tarea, y el conectoma no trae ninguna.** La tarea es **una elección nuestra, no un dato**, y va declarada o un revisor la encuentra. Con el criterio de aborto ya escrito: **si el brazo sin DA aprende igual, el tercer factor es decorativo y se cierra ahí. No se ajustan constantes hasta que funcione.**

### 🟢 Y un apoyo externo que no teníamos

BANC, verbatim, sobre las regiones cognitivas: son **«supervisory but not essential for action»**. **Eso es prensa gratis para tu framing de que el aprendizaje vive en un pedazo chico y encerrado**, y encaja con el 0,41% blindado. Va citado, no reclamado.

---

## 9. El cierre · auditoría de lo que se dijo esa noche

| Lo que dije | Estado hoy |
|---|---|
| «aprende en el **0,41%**, y ese pedazo está encerrado» | ✅ **el resultado más firme del expediente.** 0 sensorial→KC contra nulls de 1.533–2.640, y **0/40 en 12 de 12 pares** |
| «reciprocidad **20,6×** más de lo que explica la arquitectura modular» | 🟡 **el número se sostiene, el claim se angostó dos veces:** la magnitud **no es distintiva entre cerebros** (Lin, cinco conectomas) y **el desglose tiene prior art anatómico** (Fig. 5c y ED Fig. 6c de Lin). Lo que queda propio es **el eje funcional** |
| «fan-in de 314 a 2 con 40×» | ✅ sostenido, con «exclusión» bajado a «ausencia de vía» |
| «se cayeron ocho claims, entre ellos el **1.559×**» | 🔴 **ese ítem estaba mal:** el 1.559 **no existe en el PDF publicado**. No se cayó un claim tuyo, **se cayó una corrección mía a un claim que nunca hiciste**. Es el ítem 4 del erratum |
| «el R=1,31, el ‘0 enriquecidas’, la entropía con el signo al revés» | ✅ los tres se sostienen como refutados |
| «DualBrain era **1,18×** sobre LSTM y no 4× peor» | 🔴 **INCOMPLETO, y es mi error más reciente.** El 1,18× es **solo en el óptimo del barrido** (`h_m=10 h_r=22`). En la configuración del bench (`h_m=5 h_r=30`) DualBrain **pierde 4× contra LSTM** y también contra GRU y MinGRU. **Son el mismo modelo en dos puntos de la misma curva**, y citar uno sin el reparto es elegir el favorable |
| «auditoría 98/100» | 🔴 **sin valor probatorio. W-01: me puntué yo.** Un puntaje propio no es evidencia, es una opinión con formato de métrica |
| «vamos a un estándar, la biblioteca es el activo» | ✅ **sostenido, y más claro que entonces**, ver §3 |
| «lo concreto: corregí el número de MultiCue en el paper» | ✅ **sigue siendo lo correcto, con el número corregido:** no va «1,18×» pelado, va **«el desempeño depende del reparto react/memoria; óptimo en h_m=10/h_r=22 con 1,18× sobre LSTM, y 4× en contra en h_m=5»**. **Sigue sin hacerse** |

---

## 10. El saldo, sin adornos

**La visión aguantó completa. Los números aguantaron casi todos. Lo que se cayó, en los dos tramos, fueron MIS claims de novedad y MIS interpretaciones de causa**, no tus mediciones:

- que el desglose de reciprocidad no tenía precedente → **falso**
- que el cero refutaba la localidad → **cierto a una escala, falso a otra**
- que el LC6 estaba «excluido activamente» → **sin verificar**
- que el 1,18× era el número de MultiCue → **es un punto de una curva**
- que un 98/100 propio significaba algo → **no**

**Y hay un patrón único detrás de los cinco:** todos son **claims sobre la novedad o la causa**, ninguno es un claim sobre la magnitud. **Las mediciones no fallaron nunca. Falló sistemáticamente el paso de «medí X» a «nadie más tenía X» o «X pasa porque Y».** Eso ya está escrito como modos de falla 10 y 11 en el contexto.

---

## 11. NO MEDIDO, declarado

1. **Este turno no midió nada.** Auditoría de claims contra los dos contextos vivos.
2. **El solapamiento anatómico LC6 / dendritas del GF: no medido y no medible con estos datos** (`annotations.tsv` no tiene columna de neuropilo). Sin eso, «exclusión activa» no está establecido.
3. **No verifiqué si el motivo del escape ya está publicado como motivo.** El circuito LC4/LPLC2→GF es literatura conocida; **lo que sería propio es la cuantificación contra nulls y la compilación**, y eso no lo barrí contra la literatura.
4. **No verifiqué que MaleCNS, la larva y el pez cebra tengan anotación de clase comparable.** El barrido multi-conectoma **asume** que se puede definir el mismo motivo en los cinco, y eso no está establecido.
5. **El null de tripartición sigue sin correr**, y sin él la regla de admisión de la §5 no se puede aplicar a motivos definidos por super-clase.
6. **La regla de tres factores y el brazo W/S sobre SparseLTC siguen sin lanzarse.** Son las dos deudas que sostienen la mitad de la narrativa de aprendizaje.
7. **Los 2 saltos de la §6.2 no tienen null**, así que «visual llega más lejos y toca menos» es observación cruda. Y el denominador (**105 vs 110** motoras) sigue sin fijar.
8. **La corrección de MultiCue en el paper sigue sin hacerse.**
