# 2026-10-12-011: no es la neurona; el motivo de 28 tiene el 3% de la entrada de sus descendentes y nada de su inhibición, y la DCMT como vino invierte el glutamato

**Doc espejo:** https://app.clickup.com/90171457413/docs/2kza6fw5-21497
**Rama con scripts y logs crudos:** `titan/chequeo-dcmt-2026-10-12` (`6ebe1f7`), sin PR.
**Base:** `main` en `846cb76`.

## Veredicto (conclusión, no medición)

**No es la neurona.** Lo medido no apunta a ella, y una neurona nueva no rescata «todo».

- **Los dos fracasos que pesan no son de la neurona.** En la 004 la LSTM, que es otra neurona, falla igual que DBC3 (0,658 a 0,672 contra el techo de no recordar, 2/3) y una máquina de estados de dos líneas les gana (0,7663). En la 005 los 28 estados conservan la información (0,8717 a 0,9867) y lo que la pierde es el embudo de 4 descendentes leído con un lector entrenado. Ninguna neurona agranda ese embudo: cada descendente sigue siendo un número.
- **Donde la neurona sí pesó, la líquida ya pasó su control.** La plena le gana a la no líquida con los mismos parámetros (0,9854 contra 0,9453, 4/4; 013 y 014). Es la «τ dinámica» que propone la DCMT, y ya está.
- **Medido hoy, y no estaba en el CONTEXTO: el candidato es el recorte.** El motivo de 28 de la 003 a la 005 lleva **539 de las 18.191 sinapsis de entrada de sus 4 descendentes (2,96%)** y **ninguna de las 7.889 inhibitorias (43,4%)**. DNp01 recibe 48,5 a 51,5% de entrada inhibitoria y DNp07 35,9 a 36,8%, toda afuera del motivo.
- **Lo nuevo de la DCMT no tiene con qué alimentarse ni qué separar.** El parquet del pipeline no trae neuropilo ni coordenadas por sinapsis (no hay cómo asignar dendritas) y el motivo no tiene aristas inhibitorias (el compartimento I quedaría vacío). En la fibra gigante, Ache 2019 reproduce la respuesta con una **suma** de lo que traen LC4 y LPLC2: la no linealidad está antes, en los detectores.
- **Su mapeo E/I está mal para la mosca.** Poner el glutamato como excitatorio da vuelta **21.863 neuronas y 9.266.016 sinapsis (17,00% del cerebro)**, entre ellas PVLP010, CL038 y PLP214, que hoy inhiben a estas descendentes. Shiu 2024 midió que ese cambio sube los falsos positivos de su validación optogenética **de 1% a 16%**. La octopamina no tiene clase (193 neuronas) y la glicina no es una clase de FlyWire (0 neuronas).
- **Los modelos de mosca con resultados usan neuronas puntuales simples:** Shiu 2024 (LIF, signo por neurotransmisor, un solo parámetro libre), FlyVis 2024 (tasa con τ fija por tipo, 734 parámetros; ver la 2026-10-11-009) y Eon 2026 (el LIF de Shiu en un cuerpo de MuJoCo: «91% behavior accuracy» según su anuncio, no el 95% que dice el análisis).

**Sobre «que todo resulte»:** elegir la neurona después de los fracasos para rescatar las hipótesis es el camino del que la 013 enseñó a desconfiar (la diagonal ganaba por parámetros). Una neurona nueva entra como hipótesis con falsador, con control de parámetros y contra los mismos nulos (SL y T), que corren la misma neurona.

## 1. Pedido

Abraham, 12-oct, 15:28 ART, resumido sin interpretar: si parte del problema por el que no se pueden emular a la perfección las partes del cerebro de la mosca ni demostrar sus hipótesis es que la neurona líquida o el esquema armado con ellas no son apropiados; y si puede existir la posibilidad de que todo su trabajo resulte apoyándose en una neurona nueva que tome lo mejor de SparseLTC, DualBrain y DBC3 más lo mejor de un análisis pegado. El análisis (de otra IA) propone la neurona **DCMT** (compartimentos dendríticos con pesos E/I separados por neurotransmisor, soma CfC/LTC con τ(m), vía moduladora lenta m, disparo opcional) y cinco capas sobre PyTorch: cola de eventos asíncrona, kernel dendrítico en Triton, solver ODE adjunto con torchode, grafo E/I de FlyWire y la celda `DCMTCell`.

## 2. Herramientas y máquina

- **GitHub, lectura:** `docs/agents/CONTEXTO-drosophila-fep.md` (blob `f0f7d744…`), las respuestas 2026-10-12-010, 2026-10-12-008 y 2026-10-11-009, y `tools/escape_aterrizaje/escape_aterrizaje_dbc3.py` en `titan/escape-aterrizaje-2026-10-12` (`af4bea6`; de ahí se copió la selección del motivo).
- **Web, lectura:** eon.systems (anuncio del 8-mar-2026), Shiu et al. 2024 (Nature 634), documentación de torchode (readthedocs), Ache et al. 2019 (Current Biology 29) y Suver, Mamiya y Dickinson 2012 (Current Biology 22).
- **brain-env** (gateway, servicio `build`): búsqueda de datos en `/workspace`, dos scripts escritos en `/workspace/dcmt_2026-10-12/` y corridos (7,2 s y 3,8 s), y cotejo md5 de lo commiteado bajándolo por raw. Sólo lectura de datos; sin cuota ajena.
- **Sandbox de ClickUp:** escritura de los scripts, reconstrucción byte a byte de los logs (md5 iguales a los del taller) y aritmética de porcentajes.
- **Escrituras:** la rama `titan/chequeo-dcmt-2026-10-12` (`6ebe1f7`: scripts y logs), este archivo en `main` y su Doc (https://app.clickup.com/90171457413/docs/2kza6fw5-21497). **No** se tocó el PR #27, Zenodo, Tao ni el CONTEXTO.
- **Inventario de las tres máquinas:** no re-medido. Ninguna conclusión de hoy depende de una capacidad que no se haya usado en el acto.

## 3. Qué se midió

Instrumentos: `tools/neurona_nueva/chequeo_dcmt.py` (md5 `d965ee12cd7bd0bece24eb0790274bb5`) y `tools/neurona_nueva/inhibicion_visual_q5.py` (md5 `c2e5719c0bea041b825c6a4335a24222`), sobre `/workspace/connectivity.parquet` (md5 `3d802fd542b5d18570ba1ba0bb0abed9`, el pin de la 003; 15.091.983 aristas y 54.492.922 sinapsis) y `/workspace/annotations.tsv` (md5 `719904abad876c68ace1b5690c9b9b63`; 139.248 filas). Exit 0 en los dos. Ninguno entrena nada.

### Q1 · Qué signo usa el pipeline

Cada neurona presináptica tiene un solo signo (0 mixtas de 138.005). El glutamato va inhibitorio (21.863 de 24.804 neuronas Glu), el GABA inhibitorio (17.731 de 19.079), y ACh, DA, 5HT y OA excitatorios: la convención de Shiu 2024. **3.079 neuronas** tienen un signo distinto del que daría su `top_nt` en este archivo de anotaciones (0,76% de las sinapsis): el signo del parquet no sale de esta columna, y su fuente exacta queda NO MEDIDA.

### Q2 · Qué daría vuelta el mapeo de la DCMT

ACh, Glu, DA y 5HT excitatorias; GABA y glicina inhibitorias. En total: 24.942 neuronas (18,07%), 2.944.379 aristas (19,51%) y 9.678.587 sinapsis (17,76%). **La regla del glutamato sola: 21.863 neuronas (15,84%), 2.829.009 aristas (18,75%) y 9.266.016 sinapsis (17,00%).** El resto es la discrepancia de Q1. Sin clase en la DCMT: octopamina, 193 neuronas y 137.839 sinapsis. Glicina: 0 neuronas en `top_nt`.

### Q3 · Con qué se asignarían dendritas

Columnas del parquet: `Presynaptic_ID, Postsynaptic_ID, Presynaptic_Index, Postsynaptic_Index, Connectivity, Excitatory, Excitatory x Connectivity, __index_level_0__`. **No hay neuropilo ni coordenadas por sinapsis.** El filtro por subcadena del script marcó `Postsynaptic_ID` y `Postsynaptic_Index` como espaciales porque contienen «pos»: **falso positivo del instrumento**, corregido con la lista de columnas, que sí podía contradecir. Las anotaciones traen `pos_x/y/z` y `soma_x/y/z`: un punto por neurona, no por sinapsis. En `/workspace`, hasta profundidad 4, los únicos datos de FlyWire son ese parquet y esas anotaciones (más una copia en `wrun/datos/` y `annot_hist/annot_c03ad46.tsv`): no hay tabla de sinapsis ni de conexiones por neuropilo.

### Q4 · El motivo y lo que deja afuera

Reproduce el de la 003: 28 neuronas, 73 aristas, 0 inhibitorias, 665 sinapsis (`top_nt`: ACh 27, Glu 1).

| Descendente | Entrada total | Inhibitoria | Del motivo | De todos los LC4, LPLC2 y LPLC4 | Presinápticas |
|---|---|---|---|---|---|
| DNp01 izq. | 4.327 | 2.227 (51,5%) | 110 (2,5%) | 832 (19,2%) | 479 |
| DNp01 der. | 5.147 | 2.495 (48,5%) | 121 (2,4%) | 1.053 (20,5%) | 483 |
| DNp07 izq. | 4.656 | 1.672 (35,9%) | 170 (3,7%) | 811 (17,4%) | 556 |
| DNp07 der. | 4.061 | 1.495 (36,8%) | 138 (3,4%) | 638 (15,7%) | 492 |
| **Total** | **18.191** | **7.889 (43,4%)** | **539 (2,96%)** | 3.334 (18,3%) | |

Inhibitorias mayores: CB3707, SAD014, LHAD1g1 y CB0010 (GABA), PVLP010 y CL038 (Glu) a DNp01; CB0442, CL128a, PLP173, SAD072 y AOTU049 (GABA), PLP214 y AOTU063b (Glu) a DNp07. Con el mapeo de la DCMT, las glutamatérgicas pasarían a excitarlas.

### Q5 · Cuánta de esa inhibición es visual a dos saltos

De las 551 inhibitorias que llegan a las 4 descendentes (7.889 sinapsis), las que a su vez reciben de LC4, LPLC2 o LPLC4:

| Umbral de entrada visual | DNp01 izq. | DNp01 der. | DNp07 izq. | DNp07 der. | Motivo ampliado |
|---|---|---|---|---|---|
| ≥ 1 sinapsis | 57,8% | 62,1% | 57,9% | 51,0% | 265 neuronas |
| ≥ 5 | 41,4% | 49,0% | 43,2% | 42,3% | 195 |
| ≥ 20 | 30,4% | 27,5% | 36,5% | 37,3% | 140 |

**Pero esas inhibitorias reciben poco de lo visual:** de las 12 mayores, la que más recibe de LC4, LPLC2 y LPLC4 es LHAD1g1, con 5,2% de su entrada; CB0442, CB0563 y una CB3707 reciben 0. Hay una vía de inhibición a dos saltos de la misma entrada, pero casi todo lo que mueve a esas inhibitorias viene de afuera de esta visión.

### Literatura verificada hoy (verbatim)

- **Shiu et al. 2024, Nature 634** (nature.com/articles/s41586-024-07763-9): «Although glutamate can be either excitatory or inhibitory in Drosophila, by default we assume that glutamate is inhibitory, consistent with previous experimental work and computational modelling … altering this assumption increases the false positive rate of the optogenetic activation experiment (Fig. 2) from 1% to 16%.»
- **Eon Systems, 8-mar-2026** (eon.systems/updates/weve-uploaded-a-fruit-fly): «We took the @FlyWireNews connectome of the fruit fly brain, applied a simple neuron model (@Philip_Shiu Nature 2024) and used it to control a MuJoCo physics-simulated body … The uploaded fly has 91% behavior accuracy» y «Another limitation is that we're using Leaky Integrate-and-Fire, which doesn't have any kind of plasticity rules. This fly cannot form long-term memories atm.» Es un anuncio de la empresa, no un paper revisado.
- **Ache et al. 2019, Current Biology 29** (doi 10.1016/j.cub.2019.01.079): «A model summing a linear function of angular velocity (provided by LC4) and a Gaussian function of angular size (provided by LPLC2) replicates GF looming response dynamics and predicts the peak response time.»
- **Suver, Mamiya y Dickinson 2012, Current Biology 22(24)** (doi 10.1016/j.cub.2012.10.034): «octopamine cells that project to the optic lobes increase in activity during flight … we find that they are both necessary and sufficient for the flight-induced visual boost.»
- **torchode** (torchode.readthedocs.io): el solver se arma como `to.AutoDiffAdjoint(step_method, step_size_controller)` y se llama `solver.solve(to.InitialValueProblem(y0=..., t_eval=...))`; `AutoDiffAdjoint` retropropaga a través del solver, y el método adjunto es `to.BacksolveAdjoint`.

### Lectura del código pegado (no ejecutado)

- El kernel Triton calcula `sigmoid(w_e·x_e − w_i·x_i)` elemento a elemento, un escalar por programa: **no suma sobre sinapsis**, así que no implementa z_d = σ(W_d·x_d). PyTorch eso lo hace solo, y el backward a mano duplica autograd. Triton pide GPU: en el inventario sólo Kaggle tiene (foto de agosto, no re-medida).
- `DCMTDynamics` parte el estado con `self.D` (número de dendritas, 4) cuando `x` tiene `hidden_fast` (64); `self.soma(soma_input, m)` le pasa dos argumentos a un `nn.Sequential`, que acepta uno; `DendriteLayer.apply(...)` tiene puntos suspensivos literales.
- `solve_ivp(term=…, t_span=…, method=Tsit5(), adjoint=True)` no es la API documentada de torchode.
- «Gradientes exactos sin discretización temporal»: el adjunto integra hacia atrás numéricamente; ahorra memoria, no es exacto.
- `EventQueue` con `heapq` en Python: un evento por vez, no diferenciable, y contradice «el mismo optimizer.step() de siempre».
- `_assign_dendrites(df)` no está definida, y con estos datos no se puede definir (Q3).
- La tabla del análisis dice que el LIF es de «tiempo discreto fijo»: el LIF es una ODE continua; discreto es el simulador.
- «Conectividad poliádica, entonces compartimentos» no se sigue: poliádica es un sitio presináptico con varios postsinápticos, y no dice nada de los compartimentos de una neurona postsináptica.

## 4. Evidencia cruda

### Búsqueda de datos en brain-env

Herramienta `python` del servicio `build`; recorre `/workspace` hasta profundidad 4 salteando `.git`, `node_modules`, `.gradle`, `build`, `__pycache__` y `.cache`, y lista `.parquet`, `.feather`, anotaciones `.tsv`/`.csv` y nombres con «synapse». Exit 0. Salida completa:

```plain
MAQUINA 6c09d8604b07 Linux-4.19.0-27-amd64-x86_64-with-glibc2.41 2026-10-12 18:35:24 +0000
32638576 /workspace/annot_hist/annot_c03ad46.tsv
31718505 /workspace/annotations.tsv
100804642 /workspace/connectivity.parquet
31718505 /workspace/wrun/datos/annotations.tsv
100804642 /workspace/wrun/datos/connectivity.parquet
TOTAL 5
```

Entorno (`free -m` y versiones, mismo turno): pyarrow 25.0.1, pandas 3.0.5, numpy 2.5.3; memoria disponible 2.786 MB de 7.802.

### Corrida 1: chequeo_dcmt.py

```plain
cd /workspace/dcmt_2026-10-12 && md5sum chequeo_dcmt.py && (python3 chequeo_dcmt.py > run.log 2>&1 || echo FALLO_PYTHON) && cat run.log && md5sum run.log
```

Exit 0. Salida completa:

```plain
d965ee12cd7bd0bece24eb0790274bb5  chequeo_dcmt.py
# maquina: 6c09d8604b07 | Linux-4.19.0-27-amd64-x86_64-with-glibc2.41 | Python 3.12.14 | numpy 2.5.3 | pandas 3.0.5 | pyarrow 25.0.1
# md5 script = d965ee12cd7bd0bece24eb0790274bb5
# fecha: 2026-10-12 18:38:58 +0000
# md5 conn = 3d802fd542b5d18570ba1ba0bb0abed9 | md5 annot = 719904abad876c68ace1b5690c9b9b63
Q3 PARQUET_COLUMNAS Presynaptic_ID,Postsynaptic_ID,Presynaptic_Index,Postsynaptic_Index,Connectivity,Excitatory,Excitatory x Connectivity,__index_level_0__
Q3 ANNOT_COLUMNAS supervoxel_id,root_id,pos_x,pos_y,pos_z,soma_x,soma_y,soma_z,nucleus_id,flow,super_class,cell_class,cell_sub_class,supertype,cell_type,hemibrain_type,ito_lee_hemilineage,hartenstein_hemilineage,top_nt,top_nt_conf,known_nt,known_nt_source,side,nerve,vfb_id,fbbt_id,status,dimorphism,matching_notes,fru_dsx,synonyms
Q3 COLUMNAS_ESPACIALES_EN_PARQUET Postsynaptic_ID,Postsynaptic_Index
Q1 COLUMNA_NT top_nt
ANNOT filas=139248
CONN filas=15091983
Q1 PRESINAPTICAS=138005 con_signo_mixto=0
Q1 NT=5HT signo_pipeline=-1 neuronas=9 aristas=217 sinapsis=928
Q1 NT=5HT signo_pipeline=+1 neuronas=2127 aristas=113712 sinapsis=435278
Q1 NT=ACh signo_pipeline=-1 neuronas=1719 aristas=73031 sinapsis=269984
Q1 NT=ACh signo_pipeline=+1 neuronas=84162 aristas=8114668 sinapsis=30190689
Q1 NT=DA signo_pipeline=-1 neuronas=3 aristas=269 sinapsis=621
Q1 NT=DA signo_pipeline=+1 neuronas=5897 aristas=656120 sinapsis=1383910
Q1 NT=GABA signo_pipeline=-1 neuronas=17731 aristas=3129840 sinapsis=12459807
Q1 NT=GABA signo_pipeline=+1 neuronas=1348 aristas=41853 sinapsis=141038
Q1 NT=Glu signo_pipeline=-1 neuronas=21863 aristas=2829009 sinapsis=9266016
Q1 NT=Glu signo_pipeline=+1 neuronas=2941 aristas=70756 sinapsis=205860
Q1 NT=OA signo_pipeline=-1 neuronas=1 aristas=11 sinapsis=18
Q1 NT=OA signo_pipeline=+1 neuronas=192 aristas=62103 sinapsis=137821
Q1 NT=SIN_ANOTACION signo_pipeline=-1 neuronas=7 aristas=304 sinapsis=831
Q1 NT=SIN_ANOTACION signo_pipeline=+1 neuronas=5 aristas=90 sinapsis=121
Q2 DCMT_CAMBIA_SIGNO neuronas=24942/138005 (18.07%) aristas=2944379/15091983 (19.51%) sinapsis=9678587/54492922 (17.76%)
Q2 CAMBIA nt=5HT neuronas=9 aristas=217 sinapsis=928
Q2 CAMBIA nt=ACh neuronas=1719 aristas=73031 sinapsis=269984
Q2 CAMBIA nt=DA neuronas=3 aristas=269 sinapsis=621
Q2 CAMBIA nt=GABA neuronas=1348 aristas=41853 sinapsis=141038
Q2 CAMBIA nt=Glu neuronas=21863 aristas=2829009 sinapsis=9266016
Q2 SIN_CLASE_EN_DCMT nt=OA neuronas=193 aristas=62114 sinapsis=137839
Q2 SIN_CLASE_EN_DCMT nt=SIN_ANOTACION neuronas=12 aristas=394 sinapsis=952
Q4 MOTIVO neuronas=28 aristas=73 inhibitorias=0 sinapsis=665
Q4 MOTIVO_NT ACh=27,Glu=1
Q4 REPRODUCE_003 (28 neuronas, 73 aristas, 0 inhibitorias) -> True
Q4 DN DNp01 left entrada_total=4327 inhibitoria=2227 (51.5%) de_las_neuronas_del_motivo=110 (2.5%) de_tipos_LC4_LPLC2_LPLC4=832 (19.2%) presinapticas=479
Q4 DN DNp01 left top_inhibitorias CB3707(GABA)=293; SAD014(GABA)=136; LHAD1g1(GABA)=130; PVLP010(Glu)=113; CB0010(GABA)=111
Q4 DN DNp01 right entrada_total=5147 inhibitoria=2495 (48.5%) de_las_neuronas_del_motivo=121 (2.4%) de_tipos_LC4_LPLC2_LPLC4=1053 (20.5%) presinapticas=483
Q4 DN DNp01 right top_inhibitorias CB3707(GABA)=340; SAD014(GABA)=156; CL038(Glu)=143; PVLP010(Glu)=137; LHAD1g1(GABA)=124
Q4 DN DNp07 left entrada_total=4656 inhibitoria=1672 (35.9%) de_las_neuronas_del_motivo=170 (3.7%) de_tipos_LC4_LPLC2_LPLC4=811 (17.4%) presinapticas=556
Q4 DN DNp07 left top_inhibitorias CB0442(GABA)=241; PLP214(Glu)=227; CL128a(GABA)=95; PLP173(GABA)=80; AOTU063b(Glu)=68
Q4 DN DNp07 right entrada_total=4061 inhibitoria=1495 (36.8%) de_las_neuronas_del_motivo=138 (3.4%) de_tipos_LC4_LPLC2_LPLC4=638 (15.7%) presinapticas=492
Q4 DN DNp07 right top_inhibitorias PLP214(Glu)=201; CB0442(GABA)=160; SAD072(GABA)=99; AOTU049(GABA)=90; CL128a(GABA)=81
# duracion_s=7.2
EXIT_RUN=0
e6785f89b1a71d34c4b9eb39f9ac1aa6  run.log
```

### Corrida 2: inhibicion_visual_q5.py

```plain
cd /workspace/dcmt_2026-10-12 && md5sum inhibicion_visual_q5.py && (python3 inhibicion_visual_q5.py > q5.log 2>&1 || echo FALLO_PYTHON) && cat q5.log && md5sum q5.log
```

Exit 0. Salida completa:

```plain
c2e5719c0bea041b825c6a4335a24222  inhibicion_visual_q5.py
# maquina: 6c09d8604b07 | Linux-4.19.0-27-amd64-x86_64-with-glibc2.41 | Python 3.12.14 | numpy 2.5.3 | pandas 3.0.5 | pyarrow 25.0.1
# md5 script = c2e5719c0bea041b825c6a4335a24222
# fecha: 2026-10-12 18:41:26 +0000
# md5 conn = 3d802fd542b5d18570ba1ba0bb0abed9 | md5 annot = 719904abad876c68ace1b5690c9b9b63
DN=4 VISUALES_LC4_LPLC2_LPLC4=424
INHIBITORIAS_PRESINAPTICAS_A_LAS_4_DN=551 sinapsis=7889
Q5 umbral_vis>=1 DN DNp01 left inhibitoria=2227 de_inhibitorias_con_entrada_visual=1287 (57.8%) neuronas=72
Q5 umbral_vis>=1 DN DNp01 right inhibitoria=2495 de_inhibitorias_con_entrada_visual=1550 (62.1%) neuronas=72
Q5 umbral_vis>=1 DN DNp07 left inhibitoria=1672 de_inhibitorias_con_entrada_visual=968 (57.9%) neuronas=86
Q5 umbral_vis>=1 DN DNp07 right inhibitoria=1495 de_inhibitorias_con_entrada_visual=762 (51.0%) neuronas=82
Q5 umbral_vis>=1 TAMANO_MOTIVO_AMPLIADO 28 + 237 inhibitorias = 265 neuronas
Q5 umbral_vis>=5 DN DNp01 left inhibitoria=2227 de_inhibitorias_con_entrada_visual=923 (41.4%) neuronas=47
Q5 umbral_vis>=5 DN DNp01 right inhibitoria=2495 de_inhibitorias_con_entrada_visual=1223 (49.0%) neuronas=51
Q5 umbral_vis>=5 DN DNp07 left inhibitoria=1672 de_inhibitorias_con_entrada_visual=723 (43.2%) neuronas=65
Q5 umbral_vis>=5 DN DNp07 right inhibitoria=1495 de_inhibitorias_con_entrada_visual=633 (42.3%) neuronas=55
Q5 umbral_vis>=5 TAMANO_MOTIVO_AMPLIADO 28 + 167 inhibitorias = 195 neuronas
Q5 umbral_vis>=20 DN DNp01 left inhibitoria=2227 de_inhibitorias_con_entrada_visual=676 (30.4%) neuronas=32
Q5 umbral_vis>=20 DN DNp01 right inhibitoria=2495 de_inhibitorias_con_entrada_visual=685 (27.5%) neuronas=32
Q5 umbral_vis>=20 DN DNp07 left inhibitoria=1672 de_inhibitorias_con_entrada_visual=610 (36.5%) neuronas=47
Q5 umbral_vis>=20 DN DNp07 right inhibitoria=1495 de_inhibitorias_con_entrada_visual=557 (37.3%) neuronas=39
Q5 umbral_vis>=20 TAMANO_MOTIVO_AMPLIADO 28 + 112 inhibitorias = 140 neuronas
Q5 TOP_INHIBITORIA CB0442 (gaba, right) a_las_DN=271 entrada_desde_LC4_LPLC2_LPLC4=0 de 1952 (0.0%)
Q5 TOP_INHIBITORIA PLP214 (glutamate, left) a_las_DN=227 entrada_desde_LC4_LPLC2_LPLC4=109 de 2463 (4.4%)
Q5 TOP_INHIBITORIA PLP214 (glutamate, right) a_las_DN=201 entrada_desde_LC4_LPLC2_LPLC4=70 de 2352 (3.0%)
Q5 TOP_INHIBITORIA CB3707 (gaba, left) a_las_DN=173 entrada_desde_LC4_LPLC2_LPLC4=0 de 870 (0.0%)
Q5 TOP_INHIBITORIA CB3707 (gaba, right) a_las_DN=162 entrada_desde_LC4_LPLC2_LPLC4=9 de 1032 (0.9%)
Q5 TOP_INHIBITORIA CB3707 (gaba, left) a_las_DN=154 entrada_desde_LC4_LPLC2_LPLC4=36 de 1048 (3.4%)
Q5 TOP_INHIBITORIA CB3707 (gaba, right) a_las_DN=144 entrada_desde_LC4_LPLC2_LPLC4=10 de 1117 (0.9%)
Q5 TOP_INHIBITORIA PVLP010 (glutamate, right) a_las_DN=137 entrada_desde_LC4_LPLC2_LPLC4=216 de 8923 (2.4%)
Q5 TOP_INHIBITORIA CB0442 (gaba, left) a_las_DN=130 entrada_desde_LC4_LPLC2_LPLC4=0 de 1948 (0.0%)
Q5 TOP_INHIBITORIA LHAD1g1 (gaba, left) a_las_DN=130 entrada_desde_LC4_LPLC2_LPLC4=885 de 17164 (5.2%)
Q5 TOP_INHIBITORIA LHAD1g1 (gaba, right) a_las_DN=124 entrada_desde_LC4_LPLC2_LPLC4=695 de 17574 (4.0%)
Q5 TOP_INHIBITORIA CB0563 (gaba, left) a_las_DN=115 entrada_desde_LC4_LPLC2_LPLC4=0 de 2148 (0.0%)
# duracion_s=3.8
EXIT_RUN=0
64e22cbb9890a73d17bf8cbd2cd40b21  q5.log
```

### Cotejo de lo commiteado contra lo corrido

En brain-env, los cuatro archivos bajados por `curl -sfL` desde `raw.githubusercontent.com/gatehot59-star/drosophila-fep-connectome/6ebe1f74e39af24dcf316c0b8690788a103063b5/...` y pasados por `md5sum`, contra los del taller. Exit 0:

```plain
d965ee12cd7bd0bece24eb0790274bb5  -
c2e5719c0bea041b825c6a4335a24222  -
e6785f89b1a71d34c4b9eb39f9ac1aa6  -
64e22cbb9890a73d17bf8cbd2cd40b21  -
d965ee12cd7bd0bece24eb0790274bb5  chequeo_dcmt.py
c2e5719c0bea041b825c6a4335a24222  inhibicion_visual_q5.py
e6785f89b1a71d34c4b9eb39f9ac1aa6  run.log
64e22cbb9890a73d17bf8cbd2cd40b21  q5.log
```

4/4 iguales.

### Aritmética derivada (sandbox de ClickUp, desde los logs)

```plain
GLU_REGLA neuronas 15.84% aristas 18.75% sinapsis 17.00%
DISCREPANCIA_top_nt_vs_signo neuronas 3079 sinapsis 412571 0.76%
motivo sinapsis a las DN 539 de 18191 2.96%
inhibitorias totales a las DN 7889 de 18191 43.37%
```

## 5. Qué propongo (decide Abraham; nada corrido)

1. **Líneas etiquetadas** (diseño de la 008, sin cambios): cada descendente con su umbral dispara una acción, sin lector entrenado, contra SL y T. Prueba el embudo como lo usa la mosca. **No cambia la neurona.**
2. **Motivo ampliado con su inhibición** (nuevo): las 28 más las 167 inhibitorias con ≥ 5 sinapsis desde LC4, LPLC2 o LPLC4 (195 neuronas), la tarea de la 005, SL y T, con la neurona actual (τ fija y líquida plena). Hipótesis: el cableado paga cuando el recorte trae la inhibición de sus descendentes. **Falsador:** W ampliado no le gana a SL ampliado con Holm. **Riesgo declarado:** esas inhibitorias reciben ≤ 5,2% de su entrada desde estas visuales, así que en una tarea sólo visual pueden quedar casi sin manejo y empatar por construcción; habría que darles su entrada de fondo o ampliar un salto más (tamaño NO MEDIDO).
3. **Recién si la 2 muestra que la inhibición importa, DCMT-lite:** dos compartimentos por neurona (E e I, cada uno con su no linealidad) más la líquida plena, contra la neurona puntual con **los mismos parámetros**, en el motivo ampliado, con SL y T corriendo la misma neurona y el glutamato inhibitorio como Shiu. **Falsador doble:** no le gana a la puntual con los mismos parámetros, o no agranda la distancia W − SL.
4. **El estado de vuelo como ganancia, no como memoria.** En la mosca el vuelo prende la octopamina, que sube la ganancia visual mientras dura (Suver 2012): no se recuerda, se siente en continuo. Es la vía lenta de la DCMT puesta en su lugar: una señal por flujo que modula la ganancia (el ADR ya pone una DBC3 por flujo y nunca por neurona), alimentada por propiocepción y no por una pista que se apaga. La 004 ya mandó el estado de vuelo a lo clásico; esto le da su forma biológica.

## 6. Archivos generados

- `main`: este archivo.
- `titan/chequeo-dcmt-2026-10-12` (`6ebe1f7`): `tools/neurona_nueva/chequeo_dcmt.py`, `tools/neurona_nueva/inhibicion_visual_q5.py`, `results/chequeo_dcmt_2026-10-12/run.log` y `results/chequeo_dcmt_2026-10-12/q5.log`. md5 4/4 iguales entre lo commiteado y lo corrido.
- brain-env: `/workspace/dcmt_2026-10-12/` (los mismos cuatro).
- ClickUp: https://app.clickup.com/90171457413/docs/2kza6fw5-21497 (Space > Doc).
- `docs/agents/CONTEXTO-drosophila-fep.md` **no se reescribió** en este turno: el estado nuevo vive en este archivo, que es la respuesta más reciente. Queda para la próxima escritura del contexto.

## 7. NO MEDIDO

- Que el recorte sea la causa de que W no le gane a SL y T: es hipótesis; la decide la propuesta 2.
- La DCMT en cualquier forma, la DCMT-lite y las líneas etiquetadas (siguen en diseño).
- La fuente del signo del parquet para las 3.079 neuronas que no siguen su `top_nt`.
- Una tabla de sinapsis con coordenadas o por neuropilo: no está en el taller; tamaño y descarga, NO MEDIDOS.
- El código pegado: sólo lectura, no ejecutado.
- El 91% de Eon: anuncio de la empresa, sin verificación independiente.
- Las 166.000 neuronas y 125 millones de sinapsis que cita el análisis: no verificadas.
- El inventario de las tres máquinas: no re-medido hoy.

## Antes de firmar

```plain
"el motivo es el de la 003"                    -> 28/73/0 contra el conteo             -> sí, podía dar False -> medido, True
"el pipeline usa Glu inhibitorio"              -> cruce signo x top_nt                 -> sí                  -> medido: 21.863 de 24.804
"la DCMT invierte el 17% de las sinapsis"      -> conteo sobre el parquet              -> sí                  -> medido: 17,00% por Glu
"no hay dónde cae cada sinapsis"               -> lista de columnas                    -> sí                  -> medido; el filtro por subcadena NO podía (falso positivo "pos")
"el motivo trae 2,96% de la entrada de sus DN" -> suma sobre el parquet                -> sí                  -> medido
"la inhibición de las DN es visual"            -> Q5                                   -> sí                  -> medido parcial: 41-49% con >=5, pero <=5,2% de su propia entrada
"no es la neurona"                             -> 004, 005, 008, 013, 014 + literatura -> sí                  -> conclusión sobre corridas previas, no medición nueva
"con inhibición la mosca ganaría"              -> ninguno                              -> no                  -> NO MEDIDO
"la DCMT mejoraría algo"                       -> ninguno                              -> no                  -> NO MEDIDO
```

--- METODO PROMETEO ---
Acción delicada: NO (lectura de datos, rama nueva sin PR, bitácora; sin merge, sin PR #27, sin Zenodo)
Modo aplicado: LIGERO con medición (pregunta de rumbo; un rol)
Rúbrica: N/A (modo ligero)
Instrumento: chequeo_dcmt.py y inhibicion_visual_q5.py con pin md5 de datos; exit 0; salidas completas en §4 y en la rama
Maquina: brain-env (corridas) + sandbox de ClickUp (escritura y cotejo) + GitHub y web (lecturas)
Artefactos: docs/agents/respuestas/2026-10-12-011-no-es-la-neurona-es-el-recorte-y-la-dcmt-invierte-el-glutamato.md + https://app.clickup.com/90171457413/docs/2kza6fw5-21497
