# 2026-10-12-003 · Escape o aterrizaje según vuelo: el primer acople SparseLTC → DBC3 acierta el 100%, pero empata con LSTM y con el cableado barajado; lo que paga es tener memoria

**Fecha:** 2026-10-12, madrugada (America/Buenos_Aires).
**Base:** `main` en `1e88378` (2026-10-12-002). Datos pinneados: `connectivity.parquet` md5 `3d802fd542b5d18570ba1ba0bb0abed9`, `annotations.tsv` md5 `719904abad876c68ace1b5690c9b9b63` (`17fc577`).
**Instrumento:** rama `titan/escape-aterrizaje-2026-10-12`: `tools/escape_aterrizaje/escape_aterrizaje_dbc3.py` (md5 `4d40477d87406c31672acfb6e6e8f5a2`, pre-registro `d9f012d`) y `results/escape_aterrizaje_2026-10-12/run.log` (md5 `57789ead197c7dbef55840ecfb9edb37`, 72 líneas, `af4bea6`).
**Doc de ClickUp (público):** https://app.clickup.com/90171457413/docs/2kza6fw5-21337

## Veredicto

**El primer acople real SparseLTC → DBC3 funciona de punta a punta:** el motivo de la mosca corre en SparseLTC, DBC3 lee sólo las 4 descendentes y la señal de estado, y elige escapar o aterrizar bien en el **100% (1,0000 en 4/4 semillas)**. Instrumento VÁLIDO.

**Pero lo que paga es tener memoria, no DBC3 ni la mosca:**

- **H1 DBC3 contra LSTM con el mismo presupuesto: EMPATE** (LSTM 0,9990 a 1,0000; discordantes 6 contra 0, p 0,031, pero la semilla 0 empata exacto y la regla pre-registrada pide las 4).
- **H2 DBC3 contra lector sin memoria: MEJOR** (3.937 contra 0). Sin memoria se llega a 0,672, el techo teórico de quien no recuerda el estado (2/3).
- **H3 mosca contra 16 SL: W NO GANA** (SL 0,9997 a 1,0000; 14 de 16 igualan la media de W; p 0,38).
- **H4 DBC3 contra la regla a mano: MEJOR** (2.228 contra 0; la regla saca 0,8143). La regla es un rival flojo.

**Lectura:** la tarea quedó en el techo. Prueba la tubería, no separa DBC3 de LSTM ni la mosca de su barajado.

**Dos correcciones a la 002, medidas al armar el motivo:** DNp10 casi no recibe de las visuales de looming (LPLC4 22 de 9.480 sinapsis; LC4 y LPLC2 0); la vía visual del aterrizaje es LPLC4 → DNp07 (1.448). Y LC9 no le habla a DNp01 (0): sus 1.167 sinapsis van a DNp09. A DNp01 le entran sobre todo LPLC2 (1.080) y LC4 (805).

## 1. Pedido

Clic en «Correr escape o aterrizaje según vuelo, con DBC3» de la 002: las dos salidas en SparseLTC, DBC3 como compuerta con la señal «estoy volando», contra un rival clásico y contra su barajado.

## 2. Herramientas y máquina

- **brain-env** (Celeron N4020, Python 3.12.14, numpy 2.5.3, torch 2.14.1 CPU con 2 hilos): búsqueda de una implementación de DBC3 (`/workspace/dbc3_lib.py`, md5 `39566d9aea686b9a03310ccdd443bfd2`, notebook DBC3-v3 adaptado; y `/workspace/dbc3_motor.h`, md5 `6199c45246ad48e2ff4261654f705069`, «clean-room reconstruction» sin pesos, que no se usó); exploración de estructura del motivo antes de fijar (ρ, grados y entradas de DNp01, DNp07 y DNp10); dos humos de 15 iteraciones; la corrida completa (59,4 min) desde un clon fresco de la rama; verificación de md5 en otro clon fresco.
- **Sandbox de ClickUp:** escritura del script (no tiene torch; el humo se hizo en brain-env).
- **GitHub MCP:** rama nueva `titan/escape-aterrizaje-2026-10-12`; pre-registro `d9f012d`; log `af4bea6`; este archivo y el CONTEXTO en `main`.
- **ClickUp:** un Doc público nuevo y un aviso de corrección en el Doc de la 002. Actions y Kaggle sin uso; sin cuota ajena.
- **Humo:** el primero dio `CHEQUEO REPRODUCE ... -> False` porque el modelo se inicializaba antes de fijar la semilla. Se corrigió (semilla antes de construir) y el segundo dio True. El script sellado es el corregido.

## 3. Qué se midió

### 3.1 Diseño (fijado antes de correr)

- **Sujeto:** 28 neuronas. Por lado, las 4 LC4 y las 4 LPLC2 con más sinapsis sobre DNp01 y las 4 LPLC4 con más sinapsis sobre DNp07; DNp01 y DNp07 de cada lado. 73 aristas (665 sinapsis), 0 inhibitorias, 73 del mismo lado; ρ crudo 19,72, llevado a 0,9. DNp10 quedó afuera por la medición de arriba.
- **Motor:** SparseLTC con estado real, z ← (1 − t)·z + t·tanh(W·z + x), t = dt/τ, dt 0,02, τ fija heterogénea en [0,06; 0,18], sin entrenar.
- **Tarea (40 pasos):** pasos 0 a 2, señal de estado ±1 (volando o en el piso) que después se apaga; desde un paso al azar entre 15 y 25, looming por un lado (rampa de 8 pasos hasta 0,6 a 1,0) o un objeto que pasa sin acercarse (0,3 a 0,7, alternando de lado cada 4 pasos); ruido 0,15. Clases: 0 nada, 1 escapar de la izquierda, 2 escapar de la derecha, 3 aterrizar. Seis condiciones balanceadas; 4.096 de entrenamiento y 3.000 de prueba con semillas distintas.
- **Lectores (ven sólo las 4 descendentes y la señal):** DBC3 con las ecuaciones de `DBC3Motor` (h_m 20, h_r 36; 4.696 parámetros); LSTM h 30 (4.564); sin memoria (644, control negativo); regla a mano con umbral calibrado en entrenamiento. Adam 3e-3 coseno, 400 iteraciones de 256, pérdida en los 5 últimos pasos, prueba en el último.
- **Barajado SL:** permutación de destinos dentro de cada bloque de lado; conserva grado de entrada y de salida de cada neurona y el lado de cada arista. 16 redes, cada una con DBC3.
- **Controles:** sin memoria ≤ 0,75 y DBC3 − sin memoria ≥ 0,10; regla a mano ≥ 0,80; guarda SL; reproduce.

### 3.2 Resultados

| Lector | Acierto | Por clase (nada, esc. izq., esc. der., aterrizar) |
|---|---|---|
| DBC3, semillas 0 a 3 | 1,0000 × 4 | 1,000 en todas |
| LSTM, semillas 0 a 3 | 1,0000; 0,9997; 0,9993; 0,9990 | ≥ 0,996 |
| Sin memoria | 0,6730; 0,6717; 0,6710; 0,6720 | aterrizar 0,167 a 0,205 |
| Regla a mano | 0,8143 | 0,618; 0,848; 0,996; 0,903 |
| DBC3 sobre 16 SL | 0,9997 a 1,0000 | (14 en 1,0000) |

La regla a mano sobre las SL va de 0,6553 a 0,9330 (sobre W, 0,8143): con esa lectura fija, el cableado de la mosca queda en el medio de sus barajados.

## 4. Evidencia cruda (verbatim)

Comando (brain-env, desde el clon fresco de `d9f012d`):

```text
python3 tools/escape_aterrizaje/escape_aterrizaje_dbc3.py --conn /workspace/connectivity.parquet --annot /workspace/annotations.tsv --out results/escape_aterrizaje_2026-10-12
RC=0
```

Líneas 1 a 4 y 33 a 72 de `run.log` (md5 `57789ead197c7dbef55840ecfb9edb37`; las líneas 5 a 32 listan las 28 neuronas por `root_id`):

```text
# maquina: 6c09d8604b07 | Linux-4.19.0-27-amd64-x86_64-with-glibc2.41 | Python 3.12.14 | numpy 2.5.3 | torch 2.14.1+cu130
# md5 script = 4d40477d87406c31672acfb6e6e8f5a2
# fecha: 2026-10-12 03:57:23 +0000
# md5 conn = 3d802fd542b5d18570ba1ba0bb0abed9 | md5 annot = 719904abad876c68ace1b5690c9b9b63
MOTIVO neuronas=28 aristas=73 sinapsis=665 inhibitorias=0 ipsilaterales=73 rho_crudo=19.7206
PARAMS DBC3=4696 LSTM(h=30)=4564 SIN_MEMORIA=644
W lector=DBC3 semilla=0 acierto=1.0000 por_clase(nada,esc_izq,esc_der,aterr)=1.000,1.000,1.000,1.000
W lector=DBC3 semilla=1 acierto=1.0000 por_clase(nada,esc_izq,esc_der,aterr)=1.000,1.000,1.000,1.000
W lector=DBC3 semilla=2 acierto=1.0000 por_clase(nada,esc_izq,esc_der,aterr)=1.000,1.000,1.000,1.000
W lector=DBC3 semilla=3 acierto=1.0000 por_clase(nada,esc_izq,esc_der,aterr)=1.000,1.000,1.000,1.000
W lector=LSTM semilla=0 acierto=1.0000 por_clase(nada,esc_izq,esc_der,aterr)=1.000,1.000,1.000,1.000
W lector=LSTM semilla=1 acierto=0.9997 por_clase(nada,esc_izq,esc_der,aterr)=1.000,1.000,0.998,1.000
W lector=LSTM semilla=2 acierto=0.9993 por_clase(nada,esc_izq,esc_der,aterr)=1.000,0.996,1.000,1.000
W lector=LSTM semilla=3 acierto=0.9990 por_clase(nada,esc_izq,esc_der,aterr)=1.000,1.000,0.998,0.998
W lector=SIN_MEMORIA semilla=0 acierto=0.6730 por_clase(nada,esc_izq,esc_der,aterr)=0.998,0.834,0.798,0.205
W lector=SIN_MEMORIA semilla=1 acierto=0.6717 por_clase(nada,esc_izq,esc_der,aterr)=1.000,0.768,0.892,0.185
W lector=SIN_MEMORIA semilla=2 acierto=0.6710 por_clase(nada,esc_izq,esc_der,aterr)=0.998,0.850,0.846,0.167
W lector=SIN_MEMORIA semilla=3 acierto=0.6720 por_clase(nada,esc_izq,esc_der,aterr)=1.000,0.766,0.860,0.203
CHEQUEO REPRODUCE DBC3 semilla=0 -> True
W lector=REGLA_A_MANO umbral=0.8564 acierto=0.8143 por_clase=0.618,0.848,0.996,0.903
SL k=0 guarda=True lector=DBC3 acierto=1.0000 regla_a_mano=0.8517
SL k=1 guarda=True lector=DBC3 acierto=1.0000 regla_a_mano=0.7863
SL k=2 guarda=True lector=DBC3 acierto=1.0000 regla_a_mano=0.6593
SL k=3 guarda=True lector=DBC3 acierto=1.0000 regla_a_mano=0.7000
SL k=4 guarda=True lector=DBC3 acierto=0.9997 regla_a_mano=0.7750
SL k=5 guarda=True lector=DBC3 acierto=0.9997 regla_a_mano=0.6870
SL k=6 guarda=True lector=DBC3 acierto=1.0000 regla_a_mano=0.8437
SL k=7 guarda=True lector=DBC3 acierto=1.0000 regla_a_mano=0.8277
SL k=8 guarda=True lector=DBC3 acierto=1.0000 regla_a_mano=0.8417
SL k=9 guarda=True lector=DBC3 acierto=1.0000 regla_a_mano=0.9180
SL k=10 guarda=True lector=DBC3 acierto=1.0000 regla_a_mano=0.6553
SL k=11 guarda=True lector=DBC3 acierto=1.0000 regla_a_mano=0.6697
SL k=12 guarda=True lector=DBC3 acierto=1.0000 regla_a_mano=0.8310
SL k=13 guarda=True lector=DBC3 acierto=1.0000 regla_a_mano=0.9330
SL k=14 guarda=True lector=DBC3 acierto=1.0000 regla_a_mano=0.7413
SL k=15 guarda=True lector=DBC3 acierto=1.0000 regla_a_mano=0.8333
H1_DBC3_vs_LSTM discordantes 6 contra 0 p=0.0312 -> EMPATE
H2_DBC3_vs_SIN_MEMORIA discordantes 3937 contra 0 p=0 -> MEJOR
H4_DBC3_vs_REGLA_A_MANO discordantes 2228 contra 0 p=0 -> MEJOR
H3_W_vs_SL DBC3 W media=1.0000 SL media=1.0000 max=1.0000 igualan=14/16 U=36.0 p=0.3752 -> W NO GANA
CHEQUEO INSTRUMENTO control_negativo(sin_memoria<=0.75 y DBC3-sin_memoria>=0.10)=True control_positivo(regla_a_mano>=0.80)=True guarda_SL=True reproduce=True -> VALIDO
escrito resultados.json md5=9f7a668facbb67e4e952e70665c20aac
# duracion_s=3562.7
EXIT_RUN=0
```

Verificación en otro clon fresco de `af4bea6`:

```text
57789ead197c7dbef55840ecfb9edb37  /tmp/fc3/results/escape_aterrizaje_2026-10-12/run.log
4d40477d87406c31672acfb6e6e8f5a2  /tmp/fc3/tools/escape_aterrizaje/escape_aterrizaje_dbc3.py
```

Entradas medidas a DNp01, DNp07 y DNp10 (sinapsis con ≥ 1, todos los tipos presinápticos; exploración en brain-env antes de fijar el motivo):

```text
DNp01 9407 {'LC4': 805, 'LPLC2': 1080, 'LPLC4': 0, 'LC6': 0, 'LC9': 0}
DNp07 8715 {'LC4': 1, 'LPLC2': 0, 'LPLC4': 1448, 'LC6': 0, 'LC9': 0}
DNp10 9480 {'LC4': 0, 'LPLC2': 0, 'LPLC4': 22, 'LC6': 0, 'LC9': 0}
```

Recomputable: `git checkout titan/escape-aterrizaje-2026-10-12 && python3 tools/escape_aterrizaje/escape_aterrizaje_dbc3.py --conn <parquet> --annot <tsv> --out <dir>` (pide torch y scipy). Con otros datos sale con 2.

## 5. Archivos generados

- **Rama `titan/escape-aterrizaje-2026-10-12`:** el script (`d9f012d`) y `results/escape_aterrizaje_2026-10-12/run.log` (`af4bea6`). `resultados.json` (md5 `9f7a668facbb67e4e952e70665c20aac`) no se commitea: derivado y determinista; queda en brain-env en `/workspace/escater/clon/results/escape_aterrizaje_2026-10-12/`.
- **`main`:** este archivo y `docs/agents/CONTEXTO-drosophila-fep.md`.
- **ClickUp:** Doc público https://app.clickup.com/90171457413/docs/2kza6fw5-21337 y aviso de corrección en el Doc de la 002 (https://app.clickup.com/90171457413/docs/2kza6fw5-21317).

## 6. NO MEDIDO

- **Ventaja de DBC3 sobre LSTM** en una tarea fuera del techo (esperas largas, varias señales, menos presupuesto).
- **Ventaja del cableado** con una entrada que distinga a LPLC4 de LC4 y LPLC2: hoy las tres reciben el mismo estímulo, así que el cableado no podía importar para el lector entrenado.
- **Un rival clásico fuerte** (máquina de estados con mejores rasgos): la regla de hoy es floja.
- **DBC3 en C:** `dbc3_motor.h` reconstruido existe en brain-env (sin pesos) y no se usó; tampoco paridad con el `DBC3Motor` de torch.
- **La líquida** (ni nativa ni plena) en este motivo; condiciones fuera de las entrenadas; hardware; reproducción en una segunda máquina; review externo.

## Antes de firmar

```text
"el acople SparseLTC -> DBC3 funciona"  → DBC3 sobre las 4 descendentes        → podía dar rojo: SÍ (humo: 0,64 con 15 iteraciones) → medido, bien
"hace falta memoria"                    → lector sin memoria                   → podía dar rojo: SÍ (si 0,75 o más, INVALIDO)       → medido, bien (0,672)
"DBC3 le gana a LSTM"                   → McNemar por semilla                  → podía dar rojo: SÍ                                 → EMPATE
"el cableado de la mosca paga"          → 16 SL, Mann-Whitney                  → podía dar rojo: SÍ, pero la entrada no distingue tipos → NO GANA (sesgo hacia el empate, declarado)
"DBC3 le gana a lo clásico"             → regla a mano floja                   → rival débil                                         → MEJOR, sin valor contra un rival fuerte
```

## QA (TITAN FULL)

| Criterio | Puntaje | Evidencia |
|---|---|---|
| Completitud | 13/15 | Cuatro hipótesis, cuatro controles y las correcciones a la 002. −2: rival clásico flojo y entrada sin tipos |
| Ejecutabilidad | 15/15 | Exit 0 con VALIDO desde un clon fresco; md5 2/2 en otro clon; humo con el error de semilla detectado y corregido antes de sellar |
| Arquitectura del razonamiento | 8/10 | Pre-registro con regla de decisión y control negativo con techo teórico (2/3). −2: la tarea quedó en el techo y no discrimina |
| Documentación | 9/10 | Docstring con sujeto, tarea, brazos y códigos de salida. −1: stdout sin flush (el log aparece recién al final) |
| Innovación | 3/5 | Primer acople SparseLTC → DBC3 sobre cableado real con tarea de contexto biológica |
| Proceso QA | 4/5 | Cada fila con su línea de log. −1: sin review externo |
| Seguridad, Testing, DevOps | N/A (40) | Sin frontera de confianza; los controles del instrumento son la prueba; sin CI nuevo |

**52/60 → 87/100 sobre lo aplicable.** Aprobado con deuda: tarea fuera del techo, entrada con tipos, rival clásico fuerte y review.

--- METODO PROMETEO ---
Acción delicada: NO (bitácora y contexto a main; instrumento en titan/escape-aterrizaje-2026-10-12)
Modo aplicado:   TITAN FULL
Rúbrica:         52/60 -> 87/100
N/A declarados:  40 (Seguridad 15, Testing 15, DevOps 10)
Review externo:  no pedido: no hay PR (deuda)
Instrumento:     tools/escape_aterrizaje/escape_aterrizaje_dbc3.py (md5 4d40477d87406c31672acfb6e6e8f5a2 sellado en d9f012d); VALIDO; EXIT_RUN=0; run.log md5 57789ead197c7dbef55840ecfb9edb37 (72 líneas) en af4bea6; md5 2/2 en clon fresco
Máquina:         brain-env (Celeron N4020, torch 2.14.1 CPU), 59,4 min; sandbox de ClickUp para escribir el script
Artefactos:      docs/agents/respuestas/2026-10-12-003-escape-o-aterrizaje-con-dbc3.md + https://app.clickup.com/90171457413/docs/2kza6fw5-21337
