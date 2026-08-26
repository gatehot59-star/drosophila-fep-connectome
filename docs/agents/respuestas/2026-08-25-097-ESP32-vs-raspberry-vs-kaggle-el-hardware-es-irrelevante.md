# 097 · ¿ESP32, Raspberry o ninguno? El hardware es irrelevante para ARC-3, y eso es buena noticia

**Fecha:** 2026-08-25 23:40 (America/Buenos_Aires) · **Modo:** TITAN FULL

**La pregunta:** ¿escalar de ESP32 a Raspberry Pi 3 ayuda en ARC-3? ¿O en la competencia no sirve ninguno de los dos?

<hr/>

## 1. La respuesta directa: en la competencia no corre ni uno ni otro

**Leí el código del agente oficial.** `agent/my_agent.py` del starter, verbatim:

```python
from arcengine import FrameData, GameAction, GameState
from agents.agent import Agent

class MyAgent(Agent):
    MAX_ACTIONS = 80

    def is_done(self, frames, latest_frame) -> bool: ...
    def choose_action(self, frames, latest_frame) -> GameAction: ...
```

Y el detalle de la acción compleja:

```python
if action.is_complex():
    # ACTION6 takes (x, y) coordinates on a 64x64 grid.
    action.set_data({"x": random.randint(0, 63), "y": random.randint(0, 63)})
```

**Aceleradores que ofrece el starter:** `cpu`, `t4`, `p100`, `rtx6000` (éste último **exclusivo de ARC-AGI-3**).

> **El agente corre en un notebook de Kaggle. Punto.** El hardware disponible es **enorme** comparado con un ESP32 o una Raspberry. No hay ninguna categoría "embebido" ni bonus por eficiencia de hardware.

<hr/>

## 2. 🟢 Y eso es BUENA noticia, no mala. Tres razones medidas

### 2.1 El presupuesto que hoy limita al motor DESAPARECE

Lo que hoy constriñe el DualBrain está medido: **800 B de RAM** y **1.336 B de `.text`**. En un T4 eso deja de existir como restricción. **El motor puede crecer sin pagar el peaje del micro.**

### 2.2 🔥 Se puede meter el planificador que falta

El hueco rojo del mapeo contra ARC-3 era **planificación / world model / goal acquisition**. Y había una duda práctica escrita como "no medido": *"no sé si el planificador entra en el presupuesto"*.

**En un ESP32 no entraba. En un T4 sí.** La restricción que hacía difícil el hueco **no aplica en la competencia**.

### 2.3 El límite real de ARC-3 no es memoria ni FLOPs

```python
MAX_ACTIONS = 80   # por juego, mas los limites globales del framework
```

**Lo que se optimiza son ACCIONES, no milisegundos.** Un agente que decide **bien** en 80 movidas gana; uno que decide **rápido y mal**, no. Y el score del benchmark es *"skill-acquisition efficiency"*, o sea **eficiencia por acción**.

> **Eso cambia qué hay que optimizar.** Todo el trabajo de bajar bytes y ciclos es irrelevante acá. Lo que importa es **cuánta información extrae el agente por movida**.

<hr/>

## 3. 🔥 Entonces ¿para qué sirvió el trabajo del ESP32? Y acá está el punto no obvio

**No como plataforma. SÍ como DISCIPLINA DE DISEÑO.**

El presupuesto de 800 B **forzó** un motor de 3.553 parámetros cuya vía rápida **no entrena**. Esa restricción es la que produjo la arquitectura que ahora resulta compatible con *"desplegarse en un lugar desconocido sin entrenamiento previo"*.

> **Sin el corsé del micro, el diseño natural habría sido un modelo grande entrenado con un dataset**, que es exactamente lo que ARC-3 prohíbe por construcción. **El ESP32 fue el instrumento que forzó la idea, no el destino de la idea.**

Y hay evidencia de eso en el propio expediente: el `CONTEXTO-motor` define el producto como *"que el motor deje de necesitar entrenamiento para funcionar"*, y esa definición salió de la línea embebida, no del paper.

<hr/>

## 4. La Raspberry Pi 3: no aporta a la competencia, sí al producto

**Y son dos objetivos distintos que conviene no mezclar (O-01, que ya se incumplió una vez hoy).**

| destino | ¿sirve para ARC-3? | ¿sirve para el producto? |
|---|---|---|
| **ESP32** | 🔴 no, no es la plataforma | 🟢 **sí, es el diferencial**: nadie más entra ahí |
| **Raspberry Pi 3** | 🔴 no, no es la plataforma | 🟡 **sí, pero ahí HAY competencia** |
| **notebook de Kaggle** | 🟢 **es LA plataforma** | 🔴 no es un producto vendible |

**El dato que decide sobre la Raspberry, y ya está en el `CONTEXTO-motor`:** *"Competidor medido: Liquid AI (Hasani, 293 M USD, 97 empleados). Su producto más chico es LFM2.5-230M **en Raspberry Pi**"*.

> **Subir a Raspberry es entrar justo en el terreno donde ya juega un rival con 293 millones de dólares.** Abajo del teléfono, ellos no entran, y eso hoy es la ventaja. **Escalar a Raspberry es abandonar el único nicho donde no hay competencia.**

Para el **producto** es un escalón legítimo si el mercado lo pide. Para **ARC-3 en 69 días** es una distracción.

<hr/>

## 5. 🔴 La contra que hay que decir, porque corta para el otro lado

**Si el hardware es irrelevante y el presupuesto desaparece, también desaparece la ventaja del motor.**

En un T4, un motor de 3.553 parámetros compite contra cualquier cosa: transformers, búsqueda con LLM, RL con millones de parámetros. **La eficiencia deja de ser un diferencial y pasa a ser una limitación autoimpuesta.**

**Lo que sigue valiendo en ese terreno no es el tamaño: es NO ENTRENAR.** Y eso vale porque el benchmark lo exige, no porque sea barato.

> **La línea correcta para ARC-3: "nuestro agente no necesita entrenamiento", no "nuestro agente es chiquito".** El segundo argumento no le importa a nadie en Kaggle.

<hr/>

## 6. Y un dato del tablero que conviene tener

**El Milestone #1 lo ganó Tufa Labs** con un agente llamado *"the Duck"*, sucesor de *"Stochastic Goose"*, con seis autores. Y su propia descripción dice que consiste en *"an inference harness leveraging..."*.

**El agente random del starter es literalmente un port de Stochastic Goose.** O sea: el baseline que Kaggle reparte es el ancestro del ganador del primer milestone.

> **Eso calibra la vara: los que ganan son equipos con harness de inferencia, no arquitecturas exóticas de pocos parámetros.**

<hr/>

## 7. Veredicto, en tres líneas

1. **Para ARC-3: ni ESP32 ni Raspberry. Corre en Kaggle, con T4 o RTX 6000 disponibles.**
2. **El trabajo del ESP32 no se tira: fue la restricción que produjo la arquitectura sin entrenamiento.** Ese es su aporte, y es grande.
3. **La Raspberry es para el producto, no para la competencia**, y entra en terreno donde ya hay un rival de 293 M USD.

<hr/>

## 8. NO MEDIDO, declarado

1. **No leí las reglas completas de Kaggle**, solo la página pública. **No sé el límite de tiempo de ejecución del notebook**, que es el único límite de cómputo que podría importar.
2. **No sé si hay límite de tamaño de modelo** ni de acceso a internet en la fase de scoring (el starter dice que las sesiones aceleradas tienen internet deshabilitado).
3. **No corrí el starter.** Todo esto es lectura de código y documentación.
4. **No leí el write-up completo de Tufa Labs**, solo su primer párrafo. **No sé su score ni su método.**
5. **`MAX_ACTIONS = 80` es del agente de ejemplo**, no necesariamente el límite duro del framework. El comentario dice *"the framework also enforces global limits"* y **esos límites no los leí**.
6. **La afirmación "el ESP32 forzó la arquitectura" es una interpretación histórica mía**, no un hecho documentado. La cronología del expediente dice que la línea neuromórfica es la primera, lo cual es **consistente** con esa lectura, pero no la prueba.
7. **La sección 7 es juicio.** Contradecible.
