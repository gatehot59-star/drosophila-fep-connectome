# SELLO · H_REUSO: la misma plantilla de circuito para distintas acciones, en FlyWire y otra vez en BANC (respuesta 2026-10-14-029)

**Pedido.** Abraham, 14-oct 21:20, ClickKit `sellar_reuso_028`: «Sellá H_REUSO (FlyWire y BANC)». Viene de su idea de la 028: mucho de la mosca sería «lo mismo aplicado de distintas formas para distintas acciones».

## Orden del sello (verificable en git)
| Paso | Commit | Qué | md5 |
|---|---|---|---|
| A | `613317d` | Instrumento, prueba y workflows, antes de ver T1, T2 o p | `reuso_mosca.py` e9a07a7c58d926c00fec9c64cf4eb253; `prueba_reuso.py` 2a00e8a974d04cebc75bb0e077a74da3; `reuso-mosca.yml` a0986279fa1f92e6b2082131124c87f7; `reuso-humo.yml` a0defa1dea62cf695c06b0e7ab039813 |

## La plantilla (inhibición de avance)
- **Unidades:**
  - Un sensor S es un tipo de proyección visual con su lado.
  - Una descendente D es un tipo descendente con su lado.
- **Par cableado:** S le da a D, del mismo lado, al menos 20 sinapsis directas.
- **Plantilla:** existe una inhibitoria X, que no es sensor ni descendente, con al menos 5 sinapsis desde S y al menos 5 sobre D.
- **T1:** la fracción de pares cableados que tienen la plantilla.
- **T2:** cuántas X hacen la plantilla para dos o más **tipos** de descendente distintos. Es la misma pieza al servicio de varias acciones.

## Nulo y decisión
- **Nulo SL:**
  - Los destinos de todas las aristas se barajan dentro de cada bloque (lado de la presináptica, lado de la postsináptica).
  - Conserva las aristas que salen y llegan por neurona, el peso y el signo.
  - Son 200 nulos por conectoma (semillas 2029 y 2030), con p = (1 + nulos ≥ observado) / 201.
- **Holm** sobre las 4 pruebas (T1 y T2, en FlyWire y en BANC), con alfa 0,05.
- **Por conectoma:** SOSTENIDA si T1 y T2 pasan Holm; REFUTADA si ninguna tiene p crudo menor que 0,05; si no, PARCIAL.
- **H_REUSO:**
  - SOSTENIDA si los dos conectomas dan SOSTENIDA.
  - REFUTADA si FlyWire da REFUTADA.
  - NO_SE_REPLICA si FlyWire da SOSTENIDA y BANC REFUTADA.
  - Si no, SIN_DECIDIR.
  - INVALIDO si falla un control o una guarda.
- **Controles:**
  - FlyWire: (LPLC2, DNp06) es par cableado en los dos lados, y LHAD1g1 está entre sus X (lo de la 024).
  - BANC: (LPLC2, DNp06) es par cableado en los dos lados.
- **Guarda del nulo:** conserva las llegadas por neurona y el lado del destino, y cambia más de la mitad de los destinos.
- **Signo:**
  - FlyWire: la columna Excitatory, con la convención de Shiu.
  - BANC: gaba o glutamate en `neurotransmitter_predicted` son inhibitorias; el resto, incluso sin predicción (34.455 neuronas), no.
  - Tipos en BANC: `fafb_cell_type` y, si falta, `cell_type`.
- **Descriptivo, sin veredicto:** los tipos de X compartidos, a qué descendentes sirven, y cuántos se repiten en los dos conectomas.

## Prueba
- `prueba_reuso.py` da 7/7 en brain-env y desde un clon limpio (log 0ca00af2).
- **Puede dar rojo, y dio rojo una vez:** en la primera versión, el grafo «sin plantar» todavía tenía una pieza compartida (X0), y PUEDE_DAR_ROJO falló. El error estaba en la prueba, no en el instrumento; lo corregí antes de cualquier dato real.
- Plantado: T2 = 11 contra un máximo nulo de 0 (p = 0,032). Sin plantar: 0 contra 0 (p = 1).

## Humo ciego
- **brain-env, 21:29 (2 nulos por conectoma, 145,7 s).** Log `results/reuso_2026-10-14_humo/brain-env-humo.log`, md5 d9a75475f61e4c1927af44abd853d7f4.
- **CIEGO:** no imprime T1, T2, p ni las listas. No los vi.
- **FlyWire:** 652 sensores, 925 descendentes, 996 pares cableados; el control PASA y la guarda también; 5 s por nulo.
- **BANC:** 842 sensores, 901 descendentes, 753 pares cableados; el control PASA y la guarda también; 5 s por nulo.
- **Declarado:** el control de BANC imprime si LHAD1g1 está entre las X de (LPLC2, DNp06), aunque allí no se exige. Dio True en los dos lados: esa pieza también está en el otro animal. Lo vi antes de sellar; no cambia ni T1 ni T2.
- **Actions x64:** se dispara con `results/reuso_2026-10-14_humo/HUMO`, en este mismo commit.

## Disparo
La corrida completa (200 nulos por conectoma, unos 40 minutos en brain-env) **solo** se dispara al pushear `results/reuso_2026-10-14/CORRER`, con el sí de Abraham.
