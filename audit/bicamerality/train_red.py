# Entrenamiento REDUCIDO: 3 cerebros x 2 semillas x 40 episodios.
# NO alcanza para comparar arquitecturas (el original usa 500 ep x 3 semillas).
# Su unico proposito es verificar que el loop PPO + aux loss corre end to end.
import torch, random, numpy as np, time, json
src = open('cell1.py').read().replace('if __name__ ==', 'if False and __name__ ==')
ns = {'__name__': 'a'}
exec(compile(src, 'c', 'exec'), ns)
PB = ns['PrincipiaBrain']
DB = ns['DualBrain']
MB = ns['MLPBrain']
PM = ns['PureMemoryTask']
train = ns['train']
N_EP = 40
MS = 256
SEEDS = [42, 123]
out = {}
for nm, mk in [('Princip', lambda: PB(2, 1, 8, 24)), ('Dual', lambda: DB(2, 1, 24, 8)), ('MLP', lambda: MB(2, 1, 32))]:
    out[nm] = []
    for sd in SEEDS:
        torch.manual_seed(sd)
        random.seed(sd)
        np.random.seed(sd)
        t0 = time.time()
        res = train(mk(), PM(), n_ep=N_EP, min_steps=MS, name=nm, seed_id=sd)
        al = [a for a in res['align'][-10:]]
        out[nm].append({'seed': sd, 'align_final': float(np.mean(al)), 'R_final': float(np.mean(res['r'][-10:])), 'secs': time.time() - t0})
print('')
print('=========== RESULTADO REDUCIDO  n_ep=40  seeds=2 ===========')
for nm in out:
    a = [x['align_final'] for x in out[nm]]
    r = [x['R_final'] for x in out[nm]]
    s = sum(x['secs'] for x in out[nm])
    print(f'{nm:>8}  align={np.mean(a):.4f} +-{np.std(a):.4f}   R={np.mean(r):7.2f}   {s:.0f}s')
json.dump(out, open('train_reducido.json', 'w'), indent=1)
print('FINTRAIN')
