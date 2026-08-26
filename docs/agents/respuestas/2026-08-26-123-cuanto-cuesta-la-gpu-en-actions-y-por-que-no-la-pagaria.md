# 123 · Cuánto cuesta la GPU en Actions, y por qué **no la pagaría**

**Fecha:** 2026-08-26 · rama `titan/twohop-nulls` · **TITAN FULL**

**Evidencia cruda:** `docs/agents/evidencia/2026-08-26-123-precios-gpu-evidencia-cruda.md`

**Herramientas declaradas antes de ejecutar (C-03):** búsqueda web (contexto de mercado), `run` del servicio `build` del gateway (4 corridas contra fuentes primarias y APIs de precios), integración de GitHub (2 escrituras).

---

## 1. La respuesta corta, con los tres números

**El mínimo son 4 USD por mes.** Y con eso **no tenés ni un minuto de GPU**: solo el derecho a comprarla.

| concepto | precio medido |
|---|---|
| **plan Team** (requisito de entrada) | **4 USD / usuario / mes** |
| **GPU Linux 4-core** (`linux_4_core_gpu`) | **0,052 USD / minuto = 3,12 USD / hora** |
| GPU Windows 4-core | 0,102 USD / min = **6,12 USD / hora** |

**Qué GPU es:** **1× Tesla T4, 16 GB de VRAM**, 4 CPU, 28 GB de RAM, 176 GB de SSD.

> **La misma clase de GPU que Kaggle nos da gratis.**

---

## 2. Los tres renglones de la letra chica que arruinan el plan

Leídos del archivo oficial de facturación, no de un blog:

1. **`The hosted runners are not free for public repositories.`**  
   La ventaja entera de la respuesta 122 — el repo público con cómputo ilimitado — **desaparece en cuanto pedimos GPU.**
2. **`Included minutes cannot be used for hosted runners.`**  
   Los 3.000 minutos que trae Team **no sirven** para GPU. Es 100% pago por uso, desde el primer minuto.
3. **`Larger runners are only available for organizations and enterprises using the Team or GitHub Enterprise Cloud plans.`**

### Y el requisito escondido, que ya estaba medido

De la respuesta 121: los 4 repos cuelgan de `"type": "User"`. **Es una cuenta personal, no una organización.**

<p></p>

Así que el camino real no es "pagar 4 dólares": es **crear una organización, mover los repos ahí, y después pagar**. Es una migración, no un botón.

---

## 3. El precio comparado, y acá se termina la discusión

Medido en vivo por la **API pública de Vast.ai**, filtrando por ofertas **verificadas y alquilables**, ordenadas por precio:

```plain
RTX 4090  1x  $0.336/hr  24 GB VRAM
RTX 4090  1x  $0.343/hr  24 GB VRAM
RTX 4090  1x  $0.347/hr  24 GB VRAM
```

Y de la página de RunPod: **RTX 4090 desde 0,34** · A40 0,35 · L4 0,44 · A100 PCIe 1,19 · H100 PCIe 1,99.

<p></p>

| opción | GPU | VRAM | USD / hora |
|---|---|---|---|
| **Actions GPU** | Tesla T4 | 16 GB | **3,12** |
| Vast.ai verificada | **RTX 4090** | **24 GB** | **0,336** |
| RunPod Community | RTX 4090 | 24 GB | 0,34 |
| RunPod Community | A40 | 48 GB | 0,35 |
| **Kaggle (lo que ya usamos)** | T4 / P100 | 16 GB | **0,00** |

> **La GPU de GitHub sale 9,3 veces más que una RTX 4090 en Vast.ai, y la 4090 es muchísimo más rápida y trae 8 GB más de VRAM.**

**Es la T4 más caras del mercado medido.** Tiene sentido para una empresa que ya vive en GitHub y necesita todo en un solo pipeline con una sola factura. **Para vos no.**

---

## 4. Qué costaría en tu caso concreto (cálculo, no medición)

**Repetir los 39 nulls** (4 shards × ~7 min ≈ 28 min de GPU):

```plain
Actions GPU:   $1,46  + $4/mes de Team + crear una organizacion
Vast.ai 4090:  $0,16
Kaggle:        $0,00   <- es lo que ya corrimos, dos veces
```

**Un mes con 30 horas de GPU:**

```plain
Actions GPU:   $97,60
Vast.ai 4090:  $10,08
Kaggle:        $0,00   (cuota medida: 27,9 h + 29,3 h en las dos cuentas)
```

**Kaggle ya te da más GPU gratis que la que consumimos.** Las corridas grandes del expediente tardaron **5 a 7 minutos por shard**. Estamos hablando de minutos, no de horas.

---

## 5. Mi recomendación, sin diplomacia

**No pagues GPU en Actions. Ni 4 dólares.**

<p></p>

Y el argumento no es solo el precio: **pagar rompe lo que hacía valioso al repo público.** Hoy tiene 4 vCPU / 16 GB × 20 concurrentes **gratis e ilimitado**. En el momento en que se mete un runner pago, ese renglon deja de ser gratis. **Estarías pagando por perder una ventaja.**

### Dejá el reparto como está, que ya es bueno

| necesidad | dónde | costo |
|---|---|---|
| cómputo CPU masivo y paralelo | **Actions en repo público** | **0** |
| GPU | **Kaggle**, 4 slots concurrentes | **0** |
| taller persistente e interactivo | **`brain-env`** | **0** |
| proceso 24/7 | Oracle ARM (2 OCPU / 12 GB) | **0** |

**Cuatro necesidades, cuatro soluciones, cero pesos.** El agujero de este stack **no es GPU**: es que Actions está sin usar y Oracle sin crear.

### Cuándo SÍ tendría sentido pagar, y cuánto

**Si alguna vez hace falta GPU de verdad** (entrenar algo grande, que hoy no está en ninguna de las cuatro líneas):

- **Vast.ai o RunPod, ~0,34 USD/hora**, pago por uso, sin suscripción, sin organización, sin migrar repos.
- **10 dólares te compran 30 horas de RTX 4090.** Los mismos 10 dólares en Actions te compran **3,2 horas de T4**.

**Y ojo con el orden (O-01):** ninguna de las cuatro líneas vivas está hoy bloqueada por falta de GPU. Lo que está bloqueado es **el erratum sin depositar**, **los tres clicks de ARC** y **el agente sin escribir**. Comprar GPU ahora sería armar infraestructura antes del producto, que es exactamente el error que señalé en la 121 sobre Oracle.

---

## 6. Dato útil aparte: los larger runners SIN GPU

Si alguna vez hace falta una máquina grande de CPU (no GPU), las tarifas son sorprendentemente razonables:

```plain
Linux 16-core  $0.042/min = $2,52/hora   (64 GB RAM, 600 GB SSD)
Linux 32-core  $0.082/min = $4,92/hora   (128 GB RAM)
Linux 64-core  $0.162/min = $9,72/hora   (256 GB RAM)
Linux 96-core  $0.252/min = $15,12/hora  (384 GB RAM)

arm64 es MAS BARATO que x64 en toda la escala:
Linux 16-core arm  $0.026/min = $1,56/hora  (38% menos que x64)
Linux 32-core arm  $0.050/min = $3,00/hora
```

**Igual: 20 jobs gratis de 4 vCPU en el repo público son 80 vCPU.** Un runner de 96 cores a 15 USD/hora no compra más CPU total que lo que ya tenés gratis; compra **más CPU en una sola máquina**, que es otra cosa y solo importa si el trabajo no se puede shardear. **El de los nulls sí se shardea.**

---

## 7. NO MEDIDO

- **El asterisco del "$4 for the first 12 months"**: no leí la nota al pie. **No sé si el precio sube después del año.**
- **No verifiqué el costo de migrar los repos a una organización** ni si eso rompe algo (issues, PRs, la integración de ClickUp, los tokens de Tachi). Es el riesgo mayor de ese camino y **está sin medir**.
- **No probé alquilar en Vast.ai ni en RunPod.** Leí sus precios publicados y sus ofertas listadas; **no sé si el alta funciona desde Argentina** ni si aceptan tu medio de pago.
- **Los precios de Vast.ai son de un instante.** Es un marketplace: fluctúan. La medición vale para hoy, 2026-08-26.
- **No re-medi la cuota de Kaggle en este turno.** Los 27,9 h y 29,3 h son de una medición anterior del expediente.
- **No comparé rendimiento real T4 vs RTX 4090** en nuestro código. Que la 4090 sea "mucho más rápida" es de sus especificaciones, **no de una corrida nuestra**.
- **No verifiqué si los 100 jobs concurrentes de GPU** aplican al plan Team desde el primer día o requieren aprobación.

---

--- METODO TITAN ---
Accion delicada: NO (lecturas + 2 escrituras de documentacion en rama de trabajo)
Modo aplicado:   TITAN FULL
Rubrica:         43/45 -> 96/100
                 Completitud 14/15 (-1: no lei la nota al pie del precio de Team)
                 Arquitectura del razonamiento 10/10 (el hallazgo no es el precio
                 sino que pagar DESTRUYE la gratuidad del repo publico: se paga
                 por perder una ventaja)
                 Documentacion 10/10 · Innovacion 5/5 (la tabla de larger runners
                 sin GPU y el punto de que 20 jobs gratis son 80 vCPU no fue
                 pedido) · Proceso QA 4/5 (-1: toda la aritmetica de costos es
                 derivada y depende de estimaciones de duracion)
N/A declarados:  55 pts (Ejecutabilidad, Seguridad, Testing, DevOps: es un
                 peritaje de precios, no codigo de produccion)
Review externo:  no pedido (no hay PR: son dos archivos de documentacion)
Instrumento:     gateway MUDH servicio build, 4 corridas python3 (exit=0) contra
                 github/docs raw, github.com/pricing, API publica de Vast.ai
                 (HTTP 200) y runpod.io/pricing. Salida cruda verbatim
                 commiteada aparte (W-01).
