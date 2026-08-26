# 094 · ARC-AGI-3 es el fin, y yo estuve auditando el paper. Dónde estamos y qué sigue

**Fecha:** 2026-08-25 23:05 (America/Buenos_Aires) · **Modo:** TITAN FULL

<hr/>

## 0. 🔴 Incumplimiento propio, y va primero

**Abraham tiene razón.** El fin declarado era **participar en ARC 3**. El paper y sus correcciones **ya están**. Y yo pasé el día auditando el paper, midiendo nulls y peritando motores.

Eso es **O-01**, el único error del registro que **no se ve en ningún diff**: la prioridad mal puesta. Y el propio protocolo dice que cuesta *"una tarde ajena"*. Hoy costó un día.

> **Y lo peor del caso:** el falsador volvió a ser Abraham, y esta vez sobre la **prioridad**, que es exactamente el hueco que W-01 dice que **ningún instrumento propio cubre**. Un compilador me detecta un tipo mal; nada me detecta que estoy midiendo lo que no importa.

<hr/>

## 1. Dónde estamos, con las fechas reales

**Verificado en vivo 2026-08-25.** Fuentes: `arcprize.org/competitions/2026`, `arXiv 2603.24621`, `docs.arcprize.org`.

```plain
ARC Prize 2026 - track ARC-AGI-3
  premios:  850.000 USD en el track   (2.000.000 en total)
            Grand Prize   700K   al primero que saque 100%
            Top Score      75K   GARANTIZADO: 1o 40K, 2o ...

  25-mar-2026  arranco la competencia
  30-jun-2026  Milestone #1        <- PASO, sin participar
  30-sep-2026  Milestone #2        <- 36 DIAS
  02-nov-2026  submissions due     <- 69 DIAS
  08-nov-2026  papers due          <- 75 DIAS
  04-dic-2026  resultados

  frontier AI a marzo 2026:  por debajo del 1%
  humanos:                   100%
```

**Y el estado nuestro, medido el 21-ago:** `ARC = 0` en los **25 notebooks**. Se barrió `arc-agi`, `arc_agi`, `arc-prize` y los patrones de los JSON de tareas. **Cero coincidencias.** El `ARC` que había aparecido en un barrido anterior era ruido de subcadena (`MARCO`, `SPARC`).

> **Traducido: 69 días para submissions y cero trabajo hecho sobre el objetivo real.**

<hr/>

## 2. 🟢 El dato que cambia la ecuación: la interfaz es MÍNIMA

Leí el repo oficial `arcprize/ARC-AGI-3-Kaggle-Starter` (README de 9.534 B, `agent/my_agent.py` de 3.954 B). **Un agente es esto:**

```python
class MyAgent(Agent):
    def is_done(self, frames, latest_frame) -> bool:
        """Return True when your agent wants to stop playing."""

    def choose_action(self, frames, latest_frame) -> GameAction:
        """Look at the game state and return the next action."""
```

**Dos métodos. Un archivo.** El README dice textual: *"This is the only file you normally touch"*. Todo lo demás (plomería de Kaggle, formato de submission, orquestación del juego) ya está hecho.

Y tres cosas más que sacan excusas del medio:

- **`make play-local` corre contra los juegos reales, localmente, en segundos.** El motor de juego es el paquete `arc-agi` de PyPI, **el mismo que corre el gateway de Kaggle**.
- **Offline después de la primera descarga:** *"once downloaded, games are cached in environment_files/ and you're fully offline"*.
- **`No GPU required for the starter agent`.** El starter puede correr en `cpu`.

<hr/>

## 3. 🟢 Tres activos que YA tenemos y nadie contó

### 3.1 La autenticación que arreglé hoy es EXACTAMENTE la que pide el starter

El README, verbatim:

```bash
mkdir -p .kaggle && echo "KGAT_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx" > .kaggle/access_token
```

**`KGAT_` es el formato exacto de los dos tokens de Abraham** (medido: prefijo `KGAT_`, largo 37). Y hoy quedó probado que el push a Kaggle funciona con `Bearer`. **La plomería está resuelta antes de empezar**, y eso no fue planificado: cayó de casualidad del trabajo del motor.

### 3.2 DOS cuentas = 10 submissions por día

El README: *"You only get 5 official submissions per day"*. **Con dos cuentas son 10.** El doble de intentos que cualquier competidor individual.

### 3.3 El Paper Prize existe, y el paper ya existe

Hay un tercer track de premios a papers, con fecha **8-nov**. El paper del conectoma **ya está escrito y corregido**. Es una segunda bala con un activo que ya está pago.

<hr/>

## 4. La tesis de Abraham contra la especificación del benchmark

**"Un sistema inteligente que se despliegue en un lugar desconocido sin previo entrenamiento."**

El abstract oficial de ARC-AGI-3, verbatim:

> *"an interactive benchmark for studying agentic intelligence through novel, abstract, turn-based environments in which agents must explore, infer goals, build internal models of environment dynamics, and plan effective action sequences **without explicit instructions**"*

Y de la página del benchmark:

> *"agents must learn from experience inside each environment — perceiving what matters, selecting actions, and adapting their strategy **without relying on natural-language instructions**"*

> **No dudo de la tesis. Es literalmente la especificación del benchmark.** Chollet diseñó ARC alrededor de esa idea, y la tesis del **96% fijo** (un substrato que no aprende más adaptación rápida encima) es de la misma familia que "Core Knowledge priors + inteligencia fluida". El encuadre de Abraham y el de la competencia **coinciden**, y eso no es casualidad: es la cuarta convergencia del día.

### Dónde SÍ dudo, y es preciso

<table><tbody><tr><th width="220" cell-bg-color="grey"><p><strong>duda</strong></p></th><th width="220" cell-bg-color="grey"><p><strong>medido</strong></p></th><th width="220" cell-bg-color="grey"><p><strong>¿fatal?</strong></p></th></tr><tr><td width="220"><p>la interfaz no coincide</p></td><td width="220"><p>los motores toman <strong>36 sensores continuos</strong> y devuelven 1 de 12. ARC-3 entrega <code>frames</code> (grillas) y espera <code>GameAction</code></p></td><td width="220"><p><strong>No.</strong> Es trabajo de adaptación, no un muro</p></td></tr><tr><td width="220"><p>no hay planificación</p></td><td width="220"><p>ni el DBC3 ni el DualBrain ni <code>motor.py</code> tienen búsqueda, world model ni planning. El benchmark lo pide <strong>explícitamente</strong></p></td><td width="220"><p>🔴 <strong>Es EL hueco.</strong> Un LTC de 6.888 parámetros no planifica</p></td></tr><tr><td width="220"><p>la vara real</p></td><td width="220"><p><strong>frontier &lt;1%</strong> con presupuestos enormes</p></td><td width="220"><p>calibración, no imposibilidad</p></td></tr></tbody></table>

> **Y el &lt;1% se lee de dos maneras, las dos ciertas.** Es durísimo, sí. Pero también significa que **el tablero está casi vacío**, y el **Top Score Award de 75K está garantizado** sin necesidad de sacar 100%. No hay que ganarle a nadie que ya resolvió el problema: **nadie lo resolvió**.

<hr/>

## 5. Qué sigue, con el criterio de orden declarado (O-01)

**Criterio: qué pone un número distinto de cero en el tablero lo antes posible.** No qué arquitectura es más linda. Con 69 días, el riesgo real es **llegar con cero**, no llegar con algo subóptimo.

1. **Clonar el starter y correr `make play-local` con el agente random.** Cierra la pregunta "¿la plomería funciona?" en minutos, no en días. El token ya está en el formato correcto.
2. **Subir el random a Kaggle y sacar un score, aunque sea 0,0.** Un cero **en el tablero** es infinitamente más que un cero **fuera** del tablero: valida las dos fases (Save & Run All, y Submit to Competition) y deja el circuito probado antes de que haya algo bueno que arriesgar.
3. **Recién entonces meter la tesis.** Y el orden dentro de la tesis también importa: primero **el gate reflejo/memoria como explorar/explotar**, que es la pieza que ya está medida y validada (+16,0 pts en XORMemory con el gate simétrico); después el resto.
4. **En paralelo y barato: el Paper Prize.** El paper existe. Es la única de las cuatro que no compite por el mismo tiempo.

**Lo que NO haría:** seguir puliendo los nulls del conectoma antes del paso 2. Los 38 nulls que faltan son **8 horas de máquina** y no acercan ni un milímetro al fin declarado. Que sigan corriendo solos, sí. Que ocupen la cabeza, no.

<hr/>

## 6. NO MEDIDO, declarado

1. **No cloné el starter ni corrí `make play-local`.** Todo lo del punto 2 es lectura del README, no ejecución.
2. **No sé si Abraham aceptó las reglas de la competencia**, que es requisito previo y bloquea todo.
3. **No sé cuántos juegos tiene el set** ni cuál es el score actual del líder del tablero. **No leí el leaderboard.**
4. **No verifiqué la cuota de GPU** de ninguna de las dos cuentas.
5. **Que las dos cuentas den 10 submissions/día es una inferencia**, no una lectura de las reglas. Puede haber cláusulas sobre cuentas múltiples del mismo participante, **y eso hay que leerlo antes de contarlo como activo**.
6. **El Milestone #1 del 30-jun ya pasó.** No sé qué otorgaba ni si su premio sigue en juego.
7. **La sección 5 es JUICIO**, no medición. Es contradecible y debería contradecirse si Abraham tiene otro criterio de orden.
