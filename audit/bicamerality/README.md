# Auditoría de BICAMERALITY · paréntesis declarado

**Esto NO pertenece al proyecto del conectoma.** Abraham lo marcó dos veces y tiene razón. Vive en `audit/` y no en `src/` a propósito.

## Qué es el sujeto

| | |
|---|---|
| Origen | celda **1** de `fabiomurillohot/notebookceb82767da` (Kaggle, `lastRun 2026-02-23T03:20:14Z`) |
| Tamaño | 34.903 B, 923 líneas |
| md5 | `9d89a158f809ff5f3765f42848502665` |
| Bytes de salida en el notebook | **0** — esa celda nunca se ejecutó |
| Procedencia del código | **DESCONOCIDA.** Ver `docs/agents/respuestas/2026-08-23-013` |

**El código del sujeto no se commitea acá**, porque su procedencia no está establecida y no es material del proyecto. Para reproducir, extraerlo así:

```python
import json
nb = json.load(open("fabiomurillohot__notebookceb82767da.txt"))
open("cell1.py", "w").write("".join(nb["cells"][1]["source"]))
# verificar: md5 == 9d89a158f809ff5f3765f42848502665
```

## Entorno, medido antes de decidir

```
python  3.12.14
torch   2.13.0+cpu
cuda    False
threads 2
nproc   2
```

**No se usó Kaggle.** Torch estaba en el container, así que todo corrió local y no se consumió cuota ajena.

## Los cuatro instrumentos

| Archivo | Qué mide | Log |
|---|---|---|
| `audit_bicam.py` | 11 tests, cada uno **puede dar rojo**. T0 es el control del control | `audit_bicam.log` |
| `zen.py` | Si el Zen clamp es alcanzable, barriendo `H` de 4 a 32 | `zen.log` |
| `train_red.py` | Entrenamiento reducido, 3 cerebros × 2 semillas × 40 episodios | `train_red.log` |
| `veto.py` | Trayectoria del veto α sobre 240 episodios | `veto.log` |

## Resultado: 2 de 11 en rojo

```
TESTS EN ROJO: 2
   - presupuesto_pareado_PureMemory
   - zen_clamp_se_activa
```

El detalle está en `docs/agents/respuestas/2026-08-23-014-auditoria-bicamerality.md`.
