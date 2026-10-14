#!/usr/bin/env python3
"""Topo v0.1: el programa como grafo, chequeado contra el conectoma (respuesta 2026-10-14-020).

Topo v0 (topo.py, md5 9abefe9d, importado sin cambios) escribe un reflejo como flechas: sensor@lado con signo ->
linea -> accion. Esta pieza agrega dos cosas:
  grafo    el programa como grafo: nodos sensor@lado, lineas y acciones; aristas con el signo y el peso del programa.
           Sale en Mermaid (GitHub lo dibuja) y en una tabla.
  chequeo  cada flecha sensor@lado -> linea se busca en FlyWire v783 cuando el nombre de la linea es una descendente
           del conectoma (TIPO@LADO, por ejemplo DNp07@L): sinapsis directas de todas las neuronas de ese tipo y lado
           sobre esa descendente, su signo (fraccion excitatoria) e intermediarias a dos saltos (5 o mas sinapsis en
           cada tramo, la fraccion inhibitoria es la del segundo tramo).
Veredicto por flecha:
  CABLEADA          hay sinapsis directas y el signo mayoritario coincide con el del programa
  SIGNO_CONTRARIO   hay sinapsis directas con el signo mayoritario opuesto al del programa
  SIN_VIA_DIRECTA   cero sinapsis directas: esa cuenta la hace la regla, no la mosca
  TIPO_INEXISTENTE  el tipo del sensor no tiene neuronas de ese lado en las anotaciones
  SIN_BLANCO        la linea no nombra una descendente del conectoma: no se chequea
Tambien da el total por tipo (los dos lados) sobre cada descendente (los dos lados), para cotejar con la
2026-10-12-014.
Uso:
  python3 topo_grafo.py PROGRAMA.topo [--conn C --annot A] [--md SALIDA.md] [--json SALIDA.json]
Salida: 0 si el programa es valido (y el chequeo corrio, si se pidio); 2 si no es valido; 3 si topo.py no es el sellado.
"""
import hashlib
import json
import os
import sys

import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import topo  # noqa: E402  Topo v0 sellado (9abefe9d), sin cambios

NL = chr(10)
MD5_TOPO = "9abefe9d620e9f94f4a68ed75108d6be"
MIN_DOS = 5
LADO_TXT = {"L": "izq", "R": "der"}
COLOR = {"SIN_VIA_DIRECTA": "#c62828", "SIGNO_CONTRARIO": "#ef6c00", "TIPO_INEXISTENTE": "#6a1b9a"}


def md5(ruta):
    return hashlib.md5(open(ruta, "rb").read()).hexdigest()


def blanco(nombre):
    if "@" not in nombre:
        return None
    t, l = nombre.split("@", 1)
    return (t, l) if l in topo.LADOS else None


def flechas(p):
    out = []
    for ln in p["lineas"]:
        for coef, refs in ln["terminos"]:
            for tipo, lado in refs:
                out.append(dict(linea=ln["nombre"], tipo=tipo, lado=lado, coef=coef / len(refs),
                                blanco=blanco(ln["nombre"])))
    return out


def cargar(conn, annot):
    import pandas as pd
    a = pd.read_csv(annot, sep=chr(9), dtype=str, usecols=["root_id", "cell_type", "side"])
    a["root_id"] = a.root_id.astype(np.int64)
    c = pd.read_parquet(conn, columns=["Presynaptic_ID", "Postsynaptic_ID", "Connectivity", "Excitatory"])
    return a, c


def ids_de(a, tipo, lado=None):
    m = a.cell_type == tipo
    if lado is not None:
        m = m & (a.side == topo.LADOS[lado])
    return a.root_id[m].to_numpy()


def chequear(p, a, c):
    fl = flechas(p)
    dns = sorted(set(f["blanco"] for f in fl if f["blanco"]))
    dn_ids = {b: ids_de(a, b[0], b[1]) for b in dns}
    todos = np.concatenate([v for v in dn_ids.values()] + [np.zeros(0, dtype=np.int64)])
    entra = c[c.Postsynaptic_ID.isin(todos)]
    for f in fl:
        f.update(sinapsis=0, neuronas=0, excitatoria=None, dos_inter=0, dos_sinapsis=0, dos_inhibitoria=None)
        if f["blanco"] is None or len(dn_ids[f["blanco"]]) == 0:
            f["veredicto"] = "SIN_BLANCO"
            continue
        pre = ids_de(a, f["tipo"], f["lado"])
        if len(pre) == 0:
            f["veredicto"] = "TIPO_INEXISTENTE"
            continue
        dn = dn_ids[f["blanco"]]
        e = entra[entra.Postsynaptic_ID.isin(dn)]
        d = e[e.Presynaptic_ID.isin(pre)]
        s = int(d.Connectivity.sum())
        f["sinapsis"], f["neuronas"] = s, int(d.Presynaptic_ID.nunique())
        signo_prog = 1 if f["coef"] > 0 else -1
        if s > 0:
            exc = int(d.Connectivity[d.Excitatory > 0].sum())
            f["excitatoria"] = exc / s
            signo_real = 1 if 2 * exc > s else -1
            f["veredicto"] = "CABLEADA" if signo_real == signo_prog else "SIGNO_CONTRARIO"
        else:
            f["veredicto"] = "SIN_VIA_DIRECTA"
        l2 = e[~e.Presynaptic_ID.isin(pre) & ~e.Presynaptic_ID.isin(dn)]
        t2 = l2.groupby("Presynaptic_ID").Connectivity.sum()
        t2 = t2[t2 >= MIN_DOS]
        if len(t2):
            l1 = c[c.Presynaptic_ID.isin(pre) & c.Postsynaptic_ID.isin(t2.index)]
            t1 = l1.groupby("Postsynaptic_ID").Connectivity.sum()
            ks = t1[t1 >= MIN_DOS].index
            ks2 = l2[l2.Presynaptic_ID.isin(ks)]
            s2 = int(ks2.Connectivity.sum())
            f["dos_inter"], f["dos_sinapsis"] = int(len(ks)), s2
            if s2 > 0:
                f["dos_inhibitoria"] = int(ks2.Connectivity[ks2.Excitatory < 0].sum()) / s2
    pares = sorted(set((f["tipo"], f["blanco"][0]) for f in fl if f["blanco"]))
    totales = []
    for tipo, b in pares:
        pre, dn = ids_de(a, tipo), ids_de(a, b)
        d = c[c.Postsynaptic_ID.isin(dn) & c.Presynaptic_ID.isin(pre)]
        totales.append(dict(tipo=tipo, blanco=b, sinapsis=int(d.Connectivity.sum()),
                            neuronas=int(d.Presynaptic_ID.nunique())))
    return fl, totales


def nodo(t, l):
    return "%s_%s" % (t, l)


def mermaid(p, fl):
    out = ["flowchart LR"]
    estilos, k = [], 0
    for f in fl:
        sg = "+" if f["coef"] > 0 else "-"
        et = "%s%.2f" % (sg, abs(f["coef"]))
        if "veredicto" in f:
            if f["veredicto"] in ("CABLEADA", "SIGNO_CONTRARIO"):
                et += " · %d sin, %.0f%% exc · %s" % (f["sinapsis"], 100.0 * f["excitatoria"], f["veredicto"])
            elif f["veredicto"] == "SIN_VIA_DIRECTA":
                et += " · 0 sin directas · a dos saltos %d inter · SIN_VIA_DIRECTA" % f["dos_inter"]
            else:
                et += " · " + f["veredicto"]
        flecha = "-.->" if f.get("veredicto") in ("SIN_VIA_DIRECTA", "TIPO_INEXISTENTE") else "-->"
        out.append('  %s["%s %s"] %s|"%s"| %s["%s"]' % (
            nodo(f["tipo"], f["lado"]), f["tipo"], LADO_TXT[f["lado"]], flecha, et,
            nodo(*f["linea"].split("@")) if "@" in f["linea"] else f["linea"], f["linea"]))
        if f.get("veredicto") in COLOR:
            estilos.append("  linkStyle %d stroke:%s,stroke-width:2px" % (k, COLOR[f["veredicto"]]))
        k += 1
    for ln in p["lineas"]:
        n = nodo(*ln["nombre"].split("@")) if "@" in ln["nombre"] else ln["nombre"]
        out.append('  %s -->|"en %s"| %s(["%s"])' % (n, ln["estado"], ln["accion"], ln["accion"]))
        k += 1
    return NL.join(out + estilos)


def tabla(fl):
    filas = ["| flecha | signo en el programa | sinapsis directas | neuronas | excitatoria | veredicto | "
             "a dos saltos: intermediarias, sinapsis, inhibitoria |", "|---|---|---|---|---|---|---|"]
    for f in fl:
        exc = "" if f.get("excitatoria") is None else "%.0f %%" % (100.0 * f["excitatoria"])
        inh = "" if f.get("dos_inhibitoria") is None else "%.0f %%" % (100.0 * f["dos_inhibitoria"])
        filas.append("| %s@%s a %s | %+.2f | %s | %s | %s | %s | %s, %s, %s |" % (
            f["tipo"], f["lado"], f["linea"], f["coef"], f.get("sinapsis", ""), f.get("neuronas", ""), exc,
            f.get("veredicto", "sin chequear"), f.get("dos_inter", ""), f.get("dos_sinapsis", ""), inh))
    return NL.join(filas)


def main(argv):
    if len(argv) < 2:
        print(__doc__)
        return 2
    mt = md5(os.path.join(AQUI, "topo.py"))
    print("# md5 topo.py = %s (sellado %s)" % (mt, MD5_TOPO[:8]))
    if mt != MD5_TOPO:
        print("ABORTA: topo.py no es el sellado")
        return 3
    try:
        p = topo.parsear(open(argv[1], encoding="utf-8").read())
    except topo.ErrorTopo as e:
        print("PROGRAMA_INVALIDO %s" % e)
        return 2
    fl = flechas(p)
    print("GRAFO %s flechas_sensor_a_linea=%d lineas_a_accion=%d" % (p["reflejo"], len(fl), len(p["lineas"])))
    totales = []
    if "--conn" in argv:
        a, c = cargar(argv[argv.index("--conn") + 1], argv[argv.index("--annot") + 1])
        fl, totales = chequear(p, a, c)
        for f in fl:
            print("FLECHA %s@%s -> %s coef=%+.2f sinapsis=%d neuronas=%d exc=%s dos_saltos=%d/%d/%s -> %s" % (
                f["tipo"], f["lado"], f["linea"], f["coef"], f["sinapsis"], f["neuronas"],
                "-" if f["excitatoria"] is None else "%.3f" % f["excitatoria"], f["dos_inter"], f["dos_sinapsis"],
                "-" if f["dos_inhibitoria"] is None else "%.3f" % f["dos_inhibitoria"], f["veredicto"]))
        for t in totales:
            print("TOTAL %s -> %s sinapsis=%d neuronas=%d" % (t["tipo"], t["blanco"], t["sinapsis"], t["neuronas"]))
        cuenta = {}
        for f in fl:
            cuenta[f["veredicto"]] = cuenta.get(f["veredicto"], 0) + 1
        print("CHEQUEO %s %s" % (p["reflejo"], " ".join("%s=%d" % kv for kv in sorted(cuenta.items()))))
    if "--md" in argv:
        ruta = argv[argv.index("--md") + 1]
        bt3 = chr(96) * 3
        txt = ("# Grafo de %s (Topo v0.1)" % p["reflejo"] + NL + NL +
               "Generado por tools/topo/topo_grafo.py desde el programa, sin tocarlo a mano. Flecha punteada y roja: "
               "el programa hace esa cuenta pero la mosca no tiene sinapsis directas ahi." + NL + NL +
               bt3 + "mermaid" + NL + mermaid(p, fl) + NL + bt3 + NL + NL + tabla(fl) + NL)
        if totales:
            txt += NL + "| tipo (los dos lados) | descendente (las dos) | sinapsis | neuronas |" + NL + "|---|---|---|---|" + NL
            txt += NL.join("| %s | %s | %d | %d |" % (t["tipo"], t["blanco"], t["sinapsis"], t["neuronas"])
                           for t in totales) + NL
        open(ruta, "w", encoding="utf-8").write(txt)
        print("ESCRITO %s md5=%s" % (ruta, md5(ruta)))
    if "--json" in argv:
        ruta = argv[argv.index("--json") + 1]
        json.dump(dict(reflejo=p["reflejo"], flechas=fl, totales=totales), open(ruta, "w"), indent=1)
        print("ESCRITO %s md5=%s" % (ruta, md5(ruta)))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
