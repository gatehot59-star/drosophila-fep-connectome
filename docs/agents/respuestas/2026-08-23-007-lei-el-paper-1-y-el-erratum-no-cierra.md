# resp 007 · SÍ puedo leer el Paper 1, y contradice tres cosas que yo mismo afirmé

**Fecha:** 2026-08-23 21:17–21:35 (America/Buenos_Aires) · **Modo:** TITAN FULL · **Tipo:** auditoría de documento

## 1. Pedido

> «¿Podés leer los 7 documentos que te compartí, desde el primero que fue el paper que publiqué?»

## 2. Herramientas declaradas (C-03)

- Contexto vivo en git: leído antes de responder.
- Búsqueda del workspace: localización de los adjuntos indexados y **lectura del texto extraído** del PDF del Paper 1.
- Búsqueda web: intento de localizar el registro de Zenodo por DOI.
- GitHub: **un commit**. Cero Kaggle, cero container, nada mergeado.

## 3. Qué se puede leer y qué no — medido, no supuesto

| # | Documento | ¿Legible? |
|---|---|---|
| 2 | **`Paper1_SignalPropagation (1).pdf`** | **SÍ, texto completo extraído.** Abstract, §1–§5, Tablas 1–11 |
| — | `Análisis de Publicabilidad de Manuscrito.pdf` | SÍ, incluye el LaTeX del Paper C y las dos rondas de revisión |
| 4,5,6 | `Arena _ Benchmark & N.html` | **NO como conversación.** Devuelven el markup de la página: CSS, bundles de Next.js, meta tags. El contenido del chat no está en el HTML guardado |
| 1,3,7 | Patente, Script R, PDF de Gemini | no localizados por nombre en esta pasada |

**Y un dato que explica una sensación tuya:** varios adjuntos están **subidos más de una vez con IDs distintos**. `Arena _ Benchmark & 2.html` aparece 2 veces, `& 6.html` **3 veces**, y `Análisis de Publicabilidad de Manuscrito.pdf` 2 veces. No es que los pasaste dos veces por error: están duplicados en el workspace.

## 4. TRES hallazgos que contradicen afirmaciones mías previas

### 4.1 El DOI del PDF es un placeholder

```
PREPRINT — Not peer reviewed
Deposited at Zenodo, March 20, 2026   ·   DOI: 10.5281/zenodo.XXXXXXX
```

**`XXXXXXX` literal.** Eso resuelve dos cosas a la vez: por qué el borrador del erratum pide `[DOI v1]` (no es que faltara el dato tuyo, **el paper no lo tiene**) y por qué la búsqueda web del DOI `10.5281/zenodo.19136948` no devuelve ningún registro. **Ese número de DOI no sale del PDF.** De dónde salió es una pregunta abierta.

### 4.2 La densidad mal SÍ está en el paper publicado

Mi auditoría previa afirmó: *«Este paper evita el número contaminado por completo: dice "la densidad del grafo hace probable…" en prosa, sin citar el valor.»*

**Falso.** Verbatim del PDF:

```
2.1 Connectome
FlyWire v783: 15,091,983 connections among 138,639 neurons. Weight:
Excitatory x Connectivity (9,059,302 excitatory, 60.0%; 6,032,681
inhibitory, 40.0%; E/I = 1.50). Density = 0.0074.
```

Y el Abstract:

```
...confirming dependence on fine wiring — including reciprocity
(36x over density expectation).
```

**El 0,0074 y el 36× están los dos en el paper publicado**, uno en Methods y el otro en el Abstract. La cadena «este paper → patente → Paper C» ordenada por madurez del manejo de ese número **queda refutada**: los tres lo tienen mal.

### 4.3 EL MÁS GRAVE: el erratum E3 apunta a una tabla que no existe

El borrador del erratum dice, sobre «Table 7»:

| | Real | Control μ | Control σ | Δ | Ratio |
|---|---|---|---|---|---|
| Step 195 | 0.8328 | 0.0005 | 0.0003 | 0.832 | 1,559× |

**En el PDF publicado, Table 7 es «Reciprocity by circuit type»** (Intra-motor 41,3%, Intra-optic 32,0%, Optic→motor 0,0%…). No tiene columna Ratio ni control.

La tabla de RDI es **Table 8**, y su estructura es otra:

```
Table 8: Cosine RDI — Real vs. CP vs. MS.
Step  Phase       Real    CP      Z_CP    MS      Z_MS
 15   During      0.687   0.711   -24.8   0.653   +40.3
 60   End stim    0.630   0.663   -10.6   0.469   +97.1
 80   Post+20     0.680   0.526   +29.5   0.111   +230
120   Post+60     0.807   0.368   +18.4   0.004   +923
195   Post+135    0.833   0.299   +14.8   0.001   +2842
```

**No hay columna Ratio, no hay 0.0005 ± 0.0003, y el 1.559× no aparece** ni en el Abstract, ni en §1.3, ni en §3.4, ni en §4.1, que son los cuatro lugares donde el erratum dice que está.

**Consecuencia:** el erratum, tal como está redactado, corrige un número y una tabla que pertenecen a **otro documento** (probablemente la patente o el Paper C). **No se puede subir a Zenodo así.** Antes hay que decidir cuál de los tres documentos contiene realmente el 1.559× y reescribir E3 contra ese.

Es el mismo error de siempre con otra cara: **medir el sujeto equivocado** (E-01). Y esta vez el sujeto equivocado iba a terminar en una publicación con DOI.

## 5. Dos cosas que el paper hace mejor de lo que yo le reconocía

**El guard de tautología ya estaba en el paper**, §2.4 verbatim:

```
Analytical property of the CP null. Net RDI at 1-hop is exactly invariant
under CP null (sigma = 0), because F_motor depends only on the block weight
sum, not on the distribution among individual neurons. Verified empirically:
F_motor identical for 3 CP realizations. The CP null is informative only for
temporal (multi-hop) metrics.
```

Eso es exactamente el `sd=0 → NO TESTEABLE` que después implementé en `src/motor.py` como si fuera aporte propio. **Estaba escrito y derivado analíticamente en el paper de marzo.**

**Y la cita a Betzel está bien en el cuerpo.** §1.2: *"Betzel et al. [2026] demonstrated convergence of sensory cascades…"*. La atribución a «Barsotti» que declaré como error del Paper 1 no aparece en el cuerpo. Si está en la bibliografía, no lo puedo confirmar: la lectura se cortó en §5.

## 6. Archivos generados

- este archivo
- `docs/agents/CONTEXTO-drosophila-fep.md` actualizado con las tres correcciones

## 7. NO MEDIDO, declarado

- **No leí las Conclusiones, la bibliografía completa ni el Material Suplementario** del PDF: la extracción se cortó en §5 Limitations. El 1.559× podría estar en las Conclusiones, y en ese caso E3 se salva parcialmente. **Hay que leer esa sección antes de decidir.**
- **No confirmé si la bibliografía dice Barsotti o Betzel.**
- **De dónde salió el DOI `10.5281/zenodo.19136948`** que vengo citando: no está en el PDF y la web no lo encuentra.
- Los adjuntos 1, 3 y 7 (patente, Script R, PDF de Gemini de 101 páginas) no los localicé por nombre en esta pasada. **No afirmo que no estén.**
- Los HTML de Arena: contienen el markup de la página. **No verifiqué si el texto del chat está embebido en algún payload JSON del bundle**, solo que no aparece en el HTML plano.
