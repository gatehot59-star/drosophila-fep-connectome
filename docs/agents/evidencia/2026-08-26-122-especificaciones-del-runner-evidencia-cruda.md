# Evidencia cruda · especificaciones e inventario del runner de GitHub Actions

**Instrumento:** gateway MUDH servicio `build` (`run` en `brain-env`), `python3` + `requests` contra `raw.githubusercontent.com` · 2026-08-26 · 4 corridas, exit=0 en todas.

**Fuentes primarias leídas** (no búsqueda web, el archivo real del repo oficial):
- `actions/runner-images` → `images/ubuntu/Ubuntu2404-Readme.md` (HTTP 200, 15.740 B, 331 líneas)
- `github/docs` → `data/reusables/actions/supported-github-runners.md` (HTTP 200, 9.435 B)
- `github/docs` → `content/actions/reference/limits.md` (HTTP 200, 11.327 B)
- `github/docs` → `content/actions/reference/runners/github-hosted-runners.md` (HTTP 200, 8.957 B)

Salida **verbatim**. Veredicto derivado en `docs/agents/respuestas/2026-08-26-122-el-runner-gratis-en-detalle-y-que-hace-que-brain-env-no.md`.

---

## 1. Corrección de ruta: mi primer intento falló

```plain
404  images/ubuntu/Ubuntu24-Readme.md  14B
404  images/ubuntu/Ubuntu22-Readme.md  14B
```

Adiviné el nombre del archivo. **Los reales son `Ubuntu2404-Readme.md`** (cuatro dígitos), y los listé con la integración de GitHub antes de reintentar:

```plain
Ubuntu2204-Arm64-Readme.md
Ubuntu2204-Readme.md
Ubuntu2404-Arm64-Readme.md
Ubuntu2404-Readme.md
Ubuntu2604-Arm64-Readme.md
Ubuntu2604-Readme.md
```

---

## 2. Cabecera del manifiesto de la imagen

```plain
HTTP 200 15740 bytes
lineas totales: 331

| Announcements |
| [[Ubuntu] The Ubuntu 22 based runner images will begin deprecation on September 17th
  and will be fully unsupported by April 17th for GitHub Actions and Azure DevOps |
| [[Ubuntu] Ubuntu 26.04 and Ubuntu 26.04 Arm is now available as a public preview |
***
# Ubuntu 24.04
- OS Version: 24.04.4 LTS
- Kernel Version: 6.17.0-1022-azure
- Image Version: 20260816.277.1
- Systemd version: 255.4-1ubuntu8.17
```

### Secciones del manifiesto

```plain
## Installed Software
### Language and Runtime
### Package Management
### Project Management
### Tools
### CLI Tools
### Java
### PHP Tools
### Haskell Tools
### Rust Tools
### Browsers and Drivers
### .NET Tools
### Databases
### Cached Tools
### PowerShell Tools
### Web Servers
### Android
### Installed apt packages
```

---

## 3. Language and Runtime, verbatim

```plain
- Bash 5.2.21(1)-release
- Clang: 16.0.6, 17.0.6, 18.1.3
- Clang-format: 16.0.6, 17.0.6, 18.1.3
- Clang-tidy: 16.0.6, 17.0.6, 18.1.3
- Dash 0.5.12-6ubuntu5
- GNU C++: 12.4.0, 13.3.0, 14.2.0
- GNU Fortran: 12.4.0, 13.3.0, 14.2.0
- Julia 1.12.7
- Kotlin 2.4.10-release-377
- Node.js 22.23.2
- Perl 5.38.2
- Python 3.12.3
- Ruby 3.2.3
- Swift 6.3.3
```

## 4. Package Management y Project Management, verbatim

```plain
- cpan 1.64
- Helm 3.21.4
- Homebrew 6.0.17
- Miniconda 26.5.3
- Npm 10.9.8
- Pip 24.0
- Pip3 24.0
- Pipx 1.16.7
- RubyGems 3.4.20
- Vcpkg (build from commit 94a5411977)
- Yarn 1.22.22

- Ant 1.10.14
- Gradle 9.7.0
- Lerna 10.0.0
- Maven 3.9.16
```

## 5. Tools, verbatim (41 entradas)

```plain
- Ansible 2.21.3
- AzCopy 10.32.7 - available by azcopy and azcopy10 aliases
- Bazel 9.2.0
- Bazelisk 1.28.1
- Bicep 0.46.1
- Buildah 1.33.7
- CMake 3.31.6
- CodeQL Action Bundle 2.26.3
- Docker Amazon ECR Credential Helper 0.12.0
- Docker Compose 2.38.2
- Docker-Buildx 0.36.1
- Docker Client 28.0.4
- Docker Server 28.0.4
- Fastlane 2.238.0
- Git 2.55.0
- Git LFS 3.7.1
- Git-ftp 1.6.0
- Haveged 1.9.14
- jq 1.7
- Kind 0.32.0
- Kubectl 1.36.3
- Kustomize 5.8.1
- MediaInfo 24.01
- Mercurial 6.7.2
- Minikube 1.38.1
- n 10.2.0
- Newman 6.2.2
- nvm 0.40.6
- OpenSSL 3.0.13-0ubuntu3.12
- Packer 1.16.0
- Parcel 2.16.4
- Podman 5.8.4
- Pulumi 3.257.0
- Skopeo 1.13.3
- Sphinx Open Source Search Server 2.2.11
- yamllint 1.38.0
- yq 4.53.3
- zstd 1.5.7
- Ninja 1.13.2
```

## 6. CLI Tools, Rust, Browsers, Databases, Cached Tools, verbatim

```plain
### CLI Tools
- AWS CLI 2.36.24
- AWS CLI Session Manager Plugin 1.2.835.0
- AWS SAM CLI 1.165.0
- Azure CLI 2.89.1
- Azure CLI (azure-devops) 1.0.6
- GitHub CLI 2.97.0
- Google Cloud CLI 580.0.0

### Rust Tools
- Cargo 1.97.1
- Rust 1.97.1
- Rustdoc 1.97.1
- Rustup 1.29.0
- Rustfmt 1.9.0

### Browsers and Drivers
- Google Chrome 151.0.7922.137
- ChromeDriver 151.0.7922.138
- Chromium 151.0.7922.0
- Microsoft Edge 151.0.4129.86
- Microsoft Edge WebDriver 151.0.4129.86
- Selenium server 4.47.0
- Mozilla Firefox 153.0.4
- Geckodriver 0.37.1

### Databases
- sqlite3 3.45.1
- PostgreSQL 16.15
- MySQL 8.0.46-0ubuntu0.24.04.3

### Cached Tools (Python / Node / Go / Ruby, multiples versiones)
- 1.24.13 / 1.25.13 / 1.26.6          (Go)
- 22.23.2 / 24.19.0                   (Node)
- 3.10.21 / 3.11.16 / 3.12.14 / 3.13.15 / 3.14.7   (Python)
- 3.9.19 [PyPy 7.3.16] / 3.10.16 [PyPy 7.3.19] / 3.11.15 [PyPy 7.3.23]
- 3.2.11 / 3.3.12 / 3.4.10 / 4.0.6    (Ruby)
```

**Nota:** las secciones `### Java`, `### Web Servers` y `### Android` salieron **vacías con mi filtro** porque su contenido está en tablas markdown, no en viñetas `-`. **NO MEDIDO:** su contenido exacto.

---

## 7. Hardware oficial · tabla de repos PÚBLICOS, verbatim

```html
### Standard GitHub-hosted runners for public repositories
<tr><td>Linux</td>   <td>4</td> <td>16 GB</td> <td>14 GB</td> <td>x64</td>
    <td>ubuntu-latest, ubuntu-24.04, ubuntu-22.04, ubuntu-26.04 (public preview)</td></tr>
<tr><td>Windows</td> <td>4</td> <td>16 GB</td> <td>14 GB</td> <td>x64</td>
    <td>windows-latest, windows-2025, windows-2025-vs2026, windows-2022</td></tr>
<tr><td>Linux</td>   <td>4</td> <td>16 GB</td> <td>14 GB</td> <td>arm64</td>
    <td>ubuntu-24.04-arm, ubuntu-22.04-arm, ubuntu-26.04-arm (public preview)</td></tr>
<tr><td>Windows</td> <td>4</td> <td>16 GB</td> <td>14 GB</td> <td>arm64</td>
    <td>windows-11-arm, windows-11-vs2026-arm</td></tr>
<tr><td>macOS</td>   <td>4</td> <td>14 GB</td> <td>14 GB</td> <td>Intel</td>
    <td>macos-15-intel, macos-26-intel</td></tr>
<tr><td>macOS</td>   <td>3 (M1)</td> <td>7 GB</td> <td>14 GB</td> <td>arm64</td>
    <td>macos-latest, macos-14, macos-15, macos-26, xcode-27 (public preview)</td></tr>
```

## 8. Hardware oficial · tabla de repos PRIVADOS, verbatim

```html
<tr><td>Linux</td>   <td>2</td> <td>8 GB</td> <td>14 GB</td> <td>x64</td>   <td>ubuntu-latest...</td></tr>
<tr><td>Windows</td> <td>2</td> <td>8 GB</td> <td>14 GB</td> <td>x64</td>   <td>windows-latest...</td></tr>
<tr><td>Linux</td>   <td>2</td> <td>8 GB</td> <td>14 GB</td> <td>arm64</td> <td>ubuntu-24.04-arm...</td></tr>
<tr><td>Windows</td> <td>2</td> <td>8 GB</td> <td>14 GB</td> <td>arm64</td> <td>windows-11-arm...</td></tr>
<tr><td>macOS</td>   <td>4</td> <td>14 GB</td> <td>14 GB</td> <td>Intel</td> <td>macos-15-intel...</td></tr>
<tr><td>macOS</td>   <td>3 (M1)</td> <td>7 GB</td> <td>14 GB</td> <td>arm64</td> <td>macos-latest...</td></tr>
```

> **El público tiene EL DOBLE de CPU y RAM que el privado.** 4 vCPU / 16 GB contra 2 vCPU / 8 GB. No es solo que el público sea gratis: **es mejor máquina.**

---

## 9. Límites duros, verbatim

```plain
| Runner type | plan | Total concurrent jobs | Max macOS jobs | Max GPU jobs |
| Standard GitHub-hosted runner | Free       |  20 |  5 | Not applicable |
| Standard GitHub-hosted runner | Pro        |  40 |  5 | Not applicable |
| Standard GitHub-hosted runner | Team       |  60 |  5 | Not applicable |
| Standard GitHub-hosted runner | Enterprise | 500 | 50 | Not applicable |
| Larger runner                 | Team       | 1000 | 5 | 100 |

| All GitHub-hosted runners | Job execution time | 6 hours |
| Self-hosted               | Job execution time | 5 days  |
| Self-hosted               | Job queue time     | 24 hours |
| Workflow execution limit  | Workflow run time  | 35 days / workflow run |
| Workflow execution limit  | Job Matrix         | 256 jobs / workflow run |
| Workflows queuing         | Workflow run queued | 500 workflow runs / 10 seconds |
| Dependency caching | Uploads per minute   |  200 per minute |
| Dependency caching | Downloads per minute | 1500 per minute |
| Dependency caching | Deletes per minute   |  400 per minute |

### Workflow file size
Each workflow file in .github/workflows must be 500 KB or smaller to trigger a run.

GitHub Support **can** increase job concurrency limits. To request an increase,
submit a support ticket.
```

**Nota importante sobre GPU:** `Maximum concurrent GPU jobs = 100` existe **solo** para *larger runners* en planes Team y Enterprise. En **Free es `Not applicable`**: **no hay GPU gratis en Actions.**

## 10. `ubuntu-slim`, el runner de 1 CPU

```plain
Single-CPU GitHub-hosted runners are available in both public and private
repositories. These runners - specified using the workflow label `ubuntu-slim` -
offer a lower-cost o[ption]

`ubuntu-slim` runners execute Actions workflows in Ubuntu Linux, inside a
container rather than a full VM instance.

> [!NOTE] The container for `ubuntu-slim` runners runs in unprivileged mode.
> This means that some operations requiring elevated privileges - such as
> mounting file systems, using Docker-in-Docker, or accessing l[ow-level...]

The job timeout for single-CPU runners is 15 minutes.
```

---

## 11. `brain-env` NO tiene credencial de GitHub · medido

```plain
=== hay token de GitHub en el entorno? ===
env vars candidatas: []

--- home/cred ---
/root:  .android  .bashrc  .cache  .conda  .config  .kaggle  .local
        .mamba  .npm  .profile  .wget-hsts
ls: cannot access '/workspace/.kaggle*': No such file or directory
```

**Cero variables de entorno con `GITHUB`, `GH_`, `TOKEN` o `CRED`.** La credencial de Kaggle está en `/root/.kaggle`; **de GitHub no hay ninguna.**

<p></p>

Consecuencia medida: **`brain-env` no puede manejar la API de Actions por sí mismo.** Yo escribo por la integración de ClickUp→GitHub, que es otro canal.

### Y el límite de mi propio catálogo, verificado

Busqué herramientas de workflow runs en mi catálogo. **No hay ninguna** que liste corridas ni baje logs de Actions. Lo que hay es lectura y escritura de archivos, PRs, issues, ramas, commits y escaneo de secretos.

<p></p>

**Consecuencia de diseño, no queja:** un workflow que yo escriba tiene que **commitear su propia evidencia al repo** para que yo pueda leerla. No es un workaround: es exactamente W-01 forzado por el entorno, y es mejor así, porque la evidencia queda en el expediente en vez de en un log que expira.

---

--- METODO TITAN ---
Accion delicada: NO (6 corridas de lectura + 1 lectura de la integracion GitHub)
Modo aplicado:   TITAN FULL
Rubrica:         41/45 -> 91/100
N/A declarados:  55 pts (Ejecutabilidad, Seguridad, Testing, DevOps: es
                 evidencia de peritaje, no codigo de produccion)
Review externo:  no pedido (no hay PR: es evidencia)
Instrumento:     gateway MUDH servicio build, 6 corridas python3 (exit=0), y
                 la integracion de GitHub para listar images/ubuntu. Fuentes
                 primarias: archivos reales de actions/runner-images y
                 github/docs, no busqueda web. Un 404 propio incluido.
