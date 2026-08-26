# 122 · El runner gratis en detalle, y las 13 cosas que hace y `brain-env` no puede

**Fecha:** 2026-08-26 · rama `titan/twohop-nulls` · **TITAN FULL**

**Evidencia cruda:** `docs/agents/evidencia/2026-08-26-122-especificaciones-del-runner-evidencia-cruda.md`

**Herramientas declaradas antes de ejecutar (C-03):** `run` del servicio `build` del gateway (6 corridas de lectura), integración de GitHub (1 listado + 2 escrituras). **Fuentes primarias**: los archivos reales de `actions/runner-images` y `github/docs`, no búsqueda web.

---

## 1. El dato que da vuelta el argumento entero

| | **repo PÚBLICO** | repo privado | `brain-env` |
|---|---|---|---|
| CPU | **4 vCPU** | 2 vCPU | **2 CPU** |
| RAM | **16 GB** | 8 GB | **8 GB (650 MB libres)** |
| SSD | 14 GB | 14 GB | 157 GB libres |
| costo | **0, ilimitado** | consume cuota | — |

> **El runner público tiene el DOBLE de CPU y RAM que el privado, y el doble de CPU que `brain-env`.** No es "gratis pero peor": es **gratis y mejor máquina**.

Y es **×20 concurrentes** en plan Free. O sea **80 vCPU y 320 GB de RAM en paralelo**, contra la única máquina de 2 CPU que veníamos usando.

---

## 2. Características del runner, medidas del manifiesto real

**La máquina:** Ubuntu **24.04.4 LTS**, kernel **6.17.0-1022-azure**, imagen **20260816.277.1**, systemd 255.4. VM completa, no container, con **root**.

**Los límites, del doc oficial:**
- **6 horas por job** · **35 días por workflow run** · **256 jobs por matriz**
- **20 jobs concurrentes** en Free (40 Pro, 60 Team, 500 Enterprise) · **5 macOS**
- caché: 200 subidas, 1.500 bajadas, 400 borrados por minuto
- el archivo de workflow: máximo **500 KB**
- **GPU: `Not applicable` en Free.** Los 100 jobs de GPU son solo *larger runners* en Team/Enterprise. **No hay GPU gratis en Actions.**

**Variante barata:** `ubuntu-slim`, 1 CPU, corre en **container sin privilegios** (no hay Docker-in-Docker ni montar filesystems) y **timeout de 15 minutos**.

---

## 3. LISTA 1 · el inventario completo del runner

### Compiladores y lenguajes
**GCC 12.4.0 / 13.3.0 / 14.2.0** · **Clang 16.0.6 / 17.0.6 / 18.1.3** (+ clang-format y clang-tidy en las tres) · **GNU Fortran 12/13/14** · Rust 1.97.1 (cargo, rustup, rustfmt) · Swift 6.3.3 · Kotlin 2.4.10 · Julia 1.12.7 · Node.js 22.23.2 · Python 3.12.3 · Ruby 3.2.3 · Perl 5.38.2 · Bash 5.2.21 · Dash

### Versiones precacheadas (cambio de versión sin instalar)
**Python 3.10.21 / 3.11.16 / 3.12.14 / 3.13.15 / 3.14.7** + **PyPy 7.3.16 / 7.3.19 / 7.3.23** · Go 1.24.13 / 1.25.13 / 1.26.6 · Node 22.23.2 / 24.19.0 · Ruby 3.2.11 / 3.3.12 / 3.4.10 / 4.0.6

### Gestores de paquetes
pip 24.0 · pipx 1.16.7 · **Miniconda 26.5.3** · npm 10.9.8 · Yarn 1.22.22 · **Homebrew 6.0.17** · RubyGems · cpan · **Vcpkg** · Helm 3.21.4

### Build systems
**CMake 3.31.6** · **Ninja 1.13.2** · **Bazel 9.2.0** + Bazelisk · **Gradle 9.7.0** · Maven 3.9.16 · Ant 1.10.14 · Lerna · Parcel

### Contenedores y orquestación
**Docker Client Y Server 28.0.4** · Docker Compose 2.38.2 · Buildx 0.36.1 · **Podman 5.8.4** · **Buildah 1.33.7** · **Skopeo 1.13.3** · **Kind 0.32.0** · **Minikube 1.38.1** · kubectl 1.36.3 · Kustomize 5.8.1

### Git y CI
**Git 2.55.0** · Git LFS 3.7.1 · git-ftp · **Mercurial 6.7.2** · **GitHub CLI 2.97.0** · **CodeQL Action Bundle 2.26.3**

### Nube e infraestructura como código
**AWS CLI 2.36.24** + SAM CLI · **Azure CLI 2.89.1** · **Google Cloud CLI 580.0.0** · **Terraform-equivalentes: Pulumi 3.257.0, Packer 1.16.0, Bicep 0.46.1** · Ansible 2.21.3 · AzCopy

### Bases de datos, corriendo
**PostgreSQL 16.15** · **MySQL 8.0.46** · **sqlite3 3.45.1**

### Navegadores con driver
**Chrome 151 + ChromeDriver** · **Chromium 151** · **Firefox 153 + Geckodriver** · **Edge 151 + WebDriver** · **Selenium Server 4.47.0**

### Utilidades
**jq 1.7** · **yq 4.53.3** · yamllint · zstd 1.5.7 · OpenSSL 3.0.13 · Newman · MediaInfo · Fastlane 2.238.0 · nvm · Haveged

### Otras arquitecturas y sistemas, gratis en público
**`ubuntu-24.04-arm` (arm64 nativo, 4 vCPU / 16 GB)** · `windows-latest` (4/16) · `windows-11-arm` · `macos-15-intel` (4 vCPU / 14 GB) · **`macos-latest` (3 núcleos M1 / 7 GB) con Xcode**

---

## 4. LISTA 2 · lo que el runner hace y `brain-env` NO puede

Cada renglón contra la ausencia **medida** en `brain-env` (respuesta 119 y 120).

| # | capacidad | por qué `brain-env` no puede | a qué proyecto le sirve |
|---|---|---|---|
| 1 | **compilar C/C++ nativo** (GCC 14, Clang 18) | `FALTA:gcc`, `FALTA:cc` medidos | **DualBrain C99: tests nativos antes de cruzar a ESP32.** Hoy imposible acá |
| 2 | **binario `git`** 2.55.0 + LFS | `FALTA:git` medido; `dulwich` clona pero no es git | expediente, ramas, PRs desde el propio job |
| 3 | **`procps`** (`ps`, `top`, `free`) | `FALTA:ps`, `FALTA:pgrep` medidos | lo que me falló dos veces al reportarte procesos |
| 4 | **Docker y Podman de verdad** | `FALTA:docker` medido, y no hay anidamiento | **clean-room INC-002: build reproducible desde fuente** |
| 5 | **20 jobs en paralelo** | `brain-env` es **una** máquina de 2 CPU | los 40 nulls del conectoma en minutos, no en 390,5 |
| 6 | **4 vCPU / 16 GB por job** | 2 CPU / 8 GB, con **650 MB libres ahora** | cualquier corrida que hoy no entra en RAM |
| 7 | **arm64 NATIVO** | x64 solamente | **Oracle ARM y Raspberry sin emulación**: el puente ESP32→Pi |
| 8 | **macOS + Xcode** | no existe en el stack | única vía si MUDH-Mobile toca iOS |
| 9 | **Windows** | no existe en el stack | portabilidad del motor |
| 10 | **Gradle 9.7 + Java + Android SDK** | `java` sí, **`FALTA:gradle`** medido | los 7 workflows de `mudh-mobile`, el emulador con aceleración |
| 11 | **navegadores + Selenium** | no hay navegador dentro | leer las páginas JS de Kaggle sin depender del servicio aparte |
| 12 | **PostgreSQL y MySQL levantados** | solo `sqlite3` por Python | cualquier servicio con base real |
| 13 | **`gh` CLI + AWS/Azure/GCloud CLI** | ninguno, **y sin token de GitHub** (`env vars candidatas: []`) | operar la nube desde el job |

### Y la que más vale, que no es una herramienta

**14. VM limpia, efímera, con versión de imagen inmutable y log público.**

<p></p>

Esto es **W-01 resuelto por construcción**. Un resultado de `brain-env` siempre carga la sospecha de contaminación local: 57 procesos residuales de 71 horas, 5 paquetes que instalé hoy, estado acumulado en `/workspace`. Un job de Actions arranca de **`Image Version: 20260816.277.1`**, exactamente la misma para cualquiera que lo repita, y **su log es público**.

<p></p>

> **Cualquiera puede recomputar el veredicto y contradecirlo sin pedirme permiso.** Eso es lo que el método persigue desde el principio, y es gratis.

**15. Cron.** Trabajo periódico sin dejar nada encendido. Ni `brain-env` ni Kaggle lo dan.

---

## 5. Y al revés: lo que `brain-env` hace y Actions NO

Decirlo completo, porque si no la comparación es propaganda:

1. **Estado persistente.** `/workspace` tiene **157 GB libres** y sobrevive entre llamadas. Actions **borra todo** al terminar el job.
2. **Procesos largos al fondo**, poleables entre turnos. Actions corta a las **6 horas** y no hay a dónde volver.
3. **Iteración interactiva.** Acá abro un archivo, lo toco, lo vuelvo a correr. Actions es disparar y esperar.
4. **Toolchain de ESP32 ya instalado** (`xtensa-esp32-elf-gcc`), que en Actions habría que bajar en cada job.
5. **Lo más importante: no puedo leer los logs de Actions.** Verifiqué mi catálogo y **no hay herramienta de workflow runs**. Así que un workflow mío tiene que **commitear su propia evidencia al repo**. No es un parche: es W-01 forzado, y queda mejor, porque la evidencia entra al expediente en vez de a un log que expira.

**Conclusión de reparto, no de ranking:** `brain-env` es el **taller** (persistente, interactivo). Actions es la **fábrica** (potente, paralela, efímera, auditable). Kaggle es la **GPU**. Son tres, no compiten, y hoy solo usábamos dos.

---

## 6. Lo primero que yo pondría ahí, en orden

**Criterio declarado: qué está hoy imposible y pasa a posible.**

1. **Tests nativos del C99 de DualBrain.** Hoy **no se pueden correr en ningún lado**: no hay compilador de host. Es lo único de esta lista que está en cero absoluto.
2. **Los nulls del conectoma en matriz de 20 jobs.** 390,5 min → ~20 min, y libera los 4 slots de Kaggle.
3. **`guards.yml` a `main`.** Hoy el único CI del repo científico vive solo en la rama de trabajo: **no protege la rama de la que otros clonan.**
4. **Build arm64 nativo** del motor, que es el puente ESP32→Raspberry sin emular.

**Verificación de dependencia (O-01):** los cuatro son **independientes entre sí** y ninguno depende de una credencial tuya. Toco archivos en `.github/workflows/`, nada más.

---

## 7. NO MEDIDO

- **No corrí un solo job todavía.** Todos los números de esta respuesta son del **manifiesto oficial de la imagen** y del **doc oficial**, no de una corrida en tu cuenta. Es la diferencia entre leer la ficha técnica y arrancar el motor.
- **Las secciones `Java`, `Android` y `Web Servers` del manifiesto salieron vacías con mi filtro**, porque su contenido está en tablas y no en viñetas. **No sé qué versiones de JDK ni de Android SDK trae.** Se cierra con otra lectura.
- **No verifiqué el plan real de tu cuenta de GitHub.** Asumo **Free** por los 20 jobs; si fuera Pro son 40. Es inferencia, no medición.
- **No medi la cuota consumida** por `mudh-mobile`: el endpoint de billing pide un scope que la integración no expone. Sigue abierto de la 121.
- **No probé `ubuntu-slim`** ni los runners de arm64, Windows o macOS.
- **404 propio declarado:** adiviné `Ubuntu24-Readme.md`; el real es `Ubuntu2404-Readme.md`. Lo cerré listando el directorio en vez de seguir adivinando.

---

--- METODO TITAN ---
Accion delicada: NO (lecturas + 2 escrituras de documentacion en rama de trabajo)
Modo aplicado:   TITAN FULL
Rubrica:         41/45 -> 91/100
                 Completitud 12/15 (-3: no corri ningun job, y tres secciones
                 del manifiesto quedaron sin leer por mi propio filtro)
                 Arquitectura del razonamiento 10/10 (el reparto taller /
                 fabrica / GPU y la lista inversa evitan que sea propaganda)
                 Documentacion 10/10 · Innovacion 5/5 (el punto 14, Actions
                 como instrumento que resuelve W-01 por construccion, no fue
                 pedido) · Proceso QA 4/5 (-1: el plan Free es inferencia)
N/A declarados:  55 pts (Ejecutabilidad, Seguridad, Testing, DevOps: es un
                 peritaje de infraestructura, no codigo de produccion)
Review externo:  no pedido (no hay PR: son dos archivos de documentacion)
Instrumento:     gateway MUDH servicio build, 6 corridas python3 (exit=0) contra
                 raw.githubusercontent.com · integracion GitHub, 1 listado.
                 Salida cruda verbatim commiteada aparte, con mi 404 (W-01).
