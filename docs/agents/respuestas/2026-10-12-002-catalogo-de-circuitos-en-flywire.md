# 2026-10-12-002 · Catálogo de circuitos en FlyWire: las 10 predicciones de literatura están en el cableado; el próximo motivo es el aterrizaje, que comparte la entrada del escape, y rumbo, objetos chicos y olfato no llegan directo a las descendentes

**Fecha:** 2026-10-12, madrugada (America/Buenos_Aires).
**Base:** `main` en `7ab677e` (2026-10-12-001). Datos pinneados: `connectivity.parquet` md5 `3d802fd542b5d18570ba1ba0bb0abed9`, `annotations.tsv` md5 `719904abad876c68ace1b5690c9b9b63` (flywire_annotations `17fc577`).
**Instrumento:** rama `titan/catalogo-circuitos-2026-10-12`: `tools/catalogo_circuitos/catalogo_circuitos.py` (md5 `4137ba5c4a35fc023df1346202f40339`, pre-registro `38baa15`) y `results/catalogo_circuitos_2026-10-12/run.log` (md5 `bd639879049c52c8fbe1a2c437c4bd8d`, 193 líneas, `bb68d7f`).
**Doc de ClickUp (público):** https://app.clickup.com/90171457413/docs/2kza6fw5-21317

## Veredicto

**Los ocho circuitos del catálogo de la 001 están en FlyWire v783 y las 10 predicciones de literatura aparecen en el cableado** (instrumento VÁLIDO: LC4 → DNp01 757 sinapsis; LC6 → DNp01 0, ni siquiera con 1 sinapsis).

**Lo que decide si un circuito entra como reflejo es cuánto de su salida llega directo a las descendentes:**

- **Aterrizaje y escape sí** (22,8% y 15,6%, unos 4 KB cada uno, 100% del mismo lado y 100% excitatorios por dentro).
- **Flujo óptico, a medias** (11,3%, sobre todo a DNp15; 248 B internos).
- **Objetos chicos (1,1%), olfato (0,5%) y rumbo (0%) no:** pasan por el cerebro central. Van a E1 o E3, no a E2.
- **Giro y marcha** son descendentes con entrada muy repartida (las 5 mayores suman 9% y 21%): interfaz motora (E4), no motivo recortable.

**Recomendación:** el próximo motivo es el **aterrizaje junto al escape**. La misma entrada visual (LC4, LPLC2) alimenta a los dos, y en la mosca el estado de vuelo decide cuál responde (Ache 2019). Es un cambio de contexto, donde DBC3 tiene ventaja medida: el primer acople SparseLTC → DBC3 con sentido biológico.

**Letra chica:** «confirma» es existencia de aristas con al menos 5 sinapsis; no mide fuerza ni función. Es una vara baja, aunque podía dar rojo (el control negativo lo prueba).

## 1. Pedido

Clic en el botón «Armar el catálogo de circuitos en FlyWire» de la 2026-10-12-001, cuyo paso 1 decía: «con las anotaciones pinneadas (`17fc577`), buscar cada circuito de la tabla y medir tamaño, cables y lateralidad, igual que con el escape».

## 2. Herramientas y máquina

- **brain-env** (Celeron N4020, Python 3.12.14, numpy 2.5.3, pandas 3.0.5): búsqueda exploratoria de nombres en las anotaciones (antes de fijar las definiciones), md5 de los datos contra `docs/METHODS.md`, la corrida (48,5 s, en segundo plano) y dos clones frescos para verificar md5 del script y del log. Sin credencial de push.
- **Sandbox de ClickUp** (Python 3.12.13, numpy 2.4.6, pandas 3.0.3): escritura del script y prueba sintética con un conectoma de 22 neuronas.
- **Búsqueda web:** Ache 2019 (Nat Neurosci, DNp07 y DNp10), Sapkal 2024 (Nature, oDN1 y BDN2), Braun 2024 (Nature, DNp09 → DNa02 y MDN → DNa01) y la revisión de Simpson 2023 (Curr Opin Neurobiol: DNp15 = DNHS1, DNp06, DNg02, DNa02, DNg13).
- **GitHub MCP:** rama nueva `titan/catalogo-circuitos-2026-10-12` desde `main`; pre-registro del script (`38baa15`); log crudo (`bb68d7f`); este archivo y el CONTEXTO en `main`.
- **ClickUp:** un Doc público nuevo. Actions y Kaggle sin uso; sin cuota ajena.

## 3. Qué se midió

### 3.1 Definiciones (fijadas en el script antes de correr)

Nombres buscados antes en las anotaciones: **oDN1, BDN2 y LPLC3 no están con ese nombre en v783**; DNg02 aparece como `DNg02_a` a `DNg02_h` (se toma el prefijo). Umbral: aristas con al menos 5 sinapsis. Bytes: formato de `swarm/` (6 B por arista y 2 B por neurona), sólo del conjunto definido.

### 3.2 El catálogo

| Circuito | Entrada → salida | Neuronas | Aristas internas | Bytes | Interno: excit. / mismo lado | Salida de la entrada a descendentes |
|---|---|---|---|---|---|---|
| Escape | LC4 (104), LPLC2 (210), LC6 (125) → DNp01 (2), DNp09 (2) | 443 | 439 | 3.520 | 1,00 / 1,00 | 15,6%: DNp04 23%, DNp103 23%, DNp01 13%, DNp02 8%, DNp11 7% |
| Aterrizaje | LPLC4 (110), LC4, LPLC2 → DNp07 (2), DNp10 (2) | 428 | 524 | 4.000 | 1,00 / 1,00 | 22,8%: DNb05 15%, DNp04 11%, DNp103 10%, DNp01 6%, DNp07 5% |
| Flujo óptico | HSE, HSN, HSS, H1, H2, VS1 a VS8 (2 cada uno) → DNp15 (2), DNp06 (2), DNg02 (25) | 55 | 23 | 248 | 0,96 / 0,65 | 11,3%: DNp15 17%, DNb03 14%, DNp20 13% |
| Giro | DNa01 (2), DNa02 (2), DNg13 (2), DNb02 (4) | 10 | 7 | 62 | 0,62 / 0,62 | (son descendentes) |
| Marcha | DNp09 (2), MDN (4); oDN1 y BDN2 no encontradas | 6 | 0 | 12 | NA | (son descendentes) |
| Rumbo | EPG (47), EPGt (4) → P-EN1 (20), P-EN2 (22) | 93 | 1.605 | 9.816 | 1,00 / 0,63 | 0% |
| Objetos chicos | LC11 (127), LC10a a f (816) | 943 | 1.127 | 8.648 | 0,89 / 1,00 | 1,1%: DNp35 59%, DNa10 37% |
| Olfato | receptores (2.282), PN (685) → Kenyon (5.177), LHLN (514), LHCENT (42), MBON (96) | 8.796 | 68.419 | 428.106 | 0,90 / 0,83 | 0,5% |

Todos los tipos con neuronas encontradas están repartidos casi parejo entre izquierda y derecha (ver las líneas TIPO del log).

### 3.3 Quién le entra a las salidas (top 5, fracción de la entrada total)

- **Escape (DNp01, DNp09):** LC9 6,8%, LPLC2 5,0%, LC31a 4,4%, LC4 4,4%, CB3707 3,7%. **La entrada mayor no está en nuestro motivo de 26.**
- **Aterrizaje (DNp07, DNp10):** **LPLC4 9,2%**, LTe64 4,6%, PS088 3,4%, PS058 3,1%, CB0442 3,1%.
- **Giro:** VES051/052 2,4%, LT51 1,9%, PS049 1,8%, CB0757 1,6%, DNae005 1,3% (suman 9%).
- **Marcha (DNp09, MDN):** LC9 6,8%, LC31a 4,5%, PVLP020 3,6%, CB0095 3,4%, PVLP004/005 2,9% (suman 21%).
- **Flujo (DNp15, DNp06, DNg02):** LPLC1 2,9%, IB008 2,6%, LHAD1g1 2,6%, LPLC2 2,3%, LC31a 1,9%.
- **Rumbo (P-EN):** GLNO 22,3%, EPG 18,8%, P-EN2 11,8%, ExR6 9,9%, Delta7 7,2%.

### 3.4 Predicciones de literatura (aristas ≥ 5)

| Id | Predicción | Fuente | Sinapsis (aristas) | Resultado |
|---|---|---|---|---|
| C+ | LC4 → DNp01 | control positivo | 757 (89) | PASS |
| C− | LC6 → DNp01 = 0 | control negativo | 0 (0); con ≥ 1 también 0 | PASS |
| E2 | LPLC2 → DNp01 | literatura y GF-01 | 844 (99) | CONFIRMA |
| A1 | LPLC4 → DNp07 o DNp10 | Ache 2019 | 1.414 (74) | CONFIRMA |
| M1 | DNp09 → DNa02, excitatoria | Braun 2024 | 55 (2), 100% exc. | CONFIRMA |
| M2 | MDN → DNa01 | Braun 2024 | 24 (3) | CONFIRMA |
| R1 | EPG → P-EN | de memoria | 6.409 (382) | CONFIRMA |
| R2 | P-EN → EPG | de memoria | 9.361 (437) | CONFIRMA |
| F1 | HS → DNp15 | Simpson 2023 (DNHS1) | 185 (5) | CONFIRMA |
| O1 | receptores → PN | vía clásica | 144.919 (7.687) | CONFIRMA |
| O2 | PN → Kenyon | vía clásica | 316.862 (21.509) | CONFIRMA |
| O3 | PN → cuerno lateral | vía clásica | 111.143 (6.583) | CONFIRMA |

**10 de 10.** Con una vara de existencia, se esperaba casi todo verde; lo informativo es la tabla 3.2 y la 3.3, no este conteo.

### 3.5 Lectura

- **La regla de reparto de la 001 ahora tiene número:** entra como reflejo (E2) lo que le habla directo a las descendentes. Aterrizaje y escape sí; rumbo, objetos chicos y olfato no.
- **Escape y aterrizaje comparten entrada** (LC4 y LPLC2 están en los dos; DNp04 y DNp103 aparecen en las dos listas de descendentes). En la mosca el estado de vuelo decide cuál manda (Ache 2019): es la tarea natural para DBC3 como compuerta de contexto.
- **El motivo de 26 de la 010 a la 015 es un recorte:** el escape completo tiene 443 neuronas, y la entrada mayor a DNp01 y DNp09 es LC9, que no está en el motivo.
- **El rumbo no llega al cuerpo por sí solo:** 0 sinapsis de EPG a descendentes. Hace falta su lector, que no está en este catálogo.
- **El olfato pesa 428 KB** sólo en su núcleo: no entra como reflejo en un microcontrolador chico.

## 4. Evidencia cruda (verbatim)

Comando (en brain-env, en segundo plano):

```text
python3 tools/catalogo_circuitos/catalogo_circuitos.py --conn /workspace/connectivity.parquet --annot /workspace/annotations.tsv --out results/catalogo_circuitos_2026-10-12
RC=0
```

Líneas 1 a 5, 12, 18, 25, 37, 39, 44, 56, 63, 69, 70, 87, 94, 105, 120, 128, 145, 147, 167, 169 y 175 a 193 de `run.log` (md5 `bd639879049c52c8fbe1a2c437c4bd8d`):

```text
# maquina: 6c09d8604b07 | Linux-4.19.0-27-amd64-x86_64-with-glibc2.41 | Python 3.12.14 | numpy 2.5.3 | pandas 3.0.5
# md5 script = 4137ba5c4a35fc023df1346202f40339
# fecha: 2026-10-12 03:29:42 +0000
# md5 conn = 3d802fd542b5d18570ba1ba0bb0abed9 (pin 3d802fd542b5d18570ba1ba0bb0abed9) | md5 annot = 719904abad876c68ace1b5690c9b9b63 (pin 719904abad876c68ace1b5690c9b9b63)
DATOS aristas=15091983 neuronas_anotadas=139248 extremos_sin_anotacion=1100 umbral=5
INTERNO circuito=escape neuronas=443 aristas5=439 sinapsis5=3066 frac_exc=1.0000 frac_ipsi=1.0000 bytes_formato_swarm=3520
  top1 entrada=LC9 sinapsis=1167 frac=0.0679
SALIDA_DE_ENTRADA circuito=escape sinapsis5=78253 a_descendentes=12199 frac=0.1559
INTERNO circuito=aterrizaje neuronas=428 aristas5=524 sinapsis5=4436 frac_exc=1.0000 frac_ipsi=1.0000 bytes_formato_swarm=4000
  top1 entrada=LPLC4 sinapsis=1414 frac=0.0920
SALIDA_DE_ENTRADA circuito=aterrizaje sinapsis5=114498 a_descendentes=26061 frac=0.2276
INTERNO circuito=giro neuronas=10 aristas5=7 sinapsis5=45 frac_exc=0.6222 frac_ipsi=0.6222 bytes_formato_swarm=62
TIPO circuito=marcha parte=salida tipo=oDN1 n=0 izq=0 der=0 centro=0 -> NO_ENCONTRADO
TIPO circuito=marcha parte=salida tipo=BDN2 n=0 izq=0 der=0 centro=0 -> NO_ENCONTRADO
INTERNO circuito=vuelo_flujo neuronas=55 aristas5=23 sinapsis5=491 frac_exc=0.9593 frac_ipsi=0.6517 bytes_formato_swarm=248
SALIDA_DE_ENTRADA circuito=vuelo_flujo sinapsis5=17686 a_descendentes=1989 frac=0.1125
INTERNO circuito=rumbo neuronas=93 aristas5=1605 sinapsis5=24133 frac_exc=1.0000 frac_ipsi=0.6302 bytes_formato_swarm=9816
SALIDA_DE_ENTRADA circuito=rumbo sinapsis5=37337 a_descendentes=0 frac=0.0000
INTERNO circuito=objetos_chicos neuronas=943 aristas5=1127 sinapsis5=7209 frac_exc=0.8889 frac_ipsi=1.0000 bytes_formato_swarm=8648
SALIDA_DE_ENTRADA circuito=objetos_chicos sinapsis5=212588 a_descendentes=2382 frac=0.0112
INTERNO circuito=olfato neuronas=8796 aristas5=68419 sinapsis5=887053 frac_exc=0.9034 frac_ipsi=0.8344 bytes_formato_swarm=428106
SALIDA_DE_ENTRADA circuito=olfato sinapsis5=1284026 a_descendentes=6392 frac=0.0050
PRED C+ pre=LC4 post=DNp01 cond=>0 aristas5=89 sinapsis5=757 frac_exc5=1.0000 aristas1=104 sinapsis1=805 -> PASS | control positivo (ficha GF-01)
PRED C- pre=LC6 post=DNp01 cond===0 aristas5=0 sinapsis5=0 frac_exc5=NA aristas1=0 sinapsis1=0 -> PASS | control negativo (ficha GF-01)
PRED E2 pre=LPLC2 post=DNp01 cond=>0 aristas5=99 sinapsis5=844 frac_exc5=1.0000 aristas1=189 sinapsis1=1080 -> CONFIRMA | LPLC2 -> GF (literatura y GF-01)
PRED A1 pre=LPLC4 post=DNp07|DNp10 cond=>0 aristas5=74 sinapsis5=1414 frac_exc5=1.0000 aristas1=104 sinapsis1=1470 -> CONFIRMA | Ache 2019 (solapamiento de dendritas)
PRED M1 pre=DNp09 post=DNa02 cond=>0exc aristas5=2 sinapsis5=55 frac_exc5=1.0000 aristas1=2 sinapsis1=55 -> CONFIRMA | Braun 2024 (excitatoria directa)
PRED M2 pre=MDN post=DNa01 cond=>0 aristas5=3 sinapsis5=24 frac_exc5=1.0000 aristas1=4 sinapsis1=26 -> CONFIRMA | Braun 2024
PRED R1 pre=EPG|EPGt post=PEN_a(PEN1)|PEN_b(PEN2) cond=>0 aristas5=382 sinapsis5=6409 frac_exc5=1.0000 aristas1=582 sinapsis1=6852 -> CONFIRMA | anillo de rumbo, de memoria
PRED R2 pre=PEN_a(PEN1)|PEN_b(PEN2) post=EPG|EPGt cond=>0 aristas5=437 sinapsis5=9361 frac_exc5=1.0000 aristas1=608 sinapsis1=9753 -> CONFIRMA | anillo de rumbo, de memoria
PRED F1 pre=HSE|HSN|HSS post=DNp15 cond=>0 aristas5=5 sinapsis5=185 frac_exc5=1.0000 aristas1=6 sinapsis1=187 -> CONFIRMA | nombre DNHS1 (Simpson 2023)
PRED O1 pre=class:olfactory post=class:ALPN cond=>0 aristas5=7687 sinapsis5=144919 frac_exc5=0.9998 aristas1=19438 sinapsis1=166172 -> CONFIRMA | via olfativa
PRED O2 pre=class:ALPN post=class:Kenyon_Cell cond=>0 aristas5=21509 sinapsis5=316862 frac_exc5=0.9986 aristas1=27848 sinapsis1=329394 -> CONFIRMA | via olfativa
PRED O3 pre=class:ALPN post=class:LHLN|class:LHCENT cond=>0 aristas5=6583 sinapsis5=111143 frac_exc5=0.9072 aristas1=20666 sinapsis1=136493 -> CONFIRMA | via olfativa
CHEQUEO INSTRUMENTO C+=PASS C-=PASS -> VALIDO
RESUMEN predicciones_de_literatura confirmadas=10 de 10
escrito resultados.json md5=38b54557aacd9f8c32ac5dbab17335d1
# duracion_s=48.5
EXIT_RUN=0
```

El log entero está en la rama. Verificación en clon fresco de `bb68d7f` (brain-env):

```text
bd639879049c52c8fbe1a2c437c4bd8d  /tmp/fc2/results/catalogo_circuitos_2026-10-12/run.log
4137ba5c4a35fc023df1346202f40339  /tmp/fc2/tools/catalogo_circuitos/catalogo_circuitos.py
```

Prueba sintética en el sandbox (22 neuronas): con el control limpio, `CHEQUEO INSTRUMENTO C+=PASS C-=PASS -> VALIDO`; al agregar una arista LC6 → DNp01 de 9 sinapsis, `PRED C- ... aristas5=1 sinapsis5=9 ... -> FAIL`, `CHEQUEO INSTRUMENTO C+=PASS C-=FAIL -> INVALIDO`, `EXIT_RUN=3`. En esa prueba, E2 y O3 dieron NO_CONFIRMA porque faltaban las aristas: el veredicto de predicción puede dar rojo.

Recomputable: `git checkout titan/catalogo-circuitos-2026-10-12 && python3 tools/catalogo_circuitos/catalogo_circuitos.py --conn <connectivity.parquet> --annot <annotations.tsv> --out <dir>`. Si los md5 de los datos no son los del pin, sale con 2.

## 5. Archivos generados

- **Rama `titan/catalogo-circuitos-2026-10-12`:** `tools/catalogo_circuitos/catalogo_circuitos.py` (`38baa15`) y `results/catalogo_circuitos_2026-10-12/run.log` (`bb68d7f`). `resultados.json` (md5 `38b54557aacd9f8c32ac5dbab17335d1`) no se commitea: es derivado y determinista; queda en brain-env en `/workspace/catalogo/results/catalogo_circuitos_2026-10-12/`.
- **`main`:** este archivo y `docs/agents/CONTEXTO-drosophila-fep.md`.
- **Doc de ClickUp público:** https://app.clickup.com/90171457413/docs/2kza6fw5-21317

## 6. NO MEDIDO

- **Fuerza o función** de cualquier conexión: sólo existencia con al menos 5 sinapsis.
- **Nulo** para las fracciones a descendentes y para el mismo lado: son descriptivas.
- **oDN1, BDN2 y LPLC3:** no están con ese nombre en v783; no se buscaron por morfología ni por correspondencia con otros conectomas.
- **Los bytes** cuentan sólo el conjunto definido, sin las entradas de más arriba (por ejemplo LC9 en el escape).
- **El lector del rumbo** (camino de EPG a la motora), el cordón nervioso (MANC, BANC) y cualquier hardware.
- **Las fuentes «de memoria»** (anillo E-PG / P-EN, HS y VS, LC10 y LC11, la vía olfativa): sin cita verificada en este turno. Ache 2019, Braun 2024, Sapkal 2024 y Simpson 2023 sí se verificaron.
- **Reproducción en una segunda máquina** y review externo.

## Antes de firmar

```text
"el instrumento es válido"             → C+ y C- sobre datos pinneados      → podía dar rojo: SÍ (prueba sintética: INVALIDO) → medido, bien
"las 10 predicciones están"           → aristas ≥ 5 entre tipos            → podía dar rojo: SÍ (sintética: NO_CONFIRMA) → medido, bien; vara baja
"aterrizaje y escape son reflejos"    → fracción de salida a descendentes  → descriptivo, sin nulo                          → medido sin nulo
"el rumbo no llega al cuerpo"         → sinapsis EPG → descendentes = 0    → podía dar rojo: SÍ                            → medido (sólo directo)
"el aterrizaje es el próximo motivo"  → ninguno                            → recomendación                                  → NO MEDIDO
```

## QA (TITAN FULL)

| Criterio | Puntaje | Evidencia |
|---|---|---|
| Completitud | 13/15 | Los ocho circuitos y las predicciones, con tamaño, lados, signo, bytes y salida a descendentes. −2: oDN1 y BDN2 sin buscar por otra vía; sin el lector del rumbo |
| Ejecutabilidad | 15/15 | Exit 0 con instrumento VÁLIDO; md5 2/2 en clon fresco; prueba sintética con rojo provocado |
| Arquitectura del razonamiento | 8/10 | Pre-registro antes de correr y controles de los dos signos. −2: la vara de existencia es baja y las fracciones no tienen nulo |
| Documentación | 9/10 | Docstring, códigos de salida y fuentes por circuito en el script. −1: los «de memoria» sin cita |
| Innovación | 4/5 | Métrica de «cuánto habla con el cuerpo» para decidir la etapa |
| Proceso QA | 4/5 | Cada fila con su línea de log. −1: sin review externo |
| Seguridad, Testing, DevOps | N/A (40) | Sin frontera de confianza; instrumento descriptivo cuyos controles son la prueba; sin CI nuevo |

**53/60 → 88/100 sobre lo aplicable.** Aprobado con deuda: nulos para las fracciones, citas de lo «de memoria» y review.

--- METODO PROMETEO ---
Acción delicada: NO (bitácora y contexto a main; instrumento en titan/catalogo-circuitos-2026-10-12)
Modo aplicado:   TITAN FULL
Rúbrica:         53/60 -> 88/100
N/A declarados:  40 (Seguridad 15, Testing 15, DevOps 10)
Review externo:  no pedido: no hay PR (deuda)
Instrumento:     tools/catalogo_circuitos/catalogo_circuitos.py (md5 4137ba5c4a35fc023df1346202f40339 sellado en 38baa15); VALIDO; EXIT_RUN=0; run.log md5 bd639879049c52c8fbe1a2c437c4bd8d (193 líneas) en bb68d7f; md5 2/2 en clon fresco
Máquina:         brain-env (Celeron N4020), 48,5 s; sandbox de ClickUp para escribir el script y la prueba sintética
Artefactos:      docs/agents/respuestas/2026-10-12-002-catalogo-de-circuitos-en-flywire.md + https://app.clickup.com/90171457413/docs/2kza6fw5-21317
