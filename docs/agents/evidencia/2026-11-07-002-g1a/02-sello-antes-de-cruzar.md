# G1-A · sello antes de cruzar

Respuesta 2026-11-07-002. Este archivo se commitea **después de la calibración y antes de cruzar la Y real con el M real**. El cruce corre con g1a.py sha256 a1c5ec691636ca57763fd3a37b78a59fd0acc27f14a8b47d948ac1a3db6dcd5e, el mismo de las enmiendas (commit d365b545), y recibe este commit como sello.

## La calibración pasó en las dos moscas

200 réplicas por β, Y sintética desde el G0 ajustado a la Y real (G0 no mira M), β plantado sobre el M real. Cortes fijados en d365b545: cobertura de 181 o más de 200, sesgo menor a 0,1, y con β = 0 a lo sumo 6 con p < 0,01 y 19 con p < 0,05.

| | FlyWire 783 | BANC 888 cerebro |
|---|---|---|
| β = 0: sesgo · cobertura · p < 0,01 · p < 0,05 | −0,033 · 191 · 1 · 3 | −0,003 · 190 · 2 · 11 |
| β = 0,4: sesgo · cobertura | +0,008 · 185 | +0,021 · 191 |
| β = 0,7: sesgo · cobertura | +0,007 · 195 | +0,015 · 185 |
| β = 1,1: sesgo · cobertura | +0,025 · 184 | +0,039 · 189 |
| ajustes que convergen | 800 de 800 | 800 de 800 |
| **veredicto** | **PASA** | **PASA** |

El error robusto acierta: con β = 0 la dispersión real de β̂ es 0,124 en FlyWire y 0,183 en BANC, y el error robusto medio da 0,128 y 0,183 (el del modelo, 0,129 y 0,183). En FlyWire la prueba es conservadora con β = 0: 3 de 200 debajo de 0,05 donde se esperaban 10, porque el nulo de recableados es más ancho que el ruido del mundo de G0. Eso cuesta potencia, no validez.

## Potencia: lo que el sello tiene que decir antes de cruzar

| β plantado (OR) | FlyWire: potencia_p · completa | BANC cerebro: potencia_p · completa |
|---|---|---|
| 0,4 (1,49) | 0,595 · 0,425 | 0,225 · 0,21 |
| 0,7 (2,01) | 1,0 · 1,0 | 0,74 · 0,74 |
| 1,1 (3,00) | 1,0 · 1,0 | 1,0 · 1,0 |

**Las dos moscas quedan debajo de 0,8 a OR 1,5: FlyWire 0,60 y BANC cerebro 0,23.** La prueba ve bien un efecto de OR 2 en FlyWire y de OR 3 en BANC; uno real de OR 1,5 probablemente no llegue a significativo en BANC. Consecuencia para leer: si el efecto existe pero es chico, lo esperable es SOSTENIDA_EN_FLYWIRE o SIN_DECIDIR, no SOSTENIDA; y NO_REPLICA pide que el IC de BANC quede entero debajo de 1,5, que con su error (±0,32 en β) exige un β̂ de BANC menor a 0,09.

## Bancos de recableados fijados

| | FlyWire 783 | BANC 888 |
|---|---|---|
| semilla · sha256 | 7830711 · 982cc13bb3adbfc6dc51a0edf6486b25bc0852ff5c22a1dac4947677ade0eb0e | 8880711 · 1a2cef420148044f82a6d8989ce2726665455875c7061e612e1785a75a6a12ce |
| grados, unicidad y lado conservados | 1.000 de 1.000 | 1.000 de 1.000 |
| intercambios efectivos por recableado | 8.264,7 de 9.960 intentos | 6.081,9 de 7.530 |
| aristas reales que sobreviven | 9,4 % | 10,4 % |
| pares con M = 1 por recableado (real) | 2.077 en promedio, de 1.617 a 2.615 (real 1.828) | 873, de 655 a 1.133 (real 864) |

## Archivos de la calibración (03-calibracion/)

- cal_flywire.json (4.273 B, e5032620226e446ed78cd3135166096a36eae6a9a8801afd0bde3d33a5c5a8a8) y cal_banc.json (4.301 B, c4de59c47057528fb23bf628b16dad2a31c5c603bdb4b900bd38465de498173c), verbatim.
- cal_flywire.log, cal_banc.log y corrida.log, verbatim. corrida.log anota 860,1 s para las dos porque el lanzador espera a FlyWire antes de anotar BANC; BANC tardó 481,3 s (su JSON) y FlyWire 856,7 s. Las dos con rc 0 y error estándar vacío.
- Las 800 filas por mosca quedan en brain-env y se fijan sólo por sha256: cal_flywire_replicas.csv (194.749 B, 26343a16f91d9d03ad3fa3cc4ec30644628b31544cc0d5a4a89c358fbbb5d3ce) y cal_banc_replicas.csv (191.853 B, 1c5d1ddf9bc6b8fc7671003b916e7382677c2563214bb3337c863dd0186000b6). Se recomputan con el mismo g1a.py y las semillas.

## Comando del cruce

python3 /workspace/a1/v2/g1/a/correr_g1a.py /workspace/a1/v2/g1/a/corrida cruzar a1c5ec691636ca57763fd3a37b78a59fd0acc27f14a8b47d948ac1a3db6dcd5e <sha de este commit>

Corre FlyWire, después BANC (que usa el β̂ de FlyWire para la transferencia) y al final la lectura. g1a.py se niega a cruzar si su sha256 no es el de arriba, si la calibración de la mosca no pasó o si su banco no tiene el sha256 de esta tabla.

## Lectura

Sin cambios: la tabla de 2026-11-04-001 con las enmiendas de d365b545. INVALIDO ya no puede salir por la calibración; sólo saldría si las dos moscas corrieran con instrumentos o sellos distintos.
