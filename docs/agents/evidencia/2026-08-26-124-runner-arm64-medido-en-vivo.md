# Evidencia cruda - runner arm64 de GitHub Actions, MEDIDO EN VIVO

**Instrumento:** el propio runner de GitHub Actions. Este archivo
lo escribio el job, no BRAIN. Cualquiera puede reejecutar el
workflow y contradecirlo (W-01).

- workflow: .github/workflows/probe-entorno.yml
- runner solicitado: ubuntu-24.04-arm
- run: 33009493423 intento 1
- commit disparador: 64194b90f87a21032b16310d94256072bbf8fc5f

## Maquina, herramientas y paralelismo
```plain
===== IDENTIDAD =====
hostname   : runnervmpxp9w
platform   : Linux-6.17.0-1022-azure-aarch64-with-glibc2.39
machine    : aarch64
python     : 3.12.3 (/usr/bin/python3)
uid/gid    : 1001/1001
GITHUB_ACTIONS: true
RUNNER_OS  : Linux
RUNNER_ARCH: ARM64
ImageOS    : ubuntu24-arm64
ImageVersion: 20260817.96.1
ANDROID_HOME: (vacio)

===== HARDWARE MEDIDO =====
cpu_count  : 4
cpu_model  : (desconocido)
MemTotal   : 16330120 kB
MemAvailable: 15195516 kB
MemFree    : 14240476 kB
SwapTotal  : 3145724 kB
loadavg    : 0.28 0.09 0.03 1/244 2323
uptime_min : 9.5
disco /           total=  144.3 GB libre=  108.4 GB
disco /tmp        total=  144.3 GB libre=  108.4 GB
disco /home/runner total=  144.3 GB libre=  108.4 GB

===== BINARIOS (OK / FALTA) =====
OK    gcc                    /usr/bin/gcc
OK    cc                     /usr/bin/cc
OK    g++                    /usr/bin/g++
OK    gfortran               /usr/bin/gfortran
OK    clang                  /usr/bin/clang
OK    git                    /usr/bin/git
OK    ps                     /usr/bin/ps
OK    pgrep                  /usr/bin/pgrep
OK    top                    /usr/bin/top
OK    free                   /usr/bin/free
OK    lsof                   /usr/bin/lsof
OK    docker                 /usr/bin/docker
OK    podman                 /usr/local/bin/podman
OK    buildah                /usr/bin/buildah
OK    skopeo                 /usr/bin/skopeo
OK    gradle                 /usr/bin/gradle
OK    java                   /usr/bin/java
OK    javac                  /usr/bin/javac
OK    kotlinc                /usr/bin/kotlinc
OK    cmake                  /usr/local/bin/cmake
OK    ninja                  /usr/local/bin/ninja
OK    bazel                  /usr/local/bin/bazel
OK    make                   /usr/bin/make
OK    jq                     /usr/bin/jq
OK    yq                     /usr/bin/yq
OK    gh                     /usr/bin/gh
OK    unzip                  /usr/bin/unzip
OK    zip                    /usr/bin/zip
OK    wget                   /usr/bin/wget
OK    curl                   /usr/bin/curl
OK    less                   /usr/bin/less
OK    rsync                  /usr/bin/rsync
OK    sqlite3                /usr/bin/sqlite3
FALTA psql                  
OK    mysql                  /usr/bin/mysql
FALTA google-chrome         
FALTA chromium              
OK    firefox                /usr/bin/firefox
FALTA chromedriver          
OK    geckodriver            /usr/bin/geckodriver
OK    aws                    /usr/local/bin/aws
OK    az                     /usr/bin/az
OK    gcloud                 /usr/bin/gcloud
OK    helm                   /usr/local/bin/helm
OK    kubectl                /usr/bin/kubectl
OK    minikube               /usr/local/bin/minikube
OK    pulumi                 /usr/local/bin/pulumi
OK    packer                 /usr/local/bin/packer
OK    ansible                /opt/pipx_bin/ansible
FALTA terraform             
OK    cargo                  /home/runner/.cargo/bin/cargo
OK    rustc                  /home/runner/.cargo/bin/rustc
OK    node                   /usr/local/bin/node
OK    npm                    /usr/local/bin/npm
OK    python3                /usr/bin/python3
OK    pip3                   /usr/bin/pip3
FALTA uv                    
FALTA nvidia-smi            
FALTA xtensa-esp32-elf-gcc  
FALTA riscv32-esp-elf-gcc   
FALTA qemu-system-arm       
--- presentes: 51 de 61 ---

===== MODULOS DE PYTHON =====
FALTA numpy        ModuleNotFoundError
FALTA scipy        ModuleNotFoundError
FALTA pandas       ModuleNotFoundError
FALTA pyarrow      ModuleNotFoundError
FALTA matplotlib   ModuleNotFoundError
FALTA networkx     ModuleNotFoundError
FALTA psutil       ModuleNotFoundError
OK    requests     2.31.0
FALTA cupy         ModuleNotFoundError
FALTA dulwich      ModuleNotFoundError
FALTA arcengine    ModuleNotFoundError
FALTA sklearn      ModuleNotFoundError

===== VERSIONES EJECUTADAS =====
gcc     : gcc (Ubuntu 13.3.0-6ubuntu2~24.04.1) 13.3.0
git     : git version 2.55.0
docker  : Docker version 28.0.4, build b8034c0
java    : openjdk version "17.0.20" 2026-07-21
cmake   : cmake version 3.31.6
gh      : gh version 2.97.0 (2026-07-31)
node    : v22.23.2

===== PARALELISMO REAL =====
1 tarea en serie      : 0.192 s
4 tareas en paralelo : 0.204 s
speedup vs 4 en serie: 3.77x
throughput            : 39.31 M iter/s
```

## Compilacion C99 nativa (lo que brain-env no puede)
```plain
=== gcc -std=c99 -O2 -Wall -Wextra -Werror ===
exit_compilacion=0
=== ejecucion ===
gate_acc=2007
sizeof(int32_t)=4 sizeof(long)=8 sizeof(void*)=8
INT32_MAX=2147483647  INT32_MAX+1_en_int64=2147483648
pares_ordenados=19220633682  aristas_aprox=14918743
probe_c99 OK
exit_ejecucion=0
=== tamano del binario (lo mismo que medimos en ESP32) ===
   text	   data	    bss	    dec	    hex	filename
   2003	    640	      8	   2651	    a5b	probe_c99
```

## Docker
```plain
=== docker info ===
28.0.4 linux/aarch64
exit=0
=== docker run alpine ===
Unable to find image 'alpine:3.21' locally
3.21: Pulling from library/alpine
2dd7199cff98: Pulling fs layer
2dd7199cff98: Verifying Checksum
2dd7199cff98: Download complete
2dd7199cff98: Pull complete
Digest: sha256:48b0309ca019d89d40f670aa1bc06e426dc0931948452e8491e3d65087abc07d
Status: Downloaded newer image for alpine:3.21
dentro-del-container
aarch64
exit=0
```
