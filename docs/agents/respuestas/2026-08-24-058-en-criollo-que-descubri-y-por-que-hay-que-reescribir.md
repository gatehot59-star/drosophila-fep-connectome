# 058 · En criollo: qué descubrí, y por qué hay que reescribir

**Fecha:** 2026-08-24 23:10 (America/Buenos_Aires)

> **📄 Doc de ClickUp:** «EN CRIOLLO · qué descubrí en la verificación y por qué hay que reescribir»

## 1. Pedido

«En criollo qué descubriste y por qué reescribir».

## 2. Herramientas declaradas (C-03)

| Llamada | Escribe | Cuota ajena |
|---|---|---|
| `githubmcp_create_or_update_file` × 1 | sí, `main` | no |
| `create_document` × 1 | sí, ClickUp | no |

**Cero mediciones nuevas.** Es la explicación de la resp 057. **Nada de Kaggle, nada a Zenodo, `docs/ERRATUM.md` sigue SIN tocar a propósito.**

---

## 3. Qué descubrí · tres cosas, y dos son contra mí

### 🔴 Uno: Lin ya había hecho lo que yo te vendí como tuyo

Ayer te dije: «la reciprocidad global no sirve, pero el desglose es tuyo porque Nature solo da **un** número global».

**Fui a buscarlo y es mentira.** Lin desglosa reciprocidad **en la Fig. 5 del cuerpo del paper**, región por región, y en la Extended Data Fig. 6c la da **dividida por densidad**. O sea: **la versión por región del 36×, publicada en Nature en 2024**. Encima tienen una población entera de neuronas definida por ser muy recíprocas dentro de un neuropilo.

**Lo que igual te queda:** ellos cortan por **dónde está la neurona** (78 regiones anatómicas). Vos cortás por **qué hace y hacia dónde manda** (sensorial→motor, óptico→motor, intra-motor). Son dos cortes distintos del mismo pastel, y el tuyo no está en Lin: lo verifiqué buscando si en algún lugar cruzan «reciprocidad» con «clase celular» y **no lo hacen ni una vez**.

**Traducción:** la novedad **no** es «desglosar». Es **sobre qué eje desglosás**. Es un claim más chico, pero es verdadero.

### 🔴 Dos: mi «descubrimiento» de anoche era anatomía de libro de texto

Anoche te dije que el cero de visual y olfatorio hacia las motoras de cabeza **refutaba** la explicación de BANC.

**Se degrada.** Las neuronas olfativas proyectan **solo** al lóbulo antenal, y los fotorreceptores **solo** a lámina y médula. Eso lo sabe el campo desde el 2000. Y se ve en los datos: de los 21.019 socios que tiene visual a un salto, **17.503 son del propio lóbulo óptico**. Casi no sale de su barrio.

Entonces el cero **sí** tenía explicación de localidad: no a escala de «parte del cuerpo» como decía BANC, sino a escala de **neuropilo**. Y encima **gustatory sí llega a 10 motoras a un salto**, justo donde BANC predice, porque ahí los arbores se tocan.

**El error propio, nombrado:** verifiqué el sujeto pero no la **escala** a la que la explicación rival era cierta. Es el E-01 de siempre, con otra cara.

### 🟢 Tres: y acá está lo bueno, que es mejor que lo que se cayó

Si el cero a un salto es «no llegó porque no salió del barrio», entonces la pregunta correcta es: **¿y cuando SÍ sale del barrio, llega?**

Lo medí. A **dos** saltos:

```
visual          alcanza 95.160 nodos  ->  toca  15 de 110 motoras de cabeza
mechanosensory  alcanza 68.471 nodos  ->  toca 110 de 110
gustatory       alcanza 26.535 nodos  ->  toca 107 de 110
olfactory       alcanza 22.940 nodos  ->  toca  23 de 110
```

**Visual es la que llega MÁS LEJOS de todas (95.160, más que ninguna) y es la que toca MENOS motoras (15).** Mechano llega menos lejos y toca **todas**.

A dos saltos ninguna se quedó en su barrio: todas salieron por decenas de miles de nodos. **Entonces el arbor ya no es excusa, y la asimetría sigue ahí.**

Y el enunciado deja de ser «visual no llega», que es débil y explicable, y pasa a ser **«visual llega a todas partes menos ahí»**, que es raro y necesita explicación. **Ese es el hallazgo de verdad, y es más fuerte que el cero que perdí.**

---

## 4. Por qué hay que reescribir · y acá hay reloj

**El erratum tiene una frase falsa, y ese archivo se sube a Zenodo antes del 30-ago. Faltan 6 días.**

La frase, en el ítem 3 de `docs/ERRATUM.md`:

> ~~*«which the published network analyses report only as a single global figure»*~~

O sea: **el erratum le acusa a Nature de haber reportado solo un número global, y Nature reporta el desglose completo.**

### Y por qué esto es grave y no un detalle

El **ítem 4 del propio erratum** existe porque un borrador anterior corrigíó un «1.559×» que **no existía en el paper**. La lección que quedó escrita ahí es: *un erratum que corrige un claim que el paper nunca hizo es él mismo un error*.

**Esto es la misma falla apuntando al otro lado:** un erratum que le atribuye a **Nature** un defecto que Nature no tiene. Y es peor que el original, porque el primero era un error contra vos mismo y este es un error **contra el paper de otros, con nombre y apellido, en un documento con DOI**.

Un revisor que abra la Fig. 5 de Lin lo ve en treinta segundos. Y no te discute solo esa frase: te discute la buena fe de todo el erratum.

### Qué va en su lugar

De «ellos solo dan un global, yo doy la distribución» (falso) a **«ellos la desglosan por región anatómica, yo por clase funcional dirigida; son ejes complementarios»** (verdadero, y además te hace ver como alguien que leyó el paper de verdad).

**Perdés tamaño de claim y ganás que no se pueda tumbar.** Es el mismo canje que ya hiciste con el 36×.

### Y lo que YA reescribí vs lo que NO

| Archivo | Estado | Por qué |
|---|---|---|
| `docs/PIVOTE-RECIPROCIDAD.md` | ✅ **corregido** | es un borrador de trabajo, no tiene DOI |
| `docs/ERRATUM.md` | ❌ **intacto a propósito** | **cambia un claim científico en un documento que se publica. Eso es tuyo.** |
| `CONTEXTO-drosophila-fep.md` | ❌ todavía dice «Lin da un número global; el Paper 1 da la distribución» | mismo defecto, arreglable sin permiso, **no lo hice en este turno** |

---

## 5. La segunda cosa a arreglar, más chica pero fea

Anoche conté **105** motoras de cabeza. Hoy, **110**. Con los nervios también distintos (CV 20 vs 19, ON 10 vs 6).

Usé dos filtros distintos y **no establecí cuál es el que corresponde a la población del paper**. El cero se sostiene con los dos, así que el hallazgo no se cae, pero **el denominador de cualquier fracción está sin fijar**, y «15 de 110» es una fracción. Se arregla en una corrida.

---

## 6. En tres líneas

- **Descubrí que dos cosas que te vendí eran más chicas de lo que dije**, y las dos las verifiqué yo, no me las señaló nadie.
- **Y que hay algo mejor abajo:** visual llega más lejos que nadie y toca menos motoras que nadie.
- **Hay que reescribir porque una frase falsa sobre Nature se va a un DOI en 6 días**, y es literalmente el error que el propio erratum dice que no hay que cometer.

---

## 7. NO MEDIDO, declarado

1. **Este turno no midió nada.** Todo número viene de la resp 057.
2. **No leí los valores de la Fig. 5c ni de la ED Fig. 6c de Lin.** Sé qué miden por el pie de figura; **si alguno de sus neuropilos coincide funcionalmente con un circuito de la Table 7, «complementarios» es demasiado generoso**.
3. **Los conteos a 2 saltos no tienen null.** Sin null preservando grado, «visual llega más lejos y toca menos» es una observación cruda, **no un resultado publicable**.
4. **El alcance a 2 saltos ignora signo y peso:** cuenta si existe camino, no cuánta señal pasa.
5. **El erratum y el contexto siguen con la frase falsa.** Declarado, no arreglado.
6. **La discrepancia 105 vs 110 sigue abierta.**
