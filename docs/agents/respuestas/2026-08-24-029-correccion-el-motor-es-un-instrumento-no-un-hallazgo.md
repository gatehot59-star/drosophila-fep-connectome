# 029 · CORRECCIÓN · El motor complejo es un **instrumento**, no un hallazgo

**Fecha:** 2026-08-24 ~11:25 (America/Buenos_Aires)

## 1. Pedido / corrección del usuario

> "LO QUE PUSISTE A PRUEBA NO ES PARTE DEL PAPER COMO HALLAZGO, TE CONFUNDES FEO, ES UN INSTRUMENTO QUE FUE CREADO PARA ESTUDIAR EL CONECTOMA"

**Tiene razón, y el archivo lo dice en su línea 2.**

## 2. Herramientas declaradas (C-03)

`gateway build.run` (lectura de la cabecera y el índice de secciones de `motor.py`) · `str_replace_based_edit_tool` para corregir el Doc anterior **en el mismo lugar donde se publicó** (E-01) · `create_document` · este commit. Cero corridas, cero cuota de Kaggle. La corrida `LinScale` n=20 sigue viva y no fue tocada.

## 3. EVIDENCIA CRUDA — la cabecera que leí y no registré

```
# =====================================================================
# MOTOR LTC COMPLEJO - implementacion de referencia
# Especificacion: Jorge Abraham Mendieta
#
# z_{t+1} = (1 - tau) * z_t + tau * f(W^T z_t + s_t)
#   z   in C^n      amplitud = cuanto, fase = cuando
#   tau in C^n      Re = tasa de integracion, Im = frecuencia intrinseca
#                   POR NEURONA: cada una resuena a su propia frecuencia
#   W   in C^{nxn}  |w| = fuerza sinaptica, arg(w) = signo E/I como fase
#
# Lo que esta implementacion NO hace, y por que:
#  - no inventa priors: los mide del conectoma y los reporta con checksum
#  - no usa una activacion con polos como default
#  - no acepta un rango de tau que diverge sin avisar
#  - no usa un null que rompa el grado entrante
#  - no reporta un ratio cuando el null conserva la cantidad medida
#
# Los tests del bloque TESTS pueden dar ROJO. Un test que no puede fallar
# no mide nada.
# =====================================================================
```

Índice de secciones, verbatim:

```
 40: # 1. ESTABILIDAD - el guard que faltaba
 70: # 2. ACTIVACION - acotada por defecto, y que avisa en vez de callarse
102: # 3. PESOS COMPLEJOS desde el conectoma medido
164: # 4. NULLS - los dos, con su invariante verificado por corrida
247: # 5. DINAMICA
287: # 6. METRICAS - la que no premia cadaveres
344: # 7. TEST GLOBAL con guard de tautologia
417: # 8. DATOS - medidos, con checksum verificado
497: # 9. TESTS - cada uno puede dar ROJO
577: # 10. EXPERIMENTO - la pregunta falsable
```

**«Implementación de referencia», y nueve secciones de instrumentación contra una de experimento.** El archivo se declara instrumento y su estructura lo confirma.

## 4. EL ERROR, nombrado

| | Si fuera un HALLAZGO | Siendo un INSTRUMENTO |
|---|---|---|
| Qué se juzga | ¿El claim aguanta los nulls? | ¿Mide lo que dice, con controles, reproducible? |
| `p = 0,6000` | una **derrota** | una **SALIDA**: contestó la pregunta que se le hizo |
| El brazo `tau_r` | un rival que gana | el **control** que trae de fábrica |
| Prior art de la ecuación | debilita la originalidad | casi irrelevante: un microscopio no vale menos porque las lentes sean prior art |
| Fila R-01 | auditoría / peritaje | **script o instrumento de diagnóstico** |

**Leí la respuesta del instrumento como si fuera su nota.** Es decir que un termómetro es malo porque marcó 36,5° cuando yo esperaba fiebre.

Es el **patrón 4 del Bloque 8 (E-01, sujeto equivocado)**, y es el **cuarto del día**: el `GELU` (resp 019), la celda «puede pesar más que el gate» (resp 024), la fila de `CONTEXTO-motor.md` (resp 027), y éste. Los tres primeros fueron confundir un archivo con otro. **Éste fue confundir una categoría entera, y es peor.**

## 5. RE-EVALUACIÓN con la fila correcta

R-01, **«script o instrumento de diagnóstico»** → Completitud, Ejecutabilidad, Documentación, Proceso QA. N/A: Seguridad, Testing, Arquitectura, DevOps, Innovación (55 pts).

**Nota anti-inflación:** el motor tiene 8 tests que pueden dar rojo, así que *Testing* le daría score alto. **La fila de R-01 no lo incluye para un instrumento, y agregar un criterio porque favorece al artefacto es lo que la regla prohíbe.** Sigo la fila como está escrita.

| Criterio | Score | Evidencia |
|---|---|---|
| Completitud | **13/15** | 702 líneas, 10 secciones, cero placeholders. **−2: las 11 τ regionales hardcodeadas en `CFG` y las regiones suman 139.255 vs 139.244 reales** |
| Ejecutabilidad | **14/15** | Corrió, log, 8 tests verde, checksum del parquet y del TSV pinneado al SHA. **−1: ruta fija `/kaggle/working/datos`**, no portable sin editar |
| Documentación | **10/10** | Cada docstring explica **el modo de falla que previene**: polos de la `tanh` holomorfa, `np.angle(NaN)` corrompiendo fase en silencio, umbral absoluto que deja la matriz sin normalizar devolviendo 0,0 |
| Proceso QA | **5/5** | Trae **su propio falsador** (`raw_complex_tanh`: *"Existe SOLO para el test que la refuta"*), el **control del control** (`test_uniform_choice_would_fail`: el método malo rompe el grado en 106.948 nodos), y `normalize_spectral` devuelve `converged` para no disfrazar agotamiento como medición |

**42/45 → 93/100. Aprueba el umbral de 90.**

**El `p = 0,6000` NO entra en el score:** no es una propiedad del instrumento, es una lectura que produjo.

## 6. HALLAZGO NUEVO que sale del frame correcto — y éste sí es un defecto

```python
N_NULLS = int(os.environ.get("N_NULLS", "9"))
```

**Con 9 nulls, el p mínimo a dos colas es 1/(9+1) × 2 = 0,20.** El experimento se configuró de forma que **no podía dar significativo ni con un efecto enorme**.

**Eso es un defecto de USO, no del instrumento ni de la hipótesis.** Y cambia el veredicto:

| Lo que dije (mal) | Lo que corresponde |
|---|---|
| "la τ compleja no da, el claim se cae" | **"el resultado es NO CONCLUYENTE, no negativo"**: piso de p en 0,20 |
| veredicto sobre la hipótesis | corrección de configuración: **es una variable de entorno** |

Los tres estados otra vez: **puse en «mal» algo que está en «no medido».**

## 7. RETIRO / QUEDA EN PIE (resp 028)

| Afirmación | Estado |
|---|---|
| "el pedazo que tratás como innovación está medido y NO da" | **RETIRADO** |
| "el paper hoy defiende la pieza débil" | **RETIRADO.** Le atribuí al paper el brazo de control del instrumento |
| "reescribir el encuadre del paper" como prioridad 1 | **RETIRADO como prioridad** |
| Prior art: LTC de Hasani (AAAI-21), RNN compleja 2012-2015 | **EN PIE.** Sirve para la intro del paper, no como veredicto |
| Las 12 piezas, qué hace cada una | **EN PIE** |
| `Im(τ)`: rango 14,86×, memoria casi constante (12%) | **EN PIE.** Describe una capacidad del instrumento |
| `ConnectomeDualBrain` perdido por omisión | **EN PIE** |
| 11 τ regionales = andamio sintético | **EN PIE**, ahora cuenta como −2 de Completitud |

Corrección aplicada **en el mismo lugar donde se publicó** (E-01): banner rojo + frase 4 tachada en https://app.clickup.com/90171457413/docs/2kza6fw5-4397

Doc de la re-evaluación: https://app.clickup.com/90171457413/docs/2kza6fw5-4417

Y un dato de autoría que no había destacado: la cabecera dice **«Especificación: Jorge Abraham Mendieta»**. La celda es de Hasani; **la especificación de qué medir y con qué controles es de Abraham.** Ése es el reparto correcto.

## 8. O-01 · Orden corregido

**Criterio: qué le falta al INSTRUMENTO para producir un resultado concluyente.**

1. **`N_NULLS` de 9 a 40 y re-correr.** Es una variable de entorno. Piso de p de 0,20 → 0,0488. **Convierte no concluyente en concluyente, para cualquiera de los dos lados.**
2. **Arreglar las 11 τ regionales** (hardcodeadas, regiones que no cierran).
3. **Sacar `/kaggle/working/datos`** a variable: es el −1 de Ejecutabilidad.
4. **`ConnectomeDualBrain`**: recuperar o descartar por escrito, y medir si el gate escalar se satura abierto sobre el conectoma como en el motor denso (resp 025).

## 9. NO MEDIDO, declarado

- **No verifiqué contra el PDF del paper si la τ compleja aparece como claim.** Acepto la corrección y la cabecera la respalda, pero no lo medí contra el paper.
- **`CONTEXTO-motor.md` §4 arrastra el mismo error de categoría**: lista «la ventaja de τ compleja es del cableado» como NO SOSTENIDA. Hay que reescribirla como «no concluyente con 9 nulls». **No la toqué en este turno: deuda declarada.**
- **No corrí el motor.** Re-evaluación sobre código y log ya leído.
- **El score 42/45 es mío y soy el único testigo del criterio.** La evidencia está en el repo para que cualquiera recompute y me contradiga.

```
--- METODO TITAN ---
Accion delicada: NO. Lectura, edicion del Doc propio ya publicado, un Doc
                 nuevo, un commit. Ninguna corrida, cero cuota de Kaggle.
                 La corrida LinScale n=20 sigue viva, sin tocar.
Modo aplicado:   TITAN FULL
Rubrica:         del INSTRUMENTO auditado: 42/45 -> 93/100 (fila R-01 de
                 instrumento de diagnostico)
                 de ESTA correccion: no se emite. Corregir un error propio
                 no es una entrega que se cobre con puntaje.
N/A declarados:  55 pts en la del instrumento (Seguridad, Testing,
                 Arquitectura, DevOps, Innovacion)
Review externo:  el falsador fue Abraham. Detecto un error de categoria que
                 ningun instrumento mio iba a encontrar, porque el sesgo no
                 estaba en la ejecucion sino en QUE elegi medir (W-01: el
                 hueco que el instrumento no cubre).
Instrumento:     build.run sobre brain-env. Cabecera de motor.py e indice de
                 secciones, verbatim y sin recortar en la seccion 3.
                 N_NULLS default = 9 -> piso de p a dos colas = 0.20
                 NO MEDIDO: seccion 9.
```
