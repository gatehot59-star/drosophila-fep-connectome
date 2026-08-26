# EVIDENCIA CRUDA · 2026-08-26 · auditoría v1 vs v2, las dos corridas sobre el mismo input

**Instrumento:** `gateway build.run` sobre `brain-env`. Los dos archivos se importan como
módulos (`importlib`) y se llaman sus funciones reales. **E-01: el sujeto son los archivos,
no una reimplementación.**

---

## 1. Inventario (`tools/auditoria_v1_vs_v2_inventario.py`)

```
  v1: 27 funciones/clases   v2: 45

[A] SOLO EN v1 (1) -> desaparecieron o se renombraron
    build_complex_weights                  (pre, post, w, n, phase_jitter=0.1, seed=42)

[B] SOLO EN v2 (19) -> capacidades NUEVAS
    build_config                           (args)
    build_weights                          (pre, post, w, n, mode=WEIGHT_COMPLEX, phase_jitter=0.1, seed=42)
    coalesce_edges                         (pre, post, w, n)
    infer_inhibitory                       (pre, w, n)
    make_null                              (kind, pre, post, n, block_of_node, seed)
    nulls_needed_for                       (alpha)
    p_floor_two_sided                      (n_nulls)
    rankdata_naive                         (v)
    run_self_tests                         (D=None, null_kind="cp")
    spectral_radius_arpack                 (W, tol=1e-8, maxiter=5000)
    spectral_radius_power                  (W, n_iter=500, tol=1e-10, seed=7)
    statistic_names                        (snap)
    synthetic_graph                        (n=3000, e=90000, n_blocks=10, p_intra=0.70, frac_inh=0.30, n_mods=4, s)
    test_arms_are_different_functions      ()
    test_metric_guards                     ()
    test_power_guard                       ()
    test_rankdata_vectorizado              ()
    test_spectral_normalization            ()
    validate_statistical_power             (n_nulls, alpha=0.05, strict=False)

[C] COMUNES (26)  ->  identicas: 0   cambiadas: 26

[D] LAS FIRMAS QUE CAMBIARON (contrato distinto)
    global_rank_test      v1: (real, nulls, names)                v2: (real, nulls, names, alpha=0.05)
    lg                    v1: (s)                                 v2: (msg)
    load_connectome       v1: (data_dir)                          v2: (data_dir, modalities=MODALITIES, download=True)
    main                  v1: ()                                  v2: (argv=None)
    md5_of                v1: (path)                              v2: (path, chunk=1048576)
    measure_graph         v1: (..., stim, tau_c, tau_r, label)     v2: (..., stim, cfg, label)
    normalize_spectral    v1: (W, target=0.99, n_iter=200, tol=1e-10)  v2: (W, target=0.99, n_iter=500, tol=1e-10, rel_tol=0.02)
    null_maslov_sneppen   v1: (..., seed=0)                       v2: (..., seed=0, max_rounds=20000)
    propagate             v1: (..., save_at=None)                 v2: (..., save_at=None, clip=2.0)
    test_null_preserves_degree  v1: (pre, post, n, bin_of)        v2: (pre, post, n, bin_of, kind="cp")
```

---

## 2. LA FÍSICA: idéntica. Medido, no leído.

Grafo de prueba generado **fuera** de los dos motores: n=4000, 62.889 aristas crudas con
3.000 duplicadas a propósito, 59.266 pares únicos.

```
[2] NORMALIZACION ESPECTRAL, sobre la MISMA matriz
    v1 devuelve 3 valores: ['csr_matrix', 'float', 'bool']
    v2 devuelve 2 valores: ['csr_matrix', 'dict']
    radio espectral REAL de la salida:  v1=0.989999763   v2=0.989999763   target=0.99
    lo que cada uno REPORTA:            v1=(7.194096580215254, True)
                                        v2=({'rho_pre': 7.194096580215254, 'pre_converged': True,
                                             'scale': 0.13761283143218217, 'rho_post_power': 0.9899999999999992,
                                             'post_converged': True, 'rho_post_arpack': 0.9899997633854589,
                                             'arpack_measur...
    |salida1-salida2| max = 0.000000e+00

[3] TAU  (make_tau)
    |tau1-tau2| max = 0.000000e+00
    Re v1=0.119000  Re v2=0.119000   |Im| medio v1=0.079724  v2=0.079724

[4] LA DINAMICA  (propagate), MISMA W, MISMO tau
    |z_final| max v1=1.000610945   v2=1.000610945
    |z1-z2| max = 0.000000e+00
      snapshot t=20  |dif| max = 0.000000e+00
      snapshot t=40  |dif| max = 0.000000e+00
      snapshot t=59  |dif| max = 0.000000e+00

[METRICAS] sobre EXACTAMENTE los mismos vectores
    region_profile   |dif| max = 0.000000e+00
    cosine_distance  v1=0.000100054331  v2=0.000100054331  dif=0.000e+00
    rdi              v1=(0.0012750172229900603, 3, 0)
                     v2=(0.0012750172229900603, 3, 0)
    phase_coherence  v1=0.581680290045  v2=0.581680290045
    rankdata empates v1=[4.0, 1.5, 1.5, 3.0, 6.0, 6.0, 6.0]
                     v2=[4.  1.5 1.5 3.  6.  6.  6. ]

    -- el caso que separaria a los dos: un vector MUERTO --
      v1  cosine(muerto,vivo)=nan   phase_coherence(muerto)=nan
      v2  cosine(muerto,vivo)=nan   phase_coherence(muerto)=nan
```

**Nota importante y contra una lectura cómoda:** el guard de NaN sobre vectores muertos
**ya estaba en v1**. No es una mejora de v2. Lo que v2 agrega es `rdi()` devolviendo el
conteo de pares excluidos y el `NO_TESTEABLE` del test global, no el NaN en sí.

---

## 3. LO ÚNICO NUMÉRICO QUE CAMBIA: el jitter de fase

(`tools/auditoria_v1_vs_v2_pesos.py`)

```
  v2 valores 2 y 3: [False True True ...] | {'edges_in': 62889, 'edges_out': 59266, 'merged_multi_edges': 3623}
  mismos indices? True
  nnz 59266 vs 59266

[MAGNITUD]  |w|
    v1: min=0.086692  med=1.040823  max=11.463150  suma=75224.4190
    v2: min=0.086692  med=1.040917  max=11.463150  suma=75242.9762
    | |w1|-|w2| |  max=1.181004e-01  medio=3.131171e-04  cuantos difieren>1e-12: 3548 de 59266

[FASE]  angulo
    |fase1-fase2|  max=0.622399  medio=0.112362  cuantos difieren>1e-12: 59265 de 59266

[SIGNO / reparto E-I]
    v1: parte real negativa en 18134 de 59266 aristas (30.60%)
    v2: parte real negativa en 18134 de 59266 aristas (30.60%)

[LA MISMA MATRIZ SIN JITTER DE FASE?]
    con phase_jitter=0.0  ->  |W1-W2| max = 8.881784e-16   difieren>1e-12: 0 de 59266
    *** LA DIFERENCIA ES SOLO EL JITTER DE FASE

[MODOS DE PESO]
    modos de v2: ['WEIGHT_COMPLEX', 'WEIGHT_REAL']
    modos de v1: []
```

**Lectura:** las dos funden las mismas 3.623 multi-aristas (nnz idéntico y ambos igual a
los pares únicos). El **signo** y el **reparto E/I** son idénticos (18.134 en las dos).
Las **3.548 magnitudes que difieren** son exactamente las multi-aristas fundidas: al sumar
dos complejos con fases distintas, el módulo del resultado depende de la fase. Con
`phase_jitter=0.0` la diferencia cae a **8,88e-16**, el epsilon del doble.

**Conclusión: v1 y v2 son el MISMO modelo con otra realización del ruido de fase.**

---

## 4. El test global

```
[TEST GLOBAL] mismos datos de entrada
    v1 claves: ['global', 'per_statistic']
    v2 claves: ['global', 'per_statistic', 'p_floor']
    p dos colas      v1=0.2                    v2=0.2
    S_real           v1=90.0                   v2=90.0
    piso             v1=0.2                    v2=0.2
    piso alcanzable  v1=None                   v2=False
    significativo    v1=None                   v2=False
```

**El p es el mismo. Lo que v1 NO tiene es el veredicto**: `piso alcanzable` y
`significativo` son `None` en v1 porque esas claves no existen.

---

## 5. PERFORMANCE, min de 3 corridas, misma máquina

```
    tarea                v1 min(s)    v2 min(s)    v2/v1
    build_weights        0.0157       0.0251       1.600
    normalize_spectral   0.0422       0.1830       4.339
    propagate 60 pasos   0.0514       0.0509       0.991
    rankdata 5k          0.0100       0.0416       4.174
```

**v2 es MÁS LENTO en 3 de 4.** Y la que empata es `propagate`, que es **el 96,2% del
tiempo** de una corrida real (medido en el parche GPU). O sea: v2 paga 4,3× en funciones
que corren **una vez por grafo** y 0,99× en la que corre 150 veces por estímulo.

---

## 6. Lo que v2 puede y v1 no (llamadas reales)

```
    validate_statistical_power(9)    v1: NO EXISTE en v1    v2: (0.2, 39, False)
    validate_statistical_power(39)   v1: NO EXISTE en v1    v2: (0.05, 39, True)
    p_floor_two_sided(9)             v1: NO EXISTE en v1    v2: 0.2
    p_floor_two_sided(39)            v1: NO EXISTE en v1    v2: 0.05
    nulls_needed_for(0.05)           v1: NO EXISTE en v1    v2: 39

  AVISO emitido por v2 al llamarla con 9: POTENCIA INSUFICIENTE: con 9 nulls el piso de p
  a dos colas es 0.2000, que NO alcanza alpha=0.0500. Hacen falta al menos 39 nulls. Este
  experimento no puede dar significativo ni en el mejor caso posible.
```

---

## 7. RETROSPECTIVA: el experimento de v1 sobre el conectoma real

Está versionado en `results/motor_ltc_complejo.log`. Verbatim:

```
[0.0s] python 3.12.13  numpy 2.0.2  scipy 1.16.3
[7.7s]   OK    md5_parquet: 3d802fd542b5d18570ba1ba0bb0abed9
[7.7s]   OK    md5_annotations: 719904abad876c68ace1b5690c9b9b63  (SHA 17fc5772)
[14.9s]   N=138639  E=15091983  regiones=10
[14.9s]   poblaciones estimuladas: [('visual', 10854), ('olfactory', 2279), ('mechanosensory', 2656)]
[15.1s]   OK    ley_de_Dale_sin_neuronas_mixtas: 0 mixtas de 138005 con salidas  (E puras 96672, I puras 41333)
[18.2s]   nulls=9  pasos=200  snapshots=[60, 120, 199]
[171.6s]   REAL            rho=2153.6528  rdi_cplx=0.3598  rdi_real=0.1634  ventaja=+0.1964
[307.4s]   CP 1/9          rho=652.3789  rdi_cplx=0.0141  rdi_real=0.0179  ventaja=-0.0038
[444.4s]   CP 2/9          rho=673.1619  rdi_cplx=0.0083  rdi_real=0.0121  ventaja=-0.0038
[583.0s]   CP 3/9          rho=712.2781  rdi_cplx=0.0119  rdi_real=0.0701  ventaja=-0.0582
[718.7s]   CP 4/9          rho=685.4027  rdi_cplx=0.0072  rdi_real=0.0397  ventaja=-0.0324
[854.2s]   CP 5/9          rho=735.2409  rdi_cplx=0.0218  rdi_real=0.0252  ventaja=-0.0034
[990.6s]   CP 6/9          rho=699.3498  rdi_cplx=0.0159  rdi_real=0.0392  ventaja=-0.0232
[1126.4s]   CP 7/9          rho=699.4599  rdi_cplx=0.0061  rdi_real=0.0688  ventaja=-0.0627
[1262.5s]   CP 8/9          rho=621.1696  rdi_cplx=0.0059  rdi_real=0.0489  ventaja=-0.0429
[1398.1s]   CP 9/9          rho=708.4012  rdi_cplx=0.0291  rdi_real=0.0427  ventaja=-0.0137
[1398.1s]   rdi_cplx_t60              real=+0.02034  null_mu=+0.12771  sd=0.01133  n_ge=9/9  p2=0.2000
[1398.1s]   rdi_cplx_t120             real=+0.80747  null_mu=+0.45317  sd=0.04048  n_ge=0/9  p2=0.2000
[1398.1s]   rdi_cplx_t199             real=+0.35985  null_mu=+0.01337  sd=0.00745  n_ge=0/9  p2=0.2000
[1398.1s]   TEST GLOBAL sobre 6 de 6 estadisticos
[1398.1s]     S_real=38.0  S_null_mu=32.4  sd=5.4  min=27.0
[1398.1s]     nulls por debajo=8/9   p dos colas=0.6000   piso alcanzable=0.2000
```

### `measure_graph` de v1, verbatim: TENÍA brazo de control

```python
def measure_graph(pre, p, w, n, bin_of, n_bins, stim, tau_c, tau_r, label):
    """Mide un grafo con tau COMPLEJA y con tau REAL, en la misma corrida."""
    W, is_inh = build_complex_weights(pre, p, w, n)
    W, rho, conv = normalize_spectral(W)
    ...
    for tag, tau in (("cplx", tau_c), ("real", tau_r)):
    ...
        res["ventaja_compleja_t" + str(t)] = (a - b) ...
```

**CORRECCIÓN DE UN CLAIM PROPIO:** en el chat afirmé que v1 tenía «cero de los cuatro
brazos» y que le faltaba «el brazo de control». Es engañoso. **v1 tenía DOS brazos**
(`tau` compleja contra `tau` real) y calculaba `ventaja_compleja`. Lo que le faltaba era
el brazo de **`W`**, que es lo que el peritaje 092 dijo con precisión y yo degradé al
repetirlo. v1 controla tau; **no** controla W. v2 hace el 2×2 completo.

---

## 8. La comparación de los dos experimentos sobre el MISMO conectoma

| | v1 (23-ago, Kaggle CPU) | v2 (26-ago, GPU + container) |
|---|---|---|
| md5 del parquet | `3d802fd542b5...` | `3d802fd542b5...` (**el mismo dato**) |
| N / E | 138.639 / 15.091.983 | 138.639 / 15.091.983 |
| brazos | **2** (tauC, tauR) | **4** (Wc/Wr × tauC/tauR) |
| modalidades / pares RDI | **3 / 3** | **4 / 6** |
| nulls | **9** | **39** |
| pasos / snapshots | 200 / 60,120,199 | 150 / 50,100,149 |
| piso del p | **0,20** | **0,05** |
| `rho` del grafo REAL | **2153,6528** | **2152,6355** |
| rdi REAL, t temprano | 0,02034 · **9/9 nulls arriba** | 0,4311 · **39/39 nulls arriba** |
| rdi REAL, t medio | 0,80747 · **0/9** | 0,7184 · **0/39** |
| rdi REAL, t final | 0,35985 · **0/9** | 0,6642 · **0/39** |
| test global | p = **0,60** (no podía ganar) | p = **0,25** (podía, no ganó) |

**Δrho = 2153,6528 − 2152,6355 = 1,0173, o sea 0,047%.** Es exactamente el orden que
explica el jitter de fase medido en la sección 3. **No es un error: es la realización del
ruido.**

**Y el hallazgo que ninguna de las dos corridas por separado podía dar: la INVERSIÓN DE
SIGNO A TIEMPO TEMPRANO REPLICA.** v1 con 9 nulls, 200 pasos, 3 modalidades y otra
semilla de fase: **9/9 arriba**. v2 con 39 nulls, 150 pasos, 4 modalidades y otra semilla:
**39/39 arriba**. Dos versiones, dos máquinas, dos semillas, dos rejillas de tiempo, mismo
signo invertido. **Eso no es artefacto de v2.**

---

## 9. NO MEDIDO

- **No se re-corrió v1 sobre el conectoma real en esta sesión.** La comparación de la
  sección 8 usa el log archivado del 23-ago. Los dos experimentos difieren en **cuatro
  variables a la vez** (brazos, modalidades, nulls, rejilla de tiempo), así que la tabla
  **no** es un A/B controlado: es un cruce de dos corridas distintas.
- El cronómetro es de la misma máquina y momento, pero **con un solo tamaño de grafo**
  (n=4000). No se barrió escala.
- `rankdata` de v2 salió **4,17× más lento** y no se investigó por qué. Nombrarlo sin
  explicarlo es lo honesto: es una medición, no un diagnóstico.
- `tools/auditoria_v1_vs_v2_pesos.py` no compara `null_maslov_sneppen` ni
  `null_community_preserving` entre versiones: los nulls quedaron fuera por pedido
  explícito («aparte de los null»).
- No se midió el consumo de memoria de ninguna de las dos.
