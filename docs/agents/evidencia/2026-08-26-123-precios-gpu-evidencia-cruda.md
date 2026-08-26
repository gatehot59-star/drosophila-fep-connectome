# Evidencia cruda · precios de GPU medidos en vivo

**Instrumento:** gateway MUDH servicio `build` (`run` en `brain-env`), `python3` + `requests` · 2026-08-26 · 4 corridas, exit=0.

**Fuentes primarias:** archivos reales del repo `github/docs`, la página pública `github.com/pricing`, la **API pública de Vast.ai** y la página de precios de RunPod. No búsqueda web para las cifras.

Salida **verbatim**. Veredicto derivado en `docs/agents/respuestas/2026-08-26-123-cuanto-cuesta-la-gpu-en-actions-y-por-que-no-la-pagaria.md`.

---

## 1. Tarifa oficial de runners GPU, verbatim

`github/docs` → `content/billing/reference/actions-runner-pricing.md` (HTTP 200, 4.858 B):

```plain
## GPU-powered hosted runners

| Operating system   | Billing SKU          | Per-minute rate (USD) |
| ------------------ | ---------------------| ----------------------|
| Linux 4-core       | linux_4_core_gpu     | $0.052                |
| Windows 4-core     | windows_4_core_gpu   | $0.102                |
```

### Y los tres renglones que cambian todo, del mismo archivo

```plain
* Included minutes cannot be used for hosted runners.
* The hosted runners are not free for public repositories.
* Larger runners are only billed at the per-minute rate for the amount of time
  workflows are executed on them. There is no cost associated with creating a
  hosted runner that is not being used by a workflow.
```

**"The hosted runners are not free for public repositories."** La ventaja del repo público **desaparece** en cuanto se pide GPU. Y **los minutos incluidos no se pueden usar**: la GPU es 100% pago por uso.

---

## 2. Qué GPU es exactamente, verbatim

`github/docs` → `content/actions/reference/runners/larger-runners.md` (HTTP 200, 9.503 B):

```plain
### Specifications for GPU hosted runners

| CPU | GPU | GPU card | Memory (RAM) | GPU memory (VRAM) | Storage (SSD) | Operating system (OS) |
| --- | --- | -------- | ------------ | ----------------- | ------------- | --------------------- |
| 4   | 1   | Tesla T4 | 28 GB        | 16 GB             | 176 GB        | Ubuntu, Windows       |
```

**Una Tesla T4 con 16 GB de VRAM.** Es la **misma clase de GPU que Kaggle da gratis.**

---

## 3. El requisito de plan, verbatim

`github/docs` → `data/reusables/actions/larger-runner-permissions.md` (HTTP 200):

```plain
Larger runners are only available for organizations and enterprises using the
Team or GitHub Enterprise Cloud plans.
```

**Dos condiciones, no una:** plan **Team o superior**, y ser una **organización o enterprise**.

### El detalle que lo complica, medido

De la integración de GitHub, en la respuesta 121:

```plain
"owner": { "login": "gatehot59-star", "type": "User" }
```

**Los 4 repos cuelgan de una cuenta PERSONAL, no de una organización.** Así que Team en una cuenta personal no alcanza: hay que **crear una organización y mover los repos**.

---

## 4. Precio del plan, de la página pública

`github.com/pricing` (HTTP 200, 704.265 B), texto extraído verbatim:

```plain
Free        The basics for individuals and organizations              $ 0
Team        Advanced collaboration for individuals and organizations  $ 4
Enterprise  Security, compliance, and flexible deployment   Starting at $ 21

contexto Team: "...Most popular Team Advanced collaboration for individuals and
organizations $ 4 USD per user/month $ 4 USD per user/month for the first 12
months * Continue with Team Everything included in Free, plus... Access to
GitHub Codespaces..."
```

**Team = 4 USD por usuario por mes.** El asterisco de "for the first 12 months" queda como **NO MEDIDO**: no leí la nota al pie.

---

## 5. Escala completa de larger runners sin GPU, verbatim

```plain
## x64-powered hosted runners
| Linux Advanced 2-core | linux_2_core_advanced | $0.006 |
| Linux 4-core          | linux_4_core          | $0.012 |
| Linux 8-core          | linux_8_core          | $0.022 |
| Linux 16-core         | linux_16_core         | $0.042 |
| Linux 32-core         | linux_32_core         | $0.082 |
| Linux 64-core         | linux_64_core         | $0.162 |
| Linux 96-core         | linux_96_core         | $0.252 |
| macOS 12-core         | macos_l               | $0.077 |

## arm64-powered hosted runners
| Linux 2-core  | linux_2_core_arm  | $0.005 |
| Linux 4-core  | linux_4_core_arm  | $0.008 |
| Linux 8-core  | linux_8_core_arm  | $0.014 |
| Linux 16-core | linux_16_core_arm | $0.026 |
| Linux 32-core | linux_32_core_arm | $0.050 |
| Linux 64-core | linux_64_core_arm | $0.098 |
| macOS 5-core (M2 Pro) | macos_xl  | $0.102 |

## Tarifas de runners ESTANDAR (del reusable de billing)
| Linux 1-core (x64)  | actions_linux_slim   | $0.002 |
| Linux 2-core (x64)  | actions_linux        | $0.006 |
| Linux 2-core (arm64)| actions_linux_arm    | $0.005 |
| Windows 2-core (x64)| actions_windows      | $0.010 |
| macOS 3/4-core      | actions_macos        | $0.062 |
```

**Especificaciones de larger runners generales, verbatim:**

```plain
| CPU | Memory (RAM) | Storage (SSD) | Architecture | OS |
| 2   | 8 GB    | 75 GB   | x64, arm64 | Ubuntu |
| 4   | 16 GB   | 150 GB  | x64, arm64 | Ubuntu, Windows |
| 8   | 32 GB   | 300 GB  | x64, arm64 | Ubuntu, Windows |
| 16  | 64 GB   | 600 GB  | x64, arm64 | Ubuntu, Windows |
| 32  | 128 GB  | 1200 GB | x64, arm64 | Ubuntu, Windows |
| 64  | 256 GB  | 2040 GB | x64        | Ubuntu, Windows |
| 96  | 384 GB  | 2040 GB | x64        | Ubuntu, Windows |
| 5   | 14 GB   | 14 GB   | arm64 (M2) | macOS |
| 12  | 30 GB   | 14 GB   | x64 Intel  | macOS |
```

---

## 6. Precios de GPU EN VIVO por API de Vast.ai (sin credencial)

```plain
=== Vast.ai: precios publicos por API (sin key) ===
HTTP 200 14709
  RTX 4090  1x  $0.336/hr  24564MB
  RTX 4090  1x  $0.343/hr  24564MB
  RTX 4090  1x  $0.347/hr  24564MB
  RTX 4090  1x  $0.348/hr  24564MB
  RTX 4090  1x  $0.353/hr  24564MB
```

**Consulta usada:** `verified=true`, `rentable=true`, `gpu_name="RTX 4090"`, orden por `dph_total` ascendente. O sea: **ofertas verificadas y efectivamente alquilables**, no el piso teórico del marketplace.

---

## 7. Precios de RunPod, de su página de precios

```plain
HTTP 200 281002
  * H100 80GB from $1.99
  * RTX 4090 from $0.34
  * H100 NVL   Community Cloud $2.59
  * H100 PCIe  Community Cloud $1.99
  * H100 SXM   Community Cloud $2.69
  * A100 PCIe  Community Cloud $1.19
  * A100 SXM   Community Cloud $1.39
  * L40S       Community Cloud $0.79
  * A40        Community Cloud $0.35
  * L40        Community Cloud $0.69
  * L4         Community Cloud $0.44
  * RTX 4090   Community Cloud $0.34
```

---

## 8. Aritmética derivada (cálculo propio, no medición)

```plain
Actions GPU Linux:  $0.052/min x 60 = $3.12 / hora
Actions GPU Windows:$0.102/min x 60 = $6.12 / hora

Vast.ai RTX 4090 verificada:  $0.336 / hora
RunPod RTX 4090:              $0.34  / hora
RunPod A40:                   $0.35  / hora
Kaggle T4/P100:               $0.00  (cuota medida: 27,9 h + 29,3 h)

Ratio Actions T4 vs Vast 4090:  3.12 / 0.336 = 9,29x MAS CARO
  ...y la 4090 tiene 24 GB de VRAM contra los 16 GB de la T4.

Costo de repetir los 39 nulls (4 shards x ~7 min = ~28 min de GPU):
  Actions GPU:  28 min x $0.052 = $1,46  + $4/mes de Team
  Vast.ai 4090: 0,47 h x $0,336 = $0,16
  Kaggle:                         $0,00   <- es lo que ya usamos

Costo de 30 horas de GPU en un mes:
  Actions GPU:  1800 min x $0.052 = $93,60  + $4 = $97,60
  Vast.ai 4090: 30 h x $0,336     = $10,08
  Kaggle:                           $0,00
```

---

--- METODO TITAN ---
Accion delicada: NO (4 corridas de lectura + 1 escritura de documentacion)
Modo aplicado:   TITAN FULL
Rubrica:         43/45 -> 96/100
N/A declarados:  55 pts (Ejecutabilidad, Seguridad, Testing, DevOps: es
                 evidencia de peritaje de precios, no codigo)
Review externo:  no pedido (no hay PR: es evidencia)
Instrumento:     gateway MUDH servicio build, 4 corridas python3 (exit=0).
                 Fuentes: github/docs raw, github.com/pricing, API publica de
                 Vast.ai (HTTP 200, 14.709 B) y runpod.io/pricing (HTTP 200).
                 Toda la aritmetica marcada como derivada, no medida.
