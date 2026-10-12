# 2026-10-12-001 · La arquitectura por etapas tiene sentido: SparseLTC para los circuitos cableados, DBC3 para memoria y contexto, lo clásico para carga y motores; no todo el cerebro de la mosca es reutilizable

**Fecha:** 2026-10-12, madrugada (America/Buenos_Aires).
**Base:** `drosophila-fep-connectome` main en `8467aef` (016); `mojo-absoluto` main en `613bf49` (leído en la 016); `dualbrain` main (README).
**Tipo:** respuesta de diseño. **Sin corrida nueva.** Lo medido que se usa viene de la 007 a la 016 y de `mojo-absoluto`; todo lo demás es diseño u opinión y está marcado así.
**Doc de ClickUp (público):** https://app.clickup.com/90171457413/docs/2kza6fw5-21297

## Veredicto

**Sí a la arquitectura por etapas, con una regla para repartir las piezas:**

- **SparseLTC** va donde hay cableado de la mosca que certificar: los circuitos sensoriales y los reflejos.
- **DBC3** va donde hay que recordar o cambiar de contexto con poco presupuesto, una por flujo y nunca una por neurona.
- **El patrón DualBrain** (vía rápida, memoria y compuerta) es el esqueleto que une las dos.
- **Lo clásico y determinista** va donde manda la seguridad: carga de batería, drivers de motor (ESC) y lazo de actitud.

**Regla de reparto, en una línea:** el cableado de la mosca entra donde gana en su función contra su barajado (S y SL) y contra un rival clásico entrenado. Donde no gana, va lo clásico.

**Lo que no comparto:** «todas las capacidades del cerebro de la mosca son reutilizables». Es una hipótesis que hay que probar circuito por circuito, y ya hay un contraejemplo medido: en tareas genéricas el cableado de la mosca empata 4/4 con su barajado de igual grado (008). Y en el único circuito que sí paga en su función, el reflejo escrito a mano rinde 0,9167 sin entrenar (011) y la ventaja contra SL es de grupo (88%), no de cada entrenamiento (015).

**Antidrones como detección y evasión: sí. Antimisiles: mi recomendación es sacarlo del roadmap.**

## 1. Pedido

Verbatim:

> LA VERDADERA ARQUITECTURA ESTARA DADA POR SPARSELTC EN ALGUNAS PARTES DUAL BRAIN EN OTRA Y DBC3 EN OTRA, YA QUE ESTAN DIEÑADAS PARA DISTINTAS PARTES Y SON FUNCIONALES A DIFERENTES ETAPS, DESDE TOMAR LA SEÑAL DESDE UN TRANDUCTORO SER EL TRANSUDCTOR, POR EJEMPLO CAMARAS , SENSORES CIENTOS, CONTROL, CARGA DE BATERIA, ACTUADORES. ETC. Y OBVIO QUE HAY QUE ESTUDIAR Y COMPLETAR CADA UNO DE LOS CIRCUITOS, GIRAR, ATERRIZAR, OLER, ETC. TODOS LOS QUE SE PUEDAN TOMAR DEL CEREBRO Y TRAPOLAR A UN DRONE , QUE YA NO SERIA UN DRONE SERIA UN ROBOT AUTINOMO AEREO, MARITIMO O TERRESTRE Y PORQ NO APLICARLO EN SISTEMA CONTRA DRONES O ANTIMISILES. CREO QUE TODAS LAS CPACIDADES DEL CEREBRO DE LA MOSCA SON REUTILIZABLES

Resumen sin interpretar: la arquitectura real repartiría SparseLTC, DualBrain y DBC3 por etapas, desde el transductor (o siendo el transductor) hasta control, carga de batería y actuadores; hay que estudiar y completar cada circuito (girar, aterrizar, oler) para un robot autónomo aéreo, marítimo o terrestre; pregunta por qué no aplicarlo contra drones o misiles; y afirma que todas las capacidades del cerebro de la mosca son reutilizables.

## 2. Herramientas y máquina

- **Ninguna corrida.** brain-env, Actions y Kaggle sin uso en este turno; no se gastó cuota ajena.
- **GitHub MCP, lectura:** en este repo, `docs/agents/CONTEXTO-drosophila-fep.md` en `8467aef` y la respuesta 007 (para verificar el dato del dron, `t_hasta_30grados_s=0.267`); en `dualbrain`, `README.md` de `main`. Reusadas de la 016 sin releer: en `mojo-absoluto` `613bf49`, `include/mojo_abs/connectome_ltc.hpp`, `include/mojo_abs/sparse_ltc_projector.hpp` y `docs/adr/2026-10-01-sparseltc-dbc3-adapter.md`.
- **ClickUp, lectura:** el Doc del 3-oct «Mojo Absoluto Compiler: DualBrain/DBC3, SparseLTC e hipótesis de desarrollo» (https://app.clickup.com/90171457413/docs/2kza6fw5-19197/2kza6fw5-21757) y búsqueda en el índice del workspace.
- **Escrituras:** un Doc público nuevo en ClickUp (https://app.clickup.com/90171457413/docs/2kza6fw5-21297); este archivo y el CONTEXTO en `main`, en un commit. No toqué ramas, PRs ni código.

## 3. Respuesta (qué se midió: nada nuevo)

### 3.1 Las etapas y qué pieza va en cada una

| Etapa | Qué hace | Pieza | Qué hay medido |
|---|---|---|---|
| E0 · Transducción | cámara, IMU, micrófono, sensor de gas; o «ser el transductor», imitando a los fotorreceptores | sensores comerciales; más adelante, una cámara de eventos alimentando un modelo de la retina | nada |
| E1 · Rasgos sensoriales | movimiento, expansión, flujo óptico, objetos chicos | **SparseLTC** sobre subcircuitos ópticos de FlyWire (lo que FlyVis validó con 734 parámetros) | FlyVis, externo; en nuestro escape la entrada visual es un modelo de literatura, no un circuito |
| E2 · Reflejos (motivos) | escapar, girar, aterrizar, frenar | **SparseLTC** con el cableado real y la τ entrenada | **escape: sí**, en simulación (010 a 015) |
| E3 · Contexto y memoria | recordar, cambiar de modo, decidir a qué reflejo hacerle caso | **DBC3**, una por flujo, nunca una por neurona (ADR, D1) | DBC3 gana en memoria diferida y cambio de contexto y pierde en selección temporal (Doc del 3-oct); nunca se conectó a un motivo |
| E4 · Interfaz motora | de las descendentes a órdenes: escapar, girar, avanzar | tabla descendente → orden | nada |
| E5 · Control de bajo nivel | actitud y estabilización (lo que en la mosca hace el haltere) | lazo clásico o CPG: el «cordón sintético» | sin él, el dron de `swarm/` pasa los 30° en 0,267 s (007) |
| E6 · Energía y actuadores | carga de batería, ESC, motores | **clásico y determinista**; el cerebro sólo decide cuándo volver a cargar, como el hambre en la mosca: una señal que entra a la compuerta de DBC3 | nada |

**Dónde entra DualBrain:** no como una etapa más, sino como el patrón que une E2 y E3: la vía rápida (el motivo en SparseLTC), la memoria (DBC3) y la compuerta que decide cuál manda. Es lo que diseña el ADR del 1-oct (SparseLTC → proyección a features → un DBC3 por flujo) y lo que la 016 dejó sin correr.

### 3.2 «Todas las capacidades son reutilizables»: hipótesis, no hecho

- **Contraejemplo medido (008):** en tareas genéricas, el cableado de la mosca y su barajado de igual grado empatan 4/4 en el reservorio recurrente de SparseLTC; paga la sparsity, no la mosca.
- **Donde sí paga, paga en su función (010 a 015)**, y con matices: por lateralidad sin entrenar (010), por cableado fino fuera del techo (011), y con la líquida plena entrenada en promedio contra SL (88%, Mann-Whitney p 0,0002) pero no en cada entrenamiento (015).
- **El rival a mano ya existe:** el reflejo escrito a mano sin LC6 rinde 0,9167 sin entrenar (011).
- **Consecuencia:** cada circuito entra al robot sólo después de pasar su falsador. «Reutilizable» se gana, no se supone.

### 3.3 El catálogo de circuitos a compilar

Candidatas de literatura, **todas a verificar en FlyWire antes de usarlas:**

| Circuito | Neuronas candidatas | Fuente | Para qué robot |
|---|---|---|---|
| Escape | LC4, LPLC2 → fibra gigante (DNp01) | medido acá (010 a 015; ficha GF-01) | aéreo, terrestre |
| Giro | DNa01, DNa02 | Yang 2024, citado por Eon (verificado en la 007) | todos |
| Avanzar caminando | oDN1 | Sapkal 2024, citado por Eon (007) | terrestre |
| Retroceder caminando | MDN | Bidaye 2014 (007) | terrestre |
| Rumbo (brújula interna) | anillo E-PG del complejo central | literatura, sin cita verificada en este turno | todos |
| Estabilizar con flujo óptico | células HS y VS de la placa lobular | literatura, sin cita verificada en este turno | aéreo |
| Detectar y seguir objetos chicos | LC11, LC10 | literatura, sin cita verificada en este turno | aéreo (detección de otros drones) |
| Olfato | lóbulo antenal → cuerno lateral (innato) y cuerpo fungiforme (aprendido) | literatura, sin cita verificada en este turno | terrestre, con sensores de gas |
| Aterrizaje | descendentes de aterrizaje descritas en la literatura; a identificar | sin cita en este turno | aéreo |

**Ojo con el cuerpo:** FlyWire es sólo el cerebro. El vuelo, las patas y el haltere viven en el cordón nervioso ventral, que está en otros conectomas (MANC, BANC). Y cada circuito necesita su propio falsador: el brazo S y SL en su función, y un rival clásico entrenado.

### 3.4 Aéreo, marítimo y terrestre

Lo visual de movimiento relativo (algo que se acerca, flujo óptico, objetos chicos) se traslada a cualquier plataforma. Lo motor depende del cuerpo: los circuitos de vuelo no sirven en un barco, y los de caminar sirven en un robot con patas, no en uno con ruedas. **El agua es mala para el flujo óptico:** tiene pocas texturas fijas.

### 3.5 Antidrones y antimisiles

- **Antidrones como detección y evasión: tiene sentido.** La mosca detecta lo que se le viene encima (LC4, LPLC2) y objetos chicos que se mueven (LC11).
- **Interceptar es otro comportamiento:** perseguir. La Drosophila es buena escapando, no cazando; las cazadoras (libélulas, moscas asesinas) no están en FlyWire.
- **Antimisiles, mi opinión: sacarlo del roadmap.** Otras velocidades, distancias y sensores (radar, infrarrojo) y otras leyes de guiado; lo que aporta la mosca ahí es poco, y es terreno de uso dual con control de exportaciones, que cierra puertas comerciales y de publicación.

### 3.6 Qué sigue (orden propuesto; decide Abraham)

1. **Catálogo de circuitos en FlyWire:** con las anotaciones pinneadas (`17fc577`), buscar cada circuito de la tabla y medir tamaño, cables y lateralidad, igual que con el escape.
2. **La líquida nativa de SparseLTC** (τ / (1 + tau_gain·|drive|)) en el escape contra su control (pendiente de la 016).
3. **El primer acople SparseLTC → DBC3** sobre el escape: las 26 como reflejo y DBC3 decidiendo cuándo hacerle caso. Para el target en C falta `dbc3_motor.h` en `dualbrain`.
4. **Un rival clásico entrenado** en el escape, para saber si la mosca le gana a la ingeniería y no sólo a su barajado.

## 4. Evidencia cruda (verbatim)

Citas textuales de las fuentes:

- Doc del 3-oct (https://app.clickup.com/90171457413/docs/2kza6fw5-19197/2kza6fw5-21757): «SparseLTC aporta estructura, dinámica y priors medidos. DBC3 aporta memoria, compuerta y readout compacto. Se mantienen como capas distintas.»
- Mismo Doc: «DBC3 tiene ventaja selectiva en memoria diferida y cambio de contexto, no superioridad universal.»
- ADR `docs/adr/2026-10-01-sparseltc-dbc3-adapter.md` de `mojo-absoluto` (`613bf49`, estado «Propuesto»): «D1. DBC3 es readout/controlador, no célula por neurona» y «Todavía no existe una corrida SparseLTC → DBC3 real».
- `README.md` de `dualbrain` (`main`): «❌ Falta `dbc3_motor.h` (los bloques/swarm lo incluyen; sin él no compila).»
- Respuesta 007, línea del log `results/swarm_lazo_cerrado_2026-10-11/run.log` (rama `titan/swarm-lazo-cerrado-2026-10-11`, md5 `b109936678e1fee1c85af5574b9acbd7`), leída hoy:

```text
REPOSO lectura=ORIGINAL sin_amenaza rumbo=0 deriva_a_0.15s_x_m=-0.000408 y_m=+0.000029 inclinacion_a_0.15s_grados=3.64 t_hasta_30grados_s=0.267
```

Números transcriptos, no textuales, del Doc del 3-oct: DelayedClass 100% contra 18,1% de LSTM; ContextSwitch 55,6% contra 43,2%; TemporalSelect 8,7 contra 16,4 de LSTM (DBC3 pierde); XORMemory cerca del azar; la compuerta escalar empata o le gana a menudo a la vectorial. Del README de `dualbrain`: DBC3-v3 con 6.888 parámetros, 5/5 contra LSTM.

Números del escape, transcriptos de los archivos de respuesta ya commiteados en `main` (cada uno trae sus líneas crudas y su md5; los instrumentos están en la rama `titan/escape-motivo-2026-10-11`):

- 008: RW contra RS empate 4/4; LW contra LS empate 4/4.
- 011: W 0,8177 contra SL 0,6819 (6/200, p = 0,0348); reflejo a mano C+L 0,9167.
- 014: líquida plena 0,9854 contra no líquida 0,9453; 169 contra 15, 4/4.
- 015 (run.log md5 `48b74e4c569d351fafda72667e5dcced`, 77 líneas, en `cc531e7`): VEREDICTO_FIRMA = SOLO LA SEMILLA 0; Mann-Whitney 8 W contra 69 SL, U 488 de 552 (88%), p 0,0002.

Recomputable: cada número de la 008 a la 015 se recalcula con el script y el comando de su archivo de respuesta. Esta respuesta no agrega ninguno.

## 5. Archivos generados

- `docs/agents/respuestas/2026-10-12-001-arquitectura-por-etapas.md` (este).
- `docs/agents/CONTEXTO-drosophila-fep.md`: encabezado, bullet «Arquitectura por etapas» en Robótica, «Espera decisión», Próximos pasos 7, Fuentes, NO MEDIDO y bloque de método.
- Doc de ClickUp público: https://app.clickup.com/90171457413/docs/2kza6fw5-21297
- Sin código ni resultados nuevos.

## 6. NO MEDIDO

- **Toda la arquitectura por etapas** salvo E2, y E2 sólo con un circuito (el escape, 26 neuronas) y en simulación.
- E0 (cámara de eventos, modelo de retina, «ser el transductor»), E1 con nuestro motor sobre FlyWire (FlyVis es externo), E4 (tabla descendente → orden), E5 (cordón sintético) y E6 (energía y actuadores).
- **DBC3 conectado a un motivo;** DBC3 en C sobre un microcontrolador (sin `dbc3_motor.h` no compila).
- **Los circuitos del catálogo:** ninguno buscado en FlyWire en este turno. Las candidatas de giro y marcha vienen de la búsqueda de la 007; las de rumbo, flujo, objetos chicos, olfato y aterrizaje salen de literatura sin cita verificada hoy.
- **El cordón nervioso** (MANC, BANC): no abierto.
- **Transferencia a marítimo y terrestre;** cualquier medición de antidrones; cualquier hardware.
- **«Todas las capacidades son reutilizables»:** sin medir, salvo un contraejemplo (008) y un circuito que paga en su función (010 a 015).
- **Review externo.** Silencio no es aprobación.

## Antes de firmar

```text
"sí a la arquitectura por etapas"        → ninguno (diseño)                    → NO MEDIDO
"no todo es reutilizable"                → brazo S en tareas genéricas (008)   → podía dar rojo: SÍ → medido: empate 4/4
"el escape paga en su función"           → S y SL en lazo cerrado (010 a 015)  → podía dar rojo: SÍ → medido, con matiz (grupo 88%; la peor semilla no gana)
"DBC3 sirve para memoria y contexto"     → benchmarks del Doc del 3-oct        → podía dar rojo: SÍ (pierde en TemporalSelect) → medido allá, no re-medido acá
"sin lazo de actitud el dron se voltea"  → arnés de la 007, reposo             → podía dar rojo: SÍ → medido (simulación)
"el catálogo sirve"                      → ninguno                             → NO MEDIDO
"antimisiles fuera del roadmap"          → ninguno                             → opinión, no medición
```

## QA (TITAN FULL)

Rúbrica N/A: respuesta de diseño sin ejecución. Control de salida: cada afirmación está marcada como medida (con su archivo), diseño u opinión; las fuentes de fuera de este repo están citadas textuales o marcadas como transcriptas; el dato del dron se verificó contra el log de la 007 en este turno. Deuda: review externo y verificación del catálogo en FlyWire.

--- METODO PROMETEO ---
Acción delicada: NO (bitácora y contexto a main)
Modo aplicado:   TITAN FULL (diseño, sin corrida nueva)
Rúbrica:         N/A (diseño sin ejecución)
Review externo:  no pedido (deuda)
Instrumento:     ninguno nuevo; lecturas por GitHub (CONTEXTO en 8467aef, respuesta 007 con la línea REPOSO de su log, README de dualbrain) y de ClickUp (Doc del 3-oct)
Máquina:         ninguna corrida (diseño; lecturas en GitHub y ClickUp)
Artefactos:      docs/agents/respuestas/2026-10-12-001-arquitectura-por-etapas.md + https://app.clickup.com/90171457413/docs/2kza6fw5-21297
