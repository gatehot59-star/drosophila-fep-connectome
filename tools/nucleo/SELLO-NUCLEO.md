# SELLO del núcleo conservado: H_CONSENSO y H_CABLEADO_NUCLEO (respuesta 2026-10-14-002)

Rama `titan/htau-nucleo-banc-2026-10-14`, aparte de H_TAU (carpetas, agregador, disparo y sello propios). Sellado antes de correr.
Pedido: «CONSERVA POR APARTE EL NUCLEO» (14-oct 08:18) y ClickKit `terminar_sellos_002` (10:51).

## La pieza
Núcleo de Schlegel de R2 (Schlegel et al., Nature 2024, doi 10.1038/s41586-024-07686-5): de las aristas de R2 quedan las de 10 sinapsis o más, o las que pesan más del 1 % de la entrada total de su neurona post en todo FlyWire 783.
Medido (brain-env, dos construcciones iguales): **603.219 de 4.031.897 aristas (14,96 %)**, 260.173 inhibitorias, **9.668.248 de 16.971.919 sinapsis (56,97 %)**, 6/6 descendentes con entrada, 563/564 entradas con salida. Huella `69255109562f8a93270c435acdde2239`. El parquet (md5 ef1a221f) queda afuera de git; lo identifica la huella.
Apoyo externo, sin nulo: en BANC se conserva el 77,0 % de las aristas del núcleo evaluables, contra el 32,7 % del resto (`results/banc_2026-10-14/`).

## Hipótesis
- **H_CONSENSO:** el núcleo rinde como R2 entero sin perder más de 1 punto y le gana a sus barajados.
- **H_CABLEADO_NUCLEO:** el núcleo real le gana a 50 SL y 50 T del núcleo (Holm < 0,05 en los dos).

## Diseño
- Grilla del factorial 3 con el núcleo en lugar de R2: taus 0 a 9, pruebas 2 a 11, 6 celdas, 600 corridas. Se parea corrida por corrida con R2 (`results/factorial3_2026-10-13`).
- Nulos: 50 SL y 50 T del núcleo en tau 0, prueba 2, 0,3|0,15.

## Decisión (agregar_nucleo.py)
- Primaria: núcleo menos R2; bootstrap de dos vías (tau, prueba), B 20.000, semilla 2030, IC90; M 0,01. lo > −0,01 → NO_PIERDE; hi < −0,01 → PIERDE; si no, INDETERMINADO.
- H_CONSENSO SOSTENIDA si NO_PIERDE y H_CABLEADO_NUCLEO sostenida; REFUTADA si PIERDE o si no les gana a sus barajados; si no, SIN_DECIDIR.
- **Falsador:** el núcleo pierde más de 1 punto contra R2, o no le gana a sus barajados.
- Descriptivo: núcleo menos regla propia (semilla 2031).
- Invalidan: faltan json o nulos, humo, otro md5, otro núcleo (huella), regla distinta de la del factorial 3 en alguna de las 60 combinaciones, otras tau de las DN, REAL_IGUAL falso.

## Archivos sellados (md5)
| archivo | md5 |
|---|---|
| tools/nucleo/nucleo_mosca.py | 4697c81d994de841f167698562924caa |
| tools/nucleo/agregar_nucleo.py | cb8a797b00b8b6d2b2f9f891f2a7ac6e |
| tools/nucleo/prueba_agregar_nucleo.py | 34f671ec9a66457999b390ef70a52b05 |
| .github/workflows/nucleo-humo.yml | a23a9ecf3d53c4ea197c7be799466ef2 |
| .github/workflows/nucleo-mosca.yml | 81a70a964867cc3f961c897c64544fab |
| tools/factorial2/factorial2_mosca.py (importado) | 798a824cd47808155fa12adb9e652dac |
| tools/factorial3/nulos_r2.py (importado) | c4f1c4d39c99f07cb9ad7977b6f3b01a |

## Humo (Actions)
Commit del bot `fb54d9f`, carpeta `results/nucleo_2026-10-14_humo/` (MD5SUMS del bot):
- **construir a tamaño real en Actions: NUCLEO_tamano True** (603.219 aristas, 260.173 inhibitorias, huella 69255109): la misma pieza en una tercera corrida y otra máquina.
- Grilla corta (tau 0, prueba 2, 0,3|0,15, 120 / 80 ensayos): VÁLIDO, EXIT 0. Radio crudo del núcleo 2.023,71.
- Nulos cortos: SL k 0 con 603.009 destinos cambiados y guarda True; T k 0 con 423 tipos cambiados y guarda True. El núcleo real por el camino de nulos dio lo mismo que la grilla (0,8500 los dos, humo).
- Prueba del agregador en Actions: **PRUEBA_AGREGADOR_NUCLEO PASA 6/6** (incluye el caso de regla distinta, que primero falló en el sandbox y se arregló antes del sello).
- Velocidad medida: 0,045 s por ensayo simulado, un tercio de R2.

## Costo y disparo
80 trabajos de Actions (60 de grilla y 20 de nulos) más el agregado. Unos 17 min por trabajo de grilla (22.400 ensayos) y unos 20 min por trabajo de nulos; con 20 trabajos a la vez, cerca de 1,5 h. Gratis.
**Corre solo cuando Abraham lo pide:** pushear `results/nucleo_2026-10-14/CORRER` en esta rama.
