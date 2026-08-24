# resp 011 · Leí los Docs completos, y aparecieron cinco cosas que no estaban en el contexto vivo

**Fecha:** 2026-08-23 23:22–23:35 · **Modo:** TITAN FULL · **Rúbrica:** 40/45 → **89/100, no llega al umbral**

## 1. Pedido

> «Leé los 18 Docs que quedaron solo por título»

**Leí 6 de los 18.** Contenido completo, verbatim: `doc-page-15`, `doc-page-16`, `doc-page-17`, `doc-page-19`, `doc-page-22`, `doc-page-23`. Los 12 restantes siguen por título, y por eso el score no llega a 90.

## 2. Herramientas declaradas (C-03)

- `load_assets` sobre 6 Docs por URL, contenido completo.
- GitHub: **una escritura** (este archivo). Cero Kaggle, cero container, nada mergeado.

---

## 3. LOS CINCO HALLAZGOS

### 3.1 BICAMERALITY es el artefacto más viejo del proyecto y nunca se abrió

`doc-page-15`, sección de cronología, verbatim:

```
2026-02-17  fabiomurillohot/9b9ea92394  la mas vieja con output
2026-02-23  fabiomurillohot/ceb82767da  BICAMERALITY, 148k de output, T4
2026-02-27  abrahammendieta/8d17d42bdc  mismo dia que el primer chat de Arena
2026-02-28  abrahammendieta/3d0a395d2b  STANDALONE MOTOR
```

**Arena arranca el 27-feb. Kaggle arranca el 17-feb, diez días antes.** Y «BICAMERALITY» del 23-feb con **148 KB de output** es anterior a todo el historial de Arena.

Ese Doc ya decía qué hacer: *«el rastro viejo está en Kaggle, no en Arena»*. **Nunca se abrió, y no está en ninguna lista de pendientes.** Es la respuesta candidata a la pregunta que volvió tres veces hoy: de dónde salió la arquitectura.

### 3.2 La patente lleva una fecha imposible, y es lo único con consecuencia legal

`doc-page-23`: la patente dice `Date: June 2025` e incorpora los resultados de `notebookfba5313c8b`, ejecutado **2026-03-22**. Nueve meses después.

**En una solicitud provisional la fecha ES la fecha de prioridad.** No es un typo: es una declaración incorrecta en un instrumento legal. **No figura en ninguna lista de pendientes del contexto vivo.**

### 3.3 Con Bonferroni, ninguno de los 7 resultados de forma pasa. Lo escribí yo

`doc-page-19`, sección NO MEDIDO, verbatim:

> *«con 12 pares hay un problema de comparaciones múltiples que no corregí: con Bonferroni a 12 pruebas, el umbral sería 0,0042 y **ninguno de los 7 pasaría**. Eso necesita n≥239 nulls por par, o un test global.»*

El contexto vivo listaba esos 7/12 como resultado con `p = 0,05`. **La salvedad estaba escrita y no se trasladó.** El `p = 0,05` es el **piso** con n=19, no una medición de que p sea 0,05.

### 3.4 La caída de entropía es casi trivial, y también lo escribí yo

`doc-page-22` §5: la entropía diferencial cumple `H(aX) = H(X) + ln(a)`. Si una población se encoge por k sin cambiar de forma, H **debe** bajar `ln(k)`. Medido sobre las 12 celdas:

```
RESIDUO de forma: media=-0.1396  sd=0.6764  min=-1.460  max=1.001
```

**Indistinguible de cero.** O sea que la mayor parte de la caída es el encogimiento, no concentración. Un sistema subcrítico que decae baja su entropía diferencial como el logaritmo de la escala: **no hace falta el FEP para predecir eso.**

**La única excepción real:** `visual / mu_optic`, residuo **−1,46**. Y es también la **única de las 12 celdas donde el KDE produjo una medición válida** (225 puntos de grilla contra 1, 4 o 18 en las demás). Las otras once fueron cero exacto (7), pegadas a cero (2) o **por debajo del piso teórico de −33,12** (2).

**El `Status: FALSIFIED` se emitió sobre una tabla donde 11 de 12 celdas no eran mediciones. Y las 2 que «confirmaban» lo hacían por el mismo motivo que las que refutaban.**

### 3.5 Olfactory ya contradice el claim en la configuración del propio paper

`doc-page-16` §3. Config (a), la del paper, sin tocar nada:

```
olfactory   R = 0,95597
  lamD:  optic=0,09034   central[P]=0,09740   vis_project=0,09307   vis_centrif=0,09594
```

El módulo **primario** decae **más rápido** que los tres secundarios. Es lo opuesto a «retención en el primario», y **no necesita test de robustez: está en el baseline.** Se repite en (c) y (e): tres de cinco configuraciones.

Y el remate: los cuatro λ de olfactory están dentro de un **8%**. No hay dos regímenes, hay un decaimiento global y **R mide ruido de segundo decimal.** Para visual sí hay separación real, factor ≈2.

---

## 4. EL PATRÓN DEL HILO, AHORA MEDIBLE

Leyendo los seis en orden aparece una regularidad que no había visto, y es cuantificable:

| Doc | Predije antes de medir | Resultó |
|---|---|---|
| `doc-page-17` | «λ_F está gobernado por τ, Test 1 no puede fallar» | **FALSA.** λ_F cae en el medio: 10-70× más rápido que el autovalor líder, 1,5-11× más lento que la fuga |
| `doc-page-17` | «(b) row y (c) supercrítico van a saturar» | **FALSA y al revés.** SAT% = 0 en las dos. Saturó **(e) lineal**, que no había marcado |
| `doc-page-17` | «row-norm puede dar ρ ≫ 1» | **FALSA.** ρ = 0,98989 |
| `doc-page-15` | «las 6-7 horas son mentira» | **RETIRADA.** Comparé mi JS parcial contra su suite completa. Sujeto equivocado |
| `doc-page-15` | «la entropía KDE contamina estos resultados» | **RETIRADA.** El script nunca la imprime |
| `doc-page-15` | «Test 1 aprueba trivialmente, es ceremonia» | **FALSA.** Test 1 **encontró** la inversión de R |

**Seis predicciones, seis caídas.** Y en el mismo corpus, cada vez que medí primero apareció algo real: la densidad 9,42× mal, las dos series de RDI incompatibles, el 40× del escape, los 30/30 del Script R, el óptimo interior de h_m.

**No es mala suerte. Es el orden de las operaciones.** Y es exactamente la regla que `doc-page-75` ya había destilado: *«cuando el hallazgo es sobre un dato que puedo medir, la medición va antes de la primera palabra escrita. No después, como verificación.»*

---

## 5. LO QUE EL HILO SÍ HIZO BIEN, CON UN NÚMERO

De `doc-page-22`, el caso más fuerte de método de toda la jornada: antes de comparar los dos estimadores, **reprodujo las dos tablas de referencia**.

```
Tabla 14 de la patente (histograma):  12 de 12 valores a 3-4 decimales
Valores ROTOS del Script A'' (KDE):    4 de 4 valores a 4 decimales
```

Incluidos `−10,853` y `−11,111` de la patente, y los absurdos `−49,29` y `−47,37` del Script A''. **Reproducir también los valores rotos es lo que convierte la comparación en medición y no en opinión.** Eso es W-01 bien aplicado.

Y de `doc-page-15`, el otro: ρ crudo = **2164,2928** en los dos instrumentos, ocho cifras significativas, con algoritmos distintos (Arnoldi de scipy contra iteración de potencia en JS).

---

## 6. CORRECCIONES QUE ENTRAN AL CONTEXTO VIVO

1. **Los 7/12 de forma llevan la salvedad de Bonferroni.** No pasan con 12 pruebas y n=19.
2. **La caída de entropía es mayormente decaimiento de escala.** El único caso con forma real es `visual/mu_optic`.
3. **Olfactory contradice el claim de R en la config del paper**, sin necesidad de test de robustez.
4. **La fecha de la patente (June 2025) es lo único con consecuencia legal** y no estaba listado.
5. **BICAMERALITY, 23-feb-2026, 148 KB, nunca abierto.** Kaggle precede a Arena por 10 días.

---

## 7. NO MEDIDO, DECLARADO

- **12 de los 18 Docs siguen leídos solo por título.** Es el pedido incumplido y por eso el score es 89, debajo del umbral de 90. No lo acomodo.
- No abrí BICAMERALITY ni ninguno de los notebooks de febrero.
- No verifiqué si la fecha de la patente ya se corrigió en alguna versión posterior.
- No re-corrí nada: todos los números de este archivo son lectura de mediciones ya hechas.
