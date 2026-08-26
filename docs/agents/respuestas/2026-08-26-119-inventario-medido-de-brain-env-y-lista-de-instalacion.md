# 119 · Inventario re-medido de `brain-env` y qué falta instalar

**Medido:** 2026-08-26 · servicio `build` del gateway MUDH · `command -v` binario por binario + `psutil`

---

## 0. Cierro el NO MEDIDO que dejé abierto en la 118

En la 118 declaré que no podía ver procesos porque no hay `ps` ni `pgrep`. **Eso era el primer obstáculo, no el último.** `psutil` **sí está instalado**, y con eso se cierra:

```plain
LOAD (2.03, 2.19, 2.38)
TOTAL PROCS 57
  5644      0.5MB   3110.1min  adb -L tcp:5037 fork-server server --reply-fd 4
     1      0.0MB   4307.6min  sleep infinity
  1072      0.0MB   4270.9min  sh
  1099      0.0MB   4270.1min  R
  1609      0.0MB   4239.7min  python3
--- MATCHES NUESTROS (motor|kernel_shard|nm_core|ab39|dbc3|kaggle|rk_gpu|arc) ---
NINGUNO
```

**Veredicto medido:** **ninguna corrida nuestra está viva.** Lo que hay son 57 procesos, casi todos de 0,0 MB y ~71 horas de antigüedad (residuos, estado `R` sin cmdline), más el `adb fork-server` de 51,8 horas y el `sleep infinity` del PID 1 que mantiene el container.

Y la contradicción a explicar: **load ~2,0 con 2 CPUs y ningún proceso consumiendo RAM.** Eso apunta a los residuos, no a un job nuestro. **NO MEDIDO:** la causa exacta del load.

---

## 1. Lo que SÍ hay (para no volver a pedirlo)

**Soy root** (`uid=0`), y `apt-get` existe.

| categoría | presente |
|---|---|
| Python | `python3` 3.12.14 en `/usr/local/bin`, `pip3` |
| stack científico | **numpy 2.5.2 · scipy 1.18.1 · pandas 3.0.5 · pyarrow 25.0.1 · matplotlib 3.11.1 · networkx 3.6.1 · psutil · requests** |
| red | `curl` (en `/opt/mamba/bin`) |
| Node | v24.18.0 + `npm` |
| JVM | `java` (jdk17) |
| ESP32 | **`xtensa-esp32-elf-gcc` en `/opt/xtensa-esp-elf/bin`** |
| shell/base | `bash`, `grep`, `sed`, `awk`, `find`, `tar`, `make`, `kill` |
| recursos | **2 CPUs · 7,99 GB RAM (650 MB libres) · 157 GB libres en `/workspace`** |

**El stack científico de Python está completo. No hace falta un solo `pip install`.**

---

## 2. Lo que FALTA, medido y priorizado

### Crítico

1. **`git`** — FALTA. Es el bloqueante conceptual más grande: hoy el repo no se puede clonar adentro, así que cada script se transfiere por base64 y cada commit sale por la integración. Con `git` el container trabaja **contra el árbol real**.
2. **`procps`** (`ps`, `pgrep`, `pkill`, `top`, `free`, `uptime`, `vmstat`) — FALTA. Esto es lo que me falló **dos veces** al reportar procesos. `psutil` es una vuelta, no el arreglo.
3. **`build-essential`** (`gcc`, `cc`, `g++`) — FALTA. Existe el compilador cruzado de ESP32 pero **no hay compilador de host**: no se pueden correr tests nativos del C99 de DualBrain antes de cruzar a target.
4. **`unzip`** / `zip` — FALTA. Las salidas de Kaggle bajan comprimidas. Fricción real y repetida.

### Útil

5. **`jq`** — FALTA. Trabajamos con JSON de Kaggle todo el tiempo.
6. **`gh`** (GitHub CLI) — FALTA. Permitiría PRs y issues desde adentro sin depender de la integración.
7. **`wget`**, **`less`**, **`sqlite3`** (CLI) — FALTAN, prioridad baja: `curl` cubre el primero, `python3 -m sqlite3` el tercero.

### Lo que NO pido, y digo por qué

- **`cupy`**: no hay evidencia de GPU en este container (2 CPUs). Sin GPU no sirve para nada, y la GPU real la tenemos en Kaggle. **NO MEDIDO:** no corrí `nvidia-smi`.
- **`tmux`**: los jobs al fondo ya sobreviven entre llamadas. Medido y suficiente.

---

## 3. Un arreglo que NO es una instalación

La tool `run` del servicio `build` ejecuta con **`sh`** y **pre-expande `$`**. Consecuencias medidas hoy:

- los heredocs (`<<'PY'`) revientan con `Syntax error: "(" unexpected`
- un `for b in ...; do ... $b` imprime la variable **vacía**: dio 57 líneas de `OK` sin nombre

**`bash` ya está en `/usr/bin/bash`.** El arreglo es de configuración del wrapper del gateway, no de paquetes, y vale más que la mitad de la lista de arriba.

---

## 4. El comando

```sh
apt-get update && apt-get install -y git procps build-essential jq zip unzip wget less sqlite3
```

**Por qué te lo paso a vos y no lo corro yo, siendo root:** el 2026-08-22 un `apt-get install` desde adentro dejó el gateway en **502 en todos los servicios** (no solo `build`), y volvió solo a los minutos. Hoy hay **650 MB libres de 7,99 GB**. Con esa memoria y ese antecedente, esto se hace con la máquina tranquila y con vos mirando, no a ciegas en medio de una conversación.

---

## 5. NO MEDIDO

- **No corrí `nvidia-smi`**: no sé si hay GPU. Deduzco que no por los 2 CPUs, pero es inferencia, no medición.
- **No medi la causa del load ~2,0** con cero procesos pesados.
- **No probé si `pip3 install` funciona** (la instalación de paquetes de Python puede estar bloqueada por `EXTERNALLY-MANAGED`).
- **No verifiqué los 57 procesos uno por uno**: 50 de ellos no tenían cmdline legible.
- **No actualicé `CONTEXTO-ENTORNO.md`** con este inventario: conviene hacerlo **después** de la instalación, para que refleje el estado final y no uno intermedio.
