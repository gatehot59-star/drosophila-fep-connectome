# 066 · Barrido de literatura: la tabla de ruteo YA está publicada

**Fecha:** 2026-08-25 01:20 (America/Buenos_Aires) · **Modo:** TITAN FULL

> **📄 Doc de ClickUp:** «LA TABLA YA ESTÁ PUBLICADA · y desde el mismo dataset»

---

## 1. Pedido

«Barré la literatura: ¿esta tabla ya está publicada?» Era el ítem 6 de los NO MEDIDO de la resp 065, y el que yo mismo había puesto arriba de la lista.

## 2. Herramientas declaradas (C-03)

| Llamada | Escribe | Cuota ajena |
|---|---|---|
| `search_web` × 4 | no | no |
| `fetch_website` × 2 (`elifesciences.org`, `biorxiv.org`) | no | no |
| `githubmcp_create_or_update_file` × 2 | sí, rama `titan/twohop-nulls` | no |
| `create_document` × 1 | sí, ClickUp | no |

**Cero mediciones nuevas, cero Kaggle, nada a Zenodo.** Es peritaje bibliográfico.

---

## 3. 🔴 VEREDICTO: SÍ, ESTÁ PUBLICADA. Y desde el MISMO dataset

**La fuente que lo cierra:**

> **Kind, E., et al.** *Morphology and synapse topography optimize linear encoding of synapse numbers in Drosophila looming responsive descending neurons.* bioRxiv **2024.04.24.591016**, eLife Reviewed Preprint **99277** (10-oct-2024).

Su **Figura 1B**, pie de figura verbatim:

> *«Looming sensitive VPN connectivity onto five DNs **based on the FAFB EM connectome**. The numbers of neurons within a VPN population are given within the circles, and the numbers of synaptic connections made by the whole population onto each DN are given next to the connections.»*

**FAFB es exactamente mi dataset.** Sus poblaciones, verbatim del panel D: *«LC4, LC6, LC22, LPLC1, LPLC2, and LPLC4»*. Sus blancos: **DNp01, DNp02, DNp03, DNp04, DNp06**. Y **DNp01 es el Giant Fiber**: su Figura 8—supl. 1 dice *«RFP labeled DNp01»* y su Figura 2 usa *«LC4 and LPLC2 synapsing onto a downstream partner (DNp01)»*.

### La prueba dura: su lista de pares reproduce mi patrón, incluidas las ausencias

La Figura 4—supl. 1 de Kind et al. enumera **todos los pares VPN-DN que analizan**, verbatim:

```
LC4-DNp02 · LC4-DNp03 · LC4-DNp04 · LC4-DNp06 · LC6-DNp06 · LC22-DNp03
LPLC1-DNp03 · LPLC1-DNp06 · LPLC2-DNp01 · LPLC2-DNp03 · LPLC2-DNp04 · LPLC2-DNp06
```

Más **LC4-DNp01**, que está en la Figura 4 principal.

**Cruzado contra lo que medí anoche:**

| Par | Yo (resp 065) | Kind et al. |
|---|---|---|
| LC4 → GF (DNp01) | **104** aristas | **presente** |
| LPLC2 → GF | **189** aristas | **presente** |
| **LC6 → GF** | **0** | **AUSENTE de su lista.** LC6 solo aparece con DNp06 |
| **LPLC1 → GF** | **0** | **AUSENTE de su lista.** LPLC1 solo con DNp03 y DNp06 |

**Coincide en los cuatro casos, incluidos los dos ceros.** Mi «hallazgo» de que LC6 y LPLC1 no tocan el Giant Fiber mientras LC4 y LPLC2 sí **está en un preprint de abril de 2024, medido sobre el mismo conectoma.**

### Y la mitad funcional es prior art de hace una década

| Fuente | Qué estableció |
|---|---|
| **Wu, M., et al. (2016)** eLife 5:e21022 | 22 tipos de LC caracterizados anatómicamente, con activación optogenética y conductas específicas por tipo |
| **von Reyn, C. R., et al. (2017)** Neuron 94:1190–1204 | *«we identify a visual projection neuron type that conveys predator approach information to the Drosophila **giant fiber (GF) escape circuit**»* — LC4, y codifica velocidad angular |
| **Ache, J. M., et al. (2019)** Curr Biol 29(6):1073–1081 | LC4 velocidad + LPLC2 tamaño, con **integración lineal dentro del GF** |
| **Morimoto, M. M., et al. (2020)** eLife 9:e57685 | *«We identified **multiple cell types downstream of LC6** in the glomerulus»* — o sea, adónde SÍ va LC6 |
| **Namiki, S., et al. (2018)** eLife 7:e34272 | la organización de la población de descendentes, mapeada sistemáticamente |

**«LC4 y LPLC2 son las entradas del Giant Fiber» no es un hallazgo de connectomíca: es el resultado central de dos papers de Card Lab, con electrofisiología y con manipulación genética.** Y yo lo presenté el 24-ago como «encontrado».

---

## 4. 🟡 Lo que el barrido NO encontró publicado

Cuatro búsquedas dirigidas a esto y no apareció:

**1 · El test contra un null que preserve neuropilos.** Kind et al. tienen **un solo** procedimiento de barajado, su Figura 5, y responde otra pregunta:

> *«Schematic representation of classifying nearest neighboring (NN) synapse pairs along the DN dendrites in the original dataset and **after shuffling synapse identities**.»*

Eso baraja **la identidad de sinapsis ya existentes a lo largo de la dendrita**: es un null de **topografía**, no de **existencia de conexión**. No puede decir si una conexión ausente es inesperada.

**2 · La métrica de oportunidad.** No encontré nada que compare **sitios sinápticos compartidos por neuropilo** entre una vía cableada y una excluida. El dato que hace fuerte mi turno anterior, **LC6 con 5.335 sitios compartidos con el GF contra 4.523 de LC4**, no aparece en ninguna fuente barrida.

**3 · LC9 y el canal DNp09.** Kind et al. **no incluyen** ni LC9 ni DNp09. El `LC9 → DNp09 = 114, 7,6×, 0/40` no está en su tabla. **⚠️ Pero ver §6: hay una fuente que probablemente lo tiene y no la leí.**

**4 · Un null de conectividad para VPN→DN en general.** Lo más cercano que apareció es de otro dominio y de este año: **Dhiman, N. (2026)**, *Topological Sensitivity in Connectome-Constrained Neural Networks*, arXiv 2604.04033, que usa **nulls que preservan grado** sobre el conectoma de la mosca y concluye, verbatim, que *«previously reported topology advantages in connectome-constrained neural networks can arise from initialization and **null-model confounds**, and largely disappear under fair from-scratch initialization and degree-preserving controls»*. **No es mi tema, pero es exactamente la lección de anoche publicada por otro, y conviene citarlo.**

---

## 5. La corrección al framing de la resp 065

**Sale** de la resp 065: *«apareció algo que no buscaba: una tabla de ruteo cruzado»* como si fuera un hallazgo.

**Entra** lo que se puede sostener:

> **La tabla de conectividad no es nueva: está en Kind et al. (2024) desde el mismo dataset, y su mitad funcional en Wu (2016), von Reyn (2017) y Ache (2019).** Lo que este trabajo agrega es **el estatus estadístico de las ausencias**: que `LC6 → GF = 0` y `LPLC1 → DNp09 = 0` sobreviven a un null que preserva el par de neuropilos, mientras que `LPLC1 → GF = 0` **no** lo sobrevive y por lo tanto es geometría. **Eso es una distinción de método, no un circuito nuevo.**

**Y hay un lado a favor que es real:** que Kind et al. reporten el mismo patrón desde el mismo conectoma con otro código y otro equipo es una **validación externa de mi medición** (B-01: cuando existe medición externa, gana, y acá coincide). Mi número no está mal. Mi reclamo de novedad sí estaba mal.

**Consecuencia para la biblioteca:** la entrada no dice «descubrimos este circuito», dice **«circuito conocido (citas), con sus exclusiones verificadas estadísticamente por primera vez (aporte propio, y ver §6)»**. Y el conteo de motivos con 0/40 **no sube a 2**: sigue en **1**, mejor caracterizado.

---

## 6. 🔴 NO MEDIDO, y el primer ítem puede tumbar lo que queda

1. **⚠️ NO leí el Cell Type Explorer del sistema visual del macho** (`reiserlab.github.io/male-drosophila-visual-system-connectome/LC9_R.html`, de **Matsliah et al. 2024, Nature**, *Neuronal parts list and wiring diagram for a visual system*). Apareció en el barrido con la página de **LC9** y **publica conectividad por tipo celular**. **Si ahí están los socios descendentes de LC9, el último pedazo de tabla que creía propio también es prior art.** Es una lectura y no la hice.
2. **NO leí los valores numéricos de la Figura 1B de Kind et al.** Es una imagen y el full text de bioRxiv no se pudo bajar. **Sé QUÉ pares reportan, por su lista de suplementos y sus pies de figura; NO tengo sus conteos.** Así que «coincide en los cuatro casos» está verificado a nivel de **presencia/ausencia**, no de magnitud.
3. **No leí los Methods de Kind et al.** Si tienen un null de conectividad en el texto y no en las figuras, el aporte de §4.1 se cae.
4. **No barrí el suplementario de BANC ni de Dorkenwald 2024** buscando tablas VPN→DN. Dorkenwald traza *«from a subset of photoreceptors to descending motor pathways»*, o sea que está en la zona.
5. **No busqué en el hemibrain** (Scheffer et al. 2020), que cubre PVLP y tiene sus propias tablas de conectividad.
6. **Cuatro búsquedas y dos lecturas no son una revisión sistemática.** El veredicto «esto no está publicado» de la §4 está **apoyado, no establecido**, y con el ítem 1 abierto **no debería citarse como establecido en ningún documento público.**
7. **Los contextos y la entrada de biblioteca siguen sin corregir** con este veredicto.

---

## 7. La regla que sale, y es la sexta vez

**Buscar el prior art ANTES de medir, no después de escribir el hallazgo.** El barrido de hoy costó cuatro búsquedas y dos lecturas: **menos que la corrida de 234 segundos que lo precedió**, y habría cambiado el framing del turno entero en vez de obligar a retirarlo.

Y el corolario, que es el que me falta interiorizar: **la pregunta «¿esto ya está publicado?» no se contesta con el abstract del paper de referencia, se contesta con su lista de figuras y de suplementos.** Es la misma lección de la resp 057 con la Fig. 5c de Lin, y la volví a necesitar cinco respuestas después.
