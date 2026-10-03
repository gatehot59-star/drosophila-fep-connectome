# Hueco conectoma + dinámica líquida frente a patentes y estándares

**Fecha:** 2026-10-02 ART  
**Alcance:** comparación técnica y de prior art público; no es opinión legal, análisis de infracción ni libertad de operación.

## Veredicto

El hueco sigue siendo real, pero no está vacío:

> **Hay patentes activas que cubren piezas amplias del puente conectoma→arquitectura y conectoma→controlador. Hay estándares que cubren descripción de modelos, datos neurofisiológicos, redes spiking e interoperabilidad neuromórfica. No encontré una fuente que reúna de forma explícita y completa: conectoma celular medido + dinámica LTC/CfC adaptable + compilación dispersa + validación causal reproducible.**

La consecuencia práctica es doble:

1. No conviene reclamar una patente amplia sobre «usar un conectoma para crear una red neuronal».
2. Sí queda espacio para una implementación más estrecha y técnica: máscara anatómica fija, dinámica líquida definida formalmente, solver disperso, contrato de provenance/uncertainty/nulls y exportación verificable a hardware.

## Distinción que evita errores

- **Patente:** puede conferir derechos exclusivos sobre reivindicaciones concretas en jurisdicciones concretas. Que una patente aparezca como activa en Google Patents es solo una señal de estado; Google advierte que no hace análisis legal. Hay que leer reivindicaciones, familia, jurisdicción, mantenimiento y prosecution history.
- **Estándar:** define interoperabilidad, semántica o formato. No otorga exclusividad por sí mismo. Un estándar publicado puede ser relevante como estado de la técnica, pero su función principal aquí es decir qué debe poder intercambiarse y reproducirse.
- **Artículo/preprint:** evidencia de que una técnica fue divulgada, no necesariamente una patente vigente ni una barrera de implementación.

## Matriz de patentes relevantes

| Familia pública | Estado observado | Qué cubre | Solapamiento con SparseLTC | Lo que no cubre explícitamente |
|---|---|---|---|---|
| [US12050991B1, Connectomics-based neural architecture search](https://patents.google.com/patent/US12050991B1/en) | Patente concedida, listada activa; Google LLC; prioridad 2018-05-21 | Usa datos de conectómica para identificar motivos y restringir/buscar arquitecturas ANN | **Alto** para claims amplios de grafo biológico que guía arquitectura, motivos y NAS | No aparece como LTC/CfC, solver ODE disperso, evidencia causal o pipeline FlyWire→hardware específico |
| [US20230196059A1, Attention-based brain emulation neural networks](https://patents.google.com/patent/US20230196059A1/en) | Solicitud publicada, listada pending; X Development LLC; prioridad 2021-12-21 | Mapea un grafo de conectividad sináptica a capas/arquitecturas de brain emulation con atención | **Medio-alto** para «grafo biológico→red artificial» y emulación | No es liquid/LTC, no fija compilación sparse ni validación causal; está pendiente y sus reivindicaciones pueden cambiar |
| [US12070858B2, Neuromorphic smooth control of robotic arms](https://patents.google.com/patent/US12070858B2/en) | Patente concedida, listada activa; Accenture; prioridad 2021-08-02 | Control robótico con SNN que imita conectomas identificados y usa una microarquitectura sensorimotora | **Medio** en el extremo «conectoma/control embebido» | No es LTC, no es compilador de conectoma completo, no es FlyWire ni SparseLTC |
| [US7392230B2, Physical neural network liquid state machine](https://patents.google.com/patent/US7392230B2/en) | Concedida pero listada expirada en 2023 | LSM física con memoria temporal/fading memory en hardware molecular | **Conceptual**, sobre LSM y hardware líquido | Está expirada; no cubre el puente moderno conectoma medido→LTC dispersa |
| [US10210452B2, High level neuromorphic network description](https://patents.google.com/patent/US10210452B2/en) | Patente concedida, listada activa | Descripción de redes neuromórficas, nodos, conexiones, tipos y traducción a instrucciones | **Medio** para la capa de descripción/compilación | No es específica de conectomas ni de LTC; el solapamiento es de infraestructura |
| [US9753959B2, neuroscience-inspired ANN with neural pathway visualization](https://patents.google.com/patent/US9753959B2/en) | Patente concedida, listada activa | Construcción y visualización de arquitecturas dinámicas inspiradas en neurociencia | **Bajo-medio**, principalmente visualización/composición y rutas | No es conectoma FlyWire ni dinámica LTC formal |
| [US20180053090A1, dynamic neural networks](https://patents.google.com/patent/US20180053090A1/en) | Publicación de solicitud; usar el estado de familia, no asumir vigencia | Describe familias dinámicas, ESN/LSM, filtros temporales y aprendizaje de redes dinámicas | **Conceptual** para reservoir/liquid temporal | No conecta una matriz anatómica medida con SparseLTC |

### Lectura patentaria

El riesgo mayor está en la **frase amplia**, no en el detalle SparseLTC:

- «generar arquitecturas ANN a partir de conectómica» ya tiene una patente fuerte y directa en US12050991B1;
- «mapear un grafo sináptico a una red de brain emulation» aparece en la familia de X Development;
- «usar un conectoma/SNN para control robótico» aparece en US12070858B2;
- «describir y traducir redes neuromórficas» tiene precedentes de infraestructura.

La defensa técnica de SparseLTC no debe ser «el conectoma inspira una red». Debe ser una combinación verificable de elementos que la chart no muestra reunidos en una misma reivindicación: máscara de aristas medida y versionada, parámetros compartidos con contrato biológico, dinámica líquida específica, propagación sparse con coste medido, solver/quantización reproducibles, null estructural pareado, predicción de perturbaciones y exportación con equivalencia numérica.

Esto **no** concluye patentabilidad ni libertad de operación. Antes de presentar algo, hay que hacer búsqueda por reivindicaciones en las familias US/WO/EP/CN y revisar un abogado de patentes.

## Matriz de estándares técnicos

| Estándar/ecosistema | Qué resuelve | Qué puede aportar al proyecto | Hueco que deja |
|---|---|---|---|
| [NeuroML v2.3 / LEMS](https://docs.neuroml.org/Userdocs/NeuroMLv2.html) | Descripción declarativa de células, sinapsis, redes y dinámica; NeuroML es estándar respaldado por INCF/COMBINE | Puede describir red, unidades, parámetros y ODEs; LEMS permite definir ComponentTypes nuevos | La dinámica LTC no es una primitive interoperable universal; extensiones custom pueden dejar de ser portables entre herramientas |
| [NineML](https://github.com/INCF/nineml-spec) | Lenguaje independiente del simulador para describir redes neuronales, especialmente spiking | Puede servir como formato de intercambio para modelos spiking y componentes | No define provenance de conectoma, incertidumbre anatómica, nulls ni un contrato LTC completo |
| [PyNN](https://neuralensemble.org/docs/PyNN/) | API procedural independiente del simulador; interoperable con NeuroML, NineML y SONATA | Puede construir/ejecutar modelos comparables en simuladores compatibles | Es API, no un IR completo de conectoma→liquid ni un formato de evidencia |
| [SONATA](https://neuralensemble.org/docs/PyNN/import_export.html) | Almacenamiento de redes spiking data-driven, planes de simulación y outputs | Adecuado para nodos, edges, tipos y redes grandes, incluyendo conectividad explícita | Su centro es spiking/network data; no fija semántica de tau dependiente del estado, solver LTC o causal gates |
| [NWB 2.0](https://nwb.org/faq/comparison_to_other_standards/) | Datos de neurofisiología, comportamiento, optogenética y sesiones | Puede ser destino para actividad, conducta, estímulos y provenance experimental | No es un lenguaje de dinámica ni un compilador de conectomas |
| [BIDS](https://www.incf.org/blog/incf-re-endorses-neuroml-bids-and-pynn) | Organización de datos de neuroimagen, comportamiento y estudios multi-sesión | Puede ordenar sujetos, sesiones, conducta y derivados | No describe una red neuronal ejecutable ni dinámica líquida |
| [NIR](https://neuroir.org/docs/what/) | IR declarativa para grafos neuromórficos, dinámica continua/híbrida y despliegue entre simuladores/hardware | Es el candidato más cercano para la salida de compilación hacia hardware; soporta grafos y primitives continuas | La versión actual se centra en primitives comunes y excluye mecanismos como gating, adaptive threshold y multicompartment; no contiene provenance de conectoma, mapping anatómico, nulls ni causalidad |
| [NIR paper](https://doi.org/10.1038/s41467-024-52259-9) | Demuestra interoperabilidad entre múltiples simuladores/plataformas | Sirve como referencia de cómo hacer un backend verificable | Reporta divergencias en modelos recurrentes y discretización; una SparseLTC necesitaría primitive/extensión propia y pruebas de equivalencia |

### Conclusión de estándares

Los estándares existentes cubren **tres capas separadas**:

1. datos experimentales: BIDS/NWB;
2. modelo y simulación: NeuroML/NineML/PyNN/SONATA;
3. despliegue neuromórfico: NIR.

Lo que falta es una capa transversal que conserve, en un solo artefacto reproducible:

- identidad y versión del conectoma;
- IDs neuronales y aristas, conteo de contactos y signos/uncertainty;
- mapping de observaciones ROI→neurona/tipo/neuropilo;
- ecuaciones de dinámica líquida y unidades;
- solver, paso, tolerancias, discretización y cuantización;
- máscara de entrenamiento y parámetros compartidos;
- nulls estructurales y causal perturbations;
- hashes de resultados y equivalencia entre referencia y target.

## Qué debería hacer SparseLTC ahora

No inventar otro formato aislado. La vía fuerte es una arquitectura por capas:

1. **Entrada:** FlyWire/SONATA o representación equivalente, con manifest de checksums y provenance.
2. **Datos:** NWB/BIDS para actividad, conducta y sesiones; mantener el guard temporal de H4.
3. **Modelo:** NeuroML/LEMS para una especificación legible de dinámica y unidades, o una extensión documentada si la ecuación LTC no cabe en las primitives estándar.
4. **Compilación:** SparseLTC genera una máscara/CSR y una representación target; exportar a NIR cuando la dinámica pueda expresarse sin pérdida, o declarar `custom primitive` y no fingir portabilidad.
5. **Evidencia:** sidecar machine-readable propio, por ejemplo `connectome-liquid-manifest/v1`, con hashes, solver, nulls, perturbaciones y límites.
6. **Control:** DBC3 como readout/controlador separado; no mezclar la evidencia de SparseLTC con la de DBC3.

La oportunidad de estándar no es «otro XML de neuronas». Es un **contrato de compilación y evidencia** entre conectoma, dinámica y hardware.

## Veredicto de oportunidad

- **Patentes:** espacio amplio solo en la combinación técnica estrecha y demostrable; espacio pobre en claims genéricos de conectoma→ANN, conectoma→motivos o conectoma→controlador.
- **Estándares:** no hay una especificación dominante para conectoma medido + LTC + validación causal + despliegue; NIR es el puente de ejecución más útil, pero no resuelve la semántica científica.
- **Proyecto:** SparseLTC puede diferenciarse como compilador/contrato verificable, no como «primera red neuronal inspirada en el cerebro».

## Fuentes clave

- [US12050991B1](https://patents.google.com/patent/US12050991B1/en)
- [US20230196059A1](https://patents.google.com/patent/US20230196059A1/en)
- [US12070858B2](https://patents.google.com/patent/US12070858B2/en)
- [US7392230B2](https://patents.google.com/patent/US7392230B2/en)
- [NeuroML v2.3](https://docs.neuroml.org/Userdocs/NeuroMLv2.html)
- [NineML](https://github.com/INCF/nineml-spec)
- [PyNN](https://neuralensemble.org/docs/PyNN/)
- [SONATA interoperability](https://neuralensemble.org/docs/PyNN/import_export.html)
- [NWB vs BIDS](https://nwb.org/faq/comparison_to_other_standards/)
- [NIR](https://neuroir.org/docs/what/)
- [NIR, Nature Communications](https://doi.org/10.1038/s41467-024-52259-9)
