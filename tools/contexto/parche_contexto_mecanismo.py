#!/usr/bin/env python3
"""Parche anclado del CONTEXTO por la respuesta 2026-11-02-004 (H_MECANISMO MIXTA en el modelo).

Cada ancla tiene que aparecer exactamente una vez en la base; la base y el resultado se fijan por sha256.
Uso: python3 parche_contexto_mecanismo.py CONTEXTO [--base SHA] [--resultado SHA] [--escribir]
Salidas: 0 bien; 2 base distinta; 3 ancla ausente o repetida; 4 resultado distinto.
"""
import hashlib, sys

NUEVO = (
    "- **H_MECANISMO, MIXTA en el modelo:** [respuesta 2026-11-02-004](respuestas/2026-11-02-004-mecanismo-reconstruido.md) y [Doc](https://app.clickup.com/90171457413/docs/2kza6fw5-26157/2kza6fw5-29337). "
    "Modelo LIF de Shiu sin tocar (philshiu/Drosophila_brain_model@91bdd1e7, Brian2 2.10.1), FlyWire 783 entero, S con Poisson a 50 Hz, 20 ensayos de 1 s con semillas comunes. "
    "Sello `3c47400`, enmienda `3e34d46`, run 41459331354 (fuente `b3b398d`, evidencia `8ffdfc6a`). "
    "Silenciar X sube a D entre 40 y 237 %; P1 a P4 pasan en los cuatro estímulos (20/20, p exacto 1,9e-06, Holm 3,05e-05). "
    "X frena por sus sinapsis directas (ΔXD/ΔX 1,02 / 0,72 / 1,09 / 0,79), pero S→X directo carga solo 23 a 49 % del freno "
    "(ΔSX/ΔX 0,289 / 0,260 / 0,232 / 0,487, debajo de 0,5 en los cuatro): cuatro PARCIAL. "
    "Verificador propio en `72e9eff`: veredicto, filas tocadas, K, fuera del objetivo y réplica izquierda iguales al agregado; "
    "su v1 tenía un error en la línea de fuera del objetivo y se corrigió. Es causalidad del modelo, no de la mosca.\n"
    "- **Qué enciende al freno, post hoc y no sellado (`aaea8b6`):** las sinapsis S→X directas sostienen alrededor de la mitad de las espigas de X. "
    "En LC4, el 72,5 % del freno lineal es PVLP010 (glutamato), relevo uno a uno de DNp04 por 190 sinapsis (107,3 y 106,7 espigas/s; "
    "en el modelo bastan 162 sinapsis de una neurona para cruzar el umbral con una espiga): inhibición recurrente entre descendentes. "
    "En LPLC2 el freno se reparte entre LHAD1g1 (S directo), AVLP080 (otras vías) y PVLP010 (DNp04); en LPLC1 es AVLP080 (62 %); "
    "en LPLC4 se reparte en 56 tipos. X veta descendentes enteros: con LC4, DNp06 pasa de 0 a 61,7 espigas/s al silenciar X. "
    "El ranking anatómico no predice quién frena: LHAD1g1 tiene 399 sinapsis sobre DNp06 y con LC4 lleva el 2 % del freno.\n"
    "- **Corridas del mecanismo:** la corrida 1 (run 41410027436) dio INVALIDA por infraestructura, con 8 de 17 celdas muertas por exit 143 "
    "([respuesta 2026-11-02-002](respuestas/2026-11-02-002-mecanismo-corrida1-verificada.md)). "
    "La enmienda aisló cada ensayo en su proceso y partió las celdas principales; la corrida 2 replicó a la 1 espiga por espiga en las 9 celdas comunes "
    "([respuesta 2026-11-02-003](respuestas/2026-11-02-003-mecanismo-corrida2-replica.md)). "
    "Apuestas selladas: 2 de 6 ganadas, Brier 0,244. K quedó emparejado solo en LPLC1; en los otros tres el pool activo llegó a 26 a 37 % del impulso de X.\n"
    "- **Pendiente del mecanismo, NO MEDIDO:** la mosca; el efecto causal de cada tipo de X; el corte sellado DNp04→PVLP010 "
    "(H_MECANISMO_DNp04 propuesta y sin sellar: D sin DNp04 debería subir en LC4 y LPLC2, y no en LPLC1 ni LPLC4); BANC en el modelo; "
    "robustez a peso por sinapsis, tau y umbral; por qué DNp03 no dispara en el modelo; función y formación. "
    "Experimento en la mosca propuesto: RNAi de GluClα contra Rdl solo en el GF, y silenciar DNp04, registrando GF y DNp06 ante looming.\n"
)

R = [
    ("**Última actualización:** 2026-11-02 (America/Buenos_Aires), respuesta 2026-11-02-001: H_REUSO_CIERRE leído",
     "**Última actualización:** 2026-11-02 (America/Buenos_Aires), respuesta 2026-11-02-004: H_MECANISMO leído y verificado con instrumento propio, "
     "MIXTA en el modelo de Shiu (cuatro PARCIAL). Antes, respuesta 2026-11-02-001: H_REUSO_CIERRE leído"),
    ("respuestas 2026-11-01-001 a 005 y 2026-11-02-001.",
     "respuestas 2026-11-01-001 a 005 y 2026-11-02-001 a 004."),
    ("titan/reuso-estricto-2026-11-01 y titan/reuso-cierre-2026-11-01, sin merge.",
     "titan/reuso-estricto-2026-11-01, titan/reuso-cierre-2026-11-01 y titan/mecanismo-2026-11-02, sin merge."),
    ("no se atribuye causalmente la diferencia sólo al signo.\n",
     "no se atribuye causalmente la diferencia sólo al signo.\n" + NUEVO),
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
