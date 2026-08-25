"""run_ci_local.py - corre el job de CI EN LOCAL, leyendo el workflow real.

Por que existe, y es la unica razon que importa: el job de guards dio ROJO cuatro
veces seguidas, y las cuatro causas eran condiciones que el banco de pruebas local
NO reproducia. La cuarta es el ejemplo exacto: se probo "el ciclo completo, los
siete pasos" en un directorio que no era un repo git, asi que el paso que mide
`git status --porcelain` nunca se ejecuto, y se declaro verificado igual.

El ciclo de descubrimiento era: escribir el YAML -> push -> esperar el runner ->
consultar la API para ver el resultado. Ese ultimo paso quemo 60 llamadas de una
cuota compartida y aun asi no decia POR QUE fallaba. Este script reemplaza el ciclo
entero por una corrida local de segundos.

LA DECISION DE DISENO QUE LO HACE UTIL: no reimplementa los pasos del CI, los LEE
del archivo del workflow. Una copia local escrita a mano se desincroniza del CI
real en el primer cambio, y entonces vuelve a medir otra cosa que el CI. Aca, si
alguien edita guards.yml, este script corre lo editado.

Lo que reproduce del entorno del runner:
  - clon FRESCO: repo git nuevo, con solo los archivos que el repo trackea, y un
    commit base. Asi el paso que exige arbol limpio tiene un arbol que medir.
  - el bloque `env:` del job, aplicado a cada paso.
  - `bash -e` por paso, que es como Actions ejecuta un `run:`.

Lo que NO reproduce, declarado:
  - los pasos con `uses:` (checkout, setup-python). Se listan como OMITIDOS y no
    se simulan: el checkout lo hace el propio armado del repo fresco.
  - la version exacta de python del runner ni su sistema operativo.
  - cualquier cosa que dependa de la red o de secretos. Si el job instalara
    dependencias, un sandbox sin red daria rojo por falta de red y no por el
    paquete: el arnes lo CATCHEA pero no lo DIAGNOSTICA.
  Asi que un verde local NO sustituye al CI: lo ADELANTA. El CI sigue siendo el
  testigo, este script es el ensayo.

Uso:
    python3 tools/run_ci_local.py                    # corre el job
    python3 tools/run_ci_local.py --keep             # deja el directorio temporal
    python3 tools/run_ci_local.py --break-pycache    # AUTOPRUEBA: quita
        PYTHONDONTWRITEBYTECODE del env y verifica que el arnes detecta el bug 4.
        Si con esa mutacion el arnes da VERDE, el arnes no mide y aborta con 2.
        (Medido: da 2 mientras exista el .gitignore, porque el .gitignore tapa el
        __pycache__ por su cuenta. Ver la evidencia cruda.)
"""

import os
import re
import shutil
import subprocess
import sys
import tempfile

EXIT_GUARD = 2
WORKFLOW = os.environ.get("DB_WORKFLOW", ".github/workflows/guards.yml")


def lg(msg):
    sys.stdout.write(str(msg) + "\n")
    sys.stdout.flush()


def fail(message):
    sys.stderr.write("GUARD_FAILED " + str(message) + "\n")
    sys.stderr.flush()
    raise SystemExit(EXIT_GUARD)


def parse_workflow(path):
    """Extrae el env del job y la lista ordenada de pasos con su script.

    Parser minimo a proposito: cubre el subconjunto de sintaxis que este workflow
    usa y NADA mas. Lleva tres guards para no leer de menos en silencio, que es la
    forma en que un parser casero miente.
    """
    if not os.path.exists(path):
        fail("no existe el workflow " + path)
    lines = open(path, encoding="utf-8").read().splitlines()

    env = {}
    steps = []            # (nombre, tipo, script)
    in_env = False
    cur = None            # paso en construccion
    body = []             # lineas del bloque run:
    run_indent = None

    def close_step():
        if cur is None:
            return
        kind, name = cur
        if kind == "run":
            steps.append((name, "run", "\n".join(body)))
        else:
            steps.append((name, kind, ""))

    for raw in lines:
        line = raw.rstrip("\n")
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            if (cur is not None and cur[0] == "run"
                    and line.startswith(" " * (run_indent or 999))):
                body.append(line[run_indent:])
            continue

        indent = len(line) - len(line.lstrip())

        # bloque env: del job (indentado 4, sus claves a 6)
        if stripped == "env:" and indent == 4:
            in_env = True
            continue
        if in_env:
            m = re.match(r"^\s{6}([A-Za-z_][A-Za-z0-9_]*):\s*(.*)$", line)
            if m:
                env[m.group(1)] = m.group(2).strip().strip("'\"")
                continue
            if indent <= 4:
                in_env = False

        # comienzo de un paso
        m = re.match(r"^\s{6}-\s+name:\s*(.+)$", line)
        if m:
            close_step()
            cur = ("pendiente", m.group(1).strip())
            body = []
            run_indent = None
            continue

        if cur is not None:
            if re.match(r"^\s{8}uses:\s*", line):
                cur = ("uses", cur[1])
                continue
            m = re.match(r"^\s{8}run:\s*(\|?)\s*(.*)$", line)
            if m:
                cur = ("run", cur[1])
                body = []
                if m.group(1) == "|":
                    run_indent = 10
                else:
                    body = [m.group(2)]
                    run_indent = None
                continue
            if run_indent is not None and cur[0] == "run" and indent >= run_indent:
                body.append(line[run_indent:])
                continue
            if indent <= 8 and cur[0] == "run":
                close_step()
                cur = None
                body = []
                run_indent = None

    close_step()

    # GUARD 1: si no encontro pasos, el parser no sirve.
    if not steps:
        fail("el parser no encontro ningun paso en " + path
             + ". Un arnes que corre cero pasos y dice verde es peor que no tenerlo.")

    # GUARD 2: contar los `- name:` del archivo y exigir que coincidan.
    declared = len([1 for l in lines if re.match(r"^\s{6}-\s+name:", l)])
    if declared != len(steps):
        fail("el parser leyo " + str(len(steps)) + " pasos y el archivo declara "
             + str(declared) + ". Se perdio al menos un paso en silencio.")

    # GUARD 3: todo paso `run` tiene que tener script.
    for name, kind, script in steps:
        if kind == "run" and not script.strip():
            fail("el paso " + repr(name) + " es run: y quedo con script vacio")

    return env, steps


def build_fresh_repo(dst):
    """Arma un repo git nuevo con los archivos TRACKEADOS del repo actual."""
    tracked = subprocess.run(["git", "ls-files"], capture_output=True, text=True)
    if tracked.returncode != 0:
        fail("no estoy dentro de un repo git: `git ls-files` devolvio "
             + str(tracked.returncode))
    files = [f for f in tracked.stdout.splitlines() if f.strip()]
    if not files:
        fail("`git ls-files` no devolvio archivos")
    for f in files:
        if not os.path.exists(f):
            continue
        target = os.path.join(dst, f)
        os.makedirs(os.path.dirname(target) or dst, exist_ok=True)
        shutil.copyfile(f, target)
    for cmd in (["git", "init", "-q", "."],
                ["git", "add", "-A"],
                ["git", "-c", "user.email=ci@local", "-c", "user.name=ci",
                 "commit", "-qm", "base"]):
        r = subprocess.run(cmd, cwd=dst, capture_output=True, text=True)
        if r.returncode != 0:
            fail("fallo " + " ".join(cmd) + ": " + r.stderr.strip()[:200])
    dirty = subprocess.run(["git", "status", "--porcelain"], cwd=dst,
                           capture_output=True, text=True)
    if dirty.stdout.strip():
        fail("el repo fresco arranca SUCIO, el paso de arbol limpio no mediria nada:\n"
             + dirty.stdout)
    return len(files)


def run_job(env_extra, steps, workdir):
    """Corre cada paso `run` con bash -e. Devuelve la lista de (nombre, rc)."""
    env = dict(os.environ)
    env.update(env_extra)
    env["CI"] = "true"
    results = []
    for name, kind, script in steps:
        if kind != "run":
            lg("  OMITIDO (uses:)  " + name)
            continue
        p = subprocess.run(["bash", "-e", "-c", script], cwd=workdir,
                           capture_output=True, text=True, env=env)
        mark = "OK  " if p.returncode == 0 else "ROJO"
        lg("  " + mark + " rc=" + str(p.returncode) + "  " + name)
        if p.returncode != 0:
            out = (p.stdout + p.stderr).strip().splitlines()
            for l in out[-8:]:
                lg("        | " + l)
        results.append((name, p.returncode))
    return results


def main(argv):
    keep = "--keep" in argv
    break_pycache = "--break-pycache" in argv

    lg("=== run_ci_local  ---  corre el job de CI leyendo el workflow real ===")
    lg("workflow = " + WORKFLOW)
    env, steps = parse_workflow(WORKFLOW)
    lg("env del job: " + (", ".join(k + "=" + v for k, v in env.items()) or "(vacio)"))
    lg("pasos leidos: " + str(len(steps))
       + "  (run: " + str(len([s for s in steps if s[1] == "run"]))
       + ", uses: " + str(len([s for s in steps if s[1] == "uses"])) + ")")

    if break_pycache:
        removed = env.pop("PYTHONDONTWRITEBYTECODE", None)
        lg("")
        lg("*** AUTOPRUEBA --break-pycache: se quita PYTHONDONTWRITEBYTECODE"
           + ((" (valia " + str(removed) + ")") if removed else " (NO ESTABA)"))
        if removed is None:
            fail("el workflow ya no define PYTHONDONTWRITEBYTECODE, asi que esta"
                 " autoprueba no puede reproducir el bug 4 y no mide nada.")
        lg("*** se espera que el arnes detecte ROJO en el paso del arbol limpio")

    tmp = tempfile.mkdtemp(prefix="ci_local_")
    try:
        n = build_fresh_repo(tmp)
        lg("repo fresco en " + (tmp if keep else "(temporal)")
           + " con " + str(n) + " archivos trackeados, arbol limpio")
        lg("")
        results = run_job(env, steps, tmp)
    finally:
        if keep:
            lg("")
            lg("directorio conservado: " + tmp)
        else:
            shutil.rmtree(tmp, ignore_errors=True)

    reds = [n for n, rc in results if rc != 0]
    lg("")
    lg("=== RESUMEN ===")
    lg("pasos run corridos: " + str(len(results)) + "   en rojo: " + str(len(reds)))
    for n in reds:
        lg("   ROJO: " + n)

    if break_pycache:
        if reds:
            lg("")
            lg("AUTOPRUEBA OK: el arnes detecta el bug 4 EN LOCAL. Puede dar rojo.")
            return 0
        fail("AUTOPRUEBA FALLIDA: con el bug 4 reintroducido el arnes dio VERDE."
             " Un arnes que no puede dar rojo no adelanta nada.")

    if reds:
        lg("")
        lg("VEREDICTO: el job fallaria en el CI. Arreglar antes de pushear.")
        return 1
    lg("")
    lg("VEREDICTO: el job pasa en local. El CI sigue siendo el testigo.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
