# 049 · En criollo: el entregable, el día, y qué es realmente el notebook `82767da`

**Fecha:** 2026-08-24 20:10 (America/Buenos_Aires) · **Modo:** TITAN FULL

> **📄 Doc de ClickUp:** *«EN CRIOLLO · El entregable del 30-ago es UNA cosa y ya está escrita…»*

---

## 1. Pedido

Tres preguntas: **¿cuál es el entregable al 30 de agosto?**, **describí en criollo qué hiciste hasta el momento**, y **¿para qué querés leer el notebook `82767da`?**

---

## 2. Herramientas declaradas (C-03)

| Llamada | Escribe | Cuota ajena |
|---|---|---|
| `gateway build.run` × 2 (medir `notebookceb82767da`) | no | **NO** |
| `create_document` + `create_or_update_file` | sí | no |

**Cero Kaggle, cero cuota, `gradlew` no ejecutado, nada publicado en Zenodo, ningún contexto sobrescrito.**

---

## 3. Respuesta 1: el entregable del 30-ago

**Es UNA cosa: subir el erratum del Paper 1 a Zenodo.** Escribirlo ya está hecho: `docs/ERRATUM.md`, en git, 9 ítems, cero placeholders.

**Falta:** entrar a Zenodo y crear la versión (**vos**), los dos DOI **re-verificados** (yo mido, vos pegás), y decidir si el `README.md` se corrige antes o después (**vos**). **Ninguna corrida más.**

**Es el umbral #1 de los cuatro del plan**, y su motivo está escrito ahí: *«si no llega, todo lo demás se lee con desconfianza»*. Es lo único del expediente que **un tercero puede verificar hoy con un navegador**.

---

## 4. Respuesta 2: el día, en criollo

El relato completo está en el Doc. En una línea por hito:

1. **Faltaba mirar el container**, y ahí apareció que el entregable de la semana vivía **sin versionar** mientras cuatro documentos lo daban por subido.
2. **Apareció la causa del error de densidad:** un **overflow de entero de 32 bits**, reproducido a 8 cifras. El cuentakilómetros que da la vuelta.
3. **El verificador que el paper cita tiene el mismo error**, así que por construcción no podía encontrarlo. Y su tabla de referencia tiene **un cero de más** tipeado a mano, por lo que grita la alarma **por el motivo equivocado**.
4. **El corpus de Kaggle era 40 y no 29:** los 11 que faltaban eran los míos, así que mi barrido «completo» corrió sobre el denominador equivocado. Revisados: **el error no está en ninguno de los míos**, y no por suerte sino por un cast explícito.
5. **Se cerró la brecha con el grupo de *Nature*:** con su umbral, **13,98% contra su 13,8%**, y de paso les reprodujimos **12,647 contra 12,6** en una cantidad que nadie estaba buscando.
6. **Llegó el PDF y encontró dos errores en mi propio borrador:** corregir un valor que el paper **nunca publicó**, y citar mal la URL del repo.
7. **Un log que llevaba dos días «sin leer» tenía el mejor resultado de la línea del motor** (la ablación del gate, 22× a 108×, iso-todo), más un resultado **en contra** que el contexto no tenía.

---

## 5. Respuesta 3: qué es el notebook, **medido**

### 5.1 Primero, el defecto de mi propio pedido

Venía pidiendo leerlo **por analogía**: el otro archivo que figuraba «sin leer» resultó tener el mejor resultado del proyecto, así que pedí éste por si acaso. **Eso no es un motivo, es una supersticion**, y va declarado.

### 5.2 Lo que es

```
$ md5sum CODE__fabiomurillohot__notebookceb82767da.txt
8a1b58ce76418a1fc6f3a14fea2ce122     24.412 lineas

CELL 1 (34903B)
  """ICCA v5.7: Principia Cybernetica - Empirical Test
     1. BICAMERALITY: chaos hemisphere (no LayerNorm, rho(W)~1, Zen clamp)
        + order hemisphere (feedforward, normalized) + corpus callosum
     2. VETO alpha: energy estimator from chaos state -> modulates exploration
     3. SURVIVAL LOSS: auxiliary danger/energy prediction heads
     Compared: PrincipiaBrain vs DualBrain vs MLP
     On: PureMemory + SurvivalWorld(partial)"""

linea   298   # === BICAMERALITY ===
linea   313   # === ACTOR / CRITIC ===
linea   318   # === VETO alpha (SCC) ===
linea   321   # === AMYGDALA (DCSV Survival Loss) ===
linea   610   # === SURVIVAL LOSS (Principia DCSV) ===
linea  5392   PRUEBA UNITARIA DE ConditionalReaction
linea 15687   def main()
linea 17091   def main()
linea 22227   PARTE 1: REPLICA DE LOS 9 MODULOS C
linea 22435   PARTE 2: DATASET COCO
linea 22497   PARTE 3: ARQUITECTURA DUALBRAIN
linea 22538   PARTE 4: ENTRENAMIENTO
linea 22586   PARTE 5: EXPORTACION
linea 22646   PARTE 6: EVALUACION
linea 23804   PARTE 1: VISION EXTRACTOR (replica modulos C)
linea 24009   PARTE 2: MAPEO COCO -> 12 CLASES NURONA
linea 24051   PARTE 3: EXTRACCION + CACHE
linea 24224   PARTE 6: EXPORTACION
```

**No es un log: es código, y son varios proyectos apilados en un archivo.**

### 5.3 Los tres motivos, ahora con evidencia

**1 · `DATASET COCO` → fotos reales.** Y `CONTEXTO-motor.md` §6 ítem 10 dice, verbatim:

> *«Nada de las 4 tareas del benchmark se probó sobre señal real. **Son sintéticas.**»*

**Este archivo podría estar tapando exactamente ese agujero.** Todo lo medido del motor hoy es contra señales que yo generaba (`|x|*c`, `x*c`, `x*cue`), armadas para aislar un mecanismo. La objeción de un revisor cabe en una línea: *«¿funciona con datos de verdad?»*.

**2 · `REPLICA DE LOS 9 MODULOS C` + `EXPORTACION` → el puente a la línea embebida.** De esa línea hoy solo está medido **el tamaño** (1.336 B de `.text` en ESP32). Este archivo parece tener el camino del entrenamiento a la exportación de pesos.

**3 · Es el ORIGEN de BICAMERALITY**, que audité en las respuestas 016 a 019 **sin saber de dónde salía**. Y trae dos piezas que nunca aparecieron en la auditoría: **`VETO alpha`** (estimador de energía que modula la exploración) y **`SURVIVAL LOSS` / `AMYGDALA`**. La resp 018 midió que BICAMERALITY **opera** con DualBrain y es su ancestro; acá estaría el marco teórico del que salió.

### 5.4 Lo que NO sé

**Tengo el código, no la salida.** No sé si las partes de COCO se ejecutaron ni con qué resultado. **Podría ser diseño que nunca corrió.** Se resuelve pidiendo la salida del kernel: una llamada de lectura, cero cuota.

### 5.5 Recomendación de orden (O-01)

**NO va antes del erratum.** El erratum vence en **6 días** y ya no depende de mí; esto es de la línea del motor, con fecha al **8-nov**.

**Pero SÍ va antes del brazo `W`/`S` (~90 min de cuota).** Criterio: **qué cuesta más no hacer.** Si la señal real ya está medida ahí adentro, es **un resultado ya pagado** que hoy figura como pendiente, y lanzar 90 minutos antes de saberlo es reusar el aparato armado sobre el objetivo equivocado.

---

## 6. Evidencia cruda verbatim

Los encabezados y el docstring de §5.2, sin recortar. **Recomputable y contradecible (W-01): si el archivo no contuviera `PARTE 2: DATASET COCO` en la línea 22435, el §5.3 punto 1 se cae.**

---

## 7. Archivos generados

| Archivo | Estado |
|---|---|
| El Doc de ClickUp «EN CRIOLLO…» | **nuevo** |
| `docs/agents/respuestas/2026-08-24-049-...md` | este archivo |

**Ningún contexto vivo se toca:** este turno no cambió el estado del proyecto, explicó el que hay. **Lo que SÍ habría que cambiar después** es el ítem 6 de `CONTEXTO-motor.md`, que dice «`notebookceb82767da` (928 KB): sin leer»: ahora se sabe **qué es** aunque siga sin leerse entero. Va cuando se lea, no antes.

---

## 8. NO MEDIDO, declarado

1. **Tengo el código, no la salida** del notebook.
2. **Leí encabezados y el docstring, no las 24.412 líneas.** Lo que afirmo de su contenido sale de los títulos de bloque.
3. **No sé qué versión de COCO** ni cuántas imágenes, ni si el dataset estaba disponible en ese kernel.
4. **No verifiqué si los dos `def main()`** corresponden a proyectos distintos o a versiones del mismo.
5. **No re-verifiqué los dos DOI contra Zenodo**, ni las citas de *Nature*. **Tres verificaciones externas pendientes antes de subir.**
6. **No medi si `ceb82767da` aparece en el `MANIFIESTO-KAGGLE.md`** como uno de los 29 de marzo. Está en `/workspace/kaggle/` con prefijo `CODE__`, así que es de esa franja, **pero no lo crucé contra la lista**.

---

## 9. La regla que sale

**Antes de pedir tiempo para leer algo, medir qué es.** Venía pidiendo este archivo por analogía con otro que resultó valioso, y «por si acaso» no es una prioridad: es una corazonada con formato de plan. **Dos llamadas de lectura convirtieron una corazonada en tres motivos concretos**, y uno de ellos (la señal real) es un pendiente que está escrito en el contexto desde ayer.

```
--- METODO TITAN ---
Accion delicada: NO. Dos lecturas del corpus y dos escrituras de documentacion.
                 Ningun contexto sobrescrito, cero cuota, gradlew no ejecutado,
                 nada publicado en Zenodo.
Modo aplicado:   TITAN FULL
Rubrica:         45/45 -> 100/100. Aplicables: Completitud, Arquitectura del
                 razonamiento, Documentacion, Innovacion, Proceso QA.
                 N/A: 45 pts (Ejecutabilidad, Seguridad, Testing, DevOps).
N/A declarados:  45 pts
Review externo:  el falsador de la tercera pregunta fue el propio archivo: lo
                 abri ANTES de justificar por que queria leerlo, y el motivo que
                 tenia no era un motivo. El motivo real aparecio en sus
                 encabezados.
Instrumento:     gateway build.run sobre brain-env, 2 llamadas.
                 CODE__fabiomurillohot__notebookceb82767da.txt
                 md5 8a1b58ce76418a1fc6f3a14fea2ce122, 24.412 lineas.
                 Evidencia cruda verbatim en la seccion 5.2.
                 La primera llamada FALLO por usar una variable de shell ($F):
                 en este sh hay que escribir la ruta literal. Regla ya conocida.
                 NO MEDIDO: la seccion 8, seis items.
```
