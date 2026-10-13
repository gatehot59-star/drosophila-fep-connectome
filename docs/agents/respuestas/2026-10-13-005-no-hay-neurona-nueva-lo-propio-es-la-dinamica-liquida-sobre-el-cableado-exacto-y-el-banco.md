# 2026-10-13-005 · No hay neurona nueva: lo propio es poner la dinámica líquida sobre el cableado exacto de la mosca y el banco que la falsa

## Veredicto

- **[LITERATURA] La neurona no es nueva.** Ninguna de nuestras dos variantes líquidas es un invento nuestro:
  - **La líquida nativa de SparseLTC**, τ_ef = τ / (1 + g·|drive|), es de la familia LTC. Hasani et al. (AAAI 2021, doi 10.1609/aaai.v35i9.16936) definen τ_sys = τ / (1 + τ·f(x, I, t, θ)).
  - **La que ganó entrenada en el escape** (012 a 015) usa t = sigmoid(b + Vx·x + Vh·z) y z ← (1 − t)·z + t·tanh(·). Es la actualización de una GRU sin compuerta de reset (Cho et al., EMNLP 2014, ecuaciones 6 y 7). En DualBrain, la LiquidRealCell suma además LayerNorm.
- **[LITERATURA] Lo de poner neuronas líquidas sobre cableado biológico tampoco es nuevo:**
  - las NCP de Lechner et al. (Nat Mach Intell 2:642–652, 2020) ponen neuronas LTC sobre un cableado inspirado en C. elegans (19 neuronas de control, 253 sinapsis);
  - Lappalainen et al. (Nature 2024, doi 10.1038/s41586-024-07939-3) entrenan τ y potencial de reposo por tipo sobre el cableado real del ojo de la mosca (45.669 neuronas, 1.513.231 conexiones, 734 parámetros).
- **[MEDIDO] Las neuronas del modelo nunca fueron las de la mosca.** La mosca pone el cableado: quién conecta con quién, el signo, la cantidad de sinapsis y el tipo. La neurona es genérica (tasa, líquida o LIF).
  - Lo más parecido a una neurona de mosca fue el LIF con los parámetros de Shiu 2024, y tal como lo armamos **DAÑA** (factorial 1, 2026-10-13-002).
  - Sin entrenar, la líquida nativa **empata** con la de tasa en R1.
  - Entrenada, la plena le gana a su control con los mismos parámetros: 0,9826 contra 0,9214, 4/4, p 1,3e-59 (013). Fue en un motivo, en una tarea y en simulación.
- **[CONCLUSIÓN] Lo propio y defendible es una combinación, no una neurona:**
  1. dinámica líquida sobre el cableado **exacto** de FlyWire, no inspirado;
  2. un **banco sellado** que la falsa: nulos SL y T, la regla de diseño como rival, ancla de reproducción y réplica en Actions;
  3. el resultado medido de que la líquida entrenada paga por ser líquida en el reflejo de escape.

  La novedad de la combinación no está verificada con un barrido de literatura.
- **[MEDIDO] El laboratorio sólo corrió con FlyWire v783.** El código lee las columnas de FlyWire (`Presynaptic_ID`, `Postsynaptic_ID`, `Connectivity`, `Excitatory`; `cell_type`, `side`). Correrlo sobre otros conectomas (MANC, BANC, hemibrain, C. elegans) está NO MEDIDO y pide un adaptador.
- **[MEDIDO] Papers: son dos, en estados distintos.**
  - **Paper 1** (conectoma): v1.0 en Zenodo (20-mar). La v2.0 está en el PR #27 sin depositar, con F01, F06 y F07 abiertos.
  - **Paper de DualBrain** (feb 2026, `dualbrain/docs/01-paper-dualbrain.md`). Su aporte es la compuerta vectorial entre la vía reactiva y la de memoria (17× contra la misma arquitectura sin compuerta), no la célula. Su README marca que faltan `dbc3_motor.h` y el script del benchmark DBC3-v3. Su depósito con DOI está NO VERIFICADO.
- **[CONCLUSIÓN] "Miles de aplicaciones" no se sostiene.** Las aplicaciones medidas fuera de simulación hoy son **cero**. Las que tienen evidencia son un puñado:
  1. **El banco** como herramienta para que otros prueben hipótesis sobre conectomas. Es lo más maduro, y sólo con FlyWire.
  2. **Reflejos de pocos KB** sacados de FlyWire (escape, aterrizaje) para robots chicos. Funcionan en simulación; el costo en ESP32 y en hardware real está NO MEDIDO. El `swarm/` tiene dos desbordes int32 y un test que no puede dar rojo (auditoría de Tao, 2026-10-13-001).
  3. **DualBrain/DBC3** como memoria compacta para edge, con benchmarks propios y reproducción incompleta.
  4. **El Paper 1** como análisis citable de la estructura de FlyWire.

## Pedido

"En pocas palabras, creamos una nueva neurona, es decir, ¿podríamos posicionarla como nueva o generar ese elemento? Hicimos un artilugio con las bases que teníamos para luego acomodarnos a las neuronas propias de la mosca. Aparte, el laboratorio para trabajar con nuevos conectomas. Y las miles de aplicaciones que se derivan de los dos papers y de lo anteriormente nombrado." (13-oct, 09:14)

## Herramientas y máquina

- **brain-env** (gateway MUDH, `run`):
  - clon de main en `9bcb2bb` y lectura del CONTEXTO (md5 `6bc1a251…`, 402 líneas);
  - prueba del parche del CONTEXTO sobre una copia;
  - el clon de `dualbrain` falló: es privado y no hay credenciales en brain-env.
- **GitHub MCP:** lectura de `dualbrain` (`README.md` y `docs/01-paper-dualbrain.md`, en `52667ad`) y del workflow de parche de la 003 (`c1482a0`). Escritura: este commit en main.
- **Web:** cuatro búsquedas (LTC, NCP, Lappalainen 2024 y GRU), sin cuota ajena.
- **Actions:** el workflow de este commit aplica el parche del CONTEXTO y se retira. El factorial 2 no se disparó.

## Qué se midió

| Afirmación | Fuente | Dato |
|---|---|---|
| La líquida nativa es de la familia LTC | Hasani et al. 2021 (AAAI 35(9); arXiv 2006.04439) | τ_sys = τ / (1 + τ·f(x, I, t, θ)) |
| La que ganó es una GRU sin reset | Cho et al. 2014 (EMNLP), ec. 6 y 7; la forma de la 012 a la 015 según el CONTEXTO (línea 234) | z_j = σ(·); h = z·h_prev + (1 − z)·h̃ |
| LiquidRealCell de DualBrain | `dualbrain/docs/01-paper-dualbrain.md` | τ = σ(W_τ·c + b_τ); h' = LayerNorm(h⊙(1 − τ) + tanh(W_flow·c)⊙τ) |
| LTC sobre cableado biológico ya existe | Lechner et al. 2020 (Nat Mach Intell 2:642–652) | 19 neuronas de control, 253 sinapsis, cableado inspirado en C. elegans |
| Cableado real de la mosca con τ entrenada ya existe | Lappalainen et al. 2024 (Nature) | 45.669 neuronas, 1.513.231 conexiones, 734 parámetros libres |
| La líquida plena entrenada paga | CONTEXTO, líneas 217 y 222 (013 y 014) | 0,9826 contra 0,9214, 252 contra 12, p 1,3e-59, 4/4; P3: 0,9854 contra 0,9453 |
| La nativa sin entrenar empata | Factorial 1 (2026-10-13-002) | LIQ_R1 EMPATE; LIQ_M46 MIXTO |
| El LIF tipo Shiu daña | Factorial 1 | LIF_M46 y LIF_R1 DAÑA |
| El banco sólo leyó FlyWire | `tools/factorial2/factorial2_mosca.py` y `tarea_mosca.py` | columnas fijas de FlyWire v783 y anotaciones `17fc577` |
| Estado de los papers | CONTEXTO, línea 5; README de `dualbrain` | Zenodo sólo v1.0; v2.0 en el PR #27; DualBrain sin `dbc3_motor.h` ni el script DBC3-v3 |

## Evidencia cruda

```
# brain-env, clon de main
9bcb2bb respuesta(2026-10-13-004): factorial 2 sellado (9442fdf) sin disparar ...
6bc1a251853f92ed4cc5326cef22dc8f  docs/agents/CONTEXTO-drosophila-fep.md   (402 líneas)
5: **Base vigente del paper:** ... **Zenodo tiene sólo la v1.0** (20-mar).
234: - **La líquida que ganó (012 a 015) tiene la forma de la LiquidCell de DualBrain** (t = sigmoid(b + Vx·x + Vh·z)) aplicada a cada neurona; la nativa de SparseLTC es τ_ef = τ / (1 + tau_gain·|drive|) y no se probó.
217: - **Plena (1.378):** líquida 0,9826 contra no líquida 0,9214; 252 contra 12 (p 1,3e-59), 4/4: **la líquida MEJOR.**
# git clone dualbrain (brain-env)
fatal: could not read Username for 'https://github.com': No such device or address
# GitHub MCP, dualbrain@52667ad
README.md: "❌ Falta `dbc3_motor.h` (los bloques/swarm lo incluyen; sin él no compila)." / "❌ Falta el script Python que produjo el benchmark DBC3-v3"
docs/01-paper-dualbrain.md: "*DualBrain: Vectorial Gating for Efficient Memory-Reactive Computation in Compact Neural Architectures*"
docs/01-paper-dualbrain.md: "`c=[x;h]` · `τ=σ(W_τ·c+b_τ)` (b_τ=-2.0) · `h' = LayerNorm(h⊙(1-τ) + tanh(W_flow·c)⊙τ)`"
# web
AAAI 2021 (Hasani, Lechner, Amini, Rus, Grosu): "input-dependent varying time-constant (τsys = τ / (1+τ f(x(t),I(t),t,θ)))"
Nat Mach Intell 2020 (Lechner et al.): "19 control neurons, connecting 32 encapsulated input features to outputs by 253 synapses" / "The network structure of NCPs is inspired by the wiring diagram of the C. elegans nematode"
Nature 2024 (Lappalainen et al.): "the connectome-constrained model comprises 45,669 neurons and 1,513,231 connections" / "The only free parameters in our model are the single-neuron time constants and resting membrane potentials"
EMNLP 2014 (Cho et al.): "zj = σ([Wz x]j + [Uz h<t−1>]j)" (6); "hj<t> = zj hj<t−1> + (1 − zj) h̃j<t>" (7)
# prueba del parche del CONTEXTO sobre una copia (brain-env)
152d74aa4920d3e3ae4518fbcd00cd9f  parche.py
md5 antes 6bc1a251853f92ed4cc5326cef22dc8f
ANCLA apariciones=1 :: **Última actualización:** 2026-10-13, 08:30 (America/Buenos_
ANCLA apariciones=1 :: ## Madrugada y mañana del 13-oct (019 a 2026-10-13-003) · ma
ANCLA apariciones=1 :: - **Espera decisión de Abraham:** sellar el factorial 2 (la
md5 despues 13e8469b9fc233addba9c093913a5fd4
PARCHE OK   (422 líneas)
```

## Archivos

- `docs/agents/respuestas/2026-10-13-005-no-hay-neurona-nueva-lo-propio-es-la-dinamica-liquida-sobre-el-cableado-exacto-y-el-banco.md` (este archivo).
- `tools/contexto/actualizar_contexto_2026-10-13-005.py`, md5 `152d74aa…`. Suma la 004 y la 005 al CONTEXTO y cambia "sellar el factorial 2" por "correr el factorial 2".
- `.github/workflows/contexto-2026-10-13-005.yml`: aplica el parche en Actions y se retira. Debe dejar el CONTEXTO en md5 `13e8469b…`.

## NO MEDIDO

- **Un barrido sistemático de literatura** sobre "dinámica líquida en cableado exacto de un conectoma". Que la combinación sea nueva es una conclusión sin verificar.
- **El banco sobre cualquier conectoma que no sea FlyWire v783.**
- **El costo en microcontrolador y cualquier prueba en hardware.**
- **El depósito del paper de DualBrain** (si tiene DOI), y la reproducción de su benchmark DBC3-v3.
- **Si una célula propia podría ser nueva** con un cambio de forma (por ejemplo, τ ligada a la sinapsis y no a la neurona). No se diseñó ni se midió.

## Antes de firmar

| Afirmación | Instrumento | ¿Podía dar rojo? |
|---|---|---|
| La líquida nativa es LTC | Fórmula del paper de Hasani contra la de `connectome_ltc.hpp` (vía el CONTEXTO) | Sí: si τ no dependiera de la entrada, no sería LTC |
| La que ganó es una GRU sin reset | Ecuaciones 6 y 7 de Cho contra la forma del CONTEXTO | Sí: con otra regla de mezcla no coincidiría |
| No hay neuronas de mosca en el modelo | Lectura del instrumento: tasa, líquida y LIF genéricos | Sí: si alguna célula tuviera parámetros por tipo medidos en la mosca, sería falso |
| El banco sólo corrió con FlyWire | Columnas leídas y pins de md5 | Sí: un log con otro conectoma lo refutaría; no hay ninguno |
| Cero aplicaciones fuera de simulación | CONTEXTO y respuestas | Sí: una prueba en hardware lo refutaría; no hay ninguna |

```
--- METODO PROMETEO ---
Accion delicada: no (documentacion; el workflow solo edita el CONTEXTO y se retira)
Maquina: brain-env (lectura del CONTEXTO y prueba del parche) | GitHub MCP (lectura de dualbrain) | web (literatura) | Actions x64 (aplica el parche)
Artefactos: docs/agents/respuestas/2026-10-13-005-no-hay-neurona-nueva-lo-propio-es-la-dinamica-liquida-sobre-el-cableado-exacto-y-el-banco.md + Doc de ClickUp 2026-10-13-005
```
