#!/usr/bin/env python3
"""Pruebas de Topo v0.1, el grafo chequeado contra el conectoma (respuesta 2026-10-14-020).

Sin datos:
  ESTRUCTURA       escape.topo da 14 flechas y 6 lineas; aterrizaje_dir.topo da 16 (suma -LPLC1 en DNp07); los
                   coeficientes salen del programa; el Mermaid tiene una arista por flecha y por linea.
Con datos (--conn y --annot):
  REPRODUCE_014    los totales por tipo sobre cada descendente son los de la 2026-10-12-014 (sinapsis y neuronas).
  PUEDE_DAR_ROJO   LPLC1 a DNp07 da SIN_VIA_DIRECTA de los dos lados y LC4@L a DNp01@L da CABLEADA.
  SIGNO_CONTRARIO  restar LC4@L en DNp01@L (una via excitatoria) da SIGNO_CONTRARIO.
  TIPO_INEXISTENTE un tipo que no existe (LC4X) da TIPO_INEXISTENTE sin romper.
Uso: python3 tools/topo/prueba_grafo.py [--conn C --annot A]   Salida: 0 si pasan todas.
"""
import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import topo  # noqa: E402
import topo_grafo as tg  # noqa: E402

RAIZ = os.path.normpath(os.path.join(AQUI, "..", ".."))
ESCAPE = os.path.join(RAIZ, "tools", "topo", "escape.topo")
ATERRIZAJE = os.path.join(RAIZ, "tools", "topo_barra", "aterrizaje_dir.topo")
TOTALES_014 = {("LPLC2", "DNp01"): (1080, 189), ("LC4", "DNp01"): (805, 104), ("LPLC1", "DNp06"): (1023, 136),
               ("LPLC2", "DNp06"): (1003, 200), ("LPLC4", "DNp07"): (1448, 92), ("LPLC1", "DNp07"): (0, 0)}


def leer(r):
    return open(r, encoding="utf-8").read()


def buscar(fl, tipo, lado, linea):
    m = [f for f in fl if (f["tipo"], f["lado"], f["linea"]) == (tipo, lado, linea)]
    return m[0] if len(m) == 1 else None


def aristas_mermaid(txt):
    return sum(1 for x in txt.split(tg.NL) if ("-->" in x or "-.->" in x) and not x.strip().startswith("linkStyle"))


def main(argv):
    res = []
    pe, pa = topo.parsear(leer(ESCAPE)), topo.parsear(leer(ATERRIZAJE))
    fe, fa = tg.flechas(pe), tg.flechas(pa)
    a1 = buscar(fa, "LPLC1", "R", "DNp06@L")
    a2 = buscar(fa, "LPLC4", "L", "DNp07@L")
    a3 = buscar(fa, "LPLC1", "L", "DNp07@L")
    ok = (len(fe) == 14 and len(pe["lineas"]) == 6 and len(fa) == 16 and a1 is not None and a1["coef"] == -0.5 and
          a2 is not None and a2["coef"] == 1.0 and a3 is not None and a3["coef"] == -1.0 and
          buscar(fe, "LPLC1", "L", "DNp07@L") is None and
          aristas_mermaid(tg.mermaid(pe, fe)) == 20 and aristas_mermaid(tg.mermaid(pa, fa)) == 22)
    res.append(("ESTRUCTURA", ok, "escape=%d aterrizaje=%d mermaid=%d/%d" % (
        len(fe), len(fa), aristas_mermaid(tg.mermaid(pe, fe)), aristas_mermaid(tg.mermaid(pa, fa)))))
    if "--conn" in argv:
        a, c = tg.cargar(argv[argv.index("--conn") + 1], argv[argv.index("--annot") + 1])
        fa, ta = tg.chequear(pa, a, c)
        tot = {(t["tipo"], t["blanco"]): (t["sinapsis"], t["neuronas"]) for t in ta}
        ok = tot == TOTALES_014
        res.append(("REPRODUCE_014", ok, "%d pares, iguales=%d" % (
            len(TOTALES_014), sum(1 for k, v in TOTALES_014.items() if tot.get(k) == v))))
        v1 = buscar(fa, "LPLC1", "L", "DNp07@L")["veredicto"]
        v2 = buscar(fa, "LPLC1", "R", "DNp07@R")["veredicto"]
        v3 = buscar(fa, "LC4", "L", "DNp01@L")["veredicto"]
        ok = (v1, v2, v3) == ("SIN_VIA_DIRECTA", "SIN_VIA_DIRECTA", "CABLEADA")
        res.append(("PUEDE_DAR_ROJO", ok, "%s %s %s" % (v1, v2, v3)))
        viejo = "linea DNp01@L = media(LC4@L, LPLC2@L) en posada -> despegar"
        nuevo = "linea DNp01@L = media(LPLC2@L) - media(LC4@L) en posada -> despegar"
        txt = leer(ESCAPE)
        ok_txt = txt.count(viejo) == 1
        ps = topo.parsear(txt.replace(viejo, nuevo))
        fs, _ = tg.chequear(ps, a, c)
        v = buscar(fs, "LC4", "L", "DNp01@L")
        ok = ok_txt and v is not None and v["coef"] == -1.0 and v["veredicto"] == "SIGNO_CONTRARIO"
        res.append(("SIGNO_CONTRARIO", ok, v["veredicto"] if v else "sin flecha"))
        pi = topo.parsear(txt.replace("LC4", "LC4X"))
        fi, _ = tg.chequear(pi, a, c)
        vs = sorted(set(f["veredicto"] for f in fi if f["tipo"] == "LC4X"))
        ok = vs == ["TIPO_INEXISTENTE"]
        res.append(("TIPO_INEXISTENTE", ok, ",".join(vs)))
    for nombre, ok, det in res:
        print("PRUEBA %s %s -> %s" % (nombre, det, "PASA" if ok else "FALLA"))
    n = sum(1 for _, ok, _ in res if ok)
    print("VEREDICTO_GRAFO %s %d/%d" % ("PASA" if n == len(res) else "FALLA", n, len(res)))
    return 0 if n == len(res) else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
