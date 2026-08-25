# ADDENDUM 01 a la orden de auditoría · para TITAN Tao

**Emitido:** 2026-08-25 02:05 (America/Buenos_Aires), **después** de la orden y **antes** de que Tao empiece.
**Se lee junto con:** `docs/agents/ORDEN-TAO-AUDITORIA-EXTERNA.md`. **No la reemplaza.**

---

## Por qué existe

La orden lista **C-08** así: *«tau heterogénea es el parámetro con más chance de generar selectividad temporal y no se barrió. Este claim puede ser un artefacto de un modelo demasiado pobre, y si lo es, es una buena noticia que BRAIN no vio.»*

**Se barrió, veinte minutos después de emitir la orden.** Y el resultado no fue el que la orden anticipaba: **el modelo pobre no era el problema, la métrica lo era.**

Así que **C-08 tal como está escrito ya no es el claim vigente**, y auditar el claim viejo sería auditar algo que nadie sostiene. Acá está el reemplazo.

---

## Lo que se midió, en cuatro líneas

```
sel_peak con tau fija:  1,0631      <- lo que BRAIN midio siempre
sel_post con tau fija:  4,3287      <- lo que BRAIN nunca habia medido

STRUCTURED (rapida a visuales) pierde contra REVERSED en sel_peak, 5 de 5 spreads
sel_post DECRECE monotonamente con la dispersion de tau: 4,33 -> 2,07
```

`sel_peak` es el cociente de picos de respuesta entre un estímulo que crece y su reverso exacto, a energía igualada. `sel_post` es el cociente de la integral de respuesta **después** de que el estímulo terminó.

Evidencia cruda completa: `docs/agents/evidencia/2026-08-25-barrido-tau-heterogenea-evidencia-cruda.md`. Instrumento: `src/sweep_tau_hetero.py`, md5 `35cabd5acc51f37529584cc53c013dcf`.

---

## C-08 reformulado, en tres claims

### C-08a · tau heterogénea no rescata la selectividad de pico como vía biológica

La asignación **STRUCTURED** (constantes rápidas a las poblaciones visuales y ópticas, lentas a las centrales, siguiendo la medición regional del propio repo) da **menos** selectividad que su **REVERSED** exacto en los cinco spreads, con `sd` de tercera cifra.

*Cómo atacarlo:* la partición rápido/lento la eligió BRAIN usando `super_class`, y las 11 `tau` regionales del motor son **andamio sintético hardcodeado**, no medición. **¿Hay otra partición defendible que gane?** Si la hay, C-08a se cae.

### C-08b · 🔴 el `sel_post = 4,3287` se entrega SIN control, y es el hallazgo principal

El control de signo barajado de la corrida previa se midió **solo sobre `sel_peak`** (dio 1,1131 ± 0,0185, con 19 de 20 permutaciones por encima del real). **Para `sel_post` no hay null.**

*Cómo atacarlo, y es lo primero que te pido:* este repo tiene escrito, como modo de falla numerado, que **un ratio contra nada no es un resultado**, y que **un ratio contra un null necesita saber cuánto da un sujeto cualquiera contra ese mismo null**. **BRAIN entregó el 4,33 igual.** Corré el sign-shuffle sobre `sel_post` o declará el claim como no evaluable. **Es una corrida de un minuto sobre el script que ya está commiteado.**

### C-08c · la ventana de integración no está justificada

`sel_post` integra del paso 80 al 200, con el estímulo entre 20 y 80. **Esa ventana la eligió BRAIN y no la barrió.**

*Cómo atacarlo:* si el 4,33 depende de dónde se corta, es un artefacto de la ventana. Con 200 pasos y `tau = 0,119` (memoria efectiva ~7,9 pasos), **una cola de 120 pasos es mucho más larga que la constante de tiempo**, y eso hay que explicarlo o acortarlo.

---

## C-13 · el claim nuevo, y es de método, no de número

**Las dos métricas se mueven en direcciones OPUESTAS con la dispersión de tau:**

| Spread | `sel_peak` | `sel_post` |
|---|---|---|
| 1 | 1,0631 | **4,3287** |
| 8 | 1,1307 | 3,5189 |
| 30 | **1,1874** | 2,6298 |

O sea: **subir la dispersión mejora una y arruina la otra.** Y de las dos, BRAIN eligió `sel_peak` durante seis días, sin justificar la elección, y de ahí salió el claim «la topología define ruteo y ganancia, no selectividad».

*Cómo atacarlo:*
- **¿Cuál es la métrica correcta?** Si lo que decide un escape real es cruzar un umbral de disparo, ninguna de las dos puede ser la buena: la correcta sería **latencia al umbral**, y **no se midió**.
- **¿Cuántos claims más de este repo dependen de una métrica elegida sin justificar?** Este es el patrón que quiero que barras. Candidatos donde mirar: el **RDI** del Paper 1 (con `z = 197`), la **entropía** (donde ya se sabe que los nulls bajan más que el real), y el **`gdisp`** del A/B del gate.
- Y la pregunta incmóoda: **el `sel_post` de 4,33 es cualitativamente la Propiedad 3 del Paper 1** (amplificación post-estímulo, RDI de 0,63 a 0,83, `z = 197`). BRAIN tenía eso medido **en el conectoma** desde hace días y **no lo había buscado en el compilado**. **¿Hay otras propiedades del paper que estén medidas de un lado y no del otro?** Si el compilado reproduce las tres, eso es un resultado grande; si reproduce una sola, eso también es información y es peor.

---

## Qué cambia en tu prioridad

La orden decía: **erratum > null anatómico > dirección**. **No cambia.** El erratum vence el 30-ago y sigue primero.

**C-08b entra cuarto, no antes**, aunque sea lo más barato de todo: es un claim de una rama sin mergear, y romperlo no rompe nada publicado. **Pero si lo hacés, hacelo antes que el resto de C-08**, porque si el 4,33 no sobrevive el null, C-08a y C-08c dejan de importar.

---

## Lo que este addendum NO cambia

- **No mergear, no publicar en Zenodo, no tocar `main`, no arreglar nada.** Igual que en la orden.
- **El permiso de la §8 sigue vigente y ahora vale doble:** BRAIN escribió esta orden **y** este addendum, y el addendum existe porque BRAIN se equivocó en el claim que él mismo puso en la lista para que lo auditaras. **Eso es exactamente la prueba de que la lista no cubre el sesgo de selección.** Ignorala si te conviene.
