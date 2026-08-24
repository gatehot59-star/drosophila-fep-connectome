# Distribucion real de la norma del estado, para calibrar max_norm con dato
# en vez de con un numero elegido a dedo.
import torch, numpy as np
s = open('cell1_fixed.py').read().replace('if __name__ ==', 'if False and __name__ ==')
ns = {'__name__': 'a'}
exec(compile(s, 'c', 'exec'), ns)
LC = ns['LiquidChaosCell']
print('DISTRIBUCION REAL DE LA NORMA DEL ESTADO  H=8  cota sqrt(8)=2.8284')
print('')
print('escala_x   p50      p99      p99.9     max      seeds')
allv = []
for esc in [0.5, 1.0, 2.0, 5.0, 20.0, 100.0]:
    vs = []
    for sd in [5, 17, 33]:
        torch.manual_seed(sd)
        c = LC(8)
        h = torch.zeros(256, 8)
        for st in range(300):
            x = torch.randn(256, 8) * esc
            with torch.no_grad():
                cat = torch.cat([x, h], -1)
                tg = torch.tanh(c.W_flow(cat))
                tau = c.W_tau(cat)
                hp = h * (1 - tau) + tg * tau
                vs.extend(hp.norm(dim=-1).tolist())
                h, _ = c(x, h)
    a = np.array(vs)
    allv.extend(vs)
    print(format(esc, '8.1f') + '   ' + format(np.percentile(a, 50), '.4f') + '   ' + format(np.percentile(a, 99), '.4f') + '   ' + format(np.percentile(a, 99.9), '.4f') + '   ' + format(a.max(), '.4f') + '     3')
A = np.array(allv)
print('')
print('GLOBAL sobre ' + repr(len(A)) + ' muestras:  p99.9=' + format(np.percentile(A, 99.9), '.4f') + '  max=' + format(A.max(), '.4f'))
print('cota analitica sqrt(8) = 2.8284')
print('')
print('CONSECUENCIA: cualquier umbral en (max_observado, 2.8284) es CODIGO MUERTO,')
print('y cualquier umbral por debajo del max_observado DISTORSIONA la dinamica normal.')
print('El clamp no puede ser a la vez inocuo y alcanzable.')
print('FINDIST')
