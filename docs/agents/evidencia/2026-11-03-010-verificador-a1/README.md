# Evidencia de la respuesta 2026-11-03-010 · verificador independiente de 009-A1

**Máquina:** brain-env (host `6c09d8604b07`, Python 3.12.14, NumPy 2.5.3, SciPy 1.18.1), por MUDH Gateway/build.

**Qué corrió:** `correr10.sh`, entre las 00:24:05Z y las 00:30:34Z del 4-nov-2026 UTC (21:24 a 21:30 ART del 3-nov). Corrió sobre los bytes de `tools/verificador_a1/` bajados de raw en el commit `5eaf35d08117a34bb37a325a1e4422ffb316b650` de la rama `titan/verificador-a1-independiente`.

**Quién:** BRAIN. Los archivos son copia byte a byte de `/workspace/a1/v2/evid10/`; cada sha256 se cotó contra el de brain-env antes de commitear.

| Archivo | Bytes | SHA-256 | Qué es |
| --- | --- | --- | --- |
| `descarga.log` | 1.431 | `f95cc3dc0a6a976b1fd48892d97729b1c3c9a0a12b22dea5977388bb745a1005` | huellas de los bytes bajados, del manifiesto y de los sobres de ensayo, y el entorno |
| `correr10.sh` | 1.090 | `9a256950804f1057a945c1208095c3bd88d207314442c29029763923e922d762` | los comandos exactos |
| `tiempos.log` | 117 | `8927fd7e0559417a8678e95dc35e64ffb011e55de1ac4fed0239a94240e1a7fc` | inicio y fin de cada etapa |
| `ensayo.log` | 1.151 | `2ed888e4c79ca853402cdc8f8aed566ec6d8fbfd0aae8f617e4678158920aefb` | ensayo general: 12/12 PASS, exit 0 |
| `ensayo/limpio.log` | 1.724 | `c1013ace6432de97bc22ac1182fed409384debd6aa1efe72ce1d5a30aee3fa83` | verificador sobre el limpio: CONCORDANTE |
| `ensayo/limpio_bis.log` | 1.728 | `7918b33b742d1099696423362d3dc8fe32d01de6b1b84c0f644be97a4f019e8d` | segunda corrida del limpio: misma salida |
| `ensayo/sucio.log` | 4.914 | `7065e1d1f2f5c37bf532dbdc47a8516a64493bdcb081641811b2c8bc8c4aad37` | sucio: 22 fallas en 19 celdas, 6 huecos del control, CONCORDANTE |
| `ensayo/global.log` | 1.843 | `ffb8b8e0fcfb59a889ff749412554b60985ec27a62ec808b6408da97c66decf0` | global: ILEGIBLE, 44 inválidas, CONCORDANTE |
| `ensayo/ensayo_resumen.json` | 6.301 | `8311a3e769d5eca05ed1f9e19f829d7469de8897ff60258ee0d227021b861f26` | chequeos y veredictos sintéticos por escenario |
| `prueba.log` | 1.100 | `d06ae1713e0445bc1cc9b4c1d87246145354a2c87e500d29805fa5688a8faccf` | pruebas: 14/14 PASS, exit 0 |
| `mutantes.log` | 1.678 | `65350769ce105a308f4b396f5bf5172ec42609bd78760a46dabc340206de299b` | mutantes: 10/10 MUERTOS, control 9/9, exit 0 |
| `lectura_010.md` | 5.557 | `624b2a98129393293c77f5a6fe02dcbc06c41d3af8fb7255e8ce66805089e59c` | D1 a D15 contra la letra de 010 (no independiente) |

**El exit 1 de `sucio.log` y `global.log` es el esperado:** el verificador sale con 1 cuando la fase T encuentra fallas técnicas, y en esos sobres las fallas están sembradas. El chequeo que vale es el de `ensayo.log`.

**Las salidas grandes quedan en brain-env**, en `/workspace/a1/v2/evid10/ensayo/<escenario>/`, y sus sha256 están en los logs: `verificacion_tecnica.json`, `verificador_a1.json`, `verificador_a1_espejo.json` (sólo en el sucio) y `cotejo_a1.json`. Se regeneran byte a byte con `correr10.sh`.

**Nada de esto lee el sobre real** `results/a1_2026-11-03/corrida_1/`.
