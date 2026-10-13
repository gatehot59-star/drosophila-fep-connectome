# 016: la corrida sellada de la 015 está en marcha, sin tocar; resultados NO MEDIDOS todavía

**Veredicto primero (F-01).** [MEDIDO] La corrida completa del script sellado `tools/escape_aterrizaje/tarea_mosca.py` (seal 57d094a, md5 40d64e074d9163753439307c5be4ac5e) arrancó a las 00:59:04 UTC del 13-oct (21:59 ART del 12-oct) desde un clon limpio, sin modificaciones, y a las 01:03:00 UTC seguía viva. [CONCLUSIÓN] Todavía no hay ningún número del experimento: PAGA / DEPENDE / NO PAGA es NO MEDIDO hasta que el log imprima `VEREDICTO_GLOBAL` y el `EXIT_RUN` propio del script.

## Pedido

Botón `correr_tarea_mosca` (valor `correr_sellada`): correr la tarea de la 015 exactamente como quedó sellada.

## Herramientas y máquina

brain-env vía MUDH Gateway (servicio `build`), 2 CPU, contenedor en UTC, Python 3.12.14, numpy 2.5.3. Escritura en git vía GitHub MCP (brain-env no tiene credenciales de push). Acción delicada: no (lectura de datos y cómputo; no se toca código sellado).

## Qué se midió

1. Clon nuevo de la rama `titan/tarea-mosca-2026-10-12` en `/workspace/tm_2026-10-12/clon_full`, checkout del seal y md5 del script.
2. Lanzamiento en segundo plano sin `--humo`.
3. Cabecera del log (66 líneas): motivo, composición, guardas, tamaños.
4. Cronómetro aparte (`/workspace/tm_2026-10-12/bench.py`, md5 25d100f0ca82adffc74275d68eb42606, no se commitea, es instrumento de estimación): una red de 46 neuronas, T=40, 2.400 + 2.000 ensayos, con la misma recurrencia `tanh`, compitiendo por CPU con la corrida.

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

## Estimación de duración (ESTIMADO, no medido)

Cada una de las 6 celdas primarias simula 601 redes (W + 300 SL + 300 T) sobre 4.400 ensayos: 601 × 4,36 s ≈ 44 min por celda, unas 4,5 a 5 h en total más controles y brazos descriptivos. Fin esperado cerca de las 03:00 ART del 13-oct. El humo 2 (7 redes, 1.000 ensayos, 26 a 55 s por celda) es consistente con este orden.

## Desvío del envoltorio, declarado

El `sh -c` que envuelve la corrida termina con `echo EXIT_RUN=...`, pero el shell del gateway expandió `$?` antes de lanzar: el `ps` muestra literalmente `echo EXIT_RUN=0`. Esa última línea del log NO vale como código de salida. Vale sólo el `EXIT_RUN=%d` que imprime el propio script después de `escrito resultados.json md5=` y `# duracion_s=`. Si el script muriera, el log tendría el `EXIT_RUN=0` falso sin las dos líneas previas: eso se lee como FALLO.

## Archivos

- Script sellado: rama `titan/tarea-mosca-2026-10-12`, commit 57d094a, `tools/escape_aterrizaje/tarea_mosca.py`.
- Log en curso: `/workspace/tm_2026-10-12/completa.log` (sólo brain-env; se commitea con md5 al terminar).
- Resultados: `/workspace/tm_2026-10-12/completa/resultados.json` (todavía no existe).

## NO MEDIDO

- Todas las celdas CELDA/RIVAL, Holm, VEREDICTO_CELDA/AMPLITUD/GLOBAL.
- Controles de la corrida completa (reproduce, negativo AGNOSTICA, positivo regla a mano).
- Brazos descriptivos LPLC1_SILENCIOSA y LPLC4_SILENCIOSA.
- Duración real (sólo estimada).

## Antes de firmar

| Afirmación | Instrumento | ¿Podía dar rojo? |
|---|---|---|
| Se corre el script sellado sin tocar | md5 del clon contra 40d64e07… | Sí: cualquier cambio cambia el md5 |
| Corre la versión completa, no el humo | línea DATOS 2400/2000 y NULOS 300/300 | Sí: el humo imprime 600/400 y 3/3 |
| El motivo es el de la 015 | MOTIVO 46/187/1149 y REPRODUCE_003 True | Sí: otro corte da otros números |
| Sigue viva | `ps` a las 01:03:00 UTC | Sí: un proceso muerto no aparece |
| Duración ~5 h | cronómetro de una red | Parcial: es estimación, puede variar con la carga |

--- METODO PROMETEO ---
Acción delicada: no
Máquina: brain-env (MUDH Gateway, build), 2 CPU, UTC
Artefactos: docs/agents/respuestas/2026-10-12-016-la-corrida-sellada-de-la-015-esta-en-marcha-sin-tocar.md; Doc de ClickUp con los resultados cuando termine la corrida
