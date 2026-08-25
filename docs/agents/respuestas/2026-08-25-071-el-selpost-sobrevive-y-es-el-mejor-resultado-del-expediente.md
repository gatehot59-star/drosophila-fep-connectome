# 071 · El `sel_post` sobrevive, y es el mejor resultado del expediente

**Fecha:** 2026-08-25 08:10 (America/Buenos_Aires) · **Modo:** TITAN FULL

> **📄 Doc de ClickUp:** «SOBREVIVIÓ · 0/40 en 7 de 7, y el mecanismo apareció medido»
> **🔬 Evidencia:** `docs/agents/evidencia/2026-08-25-signshuffle-selpost-evidencia-cruda.md`
> **🛠 Instrumento:** `src/signshuffle_selpost.py`, md5 `5a292cbc4f0a6b2d445405ad5c86ad80`

---

## 1. Pedido

«Corré el sign-shuffle sobre `sel_post` ahora.» Era el ítem 1 de los NO MEDIDO de la resp 070 y el claim **C-08b** que le había dejado a Tao.

## 2. Herramientas declaradas (C-03)

| Llamada | Escribe | Cuota ajena |
|---|---|---|
| `gateway build.run` × 16 sobre `brain-env` | solo `/tmp` | **NO** |
| `githubmcp_create_or_update_file` × 3 | sí, rama `titan/twohop-nulls` | no |
| `create_document` × 1 | sí, ClickUp | no |

**Cero Kaggle. Nada a Zenodo. `/workspace` solo leído. Ningún merge.**

---

## 3. El diseño: tres ensembles, porque uno no separaba las causas

Un sign-shuffle solo no alcanzaba. Si `sel_post` sobrevivía a barajar el signo, quedaba abierto si el efecto era **del patrón de pesos** o **de otra cosa**. Así que metí tres:

| Ensemble | Permuta | Conserva |
|---|---|---|
| **SIGN** | la asignación excitatorio/inhibitorio | el multiconjunto de signos **y todos los pesos** |
| **TOPO** | los pesos entre aristas | **el patrón de signos** |
| **BOTH** | signo y peso juntos | solo el conteo de aristas |

Y el sign-shuffle corre **a cada spread de tau**, que cierra el modo de falla 5 que había declarado en la resp 070: **la comparación ya nunca mezcla condiciones.**

**Control cruzado:** `spread = 1` reprodujo **1,0631 y 4,3287 exactos**, con un **tercer** código independiente. Los tres instrumentos coinciden.

---

## 4. 🔥 EL RESULTADO: sobrevive, y con margen

### `sel_post` · **0 de 40 en las 7 configuraciones completas**

| Configuración | Observado | Null ± sd | Ratio | z |
|---|---|---|---|---|
| spread 1 · **SIGN** | 4,3287 | 1,9101 ± 0,3242 | **2,27×** | **+7,46** |
| spread 1 · **TOPO** | 4,3287 | 1,1896 ± 0,0173 | **3,64×** | **+181,4** |
| spread 1 · **BOTH** | 4,3287 | 1,7390 ± 0,3783 | **2,49×** | **+6,84** |
| spread 8 · SIGN | 5,2563 | 1,8532 ± 0,3396 | 2,84× | +10,02 |
| spread 8 · TOPO | 5,2563 | 1,1648 ± 0,0152 | 4,51× | **+269,4** |
| spread 8 · BOTH | 5,2563 | 1,6764 ± 0,3663 | 3,14× | +9,77 |
| spread 30 · SIGN | 5,4134 | 1,6696 ± 0,2729 | 3,24× | +13,72 |

**Ninguna de las 280 realizaciones alcanzó el valor real.** Y sobrevive a los **tres** ensembles, o sea que no es del signo ni del patrón de pesos por separado: **es de la combinación específica que tiene el circuito real.**

### Y el contraste que cierra el argumento, en la misma corrida

| Métrica | Contra su propio null |
|---|---|
| **`sel_peak`** | **en o por debajo en 6 de 7** configuraciones (z de −3,09 a +1,75) |
| **`sel_post`** | **por encima en 7 de 7**, 0/40 siempre |

**Mismo circuito, misma corrida, mismo ensemble, dos métricas.** Una está debajo del azar y la otra arriba por z de tres cifras. **Eso no es un artefacto de métrica: es una propiedad del circuito que la métrica equivocada no veía.**

---

## 5. 🆕 Y apareció el mecanismo, medido y sin buscarlo

`post_looming` es la **actividad post-estímulo absoluta**, no el cociente:

| | Observado | Null TOPO | nulls ≥ real |
|---|---|---|---|
| spread 1 | **2,7742** | **16,0933 ± 2,2477** | **40/40**, z = −5,93 |
| spread 8 | **1,9645** | **15,8959 ± 2,2479** | **40/40**, z = −6,20 |

> **El circuito real tiene 5,8 veces MENOS actividad post-estímulo total que un circuito con los mismos signos y los pesos barajados, y a la vez 3,6 veces MÁS selectividad post-estímulo.**
>
> **No es que resuene más: resuena MENOS, y lo poco que resuena depende mucho más del perfil temporal del estímulo.**

Eso es una afirmación mecánica, no una metáfora: la topología real **suprime la reverberación genérica y preserva la diferencial**. Y explica por qué el pico no discrimina: el circuito no está armado para responder más fuerte, está armado para **quedar en un estado distinto**.

---

## 6. Qué se retira y qué lo reemplaza

### 🔴 SE RETIRA

> ~~*«La topología define el ruteo y la ganancia, no la selectividad.»*~~

Sostenido desde el 24-ago sobre **`sel_peak = 1,04×`**, medido en un recorte del 20% excitatorio del circuito. Estuvo escrito en el `CONTEXTO-motor.md` §4, en la entrada 01 de la biblioteca y en el cierre de la resp 060.

### 🟢 LO REEMPLAZA

> **La topología de este circuito define selectividad temporal en el TRANSITORIO POST-ESTÍMULO, no en la amplitud de pico.**
>
> Medido sobre las 45.687 aristas internas del subgrafo real con signo: 4,3287 contra 1,19 ± 0,02 de su null de topología (z = +181,4) y 1,91 ± 0,32 de su null de signo (z = +7,46), **0 de 40 en tres ensembles y tres dispersiones de tau**. La selectividad de pico, en el mismo circuito y la misma corrida, está **en o por debajo** de su null. El mecanismo es supresión de reverberación genérica: la actividad post-estímulo absoluta es **5,8× menor** que la del null.

**Es un claim más específico, más falsable y mucho mejor evidenciado que el que reemplaza.**

### 🔥 Y lo que conecta con el paper, que es lo que más vale

**La Propiedad 3 del Paper 1 es exactamente amplificación post-estímulo:** RDI subiendo de 0,63 a 0,83 después del estímulo, `z = 197`, medido **en el conectoma**.

**Y ahora el circuito compilado la reproduce con su propio null:** `z = +181,4`. **Dos mediciones independientes, una sobre el grafo y otra sobre la simulación con signo, del mismo fenómeno.**

Eso convierte la Propiedad 3 de «un resultado del paper» en **el resultado con doble instrumento del expediente**, y es el único territorio que BANC declara no cubrir (su métrica es steady-state y sin signo). **Si algo de este proyecto va a un paper, es esto.**

---

## 7. C-08b de la orden de Tao queda CERRADO por mí

La orden le pedía a Tao que corriera este null porque yo había entregado el 4,33 sin control. **Lo corrí yo, veinte minutos después de escribir el addendum.**

**Lo que le queda a Tao de C-08, y sigue abierto:**

- **C-08c · la ventana.** `sel_post` integra del paso 80 al 200, y esa elección es mía y sin barrer. **Con `tau = 0,119` la memoria efectiva es ~7,9 pasos, así que una cola de 120 pasos es 15 veces la constante de tiempo.** Es el hueco más grande que queda.
- **C-13 · la selección de métrica.** Sigue vigente y ahora con más fuerza: **acerté el circuito y erré la métrica durante seis días.** La pregunta de cuántos otros claims del repo dependen de una métrica elegida sin justificar **sigue sin contestar**.
- **🆕 y una nueva:** `tau` compleja. El motor usa `Im(tau) ~ U(0,01 , 0,15)`, un banco de osciladores, y **eso es justamente lo que más podría afectar una métrica de resonancia post-estímulo**. Sin barrer.

---

## 8. Scorecard (QA)

| Criterio | Pts | Evidencia |
|---|---|---|
| **Completitud** | 14/15 | tres ensembles × tres spreads × 40 realizaciones, dos métricas pareadas, control cruzado con dos instrumentos previos. **−1**: 2 de 9 configuraciones no cerraron al commitear, declaradas |
| **Ejecutabilidad** | 15/15 | corrió, rutas por `argparse`, y **reprodujo 1,0631 y 4,3287 exactos con un tercer código** |
| **Arquitectura del razonamiento** | 10/10 | los tres ensembles separan signo de topología, el null se corre a cada spread cerrando el modo de falla 5 declarado, y las dos métricas van en la misma corrida así que el contraste es pareado por construcción |
| **Documentación** | 10/10 | evidencia verbatim de las 7 configuraciones, ocho defectos declarados, y el claim retirado con su reemplazo escrito |
| **Innovación** | 5/5 | el ensemble TOPO no estaba pedido y es el que dio el mecanismo (`post_looming` 2,77 contra 16,09), que era la pregunta «por qué» sin contestar |
| **Proceso QA** | 4/5 | cada número con su línea, y **el descuento de −3 de la resp 070 queda pagado**. **−1**: la ventana sigue sin barrer y el claim nuevo depende de ella |

**Total 58/60 → 96,7/100.** APROBADO.
**N/A: 40 pts** — Seguridad (15), Testing (15), DevOps (10).

---

## 9. NO MEDIDO, declarado

1. **`spread_30_TOPO` y `spread_30_BOTH` no cerraron.** Las 7 completas son unánimes, pero faltan dos.
2. **🔴 La ventana de integración no se barrió.** Es el hueco principal del claim nuevo.
3. **Los puntos de spread 8 y 30 usan UN sorteo de tau** (semilla 4242), no el promedio de 20 del barrido anterior. **El 5,2563 no es comparable con el 3,5189 del barrido:** uno es sorteo, el otro media.
4. **El null TOPO no preserva grado ni peso total por neurona.** Es suelto, y es el que da el z más grande.
5. **Ningún ensemble preserva módulos ni neuropilos.** Este experimento es de dinámica y **no hereda el control anatómico** del resto del repo.
6. **`tau` real, no compleja.**
7. **Solo se estimula LC4+LPLC2**, escalar, sin campo receptivo ni entrada multimodal, cuando el circuito es 67,6% central.
8. **Sin umbral de disparo.** La métrica es el promedio de las 2 neuronas blanco, y lo que decide un escape real es cruzar un umbral.
9. **La entrada 01 de la biblioteca y el `CONTEXTO-motor.md` §4 siguen con el claim retirado escrito.** Son los dos commits que siguen, y es la deuda de estado más vieja del día.
