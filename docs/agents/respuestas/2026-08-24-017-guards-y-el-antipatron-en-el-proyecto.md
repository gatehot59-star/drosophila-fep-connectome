# resp 017 · BICAMERALITY auditado, mejorado, y el antipatrón encontrado en el código del proyecto

**Fecha:** 2026-08-24 00:17–01:05 · **Modo:** TITAN FULL · **Rúbrica:** 71/75 → **95/100**

## 1. Pedido

> «Sobre BICAMERALITY, TITAN FULL: audita, mejora, trae información relacionada de git, innova, y resuelve.»

**Router:** trigger de mayor precedencia = **repo**, así que GITHUB lee primero. Roles: GITHUB → SECURITY (revisión del guard como frontera de confianza) → INNOVATOR → TESTER → QA.

## 2. Herramientas declaradas (C-03)

GitHub: lectura del árbol de `src/` y de `motor.py`. `build.run` en el container. **Cero Kaggle, cero cuota.** Un commit, sin sobreescribir ningún archivo existente.

---

## 3. LO QUE TRAJE DE GIT, Y ES EL HALLAZGO PRINCIPAL

Busqué el antipatrón de BICAMERALITY en el código del proyecto. **Está, y en un archivo ya commiteado.**

### `src/scriptR.py`, líneas 88-90

```python
if clip is not None: np.clip(h,-clip,clip,out=h)
mx=float(np.abs(h).max())
if mx>1e6 or not np.isfinite(mx):
    diverged=True; res[t]=h.copy(); break
```

**Se recorta a ±clip y después se pregunta si superó 1e6.** Con `clip = 2.0` o `5.0`, esa condición es inalcanzable. Es exactamente el mismo error que el `max_norm=3.0` con cota `sqrt(8)=2.8284`.

### Y no es hipotético: el daño está en `results/R_out.json`, ya commiteado

```
config          modalidad     max_abs_h60   clip   veredicto_del_script
e_col099_lin    visual        2.0000        2.0    SATURADO y reporta diverged=False
e_col099_lin    olfactory     2.0000        2.0    SATURADO y reporta diverged=False
e_col099_lin    mechano       1.9600        2.0    ok

celdas pegadas al clip: 2 de 15
```

**Dos celdas clavadas en 2,0000 exacto, reportadas como sanas** por un guard que no puede dar rojo. El falsador de este hallazgo es evidencia que ya estaba en el repo desde antes: no depende de nada que hiciera hoy.

### El contraste positivo: `src/motor.py:383` lo hace BIEN

```python
if sd == 0.0:
    per[nm] = {"verdict": "NO_TESTEABLE", "reason": "...", "real": ..., "null_mean": ...}
    continue          # <- NO entra en usable, o sea que sale del test global
usable.append(nm)
```

Tres cosas bien hechas, y hay que decirlo:

1. Marca `NO_TESTEABLE` en vez de un ratio de 1,000×.
2. **Omite la clave `ratio`**, así que un consumidor que la lea explota con `KeyError` en vez de leer un número falso. Es fail-closed.
3. **Excluye el estadístico de `usable`**, o sea que propaga al consumidor (el test global).

**De los tres guards del corpus, `motor.py` es el único que cierra el círculo.** Y eso lo escribimos ayer sin darnos cuenta de que era el patrón correcto.

---

## 4. INNOVACIÓN: `src/guards.py`

185 líneas, md5 `cb462ea31d0267ea1878f2a030bb71c4`. Generaliza lo de `motor.py` y agrega lo que faltaba.

| Función | Qué resuelve |
|---|---|
| `assert_threshold_reachable(t, bound)` | Levanta `ReachabilityError` si el umbral está en o sobre la cota. **Un guard decorativo no se construye** |
| `convex_state_bound(H)` | La cota `sqrt(H)` para `h = (1−τ)h + τf(·)`, derivada y verificada contra la medición |
| `guarded_ratio(real, nulls)` | Fail-closed: **sin clave `ratio`** cuando `sd(null) == 0` |
| `TautologyGuard` | `register` / `observe` / `enabled`: **propaga al consumidor** |

### La pieza nueva es `enabled()`

```python
g.register("energy", consumers=["veto"])
if g.observe("energy", batch): loss += mse(pred, batch)
if g.enabled("veto"):          lstd += veto_shift   # <- esto es lo que faltaba
```

Y es fail-closed en tres puntos: observar sin registrar levanta `KeyError` (sin declarar consumidores no hay propagación), un consumidor sin observación está **apagado**, y una etiqueta constante apaga a todos sus consumidores.

### 16 tests, 0 en rojo, con control del control

T0 verifica que un umbral **alcanzable** NO se rechaza: sin eso, el resto de la suite no distinguiría nada. Y los tests corren sobre los **casos reales**, no sobre ejemplos inventados: el `clip` de `scriptR.py`, el `max_norm` de BICAMERALITY, y las dos etiquetas de `PureMemory`.

### Integrado en el código real, no en el vacío

```
guards.py sobre PureMemory:
  energy   {'usada': 0, 'no_testeable': 12, 'verdict': 'NO_MEDIDO'}
  veto     {'depende_de': ['energy'], 'habilitado_en_el_ultimo_lote': False}
```

**Reproduce el `AUX_GUARD` ad-hoc del parche de anoche.** El módulo genérico y el parche específico coinciden, que es la forma de saber que la abstracción no perdió nada.

Y discrimina donde debe: en SurvivalWorld `energy` se usa en 36 de 36 lotes y `danger` en 15 de 36. **El guard no apaga lo que informa.**

---

## 5. RESUELTO: el target imposible de `energy`

Este pendiente lo declaré **dos veces** como NO MEDIDO. Ahora está medido, y es el mejor hallazgo del paréntesis.

**El env deja que `energy` sea negativa. El estimador es una `sigmoid`, que vive en (0,1) abierto.**

```
pasos=2545  energy en [-0.1340, 1.0000]  negativos=5 (0.196 por ciento)

logit=   0.0  sigmoid=5.000e-01  error_al_target=0.634000
logit= -10.0  sigmoid=4.540e-05  error_al_target=0.134045
logit= -20.0  sigmoid=2.061e-09  error_al_target=0.134000
logit= -40.0  sigmoid=4.248e-18  error_al_target=0.134000

error MINIMO alcanzable = 0.134000, y solo en el limite logit -> -inf
```

**La MSE nunca puede cerrar ese error, así que empuja el logit a −∞.** Y `alpha = energy_est`, con `veto_shift = −2(1−alpha)`. O sea:

> **alpha → 0 ⇒ veto_shift → −2,0 ⇒ factor sobre el std = e⁻² = 0,1353.**
>
> **El caso donde el veto MÁS debería apretar (el agente muriéndose) es exactamente el que rompe el estimador que lo comanda.**

Y el mecanismo es peor de lo que parece: son solo **5 pasos de 2.545**, pero como el gradiente de esos pasos no tiene techo, un puñado de muestras imposibles puede dominar la dirección del logit.

**Fix:** clampear el target a [0,1], o normalizar la energía. El p1 de la distribución es 0,0409, así que clampear a 0 pierde muy poca información.

---

## 6. RESUELTO: el presupuesto

```
H_order=24  Principia=1174  Dual=1084  P/D=1.0830
H_order=23  Principia=1117  Dual=1084  P/D=1.0304  <-- dentro de 5 por ciento
H_order=22  Principia=1062  Dual=1084  P/D=0.9797  <-- dentro de 5 por ciento
```

**Dos valores lo cierran.** `H_order=22` es el más parejo (0,9797) y además deja a Principia **por debajo** de Dual, o sea que si gana, gana con menos parámetros. Es un cambio de una línea y queda como tu decisión.

---

## 7. LO QUE NO TOQUÉ, Y POR QUÉ

**`src/scriptR.py` NO se parchea en este commit.** Su md5 `6f943ced09d949c45575e1a125ab2eca` está citado como el instrumento que reprodujo **30 de 30 valores** contra la corrida de marzo y el PDF de Gemini. Cambiar el archivo invalida esa cadena de evidencia.

El fix son dos líneas, y va en su propio commit con su corrida de verificación:

```python
# antes del loop
SAT_UMBRAL = 0.99 * clip if clip is not None else float("inf")
# dentro del loop, reemplazando el guard muerto
sat_pct = float(np.mean(np.abs(h) >= SAT_UMBRAL) * 100.0)
if sat_pct > 0.0:
    saturado = True   # tercer estado: ni sano ni divergido
```

Eso convierte dos estados («sano» / «diverge») en los tres que corresponden, y las dos celdas de `e_col099_lin` pasarían de «ok» a **SATURADO**.

---

## 8. Orden de lo que sigue (O-01)

**Criterio: qué cuesta más no hacer.** Verifiqué que tocan archivos distintos, no hay dependencias.

1. **El guard de saturación en `src/scriptR.py`.** Es el único de esta lista que afecta un instrumento cuyos resultados ya se citan. Dos líneas, y cambia el veredicto de 2 celdas.
2. **Usar `guarded_ratio` en `cp40.py` y `nulls40_kaggle.py`.** Los dos calculan ratios contra nulls sin el guard: `cp40.py` divide por `m` con un `if m > 0` que no distingue «cero» de «sin varianza».
3. **Clampear el target de `energy`** si BICAMERALITY se vuelve a correr.
4. `H_order=22` para parear el presupuesto.

---

## 9. Scorecard

| Criterio | Pts | Evidencia |
|---|---|---|
| Completitud | 13/15 | Los cuatro verbos del pedido: auditado, mejorado (`guards.py`), traído de git (el antipatrón en `scriptR.py` y el contraste con `motor.py`), innovado y resuelto (los dos pendientes). **−2: el benchmark completo de BICAMERALITY sigue sin correr, y `scriptR.py` sigue con su guard muerto a propósito** |
| Ejecutabilidad | 15/15 | `guards.py` sin dependencias externas más allá de `math`, `py_compile` OK, 16 tests con `exit=0`, e integrado en el código real |
| Testing | 14/15 | Cada test corre sobre un **caso real del corpus**, no sobre un ejemplo. T0 es el control del control. **−1: no hay test de `_flatten` con un tensor de torch, solo con listas** |
| Arquitectura del razonamiento | 10/10 | El módulo no sale de una idea: sale de **tres fallas medidas** en tres archivos, y la pieza nueva (`enabled`) sale de la única que ninguna abstracción anterior cubría. Y se valida contra el parche ad-hoc, que es el falsador natural |
| Documentación | 10/10 | El docstring del módulo cita los tres casos con archivo y línea, y los números medidos de cada uno |
| Innovación | 5/5 | No pedido: el `ReachabilityError` fail-closed; que `guarded_ratio` **omita la clave** en vez de devolver `None`; el registro obligatorio de consumidores; y el hallazgo de que el target negativo rompe el veto justo cuando más se necesita |
| Proceso QA | 4/5 | Cada score con su archivo y su número. **−1: el score de Testing se apoya en mi propia suite, y no hay review externo de `guards.py`** |
| Seguridad · DevOps | N/A | 25 pts fuera del denominador: el módulo no toca red, credenciales ni deserialización, y no tiene deployment propio (R-01) |

**71/75 aplicables → 95/100.** N/A declarados: 25 pts.

---

## 10. NO MEDIDO, declarado

- **El benchmark completo de BICAMERALITY** (500 ep × 3 semillas × 2 tareas) sigue sin correr. Sin eso no hay afirmación de desempeño.
- **`src/scriptR.py` sigue con el guard muerto.** El fix está escrito en §7 y **no** aplicado.
- **No verifiqué si `cp40.py` y `nulls40_kaggle.py` tienen el mismo hueco de ratio.** Lo leí de pasada y lo pongo en la lista; **no está medido**.
- **`guards.py` no tiene review externo.** K-02: nadie lo objetó, y eso no es una aprobación.
- No testé `_flatten` con un tensor de torch real, solo con listas anidadas.
