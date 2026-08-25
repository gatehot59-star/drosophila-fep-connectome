# Evidencia cruda · circuito de escape contra el null de neuropilos

**Corrida:** 2026-08-25 04:02 a 04:06 UTC · **`DONE in 234.6 s`**
**Instrumento:** `src/escape_neuropil_null.py`, md5 `c04ddd4282ada4f9df462f87d84d85ba`

```
python3 escape_neuropil_null.py \
  --conn /workspace/connectivity.parquet --ann /workspace/annotations.tsv \
  --pre /tmp/np/pre.feather --post /tmp/np/post.feather \
  --nulls 40 --out /tmp/run/escape_null.json
```

**Poblaciones** (por `cell_type`, todas presentes en el grafo):

```
{"LC4": 104, "LPLC2": 210, "LC6": 125, "LC9": 179, "LPLC1": 140, "GF": 2, "DNp09": 2}
GF == DNp01.  neuropil labels 79, unassigned_out 283, unassigned_in 495
blocks with more than one edge 3796
graph nodes 138639 edges 15091983
```

---

## 1. Paso 1 · OPORTUNIDAD: dónde pone sus sinapsis cada población

**Salida (sitios presinápticos por neuropilo), verbatim, top 6:**

```
OUT LC4    {"PVLP_L": 23057, "PVLP_R": 17438, "LO_L": 9037, "LO_R": 8429, "PLP_R": 2920, "PLP_L": 715}
OUT LPLC2  {"PVLP_R": 59385, "PVLP_L": 59195, "LO_L": 9613, "LO_R": 9379, "LOP_R": 7912, "LOP_L": 6331}
OUT LC6    {"PVLP_R": 39008, "PVLP_L": 29074, "PLP_L": 9158, "LO_L": 5794, "LO_R": 5623, "AVLP_R": 3472}
OUT LC9    {"PVLP_R": 46226, "LO_R": 45292, "LO_L": 42967, "PVLP_L": 38868, "AVLP_R": 9829, "LAL_L": 5311}
OUT LPLC1  {"LO_R": 25870, "LO_L": 24708, "PVLP_L": 14035, "PLP_L": 11175, "PVLP_R": 10546, "PLP_R": 10505}
OUT GF     {"PVLP_L": 558, "PVLP_R": 548, "AVLP_R": 151, "GOR_L": 143, "AMMC_L": 126, "GOR_R": 119}
OUT DNp09  {"GNG": 5147, "IPS_R": 1505, "IPS_L": 1171, "WED_L": 443, "VES_L": 359, "WED_R": 357}
```

**Entrada (sitios postsinápticos por neuropilo), verbatim, top 6:**

```
IN LC4    {"LO_R": 66418, "LO_L": 65259, "PVLP_L": 3792, "PVLP_R": 3243, "PLP_R": 241, "LOP_L": 156}
IN LPLC2  {"LOP_R": 55827, "LO_L": 42497, "LO_R": 39320, "LOP_L": 34854, "PVLP_R": 13849, "PVLP_L": 13054}
IN LC6    {"LO_L": 28389, "LO_R": 27760, "PVLP_R": 5584, "PVLP_L": 4287, "PLP_L": 1439, "AVLP_R": 511}
IN LC9    {"PVLP_R": 25234, "LO_R": 24523, "LO_L": 22049, "PVLP_L": 21514, "AVLP_R": 6923, "LAL_L": 2427}
IN LPLC1  {"LO_R": 86406, "LO_L": 84072, "LOP_R": 40204, "LOP_L": 23475, "PLP_L": 4597, "PLP_R": 4205}
IN GF     {"PVLP_L": 2127, "PVLP_R": 1958, "AMMC_R": 1101, "AMMC_L": 1054, "AVLP_R": 860, "GOR_R": 850}
IN DNp09  {"AVLP_R": 2351, "PVLP_R": 1966, "PVLP_L": 1326, "ICL_R": 1246, "AVLP_L": 847, "ICL_L": 619}
```

### 🔑 La tabla que decide el caso sin necesidad de estadística

`shared_min_sites` = suma sobre neuropilos compartidos del mínimo entre sitios de salida de la fuente y sitios de entrada del blanco. Es la **cota superior de oportunidad** de conexión.

| Par | Neuropilos compartidos | `shared_min_sites` | Aristas reales |
|---|---|---|---|
| **LC6 → GF** | **7** | **5.335** | **0** |
| LPLC2 → GF | 7 | 5.075 | **189** |
| LC9 → GF | 7 | 5.335 | **0** |
| **LC4 → GF** | 9 | **4.523** | **104** |
| LPLC1 → GF | 9 | 4.478 | 0 |

**LC6 tiene MÁS oportunidad que LC4 (5.335 contra 4.523) y conecta CERO donde LC4 conecta 104.** El neuropilo dominante de salida de LC6 es **PVLP** (39.008 + 29.074 sitios), y el neuropilo dominante de entrada del Giant Fiber es **PVLP** (2.127 + 1.958). **Comparten el territorio principal, y masivamente.**

---

## 2. Paso 2 · El null que preserva neuropilos, verbatim

```
observed {"LC4->GF": 104, "LC4->DNp09": 0, "LPLC2->GF": 189, "LPLC2->DNp09": 32,
          "LC6->GF": 0, "LC6->DNp09": 1, "LC9->GF": 0, "LC9->DNp09": 114,
          "LPLC1->GF": 0, "LPLC1->DNp09": 0, "_MIRROR_edges_into_GF": 962}

RESULT LC4->GF      {"observed": 104, "null_mean": 9.600,  "null_sd": 2.990, "null_min": 5,  "null_max": 16, "nulls_ge_observed": 0,  "ratio": 10.8333, "z": 31.57}
RESULT LC4->DNp09   {"observed": 0,   "null_mean": 4.950,  "null_sd": 2.085, "null_min": 1,  "null_max": 11, "nulls_ge_observed": 40, "ratio": 0.0,     "z": -2.37}
RESULT LPLC2->GF    {"observed": 189, "null_mean": 19.375, "null_sd": 4.351, "null_min": 13, "null_max": 30, "nulls_ge_observed": 0,  "ratio": 9.7548,  "z": 38.98}
RESULT LPLC2->DNp09 {"observed": 32,  "null_mean": 11.375, "null_sd": 3.519, "null_min": 2,  "null_max": 21, "nulls_ge_observed": 0,  "ratio": 2.8132,  "z": 5.86}
RESULT LC6->GF      {"observed": 0,   "null_mean": 17.200, "null_sd": 3.068, "null_min": 12, "null_max": 25, "nulls_ge_observed": 40, "ratio": 0.0,     "z": -5.61}
RESULT LC6->DNp09   {"observed": 1,   "null_mean": 8.700,  "null_sd": 2.590, "null_min": 3,  "null_max": 14, "nulls_ge_observed": 40, "ratio": 0.1149,  "z": -2.97}
RESULT LC9->GF      {"observed": 0,   "null_mean": 11.925, "null_sd": 2.978, "null_min": 3,  "null_max": 17, "nulls_ge_observed": 40, "ratio": 0.0,     "z": -4.00}
RESULT LC9->DNp09   {"observed": 114, "null_mean": 15.075, "null_sd": 3.467, "null_min": 9,  "null_max": 23, "nulls_ge_observed": 0,  "ratio": 7.5622,  "z": 28.53}
RESULT LPLC1->GF    {"observed": 0,   "null_mean": 0.225,  "null_sd": 0.418, "null_min": 0,  "null_max": 1,  "nulls_ge_observed": 40, "ratio": 0.0,     "z": -0.54}
RESULT LPLC1->DNp09 {"observed": 0,   "null_mean": 16.800, "null_sd": 3.437, "null_min": 10, "null_max": 24, "nulls_ge_observed": 40, "ratio": 0.0,     "z": -4.89}

RESULT _MIRROR_edges_into_GF {"observed": 962, "null_mean": 962.0, "null_sd": 0.0,
                              "nulls_ge_observed": 40, "ratio": 1.0, "z": null,
                              "sd_zero_reason": "conserved"}
```

**El espejo a propósito:** el total de aristas que entran al Giant Fiber es **962 observadas y 962 en las 40 realizaciones, `sd` exactamente 0**. Es una cantidad que ninguna permutación de destinos puede tocar. **Los diez pares de interés NO se comportan así** (todos con `sd` entre 0,42 y 4,35), o sea que **son testeables**, y eso queda demostrado dentro de la misma corrida en vez de argumentado.

---

## 3. Verificación cruzada contra las mediciones históricas

| Cantidad | Medición vieja | Esta corrida | ¿Coincide? |
|---|---|---|---|
| LC4 → GF | 104 | **104** | ✅ exacto |
| LPLC2 → GF | 189 | **189** | ✅ exacto |
| LC6 → GF | 0 | **0** | ✅ exacto |
| población LC4 / LPLC2 / LC6 | 104 / 210 / 125 | **104 / 210 / 125** | ✅ exacto |
| LPLC2 → DNp09 | **170** | **32** | 🔴 **NO** |
| población DNp09 | **4** | **2** | 🔴 **NO** |

### 🔴 La discrepancia de DNp09, resuelta midiendo

```
ct==DNp09: 2    hb==DNp09: 4
LPLC2->DNp09 por cell_type:      N= 2  aristas= 32
LPLC2->DNp09 por hemibrain_type: N= 4  aristas= 170
union:                           N= 4  aristas= 170
hb con DNp01: []   <- el Giant Fiber solo existe como cell_type
```

**Las dos mediciones son correctas y son poblaciones distintas.** La corrida histórica usó `hemibrain_type == 'DNp09'` (4 neuronas, 170 aristas); esta usó `cell_type == 'DNp09'` (2 neuronas, 32 aristas). **Nunca se declaró cuál.**

**El resultado central no se afecta:** el Giant Fiber **no existe** como `hemibrain_type`, solo como `cell_type == 'DNp01'`, así que para los pares → GF hay una única definición posible y los tres números históricos se reproducen exactos.

**NO MEDIDO: los pares → DNp09 no se re-corrieron con la definición de 4 neuronas**, así que sus ratios contra el null valen para la población de 2 y **no son comparables con el 3,6× histórico**.

---

## 4. Defectos declarados de esta corrida

1. **`shared_min_sites` es una cota, no una medición de contacto.** Dos neuronas pueden tener sitios en el mismo neuropilo y estar a decenas de micrones. **No se midió distancia entre árboles.**
2. **El null asigna a cada neurona UN neuropilo dominante**, no reparte sus sinapsis. Es la misma familia que el NPC de Lin, no idéntico.
3. **El null no preserva el grado entrante exacto**, solo dentro de bloque.
4. **Sin umbral de sinapsis** (`--threshold 1`). No re-corrido a ≥5.
5. **LPLC1 → GF es NO TESTEABLE**: el null predice 0,225, o sea ≈ 0, así que ahí sí conserva la cantidad medida y ese cero **sí** es geometría.
6. **No se barrió la literatura** para ver si esta tabla de ruteo ya está publicada.
