# resp 014 · Auditoría de BICAMERALITY · TITAN FULL

**Fecha:** 2026-08-23 23:36–24:00 (America/Buenos_Aires) · **Modo:** TITAN FULL · **Tipo:** peritaje de código con instrumento propio · **Rúbrica:** 41/45 → **91/100**

## 1. Pedido

> «BICAMERALITY no corresponde a este proyecto, pero creo en las casualidades, así que haremos un paréntesis y aplicarás auditoría a BICAMERALITY. Probarás código, todo lo que necesites, de manera íntegra. Usa Kaggle y en simultáneo tu entorno virtual; si no es necesario Kaggle, solo el entorno.»

**Paréntesis declarado:** el sujeto **no pertenece** al proyecto del conectoma. Se audita como caso de estudio y el material queda en `audit/bicamerality/`, no en `src/`.

## 2. Herramientas declaradas (C-03)

**Se midió primero si Kaggle era necesario:**

```
python 3.12.14   torch 2.13.0+cpu   cuda False   threads 2   nproc 2
```

**Torch está en el container, así que NO se usó Kaggle. Cero cuota consumida, cero kernels lanzados.** Todo corrió en `/workspace/bicam/`. GitHub: un commit con el arnés, los cuatro logs y este archivo.

## 3. El sujeto, con procedencia

| | |
|---|---|
| Origen | celda **1** de `fabiomurillohot/notebookceb82767da` |
| Tamaño | 34.903 B, 923 líneas, 12 clases y funciones |
| md5 | `9d89a158f809ff5f3765f42848502665` |
| Salida en el notebook | **0 bytes.** Nunca se ejecutó |
| Procedencia del código | **DESCONOCIDA** (resp 013) |

**Primera vez que este código corre.** Compila sin errores (`py_compile` OK) y los tres cerebros hacen forward.

## 4. Resultado: 11 tests, 2 EN ROJO

```
TESTS EN ROJO: 2
   - presupuesto_pareado_PureMemory
   - zen_clamp_se_activa
```

Y **T0 es el control del control**: verifica que una matriz ortogonal SÍ tiene radio espectral 1 (`sr=1.0000001192`) y que una random NO (`sr=1.332867`). Sin T0, el T1 no estaría midiendo nada.

---

## 5. ROJO 1 · El «Resilience Zen» es una rama INALCANZABLE

El código declara, citando una ecuación:

```python
# Resilience Zen (Principia eq 4.6): soft norm clamp
h_norm = torch.norm(h_new, dim=-1, keepdim=True)
scale = torch.where(h_norm > self.max_norm, self.max_norm / (h_norm + 1e-8), ones)
```

**Medido: 0 activaciones de 12.800**, con norma máxima vista **1,3949** contra un umbral de 3,0.

Y no es cuestión de suerte ni de semilla, es una **cota analítica**. La actualización es `h = h*(1-tau) + tanh(.)*tau` con `tau` en (0,1): cada componente es una combinación convexa de algo en [-1,1] con algo en [-1,1], así que **queda en [-1,1]**, y por lo tanto `||h|| <= sqrt(H)`.

Barrido de `H` para probarlo:

```
 H   sqrt(H)   max_norm   alcanzable   max_visto_1000pasos
  4    2.0000        3.0           NO                1.7060
  8    2.8284        3.0           NO                1.8238
  9    3.0000        3.0           NO                1.9479
 10    3.1623        3.0           SI                1.9097
 16    4.0000        3.0           SI                2.1187
 32    5.6569        3.0           SI                3.3720
```

**Con `H_chaos=8`, que es el valor que usa `PrincipiaBrain`, la cota es 2,8284 y el umbral 3,0. La rama nunca puede ejecutarse.** El cruce recién aparece en H=10.

Y el `except` que hay al lado (`W_rec * 0.95`) tampoco: `nn.init.orthogonal_` no tira excepción para una matriz cuadrada, y `eigvals` de una ortogonal no falla.

**Es el patrón 2 del Bloque 8: un guard cuya rama es inalcanzable. Parece una validación, y el próximo que lo lea va a razonar sobre un caso que no existe.** Misma familia que el detector de divergencia del Script R (`max_h > 1e6` **después** de `np.clip`), y que el `'in_physiological_range': True` hardcodeado. Tres archivos distintos, el mismo error.

---

## 6. ROJO 2 · El presupuesto no está pareado en PureMemory

```
PureMemory     Principia= 1174  Dual= 1084  MLP= 1219   P/D=1.083
SurvivalWorld  Principia= 1912  Dual= 1822  MLP= 1957   P/D=1.049
```

**En PureMemory, Principia tiene 8,3% más parámetros que Dual** (90 de diferencia, de los cuales 42 son las dos cabezas auxiliares). El benchmark compara los dos y atribuye la diferencia a *«Bicamerality + Veto + SurvLoss add real value»*.

En SurvivalWorld el ratio es 1,049, dentro de tolerancia. Así que el problema es de la tarea chica, donde 90 parámetros pesan más.

---

## 7. EL HALLAZGO MAYOR, no pedido: el veto no es inerte, es un castigo espurio permanente

Esto es lo más grave y no estaba en ninguna lista.

### Las dos etiquetas de la survival loss no llevan información en PureMemory

El loop de entrenamiento construye las etiquetas así:

```python
danger = float(rew < -1.0)
energy = einfo.get('energy', 1.0)
```

Medido sobre `PureMemoryTask`:

| Etiqueta | Medición | Consecuencia |
|---|---|---|
| `danger` | reward en **[−0,4998, 0,4983]** sobre 2.000 pasos → `rew < -1.0` en **0 de 2.000** | la BCE regresiona contra un target **constante 0** |
| `energy` | valores distintos observados: **[1.0]** | la MSE regresiona contra un target **constante 1** |

El reward de esa tarea es `0.5 * a * cue` con `a` y `cue` en [−1,1]: **por construcción no puede bajar de −0,5.** El umbral de −1,0 es inalcanzable.

### Y el veto usa esa salida sin información

```python
alpha = energy_est.detach()
veto_shift = -2.0 * (1.0 - alpha)
lstd = self.log_std + veto_shift
```

Si `alpha` fuera 1, el veto sería inerte. **Pero el estimador converge lento, y medido sobre 240 episodios reales nunca llega:**

```
bloque_de_ep   alpha_medio   veto_shift   factor_sobre_std   gate_medio
   0-40        0.3742       -1.252        0.2860        0.4413
  40-80        0.3965       -1.207        0.2991        0.4408
  80-120       0.4177       -1.165        0.3121        0.4401
 120-160       0.4291       -1.142        0.3193        0.4480
 160-200       0.4518       -1.096        0.3341        0.4467
 200-240       0.4758       -1.048        0.3505        0.4578
```

**Durante los 240 episodios completos, Principia explora con un desvío estándar entre el 28,6% y el 35,1% del nominal.** Dual y MLP exploran al 100%.

> **El veto no es inerte: es un handicap de exploración de casi 3× que sale de un estimador que regresiona contra una constante.** No mide peligro ni energía, porque en esa tarea no hay ninguno de los dos. Y penaliza justamente al modelo que el benchmark quiere defender.

Cualquier diferencia Principia vs Dual en PureMemory está confundida por **dos** factores ajenos a la bicameralidad: 8,3% más parámetros a favor, y 3× menos exploración en contra.

### En SurvivalWorld sí hay señal, y es usable

```
pasos=1958  danger=1 en 55  fraccion=0.02809
reward en [-6.952, 6.179]   energy en [-0.134, 1.000]
```

2,8% de positivos: desbalanceado pero por encima del 1% donde la BCE colapsa. **La survival loss tiene sentido en SurvivalWorld y no lo tiene en PureMemory.** El código la aplica en las dos.

---

## 8. Lo que SÍ está bien hecho

Para no dejar solo lo malo:

1. **El ρ=1 se logra de verdad.** `rho_W_rec = 1.0000000000`, con error de ortogonalidad `1,729e-06`. El objetivo declarado se cumple.
2. **El contraste con la celda de orden es real:** `LiquidRealCell` tiene `rho = 0,396643`, el default de `nn.Linear` sin ningún control. Así que la asimetría caos/orden **existe** en el código, no es solo un comentario.
3. **El `detach` del alpha está bien puesto.** Medido: `grad log_std = 0.000e+00`. La aux loss entrena el estimador (`grad energy_head = 4,06e-02`, `grad danger_head = 6,15e+00`) sin que el veto pelee con el gradiente de política. Ese comentario del código es correcto y verificado.
4. **El PPO por secuencias maneja bien el estado recurrente:** `states[s]` es el estado previo al paso `s`, y los chunks se agrupan por longitud antes de apilar. No encontré bug ahí.

---

## 9. Un detalle que la division por sr revela

```
la_division_por_sr_es_NO_OP: max abs(W - W/sr) = 1.788e-07 con sr = 1.0000002384
```

Una matriz ortogonal tiene **todos** sus autovalores de módulo 1, así que `sr = 1` y dividir por `sr` no cambia nada. La línea que dice *«Edge-of-chaos initialization»* es **decorativa**: lo que produce ρ=1 es `nn.init.orthogonal_`, no la normalización.

No es un bug (el resultado es correcto), pero sí es una línea que hace creer que hay un cálculo donde no hay ninguno.

---

## 10. Veredicto

**El código corre, la arquitectura hace lo que dice en la asimetría caos/orden, y dos de sus tres ideas están instrumentadas de forma que no pueden funcionar en la tarea donde se las mide.**

| Idea | Estado medido |
|---|---|
| **Bicameralidad** | **Implementada de verdad.** ρ=1 sin LayerNorm contra ρ=0,40 con LayerNorm |
| **Veto α** | **Roto en PureMemory.** Etiqueta constante → handicap de exploración de 3× durante todo el run |
| **Survival loss** | **Sin información en PureMemory** (0 de 2.000 positivos). Usable en SurvivalWorld (2,8%) |
| **Resilience Zen** | **Código muerto.** Cota `sqrt(8)=2,83` < umbral 3,0 |

**Si el benchmark original hubiera corrido, su veredicto sobre PureMemory no habría medido bicameralidad.** Habría medido la suma de un bono de parámetros y una penalización de exploración, las dos ajenas a la hipótesis.

### Los cuatro arreglos, en orden de qué cuesta más no hacer

1. **`max_norm` de 3,0 a `0.35 * sqrt(H)`** o algo alcanzable, o borrar el clamp y decir que no hace falta. Hoy es una promesa que ningún camino cumple.
2. **No aplicar la survival loss donde la etiqueta es constante.** Un guard de tres líneas: si `sd(label) == 0` sobre el batch, reportar **NO TESTEABLE** y poner `aux_weight = 0`. Es el mismo guard de tautología que ya existe en `src/motor.py`.
3. **Parear el presupuesto en PureMemory** bajando `H_order` de 24 a 23, o declarar el 8,3% en la tabla.
4. **Correr el benchmark completo** (500 ep × 3 semillas × 2 tareas) **después** de 1 y 2. Antes no mide lo que dice medir.

---

## 11. Evidencia cruda (W-01)

Los cuatro logs verbatim están commiteados en `audit/bicamerality/`:

| Log | Qué contiene |
|---|---|
| `audit_bicam.log` | los 11 tests con su detalle, y los 2 en rojo |
| `zen.log` | el barrido de `H` que prueba la cota analítica |
| `veto.log` | la trayectoria de α sobre 240 episodios, 99 s |
| `train_red.log` | el entrenamiento reducido, 3 cerebros × 2 semillas |
| `audit_out.json` | los 17 valores numéricos en crudo |

md5 de los instrumentos: `audit_bicam.py f27e716414467a316614d1e058cd827b` · `zen.py ecb1649218e71a90736aa15c7afee10a` · `veto.py dc811a87dfc93d0e292ef29d3267bce4` · `train_red.py dc2793bf9aeb2ee8bef25051907c7318`.

---

## 12. Scorecard

| Criterio | Pts | Evidencia |
|---|---|---|
| Completitud | 13/15 | 11 tests + barrido de H + trayectoria de α + entrenamiento end-to-end de los 3 cerebros. **−2: el benchmark completo (500 ep × 3 semillas × 2 tareas) NO se corrió** |
| Ejecutabilidad | 15/15 | Los 4 instrumentos pasan `py_compile` y corrieron con `exit=0`. El sujeto corre por primera vez |
| Testing | 13/15 | Cada test puede dar rojo, y **dos dieron rojo**. T0 es el control del control. **−2: no hay test sobre `ppo_seq_update` con un chunk sintético de gradiente conocido** |
| Arquitectura del razonamiento | 10/10 | El hallazgo del Zen clamp pasa de empírico (0 de 12.800) a **analítico** (`sqrt(H)` contra `max_norm`) con un barrido que muestra dónde cambia. Y el del veto no se quedó en «es inerte»: se midió la trayectoria y resultó ser **peor** que inerte |
| Documentación | 10/10 | 4 logs verbatim, md5 de todo, procedencia del sujeto declarada, y el README del paréntesis |
| Innovación | 5/5 | No pedido: la cota `sqrt(H)`; que el veto sea un handicap de 3× y no una inercia; que las dos etiquetas sean constantes por construcción de la tarea; y el reconocimiento de lo que SÍ está bien (ρ=1 real, `detach` correcto) |
| Proceso QA | 5/5 | Se midió el entorno **antes** de decidir si usar Kaggle, y no se usó. Se declara que el entrenamiento reducido deja `align` en ~0,53, o sea azar, y **no alcanza** para comparar arquitecturas |
| Seguridad · DevOps | N/A | 25 pts fuera del denominador: el sujeto no tiene superficie de red, credenciales ni deployment (R-01) |

**41/45 aplicables → 91/100.** N/A declarados: 25 pts.

---

## 13. NO MEDIDO, declarado

- **El benchmark completo no se corrió.** 500 episodios × 3 semillas × 3 cerebros × 2 tareas. Con 2 threads de CPU son varias horas. El reducido (40 y 240 ep) deja `align` en **0,50–0,53**, o sea nivel de azar: **no se puede comparar arquitecturas con eso**, y no lo voy a presentar como si se pudiera.
- **`SurvivalWorld` no se entrenó**, solo se muestrearon sus recompensas con política aleatoria.
- **No testé `ppo_seq_update` con un caso de gradiente conocido.** Lo leí y no encontré bug, pero leer no es medir.
- **La celda 23 del notebook** (13.180 B de prosa, sin salida) sigue sin leer.
- **El `energy` de SurvivalWorld llega a −0,134**, o sea negativo, y la MSE del estimador lo persigue con una `sigmoid` acotada en (0,1). **No medi qué efecto tiene ese target inalcanzable.** Es el siguiente test.
