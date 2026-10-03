# Resumen técnico del estado real

**Fecha:** 2026-10-03 ART  
**Repositorio H4:** `gatehot59-star/drosophila-fep-connectome`  
**`main` auditado:** `4d8b0fc6eab4bbe2f8d68c2482d680f4db915cc4`  
**Estado científico:** H4 fuerte **NO MEDIDA**.

## 1. Veredicto en una línea

Tenés un taller propio que ya conecta **atlas biológico medido → pipeline de evidencia → dinámica sparse líquida → biblioteca de motivos → controlador DBC3/DualBrain**. Lo que todavía no tenés es una mosca digital completa, una identidad anatómica verificada para `ROI_0`/`ROI_1`, una prueba causal de H4 ni un puente SparseLTC→DBC3 validado sobre señal biológica real.

La parte fuerte hoy no es una demo de “cerebro artificial”: es un sistema auditable para **compilar estructura biológica medida a control pequeño, rápido, explicable y potencialmente embebible**.

## 2. Qué es propio y qué es precedente

### Trabajo propio de Abraham

- SparseLTC y su formulación de propagación sparse sobre estructura biológica.
- DualBrain y DBC3.
- El paper, sus correcciones, erratum, nulls y auditorías.
- Los guards de alineación, loader oficial, features ROI-preserving, null por bouts, generalización intra-animal y estabilidad temporal.
- La arquitectura de cuatro capas: Atlas, compilador, biblioteca de motivos y controlador.
- Los hallazgos de estructura, límites y decisiones de producto.

### Precedentes externos usados para comparar

FlyVis/Lappalainen, Shiu, Costi, Neurokernel, conn2res, NCP, ESN/LSM, modelos LIF, Wilson-Cowan, conductance-based, SONATA, NWB, BIDS, NeuroML, NineML, PyNN y trabajos de conectoma a dinámica.

La exploración global no encontró una línea consolidada que reúna de forma estricta **conectoma completo medido + dinámica LTC/CfC/LSM explícita + propagación sparse compilada + validación causal**. Eso es un hueco comparativo, no una patente automática ni una prueba de prioridad mundial.

## 3. Atlas y base estructural

El corpus estructural auditado contiene aproximadamente:

- **138.639 neuronas**.
- **15.091.983 aristas dirigidas únicas**.
- **54.492.922 contactos sinápticos** en el recuento de contactos del análisis.
- Ley de Dale: **0 neuronas mixtas** entre 138.005 evaluadas; 96.672 excitatorias puras y 41.333 inhibitorias puras.
- Circuito plástico auditado: 5.608 neuronas.
- Densidad corregida aproximada: `0.000785197`.

El atlas FlyWire v783 fue importado en el pipeline de `mojo-absoluto` con inputs pinned:

- conectividad MD5: `3d802fd542b5d18570ba1ba0bb0abed9`;
- annotations MD5: `719904abad876c68ace1b5690c9b9b63`;
- loader real: 138.639 neuronas, 15.091.983 aristas, 138.625 neuronas con annotation y 14 sin annotation;
- materialización normalizada: `connectome_nodes.tsv` y `connectome_edges.tsv`, con checksums de salida `0f90a72dcb1e2c4864a618fd7d733084` y `04125d7b83317428060156c1570a8c6b`.

Esto demuestra que el **atlas global** está cargable y verificable. No demuestra que una ROI de calcio concreta corresponda a una neurona FlyWire concreta.

## 4. Runtime de conectoma que ya existe

En `mojo-absoluto` existe una primera capa ejecutable:

- una estructura de parámetros por neurona;
- un grafo sparse de sinapsis;
- CSR por entradas de cada neurona objetivo;
- un estado complejo escalar por célula en la primera capa;
- un peso complejo por arista agregada;
- solver Euler explícito;
- loader C++ con checksums de manifest, conteos, IDs y annotations;
- tests de loader, topología, checksums y seguridad de índices.

La arquitectura declarada es **una célula por neurona y una arista por sinapsis agregada**, no una matriz densa. Todavía no modela toda la biología: delays, compartimentos, dinámica de neurotransmisor, plasticidad detallada, sinapsis múltiples no agregadas ni parámetros específicos validados por tipo celular.

## 5. Cadena H4 corregida

El pipeline viejo fue retirado como evidencia biológica porque unía conducta y DFF por el entero `Frame`, aunque los relojes y tamaños no correspondían. Ese error invalidó los resultados antiguos cross-animal y temporales.

La cadena nueva quedó integrada en `main` y tiene **41 contratos**:

| Capa | Tests | Estado |
|---|---:|---|
| Alignment guard | 7 | confirmado |
| Loader oficial | 6 | confirmado |
| Features alineadas | 7 | confirmado |
| Null por bouts | 5 | confirmado |
| Generalización entre trials | 4 | confirmado |
| Estabilidad temporal | 5 | confirmado |
| Gate ROI→FlyWire | 7 | confirmado |
| **Total** | **41** | **check post-merge verde** |

El job post-merge `integrated-contracts` sobre `main` terminó `completed / success` en el SHA `4d8b0fc`.

## 6. Alignment y loader real

El loader oficial trabaja con reloj ThorSync explícito, no con `Frame`:

- animal: `R65D11-tdTomGC6fopt-fly1`;
- timebase: `thor_sync_seconds`;
- join: `Time`;
- 8/8 trials con manifest `BIEN`;
- 7.440 frames de cámara, 1.067 frames neurales y 7.440 labels por trial;
- 2 ROI por trial;
- error relativo de duración aproximado: `0.0029859–0.0030378`;
- cobertura neural aproximada: `0.9969621–0.9970141`;
- etiquetas sin pareja: 0/8;
- ROI con longitud incorrecta: 0/8;
- pérdidas de borde explícitas, sin extrapolar silenciosamente.

El materializador conserva `ROI_0` y `ROI_1`, contexto `co2_on/co2_off`, `bout_id`, posición y longitud. En trials 1 y 2 se descartó explícitamente un frame conductual fuera de cobertura; no se inventó.

## 7. Resultados H4 válidos, y sus límites

Los ocho trials pertenecen al **mismo animal**. Por eso ningún resultado de esta fase es cross-animal.

### Null ROI-label por bouts

- observado: `0.35831155721189717`;
- null mean: `0.06104563938527175`;
- null SD: `0.017371858516985278`;
- `p=0.001`;
- `z=17.11192372053771`;
- 999 permutaciones, seed `20261002`;
- distribución f64 exacta publicada con SHA `74eb80de8891a01660284e26fba0b4c4e3138d632359d0d34c836faf12a8f01f`.

Interpretación: existe separación descriptiva ROI-label dentro de un animal y sobre este null bloqueado. No identifica rutas anatómicas ni causalidad.

### Generalización leave-one-trial-out

- balanced accuracy: `0.5018855395873556`;
- null mean: `0.5081554609448383`;
- `p=0.623`;
- `z=-0.2997617877213725`.

Veredicto: **NO EVIDENCIA DE GENERALIZACIÓN ENTRE TRIALS dentro de este animal**. No es refutación de H4 fuerte.

### Estabilidad temporal por mitades

- transferencia bidireccional observada: `0.5327595514498719`;
- null mean: `0.5018239610724393`;
- `p=0.055`;
- `z=1.588344413918904`;
- 999 permutaciones, seed `20261002`;
- resultado byte-reproducible, SHA crudo `c2c0e2f2093bc85650daa6bb487b8dcd4bf1ae38278d64de24fd040abb202d98`.

Veredicto: **sugestivo, pero NO EVIDENCIA ROBUSTA** al umbral one-sided 0.05. No refuta ni confirma H4 fuerte.

## 8. El gate anatómico nuevo

El problema actual más importante quedó explicitado: Aymanns `DFF_dic.p` contiene solo claves `ROI_0` y `ROI_1` con series numéricas; el H5 contiene señales ThorSync, no root IDs ni máscaras espaciales.

El gate `tools/h4_roi_anatomy_manifest.py`:

- exige una fila por ROI;
- exige root ID positivo para cada ROI marcada `MAPPED`;
- exige root ID presente en la snapshot de annotations;
- exige evidencia `direct_root_id` o `manual_roi_to_cell`;
- exige confianza finita `[0,1]` y notas de procedencia;
- permite `UNMAPPED`, pero lo marca `PARTIAL` o `NO_MAPPED_ROIS`;
- rechaza mapping por índice, orden, correlación de señal, super_class o neuropilo;
- suma 7 contratos al tren H4.

El gate está verde. El mapping experimental real de `ROI_0`/`ROI_1` sigue **NO MEDIDO**. Bien: el sistema ahora no permite convertir una suposición en anatomía.

## 9. Motores propios y producto

### SparseLTC

Es el compilador/dinámica sparse propio. Su papel es recorrer subgrafos observados y transformar estructura en propagación líquida reproducible, no simular una mosca completa por obligación.

### DualBrain / DBC3

Es el controlador/readout embebible separado de la evidencia biológica. Mediciones existentes:

- ablación iso-run del gate mejora 4/4 tareas, aproximadamente entre `21.85x` y `108.11x`;
- `.text` ESP32 medido: 1.336 bytes con `-Os`, 1.796 con `-O2`;
- 704 bytes de RAM medidos en x86, no todavía en hardware equivalente;
- comparación contra GRU/LSTM/MinGRU realizada, con configuración siempre explícita;
- no se presenta como cerebro completo ni como 138.639 células duplicadas.

### ComplexVectorLTC / Mojo Absoluto

Existe un runtime complejo/vectorial experimental con autodiff Wirtinger, gradchecks y referencia canónica. La decisión vigente es no meterlo en producto ni reclamar superioridad IQ/radar hasta demostrar una tarea donde fase o acoplamiento complejo sean necesarios.

### Producto correcto

No es “una mosca digital”. Es:

> un compilador de estructura biológica medida a dinámica sparse y control eficiente, con provenance, nulls, perturbaciones y equivalencia de backend; encima, una biblioteca de motivos funcionales que sobreviven a sus falsadores.

## 10. Lo que no tenemos todavía

- H4 fuerte confirmada.
- Mapping real `ROI_0/ROI_1 → root_id/cell_type/neuropilo`.
- Null anatómico pareado que preserve grado, neuropilo, distancia, signo y población.
- Silenciamiento cruzado de rutas reales.
- SparseLTC ejecutado sobre un subgrafo biológico observado con función medida.
- Puente SparseLTC→DBC3 sobre señal biológica real.
- Equivalencia entre backend de referencia y hardware final.
- Una demostración de producto end-to-end que vaya de atlas real a controlador y mida coste, actividad retenida, perturbación y memoria.
- Cierre reproducible de las seis fuentes Kaggle, Tabla 7 y Tabla 5/p-valores donde siguen fuera de Git.

## 11. Siguiente orden correcto

1. Conseguir la identidad experimental de las dos ROI desde la segmentación/calcium pipeline; si no existe, declarar ambas `UNMAPPED`.
2. Ejecutar el mapping manifest y preservar su provenance.
3. Construir el null anatómico pareado, sin mezclarlo con el null temporal ni con el null de bouts.
4. Repetir la pregunta H4 solo después de ese control anatómico.
5. Ejecutar SparseLTC sobre el subgrafo real y comparar contra LIF, CTRNN, ESN/LSM y baselines de control.
6. Medir perturbación, coste por segundo biológico, aristas visitadas, memoria y equivalencia de backend.
7. Mantener DBC3 como controlador separado y medir el puente con señal real.
8. Promover solo motivos con función, null, límites y criterio de aborto.

## 12. Fuentes principales

- `docs/agents/CONTEXTO-drosophila-fep.md` en `main`.
- `docs/agents/respuestas/2026-10-02-011-h4-exact-distribution-published.md`.
- `docs/agents/respuestas/2026-10-02-012-h4-trial-generalization.md`.
- `docs/agents/respuestas/2026-10-02-013-h4-temporal-halves.md`.
- `docs/adr/2026-10-03-h4-roi-anatomy-gate.md`.
- [PR #24](https://github.com/gatehot59-star/drosophila-fep-connectome/pull/24).
- [Check post-merge de 41 contratos](https://github.com/gatehot59-star/drosophila-fep-connectome/actions/runs/37123985170/job/111205490912).
- [Auditoría de main final](https://app.clickup.com/90171457413/docs/2kza6fw5-18477).

--- METODO TITAN ---
Accion delicada: NO
Modo aplicado: TITAN FULL
Rubrica: 36/40 -> 90/100
N/A declarados: seguridad, deployment y producto no aplican a un resumen técnico científico
Review externo: no pedido; deuda K-02 declarada
Instrumento: GitHub API, workflow post-merge, contratos, recibos H4, pipeline `mojo-absoluto` y brain-env
Evidencia cruda: SHAs, checksums, métricas y links citados arriba
NO MEDIDO: mapping experimental, null anatómico, causalidad, SparseLTC→DBC3 real y equivalencia hardware
