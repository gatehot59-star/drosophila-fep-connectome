#!/usr/bin/env python3
"""Pone al dia el CONTEXTO del conectoma con la 010 a la 018 y deja en la 017 el puntero a su correccion.

Respuesta 2026-10-12-018. Cada cambio exige exactamente un ancla. Uso: python3 actualizar_contexto_018.py <raiz>
"""
import hashlib, os, sys

raiz = sys.argv[1]
CTX = "docs/agents/CONTEXTO-drosophila-fep.md"
R17 = "docs/agents/respuestas/2026-10-12-017-objetivamente-mapa-y-reflejos-chicos-no-cerebro-y-la-regla-a-mano-sigue-adelante.md"
R18 = "docs/agents/respuestas/2026-10-12-018-paga-la-tarea-de-la-mosca-la-regla-era-la-mosca-idealizada-y-la-v2-quedo-corregida.md"

CABECERA = ("**Última actualización:** 2026-10-13, 00:50 (America/Buenos_Aires), con la respuesta 2026-10-12-018. "
            "**La sección «Tarde y noche del 12-oct (010 a 018)» manda sobre lo que choque en el resto del archivo**, "
            "que sigue escrito al estado de la 009 (11:58).")

BLOQUE = """
## Tarde y noche del 12-oct (010 a 018) · manda sobre el resto

- **Paper 1 v2.0 (010 y 018):** la 010 retiró «lista para depositar» por tres inconsistencias internas del manuscrito del PR #27. **La 018 las corrigió** con `tools/v2/fix_v2_018.py`, aplicado en brain-env y en Actions con md5 iguales:
  - el «2.4-fold» era visual sobre gustatory; el cociente entre extremos es 4,2× sin umbral y baja de 3.862× a 40× con el umbral;
  - la amplificación temporal aparece con SparseLTC y Linear y no con LIF-soft (0,253 a 0,002); corregido también en el erratum, ítem 7, porque la v1.0 tenía el mismo error;
  - el cero de olfato y visión sin umbral es compatible con el nulo de neurópilo (1,0 ± 0,9 y 0,03 ± 0,16), no intesteable; sólo con el umbral el nulo es 0,0 exacto.
  - PDF nuevos en `/workspace/v2cierre_2026-10-12/deposito_018/`: manuscrito `d353cf0f…` (17 páginas) y erratum `05052e6e…` (15 páginas); render PASS y verificación PASS en clon fresco de `f19a9c7`.
  - **Falta:** la Tabla 8 (el resumen y el §4.1 usan +14,8σ como firme y no se reprodujo), el informe archivado de Tao (comunicó hallazgos a las 13:25 en su chat, 010), el merge y el token.
- **No es la neurona (011):** el motivo de 28 llevaba el 2,96% de la entrada de sus descendentes y nada de su inhibición; la DCMT como vino invierte el glutamato (17% del cerebro).
- **Líneas etiquetadas (012): NO PAGAN** con la tarea de la 005; lo que decidía era un supuesto de entrada (LPLC2 al punto).
- **Fisiología (013 y 014):** LPLC2 responde a objetos que pasan (Kim 2023) y la mosca esquiva en vuelo por DNp06, cuya mayor entrada es LPLC1 (1.023 sinapsis) y después LPLC2 (1.003); las barras de adelante hacia atrás piden aterrizaje (Ache 2019).
- **Tarea de la mosca (015 sellada, 016 corrida, 018 leída): PAGA LA TAREA DE LA MOSCA.** 46 neuronas, cinco acciones, líneas etiquetadas sin entrenar: W les gana a 300 SL y 300 T en 6/6 celdas (Holm 0,0399), instrumento VÁLIDO. Contra la regla a mano: PEOR en 4, EMPATE en 2, nunca MEJOR.
  - **La regla a mano es el mismo diseño de la mosca idealizado** (las etiquetas tipo → descendente de FlyWire sobre las entradas crudas): el diseño paga y nuestra simulación de sus sinapsis le resta.
  - Descriptivo: con LPLC4 muda W aguanta más que la regla (0,8030 contra 0,7680); con ruido 0,45 W gira mejor en 2 de 3 amplitudes.
  - Rama `titan/tarea-mosca-2026-10-12`: sello `57d094a`, log `bdf03c2` (md5 `ad8c94b4…`).
- **Qué le falta al modelo (018):** las 6 descendentes reciben 40.145 sinapsis; el motivo lleva 875 (2,18%) y 0 de las 14.576 inhibitorias (36,3%). R1 (con sus presinápticas de 5 sinapsis o más) tiene 1.504 neuronas; R2, 33.489. Rama `titan/que-falta-al-modelo-2026-10-12` (`3cf6332`).
- **Corrección a la 017:** «la mosca no reemplaza a la ingeniería» estaba mal planteado; lo que le ganó a nuestro modelo fue la mosca idealizada.
- **Máquinas (016 y 017):** para un script numpy sellado la máquina rápida es Actions (11,6×), no Kaggle con GPU; Kaggle sólo con un port a torch verificado contra numpy.
- **Espera decisión de Abraham:** sellar el factorial de la 018 (recorte 46 / R1 / R2, neurona de tasa / LIF con signo / líquida plena, con y sin inhibición; misma tarea, mismos nulos, la regla idealizada como rival); la Tabla 8; el merge del PR #27 y el token de Zenodo.
"""

PUNTERO = ("\n**Corregido por la 018:** la regla a mano de la 015 es el mismo diseño de la mosca idealizado, no un control "
           "clásico, y la corrida completa dio PAGA LA TAREA DE LA MOSCA (6/6 contra SL y T). Ver `" + R18 + "`.\n")

def leer(r):
    with open(os.path.join(raiz, r), encoding="utf-8") as f:
        return f.read()

def escribir(r, t):
    with open(os.path.join(raiz, r), "w", encoding="utf-8") as f:
        f.write(t)

ctx = leer(CTX)
print("ANTES", CTX, hashlib.md5(ctx.encode()).hexdigest())
lineas = ctx.split("\n")
i_cab = [i for i, l in enumerate(lineas) if l.startswith("**Última actualización:**")]
i_base = [i for i, l in enumerate(lineas) if l.startswith("**Base vigente del paper:**")]
print("ANCLA cabecera=%d base=%d" % (len(i_cab), len(i_base)))
assert len(i_cab) == 1 and len(i_base) == 1
lineas[i_cab[0]] = CABECERA
lineas.insert(i_base[0] + 1, BLOQUE.rstrip("\n"))
ctx = "\n".join(lineas)
viejo = "el spread cae a 2,4×"
print("ANCLA spread=%d" % ctx.count(viejo))
assert ctx.count(viejo) == 1
ctx = ctx.replace(viejo, "el cociente entre extremos cae a 4,2× sin umbral (la v2.0 decía 2,4×, que era visual sobre gustatory: corregido en la 018)")
escribir(CTX, ctx)
print("DESPUES", CTX, hashlib.md5(ctx.encode()).hexdigest())

r17 = leer(R17)
print("ANTES", R17, hashlib.md5(r17.encode()).hexdigest())
l17 = r17.split("\n")
i_doc = [i for i, l in enumerate(l17) if l.startswith("**Doc espejo:**")]
print("ANCLA doc_espejo_017=%d" % len(i_doc))
assert len(i_doc) == 1 and "Corregido por la 018" not in r17
l17.insert(i_doc[0] + 1, PUNTERO.rstrip("\n"))
r17 = "\n".join(l17)
escribir(R17, r17)
print("DESPUES", R17, hashlib.md5(r17.encode()).hexdigest())
assert os.path.exists(os.path.join(raiz, R18)), "falta la 018 en main"
print("CONTEXTO OK")
