# EVIDENCIA CRUDA · 2026-08-26 · la suite que autoriza el fix de rankdata

**Instrumento:** `gateway build.run` sobre `brain-env`. `tools/test_rankdata_v3.py`,
corrido ANTES de tocar el motor. Exit 0.

---

## 1. Equivalencia contra las tres implementaciones existentes

```
    caso                                   n        vs v1        vs v2_naive  vs v2_vect
    un solo elemento                       1        OK           OK           OK
    dos iguales                            2        OK           OK           OK
    todos iguales                          9        OK           OK           OK
    todos distintos                        6        OK           OK           OK
    el caso del docstring                  7        OK           OK           OK
    ya ordenado                            12       OK           OK           OK
    orden inverso                          12       OK           OK           OK
    negativos y cero                       5        OK           OK           OK
    cero negativo                          3        OK           OK           OK
    muy grandes y muy chicos               4        OK           OK           OK
    con infinitos                          5        OK           OK           OK
    40 elementos, como el test global      40       OK           OK           OK
    1000 con muchos empates                1000     OK           OK           OK
    1000 sin empates                       1000     OK           OK           OK
```

## 2. Propiedades que valen por definicion

```
    caso                                   suma       empates    monotonia    rango 1..n
    (los 14 casos)                         OK         OK         OK           OK
```

Las cuatro: suma de rangos = n(n+1)/2 · valores iguales con rango igual · monotonia ·
rango contenido en 1..n.

## 3. Los mutantes: la suite DETECTA los 5

```
    mutante                            detectado    primer caso que lo mata
    sin el +1 (0-based)                SI           un solo elemento
    no promedia empates                SI           dos iguales
    no vuelve al orden original        SI           todos distintos
    ordena descendente                 SI           el caso del docstring
    c/2 en vez de (c-1)/2              SI           un solo elemento
```

**Sin esto la suite no autorizaba nada.** Un test que pasa con el codigo roto no mide.

## 4. La ganancia, medida

```
    caso                       unicos    v2_vect      v3           v3/v2        ganancia
    5k sin empates             5000      0.057854     0.001034     0.0179       55.9x
    50k sin empates            50000     0.567109     0.011701     0.0206       48.5x
    50k con 100 valores        100       0.008773     0.007298     0.8319       1.2x
    40 (el uso real)           40        0.000693     0.000307     0.4429       2.3x
```

**CORRIGE a la respuesta 106.** Ahi escribi "impacto nulo en el experimento actual".
Medido: **2,3x en el tamano real de uso** (40 elementos). Chico, pero **no nulo**, y
decir "nulo" era redondear a favor de mi propia conclusion.

## 5. Veredicto de la suite

```
VERDE: 14 casos x 3 referencias equivalentes, 4 propiedades por caso,
       y 5 de 5 mutantes DETECTADOS. La suite puede dar rojo, o sea que mide.
       El cambio del motor queda AUTORIZADO por esta suite.
```

---

## 6. Despues de aplicar el fix: la suite PROPIA del motor, completa

```
  OK    tau_limite_es_0.473116: 0.473116
  OK    tau_acepta_el_default: (0.01, 0.15) con Re=0.119
  OK    tau_rechaza_0.48: |1-tau| seria 1.003275 > 1
  OK    tanh_cruda_explota: |tanh| max = 9.998e+11
  OK    tanh_acotada_respeta_el_clip: |f| max = 2.000000
  OK    el_clip_preserva_la_fase: desvio maximo de fase = 0.000e+00
  OK    el_clip_preserva_el_signo_en_el_brazo_real: signos [1.0, -1.0, 1.0]
  OK    piso_de_p_con_9_nulls_es_0.20: 0.2000
  OK    piso_de_p_con_99_nulls_es_0.02: 0.0200
  OK    para_alpha_0.05_hacen_falta_39_nulls: 39
  AVISO: POTENCIA INSUFICIENTE: con 9 nulls el piso de p a dos colas es 0.2000...
  OK    9_nulls_NO_alcanzan_alpha_0.05: alcanzable=False
  OK    39_nulls_SI_alcanzan_alpha_0.05: alcanzable=True
  OK    modo_strict_ABORTA_con_potencia_insuficiente: levanto ValueError=True
  OK    rankdata_vectorizado_coincide_con_el_ingenuo: desvio maximo = 0.000e+00 sobre 30 vectores con empates
  OK    cosine_de_un_vector_muerto_es_NaN: nan
  OK    rdi_excluye_los_NaN_y_los_cuenta: validos=1 excluidos=2 valor=1.0000
  OK    coherencia_de_una_red_apagada_es_NaN: nan
  OK    el_test_global_marca_NO_TESTEABLE_NAN: NO_TESTEABLE_NAN
  OK    el_test_global_marca_NO_TESTEABLE_con_sd_cero: NO_TESTEABLE
  OK    normalizacion_complex_phase_queda_en_el_target: veredicto=OK rho_pre=10.2469 rho_post=0.990000 err_rel=6.69e-11 arpack=True
  OK    normalizacion_real_signed_queda_en_el_target: veredicto=OK rho_pre=10.3014 rho_post=0.990000 err_rel=3.08e-09 arpack=True
  AVISO: la normalizacion espectral quedo FUERA DE TOLERANCIA. target=0.9900 rho_post=0.990000 err_rel=0.0000
  OK    el_veredicto_espectral_PUEDE_dar_rojo: con rel_tol=0 el veredicto es FUERA_DE_TOLERANCIA -> el test anterior mide
  OK    los_dos_instrumentos_espectrales_COINCIDEN: arpack=0.990000 potencia=0.990000 brecha_rel=6.407e-11
  OK    sin_ARPACK_la_iteracion_de_potencia_sola_alcanza: veredicto=OK rho_post=0.990000 arpack=False
  OK    los_dos_brazos_funden_las_MISMAS_multi_aristas: 193 fundidas en los dos
  OK    los_dos_brazos_comparten_el_reparto_E_I: mismas 227 inhibitorias en los dos
  OK    los_dos_brazos_comparten_las_MAGNITUDES: desvio maximo de |w| = 8.882e-16
  OK    los_dos_brazos_NO_son_la_misma_matriz: desvio maximo de w = 1.1203 -> difieren solo en la fase
  OK    los_dos_brazos_producen_DINAMICAS_distintas: desvio maximo del estado final = 5.1666e-02
  OK    ley_de_Dale_sin_neuronas_mixtas: 0 mixtas de 3000 con salidas  (E puras 2092, I puras 908)
  OK    cp_preserva_grado_entrante: 0 nodos alterados de 3000
  OK    cp_preserva_grado_saliente: 0 nodos alterados
       CP crea 598 multi-aristas (esperado: el CP las admite)
  OK    el_metodo_uniforme_ROMPE_el_grado: 2774 nodos alterados -> el test anterior puede fallar, o sea que mide

TESTS EN ROJO DEL MOTOR: []
```

---

## 7. Un error propio de este mismo turno, registrado

El primer parche dejo una **linea muerta**: `ranks_sorted = np.empty(n, ...)` que la
linea siguiente sobreescribia de inmediato. Es el **patron 2 del Bloque 8** (la
constante que nadie consulta) cometido mientras arreglaba otra cosa. Se detecto
leyendo la funcion de vuelta y se limpio en el mismo turno.

Y un segundo, del entorno: al reescribir el docstring, el wrapper del gateway
**ejecuto los backticks** de `` `start` `` y `` `c` `` como sustitucion de comando y los
borro del archivo, dejando "que arranca en  y tiene ". Se detecto por el stderr
(`sh: 1: start: not found`) y se reparo. **Regla 13 del entorno: nada de backticks en
el texto que se pasa por build.run, ni en comentarios.**

---

## 8. Cadena de md5

```
8f7ad4740727478bf62b7cd0663fb341   pre-fix   <- el que embeben los 5 kernels en vuelo
3d10505da2deebaac756b37b2d9a56c0   intermedio (con la linea muerta)
e3d037bd4d14eabd95e81129fb863687   intermedio (docstring mutilado por el shell)
22f9904bcae82225876d8f0be9fac127   post-fix  <- el del container, verde en las dos suites
```

Los kernels llevan su copia embebida y verifican su md5 al arrancar, asi que el cambio
**no contamina la corrida en vuelo**. Los cuatro hashes van publicados para que la
secuencia sea auditable y no haya que creerme el orden.

---

## 9. NO MEDIDO

- El fix **no se probo en GPU**: `rankdata` corre en CPU en las dos versiones.
- No se midio con `n > 50.000` sin empates.
- `src/motor_v2.py` en git **no se sobrescribio**: se entrega el diff aplicable. Un
  archivo de 66 KB reescrito a mano es exactamente donde se trunca en silencio, y eso
  es peor que un placeholder.
- La suite no cubre entradas con **NaN**: `np.unique` los agrupa al final y el
  comportamiento correcto en ese caso **no esta especificado** por el motor. Se declara
  en vez de inventar una expectativa.
