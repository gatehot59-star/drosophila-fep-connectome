# Parche a la celda 1 de notebookceb82767da (BICAMERALITY / PrincipiaBrain).
#
# POR QUE ESTE ARCHIVO Y NO EL RESULTADO: cell1_fixed.py seria obra derivada
# de codigo cuya procedencia NO esta establecida (ver
# docs/agents/respuestas/2026-08-23-013). Este script lo regenera de forma
# determinista a partir del original, y fix.diff contiene solo los cambios.
#
# Uso:
#   1. extraer la celda 1 a cell1.py (ver README.md de esta carpeta)
#   2. verificar md5 9d89a158f809ff5f3765f42848502665
#   3. python3 patch.py   -> escribe cell1_fixed.py
#      md5 esperado: 57c91b7f5c30fd9e1ad4c02fbf340226
import hashlib, sys

src = open('cell1.py').read()
print('sujeto md5  ' + hashlib.md5(src.encode()).hexdigest())
N = 0

# ---------- FIX 1: max_norm alcanzable + guard del guard ----------
OLD1 = '''    def __init__(self, H, max_norm=3.0):
        super().__init__()
        self.H = H
        self.max_norm = max_norm'''

NEW1 = '''    def __init__(self, H, max_norm=None, clamp_frac=0.97):
        super().__init__()
        self.H = H
        # FIX 1. La actualizacion h = h*(1-tau) + tanh(.)*tau con tau en (0,1)
        # deja cada componente en [-1,1], asi que la norma esta acotada por
        # sqrt(H). Con H=8 la cota es 2.8284 y el max_norm original era 3.0:
        # la rama del clamp era INALCANZABLE. Medido: 0 de 12800 activaciones,
        # y 0 tambien con estimulo x100, donde la norma llega a 2.828427 exacto.
        self.norm_bound = float(H) ** 0.5
        if max_norm is None:
            max_norm = clamp_frac * self.norm_bound
        if max_norm >= self.norm_bound:
            raise ValueError(
                'max_norm=' + repr(max_norm) + ' es INALCANZABLE: la cota '
                'analitica con H=' + repr(H) + ' es sqrt(H)=' +
                format(self.norm_bound, '.4f') + '. Un guard cuya rama nunca '
                'se ejecuta no protege nada y hace creer que si.')
        self.max_norm = max_norm
        self.clamp_hits = 0
        self.clamp_calls = 0'''

if OLD1 not in src:
    print('FALLO: no encontre el bloque 1')
    sys.exit(1)
src = src.replace(OLD1, NEW1, 1)
N += 1
print('fix 1 aplicado: max_norm auto + ValueError si es inalcanzable')

# ---------- FIX 1b: instrumentar el clamp para que sea medible ----------
OLD1B = '''        # Resilience Zen (Principia eq 4.6): soft norm clamp
        h_norm = torch.norm(h_new, dim=-1, keepdim=True)
        scale = torch.where(h_norm > self.max_norm,
                            self.max_norm / (h_norm + 1e-8),
                            torch.ones_like(h_norm))
        h_new = h_new * scale'''

NEW1B = '''        # Resilience Zen (Principia eq 4.6): soft norm clamp
        h_norm = torch.norm(h_new, dim=-1, keepdim=True)
        over = h_norm > self.max_norm
        self.clamp_calls += int(h_norm.numel())
        self.clamp_hits += int(over.sum().item())
        scale = torch.where(over,
                            self.max_norm / (h_norm + 1e-8),
                            torch.ones_like(h_norm))
        h_new = h_new * scale'''

if OLD1B not in src:
    print('FALLO: no encontre el bloque 1b')
    sys.exit(1)
src = src.replace(OLD1B, NEW1B, 1)
N += 1
print('fix 1b aplicado: contadores clamp_hits / clamp_calls')

# ---------- FIX 2: el veto se puede desactivar ----------
OLD2 = '    def __init__(self, obs_dim, act_dim, H_chaos=8, H_order=24):'
NEW2 = '    def __init__(self, obs_dim, act_dim, H_chaos=8, H_order=24, veto_enabled=True):'
if OLD2 not in src:
    print('FALLO: no encontre la firma de PrincipiaBrain')
    sys.exit(1)
src = src.replace(OLD2, NEW2, 1)
N += 1

OLD2B = '        self.H_chaos = H_chaos'
NEW2B = '''        self.H_chaos = H_chaos
        # FIX 2. Si la etiqueta energy no lleva informacion, el estimador
        # regresiona contra una constante y su salida NO mide energia. Usarla
        # igual como veto produce un handicap de exploracion permanente:
        # medido, alpha se queda en 0.37-0.48 durante 240 episodios, o sea
        # 29-35 por ciento del std nominal. Con veto_enabled=False el shift es 0.
        self.veto_enabled = veto_enabled'''
if OLD2B not in src:
    print('FALLO: no encontre self.H_chaos')
    sys.exit(1)
src = src.replace(OLD2B, NEW2B, 1)
N += 1

OLD2C = 'veto_shift = -2.0 * (1.0 - alpha)'
NEW2C = 'veto_shift = (-2.0 * (1.0 - alpha)) if self.veto_enabled else torch.zeros_like(alpha)'
if OLD2C not in src:
    print('FALLO: no encontre veto_shift')
    sys.exit(1)
src = src.replace(OLD2C, NEW2C, 1)
N += 1
print('fix 2 aplicado: veto_enabled propagado a veto_shift')

# ---------- FIX 3: guard de tautologia por termino ----------
OLD3A = 'def ppo_seq_update(brain, opt, chunks, epochs=4, clip=0.2,'
NEW3A = '''AUX_GUARD = {'danger_no_testeable': 0, 'energy_no_testeable': 0,
             'danger_usada': 0, 'energy_usada': 0}


def ppo_seq_update(brain, opt, chunks, epochs=4, clip=0.2,'''
if OLD3A not in src:
    print('FALLO: no encontre ppo_seq_update')
    sys.exit(1)
src = src.replace(OLD3A, NEW3A, 1)
N += 1

OLD3B = '''                aux_loss = torch.tensor(0.0, device=device)
                if danger_preds:
                    dp = torch.stack(danger_preds, dim=1)
                    ep = torch.stack(energy_preds, dim=1)
                    aux_loss = (F.binary_cross_entropy(dp, danger_lb)
                                + F.mse_loss(ep, energy_lb))
                    loss = loss + aux_weight * aux_loss'''

NEW3B = '''                # FIX 3. Guard de tautologia, POR TERMINO. Si una etiqueta
                # tiene sd == 0 en el batch, ese termino no puede ensenar nada:
                # regresionar contra una constante solo empuja el estimador a
                # un valor fijo. Se cuenta como NO TESTEABLE y se excluye.
                # Medido en PureMemory: danger = 0 en 2000 de 2000 pasos y
                # energy = 1.0 constante. Los dos terminos eran tautologicos.
                aux_loss = torch.tensor(0.0, device=device)
                if danger_preds:
                    dp = torch.stack(danger_preds, dim=1)
                    ep = torch.stack(energy_preds, dim=1)
                    terms = []
                    if float(danger_lb.std()) > 0.0:
                        terms.append(F.binary_cross_entropy(dp, danger_lb))
                        AUX_GUARD['danger_usada'] += 1
                    else:
                        AUX_GUARD['danger_no_testeable'] += 1
                    if float(energy_lb.std()) > 0.0:
                        terms.append(F.mse_loss(ep, energy_lb))
                        AUX_GUARD['energy_usada'] += 1
                    else:
                        AUX_GUARD['energy_no_testeable'] += 1
                    if terms:
                        aux_loss = sum(terms)
                        loss = loss + aux_weight * aux_loss'''

if OLD3B not in src:
    print('FALLO: no encontre el bloque de survival loss')
    sys.exit(1)
src = src.replace(OLD3B, NEW3B, 1)
N += 1
print('fix 3 aplicado: guard de tautologia por termino + contadores')

open('cell1_fixed.py', 'w').write(src)
print('')
print('reemplazos aplicados: ' + repr(N) + ' de 7')
print('cell1_fixed.py  bytes ' + repr(len(src)) + '  md5 ' + hashlib.md5(src.encode()).hexdigest())
