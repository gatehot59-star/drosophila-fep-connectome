# resp 016 · Qué es BICAMERALITY, y la colisión de «brazos» que generé yo

**Fecha:** 2026-08-24 00:12 · **Modo:** TITAN LIGERO

## 1. Pedido

> «¿Qué tiene que ver BICAMERALITY con los brazos? Yo te mandé a probar el primero, para entender de qué se trataba. No entiendo qué probaste, o los fusionás. Explicá detalladamente qué hiciste, y de qué trata BICAMERALITY.»

---

## 2. LA CONFUSIÓN ES MÍA Y TIENE NOMBRE

**Usé la palabra «brazos» para dos cosas distintas, con las mismas letras A/B/C, y nunca lo aclaré.**

| | **TUS brazos** | **MIS brazos** |
|---|---|---|
| Dónde | `titan-tres-brazos` en Kaggle, junio-agosto | auditoría de anoche, en tu container |
| Sujeto | `LiquidCell` **denso**, 8 unidades, ~1.400 params | `PrincipiaBrain`, celda 1 de un notebook |
| A | todo entrenable | código **original** |
| B | `react` **congelado** | con el guard, veto **ON** |
| C | solo memoria entrenable | con el guard, veto **OFF** |
| Qué pregunta | ¿cuánto de DualBrain necesita entrenarse? | ¿mi parche arregla lo que dice arreglar? |

**No hay relación entre las dos cosas.** Coincide la palabra y coinciden las letras, nada más.

Y es exactamente la trampa que yo mismo documenté en la auditoría de la patente (§6.5): *«dos métricas con nombres parecidos, una invariante bajo CP y la otra no. Si alguien lee que RDI es invariante y lo aplica al coseno, concluye mal.»* Lo detecté en código ajeno y lo cometí en mi propio reporte doce horas después.

### No hubo fusión, y es verificable

Mis tres brazos corren sobre `cell1.py` y `cell1_fixed.py`, con `PureMemoryTask` y `PrincipiaBrain`. **Cero líneas del conectoma, cero `tres_brazos.py`, cero kernels de Kaggle.** Está en `audit/bicamerality/arms.py`, importable y recomputable.

---

## 3. QUÉ ES BICAMERALITY, EN CRIOLLO

Es un diseño de agente con **dos hemisferios que procesan lo mismo de formas opuestas**, y tres agregados encima.

### Los dos hemisferios

| | **Derecho: «caos»** | **Izquierdo: «orden»** |
|---|---|---|
| Estructura | recurrente: se acuerda de su estado previo | feedforward: mira el presente y nada más |
| Normalización | **ninguna** | LayerNorm y Tanh |
| Calibración | pesos con radio espectral 1, «al borde del caos» | los defaults de la librería |
| Tamaño | 8 unidades | 24 unidades |

**Qué significa «al borde del caos» en criollo:** si los pesos recurrentes son chicos, la actividad se apaga y el agente olvida enseguida. Si son grandes, explota. Con radio espectral exactamente 1 el eco **ni se apaga ni crece**: dura. Es la zona donde una red retiene información sin descontrolarse.

Y la asimetría es real, no un comentario: **medido, el hemisferio caos tiene ρ = 1,0000000000 y el de orden ρ = 0,3966.**

### El «cuerpo calloso»

Una compuerta decide cuánto del hemisferio caos pasa a la decisión, y después normaliza los dos juntos. Es el traductor entre «lo que siento» y «lo que hago».

### Los tres agregados

1. **Veto α.** Una cabecita estima cuánta energía le queda al agente. Si cree que se está muriendo, **baja la exploración**: deja de probar cosas raras y se vuelve conservador. La idea es buena: un bicho con hambre no experimenta.
2. **Amígdala.** Otra cabecita predice peligro. No se usa para decidir: se usa como **tarea extra**, para forzar al cerebro a representar cosas relevantes para sobrevivir.
3. **Resilience Zen.** Un tope de seguridad: si el estado interno crece demasiado, lo achica.

### Contra qué se compara y en qué

Contra **DualBrain** (dos vías, reactiva + memoria líquida con compuerta) y contra un **MLP** pelado. En dos tareas:

- **PureMemory:** aparece una señal 5 pasos, desaparece, y hay que seguir respondiendo según ella durante 95 pasos más. Pura memoria.
- **SurvivalWorld:** buscar comida, esquivar peligros, con la energía bajando y el ambiente cambiando entre abundancia y escasez.

**La hipótesis:** que los tres agregados hagan que Principia le gane a DualBrain en las dos.

---

## 4. QUÉ HICE, EN ORDEN

### Paso 1 · Medí el entorno antes de decidir

`torch 2.13.0+cpu` está en tu container. **Así que no usé Kaggle y no gasté tu cuota.**

### Paso 2 · Saqué la celda 1 a un archivo y la compilé

34.903 bytes, 923 líneas. **Primera vez que ese código corre**: en el notebook tiene 0 bytes de salida.

### Paso 3 · Escribí 11 tests que pueden dar rojo

Y uno que existe solo para validar a los demás: verifico que una matriz ortogonal **sí** tiene radio espectral 1 y que una al azar **no**. Sin eso, el test principal no distinguiría nada.

**Dos dieron rojo:**

- **El tope de seguridad nunca se puede activar.** El estado no puede superar `√8 = 2,8284` por cómo está escrita la fórmula, y el tope estaba en 3,0. Es código muerto, y no por mala suerte: por matemática.
- **Principia tiene 8,3% más parámetros que DualBrain** en PureMemory, y el benchmark atribuye la diferencia a la arquitectura.

### Paso 4 · Lo que encontré sin buscarlo, y es lo peor

En PureMemory, **las dos etiquetas que alimentan al veto y a la amígdala no tienen información**:

- La recompensa vive en [−0,4998, 0,4983], y el código marca peligro cuando baja de −1,0. **Nunca pasa: 0 de 2.000 pasos.**
- La energía es **constante 1,0**, porque en esa tarea no hay energía.

O sea que las dos cabecitas están aprendiendo a predecir un número fijo. Eso no sería grave si quedara ahí. **Pero el veto usa esa salida para decidir cuánto explorar.** Y medido sobre 240 episodios:

> **Principia explora al 29-35% de lo normal, todo el tiempo, por una señal que no dice nada.** DualBrain y el MLP exploran al 100%.

Así que si el benchmark hubiera corrido, en PureMemory no habría medido bicameralidad: habría medido **un bono de parámetros a favor y una penalización de exploración en contra**, las dos ajenas a la hipótesis.

### Paso 5 · Los dos arreglos que me pediste

**El tope:** el arreglo no es cambiar el 3,0 por otro número, porque el próximo que toque el tamaño lo rompe otra vez en silencio. Le puse una **validación que se niega a construir el objeto** si el tope es inalcanzable. Y calibré el valor nuevo con la distribución real de 1,38 millones de muestras: queda inerte en operación normal y dispara 122.097 veces bajo estrés.

**Mi primer intento falló y mi propia suite lo cazó.** Puse el tope en 1,6971: alcanzable en teoría, cero activaciones en la práctica. Alcanzable y alcanzado no son lo mismo.

**El guard:** si una etiqueta es constante en el lote, ese término se marca **NO TESTEABLE** y sale del entrenamiento. Discrimina por lote: en PureMemory descarta los dos términos siempre (56 de 56); en SurvivalWorld usa energía siempre y peligro en 23 de 36.

### Paso 6 · Los tres brazos, que son MÍOS y sirven para una cosa sola

Para saber si mi propio parche alcanza. Y **no alcanzaba**:

| Brazo | Cuánto explora |
|---|---|
| A original | 29% → 35% |
| B con el guard | 28% → **29%** |
| C con el guard y el veto apagado | **100%** |

**El B es peor que el A.** Porque la etiqueta constante, aunque no enseñaba nada, **iba arrastrando el estimador hacia arriba y aflojando de a poco el castigo que ella misma causaba**. Al sacarla, el castigo queda congelado para siempre.

**La lección, que sirve para todo:** un guard de tautología tiene que **apagar también al que consume la señal**, no solo sacar el término de la cuenta. Marcar el síntoma y dejar actuar la causa es peor que no tener guard.

---

## 5. Y qué tiene que ver todo esto con TU proyecto

**Casi nada, y hay que decirlo así.**

Lo único que liga BICAMERALITY con tu trabajo es **un string**: el nombre `DualBrain` aparece en ese código, descrito como «campeón v5.6». Pero eso está en una celda con **0 bytes de salida** y procedencia **no establecida** (resp 013). **Un nombre coincidente no es evidencia de linaje**, y ya me equivoqué una vez atribuyéndotelo.

Lo que sí vale, y es tuyo:

1. **El paréntesis dio un caso de estudio útil.** Tres archivos distintos del corpus tienen el **mismo** tipo de error: un guard que no puede dispararse. El `max_h > 1e6` después del `clip` en el Script R, el `'in_physiological_range': True` hardcodeado, y este tope. **Ese patrón es el hallazgo transferible**, y no depende de quién escribió BICAMERALITY.
2. **La lección del guard es directamente aplicable** a `src/motor.py`, que ya marca `NO_TESTEABLE` cuando `sd(null) == 0`. Ahí la propagación sí está hecha, pero conviene revisar que ningún otro consumidor lea ese campo como si fuera un número.

---

## 6. NO MEDIDO

- **No corrí el benchmark completo** (500 episodios × 3 semillas × 2 tareas). Los tres brazos dan acierto 0,52-0,53, o sea **azar**. Los arreglos quitan un confound; **que mejoren la tarea no está medido**.
- **No verifiqué si `DualBrain` en ese código es el tuyo** o una coincidencia de nombre. No se puede desde el archivo.
- Esta respuesta **no mide nada nuevo**: aclara nomenclatura y cita mediciones ya commiteadas en `audit/bicamerality/`.
