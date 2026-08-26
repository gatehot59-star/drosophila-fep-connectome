# Evidencia cruda · qué del DBC3 sirve para DualBrain y para el puente conectoma→chip

**Fecha:** 2026-08-25 22:35 (America/Buenos_Aires) · **Modo:** TITAN FULL

**Instrumento:** `build.run` sobre `brain-env`, torch CPU. `tools/dbc3_puente.py` y `src/dbc3_v4.py`, los dos bajados **desde este repo** y corridos sobre `dbc3_lib.py`, que es `dbc3_benchmark.py` cortado antes de `tasks_cfg` sin tocar lógica (E-01: sujeto exacto).

<hr/>

## 1. P-1 · El `tau` del DBC3 SÍ varía: hay algo que transferir

Era lo primero que había que falsar. Si `tau` fuera casi constante, sus 820 parámetros (11,9% del modelo) serían adorno y no habría nada que mover a otro motor.

```plain
  entrada grande |x|~3.0   tau: min=0.0000 med=0.1526 max=0.9998  sd_canales=0.2170  sd_tiempo=0.2406

  sigmoid(b_tau=-2.0) = 0.119203  <- el punto de partida; motor.py usa 0.119 fijo
```

**Rango completo de 0,0000 a 0,9998**, con desvío de 0,2170 entre canales y 0,2406 en el tiempo. El `tau_learner` **no es decoración**: usa todo el rango disponible.

### 🔥 Y el cordón umbilical quedado medido

`sigmoid(-2.0) = 0.119203`. Ese es **exactamente** el `0.119` que `motor.py` tiene hardcodeado como `tau_real`.

> **Los dos motores del proyecto arrancan del MISMO punto de operación.** No es coincidencia numérica: es la prueba de que uno sale del otro. Ya estaba registrado para el SparseLTC de marzo, y ahora se confirma que el DBC3 hereda el mismo sesgo.

<hr/>

## 2. P-2 · Los tres motores son LA MISMA ecuación. Lo único distinto es `tau`

```plain
  motor.py     z  <- (1-tau)*z  + tau*f(W^T z + s)          tau COMPLEJA, FIJA
  DBC3         hm <- (1-tau)*hm + tau*f(W_in e + W_res hm)  tau REAL, DINAMICA
  DualBrain    idem DBC3, con tau_learner de 528 params

  motor                              tamano        tau       depende de           acotado?
  motor.py (conectoma)   15.091.983 aristas   compleja      NADA (fija)       si, clip 2.0
  DBC3-v3                             6.888       real   entrada+estado  no (LN emergente)
  DBC3-v4                             6.936       real   entrada+estado       si, tanh 3.0
  DualBrain (ESP32)                   3.553       real   entrada+estado          por medir
```

### El hueco que esto expone, y es el más interesante del turno

<table><tbody><tr><th width="220" cell-bg-color="grey"><br></th><th width="220" cell-bg-color="grey"><p><strong>tau ESTÁTICA</strong></p></th><th width="220" cell-bg-color="grey"><p><strong>tau DINÁMICA</strong></p></th></tr><tr><td width="220"><p><strong>tau REAL</strong></p></td><td width="220"><p>SparseLTC de marzo</p></td><td width="220"><p>DBC3 y DualBrain</p></td></tr><tr><td width="220"><p><strong>tau COMPLEJA</strong></p></td><td width="220"><p><code>motor.py</code></p></td><td width="220"><p><strong>VACÍO · nadie lo probó</strong></p></td></tr></tbody></table>

> **La celda vacía de esa tabla es el cruce de los dos motores del proyecto.** `motor.py` tiene la aritmética compleja (amplitud + fase) pero su `tau` es fija por neurona. El DBC3 tiene `tau` que se decide en cada paso, pero real. **Nadie combinó las dos cosas**, y es la extensión natural que sale de mirar los tres motores juntos.

<hr/>

## 3. 🔴 P-3 · REFUTA la dirección que yo asumía

Yo daba por hecho que el fix M-2 del DBC3-v4 (normalizar el candidato y no el estado) se podía llevar a `motor.py`. **Leí el sujeto exacto y es al revés:**

```plain
  motor.py hace:  z = (1-tau)*z + tau*bounded_complex_tanh(drive)
  o sea: acota la ACTIVACION (el candidato), NO el estado ya mezclado.
  VEREDICTO: motor.py YA hace lo correcto. El defecto es exclusivo del DBC3,
  y la transferencia va del motor del conectoma al del chip, no al reves.
```

**`motor.py` ya hace lo correcto.** El defecto de normalizar después de integrar es **exclusivo del DBC3**, y la transferencia en este punto va **del conectoma al chip**, no al revés. Es la segunda vez en el día que la dirección que asumía estaba invertida.

<hr/>

## 4. P-4 · Lo que el DBC3 le puede dar al DualBrain, con su precio

```plain
  El DualBrain embebido tiene el MISMO gate asimetrico que el DBC3-v3:
  modula la memoria y no el reflejo. El fix M-1 le costaria:
    gate de reflejo: 1568 params sobre 3.553 = +44.1%
    bias en el nucleo: 32 params = +0.9%
    RAM extra: 128 B sobre 800 B = +16.0%
```

**+44,1% de parámetros y +16,0% de RAM.** Es caro en proporción, y en un módulo de 800 B ese pago no es gratis.

> **Declarado como ESTIMACIÓN, no medición:** `m=16` y `r=32` son las dimensiones **supuestas** del DualBrain embebido a partir de su blob de 3553 floats. **No se leyeron de su header en esta corrida.**

<hr/>

## 5. 🟢 El primer dato del A/B pareado, y respalda el M-1

```plain
tarea            piso  clas | v3 (media+-sd)         v4 (media+-sd)         LSTM (media+-sd)
----------------------------------------------------------------------------------------------
XORMemory       50.4%     2 |  50.8% +- 0.5           66.8% +-23.1           50.0% +- 0.1
```

**Con el piso medido en 50,4%:**

- **LSTM: 50,0%** → está **en el piso**, no aprendió nada
- **DBC3-v3: 50,8%** → está **en el piso**, tampoco aprendió
- **DBC3-v4: 66,8%** → **+16,4 puntos sobre el piso**

> **El gate simétrico convierte una tarea que la v3 no resolvía en una que sí.** Y además la v4 tiene **35% menos ancho de memoria** (h_m 13 contra 20), porque pagó el gate nuevo bajando el estado.

### 🔴 Y la advertencia que va junto al número

**La sd de la v4 es 23,1 sobre 3 semillas.** Eso significa que alguna semilla resolvió la tarea y otra no. **Es un efecto grande con dispersión grande: muestra chica, no resultado cerrado.** Con n=3 no hay intervalo y no se declara significancia.

<hr/>

## 6. NO MEDIDO, declarado

1. **El A/B no cerró:** falta DelayedClass y falta el veredicto pareado con su `t`.
2. **Los costos de P-4 son estimaciones** sobre dimensiones supuestas del DualBrain. Hay que leer su header.
3. **La celda vacía (tau compleja Y dinámica) NO se implementó ni se corrió.** Es una extensión identificada, no un resultado.
4. **P-1 se midió con pesos SIN ENTRENAR.** Que `tau` use todo el rango al inicializar no prueba que lo siga usando después de entrenar.
5. **No se midió el `tau` del DualBrain real**, solo el del DBC3.
6. **El puente conectoma→chip sigue sin construirse.** Esto identifica **por dónde** iría (el eje de `tau`), no lo construye.
