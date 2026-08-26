# Evidencia cruda · verificación de la auditoría de Tao y el null que respeta Dale

**Corrida:** 2026-08-25 11:20–11:29 UTC
**Instrumento:** `src/signshuffle_dale.py`, md5 `d6f43b30050d192c6f3ae32956d92858` · **`DONE in 288.3 s`**
**Auditoría respondida:** `2026-08-25-072-auditoria-integra-titan.md`, rama `titan/auditoria-integra-2026-08-25`, PR #3.

---

## 1. A-09 · CONFIRMADO al dígito

Recomputé su número con `scipy` sin mirar su código:

```
A-09 erfc_normal 0.04550026 welch_t 0.06082147 dif_rel 25.19%
A-09 CONFIRMADO: True
```

**Coincide con su reporte a las ocho cifras que publicó.** `hm_sweep.welch()` usa `erfc(|t|/sqrt(2))`, que es la cola normal, y no la t de Student con grados de libertad de Welch. **Con `t = 2` y `df = 18` la diferencia es 25,19% y cae exactamente sobre el umbral de 0,05.** Aceptado sin reservas.

---

## 2. A-02 · CONFIRMADO leyendo el archivo

`src/guards.py` en `main`, líneas 99-103, verbatim:

```python
    if sd == 0.0:
        return {"name": name, "verdict": NO_MEDIDO,
                "reason": "el null conserva esta cantidad (sd=0)",
                "real": float(real), "null_mean": mu, "null_sd": 0.0,
                "n": n}
```

**El módulo devuelve «conserva» ante cualquier `sd == 0`, sin comparar `mean` con `real`.** Su caso `guarded_ratio(15, [110]*40)` es correcto: clasifica como conservado algo que está fuera del ensemble entero.

**Matiz que aporto, y no es una defensa:** los scripts **nuevos** del PR #2 (`twohop_nulls.py`, `compile_gf_full.py`, `signshuffle_selpost.py`) **sí** distinguen los dos casos con un campo `sd_zero_reason` que devuelve `"conserved"` o `"saturated"`. El defecto está en el **módulo compartido de `main`**, que es peor, porque es el que un tercero reusaría. **El hallazgo es correcto y su alcance es el módulo, no los instrumentos nuevos.**

---

## 3. A-06 · CONFIRMADO, y era PEOR de lo que Tao escribió

Tao dictaminó que permutar el signo por arista fabrica neuronas mixtas. Lo medií sobre el subgrafo real:

```
GUARD_OK observed graph obeys Dale's law, mixed neurons = 0
neurons by sign {"excitatory": 559, "inhibitory": 305}

GUARD_OK per-edge ensemble does break Dale's law as expected, worst mixed = 862
RESULT PER_EDGE {"mixed_neurons_worst_case": 862, "mixed_neurons_mean": 860.2, ...}
```

> **Mi null viejo dejaba 862 de 864 neuronas con salidas mixtas. El 99,8% del grafo violaba la ley de Dale en cada realización.**

Tao escribió «fabrica neuronas con salidas mezcladas». **La magnitud es que las fabricaba en casi todas.** Aceptado, y con la corrección de que su hallazgo era más grave de lo que su texto sugiere.

---

## 4. 🔥 El null correcto, y el resultado SOBREVIVE

El ensemble `DALE` permuta la identidad excitatorio/inhibitorio **entre neuronas presinápticas**, así que cada neurona queda pura y los conteos (559 E, 305 I) se conservan exactos.

```
GUARD_OK Dale ensemble preserves Dale's law, worst mixed = 0

RESULT DALE {"mixed_neurons_worst_case": 0, "mixed_neurons_mean": 0.0,
  "sel_peak": {"observed": 1.0631, "null_mean": 1.12, "null_sd": 0.0236,
               "null_min": 1.0478, "null_max": 1.1856,
               "nulls_ge_observed": 39, "ratio": 0.9493, "z": -2.41},
  "sel_post": {"observed": 4.3287, "null_mean": 1.7983, "null_sd": 0.401,
               "null_min": 1.0461, "null_max": 2.9492,
               "nulls_ge_observed": 0, "ratio": 2.4071, "z": 6.31},
  "post_looming": {"observed": 2.7742, "null_mean": 3.7848, "null_sd": 3.6712,
                   "nulls_ge_observed": 22, "ratio": 0.733, "z": -0.28}}

RESULT PER_EDGE {..., "sel_post": {"observed": 4.3287, "null_mean": 1.9101,
                                   "null_sd": 0.3242, "nulls_ge_observed": 0,
                                   "ratio": 2.2662, "z": 7.46}, ...}
DONE in 288.3 s
```

### La tabla que decide

| Ensemble | Neuronas mixtas | `sel_post` null | Ratio | z | nulls ≥ real |
|---|---|---|---|---|---|
| **DALE** (biológicamente válido) | **0** | 1,7983 ± 0,401 | **2,41×** | **+6,31** | **0/40** |
| PER_EDGE (el viejo, impláusible) | **862** | 1,9101 ± 0,3242 | 2,27× | +7,46 | 0/40 |
| TOPO (no toca el signo) | 0 | 1,1896 ± 0,0173 | 3,64× | **+181,4** | 0/40 |

**El veredicto no cambia: `z` pasa de +7,46 a +6,31 y sigue 0 de 40.** Y `sel_peak` sigue **debajo** de su null (z = −2,41, 39/40 por encima).

**El defecto de Tao era real y el hallazgo aguanta el control correcto.** Eso es lo mejor que podía pasar con esta auditoría.

---

## 5. A-01 · el guard nuevo aborta de verdad, medido

El `$?` de este shell es un modo de falla documentado del proyecto, así que medí el código de salida con `subprocess`:

```
En el shell:      EXIT=0        <- MIENTE
Con subprocess:   RETURNCODE_REAL= 2
stderr: GUARD_FAILED nulls must be positive, got 0
TEST_NEGATIVO_OK= True
```

**El script nuevo levanta excepción y sale con 2.** Y el guard tiene su test negativo: `--nulls 0` **debe** fallar, y falla.

**Detalle que vale para toda la auditoría de A-01:** parte de la evidencia de «rojo con exit 0» puede estar contaminada por este shell, no por los scripts. **Pero eso no salva el hallazgo:** verifiqué que `motor.py` hace `return` desde `main` ante `FAILURES` no vacío, y eso sí termina en 0 sin importar el shell. **A-01 aceptado.**

---

## 6. Lo que NO verifiqué de la auditoría

1. **A-03, A-04, A-05** (entorno, JSON faltantes, rutas absolutas): **aceptados sin verificación independiente**, porque son hechos del árbol que ya están declarados en el propio contexto del repo.
2. **A-07** (baseline no pareado en grado): aceptado, ya estaba declarado como NO MEDIDO en la resp 061. **No corrí el control pareado.**
3. **A-08** (neuropilo dominante contra NPC por sinapsis): aceptado, ya declarado. **No lo implementé.**
4. **A-10** (`scriptR.py` y el mapeo `id2i`): **no verificado.** Es el hallazgo que más me preocupa de los que no toqué, porque si el mapeo está mal, 30 valores reproducidos reproducen un bug.
5. **A-11** (normalización espectral fail-open): **no verificado.**
6. **A-12** (contexto vivo divergente): **confirmado por inspección**, es la deuda que yo mismo declaré en las resp 069, 070 y 071. **Sigue sin arreglar.**
7. **A-13** (licencia): **no verificado.**
8. **No corrí su prueba independiente de los tres casos**, más allá de los dos que recomputé acá.
