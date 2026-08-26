# 074 · HANDOFF para chat nuevo · estado al 2026-08-25 08:40

**Leer esto primero, junto con `CONTEXTO-drosophila-fep.md` y `CONTEXTO-motor.md`.**

> **⚠️ Los dos contextos vivos están VENCIDOS: terminan antes de la resp 063.** Todo lo de abajo desde el null anatómico en adelante está en las **respuestas 063 a 073** de la rama `titan/twohop-nulls`, no en el contexto. **Ese es el hallazgo A-12 de la auditoría externa y sigue sin arreglar.**

---

## 0. 🚨 EL RELOJ

| Qué | Cuándo | Estado |
|---|---|---|
| **Erratum a Zenodo** | **antes del 30-ago** (faltan 5 días) | ✅ **texto listo en `docs/ERRATUM.md`**, 9 ítems, claim falso retirado, Bates citado. **Falta la acción de Abraham** |
| Papers a ARC Prize | 8-nov-2026 | 0 subidos |

**El erratum NO está en riesgo por la auditoría:** ninguno de los 13 hallazgos toca sus nueve ítems, y Tao lo confirma explícitamente.

---

## 1. Lo que se hizo en esta sesión, en una tabla

| # | Turno | Resultado |
|---|---|---|
| 057 | verificar prior art de Lin | 🔴 **Lin SÍ descompone reciprocidad** (Fig. 5c, ED Fig. 6c). Mi claim de novedad era falso |
| 059 | corregir el erratum | ✅ frase falsa retirada, novedad angostada al **eje funcional**, Bates citado |
| 061 | null de grado a 2 saltos | ✅ spread 323×, 0/40 y 40/40. Y cerré el 105 vs 110 |
| 063 | **null ANATÓMICO** | 🔴 **el spread de 323× colapsa a 2,4× y 3 de 4 signos se invierten.** El dato estaba en Zenodo a una llamada |
| 065 | LC6→GF contra neuropilos | ✅ **sobrevive**: null predice 17,2 ± 3,1, hay 0, z = −5,6 |
| 066-067 | barrer literatura | 🔴 **la tabla de ruteo ya está publicada** (Kind 2024 + Cell Type Explorer de `flywire-fafb:v783b`) |
| 068 | corregir biblioteca | 🔴 el GF es **67,6% central y 49,8% inhibitorio**. Mi «0 inhibitorias» era de un recorte del 20% |
| 069 | compilar las 962 | 🔴 **mi predicción se refuta**: el recorte *sobreestimaba* la selectividad de pico |
| 070 | barrer τ heterogénea | 🔴 τ no rescata nada, **y descubrí que medía la métrica equivocada** |
| 071 | null sobre `sel_post` | 🟢 **0/40 en 7 de 7 configuraciones**, z hasta +181,4 |
| 073 | responder auditoría de Tao | 🔴 **13 de 13 hallazgos aceptados. 62/100, RECHAZADO como release** |

---

## 2. 🟢 Lo que sobrevive con evidencia, y es el activo

**El resultado más fuerte del expediente, con doble instrumento:**

> **La topología de este circuito define selectividad temporal en el TRANSITORIO POST-ESTÍMULO, no en la amplitud de pico.**

| Medición | Número |
|---|---|
| `sel_post` observado | **4,3287** |
| contra null de **topología** | 1,1896 ± 0,0173 → **z = +181,4**, 0/40 |
| contra null de **signo que respeta Dale** | 1,7983 ± 0,401 → **z = +6,31**, 0/40 |
| `sel_peak` en la misma corrida | **debajo** de su null (z = −2,41) |
| actividad post-estímulo **absoluta** | **2,77 contra 16,09** del null → el circuito **resuena MENOS y de forma diferencial** |

**Y lo que lo hace valioso:** es cualitativa y cuantitativamente **la Propiedad 3 del Paper 1** (RDI post-estímulo, `z = 197` medido en el conectoma). **Dos instrumentos independientes, mismo fenómeno.** Y es el territorio que BANC declara no cubrir (su métrica es steady-state y sin signo).

**También sigue en pie:** 0 sensorial→KC contra nulls de 1.533–2.640 · 0/40 en 12 de 12 pares del centro de aprendizaje · reciprocidad 20,59× vs CP · Dale exacta (0 mixtas de 138.005) · **LC6→GF = 0 contra el null anatómico** · 1.336 B de `.text` en ESP32.

---

## 3. 🔴 Las ocho autorrefutaciones, y todas tienen la misma forma

1. el desglose de reciprocidad era prior art de Lin
2. el cero de motoras de cabeza era **geometría**, no prohibición
3. «las cuatro clases son igual de locales» era **falso** (104 de 110 motoras viven en GNG/PRW, y mechano y gustativa también)
4. el piso de 0,652× era anatomía, no propiedad del conectoma
5. la tabla de ruteo ya estaba publicada, **desde mi mismo snapshot**
6. el «0 inhibitorias» describía un recorte del 20%
7. el AMMC al 33,5% era **localización de sinapsis**, no origen de señal (la real es 2,0%)
8. medí `sel_peak` seis días, y el pico es **lo único que este circuito no discrimina**

> **La forma común: medí bien y después afirmé sobre la NOVEDAD o la CAUSA sin medir eso.** Las mediciones no fallaron nunca.

**Las dos reglas que salen, y son las más caras:**
- **Buscar el prior art ANTES de medir.** El barrido costó menos que la corrida que lo precedió.
- **Antes de medir un par en un conectoma público, buscar si existe un CATÁLOGO navegable de ese snapshot.** El conteo ya está publicado por construcción: **el null es el producto, no el número.**

---

## 4. 🔴 La auditoría externa de Tao · 62/100, RECHAZADO

**Rama `titan/auditoria-integra-2026-08-25`, PR #3.** 13 hallazgos, **13 aceptados por mí, 0 rechazados.** Verifiqué tres independientemente y los tres dieron confirmado.

**Su diagnóstico, verbatim, y es el mejor resumen del estado real:**

> *«El problema no es que el proyecto no tenga resultados; es que **la rama pública, el ejecutor y el testigo no están alineados**.»*

**Los cinco bloqueantes:** A-01 los guards imprimen rojo y salen con 0 · A-02 `guards.py` confunde conservación con saturación · A-03 no hay entorno reproducible (sin pins, sin lockfile, sin CI) · A-04 los JSON chicos (191 KB y 31 KB) no están en `results/` · A-05 el clon fresco no corre (rutas `/workspace/` absolutas).

**El que más puede doler y NO verifiqué: A-10.** Si el mapeo `id2i` de `scriptR.py` no coincide con el índice real del parquet, **los 30/30 valores reproducidos reproducen un bug.**

**Lo que más vale de su auditoría, y no es un hallazgo:** mis ocho autorrefutaciones son **todas científicas**. Sus cinco bloqueantes son **todos de infraestructura**, porque yo nunca miré ahí. Es el sesgo de selección que un instrumento propio no cubre.

**Y su orden de reparación es mejor que el mío:** *«primero lo que vuelve confiable al testigo; después lo que amplía el claim»*.

---

## 5. Decisiones esperando a Abraham

1. **🔴 SUBIR EL ERRATUM A ZENODO antes del 30-ago.** Listo en `docs/ERRATUM.md`. **W-01: leelo una vez antes, soy el único testigo de que la corrección está bien.**
2. **🔴 El cronograma.** La reparación de infraestructura son días y **no estaba en ninguno de los cinco entregables del plan de 10 semanas**. O se corre el cronograma, o se mata un entregable. **No lo decido yo.**
3. **¿Abro los 13 issues de la auditoría?** Son 5+ escrituras y requieren tu confirmación. Sin issues, los hallazgos son deuda sin dueño.
4. **Mergear o partir el PR #2** (nueve respuestas y siete scripts nuevos) y **cerrar o retargetear el PR #1**, que está viejo.
5. **Reclasificar el `temporal RDI` del README**, que hoy lo llama «negative methodological result» cuando es lo único que BANC no cubre.
6. **¿Adoptar el umbral de 5 sinapsis?** Los tres papers de referencia lo usan y es **técnicamente mejor**: destapó un estadístico que sin él no se podía usar.

---

## 6. Los pendientes técnicos, en orden

1. **A-01 y A-02:** un `require()` único que aborte, tests negativos con exit distinto de cero, y arreglar `guards.py`. **Ya hay un ejemplo funcionando en `src/signshuffle_dale.py`** (returncode 2 verificado con `subprocess`, porque **el `$?` de este shell miente**).
2. **A-03:** pins, lockfile, CI mínimo.
3. **A-04:** commitear los JSON chicos con su SHA-256.
4. **A-05:** rutas por argumento. **Los cinco scripts nuevos ya lo hacen**; los dos `.mjs` del release no.
5. **A-07 y A-08:** baseline pareado en grado, y null anatómico **por sinapsis** en vez de neuropilo dominante.
6. **A-10:** verificar el mapeo `id2i`. **Prioridad máxima de los técnicos.**
7. **A-12:** unificar los contextos vivos. Lo declaré cuatro veces sin hacerlo.
8. **Del claim `sel_post`:** barrer la **ventana de integración** (integra 120 pasos cuando la memoria efectiva es ~8) y **τ compleja**, el banco de osciladores del motor real.

---

## 7. Lo que no se movió en toda la sesión

Null de tripartición · 21 nulls del test global de 12 pares · script de la Tabla 8 · la décima clase de la Tabla 5 · la fila AN · Betzel y los dos DOI sin verificar · la hipótesis del 96% fijo sobre SparseLTC (la deuda más vieja) · la regla de tres factores del aprendizaje · los 6 `.py` de deuda · **motivos de biblioteca: sigue habiendo 1 de los 3-4 que pide el plan.**
