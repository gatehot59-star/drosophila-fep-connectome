# 064 · En criollo: qué fue la entrega del null anatómico

**Fecha:** 2026-08-25 00:50 (America/Buenos_Aires)

> **📄 Doc de ClickUp:** «EN CRIOLLO Y DETALLADO · qué pasó en la entrega del null anatómico»
> **🔬 Los números:** `docs/agents/evidencia/2026-08-24-null-anatomico-evidencia-cruda.md`

## 1. Pedido

«En criollo y detallado explica la entrega anterior.»

## 2. Herramientas declaradas (C-03)

Ninguna medición nueva. Es explicación de la resp 063. **Cero Kaggle, nada a Zenodo, nada borrado.**

---

## 3. Arranquemos por el problema, porque sin eso el resto no se entiende

Hace unos días medí algo que parecía enorme: **las neuronas visuales y olfativas no tienen ni una sola conexión con las motoras de la cabeza.** Cero. Sobre más de un millón de pares posibles.

Y dije: esto es un blindaje estructural, el cerebro **prohíbe** que la vista mande al músculo directamente.

**El problema de decir eso es que "cero" solo, sin comparación, no significa nada.** Necesitás saber **cuánto debería haber**. Y para eso se usa un *null*: barajás el cerebro al azar, pero conservando alguna propiedad, y mirás qué pasa. Si en el cerebro barajado aparecen 70 conexiones y en el real hay 0, ahí sí tenés algo.

**Ahí está toda la pelea de anoche: QUÉ conservás cuando barajás.**

---

## 4. El primer null, el de grado, y por qué me dio un resultado espectacular y equivocado

El null de **grado** conserva cuántas conexiones tiene cada neurona, pero manda esas conexiones **a cualquier parte del cerebro**.

Con ese null los números fueron gigantes:

| Clase | Real | Lo que predice el null | Veredicto |
|---|---|---|---|
| olfatorio | 901 caminos | 39.522 | **43× menos** |
| visual | 1.413 | 23.311 | **16× menos** |
| mechano | 293.022 | 39.787 | **7× más** |
| gustativo | 67.439 | 10.304 | **6× más** |

Diferencia entre extremos: **323 veces**. Un resultado de portada.

### Pero ese null tiene un defecto que yo mismo escribí en las Limitations

Barajar «a cualquier parte del cerebro» es **físicamente imposible**. Una neurona no puede conectar con algo que está lejos y que no toca. Las neuronas olfativas terminan **solo en el lóbulo antenal**; las de la vista, **solo en lámina y médula**. Eso es anatomía de libro de texto de hace 25 años.

Entonces ese null predice conexiones que **no podrían existir nunca**, y contra esa expectativa inflada **cualquier restricción física parece un descubrimiento**.

Y yo lo sabía: lo escribí en el texto, con número. En el paper de Lin, pasar de un null de grado a uno que respeta anatomía **se come el 84% del efecto**. Escribí «no se puede descartar una reducción comparable acá» y seguí.

---

## 5. La parte que más me molesta: dije que no se podía medir, y se podía

Durante días el contexto decía: **el null anatómico NO es testeable**, porque la tabla de anotaciones que tengo tiene 31 columnas y ninguna dice en qué región vive cada neurona.

Eso era cierto **sobre ese archivo**. Y yo lo convertí en «no se puede», que es otra cosa.

Lo busqué en serio y estaba a **una llamada**: en Zenodo, en el mismo paquete público del release 783, sin login, hay dos archivos que dicen exactamente eso, neurona por neurona. **79 regiones**, y de 138.639 neuronas solo 283 quedan sin asignar.

**Un límite de un archivo no es un límite del entorno.** Esa es la falla y está anotada como tal.

---

## 6. El segundo null, el anatómico, y qué hace distinto

Este baraja **solo dentro del mismo par de regiones**. O sea: una conexión que iba del lóbulo antenal al ganglio gnatal, al barajar **sigue yendo del lóbulo antenal al ganglio gnatal**, pero a otra neurona de ahí.

En criollo: **el null viejo permitía mudanzas a cualquier barrio de la ciudad. El nuevo solo permite cambiar de casa dentro del mismo barrio.** Y ese es el control correcto, porque es el que responde la pregunta que importa: dado que estas dos regiones se hablan tanto, ¿esta vía en particular está más o menos conectada de lo esperable?

Es la misma familia que el modelo NPC de Lin, que se publicó en Nature.

---

## 7. 🔴 El resultado: se cayó, y no de a poco

| Clase | Null de GRADO | Null ANATÓMICO | Qué pasó |
|---|---|---|---|
| olfatorio | 0,023 (43× menos) | 0,368 | sobrevive el signo, pero **16 veces más débil** |
| visual | 0,061 (16× menos) | **1,53 (MÁS de lo esperado)** | **se dio vuelta** |
| mechano | 7,36 (más) | **0,80 (MENOS)** | **se dio vuelta** |
| gustativo | 6,54 (más) | **0,63 (MENOS)** | **se dio vuelta** |

**Tres de cuatro cambiaron de signo. El spread de 323× quedó en 2,4×.** Y pasó igual con umbral de 5 sinapsis, así que no es un artefacto de cómo conté las conexiones.

**Y hay un detalle que es la prueba más limpia de que el problema era mío:** yo había reportado como hallazgo que el cerebro real tiene «menos caminos de dos saltos que un grafo al azar», un factor de 0,652. Contra el null anatómico eso da **1,010**. O sea **exactamente lo esperado**. Ese «hallazgo» era, íntegramente, el efecto de que las conexiones respetan regiones.

---

## 8. Por qué se cayó, y esto lo pude medir

Mi argumento central era: *«la localidad no puede explicar 323×, porque las cuatro clases son todas locales y todas entran por nervios de la cabeza».*

Medí dónde vive cada una:

```
MOTORAS de la cabeza:  GNG 89,  PRW 15,  IPS 5,  FLA 1
mechanosensorial:      GNG 1712, SAD 468, AMMC 406
gustativo:             GNG 353,  PRW 52
olfatorio:             lóbulo antenal (AL) 2276
visual:                lámina 8086, médula 2622
```

**104 de las 110 motoras viven en GNG o PRW. Mechanosensorial y gustativa también.**

O sea: **dos de las cuatro clases comparten dirección con las motoras y dos no.** No eran «todas igual de locales». Ni parecido.

Mi frase no era floja: **era falsa**, y falsa por algo que podía medir en cinco minutos y no medí. Escribí «todas locales» sin verificar **dónde**.

Y encima, esto le da la razón a BANC, el paper de Nature de junio. Ellos dicen que los efectores reciben influencia sobre todo de sensores **de la misma parte del cuerpo**. A escala de región, esa explicación **gana**. Yo había cantado que la refutaba.

---

## 9. 🟢 Y acá está lo bueno, que es mejor que lo que perdí

Cuando controlás por la región, la pregunta interesante **se da vuelta**. Ya no es «por qué la vista no llega», porque la vista no llega por geometría y el null lo predice exactamente.

La pregunta buena es: **¿y las que SÍ están en el mismo barrio que las motoras, conectan?**

| Clase | Conexiones directas a motoras | Lo que predice su propia ubicación | z |
|---|---|---|---|
| **gustativo** | **10** | **101,6** | **−78,9** |
| **mechanosensorial** | **64** | **98,6** | **−21,7** |

Con umbral de 5 sinapsis es todavía más nítido: **gustativa conecta con 2 motoras donde su ubicación predice 91.**

**En criollo: las neuronas del gusto entran al mismo barrio donde viven las motoras, pasan literalmente por la puerta, y no golpean. Conectan con diez cuando deberían conectar con cien.**

Eso es un resultado de verdad, porque **sobrevive al null más fuerte que existe para este dato**, con un z de −79. Y no lo podía ver ninguna de las dos versiones anteriores del análisis, porque el null de grado lo tapaba: contra grado, gustativa aparecía **enriquecida**.

**El enunciado nuevo:** el cero de la vista y el olfato es **geometría**. El blindaje real está en las vías que tienen la oportunidad de conectar y no la usan.

---

## 10. Dos cosas más que salieron y no son menores

**El umbral de 5 sinapsis no es cosmético.** Sin umbral, el estadístico de «a cuántas motoras llega» era inservible: los 40 barajados llegaban a las 110 y el desvío daba cero exacto. Con umbral el desvío es 1,04 y el estadístico **funciona**: olfatorio llega a 1 de 109 donde se esperan 107. O sea, **adoptar el criterio del campo no es solo alinearse con los tres papers de Nature, es técnicamente mejor.**

**Y ahora hay un solo instrumento en vez de tres corridas sueltas.** Un script que recomputa todo desde los datos crudos, con las rutas por argumento (así corre en la máquina de cualquiera, que era un defecto declarado de los scripts del release), que vuelca las 40 realizaciones de cada ensemble a JSON y que **genera las tres figuras**. Y de paso reprodujo exactamente los números de las corridas anteriores, que estaban escritos con otro código: eso es una verificación cruzada gratis.

---

## 11. Y un error mío de método, del mismo día

En la corrida de ayer imprimí un chequeo de grado que **se comparaba contra sí mismo**. Da verde siempre. Es un test que no puede fallar, o sea el modo de falla que este proyecto tiene documentado y numerado, **cometido en el mismo turno en que lo estaba citando**.

En el instrumento nuevo eso está arreglado: el guard tiene control positivo **y negativo** (el método malo rompe el grado en 138.142 de 138.639 neuronas, así que el test puede dar rojo), y además metí adentro de la misma corrida **una cantidad que el null no puede tocar**, para demostrar que el estadístico principal no es un espejo, en vez de argumentarlo.

---

## 12. El saldo honesto

**De las dos horas anteriores sobreviven todas las mediciones y se cae la interpretación principal, que era mía.** Es el quinto claim mío de causa o de novedad que muere en el día, y los cinco tienen la misma forma: **medir bien, y después afirmar POR QUÉ sin medir el por qué.**

Y lo que salvó el turno fue **haber escrito la limitación con un número**. Si en vez de «falta el control anatómico, y en Lin ese control se come el 84%» hubiera puesto «hacen falta más controles», nadie lo iba a correr, y esto se iba a la v2 del paper.

**No lo mergeé.** Está en una rama con su PR, con la rúbrica y con el review automático pedido. El merge es tuyo, porque aceptarlo es aceptar que el 323× no se publica como jerarquía de ruteo.

---

## 13. Lo que queda pendiente, declarado

1. **El NPC exacto de Lin**, que asigna por sinapsis y no por región dominante de cada neurona. El mío es la misma familia, no idéntico.
2. **Un null combinado** que preserve grado **y** región a la vez. Es el control que sigue.
3. **El null por distancia física.** Los datos están en la tabla que ya tengo y no los usé.
4. **Para la vista y el olfato, el null anatómico predice casi exactamente cero**, así que esas dos filas quedan **NO TESTEABLES** contra él, no refutadas.
5. **El hallazgo nuevo de gustativa no lo barrí contra la literatura.** Si ya está publicado, pasa a ser de otro, y ese es exactamente el error que esta entrega corrige.
6. **El cero de LC6 hacia el Giant Fiber** del circuito de escape sigue sin testear contra regiones, y ahora se puede con estos mismos datos. Es la deuda más barata que queda.
