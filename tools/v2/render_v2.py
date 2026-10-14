#!/usr/bin/env python3
"""Renderiza la v2.0 del Paper 1 y el erratum a PDF, de forma determinista.

Cadena: pandoc (markdown -> typst) + typst (paquete de PyPI `typst`, compilador embebido).
Se antepone `#set document(date: none)` para que el PDF no lleve la hora de la corrida:
dos corridas con las mismas fuentes dan el mismo md5, y el script lo comprueba.
Tambien se apaga la particion silabica para que la extraccion de texto no corte palabras.

Uso:
    python3 tools/v2/render_v2.py DIRECTORIO_DE_SALIDA

Imprime, por archivo: md5 y bytes de la fuente, md5 y bytes del PDF, paginas, si dos
compilaciones dieron el mismo PDF, y una lista de cadenas que tienen que aparecer en el
texto extraido (pypdf). Sale con codigo 1 si falta alguna o si no es determinista.
En brain-env: pandoc 3.10.2 en /opt/mamba/bin/pandoc, typst 0.15.0 por pip, pypdf 6.16.2.
"""
import hashlib
import os
import re
import shutil
import subprocess
import sys

RAIZ = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
PANDOC = shutil.which("pandoc") or "/opt/mamba/bin/pandoc"
PREAMBULO = "#set document(date: none)\n#set text(hyphenate: false)\n"

FUENTES = [
    (
        "docs/v2/paper1-v2.0.md",
        "Mendieta2026_Paper1_v2.0.pdf",
        [
            "Version 2.0",
            "10.5281/zenodo.19136947",
            "7.85197",
            "12.38",
            "Table 5b",
            "Table 5c",
            "101.6",
            "20.59",
            "13.98%",
            "8.6%",
            "7.9 ms",
            "gatehot59-star/drosophila-fep-connectome",
            "Changes from version 1.0",
            "Gordon, M.D. & Scott, K. (2009)",
        ],
    ),
    (
        "docs/ERRATUM.md",
        "Mendieta2026_Paper1_Erratum_v1.0.pdf",
        [
            "Erratum to Mendieta (2026a)",
            "0.000785197",
            "8.6",
            "98.5 per cent",
            "Outstanding verification",
        ],
    ),
]


def md5_bytes(b):
    return hashlib.md5(b).hexdigest()


def normalizar(texto):
    return re.sub(r"\s+", "", texto)


def main():
    if len(sys.argv) != 2:
        sys.exit("uso: render_v2.py DIRECTORIO_DE_SALIDA")
    salida = os.path.abspath(sys.argv[1])
    os.makedirs(salida, exist_ok=True)
    import typst
    from pypdf import PdfReader

    version_pandoc = subprocess.run([PANDOC, "--version"], capture_output=True, text=True, check=True).stdout.splitlines()[0]
    print("ENTORNO", version_pandoc, "| typst", getattr(typst, "__version__", "?"), flush=True)
    todo_ok = True
    for fuente, nombre_pdf, chequeos in FUENTES:
        ruta_fuente = os.path.join(RAIZ, fuente)
        crudo = open(ruta_fuente, "rb").read()
        print("FUENTE", fuente, len(crudo), md5_bytes(crudo), flush=True)
        ruta_typ = os.path.join(salida, nombre_pdf[:-4] + ".typ")
        subprocess.run([PANDOC, ruta_fuente, "-f", "markdown", "-t", "typst", "-s", "-o", ruta_typ], check=True)
        texto_typ = open(ruta_typ, encoding="utf-8").read()
        with open(ruta_typ, "w", encoding="utf-8") as f:
            f.write(PREAMBULO + texto_typ)
        pdf_1 = typst.compile(ruta_typ)
        pdf_2 = typst.compile(ruta_typ)
        determinista = pdf_1 == pdf_2
        ruta_pdf = os.path.join(salida, nombre_pdf)
        with open(ruta_pdf, "wb") as f:
            f.write(pdf_1)
        lector = PdfReader(ruta_pdf)
        extraido = "".join((pagina.extract_text() or "") for pagina in lector.pages)
        plano = normalizar(extraido)
        faltan = [c for c in chequeos if normalizar(c) not in plano]
        print("PDF", nombre_pdf, len(pdf_1), md5_bytes(pdf_1), "paginas", len(lector.pages), "determinista", determinista, flush=True)
        for c in chequeos:
            print("  CHEQUEO", "OK " if c not in faltan else "FALTA", c, flush=True)
        if faltan or not determinista:
            todo_ok = False
    print("VEREDICTO_RENDER", "PASS" if todo_ok else "FAIL", flush=True)
    sys.exit(0 if todo_ok else 1)


if __name__ == "__main__":
    main()
