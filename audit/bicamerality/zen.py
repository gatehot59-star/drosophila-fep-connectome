# Es alcanzable la rama del Zen clamp? Barrido de H.
# La actualizacion es h = h*(1-tau) + tanh(.)*tau con tau en (0,1), asi que
# cada componente queda en [-1,1] y la norma esta acotada por sqrt(H).
import math, torch, random, numpy as np, json, time
src = open('cell1.py').read().replace('if __name__ ==', 'if False and __name__ ==')
ns = {'__name__': 'a'}
exec(compile(src, 'c', 'exec'), ns)
LC = ns['LiquidChaosCell']
print('COTA ANALITICA: h = h*(1-tau) + tanh(.)*tau  con tau en (0,1)')
print('cada componente queda en [-1,1] => norma <= sqrt(H)')
print('')
print(' H   sqrt(H)   max_norm   alcanzable   max_visto_1000pasos')
for H in [4, 8, 9, 10, 16, 32]:
    torch.manual_seed(11)
    c = LC(H, max_norm=3.0)
    h = torch.zeros(128, H)
    mx = 0.0
    for s in range(1000):
        x = torch.randn(128, H) * 3.0
        with torch.no_grad():
            cat = torch.cat([x, h], -1)
            tg = torch.tanh(c.W_flow(cat))
            tau = c.W_tau(cat)
            hp = h * (1 - tau) + tg * tau
            mx = max(mx, float(hp.norm(dim=-1).max()))
            h, _ = c(x, h)
    alc = 'SI' if math.sqrt(H) > 3.0 else 'NO'
    print(f'{H:3d}   {math.sqrt(H):7.4f}   {3.0:8.1f}   {alc:>10}   {mx:19.4f}')
print('')
print('VEREDICTO: con H_chaos=8 la cota es sqrt(8)=2.8284 < 3.0')
print('=> la rama del clamp es INALCANZABLE por construccion, no por suerte')
