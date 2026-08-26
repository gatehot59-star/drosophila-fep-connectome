#!/usr/bin/env python3
"""Mide hardware, herramientas y paralelismo real de la maquina donde corre.

El mismo archivo se ejecuta en `brain-env` y en el runner de GitHub Actions.
Esa es la razon de que exista: si cada maquina se mide con un script distinto,
la diferencia observada puede ser del script y no de la maquina.

Uso:
    python3 tools/probe_maquina.py            # imprime a stdout
    python3 tools/probe_maquina.py salida.txt # y ademas escribe el archivo

No importa nada fuera de la biblioteca estandar, para poder correr en una
maquina recien creada sin instalar nada.
"""
from __future__ import annotations

import multiprocessing
import os
import platform
import shutil
import socket
import subprocess
import sys
import time

# Los binarios que separan al runner de Actions de brain-env, mas los basicos.
BINARIOS = [
    "gcc", "cc", "g++", "gfortran", "clang",
    "git", "ps", "pgrep", "top", "free", "lsof",
    "docker", "podman", "buildah", "skopeo",
    "gradle", "java", "javac", "kotlinc",
    "cmake", "ninja", "bazel", "make",
    "jq", "yq", "gh", "unzip", "zip", "wget", "curl", "less", "rsync",
    "sqlite3", "psql", "mysql",
    "google-chrome", "chromium", "firefox", "chromedriver", "geckodriver",
    "aws", "az", "gcloud", "helm", "kubectl", "minikube", "pulumi",
    "packer", "ansible", "terraform",
    "cargo", "rustc", "node", "npm", "python3", "pip3", "uv",
    "nvidia-smi", "xtensa-esp32-elf-gcc", "riscv32-esp-elf-gcc", "qemu-system-arm",
]

MODULOS = [
    "numpy", "scipy", "pandas", "pyarrow", "matplotlib", "networkx",
    "psutil", "requests", "cupy", "dulwich", "arcengine", "sklearn",
]


def _leer(ruta: str) -> str:
    """Lee un archivo de texto y devuelve cadena vacia si no se puede."""
    try:
        with open(ruta, "r", encoding="utf-8", errors="replace") as fh:
            return fh.read()
    except OSError:
        return ""


def seccion_identidad() -> list[str]:
    """Devuelve las lineas de identidad de la maquina."""
    out = ["===== IDENTIDAD ====="]
    out.append(f"hostname   : {socket.gethostname()}")
    out.append(f"platform   : {platform.platform()}")
    out.append(f"machine    : {platform.machine()}")
    out.append(f"python     : {sys.version.split()[0]} ({sys.executable})")
    out.append(f"uid/gid    : {os.getuid()}/{os.getgid()}")
    # Variables que solo existen dentro de un runner de Actions.
    for var in ("GITHUB_ACTIONS", "RUNNER_OS", "RUNNER_ARCH",
                "ImageOS", "ImageVersion", "ANDROID_HOME"):
        out.append(f"{var:<11}: {os.environ.get(var, '(vacio)')}")
    return out


def seccion_hardware() -> list[str]:
    """Devuelve las lineas de CPU, memoria y disco."""
    out = ["", "===== HARDWARE MEDIDO ====="]
    out.append(f"cpu_count  : {os.cpu_count()}")

    modelo = "(desconocido)"
    for linea in _leer("/proc/cpuinfo").splitlines():
        if "model name" in linea:
            modelo = linea.split(":", 1)[1].strip()
            break
    out.append(f"cpu_model  : {modelo}")

    meminfo = {}
    for linea in _leer("/proc/meminfo").splitlines():
        if ":" in linea:
            clave, valor = linea.split(":", 1)
            meminfo[clave.strip()] = valor.strip()
    for clave in ("MemTotal", "MemAvailable", "MemFree", "SwapTotal"):
        out.append(f"{clave:<11}: {meminfo.get(clave, '(no legible)')}")

    carga = _leer("/proc/loadavg").strip()
    out.append(f"loadavg    : {carga or '(no legible)'}")

    uptime = _leer("/proc/uptime").split()
    if uptime:
        out.append(f"uptime_min : {float(uptime[0]) / 60:.1f}")

    for punto in ("/", "/tmp", "/workspace", os.path.expanduser("~")):
        if os.path.isdir(punto):
            try:
                uso = shutil.disk_usage(punto)
                out.append(
                    f"disco {punto:<11} total={uso.total / 2**30:7.1f} GB "
                    f"libre={uso.free / 2**30:7.1f} GB"
                )
            except OSError:
                out.append(f"disco {punto:<11} (no medible)")
    return out


def seccion_binarios() -> list[str]:
    """Devuelve OK o FALTA por cada binario de la lista."""
    out = ["", "===== BINARIOS (OK / FALTA) ====="]
    presentes = 0
    for nombre in BINARIOS:
        ruta = shutil.which(nombre)
        if ruta:
            presentes += 1
            out.append(f"OK    {nombre:<22} {ruta}")
        else:
            out.append(f"FALTA {nombre:<22}")
    out.append(f"--- presentes: {presentes} de {len(BINARIOS)} ---")
    return out


def seccion_modulos() -> list[str]:
    """Devuelve la version de cada modulo de Python, o su ausencia."""
    out = ["", "===== MODULOS DE PYTHON ====="]
    for nombre in MODULOS:
        try:
            modulo = __import__(nombre)
            version = getattr(modulo, "__version__", "(sin __version__)")
            out.append(f"OK    {nombre:<12} {version}")
        except Exception as exc:            # noqa: BLE001 - queremos el motivo
            out.append(f"FALTA {nombre:<12} {type(exc).__name__}")
    return out


def seccion_versiones() -> list[str]:
    """Corre los binarios clave con su flag de version."""
    out = ["", "===== VERSIONES EJECUTADAS ====="]
    pruebas = [
        ("gcc", ["gcc", "--version"]),
        ("git", ["git", "--version"]),
        ("docker", ["docker", "--version"]),
        ("java", ["java", "-version"]),
        ("cmake", ["cmake", "--version"]),
        ("gh", ["gh", "--version"]),
        ("node", ["node", "--version"]),
    ]
    for etiqueta, comando in pruebas:
        if shutil.which(comando[0]) is None:
            out.append(f"{etiqueta:<8}: AUSENTE")
            continue
        try:
            proceso = subprocess.run(
                comando, capture_output=True, text=True, timeout=30, check=False
            )
            salida = (proceso.stdout + proceso.stderr).strip().splitlines()
            out.append(f"{etiqueta:<8}: {salida[0] if salida else '(sin salida)'}")
        except (OSError, subprocess.SubprocessError) as exc:
            out.append(f"{etiqueta:<8}: ERROR {type(exc).__name__}")
    return out


def _carga(n: int) -> float:
    """Trabajo puro de CPU, identico en cualquier maquina."""
    total = 0.0
    for i in range(1, n):
        total += (i ** 0.5) / i
    return total


def seccion_paralelismo(n: int = 2_000_000) -> list[str]:
    """Mide el speedup real usando todos los nucleos disponibles."""
    out = ["", "===== PARALELISMO REAL ====="]
    cpus = os.cpu_count() or 1

    inicio = time.perf_counter()
    _carga(n)
    serie = time.perf_counter() - inicio
    out.append(f"1 tarea en serie      : {serie:.3f} s")

    inicio = time.perf_counter()
    try:
        with multiprocessing.Pool(cpus) as pool:
            pool.map(_carga, [n] * cpus)
        paralelo = time.perf_counter() - inicio
        out.append(f"{cpus} tareas en paralelo : {paralelo:.3f} s")
        if paralelo > 0:
            out.append(f"speedup vs {cpus} en serie: {(serie * cpus) / paralelo:.2f}x")
        out.append(f"throughput            : {cpus / paralelo * n / 1e6:.2f} M iter/s")
    except (OSError, ValueError) as exc:
        out.append(f"pool fallo: {type(exc).__name__} {exc}")
    return out


def main() -> int:
    """Arma el informe completo, lo imprime y lo escribe si se pidio archivo."""
    lineas: list[str] = []
    lineas += seccion_identidad()
    lineas += seccion_hardware()
    lineas += seccion_binarios()
    lineas += seccion_modulos()
    lineas += seccion_versiones()
    lineas += seccion_paralelismo()

    texto = "\n".join(lineas)
    print(texto)

    if len(sys.argv) > 1:
        destino = sys.argv[1]
        with open(destino, "w", encoding="utf-8") as fh:
            fh.write(texto + "\n")
        print(f"\n[escrito en {destino}]")
    return 0


if __name__ == "__main__":
    sys.exit(main())
