# Respuesta punto por punto al auditor externo

**Sujeto auditado:** informe adjunto `vovliendo al la mosca.md`, que mezcla el Paper 1 de Drosophila con DualBrain/DBC3.

**Respuesta corta:** el informe encontró preguntas válidas, pero su premisa principal es incorrecta: el paper publicado sí es público y verificable. También mezcla resultados viejos del abstract con correcciones ya hechas, y trata DualBrain como si fuera evidencia biológica del conectoma. Abajo queda la respuesta precisa.

## 0. Sobre la accesibilidad del preprint

**Auditor:** el preprint Mendieta (2026) no es localizable, no tiene DOI verificable y no puede ser auditado.

**Respuesta:** incorrecto. La v1.0 está publicada en Zenodo y resuelve públicamente:

- DOI v1.0: https://doi.org/10.5281/zenodo.19136948
- Registro: https://zenodo.org/records/19136948
- DOI conceptual para futuras versiones: https://doi.org/10.5281/zenodo.19136947

Lo correcto es: **la v1.0 es pública y auditable; la v2 con el erratum todavía no está depositada**. La búsqueda que no encontró el registro no autoriza a concluir que no existe.

## 1. Dataset FlyWire v783

### 1.1 Neuronas

**Auditor:** `N=138.639` diverge de las `139.255` neuronas proofread oficiales.

**Respuesta:** son denominadores distintos. El paper trabaja con el subgrafo que contiene `138.639` neuronas y `15.091.983` conexiones dirigidas. La cifra de `139.255` corresponde al total proofread del trabajo de datos; no invalida que el análisis use una intersección filtrada. Lo que sí debía declararse mejor es el criterio exacto de inclusión, y eso queda como corrección metodológica.

### 1.2 Conexiones versus sinapsis

**Auditor:** `15.091.983` parece una subfracción de más de 50 millones de sinapsis y no se explica.

**Respuesta:** la objeción de terminología es válida. El abstract de v1.0 dice *synapses* y §2.1 dice *connections* para el mismo número. Debe decir **conexiones/aristas dirigidas agregadas**, no sinapsis individuales. El erratum corrige esa ambigüedad y exige declarar el criterio de inclusión y cualquier umbral.

### 1.3 Densidad `0,0074`

**Auditor:** la densidad publicada es matemáticamente consistente con `N` y `E`.

**Respuesta:** incorrecto. La recomputación directa es:

```text
15.091.983 / (138.639 × 138.638) = 0,000785197
```

El `0,00739526` publicado coincide con `N×(N−1)` calculado en `int32` con overflow silencioso. No es una densidad defendible ni evidencia de un subgrafo central. La causa está establecida en el erratum.

## 2. Modelos sin parámetros ajustables

**Auditor:** evaluar cuatro modelos sin entrenamiento es metodológicamente válido.

**Respuesta:** de acuerdo, con una precisión importante. Se evaluaron cuatro modelos, pero el resultado temporal solo es compatible en **tres**: `SparseLTC`, `Linear` y `LIF-soft`. `LIF-hard` produce métrica indefinida en los pasos muestreados y debe aparecer como modelo evaluado pero incompatible con ese estadístico, no como cuarto soporte del hallazgo.

Esto no demuestra que la topología explique todo: demuestra qué propiedades aparecen bajo esos modelos y nulls concretos. Los resultados dependen del modelo nulo, la normalización y el estimador.

## 3. Propiedad 1: aislamiento intermodal

### 3.1 Cancelación contralateral `1,37`

**Auditor:** el número es plausible, pero no es auditable sin definición operacional ni null.

**Respuesta:** la crítica es válida. `1,37` es una medida descriptiva de la Tabla 2, no un resultado inferencial independiente. No debe presentarse como si tuviera un `Z` o un `p` propios. El documento posterior lo había mezclado con el `Z_CP=+14,8` de la trayectoria temporal; esa mezcla debe corregirse.

### 3.2 `Z_CP=+14,8`

**Auditor:** un valor tan grande necesita más nulls y una definición completa.

**Respuesta:** correcto como exigencia de reporte. El `+14,8` aparece en una celda concreta de la serie temporal y no puede usarse dos veces para inflar dos propiedades distintas. Además, con pocos nulls no corresponde vender precisión decimal de un z-score. La v1.0 debe quedar citada con su limitación, y la v2 debe separar: dato observado, distribución del null, `n`, estadístico y fase temporal.

## 4. Propiedad 2: acceso motor diferencial

### 4.1 `95,2%` y `7/10`

**Auditor:** la dominancia mecanosensorial y las 7/10 clases depletadas son plausibles y robustas.

**Respuesta:** no se pueden conservar sin corrección. La recomputación de la Tabla 5 con la densidad correcta da **4 clases enriquecidas, 4 depletadas y 1 dentro de expectativa**, sobre las 9 filas reportadas. La fila AN (`N=495`) no se reproduce con ningún filtro consistente y queda declarada **no reproducible**.

Por lo tanto se retiran las frases «7/10 depletadas» y «cero clases enriquecidas». La intuición biológica no reemplaza la recomputación.

### 4.2 El `95,2%`

**Respuesta:** ese porcentaje pertenece al abstract v1.0 y requiere calificación. No se lo puede usar como puente automático hacia una constante del motor. Es una cifra de concentración en el análisis del conectoma, no una derivación del ratio arquitectónico `1,8` de DualBrain.

## 5. Propiedad 3: amplificación temporal

### 5.1 `RDI 0,63 → 0,83`

**Auditor:** es el resultado más interesante y técnicamente plausible.

**Respuesta:** puede mantenerse como resultado del pipeline bajo las condiciones declaradas, pero no debe generalizarse más allá de ellas. El README actual separa resultados estructurales y dinámicos, y el temporal RDI requiere reclasificación cuidadosa por null y métrica. No es válido sostenerlo solo porque «suena biológicamente plausible».

### 5.2 Equivalencia SparseLTC/Linear

**Auditor:** la equivalencia en régimen cuasi-lineal es matemáticamente coherente.

**Respuesta:** de acuerdo como descripción local, no como identidad universal. `SparseLTC` conserva dinámica compleja, tau heterogénea y activación acotada; `Linear` es un control. La aproximación puede valer en un régimen de operación, pero debe reportarse como equivalencia experimental/local, no como que ambos motores son el mismo sistema.

## 6. Reciprocidad `36×`

**Auditor:** la reciprocidad 36× podría ser biológicamente plausible.

**Respuesta:** el conteo observado `4.014.518` y `26,60%` se conservan; el `36×` no. Es `0,2660 / 0,00739526`, por lo que hereda el overflow de densidad. No se reemplaza por `339×`: también sería un cociente contra densidad uniforme y no es el headline correcto.

La formulación que queda es: **26,60% de aristas recíprocas; rango 1/41 frente al null comunitario; 20,59× sobre la media; 0/40 nulls alcanzando el real**. Y la magnitud global no es distintiva entre cinco conectomas según Lin.

Además, la versión anterior del erratum afirmaba que Lin solo reportaba una cifra global. Eso también era falso: Lin descompone reciprocidad por neuropilo. Lo corregido es el eje: la Tabla 7 es funcional y dirigida; Lin es anatómico. No se reclama novedad por «descomponer» en abstracto.

## 7. Auditoría de DualBrain/DBC3

### 7.1 Existencia pública

**Auditor:** DBC3 no aparece en fuentes públicas indexadas.

**Respuesta:** el repositorio existe, aunque es privado: https://github.com/gatehot59-star/dualbrain. La auditoría externa puede no tener acceso, pero eso no prueba inexistencia. La documentación versionada contiene el paper de DualBrain, benchmarks y DBC3-v3.

### 7.2 Qué es DBC3-v3

DBC3-v3 es **DualBrain escalado**, no una arquitectura biológica nueva: vía reactiva, célula líquida de memoria, compuerta vectorial y combinación `[h_r ; g⊙h_m]`. Los benchmarks sintéticos de DualBrain son evidencia de ingeniería de arquitectura, no evidencia directa del Paper 1 ni del conectoma.

### 7.3 Benchmark

**Auditor:** los resultados son plausibles, pero faltan dataset, perfilado y reproducción.

**Respuesta:** correcto y debe quedar como deuda.

- `DelayedClass`: resultado fuerte, `99,2% ± 0,6%` contra `16,7% ± 0,3%` de LSTM, ratio `5,93×`.
- `ThermalPredict`, `Tracking` y `ContextSwitch`: diferencias pequeñas, técnicamente cercanas a empate.
- `XORMemory`: `67,0% ± 22,6%` con 3 semillas; reproducción CPU `49,8%` contra `49,9%`. Está en chance y no debe venderse como victoria.
- El «5/5» es descriptivo de la tabla, no cinco demostraciones robustas.
- El script Python está commiteado, pero falta reproducir la corrida completa GPU y cerrar la verificación Python↔C.

### 7.4 Falta `dbc3_motor.h`

**Auditor:** los headers C no compilan porque falta `dbc3_motor.h`.

**Respuesta:** correcto. Es un bloqueo real, no una opinión. También falta el match bit a bit contra pesos exportados y el swarm actual usa pesos placeholder. Hasta cerrar esos tres puntos, el C embebido no puede presentarse como reproducible.

## 8. Radio espectral y estabilidad

**Auditor:** hay que imponer `ρ(W_mem)<1`, normalizar a `0,95` y usar `static_assert`.

**Respuesta:** esa recomendación apunta a una arquitectura hipotética, no al DualBrain real. La célula documentada usa:

```text
τ = sigmoid(W_tau·c + b_tau), b_tau = -2,0
h' = LayerNorm(h·(1−τ) + tanh(W_flow·c)·τ)
```

No es simplemente `h'=W_mem h`. Un `static_assert` puede verificar que una constante de compilación sea menor que 1, pero no prueba el radio espectral de un operador calculado en runtime ni garantiza estabilidad de una matriz no normal. La mitigación correcta es medir el motor exacto: `NaN`, `Inf`, saturación, overflow, crecimiento del estado, rango de tau y formato numérico, incluyendo entradas adversariales. Si luego hace falta una cota, se construye sobre el operador real.

También hay una inconsistencia en la propuesta externa: `RHO_TARGET=0,95` y `RHO_SAFETY_MARGIN=0,04` pueden producir `0,91` según la fórmula, pero el texto habla de normalizar a `0,95`. Eso no es todavía un contrato reproducible.

## 9. Ratio reactivo/memoria `1,8`

**Auditor:** el `1,8` no está formalmente derivado del `95,2%` y debería convertirse en una función de dominancia.

**Respuesta:** la primera parte es correcta; la solución propuesta no. Un solo punto `D_motor=0,952 → A_ratio=1,8` no identifica `k` y `alpha` en `1+k·D_motor^alpha`. Tampoco hay un segundo `D_PER` y un `A_PER` objetivo independiente medidos.

Por ahora `1,8` debe llamarse **configuración de diseño de DBC3-v3**. La forma seria de estudiarlo es barrer `h_r/h_m` y medir tareas, presupuesto y generalización. Si aparece una relación reproducible, se reporta como resultado de ingeniería, no como ley biológica automática.

## 10. Filtrado FlyWire y ecuaciones

**Auditor:** hay que publicar la ecuación exacta del subgrafo y el orden de filtros.

**Respuesta:** de acuerdo. La metodología debe distinguir: dataset de origen, tabla de anotaciones, definición de nodo, definición de arista/conexión, umbral de sinapsis, filtros anatómicos y orden de aplicación. Lo que no corresponde es inventar ahora `θ_syn` o afirmar que el grafo de 15.091.983 proviene de un único umbral si el código no lo demuestra.

## 11. Publicación y citabilidad

**Auditor:** el trabajo debe depositarse en bioRxiv/arXiv para que sea falsable.

**Respuesta:** la falsabilidad mínima ya existe por Zenodo v1.0 público y por el repositorio de análisis. Depositar una v2 corregida es recomendable, pero no se debe afirmar que la v1.0 era inaccesible. La acción pendiente es subir la nueva versión del erratum/paper, no descubrir un DOI inexistente.

## 12. Veredicto final

El informe externo queda clasificado así:

- **Aciertos:** pide reproducibilidad C↔Python; detecta que `XORMemory` no es una victoria; exige declarar filtros, datos y perfil de latencia; identifica que falta `dbc3_motor.h`; separa estabilidad teórica de evidencia empírica.
- **Errores:** declara inexistente un DOI público; acepta como correcta una densidad que no cierra; conserva cifras viejas de la Tabla 5; trata `36×` como posible headline; convierte un ratio de diseño en ley biológica; aplica `ρ(W_mem)<1` a una célula que no fue descrita así.
- **Estado final:** Paper 1 necesita una v2/erratum público con correcciones reales. DualBrain/DBC3 tiene evidencia fuerte para interacción multiplicativa y retención con delay, pero reproducción incompleta a nivel C y resultados débiles en XORMemory. La estabilidad del motor sigue siendo una pregunta de ingeniería que debe medirse sobre el código real.

## Fuentes

- Paper v1.0: https://doi.org/10.5281/zenodo.19136948
- Erratum preparado: https://github.com/gatehot59-star/drosophila-fep-connectome/blob/main/docs/ERRATUM.md
- Pivote de reciprocidad: https://github.com/gatehot59-star/drosophila-fep-connectome/blob/main/docs/PIVOTE-RECIPROCIDAD.md
- Repo conectoma: https://github.com/gatehot59-star/drosophila-fep-connectome
- Repo DualBrain: https://github.com/gatehot59-star/dualbrain
- Paper DualBrain: https://github.com/gatehot59-star/dualbrain/blob/main/docs/01-paper-dualbrain.md
- Benchmarks: https://github.com/gatehot59-star/dualbrain/blob/main/docs/02-benchmarks-extendidos.md
- DBC3-v3: https://github.com/gatehot59-star/dualbrain/blob/main/docs/03-dbc3-v3-benchmark.md
- Reproducción: https://github.com/gatehot59-star/dualbrain/blob/main/REPRODUCCION.md

--- METODO TITAN ---
Accion delicada: NO. Se redactó y versionó una respuesta; no se publicó ni se envió al auditor.
Modo aplicado: TITAN FULL
Rubrica: N/A (documento de respuesta/peritaje)
N/A declarados: ejecutabilidad, deployment y seguridad de producto; no se modificó código ni se ejecutó benchmark nuevo.
Review externo: el auditor externo es el objeto contrastado; no se interpreta su silencio como aprobación.
Instrumento: lectura del adjunto, búsqueda de workspace/web y lectura GitHub en vivo de los repos de conectoma y DualBrain; evidencia en este archivo.
