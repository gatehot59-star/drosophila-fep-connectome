# 009-A1 · Compromiso del productor antes del cotejo

Paso 4 de la 010: estadistica_a1.py (37ab63d7…, sin cambios desde 5c9492ff) corrió sobre el sobre real con --abrir-sobre después del commit 698d9652, que fijó la salida del verificador. Este commit fija su salida antes de la fase K. Su salida por pantalla trae veredictos y no se leyó: va acá sólo por sha256.

| Archivo (brain-env, /workspace/a1/v2/apertura/prod/) | Bytes | sha256 |
|---|---|---|
| agregado_a1.json | 339.460 | 7fcc6ddc27774fd5b1b702803de3dd3953c2b91b724294c04c9159442ceba02a |
| estadistica_a1.log (igual a su salida por pantalla) | 9.744 | d6b1ff711c8ac1406e49da5a0943a9772108b50b45e4c9025ccc1155c123d55b |
| tasas_por_neurona.csv | 1.152.346 | c7cc155de8d803104fbb298be6bc4a6af9d47c274f166c4bb010fc7f05b7a329 |

Salió con rc 0 en 8,7 s y sin nada en stderr. Los tres van por sha256 por la misma razón que verificador_a1.json: se recalculan desde git con el productor de 801487ca, el manifiesto 267ca1d0 y el sobre de 7d953dc8.
