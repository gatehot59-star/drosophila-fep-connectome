# Evidencia cruda · null anatómico y barrido con umbral 5

**Corrida:** 2026-08-25 03:14 a 03:34 UTC · **`DONE in 1280.8 s`**

**Instrumento:** `src/twohop_nulls.py`, md5 `a3d52df61a2bc2ccbb332a01c1353dba`, 469 líneas.

```
python3 twohop_nulls.py \
  --conn /workspace/connectivity.parquet \
  --ann  /workspace/annotations.tsv \
  --pre  /tmp/np/pre.feather \
  --post /tmp/np/post.feather \
  --nulls 40 --thresholds 1 5 --outdir /tmp/run/out
```

**Entradas y su procedencia:**

| Archivo | Tamaño | md5 / origen |
|---|---|---|
| `connectivity.parquet` | 100.804.642 B | `3d802fd542b5d18570ba1ba0bb0abed9` |
| `annotations.tsv` | 31.718.505 B | `719904abad876c68ace1b5690c9b9b63` |
| `per_neuron_neuropil_count_pre_783.feather` | 16.853.770 B | **Zenodo 10676866**, v783.0, público sin login |
| `per_neuron_neuropil_count_post_783.feather` | 233.843.050 B | **Zenodo 10676866**, v783.0 |

**Salidas, por md5 (derivadas, no commiteadas según la política del repo):**

```
8a1806e9b16db8c4d3210523d51622ef  fig_twohop_a_pathcount.svg    168.751 B
c420213caa112be0db40bb7049fc81a9  fig_twohop_b_reach.svg         31.788 B
6ffc18be441974d6fbe7239c6daef572  fig_twohop_c_normalised.svg    24.186 B
3e3165a6f2b345d720af33a081a6578d  twohop_nulls.json              29.732 B
a67a6298c73f6e7d6231b2250a48e15e  twohop_nulls_raw.json          61.481 B
```

`twohop_nulls_raw.json` contiene **las 40 realizaciones individuales de cada ensemble**, que es lo que permite recomputar cualquier `sd` o rank de abajo.

---

## 1. Guards, verbatim

### Umbral 1

```
=== threshold 1 ===
  edges 15091983 of 15091983 (1.0 retained)
  nodes 138639
  motor in graph: 110-definition 110, 105-definition 105
  class sizes {"olfactory": 2279, "visual": 10855, "mechanosensory": 2656,
               "gustatory": 408, "CTRL_arbitrary": 10855}
  guard {"permutation_preserves_in_degree": true,
         "uniform_preserves_in_degree": false,
         "nodes_with_in_degree_broken_by_uniform": 138140,
         "nodes_total": 138639,
         "edges_retargeted_by_permutation": 15091661,
         "self_loops_observed": 0, "self_loops_permuted": 317}
  observed {"olfactory": {"R1": 0, "R2": 23, "P2": 901, "H1": 3184},
            "visual": {"R1": 0, "R2": 15, "P2": 1413, "H1": 21019},
            "mechanosensory": {"R1": 64, "R2": 110, "P2": 293022, "H1": 5601},
            "gustatory": {"R1": 10, "R2": 107, "P2": 67439, "H1": 1793},
            "CTRL_arbitrary": {"R1": 110, "R2": 110, "P2": 312457, "H1": 123117},
            "_MIRROR_edges_into_motor": {"R1": 0, "R2": 0, "P2": 19860, "H1": 0}}
  neuropil blocks {"neuropils": 79,
                   "neurons_without_output_neuropil": 283,
                   "neurons_without_input_neuropil": 495}
```

### Umbral 5

```
=== threshold 5 ===
  edges 2700513 of 15091983 (0.1789 retained)
  nodes 134181
  motor in graph: 110-definition 109, 105-definition 105
  class sizes {"olfactory": 2170, "visual": 7778, "mechanosensory": 2165,
               "gustatory": 405, "CTRL_arbitrary": 7778}
  guard {"permutation_preserves_in_degree": true,
         "uniform_preserves_in_degree": false,
         "nodes_with_in_degree_broken_by_uniform": 132116,
         "nodes_total": 134181,
         "edges_retargeted_by_permutation": 2700355,
         "self_loops_observed": 0, "self_loops_permuted": 90}
  observed {"olfactory": {"R1": 0, "R2": 1, "P2": 7, "H1": 635},
            "visual": {"R1": 0, "R2": 8, "P2": 247, "H1": 7352},
            "mechanosensory": {"R1": 33, "R2": 102, "P2": 26142, "H1": 1808},
            "gustatory": {"R1": 2, "R2": 78, "P2": 4625, "H1": 891},
            "CTRL_arbitrary": {"R1": 97, "R2": 109, "P2": 27688, "H1": 60832},
            "_MIRROR_edges_into_motor": {"R1": 0, "R2": 0, "P2": 7305, "H1": 0}}
  neuropil blocks {"neuropils": 79,
                   "neurons_without_output_neuropil": 51,
                   "neurons_without_input_neuropil": 190}
```

**Los tres controles se leen acá:** la permutación preserva el grado entrante exacto, el método uniforme lo rompe en 138.140 de 138.639 nodos (**así que el guard puede dar rojo**), y `_MIRROR_edges_into_motor` es la cantidad conservada a propósito.

**Verificación cruzada por reimplementación:** los valores observados a umbral 1 (`R1` 0, `R2` 23, `P2` 901 para olfatorio; 0, 15, 1413 para visual; 64, 110, 293022 para mechano) **coinciden exactamente** con los de las tres corridas ad hoc de la resp 061, escritas con otro código.

---

## 2. Ensemble de GRADO, verbatim

### Umbral 1

```
DEGREE olfactory      P2 obs 901.0     mean 39522.550 sd  745.663 ratio 0.022797 z  -51.79 ge 40 | R1 obs 0.0  mean 71.325 ge 40 | R2 obs 23.0  mean 110.000 sd 0.000 saturated
DEGREE visual         P2 obs 1413.0    mean 23311.550 sd  405.338 ratio 0.060614 z  -54.03 ge 40 | R1 obs 0.0  mean 52.275 ge 40 | R2 obs 15.0  mean 110.000 sd 0.000 saturated
DEGREE mechanosensory P2 obs 293022.0  mean 39787.800 sd  740.236 ratio 7.364619 z  342.10 ge  0 | R1 obs 64.0 mean 70.650 ge 35 | R2 obs 110.0 mean 110.000 sd 0.000 conserved
DEGREE gustatory      P2 obs 67439.0   mean 10304.100 sd  229.680 ratio 6.544870 z  248.76 ge  0 | R1 obs 10.0 mean 27.450 ge 40 | R2 obs 107.0 mean 109.950 sd 0.218
DEGREE CTRL_arbitrary P2 obs 312457.0  mean 479029.575 sd 7188.540 ratio 0.652271 z  -23.17 ge 40 | R1 obs 110.0 mean 109.000 ge 15 | R2 obs 110.0 mean 110.000 sd 0.000 conserved
```

### Umbral 5

```
DEGREE olfactory      P2 obs 7.0      mean 4652.375  sd  229.417 ratio 0.001505 z  -20.25 ge 40 | R1 obs 0.0  mean 36.650 ge 40 | R2 obs 1.0   mean 107.250 sd 1.043
DEGREE visual         P2 obs 247.0    mean 5315.425  sd  303.246 ratio 0.046469 z  -16.71 ge 40 | R1 obs 0.0  mean 38.875 ge 40 | R2 obs 8.0   mean 107.325 sd 1.034
DEGREE mechanosensory P2 obs 26142.0  mean 4498.025  sd  245.536 ratio 5.811884 z   88.15 ge  0 | R1 obs 33.0 mean 34.275 ge 27 | R2 obs 102.0 mean 107.150 sd 0.937
DEGREE gustatory      P2 obs 4625.0   mean 1765.625  sd  137.368 ratio 2.619469 z   20.82 ge  0 | R1 obs 2.0  mean 16.075 ge 40 | R2 obs 78.0  mean 105.350 sd 1.542
DEGREE CTRL_arbitrary P2 obs 27688.0  mean 43978.750 sd 2079.236 ratio 0.629577 z   -7.83 ge 40 | R1 obs 97.0 mean 98.500 ge 34 | R2 obs 109.0 mean 108.850 sd 0.357
```

**Nota sobre `R2` a umbral 5:** el `sd` deja de ser cero (1,04 y 1,03). **El censurado por techo era un artefacto del grafo sin umbral**, y a umbral 5 el estadístico de reach sí es estimable.

---

## 3. Ensemble de NEUROPILOS, verbatim — el que da vuelta el resultado

### Umbral 1

```
NEUROPIL olfactory      P2 obs 901.0    mean   2450.650 sd  349.233 ratio 0.367658 z  -4.44 ge 40 | R1 obs 0.0  mean   1.025 ge 40 | R2 obs 23.0  mean 105.500 sd 1.844
NEUROPIL visual         P2 obs 1413.0   mean    922.850 sd  119.604 ratio 1.531126 z   4.10 ge  0 | R1 obs 0.0  mean   0.025 ge 40 | R2 obs 15.0  mean  52.125 sd 4.966
NEUROPIL mechanosensory P2 obs 293022.0 mean 364783.600 sd 3485.372 ratio 0.803276 z -20.59 ge 40 | R1 obs 64.0 mean  98.550 ge 40 | R2 obs 110.0 mean 110.000 sd 0.000 conserved
NEUROPIL gustatory      P2 obs 67439.0  mean 106654.650 sd 1053.158 ratio 0.632312 z -37.24 ge 40 | R1 obs 10.0 mean 101.550 ge 40 | R2 obs 107.0 mean 110.000 sd 0.000 saturated
NEUROPIL CTRL_arbitrary P2 obs 312457.0 mean 309398.775 sd 2587.150 ratio 1.009884 z   1.18 ge  6 | R1 obs 110.0 mean 109.100 ge 15 | R2 obs 110.0 mean 110.000 sd 0.000 conserved
```

### Umbral 5

```
NEUROPIL olfactory      P2 obs 7.0     mean    57.875 sd  24.798 ratio 0.120950 z  -2.05 ge 40 | R1 obs 0.0  mean  0.000 ge 40 | R2 obs 1.0   mean  11.025 sd 3.778
NEUROPIL visual         P2 obs 247.0   mean    50.700 sd  18.061 ratio 4.871795 z  10.87 ge  0 | R1 obs 0.0  mean  0.000 ge 40 | R2 obs 8.0   mean  10.425 sd 2.355
NEUROPIL mechanosensory P2 obs 26142.0 mean 26835.125 sd 437.285 ratio 0.974171 z  -1.59 ge 38 | R1 obs 33.0 mean 89.200 ge 40 | R2 obs 102.0 mean 107.650 sd 0.572
NEUROPIL gustatory      P2 obs 4625.0  mean 12305.250 sd 245.501 ratio 0.375856 z -31.28 ge 40 | R1 obs 2.0  mean 91.000 ge 40 | R2 obs 78.0  mean 107.275 sd 0.866
NEUROPIL CTRL_arbitrary P2 obs 27688.0 mean 24131.650 sd 355.040 ratio 1.147373 z  10.02 ge  0 | R1 obs 97.0 mean 97.925 ge 32 | R2 obs 109.0 mean 108.950 sd 0.218
```

---

## 4. El diagnóstico de co-localización, verbatim

Neuropilo de **salida dominante** (el que concentra la mayor cantidad de sitios presinápticos de cada neurona):

```
SALIDA_DOMINANTE_MOTORAS {'GNG': 89, 'PRW': 15, 'IPS_L': 3, 'IPS_R': 2, 'FLA_R': 1}

SALIDA_DOM olfactory      {'AL_L': 1295, 'AL_R': 981, 'NINGUNO': 6}
SALIDA_DOM visual         {'LA_L': 4250, 'LA_R': 3836, 'ME_R': 1315, 'ME_L': 1307}
SALIDA_DOM mechanosensory {'GNG': 1712, 'SAD': 468, 'AMMC_R': 242, 'AMMC_L': 164}
SALIDA_DOM gustatory      {'GNG': 353, 'PRW': 52, 'SAD': 3}
```

**104 de las 110 motoras tienen su salida dominante en GNG o PRW.** Mechanosensorial y gustativa también. Olfatoria vive en AL, visual en LA y ME. **Las cuatro clases NO son «igual de locales»: dos son locales al neuropilo motor y dos son locales a neuropilos sensoriales.**

---

## 5. Defectos del instrumento y del turno, declarados

1. **Un `grado_check_in` de la corrida ad hoc de la resp 061 comparaba `bincount(dst)` contra sí mismo**, o sea no podía fallar. En este instrumento el guard tiene control negativo real (`degree_guard`).
2. **Un estadístico de reach de una corrida ad hoc intermedia estaba mal calculado** (contaba destinos de 1 salto, no motoras a 2 saltos). En este instrumento `R2` sale de una sola definición usada por los dos ensembles y por los dos umbrales.
3. **El `echo $?` del shell devolvió `exit=0` sobre un traceback de Python** durante el smoke test. El traceback es la señal; el código de salida de este shell no.
4. **`--pre`/`--post` se leen dos veces por umbral** (43 M de filas cada vez). Es el cuello de botella de los 1.280 s y no se optimizó.
5. El ensemble de neuropilos **no preserva el grado entrante exacto**, solo dentro de cada bloque. Es la misma renuncia que hace el NPC de Lin y va declarada, no escondida.
