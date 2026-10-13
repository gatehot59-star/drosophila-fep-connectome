# 016: la corrida sellada de la 015 está en marcha, sin tocar; resultados NO MEDIDOS todavía

**Veredicto primero (F-01).** [MEDIDO] La corrida completa del script sellado `tools/escape_aterrizaje/tarea_mosca.py` (seal 57d094a, md5 40d64e074d9163753439307c5be4ac5e) arrancó a las 00:59:04 UTC del 13-oct (21:59 ART del 12-oct) desde un clon limpio, sin modificaciones. A las 01:32:30 UTC llevaba 2 de 6 celdas primarias, a 871,3 s y 943,4 s cada una. [CONCLUSIÓN] Todavía no hay veredicto: PAGA / DEPENDE / NO PAGA es NO MEDIDO hasta que el log imprima `VEREDICTO_GLOBAL` y el `EXIT_RUN` propio del script.

## Pedido

Botón `correr_tarea_mosca` (valor `correr_sellada`): correr la tarea de la 015 exactamente como quedó sellada. Después, a las 22:31 ART: «por qué no lo hacés correr en Kaggle con GPU».

## Herramientas y máquina

brain-env vía MUDH Gateway (servicio `build`), 2 CPU, sin GPU (`nvidia-smi: not found`), contenedor en UTC, Python 3.12.14, numpy 2.5.3. Escritura en git vía GitHub MCP (brain-env no tiene credenciales de push). Acción delicada: no (lectura de datos y cómputo; no se toca código sellado).

## Qué se midió

1. Clon nuevo de la rama `titan/tarea-mosca-2026-10-12` en `/workspace/tm_2026-10-12/clon_full`, checkout del seal y md5 del script.
2. Lanzamiento en segundo plano sin `--humo`.
3. Cabecera del log (66 líneas): motivo, composición, guardas, tamaños.
4. Cronómetro aparte (`/workspace/tm_2026-10-12/bench.py`, md5 25d100f0ca82adffc74275d68eb42606, no se commitea): una red de 46 neuronas, T=40, 2.400 + 2.000 ensayos, compitiendo por CPU con la corrida. Quedó superado por la duración real de las celdas (ver Corrección).
5. Para la pregunta de Kaggle: qué importa y qué usa el script, tamaño de los datos, CLI de Kaggle en brain-env.

## Evidencia cruda

```
57d094a4abcaae2e5e28a219de8d6701206e8699
40d64e074d9163753439307c5be4ac5e  tools/escape_aterrizaje/tarea_mosca.py
Tue Oct 13 00:59:04 UTC 2026
2
```

```
MOTIVO neuronas=46 visuales=40 aristas=187 sinapsis=1149 inhibitorias=0 ipsilaterales=187 rho_crudo=22.9733
MOTIVO tipo=LC4 por_lado=(4,4)
MOTIVO tipo=LPLC2 por_lado=(8,8)
MOTIVO tipo=LPLC4 por_lado=(4,4)
MOTIVO tipo=LPLC1 por_lado=(4,4)
COMPOSICION dn=DNp01 lado=left sinapsis_desde={'LC4': 54, 'LPLC2': 63, 'LPLC4': 0, 'LPLC1': 0}
COMPOSICION dn=DNp01 lado=right sinapsis_desde={'LC4': 61, 'LPLC2': 74, 'LPLC4': 0, 'LPLC1': 0}
COMPOSICION dn=DNp07 lado=left sinapsis_desde={'LC4': 1, 'LPLC2': 0, 'LPLC4': 169, 'LPLC1': 0}
COMPOSICION dn=DNp07 lado=right sinapsis_desde={'LC4': 0, 'LPLC2': 0, 'LPLC4': 138, 'LPLC1': 0}
COMPOSICION dn=DNp06 lado=left sinapsis_desde={'LC4': 9, 'LPLC2': 72, 'LPLC4': 0, 'LPLC1': 79}
COMPOSICION dn=DNp06 lado=right sinapsis_desde={'LC4': 10, 'LPLC2': 78, 'LPLC4': 0, 'LPLC1': 65}
CHEQUEO REPRODUCE_003 neuronas=True aristas=73 contra 73 -> True
NULOS SL=300 guarda=True T=300 guarda=True
DATOS entrenamiento=2400 prueba=2000 clases_prueba(nada,despegar,aterrizar,girar_der,girar_izq)=800,400,400,200,200 azar_mayoria_por_estado=0.5000 FA_por_linea=0.05
ORDEN por_condicion = posada(LOOM_LATERAL,LOOM_FRONTAL,PUNTO,BARRA,NADA) | vuelo(LOOM_LATERAL,LOOM_FRONTAL,PUNTO,BARRA,NADA)
```

```
Tue Oct 13 01:03:00 UTC 2026
  PID     ELAPSED %CPU COMMAND
23881       03:55  117 python3 tools/escape_aterrizaje/tarea_mosca.py --conn /workspace/connectivity.parquet --annot /workspace/annotations.tsv --out /workspace/tm_2026-10-12/completa
```

```
T 40 DT 0.02
seg_por_red_tr_mas_te 4.36
```

Parcial a las 01:31:53 UTC (2 de 6 celdas; sin Holm, sin veredicto):

```
CELDA A=0.0 ruido=0.15 W=0.9005 por_condicion=1.000,1.000,0.725,0.930,0.995,0.895,0.940,0.745,0.985,0.790 umbrales=0.306,0.355,0.246,0.261,0.224,0.262 | SL media=0.6967 max=0.8915 igualan=0/300 p_sup=0.0033 p_inf=1.0000 | T media=0.7192 max=0.8730 igualan=0/300 p_sup=0.0033 p_inf=1.0000 | 871.3 s
RIVAL A=0.0 ruido=0.15 regla_a_mano=0.9195 por_condicion=1.000,1.000,0.885,0.840,0.945,0.925,0.950,0.885,0.960,0.805 | H3 W contra regla 118 contra 156 p=0.0252 -> PEOR | ridge_crudo_entrenado(descriptivo)=0.9935
CELDA A=0.0 ruido=0.45 W=0.8805 por_condicion=1.000,1.000,0.820,0.875,0.905,0.785,0.965,0.705,0.965,0.785 umbrales=0.418,0.491,0.534,0.571,0.522,0.590 | SL media=0.6716 max=0.8305 igualan=0/300 p_sup=0.0033 p_inf=1.0000 | T media=0.7033 max=0.8515 igualan=0/300 p_sup=0.0033 p_inf=1.0000 | 943.4 s
RIVAL A=0.0 ruido=0.45 regla_a_mano=0.8705 por_condicion=1.000,1.000,0.925,0.880,0.915,0.880,0.935,0.405,0.960,0.805 | H3 W contra regla 175 contra 155 p=0.296 -> EMPATE | ridge_crudo_entrenado(descriptivo)=0.9595
```

Para la pregunta de Kaggle:

```
tarea_mosca.py:74:import numpy as np
tarea_mosca.py:75:import pandas as pd
tarea_mosca.py:78:import escape_aterrizaje_dbc3 as base  # noqa: E402  modulo de la 003, sin cambios
tarea_mosca.py:79:import entrada_por_tipos as ept  # noqa: E402  modulo de la 005, sin cambios
escape_aterrizaje_dbc3.py:21:import torch
tarea_mosca.py:213:    """Mismas operaciones que base.simular; devuelve las 6 descendentes."""
-rw-r--r-- 1 root root  31718505 Aug 22 20:46 /workspace/annotations.tsv
-rw-r--r-- 1 root root 100804642 Aug 22 20:12 /workspace/connectivity.parquet
Kaggle CLI 2.2.4
usage: kaggle kernels [-h]
                      {list,files,get,init,push,pull,output,status,logs,update,delete,topics}
sh: 1: nvidia-smi: not found
```

## Corrección de la estimación (01:32 UTC)

[MEDIDO] Las dos primeras celdas tardaron 871,3 s y 943,4 s, no los ~44 min que estimé. El cronómetro aparte daba 4,36 s por red porque corría compitiendo por los 2 CPU con la corrida y generando sus propios números al azar dentro del tramo medido; la corrida real va a ~1,5 s por red. [CONCLUSIÓN] Con 4 celdas a ~15 min más controles y brazos descriptivos, el fin esperado pasa a ~02:35 UTC (~23:35 ART del 12-oct), no 03:00 ART. Sigue siendo una estimación.

## Por qué no Kaggle con GPU, para esta corrida

[MEDIDO] La cuenta pesada de la 015 (601 redes por celda en `simular`) es numpy en CPU; torch sólo entra porque lo importa el módulo de la 003, y la simulación de la 015 no lo usa. [CONCLUSIÓN] En una máquina de Kaggle con GPU el script sellado correría en sus CPU y la GPU quedaría sin usar. Para aprovecharla hay que reescribir `simular` en torch (por ejemplo, las 601 redes juntas en un solo tensor), y eso es cambiar el instrumento después del sello: exige declararlo y probar que el port da las mismas predicciones que numpy antes de creerle. Además, subir 100,8 MB + 31,7 MB de datos, empujar el kernel, esperar la cola y validar el port no termina antes de las ~23:35 ART que ya da la corrida en curso. [MEDIDO] brain-env tiene el CLI de Kaggle 2.2.4 con credenciales de las dos cuentas, así que la vía existe para las próximas corridas grandes.

## Desvío del envoltorio, declarado

El `sh -c` que envuelve la corrida termina con `echo EXIT_RUN=...`, pero el shell del gateway expandió `$?` antes de lanzar: el `ps` muestra literalmente `echo EXIT_RUN=0`. Esa última línea del log NO vale como código de salida. Vale sólo el `EXIT_RUN=%d` que imprime el propio script después de `escrito resultados.json md5=` y `# duracion_s=`. Si el script muriera, el log tendría el `EXIT_RUN=0` falso sin las dos líneas previas: eso se lee como FALLO.

## Archivos

- Script sellado: rama `titan/tarea-mosca-2026-10-12`, commit 57d094a, `tools/escape_aterrizaje/tarea_mosca.py`.
- Log en curso: `/workspace/tm_2026-10-12/completa.log` (sólo brain-env; se commitea con md5 al terminar).
- Resultados: `/workspace/tm_2026-10-12/completa/resultados.json` (todavía no existe).

## NO MEDIDO

- Celdas 3 a 6 (A=0,3 y A=0,6), Holm sobre las 12, VEREDICTO_CELDA/AMPLITUD/GLOBAL.
- Controles de la corrida completa (reproduce, negativo AGNOSTICA, positivo regla a mano).
- Brazos descriptivos LPLC1_SILENCIOSA y LPLC4_SILENCIOSA.
- Duración total real (sólo estimada).
- Velocidad de un port a GPU en Kaggle y su equivalencia con numpy: no existe el port.

## Antes de firmar

| Afirmación | Instrumento | ¿Podía dar rojo? |
|---|---|---|
| Se corre el script sellado sin tocar | md5 del clon contra 40d64e07… | Sí: cualquier cambio cambia el md5 |
| Corre la versión completa, no el humo | línea DATOS 2400/2000 y NULOS 300/300 | Sí: el humo imprime 600/400 y 3/3 |
| El motivo es el de la 015 | MOTIVO 46/187/1149 y REPRODUCE_003 True | Sí: otro corte da otros números |
| Sigue viva y lleva 2 de 6 | `ps` y `grep -c ^CELDA` a las 01:31 a 01:32 UTC | Sí: un proceso muerto no aparece y las celdas se cuentan |
| ~15 min por celda | duración impresa por el propio script en cada CELDA | Sí: el script mide su reloj por celda |
| La GPU no acelera el script sellado | imports y llamadas del script | Sí: si `simular` usara torch aparecería en el grep |
| Fin ~23:35 ART | extrapolación de 2 celdas | Parcial: es estimación |

--- METODO PROMETEO ---
Acción delicada: no
Máquina: brain-env (MUDH Gateway, build), 2 CPU, sin GPU, UTC
Artefactos: docs/agents/respuestas/2026-10-12-016-la-corrida-sellada-de-la-015-esta-en-marcha-sin-tocar.md; Doc de ClickUp con los resultados cuando termine la corrida
