# SELLO de H_TAU (respuesta 2026-10-14-002)

Rama `titan/htau-nucleo-banc-2026-10-14`. Sellado antes de correr: nada de lo que decide H_TAU se midió.
Pedido: «SELLA EL H_TAU» (14-oct 08:18) y ClickKit `terminar_sellos_002` (10:51).

## Pregunta
En los factoriales 3 y 4 la red le ganó a su regla en 8 de 10 semillas de tau y perdió en la 5 y la 7 (post-hoc, 2026-10-14-001).
H_TAU: **si las constantes de tiempo se eligen solo con el entrenamiento, el cableado de R2 le gana a su regla propia por más de 1 punto en ensayos de prueba que nadie vio.**

## Diseño (todo nuevo)
- Sujeto: R2 (33.489 neuronas, 4.031.897 aristas, 564 entradas), `tools/factorial2/factorial2_mosca.py` sin cambios.
- Candidatas: semillas de tau 10 a 19 (nunca usadas).
- Elección por celda: validación cruzada de 5 pliegues en los 2.400 ensayos de entrenamiento (pliegue = índice mod 5). Empate: la semilla más chica. La peor se guarda como diagnóstico.
- Prueba: semillas 12 a 21 (nunca usadas), 2.000 ensayos cada una.
- REPRO_R2 (control): en 0,3|0,15, tau 0 y prueba 2 tienen que dar exacto lo del factorial 3 (0,9465 / 0,9375 / 0,9235).

## Decisión (agregar_htau.py)
- Primaria: elegida menos regla propia; bootstrap sobre las 10 semillas de prueba, B 20.000, semilla 2028, IC90; margen 0,01.
- SUPERA → **H_TAU SOSTENIDA**. EQUIVALENTE, NO_SUPERIOR o PIERDE → **REFUTADA**. NO_INFERIOR o INDETERMINADO → SIN_DECIDIR.
- **Falsador:** si el IC90 no queda entero arriba de +0,01, H_TAU no se sostiene; si queda entero abajo, queda refutada.
- Diagnóstico (no decide): elegida menos peor (semilla 2029), semilla elegida por celda.
- Invalidan: faltar una celda, humo, otro plan, otro md5, REPRO_R2 falso, otras DN.

## Archivos sellados (md5)
| archivo | md5 |
|---|---|
| tools/htau/htau_mosca.py | 2006cfef6eaffc023086fd35fbe20f64 |
| tools/htau/agregar_htau.py | 0baa11d836ef6f450aa34134d7c85181 |
| tools/htau/prueba_agregar_htau.py | 36237b4454db930f17d89ca0e9ba6c4a |
| .github/workflows/htau-humo.yml | 1ef7f511d0673a203e9a4e47be2af139 |
| .github/workflows/htau-mosca.yml | f99f6679ec5b5a47fd5e7f756e73c251 |
| tools/factorial2/factorial2_mosca.py (importado) | 798a824cd47808155fa12adb9e652dac |
| tools/escape_aterrizaje/tarea_mosca.py (importado) | 40d64e074d9163753439307c5be4ac5e |
| connectivity.parquet / annotations.tsv | 3d802fd5… / 719904ab… |

## Humo (Actions)
Commit del bot `0cffc8d`, carpeta `results/htau_2026-10-14_humo/` (MD5SUMS del bot):
- **REPRO_R2 a tamaño real: True.** tau 0, prueba 2, 0,3|0,15 dio W 0,9465, regla propia 0,9375, regla de 40 0,9235: exacto lo del factorial 3 (647,8 s; `htau_humo_repro.log` 4b01e9fa).
- Corrida corta (600 / 200 ensayos, candidatas 10 y 11, pruebas 12 y 13): validación, elección (empate a 0,9100 resuelto por la semilla más chica), prueba y json; VÁLIDO, EXIT 0 (`htau_humo_corto.log` 8b1aed5a). Los números de humo no valen.
- Prueba del agregador en Actions: **PRUEBA_AGREGADOR_HTAU PASA 6/6** (`htau_humo_agregador.log` 65e6abdb).
- Velocidad medida: 0,146 s por ensayo simulado.

## Costo y disparo
6 trabajos de Actions (uno por celda) en paralelo: 64.000 ensayos simulados por celda a 0,146 s (medido en el humo), unas 2,6 h; la celda 0,3|0,15 suma REPRO (unos 11 min). Debajo del límite de 340 min. Gratis.
**Corre solo cuando Abraham lo pide:** pushear `results/htau_2026-10-14/CORRER` en esta rama.
