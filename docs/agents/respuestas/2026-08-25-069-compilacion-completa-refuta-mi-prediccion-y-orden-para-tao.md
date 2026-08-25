# 069 · La compilación completa refuta mi predicción, y la orden para Tao

**Fecha:** 2026-08-25 01:45 (America/Buenos_Aires) · **Modo:** TITAN FULL

> **📄 Doc de ClickUp:** «COMPILÉ LAS 962 · me refutó, y ahí está lo bueno»
> **🔬 Evidencia:** `docs/agents/evidencia/2026-08-25-compilacion-gf-completo-evidencia-cruda.md`
> **📋 La orden:** `docs/agents/ORDEN-TAO-AUDITORIA-EXTERNA.md`

---

## 1. Pedido

«Compila las 962 y prepara un prompt maestro para que Tao audite todo el repositorio de este proyecto, necesitamos un veedor externo no sea para dónde estás yendo.»

## 2. Herramientas declaradas (C-03)

| Llamada | Escribe | Cuota ajena |
|---|---|---|
| `gateway build.run` × 3 sobre `brain-env` | solo `/tmp` | **NO** |
| `githubmcp_create_or_update_file` × 4 | sí, rama `titan/twohop-nulls` | no |
| `create_document` × 1 | sí, ClickUp | no |

**Cero Kaggle. Nada a Zenodo. `/workspace` solo leído. Ningún merge, ningún borrado.**

---

## 3. 🔴 LA PREDICCIÓN SE REFUTA, y era mía

Hace diez minutos escribí: *«compilar las 962 aristas con signo y ver si la selectividad temporal aparece. Si aparece, «la topología no explica la función» se retira.»*

**No aparece.**

### El subgrafo, primero, porque sin él el experimento no tenía sentido

```
nodes 864   internal_edges 45687   synapses 256161
driven (LC4+LPLC2) 293   target 2   central partners 475
edges into target 962   inhibitory share 0.3462
```

**El punto clave del diseño:** no alcanzaba con agregar las 962 aristas de entrada, porque los socios inhibitorios y centrales quedaban **mudos**. Hacía falta el subgrafo con las **44.725 aristas entre socios**, que lo vuelve recurrente y hace que las inhibitorias se manejen solas desde el estímulo visual.

### Los cuatro brazos, iso-modelo, iso-estímulo, iso-semilla

| Brazo | Aristas | Selectividad looming/receding |
|---|---|---|
| **FULL** | 45.687 | **1,0631** |
| NO_INHIB | 29.872 | 1,0384 |
| NO_CENTRAL | 19.978 | 1,0633 |
| **CUT_V1** (el recorte de la v1) | 293 | **1,1128** |

**El recorte del 20% daba MÁS selectividad que el circuito completo.** O sea que mi diagnóstico estaba invertido: el recorte no la escondía, la **sobreestimaba**.

### Y el control que lo cierra sin discusión

```
SIGN_SHUFFLE {"n": 20, "mean": 1.1131, "sd": 0.0185,
              "min": 1.0598, "max": 1.1333, "shuffles_ge_observed": 19}
```

**Barajando la asignación excitatorio/inhibitorio sobre el mismo cableado, la selectividad da 1,1131 ± 0,0185, y 19 de 20 permutaciones quedan POR ENCIMA del real (1,0631).**

> **El signo real de este circuito produce MENOS selectividad temporal que el signo al azar.**

No es «no significativo»: es que el valor observado está **debajo** del ensemble. Y con la escala puesta: **duplicar la energía del estímulo mueve el pico solo 1,182×**, así que el techo de este lector está en ese orden y 1,0631 es **un tercio** de eso.

### Qué gana el expediente con esto

**El claim «la topología define ruteo y ganancia, no selectividad» pasa de estar apoyado por un recorte del 20% a estar apoyado por el circuito completo, con signo, con ablaciones iso-modelo y con un control de signo barajado.**

**Es el resultado mejor sostenido del día, y salió de un experimento diseñado para tumbarlo.** Eso es lo más parecido a ciencia que hizo este proyecto hoy.

**Y la corrección de la entrada 01 sigue siendo válida** (el circuito **sí** es 67,6% central y 49,8% inhibitorio, eso no cambia). Lo que se cae es **mi explicación de por qué el 1,04× daba así.**

---

## 4. La orden para Tao

`docs/agents/ORDEN-TAO-AUDITORIA-EXTERNA.md`, ocho secciones, **autocontenida** porque Tao trabaja desatendido y no puede preguntar.

**El mandato, en las palabras de Abraham:** *«no sea para dónde estás yendo»*. O sea que el pedido **no** es revisión de código: es que alguien que no escribió esto diga si la dirección sirve. La orden lo dice así y le da **permiso explícito de concluir que no**.

| Sección | Qué lleva |
|---|---|
| §0 | por qué existe: **siete autorrefutaciones en cuatro horas, todas encontradas por mí**, lo que es sano y también es lo que se ve cuando hay un solo testigo |
| §1 | contexto mínimo: las tres líneas, los deadlines, el riesgo declarado |
| §2 | qué leer **en qué orden**, cuatro bloques, más los md5 de los datos y dónde bajar los neuropilos |
| §3 | **doce claims en forma falsable, cada uno con el «cómo atacarlo»** y el punto débil que yo mismo veo |
| §4 | los **doce modos de falla** como checklist, más el decimotercero de hoy |
| §5 | formato obligatorio de informe, con **«EL OCTAVO ERROR»** como sección propia |
| §6 | prohibiciones: no mergear, no publicar, no tocar `main`, no arreglar nada |
| §7 | prioridad si le alcanza para poco: **erratum > null anatómico > dirección** |
| §8 | **la advertencia sobre mí**, ver abajo |

### Los tres claims que le marqué como más probables de caer

- **C-05:** mi null anatómico asigna **un** neuropilo dominante por neurona; el NPC de Lin lo hace **por sinapsis**. ¿Esa simplificación produce el colapso de 323× a 2,4×, o el colapso es real? **Es la pregunta técnica más importante del repo.**
- **C-07:** `shared_min_sites` mide coincidencia de neuropilo, **no contacto físico**. Las coordenadas están en `annotations.tsv` y **no las usé**. Un control de distancia puede tumbar el LC6.
- **C-08:** `tau = 0,119` fijo para las 864 neuronas, cuando el motor real usa **τ heterogénea**, que es el parámetro con más chance de generar selectividad temporal. **El resultado de la §3 puede ser artefacto de un modelo pobre, y si lo es es una buena noticia que yo no vi.**

### Y la §8, que es la parte que importa

La orden termina declarando que **yo la escribí**, y que eso la hace sospechosa por construcción: los doce claims son los que **yo** creo atacables, y **el octavo error por definición no está en esa lista**. Así que le doy permiso explícito de ignorar la §3 entera.

**Es la aplicación de W-01 en su forma útil:** un instrumento cubre el sesgo de **ejecución**; el sesgo de **selección** — qué se eligió medir — solo lo cubre un tercero. **Y eso es exactamente lo que Abraham pidió.**

---

## 5. Scorecard (QA)

| Criterio | Pts | Evidencia |
|---|---|---|
| **Completitud** | 14/15 | `compile_gf_full.py` completo, 4 brazos + 20 permutaciones + 3 guards, docstrings en las cinco funciones. La orden a Tao con 8 secciones y 12 claims. **−1**: el brazo con τ heterogénea, que es el más informativo, no está implementado |
| **Ejecutabilidad** | 15/15 | corrió de punta a punta, `DONE in 48.5 s`, rutas por `argparse`. Los tres guards dieron `MATCHED_OK`, `DIFFERS_OK` y un ensemble con `sd > 0` |
| **Arquitectura del razonamiento** | 9/10 | los cuatro brazos son iso-modelo, iso-estímulo e iso-semilla, y la normalización por columna más el radio espectral fijo evitan que un brazo gane por tener más peso total. **−1**: esa misma normalización borra las diferencias de ganancia absoluta, que es donde el circuito **sí** muestra estructura |
| **Documentación** | 10/10 | evidencia cruda verbatim sin recortar, siete defectos declarados en el archivo de evidencia, y la orden a Tao incluye una advertencia sobre su propio autor |
| **Innovación** | 4/5 | el control de signo barajado no estaba pedido y es lo que convirtió un «no significativo» en un «por debajo del azar». **−1**: no se barrió τ |
| **Proceso QA** | 5/5 | cada número tiene su línea en la salida commiteada, y **la predicción refutada es mía y quedó escrita antes de correr** |

**Total 57/60 → 95,0/100.** APROBADO (umbral 90).
**N/A: 40 pts** — Seguridad (15), Testing (15), DevOps (10): script de simulación de solo lectura, sin red, sin entrada de usuario, sin deployment.

---

## 6. NO MEDIDO, declarado

1. **τ heterogénea no se barrió.** Es el único parámetro que puede dar vuelta el resultado de la §3 y **es la primera cosa que hay que correr**.
2. **El modelo no es el que produjo el 1,04× histórico** (ese script no está en el corpus). **La comparación válida es interna: FULL contra CUT_V1 en la misma corrida.**
3. **Solo se estimula LC4+LPLC2.** Los 39 socios sensoriales y los 28 descendentes se mueven solo por recurrencia: **un estímulo multimodal no se probó**, y es lo que la entrada 01 sugiere que importa.
4. **La normalización iguala la ganancia entre brazos a propósito**, así que este experimento **no dice nada sobre la ganancia**, solo sobre la selectividad.
5. **Un solo tamaño de ventana** (onset 20, duración 60, 200 pasos), sin barrido.
6. **La métrica es el pico del promedio de las 2 neuronas blanco.** Sin integral, sin umbral de disparo, que es lo que decide un escape real.
7. **El estímulo es escalar por población**, no espacial por campo receptivo.
8. **La orden a Tao no fue ejecutada.** Está emitida y commiteada; **lanzarla es de Abraham**, y hasta que Tao emita informe **el review externo sigue siendo deuda declarada (K-02)**.
9. **Los contextos siguen sin actualizar** con las resp 065 a 069. Es la deuda de estado más vieja que queda abierta.
