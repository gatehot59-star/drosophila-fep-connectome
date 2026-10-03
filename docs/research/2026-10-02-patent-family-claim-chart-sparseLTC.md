# Claim chart por familia patentaria: SparseLTC

**Fecha de corte:** 2026-10-02 ART  
**Objeto:** comparar las reivindicaciones y núcleos técnicos de familias públicas cercanas al puente conectoma→red líquida→compilación→control.

> **Aviso:** esto es un chart técnico preliminar, no una opinión legal, claim construction, patentabilidad, infracción ni freedom-to-operate. Las familias se agrupan con la lógica de familia simple/PCT cuando la información pública lo permite; las bases pueden mostrar miembros distintos según usen familia simple, nacional o INPADOC extendida.

## Veredicto ejecutivo

El claim amplio **«usar un conectoma para crear una red neuronal» ya está muy trabajado**. La familia Google de connectomics-based neural architecture search es el principal choque conceptual; X Development cubre una variante de brain emulation con parámetros de conectividad y atención; Accenture cubre un controlador SNN basado en un circuito sensorimotor conectómico; Qualcomm/Brain Corp cubre una capa de descripción/compilación neuromórfica; PROME cubre una emulación artificial connectome de entrada sensorial a salida motora; y Knowmtech tiene un antecedente histórico de LSM física, hoy expirado.

La posición defendible para SparseLTC no es reclamar cualquiera de esas piezas por separado. Es reclamar, si los datos y la búsqueda profesional lo sostienen, una **combinación técnica estrecha**:

> máscara de conectividad biológica versionada y no expandible, parámetros dinámicos líquidos definidos por ecuación, propagación sparse compilada, contrato reproducible de solver/cuántización/provenance y validación por null estructural y perturbación.

Ese conjunto **no fue localizado reunido en las reivindicaciones independientes revisadas**, pero la ausencia no equivale a novedad legal.

## Cómo leer el chart

- **Sí:** el núcleo técnico aparece expresamente en el claim independiente o en el núcleo inequívoco de la familia.
- **Parcial:** aparece como modalidad, descripción o claim dependiente, pero no es el centro mínimo del claim independiente.
- **No:** no fue localizado en el claim independiente revisado.
- Las reivindicaciones se **parafrasean** para hacerlas comparables; no se sustituyen por el texto legal completo.

## Familias revisadas

| ID | Familia representativa y prioridad | Miembros públicos destacados | Estado observado | Núcleo de reivindicación independiente |
|---|---|---|---|---|
| F1 | **Google: Connectomics-based neural architecture search**, prioridad 2018-05-21 | US12050991B1; WO2019209820A1; EP3785231A1; CN112204620B; JP7039153B2; AU2019257675B2 | US listada activa; PCT cesada; miembros nacionales con estados propios | Obtener datos de conectómica y ejecutar NAS sobre un espacio restringido por esos datos para generar arquitecturas ANN; motivos conectómicos pueden guiar la búsqueda |
| F2 | **X Development: Attention-based brain emulation neural networks**, prioridad 2021-12-21 | US20230196059A1; familia extranjera no confirmada en este corte | Solicitud US listada pending | Procesar una entrada secuencial con encoder/decoder y atención; parámetros de capas, inicializados desde un grafo de conectividad sináptica, representan conexiones biológicas |
| F3 | **Accenture: Neuromorphic smooth control of robotic arms**, prioridad 2021-08-02 | US12070858B2; US20230029494A1; EP4129580B1 | US listada activa; EP con patente concedida | Controlar una articulación mediante SNN con proprioceptores de posición/velocidad, neuronas motoras extensor/flexor y señal de actuación derivada de spikes y error de posición |
| F4 | **Qualcomm/Brain Corp: High level neuromorphic network description apparatus and methods**, prioridad 2011-09-21 | US10210452B2; parent US9104973B2; WO2013138778A1; EP2825974A4; CN104620236B; familia relacionada US9652713B2 | US listada activa, expira 2032 según registro público | Representar una red mediante instrucciones de un lenguaje/IR, compilarla a formato independiente de hardware y convertirla en instrucciones ejecutables; nodos, conexiones, tags y selección de subconjuntos |
| F5 | **PROME: Artificial connectomes**, prioridad provisional 2017-06-08 | US20180357545A1; prioridad provisional 62/516,920 | US listada abandoned | Crear/usar un connectome artificial: entrada sensorial codificada, red de neuronas con umbrales/pesos y dinámica temporal, salida motora física/virtual y feedback; incluye plasticidad/crecimiento en la descripción |
| F6 | **Knowmtech: Physical neural network liquid state machine utilizing nanotechnology**, prioridades 2002 | US7392230B2 y familias/continuaciones relacionadas US6889216B2, US7752151B2, US7827131B2, US9104975B2, US9269043B2, US9679242B2 | US7392230B2 listada expired-lifetime desde 2023 | LSM física con conexiones moleculares/nanoconductores y mecanismo de aprendizaje supervisado/fading memory |

### Exclusión importante: LTC fundacional

La publicación de Hasani et al. sobre LTC es un paper, no una familia patentaria pública localizada en este corte. El CV público de Hasani menciona una provisional posterior sobre algoritmos sparse closed-form, pero una provisional no publicada no permite hacer un chart de reivindicaciones público ni debe tratarse como patent family confirmada.

## Chart de elementos técnicos

| Elemento | F1 Google NAS | F2 X brain emulation | F3 Accenture SNN control | F4 HLND/END | F5 PROME | F6 LSM física | SparseLTC actual/propuesto |
|---|---:|---:|---:|---:|---:|---:|---:|
| Grafo de conexiones biológicas como entrada | Sí | Sí | Parcial | No específico | Parcial, reglas animales | No | Sí |
| Máscara fija de aristas y ceros fuera de la conectividad | Parcial | Sí | No | Parcial | Parcial | No | Sí, requisito de diseño |
| Buscar/generar nuevas arquitecturas desde el grafo | Sí | Parcial | No | No | No | No | No, compilación determinista |
| Motivos conectómicos como semillas o restricciones de NAS | Sí | No | No | No | Parcial, reglas/motivos | No | Biblioteca de motivos, pero no NAS |
| Dinámica continua con tau dependiente de estado/entrada | No | No localizado | No, LIF/SNN | No específico | No, umbral/peso | No, LSM/fading memory físico | Sí, núcleo LTC/SparseLTC |
| Solver temporal explícito y reproducible | No | No localizado | Parcial, dinámica SNN | No | Parcial | Parcial | Sí, debe formar parte del manifest |
| Propagación sparse compilada | No específico | Matriz/grafo, no compiler sparse | Hardware SNN, no SparseLTC | Sí, compilación general | Adyacencia/mensajería | Hardware molecular | Sí, CSR/CSC o backend equivalente |
| IR o lenguaje hardware-independent | No | No | No específico | Sí | No específico | No | Sí, reutilizar NIR/NeuroML y sidecar |
| Entrada sensorial→salida motora en la misma reivindicación | No | Predicción ANN | Sí | Opcional | Sí | No | No como claim principal; DBC3 separado |
| Control robótico | No | No | Sí | Opcional | Sí, robot/virtual | No | DBC3, todavía no end-to-end biológico medido |
| Plasticidad/growth de la red | No | No | Parcial, ajuste PSI | Sí como instrucción posible | Sí en descripción | Aprendizaje de conexiones | No en producto base |
| Provenance, hashes, null estructural y perturbación causal | No localizado | No localizado | No localizado | No localizado | No localizado | No localizado | Sí como contrato de evidencia propuesto |
| Hardware molecular/físico | No | No | No | No | No | Sí | No |

## Chart por familia y diseño-around

### F1. Google, connectomics-based neural architecture search

**Claim independiente representativo, parafraseado:** obtener datos que describen conexiones entre neuronas biológicas y ejecutar una búsqueda de arquitectura neuronal cuyo espacio está restringido por esos datos; la familia añade motivos, geometría, biophysics/activity side information y arquitecturas construidas por combinación de motivos.

**Solapamiento con SparseLTC:** alto en el uso del conectoma como fuente de estructura; bajo en el mecanismo si SparseLTC no busca arquitecturas y solo compila una topología ya decidida.

**Diseño-around técnico:** no hacer NAS ni generar candidatos para seleccionar el de mejor métrica. Definir de antemano la máscara de aristas, los parámetros compartidos y la ecuación LTC; producir un artefacto determinista y auditable. La biblioteca de motivos debe ser un catálogo validado, no un motor de búsqueda de arquitecturas.

**Riesgo:** una implementación futura que extraiga motivos y los use como semillas para evolución/RL/NAS se acercaría mucho más a esta familia.

### F2. X Development, attention-based brain emulation

**Claim independiente representativo, parafraseado:** procesar una secuencia con bloques encoder y decoder; aplicar atención; usar parámetros de capas que, al inicializarse, representan un grafo de conectividad sináptica entre elementos neuronales biológicos. La especificación contempla pesos cero para pares sin conexión, pesos no cero para conexiones y parámetros estáticos durante training.

**Solapamiento con SparseLTC:** medio en grafo biológico→parámetros y ceros fuera de aristas; bajo en la arquitectura porque SparseLTC no es un transformer encoder/decoder ni usa atención como núcleo.

**Diseño-around técnico:** no usar bloques de atención, query/key/value ni encoder/decoder brain-emulation; usar recurrencia continua sobre la máscara sparse, con estado y tau documentados. DBC3 debe permanecer como readout/controlador separado, no como attention brain-emulation layer.

**Riesgo:** si se implementa una cabeza de atención cuyos pesos se inicializan directamente desde FlyWire, el chart cambia a solapamiento alto en esa parte.

### F3. Accenture, neuromorphic smooth control

**Claim independiente representativo, parafraseado:** recibir un objetivo de una articulación, comparar objetivo y valor actual, y producir actuación mediante un SNN que contiene proprioceptores de posición/velocidad, neuronas motoras extensor/flexor y patrones de spikes; las dependientes incluyen inhibición presináptica, coordinación multiarticulación y reducción de overshoot.

**Solapamiento con SparseLTC/DBC3:** medio solo si el producto se concreta como controlador SNN de articulación con esa microarquitectura. SparseLTC como compilador de dinámica no contiene esa organización.

**Diseño-around técnico:** no copiar la microarquitectura posición/velocidad + extensor/flexor + PSI. Mantener DBC3 como controlador compacto con interfaz de features explícita y medir su contrato propio. No afirmar que DBC3 es una réplica del connectome motor.

**Riesgo:** una integración end-to-end que compile un circuito FlyWire en una red spiking para control de brazo puede entrar en el mismo campo, aunque no sea literalmente la arquitectura descrita.

### F4. Qualcomm/Brain Corp, HLND/END

**Claim independiente representativo, parafraseado:** representar una red por instrucciones de un lenguaje de alto nivel; crear nodos y conexiones, seleccionar subconjuntos por tags/Boolean expressions y compilar la representación a un formato hardware-independent y luego a instrucciones de CPU/GPU/FPGA.

**Solapamiento con SparseLTC:** alto en la capa genérica “descripción de red→compilación”, bajo si SparseLTC aporta una semántica distinta y usa estándares/IR existentes.

**Diseño-around técnico:** no copiar sintaxis, tags, keywords ni arquitectura HLND/END. Definir un contrato de compilación centrado en conectoma versionado, unidades LTC, CSR/CSC, solver, cuantización, hashes y equivalencia. Usar NeuroML/LEMS para semántica de modelo y NIR cuando sus primitives alcancen; declarar custom primitive cuando no alcancen.

**Riesgo:** una reivindicación amplia de “compilar una red neuromórfica descrita a instrucciones hardware-independent” es territorio trabajado. La ventaja tiene que estar en la combinación conectome-liquid-evidence, no en el compilador genérico.

### F5. PROME, artificial connectomes

**Claim independiente representativo, parafraseado:** codificar datos sensoriales, pasarlos por un artificial connectome basado en reglas de cableado/modulación animal, producir movimiento físico/virtual y retroalimentar la entrada. La descripción añade neuronas con umbral, pesos excitatorios/inhibitorios, acumuladores temporales, plasticidad y crecimiento de conexiones.

**Solapamiento con SparseLTC:** medio en el concepto entrada→red→salida y bajo en la implementación actual porque SparseLTC no crea un artificial connectome autorregenerativo ni pretende emular conducta completa.

**Diseño-around técnico:** no reclamar “emular cualquier sistema nervioso animal” ni plasticidad/growth genéricos. Reclamar, si corresponde, compilación de una estructura medida y versionada a una dinámica líquida con evidencia y límites; DBC3 queda como consumidor de features, no como connectome artificial completo.

**Estado:** la solicitud US está listada abandoned; sigue siendo disclosure/prior art técnico, no una patente US activa según el registro consultado.

### F6. Knowmtech, physical LSM

**Claim independiente representativo, parafraseado:** construir una red física con conexiones moleculares/nanoconductores entre electrodos, asociar un mecanismo de aprendizaje supervisado y obtener fading memory de LSM.

**Solapamiento con SparseLTC:** prácticamente nulo: SparseLTC es software/compilación digital y no usa nanoconductores, solvente dieléctrico ni hardware molecular.

**Diseño-around:** no hace falta un diseño-around específico; evitar lenguaje de physical/molecular LSM si no se implementa.

**Estado:** la patente representativa está listada expired-lifetime desde 2023. Se conserva como antecedente histórico de “liquid state machine” física, no como barrera activa.

## Matriz de reivindicación candidata para SparseLTC

Estas son **temáticas de claim**, no texto final de una solicitud:

| Elemento candidato | Razón técnica | Familias que lo rozan | Cómo hacerlo defendible |
|---|---|---|---|
| Ingesta de un conectoma versionado con IDs, contactos, signos, tipos, hashes y población | Evita que el atlas sea una matriz anónima | F1, F2, F5 | No limitarse a “datos de conectómica”; exigir provenance y contrato de población |
| Máscara de aristas fija y no expandible durante la compilación | Diferencia compilador determinista de NAS | F1, F2, F4 | Mostrar fail-closed ante aristas fuera de M y prueba negativa |
| Dinámica líquida con tau/estado dependiente de entrada, estado y parámetros compartidos | Núcleo matemático SparseLTC | LTC como literatura, no familia patentaria pública confirmada; F2 solo tangencial | Definir ecuación, unidades, solver, cotas y equivalencia numérica |
| Propagación CSR/CSC o event/sparse con complejidad y memoria medidas | Efecto técnico de escala | F4, F6 indirecto | Medir coste por segundo biológico, bytes, aristas visitadas y backend |
| Sidecar de evidencia: solver, seed, quantización, null, perturbación, hashes y verdict | Convierte el compilador en instrumento reproducible | No localizado en las familias revisadas | Especificar schema y validadores; no venderlo como novedad patentaria sin buscar más |
| Exportación a NIR/NeuroML o backend custom con equivalencia contra referencia | Interoperabilidad y despliegue | F4, NIR/NeuroML como estándares | Separar semántica del modelo, target y prueba de equivalencia |
| Validación por rewiring/null estructural y silenciamiento | Conecta compilación con afirmación mecanística | No localizado en claims revisados | Mantener H4 fuerte como NO MEDIDA hasta ejecutarlo; evitar claim de causalidad prematuro |
| DBC3 como readout/controlador separado | Reduce mezcla de claims y de evidencia | F3 | Reivindicar interfaz y contrato del controlador, no “cerebro completo” |

## Decisión operativa

1. **No presentar claim amplio** de “conectoma→red neuronal” o “conectoma→controlador”: F1, F2, F3 y F5 ya ocupan ese terreno.
2. **No presentar el compilador genérico** como novedad: F4 lo trabaja desde 2011.
3. **Congelar una reivindicación técnica estrecha** alrededor de la combinación medible: máscara fija + dinámica líquida + propagación sparse + manifest de evidencia + equivalencia/perturbación.
4. **No incluir ComplexVectorLTC** en una solicitud de producto hasta que pase su gate experimental; la decisión vigente lo deja fuera.
5. **Hacer una búsqueda profesional por claims** en US/WO/EP/CN/JP antes de presentar; las familias y estados de Google Patents son un punto de partida, no clearance.

## Fuentes y límites

- [US12050991B1](https://patents.google.com/patent/US12050991B1/en)
- [WO2019209820A1](https://patents.google.com/patent/WO2019209820A1/en)
- [US20230196059A1](https://patents.google.com/patent/US20230196059A1/en)
- [US12070858B2](https://patents.google.com/patent/US12070858B2/en)
- [US10210452B2](https://patents.google.com/patent/US10210452B2/en)
- [US20180357545A1](https://patents.google.com/patent/US20180357545A1/en)
- [US7392230B2](https://patents.google.com/patent/US7392230B2/en)
- [EPO: definición de familias](https://www.epo.org/en/searching-for-patents/helpful-resources/first-time-here/patent-families)
- [WIPO: conceptos de familia PCT](https://www.wipo.int/edocs/mdocs/pct/en/wipo_pct_lua_22/wipo_pct_lua_22_t2.pdf)

**Límites:** no se revisaron expedientes completos de prosecution, reivindicaciones enmendadas de todas las jurisdicciones, maintenance fees, oposiciones ni litigios. El chart no determina patentabilidad, infracción ni libertad de operación.