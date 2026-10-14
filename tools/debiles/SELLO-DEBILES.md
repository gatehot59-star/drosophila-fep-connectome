# SELLO de H_DEBILES: las aristas débiles de R2, ¿pesan por cuáles son o por cuántas son? (respuesta 2026-10-14-016)

Rama `titan/debiles-2026-10-14`, desde `2d4dbfb`. Sellado antes de correr.
Pedido: ClickKit `sellar_debiles_015` (Abraham, 14-oct 16:42), «Sellá H_DEBILES».

## De dónde viene
El núcleo de Schlegel (603.219 de 4.031.897 aristas, 14,96 %) pierde 4,59 puntos contra R2 entero, IC90 [−5,07; −4,10], en 600 de 600 corridas (2026-10-14-015). Los puntos que faltan los ponen las 3.428.678 aristas débiles.

## La pieza
MEZCLA_k = R2 con el núcleo intacto (mismas aristas, pesos y signos) y las débiles con destinos barajados por bloque de lados (`n3.barajar_sl_np` sobre las débiles solas, semilla [17, k]). Conserva grados de entrada y salida de las débiles, pesos, signos y lados; cambia a quién llegan. Radio espectral a 0,9. Pares repetidos se suman.
Medido en el humo: k 0 cambia 3.427.496 destinos (99,97 %), 69.542 pares repetidos, huella `32808d536984669b4fb5b025f34197d4`.

## Hipótesis
- **H_DEBILES_ESPECIFICAS** (importa cuáles son): barajar las débiles cuesta más de 1 punto contra R2.
- **H_DEBILES_SUMAN** (importa cuántas son): barajadas igual suman más de 1 punto sobre el núcleo.

## Diseño
- Grilla: MEZCLA_0 en el banco del factorial 3 (taus 0 a 9, pruebas 2 a 11, 6 celdas, 600 corridas), pareada corrida por corrida con R2 (`results/factorial3_2026-10-13`) y con el núcleo (`results/nucleo_2026-10-14`).
- Mezclas: 20 (k 0 a 19) en tau 0, prueba 2, 0,3|0,15; el trabajo de k0 0 mide también R2 real y núcleo real por el mismo camino.

## Decisión (agregar_debiles.py)
- E1 = mezcla menos R2; bootstrap de dos vías (tau, prueba), B 20.000, semilla 2040, IC90; M 0,01. hi < −0,01: ESPECIFICAS SOSTENIDA; lo > −0,01: REFUTADA; si no, SIN_DECIDIR.
- E2 = mezcla menos núcleo; semilla 2041. lo > +0,01: SUMAN SOSTENIDA; hi < +0,01: REFUTADA; si no, SIN_DECIDIR.
- Lectura: S y R, pesa cuáles; R y S, pesa cuántas; S y S, pesan las dos; R y R, inconsistente; cualquier SIN_DECIDIR, no se lee.
- **Falsadores:** ESPECIFICAS cae si la mezcla no pierde más de 1 punto contra R2; SUMAN cae si la mezcla no le saca más de 1 punto al núcleo.
- Descriptivo: por celda (alfa 0,05/6), por semilla de tau, fracción recuperada, y las 20 mezclas contra R2 real y núcleo real.
- Invalidan: faltan json o corridas, humo, otro md5, otro núcleo, dos mezclas distintas en la grilla, regla o tau o descendentes distintas del factorial 3 y del núcleo, mezclas repetidas o faltantes, reales distintos de 0,9465 y 0,9135, MEZCLA_IGUAL falso.

## Archivos sellados (md5)
| archivo | md5 |
|---|---|
| tools/debiles/debiles_mosca.py | f28404c2ecb1ae84e0a58936964cb7e9 |
| tools/debiles/agregar_debiles.py | c60fbbc618999cd73b67e5998bcbc780 |
| tools/debiles/prueba_agregar_debiles.py | fc7d906ab9f690c1b8ae3987b7ea1fc3 |
| .github/workflows/debiles-mosca.yml | 53c88f1282167eba7ff481bb7d52a184 |
| .github/workflows/debiles-humo.yml | 35bb8225b11ea2a6c5caa61647c75dbc |
| tools/nucleo/nucleo_mosca.py (importado) | 4697c81d994de841f167698562924caa |
| tools/nucleo/agregar_nucleo.py (importado) | cb8a797b00b8b6d2b2f9f891f2a7ac6e |

## Humo
brain-env: grilla corta VÁLIDO; mezclas k 0 y k 1 con guarda True; la mezcla k 0 da lo mismo por la grilla y por las mezclas (0,8500, humo); prueba del agregador PASA 7/7; el agregador lee las carpetas reales del factorial 3 y del núcleo (60 y 60 json, TAU_DN y DN iguales).
Actions (corrida 38629138935): grilla, mezclas y prueba del agregador terminaron en verde. El trabajo de R2 real y núcleo real a tamaño completo (REAL_R2_IGUAL, REAL_NUCLEO_IGUAL) seguía corriendo al sellar: **NO MEDIDO todavía**. Es condición para disparar CORRER: si no da True, no se corre.
Visto antes del sello: números de humo de 80 ensayos (R2 0,9750, núcleo 0,8500, mezclas 0,8500), sin valor. No se cambió nada después.

## Costo y disparo
64 trabajos de Actions (60 de grilla de unos 55 min, 4 de mezclas de cerca de 1 h) más el agregado. Con 20 a la vez, unas 3 h. Gratis.
**Corre solo cuando Abraham lo pide y con los reales en True:** pushear `results/debiles_2026-10-14/CORRER` en esta rama.
