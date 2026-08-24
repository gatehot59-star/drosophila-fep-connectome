# CONTEXTO VIVO · EL ENTORNO DE EJECUCIóN

**Última medición:** 2026-08-24 15:06 UTC (12:06 America/Buenos_Aires) · **Se sobreescribe, no se acumula.**

<p><br/></p>

**POR QUÉ EXISTE ESTE ARCHIVO.** Abraham lo señaló hoy y tenía razón: *"en ningún lugar está especificado el entorno virtual que te preparé y las actualizaciones que te hice, en git está a medias"*. Los tres contextos que había (`CONTEXTO-motor.md`, `CONTEXTO-drosophila-fep.md`, `AGENT-BRAIN.md`) documentan **el trabajo** y no **la máquina donde se hace**. Así que cada vez que el chat se cortaba, el inventario del entorno se reconstruía de memoria, y la memoria estaba vieja.

<p><br/></p>

**Todo lo de abajo está MEDIDO hoy con llamadas reales, no listado de memoria.** Lo no medido va declarado al final.

---

## 0. LAS CUATRO AFIRMACIONES MÍAS QUE ERAN FALSAS

Esto va primero porque es el daño concreto de no haber tenido este archivo:

| Lo que afirmé, y dónde | Lo medido hoy |
|---|---|
| *"el sandbox no tiene red"* / *"contenedor local, **sin red**"* | **Red completa.** `api.github.com`, `www.kaggle.com`, `pypi.org` y DNS: los cuatro alcanzables |
| *"NO tengo: `npm`, `tsc`, `javac`, `gradle`, `cmake`"* | **`npm` 11.16.0 y `javac` 17.0.20 SÍ están, y javac COMPILA (exit=0).** `cmake` 3.22.1 está dentro del SDK de Android |
| *"el container no tiene Python"* (usado para justificar "Kaggle es el compilador") | **Python 3.12.14 con torch, numpy, scipy, pandas, igraph, sklearn** |
| *"el cruce real al ESP32 queda pendiente / sin hardware no hay número"* | **`xtensa-esp32-elf-gcc` 16.1.0 está en el PATH y COMPILA para Xtensa (exit=0)** |

**Las cuatro son el patrón 3 del Bloque 8: un límite afirmado sin verificar.** Y las cuatro llevaron a derivar trabajo a Kaggle o a Tachi que este container podía hacer.

---

## 1. 🔥 EL HALLAZGO: el toolchain del ESP32 está instalado y funciona

**Esto desbloquea la línea embebida y estaba en `EN PAUSA` desde el HANDOFF del 22-ago.**

```
/opt/xtensa-esp-elf/bin          -> EN EL PATH, 116 binarios
xtensa-esp-elf-gcc (crosstool-NG esp-16.1.0_20260609) 16.1.0

compiladores presentes:
  xtensa-esp32-elf-gcc     <- ESP32
  xtensa-esp32s2-elf-gcc   <- ESP32-S2
  xtensa-esp32s3-elf-gcc   <- ESP32-S3
  xtensa-esp-elf-gcc       <- genérico

PRUEBA REAL (no lectura del PATH):
  $ xtensa-esp32s3-elf-gcc -Os -c -o /tmp/esp/m.o /tmp/esp/m.c
  exit=0
  $ xtensa-esp-elf-size /tmp/esp/m.o
  text   data   bss   dec   hex   filename
     7      0     0     7     7   /tmp/esp/m.o
```

También están `xtensa-esp-elf-as`, `-ar`, `-objdump`, `-nm`, `-size`, `-addr2line`, `-c++`, `-cpp`, `-elfedit`, `-ranlib`.

<p><br/></p>

**Consecuencia directa y medible para DualBrain C99:** los **2.496 B de `.text` y 704 B de RAM** se midieron con **gcc de x86**, y de ahí salió la cota de ~20 kSPS marcada como *"derivada del conteo de MAC, no medida en hardware"*. Con `xtensa-esp32-elf-gcc -Os` + `xtensa-esp-elf-size` se puede medir **el tamaño real en el target**, que es un número distinto y publicable. **Eso ya no es un pendiente de hardware: es un pendiente de correr un comando.**

---

## 2. La máquina

| | |
|---|---|
| SO | **Debian GNU/Linux 13 (trixie)** |
| Kernel | 4.19.0-27-amd64, x86_64 |
| Host | `d250f65d4cc4` |
| CPU | **2 núcleos** |
| RAM | **7.989.580 kB ≈ 7,99 GB** |
| `/workspace` | **406 GB total, 229 GB usados, 158 GB libres (60%)**, en `/dev/sda4` |
| **Uptime** | **275.200 s = 76,4 h = 3,2 días** |

**El uptime es la medición que cierra la discusión de la persistencia:** el container lleva **3,2 días** vivo. No es efímero, y `/workspace` sobrevive entre llamadas y entre sesiones. La nota vieja que decía lo contrario está refutada por un número.

**Y los procesos en background SÍ sobreviven** entre llamadas (verificado por `/proc` en las corridas del A/B del gate, resp 020-025). `ps` no existe: la liveness se mide con `grep -al <patron> /proc/[0-9]*/cmdline`.

---

## 3. Runtimes: lo que HAY, con versión exacta y ruta

| Herramienta | Versión | Ruta |
|---|---|---|
| `python3` | **3.12.14** | `/usr/local/bin/python3` |
| `pip3` | 25.0.1 | `/usr/local/bin/pip3` |
| `node` | **v24.18.0** | `/home/estudiante/.nvm/versions/node/v24.18.0/bin/node` |
| `npm` | **11.16.0** | idem (nvm) |
| `npx` | 11.16.0 | idem (nvm) |
| `java` | **openjdk 17.0.20 2026-07-21** | `/home/estudiante/jdk17/bin/java` |
| `javac` | **17.0.20** | `/home/estudiante/jdk17/bin/javac` |
| `R` | **4.5.3 (2026-03-11)** | `/opt/mamba/bin/R` |
| `Rscript` | 4.5.3 | `/opt/mamba/bin/Rscript` |
| `make` | GNU Make 4.4.1 | `/opt/mamba/bin/make` |
| `curl` | 8.21.0 | `/opt/mamba/bin/curl` |
| `openssl` | 3.6.3 | `/opt/mamba/bin/openssl` |
| `tar` | GNU tar 1.35 | `/usr/bin/tar` |
| `md5sum` | coreutils 9.7 | `/usr/bin/md5sum` |

### Lo que NO hay (medido, no supuesto)

`git` · `gcc` del host · `tsc` · `cmake` en PATH · `gradle` en PATH · `sqlite3` · `ps` · `top` · `jq` · `wget` · `docker` · `gh` · `bc` · `vim` · `unzip` · `xz` · `rsync` · `adb` en PATH

**`tsc` no está pero `npm` sí**, o sea que se instala. El *"el TypeScript NO se compiló"* de los PRs #64 y #68 no está bloqueado por el entorno.

### Paquetes de Python

| | |
|---|---|
| **SÍ** | numpy **2.5.2** · scipy **1.18.1** · pandas **3.0.5** · **torch 2.13.0+cpu** · igraph **1.0.0** · scikit-learn **1.9.0** · matplotlib **3.11.1** · pyarrow **25.0.1** · networkx **3.6.1** · numba **0.67.0** · requests **2.34.2** |
| **NO** | `h5py` · `statsmodels` |

---

## 4. El SDK de Android que instaló Abraham

`ANDROID_HOME=/home/estudiante/Android` · `JAVA_HOME=/home/estudiante/jdk17` (las dos seteadas)

| Componente | Versión / ruta |
|---|---|
| `platform-tools` | con **`adb`** en `Android/platform-tools/adb` (12 archivos) |
| `build-tools` | **36.0.0**, con `aapt2` y `apksigner` |
| `platforms` | **android-36** |
| `system-images` | **android-34** |
| **NDK** | **28.2.13676358** con `clang` en `toolchains/llvm/prebuilt/linux-x86_64/bin/` |
| `cmake` | **3.22.1** |
| `emulator` | presente (bin64, lib64, qemu, resources) |
| `licenses` | **7 licencias aceptadas** |

**Prueba real de la cadena Java:**
```
$ javac T.java   -> exit=0
$ java T         -> exit=0, salida: JAVAC_OK
```

**Nota del NDK:** `clang` sin `--target` no encuentra `stdio.h` (`fatal error: 'stdio.h' file not found`). No es una falla del toolchain: falta el triple del target y el sysroot. Compilar para Android necesita `--target=aarch64-linux-android21` o el `CMakeLists` del NDK.

---

## 5. Red

| Destino | Estado |
|---|---|
| `api.github.com:443` | **alcanzable** |
| `www.kaggle.com:443` | **alcanzable** |
| `pypi.org:443` | **alcanzable** |
| `1.1.1.1:53` (DNS) | **alcanzable** |

**El container tiene salida a internet.** Eso habilita `pip install`, `npm install` y la API de Kaggle desde acá, sin intermediario.

---

## 6. `/workspace`: 999 archivos, 528,3 MB

| Directorio | Qué es |
|---|---|
| **`mudh/`** | **Árbol de trabajo del repo MUDH-Mobile**: `gradlew`, `app/`, `build/`, `build.gradle.kts`, `local.properties`, `mudh-kernel/`, `AGENTS.md`, `BUILD_REPORT.md`, `audit/`, `docs/`, `.github/`. **`.git` existe pero NO es directorio** (gitfile o worktree): hay que medir antes de tratarlo como clon |
| `ab_cell/` | A/B del bias de flujo (resp 024-025, 030) |
| `ab_gate/` | A/B del gate escalar vs vectorial (resp 020-023) |
| `bicam/` | BICAMERALITY: `cell1.py`, `cell1_fixed.py` |
| `brazos/` · `wbrazo/` | los tres brazos y el brazo W |
| `kaggle/` | dumps de los 29 notebooks + helpers |
| `repo/` | los 11 archivos staged del release que nunca se commiteó |
| `c/` · `gg/` · `tags/` | sin auditar |
| `node_modules/` · `__pycache__/` | derivados |

Archivos de primer nivel ya conocidos: `motor.py` (30.644 B), `scriptR.py` (10.376 B), `tres_brazos.py` (430 líneas), `hm_sweep.py`, `hm_base.py`, `paper_db.py`, `dualbrain_src.py`, y ~20 logs.

---

## 7. El gateway MCP

| Servicio | Tools | Estado |
|---|---|---|
| `build` | **2** (`run`, `list_files`) | shell dentro de `brain-env`. Es el instrumento principal |
| `adb` | **65** | control del emulador. **Las tools que tocan el host (gradle, file, scaffold) están BLOQUEADAS a propósito** |
| `kaggle` | — | 2 cuentas (`fabiomurillohot`, `abrahammendieta`) con rotación |
| `playwright` | — | navegador real, aislado |
| `sqlite` | — | base compartida `nexus.db` con Tachi. **`sqlite3` CLI no existe en el container: la vía es el servicio** |
| `supply-chain` | 7 | orquestan ~90 técnicas sobre 21 fuentes |
| `registry` | — | verificación de versiones |
| `seq-think` | — | **valor NO MEDIDO, cuarta vez declarado** |

**Límite del gateway medido:** el timeout de una llamada está **entre 45 y 75 s**. `sleep 45` pasa, `sleep 75` no. Para esperas largas: lanzar en background y hacer polling.

---

## 8. Reglas operativas del entorno, aprendidas a los golpes

1. **`ps` no existe.** Liveness: `grep -al <patron> /proc/[0-9]*/cmdline`.
2. **`cd X && cmd &` backgroundea la cadena entera** y el proceso arranca en `/`. Usar **rutas absolutas** al lanzar (resp 021).
3. **Verificar TAG/env de cada proceso en `/proc/<pid>/environ` antes de dejarlos correr.** Dos procesos con el mismo tag se pisan el archivo de salida (resp 021, costó 30 min de CPU).
4. **El shell es `sh`, no bash.** Fallan: `heredoc` anidado, `process substitution`, `for c in ...; do $c --version`. La vía que funciona: escribir el script con `printf '%s\n'` y correrlo, o usar Python.
5. **Los MSE de torch son deterministas por semilla:** idénticos a 6 decimales con `THREADS=1` y con 4. Y **`THREADS=1` es más rápido** con modelos chicos.
6. **Guardado incremental obligatorio** en cualquier corrida larga: un `json.dump` por brazo, para que un corte no borre horas.

---

## 9. Lo que esto DESBLOQUEA, y hay que decidir

| Pendiente que estaba bloqueado | Con qué se desbloquea |
|---|---|
| **El cruce al ESP32 del DualBrain C99** | `xtensa-esp32-elf-gcc -Os` + `xtensa-esp-elf-size`. **Convierte los 2.496 B de x86 en el número real del target** |
| *"el TypeScript NO se compiló"* (PRs #64, #68) | `npm install typescript` → `tsc`. `npm` existe y hay red |
| Cualquier build de Java/Kotlin | `javac` compila, medido. `gradlew` está en `/workspace/mudh` |
| Compilación nativa para Android | NDK 28.2 con `clang`, con `--target` y sysroot |

**Y una advertencia que va con esto (Bloque 2.3, item 6 de acciones delicadas):** `build.gradle.kts` **es código Kotlin que corre con los permisos del usuario**. Que el toolchain exista no autoriza a disparar un build de Gradle en la máquina de Abraham. Eso sigue siendo su decisión, y la restricción del gateway (host bloqueado) está puesta con criterio.

---

## 10. NO MEDIDO, declarado

- **No corrí `gradlew`.** No sé si el build de MUDH pasa. Y **no lo voy a correr sin permiso**: es código que se ejecuta en su máquina.
- **`/workspace/mudh/.git` no es un directorio.** No verifiqué si es un gitfile de worktree, un submodule, o un archivo cualquiera. **Traté el árbol como "working tree" sin confirmar que sea un clon.**
- **No compilé el DualBrain C99 para Xtensa.** Probé el toolchain con un `int suma(int,int)`. Que compile un archivo trivial **no prueba** que compile `esp32c.py`/el C99 real: falta el `.h`, los flags y el linkeo.
- **No medi las tools de `kaggle`, `playwright`, `sqlite`, `registry` ni `seq-think`.** Solo `adb` (65) y `build` (2). El total de 101 de la memoria **no lo reverifiqué hoy**.
- **`seq-think` sigue sin probarse.** Cuarta declaración.
- **No audité `/workspace/c`, `/workspace/gg` ni `/workspace/tags`.** No sé qué hay.
- **No verifiqué si hay un AVD creado** ni si el emulador arranca hoy. La última vez (21-ago) el System UI estaba colgado.
- **No sé qué más instaló Abraham fuera de `/home/estudiante` y `/opt`.** Barrí esos dos.
- **La lista de "lo que NO hay" es de 38 comandos probados**, no del PATH completo.

---

## 11. Regla de mantenimiento de este archivo

**Se re-mide, no se recuerda.** Cada vez que una decisión dependa de una capacidad del entorno:

1. **Hacer la llamada** antes de afirmar el límite.
2. Si lo medido contradice este archivo, **gana lo medido** y este archivo se corrige en el mismo turno.
3. Si Abraham instala algo, **entra acá con su versión y su prueba de que funciona**, no con su nombre.

**El criterio de suficiencia:** una capacidad se declara presente **solo con la salida cruda de haberla usado**. "Está en el PATH" no es "funciona": el `clang` del NDK está en el disco y falla sin `--target`.
