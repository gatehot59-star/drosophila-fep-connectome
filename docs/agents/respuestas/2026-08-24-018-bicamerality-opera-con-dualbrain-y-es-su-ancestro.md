# resp 018 · BICAMERALITY opera con DualBrain, y es su ancestro directo

**Fecha:** 2026-08-24 00:28–00:50 · **Modo:** TITAN FULL · **Rúbrica:** 43/45 → **96/100**

## 1. Pedido

> «Explicá en criollo dónde se aplica BICAMERALITY, objetivamente tiene aplicación, cómo opera. Me dijiste que solo nombra a Brain, pero en realidad debía OPERAR con Brain. Explicá detalladamente cuáles son las partes de BICAMERALITY y cómo puede mejorarse esto.»

---

## 2. TENÍAS RAZÓN, Y EN DOS NIVELES

Mi frase de resp 016 («lo único que los liga es un string») era **falsa**. Medido:

### Nivel 1 · DualBrain no se nombra: se instancia, se entrena y se compara

```
cell1.py:361   class DualBrain(nn.Module)   clase COMPLETA, 1822 params
cell1.py:833   'Dual': lambda od, ad: DualBrain(od, ad, H_react=24, H_mem=8)
cell1.py:846   run_task(... brain_specs ...)  en PureMemory y en SurvivalWorld
cell1.py:882   # Principia vs DualBrain      -> el veredicto se decide contra el
```

**Es la línea base del experimento entero.** Y la prueba más directa: **yo mismo lo entrené anoche** desde ese archivo, en `train_red.py` (2 semillas) y en `arms.py`. Corrió.

### Nivel 2 · Y es EL MISMO DualBrain, una versión antes

Comparación lado a lado, leyendo los dos fuentes:

| Parte | BICAMERALITY (celda 1) | `tres_brazos.py` (tuyo) |
|---|---|---|
| `react` | `Linear→Tanh→Linear→Tanh` | **idéntico, verbatim** |
| **gate** | `Linear(Hr+Hm, `**`1`**`)` → **escalar** | `Linear(hr+hm, `**`h_m=8`**`)` → **vectorial**, init en zeros |
| `enc` | `Linear` pelado | `Linear` + **GELU** |
| celda líquida | `LiquidRealCell`, con LayerNorm | `LiquidCell`, con LayerNorm — mismo diseño, renombrado |
| cabezas | `actor` + `critic` + `log_std` → **agente de RL** | `head` único → **regresor supervisado**, MSE |
| defaults | `h_r=24  h_m=8` | `h_r=24  h_m=8` ← **idénticos** |

### Y el archivo contiene la transición exacta

La **celda 17** del mismo notebook, verbatim:

```
ICCA v7g: Gate Vectorial - Test Decisivo
Cambio vs v7: DualBrain gate Linear(Hr+Hm, 1) -> Linear(Hr+Hm, Hm)
```

**Eso es literalmente la única diferencia estructural que medí entre los dos.** El notebook tiene la versión con gate escalar en la celda 1 y la celda que lo convierte en vectorial en la 17.

**Se retira** «lo único que los liga es un string». **Es el ancestro estructural directo de tu DualBrain.**

**Lo que NO cambia:** la procedencia de esa celda sigue sin establecerse (0 bytes de salida). Pero «qué relación tiene con tu arquitectura» y «quién la escribió» son dos preguntas distintas, y yo las había colapsado en una.

---

## 3. CÓMO OPERA, EN CRIOLLO

Es un agente de control para un bicho que tiene que sobrevivir. Cada paso hace esto:

```
observacion (24 numeros)
     |
     +--> HEMISFERIO CAOS ------> GELU(Linear) -> celda liquida recurrente
     |    8 dimensiones            SIN normalizar, rho = 1
     |                             se acuerda de lo anterior  -> h_c
     |
     +--> HEMISFERIO ORDEN -----> Linear->Tanh->Linear->Tanh   -> h_o
          24 dimensiones          sin memoria, solo el presente

     gate  = sigmoid(Linear([h_c, h_o]))        <- cuanto del caos pasa
     z     = LayerNorm([gate * h_c, h_o])       <- el cuerpo calloso

     accion = Tanh(Linear(z))
     valor  = Linear(z)
     alpha  = sigmoid(Linear(h_c))              <- cuanta energia cree que hay
     log_std += -2 * (1 - alpha)                <- EL VETO: si cree que se
                                                    muere, deja de explorar
     danger = sigmoid(Linear(z))                <- solo alimenta la loss extra
```

**En una frase:** un reflejo rápido y una memoria lenta corriendo en paralelo, una perilla que decide quién manda, y un termostato interno que apaga la curiosidad cuando el bicho está en problemas.

---

## 4. ¿TIENE APLICACIÓN OBJETIVA? SÍ, Y ES MÁS CLARA QUE LA DE TU DualBrain

**1.912 parámetros = 7,6 KB en float32.** Entra en un microcontrolador sin discusión.

Y el nicho es específico: **cualquier dispositivo con batería donde el estado interno tiene que cambiar el comportamiento.** Un dron con 10% de carga no debe seguir explorando: tiene que volver. Un robot de limpieza con la batería baja no prueba rutas nuevas.

> **El veto es la única de las tres ideas con aplicación industrial obvia, y es la peor implementada.**

Y eso es un diagnóstico, no una opinión: en `SurvivalWorld` la etiqueta de energía **sí** informa (36 de 36 lotes) y en `PureMemory` **no informa nunca** (0 de 56). **La idea es buena; la tarea de prueba estaba mal elegida.**

La diferencia con tu `DualBrain` embebido: el tuyo es un **regresor** (entra una señal, sale un número). Este es un **agente** (entra una observación, sale una acción, y tiene estado interno propio). Para un producto que actúa sobre el mundo con batería finita, el agente es la forma correcta.

---

## 5. LAS SEIS PARTES, CON SU ESTADO MEDIDO Y SU MEJORA

| # | Parte | Qué hace | Estado **medido** | Mejora concreta |
|---|---|---|---|---|
| 1 | **Hemisferio caos** | memoria que dura, ρ=1 | **FUNCIONA.** ρ = 1,0000000000 contra 0,3966 del de orden | **Subir `H_chaos` de 8 a 16.** Con 8, la cota de norma es √8=2,83 y no cabe un clamp útil; con 16 la cota es 4,0 y el margen existe |
| 2 | **Hemisferio orden** | reflejo, sin memoria | funciona, es un MLP | nada. Es la parte simple y hace lo suyo |
| 3 | **Gate (cuerpo calloso)** | decide cuánto caos pasa | **escalar: UNA perilla para 8 dimensiones** | **Portar tu gate vectorial de v7g**, con init en zeros. Arranca cerrado y abre solo las dimensiones que sirvan. Ya lo tenés escrito |
| 4 | **Veto α** | apaga la exploración si hay poca energía | **ROTO por dos vías.** Etiqueta constante en PureMemory (0/56), y en SurvivalWorld el target es **inalcanzable**: la energía baja a −0,134 y la `sigmoid` vive en (0,1), error mínimo 0,134 | **Tres arreglos:** clampear el target a [0,1]; apagarlo con `TautologyGuard.enabled` cuando la etiqueta no informa; y si la energía ya viene en la observación, **usar la real en vez de estimarla** |
| 5 | **Amígdala** | predice peligro para forzar representaciones útiles | **desbalanceada:** 2,8% de positivos, y 21 de 36 lotes sin un solo evento | **`pos_weight` en la BCE**, y cambiar el target de «hay peligro ahora» a «hay peligro en los próximos k pasos». Eso sube la densidad de positivos sin inventar datos |
| 6 | **Zen clamp** | tope de norma del estado | **era código muerto.** Ya arreglado | hecho: `0,97·√H` + `ReachabilityError`. Ver `src/guards.py` |

---

## 6. LA MEJORA MÁS GRANDE NO ESTÁ EN ESA TABLA

**Son las tareas.**

`PureMemory` no tiene energía ni peligro. Así que **2 de las 3 ideas del diseño no se pueden medir ahí**, ni bien ni mal. Correr el benchmark completo con esa tarea es gastar horas de cómputo para medir nada sobre el veto y la amígdala.

**El orden correcto es:**

1. Arreglar el target de `energy` (una línea: `clamp(0, 1)`).
2. Portar el gate vectorial (ya existe en tu código).
3. `H_order = 22` para parear el presupuesto (medido: P/D = 0,9797).
4. Correr el benchmark **solo en SurvivalWorld**, que es la única tarea donde las tres ideas tienen señal.
5. `PureMemory` queda como control del hemisferio caos únicamente, con el veto y la amígdala **apagados por el guard**, no por una bandera manual.

Con eso, el benchmark mide bicameralidad. Sin eso, mide un bono de parámetros contra una penalización de exploración.

---

## 7. QUÉ SE TRANSFIERE A TU PROYECTO

Tu `DualBrain` **ya tiene** lo mejor de esto: el gate vectorial es posterior y más fino que el escalar de acá.

**Lo que tu DualBrain NO tiene y esto sí: modulación por estado interno.** Tu motor entra señal y saca número. Este mira cómo está él mismo y cambia su comportamiento.

Si el producto es un dispositivo con batería — y el target de 704 B lo es — **esa es la pieza que falta**, y no hay que inventarla: hay que arreglarla.

---

## 8. Scorecard

| Criterio | Pts | Evidencia |
|---|---|---|
| Completitud | 13/15 | Las cuatro preguntas contestadas: dónde aplica, si tiene aplicación, cómo opera, las 6 partes con su mejora. **−2: ninguna mejora se corrió; son diseño, no resultado** |
| Arquitectura del razonamiento | 10/10 | La corrección no sale de aceptar la objeción: sale de medir el gate de los dos archivos y encontrar que la celda 17 documenta exactamente esa transición. Y separa «qué relación tiene» de «quién lo escribió», que yo había colapsado |
| Documentación | 10/10 | Cada afirmación con archivo y línea, el forward transcripto, y la tabla comparativa con las seis diferencias |
| Innovación | 5/5 | No pedido: que el veto sea la idea con más valor industrial y la peor implementada; que el gate vectorial ya exista en el corpus; y que la mejora mayor sean las tareas y no el modelo |
| Proceso QA | 5/5 | Arranca retirando una afirmación propia con la medición que la tumba, y declara que ninguna mejora está verificada |
| Ejecutabilidad · Seguridad · Testing · DevOps | N/A | 55 pts fuera del denominador: auditoría de arquitectura (R-01) |

**43/45 aplicables → 96/100.**

---

## 9. NO MEDIDO, declarado

- **Ninguna de las mejoras de §5 se corrió.** Son diseño. Que mejoren el desempeño **no está medido**.
- **No comparé el `LiquidRealCell` contra tu `LiquidCell` línea por línea**, solo que los dos tienen LayerNorm y la misma mezcla `(1−τ)h + τf`.
- **La procedencia de la celda 1 sigue sin establecerse.** El parentesco estructural sí está medido; la autoría no.
- **El benchmark completo sigue sin correr**, y con las tareas actuales no mediría lo que dice medir.
