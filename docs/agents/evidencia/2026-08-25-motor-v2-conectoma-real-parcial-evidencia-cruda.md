# Evidencia cruda · motor v2 sobre el CONECTOMA REAL · PARCIAL 1/39

**Fecha:** 2026-08-25 20:50 (America/Buenos_Aires)

**Estado:** 🟡 **EN CURSO, NO CERRADO.** 1 de 39 nulls. El proceso 9604 está vivo. Nada de lo que sigue es un veredicto final, y el test global **todavía no existe**.

**Instrumento:** `build.run` sobre `brain-env`. Python 3.12.14, numpy 2.5.2, scipy 1.18.1, ARPACK=True.

**Comando exacto:**

```plain
python3 motor_v2.py --data-dir /workspace --out-dir /workspace/motor_v2_real \
                    --nulls 39 --steps 150
```

<hr/>

## 1. Los datos reales, verificados por checksum

```plain
[1.0s]   OK    md5_parquet: 3d802fd542b5d18570ba1ba0bb0abed9
[1.0s]   OK    md5_annotations: 719904abad876c68ace1b5690c9b9b63  (SHA 17fc5772)
[32.6s]   anotaciones: 138625 de 139248 matchean un nodo; 623 NO matchean y quedan SIN region (declarado, no oculto)
[33.1s]   N=138639  E=15091983  regiones=10
[33.1s]   poblaciones estimuladas: [('visual', 10854), ('olfactory', 2279), ('mechanosensory', 2656), ('gustatory', 408)]
[33.1s]   el RDI descansa en 6 pares de 4 modalidades (declarado: es el limite de muestra de la metrica)
```

**Los dos md5 coinciden**, así que este ES el grafo sobre el que se midieron los priors. Y el conteo de anotaciones huérfanas de la v2 confirma el número que estaba en el aire: **623 filas exactas** no matchean ningún nodo.

<hr/>

## 2. Los 25 invariantes sobre datos reales, verbatim

```plain
[33.1s]   OK    tau_limite_es_0.473116: 0.473116
[33.1s]   OK    tau_acepta_el_default: (0.01, 0.15) con Re=0.119
[33.1s]   OK    tau_rechaza_0.48: |1-tau| seria 1.003275 > 1
[33.1s]   OK    tanh_cruda_explota: |tanh| max = 9.998e+11
[33.1s]   OK    tanh_acotada_respeta_el_clip: |f| max = 2.000000
[33.1s]   OK    el_clip_preserva_la_fase: desvio maximo de fase = 0.000e+00
[33.1s]   OK    el_clip_preserva_el_signo_en_el_brazo_real: signos [1.0, -1.0, 1.0]
[33.1s]   OK    piso_de_p_con_9_nulls_es_0.20: 0.2000
[33.1s]   OK    piso_de_p_con_99_nulls_es_0.02: 0.0200
[33.1s]   OK    para_alpha_0.05_hacen_falta_39_nulls: 39
[33.1s]   AVISO: POTENCIA INSUFICIENTE: con 9 nulls el piso de p a dos colas es 0.2000, que NO alcanza alpha=0.0500. Hacen falta al menos 39 nulls. Este experimento no puede dar significativo ni en el mejor caso posible.
[33.1s]   OK    9_nulls_NO_alcanzan_alpha_0.05: alcanzable=False
[33.1s]   OK    39_nulls_SI_alcanzan_alpha_0.05: alcanzable=True
[33.1s]   OK    modo_strict_ABORTA_con_potencia_insuficiente: levanto ValueError=True
[33.2s]   OK    rankdata_vectorizado_coincide_con_el_ingenuo: desvio maximo = 0.000e+00 sobre 30 vectores con empates
[33.2s]   OK    cosine_de_un_vector_muerto_es_NaN: nan
[33.3s]   OK    rdi_excluye_los_NaN_y_los_cuenta: validos=1 excluidos=2 valor=1.0000
[33.3s]   OK    coherencia_de_una_red_apagada_es_NaN: nan
[33.3s]   OK    el_test_global_marca_NO_TESTEABLE_NAN: NO_TESTEABLE_NAN
[33.3s]   OK    el_test_global_marca_NO_TESTEABLE_con_sd_cero: NO_TESTEABLE
[34.1s]   OK    normalizacion_complex_phase_queda_en_el_target: veredicto=OK rho_pre=10.2469 rho_post=0.990000 err_rel=8.98e-11 arpack=True
[34.4s]   OK    normalizacion_real_signed_queda_en_el_target: veredicto=OK rho_pre=10.3014 rho_post=0.990000 err_rel=2.94e-09 arpack=True
[34.8s]   AVISO: la normalizacion espectral quedo FUERA DE TOLERANCIA. target=0.9900 rho_post=0.990000 err_rel=0.0000
[34.8s]   OK    el_veredicto_espectral_PUEDE_dar_rojo: con rel_tol=0 el veredicto es FUERA_DE_TOLERANCIA -> el test anterior mide
[34.9s]   OK    los_dos_instrumentos_espectrales_COINCIDEN: arpack=0.990000 potencia=0.990000 brecha_rel=6.429e-11
[35.0s]   OK    sin_ARPACK_la_iteracion_de_potencia_sola_alcanza: veredicto=OK rho_post=0.990000 arpack=False
[35.1s]   OK    los_dos_brazos_funden_las_MISMAS_multi_aristas: 193 fundidas en los dos, de 16000 aristas crudas -> 15807 pares unicos
[35.1s]   OK    los_dos_brazos_comparten_el_reparto_E_I: mismas 227 inhibitorias en los dos
[35.1s]   OK    los_dos_brazos_comparten_las_MAGNITUDES: desvio maximo de |w| = 8.882e-16
[35.1s]   OK    los_dos_brazos_NO_son_la_misma_matriz: desvio maximo de w = 1.1203 -> difieren solo en la fase
[35.4s]   OK    los_dos_brazos_producen_DINAMICAS_distintas: desvio maximo del estado final = 5.1666e-02

[35.4s] ########## TESTS SOBRE LOS DATOS ##########
[35.8s]   OK    ley_de_Dale_sin_neuronas_mixtas: 0 mixtas de 138005 con salidas  (E puras 96672, I puras 41333)
[41.4s]   OK    cp_preserva_grado_entrante: 0 nodos alterados de 138639
[41.5s]   OK    cp_preserva_grado_saliente: 0 nodos alterados
[68.2s]        CP crea 149589 multi-aristas (esperado: el CP las admite)
[68.8s]   OK    el_metodo_uniforme_ROMPE_el_grado: 106948 nodos alterados -> el test anterior puede fallar, o sea que mide
```

### Lo que estas líneas cierran, sobre el grafo real y no sobre uno sintético

1. **La ley de Dale es EXACTA en el conectoma real:** 0 neuronas mixtas de 138.005 con salidas. 96.672 puramente excitatorias, 41.333 puramente inhibitorias. El comentario del archivo dejó de ser comentario.
2. **El null CP preserva grado entrante y saliente en las 138.639 neuronas:** 0 nodos alterados.
3. **Y el control del control funciona a escala real:** el método uniforme altera **106.948 nodos**, o sea que el test anterior sí podía dar rojo.
4. 🔴 **El CP crea 149.589 multi-aristas sobre el grafo real.** Ese es exactamente el confound que el `coalesce_edges` de la v2 neutraliza, y acá se ve por qué importaba: **149.589 no es un detalle de borde**.

<hr/>

## 3. 🔥 El avance del 2x2, verbatim

```plain
[68.8s] ########## EXPERIMENTO 2x2 ##########
[68.8s]   brazos: Wc_tauC, Wc_tauR, Wr_tauC, Wr_tauR
[68.8s]   nulls=39 (cp)  pasos=150  snapshots=[50, 100, 149]
[68.8s]   piso de p=0.0500  alpha=0.0500  alcanzable=True

[1218.5s]   REAL         rho_post=0.9900 [OK]  rdi(Wc,tauC)=0.6642  vent_tau=+0.0060  vent_W=+0.0021  clip=0.00
[1983.1s]   CP 1/39      rho_post=0.9900 [OK]  rdi(Wc,tauC)=0.0727  vent_tau=-0.0597  vent_W=-0.0096  clip=0.00
```

<hr/>

## 4. Veredicto derivado · PROVISORIO (conclusión, no medición)

**Con un solo null no hay test. Lo que sigue es lectura de dos filas, y puede caerse con los 38 que faltan.**

<table><tbody><tr><th width="220" cell-bg-color="grey"><p><strong>cantidad</strong></p></th><th width="220" cell-bg-color="grey"><p><strong>REAL</strong></p></th><th width="220" cell-bg-color="grey"><p><strong>CP 1</strong></p></th><th width="220" cell-bg-color="grey"><p><strong>lectura</strong></p></th></tr><tr><td width="220"><p><code>rdi(Wc,tauC)</code></p></td><td width="220"><p><strong>0,6642</strong></p></td><td width="220"><p><strong>0,0727</strong></p></td><td width="220"><p><strong>9,13×</strong><span> a favor del real</span></p></td></tr><tr><td width="220"><p><code>ventaja_tau</code></p></td><td width="220"><p><strong>+0,0060</strong></p></td><td width="220"><p><strong>−0,0597</strong></p></td><td width="220"><p><strong>cambia de signo</strong></p></td></tr><tr><td width="220"><p><code>ventaja_W</code></p></td><td width="220"><p><strong>+0,0021</strong></p></td><td width="220"><p><strong>−0,0096</strong></p></td><td width="220"><p><strong>cambia de signo</strong></p></td></tr><tr><td width="220"><p><code>rho_post</code></p></td><td width="220"><p>0,9900 [OK]</p></td><td width="220"><p>0,9900 [OK]</p></td><td width="220"><p>la normalización cierra en el real</p></td></tr><tr><td width="220"><p><code>frac_at_clip</code></p></td><td width="220"><p>0,00</p></td><td width="220"><p>0,00</p></td><td width="220"><p>no hay saturación: la dinámica no está al tope</p></td></tr></tbody></table>

<p><br/></p>

1. **El punto 5 del peritaje queda CERRADO y en contra de mi propia sospecha.** Yo dejé escrito que faltaba verificar si el defecto de `normalize_spectral` aparecía con los pesos reales. Con el conectoma real, `rho_post = 0.9900` con veredicto **OK** y los dos instrumentos coincidiendo. **No aparece.** El defecto era de contrato, no de aritmética, y ahora está medido sobre el sujeto correcto.
2. 🟡 **El brazo de `W` deja de ser «NO MEDIDO» y pasa a «medido, sin test todavía».** Su magnitud es chica (+0,0021) contra un `rdi` de 0,6642, o sea **0,32% del valor**. Si eso se sostiene con los 39 nulls, la lectura honesta va a ser que **la aritmética compleja aporta poco**, no que aporta mucho. Pero **falta el test**: sin la distribución de los 39 no hay `p`.
3. **La señal grande no está en los contrastes: está en el `rdi` crudo.** 0,6642 contra 0,0727 es un orden de magnitud. Si se sostiene, el resultado del expediente no es «la tau compleja gana» sino **«el cableado real diferencia modalidades y el control modular no»**.

<hr/>

## 5. ⏱️ El costo medido, que cambia la planificación

```plain
REAL:    68,8 s -> 1218,5 s   =  1149,7 s
CP 1:  1218,5 s -> 1983,1 s   =   764,6 s por null
```

**38 nulls restantes × 764,6 s = 29.055 s = 8,07 horas.** Total desde el arranque: **~8,6 h**.

> Eso **no era estimable desde el sintético**, donde los 39 nulls tardaron 41,6 s. El factor real es de **~700×** por null. Es la clase de dato que decide si una corrida se lanza o se reparte, y por eso este parcial se commitea ahora en vez de esperar el cierre.

<hr/>

## 6. NO MEDIDO, declarado

1. **El test global NO existe todavía.** Cualquier `p` sobre el conectoma real sería inventado en este momento.
2. **`ventaja_W` tiene un solo punto de comparación.** Un cambio de signo entre el real y UN null no es un efecto: es una observación.
3. **`null_maslov_sneppen` no se corrió sobre el conectoma real.** Solo el CP. El MS a esta escala ni se estimó.
4. **`phase_jitter` no se barrió sobre el real.** Sigue en su default de 0,1 sin justificación medida.
5. **El JSON de salida no existe** hasta que la corrida cierre, así que no hay artefacto reproducible todavía: solo el log.
6. **No se sabe si la corrida va a sobrevivir 8 horas** en ese container. Si se corta, este parcial es lo único que queda, y por eso está commiteado.