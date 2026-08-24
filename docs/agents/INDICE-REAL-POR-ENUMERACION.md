# ÍNDICE REAL · por **enumeración de IDs**, no por cosecha del chat

**Última pasada:** 2026-08-24 13:35 (America/Buenos_Aires) · **Estado: PARCIAL, pasada 4 de N.** **46 de ~65 identificados (71%).**

**Por qué existe y no basta `INDICE-DE-ENLACES.md`:** ese índice se armó **desde los fragmentos de chat que Abraham pegó**, así que solo podía contener lo que algún mensaje citó. Este se arma **enumerando el espacio de IDs del workspace**. Frutos hasta ahora: `5177`, `5077` (el origen), `5117`, `5637` y ahora los cinco del lote 1, ninguno de los cuales estaba en el otro índice.

**Método:** IDs de página secuenciales, **paso 20**, prefijo `2kza6fw5-`. `load_assets` los acepta directo. **Límite medido en la pasada 4: cinco Docs completos no entran en una ventana** — el `6117` se cayó por tamaño y hubo que pedirlo aparte. El lote de 5 es el techo, y con un Doc grande adentro es 4 + 1.

---

# 🎯 EL ORIGEN

> **`doc:2kza6fw5-5077` · 21-ago · "Auditoría del paper del conectoma — hay UN número que puede invertir tu hallazgo central"**

Es el peritaje del PDF que Abraham adjuntó **una sola vez**: DOI `10.5281/zenodo.19136948`, 7 páginas. Instrumento `auditar_paper.py`, **21 chequeos: 15 OK, 6 FALLA, exit 0.**

Densidad reportada 0,0074 vs recomputada **0,000785** (factor **9,42×**) · `N=45.161` la haría cierta · `26,6/0,74 = 35,9` **confirma que 0,0074 es el número que usó el pipeline entero** · **Propiedades 1 y 3 comparten una sola celda** de la Tabla 8 · el **−24,8σ ignorado** es la desviación más grande de la tabla · con N=5 el `Z=14,8` vive entre **8,7 y 48** y el `p_perm` mínimo es **0,20** · 15 concretos incluido `DOI: 10.5281/zenodo.XXXXXXX` literal en el PDF publicado y el repo en **404**.

---

# 🚨 EL DOCUMENTO CON FECHAS · hallazgo de la pasada 4

> **`doc:2kza6fw5-6117` · "PLAN MAESTRO 10 SEMANAS · 24-ago al 8-nov 2026"** · 100/100

**No estaba en ningún contexto vivo, y su primer umbral vence el 30-ago.** Hoy es el 24-ago: **la S1 es esta semana.**

| # | Número que decide el éxito | Umbral | Si no llega |
|---|---|---|---|
| 1 | **Erratum en Zenodo** | **antes del 30-ago** | *«todo lo demás se lee con desconfianza»* |
| 2 | Motivos con 0/40 en la biblioteca | ≥ 3 | P3 se reagenda |
| 3 | Nulls del motor complejo | **40** (piso de `p` 0,20 → 0,0488) | sale de P4 |
| 4 | Papers subidos | ≥ 2 antes del 8-nov | *«el año no produjo publicación»* |

**Deadlines externos** (verificados en vivo contra `arcprize.org` el 23-ago): **2-nov** código a Kaggle · **8-nov** papers · resultados 4-dic. Premios 450 mil (Paper Prize) + 850 mil (ARC-AGI-3). **El código no necesita puntuar alto** y puntean con **RHAE** (eficiencia de acción, no acierto): eso es lo que favorece estructura previa, y es la puerta real.

**Las 10 semanas:** S1 cerrar lo público · S2 los nulls que faltan · S3 dos o tres motivos más · S4 mecanismo de aprendizaje · **S5 P1** · **S6 P2** · S7 agente ARC-AGI-3 · S8 P4 · S9 revisión externa · S10 cerrar y subir. **Cada actividad lleva criterio de aborto.**

**Los 5 papers:** P1 auditoría de connectomíca dinámica (**evidencia completa, aborto: ninguno**) · P2 el 0,41% blindado (**evidencia completa**) · P3 biblioteca de primitivas (**1 de 3-4 motivos**) · P4 ARC (depende de P1 y P2) · P5 Paper 2 como resultado negativo. **P1 y P2 están en S5-S6 a propósito: si todo lo demás falla, esos dos salen.**

**El producto en tres capas:** (1) la fuente de calibración = el conectoma medido y sus priors · (2) el motor = SparseLTC/DualBrain, de 15M aristas a 704 B · (3) **la biblioteca = el activo**, hoy con **1** motivo de los 3-4 que hacen falta. La analogía operativa es **la hoja de datos de los 74xx**: cada entrada dice qué hace el circuito **y qué no**.

**Lo que el producto NO es:** no compite con Liquid AI (293 M USD, su modelo más chico es 230 M parámetros en Raspberry Pi; el target son **704 bytes** en un MCU sin SO) · no sirve para fusión de múltiples referencias (1,18× sobre LSTM aun en el óptimo) · **no se vende como «derivado del cerebro de la mosca»**: se venden microsegundos, miliwatts y BOM. El conectoma es el currículum, no el pitch.

**⚠️ CONTRADICCIÓN SIN RESOLVER:** el `6117` dice que el erratum está *«escrito y commiteado en `docs/ERRATUM.md`, 7 puntos»* y que **falta un solo dato: los dos DOI**. El `CONTEXTO-drosophila-fep.md` dice que **E3 no se puede subir** porque corrige una «Table 7» con columna Ratio y 1.559× que no existen en el PDF publicado. **Los dos no pueden ser ciertos.** Hay que abrir `docs/ERRATUM.md` y compararlo con el PDF: es lectura, no cómputo.

---

# 🧵 EL HILO DEL CONECTOMA, EN ORDEN

| # | ID | Qué pasó |
|---|---|---|
| **1** | `5077` | **Llega el paper.** 6 fallas aritméticas. Afirma que con la densidad correcta **4 de 9 clases pasan a ENRIQUECIDAS** |
| **2** | `5097` | **Busco quién refuta.** Nadie publicó lo mismo, **pero** aparece Therianos (arXiv 2606.17745, 16-jun): misma tesis, conectoma **larval**, **N=1.000 nulls** vs N=5, y **reciprocidad 26,09% vs 26,60%** |
| **3** | `5117` | **Se resuelve la densidad con Nature.** Lin et al. 2024 da **0,000161**: el 0,0074 es **46×** más. **Se descarta mi hipótesis del cerebro central** (el rich club concentra 5,4×, no 46×). Causa real: **el paper usa "synapses" en el abstract y "connections" en §2.1 para el mismo número**. Y **el «36×» no sobrevive**: con la densidad real es **1.652×**. Y **retiro el entusiasmo por Therianos**: Lin mide reciprocidad **13,8%** en el adulto, o sea que Abraham **coincide con el cerebro equivocado** |
| **4** | `5137` | Borrador **LTFF**, US$36.000. El conectoma **no entra** en el alcance del fondo |
| **5** | `5157` | **Erratum v1→v2 formal, E1-E8**, con **tres corchetes sin rellenar a propósito** |
| **6** | `5177` | **RETRACTACIÓN.** La expectativa de la Tabla 5 **NO es de densidad** (densidades implicadas 0,016719 y 0,014132; `Exp_m/Exp_g ∈ [6,68 , 8,82]` vs `N_m/N_g = 6,52`). **Se retira el "4 de 9 enriquecidas"** |

**La lección, escrita en el `5177`:** *"medí una cosa (la densidad) y concluí sobre otra (la Tabla 5, cuya expectativa no había inspeccionado). Es E-01 y lo hice con una rúbrica de 100/100 puesta."*

**Lo que bloquea publicar la v2:** los **tres corchetes** del `5157` necesitan una corrida del código de Abraham.

---

# 🔥 HALLAZGO DE LA PASADA 3: los bugs del Script R **ya están publicados**

> **`doc:2kza6fw5-5637`** grepeó el Script V-K, que es **el verificador que el manuscrito cita como garantía de reproducibilidad**, y encontró **14 citas al Script R** con número de línea:

```
101| #  DATA LOADING — from Script R (proven on Kaggle)
351| """Row normalization + scaling. From Script R."""
363| """Column normalization + scale to SR > 1. From Script R."""
375| """Scale raw weights to target spectral radius. From Script R."""
512| #  METRIC FUNCTIONS — from Script R (superior implementations)
```

**Consecuencia:** las tres funciones de normalización que producen el `SR = 4/4 PASS` de la Tabla S2 **son las del Script R**, y `normalize_global_spectral` tiene un **fallback silencioso**: si ARPACK no converge en 500 iteraciones, el esquema deja de ser "escalado a radio espectral" y pasa a ser "escalado por norma de Frobenius", **con el mismo nombre**. Eso explica el `SR = 0.990000` exacto, que es la cota y no el autovalor.

**Los bugs no son riesgo futuro: son deuda dentro del verificador que el paper cita.**

Y el `5617` (primera pasada sobre el mismo script) encontró que **el detector de divergencia es inalcanzable en las 5 configuraciones** (`np.clip` antes de `if max_h > 1e6`), que **`entropy_kde` con pad fijo devuelve `0.0000` en vez de `nan`** cuando la población colapsa, y que **el test "supercrítico" no puede dar su propio resultado** porque usa `clip=5.0`.

---

# 🔥 HALLAZGO DE LA PASADA 4: un test propio que **no podía fallar**

> **`doc:2kza6fw5-6057`** · el CP de 40 nulls salió (22,2 min) y el veredicto es sobre el instrumento:

```
  MBON->MOTOR   obs=  364  CP_mu=  364.0  sd= 0.0  ratio= 1.00x  n_ge=40/40
  visual->KC    obs=    0  CP_mu=    0.0  sd= 0.0  ratio=  inf   n_ge=40/40
  las 8 clases sensoriales -> motor:  sd = 0.0 EXACTO, ratio_CP = 1.000x
  rango CP = 1.0x   (contra grado preservado fue 283.2x, contra densidad 991x)
```

**La jerarquía de ruteo es una cantidad CONSERVADA bajo CP**, o sea **NO TESTEABLE**, y es aritmético: el null baraja destinos dentro de bloques definidos por (super_class emisor, super_class receptor), la columna de emisores no se toca, y **el grupo MOTOR está definido por la misma super_class**. El conteo visual→motor no puede cambiar ni en una arista. Idem `sensory→KC` y `MBON→motor`.

**Lo que SÍ sobrevive al CP, 0/40:** reciprocidad **20,59×** (← el número a publicar, no 47,3× ni 338,8×), `KC→MBON` **7,81×**, `DAN→KC` **8,71×**, `KC→KC` **7,26×**, `DAN→MBON` 1,88×, `ALPN→KC` 1,70×. El circuito de aprendizaje es **más que los módulos**, no solo más que los grados: la hipótesis queda **más fuerte**.

**El arreglo:** null de **tripartición** (sensorial / interno / motor), bloques más gruesos que la cantidad medida. Hasta entonces la etiqueta honesta es la que **ya tiene** el `README.md`. **Guard de 4 líneas:** si `sd(null) == 0`, reportar **NO TESTEABLE**, no `1,000×`.

---

## Zonas del espacio de IDs · **cinco líneas de trabajo**

| Rango | Fecha | Línea | Barrido |
|---|---|---|---|
| ~1057-1097 | 14-ago | MUDH v1.0, AURA OS (TITÁN Tao) | no barrido |
| ~3537-3617 | 16-ago | MUDH-Mobile, OPERIT clean-room, Tachi | 4 confirmados |
| ~4737-4937 | 21-ago | gateway MCP, Daytona, foros de agentes | 2 confirmados |
| **~5057-5177** | 21-ago | **🎯 CONECTOMA: el arranque** | **6 de 6 ✅** |
| ~5197-5537 | 22-ago | icca-engine.com / MCP / kiosco | 2 confirmados |
| ~5557-6357 | 22-24 ago | CONECTOMA, erratum, motores | **32 identificados** |

---

## A · 21-ago · CONECTOMA · EL ARRANQUE ✅ COMPLETO

| ID | Título | Veredicto |
|---|---|---|
| **`5077`** | Auditoría del paper ⭐⭐ | **EL ORIGEN.** 6 fallas, densidad 9,42× |
| `5097` | Busqué quién te refuta ⭐ | Therianos con N=1.000 |
| **`5117`** | **La densidad de Lin es 0,000161** ⭐⭐ | **46× de diferencia. El «36×» es 1.652×. Retira 2 afirmaciones propias** |
| `5137` | Borrador LTFF | El conectoma no entra en el alcance |
| `5157` | **Erratum formal E1-E8** ⭐ | Tres corchetes sin rellenar |
| `5177` | Tabla 5 no se puede recalcular ⭐ | **Retira 3 afirmaciones propias** |

## B · 21-ago · GATEWAY / INFRAESTRUCTURA

| ID | Veredicto |
|---|---|
| `4737` | `supply-chain` no son 7 tools: **7 que orquestan 90 técnicas sobre 21 fuentes**. **El multiplicador no es tener tools: es que el lazo de verificación cierre dentro de un turno** |
| `4937` | **"0 MCPs conectados" era FALSO**: 4 servicios, 69 tools. Moltbook (**204.940 agentes, Meta lo compró**). Daytona **elimina** el riesgo de suspensión cruzada |

## C · 22-ago · ICCA-ENGINE / MCP

| ID | Veredicto |
|---|---|
| `5217` | **76.266 servidores MCP, <5% cobra, 92,8% de endpoints pagos muertos** |
| `5297` | CI del kiosco 9/9 verde. **0 llamadas al gateway, 0 a Cloudflare** |

## D · 22 al 24-ago · CONECTOMA, PAPERS Y MOTORES

| ID | Qué establece |
|---|---|
| `5557` | DualBrain = banco de 16 filtros de ancho de banda adaptativo |
| `5597` | Auditoría de la Tabla 7 contra los 19+19: baja el Z=+14,8σ a z=15 |
| **`5617`** | **Auditoría 1 del Script R** ⭐⭐: divergencia **inalcanzable** en 5/5 configs · `entropy_kde` devuelve `0.0000` en vez de `nan` · **el test supercrítico no puede dar su resultado** · promete T4 y no usa GPU · **3 de sus 5 tests ya estaban corridos**. 93/100 |
| **`5637`** | **Auditoría 2 del Script R** ⭐⭐: **14 citas prueban que es el ANCESTRO del verificador que el paper cita** · `rdi_cosine` explica solo las 6-7 h (**22 millones de iteraciones de bucle Python**) · `return None` dentro del bucle · la población PER es **105 de 1.485 motoras (7,1%)**. 93/100 |
| `5657` | Índice cronológico maestro: 20 chats de Arena fechados ⭐ |
| `5677` | HANDOFF al 2026-08-22 23:47 |
| `5697` | La patente está ÍNTEGRA pero congelada. **Dos series de RDI incompatibles** |
| `5717` | RESUELTO: la patente tiene razón, el FALSIFIED es un artefacto |
| `5737` | visual/mu_optic vs 19 CP: sobrevive con **el signo INVERTIDO** ⭐ |
| `5757` | El **1.559× es artefacto de división por casi cero**, aparece 9 veces ⭐ |
| `5777` | Los 12 pares: entropía NO distingue 12/12; la FORMA sí 7/12 ⭐ |
| `5797` | ERRATUM v1→v2 (segunda versión del texto) |
| `5817` | El Script R acierta el diseño y falla la ejecución |
| `5837` | Las 5 normalizaciones: **R se invierte en visual (1,878 → 0,811)** ⭐ |
| `5857` | Encontré TU corrida del Script R: reproduce a 4-5 cifras |
| `5877` | Índice auditado de los 7 docs. **El TSV mutó**; la normalización «biológica» destruye la heterogeneidad (CV 2,402 → 0) ⭐ |
| `5897` | Qué se publica en criollo: **jerarquía de ruteo**, no frugalidad ⭐ |
| `5917` | **El 96% del cerebro NO aprende** (4,045% neuronas, 0,41% conexiones) ⭐ |
| **`5937`** | **Los 40 nulls cerraron: 0/40 en las 12 clases** ⭐⭐. **El centro de aprendizaje está BLINDADO**: cero sinapsis sensoriales directas a Kenyon donde el null pone 2.640, y MBON→motor depletado 0,41×. **Correcciones: el rango de ruteo cae de 991× a 283,2×** y **"visual es la vía con menos acceso motor" NO sobrevive** (es olfactory). 100/100 |
| **`5957`** | **Test global sobre los 12 pares** ⭐⭐: el real sale **1º de 20 grafos (0/19)** pero **NO llega a p=0,05** porque la dirección es post-hoc y el piso de dos colas con 19 nulls es 0,10. **El efecto ES la vía visual: S=4, el mínimo teórico.** Y la métrica del paper distingue **al máximo (240 de 240) en dirección contraria**. **40 nulls era el número correcto para el test correcto.** 100/100 |
| **`5977`** | **"Tenés razón y el error es mío"** ⭐⭐: metió el **RDI dinámico (z=197, el resultado más fuerte) en la columna de «frágil»**. **El eje no es estático vs dinámico: es CONTRA QUÉ NULL.** Lo que falla contra CP **no está refutado: la modularidad lo explica**. Y sus propios 40 nulls son MS, **nunca probados contra CP**. Bonus: el job local **no murió**, dio replicación cruzada JS/Python (46,88× vs 47,27×, el 0,8% explicado por la convención de swaps), y **la evidencia viaja byte-idéntica: el token no hacía falta**. 100/100 |
| **`6017`** | **La Tabla 7 no se reproduce en 4 particiones con la definición exacta del código** ⭐⭐, y **sus 6 valores no existen en ninguno de los 29 notebooks**: falta el instrumento, no el esfuerzo. **Mi hipótesis del desfasaje REFUTADA por lectura** (`res[t]=h.copy()` va después del update en los dos loops) **y sigue escrita en el `docs/ERRATUM.md` público**. «RDI» nombra **dos métricas** (3 pares con filtro `afferent` vs 6 sin filtro): esa era la causa de la discrepancia del 19+19. Un valor alto a t=15 es **imposible** con esa partición (las 3 modalidades caen en el bin `sensory`). `ORN` tiene **0 filas**: la rama del código es inerte. 100/100 |
| **`6057`** | **El test de la jerarquía de ruteo NO PODÍA FALLAR** ⭐⭐: `sd=0,0` exacto, `ratio=1,000`, 40/40 → **cantidad conservada bajo CP**. Reciprocidad cae a **20,59×** (el número a publicar) y `KC→MBON` **sobrevive** con 7,81× contra mi predicción. Hace falta un null de **tripartición**. Bonus: el `sqrt(a·b)` del Substrate Architect se equivoca **316.852×** y su `_cosine_distance` **premia al control muerto** (1,0000 le gana al real 0,7424): el mismo bug del 1.559× en otro lugar de la fórmula |
| **`6077`** | **Auditoría ejecutada del Complex-valued LTC ajeno** ⭐⭐: su null CP **destruye el grado entrante en 188/200 nodos** · `complex_tanh` tiene **POLOS** (`|tanh|=1e8` a `1e-8` del polo) y es el **default** · umbral de τ exacto **0,473116** sin validar · su generador usa `reciprocity_factor=36.0` y `density_intra=0.02`, o sea **está calibrado contra el error pre-erratum** · y su detector de 5 estados **no es falsable**: 14 umbrales a mano × ~280 evaluaciones con **una sola semilla**. **De acá salen `bounded_complex_tanh` y `validate_tau` del motor propio.** Retira 2 hallazgos propios (la máscara E/I por neurona **no** pierde nada: 0 mixtas de 138.005) |
| `6037` | **La Tabla 7 no es reproducible con el código archivado** ⭐ |
| `6097` | Auditoría de la jornada: 11/11. h_m mejora el paper 3,44× ⭐ |
| **`6117`** | **🚨 PLAN MAESTRO 10 SEMANAS** ⭐⭐ · ver la sección de arriba. **Erratum a Zenodo antes del 30-ago.** 100/100 |
| **`6137`** | **Los tres brazos: predicción REFUTADA 4/4** ⭐⭐, congelar `react` empeora 2,19× a 14,26×. **Error de diseño propio: congelé un react ALEATORIO, no uno CABLEADO** → midió el null de la hipótesis. El hallazgo de §3 (el brazo más congelado le gana a `DualNoGate` por 3,2× a 34,9×) es **CROSS-RUN** (`h_r=30 h_m=5` vs `26/8`): **indicativo, NO concluyente**, falta el brazo `D`. Y define el **brazo `S` (shuffle)**, sin el cual un `W` que funcione se explica por regularización. 98/100 |
| `6297` | El brazo W terminó completo y sin leer ⭐ |
| `6357` | Motor complejo vs SparseLTC: padre e hijo, p=0,6000 |

**Sin identificar en esta zona:** `6157`, `6177`, `6197`, `6217`, `6237`, `6257`, `6277`, `6317`, `6337`. **9 pendientes** (eran 14; el lote 1 cerró 5).

## E · 16-ago · MUDH-MOBILE

`3537` Hot-Update vía proot · `3577` OPERIT clean-room ("el profesor, no el socio") · `3597` PAQUETE MAESTRO para OpenCode · `3617` Auditoría D1-D7 para Tachi. `3557` sin respuesta, **no distinguido** entre inexistente y omitido.

---

## NO MEDIDO, declarado

- **46 de ~65 identificados** en el rango 3537-6357. **9 pendientes** en la zona del conectoma, ~15 en icca-engine, ~50 IDs sin barrer entre 3637 y 4717.
- **No barrido:** MUDH/AURA de 14-ago, nada por debajo de `3537` ni por encima de `6357`.
- **No conozco los límites del espacio.**
- **De los 32 de la sección D, 22 están identificados por TÍTULO**, no por lectura completa. Leídos en profundidad: `5617`, `5637`, `5937`, `5957`, `5977` (pasada 3) y `6017`, `6057`, `6077`, `6117`, `6137` (pasada 4).
- **`6057` y `6077` llegaron TRUNCADOS** (cortan en PARTE 4-6). Sus cierres no se leyeron.
- **No verifiqué si `2kza6fw5-` cubre todos los Docs.**
- **`3557` no distinguido** entre inexistente y omitido por tamaño.
- **Las fechas de ARC no las verifiqué yo:** vienen del `6117`, que dice haberlas chequeado en vivo el 23-ago. Un deadline de premio se re-verifica antes de planificar sobre él.

---

## Deuda que el barrido destapó y sigue abierta

1. **🚨 El erratum a Zenodo vence el 30-ago** (`6117`, umbral #1 de 4). Y hay una **contradicción sin resolver** sobre si está listo: hay que abrir `docs/ERRATUM.md`.
2. **Los tres corchetes del erratum** (`5157`): sin ellos la v2 no se publica. Necesitan una corrida de Abraham.
3. **El `README.md` público con la clasificación equivocada** (`5977`): el `temporal RDI` (`z=197`, el más fuerte) sigue marcado como frágil en un repo que va a citar un preprint con DOI.
4. **El `docs/ERRATUM.md` público tiene mi hipótesis del desfasaje, que está REFUTADA** (`6017`).
5. **La jerarquía de ruteo no tiene null válido** (`6057`): el CP la conserva. Hace falta el de tripartición antes de publicarla.
6. **Reciprocidad y KC→MBON contra CP: RESUELTO** (`6057`, 20,59× y 7,81×, 0/40). Lo que falta es el **tercer** null.
7. **Los 21 nulls que faltan** para que el test global llegue a p<0,05 (`5957`): ~30 min.
8. **Los bugs del Script R están dentro del verificador que el paper cita** (`5637`): se arreglan en el **V-K**, no en el R.
9. **El brazo `D` y el brazo `S`** (`6137`): sin `D` el hallazgo de §3 es cross-run; sin `S` el experimento del 96% no es falsable.

```
--- METODO TITAN ---
Accion delicada: NO. Lectura de 26 Docs por ID construido en cuatro pasadas,
                 cuatro escrituras de este archivo. Ninguna corrida, cero cuota.
Modo aplicado:   TITAN FULL
Rubrica:         no se emite: el barrido esta al 71%. Puntuar un indice
                 parcial como completo es el septimo patron del Bloque 8, y es
                 exactamente el error que cometi en la respuesta 036 citando
                 ESTE archivo como prueba de cierre.
N/A declarados:  pendiente
Review externo:  el metodo sigue siendo el falsador del indice viejo. En la
                 pasada 4 aparecio un documento con FECHAS que ningun contexto
                 vivo tenia (doc 6117: erratum a Zenodo antes del 30-ago, y
                 hoy es el 24) y un test propio que no podia fallar (doc 6057:
                 sd=0 exacto, 22,2 min de cuota para medir nada).
Instrumento:     load_assets con IDs construidos, no provistos.
                 Pasada 1: 5057, 5097, 5137, 5177, 5217, 5297, 3537, 3577,
                   3597, 3617. Sin respuesta: 3557.
                 Pasada 2: 4737, 4937, 5077, 5157.
                 Pasada 3: 5117, 5617, 5637, 5937, 5957, 5977.
                 Pasada 4 (lote 1): 6017, 6057, 6077, 6117, 6137. 5 de 5.
                   6117 omitido por tamano en la llamada de 5, recuperado solo.
                 NO MEDIDO: la seccion homonima.
```
