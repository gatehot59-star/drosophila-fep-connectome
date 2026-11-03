#!/usr/bin/env python3
"""comun_a1.py - BRAIN, 2026-11-03 (respuesta 2026-11-03-005).

Piezas compartidas de H_MECANISMO_RELEVOS16 / 009-A1 (enmienda 2026-11-02-010): contrato de semilla, eventos
externos, reglas de mascara, D' y huellas. Solo NumPy (y pyarrow para leer el parquet). Lo importan manifiesto_a1.py,
runner_a1.py, validar_a1.py y prueba_a1.py.
"""
import hashlib
import json

import numpy as np

PROTOCOLO = '009-A1'
DT_S = 1e-4                          # paso de 0,1 ms
NTICKS = 10000                       # lectura en [0, 1000 ms)
TASA_A = 150.0                       # Hz a cada miembro de la poblacion A
TASA_DRIVER = 50.0                   # Hz al driver, o a cada driver del hub
TASA_BLANCO = 25.0                   # Hz a cada miembro del D' fijo
N_REPLAY = 50                        # espigas por driver encendido en el banco C
DESPLAZAMIENTOS = {1: (0,), 2: (0, 100), 3: (0, 50, 100)}   # en ticks: 0/10 ms y 0/5/10 ms
SEMILLAS_PLAN = tuple(range(20))
SEMILLAS_HUMO = (900, 901)           # fuera del plan: no entran a ningun analisis
SUF_PRE = '_presinapticas_directas'

COMP_RELEVO = {'C0': [], 'Q1': ['Q1'], 'Q2': ['Q2'], 'Q3': ['Q3'], 'Q4': ['Q4'], 'QCOL': ['QCOL'],
               'Q1uQCOL': ['Q1', 'QCOL'], 'QXD': ['QXD'], 'Q1uQXD': ['Q1', 'QXD'], 'QWEAK': ['QWEAK'], 'SHAM': []}
COMP_CASCADA = {'ZA': ['ZA'], 'ZAuQ1': ['ZA', 'Q1'], 'ZAuQCOL': ['ZA', 'QCOL'], 'ZAuQ1uQCOL': ['ZA', 'Q1', 'QCOL']}
ORDEN_RELEVO = ('C0', 'Q1', 'Q2', 'Q3', 'Q4', 'QCOL', 'Q1uQCOL', 'QXD', 'Q1uQXD', 'QWEAK', 'SHAM')
ORDEN_CASCADA = ('ZA', 'ZAuQ1', 'ZAuQCOL', 'ZAuQ1uQCOL')


def texto_semilla(grupo, s, indice, rol):
    return '%s|%s|%d|%d|%s' % (PROTOCOLO, grupo, int(s), int(indice), rol)


def semilla(grupo, s, indice, rol):
    """Primeros 16 hexadecimales de SHA-256 del texto UTF-8, en base 16: 64 bits, sin truncar."""
    return int(hashlib.sha256(texto_semilla(grupo, s, indice, rol).encode('utf-8')).hexdigest()[:16], 16)


def eventos_bernoulli(seed, tasa_hz, nticks=NTICKS):
    """Evento en el tick k si u_k < tasa_Hz * 0,0001, con u = Generator(PCG64(seed)).random(nticks)."""
    u = np.random.Generator(np.random.PCG64(int(seed))).random(nticks)
    return np.flatnonzero(u < float(tasa_hz) * 0.0001).astype(np.int64)


def ticks_replay(seed, n=N_REPLAY, nticks=NTICKS):
    """n ticks sin reemplazo: los indices de los n menores de Generator(PCG64(seed)).random(nticks), ordenados."""
    u = np.random.Generator(np.random.PCG64(int(seed))).random(nticks)
    return np.sort(np.argsort(u, kind='stable')[:n]).astype(np.int64)


def eventos_grupo(grupo, s, fuentes, fsemilla=None):
    """fuentes: [[rol, indice, tasa_Hz o None], ...] en el orden del manifiesto. Devuelve [(rol, indice, ticks)]."""
    fs = fsemilla or semilla
    out = []
    for rol, idx, tasa in fuentes:
        sd = fs(grupo, s, idx, rol)
        t = ticks_replay(sd) if rol == 'replay' else eventos_bernoulli(sd, tasa)
        out.append((str(rol), int(idx), t))
    return out


def huella_eventos(evs):
    """sha256 de (rol, indice, cantidad, ticks) por fuente, en orden de (rol, indice)."""
    h = hashlib.sha256()
    for rol, idx, t in sorted(evs, key=lambda e: (e[0], int(e[1]))):
        t = np.asarray(t, dtype='<i8')
        h.update(('%s|%d|%d|' % (rol, int(idx), t.size)).encode())
        h.update(t.tobytes())
        h.update(b';')
    return h.hexdigest()


def huella_lista(v):
    """Formato de la evidencia de 010: sha256 de la lista JSON compacta y ordenada, mas LF."""
    w = sorted(int(t) for t in v)
    return hashlib.sha256((json.dumps(w, separators=(',', ':')) + '\n').encode()).hexdigest()


def huella_espigas(i, ticks):
    """sha256 del tren completo de la red: indices y ticks en el orden del SpikeMonitor."""
    h = hashlib.sha256()
    h.update(np.asarray(i, dtype='<i8').tobytes())
    h.update(b'|')
    h.update(np.asarray(ticks, dtype='<i8').tobytes())
    return h.hexdigest()


def sha_archivo(ruta):
    h = hashlib.sha256()
    with open(ruta, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''):
            h.update(b)
    return h.hexdigest()


def huella_contenido_npz(ruta):
    """sha256 de los arreglos (nombre, dtype, forma y bytes) en orden de nombre: no depende del zip."""
    z = np.load(ruta)
    h = hashlib.sha256()
    for k in sorted(z.files):
        a = z[k]
        h.update(k.encode() + b'|' + a.dtype.str.encode() + b'|' + str(a.shape).encode() + b'|')
        h.update(np.ascontiguousarray(a).tobytes())
    return h.hexdigest()


class Grafo:
    """Filas del parquet de Shiu en su orden: la fila k es la sinapsis k de create_model()."""

    def __init__(self, pre, post, w):
        self.pre = np.ascontiguousarray(pre, dtype=np.int32)
        self.post = np.ascontiguousarray(post, dtype=np.int32)
        self.w = np.ascontiguousarray(w, dtype=np.int32)
        self._de, self._a = {}, {}

    @classmethod
    def desde_parquet(cls, ruta):
        import pyarrow.parquet as pq
        cols = []
        for c in ('Presynaptic_Index', 'Postsynaptic_Index', 'Excitatory x Connectivity'):
            cols.append(np.asarray(pq.read_table(ruta, columns=[c]).column(0).to_numpy(), dtype=np.int32))
        return cls(*cols)

    def desde(self, i):
        i = int(i)
        if i not in self._de:
            self._de[i] = np.flatnonzero(self.pre == i).astype(np.int64)
        return self._de[i]

    def hacia(self, i):
        i = int(i)
        if i not in self._a:
            self._a[i] = np.flatnonzero(self.post == i).astype(np.int64)
        return self._a[i]


def _ids(G):
    return np.asarray(sorted(int(v) for v in G), dtype=np.int64)


def dprime(g, Dset, x, G):
    """D'(x, G): neuronas D elegibles con fila x->j de peso firmado negativo, menos G, desde el grafo intacto."""
    r = g.desde(x)
    r = r[(g.w[r] < 0) & Dset[g.post[r]]]
    t = np.unique(g.post[r]).astype(np.int64)
    return t[~np.isin(t, _ids(G))]


def m_fila(g, a, b):
    r = g.desde(a)
    return np.unique(r[g.post[r] == int(b)])


def m_q1(g, G, x):
    r = g.hacia(x)
    return np.unique(r[np.isin(g.pre[r], _ids(G))])


def m_q2(g, x):
    return np.unique(g.desde(x))


def m_q3(g, d):
    return np.unique(g.desde(d))


def m_q4(g, x, G):
    r = g.hacia(x)
    return np.unique(r[~np.isin(g.pre[r], _ids(G))])


def m_qcol(g, G, Dp):
    r = np.concatenate([g.desde(d) for d in _ids(G)])
    return np.unique(r[(g.w[r] > 0) & np.isin(g.post[r], np.asarray(Dp, dtype=np.int64))])


def m_qxd(g, x, Dp):
    r = g.desde(x)
    return np.unique(r[(g.w[r] < 0) & np.isin(g.post[r], np.asarray(Dp, dtype=np.int64))])


def m_qweak(g, Dset, x, G):
    """Fila excitatoria D elegible -> x de peso 1 a 5 fuera de G: la de mayor peso; empate, menor origen."""
    r = g.hacia(x)
    a = np.abs(g.w[r].astype(np.int64))
    ok = (g.w[r] > 0) & Dset[g.pre[r]] & ~np.isin(g.pre[r], _ids(G)) & (a >= 1) & (a <= 5)
    r, a = r[ok], a[ok]
    if r.size == 0:
        return np.zeros(0, dtype=np.int64)
    c = r[a == a.max()]
    return np.array([c[np.argmin(g.pre[c])]], dtype=np.int64)


def mascara_base(nombre, suj, g, Dset):
    """Filas de una mascara base por nombre, con la regla de 010 seccion 3."""
    x, G, Dp = suj['x'], suj['G'], suj['Dp']
    if nombre in ('Q1', 'Q1conj'):
        return m_q1(g, G, x)
    if nombre.startswith('Q1_'):
        return m_q1(g, [int(nombre[3:])], x)
    if nombre == 'Q2':
        return m_q2(g, x)
    if nombre == 'Q3':
        return m_q3(g, suj['d'])
    if nombre.startswith('Q3_'):
        return m_q3(g, int(nombre[3:]))
    if nombre in ('Q4', 'Q4conj'):
        return m_q4(g, x, G)
    if nombre == 'QCOL':
        return m_qcol(g, G, Dp)
    if nombre == 'QXD':
        return m_qxd(g, x, Dp)
    if nombre == 'QWEAK':
        return m_qweak(g, Dset, x, G)
    if nombre == 'ZA':
        a, b = suj['cascada_ZA']
        return m_fila(g, a, b)
    raise ValueError('mascara base desconocida: %s' % nombre)


def huella_mascara(g, filas):
    """n, suma de |peso| y sha256 de (filas, pre, post, peso): la suma sola no basta (010, seccion 8)."""
    f = np.unique(np.asarray(filas, dtype=np.int64))
    h = hashlib.sha256()
    for a in (f, g.pre[f], g.post[f], g.w[f]):
        h.update(np.asarray(a, dtype='<i8').tobytes())
        h.update(b'|')
    return {'n': int(f.size), 'abs': int(np.abs(g.w[f].astype(np.int64)).sum()), 'sha256': h.hexdigest()}


def filas_condicion(suj, cond, cache):
    partes = [np.asarray(cache[b], dtype=np.int64) for b in suj['composicion'][cond]]
    return np.unique(np.concatenate(partes)) if partes else np.zeros(0, dtype=np.int64)


def id_ensayo(suj, reg, cond, s):
    return '%s|%s|%s|%d' % (suj, reg, cond, int(s))
