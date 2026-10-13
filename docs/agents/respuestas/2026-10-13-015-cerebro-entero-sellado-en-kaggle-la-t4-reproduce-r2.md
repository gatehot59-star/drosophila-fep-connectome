# 2026-10-13-015 · El banco con el cerebro entero quedó sellado en Kaggle: la T4 reproduce exacto R2 y corre a 0,026 s por ensayo

## Veredicto

- **[MEDIDO] Sellado, sin disparar.** Rama `titan/factorial4-cerebro-entero-2026-10-13`, sello `431b7bd` (instrumento `ace8fe7`). Las 600 corridas del factorial 3 más 50 SL y 50 T, ahora con el **cerebro entero de FlyWire v783**: 138.639 neuronas, 15.091.983 aristas (6.032.681 inhibitorias) y las mismas 564 entradas de R2. Dos kernels T4 x2 de `abrahammendieta`, cuatro carriles, 22 trabajos.
- **[MEDIDO] Todos los controles VÁLIDOS** en brain-env (CPU) y en tres sesiones de Kaggle. **La T4 da 0,9465 en R2, el número exacto del factorial 3**, en cada una de las dos GPU. Torch y numpy coinciden a 4e-16 o menos en R1 y en el cerebro entero.
- **[MEDIDO] 0,0260 s por ensayo por T4**, igual con dos procesos a la vez. En brain-env, 3,2 s: unas 124 veces más lento.
- **[CONCLUSIÓN] La corrida completa lleva unas 3,6 h de reloj y unas 7 h de la cuota semanal de GPU.** Se dispara cuando Abraham lo pida.
- **[MEDIDO] Del cerebro entero en la tarea no hay ningún número con valor:** el humo usa 80 ensayos de prueba.
- La respuesta se demoró: el pedido de las 18:35 no tuvo contestación hasta acá (Abraham preguntó «Y» a las 19:56 y a las 20:42).

## Pedido

18:35: «Sella el banco con el cerebro entero en kaggle». 19:56 y 20:42: «Y».

## Herramientas y máquina

- **brain-env** (gateway MUDH, servicio `build`): humo en CPU de `cerebro_mosca.py` (modos verificar y grilla), prueba local del envoltorio con carriles, prueba del agregador, verificación del sello en clon fresco y prueba del parche del CONTEXTO. Escribió sólo en `/workspace/f4cerebro_2026-10-13/`.
- **Kaggle, cuenta `abrahammendieta`, GPU (gasta cuota de Abraham):** tres kernels privados de humo. `f4-ce-humo-t4-2026-10-13` (277,0 s), `f4-ce-humo-p100-2026-10-13` (270 s; Kaggle le dio T4 aunque se pidió P100) y `f4-ce-humo-carriles-2026-10-13` (150,7 s). Unos 12 min de sesión de GPU en total.
- **GitHub:** commits `ace8fe7` (candidato), `e2c2e1f` (sello) y `431b7bd` (un byte corregido) en la rama titan; este commit en `main`. Nada mergeado.
- **ClickUp:** el Doc de esta respuesta.

## Qué se midió

| control | brain-env CPU | Kaggle T4 (humo 1) | Kaggle «P100» (T4) | Kaggle carriles, GPU 0 / 1 |
|---|---|---|---|---|
| SUJETO_IGUAL_F2 (el armado nuevo da el R1 sellado) | True | True | True | True / True |
| PARIDAD_R1, 16 ensayos | 1,11e-16 | 3,33e-16 | 3,33e-16 | 2,78e-16 / 3,89e-16 |
| CE_tamano | True | True | True | True / True |
| PARIDAD_CE, 4 ensayos | 2,78e-17 | 1,25e-16 | 1,25e-16 | 9,71e-17 / 1,11e-16 |
| REPRO_R2 (factorial 3: 0,9465) | no pedido | 0,9465 | 0,9465 | 0,9465 / 0,9465 |
| s por ensayo, cerebro entero | 3,2160 (20) | 0,0262 (1000) | 0,0261 (1000) | 0,0260 / 0,0260 (1000) |
| memoria de GPU | - | 3,11 GB | 3,11 GB | 3,11 / 3,11 GB |

- **Sujeto CE** (igual en todas): 138.639 neuronas, 15.091.983 aristas, 6.032.681 inhibitorias, 564 entradas (LC4 54/50, LPLC2 108/102, LPLC4 56/54, LPLC1 68/72 por lado), contiene M46 y R1, radio crudo 2164,292802.
- **Humo de grilla** (80 ensayos, sin valor): W 0,9750, regla propia 0,9500, regla de 40 0,9250. **Idéntico en CPU y en las dos T4.**
- **Humo de nulos** (sin valor): SL k0 0,6250 (radio 1503,1147, 15.090.092 destinos cambiados); T k0 0,7625 (423 tipos cambiados); guardas True.
- **Concurrencia:** dos sesiones de Kaggle a la vez (23:19:26 a 23:24:03 y 23:19:29 a 23:23:59 UTC). Dos carriles a la vez en una sesión (los dos de 23:35:23 a 23:37:04), sin perder velocidad.
- **Envoltorio local:** con dos GPU simuladas los carriles corren en paralelo y el carril 0 sigue en serie (rc 0); sin GPU sale rc 6 sin correr.
- **Agregador: PASA 5/5.** El humo real da VÁLIDO; con un W tocado da INVÁLIDO por integridad. Tres sintéticos hechos con los json del factorial 3: igual a R2 da la primaria del factorial 3 exacta y la escala en 0 (EQUIVALENTE); con W + 0,02 da SUPERA en las dos; con W − 0,02 da NO_SUPERIOR y PIERDE.
- **Sello en clon fresco de `431b7bd`:** 13 md5 de fuentes y humo OK, 9 archivos rearmados OK y PASA 5/5: VERIFICACION_SELLO PASA. En `e2c2e1f` había dado FALLA por un salto de línea final que faltaba en `plan_humo_kaggle.json`; se corrigió en `431b7bd`.
- **Parche del CONTEXTO probado en copia:** `9430de7b` → `055a51a9`.

## Plan sellado y costo

| carril | trabajos en serie |
|---|---|
| a, GPU 0 | grilla c0h0 (+REPRO_R2), c1h0, c2h0; nulos SL k0 (+real), k10, k20 |
| a, GPU 1 | grilla c3h0 (+REPRO_R2), c4h0, c5h0; nulos T k0, k10, k20 |
| b, GPU 0 | grilla c0h1 (+REPRO_R2), c1h1, c2h1; nulos SL k30, k40 |
| b, GPU 1 | grilla c3h1 (+REPRO_R2), c4h1, c5h1; nulos T k30, k40 |

- Celdas c0 a c5: 0.0|0.15, 0.0|0.45, 0.3|0.15, 0.3|0.45, 0.6|0.15, 0.6|0.45. h0 son las tau 0 a 4 y h1 las 5 a 9; pruebas 2 a 11.
- 1.344.000 ensayos de grilla y 440.000 de nulos: unas 12,9 h de GPU en cuatro carriles. Kernel a unas 3,6 h, kernel b unas 3,2 h, a la vez: **unas 7 h de sesión de la cuota semanal**.
- **Hipótesis** (`agregar_factorial4.py`, el diseño del factorial 3):
  - H_SUPERA_CE: CE menos su regla con los mismos 564 sensores, bootstrap de dos vías, IC90, margen 1 punto.
  - H_ESCALA: CE menos R2 en las mismas 600 corridas (los mismos ensayos y la misma regla).
  - H_CABLEADO_CE: el real contra 50 SL y 50 T, p por rango y Holm.
  - Si el VEREDICTO_GLOBAL da INVÁLIDO, no se lee ninguna.
- **Disparo:** clon fresco de `431b7bd`, rearmar plan y kernels (los md5 tienen que dar `c3ed538d`, `d76dc652` y `09ffa774`), y `kaggle kernels push` de los dos. Está todo en `tools/factorial4/SELLO-FACTORIAL4.md`.

## Evidencia cruda

brain-env, CPU (`humo_ce/log.txt` md5 `6a919cde`, `humo_grilla/log.txt` md5 `8f8f03a3`):

```
# md5 script = 36a9f005cfc87470c74af8f303af56c3
CHEQUEO SUJETO_IGUAL_F2 (R1) -> True | 38.7 s
CHEQUEO PARIDAD_R1 (16 ensayos) max_dif=1.11e-16 numpy=0.1 s torch=0.5 s -> True
SUJETO CE neuronas=138639 aristas=15091983 inhibitorias=6032681 entradas=564 contiene_M46=True contiene_R1=True -> True | 42.4 s
RADIO CE crudo=2164.292802 | 23.2 s
CHEQUEO PARIDAD_CE (4 ensayos) max_dif=2.78e-17 numpy=24.1 s torch=17.8 s -> True
TIEMPO CE torch: 20 ensayos, trozo 500 -> 3.2160 s por ensayo
CHEQUEO INSTRUMENTO SUJETO_IGUAL_F2=True PARIDAD_R1=True CE_tamano=True PARIDAD_CE=True -> VALIDO
EXIT_RUN=0
CORRIDA celda=0.3|0.15 tau=0 prueba=2 W=0.9750 regla_propia=0.9500 regla40=0.9250 dif=+0.0250
```

Kaggle T4, humo 1 (`kernel_f4-ce-humo-t4-2026-10-13.log` md5 `e5b3326c`, recibo `b8766da8`, en git en `results/factorial4_2026-10-13_humo/t4/` de la rama):

```
# maquina: a1197ea0dc4a | Linux-6.18.48+-x86_64-with-glibc2.39 | Python 3.13.15 | numpy 2.5.3 | pandas 3.0.5 | torch 2.11.0+cu128 | dispositivo cuda Tesla T4
MD5 instrumento (6 archivos) -> OK
CHEQUEO REPRO_R2 torch=0.9465 factorial3=0.9465 -> True | 32.6 s
CHEQUEO PARIDAD_CE (4 ensayos) max_dif=1.25e-16 numpy=4.4 s torch=0.8 s -> True
TIEMPO CE torch: 1000 ensayos, trozo 500 -> 0.0262 s por ensayo
MEMORIA GPU max=3.11 GB
CHEQUEO INSTRUMENTO SUJETO_IGUAL_F2=True PARIDAD_R1=True REPRO_R2=True CE_tamano=True PARIDAD_CE=True -> VALIDO
CORRIDA celda=0.3|0.15 tau=0 prueba=2 W=0.9750 regla_propia=0.9500 regla40=0.9250 dif=+0.0250
NULO SL k=0 acierto=0.6250 radio=1503.1147 guarda=True | 8.9 s
NULO T k=0 acierto=0.7625 guarda=True | 4.8 s
FIN rc=0 motivo=corridas recibo_md5=b8766da86ebb2a0d9403869ba26cdb45
```

Kaggle «P100» (`kernel_f4-ce-humo-p100-2026-10-13.log` md5 `205a68df`, recibo `d3deb3c6`):

```
|   0  Tesla T4                       Off |   00000000:00:04.0 Off |                    0 |
|   1  Tesla T4                       Off |   00000000:00:05.0 Off |                    0 |
CHEQUEO REPRO_R2 torch=0.9465 factorial3=0.9465 -> True | 32.5 s
TIEMPO CE torch: 1000 ensayos, trozo 500 -> 0.0261 s por ensayo
FIN rc=0 motivo=corridas recibo_md5=d3deb3c66853f1f337538af689e741b7
```

Kaggle, carriles (`kernel_f4-ce-humo-carriles-2026-10-13.log` md5 `269bb479`, recibo `9021505b`; kernel `09b876f4`):

```
GPUS 2
CARRILES n_gpu=2 {"0": ["verificar_g0"], "1": ["verificar_g1"]}
[gpu1] CHEQUEO REPRO_R2 torch=0.9465 factorial3=0.9465 -> True | 33.5 s
[gpu1] TIEMPO CE torch: 1000 ensayos, trozo 500 -> 0.0260 s por ensayo
[gpu0] CHEQUEO REPRO_R2 torch=0.9465 factorial3=0.9465 -> True | 33.6 s
[gpu0] TIEMPO CE torch: 1000 ensayos, trozo 500 -> 0.0260 s por ensayo
FIN rc=0 motivo=corridas recibo_md5=9021505bb45c8dffeb932d0b2ae212a5
recibo: verificar_g1 2026-10-13T23:35:23Z a 23:37:04Z | verificar_g0 2026-10-13T23:35:23Z a 23:37:04Z
```

brain-env, prueba local de carriles (`prueba_carriles_local.log` md5 `50d86cb2`):

```
PLAN trabajos=22 grilla=12 nulos=10 corridas_de_grilla=600 nulos_por_tipo=50 -> OK
kernel f4-ce-a-2026-10-13 maquina=NvidiaTeslaT4 corridas=12 md5=d76dc6522aa773489a3505c73d96f9e5
kernel f4-ce-b-2026-10-13 maquina=NvidiaTeslaT4 corridas=10 md5=09ffa7743101c614cd5f511e87776917
RECIBO rc=0 motivo=corridas n_gpu=2 carriles={'0': ['ayuda_g0', 'ayuda_g0b'], '1': ['ayuda_g1']}
RECIBO rc=6 motivo=sin GPU: no se corre en CPU n_gpu=0 carriles=None corridas=[]
```

brain-env, verificación del sello en clon fresco (`verificar_sello_431b7bd.log`; la de `e2c2e1f` en `verificar_sello_e2c2e1f.log`):

```
MD5 749b5e2bf1afbdfbf4f7ff87e777e657 tools/factorial4/kaggle/plan_humo_kaggle.json -> DISTINTO (esperado 3efe72d1e3f6cfd55f506dfa72966140)   [e2c2e1f]
SELLO_MD5 distintos=0 -> OK   [431b7bd]
==== CASO humo_t4 -> PASA
==== CASO humo_alterado -> PASA
==== CASO sint_igual -> PASA
==== CASO sint_mas2 -> PASA
==== CASO sint_menos2 -> PASA
PRUEBA_AGREGADOR -> PASA 5/5
VERIFICACION_SELLO -> PASA
```

Parche del CONTEXTO en copia (script `a0126e91`): `md5 antes 9430de7be54f040be08a5ca07bcb7290`, cuatro anclas con 1 aparición, `md5 despues 055a51a914fe2cf5cb7c286f29566923`, `PARCHE OK`.

## Archivos

- Rama `titan/factorial4-cerebro-entero-2026-10-13` (`431b7bd`): `tools/factorial4/` (`cerebro_mosca.py`, `agregar_factorial4.py`, `prueba_agregar_factorial4.py`, `SELLO-FACTORIAL4.md`), `tools/factorial4/kaggle/` (`cuerpo_kernel.py`, `cuerpo_kernel_humo1.py`, `armar_plan.py`, `generar_kernels.py`, `plan_humo_kaggle.json`) y `results/factorial4_2026-10-13_humo/t4/` (recibo y cuatro json del humo en T4).
- `main`: esta respuesta, `tools/contexto/actualizar_contexto_2026-10-13-015.py` y su workflow, que se retira solo.
- Fuera de git, por md5: los logs crudos de los humos y las salidas de Kaggle de los otros dos kernels, en `/workspace/f4cerebro_2026-10-13/` de brain-env y en la salida de cada kernel.

## NO MEDIDO

- Ningún resultado del cerebro entero sobre la tarea: la grilla y los nulos de verdad no corrieron.
- Cuánta cuota semanal de GPU le queda a `abrahammendieta`: el CLI no la informa.
- Que una sesión de 3,6 h termine sin cortes: el humo más largo duró 4,6 min. El tope de 12 h por sesión es lo que publica Kaggle, no se midió acá.
- Que Kaggle siga dando T4 x2: lo dio las tres veces, y el pedido de P100 también cayó en T4.
- El tiempo real de un trabajo de grilla completo: estimado en unos 49 min (112.000 ensayos a 0,026 s).
- El costo de CE contra R2 en la misma máquina: la 013 lo estimaba en 3,7 veces; R2 no se cronometró en T4.
- La vía a git de los json grandes de la corrida real, unos 1,6 MB con la predicción de cada ensayo.

## Antes de firmar

| afirmación | instrumento | ¿podía dar rojo? |
|---|---|---|
| la T4 reproduce R2 | REPRO_R2 contra el 0,9465 que dio numpy en Actions (otro motor, otra máquina) | sí, tolerancia 0,001 |
| torch calcula lo mismo que numpy | PARIDAD_R1 y PARIDAD_CE: `factorial2_mosca.sim` (scipy) contra `sim_torch` (torch), dos funciones distintas | sí, umbral 1e-9 |
| el agregador decide bien | prueba 5/5 | sí: el humo tocado da INVÁLIDO y W − 0,02 da REFUTADA |
| lo sellado es lo que va a correr | 13 md5 y 9 rearmados desde clon fresco | sí: dio FALLA en `e2c2e1f` por un byte |
| los carriles corren a la vez | horas de inicio y fin en el recibo del humo de carriles | sí: en serie no se solaparían |
| sin GPU no corre en CPU | prueba local sin GPU | sí: salió rc 6 |

```
--- METODO PROMETEO ---
Accion delicada: no (rama titan; tres humos chicos en Kaggle con la cuota de abrahammendieta, unos 12 min; nada mergeado ni disparado)
Maquina: brain-env | Kaggle T4 x2 (abrahammendieta)
Artefactos: docs/agents/respuestas/2026-10-13-015-cerebro-entero-sellado-en-kaggle-la-t4-reproduce-r2.md + Doc de ClickUp 2026-10-13-015
```
