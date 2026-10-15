import re
import sys


def limpiar(ruta):
    out = []
    for ln in open(ruta, encoding="utf-8").read().split(chr(10)):
        if ln.startswith("# maquina") or ln.startswith("# fecha") or ln.startswith("# HUMO"):
            continue
        ln = re.sub(" [|] [0-9.]+ s$", "", ln)
        ln = re.sub("EXIT_RUN=0 .*", "EXIT_RUN=0", ln)
        out.append(ln)
    return out


a, b = limpiar(sys.argv[1]), limpiar(sys.argv[2])
dif = [(i, x, y) for i, (x, y) in enumerate(zip(a, b)) if x != y]
print("COTEJO lineas=%d/%d distintas=%d -> %s" % (len(a), len(b), len(dif) + abs(len(a) - len(b)),
                                                  "IGUAL" if not dif and len(a) == len(b) else "DISTINTO"))
for i, x, y in dif[:5]:
    print("  %d A: %s" % (i, x[:150]))
    print("  %d B: %s" % (i, y[:150]))
