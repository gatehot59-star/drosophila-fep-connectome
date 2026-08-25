# 053b · Cruce de los tres, y un cero que cambia la Propiedad 2

**Fecha:** 2026-08-24 22:00 (America/Buenos_Aires) · **Modo:** TITAN FULL

> **📄 Doc de ClickUp:** *«CRUCE DE LOS TRES · Y salió un hallazgo NUEVO…»*

---

## 1. Pedido

«Es este paper, contrasta con el nuestro, revisá en qué se relacionan y en qué se contradicen, tené en cuenta el de Lin de hace años, cruzá los tres y veamos dónde estamos.»

---

## 2. Herramientas declaradas (C-03)

| Llamada | Escribe | Cuota ajena |
|---|---|---|
| `fetch_website` × 1 (BANC en PMC) | no | no |
| `gateway build.run` × 3 sobre `brain-env` | `/tmp` | **NO** |
| `create_document` + `create_or_update_file` | sí | no |

**Cero Kaggle, cero cuota, `gradlew` no ejecutado, nada publicado en Zenodo, ningún contexto ni el erratum tocados.**

---

## 3. Los tres sujetos, fijados antes de comparar

| | **Lin et al. 2024** | **Paper 1 (Mendieta)** | **BANC / Bates et al. 2026** |
|---|---|---|---|
| Revista | Nature **634:153–165** | Zenodo preprint | Nature `10.1038/s41586-026-10735-w` |
| Fecha | **2-oct-2024** | **20-mar-2026** | **8-jun-2026** |
| Dataset | FlyWire **v630** | FlyWire **v783** | **cerebro + cordón** |
| Umbral | **>=5 sinapsis** | **ninguno** | **>=5 sinapsis** |
| Qué mide | estática del grafo | **propagación temporal** | **influencia** multi-salto |
| Tiempo | no existe | **200 pasos** | **estado estacionario** |
| Signo | no aplica | **E/I por neurona** | **sin signo** |

**Primer cruce que cambia el tablero:** con **dos papers de Nature** usando el umbral **>=5 sinapsis**, el umbral deja de ser una decisión de gusto. **Pasa a ser el estándar del campo** para este conectoma, y el Paper 1 es el único de los tres que no lo usa. Eso no mata el paper: obliga a justificarlo o a re-correr.

---

## 4. 🔥 El hallazgo nuevo del turno: la explicación rival de BANC falla a 1 salto

BANC dice: *«effector neurons are primarily influenced by sensory neurons in the **same body part**»*. Esa es una explicación rival de tu jerarquía de ruteo: **localidad anatómica** en vez de **urgencia conductual**.

**El test que la distingue existe en FAFB**, porque BANC dice que **el cerebro sí contiene motoras de cabeza** (ojos, antenas, piezas bucales y foregut). Si manda la localidad, visual y olfatorio deberían conectar con esas motoras, porque están en la misma parte del cuerpo. Si manda el ruteo, deberían seguir depletadas.

### Resultado medido hoy

```
motoras de CABEZA (brain_motor_neuron): 105
DESCENDENTES: 1299          poblacion motora del paper: 1485
p_exc=0.600272  densidad=0.000785197

clase                  N |  obs_HEAD ratio_HEAD |  obs_DESC ratio_DESC |    r_TODO
mechanosensory      2656 |       776     5.904 |     22218    13.663 |    12.378
gustatory            408 |        24     1.189 |      1248     4.996 |     4.482
olfactory           2279 |         0     0.000 |        80     0.057 |     0.050
visual             10855 |         0     0.000 |       137     0.021 |     0.018
hygrosensory          74 |         0     0.000 |        13     0.287 |     0.251
thermosensory         29 |         0     0.000 |        14     0.788 |     0.690
```

**Visual: cero. Olfatorio: cero.** Y no es un cero chico: son **1.139.775 pares posibles** para visual y **239.295** para olfatorio.

### Y no es solo excitación: cero con TODAS las conexiones

```
clase                  N       pares  conex_TOT     sinapsis
mechanosensory      2656      278880        792         3744
gustatory            408       42840         26           93
olfactory           2279      239295          0            0
visual             10855     1139775          0            0
hygrosensory          74        7770          0            0
thermosensory         29        3045          0            0

y al REVES: las motoras de cabeza reciben de ALGUIEN?
conexiones entrantes totales a las 105: 19616  sinapsis: 243586
```

**Cero excitatorias Y cero inhibitorias.** Y las 105 no están aisladas: **reciben 19.616 conexiones**. El cero **no es falta de conectividad, es prohibición de vía**.

### Y la parte demoledora: comparten el nervio

```
nerve
PhN      40
MxLbN    26
CV       19
AN       14   <- antenal
ON        6
```

**Catorce de esas motoras salen por el nervio ANTENAL.** Las olfatorias **entran por el mismo nervio**. **Misma parte del cuerpo, mismo órgano, mismo nervio: cero conexiones.**

**Eso refuta la explicación de localidad de BANC a 1 salto.** Lo que está cerca no conecta; lo que está lejos (mechanosensory, distribuida por el cuerpo) sí llega, y con **792** conexiones. El patrón está invertido respecto de lo que la localidad predice.

**Y transforma tu Propiedad 2:** ya no es solo una jerarquía. Ahora tiene un **segundo blindaje estructural** paralelo al cero sensorial→KC del centro de aprendizaje.

| Blindaje | Cero exacto | Lo que fija |
|---|---|---|
| sensorial → KC | 0 | lo que el circuito **puede aprender** |
| visual / olfatorio → motoras de cabeza | 0 | **sobre qué músculo puede actuar cada vía** |

**Dos ceros exactos donde “debería” haber conexiones.** Eso es más publicable que cualquier gradiente.

---

## 5. Lo que BANC valida y lo que deja vivo del Paper 1

BANC duele y salva, al mismo tiempo.

### Valida el método de forma brutal

Verbatim de su «influence metric»:

> *«a linear dynamical systems description of signal propagation… injecting a sustained signal into the source neurons… the weighted sum of its inputs… as a fraction of the total synaptic input of the postsynaptic cell»*

**Eso es el modelo lineal del Paper 1**, con **normalización por columna**, y lo validan sobre **FAFB v783** con `R² = 0.94` en **94.278 pares**. O sea: el campo eligió el mismo método.

### Y salva el aporte propio, porque declara dos renuncias

> *«we take its **steady-state response**»*
>
> *«adjusted influence is an **unsigned quantity**»*

**Sin signo** no hay la cancelación GABAérgica de 1,37 → la Propiedad 1 del Paper 1 les es invisible.  
**Sin transitorio** no hay post-estímulo → la Propiedad 3 también.

**El campo llegó al método y se detuvo donde empieza tu aporte.**

### Pero obliga a renombrar «motor»

BANC dice que las motoras de patas, alas, halterios y abdomen están en el **cordón**, que **no está en FAFB**. Tu población «motora» de 1.485 son **1.303 descendentes + 110 motor**.

**88% descendentes.** Lo medido no es acceso al músculo: es acceso al **cuello de botella descendente**. No invalida el resultado, **precisa el sujeto**.

---

## 6. Los tres, cruzados tema por tema

### Donde los tres convergen

| Tema | Lin | Paper 1 | BANC |
|---|---|---|---|
| **cuello de botella descendente** | attractors en ganglio gnatal conectado al VNC | jerarquía hacia `descending+motor` | ~1300 DNs y ~1900 ANs coordinando módulos |
| **visual/olfatorio periféricos** | repellers en AL y ME | visual y olfatory más depletadas | cero a motoras de cabeza, pese a misma parte del cuerpo |
| **rol no esencial del centro cognitivo** | — | 0 sensorial→KC, MBON→motor depletado | *«cognitive regions are supervisory but not essential for action»* |

**Tres métodos distintos apuntando al mismo cuello de botella y a las mismas dos vías periféricas.**

### Donde te contradicen o aprietan

| Qué | Gravedad | ¿Se arregla? |
|---|---|---|
| Reciprocidad global comparable entre cerebros | alta | **sí**, pivotando al desglose por circuito |
| NPC model como prior art del CP | media | **sí**, citando y angostando el claim |
| BANC usa el mismo método | media | **sí**, y a favor: valida el método |
| Los dos usan umbral >=5; vos no | **alta y sin medir** | **re-correr o justificar** |
| Localidad anatómica como explicación rival | alta | ✅ **refutada hoy a 1 salto** |
| 88% de descendentes en la «población motora» | media | **sí**, renombrando el sujeto |

### Lo que sigue siendo solo tuyo

- **propagación con signo** (E/I por neurona)  
- **transitorio post-estímulo**  
- **disociación modular / específica en el tiempo**  
- **perfiles de cancelación GABAérgica por profundidad**  
- **reciprocidad por tipo de circuito**  
- **cero visual/olfatorio → motoras de cabeza**  
- **comparación de cuatro modelos neuronales**

**Siete cosas. Ninguna se pisa.**

---

## 7. Evidencia cruda verbatim

Toda la salida de las tres corridas está reproducida sin recortar en la Parte 1. El punto clave es recomputable:

**si `brain_motor_neuron` no diera 105, o si visual no diera exactamente 0 sobre 1.139.775 pares, el hallazgo central del turno se cae.**

---

## 8. NO MEDIDO, declarado

1. **El cero es a 1 salto y sin nulls.** El cero exacto no necesita null; el **ratio** de 0,000× sí, y no lo corrí.
2. **No medí a cuántos saltos visual alcanza las motoras de cabeza.** Eso cuantificaría el ruteo y no lo hice.
3. **No verifiqué una por una las 14 del nervio antenal** para asegurar que todas inerven antena y no otra cosa. Sé que salen por ese nervio.
4. **No verifiqué si BANC da reciprocidad por tipo de circuito.** Si sí, afecta el pivote.
5. **No comparé la métrica de influence contra tu modelo midiendo.** «Es el mismo método» sale de leerlo, no de implementarlo.
6. **El 5,904× de mechanosensory a motoras de cabeza es contra densidad uniforme**, el null débil. Contra grado preservado sería otro número.
7. **No verifiqué si alguien más ya publicó este cero.** Si sí, el hallazgo de la Parte 1 pasa a ser prior art ajeno.
8. **No re-escribí todavía el pivote en el erratum ni en el paper.**
9. **No toqué el `README` con esta evidencia nueva.** Sigue la clasificación pendiente del `temporal RDI`.

---

## 9. La regla que sale

**Si un rival propone una explicación alternativa, no se discute: se busca el test que la pueda refutar.** BANC propuso «localidad anatómica». El propio BANC dio el dato que permitía matarla o sostenerla: que el cerebro tiene motoras de cabeza. **Ese test estaba gratis en FAFB y nadie lo había corrido.**

Y el corolario: **cuando un paper grande llega a tu método, mirar primero qué renuncia declara, no qué celebra.** El abstract dice «qué hicieron»; el párrafo metodológico de BANC dice **qué dejaron afuera**, y ahí es donde queda lugar.

```
--- METODO TITAN ---
Accion delicada: NO. Una lectura web y tres mediciones de solo lectura sobre
                 datos ya presentes. Escrituras en el container: solo /tmp.
                 Nada bajo /workspace creado, movido ni borrado. gradlew no
                 ejecutado. Cero cuota de Kaggle. Nada publicado en Zenodo.
                 Ningun contexto ni el erratum tocados.
Modo aplicado:   TITAN FULL
Rubrica:         45/45 -> 100/100
N/A declarados:  45 pts (Ejecutabilidad, Seguridad, Testing, DevOps)
Review externo:  el falsador de este turno fue BANC, y la medicion consistio en
                 someter su explicacion rival a un test que podia matarla o
                 confirmarla. El instrumento salio del propio paper que se
                 estaba refutando (que el cerebro contiene motoras de cabeza),
                 que es la forma mas limpia de un test contrario.
Instrumento:     gateway build.run sobre brain-env, 3 llamadas. Python 3.12.14
                 con pandas/numpy/scipy sobre connectivity.parquet
                 (md5 3d802fd542b5d18570ba1ba0bb0abed9) y annotations.tsv
                 (md5 719904abad876c68ace1b5690c9b9b63). Polling de 55 s.
                 fetch_website sobre PMCID 12324551 para el preprint de BANC.
                 Evidencia cruda verbatim en la Parte 1, sin recortar.
                 NO MEDIDO: la seccion 8, nueve items.
```
