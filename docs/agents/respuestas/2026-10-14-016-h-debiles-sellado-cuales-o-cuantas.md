# 2026-10-14-016 · H_DEBILES sellado: R2 con el núcleo intacto y las débiles barajadas, para separar cuáles son de cuántas son

**Pedido:** ClickKit `sellar_debiles_015` (Abraham, 14-oct 16:42), «Sellá H_DEBILES». Sellar, no correr.

## Veredicto primero
- [SELLADO] H_DEBILES queda sellado en la rama `titan/debiles-2026-10-14` (código `c9ec855`, sello `987b73c`): instrumento, agregador, prueba, dos workflows y `tools/debiles/SELLO-DEBILES.md`. No corrió nada que decida.
- [CONCLUSIÓN] La pregunta: el núcleo pierde 4,59 puntos contra R2 (2026-10-14-015). Los ponen las 3.428.678 aristas débiles. ¿Pesan por cuáles son o por cuántas son?
- [SELLADO] La MEZCLA es R2 con el núcleo intacto y las débiles con destinos barajados por lado (mismos grados, pesos, signos y lados). Misma grilla del factorial 3 (600 corridas), pareada con R2 y con el núcleo.
- [SELLADO] E1 = mezcla menos R2 decide H_DEBILES_ESPECIFICAS; E2 = mezcla menos núcleo decide H_DEBILES_SUMAN; M 0,01. S y R: pesa cuáles; R y S: pesa cuántas; S y S: pesan las dos.
- [MEDIDO] Humo brain-env: grilla corta VÁLIDO, mezcla igual por grilla y por mezclas, prueba del agregador 7/7. Humo Actions (corrida 38629138935): grilla, mezclas y agregador en verde.
- [NO MEDIDO] R2 real y núcleo real a tamaño completo por el camino nuevo (tienen que dar 0,9465 y 0,9135): seguían corriendo en Actions y en brain-env al cerrar. Es condición para el CORRER.
- [NO MEDIDO] La corrida completa: 64 trabajos, unas 3 h.

## Herramientas y máquina
brain-env (Linux x86_64, Python 3.12.14, numpy 2.5.3) con insumos pineados (3d802fd5, 719904ab); GitHub Actions x64 con torch 2.14.1 cpu. Acción delicada: ninguna.

## Evidencia del humo
- Sujeto: R2 33.489 neuronas, 4.031.897 aristas; núcleo 603.219 (huella 69255109); débiles 3.428.678. R2_tamano y NUCLEO_tamano True.
- Mezcla k 0: 3.427.496 destinos cambiados (99,97 %), núcleo intacto, grados y lados iguales, 69.542 pares repetidos sumados, huella 32808d53. k 1: 3.427.494 cambiados.
- Visto antes de sellar (declarado): números de humo de 80 ensayos, R2 0,9750, núcleo 0,8500, mezclas 0,8500. Sin valor; no se cambió nada.
- El agregador sobre el humo lee las carpetas reales del factorial 3 y del núcleo (60 y 60 json, TAU_DN y DN iguales); REGLA y REALES dan False en humo, como corresponde a 120/80 ensayos.

## Archivos (md5, verificados desde clon limpio)
| archivo | md5 |
|---|---|
| tools/debiles/debiles_mosca.py | f28404c2ecb1ae84e0a58936964cb7e9 |
| tools/debiles/agregar_debiles.py | c60fbbc618999cd73b67e5998bcbc780 |
| tools/debiles/prueba_agregar_debiles.py | fc7d906ab9f690c1b8ae3987b7ea1fc3 |
| .github/workflows/debiles-mosca.yml | 53c88f1282167eba7ff481bb7d52a184 |
| .github/workflows/debiles-humo.yml | 35bb8225b11ea2a6c5caa61647c75dbc |

## NO MEDIDO
- Los reales a tamaño completo por el camino nuevo, y la corrida completa.
- Si los 69.542 pares sumados mueven algo.
- Mezclas en otras celdas (las 20 son solo en 0,3|0,15); barajados que respeten tipo de neurona.

## Antes de firmar
| afirmación | instrumento | ¿podía dar rojo? |
|---|---|---|
| núcleo intacto en la mezcla | NUCLEO_INTACTO | sí |
| débiles con grados y lados iguales | bincount y lado del destino | sí |
| el agregador decide bien | 7 casos sintéticos, 3 inválidos a propósito | sí |
| el camino nuevo reproduce R2 y núcleo | REAL_R2_IGUAL y REAL_NUCLEO_IGUAL | sí; todavía sin resultado |
| git tiene lo probado | md5 desde clon limpio | sí |

--- METODO PROMETEO ---
Inventario: brain-env y Actions medidos; la PC de Abraham no se usó. Contexto vivo: CONTEXTO md5 4fd0f805, main 2b57671. Sello antes de correr; la corrida espera el click de Abraham y los reales en True.
