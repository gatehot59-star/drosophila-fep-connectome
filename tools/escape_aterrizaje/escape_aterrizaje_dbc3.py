#!/usr/bin/env python3
"""Escape o aterrizaje segun el estado de vuelo: motivo de FlyWire en SparseLTC + DBC3 (2026-10-12-003).

Sujeto: motivo recortado de FlyWire v783 (anotaciones 17fc577): por lado, las 4 LC4 y las 4 LPLC2
con mas sinapsis sobre DNp01 y las 4 LPLC4 con mas sinapsis sobre DNp07; salidas DNp01 y DNp07 de
cada lado (28 neuronas). DNp10 queda afuera: casi no recibe de estas visuales (medido antes de fijar).
Dinamica SparseLTC con estado real y tau fija heterogenea (sin entrenar):
  z <- (1 - t) z + t tanh(W z + x),  t = dt / tau,  dt = 0.02, tau_i en [0.06, 0.18], W con rho 0.9.
Tarea (Ache 2019): al principio llega una senal de estado (volando +1 / en el piso -1) y se apaga;
despues de una espera, aparece algo que se acerca por un lado o un objeto que pasa sin acercarse.
Respuesta al final: 0 nada (objeto que pasa), 1 escapar de la izquierda, 2 escapar de la derecha,
3 aterrizar (volando, cualquier lado). El lector ve solo las 4 descendentes y la senal de estado.
Brazos: DBC3 (ecuaciones de DBC3Motor de dbc3_lib.py), LSTM con el mismo presupuesto, lector sin
memoria (control negativo), regla a mano (rival clasico) y DBC3 sobre 16 SL (barajado de grado que
conserva el lado).
Salida: 0 completo; 2 md5 de datos distinto del pin; 3 instrumento invalido.
"""
import argparse, hashlib, json, os, platform, sys, time
import numpy as np
import pandas as pd
import torch
import torch.nn as nn
import torch.nn.functional as F
from scipy import stats

MD5_CONN = "3d802fd542b5d18570ba1ba0bb0abed9"
MD5_ANNOT = "719904abad876c68ace1b5690c9b9b63"
T, DT, RHO, K = 40, 0.02, 0.9, 4
N_TRAIN, N_TEST = 4096, 3000
SEMILLAS = [0, 1, 2, 3]
N_SL = 16


def md5(p):
    h = hashlib.md5()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


# ---------------- motivo ----------------
def construir_motivo(conn, annot):
    a = pd.read_csv(annot, sep="\t", dtype=str, usecols=["root_id", "cell_type", "side"])
    a["root_id"] = a.root_id.astype(np.int64)
    c = pd.read_parquet(conn, columns=["Presynaptic_ID", "Postsynaptic_ID", "Connectivity", "Excitatory"])
    sel = []
    for tipo, blanco in (("LC4", "DNp01"), ("LPLC2", "DNp01"), ("LPLC4", "DNp07")):
        bl = a.root_id[a.cell_type == blanco]
        for lado in ("left", "right"):
            v = a[(a.cell_type == tipo) & (a.side == lado)].copy()
            m = c.Presynaptic_ID.isin(v.root_id) & c.Postsynaptic_ID.isin(bl)
            s = c[m].groupby("Presynaptic_ID").Connectivity.sum()
            v["s"] = v.root_id.map(s).fillna(0)
            v = v.sort_values(["s", "root_id"], ascending=[False, True]).head(K)
            sel += [(int(r), tipo, lado, float(x)) for r, x in zip(v.root_id, v.s)]
    for tipo in ("DNp01", "DNp07"):
        for lado in ("left", "right"):
            r = a[(a.cell_type == tipo) & (a.side == lado)].root_id
            assert len(r) == 1, (tipo, lado, len(r))
            sel.append((int(r.iloc[0]), tipo, lado, 0.0))
    ids = [s[0] for s in sel]
    ix = {r: i for i, r in enumerate(ids)}
    sub = c[c.Presynaptic_ID.isin(ids) & c.Postsynaptic_ID.isin(ids)]
    aristas = [(ix[p], ix[q], float(w * e)) for p, q, w, e in sub.itertuples(index=False)]
    return sel, aristas


def matriz(n, aristas):
    W = np.zeros((n, n))
    for p, q, w in aristas:
        W[q, p] += w
    r = np.abs(np.linalg.eigvals(W)).max()
    return W * (RHO / r), r


def barajar_sl(aristas, lados, rng):
    """Permuta los destinos entre aristas del mismo bloque (lado pre, lado post): conserva grado de
    entrada y de salida de cada neurona y el lado de cada arista."""
    out = list(aristas)
    bloques = {}
    for k, (p, q, w) in enumerate(aristas):
        bloques.setdefault((lados[p], lados[q]), []).append(k)
    for ks in bloques.values():
        qs = [aristas[k][1] for k in ks]
        perm = rng.permutation(len(qs))
        for k, j in zip(ks, perm):
            out[k] = (aristas[k][0], qs[j], aristas[k][2])
    return out


def grados(n, aristas):
    gi, go = np.zeros(n, int), np.zeros(n, int)
    for p, q, _ in aristas:
        go[p] += 1
        gi[q] += 1
    return gi, go


# ---------------- tarea ----------------
def generar(n, seed, n_vis_lado):
    """Seis condiciones balanceadas: estado (vuelo, piso) x estimulo (izq, der, pasa)."""
    rng = np.random.default_rng(seed)
    cond = np.arange(n) % 6
    rng.shuffle(cond)
    vuelo = cond < 3
    est = cond % 3  # 0 izq, 1 der, 2 pasa
    y = np.where(est == 2, 0, np.where(vuelo, 3, np.where(est == 0, 1, 2)))
    cue = np.zeros((n, T))
    cue[:, 0:3] = np.where(vuelo, 1.0, -1.0)[:, None]
    drive = np.zeros((n, T, 2))  # por lado
    for i in range(n):
        t0 = rng.integers(15, 26)
        if est[i] < 2:
            amp = rng.uniform(0.6, 1.0)
            ramp = np.clip((np.arange(T) - t0 + 1) / 8.0, 0, 1) * amp
            drive[i, :, est[i]] = ramp
        else:
            amp = rng.uniform(0.3, 0.7)
            for t in range(t0, T):
                drive[i, t, ((t - t0) // 4) % 2] = amp
    ruido = rng.normal(0, 0.15, (n, T, 2 * n_vis_lado))
    return dict(y=y, cue=cue, drive=drive, ruido=ruido, vuelo=vuelo, est=est)


def simular(W, tau, lados_vis, d):
    n_neur = W.shape[0]
    n = len(d["y"])
    t_ = DT / tau
    z = np.zeros((n, n_neur))
    out = np.zeros((n, T, 4))
    nv = len(lados_vis)
    for t in range(T):
        x = np.zeros((n, n_neur))
        x[:, :nv] = d["drive"][:, t, :][:, lados_vis] + d["ruido"][:, t, :]
        z = (1 - t_) * z + t_ * np.tanh(z @ W.T + x)
        out[:, t, :] = z[:, nv:nv + 4]
    return out


def entradas(dn, d):
    return np.concatenate([dn, d["cue"][:, :, None]], axis=2).astype(np.float32)


# ---------------- lectores ----------------
def gelu_c(x):
    return x * torch.sigmoid(1.702 * x)


class DBC3Motor(nn.Module):
    """Ecuaciones copiadas de DBC3Motor en dbc3_lib.py (DBC3-v3, notebook de Kaggle)."""
    def __init__(self, d, o, m=20, r=36):
        super().__init__()
        self.m = m
        self.W_r1 = nn.Parameter(torch.empty(r, d)); self.b_r1 = nn.Parameter(torch.zeros(r))
        self.W_r2 = nn.Parameter(torch.empty(r, r)); self.b_r2 = nn.Parameter(torch.zeros(r))
        self.W_enc = nn.Parameter(torch.empty(m, d)); self.b_enc = nn.Parameter(torch.zeros(m))
        self.W_in = nn.Parameter(torch.empty(m, m)); self.W_res = nn.Parameter(torch.empty(m, m))
        self.W_tau = nn.Parameter(torch.empty(m, m * 2)); self.b_tau = nn.Parameter(torch.full((m,), -2.0))
        self.ln_gamma = nn.Parameter(torch.ones(m)); self.ln_beta = nn.Parameter(torch.zeros(m))
        self.W_gate = nn.Parameter(torch.empty(m, r + m)); self.b_gate = nn.Parameter(torch.zeros(m))
        self.W_head = nn.Parameter(torch.empty(o, r + m)); self.b_head = nn.Parameter(torch.zeros(o))
        for n_, p in self.named_parameters():
            if n_.startswith("W_"):
                nn.init.xavier_uniform_(p)

    def _step(self, x, hm):
        t = torch.tanh(F.linear(x, self.W_r1, self.b_r1))
        r = torch.tanh(F.linear(t, self.W_r2, self.b_r2))
        e = gelu_c(F.linear(x, self.W_enc, self.b_enc))
        tau = torch.sigmoid(F.linear(torch.cat([e, hm], -1), self.W_tau, self.b_tau))
        f = torch.tanh(F.linear(e, self.W_in) + F.linear(hm, self.W_res))
        hm = (1.0 - tau) * hm + tau * f
        mu = hm.mean(-1, keepdim=True)
        var = ((hm - mu) ** 2).mean(-1, keepdim=True)
        hm = self.ln_gamma * (hm - mu) / (var + 1e-5).sqrt() + self.ln_beta
        g = torch.sigmoid(F.linear(torch.cat([r, hm], -1), self.W_gate, self.b_gate))
        return F.linear(torch.cat([r, g * hm], -1), self.W_head, self.b_head), hm

    def forward(self, x):
        hm = x.new_zeros(x.shape[0], self.m)
        outs = []
        for t in range(x.shape[1]):
            lo, hm = self._step(x[:, t], hm)
            outs.append(lo)
        return torch.stack(outs, 1)


class LSTMLector(nn.Module):
    def __init__(self, d, o, h):
        super().__init__()
        self.lstm = nn.LSTM(d, h, batch_first=True)
        self.head = nn.Linear(h, o)

    def forward(self, x):
        return self.head(self.lstm(x)[0])


class SinMemoria(nn.Module):
    def __init__(self, d, o, h=64):
        super().__init__()
        self.net = nn.Sequential(nn.Linear(d, h), nn.Tanh(), nn.Linear(h, o))

    def forward(self, x):
        return self.net(x)


def n_params(m):
    return sum(p.numel() for p in m.parameters())


def lstm_h_para(d, o, objetivo):
    best = min(range(1, 200), key=lambda h: abs(4 * h * (d + h + 2) + h * o + o - objetivo))
    return best


def entrenar(modelo, xtr, ytr, xte, seed, iters, lr=3e-3, batch=256):
    torch.manual_seed(seed)
    rng = np.random.default_rng(1000 + seed)
    opt = torch.optim.Adam(modelo.parameters(), lr=lr)
    sch = torch.optim.lr_scheduler.CosineAnnealingLR(opt, T_max=iters, eta_min=lr * 0.01)
    Xtr, Ytr = torch.from_numpy(xtr), torch.from_numpy(ytr.astype(np.int64))
    for it in range(iters):
        b = torch.from_numpy(rng.integers(0, len(ytr), batch))
        lo = modelo(Xtr[b])[:, -5:, :]
        loss = F.cross_entropy(lo.reshape(-1, lo.shape[-1]), Ytr[b].repeat_interleave(5))
        opt.zero_grad(); loss.backward(); opt.step(); sch.step()
    with torch.no_grad():
        pred = modelo(torch.from_numpy(xte))[:, -1, :].argmax(-1).numpy()
    return pred


def nuevo(nombre, d, o, h_lstm, seed):
    torch.manual_seed(seed)  # la inicializacion depende solo de la semilla
    if nombre == "DBC3":
        return DBC3Motor(d, o)
    if nombre == "LSTM":
        return LSTMLector(d, o, h_lstm)
    return SinMemoria(d, o)


def regla_a_mano(dn_tr, dtr, dn_te, dte, onset_min=15):
    """Rival clasico: latch de la senal de estado; deteccion por umbral (calibrado en entrenamiento)
    del maximo de las 4 descendentes; lado por la diferencia izquierda menos derecha."""
    def rasgos(dn):
        pico = dn[:, onset_min:, :].max(axis=(1, 2))
        izq = dn[:, onset_min:, 0] + dn[:, onset_min:, 2]
        der = dn[:, onset_min:, 1] + dn[:, onset_min:, 3]
        return pico, (izq - der).sum(1)
    def clasif(pico, lado, vuelo, th):
        det = pico > th
        return np.where(~det, 0, np.where(vuelo, 3, np.where(lado > 0, 1, 2)))
    ptr, ltr = rasgos(dn_tr)
    vtr = dtr["cue"][:, 0] > 0
    cands = np.quantile(ptr, np.linspace(0.01, 0.99, 197))
    th = max(cands, key=lambda c: (clasif(ptr, ltr, vtr, c) == dtr["y"]).mean())
    pte, lte = rasgos(dn_te)
    return clasif(pte, lte, dte["cue"][:, 0] > 0, th), float(th)


def mcnemar(a_ok, b_ok):
    b = int((a_ok & ~b_ok).sum()); c = int((~a_ok & b_ok).sum())
    p = stats.binomtest(b, b + c, 0.5).pvalue if b + c else 1.0
    return b, c, p


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--conn", required=True); ap.add_argument("--annot", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--iters", type=int, default=400)
    ap.add_argument("--humo", action="store_true", help="corrida corta de humo: numeros sin valor")
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    torch.set_num_threads(2)
    t0 = time.time()
    print("# maquina: %s | %s | Python %s | numpy %s | torch %s" % (platform.node(), platform.platform(),
          platform.python_version(), np.__version__, torch.__version__))
    print("# md5 script = " + md5(os.path.abspath(__file__)))
    print("# fecha: " + time.strftime("%Y-%m-%d %H:%M:%S %z"))
    mc, ma = md5(a.conn), md5(a.annot)
    print("# md5 conn = %s | md5 annot = %s" % (mc, ma))
    if mc != MD5_CONN or ma != MD5_ANNOT:
        print("ABORTA: datos distintos del pin"); print("EXIT_RUN=2"); return 2
    if a.humo:
        print("# HUMO: corrida corta, estos numeros no valen")
    sel, aristas = construir_motivo(a.conn, a.annot)
    n = len(sel)
    lados = ["L" if s[2] == "left" else "R" for s in sel]
    for s in sel:
        print("MOTIVO root_id=%d tipo=%s lado=%s sinapsis_al_blanco=%d" % (s[0], s[1], s[2], s[3]))
    W, rho0 = matriz(n, aristas)
    ipsi = sum(lados[p] == lados[q] for p, q, _ in aristas)
    inh = sum(w < 0 for _, _, w in aristas)
    print("MOTIVO neuronas=%d aristas=%d sinapsis=%d inhibitorias=%d ipsilaterales=%d rho_crudo=%.4f" % (
        n, len(aristas), int(sum(abs(w) for _, _, w in aristas)), inh, ipsi, rho0))
    nv = n - 4
    lados_vis = np.array([0 if lados[i] == "L" else 1 for i in range(nv)])
    tau = 0.06 + 0.12 * np.random.default_rng(0).random(n)
    dtr, dte = generar(N_TRAIN, 1, nv // 2), generar(N_TEST, 2, nv // 2)
    # el ruido se genera por lado con nv//2 columnas por lado: lo reordeno a las nv visuales
    for d in (dtr, dte):
        orden = np.argsort(np.argsort(lados_vis, kind="stable"), kind="stable")
        d["ruido"] = d["ruido"][:, :, orden]
    iters = 15 if a.humo else a.iters
    semillas = SEMILLAS[:1] if a.humo else SEMILLAS
    n_sl = 2 if a.humo else N_SL

    dn_tr, dn_te = simular(W, tau, lados_vis, dtr), simular(W, tau, lados_vis, dte)
    xtr, xte = entradas(dn_tr, dtr), entradas(dn_te, dte)
    ytr, yte = dtr["y"], dte["y"]
    d_in, d_out = xtr.shape[2], 4
    p_dbc3 = n_params(DBC3Motor(d_in, d_out))
    h = lstm_h_para(d_in, d_out, p_dbc3)
    print("PARAMS DBC3=%d LSTM(h=%d)=%d SIN_MEMORIA=%d" % (p_dbc3, h, n_params(LSTMLector(d_in, d_out, h)),
          n_params(SinMemoria(d_in, d_out))))
    res = {"W": {}, "SL": [], "controles": {}}
    preds = {}
    for nom in ("DBC3", "LSTM", "SIN_MEMORIA"):
        for s in semillas:
            pr = entrenar(nuevo(nom, d_in, d_out, h, s), xtr, ytr, xte, s, iters)
            preds[(nom, s)] = pr
            acc = float((pr == yte).mean())
            res["W"].setdefault(nom, []).append(acc)
            por = [float((pr[yte == k] == k).mean()) for k in range(4)]
            print("W lector=%s semilla=%d acierto=%.4f por_clase(nada,esc_izq,esc_der,aterr)=%s" % (
                nom, s, acc, ",".join("%.3f" % x for x in por)))
    pr2 = entrenar(nuevo("DBC3", d_in, d_out, h, semillas[0]), xtr, ytr, xte, semillas[0], iters)
    repro = bool((pr2 == preds[("DBC3", semillas[0])]).all())
    print("CHEQUEO REPRODUCE DBC3 semilla=%d -> %s" % (semillas[0], repro))
    pm, th = regla_a_mano(dn_tr, dtr, dn_te, dte)
    acc_m = float((pm == yte).mean())
    print("W lector=REGLA_A_MANO umbral=%.4f acierto=%.4f por_clase=%s" % (th, acc_m, ",".join(
        "%.3f" % float((pm[yte == k] == k).mean()) for k in range(4))))
    res["W"]["REGLA_A_MANO"] = acc_m

    rng = np.random.default_rng(7)
    gi0, go0 = grados(n, aristas)
    guard_sl = True
    for k in range(n_sl):
        ar = barajar_sl(aristas, lados, rng)
        gi, go = grados(n, ar)
        distinto = sorted((p, q) for p, q, _ in ar) != sorted((p, q) for p, q, _ in aristas)
        ok = bool((gi == gi0).all() and (go == go0).all() and distinto and
                  all(lados[p] == lados[q] for p, q, _ in ar))
        guard_sl &= ok
        Ws, _ = matriz(n, ar)
        a_tr, a_te = simular(Ws, tau, lados_vis, dtr), simular(Ws, tau, lados_vis, dte)
        pr = entrenar(nuevo("DBC3", d_in, d_out, h, 100 + k), entradas(a_tr, dtr), ytr, entradas(a_te, dte), 100 + k, iters)
        acc = float((pr == yte).mean())
        pm_s, _ = regla_a_mano(a_tr, dtr, a_te, dte)
        res["SL"].append({"dbc3": acc, "regla": float((pm_s == yte).mean())})
        print("SL k=%d guarda=%s lector=DBC3 acierto=%.4f regla_a_mano=%.4f" % (k, ok, acc, res["SL"][-1]["regla"]))

    ok = lambda nom: [preds[(nom, s)] == yte for s in semillas]
    def comparar(a_, b_):
        bb = cc = 0; signos = []
        for x, y_ in zip(ok(a_), ok(b_) if b_ != "REGLA_A_MANO" else [pm == yte] * len(semillas)):
            b1, c1, _ = mcnemar(x, y_); bb += b1; cc += c1; signos.append(np.sign(b1 - c1))
        p = stats.binomtest(bb, bb + cc, 0.5).pvalue if bb + cc else 1.0
        if all(s_ > 0 for s_ in signos) and p < 0.05:
            v = "MEJOR"
        elif all(s_ < 0 for s_ in signos) and p < 0.05:
            v = "PEOR"
        else:
            v = "EMPATE"
        return bb, cc, p, v
    for pid, (x, y_) in {"H1_DBC3_vs_LSTM": ("DBC3", "LSTM"), "H2_DBC3_vs_SIN_MEMORIA": ("DBC3", "SIN_MEMORIA"),
                         "H4_DBC3_vs_REGLA_A_MANO": ("DBC3", "REGLA_A_MANO")}.items():
        bb, cc, p, v = comparar(x, y_)
        res[pid] = dict(gana_a=bb, gana_b=cc, p=p, veredicto=v)
        print("%s discordantes %d contra %d p=%.3g -> %s" % (pid, bb, cc, p, v))
    wv = res["W"]["DBC3"]; slv = [s["dbc3"] for s in res["SL"]]
    u = stats.mannwhitneyu(wv, slv, alternative="greater", method="exact")
    iguala = sum(s >= np.mean(wv) for s in slv)
    v3 = "W GANA" if u.pvalue < 0.05 else "W NO GANA"
    res["H3_W_vs_SL"] = dict(U=float(u.statistic), p=float(u.pvalue), sl_media=float(np.mean(slv)),
                             sl_max=float(np.max(slv)), sl_igualan_media_W=int(iguala), veredicto=v3)
    print("H3_W_vs_SL DBC3 W media=%.4f SL media=%.4f max=%.4f igualan=%d/%d U=%.1f p=%.4f -> %s" % (
        np.mean(wv), np.mean(slv), np.max(slv), iguala, len(slv), u.statistic, u.pvalue, v3))

    sm = float(np.mean(res["W"]["SIN_MEMORIA"])); dm = float(np.mean(wv))
    c_neg = sm <= 0.75 and dm - sm >= 0.10
    c_pos = acc_m >= 0.80
    valido = bool(c_neg and c_pos and guard_sl and repro)
    res["controles"] = dict(sin_memoria_media=sm, control_negativo=c_neg, regla_a_mano=acc_m,
                            control_positivo=c_pos, guarda_sl=guard_sl, reproduce=repro)
    print("CHEQUEO INSTRUMENTO control_negativo(sin_memoria<=0.75 y DBC3-sin_memoria>=0.10)=%s "
          "control_positivo(regla_a_mano>=0.80)=%s guarda_SL=%s reproduce=%s -> %s" % (
              c_neg, c_pos, guard_sl, repro, "VALIDO" if valido else "INVALIDO"))
    with open(os.path.join(a.out, "resultados.json"), "w") as fh:
        json.dump(res, fh, indent=1, sort_keys=True, default=float)
    print("escrito resultados.json md5=" + md5(os.path.join(a.out, "resultados.json")))
    print("# duracion_s=%.1f" % (time.time() - t0))
    rc = 0 if valido else 3
    print("EXIT_RUN=%d" % rc)
    return rc


if __name__ == "__main__":
    sys.exit(main())
