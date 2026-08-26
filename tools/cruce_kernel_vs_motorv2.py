"""E-01: verificar el SUJETO EXACTO que corrio en Kaggle.

Pregunta: kernel_shard.py, es motor_v2.py + un parche, o es otra cosa?
Y el parche, REEMPLAZA el nucleo o solo lo acelera?

No se razona sobre el mapa: se compara byte por byte y se listan los def duplicados.
Motivo: el peritaje 092 ya se comio un caso de medir una primitiva y concluir sobre
el llamador. Antes de decir "corri la version corregida", hay que probar que el
archivo que corrio ES la version corregida.

Corrido en brain-env el 2026-08-26. Salida verbatim en
docs/agents/evidencia/2026-08-26-102-identidad-del-kernel-y-cruce-cpu-gpu.md
"""
import hashlib, re, difflib

K = open("/workspace/kernel_shard.py", "r", encoding="utf-8").read()
V = open("/workspace/motor_v2.py", "r", encoding="utf-8").read()
M = open("/workspace/motor.py", "r", encoding="utf-8").read()

md5 = lambda s: hashlib.md5(s.encode("utf-8")).hexdigest()
print("=" * 90)
print("QUE CORRIO EN KAGGLE  \u00b7  cruce byte a byte contra motor_v2 y contra motor v1")
print("=" * 90)
print("\n[1] LOS TRES ARCHIVOS")
for n, s in [("motor.py (v1)", M), ("motor_v2.py", V), ("kernel_shard.py", K)]:
    print("    %-16s %7d B  %5d lineas  md5=%s" % (n, len(s.encode()), s.count("\n") + 1, md5(s)))

print("\n[2] ESTA motor_v2 ADENTRO DEL KERNEL, VERBATIM?")
marca = "# PARCHE GPU + CORREDOR DE SHARD"
i = K.find(marca)
print("    marca del parche en offset de caracter: %s" % i)
cuerpo = K[:i]
pos = K.find(V[:200])
print("    los primeros 200 caracteres de motor_v2 aparecen en el kernel en: %s" % pos)
if pos >= 0:
    seg = K[pos:pos + len(V)]
    print("    segmento de igual largo desde ahi:  identico a motor_v2? %s" % (seg == V))
    if seg != V:
        sm = difflib.SequenceMatcher(None, V, seg)
        print("    similitud del segmento con motor_v2: %.4f" % sm.ratio())
print("    cabecera del kernel ANTES de motor_v2 (%d caracteres):" % max(pos, 0))
print("    " + repr(K[:pos if pos > 0 else 0][:400]))

print("\n[3] EL CUERPO PRE-PARCHE contra motor_v2")
print("    pre-parche: %d caracteres   motor_v2: %d caracteres   diferencia: %+d"
      % (len(cuerpo), len(V), len(cuerpo) - len(V)))
sm = difflib.SequenceMatcher(None, V, cuerpo)
print("    similitud pre-parche vs motor_v2: %.4f" % sm.ratio())
ops = [o for o in sm.get_opcodes() if o[0] != "equal"]
print("    bloques de diferencia: %d" % len(ops))
for tag, i1, i2, j1, j2 in ops[:12]:
    a = V[i1:i2].replace("\n", "\\n")[:110]
    b = cuerpo[j1:j2].replace("\n", "\\n")[:110]
    print("      %-8s v2[%6d:%6d]=%-112s  ker[%6d:%6d]=%s" % (tag, i1, i2, a, j1, j2, b))

print("\n[4] EL PARCHE: que funciones DEFINE, y cuales PISAN a las del motor")
def defs(src):
    return re.findall(r"^(?:def|class)\s+(\w+)", src, re.M)
d_v2 = defs(V)
d_pre = defs(cuerpo)
d_par = defs(K[i:])
print("    defs en motor_v2      : %d" % len(d_v2))
print("    defs en el pre-parche : %d" % len(d_pre))
print("    defs en el parche GPU : %d  -> %s" % (len(d_par), ", ".join(d_par)))
pisadas = [x for x in d_par if x in d_pre]
print("\n    *** REDEFINICIONES (el parche PISA una funcion del motor): %d" % len(pisadas))
for p in pisadas:
    print("        %s" % p)
nuevas = [x for x in d_par if x not in d_pre]
print("    funciones NUEVAS del parche: %s" % ", ".join(nuevas))

print("\n[5] EL NUCLEO: hay dos propagate?")
for name in ["propagate", "propagate_gpu", "rdi", "cosine_distance", "normalize_spectral",
             "null_configuration_preserving", "null_maslov_sneppen", "build_weights"]:
    n_pre = len(re.findall(r"^(?:def)\s+%s\b" % name, cuerpo, re.M))
    n_par = len(re.findall(r"^(?:def)\s+%s\b" % name, K[i:], re.M))
    print("    %-32s pre-parche=%d  parche=%d  %s"
          % (name, n_pre, n_par, "<<< DOS VERSIONES" if n_pre and n_par else ""))

print("\n[6] QUE main SE EJECUTA")
mains = [(m.start(), m.group(0)) for m in re.finditer(r"^if __name__.*$", K, re.M)]
print("    bloques '__main__' en el kernel: %d" % len(mains))
for off, txt in mains:
    zona = "PRE-parche (motor v2)" if off < i else "PARCHE (corredor de shard)"
    print("      offset %6d  %s   -> %s" % (off, txt.strip(), zona))
print("    el ultimo en ejecutarse gana: %s" % ("PARCHE" if mains and mains[-1][0] > i else "MOTOR V2"))
