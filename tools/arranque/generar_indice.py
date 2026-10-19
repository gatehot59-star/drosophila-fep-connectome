#!/usr/bin/env python3
"""Indice completo del repo para arrancar un chat nuevo (respuesta 2026-10-14-060).

Recorre main y todas las ramas del clon (hace falta fetch-depth 0) y escribe un Markdown con:
  B.1 las respuestas de docs/agents/respuestas/ que estan en main, con titulo, link de git y el Doc de ClickUp que nombra cada una;
  B.2 las respuestas que solo estan en ramas (el expediente de agosto, entre otras), con la rama donde viven;
  B.3 cada rama con su punta y su fecha, y cada sello o enmienda (SELLO-*.md, ENMIENDA-*.md) una vez;
  B.4 los demas .md de docs/ (contextos, papers, auditorias, adr), de main y de ramas;
  B.5 los links de ClickUp citados en los .md del repo que no son el Doc de una respuesta.
Solo lee git; no usa la red. La fecha del encabezado es la del commit de HEAD, asi que dos corridas sobre el mismo HEAD dan
el mismo archivo.
Uso: python3 tools/arranque/generar_indice.py --repo . --salida docs/agents/INDICE-COMPLETO-GIT.md
"""
import argparse
import collections
import hashlib
import re
import subprocess
import sys

BASE_DEF = "https://github.com/gatehot59-star/drosophila-fep-connectome"
RE_CU = re.compile(r"https://app\.clickup\.com/[^\s)\]>\"'`|*]+")
RE_DOC = re.compile(r"^[\s>*_\-+]*doc(?:\s+(?:p\u00fablico|publico|de\s+clickup|en\s+clickup|espejo))?[\s*_]*:", re.I)
RE_SELLO = re.compile(r"(^|/)(SELLO|ENMIENDA)[^/]*\.md$")
RESP = "docs/agents/respuestas/"


def git(repo, *args):
    r = subprocess.run(["git", "-C", repo] + list(args), capture_output=True)
    if r.returncode != 0:
        sys.stderr.write(r.stderr.decode("utf-8", "replace"))
        raise SystemExit("git fallo: " + " ".join(args))
    return r.stdout.decode("utf-8", "replace")


def limpiar(u):
    return u.rstrip(".,;:")


def doc_de(texto):
    """Devuelve (url, metodo): la ultima linea que empieza con Doc: y trae un link de ClickUp; si no, el primer link de ClickUp."""
    cand = None
    for linea in texto.splitlines():
        if RE_DOC.match(linea):
            us = RE_CU.findall(linea)
            if us:
                cand = limpiar(us[0])
    if cand:
        return cand, "linea Doc"
    us = RE_CU.findall(texto)
    if us:
        return limpiar(us[0]), "primer link"
    return None, "sin link"


def titulo_de(texto, nombre):
    for linea in texto.splitlines():
        if linea.startswith("# "):
            return linea[2:].strip()
    return nombre


def esc(s):
    return s.replace("[", "(").replace("]", ")")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", default=".")
    ap.add_argument("--salida", required=True)
    ap.add_argument("--base", default=BASE_DEF)
    a = ap.parse_args()
    repo, base = a.repo, a.base.rstrip("/")

    head = git(repo, "rev-parse", "--short=7", "HEAD").strip()
    fecha_head = git(repo, "log", "-1", "--format=%cI", "HEAD").strip()
    refs = []
    for linea in git(repo, "for-each-ref", "--format=%(refname)|%(objectname:short=7)|%(committerdate:short)", "refs/remotes/origin").splitlines():
        ref, sha, fecha = linea.split("|")
        nombre = ref[len("refs/remotes/origin/"):]
        if nombre == "HEAD":
            continue
        refs.append((nombre, ref, sha, fecha))
    nombres = [r[0] for r in refs]
    if "main" not in nombres:
        raise SystemExit("no hay origin/main en el clon (falta fetch-depth 0?)")
    orden = ["main"] + sorted(n for n in nombres if n != "main")
    porref = {r[0]: r for r in refs}

    md = collections.defaultdict(dict)
    sellos = collections.defaultdict(list)
    for n in orden:
        ref = porref[n][1]
        for linea in git(repo, "ls-tree", "-r", ref).splitlines():
            meta, path = linea.split("\t", 1)
            _, tipo, blob = meta.split()
            if tipo != "blob" or not path.endswith(".md"):
                continue
            md[path][n] = blob
            if RE_SELLO.search(path):
                sellos[n].append(path)

    cache = {}

    def leer(blob):
        if blob not in cache:
            cache[blob] = git(repo, "cat-file", "-p", blob)
        return cache[blob]

    def donde(path):
        ramas = md[path]
        r = "main" if "main" in ramas else sorted(ramas)[0]
        return r, ramas[r], len(ramas), len(set(ramas.values()))

    resp_main, resp_ramas, docs_resp = [], [], set()
    for path in sorted(p for p in md if p.startswith(RESP)):
        r, blob, nref, nver = donde(path)
        t = leer(blob)
        nombre = path[len(RESP):]
        url, metodo = doc_de(t)
        if url:
            docs_resp.add(url)
        fila = (nombre, titulo_de(t, nombre), r, path, url, metodo, nref, nver)
        (resp_main if r == "main" else resp_ramas).append(fila)

    otros_docs = sorted(p for p in md if p.startswith("docs/") and not p.startswith(RESP))
    citados = collections.defaultdict(set)
    for path in md:
        r, blob, _, _ = donde(path)
        for u in RE_CU.findall(leer(blob)):
            citados[limpiar(u)].add(path)

    out = []
    w = out.append
    w("# INDICE COMPLETO DEL REPO (generado)")
    w("")
    w("Generado por `tools/arranque/generar_indice.py` (respuesta 2026-10-14-060) sobre `%s` (%s), con main y %d ramas. "
      "No se edita a mano: se regenera corriendo el script. Repo: %s" % (head, fecha_head, len(orden) - 1, base))
    w("")
    w("Totales: %d respuestas en main, %d respuestas solo en ramas, %d ramas, %d .md de docs/ fuera de respuestas, %d links de ClickUp distintos citados."
      % (len(resp_main), len(resp_ramas), len(orden) - 1, len(otros_docs), len(citados)))
    w("")
    met = collections.Counter(f[5] for f in resp_main + resp_ramas)
    w("Doc de cada respuesta: %d por su linea Doc:, %d por el primer link de ClickUp del archivo (revisar), %d sin link." %
      (met["linea Doc"], met["primer link"], met["sin link"]))
    w("")

    def fila_resp(f, con_rama):
        nombre, tit, r, path, url, metodo, nref, nver = f
        clave = nombre[:-3] if nombre.endswith(".md") else nombre
        num = clave[:14] if re.match(r"\d{4}-\d{2}-\d{2}-\d{2,3}", clave) else clave
        s = "- `%s` [%s](%s/blob/%s/%s)" % (num, esc(tit), base, r, path)
        if con_rama:
            s += " (rama `%s`%s)" % (r, ", en %d ramas" % nref if nref > 1 else "")
        if url:
            s += " · [Doc](%s)" % url + (" (primer link, revisar)" if metodo == "primer link" else "")
        else:
            s += " · sin Doc nombrado"
        if nver > 1:
            s += " · %d versiones entre ramas" % nver
        return s

    w("## B.1 Respuestas en main (%d)" % len(resp_main))
    w("")
    for f in resp_main:
        w(fila_resp(f, False))
    w("")
    w("## B.2 Respuestas que solo estan en ramas (%d)" % len(resp_ramas))
    w("")
    for f in resp_ramas:
        w(fila_resp(f, True))
    w("")
    w("## B.3 Ramas (%d)" % (len(orden) - 1))
    w("")
    for n in orden[1:]:
        _, _, sha, fecha = porref[n]
        k = len(sellos.get(n, []))
        w("- [`%s`](%s/tree/%s) · punta `%s` · %s · %d %s adentro" % (n, base, n, sha, fecha, k, "sello o enmienda" if k == 1 else "sellos o enmiendas"))
    w("")
    unicos = collections.defaultdict(list)
    for n in orden:
        for path in sellos.get(n, []):
            unicos[(path, md[path][n])].append(n)
    w("## B.3b Sellos y enmiendas, cada version una vez (%d)" % len(unicos))
    w("")
    w("Rama: main si esta en main; si no, la rama de punta mas vieja que lo contiene (casi siempre la del experimento).")
    w("")
    for (path, blob), ramas in sorted(unicos.items(), key=lambda kv: (kv[0][0], kv[0][1])):
        origen = "main" if "main" in ramas else min(ramas, key=lambda n: (porref[n][3], n))
        w("- [%s](%s/blob/%s/%s) · `%s` · blob `%s` · en %d %s" % (path, base, origen, path, origen, blob[:7], len(ramas), "rama" if len(ramas) == 1 else "ramas"))
    w("")
    w("## B.4 Otros .md de docs/ (%d)" % len(otros_docs))
    w("")
    for p in otros_docs:
        r, blob, nref, nver = donde(p)
        s = "- [%s](%s/blob/%s/%s)" % (p, base, r, p)
        if r != "main":
            s += " (rama `%s`)" % r
        w(s)
    w("")
    resto = sorted(u for u in citados if u not in docs_resp)
    w("## B.5 Otros links de ClickUp citados en el repo (%d)" % len(resto))
    w("")
    for u in resto:
        ps = sorted(citados[u])
        w("- %s · en %s%s" % (u, ", ".join("`%s`" % p.split("/")[-1] for p in ps[:3]), " y %d mas" % (len(ps) - 3) if len(ps) > 3 else ""))
    w("")
    texto = "\n".join(out)
    open(a.salida, "w", encoding="utf-8").write(texto)
    print("INDICE escrito %s md5 %s bytes %d" % (a.salida, hashlib.md5(texto.encode("utf-8")).hexdigest(), len(texto.encode("utf-8"))))
    print("respuestas main=%d ramas=%d ramas_git=%d otros_docs=%d links_clickup=%d doc_por_linea=%d primer_link=%d sin_link=%d" % (
        len(resp_main), len(resp_ramas), len(orden) - 1, len(otros_docs), len(citados), met["linea Doc"], met["primer link"], met["sin link"]))


if __name__ == "__main__":
    main()
