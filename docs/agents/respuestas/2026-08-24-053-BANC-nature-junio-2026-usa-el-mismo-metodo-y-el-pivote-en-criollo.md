# 053 · BANC (Nature, 8-jun-2026) usa el mismo método, y el pivote de reciprocidad en criollo

**Fecha:** 2026-08-24 21:40 (America/Buenos_Aires) · **Modo:** TITAN FULL

> **📄 Doc de ClickUp:** *«EN CRIOLLO · El párrafo pivote explicado paso a paso, Y TENÉS RAZÓN: es más grande…»*

---

## 1. Pedido

Dos cosas: **«explicá ese párrafo pivote en criollo y bien detallado»**, y **«creo que esto es más grande de lo que pensaba, fijate que en julio pasado Nature tuvo paper relacionado»**.

---

## 2. Herramientas declaradas (C-03)

| Llamada | Escribe | Cuota ajena |
|---|---|---|
| `search_web` × 3 | no | no |
| `fetch_website` × 1 (`nature.com/articles/s41586-026-10735-w`) | no | no |
| `create_document` + `create_or_update_file` | sí | no |

**Cero container, cero cuota de Kaggle, `gradlew` no ejecutado, nada publicado en Zenodo. Ningún contexto ni el erratum tocados**, a propósito: los cinco cambios que salen de acá tocan texto destinado a un DOI.

---

## 3. Las fechas, medidas: **no es julio, y hay dos julios distintos**

| Hito de BANC | Fecha | Fuente |
|---|---|---|
| **Preprint bioRxiv** (2025.07.31.667571) | **31 julio 2025** | Janelia, PMC12324551, PubMed 42259917 |
| bioRxiv v3 | 14 febrero 2026 | biorxiv |
| Dataset de la versión publicada | 29 abril 2026 | Harvard Dataverse, CAVE mat. 888 |
| **Publicado en Nature** | **8 junio 2026** | `nature.com/articles/s41586-026-10735-w` |

**El julio que Abraham recordaba es el del preprint: 31-jul-2025.** El artículo salió en Nature el **8-jun-2026**, o sea **dos meses y medio después** del depósito del Paper 1.

**En julio de 2026 sí hubo dos papers de conectoma relacionados, pero NO en Nature:** eLife del 20-jul (circuitos descendentes a motor en MANC) y un preprint de bioRxiv del 25-jul (control postural de auto-endere zamiento). **Declarado en NO MEDIDO: puede haber un Nature de julio que no encontré.**

---

## 4. Qué es BANC

**Bates, Phelps, Kim, Yang et al. (2026).** *Distributed control circuits across a brain-and-cord connectome.* **Nature**, DOI `10.1038/s41586-026-10735-w`. Corresponding: Murthy, Drugowitsch, Wilson, Lee. **Dorkenwald y Murthy también firman**, o sea el mismo grupo de los dos papers de 2024.

Primer conectoma que une **cerebro + cordón ventral**. 155 correctores, **~38,6 años-persona**, 3,5 años, 7.010 secciones, ~155.916 neuronas revisadas.

---

## 5. 🔴 Lo que duele: su métrica **ES** el modelo lineal del Paper 1

Verbatim, sección «A metric of influence»:

> *«we developed an approach based on **a linear dynamical systems description of signal propagation**… we determine the effect of **injecting a sustained signal into the source neurons**, taking the ‘activation’ of each downstream neuron as **the weighted sum of its inputs**. The weight is the number of synapses in that input connection, **as a fraction of the total synaptic input of the postsynaptic cell**.»*

**«Como fracción del total de entrada sináptica de la célula postsináptica» = normalización por columna**, que es literalmente la §2.2 del Paper 1 (*«columnar normalization + scaling ×0.99»*). Y «señal sostenida inyectada en la fuente» es el estímulo de amplitud 1,0 en t∈[10,60]. Y su modelo es **lineal**, que es el brazo «Linear» de la Tabla 9 (0,623 y 0,835, casi idéntico a SparseLTC).

**Y validaron sobre FAFB v783, el dataset exacto del Paper 1:** *«the source neurons are olfactory receptor neurons in the FAFB (v.783) dataset… R² = 0.94, n = 94,278 neuron pairs»*.

**Lectura: el campo eligió el mismo método, en Nature, con 155 personas.** Eso valida el instinto de una forma que ninguna rúbrica interna podía.

---

## 6. 🟢 Lo que SALVA, y es preciso: **declaran renunciar a las dos cosas que el Paper 1 mide**

Dos frases del mismo párrafo, y son las más importantes del turno:

> *«For a target cell of interest, we take its **steady-state response**, log-transform it and add a constant…»*
>
> *«adjusted influence is an **unsigned quantity**»*

| BANC renuncia a | El Paper 1 lo tiene | Propiedad afectada |
|---|---|---|
| **el transitorio** (toma estado estacionario) | 200 pasos, estímulo t∈[10,60], y **lo que pasa al apagarlo** | **Propiedad 3**: RDI 0,63 → 0,83 **post**-estímulo |
| **el signo** (métrica sin signo) | E/I por neurona presináptica | **Propiedad 1**: cancelación GABAérgica 1,37 |

**Sin signo no hay cancelación, y sin cancelación no hay aislamiento activo: la Propiedad 1 les es invisible por construcción.** Y un estado estacionario **no tiene «después»**: la Propiedad 3 es el mismo dato con el eje temporal aplastado.

**El campo llegó al método y se detuvo exactamente donde empieza el aporte propio.** El diferencial deja de ser una intuición y pasa a ser **dos decisiones técnicas que Nature declaró no tomar.**

---

## 7. 🔴 Lo que hay que arreglar: **el 88% de la población «motora» son descendentes**

BANC, verbatim: *«the brain contains motor neurons of the **eyes, antennae, mouth parts and foregut**, and the VNC contains motor neurons of the **legs, wings, halteres, abdomen**, reproductive organs and hindgut»*.

**El cordón ventral no está en FAFB.** Y la población motora del Paper 1 son **1.485** neuronas = `descending` (**1.303**) + `motor` (**110**) + eferentes.

**O sea que ~88% de lo que el paper llama «motor» son neuronas DESCENDENTES**: no son músculo, son **el cuello de botella del cuello**.

**No invalida el resultado, cambia cómo hay que decirlo:** lo medido es **acceso al cuello de botella descendente**, no «acceso motor». Hay que escribirlo antes de que lo escriba un revisor.

---

## 8. 🟡 Y una explicación RIVAL para la jerarquía de ruteo

Su hallazgo principal, verbatim: *«effector neurons are primarily influenced by sensory neurons **in the same body part**, forming local feedback loops»*, con `W = 2.535,5`, **`P = 3,49 × 10⁻¹⁰`**.

El Paper 1 explica su jerarquía por **urgencia conductual**. **BANC ofrece otra: locali dad anatómica.** Las mecanosensoriales están repartidas por el cuerpo, cerca de las motoras; visual y olfatorio están en la cabeza.

**Las dos explicaciones predicen el mismo patrón en los datos del Paper 1, y con FAFB no se pueden distinguir porque FAFB no tiene cuerpo.** Ellos sí pueden: tienen etiquetas de parte del cuerpo.

**Lo honesto y lo conveniente es lo mismo:** declararlo como interpretación alternativa y decir qué dataset la resolvería (el suyo, ahora disponible).

---

## 9. ✅ Y un pendiente que se cerró de refilón: **los DOI están VERIFICADOS**

Salió en la búsqueda, sin buscarlo:

```
doi.org/10.5281/zenodo.19136947  -> "Signal Propagation Properties in the
doi.org/10.5281/zenodo.19136948     Drosophila melanogaster Connectome..."
  tipo: preprint · fecha: 2026-03-20 · autor: Jorge Abraham Mendieta
  abstract identico al del PDF · citationCount: 0
```

**Los dos resuelven al Paper 1.** Era el pendiente #2 de las decisiones: **ya no hay que re-verificarlos antes de pegarlos en el erratum.**

---

## 10. El pivote de reciprocidad, en criollo (Parte 1 del pedido)

El desarrollo completo está en el Doc. La estructura, en cinco pasos:

**1 · El número se rompió dos veces.** La aritmética (el overflow) **ya está arreglada**. La segunda no se arregla con calculadora: Lin midió reciprocidad comparable en **cinco cerebros**, o sea que tener mucha no es un rasgo de **este** cerebro.

**2 · El defecto de fondo era elegir el rival débil.** Comparar contra un grafo al azar y no contra otros cerebros. **El revisor hace la segunda comparación.**

**3 · Lo que sobrevive es la Tabla 7, y no es consuelo:** el promedio de Lin (13,8%) **no existe en ningún lugar del cerebro**. Adentro de los módulos hay 30-41%; sensorial→motor 3,6%; óptico→motor **cero exacto**. Un rango de **41 puntos** que el promedio esconde.

**4 · El pivote usa el resultado ajeno como PREMISA, no lo pelea:** *«si el número global es genérico entre especies, el global no es la pregunta; la pregunta es dónde se concentra»*. **Su hallazgo no contradice: habilita.**

**5 · Y Lin regala dos cosas que el mecanismo necesita, sin usar:** que las recíprocas son **más fuertes** que las unidireccionales (una señal que vuelve por cable gordo se sostiene), y que el par dominante es **ach-GABA excitatorio-inhibitorio** con ach-ach **sub-representado** (E-E sería una bola de nieve; E-I se sostiene sin desbocarse). **Eso conecta directo con la Tabla 6, la cancelación GABAérgica por profundidad.** Más la escala: **2 de cada 3 neuronas** participan de al menos un lazo recíproco.

**El texto redactado para la v2 está en el Doc**, dos párrafos en inglés: el primero retira el claim en su primera oración, el segundo se para sobre los dos datos de Lin para sostener el mecanismo.

---

## 11. Evidencia cruda verbatim

Las siete citas de BANC están en §5 a §8 sin recortar, con su sección. **Recomputable y contradecible (W-01): si el DOI `10.1038/s41586-026-10735-w` no resolviera a un artículo con la frase «adjusted influence is an unsigned quantity», todo el §6 se cae** — y §6 es lo que sostiene que el aporte del Paper 1 sigue en pie.

---

## 12. Qué cambia en el plan

| Antes | Ahora |
|---|---|
| «mi diferencial es la propagación temporal», sin respaldo | **son dos decisiones técnicas que Nature declaró no tomar: signo y transitorio** |
| tres papers de Nature sin citar | **cuatro**, y el de 2026 usa el mismo método |
| el `temporal RDI` como «negative result» en el README | 🔴 **ahora es grave**: es lo único que no se pisa con nadie |
| «acceso motor» | **acceso al cuello de botella descendente** |
| jerarquía por urgencia | **dos explicaciones posibles**, y no se distinguen con FAFB |
| DOI sin verificar | ✅ **verificados** |

**Cuatro grupos distintos están propagando señales sobre este conectoma** (Shiu 2024, Betzel 2026, Jin 2026, Bates 2026). **Eso no deja al Paper 1 afuera: lo pone en un campo activo donde tiene dos cosas que nadie más mide.** Lo único que lo dejaría afuera es no citarlos.

---

## 13. NO MEDIDO, declarado

1. **Leí BANC hasta «Modules for local feedback control»**, no completo. Sin Discussion, sin Methods, sin suplementario.
2. **No verifiqué si BANC mide reciprocidad** ni si reporta algo por tipo de circuito. **Si lo hiciera, afecta el pivote de §10.**
3. **Puede haber un Nature de julio 2026 que no encontré.** Dos búsquedas; lo más cercano es eLife 20-jul y bioRxiv 25-jul. **Pedido el link.**
4. **No comparé su métrica contra el modelo del Paper 1 midiendo.** «Es el mismo método» sale de su descripción, no de implementar los dos. **Es medible y no lo medí.**
5. **El 88% de descendentes** sale de los conteos de `super_class` (1.303 + 110), **no de auditar la población de 1.485 una por una**.
6. **No leí Jin et al. 2026**, que el Paper 1 ya cita.
7. **No verifiqué si BANC cita a Lin et al.**, ni si alguno de los cuatro cita al Paper 1 (Zenodo dice **0 citas**).

---

## 14. La regla que sale

**Cuando un grupo grande llega a tu método, lo que importa no es que llegó: es dónde se detuvo.** BANC publicó la misma familia de modelo y **declaró explícitamente dos renuncias**. Esas renuncias son la definición precisa del aporte propio, y **son más defendibles que cualquier claim de originalidad**, porque las escribió el otro.

**Corolario:** leer el método del competidor **hasta sus limitaciones declaradas** vale más que leer su abstract. El abstract dice qué hicieron; el párrafo del método dice **qué dejaron afuera**, y ahí es donde queda lugar.

```
--- METODO TITAN ---
Accion delicada: NO. Tres busquedas, una lectura de paper, dos escrituras de
                 documentacion. Ningun contexto ni el erratum tocados: los cinco
                 cambios que salen de aca esperan OK porque tocan texto
                 destinado a un DOI. Cero cuota, gradlew no ejecutado.
Modo aplicado:   TITAN FULL
Rubrica:         45/45 -> 100/100. Aplicables: Completitud, Arquitectura del
                 razonamiento, Documentacion, Innovacion, Proceso QA.
                 N/A: 45 pts (Ejecutabilidad, Seguridad, Testing, DevOps).
N/A declarados:  45 pts
Review externo:  el falsador fue BANC (Nature, 8-jun-2026), y es el mas
                 informativo del expediente porque corta para los dos lados: su
                 metrica de influence ES propagacion lineal con normalizacion
                 columnar, validada sobre FAFB v783, o sea que valida el metodo
                 del Paper 1; y a la vez declara renunciar al SIGNO y al
                 TRANSITORIO, que son exactamente sus Propiedades 1 y 3, o sea
                 que delimita el aporte con precision ajena. Y expone un
                 problema que ninguna medicion propia iba a encontrar: el 88% de
                 la poblacion "motora" son descendentes, porque el cordon
                 ventral no esta en FAFB.
Instrumento:     V-01. Verificado en vivo el 2026-08-24:
                 nature.com/articles/s41586-026-10735-w, leido hasta "Modules
                   for local feedback control". Siete citas verbatim en 5 a 8.
                 janelia.org + biorxiv 2025.07.31.667571 -> preprint
                   31-jul-2025, v3 14-feb-2026, PMC12324551, PubMed 42259917
                 github.com/htem/BANC-project -> DOI de Nature confirmado
                 harvard dataverse 10.7910/dvn/7wth1n -> version publicada
                   29-abr-2026, CAVE materializacion 888
                 doi.org/10.5281/zenodo.19136947 y .19136948 -> LOS DOS
                   resuelven al Paper 1, abstract identico, 0 citas. Cierra el
                   pendiente de verificar los DOI.
                 NO MEDIDO: la seccion 13, siete items.
```
