"""AUDITORIA v1 vs v2, paso 1: el inventario de funciones.

No se razona sobre el mapa: se listan las firmas y se comparan los cuerpos por md5.
Corrido en brain-env el 2026-08-26. Salida verbatim en
docs/agents/evidencia/2026-08-26-105-auditoria-v1-vs-v2-evidencia-cruda.md
"""
import re, hashlib

v1 = open("/workspace/motor.py").read()
v2 = open("/workspace/motor_v2.py").read()

def sigs(src):
    out = {}
    for m in re.finditer(r"^(def|class)\s+(\w+)\s*\(([^)]*)\)", src, re.M | re.S):
        out[m.group(2)] = " ".join(m.group(3).split())
    return out

def bodies(src):
    """Cuerpo de cada def, desde su linea hasta el proximo def/class de nivel 0."""
    idx = [(m.start(), m.group(2)) for m in re.finditer(r"^(def|class)\s+(\w+)", src, re.M)]
    out = {}
    for i, (s, name) in enumerate(idx):
        e = idx[i + 1][0] if i + 1 < len(idx) else len(src)
        out[name] = src[s:e]
    return out

s1, s2 = sigs(v1), sigs(v2)
b1, b2 = bodies(v1), bodies(v2)

print("=" * 100)
print("AUDITORIA motor.py (v1) vs motor_v2.py  \u00b7  PASO 1: inventario de funciones")
print("=" * 100)
print("\n  v1: %d funciones/clases   v2: %d" % (len(s1), len(s2)))

comunes = sorted(set(s1) & set(s2))
solo1 = sorted(set(s1) - set(s2))
solo2 = sorted(set(s2) - set(s1))

print("\n[A] SOLO EN v1 (%d) -> desaparecieron o se renombraron" % len(solo1))
for n in solo1:
    print("    %-38s (%s)" % (n, s1[n][:60]))

print("\n[B] SOLO EN v2 (%d) -> capacidades NUEVAS" % len(solo2))
for n in solo2:
    print("    %-38s (%s)" % (n, s2[n][:70]))

print("\n[C] COMUNES (%d): identicas, o cambiaron?" % len(comunes))
print("    %-32s %-10s %-8s %-8s %s" % ("funcion", "cuerpo", "lineas1", "lineas2", "firma cambio?"))
cambiadas = []
for n in comunes:
    h1 = hashlib.md5(b1[n].encode()).hexdigest()
    h2 = hashlib.md5(b2[n].encode()).hexdigest()
    ig = h1 == h2
    l1, l2 = b1[n].count("\n"), b2[n].count("\n")
    fc = "NO" if s1[n] == s2[n] else "SI"
    if not ig:
        cambiadas.append(n)
    print("    %-32s %-10s %-8d %-8d %s" % (n, "IGUAL" if ig else "CAMBIO", l1, l2, fc))

print("\n  identicas: %d   cambiadas: %d" % (len(comunes) - len(cambiadas), len(cambiadas)))

print("\n[D] LAS FIRMAS QUE CAMBIARON (contrato distinto)")
for n in comunes:
    if s1[n] != s2[n]:
        print("    %s" % n)
        print("       v1: (%s)" % s1[n][:150])
        print("       v2: (%s)" % s2[n][:150])
