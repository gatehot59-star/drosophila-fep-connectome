# SELLO · H_TOPO_FIEL: el programa que usa solo flechas que la mosca tiene, contra el que resta (respuesta 2026-10-14-021)

**Pedido.** Abraham, 14-oct 18:20, ClickKit `sellar_topo_fiel_020`: «Sellá el programa fiel a la mosca».

## La pregunta
Topo v0.1 (2026-10-14-020) mostró que `escape.topo` hace una cuenta que la mosca no tiene cableada: las líneas de giro de DNp06 restan el LPLC1 y el LPLC2 del otro lado, y esas 4 flechas no tienen sinapsis directas en FlyWire v783 (SIN_VIA_DIRECTA). El aterrizaje de `escape.topo` ya es fiel (lee solo LPLC4). La pregunta es si el programa que no resta rinde igual.

## Orden del sello (verificable en git)
| Paso | Commit | Qué | md5 |
|---|---|---|---|
| A | `27fe098` | Los programas, antes de cualquier banco: el fiel y el control cruzado; chequeo Topo v0.1 del fiel | `escape_fiel.topo` 8e7f23be70392bde04643a2bf3c1fa65; `escape_cruzado.topo` 9d0bb0f6f4cdc48f138b09f5b268429d; `docs/topo/grafo-fiel-2026-10-14.log` 53961f0d598a8125547cd93583bbcd58; `docs/topo/grafos/escape_fiel.md` bd4683fcfb5da263c0fb1841531d2b48 |
| B | `b3548c8` | El banco, la regla de decisión, su prueba y los workflows | `banco_fiel.py` ff0a7cbf333788634c405da7d09fcae7; `decidir_fiel.py` 840aeabf15446852cd0122a6fc4e5b7a; `prueba_fiel.py` 016a6307ce06f4f70cf74eb753a9cd8d; `topo-fiel-mosca.yml` 8c18ab3d6ffeed8648905b8e81202ff2; `topo-fiel-humo.yml` 63bbfde18d825c4125fbd5d04719cb27 |

Sin cambios: `tarea_mosca.py` 40d64e07, `escape_aterrizaje_dbc3.py` 4d40477d, `entrada_por_tipos.py` e060c4bf, `topo.py` 9abefe9d, `topo_grafo.py` 0ea68782, `escape.topo` dae4967d, `tarea_barra_dir.py` d2515357, `aterrizaje_dir.topo` 0122a4ce.

## Los programas
- **Fiel** (`escape_fiel.topo`): igual a `escape.topo` salvo las dos líneas de giro, que leen solo el lado propio: `DNp06@L = media(LPLC1@L, LPLC2@L)`. Topo v0.1: **CABLEADA=10**, ninguna flecha sin vía.
- **El que resta** (`escape.topo`, sellado en la 011): `DNp06@L = media(LPLC1@L, LPLC2@L) - media(LPLC1@R, LPLC2@R)`. Topo v0.1: CABLEADA=10, SIN_VIA_DIRECTA=4.
- **Control cruzado** (`escape_cruzado.topo`): el fiel con las acciones de giro intercambiadas (gira hacia el estímulo).
- `prueba_fiel.py` verifica que son pares mínimos: el fiel difiere del que resta solo en las líneas 5 y 6, y el cruzado del fiel solo en sus acciones.

## Banco
- Tarea de la 012 (`tarea_barra_dir.py`: la 015 más la barra de atrás hacia adelante), 6 celdas (A × ruido), 2400 de entrenamiento y 2000 de prueba por celda, backend regla de Topo, todos los programas en los mismos ensayos.
- **Semillas nuevas:** 31 y 32 para los ensayos, 131 y 132 para el ruido. Las de la 014 (1, 2, 101, 102) ya se habían visto.

## Hipótesis (margen 0,01, IC90 por bootstrap estratificado por celda, B = 20.000)
- **H_TOPO_FIEL:** d = acierto del fiel menos acierto del que resta, en 12.000 ensayos.
  - SOSTENIDA si el límite inferior es mayor que −0,01 (el fiel no pierde más de un punto).
  - REFUTADA si el superior es menor que −0,01.
  - Si no, SIN_DECIDIR.
- **CONTROL_ROJO:** el mismo criterio con el cruzado en lugar del fiel. Tiene que salir REFUTADA; si no, el veredicto de H_TOPO_FIEL es **INVALIDO**.
- **Guardas** (salida 3): md5 de todo; la tarea pasa sus chequeos; REPRODUCE_M46; CABLEADO_FIEL (CABLEADA=10); CONTROL_GRAFO (el que resta da SIN_VIA_DIRECTA=4).
- **Descriptivo, sin veredicto:** fiel contra `aterrizaje_dir.topo`; fiel contra W (el cableado de la 015 sin entrenar las líneas); por celda; por subconjunto (giro en vuelo, looming frontal en vuelo, barras AA y AD en vuelo, posada).

## Prueba de la regla
- `prueba_fiel.py` 8/8 en brain-env y desde un clon limpio.
- Puede dar rojo: con `escape.topo` en lugar del fiel, PAR_MINIMO_FIEL y PAR_MINIMO_CRUZADO dan FALLA (6/8); los escenarios sintéticos cubren SOSTENIDA, REFUTADA y SIN_DECIDIR.

## Humo
- **brain-env, 18:27 (600/400, B = 2.000).** Log `results/topo_fiel_2026-10-14_humo/brain-env-humo.log`, md5 eac0b4e769fff46f7321f13564beaf2a; JSON 174d6621f9d50802f0dd847a1a885109; 64,8 s.
  - Controles: VEREDICTO_TAREA VALIDA, CABLEADO_FIEL True, CONTROL_GRAFO True, REPRODUCE_M46 True, EXIT_RUN=0.
  - CONTROL_ROJO salió REFUTADA (−27,5 puntos): el banco puede dar rojo.
  - **Declarado:** vi los números del humo antes de sellar, y no cambié nada de A ni de B después de verlos.
  - El humo ya muestra al fiel perdiendo unos 5 puntos, y casi todo viene del looming frontal en vuelo.
  - El humo usa las mismas semillas 31 y 32 a menor tamaño, así que la corrida completa **no es ciega** respecto del humo. Lo que agrega es precisión (12.000 ensayos contra 2.400) y el desglose completo.
- **Actions x64:** se dispara con `results/topo_fiel_2026-10-14_humo/HUMO`, en este mismo commit.

## Disparo
La corrida completa (minutos, un solo trabajo, sin nulos) **solo** se dispara al pushear `results/topo_fiel_2026-10-14/CORRER`, con el sí de Abraham.
