# Brazo S recurrente (11-oct)

El falsador de «la mosca nace sabiendo» en el sustrato que pidió `docs/agents/CONTEXTO-motor.md` §6.2:
el motivo de escape de 26 neuronas (8 LC4, 8 LPLC2, 4 LC6, 2 GF, 4 DNp09; 88 aristas, todas excitatorias)
como **reservorio recurrente SparseLTC congelado**, contra su **shuffle de grado exacto** (brazo S), dentro
del mismo DualBrain y las mismas cuatro tareas del brazo W de agosto.

| Archivo | Qué hace |
|---|---|
| `motivo26.py` | Reconstruye el motivo desde el parquet pinneado (md5 `3d802fd5…`) con la selección verbatim de `brazo_w.py` y lo compara contra la matriz del brazo W (tiene que dar diferencia 0). Corre en brain-env, donde está el parquet. |
| `motivo26.json` | Su salida: matriz cruda con signo, aristas, root_ids y la verificación. |
| `brazo_s_recurrente.py` | Una celda tarea × brazo, 10 semillas. Lo que no es la vía react está copiado verbatim de `brazo_w.py`. |
| `agregar.py` | Junta las 36 celdas y aplica las reglas escritas antes de correr (ver su docstring). |
| `referencia_brazo_w.json` | Las semillas crudas del brazo W re-corrido el 2-oct en brain-env, extraídas de `/workspace/wrun/brazo_w.json` (md5 `690052d9…`). Sirve para chequear que A y B reproducen y para auditar los p de agosto. |

Brazos: `A` techo, `B` react denso congelado (los dos tienen que reproducir agosto), `RB/RW/RS` reservorio
recurrente con τ fija heterogénea (ruido, conectoma, shuffle), `LB/LW/LS` lo mismo con τ líquida congelada,
y `F` la memoria de DualBrain sin liquidez (τ constante por unidad).

Correr una celda a mano:

```bash
python3 tools/brazo_s/brazo_s_recurrente.py --tarea Gated --brazo RS --motivo tools/brazo_s/motivo26.json --out celda.json
python3 tools/brazo_s/agregar.py --celdas <dir con celda_*.json> --referencia tools/brazo_s/referencia_brazo_w.json --json resultados.json
```

En la fábrica lo corre `.github/workflows/brazo-s-recurrente.yml` (36 celdas en matriz) y el job final
commitea `results/brazo_s_recurrente_2026-10-11/` con el log crudo de cada celda.
