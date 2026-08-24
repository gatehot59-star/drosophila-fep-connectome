# TITAN v5.4 - Experimentos para el paper de DualBrain
#
# Que agrega sobre el benchmark original (notebookceb82767da, N_SEEDS=3):
#   A. BODE: respuesta en frecuencia de las 16 dimensiones de h_m.
#      Convierte -es un filtro adaptativo- de lectura en medicion.
#   B. ABLACION del gate: DualNoGate con g fijo en 1. Aisla si la
#      multiplicacion g*h_m es lo que produce la ventaja.
#   C. n=10 semillas en las 3 tareas de interaccion, en vez de 3.
#      Con n=3 y LSTM mostrando 72% de dispersion no hay intervalo.
#   D. Las tareas, releidas: el target de Gated es |x|*c, o sea
#      RECTIFICACION por referencia retenida. Se agrega una tarea nueva
#      de control, LinearScale (x*c sin rectificar), para separar
#      -no lineal en x- de -multiplicativo-.
#
# Guarda incremental: si la sesion muere, lo corrido sobrevive.
import os, json, math, time
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F

T0 = time.time()
OUT = "/kaggle/working"
os.makedirs(OUT, exist_ok=True)
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
N_SEEDS = 10
BATCH = 64
LR = 1e-3
print("device=", DEVICE, " seeds=", N_SEEDS, flush=True)

def set_seed(s):
    torch.manual_seed(s); np.random.seed(s)
    if torch.cuda.is_available(): torch.cuda.manual_seed_all(s)

def count_params(m):
    return sum(p.numel() for p in m.parameters() if p.requires_grad)

def welch(a, b):
    a, b = np.array(a), np.array(b)
    ma, mb = a.mean(), b.mean()
    va, vb = a.var(ddof=1), b.var(ddof=1)
    if va + vb < 1e-15: return 0.0, 1.0, 0.0
    se = math.sqrt(va/len(a) + vb/len(b))
    t = (ma - mb) / max(se, 1e-15)
    p = math.erfc(abs(t)/math.sqrt(2))
    sp = math.sqrt(((len(a)-1)*va + (len(b)-1)*vb) / max(len(a)+len(b)-2, 1))
    return float(t), float(p), float((ma-mb)/max(sp,1e-15))

# =====================================================================
# MODELOS - copiados verbatim del notebook original
# =====================================================================
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

class DualNoGate(DualBrain):
    """ABLACION: el gate se reemplaza por 1. Todo lo demas identico."""
    def forward(self, xs, h=None, probe=False):
        T,B,_ = xs.shape
        if h is None: h = xs.new_zeros(B, self.h_m)
        out = []
        for t in range(T):
            hr = self.react(xs[t])
            hm, _ = self.cell(self.enc(xs[t]), h); h = hm
            out.append(self.head(torch.cat([hr, hm],-1)))
        return torch.stack(out)

class GRUModel(nn.Module):
    def __init__(self, ind, outd, hidden_dim=16):
        super().__init__()
        self.hd = hidden_dim
        self.gru = nn.GRUCell(ind, hidden_dim)
        self.head = nn.Linear(hidden_dim, outd)
    def forward(self, xs, h=None):
        T,B,_ = xs.shape
        if h is None: h = xs.new_zeros(B, self.hd)
        out = []
        for t in range(T):
            h = self.gru(xs[t], h); out.append(self.head(h))
        return torch.stack(out)

class LSTMModel(nn.Module):
    def __init__(self, ind, outd, hidden_dim=12):
        super().__init__()
        self.hd = hidden_dim
        self.lstm = nn.LSTMCell(ind, hidden_dim)
        self.head = nn.Linear(hidden_dim, outd)
    def forward(self, xs, h=None):
        T,B,_ = xs.shape
        h = xs.new_zeros(B,self.hd); c = xs.new_zeros(B,self.hd)
        out = []
        for t in range(T):
            h,c = self.lstm(xs[t],(h,c)); out.append(self.head(h))
        return torch.stack(out)

class MinGRUModel(nn.Module):
    def __init__(self, ind, outd, hidden_dim=18):
        super().__init__()
        self.hd = hidden_dim
        self.Wz = nn.Linear(ind+hidden_dim, hidden_dim)
        self.Wh = nn.Linear(ind+hidden_dim, hidden_dim)
        self.head = nn.Linear(hidden_dim, outd)
    def forward(self, xs, h=None):
        T,B,_ = xs.shape
        if h is None: h = xs.new_zeros(B, self.hd)
        out = []
        for t in range(T):
            xh = torch.cat([xs[t],h],-1)
            z = torch.sigmoid(self.Wz(xh))
            h = (1-z)*h + z*torch.tanh(self.Wh(xh))
            out.append(self.head(h))
        return torch.stack(out)

class LTCModel(nn.Module):
    def __init__(self, ind, outd, hidden_dim=18):
        super().__init__()
        self.hd = hidden_dim
        self.Wi = nn.Linear(ind, hidden_dim, bias=False)
        self.Wr = nn.Linear(hidden_dim, hidden_dim, bias=False)
        self.tau = nn.Linear(ind+hidden_dim, hidden_dim)
        nn.init.constant_(self.tau.bias, -2.0)
        self.head = nn.Linear(hidden_dim, outd)
    def forward(self, xs, h=None):
        T,B,_ = xs.shape
        if h is None: h = xs.new_zeros(B, self.hd)
        out = []
        for t in range(T):
            t_ = torch.sigmoid(self.tau(torch.cat([xs[t],h],-1)))
            h = (1-t_)*h + t_*torch.sigmoid(self.Wi(xs[t])+self.Wr(h))
            out.append(self.head(h))
        return torch.stack(out)

def calibrate(ind, outd, target=1400):
    best_db, best_d = None, 99999
    for hr in range(8,40):
        for hm in range(4,20):
            p = count_params(DualBrain(ind,outd,hr,hm))
            if abs(p-target) < best_d: best_db=(hr,hm,p); best_d=abs(p-target)
    def find_h(Cls):
        best_h, best_d = 4, 99999
        for h in range(4,50):
            p = count_params(Cls(ind,outd,hidden_dim=h))
            if abs(p-target)<best_d: best_h,best_d=h,abs(p-target)
        return best_h
    cfg = {"DualBrain": {"h_r":best_db[0],"h_m":best_db[1]},
           "DualNoGate": {"h_r":best_db[0],"h_m":best_db[1]},
           "GRU": {"hidden_dim":find_h(GRUModel)},
           "LSTM": {"hidden_dim":find_h(LSTMModel)},
           "MinGRU": {"hidden_dim":find_h(MinGRUModel)},
           "LTC": {"hidden_dim":find_h(LTCModel)}}
    fac = {"DualBrain": lambda: DualBrain(ind,outd,**cfg["DualBrain"]),
           "DualNoGate": lambda: DualNoGate(ind,outd,**cfg["DualNoGate"]),
           "GRU": lambda: GRUModel(ind,outd,**cfg["GRU"]),
           "LSTM": lambda: LSTMModel(ind,outd,**cfg["LSTM"]),
           "MinGRU": lambda: MinGRUModel(ind,outd,**cfg["MinGRU"]),
           "LTC": lambda: LTCModel(ind,outd,**cfg["LTC"])}
    print("  presupuesto objetivo", target, flush=True)
    for n,f in fac.items():
        print("   ", n.ljust(11), count_params(f()), cfg[n], flush=True)
    return fac, cfg

# =====================================================================
# TAREAS. Las tres primeras son verbatim del notebook. La cuarta es nueva.
# =====================================================================
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

RES = {"meta": {"device": str(DEVICE), "n_seeds": N_SEEDS, "batch": BATCH, "lr": LR,
                "torch": torch.__version__}, "cfg": {}, "bench": {}, "bode": {}}
def save():
    with open(os.path.join(OUT, "paper_dualbrain.json"), "w") as f:
        json.dump(RES, f, indent=1)

# BARRIDO DE h_m EN MultiCue
#
# El benchmark de anoche dio en MultiCue: DualBrain 0.000326 contra
# LSTM 0.000081, o sea DualBrain pierde 4x, y se reporto como limitacion
# de la arquitectura con dos referencias.
#
# Pero calibrate() es una busqueda ciega sobre (h_r, h_m) que minimiza la
# distancia a 1400 parametros sin saber que h_m ES el banco de memoria.
# Verificado a mano: en MultiCue elige h_m cerca de 5, o sea CINCO slots
# de memoria para DOS referencias, y en Gated (una referencia) elige 13.
# El recorte de presupuesto cayo exactamente sobre el mecanismo.
#
# Los competidores tienen un solo hidden, asi que el mismo presupuesto no
# les quita nada estructural. Parejo en PARAMETROS, despareja en MEMORIA.
#
# El barrido puede refutar mi hipotesis:
#   si el MSE mejora al subir h_m, era el presupuesto
#   si no mejora, era la arquitectura y mi hipotesis se cae

HM_GRID = [5, 6, 8, 10, 13, 16]
TARGET = 1400
SPEC = TAREAS["MultiCue"]
IND = SPEC["ind"]
STEPS = SPEC["steps"]
GEN = SPEC["gen"]

def hr_for_hm(ind, outd, hm, target):
    best_hr, best_d, best_p = 8, 999999999, 0
    for hr in range(6, 60):
        p = count_params(DualBrain(ind, outd, hr, hm))
        if abs(p - target) < best_d:
            best_hr, best_d, best_p = hr, abs(p - target), p
    return best_hr, best_p

def train_eval(factory, seeds=N_SEEDS):
    mses = []
    for s in range(seeds):
        set_seed(s)
        m = factory().to(DEVICE)
        m.train()
        opt = torch.optim.Adam(m.parameters(), lr=LR)
        for _ in range(STEPS):
            o, tg, mk = GEN(BATCH, dev=DEVICE)
            out = m(o)
            loss = ((out - tg) ** 2).squeeze(-1) * mk
            loss = loss.sum() / max(mk.sum(), 1)
            opt.zero_grad()
            loss.backward()
            nn.utils.clip_grad_norm_(m.parameters(), 1.0)
            opt.step()
        m.eval()
        with torch.no_grad():
            o, tg, mk = GEN(2000, dev=DEVICE)
            out = m(o)
            mse = (((out - tg) ** 2).squeeze(-1) * mk).sum() / max(mk.sum(), 1)
            mses.append(float(mse.item()))
    return mses

print("", flush=True)
print("=" * 68, flush=True)
print("  BARRIDO DE h_m EN MultiCue", flush=True)
print("  n =", N_SEEDS, "semillas por punto. Presupuesto objetivo", TARGET, flush=True)
print("=" * 68, flush=True)

RES2 = {"meta": {"n_seeds": N_SEEDS, "target": TARGET, "hm_grid": HM_GRID,
                 "steps": STEPS, "batch": BATCH, "lr": LR,
                 "device": str(DEVICE), "torch": torch.__version__},
        "puntos": [], "referencias": {}}

def save2():
    f = open(os.path.join(OUT, "hm_sweep.json"), "w")
    json.dump(RES2, f)
    f.close()

print("", flush=True)
print("  REFERENCIAS al mismo presupuesto:", flush=True)
for nm, Cls in (("LSTM", LSTMModel), ("GRU", GRUModel), ("MinGRU", MinGRUModel)):
    bh, bd = 4, 999999999
    for h in range(4, 60):
        p = count_params(Cls(IND, 1, hidden_dim=h))
        if abs(p - TARGET) < bd:
            bh, bd = h, abs(p - TARGET)
    pr = count_params(Cls(IND, 1, hidden_dim=bh))
    t0 = time.time()
    ms = train_eval(lambda C=Cls, H=bh: C(IND, 1, hidden_dim=H))
    a = np.array(ms)
    RES2["referencias"][nm] = {"hidden_dim": bh, "params": int(pr), "mse": ms,
                               "mean": float(a.mean()), "sd": float(a.std(ddof=1))}
    print("    " + nm.ljust(8) + " hidden=" + str(bh).rjust(3) + "  params=" + str(pr).rjust(5)
          + "  MSE=" + format(a.mean(), ".6f") + " +-" + format(a.std(ddof=1), ".6f")
          + "  [" + format((time.time() - t0) / N_SEEDS, ".0f") + "s/seed]", flush=True)
    save2()

print("", flush=True)
print("  DualBrain barriendo h_m:", flush=True)
print("    h_m  h_r  params      MSE          sd      vs_LSTM", flush=True)
lstm_mean = RES2["referencias"]["LSTM"]["mean"]
for hm in HM_GRID:
    hr, pr = hr_for_hm(IND, 1, hm, TARGET)
    t0 = time.time()
    ms = train_eval(lambda A=hr, B=hm: DualBrain(IND, 1, A, B))
    a = np.array(ms)
    ratio = float(a.mean() / lstm_mean) if lstm_mean > 0 else float("inf")
    RES2["puntos"].append({"h_m": hm, "h_r": hr, "params": int(pr), "mse": ms,
                           "mean": float(a.mean()), "sd": float(a.std(ddof=1)),
                           "vs_lstm": ratio})
    print("    " + str(hm).rjust(3) + "  " + str(hr).rjust(3) + "  " + str(pr).rjust(5)
          + "   " + format(a.mean(), ".6f") + "  " + format(a.std(ddof=1), ".6f")
          + "   " + format(ratio, ".2f") + "x" + ("  GANA" if ratio < 1.0 else "")
          + "  [" + format((time.time() - t0) / N_SEEDS, ".0f") + "s/seed]", flush=True)
    save2()

print("", flush=True)
print("=" * 68, flush=True)
print("  VEREDICTO", flush=True)
print("=" * 68, flush=True)
pts = RES2["puntos"]
base = None
for p in pts:
    if p["h_m"] == 5:
        base = p
best = pts[0]
for p in pts:
    if p["mean"] < best["mean"]:
        best = p
if base is not None:
    print("  h_m=5, lo que eligio el calibrador original: MSE="
          + format(base["mean"], ".6f") + "  vs LSTM=" + format(base["vs_lstm"], ".2f") + "x", flush=True)
print("  mejor punto: h_m=" + str(best["h_m"]) + "  h_r=" + str(best["h_r"])
      + "  MSE=" + format(best["mean"], ".6f") + "  vs LSTM=" + format(best["vs_lstm"], ".2f") + "x", flush=True)
if base is not None and best["mean"] > 0:
    print("  mejora contra el punto original: " + format(base["mean"] / best["mean"], ".2f") + "x", flush=True)
    wt, wp = welch(base["mse"], best["mse"])[:2]
    print("  Welch h_m=5 contra h_m=" + str(best["h_m"]) + ": t=" + format(wt, ".2f")
          + "  p=" + format(wp, ".2e"), flush=True)
print("", flush=True)
if best["vs_lstm"] < 1.0:
    print("  HIPOTESIS CONFIRMADA: con memoria suficiente DualBrain gana en", flush=True)
    print("  MultiCue. La limitacion correcta del paper no es que pierde con", flush=True)
    print("  dos referencias, sino que necesita un slot de memoria por referencia.", flush=True)
else:
    print("  HIPOTESIS REFUTADA: ni con h_m=" + str(best["h_m"]) + " DualBrain alcanza al", flush=True)
    print("  LSTM en MultiCue. La limitacion del paper queda como esta y es de la", flush=True)
    print("  arquitectura, no del presupuesto.", flush=True)
RES2["veredicto"] = {"mejor_hm": best["h_m"], "mejor_mse": best["mean"],
                     "vs_lstm": best["vs_lstm"], "confirmada": bool(best["vs_lstm"] < 1.0)}
save2()
print("", flush=True)
print("FIN  minutos=" + format((time.time() - T0) / 60.0, ".1f"), flush=True)
print("FINHM", flush=True)
