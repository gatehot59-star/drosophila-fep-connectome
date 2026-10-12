# 2026-10-12-013: LPLC2 sí responde a objetos que pasan, y la mosca usa esa respuesta para esquivar en vuelo; la tarea de la 005 y la 012 castigaba a la mosca por hacer lo que hace

**Doc espejo:** https://app.clickup.com/90171457413/docs/2kza6fw5-21537
**Rama:** `titan/chequeo-dcmt-2026-10-12`: medición `6f53501` (script `tools/neurona_nueva/lplc2_salidas.py`, md5 `4012cbac716f6e812ac6158a57b15b5f`; log `results/chequeo_dcmt_2026-10-12/lplc2.log`, md5 `f185938782a67969efb30222de870ebe`, 58 líneas). Sin PR.

## Veredicto (conclusión)

- [LITERATURA, leída hoy] El supuesto de la 005 (LPLC2 responde a un objeto que pasa) es **cualitativamente cierto**: «LPLC2 neurons responded not only to a looming disc but also to a translating spot both at high and low velocities» (Kim 2023). Su forma en la 005 no: en la mosca la respuesta es **direccional** (más a lo que va de atrás hacia adelante, vía T4/T5) y su amplitud **no está sostenida como número** por ninguna fuente leída (Klapoetke 2017 y 2022 la ven nula o chica).
- [LITERATURA] La mosca **usa** esa respuesta para **esquivar en vuelo**: LPLC2 y DNp06 «underlie evasive flight turns in response to laterally moving or approaching visual objects» (Kim 2023). Silenciar LPLC2 baja casi a la mitad el giro ante un punto que pasa.
- [LITERATURA] El mismo looming da **despegue sólo posada** y **aterrizaje sólo en vuelo** (Ache 2019, Nature Neuroscience).
- [MEDIDO, FlyWire v783] LPLC2 le habla a DNp06 casi tanto como a la fibra gigante: **1.003 sinapsis desde 200 LPLC2** contra **1.080 desde 189** (con ≥ 5 por par, 725 desde 88 contra 844 desde 99). A DNp07 y DNp10, 0. Todo del mismo lado.
- [MEDIDO] El motivo de 28 de la 003 usa **8 de las 210 LPLC2** (4 por lado) y **no tiene DNp06**.
- [CONCLUSIÓN] La tarea de la 005, heredada por la 012, etiqueta «pasa en vuelo → nada», y la 012 lee la amenaza en vuelo por la línea de DNp01 (fibra gigante). Las dos cosas van contra lo que hace la mosca. El NO PAGAN de la 012 es una medición válida **de esa tarea**, no prueba de que el cableado no sirve. **No ampliar el motivo antes de corregir la tarea.**

## 1. Pedido

17:59: «Verificá la fisiología real de LPLC2 antes de ampliar el motivo».

## 2. Herramientas y máquina

- **Web (sólo lectura):** Klapoetke 2017 (Nature 551:237-241), Klapoetke 2022 (Neuron 110:1700-1711), Kim, Park, Lee y Kim 2023 (Current Biology 33:321-335, doi 10.1016/j.cub.2022.12.014), Ache 2019 (Current Biology 29), Ache 2019 (Nature Neuroscience 22:1132-1139) y una revisión de 2022 en Frontiers.
- **brain-env:** `lplc2_salidas.py`, sólo lectura de los datos pinneados (3,3 s, `EXIT_RUN=0`).
- **Sandbox de ClickUp:** escritura del script y reconstrucción del log para subirlo (md5 igual al de brain-env).
- **GitHub MCP:** push `6f53501` a `titan/chequeo-dcmt-2026-10-12`; lectura de `entrada_por_tipos.py` (`f7844be`), `lineas_etiquetadas.py` (`debfd05`) y la 003 para citar la tarea y el motivo; este archivo a `main`.
- **ClickUp:** Doc público nuevo https://app.clickup.com/90171457413/docs/2kza6fw5-21537. Actions y Kaggle sin uso; sin cuota ajena.

## 3. Qué se midió

### 3.1 Fisiología (citas textuales)

- **Klapoetke 2017, Nature 551:237-241:** LPLC2 es «non-responsive to related patterns of motion such as contraction, wide-field rotation or luminance change»; a la traslación de campo amplio (barras de 10° a 20°/s) no responde, y a una expansión descentrada responde menos que a una centrada.
- **Klapoetke 2022, Neuron 110:1700-1711:** «Due to small responses to moving bars, we did not run directional and speed tuning for LPLC2». LPLC2 queda en el grupo «primariamente looming».
- **Kim 2023, Current Biology 33:321-335** («A visuomotor circuit for evasive flight turns in Drosophila»): «LPLC2 neurons responded not only to a looming disc but also to a translating spot both at high and low velocities»; «the response amplitude was almost identical for the entire velocity range»; responde más a lo que va de atrás hacia adelante que al revés (eso depende de T4/T5) y de forma tónica. LPLC2 se registró en moscas **sin volar**. Silenciar LPLC2 baja casi a la mitad el giro evasivo ante un punto que pasa; **DNp06** hereda la selectividad, con respuesta fásica. Resumen: «a pair of visual projection neurons (LPLC2) and descending neurons (DNp06) that underlie evasive flight turns in response to laterally moving or approaching visual objects».
- **Ache 2019, Current Biology 29:** la fibra gigante suma velocidad (de LC4) y una gaussiana de tamaño (de LPLC2).
- **Ache 2019, Nature Neuroscience 22:1132-1139:** «landing responses were only evoked in flight, whereas escape-related leg movements were only evoked in non-flying flies». DNp07 y DNp10 responden más a barras oscuras que van de adelante hacia atrás del mismo lado, y sus respuestas «are severely attenuated during non-flight periods»; «Octopamine exposure mimics flight effects in one».
- **LPLC4:** sin fisiología encontrada; la revisión de 2022 dice que sus propiedades visuales «are yet to be characterized».

### 3.2 FlyWire v783 (`lplc2_salidas.py`)

Sinapsis sumadas sin umbral; entre paréntesis, neuronas presinápticas y porcentaje de la entrada total de las dos neuronas de ese tipo (izquierda más derecha). Fracción ipsilateral 1,000 en todas las filas no nulas.

| De | a DNp01 (fibra gigante) | a DNp06 (giro evasivo) | a DNp07 (aterrizaje) | a DNp10 | a DNp04 |
|---|---|---|---|---|---|
| LPLC2 (108 + 102 = 210) | 1.080 (189; 11,4%) | 1.003 (200; 4,6%) | 0 | 0 | 1.212 (197; 21,9%) |
| LC4 (54 + 50 = 104) | 805 (104; 8,5%) | 163 (70; 0,7%) | 1 (1; 0,0%) | 0 | 1.854 (104; 33,5%) |
| LPLC4 (56 + 54 = 110) | 0 | 1 (1; 0,0%) | 1.448 (92; 16,6%) | 22 (12; 0,2%) | 0 |

Con ≥ 5 sinapsis por par: LPLC2 → DNp01 844 (99), → DNp06 725 (88), → DNp04 1.007 (119); LC4 → DNp01 757 (89), → DNp06 50 (9); LPLC4 → DNp07 1.408 (73), → DNp10 6 (1).

### 3.3 Qué dice la tarea (leído en el código sellado)

`tools/escape_aterrizaje/entrada_por_tipos.py` (`f7844be`), docstring:

```text
Tarea de robot inspirada en la mosca (no es una afirmacion sobre la conducta de la mosca): amenaza rapida
(l/v 10 a 30 ms), acercamiento lento (l/v 150 a 300 ms) u objeto que pasa sin acercarse, por un lado.
  vuelo: amenaza -> escapar hacia el otro lado (1 de la izq, 2 de la der); acercamiento -> aterrizar (3);
         pasa -> nada (0).
  piso:  amenaza -> escapar (1, 2); acercamiento -> nada (0); pasa -> nada (0).
```

Etiqueta y respuesta de LPLC2 en el código:

```text
    y = np.where(est == 0, 1 + lado, np.where((est == 1) & vuelo, 3, 0))
    lplc2 = np.where(expande, g, 0.0) + np.where(hay_punto, F_PUNTO * g, 0.0)
F_PUNTO, F_LC4_PUNTO = 0.6, 0.1
TH_MAX, V_REF, TH_P, TH_S = 100.0, 15.0, 50.0, 20.0
```

La respuesta al punto es `F_PUNTO * g` (gaussiana del tamaño), igual para cualquier sentido de movimiento.

`tools/escape_aterrizaje/lineas_etiquetadas.py` (`debfd05`), docstring y código:

```text
  lineas = [DNp01 izq, DNp01 der, DNp07 izq, DNp07 der] -> [escapar de la izq (1), de la der (2),
  aterrizar (3), aterrizar (3)].
    assert all(t in TIPOS for t in tipos[:nv]) and tipos[nv:] == ["DNp01", "DNp01", "DNp07", "DNp07"]
        m = ete["est"] == 2
        return float((p[m] != 0).mean())
```

En vuelo compiten las cuatro líneas, así que la amenaza en vuelo se lee por DNp01; cualquier acción ante el objeto que pasa cuenta como falsa alarma.

Composición del motivo (003, §3.1): «Por lado, las 4 LC4 y las 4 LPLC2 con más sinapsis sobre DNp01 y las 4 LPLC4 con más sinapsis sobre DNp07; DNp01 y DNp07 de cada lado.»

## 4. Evidencia cruda (verbatim)

Comando en brain-env: el script sin argumentos (rutas fijas `/workspace/connectivity.parquet` y `/workspace/annotations.tsv`; sale con 2 si los md5 no son los del pin), salida a `lplc2.log`. Log completo (md5 `f185938782a67969efb30222de870ebe`, 58 líneas):

```text
# maquina: 6c09d8604b07 | Linux-4.19.0-27-amd64-x86_64-with-glibc2.41 | numpy 2.5.3 | pandas 3.0.5
# md5 script = 4012cbac716f6e812ac6158a57b15b5f
# fecha: 2026-10-12 21:02:37 +0000
# md5 conn = 3d802fd542b5d18570ba1ba0bb0abed9 | md5 annot = 719904abad876c68ace1b5690c9b9b63
CUENTA tipo=LPLC2 por_lado={'left': 108, 'right': 102}
CUENTA tipo=LC4 por_lado={'left': 54, 'right': 50}
CUENTA tipo=LPLC4 por_lado={'left': 56, 'right': 54}
CUENTA tipo=DNp01 por_lado={'right': 1, 'left': 1}
CUENTA tipo=DNp06 por_lado={'right': 1, 'left': 1}
CUENTA tipo=DNp07 por_lado={'right': 1, 'left': 1}
CUENTA tipo=DNp10 por_lado={'left': 1, 'right': 1}
CUENTA tipo=DNp11 por_lado={'right': 1, 'left': 1}
CUENTA tipo=DNp02 por_lado={'left': 1, 'right': 1}
CUENTA tipo=DNp04 por_lado={'left': 1, 'right': 1}
SALIDA pre=LPLC2 umbral>=1 dn=DNp01 sinapsis=1080 (11.4% de la entrada de DNp01) pares=189 presinapticas=189 ipsilaterales=1.000
SALIDA pre=LPLC2 umbral>=1 dn=DNp06 sinapsis=1003 (4.6% de la entrada de DNp06) pares=200 presinapticas=200 ipsilaterales=1.000
SALIDA pre=LPLC2 umbral>=1 dn=DNp07 sinapsis=0 pares=0
SALIDA pre=LPLC2 umbral>=1 dn=DNp10 sinapsis=0 pares=0
SALIDA pre=LPLC2 umbral>=1 dn=DNp11 sinapsis=19 (0.2% de la entrada de DNp11) pares=13 presinapticas=13 ipsilaterales=1.000
SALIDA pre=LPLC2 umbral>=1 dn=DNp02 sinapsis=5 (0.1% de la entrada de DNp02) pares=3 presinapticas=3 ipsilaterales=1.000
SALIDA pre=LPLC2 umbral>=1 dn=DNp04 sinapsis=1212 (21.9% de la entrada de DNp04) pares=197 presinapticas=197 ipsilaterales=1.000
SALIDA pre=LPLC2 umbral>=5 dn=DNp01 sinapsis=844 (8.9% de la entrada de DNp01) pares=99 presinapticas=99 ipsilaterales=1.000
SALIDA pre=LPLC2 umbral>=5 dn=DNp06 sinapsis=725 (3.3% de la entrada de DNp06) pares=88 presinapticas=88 ipsilaterales=1.000
SALIDA pre=LPLC2 umbral>=5 dn=DNp07 sinapsis=0 pares=0
SALIDA pre=LPLC2 umbral>=5 dn=DNp10 sinapsis=0 pares=0
SALIDA pre=LPLC2 umbral>=5 dn=DNp11 sinapsis=0 pares=0
SALIDA pre=LPLC2 umbral>=5 dn=DNp02 sinapsis=0 pares=0
SALIDA pre=LPLC2 umbral>=5 dn=DNp04 sinapsis=1007 (18.2% de la entrada de DNp04) pares=119 presinapticas=119 ipsilaterales=1.000
SALIDA pre=LC4 umbral>=1 dn=DNp01 sinapsis=805 (8.5% de la entrada de DNp01) pares=104 presinapticas=104 ipsilaterales=1.000
SALIDA pre=LC4 umbral>=1 dn=DNp06 sinapsis=163 (0.7% de la entrada de DNp06) pares=70 presinapticas=70 ipsilaterales=1.000
SALIDA pre=LC4 umbral>=1 dn=DNp07 sinapsis=1 (0.0% de la entrada de DNp07) pares=1 presinapticas=1 ipsilaterales=1.000
SALIDA pre=LC4 umbral>=1 dn=DNp10 sinapsis=0 pares=0
SALIDA pre=LC4 umbral>=1 dn=DNp11 sinapsis=923 (11.1% de la entrada de DNp11) pares=92 presinapticas=92 ipsilaterales=1.000
SALIDA pre=LC4 umbral>=1 dn=DNp02 sinapsis=1001 (18.6% de la entrada de DNp02) pares=102 presinapticas=102 ipsilaterales=1.000
SALIDA pre=LC4 umbral>=1 dn=DNp04 sinapsis=1854 (33.5% de la entrada de DNp04) pares=104 presinapticas=104 ipsilaterales=1.000
SALIDA pre=LC4 umbral>=5 dn=DNp01 sinapsis=757 (8.0% de la entrada de DNp01) pares=89 presinapticas=89 ipsilaterales=1.000
SALIDA pre=LC4 umbral>=5 dn=DNp06 sinapsis=50 (0.2% de la entrada de DNp06) pares=9 presinapticas=9 ipsilaterales=1.000
SALIDA pre=LC4 umbral>=5 dn=DNp07 sinapsis=0 pares=0
SALIDA pre=LC4 umbral>=5 dn=DNp10 sinapsis=0 pares=0
SALIDA pre=LC4 umbral>=5 dn=DNp11 sinapsis=860 (10.3% de la entrada de DNp11) pares=63 presinapticas=63 ipsilaterales=1.000
SALIDA pre=LC4 umbral>=5 dn=DNp02 sinapsis=962 (17.9% de la entrada de DNp02) pares=90 presinapticas=90 ipsilaterales=1.000
SALIDA pre=LC4 umbral>=5 dn=DNp04 sinapsis=1850 (33.4% de la entrada de DNp04) pares=103 presinapticas=103 ipsilaterales=1.000
SALIDA pre=LPLC4 umbral>=1 dn=DNp01 sinapsis=0 pares=0
SALIDA pre=LPLC4 umbral>=1 dn=DNp06 sinapsis=1 (0.0% de la entrada de DNp06) pares=1 presinapticas=1 ipsilaterales=1.000
SALIDA pre=LPLC4 umbral>=1 dn=DNp07 sinapsis=1448 (16.6% de la entrada de DNp07) pares=92 presinapticas=92 ipsilaterales=1.000
SALIDA pre=LPLC4 umbral>=1 dn=DNp10 sinapsis=22 (0.2% de la entrada de DNp10) pares=12 presinapticas=12 ipsilaterales=1.000
SALIDA pre=LPLC4 umbral>=1 dn=DNp11 sinapsis=136 (1.6% de la entrada de DNp11) pares=22 presinapticas=22 ipsilaterales=1.000
SALIDA pre=LPLC4 umbral>=1 dn=DNp02 sinapsis=0 pares=0
SALIDA pre=LPLC4 umbral>=1 dn=DNp04 sinapsis=0 pares=0
SALIDA pre=LPLC4 umbral>=5 dn=DNp01 sinapsis=0 pares=0
SALIDA pre=LPLC4 umbral>=5 dn=DNp06 sinapsis=0 pares=0
SALIDA pre=LPLC4 umbral>=5 dn=DNp07 sinapsis=1408 (16.2% de la entrada de DNp07) pares=73 presinapticas=73 ipsilaterales=1.000
SALIDA pre=LPLC4 umbral>=5 dn=DNp10 sinapsis=6 (0.1% de la entrada de DNp10) pares=1 presinapticas=1 ipsilaterales=1.000
SALIDA pre=LPLC4 umbral>=5 dn=DNp11 sinapsis=108 (1.3% de la entrada de DNp11) pares=12 presinapticas=12 ipsilaterales=1.000
SALIDA pre=LPLC4 umbral>=5 dn=DNp02 sinapsis=0 pares=0
SALIDA pre=LPLC4 umbral>=5 dn=DNp04 sinapsis=0 pares=0
# duracion_s=3.3
EXIT_RUN=0
```

Recomputable: `git checkout 6f53501 && python3 tools/neurona_nueva/lplc2_salidas.py` con los datos pinneados en `/workspace`.

## 5. Qué cambia

- **El 0,6 de la 005:** acierta en que LPLC2 responde a lo que pasa, pero la pone sin dirección y con una amplitud que ninguna fuente leída sostiene como número (Kim no la da en el texto leído; Klapoetke la ve chica o nula). Tiene que ser direccional y barrida, no fija.
- **La tarea y su lectura van contra la mosca:** «pasa en vuelo → nada», cuando la mosca gira para esquivar lo que pasa (Kim 2023); y la 012 lee la amenaza en vuelo por DNp01, cuando el despegue de la fibra gigante sólo ocurre posada (Ache 2019). En vuelo la evasión va por DNp06, que falta en el motivo.
- **La 012 queda como medición válida de una tarea mal etiquetada.** Cuadra con su D2 post hoc: sin la respuesta al punto (`F_PUNTO = 0`), W subía a 0,6206 y empataba con SL.
- **La 005 lo había declarado** («no es una afirmacion sobre la conducta de la mosca»). El problema no es de honestidad sino de juez: con esa tarea, que la mosca responda a lo que pasa cuenta como falsa alarma.

## 6. Propuesta (decide Abraham, nada corrido)

Rehacer la tarea con las etiquetas de la mosca **antes** de ampliar el motivo:

1. Agregar DNp06 de cada lado, con sus LPLC2 (hoy 200 de las 210 le hablan).
2. Líneas por estado: posada, DNp01 → despegue; en vuelo, DNp06 → giro hacia el otro lado y DNp07 → aterrizaje.
3. Objeto que pasa en vuelo → giro, no «nada».
4. Respuesta de LPLC2 al punto direccional (más de atrás hacia adelante), con amplitud barrida {0; 0,3; 0,6} declarada.
5. Mismos nulos SL y T, misma regla a mano, sellado antes de correr.

**Falsador:** con la tarea de la mosca, W no le gana a SL ni a T con Holm.

## 7. Archivos

- `main`: este archivo.
- Rama `titan/chequeo-dcmt-2026-10-12` (`6f53501`): `tools/neurona_nueva/lplc2_salidas.py` y `results/chequeo_dcmt_2026-10-12/lplc2.log`.
- ClickUp: Doc público https://app.clickup.com/90171457413/docs/2kza6fw5-21537.

## 8. NO MEDIDO

- La relación punto/looming de LPLC2 (figura 4E de Kim 2023, no leída): es el número que reemplazaría al 0,6.
- Los parámetros de la gaussiana de tamaño de la 005 (`TH_P` 50°, `TH_S` 20°) contra Ache 2019.
- LPLC2 en vuelo: Kim la registró en moscas sin volar, y Ache 2019 muestra que el vuelo cambia las respuestas de otras descendentes.
- Qué pasa en Kim 2023 al inactivar DNp01 y DNp04 (la frase quedó cortada en lo leído).
- La fibra gigante ante objetos que pasan.
- La fisiología de LPLC4.
- La tarea corregida y el motivo ampliado: nada corrido.
- La entrada total de DNp01 da 9.407 en la exploración de la 003 y 9.474 en la 011 (4.327 + 5.147); el 11,4% de hoy cuadra con 9.474. La diferencia (67 sinapsis) no está explicada y no mueve ningún porcentaje más de 0,1 punto.
- Segunda máquina. CONTEXTO sin reescribir: de la 011 a la 013 vive en sus respuestas.

## Antes de firmar

```text
"LPLC2 responde a lo que pasa"             → texto de Kim 2023                       → podía dar rojo: SÍ (Klapoetke 2022 la ve chica) → bien, cualitativo; amplitud NO MEDIDA
"esa respuesta es direccional"             → texto de Kim 2023                       → podía dar rojo: SÍ                              → bien
"la mosca la usa para esquivar en vuelo"   → resumen y silenciamiento de Kim 2023    → podía dar rojo: SÍ                              → bien (literatura, no medición nuestra)
"LPLC2 llega a DNp06 casi como a DNp01"    → lplc2_salidas.py sobre v783             → podía dar rojo: SÍ (a DNp07 y DNp10 dio 0)      → medido, bien
"el motivo no tiene DNp06"                 → diseño de la 003 y assert de la 012      → podía dar rojo: SÍ                              → medido
"la tarea va contra la mosca"              → código sellado contra la literatura    → podía dar rojo: SÍ (si las etiquetas fueran otras) → bien
"el cableado paga con la tarea de la mosca" → nada corrido                           → podía dar rojo: NO                              → NO MEDIDO
```

--- METODO PROMETEO ---
Acción delicada: NO
Máquina: brain-env (lplc2_salidas.py, 3,3 s, EXIT_RUN=0) + sandbox de ClickUp + GitHub y web
Artefactos: docs/agents/respuestas/2026-10-12-013-lplc2-responde-a-lo-que-pasa-y-la-mosca-lo-usa-para-esquivar.md + https://app.clickup.com/90171457413/docs/2kza6fw5-21537
