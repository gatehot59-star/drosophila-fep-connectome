# SELLO · H_TOPO_NUEVO con la barra según su dirección (respuesta 2026-10-14-012)

**Pedido.** Abraham, 14-oct 13:07: «Dale con la barra según su dirección» (antes, ClickKit `topo_nuevo_barra_011`).

## Por qué no la barra sola
La barra que va de adelante hacia atrás ya estaba en la tarea sellada de la 015, etiquetada «aterrizar» en vuelo. En el modelo de entrada, LPLC4 responde a esa barra, y la línea de aterrizaje de `escape.topo` lee LPLC4. Sellarla como «nueva» hubiera sido una prueba que no puede dar rojo. Lo nuevo es la **dirección**: la barra que va de atrás hacia adelante (AD).

## Orden del sello (verificable en git)
| Paso | Commit | Qué | md5 |
|---|---|---|---|
| A | `42d2f60` | La tarea: etiquetas y modelo de entrada desde la literatura, antes del programa | `tarea_barra_dir.py` d25153570edff8dfc249945c88cd7d4c |
| B | `2deb335` | El programa Topo nuevo, antes de cualquier corrida del banco | `aterrizaje_dir.topo` 0122a4ce64884010e8bb741bb57f2e29 |
| C | `8c7cf1b` | El banco y los workflows | `banco_barra_dir.py` c033f214869b5b7776a26afad3c744a5; `barra-dir-mosca.yml` 758715aa8c1afcd54298dff1a79f4be2; `barra-dir-humo.yml` c1d05b7847bbaa94cb3ce54b42bcbff8 |

Sin cambios: `tarea_mosca.py` 40d64e07, `escape_aterrizaje_dbc3.py` 4d40477d, `entrada_por_tipos.py` e060c4bf, `topo.py` 9abefe9d, `escape.topo` dae4967d.

## Etiquetas y fuentes
- **En vuelo, barra de adelante hacia atrás → aterrizar.** Ache 2019, *Nat Neurosci*: «silencing DNp07 or DNp10 [...] significantly reduced landing response rates to unilateral, front-to-back moving bars».
- **En vuelo, barra de atrás hacia adelante → girar alejándose. Etiqueta nueva, con fuente indirecta.**
  - Ache 2019, Supp Fig 5d: las descendentes de aterrizaje tienen sintonía de dirección; «movements in other directions [...] were less effective».
  - Kim 2023, *Curr Biol*: LPLC2 y DNp06 median giros evasivos ante objetos que se mueven de costado, y «Direction-selective responses to the bar were observed» en DNp06.
  - La conducta exacta ante esa barra no está medida como número en lo leído.
- **Posada, cualquier barra → nada.** Etiqueta de trabajo, como en la 015.

## Modelo de entrada para barras (supuestos declarados)
- **LPLC2:** amplitud A de la celda; atrás hacia adelante 1, adelante hacia atrás F_DIR = 0,5 (Kim 2023: «stronger responses to back-to-front motion than to front-to-back motion for both bars and spots»).
- **LPLC1:** atrás hacia adelante 1, adelante hacia atrás 0,5 (Kim 2023, citando su ref. 34).
- **LPLC4:** adelante hacia atrás 1 y atrás hacia adelante F4_AD = 0,3. Inferido de la sintonía de DNp07 (su primera entrada es LPLC4). **Es el supuesto más débil.**
- **Chequeo:** con las barras nuevas apagadas, la entrada es exactamente la de la 015 (SINTONIAS_015_IGUAL).

## El programa nuevo
Es igual a `escape.topo`, salvo que aterrizar = media(LPLC4) − media(LPLC1) del mismo lado. Las vías no cambian: en FlyWire v783, LPLC1 no tiene sinapsis directas sobre DNp07 (2026-10-12-014). Por eso el cableado que baja es el mismo motivo de 46 neuronas.

## Hipótesis (margen 0,01, alfa 0,05)
- **H_TN_CABLEADO:**
  - W le gana a 300 SL y a 300 T en acierto en las 6 celdas, con Holm sobre 12 pruebas (el mínimo posible es 0,0399).
  - Se sostiene si las 12 dan menos de 0,05; si no, queda refutada.
- **H_TN_REGLA:**
  - d = acierto de la regla nueva menos acierto de W, en 12.000 ensayos, con un IC90 bootstrap estratificado por celda (B = 20.000).
  - Se sostiene si el límite inferior es mayor que −0,01; queda refutada si el superior es menor que −0,01; si no, SIN_DECIDIR.
- **H_TOPO_NUEVO:** se sostiene si se sostienen las dos; queda refutada si alguna lo está.
- **Descriptivo, sin veredicto:** la regla vieja contra la nueva; aciertos en barras AA y AD en vuelo.

## Humo
- **brain-env, 13:15 (3 nulos, 600/400, B = 2.000).** Log md5 `55761c49240c9d51d7cb2c2fd270b3cc`.
  - Controles: VEREDICTO_TAREA VALIDA, REPRODUCE_M46 True, guardas SL y T True, EXIT_RUN=0, 40,8 s.
  - El veredicto de humo es REFUTADA, mecánicamente: con 3 nulos el p mínimo es 0,25.
  - **Declarado:** vi los números del humo antes de sellar, y no cambié nada de A, B ni C después de verlos.
- **Actions x64:** se dispara con `results/topo_barra_2026-10-14_humo/HUMO`, en este mismo commit.

## Disparo
La corrida completa (unas 1,5 h estimadas en un solo trabajo) **solo** se dispara al pushear `results/topo_barra_2026-10-14/CORRER`, con el sí de Abraham.
