# Evidencia cruda · barrido de tau heterogénea sobre el Giant Fiber completo

**Corrida:** 2026-08-25 04:54–05:02 UTC · **`DONE in 511.8 s`**
**Instrumento:** `src/sweep_tau_hetero.py`, md5 `35cabd5acc51f37529584cc53c013dcf`
**Salida:** `tau_sweep.json`, md5 `56e1389a84dc8fedaed7ae86f89b90ed`, 9.780 B (por md5, no commiteada)

```
python3 sweep_tau_hetero.py \
  --conn /workspace/connectivity.parquet --ann /workspace/annotations.tsv \
  --spreads 1 2 4 8 15 30 --draws 20 --out /tmp/run/tau_sweep.json
```

**13 configuraciones · 20 sorteos cada una · semillas `1000 + 7i`.** Las `tau` se sortean log-uniformes con **media geométrica fija en 0,119**, así que el spread cambia y el valor central no: **ningún brazo puede ganar por ser globalmente más rápido o más lento.**

---

## 1. Setup y guards, verbatim

```
nodes 864 internal_edges 45687 spectral_radius_before_scaling 0.612675
driven 293  target 2  fast-class neurons 303
GUARD energies {"looming": 20.5027777778, "receding": 20.5027777778,
                "constant": 20.5027777778, "double_energy": 41.0055555556}
GUARD comparable profiles matched: MATCHED_OK
```

---

## 2. ✅ El control interno, que valida el instrumento entero

```
RESULT spread_1_RANDOM {"sel_peak": {"n": 1, "mean": 1.0631, "sd": 0.0, ...},
                        "sel_post": {"n": 1, "mean": 4.3287, ...},
                        "sel_constant": {"n": 1, "mean": 1.1931, ...},
                        "control_double": {"n": 1, "mean": 1.182, ...},
                        "peak_looming": {"n": 1, "mean": 0.1814, ...}}
```

**`spread = 1` reproduce 1,0631 exacto**, el mismo valor de la corrida de `compile_gf_full.py`, con otro código y otra ruta de ejecución. **Si esto no hubiera coincidido, el barrido entero era inválido.**

---

## 3. La tabla completa, las 13 configuraciones

```
config                       sel_peak               sel_post               control_double
spread_1_RANDOM              1.0631 +/- 0.0         4.3287 +/- 0.0         1.182
spread_2_RANDOM              1.0729 +/- 0.0093      4.2328 +/- 0.3548      1.1824
spread_2_STRUCTURED          1.0599 +/- 0.0008      3.8616 +/- 0.0144      1.172
spread_2_REVERSED            1.0802 +/- 0.0006      4.3313 +/- 0.0243      1.1914
spread_4_RANDOM              1.0981 +/- 0.0199      3.9853 +/- 0.6057      1.1823
spread_4_STRUCTURED          1.0726 +/- 0.0015      3.1302 +/- 0.0217      1.1616
spread_4_REVERSED            1.104  +/- 0.0009      3.991  +/- 0.0591      1.2003
spread_8_RANDOM              1.1307 +/- 0.0315      3.5189 +/- 0.7335      1.1823
spread_8_STRUCTURED          1.0972 +/- 0.0022      2.5819 +/- 0.0235      1.1506
spread_8_REVERSED            1.1276 +/- 0.0011      3.4767 +/- 0.0854      1.2083
spread_15_RANDOM             1.1598 +/- 0.0422      3.0157 +/- 0.7361      1.1819
spread_15_STRUCTURED         1.1235 +/- 0.0027      2.2781 +/- 0.0259      1.1409
spread_15_REVERSED           1.1452 +/- 0.0013      2.9797 +/- 0.0938      1.2146
spread_30_RANDOM             1.1874 +/- 0.0537      2.6298 +/- 0.7849      1.1812
spread_30_STRUCTURED         1.1503 +/- 0.0027      2.0686 +/- 0.0264      1.131
spread_30_REVERSED           1.1591 +/- 0.0023      2.4986 +/- 0.0861      1.2208
```

*(16 filas: las 13 configuraciones del barrido incluyen los tres modos por spread desde 2, más el control de spread 1.)*

### Las cuatro filas de spread 30 y 15, verbatim y completas

```
RESULT spread_15_STRUCTURED {"sel_peak": {"n": 20, "mean": 1.1235, "sd": 0.0027, "min": 1.1189, "max": 1.1288}, "sel_post": {"n": 20, "mean": 2.2781, "sd": 0.0259, "min": 2.2253, "max": 2.3246}, "sel_constant": {"n": 20, "mean": 1.1619, "sd": 0.0042, "min": 1.1532, "max": 1.17}, "control_double": {"n": 20, "mean": 1.1409, "sd": 0.0006, "min": 1.1395, "max": 1.1419}, "peak_looming": {"n": 20, "mean": 0.1845, "sd": 0.0011, "min": 0.1826, "max": 0.1862}}
RESULT spread_15_REVERSED   {"sel_peak": {"n": 20, "mean": 1.1452, "sd": 0.0013, "min": 1.1429, "max": 1.1474}, "sel_post": {"n": 20, "mean": 2.9797, "sd": 0.0938, "min": 2.8393, "max": 3.1832}, "sel_constant": {"n": 20, "mean": 1.1185, "sd": 0.0084, "min": 1.1048, "max": 1.1374}, "control_double": {"n": 20, "mean": 1.2146, "sd": 0.0012, "min": 1.2116, "max": 1.2164}, "peak_looming": {"n": 20, "mean": 0.1554, "sd": 0.0015, "min": 0.1529, "max": 0.1587}}
RESULT spread_30_STRUCTURED {"sel_peak": {"n": 20, "mean": 1.1503, "sd": 0.0027, "min": 1.1454, "max": 1.1557}, "sel_post": {"n": 20, "mean": 2.0686, "sd": 0.0264, "min": 2.0126, "max": 2.1178}, "sel_constant": {"n": 20, "mean": 1.1398, "sd": 0.0072, "min": 1.1264, "max": 1.1536}, "control_double": {"n": 20, "mean": 1.131, "sd": 0.0007, "min": 1.1293, "max": 1.1322}, "peak_looming": {"n": 20, "mean": 0.1814, "sd": 0.0016, "min": 0.1786, "max": 0.1839}}
RESULT spread_30_REVERSED   {"sel_peak": {"n": 20, "mean": 1.1591, "sd": 0.0023, "min": 1.1548, "max": 1.1629}, "sel_post": {"n": 20, "mean": 2.4986, "sd": 0.0861, "min": 2.3725, "max": 2.6906}, "sel_constant": {"n": 20, "mean": 1.0826, "sd": 0.0103, "min": 1.0664, "max": 1.1059}, "control_double": {"n": 20, "mean": 1.2208, "sd": 0.0015, "min": 1.217, "max": 1.2231}, "peak_looming": {"n": 20, "mean": 0.1444, "sd": 0.0021, "min": 0.141, "max": 0.1491}}
DONE in 511.8 s -> /tmp/run/tau_sweep.json
```

---

## 4. Los dos contrastes que decide este barrido

### A · STRUCTURED contra REVERSED, en `sel_peak`, spread por spread

| Spread | STRUCTURED | REVERSED | ¿Gana la asignación biológica? |
|---|---|---|---|
| 2 | 1,0599 ± 0,0008 | **1,0802 ± 0,0006** | **no** |
| 4 | 1,0726 ± 0,0015 | **1,1040 ± 0,0009** | **no** |
| 8 | 1,0972 ± 0,0022 | **1,1276 ± 0,0011** | **no** |
| 15 | 1,1235 ± 0,0027 | **1,1452 ± 0,0013** | **no** |
| 30 | 1,1503 ± 0,0027 | **1,1591 ± 0,0023** | **no** |

**5 de 5, y con `sd` de tercera cifra: la asignación de constantes rápidas a las poblaciones visuales y lentas a las centrales da MENOS selectividad de pico que su reverso exacto.**

### B · `sel_post` contra la dispersión

| Spread | RANDOM | STRUCTURED |
|---|---|---|
| **1 (homogénea)** | **4,3287** | — |
| 2 | 4,2328 | 3,8616 |
| 4 | 3,9853 | 3,1302 |
| 8 | 3,5189 | 2,5819 |
| 15 | 3,0157 | 2,2781 |
| 30 | 2,6298 | **2,0686** |

**Monotónicamente decreciente en los dos modos.** La dispersión de `tau` **destruye** la selectividad post-estímulo, y la asignación estructurada la destruye más rápido.

---

## 5. Defectos declarados de esta corrida

1. **🔴 El `sel_post = 4,3287` NO tiene null.** El control de signo barajado de la corrida anterior se midió **solo sobre `sel_peak`**. **Sin el equivalente para `sel_post`, ese 4,33 es un número crudo y no un resultado.** Es el experimento que sigue y es barato.
2. **El sign-shuffle de 1,1131 ± 0,0185 se midió con `tau` FIJA.** Comparar contra él los valores de spread 15 y 30 **mezcla dos condiciones** y no es válido: es el modo de falla 5 de este proyecto. Hace falta el sign-shuffle **a cada spread**.
3. **`sel_peak` y `sel_post` se mueven en direcciones OPUESTAS con la dispersión.** No se decidió cuál es la métrica correcta para «selectividad temporal», y **el veredicto depende de esa elección.**
4. **La partición rápido/lento usa `super_class`**, con 303 de 864 neuronas en las clases «rápidas». Las 11 `tau` regionales del motor son **andamio sintético hardcodeado**, no medición, así que STRUCTURED es **una hipótesis de asignación, no la asignación real**.
5. **`tau` es real, no compleja.** El motor usa `tau` compleja con `Im(tau) ~ U(0,01 , 0,15)`, que es un banco de osciladores. **Eso no se barrió, y es la diferencia con el motor real.**
6. **Solo se estimula LC4+LPLC2**, escalar por población, sin campo receptivo espacial y sin entrada multimodal.
7. **Una sola ventana** (onset 20, duración 60, 200 pasos). `sel_post` integra desde el paso 80 y **depende de cuántos pasos quedan**: no se barrió la longitud.
8. **La normalización por columna y el radio espectral fijo** igualan la ganancia entre configuraciones a propósito, así que este barrido **no dice nada sobre ganancia**.
