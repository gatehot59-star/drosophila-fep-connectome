"""W-01: el control de instrumento.

La corrida CPU del container y los 4 shards GPU de Kaggle son DOS instrumentos
distintos: maquina distinta, backend distinto (scipy vs cupy), SpMV distinto.
Si el mismo indice de null da el mismo numero en los dos, el resultado no depende
del aparato, y deja de haber un unico testigo.

No se compara "a ojo": se parean por indice global y se mide el desvio maximo.
El contador del log del container es 1-based (CP 17/39 == indice global 16).

Corrido en brain-env el 2026-08-26. Salida verbatim en
docs/agents/evidencia/2026-08-26-102-identidad-del-kernel-y-cruce-cpu-gpu.md
"""
import json, re, glob

# --- lado GPU: los 4 shards ---
gpu = {}
real_gpu = None
for p in sorted(glob.glob("/workspace/kshards/shard*_shard_*.json")):
    j = json.load(open(p))
    for k, v in j["nulls"].items():
        gpu[int(k)] = v["rdi_Wc_tauC_t149"]
    if j.get("real"):
        real_gpu = j["real"]["rdi_Wc_tauC_t149"]

# --- lado CPU: el log del container ---
txt = open("/workspace/motor_v2_real.log", encoding="utf-8", errors="replace").read()
cpu = {}
for m in re.finditer(r"CP\s+(\d+)/39\s+.*?rdi\(Wc,tauC\)=([\d.\-]+)", txt):
    cpu[int(m.group(1))] = float(m.group(2))
mr = re.search(r"REAL\s+.*?rdi\(Wc,tauC\)=([\d.\-]+)", txt)
real_cpu = float(mr.group(1)) if mr else None

print("=" * 88)
print("CONTROL DE INSTRUMENTO  \u00b7  CPU (container) contra GPU (Kaggle P100)")
print("=" * 88)
print("\n  nulls medidos en GPU : %d" % len(gpu))
print("  nulls medidos en CPU : %d  (etiquetas %s..%s)" % (len(cpu), min(cpu) if cpu else "-", max(cpu) if cpu else "-"))
print("  REAL  CPU=%s   GPU=%s" % (real_cpu, real_gpu))

print("\n  %-6s %-12s %-12s %-12s" % ("idx", "GPU", "CPU", "|dif|"))
difs = []
for et in sorted(cpu):
    idx = et - 1
    if idx in gpu:
        d = abs(gpu[idx] - cpu[et])
        difs.append((idx, gpu[idx], cpu[et], d))
for idx, g, c, d in difs:
    print("  %-6d %-12.4f %-12.4f %-12.2e %s" % (idx, g, c, d, "COINCIDE" if d < 5e-5 else "DIFIERE"))
print("\n  pares comparables: %d" % len(difs))
if difs:
    mx = max(d for _, _, _, d in difs)
    print("  desvio maximo entre CPU y GPU: %.3e" % mx)
    print("  VEREDICTO: %s" % ("los dos instrumentos coinciden dentro del redondeo del log (4 decimales)"
                               if mx < 5e-5 else "DIFIEREN: el resultado depende del aparato"))
    if real_cpu is not None:
        print("  REAL: |CPU - GPU| = %.3e" % abs(real_cpu - real_gpu))
else:
    print("  NO MEDIDO: el pareo por indice no encontro solapamiento.")
