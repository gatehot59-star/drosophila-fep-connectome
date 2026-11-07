# 2026-11-07-001 · El nulo de 1.000 recableados de G1-A casi no ocupa memoria: los 1.000 no suben el proceso y cada vuelta usa unos 2 MiB · lo que pesa es cargar la mosca una vez (0,7 GiB FlyWire, 1,4 GiB BANC)

**Veredicto del pedido:** el nulo de 1.000 recableados necesita, por sí solo, unos **2 MiB** de trabajo por vuelta en FlyWire y **1 MiB** en BANC cerebro, y las 1.000 vueltas seguidas no suben la memoria del proceso ni 0,1 MiB. Lo que pide memoria es armar las tablas una vez por mosca: el proceso llega a **705 MiB** en FlyWire y a **1.369 MiB** en BANC. Con **1,5 GiB por mosca**, cada una en su proceso, alcanza, incluso para el secundario más grande (1.451 MiB). Hoy entra en brain-env (4.151 MiB disponibles al empezar) y sobra en Actions (16 GB según el inventario de agosto, no re-medido).

Doc: [2026-11-07-001 · El nulo de G1-A casi no ocupa memoria](https://app.clickup.com/90171457413/docs/2kza6fw5-26157/2kza6fw5-30757)

## En criollo

El nulo no guarda 1.000 cerebros. Recablea una tabla chica (996 conexiones visual→descendente en FlyWire, 753 en BANC), recalcula quién compite con quién y vuelve a estimar un número. Se hace de a una vuelta y se tira, así que la memoria no crece con la cantidad. Lo caro es leer la mosca entera para armar esa tabla, y eso pasa una sola vez.

## Cálculo y medición

| | FlyWire 783, pesadas | BANC 888 cerebro, pesadas | BANC entero, livianas (peor caso) |
|---|---|---|---|
| pares x, D′ · X · aristas S→D | 111.751 · 121 · 996 | 61.149 · 68 · 753 | 1.812.760 · 2.017 · 753 |
| pico del proceso (cargar la mosca y armar tablas) | 704,8 MiB | 1.368,9 MiB | 1.451,4 MiB |
| proceso antes del nulo | 289,7 MiB | 1.151,8 MiB | 1.246,3 MiB |
| proceso después de 1.000 recableados | 289,7 MiB | 1.151,8 MiB | 1.246,3 MiB |
| trabajo de una vuelta (pico de tracemalloc en 50 vueltas) | 1,94 MiB | 0,99 MiB | 21,4 MiB |
| ajuste de G0, una sola vez | +7,3 MiB | +5,2 MiB | +31,4 MiB |
| tiempo de las 1.000 vueltas en brain-env | 20,2 s | 16,5 s | 38,7 s |
| resultado: 1.000 valores de β̃ | 8 KB | 8 KB | 8 KB |
| si además se guardan las 1.000 tablas (int16, calculado) | 4,0 MB | 3,0 MB | 3,0 MB |

**El cálculo cuadra con lo medido.** En FlyWire cada vuelta toca los pares con información (97.144 con esta Y sintética): la matriz de competidores por driver (121 × 925 en float64, 0,9 MB), los valores de esa matriz en los pares (0,8 MB) y el vector M (0,1 MB), unos 2 MB; tracemalloc dio 1,94 MiB. En el peor caso la matriz es 2.017 × 901 (14,5 MB) y los pares con información son 778.231 (6,2 MB); tracemalloc dio 21,4 MiB.

**Por qué BANC pesa más:** después de liberar la mosca, el proceso de BANC sigue con 1,15 GiB tomados. Es memoria que el asignador no devuelve después de la carga, no del nulo. Correr el nulo en un proceso aparte, con las tablas ya armadas, debería bajarlo a lo que ocupan Python y sus bibliotecas al arrancar (unos 125 MiB), pero eso no lo corrí.

**Brain-env:** hoy hay margen. En agosto el inventario medía 1,7 GB libres; con eso BANC entraba justo.

**Comparación:** H_REUSO_CIERRE recableaba la red entera y usó 2,9 GiB en Actions. El nulo de G1-A recablea sólo la tabla S→D; por eso cada vuelta usa megas y no la red.

## Lo que adelanta de paso (no es la calibración)

Con la Y sintética, el nulo de β̃ tiene un ancho (desvío) de 0,11 en FlyWire y 0,20 en BANC cerebro, y no queda centrado en cero: −0,06 y −0,12. Un OR de 1,5 es β = 0,41, unos 3,5 anchos en FlyWire y unos 2 en BANC cerebro. Adelanta dos cosas para la calibración: BANC cerebro va a quedar justo de potencia, y el sesgo de β̃ hay que medirlo, porque el criterio pide menos de 0,1 y acá, con otra Y sintética, BANC dio −0,12. El p no se ve afectado por un corrimiento parejo, porque sale del propio nulo.

## 1. Pedido

«Calculá cuánta memoria necesitará el nulo de 1.000 recableados» (Abraham, 7-nov-2026). Es el nulo de H_G1_VETO en la 2026-11-04-001: 1.000 recableados por mosca de la tabla S→D cableada, conservando grados dentro de cada lado, recalculando M y re-estimando β̃.

## 2. Herramientas

- brain-env por el gateway: lectura de 00-ENTORNOS-Y-CAPACIDADES.md desde raw; sonda g1_memoria_nulo.py lanzada por correr_sondas.py en segundo plano, tres configuraciones, cada una en su proceso. Escribió sólo en /workspace/a1/v2/g1/mem/.
- GitHub MCP: este commit. ClickUp: la página nueva del Doc.
- Sin Actions, sin GPU, sin tocar trabajo ajeno.

## 3. Qué se midió

| # | Afirmación | Instrumento | ¿Podía dar rojo? | Veredicto |
|---|---|---|---|---|
| 1 | Las 1.000 vueltas no suben la memoria | VmRSS en las vueltas 1, 10, 100, 200 y así hasta 1.000 | sí, si creciera | PASS: igual en las 12 muestras, en las tres configuraciones |
| 2 | Una vuelta usa unos 2 MiB | pico de tracemalloc en 50 vueltas | sí | medido: 1,94; 0,99 y 21,4 MiB, sólo lo que pasa por Python y numpy |
| 3 | El pico lo pone la carga | VmHWM por etapa | sí | medido: 704,8; 1.368,9 y 1.451,4 MiB |
| 4 | Los recableados conservan los grados | grados de cada S y cada D comparados en cada vuelta | sí | PASS: 1.000 de 1.000 en las tres |
| 5 | Las tablas son las del censo | X, pares, Y = 1, L = 1 y aristas S→D contra g1_censo.json | sí | PASS: 5 de 5 en las tres |
| 6 | Las entradas son las fijadas | md5 de las cuatro | sí | PASS: iguales a la 2026-11-04-001 |
| 7 | La sonda no cruza Y con M reales | lectura del código: M sólo sale de tablas recableadas y la Y real se borra antes del nulo | el código, sí; lo que yo haya hecho fuera de él, no | DECLARADO |
| 8 | Entra en brain-env | MemAvailable al empezar | sí | medido hoy: 4.151 MiB contra 1.451 de pico |
| 9 | Entra en Actions | inventario del 26-ago | no, no se re-midió | NO MEDIDO hoy; el inventario dice 16 GB |

## 4. Evidencia cruda

En docs/agents/evidencia/2026-11-07-001-memoria-nulo/, verbatim: g1_memoria_nulo.py, correr_sondas.py, corrida.log, los tres mem_*.log y los tres mem_*.json. corrida.log entero:

```plain
flywire entero pesado 1000 50 20261107 rc=0 44.0 s
banc cerebro pesado 1000 50 20261107 rc=0 42.5 s
banc entero liviano 1000 50 20261107 rc=0 79.5 s
TERMINADO
```

Memoria de brain-env al empezar (2026-11-07T19:15:32Z, host 6c09d8604b07, 2 CPU): MemTotal 7.802 MiB, MemAvailable 4.151 MiB, swap 20.480 MiB con 15.228 libres. Fila RAM del inventario, medida el 2026-08-26: «8 GB (~1,7 GB disponible) | 16 GB (14,9 libres) | 16 GB (15,2 libres) | 13-16 GB».

## 5. Archivos

- Este archivo.
- docs/agents/evidencia/2026-11-07-001-memoria-nulo/: los nueve archivos de la sección 4.

## 6. NO MEDIDO

- Un proceso que haga sólo el nulo, con las tablas ya armadas.
- Actions: memoria y velocidad salen del inventario de agosto, no de esta sonda.
- Lo que una vuelta reserve fuera de Python y numpy: tracemalloc no lo ve; VmRSS sí, y no se movió.
- El bootstrap de 2.000 remuestreos y la calibración.
- El nulo real: la sonda usa Y sintética, y el instrumento sellado todavía no existe.

## Estado vigente que CONTEXTO todavía no refleja

Suma a la 2026-11-04-001: el nulo de G1-A entra en brain-env, así que la memoria no decide la máquina. Siguen pendientes el instrumento, la calibración, el sello y la corrida.

```plain
--- METODO PROMETEO ---
Accion delicada: NO (sonda de medicion; evidencia append-only)
Modo aplicado:   LIGERO (pregunta tecnica, recibo corto)
Maquina:         brain-env (host 6c09d8604b07, Python 3.12.14, NumPy 2.5.3, SciPy 1.18.1, pandas 3.0.5, pyarrow 25.0.1)
Rubrica:         no aplica (entrega chica)
N/A declarados:  rubrica entera (entrega chica)
Review externo:  no pedido
Instrumento:     g1_memoria_nulo.py por correr_sondas.py, rc 0, 0 y 0; salida cruda en docs/agents/evidencia/2026-11-07-001-memoria-nulo/
Artefactos:      docs/agents/respuestas/2026-11-07-001-el-nulo-de-g1a-casi-no-ocupa-memoria.md
                 + https://app.clickup.com/90171457413/docs/2kza6fw5-26157/2kza6fw5-30757
```
