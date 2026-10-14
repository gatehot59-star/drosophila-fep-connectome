#!/usr/bin/env python3
"""Topo v0.2: salida diferencial aguas abajo (respuesta 2026-10-14-026). Envuelve Topo v0 (topo.py 9abefe9d) y
Topo v0.1 (topo_grafo.py 0ea68782) sin cambiarlos.

Por que: la 025 encontro en la literatura que DNp06 responde a los dos ojos (Jang 2023, Kim 2023) y la 024 que a dos
saltos en el cerebro no hay resta del otro lado. Si el lado del giro se decide, se decide aguas abajo, comparando las
dos DNp06. v0 no lo puede escribir: la resta tenia que ir adentro de la linea de DNp06.

Gramatica nueva (el resto es v0):
  linea NOMBRE = EXPR en ESTADO -> interna     una linea interna no compite: es una salida que otra cosa lee
  compara NOMBRE = A - B en ESTADO -> ACCION   compite como una linea; su senal es la de A menos la de B
      A y B son lineas internas distintas, del mismo ESTADO que el comparador. Toda linea interna se usa en algun
      comparador.
Backend regla: las lineas no internas y los comparadores compiten en carrera, en ese orden, con los umbrales de v0.
Chequeo contra el conectoma: las flechas sensor -> linea se chequean en FlyWire como en v0.1; las flechas
linea -> comparador se marcan AGUAS_ABAJO: no son del cerebro, se chequean en el cordon nervioso (BANC), no aca.
Consecuencia declarada: por linealidad, un comparador A - B rinde lo mismo que una linea que resta adentro. v0.2 no
cambia lo que el programa hace; cambia donde dice que ocurre la cuenta, y eso es lo que se puede falsar en BANC.
El archivo no lleva barras invertidas: los saltos se arman con chr().
"""
import hashlib
import os
import sys

import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(AQUI), "topo"))
import topo  # noqa: E402
import topo_grafo as tg  # noqa: E402

NL = chr(10)
MD5_TOPO, MD5_GRAFO = "9abefe9d620e9f94f4a68ed75108d6be", "0ea687824a45456e0a02b0b197f57a8a"
ErrorTopo = topo.ErrorTopo


def md5(ruta):
    return hashlib.md5(open(ruta, "rb").read()).hexdigest()


def parsear(texto):
    renglones = texto.split(NL)
    acciones = None
    for cruda in renglones:
        t = topo.tokens(cruda.split("#", 1)[0].strip()) if cruda.split("#", 1)[0].strip() else []
        if t and t[0] == "acciones" and len(t) >= 3:
            acciones = t[1:]
    if acciones is None:
        raise ErrorTopo("falta la sentencia acciones (con al menos dos)")
    internas, compara, resto = [], [], []
    for n, cruda in enumerate(renglones, 1):
        lin = cruda.split("#", 1)[0].strip()
        t = topo.tokens(lin) if lin else []
        if t and t[0] == "compara":
            if len(t) != 10 or t[2] != "=" or t[4] != "-" or t[6] != "en" or t[8] != "FLECHA":
                raise ErrorTopo("renglon %d: compara NOMBRE = A - B en ESTADO -> ACCION" % n)
            compara.append(dict(nombre=t[1], a=t[3], b=t[5], estado=t[7], accion=t[9], renglon=n))
            resto.append("")
        elif t and t[0] == "linea" and t[-1] == "interna" and len(t) >= 2 and t[-2] == "FLECHA":
            internas.append(t[1])
            resto.append(lin[: lin.rindex("interna")] + acciones[1])
        else:
            resto.append(cruda)
    p = topo.parsear(NL.join(resto))
    p["internas"], p["compara"] = internas, compara
    validar(p)
    return p


def validar(p):
    lineas = {ln["nombre"]: ln for ln in p["lineas"]}
    usadas, nombres = set(), set(lineas)
    for c in p["compara"]:
        if c["nombre"] in nombres:
            raise ErrorTopo("renglon %d: nombre repetido %s" % (c["renglon"], c["nombre"]))
        nombres.add(c["nombre"])
        for x in (c["a"], c["b"]):
            if x not in lineas or x not in p["internas"]:
                raise ErrorTopo("renglon %d: %s no es una linea interna" % (c["renglon"], x))
            if lineas[x]["estado"] != c["estado"]:
                raise ErrorTopo("renglon %d: %s es de otro estado" % (c["renglon"], x))
            usadas.add(x)
        if c["a"] == c["b"]:
            raise ErrorTopo("renglon %d: A y B tienen que ser distintas" % c["renglon"])
        if c["estado"] not in p["estados"]:
            raise ErrorTopo("renglon %d: estado desconocido %s" % (c["renglon"], c["estado"]))
        if c["accion"] not in p["acciones"][1:]:
            raise ErrorTopo("renglon %d: accion desconocida o por omision %s" % (c["renglon"], c["accion"]))
    sin_uso = [x for x in p["internas"] if x not in usadas]
    if sin_uso:
        raise ErrorTopo("linea interna sin comparador: %s" % ", ".join(sin_uso))


def compiten(p):
    """Lo que compite en carrera, en orden: lineas no internas y despues comparadores."""
    out = [dict(nombre=ln["nombre"], estado=ln["estado"], accion=ln["accion"]) for ln in p["lineas"]
           if ln["nombre"] not in p["internas"]]
    return out + [dict(nombre=c["nombre"], estado=c["estado"], accion=c["accion"]) for c in p["compara"]]


def senales(p, X, tipo_ent, lado_ent):
    S = topo.senales(p, X, tipo_ent, lado_ent)
    idx = {ln["nombre"]: j for j, ln in enumerate(p["lineas"])}
    cols = [S[:, :, idx[ln["nombre"]]] for ln in p["lineas"] if ln["nombre"] not in p["internas"]]
    cols += [S[:, :, idx[c["a"]]] - S[:, :, idx[c["b"]]] for c in p["compara"]]
    return np.stack(cols, axis=2)


def ejecutar_regla(p, Xtr, ytr, etr, Xte, ete, tipo_ent, lado_ent):
    q = dict(p, lineas=compiten(p))
    Str = senales(p, Xtr, tipo_ent, lado_ent)
    th = topo.umbrales(q, Str, ytr, etr)
    Ste = senales(p, Xte, tipo_ent, lado_ent)
    return topo.carrera(q, Ste, th, ete), th, Ste


def flechas_aguas_abajo(p):
    out = []
    for c in p["compara"]:
        for x, s in ((c["a"], 1.0), (c["b"], -1.0)):
            out.append(dict(linea=c["nombre"], origen=x, coef=s, veredicto="AGUAS_ABAJO"))
    return out


def main(argv):
    if len(argv) < 2:
        print(__doc__)
        return 2
    for nombre, ruta, m in (("topo.py", topo.__file__, MD5_TOPO), ("topo_grafo.py", tg.__file__, MD5_GRAFO)):
        got = md5(ruta)
        print("# md5 %s = %s (sellado %s)" % (nombre, got, m[:8]))
        if got != m:
            print("ABORTA: %s no es el sellado" % nombre)
            return 3
    try:
        p = parsear(open(argv[1], encoding="utf-8").read())
    except ErrorTopo as e:
        print("PROGRAMA_INVALIDO %s" % e)
        return 2
    print("PROGRAMA %s lineas=%d internas=%d comparadores=%d compiten=%s" % (
        p["reflejo"], len(p["lineas"]), len(p["internas"]), len(p["compara"]),
        ",".join(c["nombre"] for c in compiten(p))))
    if "--conn" in argv:
        a, c = tg.cargar(argv[argv.index("--conn") + 1], argv[argv.index("--annot") + 1])
        fl = tg.chequear(p, a, c)[0]
        cuenta = {}
        for f in fl:
            print("FLECHA %s@%s -> %s coef=%+.2f sinapsis=%d -> %s" % (f["tipo"], f["lado"], f["linea"], f["coef"],
                                                                 f["sinapsis"], f["veredicto"]))
            cuenta[f["veredicto"]] = cuenta.get(f["veredicto"], 0) + 1
        for f in flechas_aguas_abajo(p):
            print("FLECHA %s -> %s coef=%+.2f -> %s (se chequea en el cordon nervioso, no en FlyWire)" % (
                f["origen"], f["linea"], f["coef"], f["veredicto"]))
            cuenta[f["veredicto"]] = cuenta.get(f["veredicto"], 0) + 1
        print("CHEQUEO %s %s" % (p["reflejo"], " ".join("%s=%d" % kv for kv in sorted(cuenta.items()))))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
