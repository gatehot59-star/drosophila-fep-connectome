# EVIDENCIA CRUDA · 2026-08-26 · el erratum no está publicado, y eso es el hallazgo

**Lo que dijo Abraham:** «los hallazgos son post-creación de ese paper, pero no
post-publicación».

**Tenía razón, y lo medí.**

---

## 1. MEDIDO: el v2.0 no está depositado

API de Zenodo, los dos identificadores:

```
record 19136947
   version    : 1.0
   publicado  : 2026-03-20
   modificado : 2026-03-20T18:38:16
   conceptrecid: 19136947   este id: 19136948
   is_last=True  index=0
   contiene '36'                  : True
   contiene 'four parameter-free' : True
   contiene '338'                 : False

record 19136948   -> identico
```

Tres cosas quedan establecidas:

1. **`version = 1.0` y `is_last = True` con `index = 0`.** No hay v2.0. El concept DOI
   `19136947`, que por diseño resuelve siempre a la última versión, resuelve a v1.0.
2. **`modificado = 2026-03-20T18:38:16`.** El registro no se tocó desde el día del
   depósito.
3. **La descripción pública todavía contiene «36» y «four parameter-free», y NO contiene
   «338».** O sea: las dos cifras que el erratum corrige siguen públicas y la corregida no
   aparece en ninguna parte.

### El reloj

```
deposito v1.0 : 2026-03-20
hoy           : 2026-08-26
DIAS          : 159
```

**159 días con «Zero classes enriched. Seven classes depleted» público**, una frase que el
propio erratum declara **withdrawn**. Cualquiera que cite el paper hoy cita algo retirado
en un documento que no puede leer.

---

## 2. Y esto tiene DOS consecuencias opuestas, que hay que separar

### 2.1 El daño científico está corriendo

El erratum tiene **nueve items**, y sus propias palabras: *«items 1 to 3 change reported
values and one qualitative conclusion»*. Está terminado, es exhaustivo, cita a Lin et al.
y a Bates et al. que v1.0 no citaba, y hasta **se retracta de una afirmación falsa que
había hecho sobre el trabajo ajeno** (item 3, la retracción interna).

**Y no existe para nadie afuera.** Está en git, en una rama de trabajo.

Depositar el v2.0 en Zenodo es **subir un archivo a un registro que ya existe** y que ya
tiene el mecanismo de versiones previsto (el concept DOI está justamente para eso). Es de
las acciones más baratas de todo el expediente.

### 2.2 Pero la novedad está INTACTA, y eso es un activo

Y acá es donde la observación de Abraham cambia el peritaje de patentes de hace una hora.

**Lo que está divulgado desde el 20-mar** (y por lo tanto es estado de la técnica): 1.37,
RDI 0.63→0.83, +14.8σ, Δ=+0.365, τ=0.119, 36×, y las nueve filas de la Tabla 5 con sus
ratios equivocados.

**Lo que NO está divulgado:** el 338,8×, las cuatro clases enriquecidas, la jerarquía de
ruteo contra 40 nulls de grado con 8 de 8 signos preservados, el rank 1 de 41 en
reciprocidad, el spread de 283×, la tabla de reciprocidad por umbral de sinapsis, y el
item 9 completo.

**Ninguna de esas cosas tiene reloj de gracia corriendo, porque el reloj arranca con la
divulgación.** Y depositar v2.0 lo arranca.

**Aclaración honesta:** eso **no** las vuelve patentables. Siguen siendo mediciones de un
objeto natural, excluidas por el art. 6. La consecuencia real es de **prioridad y de
orden**, no de patente: si alguna vez algo de esa línea va a protegerse, se presenta antes
de depositar, no después.

---

## 3. Y AHORA LO MÍO: mi hallazgo de hace diez minutos era REDUNDANTE AL 100 %

Declaré el riesgo y el riesgo se materializó. El erratum tenía **todo**, antes y mejor.

| lo que reporté como hallazgo | dónde estaba ya |
|---|---|
| «el overflow se propaga a dos resultados titulares» | **item 1**, subtítulo literal: *«Two published quantities descend from that single line»* |
| reciprocidad corregida = 338,8× | **item 3**, el mismo número exacto |
| gustativa se invierte de empobrecida a enriquecida | **item 2**, columna «sign reversed» |
| «cuatro enriquecidas» | **item 2**: *«4 enriched, 4 depleted, 1 within expectation»* |
| «la paradoja gustativa desaparece» | **item 2**, §Consequence: §3.3 y §4.2 **withdrawn** |
| «no recomputé los p-valores binomiales» | **Outstanding verification 3**, declarado abierto |

### Y su número es MEJOR que el mío, por una razón que vale registrar

Yo escalé el ratio **publicado y redondeado**: 0,5 × 9,4244 = **4,712×**.
El erratum **recomputó desde el dato**: **4,482×**.

La diferencia es que el ratio real bajo la densidad desbordada es **0,476**, no 0,5:
0,476 × 9,4244 = 4,486, que es lo que ellos reportan. Lo mismo en mechano: yo 12,252×
desde 1,3; ellos 12,378× desde 1,314.

**Mi escalado propagó el redondeo del paper.** Multiplicar una cifra publicada a una
cifra significativa por un factor exacto da un número con la precisión de la peor de las
dos. Es aritmética correcta sobre una entrada degradada, y se ve como una medición.

### Dos errores más, también del turno anterior

**a) El repo citado.** Dije «el paper apunta a `Mendieta-Architect/...`, no a este: son dos
repos y el publicado es el otro». El **item 8** dice: *«No repository was ever created at
that path and the account name is incorrect. The correct location is
`github.com/gatehot59-star/drosophila-fep-connectome`»*. **No son dos repos: la URL
publicada nunca existió, y el correcto es este.**

**b) La licencia.** Dije que AGPL v3 concedía patente expresa y que «la elección ya está
hecha». El **item 8** dice: *«This is superseded: GPLv3 for the analysis code, and GPLv3
plus a commercial option for the embedded inference engine and the network topologies.»*

**Abraham ya había resuelto exactamente el problema que yo le planteé hace una hora**, y con
el mecanismo correcto: **licenciamiento dual**. GPLv3 para el análisis, GPLv3 + opción
comercial para el motor embebido. Eso monetiza sin patente y sin litigar, que es la
objeción que yo mismo había puesto contra patentar.

---

## 4. Qué sobrevive de hoy, y es chico

Sobre **el paper**, una sola cosa que no encuentro en el erratum:

- **E/I por neuronas contra por aristas.** El paper reporta 40,0 % inhibitorio por arista.
  Medido: **29,95 % por neurona**, porque las inhibitorias tienen **1,557× más aristas de
  salida** (146,0 contra 93,7). Y por peso el ratio E/I es **1,477**, no 1,50 (que es el
  del conteo). Relevante para §3.1, inhibición dirigida.

Y una que **se debilita** al leer el erratum:

- Mis **39 nulls CP temporales** los presenté como pago de la Limitación 2 del paper
  («N ≥ 20»). Pero **Outstanding verification 4** dice que **la Tabla 8 no es reproducible
  del código archivado** y que *«the six published values do not appear in any of the 40
  archived notebooks»*. Así que mis 39 nulls corren **mi** métrica, no la del paper: no son
  una réplica de la Tabla 8 y no cierran esa limitación.

El resto de lo de hoy (identidad v1/v2 a 2,22e-16, el fix de `rankdata`, el A/B de los 39)
es sobre **mi instrumento**, no sobre el paper. Vale, y es otra cosa.

---

## 5. NO MEDIDO

- **No verifiqué si el erratum está publicado en otro lado** (bioRxiv, un PDF en el repo
  público, la página de GitHub). Medí **Zenodo** y ahi no está.
- **No verifiqué si `LICENSE` en el repo ya dice GPLv3** o si sigue en AGPL. El item 8 dice
  «See LICENSE»; no abrí el archivo.
- **No verifiqué la rama.** Todo lo que leí está en `titan/twohop-nulls`. Si `main` tiene
  otra versión del erratum, no la vi.
- **No verifiqué el E/I por neuronas contra el erratum entero** palabra por palabra: busqué
  el concepto y no lo encontré, que no es lo mismo que probar que no está.
- **No sé por qué el v2.0 no se depositó.** Puede haber una razón deliberada (esperar a
  cerrar los nueve items de Outstanding verification, por ejemplo) y **no la pregunté**.
  Reportar «falta depositar» como si fuera un olvido sería suponer.
