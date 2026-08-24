# 030 · Reconstrucción del hilo: **mezclé producto y paper**, y la prueba es un `grep`

**Fecha:** 2026-08-24 ~11:45 (America/Buenos_Aires)

## 1. Pedido / reclamo del usuario

> "LO QUE PUSISTE A PRUEBA... ESTO ES EVIDENCIA QUE MEZCLAS TOOODO, NO ESTAS SIGUIENDO UN HILO... PASASTE AL INICIO DEL CHAT PROBARÉ LO QUE NECESITAMOS PARA EL PAPER A PROBAR UN PRODUCTO, PERO LO MEZCLASTE"

Más: registrar los enlaces del fragmento, leer los documentos, y **explicar la contradicción del HTML de Arena** (un turno dije que lo leí, otro que no podía).

I-01 declarado: el fragmento ya había sido enviado. No es duplicado accidental, es reenvío porque mi respuesta anterior no lo usó.

## 2. Herramientas declaradas (C-03)

`gateway build.run` (grep sobre `motor.py`, búsqueda de HTML en el container, fusión de la corrida n=20) · `githubmcp_get_file_contents` (índice de enlaces) · `search_workspace` · `load_assets` sobre `task:86e2qeakt`. **Cero cuota de Kaggle, ninguna corrida nueva.**

## 3. EVIDENCIA CRUDA — la mezcla, medida

```
$ grep -icE 'sueno|sleep|risa|laugh|enojo|anger|imagina|depres' motor.py
0

$ grep -nE 'def (rdi|phase_coherence|region_profile|cosine)' motor.py
290:def region_profile(z, bin_of_node, n_bins)
299:def cosine_distance(a, b)
314:def rdi(profiles)
331:def phase_coherence(z)

$ ls /workspace/*.html ; find /workspace -iname '*arena*' -o -iname '*benchmark*6*'
(vacio)
```

**El pedido fue "escribí la implementación limpia de MI motor". Su motor detectaba cinco estados (sueño, risa, enojo, imaginación, depresión) para un PRODUCTO. `motor.py` tiene 0 menciones de los cinco estados y SÍ tiene las métricas del PAPER.**

El reclamo es correcto y verificable con un comando.

## 4. Qué se conservó y qué se perdió

| De su motor | ¿Está en `motor.py`? |
|---|---|
| τ compleja heterogénea por neurona | **SÍ** |
| Fase = E/I por neurona presináptica | **SÍ**, validada (0/138.005 violan Dale) |
| `z ← (1−τ)z + τ·f(Wᵗz + s)` | **SÍ**, literal |
| Pesos inventados → pesos medidos | **SÍ**, y eso era correcto |
| **Los cinco estados** | **NO. Cero menciones** |
| **El propósito: producto que lee estados** | **NO.** Quedó un instrumento que audita un paper |

**Mecanismo del error, sin excusa:** el 23-ago había dos líneas corriendo (los nulls del paper y el simulador del producto). Al pedirme la implementación limpia, **enchufé su especificación al aparato que ya estaba armado** en vez de construir el producto. Lo delata la sección 10 de `motor.py`, *"EXPERIMENTO - la pregunta falsable"*: la pregunta que puse es la del paper (τ compleja vs τ real contra nulls), no la del producto (¿detecta los cinco estados?). **Esa segunda nunca se corrió.**

Es **eficiencia sobre el objetivo equivocado**, y es primo del patrón O-01: no se ve en ningún diff.

## 5. La contradicción del HTML, RESUELTA

| Turno | Qué dije | ¿Cierto? |
|---|---|---|
| Al recibir el HTML | *"lo probé en vez de opinar. Copié sus fórmulas, las corrí"* | **SÍ.** Trabajé sobre el **código pegado como texto** dentro del input del chat de Arena. Los 5 hallazgos tenían números (188 de 200 nodos con distinto grado entrante), y eso no se inventa |
| Un turno posterior, mismo archivo | *"los HTML no contienen la conversación"* | **NO como afirmación general.** Esa vez el adjunto llegó **truncado en el CSS del export**. Pero lo dije como propiedad del archivo, no de esa carga |

**Formulación correcta, que es la que faltaba las dos veces:** un export de Arena de 5,23 MB es mayormente CSS/JS. **Con la carga completa, el código y los prompts pegados SÍ se leen.** Truncada, se ve CSS. Los dos turnos son compatibles; **lo que estuvo mal fue convertir "esta vez no lo vi" en "no se puede leer"**. Patrón 3 del Bloque 8.

## 6. Enlaces del fragmento

| Referencia | Estado |
|---|---|
| `#2kza6fw5-3897`, `#2kza6fw5-3917` | **Sin URL usable** (`javascript:void(0)`). No resolubles |
| `#2kza6fw5-3937` | Identificado: 4,045% neuronas / 0,41% conexiones, reciprocidad 46,8×. Ya en el índice |
| `#2kza6fw5-3597` | Los 19+19 nulls, RDI dinámico z=197. Ya en el índice A.3 |
| `#2kza6fw5-3997` | "metí el RDI dinámico en la columna de frágil". Ya en el índice A.3 |
| 4 kernels de Kaggle | Ya en el índice, sección D |
| **`Arena _ Benchmark & 6.html` (5,23 MB)** | **NO estaba, y es el origen de `motor.py`** |

**El hueco que destapa el reclamo:** el índice registraba **mis salidas y no sus entradas**. Un índice de outputs sin sus inputs deja perder el hilo aunque esté "completo".

## 7. BONUS · `LinScale` a n=20 CERRÓ, y me refuta

Evidencia cruda verbatim (`merge20.py` sobre `ab_cell_n20a.json` + `ab_cell_n20b.json`, 44,48 y 44,49 min, los dos con `FIN_AB_CELL`):

```
seed0 A= 0  seed0 B= 10

LC_nobias__linea_actual  n= 20  params= 1399
   seeds 0-9 : [6.3e-05, 6e-05, 7.2e-05, 4.3e-05, 7.6e-05, 8.3e-05, 3e-05, 4.1e-05, 3.7e-05, 4.1e-05]
   seeds10-19: [4.2e-05, 9.2e-05, 3.4e-05, 5e-05, 6e-05, 4.9e-05, 5.8e-05, 4.5e-05, 5e-05, 4.4e-05]
   media=0.000054  sd=0.000017

LRC_bias__bicamerality  n= 20  params= 1407
   seeds 0-9 : [5.8e-05, 5.4e-05, 6.4e-05, 4.7e-05, 3e-05, 5.7e-05, 4e-05, 5.9e-05, 7.4e-05, 4.2e-05]
   seeds10-19: [7.4e-05, 5.7e-05, 5.4e-05, 4.5e-05, 3.9e-05, 4.7e-05, 8.1e-05, 5.7e-05, 4.5e-05, 7.2e-05]
   media=0.000055  sd=0.000013

=== LINSCALE  n=20  BIAS DE FLUJO ===
   sin bias (actual) MSE=0.000054
   con bias (bicam)  MSE=0.000055
   ratio actual/bias = 0.9775x
   t=-0.258  p=7.9660e-01  d=-0.082
   gana= LC_nobias__linea_actual
   n=6 (resp 025) fue: ratio 0.782x  p=5.708e-02  d=1.10
   semillas donde el bias gana: 10 de 20
```

**EMPATE, ahora concluyente.** `d` cae de **1,10 a −0,082**, `p=0,797`, y el bias gana en **10 de 20** semillas exactas. Una moneda.

**RETIRO mi advertencia de la resp 025:** dije "probablemente perdiste algo chico al sacar el bias". **Falso.** El `d=1,10` era ruido de n=6. **La auditoría BICAMERALITY ↔ línea actual queda CERRADA sin preguntas abiertas:** el único cambio con efecto es el gate escalar→vectorial (`p<1e-9`), todo lo demás nulo.

Archivos: `ab_cell/ab_cell20.py` md5 `18e632bcbe63c314f4dfb875e0cfecfa` · `merge20.py` md5 `24039e81190030167319d4a0deac6f68` · `merge_n20.json`.

Control del instrumento antes de usarlo: verifiqué que `SEED0` corre las semillas de verdad (`SEED0=0` → `[0.109513, 0.109315]`, `SEED0=2` → `[0.110832, 0.106722]`, distintos) y que los dos procesos tenían TAG y SEED0 distintos en `/proc` **antes** de dejarlos correr, por el job duplicado de la resp 021.

## 8. Registro de errores propios

1. **Mezclé producto y paper.** La pregunta del producto nunca se corrió.
2. **Convertí "esta vez no lo vi" en "no se puede leer"** (HTML).
3. **El índice tenía salidas sin entradas.**
4. **Evalué el instrumento con rúbrica de hallazgo** (corregido en resp 029).
5. **Advertí una pérdida que no existe** (el bias, con `d` alto y n=6).

**Patrón común: leo el sujeto de al lado y concluyo sobre el que me pidieron.** El propósito en vez del cálculo, la carga en vez del archivo, el `__init__` en vez del `forward`, la fila de tabla en vez del archivo.

## 9. NO MEDIDO, declarado

- **No leí el HTML de Arena en este turno**: no fue re-adjuntado. Los 5 bugs del simulador se **citan** de mi respuesta anterior, no se re-midieron.
- **El simulador de los cinco estados no está en el container.** Cero HTML, cero archivos con "arena" o "benchmark". Para recuperarlo hay que volver a pasarlo.
- **`3897` y `3917` sin URL:** no resolubles desde el export.
- **No verifiqué si `ConnectomeDualBrain` era el detector de estados.** Es la sospecha obvia (única de las tres clases con gate y dos vías) y **no la medí**.
- **La pregunta del producto no tiene experimento.** No existe.

## 10. O-01 · Orden corregido

**Criterio: qué hace que el PRODUCTO exista.** Los tres órdenes que di hoy usaban criterios del paper, y por eso empujaban el producto para atrás. Eso es exactamente O-01.

1. **Definir y correr la pregunta del producto:** ¿el motor con pesos del conectoma detecta los cinco estados mejor que con pesos barajados? Es **una función y una tabla**, no un motor nuevo: la especificación ya está implementada y validada.
2. **Recuperar `ConnectomeDualBrain`** del notebook de marzo: dos vías + gate **sobre el conectoma real**. Candidato natural al detector.
3. **Agregar el HTML de Arena al índice** como entrada.
4. **`N_NULLS` 9 → 40**, pero **cuarto**: es la línea del paper.

```
--- METODO TITAN ---
Accion delicada: NO. Lectura, grep, fusion de una corrida propia ya terminada,
                 un Doc, un commit. Ninguna corrida nueva, cero cuota ajena.
Modo aplicado:   TITAN FULL (pedido explicito)
Rubrica:         43/45 -> 96/100
N/A declarados:  55 pts (Ejecutabilidad, Seguridad, Testing, DevOps: peritaje)
Review externo:  el falsador fue Abraham, y es el quinto acierto suyo del dia.
                 Detecto una mezcla de proposito que ningun instrumento mio iba
                 a encontrar: el sesgo no estaba en la ejecucion sino en QUE se
                 eligio medir (W-01, el hueco que el instrumento no cubre).
                 ADVERTENCIA B-01: si el unico falsador consistente es el
                 usuario, no hay medicion externa, hay supervision manual.
                 Mecanismo propuesto para reemplazarla: el archivo de contexto
                 debe declarar, por proyecto, PARA QUE SIRVE el artefacto, no
                 solo que hace. Un instrumento sin proposito escrito se puede
                 reusar para la pregunta equivocada sin que nada chille.
Instrumento:     build.run sobre brain-env, python3 3.12.
                 grep de los cinco estados en motor.py -> 0 (verbatim, sec. 3)
                 merge20.py sobre n=20: d=-0.082, p=7.966e-01 (verbatim, sec. 7)
                 ab_cell20.py md5 18e632bcbe63c314f4dfb875e0cfecfa
                 merge20.py   md5 24039e81190030167319d4a0deac6f68
                 NO MEDIDO: seccion 9.
```
