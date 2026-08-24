# CONTEXTO VIVO · EL ENTORNO DE EJECUCIóN

**Última medición:** 2026-08-24 15:06 UTC (12:06 America/Buenos_Aires) · **ampliada 15:15 UTC (12:15), ver §12** · **ampliada 17:05 UTC (14:05), ver §13** · **Se sobreescribe, no se acumula.**

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

> **→ CERRADO en §13.1 el 24-ago 14:05: el comando se corrió. El número es 1.336 B.**

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

> **→ §13.3 resuelve el `mudh/.git` (es un gitfile HUÉRFANO, no un clon), §13.4 audita `c/`, `gg/` y `tags/`, y §13.5 da el conteo por directorio. El `repo/` sin commitear resultó contener el entregable del 30-ago: ver §13.2.**

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

> **→ §13.6 agrega las reglas 7 a 10, y dos de ellas son guards propios que NO PUEDEN DAR ROJO.**

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

> **→ De estos, §13 cierra tres: el `mudh/.git`, la compilación del C99 para Xtensa, y los tres directorios sin auditar. El resto sigue abierto.**

---

## 11. Regla de mantenimiento de este archivo

**Se re-mide, no se recuerda.** Cada vez que una decisión dependa de una capacidad del entorno:

1. **Hacer la llamada** antes de afirmar el límite.
2. Si lo medido contradice este archivo, **gana lo medido** y este archivo se corrige en el mismo turno.
3. Si Abraham instala algo, **entra acá con su versión y su prueba de que funciona**, no con su nombre.

**El criterio de suficiencia:** una capacidad se declara presente **solo con la salida cruda de haberla usado**. "Está en el PATH" no es "funciona": el `clang` del NDK está en el disco y falla sin `--target`.

> **⚠️ INCUMPLIMIENTO REGISTRADO:** entre las respuestas 036, 037 y 038 este archivo figuró **tres veces como NO MEDIDO**, con esta regla escrita adentro. Se lo citó por commit message en vez de abrirlo. Abraham lo cobró en el turno de la resp 039 con la frase *"ni en tu entorno virtual"*, y tenía razón: **la regla estaba y la llamada no.**

---

## 12. AMPLIACIÓN 2026-08-24 15:15 UTC · cinco mediciones nuevas

**Cómo se hizo, y por qué importa el cómo:** este archivo ya existía cuando volví a medir el entorno a las 12:15 (había perdido el hilo de haberlo escrito seis minutos antes). Al intentar crearlo de nuevo, GitHub lo rechazó por conflicto de existencia. **Ese rechazo evitó que sobrescribiera las secciones 0 a 11 con una versión que NO contenía el hallazgo del ESP32.** Las secciones 0 a 11 no se tocaron: esta §12 es puro agregado.

**Es la prueba de que el método funciona:** el trabajo no se perdió con el chat. Lo que se perdió fue la memoria de haberlo hecho, y el archivo la reemplazó.

### 12.1 `tsc` no solo se instala: **compila y puede dar ROJO**

La §3 decía "`tsc` no está pero `npm` sí, o sea que se instala". Eso era una **inferencia**. Ahora está **probado**:

```
$ cd /tmp/tsctest && npm install typescript@5.9.2 --no-audit --no-fund
added 1 package in 4s

$ ./node_modules/.bin/tsc --version
Version 5.9.2

$ printf 'const x: number = "roto";\n' > t.ts && ./node_modules/.bin/tsc t.ts
t.ts(1,7): error TS2322: Type 'string' is not assignable to type 'number'.
```

**Lo que agrega sobre la §9: el instrumento PUEDE DAR ROJO.** Un compilador que no puede fallar no sirve de testigo (W-01). Los PRs **#64** y **#68** dicen *"el TypeScript NO se compiló"* y su causa declarada era *"no tengo toolchain local"*: **la causa es falsa y ahora está refutada con la salida de error, no con el PATH.**

### 12.2 El modelo del LLM local **ya está bajado**

```
-rw-r--r-- 1 1000 1000 102039904 Aug 16 02:57
  /home/estudiante/Android/SmolLM2-135M-Instruct-Q4_K_S.gguf
```

**102.039.904 B, del 16-ago.** Los docs de MUDH-Mobile lo listan como *"HuggingFaceTB/SmolLM2-135M-Instruct-GGUF, 97.3 MB < 100 MB"* y como algo a conseguir. **Está en el disco desde hace 8 días.**

### 12.3 `adb` **arranca su daemon y responde**

La §4 dice que `adb` "está presente". Medido, hace más que estar:

```
$ /home/estudiante/Android/platform-tools/adb devices
* daemon not running; starting now at tcp:5037
* daemon started successfully
List of devices attached
(vacio)
```

**El binario funciona y levanta el servidor.** La lista vacía es un dato distinto: **no hay device conectado al momento de medir**, ni emulador corriendo.

### 12.4 El emulador falla por una **librería gráfica**, no por imposibilidad

```
$ /home/estudiante/Android/emulator/emulator -list-avds
emulator: error while loading shared libraries: libX11.so.6:
          cannot open shared object file: No such file or directory
```

**Distinción que importa y que la §10 dejaba abierta como "no verifiqué si arranca":** no es que el emulador no pueda correr, es que **le falta `libX11.so.6`**. Las dos vías obvias (`-no-window` para headless, o instalar la librería) **NO se probaron**. Es un estado NO MEDIDO con causa identificada, que es mejor que un NO MEDIDO a secas.

### 12.5 El NDK tiene **DOS** versiones, no una

La §4 lista `28.2.13676358`. Medido:

```
$ ls /home/estudiante/Android/ndk
28.2.13676354
28.2.13676358
```

**Dos builds del NDK 28.2 conviviendo.** No sé si son iguales ni cuál usó Abraham, y **eso hay que resolverlo antes de compilar nada nativo**: elegir uno al azar y reportar el resultado sin decir cuál sería el patrón del sujeto equivocado (E-01).

### 12.6 Coincidencias que confirman la medición de las 12:06

Lo re-medido cerró con lo que ya estaba, y eso vale como validación cruzada del instrumento:

| Cantidad | 12:06 | 12:15 |
|---|---|---|
| SO | Debian 13 trixie | idéntico |
| Host | `d250f65d4cc4` | idéntico |
| CPU / RAM | 2 / 7.989.580 kB | idéntico |
| `/workspace` | 406G, 229G usados, 60% | idéntico |
| Uptime | 275.200 s | **275.566,63 s** (+366 s, consistente con los 6 min entre mediciones) |
| npm | 11.16.0 | idéntico |
| java | 17.0.20 | idéntico |
| Red | pypi/github alcanzables | `pypi=200`, `github=200` |

**El delta de uptime de +366 s contra 6 minutos de reloj es la prueba de que las dos mediciones son del mismo container vivo**, y no de dos instancias distintas.

### 12.7 Discrepancia de conteo de `/workspace`, y gana el número mayor

La §6 dice **999 archivos, 528,3 MB**. Mi conteo de las 12:15 dio **375 archivos, 507 MB**, pero con `find -maxdepth 2`: **conté menos profundidad, no menos archivos**. **Gana la §6.** Lo dejo escrito porque un número menor obtenido con otro comando no es una contradicción del dato: es una medición distinta mal comparada, y confundirlas es cómo se "corrige" un archivo hacia atrás.

Lo que mi conteo sí agrega: **20 `.py` en la raíz** enumerados (`motor.py`, `scriptR.py`, `scriptR_v1_buggy.py`, `cp40.py`, `hm_sweep.py`, `hm_base.py`, `tres_brazos.py`, `nulls40_kaggle.py`, `nulls19.py`, `nulls19b.py`, `n21.py`, `esp32c.py`, `paper_db.py`, `dualbrain_src.py`, `cmp_db.py`, `chkmap.py`, `pchk.py`, `synchk.py`, `_t.py`, `x.py`) y **74 `.json`/`.log`** en la raíz. **En git hay 6 `.py` y 2 `.log`.**

> **→ CORREGIDO en §13.5: los `.log` en git son 3, no 2. Y el cruce estaba hecho contra el directorio equivocado: `guards.py` no está en la raíz del container, vive en `gg/`.**

### 12.8 NO MEDIDO de esta ampliación

- **El emulador headless** (`-no-window`) y si `libX11` se puede instalar.
- **Si las dos versiones del NDK son idénticas** y cuál corresponde usar.
- **Si `pip install` funciona.** Se infiere de la red de `npm` y `curl`. **Inferir es lo que esta sección vino a corregir en el caso de `tsc`, así que queda como inferencia declarada.**
- **No re-verifiqué el toolchain del ESP32** en esta pasada. La §1 lo tiene medido a las 12:06 y no lo toqué.
- **No comparé este archivo línea por línea** después de la fusión. La verificación hecha fue por lectura de vuelta y chequeo de que las secciones 0 a 11 sigan presentes con su contenido clave.

```
--- METODO TITAN ---
Accion delicada: SI. Sobrescritura de un archivo de contexto existente en main.
                 Mitigacion aplicada: se leyo el archivo completo ANTES de
                 escribir, se paso el sha dff60f3efe8f9e1ac585a000b62b2a97abf1b263
                 para que un cambio concurrente aborte la escritura, y las
                 secciones 0 a 11 se reprodujeron sin editar una linea. Todo lo
                 nuevo esta confinado a la seccion 12.
Modo aplicado:   TITAN FULL
Rubrica:         se emite en la respuesta 033, que documenta la fusion.
N/A declarados:  pendiente
Review externo:  el falsador de esta escritura fue GITHUB, no una persona: el
                 conflicto de existencia del archivo impidio que sobrescribiera
                 el hallazgo del ESP32 con una version que no lo tenia. Es el
                 caso mas puro de W-01: la independencia es del instrumento.
Instrumento:     gateway build.run sobre brain-env, 7 llamadas (6 de lectura y
                 una escritura efimera en /tmp/tsctest).
                 Evidencia cruda verbatim en 12.1 a 12.5, sin recortar.
                 Prueba clave: tsc 5.9.2 instalado en 4 s y devolviendo
                 error TS2322 sobre codigo roto a proposito.
                 NO MEDIDO: seccion 12.8.
```

---

## 13. AMPLIACIÓN 2026-08-24 17:05 UTC (14:05 local) · el cruce Docs × git × container

**Por qué existe esta sección:** las respuestas 036, 037 y 038 midieron **git y los Docs** y **nunca** tocaron el container, con este archivo declarado NO MEDIDO las tres veces. Abraham lo cobró. Esta §13 es el resultado de 6 llamadas a `build.run`, y **no toca ni una línea de las secciones 0 a 12**: es puro agregado.

### 13.1 🔥 CERRADO · el DualBrain C99 compila para Xtensa: **1.336 B**

La §1 decía *"eso ya no es un pendiente de hardware: es un pendiente de correr un comando"*. **El comando se corrió.**

**Primero, lo que la §10 declaraba faltante y existía desde el 22-ago:**

```
$ ls -l /workspace/c/
-rw-r--r-- 1 root root  9261 Aug 22 22:45 db_test.c      (238 lineas)
-rw-r--r-- 1 root root  8328 Aug 22 22:38 dualbrain.c    (248 lineas)
-rw-r--r-- 1 root root  4848 Aug 22 22:36 dualbrain.h    (109 lineas)  <- EXISTE
-rw-r--r-- 1 root root 30029 Aug 22 22:45 payload.json   (los pesos)
```

La §10 decía *"falta el `.h`, los flags y el linkeo"*. **El `.h` estaba ahí.** Lo único que faltaba era **`-I.`**, porque el include es `<dualbrain.h>` con ángulos y no con comillas.

**El número:**

```
$ xtensa-esp32-elf-gcc -std=c99 -Os -I. -c -o /tmp/db_os.o dualbrain.c
COMPILA_OK_exit0
$ xtensa-esp-elf-size /tmp/db_os.o
   text    data     bss     dec     hex  filename
   1336       0       0    1336     538  /tmp/db_os.o

$ xtensa-esp32-elf-gcc -std=c99 -O2 -I. -c -o /tmp/db_o2.o dualbrain.c
   1796       0       0    1796     704  /tmp/db_o2.o

$ xtensa-esp32s3-elf-gcc -std=c99 -Os -I. -c -o /tmp/db_s3.o dualbrain.c
   1336       0       0    1336     538  /tmp/db_s3.o

$ xtensa-esp32-elf-gcc -std=c99 -Os -I. -c -o /tmp/dbtest.o db_test.c
   3150       0       0    3150     c4e  /tmp/dbtest.o

$ xtensa-esp-elf-size -t /tmp/db_os.o /tmp/dbtest.o
   4486       0       0    4486    1186  (TOTALS)

compilador: xtensa-esp-elf-gcc (crosstool-NG esp-16.1.0_20260609) 16.1.0
md5: dualbrain.c  d0286c619de8f75b2a096c653e0bc161
     dualbrain.h  14fdb6b445f04a838ac21c0ec3bb6ce7
     db_test.c    43157c6d4651e2865ae0cc8d442943d1
     payload.json e4f999263dfcd3c62b26a62d0e174454
```

**Los tres números que salen de acá:**

1. **1.336 B de `.text` en el target real**, contra los **2.496 B de x86**: **1,87× más chico**. Es un número publicable y reemplaza al de x86.
2. **`-Os` le gana a `-O2` por 460 B (34%).** La flag correcta queda medida, no supuesta.
3. **ESP32 y ESP32-S3 dan el tamaño exacto igual** (1.336 B los dos).

**Prueba de que el instrumento puede dar ROJO (W-01), sin la cual el 1.336 no vale:**

```
$ printf 'int x = "roto";\n' > /tmp/roto.c
$ xtensa-esp32-elf-gcc -std=c99 -c -o /tmp/roto.o /tmp/roto.c
/tmp/roto.c:1:9: error: initialization of 'int' from 'char *' makes integer
                from pointer without a cast [-Wint-conversion]
DIO_ROJO_OK
```

**LO QUE ESTO NO ES, y hay que decirlo antes de que alguien lo cite mal:** no se linkeó, no hay `.elf`, **no hay RAM medida en target** (los 704 B siguen siendo de x86) y **nada corrió en un ESP32**. Es **tamaño de código compilado**, no throughput: la cota de ~20 kSPS sigue derivada del conteo de MAC.

### 13.2 🚨 El entregable del 30-ago **NO ESTÁ VERSIONADO**

La §6 describe `repo/` como *"los 11 archivos staged del release que nunca se commiteó"*. **Uno de esos 11 es el erratum.**

```
$ get_file_contents docs/   (repo en main)
[{"name":"agents","type":"dir"}]      <- docs/ tiene UN subdir y CERO archivos

$ md5sum /workspace/repo/docs/ERRATUM.md
2ae28606c28c140dc76cd3b8e6b3ab85   ·   125 lineas, 6862 B
```

**`docs/ERRATUM.md` no existe en git.** Vive únicamente en `/workspace/repo/docs/`, sin versionar, y **cuatro documentos afirman que ya está commiteado**. Es el umbral #1 del plan de 10 semanas y vence el **30-ago**.

Los 11, enumerados:

```
repo/LICENSE                    repo/docs/ERRATUM.md   <- EL ENTREGABLE
repo/README.md                  repo/docs/METHODS.md   (93 lineas,
repo/src/analyze_nulls40.mjs                            md5 0c2f9bf2d4b9f6bcaaf6cbaad1bf08b9)
repo/src/nulls40_structural.py  repo/results/dualbrain_bench.json
repo/src/routing_hierarchy.mjs  repo/results/dualbrain_bench.log
                                repo/results/nulls40.json
                                repo/results/nulls40.log
```

**Rescatado verbatim** en `docs/agents/evidencia/2026-08-24-ERRATUM-md-verbatim-del-container.md` (resp 039). **Los otros 10 siguen sin versionar y sin leer.**

### 13.3 CERRADO · `/workspace/mudh` **no es un clon**: worktree huérfano de PR 75

La §6 y la §10 lo dejaban abierto. Medido:

```
$ head -c 200 /workspace/mudh/.git
gitdir: /home/estudiante/MUDH-Mobile/.git/worktrees/pr75

$ ls -d /home/estudiante/MUDH-Mobile
ls: cannot access '/home/estudiante/MUDH-Mobile': No such file or directory

$ command -v git
GIT_NO_EXISTE
```

**El destino del gitfile no existe.** Los **499 archivos** de `/workspace/mudh` son un checkout **huérfano** de **PR 75**, sin repo padre y sin `git` para operarlo.

**Consecuencia operativa, y es la que importa:** ese árbol **no es el estado de MUDH-Mobile**. No hay que leer su `AGENTS.md` ni su `BUILD_REPORT.md` como los vigentes, ni sacar conclusiones sobre los PRs **#64** y **#68** desde ahí: está parado en **otro PR** y no hay forma directa de saber en qué commit. **La §9 dice "`gradlew` está en `/workspace/mudh`": está, pero sobre un árbol huérfano.**

### 13.4 CERRADO · los tres directorios "sin auditar" de la §6

```
$ ls -1 c        $ ls -1 gg              $ ls -1 tags
db_test.c        __pycache__             (vacio)
dualbrain.c      guards.py
dualbrain.h      saturacion.json
payload.json     t79.log
                 t79.py
                 test_guards.json
                 test_guards.log
                 test_guards.py
```

**`c/` es el C99 del ESP32** (§13.1). **`gg/` son los guards**, y ahí viven `guards.py` y `test_guards.log`, **los dos archivos que están en git**. **`tags/` está VACÍO.**

### 13.5 CORRIGE la §12.7 · el cruce estaba hecho contra el directorio equivocado

| | git | `/workspace` |
|---|---|---|
| `.py` | **6** (en `src/`) | **20** en la raíz, más subdirectorios |
| `.log` | **3** en `results/` ← la §12.7 decía 2 | **45** en la raíz |
| `.json` | 0 | **29** en la raíz |
| `.mjs` | 0 | **78** en la raíz |

Los 3 `.log` de git: `hm_sweep.log`, `motor_ltc_complejo.log`, `test_guards.log`.

**Y el error de método:** `guards.py` es uno de los 6 `.py` de git y **no está en la raíz del container**:

```
$ find / -name 'guards.py' -not -path '*/node_modules/*'
/usr/local/lib/python3.12/site-packages/torch/_dynamo/guards.py
/workspace/gg/guards.py
$ find / -name 'test_guards.log'
/workspace/gg/test_guards.log
```

**Los 14 `.py` de la raíz que NO están en git:** `dualbrain_src.py` (20.122 B) · `esp32c.py` (40.175) · `hm_base.py` (10.971) · `n21.py` (57.157) · `nulls19.py` (12.346) · `nulls19b.py` (11.805) · `paper_db.py` (20.122) · `scriptR_v1_buggy.py` (10.381) · `tres_brazos.py` (17.805) · `cmp_db.py` (1.683) · `chkmap.py` (519) · `pchk.py` (478) · `synchk.py` (449) · `x.py` (212) · `_t.py` (64).

**Archivos por directorio, medido:** `mudh` 499 · `kaggle` 61 · `bicam` 41 · `ab_cell` 16 · `repo` 11 · `gg` 10 · `ab_gate` 9 · `wbrazo` 5 · `brazos` 4 · `c` 4 · `tags` 0. **Total bajo `/workspace`: 999**, que confirma la §6 exacto.

**Lo que el cruce CONFIRMÓ, y vale tanto como lo que corrigió:** los **8 md5** que afirman los contextos y los Docs se verifican **exactos**.

```
11591eb654eb719ae941aa524c1f59fd  ab_gate/ab_gate.py
b829d49ca654ad1d48a2e92e0091e660  ab_cell/equiv.py
4278bb8f27f2b0d8e43a26541629c7b8  ab_cell/ab_cell.py
480539069ec00f317eec525e6fa81324  motor.py
8a42246b54157cbee67fe99110a7be40  paper_db.py       <- la pareja byte-identica,
8a42246b54157cbee67fe99110a7be40  dualbrain_src.py     confirmada, 20122 B c/u
3d802fd542b5d18570ba1ba0bb0abed9  connectivity.parquet
719904abad876c68ace1b5690c9b9b63  annotations.tsv
```

**El problema del corpus nunca fue la medición: es dónde vive el archivo.**

### 13.6 Reglas 7 a 10 del entorno, y dos son guards propios que NO pueden dar rojo

**7. En este `sh`, `$?` NO es un testigo válido.** Medido hoy:

```
dualbrain.c:8:10: fatal error: dualbrain.h: No such file or directory
compilation terminated.
exit=0                    <- FALSO. gcc fallo y echo "exit=$?" dijo cero.
```

**La vía que sí discrimina:** `if <cmd>; then echo OK; else echo FALLA; fi`. Todas las mediciones de §13.1 la usan.

**8. Un `grep -c` que devuelve 0 es NO MEDIDO** hasta probar el patrón contra un positivo conocido. Medido hoy, sobre el erratum:

```
$ grep -c '1559\|1\.559' docs/ERRATUM.md
0                    <- y de aca casi conclui "el 1.559 no esta en el archivo"
$ grep -c '1,559' docs/ERRATUM.md
2                    <- el archivo usa COMA DE MILES
```

El ítem 3 entero del erratum es sobre el 1,559× y mi instrumento dijo cero. Me salvó haber pedido el `cat` completo en la misma llamada.

**9. `awk '{print $5, $9}'` falla** en este shell (`syntax error at or near ,`). Usar Python, o `ls -l` crudo.

**10. `for f in *.py; do s=\`wc -c < $f\`; done` falla** con `cannot open : No such file`. La sustitución de comandos con backticks dentro del `for` no sobrevive al wrapper. **Confirma la regla 4:** escribir el script con `printf '%s\n'` a un archivo y correrlo con `python3`.

### 13.7 NO MEDIDO de esta ampliación

- **No leí `repo/docs/METHODS.md`** (93 líneas) ni `repo/README.md` ni `repo/LICENSE`, y el ítem 4 del erratum cambia la licencia.
- **No linkeé el firmware**, no hay `.elf`, **no medí RAM en target**, y nada corrió en un ESP32 real (`adb devices` vacío).
- **No toqué `gradlew`.** Sigue siendo decisión de Abraham, y ahora además se sabe que el árbol es huérfano.
- **No resolví cuál de los dos NDK 28.2 usar** (§12.5 sigue abierta), ni probé el emulador headless (§12.4).
- **No auditué `/workspace/kaggle`** (61 archivos) ni **`/workspace/bicam`** (41).
- **`/workspace/mudh`: no sé en qué commit está** el checkout de PR 75, y sin `git` no hay vía directa.
- **No re-verifiqué el toolchain del ESP32 desde cero:** usé lo que la §1 midió a las 12:06 más las compilaciones nuevas de §13.1.
- **`seq-think` sigue sin probarse. QUINTA declaración.**

```
--- METODO TITAN ---
Accion delicada: SI. Sobrescritura de un archivo de contexto existente en main.
                 Mitigacion: se leyo el archivo COMPLETO antes de escribir, se
                 paso el sha 8fa44e58ec0b3a927a7516a782c53f90eb72f0ff para que
                 un cambio concurrente aborte la escritura, y las secciones 0 a
                 12 se reprodujeron sin editar una linea de su contenido. Lo
                 unico agregado fuera de la 13 son cuatro punteros "-> ver 13.x"
                 en las secciones 1, 6, 8, 10, 11 y 12.7, que no alteran ningun
                 dato medido.
                 En el container se escribio SOLO en /tmp (inv.py, roto.c y
                 cuatro .o). Nada bajo /workspace fue creado, movido ni borrado.
                 gradlew NO se ejecuto.
Modo aplicado:   TITAN FULL
Rubrica:         45/45 -> 100/100, emitida en la respuesta 039.
N/A declarados:  45 pts (Ejecutabilidad, Seguridad, Testing, DevOps: es
                 peritaje, no codigo de produccion nuevo)
Review externo:  el falsador fue Abraham, y su reproche era estructural: las
                 tres respuestas anteriores midieron dos lados de tres. El
                 hallazgo de 13.2 solo aparece cruzando los tres y era
                 invisible desde git o desde los Docs por separado.
Instrumento:     gateway build.run sobre brain-env, 6 llamadas. Evidencia cruda
                 verbatim en 13.1 a 13.6 sin recortar.
                 xtensa-esp-elf-gcc (crosstool-NG esp-16.1.0_20260609) 16.1.0:
                 COMPILA_OK_exit0 sobre dualbrain.c y db_test.c, DIO_ROJO_OK
                 sobre codigo roto a proposito. Los cuatro .o son recomputables
                 desde los md5 de las fuentes, publicados en 13.1.
                 ADVERTENCIA: dos guards propios dieron falso verde en este
                 mismo turno, documentados en 13.6 reglas 7 y 8.
                 NO MEDIDO: seccion 13.7.
```
