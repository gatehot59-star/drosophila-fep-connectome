#!/usr/bin/env python3
"""Diff de super_class entre dos versiones del TSV de anotaciones FlyWire.
Uso: diff_annot.py <tsv_A> <tsv_B>
Imprime filas, conteo por super_class de cada archivo, root_id solo en uno,
y la matriz de cambios de super_class para los root_id comunes."""
import collections
import csv
import hashlib
import sys


def md5(p):
    h = hashlib.md5()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def load(p):
    d = {}
    dup = 0
    with open(p, newline="") as f:
        for row in csv.DictReader(f, delimiter="\t"):
            rid = row["root_id"]
            if rid in d:
                dup += 1
            d[rid] = row["super_class"]
    return d, dup


pa, pb = sys.argv[1], sys.argv[2]
a, da = load(pa)
b, db = load(pb)
print("A", pa, "md5", md5(pa), "filas_unicas", len(a), "duplicados", da)
print("B", pb, "md5", md5(pb), "filas_unicas", len(b), "duplicados", db)
print("A super_class", dict(sorted(collections.Counter(a.values()).items())))
print("B super_class", dict(sorted(collections.Counter(b.values()).items())))
only_a = sorted(set(a) - set(b))
only_b = sorted(set(b) - set(a))
print("solo_en_A", len(only_a), [(k, a[k]) for k in only_a[:30]])
print("solo_en_B", len(only_b), [(k, b[k]) for k in only_b[:30]])
common = set(a) & set(b)
ch = collections.Counter((a[k], b[k]) for k in common if a[k] != b[k])
print("comunes", len(common), "cambios_super_class", sum(ch.values()))
for (x, y), n in sorted(ch.items(), key=lambda t: -t[1]):
    print("  CAMBIO", x, "->", y, n)
print("FIN_DIFF")
