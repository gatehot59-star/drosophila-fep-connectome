# Evidencia cruda · compilación del Giant Fiber COMPLETO, con signo

**Corrida:** 2026-08-25 04:39–04:40 UTC · **`DONE in 48.5 s`**
**Instrumento:** `src/compile_gf_full.py`, md5 `a355274ac90182b594033542c1f4ae2f`
**Salida:** `gf_full.json`, md5 `d7ef10779b73f08d23c18ad5ed55e996`, 5.256 B (por md5, no commiteada)

```
python3 compile_gf_full.py \
  --conn /workspace/connectivity.parquet --ann /workspace/annotations.tsv \
  --steps 200 --shuffles 20 --out /tmp/run/gf_full.json
```

---

## 1. El subgrafo y los guards, verbatim

```
nodes 864 internal_edges 45687 synapses 256161
driven neurons (LC4+LPLC2) 293  target 2  central partners 475
edges into target 962  inhibitory share of internal edges 0.3462

GUARD stimulus energies {"looming": 20.5027777778, "receding": 20.5027777778,
                         "constant": 20.5027777778, "double_energy": 41.0055555556}
GUARD energy matched to 1e-9: MATCHED_OK
GUARD double_energy differs on purpose: DIFFERS_OK
```

**Los tres guards pueden dar rojo:** la energía de los tres perfiles comparables es idéntica a 10 cifras, el brazo de control positivo tiene el doble de energía **a propósito**, y el chequeo distingue los dos casos.

---

## 2. Los cuatro brazos, verbatim

```
ARM FULL {"edges_kept": 45687,
  "responses": {
    "looming":  {"peak": 0.18139962219650965, "final": 0.0006561878967067645, "integral": 7.911794694542232},
    "receding": {"peak": 0.17062691580115258, "final": 0.0005392995384523357, "integral": 7.483653242999343},
    "constant": {"peak": 0.15203643696968816, "final": 0.0007191017511675932, "integral": 9.27701958529656},
    "double_energy": {"peak": 0.2144074251426086, "final": 0.0007581533071392522, "integral": 9.743084581097134}},
  "selectivity_looming_over_receding": 1.0631,
  "selectivity_looming_over_constant": 1.1931,
  "positive_control_double_over_single": 1.182}

ARM NO_INHIB {"edges_kept": 29872,
  "responses": {
    "looming":  {"peak": 0.47009545274551456, "final": 0.22720324266049624, "integral": 51.76738546067603},
    "receding": {"peak": 0.4527114467967079,  "final": 0.21499151891177037, "integral": 55.55637488637869},
    "constant": {"peak": 0.4905469478299548,  "final": 0.2273277381647767,  "integral": 58.1972764031685},
    "double_energy": {"peak": 0.49948229343839273, "final": 0.23011387112696788, "integral": 54.89716744272616}},
  "selectivity_looming_over_receding": 1.0384,
  "selectivity_looming_over_constant": 0.9583,
  "positive_control_double_over_single": 1.0625}

ARM NO_CENTRAL {"edges_kept": 19978,
  "responses": {
    "looming":  {"peak": 0.5270640822434082, "final": 0.1421642746886062, "integral": 47.85777230442993},
    "receding": {"peak": 0.49569586736959603, "final": 0.13013768385695168, "integral": 50.38844398159379},
    "constant": {"peak": 0.526141272424998,  "final": 0.14063397050023008, "integral": 53.88340076426495},
    "double_energy": {"peak": 0.559374346987644, "final": 0.14360724021038948, "integral": 51.031246556017024}},
  "selectivity_looming_over_receding": 1.0633,
  "selectivity_looming_over_constant": 1.0018,
  "positive_control_double_over_single": 1.0613}

ARM CUT_V1 {"edges_kept": 293,
  "responses": {
    "looming":  {"peak": 0.5517899005228006, "final": 2.945664125403062e-06, "integral": 24.50494150919824},
    "receding": {"peak": 0.49583722722840223, "final": 6.098708614085582e-07, "integral": 24.56994419131985},
    "constant": {"peak": 0.48057556235839255, "final": 2.239209473607319e-06, "integral": 29.432526603653926},
    "double_energy": {"peak": 0.6417460339018068, "final": 3.5141578770926516e-06, "integral": 29.974280778397702}},
  "selectivity_looming_over_receding": 1.1128,
  "selectivity_looming_over_constant": 1.1482,
  "positive_control_double_over_single": 1.163}
```

---

## 3. El control de signo barajado, verbatim

```
  sign shuffle 10/20
  sign shuffle 20/20
SIGN_SHUFFLE {"n": 20, "mean": 1.1131, "sd": 0.0185,
              "min": 1.0598, "max": 1.1333,
              "shuffles_ge_observed": 19}
DONE in 48.5 s
```

**El real da 1,0631. El ensemble con signo barajado da 1,1131 ± 0,0185, y 19 de 20 permutaciones quedan POR ENCIMA del real.**

---

## 4. La tabla del veredicto

| Brazo | Aristas | Selectividad looming/receding | Control positivo (doble energía) |
|---|---|---|---|
| **FULL** | 45.687 | **1,0631** | 1,182 |
| NO_INHIB | 29.872 | 1,0384 | 1,0625 |
| NO_CENTRAL | 19.978 | 1,0633 | 1,0613 |
| **CUT_V1** (el recorte de la v1) | 293 | **1,1128** | 1,163 |
| **signo barajado sobre FULL** | 45.687 | **1,1131 ± 0,0185** | — |

**Y la referencia de escala:** duplicar la energía del estímulo mueve el pico solo **1,182×** en FULL. Así que el techo de lo que este lector resuelve está en ese orden, y la selectividad de 1,0631 es **un tercio** de lo que produce duplicar la energía.

---

## 5. Defectos declarados de esta corrida

1. **El modelo no es el mismo que produjo el 1,04× original.** Ese script no está en el corpus. **La comparación válida es INTERNA (FULL contra CUT_V1 en esta misma corrida), no contra el 1,04× histórico.**
2. **Solo se estimula LC4+LPLC2.** Los 39 socios sensoriales y los 28 descendentes no reciben estímulo externo: se mueven solo por recurrencia. **Un estímulo multimodal no se probó.**
3. **La normalización por columna y el radio espectral fijo igualan la ganancia entre brazos a propósito.** Eso hace la comparación justa pero **borra las diferencias de ganancia absoluta**, que es justamente donde el circuito sí muestra estructura.
4. **`tau = 0,119` fijo y único para las 864 neuronas.** El motor real usa τ heterogénea, y **ese es el parámetro con más chance de generar selectividad temporal**. No se barrió.
5. **El estímulo es escalar por población**, no espacial por campo receptivo.
6. **Un solo tamaño de ventana** (onset 20, duración 60, 200 pasos). Sin barrido.
7. **La métrica es el pico del promedio de las 2 neuronas blanco.** No se probó con integral ni con umbral de disparo, que es lo que decide un escape real.
