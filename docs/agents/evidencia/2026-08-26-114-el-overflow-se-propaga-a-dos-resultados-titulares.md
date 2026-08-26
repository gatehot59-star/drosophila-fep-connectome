# EVIDENCIA CRUDA · 2026-08-26 · el PDF del paper, y el overflow que no se queda en la densidad

**Sujeto:** `Paper1_SignalPropagation.pdf`, 7 páginas, el preprint completo. Antes había
leído **solo el abstract vía DOI** y un draft truncado de marzo.

**Instrumento:** `gateway build.run` sobre `brain-env`, sobre `connectivity.parquet`
(md5 `3d802fd542b5d18570ba1ba0bb0abed9`).

---

## 1. LA RECIPROCIDAD DEL PAPER ES EXACTA. Verificada.

```
n=138639  E=15091983
aristas con reciproca presente: 4014518 de 15091983 = 26.6003%
```

**El paper dice 26,6 %. Medido: 26,6003 %.** Exacto a la cuarta cifra.

---

## 2. 🚨 PERO EL «36×» NO. Y ese es el hallazgo.

```
densidad correcta = 0.000785197     (el paper publica 0.0074)
cociente publicado/correcto = 9.42
reciprocidad / densidad = 338.8x
```

El paper reporta reciprocidad **«36× sobre la expectativa de densidad»**, tres veces: en el
abstract, en §1.3 (Contributions) y en §3.5. Con la densidad **publicada** (0,0074):
0,266/0,0074 = **35,9 ≈ 36×**. Con la densidad **correcta**: **338,8×**.

**El overflow de int32 que `ERRATUM.md` item 1 documenta para la densidad NO se queda en la
densidad: entra en el 36× y lo subestima por 9,41.**

Y esto **no debilita** el paper en ese punto: lo **fortalece**. La reciprocidad es el
«sustrato candidato para la reverberación» de la Propiedad 3, y es **9,4 veces más
excepcional** de lo publicado.

---

## 3. 🚨 Y LA TABLA 5 SE INVIERTE EN DOS FILAS

La fórmula que `METHODS.md` documenta es:

```
expected_edges = N_class x N_motor x density x P(excitatory | edge exists)
con P(excitatory) = 0.600272
```

Medido hoy: 9059302/15091983 = **0,600272**. Coincide exacto.

**Esa fórmula es LINEAL en la densidad.** Si la densidad está 9,4244× grande, cada
`expected` está 9,4244× grande y cada `Obs/Exp` está 9,4244× **chico**. La corrección es
aritmética exacta, **no** hace falta re-correr nada:

```
factor de correccion = 9.4244

clase                   N  Obs/Exp pub   Obs/Exp corr veredicto
mechanosensory       2659        1.300x        12.252x  enriquecida -> ENRIQUECIDA
unk. sensory          131        1.400x        13.194x  enriquecida -> ENRIQUECIDA
AN                    495        0.600x         5.655x  empobrecida -> ENRIQUECIDA  <<< SE INVIERTE
gustatory             408        0.500x         4.712x  empobrecida -> ENRIQUECIDA  <<< SE INVIERTE
hygrosensory           74        0.030x         0.283x  empobrecida -> empobrecida
thermosensory          29        0.070x         0.660x  empobrecida -> empobrecida
olfactory            2279        0.005x         0.047x  empobrecida -> empobrecida
visual              10853        0.002x         0.019x  empobrecida -> empobrecida
visual optic        77521        0.003x         0.028x  empobrecida -> empobrecida

PUBLICADO:  el paper afirma "Zero classes enriched. Seven classes depleted."
CORREGIDO:  4 enriquecidas, 5 empobrecidas
```

### Lo que esto le hace a la Propiedad 2

El paper construye su lectura conceptual sobre esa tabla, §3.3 y §4.2:

> *«Zero classes enriched. Seven classes depleted. No sensory class has more direct motor
> access than expected from graph density.»*

> *«The correct reading is: the topology has **concentrated** existing connections onto the
> somatosensory pathway, actively depleting all other pathways. … it suggests a principle
> of wiring budget allocation, **not proliferation**.»*

**Con la densidad corregida, cuatro clases tienen MÁS acceso motor del esperado.** La
afirmación «ninguna clase sensorial tiene más acceso motor directo que el esperado» es
falsa bajo la densidad correcta. Y la dicotomía «concentra, no proliferan» pierde su
evidencia: hay proliferación en la vía somatosensorial.

### Y la PARADOJA GUSTATIVA se disuelve

El paper dedica un párrafo entero, §3.3, a explicar una paradoja:

> *«Gustatory neurons have **half** (0.5×) the motor connections expected by density, yet
> still outperform MS controls (Z = +4.5σ). This implies that the modular topology channels
> the few existing gustatory→motor connections in a functionally effective manner…»*

**Con la densidad correcta, gustativa tiene 4,71× MÁS de lo esperado, no la mitad.**
No hay paradoja que explicar: gana contra los controles MS **porque tiene más conexiones
de las esperadas**, que es la explicación simple. El párrafo entero explica un fenómeno que
no existe.

**Nota de honestidad sobre esta sección:** la corrección es aritmética y exacta, pero los
**p-valores** de la Tabla 5 (binomiales) **no** escalan linealmente y **no los recomputé**.
Un `Obs/Exp` que cruza 1,0 cambia el signo del test, no solo su magnitud.

---

## 4. LO QUE EL PDF DESMIENTE DE MIS PROPIOS DOCS DE HOY

Tres correcciones, y las tres son mías.

### 4.1 La «discrepancia N = 100 / 40 / 20» NO EXISTE

Esta mañana escribí que era «un problema de integridad del paper». **Falso.** El PDF §2.4
y §3.4 lo declaran explícitamente, y son **cuatro** N distintos porque son **cuatro
análisis** distintos:

| análisis | null | N |
|---|---|---|
| estáticos (Net RDI, Tabla 3) | Maslov-Sneppen | **100** (3 lotes: 34+33+33) |
| perfiles de profundidad (Tabla 6) | Maslov-Sneppen | **20** |
| temporales (Tabla 8) | Maslov-Sneppen | **5** |
| estáticos | community-preserving | **10** |
| temporales | community-preserving | **5** |

**El paper es internamente consistente y yo comparé el abstract contra un documento de
re-corrida.** Comparar dos números de dos corridas distintas y llamarlo contradicción es el
patrón del sujeto equivocado (E-01).

### 4.2 El caveat de los Z gigantes YA ESTÁ EN EL PAPER

Escribí que `METHODS.md` «refutaba» los 161,9σ del draft. El PDF §2.7 tiene su propia
nota, y dice lo mismo:

> *«Some Z-scores reported herein exceed Z > 100σ. This reflects the extremely low
> inter-control variance of the Maslov-Sneppen null … **not implausible effect sizes**. The
> primary statistics for interpretation are Δ, p_perm, and bootstrap confidence intervals.»*

**El paper se auto-limita antes de que nadie se lo señale.** Mi «hallazgo» era leer una
advertencia que el autor ya había escrito.

### 4.3 Atribuí mal el 472 % a la vía olfatoria

Del HTML truncado leí «olfativa 4,719 (472 %) bloqueo activo». La Tabla 6 del PDF dice lo
contrario:

```
Pop.        1-hop   2-hop   3-hop   Profile
Mechano.    0.04%   135%    953%    Reflex + strong containment
Gustatory   0.05%   73%     704%    Reflex + gradual containment
Olfactory   0.00%   8.7%    10.7%   Free propagation
Visual L    12.1%   40%     496%    Progressive blocking
```

**Olfatoria es propagación LIBRE (10,7 %), la que bloquea progresivamente es VISUAL (496 %),
y la de contención fuerte es MECANOSENSORIAL (953 %).** Leí un volcado cortado y reporté
sobre él como si fuera la fuente.

### 4.4 Y dos cosas que declaré «ausentes» del paper y están

- **Normalización por columna:** §2.2, explícita, con cita a Jaeger 2001. La declaré como
  «algo del draft que no está en git»; está en el paper publicado.
- **El guard de NO_TESTEABLE del null CP:** §2.4, «Analytical property of the CP null», con
  la demostración de por qué `F_motor` es invariante a 1 salto y la conclusión de que
  «el null CP es informativo solo para métricas temporales multi-salto».

---

## 5. Y LO QUE MÁS DUELE: mi «t50 invertido» ESTÁ PUBLICADO

La Tabla 8 del paper:

```
Step  Phase       Real    CP      Z_CP     MS      Z_MS
15    During      0.687   0.711   -24.8    0.653   +40.3
60    End stim    0.630   0.663   -10.6    0.469   +97.1
80    Post+20     0.680   0.526   +29.5    0.111   +230
120   Post+60     0.807   0.368   +18.4    0.004   +923
195   Post+135    0.833   0.299   +14.8    0.001   +2842
```

**`Z_CP` es NEGATIVO en los dos pasos durante el estímulo.** O sea: el real queda **por
debajo** del null CP mientras el estímulo está activo. Y el paper lo explica en §3.6:

> *«During stimulus: Separation is modular. CP ≥ Real … Z_CP is negative, indicating that
> the CP null even separates slightly better.»*

Hoy reporté como hallazgo que «en t50 el real queda por debajo de los 39 nulls, con el
signo invertido», y esta mañana le dije a Abraham que el cruce de signo era **«lo único
vivo del conectoma y el número no está medido»**.

**Está medido, publicado, en cinco puntos temporales, y explicado.** Mi t50 es el paso 15.

---

## 6. LO QUE SÍ APORTA lo de hoy, medido contra el paper

Tres cosas, y una es lo que el paper mismo pide.

**6.1 N = 39 donde el paper tiene N = 5.** Limitación 2 del propio paper:

> *«**N = 5 for temporal CP.** Sufficient for Z = +14.8σ, but tighter CIs would require
> N ≥ 20.»*

**Corrí 39 nulls CP temporales.** Es **7,8×** el N del paper y casi **2×** el N≥20 que su
limitación pide. Eso no es re-descubrir: es pagar una deuda que el paper declara.

**6.2 El test global sobre 9 estadísticos.** El paper reporta Δ y p_perm **por métrica** y
no hace un test agregado. Mi corrida dio **p = 0,25 con potencia suficiente** sobre 9
estadísticos a la vez. **Es el instrumento honesto de comparaciones múltiples y el paper no
lo tiene.** Y es exactamente lo que `METHODS.md` recomienda: «one global statistic over the
twelve, not twelve tests with a corrected threshold».

**6.3 E/I por neuronas contra por aristas.** El paper reporta 40,0 % inhibitorio **por
arista**. Medido hoy: **29,95 % por neurona**, porque las inhibitorias tienen **1,557× más
salidas** (146,0 contra 93,7). No está en el paper y es relevante para su sección de
inhibición dirigida.

---

## 7. Y UN DATO QUE CAMBIA EL PERITAJE DE PATENTES DE HACE UNA HORA

§7 del paper, Data Availability:

> *«Analysis code, processed matrices, and propagation scripts are available at
> https://github.com/Mendieta-Architect/drosophila-connectome-propagation under **AGPL v3
> license**.»*

Dos cosas:

1. **El repo citado NO es este.** El paper apunta a `Mendieta-Architect/...`, no a
   `gatehot59-star/drosophila-fep-connectome`. Son dos repos y el publicado es el otro.
2. **AGPL v3 tiene concesión EXPRESA de patente en su sección 11.** En el peritaje de hace
   una hora escribí que «Apache-2.0 concede licencia de patente expresa; MIT no» y que
   había que elegir con cuidado. **La elección ya está hecha y publicada desde marzo.**
   Cualquier patente que cubriera ese código ya tiene licencia otorgada a todo el que lo
   reciba.

**Esto no lo había contemplado, y cambia la conclusión de ese peritaje para el software
del conectoma.** No toca a DualBrain embebido, que no está en ese repo ni en ese paper.

---

## 8. NO MEDIDO

- **No recomputé los p-valores de la Tabla 5.** El test es binomial y **no** escala
  linealmente con la densidad. Los ratios sí, los p no. Un ratio que cruza 1,0 invierte el
  sentido del test y eso hay que recorrerlo con el código, no con una multiplicación.
- **No re-corrí la Tabla 5 desde el dato.** Usé la linealidad de la fórmula que
  `METHODS.md` documenta. Si la fórmula archivada difiere de la documentada, la corrección
  cambia.
- **No verifiqué las poblaciones de la Tabla 1** (43.056 visual L, 3.067 somato, etc.)
  contra las anotaciones.
- **No verifiqué la Tabla 2** (cancelación contralateral 1,37 y sus cuatro flujos).
- **No verifiqué la Tabla 6** (los perfiles de profundidad 1/2/3 saltos).
- **No verifiqué la Tabla 7** (reciprocidad por tipo de circuito). Solo la global, que dio
  exacta.
- **No abrí el repo `Mendieta-Architect/drosophila-connectome-propagation`** ni verifiqué
  que exista ni qué contiene.
- **No leí `docs/ERRATUM.md`** (31.729 B), que es donde esta propagación del overflow
  podría estar ya declarada. **Si está, §2 y §3 de este documento son redundantes**, y ese
  es el riesgo más probable de todo lo que escribí acá.
