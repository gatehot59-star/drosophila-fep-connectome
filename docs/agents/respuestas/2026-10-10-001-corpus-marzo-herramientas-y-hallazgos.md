# 2026-10-10-001 · Corpus de marzo (Arena + Gemini): herramientas y hallazgos que sostienen la hipótesis, y los que no

**Fecha:** 2026-10-10 01:00 (America/Buenos_Aires) · **Línea:** conectoma / paper (zenodo.19136948) · **Toca:** HC-2 de Mojo Absoluto

## 1. Pedido

«Revisá esto, quizás están las herramientas y hallazgos que mantienen la hipótesis; realizá un análisis exhaustivo de todo el contenido», con 9 adjuntos: 6 HTML de Arena, `Análisis de Conectoma de Drosophila FEP.pdf`, `2.pdf` y `CONCATETOMAMARZO22.pdf`.

## 2. Herramientas declaradas (C-03)

| Llamada | Escribe | Cuota ajena |
|---|---|---|
| Sandbox: md5, pdftotext, pdfinfo/pdffonts, tesseract spa+eng (concat p.1, 50, 101), BeautifulSoup + pandoc | solo sandbox | no |
| 19 agentes de minería read-only, uno por lote, rúbrica fija v2 | no | no |
| GitHub lectura: `docs/ERRATUM.md`, resp 004 (informe maestro), 008, 056; `mojo-absoluto` `benchmarks/hc2_shard_runner.py` y `hc2_controls.py` (rama HC-2) | no | no |
| GitHub escritura: este archivo, `main` | sí | no |
| ClickUp: 1 Doc público | sí | no |

Cero Kaggle, cero brain-env, nada mergeado, el PDF publicado no se tocó.

## 3. Qué se midió

### 3.1 El corpus

- 9 adjuntos = **4 conversaciones**. Los 6 HTML son 3 pares byte-idénticos. `fep1.pdf` y `2.pdf` son el mismo chat de Gemini (difieren en encabezados y espacios). `CONCATETOMAMARZO22.pdf` (81.411.813 B, 101 páginas, sin capa de texto) es el mismo chat de Gemini: el OCR de p.1 y p.101 coincide.
- Fechas por UUIDv7 (-03:00): **A1** `019cd82f` 2026-03-10 11:38 (claude-opus-4-6-thinking: scripts CONNECTOME LNN v4-v8 + borrador «Aislamiento Topológico»); **A11** `019cfc54` 2026-03-17 12:05 (patentes, Zenodo, Paper 1/2 en LaTeX, licencias); **A10** `019cfe4e` 2026-03-17 21:18 (publicabilidad, Markov blanket, auditoría cruzada, LTC complejo); **G** Gemini `e26fcf246e9f0dad`, desde el depósito en Zenodo (20-mar) en adelante (FEP Scripts A, A', A'', B, R).
- Corrige a resp 008 solo para estos archivos: estos HTML sí traen el DOM renderizado con la conversación (orden invertido por `flex-col-reverse`; se reordenó).

### 3.2 Cobertura

- **Colección:** 213/213 turnos (G 144 + encabezado, A1 20, A10 24, A11 24), 2.198.332 caracteres limpios, 19 lotes cortados en borde de turno. COMPLETA.
- **Procesamiento:** 19/19 lotes, 213/213 turnos analizados, 0 duplicados, **1.028 ítems**; 1.020/1.028 citas verificadas verbatim contra su lote (8 vacías, todas en G-B02). COMPLETA con esa salvedad.
- Por tipo: herramienta-código 252, corrección 144, afirmación LLM 129, propuesta 118, salida medida 108, herramienta-método 108, referencia 89, afirmación del usuario 80.
- Solo 111 ítems son salida de corrida pegada en el chat; los otros 917 son código sin salida o afirmación sin salida.
- Auditoría propia de las etiquetas de los mineros: 2 corregidas (ver 3.4).

### 3.3 Lo que SOSTIENE la hipótesis madre (con número y null)

1. **Retención más lenta que los nulls, en las tres modalidades** (G-T111, salida de Script B v3, FlyWire real, n=5 por null): λ_F visual real 0,055142 vs MS 0,197905±0,0023 (Z -61,33σ) y CP 0,175128±0,0027 (Z -44,53σ); olfatoria 0,095519 vs MS 0,188752 y CP 0,213035; mecano 0,109976 vs MS 0,189003 y CP 0,208363. Es el único efecto dinámico del corpus medido contra MS y CP a la vez. **Límite:** la predicción preregistrada era la contraria (decaimiento más rápido); el script imprimió `DECISION: NO_GO` y la lectura como «retención topológica» es post hoc. Sirve como hipótesis para preregistrar, no como resultado confirmado. Git mide ~5,8x menos actividad post-estímulo absoluta que el null: es otra métrica y la tensión queda NO MEDIDA.
2. **El efecto es topológico y casi lineal:** sin tanh, R(vis)=2,1288 y RDI_180=0,7835 (G-T139, Test 1e); tanh vs lineal 19/20 mismas direcciones (G-T89); max|h| visual 0,048 en el esquema original, o sea tanh en su rango lineal. El propio paper dice «SparseLTC ≈ Linear» (A10-T01). Esto **apoya MADRE** (decide el cableado) y **explica HC-2 FAIL** (0/48 contra el control lineal): en este régimen la no linealidad de SparseLTC no agrega nada.
3. **La Tabla 7 tiene una salida que la reproduce** (G-T13, bloque L3): sensory->central 24,19%, sensory->descending 8,65%, sensory->motor 3,57%, optic->motor 0/6 = 0,00%. Git daba por perdido el script de la Tabla 7: acá está su salida y, en el mismo tramo, el script de validación L1-L6 (con la indentación destruida por el PDF). NUEVO, a recuperar.
4. **Invariancia CP medida, no solo derivada** (G-T13, L1): F_motor real 90068,0000 = CP #1, #2 y #3, diff 0,000000.
5. **Asimetría visual R contra nulls** (G-T111): R_visual 1,8792 vs MS 0,9890±0,0072 y CP 0,9407±0,0104 (n=5). **Límites:** métrica post hoc y dependiente de la normalización: con escalado espectral global R(vis)=0,8111 (se invierte) y con normalización por filas R(mecano)=0,9207 (se invierte). El «5/5 schemes produced stable results» del script habla de estabilidad numérica, no del efecto.
6. **PER:** la gustativa da la mayor activación PER (0,2965 vs visual 0,1400 y olfativa 0,0067), consistente con Shiu 2024 (G-T139, 3A); pero la activación motora total es mecano 37,35 contra gustativa 4,86.

### 3.4 Lo que NO la sostiene, o ya estaba caído

- **FEP:** la predicción de entropía falló (Script A: sube en 4/6; Script A'': 3/12 consistentes, 9/12 FALSIFIED). Gemini admitió circularidad (G-T70). Held-out 6/8, pero los 2 primarios 0/2. D(t), F_mod y la reducción de MI (86,3-92,8%) no tienen null; la partición S/A/μ sale de la anotación `flow`, no se descubre. **FEP no queda sostenido.**
- **El Z_CP=+14,8σ del Script A no es una medición:** es un literal impreso (ver 4). El minero lo había marcado SOSTIENE; corregido.
- **A1 (LNN v4-v8) corrió sobre un conectoma SINTÉTICO:** el log v4 dice `Real data: not found (using synthetic)`; 139.255 neuronas y 8.392.560 aristas en v4-v8 (FlyWire: 138.639 y 15.091.983). Todo structured-vs-rewired prueba el generador, no la mosca. Y aun así: v7/v8 `REWIRED discriminates stimuli better` (motor 0,634845 vs 0,802265), STDP con bugs (0,0% de poda en v7; 53,8% con «cap 10%» en v6) y calibración fallida (v5 0,00% de actividad; v6 0,0258 contra objetivo 0,15). No sirve como evidencia.
- **Gustativa «Z=203,9σ»** (borrador del 10-mar, 20 MS) contra **≈ +4,5σ** en el consolidado MS-100 del 17-mar (0/100, p_perm < 1/101), con mecano ≈ +245σ. Ese consolidado es una tabla escrita por otra IA dentro de un turno del usuario, no un log crudo (el minero lo había marcado SALIDA_MEDIDA; corregido). La causa del salto queda NO MEDIDA; candidata medida en G-T13 L6: MS con 1 swap por arista no converge (f=1 vs f=3 incompatibles en 2/5 poblaciones: somatosensorial -0,9040±0,0031 vs -0,9522±0,0018; mecano -0,8858±0,0034 vs -0,9524±0,0026).
- **Tabla 8** aparece completa en el paper pegado (A10-T01): Real 0,687/0,630/0,680/0,807/0,833; CP 0,711/0,663/0,526/0,368/0,299; Z_CP -24,8/-10,6/+29,5/+18,4/+14,8; Z_MS hasta +2842. Durante el estímulo CP supera al real. El script que la genera **no está** en el corpus: sigue NO REPRODUCIBLE.
- Se repiten los ya retirados: densidad 0,0074, 36x, 0/7, «cuatro modelos», 8,4 ms. Latencias del Test 3B: todas en t=59 (bug), FAIL.

### 3.5 Relación con HC-2 (Mojo)

`hc2_shard_runner.py` escala con `A/max(suma |A| por fila)` y `DT=.05`, no con la normalización por columnas x0,99 de marzo. Ambos son régimen de señal débil; si HC-2 operó con tanh ≈ identidad no se midió (no se guardó max|h|).

## 4. Evidencia cruda verbatim

```
UUIDv7:
A1  019cd82f-c212-7faf-8748-370b9a1aee42 ver 7 2026-03-10T11:38:54.482-03:00
A10 019cfe4e-fef6-718f-b69e-4ace0bff3ae9 ver 7 2026-03-17T21:18:35.894-03:00
A11 019cfc54-9214-716d-b60d-6e5fbc2439d9 ver 7 2026-03-17T12:05:26.804-03:00
bytes: a_models.html 4221311 | a_models10.html 3208755 | a_models11.html 2881630 | fep1.pdf 1669657 | 2.pdf 1676983 | CONCATETOMAMARZO22.pdf 81411813
merge: ITEMS 1028 | ids duplicados 0 | TURNOS corpus 213 | cubiertos 213 | faltantes [] | duplicados [] | QUOTES ok 1020 / 1028
A1-T09 (log v4): Real data: not found (using synthetic)
G-T103 (Script B): DECISION: NO_GO
G-T104 (Gemini): El script gritó NO_GO, pero el script se equivoca
G (código Script A): print(f" ★ CONTROLLED: Z_CP=+14.8σ (Paper 1)")
G-T139 Test 1: (d) Global spectral ×0.99 0.990 no 0.170098 0.023042 0.8111 1.2793 0.1288 0.0% 0.5411 (e) Column ×0.99 + Linear (no tanh) 0.990 no 0.036987 0.095012 2.1288 0.9536 1.9467 0.6% 0.7835
G-T13 L3: sensory→motor 1,178 42 3.57% sensory→central 159,360 38,554 24.19% optic→descending 3,069 285 9.29% optic→motor 6 0 0.00%
G-T13 L6: Verificación: factor=1 vs factor=3 (5 controles cada uno)
G-T70 (Gemini): Sí. Aplicaste circularidad metodológica (específicamente Double Dipping y HARKing
mojo-absoluto hc2_shard_runner.py: SNAPS=(1,4,8,16); DT=.05 | scale=float(np.asarray(np.abs(A).sum(1)).max()); A=(A/np.float32(scale))
```

## 5. Archivos generados

- Este archivo.
- Inventario de 1.028 ítems (JSONL, 16 campos, con turno y cita) y la rúbrica v2: adjuntos al Doc de ClickUp. No commiteados por tamaño; se regeneran desde los 9 adjuntos con la rúbrica.

## 6. NO MEDIDO

1. Que el script L1-L6 de G sea el que generó la Tabla 7 publicada: solo coincide la salida; el código del PDF perdió la indentación y no se ejecutó.
2. Retención λ_F y asimetría R contra null anatómico y con n>=40: solo hay MS y CP con n=5.
3. La causa del salto gustativo 203,9σ -> ~4,5σ.
4. Los logs crudos del MS-100: no están en el corpus.
5. max|h| en HC-2.
6. Las 1.028 etiquetas: revisé contra la fuente las ~20 que sostienen este informe y corregí 2; el resto no se re-auditó una por una.
7. `CONCATETOMAMARZO22.pdf`: OCR solo de p.1, 50 y 101.

## 7. Qué sigue

1. Preregistrar «retención topológica»: λ_F y R contra null anatómico + MS + CP, n>=40, umbral fijado antes de correr.
2. Reconstruir y correr el script L1-L6 y comparar bit a bit con la Tabla 7.
3. Re-correr el Script R con null anatómico antes de decir «robusto».
4. Sacar A1 v4-v8 de cualquier lista de evidencia.

--- METODO ---
Acción delicada: NO
Máquina: sandbox + GitHub API + ClickUp
Instrumento: 19 mineros con rúbrica fija + verificación propia por grep contra el corpus limpio
Review externo: ninguno
NO MEDIDO: sección 6
