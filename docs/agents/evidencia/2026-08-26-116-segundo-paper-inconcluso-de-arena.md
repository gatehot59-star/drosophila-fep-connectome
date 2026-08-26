# PERITAJE · segundo paper inconcluso de Arena (`Arena ... Models10.html`)

**Pedido de Abraham:** "revisá qué hay de nuevo, qué se repite, entendé que del primer paper hubo dos más, que no se terminaron, con hallazgos distintos".

---

## 0. Qué hago con estos archivos, para que no parezca que se evaporan

**No los guardo en una carpeta secreta ni en mi cabeza.** Cada archivo que Abraham comparte:

1. **se lee**;
2. **se cruza con git** para ver si ya hay registro;
3. si aporta algo, **se deja commiteado** como evidencia o peritaje, con fecha y veredicto;
4. y si no aporta nada nuevo, **también se deja dicho** para no volver a abrirlo como si fuera novedad.

O sea: **no se pierden, se convierten en expediente**.

Este archivo queda registrado acá. Si mañana el chat se corta, este recibo sobrevive y el
HTML no hay que volver a mandarlo.

---

## 1. Lo que sí es NUEVO en este segundo paper inconcluso

Este HTML no es el paper publicado ni el draft de marzo que traje antes. Es otra rama:
**del hallazgo biológico salta a una arquitectura ingenieril explícita.**

Las dos novedades reales son:

### 1.1 La tesis de "ingeniería inversa de cerebros no escaneados"

El prompt humano abre con esto, textual:

> *"Los hemisferios son distintos... ¿eres capaz de aplicar ingeniería inversa a los cerebros que todavía no fueron escaneados? Yo podría, tengo la base, el paper, demuéstrame que eres digno"*

**Eso no estaba en el paper 1.** El paper 1 mide propiedades del conectoma ya escaneado.
Acá aparece una **línea de producto distinta**: usar las propiedades medidas (aislamiento,
acceso motor, reverberación) como priors para reconstruir o sintetizar circuitos de
cerebros todavía no observados.

En criollo: pasar de **"qué hace este cerebro"** a **"cómo diseño uno que haga esto"**.

### 1.2 La formalización ingenieril completa: neurona + builder

No es una idea suelta: baja a dos archivos con nombres y API:

- `complex_ltc_core.py` — la neurona LTC compleja
- `connectome_builder.py` — el constructor de topologías y controles

Eso tampoco estaba en el PDF publicado. El paper habla de SparseLTC y nulls; este HTML
los reescribe como **framework de ingeniería reusable**, con constructor sintético,
nulls, builder y activaciones complejas como piezas intercambiables.

**Eso sí es un hallazgo de diseño de sistema**, aunque no necesariamente científico.

---

## 2. Lo que REPITE de material que ya está en expediente

Muchísimo. Y esto importa porque no todo paper inconcluso suma conocimiento nuevo:

### 2.1 Repite el motor complejo

El núcleo de `ComplexLTCNetwork` es exactamente la misma ecuación que ya venimos usando:

```
z_{t+1} = (1 - τ_c) * z_t + τ_c * f(W_c^T z_t + s_t)
```

Con:
- `τ = 0.119`
- pesos complejos E/I como fase 0 / π
- normalización por radio espectral al 0.99
- activación `complex_tanh`

**Eso no es nuevo.** Es el mismo sujeto que ya traimos, explicamos, corrimos, peritamos,
corregimos y llevamos a `motor_v2.py`.

### 2.2 Repite el builder de nulls

`maslov_sneppen_null()` y `community_preserving_null()` también son lo mismo en espíritu:
- preservar grado
- destruir modularidad o preservar bloques
- comparar contra controles estadísticos

**Tampoco es nuevo como línea.** Lo nuevo acá es que lo empaqueta explícitamente como
infraestructura de diseño, no como scripts del paper.

---

## 3. Y el problema gordo: hereda DOS números que el erratum ya retiró

En `synthetic_connectome()` el texto dice:

> *"Genera un conectoma sintético con las propiedades estadísticas del FlyWire v783"*
>
> `reciprocity_factor: float = 36.0`
>
> `density global ~0.0074`

**Esos son exactamente los dos números que el erratum ya corrige.**

- `0.0074` de densidad: **9,42× grande** por overflow de int32
- `36×` de reciprocidad: también heredado de esa densidad errónea; el valor correcto es
  **338,8×**

O sea: **el builder sintético está calibrado contra una estadística ya refutada**.

Y eso no es menor: si querés pasar de hallazgo biológico a ingeniería inversa, el builder
es el puente. Si el puente sale de una densidad 9,42× inflada, todo lo que generes del
otro lado nace sesgado.

---

## 4. Qué cambia conceptualmente este segundo paper

El paper publicado 1 decía, en esencia:
- el conectoma aísla modalidades
- concentra acceso motor
- reverbera en un régimen cuasi-lineal

Este segundo paper inconcluso intenta decir:
- **esas tres propiedades son suficientes para diseñar un motor bioinspirado nuevo**
- y encima **para inferir cerebros no escaneados** a partir de sus constraints funcionales

Ese salto es serio. No es cosmética. Es una propuesta distinta.

### Mi veredicto en una frase

**El paper 2 no trae un hallazgo empírico nuevo sólido; trae una ambición de ingeniería nueva sobre una base estadística que hoy sabemos que está parcialmente mal calibrada.**

O sea: **la dirección es nueva, el piso todavía no está limpio.**

---

## 5. ¿Está registrado esto en git?

Busqué en el repo por dos firmas fuertes de este HTML:
- `Complex-valued LTC Neural Network`
- `maslov_sneppen_null` / `synthetic_connectome`

**Cero resultados.**

Así que no, **este segundo paper inconcluso no estaba registrado** en nuestro expediente. Ahora sí: queda en este archivo commiteado.

---

## 6. Qué haría con esto, sin perder tiempo

1. **No tomaría el builder sintético como verdad** hasta reemplazar `density ~0.0074` y
   `reciprocity_factor=36.0` por los valores corregidos.
2. **Sí rescataría la tesis de producto**: "ingeniería inversa de cerebros no escaneados".
   Esa línea no estaba en el paper 1 y sí puede conectar con ARC y con producto.
3. **Lo separaría del connectoma paper**. No es un suplemento del paper 1: es otra cosa.
   Es un dossier de arquitectura o una línea de I+D, no un erratum.

---

## 7. NO MEDIDO

- El HTML viene truncado: `connectome_builder.py` queda cortado en medio de `community_preserving_null`.
- **No verifiqué** si había un archivo 3 en ese hilo de Arena ni qué más proponía.
- No medí si la idea de "ingeniería inversa de cerebros no escaneados" tiene ya arte previo
  explícito en neuroingeniería o connectomics generativa.
- No convertí este borrador en código ejecutable ni lo crucé contra `motor_v2.py` línea por línea.
- No se puede decir todavía si esto es paper 2 o paper 3: solo que es **otra rama distinta** del paper 1.
