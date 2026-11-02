# 2026-11-02-006 · H_MECANISMO_DNp04: SOSTENIDA_EN_MODELO

**Veredicto del pedido.** Sellado antes del instrumento, corrido en Actions y verificado con un instrumento propio que no importa al agregador: **SOSTENIDA_EN_MODELO**. Con LC4 derecho, cortar solo la fila DNp04→PVLP010 (1 fila, 190 sinapsis) sube D' (los descendentes sin DNp04) de 266,15 a 368,60 espigas por ensayo: r_Q1 = 0,4056 del freno entero de X. Silenciar PVLP010 la sube a 454,50 (r_Q2 = 0,7456). PVLP010 alimentado solo por DNp04 conserva el 96,8 % de sus espigas (s4 = 0,9677). Es causalidad del modelo de Shiu, no de la mosca.

Doc: https://app.clickup.com/90171457413/docs/2kza6fw5-26157/2kza6fw5-29357 (página 2026-11-02-006 del Doc Topo inverso, creada después del commit `2bacc94`, a pedido).

## 1. Pedido

«Sellá y corré H_MECANISMO_DNp04» (2-nov-2026, 12:54 ART).

## 2. Herramientas declaradas

- brain-env (gateway python): lectura de lo commiteado, prueba local, huellas y verificador propio. Escribió solo bajo /workspace/dnp04.
- GitHub MCP push_files: en titan/mecanismo-dnp04-2026-11-02, `db369ad` (HUELLAS.sha256, prueba endurecida y PROBAR) y `2f991c3` (CORRER). En main, este archivo.
- GitHub Actions, repo público, sin cuota: mecanismo-dnp04-prueba run 41480897832 (success) y mecanismo-dnp04-correr run 41481727412 (8 celdas y agregar, success, 16:27:56 a 16:40:35 UTC). El workflow preexistente «H4 integrated regression» corrió solo sobre `db369ad` (run 41480897332, success).
- API pública de GitHub sin autenticar para runs y jobs, y raw.githubusercontent para leer archivos.

## 3. Qué se midió

Modelo LIF de Shiu sin cambios (philshiu@91bdd1e7, Brian2 2.10.1), FlyWire 783 entero, Poisson a 50 Hz sobre S, 20 ensayos de 1 s con semillas 20261102 + t, las mismas de la corrida 2. Silenciar es poner peso 0 en las salidas: la neurona silenciada sigue contando sus propias espigas.

**LC4 derecho** (ΔX' = 252,60):

| Condición | D' | r | PVLP010 | DNp04 |
|---|---|---|---|---|
| C0 intacto | 266,15 | | 106,70 | 107,30 |
| C1 silenciar X | 518,75 | 1 | 109,10 | 109,40 |
| Q1 cortar DNp04→PVLP010 | 368,60 | 0,4056 | 46,35 | 107,60 |
| Q2 silenciar PVLP010 | 454,50 | 0,7456 | 106,95 | 107,40 |
| Q3 silenciar DNp04 | 308,50 | 0,1677 | 42,55 | 110,15 |
| Q4 PVLP010 recibe solo de DNp04 | 272,80 | 0,0263 | 103,25 | 107,80 |
| Q5 silenciar LHAD1g1 | 269,00 | 0,0113 | 106,50 | 107,05 |
| Q6 silenciar AVLP080 | 272,40 | 0,0247 | 106,70 | 107,35 |

**Otros estímulos.** LPLC2 (ΔX' = 663,30): r_Q1 0,1122, r_Q2 0,2488, r_Q3 0,1188, r_Q4 −0,0222, r_Q5 0,2078, r_Q6 0,0261; PVLP010 baja de 79,25 a 35,15 con Q1. LPLC1 (ΔX' = 192,60): r_Q2 0,4839, r_Q4 0,4839 (PVLP010 queda en 0 sin sus otras entradas, porque DNp04 no dispara), r_Q5 0,0877, r_Q6 0,3297; Q1 y Q3 idénticos a C0. LPLC4: Q1 a Q4 idénticos a C0; r_Q5 −0,0047 y r_Q6 −0,0037.

**Pruebas primarias.** P1 (LC4, Q1) +102,45; P2 (LPLC2, Q1) +74,45; P3 (LC4, Q2) +188,35; P4 (LC4, Q3) +42,35. Las cuatro con 20 de 20 ensayos positivos, p exacta 1,91e-06 y Holm 7,63e-06.

**Guardas.** G1 a G5 verdaderas: C0 y C1 iguales a la corrida 2 ensayo por ensayo en los cuatro estímulos; mitades iguales; filas 1 / 937 / 505 / 1.184 / 1.243 / 1.677 con peso 190 en Q1; los 6 controles técnicos idénticos a C0; techo y piso.

**Proxy lineal: PROXY_PARCIAL, 4 de 7.** Acierta PVLP010 con LC4 (0,729 predicho, 0,7456 medido), PVLP010 con LPLC2 (0,194 y 0,2488), LHAD1g1 con LC4 (0,022 y 0,0113) y LHAD1g1 con LPLC2 (0,308 y 0,2078). Falla PVLP010 con LPLC1 (0,217 y 0,4839), AVLP080 con LPLC2 (0,201 y 0,0261) y AVLP080 con LPLC1 (0,624 y 0,3297).

**Descriptivos.** r_Q3 − r_Q1 = −0,2379; D'_Q4 / D'_C0 = 1,0250 con LC4.

**Apuestas selladas: 6 de 8 ganadas, Brier 0,113.**

| Apuesta | p | Resultado |
|---|---|---|
| 1. P1 pasa | 0,85 | ganada |
| 2. r_Q1 ≥ 0,25 | 0,65 | ganada (0,406; estimé 0,45) |
| 3. SOSTENIDA_EN_MODELO | 0,5 | ganada |
| 4. s4 ≥ 0,8 | 0,85 | ganada (0,968) |
| 5. r_Q2 ≥ 0,5 | 0,6 | ganada (0,746) |
| 6. abs(r_Q3 − r_Q1) ≤ 0,10 | 0,35 | perdida (−0,238; r_Q3 menor, como esperaba) |
| 7. PROXY_UTIL | 0,45 | perdida (4 de 7) |
| 8. G4 pasa | 0,95 | ganada |

**Lectura, con etiqueta.**

- MEDIDO modelo: con LC4, una sola fila sináptica entre dos neuronas (DNp04→PVLP010) lleva el 40,6 % del freno entero de X sobre los demás descendentes. PVLP010 completo lleva el 74,6 %, y el proxy lo había predicho (72,9 %).
- MEDIDO modelo: DNp04 alcanza para encender a PVLP010 (s4 0,97, y D' no cambia en Q4). No es la única fuente: sin DNp04, PVLP010 todavía dispara 46,35 por segundo con sus otras entradas. Por eso r_Q1 queda debajo de r_Q2.
- MEDIDO modelo: silenciar DNp04 suelta menos freno (0,168) que cortar solo su sinapsis sobre PVLP010 (0,406), porque DNp04 también excita directo a D'. El mismo descendente excita a sus vecinos y los frena a través de PVLP010: inhibición recurrente entre descendentes, el mecanismo M6 que la respuesta 004 sugería post hoc.
- MEDIDO modelo: el proxy de espigas por sinapsis sirve donde un relevo domina (LC4) y falla donde el freno se reparte (LPLC1, y AVLP080 con LPLC2). La anatomía con tasas no alcanza para atribuir causa en esos casos.
- NO MEDIDO: la mosca, la función y la formación.

## 4. Evidencia cruda verbatim

Resultado de la corrida (results/mecanismo_dnp04_2026-11-02/actions_correr/RESULTADO.txt en titan/mecanismo-dnp04-2026-11-02):

```
medir=success fuente=2f991c3c5a733c9affceb2b0b0c3ecdc62e57c66 run=41481727412
```

MD5SUMS.txt lista 27 archivos; los 27 bajados a brain-env coinciden (md5_mal 0).

agregar_stdout.log, sin las líneas NOMBRES y GUARDAS por estímulo, que están completas en el archivo de la rama:

```
== agregar_dnp04.py :: H_MECANISMO_DNp04 (2026-11-02-006) ==
ESTIMULO LC4 dXprima=252.60 Dprima={"C0": 266.15, "C1": 518.75, "Q1": 368.6, "Q2": 454.5, "Q3": 308.5, "Q4": 272.8, "Q5": 269.0, "Q6": 272.4} r={"Q1": 0.4056, "Q2": 0.7456, "Q3": 0.1677, "Q4": 0.0263, "Q5": 0.0113, "Q6": 0.0247} s4=0.9677 DprimaQ4/DprimaC0=1.0250
ESTIMULO LPLC2 dXprima=663.30 Dprima={"C0": 505.55, "C1": 1168.85, "Q1": 580.0, "Q2": 670.55, "Q3": 584.35, "Q4": 490.85, "Q5": 643.4, "Q6": 522.85} r={"Q1": 0.1122, "Q2": 0.2488, "Q3": 0.1188, "Q4": -0.0222, "Q5": 0.2078, "Q6": 0.0261} s4=1.0852 DprimaQ4/DprimaC0=0.9709
ESTIMULO LPLC1 dXprima=192.60 Dprima={"C0": 81.3, "C1": 273.9, "Q1": 81.3, "Q2": 174.5, "Q3": 81.3, "Q4": 174.5, "Q5": 98.2, "Q6": 144.8} r={"Q1": 0.0, "Q2": 0.4839, "Q3": 0.0, "Q4": 0.4839, "Q5": 0.0877, "Q6": 0.3297} s4=0.0000 DprimaQ4/DprimaC0=2.1464
ESTIMULO LPLC4 dXprima=503.95 Dprima={"C0": 1258.25, "C1": 1762.2, "Q1": 1258.25, "Q2": 1258.25, "Q3": 1258.25, "Q4": 1258.25, "Q5": 1255.9, "Q6": 1256.4} r={"Q1": 0.0, "Q2": 0.0, "Q3": 0.0, "Q4": 0.0, "Q5": -0.0047, "Q6": -0.0037} s4=nan DprimaQ4/DprimaC0=1.0000
PRUEBA P1 LC4 Q1 media_dif=102.45 positivos=20/20 negativos=0 p=1.91e-06 p_holm=7.63e-06 pasa=True
PRUEBA P2 LPLC2 Q1 media_dif=74.45 positivos=20/20 negativos=0 p=1.91e-06 p_holm=7.63e-06 pasa=True
PRUEBA P3 LC4 Q2 media_dif=188.35 positivos=20/20 negativos=0 p=1.91e-06 p_holm=7.63e-06 pasa=True
PRUEBA P4 LC4 Q3 media_dif=42.35 positivos=20/20 negativos=0 p=1.91e-06 p_holm=7.63e-06 pasa=True
PROXY PVLP010_LC4 predicho=0.729 medido=0.7456 pasa=True
PROXY PVLP010_LPLC2 predicho=0.194 medido=0.2488 pasa=True
PROXY PVLP010_LPLC1 predicho=0.217 medido=0.4839 pasa=False
PROXY LHAD1g1_LC4 predicho=0.022 medido=0.0113 pasa=True
PROXY LHAD1g1_LPLC2 predicho=0.308 medido=0.2078 pasa=True
PROXY AVLP080_LPLC2 predicho=0.201 medido=0.0261 pasa=False
PROXY AVLP080_LPLC1 predicho=0.624 medido=0.3297 pasa=False
PROXY_FUERA_DE_X {"PVLP010_LPLC4": 0.0, "LHAD1g1_LPLC1": 0.0877, "LHAD1g1_LPLC4": -0.0047, "AVLP080_LC4": 0.0247, "AVLP080_LPLC4": -0.0037}
PROXY_VEREDICTO PROXY_PARCIAL 4/7
DESCRIPTIVOS LC4 r_Q3-r_Q1=-0.2379 DprimaQ4/DprimaC0=1.0250
GUARDAS_GLOBALES {"G1": true, "G2": true, "G3": true, "G4": true, "G5": true}
H_MECANISMO_DNp04 SOSTENIDA_EN_MODELO r_Q1=0.4056 r_Q2=0.7456 s4=0.9677
EXIT_AGREGAR=0
```

Verificador propio (verificar_dnp04.py, brain-env, exit 0). Reconstruye D' desde las cuentas por neurona y calcula la p exacta por convolución entera, otro algoritmo que la enumeración del agregador. Antes de la corrida dio el veredicto esperado en los 11 casos plantados y la misma p que el agregador en 12 vectores al azar (diferencia máxima 0).

```
PRUEBA P1 LC4 Q1 media=102.45 pos=20 neg=0 p=1.90735e-06 p_holm=7.62939e-06 pasa=True
PRUEBA P2 LPLC2 Q1 media=74.45 pos=20 neg=0 p=1.90735e-06 p_holm=7.62939e-06 pasa=True
PRUEBA P3 LC4 Q2 media=188.35 pos=20 neg=0 p=1.90735e-06 p_holm=7.62939e-06 pasa=True
PRUEBA P4 LC4 Q3 media=42.35 pos=20 neg=0 p=1.90735e-06 p_holm=7.62939e-06 pasa=True
ESTRUCTURA {"LC4": true, "LPLC1": true, "LPLC2": true, "LPLC4": true}
GUARDAS_PROPIAS {"G1": true, "G2": true, "G3": true, "G4": true, "G5": true}
COMPARA_AGREGADO {"global": true, "guardas": true, "p": true, "proxy": true, "r": true, "s4": true} todo_igual=True
PROXY_PROPIO PROXY_PARCIAL 4/7
H_MECANISMO_DNp04_PROPIO SOSTENIDA_EN_MODELO r_Q1=0.4056 r_Q2=0.7456 s4=0.9677
```

Prueba previa en Actions (results/mecanismo_dnp04_2026-11-02/prueba/prueba.log, fuente `db369ad`): las 12 huellas OK, pines de modelo y datos OK, `PRUEBA 44/44 PASS`. Entre los 44: cada guarda rota por separado da INVALIDA con solo esa guarda en falso, y el humo dio C0 y C1 de LC4 idénticos a la corrida 2 y Q2 idéntico a C0 con LPLC4. En brain-env, sin humo: `PRUEBA 38/38 PASS`.

## 5. Archivos generados

En titan/mecanismo-dnp04-2026-11-02, sin merge:

- `40969fb` tools/mecanismo/dnp04/SELLO-DNP04-2026-11-02.md (sha256 3ea514fa…), antes del código.
- `11881e3` intervenir_dnp04.py (f629adb9…), agregar_dnp04.py (823d2095…), los workflows mecanismo-dnp04-prueba.yml (3454851c…) y mecanismo-dnp04-correr.yml (a08b71a2…).
- `db369ad` prueba_dnp04.py endurecida (820fdd42…, 15.882 bytes), HUELLAS.sha256 (4675bd5e…, 1.433 bytes) y PROBAR. Leídos de vuelta byte a byte.
- `2f991c3` results/mecanismo_dnp04_2026-11-02/CORRER.
- Commits del bot: results/mecanismo_dnp04_2026-11-02/prueba/ (7 archivos) y results/mecanismo_dnp04_2026-11-02/actions_correr/ (27 archivos con MD5SUMS.txt: 8 celdas, 8 logs, 8 versiones, agregado_dnp04.json, agregar_stdout.log y RESULTADO.txt).

En main: este archivo.

## 6. NO MEDIDO y pendiente

- La mosca. Todo lo de arriba es causalidad del modelo.
- La página del Doc no estaba creada en el commit `2bacc94`: se creó después, a pedido, en https://app.clickup.com/90171457413/docs/2kza6fw5-26157/2kza6fw5-29357.
- verificar_dnp04.py (sha256 623f028c0646460bc18b7e01bc07405698f1aa887b3a0d554458910081ab48b7, 12.408 bytes) y su log completo corrieron en brain-env y **todavía no están commiteados**. Las líneas de arriba son verbatim.
- El verificador corrió sin `--parquet`: el recuento propio de filas en el parquet no se hizo en esta lectura. Las filas reales están medidas en la prueba (filas_reales_Q1 a Q6).
- CONTEXTO-drosophila-fep.md no está actualizado con este resultado. Las cinco anclas del parche aparecen una vez cada una en la base 64b5f6f3…. La cabecera del Doc Topo inverso tampoco está actualizada.
- Robustez a peso por sinapsis, tau y umbral; lado izquierdo; BANC; el signo inhibitorio del glutamato de PVLP010 (supuesto del modelo); qué otras entradas sostienen a PVLP010 sin DNp04.
- `nproc` imprimió 1 en versiones.txt porque respeta OMP_NUM_THREADS=1: no mide núcleos. La memoria sí: 15.983 MB.
- Review externo: no pedido; no hay PR.

**Experimento en la mosca que decidiría:** silenciar PVLP010, o bloquear su receptor GluClα en los descendentes, y registrar DNp01 y DNp06 ante looming. Lo mismo con DNp04 silenciado: este resultado predice que liberar a los vecinos de PVLP010 pesa más que perder la excitación de DNp04. No conozco líneas driver publicadas para PVLP010.

## Rúbrica (PROMETEO-QA)

Criterios aplicables: instrumento, workflow y reporte. DevOps N/A (10 puntos, no hay deployment).

| Criterio | Puntos | Evidencia |
|---|---|---|
| Completitud | 12/15 | instrumento, agregador, prueba y workflows completos en `11881e3` y `db369ad`; −3 porque el verificador, el Doc y el CONTEXTO están pendientes |
| Ejecutabilidad | 15/15 | runs 41480897832 y 41481727412 success desde fuentes fijadas por HUELLAS; EXIT_AGREGAR=0 |
| Seguridad | 13/15 | permisos contents: write, sin secretos, checkout y setup-python fijados por SHA; −2 por upload-artifact y download-artifact en @v4 |
| Testing | 13/15 | 44 chequeos que pueden fallar, cada guarda rota por separado, dos p exactas independientes; −2 sin cobertura medida |
| Arquitectura del razonamiento | 9/10 | sello antes del código, exposición declarada, controles técnicos; −1 solo lado derecho |
| Documentación | 8/10 | sello y este archivo; −2 por Doc y CONTEXTO pendientes |
| Innovación | 5/5 | guardas aisladas por caso plantado, p por convolución, prueba del proxy |
| Proceso QA | 5/5 | cada puntaje cita SHA, run o archivo |

Total 80/90 → 89/100: **no llega al umbral de 90**. Lo que falta es ejecutar (Doc, verificador y CONTEXTO), no reescribir.

```
--- METODO PROMETEO ---
Accion delicada: SI (disparo dos workflows de CI)
Modo aplicado:   FULL
Maquina:         Actions x64 ubuntu-24.04 (prueba y corrida) + brain-env (prueba local y verificador)
Rubrica:         80/90 -> 89/100 en 2bacc94; 82/90 -> 91/100 con el Doc (ver Actualizacion)
N/A declarados:  10 (DevOps: no hay deployment)
Review externo:  no pedido (no hay PR; deuda declarada)
Instrumento:     agregar_dnp04.py en run 41481727412, EXIT_AGREGAR=0, evidencia en
                 results/mecanismo_dnp04_2026-11-02/actions_correr/ de titan/mecanismo-dnp04-2026-11-02;
                 verificar_dnp04.py en brain-env, exit 0, todo_igual=True (sin commitear, declarado)
Artefactos:      docs/agents/respuestas/2026-11-02-006-mecanismo-dnp04-sostenida.md + Doc https://app.clickup.com/90171457413/docs/2kza6fw5-26157/2kza6fw5-29357
```

## Actualización · 2-nov-2026 (pedido de las 16:48 ART)

Pedido: «Creá la página del Doc 006». Página creada en el Doc Topo inverso y leída de vuelta completa (banner, cuatro tablas, bloques de evidencia, rúbrica y bloque de método): https://app.clickup.com/90171457413/docs/2kza6fw5-26157/2kza6fw5-29357. Con la página, Completitud pasa a 13/15 y Documentación a 9/10: **82/90 → 91/100**. Siguen pendientes, y NO MEDIDOS: commitear verificar_dnp04.py y su log, el CONTEXTO y la cabecera de la página principal del Doc.
