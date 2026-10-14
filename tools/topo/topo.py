#!/usr/bin/env python3
"""Topo v0: lenguaje topologico ejecutable para reflejos (respuesta 2026-10-14-011).

Un programa Topo dice que tipos de neurona, de que lado y con que signo alimentan cada comando motor.
El significado esta en quien se conecta con quien (tipo x lado x signo -> comando), no en la geometria.

Dos backends, el mismo programa:
  regla     ejecuta las lineas sobre las entradas crudas: media por tipo y lado, umbral por linea, carrera.
  cableado  baja las vias a un subgrafo de FlyWire v783: neuronas elegidas y sus aristas con signo.

Gramatica v0 (una sentencia por renglon; lo que sigue a # es comentario):
  reflejo NOMBRE
  tipos T1 T2 ...                       vocabulario: tipos de celda del conectoma
  estados E1 E2 ...                     contexto del animal o del robot
  acciones A0 A1 ...                    A0 es la accion por omision (no hacer nada)
  via TIPO -> BLANCO top N por lado     backend cableado: las N de TIPO con mas sinapsis sobre BLANCO, por lado
  salida B1 B2 ...                      backend cableado: las descendentes, izquierda y derecha
  linea NOMBRE = EXPR en ESTADO -> ACCION
      EXPR := TERMINO { (+|-) TERMINO }
      TERMINO := [NUMERO *] media(TIPO@LADO, ...)      LADO es L o R; la media junta todas las entradas
  umbral falsas P sobre A0              umbral de cada linea: cuantil 1 - P de su maximo cuando la respuesta es A0
  decide carrera                        gana la primera linea que cruza; empate por mayor exceso; nadie, A0

Uso:
  python3 topo.py PROGRAMA.topo                         muestra el programa ya validado
  python3 topo.py PROGRAMA.topo --bajar CONN ANNOT      baja el backend cableado y escribe el resumen
El archivo no lleva barras invertidas: los saltos se arman con chr().
"""
import json
import sys

import numpy as np

NL = chr(10)
TAB = chr(9)
LADOS = {"L": "left", "R": "right"}
SEPARADORES = "(),=+*"


class ErrorTopo(Exception):
    pass


def tokens(s):
    s = s.replace("->", " FLECHA ")
    out, cur = [], ""
    for ch in s:
        if ch in SEPARADORES or ch == "-":
            if cur.strip():
                out.append(cur.strip())
            out.append(ch)
            cur = ""
        elif ch == " " or ch == TAB:
            if cur.strip():
                out.append(cur.strip())
            cur = ""
        else:
            cur += ch
    if cur.strip():
        out.append(cur.strip())
    return out


def _ref(tok, n):
    if "@" not in tok:
        raise ErrorTopo("renglon %d: falta el lado en %s (usar TIPO@L o TIPO@R)" % (n, tok))
    tipo, lado = tok.split("@", 1)
    if lado not in LADOS:
        raise ErrorTopo("renglon %d: lado %s desconocido (L o R)" % (n, lado))
    return (tipo, lado)


def _expr(t, n):
    """t: tokens entre '=' y 'en'. Devuelve [(coef, [(tipo, lado), ...]), ...]."""
    terminos, i, signo = [], 0, 1.0
    while i < len(t):
        if t[i] in ("+", "-"):
            signo = 1.0 if t[i] == "+" else -1.0
            i += 1
            continue
        coef = 1.0
        if i + 1 < len(t) and t[i + 1] == "*":
            try:
                coef = float(t[i])
            except ValueError:
                raise ErrorTopo("renglon %d: coeficiente invalido %s" % (n, t[i]))
            i += 2
        if i >= len(t) or t[i] != "media" or i + 1 >= len(t) or t[i + 1] != "(":
            raise ErrorTopo("renglon %d: se esperaba media(...)" % n)
        i += 2
        refs = []
        while i < len(t) and t[i] != ")":
            if t[i] != ",":
                refs.append(_ref(t[i], n))
            i += 1
        if i >= len(t):
            raise ErrorTopo("renglon %d: falta cerrar el parentesis" % n)
        i += 1
        if not refs:
            raise ErrorTopo("renglon %d: media() vacia" % n)
        terminos.append((signo * coef, refs))
        signo = 1.0
    if not terminos:
        raise ErrorTopo("renglon %d: expresion vacia" % n)
    return terminos


def parsear(texto):
    p = dict(reflejo=None, tipos=[], estados=[], acciones=[], vias=[], salidas=[], lineas=[], falsas=None,
             decide=None)
    for n, cruda in enumerate(texto.split(NL), 1):
        linea = cruda.split("#", 1)[0].strip()
        if not linea:
            continue
        t = tokens(linea)
        k = t[0]
        if k == "reflejo" and len(t) == 2:
            p["reflejo"] = t[1]
        elif k in ("tipos", "estados", "acciones", "salida") and len(t) >= 2:
            p["salidas" if k == "salida" else k] = t[1:]
        elif k == "via":
            if len(t) != 8 or t[2] != "FLECHA" or t[4] != "top" or t[6:] != ["por", "lado"]:
                raise ErrorTopo("renglon %d: via TIPO -> BLANCO top N por lado" % n)
            p["vias"].append(dict(tipo=t[1], blanco=t[3], top=int(t[5])))
        elif k == "linea":
            if len(t) < 9 or t[2] != "=" or "en" not in t or t[-2] != "FLECHA":
                raise ErrorTopo("renglon %d: linea NOMBRE = EXPR en ESTADO -> ACCION" % n)
            j = len(t) - 1 - t[::-1].index("en")
            if j != len(t) - 4:
                raise ErrorTopo("renglon %d: despues de 'en' va ESTADO -> ACCION" % n)
            p["lineas"].append(dict(nombre=t[1], terminos=_expr(t[3:j], n), estado=t[j + 1], accion=t[-1],
                                    renglon=n))
        elif k == "umbral":
            if len(t) != 5 or t[1] != "falsas" or t[3] != "sobre":
                raise ErrorTopo("renglon %d: umbral falsas P sobre ACCION" % n)
            p["falsas"] = (float(t[2]), t[4])
        elif k == "decide":
            if t[1:] != ["carrera"]:
                raise ErrorTopo("renglon %d: la unica decision de v0 es 'carrera'" % n)
            p["decide"] = "carrera"
        else:
            raise ErrorTopo("renglon %d: sentencia desconocida: %s" % (n, linea))
    validar(p)
    return p


def validar(p):
    for campo in ("reflejo", "tipos", "estados", "acciones", "lineas", "falsas", "decide"):
        if not p[campo]:
            raise ErrorTopo("falta la sentencia %s" % campo)
    if p["falsas"][1] != p["acciones"][0]:
        raise ErrorTopo("el umbral se mide sobre la accion por omision %s" % p["acciones"][0])
    if not 0.0 < p["falsas"][0] < 1.0:
        raise ErrorTopo("la tasa de falsas tiene que estar entre 0 y 1")
    vistos = set()
    for ln in p["lineas"]:
        if ln["nombre"] in vistos:
            raise ErrorTopo("renglon %d: linea repetida %s" % (ln["renglon"], ln["nombre"]))
        vistos.add(ln["nombre"])
        if ln["estado"] not in p["estados"]:
            raise ErrorTopo("renglon %d: estado desconocido %s" % (ln["renglon"], ln["estado"]))
        if ln["accion"] not in p["acciones"][1:]:
            raise ErrorTopo("renglon %d: accion desconocida o por omision %s" % (ln["renglon"], ln["accion"]))
        for _, refs in ln["terminos"]:
            for tipo, _ in refs:
                if tipo not in p["tipos"]:
                    raise ErrorTopo("renglon %d: tipo %s fuera del vocabulario" % (ln["renglon"], tipo))
    for v in p["vias"]:
        if v["tipo"] not in p["tipos"]:
            raise ErrorTopo("via: tipo %s fuera del vocabulario" % v["tipo"])
        if v["top"] < 1:
            raise ErrorTopo("via: top tiene que ser 1 o mas")


# ---------------- backend regla ----------------

def senales(p, X, tipo_ent, lado_ent):
    """X (ensayos, pasos, entradas); tipo_ent y lado_ent por entrada ('L' o 'R'). Devuelve (ensayos, pasos, lineas)."""
    n, T, k = X.shape
    par = list(zip(tipo_ent, lado_ent))
    S = np.zeros((n, T, len(p["lineas"])))
    for j, ln in enumerate(p["lineas"]):
        for coef, refs in ln["terminos"]:
            m = np.array([par[i] in refs for i in range(k)])
            if not m.any():
                raise ErrorTopo("linea %s: ninguna entrada coincide con %s" % (ln["nombre"], refs))
            S[:, :, j] += coef * X[:, :, m].mean(2)
    return S


def _compite(p, estado):
    """estado: indice en p['estados'] por ensayo. Devuelve (ensayos, lineas) booleano."""
    e_ln = np.array([p["estados"].index(ln["estado"]) for ln in p["lineas"]])
    return estado[:, None] == e_ln[None, :]


def umbrales(p, S, y, estado):
    """y: indice de accion correcta por ensayo (0 = por omision)."""
    q = 1.0 - p["falsas"][0]
    comp = _compite(p, estado)
    pico = S.max(axis=1)
    th = np.zeros(S.shape[2])
    for j in range(S.shape[2]):
        m = (y == 0) & comp[:, j]
        if not m.any():
            raise ErrorTopo("linea %s: sin ensayos de referencia para el umbral" % p["lineas"][j]["nombre"])
        th[j] = np.quantile(pico[m, j], q)
    return th


def carrera(p, S, th, estado):
    """Primera linea que compite y cruza su umbral; empate en el paso, mayor exceso; empate, la primera escrita."""
    n, T, L = S.shape
    accion = np.array([p["acciones"].index(ln["accion"]) for ln in p["lineas"]])
    comp = _compite(p, estado)
    out = np.zeros(n, dtype=int)
    for i in range(n):
        mejor, t_mejor, exc_mejor = -1, T + 1, -np.inf
        for j in range(L):
            if not comp[i, j]:
                continue
            cruza = np.nonzero(S[i, :, j] > th[j])[0]
            if cruza.size == 0:
                continue
            t0 = int(cruza[0])
            exc = float((S[i, :, j] - th[j]).max())
            if t0 < t_mejor or (t0 == t_mejor and exc > exc_mejor):
                mejor, t_mejor, exc_mejor = j, t0, exc
        out[i] = 0 if mejor < 0 else accion[mejor]
    return out


def ejecutar_regla(p, Xtr, ytr, etr, Xte, ete, tipo_ent, lado_ent):
    Str = senales(p, Xtr, tipo_ent, lado_ent)
    th = umbrales(p, Str, ytr, etr)
    Ste = senales(p, Xte, tipo_ent, lado_ent)
    return carrera(p, Ste, th, ete), th, Ste


# ---------------- backend cableado ----------------

def bajar_cableado(p, conn_path, annot_path):
    """Baja las vias y la salida a un subgrafo de FlyWire. Devuelve (seleccion, aristas).

    seleccion: [(root_id, tipo, lado, sinapsis_al_blanco, blanco)], primero las vias en orden y despues la salida.
    aristas: [(i, j, peso con signo)] entre las elegidas.
    """
    import pandas as pd
    if not p["vias"] or not p["salidas"]:
        raise ErrorTopo("el backend cableado necesita via y salida")
    a = pd.read_csv(annot_path, sep=TAB, dtype=str, usecols=["root_id", "cell_type", "side"])
    a["root_id"] = a.root_id.astype(np.int64)
    c = pd.read_parquet(conn_path, columns=["Presynaptic_ID", "Postsynaptic_ID", "Connectivity", "Excitatory"])
    sel, vistos = [], set()
    for v in p["vias"]:
        bl = a.root_id[a.cell_type == v["blanco"]]
        if len(bl) == 0:
            raise ErrorTopo("via: el blanco %s no existe en las anotaciones" % v["blanco"])
        for lado in ("left", "right"):
            cand = a[(a.cell_type == v["tipo"]) & (a.side == lado)].copy()
            m = c.Presynaptic_ID.isin(cand.root_id) & c.Postsynaptic_ID.isin(bl)
            s = c[m].groupby("Presynaptic_ID").Connectivity.sum()
            cand["s"] = cand.root_id.map(s).fillna(0)
            cand = cand.sort_values(["s", "root_id"], ascending=[False, True]).head(v["top"])
            for r, x in zip(cand.root_id, cand.s):
                if int(r) in vistos:
                    continue
                vistos.add(int(r))
                sel.append((int(r), v["tipo"], lado, float(x), v["blanco"]))
    for b in p["salidas"]:
        for lado in ("left", "right"):
            r = a[(a.cell_type == b) & (a.side == lado)].root_id
            if len(r) != 1:
                raise ErrorTopo("salida: %s %s tiene %d neuronas, se espera 1" % (b, lado, len(r)))
            sel.append((int(r.iloc[0]), b, lado, 0.0, ""))
    ids = [s[0] for s in sel]
    ix = {r: i for i, r in enumerate(ids)}
    sub = c[c.Presynaptic_ID.isin(ids) & c.Postsynaptic_ID.isin(ids)]
    aristas = [(ix[q0], ix[q1], float(w * e)) for q0, q1, w, e in sub.itertuples(index=False)]
    return sel, aristas


def main(argv):
    if len(argv) < 2:
        print(__doc__)
        return 1
    p = parsear(open(argv[1], encoding="utf-8").read())
    print("PROGRAMA %s tipos=%d estados=%d acciones=%d vias=%d salidas=%d lineas=%d falsas=%s decide=%s" % (
        p["reflejo"], len(p["tipos"]), len(p["estados"]), len(p["acciones"]), len(p["vias"]),
        len(p["salidas"]), len(p["lineas"]), p["falsas"][0], p["decide"]))
    for ln in p["lineas"]:
        print("LINEA %s en %s -> %s :: %s" % (ln["nombre"], ln["estado"], ln["accion"], ln["terminos"]))
    if "--bajar" in argv:
        i = argv.index("--bajar")
        sel, ar = bajar_cableado(p, argv[i + 1], argv[i + 2])
        print("CABLEADO neuronas=%d aristas=%d inhibitorias=%d sinapsis=%d" % (
            len(sel), len(ar), sum(1 for x in ar if x[2] < 0), int(sum(abs(x[2]) for x in ar))))
        if "--salida" in argv:
            out = argv[argv.index("--salida") + 1]
            json.dump(dict(seleccion=sel, aristas=ar), open(out, "w"))
            print("ESCRITO", out)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
