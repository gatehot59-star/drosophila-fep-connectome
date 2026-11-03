#!/usr/bin/env python3
"""Parche anclado del CONTEXTO por la respuesta 2026-11-03-002.

Absorbe las respuestas 2026-11-02-006 a 011, 2026-11-03-001 y las auditorias 2026-11-02-01 a 03, con lo que BRAIN
re-midio y lo que no. Cada ancla tiene que aparecer exactamente una vez; base y resultado se fijan por sha256.
Uso: python3 parche_contexto_2026_11_03.py CONTEXTO [--base SHA] [--resultado SHA] [--escribir]
Salidas: 0 bien; 2 base distinta; 3 ancla ausente o repetida; 4 resultado distinto.
"""
import hashlib, sys

R002 = "respuestas/2026-11-03-002-seis-documentos-contrastados-y-guardas-a1-iguales.md"

NUEVO = (
    "- **H_MECANISMO_DNp04, SOSTENIDA_EN_MODELO:** [respuesta 2026-11-02-006](respuestas/2026-11-02-006-mecanismo-dnp04-sostenida.md) y [Doc](https://app.clickup.com/90171457413/docs/2kza6fw5-26157/2kza6fw5-29357). "
    "Sello `40969fb` commiteado antes del código (`11881e3`); prueba 44/44 (run 41480897832); corrida run 41481727412 (fuente `2f991c3`), 8 celdas con las semillas de la corrida 2. "
    "D′ es D sin DNp04. En LC4, cortar sólo la fila DNp04→PVLP010 (190 sinapsis) devuelve el 40,6 % del freno que aparece al silenciar X (r_Q1 0,4056); "
    "silenciar PVLP010, el 74,6 % (r_Q2 0,7456); con Q4, PVLP010 conserva el 96,8 % de sus espigas (s4 0,9677). "
    "P1 a P4 20/20, Holm 7,63e-06; G1 a G5 verdes; proxy PARCIAL (4 de 7); apuestas 6 de 8, Brier 0,113. "
    "Verificador propio con otro algoritmo para el p exacto: todo igual; Argon lo corrió con --parquet y también dio igual. Causalidad del modelo, no de la mosca.\n"
    "- **Evaluación externa contrastada:** [respuesta 2026-11-02-007](respuestas/2026-11-02-007-evaluacion-externa-contrastada.md). "
    "En el modelo, el motivo S→X→D no es el camino que frena: S→X directo carga 23 a 49 % del freno y con LC4 el 41 % viaja por DNp04→PVLP010. "
    "La regla candidata es D→X⊣D′, inhibición recurrente entre descendentes.\n"
    "- **17 relevos D→X conservados y predictor 7/7:** la [respuesta 2026-11-02-008](respuestas/2026-11-02-008-auditoria-mejora-topo-inverso-freno-efectivo-y-veto-recurrente.md) (Argon) "
    "propuso 17 relevos recurrentes pesados D→X conservados entre FlyWire y BANC y un «Freno Efectivo Rectificado» con 7/7 y R² 0,91. "
    "La [auditoría 2026-11-02-02](../auditorias/2026-11-02-02-astra-topo-relevos-conservados-predictor-no-validado.md) (Astra) sostiene los 17 relevos frente a un nulo de grados "
    "del subgrafo pesado de BANC (1/10.001, una vez corregido un nulo que colapsaba duplicados) y deja el 7/7 como ajuste retrospectivo sobre siete combinaciones ya vistas: "
    "permutación compartida p≈0,14, y una línea base más simple llega a 6/7. No valida el mecanismo. Medido por Astra; BRAIN no lo re-midió.\n"
    "- **H_MECANISMO_RELEVOS16 / 009-A1, diseño sin runner:** el diseño [009](respuestas/2026-11-02-009-diseno-corte-causal-16-relevos-recurrentes.md) (Argon) quedó enmendado por "
    "[010](respuestas/2026-11-02-010-enmienda-009-a1-sello-original-intacto.md) sin tocar su sello: BANC es v888 (no v626) y DNp04→PVLP010 pesa 123 en BANC (no 138); "
    "las colaterales se cuentan sobre el D′ exacto; B es entrada Poisson directa, no clamp; el predictor de 008/009 queda retirado como primario; "
    "una t pareada unilateral con familias F_B (46 pruebas), F_C (6) y F_R01 (3), Holm <0,01; banco C artificial para hablar de compuertas. "
    "Las guardas anatómicas de 010 (16 D′ con huella exacta, QCOL, QXD y sus uniones, seis hubs, cascada ZA, poblaciones A y QWEAK) y las 64 guardas originales del sello 009 "
    "fueron recalculadas por BRAIN con instrumento propio sobre el parquet fijado: 314 de 314 iguales, y el control con el número colateral viejo de R03 dio rojo "
    "([respuesta 2026-11-03-002](" + R002 + ")). "
    "NO MEDIDO: manifiesto de ejecución, runner A1, su prueba con recibos corruptos, corrida, verificador distinto del productor y potencia con n=20. Ninguna corrida está autorizada.\n"
    "- **Reauditoría de los Papers 1 a 3 (Astra):** la [auditoría 2026-11-02-03](../auditorias/2026-11-02-03-astra-reauditoria-papers-topo-replica-y-rutas-visuales.md) "
    "coteja la réplica guardada de H_LECTOR (CERCA y PAGA), deja a H_PARES como ventaja promedio y no universal, y refuta la afirmación del Paper 3 de que la visión "
    "tiene que pasar por neuronas descendentes, con una ruta visual que no pasa por DN (LPi14→H2→CB0705). "
    "La [respuesta 2026-11-02-011](respuestas/2026-11-02-011-rectificacion-alcance-lectura-papers-propios.md) reconoce que la auditoría anterior de Topo no había leído los tres papers. "
    "Medido por Astra; BRAIN no lo re-midió.\n"
    "- **Errata pendiente en el Doc maestro:** la sección 15 del Doc de Topo inverso trae medias del nulo de H_REUSO_CIERRE equivocadas (80,26 % y 74,31 %; 539,86 y 328,99). "
    "Las correctas son las de este CONTEXTO (T1 49,66 % y 35,01 %; T2 286,04 y 76,515), recalculadas por BRAIN sobre los 200 nulos por mosca de "
    "`results/reuso_cierre_2026-11-01/cierre.json` (`7f3cbc1`). Es texto de otro agente: se corrige en el lugar cuando Abraham lo apruebe.\n"
    "- **Síntesis vigente en criollo:** [respuesta 2026-11-03-001](respuestas/2026-11-03-001-en-criollo-que-tenemos-y-potencial.md), de otro agente.\n"
    "- **Decisión que espera a Abraham:** autorizar la implementación y prueba del runner 009-A1 (manifiesto, fixtures chicos, SHAM, signos, poblaciones, eventos pareados, "
    "replay y recibos corruptos), sin corrida grande; y aprobar la corrección en el lugar de la sección 15 del Doc maestro.\n"
)

R = [
    ("**Última actualización:** 2026-11-02 (America/Buenos_Aires), respuesta 2026-11-02-004: H_MECANISMO leído",
     "**Última actualización:** 2026-11-03 (America/Buenos_Aires), respuesta 2026-11-03-002: contrastadas las respuestas 2026-11-02-006 a 011, "
     "2026-11-03-001 y las auditorías 2026-11-02-01 a 03; H_MECANISMO_DNp04 SOSTENIDA_EN_MODELO; guardas anatómicas de 009-A1 recalculadas con instrumento "
     "propio, 314 de 314 iguales; runner A1 sin implementar. Antes, respuesta 2026-11-02-004: H_MECANISMO leído"),
    ("con auditorías 2026-11-01-01/02, respuestas 2026-11-01-001 a 005 y 2026-11-02-001 a 004.",
     "con auditorías 2026-11-01-01/02 y 2026-11-02-01/02/03, respuestas 2026-11-01-001 a 005, 2026-11-02-001 a 011 y 2026-11-03-001 a 002."),
    ("titan/reuso-cierre-2026-11-01 y titan/mecanismo-2026-11-02, sin merge.",
     "titan/reuso-cierre-2026-11-01, titan/mecanismo-2026-11-02 y titan/mecanismo-dnp04-2026-11-02, sin merge."),
    ("el corte sellado DNp04→PVLP010 (H_MECANISMO_DNp04 propuesta y sin sellar: D sin DNp04 debería subir en LC4 y LPLC2, y no en LPLC1 ni LPLC4); ",
     ""),
    ("registrando GF y DNp06 ante looming.\n",
     "registrando GF y DNp06 ante looming.\n" + NUEVO),
]


def main():
    a = sys.argv[1:]
    ruta = a[0]
    base = a[a.index("--base") + 1] if "--base" in a else None
    res = a[a.index("--resultado") + 1] if "--resultado" in a else None
    b = open(ruta, "rb").read()
    hb = hashlib.sha256(b).hexdigest()
    print("BASE_SHA256", hb, "bytes", len(b))
    if base and hb != base:
        print("BASE_DISTINTA esperada", base)
        sys.exit(2)
    s = b.decode("utf-8")
    for k, (viejo, nuevo) in enumerate(R):
        n = s.count(viejo)
        print("ANCLA", k, "apariciones", n)
        if n != 1:
            sys.exit(3)
        s = s.replace(viejo, nuevo)
    out = s.encode("utf-8")
    ho = hashlib.sha256(out).hexdigest()
    print("RESULTADO_SHA256", ho, "bytes", len(out))
    if res and ho != res:
        print("RESULTADO_DISTINTO esperado", res)
        sys.exit(4)
    if "--escribir" in a:
        open(ruta, "wb").write(out)
        print("ESCRITO")


if __name__ == "__main__":
    main()
