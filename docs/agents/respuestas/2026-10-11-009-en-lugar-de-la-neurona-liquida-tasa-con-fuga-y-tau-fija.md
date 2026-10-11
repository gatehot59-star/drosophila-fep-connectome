# 2026-10-11-009 · En lugar de la neurona líquida: tasa con fuga y τ fija sobre el cableado real; la τ líquida sólo en la memoria de DualBrain

**Doc espejo:** https://app.clickup.com/90171457413/docs/2kza6fw5-21137

**Base:** `main` en `403762a` (respuesta 008). Pregunta técnica sin corrida nueva: recibo corto.

## 1. Pedido

Verbatim: «SI NO USAS NURONA LIQUIDA QUE USAS A CZMBIO PARA EMULAR PARTES DE LA MOSCA».

Resumen: si la neurona líquida no es la pieza, qué se usa para emular una parte del cerebro de la mosca.

## 2. Herramientas y máquina

- Lecturas: GitHub MCP (`list_commits` de `main`, HEAD `403762a`; listado de `docs/agents/respuestas/`), el Doc espejo de la 007 y una búsqueda web del paper de FlyVis (Lappalainen y otros, Nature 2024).
- Escrituras: este archivo en `main` y su Doc espejo en ClickUp.
- Máquina: ninguna corrida. `brain-env`, Actions y Kaggle sin uso; sin cuota ajena.

## 3. Respuesta

**En lugar de la neurona líquida va una neurona de tasa con fuga y τ fija: tu SparseLTC sin la parte que depende de la entrada, corriendo sobre el cableado real de la parte que se corta de FlyWire, con sus signos, y siempre contra un brazo lineal.** El conocimiento lo pone el cableado; la neurona sólo integra con fuga y no explota. La τ líquida queda en un solo lugar, la memoria de DualBrain, que es donde pagó (MultiCue, 3,8×).

| Pieza | Qué se usa | De dónde sale |
|---|---|---|
| El conocimiento | el cableado real del motivo como máscara fija, con signo por Dale (FlyWire v783: 96.672 E, 41.333 I, 0 mixtas) | 007, capas L0 y L1 |
| La neurona | `z ← (1-τ)·z + τ·tanh(W·z + U·x)` con τ fija (uniforme en el producto), CSR, radio espectral 0,99 y Q15 con LUT de tanh centrada | 007, capa L2 |
| El control obligatorio | un brazo lineal con la misma entrada: si la parte no le gana, no entra | HC-2: SparseLTC empata 48/48 con el lineal |
| Lo que se entrena | la ganancia por par de tipos celulares, la compuerta de DualBrain, la memoria de DBC3 y el readout | 007, §3 y §5 |
| La salida | órdenes por descendentes: GF (DNp01) escapar, DNa01 y DNa02 girar, oDN1 avanzar, MDN retroceder; candidatas de literatura | 007, capa L3 |
| La estabilidad | cordón sintético: lazo de actitud con giróscopo (lo que hace el haltere) o CPG | 007, capa L4; sin él, el dron pasa 30° en 0,267 s |
| La τ líquida | sólo en la memoria de DualBrain (`LiquidCell`) | 008, contraste C6 |

## 4. Por qué no la líquida: lo ya medido

Copiado de la 008 y de la 007; acá no corrió nada nuevo.

**Reservorio recurrente sobre el motivo de 26 neuronas** (Actions run 38143998992; log crudo en `results/brazo_s_recurrente_2026-10-11/run.log`, rama `titan/brazo-s-recurrente-2026-10-11`, commit `9473852`). Contraste C4, τ líquida (LW) contra τ fija heterogénea y congelada (RW): indistinguibles en 4/4.

| Tarea | LW, τ líquida (MSE medio) | RW, τ fija (MSE medio) |
|---|---|---|
| Gated | 0.019249 | 0.021818 |
| LinScale | 0.000569 | 0.000554 |
| MultiCue | 0.001551 | 0.001050 |
| CR | 0.000666 | 0.000664 |

**Memoria de DualBrain** (misma corrida). Contraste C6, A con τ líquida contra F con τ constante por unidad: A gana sólo en MultiCue, 0,263× (p_welch 0,0011; Holm 0,0044), y empata en las otras tres.

| Tarea | A, τ líquida (MSE medio) | F, τ constante (MSE medio) |
|---|---|---|
| Gated | 0.000236 | 0.000266 |
| LinScale | 0.000055 | 0.000061 |
| MultiCue | 0.000098 | 0.000374 |
| CR | 0.000040 | 0.000071 |

**Sobre el conectoma** (007, tabla del texto BEEC): SparseLTC con τ fija por neurona empata 48/48 con el control lineal (HC-2); la τ compleja da p = 0,60; en el mismo subgrafo, la ecuación tipo FlyVis le gana a SparseLTC real por 5,56 puntos (una semilla).

**Comparador externo, verificado hoy** en [Lappalainen y otros, Nature 634, 2024](https://www.nature.com/articles/s41586-024-07939-3) (también en PMC11525180), verbatim:

> "We assumed that neurons of the same cell type shared the same neuron time constant and resting membrane potential."

> "The only free parameters in our model are the single-neuron time constants and resting membrane potentials (two parameters per cell type), and the unitary synapse strengths (one parameter per type-to-type connection)."

> "Connectome constraints, and our assumption of spatial homogeneity (that is, the hexagonally convolutional structure of the network), result in a marked reduction to just 734 free parameters for this large network model."

> "We show that this strategy is more likely to be successful when neurons are sparsely connected"

El modelo tiene 45.669 neuronas y 1.513.231 conexiones en 64 tipos celulares. Es la misma receta que la 007 eligió para el producto: máscara fija, τ fija y sólo una ganancia por par de tipos entrenable. La última cita va en la misma dirección que la 008: lo que paga es la sparsity. [Shiu y otros, Nature 2024](https://www.nature.com/articles/s41586-024-07763-9) usan LIF con spikes para el cerebro entero: es la alternativa si hiciera falta spike, y acá no está medida.

## 5. Letra chica

La neurona elegida está respaldada; el valor de la parte de la mosca, todavía no. En tareas genéricas el cableado del motivo empata con su shuffle en 4/4 (C2: p_welch 0,9899; 0,8622; 0,3754; 0,9625), no le gana al ruido congelado (C1: 0/4) y el reservorio rinde peor que el B feedforward de agosto en 3/4 (C7). La prueba que falta es la función propia del motivo: looming → escape a lazo cerrado, con S, τ fija y τ líquida como brazos.

## 6. Antes de firmar

| Afirmación | Instrumento | ¿Podía dar rojo? | Veredicto |
|---|---|---|---|
| La τ fija rinde como la líquida en el reservorio | Welch, C4, run 38143998992 | sí: con p < 0,05 la marcaba distinta | medido: indistinguibles 4/4; la equivalencia formal (potencia) NO MEDIDA |
| La τ líquida paga en la memoria sólo en MultiCue | Welch y Holm, C6 | sí | medido: 1/4 |
| FlyVis usa τ fija por tipo celular | texto del paper (Nature y PMC) | sí: podía decir otra cosa | verificado hoy |
| Esta receta emula bien una parte de la mosca | ninguno | no | NO MEDIDO |

## 7. Archivos generados

- `docs/agents/respuestas/2026-10-11-009-en-lugar-de-la-neurona-liquida-tasa-con-fuga-y-tau-fija.md` (este archivo). Ningún código ni resultado nuevo; `CONTEXTO-drosophila-fep.md` no cambia.

## 8. NO MEDIDO

- τ fija contra τ líquida, y contra la ecuación tipo FlyVis, en la función propia del motivo (looming → escape a lazo cerrado).
- El brazo S en esa misma función.
- τ uniforme contra τ líquida en el reservorio: la 008 usó τ fija heterogénea, U[0,06; 0,18].
- La τ propia de DBC3 aislada: F probó la `LiquidCell` de DualBrain.
- F con parámetros igualados: entrena 128 menos que A.
- El motivo en Q15 corriendo en un ESP32 real.
- LIF con spikes contra tasa con fuga en este pipeline.
- La potencia de los empates.
