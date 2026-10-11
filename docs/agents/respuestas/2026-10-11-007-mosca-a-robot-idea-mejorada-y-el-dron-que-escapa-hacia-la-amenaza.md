# 2026-10-11-007 · De la mosca al robot: la idea mejora si compila motivos certificados que hablan por las descendentes, y el dron de `swarm/` escapa hacia la amenaza

**Fecha:** 2026-10-11, madrugada (America/Buenos_Aires).
**Base:** `drosophila-fep-connectome` main en `5fdf5a4` (los archivos de `swarm/` son los de `02da943`, verificado por blob SHA); `dualbrain` main en `52667ad`; `mojo-absoluto` main en `e1b5b02`.
**Instrumento:** rama `titan/swarm-lazo-cerrado-2026-10-11`: `tools/swarm_lazo_cerrado.py` (md5 `65661dc3a4a65d462588ad5f614b3dbb`) y su log crudo `results/swarm_lazo_cerrado_2026-10-11/run.log` (md5 `b109936678e1fee1c85af5574b9acbd7`, 76 líneas).
**Doc de ClickUp (público):** https://app.clickup.com/90171457413/docs/2kza6fw5-21097

## Veredicto

**La idea, mejorada, en cinco puntos:**

1. **No es un motor que reemplaza el entrenamiento: es un compilador de motivos certificados.** Del conectoma se corta el circuito mínimo que hace una función (escapar, girar, sostener contexto), se certifica contra el nulo anatómico y el de signo, y se compila a C de punto fijo que entra en un microcontrolador. El cerebro entero no entra: la estimación de la rama de materialización para `motor.py` en ESP32 da 2,12 MB de RAM y 173 MB de flash en float32, con 60.367.932 multiplicaciones por paso contra las 3.440 MAC de DualBrain (17.549×).
2. **El motivo habla por las descendentes, no por «neuropilos motores».** Las motoras del cerebro mueven cabeza, boca, antena y cuello; las patas y las alas cuelgan del cordón ventral, que FlyWire no tiene. El Giant Fiber tiene 0 aristas a motoras del cerebro. Y lo único que aguanta los dos nulos con FWER es descendentes → descendentes, → motoras, → cuello y → antena.
3. **La estabilidad la pone un lazo clásico abajo de las descendentes**, un «cordón sintético»: control de actitud con giróscopo (lo que en la mosca hace el haltere) o CPG para patas. La estabilidad no la da la red: el dron de hoy, sin lazo de actitud, pasa los 30° de inclinación en 0,267 s.
4. **Se entrena sólo lo que ya pagó:** la compuerta de DualBrain (21,85× a 108,11× en 4/4, iso-run), la memoria de DBC3 (AULC 0,823 contra 0,635, una tarea) y el readout. La dinámica líquida sobre el conectoma se retira como pilar: empató o perdió en todo lo que se midió.
5. **El falsador de toda la tesis es el brazo S:** la misma máscara barajada con igual grado y sparsity. Si S rinde como el conectoma, lo que paga es la sparsity y no la mosca. Está diseñado desde agosto y nunca se corrió.

**Lo que encontré de paso, y cambia el orden.** El único robot de los repos, `swarm/` (34 neuronas, 83 sinapsis, Q15 para ESP32), **no sale del conectoma**: es una red escrita a mano con nombres de regiones de la mosca. Medido hoy en un cuadricóptero X con física estándar, **escapa hacia la amenaza en las 4 direcciones, y en 108 de 108 combinaciones de parámetros**. Una línea lo da vuelta: leer los motores con reflexión puntual (FL↔BR, FR↔BL) da 4/4 hacia afuera. Además, su test no puede dar rojo (con los 83 pesos en cero sale con 0) y su auditoría devuelve `PASS` fijo aunque se mezclen modalidades, se inviertan los signos o se cableen los sensores directo a los motores. El instrumento sí puede dar rojo: un reflejo físico escrito a mano da 4/4 hacia afuera y una red nula da 4/4 neutro.

## 1. Pedido

> «TITAN FULL, tomá este documento [El repo del conectoma de punta a punta, 11-oct], analizá todo lo relacionado, también la idea de generar partes del cerebro de la mosca y aplicarlo a robótica, eso está en uno de los dos repositorios que nombra el documento. Con todo ello mejorá esta idea: [texto BEEC: DualBrain como núcleo determinista fijado por el conectoma más un módulo líquido entrenable con recableado; ingesta FlyWire, core DualBrain, traducción sensoriomotora, recableado topológico y stack CAVEclient, PyG, JAX y Brian2]».

Los dos repositorios que nombra el documento son `drosophila-fep-connectome` y `mojo-absoluto`. La idea de robótica vive en el primero (`swarm/`, la biblioteca de motivos y el plan de materialización) y tiene un hermano en `dualbrain` (bloques y swarm en C).

## 2. Herramientas y máquina

- **GitHub MCP, lectura:** el contexto vivo, las respuestas 004 a 006 del 11-oct (la 003, a través del contexto) y la 003 del 10-oct; `swarm/` completo; `docs/PLAN-MATERIALIZACION-2026-10-02.md`; `docs/agents/CONTEXTO-motor.md`; `docs/BIBLIOTECA-01-giant-fiber.md` (rama `titan/materializacion-h4-guard-2026-10-02`); la exploración de antecedentes y el claim chart (rama `research/global-connectome-liquid-2026-10-02`); en `dualbrain`, README, ANALISIS y `docs/04-bloques-y-swarm.md`; en `mojo-absoluto`, README y las respuestas 49 y 51 del 1-oct.
- **Índice de 349 registros de la 004** (el CSV del Doc), filtrado en el sandbox por robótica, drones, firmware, motivos, patentes y fuera de distribución.
- **Búsqueda web** para los antecedentes de 2020 a 2026 (§3.4).
- **Sandbox de ClickUp** (Debian 12, gcc 12.2.0, Python 3.12.13, numpy 2.4.6): reconstruí `swarm/` y este CONTEXTO byte a byte, con el blob SHA de git verificado, y corrí el instrumento. No es ninguna de las tres máquinas: brain-env, Actions y Kaggle no se usaron y no se gastó cuota ajena.
- **Escrituras:** la rama `titan/swarm-lazo-cerrado-2026-10-11` con el instrumento y su log; este archivo y el CONTEXTO en `main`; un Doc público en ClickUp. No toqué `swarm/`, ni ramas ajenas, ni PRs.
- **La búsqueda de código de GitHub dio 0 resultados incluso para `swarm/`, que existe.** Ese instrumento no podía dar verde, así que no lo usé como prueba de ausencia.
- **Concurrencia:** mientras trabajaba, otra instancia commiteó la 006 (`5fdf5a4`), que sólo agrega su respuesta. Por eso esta es la 007, y el CONTEXTO toma sus dos correcciones (182 archivos y 27 ramas).

## 3. Qué se midió

### 3.1 Dónde vive «partes del cerebro → robot»

| Pieza | Dónde | Qué es | Estado |
|---|---|---|---|
| `swarm/`, sustrato para micro-drones | `drosophila-fep-connectome`, main | 34 neuronas, 83 sinapsis, Q15, τ = 0,119, para ESP32 | sin hardware; auditado hoy (§3.2) |
| Biblioteca de motivos, ficha GF-01 | rama `titan/materializacion-h4-guard-2026-10-02` | Giant Fiber medido del parquet: 962 aristas de entrada, 9.474 sinapsis, 49,8% inhibitorias; LC6→GF 0 contra 17,2 ± 3,1 | 1 de las 3 o 4 entradas que pide el plan |
| Compilación del GF completo | rama `titan/auditoria-integra-2026-08-25` (`src/compile_gf_full.py`) | 864 nodos, 45.687 aristas | refutó la predicción: FULL 1,0631 contra recorte 1,1128 y sign-shuffle 1,1131 ± 0,0185 |
| Plan de materialización | main | atlas → compilador → biblioteca → controlador embebido, con 4 gates | escrito; capas 3 y 4 sin cerrar |
| DualBrain C99 | main y rama de materialización | 1.336 B de `.text` en ESP32 a `-Os`; ELF linkeado de 44.292 B (no flasheable) y arnés de 512 pasos contra el oráculo numpy | QEMU no bootea; sin hardware |
| Bloques y swarm DBC3 | `dualbrain` | 32 bloques, unos 178 motores | no compila (falta `dbc3_motor.h`), pesos placeholder, sólo PARALLEL validada |

**El hallazgo que ordena todo lo demás:** `gen_swarm.py` no lee ningún parquet. Las 83 conexiones y sus pesos están escritos a mano; de la mosca tiene los nombres. Lo que sí sale del conectoma (la ficha GF-01 y la compilación del GF) nunca llegó al robot.

### 3.2 Auditoría de `swarm/` con un instrumento que puede dar rojo

Convención física declarada: multirrotor X estándar; el lado con más empuje sube y el vehículo acelera hacia el lado contrario. Interfaz que declara el propio repo: `MOTOR | músculos | ESCs (4)` y `q15_to_pwm`, o sea empuje directo. Cada caso se compara contra la misma lectura sin amenaza.

| Gate | Pregunta | Resultado |
|---|---|---|
| G0 | ¿Los archivos son los de main? | **PASS**: 4/4 blob SHA iguales |
| G1 | ¿`gen_swarm.py` regenera lo commiteado? | **PASS**: `.h` y `.json` byte a byte |
| G2 | ¿El test original puede dar rojo? | **FAIL**: con los 83 pesos en cero imprime `505 505 505 505` y sale con 0 |
| G3 | ¿La auditoría de `gen_swarm.py` puede dar rojo? | **FAIL**: `PASS` y `rdi_diseno = 0.0` con modalidades mezcladas, signos invertidos y sensores directo a motores |
| G4 | ¿El escape visual aleja de la amenaza? | **FAIL**: ACERCA en frente, atrás, izquierda y derecha |
| Control positivo | reflejo físico escrito a mano | ALEJA 4/4 |
| Control negativo | red nula | NEUTRO 4/4 |
| Parche | leer los motores con reflexión FL↔BR, FR↔BL | ALEJA 4/4 |
| Sensibilidad | k × horizonte × frecuencia × dirección, 108 casos | original 108 hacia la amenaza; parche 108 hacia afuera |

Lectura:

- **El error es de modelo mental, no de un cable.** Todo el bloque motor supone que el dron va hacia el lado con más empuje, y es al revés. Por eso falla igual en las cuatro direcciones y también con la proximidad por antena (4/4 hacia el vecino; en los laterales ahí se mezclan el escape del GF y la cohesión de FAN_BODY, así que ese canal es informativo y no gate).
- **El README dice «retrocede y rola hacia el vecino. Correcto».** Con física estándar, ese vector de motores **avanza** hacia el obstáculo y rola hacia el vecino. El test, que imprime y no afirma, dice otra cosa: «roll derecha».
- **Sin lazo de actitud, cualquier orden sostenida voltea el dron.** Sin amenaza y con rumbo 0°, la entrada del ocelo al integrador de pitch lo pasa de 30° en 0,267 s. El sustrato no tiene ninguna entrada de velocidad angular: usa el haltere como «altitud», cuando en la mosca el haltere es justamente el giróscopo (Dickinson, 1999).
- **Detalle de la LUT:** la tanh tabulada no pasa por cero (con entrada cero cae en el índice 128, que vale +514 en Q15). Por eso, con los pesos en cero, cada neurona se va a +505: es lo que imprime el test.
- **El tipo «I» del GF en el sustrato no sale del parquet.** En la ficha GF-01, lo inhibitorio es la mitad de su **entrada**; el sustrato lo pone como si el GF fuera inhibidor.

### 3.3 El texto BEEC contra lo que ya está medido

| Afirmación del texto | Evidencia en los repos | Queda |
|---|---|---|
| «El conocimiento está en la topología» | El cableado define ruteo y ganancia (40× entre entrada cableada y no cableada) y prohíbe rutas (LC6→GF 0 contra 17,2; z = −5,61). La persistencia post-estímulo es de topología y signo (sel_post z = +181 y +6,31). **No define la selectividad de pico:** el GF completo da 1,0631 y su sign-shuffle 1,1131 (19 de 20 por encima) | **se acota** a ruteo, ganancia, exclusiones y persistencia |
| «τ dependiente del flujo; adaptación nativa fuera de distribución» | Sobre el conectoma, SparseLTC usa τ fija por neurona y empata 48/48 con el control lineal (HC-2). τ compleja: p = 0,60. τ heterogénea **baja** sel_post (2,0686 contra 4,3287 con τ homogénea, spread 30, sin nulos comparables). En el mismo subgrafo, la ecuación tipo FlyVis le gana a SparseLTC real por 5,56 puntos (una semilla). La τ que depende de la entrada vive en DBC3 y su aporte aislado no está medido. Fuera de distribución: ninguno de los 349 registros del índice lo mide | **se retira como pilar**; τ uniforme en el conectoma; la de DBC3 se mide aislada antes de citarla |
| «El núcleo determinista garantiza estabilidad y cero deriva» | Lo medido es radio espectral 0,99 y tanh acotada: estabilidad del estado interno. La del robot no: el dron se voltea en 0,267 s | **se acota**: la estabilidad del cuerpo la da un lazo clásico |
| «Salida: neuropilos motores → actuadores» | Las motoras del cerebro son de cabeza, boca, antena y cuello; GF → motoras del cerebro = 0 aristas; descendentes → motoras ×3,69 / ×3,21 con nulo de región, y aguanta FWER con los dos nulos | **se reemplaza** por una interfaz de descendentes |
| «Recableado sin fuerza bruta» y «preservación del grafo base» | Se contradicen. El claim chart avisa que buscar arquitecturas desde el conectoma es el terreno de la familia de Google (NAS conectómico, prioridad 2018-05-21) | **se redefine:** máscara fija; se entrena sólo la ganancia por par de tipos celulares, la compuerta y el readout |
| «Más de 130 millones de sinapsis» | Son las detectadas en todo el cerebro. Entre neuronas revisadas hay 54,5 millones (Dorkenwald 2024); el pin del repo tiene 54.492.922 en 15.091.983 aristas | **se corrige** |
| Stack CAVEclient, PyG, JAX, Brian2 | Consultar CAVE en vivo rompe el gate de procedencia. PyTorch es referencia, no runtime. El runtime que existe es C99 en Q15, y el compilador propio es Mojo Absoluto con MLIR (HC-1) | **se reordena** |

### 3.4 Antecedentes que cambian el posicionamiento (verificados hoy)

- **NCP, Lechner, Hasani y otros, Nature Machine Intelligence 2020:** 19 neuronas LTC con cableado inspirado en *C. elegans* y 253 sinapsis manejan la dirección de un auto. «Topología biológica + LTC + control» existe desde hace seis años. https://www.nature.com/articles/s42256-020-00237-3
- **Shiu y otros, Nature 2024:** LIF del cerebro entero sobre FlyWire. https://www.nature.com/articles/s41586-024-07763-9
- **Lappalainen y otros, Nature 2024:** red restringida por conectoma, 64 tipos visuales, entrenada. https://www.nature.com/articles/s41586-024-07939-3
- **NeuroMechFly v2, Nature Methods 2024:** cuerpo simulado con una interfaz descendente que modula CPGs. https://www.nature.com/articles/s41592-024-02497-y
- **Eon Systems, 10-mar-2026:** Shiu, Lappalainen y NeuroMechFly en lazo cerrado. El cuerpo se maneja con unas pocas descendentes (DNa01 y DNa02 para girar, oDN1 para avanzar, las antenales para acicalarse), con mapeos elegidos a mano y sincronía cada 15 ms. El escape por looming no está implementado en el cuerpo. https://eon.systems/updates/embodied-brain-emulation
- **Dorkenwald y otros, Nature 2024:** 139.255 neuronas, 54,5 millones de sinapsis entre ellas y unas 130 millones detectadas en total. https://www.nature.com/articles/s41586-024-07558-y
- **Patentes**, según el claim chart del repo: Google, X Development, Accenture, Qualcomm/Brain Corp y PROME ya ocupan «conectoma → red» y «conectoma → controlador».

**Consecuencia:** «el cerebro entero de la mosca maneja un cuerpo» ya existe, y lo hizo un equipo con el autor del modelo LIF. **La exploración de antecedentes del 2-oct de la rama `research/` no menciona a Eon.** El hueco que queda es el opuesto: el circuito mínimo certificado que entra en un microcontrolador, con su evidencia. No lo encontré en esta búsqueda, que no fue exhaustiva.

## 4. La idea mejorada: BEEC v2, compilador de motivos certificados

**Tesis en una línea:** el conectoma decide qué cables pueden existir y qué ausencias son obligatorias; un motivo chico, certificado contra el nulo, se compila a C de bytes y emite órdenes descendentes; abajo, un lazo clásico pone la estabilidad; y lo único que se entrena es la compuerta, la memoria y el readout.

### 4.1 Capas

| Capa | Qué hace | Qué ya existe | Qué falta |
|---|---|---|---|
| L0 Atlas | FlyWire v783 pinneado por md5 (`3d802fd5…`) y anotaciones `17fc577`; signo por Dale (96.672 E, 41.333 I, 0 mixtas) | `src/cp40.py`, `docs/METHODS.md` | nada para empezar |
| L1 Extractor de motivos («partes del cerebro») | corta del parquet el subgrafo de una función y le arma su ficha: entrada, salida, nulo, límites, costo en bytes y criterio de aborto | ficha GF-01, `compile_gf_full.py` | que `gen_swarm.py` lea el parquet en vez de una lista a mano |
| L2 Compilador | SparseLTC con τ uniforme, CSR, radio 0,99 y Q15 con LUT de tanh centrada; brazo lineal obligatorio | la mitad está en `gen_swarm.py` y `esp32c.py` | exportar a NIR o NeuroML y a Mojo Absoluto con MLIR (HC-1) |
| L3 Interfaz descendente | decodifica la población descendente del motivo en órdenes: escapar con lado, girar, avanzar, retroceder | la medición que la justifica (005 a 009) | la tabla descendente → orden, medida y no elegida a mano |
| L4 Cordón sintético | lazo de actitud con giróscopo (el haltere) o CPG para patas; acá vive la estabilidad | nada en los repos | todo |
| L5 DualBrain/DBC3 | compuerta entre el reflejo del motivo y la memoria de contexto; memoria compacta; readout edge (HC-6) | ablación de la compuerta 4/4; HC-3b; 1.336 B en ESP32 | correr en el target |

**Tamaño, por aritmética y NO MEDIDO:** el subgrafo del GF compilado (864 nodos y 45.687 aristas), en el formato de `swarm/` (6 B por sinapsis), son 274.122 B de tabla y 1.728 B de estado, con 13,3 veces las MAC de DualBrain por paso. Entra en un ESP32; el cerebro entero, no.

### 4.2 La interfaz descendente: candidatos de literatura, a medir

| Orden para el robot | Descendentes candidatas | Estado acá |
|---|---|---|
| Escapar, con lado | Giant Fiber (DNp01), una por hemisferio | ficha GF-01 medida: LC4 10,8× y LPLC2 9,8× sobre el nulo anatómico |
| Girar | DNa01 y DNa02 (Yang 2024, usado por Eon) | NO MEDIDO |
| Avanzar | oDN1 (según Eon, citando a Sapkal 2024) | NO MEDIDO |
| Retroceder | MDN (Bidaye 2014) | NO MEDIDO |

### 4.3 Gates, todos con su forma de dar rojo

1. **Procedencia:** pin de datos y de código; prohibido mezclar snapshots.
2. **Nulo:** anatómico, de signo con Dale y **brazo S**. Un motivo entra a la biblioteca sólo si le gana a S.
3. **Física en lazo cerrado:** el motivo, con su interfaz descendente y su cordón sintético, tiene que producir la conducta en simulación y fallar cuando se lo rompe. El instrumento de hoy es el primero, y ya dio rojo.
4. **Edge:** bytes, RAM y latencia medidos en el target, no en x86.
5. **Causal:** silenciar el motivo en la simulación tiene que hacer caer la conducta.

### 4.4 Orden de trabajo y su criterio

Criterio: primero lo que hace que el producto exista; después, lo que lo certifica. Las dependencias se miraron por archivo.

1. **Arreglar el dron (una tarde, no depende de nada).** Reflexión de la lectura de motores, un test que afirme y pueda fallar, el haltere como giróscopo y la LUT centrada. El parche de lectura ya está probado como brazo del instrumento. Toca sólo `swarm/`.
2. **El primer motivo real (depende del parquet, que está cargado en brain-env).** GF-01 → interfaz descendente → dron, en lugar de la red escrita a mano. Toca `compile_gf_full.py` y un generador nuevo.
3. **Brazo S contra W y B (unos 90 minutos de CPU).** El falsador de toda la tesis, con el criterio de aborto ya escrito en `CONTEXTO-motor.md` §6.2. No comparte archivos con 1 y 2: puede correr en paralelo.
4. **Edge:** linkear y correr DualBrain y el motivo en un ESP32.

### 4.5 Qué se deja afuera, a propósito

- **Emular el cerebro entero en un cuerpo:** ya lo hace Eon, con el autor del modelo LIF.
- **τ compleja y τ heterogénea en el producto:** perdieron o empataron en todo lo medido.
- **NAS o un recableado que agregue aristas:** choca con la familia de Google y rompe la máscara.
- **El swarm de 32 bloques de `dualbrain`:** no compila y sus pesos son placeholder. Vuelve cuando existan `dbc3_motor.h` y pesos entrenados.

## 5. Evidencia cruda (verbatim)

Líneas 1 a 4, 9, 13 a 22, 24 a 27, 32 a 40, 44, 64 a 66, 71 a 73 y 75 de `results/swarm_lazo_cerrado_2026-10-11/run.log` (rama `titan/swarm-lazo-cerrado-2026-10-11`, md5 `b109936678e1fee1c85af5574b9acbd7`). El log entero son 76 líneas.

```text
$ python3 tools/swarm_lazo_cerrado.py --swarm-dir swarm --out results/swarm_lazo_cerrado_2026-10-11
# maquina: sandbox de ClickUp | Linux 6.1.158+ x86_64 | gcc (Debian 12.2.0-14+deb12u1) 12.2.0 | Python 3.12.13 | numpy 2.4.6
# md5 tools/swarm_lazo_cerrado.py = 65661dc3a4a65d462588ad5f614b3dbb
# fecha: 2026-10-11 04:05:22 -03
CHEQUEO G0_PROCEDENCIA PASS
CHEQUEO G1_REPRODUCIBILIDAD PASS
G2 mutacion=original sinapsis_cambiadas=0 gcc_exit=0 test_exit=0 salida=motores (FL FR BL BR): -11037 -9499 15973 17462
G2 mutacion=pesos_cero sinapsis_cambiadas=83 gcc_exit=0 test_exit=0 salida=motores (FL FR BL BR): 505 505 505 505
G2 mutacion=gf_motor_invertido sinapsis_cambiadas=8 gcc_exit=0 test_exit=0 salida=motores (FL FR BL BR): -5937 -4248 566 3096
CHEQUEO G2_TEST_PUEDE_DAR_ROJO FAIL
G3 {"E": 83, "firewalls": [], "gaba_gate": "PASS", "gen_exit": 0, "motor_starvation": "NO", "ms_gate": "PASS", "mutacion": "sin_mutar", "rdi_diseno": 0.0}
G3 {"E": 87, "firewalls": [], "gaba_gate": "PASS", "gen_exit": 0, "motor_starvation": "NO", "ms_gate": "PASS", "mutacion": "mezcla_modalidades", "rdi_diseno": 0.0}
G3 {"E": 83, "firewalls": ["gf_f", "gf_b", "gf_l", "gf_r", "wta_f", "wta_b", "wta_l", "wta_r", "lh_f", "lh_b", "lh_l", "lh_r", "fb_l", "fb_r", "pb_alt", "pb_pitch", "pb_roll", "pb_head", "mot_fl", "mot_fr", "mot_bl", "mot_br"], "gaba_gate": "PASS", "gen_exit": 0, "motor_starvation": "REVISAR", "ms_gate": "PASS", "mutacion": "signos_invertidos", "rdi_diseno": 0.0}
G3 {"E": 131, "firewalls": [], "gaba_gate": "PASS", "gen_exit": 0, "motor_starvation": "NO", "ms_gate": "PASS", "mutacion": "sensores_directo_a_motores", "rdi_diseno": 0.0}
CHEQUEO G3_AUDITORIA_PUEDE_DAR_ROJO FAIL
ESTATICO canal=lamina amenaza=frente motores_FL_FR_BL_BR=-10088 -10564 16919 16764 torque_roll=+631 torque_pitch=-54335 -> ACERCA
ESTATICO canal=lamina amenaza=atras motores_FL_FR_BL_BR=17403 16919 -10564 -10873 torque_roll=+793 torque_pitch=+55759 -> ACERCA
ESTATICO canal=lamina amenaza=izquierda motores_FL_FR_BL_BR=-10088 16919 -10564 16764 torque_roll=-54335 torque_pitch=+631 -> ACERCA
ESTATICO canal=lamina amenaza=derecha motores_FL_FR_BL_BR=17403 -10564 16919 -10873 torque_roll=+55759 torque_pitch=+793 -> ACERCA
LAZO canal=lamina lectura=ORIGINAL amenaza=frente H=0.15s delta_hacia_amenaza_m=+0.000537 inclinacion_max_grados=4.48 -> ACERCA
LAZO canal=lamina lectura=ORIGINAL amenaza=atras H=0.15s delta_hacia_amenaza_m=+0.000568 inclinacion_max_grados=4.89 -> ACERCA
LAZO canal=lamina lectura=ORIGINAL amenaza=izquierda H=0.15s delta_hacia_amenaza_m=+0.000537 inclinacion_max_grados=4.48 -> ACERCA
LAZO canal=lamina lectura=ORIGINAL amenaza=derecha H=0.15s delta_hacia_amenaza_m=+0.000568 inclinacion_max_grados=4.89 -> ACERCA
LAZO canal=lamina lectura=REFLEJADO amenaza=frente H=0.15s delta_hacia_amenaza_m=-0.000537 inclinacion_max_grados=4.48 -> ALEJA
LAZO canal=lamina lectura=REFLEJADO amenaza=atras H=0.15s delta_hacia_amenaza_m=-0.000568 inclinacion_max_grados=4.89 -> ALEJA
LAZO canal=lamina lectura=REFLEJADO amenaza=izquierda H=0.15s delta_hacia_amenaza_m=-0.000537 inclinacion_max_grados=4.48 -> ALEJA
LAZO canal=lamina lectura=REFLEJADO amenaza=derecha H=0.15s delta_hacia_amenaza_m=-0.000568 inclinacion_max_grados=4.89 -> ALEJA
LAZO canal=lamina lectura=CERO amenaza=frente H=0.15s delta_hacia_amenaza_m=+0.000000 inclinacion_max_grados=0.00 -> NEUTRO
LAZO canal=lamina lectura=REFLEJO_FISICO amenaza=frente H=0.15s delta_hacia_amenaza_m=-0.006601 inclinacion_max_grados=20.22 -> ALEJA
SENSIBILIDAD lectura=ORIGINAL combinaciones=108 (k x H x frecuencia x direccion) signo_hacia_amenaza: positivo=108 negativo=0 cero=0 |delta|_min_m=5.889e-07 |delta|_max_m=3.379e-02
SENSIBILIDAD lectura=REFLEJADO combinaciones=108 (k x H x frecuencia x direccion) signo_hacia_amenaza: positivo=0 negativo=108 cero=0 |delta|_min_m=5.889e-07 |delta|_max_m=3.379e-02
REPOSO lectura=ORIGINAL sin_amenaza rumbo=0 deriva_a_0.15s_x_m=-0.000408 y_m=+0.000029 inclinacion_a_0.15s_grados=3.64 t_hasta_30grados_s=0.267
CHEQUEO INSTRUMENTO control_positivo=ALEJA/ALEJA/ALEJA/ALEJA control_negativo=NEUTRO/NEUTRO/NEUTRO/NEUTRO -> VALIDO
CHEQUEO G4_ESCAPE_LAMINA original=ACERCA/ACERCA/ACERCA/ACERCA reflejado=ALEJA/ALEJA/ALEJA/ALEJA -> FAIL
VEREDICTO_SUJETO=FAIL gates_en_rojo=G2,G3,G4
EXIT_RUN=1
```

Recomputable: en un clon, `git checkout titan/swarm-lazo-cerrado-2026-10-11 && python3 tools/swarm_lazo_cerrado.py --swarm-dir swarm --out results/swarm_lazo_cerrado_2026-10-11`. Pide `gcc` y `numpy`. Si G0 no da 4/4 IGUAL, `swarm/` cambió y el veredicto no aplica.

## 6. Archivos generados

- **En la rama `titan/swarm-lazo-cerrado-2026-10-11`:** `tools/swarm_lazo_cerrado.py` (md5 `65661dc3a4a65d462588ad5f614b3dbb`) y `results/swarm_lazo_cerrado_2026-10-11/run.log` (md5 `b109936678e1fee1c85af5574b9acbd7`). El JSON que escribe el instrumento no se commitea: es derivado y determinista (md5 `facac8527a0fcc9779aacee2aafe6ff6` en dos corridas).
- **En `main`:** este archivo y `docs/agents/CONTEXTO-drosophila-fep.md` actualizado.
- **Doc de ClickUp público:** https://app.clickup.com/90171457413/docs/2kza6fw5-21097
- No se commitea la reconstrucción de `swarm/` del sandbox: es copia byte a byte de main.

## 7. NO MEDIDO

- **Nada en hardware:** ni ESP32 ni dron real. La física es un modelo lineal de ángulo chico que sostiene el signo; los metros y los tiempos dependen de k, I y l elegidos.
- **La conclusión vale para la interfaz que declara el repo** (salida → ESC). Si la salida fuera una consigna para un controlador de vuelo, hay que volver a medir.
- **BEEC v2 entera:** es diseño; ninguna capa nueva está implementada.
- **La tabla descendente → orden:** sale de literatura, no de una medición propia.
- **GF-01 compilado en Q15 y montado en el dron:** sólo la estimación aritmética.
- **El brazo S** y cualquier medición fuera de distribución.
- **La búsqueda de antecedentes no fue exhaustiva:** «no lo encontré» no es «no existe».
- **Review externo:** no hay PR ni review de Copilot. El instrumento es el testigo de la corrida y su log va crudo; la elección de qué medir es mía (W-01), así que falta que alguien que no escribió el instrumento elija otro objetivo.
- **`CONTEXTO-motor.md` sigue vencido** desde el 24-ago; no lo reescribí.

## Antes de firmar

```text
"gen_swarm.py reproduce lo commiteado"  → blob SHA del regenerado          → podía dar rojo: SÍ → medido, bien
"el test de swarm no detecta nada"      → test con los 83 pesos en cero    → podía dar rojo: SÍ → medido, mal
"la auditoría de gen_swarm es fija"     → 3 topologías mutadas             → podía dar rojo: SÍ → medido, mal
"el dron escapa hacia la amenaza"       → lazo cerrado con dos controles   → podía dar rojo: SÍ → medido, mal
"el parche lo da vuelta"                → mismo arnés, lectura reflejada   → podía dar rojo: SÍ → medido, bien (en simulación)
"anda en un dron de verdad"             → ninguno                          → NO MEDIDO
"BEEC v2 funciona"                      → ninguno                          → NO MEDIDO
```

## QA (TITAN FULL)

| Criterio | Puntaje | Evidencia |
|---|---|---|
| Completitud | 14/15 | Los seis campos, el inventario de las tres fuentes y las cinco capas. −1: la capa descendente queda especificada con literatura, sin tabla medida |
| Ejecutabilidad | 15/15 | `python3 tools/swarm_lazo_cerrado.py ...`: exit 1 con el instrumento VÁLIDO; el arnés compila con `-Wall -Wextra -Werror`; dos corridas, mismo JSON |
| Arquitectura del razonamiento | 9/10 | Cada pilar del texto contra su número (§3.3). −1: el hueco del microcontrolador sale de una búsqueda no exhaustiva |
| Documentación | 9/10 | Docstring, convenciones físicas y códigos de salida en el instrumento; fuentes linkeadas. −1: el README de `swarm/` sigue diciendo «Correcto» |
| Innovación | 5/5 | Implementado en el instrumento: pin por blob SHA, mutaciones del test y de la auditoría, lazo cerrado con dos controles, sensibilidad de 108 casos y el parche como brazo |
| Proceso QA | 4/5 | Cada fila con línea del log o archivo. −1: sin review externo |
| Seguridad, Testing, DevOps | N/A (40) | Sin frontera de confianza ni red; un instrumento de diagnóstico, cuyos controles positivo y negativo son la prueba; sin despliegue ni CI nuevo |

**56/60 → 93/100 sobre lo aplicable.** Aprobado con deuda: review externo, hardware y el brazo S.

--- METODO PROMETEO ---
Acción delicada: NO
Modo aplicado:   TITAN FULL
Rúbrica:         56/60 -> 93/100
N/A declarados:  40 (Seguridad 15, Testing 15, DevOps 10; ver QA)
Review externo:  no pedido: no hay PR (deuda)
Instrumento:     sandbox de ClickUp; `python3 tools/swarm_lazo_cerrado.py --swarm-dir swarm --out results/swarm_lazo_cerrado_2026-10-11`; exit 1 (sujeto FAIL, instrumento VÁLIDO); log crudo en la rama `titan/swarm-lazo-cerrado-2026-10-11`
Máquina:         sandbox de ClickUp (Debian 12, gcc 12.2.0, Python 3.12.13, numpy 2.4.6); brain-env, Actions y Kaggle sin uso
Artefactos:      `docs/agents/respuestas/2026-10-11-007-mosca-a-robot-idea-mejorada-y-el-dron-que-escapa-hacia-la-amenaza.md` + https://app.clickup.com/90171457413/docs/2kza6fw5-21097
