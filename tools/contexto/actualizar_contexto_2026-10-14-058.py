#!/usr/bin/env python3
"""Pone al dia el CONTEXTO con la respuesta 2026-10-14-058 (pares artificiales) y corrige la entrada de la 057.

Reemplazos exactos, cada ancla tiene que aparecer una sola vez; si no, aborta sin escribir.
Uso: python3 actualizar_contexto_2026-10-14-058.py docs/agents/CONTEXTO-drosophila-fep.md
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

NUEVO_058 = (
    "- **Pares artificiales (2026-10-14-058, pregunta de Abraham 17-oct 18:47):** H_RIVAL comparo la mosca contra un "
    "techo y no contra su par: el ridge leyo las 22.560 entradas crudas con 2.400 ensayos etiquetados y unos 135.000 "
    "pesos (cuenta sobre el sello), contra 6 umbrales de la mosca calibrados solo con ensayos sin evento "
    "(@@umbrales()@@ de @@tarea_mosca.py@@) y una tau elegida entre 10; la asimetria estaba declarada en el sello "
    "(Limitacion 3), pero la 057 la resumio de mas y queda corregida. Cuatro preguntas, cuatro rivales: barajados (si "
    "importa el cableado; hecho), par artificial al mismo presupuesto (si conviene tomar la pieza; casi sin hacer), "
    "techo sin limite (cuanto falta; H_RIVAL) y la mosca o un modelo validado (Shiu). Pares ya medidos: el motivo de 26 "
    "como reservorio empata con su barajado y no le gana al ruido en tareas genericas (2026-10-11-008), la liquida "
    "plena gana a su control no liquido, DBC3 empata con LSTM, SparseLTC empata con su control lineal (HC-2) y gana a "
    "la propagacion sin dinamica (049). Literatura: FLYNN (Wang y Chen, arXiv 2607.00025) rinde como redes "
    "artificiales del mismo tamano y aguanta mejor fuera de lo entrenado; Dhiman (arXiv 2604.04033) ve desaparecer la "
    "ventaja con nulo que conserva grados e igual inicializacion. Lo que queremos tomar de la mosca (competencia con "
    "pocos datos, robustez, costo) esta NO MEDIDO. Propuesta sin sellar, H_PARES: 1) curva de datos en R2 con el "
    "embudo de la mosca contra PCA y proyeccion aleatoria de 240 rasgos; 2) robustez sin reentrenar (sensor apagado, "
    "ruido fuera de lo entrenado, neuronas muertas); 3) R2 contra reservorios Erdos-Renyi y de mundo pequeno del mismo "
    "tamano.%%"
)

R = [
    ("**Última actualización:** 2026-10-17, 09:25 (America/Buenos_Aires), con la respuesta 2026-10-14-057.",
     "**Última actualización:** 2026-10-17, 19:10 (America/Buenos_Aires), con la respuesta 2026-10-14-058."),
    ("## Madrugada y mañana del 13-oct (019 a 2026-10-14-057) · manda sobre el resto",
     "## Madrugada y mañana del 13-oct (019 a 2026-10-14-058) · manda sobre el resto"),
    ("Pero no es un cerebro mejor que lo clasico: un ridge entrenado sobre las mismas 564 entradas le gana por 5 "
     "puntos (H_RIVAL),",
     "En acierto dentro de lo entrenado, un ridge entrenado sobre las mismas 564 entradas le gana por 5 puntos "
     "(H_RIVAL, con 2.400 ensayos etiquetados y unos 135.000 pesos contra 6 umbrales; la 2026-10-14-058 corrige el "
     "«no es un cerebro mejor que lo clasico»),"),
    ("conviene lo clasico (ridge o la regla del plano) y la mosca aporta el plano.",
     "conviene lo clasico (ridge o la regla del plano) y la mosca aporta el plano [corregido en la 2026-10-14-058: es "
     "solo acierto dentro de lo entrenado, con capacidad y datos desiguales; para un producto decide la comparacion "
     "con su par artificial al mismo presupuesto, en datos, robustez y costo, NO MEDIDA]."),
    ("- **Espera decisión de Abraham:** revocar el token de Zenodo, que quedo escrito en el chat (2026-10-14-034); ",
     NUEVO_058 + "- **Espera decisión de Abraham:** revocar el token de Zenodo, que quedo escrito en el chat "
     "(2026-10-14-034); si se sella H_PARES y por cual pieza se empieza (datos y embudo, robustez o reservorio; "
     "2026-10-14-058); "),
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
