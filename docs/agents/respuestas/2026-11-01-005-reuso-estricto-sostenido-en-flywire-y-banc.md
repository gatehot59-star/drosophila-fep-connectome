# 2026-11-01-005 · H_REUSO_ESTRICTO se sostiene en FlyWire y BANC

Doc: https://app.clickup.com/90171457413/docs/2kza6fw5-26157

## 1. Pedido y veredicto

Pedido literal: «Run H_REUSO_ESTRICTO before designing G1».

**Ejecutado: H_REUSO_ESTRICTO SOSTENIDA en ambos conectomas, con corrida VÁLIDA.** Preservar el presupuesto de salida de cada neurona por superclase y lado del destino no eliminó el exceso del motivo bajo este nulo. Ninguno de los 200 barajados de cada conectoma alcanzó al real en ninguna de las dos métricas. Las cuatro p ajustadas por Holm son 4/201 = 0,01990049751243781.

**G1 no fue diseñado ni implementado.** El control anatómico solicitado está resuelto; el resultado permite conservar el motivo como candidato a probar, no afirmar que ya exista una gramática útil ni que vaya a ahorrar cálculo.

El sello se publicó antes del instrumento y de mirar resultados del nulo estricto. Los valores observados y BANC ya eran conocidos: no se presenta como descubrimiento ciego ni como un animal de prueba nunca visto.

## 2. Qué se midió

Se conservaron las poblaciones, los umbrales y las estadísticas del H_REUSO original. S es una unidad de tipo/lado de proyección visual; D, una unidad descendente del mismo lado. Hay al menos 20 sinapsis directas S→D y una vía S→X→D con al menos 5 sinapsis en cada tramo. X tiene signo inhibitorio predicho.

Corrección de categoría al releer el código: X excluye las neuronas pertenecientes a los conjuntos S/D **elegibles**, definidos con tipo y lado válidos. No excluye automáticamente a toda neurona de esas dos superclases. La redacción anterior «cualquier superclase salvo esas dos» era demasiado fuerte.

- **T1:** fracción de pares cableados elegibles que tienen la plantilla. El denominador se recalcula para cada barajado; no se fija al del grafo real.
- **T2:** cantidad de neuronas X que sirven a al menos dos **tipos** distintos de descendente, no sólo a dos unidades tipo/lado.

Resultados del [JSON íntegro del runner](https://github.com/gatehot59-star/drosophila-fep-connectome/blob/0bc09b6736e43b1ee66ac265a94f0fdfe91480f2/results/reuso_estricto_2026-11-01/estricto.json):

- **FlyWire, T1:** 880/996 = 88,35 % real; media estricta 61,17 %, máximo 64,22 %. T2: **698** real; media 565,02, máximo 607.
- **BANC, T1:** 622/753 = 82,60 % real; media estricta 35,68 %, máximo 39,68 %. T2: **419** real; media 112,385, máximo 141.
- Cada comparación tiene 0/200 barajados iguales o mejores: p unilateral por rango = 1/201, **no cero**. Holm sobre las cuatro pruebas, alfa 0,05: todas 4/201. Se mantuvo el plan de 200 por conectoma; no se agregaron muestras al ver el resultado.
- Los denominadores n_cab de los nulos fueron 1.582 a 1.682 en FlyWire y 877 a 937 en BANC. Por eso T1 no es un contraste con el mismo número de pares en cada red.

El control importó: la media nula de T2 sube de aproximadamente 128,6 a 565,02 en FlyWire y de 11,0 a 112,385 en BANC respecto del nulo original. La brecha se achica, sobre todo en FlyWire, pero sobrevive. Esto no autoriza decir que la clase no influye ni que todos los estadísticos nulos suben.

### Lo que preserva el nulo y lo que deja variar

Permuta los identificadores de destino dentro de estratos de lado del origen × lado del destino × superclase del destino. Cada sorteo parte de las filas originales; no hay cadena MCMC ni burn-in. Son 72 estratos en FlyWire y 143 en BANC. No se homogenizan nombres de clases entre atlas; las clases ausentes conservan una categoría propia.

Preserva el origen, peso y signo asociados a cada fila, el número de filas y presupuesto de peso saliente de cada origen por clase/lado del destino, y el histograma entrante por filas condicionado al lado del origen. Las invariantes de clase, lado, índices, histograma y mezcla se comprueban en **cada uno de los 400 nulos**. Los presupuestos salientes se recomputan por una vía adicional en el primero y el último de cada serie real y en los controles sintéticos.

No preserva grado de vecinos únicos después de agregar duplicados, fuerza ponderada entrante, tipo fino del destino, composición inhibitoria dentro de cada clase, superclase del origen de cada arista entrante, geometría ni contacto de arborizaciones. Puede generar duplicados y autoaristas. Es un nulo de filas ponderadas condicionado a clases, no un grafo simple con todos sus grados y fuerzas fijados.

Se verificaron 200 huellas de destinos distintas por conectoma. La fracción mínima cambiada entre todos los estratos funcionales evaluados fue 0,99448 en FlyWire y 0,99502 en BANC, sobre el umbral sellado de 0,5. T1 y T2 variaron: el estadístico no quedó fijado por construcción. Eso demuestra mezcla según esos controles, no una exploración de todo espacio de grafos posible.

### Superclases: se cerró la consulta descriptiva, no una hipótesis nueva

- Las 698 X compartidas de FlyWire: 662 `central`, 26 `visual_centrifugal`, 6 `ascending`, 4 `optic`.
- Las 419 de BANC: 398 `central_brain_intrinsic`, 18 `visual_centrifugal`, 3 `ascending`.
- **AN_multi_11 está anotada como `ascending` en ambos conjuntos.** Ya no queda como categoría inferida sólo por su nombre.

Estas son cuentas descriptivas del grafo observado. **H_REUSO estratificado por superclase y con S sensoriales sigue pendiente.** La composición no prueba inhibición local, actividad fisiológica ni equivalencia de etiquetas entre atlas.

## 3. Instrumentos, evidencia cruda y procedencia

La evidencia se conserva completa, sin sustituirla por este veredicto:

1. [Sello previo](https://github.com/gatehot59-star/drosophila-fep-connectome/blob/750f89adb4b8710bd0d4d7105af1c7073296dd90/tools/reuso/SELLO-ESTRICTO-2026-11-01.md), commit `750f89adb4b8710bd0d4d7105af1c7073296dd90`. Semillas inferenciales 12029/12030; humo ciego 912029/912030, dos sorteos por conectoma sin imprimir sus T1/T2/p.
2. [Instrumento ejecutado](https://github.com/gatehot59-star/drosophila-fep-connectome/blob/5497aa569450415b2101e2ea0f99680a3c540dbe/tools/reuso/reuso_estricto.py), SHA256 `a0d35aa1810e6513bbacaba36ce17b768c3792132cf86b20012ae2d754588083`. Reutiliza las métricas históricas fijadas por hash, sin editarlas.
3. [Workflow exacto](https://github.com/gatehot59-star/drosophila-fep-connectome/blob/5497aa569450415b2101e2ea0f99680a3c540dbe/.github/workflows/reuso-estricto.yml), SHA256 `7ff9f795c87c66fea676b0fdc80b7e987da353531188a27db45c148c62a72825`.
4. [Log íntegro de la corrida, incluidos controles y fallos inducidos](https://github.com/gatehot59-star/drosophila-fep-connectome/blob/0bc09b6736e43b1ee66ac265a94f0fdfe91480f2/results/reuso_estricto_2026-11-01/run.log), 379.396 bytes, SHA256 `00058fbd432f3d298c2d8edc7c5b4485f28ec95208413211fb1256f4d80a60f0`. El JSON enlazado en la sección 2 tiene 307.449 bytes, SHA256 `ffce074c422835b426c717902e0510d6bcdd130ecff45d9fccce25e182a89282`.
5. [Verificador separado](https://github.com/gatehot59-star/drosophila-fep-connectome/blob/6db5d089efa71199f775d1b6619b1cf9f790b7fe/tools/reuso/verificar_estricto.py), 8.719 bytes, SHA256 `41ab582abb40fb707cc3f17d18fccd6e35309561b5116254b51d96b06248a9ef`. No importa el productor: cuenta comparaciones racionales exactas, recompone Holm y contrasta cada fila real contra el log.
6. [Salida íntegra del verificador](https://github.com/gatehot59-star/drosophila-fep-connectome/blob/6db5d089efa71199f775d1b6619b1cf9f790b7fe/results/reuso_estricto_2026-11-01/verificacion.log), 2.537 bytes, SHA256 `7dc94d7832a52054368774c83e0de4ffaf093bdc4a94c9bcb4e7dbc488e039cc`. Ambos archivos publicados se descargaron y coincidieron byte a byte con los ejecutados.

Comando científico, con la variable D resuelta al directorio usado por el workflow:

```sh
python tools/reuso/reuso_estricto.py --mode full --inputs-dir /tmp/reuso-input --out results/reuso_estricto_2026-11-01/estricto.json
```

Comando registrado literalmente por el verificador; el archivo local con sufijo v2 tiene los mismos bytes que `tools/reuso/verificar_estricto.py` publicado:

```text
COMMAND ['/usr/local/bin/python3', 'verificar_estricto_v2.py', '--json', 'estricto.json', '--log', 'run.log']
NEGATIVE_REJECTED missing_draw incomplete plan
NEGATIVE_REJECTED changed_p Holm mismatch
NEGATIVE_REJECTED guard_disabled JSON and verbatim log disagree
NEGATIVE_REJECTED wrong_source source or seal mismatch
```

Cierre literal de ese log, cuyos datos intermedios están íntegros en el enlace:

```text
VERIFY_PASS 400/400 nulls; exact rational p; Holm; log parity; four negative controls

PROCESS_EXIT=0
```

El rechazo del recibo con guard apagado se produjo por discrepancia JSON/log. No se lo presenta como prueba aislada de la invariante del guard: esa capacidad de fallo se prueba con la mutación de código y las fixtures del instrumento.

### Pines de entrada

No se commitean los datasets ni binarios derivados. El sello y el JSON registran procedencia y pines completos. Bytes y SHA256 verificados:

- FlyWire connectivity: 100.804.642 bytes; `efeb23fb99098e9c390f6869969b2a121a2ee92c833cfc45ecb2c1d8e1af0347`.
- Anotaciones FlyWire: 31.718.505 bytes; `9a4f8b2f843196074431ebd7cd883536afa1be86c8a4ce90970441e8be81d1be`; revisión `17fc57722002e1a7d38cdd0c89ac382bf92718da`.
- Metadata BANC: 57.503.026 bytes; `86ccf5df0c67419f8c5f43e93a7ed38d23a080e9f7fde26737290252f3780098`.
- Aristas BANC: 359.161.658 bytes; `8c296e946f3c69a8c7222f30ad75fa8a98eeb189124fec6df829c9125f4be64b`.

FlyWire: 138.639 nodos y 15.091.983 filas. BANC: 188.508 entradas de metadata y 13.620.865 filas. El cargador histórico conserva categorías no neuronales/desconocidas de BANC: no se transforma ese total de metadata en una afirmación de pureza biológica.

## 4. Herramientas, máquinas y controles capaces de fallar

Se leyeron en vivo main, CONTEXTO, respuesta 004, inventario, ramas, PRs abiertos y la implementación original. GitHub publicó sello, código, workflow, resultados y este recibo. El gateway de build en brain-env preparó archivos, ejecutó pruebas y recomputó resultados. ClickUp registra el cierre en el Doc existente. No se modificaron PRs ajenos ni se fusionó código a main.

La corrida real fue [Actions x64, run 41320710194](https://github.com/gatehot59-star/drosophila-fep-connectome/actions/runs/41320710194), estado estructurado `completed / success`, intento 1. Job del 1-nov-2026, 15:20:19 a 15:27:26 UTC. Imagen `20261026.354.1`, ubuntu-24.04, 4 CPU, Python 3.12.14; numpy 2.5.3, pandas 3.0.5, pyarrow 25.0.1. Las versiones se consultaron en PyPI; su lista de vulnerabilidades estaba vacía, lo cual no equivale a una auditoría exhaustiva de seguridad.

El instrumento completo informó **396,725858829 s** y **3.048.200 KiB de RSS máximo (2,907 GiB)**. Son costos de este ensayo anatómico en esa máquina, no costos de una futura gramática. No se usó GPU ni Kaggle; el trabajo corrió en el repositorio público.

Controles y alcance:

- 25/25 comprobaciones del instrumento. Una envuelve las siete históricas: no son 32 pruebas independientes.
- Oráculo por enumeración de caminos distinto del productor: coincidencia en el grafo sintético y 39 nulos.
- Motivo plantado y motivo ausente: desenlaces SOSTENIDA y REFUTADA respectivamente en pruebas end-to-end de 200 nulos sintéticos.
- Sabotaje de la validación de clase: 23/25, fallan `old_SL_null_rejected` y `class_swap_rejected`, exit 3. La misma mutación se ejecutó en Actions antes del ensayo real.
- Humo ciego: 2/2 sorteos válidos en cada conectoma. Corrida real: 400/400 completos, distintos dentro de cada serie y con guards aprobados.
- Cobertura sólo con fixtures: 247/391 sentencias, 63,17 % global; 100 % en `strict_null`, `guard`, `budgets`, `nonfrozen`, `complete_plan` y `naive_stats`. No se declara cobertura global del camino real de datos.
- Verificador separado: 400/400 filas conciliadas con el log, cuatro recibos corruptos rechazados, exit 0 para el válido.

Error de preparación registrado: el primer borrador del workflow tenía un terminador heredoc indentado y `bash -n` lo rechazó. Se corrigió antes de publicar y antes de la corrida real. El YAML final, ambos scripts Bash y ambos bloques Python pasaron; el bloque verificador se ejecutó sobre fixtures. No hubo una corrida científica fallida que luego se ocultara o reemplazara.

W-01: la ejecución y su salida cruda son comprobables; la selección de controles y la interpretación provienen de la misma instancia. **Esto no es una auditoría independiente ni una réplica por otro investigador.**

## 5. Archivos generados y estado de publicación

Rama experimental `titan/reuso-estricto-2026-11-01`, desde la base histórica `c74509ac461bb1aa129f1a42dc9645d26b22f444`:

- Sello: `tools/reuso/SELLO-ESTRICTO-2026-11-01.md`, commit `750f89adb4b8710bd0d4d7105af1c7073296dd90`.
- Código y workflow: `tools/reuso/reuso_estricto.py` y `.github/workflows/reuso-estricto.yml`, commit `5497aa569450415b2101e2ea0f99680a3c540dbe`.
- Evidencia del runner: `results/reuso_estricto_2026-11-01/estricto.json` y `run.log`, commit `0bc09b6736e43b1ee66ac265a94f0fdfe91480f2`.
- Verificador y evidencia de lectura: `tools/reuso/verificar_estricto.py` y `results/reuso_estricto_2026-11-01/verificacion.log`, commit `6db5d089efa71199f775d1b6619b1cf9f790b7fe`.

Este commit documental de main agrega `docs/agents/respuestas/2026-11-01-005-reuso-estricto-sostenido-en-flywire-y-banc.md`. El cierre de CONTEXTO se incorpora después mediante parche anclado y se registra como apéndice, sin reescribir este recibo. El Doc se actualiza en Space > Topo inverso > sección 14. La publicación no se considera completa hasta leer Git y Doc de vuelta.

No se modifica el instrumento original, no se hace merge y no se borra ninguna rama. El workflow científico rechaza una nueva ejecución automática si ya hay recibo.

## 6. NO MEDIDO y decisión que deja habilitada

- G1 sigue sin diseño, implementación, sello ni corrida. No se lo empieza por esta entrega.
- La aportación funcional del motivo frente a G0, la gramática aprendida, la conservación de H_PARES_DATOS y cualquier reducción de descripción, RAM, latencia o energía.
- Inferencia separada por superclase, S genuinamente sensoriales, sensibilidad a signos desconocidos y fisiología real.
- Nulos con oportunidades geométricas, fuerza entrante o grados de vecinos únicos preservados. El resultado no descarta esas explicaciones.
- Repeticiones con MOSCA_L de los negativos históricos de compresión.
- Validación en datos biológicos nuevos no observados; BANC no era virgen.
- Novedad global y revisión independiente.

La decisión respaldada es estrecha: **no descartar el motivo por la objeción concreta del presupuesto saliente por clase; conservarlo como candidato a una comparación futura.** No es evidencia de que todo el exceso sea inexplicable por controles aún no hechos, ni de causalidad, ni de que G1 vaya a ganar.

## 7. QA del instrumento y workflow

FULL por el nuevo workflow de ejecución. **58/60 = 96,7/100** sobre criterios aplicables. N/A 40 puntos de testing, arquitectura, DevOps e innovación de producto: se entrega un instrumento científico con workflow, no un producto desplegable. Los controles científicos y la cobertura se reportan arriba, no se esconden detrás del N/A.

- Completitud 15/15: sello previo, fuente completa, 200+200 muestras y logs íntegros, identificados en secciones 2 y 3.
- Ejecutabilidad 15/15: source/workflow publicados iguales a los probados, Actions completed/success y verificador exit 0.
- Seguridad 14/15: acciones fijadas por commit, entradas por hash, permisos ya acotados de escritura, sin secretos nuevos, publicación limitada a dos rutas de resultado; consultas de paquetes no constituyen un análisis exhaustivo de cadena de suministro.
- Documentación 10/10: contrato de seis campos, invariantes y no-invariantes, comandos, pines y límites en este recibo y el sello.
- Proceso QA 4/5: oráculo distinto, sabotaje real y recomputo separado con salida cruda. Falta selección e interpretación independientes.

El score evalúa la entrega técnica; no es la probabilidad de la hipótesis ni una autorización de merge. Afirmación anatómica → instrumento de nulos estrictos con controles positivo y negativo → podía refutarla → SOSTENIDA bajo el nulo especificado. Gramática útil o ejecución barata → ningún experimento adecuado todavía → NO MEDIDO.

--- METODO PROMETEO ---

Accion delicada: SI en el flujo completo, por el instrumento y su workflow; este commit agrega sólo documentación.
Modo aplicado: FULL.
Roles: lectura del repositorio, diseño del control, implementación, seguridad, pruebas, documentación y QA; misma instancia.
Maquina: brain-env para preparación y recomputo; Actions x64 para el ensayo; GitHub y ClickUp para publicación.
Rubrica: 58/60 = 96,7/100. N/A: 40 puntos de producto, justificados en sección 7.
Review externo: no realizado; no hay independencia de selección ni interpretación.
Instrumento: reuso_estricto.py, exit 0; verificar_estricto.py, exit 0; evidencia cruda completa enlazada en sección 3.
Artefactos: docs/agents/respuestas/2026-11-01-005-reuso-estricto-sostenido-en-flywire-y-banc.md + https://app.clickup.com/90171457413/docs/2kza6fw5-26157

## 8. Cierre anclado del estado 005

El CONTEXTO incorpora el control estricto ya ejecutado, la categoria ascending de AN_multi_11 y la definicion precisa de X. G1 sigue sin diseno. No se vuelve a ejecutar el experimento.

Instrumento: https://github.com/gatehot59-star/drosophila-fep-connectome/blob/4293ab19c91d101b1cf47a1f79ea5425e9395cbc/.github/workflows/contexto-topo-2026-11-01.yml

Run: https://github.com/gatehot59-star/drosophila-fep-connectome/actions/runs/41322130809

Comando: Python embebido en el workflow, CONTEXTO_MODE=apply. Salida completa:

```text
source_blob=68e8be1ef8d937d48e3c427de8617257ef44f0d2
source_bytes=124737
response_blob=974d9567a64d97032c9d69c29bac9bc40cbd1375
response_bytes=17279
anchor_1_count=1
anchor_2_count=1
anchor_3_count=1
anchor_4_count=1
anchor_5_count=1
anchor_6_count=1
positive_transform=PASS
missing_anchor_1=REJECTED anchor_1: expected 1, got 0
duplicate_anchor_1=REJECTED anchor_1: expected 1, got 2
missing_anchor_2=REJECTED anchor_2: expected 1, got 0
duplicate_anchor_2=REJECTED anchor_2: expected 1, got 2
missing_anchor_3=REJECTED anchor_3: expected 1, got 0
duplicate_anchor_3=REJECTED anchor_3: expected 1, got 2
missing_anchor_4=REJECTED anchor_4: expected 1, got 0
duplicate_anchor_4=REJECTED anchor_4: expected 1, got 2
missing_anchor_5=REJECTED anchor_5: expected 1, got 0
duplicate_anchor_5=REJECTED anchor_5: expected 1, got 2
missing_anchor_6=REJECTED anchor_6: expected 1, got 0
duplicate_anchor_6=REJECTED anchor_6: expected 1, got 2
source_drift=REJECTED source blob changed
repeat_application=REJECTED anchor_3: expected 1, got 0
negative_controls=14/14
historical_tail_bytes=119028
historical_tail_sha256=b6c9d0cf10d6dd0b4bb6f9abd6e39c4ac1891bf7c101f169cef4f38ca5b31fb5
historical_tail_unchanged=True
reverse_roundtrip=PASS
result_blob=f3bbbc2ecf9a3f6d05f5dbc84058201d5ecfdf2c
result_bytes=126524
result_sha256=9c24e919dcec1df4f009d0da91d7e63ea4c2bca0155b29ee24033ef910009413
git_hash_object=f3bbbc2ecf9a3f6d05f5dbc84058201d5ecfdf2c
target_readback_equal=True
```

Las seis anclas fueron probadas en copia antes de publicar; catorce entradas invalidas fueron rechazadas por el motivo esperado. Los 119.028 bytes historicos quedan identicos y la respuesta 005 anterior se conserva como prefijo exacto. Este cierre y CONTEXTO son las dos unicas rutas staged; push normal, sin force, permisos nuevos, merge ni cambios al ensayo cientifico. La publicacion efectiva se verifica leyendo main despues del push.

QA previa de mantenimiento: 57/60 (95/100): completitud 15/15, ejecutabilidad 14/15 por runner aun pendiente, seguridad 14/15, documentacion 10/10 y proceso 4/5 por falta de seleccion independiente. Evidencia: programa ejecutado en copia, seis anclas, catorce rechazos especificos, reversibilidad, cola y prefijo exactos, YAML/Bash/AST validos, checkout fijado y staged acotado. N/A 40 puntos de producto. No es una medida de probabilidad cientifica.

--- METODO PROMETEO ---
Accion delicada: SI, mantenimiento del workflow documental existente.
Modo aplicado: FULL.
Maquina: brain-env para preflight y Actions x64 para el parche.
Rubrica previa: 57/60 (95/100); N/A 40 puntos de producto.
Review externo: no realizado.
Instrumento: workflow y salida completa enlazados arriba.
Artefactos: docs/agents/respuestas/2026-11-01-005-reuso-estricto-sostenido-en-flywire-y-banc.md + https://app.clickup.com/90171457413/docs/2kza6fw5-26157
