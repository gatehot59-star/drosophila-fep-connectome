# Evidencia 2026-11-03-006 · corrida grande de 009-A1

Respuesta: [2026-11-03-006](../../respuestas/2026-11-03-006-corrida-a1-8540-de-8540-sellada-sin-leer.md). Código en la rama `titan/a1-runner-2026-11-03`, sin merge. Resultados en `results/a1_2026-11-03/corrida_1/` de esa rama, commit del bot `7d953dc8577ecf1fdbaecc4859b902af8854e79b`.

**Nadie computo ni leyo un estimando.** Los scripts de esta carpeta imprimen solo estados, huellas y datos de máquina. Los `ensayos.log` de cada bloque tienen las líneas `ENSAYO` del runner, con conteos por ensayo; no los abrí.

## Bytes probados y corridos

Los nuevos se descargaron de raw en `a42c9fa5c61001e0eef66040b2120a87ce701e21`. Son los que lista `tools/a1/HUELLAS.sha256` en `e7490f59fee2f36c7a266a712415257f61361939`, y cada uno de los 21 jobs los chequeó OK antes de correr.

| Archivo | Bytes | sha256 |
|---|---|---|
| tools/a1/plan_a1.py | 5.408 | d1b26450ecf8e9ca5211ab7a78beadf536ff61c4db659ed79c3dd9e142662e5d |
| tools/a1/juntar_a1.py | 7.757 | 051d0b474a911930db692fed5826839b426df2953eebd39a86ab69538260d414 |
| .github/workflows/a1-corrida.yml | 13.719 | ecf189be4421681be8d377508c04cf34f71a628b13728141cb7f1671bebbe064 |

El runner, el manifiesto, validar y comun no cambiaron desde `4c499296`. Sus sha256 están en la evidencia de [2026-11-03-005](../2026-11-03-005-runner-a1-real/README.md).

## Pruebas en brain-env, antes de disparar

1. `python3 plan_a1.py --manifiesto /workspace/a1/v2/manifiesto_a1.json --sha-manifiesto 267ca1d0… --bloques 20 --resumen --prueba` produce `plan_prueba.log`:
   - el reparto cubre los 8.540 ensayos, sin duplicados, faltantes ni celdas partidas;
   - los bloques tienen entre 340 y 440 ensayos;
   - el chequeo da rojo con un ensayo movido, uno faltante y uno duplicado.
2. `python3 juntar_a1.py prueba --registros /workspace/a1/v2/fx2/recibos --trabajo /workspace/a1/v2/jx --manifiesto-fixture /workspace/a1/v2/fx2/manifiesto_fx.json` produce `juntar_prueba.log`: 6/6. Prueba la ida y vuelta del JSONL, que cada línea sea el archivo tal cual, que un testigo adulterado dé DISTINTO, que una línea rota quede ilegible y que un plan incompleto no valide.
3. `python3 juntar_a1.py testigos --registros humo_ref --referencia humo_ref`, sobre los 10 recibos del humo bajados de `737aafec`, produce `testigos_contra_si_mismo.log`: 10/10 IGUAL.
4. `workflow_sintaxis.log`: el YAML parsea y cada paso pasa `bash -n`.

## Corrida en Actions

Run 41684131931, disparado por `e7490f59` a las 17:25:39Z. Los 21 jobs terminaron en success: 20 bloques y el job final, que cerró a las 17:55:44Z. El bot commiteó `7d953dc8` a las 17:55:22Z.

| Bloque | Ensayos | CPU | Job, s | Paso de ensayos, s |
|---|---|---|---|---|
| 00 | 400 | AMD EPYC 7763 | 1.570 | 1.418 |
| 01 | 440 | AMD EPYC 7763 | 1.686 | 1.537 |
| 02 | 440 | AMD EPYC 7763 | 1.744 | 1.593 |
| 03 | 440 | AMD EPYC 7763 | 1.741 | 1.556 |
| 04 | 440 | Intel Xeon 6975P-C | 1.405 | 1.267 |
| 05 | 440 | AMD EPYC 9V45 | 1.019 | 912 |
| 06 | 440 | AMD EPYC 9V45 | 1.023 | 924 |
| 07 | 440 | AMD EPYC 9V45 | 1.018 | 914 |
| 08 | 440 | AMD EPYC 9V74 (sin avx512f) | 1.654 | 1.501 |
| 09 | 440 | AMD EPYC 9V74 (con avx512f) | 1.289 | 1.168 |
| 10 | 440 | AMD EPYC 9V45 | 1.061 | 956 |
| 11 | 440 | AMD EPYC 9V45 | 1.006 | 907 |
| 12 | 440 | AMD EPYC 7763 | 1.734 | 1.556 |
| 13 | 400 | AMD EPYC 7763 | 1.552 | 1.398 |
| 14 | 360 | AMD EPYC 7763 | 1.390 | 1.245 |
| 15 | 440 | AMD EPYC 9V45 | 1.057 | 948 |
| 16 | 440 | AMD EPYC 7763 | 1.734 | 1.567 |
| 17 | 440 | AMD EPYC 7763 | 1.672 | 1.524 |
| 18 | 440 | AMD EPYC 9V45 | 1.046 | 942 |
| 19 | 340 | Intel Xeon Platinum 8573C | 1.184 | 1.054 |

Los tiempos salen de la API pública de Actions, y la CPU sale de `lscpu` en el `intento.log` de cada bloque. La suma de los pasos de ensayos da 24.887 s, unos 2,9 s por ensayo con 3 procesos.

## Cotejo en brain-env, después de la corrida

`python3 comparar_corrida_a1.py --commit 7d953dc8577ecf1fdbaecc4859b902af8854e79b --manifiesto-local /workspace/a1/v2/manifiesto_a1.json --tools /workspace/a1/v2/tools/a1` produce `comparar_corrida_a1.log` (6/6 IGUAL) y `comparar_corrida_a1.exit` (0).

Con `--adulterar` produce `control_negativo_corrida.log`: K3 y K5 dan DISTINTO, con 4/6 y EXIT=1.
