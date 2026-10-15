# 2026-10-14-029 · H_REUSO sellado: si la misma pieza de freno sirve a varias acciones, en FlyWire y otra vez en BANC, sin haber mirado el resultado

## Pedido
Abraham, 14-oct 21:20, ClickKit `sellar_reuso_028`: «Sellá H_REUSO (FlyWire y BANC)».

## Veredicto primero
- [SELLADO] H_REUSO en `titan/reuso-2026-10-14`. Instrumento, prueba y workflows en `613317d`, antes de ver un solo resultado. Sello, humo y disparo en `5ef2a63` (`tools/reuso/SELLO-REUSO.md`).
- [SELLADO] **La plantilla:**
  - Un sensor visual le da 20 sinapsis o más a una descendente de su mismo lado.
  - Una inhibitoria recibe 5 o más de ese sensor y le da 5 o más a esa descendente.
  - **T1:** cuántos pares la tienen.
  - **T2:** cuántas inhibitorias la hacen para dos o más tipos de descendente.
- [SELLADO] **El contraste:** contra 200 barajados por conectoma, que conservan las aristas por neurona, los lados, los pesos y los signos. Holm sobre las 4 pruebas. Se sostiene si pasa en FlyWire y otra vez en BANC; si en BANC no aparece, queda NO_SE_REPLICA.
- [MEDIDO] La prueba con grafos de juguete da 7/7. Dio rojo una vez, por un error de la prueba misma; lo corregí antes de tocar datos reales.
- [MEDIDO] **El humo fue ciego:** no imprime T1, T2 ni p, y no los vi. Los controles y las guardas pasan en los dos conectomas: FlyWire, 996 pares cableados; BANC, 753. Cada barajado tarda unos 5 s.
- [MEDIDO, de paso] El control de BANC mostró que **LHAD1g1 también está entre las inhibitorias de LPLC2 a DNp06 en BANC**, en los dos lados. Esa pieza se repite en el otro animal. Es un solo caso, no la hipótesis.
- [NO MEDIDO] T1, T2 y el veredicto. La corrida espera el `CORRER` (unos 40 minutos en brain-env).

## Herramientas y máquina
- brain-env (Python 3.12.14, numpy 2.5.3, pandas 3.0.5, 7,8 GB de memoria): estructura de BANC (los ids de las aristas son `root_888`, como texto, y el 100 % está en el meta), la prueba y el humo ciego.
- GitHub: rama nueva desde main y md5 verificados desde un clon limpio.
- El humo en Actions ya está disparado. Baja BANC del bucket público por HTTPS.
- Acción delicada: ninguna.

## Archivos
| Archivo (rama `titan/reuso-2026-10-14`) | md5 |
|---|---|
| `tools/reuso/reuso_mosca.py` | e9a07a7c58d926c00fec9c64cf4eb253 |
| `tools/reuso/prueba_reuso.py` | 2a00e8a974d04cebc75bb0e077a74da3 |
| `tools/reuso/SELLO-REUSO.md` | 29d90bbd1bfecb43c60b8b3d5bd61e11 |
| `.github/workflows/reuso-mosca.yml` | a0986279fa1f92e6b2082131124c87f7 |
| `.github/workflows/reuso-humo.yml` | a0defa1dea62cf695c06b0e7ab039813 |
| `results/reuso_2026-10-14_humo/brain-env-humo.log` | d9a75475f61e4c1927af44abd853d7f4 |
| `results/reuso_2026-10-14_humo/brain-env-prueba.log` | 0ca00af277704ee493cf927366d726c7 |
| `tools/contexto/actualizar_contexto_2026-10-14-029.py` (main) | 843a0f88c5c2deb847fa7edfb66a5c20 |

## NO MEDIDO
- T1, T2 y H_REUSO.
- El humo en Actions.
- Otras plantillas: la comparación izquierda-derecha en el cordón (H_COMPARADOR) y la convergencia bilateral. Esta prueba mira una sola.
- MANC y hemibrain.

## Antes de firmar
| Afirmación | Instrumento | ¿Podía dar rojo? |
|---|---|---|
| La regla cuenta bien | prueba_reuso.py | Sí: EXACTO, OTRO_LADO y UMBRAL_X con valores a mano |
| El nulo puede dejar pasar o frenar | PUEDE_DAR_ROJO | Sí: plantado p = 0,032; sin plantar p = 1 |
| El nulo conserva lo que dice | guarda | Sí: falla si cambian las llegadas o los lados |
| No vi el resultado | humo ciego | El log no tiene T1, T2 ni p |
| Multiplicidad | Holm sobre 4 | Declarado |

--- METODO PROMETEO ---
Mirar la estructura de BANC antes de escribir el instrumento. Fijar la plantilla, los umbrales y el nulo antes de ver nada. Humo ciego. Declarar lo que se filtró del control. Corrida solo con `CORRER`.
