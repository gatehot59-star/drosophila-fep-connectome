# Peritaje corregido del informe externo · Drosophila + DualBrain

**Fecha:** 2026-09-22
**Sujeto:** el archivo adjunto `vovliendo al la mosca.md`, que mezcla la auditoría del paper de Drosophila con la especificación/benchmark de DualBrain DBC3.

## Veredicto corto

El informe externo encontró deudas reales, pero arranca con un error factual grave y después arrastra varias conclusiones que no corresponden al estado medido del proyecto: **el paper sí es localizable y público**. El DOI `10.5281/zenodo.19136948` resuelve a un registro público de Zenodo, publicado el 20-mar-2026, con autor Jorge Abraham Mendieta y el abstract completo de v1.0.

La auditoría mejorada debe separar tres cosas: **qué estaba mal en el paper publicado**, **qué ya fue corregido en el erratum preparado**, y **qué pertenece a DualBrain/DBC3 y todavía no está reproducido de punta a punta**.

## 1. Correcciones al informe externo

### 1.1 El preprint no está perdido

La frase «no existe DOI, URL ni metadato verificable» es falsa. La búsqueda superficial no encontró el registro, pero la resolución directa sí:

- DOI v1.0: https://doi.org/10.5281/zenodo.19136948
- Registro público: https://zenodo.org/records/19136948
- DOI conceptual para futuras versiones: https://doi.org/10.5281/zenodo.19136947

Esto no significa que la v2 del erratum ya esté depositada. Significa algo más preciso: **v1.0 es pública y auditable; la corrección preparada todavía debe depositarse como nueva versión**.

### 1.2 La densidad 0.0074 no es consistente

El informe externo llama «matemáticamente consistente» a `0.0074`. No lo es con los propios `N` y `E` publicados:

```text
E / (N·(N−1))
= 15,091,983 / (138,639·138,638)
= 0.000785197
```

El `0.00739526` publicado sale de un overflow silencioso de `int32` en `N·(N−1)`. No es un criterio de filtrado desconocido ni una densidad defendible del subgrafo. La hipótesis de que eran solo neuronas del cerebro central fue una especulación temprana y quedó reemplazada por la causa medida: overflow.

### 1.3 15,091,983 no puede llamarse sin más «sinapsis»

El registro público conserva la terminología ambigua de v1.0: el abstract dice *synapses* y §2.1 dice *connections*. La corrección debe declarar que el análisis trabaja con **aristas dirigidas/conexiones agregadas**, no presentar ese número como sinapsis individuales. El total bruto de sinapsis del conectoma es otra cantidad.

El criterio de inclusión y el umbral de sinapsis deben quedar explícitos por versión del análisis. La comparación con Lin a umbral de 5 produce `13.98%` de reciprocidad en esta matriz, cercano al `13.8%` de Lin, pero no convierte retrospectivamente el análisis sin umbral de v1.0 en uno umbralizado.

### 1.4 Cuatro modelos no significa cuatro modelos compatibles

La descripción de «cuatro modelos sin parámetros ajustables» es correcta como inventario de modelos evaluados, pero el paper ya reconoce que `LIF-hard` produce una métrica indefinida en los pasos muestreados. El abstract debe decir **tres modelos compatibles para el resultado temporal**, con el cuarto reportado como métrica-incompatible, no vender «4/4» como si todos sostuvieran el hallazgo.

### 1.5 El 95.2% y el 7/10 no se pueden conservar sin calificación

Son cifras del abstract v1.0. La recomputación posterior corrigió la lectura de la Tabla 5: con densidad correcta aparecen **4 clases enriquecidas, 4 depletadas y 1 dentro de expectativa** entre las 9 filas reportadas; la fila AN no es reproducible. El informe externo conserva «7/10 depletadas» como si siguiera vigente: eso debe retirarse.

### 1.6 El 36× de reciprocidad es un artefacto de normalización

El conteo de reciprocidad `4,014,518` y el `26.60%` no desaparecen, pero el `36×` se obtiene contra la densidad overflowed y no es un headline defendible. El reemplazo correcto es: `26.60%`, primer lugar entre 41 valores frente al null comunitario, `20.59×` sobre la media del null y `0/40` nulls alcanzando el real. Además, la magnitud global no es distintiva entre conectomas y Lin ya descompone reciprocidad por neuropilo.

## 2. Qué queda corregido en el paper publicado

El texto listo para la v2/erratum está en:

- `docs/ERRATUM.md`: https://github.com/gatehot59-star/drosophila-fep-connectome/blob/main/docs/ERRATUM.md
- Párrafo de reciprocidad: https://github.com/gatehot59-star/drosophila-fep-connectome/blob/main/docs/PIVOTE-RECIPROCIDAD.md
- Paper publicado v1.0: https://doi.org/10.5281/zenodo.19136948

La corrección cubre densidad, Tabla 5, reciprocidad, umbral de 5 sinapsis, referencias omitidas, conteos internos, tau, cantidad de modelos, URL de repositorio, DOI placeholder, licencia, SHA de anotaciones, tasa de swaps y el verificador que comparte el overflow.

**No hay que meter DualBrain dentro del erratum del Paper 1.** DualBrain es una línea posterior/relacionada de arquitectura y producto; sus benchmarks sintéticos no son evidencia biológica del conectoma.

## 3. Qué dice realmente DualBrain/DBC3

El repositorio separado es privado pero existe y fue leído en vivo:

- Repo DualBrain: https://github.com/gatehot59-star/dualbrain
- Paper de arquitectura: https://github.com/gatehot59-star/dualbrain/blob/main/docs/01-paper-dualbrain.md
- Benchmarks extendidos: https://github.com/gatehot59-star/dualbrain/blob/main/docs/02-benchmarks-extendidos.md
- Benchmark DBC3-v3: https://github.com/gatehot59-star/dualbrain/blob/main/docs/03-dbc3-v3-benchmark.md
- Reproducción: https://github.com/gatehot59-star/dualbrain/blob/main/REPRODUCCION.md
- Diferencia DualBrain/DBC3: https://github.com/gatehot59-star/dualbrain/blob/main/dbc3-v3/DIFERENCIA-DUALBRAIN-DBC3.md

La afirmación correcta es que **DBC3-v3 es DualBrain escalado**, no una arquitectura biológica nueva: MLP reactivo, célula líquida de memoria, gate vectorial y combinación `[h_r ; g⊙h_m]`.

### Resultados que sí se pueden reportar

- En el benchmark original de arquitectura, el gate vectorial mejora la interacción multiplicativa frente a modelos comparadores.
- En la ablación iso-run del repositorio del conectoma, gate contra no-gate mejora entre `21.85×` y `108.11×` en 4/4 tareas, con misma celda, arquitectura y presupuesto.
- En DBC3-v3 escalado, `DelayedClass` es el resultado fuerte: `99.2% ± 0.6%` frente a `16.7% ± 0.3%` de LSTM, ratio `5.93×`.
- `ThermalPredict`, `Tracking` y `ContextSwitch` son prácticamente empates técnicos.
- `XORMemory` no es una victoria cerrada: `67.0% ± 22.6%` con 3 semillas, y la reproducción CPU da `49.8%` contra `49.9%`, ambos en chance.
- Por lo tanto, «5/5» es descriptivamente cierto en esa tabla, pero no debe venderse como cinco demostraciones fuertes.

### Qué sigue sin reproducir

- Falta `dbc3-v3/c/dbc3_motor.h`; los headers de bloque y swarm no compilan sin él.
- La tabla GPU original tiene 3 semillas; la reproducción pública disponible es parcial, en CPU y `FAST_MODE`.
- Falta cerrar el match bit a bit Python↔C con pesos exportados.
- El swarm usa pesos placeholder y no es evidencia de desempeño útil.

## 4. Corrección técnica al consejo sobre estabilidad

El informe externo propone imponer `ρ(W_mem)<1`, normalizar a `0.95` y usar `static_assert`. Esa recomendación **no se puede aceptar como solución del DualBrain real** sin leer y medir el llamador exacto.

La celda real documentada para DualBrain/DBC3 es:

```text
τ = sigmoid(W_tau·c + b_tau),  b_tau = -2.0
h' = LayerNorm(h·(1−τ) + tanh(W_flow·c)·τ)
```

Eso es una célula líquida con `tau` dinámica y `LayerNorm`, no una recurrencia fija `h' = W_mem h`. Un `static_assert` tampoco verifica un radio espectral obtenido por iteración en runtime: solo puede verificar una constante de compilación. Y la iteración de potencia no constituye por sí sola una garantía general para matrices no normales o autovalores degenerados.

La mitigación correcta, si se decide hacerla, es otra:

1. definir el contrato numérico del motor real: rangos de `tau`, estado, activación y formato float/fixed-point;
2. ejecutar el instrumento sobre el código exacto, no sobre una matriz hipotética;
3. medir `NaN`, `Inf`, saturación, overflow y crecimiento del estado bajo entradas y pesos adversariales;
4. si hace falta una garantía estática, usar una cota conservadora verificable del operador que realmente se ejecuta, no afirmar que `static_assert` prueba estabilidad de Lyapunov;
5. recién después comparar una normalización espectral con un baseline sin ella.

Además, el informe mezcla `ρ_target=0.95` con un `RHO_SAFETY_MARGIN=0.04` sin definir si el escalado final es `0.95` o `0.91`. Eso no es un contrato cerrado.

## 5. Corrección al consejo sobre el ratio 1.8

La función `A_ratio = 1 + k·D_motor^α` no deriva el ratio con los datos disponibles. Un punto (`D_motor=0.952`, `A_ratio=1.8`) deja infinitas parejas `(k, α)`. El supuesto segundo punto gustativo no está medido como `D_PER` y tampoco existe un `A_PER` objetivo independiente.

La forma honesta es:

- llamar `1.8` **configuración de DBC3-v3**, no una ley derivada del conectoma;
- mantenerlo como hiperparámetro de diseño;
- medir un barrido de `h_r/h_m` o del ratio equivalente contra las tareas del motor;
- si después aparece una relación reproducible, documentarla como resultado de ingeniería, no como traducción biológica automática.

El propio benchmark extendido ya muestra sensibilidad fuerte al reparto reactivo/memoria. Eso hace innecesario inventar una función biológica para justificar el `1.8`.

## 6. Qué hay que cambiar en el informe externo

1. Reemplazar la apertura «preprint no localizable» por «v1.0 pública; v2 del erratum todavía no depositada».
2. Retirar la explicación especulativa del subgrafo central.
3. Reemplazar `densidad 0.0074 consistente` por `overflow int32 confirmado`.
4. Separar conexiones agregadas de sinapsis individuales.
5. Retirar `7/10 depletadas`, `36× distintivo` y «4 modelos compatibles».
6. Separar Paper 1, SparseLTC y DualBrain/DBC3 en tres objetos auditables.
7. Mantener como hallazgos válidos de ingeniería: benchmark incompleto, falta `dbc3_motor.h`, falta match Python↔C y debilidad estadística de 3 semillas/XORMemory.
8. Reemplazar `static_assert`/Lyapunov por un plan de medición sobre el motor real.
9. No presentar el ratio `1.8` como derivado del `95.2%` sin un experimento que lo conecte.
10. Añadir los enlaces canónicos y la fecha/SHA de cada fuente.

## Veredicto final

**El intento externo es útil como lista de preguntas, no como auditoría final.** Acertó al pedir reproducibilidad de DBC3, al desconfiar de XORMemory y al exigir transparencia del filtro y de los benchmarks. Falló en el primer requisito de una auditoría: identificar correctamente el objeto público que está auditando.

La versión mejorada queda así: el Paper 1 necesita un erratum público que ya está escrito y corrige errores reales; DualBrain/DBC3 es una arquitectura de compuerta vectorial con evidencia fuerte en interacción y evidencia más limitada a escala; y la estabilidad del motor debe auditarse contra su ecuación real, no contra una cámara `W_mem` inventada.

--- METODO TITAN ---
Accion delicada: NO. Se leyó el adjunto, Zenodo, el repo del conectoma y el repo privado DualBrain; no se publicó ni se modificó ningún release.
Modo aplicado: TITAN FULL
Rubrica: N/A (peritaje comparativo)
N/A declarados: ejecutabilidad del C de DBC3, deployment, seguridad de producto y publicación en Zenodo; no se modificaron archivos fuente ni se ejecutó la GPU.
Review externo: el informe adjunto es la fuente externa auditada; sus afirmaciones fueron contrastadas con DOI, GitHub y los documentos versionados.
Instrumento: búsqueda de workspace, búsqueda web, lectura GitHub en vivo de `drosophila-fep-connectome` y `dualbrain`; evidencia en este archivo.
