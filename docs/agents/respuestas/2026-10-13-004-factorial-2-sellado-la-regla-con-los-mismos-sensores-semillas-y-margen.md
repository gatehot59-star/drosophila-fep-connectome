# 2026-10-13-004 · Factorial 2 sellado: la regla con los mismos sensores que la red, 10×10 semillas, margen de 1 punto y R2 en Actions

## Veredicto

- **[MEDIDO] Sellado y sin disparar.** Rama `titan/factorial2-mosca-2026-10-13`, commit de sello `9442fdf`. El instrumento no cambió desde el humo: `factorial2_mosca.py` md5 `798a824c…`, `agregar_factorial2.py` md5 `150b6f08…`, workflow `factorial2-mosca.yml` md5 `b497fe0d…`. Los tres md5 se verificaron en un clon limpio. La API pública de Actions no muestra ninguna corrida del factorial en la rama.
- **[MEDIDO] Humo en brain-env: 8 de 8 corridas VALIDO.** El ancla reproduce la 015 **exacta** (12 de 12 números iguales). Los dos controles nuevos dan verde: TAU_DN_IGUAL (las 6 descendentes tienen el mismo tau en M46, R1 y R2) y REGLA40_IGUAL (la regla de 40 da lo mismo en los tres recortes). Los números del humo **no valen** (120 ensayos de entrenamiento y 80 de prueba).
- **[CONCLUSIÓN] Listo para correr en Actions.** Son 29 trabajos y el más largo es R2.
- **[CONCLUSIÓN] Cambio contra lo propuesto en la 003: R2 va a Actions, no a Kaggle.**
  - En brain-env, R2 tarda 0,79 s por ensayo con numpy y scipy.
  - Un trabajo de R2 (1 semilla de tau, 1 celda, 12.400 ensayos) toma unas 2,7 h a la velocidad de brain-env, dentro del tope de 340 min aunque Actions no fuera más rápido.
  - Es el mismo instrumento que R1, así que no hay un port a torch que verificar (W-01).
  - Kaggle queda de reserva, sólo si algún trabajo de R2 se pasa del tope.

## Pedido

ClickKit `sellar_factorial2_003` (valor `sellar_factorial2`), sobre lo propuesto en la 2026-10-13-003. Sellar la revancha: la regla con los mismos sensores que la red, varias semillas de tau y de prueba, un margen de equivalencia declarado antes de correr, y R2.

## Herramientas y máquina

- **brain-env**, por el gateway MUDH (`run`):
  - medición de costo de R2 (`/workspace/tm_2026-10-13/f2/medir_r2.py`, md5 `43623339…`);
  - humo (`tools/factorial2/humo_f2.sh`);
  - clon de verificación;
  - consulta a la API pública de Actions.
- **GitHub MCP:** `create_branch` y dos `push_files` en la rama titan, más este archivo en main. No se mergeó nada.
- **Actions:** no se disparó nada del factorial. Al pushear el candidato `4325c18` corrió solo un workflow ajeno ("H4 integrated regression", success); no es de este experimento.
- **Kaggle:** no se usó. No se gastó cuota ajena.

## Diseño sellado (qué cambia contra el factorial 1)

| # | Factorial 1 (019) | Factorial 2 (este) | Por qué |
|---|---|---|---|
| 1 | Regla de 40 entradas para todos | **Regla propia**: la regla sobre las mismas entradas que recibe la red (40 en M46, 418 en R1, 564 en R2). La de 40 queda como referencia. | El post-hoc de la 002 mostró que el SUPERA de R1 venía de tener más sensores. |
| 2 | Tau por orden, `default_rng(0)` | Tau por `root_id`: `default_rng([semilla, root_id])` | En el factorial 1, las DN cambiaban de tau al cambiar de recorte (confusión declarada en la 001). |
| 3 | Ruido por bloque (101/102 y 103/104) | Ruido por `root_id`: 101 en entrenamiento y 1000 + semilla en prueba | Un mismo sensor ve el mismo ruido en los tres recortes. |
| 4 | 1 semilla de tau (0) y 1 de prueba (2) | Tau 0..9 y prueba 2..11 (en R2: tau 0..2 y prueba 2..6) | Sacar el resultado de una sola semilla. |
| 5 | IGUALA sin margen | **Margen M = 0,01** (20 de 2.000 ensayos) | IGUALA no es equivalencia (001). |
| 6 | R1 como recorte mayor | Se suma **R2**: R1 más las presinápticas con 5 sinapsis o más (definición de la 018); radio espectral por ARPACK | Ver si más cableado aporta algo. |
| 7 | Nulos SL/T y LIF | Fuera | Ya están medidos; el LIF dañó y es lo más lento. |

**Lo que no cambia:** la tarea, las sintonías, el lector (líneas, umbrales con FA 0,05, carrera), el radio 0,9, las neuronas TASA y LIQ (g = 1,0) y el pin de md5 de los insumos.

**Configuraciones y trabajos (29):**

- ANCLA_015: 1 trabajo.
- M46_TASA y M46_LIQ: 1 trabajo cada una (10×10 semillas).
- R1_CON_TASA, R1_CON_LIQ, R1_SIN_TASA y R1_SIN_LIQ: 2 trabajos cada una (tau 0..4 y 5..9).
- R2_CON_TASA: 18 trabajos (3 semillas de tau × 6 celdas, 5 semillas de prueba).

**Primaria, por configuración (7, sin el ancla):**

- **Diferencia:** d = acierto de W menos acierto de la regla propia, por semilla de tau, semilla de prueba y celda; el estimador es la media.
- **Intervalo:** bootstrap de dos vías (semillas de tau y de prueba remuestreadas por separado), B = 20.000, semilla 2026, percentiles α' = 0,05/7 por lado (nivel 98,57 %).
- **Veredictos:**
  - SUPERA si lo > +M;
  - PIERDE si hi < −M;
  - EQUIVALENTE si −M < lo y hi < +M;
  - NO_INFERIOR si lo > −M y hi ≥ +M;
  - NO_SUPERIOR si hi < +M y lo ≤ −M;
  - INDETERMINADO en cualquier otro caso.

**Contrastes (familia aparte, α' = 0,05/9):** INHIB ×2, LIQ ×3, RECORTE R1 ×2, RECORTE R2 y SENSORES (regla de 418 menos regla de 40).

**Hipótesis pre-registradas:**

- **H_ALCANZA**, "con cableado suficiente la simulación alcanza al diseño":
  - refutada si R1_CON_TASA y R1_CON_LIQ dan PIERDE;
  - sostenida si alguna de las dos da EQUIVALENTE, NO_INFERIOR o SUPERA.
- **H_SUPERA**, "el cableado aporta algo más que el diseño": sostenida sólo si alguna configuración R da SUPERA.

## Qué se midió (humo en brain-env, Celeron con 2 CPU, Python 3.12.14, numpy 2.5.3)

| Control | Resultado |
|---|---|
| Ancla REPRODUCE_015 | tolerancia 6/6 True, **exacto 6/6 True** |
| SIM_IGUAL (M46: este script contra el módulo de la 015) | max_dif = 0 |
| R1 | 1.504 neuronas, 91.484 aristas, 30.862 inhibitorias, 418 entradas |
| RADIO (R1, densa contra eigs) | 587,650540939 = 587,650540939 |
| DISPERSA_IGUAL (R1) | 2,78e-16 |
| TROZOS_IGUAL (R1) | 0 |
| R2 | 33.489 neuronas, 4.031.897 aristas, 1.506.653 inhibitorias, contiene a R1 y a M46 |
| R2, entradas sintonizadas por lado | 564 (LC4 54/50, LPLC2 108/102, LPLC4 56/54, LPLC1 68/72) |
| R2, radio por eigs | 2032,307097 en 2,3 s |
| TAU_DN_IGUAL (semillas 0 y 1, incluye R2) | True |
| REGLA40_IGUAL (12 claves, incluye R2) | True |
| Agregador de humo | EXIT 0, todas las primarias INDETERMINADO (n chico, como se esperaba); R2 NO_EVALUABLE por plan incompleto (el humo usó 1 celda) |
| Costo de R2 | 280 ensayos en 220,2 s, o sea 0,79 s por ensayo de 40 pasos |
| Costo de R1 | unos 5 s por celda con 2 tau y 280 ensayos, o sea 0,009 s por ensayo |

## Evidencia cruda

```
# ANCLA_015.log (md5 56301f6a…)
CHEQUEO REPRODUCE_015 tolerancia=[True, True, True, True, True, True] exacto=[True, True, True, True, True, True] -> True
CHEQUEO INSTRUMENTO sin_negativas=True SIM_IGUAL=True REPRODUCE_015=True -> VALIDO
escrito factorial2_ANCLA_015.json md5=d5216da02f35ff1d2374d5504438c381
# R1_CON_TASA.log (md5 9b334078…)
SUJETO R1 neuronas=1504 aristas_crudas=91484 inhibitorias_crudas=30862 entradas=418 contiene_M46=True contiene_R1=True esperado=(1504, 91484) -> True
CHEQUEO RADIO densa=587.650540939 eigs=587.650540939 -> True
CHEQUEO DISPERSA_IGUAL max_dif=2.78e-16 -> True | TROZOS_IGUAL max_dif=0 -> True
# R2_CON_TASA.log (md5 7678358f…)
SUJETO R2 neuronas=33489 aristas_crudas=4031897 inhibitorias_crudas=1506653 entradas=564 contiene_M46=True contiene_R1=True esperado=(33489, 4031897) -> True
RADIO crudo=2032.307097 metodo=eigs | 2.3 s
CELDA 0.3|0.15 lista | 220.2 s
CHEQUEO INSTRUMENTO R2_tamano=True -> VALIDO
# agregado.log (humo, md5 d93c2d93…)
CHEQUEO TAU_DN_IGUAL semillas=[0, 1] -> True
CHEQUEO REGLA40_IGUAL claves=12 -> True
VEREDICTO_GLOBAL -> VALIDO | M46_TASA=INDETERMINADO M46_LIQ=INDETERMINADO R1_CON_TASA=INDETERMINADO R1_CON_LIQ=INDETERMINADO R1_SIN_TASA=INDETERMINADO R1_SIN_LIQ=INDETERMINADO R2_CON_TASA=NO_EVALUABLE
estado: ANCLA_015 rc=0 M46_TASA rc=0 M46_LIQ rc=0 R1_CON_TASA rc=0 R1_CON_LIQ rc=0 R1_SIN_TASA rc=0 R1_SIN_LIQ rc=0 R2_CON_TASA rc=0 agregado rc=0
# duraciones (s): ANCLA 27,0 · M46_TASA 18,8 · M46_LIQ 15,2 · R1_CON_TASA 71,5 · R1_CON_LIQ 70,0 · R1_SIN_TASA 57,6 · R1_SIN_LIQ 80,3 · R2 253,5
# clon limpio de 9442fdf
798a824cd47808155fa12adb9e652dac  tools/factorial2/factorial2_mosca.py
150b6f08ab2d9850bcf3467d9770ed5a  tools/factorial2/agregar_factorial2.py
b497fe0dd9527870e23d81d44f327d58  .github/workflows/factorial2-mosca.yml
sin_CORRER · yaml_ok 29 ['correr', 'agregar']
runs_en_rama 1: H4 integrated regression completed success 4325c18
```

**md5 de los json del humo (en brain-env, `/workspace/tm_2026-10-13/f2/humo/`):**

| JSON | md5 |
|---|---|
| M46_TASA | 786ba01a… |
| M46_LIQ | 9cf6d0ef… |
| R1_CON_TASA | ae272ee3… |
| R1_CON_LIQ | cc49aef0… |
| R1_SIN_TASA | 10894596… |
| R1_SIN_LIQ | f72c81e2… |
| R2_t0c3 | d69db56d… |

**Cómo se corre:** pushear `results/factorial2_2026-10-13/CORRER` en la rama. El agregado lo commitea el bot en `results/factorial2_2026-10-13/`.

## Archivos

- Rama `titan/factorial2-mosca-2026-10-13`:
  - `tools/factorial2/factorial2_mosca.py`, `tools/factorial2/agregar_factorial2.py` y `tools/factorial2/humo_f2.sh` (commit `4325c18`);
  - `.github/workflows/factorial2-mosca.yml` (sello `9442fdf`).
- main: este archivo.
- Los logs y json del humo quedan en brain-env; acá van sus md5 y sus líneas clave, porque son números sin valor.

## NO MEDIDO

- **Ningún resultado del factorial 2.** Todavía no corrió.
- **El tiempo real de R2 en Actions.** Hay una estimación por brain-env (2,7 h por trabajo como techo) y no está medida. Si un trabajo pasa de 340 min, muere, y su configuración queda NO_EVALUABLE.
- **Debilidades declaradas antes de correr:**
  - **El bootstrap de R2 es grueso.** R2 tiene 3 semillas de tau y 5 de prueba, así que su intervalo es menos confiable que el de R1.
  - **El entrenamiento es uno solo** (semilla 1), así que su varianza no entra en el intervalo.
  - **Lo que queda fuera:** R2 sin inhibición, R2 con LIQ, LIF, los nulos SL/T y un g distinto de 1,0.
- **La pregunta de fondo sigue abierta.** Si a la mosca le falta otra neurona o la forma dendrítica no se puede medir con estos insumos, porque no hay coordenadas de sinapsis.

## Antes de firmar

| Afirmación | Instrumento | ¿Podía dar rojo? |
|---|---|---|
| El ancla reproduce la 015 exacta | REPRODUCE_015 contra los 12 números del log de la 015 | Sí: compara número a número, con bandera de exacto |
| Las DN tienen el mismo tau en los tres recortes | TAU_DN_IGUAL en el agregador | Sí: con tau por orden (factorial 1) daba distinto |
| Un mismo sensor ve el mismo ruido en todo recorte | REGLA40_IGUAL | Sí: con ruido por bloque, R2 tendría otro orden de entradas |
| R2 es el de la 018 | R2_tamano (33.489 / 4.031.897, contiene R1) | Sí: compara con el log de la 018 |
| Sellado sin disparar | API de runs de la rama, más la ausencia de CORRER | Sí: listaría la corrida |
| R2 cabe en el tope | Estimación | **No es una medición: queda NO MEDIDO** |

```
--- METODO PROMETEO ---
Accion delicada: no (rama titan, nada disparado, nada mergeado)
Maquina: brain-env (medicion de costo, humo, clon de verificacion) | Actions x64 (cuando se dispare)
Artefactos: docs/agents/respuestas/2026-10-13-004-factorial-2-sellado-la-regla-con-los-mismos-sensores-semillas-y-margen.md + Doc de ClickUp 2026-10-13-004
```
