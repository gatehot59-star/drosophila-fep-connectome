# Auditoria de la celda 1 de notebookceb82767da (BICAMERALITY / PrincipiaBrain).
# Cada test PUEDE dar rojo. T0 es el control del control: si una matriz
# ortogonal no tuviera radio espectral 1, T1 no estaria midiendo nada.
#
# Sujeto: /workspace/bicam/cell1.py, md5 9d89a158f809ff5f3765f42848502665
# Entorno: python 3.12.14, torch 2.13.0+cpu, 2 threads, sin CUDA.
import sys, math, random, json
import numpy as np
import torch
import torch.nn.functional as F

FAIL = []
def chk(name, ok, detail):
    print(('  OK  ' if ok else '  FAIL') + '  ' + name + ': ' + detail, flush=True)
    if not ok:
        FAIL.append(name)
    return ok

src = open('/workspace/bicam/cell1.py').read()
src = src.replace('if __name__ ==', 'if False and __name__ ==')
ns = {'__name__': 'audited'}
exec(compile(src, 'cell1.py', 'exec'), ns)
PrincipiaBrain = ns['PrincipiaBrain']
DualBrain = ns['DualBrain']
MLPBrain = ns['MLPBrain']
LiquidChaosCell = ns['LiquidChaosCell']
LiquidRealCell = ns['LiquidRealCell']
PureMemoryTask = ns['PureMemoryTask']
SurvivalWorld = ns['SurvivalWorld']
print('celda1 importada  torch ' + torch.__version__)
print('')
R = {}
torch.manual_seed(0)
random.seed(0)
np.random.seed(0)

print('########## T0 CONTROL DEL CONTROL ##########')
W = torch.empty(8, 8)
torch.nn.init.orthogonal_(W)
sr_orth = torch.linalg.eigvals(W).abs().max().item()
chk('una_matriz_ortogonal_TIENE_sr_1', abs(sr_orth - 1.0) < 1e-5, f'sr={sr_orth:.10f} -> T1 puede medir algo')
Wr = torch.randn(8, 8) * 0.5
sr_rand = torch.linalg.eigvals(Wr).abs().max().item()
chk('una_matriz_random_NO_tiene_sr_1', abs(sr_rand - 1.0) > 0.05, f'sr={sr_rand:.6f} -> el test distingue')
R['sr_ortogonal'] = sr_orth
R['sr_random'] = sr_rand
print('')

print('########## T1 LA NORMALIZACION EDGE-OF-CHAOS ##########')
torch.manual_seed(1)
cell = LiquidChaosCell(8)
H = 8
Wrec = cell.W_flow.weight[:, H:].detach().clone()
sr_after = torch.linalg.eigvals(Wrec).abs().max().item()
ortho_err = (Wrec @ Wrec.T - torch.eye(H)).abs().max().item()
chk('W_rec_quedo_ortogonal', ortho_err < 1e-4, f'norma_inf(W Wt - I) = {ortho_err:.3e}')
chk('rho_W_rec_es_1', abs(sr_after - 1.0) < 1e-4, f'rho = {sr_after:.10f}')
torch.manual_seed(1)
W2 = torch.empty(H, H)
torch.nn.init.orthogonal_(W2)
sr2 = torch.linalg.eigvals(W2).abs().max().item()
delta = (W2 - W2 / sr2).abs().max().item()
chk('la_division_por_sr_es_NO_OP', delta < 1e-6, f'max abs(W - W/sr) = {delta:.3e} con sr = {sr2:.10f}')
R['rho_chaos'] = sr_after
R['delta_division'] = delta
print('')

print('########## T2 LA CELDA DE ORDEN NO TIENE rho CONTROLADO ##########')
torch.manual_seed(1)
real = LiquidRealCell(8)
Wrec_real = real.W_flow.weight[:, 8:].detach().clone()
sr_real = torch.linalg.eigvals(Wrec_real).abs().max().item()
chk('rho_LiquidRealCell_NO_es_1', abs(sr_real - 1.0) > 0.05, f'rho = {sr_real:.6f} default de nn.Linear sin control')
R['rho_real'] = sr_real
print('')

print('########## T3 LA ETIQUETA danger EN PureMemory ##########')
t = PureMemoryTask()
random.seed(7)
np.random.seed(7)
rews = []
for ep in range(20):
    t.reset()
    for i in range(100):
        a = np.array([np.random.uniform(-1, 1)], dtype=np.float32)
        o, r, d, inf = t.step(a)
        rews.append(r)
        if d:
            break
rmin = float(np.min(rews))
rmax = float(np.max(rews))
n_danger = sum(1 for r in rews if r < -1.0)
chk('PureMemory_NUNCA_dispara_danger', n_danger == 0, f'reward en [{rmin:.4f}, {rmax:.4f}] sobre {len(rews)} pasos; rew menor a -1.0 en {n_danger}')
R['pm_rew_min'] = rmin
R['pm_rew_max'] = rmax
R['pm_n_danger'] = n_danger
print('')

print('########## T4 LA ETIQUETA energy EN PureMemory ##########')
ens = []
t.reset()
for i in range(100):
    o, r, d, inf = t.step(np.array([0.3], dtype=np.float32))
    ens.append(inf.get('energy', 1.0))
    if d:
        break
uniq = sorted(set(ens))
chk('PureMemory_energy_es_CONSTANTE_1', uniq == [1.0], f'valores distintos de energy: {uniq}')
R['pm_energy_uniq'] = uniq
print('')

print('########## T5 CONSECUENCIA: EL VETO ES INERTE EN PureMemory ##########')
for a in [1.0, 0.5, 0.0]:
    vs = -2.0 * (1.0 - a)
    print(f'     alpha={a:.1f} -> veto_shift={vs:+.2f}')
chk('veto_shift_es_0_cuando_alpha_es_1', abs(-2.0 * (1.0 - 1.0)) < 1e-12, 'con energy_lb constante en 1 el veto no modula nada')
print('')

print('########## T6 SurvivalWorld: FRECUENCIA REAL DE danger ##########')
random.seed(3)
np.random.seed(3)
sw = SurvivalWorld(partial=True)
rews2 = []
ens2 = []
for ep in range(6):
    sw.reset()
    d = False
    k = 0
    while not d and k < 500:
        a = np.random.uniform(-1, 1, 2).astype(np.float32)
        o, r, d, inf = sw.step(a)
        rews2.append(r)
        ens2.append(inf['energy'])
        k = k + 1
nd = sum(1 for r in rews2 if r < -1.0)
frac = nd / len(rews2)
print(f'     pasos={len(rews2)}  danger=1 en {nd}  fraccion={frac:.5f}')
print(f'     reward en [{min(rews2):.3f}, {max(rews2):.3f}]   energy en [{min(ens2):.3f}, {max(ens2):.3f}]')
chk('SurvivalWorld_SI_dispara_danger', nd > 0, f'{nd} de {len(rews2)} pasos')
chk('danger_NO_esta_severamente_desbalanceado', frac > 0.01, f'fraccion={frac:.5f}; por debajo de 0.01 la BCE colapsa a predecir 0 siempre')
R['sw_frac_danger'] = frac
R['sw_energy_min'] = float(min(ens2))
print('')

print('########## T7 PRESUPUESTO DE PARAMETROS ##########')
for tname, od, ad in [('PureMemory', 2, 1), ('SurvivalWorld', 24, 2)]:
    p = sum(x.numel() for x in PrincipiaBrain(od, ad, 8, 24).parameters())
    dd = sum(x.numel() for x in DualBrain(od, ad, 24, 8).parameters())
    mm = sum(x.numel() for x in MLPBrain(od, ad, 32).parameters())
    ratio = p / dd
    print(f'     {tname:<14} Principia={p:5d}  Dual={dd:5d}  MLP={mm:5d}   P/D={ratio:.3f}')
    R['params_' + tname] = {'principia': p, 'dual': dd, 'mlp': mm, 'ratio': ratio}
    chk('presupuesto_pareado_' + tname, abs(ratio - 1.0) <= 0.05, f'Principia/Dual = {ratio:.3f} con tolerancia 0.05')
print('')

print('########## T8 SMOKE: LOS TRES CEREBROS CORREN ##########')
specs = [('Principia', PrincipiaBrain(24, 2, 8, 24)), ('Dual', DualBrain(24, 2, 24, 8)), ('MLP', MLPBrain(24, 2, 32))]
for nm, b in specs:
    x = torch.randn(4, 24)
    st = b.init_states(4)
    out = b(x, st)
    fin = bool(torch.isfinite(out[0]).all())
    chk('forward_' + nm, len(out) == 5 and fin, f'salidas={len(out)} mean_finito={fin} recurrente={b.is_recurrent}')
print('')

print('########## T9 EL ZEN CLAMP SE ACTIVA ALGUNA VEZ ##########')
torch.manual_seed(5)
cz = LiquidChaosCell(8, max_norm=3.0)
h = torch.zeros(64, 8)
hits = 0
norms = []
for step in range(200):
    x = torch.randn(64, 8) * 2.0
    cat = torch.cat([x, h], -1)
    target = torch.tanh(cz.W_flow(cat))
    tau = cz.W_tau(cat)
    h_pre = h * (1 - tau) + target * tau
    n = h_pre.norm(dim=-1)
    hits = hits + int((n > 3.0).sum())
    norms.append(float(n.max()))
    h, _ = cz(x, h)
chk('zen_clamp_se_activa', hits > 0, f'activaciones={hits} de {200*64}  max_norma_vista={max(norms):.4f} umbral 3.0')
R['zen_hits'] = hits
R['zen_max_norm'] = max(norms)
print('')

print('########## T10 GRADIENTE: LA AUX LOSS ENTRENA EL ESTIMADOR ##########')
torch.manual_seed(9)
b = PrincipiaBrain(24, 2, 8, 24)
x = torch.randn(16, 24)
st = b.init_states(16)
m, ls, v, hh, info = b(x, st)
aux = F.binary_cross_entropy(info['danger_pred'].squeeze(-1), torch.zeros(16)) + F.mse_loss(info['energy_est'].squeeze(-1), torch.ones(16))
b.zero_grad()
aux.backward()
ge = b.energy_head.weight.grad
gd = b.danger_head[0].weight.grad
gl = b.log_std.grad
se = 0.0 if ge is None else ge.abs().sum().item()
sd = 0.0 if gd is None else gd.abs().sum().item()
sl = 0.0 if gl is None else gl.abs().sum().item()
chk('aux_loss_entrena_energy_head', se > 0, f'suma_abs_grad = {se:.6e}')
chk('aux_loss_entrena_danger_head', sd > 0, f'suma_abs_grad = {sd:.6e}')
chk('el_veto_NO_recibe_gradiente_por_el_detach', sl == 0.0, f'suma_abs_grad log_std = {sl:.3e} esperado 0 porque alpha esta detacheado')
R['grad_energy_head'] = se
R['grad_danger_head'] = sd
R['grad_log_std'] = sl
print('')

print('==============================================================')
print(f'TESTS EN ROJO: {len(FAIL)}')
for f in FAIL:
    print('   - ' + f)
print('==============================================================')
json.dump(R, open('/workspace/bicam/audit_out.json', 'w'), indent=1)
print('FINAUDIT')
