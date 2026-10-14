# 2026-10-14-026 · Topo v0.2: la resta del giro sale de DNp06 y pasa a una salida diferencial aguas abajo; en el banco rinde igual por construcción, así que el falsador va a BANC

## Pedido
Abraham, 14-oct 20:22, ClickKit `topo_v02_diferencial_025`: «Sellá Topo v0.2 con salida diferencial».

## Veredicto primero
- [HECHO] Topo v0.2 en `titan/topo-v02-2026-10-14` (`a817ad3`). `topo_v02.py` envuelve a `topo.py` (9abefe9d) y a `topo_grafo.py` (0ea68782) sin cambiarlos; verifica sus md5 y aborta si cambian.
- [HECHO] **Gramática nueva:**
  - `linea ... -> interna`: una línea que no compite.
  - `compara NOMBRE = A - B en ESTADO -> ACCION`: un comparador que compite como línea.
  - Las flechas línea → comparador se marcan AGUAS_ABAJO.
- [MEDIDO] `escape_dif.topo` (las DNp06 leen su lado y el giro sale de comparar izquierda contra derecha), contra FlyWire v783: **CABLEADA=10, AGUAS_ABAJO=4**, ninguna SIN_VIA_DIRECTA. El que resta daba SIN_VIA_DIRECTA=4.
- [MEDIDO] **Pruebas 9/9**, reproducidas byte a byte desde un clon limpio:
  - PARIDAD_ESCAPE: las mismas predicciones que `escape.topo` en 800 de 800 ensayos y los mismos umbrales, bit a bit.
  - PARIDAD_V0: un programa sin `interna` ni `compara` da en v0.2 lo mismo que en v0.
  - PUEDE_DAR_ROJO: con el comparador invertido cambian 20 predicciones.
  - SIN_COMPARADOR_DIFIERE: el fiel sin comparador difiere en 36.
  - Cuatro errores de programa rechazados.
- [CONCLUSIÓN] **No sello una prueba de banco.** Por linealidad, comparar A − B aguas abajo es la misma cuenta que restar adentro de la línea. «v0.2 recupera el aterrizaje ante el looming frontal» no puede dar rojo: saldría igual que `escape.topo`, que ya lo hacía. En la 025 lo ofrecí como prueba, y me equivoqué: lo corrijo acá.
- [CONCLUSIÓN] Lo que v0.2 cambia es **dónde** dice el programa que ocurre la resta. Eso se falsa en el cordón nervioso, con H_COMPARADOR en BANC: que las salidas de DNp06 izquierda y derecha converjan con signo opuesto sobre motoneuronas de vuelo de un mismo lado, más que en otras descendentes bilaterales. Está sin sellar, y los datos de BANC 888 están en brain-env.

## Herramientas y máquina
- brain-env (Python 3.12.14, numpy 2.5.3, pandas 3.0.5): pruebas y chequeo contra FlyWire v783 (pin 3d802fd5 / 719904ab).
- GitHub: rama nueva y verificación desde un clon limpio.
- Acción delicada: ninguna.

## Archivos
| Archivo (rama `titan/topo-v02-2026-10-14`) | md5 |
|---|---|
| `tools/topo_v02/topo_v02.py` | fe059177286d520e451600e4cea0b2e2 |
| `tools/topo_v02/escape_dif.topo` | 11f6c216043b59e96fad244f05ba47ac |
| `tools/topo_v02/prueba_v02.py` | 7302148ce1b07b9097014b61427eae9e |
| `docs/topo/grafo-v02-2026-10-14.log` | 6d1fd094403be2e90c1aba14afedb690 |
| `docs/topo/prueba-v02-2026-10-14.log` | f3e0a57998d447c10f60f5199fad5afa |
| `docs/topo/TOPO-v0.2-diferencial.md` | 137c103c3a64d3186a26493145bc05b8 |
| `tools/contexto/actualizar_contexto_2026-10-14-026.py` (main) | e75a6572cf4d240ca426914d9bc81d35 |

## NO MEDIDO
- H_COMPARADOR en BANC.
- La paridad con entradas reales del banco: la probé con entradas sintéticas. La cuenta es la misma, pero no corrí el banco.
- Las pruebas en Actions.
- Que la entrada del otro ojo sobre DNp06 (excitatoria, según la 025) cambie algo en la regla: v0.2 no la modela.

## Antes de firmar
| Afirmación | Instrumento | ¿Podía dar rojo? |
|---|---|---|
| v0.2 = v0 en escape | PARIDAD_ESCAPE | Sí: con el comparador invertido da distinto |
| v0.2 no rompe v0 | PARIDAD_V0 | Sí: compara predicciones y umbrales exactos |
| Las flechas del cerebro están cableadas | topo_grafo sellado | Sí: el que resta da SIN_VIA_DIRECTA=4 |
| Una prueba de banco sería informativa | análisis | No: daría igual por construcción, por eso no la sello |

--- METODO PROMETEO ---
Leído `topo.py` antes de extenderlo; sin tocar lo sellado. Paridad exacta como prueba de compilador. Antes de sellar una hipótesis, chequear que pueda dar rojo; esta no podía, y lo declaro en lugar de sellarla.
