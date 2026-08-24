# ÍNDICE REAL · por **enumeración de IDs**, no por cosecha del chat

**Creado:** 2026-08-24 12:10 (America/Buenos_Aires) · **Estado: PARCIAL, pasada 1 de N.**

**Por qué existe este archivo y no basta `INDICE-DE-ENLACES.md`:** ese índice se armó **desde los fragmentos de chat que Abraham pegó**, así que solo podía contener lo que algún mensaje citó. Este se arma **enumerando el espacio de IDs del workspace**, que es la lista de lo que existe. La diferencia ya dio fruto: **el Doc `5177` no estaba en el otro**, y es de la línea del conectoma con 100/100.

<p><br/></p>

**Método, verificado:** los IDs de página son **secuenciales con paso 20** bajo el prefijo `2kza6fw5-`, y `load_assets` los acepta directo. No hace falta que nadie pegue un enlace.

**Por qué va commiteado parcial:** cada Doc vuelve con su contenido completo (10-30 KB). **El barrido de ~65 IDs no entra en una ventana de conversación.** Se commitea por pasadas para que un corte de contexto no lo tire. Prometer el barrido completo de una sola vez sería el error de siempre.

---

## HALLAZGO DE ESTA PASADA · no son tres proyectos, son **CUATRO**

En la respuesta 031 dije tres. **Falso, medido en esta pasada:** el rango `5197-5537` no es conectoma, es la línea de **icca-engine.com / MCP / kiosco**.

| Rango de ID | Fecha | Proyecto | Estado del barrido |
|---|---|---|---|
| ~1057-1097 | 14-ago | **MUDH v1.0, AURA OS** (TITÁN Tao) | no barrido |
| ~3537-3617 | 16-ago | **MUDH-Mobile, OPERIT clean-room, Tachi** | 4 confirmados |
| ~5057-5177 | 21-ago | **arranque: publicación, prior art, financiamiento** | 4 confirmados |
| **~5197-5537** | 22-ago | **icca-engine.com / MCP / kiosco** ← **NUEVO** | 2 confirmados, ~15 sin barrer |
| ~5557-6357 | 22 al 24-ago | **CONECTOMA, papers, erratum, motores** | ~21 identificados |

**Cinco líneas de trabajo en un solo espacio de nombres, sin separador.** Eso es el mecanismo del guiso, y ahora tiene coordenadas.

---

## A · 21-ago · EL ARRANQUE (lo que rodea al paper publicado)

| ID | Título | Línea | Veredicto |
|---|---|---|---|
| `5057` | Tenías el círculo cerrado y yo no lo vi: los papers SON el corpus | publicación | **arXiv cerró la puerta el 21-ene-2026** (exige email académico + autoría previa). **Zenodo abierto, DOI gratis, sin institución.** 100/100 |
| `5097` | Busqué quién te refuta | **conectoma** ★ | **Nadie publicó lo tuyo.** PERO existe **Therianos, arXiv 2606.17745 (16-jun-2026)**: misma tesis, conectoma **larval**, **N=1.000 nulls** contra tu N=5. Y **reciprocidad 26,09% vs tu 26,60%**: convergencia entre larva y adulto al medio punto. 100/100 |
| `5137` | Borrador de la solicitud al LTFF | financiamiento | US$36.000 / 6 meses. **Advertencia: el conectoma no entra en el alcance del fondo**; el encuadre tiene que ser MUDH. 100/100 |
| `5177` | Tabla 5 — no se puede recalcular | **conectoma** ★ | **NO estaba en el índice viejo.** Retira tres afirmaciones propias: **la expectativa de la Tabla 5 NO es de densidad** (densidades implicadas 0,016719 y 0,014132; `Exp_m/Exp_g ∈ [6,68 , 8,82]` vs `N_m/N_g = 6,52`). 100/100 |

**Lo que ubica esta zona:** acá arranca el trabajo sobre el paper publicado. El `5097` es el más importante de los cuatro y **no estaba siendo usado en ninguna decisión reciente**.

---

## B · 22-ago · ICCA-ENGINE / MCP (línea distinta, NO conectoma)

| ID | Título | Veredicto |
|---|---|---|
| `5217` | Tu intuición del océano azul es correcta y el océano NO es la web | **76.266 servidores MCP, 602.506 tools, <5% cobra, precio promedio $0**, y **92,8% de los endpoints pagos están muertos** (7,2% vivos de 13.334 probados). Declara que 163 tests propios apuntaban al canal equivocado. 100/100 |
| `5297` | El run del fix está VERDE 9/9 | CI del kiosco completo por primera vez. Auditoría de llamadas: **0 al MUDH Gateway, 0 a Cloudflare**. Deuda: `09-bundle` da exit 0 sin publicar los bytes. 100/100 |

**~15 IDs de esta zona sin barrer** (`5197`, `5237-5277`, `5317-5537`).

---

## C · 22 al 24-ago · CONECTOMA, PAPERS Y MOTORES

Identificados por título (la mayoría ya en el índice viejo). **Los marcados ★ son los que cambian el estado del proyecto.**

| ID | Qué establece | Línea |
|---|---|---|
| `5557` | DualBrain es un banco de 16 filtros de ancho de banda adaptativo. Gana 23× donde gana, pierde donde pierde | motor |
| `5597` | Auditoría de la Tabla 7 contra los 19+19: baja el Z=+14,8σ a z=15 | conectoma |
| `5657` | Índice cronológico maestro: 20 chats de Arena fechados ★ | continuidad |
| `5677` | HANDOFF al 2026-08-22 23:47 | continuidad |
| `5697` | La patente está ÍNTEGRA pero congelada antes del erratum. **Dos series de RDI incompatibles** | patente |
| `5717` | RESUELTO: la patente tiene razón y el FALSIFIED es un artefacto | conectoma |
| `5737` | visual/mu_optic vs 19 CP: sobrevive con **el signo INVERTIDO** (dH −9,79 vs −2,88, z=18,1) | conectoma ★ |
| `5757` | PAPER 1 es el más honesto, pero el **1.559× es artefacto de división por casi cero** y aparece 9 veces | conectoma ★ |
| `5777` | Los 12 pares: la caída de entropía NO distingue en 12/12; la FORMA sí en 7/12. Los 4 visuales dan 4/4 | conectoma ★ |
| `5797` | ERRATUM v1 → v2, texto formal para Zenodo | erratum |
| `5817` | El Script R acierta el diseño y falla la ejecución | conectoma |
| `5837` | Las 5 normalizaciones: **la asimetría R se invierte en visual (1,878 → 0,811)** y λ_F no es τ | conectoma ★ |
| `5857` | Encontré TU corrida del Script R: reproduce a 4-5 cifras. La discrepancia está en el veredicto, no en los datos | conectoma |
| `5877` | Índice auditado de los 7 documentos del corpus. **El TSV mutó** y la normalización «biológica» destruye la heterogeneidad (CV 2,402 → 0) | corpus ★ |
| `5897` | Qué se publica, en criollo: no hay frugalidad uniforme, hay **jerarquía de ruteo** | conectoma ★ |
| `5917` | El 96% del cerebro de la mosca NO aprende (4,045% de neuronas, 0,41% de conexiones). DualBrain terminó, gate 4/4 | conectoma + motor ★ |
| `5997` | ERRATUM v2 · 7 puntos. **Mi RDI no reproduce tu Tabla 7 a t=60 (factor 2,9)** | erratum ★ |
| `6037` | Cerradas las dos deudas del E7: **la Tabla 7 no es reproducible con el código archivado** | conectoma ★ |
| `6097` | Auditoría de la jornada: 11/11 coherencia. El barrido de h_m mejora el paper 3,44× (4,05× → **1,18×** vs LSTM) | conectoma + motor ★ |
| `6297` | Barrí las dos cuentas de Kaggle: el brazo W terminó completo y sin leer | motor ★ |
| `6357` | Motor complejo vs SparseLTC: son padre e hijo, y el cara a cara ya corre dentro de `motor.py` (p=0,6000) | motor |

**IDs de esta zona sin identificar:** `5617`, `5637`, `5937`, `5957`, `5977`, `6017`, `6057`, `6077`, `6117`, `6137`, `6157`, `6177`, `6197`, `6217`, `6237`, `6257`, `6277`, `6317`, `6337`. **19 pendientes.**

---

## D · 16-ago · MUDH-MOBILE (confirmado por enumeración, fuera de la línea del conectoma)

| ID | Título |
|---|---|
| `3537` | MUDH — Hot-Update de agentes vía proot (firma Ed25519, anti-rollback) |
| `3577` | OPERIT: clean-room vs IPC, decisión final. **"OPERIT es el profesor, no el socio"** |
| `3597` | PAQUETE MAESTRO único para OpenCode (vectores A/B + hot-update) |
| `3617` | MUDH-Mobile — Auditoría + completamiento D1-D7 para Tachi |

`3557` **no devolvió nada y NO se distinguió** si no existe o si quedó omitido por límite de tamaño. Los tres estados.

---

## NO MEDIDO, declarado

- **27 de ~65 IDs del rango 5057-6357 identificados. 19 pendientes en la zona del conectoma, ~15 en la de icca-engine.**
- **No barrido:** la zona MUDH/AURA de 14-ago (`1057-1097` y alrededores), ni nada por debajo de `3537`, ni por encima de `6357`.
- **No conozco los límites del espacio.** No sé dónde arranca ni dónde termina.
- **El paso 20 está confirmado en tres zonas, no en todo el espacio.** Puede haber huecos o cambios de paso.
- **De los 21 de la sección C, la mayoría está identificada por TÍTULO**, no por lectura completa en esta pasada. Sus números vienen del índice viejo y de búsquedas, no de haberlos abierto hoy.
- **No encontré el Doc del primer análisis del paper publicado.** Está entre `3617` (16-ago) y `5057` (21-ago), o sea en un hueco de **72 IDs sin barrer**. Es lo que Abraham pidió ubicar y **sigue sin ubicar**.
- **No verifiqué si el prefijo `2kza6fw5-` cubre todos los Docs** o si hay otro espacio de nombres.

---

## Próxima pasada

1. **El hueco `3637-5037`** (72 IDs): ahí está el primer análisis del paper publicado, que es lo que se pidió ubicar.
2. Los **19 pendientes** de la zona del conectoma.
3. Los ~15 de icca-engine, con menos prioridad: es otra línea.

```
--- METODO TITAN ---
Accion delicada: NO. Lectura de 9 Docs por ID construido, un archivo nuevo en
                 git. Ninguna corrida, cero cuota ajena.
Modo aplicado:   TITAN FULL
Rubrica:         no se emite: el barrido esta al 40% y puntuar un indice
                 parcial como completo es el septimo patron del Bloque 8.
N/A declarados:  pendiente
Review externo:  el metodo mismo es el falsador del indice anterior: encontro
                 el 5177 que la cosecha del chat no podia ver, y refuto mi
                 propia afirmacion de la resp 031 de que eran TRES proyectos.
                 Son cuatro (cinco contando el arranque del 21-ago).
Instrumento:     load_assets con IDs construidos por mi, no provistos.
                 Confirmados en esta pasada: 5057, 5097, 5137, 5177, 5217,
                 5297, 3537, 3577, 3597, 3617.
                 Sin respuesta: 3557 (no distinguido: inexistente vs omitido).
                 NO MEDIDO: la seccion homonima.
```
