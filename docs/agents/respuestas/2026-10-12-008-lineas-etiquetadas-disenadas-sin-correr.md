# 2026-10-12-008: líneas etiquetadas diseñadas y sin correr; estado de la v2 y de Tao

**Estado de la respuesta: PARCIAL.** Hay diseño y no hay medición. Cuando se corra, el resultado entra como addendum de este mismo archivo.

Doc de ClickUp: https://app.clickup.com/90171457413/docs/2kza6fw5-21457

## 1. Pedido

- **11:41:** botón `lineas_etiquetadas_actions_006` (valor "lineas") de la 006. Pide correr líneas etiquetadas, donde cada descendente tiene su umbral y dispara una acción, contra SL y T, con la misma entrada que la 005 y en Actions.
- **11:44:** "no veo tus respuestas".

## 2. Herramientas y máquina

- **brain-env:** clon fresco del repo (36 refs) en `/workspace/le_2026-10-12/repo`, sólo de lectura. No se escribieron datos ni se gastó cuota.
- **ClickUp:** se creó el Doc https://app.clickup.com/90171457413/docs/2kza6fw5-21457.
- **GitHub:** este commit.

## 3. Qué se midió

Nada del experimento. Sólo se leyeron los insumos.

## 4. Evidencia cruda

```
md5sum tools/escape_aterrizaje/*.py   (en origin/titan/entrada-por-tipos-2026-10-12 @ f7844be)
e060c4bffb685aa550dadc19eda3dd02  tools/escape_aterrizaje/entrada_por_tipos.py   (547 lineas)
4d40477d87406c31672acfb6e6e8f5a2  tools/escape_aterrizaje/escape_aterrizaje_dbc3.py   (401 lineas)
origin/main HEAD = b8eac1c
```

El módulo de la 003 importa numpy, pandas, torch y scipy. La 005 importa torch.

`construir_motivo` lee el parquet de 15.091.983 aristas (md5 3d802fd542b5d18570ba1ba0bb0abed9) y las anotaciones (md5 719904abad876c68ace1b5690c9b9b63).

`barajar_sl` y el nulo T actúan sólo sobre las 73 aristas del motivo.

## Diseño (sin sellar)

**Insumos:** entrada por tipos de la 005 sin cambios (LC4, LPLC2 y LPLC4 en las variantes COMO_LPLC2, SILENCIOSA y MOVIMIENTO; ruido 0,15 y 0,45), con el motivo de 28 neuronas y la dinámica SparseLTC con tau semilla 0.

**Lector sin entrenar:** cada descendente tiene un umbral calibrado sólo con ensayos de ruido, que fija una tasa de falsa alarma declarada antes de correr.

- DNp01 izquierda o derecha → escapar hacia el otro lado.
- DNp07 → aterrizar si está volando.
- Si no cruza ningún umbral → nada.

**Comparaciones:**

- W contra 300 SL y 300 T, con p por rango y Holm.
- Rival crudo (ridge) y regla a mano con umbrales calibrados sobre las entradas crudas.
- Control negativo: con entrada AGNOSTICA, T tiene que dar idéntico a W.

**Máquina:** Actions. Hay que instalar numpy, pandas, pyarrow, scipy y torch CPU. Como el parquet no está en Actions, se fija el motivo como fixture con md5 o se baja de su fuente. Lo que se elija hay que medirlo antes.

## 5. Archivos

Este archivo.

El CONTEXTO no se reescribe en este turno: se actualiza con la entrega de la 008.

## 6. NO MEDIDO

- El resultado completo de las líneas etiquetadas.
- La rama, el sellado y la corrida en Actions.
- Si TITÁN Tao arrancó la auditoría: tarea https://app.clickup.com/t/86e3p74xa, sin respuesta vista a las 11:45.
- La v2: el depósito sigue bloqueado hasta el merge del PR #27 y un token de Zenodo con deposit:write y deposit:actions.

## Antes de firmar

No se afirma nada verde. El único estado es diseñado y sin correr.
