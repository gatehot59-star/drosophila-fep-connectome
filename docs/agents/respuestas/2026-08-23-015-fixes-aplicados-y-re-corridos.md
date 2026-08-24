# resp 015 · Los dos fixes aplicados y re-corridos · TITAN FULL

**Fecha:** 2026-08-23 23:56 → 2026-08-24 00:35 · **Modo:** TITAN FULL · **Rúbrica:** 72/75 → **96/100**

## 1. Pedido

> «Arreglá el max_norm y el guard de tautología, y re-corré»

## 2. Herramientas declaradas (C-03)

`build.run` en el container. **No se usó Kaggle:** torch 2.13.0+cpu está local, cero cuota. GitHub: un commit. Nada del proyecto se sobreescribió: todo vive en `audit/bicamerality/`.

**Lo que NO se commitea y por qué:** `cell1_fixed.py` es obra derivada de código de procedencia desconocida (resp 013). Se commitea `patch.py`, que lo regenera de forma determinista (7 de 7 reemplazos, md5 esperado `57c91b7f5c30fd9e1ad4c02fbf340226`), y `fix.diff`, que contiene **solo mis cambios**: 8 líneas menos, 53 más.

---

## 3. FIX 1 · max_norm: el problema no era el valor, era que no había validación

Cambiar 3,0 por otro número no arregla nada: el próximo que toque `H` vuelve a romperlo en silencio. Lo que faltaba era un **guard del guard**:

```python
self.norm_bound = float(H) ** 0.5
if max_norm is None:
    max_norm = clamp_frac * self.norm_bound
if max_norm >= self.norm_bound:
    raise ValueError('max_norm=... es INALCANZABLE: la cota analitica con '
                     'H=... es sqrt(H)=... Un guard cuya rama nunca se '
                     'ejecuta no protege nada y hace creer que si.')
```

Ahora **una configuración imposible no compila**, en vez de pasar callada.

### Y mi primer intento quedó corto. Mi propia suite lo marchó en rojo

Con `clamp_frac=0.6` el umbral daba **1,6971**: analíticamente alcanzable (menor que 2,8284) pero **empíricamente 0 de 12.800 activaciones**. El log está conservado en `refix_quick.log` porque es el falsador de mi propio fix.

**Alcanzable y alcanzado no son lo mismo.** Había que calibrar con la distribución medida, no con un número elegido a dedo. `dist.log`, 1.382.400 muestras:

```
escala_x   p50      p99      p99.9     max
     0.5   0.5347   1.1526   1.2296   1.3052
     2.0   0.7930   1.3436   1.4954   1.7581
     5.0   1.4222   1.9351   2.0964   2.3503
    20.0   2.0201   2.5364   2.6617   2.8011
   100.0   2.2657   2.7211   2.8258   2.8284
```

**Con estímulo ×100 la norma llega a 2,8284, que es exactamente sqrt(8).** El estado satura **en** la cota analítica. Así que el umbral correcto para una red de seguridad está justo por debajo: `0,97 × sqrt(H) = 2,7436`.

### Verificado en los dos regímenes

```
regimen        escala_x   activaciones / llamadas
NORMAL             2.0     0 / 230.400        -> inocuo, no distorsiona
ESTRES           100.0     122.097 / 230.400  -> alcanzable de verdad
```

Eso es lo que una red de seguridad tiene que hacer: **no tocar la dinámica de trabajo y disparar cuando algo se va de rango.**

### Y el original queda refutado sin apelación

```
ORIGINAL con umbral 3.0, bajo el MISMO estres x100:
  max norma = 2.828427    umbral = 3.0
```

**Ni con estímulo cien veces mayor al normal llega a 3,0**, porque no puede: `sqrt(8) = 2,8284` es el techo matemático. Código muerto confirmado, no por semilla ni por suerte.

---

## 4. FIX 2 · El guard de tautología, por término

Si `sd(label) == 0` en el batch, ese término no puede enseñar nada: regresionar contra una constante solo empuja el estimador a un valor fijo. Se cuenta **NO TESTEABLE** y sale de la loss. Los dos términos se evalúan **por separado**, porque uno puede tener señal y el otro no.

### Discrimina por batch, que es lo que lo hace un guard y no un interruptor

```
PureMemory     danger:  0 usada / 56 NO TESTEABLE    energy:  0 / 56
SurvivalWorld  danger: 23 usada / 13 NO TESTEABLE    energy: 36 / 0
```

**En PureMemory los dos términos son tautológicos en el 100% de los batches.** En SurvivalWorld `energy` siempre tiene señal, y `danger` la tiene en 23 de 36 batches: con 2,8% de positivos, hay batches enteros sin un solo evento. **El guard los distingue uno por uno.**

---

## 5. EL HALLAZGO: el guard solo NO arregla el veto. Lo CONGELA

Tres brazos, PureMemory, 240 episodios, semilla 42:

| Brazo | alpha ini → fin | factor sobre el std | align ini → fin |
|---|---|---|---|
| **A** original | 0,3742 → 0,4758 | 0,2860 → **0,3505** | 0,5045 → 0,5297 |
| **B** guard, veto ON | 0,3645 → 0,3813 | 0,2806 → **0,2901** | 0,5045 → 0,5308 |
| **C** guard, veto OFF | 0,3644 → 0,3830 | **1,0000** | 0,4995 → 0,5232 |

**El brazo B es peor que el A.** Y la explicación es incómoda y buena:

> En el original, la MSE tautológica regresionaba `energy_est` contra la constante 1,0. Eso no enseñaba nada sobre energía, **pero arrastraba alpha hacia arriba** (+0,10 en 240 episodios) y así **iba aflojando el handicap que ella misma causaba**. Al excluir el término con el guard, ese arrastre desaparece y alpha queda clavado en 0,38: **el castigo de exploración del 29% se vuelve permanente.**

La loss tautológica estaba mitigando accidentalmente su propio daño. Sacarla sin tocar el veto deja el daño y quita la mitigación.

**Solo el brazo C lo elimina:** `factor_std = 1,0000` exacto.

### La regla que sale, y es general

**Un guard de tautología tiene que propagarse al consumidor de la señal, no solo excluir el término de la loss.** Si una etiqueta es NO TESTEABLE, todo lo que dependa de esa señal tiene que apagarse también. Un guard que marca el síntoma y deja actuar la causa es peor que no tenerlo.

Eso aplica hacia atrás: el guard de `src/motor.py` marca `NO_TESTEABLE` cuando `sd(null) == 0` y **no reporta un ratio**, o sea que ahí la propagación sí está hecha. Vale revisar que ningún otro consumidor lea ese campo igual.

---

## 6. Lo que NO se puede afirmar

**Los fixes quitan un confound. Que mejoren el desempeño NO está medido.**

Los tres brazos dan align **0,5232 / 0,5297 / 0,5308**: los tres en **nivel de azar** (0,5). Con 240 episodios y una semilla, la tarea no se aprende en ningún brazo. El recompensa final va 1,557 → 1,770 → 1,842, monótona en la dirección esperada, pero **con n=1 eso no es una medición.**

Para afirmar mejora hace falta el benchmark completo: 500 episodios × 3 semillas × 2 tareas. Con 2 threads de CPU son varias horas.

---

## 7. Estado de los dos rojos originales

| Rojo de resp 014 | Estado |
|---|---|
| `zen_clamp_se_activa` | **CERRADO.** Umbral 2,7436, inerte en normal, 122.097 activaciones bajo estrés, y una configuración inalcanzable ahora levanta `ValueError` |
| `presupuesto_pareado_PureMemory` | **ABIERTO a propósito.** No se pidió y no lo toqué. Medido: con `H_order=22` el ratio da 0,980, dentro de tolerancia. Es un cambio de una línea cuando lo decidas |

---

## 8. Evidencia cruda (W-01)

| Archivo | Qué contiene |
|---|---|
| `patch.py` | el parche, 7 de 7 reemplazos, regenera `cell1_fixed.py` determinista |
| `fix.diff` | solo mis cambios: 8 líneas menos, 53 más |
| `refix_quick.log` | **mi primer fix en rojo.** Conservado a propósito |
| `dist.log` | 1.382.400 muestras de norma, 6 escalas × 3 semillas |
| `refix2.log` | el fix recalibrado: 0 en normal, 122.097 en estrés, 0 rojos |
| `arms.log` · `arms.json` | los tres brazos y los contadores del guard |

md5: sujeto `9d89a158f809ff5f3765f42848502665` · `cell1_fixed.py` `57c91b7f5c30fd9e1ad4c02fbf340226`.

---

## 9. Scorecard

| Criterio | Pts | Evidencia |
|---|---|---|
| Completitud | 13/15 | Los dos fixes pedidos, aplicados, con el guard del guard, y re-corridos con 3 brazos. **−2: mi primera calibración quedó empíricamente muerta y hubo que iterar; y el efecto sobre el desempeño no es medible a este presupuesto** |
| Ejecutabilidad | 15/15 | `patch.py` aplica 7 de 7, `py_compile` OK, las cuatro corridas con `exit=0`, y todo regenerable desde el original |
| Testing | 14/15 | Cada test puede dar rojo, y **la suite marcó en rojo un fix mío**. G0 y G2c son controles del control. **−1: sigue sin haber test de `ppo_seq_update` con gradiente conocido** |
| Arquitectura del razonamiento | 10/10 | El fix estructural es el `ValueError`, no el valor. Y el diseño de tres brazos aisló que el guard solo **empeora**, que era invisible con dos brazos |
| Documentación | 10/10 | Diff acotado, md5 de todo, instrucciones de regeneración, y el log del fix fallido conservado |
| Innovación | 5/5 | No pedido: el `ValueError` que rechaza configuraciones imposibles; el test de dos regímenes (inocuo vs alcanzable); y el hallazgo de que la loss tautológica mitigaba su propio daño |
| Proceso QA | 5/5 | Se declara que mi primer fix falló, que el align está en nivel de azar, y que el segundo rojo quedó abierto a propósito |
| Seguridad · DevOps | N/A | 25 pts fuera del denominador (R-01) |

**72/75 aplicables → 96/100.**

---

## 10. NO MEDIDO, declarado

- **El benchmark completo.** 500 ep × 3 semillas × 3 cerebros × 2 tareas. Sin eso, no hay afirmación de desempeño.
- **`SurvivalWorld` con los fixes no se entrenó más allá de 6 episodios**, solo para leer los contadores del guard.
- **El `energy` de SurvivalWorld llega a −0,134**, negativo, y el estimador lo persigue con una `sigmoid` acotada en (0,1). Sigue sin medir qué efecto tiene ese target inalcanzable. Es el siguiente test.
- **El presupuesto de PureMemory sigue desparejo** (P/D = 1,083). No se pidió.
- **No testé `ppo_seq_update`** con un chunk sintético de gradiente conocido.
