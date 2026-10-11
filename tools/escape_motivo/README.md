# escape_motivo: el brazo S en la función propia del motivo

El motivo de escape de 26 neuronas (8 LC4, 8 LPLC2, 4 LC6, 2 GF, 4 DNp09; el mismo de `tools/brazo_s/`) recibe looming por sus neuronas visuales, cada una por el ojo de su lado, y se lee sólo por sus dos Giant Fiber. No se entrena nada. Se compara contra su shuffle de grado exacto (S), contra un shuffle de grado exacto que conserva el hemisferio (SL) y contra ruido congelado (B), con τ fija heterogénea, τ fija uniforme, τ líquida y el brazo lineal. Reglas pre-registradas en el docstring de `escape_motivo.py` (commit `445646a`, antes de la corrida completa).

## Cómo se corrió

```
python3 tools/escape_motivo/lados26.py --annot annotations.tsv --motivo tools/brazo_s/motivo26.json --out tools/escape_motivo/lados26.json
python3 tools/escape_motivo/escape_motivo.py --motivo tools/brazo_s/motivo26.json --lados tools/escape_motivo/lados26.json \
    --brazo-s tools/brazo_s/brazo_s_recurrente.py --k 200 --out-dir results/escape_motivo_2026-10-11
```

Máquina: brain-env (Celeron N4020, Python 3.12.14, numpy 2.5.3), desde un clon fresco de esta rama; 5,18 min. La línea final `EXIT=0` del log la agrega el lanzador; el script imprime `EXIT_RUN=0` antes de salir. `resultados.json` (533.509 B, md5 `e3ce0eb262fae32605c1af4f009976e1`) no se commitea por tamaño: se regenera con el mismo comando.

## Resultado (de `results/escape_motivo_2026-10-11/run.log`)

| Contraste | W | Nulo (media) | Nulo >= W | p | Regla |
|---|---|---|---|---|---|
| P1 acierto, W vs S | 1.0000 | 0.5102 | 7/200 | 0.0398 | W GANA |
| P3 supervivencia, W vs S | 1.0000 | 0.6605 | 6/200 | 0.0348 | W GANA |
| P2 acierto, W vs SL | 1.0000 | 0.9806 | 149/200 | 0.7463 | W NO GANA |
| P3 supervivencia, W vs SL | 1.0000 | 0.9983 | 161/200 | 0.8060 | W NO GANA |
| P4 acierto, W vs B | 1.0000 | 0.4617 | 12/200 | 0.0647 | W NO GANA |
| P4 supervivencia, W vs B | 1.0000 | 0.5976 | 8/200 | 0.0448 | W GANA |

W saca 180/180 en las seis variantes (τ fija heterogénea, uniforme, líquida; tanh y lineal): P5 y P6 dan IGUAL con 0 pares discordantes, **en el techo**. El reflejo escrito a mano (C+) también saca 1.0/1.0; la red nula (C0) 0.0/0.0; una política ciega al lado sobrevive 0.7222.

**Lectura:** el motivo de la mosca son dos mitades ipsilaterales (88/88 aristas del mismo lado). En su función, eso le gana al shuffle que la rompe; el shuffle que la conserva empata. Paga la lateralidad, no el cableado fino, y la tarea no distingue τ fija de líquida porque todas llegan al techo.
