# Evidencia cruda · `motor.py` EJECUTADO y su presupuesto contra un ESP32

**Fecha:** 2026-08-25 17:55 (America/Buenos_Aires) · **Instrumento:** sandbox propio, Python 3.12 / numpy 2.4.6, 2 núcleos x86.

**Qué se corrió:** las funciones de `src/motor.py` verbatim (copiadas sin modificar su lógica), sobre un grafo de 3.000 nodos / 89.773 aristas con ley de Dale exacta y estructura de 10 bloques. **El conectoma real de 15.091.983 aristas NO se descargó en esta corrida** (sin red hacia los datasets), así que el sujeto de la corrida es *el código*, no *el grafo del paper*. Eso se declara y no se disfraza.

<hr/>

## 1. Salida cruda de `run_motor.py`, verbatim

```plain
### numpy 2.4.6

########## BLOQUE 1-2 · TESTS DE UNIDAD (sujeto exacto: funciones de motor.py) ##########
[0.0s]   OK    tau_limit_es_0.473116: 0.473116
[0.0s]   OK    tau_acepta_el_default: (0.01, 0.15) con Re=0.119
[0.0s]   OK    tau_rechaza_0.48: |1-tau| seria 1.003275 > 1
[0.0s]   OK    tanh_cruda_explota: |tanh| max = 9.998e+11
[0.0s]   OK    tanh_acotada_respeta_el_clip: |f| max = 2.000000
[0.0s]   OK    el_clip_preserva_la_fase: desvio maximo de fase = 0.000e+00

########## BLOQUE 3-4 · TESTS SOBRE LOS DATOS ##########
  N=3000  E=89773  bloques=10
[0.0s]   OK    ley_de_Dale_sin_neuronas_mixtas: 0 mixtas de 3000 con salidas  (E puras 2110, I puras 890)
[0.0s]   OK    CP_preserva_grado_entrante: 0 nodos alterados de 3000
[0.1s]        CP crea 2391 multi-aristas (esperado: el CP las admite)
[0.1s]   OK    CP_preserva_grado_saliente: 0 nodos alterados
[0.1s]   OK    el_metodo_uniforme_ROMPE_el_grado: 2817 nodos alterados -> el test anterior puede fallar, o sea que mide

  FAILURES acumulados: []

########## BLOQUE 5-6 · EXPERIMENTO (CP nulls, tau compleja vs tau real) ##########
  tau compleja Re=0.119 Im in (0.01,0.15)  limite de estabilidad=0.473116
  nulls=9 pasos=120 snapshots=[40, 80, 119]
  REAL           rho=14.6228  rdi_cplx=0.0042  rdi_real=0.0406  ventaja=-0.0365  coh=0.8634
  CP 1/9         rho=14.6465  rdi_cplx=0.0048  rdi_real=0.0376  ventaja=-0.0328  coh=0.8240
  CP 2/9         rho=14.8169  rdi_cplx=0.0042  rdi_real=0.0566  ventaja=-0.0523  coh=0.8098
  CP 3/9         rho=15.0038  rdi_cplx=0.0023  rdi_real=0.0165  ventaja=-0.0141  coh=0.8626
  CP 4/9         rho=15.5318  rdi_cplx=0.0005  rdi_real=0.0330  ventaja=-0.0325  coh=0.8706
  CP 5/9         rho=15.1799  rdi_cplx=0.0021  rdi_real=0.0207  ventaja=-0.0186  coh=0.8514
  CP 6/9         rho=15.6003  rdi_cplx=0.0023  rdi_real=0.0381  ventaja=-0.0358  coh=0.8745
  CP 7/9         rho=15.6278  rdi_cplx=0.0035  rdi_real=0.0332  ventaja=-0.0297  coh=0.8818
  CP 8/9         rho=14.9234  rdi_cplx=0.0040  rdi_real=0.0469  ventaja=-0.0429  coh=0.8303
  CP 9/9         rho=14.7389  rdi_cplx=0.0047  rdi_real=0.0355  ventaja=-0.0308  coh=0.8217
  tiempo del experimento: 2.6 s

########## BLOQUE 7 · RESULTADO ##########
  rdi_cplx_t40               real=+0.70408 null_mu=+0.71670 sd=0.01485 n_ge=7/9 p2=0.6000
  rdi_cplx_t80               real=+0.17763 null_mu=+0.19870 sd=0.02998 n_ge=7/9 p2=0.6000
  rdi_cplx_t119              real=+0.00419 null_mu=+0.00318 sd=0.00135 n_ge=3/9 p2=0.8000
  ventaja_compleja_t40       real=-0.08006 null_mu=-0.07649 sd=0.00556 n_ge=7/9 p2=0.6000
  ventaja_compleja_t80       real=-0.14381 null_mu=-0.14119 sd=0.00989 n_ge=6/9 p2=0.8000
  ventaja_compleja_t119      real=-0.03645 null_mu=-0.03217 sd=0.01082 n_ge=7/9 p2=0.6000

  TEST GLOBAL sobre 6 de 6 estadisticos
    S_real=23.0 S_null_mu=34.1 sd=5.1 min=24.0
    nulls por debajo=0/9  p dos colas=0.2000  piso alcanzable=0.2000

  FAILURES finales: []
  motor_resultados.json escrito: 11856 B
```

<hr/>

## 2. Salida cruda de `presupuesto_esp32.py`, verbatim

```plain
==============================================================================
PRESUPUESTO: el motor complejo de motor.py contra un ESP32
==============================================================================
  N   = 138639 neuronas
  NNZ = 15091983 aristas

  --- como esta escrito: complex128 + int32 ---
    estado z                 2,218,224 B
    tau por neurona          2,218,224 B
    W datos                241,471,728 B
    W indices+indptr        60,922,492 B
    RAM viva minima          4,436,448 B  =     4.23 MB   ->      8.3x la SRAM del ESP32
    pesos (a flash)        302,394,220 B  =   288.39 MB   ->     72.1x el flash de 4MB
    TOTAL                  306,830,668 B  =   292.62 MB
    con PSRAM de 8MB    NO ENTRA (36.6x por encima)

  --- comprimido a complex64 (float32) + int32 ---
    estado z                 1,109,112 B
    tau por neurona          1,109,112 B
    W datos                120,735,864 B
    W indices+indptr        60,922,492 B
    RAM viva minima          2,218,224 B  =     2.12 MB   ->      4.2x la SRAM del ESP32
    pesos (a flash)        181,658,356 B  =   173.24 MB   ->     43.3x el flash de 4MB
    TOTAL                  183,876,580 B  =   175.36 MB
    con PSRAM de 8MB    NO ENTRA (21.9x por encima)

  Ni la version comprimida entra. Y comprimir cambia el sujeto medido.

==============================================================================
COMPUTO POR PASO
==============================================================================
  W^T z es un SpMV complejo: 60,367,932 mult. reales por paso (4 por arista complejo)
  + 138,639 tanh complejas + 138,639 mult. complejas del update
  DualBrain embebido, medido:            3,440 MAC por paso
  factor motor.py / DualBrain:             17549x

==============================================================================
MEDICION REAL: costo de un paso a escala reducida, y extrapolacion
==============================================================================
  n= 20000 nnz=   400000  rho=   9.1352 conv=True      1.88 ms/paso  (host x86, 2 nucleos)
                    extrapolado a las 15.091.983 aristas:    71.03 ms/paso ->  14.08 pasos/s en HOST
  n= 60000 nnz=  1200000  rho=   9.0757 conv=True      7.56 ms/paso  (host x86, 2 nucleos)
                    extrapolado a las 15.091.983 aristas:    95.04 ms/paso ->  10.52 pasos/s en HOST

  Un ESP32 a 240 MHz es del orden de 100-1000x mas lento que este host por FLOP.
  O sea: minutos u horas por paso, si la memoria alcanzara. Y no alcanza.

==============================================================================
VEREDICTO
==============================================================================
  motor.py NO puede ser el motor del ESP32. No es opinion: es 8x la RAM y 72x el flash.
  DualBrain embebido: 800 B RAM / 15704 B flash. Ese SI es el del chip.
  Relacion de tamano entre los dos motores: 4248x en parametros.
```

<hr/>

## 3. Veredicto derivado (conclusión, no medición)

1. **Los 8 tests de `motor.py` dieron verde y el control del control dio su rojo esperado.** El instrumento funciona: `el_metodo_uniforme_ROMPE_el_grado` alteró 2.817 nodos, o sea que el test de preservación de grado **podía** fallar.
2. **La respuesta a «¿este no debería ser el motor del ESP32?» es NO, y ahora está medida:** 8,3× la SRAM sólo para el estado vivo, 72× el flash para los pesos, y ni comprimido a float32 entra en 8 MB de PSRAM.
3. **El cómputo lo confirma por otra vía:** 60.367.932 multiplicaciones reales por paso contra 3.440 MAC del DualBrain embebido. **17.549×.**
4. 🔴 **Hallazgo del turno, y es un defecto real de `normalize_spectral`:** con este grafo `rho` salió **14,62 y no 0,99**. La función escala por `target/rho`, pero después se vuelve a medir el radio espectral **de la matriz escalada** y da 14,6: o sea que **el valor devuelto como `rho` no deja el sistema en 0,99 en este régimen**. Con pesos lognormales y grado alto, la iteración de potencia converge (`conv=True`) a un valor que no cumple lo que el docstring promete. **No es un bug de la corrida: es un bug del sujeto.**
5. 🔴 **La «ventaja compleja» salió NEGATIVA en los tres snapshots**, tanto en el grafo estructurado como en los nueve CP. O sea: en este régimen la `tau` real le gana a la compleja. Coincide en signo con el `p = 0,6000` ya registrado y **angosta más el claim**.
6. **El test global dio `p = 0,2000`, que es exactamente el piso alcanzable con 9 nulls.** `S_real = 23,0` contra `S_null_min = 24,0`: el grafo estructurado quedó **por debajo de los nueve nulls**, o sea 0/9. Con 9 nulls eso **no puede** producir un p publicable ni en el mejor caso. Es un problema de diseño del número de nulls, no de la hipótesis.

<hr/>

## 4. NO MEDIDO, declarado

1. **No se corrió sobre el conectoma real.** El grafo es sintético con ley de Dale exacta y bloques. Los números de `rdi`, `rho` y `p` **no son los del paper** y no deben citarse como tales.
2. **`load_connectome()` no se ejecutó**, así que los md5 del parquet y de las anotaciones **no se verificaron** en esta corrida.
3. **`null_maslov_sneppen()` no se corrió.** Sólo el community-preserving. El MS es el caro y quedó afuera.
4. **El presupuesto de ESP32 es aritmética exacta sobre tamaños de tipos, no una compilación cruzada.** El ms/paso extrapolado es del host x86; **el número del ESP32 sigue sin medirse en chip**.
5. **El factor «100-1000× más lento» del ESP32 es una estimación de orden**, no una medición. Se etiqueta como tal.
6. **El bug de `normalize_spectral` no se corrigió en el repo.** Se declara acá y su fix va en un commit propio, con su propio test que pueda dar rojo.

```plain
--- METODO TITAN ---
Accion delicada: NO (ejecucion en sandbox propio, cero escrituras en datos ajenos)
Modo aplicado:   TITAN FULL
Rubrica:         instrumento de diagnostico -> Completitud, Ejecutabilidad,
                 Documentacion, Proceso QA aplicables
N/A declarados:  Seguridad, Testing, DevOps, Arquitectura, Innovacion
Review externo:  no pedido (evidencia, no PR de codigo)
Instrumento:     python3.12 / numpy 2.4.6 en sandbox propio, exit 0 las dos corridas.
                 Salida cruda de las dos arriba, verbatim y sin recortar.
```