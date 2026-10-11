# 2026-10-11-008 · El brazo S ya había corrido, y en el reservorio recurrente paga la sparsity, no la mosca

**Fecha:** 2026-10-11, mañana (America/Buenos_Aires).
**Doc espejo:** [El brazo S ya había corrido, y en el reservorio recurrente el cableado de la mosca empata con su shuffle 4 de 4: paga la sparsity; la neurona líquida sólo ayuda en 1 de 4 (11-oct)](https://app.clickup.com/90171457413/docs/2kza6fw5-21117) (Luz delmis tarraga's Workspace > Space > Doc).
**Corrida:** rama `titan/brazo-s-recurrente-2026-10-11`: `tools/brazo_s/` (`66fa30e`), el workflow (`670fb58`) y `results/brazo_s_recurrente_2026-10-11/`, commiteado por el propio runner (`9473852`). Run de Actions `38143998992`.

## Veredicto

**Lo corrí, y en el reservorio recurrente el cableado de la mosca empata con su shuffle en 4 de 4 tareas, con τ fija y con τ líquida. Tampoco le gana a un reservorio de ruido (0 de 4). En estas cuatro tareas paga la sparsity, no la mosca. Y la neurona líquida ayuda en 1 de 4.**

1. **Lo corrí.** El brazo S en el sustrato que nunca se había probado (el reservorio recurrente de SparseLTC, con el motivo de escape de 26 neuronas congelado) **empata con el conectoma en 4 de 4 tareas**: p de Welch 0,99 / 0,86 / 0,38 / 0,96. Con τ líquida, también 4 de 4. Y el cableado de la mosca tampoco le gana a un reservorio de ruido: 0 de 4. **En estas cuatro tareas paga la sparsity, no la mosca.**
2. **Me corrijo:** en la 007 escribí que el brazo S «nunca se corrió», y era falso. Corrió el 23-ago en Kaggle y el 2-oct en brain-env, con los mismos números, pero en un sustrato feedforward: el motivo como segunda capa de un MLP, sin recurrencia y sin τ. Ahí también empató, y en 4 de 4, no en 3 de 4 como dijo el log de agosto: su p = 0,046 era una aproximación normal; la t de Welch da 0,0646 y la permutación exacta 0,0570.
3. **Tu hipótesis existe y está escrita.** Se llama «conocimiento de existencia» en el Doc del 23-ago, que la reformuló como «competencia sin cambio de pesos», y vive como producto en `docs/agents/CONTEXTO-motor.md` §5: «funciona el primer día, sin dataset». Por partes: el aprendizaje mínimo está **sostenido como anatomía**; «apagar y prender partes según haga falta» está **sostenido como ingeniería** en la compuerta de DualBrain (21,85× a 108,11×) y **NO MEDIDO en la mosca**; «el conocimiento ya está en el cableado» **no aparece en tareas genéricas**, en ninguno de los dos sustratos.
4. **La neurona líquida no es «más que necesaria».** Sacarle la liquidez a la memoria de DualBrain (τ constante por unidad, brazo F) empata en 3 de 4 y pierde sólo en MultiCue, donde la líquida tiene 3,8 veces menos error (p de Welch 0,0011, Holm 0,0044). Sirve para integrar varias señales a la vez; en lo demás no se nota. Sobre el cableado de la mosca, la τ líquida no cambia nada: empate 4 de 4.
5. **Lo que queda vivo, y es el próximo falsador con dientes:** en MultiCue la mosca tiene 0,42 veces el error de su shuffle con τ fija y 0,65 con τ líquida. Con 10 semillas no llega a significativo (p 0,38), pero las dos corridas apuntan al mismo lado. Hay que repetir MultiCue con 50 semillas y, sobre todo, correr el brazo S en la función propia del motivo (looming → escape en lazo cerrado), que estas cuatro tareas no miden.

## 1. Pedido

«PUES CORRELO»: correr el brazo S, la misma máscara barajada con igual grado y sparsity; si S rinde como el conectoma, lo que paga es la sparsity y no la mosca. Además, buscar la hipótesis de agosto (el aprendizaje de la mosca es mínimo; al empezar a existir activa todo su conocimiento a la vez; el conocimiento está en cada neurona y la topología y el cableado hacen el resto; después apaga y prende partes según las necesite; en la emulación eso lo hacen DualBrain o DBC3 y, cuando no hace falta, se usa la parte determinista; «salió un motor»), y responder a «la neurona líquida es más que necesaria en todo esto».

## 2. Herramientas y máquina

- **ClickUp:** búsqueda y lectura de los Docs del 23-ago, 26-ago y 2-oct; creación del Doc espejo; corrección del punto 5 del Doc de la 007.
- **GitHub (MCP):** lectura de `CONTEXTO-motor.md`, `CONTEXTO-drosophila-fep.md` y la 007; creación de la rama `titan/brazo-s-recurrente-2026-10-11` desde `250b5e9`; dos pushes a la rama (código y workflow) y uno a `main` (esta respuesta y el contexto).
- **brain-env:** lectura de `/workspace/wrun/brazo_w.{py,log,json}`; `motivo26.py`, que reconstruye el motivo desde el parquet; prueba de humo de 18 celdas; validación del YAML; sondeo de la API de Actions sin token.
- **GitHub Actions x64, repo público, sin costo:** run `38143998992`, 37/37 jobs en verde (36 celdas más el agregador); torch 2.10.0+cpu, numpy 2.5.3, scipy 1.18.1; 2 hilos por celda; CPUs AMD EPYC 7763, 9V45 y 9V74 e Intel Xeon 8573C y 8370C.
- **Sandbox de ClickUp:** escritura de los scripts y auditoría de los p de agosto.
- **Kaggle:** sin uso. **Cuota ajena:** ninguna.
- **Acción delicada:** el workflow nuevo, en rama, con `contents: write` sólo en el job agregador y las actions pinneadas por SHA (checkout v7.0.1, upload-artifact v7.0.2, download-artifact v8.0.2). QA previo al push: 47/50 → 94/100.

## 3. Qué se midió

### 3.1 La hipótesis que pediste buscar: está, tiene nombre y ya se partió en piezas

**Existe, y la encontré en los dos lugares que dijiste.** En ClickUp, el 23-ago, bajo el nombre que vos le diste, «conocimiento de existencia», que en ese mismo Doc se reformuló como **«competencia sin cambio de pesos»** para que fuera falsable. En git, como producto, en `docs/agents/CONTEXTO-motor.md` §5 (24-ago): *«Que el motor deje de necesitar entrenamiento para funcionar. Topología cableada de fábrica: vía rápida por estructura (reflejo, sin memoria), vía lenta con τ heterogénea acumulando contexto, gate decidiendo cuál manda. Funciona el primer día, sin dataset»*. El «motor que salió» es ese: SparseLTC (`src/motor.py`) más DualBrain en C99 (1.336 B de `.text` en ESP32).

| Tu frase de hoy | Dónde quedó escrita | Qué se midió | Estado |
|---|---|---|---|
| «El aprendizaje de las neuronas de la mosca es mínimo» | Doc del 23-ago «el 96% NO aprende»; auditoría del 2-oct, H2 | El circuito que aprende es el 4,045% de las neuronas y el 0,41% de las conexiones; el centro de aprendizaje está blindado: 0 sinapsis sensoriales directas a Kenyon donde 40 nulos con grado exacto ponen entre 1.533 y 2.640; KC→MBON 24,25× (0/40) | **SOSTENIDA como anatomía** |
| «Con eso alcanza para funcionar: el 96% puede quedar fijo» | Docs del 23-ago (tres brazos y brazo W); `CONTEXTO-motor.md` §6.2; auditoría del 2-oct, H3 | Brazo W en agosto y el 2-oct (feedforward, §3.2). Hoy, en el reservorio recurrente: la mosca no le gana al ruido (0/4) y el reservorio fijo es peor que el react denso de agosto en 3/4 | **RETIRADA en los dos sustratos** |
| «Activa todos los conocimientos a la vez; el conocimiento ya está en cada neurona; la topología y el cableado hacen el resto» | auditoría del 2-oct, H1, H5 y H6 | Ruteo diferencial 0/40 en las 12 clases; reciprocidad 47,27× sobre el nulo de grado (0/40); persistencia post-estímulo sel_post z = +181 contra el nulo de topología. Hoy: el cableado empata con su shuffle 4/4, con τ fija y con τ líquida | **SOSTENIDA como estructura; sin señal funcional en tareas genéricas** |
| «Apaga partes de neuronas según las necesite y las vuelve a activar» | auditoría del 2-oct, H4; Doc «En criollo: qué hicimos con H4» | H4 débil: los perfiles de escape, acicalado y alimentación salen casi idénticos (coseno 0,999786 a 0,999845); H4 fuerte: en Aymanns, bajo CO2 sólo hubo reposo y caminata, sin acción alternativa | **H4 débil refutada; H4 fuerte NO MEDIDA** |
| «En nuestra emulación eso lo hace DualBrain o DBC3; cuando no se necesita, se usa la parte determinista» | `CONTEXTO-motor.md` §0.bis; Doc del 26-ago «el gate es explorar/explotar (108× medido)» | Ablación de la compuerta: 21,85× a 108,11× en 4/4 tareas, iso-run e iso-arquitectura | **SOSTENIDA como ingeniería**; no dice que la mosca use ese mecanismo |
| «La neurona líquida es más que necesaria en todo esto» | 007 y `CONTEXTO-motor.md` §4 | Antes de hoy: SparseLTC empata 48/48 con un control lineal; τ compleja p = 0,60; una LTC sola pierde contra DualBrain en las 4 tareas (9,49× a 500,98×). Hoy: la memoria sin liquidez (F) empata con la líquida en 3/4 y pierde sólo en MultiCue (3,8×); sobre el cableado de la mosca, empate 4/4 | **NO en 3 de 4; útil para integrar varias señales** |

**Una contradicción entre fuentes, y quién tiene razón.** La auditoría del 2-oct dice que H3 quedó refutada porque «el experimento corregido W/S sí probó el sujeto correcto». `CONTEXTO-motor.md` (24-ago) dice lo contrario: que el brazo W «no refuta la hipótesis: nunca la testeó». Leí `brazo_w.py` línea por línea y tiene razón el contexto del motor: la matriz del motivo entra como `react[2]`, la segunda capa de un MLP feedforward (`Linear → Tanh → Linear(W) → Tanh`), aplicada una vez por paso, sin recurrencia y sin τ. El motivo tiene 54 de sus 88 aristas recíprocas y ahí no se usan como lazo: se usan como una mezcla lineal de un salto. **Por eso hoy corrí la versión recurrente.**

**Fuentes de la hipótesis:**

- [Tu hipótesis… el 96% NO aprende (23-ago)](https://app.clickup.com/90171457413/docs/2kza6fw5-3937/2kza6fw5-5917)
- [40 nulls: el centro de aprendizaje blindado (23-ago)](https://app.clickup.com/90171457413/docs/2kza6fw5-3957/2kza6fw5-5937)
- [Tres brazos (23-ago)](https://app.clickup.com/90171457413/docs/2kza6fw5-4157/2kza6fw5-6137)
- [Brazo W terminó (23-ago)](https://app.clickup.com/90171457413/docs/2kza6fw5-4317/2kza6fw5-6297)
- [El gate es explorar/explotar, 108× medido (26-ago)](https://app.clickup.com/90171457413/docs/2kza6fw5-5777/2kza6fw5-7717)
- [Auditoría por hipótesis (2-oct)](https://app.clickup.com/90171457413/docs/2kza6fw5-17057/2kza6fw5-19637)
- [En criollo: qué hicimos con H4 (2-oct)](https://app.clickup.com/90171457413/docs/2kza6fw5-17517/2kza6fw5-20097)

### 3.2 El brazo S ya había corrido dos veces: me corrijo

**En la 007 escribí que el brazo S «está diseñado desde agosto y nunca se corrió». Es falso.** Corrió el 23-ago en Kaggle (`abrahammendieta/titan-brazo-w`, 122,3 min) y se re-corrió el 2-oct en brain-env (`/workspace/wrun/brazo_w.py`, md5 `ebf757df2d925420faa43082ad9d30c3`, 558,6 min), con los mismos números a seis decimales. Lo que nunca corrió es el S en el sustrato que pide `CONTEXTO-motor.md` §6.2. Mi frase confundió las dos cosas. La 007 es append-only y no se edita: la corrección vive acá, en el contexto y en el punto 5 del Doc de la 007.

Lo que dio, con las semillas crudas del 2-oct (`/workspace/wrun/brazo_w.json`, md5 `690052d9b356c0896ee99c39f46c237c`):

| Tarea | W | S | B | W contra S | W contra B |
|---|---|---|---|---|---|
| Gated | 0,006297 | 0,002626 | 0,001393 | indistinguibles | W peor (p_welch 0,036) |
| LinScale | 0,000298 | 0,000227 | 0,000205 | indistinguibles | W peor (p_welch 0,016) |
| MultiCue | 0,000223 | 0,000199 | 0,000215 | indistinguibles | indistinguibles |
| CR | 0,000432 | 0,000433 | 0,000574 | indistinguibles | indistinguibles |

**Y un error de ese instrumento que nadie había marcado:** el log de agosto dice que en LinScale W y S «difieren» (p = 0,046). Ese p sale de una aproximación normal (`erfc(|t|/√2)`) con 10 semillas por brazo. Con la t de Welch de verdad (df 15,1) da **p = 0,0646**, y la permutación exacta de las 184.756 particiones da **p = 0,0570**. **W y S son indistinguibles en 4 de 4, no en 3 de 4.**

### 3.3 El brazo S en el reservorio recurrente, que nunca se había corrido

- **Sujeto exacto (E-01):** el mismo motivo de escape del brazo W, 26 neuronas (8 LC4, 8 LPLC2, 4 LC6, 2 GF y 4 DNp09), 88 aristas, 54 recíprocas y **ninguna inhibitoria**. `motivo26.py` lo reconstruyó en brain-env desde el parquet pinneado (md5 `3d802fd542b5d18570ba1ba0bb0abed9`) con la selección copiada de `brazo_w.py`, y la matriz normalizada dio **diferencia 0,000e+00** contra la que guardó el brazo W.
- **Sustrato:** la vía react deja de ser un MLP y pasa a ser el reservorio de SparseLTC, `z ← (1 − τ)·z + τ·tanh(W·z + U·x)`, con W llevada a radio espectral 0,9 (igual que el brazo W) y U, W y τ congeladas. τ fija y heterogénea, una por neurona, en [0,06; 0,18] alrededor del 0,119 del motor, la misma para todos los brazos.
- **El brazo S:** el shuffle de grado de entrada y de salida exacto, con los mismos pesos permutados entre aristas, **uno distinto por semilla**. La semilla 0 es exactamente el S del brazo W (diferencia 0,0; 1.395 intercambios); las otras nueve son shuffles nuevos, así el nulo no depende de un solo grafo al azar.
- **Brazos (10 semillas cada uno, las mismas para todos):** `A` techo y `B` react denso congelado, que tienen que reproducir agosto; `RB`, `RW` y `RS`, el reservorio con ruido, con la mosca y con su shuffle; `LB`, `LW` y `LS`, lo mismo con τ líquida (depende de la entrada y del estado, también congelada); y `F`, la memoria de DualBrain con τ constante por unidad.
- **Todo lo demás, copiado verbatim de `brazo_w.py`** y verificado como texto idéntico: las 7 funciones del motor y de las tareas y el dict `TAREAS`. Mismo entrenamiento (Adam 1e-3, batch 64, 2000 pasos, clip 1,0) y misma evaluación (2000 secuencias). En RB a LS se entrenan los mismos 619 o 627 parámetros que en B, W y S de agosto; F entrena 128 menos que A.
- **Reglas escritas antes de correr** (docstring de `tools/brazo_s/agregar.py`): decide la t de Welch con p ≤ 0,05 por tarea, y se reportan además Holm, la permutación exacta y la aproximación normal de agosto. C1: si RW no le gana a RB en al menos 3 de 4, la analogía del 96% fijo se retira también acá. C2 y C3, el brazo S: gana en ≥ 3/4, «la mosca paga»; empata en ≥ 3/4, «paga la sparsity, no la mosca». C6: la neurona líquida es necesaria en la memoria si A le gana a F en ≥ 3/4.

**Error cuadrático medio, media de 10 semillas (menor es mejor):**

| Tarea | A | B | RB | RW | RS | LB | LW | LS | F |
|---|---|---|---|---|---|---|---|---|---|
| Gated | 0,000236 | 0,001393 | 0,021557 | 0,021818 | 0,021768 | 0,018392 | 0,019249 | 0,018618 | 0,000266 |
| LinScale | 0,000055 | 0,000205 | 0,000494 | 0,000554 | 0,000564 | 0,000516 | 0,000569 | 0,000625 | 0,000061 |
| MultiCue | 0,000098 | 0,000215 | 0,002664 | 0,001050 | 0,002502 | 0,003156 | 0,001551 | 0,002380 | 0,000374 |
| CR | 0,000040 | 0,000574 | 0,000649 | 0,000664 | 0,000668 | 0,000623 | 0,000666 | 0,000653 | 0,000071 |

**Contrastes:**

| Contraste | Qué pregunta | Resultado |
|---|---|---|
| C1 · RW contra RB | ¿el cableado de la mosca le gana a un reservorio de ruido? | 0 de 4 (p 0,22 a 0,95): la analogía del 96% fijo se retira también en el sustrato recurrente |
| **C2 · RW contra RS** | **el brazo S** | **empate 4 de 4** (p 0,99 / 0,86 / 0,38 / 0,96): paga la sparsity, no la mosca |
| C3 · LW contra LS | el brazo S con τ líquida | empate 4 de 4: paga la sparsity |
| C4 · LW contra RW | ¿la τ líquida mejora el cableado de la mosca? | empate 4 de 4 |
| C5 · LS contra RS | ¿y el del shuffle? | empate 4 de 4 |
| C6 · A contra F | ¿la memoria necesita ser líquida? | gana en 1 de 4 (MultiCue, 0,263×, p 0,0011, Holm 0,0044), empata 3, pierde 0 |
| C7 · RW contra B | ¿el reservorio fijo con la mosca mejora el react denso de agosto? | peor en 3 de 4 (Gated 15,7×) |
| C8 · RB contra B | ¿la recurrencia sola mejora? | peor en 2 de 4 |

**Cuánto error tiene la mosca respecto de su shuffle** (Gated / LinScale / MultiCue / CR): RW/RS = 1,002 / 0,984 / 0,420 / 0,993; LW/LS = 1,034 / 0,911 / 0,652 / 1,020.

**Reproducción de agosto:** A y B coinciden con la corrida del 2-oct a seis decimales en la media; la diferencia relativa máxima por semilla va de 2,9e-06 a 6,2e-05. El agregador imprimió «NO REPRODUCE EXACTO» porque su umbral era 1e-6: reproduce en la media, no bit a bit.

**En criollo:** en las cuatro tareas del banco de agosto, el motivo de escape con su cableado real rinde igual que el mismo motivo con las aristas barajadas, y que un reservorio de ruido. En este banco, la mosca no aporta nada que no aporte cualquier grafo igual de ralo. Esto no refuta que el motivo sirva para lo suyo: estas tareas no son escapar de algo que se acerca.

### 3.4 La neurona líquida, medida por primera vez dentro de la memoria

- **A contra F:** la memoria de DualBrain con τ líquida contra la misma con τ constante por unidad. Empate en Gated, LinScale y CR; la líquida gana sólo en MultiCue, con 0,263 veces el error (p de Welch 0,0011, Holm 0,0044).
- **τ líquida en el reservorio:** LW contra RW y LS contra RS, empate 4 de 4 en los dos. Sobre el cableado de la mosca la liquidez no agrega nada.
- **Ojo con la capacidad:** F entrena 128 parámetros menos que A. Aun con esa ventaja para A, gana en 1 de 4. Que lo de MultiCue sea liquidez y no capacidad queda NO MEDIDO.
- **Lectura:** la liquidez es una herramienta para una clase de tarea (integrar varias señales con distinto ritmo), no un pilar. Lo que pagó en todo lo medido sigue siendo la compuerta (21,85× a 108,11×) y la memoria de DBC3 (AULC 0,823 contra 0,635).

## 4. Evidencia cruda

- **Log crudo, escrito y commiteado por el runner:** `results/brazo_s_recurrente_2026-10-11/run.log`, con `resultados.json`, `celdas/*.json` y `celdas/*.log`, en la rama `titan/brazo-s-recurrente-2026-10-11`, commit `9473852`. El texto de un log de Actions no se puede leer desde afuera; por eso el workflow commitea su propio resultado.
- **Líneas de veredicto del `run.log`, verbatim** (el original va sin tildes):
  - C1: `La analogia del 96% fijo se retira tambien en el sustrato recurrente` (0/4)
  - C2 y C3: `PAGA LA SPARSITY, NO LA MOSCA` · `indistinguibles en 4/4`
  - C6: `LA NEURONA LIQUIDA NO ES NECESARIA` · `gana solo en 1/4 (empata 3, pierde 0)`
  - Reproducción: `NO REPRODUCE EXACTO`
- **Motivo:** `motivo26.py` en brain-env, exit 0, `VEREDICTO_MOTIVO=OK`; 88 aristas, 54 recíprocas, 0 inhibitorias, radio crudo 17,6597; `max|W - W_brazo_w| = 0.000e+00`.

| Artefacto | md5 |
|---|---|
| `tools/brazo_s/brazo_s_recurrente.py` (448 líneas) | `f8b10037e70dfe897ff2d841077419b4` |
| `tools/brazo_s/agregar.py` (270 líneas) | `8ae0b7fab0247d72596d8d29fb276324` |
| `tools/brazo_s/referencia_brazo_w.json` (8.395 B) | `a04e677325b662f2f4c38bb8fdf8bf00` |
| `tools/brazo_s/motivo26.py` | `e1ef2cee497b5ccc796d1299f03200a6` |
| `motivo26.json` (salida en brain-env) | `eb6e53e047c864a46c56bf38b397d289` |
| `.github/workflows/brazo-s-recurrente.yml` | `075a200ae3e10d249301215ee6a70ec2` |
| `/workspace/wrun/brazo_w.py` (agosto) | `ebf757df2d925420faa43082ad9d30c3` |
| `/workspace/wrun/brazo_w.json` (2-oct) | `690052d9b356c0896ee99c39f46c237c` |
| `/workspace/connectivity.parquet` | `3d802fd542b5d18570ba1ba0bb0abed9` |

## 5. Archivos generados

- **En `main`, en este commit:** esta respuesta y `docs/agents/CONTEXTO-drosophila-fep.md` actualizado.
- **En la rama `titan/brazo-s-recurrente-2026-10-11`:** `tools/brazo_s/` (`66fa30e`), `.github/workflows/brazo-s-recurrente.yml` (`670fb58`) y `results/brazo_s_recurrente_2026-10-11/` (`9473852`, del runner). Sin PR.

## 6. NO MEDIDO

- **El brazo S en la función propia del motivo:** looming → escape en lazo cerrado. Las cuatro tareas son genéricas, así que este experimento no podía dar rojo por «el motivo de escape sirve para escapar».
- **MultiCue con más semillas:** la tendencia 0,42× (τ fija) y 0,65× (τ líquida) no está firmada.
- **Un S que conserve Dale por neurona:** este motivo no tiene aristas inhibitorias, así que acá el signo no se puso a prueba.
- **SparseLTC completo** (138.639 neuronas) como reservorio: medido sólo el motivo de 26.
- **La τ propia de DBC3:** el brazo F mide la `LiquidCell` de DualBrain, no la memoria de DBC3.
- **F con los mismos parámetros que A:** F entrena 128 menos.
- **H4 fuerte en la mosca:** sigue NO MEDIDA.
- **Reproducción bit a bit de agosto:** reproduce en la media, no bit a bit.
- **Review externo:** no hay PR; nadie ajeno eligió qué medir.
- **`CONTEXTO-motor.md`** sigue sin reescribir; sus §1, §4 y §6.2 quedan superados por esta respuesta.

## Antes de firmar

| Afirmación | Instrumento | ¿Podía dar rojo? | Veredicto |
|---|---|---|---|
| paga la sparsity, no la mosca (4 tareas) | Welch por tarea, 10 semillas, regla previa | sí: ≥ 3/4 a favor de RW era «la mosca paga», y el mismo agregador sí vio la diferencia de C6 | medido |
| la neurona líquida no hace falta en 3/4 | A contra F, Welch y Holm | sí, y dio rojo en MultiCue | medido |
| el sujeto es el motivo del brazo W | diff de la matriz | sí | medido (0,000e+00) |
| el RS de la semilla 0 es el S de agosto | diff de la matriz | sí | medido (0,0) |
| A y B reproducen agosto | `referencia_brazo_w.json`, umbral 1e-6 | sí, y dio rojo bit a bit | medido: a seis decimales en la media |
| la mosca no aporta en su propia función | este banco | no | NO MEDIDO |
| empate es equivalencia | Welch con 10 semillas | no | NO MEDIDO |

## QA

Entrega mixta (instrumento ejecutado más reporte). Aplicables 60 puntos; N/A 40: Seguridad 15 (sin superficie nueva fuera del workflow, auditado antes del push), Testing 15 (no hay suite; los controles son A y B reproduciendo agosto) y DevOps 10.

| Criterio | Puntos | Evidencia |
|---|---|---|
| Completitud | 14/15 | seis campos, 36 celdas, C1 a C8; −1: el md5 del `run.log` no está citado acá (el archivo está en la rama) |
| Ejecutabilidad | 14/15 | 37/37 jobs en el run `38143998992` y humo 18/18; −1: el umbral de reproducción del agregador es más estricto que lo que permite cambiar de CPU |
| Arquitectura del razonamiento | 9/10 | sujeto exacto (diff 0,0) y reglas escritas antes de correr; −1: el banco no incluye la función propia del motivo |
| Documentación | 9/10 | git, Doc y contexto; −1: `CONTEXTO-motor.md` sin reescribir |
| Innovación | 4/5 | brazos L y F, auditoría de los p de agosto, un S distinto por semilla |
| Proceso QA | 5/5 | cada puntaje con archivo, commit o run |
| **Total** | **55/60 → 92/100** | aprobado con deuda: sin review externo y sin la función propia del motivo |

## Qué espera decisión de Abraham

1. Repetir MultiCue con 50 semillas en Actions (gratis, el mismo workflow): decide si la ventaja 0,42× de la mosca es real.
2. Correr el brazo S en la función propia del motivo: looming → escape en lazo cerrado, enganchado al instrumento de la 007.
3. Reescribir `CONTEXTO-motor.md`.
4. Abrir PR de `titan/brazo-s-recurrente-2026-10-11` y `titan/swarm-lazo-cerrado-2026-10-11`, y pedir review.
5. Lo pendiente de la 007: el parche de lectura de `swarm/` y BEEC v2 como norte.

--- METODO PROMETEO ---
Acción delicada: NO (bitácora y contexto a main; el workflow, delicado, se auditó antes del push en 670fb58: 47/50 -> 94/100)
Modo aplicado:   TITAN FULL
Rúbrica:         55/60 -> 92/100
N/A declarados:  40 (Seguridad 15, Testing 15, DevOps 10)
Review externo:  no pedido: no hay PR (deuda)
Instrumento:     GitHub Actions run 38143998992, 37/37 jobs OK; evidencia cruda commiteada por el runner en results/brazo_s_recurrente_2026-10-11/ (rama titan/brazo-s-recurrente-2026-10-11, 9473852)
Máquina:         Actions x64 (corrida) + brain-env (motivo26.py, humo de 18 celdas, YAML) + sandbox de ClickUp (scripts, auditoría de los p)
Artefactos:      docs/agents/respuestas/2026-10-11-008-el-brazo-s-ya-habia-corrido-y-en-el-reservorio-recurrente-paga-la-sparsity-no-la-mosca.md + https://app.clickup.com/90171457413/docs/2kza6fw5-21117
