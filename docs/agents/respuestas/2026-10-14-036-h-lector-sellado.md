# 2026-10-14-036 · H_LECTOR sellado: la mosca va a leer con el mismo ridge que le ganó H_RIVAL, sobre sus 6 descendentes, contra el ridge crudo, sus líneas sin entrenar y 80 barajados

## Pedido
Abraham, 15-oct 09:52, ClickKit `sellar_lector_mosca`: «Sellá la mosca con lector entrenado».

## Veredicto primero
- [HECHO] **Sello en un commit aparte, antes de cualquier script:** rama `titan/lector-2026-10-15` desde `576fc4c`; commit `8e65e05` con un solo archivo, `tools/lector/SELLO-LECTOR.md` (md5 6e587be69bbffcdc25b98b4899579edd, 10.056 bytes), verificado desde un clon limpio.
- [SELLADO] **Lector:** el RIDGE de H_RIVAL sin cambios (`rival_mosca.py`, 774232f5), sobre las trazas de las 6 descendentes que devuelve `f2.sim_trozos` (40 pasos por 6, 240 rasgos, 94 veces menos que los 22.560 del ridge crudo), con la red elegida de H_TAU (tau de semilla 10).
- [SELLADO] **Tres hipótesis, margen de 1 punto:**
  - H_LECTOR_CERCA: no pierde más de 1 punto contra el RIDGE crudo (piso del IC de D1 mayor que -0,01).
  - H_LECTOR_PAGA: supera por más de 1 punto a las líneas sin entrenar (piso de D2 mayor que +0,01).
  - H_LECTOR_CABLEADO: con el mismo lector, el cableado real supera a 40 SL y 40 T (`nulos_r2.py` sin cambios, semillas [7, k] y [11, k]) en c2 y c5, prueba 12; p de 0,05 o menos y más de 1 punto en las 4 combinaciones (intersección-unión).
  - Primaria: bootstrap de las 10 semillas de prueba, B 20.000, semilla 2041, percentiles 2,5 y 97,5 (90% con Bonferroni por 2).
- [SELLADO] **Controles:** PIN, REPRO_W (las trazas reproducen exactas las 60 `pred_elegida`), REPRO_RIDGE (60 de 60), CONTROL_LECTOR_CRUDO (el lector sobre las entradas crudas da exactas las `pred_RIDGE` en c0, prueba 12), CONTROL_NEGATIVO (etiquetas permutadas, semilla 2043), NULOS_VALIDOS, REAL_EN_NULOS y GUARDA_FUGA.
- [DECLARADO] **Antecedente en contra:** en la entrada por tipos del 12-oct, con lector entrenado, el cableado no le ganó a SL ni a T en ninguna celda leída. Expectativa: CABLEADO probablemente REFUTADA; PAGA puede salir; CERCA abierta.
- [CORRECCIÓN] El encabezado del sello dice «10:00», pero el commit es de las 09:57:06: lo redondeé hacia adelante. El sello no se edita; manda la hora del commit.
- [NO MEDIDO] Ningún lector corrido, ningún acierto visto. El costo (unos 50 minutos por celda en la primaria y unos 10 por red y celda en los nulos, estimado desde H_TAU) lo mide el humo.

## Herramientas y máquina
- **brain-env.** Lectura de `factorial2_mosca.py` (la simulación devuelve las 6 descendentes), `nulos_r2.py`, los json de H_TAU (`elegida` = 10) y de H_RIVAL (`RIDGE` y `pred_RIDGE` por prueba), y de `results/entrada_por_tipos_2026-10-12/`. Prueba del parche en copia.
- **GitHub.** Rama, sello y push; md5 desde clon limpio.
- Acción delicada: ninguna (documento solo).

## Archivos
| Archivo | md5 |
|---|---|
| `tools/lector/SELLO-LECTOR.md` (`8e65e05`) | 6e587be69bbffcdc25b98b4899579edd |
| `tools/factorial3/nulos_r2.py` (pin) | c4f1c4d39c99f07cb9ad7977b6f3b01a |
| `tools/rival/rival_mosca.py` (pin) | 774232f5b4a53872a05f6a0f06015f34 |
| `results/rival_2026-10-15/MD5SUMS.txt` (pin) | 78477d7a099e3399333309126a42ee6d |
| `tools/contexto/actualizar_contexto_2026-10-14-036.py` (main, este commit) | 67fb49e714eb288c4f29ee576890979b |
| `.github/workflows/contexto-2026-10-14-036.yml` (se borra al aplicarse) | c1334efb5f96fd63bbc666f6e002ef70 |
| CONTEXTO antes y después del parche (probado en copia; la segunda aplicación aborta) | 933a87e30d03272e3525d35ad56a9a71 y b2b0b7724a23fb20b3865b9e230ef69f |

Doc de ClickUp: [036](https://app.clickup.com/90171457413/docs/2kza6fw5-22957).

## NO MEDIDO
- Todo acierto de H_LECTOR.
- El costo real en Actions y en brain-env.
- La réplica de H_RIVAL en brain-env sigue en curso (c0 terminado, c1 corriendo).

## Antes de firmar
| Afirmación | Instrumento | ¿Podía dar rojo? |
|---|---|---|
| El sello es anterior a cualquier script | el commit `8e65e05` trae un solo archivo | Sí |
| La simulación da las trazas de 6 descendentes | lectura de `f2.sim` (`out[:, t, :] = z[:, N - 6:]`) | Sí |
| H_RIVAL guarda lo que el pareo necesita | lectura de `rival_c0.json` (`RIDGE` y `pred_RIDGE` por prueba) | Sí |
| La hora del sello es la real | encabezado contra la hora del commit | Sí, y dio rojo: 10:00 contra 09:57, declarado |

--- METODO PROMETEO ---
Sellar antes de escribir el instrumento, con la expectativa en contra declarada. Pareo ensayo por ensayo con lo ya corrido. Ningún acierto antes del CORRER.
Máquina: brain-env y GitHub. Artefactos: el sello en su rama, este archivo en main y su Doc en ClickUp.
