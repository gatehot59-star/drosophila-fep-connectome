#!/usr/bin/env python3
"""Brazo S en el sustrato que pide CONTEXTO-motor.md 6.2: el motivo como reservorio recurrente congelado.

Por que existe. El brazo W del 23-ago (Kaggle abrahammendieta/titan-brazo-w) y su re-corrida del 2-oct en
brain-env pusieron la matriz 26x26 del conectoma como react[2], la segunda capa de un MLP FEEDFORWARD de
DualBrain. Ahi no hay recurrencia ni tau: el cableado recurrente del motivo (54 de 88 aristas reciprocas)
se usa como un solo salto lineal por paso. CONTEXTO-motor.md (24-ago) lo marco: "no refuta la hipotesis:
nunca la testeo". Este script corre la version que faltaba: el motivo como reservorio con la dinamica
real de SparseLTC, congelado, con tau congelada, contra su shuffle de grado exacto.

Que corre: UNA celda (tarea x brazo) con N semillas. Todo lo que no es la via react se copia VERBATIM de
brazo_w.py: tareas, LiquidCell, DualBrain, gate, head, Adam lr=1e-3, batch 64, 2000 pasos, clip 1.0,
evaluacion en 2000 secuencias, set_seed(s) antes de construir el modelo. Para una semilla dada, todos los
brazos arrancan con los mismos pesos de enc, cell, gate y head, y ven el mismo flujo de datos.

Brazos:
  A   DualBrain original, todo entrenable. Techo. Debe reproducir el brazo W.
  B   react MLP denso aleatorio, congelado. Debe reproducir el brazo W.
  RB  react recurrente: z = (1 - tau) z + tau tanh(W z + U x); W = react[2] aleatorio llevado a rho 0.9
  RW  igual, W = motivo real del conectoma llevado a rho 0.9 (la misma matriz que el brazo W)
  RS  igual, W = shuffle de grado in/out exacto del motivo, pesos permutados, UNO DISTINTO por semilla
      (la semilla 0 usa exactamente el shuffle del brazo W: seed 20260823 y permutacion 777)
  LB, LW, LS  como RB, RW, RS pero con tau liquida: tau_t = sigmoid(logit(tau) + Vx x + Vh z), congelada
  F   DualBrain original con la memoria SIN liquidez: el peso de cell.tau en cero y congelado, asi
      tau = sigmoid(b) por unidad (b entrenable). Mide si la tau dependiente de la entrada hace falta.
En RB..LS se congelan U (react[0]), W y tau; se entrenan enc, cell, gate y head, igual que B, W y S.

Uso:
  python3 brazo_s_recurrente.py --tarea Gated --brazo RS --motivo motivo26.json --out celda.json
Opciones para humo: --semillas 2 --pasos 5 --eval-n 64

Codigos de salida: 0 celda completa; 2 un guard fallo (shuffle invalido, W == S, radio distinto de 0.9,
cantidad de parametros entrenables distinta de la declarada): la celda no vale y no se escribe veredicto.
"""
import argparse
import hashlib
import json
import math
import os
import platform
import sys
import time

import numpy as np
import torch
import torch.nn as nn


# ===== copiado VERBATIM de brazo_w.py (que lo copio de titan-tres-brazos): motor y tareas =====
def set_seed(s):
    torch.manual_seed(s); np.random.seed(s)
    if torch.cuda.is_available(): torch.cuda.manual_seed_all(s)


class LiquidCell(nn.Module):
    def __init__(self, inp, hid, tau_bias=-2.0):
        super().__init__()
        self.W_in = nn.Linear(inp, hid, bias=False)
        self.W_res = nn.Linear(hid, hid, bias=False)
        self.tau = nn.Linear(inp+hid, hid)
        nn.init.constant_(self.tau.bias, tau_bias)
        self.ln = nn.LayerNorm(hid)
    def forward(self, x, h):
        t = torch.sigmoid(self.tau(torch.cat([x,h],-1)))
        f = torch.tanh(self.W_in(x)+self.W_res(h))
        return self.ln((1-t)*h + t*f), t

class DualBrain(nn.Module):
    def __init__(self, ind, outd, h_r=24, h_m=8):
        super().__init__()
        self.h_m = h_m
        self.react = nn.Sequential(nn.Linear(ind,h_r),nn.Tanh(),nn.Linear(h_r,h_r),nn.Tanh())
        self.enc = nn.Sequential(nn.Linear(ind,h_m),nn.GELU())
        self.cell = LiquidCell(h_m, h_m)
        self.gate = nn.Linear(h_r+h_m, h_m)
        nn.init.zeros_(self.gate.weight); nn.init.zeros_(self.gate.bias)
        self.head = nn.Linear(h_r+h_m, outd)
    def forward(self, xs, h=None, probe=False):
        T,B,_ = xs.shape
        if h is None: h = xs.new_zeros(B, self.h_m)
        out, hs, ts, gs = [], [], [], []
        for t in range(T):
            hr = self.react(xs[t])
            hm, tau = self.cell(self.enc(xs[t]), h); h = hm
            g = torch.sigmoid(self.gate(torch.cat([hr,hm],-1)))
            out.append(self.head(torch.cat([hr, g*hm],-1)))
            if probe: hs.append(hm); ts.append(tau); gs.append(g)
        if probe:
            return torch.stack(out), torch.stack(hs), torch.stack(ts), torch.stack(gs)
        return torch.stack(out)

def gen_cr(B, steps=10, cue=3, dev="cpu"):
    # target = x * cue, con cue en {-1,+1}. Inversion de fase.
    cues = torch.sign(torch.randn(B,device=dev)); cues[cues==0]=1.
    obs = torch.zeros(steps,B,3,device=dev)
    tgt = torch.zeros(steps,B,1,device=dev)
    mask = torch.zeros(steps,B,device=dev)
    for t in range(steps):
        x = torch.rand(B,device=dev)*2-1
        obs[t,:,0]=x; obs[t,:,2]=t/steps
        if t<cue: obs[t,:,1]=cues
        else: mask[t]=1.
        tgt[t,:,0]=x*cues
    return obs,tgt,mask

def gen_gated(B, L=20, dev="cpu"):
    # target = x * c * sign(x) = |x| * c.  RECTIFICACION por referencia.
    c = torch.rand(B,device=dev)*2-1
    obs = torch.zeros(L,B,2,device=dev)
    tgt = torch.zeros(L,B,1,device=dev)
    mask = torch.zeros(L,B,device=dev)
    obs[0,:,1] = c
    for t in range(L):
        x = torch.rand(B,device=dev)*2-1
        obs[t,:,0] = x
        tgt[t,:,0] = x * c * torch.sign(x)
        if t > 0: mask[t] = 1.
    return obs, tgt, mask

def gen_multicue(B, L=15, dev="cpu"):
    # target = x * (c1+c2)/2. Lineal en x, dos referencias promediadas.
    c1 = torch.rand(B,device=dev)*2-1
    c2 = torch.rand(B,device=dev)*2-1
    obs = torch.zeros(L,B,3,device=dev)
    tgt = torch.zeros(L,B,1,device=dev)
    mask = torch.zeros(L,B,device=dev)
    obs[0,:,1] = c1
    obs[1,:,2] = c2
    for t in range(L):
        x = torch.rand(B,device=dev)*2-1
        obs[t,:,0] = x
        tgt[t,:,0] = x * (c1+c2)/2
        if t > 1: mask[t] = 1.
    return obs, tgt, mask

def gen_linscale(B, L=20, dev="cpu"):
    # CONTROL NUEVO: target = x * c. Identico a gen_gated pero SIN rectificar.
    # Separa -no lineal en x- de -multiplicativo-. Misma longitud, misma
    # estructura de mascara: la UNICA diferencia es el sign(x).
    c = torch.rand(B,device=dev)*2-1
    obs = torch.zeros(L,B,2,device=dev)
    tgt = torch.zeros(L,B,1,device=dev)
    mask = torch.zeros(L,B,device=dev)
    obs[0,:,1] = c
    for t in range(L):
        x = torch.rand(B,device=dev)*2-1
        obs[t,:,0] = x
        tgt[t,:,0] = x * c
        if t > 0: mask[t] = 1.
    return obs, tgt, mask

TAREAS = {
  "CR":        {"gen": gen_cr,       "ind": 3, "steps": 2000, "desc": "x*cue, cue en +-1 (inversion de fase)"},
  "Gated":     {"gen": gen_gated,    "ind": 2, "steps": 2000, "desc": "|x|*c (rectificacion x referencia)"},
  "MultiCue":  {"gen": gen_multicue, "ind": 3, "steps": 2000, "desc": "x*(c1+c2)/2 (lineal, 2 refs)"},
  "LinScale":  {"gen": gen_linscale, "ind": 2, "steps": 2000, "desc": "x*c (lineal, 1 ref) CONTROL"},
}
# ===== fin de lo copiado =====

HR, HM, BATCH, LR = 26, 8, 64, 1e-3
RHO = 0.9
TAU_LO, TAU_HI, TAU_SEED = 0.06, 0.18, 119
VH_SEED, VX_SEED = 120, 121
SHUFFLE_SEED0, PERM_SEED0 = 20260823, 777
ENTRENABLES = {"A": {2: 1399, 3: 1433}, "B": {2: 619, 3: 627}, "F": {2: 1271, 3: 1305}}
for _k in ("RB", "RW", "RS", "LB", "LW", "LS"):
    ENTRENABLES[_k] = ENTRENABLES["B"]
BRAZOS = {
    "A": "DualBrain original, todo entrenable (techo; debe reproducir el brazo W)",
    "B": "react MLP denso aleatorio, congelado (debe reproducir el brazo W)",
    "RB": "react recurrente SparseLTC, W aleatorio denso rho 0.9, tau fija heterogenea, congelado",
    "RW": "react recurrente SparseLTC, W = motivo real del conectoma rho 0.9, tau fija heterogenea, congelado",
    "RS": "react recurrente SparseLTC, W = shuffle grado exacto del motivo (uno por semilla), tau fija, congelado",
    "LB": "como RB con tau liquida (depende de la entrada y del estado), congelado",
    "LW": "como RW con tau liquida, congelado",
    "LS": "como RS con tau liquida, congelado",
    "F": "DualBrain original con la memoria sin liquidez: tau = sigmoid(b) por unidad",
}
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")


def md5_file(path):
    """md5 de un archivo."""
    h = hashlib.md5()
    with open(path, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def deg_io(E, n=26):
    """Grado de entrada y de salida de una lista de aristas (i -> j)."""
    di = np.zeros(n, dtype=np.int64); do = np.zeros(n, dtype=np.int64)
    for (i, j) in E:
        do[i] += 1; di[j] += 1
    return di, do


def ms_shuffle(E, seed, iters):
    """Swap de Maslov-Sneppen, verbatim de brazo_w.py: conserva grado in y out, sin autolazos ni multiaristas."""
    rng = np.random.default_rng(seed)
    Ez = [list(e) for e in E]
    have = set((a, b) for (a, b) in E)
    ok = 0
    for _ in range(iters):
        p = int(rng.integers(0, len(Ez))); q = int(rng.integers(0, len(Ez)))
        if p == q: continue
        a, b = Ez[p]; c, d = Ez[q]
        if a == d or c == b: continue
        if (a, d) in have or (c, b) in have: continue
        have.discard((a, b)); have.discard((c, d))
        have.add((a, d)); have.add((c, b))
        Ez[p] = [a, d]; Ez[q] = [c, b]; ok += 1
    return [tuple(e) for e in Ez], ok


def radio(A):
    """Radio espectral en float64."""
    return float(np.max(np.abs(np.linalg.eigvals(np.asarray(A, dtype=np.float64)))))


def a_rho(A, target=RHO):
    """Escala la matriz a radio espectral target, como spec_norm de brazo_w.py."""
    r = radio(A)
    if r < 1e-12:
        raise SystemExit("ABORTA: radio espectral nulo")
    return np.asarray(A, dtype=np.float64) * (target / r), r


def matriz_shuffle(M, edges, s):
    """Shuffle de grado exacto del motivo para la semilla s, con los mismos pesos permutados.

    Con s = 0 reproduce el S del brazo W (seed 20260823, permutacion default_rng(777)).
    """
    nE = len(edges)
    E_sh, n_ok = ms_shuffle(edges, SHUFFLE_SEED0 + s, 30 * nE)
    di0, do0 = deg_io(edges); di1, do1 = deg_io(E_sh)
    g = {"swaps_efectivos": int(n_ok),
         "grado_mal": int(np.sum(di0 != di1) + np.sum(do0 != do1)),
         "unicas": len(set(E_sh)),
         "autolazos": sum(1 for (i, j) in E_sh if i == j),
         "aristas_sin_mover": sum(1 for e in E_sh if e in set(edges))}
    if g["grado_mal"] != 0 or g["unicas"] != nE or g["autolazos"] != 0 or n_ok == 0:
        raise SystemExit("ABORTA: shuffle invalido en semilla " + str(s) + ": " + json.dumps(g))
    pesos = np.array([M[j, i] for (i, j) in edges], dtype=np.float64)
    perm = np.random.default_rng(PERM_SEED0 + s).permutation(len(pesos))
    MS = np.zeros_like(M)
    for k, (i, j) in enumerate(E_sh):
        MS[j, i] = pesos[perm[k]]
    return MS, g


class ReactRecurrente(nn.Module):
    """Via react como reservorio SparseLTC real y congelado: z = (1 - tau) z + tau tanh(W z + U x)."""

    def __init__(self, U, Wrec, tau, liquida, Vx=None, Vh=None):
        super().__init__()
        self.U = U
        self.register_buffer("Wrec", Wrec.clone())
        self.register_buffer("tau_logit", torch.logit(tau.clone()))
        self.liquida = bool(liquida)
        if self.liquida:
            self.register_buffer("Vx", Vx.clone())
            self.register_buffer("Vh", Vh.clone())

    def forward(self, x, z):
        """Un paso de la dinamica; x es (B, ind) y z es (B, h_r)."""
        f = torch.tanh(z @ self.Wrec.t() + self.U(x))
        if self.liquida:
            t = torch.sigmoid(self.tau_logit + x @ self.Vx.t() + z @ self.Vh.t())
        else:
            t = torch.sigmoid(self.tau_logit).expand_as(z)
        return (1.0 - t) * z + t * f


class DualBrainRecurrente(nn.Module):
    """DualBrain con la via react recurrente; enc, cell, gate y head son los objetos del DualBrain base."""

    def __init__(self, base, react):
        super().__init__()
        self.h_m = base.h_m
        self.h_r = int(react.Wrec.shape[0])
        self.react = react
        self.enc = base.enc
        self.cell = base.cell
        self.gate = base.gate
        self.head = base.head

    def forward(self, xs, h=None):
        """Mismo lazo que DualBrain.forward, con el estado z de la via react arrastrado entre pasos."""
        T, B, _ = xs.shape
        if h is None:
            h = xs.new_zeros(B, self.h_m)
        z = xs.new_zeros(B, self.h_r)
        out = []
        for t in range(T):
            z = self.react(xs[t], z)
            hm, _ = self.cell(self.enc(xs[t]), h); h = hm
            g = torch.sigmoid(self.gate(torch.cat([z, hm], -1)))
            out.append(self.head(torch.cat([z, g * hm], -1)))
        return torch.stack(out)


def cargar_motivo(path):
    """Lee motivo26.json (salida de motivo26.py) y devuelve la matriz cruda y sus aristas."""
    d = json.load(open(path))
    if d.get("fallas"):
        raise SystemExit("ABORTA: el motivo trae fallas: " + str(d["fallas"]))
    M = np.array(d["M_cruda"], dtype=np.float64)
    edges = [tuple(e) for e in d["aristas"]]
    if M.shape != (26, 26) or len(edges) != d["n_aristas"]:
        raise SystemExit("ABORTA: motivo con forma inesperada")
    return M, edges, d


def construir(brazo, ind, s, M, edges, tau, Vx, Vh):
    """Construye el modelo del brazo para la semilla s, consumiendo el RNG de torch igual que brazo_w.py."""
    set_seed(s)
    base = DualBrain(ind, 1, HR, HM)
    g = {}
    if brazo == "A":
        return base, g
    if brazo == "B":
        for p in base.react.parameters():
            p.requires_grad = False
        return base, g
    if brazo == "F":
        with torch.no_grad():
            base.cell.tau.weight.zero_()
        base.cell.tau.weight.requires_grad = False
        g["tau_peso_max_abs"] = float(base.cell.tau.weight.abs().max().item())
        return base, g
    liquida = brazo.startswith("L")
    tipo = brazo[1]
    Wn_real, _ = a_rho(M)
    if tipo == "B":
        Wn, r0 = a_rho(base.react[2].weight.detach().double().numpy())
    elif tipo == "W":
        Wn, r0 = Wn_real, radio(M)
    else:
        MS, gs = matriz_shuffle(M, edges, s)
        g.update(gs)
        Wn, r0 = a_rho(MS)
        g["max_abs_W_menos_S"] = float(np.max(np.abs(Wn_real - Wn)))
        if g["max_abs_W_menos_S"] < 1e-9:
            raise SystemExit("ABORTA: W y S son la misma matriz en la semilla " + str(s))
    Wt = torch.tensor(Wn, dtype=torch.float32)
    g["radio_crudo"] = float(r0)
    g["radio_post"] = radio(Wt.double().numpy())
    if abs(g["radio_post"] - RHO) > 1e-5:
        raise SystemExit("ABORTA: radio post-normalizacion " + str(g["radio_post"]))
    U = base.react[0]
    for p in U.parameters():
        p.requires_grad = False
    react = ReactRecurrente(U, Wt, torch.tensor(tau, dtype=torch.float32), liquida,
                            torch.tensor(Vx, dtype=torch.float32) if liquida else None,
                            torch.tensor(Vh, dtype=torch.float32) if liquida else None)
    return DualBrainRecurrente(base, react), g


def main():
    """Corre una celda tarea x brazo y escribe su JSON con la evidencia por semilla."""
    ap = argparse.ArgumentParser(description="Brazo S recurrente: una celda tarea x brazo")
    ap.add_argument("--tarea", required=True, choices=sorted(TAREAS.keys()))
    ap.add_argument("--brazo", required=True, choices=list(BRAZOS.keys()))
    ap.add_argument("--motivo", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--semillas", type=int, default=10)
    ap.add_argument("--pasos", type=int, default=0, help="0 = los de la tarea (2000)")
    ap.add_argument("--eval-n", type=int, default=2000)
    a = ap.parse_args()

    T0 = time.time()
    spec = TAREAS[a.tarea]
    ind, gen = spec["ind"], spec["gen"]
    steps = a.pasos if a.pasos > 0 else spec["steps"]
    M, edges, mot = cargar_motivo(a.motivo)
    tau = np.random.default_rng(TAU_SEED).uniform(TAU_LO, TAU_HI, size=HR)
    Vh = np.random.default_rng(VH_SEED).normal(0.0, 1.0 / math.sqrt(HR), size=(HR, HR))
    Vx = np.random.default_rng(VX_SEED + ind).normal(0.0, 1.0 / math.sqrt(ind), size=(HR, ind))
    cpu = "desconocida"
    try:
        for line in open("/proc/cpuinfo"):
            if line.startswith("model name"):
                cpu = line.split(":", 1)[1].strip(); break
    except OSError:
        pass
    meta = {"torch": torch.__version__, "numpy": np.__version__, "python": platform.python_version(),
            "maquina": platform.platform(), "cpu": cpu, "hilos_torch": torch.get_num_threads(),
            "device": str(DEVICE), "md5_script": md5_file(os.path.abspath(__file__)),
            "md5_motivo": md5_file(a.motivo), "motivo_fuente": mot.get("fuente", {}),
            "git_sha": os.environ.get("GITHUB_SHA", ""), "run_id": os.environ.get("GITHUB_RUN_ID", ""),
            "fecha_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "semillas": a.semillas, "pasos": steps, "eval_n": a.eval_n, "batch": BATCH, "lr": LR,
            "h_r": HR, "h_m": HM, "rho": RHO, "tau_rango": [TAU_LO, TAU_HI], "tau_seed": TAU_SEED,
            "tau_media": float(tau.mean()), "vh_seed": VH_SEED, "vx_seed": VX_SEED + ind}
    print("# celda tarea=" + a.tarea + " brazo=" + a.brazo + " :: " + BRAZOS[a.brazo])
    print("# " + json.dumps(meta, sort_keys=True))

    mses, guardas, segs = [], [], []
    ntr = ntot = -1
    for s in range(a.semillas):
        t0 = time.time()
        m, g = construir(a.brazo, ind, s, M, edges, tau, Vx, Vh)
        m = m.to(DEVICE)
        ntr = sum(p.numel() for p in m.parameters() if p.requires_grad)
        ntot = sum(p.numel() for p in m.parameters())
        if ntr != ENTRENABLES[a.brazo][ind]:
            print("ABORTA: entrenables=" + str(ntr) + " declarados=" + str(ENTRENABLES[a.brazo][ind]))
            return 2
        m.train()
        ps = [p for p in m.parameters() if p.requires_grad]
        opt = torch.optim.Adam(ps, lr=LR)
        for _ in range(steps):
            o, tg, mk = gen(BATCH, dev=DEVICE)
            out = m(o)
            loss = ((out - tg) ** 2).squeeze(-1) * mk
            loss = loss.sum() / max(mk.sum(), 1)
            opt.zero_grad()
            loss.backward()
            nn.utils.clip_grad_norm_(ps, 1.0)
            opt.step()
        m.eval()
        with torch.no_grad():
            o, tg, mk = gen(a.eval_n, dev=DEVICE)
            out = m(o)
            mse = (((out - tg) ** 2).squeeze(-1) * mk).sum() / max(mk.sum(), 1)
        mses.append(float(mse.item()))
        guardas.append(g)
        segs.append(time.time() - t0)
        print("semilla=" + str(s) + " mse=" + repr(mses[-1]) + " entrenables=" + str(ntr) + "/" + str(ntot)
              + " seg=" + format(segs[-1], ".1f") + " guardas=" + json.dumps(g, sort_keys=True), flush=True)

    arr = np.array(mses)
    res = {"tarea": a.tarea, "brazo": a.brazo, "desc": BRAZOS[a.brazo], "mse": mses,
           "mean": float(arr.mean()), "sd": float(arr.std(ddof=1)) if len(arr) > 1 else 0.0,
           "entrenables": int(ntr), "totales_parametros": int(ntot), "seg_por_semilla": segs,
           "guardas": guardas, "meta": meta, "minutos": (time.time() - T0) / 60.0}
    with open(a.out, "w") as f:
        json.dump(res, f)
    print("RESUMEN tarea=" + a.tarea + " brazo=" + a.brazo + " mean=" + format(res["mean"], ".6f")
          + " sd=" + format(res["sd"], ".6f") + " n=" + str(len(mses)) + " minutos=" + format(res["minutos"], ".1f"))
    print("FIN_CELDA")
    return 0


if __name__ == "__main__":
    sys.exit(main())
