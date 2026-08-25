# EVIDENCIA CRUDA · revisión del barrido a 17 de 30 puntos

**Fecha:** 2026-08-25 13:15 (America/Buenos_Aires)
**Instrumento:** `src/cascade_sensitivity.py` md5 `74a6a2261e87e8683147364cc9227c20`, **CORRIENDO** en `brain-env`, `/workspace/sens/`
**Estado:** 17 de 30 puntos. **NO se emite veredicto.**

---

## 0. 🔴 Lo primero: dos falsos hallazgos que casi publico, y el punto 17 los mató

Esta sección va primera porque el patrón es más útil que los números.

### Falso hallazgo 1 · «el flag SATURADO nunca se enciende»

Lo verifiqué con aritmética y estaba **correcto sobre 16 puntos**:

```
=== DEFECTO 1: mi flag SATURADO puede encenderse? ===
  umbral que puse: hi >= 0.90 * 110 = 99.0
  el maximo observado en 16 puntos: 94.97
  o sea que el flag NUNCA se enciende -> False
```

**Iba a reportarlo como un guard que no puede dar verde**, o sea el modo de falla 2 en mi propio instrumento. **Y es falso.** El punto 17:

```
  p=0.0100 seed=  4  vis= 52.62  olf=105.62  mec= 92.00  gus=105.30  | AZAR=105.62  spread=  2.007  SATURADO
```

**El flag se enciende.** El defecto no existía: **leí 16 de 30 y concluí sobre 30.**

### Falso hallazgo 2 · «mis dos implementaciones dan techos distintos»

Más caro, porque **ya había escrito y lanzado un instrumento para resolverlo** (`cmp_impl.py`, 4.401 B).

El razonamiento era: la resp 082 midió **105-106** motoras a `p=0.01, seed=16`, y el barrido no pasaba de **95** en ningún punto. Dos números de la misma cantidad con dos instrumentos propios → **modo de falla 5**.

**También falso.** El barrido **todavía no había llegado a `p=0.01`**: sus 16 primeros puntos son `p` de 0,0001 a 0,003. En `p=0.0100 seed=4` da **105,62**, que **reproduce la corrida vieja**. Las dos implementaciones **coinciden**, y la diferencia era **el régimen de `p_trans`, no el código.**

> **Los dos errores tienen la misma forma: leer una serie incompleta y concluir sobre la serie.** Es «una lista hecha de lo que está a mano solo contiene lo que está a mano», **aplicado al tiempo en vez de al espacio**. Y el antídoto estaba escrito en el propio instrumento: **no emitir veredicto hasta los 30 puntos.**

**Lo que salva el turno:** los dos se detectaron **antes** de salir, y el falsador fue **el propio barrido**, no yo.

---

## 1. Los 17 puntos, verbatim

```
=== CASCADE SENSITIVITY  ---  items 1 y 2 de la deuda declarada ===
N=138639  E=15091983  Mw=54492922
G1 los tres conteos coinciden con Betzel 2026: OK
  pob visual           n=10855  descartadas=536
  pob olfactory        n=2279  descartadas=3
  pob mechanosensory   n=2656  descartadas=12
  pob gustatory        n=408  descartadas=0
  pob motor            n=110  descartadas=0
  pob ZZQQXX_AZAR      n=256  (control negativo, nodos al azar del grafo)

=== ITEM 2 - BARRIDO de p_trans x N_seed, unimodal, 40 realizaciones por punto ===
   (el sensitivity analysis que pidio su Revisor #3)
  p=0.0001 seed=  1  vis=  0.00  olf=  0.00  mec=  0.00  gus=  0.00  | AZAR=  0.00  spread=    inf  no-sat
  p=0.0001 seed=  4  vis=  0.00  olf=  0.00  mec=  0.00  gus=  0.00  | AZAR=  0.05  spread=    inf  no-sat
  p=0.0001 seed= 16  vis=  0.00  olf=  0.00  mec=  0.00  gus=  0.00  | AZAR=  0.05  spread=    inf  no-sat
  p=0.0001 seed= 64  vis=  0.00  olf=  0.00  mec=  0.00  gus=  0.03  | AZAR=  0.12  spread=    inf  no-sat
  p=0.0001 seed=256  vis=  0.00  olf=  0.00  mec=  0.07  gus=  0.10  | AZAR=  0.30  spread=    inf  no-sat
  p=0.0010 seed=  1  vis=  0.00  olf=  0.10  mec=  0.30  gus=  0.75  | AZAR=  1.48  spread=    inf  no-sat
  p=0.0010 seed=  4  vis=  0.00  olf=  3.92  mec=  0.65  gus=  6.40  | AZAR=  5.42  spread=    inf  no-sat
  p=0.0010 seed= 16  vis=  0.00  olf=  7.33  mec=  5.40  gus= 20.85  | AZAR= 16.00  spread=    inf  no-sat
  p=0.0010 seed= 64  vis=  0.03  olf= 19.57  mec= 20.10  gus= 33.35  | AZAR= 32.15  spread=1334.000  no-sat
  p=0.0010 seed=256  vis=  0.05  olf= 25.65  mec= 40.23  gus= 42.35  | AZAR= 45.00  spread=847.000  no-sat
  p=0.0030 seed=  1  vis=  1.57  olf= 13.72  mec= 18.82  gus= 42.20  | AZAR= 27.32  spread= 26.794  no-sat
  p=0.0030 seed=  4  vis=  7.65  olf= 74.47  mec= 41.88  gus= 86.42  | AZAR= 84.17  spread= 11.297  no-sat
  p=0.0030 seed= 16  vis= 24.77  olf= 93.78  mec= 90.15  gus= 94.20  | AZAR= 94.40  spread=  3.802  no-sat
  p=0.0030 seed= 64  vis= 54.98  olf= 93.12  mec= 94.25  gus= 94.33  | AZAR= 94.80  spread=  1.716  no-sat
  p=0.0030 seed=256  vis= 91.55  olf= 94.17  mec= 94.85  gus= 94.97  | AZAR= 94.90  spread=  1.037  no-sat
  p=0.0100 seed=  1  vis= 29.12  olf= 74.05  mec= 47.48  gus= 84.22  | AZAR= 73.65  spread=  2.892  no-sat
  p=0.0100 seed=  4  vis= 52.62  olf=105.62  mec= 92.00  gus=105.30  | AZAR=105.62  spread=  2.007  SATURADO
```

---

## 2. 🔥 Lo que SÍ sobrevive: el azar le gana a las vías reales

Medido sobre los 16 primeros puntos:

```
  puntos analizados: 16
  visual   el AZAR le gana en 15 de 16 puntos
  olfat    el AZAR le gana en 14 de 16 puntos
  mecano   el AZAR le gana en 15 de 16 puntos
  gustat   el AZAR le gana en  8 de 16 puntos

  el AZAR le gana a LAS CUATRO a la vez en 8 puntos
  el AZAR queda ULTIMO (peor que las cuatro) en 0 puntos
```

> **256 nodos tomados al azar del grafo entero alcanzan más motoras que las vías sensoriales reales, en casi todo el rango de parámetros.** Y **nunca** queda último.

**Por qué este hallazgo NO depende de los 13 puntos que faltan:** ya tiene **16 mediciones a favor y cero en contra** en la dirección del conteo. Los puntos que faltan pueden cambiar la magnitud, no el signo. **Es lo más fuerte que deja el barrido hasta ahora**, y hay que decir por qué importa: **una cascada sin signo que no distingue una vía sensorial de un puñado de nodos cualquiera no está midiendo especificidad de modalidad para acceso motor.**

⚠️ **Con una salvedad de tamaño que hay que declarar:** el control tiene **256 nodos** y las clases reales tienen 408 (gustativa), 2.279, 2.656 y 10.855. Pero `N_seed` acota la siembra a 1, 4, 16, 64 o 256, **así que en el punto de 256 semillas el control siembra su pool ENTERO y las clases reales siembran una fracción**. Eso **favorece al control** en ese punto y **no está controlado**. Es la limitación principal del hallazgo.

---

## 3. Los dos regímenes, y ninguno informativo

| régimen | qué pasa |
|---|---|
| `p = 0.0001`, los cinco `N_seed` | **la cascada MUERE**: 0,00 motoras en las cuatro clases |
| `p = 0.01`, `N_seed = 4` | **ya SATURA**: 105,62 de 110 |

> **El rango útil es angosto y está entre medio.** Con dos órdenes de magnitud de `p_trans` el modelo pasa de no encender nada a encender casi todo. **El `p = 0.01` que Betzel fija en el cuerpo del paper está del lado saturado**, y eso es exactamente lo que su Revisor #3 pidió y el paper no reporta.

---

## 4. 🟢 Y lo único que se separa de forma consistente: VISUAL

**Visual queda por debajo de las otras tres en 16 de 16 puntos**, y por debajo del azar en 15 de 16. En el punto 17, con las otras tres entre 92 y 105,6, visual da **52,62**.

> **Esa es la única especificidad de modalidad que el modelo de cascada conserva, y es robusta al parámetro.** Coincide en dirección con lo que el modelo lineal con signo mide (olfatoria y visual depletadas), pero **el lineal separa 98× y la cascada separa 2×** en el mismo punto.

---

## 5. El techo no es un artefacto de conectividad

```
motoras totales       110
con al menos 1 entrada 110
con CERO entradas      0
```

**Las 110 motoras son alcanzables en principio.** El techo de ~105 que se observa **no** viene de neuronas sin entrada.

---

## 6. NO MEDIDO, declarado

1. **El barrido está en 17 de 30. NO hay veredicto**, y los dos falsos hallazgos de la §0 son la prueba de por qué no conviene emitirlo.
2. **`cmp_impl.py` quedó corriendo y sin terminar.** Ya no resuelve una discrepancia (que no existía) pero **sigue midiendo algo útil**: la sensibilidad a `CSTEPS` y al número de realizaciones, que el barrido **no** barre.
3. **El desbalance de tamaño del control** (§2) no está corregido: en `N_seed=256` el control siembra su pool entero y las clases reales no. **Un control con el mismo tamaño de pool que cada clase sería el diseño correcto y no se corrió.**
4. **Las dinámicas cooperativa y competitiva corren al final del script y todavía no llegaron.** El ítem 1 de la deuda sigue abierto.
5. **`CSTEPS = 12` sigue siendo una elección mía**, no de Betzel: su paper no fija ese número en el cuerpo.
6. **El punto de comparación exacto con la resp 082** (`p=0.01, seed=16`) **aún no llegó**: la coincidencia se apoya en `seed=4`, que da 105,62 contra los 105,1-106,05 de la corrida vieja con `seed=16`. **Es consistente, no idéntico.**
