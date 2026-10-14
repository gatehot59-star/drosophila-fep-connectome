#!/usr/bin/env python3
"""Deposita la v2.0 del Paper 1 como nueva version del concepto 10.5281/zenodo.19136947.

Tres modos, y solo el tercero es irreversible:

    python3 tools/zenodo/depositar_v2.py --verificar
        Sin red. Comprueba que los PDF existen con el md5 registrado y que los metadatos
        tienen los campos que Zenodo exige.

    python3 tools/zenodo/depositar_v2.py --borrador
        Crea la nueva version como BORRADOR desde la v1.0 (19136948), le saca el PDF
        heredado de la v1.0, sube los archivos de la v2.0 comparando el md5 que devuelve
        Zenodo, y carga los metadatos. NO publica. Imprime el link del borrador para que
        Abraham lo revise en Zenodo. Un borrador se puede descartar.

    python3 tools/zenodo/depositar_v2.py --publicar ID_DEL_BORRADOR
        Publica el borrador. IRREVERSIBLE: acuna el DOI de la v2.0 y no se puede borrar.
        Solo con el si explicito de Abraham.

Token: variable ZENODO_TOKEN o archivo /workspace/.zenodo_token (permisos 600). El script
nunca lo imprime ni lo escribe en los recibos. Alcances necesarios: deposit:write (subir y
editar) y deposit:actions (nueva version y publicar), segun developers.zenodo.org.
Los recibos van a docs/v2/ como JSON sin el token.
"""
import argparse
import datetime
import hashlib
import json
import os
import sys
import urllib.error
import urllib.request

API = "https://zenodo.org/api"
V1_ID = 19136948
CONCEPTO_DOI = "10.5281/zenodo.19136947"
RAIZ = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
RUTA_META = os.path.join(RAIZ, "docs", "v2", "zenodo-v2.0-metadata.json")
RUTA_ARCHIVOS = os.path.join(RAIZ, "docs", "v2", "archivos-deposito-v2.0.json")
CAMPOS_EXIGIDOS = ["title", "upload_type", "publication_type", "description", "creators", "access_right", "license", "version"]


def md5_archivo(ruta):
    h = hashlib.md5()
    with open(ruta, "rb") as f:
        for bloque in iter(lambda: f.read(1 << 20), b""):
            h.update(bloque)
    return h.hexdigest()


def leer_token():
    token = os.environ.get("ZENODO_TOKEN", "").strip()
    if not token and os.path.exists("/workspace/.zenodo_token"):
        with open("/workspace/.zenodo_token", encoding="utf-8") as f:
            token = f.read().strip()
    if not token:
        sys.exit("FALTA TOKEN: definir ZENODO_TOKEN o escribir /workspace/.zenodo_token")
    return token


def pedir(metodo, url, token, cuerpo=None, tipo="application/json"):
    solicitud = urllib.request.Request(url, method=metodo, data=cuerpo)
    solicitud.add_header("Authorization", "Bearer " + token)
    if cuerpo is not None:
        solicitud.add_header("Content-Type", tipo)
    try:
        with urllib.request.urlopen(solicitud, timeout=300) as respuesta:
            datos = respuesta.read()
            return respuesta.status, (json.loads(datos) if datos else {})
    except urllib.error.HTTPError as error:
        return error.code, {"error": error.read().decode("utf-8", "replace")[:1000]}


def cargar():
    with open(RUTA_META, encoding="utf-8") as f:
        meta = json.load(f)
    with open(RUTA_ARCHIVOS, encoding="utf-8") as f:
        archivos = json.load(f)["archivos"]
    return meta, archivos


def verificar(meta, archivos):
    ok = True
    for campo in CAMPOS_EXIGIDOS:
        presente = campo in meta["metadata"] and bool(meta["metadata"][campo])
        print("META", campo, "OK" if presente else "FALTA", flush=True)
        ok = ok and presente
    for archivo in archivos:
        ruta = archivo["ruta"]
        if not os.path.exists(ruta):
            print("ARCHIVO FALTA", ruta, flush=True)
            ok = False
            continue
        h = md5_archivo(ruta)
        coincide = h == archivo["md5"]
        print("ARCHIVO", archivo["nombre"], os.path.getsize(ruta), h, "OK" if coincide else "MD5_DISTINTO", flush=True)
        ok = ok and coincide
    print("VEREDICTO_VERIFICAR", "PASS" if ok else "FAIL", flush=True)
    return ok


def guardar_recibo(nombre, datos):
    ruta = os.path.join(RAIZ, "docs", "v2", nombre)
    with open(ruta, "w", encoding="utf-8") as f:
        json.dump(datos, f, indent=2, ensure_ascii=False)
    print("RECIBO", ruta, flush=True)


def borrador(meta, archivos):
    if not verificar(meta, archivos):
        sys.exit("NO SE CREA EL BORRADOR: la verificacion fallo")
    token = leer_token()
    estado, v1 = pedir("GET", API + "/deposit/depositions/" + str(V1_ID), token)
    print("GET v1.0", estado, flush=True)
    if estado != 200:
        sys.exit("NO SE PUDO LEER LA v1.0 CON ESTE TOKEN: " + json.dumps(v1)[:400])
    concepto = v1.get("conceptdoi") or v1.get("metadata", {}).get("conceptdoi")
    print("CONCEPTO", concepto, flush=True)
    if concepto and concepto != CONCEPTO_DOI:
        sys.exit("EL CONCEPTO NO COINCIDE: " + str(concepto))
    estado, nueva = pedir("POST", API + "/deposit/depositions/" + str(V1_ID) + "/actions/newversion", token)
    print("POST newversion", estado, flush=True)
    enlace = (nueva.get("links", {}) if isinstance(nueva, dict) else {}).get("latest_draft") or v1.get("links", {}).get("latest_draft")
    if not enlace:
        sys.exit("SIN latest_draft: " + json.dumps(nueva)[:400])
    estado, draft = pedir("GET", enlace, token)
    print("GET borrador", estado, "id", draft.get("id"), flush=True)
    if estado != 200:
        sys.exit("NO SE PUDO LEER EL BORRADOR: " + json.dumps(draft)[:400])
    id_borrador = draft["id"]
    for heredado in draft.get("files", []):
        estado, _ = pedir("DELETE", API + "/deposit/depositions/" + str(id_borrador) + "/files/" + heredado["id"], token)
        print("DELETE heredado", heredado.get("filename"), estado, flush=True)
    balde = draft["links"]["bucket"]
    subidos = []
    for archivo in archivos:
        with open(archivo["ruta"], "rb") as f:
            contenido = f.read()
        estado, resultado = pedir("PUT", balde + "/" + archivo["nombre"], token, contenido, "application/octet-stream")
        devuelto = str(resultado.get("checksum", "")).replace("md5:", "")
        coincide = devuelto == archivo["md5"]
        print("PUT", archivo["nombre"], estado, devuelto, "OK" if coincide else "MD5_DISTINTO", flush=True)
        if not coincide:
            sys.exit("EL MD5 QUE DEVOLVIO ZENODO NO COINCIDE; el borrador queda sin metadatos para revisarlo a mano")
        subidos.append({"nombre": archivo["nombre"], "md5": devuelto, "bytes": len(contenido)})
    meta["metadata"]["publication_date"] = datetime.date.today().isoformat()
    estado, actualizado = pedir("PUT", API + "/deposit/depositions/" + str(id_borrador), token, json.dumps(meta).encode("utf-8"))
    print("PUT metadatos", estado, flush=True)
    if estado != 200:
        sys.exit("METADATOS RECHAZADOS: " + json.dumps(actualizado)[:800])
    reservado = actualizado.get("metadata", {}).get("prereserve_doi", {}).get("doi")
    html = actualizado.get("links", {}).get("html")
    print("BORRADOR_LISTO id", id_borrador, "doi_reservado", reservado, "revisar en", html, flush=True)
    guardar_recibo("recibo-borrador-v2.0.json", {"id_borrador": id_borrador, "doi_reservado": reservado, "html": html, "archivos": subidos, "fecha": datetime.datetime.now(datetime.timezone.utc).isoformat()})


def publicar(id_borrador):
    token = leer_token()
    estado, resultado = pedir("POST", API + "/deposit/depositions/" + str(id_borrador) + "/actions/publish", token)
    print("POST publish", estado, flush=True)
    if estado not in (200, 202):
        sys.exit("NO SE PUBLICO: " + json.dumps(resultado)[:800])
    doi = resultado.get("doi")
    registro = resultado.get("links", {}).get("record_html") or resultado.get("links", {}).get("html")
    print("PUBLICADO doi", doi, "registro", registro, flush=True)
    guardar_recibo("recibo-publicacion-v2.0.json", {"id": id_borrador, "doi": doi, "registro": registro, "concepto": CONCEPTO_DOI, "fecha": datetime.datetime.now(datetime.timezone.utc).isoformat()})


def main():
    analizador = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    modo = analizador.add_mutually_exclusive_group(required=True)
    modo.add_argument("--verificar", action="store_true")
    modo.add_argument("--borrador", action="store_true")
    modo.add_argument("--publicar", metavar="ID_DEL_BORRADOR")
    argumentos = analizador.parse_args()
    meta, archivos = cargar()
    if argumentos.verificar:
        sys.exit(0 if verificar(meta, archivos) else 1)
    if argumentos.borrador:
        borrador(meta, archivos)
        return
    publicar(argumentos.publicar)


if __name__ == "__main__":
    main()
