# 2026-11-01-004 · Antecedentes leídos: una receta corta no garantiza menos cálculo

Doc: https://app.clickup.com/90171457413/docs/2kza6fw5-26157

## 1. Pedido y avance

Pedido: «CONTINUA», después de la explicación en criollo de Topo inverso. Se avanzó con el primer paso anunciado: leer los tres antecedentes directos y precisar qué nos falta probar. No se selló ni se ejecutó un experimento.

**La idea general de generar redes con descripciones pequeñas ya tiene antecedentes directos. Nuestra pregunta útil es más concreta: si una receta genera otros circuitos y conserva la ventaja funcional del embudo, con menos descripción total y sin ocultar su costo.** Aprender esa receta, conservar la función y ahorrar ejecución son afirmaciones distintas.

La lectura también corrige una frase de la respuesta 001: hay evidencia publicada sobre distancia y probabilidad de conexión entre neuronas de FlyWire adulto. Lo que sigue sin medir es nuestra implementación y réplica, no la existencia de ese antecedente.

## 2. Qué cambian los tres trabajos

### Shuvaev: comprimir una inicialización útil, no demostrar un cerebro barato

Se leyó el texto principal completo, incluidos métodos y discusión, de [Encoding innate ability through a genomic bottleneck, PNAS 2024](https://pmc.ncbi.nlm.nih.gov/articles/PMC11420173/).

Una red pequeña recibe identificadores de dos neuronas y produce el peso que las conecta en una red mayor. Alternan entrenamiento de la tarea y ajuste del generador a los pesos. La arquitectura de la red grande está fijada y la decodificación es determinista. No recupera genes reales.

En MNIST, 1.973 parámetros representan una red de 636.010: compresión declarada de 322 veces, con 94 % inicial frente a aproximadamente 98 % de la red entrenada. En CIFAR-10, 14.958 representan 1.369.738: 92 veces, con 76 % inicial frente a 89 % entrenado. Son resultados de los autores, no réplicas nuestras.

La descripción se expande en una red que todavía debe calcularse. El artículo no demuestra que comprimir los parámetros reduzca por sí solo el costo de inferencia. Tampoco todo se transfiere: la inicialización aprendida con MNIST no mejoró el aprendizaje de Fashion-MNIST. Mejor arranque no prueba una ventaja general de aprendizaje.

**Para nosotros:** contar programa, parámetros, etiquetas/mapas, excepciones y decodificador. Las etiquetas espaciales que recibe el generador aportan información. No anunciar menos cálculo contando solamente los parámetros de la receta.

El suplemento no quedó leído: su enlace de PMC devolvió HTML en lugar de PDF; una consulta alternativa de acceso abierto respondió 404. Se rechazó el formato. La lectura completa declarada es del artículo principal. No quedó establecido un repositorio oficial de implementación; no encontrarlo no prueba que no exista.

### Betzel: un comparador estructural, no 45 funciones demostradas

Se leyó el texto principal completo, métodos, limitaciones y leyendas suplementarias incorporadas de [Hierarchical Community Structure of the Adult Drosophila Connectome Reveals Conserved Circuit Archetypes, bioRxiv v2](https://www.biorxiv.org/content/10.64898/2025.12.10.689094v2.full-text). **La versión leída fue publicada el 17-jun-2026**; el preprint empezó en diciembre de 2025 y no tiene revisión por pares certificada.

Usa FlyWire adulto v783 sin umbral: 138.639 neuronas y 15.091.983 aristas. Identifica 1.449 comunidades finas mediante un modelo de bloques anidado, ponderado y corregido por grados. Después agrupa comunidades por 63 características. Los 45 arquetipos son meta-grupos estructurales, no 45 instrucciones generadoras ni funciones validadas. El texto advierte: «they do not necessarily constitute functional subunits».

**Corrección a la 001/002:** el artículo informa, a nivel neuronal, «connection probability decays monotonically with inter-soma distance» y remite a su figura S2. Entre pares conectados, la asociación del número de sinapsis con distancia somática es débil: r = 0,02 y rho = 0,04. Nuestro «en el adulto queda por medir» era demasiado amplio. Hay evidencia externa adulta; no demuestra una ley exponencial exacta, causalidad, distancia por arborizaciones ni que nuestro instrumento ya tenga geometría.

Se verificaron [datos y partición](https://zenodo.org/records/20399924) y [código v1.0](https://zenodo.org/records/20649529), ambos con licencia CC-BY-4.0. Las matrices grandes no se descargaron. El archivo de código resuelve al commit `a25219060f467ddf3ee5635bf59ee77c23450e5e`.

Se leyeron el [README fijado](https://github.com/rbetzel/fafb_nested_communities/blob/a25219060f467ddf3ee5635bf59ee77c23450e5e/README.md) y el [notebook de ajuste](https://github.com/rbetzel/fafb_nested_communities/blob/a25219060f467ddf3ee5635bf59ee77c23450e5e/py/sample_posterior_distribution_no_threshold.ipynb). El constructor especifica `deg_corr=True` y `rec_types=["discrete-geometric"]`. El README distingue análisis MATLAB con derivados precalculados de regenerar la partición.

**No está verificado como ejecutable de punta a punta.** El parser de Python encuentra un error de indentación en la celda 8 del notebook publicado: sintaxis válida en 14/15 celdas y una falla. No se ejecutó graph-tool ni se cargó ningún pickle. Esto se limita a ese archivo/commit, no refuta las cifras del artículo ni invalida por sí solo sus derivados publicados.

**Para nosotros:** la partición del grafo completo sirve para describir y explorar correspondencias, no para afirmar predicción ciega de sus propias aristas reservadas. Hay que ajustar usando solo entrenamiento o llamar al análisis condicionado/transductivo. Tampoco reemplazar comunidades por nodos funcionales automáticamente: se pueden perder interfaces necesarias de la tarea.

### Barabási: reglas que producen motivos, no nuestra función ni nuestro motivo

Se leyó el [artículo de Barabási y Barabási](https://doi.org/10.1016/j.neuron.2019.10.031), STAR Methods y el texto suplementario incluido en el [PDF de los autores](https://barabasi.com/media/pub_imports/files/1035.pdf), de 23 páginas. Publicación en línea en diciembre de 2019; volumen de Neuron de febrero de 2020.

Las identidades neuronales se representan por códigos de expresión. Operadores selectivos producen bicliques dirigidas: todas las conexiones de un conjunto de origen a uno de destino. Pueden solaparse. Es un antecedente directo de reglas compactas que generan motivos repetidos.

La parte de Drosophila usa un circuito olfativo/cuerpo pedunculado larval, no FlyWire adulto. Una biclique tampoco es nuestra plantilla S→D más S→X→D con signo inhibitorio predicho. Enriquecimiento y asociación con expresión no identifican por sí solos el mecanismo genético causal ni conservan la tarea de nuestro banco.

**Para nosotros:** aprovechar operadores compartidos sin presentar «reglas generadoras» como una idea nueva ni llamar genética a cualquier compresión.

## 3. Próxima prueba, más precisa pero no ejecutada

**Primero comprobaría si nuestro motivo agrega algo más que especialización por clase.** Criterio de prioridad: evitar construir una gramática sobre una señal que el control más pertinente podría explicar.

La relectura de [reuso_mosca.py](https://github.com/gatehot59-star/drosophila-fep-connectome/blob/c74509ac461bb1aa129f1a42dc9645d26b22f444/tools/reuso/reuso_mosca.py) muestra que el nulo permuta destinos en nueve bloques de lateralidad. Conserva el histograma de destinos por filas y mantiene origen, peso y signo de cada fila. Eso no equivale a preservar vecinos únicos después de agregar duplicados, fuerza ponderada de entrada ni el presupuesto de salida de cada X hacia descendentes.

H_REUSO_ESTRICTO necesita definir esas invariantes y demostrar mezcla sin congelar el estadístico. Para el análisis por superclase hay que conservar etiquetas e identidad: `armar` recibe `sc` pero no la retiene en el diccionario que devuelve; tampoco retiene allí los identificadores originales. No alcanza con cambiar el reporte. No carga geometría.

Este control condiciona la interpretación del motivo, **no bloquea por lógica construir G0**. Después:

1. G0 representa tipos/lado y grados o bloques sin usar anatomía reservada para ajustar sus componentes. G1 añade el motivo sobre la misma base y presupuesto.
2. Para explicar biología, congelar la regla antes de medir función. Para rediseñar, permitir ajuste funcional, pero evaluarlo en una prueba nueva y nombrarlo como ingeniería.
3. Medir por separado anatomía reservada, función/curva de pocos ejemplos, descripción completa y ejecución real. Contar también la información de etiquetas y particiones.
4. Si G0 iguala a G1, el motivo no se ganó su lugar. Si baja la descripción pero no RAM/tiempo, hay almacenamiento comprimido, no ejecución barata. Si funciona sin predecir anatomía, puede ser ingeniería útil sin explicar al animal.

Márgenes, particiones y semillas siguen sin sellar. BANC ya fue observado, no es un test virgen. Los negativos de compresión con MOSCA_L siguen pendientes; los históricos con W no se convierten en pruebas con lector entrenado por esta lectura.

## 4. Herramientas, máquina y evidencia

Fuentes primarias y GitHub; descargas públicas y extracción con requests, BeautifulSoup y pypdf en brain-env; AST de Python sobre el notebook exacto. GitHub y ClickUp para documentar. El cierre anclado, si se completa, se agrega al final con su propia ejecución y verificación.

No se entrenó una red, instaló graph-tool, descargaron las matrices grandes, usó Kaggle/GPU ni mergeó código. Leer un paper no replica sus resultados; AST no mide calidad del modelo ni convergencia.

Fuentes descargadas durante la lectura:

- Shuvaev HTML: 221.310 bytes; SHA256 `a0bdfee1646ae1221daed574e1c3c40e7f673920c0689a46c3ae108c6580954b`.
- Betzel v2 HTML: 594.891 bytes; SHA256 `144ba006466266178944590cdeaccd53aa0ac219e1066f45112eb637e0e9f2a6`.
- Barabási PDF: 2.591.763 bytes; SHA256 `a9c59bd05cae086af408907ddbb6b775f880b5699fa0eba3c47f03ebcb726067`.
- Notebook: 23.991 bytes; blob `dac5a96a926133a3fb68f535b960859c3b318e37`; SHA256 `f5ef5f1836d4729e8608d6d9d126d65deac77cfbcf9209b6ee4354329cd15768`.

Comprobación AST en brain-env, salida completa del registro de diagnóstico, no los outputs guardados por los autores. Se descargó el archivo fijado, verificó su blob y ejecutó `ast.parse(source, filename="cell_" + str(i))` por celda, sin `exec`, import de graph-tool ni deserialización de pickle. El programa exacto reproducible y el control del contexto se conservan en el instrumento enlazado por el cierre anclado.

```text
SOURCE https://raw.githubusercontent.com/rbetzel/fafb_nested_communities/a25219060f467ddf3ee5635bf59ee77c23450e5e/py/sample_posterior_distribution_no_threshold.ipynb
bytes=23991 git_blob=dac5a96a926133a3fb68f535b960859c3b318e37 sha256=f5ef5f1836d4729e8608d6d9d126d65deac77cfbcf9209b6ee4354329cd15768
cell=1 id=43edbff7 SYNTAX_PASS
cell=2 id=7b0d997f SYNTAX_PASS
cell=3 id=42f9a539 SYNTAX_PASS
cell=4 id=104654b8 SYNTAX_PASS
cell=5 id=50eddc8d SYNTAX_PASS
cell=6 id=ee448ed7 SYNTAX_PASS
cell=7 id=38332a1d SYNTAX_PASS
cell=8 id=78c9968d SYNTAX_FAIL IndentationError line=18 unexpected indent
SOURCE_BEGIN
# Filename for sampled partitions
filename = outputdir + 'sampled_partitions_no_threshold.pickle'

# Filename for nested blockstate after sampling procedure
filename2 = outputdir + 'state_after_sampled_partitions_no_threshold.pickle'

# Do both files already exist? If so ...
if os.path.isfile(filename) and os.path.isfile(filename2):

    # Load sampled partitions
    file = open(filename,'rb')
    # Load blockstate
    file = open(filename2,'rb')
    
else:state = pickle.load(file)

    # Define an empty list for storing partitions
    bs = []
    
    # Collect force_niter partitions
    gt.mcmc_equilibrate(state, force_niter=1000, mcmc_args=dict(niter=10),
                        callback=collect_partitions)
    
    # Save the sampled partitions
    with open(filename,'wb') as f:
        pickle.dump(bs,f,pickle.HIGHEST_PROTOCOL)

    # Save current blockstate
    with open(filename2,'wb') as f:
        pickle.dump(state,f,pickle.HIGHEST_PROTOCOL)
SOURCE_END
cell=9 id=929db638-97e1-48c9-9268-02e02e807a9a SYNTAX_PASS
cell=10 id=7f841bc6-6bac-4271-99c7-a60bf062618e SYNTAX_PASS
cell=11 id=94ac473f SYNTAX_PASS
cell=12 id=396dfc3c SYNTAX_PASS
cell=13 id=19d9ffd4 SYNTAX_PASS
cell=14 id=2914eaff SYNTAX_PASS
cell=15 id=9cbf2b9d SYNTAX_PASS
TOTAL code_cells=15 pass=14 fail=1
PARSER_POSITIVE pass
PARSER_NEGATIVE rejected
EXTERNAL_CODE_EXECUTED=false graph_tool_imported=false pickle_loaded=false
```

Log: 2.014 bytes; SHA256 `b46e4da1eb523d835f57d3594eec9bc4d91cd4d9cfd28413a0d7224e6fbe6ae5`. El proceso de diagnóstico terminó con exit=0 porque registró el resultado; el notebook evaluado tiene un FAIL de sintaxis, no un PASS de ejecución.

## 5. Archivos y estado documental

Esta respuesta: `docs/agents/respuestas/2026-11-01-004-antecedentes-leidos-compresion-no-es-ahorro-de-calculo.md`. Doc: el canónico de Topo inverso, en Space, sección 13. CONTEXTO se actualiza con un parche anclado separado y su cierre se agrega aquí; este primer commit no afirma que ese paso ya ocurrió. Las respuestas 001 a 003 permanecen como historia; esta 004 corrige explícitamente el alcance anterior.

No se modifica ningún sello, resultado experimental ni archivo de producto. No se borra la rama original ni se mergea un PR.

## 6. NO MEDIDO

Gramática aprendida; novedad global; H_REUSO_ESTRICTO y por superclase; superclase de AN_multi_11; réplica propia de geometría adulta; función en grafos generados; suplemento de Shuvaev; reproducción integral de los tres trabajos; ventaja de memoria/latencia/energía; validación fisiológica; revisión independiente.

La sintaxis fallida del notebook es **FAIL medido**, no NO MEDIDO. La disponibilidad de fuentes y archivos fue verificada. La eficacia de Topo inverso sigue **NO MEDIDA**.

--- METODO PROMETEO ---
Rol: lectura crítica y documentación focalizada.
Accion delicada: NO en esta publicación documental; el mantenimiento anclado tiene su propio cierre.
Modo aplicado: LIGERO; no revisión sistemática ni experimento.
Maquina: brain-env (lectura y AST), GitHub y ClickUp (documentación).
Rubrica: N/A para la lectura focalizada.
Review externo: no realizado; la misma instancia seleccionó e interpretó las fuentes.
Instrumento: textos completos principales y archivos fijados; ast.parse sobre las 15 celdas, salida íntegra arriba.
Artefactos: docs/agents/respuestas/2026-11-01-004-antecedentes-leidos-compresion-no-es-ahorro-de-calculo.md + https://app.clickup.com/90171457413/docs/2kza6fw5-26157

## 7. Cierre anclado: contexto y evidencia documental

El CONTEXTO incorpora la lectura principal, la corrección de distancia adulta, el límite de los arquetipos y el FAIL sintáctico. No cambia resultados experimentales. Esta sección se publica junto al CONTEXTO mediante push normal; la publicación se verifica leyendo main, no por el log.

Instrumento: https://github.com/gatehot59-star/drosophila-fep-connectome/blob/3e1c5adf5237816f6ac82ccca26d057d7f172698/.github/workflows/contexto-topo-2026-11-01.yml

Run: https://github.com/gatehot59-star/drosophila-fep-connectome/actions/runs/41318785055

Comando: Python embebido en ese workflow, CONTEXTO_MODE=apply. Salida completa:

```text
SOURCE https://raw.githubusercontent.com/rbetzel/fafb_nested_communities/a25219060f467ddf3ee5635bf59ee77c23450e5e/py/sample_posterior_distribution_no_threshold.ipynb
bytes=23991 git_blob=dac5a96a926133a3fb68f535b960859c3b318e37 sha256=f5ef5f1836d4729e8608d6d9d126d65deac77cfbcf9209b6ee4354329cd15768
cell=1 id=43edbff7 SYNTAX_PASS
cell=2 id=7b0d997f SYNTAX_PASS
cell=3 id=42f9a539 SYNTAX_PASS
cell=4 id=104654b8 SYNTAX_PASS
cell=5 id=50eddc8d SYNTAX_PASS
cell=6 id=ee448ed7 SYNTAX_PASS
cell=7 id=38332a1d SYNTAX_PASS
cell=8 id=78c9968d SYNTAX_FAIL IndentationError line=18 unexpected indent
SOURCE_BEGIN
# Filename for sampled partitions
filename = outputdir + 'sampled_partitions_no_threshold.pickle'

# Filename for nested blockstate after sampling procedure
filename2 = outputdir + 'state_after_sampled_partitions_no_threshold.pickle'

# Do both files already exist? If so ...
if os.path.isfile(filename) and os.path.isfile(filename2):

    # Load sampled partitions
    file = open(filename,'rb')
    # Load blockstate
    file = open(filename2,'rb')
    
else:state = pickle.load(file)

    # Define an empty list for storing partitions
    bs = []
    
    # Collect force_niter partitions
    gt.mcmc_equilibrate(state, force_niter=1000, mcmc_args=dict(niter=10),
                        callback=collect_partitions)
    
    # Save the sampled partitions
    with open(filename,'wb') as f:
        pickle.dump(bs,f,pickle.HIGHEST_PROTOCOL)

    # Save current blockstate
    with open(filename2,'wb') as f:
        pickle.dump(state,f,pickle.HIGHEST_PROTOCOL)
SOURCE_END
cell=9 id=929db638-97e1-48c9-9268-02e02e807a9a SYNTAX_PASS
cell=10 id=7f841bc6-6bac-4271-99c7-a60bf062618e SYNTAX_PASS
cell=11 id=94ac473f SYNTAX_PASS
cell=12 id=396dfc3c SYNTAX_PASS
cell=13 id=19d9ffd4 SYNTAX_PASS
cell=14 id=2914eaff SYNTAX_PASS
cell=15 id=9cbf2b9d SYNTAX_PASS
TOTAL code_cells=15 pass=14 fail=1
PARSER_POSITIVE pass
PARSER_NEGATIVE rejected
EXTERNAL_CODE_EXECUTED=false graph_tool_imported=false pickle_loaded=false
source_blob=af3b24335a8b33939c4c88710b2e2dbffe2e7e60
source_bytes=123453
anchor_1_count=1
anchor_2_count=1
anchor_3_count=1
anchor_4_count=1
anchor_5_count=1
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
source_drift=REJECTED source blob changed
repeat_application=REJECTED anchor_1: expected 1, got 0
negative_controls=12/12
historical_tail_bytes=119028
historical_tail_sha256=b6c9d0cf10d6dd0b4bb6f9abd6e39c4ac1891bf7c101f169cef4f38ca5b31fb5
historical_tail_unchanged=True
reverse_roundtrip=PASS
result_blob=68e8be1ef8d937d48e3c427de8617257ef44f0d2
result_bytes=124737
result_sha256=e31550410fa6602a745bf9546174fd0885f9494189de8a2e77ea092da70d8e76
git_hash_object=68e8be1ef8d937d48e3c427de8617257ef44f0d2
target_readback_equal=True
```

La respuesta original 004 se conserva como prefijo byte a byte; este cierre se agrega. El workflow queda en su rama, sin permisos nuevos, sin merge, sin force y con solo dos rutas staged.

QA de mantenimiento: preflight 57/60 (95/100): completitud 15/15, ejecutabilidad 14/15, seguridad 14/15, documentación 10/10, proceso QA 4/5. Evidencia: ejecución previa del programa, cinco anclas, doce rechazos, reversión exacta y cola idéntica, YAML/shell/AST verificados, checkout fijado y rutas acotadas. Descuentos por runner todavía pendiente en preflight y falta de selección independiente de controles. N/A 40 puntos de testing, arquitectura, DevOps e innovación de producto. Este score no valida la hipótesis científica.

--- METODO PROMETEO ---
Accion delicada: SI, mantenimiento del workflow documental existente, sin permisos nuevos.
Modo aplicado: FULL.
Maquina: brain-env (preflight), Actions x64 (parche y AST), ClickUp (Doc).
Rubrica: 57/60, 95/100; N/A 40 puntos de producto.
Review externo: no realizado; sin independencia de selección o interpretación.
Instrumento: workflow fijado y salida completa arriba.
Artefactos: docs/agents/respuestas/2026-11-01-004-antecedentes-leidos-compresion-no-es-ahorro-de-calculo.md + https://app.clickup.com/90171457413/docs/2kza6fw5-26157
