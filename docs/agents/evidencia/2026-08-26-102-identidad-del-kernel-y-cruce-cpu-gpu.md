# EVIDENCIA CRUDA · 2026-08-26 · qué corrió en Kaggle, y el cruce CPU contra GPU

**Instrumento:** `gateway build.run` sobre `brain-env`. **Sujeto:** `kernel_shard.py`
(lo que se subió a Kaggle), `motor_v2.py` (la versión corregida) y `motor.py` (la v1).

---

## 1. Identidad del kernel (`tools/cruce_kernel_vs_motorv2.py`)

```
==========================================================================================
QUE CORRIO EN KAGGLE  ·  cruce byte a byte contra motor_v2 y contra motor v1
==========================================================================================

[1] LOS TRES ARCHIVOS
    motor.py (v1)      30644 B    703 lineas  md5=480539069ec00f317eec525e6fa81324
    motor_v2.py        65543 B   1533 lineas  md5=8f7ad4740727478bf62b7cd0663fb341
    kernel_shard.py    76731 B   1800 lineas  md5=bfaea0cf2a2e3948970f38c7c52b2b54

[2] ESTA motor_v2 ADENTRO DEL KERNEL, VERBATIM?
    marca del parche en offset de caracter: 65593
    los primeros 200 caracteres de motor_v2 aparecen en el kernel en: 26
    segmento de igual largo desde ahi:  identico a motor_v2? False
    similitud del segmento con motor_v2: 0.9993
    cabecera del kernel ANTES de motor_v2 (26 caracteres):
    '# GENERATED kernel shard\n\n'

[3] EL CUERPO PRE-PARCHE contra motor_v2
    pre-parche: 65593 caracteres   motor_v2: 65542 caracteres   diferencia: +51
    similitud pre-parche vs motor_v2: 0.9989
    bloques de diferencia: 2
      insert   v2[     0:     0]=                     ker[     0:    26]=# GENERATED kernel shard\n\n
      replace  v2[ 65494: 65542]=if __name__ == "__main__":\n    sys.exit(main())\n   ker[ 65520: 65593]=\n# ====...

[4] EL PARCHE: que funciones DEFINE, y cuales PISAN a las del motor
    defs en motor_v2      : 45
    defs en el pre-parche : 45
    defs en el parche GPU : 5  -> gpu_info, propagate_gpu, verify_gpu_against_cpu, shard_indices, main_shard

    *** REDEFINICIONES (el parche PISA una funcion del motor): 0
    funciones NUEVAS del parche: gpu_info, propagate_gpu, verify_gpu_against_cpu, shard_indices, main_shard

[5] EL NUCLEO: hay dos propagate?
    propagate                        pre-parche=1  parche=0
    propagate_gpu                    pre-parche=0  parche=1
    rdi                              pre-parche=1  parche=0
    cosine_distance                  pre-parche=1  parche=0
    normalize_spectral               pre-parche=1  parche=0
    null_maslov_sneppen              pre-parche=1  parche=0
    build_weights                    pre-parche=1  parche=0

[6] QUE main SE EJECUTA
    bloques '__main__' en el kernel: 1
      offset  76676  if __name__ == "__main__":   -> PARCHE (corredor de shard)
    el ultimo en ejecutarse gana: PARCHE
```

**Lectura:** las **dos únicas** diferencias entre el kernel y `motor_v2.py` son una
cabecera de 26 caracteres y el `__main__` cambiado por el corredor de shard. Las **45
funciones** de `motor_v2` están verbatim y el parche **no redefine ninguna**: agrega 5
funciones nuevas. Lo que corrió en Kaggle **es la versión corregida**, no la v1.

---

## 2. La verificación GPU-contra-CPU que corrió ADENTRO del kernel

Del log de `shard0`, verbatim:

```
[20.8s] ########## VERIFICACION GPU CONTRA CPU (sobre el grafo REAL) ##########
[79.9s]   OK    gpu_reproduce_a_la_cpu: desvio relativo maximo = 3.857e-16 contra tolerancia 1.0e-09 | max|z| cpu=0.875505 gpu=0.875505
[79.9s]   (la verificacion tardo 59.1 s)
[79.9s]   BACKEND EFECTIVO: GPU
[79.9s]   propagate() reemplazada por la version GPU.
```

---

## 3. Los controles del peritaje 092 que se ejecutaron sobre el grafo REAL

```
[17.8s]   OK    tau_limite_es_0.473116: 0.473116
[17.8s]   OK    el_clip_preserva_la_fase: desvio maximo de fase = 0.000e+00
[17.8s]   OK    para_alpha_0.05_hacen_falta_39_nulls: 39
[17.8s]   AVISO: POTENCIA INSUFICIENTE: con 9 nulls el piso de p a dos colas es 0.2000, que NO alcanza alpha=0.0500...
[17.8s]   OK    9_nulls_NO_alcanzan_alpha_0.05: alcanzable=False
[17.8s]   OK    39_nulls_SI_alcanzan_alpha_0.05: alcanzable=True
[17.8s]   OK    modo_strict_ABORTA_con_potencia_insuficiente: levanto ValueError=True
[17.8s]   OK    cosine_de_un_vector_muerto_es_NaN: nan
[17.8s]   OK    rdi_excluye_los_NaN_y_los_cuenta: validos=1 excluidos=2 valor=1.0000
[17.8s]   OK    normalizacion_complex_phase_queda_en_el_target: veredicto=OK rho_pre=10.2469 rho_post=0.990000 err_rel=7.96e-11 arpack=True
[17.9s]   OK    normalizacion_real_signed_queda_en_el_target: veredicto=OK rho_pre=10.3014 rho_post=0.990000 err_rel=2.97e-09 arpack=True
[17.9s]   OK    el_veredicto_espectral_PUEDE_dar_rojo: con rel_tol=0 el veredicto es FUERA_DE_TOLERANCIA -> el test anterior mide
[17.9s]   OK    los_dos_instrumentos_espectrales_COINCIDEN: arpack=0.990000 potencia=0.990000 brecha_rel=3.147e-11
[17.9s]   OK    sin_ARPACK_la_iteracion_de_potencia_sola_alcanza: veredicto=OK rho_post=0.990000 arpack=False
[17.9s]   OK    los_dos_brazos_funden_las_MISMAS_multi_aristas: 193 fundidas en los dos
[17.9s]   OK    los_dos_brazos_comparten_el_reparto_E_I: mismas 227 inhibitorias en los dos
[17.9s]   OK    los_dos_brazos_comparten_las_MAGNITUDES: desvio maximo de |w| = 8.882e-16
[17.9s]   OK    los_dos_brazos_NO_son_la_misma_matriz: desvio maximo de w = 1.1203 -> difieren solo en la fase
[18.0s]   OK    los_dos_brazos_producen_DINAMICAS_distintas: desvio maximo del estado final = 5.1666e-02
[18.2s]   OK    ley_de_Dale_sin_neuronas_mixtas: 0 mixtas de 138005 con salidas  (E puras 96672, I puras 41333)
[20.0s]   OK    cp_preserva_grado_entrante: 0 nodos alterados de 138639
[20.1s]   OK    cp_preserva_grado_saliente: 0 nodos alterados
[20.4s]        CP crea 149589 multi-aristas (esperado: el CP las admite)
[20.8s]   OK    el_metodo_uniforme_ROMPE_el_grado: 106948 nodos alterados -> el test anterior puede fallar, o sea que mide
```

Nota importante: `los_dos_brazos_NO_son_la_misma_matriz` y
`los_dos_brazos_producen_DINAMICAS_distintas` son el guard contra el error A/B: los
brazos `Wc` y `Wr` comparten magnitudes y reparto E/I, difieren **solo en la fase**, y
producen dinamicas distintas. O sea que el brazo `W` **mide algo**, y su `p = 0,175`
no es un artefacto de comparar una funcion consigo misma.

---

## 4. Cruce CPU contra GPU, null por null (`tools/cruce_cpu_vs_gpu.py`)

```
========================================================================================
CONTROL DE INSTRUMENTO  ·  CPU (container) contra GPU (Kaggle P100)
========================================================================================

  nulls medidos en GPU : 39
  nulls medidos en CPU : 36  (etiquetas 1..36)
  REAL  CPU=0.6642   GPU=0.6642175399463487

  idx    GPU          CPU          |dif|
  0      0.0727       0.0727       4.71e-05     COINCIDE
  1      0.0522       0.0522       1.96e-05     COINCIDE
  2      0.1833       0.1833       2.41e-05     COINCIDE
  3      0.1396       0.1396       2.72e-05     COINCIDE
  4      0.2045       0.2045       6.03e-06     COINCIDE
  5      0.1251       0.1251       4.94e-05     COINCIDE
  6      0.1096       0.1096       1.84e-05     COINCIDE
  7      0.0471       0.0471       1.35e-05     COINCIDE
  8      0.1847       0.1847       1.15e-05     COINCIDE
  9      0.0763       0.0763       2.61e-05     COINCIDE
  10     0.2028       0.2028       2.41e-06     COINCIDE
  11     0.1651       0.1651       3.73e-05     COINCIDE
  12     0.2023       0.2023       1.96e-05     COINCIDE
  13     0.1645       0.1645       3.00e-05     COINCIDE
  14     0.0940       0.0940       4.08e-05     COINCIDE
  15     0.1236       0.1236       3.58e-05     COINCIDE
  16     0.1543       0.1543       4.97e-05     COINCIDE
  17     0.1490       0.1490       2.46e-05     COINCIDE
  18     0.1762       0.1762       3.07e-05     COINCIDE
  19     0.2054       0.2054       8.88e-07     COINCIDE
  20     0.1372       0.1372       1.31e-06     COINCIDE
  21     0.0314       0.0314       2.84e-05     COINCIDE
  22     0.0925       0.0925       2.95e-05     COINCIDE
  23     0.1462       0.1462       2.77e-05     COINCIDE
  24     0.1336       0.1336       1.05e-05     COINCIDE
  25     0.1815       0.1815       2.19e-05     COINCIDE
  26     0.1351       0.1351       2.74e-05     COINCIDE
  27     0.0632       0.0632       2.85e-05     COINCIDE
  28     0.1459       0.1459       3.83e-05     COINCIDE
  29     0.2456       0.2456       1.57e-05     COINCIDE
  30     0.1018       0.1018       4.28e-05     COINCIDE
  31     0.1345       0.1345       3.60e-05     COINCIDE
  32     0.1834       0.1834       4.20e-05     COINCIDE
  33     0.0995       0.0995       1.75e-05     COINCIDE
  34     0.0705       0.0705       3.92e-05     COINCIDE
  35     0.1707       0.1707       1.87e-05     COINCIDE

  pares comparables: 36
  desvio maximo entre CPU y GPU: 4.975e-05
  VEREDICTO: los dos instrumentos coinciden dentro del redondeo del log (4 decimales)
  REAL: |CPU - GPU| = 1.754e-05
```

---

## 5. NO MEDIDO

- Los desvios de la seccion 4 estan **limitados por el redondeo del log a 4 decimales**
  (4,97e-05 es exactamente el peor caso de redondear). El cruce con precision completa
  requiere el JSON final de la corrida CPU, que todavia no existe: iba en 36/39.
- El cruce se hizo sobre **una** metrica (`rdi_Wc_tauC_t149`), no sobre las 12.
- `phase_jitter` **sigue sin barrerse**.
- `null_maslov_sneppen` **no corrio sobre el grafo real**: la corrida real usa CP.
  Sobre grafo sintetico si corrio.
- La corrida CPU y la GPU comparten la **semilla** y el algoritmo del null; coinciden
  porque el null es determinista dado el indice. Eso valida el **backend**, no valida
  la eleccion del null.
