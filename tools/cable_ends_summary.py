#!/usr/bin/env python3
"""Que hay al final de cada cable: resumen por super_class de las matrices de aristas y reciprocas
que produjo tools/table7_reciprocity_by_class.py sobre FlyWire v783 (sin umbral y con >=5 sinapsis).
No recalcula el grafo: lee el JSON de esa corrida. Uso: cable_ends_summary.py <json>"""
import json
import sys

SALIDA = ["descending", "motor", "endocrine"]
ORIGENES = ["sensory", "sensory_ascending", "ascending", "optic", "visual_projection", "central", "visual_centrifugal"]


def pct(a, b):
    return format(100.0 * a / b, ".2f") if b else "nan"


def bloque(titulo, names, cnt, E, R):
    k = len(names)
    tot = sum(sum(f) for f in E)
    totr = sum(sum(f) for f in R)
    ntot = sum(cnt[c] for c in names)
    ix = {c: i for i, c in enumerate(names)}
    print("=== " + titulo + " ===")
    print("neuronas=" + str(ntot) + "  aristas=" + str(tot) + "  reciprocas=" + str(totr) + " (" + pct(totr, tot) + "%)")
    print("clase | neuronas | %neur | salen | %aristas | entran | %aristas | recip_salen% | recip_entran%")
    for c in names:
        i = ix[c]
        oe = sum(E[i])
        ie = sum(E[j][i] for j in range(k))
        orr = sum(R[i])
        ir = sum(R[j][i] for j in range(k))
        print(" | ".join([c, str(cnt[c]), pct(cnt[c], ntot), str(oe), pct(oe, tot), str(ie), pct(ie, tot), pct(orr, oe), pct(ir, ie)]))
    sal = [ix[c] for c in SALIDA if c in ix]
    nsal = sum(cnt[names[i]] for i in sal)
    esal = sum(E[j][i] for i in sal for j in range(k))
    print("EMBUDO_SALIDA neuronas=" + str(nsal) + " (" + pct(nsal, ntot) + "% del grafo)  aristas_que_entran=" + str(esal) + " (" + pct(esal, tot) + "% de todas)")
    for i in sal:
        col = sorted(((E[j][i], R[j][i], names[j]) for j in range(k)), reverse=True)
        ie = sum(x[0] for x in col)
        print("  hacia " + names[i] + " (" + str(ie) + " aristas) desde: " + "; ".join(x[2] + " " + str(x[0]) + " (" + pct(x[0], ie) + "%, recip " + pct(x[1], x[0]) + "%)" for x in col[:4] if x[0] > 0))
    for c in ORIGENES:
        if c not in ix:
            continue
        i = ix[c]
        fila = sorted(((E[i][j], R[i][j], names[j]) for j in range(k)), reverse=True)
        oe = sum(x[0] for x in fila)
        print("  desde " + c + " (" + str(oe) + " aristas) hacia: " + "; ".join(x[2] + " " + str(x[0]) + " (" + pct(x[0], oe) + "%, recip " + pct(x[1], x[0]) + "%)" for x in fila[:4] if x[0] > 0))
    pares = [(R[i][j] / E[i][j], E[i][j], R[i][j], names[i] + "->" + names[j]) for i in range(k) for j in range(k) if E[i][j] >= 1000 and names[i] != "sin_anotacion" and names[j] != "sin_anotacion"]
    pares.sort(reverse=True)
    print("PARES con >=1000 aristas: " + str(len(pares)))
    print("  mas ida y vuelta: " + "; ".join(p[3] + " " + pct(p[2], p[1]) + "% de " + str(p[1]) for p in pares[:6]))
    print("  mas una sola mano: " + "; ".join(p[3] + " " + pct(p[2], p[1]) + "% de " + str(p[1]) for p in pares[-6:]))


def main():
    res = json.load(open(sys.argv[1]))
    names = res["sin_umbral"]["clases_orden"]
    cnt = res["clases"]
    print("fuente=" + sys.argv[1])
    print("anotaciones=" + res["inputs"]["annotations"] + " md5=" + res["inputs"]["annotations_md5"])
    bloque("SIN UMBRAL", names, cnt, res["sin_umbral"]["matriz_aristas"], res["sin_umbral"]["matriz_reciprocas"])
    bloque("UMBRAL >=5 SINAPSIS", names, cnt, res["umbral_5"]["matriz_aristas"], res["umbral_5"]["matriz_reciprocas"])
    print("FIN_CABLES")


if __name__ == "__main__":
    main()
