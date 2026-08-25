"""ci_mutate_guards.py - muta guards.py a proposito, para que el CI compruebe
que la bateria de tests PUEDE DAR ROJO.

Por que existe como archivo y no como heredoc dentro del workflow: la primera
version de .github/workflows/guards.yml embebia este codigo con
`python - <<'EOF'` indentado dentro de un bloque `run:`. Bash pasa las lineas
al stdin de python CON la indentacion del YAML, asi que python recibia
"          path = ..." y abortaba con IndentationError. Medido: el CI dio
failure en 6 de 6 corridas por ese motivo, no por la bateria.

La leccion, y es la de siempre en este repo: un paso de CI que falla por un bug
del paso, y no por lo que el paso mide, es un guard que no mide. Se arregla
sacando el codigo a un archivo con nombre, que ademas se puede correr a mano y
revisar en un diff.

Uso:
    python src/ci_mutate_guards.py mutate    # rompe la rama sd==0 a proposito
    python src/ci_mutate_guards.py restore   # deja el archivo como estaba

Sale con codigo distinto de cero si el ancla no aparece, porque una mutacion
que no muta deja pasar un CI en verde sobre un test que no puede fallar, que es
exactamente el antipatron que A-01 denuncia.
"""

import sys
import os
import shutil

TARGET = os.environ.get("DB_GUARDS_PATH", "src/guards.py")
BACKUP = os.environ.get("DB_GUARDS_BACKUP", "src/guards.py.orig")

# El ancla es la linea que distingue CONSERVADO de CENSURADO, o sea el corazon
# del hallazgo A-02. Mutarla equivale a volver al comportamiento denunciado.
ANCHOR = "        if abs(mu - r) <= float(atol):"
MUTATED = "        if True:  # MUTACION DE CI: comportamiento viejo de A-02"

EXIT_GUARD = 2


def fail(message):
    sys.stderr.write("GUARD_FAILED " + str(message) + "\n")
    sys.stderr.flush()
    raise SystemExit(EXIT_GUARD)


def mutate():
    """Guarda una copia intacta y rompe la rama sd==0."""
    if not os.path.exists(TARGET):
        fail("no existe " + TARGET)
    src = open(TARGET, encoding="utf-8").read()
    if ANCHOR not in src:
        fail("el ancla de mutacion ya no existe en " + TARGET
             + ". La mutacion del CI quedo obsoleta y hay que actualizarla,"
             " porque una mutacion que no muta deja pasar cualquier test.")
    shutil.copyfile(TARGET, BACKUP)
    open(TARGET, "w", encoding="utf-8").write(src.replace(ANCHOR, MUTATED, 1))
    sys.stdout.write("MUTACION_APLICADA sobre " + TARGET + "\n")
    sys.stdout.write("  respaldo intacto en " + BACKUP + "\n")
    return 0


def restore():
    """Devuelve el archivo original desde el respaldo."""
    if not os.path.exists(BACKUP):
        fail("no existe el respaldo " + BACKUP + ": no se puede restaurar")
    shutil.copyfile(BACKUP, TARGET)
    os.remove(BACKUP)
    sys.stdout.write("RESTAURADO " + TARGET + " desde el respaldo\n")
    return 0


def main(argv):
    if len(argv) != 2 or argv[1] not in ("mutate", "restore"):
        sys.stderr.write("uso: ci_mutate_guards.py mutate|restore\n")
        return EXIT_GUARD
    return mutate() if argv[1] == "mutate" else restore()


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
