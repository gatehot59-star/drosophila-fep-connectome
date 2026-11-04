# 2026-11-03-012 · 009-A1 abierto: el freno existe en 17 de 22 circuitos, la regla de DNp04 se repite en R01 y R03, y los dos veredictos sellados quedan sin decidir

**Veredicto del pedido:** abierto y leído. El sobre de 009-A1 se abrió con la autorización escrita de Abraham, en el orden de la 010 y con un commit antes de cada paso. Las dos calculadoras dan lo mismo: cotejo CONCORDANTE, con K1 0 celdas, K2 0 y K3 0 diferencias. Leído con la tabla de la 007:

- **Freno activo en 17 de 22** (12 de 16 relevos y 5 de 6 hubs): «X frena a D′» generaliza en el modelo.
- **P_T1_B = NO_INFORMATIVO_EN_B:** R01 (DNp35→CB0527) y R03 (DNa03→PLP060) pasan; R02 (DNpe016→cL22c) es no informativo, porque en B su relevo no frena. No cuenta ni a favor ni en contra.
- **P_T2_B = SIN_DECIDIR:** pasa 1 de 4 tipos de hub (CB0534).
- **F_C:** SOSTENIDA sólo en PS100 H4b, en el banco artificial C; SIN_DECIDIR en los otros cinco. **F_R01:** SOSTENIDA, 3 de 3 contrastes.

Es el modelo LIF de Shiu sobre FlyWire 783, no la mosca.

Doc: [2026-11-03-012 · 009-A1 abierto](https://app.clickup.com/90171457413/docs/2kza6fw5-26157/2kza6fw5-29797)

## En criollo

El freno que vimos en DNp04 no es un caso raro: en 17 de los 22 circuitos, cortar los cables del relevo hacia los descendentes que frena los suelta, de 7,8 a 378 Hz. Que el freno lo prenda un solo descendente se repite clarísimo en R01 y R03, donde cortar ese único cable devuelve el 100 y el 99 % del freno; pero el veredicto sellado pedía tres de tres y R02 no se pudo medir. En los hubs la regla sólo funciona en CB0534; en PS100 los intervalos la contradicen. En una frase: el freno es general; quién lo prende, no (lo segundo, sellado en los hubs y descriptivo en los demás relevos).

## Lo sellado, con sus números (régimen B, n = 20 semillas)

| Pieza | Criterio fijado (010) | Resultado |
|---|---|---|
| Freno (ΔQ2) | ≥ 5 Hz, IC95 sin el 0, F_B Holm < 0,01, drivers y relevo ≥ 10 Hz en C0 | ACTIVADO en R01, R03 a R08, R10, R11, R14 a R16 y en H1, H2, H3, H4 y H4b; NO_INFORMATIVO_EN_B en R02, R09, R12, R13 y H1b |
| T1, R01 | r_Q1 ≥ 0,35 y s4 ≥ 0,50 con el IC sobre el margen, más T1a y T1b en F_B | PASA: r_Q1 1,003 [1,000; 1,015], s4 1,652 [1,566; 1,803] |
| T1, R02 | ídem | NO_INFORMATIVO_EN_B: ΔQ2 −0,05 Hz [−0,55; 0,45] |
| T1, R03 | ídem | PASA: r_Q1 0,994 [0,956; 1,000], s4 0,958 [0,942; 0,974] |
| T2, CB0534 (H2) | c_Xconj y r_Q1conj ≥ 0,40 con el IC sobre el margen, más T2a, T2b y T2c en F_B | PASA: c_Xconj 0,955, r_Q1conj 0,941 [0,892; 0,980] |
| T2, CB0172 (H3) | ídem | SIN_DECIDIR: c_Xconj 0,390 [0,375; 0,404], r_Q1conj 0,403 [0,350; 0,456] |
| T2, CB0580 (H1 y H1b) | ídem, los dos | SIN_DECIDIR: H1 r_Q1conj 0,330; H1b no informativo |
| T2, PS100 (H4 y H4b) | ídem, los dos | SIN_DECIDIR: r_Q1conj 0,093 [0,072; 0,110] y 0,163 [0,130; 0,185], intervalos que contradicen la predicción |
| F_C | sincronizado menos corrido > 0, Holm < 0,01 | H4b +5,85 Hz [4,95; 6,85] SOSTENIDA; H1 −4,50, H2 −2,05 y H3 −1,80 con el intervalo bajo cero; H4 −0,75 y H1b +0,35 con el cero adentro |
| F_R01 | ZA1, ZA2 y ZA3 en régimen A, Holm < 0,01 | SOSTENIDA: medias 62,0, 40,85 y 65,95 |

## Lo descriptivo, fuera de lo sellado

1. **Otros relevos con freno en B:** cortar el cable del descendente devuelve mucho del freno en R05 (0,95) y R08 (0,78), la mitad o algo menos en R06 (0,39) y R07 (0,40), y poco en R04 (0,32), R10 (0,22), R16 (0,18), R15 (0,07), R14 (0,06) y R11 (0,04).
2. **La trampa no mordió en B:** los intervalos de cociente que usaron T1 y T2 en las celdas con freno (R01, R03, H1, H2, H3, H4 y H4b) y los seis de F_C salieron con estado OK. Sí apareció en el régimen A: R02 y R04 dan c_X = r_Q1 = 1 en las 20 semillas y su BCa queda degenerado.
3. **La entrada cambia quién prende el freno:** en A, los 5 relevos reclutados (R01, R02, R04, R14 y R16) dan r_Q1 entre 0,52 y 1. R14 y R16 dan 0,52 y 0,97 en A, contra 0,06 y 0,18 en B.
4. **Banco C:** H1, H2 y H3 disparan más con las espigas corridas que sincronizadas, lo contrario de una compuerta por coincidencia.

## Qué sigue (opinión)

1. **R02 y los otros cuatro no informativos piden otra entrada, no otra anatomía** (fila de la 007). Para cerrar P_T1_B hace falta que R02 frene en B: un sobre chico, sellado antes, con otra entrada para R02, R09, R12, R13 y H1b. La alternativa es A, donde R02 sí frena, pero ahí cae la trampa y antes habría que sellar una regla para el BCa degenerado. Decide Abraham.
2. **G1 tiene material:** una regla general («X frena a D′», 17 de 22) y una condicional (el descendente prende el freno: DNp04, R01 y R03 sellados; R05 y R08 descriptivos). La pregunta de G1 es si un programa corto con esas reglas genera circuitos parecidos a los reales mejor que G0, con el mismo presupuesto.
3. **Antes de hablar de la mosca:** BANC en el modelo, y robustez a pesos, tau y umbral.

## 1. Pedido

«Autorizo abrir el sobre de 009-A1» (Abraham, chat, 3-nov-2026 23:48 ART), sin otras indicaciones. Se aplicaron las tres recomendaciones de la 011, commiteadas antes de bajar el sobre (ee866972).

## 2. Herramientas

- brain-env por el gateway (servicio build, python): descargas raw del sobre (444 archivos, 22.571.291 B) y del código fijado, corridas del verificador (fases ET, ETS y ETK) y del productor, y la lectura con lectura_a1.py. Escribió sólo en /workspace/a1/v2/apertura/. Una consulta a la API pública de GitHub para listar las respuestas del día.
- GitHub MCP: cinco commits en main (ee866972, 698d9652, b035067c, d3cb0694 y este) y lecturas.
- ClickUp: la página del Doc.
- Sin GPU, sin Actions, sin merge, y sin tocar 010, el productor ni el verificador.

## 3. Qué se midió

| # | Afirmación | Instrumento | ¿Podía dar rojo? | Veredicto |
|---|---|---|---|---|
| 1 | El sobre leído es el sellado | sha256 de los 444 archivos contra SHA256SUMS (bf9ebde6), bajados de 7d953dc8 | sí, con un byte distinto | PASS 444/444 |
| 2 | Corrió el código fijado | sha256 de verificador_a1.py (a7b553f7), de estadistica_a1.py (37ab63d7) y de sus 4 módulos contra HUELLAS | sí | PASS |
| 3 | La salida del verificador quedó fijada antes del productor | 698d9652 a las 03:00:37Z; el productor arrancó a las 03:01:07Z | sí, por el orden | PASS |
| 4 | El agregado quedó fijado antes del cotejo | b035067c a las 03:02:36Z; ETK arrancó a las 03:03:00Z | sí, por el orden | PASS |
| 5 | Las dos calculadoras coinciden | fase K del verificador | sí: en el ensayo sucio de la 010 dio diferencias | CONCORDANTE, 0 sin clasificar |
| 6 | Los veredictos decisivos son iguales en los dos JSON | lectura_a1.py compara P_T1_B, P_T2_B, F_C, F_R01 y T3 | sí | PASS 5/5. Mi primera versión comparaba el bloque entero y dio False por la redacción de P_ESTRATOS y una nota de texto de QWEAK; corregido y declarado |
| 7 | Nadie leyó un veredicto antes del cotejo | la salida del productor fue a un archivo sin imprimir | no: no se puede comprobar desde afuera | DECLARADO |
| 8 | Los bytes en git son los de brain-env | sha256 bajando de raw cada commit | sí | PASS 1/1, 8/8, 3/3 y 4/4; el de este commit queda en el Doc |

## 4. Evidencia cruda

Todo en docs/agents/evidencia/2026-11-03-012-apertura-a1/, verbatim:

- 00-decisiones-antes-de-abrir.md
- 01-descarga/bajar_sobre.py y bajar_sobre.log
- 02-verificador/paso23.py, paso23.resumen, ver_et.log, ver_ets.log, verificacion_tecnica.json y COMPROMISO.md
- 03-productor/paso4.py, paso4.resumen y COMPROMISO.md
- 04-cotejo/paso5.py, paso5.resumen, ver_etk.log y cotejo_a1.json
- 05-lectura/lectura_a1.py, lectura_a1.txt y estadistica_a1.log (la salida del productor, con las 55 pruebas)

Líneas clave, copiadas de esos archivos:

```
K: CONCORDANTE | sin clasificar 0 | K1 0 celdas | K2 espejo 0 diferencias | K3 propio 0 diferencias
VEREDICTO P_T1_B NO_INFORMATIVO_EN_B casos={"R01": "PASA", "R02": "NO_PASA:NO_INFORMATIVO_EN_B", "R03": "PASA"}
VEREDICTO P_T2_B SIN_DECIDIR tipos={"CB0172": "NO_PASA:SIN_DECIDIR", "CB0534": "PASA", "CB0580": "NO_PASA:SIN_DECIDIR", "PS100": "NO_PASA:SIN_DECIDIR"}
VEREDICTO F_C H4b SOSTENIDA
VEREDICTO F_R01 firma=SOSTENIDA contrastes={"ZA1": true, "ZA2": true, "ZA3": true}
```

| Salida (brain-env, /workspace/a1/v2/apertura/) | Bytes | sha256 |
|---|---|---|
| ver/verificador_a1.json | 283.090 | ad65761bb84ee6632d65f03de88b263a209da5a4242e1055d92bd2f4a8432334 |
| prod/agregado_a1.json | 339.460 | 7fcc6ddc27774fd5b1b702803de3dd3953c2b91b724294c04c9159442ceba02a |
| prod/tasas_por_neurona.csv | 1.152.346 | c7cc155de8d803104fbb298be6bc4a6af9d47c274f166c4bb010fc7f05b7a329 |
| ver/cotejo_a1.json | 1.290 | 584db4dd4eea62749ee7d3e489eaa073785fc9d72abbf4042527a0fbd7cc9c1d |

## 5. Archivos

- Este archivo.
- docs/agents/evidencia/2026-11-03-012-apertura-a1/05-lectura/ (lectura_a1.py, lectura_a1.txt y estadistica_a1.log), en este commit.
- Lo demás de esa carpeta, en ee866972, 698d9652, b035067c y d3cb0694.

## 6. NO MEDIDO

- La mosca: todo es el modelo LIF de Shiu sobre FlyWire 783.
- BANC en el modelo, y la robustez a pesos, tau y umbral.
- R02, R09, R12, R13 y H1b en B: la entrada no prendió su freno.
- D12, el índice de ablación original: no se calculó (decisión fijada en ee866972).
- Lo descriptivo de arriba: no está sellado.
- Dónde caen los 104 BCa degenerados que contó el motor: no lo desglosé.
- verificador_a1.json, agregado_a1.json y tasas_por_neurona.csv enteros: no están en git. Van por sha256 y se recalculan desde git.
- Que nadie miró un veredicto antes del cotejo: declarado.
- Independencia de selección del verificador: deuda de la 010; la orden 009 sigue para una auditoría externa.
- La verificación post-push de este commit: se hace después del push y queda en el Doc y en brain-env.

## Estado vigente que CONTEXTO todavía no refleja

Reemplaza al de la 011 en lo que toca a 009-A1. CONTEXTO-drosophila-fep.md sigue en la respuesta 2026-11-03-002 (136.411 B); partirlo en estado vivo corto más historial espera a Abraham.

- **009-A1, abierto y leído (esta respuesta):** freno activo en 17 de 22; P_T1_B NO_INFORMATIVO_EN_B (R01 y R03 pasan, R02 no informativo); P_T2_B SIN_DECIDIR (1 de 4 tipos, CB0534); F_C SOSTENIDA sólo en H4b; F_R01 SOSTENIDA. Cotejo CONCORDANTE. Evidencia en docs/agents/evidencia/2026-11-03-012-apertura-a1/.
- **Decisión que espera a Abraham:** cómo cerrar T1 (otra entrada en B para los 5 no informativos, o una regla sellada para el BCa degenerado en A); si G1 arranca con las dos reglas; la sección 15 del Doc maestro; partir CONTEXTO.
- **Síntesis vigente en criollo:** esta respuesta.

## QA (PROMETEO-QA, tipo «reporte»)

| Criterio | Puntos | Evidencia |
|---|---|---|
| Completitud | 14/15 | los seis pasos de la 010, en orden y con commit (ee866972, 698d9652, b035067c, d3cb0694 y este); −1 porque los JSON grandes van sólo por sha256 |
| Arquitectura del razonamiento | 9/10 | sellado y descriptivo separados, tabla de la 007 aplicada sin cambios; −1 porque «lo prende otra cosa» en R04, R10, R11 y R14 a R16 descansa en r_Q1 sin prueba sellada |
| Documentación | 9/10 | respuesta, Doc y carpeta de evidencia con un COMPROMISO por paso; −1 porque CONTEXTO sigue atrasado |
| Innovación | 4/5 | compromiso por sha256 en cada paso y decisiones commiteadas antes de bajar el sobre; −1, ningún instrumento nuevo |
| Proceso QA | 5/5 | cada puntaje cita commit o archivo; verificación post-push 1/1, 8/8, 3/3 y 4/4 |
| **Total** | **41/45 → 91/100** | N/A: 55 puntos (Ejecutabilidad, Seguridad, Testing y DevOps), porque no se entrega código nuevo: los scripts de 01 a 05 son registro de lo que corrió |

```plain
--- METODO PROMETEO ---
Accion delicada: NO (lectura autorizada de un sobre sellado; evidencia append-only)
Modo aplicado:   FULL
Maquina:         brain-env (host 6c09d8604b07, Python 3.12.14, NumPy 2.5.3, SciPy 1.18.1)
Rubrica:         41/45 -> 91/100 (reporte)
N/A declarados:  55 (Ejecutabilidad, Seguridad, Testing, DevOps: no se entrega codigo nuevo)
Review externo:  no pedido; la orden 009 sigue para una auditoria externa (deuda)
Instrumento:     verificador_a1.py de 5eaf35d0 (fases ET, ETS, ETK) y estadistica_a1.py de 801487ca,
                 rc 0 los cuatro; evidencia cruda en docs/agents/evidencia/2026-11-03-012-apertura-a1/
Artefactos:      docs/agents/respuestas/2026-11-03-012-a1-abierto-freno-17-de-22-t1-no-informativo-t2-sin-decidir.md
                 + https://app.clickup.com/90171457413/docs/2kza6fw5-26157/2kza6fw5-29797
```
