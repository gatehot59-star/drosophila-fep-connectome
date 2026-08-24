# ÍNDICE REAL · por **enumeración de IDs**, no por cosecha del chat

**Última pasada:** 2026-08-24 12:30 (America/Buenos_Aires) · **Estado: PARCIAL, pasada 3 de N.** 41 de ~65 identificados.

**Por qué existe y no basta `INDICE-DE-ENLACES.md`:** ese índice se armó **desde los fragmentos de chat que Abraham pegó**, así que solo podía contener lo que algún mensaje citó. Este se arma **enumerando el espacio de IDs del workspace**. Frutos hasta ahora: `5177`, `5077` (el origen), `5117` y `5637`, ninguno de los cuales estaba en el otro índice.

**Método:** IDs de página secuenciales, **paso 20**, prefijo `2kza6fw5-`. `load_assets` los acepta directo.

---

# 🎯 EL ORIGEN

> **`doc:2kza6fw5-5077` · 21-ago · "Auditoría del paper del conectoma — hay UN número que puede invertir tu hallazgo central"**

Es el peritaje del PDF que Abraham adjuntó **una sola vez**: DOI `10.5281/zenodo.19136948`, 7 páginas. Instrumento `auditar_paper.py`, **21 chequeos: 15 OK, 6 FALLA, exit 0.**

Densidad reportada 0,0074 vs recomputada **0,000785** (factor **9,42×**) · `N=45.161` la haría cierta · `26,6/0,74 = 35,9` **confirma que 0,0074 es el número que usó el pipeline entero** · **Propiedades 1 y 3 comparten una sola celda** de la Tabla 8 · el **−24,8σ ignorado** es la desviación más grande de la tabla · con N=5 el `Z=14,8` vive entre **8,7 y 48** y el `p_perm` mínimo es **0,20** · 15 concretos incluido `DOI: 10.5281/zenodo.XXXXXXX` literal en el PDF publicado y el repo en **404**.

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

## Zonas del espacio de IDs · **cinco líneas de trabajo**

| Rango | Fecha | Línea | Barrido |
|---|---|---|---|
| ~1057-1097 | 14-ago | MUDH v1.0, AURA OS (TITÁN Tao) | no barrido |
| ~3537-3617 | 16-ago | MUDH-Mobile, OPERIT clean-room, Tachi | 4 confirmados |
| ~4737-4937 | 21-ago | gateway MCP, Daytona, foros de agentes | 2 confirmados |
| **~5057-5177** | 21-ago | **🎯 CONECTOMA: el arranque** | **6 de 6 ✅** |
| ~5197-5537 | 22-ago | icca-engine.com / MCP / kiosco | 2 confirmados |
| ~5557-6357 | 22-24 ago | CONECTOMA, erratum, motores | **27 identificados** |

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
| `6037` | **La Tabla 7 no es reproducible con el código archivado** ⭐ |
| `6097` | Auditoría de la jornada: 11/11. h_m mejora el paper 3,44× ⭐ |
| `6297` | El brazo W terminó completo y sin leer ⭐ |
| `6357` | Motor complejo vs SparseLTC: padre e hijo, p=0,6000 |

**Sin identificar en esta zona:** `6017`, `6057`, `6077`, `6117`, `6137`, `6157`, `6177`, `6197`, `6217`, `6237`, `6257`, `6277`, `6317`, `6337`. **14 pendientes.**

## E · 16-ago · MUDH-MOBILE

`3537` Hot-Update vía proot · `3577` OPERIT clean-room ("el profesor, no el socio") · `3597` PAQUETE MAESTRO para OpenCode · `3617` Auditoría D1-D7 para Tachi. `3557` sin respuesta, **no distinguido** entre inexistente y omitido.

---

## NO MEDIDO, declarado

- **41 de ~65 identificados** en el rango 3537-6357. **14 pendientes** en la zona del conectoma, ~15 en icca-engine, ~50 IDs sin barrer entre 3637 y 4717.
- **No barrido:** MUDH/AURA de 14-ago, nada por debajo de `3537` ni por encima de `6357`.
- **No conozco los límites del espacio.**
- **De los 27 de la sección D, 22 están identificados por TÍTULO**, no por lectura completa. Los 5 leídos en profundidad en esta pasada son `5617`, `5637`, `5937`, `5957`, `5977`.
- **No verifiqué si `2kza6fw5-` cubre todos los Docs.**
- **`3557` no distinguido** entre inexistente y omitido por tamaño.

---

## Deuda que el barrido destapó y sigue abierta

1. **Los tres corchetes del erratum** (`5157`): sin ellos la v2 no se publica.
2. **El `README.md` público con la clasificación equivocada** (`5977`): el `temporal RDI` sigue marcado como frágil en un repo que va a citar un preprint con DOI.
3. **Reciprocidad y KC→MBON nunca probados contra CP** (`5977`, `5937`): los 40 nulls son MS.
4. **Los 21 nulls que faltan** para que el test global llegue a p<0,05 (`5957`): ~30 min.
5. **Los bugs del Script R están dentro del verificador que el paper cita** (`5637`): `normalize_global_spectral` y `entropy_kde` hay que arreglarlos **en el V-K**, no en el R.

```
--- METODO TITAN ---
Accion delicada: NO. Lectura de 21 Docs por ID construido en tres pasadas,
                 tres escrituras de este archivo. Ninguna corrida, cero cuota.
Modo aplicado:   TITAN FULL
Rubrica:         no se emite: el barrido esta al ~63%. Puntuar un indice
                 parcial como completo es el septimo patron del Bloque 8.
N/A declarados:  pendiente
Review externo:  el metodo sigue siendo el falsador del indice viejo. En esta
                 pasada aparecio el hallazgo mas grave del expediente y no
                 estaba en ningun contexto vivo: los bugs del Script R estan
                 DENTRO del verificador que el paper publica como garantia de
                 reproducibilidad (doc 5637, 14 citas con numero de linea).
Instrumento:     load_assets con IDs construidos, no provistos.
                 Pasada 1: 5057, 5097, 5137, 5177, 5217, 5297, 3537, 3577,
                   3597, 3617. Sin respuesta: 3557.
                 Pasada 2: 4737, 4937, 5077, 5157.
                 Pasada 3: 5117, 5617, 5637, 5937, 5957, 5977.
                 NO MEDIDO: la seccion homonima.
```
