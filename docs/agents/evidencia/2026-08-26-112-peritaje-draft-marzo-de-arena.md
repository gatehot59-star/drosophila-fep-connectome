# EVIDENCIA CRUDA · 2026-08-26 · peritaje del draft de marzo (HTML de Arena)

**Qué trajo Abraham:** un export HTML de una conversación de Arena con un borrador de paper
fechado **10 de marzo de 2026**, título *«Aislamiento Topológico de Señales en el Conectoma
de Drosophila melanogaster»*.

**Instrumento:** lectura del HTML + `gateway build.run` sobre `brain-env` para verificar
cada número contra el parquet real + lectura de `docs/METHODS.md` en git.

---

## 1. EL DATO CRUDO DEL DRAFT ES EXACTO. Verificado, no creído.

Medido hoy directamente sobre `connectivity.parquet`
(md5 `3d802fd542b5d18570ba1ba0bb0abed9`):

```
columnas: ['Presynaptic_ID', 'Postsynaptic_ID', 'Presynaptic_Index',
           'Postsynaptic_Index', 'Connectivity', 'Excitatory', 'Excitatory x Connectivity']
filas: 15091983

   Connectivity                min 1      max 2405   media 3.6107  negativos 0        positivos 15091983
   Excitatory                  min -1     max 1      media 0.2005  negativos 6032681  positivos 9059302
   Excitatory x Connectivity   min -2405  max 1897    media 0.6955  negativos 6032681  positivos 9059302
```

| lo que dice el draft | lo medido hoy | |
|---|---|---|
| `Connectivity` min 1, max 2.405, μ=3.61 | min 1, max 2405, μ=**3.6107** | **exacto** |
| `Excitatory` min −1, max +1, μ=0.20 | min −1, max +1, μ=**0.2005** | **exacto** |
| producto rango [−2.405, +1.897], μ=0.70 | [−2405, +1897], μ=**0.6955** | **exacto** |
| 9.059.302 excitatorias / 6.032.681 inhibitorias | **9059302 / 6032681** | **exacto al dígito** |
| 40,0 % inhibitorias | **39,97 %** | exacto |
| N=138.639, E=15.091.983 | idéntico | exacto |
| τ = σ(−2,0) ≈ 0,119 | el motor usa 0,119 | idéntico |

**El autor del draft verificó el dato de la misma forma y le dio lo mismo.** Eso no es un
detalle: es la parte del draft que **no** hay que volver a discutir.

---

## 2. 🔍 La contradicción aparente con lo medido hoy, RESUELTA

Hoy `motor_v2` reportó `frac_inhibitoria = 0.2981` (29,8 %) y el draft dice **40,0 %**.
Parecía un choque. Medido:

```
ARISTAS: inhibitorias 6032681 de 15091983 = 39.97%
NEURONAS con salida: 138005  mixtas: 0  I puras: 41333  E puras: 96672
  frac de neuronas inhibitorias: 0.2995
  aristas por neurona I: 146.0    por neurona E: 93.7    cociente 1.557
PESO: suma |w| inhibitorio 21998205  excitatorio 32494717  ratio E/I 1.477
```

**No es una contradicción: son dos denominadores distintos.**

- **39,97 % de las ARISTAS** son inhibitorias → el número del draft
- **29,95 % de las NEURONAS** son inhibitorias → el número del motor

Y la causa es un hecho medido que **no está en ninguno de los dos**: las neuronas
inhibitorias tienen **1,557× más aristas de salida** que las excitatorias (146,0 contra
93,7). La inhibición está **más distribuida de lo que sugiere el conteo de neuronas**, y
es exactamente el tipo de asimetría estructural que el draft persigue en su sección de
cancelación GABAérgica.

Nota sobre el ratio E/I 1,50 del draft: sale del **conteo** (9059302/6032681 = 1,502).
Por **peso** da **1,477**. Los dos son correctos y son distintos; hay que decir cuál.

---

## 3. LO QUE EL DRAFT TIENE Y NO ESTÁ EN GIT (lo genuinamente nuevo)

Busqué en el repo: `0.8218` → 0 resultados. `161.9` → 0 resultados.

### 3.1 La CURVA TEMPORAL de persistencia — y es la que me refuta hoy

> *«Bajo dinámica temporal SparseLTC de 200 pasos, el conectoma biológico mantiene un RDI
> Coseno > 0,97 durante 120 pasos después de la cesación del estímulo, mientras que la red
> aleatoria colapsa a 0,002 en el mismo intervalo.»*

**Esta mañana le dije a Abraham que «el cruce de tiempo es lo único vivo del conectoma y
el número no está medido».** El draft de marzo **ya lo tiene medido**, con otro null y otra
normalización. Mi recomendación de prioridad se apoyó en no saber que esto existía.

No lo invalida (son metodologías distintas, ver §4), pero **sí invalida que yo lo
presentara como territorio virgen**.

### 3.2 La NORMALIZACIÓN POR COLUMNA

> *«Para la propagación temporal, W se normaliza **por columna** y se escala al 99 % del
> radio espectral estimado.»*

**`motor_v2` NO normaliza por columna: solo escala espectralmente al 0,99.** Son dos
operadores distintos, y esta diferencia es la candidata más fuerte para explicar la
discrepancia de §4.

### 3.3 La CANCELACIÓN GABAÉRGICA por modalidad

| modalidad | cancelación inh/exc | lectura del draft |
|---|---|---|
| gustativa | **0,0004** (0,04 %) | autopista sensoriomotora, inhibición nula |
| visual | 0,121 (12,1 %) | intermedia |
| olfativa | **4,719** (472 %) | **bloqueo activo**, obliga a vía asociativa |

Y el test interhemisférico L→R: excitación +166.820 contra inhibición −228.314, flujo neto
**−61.494**, ratio de cancelación **1,37**. El draft lo lee como supresión **activa** y no
como simple ausencia de conexiones.

**Ninguna de estas tres cosas está en el expediente que trabajé hoy.**

---

## 4. 🚨 LA DISCREPANCIA QUE HAY QUE EXPLICAR, y es grande

| | draft de marzo | medido hoy (39 nulls CP, GPU) |
|---|---|---|
| RDI real | **0,8218** | 0,4311 (t50) · 0,7184 (t100) · 0,6642 (t149) |
| RDI del null | **0,0088 ± 0,0050** | 0,4411 (t50) · 0,4163 (t100) · 0,1340 (t149) |
| familia de null | **Maslov-Sneppen**, 20 | **CP**, 39 |
| veredicto | Z = **161,9σ** | test global **p = 0,25, NO significativo** |

**El null del draft COLAPSA a 0,009. El nuestro NO** (0,42 y 0,13). Y en t=50 nuestro real
queda **por debajo** de los 39 nulls, o sea con el signo invertido respecto del draft.

Cuatro causas candidatas, todas medibles y ninguna medida todavía:

1. **MS contra CP.** Nuestro CP admite **149.589 multi-aristas** (medido hoy); MS las
   prohíbe por construcción. `docs/METHODS.md` ya advierte que esa diferencia
   «debe declararse siempre que se comparen las dos familias».
2. **Normalización por columna** (draft) contra **solo espectral** (motor_v2).
3. **El RDI no es el mismo objeto:** el draft promedia por `super_class` de FlyWire; el
   motor usa 10 bins espaciales con 623 filas sin match.
4. **200 pasos contra 150**, y snapshots en otros tiempos.

---

## 5. Y AHORA LO INCÓMODO: git YA REFUTABA parte del draft

`docs/METHODS.md` (8.386 B, ya en el repo) dice, textual:

> *«Z-scores are reported for direction and are not interpretable as effect sizes: the
> null distributions here have very small variance, so a z of several hundred reflects a
> **tight null rather than an extraordinary effect**. Ratios and the count of nulls
> exceeding the real value are the reportable quantities.»*

**Los 161,9σ y 203,9σ del draft son exactamente lo que esa línea prohíbe reportar como
efecto.** El repo ya lo sabía.

Y hay más que el draft no tiene y git sí:

| | draft de marzo | `docs/METHODS.md` en git |
|---|---|---|
| nulls MS | **20** | **40**, semillas 4200+17i, verificados por null |
| grados preservados | «preservando exactamente» | **medido**: 0 desajustes en 40 de 40 |
| multi-aristas | no se menciona | MS **cero**; CP **149.000-150.400** por null |
| piso del p | no se menciona | **0,0244** con n=40, y «un p de 0,0244 significa cero nulls, no que p valga 0,0244» |
| Bonferroni a 12 tests | no se menciona | **no lo soportan 40 nulls**: harían falta n ≥ 239 |
| densidad | no aparece | el 0,0074 publicado es **9,42× grande** por overflow de int32 |

**El draft del HTML es una versión ANTERIOR a lo que el repo ya documenta.** 20 nulls
contra 40, y sin ninguna de las advertencias estadísticas.

---

## 6. Y ME REFUTA A MÍ, hoy

Dos incumplimientos propios, medidos contra el archivo que ya estaba en el repo:

**1. Corrí CP todo el día y `METHODS.md` ya decía que MS es la familia sin multi-aristas.**
Declaré cinco veces «`null_maslov_sneppen` no corrió sobre el grafo real» como NO MEDIDO,
sin abrir el archivo que explica que **MS es la familia principal del paper publicado** y
que CP es «la más estricta» pero admite multi-aristas. Es el patrón 3 del Bloque 8: un
límite afirmado sin abrir la fuente que lo contradice.

**2. Re-derivé desde cero cosas que ya estaban escritas.** Hoy reporté como hallazgo que
«12 métricas con Bonferroni necesitan más nulls» y que «el piso del p con 39 nulls es
1/40». Las dos están en `METHODS.md` con más precisión (n ≥ 239, piso 0,0244). Gasté
cómputo en re-descubrir el mapa que tenía.

---

## 7. NO MEDIDO

- **No corrí MS sobre el grafo real.** Sigue siendo la deuda, y ahora se sabe que es la
  familia que el paper publicado usó.
- **No probé la normalización por columna.** Es la candidata más fuerte para el colapso
  del null a 0,009 y no está implementada en `motor_v2`.
- **No verifiqué la curva temporal del draft**: 0,97 durante 120 pasos tras cesar el
  estímulo. Es una afirmación del HTML, no una medición de este expediente.
- **No verifiqué la cancelación GABAérgica** (0,04 % / 12,1 % / 472 %) ni el test
  interhemisférico. Los números del dato crudo del draft dieron exactos, lo que sube su
  credibilidad, pero **eso no es haberlos medido**.
- **No leí `docs/ERRATUM.md` (31.729 B)** en este turno. Puede contener ya alguna de las
  tres cosas que declaré como nuevas en §3.
- El HTML es un **export de chat**, no el PDF del paper: no puedo confirmar que sea el
  texto final ni si algo se truncó en el volcado (el archivo llega cortado en §3.3).
