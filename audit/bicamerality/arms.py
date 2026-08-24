# Los tres brazos del veto, para saber si el guard de tautologia ALCANZA.
#   A: original, sin guard, veto ON
#   B: con guard, veto ON      -> el guard alcanza?
#   C: con guard, veto OFF     -> el fix completo
# Mas la verificacion de que el guard dispara donde debe y no donde no debe.
import torch, random, numpy as np, json, math, time


def load(p):
    s = open(p).read().replace('if __name__ ==', 'if False and __name__ ==')
    ns = {'__name__': 'a'}
    exec(compile(s, p, 'exec'), ns)
    return ns


OUT = {}
print('########## GUARD DE TAUTOLOGIA: DISPARA DONDE DEBE ##########', flush=True)
for tarea in ['PureMemory', 'SurvivalWorld']:
    FIX = load('cell1_fixed.py')
    torch.manual_seed(42)
    random.seed(42)
    np.random.seed(42)
    if tarea == 'PureMemory':
        env = FIX['PureMemoryTask']()
        nep = 20
        ms = 256
    else:
        env = FIX['SurvivalWorld'](partial=True)
        nep = 6
        ms = 512
    FIX['train'](FIX['PrincipiaBrain'](env.obs_dim, env.act_dim, 8, 24), env, n_ep=nep, min_steps=ms, name='P-' + tarea[:6], seed_id=42)
    g = FIX['AUX_GUARD']
    print('     ' + tarea.ljust(15) + ' danger: usada=' + repr(g['danger_usada']) + ' NO_TESTEABLE=' + repr(g['danger_no_testeable']) + '   energy: usada=' + repr(g['energy_usada']) + ' NO_TESTEABLE=' + repr(g['energy_no_testeable']), flush=True)
    OUT['guard_' + tarea] = dict(g)
print('', flush=True)
print('########## TRES BRAZOS DEL VETO  PureMemory 240ep seed42 ##########', flush=True)
ARMS = [('A_original', 'cell1.py', True), ('B_guard_veto_ON', 'cell1_fixed.py', True), ('C_guard_veto_OFF', 'cell1_fixed.py', False)]
for nm, path, veto in ARMS:
    NS = load(path)
    torch.manual_seed(42)
    random.seed(42)
    np.random.seed(42)
    if path == 'cell1.py':
        br = NS['PrincipiaBrain'](2, 1, 8, 24)
    else:
        br = NS['PrincipiaBrain'](2, 1, 8, 24, veto_enabled=veto)
    t0 = time.time()
    res = NS['train'](br, NS['PureMemoryTask'](), n_ep=240, min_steps=256, name=nm[:10], seed_id=42)
    a = [x for x in res['alpha'] if x >= 0]
    al = res['align']
    a0 = float(np.mean(a[:40]))
    a1 = float(np.mean(a[-40:]))
    vs0 = -2.0 * (1.0 - a0) if veto else 0.0
    vs1 = -2.0 * (1.0 - a1) if veto else 0.0
    OUT[nm] = {'alpha_ini': a0, 'alpha_fin': a1, 'veto_shift_ini': vs0, 'veto_shift_fin': vs1, 'factor_std_ini': math.exp(vs0), 'factor_std_fin': math.exp(vs1), 'align_ini': float(np.mean(al[:40])), 'align_fin': float(np.mean(al[-40:])), 'R_fin': float(np.mean(res['r'][-40:])), 'secs': time.time() - t0}
    print('     ' + nm.ljust(18) + ' alpha ' + format(a0, '.4f') + '->' + format(a1, '.4f') + '   factor_std ' + format(math.exp(vs0), '.4f') + '->' + format(math.exp(vs1), '.4f') + '   align ' + format(np.mean(al[:40]), '.4f') + '->' + format(np.mean(al[-40:]), '.4f') + '   [' + format(time.time() - t0, '.0f') + 's]', flush=True)
json.dump(OUT, open('arms.json', 'w'), indent=1)
print('', flush=True)
print('FINARMS', flush=True)
