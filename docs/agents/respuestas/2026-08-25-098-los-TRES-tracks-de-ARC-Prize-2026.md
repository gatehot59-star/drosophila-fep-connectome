# 098 · Son TRES tracks, no uno. Y el que mejor calza no es el que yo emp**ujaba

**Fecha:** 2026-08-25 23:50 (America/Buenos_Aires) · **Modo:** TITAN FULL

<hr/>

## 0. 🔴 Corrección de un mapa incompleto mío

Abraham dijo que había **varias competencias o instancias o categorías, en distintas fechas**. **Tenía razón**, y mi respuesta anterior estaba incompleta: mapeé **solo** el track de ARC-AGI-3.

Eso es el **patrón 1 del Bloque 8**: *un mapa incompleto presentado como el mapa*. Y por segunda vez en la noche, **el falsador fue Abraham**.

<hr/>

## 1. El mapa completo, verificado en vivo

```plain
ARC PRIZE 2026 - 2.000.000 USD, TRES tracks

  ARC-AGI-3  (interactivo)     850.000   agentes en entornos novedosos
     Grand Prize      700K   al primero con 100%
     Top Score         75K   GARANTIZADO  (1o 40K, 2o ...)

  ARC-AGI-2  (estatico)        700.000   85% en el eval privado
     Progress Prizes  275K   1o 75K, 2o 50K, 3o 40K, 4o 35K, 5o 25K...
     Grand Prize      275K
     Bonus Prize      150K

  PAPER PRIZE                  450.000
     Top Paper         75K   GARANTIZADO  (1o 50K, 2o 20K, 3o 5K)
     Outstanding Pool 375K   papers con score >4.5 en la rubrica,
                             "multiple parties may win from this pool"

FECHAS
  25-mar-2026  arranco
  30-jun-2026  ARC-AGI-3 Milestone #1     <- PASO
  30-sep-2026  ARC-AGI-3 Milestone #2     <- 36 dias
  02-nov-2026  submissions due            <- 69 dias
  08-nov-2026  PAPERS due                 <- 75 dias
  04-dic-2026  resultados
```

**Y un dato del track 2 que no había visto:** ARC-AGI-2 es *"a relaunch of ARC Prize 2025"*, y su objetivo es **85% de accuracy dentro de los "Kaggle efficiency limits"**. El top score de 2025 fue **24%** con 1.455 equipos y 15.154 entradas.

<hr/>

## 2. 🔥 El hallazgo que cambia la estrategia, y está en el Paper Prize

**Verbatim de `arcprize.org/competitions/2026/paper`:**

> *"Paper submissions must be linked to a Kaggle code submission (ARC-AGI-2 or ARC-AGI-3) that demonstrates the approach detailed in the paper. **The code submission need not achieve a high score for the corresponding paper to be eligible.**"*

**Traducido: el agente random del starter, subido, YA HABILITA el Paper Prize de 450.000 USD.** El score **no es requisito de elegibilidad**.

Y el pool no es de un solo ganador: **375K para papers con score mayor a 4,5 en la rúbrica, y "multiple parties may win"**.

> **Eso invierte el orden de dificultad.** Para ARC-AGI-3 hay que resolver planificación en 69 días. Para el Paper Prize hay que **escribir bien lo que ya se midió** y tener **cualquier** submission de código linkeada.

<hr/>

## 3. 🔥 Y el dato que duele y alienta a la vez: la tesis YA GANÓ papers acá

**Ganadores del Paper Award 2025, verbatim de `arcprize.org/competitions/2025`:**

```plain
  1er lugar  50K  "Less is More: Recursive Reasoning with Tiny Networks"
                  A. Jolicoeur-Martineau
  2do lugar  20K  "Self-Improving Language Models for Evolutionary Program
                  Synthesis"
  3er lugar   5K  "ARC-AGI Without Pretraining"   I. Liao & A. Gu
```

Y el **ARC Prize 2025 Technical Report** (arXiv 2601.10904), textual:

> *"zero-pretraining deep learning methods which are now achieving competitive performance with **remarkably small networks (7M parameters)**"*

### Las dos lecturas, y las dos son ciertas

**🟢 A favor:** "redes chicas" y "sin pre-entrenamiento" **no son ideas exóticas en este concurso: son líneas PREMIADAS**, primer y tercer puesto del año pasado. El encuadre de Abraham no necesita defenderse: **ya está validado por el jurado**.

**🔴 En contra:** la referencia de escala es **7 millones de parámetros**. El DualBrain tiene **3.553** y el DBC3 **6.888**. Eso es **1.000× a 2.000× más chico que el estado del arte de "red chica"** en este benchmark.

> **La pregunta honesta que sale de ahí: ¿hay una razón para creer que 6.888 parámetros alcanzan donde 7 millones son "remarkably small"?** La única respuesta defendible es la que ya está medida: que los pesos **no se entrenan, vienen de estructura**. Si eso no funciona (brazo `W`), el argumento de escala se cae solo.

<hr/>

## 4. Los tres tracks contra lo que YA existe

| track | premio | qué exige | ¿qué tenemos? |
|---|---|---|---|
| **Paper Prize** | **450K** | paper + **cualquier** submission linkeada | 🟢 **paper escrito, bitácora de hipótesis muertas, 8 guards, ablación del gate con `p`=1,56e-105** |
| ARC-AGI-3 | 850K | agente que explore, planifique y adquiera objetivos | 🟡 gate y `τ` medidos; 🔴 **cero planificación** |
| ARC-AGI-2 | 700K | 85% en tareas estáticas de grilla | 🔴 **nada.** El top de 2025 fue 24% |

**El Paper Prize es el track con mejor relación entre lo que ya existe y lo que hay que construir.** No porque sea fácil, sino porque **el activo que el expediente tiene es exactamente lo que ese track premia**: método, hipótesis refutadas con medición, y un encuadre que ya ganó en ediciones anteriores.

<hr/>

## 5. Consecuencia de prioridad (O-01)

**No cambia el objetivo de fondo, cambia el orden.**

1. **Subir cualquier submission de código** (el random alcanza) → habilita el Paper Prize y valida el circuito. **Es el mismo paso 1 y 2 que ya estaba propuesto, pero ahora se sabe que desbloquea 450K, no solo que "prueba la plomería".**
2. **Escribir el paper para el track**, con fecha **8-nov (75 días)**. El activo está escrito; hay que reencuadrarlo hacia ARC.
3. **Correr el brazo `W`+`S`**, porque es lo que sostiene el argumento de escala frente al 7M de referencia.
4. **ARC-AGI-3 con el agente**, que es el track más grande y el que necesita la pieza que falta.
5. **ARC-AGI-2: no entrar.** Cero trabajo hecho, top de 24% y 1.455 equipos compitiendo. **Entrar ahí con 69 días y nada hecho es repartir el esfuerzo sobre el objetivo equivocado.**

<hr/>

## 6. NO MEDIDO, declarado

1. **No leí la rúbrica completa del Paper Prize**, solo que existe y que el umbral del pool es **4,5**. **No sé sus criterios.**
2. **No leí las "Kaggle efficiency limits"** de ARC-AGI-2, que son parte de su objetivo.
3. **No sé si el Milestone #2 del 30-sep tiene premio propio** ni cuánto.
4. **No leí los papers ganadores de 2025**, solo sus títulos y montos.
5. **No verifiqué si un mismo participante puede entrar a los tres tracks** ni si hay restricciones cruzadas.
6. **El "7M parámetros" es del reporte 2025**, no del estado del arte de hoy. Puede haber bajado o subido.
7. **La sección 5 es juicio, no medición.** Contradecible, y debería contradecirse si Abraham tiene otro criterio.
