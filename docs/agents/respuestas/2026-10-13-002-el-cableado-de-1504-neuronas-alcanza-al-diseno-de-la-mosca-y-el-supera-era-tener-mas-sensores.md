# 2026-10-13-002 · El cableado de 1.504 neuronas alcanza al diseño de la mosca; el "supera" sellado era tener más sensores (13-oct, 06:12)

Sigue a la 2026-10-13-001. Corrida: run 38346117181 de Actions x64 (`7534dd2`), resultados commiteados por el bot en `5c4fbac` de `titan/factorial-mosca-2026-10-13`; post-hoc en `19a508c`.

**Veredicto primero.**

- [MEDIDO] **Instrumento VALIDO 9/9.** El ancla reproduce la 015 exacta también en Actions (`REPRODUCE_015 tolerancia=[True x6] exacto=[True x6]`). Los insumos bajados por la fábrica dan los md5 pineados en los 9 trabajos. `MD5SUMS.txt` verifica 19/19 en un clon limpio.
- [MEDIDO] **Veredicto sellado: ALGUN FACTOR CIERRA LA BRECHA (R1_CON_TASA, R1_CON_LIQ, R1_SIN_LIQ).** Con el recorte R1 (1.504 neuronas, cableado con signo), TASA y LIQ le ganan a la regla de 40 entradas en 3 celdas y empatan en 3, sin ninguna peor. M46 pierde con las tres neuronas, igual que en la 015.
- [MEDIDO] **Post-hoc, no sellado, y cambia la lectura.** R1 recibe 418 neuronas sintonizadas con ruido propio; la regla sellada mira solo las 40 de la 015. La misma regla sobre las 418 entradas sube a 0,926-0,930, y contra ella R1_CON_TASA y R1_CON_LIQ **IGUALAN** en las 6 celdas (Holm, ninguna distinta), y R1_SIN_LIQ pierde en A 0,6 ruido 0,45. **El "supera" lo explica tener más sensores.** Las celdas MEJOR eran sobre todo las de ruido 0,45, que es donde promediar sensores paga.
- [MEDIDO] **El cableado sigue pagando dentro de R1.** R1_CON_TASA 0,937 contra 50 SL (media 0,774) y 50 T (media 0,742), p por rango 0,0196 en las dos, el piso con 50. Lo mismo con LIQ (0,938 contra 0,788 y 0,777).
- [MEDIDO] **Factores (McNemar por celda, Holm sobre 6):** recorte M46→R1 **AYUDA** con las tres neuronas (6/6 celdas). Inhibición CON contra SIN **AYUDA**: en TASA y LIQ solo con amplitud 0,6, en LIF en las 6. LIQ contra TASA: **EMPATE** en R1, MIXTO en M46. LIF contra TASA: **DAÑA** en M46 y en R1.
- [CONCLUSIÓN] Tenías razón en el punto que importaba: la brecha de la 015 era nuestro recorte. Con más cableado real, la mosca simulada alcanza a su propio diseño idealizado y le gana a sus barajados. No lo supera. La neurona líquida nativa no agrega nada sobre la tasa, y el LIF, como lo armamos (corriente de entrada fija, paso de 1 ms), empeora.

## Pedido
ClickKit `leer_factorial_002`: leer y firmar el factorial cuando terminara.

## Herramientas y máquina
- Actions x64: run 38346117181, 9 trabajos más el agregado, todos success (04:22 a 05:08 UTC). Duraciones del script: M46 12 a 130 s; R1 502 a 2691,6 s.
- brain-env: clon limpio de la rama, `md5sum -c`, lectura de logs, chequeo post-hoc `tools/factorial/posthoc_regla418.py` (md5 23372f548384ad42c6451bd174e73a1b). En el medio el gateway dio 502 tres veces; esperé y seguí.
- GitHub MCP: post-hoc en la rama (`19a508c`) y este archivo en main.

## Qué se midió
Primaria sellada por configuración (W contra la regla de 40 entradas, 6 celdas) y los 10 contrastes; secundaria descriptiva con nulos; un chequeo post-hoc declarado como tal.

## Evidencia cruda
`results/factorial_2026-10-13/agregado.log` (bot, `5c4fbac`):
```
CONFIG M46_TASA W=0.9005,0.8805,0.9125,0.8915,0.8680,0.8580 regla=0.9195,0.8705,0.9325,0.8935,0.9315,0.9120 H3_holm=EMPATE(0.0757),EMPATE(0.591),PEOR(0.0181),EMPATE(0.856),PEOR(4.69e-14),PEOR(5.38e-09) -> PIERDE
CONFIG M46_LIQ W=0.9170,0.8390,0.9245,0.8480,0.9260,0.8515 ... -> PIERDE
CONFIG M46_LIF W=0.6235,0.6730,0.6235,0.6810,0.6325,0.6975 ... PEOR x6 -> PIERDE
CONFIG R1_CON_TASA W=0.9415,0.9310,0.9370,0.9310,0.9330,0.9270 H3_holm=MEJOR(0.0179),MEJOR(2.04e-10),EMPATE(0.995),MEJOR(1.54e-05),EMPATE(0.995),EMPATE(0.132) -> SUPERA
CONFIG R1_CON_LIQ W=0.9420,0.9260,0.9380,0.9270,0.9390,0.9260 H3_holm=MEJOR(0.0154),MEJOR(1.25e-08),EMPATE(0.421),MEJOR(0.000215),EMPATE(0.421),EMPATE(0.183) -> SUPERA
CONFIG R1_CON_LIF W=0.8815,0.8725,0.8815,0.8720,0.8815,0.8695 ... -> PIERDE
CONFIG R1_SIN_TASA W=0.9335,0.9270,0.9290,0.9230,0.8905,0.8885 ... PEOR en A0.6 -> PIERDE
CONFIG R1_SIN_LIQ W=0.9345,0.9215,0.9385,0.9260,0.9205,0.9080 ... -> SUPERA
CONFIG R1_SIN_LIF W=0.7200,0.7130,0.7200,0.7135,0.7200,0.7135 ... -> PIERDE
NULOS_DESCRIPTIVO R1_CON_TASA W=0.9370 SL media=0.7740 p_sup=0.0196 T media=0.7418 p_sup=0.0196
NULOS_DESCRIPTIVO R1_CON_LIQ W=0.9380 SL media=0.7883 p_sup=0.0196 T media=0.7773 p_sup=0.0196
NULOS_DESCRIPTIVO R1_SIN_LIF W=0.7200 SL media=0.7383 p_sup=0.8571 T media=0.5927 p_sup=0.0476
CONTRASTE RECORTE_TASA -> AYUDA | RECORTE_LIQ -> AYUDA | RECORTE_LIF -> AYUDA
CONTRASTE INHIB_TASA celdas=99/83(0.654),96/88(0.654),66/50(0.654),69/53(0.654),132/47(9.27e-10),128/51(3.98e-08) -> AYUDA
CONTRASTE INHIB_LIQ celdas=...,75/38(0.00384),90/54(0.017) -> AYUDA | INHIB_LIF -> AYUDA
CONTRASTE LIQ_M46 -> MIXTO | LIF_M46 -> DANA | LIQ_R1 -> EMPATE | LIF_R1 -> DANA
DESCRIPTIVO mejor_config_por_media=R1_CON_TASA 0.9334
CHEQUEO INSTRUMENTO_GLOBAL ancla_M46_TASA_valida=True configuraciones_validas=9/9 -> VALIDO
VEREDICTO_GLOBAL -> ALGUN FACTOR CIERRA LA BRECHA (R1_CON_TASA,R1_CON_LIQ,R1_SIN_LIQ)
```
Ancla en Actions (`factorial_M46_TASA.log`): `CHEQUEO REPRODUCE_015 tolerancia=[True, True, True, True, True, True] exacto=[True, True, True, True, True, True] -> True`.
Versiones (9 de 9 iguales): `Linux-6.17.0-1022-azure-x86_64-with-glibc2.39 numpy 2.5.3 pandas 3.0.5 scipy 1.18.1 pyarrow 25.0.1 torch 2.14.1+cpu`; insumos `3d802fd542b5d18570ba1ba0bb0abed9` y `719904abad876c68ace1b5690c9b9b63`.
Post-hoc (`results/factorial_2026-10-13/posthoc_regla418.log`, md5 388a60998961da55baf2e3c0848ccc34):
```
CELDA A=0.0 ruido=0.45 regla40=0.8705 (json 0.8705, igual=True) regla418=0.9275 | R1_CON_TASA W=0.9310 129/122 p=0.705 | ...
CELDA A=0.3 ruido=0.45 regla40=0.8935 (json 0.8935, igual=True) regla418=0.9260 | R1_CON_TASA W=0.9310 90/80 p=0.49 | ...
POSTHOC R1_CON_TASA contra regla418: EMPATE x6 -> IGUALA
POSTHOC R1_CON_LIQ contra regla418: EMPATE x6 -> IGUALA
POSTHOC R1_SIN_LIQ contra regla418: ...,PEOR(0.0218) -> PIERDE
CHEQUEO regla40_reproduce_json=True
```

## Archivos
- Este archivo.
- `titan/factorial-mosca-2026-10-13` @ `5c4fbac` (bot): `results/factorial_2026-10-13/` con 9 logs, 9 json, 9 versiones, `agregado.log` y `MD5SUMS.txt`.
- `titan/factorial-mosca-2026-10-13` @ `19a508c`: `tools/factorial/posthoc_regla418.py` y `results/factorial_2026-10-13/posthoc_regla418.log`.

## NO MEDIDO
- El post-hoc no estaba sellado: lo corrí después de ver el SUPERA porque el diseño mezclaba cableado con cantidad de sensores. Para firmarlo hay que sellarlo antes en otra corrida.
- Equivalencia: IGUALA es "ninguna celda distinta tras Holm", no prueba de equivalencia (no hay margen pre-registrado).
- Otras semillas de τ y de prueba. El contraste RECORTE también cambia el τ de las descendentes (declarado en la 001 antes de ver resultados).
- LIF con otra entrada (Poisson, otra ganancia) o con paso de 0,1 ms: el DAÑA vale para este LIF, no para todo LIF.
- R2 (33.489 neuronas), la neurona líquida entrenada y las formas dendríticas.
- CONTEXTO sin actualizar (pendiente con la 001).

## Antes de firmar
| Afirmación | Instrumento | Podía dar rojo |
|---|---|---|
| Instrumento válido | ancla y guardas por config, MD5SUMS | sí: la corrida 1 dio rojo |
| R1 cierra la brecha | McNemar y Holm sellados | sí: M46 pierde |
| El supera es por sensores | regla sobre 418 entradas | sí: R1 podía seguir ganando |
| El cableado paga dentro de R1 | 50 SL y 50 T | sí: R1_SIN_LIF no les gana a los SL |
| Equivalencia con el diseño | ninguno | NO MEDIDO |

--- METODO PROMETEO ---
Accion delicada: no
Maquina: Actions x64 (corrida) | brain-env (lectura y post-hoc)
Artefactos: docs/agents/respuestas/2026-10-13-002-el-cableado-de-1504-neuronas-alcanza-al-diseno-de-la-mosca-y-el-supera-era-tener-mas-sensores.md + Doc de ClickUp 2026-10-13-002
