# Programa de materialización del proyecto

**Fecha:** 2026-10-02 15:xx ART  
**Base auditada:** `main` `78d0e644e07eb98088d8a843fa2efbc55a783ce3`; H4 `6112bdd25daf29d68e83d96eecd5f802d0fe8920`.

## Veredicto

El proyecto no necesita más entusiasmo ni otra variante de modelo: necesita convertirse en un sistema de evidencia que produzca un producto cedible. La arquitectura correcta tiene cuatro capas y cuatro gates.

## Las cuatro capas

1. **Atlas medido:** grafo, annotations, pesos, signos, tau, hashes y definiciones poblacionales.
2. **Compilador de dinámica:** SparseLTC que transforma el atlas en propagación reproducible, con nulls y guards.
3. **Biblioteca de motivos:** circuitos con función medida, límites explícitos y criterio de aborto.
4. **Controlador embebido:** DualBrain/DBC3 que consume features temporales; no se presenta como cerebro completo ni como sustituto de planificación.

## Los cuatro gates

- **Provenance gate:** input exacto, SHA, checksum, definición de población y no mezcla entre snapshots.
- **Alignment gate:** animal, trial, timebase, monotonicidad, cobertura y pérdidas; queda prohibido unir H4 por `Frame` sin una prueba de reloj.
- **Null gate:** el null debe poder dar rojo, no conservar la cantidad medida; modularidad, neuropilo, distancia, grado y signo se declaran por separado.
- **Causal gate:** decodificación no equivale a rutas; hace falta mapping anatómico y silenciamiento cruzado.

## Decisiones de arquitectura

- H4 fuerte queda **NO MEDIDA** hasta pasar alignment + null + causal gates.
- La H4 débil queda **REFUTADA solo en su operacionalización estrecha**.
- ComplexVectorLTC y CanonicalComplexLTCBatch quedan experimentales; no entran al producto ni reclaman superioridad IQ/radar sin una tarea donde la fase sea necesaria.
- El claim más limpio de DualBrain hoy es la ablación iso-run del gate: `21,85x–108,11x` en 4/4 tareas. El resultado MultiCue debe llevar siempre su configuración: en el bench fijo pierde frente a GRU/LSTM/MinGRU.
- La biblioteca vale más que el motor: cada motivo debe traer entrada, salida, null, límites, costo y criterio de aborto.

## Primer bloque materializado en esta fase

Rama `titan/materializacion-h4-guard-2026-10-02`:

- `tools/h4_alignment_guard.py`: guard fail-closed de identidad y reloj.
- `tests/test_h4_alignment_guard.py`: positivos y negativos, incluida la mutación conceptual que antes pasó por `Frame`.

El guard rechaza explícitamente `Frame`, exige `animal/trial/timebase`, verifica ejes finitos y monótonos, duración, cobertura y saltos. Esto no demuestra H4: evita volver a medirla con un instrumento roto.

## Ruta de materialización

1. Cerrar alignment gate y ejecutar loader oficial `roi_dFF.pkl`.
2. Rehacer features conservando ROI/cell type/neuropilo, no nueve estadísticas globales como instrumento principal.
3. Construir null anatómico pareado con grado, neuropilo, distancia y signo.
4. Repetir H4 por bouts/trials y contexto compartido; separar decodificación, estabilidad y causalidad.
5. Integrar SparseLTC sobre subgrafos observados y correr silenciamientos cruzados.
6. Promover solo los motivos que sobrevivan al null y tengan función útil en una tarea real.
7. Rehacer DBC3 con seeds y outputs persistidos; medir primero el controlador, después la integración biológica.
8. Dejar el motor complejo fuera del producto hasta que una tarea de fase obligatoria lo justifique.

## Qué se produce

Cada entrega deja: código versionado, evidencia cruda, recibo, estado vivo y Doc público. Los binarios/datasets grandes se referencian por checksum. El producto final no es “una mosca simulada”: es un compilador de priors estructurales a control eficiente, con una biblioteca de motivos verificables.

## Riesgos que no se maquillan

- H4 fuerte todavía no existe como resultado.
- Seis fuentes Kaggle no están en Git.
- Tabla 7 original no tiene script reproducible.
- Tabla 5 completa y p-valores requieren cierre.
- SparseLTC→DBC3 end-to-end sobre datos biológicos no está medido.
- Brain-env persistente sirve para iterar, pero Actions debe ser el testigo limpio de los gates cuando haya workflow.
