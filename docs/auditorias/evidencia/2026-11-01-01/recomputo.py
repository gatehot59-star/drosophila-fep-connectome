import re, numpy as np

print("== 1. Holm de H_REUSO con la funcion holm() copiada de reuso_mosca.py (blob 37b3583) ==")
def holm(ps):
    ps = np.asarray(ps, dtype=float)
    orden = np.argsort(ps)
    adj, acc = np.zeros(len(ps)), 0.0
    for r, i in enumerate(orden):
        acc = max(acc, min(1.0, (len(ps) - r) * ps[i]))
        adj[i] = acc
    return adj
p = (1 + 0) / (200 + 1.0)   # ningun nulo >= observado, N_NULO=200
print("p piso por permutacion = %.6f (log imprime 0.0050)" % p)
print("HOLM", " ".join("%.4f" % x for x in holm([p]*4)), "(log: HOLM 0.0199 0.0199 0.0199 0.0199)")

print("\n== 2. T1 contra su nulo, lineas crudas de reuso.log (blob ef631e9) ==")
for nom, obs, med, mx in [("FLYWIRE", 0.8835, 0.6823, 0.7462), ("BANC", 0.8260, 0.3472, 0.4744)]:
    print("%s T1=%.4f nulo_media=%.4f nulo_max=%.4f | obs-media=%+.4f obs/media=%.3f" % (nom, obs, med, mx, obs-med, obs/med))

print("\n== 3. Nucleo: tamano (SELLO-NUCLEO, blob 2a8190e) y lo que dice el mismo log (blob 86ce131) ==")
print("aristas 603219/4031897 = %.4f %%" % (100*603219/4031897))
print("sinapsis 9668248/16971919 = %.4f %%" % (100*9668248/16971919))
print("primaria W_nucleo-W_R2 = %+.4f (log -0.0459)" % (0.8894-0.9353))
print("nucleo real 0.9135 menos media SL 0.5913 = %+.4f ; menos media T 0.6869 = %+.4f" % (0.9135-0.5913, 0.9135-0.6869))
print("nucleo real 0.9135 menos max SL 0.7570 = %+.4f ; menos max T 0.7680 = %+.4f" % (0.9135-0.7570, 0.9135-0.7680))

print("\n== 4. Tabla beta por pares de tipos contra aristas agregadas ==")
tipos = 8453   # Schlegel et al. 2024, tipos anotados
aristas = 15091983
print("tipos^2 = %d ; aristas FlyWire agregadas = %d ; cociente = %.2f" % (tipos**2, aristas, tipos**2/aristas))

print("\n== 5. c2 de H_PARES_DATOS: donde el crudo alcanza al embudo, lineas crudas de agregado.log (blob 66c19d1) ==")
crudo = """CURVA c2 n=6 MOSCA_L=0.4508 [0.3000, 0.5797] CRUDO=0.4488 [0.2975, 0.6315] PCA_L=0.4092 [0.3000, 0.5065] PROY_L=0.4467 [0.3649, 0.5628] W_n=0.5225 (70 de 200) | W=0.9276
CURVA c2 n=12 MOSCA_L=0.5407 [0.3281, 0.7006] CRUDO=0.4729 [0.3000, 0.6270] PCA_L=0.4255 [0.3000, 0.5130] PROY_L=0.5245 [0.3000, 0.6830] W_n=0.5928 (170 de 200) | W=0.9276
CURVA c2 n=24 MOSCA_L=0.7255 [0.4000, 0.8088] CRUDO=0.7027 [0.6035, 0.8025] PCA_L=0.4581 [0.4000, 0.5505] PROY_L=0.7132 [0.6240, 0.8074] W_n=0.7003 (190 de 200) | W=0.9276
CURVA c2 n=48 MOSCA_L=0.8639 [0.7952, 0.9212] CRUDO=0.8517 [0.7635, 0.9650] PCA_L=0.5214 [0.4000, 0.6140] PROY_L=0.8460 [0.7564, 0.8994] W_n=0.7858 (200 de 200) | W=0.9276
CURVA c2 n=96 MOSCA_L=0.9298 [0.8709, 0.9589] CRUDO=0.9347 [0.8645, 0.9845] PCA_L=0.6615 [0.5000, 0.7465] PROY_L=0.9043 [0.8660, 0.9464] W_n=0.8545 (200 de 200) | W=0.9276
CURVA c2 n=192 MOSCA_L=0.9698 [0.9397, 0.9899] CRUDO=0.9717 [0.9265, 0.9945] PCA_L=0.8276 [0.7710, 0.8975] PROY_L=0.9401 [0.9046, 0.9604] W_n=0.8896 (200 de 200) | W=0.9276
CURVA c2 n=384 MOSCA_L=0.9826 [0.9654, 0.9922] CRUDO=0.9834 [0.9565, 0.9990] PCA_L=0.9442 [0.9165, 0.9675] PROY_L=0.9618 [0.9461, 0.9761] W_n=0.9136 (200 de 200) | W=0.9276
CURVA c2 n=768 MOSCA_L=0.9897 [0.9838, 0.9952] CRUDO=0.9941 [0.9845, 0.9990] PCA_L=0.9930 [0.9870, 0.9965] PROY_L=0.9743 [0.9674, 0.9812] W_n=0.9217 (200 de 200) | W=0.9276
CURVA c2 n=2400 MOSCA_L=0.9943 [0.9942, 0.9942] CRUDO=0.9995 [0.9995, 0.9995] PCA_L=0.9995 [0.9995, 0.9995] PROY_L=0.9831 [0.9831, 0.9831] W_n=- (0 de 0) | W=0.9276"""
rx = re.compile(r"n=(\d+) MOSCA_L=([\d.]+) .*?CRUDO=([\d.]+) .*?PCA_L=([\d.]+)")
for l in crudo.splitlines():
    n, m, c, pc = rx.search(l).groups()
    m, c, pc = float(m), float(c), float(pc)
    print("c2 n=%5s MOSCA_L=%.4f CRUDO=%.4f PCA_L=%.4f | crudo>=embudo: %s | pca>=embudo: %s" % (n, m, c, pc, c >= m, pc >= m))

print("\n== 6. Indice de git: las regex exactas de tools/arranque/generar_indice.py (blob ef57d55) ==")
RE_CU = re.compile(r"https://app\.clickup\.com/[^\s)\]>\"'`|*]+")
RE_DOC = re.compile(r"^[\s>*_\-+]*doc(?:\s+(?:p\u00fablico|publico|de\s+clickup|en\s+clickup|espejo))?[\s*_]*:", re.I)
URL = "https://app.clickup.com/90171457413/v/dc/SINTETICA"   # forma de URL de ClickUp; RE_DOC no depende de ella
lineas = {
 "auditada s8 (linea real, URL sintetica)": "- [Doc p\u00fablico: 2026-11-01 \u00b7 Topo inverso: tenemos piezas para buscar una gram\u00e1tica funcional del conectoma, todav\u00eda no la gram\u00e1tica](%s), en Space." % URL,
 "auditada METODO Artefactos (linea real)": "Artefactos: `docs/agents/respuestas/2026-11-01-01-topo-inverso-gramatica-funcional-por-medir.md`, en la rama documental, y Doc p\u00fablico de ClickUp enlazado en la secci\u00f3n 8.",
 "control + auditoria 2026-10-19-01": "**Fecha:** 19-oct-2026, 15:20 (America/Buenos_Aires). **Doc:** %s" % URL,
 "control + estilo nota PROMETEO": "Doc: %s" % URL,
 "control + estilo Doc publico": "Doc p\u00fablico: %s" % URL,
}
for k, l in lineas.items():
    print("%-42s RE_DOC=%-5s links_clickup=%d" % (k, bool(RE_DOC.match(l)), len(RE_CU.findall(l))))
for nombre in ["2026-11-01-01-topo-inverso-gramatica-funcional-por-medir.md", "2026-10-14-061-arranque-corregido-y-h-pares-datos-medido.md"]:
    clave = nombre[:-3]
    num = clave[:14] if re.match(r"\d{4}-\d{2}-\d{2}-\d{2,3}", clave) else clave
    print("num del indice para %s -> %r" % (nombre[:30], num))
