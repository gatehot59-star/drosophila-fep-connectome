"""DBC3-v4 - las mejoras que la auditoria de la v3 justifica, con su A/B pareado.

QUE CAMBIA Y POR QUE. Cada cambio cierra un hallazgo MEDIDO de la auditoria del
nucleo de la v3, y ninguno se acepta sin que el A/B lo respalde.

 M-1  EL GATE PASA A SER SIMETRICO.  (cierra A-6)
      v3: cat = [r, g*hm]            el gate modula la memoria y NUNCA el reflejo
      v4: cat = [(1-g_r)*r, g_m*hm]  se puede atenuar cualquiera de las dos vias
      Por que importa: en DelayedClass los pasos del medio son ruido puro, y en
      la v3 esos 36 canales de reflejo llegan al head sin atenuacion posible.

 M-2  LA NORMALIZACION SALE DEL CAMINO DE tau.  (cierra A-2, el hallazgo grande)
      v3: hm = (1-tau)*hm + tau*f ; hm = LN(hm)
          MEDIDO: la norma post-LN es 4.4720 para tau=0.02 Y para tau=0.95. O sea
          que tau elige la DIRECCION de la memoria pero NO su ESCALA, y la escala
          es justo lo que un LTC dice controlar.
      v4: f = LN(f) ; hm = (1-tau)*hm + tau*f
          Se normaliza el CANDIDATO, no el estado. La integracion vuelve a ser un
          filtro pasabajos de verdad, y tau recupera el control de la magnitud.

 M-3  COTA DECLARADA EN VEZ DE EMERGENTE.  (cierra A-3)
      Con M-2 el estado ya no lo fija el LN, asi que hay que acotarlo a proposito.
      hm se acota con tanh suave a +-CLIP. El otro motor del proyecto (motor.py)
      hace exactamente esto y lo testea; aca la cota era un efecto colateral.

 M-4  BIAS EN W_in Y W_res.  (cierra A-4)
      Sin bias no se puede desplazar el punto de operacion de tanh, que es donde
      un LTC decide entre integrar y saturar. Cuesta 2*m parametros y se descuenta
      del presupuesto para que la comparacion siga siendo a params iguales.

 M-5  EL EVALUADOR HONESTO.  (cierra el defecto que ya se midio en el grafico)
      - piso por tarea MEDIDO (clase mas frecuente), no un 8.3% unico
      - se reporta ventaja sobre el piso, no un cociente de accuracies
      - se elimina ratio = d/max(l, 0.01): denominador que puede morir
      - semillas PAREADAS: los tres modelos ven la misma secuencia de datos
      - se reporta la dispersion entre semillas, no solo la media

LO QUE NO SE TOCA, a proposito: el presupuesto de parametros igualado, el assert
que verifica el conteo analitico, la evaluacion con semilla fija y restauracion
del RNG. Eso ya estaba bien en la v3 y romperlo seria retroceder.

Uso:
    python3 dbc3_v4.py        # requiere dbc3_lib.py en el mismo directorio

dbc3_lib.py es dbc3_benchmark.py cortado justo antes de `tasks_cfg`, sin tocar
ninguna linea de logica. Se usa el sujeto exacto y no una replica.
"""
import copy
import math

import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F

import dbc3_lib as L

CLIP = 3.0


class V4Config:
    """Config de la v4. Cuenta los parametros analiticamente, como la v3."""

    def __init__(self, d_in, d_out, h_m, h_r):
        self.d_in, self.d_out, self.h_m, self.h_r = d_in, d_out, h_m, h_r

    def param_count(self):
        d, o, m, r = self.d_in, self.d_out, self.h_m, self.h_r
        return (r*d + r + r*r + r          # via rapida
                + m*d + m                   # encoder
                + m*m + m + m*m + m         # W_in + b_in, W_res + b_res  (M-4)
                + m*(m*2) + m               # tau learner
                + m + m                     # ln gamma/beta
                + m*(r+m) + m               # gate de memoria
                + r*(r+m) + r               # gate de reflejo            (M-1)
                + o*(r+m) + o)              # head

    def __repr__(self):
        return ("d_in=%d d_out=%d h_m=%d h_r=%d params=%d"
                % (self.d_in, self.d_out, self.h_m, self.h_r, self.param_count()))


class DBC3v4(nn.Module):
    """DBC3 con gate simetrico, LN sobre el candidato y estado acotado."""

    def __init__(self, cfg):
        super().__init__()
        self.cfg = cfg
        d, o, m, r = cfg.d_in, cfg.d_out, cfg.h_m, cfg.h_r
        self.W_r1 = nn.Parameter(torch.empty(r, d)); self.b_r1 = nn.Parameter(torch.zeros(r))
        self.W_r2 = nn.Parameter(torch.empty(r, r)); self.b_r2 = nn.Parameter(torch.zeros(r))
        self.W_enc = nn.Parameter(torch.empty(m, d)); self.b_enc = nn.Parameter(torch.zeros(m))
        self.W_in = nn.Parameter(torch.empty(m, m)); self.b_in = nn.Parameter(torch.zeros(m))
        self.W_res = nn.Parameter(torch.empty(m, m)); self.b_res = nn.Parameter(torch.zeros(m))
        self.W_tau = nn.Parameter(torch.empty(m, m * 2))
        self.b_tau = nn.Parameter(torch.full((m,), -2.0))
        self.ln_gamma = nn.Parameter(torch.ones(m)); self.ln_beta = nn.Parameter(torch.zeros(m))
        self.W_gate = nn.Parameter(torch.empty(m, r + m)); self.b_gate = nn.Parameter(torch.zeros(m))
        self.W_rgate = nn.Parameter(torch.empty(r, r + m)); self.b_rgate = nn.Parameter(torch.zeros(r))
        self.W_head = nn.Parameter(torch.empty(o, r + m)); self.b_head = nn.Parameter(torch.zeros(o))
        for n, p in self.named_parameters():
            if n.startswith('W_'):
                nn.init.xavier_uniform_(p)

    def _step(self, x, hm):
        t = torch.tanh(F.linear(x, self.W_r1, self.b_r1))
        r = torch.tanh(F.linear(t, self.W_r2, self.b_r2))
        e = L.gelu_c(F.linear(x, self.W_enc, self.b_enc))
        tau = torch.sigmoid(F.linear(torch.cat([e, hm], -1), self.W_tau, self.b_tau))
        f = torch.tanh(F.linear(e, self.W_in, self.b_in)
                       + F.linear(hm, self.W_res, self.b_res))
        # M-2: el LN va sobre el CANDIDATO, antes de integrar
        mu = f.mean(-1, keepdim=True)
        var = ((f - mu) ** 2).mean(-1, keepdim=True)
        f = self.ln_gamma * (f - mu) / (var + 1e-5).sqrt() + self.ln_beta
        hm = (1.0 - tau) * hm + tau * f
        # M-3: cota declarada, suave para no matar el gradiente
        hm = CLIP * torch.tanh(hm / CLIP)
        # M-1: gate simetrico
        g_m = torch.sigmoid(F.linear(torch.cat([r, hm], -1), self.W_gate, self.b_gate))
        g_r = torch.sigmoid(F.linear(torch.cat([r, hm], -1), self.W_rgate, self.b_rgate))
        cat = torch.cat([(1.0 - g_r) * r, g_m * hm], -1)
        return F.linear(cat, self.W_head, self.b_head), hm

    def forward(self, x, hm=None):
        B, T, _ = x.shape
        if hm is None:
            hm = x.new_zeros(B, self.cfg.h_m)
        outs = []
        for t in range(T):
            lo, hm = self._step(x[:, t], hm)
            outs.append(lo)
        return torch.stack(outs, 1), hm


def measured_floor(task, n_batches=6, seed=99999):
    """Piso REAL: accuracy del predictor que siempre dice la clase mas frecuente.

    Este es el numero que la v3 reemplazo por un 8.3% unico para las cinco tareas,
    y el error llego a 43.1 puntos en XORMemory.
    """
    st, sn = torch.random.get_rng_state(), np.random.get_state()
    torch.manual_seed(seed); np.random.seed(seed)
    finals = []
    for _ in range(n_batches):
        _, tgt, _ = task.batch()
        finals.append(tgt[:, -1].numpy())
    torch.random.set_rng_state(st); np.random.set_state(sn)
    f = np.concatenate(finals)
    vals, cnts = np.unique(f, return_counts=True)
    return float(cnts.max()) / len(f), int(len(vals))


def train(model, task, epochs, lr=3e-3, data_seed=0):
    """Entrena. data_seed fija la SECUENCIA DE DATOS para que sea pareada.

    Los tres modelos de una misma semilla ven exactamente los mismos batches, lo
    que convierte la comparacion en pareada y saca la varianza de los datos de la
    ecuacion. La v3 no lo hacia: cada modelo sorteaba su propia secuencia.
    """
    opt = torch.optim.Adam(model.parameters(), lr=lr)
    sched = torch.optim.lr_scheduler.CosineAnnealingLR(opt, T_max=epochs, eta_min=lr * 0.01)
    best, best_state = 0.0, None
    for ep in range(epochs):
        torch.manual_seed(data_seed * 100003 + ep)
        np.random.seed((data_seed * 100003 + ep) % (2 ** 31))
        x, tgt, w = task.batch()
        logits, _ = model(x)
        loss = torch.tensor(0.0)
        ws = 0.0
        for t in range(x.size(1)):
            if w[t] > 0:
                loss = loss + w[t] * F.cross_entropy(logits[:, t], tgt[:, t])
                ws += float(w[t])
        loss = loss / max(ws, 1.0)
        if torch.isnan(loss):
            break
        opt.zero_grad(); loss.backward()
        nn.utils.clip_grad_norm_(model.parameters(), 1.0)
        opt.step(); sched.step()
        with torch.no_grad():
            acc = float((logits[:, -1].argmax(-1) == tgt[:, -1]).float().mean())
        if acc > best:
            best, best_state = acc, copy.deepcopy(model.state_dict())
    if best_state is not None:
        model.load_state_dict(best_state)
    return best


def evaluate(model, task, n_batches=20, seed=99999):
    """Evalua con semilla fija y restaura el RNG. Igual que la v3: eso estaba bien."""
    model.eval()
    st, sn = torch.random.get_rng_state(), np.random.get_state()
    torch.manual_seed(seed); np.random.seed(seed)
    ok = tot = 0
    with torch.no_grad():
        for _ in range(n_batches):
            x, tgt, _ = task.batch()
            logits, _ = model(x)
            ok += int((logits[:, -1].argmax(-1) == tgt[:, -1]).sum())
            tot += x.size(0)
    torch.random.set_rng_state(st); np.random.set_state(sn)
    return ok / max(tot, 1)


def match_params(target, d_in, d_out, h_r):
    """Busca h_m para que la v4 quede lo mas cerca posible del presupuesto.

    La v4 agrega el gate de reflejo y dos bias, asi que con el mismo h_m tendria
    MAS parametros que la v3 y el A/B mediria tamano en vez de arquitectura. Se
    baja h_m hasta que el presupuesto cierre.
    """
    best, best_d = None, 10 ** 9
    for m in range(2, 60):
        c = V4Config(d_in, d_out, m, h_r)
        d = abs(c.param_count() - target)
        if d < best_d:
            best, best_d = c, d
    return best


def main():
    cfg3 = L.DBC3Config(36, 12, 20, 36)
    target = cfg3.param_count()
    cfg4 = match_params(target, 36, 12, 36)
    lstm_h = L.find_lstm_h(36, 12, target)

    # Verificacion de que los conteos analiticos NO mienten. Puede dar rojo.
    n3 = sum(p.numel() for p in L.DBC3Motor(cfg3).parameters())
    n4 = sum(p.numel() for p in DBC3v4(cfg4).parameters())
    nl = sum(p.numel() for p in L.LSTMBaseline(36, 12, lstm_h).parameters())
    assert n3 == cfg3.param_count(), "v3: conteo analitico != real"
    assert n4 == cfg4.param_count(), "v4: conteo analitico != real (%d vs %d)" % (n4, cfg4.param_count())

    print("=" * 90)
    print("A/B PAREADO  v3  vs  v4  vs  LSTM   a presupuesto de parametros igualado")
    print("=" * 90)
    print("  v3   %s   reales=%d" % (cfg3, n3))
    print("  v4   %s   reales=%d   (h_m bajado de 20 a %d para pagar el gate nuevo)"
          % (cfg4, n4, cfg4.h_m))
    print("  LSTM h=%d  params=%d  reales=%d" % (lstm_h, L.lstm_param_count(36, 12, lstm_h), nl))
    spread = 100.0 * (max(n3, n4, nl) - min(n3, n4, nl)) / min(n3, n4, nl)
    print("  dispersion del presupuesto: %.2f%%   %s"
          % (spread, "OK, comparable" if spread < 5 else "DEMASIADO: no comparable"))
    print()

    # Se corren las DOS tareas que la medicion de pisos mostro DISCRIMINATIVAS.
    # Tracking (1.04x) y ThermalPredict (1.09x) quedaron medidos como empates: los
    # dos modelos superan el piso por ~86 puntos, asi que no separan arquitecturas
    # y gastar computo ahi es medir sobre el objetivo equivocado. ContextSwitch
    # queda afuera por costo: su generador es un loop Python de B*T=3840 por batch.
    # Las tres exclusiones se declaran; ninguna es un resultado escondido.
    TASKS = [("XORMemory", lambda c: L.XORMemoryTask(c, 15, 128), 140),
             ("DelayedClass", lambda c: L.DelayedClassTask(c, 25, 128), 140)]
    SEEDS = [42, 1042, 2042]

    print("%-14s %6s %5s | %-22s %-22s %-22s" %
          ("tarea", "piso", "clas", "v3 (media+-sd)", "v4 (media+-sd)", "LSTM (media+-sd)"))
    print("-" * 118)
    summary = []
    for tname, mk, epochs in TASKS:
        t3, t4 = mk(cfg3), mk(cfg4)
        floor, k = measured_floor(t3)
        a3, a4, al = [], [], []
        for s in SEEDS:
            torch.manual_seed(s); np.random.seed(s)
            m3 = L.DBC3Motor(cfg3); train(m3, t3, epochs, data_seed=s); a3.append(evaluate(m3, t3))
            torch.manual_seed(s); np.random.seed(s)
            m4 = DBC3v4(cfg4); train(m4, t4, epochs, data_seed=s); a4.append(evaluate(m4, t4))
            torch.manual_seed(s); np.random.seed(s)
            ml = L.LSTMBaseline(36, 12, lstm_h); train(ml, t3, epochs, data_seed=s); al.append(evaluate(ml, t3))
        f = lambda v: "%5.1f%% +-%4.1f" % (100 * np.mean(v), 100 * np.std(v))
        print("%-14s %5.1f%% %5d | %-22s %-22s %-22s" %
              (tname, 100 * floor, k, f(a3), f(a4), f(al)))
        summary.append((tname, floor, a3, a4, al))
    print()

    print("=" * 90)
    print("VENTAJA SOBRE EL PISO MEDIDO, en puntos. Sin cocientes que puedan morir")
    print("=" * 90)
    print("  %-14s %12s %12s %12s | %s" % ("tarea", "v3", "v4", "LSTM", "v4 vs v3 (pareado)"))
    for tname, floor, a3, a4, al in summary:
        d3 = 100 * (np.mean(a3) - floor); d4 = 100 * (np.mean(a4) - floor)
        dl = 100 * (np.mean(al) - floor)
        paired = np.array(a4) - np.array(a3)
        sd = float(np.std(paired, ddof=1)) if len(paired) > 1 else float("nan")
        if sd > 0:
            tstat = float(np.mean(paired)) / (sd / math.sqrt(len(paired)))
            ver = "%+.1f pts, t=%.2f, n=%d" % (100 * np.mean(paired), tstat, len(paired))
        else:
            ver = "%+.1f pts, sd=0 NO TESTEABLE" % (100 * np.mean(paired))
        print("  %-14s %+11.1f %+11.1f %+11.1f | %s" % (tname, d3, d4, dl, ver))
    print()
    print("  Con n=3 semillas ningun t es concluyente y NO se declara significancia.")
    print("  Lo que si es medible: el signo y el tamano del efecto pareado.")
    print()
    print("=" * 90)
    print("VEREDICTO derivado (conclusion, no medicion)")
    print("=" * 90)
    wins = sum(1 for _, _, a3, a4, _ in summary if np.mean(a4) > np.mean(a3))
    print("  la v4 gana en %d de %d tareas" % (wins, len(summary)))
    print("  y paga %d parametros menos de memoria (h_m %d->%d) por el gate simetrico"
          % (cfg3.h_m - cfg4.h_m, cfg3.h_m, cfg4.h_m))


if __name__ == "__main__":
    main()
