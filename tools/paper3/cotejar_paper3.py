#!/usr/bin/env python3
"""Coteja cada numero del esqueleto del Paper 3 contra las respuestas de git que cita su seccion (2026-10-14-019).

Cada encabezado de seccion lleva entre corchetes sus fuentes (p. ej. [2026-10-10-005, 2026-10-10-006]). Para cada
numero de 3 caracteres o mas que aparece en esa seccion (fuera de codigo y de corchetes), busca el numero en las
fuentes tal cual o con punto y coma intercambiados (el paper va en ingles y las respuestas en castellano).
Lo que prueba: que cada numero esta escrito en su fuente. Lo que no prueba: que la frase que lo rodea diga lo mismo.
Uso: python3 tools/paper3/cotejar_paper3.py docs/paper3/paper3-esqueleto.md docs/agents/respuestas [--control]
--control: cambia dos numeros (60.23 por 61.23 y 256.3 por 265.3) y exige que el cotejo los marque.
Salida: 0 si todo esta en su fuente (o si el control marca los dos cambios); 1 si no.
"""
import glob
import os
import re
import sys

BT = chr(96)
RE_NUM = re.compile("[0-9]+(?:[.,][0-9]+)*")
RE_TAG = re.compile("20[0-9][0-9]-[0-9][0-9]-[0-9][0-9]-[0-9][0-9][0-9]")
RE_CODE = re.compile(BT + "[^" + BT + "]*" + BT)
RE_CORCH = re.compile(re.escape(chr(91)) + "[^" + chr(93) + "]*" + re.escape(chr(93)))
CAMBIOS = (("60.23%", "61.23%"), ("256.3", "265.3"))


def cambiar(tok):
    return tok.replace(".", "#").replace(",", ".").replace("#", ",")


def cotejar(texto, dir_resp):
    faltan, total, sin_fuente = [], 0, []
    fuentes, cache = [], {}
    en_frente = False
    for i, linea in enumerate(texto.splitlines(), 1):
        if i == 1 and linea.strip() == "---":
            en_frente = True
            continue
        if en_frente:
            if linea.strip() == "---":
                en_frente = False
            continue
        if linea.startswith("#"):
            fuentes = RE_TAG.findall(linea)
            for f in fuentes:
                if f not in cache:
                    rutas = glob.glob(os.path.join(dir_resp, f + "-*.md"))
                    cache[f] = open(rutas[0], encoding="utf-8").read() if len(rutas) == 1 else None
                    if cache[f] is None:
                        sin_fuente.append(f)
            continue
        if not fuentes:
            continue
        limpio = RE_CORCH.sub(" ", RE_CODE.sub(" ", linea))
        textos = [cache[f] for f in fuentes if cache.get(f)]
        for tok in RE_NUM.findall(limpio):
            if len(tok) < 3:
                continue
            total += 1
            alt = cambiar(tok)
            if not any(tok in t or alt in t for t in textos):
                faltan.append((i, tok, ",".join(fuentes)))
    return total, faltan, sin_fuente


def main():
    ruta, dir_resp = sys.argv[1], sys.argv[2]
    control = "--control" in sys.argv
    texto = open(ruta, encoding="utf-8").read()
    if control:
        for a, b in CAMBIOS:
            if texto.count(a) < 1:
                print("CONTROL_NEGATIVO no encuentra %s en el esqueleto -> FALLA" % a)
                return 1
            texto = texto.replace(a, b, 1)
    total, faltan, sin_fuente = cotejar(texto, dir_resp)
    for i, tok, f in faltan:
        print("FALTA linea=%d numero=%s fuentes=%s" % (i, tok, f))
    if sin_fuente:
        print("SIN_FUENTE %s" % " ".join(sorted(set(sin_fuente))))
    print("COTEJO numeros=%d en_su_fuente=%d faltan=%d fuentes_sin_archivo=%d" % (
        total, total - len(faltan), len(faltan), len(set(sin_fuente))))
    if control:
        marcados = set(tok for _, tok, _ in faltan)
        ok = all(b.rstrip("%") in marcados for _, b in CAMBIOS) and len(faltan) == len(CAMBIOS)
        print("CONTROL_NEGATIVO cambios=%d marcados=%d -> %s" % (len(CAMBIOS), len(faltan), "PASA" if ok else "FALLA"))
        return 0 if ok else 1
    ok = not faltan and not sin_fuente and total > 0
    print("COTEJO_PAPER3 -> %s" % ("PASA" if ok else "FALLA"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
