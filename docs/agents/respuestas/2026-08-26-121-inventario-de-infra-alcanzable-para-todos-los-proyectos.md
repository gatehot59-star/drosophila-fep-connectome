# 121 · El servidor gratis ya lo tenemos, está sin usar, y el free tier de VPS se derrumbó este año

**Fecha:** 2026-08-26 · rama `titan/twohop-nulls` · **TITAN FULL**

**Evidencia cruda:** `docs/agents/evidencia/2026-08-26-121-infra-alcanzable-evidencia-cruda.md`

**Herramientas declaradas antes de ejecutar (C-03):** búsqueda web, búsqueda de repos en GitHub, `run` del servicio `build` del gateway (1 corrida de 55 sondas), integración de GitHub (4 lecturas + 2 escrituras).

**Alcance pedido:** herramientas para **todos** los proyectos, no solo ARC, incluyendo servidor y VPS.

---

## 1. EL HALLAZGO: el servidor ya existe, es gratis e ilimitado, y tiene CERO uso

Medido en vivo, y es la respuesta a "hasta un servidor":

```plain
drosophila-fep-connectome   PUBLIC    <- Actions GRATIS e ILIMITADO
  .github/workflows @ main  -> NO EXISTE (cero workflows)

mudh-mobile                 private   <- consume la cuota de 2.000 min/mes
  .github/workflows @ main  -> 7 workflows, 66.652 B
```

**Regla oficial verificada hoy:** Actions con runners estándar es **gratis en repos públicos** y en self-hosted; los **privados** consumen la cuota mensual del plan (2.000 min en Free).

> **El repo público, que tiene cómputo ilimitado, no corre nada. El repo privado, que gasta cuota, corre 7 workflows.** Está exactamente al revés.

### Qué significa en números

Un runner estándar de Linux es **2 vCPU / 16 GB RAM**, con límite de **6 horas por job** y **20 jobs concurrentes** en plan Free.

<p></p>

Comparado con lo que veníamos usando:

| recurso | lo que teníamos | lo que hay sin usar |
|---|---|---|
| `brain-env` | 2 CPU, 8 GB, **sin GPU**, 1 sola máquina | — |
| Kaggle GPU | **4 slots** concurrentes con 2 cuentas | — |
| **Actions en el repo público** | **0 uso** | **20 jobs × 2 vCPU = 40 vCPU concurrentes, sin costo** |

La corrida CPU del conectoma tardó **390,5 minutos** en `brain-env`. Shardeada en 20 jobs de Actions eso son **~20 minutos de reloj**, gratis, sin tocar Kaggle y sin gastar los slots de GPU.

<p></p>

**Y el `guards.yml` existe pero solo en la rama de trabajo, no en `main`.** O sea que el único CI del repo científico no protege la rama de la que otros clonan.

---

## 2. El free tier de VPS: la mala noticia, medida

Acá la memoria de modelo está vieja y había que verificar. Verificado hoy:

| proveedor | estado real 2026 |
|---|---|
| **Oracle Always Free** | **se recortó a la mitad el 2026-06-15**, sin anuncio: de 4 OCPU / 24 GB a **2 OCPU / 12 GB** ARM. De 3.000 a 1.500 OCPU-horas/mes |
| **Fly.io** | **ya no tiene free tier** desde 2024. Trial de **2 horas de VM o 7 días** |
| **Railway** | Free = **1 USD de crédito/mes**, tope 1 vCPU / 0,5 GB. Un servicio 24/7 de 1 vCPU cuesta ~30 USD/mes al rate publicado |
| Render / Koyeb / Vercel / Netlify | alcanzables (401/403), free tier de web, no de cómputo pesado |

**Veredicto sobre VPS:** el único "servidor siempre encendido y gratis" que sigue en pie es **Oracle ARM 2 OCPU / 12 GB**, y quedó a la mitad. **Y no lo necesitás para cómputo:** Actions en público da más CPU. Oracle sirve para lo que Actions **no** puede: un proceso **persistente** (la Puerta de Cómputo de icca-engine, el gateway, un endpoint 24/7).

<p></p>

**La distinción que ordena todo:** Actions = **cómputo por lotes gratis e ilimitado**. VPS = **presencia permanente**. No compiten; son dos necesidades distintas y hoy no tenés ninguna de las dos montada.

---

## 3. El segundo hallazgo: el erratum se puede depositar por API

```plain
403  https://zenodo.org/api/deposit/depositions
```

**403 con token ausente = el endpoint de depósito existe y es alcanzable desde `brain-env`.**

<p></p>

Esto cambia el ítem #1 de la prioridad de la 118. "Depositar el erratum en Zenodo" no era un trámite tuyo de una tarde: es **una llamada de API**, y lo único que falta es un **token personal de Zenodo** con scope `deposit:write`.

<p></p>

Mismo caso, mismos códigos, para las otras vías de publicación: **OSF 200**, **figshare 200**, **Crossref 200**, **arXiv 200**, **bioRxiv 200**, **Overleaf 200**.

---

## 4. Inventario por proyecto, todo medido

### Conectoma / papers
- **`codex.flywire.ai/api/download` → 200.** La fuente de datos baja directo, sin navegador.
- **`neuprint.janelia.org/api` → 401.** Alcanzable, pide token gratuito de Janelia.
- **`v2.virtualflybrain.org` → 200.**
- **Zenodo deposit → 403** (necesita token) · **OSF, figshare, Crossref, arXiv, bioRxiv → 200.**
- **Actions en público** para correr los nulls a 20 jobs.

### Motor embebido / DualBrain / ESP32
- **`dl.espressif.com/dl/esp-idf/` → 200.** El ESP-IDF completo es descargable.
- El toolchain **`xtensa-esp32-elf-gcc` ya está instalado** en `brain-env` (medido en la 119).
- **QEMU en GitLab → 200**, así que el emulador se puede construir.
- **Falta un compilador de host** (`gcc`): sin él no hay tests nativos del C99 antes de cruzar a target. **Pero en Actions viene de fábrica**, así que el CI del `dualbrain` no depende de instalar nada acá.
- `dualbrain` es **privado**: si su CI se vuelve serio, conviene decidir si va a público o si consume cuota.

### icca-engine.com
- **Cloudflare API → 400/403** (alcanzable, pide token). Workers y Tunnel operables por API.
- **`cloudflared` descargable → 200.**
- El repo es **público** y **`has_pages: false`**: **GitHub Pages es hosting gratis y no está activado**, y el sitio es de dos caras y **cero JS**, o sea el caso ideal para estático.
- La **Puerta de Cómputo** sí necesita proceso vivo: ahí entra Oracle ARM o Daytona, **no** Pages.
- Recordatorio del contexto: la Puerta **no** va en la cuenta Cloudflare del dominio, por suspensión cruzada.

### MUDH-Mobile / AURA / infraestructura
- **Daytona `/api/health` → 200** · **E2B → 200** · **Gitpod → 200**: tres proveedores de sandbox efectivamente vivos.
- **Docker auth → 200**, **ghcr.io → 401**: se pueden publicar imágenes.
- **Sentry 401 · Grafana 401**: observabilidad disponible con cuenta.
- `mudh-mobile` privado con 7 workflows y **62 issues abiertos** es el que se come la cuota.

### Cómputo de IA con GPU (para lo que Actions no da)
- **Modal → 200 · Lightning → 200 · RunPod → 400 · Vast.ai → 403 · Replicate → 401 · Paperspace → 401.** Todos alcanzables, todos piden cuenta.
- **Ninguno es gratis para GPU sostenida.** La GPU gratis sigue siendo **Kaggle**, con sus 4 slots.

---

## 5. Lo que puedo hacer HOY sin pedirte nada

1. **Escribir los workflows de Actions** para el repo público y shardedár los nulls a 20 jobs.
2. **Bajar datos de FlyWire** por `codex.flywire.ai/api/download`.
3. **Instalar cualquier paquete de Python** (medido en la 120).
4. **Clonar y leer cualquier repo** con `dulwich` o zip de codeload.
5. **Bajar el ESP-IDF** y armar el pipeline de build embebido.

## 6. Lo que necesita una credencial tuya, en orden de impacto

| # | qué | desbloquea |
|---|---|---|
| 1 | **token de Zenodo** (`deposit:write`) | **el erratum, que es la prioridad #1 de la 118** |
| 2 | **API key de ARC** (gratis) | iterar el agente contra entornos reales |
| 3 | token de neuPrint (gratis, Janelia) | datos del conectoma por API |
| 4 | cuenta Oracle Cloud | **el único VPS gratis que queda**, para procesos 24/7 |
| 5 | token de Cloudflare | Workers y Tunnel para icca-engine |

---

## 7. Una vía que NO ejecuto, y digo por qué

`cloudflared` es descargable (200) y `brain-env` tiene red saliente. Técnicamente **puedo convertir el container en un servidor accesible desde internet** con un túnel.

<p></p>

**No lo hago sin tu OK.** El Bloque 2.3 lista como acción delicada "cualquier vía que exponga un runtime a la red", y `brain-env` es una máquina de la que **Tachi también depende**. Es capacidad presente y permiso ausente: son cosas distintas y las digo separadas.

---

## 8. Prioridad, con la dependencia verificada (O-01)

**Criterio declarado:** qué desbloquea más por unidad de esfuerzo tuyo.

<p></p>

1. **Token de Zenodo.** Convierte la prioridad #1 en una llamada de API en vez de una tarde tuya.
2. **Mover el CI al repo público.** Es cómputo gratis que hoy no se usa, y no depende de nada más. **Verificado, no supuesto:** el repo ya es público y `main` no tiene workflows, así que no hay que esperar a nadie.
3. **API key de ARC** (en paralelo, no depende de 1 ni de 2).
4. **Cuenta Oracle** solo cuando haya un proceso que de verdad tenga que estar 24/7. Hoy no lo hay: es el error de armar infraestructura antes del producto.

**Lo que NO haria:** montar un VPS pago ahora. Con Actions gratis e ilimitado en público, pagar cómputo por lotes es tirar plata.

---

## 9. NO MEDIDO, y dos errores propios de sonda

- **Error propio 1:** escribí `api.denn.com` en vez de `api.deno.com`. **Ese `ERR` no mide nada sobre Deno Deploy.** NO MEDIDO.
- **Error propio 2:** usé `api-inference.huggingface.co`, que es el endpoint viejo (HF movió a `router.huggingface.co`). Su `ERR` mide mi URL, no el servicio. NO MEDIDO.
- **No medi la cuota de minutos de Actions consumida** por `mudh-mobile`. El endpoint de billing necesita un scope que la integración no expone. Así que "se come la cuota" es **inferencia** de tener 7 workflows en privado, no una medición del contador.
- **No corrí un workflow de prueba en el repo público.** Los 20 jobs concurrentes y los 6 h por job son de la documentación oficial, **no medidos en esta cuenta**.
- **No probé ninguna credencial**: todos los `401`/`403` prueban alcance, no que la cuenta funcione.
- **`Fly.io` 404, `Tailscale` 404, `Wokwi` 404, `bossDB` 404, `Wandb` 405** son rutas o métodos equivocados **de mi sonda**, no ausencia de servicio.
- **Beam Cloud dio 502**: problema del lado de ellos, no medición de su free tier.
- **No verifiqué si `icca-engine` puede servirse por Pages tal cual** (depende de si el build es estático puro, y no leí su árbol en este turno).

---

--- METODO TITAN ---
Accion delicada: NO (lecturas + 2 escrituras de documentacion en rama de trabajo)
Modo aplicado:   TITAN FULL
Rubrica:         42/45 -> 93/100
                 Completitud 13/15 (-2: no corri un workflow de prueba, asi que
                 los 20 jobs concurrentes quedan de doc oficial y no medidos)
                 Arquitectura del razonamiento 10/10 (la distincion lotes vs
                 presencia permanente separa Actions de VPS y ordena el resto)
                 Documentacion 10/10 · Innovacion 5/5 (el hallazgo del CI
                 invertido no fue pedido) · Proceso QA 4/5 (-1: la afirmacion
                 sobre consumo de cuota es inferencia declarada, no medicion)
N/A declarados:  55 pts (Ejecutabilidad, Seguridad, Testing, DevOps: es un
                 peritaje de infraestructura, no codigo de produccion)
Review externo:  no pedido (no hay PR: son dos archivos de documentacion)
Instrumento:     gateway MUDH servicio build, 1 corrida python3 con 55 GET,
                 exit=0 · integracion GitHub, 4 lecturas. Salida cruda
                 verbatim commiteada aparte, con mis dos errores incluidos (W-01).
