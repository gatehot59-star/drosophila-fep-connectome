# Topo v0.2: la salida diferencial aguas abajo (respuesta 2026-10-14-026)

**Pedido.** Abraham, 14-oct 20:22, ClickKit `topo_v02_diferencial_025`: «Sellá Topo v0.2 con salida diferencial».

## Qué agrega
- `linea NOMBRE = EXPR en ESTADO -> interna`: una línea que no compite. Es una salida que otra cosa lee.
- `compara NOMBRE = A - B en ESTADO -> ACCION`: compite como una línea y su señal es la de A menos la de B. A y B tienen que ser internas, distintas y del mismo estado. Una interna sin comparador es un error.
- El chequeo contra el conectoma marca las flechas línea → comparador como **AGUAS_ABAJO**: no son del cerebro, se chequean en el cordón nervioso (BANC).
- `topo.py` (9abefe9d) y `topo_grafo.py` (0ea68782) siguen intactos: `topo_v02.py` los envuelve y verifica sus md5.

## El programa
`tools/topo_v02/escape_dif.topo`: las dos DNp06 leen solo su lado y el giro sale de comparar DNp06 izquierda contra derecha.

Chequeo contra FlyWire v783: **CABLEADA=10, AGUAS_ABAJO=4**, y ninguna flecha SIN_VIA_DIRECTA. El que resta, `escape.topo`, daba CABLEADA=10 y SIN_VIA_DIRECTA=4: las mismas cuatro flechas ahora quedan donde la literatura dice que deberían estar.

## Lo que no se sella, y por qué
Por linealidad, `escape_dif` rinde exactamente lo mismo que `escape.topo`. La prueba lo verifica: las mismas predicciones en 800 de 800 ensayos y los mismos umbrales, bit a bit. Entonces sellar «v0.2 recupera el aterrizaje ante el looming frontal» sería una prueba que no puede dar rojo, y no la sello. Lo que v0.2 cambia es **dónde** dice que ocurre la resta. Eso sí se puede falsar, pero en el cordón nervioso, no en el banco.

## El falsador que queda (para sellar aparte, en BANC)
- **H_COMPARADOR:** en el cordón nervioso, las salidas de DNp06 izquierda y derecha convergen con signo opuesto sobre las motoneuronas de vuelo de un mismo lado, directo o por una interneurona inhibitoria, más que las otras descendentes bilaterales.
- Si no aparece, v0.2 pone la resta en un lugar donde tampoco está, y queda la dinámica.
- Los datos de BANC 888 están en brain-env. No los miré para DNp06.

## Archivos
| Archivo | md5 |
|---|---|
| `tools/topo_v02/topo_v02.py` | fe059177286d520e451600e4cea0b2e2 |
| `tools/topo_v02/escape_dif.topo` | 11f6c216043b59e96fad244f05ba47ac |
| `tools/topo_v02/prueba_v02.py` | 7302148ce1b07b9097014b61427eae9e |
| `docs/topo/grafo-v02-2026-10-14.log` | 6d1fd094403be2e90c1aba14afedb690 |
| `docs/topo/prueba-v02-2026-10-14.log` | f3e0a57998d447c10f60f5199fad5afa |
