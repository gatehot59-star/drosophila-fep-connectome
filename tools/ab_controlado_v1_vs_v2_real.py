"""A/B CONTROLADO de v1 vs v2 sobre EL CONECTOMA REAL.

Cierra el NO MEDIDO #1 de la respuesta 105: la tabla de esa respuesta cruzaba dos
corridas que diferian en CUATRO variables a la vez (brazos, modalidades, nulls,
rejilla de tiempo), asi que no era un A/B. Aca se fija todo y se deja variar UNA
cosa: el archivo.

Diseno, y por que cada decision:
  - MISMO grafo real, cargado UNA vez, fuera de los dos motores.
  - MISMAS 3 modalidades (las de v1), MISMOS 150 pasos, MISMOS snapshots.
  - MISMO tau (el de v2, pasado a los dos).
  - Dos condiciones de jitter:
      j=0.0  -> la hipotesis fuerte. Si la unica diferencia entre v1 y v2 es la
                realizacion del ruido de fase, los dos tienen que dar IDENTICO
                sobre el conectoma real, no solo sobre un sintetico de 4000 nodos.
                Es la version FALSABLE del claim de la respuesta 105.
      j=0.1  -> el default. Cuanto vale ese ruido a escala real.
  - Un null con la MISMA semilla en los dos, porque los nulls habian quedado
    fuera y el claim tiene que valer tambien sobre un grafo permutado.

W-01: se imprime el valor crudo de los dos lados en cada linea.
Corrido en brain-env el 2026-08-26, 1.185 s. Salida verbatim en
docs/agents/evidencia/2026-08-26-106-cierre-no-medidos-evidencia-cruda.md
"""
import importlib.util, sys, os, time, json
import numpy as np

def load(p, n):
    s = importlib.util.spec_from_file_location(n, p); m = importlib.util.module_from_spec(s)
    sys.modules[n] = m; s.loader.exec_module(m); return m

T0 = time.time()
def lg(s):
    print("[%7.1fs] %s" % (time.time() - T0, s), flush=True)

V1 = load("/workspace/motor.py", "mv1")
V2 = load("/workspace/motor_v2.py", "mv2")
lg("modulos cargados")

D = V2.load_connectome("/workspace", download=False)
pre, post, w = D["pre"], D["post"], D["w"]
n = int(D["n"]); bin_of = D["bin_of"]; n_bins = len(D["bin_names"])
lg("conectoma: n=%d  e=%d  md5_parquet=%s" % (n, pre.shape[0], D["md5"]["parquet"]))
lg("modalidades disponibles: %s  tamanos=%s" % (D["mod_names"], [int(x.shape[0]) for x in D["stim"]]))

# LAS 3 DE v1, no las 4 de v2: es la variable que se fija
STIM = D["stim"][:3]
MODS = D["mod_names"][:3]
STEPS = 150
SNAP = sorted(set([max(1, STEPS//3), max(2, (2*STEPS)//3), STEPS-1]))
lg("A/B controlado: modalidades=%s  pasos=%d  snapshots=%s" % (MODS, STEPS, SNAP))

tau = V2.make_tau(n)
tau = tau[0] if isinstance(tau, tuple) else tau
lg("tau: Re=%.6f  |Im| medio=%.6f  (el MISMO para los dos)" % (tau.real.mean(), np.abs(tau.imag).mean()))

def medir(M, ver, p_post, jitter, etiqueta):
    """Corre la cadena entera de UN motor: pesos -> normalizacion -> dinamica -> rdi."""
    t = time.time()
    if ver == 1:
        r = M.build_complex_weights(pre, p_post, w, n, phase_jitter=jitter)
        W = r[0]
        o = M.normalize_spectral(W)
        Wn, rho_rep = o[0], o[1]
    else:
        r = M.build_weights(pre, p_post, w, n, mode=M.WEIGHT_COMPLEX, phase_jitter=jitter)
        W = r[0]
        o = M.normalize_spectral(W)
        Wn = o[0]; rho_rep = o[1].get("rho_pre") if isinstance(o[1], dict) else o[1]
    t_w = time.time() - t
    profs = {s: [] for s in SNAP}
    t = time.time()
    for mi in STIM:
        out = M.propagate(Wn, tau, mi, n_steps=STEPS, save_at=SNAP)[0]
        for s in SNAP:
            profs[s].append(M.region_profile(out[s], bin_of, n_bins))
    t_p = time.time() - t
    res = {"rho_pre": float(rho_rep), "nnz": int(Wn.nnz), "t_pesos_s": t_w, "t_dinamica_s": t_p}
    for s in SNAP:
        v, nv, nx = M.rdi(profs[s])
        res["rdi_t%d" % s] = float(v); res["pares_t%d" % s] = int(nv)
    lg("  %-26s rho_pre=%12.4f  nnz=%d  rdi=%s  (%.1f s)"
       % (etiqueta, res["rho_pre"], res["nnz"],
          " ".join("t%d=%.6f" % (s, res["rdi_t%d" % s]) for s in SNAP), t_w + t_p))
    return res

OUT = {"meta": {"n": n, "e": int(pre.shape[0]), "md5": D["md5"], "mods": MODS,
                "steps": STEPS, "snap": SNAP}, "corridas": {}}

lg("")
lg("########## CONDICION A: phase_jitter = 0.0  (la hipotesis fuerte) ##########")
a1 = medir(V1, 1, post, 0.0, "v1 REAL jitter=0.0")
OUT["corridas"]["v1_real_j0"] = a1
a2 = medir(V2, 2, post, 0.0, "v2 REAL jitter=0.0")
OUT["corridas"]["v2_real_j0"] = a2
json.dump(OUT, open("/workspace/ab_real.json", "w"), indent=1)

lg("")
lg("  VEREDICTO de la condicion A, sobre el conectoma real:")
lg("    d(rho_pre)  = %.6e" % abs(a1["rho_pre"] - a2["rho_pre"]))
for s in SNAP:
    lg("    d(rdi t%-3d) = %.6e   (v1=%.12f  v2=%.12f)"
       % (s, abs(a1["rdi_t%d" % s] - a2["rdi_t%d" % s]), a1["rdi_t%d" % s], a2["rdi_t%d" % s]))
ident = abs(a1["rho_pre"] - a2["rho_pre"]) < 1e-6 and all(
    abs(a1["rdi_t%d" % s] - a2["rdi_t%d" % s]) < 1e-9 for s in SNAP)
lg("    -> %s" % ("IDENTICOS a escala real: la fisica de v1 y v2 es la misma."
                  if ident else "DIFIEREN incluso sin jitter: hay algo mas que el ruido."))

lg("")
lg("########## CONDICION B: phase_jitter = 0.1  (el default) ##########")
b1 = medir(V1, 1, post, 0.1, "v1 REAL jitter=0.1")
OUT["corridas"]["v1_real_j01"] = b1
b2 = medir(V2, 2, post, 0.1, "v2 REAL jitter=0.1")
OUT["corridas"]["v2_real_j01"] = b2
json.dump(OUT, open("/workspace/ab_real.json", "w"), indent=1)
lg("")
lg("  Cuanto vale el RUIDO DE FASE a escala real:")
lg("    d(rho_pre) = %.6f   (%.4f%% de %.4f)"
   % (abs(b1["rho_pre"] - b2["rho_pre"]),
      100.0*abs(b1["rho_pre"] - b2["rho_pre"])/max(b1["rho_pre"], 1e-30), b1["rho_pre"]))
for s in SNAP:
    d = abs(b1["rdi_t%d" % s] - b2["rdi_t%d" % s])
    lg("    d(rdi t%-3d) = %.6f   (v1=%.6f  v2=%.6f)  -> %.2f%% del valor"
       % (s, d, b1["rdi_t%d" % s], b2["rdi_t%d" % s], 100.0*d/max(abs(b1["rdi_t%d" % s]), 1e-30)))

lg("")
lg("########## CONDICION C: UN NULL con la MISMA semilla, jitter=0.0 ##########")
SEED = 1000
p0 = V2.make_null("cp", pre, post, n, bin_of, seed=SEED)
lg("  null CP seed=%d generado (el MISMO array para los dos)" % SEED)
c1 = medir(V1, 1, p0, 0.0, "v1 NULL seed1000 j=0")
OUT["corridas"]["v1_null_j0"] = c1
c2 = medir(V2, 2, p0, 0.0, "v2 NULL seed1000 j=0")
OUT["corridas"]["v2_null_j0"] = c2
lg("    d(rho_pre)  = %.6e" % abs(c1["rho_pre"] - c2["rho_pre"]))
for s in SNAP:
    lg("    d(rdi t%-3d) = %.6e" % (s, abs(c1["rdi_t%d" % s] - c2["rdi_t%d" % s])))

lg("")
lg("########## PERFORMANCE A ESCALA REAL (n=138.639) ##########")
lg("  %-22s %-14s %-14s %s" % ("etapa", "v1 (s)", "v2 (s)", "v2/v1"))
for k, lbl in [("t_pesos_s", "pesos+normaliz."), ("t_dinamica_s", "dinamica x3 mods")]:
    lg("  %-22s %-14.2f %-14.2f %.3f" % (lbl, a1[k], a2[k], a2[k]/max(a1[k], 1e-9)))
tot1 = a1["t_pesos_s"] + a1["t_dinamica_s"]; tot2 = a2["t_pesos_s"] + a2["t_dinamica_s"]
lg("  %-22s %-14.2f %-14.2f %.3f" % ("TOTAL", tot1, tot2, tot2/max(tot1, 1e-9)))
lg("  fraccion del tiempo en la dinamica:  v1=%.1f%%   v2=%.1f%%"
   % (100.0*a1["t_dinamica_s"]/tot1, 100.0*a2["t_dinamica_s"]/tot2))

OUT["veredicto_identicos_sin_jitter"] = bool(ident)
json.dump(OUT, open("/workspace/ab_real.json", "w"), indent=1)
lg("")
lg("FIN. escrito /workspace/ab_real.json")
print("FINAB", flush=True)
