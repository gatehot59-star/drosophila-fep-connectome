# REGLA DEL SLUG DE KAGGLE · por qué el `403 kernels.get` era mío

**Medido:** 2026-08-26 04:50-04:57 UTC · **Instrumento:** `gateway build.run` sobre `brain-env`, API de Kaggle v1 con `Authorization: Bearer`. **Se re-mide, no se recuerda.**

## El error

Al subir un kernel con `POST /kernels/push` yo mando `slug: "<user>/titan-motorv2-gpu-shard0"` **y** `newTitle: "TITAN motor v2 GPU shard 0/4"`.

**Kaggle NO usa mi slug. Genera el `ref` slugificando el TÍTULO.**

| lo que mandé | el `ref` que Kaggle creó |
|---|---|
| `titan-motorv2-gpu-shard0` | `titan-motor-v2-gpu-shard-0-4` |
| `titan-motorv2-gpu-shard1` | `titan-motor-v2-gpu-shard-1-4` |
| `titan-motorv2-gpu-shard2` | `titan-motor-v2-gpu-shard-2-4` |
| `titan-motorv2-gpu-shard3` | `titan-motor-v2-gpu-shard-3-4` |

O sea: `motor v2` → `motor-v2` (separa la v de la versión) y `0/4` → `-0-4` (la barra se vuelve guion).

## La consecuencia medida

Con el slug que yo mandé, **las tres lecturas dan 403** y el mensaje es engañoso:

```
kernels/status  -> HTTP 403  {"code":403,"message":"Permission 'kernels.get' was denied"}
kernels/output  -> HTTP 403  {"code":403,"message":"Permission 'kernels.get' was denied"}
kernels/pull    -> HTTP 403  {"code":403,"message":"Permission 'kernels.get' was denied"}
```

Con el `ref` real, **las tres dan 200**, con el mismo token y en la misma corrida:

```
status(ref real) -> HTTP 200  {"status":"complete","failureMessage":"","hasFailureMessage":false}
output(ref real) -> HTTP 200  {"logNullable":"...GPU detectada: Tesla P100-PCIE-16GB..."}
pull  (ref real) -> HTTP 200  {"metadata":{..."machineShapeNullable":"Gpu"...}}
```

**`Permission 'kernels.get' was denied` en Kaggle significa «ese kernel no existe o no es tuyo», NO «tu token no tiene el scope».** Un kernel privado inexistente y un kernel privado ajeno devuelven el mismo 403, y por eso el mensaje no distingue el caso.

## Para Tachi: no hay nada que hacer

La pregunta era qué tenía que habilitar Tachi para desbloquearme Kaggle. **Respuesta medida: nada.**

- Los tokens `KGAT_` de las dos cuentas están **vivos** y alcanzan para leer estado, log y fuente de kernels privados propios.
- No falta ningún scope, no hay que rotar credenciales, no hay que crear una cuenta nueva ni pedir permisos.
- Lo único que faltaba era **descubrir el `ref`, no adivinarlo**.

## La vía correcta, para no repetirlo

1. Después de `push`, **no** construir la URL de monitoreo con el slug enviado.
2. Pedir `GET /kernels/list?user=<user>&page=1&pageSize=100&sortBy=dateRun` y **leer el campo `ref`** de los kernels recién corridos (`lastRunTime`).
3. Monitorear y bajar output con ese `ref`, partido en `userName` / `kernelSlug`.

Nota adicional medida: en `/kernels/list` el campo `slug` viene **vacío** (`"slug":""`); el identificador utilizable es `ref`. Y `/kernels/list?search=<slug-enviado>` devuelve `[]`, lo que confirma que ese slug no existe del lado de Kaggle.

Corolario para `kwatch*.mjs`: los watchers escritos con el slug enviado **nunca** iban a poder ver un kernel. No fallaron por permisos: preguntaban por algo que no existe.
