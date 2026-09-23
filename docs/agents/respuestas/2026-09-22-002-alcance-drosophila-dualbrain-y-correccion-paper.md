# Alcance del proyecto y corrección del paper · 2026-09-22

Sí, el proyecto del pedido es la línea combinada de:

1. **Conectoma de Drosophila / Paper 1:** auditoría del paper publicado, sus números, nulls, reciprocidad, acceso motor y erratum.
2. **DualBrain / SparseLTC:** motor derivado del conectoma y línea de producto embebido. Es un proyecto relacionado, pero no debe presentarse como si sus benchmarks sintéticos fueran hallazgos biológicos del Paper 1.

## Qué se agrega al paper publicado

La corrección debe ir como **erratum/v2**, no como un párrafo de DualBrain dentro del paper:

- densidad: `0.0074` → `0.000785197`, causada por overflow silencioso de `int32` en `N*(N-1)`;
- Tabla 5: de `0 enriquecidas / 7 depletadas` a `4 enriquecidas / 4 depletadas / 1 dentro de expectativa`; la fila AN queda no reproducible;
- retirar el `36×` de reciprocidad como headline y reemplazarlo por `26.60%`, rank `1/41`, `20.59×` contra el null comunitario, `0/40` nulls alcanzando el real;
- retirar la afirmación de que Lin et al. solo daban una cifra global: Lin ya descompone reciprocidad por neuropilo;
- declarar que el null comunitario no es novedad metodológica absoluta y citar el NPC model de Lin;
- bajo el umbral estándar de 5 sinapsis, reportar `13.98%`, consistente con el `13.8%` de Lin;
- retirar el `1,559×`, corregir los conteos, los tres modelos compatibles, la derivación de tau, la URL de GitHub, DOI, licencia, SHA de anotaciones y tasa de swaps;
- agregar las referencias de Lin, Dorkenwald y Bates.

**El resultado de dos saltos con null anatómico no va al erratum:** es material nuevo para la v2 del paper. El PR #2 muestra que el resultado previo se invierte al controlar neuropilo, así que no hay que publicar la vieja jerarquía de `323×` como conclusión biológica.

## DualBrain, separado

Lo que sí está medido en el motor es arquitectura, no biología: la ablación gate/no-gate mejora `21.85×` a `108.11×` en 4/4 tareas; DualBrain pierde contra GRU/LSTM/MinGRU en la configuración de dos referencias; el C99 mide `1,336 B` de `.text` en ESP32 a `-Os`; y la hipótesis del `96% fijo` sigue **NO MEDIDA** sobre SparseLTC.

## Enlaces canónicos

- Repo: https://github.com/gatehot59-star/drosophila-fep-connectome
- Erratum exacto: https://github.com/gatehot59-star/drosophila-fep-connectome/blob/main/docs/ERRATUM.md
- Contexto vivo del motor: https://github.com/gatehot59-star/drosophila-fep-connectome/blob/main/docs/agents/CONTEXTO-motor.md
- Párrafo de reciprocidad listo para pegar: https://github.com/gatehot59-star/drosophila-fep-connectome/blob/main/docs/PIVOTE-RECIPROCIDAD.md
- PR del null anatómico y la corrección del resultado a dos saltos: https://github.com/gatehot59-star/drosophila-fep-connectome/pull/2
- PR de auditoría de reproducibilidad: https://github.com/gatehot59-star/drosophila-fep-connectome/pull/3
- DOI conceptual que resuelve a la última versión: https://doi.org/10.5281/zenodo.19136947
- DOI de v1.0 publicada: https://doi.org/10.5281/zenodo.19136948
