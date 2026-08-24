# Trayectoria del veto alpha en PureMemory, donde la etiqueta energy es
# constante 1.0 y la etiqueta danger nunca se dispara.
import torch, random, numpy as np, time, json, math
src = open('cell1.py').read().replace('if __name__ ==', 'if False and __name__ ==')
ns = {'__name__': 'a'}
exec(compile(src, 'c', 'exec'), ns)
PB = ns['PrincipiaBrain']
PM = ns['PureMemoryTask']
train = ns['train']
torch.manual_seed(42)
random.seed(42)
np.random.seed(42)
t0 = time.time()
res = train(PB(2, 1, 8, 24), PM(), n_ep=240, min_steps=256, name='Princip', seed_id=42)
a = [x for x in res['alpha'] if x >= 0]
g = [x for x in res['gate'] if x >= 0]
print('')
print('TRAYECTORIA DEL VETO en PureMemory (energy_lb CONSTANTE = 1.0)')
print('bloque_de_ep   alpha_medio   veto_shift   factor_sobre_std   gate_medio')
B = 40
for i in range(0, len(a) - B + 1, B):
    am = float(np.mean(a[i:i+B]))
    gm = float(np.mean(g[i:i+B]))
    vs = -2.0 * (1.0 - am)
    print(f'{i:4d}-{i+B:<4d}      {am:.4f}       {vs:+.3f}        {math.exp(vs):.4f}        {gm:.4f}')
print('')
print(f'alpha primeros 40 = {np.mean(a[:40]):.4f}   ultimos 40 = {np.mean(a[-40:]):.4f}')
print(f'gate  primeros 40 = {np.mean(g[:40]):.4f}   ultimos 40 = {np.mean(g[-40:]):.4f}')
print(f'align primeros 40 = {np.mean(res["align"][:40]):.4f}   ultimos 40 = {np.mean(res["align"][-40:]):.4f}')
print(f'segundos = {time.time()-t0:.0f}')
json.dump({'alpha': a, 'gate': g, 'align': res['align']}, open('veto_traj.json', 'w'))
print('FINVETO')
