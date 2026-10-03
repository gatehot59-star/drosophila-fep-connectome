# Conectoma medido + neuronas líquidas: exploración global

**Fecha:** 2026-10-02 ART  
**Objeto:** determinar si existe una línea global que combine un conectoma biológico medido, especialmente Drosophila/C. elegans, con LTC/LNN/LSM para emulación o control.

## Veredicto

La afirmación correcta no es «nadie lo hizo». Es más precisa:

> **La combinación estricta conectoma completo medido + LTC/CfC o Liquid State Machine explícita no aparece como una línea consolidada en las fuentes primarias revisadas.** Sí hay antecedentes muy cercanos: NCP sobre un circuito pequeño de C. elegans, conectomas con LIF, CTRNN, Wilson-Cowan, ESN/reservoir y redes mecanísticas diferenciables.

El hueco parece real, pero la ausencia se amplifica por terminología fragmentada. «Liquid» puede significar LTC/LNN, LSM spiking, dinámica continua o simplemente un sistema temporal; «connectome» puede significar una matriz celular medida, un circuito parcial, un grafo regional por MRI o una arquitectura inspirada en un animal.

## Qué sí existe

### 1. El antecedente más cercano: C. elegans y NCP

Lechner, Hasani y colaboradores conservaron la topología del circuito de retirada al toque de C. elegans, aproximadamente 11 neuronas y 28 conexiones, y usaron dinámica continua de conductancias para control robótico. Es una combinación genuina de circuito anatómico medido + dinámica neuronal adaptable, pero **no es el conectoma completo de 302 neuronas**.

- [Neuronal Circuit Policies](https://arxiv.org/abs/1803.08554)
- [Can a Compact Neuronal Circuit Policy be Re-purposed to Learn Simple Robotic Control?](https://arxiv.org/abs/1809.04423)
- [Designing Worm-inspired Neural Networks for Interpretable Robotic Control](https://doi.org/10.1109/ICRA.2019.8793840)
- [Implementación NCP/LTC/CfC](https://github.com/mlech26l/ncps)

El software NCP es una fuente frecuente de confusión: `AutoNCP` genera una topología estructurada inspirada en C. elegans; no equivale automáticamente a cargar la matriz anatómica medida del gusano.

### 2. Conectomas con reservoirs, ESN y LIF

- `conn2res` permite imponer conectomas y dinámicas configurables, incluyendo LIF y otras dinámicas, sobre varias especies. Es infraestructura de conectoma + reservoir, no una LTC sobre el conectoma completo.
  - [Suárez et al., Nature Communications 2024](https://doi.org/10.1038/s41467-024-44900-4)
  - [Repositorio conn2res](https://github.com/netneurolab/conn2res)
- Damicelli et al. construyen Bio-Echo State Networks a partir de conectividad cerebral real. Es conectoma + reservoir, pero ESN no LTC.
  - [Brain connectivity meets reservoir computing](https://doi.org/10.1371/journal.pcbi.1010639)
- Costi et al. usan el conectoma de Drosophila como reservoir para predicción de series temporales. La implementación concreta es ESN rate-based, no LSM spiking ni LTC.
  - [The Drosophila Connectome as a Computational Reservoir](https://doi.org/10.3390/biomimetics10050341)
- Morra y Daley imponen topología derivada del hemibrain de Drosophila sobre una ESN. Es un antecedente de conectoma + reservoir, no de neurona líquida.
  - [Imposing Connectome-Derived Topology on an Echo State Network](https://arxiv.org/abs/2201.09359)

### 3. Emulación de la mosca con otras dinámicas

- Neurokernel propuso una arquitectura GPU para integrar modelos de módulos del cerebro de Drosophila. Su valor está en la emulación y la interoperabilidad, no en una dinámica LTC uniforme.
  - [Neurokernel, PLOS ONE 2016](https://doi.org/10.1371/journal.pone.0146581)
- Shiu et al. construyeron un modelo LIF del cerebro adulto de Drosophila, usando más de 125.000 neuronas, conectividad EM y neurotransmisores predichos, y lo validaron con alimentación, grooming y optogenética. Es el precedente más fuerte de conectoma completo + simulación sensorimotora, pero no es LNN/LTC/LSM.
  - [A Drosophila computational brain model reveals sensorimotor processing](https://doi.org/10.1038/s41586-024-07763-9)
- Lappalainen et al. usaron conectividad medida en el sistema visual de la mosca y optimizaron un modelo mecanístico diferenciable para predecir actividad neuronal. La red cubre 64 tipos celulares y comparte parámetros para hacer el problema identificable; no es LTC.
  - [Connectome-constrained networks predict neural activity across the fly visual system](https://doi.org/10.1038/s41586-024-07939-3)
  - [Código FlyVis](https://github.com/TuragaLab/flyvis)
- Izquierdo y Beer usaron conectividad de C. elegans con CTRNN y ajuste evolutivo para producir klinotaxis. Es conectome-constrained dynamical modeling, pero no LTC.
  - [Connecting a Connectome to Behavior](https://doi.org/10.1371/journal.pcbi.1002890)

## Por qué la combinación no aparece más

### 1. El conectoma no determina la dinámica

El conectoma indica quién puede influir sobre quién, y a veces cuántos contactos hay. No entrega automáticamente, para cada neurona y sinapsis, tau, umbral, capacitancia, potencial de reposo, conductancia, retardo, signo funcional, receptores, plasticidad, gap junctions, neuromodulación ni estado basal.

La misma matriz puede sostener dinámicas distintas al cambiar parámetros intrínsecos y sinápticos. Beiran y Litwin-Kumar formalizan esta degeneración: un conectoma compartido no fija una única dinámica; unas pocas grabaciones de actividad reducen la ambigüedad.

- [Bargmann y Marder, 2013](https://doi.org/10.1038/nmeth.2451)
- [Beiran y Litwin-Kumar, Nature Neuroscience 2025](https://doi.org/10.1038/s41593-025-02080-4)

Por eso una LTC conectome-constrained no debe venderse como «la dinámica de la mosca» sin más restricciones. Es una **familia de modelos** con máscara estructural biológica.

### 2. Escala y entrenamiento

En FlyWire hay del orden de 139.000 neuronas y decenas de millones de contactos. La sparsity hace viable el forward disperso, pero no elimina:

- integración temporal por muchos pasos;
- memoria de estados para BPTT;
- ajuste de parámetros y pesos;
- irregularidad de accesos en grafos dispersos;
- incertidumbre sobre qué parámetros compartir;
- necesidad de repetir simulaciones para perturbaciones y nulls.

LIF es menos expresivo, pero permite recorrer el grafo completo y hacer predicciones de ablación. LTC ofrece adaptación temporal más rica, a costa de mayor problema de identificación y solver. CfC reduce parte del coste del solver, pero sus benchmarks no demuestran todavía escalabilidad sobre un conectoma completo.

- [Liquid Time-constant Networks](https://doi.org/10.1609/aaai.v35i9.16936)
- [Closed-form Continuous-time Neural Networks](https://doi.org/10.1038/s42256-022-00556-7)

### 3. LNN, LTC, LSM, LIF y CTRNN no son sinónimos

- **LIF:** modelo spiking simple, eficiente y fácil de escalar.
- **CTRNN:** ODE continua con tau y no linealidad; puede usar conectividad anatómica.
- **LTC/LNN:** dinámica continua con constantes de tiempo efectivas dependientes de estado/entrada; normalmente la topología se entrena o se diseña.
- **LSM:** reservoir spiking transitorio, usualmente fijo, con readout entrenado.
- **Conductance-based/HH:** dinámica biofísica de corrientes, canales y potenciales de reversión.

Un artículo que usa LIF sobre un conectoma no es automáticamente una LSM. Un NCP inspirado en C. elegans no es automáticamente el conectoma real. Un CTRNN que corre sobre una matriz anatómica no es automáticamente LTC.

- [Maass, Natschläger y Markram, Liquid State Machines](https://doi.org/10.1162/089976602760407955)
- [Hodgkin y Huxley](https://doi.org/10.1113/jphysiol.1952.sp004764)

### 4. Los campos validan cosas distintas

La literatura LNN suele optimizar error de series temporales, clasificación, estabilidad, latencia y parámetros. La literatura de conectomas necesita además predecir actividad retenida, perturbaciones, ablaciones, comportamiento y generalización entre animales, con rewiring y nulls apropiados.

Un modelo puede ganar accuracy y aun así no identificar una ruta biológica. Ese desacople explica por qué muchos grupos prefieren publicar primero un LIF o un modelo mecanístico sencillo, que pueda compararse con optogenética, actividad o comportamiento.

### 5. Hay una separación institucional de comunidades

Los grupos de conectómica suelen trabajar con neuroanatomía, simuladores spiking, circuitos y causalidad. Los grupos de LNN suelen trabajar con aprendizaje temporal, sensores, control y eficiencia. La intersección exige saber medir conectividad, construir solvers dispersos, entrenar dinámicas y diseñar validación neurobiológica. Es una frontera interdisciplinaria difícil, no una idea que falte por obvia.

## Qué significa para SparseLTC

La oportunidad es real, pero el claim correcto no es «somos los primeros del mundo» todavía. Es:

> **SparseLTC puede ocupar la intersección poco poblada entre máscara anatómica medida, dinámica continua adaptable, compilación dispersa y validación mecanística.**

Para volverlo defendible:

1. fijar una máscara `M` del conectoma y prohibir aristas fuera de `M`;
2. definir pesos y taus compartidos por tipo celular, región o clase de conexión antes de permitir parámetros individuales;
3. comparar la misma máscara contra LIF, CTRNN, ESN/LSM, GRU/LSTM y modelos conductance-based;
4. empezar por subcircuitos con actividad/perturbación retenida, no por afirmar emulación completa de 138.639 neuronas;
5. medir predicción de actividad no usada en el ajuste, ablación/silenciamiento, conducta y coste por segundo biológico;
6. usar rewiring que preserve grado, pesos y tipos como null estructural;
7. publicar la incertidumbre entre parametrizaciones equivalentes.

El trabajo de Abraham ya aporta piezas que la literatura suele separar: conectoma FlyWire auditado, SparseLTC propio, guards de alineación, loader oficial, ROI-preserving features, nulls y pipeline reproducible. Pero el producto todavía no es una mosca emulada: falta el mapping ROI→anatomía, el null anatómico, el silenciamiento causal y el benchmark SparseLTC→DBC3 sobre señal biológica real.

## Conclusión operativa

El mundo no ignoró la relación conectoma-dinámica. La exploró con herramientas más simples o con circuitos parciales. Lo que casi no está resuelto es la combinación completa: **conectoma medido grande + dinámica líquida adaptable + coste manejable + validación causal**.

Ese hueco es una oportunidad de investigación y producto, no una prueba de superioridad. La próxima demostración fuerte debe ser un subcircuito conectado a FlyWire donde SparseLTC gane o iguale en actividad y perturbación, usando menos grados de libertad y mejor trazabilidad que LIF/CTRNN/LSM.

## Límite de cobertura

Esta exploración fue amplia pero no una revisión bibliométrica exhaustiva de Scopus/Web of Science/Dimensions. Se buscaron términos exactos y vecinos en artículos, preprints, repositorios y herramientas públicas. No se puede afirmar que no exista ningún preprint, tesis o código no indexado; sí se puede afirmar que la intersección estricta no aparece como línea consolidada en las fuentes primarias revisadas.
