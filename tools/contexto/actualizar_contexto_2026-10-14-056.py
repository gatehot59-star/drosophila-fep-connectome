#!/usr/bin/env python3
"""Pone al dia el CONTEXTO con las respuestas 2026-10-14-055 (H_LIF_SHUFG medido) y 056 (en criollo, que sigue).

La 055 no actualizo el CONTEXTO (quedo declarado); este parche lo hace junto con la 056.
Reemplazos exactos, cada ancla tiene que aparecer una sola vez; si no, aborta sin escribir.
Uso: python3 actualizar_contexto_2026-10-14-056.py docs/agents/CONTEXTO-drosophila-fep.md
"""
import hashlib
import sys

BT = chr(96)
NL = chr(10)


def q(s):
    return s.replace("@@", BT).replace("%%", NL)


ruta = sys.argv[1]
t = open(ruta, encoding="utf-8").read()
print("md5 antes", hashlib.md5(t.encode("utf-8")).hexdigest())

NUEVO_055 = (
    "- **H_LIF_SHUFG medido (2026-10-14-055, pedido de Abraham 15:00):** instrumento f505fa3 (@@lif_shufg.py@@, "
    "agregado y prueba; prueba 12 de 12 en Actions, bot 733e958; humo 1e46f15), CORRER run 38948072997, bot "
    "bd37336, MD5SUMS 30 de 30. PIN, CTRL_REAL (30 de 30, 62,5 Hz) y NULO_MISMO (40 de 40, max 1,0e-10) pasan. El "
    "LIF de Shiu no dispara MN9 en ninguno de los 40 SHUF_G (0 espigas en 400 ensayos): H_LIF_G_SHIU y H_LIF_G_VARA "
    "SOSTENIDAS, H_LIF_K32 NO_LLEGA. k32 es el unico nulo con arista directa de azucar a MN9 (11 sinapsis, lo que "
    "infirio el sello); el real no tiene ninguna. Lectura sellada: el atajo de k32 es de nuestra celda de tasa; el "
    "freno de H_UMB_MN9 es de la neurona, no del barajado. H_UMB_MN9 y H_ENTERA_MN9_G1 siguen SIN_DECIDIR. Respuesta "
    "en @@main@@ 642b0df; esa respuesta no actualizo el CONTEXTO y lo pone al dia la 056.%%"
)
NUEVO_056 = (
    "- **En criollo, que logramos y que sigue (2026-10-14-056, pedido de Abraham 20:22):** con nuestra neurona el "
    "cableado de la mosca da el mapa (172 de 321, J 0,366; ningun barajado pasa de 103), pero MN9 sale solo con la "
    "neurona de Shiu, que acumula y dispara con umbral; la nuestra, de tasa, deja pasar entradas chicas. Lectura: el "
    "problema esta en el tipo de neurona, no en el cableado ni en el barajado; la prueba directa es sellar una celda "
    "propia que acumule. La replica de H_LECTOR termino en brain-env (6 de 6 celdas, EXIT_RUN=0); falta el cotejo. "
    "Orden propuesto: cotejo de H_LECTOR, sellar una celda de SparseLTC que integre en el tiempo con umbral y "
    "reinicio contra los mismos 80 nulos, capitulo de la mosca entera en el Paper 2 y revocar el token de Zenodo.%%"
)

R = [
    ("**Última actualización:** 2026-10-16, 13:10 (America/Buenos_Aires), con la respuesta 2026-10-14-054.",
     "**Última actualización:** 2026-10-16, 20:40 (America/Buenos_Aires), con la respuesta 2026-10-14-056."),
    ("## Madrugada y mañana del 13-oct (019 a 2026-10-14-054) · manda sobre el resto",
     "## Madrugada y mañana del 13-oct (019 a 2026-10-14-056) · manda sobre el resto"),
    ("- **Espera decisión de Abraham:** revocar el token de Zenodo, que quedo escrito en el chat (2026-10-14-034); ",
     NUEVO_055 + NUEVO_056 + "- **Espera decisión de Abraham:** revocar el token de Zenodo, que quedo escrito en el "
     "chat (2026-10-14-034); "),
    ("el instrumento del sello H_LIF_SHUFG (@@lif_shufg.py@@, agregado y prueba) con prueba y humo, y despues CORRER "
     "(2026-10-14-054); ",
     "si se sella una celda de SparseLTC que integre en el tiempo con umbral y reinicio, contra los mismos 80 nulos de "
     "MN9 (2026-10-14-055 y 056); "),
    ("leer el cotejo de la replica de H_LECTOR en brain-env cuando termine (unas 12 h, sin medir), que es condicion "
     "para Zenodo (2026-10-14-042); ",
     "hacer el cotejo de la replica de H_LECTOR, que ya termino en brain-env (6 de 6 celdas, visto en la "
     "2026-10-14-056) y es condicion para Zenodo (2026-10-14-042); "),
]
for a, b in R:
    a, b = q(a), q(b)
    n = t.count(a)
    print("ANCLA apariciones=%d :: %s" % (n, a[:60]))
    if n != 1:
        print("ABORTA: ancla no unica")
        sys.exit(2)
    t = t.replace(a, b)
open(ruta, "w", encoding="utf-8").write(t)
print("md5 despues", hashlib.md5(t.encode("utf-8")).hexdigest())
print("PARCHE OK")
