# ÍNDICE REAL · por **enumeración de IDs**, no por cosecha del chat

**Última pasada:** 2026-08-24 12:20 (America/Buenos_Aires) · **Estado: PARCIAL, pasada 2 de N.**

**Por qué existe y no basta `INDICE-DE-ENLACES.md`:** ese índice se armó **desde los fragmentos de chat que Abraham pegó**, así que solo podía contener lo que algún mensaje citó. Este se arma **enumerando el espacio de IDs del workspace**. La diferencia ya dio dos frutos: el `5177` y el **`5077`, que es el origen de todo.**

**Método:** IDs de página secuenciales, **paso 20**, prefijo `2kza6fw5-`. `load_assets` los acepta directo, sin que nadie pegue un enlace.

**Corrección de la pasada 1:** dije que el paso era 20 pero barrí de 40 en 40 sin darme cuenta, y por eso me saltee `5077`, `5117` y `5157`. **Uno de los tres era el documento más importante del proyecto.**

---

# 🎯 EL ORIGEN, ENCONTRADO

> **`doc:2kza6fw5-5077` · 21-ago-2026 · "Auditoría del paper del conectoma — hay UN número que puede invertir tu hallazgo central"**

**Acá arranca todo.** Es el peritaje del PDF que Abraham adjuntó **una sola vez**: *Signal Propagation Properties in the Drosophila melanogaster Connectome*, DOI `10.5281/zenodo.19136948`, 7 páginas, CC-BY 4.0.

**Instrumento:** `auditar_paper.py`, Python 3.12.13, **exit 0, 21 chequeos: 15 OK y 6 FALLA.** Salida cruda verbatim en el Doc.

| Lo que salió de ahí | |
|---|---|
| **Densidad** | reportada 0,0074 vs recomputada **0,000785**. Factor **9,42×**. Y `N = 45.161` la haría cierta: el tamaño del cerebro central sin lóbulos ópticos |
| **Reciprocidad** | `26,6 / 0,74 = 35,9×` coincide con el "36×" → **confirma que 0,0074 es el número que usó el pipeline entero** |
| **Propiedades 1 y 3** | comparten **una sola celda** de la Tabla 8 (`Z_CP = +14,8σ`, paso 195). Dos hallazgos contados como tres |
| **El −24,8σ ignorado** | es la desviación **más grande** de la tabla y el texto la despacha con un *"likely"*. Puede ser un **trade-off de diseño** publicable |
| **N=5** | error del σ del **35,4%**; el `Z=14,8` vive entre **8,7 y 48**; y el `p_perm` mínimo con 5 controles es **0,20** |
| **15 concretos** | el PDF publicado dice `DOI: 10.5281/zenodo.XXXXXXX` · Tabla 5 con 9 filas y Methods con 10 clases · `85.821 + 4.281 = 90.102`, no 90.101 · el repo da **404** · ORCID en el PDF y **no** en los metadatos de Zenodo |

**Veredicto de nivel:** no llega a *Nature*; **sí** a *Network Neuroscience*, *PLOS Complex Systems*, *Biomimetics* con los críticos resueltos; **sí ya** como preprint que respalda una solicitud de fondos. 100/100.

---

# 🧵 EL HILO DEL CONECTOMA, RECONSTRUIDO EN ORDEN

Esto es lo que Abraham pidió: dónde arranca y cómo sigue. **Los cinco eslabones del 21-ago, en secuencia:**

| # | ID | Qué pasó |
|---|---|---|
| **1** | `5077` | **Llega el paper. Auditoría: 6 fallas aritméticas, 4 críticos, 15 concretos.** Afirma que con la densidad correcta **4 de 9 clases pasan a ENRIQUECIDAS y el hallazgo central se invierte** |
| **2** | `5097` | **Se busca quién refuta.** Nadie publicó lo mismo, **pero** aparece Therianos (arXiv 2606.17745, 16-jun) con la misma tesis, **N=1.000 nulls** contra N=5, y **reciprocidad 26,09% vs 26,60%**: convergencia larva/adulto al medio punto |
| **3** | `5117` | **sin barrer** |
| **4** | `5137` | Borrador de solicitud al **LTFF**, US$36.000. Advertencia: el conectoma **no entra** en el alcance del fondo |
| **5** | `5157` | **Erratum v1→2 formal, 8 ítems (E1-E8)**, con **tres corchetes sin rellenar a propósito**: inventar un número en un erratum es peor que el error |
| **6** | `5177` | **RETRACTACIÓN.** Al intentar recalcular la Tabla 5 se descubre que **la expectativa NO es de densidad** (densidades implicadas 0,016719 y 0,014132; `Exp_m/Exp_g ∈ [6,68 , 8,82]` vs `N_m/N_g = 6,52`). **Se retira el "4 de 9 enriquecidas" del paso 1** |

**La lección del hilo, y está escrita en el propio `5177`:** *"medí una cosa (la densidad, mal reportada) y concluí sobre otra (la Tabla 5, cuya expectativa no había inspeccionado). Es E-01 y lo hice con una rúbrica de 100/100 puesta."*

**Y la consecuencia práctica es buena:** puede que la Tabla 5 esté bien y el erratum solo tenga que corregir la densidad, el 36× y **la definición de la expectativa**. Mucho menos grave de lo que dijo el paso 1.

**Lo que sigue abierto de este hilo:** los **tres corchetes** del `5157` necesitan una corrida del código de Abraham. Sin ellos el erratum no se publica.

---

## Zonas del espacio de IDs · **son cinco líneas, no tres**

| Rango | Fecha | Línea | Barrido |
|---|---|---|---|
| ~1057-1097 | 14-ago | MUDH v1.0, AURA OS (TITÁN Tao) | no barrido |
| ~3537-3617 | 16-ago | MUDH-Mobile, OPERIT clean-room, Tachi | 4 confirmados |
| ~4737-4937 | 21-ago | **gateway MCP, Daytona, foros de agentes** ← NUEVO | 2 confirmados |
| **~5057-5177** | 21-ago | **🎯 CONECTOMA: el arranque** | **5 de 6 confirmados** |
| ~5197-5537 | 22-ago | icca-engine.com / MCP / kiosco | 2 confirmados |
| ~5557-6357 | 22-24 ago | CONECTOMA, erratum, motores | ~21 identificados |

---

## A · 21-ago · CONECTOMA (el arranque)

| ID | Título | Veredicto |
|---|---|---|
| **`5077`** | **Auditoría del paper del conectoma** ★★ | **EL ORIGEN.** 6 fallas, densidad 9,42×, Propiedades 1 y 3 comparten evidencia. 100/100 |
| `5097` | Busqué quién te refuta ★ | Therianos con N=1.000. Reciprocidad convergente al medio punto. 100/100 |
| `5117` | **sin barrer** | |
| `5137` | Borrador LTFF | US$36.000. El conectoma no entra en el alcance |
| `5157` | **Erratum v1→2 formal (E1-E8)** ★ | Tres corchetes sin rellenar. "No publiques la v2 solo con el erratum" |
| `5177` | Tabla 5 no se puede recalcular ★ | **Retira 3 afirmaciones propias.** La expectativa no es de densidad |

## B · 21-ago · GATEWAY / INFRAESTRUCTURA (línea distinta)

| ID | Título | Veredicto |
|---|---|---|
| `4737` | Relevamiento del potencial si me conectás el gateway | `supply-chain` no son 7 tools: son **7 que orquestan 90 técnicas sobre 21 fuentes**. Y **el multiplicador no es tener tools: es que el lazo de verificación cierre dentro de un turno** |
| `4937` | Tenías razón en las tres ★ | **"0 MCPs conectados" era FALSO**: 4 servicios, 69 tools. Moltbook (**204.940 agentes, Meta lo compró**), The Colony con MCP. Daytona **elimina** el riesgo de suspensión cruzada |

## C · 22-ago · ICCA-ENGINE / MCP

| ID | Título | Veredicto |
|---|---|---|
| `5217` | El océano azul NO es la web | **76.266 servidores MCP, <5% cobra, 92,8% de endpoints pagos muertos** |
| `5297` | El run del fix VERDE 9/9 | 0 llamadas al gateway, 0 a Cloudflare. Deuda del `09-bundle` |

## D · 22 al 24-ago · CONECTOMA, PAPERS Y MOTORES

| ID | Qué establece |
|---|---|
| `5557` | DualBrain = banco de 16 filtros de ancho de banda adaptativo |
| `5597` | Auditoría de la Tabla 7 contra los 19+19: baja el Z=+14,8σ a z=15 |
| `5657` | Índice cronológico maestro: 20 chats de Arena fechados ★ |
| `5677` | HANDOFF al 2026-08-22 23:47 |
| `5697` | La patente está ÍNTEGRA pero congelada. **Dos series de RDI incompatibles** |
| `5717` | RESUELTO: la patente tiene razón, el FALSIFIED es un artefacto |
| `5737` | visual/mu_optic vs 19 CP: sobrevive con **el signo INVERTIDO** ★ |
| `5757` | El **1.559× es artefacto de división por casi cero**, y aparece 9 veces ★ |
| `5777` | Los 12 pares: entropía NO distingue 12/12; la FORMA sí 7/12 ★ |
| `5797` | ERRATUM v1→v2 (segunda versión del texto) |
| `5817` | El Script R acierta el diseño y falla la ejecución |
| `5837` | Las 5 normalizaciones: **R se invierte en visual (1,878 → 0,811)** ★ |
| `5857` | Encontré TU corrida del Script R: reproduce a 4-5 cifras |
| `5877` | Índice auditado de los 7 docs. **El TSV mutó**; la normalización «biológica» destruye la heterogeneidad (CV 2,402 → 0) ★ |
| `5897` | Qué se publica en criollo: **jerarquía de ruteo**, no frugalidad ★ |
| `5917` | **El 96% del cerebro NO aprende** (4,045% neuronas, 0,41% conexiones) ★ |
| `5997` | ERRATUM v2, 7 puntos. **Mi RDI no reproduce la Tabla 7 a t=60 (factor 2,9)** ★ |
| `6037` | **La Tabla 7 no es reproducible con el código archivado** ★ |
| `6097` | Auditoría de la jornada: 11/11. h_m mejora el paper 3,44× ★ |
| `6297` | El brazo W terminó completo y sin leer ★ |
| `6357` | Motor complejo vs SparseLTC: padre e hijo, p=0,6000 |

**Sin identificar en esta zona:** `5617`, `5637`, `5937`, `5957`, `5977`, `6017`, `6057`, `6077`, `6117`, `6137`, `6157`, `6177`, `6197`, `6217`, `6237`, `6257`, `6277`, `6317`, `6337`. **19 pendientes.**

## E · 16-ago · MUDH-MOBILE

`3537` Hot-Update vía proot · `3577` OPERIT clean-room ("el profesor, no el socio") · `3597` PAQUETE MAESTRO para OpenCode · `3617` Auditoría D1-D7 para Tachi. `3557` sin respuesta y **no distinguido** entre inexistente y omitido.

---

## NO MEDIDO, declarado

- **35 de ~65 IDs identificados** en el rango 3537-6357. 19 pendientes en la zona del conectoma, ~15 en icca-engine, ~10 entre 3637 y 5037.
- **`5117` sin barrer**, y está en el medio del hilo del arranque. Puede ser un eslabón.
- **No barrido:** MUDH/AURA de 14-ago, nada por debajo de `3537` ni por encima de `6357`.
- **No conozco los límites del espacio.**
- **De los 21 de la sección D, la mayoría está por TÍTULO**, no por lectura completa en estas dos pasadas.
- **No verifiqué si `2kza6fw5-` cubre todos los Docs.**
- **`3557` no distinguido** entre inexistente y omitido por tamaño.

---

## Próxima pasada

1. **`5117`**, que está en el medio del hilo del arranque.
2. Los **19 pendientes** de la zona del conectoma (`5617`-`6337`).
3. El hueco `3637-4717` y `4957-5037`.
4. icca-engine y MUDH/AURA al final: son otras líneas.

```
--- METODO TITAN ---
Accion delicada: NO. Lectura de 15 Docs por ID construido en dos pasadas, dos
                 escrituras de este archivo. Ninguna corrida, cero cuota ajena.
Modo aplicado:   TITAN FULL
Rubrica:         no se emite: el barrido esta al ~54%. Puntuar un indice
                 parcial como completo es el septimo patron del Bloque 8, y ya
                 lo cometi tres veces con el indice anterior.
N/A declarados:  pendiente
Review externo:  el metodo es el falsador del indice viejo, y en esta pasada
                 tambien de MI PROPIA pasada 1: dije paso 20 y barri de 40 en
                 40, salteandome el 5077, que es el documento que ancla el
                 proyecto entero. Un metodo correcto mal ejecutado produce el
                 mismo agujero que un metodo malo.
Instrumento:     load_assets con IDs construidos, no provistos.
                 Pasada 1: 5057, 5097, 5137, 5177, 5217, 5297, 3537, 3577,
                 3597, 3617. Sin respuesta: 3557.
                 Pasada 2: 4737, 4937, 5077, 5157.
                 NO MEDIDO: la seccion homonima.
```
