# 2026-10-12-014: la auditoría de la 013 se equivoca en lo grave y acierta en lo útil; DNp06 recibe primero de LPLC1 y, en vuelo, las barras que pasan piden aterrizaje

**Doc espejo:** https://app.clickup.com/90171457413/docs/2kza6fw5-21557
**Rama:** `titan/chequeo-dcmt-2026-10-12`: medición `48feb7f` (script `tools/neurona_nueva/entradas_dn.py`, md5 `d67ffd0b9db8e88da57bf7b458745dd8`; log `results/chequeo_dcmt_2026-10-12/entradas_dn.log`, md5 `8082416f05901497da945395d5054ec1`, 106 líneas). Sin PR.

## Veredicto (conclusión)

- [MEDIDO] Las 67 sinapsis de diferencia en la entrada de DNp01 (003: 9.407; 011: 9.474) son de **4 neuronas presinápticas sin `cell_type`**. La exploración de la 003 sumó un agrupado por tipo, que en pandas descarta las claves nulas. Con ese filtro salen **exacto** los tres totales de la 003 (DNp01 9.407, DNp07 8.715, DNp10 9.480). La versión del parquet queda descartada por el pin md5.
- [MEDIDO] **DNp06 recibe primero de LPLC1** (1.023 sinapsis, 136 neuronas) y después de LPLC2 (1.003, 200). Agregar DNp06 «con sus LPLC2», como proponía la 013, dejaba afuera su primera entrada visual. DNp10 no tiene ninguna neurona de proyección visual entre sus 10 primeras entradas; LC13 no le da nada a ninguna de las cuatro descendentes; LPLC3 no existe como `cell_type` en v783.
- [LITERATURA] **Se acepta de la auditoría:** la octopamina abre DNp07 y no DNp10; sin vuelo DNp10 pierde todo disparo y DNp07 baja 70%; en vuelo una barra oscura de adelante hacia atrás pide aterrizaje, así que «lo que pasa» no tiene una sola etiqueta; las citas «Ache 2019» sin revista eran ambiguas; el banner del Doc de la 013 no tenía etiquetas.
- [LITERATURA] **Se rechaza:** el «error de primer orden» (la 013 ya decía «en vuelo: DNp07 → aterrizaje»); que barra contra punto explique Klapoetke contra Kim (Klapoetke 2022 movió rectángulos de 2 a 90 grados y LPLC2 casi no respondió); atribuir a Ache 2019 Current Biology el despegue posado y el aterrizaje en vuelo; dar por medido que la fibra gigante no opera en vuelo; mover la tabla a §0 (la 012 ya lo rechazó por F-01); el marco «la 013 corrige que LPLC2 no responde»; y sus propias etiquetas [MEDIDO] sobre lecturas de código.
- [CONCLUSIÓN] La tarea corregida necesita **cinco etiquetas**, no tres. Y la 005 tenía un desajuste más: su «acercamiento → aterrizar» en vuelo es un looming lateral, que en la mosca pide sacada.

## 1. Pedido

18:20: Abraham pega una auditoría externa de la 013 con «versión mejorada».

## 2. Herramientas y máquina

- **Web (sólo lectura):** Ache 2019, Nature Neuroscience 22:1132-1139 (texto completo en PMC7444277 y leyendas de las figuras suplementarias 4, 10 y 11 en nature.com); Klapoetke 2022, Neuron 110:1700-1711 (texto del PDF ampliado); Kim 2023, Current Biology 33:321-335; von Reyn 2017, Neuron (resumen); Shinomiya 2022, Current Biology; Klapoetke 2017, Nature (resumen).
- **brain-env:** `entradas_dn.py`, sólo lectura de los datos pinneados (4,3 s, `EXIT_RUN=0`).
- **Sandbox de ClickUp:** escritura del script (AST OK) y reconstrucción del log para subirlo (md5 igual al de brain-env).
- **GitHub MCP:** push `48feb7f` a `titan/chequeo-dcmt-2026-10-12`; lectura de la 003 y la 012; búsqueda de código «linealidad» en el repo (0 resultados, búsqueda marcada incompleta); este archivo a `main`.
- **ClickUp:** Doc público nuevo https://app.clickup.com/90171457413/docs/2kza6fw5-21557 y un aviso en el Doc de la 013. Actions y Kaggle sin uso; sin cuota ajena.

## 3. Qué se midió

### 3.1 La auditoría, punto por punto

| Punto de la auditoría | Qué dicen las fuentes | Veredicto |
|---|---|---|
| 2.1 «Error de primer orden»: la 013 implica que DNp07 no opera en vuelo | El Doc y el git de la 013 escriben «en vuelo: DNp06 → giro hacia el otro lado, DNp07 → aterrizaje»; la 005 ya etiquetaba «vuelo: acercamiento → aterrizar» y la 012 leía DNp07 «si vuela» | Se rechaza la forma. Se acepta el fondo: en vuelo una barra oscura de adelante hacia atrás pide aterrizaje |
| 2.2 «Pasa en vuelo → giro» cruza condiciones | Kim 2023 mide la conducta en vuelo («We placed a tethered, flying fly»); la respuesta de LPLC2 la registra «in tethered, non-flying animals» | A medias: la etiqueta está medida en vuelo; la entrada de LPLC2 no, y eso ya estaba en NO MEDIDO |
| 2.3 Barra contra punto explica Klapoetke contra Kim | Klapoetke 2022 movió «individual dark rectangular objects of different heights and widths (systematically varied from 2 to 90 in both dimensions) across a single cell's entire receptive field», y «LPLC2 and LC17 exhibited minimal responses to object motion stimuli» | Se rechaza: el tamaño no lo explica. Candidato sin medir: «we tested only one movement direction for each object size», y Kim encontró que LPLC2 prefiere lo que va de atrás hacia adelante |
| 2.4 Dendritas en cruz de LPLC2 | Klapoetke 2017: cada brazo en una capa de la placa lobular, con inhibición local para el movimiento hacia adentro. Shinomiya 2022: «LPLC2, the only neuron found to receive inputs from all T4/T5 subtypes» | Se acepta como contexto: la no linealidad está en LPLC2, antes de las descendentes, coherente con la 011. «La no linealidad está antes, en los detectores» no es cita de Ache 2019; como paráfrasis cuadra con von Reyn 2017 («linear integration of these two features within the GF») |
| 2.5 Las dos Ache 2019 mezcladas | La 013 decía «Ache 2019» sin revista en dos lugares | Se acepta. Pero la versión mejorada mezcla peor: atribuye a Current Biology «el despegue es posada, el aterrizaje es en vuelo» y «DNp01 opera en vuelo: FALSA», que salen de Nature Neuroscience |
| 2.5 La octopamina abre DNp07 | «DNp07 more than doubled its average non-flight visual response after OA application»; «In contrast, OA application had no effect on DNp10 visual responses» | Se acepta |
| 2.1 DNp07 y DNp10 «sólo» responden en vuelo | «Supra-threshold visual responses were completely eliminated without flight in DNp10 for all visual stimuli tested»; DNp07, «70% reduction in spike rate, from 92 to 27 Hz» | Para DNp10 sí. Para DNp07 se corrige: baja, no desaparece |
| §0 «DNp01 opera en vuelo para escape: FALSA» | «Though not directly measured here, descending neurons for escape may be gated out during flight» | Se rechaza como medido: lo medido es que en vuelo no hay despegue |
| 2.6 Las 67 sinapsis: versión del parquet, filtro o recíprocas | La 003 y la 011 corren sobre el mismo md5 de datos | Versión descartada; causa medida (3.2). Tampoco bloqueaba la tabla de la 011: su script está commiteado |
| 3.1 Tabla de falsación a §0, «regresión» | La 012 rechazó ese orden («el veredicto va primero por F-01»); la 013 no tiene esa tabla en §3, la tiene al final como manda el contrato | Se rechaza |
| 3.2 Veredicto sin etiquetas | El git de la 013 tiene [LITERATURA], [MEDIDO] y [CONCLUSIÓN]; el banner del Doc no | Se acepta para el Doc |
| 3.3 Falsador si DNp07 responde a lo que pasa | «silencing DNp07 or DNp10 using either line significantly reduced landing response rates to unilateral, front-to-back moving bars» | Se acepta y pasa a etiqueta: barra de adelante hacia atrás en vuelo → aterrizaje |
| I. «Su función es corregir la hipótesis de que LPLC2 no responde» | La 005 suponía que sí responde (`F_PUNTO = 0.6`) | Se rechaza: la 013 verificó ese supuesto |
| Etiquetas [MEDIDO] de la versión mejorada | «El 0,6 de la 005» y «la tarea contradice a la mosca» salen de leer código y papers | Se rechaza: son CONCLUSIÓN |
| Tabla de etiquetas: «en vuelo, looming → aterrizaje (DNp07/DNp10)» | «in flying flies, frontal looming stimuli elicit a landing response, whereas lateral looming stimuli drive an evasive saccade» | Se corrige: depende de frontal o lateral; y DNp10 no tiene neuronas de proyección visual entre sus 10 primeras entradas |

### 3.2 FlyWire v783 (`entradas_dn.py`)

| | DNp01 | DNp06 | DNp07 | DNp10 |
|---|---|---|---|---|
| Entrada total (todas las aristas) | 9.474 | 21.954 | 8.717 | 9.504 |
| Sin presinápticas sin `cell_type` | 9.407 | 21.803 | 8.715 | 9.480 |
| Total de la exploración de la 003 | 9.407 | sin dato | 8.715 | 9.480 |
| Presinápticas sin `cell_type` | 4 (67 sinapsis) | 12 (151) | 2 (2) | 6 (24) |
| Fracción inhibitoria | 49,8% | 30,5% | 36,3% | 38,3% |
| Primera entrada | LPLC2 1.080 (189) | LPLC1 1.023 (136) | LPLC4 1.448 (92) | PS088 528 (2, GABA) |
| Segunda entrada | LC4 805 (104) | LPLC2 1.003 (200) | LTe64 727 (14) | PS058 329 (2) |
| De LPLC1 / LC13 / LPLC3 | 0 / 0 / 0 | 1.023 / 0 / 0 | 0 / 0 / 0 | 0 / 0 / 0 |

Ningún otro filtro reproduce la 003: con `top_nt` presente, sin autapsis, sin presinápticas del mismo tipo o sólo con presinápticas anotadas sale el total completo; con lado izquierdo o derecho sale menos (DNp01 9.249). La fracción inhibitoria de DNp01 (49,8%) cuadra con la 011: 2.227 + 2.495 sobre 9.474 = 49,84%.

### 3.3 Cómo quedan las etiquetas

| Estado | Estímulo | Qué hace la mosca | Fuente | Descendente en FlyWire | ¿En el motivo? |
|---|---|---|---|---|---|
| Posada | Looming | Despega | Ache 2019, Nat Neurosci | DNp01 (LPLC2 1.080, LC4 805) | Sí |
| Posada | Objeto que pasa | Sin fuente | Ninguna | Sin dato | Etiqueta de trabajo «nada», declarada |
| En vuelo | Punto chico que se traslada | Gira para alejarse | Kim 2023 | DNp06 (LPLC1 1.023, LPLC2 1.003) | No: agregar con LPLC1 y LPLC2 |
| En vuelo | Looming lateral | Sacada evasiva | Ache 2019, Nat Neurosci; Kim 2023 | DNp06 | No |
| En vuelo | Looming frontal o barra oscura de adelante hacia atrás | Aterriza | Ache 2019, Nat Neurosci | DNp07 (LPLC4 1.448); DNp10 sin visuales entre sus 10 primeras | Sí (DNp07) |

La 005 presenta todo de un lado (`drive` sólo en el canal de `lado`), así que su «acercamiento → aterrizar» en vuelo es un looming lateral. El aterrizaje necesita un estímulo frontal (los dos lados a la vez) o una barra de adelante hacia atrás.

## 4. Evidencia cruda (verbatim)

Comando en brain-env y recibo:

```text
cd /workspace/dcmt_2026-10-12 && md5sum entradas_dn.py && (python3 entradas_dn.py > entradas_dn.log 2>&1 || echo FALLO_PYTHON) && cat entradas_dn.log && md5sum entradas_dn.log && wc -l entradas_dn.log
exit=0
d67ffd0b9db8e88da57bf7b458745dd8  entradas_dn.py
8082416f05901497da945395d5054ec1  entradas_dn.log
106 entradas_dn.log
```

Log completo (`results/chequeo_dcmt_2026-10-12/entradas_dn.log`):

```text
# maquina: 6c09d8604b07 | Linux-4.19.0-27-amd64-x86_64-with-glibc2.41 | numpy 2.5.3 | pandas 3.0.5
# md5 script = d67ffd0b9db8e88da57bf7b458745dd8
# fecha: 2026-10-12 21:26:00 +0000
# md5 conn = 3d802fd542b5d18570ba1ba0bb0abed9 | md5 annot = 719904abad876c68ace1b5690c9b9b63
ANNOT filas=139248 root_id_unicos=139248 cell_type_nulos=1528 top_nt_nulos=602
CUENTA tipo=LPLC3 por_lado={}
CUENTA tipo=LC13 por_lado={'left': 75, 'right': 70}
CUENTA tipo=LPLC1 por_lado={'right': 72, 'left': 68}
CUENTA tipo=LPLC2 por_lado={'left': 108, 'right': 102}
CUENTA tipo=LC4 por_lado={'left': 54, 'right': 50}
CUENTA tipo=LPLC4 por_lado={'left': 56, 'right': 54}
EXCITATORY valores=[-1, 1]
Q1 dn=DNp01 filtro=todas sinapsis=9474 aristas=962 difiere_003(+67)
Q1 dn=DNp01 filtro=pre_en_anotaciones sinapsis=9474 aristas=962 difiere_003(+67)
Q1 dn=DNp01 filtro=pre_con_cell_type sinapsis=9407 aristas=957 COINCIDE_003
Q1 dn=DNp01 filtro=pre_con_top_nt sinapsis=9474 aristas=962 difiere_003(+67)
Q1 dn=DNp01 filtro=pre_con_lado_left_right sinapsis=9249 aristas=934 difiere_003(-158)
Q1 dn=DNp01 filtro=sin_autapsis sinapsis=9474 aristas=962 difiere_003(+67)
Q1 dn=DNp01 filtro=sin_pre_del_mismo_tipo sinapsis=9474 aristas=962 difiere_003(+67)
Q1 dn=DNp01 filtro=suma_de_groupby_por_tipo_con_dropna sinapsis=9407 COINCIDE_003
Q1 dn=DNp01 pre_sin_cell_type sinapsis=67 neuronas=4
Q2 dn=DNp01 entrada_total=9474 presinapticas=862 inhibitoria=49.8%
Q2 dn=DNp01 top1 tipo=LPLC2 sinapsis=1080 (11.4%) neuronas=189 nt=acetylcholine
Q2 dn=DNp01 top2 tipo=LC4 sinapsis=805 (8.5%) neuronas=104 nt=acetylcholine
Q2 dn=DNp01 top3 tipo=CB3707 sinapsis=633 (6.7%) neuronas=4 nt=gaba
Q2 dn=DNp01 top4 tipo=DNp70 sinapsis=587 (6.2%) neuronas=2 nt=acetylcholine
Q2 dn=DNp01 top5 tipo=SAD014 sinapsis=292 (3.1%) neuronas=6 nt=gaba
Q2 dn=DNp01 top6 tipo=PVLP122b sinapsis=281 (3.0%) neuronas=4 nt=acetylcholine
Q2 dn=DNp01 top7 tipo=LHAD1g1 sinapsis=254 (2.7%) neuronas=2 nt=gaba
Q2 dn=DNp01 top8 tipo=PVLP010 sinapsis=250 (2.6%) neuronas=2 nt=glutamate
Q2 dn=DNp01 top9 tipo=CL038 sinapsis=249 (2.6%) neuronas=4 nt=glutamate
Q2 dn=DNp01 top10 tipo=CB0010 sinapsis=223 (2.4%) neuronas=2 nt=gaba
Q2 dn=DNp01 de=LPLC3 sinapsis=0 (0.0%) neuronas=0
Q2 dn=DNp01 de=LC13 sinapsis=0 (0.0%) neuronas=0
Q2 dn=DNp01 de=LPLC1 sinapsis=0 (0.0%) neuronas=0
Q1 dn=DNp06 filtro=todas sinapsis=21954 aristas=2114
Q1 dn=DNp06 filtro=pre_en_anotaciones sinapsis=21954 aristas=2114
Q1 dn=DNp06 filtro=pre_con_cell_type sinapsis=21803 aristas=2101
Q1 dn=DNp06 filtro=pre_con_top_nt sinapsis=21954 aristas=2114
Q1 dn=DNp06 filtro=pre_con_lado_left_right sinapsis=21451 aristas=2069
Q1 dn=DNp06 filtro=sin_autapsis sinapsis=21954 aristas=2114
Q1 dn=DNp06 filtro=sin_pre_del_mismo_tipo sinapsis=21954 aristas=2114
Q1 dn=DNp06 filtro=suma_de_groupby_por_tipo_con_dropna sinapsis=21803
Q1 dn=DNp06 pre_sin_cell_type sinapsis=151 neuronas=12
Q2 dn=DNp06 entrada_total=21954 presinapticas=1969 inhibitoria=30.5%
Q2 dn=DNp06 top1 tipo=LPLC1 sinapsis=1023 (4.7%) neuronas=136 nt=acetylcholine
Q2 dn=DNp06 top2 tipo=LPLC2 sinapsis=1003 (4.6%) neuronas=200 nt=acetylcholine
Q2 dn=DNp06 top3 tipo=LHAD1g1 sinapsis=823 (3.7%) neuronas=2 nt=gaba
Q2 dn=DNp06 top4 tipo=LC31a sinapsis=592 (2.7%) neuronas=33 nt=acetylcholine
Q2 dn=DNp06 top5 tipo=PVLP010 sinapsis=472 (2.1%) neuronas=2 nt=glutamate
Q2 dn=DNp06 top6 tipo=PVLP076 sinapsis=409 (1.9%) neuronas=2 nt=acetylcholine
Q2 dn=DNp06 top7 tipo=PVLP151 sinapsis=404 (1.8%) neuronas=4 nt=acetylcholine
Q2 dn=DNp06 top8 tipo=AN_AVLP_20 sinapsis=343 (1.6%) neuronas=2 nt=acetylcholine
Q2 dn=DNp06 top9 tipo=WED072 sinapsis=321 (1.5%) neuronas=6 nt=acetylcholine
Q2 dn=DNp06 top10 tipo=CL022 sinapsis=301 (1.4%) neuronas=6 nt=acetylcholine
Q2 dn=DNp06 de=LPLC3 sinapsis=0 (0.0%) neuronas=0
Q2 dn=DNp06 de=LC13 sinapsis=0 (0.0%) neuronas=0
Q2 dn=DNp06 de=LPLC1 sinapsis=1023 (4.7%) neuronas=136
Q1 dn=DNp07 filtro=todas sinapsis=8717 aristas=1048 difiere_003(+2)
Q1 dn=DNp07 filtro=pre_en_anotaciones sinapsis=8717 aristas=1048 difiere_003(+2)
Q1 dn=DNp07 filtro=pre_con_cell_type sinapsis=8715 aristas=1046 COINCIDE_003
Q1 dn=DNp07 filtro=pre_con_top_nt sinapsis=8717 aristas=1048 difiere_003(+2)
Q1 dn=DNp07 filtro=pre_con_lado_left_right sinapsis=8714 aristas=1045 difiere_003(-1)
Q1 dn=DNp07 filtro=sin_autapsis sinapsis=8717 aristas=1048 difiere_003(+2)
Q1 dn=DNp07 filtro=sin_pre_del_mismo_tipo sinapsis=8717 aristas=1048 difiere_003(+2)
Q1 dn=DNp07 filtro=suma_de_groupby_por_tipo_con_dropna sinapsis=8715 COINCIDE_003
Q1 dn=DNp07 pre_sin_cell_type sinapsis=2 neuronas=2
Q2 dn=DNp07 entrada_total=8717 presinapticas=934 inhibitoria=36.3%
Q2 dn=DNp07 top1 tipo=LPLC4 sinapsis=1448 (16.6%) neuronas=92 nt=acetylcholine
Q2 dn=DNp07 top2 tipo=LTe64 sinapsis=727 (8.3%) neuronas=14 nt=acetylcholine
Q2 dn=DNp07 top3 tipo=PLP214 sinapsis=428 (4.9%) neuronas=2 nt=glutamate
Q2 dn=DNp07 top4 tipo=CB0442 sinapsis=401 (4.6%) neuronas=2 nt=gaba
Q2 dn=DNp07 top5 tipo=LLPC3 sinapsis=289 (3.3%) neuronas=89 nt=acetylcholine
Q2 dn=DNp07 top6 tipo=PLP092 sinapsis=288 (3.3%) neuronas=2 nt=acetylcholine
Q2 dn=DNp07 top7 tipo=PLP245 sinapsis=236 (2.7%) neuronas=2 nt=acetylcholine
Q2 dn=DNp07 top8 tipo=CL128a sinapsis=176 (2.0%) neuronas=5 nt=gaba
Q2 dn=DNp07 top9 tipo=SAD072 sinapsis=166 (1.9%) neuronas=2 nt=gaba
Q2 dn=DNp07 top10 tipo=PS230,PLP242 sinapsis=162 (1.9%) neuronas=4 nt=acetylcholine
Q2 dn=DNp07 de=LPLC3 sinapsis=0 (0.0%) neuronas=0
Q2 dn=DNp07 de=LC13 sinapsis=0 (0.0%) neuronas=0
Q2 dn=DNp07 de=LPLC1 sinapsis=0 (0.0%) neuronas=0
Q1 dn=DNp10 filtro=todas sinapsis=9504 aristas=1370 difiere_003(+24)
Q1 dn=DNp10 filtro=pre_en_anotaciones sinapsis=9504 aristas=1370 difiere_003(+24)
Q1 dn=DNp10 filtro=pre_con_cell_type sinapsis=9480 aristas=1362 COINCIDE_003
Q1 dn=DNp10 filtro=pre_con_top_nt sinapsis=9504 aristas=1370 difiere_003(+24)
Q1 dn=DNp10 filtro=pre_con_lado_left_right sinapsis=9350 aristas=1350 difiere_003(-130)
Q1 dn=DNp10 filtro=sin_autapsis sinapsis=9504 aristas=1370 difiere_003(+24)
Q1 dn=DNp10 filtro=sin_pre_del_mismo_tipo sinapsis=9504 aristas=1370 difiere_003(+24)
Q1 dn=DNp10 filtro=suma_de_groupby_por_tipo_con_dropna sinapsis=9480 COINCIDE_003
Q1 dn=DNp10 pre_sin_cell_type sinapsis=24 neuronas=6
Q2 dn=DNp10 entrada_total=9504 presinapticas=1176 inhibitoria=38.3%
Q2 dn=DNp10 top1 tipo=PS088 sinapsis=528 (5.6%) neuronas=2 nt=gaba
Q2 dn=DNp10 top2 tipo=PS058 sinapsis=329 (3.5%) neuronas=2 nt=acetylcholine
Q2 dn=DNp10 top3 tipo=CB0344 sinapsis=255 (2.7%) neuronas=2 nt=gaba
Q2 dn=DNp10 top4 tipo=CB2885 sinapsis=253 (2.7%) neuronas=4 nt=glutamate
Q2 dn=DNp10 top5 tipo=AN_GNG_178 sinapsis=250 (2.6%) neuronas=6 nt=gaba
Q2 dn=DNp10 top6 tipo=CB3111 sinapsis=206 (2.2%) neuronas=6 nt=acetylcholine
Q2 dn=DNp10 top7 tipo=VES013 sinapsis=201 (2.1%) neuronas=2 nt=acetylcholine
Q2 dn=DNp10 top8 tipo=CB1350 sinapsis=184 (1.9%) neuronas=4 nt=acetylcholine
Q2 dn=DNp10 top9 tipo=CB2308 sinapsis=163 (1.7%) neuronas=4 nt=acetylcholine
Q2 dn=DNp10 top10 tipo=SLP222 sinapsis=163 (1.7%) neuronas=4 nt=acetylcholine
Q2 dn=DNp10 de=LPLC3 sinapsis=0 (0.0%) neuronas=0
Q2 dn=DNp10 de=LC13 sinapsis=0 (0.0%) neuronas=0
Q2 dn=DNp10 de=LPLC1 sinapsis=0 (0.0%) neuronas=0
# duracion_s=4.3
EXIT_RUN=0
```

Citas usadas (textuales):

```text
Ache 2019 NN: "Supra-threshold visual responses were completely eliminated without flight in DNp10 for all visual stimuli tested. In non-flight trials, DNp07 visual responses were reduced below the spike rates required to elicit leg movements in activation experiments (e.g. 70% reduction in spike rate, from 92 to 27 Hz, for 1000 °/s fast bars"
Ache 2019 NN: "DNp07 more than doubled its average non-flight visual response after OA application"
Ache 2019 NN: "In contrast, OA application had no effect on DNp10 visual responses"
Ache 2019 NN: "silencing DNp07 or DNp10 using either line significantly reduced landing response rates to unilateral, front-to-back moving bars"
Ache 2019 NN: "Ipsilateral, front-to-back moving dark bars drove both DN types most strongly. Contralateral stimuli, smaller moving objects, lateral looming, movements in other directions, and bright progressive edge motion were less effective"
Ache 2019 NN: "in flying flies, frontal looming stimuli elicit a landing response, whereas lateral looming stimuli drive an evasive saccade"
Ache 2019 NN, figura suplementaria 10: "Though not directly measured here, descending neurons for escape may be gated out during flight"
Klapoetke 2022: "we measured two-dimensional object size-tuning by moving individual dark rectangular objects of different heights and widths (systematically varied from 2 to 90 in both dimensions) across a single cell's entire receptive field"
Klapoetke 2022: "As most LC types were not motion direction selective, we tested only one movement direction for each object size"
Klapoetke 2022: "LPLC2 and LC17 exhibited minimal responses to object motion stimuli. This extreme selectivity was expected for LPLC2 due to strong inhibition for anything but centered looming"
Kim 2023: "We placed a tethered, flying fly at the center of a cylindrical LED display"
Kim 2023: "we imaged GCaMP signals of the axon terminals in the optic glomerulus for each VPN type, in tethered, non-flying animals"
Kim 2023: "We further characterized the visual response properties of spot-sensitive VPNs (LC11, LC13, LPLC1, and LPLC2)"
von Reyn 2017: "Motor program selection and timing emerge from linear integration of these two features within the GF."
Shinomiya 2022: "LPLC2, the only neuron found to receive inputs from all T4/T5 subtypes"
```

Recomputable: `git checkout 48feb7f && python3 tools/neurona_nueva/entradas_dn.py` con los datos pinneados en `/workspace` (sale con 2 si los md5 no son los del pin).

## 5. Propuesta (decide Abraham, nada corrido)

Rehacer la tarea con las cinco etiquetas de 3.3 antes de ampliar el motivo:

1. Agregar DNp06 de cada lado con sus LPLC1 y sus LPLC2, con el criterio de la 003 (las 4 con más sinapsis por lado y por tipo).
2. Tamaño y dirección del objeto explícitos; un estímulo frontal (los dos lados a la vez) para el aterrizaje.
3. LPLC2 al punto direccional (más de atrás hacia adelante), con amplitud barrida {0; 0,3; 0,6} declarada.
4. LPLC1 con variantes declaradas, como LPLC4 en la 005, porque su sintonía no está leída.
5. Mismos nulos SL y T, misma regla a mano, sellado antes de correr.

**Falsador:** con las etiquetas de la mosca, W no le gana a SL ni a T con Holm. Si eso pasa, el NO PAGA queda firme y ya no se le puede echar la culpa a la tarea.

## 6. Archivos

- `main`: este archivo.
- Rama `titan/chequeo-dcmt-2026-10-12` (`48feb7f`): `tools/neurona_nueva/entradas_dn.py` y `results/chequeo_dcmt_2026-10-12/entradas_dn.log`.
- ClickUp: Doc público https://app.clickup.com/90171457413/docs/2kza6fw5-21557 y aviso en el Doc de la 013.

## 7. NO MEDIDO

- La sintonía de LPLC1 (figuras 4F y 4G de Kim 2023, no leídas).
- Qué dirección usó Klapoetke 2022 para LPLC2, y por lo tanto si la dirección explica la diferencia con Kim.
- La relación punto/looming de LPLC2 (figura 4E de Kim) y LPLC2 en vuelo.
- LPLC3 bajo otro nombre en v783, y por dónde le llega la visión a DNp10 (sólo se miraron sus 10 primeras entradas y seis tipos visuales).
- La fibra gigante en vuelo; qué hace la mosca posada ante un objeto que pasa.
- La tarea corregida y el motivo ampliado: nada corrido.
- Segunda máquina. CONTEXTO sin reescribir: de la 011 a la 014 vive en sus respuestas.

## Antes de firmar

```text
"las 67 sinapsis son 4 neuronas sin tipo"      → 7 filtros contra los 3 totales de la 003 → podía dar rojo: SÍ (ninguno podía coincidir) → medido, coincide exacto en 3 de 3
"DNp06 recibe primero de LPLC1"                 → entradas_dn.py sobre v783               → podía dar rojo: SÍ                          → medido
"DNp10 sin visuales entre sus 10 primeras"      → top 10 de entradas                       → podía dar rojo: SÍ                          → medido, sólo top 10
"la octopamina abre DNp07, no DNp10"            → texto de Ache 2019 NN                    → podía dar rojo: SÍ                          → bien
"barra contra punto no explica la diferencia"   → texto de Klapoetke 2022 (2 a 90 grados) → podía dar rojo: SÍ                          → bien; la causa real NO MEDIDA
"el error de primer orden no existe"            → texto de la 013 (Doc y git)              → podía dar rojo: SÍ                          → bien
"en vuelo las barras de adelante hacia atrás piden aterrizaje" → silenciamiento en Ache 2019 NN → podía dar rojo: SÍ              → bien
"la tarea corregida le gana a SL y T"           → nada corrido                             → podía dar rojo: NO                          → NO MEDIDO
```

--- METODO PROMETEO ---
Acción delicada: NO
Máquina: brain-env (entradas_dn.py, 4,3 s, EXIT_RUN=0) + sandbox de ClickUp + GitHub y web
Artefactos: docs/agents/respuestas/2026-10-12-014-auditoria-de-la-013-lplc1-alimenta-a-dnp06-y-las-barras-piden-aterrizaje.md + https://app.clickup.com/90171457413/docs/2kza6fw5-21557
