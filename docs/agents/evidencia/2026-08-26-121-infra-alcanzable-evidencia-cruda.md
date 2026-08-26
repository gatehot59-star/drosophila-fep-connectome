# Evidencia cruda · 55 servicios de infraestructura sondeados desde `brain-env` + estado de los 4 repos

**Instrumento:** gateway MUDH servicio `build` (`run` en el container `brain-env`), `python3` 3.12.14 + `requests`, 20 hilos, timeout 15 s · 2026-08-26 · exit=0

**Segundo instrumento:** integración de GitHub (search de repos y listado de contenidos), misma fecha.

Salida **verbatim**. El veredicto derivado está en `docs/agents/respuestas/2026-08-26-121-inventario-de-infra-alcanzable-para-todos-los-proyectos.md`.

---

## Sonda · 55 endpoints de infraestructura, ciencia y datos

```plain
  401  Oracle Cloud API             137  https://iaas.us-ashburn-1.oraclecloud.com/20160918/instances
  400  Cloudflare API               115  https://api.cloudflare.com/client/v4/user/tokens/verify
  403  Cloudflare Workers upload    162  https://api.cloudflare.com/client/v4/accounts
  404  Fly.io API                   19  https://api.machines.dev/v1/apps
  400  Railway GraphQL              86  https://backboard.railway.com/graphql/v2
  401  Render API                   26  https://api.render.com/v1/services
  401  Koyeb API                    90  https://app.koyeb.com/v1/apps
  403  Vercel API                   109  https://api.vercel.com/v2/user
  401  Netlify API                  38  https://api.netlify.com/api/v1/sites
  ERR  Deno Deploy                  ConnectionError  https://api.denn.com/v1/organizations
  401  Supabase API                 26  https://api.supabase.com/v1/projects
  401  Neon Postgres                123  https://console.neon.tech/api/v2/projects
  401  Turso                        56  https://api.turso.tech/v1/organizations
  401  Upstash Redis                0  https://api.upstash.com/v2/redis/databases
  401  GitHub Actions runners API   120  https://api.github.com/repos/gatehot59-star/drosophila-fep-con
  401  GitHub Codespaces API        168  https://api.github.com/user/codespaces
  404  GitHub Pages                 126  https://api.github.com/repos/gatehot59-star/drosophila-fep-con
  403  Zenodo deposit API           48  https://zenodo.org/api/deposit/depositions
  200  OSF API                      5363  https://api.osf.io/v2/nodes/?page[size]=1
  200  figshare API                 935  https://api.figshare.com/v2/articles?page_size=1
  200  Daytona API                  15  https://app.daytona.io/api/health
  200  Gitpod API                   0  https://api.gitpod.io/gitpod.v1.WorkspaceService/ListWorkspace
  200  E2B sandbox API              23  https://api.e2b.dev/health
  401  Replicate API                93  https://api.replicate.com/v1/models
  200  Modal API                    0  https://api.modal.com/
  200  Lightning AI API             17483  https://lightning.ai/api/v1/health
  401  Paperspace API               80  https://api.paperspace.com/v1/machines
  400  RunPod API                   406  https://api.runpod.io/graphql
  403  Vast.ai API                  74  https://console.vast.ai/api/v0/instances/
  502  Beam Cloud                   960  https://api.beam.cloud/v1/health
  403  Ngrok API                    298  https://api.ngrok.com/tunnels
  404  Tailscale API                32  https://api.tailscale.com/api/v2/tunnel
  200  Cloudflare Tunnel dl         214432  https://github.com/cloudflare/cloudflared/releases/latest
  200  Docker registry auth         5069  https://auth.docker.io/token?service=registry.docker.io
  401  ghcr.io                      73  https://ghcr.io/v2/
  200  Espressif dl (esp-idf)       12184  https://dl.espressif.com/dl/esp-idf/
  404  Wokwi ESP32 sim              62993  https://wokwi.com/api/health
  200  QEMU git                     56819  https://gitlab.com/qemu-project/qemu
  401  Sentry API                   58  https://sentry.io/api/0/organizations/
  401  Grafana Cloud                114  https://grafana.com/api/orgs
  200  Overleaf                     57791  https://www.overleaf.com/
  200  arXiv submit                 10993  https://arxiv.org/submit
  200  bioRxiv API                  67  https://api.biorxiv.org/details/biorxiv/10.1101/2020.01.01.000
  429  Semantic Scholar API         174  https://api.semanticscholar.org/graph/v1/paper/search?query=co
  200  Crossref API                 2472  https://api.crossref.org/works?rows=1
  405  Wandb API                    0  https://api.wandb.ai/graphql
  200  MLflow pypi                  337458  https://pypi.org/pypi/mlflow/json
  200  Ollama dl                    15902  https://ollama.com/install.sh
  ERR  HF inference                 ConnectionError  https://api-inference.huggingface.co/models/gpt2
  403  Google AI Studio             248  https://generativelanguage.googleapis.com/v1beta/models
  401  neuPrint API                 45  https://neuprint.janelia.org/api/dbmeta/datasets
  200  FlyWire codex API            25516  https://codex.flywire.ai/api/download
  404  MICrONS bossDB               77  https://api.bossdb.io/v1/collections
  200  virtualflybrain              2029  https://v2.virtualflybrain.org/
```

### Dos errores propios en esta sonda, declarados

1. **`Deno Deploy` → `ERR ConnectionError`: es un typo mío.** Escribí `api.denn.com` en vez de `api.deno.com`. **Ese renglon no mide nada sobre Deno.** Queda NO MEDIDO.
2. **`HF inference` → `ERR ConnectionError`:** `api-inference.huggingface.co` es el endpoint viejo. HuggingFace movió la inferencia a `router.huggingface.co`. **No mido ausencia de inferencia**, mido que usé la URL vieja. NO MEDIDO.

### Nota de lectura de los códigos

- `401` / `403` = **alcanzable y pide credencial**. Es un resultado útil, no un bloqueo.
- `400` en la raíz de una API = el servicio contestó.
- `404` / `405` = ruta o método equivocados **de mi sonda**, no ausencia del servicio (caso `Fly.io`, `Tailscale`, `Wokwi`, `bossDB`, `Wandb`).
- `429` en Semantic Scholar = rate limit, o sea que **contestó**.
- `502` en Beam = el servicio está con problemas del lado de ellos.

---

## Estado real de los 4 repos (integración de GitHub)

```plain
mudh-mobile                 private   Kotlin   62 issues abiertos   size 1529
drosophila-fep-connectome   PUBLIC    Python    5 issues abiertos   size 1303
dualbrain                   private   C         0 issues abiertos   size  119
icca-engine                 PUBLIC    -         6 issues abiertos   size  188
```

**Workflows por repo, leídos en vivo:**

```plain
mudh-mobile @ main .github/workflows:
  campo-device.yml   26684 B
  campo.yml          13609 B
  kernel-ci.yml       5426 B
  proot-release.yml   7970 B
  security.yml        4395 B
  smoke.yml           3640 B
  test.yml            5318 B
  -> 7 workflows, 66.652 B totales, en repo PRIVADO

drosophila-fep-connectome @ main .github/workflows:
  -> ERROR: "The path does not point to a file or directory, or the file
     does not exist in the repository."
  -> CERO workflows en main, en repo PUBLICO

drosophila-fep-connectome @ titan/twohop-nulls .github:
  workflows (dir)
drosophila-fep-connectome @ titan/twohop-nulls .github/workflows:
  guards.yml          5318 B
  -> 1 workflow, solo en la rama de trabajo

icca-engine:  has_pages: false
drosophila-fep-connectome:  has_pages: false  (GET /pages -> 404)
```

---

## Verificado en vivo contra fuentes oficiales (V-01)

```plain
VERIFICADO EN VIVO 2026-08-26: Actions es GRATIS e ilimitado con runners
  estandar en repositorios PUBLICOS, y gratis en self-hosted. Los repos
  PRIVADOS consumen una cuota mensual (2.000 min en plan Free).
  Fuente: https://docs.github.com/en/billing/concepts/product-billing/github-actions

VERIFICADO EN VIVO 2026-08-26: Oracle Always Free bajo Ampere A1 de
  4 OCPU / 24 GB a 2 OCPU / 12 GB, con efecto 2026-06-15, SIN anuncio
  publico. De 3.000 a 1.500 OCPU-horas por mes.
  Fuente: https://www.infoq.com/news/2026/07/oracle-cloud-free-tier-limits/
          https://docs.oracle.com/en-us/iaas/Content/FreeTier/freetier_topic-Always_Free_Resources.htm

VERIFICADO EN VIVO 2026-08-26: Fly.io NO tiene free tier desde 2024. El
  trial es 2 horas de VM o 7 dias, lo que termine primero.
  Fuente: https://fly.io/docs/about/free-trial/

VERIFICADO EN VIVO 2026-08-26: Railway plan Free = 0 USD/mes con 1 USD de
  credito mensual, tope 1 vCPU / 0,5 GB por servicio, 1 replica.
  Fuente: https://railway.com/pricing
```

---

--- METODO TITAN ---
Accion delicada: NO (55 GET de lectura + lecturas de la integracion de GitHub)
Modo aplicado:   TITAN FULL
Rubrica:         42/45 -> 93/100
N/A declarados:  55 pts (Ejecutabilidad, Seguridad, Testing, DevOps: es
                 evidencia de peritaje, no codigo de produccion)
Review externo:  no pedido (no hay PR: es evidencia)
Instrumento:     gateway MUDH servicio build (1 corrida python3, exit=0) +
                 integracion GitHub (4 lecturas). Salida cruda verbatim
                 arriba, incluidos mis dos errores de sonda.
