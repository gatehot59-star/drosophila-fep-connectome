# PERITAJE DE PATENTABILIDAD · 2026-08-26

**Pregunta de Abraham:** «¿tenemos hallazgos patentables en ese documento?»

**ADVERTENCIA DE ALCANCE, primero.** Esto es un peritaje técnico sobre qué tipo de objeto es
cada cosa del expediente y qué dice la ley verificada en vivo. **No es asesoramiento legal**
y no sustituye a un agente de la propiedad industrial matriculado. Lo que sí hago es
medir las fechas y clasificar los objetos, que es donde se pierde el derecho por descuido.

---

## 1. 🚨 EL DATO QUE MANDA SOBRE TODOS LOS DEMÁS: la fecha

Verificado en vivo contra Zenodo:

```
DOI:        10.5281/zenodo.19136948  (y .19136947, dos registros)
Titulo:     Signal Propagation Properties in the Drosophila melanogaster Connectome:
            Intermodal Isolation, Differential Motor Access, and Non-Trivial
            Temporal Amplification
Autor:      Jorge Abraham Mendieta
Tipo:       preprint
PUBLICADO:  2026-03-20
```

**Está público desde el 20 de marzo de 2026, hace 5 meses y 6 días, bajo su propio nombre.**

Y el abstract público ya divulga, textual: cancelación contralateral **= 1.37**, RDI que
sube de **0.63 a 0.83** post-estímulo, **Z_CP = +14.8σ**, **Δ = +0.365**, **Z = +4.5σ**,
**τ = 0.119** con τ_m ≈ 8.4 ms, reciprocidad **36×** sobre la expectativa de densidad, y
**7 de 10** clases sensoriales por debajo de la expectativa.

**Eso es estado de la técnica desde marzo. No hay vuelta que darle.**

### El reloj, contado

Argentina tiene **período de gracia de 12 meses** («divulgación inocua», art. 5 de la ley
24.481) **cuando la divulgación la hizo el propio solicitante**, que es este caso. Las
pruebas de esa divulgación se presentan junto con la solicitud.

```
divulgacion:  2026-03-20
vence:        2027-03-20
hoy:          2026-08-26
QUEDAN:       206 dias
```

**Dos advertencias medidas sobre ese período, y las dos son malas:**

1. **Argentina NO es miembro del PCT.** Una solicitud presentada afuera no entra por esa
   vía. Hay que presentar en Argentina y después país por país, o usar la prioridad del
   Convenio de París (12 meses desde la presentación argentina).
2. **La Corte Suprema ya resolvió que una divulgación no es automáticamente «inocua»**
   (caso S.C.R.A.S. c/ INPI, confirmado en enero de 2021: la publicación de una solicitud
   PCT **no** se considera inocua a los fines del art. 5). O sea que el período de gracia
   **se invoca y se prueba**, no se presume.

---

## 2. LOS HALLAZGOS DEL PAPER: **NO** son patentables, y no por la fecha

Aun si nada estuviera publicado, **no lo serían**, y la razón es de categoría.

La ley 24.481 exige **invención**, y su artículo 6 excluye expresamente los
**descubrimientos**, las **teorías científicas** y los **métodos matemáticos**.

| lo que tenemos | qué tipo de objeto es |
|---|---|
| «el conectoma aísla modalidades por inhibición dirigida» | **descubrimiento** sobre un cerebro que existe |
| cancelación contralateral 1.37 | **medición** de un objeto natural |
| RDI 0.63 → 0.83, Z_CP +14.8σ | **medición** |
| cancelación GABAérgica 0,04 % / 12,1 % / 472 % | **medición** |
| las inhibitorias tienen 1,557× más salidas | **medición**, y es de hoy |
| τ = 0.119 ≈ 8.4 ms | **parámetro observado** en el rango fisiológico |

**Ninguno de estos es una cosa que se fabrique. Son cosas que se encontraron.**
Y la mosca no se inventó: está desde antes.

**Lo que SÍ protege a un hallazgo científico es la PRIORIDAD, y ya la tiene:** el DOI con
fecha 2026-03-20 y su nombre. Eso es lo que hace que si mañana otro publica el 1.37, la
fecha diga quién llegó primero. **Ya está hecho y no cuesta nada mantenerlo.**

---

## 3. EL INSTRUMENTO (`motor.py` / `motor_v2.py`): débil

Es software que calcula. INPI **sí** tramita invenciones implementadas en computadora
(hay un Anexo VII de las Directrices de Patentamiento dedicado a «la protección de las
invenciones relacionadas con programas de computación», modificado por la Resolución
P-318/2012), pero el criterio pide **efecto técnico** sobre algo, no solo un cálculo mejor.

Un normalizador espectral con verificación posterior y dos instrumentos cruzados es
**buena ingeniería de método** y probablemente **no supera la exclusión de método
matemático**. Y el altura inventiva es dudosa: iteración de potencia, ARPACK y permutation
tests son estándar desde hace décadas.

**Y acá el derecho que SÍ tiene y no está usando:** el software goza de **derecho de autor**
automático desde que se escribe (ley 11.723, que incluye expresamente los programas de
computación). No hay que pedirlo. Se puede **registrar** en la DNDA para tener fecha
cierta, y eso sí cuesta poco. **Los 8 md5 verificados en el repo ya funcionan como
evidencia de autoría con fecha**, que es el 80 % del valor práctico.

---

## 4. EL ÚNICO CANDIDATO REAL: **DualBrain en silicio**

De todo el expediente, lo que más se parece a una invención es esto:

```
xtensa-esp32-elf-gcc -std=c99 -Os -I. -c -o /tmp/db_os.o dualbrain.c
COMPILA_OK_exit0
   text    data     bss     dec     hex
   1336       0       0    1336     538
```

**1.336 bytes de .text en el target real**, contra 2.496 de x86. Más los **704 B de RAM**.
Y el controlador C99 corriendo inferencia activa **sin LLM** en un microcontrolador.

Por qué este es distinto de todo lo anterior:

- **Es un dispositivo, no un cálculo.** Un controlador embebido que hace inferencia en
  1,3 kB de flash tiene **efecto técnico** sobre un sistema físico.
- **Tiene un número duro y medido**, no una estimación. Y está recomputable desde los md5
  de las fuentes publicados en `CONTEXTO-ENTORNO.md` §13.1.
- **NO está en el paper publicado.** El Zenodo es sobre el conectoma. La línea embebida
  no se divulgó ahí, o sea que **su novedad no la destruyó el 20 de marzo**.

**Lo que le falta para ser una solicitud, y es bastante:**

1. **Reivindicaciones**, que es lo único que se patenta. No se patenta un archivo: se
   patenta lo que las reivindicaciones delimiten.
2. **Estado de la técnica.** TinyML, TensorFlow Lite Micro y una biblioteca entera de
   inferencia en microcontroladores existen. **La pregunta no es si funciona: es qué hace
   distinto de lo que ya está publicado.** Y eso **no está medido**.
3. **Aplicación industrial declarada.** Un controlador «para qué».

---

## 5. 🚨 EL CONFLICTO DURO, y hay que decidirlo antes de gastar un peso

**ARC Prize 2026 exige OPEN SOURCE en los tres tracks para cobrar.** Medido en la página
oficial y ya commiteado: *«Participants must open source their solutions before receiving
official private evaluation scores. This applies across all three competition tracks»*, y
en ARC-AGI-2: *«participants eligible for a prize will be removed from the competition if
they do not open source their solutions»*.

**Patentar y abrir el código no son incompatibles, pero el ORDEN es todo:**

- Si se **presenta la solicitud primero** y después se abre, la fecha de prioridad queda
  fijada y el open source no la destruye.
- Si se **abre primero**, esa divulgación arranca su propio reloj de 12 meses, y encima
  hay que probarla como divulgación propia.
- Y una licencia open source puede otorgar **licencia de patente implícita o expresa**
  según cuál se elija. **Apache-2.0 concede licencia de patente expresa; MIT no la
  menciona.** Elegir la licencia sin mirar esto es regalar la patente que se pagó.

---

## 6. HALLAZGO COLATERAL, y es un problema de integridad del paper

Cruzando el abstract publicado contra el repo aparece esto:

| fuente | nulls de Maslov-Sneppen |
|---|---|
| **abstract publicado en Zenodo** (2026-03-20) | **N = 100** |
| `docs/METHODS.md` en git | **40**, semillas 4200+17i, verificados por null |
| draft de marzo del HTML de Arena | **20** |

**Tres números distintos para el mismo ensemble.** Y el mismo abstract dice
«community-preserving, N = 5-10» mientras `METHODS.md` documenta **40** con 22,2 minutos
de corrida.

Esto **no** es un tema de patentes: es un tema de que un revisor que compare el abstract
con los métodos va a encontrar la discrepancia antes que cualquier otra cosa. Y el
`ERRATUM.md` existe justamente para eso.

**No lo resuelvo acá porque no lo medí:** no leí el PDF completo del Zenodo ni el
`ERRATUM.md` de 31.729 B. Puede estar ya declarado ahí.

---

## 7. MI RECOMENDACIÓN, y es contra patentar ahora

Criterio declarado: **qué acerca el producto a existir y a generar dinero**, que es el fin
declarado de MUDH.

**Una patente argentina cuesta plata, tarda años, y solo vale lo que uno pueda gastar en
hacerla valer.** Es un derecho de exclusión: sirve para demandar a quien copie. Sin
capacidad de litigar, un título de patente es un adorno caro.

**Lo que SÍ tiene valor hoy, en orden:**

1. **El Milestone #2 de ARC: 37.500 USD garantizados en 35 días**, sin abogados, sin
   tasas, sin esperar. Es la única plata de este expediente con fecha y monto.
2. **La prioridad científica ya está asegurada** con el DOI del 20 de marzo.
3. **El derecho de autor del código es automático** y los md5 en git le dan fecha cierta.
4. **El método y la bitácora de hipótesis muertas** son el activo cedible de verdad, y no
   se patentan: se documentan, que es exactamente lo que se viene haciendo.

**Lo único que haría con reloj:** si la línea embebida (DualBrain en chip) va a ser
producto, **medir el estado de la técnica de TinyML antes del 2027-03-20** y con eso
decidir. Esa medición la puedo hacer yo y cuesta una tarde. La decisión de patentar no.

---

## 8. NO MEDIDO

- **No leí el texto completo del artículo 6** de la ley 24.481 en esta corrida: leí la
  página de legislación del INPI y las FAQ, y las exclusiones las cito de conocimiento
  general del régimen. **Hay que verificar el texto literal antes de apoyarse en esto.**
- **No leí el Anexo VII** de las Directrices de Patentamiento. Sé que existe y que
  P-318/2012 lo modificó; **no sé qué dice**.
- **No busqué estado de la técnica de TinyML** ni de inferencia activa en
  microcontroladores. Es el trabajo que falta para que el punto 4 sea una decisión y no
  una intuición.
- **No leí el PDF completo del Zenodo**, solo el abstract vía DOI. La discrepancia
  N=100/40/20 sale de comparar abstract contra `METHODS.md`.
- **No leí `docs/ERRATUM.md`** (31.729 B). Puede ya declarar esa discrepancia.
- **No verifiqué si hay dos registros distintos o uno duplicado** en Zenodo
  (.19136947 y .19136948 aparecen los dos con la misma fecha y título).
- **No soy abogado y esto no es asesoramiento legal.** Para presentar hace falta un agente
  de la propiedad industrial matriculado.
