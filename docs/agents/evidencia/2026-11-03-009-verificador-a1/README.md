# Evidencia 2026-11-03-009 · Ensayo general del verificador independiente de 009-A1

Máquina: brain-env (host `6c09d8604b07`), `/usr/local/bin/python3` 3.12.14, NumPy 2.5.3, SciPy 1.18.1. Código bajado de raw en el commit `801487cad19747e96bb346d98ffad1c3d508847c` de `titan/a1-runner-2026-11-03`. Manifiesto real `267ca1d0820193fff08a79875a1d1bd6a36d8633e203db9e0ee3d7304c5e3dd9`. **No se leyó ningún recibo de `corrida_1`**: los únicos recibos de este ensayo son sintéticos.

## Archivos de esta carpeta

Cada uno es copia byte a byte del original en brain-env. Las transcripciones se cotejaron por sha256 en el taller antes de commitear.

| Archivo | Bytes | SHA-256 | Original en brain-env |
| --- | --- | --- | --- |
| `descarga.log` | 3.232 | `2f181b22ddab87bc909e927703b6f918f31fb1ef6841e5d1b0908958cccb187b` | `/workspace/a1/v2/evid9/descarga.log` |
| `prueba.log` | 2.733 | `4c5278f4be800ac80ca694d88c0502d73b1e19689bc44c81dcc820c47921c7c7` | `/workspace/a1/v2/evid9/prueba.log` |
| `mutantes.log` | 2.269 | `9fae3ef51e0d8dda750a19399dbbee4354ee7f74ebc9749f414e3dbd77bb6bfe` | `/workspace/a1/v2/evid9/mutantes.log` |
| `estadistica_limpio.log` | 10.018 | `dc7afcdf657da29a2c339bd5e73f0892ec109e8ccba39f7b7cb599e1c203d9be` | `/workspace/a1/v2/evid9/ensayo/est_limpio/estadistica_a1.log` |
| `mutantes_008_brain_env.log` | 3.239 | `1ce2d496387997740142e8018009ee5d0b1d7369eaa79a73cecedc5dacdc47c0` | `/workspace/a1/v2/evid8/mutantes.log` |

## Comando

`/workspace/a1/v2/evid9/correr9.sh`, lanzado desacoplado a las 22:09:53Z:

```
#!/bin/bash
cd /workspace/a1/v2/evid9
date -u +%Y-%m-%dT%H:%M:%SZ > inicio.txt
/usr/local/bin/python3 codigo/tools/a1/prueba_sobre_sintetico_a1.py --manifiesto /workspace/a1/v2/manifiesto_a1.json --sha-manifiesto 267ca1d0820193fff08a79875a1d1bd6a36d8633e203db9e0ee3d7304c5e3dd9 --trabajo /workspace/a1/v2/evid9/ensayo > prueba.log 2>&1
echo $? > prueba.exit
date -u +%Y-%m-%dT%H:%M:%SZ > fin_prueba.txt
/usr/local/bin/python3 codigo/tools/a1/mutantes_sobre_sintetico_a1.py --manifiesto /workspace/a1/v2/manifiesto_a1.json --sha-manifiesto 267ca1d0820193fff08a79875a1d1bd6a36d8633e203db9e0ee3d7304c5e3dd9 --trabajo /workspace/a1/v2/evid9/mut > mutantes.log 2>&1
echo $? > mutantes.exit
date -u +%Y-%m-%dT%H:%M:%SZ > fin_mutantes.txt
```

| Marca | Valor |
| --- | --- |
| `inicio.txt` | 2026-11-03T22:09:53Z |
| `prueba.exit` | 0 |
| `fin_prueba.txt` | 2026-11-03T22:10:58Z |
| `mutantes.exit` | 0 |
| `fin_mutantes.txt` | 2026-11-03T22:19:15Z |

## Sucio y global: extracto de los logs del productor

Sólo las líneas VALIDACION y VEREDICTO. Los logs completos quedan en brain-env.

`ensayo/est_sucio/estadistica_a1.log`: 9.544 bytes, SHA-256 `89ada089c7938cbd3cb930d1ff4840d5305c0220487eafd83e659c81a6453949`.

```
VALIDACION INVALIDO_TECNICO registros=8541 esperados=8540 fallos=15 invalidas=13
VEREDICTO P_T1_B SIN_DECIDIR casos={"R01": "PASA", "R02": "NO_PASA:SIN_DECIDIR", "R03": "PASA"}
VEREDICTO P_T2_B SOSTENIDA tipos={"CB0172": "BLOQUEADO", "CB0534": "PASA", "CB0580": "PASA", "PS100": "PASA"}
VEREDICTO F_C H1 INVALIDO_TECNICO
VEREDICTO F_C H1b SOSTENIDA
VEREDICTO F_C H2 SOSTENIDA
VEREDICTO F_C H3 SOSTENIDA
VEREDICTO F_C H4 SIN_DECIDIR
VEREDICTO F_C H4b SOSTENIDA
VEREDICTO F_R01 firma=SOSTENIDA contrastes={"ZA1": true, "ZA2": true, "ZA3": true}
```

`ensayo/est_global/estadistica_a1.log`: 7.562 bytes, SHA-256 `e6bb126ff2e9cc373a4bed73bc042423e4ff674ff3bae589131b6077d4955067`.

```
VALIDACION INVALIDO_TECNICO registros=8540 esperados=8540 fallos=1 invalidas=44
VEREDICTO P_T1_B INVALIDO_TECNICO casos={"R01": "BLOQUEADO", "R02": "BLOQUEADO", "R03": "BLOQUEADO"}
VEREDICTO P_T2_B INVALIDO_TECNICO tipos={"CB0172": "BLOQUEADO", "CB0534": "BLOQUEADO", "CB0580": "BLOQUEADO", "PS100": "BLOQUEADO"}
VEREDICTO F_C H1 INVALIDO_TECNICO
VEREDICTO F_C H1b INVALIDO_TECNICO
VEREDICTO F_C H2 INVALIDO_TECNICO
VEREDICTO F_C H3 INVALIDO_TECNICO
VEREDICTO F_C H4 INVALIDO_TECNICO
VEREDICTO F_C H4b INVALIDO_TECNICO
VEREDICTO F_R01 firma=INVALIDO_TECNICO contrastes={"ZA1": false, "ZA2": false, "ZA3": false}
```

## Qué intervalos movieron las corrupciones ciegas

Comparación del limpio contra el sucio, sólo en celdas válidas en los dos:

```
INTERVALOS_DISTINTOS ['A|R16|DQ4', 'B|R15|c_X']
  A|R16|DQ4 limpio 34.9 sucio 34.5
  B|R15|c_X limpio 0.8972602739726028 sucio 0.8852739726027398
```

## Workflows que disparó el push de 801487ca

Consulta a la API pública a las 22:11:45Z:

```
RUN 41728204681 H4 integrated regression push completed success 801487ca 2026-11-03T22:09:00Z
RUN 41701852851 H4 integrated regression push completed success 5c9492ff 2026-11-03T19:17:20Z
RUN 41684131796 H4 integrated regression push completed success e7490f59 2026-11-03T17:25:39Z
RUN 41684131931 a1-corrida push completed success e7490f59 2026-11-03T17:25:39Z
```

## Veredicto derivado

Esta parte es interpretación de BRAIN, separada de la evidencia cruda.

*   **Ensayo general:** 13 de 13 en brain-env sobre los bytes de `801487ca`, con exit 0.
*   **Mutantes del ensayo:** 7 de 7 muertos, con exit 0. La prueba puede dar rojo.
*   **Huecos del control del productor:** `validar_a1` no marca seis tipos de corrupción. Dos de ellos cambian estimandos.
*   **Mutantes de la 008:** 28 de 28 muertos en brain-env, con el control en 21/21. Termina el NO MEDIDO de la 008.
*   **Workflows:** el push de `801487ca` sólo disparó el workflow H4, que es de otra línea. Ningún workflow de a1 corrió.
