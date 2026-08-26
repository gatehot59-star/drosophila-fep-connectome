# 091 · `motor.py` explicado, y el emulador QEMU del ESP32 puesto en su lugar

**Fecha:** 2026-08-25 16:35 (America/Buenos_Aires) · **Modo:** TITAN FULL · **Tipo:** explicación técnica + estado de emulador

**Archivos fuente leídos para esta entrega:** `src/motor.py` en `titan/twohop-nulls`, más los docs 087, 089 y 090 ya producidos hoy.

<hr/>

## 1. Lo primero: `src/motor.py` NO es el motor del ESP32

Ese fue el cruce que te molestó, y con razón.

<table><tbody><tr><th width="220" cell-bg-color="grey"><p><strong>archivo</strong></p></th><th width="220" cell-bg-color="grey"><p><strong>qué es</strong></p></th><th width="220" cell-bg-color="grey"><p><strong>escala</strong></p></th><th width="220" cell-bg-color="grey"><p><strong>sirve para</strong></p></th></tr><tr><td width="220"><p><code>src/motor.py</code></p></td><td width="220"><p><strong>instrumento científico de referencia</strong><span> sobre el conectoma</span></p></td><td width="220"><p><strong>138.639 neuronas, 15.091.983 aristas</strong></p></td><td width="220"><p><span>preguntar si la estructura del conectoma produce una dinámica que los nulls no producen</span></p></td></tr><tr><td width="220"><p><code>firmware/dualbrain/*</code></p></td><td width="220"><p><strong>módulo embebido mínimo</strong><span> para microcontrolador</span></p></td><td width="220"><p><strong>3.553 parámetros, 800 B RAM</strong></p></td><td width="220"><p><span>control en chip, no auditoría del conectoma</span></p></td></tr></tbody></table>

<p><br/></p>

**En criollo:** `motor.py` es el banco de pruebas grande, el laboratorio. El DualBrain de C es la versión chiquita para producto. **No compiten. No hacen el mismo trabajo. Y hoy el puente entre los dos no existe.**

<hr/>

## 2. Qué hace `motor.py`, sin humo

`motor.py` agarra el conectoma real de Drosophila, le arma una dinámica recurrente compleja, la estimula por modalidad sensorial y pregunta si lo que aparece en el grafo real sobrevive frente a nulls que preservan propiedades estructurales.

<p><br/></p>

La ecuación central es esta:

```python
z_{t+1} = (1 - tau) * z_t + tau * f(W^T z_t + s_t)
```

<p><br/></p>

Y cada término importa:

- `z`: el estado de todas las neuronas. **Es complejo**, no real. La amplitud dice cuánto, la fase dice cuándo.
- `tau`: la constante de integración por neurona. **También es compleja**. Su parte real integra; la imaginaria mete frecuencia intrínseca.
- `W`: la matriz de conectividad. El módulo del peso es la fuerza. La fase codifica el signo excitatorio/inhibitorio.
- `s_t`: el estímulo externo, prendido en una ventana temporal.

**Traducido:** no es solo "la señal pasa o no pasa". Es "la señal pasa, con qué intensidad, con qué desfase, y si esa geometría dinámica depende del conectoma real o la explica un control".

<hr/>

## 3. Las 10 piezas de `motor.py`, una por una

### 3.1 Guard de estabilidad

`tau_stability_limit()` y `validate_tau()` están para frenar corridas que divergen por construcción.

La regla es: si `|1 - tau| > 1`, el estado puede crecer sin cota. Así que el archivo **no corre cualquier `tau`**: calcula el límite exacto y aborta si el rango imaginario lo toca.

**Esto importa porque evita un falso hallazgo numérico.** Si la dinámica explota, después cualquier métrica parece "interesante" y es basura.

### 3.2 Activación compleja acotada

`bounded_complex_tanh()` no usa una `tanh` cruda y listo. La cruda tiene polos y cerca de ellos explota. La versión acotada:

- deja la fase,
- recorta la magnitud,
- reemplaza NaN o infinito por una versión segura.

**La idea buena acá:** en un motor donde la fase es parte de la señal, un `clamp` común rompe justo lo que querés medir.

### 3.3 Pesos complejos desde el conectoma

`build_complex_weights()` hace la traducción desde el parquet real a una matriz compleja dispersa.

No inventa signo por arista al azar. Usa una regla por neurona presináptica, apoyada en la ley de Dale: si la neurona tiene salidas inhibitorias, su fase base va cerca de `pi`; si es excitatoria, cerca de `0`. Después agrega un jitter chico.

**Esto está bueno por una razón:** el signo no queda como etiqueta binaria suelta, queda metido en la geometría de fase del peso.

### 3.4 Normalización espectral

`normalize_spectral()` escala la matriz para dejar su radio espectral en `0.99`.

O sea: te deja el sistema cerca del borde de estabilidad, pero de este lado. Y además devuelve tres cosas: matriz escalada, `rho` y si convergió o no.

**Eso evita otro autoengaño clásico:** no confunde "dio un número" con "convergió de verdad".

### 3.5 Dos nulls, no uno

Acá está la parte científica de verdad.

- `null_maslov_sneppen()`: preserva grado entrante y saliente exactos, sin autolazos ni duplicados.
- `null_community_preserving()`: preserva grado y además la conectividad entre bloques.

**La pregunta que separan es distinta:**

- Maslov-Sneppen pregunta si el efecto es más que la secuencia de grados.
- Community-preserving pregunta si el efecto es más que la arquitectura modular.

Eso está bien plantado. No usa "azar" como una sola bolsa. Usa el null correcto según qué propiedad querés aislar.

### 3.6 `make_tau()`: una `tau` por neurona

Acá está el salto respecto del SparseLTC simple.

`motor.py` no tiene una única constante de tiempo global. Construye **138.639 taus**, una por neurona, con `Re=0.119` e `Im` uniforme en un rango estable.

**En criollo:** deja de ser un filtro único y pasa a ser una población de osciladores con ritmos propios.

### 3.7 `propagate()`: la corrida

`propagate()` ejecuta la dinámica paso a paso, activa el estímulo entre `t_on` y `t_off`, y puede guardar snapshots intermedios.

El detalle bueno: guarda el estado posterior al update. No mezcla índices temporales en silencio.

### 3.8 Métricas

`region_profile()`, `cosine_distance()`, `rdi()` y `phase_coherence()` resumen la salida por regiones y miden cuán separables quedan los perfiles.

Y acá hay una decisión importante: **si un vector colapsa a cero, la distancia angular no se define y devuelve NaN. No la disfraza de 1.0.**

Eso evita premiar controles muertos como si fueran "máximamente distintos".

### 3.9 Test global

`global_rank_test()` combina varios estadísticos a la vez y además tiene un guard de tautología: si un null conserva exactamente una cantidad y esa cantidad queda con desviación estándar cero, la marca `NO_TESTEABLE`.

**Esta parte me gusta porque es adulta.** No exprime un ratio bonito de algo que el control conserva por definición.

### 3.10 Datos reales con checksum

`load_connectome()` baja parquet y anotaciones, verifica md5, arma índices, modalidades sensoriales y bins anatómicos.

**No toma los insumos como palabra sagrada.** Si el checksum cambió, te lo dice. Eso importa porque la tabla de anotaciones cambió entre ramas vivas y si eso deriva, los priors dejan de ser comparables.

<hr/>

## 4. Entonces, qué es `motor.py` conceptualmente

No es un producto. No es firmware. No es un hallazgo por sí mismo.

**Es un instrumento de falsación** con tres capas al mismo tiempo:

1. **una dinámica compleja sobre el conectoma**,
2. **controles estructurales explícitos**,
3. **tests internos que pueden dar rojo antes del experimento**.

Si tengo que clavarlo en una frase: **`motor.py` es el banco donde intentás demostrar que la forma del conectoma produce una dinámica que no sale gratis de preservar grado o módulos.**

<hr/>

## 5. Qué NO hace `motor.py`

Esto también hay que decirlo, porque si no se lo infla de más.

- **No entrena nada.** No es el DualBrain entrenable.
- **No corre en un microcontrolador.** Sería absurdo: 138k neuronas y 15M aristas.
- **No es la prueba de producto.** Es peritaje científico.
- **No conecta todavía con el firmware de ESP32.** Hoy son dos líneas separadas.

O sea: si alguien vende `motor.py` como "el cerebro que ya está en el chip", está vendiendo fruta.

<hr/>

## 6. Y el emulador: qué sí hice y qué no

Acá tenías razón: esto merecía documento propio, porque no fue una nota al pie.

### Lo que sí quedó medido

En el entorno de trabajo instalé **QEMU de Espressif** resolviendo a mano sus dependencias compartidas que faltaban. No fue `apt install` prolijo, fue cirugía: bajar paquetes Debian, extraer librerías, volver a probar, repetir.

Y eso **sí llegó a un punto verificable**:

- `qemu-system-xtensa` arrancó,
- el binario quedó ejecutable,
- el emulador **lista máquinas `esp32` y `esp32s3`**.

Eso ya es bastante más que "intenté instalar un emulador". **El runtime existe y quedó vivo en el entorno.**

### Lo que NO quedó cerrado

No llegué a correr el firmware dentro de QEMU.

O sea, faltó el tramo importante:

- tomar el ELF linkeado,
- arrancarlo con `-M esp32` o `-M esp32s3`,
- ver UART o alguna forma de vida,
- medir si ejecuta la rutina real.

**Estado correcto:**

- `QEMU disponible`: **SÍ, medido**.
- `QEMU booteando el firmware`: **NO MEDIDO**.
- `firmware del ESP32 validado dentro de emulador`: **NO MEDIDO**.

Y esa distinción importa, porque decir "hay emulador" no es lo mismo que decir "el firmware ya corre emulado".

<hr/>

## 7. Qué deja armado el emulador, aunque no haya cerrado

Aunque no booteé el firmware, el valor del trabajo no fue cero.

Dejó tres cosas:

1. **Probó que el entorno sí puede alojar un runtime de ESP32.** Antes eso era especulación.
2. **Bajó la siguiente corrida de "imposible" a "pendiente".** Que no es lo mismo.
3. **Abrió la vía de validar sin hardware parte del camino embebido.** No reemplaza al chip real, pero sí puede cubrir boot, símbolos, mapa de memoria y UART.

Mi take: **para esta línea, QEMU sirve como escalón intermedio, no como veredicto final.** El veredicto de producto sigue siendo hardware real.

<hr/>

## 8. Dónde está hoy cada cosa

<table><tbody><tr><th width="220" cell-bg-color="grey"><p><strong>pieza</strong></p></th><th width="220" cell-bg-color="grey"><p><strong>estado</strong></p></th></tr><tr><td width="220"><p><code>src/motor.py</code></p></td><td width="220"><p><strong>leído y explicado</strong><span>: instrumento científico sobre conectoma</span></p></td></tr><tr><td width="220"><p>firmware DualBrain</p></td><td width="220"><p><strong>compilado, linkeado y auditado</strong><span>, pero sin corrida en chip real</span></p></td></tr><tr><td width="220"><p>QEMU ESP32</p></td><td width="220"><p><strong>instalado y arrancando</strong><span>, pero sin boot útil del firmware todavía</span></p></td></tr><tr><td width="220"><p>puente conectoma -> chip</p></td><td width="220"><p><strong>no existe aún</strong></p></td></tr></tbody></table>

<hr/>

## 9. Lo que sigue, sin chamuyo

Si el objetivo es cerrar esta línea bien, el orden correcto es:

1. **no volver a mezclar `motor.py` con el DualBrain embebido**,
2. **usar QEMU para intentar bootear el ELF real**,
3. **después** pasar a hardware,
4. y en paralelo decidir si el puente conectoma -> chip se va a construir o si siguen siendo dos artefactos distintos.

**Mi opinión:** el paso más rentable ahora es el 2. Ya pagaste casi todo el costo feo del emulador. Dejarlo en "instala y lista máquinas" sería medio boludo.

<hr/>

## 10. NO MEDIDO, declarado

- No releí `firmware/dualbrain/*` en esta entrega: esa parte sale de lo ya medido hoy, no de lectura nueva.
- No corrí `motor.py` ahora: lo expliqué desde el archivo, no desde una corrida fresca.
- No ejecuté el ELF dentro de QEMU en esta entrega.
- No medí UART, ciclos ni tiempo de paso en emulador.
- No existe todavía evidencia de que el firmware embebido reproduzca algo del conectoma: **esa conexión sigue ausente**.

```plain
--- METODO TITAN ---
Accion delicada: NO
Modo aplicado:   TITAN FULL
Rubrica:         N/A para chat; artefacto de explicación y estado
N/A declarados:  testing/deploy/security no aplican a esta nota
Review externo:  no pedido
Instrumento:     lectura real de src/motor.py y estado ya medido del trabajo QEMU/ESP32
```