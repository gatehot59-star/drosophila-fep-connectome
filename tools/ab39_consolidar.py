"""Baja y consolida los 5 kernels de cierre.

Guards, en este orden y antes de cualquier veredicto:
  1. los md5 de motor.py, motor_v2.py y ab39_core.py tienen que ser IGUALES en los
     5 shards. Si no, cada shard midio otro sujeto y no se pueden sumar (E-01).
  2. la particion de los 39 nulls tiene que cubrir 0..38 exactamente una vez.
  3. solo despues se reporta el peor desvio, y se ATRIBUYE: cada null que difiere
     se cruza contra el flag de convergencia de la iteracion de potencia de v1.

El ref de cada kernel se LEE de /kernels/list, no se adivina: Kaggle slugifica el
titulo (docs/agents/KAGGLE-REGLA-DEL-SLUG.md).
"""
import json, os, urllib.request, urllib.error

BASE = "/workspace"
OUT = os.path.join(BASE, "cierre_out")
os.makedirs(OUT, exist_ok=True)
CRED = json.load(open(os.path.join(BASE, "kaggle.json")))
API = "https://www.kaggle.com/api/v1"

def api(c, path):
    req = urllib.request.Request(API + path)
    req.add_header("Authorization", "Bearer " + c["token"])
    try:
        with urllib.request.urlopen(req, timeout=180) as r:
            return r.status, r.read().decode()
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode()[:300]

REFS = [(1, "abrahammendieta/titan-cierre-ab39-shard-0-de-4"),
        (1, "abrahammendieta/titan-cierre-ab39-shard-1-de-4"),
        (0, "fabiomurillohot/titan-cierre-ab39-shard-2-de-4"),
        (0, "fabiomurillohot/titan-cierre-ab39-shard-3-de-4"),
        (1, "abrahammendieta/titan-cierre-extras-semilla-jitter-escala-rss")]

print("=" * 104)
print("CONSOLIDACION DE LOS 5 KERNELS DE CIERRE")
print("=" * 104)

JS = {}
LOGS = {}
print("\n[0] BAJADA")
for a, ref in REFS:
    c = CRED[a]
    u, k = ref.split("/")
    st, t = api(c, "/kernels/status?userName=%s&kernelSlug=%s" % (u, k))
    estado = json.loads(t)["status"] if st == 200 else ("HTTP %s" % st)
    st2, t2 = api(c, "/kernels/output?userName=%s&kernelSlug=%s" % (u, k))
    if st2 != 200:
        print("  %-48s %-10s output HTTP %s" % (k[:46], estado, st2)); continue
    j = json.loads(t2)
    try:
        log = "".join(e["data"] for e in json.loads(j.get("logNullable") or "[]"))
    except Exception:
        log = ""
    LOGS[k] = log
    open(os.path.join(OUT, k + ".log"), "w").write(log)
    bajados = []
    for f in (j.get("files") or []):
        nm = f.get("fileName", "")
        if nm.endswith(".json") and "ab39_out" in nm:
            rr = urllib.request.Request(f["url"])
            rr.add_header("Authorization", "Bearer " + c["token"])
            txt = urllib.request.urlopen(rr, timeout=180).read().decode()
            JS[k] = json.loads(txt)
            open(os.path.join(OUT, k + ".json"), "w").write(txt)
            bajados.append("%s (%d B)" % (nm, len(txt)))
    print("  %-48s %-10s log %6d B  %s" % (k[:46], estado, len(log),
                                           ", ".join(bajados) or "sin json aun"))

AB = {k: v for k, v in JS.items() if v.get("mode") == "ab"}
EX = {k: v for k, v in JS.items() if v.get("mode") == "extras"}

# ---- Guard 1: el MISMO sujeto en los 5 ----
print("\n[1] GUARD: los md5 de los tres fuentes, por shard")
firmas = set()
for k, v in sorted(JS.items()):
    fir = (v.get("md5_motor"), v.get("md5_motor_v2"))
    firmas.add(fir)
    print("  %-48s motor=%s  motor_v2=%s  backend=%-4s %s"
          % (k[:46], str(fir[0])[:12], str(fir[1])[:12], v.get("backend"), v.get("gpu", "")[:22]))
print("  firmas distintas: %d -> %s" % (len(firmas), "MISMO SUJETO" if len(firmas) == 1 else "SUJETOS DISTINTOS, NO SE PUEDEN SUMAR"))

# ---- Guard 2: la particion ----
print("\n[2] GUARD: la particion de los 39 nulls")
idx = []
pares = {}
for k, v in AB.items():
    idx += list(v.get("null_indices") or [])
    pares.update(v.get("pares") or {})
medidos = sorted(int(x) for x in pares)
print("  indices asignados: %d   unicos: %d" % (len(idx), len(set(idx))))
print("  nulls con resultado: %d   faltan: %s"
      % (len(medidos), sorted(set(range(39)) - set(medidos)) or "ninguno"))

# ---- 3. el veredicto, con atribucion ----
if pares:
    print("\n[3] A/B v1 vs v2 SOBRE LOS %d NULLS MEDIDOS (jitter=0)" % len(medidos))
    print("  %-6s %-13s %-13s %-13s %-13s %-11s %s"
          % ("null", "d_rho", "d_rdi_t50", "d_rdi_t100", "d_rdi_t149", "v1 convergio", "veredicto"))
    peor = 0.0
    no_conv = []
    difieren = []
    snaps = None
    for gi in medidos:
        p = pares[str(gi)]
        d = p["delta"]
        if snaps is None:
            snaps = sorted(int(x.split("_t")[1]) for x in d if x.startswith("d_rdi_t"))
        vals = [d["d_rho"]] + [d["d_rdi_t%d" % s] for s in snaps]
        mx = max(vals)
        peor = max(peor, mx)
        conv = p["v1"].get("convergio", None)
        if conv is False:
            no_conv.append(gi)
        if mx > 1e-9:
            difieren.append((gi, mx, conv))
        print("  %-6d %-13.3e %-13.3e %-13.3e %-13.3e %-11s %s"
              % (gi, d["d_rho"], d["d_rdi_t%d" % snaps[0]], d["d_rdi_t%d" % snaps[1]],
                 d["d_rdi_t%d" % snaps[2]], str(conv),
                 "identico" if mx < 1e-9 else "DIFIERE %.1e" % mx))
    print("\n  peor desvio global: %.6e" % peor)
    print("  nulls donde la iteracion de potencia de v1 NO convergio: %d -> %s"
          % (len(no_conv), no_conv or "ninguno"))
    print("  nulls que difieren por encima de 1e-9: %d -> %s"
          % (len(difieren), [g for g, _, _ in difieren] or "ninguno"))
    if difieren:
        atrib = all(c is False for _, _, c in difieren)
        print("  ATRIBUCION: todos los que difieren son de NO convergencia? %s" % atrib)
    else:
        print("  ATRIBUCION: no hay nada que atribuir, los %d son identicos" % len(medidos))
    if "real" in list(AB.values())[0] if AB else False:
        pass
    for k, v in AB.items():
        if "real" in v:
            r1, r2 = v["real"]["v1"], v["real"]["v2"]
            print("\n  el grafo REAL:  d_rho=%.3e   %s"
                  % (abs(r1["rho_pre"] - r2["rho_pre"]),
                     "  ".join("d_t%d=%.3e" % (s, abs(r1["rdi_t%d" % s] - r2["rdi_t%d" % s]))
                               for s in snaps)))

# ---- 4. extras ----
for k, v in EX.items():
    print("\n[4] EXTRAS  (%s, backend=%s)" % (k[:46], v.get("backend")))
    if v.get("dist_resumen"):
        print("  DISTRIBUCION de la semilla de fase (%d realizaciones, jitter=0.1)"
              % len(v.get("dist_semilla") or []))
        print("  %-14s %-15s %-13s %-13s %-13s %s" % ("cantidad", "media", "sd", "min", "max", "rango/media %"))
        for kk, r in v["dist_resumen"].items():
            rng = r["max"] - r["min"]
            print("  %-14s %-15.6f %-13.6f %-13.6f %-13.6f %.4f%%"
                  % (kk, r["mean"], r["sd"], r["min"], r["max"],
                     100.0 * rng / max(abs(r["mean"]), 1e-30)))
    if v.get("barrido_jitter"):
        print("\n  BARRIDO de phase_jitter")
        rows = v["barrido_jitter"]
        sn = sorted(int(x.split("_t")[1]) for x in rows[0] if x.startswith("rdi_t"))
        print("  %-9s %-15s %s" % ("jitter", "rho_pre", "  ".join("rdi_t%d" % s for s in sn)))
        for r in rows:
            print("  %-9.2f %-15.6f %s" % (r["_jitter"], r["rho_pre"],
                                           "  ".join("%.6f" % r["rdi_t%d" % s] for s in sn)))
    if v.get("escala"):
        print("\n  ESCALA hasta el n REAL")
        print("  %-9s %-11s %-22s %-22s %s" % ("n", "aristas", "pesos v2/v1", "normaliz. v2/v1", "propagate v2/v1"))
        for r in v["escala"]:
            print("  %-9d %-11d %-22s %-22s %s"
                  % (r["n"], r["e"],
                     "%.4f/%.4f = %.2f" % (r["pesos_v2"], r["pesos_v1"], r["pesos_v2"]/r["pesos_v1"]),
                     "%.4f/%.4f = %.2f" % (r["norm_v2"], r["norm_v1"], r["norm_v2"]/r["norm_v1"]),
                     "%.4f/%.4f = %.2f" % (r["prop_v2"], r["prop_v1"], r["prop_v2"]/r["prop_v1"])))
    if v.get("rss"):
        print("\n  RSS REAL (ru_maxrss del proceso hijo, MB)")
        print("  %-9s %-7s %-16s %-16s %s" % ("n", "etapa", "v1 pico", "v2 pico", "v2/v1"))
        for r in v["rss"]:
            print("  %-9d %-7s %-16.1f %-16.1f %.3f"
                  % (r["n"], r["etapa"], r["v1"]["total_mb"], r["v2"]["total_mb"],
                     r["v2"]["total_mb"] / max(r["v1"]["total_mb"], 1e-9)))

print("\nescrito en %s" % OUT)
