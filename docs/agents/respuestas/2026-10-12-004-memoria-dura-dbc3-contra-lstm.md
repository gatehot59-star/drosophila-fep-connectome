# 2026-10-12-004 · Memoria dura: con 120 pasos ni DBC3 ni LSTM aprenden a recordar si vuela; empatan entre sí y una máquina de estados de dos líneas les gana

**Fecha:** 2026-10-12, mañana (America/Buenos_Aires).
**Base:** `main` en `ee62321` (2026-10-12-003). Datos pinneados como en la 003.
**Instrumento:** rama `titan/memoria-dura-2026-10-12` (sale de `titan/escape-aterrizaje-2026-10-12`): `tools/escape_aterrizaje/memoria_dura.py` (md5 `c486e79f3fd78ee8034254a1499fbcbf`, pre-registro `f58cf8e`), que importa sin cambios `escape_aterrizaje_dbc3.py` (md5 `4d40477d87406c31672acfb6e6e8f5a2`); logs en `results/memoria_dura_2026-10-12/{chico,canonico}/run.log` (`0431f35`).
**Doc de ClickUp (público):** https://app.clickup.com/90171457413/docs/2kza6fw5-21357

## Veredicto

**Endurecida la memoria, ninguna de las dos redes aprendió a recordar el estado de vuelo.** Con 120 pasos, cambio de contexto en la mitad de los ensayos y pulsos de engaño, DBC3 y LSTM quedan entre 0,658 y 0,672 (una sola semilla de DBC3 llega a 0,743), contra un techo sin memoria de 2/3. Instrumento VÁLIDO en los dos presupuestos y ninguno quedó en el techo alto.

- **H1 DBC3 contra LSTM: EMPATE** en el canónico (1.153 contra 961, p 3,2e-05, pero no en las 4 semillas: el exceso es la semilla 2) y en el chico (1.344 contra 1.397, p 0,32).
- **H2 DBC3 contra sin memoria:** MEJOR por poco en el canónico (1.143 contra 854; las 4 semillas por encima, tres por menos de 0,005), EMPATE en el chico.
- **H3 DBC3 contra la máquina de estados: PEOR en los dos** (0,7663 para la máquina).

**Lectura:** con 400 pasadas de entrenamiento ninguna red cruza 90 pasos de espera; recordar un estado discreto es trabajo de lo clásico (regla de reparto de la 001). La ventaja de DBC3 en memoria diferida de sus benchmarks (esperas de 25 pasos) no se traslada a esta espera. Queda abierto si es cuestión de entrenamiento.

## 1. Pedido

Clic en «Endurecer la memoria: DBC3 contra LSTM» de la 003: esperas largas, varias señales y poco presupuesto, para separar DBC3 de LSTM fuera del techo.

## 2. Herramientas y máquina

- **brain-env** (Celeron N4020, torch 2.14.1 CPU): humo de 10 iteraciones con 512 de entrenamiento (VALIDO salvo el control positivo: máquina de estados 0,7833 < 0,80), ajuste del umbral del control positivo a 0,75 antes de sellar, y la corrida de los dos presupuestos en paralelo (un hilo cada uno) desde un clon fresco; verificación de md5 en otro clon fresco.
- **Sandbox de ClickUp:** escritura del script.
- **GitHub MCP:** rama `titan/memoria-dura-2026-10-12`; pre-registro `f58cf8e`; logs `0431f35`; este archivo y el CONTEXTO en `main`.
- **ClickUp:** un Doc público nuevo. Actions y Kaggle sin uso; sin cuota ajena.

## 3. Qué se midió

### 3.1 Diseño (fijado antes de correr)

- **Sujeto y motor:** los de la 003, importados sin cambios (28 neuronas, 73 aristas, SparseLTC con τ fija heterogénea sin entrenar); sólo `T` del módulo se lleva a 120.
- **Tarea:** señal fuerte ±1 en los pasos 0 a 2; con probabilidad 0,5, otra señal fuerte de signo contrario en un paso al azar entre 20 y 80 (vale la última); cuatro pulsos ±0,3 de un paso en lugares al azar; looming o paso entre los pasos 90 y 105. Clases y lectura como en la 003.
- **Presupuestos:** canónico (DBC3 h_m 20, h_r 36: 4.696; LSTM h 30: 4.564) y chico (h_m 8, h_r 12: 808; LSTM h 11: 840). Sin memoria: 644. Adam 3e-3 coseno, 400 iteraciones de 128.
- **Rival clásico:** máquina de estados que guarda la última señal con |c| > 0,5 y detecta y lateraliza con la regla de la 003.
- **Reglas:** H1 a H3 con McNemar por semilla (MEJOR o PEOR sólo si las 4 semillas van para el mismo lado y p < 0,05); bandera TECHO si DBC3 y LSTM promedian 0,99 o más. Controles: sin memoria ≤ 0,75; máquina de estados ≥ 0,75 (0,80 en la 003, bajado tras el humo y antes de correr, declarado en el commit de pre-registro); reproduce.

### 3.2 Resultados

| Lector | Canónico | Chico |
|---|---|---|
| DBC3 | 0,6607; 0,6580; 0,7430; 0,6593 (media 0,6803) | 0,6640; 0,6610; 0,6610; 0,6623 (media 0,6621) |
| LSTM | 0,6650; 0,6683; 0,6627; 0,6610 (media 0,6643) | 0,6713; 0,6723; 0,6643; 0,6580 (media 0,6665) |
| Sin memoria | 0,6563; 0,6570; 0,6567; 0,6547 | igual (mismo modelo y semillas) |
| Máquina de estados | 0,7663 | 0,7663 |

La máquina de estados pierde por la detección (su umbral sobre el pico de las descendentes), no por la memoria: guarda la última señal sin error por construcción.

## 4. Evidencia cruda (verbatim)

Comandos (brain-env, desde el clon fresco de `f58cf8e`, en paralelo):

```text
python3 tools/escape_aterrizaje/memoria_dura.py --conn /workspace/connectivity.parquet --annot /workspace/annotations.tsv --presupuesto canonico --out results/memoria_dura_2026-10-12/canonico
python3 tools/escape_aterrizaje/memoria_dura.py --conn /workspace/connectivity.parquet --annot /workspace/annotations.tsv --presupuesto chico --out results/memoria_dura_2026-10-12/chico
RC=0 (los dos)
```

`chico/run.log` (md5 `f71717b8cb50e0d1e894ee558733defe`), líneas 1 a 7 y 20 a 29:

```text
# maquina: 6c09d8604b07 | Linux-4.19.0-27-amd64-x86_64-with-glibc2.41 | Python 3.12.14 | numpy 2.5.3 | torch 2.14.1+cu130
# md5 script = c486e79f3fd78ee8034254a1499fbcbf
# md5 base escape_aterrizaje_dbc3.py = 4d40477d87406c31672acfb6e6e8f5a2 (pin 4d40477d87406c31672acfb6e6e8f5a2)
# fecha: 2026-10-12 08:32:51 +0000 | presupuesto=chico
MOTIVO neuronas=28 aristas=73 rho_crudo=19.7206 (igual que la 003)
TAREA T=120 cambia_contexto_train=0.506 test=0.494
PARAMS DBC3(h_m=8,h_r=12)=808 LSTM(h=11)=840 SIN_MEMORIA=644
CHEQUEO REPRODUCE DBC3 semilla=0 -> True
W lector=MAQUINA_DE_ESTADOS umbral=0.8907 acierto=0.7663 con_cambio=0.7684
H1_DBC3_vs_LSTM presupuesto=chico discordantes 1344 contra 1397 p=0.321 -> EMPATE
H2_DBC3_vs_SIN_MEMORIA presupuesto=chico discordantes 1182 contra 1111 p=0.144 -> EMPATE
H3_DBC3_vs_MAQUINA_DE_ESTADOS presupuesto=chico discordantes 2225 contra 3476 p=4.79e-62 -> PEOR
TECHO presupuesto=chico DBC3_media=0.6621 LSTM_media=0.6665 -> FUERA DEL TECHO
CHEQUEO INSTRUMENTO control_negativo(sin_memoria<=0.75)=True control_positivo(maquina_de_estados>=0.75)=True reproduce=True -> VALIDO
escrito resultados.json md5=b7c936dc581d01a8a18f794ac82e87ec
# duracion_s=1534.3
EXIT_RUN=0
```

`canonico/run.log` (md5 `5b85fc0e88676329481910009b353400`), líneas 7 a 11 y 20 a 29:

```text
PARAMS DBC3(h_m=20,h_r=36)=4696 LSTM(h=30)=4564 SIN_MEMORIA=644
W lector=DBC3 semilla=0 acierto=0.6607 con_cambio=0.6678 por_clase=1.000,0.773,0.798,0.209 seg=326
W lector=DBC3 semilla=1 acierto=0.6580 con_cambio=0.6766 por_clase=1.000,0.420,0.956,0.299 seg=313
W lector=DBC3 semilla=2 acierto=0.7430 con_cambio=0.7664 por_clase=1.000,0.783,0.358,0.653 seg=309
W lector=DBC3 semilla=3 acierto=0.6593 con_cambio=0.6597 por_clase=1.000,0.594,0.912,0.239 seg=328
CHEQUEO REPRODUCE DBC3 semilla=0 -> True
W lector=MAQUINA_DE_ESTADOS umbral=0.8907 acierto=0.7663 con_cambio=0.7684
H1_DBC3_vs_LSTM presupuesto=canonico discordantes 1153 contra 961 p=3.23e-05 -> EMPATE
H2_DBC3_vs_SIN_MEMORIA presupuesto=canonico discordantes 1143 contra 854 p=1.08e-10 -> MEJOR
H3_DBC3_vs_MAQUINA_DE_ESTADOS presupuesto=canonico discordantes 2215 contra 3248 p=1.47e-44 -> PEOR
TECHO presupuesto=canonico DBC3_media=0.6803 LSTM_media=0.6643 -> FUERA DEL TECHO
CHEQUEO INSTRUMENTO control_negativo(sin_memoria<=0.75)=True control_positivo(maquina_de_estados>=0.75)=True reproduce=True -> VALIDO
escrito resultados.json md5=580e1a0de25eec64eb3cfa7695131cce
# duracion_s=1814.7
EXIT_RUN=0
```

Verificación en otro clon fresco de `0431f35`:

```text
f71717b8cb50e0d1e894ee558733defe  /tmp/fc4/results/memoria_dura_2026-10-12/chico/run.log
5b85fc0e88676329481910009b353400  /tmp/fc4/results/memoria_dura_2026-10-12/canonico/run.log
c486e79f3fd78ee8034254a1499fbcbf  /tmp/fc4/tools/escape_aterrizaje/memoria_dura.py
```

Recomputable: `git checkout titan/memoria-dura-2026-10-12 && python3 tools/escape_aterrizaje/memoria_dura.py --conn <parquet> --annot <tsv> --presupuesto {canonico|chico} --out <dir>`.

## 5. Archivos generados

- **Rama `titan/memoria-dura-2026-10-12`:** el script (`f58cf8e`) y los dos `run.log` (`0431f35`). Los `resultados.json` (md5 `b7c936dc…` y `580e1a0d…`) no se commitean: derivados y deterministas; quedan en brain-env en `/workspace/memdura/results/memoria_dura_2026-10-12/`.
- **`main`:** este archivo y `docs/agents/CONTEXTO-drosophila-fep.md`.
- **Doc de ClickUp público:** https://app.clickup.com/90171457413/docs/2kza6fw5-21357

## 6. NO MEDIDO

- **Entrenamiento más largo** (2.000 pasadas o más) o por etapas (esperas cortas primero), y **esperas intermedias** (40 a 120 pasos) para ver dónde se rompe cada red. Sin eso no se puede separar «no puede» de «no llegó a aprender».
- **La máquina de estados con mejor detección:** hoy pierde por la detección de «nada», no por la memoria.
- Entrada por tipos visuales, la líquida, DBC3 en C y su paridad con torch, hardware, segunda máquina, review externo.

## Antes de firmar

```text
"ninguna red aprendió la memoria"     → acierto contra sin memoria (2/3)   → podía dar rojo: SÍ (en la 003 dio 1,0) → medido: 0,66 a 0,68
"DBC3 y LSTM empatan"                → McNemar por semilla, 2 presupuestos → podía dar rojo: SÍ                   → EMPATE en los dos
"lo clásico gana en esta memoria"    → máquina de estados                  → podía dar rojo: SÍ                   → PEOR para DBC3 en los dos
"no puede cruzar 90 pasos"           → ninguno (sólo 400 pasadas)          → NO MEDIDO: puede ser entrenamiento
```

## QA (TITAN FULL)

| Criterio | Puntaje | Evidencia |
|---|---|---|
| Completitud | 13/15 | Dos presupuestos, tres hipótesis, controles y bandera de techo. −2: un solo largo de entrenamiento y una sola espera |
| Ejecutabilidad | 15/15 | Exit 0 con VALIDO en los dos, desde un clon fresco; md5 3/3 en otro clon |
| Arquitectura del razonamiento | 8/10 | Reuso sin cambios del módulo de la 003 (mismo sujeto y motor) y pre-registro. −2: el control positivo se ajustó tras el humo (declarado) y la tarea no separa «no puede» de «no aprendió» |
| Documentación | 9/10 | Docstring y logs con flush. −1: el umbral ajustado vive en un comentario |
| Innovación | 2/5 | Tarea de cambio de contexto biológica sobre el acople real |
| Proceso QA | 4/5 | Cada fila con su línea de log. −1: sin review externo |
| Seguridad, Testing, DevOps | N/A (40) | Sin frontera de confianza; controles del instrumento como prueba; sin CI nuevo |

**51/60 → 85/100 sobre lo aplicable.** Aprobado con deuda: entrenamiento largo o por etapas, esperas intermedias y review.

--- METODO PROMETEO ---
Acción delicada: NO (bitácora y contexto a main; instrumento en titan/memoria-dura-2026-10-12)
Modo aplicado:   TITAN FULL
Rúbrica:         51/60 -> 85/100
N/A declarados:  40 (Seguridad 15, Testing 15, DevOps 10)
Review externo:  no pedido: no hay PR (deuda)
Instrumento:     tools/escape_aterrizaje/memoria_dura.py (md5 c486e79f3fd78ee8034254a1499fbcbf sellado en f58cf8e); VALIDO en los dos; EXIT_RUN=0; logs en 0431f35; md5 3/3 en clon fresco
Máquina:         brain-env (Celeron N4020, torch 2.14.1 CPU, 2 procesos de 1 hilo), 25,6 y 30,2 min; sandbox de ClickUp para escribir el script
Artefactos:      docs/agents/respuestas/2026-10-12-004-memoria-dura-dbc3-contra-lstm.md + https://app.clickup.com/90171457413/docs/2kza6fw5-21357
