# 2026-11-01-002 · CONTEXTO actualizado con Topo inverso corregido

Doc: https://app.clickup.com/90171457413/docs/2kza6fw5-26157

## 1. Pedido
«Apply the anchored CONTEXTO patch». Actualizar el contexto canónico con la respuesta corregida y su auditoría, sin reescribir el contenido histórico ni ejecutar experimentos.

## 2. Herramientas y máquina
GitHub para lectura y publicación; brain-env para preflight de solo lectura; GitHub Actions x64, ubuntu-24.04, para aplicar el parche; ClickUp para registrar el cierre en el Doc existente. Repositorio público. Sin GPU, secretos nuevos, instalaciones ni merges de código.
Instrumento: https://github.com/gatehot59-star/drosophila-fep-connectome/blob/14663d9f1e3f6171613c2e5f1098b2b56e180d14/.github/workflows/contexto-topo-2026-11-01.yml
Run: https://github.com/gatehot59-star/drosophila-fep-connectome/actions/runs/41317059602

## 3. Qué se midió
Tres anclas únicas, una transformación positiva y ocho controles negativos que rechazan entradas inválidas. Igualdad byte a byte de la cola histórica; reversión exacta de los tres cambios. El blob calculado por Python coincide con git hash-object. Este recibo y el CONTEXTO se publican juntos, mediante push normal sin force.
La publicación se verifica leyendo el commit y su diff desde main. La existencia de este recibo en main documenta la publicación; el log de preflight por sí solo no la prueba.

## 4. Evidencia cruda
Comando: Python embebido en el workflow enlazado; CONTEXTO_MODE=apply.
```text
source_blob=008b1533cf85700cce7de870e67959f44a87f2ba
source_bytes=119820
source_md5=de0f8711db31d4d90dbdfde7847d1bc5
anchor_1_count=1
anchor_2_count=1
anchor_3_count=1
positive_transform=PASS
missing_anchor_1=REJECTED anchor_1: expected 1, got 0
duplicate_anchor_1=REJECTED anchor_1: expected 1, got 2
missing_anchor_2=REJECTED anchor_2: expected 1, got 0
duplicate_anchor_2=REJECTED anchor_2: expected 1, got 2
missing_anchor_3=REJECTED anchor_3: expected 1, got 0
duplicate_anchor_3=REJECTED anchor_3: expected 1, got 2
source_drift=REJECTED source blob changed
repeat_application=REJECTED anchor_1: expected 1, got 0
negative_controls=8/8
historical_tail_bytes=119028
historical_tail_sha256=b6c9d0cf10d6dd0b4bb6f9abd6e39c4ac1891bf7c101f169cef4f38ca5b31fb5
historical_tail_unchanged=True
reverse_roundtrip=PASS
result_blob=af3b24335a8b33939c4c88710b2e2dbffe2e7e60
result_bytes=123453
result_md5=500b14860ecad3d470da0fbfa79777dc
evidence_blob=e9d3a7fd527277e0e74395dbeadc37a70b52d4ba docs/agents/respuestas/2026-11-01-001-topo-inverso-gramatica-funcional-por-medir.md
evidence_blob=9493ee43d8b18f16f758979e46a240259ef60a12 docs/auditorias/2026-11-01-01-topo-inverso-numeros-bien-bitacora-fuera-de-main.md
git_hash_object=af3b24335a8b33939c4c88710b2e2dbffe2e7e60
target_readback_equal=True
```

## 5. Archivos
- docs/agents/CONTEXTO-drosophila-fep.md
- docs/agents/respuestas/2026-11-01-002-contexto-topo-inverso-actualizado.md
El workflow permanece solo en titan/contexto-topo-2026-11-01. No se incorpora a main ni se borra. La rama original de la primera respuesta se conserva.
El nuevo bloque remite a la respuesta 001 y a su auditoría. Registra H_REUSO_ESTRICTO, H_REUSO por superclase, lectura completa de los tres antecedentes antes de sellar, alcance W frente a MOSCA_L y la propuesta G0/G1 como pendientes.

## 6. NO MEDIDO
Gramática aprendida, novedad, ventaja funcional o de compresión; control estricto y superclases; repetición con MOSCA_L; nuevos resultados científicos. Revisión independiente no realizada. Los resultados históricos no cambian.
El PR #2 abierto también contiene una versión del CONTEXTO; no se modifica ni se mergea. El guard de blob fija el estado leído de main y rechaza cualquier deriva posterior.

## QA proporcional
FULL por el workflow de mantenimiento. Preflight: 57/60 (95/100): completitud 15/15, ejecutabilidad 14/15, seguridad 14/15, documentación 10/10, proceso QA 4/5. Evidencia: tres anclas y ocho rechazos en el log, cola histórica y reversión exactas, YAML y shell comprobados antes del push, checkout fijado por SHA, permiso contents:write limitado al job documental, dos rutas permitidas y push sin force. Las deducciones reflejan que antes del push todavía faltaba la ejecución del runner y no hubo revisión independiente. Los 40 puntos de testing de producto, arquitectura, DevOps de producto e innovación son N/A: no se entrega producto ni experimento.

--- METODO PROMETEO ---
Rol: documentación e instrumento de mantenimiento.
Delicado: sí, workflow nuevo en rama de trabajo; autorización: pedido de aplicar el parche anclado.
Modo: FULL. Rúbrica de preflight: 57/60, 95/100; N/A: 40 puntos.
Review externo: no realizado; no se presenta esta verificación como independiente.
Máquinas: brain-env (preflight), Actions x64 (aplicación), ClickUp (Doc).
Instrumento: workflow enlazado y evidencia cruda de esta sección 4.
Archivo: docs/agents/respuestas/2026-11-01-002-contexto-topo-inverso-actualizado.md
Doc: https://app.clickup.com/90171457413/docs/2kza6fw5-26157
