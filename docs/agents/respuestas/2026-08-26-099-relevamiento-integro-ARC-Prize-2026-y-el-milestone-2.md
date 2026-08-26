# 099 · Relevamiento íntegro de ARC Prize 2026: los 7 no-medidos, y 37.500 USD en 35 días

**Fecha:** 2026-08-26 00:45 (America/Buenos_Aires) · **Modo:** TITAN FULL

**Instrumento:** `build.run` sobre `brain-env`. Se escribió `fetch.py`, que baja y limpia las **cuatro páginas oficiales completas**. Hizo falta porque la búsqueda web devolvía el highlight **cortado justo en "with a score from"**, que es exactamente donde empezaba la rúbrica.

<hr/>

## 0. Primero lo del container: SÍ, hay algo corriendo, y es mío

```plain
loadavg: 1.65 1.86 1.92   (2 nucleos)

9604 | python3 motor_v2.py --data-dir /workspace --out-dir /workspace/motor_v2_real --nulls 39 --steps 150
9605 | tee /workspace/motor_v2_real.log
5644 | adb -L tcp:5037 fork-server server
   1 | sleep infinity

estado: CP 25/39   t=16245.3s   (4 h 31 min)
faltan: 14 nulls x ~465 s = ~1,8 h
json final: NO EXISTE todavia
```

**Es la corrida del conectoma que lancé yo, con tu permiso previo.** Un solo proceso de cómputo, un núcleo saturado, consistente con el load de 1,65 sobre 2 núcleos. **No hay ningún proceso huérfano nuevo.**

**Decisión tuya:** faltan ~1,8 h para que cierre solo. La mato o la dejo.

<hr/>

## 1. 🔥 EL HALLAZGO: el Milestone #2 SÍ tiene premio, y son 37.500 USD en 35 días

**Era el ítem 3 de los no medidos, y es el más caro de todos los que faltaban.** Verbatim de `arcprize.org/competitions/2026/arc-agi-3`:

```plain
Milestone Prizes - $75K (guaranteed)

  Participants who open source their solutions by the milestone deadlines
  are eligible for milestone prize money.

  Milestone #1 (June 30, 2026):      1st: $25K, 2nd: $10K, 3rd: $2.5K
  Milestone #2 (September 30, 2026): 1st: $25K, 2nd: $10K, 3rd: $2.5K
```

> **37.500 USD garantizados, con fecha 30 de septiembre, o sea 35 días.** Y el requisito explícito es **open-sourcear la solución por la deadline**, que es exactamente cómo trabaja este expediente por método.

**Es la fecha más cercana con dinero garantizado de todo el calendario**, y estaba figurando en mis documentos como "Milestone #2, 36 días" **sin premio asociado**, porque no lo había leído.

<hr/>

## 2. Ítem 1 CERRADO · la rúbrica del Paper Prize, completa y verbatim

```plain
Papers are evaluated equally based on the following rubric, with a score
from 0 (lowest) to 5 (highest) in each category.

  Accuracy      How accurate is the submission based on its performance
                on the leaderboard?
  Universality  How general and universal is the approach beyond the
                competition? Does your method generalize to other similar
                problems?
  Progress      How much does the paper increase the overall chance of
                anyone achieving 85% on ARC-AGI?
  Theory        How well does the paper describe WHY the approach works
                (as opposed to merely describing HOW it works)?
  Completeness  How thoroughly and completely does the paper cover the
                submission to the leaderboard?
  Novelty       How novel is the approach relative to existing public
                research?

Each paper must include a corresponding Kaggle submission confirming it
describes a real, working entry. THE SUBMISSION'S SCORE WILL BE USED IN
THE RUBRIC'S "ACCURACY" CATEGORY.

Paper rubric evaluations will not be shared.
In the event of a tie, the paper entered first will be the winner.
```

### 🔴 Y acá la fuente oficial CONTRADICE mi lectura del turno anterior

Yo dije: *"el agente random subido ya habilita el Paper Prize de 450K"*. **Es cierto para la ELEGIBILIDAD y falso para el PREMIO.**

**El score es 1 de 6 categorías, y las seis pesan igual.** Aritmética directa: con `Accuracy = 0` y **perfecto en las otras cinco**, el promedio máximo es **25/6 = 4,17**. Y el pool de 375K paga **arriba de 4,5**.

> **Con un agente random, el pool de 375.000 USD es matemáticamente inalcanzable.** El Top Paper de 75K sigue siendo posible porque es relativo ("highest-scoring"), pero el pool no. **Mi afirmación anterior estaba incompleta y se corrige acá.**

### 🟢 Lo que la rúbrica SÍ premia y el expediente tiene

**"Theory: how well does the paper describe WHY the approach works (as opposed to merely describing HOW it works)"**

Eso es **literalmente** lo que el expediente produjo todo el día: no "el gate ayuda" sino "el gate escalar se satura abierto y aprende a no gatear, medido en `gmean` 0,970". Y **"Universality"** premia que el método generalice fuera de la competencia, que es el caso de un motor que corre en un ESP32.

**Y el formato pedido es corto:** *"Shorter and clearer is always better. No filler, no unnecessary equations."*

<hr/>

## 3. Ítem 2 CERRADO · los "efficiency limits" de ARC-AGI-2 NO existen publicados

```plain
Submission Requirements
  Submissions must be made through the Kaggle competition as a Kaggle notebook.
  No internet access during evaluation
  All code and methods must be open sourced to be eligible for prizes
  HARDWARE AND COMPUTE LIMITS WILL BE ANNOUNCED WITH THE COMPETITION LAUNCH

Scoring Methodology
  For each task, you should predict exactly 2 outputs for every test input grid.
  If any of the 2 predicted outputs matches the ground truth exactly, you score
  1 for that task, otherwise 0.
```

**Estado correcto: NO PUBLICADOS, no "no leídos".** La página dice que se anuncian con el lanzamiento, y el lanzamiento fue el 25-mar. **Puede que estén en Kaggle y no en arcprize.org**, y eso queda como no medido.

**Lo que sí quedó medido:** sin internet en evaluación, y **2 intentos por tarea** (o sea que se puede apostar a dos hipótesis por grilla).

<hr/>

## 4. Ítem 5 CERRADO · se puede entrar a los tres tracks, y te lo piden

De la página de Kaggle de ARC-AGI-2, verbatim:

> *"Note: This is a relaunch of ARC Prize 2025. **If you are joining either this or ARC-AGI-3, please consider joining the paper track**, where you can document your approach for either one of the prediction competitions."*

Y del overview:

> *"Participants must open source their solutions before receiving official private evaluation scores. **This applies across all three competition tracks.**"*

**No hay restricción cruzada: el host INVITA a sumar el paper track a cualquiera de los dos de código.**

<hr/>

## 5. 🔥 Dos datos que NO estaban en ningún "no medido" y valen más que varios

### 5.1 El reglamento EXCLUYE a los sistemas por API

```plain
Internet access is not available during Kaggle evaluation
(no API-based systems like GPT/Claude/etc.)
```

> **Eso saca del tablero a cualquiera que dependa de llamar a un modelo grande por red.** Un motor autocontenido de 6.888 parámetros **no tiene ese problema por construcción**. No es una ventaja de eficiencia: es una ventaja de **elegibilidad**.

### 5.2 ARC-AGI-3 testea CUATRO capacidades, no cinco

Yo venía citando cinco ejes (de la página del benchmark). **La página de la competencia declara cuatro, y son las que valen:**

```plain
Exploration           informacion que hay que OBTENER interactuando
Modeling              observaciones -> world model que predice estados futuros
Goal-setting          identificar estados deseables SIN instrucciones
Planning and Execution  mapear el camino, y CORREGIR EL RUMBO con feedback
```

**Dos de las cuatro son exactamente los rojos del mapeo** (Modeling y Planning), y Goal-setting era el tercero. **O sea: de las cuatro capacidades oficiales, el expediente cubre una (Exploration, vía el gate) y le faltan tres.**

<hr/>

## 6. Los ítems que siguen abiertos, sin maquillar

| ítem | estado |
|---|---|
| 1. rúbrica del Paper Prize | 🟢 **CERRADO**, seis categorías verbatim |
| 2. efficiency limits de ARC-AGI-2 | 🟡 **NO PUBLICADOS en arcprize.org**. Pueden estar en Kaggle |
| 3. premio del Milestone #2 | 🟢 **CERRADO: 37.500 USD, 30-sep** |
| 4. papers ganadores 2025 | 🔴 **SIGUE ABIERTO.** Leí el reporte técnico, no los papers |
| 5. entrar a los tres tracks | 🟢 **CERRADO: permitido e invitado** |
| 6. el "7M parámetros" | 🔴 **sigue siendo del reporte 2025.** No hallada cifra 2026 |
| 7. la sección 5 es juicio | 🟢 **reconocido**, y este documento marca qué es juicio |

<hr/>

## 7. El calendario real, con los montos que faltaban

```plain
30-sep-2026   MILESTONE #2         37.500 USD garantizados   <- 35 DIAS
              requisito: open source por la deadline
02-nov-2026   submissions          Top Score 75K + Grand 700K
08-nov-2026   PAPERS               Top Paper 75K + pool 375K
04-dic-2026   resultados
```

<hr/>

## 8. NO MEDIDO, declarado

1. **No leí los papers ganadores de 2025.** Ítem 4, sigue abierto. Tengo títulos, autores y montos, no contenido.
2. **No leí la página de reglas de Kaggle de ninguno de los tres tracks**, solo arcprize.org y el highlight de Kaggle. **Los límites de hardware pueden estar ahí.**
3. **El techo de 4,17 es aritmética mía** sobre la rúbrica leída, **no una declaración del host**. Dicen "evaluated equally" y de ahi sale el promedio, pero **no publican la fórmula exacta**.
4. **No sé quién ganó el Milestone #1 en montos** ni si los 37.500 del #2 se reparten distinto si hay pocos participantes.
5. **No verifiqué si Abraham aceptó las reglas** de ninguno de los tres tracks. **Sigue siendo el bloqueante previo a todo.**
6. **No leí el leaderboard actual** de ninguno de los dos tracks de código.
7. **El "7M" del ítem 6 no se pudo actualizar.** Es del reporte 2025 y se cita así.
