# 092 · Peritaje objetivo de `src/motor.py`

**Fecha:** 2026-08-25 18:30 (America/Buenos_Aires) · **Modo:** TITAN FULL · **Tipo de entrega:** peritaje

**Sujeto y su categoría (E-01):** `src/motor.py` en `titan/twohop-nulls`. Es un **instrumento** de auditoría científica, no un hallazgo ni un producto. Se lo evalúa como instrumento.

**Base empírica de este peritaje:** lectura completa del archivo más la corrida real de hoy (evidencia cruda en `docs/agents/evidencia/2026-08-25-motor-py-ejecutado-y-presupuesto-esp32-evidencia-cruda.md`). No es opinión sobre un archivo leído en diagonal.

<hr/>

## 1. El veredicto en una frase

> **Está sobre-ingenierizado en los guards y sub-ingenierizado en el diseño estadístico. Invirtió el esfuerzo.**

El aparato que impide auto-engañarse es de primer nivel. La pregunta que ese aparato está midiendo **no puede contestarse con el diseño elegido**. Así que el archivo vale mucho como **método** y hoy vale poco como **resultado**.

<hr/>

## 2. Lo que está genuinamente bien, y por qué es raro

### 2.1 Los tres estados están cableados en el código, no en un comentario

Esto es lo mejor del archivo y no es un detalle de estilo:

- `cosine_distance()` devuelve **NaN** cuando un vector colapsa, en vez de 1.0. Elegir 1.0 haría que un control **apagado** puntuara como máximamente diferenciado y le ganara al conectoma real.
- `rdi()` devuelve **(valor, n_validos, n_excluidos)**. Un RDI sobre 3 pares y uno sobre 1 par no son el mismo número.
- `normalize_spectral()` devuelve **(matriz, rho, convergio)**. Distingue convergencia de agotamiento de iteraciones.
- `global_rank_test()` marca **`NO_TESTEABLE`** cuando el null conserva exactamente la cantidad medida (`sd = 0`).

La mayoría del código científico colapsa «cero» con «no medí». Este no. **Cada guard es una hipótesis muerta convertida en código**, y eso es exactamente el activo que querés que quede cedible.

### 2.2 El guard de estabilidad es derivado, no tuneado

`|Im(tau)| < sqrt(1 - (1-Re)^2)`. Con `Re = 0,119` da **0,473116**, y el rango usado llega a 0,15. No es un número elegido a ojo: sale de la condición de que `|1-tau| < 1`. Y **aborta antes de gastar CPU**, lo cual es la diferencia entre un guard y un adorno.

Corrido hoy: acepta el default, rechaza 0,48, y el límite sale exacto.

### 2.3 El control del control

`test_uniform_choice_would_fail()` verifica que el método uniforme **sí** rompe el grado entrante. O sea: prueba que el test anterior **podía dar rojo**. Corrido hoy alteró **2.817 nodos**.

Un test que no puede fallar no mide nada, y este archivo lo trata como axioma en vez de como frase linda.

### 2.4 Dos nulls que contestan preguntas distintas

- Maslov-Sneppen: ¿esto es más que la secuencia de grados?
- Community-preserving: ¿esto es más que la arquitectura modular?

Y el CP **permuta** destinos existentes en vez de sortear uniformemente, con la razón escrita: sortear cambiaría el grado entrante y contaminaría justo lo que el null aisla. Eso es criterio, no receta.

### 2.5 Checksums de los insumos

`load_connectome()` verifica md5 del parquet y de las anotaciones, y fija el SHA de la rama de anotaciones. Es la clase de detalle que nadie agradece hasta que una tabla cambia bajo los pies.

<hr/>

## 3. Lo que está mal, en orden de gravedad

### 3.1 🔴 El experimento no puede ganar. Es un defecto de diseño, no de hipótesis

`N_NULLS = 9`. Con 9 nulls el **piso de p a dos colas es 2/(9+1) = 0,20**.

O sea: **incluso si el conectoma real fuera perfecto y los nueve nulls fueran horribles, el mejor p posible es 0,20.** El experimento está construido de forma que no puede producir un resultado publicable ni en el escenario ideal.

Corrido hoy: `p = 0,2000` exacto, con `S_real = 23,0` contra `S_null_min = 24,0`, o sea **0 de 9**. El grafo estructurado ganó el orden y perdió la significancia, **por el número de nulls**.

**Esto es lo más grave del archivo**, porque el resto de la maquinaria es impecable y está apuntada a un blanco que no se puede acertar. Gasto de cómputo sobre el objetivo equivocado.

### 3.2 🔴 Falta el brazo de control más importante, y es el que sostiene la tesis del motor

El archivo controla la **`tau` compleja** con `tau_r` (tau real, 0,119 + 0j). Bien.

**Pero no controla la `W` compleja.** La decisión de codificar el signo E/I como **fase** de un peso complejo es la apuesta conceptual central del motor, y **no tiene brazo de control**. Nunca se compara contra la alternativa obvia: misma matriz con **pesos reales con signo** (`+|w|` / `-|w|`), que es lo que hace cualquier modelo estándar.

Sin ese brazo no se puede decir si la aritmética compleja aporta algo o si es una reparametrización elegante de un signo. **Y ese es el claim que vende el motor.** Estado correcto: **NO MEDIDO**.

Peor todavía: `phase_jitter = 0,1` es un parámetro de modelado sin barrido ni justificación medida. Aparece como default y nadie lo interrogó.

### 3.3 🔴 `normalize_spectral` no cumple lo que promete, y lo hace en silencio

Medido hoy: devolvió **`rho = 14,62` con `conv = True`** en un régimen de grado alto y pesos lognormales.

El defecto es estructural: la función mide `rho` de la matriz **original**, escala por `target/rho`, y **nunca verifica el radio espectral de la matriz escalada**. El flag `convergio` reporta que la iteración de potencia converge, **no** que la normalización haya quedado en 0,99.

Es justo el antipatrón que el propio archivo persigue en otras funciones: **un guard que reporta sobre otra cosa que la que promete.** Necesita un chequeo posterior con su test que pueda dar rojo.

### 3.4 🟡 Toda la conclusión cuelga de 3 pares

Tres modalidades (visual, olfatoria, mecanosensorial) dan **3 pares** por snapshot. El RDI es el promedio de tres números. `rdi()` reporta bien cuántos son, lo cual es honesto, pero la honestidad no agranda la muestra.

Efecto grande con `n` chico es **muestra chica**, no señal débil, y tampoco es señal fuerte.

### 3.5 🟡 No es reproducible fuera de Kaggle

`/kaggle/working/datos` y `/kaggle/working/motor_resultados.json` están hardcodeados. Un tercero que clone el repo **no puede correrlo** sin editar el archivo. Para algo que querés dejar cedible, eso es una barrera gratuita.

### 3.6 🟡 Es un script, no un módulo

700 líneas con datos, dinámica, métricas, tests y experimento en el mismo archivo. Sin CLI, sin config, sin separación entre librería y corrida. Para un paper alcanza. Para producto o para que otro lo mantenga, no.

Y un detalle menor pero sintomático: el mapeo de anotaciones usa `for k in range(rid.shape[0])` con `names.index(...)` **dentro del loop**. Es O(n·m) puro Python en un archivo que en todo lo demás vectoriza con `bincount` y `searchsorted`. Se nota dónde estaba la atención y dónde no.

<hr/>

## 4. Y lo que el archivo NO es, para que no se lo infle

- **No es el motor del ESP32.** Medido hoy: **8,3× la SRAM** sólo para el estado vivo, **72,1× el flash**, **17.549×** el cómputo del DualBrain embebido. Ni comprimido a `complex64` entra en 8 MB de PSRAM.
- **No entrena.** Eso es una propiedad interesante del producto, pero acá es una consecuencia, no una demostración.
- **No es un hallazgo.** Sus salidas (`p = 0,6000`, `p = 0,2000`) son números de un experimento sub-dimensionado, no la nota del archivo.
- **No es la hipótesis del 96% fijo testeada.** Sigue sin testear.

<hr/>

## 5. Lo que haría, en orden, con el criterio declarado

**Criterio: qué convierte este instrumento en un resultado defendible afuera.** No qué es más lindo de correr.

1. **Agregar el brazo de control de `W` real con signo.** Es el hueco conceptual, no cuesta una corrida nueva grande, y es el único que puede sostener o matar la tesis de la aritmética compleja. Si la fase no gana contra el signo real, hay que saberlo ahora.
2. **Subir los nulls a 100.** Hoy el techo del experimento es peor que su hipótesis. Con 9 nulls no hay nada que rescatar; con 100, el piso de p baja a 0,0198.
3. **Arreglar `normalize_spectral`** con verificación posterior del radio espectral escalado, y un test que dé rojo si no queda en el target.
4. **Sacar las rutas de Kaggle** y meter el directorio por parámetro o variable de entorno.
5. **Ampliar las modalidades** más allá de tres, o declarar explícitamente que el RDI descansa en 3 pares.

El 1 y el 2 son los que cambian el expediente. El 3, 4 y 5 son higiene.

<hr/>

## 6. La nota, con su categoría declarada

<table><tbody><tr><th width="220" cell-bg-color="grey"><p><strong>dimensión</strong></p></th><th width="220" cell-bg-color="grey"><p><strong>nota</strong></p></th><th width="220" cell-bg-color="grey"><p><strong>por qué</strong></p></th></tr><tr><td width="220"><p>Disciplina anti-autoengaño</p></td><td width="220"><p><strong>9,5 / 10</strong></p></td><td width="220"><p>NaN vs 0, guard de tautología, control del control, checksums</p></td></tr><tr><td width="220"><p>Corrección matemática del núcleo</p></td><td width="220"><p><strong>8 / 10</strong></p></td><td width="220"><p>guard derivado y activación que preserva fase; −2 por el defecto real de <code>normalize_spectral</code></p></td></tr><tr><td width="220"><p>Diseño experimental</p></td><td width="220"><p><strong>4 / 10</strong></p></td><td width="220"><p>9 nulls con piso 0,20, falta el brazo de <code>W</code>, RDI sobre 3 pares</p></td></tr><tr><td width="220"><p>Reproducibilidad por terceros</p></td><td width="220"><p><strong>5 / 10</strong></p></td><td width="220"><p>rutas de Kaggle hardcodeadas, sin CLI</p></td></tr><tr><td width="220"><p>Valor como activo cedible</p></td><td width="220"><p><strong>8 / 10</strong></p></td><td width="220"><p>el método y los guards son lo transferible; el experimento hay que rehacerlo</p></td></tr></tbody></table>

> **Traducido:** como **instrumento** es de los mejores archivos del expediente. Como **experimento** está mal dimensionado y hay que rehacerlo con más nulls y con el brazo de control que falta. Y confundir esas dos notas es el error que ya se comió una vez este proyecto: **evaluar un instrumento con la rúbrica de un hallazgo.**

<hr/>

## 7. NO MEDIDO, declarado

1. **No se corrió sobre el conectoma real** en esta sesión. Los números de la corrida son de un grafo sintético con ley de Dale exacta; **los del paper siguen siendo los del paper**.
2. **El brazo de control de `W` real no existe todavía**: la afirmación «falta ese control» es una lectura del código, y el resultado de ese control es **NO MEDIDO**, no negativo.
3. **`null_maslov_sneppen()` no se ejecutó.** Se lo juzga por lectura, no por corrida.
4. **No se barrió `phase_jitter`.** Que no esté justificado no prueba que esté mal elegido.
5. **El defecto de `normalize_spectral` se midió en un régimen** (lognormal, grado alto). **No se verificó si aparece con los pesos reales del conectoma**, y eso hay que medirlo antes de tocar el paper.
6. **No se corrigió nada del archivo en este turno.** Este documento es peritaje, no fix.

```plain
--- METODO TITAN ---
Accion delicada: NO (lectura y juicio; ninguna modificacion de src/motor.py)
Modo aplicado:   TITAN FULL
Rubrica:         peritaje -> Completitud, Arquitectura del razonamiento,
                 Documentacion, Innovacion, Proceso QA aplicables
N/A declarados:  Ejecutabilidad, Seguridad, Testing, DevOps (55 pts): es un peritaje
Review externo:  no pedido, sin PR. DEUDA declarada.
Instrumento:     lectura completa de src/motor.py + corrida propia de hoy con
                 evidencia cruda commiteada en docs/agents/evidencia/
                 2026-08-25-motor-py-ejecutado-y-presupuesto-esp32-evidencia-cruda.md
```