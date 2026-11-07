import subprocess, sys, time, os
A = '/workspace/a1/v2/g1/mem'
conf = [('flywire', 'entero', 'pesado', '1000', '50', '20261107'),
        ('banc', 'cerebro', 'pesado', '1000', '50', '20261107'),
        ('banc', 'entero', 'liviano', '1000', '50', '20261107')]
with open(A + '/corrida.log', 'w') as f:
    for c in conf:
        t = time.time()
        r = subprocess.run([sys.executable, A + '/g1_memoria_nulo.py', c[0], c[1], c[2], A, c[3], c[4], c[5]],
                           stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        f.write('%s rc=%d %.1f s\n' % (' '.join(c), r.returncode, time.time() - t))
        if r.stdout:
            f.write(r.stdout[-3000:] + '\n')
        f.flush()
    f.write('TERMINADO\n')
