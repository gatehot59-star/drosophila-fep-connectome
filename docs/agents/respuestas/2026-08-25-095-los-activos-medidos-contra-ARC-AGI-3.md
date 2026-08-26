# 095 · Leí el DualBrain y el conectoma: ¿de ahí sale lo que necesitamos para ARC-3?

**Fecha:** 2026-08-25 23:15 (America/Buenos_Aires) · **Modo:** TITAN FULL

**Instrumento:** lectura real de `docs/agents/CONTEXTO-motor.md` (25.688 B) cruzada contra la especificación oficial de ARC-AGI-3 verificada en vivo. **Ninguna corrida nueva:** todos los números citados acá ya están medidos y en git.

**La respuesta corta:** **sí sale, pero no completo.** Y la pieza que falta **ya estaba diseñada y sin correr**, con su costo estimado. Eso cambia la prioridad, no el plan.

<hr/>

## 1. Lo que ARC-AGI-3 pide, textual

De `arcprize.org/arc-agi/3` y del abstract de arXiv 2603.24621:

```plain
  Exploration
  Percept -> Plan -> Action
  Memory
  Goal Acquisition
  Alignment

  "agents must explore, infer goals, build internal models of environment
   dynamics, and plan effective action sequences without explicit instructions"

  "environments only leverage Core Knowledge priors"
  "skill-acquisition efficiency over time"
  "long-horizon planning with sparse feedback"
```

<hr/>

## 2. 🟢 Lo que SÍ sirve, con su número ya medido

### 2.1 EL GATE, y es el activo más fuerte de todo el expediente

```plain
  ABLACION DEL GATE (DualBrain vs DualNoGate)
  Mismos parametros, misma celda, mismo encoder.
  La unica diferencia: g*h_m contra h_m.

  Gated     con_gate=0.000236  sin_gate=0.025539  AYUDA 108.11x  p=1.56e-105
  LinScale  con_gate=0.000055  sin_gate=0.001192  AYUDA  21.85x  p=3.36e-16
  MultiCue  con_gate=0.000326  sin_gate=0.019235  AYUDA  58.97x  p=4.91e-03
  CR        con_gate=0.000054  sin_gate=0.001979  AYUDA  36.72x  p=1.38e-31
```

**Iso-run, iso-arquitectura, iso-celda, iso-encoder, 10 semillas.** El propio contexto lo llama *"el resultado con menos objeciones posibles de todo el expediente"* y **es publicable hoy**.

**Traducción a ARC-3:** el gate es literalmente el árbitro **explorar/explotar**. La vía rápida reacciona al frame actual; la vía lenta acumula el modelo del entorno; el gate decide cuál manda esta jugada. Eso cubre dos de los cinco ejes del benchmark de una sola pieza: **Percept→Plan→Action** y **Memory**.

### 🔥 Y hay un dato más fino que vale oro para un agente

> **El gate ESCALAR se satura abierto** (`gmean` 0,970 / 0,970 / 0,964), o sea **aprende a NO gatear**. El **vectorial nunca colapsa a escalar** (4/4).

**Un agente que aprende a no gatear es un agente que nunca alterna de estrategia.** Para ARC-3, donde la eficiencia de adquisición es *el* score, eso es fatal. **Ese hallazgo, que en el paper era una curiosidad, acá es una decisión de diseño: gate vectorial, no escalar.**

### 2.2 TAU HETEROGÉNEA · spread 31,2× medido

Cortes a −3 dB de 0,00195 a 0,06102 ciclos/muestra, del barrido de Bode en `results/dualbrain_bench.log`.

**ARC-3 pide "long-horizon planning with sparse feedback".** Un banco de constantes de tiempo distintas es **varios horizontes de memoria funcionando a la vez**: el canal lento retiene el objetivo entre jugadas mientras el rápido sigue el frame. **No hay que inventarlo: está medido.**

### 2.3 NO ENTRENA

Es la restricción literal del benchmark. Un agente se despliega en un entorno nuevo **sin dataset previo**. Y el producto está definido así desde el principio: *"que el motor deje de necesitar entrenamiento para funcionar"*.

### 2.4 🔥 LA BIBLIOTECA DE CIRCUITOS = los Core Knowledge priors

**Esta es la coincidencia más profunda y nadie la había encuadrado así.**

- ARC-3 declara: *"environments only leverage **Core Knowledge priors**"*.
- El contexto del motor declara: *"el activo final no es el motor: es **la biblioteca** de circuitos con función verificada (la hoja de datos de los 74xx)"*, y **cada entrada dice qué hace y qué no**.

> **Son la misma idea desde dos lados.** Chollet diseñó ARC alrededor de la tesis de que la inteligencia fluida opera sobre un conjunto chico de priors innatos. El producto de Abraham **es una tabla de priors cableados con función verificada**. Lo que en el paper es "biblioteca de circuitos" en ARC-3 se llama "Core Knowledge priors".

**Estado real de esa biblioteca: 1 entrada de las 3-4 que hacen falta.** Es el activo con más techo y el menos avanzado.

<hr/>

## 3. 🔴 Lo que NO sirve, medido y sin maquillar

### 3.1 NO HAY PLANIFICACIÓN. Es EL hueco

Ninguno de los tres motores tiene búsqueda, world model ni planning. Y el abstract oficial lo exige textual: *"build internal models of environment dynamics, and **plan** effective action sequences"*.

**Un LTC de 1.400 o 6.888 parámetros no planifica.** Es un filtro con memoria y un árbitro. Eso alcanza para *reaccionar bien*, no para *anticipar*.

### 3.2 🔴 `MultiCue` es una CONTRAINDICACIÓN DIRECTA, y hay que decirla

```plain
  MultiCue  (x*(c1+c2)/2, lineal, 2 refs)   DualBrain MSE=0.000326
   vs GRU     MSE=0.000138  ratio=0.42x  p=1.13e-06  gana=GRU
   vs LSTM    MSE=0.000081  ratio=0.25x  p=3.27e-11  gana=LSTM
   vs MinGRU  MSE=0.000191  ratio=0.59x  p=6.17e-04  gana=MinGRU
```

El propio contexto lo cierra así: **"el nicho es modulación por UNA referencia retenida, no fusión multi-referencia. Venderlo como lo segundo es venderlo donde mide peor."**

> **Y una grilla de ARC-3 tiene MUCHAS referencias simultáneas por naturaleza:** varios objetos, varias reglas, varias relaciones espaciales a la vez. **El nicho medido del motor y la naturaleza del benchmark no coinciden en este eje.** Es el riesgo más serio y está medido, no supuesto.

**El matiz que lo salva parcialmente:** el mismo contexto muestra que el reparto `h_m`/`h_r` **decide si gana o pierde** en la tarea de dos referencias (en `h_m=5` pierde 4×, en `h_m=10` queda 1,18× arriba). O sea: **la contraindicación depende del reparto, y el reparto es una perilla nuestra.**

### 3.3 Interfaz y dominio

Todo sintético, sensores continuos, 12 salidas. **Nada se probó sobre señal real** (ítem 10 del NO MEDIDO). ARC-3 son grillas discretas y `GameAction`. Adaptable, pero no gratis.

<hr/>

## 4. 🔥 EL REFRAME: el brazo W+S deja de ser deuda del paper y pasa al camino crítico

**Esto es lo más importante del documento.**

El ítem 2 del NO MEDIDO de `CONTEXTO-motor.md` es la hipótesis del **96% fijo**, con sus cuatro brazos:

| Brazo | `react` | Qué aísla |
|---|---|---|
| A | denso aleatorio entrenado | el techo |
| B | denso aleatorio **congelado** | **ya medido: 3,76× a 14,26× peor** |
| **W** | máscara del conectoma + τ heterogénea, congelado | si el **cableado** congelado alcanza |
| **S** | máscara **shuffle** (mismo grado, misma sparsity), congelado | ¿es el conectoma, o cualquier grafo disperso? |

### Por qué esto ahora es de ARC y no del paper

**Ya está medido que congelar la vía rápida con pesos ALEATORIOS empeora 2,19× a 14,26× en 4/4 tareas.** El contexto lo marca como *"REFUTADO pero mal medido: congeló pesos aleatorios, no cableados"*.

**Y esa misma medición, leída para ARC-3, dice algo crítico:**

> **Un reflejo no entrenado NO funciona, salvo que el cableado cargue información.**

Eso es **exactamente** la pregunta de la competencia. El agente se despliega sin entrenar, así que su vía rápida **tiene** que venir de estructura. Si el brazo `W` funciona, hay producto para ARC-3. Si no funciona, **el agente necesita aprender en el episodio** y es otro diseño.

**Y el contexto ya trae la lectura a favor, escrita post-hoc:** *"si congelar ruido hubiera dado igual, el conectoma no habría hecho falta para nada"*. Que el ruido congelado **empeore** es la condición necesaria para que el cableado pueda importar.

### El costo ya está estimado en el propio archivo

**~90 min de CPU, 4 brazos, 10 semillas**, y el único trabajo nuevo es la máscara desde el parquet, **que ya está cargado y verificado**. Con criterio de aborto escrito: *"si `W` no le gana a `B` en al menos 3 de 4 tareas, la analogía del 96% se retira"*.

> **Mismo experimento, otro propósito.** Antes era para salvar una sección del paper. Ahora es **la validación central del producto para la competencia**, y el brazo `S` es el que impide que sea una demo.

<hr/>

## 5. El mapeo completo, en una tabla

| eje de ARC-AGI-3 | ¿tenemos algo? | evidencia |
|---|---|---|
| **Memory** | 🟢 **sí, medido** | τ heterogénea, spread **31,2×** |
| **Exploration** (explorar/explotar) | 🟢 **sí, medido** | gate: **21,85× a 108,11×**, 4/4, `p` hasta 1,56e-105 |
| **Core Knowledge priors** | 🟡 **el marco sí, el contenido no** | biblioteca: **1 entrada** de 3-4 |
| **sin entrenamiento previo** | 🟡 **sí en diseño, NO validado** | brazo `W` **nunca corrió** |
| **Percept → Action** | 🟡 **sí, con adaptación** | 36 continuos → 12; ARC-3 da grillas |
| **Plan** (planning, world model) | 🔴 **NO. Nada** | ningún motor lo tiene |
| **Goal Acquisition** | 🔴 **NO** | no hay mecanismo de inferir objetivo |
| **multi-referencia simultánea** | 🔴 **medido EN CONTRA** | `MultiCue`: pierde contra GRU, LSTM y MinGRU |

**Cuatro verdes o amarillos fuertes, tres rojos.** Y los tres rojos son del mismo lado: **el motor sabe reaccionar y recordar; no sabe planificar ni fijarse un objetivo.**

<hr/>

## 6. Qué producto sale de esto, concreto

**Un agente de dos vías con gate vectorial y τ heterogénea, con los priors cableados en la vía rápida, y un planificador chico encima que el expediente NO tiene.**

Las tres primeras piezas están medidas. La cuarta hay que construirla o traerla, y es honesto decir que **es la mitad del problema de ARC-3**, no un detalle.

**Y lo que el expediente aporta que nadie más tiene:** no es la arquitectura (LTC es de Hasani, AAAI-21, y está declarado en el peritaje de originalidad). Es **de dónde salen los pesos**: una tabla de priors medidos sobre un conectoma real, con función verificada y con su "qué no hace" escrito al lado. **Eso es lo que se parece a Core Knowledge.**

<hr/>

## 7. NO MEDIDO, declarado

1. **No corrí el starter de ARC-3 ni un agente.** Todo el mapeo es lectura cruzada de dos especificaciones.
2. **No leí el paper técnico completo de ARC-AGI-3**, solo el abstract y las páginas públicas. **No sé el formato exacto de `frames` ni el espacio de `GameAction`.**
3. **El brazo `W` sigue sin correr.** Sin él, "el cableado alcanza" es hipótesis.
4. **La traducción gate → explorar/explotar es MI interpretación**, no una medición. El gate se midió sobre regresión continua, no sobre decisión de acción.
5. **Que "biblioteca de circuitos" y "Core Knowledge priors" sean la misma cosa es un argumento, no un hecho.** Es contradecible y debería contradecirse.
6. **No medií nada sobre grillas.** La contraindicación de `MultiCue` se extrapola de 2 referencias continuas a *n* objetos discretos, y esa extrapolación **no está medida**.
7. **No sé si el planificador se puede meter en el presupuesto** de un agente que corre bajo límite de tiempo en Kaggle.
