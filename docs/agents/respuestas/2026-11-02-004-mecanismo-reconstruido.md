# 2026-11-02-004 · Mecanismo reconstruido en el modelo: X frena a D por sus sinapsis directas, pero casi nunca la enciende S directo · en LC4 el freno es PVLP010, encendida por DNp04 · H_MECANISMO MIXTA, verificada

Doc: https://app.clickup.com/90171457413/docs/2kza6fw5-26157/2kza6fw5-29337
Rama: titan/mecanismo-2026-11-02, sin merge.
Corrida 2: run 41459331354, fuente b3b398d, evidencia en results/mecanismo_2026-11-02/actions_correr2 (8ffdfc6a30cf7f91e07617a576c106bfd277b497).
Verificación y descriptivos: results/mecanismo_2026-11-02/verificacion_veredicto/ (72e9eff206524472f86996cec5a4bcedefc8e53f y aaea8b634321f5058fd1d2c1bfb54a79e586c544).
Sello: SELLO-MECANISMO-2026-11-02.md (3c47400). Enmienda: ENMIENDA-MECANISMO-2026-11-02.md (3e34d46).

## 1. Pedido

«Reconstruí el mecanismo causal paso a paso» (2-nov-2026, 02:43 ART) y «sigue» (12:05 ART): leer y verificar el veredicto de la corrida 2 y entregar la reconstrucción. Debe incluir el circuito concreto, qué enciende a X, mecanismos rivales con predicciones distintas, cortes y restauraciones in silico, evidencia publicada y el experimento en la mosca que decide. Mecanismo separado de función y de formación, y cada eslabón etiquetado MEDIDO anatomía, MEDIDO modelo, LITERATURA o NO MEDIDO.

## 2. Herramientas declaradas

- brain-env (MUDH gateway, python), sobre la evidencia 8ffdfc6a ya bajada. Corrí verificar_veredicto.py (v1 con un defecto, v2 corregida), quien_mueve_x.py (dos versiones, se publica la segunda) y d_por_tipo.py. Bajé por raw.githubusercontent los seis archivos publicados para compararlos byte a byte. No escribí fuera de /workspace.
- GitHub MCP: dos commits en titan/mecanismo-2026-11-02 (72e9eff y aaea8b6), este archivo en main, y la lectura de la 003 en main.
- Búsqueda web: dos consultas (DNp04 y PVLP010).
- ClickUp: una página nueva en el Doc Topo inverso.
- Cuota ajena: ninguna. No corrí nada en Actions ni en Kaggle.

## 3. Qué se midió

Una línea por afirmación: afirmación → instrumento → ¿podía dar rojo? → veredicto.

- «El veredicto sellado es MIXTA» → verificar_veredicto.py v2. No importa nada del instrumento: usa permutación exacta 2^20, Holm y las reglas del sello, y rehace desde el parquet las filas que toca cada condición y la selección de K → sí: la v1 dio rojo por un error mío, y las filas y K se comparan contra lo registrado → **MIXTA**, igual al agregado; los cuatro estímulos dan PARCIAL.
- «P1 a P4 pasan en los cuatro» → el mismo verificador → sí → 16 de 16, todas con 20 de 20 ensayos positivos, p exacto 1,91e-06 y Holm 3,05e-05.
- «Falla solo ΔSX/ΔX ≥ 0,5» → el mismo → sí → ΔSX/ΔX 0,2886 / 0,2600 / 0,2321 / 0,4872 y ΔXD/ΔX 1,0239 / 0,7155 / 1,0893 / 0,7925 (LC4 / LPLC2 / LPLC1 / LPLC4).
- «Lo fuera del objetivo y la réplica izquierda del agregado están bien» → v2 → sí → iguales en los cuatro.
- «K quedó emparejado al impulso de X» → v2, campo alcanzo → sí → **NO en 3 de 4**: el pool activo llegó a 37 / 26 / 33 % del impulso de X en LC4, LPLC2 y LPLC4; en LPLC1 sí (101 %).
- «Quién enciende a X y quién lleva el freno» → quien_mueve_x.py, post hoc y no sellado → a medias: las cuentas podían dar rojo (la suma de X tiene que dar igual al agregado y el C0 de las dos mitades tiene que coincidir), pero el freno lineal es un proxy y no puede dar rojo sobre la causalidad de cada tipo → **descriptivo**.
- «DNp04 enciende a PVLP010 uno a uno» → tasas de d_por_tipo.py y quien_mueve_x.py, más una cuenta sobre las ecuaciones del modelo → las tasas podían no coincidir → DNp04 107,3 por segundo y PVLP010 106,7; 190 sinapsis contra un mínimo de 162. La causalidad de ese tramo está **NO MEDIDA**: no hay un corte sellado de DNp04→PVLP010.

### Paso 0 · Patrón, pregunta e instrumento

- Patrón, MEDIDO anatomía: S→D directo más S→X→D con X inhibitoria compartida, en FlyWire v783 y en BANC 888 (2026-11-01-001 a 005 y 2026-11-02-001).
- Instrumento: el modelo LIF de Shiu et al. 2024 sin tocar (philshiu/Drosophila_brain_model@91bdd1e7, model.py sha256 fc45837d…), Brian2 2.10.1, FlyWire 783 entero. S recibe Poisson a 50 Hz; 20 ensayos de 1 s con semillas comunes. Mide la causalidad del modelo, no de la mosca.

### Paso 1 · Circuito concreto (MEDIDO anatomía, lado derecho)

| Estímulo | S | D | X | X glu | Vía canónica: S→D; X con S→X / X→D | X→D total |
|---|---|---|---|---|---|---|
| LC4 | 50 | 10 | 49 | 8 | LC4→DNp01 431; PVLP010 209/137; LHAD1g1 51/124 | 4.017 |
| LPLC2 | 102 | 14 | 27 | 4 | LPLC2→DNp06 518; LHAD1g1 644/399 | 4.908 |
| LPLC1 | 72 | 7 | 32 | 3 | LPLC1→DNp03 848; PLP060, AVLP080, CB2700 | 2.333 |
| LPLC4 | 54 | 21 | 83 | 34 | LPLC4→DNp07 638; PLP214 70/201 | 7.425 |

### Paso 2 · Qué enciende a X

- MEDIDO anatomía. S aporta 1,5 / 3,8 / 1,5 / 4,7 % de la entrada sináptica total de X. PVLP010 recibe 2,3 % de LC4; LHAD1g1, 3,7 % de LPLC2; en BANC, LHAD1g1 y PVLP010 reciben 85 % de cerebro central. D le devuelve a X 0,50 / 0,51 / 0,05 / 0,24 % de su entrada, pero concentrado: DNp04→PVLP010 = 190 sinapsis, casi tanto como las 209 de LC4→PVLP010.
- MEDIDO modelo, sellado. Espigas de X que quedan, en % de C0:

| Condición | LC4 | LPLC2 | LPLC1 | LPLC4 |
|---|---|---|---|---|
| C2, cortar S→X | 38,5 | 53,5 | 51,5 | 48,4 |
| R2, X recibe solo de S | 75,5 | 69,0 | 45,0 | 84,9 |
| C4, cortar S→D | 76,3 | 86,9 | 98,8 | 95,1 |
| R3, S habla solo con D | 30,6 | 19,4 | 0,0 | 1,6 |

Las sinapsis directas S→X sostienen alrededor de la mitad de las espigas de X. El resto llega por otras vías que también nacen en S: en el modelo nadie dispara solo (v_0 −52 mV, umbral −45 mV, solo S recibe Poisson). En R3 S habla únicamente con D, así que lo que X dispare ahí lo origina D: 31 % de X en LC4 y 19 % en LPLC2; nada en LPLC1 ni en LPLC4. En el modelo, el 95–98 % restante de la entrada de X está callado salvo que S lo encienda; en la mosca tiene actividad propia. Qué enciende a X en la mosca: NO MEDIDO.

### Paso 3 · Quién lleva el freno (MEDIDO modelo, post hoc, no sellado)

Freno lineal = espigas medias × sinapsis X→D.

| Estímulo | X (nt) | Freno | C2/C0 | C4/C0 | R3/C0 | La enciende |
|---|---|---|---|---|---|---|
| LC4 | PVLP010 (glu), 1 | 72,5 % | 0,90 | 0,34 | 0,93 | DNp04, recurrente |
| LC4 | PVLP024 (GABA), 4 | 11,4 % | 0,00 | 1,17 | 0,00 | S directo |
| LC4 | LHAD1g1 (GABA), 1 | 2,1 % | 0,21 | 0,00 | 10,59 | casi callada, 1,9/s |
| LPLC2 | LHAD1g1 (GABA) | 30,6 % | 0,03 | 0,88 | 0,25 | S directo |
| LPLC2 | AVLP080 (GABA) | 20,0 % | 1,04 | 1,07 | 0,00 | otras vías desde S |
| LPLC2 | PVLP010 (glu) | 19,3 % | 1,11 | 0,43 | 1,08 | DNp04, recurrente |
| LPLC1 | AVLP080 (GABA) | 62,4 % | 0,96 | 0,99 | 0,00 | otras vías desde S |
| LPLC1 | PVLP010 (glu) | 21,7 % | 1,14 | 1,01 | 0,00 | otras vías desde S |
| LPLC1 | PVLP011 (GABA) | 9,5 % | 0,00 | 0,99 | 0,00 | S directo |
| LPLC4 | PS065 / PLP213 / PS002 | 30,5 % entre las tres, de 56 tipos | 0,33 / 0,04 / 0,71 | ≈ 1 | ≈ 0 | mezcla |

- Relevo DNp04→PVLP010. Con LC4, DNp04 dispara 107,3 por segundo y PVLP010 106,7. En el modelo el pico de una espiga es 0,1575 × w, con w = 0,275 mV por sinapsis: desde reposo, una sola neurona necesita 162 sinapsis para llevar a su blanco al umbral con una espiga, y DNp04→PVLP010 tiene 190 (8,23 mV contra 7 mV). Las 209 sinapsis de LC4 están repartidas en 50 neuronas, unas 4 cada una. Es una propiedad de la regla lineal de pesos de Shiu; en la mosca, NO MEDIDO.
- El proxy predice ΔSX/ΔX ≈ 1 − freno en C2: 0,28 / 0,35 / 0,12 / 0,41, contra 0,29 / 0,26 / 0,23 / 0,49 medidos. También predice M5 − C0 ≈ 2 × parte glutamatérgica × ΔX: 393 / 342 / 84 / 176, contra 371 / 265 / 84 / 113 medidos. La parte glutamatérgica del freno es 77,1 / 25,4 / 21,7 / 17,5 %.
- A quién frena (d_por_tipo.log). X veta a algunos D. Con LC4, al silenciar X: DNp06 0,0 → 61,7 por segundo, GF (DNp01) 53,8 → 116,0, DNg40 9,0 → 79,5; DNp04 casi no se mueve (107,3 → 109,4) y DNp35 baja (15,9 → 2,7). Con LPLC2: DNp06 1,6 → 127,9, DNp35 0,9 → 83,2, DNpe056 0,7 → 74,8, GF 102,5 → 142,1. Con LPLC1: DNp35 1,8 → 71,8. Con LPLC4: DNp05 5,5 → 71,3. DNp03 no dispara en ninguna condición con LPLC1 ni con LPLC4.
- Para Topo inverso: el ranking anatómico no predice quién frena. LHAD1g1 tiene 399 sinapsis sobre DNp06, pero con LC4 lleva el 2 % del freno; PVLP010 lleva el 72 %. El motivo S→X→D, tal como lo extrajimos, mezcla tres mecanismos: anticipatorio directo, anticipatorio por otras vías y recurrente a través de D.

### Paso 4 · Cortes y restauraciones (MEDIDO modelo, sellado)

D = suma de espigas por segundo sobre las neuronas D, media de 20 ensayos.

| Condición | LC4 | LPLC2 | LPLC1 | LPLC4 |
|---|---|---|---|---|
| C0 intacto | 373,45 | 592,7 | 81,3 | 1258,25 |
| C1 silenciar X | 628,15 | 1266,85 | 273,9 | 1762,2 |
| C2 cortar S→X | 446,95 | 767,95 | 126,0 | 1503,75 |
| C3 cortar X→D | 634,25 | 1075,05 | 291,1 | 1657,65 |
| C4 cortar S→D | 8,9 | 259,85 | 3,85 | 666,35 |
| R1 X solo con X→D | 320,15 | 613,95 | 47,2 | 904,95 |
| R2 X solo recibe de S | 476,25 | 900,15 | 241,6 | 1043,5 |
| R3 S solo con S→D | 364,7 | 559,7 | 313,2 | 1127,35 |
| R4 S con S→D y S→X | 274,35 | 293,15 | 240,9 | 833,05 |
| K inhibición fuera del motivo | 506,25 | 923,75 | 236,55 | 1496,2 |
| M5 glu → excitatoria | 744,55 | 857,3 | 165,4 | 1370,95 |

- C4: S→D es el motor de D. D cae 98 / 56 / 95 / 47 % y la mediana de la primera espiga pasa de 8,4 / 7,0 / 8,3 / 5,6 ms a 161,8 / 16,6 / 20,2 / 15,7 ms (latencias del agregado, no re-verificadas).
- C1 contra C3: X frena casi todo por sus sinapsis directas (72–109 % del efecto).
- C2: S→X directo carga 23–49 % del freno.
- R1 devuelve 97–170 % del freno (f_R1 1,209 / 0,968 / 1,177 / 1,701), porque X pierde también su inhibición mutua y dispara 1,36 / 1,55 / 1,21 / 1,59 veces lo de C0.
- R2 devuelve 0,596 / 0,544 / 0,168 / 1,426 del freno.
- R3 da 0,977 / 0,944 / 3,852 / 0,896 de la D intacta, y R4 da 0,735 / 0,495 / 2,963 / 0,662: el motivo mínimo no reproduce a D.
- K/X 0,521 / 0,491 / 0,806 / 0,472. Emparejado solo en LPLC1. Por unidad de impulso, K rinde 1,40 / 1,90 / 0,80 / 1,43 veces lo de X.
- Lo fuera del objetivo sube ×1,84 / ×2,10 / ×1,41 / ×2,14, 20 de 20, p exacto 1,9e-06.
- Ritmo, rel a 20 / 50 / 150 Hz: LC4 0,621 / 0,405 / 0,297, SUSTRACTIVA; LPLC2 0,598 / 0,532 / 0,338, DIVISIVA; LPLC1 0,860 / 0,703 / 0,393, SUSTRACTIVA; LPLC4 0,324 / 0,286 / 0,225, DIVISIVA.
- Réplica izquierda: P1 a P4 positivas 20 de 20 en los cuatro (p crudo 1,9e-06); ΔSX/ΔX 0,446 / 0,274 / 0,530 / 0,388.
- S queda idéntica en todas las condiciones salvo LPLC2: +3,31 % en C1, +1,70 % en C2 y +2,56 % en R1.

### Paso 5 · Mecanismos rivales

| Mecanismo | Predicción | Qué dio | Estado |
|---|---|---|---|
| M0, subproducto | silenciar X no mueve a D | D +40–237 %, 20/20 | REFUTADO en el modelo |
| M1, ganancia anticipatoria S→X→D | ΔSX/ΔX y ΔXD/ΔX ≥ 0,5 | X→D sí; S→X no | PARCIAL |
| M6, recurrente D→X→D (nueva, post hoc) | X cae con C4 y sobrevive en R3 | LC4: freno 47 % en C4 y 92 % en R3 | SUGERIDO en LC4 y en parte LPLC2; ausente en LPLC1 y LPLC4; falta prueba sellada |
| M2, ventana temporal | X corre la latencia | latencia igual con y sin X | NO SOSTENIDO, prueba débil (un solo tau) |
| M3, competencia por X compartidas | sube lo fuera del objetivo; K < X | ×1,41–2,14; X veta DNp06 | COMPATIBLE; competencia propiamente dicha NO MEDIDA |
| M4, compuerta de estado por AN_multi_11 | — | modelo sin estado | NO MEDIBLE |
| Compuerta de contexto | — | todo nace en S | NO MEDIBLE en el modelo |
| M5, glutamato excitatorio | M5 > C1 | LC4 sí (744,55 > 628,15); resto no | DECISIVO en LC4 |
| Identidad contra impulso | K emparejado ≈ X | ver K arriba | sin evidencia de que la identidad pese más que el impulso |
| Formación | — | — | NO MEDIDO |

### Paso 6 · Literatura

- Ache et al. 2019, Curr Biol: LC4 aporta la velocidad y LPLC2 el tamaño del looming en el GF. Textual: «the hyperpolarizing component derives from inhibitory GF input neurons independent from LPLC2 or LC4».
- Ache, Namiki, Lee, Branson y Card 2019, Nat Neurosci: DNp07 y DNp10 manejan el aterrizaje; el estado de vuelo compuerta su respuesta visual.
- Peek 2018 (tesis, U. Chicago, laboratorio Card): coactivar DNp02 y DNp04 da saltos hacia atrás; DNp11, hacia adelante. Namiki et al. 2018, eLife: DNp04 tiene dendritas en el glomérulo de LC4; colección split-GAL4 de descendentes.
- Croke et al. 2025, Curr Biol: DNp03 es hub de los giros ante looming; sus conexiones inhibitorias directas bajan la probabilidad de aterrizar.
- Transmisores (vía el agente de literatura, no releído hoy): Eckstein et al. 2024, 87 % de acierto por sinapsis y 94 % por neurona; PVLP010 glutamato con 54,5 %, LHAD1g1 GABA con 68,5 %; AN_multi_11 = AN06B009, GABA con 83,4 % en MANC (esto sí verificado antes); glutamato inhibitorio por GluClα (Liu y Wilson 2013).
- Sin manipulación publicada ni línea genética conocida para PVLP010, LHAD1g1, AVLP080 ni AN_multi_11.

### Paso 7 · Experimento en la mosca que decide (NO MEDIDO, propuesta)

Registro: GF y DNp06 en whole-cell durante looming, como en von Reyn 2014 y Ache 2019; GCaMP en DNp02, DNp11 y DNg40.

1. Signo del freno, sin líneas de X: RNAi de GluClα solo en el GF (y en DNp06) contra RNAi de Rdl solo en el GF.
2. Recurrencia: silenciar DNp04 (Kir2.1 o GtACR1) y registrar GF y DNp06. Acceso: DNp04 junto con DNp02 (Peek 2018); línea limpia solo de DNp04, NO VERIFICADA.
3. Estado: repetir 1 y 2 en vuelo y en reposo.

Qué decide: 1 y 2 positivos, freno recurrente glutamatérgico en la mosca; 1 positivo y 2 nulo, freno real encendido por otras vías; los dos nulos, el mecanismo del modelo no se traslada. Antes, en el modelo y sellado: H_MECANISMO_DNp04. Cortar solo DNp04→PVLP010 y silenciar de a uno PVLP010, LHAD1g1 y AVLP080. Predicción: D sin DNp04 sube en LC4 y LPLC2 y no en LPLC1 ni LPLC4, que no tienen a DNp04 en D y sirven de control negativo.

### Paso 8 · Mecanismo, función y formación

- Mecanismo: reconstruido en el modelo, arriba.
- Función: NO MEDIDA. Hipótesis: DNp04→PVLP010⊣GF/DNp06 como regla de selección entre programas de escape.
- Formación: NO MEDIDA.

### Cadena causal etiquetada

1. Looming → S: LITERATURA; en el modelo, supuesto (Poisson a 50 Hz).
2. S → D, excitación directa: MEDIDO anatomía, MEDIDO modelo (C4), LITERATURA.
3. S → X directo, la mitad de X y 23–49 % del freno: MEDIDO anatomía, MEDIDO modelo.
4. S → otras → X (AVLP080): MEDIDO modelo, post hoc.
5. S → DNp04 → PVLP010, relevo por 190 sinapsis: MEDIDO anatomía; MEDIDO modelo, post hoc; cuenta sobre las ecuaciones.
6. X ⊣ D por sinapsis directas, 72–109 % del efecto: MEDIDO modelo; transmisor, LITERATURA.
7. X ⊣ X: MEDIDO modelo (R1).
8. X ⊣ descendentes fuera del objetivo: MEDIDO modelo.
9. Signo de PVLP010: LITERATURA (54,5 %) más el contrafactual M5.
10. Todo en la mosca: NO MEDIDO.

### Apuestas

| # | Apuesta | p | Resultado |
|---|---|---|---|
| 1 | P1 pasa en los cuatro | 0,7 | GANADA, sin valor informativo por la exposición declarada |
| 2 | Global SOSTENIDA_EN_MODELO | 0,5 | PERDIDA: MIXTA; LPLC4, la que señalé como falla probable, quedó más cerca (0,487) |
| 3 | K/X ≥ 0,5 en al menos tres | 0,6 | PERDIDA: 2 de 4, con la premisa de emparejamiento caída en 3 de 4 |
| 4 | Fuera del objetivo sube con p < 0,05 en al menos tres | 0,6 | GANADA: 4 de 4 |
| 5 | SUSTRACTIVA en al menos tres | 0,55 | PERDIDA: 2 de 4 |
| 6 | M5 en LPLC4 > C1 | 0,55 | PERDIDA: 1370,95 < 1762,2 |

Brier 0,244, contra 0,25 de una moneda.

### Qué corregí antes de firmar

- La v1 del verificador reusaba en la línea FUERA la celda de LPLC4 para los cuatro estímulos, una variable vieja del primer lazo. Los cuatro daban C0=1228.2 C1=2631.2; lo cacé porque eran idénticos. La v2 recarga la celda de cada estímulo y coincide con el agregado en los cuatro.
- K no quedó emparejado en 3 de 4. Leer «K hace la mitad, así que la identidad de X importa» habría sido falso.
- La compuerta de contexto no se puede medir en un modelo donde toda la actividad nace en S.

## 4. Evidencia cruda

Comandos (brain-env, Python 3.12, directorio /workspace/mecanismo-2026-11-02):

```text
python3 -u verif_veredicto/verificar_veredicto.py --dir actions_correr2 --parquet /workspace/connectivity.parquet --comp shiu/Completeness_783.csv
python3 -u verif_veredicto/quien_mueve_x.py --dir actions_correr2 --parquet /workspace/connectivity.parquet --comp shiu/Completeness_783.csv
python3 verif_veredicto/d_por_tipo.py --dir actions_correr2 --comp shiu/Completeness_783.csv
```

Las cuatro líneas FUERA de la v1 defectuosa (verificacion_veredicto_v1_defectuosa.log, 5.149 bytes, sha256 cb530a7f8fd5af0a2e1ae707edf31bdf08f5df81fa81e5eb8adf328647a1caf4; queda en brain-env, no se publica):

```text
  FUERA LC4 C0=1228.2 C1=2631.2 cociente=2.14 positivos=20/20 p_exacto=1.91e-06 | IZQUIERDA P1 +283.9 20/20 p=1.9e-06; P2 +126.5 20/20 p=1.9e-06; P3 +307.6 20/20 p=1.9e-06; P4 +475.2 20/20 p=1.9e-06
  FUERA LPLC2 C0=1228.2 C1=2631.2 cociente=2.14 positivos=20/20 p_exacto=1.91e-06 | IZQUIERDA P1 +462.8 20/20 p=1.9e-06; P2 +126.8 20/20 p=1.9e-06; P3 +444.9 20/20 p=1.9e-06; P4 +404.6 20/20 p=1.9e-06
  FUERA LPLC1 C0=1228.2 C1=2631.2 cociente=2.14 positivos=20/20 p_exacto=1.91e-06 | IZQUIERDA P1 +73.2 20/20 p=1.9e-06; P2 +38.8 20/20 p=1.9e-06; P3 +241.9 20/20 p=1.9e-06; P4 +212.9 20/20 p=1.9e-06
  FUERA LPLC4 C0=1228.2 C1=2631.2 cociente=2.14 positivos=20/20 p_exacto=1.91e-06 | IZQUIERDA P1 +620.0 20/20 p=1.9e-06; P2 +240.8 20/20 p=1.9e-06; P3 +487.2 20/20 p=1.9e-06; P4 +798.1 20/20 p=1.9e-06
```

verificacion_veredicto.log (v2), completo:

```text
CTRL_MN9 ensayos_con_espiga=10 -> True (agregado True)
FILAS LC4 propias={"C1": 31422, "C2": 892, "C3": 232, "C4": 381, "R1": 31190, "R2": 33031, "R3": 6035, "R4": 5143, "M5": 37, "K": 23054} registradas_iguales=True K_reconstruido=True n_K=31 drive_x=99684.0 drive_k=37077.8 alcanzo=False X_inhibitorias=True X_glu=8
D_MEDIA LC4 {"C0": 373.45, "C1": 628.15, "C2": 446.95, "C3": 634.25, "C4": 8.9, "M5": 744.55, "R1": 320.15, "R2": 476.25, "R3": 364.7, "R4": 274.35, "K": 506.25} guardas=[]
FILAS LPLC2 propias={"C1": 15645, "C2": 724, "C3": 203, "C4": 908, "R1": 15442, "R2": 18538, "R3": 15463, "R4": 14739, "M5": 41, "K": 36458} registradas_iguales=True K_reconstruido=True n_K=52 drive_x=292356.2 drive_k=75488.1 alcanzo=False X_inhibitorias=True X_glu=4
D_MEDIA LPLC2 {"C0": 592.7, "C1": 1266.85, "C2": 767.95, "C3": 1075.05, "C4": 259.85, "M5": 857.3, "R1": 613.95, "R2": 900.15, "R3": 559.7, "R4": 293.15, "K": 923.75} guardas=[]
FILAS LPLC1 propias={"C1": 30861, "C2": 510, "C3": 89, "C4": 323, "R1": 30772, "R2": 29604, "R3": 12844, "R4": 12334, "M5": 11, "K": 10472} registradas_iguales=True K_reconstruido=True n_K=10 drive_x=117124.6 drive_k=118725.8 alcanzo=True X_inhibitorias=True X_glu=3
D_MEDIA LPLC1 {"C0": 81.3, "C1": 273.9, "C2": 126.0, "C3": 291.1, "C4": 3.85, "M5": 165.4, "R1": 47.2, "R2": 241.6, "R3": 313.2, "R4": 240.9, "K": 236.55} guardas=[]
FILAS LPLC4 propias={"C1": 42200, "C2": 1852, "C3": 560, "C4": 669, "R1": 41640, "R2": 43579, "R3": 12017, "R4": 10165, "M5": 210, "K": 36326} registradas_iguales=True K_reconstruido=True n_K=75 drive_x=178559.8 drive_k=59150.8 alcanzo=False X_inhibitorias=True X_glu=34
D_MEDIA LPLC4 {"C0": 1258.25, "C1": 1762.2, "C2": 1503.75, "C3": 1657.65, "C4": 666.35, "M5": 1370.95, "R1": 904.95, "R2": 1043.5, "R3": 1127.35, "R4": 833.05, "K": 1496.2} guardas=[]
  LC4 P1 media_dif=254.70 positivos=20/20 p_exacto=1.91e-06 p_holm=3.05e-05 pasa=True (agregado p=1e-05 pasa=True)
  LC4 P2 media_dif=73.50 positivos=20/20 p_exacto=1.91e-06 p_holm=3.05e-05 pasa=True (agregado p=2e-05 pasa=True)
  LC4 P3 media_dif=260.80 positivos=20/20 p_exacto=1.91e-06 p_holm=3.05e-05 pasa=True (agregado p=2e-05 pasa=True)
  LC4 P4 media_dif=364.55 positivos=20/20 p_exacto=1.91e-06 p_holm=3.05e-05 pasa=True (agregado p=2e-05 pasa=True)
VEREDICTO LC4 PARCIAL dSX/dX=0.2886 dXD/dX=1.0239 fR1=1.209 fR2=0.596 fR3=0.977 fR4=0.735 K/X=0.521 M5-C0=371.1 M5-C1=116.4 igual_al_agregado=True
  FUERA LC4 C0=336.60 C1=620.80 cociente=1.84 positivos=20/20 p_exacto=1.91e-06 (agregado C0=336.60 C1=620.80 igual=True) | IZQUIERDA P1 +283.9 20/20 p=1.9e-06; P2 +126.5 20/20 p=1.9e-06; P3 +307.6 20/20 p=1.9e-06; P4 +475.2 20/20 p=1.9e-06 | agregado_izq={"P1": {"media_dif": 283.85, "p_crudo": 1e-05}, "P2": {"media_dif": 126.5, "p_crudo": 1e-05}, "P3": {"media_dif": 307.6, "p_crudo": 1e-05}, "P4": {"media_dif": 475.25, "p_crudo": 1e-05}, "completa": true}
  LPLC2 P1 media_dif=674.15 positivos=20/20 p_exacto=1.91e-06 p_holm=3.05e-05 pasa=True (agregado p=1e-05 pasa=True)
  LPLC2 P2 media_dif=175.25 positivos=20/20 p_exacto=1.91e-06 p_holm=3.05e-05 pasa=True (agregado p=1e-05 pasa=True)
  LPLC2 P3 media_dif=482.35 positivos=20/20 p_exacto=1.91e-06 p_holm=3.05e-05 pasa=True (agregado p=1e-05 pasa=True)
  LPLC2 P4 media_dif=332.85 positivos=20/20 p_exacto=1.91e-06 p_holm=3.05e-05 pasa=True (agregado p=1e-05 pasa=True)
VEREDICTO LPLC2 PARCIAL dSX/dX=0.2600 dXD/dX=0.7155 fR1=0.968 fR2=0.544 fR3=0.944 fR4=0.495 K/X=0.491 M5-C0=264.6 M5-C1=-409.5 igual_al_agregado=True
  FUERA LPLC2 C0=998.90 C1=2102.45 cociente=2.10 positivos=20/20 p_exacto=1.91e-06 (agregado C0=998.90 C1=2102.45 igual=True) | IZQUIERDA P1 +462.8 20/20 p=1.9e-06; P2 +126.8 20/20 p=1.9e-06; P3 +444.9 20/20 p=1.9e-06; P4 +404.6 20/20 p=1.9e-06 | agregado_izq={"P1": {"media_dif": 462.75, "p_crudo": 1e-05}, "P2": {"media_dif": 126.75, "p_crudo": 1e-05}, "P3": {"media_dif": 444.95, "p_crudo": 2e-05}, "P4": {"media_dif": 404.55, "p_crudo": 2e-05}, "completa": true}
  LPLC1 P1 media_dif=192.60 positivos=20/20 p_exacto=1.91e-06 p_holm=3.05e-05 pasa=True (agregado p=1e-05 pasa=True)
  LPLC1 P2 media_dif=44.70 positivos=20/20 p_exacto=1.91e-06 p_holm=3.05e-05 pasa=True (agregado p=1e-05 pasa=True)
  LPLC1 P3 media_dif=209.80 positivos=20/20 p_exacto=1.91e-06 p_holm=3.05e-05 pasa=True (agregado p=1e-05 pasa=True)
  LPLC1 P4 media_dif=77.45 positivos=20/20 p_exacto=1.91e-06 p_holm=3.05e-05 pasa=True (agregado p=1e-05 pasa=True)
VEREDICTO LPLC1 PARCIAL dSX/dX=0.2321 dXD/dX=1.0893 fR1=1.177 fR2=0.168 fR3=3.852 fR4=2.963 K/X=0.806 M5-C0=84.1 M5-C1=-108.5 igual_al_agregado=True
  FUERA LPLC1 C0=2373.60 C1=3337.15 cociente=1.41 positivos=20/20 p_exacto=1.91e-06 (agregado C0=2373.60 C1=3337.15 igual=True) | IZQUIERDA P1 +73.2 20/20 p=1.9e-06; P2 +38.8 20/20 p=1.9e-06; P3 +241.9 20/20 p=1.9e-06; P4 +212.9 20/20 p=1.9e-06 | agregado_izq={"P1": {"media_dif": 73.25, "p_crudo": 1e-05}, "P2": {"media_dif": 38.8, "p_crudo": 1e-05}, "P3": {"media_dif": 241.95, "p_crudo": 1e-05}, "P4": {"media_dif": 212.95, "p_crudo": 1e-05}, "completa": true}
  LPLC4 P1 media_dif=503.95 positivos=20/20 p_exacto=1.91e-06 p_holm=3.05e-05 pasa=True (agregado p=2e-05 pasa=True)
  LPLC4 P2 media_dif=245.50 positivos=20/20 p_exacto=1.91e-06 p_holm=3.05e-05 pasa=True (agregado p=2e-05 pasa=True)
  LPLC4 P3 media_dif=399.40 positivos=20/20 p_exacto=1.91e-06 p_holm=3.05e-05 pasa=True (agregado p=1e-05 pasa=True)
  LPLC4 P4 media_dif=591.90 positivos=20/20 p_exacto=1.91e-06 p_holm=3.05e-05 pasa=True (agregado p=1e-05 pasa=True)
VEREDICTO LPLC4 PARCIAL dSX/dX=0.4872 dXD/dX=0.7925 fR1=1.701 fR2=1.426 fR3=0.896 fR4=0.662 K/X=0.472 M5-C0=112.7 M5-C1=-391.2 igual_al_agregado=True
  FUERA LPLC4 C0=1228.15 C1=2631.15 cociente=2.14 positivos=20/20 p_exacto=1.91e-06 (agregado C0=1228.15 C1=2631.15 igual=True) | IZQUIERDA P1 +620.0 20/20 p=1.9e-06; P2 +240.8 20/20 p=1.9e-06; P3 +487.2 20/20 p=1.9e-06; P4 +798.1 20/20 p=1.9e-06 | agregado_izq={"P1": {"media_dif": 620.05, "p_crudo": 1e-05}, "P2": {"media_dif": 240.8, "p_crudo": 1e-05}, "P3": {"media_dif": 487.25, "p_crudo": 2e-05}, "P4": {"media_dif": 798.1, "p_crudo": 2e-05}, "completa": true}
H_MECANISMO_PROPIO MIXTA (agregado MIXTA) filas_todas_iguales=True
```

quien_mueve_x.log y d_por_tipo.log están completos en la rama (60 y 50 líneas). Sus líneas de arranque, textuales:

```text
X LC4 suma_C0=575.50 (agregado 575.50) C0_a_igual_b=True espigas_rel={"C0": 1.0, "C2": 0.385, "C4": 0.763, "R2": 0.755, "R3": 0.306} freno_rel={"C0": 1.0, "C2": 0.724, "C4": 0.472, "R2": 0.557, "R3": 0.922} 1-dSX/dX=0.711
  ANAT LC4 sinapsis_S_a_X=3242 (0.015 de la entrada de X) sinapsis_D_a_X=1062 (0.0050) sinapsis_X_a_D=4017 freno_C0_glutamato=0.771
  TIPO LC4 PVLP010    n=1 nt=glutamate sin_X_a_D=677 espigas_C0=106.7 freno=0.725 acum=0.725 C2/C0=0.90 C4/C0=0.34 R3/C0=0.93 entrada_desde_S=0.023 desde_D=0.025
  D_A_X LC4 PVLP010 {"DNp04": 190, "DNp11": 8, "DNp01": 8, "DNg40": 5, "DNp06": 4, "DNp02": 4, "DNpe021": 4, "DNp35": 2, "DNp103": 1}
X LPLC2 suma_C0=776.25 (agregado 776.25) C0_a_igual_b=True espigas_rel={"C0": 1.0, "C2": 0.535, "C4": 0.869, "R2": 0.69, "R3": 0.194} freno_rel={"C0": 1.0, "C2": 0.647, "C4": 0.81, "R2": 0.61, "R3": 0.349} 1-dSX/dX=0.740
X LPLC1 suma_C0=554.60 (agregado 554.60) C0_a_igual_b=True espigas_rel={"C0": 1.0, "C2": 0.515, "C4": 0.988, "R2": 0.45, "R3": 0.0} freno_rel={"C0": 1.0, "C2": 0.881, "C4": 0.991, "R2": 0.173, "R3": 0.0} 1-dSX/dX=0.768
X LPLC4 suma_C0=2146.25 (agregado 2146.25) C0_a_igual_b=True espigas_rel={"C0": 1.0, "C2": 0.484, "C4": 0.951, "R2": 0.849, "R3": 0.016} freno_rel={"C0": 1.0, "C2": 0.591, "C4": 0.95, "R2": 1.487, "R3": 0.009} 1-dSX/dX=0.513
  LC4 DNp04    C0=107.3 C1=109.4 C3=109.6 C4=0.0
  LC4 DNp06    C0=0.0 C1=61.7 C3=57.8 C4=2.8
PSP pico = 0.15749 x w a los 9.24 ms; sinapsis minimas de una sola neurona para cruzar el umbral desde reposo = 162; 190 sinapsis dan 8.23 mV (umbral a 7.0 mV)
```

Lectura de vuelta desde GitHub, byte a byte contra brain-env: los seis archivos dan True.

| Archivo | Bytes | sha256 |
|---|---|---|
| verificar_veredicto.py | 9424 | 5569dab968f12f7236595035954737b20884712a8f1a2ca99b504b9291dd5ac9 |
| verificacion_veredicto.log | 6208 | ed77615abdb980ba0a3bb4707dbec0ae9d9574f97ecd2cc610524c7dd57119d3 |
| quien_mueve_x.py | 6123 | 70ccc8d17b2ab4661bbb3d3d2e22f314acfabec51d2bab092ab9b1ba5856f8d6 |
| quien_mueve_x.log | 8505 | 00045495c6c66bb9c57f829e1874ff4d99e1bc6fbccc3b9950e83faae8f40911 |
| d_por_tipo.py | 2586 | 8d144255a8f230f86790e43ebacee10d999988dec4e6025175f4e2babf1bbcd1 |
| d_por_tipo.log | 3021 | 9e5da319005eef10ce89122a8d296cf1b02cc09686a2d595bd6030ebc42e6133 |

Búsqueda web, lo que se usa textual: Peek 2018, «DNp11 activation generated forward jumps, whereas DNp02 and DNp04 co-activation induced backwards jumps»; Croke et al. 2025, «direct inhibitory connections from DNp03 reduce the likelihood a fly decides to land on, rather than turn away from, a looming object». La búsqueda de «PVLP010» no devolvió ningún trabajo sobre esa neurona.

## 5. Archivos generados

- titan/mecanismo-2026-11-02 @ 72e9eff: results/mecanismo_2026-11-02/verificacion_veredicto/verificar_veredicto.py, verificacion_veredicto.log, quien_mueve_x.py, quien_mueve_x.log.
- titan/mecanismo-2026-11-02 @ aaea8b6: results/mecanismo_2026-11-02/verificacion_veredicto/d_por_tipo.py, d_por_tipo.log.
- main: este archivo.
- ClickUp: página 2026-11-02-004 del Doc Topo inverso.

## 6. NO MEDIDO

- Nada de esto en la mosca.
- El efecto causal de cada tipo de X (PVLP010, LHAD1g1, AVLP080): solo hay proxy lineal.
- La ruta DNp04→PVLP010 como corte sellado (H_MECANISMO_DNp04 propuesta, sin sellar).
- K emparejado en LC4, LPLC2 y LPLC4: el sello no decía qué hacer si el pool activo se agotaba.
- El modelo sobre BANC; la robustez a w_syn, tau y umbral; los otros ritmos por tipo.
- Por qué DNp03 no dispara en el modelo.
- Función y formación.
- Las latencias: son del agregado y no las re-verifiqué.
- CONTEXTO-drosophila-fep.md: la 003 dijo que se actualizaba con esta lectura y sigue sin actualizar. Necesita un flujo documental que escriba en main; queda declarado como pendiente.

--- METODO PROMETEO ---
Accion delicada: NO. Lectura y verificacion de evidencia ya publicada, mas descriptivos post hoc; sin relanzar nada.
Modo aplicado: FULL.
Maquina: brain-env (2 CPU).
Instrumento con capacidad de dar rojo: verificador propio con permutacion exacta, filas y K rehechos desde el parquet; dio rojo una vez por un error mio y se corrigio.
NO MEDIDO declarado: la mosca, la causalidad por tipo, la ruta DNp04->PVLP010 como corte sellado, K emparejado en 3 de 4, BANC y robustez a parametros.
Review externo: no
