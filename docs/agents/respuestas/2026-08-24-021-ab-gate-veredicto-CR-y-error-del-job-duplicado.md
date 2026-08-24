# 021 · A/B gate: **CR cerrado**, veredicto duro — y un error propio que costó 30 min de tu CPU

**Fecha:** 2026-08-24 ~02:40 (America/Buenos_Aires)
**Estado:** 1 de 4 tareas CERRADA. Las otras 3 siguen corriendo. Ver §5.

## 1. Pedido

"Leelo cuando termine y dame el veredicto". Sigue de la respuesta 020.

## 2. Herramientas declaradas (C-03)

`gateway build.run` sobre `brain-env` (polling de logs + un `kill -9`, ver §4) y GitHub para este commit. Cero cuota de Kaggle.

## 3. EVIDENCIA CRUDA VERBATIM — tarea CR, completa

```
=== A/B GATE ESCALAR vs VECTORIAL ===
torch 2.13.0+cpu threads 1 seeds 6 steps 2000

### TAREA CR x*cue, cue en +-1
   calib vector hr=30 hm=5 params=1401
   calib scalar hr=12 hm=16 params=1398
   V0_vector_zeroinit               p=1401 hr=30 hm= 5 MSE=0.000043 sd=0.000022 gmean=0.487 gdisp=0.2948 549s
   Vr_vector_randinit               p=1401 hr=30 hm= 5 MSE=0.000059 sd=0.000020 gmean=0.449 gdisp=0.2869 588s
   S0_scalar_zeroinit_isoarch       p=1257 hr=30 hm= 5 MSE=0.168450 sd=0.003181 gmean=0.230 gdisp=0.0000 798s
   Sr_scalar_randinit_isoarch       p=1257 hr=30 hm= 5 MSE=0.168377 sd=0.003237 gmean=0.226 gdisp=0.0000 570s
   S0b_scalar_zeroinit_isobudget    p=1398 hr=12 hm=16 MSE=0.000360 sd=0.000118 gmean=0.970 gdisp=0.0000 570s
   Srb_scalar_randinit_isobudget    p=1398 hr=12 hm=16 MSE=0.000284 sd=0.000119 gmean=0.890 gdisp=0.0000 572s
   TEST ISO-ARCH: forma del gate           ratio=3907.043x t=-129.68 p=0.000e+00 gana=V0_vector_zeroinit
   TEST ISO-BUDGET: forma del gate         ratio=  8.339x t=  -6.45 p=1.151e-10 gana=V0_vector_zeroinit
   TEST efecto del zero-init (vector)      ratio=  1.372x t=  -1.30 p=1.950e-01 gana=V0_vector_zeroinit
   TEST efecto del zero-init (scalar)      ratio=  1.000x t=   0.04 p=9.683e-01 gana=Sr_scalar_randinit_isoarch
   TEST actual vs BICAMERALITY-like        ratio=3905.338x t=-127.39 p=0.000e+00 gana=V0_vector_zeroinit
```

Parciales de la tarea `Gated` (aún sin cerrar, **no citar como resultado**):

```
### TAREA Gated |x|*c rectificacion
   calib vector hr=26 hm=8 params=1399
   calib scalar hr=13 hm=16 params=1401
   V0_vector_zeroinit               p=1399 hr=26 hm= 8 MSE=0.000298 sd=0.000137 gmean=0.425 gdisp=0.1803 1003s
   Vr_vector_randinit               p=1399 hr=26 hm= 8 MSE=0.000185 sd=0.000082 gmean=0.403 gdisp=0.1746 1319s
   S0_scalar_zeroinit_isoarch       p=1154 hr=26 hm= 8 MSE=0.000229 sd=0.000099 gmean=0.337 gdisp=0.0000 1028s
```

## 4. VEREDICTO sobre CR

**El gate vectorial gana, y gana en la comparación honesta.** No es el presupuesto: a **1401 vs 1398 parámetros**, el vectorial da `0.000043` contra `0.000284` del mejor escalar. **8,34×, p = 1,15×10⁻¹⁰, n=6.** El cambio que hiciste de `Linear(...,1)` a `Linear(...,h_m)` está justificado por medición, no por gusto.

**Y el mecanismo se lee en dos columnas, que es lo que hace que esto no sea solo un número:**

1. **`gdisp` = 0,2948 en el vectorial.** Es el desvío del gate **entre las 8/5 dimensiones**. No colapsó a un escalar disfrazado: usa su libertad. Si hubiera dado ~0, el gate vectorial sería decorativo y el resultado sería otro.
2. **`gmean` = 0,970 y 0,890 en los escalares iso-budget.** El gate escalar **se satura abierto**: al no poder elegir *qué* dimensión pasa, su óptimo es dejar pasar **todo**, o sea dejar de gatear. Un gate que aprende a no gatear es una identidad con parámetros.

**El 3907× de ISO-ARCH hay que leerlo con cuidado y NO es el titular.** Con `hm=5` el escalar no aprende la tarea (MSE 0,168 ≈ varianza del target): no es "pierde", es "no funciona". Pero ahí tenía 1257 parámetros contra 1401, así que la comparación limpia es la de presupuesto igual: **8,34×**. El titular honesto es ese.

**El zero-init NO es el que gana.** Vectorial: 1,372× a favor pero **p = 0,195, no significativo**. Escalar: ratio 1,000, `p = 0,968`. O sea: la ganancia es de la **forma** del gate, no de cómo se inicializa. Yo había escrito en la 019 que el zero-init era "el punto no obvio": **medido, no lo es.** Se retira.

**Y el smoke me había engañado, tal como advertí en la 020.** El smoke daba el escalar iso-budget ganando 1,50× en `Gated`; con 2000 steps y n=6, en `CR` el vectorial gana 8,34×. Por eso quedó escrito antes: un smoke de 60 steps mide quién arranca más rápido, no quién converge mejor.

**Señal de alerta que ya se ve en `Gated` y hay que esperar:** ahi el escalar iso-arch (0,000229, **con 245 parámetros menos**) le gana al vectorial zero-init (0,000298). Si eso se sostiene al cerrar, **el resultado es dependiente de la tarea** y el claim correcto no es "el gate vectorial es mejor" sino "es mejor donde hay que invertir fase". No lo afirmo todavía: faltan 3 brazos de `Gated`.

## 5. ERROR PROPIO — lancé dos veces el mismo job (W-01 / patrón 2)

El primer lanzamiento falló a medias: `cd X && ... &` backgroundea la cadena entera, así que el proceso `TAG=A` **sí arrancó** con ruta relativa y el `TAG=B` murió. Leí el error de B, asumí que los dos habían fallado y relancé los dos. Resultado: **dos procesos `TAG=A` idénticos escribiendo el MISMO `ab_gate_A.json` y el MISMO `runA.log`**, y tres procesos sobre 2 núcleos (`loadavg 6.47`).

Medido verbatim antes de tocar nada:

```
/proc/3045 -> python3 ab_gate.py            TAG=A TASKS=Gated,LinScale
/proc/3060 -> python3 /workspace/.../ab_gate.py  TAG=A TASKS=Gated,LinScale
/proc/3061 -> python3 /workspace/.../ab_gate.py  TAG=B TASKS=CR,MultiCue
```

**Corrección aplicada:** copia de resguardo a `runA_contaminado.log` / `ab_gate_A_contaminado.json`, `kill -9 3045`, y verificación de que los dos JSON siguen siendo parseables y sin líneas duplicadas (`grep -c` de líneas de brazo en runA = 1). B nunca estuvo contaminado: su tag era único.

**Lo que costó:** ~30 min de CPU tuya al triple de carga, y `Gated` corrió sus dos primeros brazos con contención (1003s y 1319s contra 549-590s de los brazos de B). **Los MSE no se afectan** (son deterministas por semilla, verificado en la 020: mismo número a 6 decimales con 1 y 4 threads), pero **los tiempos de `Gated` no son comparables con los de `CR`** y eso queda declarado.

La regla que sale: **no inferir el estado de un lanzamiento desde el mensaje de error de UNO de los procesos.** Se listan los procesos vivos. Es una llamada.

Dos correcciones de entorno, medidas:
- **Los procesos en background SÍ sobreviven entre llamadas** en este container. La nota vieja que decía lo contrario era falsa para este caso.
- **`ps` no existe.** Liveness se mide con `grep -al <patron> /proc/[0-9]*/cmdline`.
- El timeout de una llamada al gateway está **entre 45 y 75 s**: `sleep 45` pasa, `sleep 75` no.

## 6. Archivos

`/workspace/ab_gate/ab_gate.py` (md5 `11591eb654eb719ae941aa524c1f59fd`), `ab_gate_A.json`, `ab_gate_B.json`, `runA.log`, `runB.log`, `runA_contaminado.log`, `ab_gate_A_contaminado.json`. Este archivo.

## 7. TRABAJO VIVO — `resultado_leido = 0`

| Tarea | Proceso | Brazos | Estado |
|---|---|---|---|
| `CR` | B (3061) | 6/6 + 5 tests | **CERRADO, LEÍDO** |
| `MultiCue` | B (3061) | 0/6 | corriendo |
| `Gated` | A (3060) | 3/6 | corriendo |
| `LinScale` | A (3060) | 0/6 | no empezó |

ETA: `Gated` ~03:15, `MultiCue` ~03:40, `LinScale` ~04:40. Se leen con `tail -40 /workspace/ab_gate/runA.log` y `runB.log`.

## 8. NO MEDIDO, declarado

- **3 de 4 tareas sin cerrar.** El veredicto de arriba vale **para CR**. Generalizarlo a las cuatro sería exactamente el error de publicar un punto de una curva como si fuera la curva.
- **n=6 semillas**, no 10. El 8,34× con p=1,15e-10 aguanta; el 1,372× del zero-init no, y por eso se declara no significativo en vez de "pequeña mejora".
- **No midí `LiquidRealCell` vs `LiquidCell`.** Los 6 brazos usan la celda actual. Este experimento mide la **forma del gate**, no reproduce BICAMERALITY entero. Sigue siendo la diferencia no auditada.
- **No hay comparación contra GRU/LSTM/MinGRU/LTC** en esta corrida.
- **`gdisp` es una métrica mía**, definida en esta corrida. No tiene antecedente en el benchmark publicado.

```
--- METODO TITAN ---
Accion delicada: SI. kill -9 sobre un proceso propio en la PC de Abraham, con
                 copia de resguardo previa de los dos archivos afectados.
                 Ningun dato suyo tocado, nada mergeado, cero cuota de Kaggle.
Modo aplicado:   TITAN FULL
Rubrica:         se emite al cerrar las 4 tareas. Puntuar ahora seria puntuar
                 1/4 del experimento como si fuera el experimento.
N/A declarados:  pendiente
Review externo:  no pedido. El falsador de esta entrega fue el propio
                 experimento: retira mi claim del zero-init de la resp 019
                 (p=0.195 y p=0.968, no significativo) y el smoke de la 020
                 quedo desmentido por la corrida larga, como estaba previsto.
Instrumento:     build.run sobre brain-env, python3 3.12 / torch 2.13.0+cpu,
                 nproc=2, THREADS=1, 6 semillas, 2000 steps por brazo.
                 Salida cruda verbatim en la seccion 3, sin recortar.
                 Estado de los procesos leido de /proc, verbatim en seccion 5.
                 NO MEDIDO: seccion 8.
```
