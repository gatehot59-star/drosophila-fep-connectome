# 056 · Tu paper: hipótesis, resultados, el descubrimiento y lo que deja abierto

**Fecha:** 2026-08-24 22:00 (America/Buenos_Aires)

> **📄 Doc de ClickUp:** «TU PAPER EN UNA HOJA · hipótesis, resultados, el descubrimiento real y la agenda»

## 1. Pedido

«Entonces mi paper, cuál es su hipótesis y resultados, cuál el descubrimiento, y qué deja para seguir investigando».

## 2. Herramientas declaradas (C-03)

| Llamada | Escribe | Cuota ajena |
|---|---|---|
| `githubmcp_get_file_contents` (contexto, resp 053b, `docs/ERRATUM.md`) | no | no |
| `githubmcp_create_or_update_file` × 1 | sí, `main` | no |
| `create_document` × 1 | sí, ClickUp | no |

**Cero mediciones nuevas.** Turno de síntesis: todo número de abajo ya estaba medido y trazado. **Nada de Kaggle, nada a Zenodo, el PDF no se tocó.**

---

## 3. LA HIPÓTESIS

El título la lleva encima: *Intermodal Isolation, Differential Motor Access, and Non-Trivial Temporal Amplification*. Son **tres** hipótesis, no una.

**La hipótesis madre, en criollo:** *el cableado por sí solo, sin aprendizaje y sin parámetros ajustados, ya decide qué información puede llegar adónde.* No es «el cerebro es una red compleja»: es que **la anatomía impone restricciones funcionales medibles antes de que exista cualquier cómputo**.

Y el corolario metodológico, que es lo que la hace testeable: **si eso es cierto, tiene que sobrevivir a nulls que preserven el grado**. Si el patrón aparece igual en una red barajada con los mismos grados, no era estructura: era conteo.

### Las tres sub-hipótesis

| # | Propiedad | En criollo |
|---|---|---|
| **P1** | Aislamiento intermodal | vías sensoriales distintas **no se contaminan** entre sí, y la inhibición cancela de forma dependiente de la profundidad |
| **P2** | Acceso motor diferencial | **no todas las modalidades llegan igual** a la salida motora |
| **P3** | Amplificación temporal no trivial | la separación entre vías **cambia con el tiempo**, y **crece después** de que el estímulo terminó |

---

## 4. LOS RESULTADOS, con el estado post-erratum

### ✅ Lo que se sostiene y es fuerte

| Resultado | Número | Contra qué |
|---|---|---|
| **Cero sensorial → Kenyon cells** | **0** en el real, los 40 nulls MS dan **1.533–2.640** | 40 nulls MS |
| **El centro de aprendizaje blindado** | **0/40 en 12 de 12 pares** | 40 nulls CP |
| **Amplificación post-estímulo (RDI dinámico)** | **z = 197** | el resultado más fuerte del expediente |
| **Jerarquía de ruteo** | spread **283×**, signo preservado 8/8, 0/40 | 40 nulls de grado |
| **Reciprocidad por circuito** (Table 7) | 41,3% intra-motor → **0,0%** óptico→motor | conteo directo |
| **Ley de Dale** | **0 mixtas de 138.005** | conteo puro |
| **`KC→MBON`, `DAN→KC`, `KC→KC`** | 7,81× · 8,71× · 7,26×, **0/40 los tres** | 40 nulls CP |
| **Circuito de escape** | 9,1× LC4→GF · **LC6→GF = 0 aristas** | 40 nulls CP |
| **Cero visual/olfatorio → motoras de cabeza** | **0** sobre 1.139.775 y 239.295 pares, y las motoras reciben 19.616 conexiones | medido el 24-ago, **nuevo, no está en el paper** |

### ❌ Lo que se cayó

- **`Density = 0.0074`** → overflow de `int32`, la real es **7,85197×10⁻⁴**.
- **«massive reciprocity 36×»** → el mismo overflow. Y aunque se corrija, **la magnitud global no es distintiva** (Lin: comparable en cinco conectomas).
- **«0 enriquecidas / 7 depletadas»** → con la densidad correcta: **4 y 4 y 1**.
- **«la topología concentra, no agrega»** → retirado, dependía del cero.
- **«cuatro modelos»** → **tres** compatibles.
- **«visual es la más depletada»** → es **olfatoria**.
- **El null CP como aporte propio** → prior art, el NPC de Lin.
- **La Tabla 8 no es reproducible**: falta el script.

**Y el que más cuesta:** el 88% de tu «población motora» son **descendentes**, porque el cordón no está en FAFB. No mediste acceso al músculo: mediste acceso al **cuello de botella descendente**. Precisa el sujeto, no lo invalida.

---

## 5. EL DESCUBRIMIENTO · uno, no diez

Si hay que quedarse con una frase:

> **El conectoma no atenuúa: prohibe. Y las prohibiciones son exactas, no gradientes.**

**Dos ceros exactos** donde la estadística dice que debería haber miles de conexiones:

| Blindaje | Cero | Qué fija |
|---|---|---|
| sensorial → KC | **0** (nulls: 1.533–2.640) | lo que el circuito **puede aprender** |
| visual / olfatorio → motoras de cabeza | **0** sobre 1,38M de pares | **sobre qué puede actuar** cada vía |

**Y el segundo cero mata la explicación fácil.** BANC propone localidad anatomómica: «las efectoras las influye lo sensorial de la misma parte del cuerpo». Pero **14 de esas motoras de cabeza salen por el nervio antenal**, el mismo por donde entran las olfatorias. **Mismo órgano, mismo nervio, cero conexiones.** Y la mecanosensorial, que está distribuida por todo el cuerpo o sea **lejos**, llega con **792**. El patrón está **invertido** respecto de lo que la localidad predice.

**El segundo hallazgo, casi igual de bueno:** la separación entre vías **crece después** del estímulo, `z = 197`. Eso solo se ve con **tiempo** y con **signo**, y es exactamente lo que BANC declara que su métrica **no** captura (steady-state, unsigned). El campo llegó a tu familia de método y **se detuvo justo antes de tu zona**.

**Lo que NO es el descubrimiento**, y confundirlo fue el error de v1.0: la reciprocidad global, la densidad, el 36×, y el null CP. Esos eran números grandes, no hallazgos.

---

## 6. QUÉ DEJA PARA SEGUIR INVESTIGANDO

### A · Lo que cierra el paper actual (barato, semanas)

1. **Null de tripartición.** Sin él la jerarquía de ruteo no se publica contra modularidad. **El CP no sirve: `sd = 0` exacto, es un espejo.**
2. **21 nulls más** para que el test global de los 12 pares llegue a `p < 0,05`. ~30 min.
3. **Re-correr todo con umbral ≥5 sinapsis**, que es lo que usan los **dos** papers de Nature. O justificar por qué no.
4. **El cero de las motoras de cabeza contra un null de grado**, y **a cuántos saltos** visual sí las alcanza. Eso convierte un cero en una **distancia de ruteo**.
5. **Buscar el script de la Tabla 8.** Aparece o la tabla queda declarada no reproducible.

### B · Las preguntas nuevas que abre, que valen papers propios

6. **¿Por qué esos ceros?** Un cero exacto sobre un millón de pares no es azar: es **desarrollo**. ¿Hay una regla de guía axonal, o un línaje, que lo explique? Eso ya no es análisis de red, es biología del desarrollo, y es la pregunta más linda del expediente.
7. **¿El blindaje es universal o de esta especie?** El cero sensorial→KC en la larva, en *C. elegans*, en cortéza de ratón. **Si aparece en tres sistemas, es un principio.** Si aparece en uno, es una mosca.
8. **La amplificación post-estímulo con signo, contra la métrica de BANC**, implementadas lado a lado. Es el único camino para decir «mi aporte es X» con un número en vez de con una lectura.
9. **¿La profundidad de cancelación inhibitoria predice latencia conductual?** Ahí hay datos publicados de comportamiento contra los que contrastar. **Sería la primera vez que esta línea toca conducta real.**
10. **De vuelta al motor:** los blindajes son **priors gratis**. Si el conectoma prohibe vías, el motor embebido **no necesita cablearlas**. Eso es compresión arquitectónica, y conecta el paper con los 1.336 B de ESP32.

### C · La deuda incontenta

11. La **décima clase** de la Tabla 5: no establecida.
12. La fila **AN**: no reproducible, declarada así.
13. **Betzel** y los dos **DOI**: sin verificar contra la fuente.
14. **¿Lin o BANC dan reciprocidad por circuito en sus suplementarios?** **Si alguno la da, se cae el único pedazo de reciprocidad que queda propio, y con él media parte B del párrafo pivote.**

---

## 7. La versión de tres líneas

- **Hipótesis:** el cableado, solo, ya decide qué llega adónde.
- **Resultado:** decide **prohibiendo**, con ceros exactos, y decide **en el tiempo**, con separación que crece post-estímulo.
- **Lo que queda:** por qué existen esos ceros, si son universales, y qué le ahorran al motor embebido.

---

## 8. NO MEDIDO, declarado

1. **Este turno no midió nada.** Es síntesis de mediciones previas, todas con su instrumento en el contexto.
2. **El cero de motoras de cabeza NO está en el paper publicado.** Es de hoy. Ponerlo en la v2 es decisión de Abraham.
3. **«z = 197» sale del doc `5977`, no se re-corrió en este turno.**
4. **El ítem 7 de la agenda (universalidad) asume que hay conectomas comparables con anotación de clase sensorial y KC-equivalente.** No verifiqué que existan.
5. **El ítem 9 (latencia conductual) asume datos publicados contrastables.** No los busqué.
6. **No verifiqué si el cero visual/olfatorio→motoras de cabeza ya lo publicó alguien.** Si sí, el descubrimiento de la §5 pasa a ser prior art ajeno.
