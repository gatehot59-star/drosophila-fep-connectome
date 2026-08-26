"""Cierre del control de instrumento con PRECISION COMPLETA.

El cruce anterior (tools/cruce_cpu_vs_gpu.py) estaba limitado por el redondeo del
log a 4 decimales: su "desvio maximo 4,975e-05" era exactamente el peor caso de
redondear, o sea que NO media el desvio, media el redondeo. Ahora existe el JSON
final de la corrida CPU, asi que se cruzan los dos JSON y las 12 metricas.

Corrido en brain-env el 2026-08-26. Salida verbatim en
docs/agents/evidencia/2026-08-26-104-cierre-39-nulls-y-test-global.md
"""
import json, glob

C = json.load(open("/workspace/motor_v2_real/motor_resultados.json"))
print("=" * 96)
print("CIERRE \u00b7 el JSON final de la corrida CPU, y el cruce de PRECISION COMPLETA contra GPU")
print("=" * 96)
print("\n[0] ESTRUCTURA DEL JSON CPU")
print("    claves raiz: %s" % ", ".join(list(C.keys())[:20]))

G, real_g = {}, None
for p in sorted(glob.glob("/workspace/kshards/shard*_shard_*.json")):
    j = json.load(open(p))
    for k, v in j["nulls"].items():
        G[int(k)] = v
    if j.get("real"):
        real_g = j["real"]

def find(d, names):
    for n in names:
        if n in d:
            return d[n]
    return None

nulls_c = find(C, ["nulls", "null", "nulos"])
real_c = find(C, ["real", "REAL"])
print("    nulls en el JSON CPU : %s" % (len(nulls_c) if nulls_c is not None else "NO ENCONTRADO"))
print("    real  en el JSON CPU : %s" % ("si" if real_c else "NO ENCONTRADO"))
if nulls_c is None:
    print("\n    claves completas: %s" % json.dumps(list(C.keys())))
    raise SystemExit(0)

if isinstance(nulls_c, dict):
    nulls_c = {int(k): v for k, v in nulls_c.items()}
else:
    nulls_c = {i: v for i, v in enumerate(nulls_c)}

claves = []
for t in [50, 100, 149]:
    claves += ["rdi_Wc_tauC_t%d" % t, "ventaja_tau_t%d" % t, "ventaja_W_t%d" % t, "interaccion_t%d" % t]

print("\n[1] CRUCE CPU vs GPU \u00b7 PRECISION COMPLETA \u00b7 las 12 metricas")
print("    %-22s %-9s %-14s %-14s %s" % ("metrica", "pares", "desvio_max", "desvio_medio", "veredicto"))
todo_ok = True
for k in claves:
    ds = []
    for i in sorted(set(nulls_c) & set(G)):
        a, b = nulls_c[i].get(k), G[i].get(k)
        if a is not None and b is not None:
            ds.append(abs(a - b))
    if not ds:
        print("    %-22s NO COMPARABLE" % k); todo_ok = False; continue
    mx, mu = max(ds), sum(ds) / len(ds)
    ok = mx < 1e-9
    todo_ok &= ok
    print("    %-22s %-9d %-14.3e %-14.3e %s" % (k, len(ds), mx, mu, "IDENTICO" if ok else ("difiere" if mx > 1e-6 else "casi")))

print("\n[2] EL BRAZO REAL, los dos lados")
for k in claves:
    a, b = (real_c or {}).get(k), (real_g or {}).get(k)
    if a is None or b is None: continue
    print("    %-22s CPU=%+.12f  GPU=%+.12f  |dif|=%.3e" % (k, a, b, abs(a - b)))

print("\n[3] TEST GLOBAL de la corrida CPU")
for key in ["test_global", "global", "S_real", "resumen"]:
    if key in C:
        print("    %s: %s" % (key, json.dumps(C[key])[:600]))

print("\n[4] VEREDICTO DEL CONTROL DE INSTRUMENTO")
print("    %s" % ("Las dos maquinas dan resultados IDENTICOS a 1e-9 en las 12 metricas."
                  if todo_ok else "Hay al menos una metrica que difiere: revisar arriba."))
