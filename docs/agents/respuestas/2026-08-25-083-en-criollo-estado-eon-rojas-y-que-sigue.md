# 083 · EN CRIOLLO · estado al 2026-08-25 11:15

**Fecha:** 2026-08-25 11:15 (America/Buenos_Aires) · **Modo:** TITAN LIGERO (síntesis, cero mediciones nuevas)

> **📄 Doc de ClickUp:** «EN CRIOLLO · dónde estamos al 25-ago 11:15 · el activo, el agujero de 5 días, y qué aportaron Eon y Rojas»
> **🛠 Instrumento:** ninguno (declarado). Todo número sale de las resp 063-082 y de sus archivos de evidencia, todos commiteados.

---

## 1. Pedido

«En criollo, cuál es el estado de nuestro trabajo, para dónde vamos, Eon y Rojas qué aportaron, qué sigue.» Cuatro preguntas. **No pidió una medición.**

## 2. Herramientas declaradas (C-03)

| Llamada | Escribe | Cuota ajena |
|---|---|---|
| `create_document` × 1 (ClickUp) | sí | no |
| `create_or_update_file` × 1 → rama `titan/twohop-nulls` | sí | no |

**Cero lecturas nuevas de repo, cero gateway, cero Kaggle, cero runtime de Tachi. Ningún merge. `main` intacta.** El estado venía cargado de los turnos anteriores.

---

## 3. El estado, en una frase

**Hay ciencia que aguanta y un envase que no.** Y en las últimas dos horas apareció un tercer problema que no es ni ciencia ni envase: **el código del repo no es el que produjo el paper.**

## 4. Lo que HAY, y hoy es más fuerte que ayer

**El hallazgo:** el circuito distingue estímulos por **cómo se apaga**, no por la altura de la respuesta. `sel_post` = **4,3287** contra **1,1896 ± 0,0173** (z = **+181,4**), y **0/40** contra el null que respeta Dale (z = +6,31).

**Dos respaldos nuevos de hoy:**

1. **Betzel et al. (2026), PLOS, con revisión por pares, valida el ítem 1 del erratum:** reporta `N = 138.639`, `M = 15.091.983`, `Mw = 54.492.922` y `d = 7,8 × 10⁻⁴`. **Los tres conteos al dígito y la densidad CORREGIDA, no la publicada.**
2. **Su modelo NO puede lo que puede el propio, y está medido sobre el mismo grafo:** su cascada **satura** — las cuatro modalidades alcanzan **105,1 / 105,5 / 105,65 / 106,05** de 110 motoras, spread **1,009×** — donde el modelo lineal con signo separa **98,4×** (32,15 contra 0,33).

**Y lo que sigue en pie:** `LC6→GF = 0` contra el null anatómico (predice 17,2 ± 3,1, z = −5,6) · 0/40 en 12 de 12 pares del centro de aprendizaje · Dale exacta · y del lado del motor la **ablación del gate: 21,85× a 108,11× en 4 de 4**, iso-run e iso-arquitectura, 10 semillas. **Ese último es publicable hoy y no depende de ninguna corrida nueva.**

## 5. Lo que NO hay, en orden de gravedad

**🔴 1. El código del repo no reproduce el paper.** El §2.4 del PDF declara **MS N=100** (con el detalle de los 3 lotes de 34+33+33) y **CP N=5-10**. El código hace **`NNULL = 40`** en los dos scripts. **El erratum no lo cubre y vence en 5 días.** No es un número mal escrito: **es que quien clone el repo no llega a las tablas publicadas.**

**🔴 2. El motor no está en el repo.** 113 archivos, **cero `.c`**. Se ofrece licencia dual comercial sobre algo que el repo no contiene. **Pero hoy apareció la vía:** el generador es **`esp32c.py`** y está entre los 6 `.py` que quedaron fuera de git. **No falta escribir C: falta subir el generador.** Pasa de problema a tarea de un turno.

**🔴 3. El testigo no era confiable.** Los guards impr imían rojo y salían con 0. **Arreglado hoy** — `require()` con exit 2, 28 assertions, prueba de mutación con exit 1, y CI que lo corre solo — **pero los llamadores viejos siguen sin migrar.**

## 6. La novena autorrefutación, de hoy

Dije que «el pico es lo único que este circuito no discrimina». Corrido el A/B: **el pico y el post-estímulo dan el MISMO orden** para acceso motor por modalidad (`identical_peak_vs_post = true`).

**El `sel_post` = 4,3287 sigue en pie** porque mide otra cosa: selectividad temporal entre perfiles de *looming* en el circuito de escape. **Pero el claim general queda ANGOSTADO a ese circuito y esa métrica.** Apareció corriendo, no releyendo.

---

## 7. 🎯 Eon y Rojas: qué aportaron

**La respuesta honesta: el aporte no fue de ellos.** Fue de **Betzel**, que apareció al ir a buscarlos.

### Eon Systems

| Lo que se creía | Lo medido |
|---|---|
| competidor científico | **no es un paper: es una demo.** *The Verge* publicó desmentida de framing |
| emuló el cerebro completo | se apoya en **Shiu et al. (Nature 2024)**, **que el Paper 1 ya cita** |
| su repo tiene la mosca 3D | **NO la tiene.** Es un banco de pruebas de simuladores LIF. Cero MuJoCo, cero cuerpo |
| sus números son sólidos | su repo dice **~5M sinapsis**, su sitio y la prensa **50M**. Factor 10 |

**Su aporte real:** la medida de **cuánta atención hay en el terreno** (+120M de impresiones) y la lección de que **la narrativa se la lleva quien la cuenta primero, no quien mide mejor.** Su riesgo **no es científico, es de relato.**

### Rojas Aliaga

| Hecho medido | Qué significa |
|---|---|
| Zenodo **21-mar-2026**, un día **después** | **no es prior art.** Cero riesgo de prioridad |
| su `code/` es **subconjunto del de Eon**, mismos nombres, incluido `paper-phil-drosophila` (phil = Philip Shiu, de Eon) | **deriva del repo de Eon y no lo cita** |
| abstract **139.255 / 54,5M sinapsis**, README **138.639 / 15.091.983 aristas** | **mezcla sinapsis con conexiones** |
| métrica central: «consciousness index» con Phi de IIT | ubica el rigor. Sin peer review |
| `demo.mp4` = **133 bytes** | no es un video |

**Su aporte real, y es el espejo más incómodo del día:** comete **el mismo defecto de sinapsis-vs-conexiones que el Paper 1** y publica **un repo que no contiene lo que muestra**, igual que este no contiene el motor. **La diferencia no es el rigor de la medición: es que Abraham escribió el erratum.** Eso es lo que hay que proteger.

### 🔑 El aporte que SÍ cambió algo: Betzel

Estaba en la propia lista de **NO MEDIDO ítem 7** desde el 24-ago y **ya citado en el §1.2**. Al ir a verificarlo:

- **valida el erratum** con revisión por pares y cuatro autores humanos,
- **declara como trabajo futuro** exactamente lo que el Paper 1 mide («synaptic polarity, inhibitory/excitatory distinctions», «motor neuron pathways»),
- y con **BANC** («steady-state», «unsigned quantity») son **dos grupos, dos revistas, la misma ausencia declarada: signo y transitorio.**

> **El nicho no lo define el autor: lo definen ellos, por escrito.** El párrafo está en `docs/POSICIONAMIENTO-VS-CONCURRENTES.md` y no cuesta una corrida.

**El filo del otro lado:** su peer review (28.034 caracteres, tres revisores) tiene **cero** menciones de `null`, `randomiz`, `surrogate`, `inhibitory` y `motor neuron`. **Ninguno los pidió.** El nicho está libre **y el null no es la vara del campo hoy.** Lo que SÍ pidieron — **validación experimental y análisis de sensibilidad** — este repo tampoco lo tiene.

---

## 8. Para dónde vamos

**El objetivo no cambió: que MUDH quede entregable y cedible.** Lo que hoy queda claro es **cuál es el cuello de botella, y no es científico.**

| Capa del producto | Estado |
|---|---|
| **fuente de calibración** (conectoma + priors) | medida, y ahora con respaldo externo publicado |
| **motor** (1.336 B en ESP32, gate 108×) | medido, **pero su generador no está en git** |
| **biblioteca** (el activo final) | **1 entrada de las 3-4** que hacen falta |

> **Lo que falta para que esto sea cedible es EMPAQUETADO, no descubrimiento.** Y eso es buena noticia: el empaquetado es trabajo conocido con fin a la vista.

## 9. Qué sigue

**De Abraham, y son minutos:**

1. **Subir el erratum a Zenodo.** 5 días. Único ítem con fecha.
2. **🔴 Decidir el N=100 vs 40.** O el erratum lo declara, o el repo se alinea. **Bloquea el punto 6.**
3. **Rotar el token del `HANDOFF`** de Tachi. Dos minutos; el repo es privado, no es emergencia.
4. **¿Abrir los 13 issues?** 5+ escrituras. Sin issues, ya van dos hallazgos que reaparecieron.

**De BRAIN, cuatro turnos:**

5. **Subir `esp32c.py`** → cierra «el motor no está en el repo».
6. **Migrar los llamadores** a los guards nuevos (**espera el punto 2**).
7. **Los JSON chicos y las rutas de los dos `.mjs`.**
8. **Recién después** el null anatómico por sinapsis, el único que puede **cambiar un resultado**.

**Recomendación, sin hedge:** **1 y 2 hoy.** El erratum porque tiene fecha; el N=100 porque es **lo único que puede convertir un erratum bueno en un erratum incompleto con DOI**, y un DOI no se borra.

## 10. NO MEDIDO, declarado

1. **Cero mediciones nuevas en este turno.** Todo traza a las resp 063-082.
2. **La cascada implementada NO es la de Betzel:** le faltan sus dinámicas cooperativa y competitiva, y usó **20 realizaciones contra sus 1000**. Es la familia, no el modelo.
3. **No se barrieron `p_trans` ni `N_seed`** (el *sensitivity analysis* que pidió su Revisor #3).
4. **`nulls40.json` y `dualbrain_bench.json` no están en el container** → A-04 no se cierra con lo que hay.
5. **El CI está commiteado y NO se vio correr.** K-02: deuda declarada.
6. **Los dos contextos vivos siguen desactualizados** y se nombran en vez de reescribirse de memoria.
