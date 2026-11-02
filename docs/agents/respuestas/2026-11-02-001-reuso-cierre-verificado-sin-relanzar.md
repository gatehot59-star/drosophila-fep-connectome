# 2026-11-02-001 · H_REUSO_CIERRE verificado sin relanzar: SOSTENIDA en FlyWire y BANC

Doc: https://app.clickup.com/90171457413/docs/2kza6fw5-26157
Ruta: Space > Topo inverso > sección 15, sin carpeta intermedia.

## 1. Pedido y conclusión derivada

«Verificá ahora el resultado terminado, sin relanzarlo» (2-nov-2026, 01:48 ART).

**Verificado: corrida VÁLIDA y H_REUSO_CIERRE SOSTENIDA en ambos conectomas.** No se relanzó el experimento, no se generaron nuevos barajados y no se cambió el diseño. Se descargaron los recibos ya publicados, se ejecutó el verificador preparado en el turno anterior y se recalcularon los descriptivos con otro fragmento de biblioteca estándar.

La lectura pendiente que el Doc llamaba «2026-11-01-006, en curso» se cierra con este archivo del 2-nov, no con una respuesta retrodatada. El resultado científico se produjo el 1-nov; esta fecha corresponde a su verificación y publicación documental.

En criollo: aun dejando intactas las conexiones directas y conservando cuánto conecta cada neurona con destinos de cada clase, lado, signo y rol, el cableado real cierra más vías por X inhibitorias predichas y reutiliza más X que los 200 barajados de cada atlas. Eso fortalece al motivo como candidato anatómico; **no demuestra todavía una gramática generadora, una función útil nueva ni ahorro de cálculo**. G1 sigue sin diseñar.

## 2. Qué se comprobó

- FlyWire: 880/996 pares con plantilla, T1 = 88,3534 %. Nulo de cierre: 457 a 524 pares, media 494,62; T1 media 49,6606 %, máximo 52,6104 %. T2: 698 X compartidas frente a media 286,04 y máximo 326.
- BANC: 622/753 pares con plantilla, T1 = 82,6029 %. Nulo de cierre: 233 a 286 pares, media 263,63; T1 media 35,0106 %, máximo 37,9814 %. T2: 419 X compartidas frente a media 76,515 y máximo 95.
- 200 nulos por conectoma, 400/400 filas conciliadas exactamente entre JSON y log; semillas 22029/22030. Denominadores fijos 996 y 753 en todos los sorteos. Huellas distintas dentro de cada serie, guardas activas y mezcla superior al umbral sellado.
- Cero superaciones en las cuatro pruebas. Recomputo racional: cada p = 1/201, no cero; Holm sobre las cuatro = 4/201 = 0,01990049751243781. El veredicto coincide con la regla sellada.
- El verificador rechazó seis recibos corruptos por el motivo esperado, incluidos signo apagado y denominador alterado simultáneamente en JSON y log. Exit 0 para el recibo real.
- Las diez combinaciones de métrica/conectoma en los resúmenes se recalcularon desde las 400 filas, sin confiar en las medias publicadas.

T1 es una proporción de pares cableados; T2 cuenta X que sirven a al menos dos tipos distintos de descendente. S es proyección visual, no sensorial. El signo es predicho, no fisiología comprobada.

### La corrección de FlyWire sigue siendo importante

En el nulo ESTRICTO anterior, el real tenía menos pares con plantilla en cantidad (880 frente a 932 a 1.060), pero mayor proporción y reuso. Eso no cambia retroactivamente. En este nulo de CIERRE, con el denominador fijo, sí supera también en cantidad (880 frente a 457 a 524). Son comparaciones distintas.

La auditoría 2026-11-01-02 queda como antecedente: R1 corrigió cantidad/proporción; R2 señaló el signo no conservado, ahora probado junto con roles y cableado directo fijo; R3 registró retroactivamente 001 a 005 en el pizarrón; R4 corrigió el QA de 005 a 56/60 = 93,3/100. Este turno verifica el resultado de cierre, no repite aquella auditoría ni se presenta como revisión independiente.

### Controles que ya ejecutó el runner, no reejecutados hoy

El log original conserva 28/28 controles de cierre (una comprobación envuelve la suite estricta 25/25), positivo y negativo end-to-end SOSTENIDA/REFUTADA, y mutación que elimina el signo del estrato: 24/28, exit 3. Fallan closure_guards_39, closure_budgets_39, closure_not_fooled_by_first_order y complete_plan_39. El INVALIDO temprano del log pertenece a ese mutante deliberado; no al ensayo real, cuyo cierre es VALID, exit 0.

La implementación alternativa scipy.sparse, sin merge/groupby de pandas, se contrastó en los observados y en los sorteos de cierre 0/199 de ambos conectomas. Hoy se verifican el código fijado y los recibos de esa comprobación; no se recalculan los grafos grandes.

REPRO_ESTRICTO = PASS: el runner regeneró y cotejó las 400 huellas estrictas, y recalculó estadísticas de los sorteos 0/199 por ambos métodos. El verificador de hoy coteja ese recibo con el JSON estricto fijado y con el log; no regeneró las 400 permutaciones. No equivale a recalcular todas las estadísticas estrictas ni a una réplica por otra instancia.

Primer orden, descriptivo: en FlyWire las S destinan a X candidatas el 36,2476 % de sus filas y 42,2257 % del peso. El cierre conserva ambos; los sorteos estrictos 0/199 daban 29,8053/29,8561 % de filas y 31,1307/31,4791 % del peso. En BANC: real/cierre 32,3096 % y 37,7473 %; estricto 27,2550/27,1176 % y 28,1823/28,2279 %. Esto confirma la dilución que motivó el control. Como cambiaron signo, rol y cableado directo a la vez, no identifica el efecto causal aislado del signo.

## 3. Procedencia, máquinas y herramientas

[Corrida científica original](https://github.com/gatehot59-star/drosophila-fep-connectome/actions/runs/41330973057): completed/success, intento 1. Lectura estructurada de API: 2026-11-02T04:48:40.903699Z. Job 124920801238, del 1-nov 17:20:30 a 17:32:00 UTC (14:20:30 a 14:32:00 ART).

Fuente f734a23120159b5caf367a88503268b313e7a8e1; sello a2bf422253b42bfc4215018c01b22c7f9113d426. Resultado del bot 7f3cbc1b1ff2243149ba45d10c18abb4ce5311e4, hijo directo de la fuente, con sólo JSON y log como archivos cambiados.

- [JSON original íntegro](https://github.com/gatehot59-star/drosophila-fep-connectome/blob/7f3cbc1b1ff2243149ba45d10c18abb4ce5311e4/results/reuso_cierre_2026-11-01/cierre.json): 371.287 bytes; SHA256 a5c689d4153a9f4fcfadc573cac58521f1ade330b82d1d122dfae6f15c41aceb.
- [Log original íntegro](https://github.com/gatehot59-star/drosophila-fep-connectome/blob/7f3cbc1b1ff2243149ba45d10c18abb4ce5311e4/results/reuso_cierre_2026-11-01/run-41330973057.log): 422.115 bytes; SHA256 6203f6035de2a3d9c1165e56a4066da79ee714065575cf05810a931e1cdc6b7f.
- Fuente reuso_cierre.py descargada del commit ejecutado: 29.256 bytes; SHA256 db27c17b31e5bceb4a237f1e86ccfb30a57b19ad3a6e9a70e4a25232faf56783. Coincide con el pin del JSON y del workflow.
- Workflow científico: 7.430 bytes; SHA256 1b931b79e538ece516ed7010e32031f150987916ed985f76a0b7c8878b461a1a. Sólo dispara por cambios del productor o de ese workflow, que no se modificaron.
- Sello: 6.956 bytes; SHA256 9146e29815e46c99ad7dd00cd968b40edd92c3fa0c55c0a381e3bf13a5d85e7b.
- Verificador usado, íntegro en el apéndice A: 12.426 bytes; SHA256 0ce8261ae0cd2fa1b3731c98b7daa7c522413ef0a75dcb799033763b421d942e. No importa el productor. Es la versión local corregida antes de leer el resultado, sin cambios hoy.

Máquina científica: Actions x64, ubuntu-24.04, imagen 20261026.354.1, 4 CPU, Python 3.12.14; numpy 2.5.3, pandas 3.0.5, pyarrow 25.0.1 y scipy 1.18.1. Tiempo total del instrumento original, incluidos humo y reproducción estricta: 651,363361894 s, unos 10 min 51 s; RSS máximo 3.065.244 KiB = 2,923244476 GiB. No son costos de G1 ni mediciones de hoy.

Verificación de hoy: Python 3.12.14 en brain-env, sólo biblioteca estándar sobre JSON y log. GitHub API pública para lecturas; integración GitHub y ClickUp para publicar. El mantenimiento documental usa el workflow ya existente, sin permisos nuevos, y no invoca el instrumento científico. Sin instalaciones, GPU, Kaggle, nuevos sorteos, merge ni modificación de las ramas experimentales.

## 4. Evidencia cruda de la verificación de hoy

La salida completa del verificador está a continuación. Su parser excluye las 400 líneas NULL de fixtures sintéticos anteriores al primer LOAD_FULL, y exige dos segmentos reales. Sin esa corrección previa habría mezclado fixtures con datos reales.

```text
COMMAND ['/usr/local/bin/python3', 'verificar_cierre.py', '--json', 'cierre.json', '--log', 'run-41330973057.log', '--strict', 'estricto.json']
NEGATIVE_REJECTED missing_draw incomplete plan
NEGATIVE_REJECTED changed_holm Holm mismatch
NEGATIVE_REJECTED wrong_source source or seal mismatch
NEGATIVE_REJECTED sign_guard_off_in_json_and_log guard
NEGATIVE_REJECTED denominator_changed_in_json_and_log denominator changed
NEGATIVE_REJECTED repro_tampered repro status mismatch
RAW_JSON_SHA256 a5c689d4153a9f4fcfadc573cac58521f1ade330b82d1d122dfae6f15c41aceb BYTES 371287
RAW_LOG_SHA256 6203f6035de2a3d9c1165e56a4066da79ee714065575cf05810a931e1cdc6b7f BYTES 422115
STRICT_JSON_SHA256 ffce074c422835b426c717902e0510d6bcdd130ecff45d9fccce25e182a89282 BYTES 307449
RECOMPUTED {"banc": {"exceed": [0, 0], "first_order": {"cierre_0": {"S_row_share": 0.323096, "S_rows": 763874, "S_to_X_rows": 246805, "S_weight_share": 0.377473, "all_row_share": 0.36921}, "cierre_199": {"S_row_share": 0.323096, "S_rows": 763874, "S_to_X_rows": 246805, "S_weight_share": 0.377473, "all_row_share": 0.36921}, "estricto_0": {"S_row_share": 0.27255, "S_rows": 763874, "S_to_X_rows": 208194, "S_weight_share": 0.281823, "all_row_share": 0.36921}, "estricto_199": {"S_row_share": 0.271176, "S_rows": 763874, "S_to_X_rows": 207144, "S_weight_share": 0.282279, "all_row_share": 0.36921}, "real": {"S_row_share": 0.323096, "S_rows": 763874, "S_to_X_rows": 246805, "S_weight_share": 0.377473, "all_row_share": 0.36921}}, "fixed_rows": 17068, "p": ["1/201", "1/201"], "repro": "PASS", "repro_hashes": 200, "repro_seconds": 91.07615184099996, "seconds": 200.29461244700002, "strata": 276, "summary": {"n_cab": {"max": 753, "mean": 753.0, "min": 753}, "n_pares_ffi": {"max": 286, "mean": 263.63, "min": 233}, "n_x": {"max": 346, "mean": 312.035, "min": 274}, "t1": {"max": 0.3798140770252324, "mean": 0.3501062416998672, "min": 0.3094289508632138}, "t2": {"max": 95, "mean": 76.515, "min": 57}}}, "flywire": {"exceed": [0, 0], "first_order": {"cierre_0": {"S_row_share": 0.362476, "S_rows": 1195456, "S_to_X_rows": 433324, "S_weight_share": 0.422257, "all_row_share": 0.363127}, "cierre_199": {"S_row_share": 0.362476, "S_rows": 1195456, "S_to_X_rows": 433324, "S_weight_share": 0.422257, "all_row_share": 0.363127}, "estricto_0": {"S_row_share": 0.298053, "S_rows": 1195456, "S_to_X_rows": 356309, "S_weight_share": 0.311307, "all_row_share": 0.363127}, "estricto_199": {"S_row_share": 0.298561, "S_rows": 1195456, "S_to_X_rows": 356917, "S_weight_share": 0.314791, "all_row_share": 0.363127}, "real": {"S_row_share": 0.362476, "S_rows": 1195456, "S_to_X_rows": 433324, "S_weight_share": 0.422257, "all_row_share": 0.363127}}, "fixed_rows": 21561, "p": ["1/201", "1/201"], "repro": "PASS", "repro_hashes": 200, "repro_seconds": 102.56182087400003, "seconds": 208.921920855, "strata": 145, "summary": {"n_cab": {"max": 996, "mean": 996.0, "min": 996}, "n_pares_ffi": {"max": 524, "mean": 494.62, "min": 457}, "n_x": {"max": 907, "mean": 848.815, "min": 795}, "t1": {"max": 0.5261044176706827, "mean": 0.49660642570281127, "min": 0.45883534136546184}, "t2": {"max": 326, "mean": 286.04, "min": 257}}}, "holm": ["4/201", "4/201", "4/201", "4/201"], "maxrss_gib": 2.9232444763183594, "per_connectome": ["SOSTENIDA", "SOSTENIDA"], "repro": "PASS", "seconds": 651.3633618939999, "verdict": "SOSTENIDA"}
VERIFY_CIERRE_PASS 400/400 nulls; fixed denominators; exact rational p; Holm; verdicts; REPRO; log parity; six negative controls

STDERR

PROCESS_EXIT=0
```

### Descriptivos recalculados por otra vía

```python
import json, math, statistics
from pathlib import Path
r = json.loads(Path("cierre.json").read_text())
for name, c in r["connectomes"].items():
    for k in ("n_cab", "n_pares_ffi", "t1", "t2", "n_x"):
        a = [x[k] for x in c["nulls"]]
        got = {"min": min(a), "max": max(a), "mean": statistics.mean(a)}
        assert all(math.isclose(got[z], c["summary"][k][z], rel_tol=1e-12, abs_tol=1e-14) for z in got)
        print(name, k, json.dumps(got, sort_keys=True))
    assert c["fixed_arrays_unchanged"] and c["nonfrozen"] and c["control"]["passed"]
    assert c["first_order"]["real"] == c["first_order"]["cierre_0"] == c["first_order"]["cierre_199"]
print("SUMMARY_RECOMPUTE_PASS 10/10; fixed arrays; nonfrozen; biological controls; first-order equality")
```

```text
COMMAND ['/usr/local/bin/python3', 'comprobar_resumen.py']
flywire n_cab {"max": 996, "mean": 996, "min": 996}
flywire n_pares_ffi {"max": 524, "mean": 494.62, "min": 457}
flywire t1 {"max": 0.5261044176706827, "mean": 0.49660642570281127, "min": 0.45883534136546184}
flywire t2 {"max": 326, "mean": 286.04, "min": 257}
flywire n_x {"max": 907, "mean": 848.815, "min": 795}
banc n_cab {"max": 753, "mean": 753, "min": 753}
banc n_pares_ffi {"max": 286, "mean": 263.63, "min": 233}
banc t1 {"max": 0.3798140770252324, "mean": 0.3501062416998672, "min": 0.3094289508632138}
banc t2 {"max": 95, "mean": 76.515, "min": 57}
banc n_x {"max": 346, "mean": 312.035, "min": 274}
SUMMARY_RECOMPUTE_PASS 10/10; fixed arrays; nonfrozen; biological controls; first-order equality

STDERR

PROCESS_EXIT=0
```

## 5. Archivos y estado de cierre

Este archivo conserva el resultado, la salida completa del verificador y su fuente exacta como evidencia documental. El código científico y los resultados originales siguen en titan/reuso-cierre-2026-11-01, sin merge. No se publican binarios ni datasets.

El cierre del CONTEXTO se agrega mediante parche anclado al mismo archivo como apéndice B, conservando esta respuesta como prefijo exacto y los 119.028 bytes de historia del contexto. El Doc seleccionado recibe la sección 15 y una cabecera vigente. La publicación se verifica leyendo Git y Doc de vuelta. No se crea un archivo retrodatado 2026-11-01-006.

## 6. NO MEDIDO y alcance del veredicto

G1: sin diseño, implementación, sello ni corrida. Gramática aprendida, función adicional frente a G0, conservación de H_PARES_DATOS por redes generadas, compresión y ahorro de RAM/latencia/energía: NO MEDIDOS. Tampoco se midieron aquí geometría, fuerza entrante, vecinos únicos preservados, sensibilidad a signos desconocidos, causalidad fisiológica o un individuo nuevo no expuesto. BANC ya era conocido; el cierre fue elegido después de observar el estricto.

El signo conservado y el cableado directo fijo no eliminan el exceso bajo este nulo. No se concluye que toda explicación alternativa haya quedado descartada. La selección de pruebas y la interpretación provienen de la misma instancia que implementó el ensayo; no es auditoría independiente. La verificación del recibo no equivale a una nueva reproducción desde las entradas anatómicas.

Afirmación «el recibo y su inferencia son consistentes» → verificador separado y seis corrupciones → podía dar rojo y las rechazó → PASS. Afirmación «el motivo aporta función o ahorro» → no hubo instrumento de esa propiedad → NO MEDIDO.

--- METODO PROMETEO ---
Accion delicada: NO en la lectura/verificación; SI en el mantenimiento del workflow documental existente, detallado en el apéndice B.
Modo aplicado: LIGERO para verificar el recibo; FULL para el mantenimiento documental.
Maquina: brain-env para recomputo; Actions x64 sólo para el cierre documental. El experimento original no se relanza.
Rubrica de la verificación: N/A, lectura y recomputo acotados. No se recicla el score de 005.
Review externo: no realizado; independencia de selección e interpretación no demostrada.
Instrumento: verificar_cierre.py, exit 0; comprobar_resumen.py, exit 0; fuentes y salidas completas en este archivo.
Artefactos: docs/agents/respuestas/2026-11-02-001-reuso-cierre-verificado-sin-relanzar.md + https://app.clickup.com/90171457413/docs/2kza6fw5-26157

## Apéndice A. Fuente exacta del verificador ejecutado

Se conserva como evidencia en este documento, no como cambio del productor ni como script de producción en main. Guardar el contenido del bloque como verificar_cierre.py conserva el SHA256 indicado; los archivos de entrada se descargan desde los commits fijados arriba y el JSON estricto desde 6db5d089efa71199f775d1b6619b1cf9f790b7fe.

```python
#!/usr/bin/env python3
"""tools/reuso/verificar_cierre.py: recompute H_REUSO_CIERRE inference from the raw receipt.

It does not import the producer. It reads cierre.json, the runner log and the
pinned strict receipt; checks plan, guards, fixed denominators, exact rational p
values, Holm, verdicts, REPRO_ESTRICTO and full JSON/log parity; then proves
that six corrupted receipts are rejected for the expected reason.
Run: python verificar_cierre.py --json cierre.json --log run.log --strict estricto.json
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import math
from fractions import Fraction
from pathlib import Path
from typing import Any

SOURCE_SHA256 = "db27c17b31e5bceb4a237f1e86ccfb30a57b19ad3a6e9a70e4a25232faf56783"
SEAL_BLOB = "bd03205cbfc98187d9f2e7aad31dde0b25212c06"
SEAL_COMMIT = "a2bf422253b42bfc4215018c01b22c7f9113d426"
ESTRICTO_BLOB = "502b2ee90f90606224a43611bd0c6f4f3b35949c"
STRICT_SHA256 = "ffce074c422835b426c717902e0510d6bcdd130ecff45d9fccce25e182a89282"
EXPECTED = {"flywire": (996, 880, 698, 1118, 22029), "banc": (753, 622, 419, 716, 22030)}
INPUT_PINS = {
    "connectivity.parquet": (100804642, "3d802fd542b5d18570ba1ba0bb0abed9", "efeb23fb99098e9c390f6869969b2a121a2ee92c833cfc45ecb2c1d8e1af0347"),
    "annotations.tsv": (31718505, "719904abad876c68ace1b5690c9b9b63", "9a4f8b2f843196074431ebd7cd883536afa1be86c8a4ce90970441e8be81d1be"),
    "banc_888_meta.feather": (57503026, "8c2b93a608c7163ec9d94d68e0756ff4", "86ccf5df0c67419f8c5f43e93a7ed38d23a080e9f7fde26737290252f3780098"),
    "banc_888_edgelist_simple_v3.feather": (359161658, "08542b0771db7418ed474be60dc9886c", "8c296e946f3c69a8c7222f30ad75fa8a98eeb189124fec6df829c9125f4be64b"),
}
GUARD_KEYS = ("index", "sd_fixed", "target_class", "target_side", "target_sign", "target_role", "incoming_by_pre_side", "mixing")
STAT_KEYS = ("n_cab", "n_pares_ffi", "t1", "t2", "n_x")
ALPHA = Fraction(1, 20)
N = 200


def require(condition: bool, message: str) -> None:
    """Raise a ValueError with a stable reason when a check fails."""
    if not condition:
        raise ValueError(message)


def holm(ps: list[Fraction]) -> list[Fraction]:
    """Exact Holm step-down adjustment on rational p values."""
    order = sorted(range(len(ps)), key=lambda i: ps[i])
    adjusted, running = [Fraction(0)] * len(ps), Fraction(0)
    for rank, i in enumerate(order):
        running = max(running, min(Fraction(1), (len(ps) - rank) * ps[i]))
        adjusted[i] = running
    return adjusted


def per_connectome(raw: list[Fraction], adjusted: list[Fraction]) -> str:
    """Original decision rule for one connectome."""
    if all(p < ALPHA for p in adjusted):
        return "SOSTENIDA"
    if all(p >= ALPHA for p in raw):
        return "REFUTADA"
    return "PARCIAL"


def final(fw: str, banc: str) -> str:
    """Original combined rule over FlyWire and BANC."""
    if fw == "SOSTENIDA" and banc == "SOSTENIDA":
        return "SOSTENIDA"
    if fw == "REFUTADA":
        return "REFUTADA"
    if fw == "SOSTENIDA" and banc == "REFUTADA":
        return "NO_SE_REPLICA"
    return "SIN_DECIDIR"


def log_rows(text: str) -> dict[str, list[dict[str, Any]]]:
    """Parse NULL lines of the real full run only (from the first LOAD_FULL line).

    The workflow first runs synthetic end-to-end fixtures that also print NULL
    lines labelled flywire; counting them would break JSON/log parity falsely.
    """
    lines = text.splitlines()
    starts = [i for i, line in enumerate(lines) if line.startswith("LOAD_FULL ")]
    require(len(starts) == len(EXPECTED), "real segment not identifiable")
    rows: dict[str, list[dict[str, Any]]] = {name: [] for name in EXPECTED}
    for line in lines[starts[0]:]:
        if line.startswith("NULL "):
            row = json.loads(line[5:])
            rows[row.pop("connectome")].append(row)
    return rows


def share(block: dict[str, Any]) -> dict[str, Any]:
    """Fractions of rows and weight that eligible S send to candidate X."""
    return dict(S_to_X_rows=block["S_to_X_rows"], S_rows=block["S_rows"],
                S_row_share=round(block["S_to_X_rows"] / block["S_rows"], 6),
                S_weight_share=round(block["S_to_X_weight"] / block["S_weight"], 6),
                all_row_share=round(block["all_to_X_rows"] / block["all_rows"], 6))


def verify(result: dict[str, Any], text: str, strict: dict[str, Any]) -> dict[str, Any]:
    """Recompute every inferential quantity and compare it with the receipt."""
    env = result["environment"]
    require(result["status"] == "VALID" and result["mode"] == "full" and result["exit_code"] == 0, "status")
    require(env["source_sha256"] == SOURCE_SHA256 and env["seal_blob"] == SEAL_BLOB and env["seal_commit"] == SEAL_COMMIT
            and env["estricto_blob"] == ESTRICTO_BLOB and env["strict_json_sha256"] == STRICT_SHA256, "source or seal mismatch")
    require(result["selftest"]["passed"] == result["selftest"]["total"] == 28, "selftest")
    require(set(result["inputs"]) == set(INPUT_PINS), "input population mismatch")
    for name, expected in INPUT_PINS.items():
        got = result["inputs"][name]
        require((got["bytes"], got["md5"], got["sha256"]) == expected, "input pin " + name)
    raw = log_rows(text)
    out: dict[str, Any] = {}
    ps: list[Fraction] = []
    for name, (nc, nf, t2, nx, seed) in EXPECTED.items():
        c = result["connectomes"][name]
        obs = c["observed"]
        require((obs["n_cab"], obs["n_pares_ffi"], obs["t2"], obs["n_x"]) == (nc, nf, t2, nx) and obs["t1"] == nf / nc,
                "observed baseline " + name)
        nulls = c["nulls"]
        require(c["seed"] == seed and c["count_expected"] == N and len(nulls) == N
                and [r["draw"] for r in nulls] == list(range(N)), "incomplete plan")
        require(len({r["targets_sha256"] for r in nulls}) == N, "duplicate draw")
        require(nulls == raw[name], "JSON and verbatim log disagree")
        for r in nulls:
            g = r["guard"]
            require(g["ok"] is True and all(g["checks"][k] is True for k in GUARD_KEYS), "guard")
            require(set(g["moved"]) == {"movable", "SX", "XD"} and all(v > 0.5 for v in g["moved"].values()), "mixing")
            require(r["n_cab"] == nc, "denominator changed")
            require(r["t1"] == r["n_pares_ffi"] / r["n_cab"], "t1 identity")
        for k in (0, N - 1):
            require(nulls[k]["guard"].get("budget_recomputed") is True and nulls[k]["guard"].get("sparse_parity") is True,
                    "budget or parity flag")
        require(any(r["t1"] != obs["t1"] for r in nulls) and any(r["t2"] != obs["t2"] for r in nulls), "frozen statistic")
        exceed = [sum(r["n_pares_ffi"] >= nf for r in nulls), sum(r["t2"] >= t2 for r in nulls)]
        p = [Fraction(1 + e, N + 1) for e in exceed]
        require([float(x) for x in p] == c["p"], "p mismatch")
        ps += p
        rep = result["repro_estricto"][name]
        sref = strict["connectomes"][name]["nulls"]
        published_ok = all(rep["stats"][str(k)]["published"] == {key: sref[k][key] for key in STAT_KEYS} for k in (0, N - 1))
        computed_ok = all(rep["stats"][str(k)]["historical"] == rep["stats"][str(k)]["published"]
                          and rep["stats"][str(k)]["sparse"] == rep["stats"][str(k)]["published"] for k in (0, N - 1))
        repro_pass = rep["hashes_equal"] == rep["hashes_total"] == N and published_ok and computed_ok
        require((rep["status"] == "PASS") == repro_pass, "repro status mismatch")
        order = c["first_order"]
        out[name] = dict(exceed=exceed, p=[str(x) for x in p], summary=c["summary"], strata=c["strata"], fixed_rows=c["fixed_rows"],
                         repro=rep["status"], repro_hashes=rep["hashes_equal"],
                         first_order=dict(real=share(order["real"]), cierre_0=share(order["cierre_0"]),
                                          cierre_199=share(order["cierre_199"]),
                                          estricto_0=share(rep["first_order"]["estricto_0"]),
                                          estricto_199=share(rep["first_order"]["estricto_199"])),
                         seconds=c["seconds"], repro_seconds=rep["seconds"])
    adjusted = holm(ps)
    require(all(math.isclose(float(a), b, rel_tol=1e-12, abs_tol=0.0) for a, b in zip(adjusted, result["holm"])), "Holm mismatch")
    vf, vb = per_connectome(ps[:2], adjusted[:2]), per_connectome(ps[2:], adjusted[2:])
    require(vf == result["H_REUSO_CIERRE_FLYWIRE"] and vb == result["H_REUSO_CIERRE_BANC"]
            and final(vf, vb) == result["H_REUSO_CIERRE"], "verdict mismatch")
    repro = "PASS" if all(out[name]["repro"] == "PASS" for name in EXPECTED) else "FAIL"
    require(repro == result["REPRO_ESTRICTO"], "repro verdict mismatch")
    out.update(holm=[str(x) for x in adjusted], per_connectome=[vf, vb], verdict=final(vf, vb), repro=repro,
               seconds=result["seconds"], maxrss_gib=result["maxrss_kib"] / (1024 ** 2))
    return out


def relog(text: str, name: str, old: dict[str, Any], new: dict[str, Any]) -> str:
    """Rewrite one NULL line exactly as the producer would have printed the changed row."""
    def line(row: dict[str, Any]) -> str:
        return "NULL " + json.dumps(dict(connectome=name, **row), ensure_ascii=False, sort_keys=True, allow_nan=False)
    require(text.count(line(old)) == 1, "log line for mutation not unique")
    return text.replace(line(old), line(new), 1)


def main() -> int:
    """Verify the real receipt, then require six corrupted receipts to be rejected."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", type=Path, required=True)
    parser.add_argument("--log", type=Path, required=True)
    parser.add_argument("--strict", type=Path, required=True)
    args = parser.parse_args()
    jb, lb, sb = args.json.read_bytes(), args.log.read_bytes(), args.strict.read_bytes()
    require(hashlib.sha256(sb).hexdigest() == STRICT_SHA256, "strict receipt pin mismatch")
    result, text, strict = json.loads(jb), lb.decode(), json.loads(sb)
    require("MUTATION_PROCESS_EXIT 3" in text and '"name": "closure_guards_39", "ok": false' in text, "workflow mutation evidence missing")
    require("E2E_POSITIVE_AND_NEGATIVE_PASS" in text and 'CIERRE_TEST_SUMMARY {"passed": 28, "total": 28}' in text, "workflow tests missing")
    out = verify(result, text, strict)
    cases = {}
    broken = copy.deepcopy(result); broken["connectomes"]["flywire"]["nulls"].pop(); cases["missing_draw"] = (broken, text, "incomplete plan")
    broken = copy.deepcopy(result); broken["holm"][0] = 0.75; cases["changed_holm"] = (broken, text, "Holm mismatch")
    broken = copy.deepcopy(result); broken["environment"]["source_sha256"] = "changed"; cases["wrong_source"] = (broken, text, "source or seal mismatch")
    broken = copy.deepcopy(result); row = broken["connectomes"]["banc"]["nulls"][0]; old = copy.deepcopy(row); row["guard"]["checks"]["target_sign"] = False
    cases["sign_guard_off_in_json_and_log"] = (broken, relog(text, "banc", old, row), "guard")
    broken = copy.deepcopy(result); row = broken["connectomes"]["flywire"]["nulls"][5]; old = copy.deepcopy(row); row["n_cab"] += 1
    cases["denominator_changed_in_json_and_log"] = (broken, relog(text, "flywire", old, row), "denominator changed")
    broken = copy.deepcopy(result); broken["repro_estricto"]["flywire"]["hashes_equal"] -= 1; cases["repro_tampered"] = (broken, text, "repro status mismatch")
    for name, (data, log_text, reason) in cases.items():
        try:
            verify(data, log_text, strict)
        except ValueError as exc:
            require(str(exc) == reason, name + ": wrong rejection: " + str(exc))
            print("NEGATIVE_REJECTED", name, str(exc))
        else:
            raise AssertionError("verifier accepted " + name)
    print("RAW_JSON_SHA256", hashlib.sha256(jb).hexdigest(), "BYTES", len(jb))
    print("RAW_LOG_SHA256", hashlib.sha256(lb).hexdigest(), "BYTES", len(lb))
    print("STRICT_JSON_SHA256", hashlib.sha256(sb).hexdigest(), "BYTES", len(sb))
    print("RECOMPUTED", json.dumps(out, ensure_ascii=False, sort_keys=True))
    print("VERIFY_CIERRE_PASS 400/400 nulls; fixed denominators; exact rational p; Holm; verdicts; REPRO; log parity; six negative controls")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

## Apéndice B. Cierre anclado del estado, sin relanzar ciencia

Cinco anclas, doce negativos rechazados, cola histórica intacta. El parche cambia sólo CONTEXTO y agrega este recibo. No modifica el productor ni su workflow, ni ejecuta nuevos nulos. La fuente del verificador queda íntegra como evidencia en el apéndice A.

Instrumento documental: https://github.com/gatehot59-star/drosophila-fep-connectome/blob/e11eccbad05862f4fc15aa09a1b603311b39297e/.github/workflows/contexto-topo-2026-11-01.yml

Run documental (no científico): https://github.com/gatehot59-star/drosophila-fep-connectome/actions/runs/41406011780

Comando: Python embebido en el workflow, CONTEXTO_MODE=apply. Salida completa:

```text
source_blob=f3bbbc2ecf9a3f6d05f5dbc84058201d5ecfdf2c
source_bytes=126524
response_prefix_blob=f4e4beafb7bfc0a49e03ae929d129545712f0b26
response_prefix_bytes=28653
verifier_embedded_bytes=12426
verifier_embedded_pin=PASS
positive_transform=PASS
anchor_1_count=1
missing_anchor_1=REJECTED anchor_1: expected 1, got 0
duplicate_anchor_1=REJECTED anchor_1: expected 1, got 2
anchor_2_count=1
missing_anchor_2=REJECTED anchor_2: expected 1, got 0
duplicate_anchor_2=REJECTED anchor_2: expected 1, got 2
anchor_3_count=1
missing_anchor_3=REJECTED anchor_3: expected 1, got 0
duplicate_anchor_3=REJECTED anchor_3: expected 1, got 2
anchor_4_count=1
missing_anchor_4=REJECTED anchor_4: expected 1, got 0
duplicate_anchor_4=REJECTED anchor_4: expected 1, got 2
anchor_5_count=1
missing_anchor_5=REJECTED anchor_5: expected 1, got 0
duplicate_anchor_5=REJECTED anchor_5: expected 1, got 2
source_drift=REJECTED source drift
repeat_application=REJECTED anchor_4: expected 1, got 0
negative_controls=12/12
historical_tail_bytes=119028
historical_tail_sha256=b6c9d0cf10d6dd0b4bb6f9abd6e39c4ac1891bf7c101f169cef4f38ca5b31fb5
historical_tail_unchanged=True
reverse_roundtrip=PASS
result_blob=438a4bf8e448b3ca771a13683ecdf61d96f471ce
result_bytes=128279
result_sha256=ea44b0bae4845bfeccfc9b09793f15465503da2a938c34f0d7a8d259b083b7ed
target_readback_equal=True
response_prefix_preserved=True
```

QA previo del mantenimiento: 57/60 = 95/100. Completitud 15/15: payload íntegro y sólo dos rutas; ejecutabilidad 14/15: programa y negativos probados, runner pendiente al puntuar; seguridad 14/15: mismo disparador y permiso, checkout fijado, pines y push sin force, sin auditoría exhaustiva de cadena de suministro; documentación 10/10: contrato, límites, código y salida cruda; proceso 4/5: instrumentos falsables, selección/interpretación no independientes. N/A 40 puntos de producto (testing de aplicación, arquitectura, DevOps e innovación): es mantenimiento documental, no producto. No es una probabilidad científica.

--- METODO PROMETEO ---
Accion delicada: SI, mantenimiento del workflow documental existente, sin permisos nuevos.
Modo aplicado: FULL.
Maquina: brain-env para preflight; Actions x64 para publicar documentación.
Rubrica previa: 57/60 = 95/100; N/A 40 puntos de producto.
Review externo: no realizado.
Instrumento: parche anclado, 12 negativos; evidencia cruda arriba. No se reejecuta H_REUSO_CIERRE.
Artefactos: docs/agents/respuestas/2026-11-02-001-reuso-cierre-verificado-sin-relanzar.md + https://app.clickup.com/90171457413/docs/2kza6fw5-26157

### Incidencias documentales, sin efecto científico

El primer lanzador del preflight omitió importar sys; se corrigió antes de probar. Después, el primer push del workflow incorporó tres errores de transcripción en el bloque comprimido: 30.218 bytes publicados frente a 30.215 probados. El run documental 41391345653 falló antes de escribir: main siguió en d866c2da6de71f404738b059a18014599a9d5c4a. No se alteró el recibo científico ni se relanzó su ejecución.

La recuperación lee aquel commit inmutable, exige su SHA256, repara exactamente las tres diferencias y exige el SHA256 90d9f86180bcfbb332065677c2a0b78a37ba2c7c7ee901bd9c3539c16611b157 del workflow que pasó el preflight. Sólo entonces ejecuta su bloque documental, que a su vez exige las huellas del recibo, del verificador y del CONTEXTO. No se debilita ninguna guarda. Se preservan el prefijo de la respuesta y la historia del contexto.
