# Evidencia 2026-11-03-005 · runner 009-A1 real y humo 10/10

Respuesta: [2026-11-03-005](../../respuestas/2026-11-03-005-runner-a1-real-humo-10-de-10.md). Código en la rama `titan/a1-runner-2026-11-03`, sin merge. Nada de esto toca el plan de 8.540 ensayos: el humo usa las semillas 900 y 901, fuera del contrato 0..19.

## Bytes probados

Se descargaron de raw en `4c499296b11bf166e763bac3bdbab84fc40ec081` (runner) y en `3faf0ac140e72c6e807d99c256119f94a04031d5` (workflow). Son los que lista `tools/a1/HUELLAS.sha256` en `dee4d670557b3c5e6c6a5b4ab7d2f352b2a07754`. Actions los chequeó 8/8 OK antes de correr.

| Archivo | Bytes | sha256 |
|---|---|---|
| tools/a1/comun_a1.py | 8.679 | 756e81aba922824f0bf4e6374936b944b7f30c17e88b659adc35b9416c0d93ed |
| tools/a1/manifiesto_a1.py | 18.205 | 042031c44f1bd8295b557f3ee373da0d64d38e1eb32cb5cbb2b54354c5425d89 |
| tools/a1/runner_a1.py | 15.927 | 6b494a25f1a556835415a5178999450a6f15bdfd849482744e2719dcba63eaac |
| tools/a1/validar_a1.py | 6.401 | 189eb6477e1f9e3685d273d89aaee4dca8c8c8a63a82a734dae74b2a6ad34e20 |
| tools/a1/prueba_a1.py | 20.334 | b88817f56b65646bbe6af7cb809e21827183391a0a86e180862ba6b6a7bde65d |
| .github/workflows/a1-prueba.yml | 10.186 | 80f4b401c0ceec8caedf9fe928c8537f7a3b302d2624cbe1002346494dd9f6df |
| tools/mecanismo/paso12.py | 11.911 | b604af62e053cacded85979002b34d70ca104d5399cfba1b8135a6626bf784eb |
| tools/reuso/reuso_mosca.py | 15.249 | 3650fc74967e35ec7fcd407964049ea91c3483b2a195790736dd2bfe58656f7d |

## Máquinas

- **brain-env**:
  - Python 3.12.14, numpy 2.5.3, pandas 3.0.5 y pyarrow 25.0.1.
  - Brian2 2.10.1 en el venv `/workspace/a1/venv`, creado con `--system-site-packages`.
  - 2 CPU y 7.802 MB de memoria, con unos 1.048 MB disponibles; el resto lo ocupa otra carga que no es mía.
  - No hay g++, así que Brian2 corre con target numpy.
- **Actions**, run 41679588168, job 126069375433:
  - ubuntu-24.04 con 15.983 MB, g++ 13.3.0, Python 3.12.14, brian2 2.10.1 y cython 3.1.3; target cython.
  - `nproc` imprimió 1 porque `OMP_NUM_THREADS=1`, que GNU nproc respeta. El `/usr/bin/time` del humo marcó 267 % de CPU.

## Comandos en brain-env, en orden

1. `cd /workspace/a1/v2/tools/a1 && /workspace/a1/venv/bin/python prueba_a1.py --shiu /workspace/mecanismo-2026-11-02/shiu --target numpy --trabajo /workspace/a1/v2/fx --n-proc 2` produce `prueba_brainenv_numpy_1.log`: 10/10 PASS, EXIT=0. Sin `--manifiesto-real`, T11 no corre.
2. `python3 manifiesto_a1.py --parquet /workspace/connectivity.parquet --units /workspace/mecanismo-2026-11-02/flywire_units.npz --sello /workspace/r2026-11-03/sello_diseno_16_relevos.json --evid010 /workspace/r2026-11-03/evid010.md --salida /workspace/a1/v2/manifiesto_a1.json` produce `manifiesto_brainenv.log`: 308/308, EXIT=0, 24,3 s. El pico de memoria fue 579.268 kB (VmHWM, sondeado en `/proc` cada segundo).
3. El comando 1 con `--trabajo /workspace/a1/v2/fx2 --manifiesto-real /workspace/a1/v2/manifiesto_a1.json` produce `prueba_brainenv_numpy_2.log`: 11/11 PASS, EXIT=0.
4. `python3 comparar_humo_a1.py --commit 737aafece2f4f96f7688289606992b93acdfe56b --manifiesto-local /workspace/a1/v2/manifiesto_a1.json --prueba-numpy /workspace/a1/v2/prueba2.log` produce `comparar_humo_a1.log` (6/6 IGUAL) y `comparar_humo_a1.exit` (0).
5. El control negativo corre el mismo cotejo con dos copias adulteradas: el manifiesto con `n_ensayos_plan` 8541 y el log numpy con una huella cambiada en un dígito. Produce `control_negativo_comparar.log`: C1 y C2 DISTINTO, 4/6, EXIT=1.

En brain-env, `prueba1.log` es `prueba_brainenv_numpy_1.log`, `prueba2.log` es `prueba_brainenv_numpy_2.log` y `manifiesto1.log` es `manifiesto_brainenv.log`.

## Actions

| Commit | Quién | Qué |
|---|---|---|
| 3faf0ac | yo | workflow v2, no dispara |
| dee4d670 | yo | HUELLAS y PROBAR con `intento=1`; dispara |
| 72835a5f | bot, 16:59:16Z | manifiesto del intento 1, antes de cualquier ensayo |
| 737aafec | bot, 17:00:28Z | resultados; `RESULTADO.txt` marca success en todos los pasos |

Horarios de los pasos, según la API pública de Actions:

| Paso | Inicio | Fin |
|---|---|---|
| intento | 16:58:33Z | 16:58:33Z |
| censo | 16:58:39Z | 16:59:14Z |
| manifiesto | 16:59:14Z | 16:59:19Z |
| fixtures | 16:59:19Z | 17:00:05Z |
| humo | 17:00:05Z | 17:00:27Z |
| validar | 17:00:27Z | 17:00:28Z |
| conservar | 17:00:28Z | 17:00:31Z |

Los resultados están en la rama, en `results/a1_2026-11-03/prueba_1/`: 39 archivos listados en `SHA256SUMS.txt`, cotejados por C6. El manifiesto de 640.908 bytes vive ahí y no en `main`.
