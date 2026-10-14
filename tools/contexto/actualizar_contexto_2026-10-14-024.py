#!/usr/bin/env python3
"""Pone al dia el CONTEXTO con la 2026-10-14-024 (H_FRENO REFUTADA en brain-env).

Reemplazos exactos, cada ancla tiene que aparecer una sola vez; si no, aborta sin escribir.
Uso: python3 actualizar_contexto_2026-10-14-024.py docs/agents/CONTEXTO-drosophila-fep.md
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

NUEVO = q(
    "- **H_FRENO REFUTADA en brain-env (2026-10-14-024, ClickKit @@correr_freno_023@@, 20:10):** @@CORRER@@ en "
    "@@d74eaf3@@; el mismo instrumento sellado corrio en brain-env (19 s, log md5 c474e1f3, rama @@d2240a6@@). Control "
    "positivo PASA (percentil 0,981 y 0,982). Los 7 mecanismos dan DESCARTADO o AUSENTE: ni DNp07, ni DNp01, ni la DNp06 "
    "opuesta inhiben directo a DNp06; por interneurona, lo del otro lado aporta 0,4 a 0,9 por ciento de su inhibicion y "
    "el detector bilateral menos de 0,1. Post hoc (descriptivo): las dos primeras inhibitorias de DNp06 son LHAD1g1 "
    "(GABA, una por lado, 11 a 13 por ciento, alimentada por LPLC2 y LC4 del MISMO lado) y PVLP010 (glutamato, "
    "alimentada por LC4 del mismo lado): inhibicion de avance ipsilateral, que no distingue frente de costado. Lectura: "
    "a dos saltos en el cerebro no hay freno cableado del giro ante el looming frontal; queda en el cordon nervioso, en la "
    "dinamica o en que el looming frontal no excite a DNp06 en la mosca (supuesto del modelo de entrada, NO MEDIDO).%%"
)

R = [
    ("**Última actualización:** 2026-10-14, 20:10 (America/Buenos_Aires), con la respuesta 2026-10-14-023.",
     "**Última actualización:** 2026-10-14, 20:15 (America/Buenos_Aires), con la respuesta 2026-10-14-024."),
    ("## Madrugada y mañana del 13-oct (019 a 2026-10-14-023) · manda sobre el resto",
     "## Madrugada y mañana del 13-oct (019 a 2026-10-14-024) · manda sobre el resto"),
    ("- **Espera decisión de Abraham:** el token de Zenodo para el borrador del depósito de la v2 (publicar, "
     "solo con su sí); leer H_DEBILES",
     NUEVO + "- **Espera decisión de Abraham:** el token de Zenodo para el borrador del depósito de la v2 (publicar, "
     "solo con su sí); leer H_DEBILES"),
    (q("correr H_FRENO, sellado en la 2026-10-14-023 (su @@CORRER@@, segundos); "),
     "confirmar H_FRENO en Actions; decidir si se prueba que el looming frontal no excita a DNp06 en la mosca "
     "(2026-10-14-024); "),
]
for a, b in R:
    n = t.count(a)
    print("ANCLA apariciones=%d :: %s" % (n, a[:60]))
    if n != 1:
        print("ABORTA: ancla no unica")
        sys.exit(2)
    t = t.replace(a, b)
open(ruta, "w", encoding="utf-8").write(t)
print("md5 despues", hashlib.md5(t.encode("utf-8")).hexdigest())
print("PARCHE OK")
