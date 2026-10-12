# 2026-10-12-010: Tao sí dejó hallazgos; la v2 no está lista para publicar

**Estado que sustituye al de la 009 y a su resumen en CONTEXTO-drosophila-fep.md:** Tao comunicó resultados a las 13:25, después de la revisión anterior. Lo hizo en su chat con Abraham, no en la tarea. El informe completo sigue sin archivarse: pide confirmar su paquete de siete objetos. La ausencia de un PR no demuestra que no haya trabajado.

**Veredicto de esta reconsulta:** confirmé tres inconsistencias internas en el manuscrito exacto del PR #27. No reproduje toda la auditoría. Retiro «lista para depositar» como aprobación científica: el render determinista y los hashes no validaban las conclusiones. No se tocó el manuscrito ni Zenodo.

**Doc actualizado con esta adenda al principio:** https://app.clickup.com/90171457413/docs/2kza6fw5-21477
**Devolución de Tao:** https://app.clickup.com/90171457413/chat/r/2kza6fw5-1037/t/80170050745296
**Hilo:** https://app.clickup.com/90171457413/chat/r/2kza6fw5-1037/t/80170050742708
**PR #27:** https://github.com/gatehot59-star/drosophila-fep-connectome/pull/27

## 1. Pedido

Abraham: «REVISA DE NUEVO», 12 de octubre de 2026, 14:15 ART. Referencia: comprobar si Tao entregó, dentro del pedido previo de revisar su auditoría antes de Zenodo.

## 2. Herramientas y máquina

- ClickUp: `load_assets` sobre la tarea con todos los comentarios y sobre el hilo nuevo; `search_index` sobre documentos, comentarios y mensajes creados desde 2026-10-12T14:36:00Z; `read_text` y `apply_patch` para actualizar el Doc anterior.
- GitHub: `githubmcp_list_pull_requests`, `githubmcp_list_branches`, `githubmcp_list_commits`, `githubmcp_get_file_contents`. Main observado: `0c6722b8a4ff8f552a872baddbf62c1865e2f21a`, la respuesta 009 y su contexto, ya presentes en esta conversación. PR #27 seguía abierto en `554f7d99be81f27da331dc5e736b89c5e704e8c2`.
- Manuscrito leído íntegro: `docs/v2/paper1-v2.0.md`, blob `6656f7f2d98431e3933208c47df430ca810fedb1`, commit `554f7d99be81f27da331dc5e736b89c5e704e8c2`.
- Inventario leído en main: `00-ENTORNOS-Y-CAPACIDADES.md`, blob `214d6d3859acfc660772460e8665f96042de90cd`. No se re-midieron las tres máquinas ni se usó su foto de agosto para afirmar una capacidad actual.
- Sandbox de ClickUp: `execute_bash`, Python estándar con Decimal. Sólo cálculos sobre los números leídos del manuscrito. No hubo acceso al parquet ni una corrida de los experimentos originales.
- Escrituras: este archivo nuevo y adenda en el Doc 009. No se envió ningún mensaje a Tao, no se disparó un Super Agent, no se cambió el PR #27, no hubo merge ni operaciones en Zenodo.

## 3. Qué se midió y qué cambia

### Estado de Tao

La tarea conserva la respuesta de las 11:39. La búsqueda fuera de la tarea localizó un hilo posterior:

- 13:12: Abraham volvió a pedir la auditoría en su chat con Tao.
- 13:13: Tao dijo que retomaba las lecturas y reconoció que no debió bloquearlas por la confirmación de publicación.
- 13:25: Tao comunicó hallazgos y dijo tener el informe preparado, pendiente de archivar.

Fuente primaria: https://app.clickup.com/90171457413/chat/r/2kza6fw5-1037/t/80170050742708, devolución https://app.clickup.com/90171457413/chat/r/2kza6fw5-1037/t/80170050745296. La respuesta 009 describe el estado anterior a esas intervenciones, no el estado actual.

### Tres inconsistencias confirmadas en el sujeto exacto

1. **FAIL, dispersión 2,4×.** Tabla 5b: ratios de neuropilo 0,368; 1,531; 0,803 y 0,632. Máximo/mínimo = 4,160326086956521739130434783. El párrafo siguiente dice «The 323-fold spread collapses to 2.4-fold». Con esas cuatro filas corresponde aproximadamente 4,16×. Son valores publicados redondeados, no un nuevo cálculo desde los datos crudos.
2. **FAIL, tres modelos amplifican.** §2.5 afirma «Temporal amplification is therefore validated across three compatible models (SparseLTC, Linear, LIF-soft)». Tabla 9: SparseLTC cambia +0,202; Linear +0,212; LIF-soft cambia −0,251 (0,253 a 0,002). Los dos primeros crecen; LIF-soft decae. Compatibilidad con la métrica no implica replicar amplificación.
3. **FAIL, invariancia sin precisar umbral.** La Tabla 5c sin umbral da desviaciones estándar 0,9 para olfato y 0,16 para visual. Por tanto hay varianza; no son nulos constantes. La frase «the statistic is not testable against it» debe distinguir este régimen del umbral de cinco sinapsis, para el que el texto reporta cero. Un cero observado compatible con un nulo no es automáticamente una invariancia por construcción.

**Tabla 8:** §3.7 y Limitaciones 5 declaran que el productor no está archivado y los valores no se reprodujeron; la conclusión central sigue usándolos como resultado firme. Confirmé esa contradicción documental, no una nueva búsqueda exhaustiva de todos los posibles productores. No se reprodujo su trayectoria en este turno.

### Lo atribuido a Tao, no reproducido aquí

Tao informa que el nulo por neuropilo conserva el grado global, que lo probó en 100 grafos sintéticos, que reprodujo dos desbordamientos ADC/PWM y que el test de swarm no impone sus expectativas. También informa coincidencia de las tablas 5 y 7 y varios contrastes estadísticos. Sin sus comandos y salidas archivadas no doy esos ensayos por reproducidos por BRAIN.

**No es un dictamen de que los conectomas no sirvan.** Es un bloqueo de esta versión del texto y una lista de hallazgos pendientes de cotejo completo. Los resultados simulados y el hardware son sujetos distintos.

## 4. Evidencia cruda y reproducción

Comando ejecutado en el sandbox de ClickUp, copiado verbatim:

```bash
python - <<'PY'
from decimal import Decimal
import json, hashlib
r = {
 'subject': 'docs/v2/paper1-v2.0.md',
 'commit': '554f7d99be81f27da331dc5e736b89c5e704e8c2',
 'table_5b_neuropil_ratios': {'olfactory': '0.368', 'visual': '1.531', 'mechanosensory': '0.803', 'gustatory': '0.632'},
 'table_9': {'SparseLTC': ['0.630', '0.832'], 'Linear': ['0.623', '0.835'], 'LIF-soft': ['0.253', '0.002']},
 'table_5c_unthresholded_null_sd': {'olfactory': '0.9', 'visual': '0.16'}
}
vals = [Decimal(v) for v in r['table_5b_neuropil_ratios'].values()]
spread = max(vals) / min(vals)
print('SOURCE_COMMIT', r['commit'])
print('INPUT_SHA256', hashlib.sha256(json.dumps(r,sort_keys=True).encode()).hexdigest())
print('TABLE_5B_SPREAD_FROM_ROUNDED_VALUES', str(spread))
print('MANUSCRIPT_SPREAD', '2.4')
for model, pair in r['table_9'].items():
    change = Decimal(pair[1])-Decimal(pair[0])
    print('TABLE_9', model, 't60', pair[0], 't180', pair[1], 'delta', str(change), 'amplifies', change>0)
for pop, sd in r['table_5c_unthresholded_null_sd'].items():
    print('TABLE_5C',pop,'sd',sd,'variance',str(Decimal(sd)**2),'invariant',Decimal(sd)==0)
print('SCOPE', 'Consistency of manuscript tables only; no regeneration of scientific experiments or inspection of Tao runtime.')
PY
```

Exit code: **0**. Stderr: **vacío**. Stdout completo:

```plain
SOURCE_COMMIT 554f7d99be81f27da331dc5e736b89c5e704e8c2
INPUT_SHA256 9213466febcf0e9b2f34e2941409bd70b8305af035d24d1c7bf39f4b8892a5f0
TABLE_5B_SPREAD_FROM_ROUNDED_VALUES 4.160326086956521739130434783
MANUSCRIPT_SPREAD 2.4
TABLE_9 SparseLTC t60 0.630 t180 0.832 delta 0.202 amplifies True
TABLE_9 Linear t60 0.623 t180 0.835 delta 0.212 amplifies True
TABLE_9 LIF-soft t60 0.253 t180 0.002 delta -0.251 amplifies False
TABLE_5C olfactory sd 0.9 variance 0.81 invariant False
TABLE_5C visual sd 0.16 variance 0.0256 invariant False
SCOPE Consistency of manuscript tables only; no regeneration of scientific experiments or inspection of Tao runtime.
```

Tao, citas relevantes de su mensaje de las 13:25:

> «No publicaría la v2 tal como está ni daría por validado el cerebro robótico.»

> «El informe está preparado. Para publicarlo y dejar continuidad falta confirmar el paquete de 7 objetos, no volver a hacer la auditoría».

Fuente: https://app.clickup.com/90171457413/chat/r/2kza6fw5-1037/t/80170050745296. Su QA declarado 41/45 no es una aprobación del proyecto, ni se adopta como puntuación propia de BRAIN.

## 5. Archivos y continuidad

- Archivo generado: `docs/agents/respuestas/2026-10-12-010-tao-si-dejo-hallazgos-la-v2-no-se-publica.md`.
- Doc 009 actualizado con una adenda de esta revisión al principio: https://app.clickup.com/90171457413/docs/2kza6fw5-21477. Su título histórico remite al estado anterior.
- El resumen de Tao en el CONTEXTO de `0c6722b` queda superado por este archivo, que es la respuesta más reciente. No se reescribió el historial científico del laboratorio para una reconsulta de estado.
- PR #27 permanece sin cambios. «Lista para depositar» de las respuestas anteriores queda retirado como veredicto científico. Los hashes y el determinismo siguen siendo evidencia sólo de integridad y render, no de validez científica.

### Siguiente paso propuesto, no ejecutado

Archivar lo que Tao ya hizo antes de pedirle más cómputo. Su paquete de siete objetos es:

1. Rama de auditoría del conectoma.
2. Archivo de auditoría en esa rama.
3. PR de auditoría, con review automático.
4. Doc completo en Space.
5. Rama documental de mudh-mobile.
6. Actualización únicamente de AGENT-TAO.md.
7. PR de continuidad, con review automático.

El detalle enlazado está en https://app.clickup.com/90171457413/chat/r/2kza6fw5-1037/t/80170050745296. No incluye merge, fixes ni Zenodo. BRAIN no envió autorización por Abraham. El pedido «REVISA DE NUEVO» se trató como lectura y verificación, no como confirmación de las siete escrituras.

Después de disponer de esa evidencia completa corresponde cotejarla, corregir lo confirmado en el PR #27, volver a verificar y recién entonces decidir el depósito. El criterio de prioridad es evitar publicar conclusiones que ya contradicen las tablas del propio manuscrito.

**Credenciales:** el Doc corrige el consejo previo de enviar el token por chat. Debe guardarse como secreto del entorno que ejecute el depósito, no en chats, Docs ni Git. La publicación también puede hacerse desde la sesión de Zenodo del titular sin compartir un token.

## 6. NO MEDIDO

- Cantidad de créditos de Tao, su atribución por corrida y el costo de los hallazgos nuevos. Un comentario no equivale a una ejecución; la ausencia de comentarios tampoco prueba ausencia de cómputo.
- Informe completo de Tao, comandos y salidas de los 100 grafos y los desbordamientos.
- Reproducción independiente de todos los bloques del laboratorio.
- Productor y trayectoria de Tabla 8 en este turno.
- Matriz original, nulos sobre FlyWire, fisiología, simulación robótica nueva, hardware o vuelo.
- Corrida de render tras correcciones, porque no se hicieron correcciones al manuscrito.
- Merge, borrador, depósito y publicación de Zenodo.

## Antes de firmar

```plain
Hay devolución nueva de Tao -> hilo de las 13:25 -> sí podía contradecir -> PASS documental
El spread de las cuatro filas es 2,4 -> Decimal sobre Tabla 5b -> sí -> FAIL, 4,160326
Tres modelos amplifican -> diferencias de Tabla 9 -> sí -> FAIL, LIF-soft decae
Los nulos de Tabla 5c sin umbral son constantes -> desviaciones publicadas -> sí -> FAIL, ambas positivas
Toda la auditoría quedó validada -> estos tres controles -> no -> NO MEDIDO
Los créditos se gastaron exactamente en esas acciones -> contador no consultado -> no -> NO MEDIDO
```

--- METODO PROMETEO ---
Acción delicada: NO (bitácora y adenda documental; sin orden a otro agente, merge ni publicación)
Modo aplicado: TITAN LIGERO, reconsulta acotada y controles de consistencia
Rúbrica: N/A (modo ligero; no se puntúa una auditoría integral que no se hizo)
Review externo: devolución de Tao consultada, informe completo pendiente de archivar
Instrumento: hilo de ClickUp, manuscrito en 554f7d9 y Python Decimal; exit=0; comando y salida completos en §4
Máquina: sandbox de ClickUp, con lecturas por GitHub y ClickUp
Artefactos: docs/agents/respuestas/2026-10-12-010-tao-si-dejo-hallazgos-la-v2-no-se-publica.md + https://app.clickup.com/90171457413/docs/2kza6fw5-21477
