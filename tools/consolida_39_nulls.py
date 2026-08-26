"""Consolida los 4 shards de Kaggle GPU en el resultado de los 39 nulls.

W-01: se verifica la particion, los md5 del dato y el veredicto espectral ANTES de
cualquier p. Si la particion no cubre 0..38 exactamente una vez, aborta.

Corrido el 2026-08-26 en brain-env sobre los 4 shard_*.json bajados de Kaggle.
Salida verbatim en docs/agents/evidencia/2026-08-26-101-kaggle-slug-403-y-39-nulls.md
"""
import json, glob, math, statistics as st

paths = sorted(glob.glob("/workspace/kshards/shard*_shard_*.json"))
S = [json.load(open(p)) for p in paths]
print("=" * 92)
print("CONSOLIDACION DE LOS 39 NULLS  ·  4 shards de Kaggle GPU (Tesla P100)")
print("=" * 92)

# --- 1. la particion ---
idx = []
for s in S:
    idx += list(s["null_indices"])
esperado = list(range(39))
dup = len(idx) != len(set(idx))
print("\n[1] PARTICION")
print("    indices reunidos : %d   unicos: %d   duplicados: %s" % (len(idx), len(set(idx)), dup))
print("    cubre 0..38      : %s" % (sorted(set(idx)) == esperado))
faltan = sorted(set(esperado) - set(idx))
print("    faltantes        : %s" % (faltan if faltan else "ninguno"))
if sorted(set(idx)) != esperado or dup:
    raise SystemExit("ABORTA: la particion no es exacta. No se calcula ningun p.")

# --- 2. el dato es el mismo en los 4 ---
print("\n[2] EL DATO (md5 del parquet y de annotations, por shard)")
md5s = set()
for s in S:
    m = s["meta"]["md5"]
    md5s.add((m["parquet"], m["annotations"]))
    print("    shard %d  n=%d  e=%d  parquet=%s  annot=%s  unmatched=%d  backend=%s  %s"
          % (s["shard_id"], s["meta"]["n"], s["meta"]["e"], m["parquet"][:12],
             m["annotations"][:12], s["meta"]["annot"]["unmatched"], s["backend"], s["gpu"]))
print("    md5 distintos entre shards: %d  -> %s" % (len(md5s), "MISMO DATO" if len(md5s) == 1 else "DATOS DISTINTOS, INVALIDO"))

# --- 3. nulls reunidos ---
nulls = {}
for s in S:
    for k, v in s["nulls"].items():
        nulls[int(k)] = v
print("\n[3] NULLS REUNIDOS: %d de 39" % len(nulls))

real = None
for s in S:
    if s.get("real"):
        real = s["real"]
        t_real = s.get("t_real_s")
print("    brazo REAL presente: %s   (t=%.1f s)" % (real is not None, t_real))

# --- 4. control espectral en los 39 + real ---
print("\n[4] CONTROL ESPECTRAL (rho_post tiene que ser 0.99 en los 4 brazos)")
for arm in ["Wc_tauC", "Wc_tauR", "Wr_tauC", "Wr_tauR"]:
    ver = [nulls[i].get("spec_verdict_" + arm) for i in sorted(nulls)]
    rho = [nulls[i].get("rho_post_" + arm) for i in sorted(nulls) if nulls[i].get("rho_post_" + arm) is not None]
    ok = sum(1 for v in ver if v == "OK")
    print("    %-9s  OK %2d/39   rho_post min=%.6f max=%.6f   real=%.6f (%s)"
          % (arm, ok, min(rho), max(rho), real["rho_post_" + arm], real["spec_verdict_" + arm]))

# --- 5. el test ---
def test(key):
    r = real.get(key)
    v = [nulls[i][key] for i in sorted(nulls) if nulls[i].get(key) is not None]
    if r is None or len(v) == 0:
        return None
    n = len(v)
    ge = sum(1 for x in v if x >= r)
    le = sum(1 for x in v if x <= r)
    p_der = (ge + 1) / (n + 1)
    p_izq = (le + 1) / (n + 1)
    p_dos = min(1.0, 2 * min(p_der, p_izq))
    z = (r - st.mean(v)) / st.stdev(v) if n > 1 and st.stdev(v) > 0 else float("nan")
    return dict(real=r, n=n, mean=st.mean(v), sd=st.stdev(v), lo=min(v), hi=max(v),
                ge=ge, le=le, p_der=p_der, p_izq=p_izq, p_dos=p_dos, z=z,
                spread=(r / st.mean(v)) if st.mean(v) != 0 else float("nan"))

print("\n[5] EL TEST · REAL contra los 39 nulls  (p una cola = (k+1)/(n+1), piso 1/40 = 0.0250)")
claves = []
for t in [50, 100, 149]:
    claves += ["rdi_Wc_tauC_t%d" % t, "ventaja_tau_t%d" % t, "ventaja_W_t%d" % t, "interaccion_t%d" % t]
print("    %-22s %9s %9s %8s %8s %8s %7s %7s %8s" % ("metrica", "REAL", "null_med", "null_sd", "null_min", "null_max", "k>=R", "p_1cola", "z"))
res = {}
for k in claves:
    d = test(k)
    if d is None:
        print("    %-22s   NO MEDIDO" % k); continue
    res[k] = d
    print("    %-22s %9.4f %9.4f %8.4f %8.4f %8.4f %7d %8.4f %8.2f"
          % (k, d["real"], d["mean"], d["sd"], d["lo"], d["hi"], d["ge"], d["p_der"], d["z"]))

print("\n[6] LECTURA")
for t in [50, 100, 149]:
    k = "rdi_Wc_tauC_t%d" % t
    if k in res:
        d = res[k]
        veredicto = "CERO (ningun null lo alcanza)" if d["ge"] == 0 else ("%d nulls igualan o superan al real" % d["ge"])
        print("    t=%3d  rdi real %.4f  vs  media null %.4f  ->  spread %.2fx  ·  %s"
              % (t, d["real"], d["mean"], d["spread"], veredicto))

out = {"n_nulls": len(nulls), "particion_ok": True, "md5_unico": len(md5s) == 1,
       "resultado": {k: res[k] for k in res}, "meta": S[0]["meta"], "backend": [s["backend"] for s in S]}
json.dump(out, open("/workspace/kshards/CONSOLIDADO_39.json", "w"), indent=1)
print("\n    escrito /workspace/kshards/CONSOLIDADO_39.json")
