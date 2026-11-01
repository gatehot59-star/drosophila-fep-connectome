# Auditoría 2026-11-01-01 · Topo inverso: los números aguantan, pero la respuesta quedó fuera de main y faltaron los tres antecedentes más cercanos

**Pedido de Abraham (1-nov-2026, 09:37, America/Buenos_Aires):** «Audita la repuaantor», leído como «auditá la respuesta anterior».

**Auditado:** la respuesta 2026-11-01-01, `docs/agents/respuestas/2026-11-01-01-topo-inverso-gramatica-funcional-por-medir.md` (solo en la rama `titan/docs-gramatica-conectoma-2026-11-01`, commit `a5a1752`, blob `f1caeac`), su [Doc de ClickUp](https://app.clickup.com/90171457413/docs/2kza6fw5-26157) y los cuatro mensajes de chat de ese turno.

Doc: https://app.clickup.com/90171457413/docs/2kza6fw5-26177

**Independencia (W-01):** la respuesta auditada salió de esta misma instancia. Cada veredicto sale del repo, de los logs, del código, de una recomputación en el sandbox o de la fuente primaria, nunca del texto auditado. Igual no es una auditoría independiente: para eso hace falta otra instancia.

## Veredicto

27 afirmaciones de estado: 24 confirmadas (cuatro con una parte que no pude medir), 2 refutadas y 1 no medida. **Ningún número está mal**: todos salen igual de sus logs, y Holm, las fracciones del núcleo y la curva de c2 dan lo mismo recalculados. Los rojos están en otro lado, y el que más pesa no es científico:

1. **La respuesta no está en main.** Vive solo en una rama documental, así que el próximo turno, que arranca leyendo la última respuesta de main, no la ve. PROMETEO §6 y el protocolo del repo mandan la bitácora directo a main.
2. **Faltaron los tres antecedentes más cercanos**, y uno ya había salido en la búsqueda del turno sin que se leyera. La propuesta B es casi el cuello de botella genómico (Shuvaev y colaboradores, PNAS 2024); la A y su G0 por bloques ya tienen un SBM anidado sobre FlyWire adulto con 45 arquetipos de circuito (Betzel y colaboradores, bioRxiv 2025); las reglas genéticas que predicen motivos están en Barabási y Barabási (Neuron 2020). Así, «la diferencia defendible sería aprender y comparar las reglas de generación» no se sostiene.
3. **El motivo se describió con categorías que el instrumento no usa.** El «sensor» es una neurona de proyección visual y la «interneurona inhibitoria» es cualquier inhibitoria que no sea S ni D, ascendentes incluidas.

Le siguen dos lecturas selectivas (el núcleo y Betzel), una mezcla de lectores y detalles de forma. La causa de fondo del primero y de los de forma: en ese turno no se cargó PROMETEO, aunque su descripción nombra este repo, y se aplicó la regla de TITAN para código («nunca a main»).

## Rojos, con su regla

**R1 · La bitácora quedó fuera de main** (PROMETEO §6; protocolo del repo, paso 3; paso 1 del próximo turno). Leer la ruta en main devuelve «the file does not exist»; la rama tiene `a5a1752` encima de `3aa1a17` y nada más. Efecto: el próximo turno lee main y no la ve, y el índice de git la mandaría a «respuestas que solo están en ramas».

**R2 · Antecedentes directos sin leer** (B-01; O-01 en el orden propuesto).

- Shuvaev, Lachi, Koulakov y Zador, «Encoding innate ability through a genomic bottleneck», PNAS 121(38) e2409160121, 2024, https://www.pnas.org/doi/10.1073/pnas.2409160121: comprimen con pérdida la matriz de pesos «en varios órdenes de magnitud» y conservan desempeño antes de entrenar. Es la propuesta B, en redes artificiales.
- Betzel y colaboradores, «Hierarchical Community Structure of the Adult Drosophila Connectome Reveals Conserved Circuit Archetypes», bioRxiv, dic-2025, v2, https://www.biorxiv.org/content/10.64898/2025.12.10.689094v2: SBM anidado sobre FlyWire adulto, unas 1.500 comunidades finas y 45 meta-clusters «arquetípicos» descritos como bloques modulares. Es el G0 por bloques y la idea de plantillas reutilizadas, en el mismo conectoma. El turno anterior lo vio en la búsqueda y no lo leyó.
- Barabási y Barabási, «A Genetic Model of the Connectome», Neuron 105(3):435-445, 2020, https://doi.org/10.1016/j.neuron.2019.10.031: reglas por identidad genética que predicen motivos biclique, validadas en conectomas de tres especies.

Efecto: la diferencia propia se achica a algo más angosto (llevarlo a FlyWire con anatomía reservada y función en el banco sellado), cuya novedad sigue NO MEDIDA. Y el §5 arranca por H_REUSO_ESTRICTO, cuando lo más barato que podía cambiar el diseño era leer esto.

**R3 · Categorías del motivo** (E-01 aplicado a la descripción). En `armar()`, S es `super_class == "visual_projection"`, y la anotación de Schlegel y colaboradores (Nature 2024) separa visual projection de sensory. X es `inh & ~excl`, con `excl = (S >= 0) | (D >= 0)`: cualquier inhibitoria que no sea unidad S o D, sean centrales, ascendentes (que según esa misma anotación «pueden ser sensoriales o interneuronas») o sensoriales. La X compartida más frecuente en las dos moscas es `AN_multi_11` (24 tipos de descendente en FlyWire, 19 en BANC); el prefijo es el de las ascendentes, superclase no verificada. Efecto: la «regla candidata» del §4A («familias sensor-descendente… población inhibitoria compartida») generaliza a sensores y a interneuronas locales algo que se midió entre proyección visual y descendentes, con X de cualquier clase. El rótulo «sensores» viene del propio log (`UNIDADES sensores=652`): heredado, no inventado.

**R4 · Lectura selectiva del núcleo.** El mismo log citado dice `HIPOTESIS H_CABLEADO_NUCLEO -> SOSTENIDA`: el núcleo, con el 14,96 % de las aristas y el 56,97 % de las sinapsis de R2, da 0,9135 contra 50 SL (media 0,5913, máximo 0,7570) y 50 T (media 0,6869, máximo 0,7680), Holm 0,0392. O sea: pierde 4,59 puntos contra R2 y a la vez queda 32,2 puntos sobre la media de sus barajados SL. Para una exploración de compresión es el dato más útil del log, y no aparece.

**R5 · Betzel 2024 leído para la cantidad equivocada** (E-01). Es el conectoma larval (2.952 células, unas 352.611 sinapsis). El número de sinapsis no correlaciona con la distancia entre somas (r = −0,0015) y sí con el camino por la arborización (r = 0,24); pero el mismo trabajo dice que **la probabilidad de conexión sí decae** con la distancia entre somas. La fórmula del pedido es un logit de P(i→j): justo la cantidad donde la distancia sí tuvo efecto. La respuesta no dice larva ni separa probabilidad de peso.

**R6 · Lectores mezclados.** Factorial 4 y núcleo se midieron con W (las descendentes con umbrales calibrados en ensayos sin evento, sin lector entrenado), y la función que la propuesta B quiere conservar es la curva de MOSCA_L, con lector. «Retener conexiones fuertes no bastó» vale para W; con MOSCA_L no se midió.

**R7 · Tres cosas chicas, ciertas pero cortas.** (a) El signo de FlyWire también es neurotransmisor predicho (Shiu y colaboradores, Nature 2024: «connectivity and predicted neurotransmitter identity»), no solo el de BANC. (b) T1 se dio sin su nulo: en FlyWire la plantilla aparece en el 68,23 % de los pares aun barajando (máximo 74,62 %), contra el 88,35 % real. (c) En c2 el crudo iguala o supera al embudo desde n = 96 (0,9347 contra 0,9298) y PCA desde 768 (0,9930 contra 0,9897), dentro de la curva sellada; no recién a 2.400.

**R8 · Forma** (M-03 y el protocolo del repo). Nombre con 2 dígitos cuando el protocolo pide `NNN` (el índice lo mostraría como `2026-11-01-01-`). Prefijo `docs(respuesta):` en vez de `resp(NNN):` o `respuesta(…)`. Bloque `METODO TITAN` y no `METODO PROMETEO`. Sin línea `Doc:`: el índice tomaría el Doc por «primer link, revisar» (probé las regex exactas: la línea del §8 empieza con `- [Doc público:` y no matchea; `Doc: <url>` sí). Fuentes numeradas desde E3, sin E1 ni E2. Doc y git con el mismo contenido pero no el mismo texto, el patrón que ya marcó la auditoría 2026-10-19-01 (#9).

## Lo que cacé sin encontrar nada

- **Instrumento contaminado:** las cifras salen de logs anteriores a la respuesta (`reuso.log` del 15-oct, 01:11 UTC; los agregados del factorial 4, del núcleo y de los pares, en sus commits de octubre), y las encontré en esos logs, no en texto propio.
- **Sujeto equivocado en el código:** `reuso_mosca.py` tiene un solo commit en su rama (`613317d`, el sello): lo leído es lo que corrió.
- **Documento vencido:** main no se movió desde `3aa1a17` (19-oct); el CONTEXTO leído era el vigente.
- **Canal sin leer:** el pizarrón (`nexus.db`) no tiene mensajes desde el 25-oct ni mensajes sin leer sobre el conectoma. Los 11 trabajos con `resultado_leido=0` (ids 3, 9 y 13 a 21) son viejos y ninguno cambia esta respuesta; el 16 (reciprocidad y KC→MBON contra nulos CP) es del conectoma y sigue sin dueño: deuda vieja, no de este turno.
- **Límites propios sin medir, corridas o gasto ajeno:** ninguno; el commit es un solo archivo de docs.
- **Mi sospecha de que «núcleo fuerte» era un rótulo equivocado:** falsa. El sello define el núcleo por fuerza (10 sinapsis o más, o más del 1 % de la entrada de la post).

## Lo que no se midió y importaba

1. Los antecedentes con nombre propio, antes de recomendar el primer experimento (R2).
2. El alcance real del motivo: qué superclase tienen las 698 y 419 X, y si T1 y T2 aguantan con S sensorial o con X solo central.
3. Si los negativos de compresión aguantan con el lector entrenado (R6).
4. Que la respuesta exista para el próximo turno, o sea, que esté en main (R1).

## Qué tiene que hacer BRAIN (propuesto; esta auditoría no lo aplica)

1. Llevar la respuesta a main con número `NNN`, línea `Doc:`, prefijo `respuesta(…)` y bloque METODO PROMETEO. Borrar la rama queda para Abraham.
2. Corregir donde se publicó (E-01): sensor → neurona de proyección visual; interneurona → neurona inhibitoria X de cualquier superclase salvo VPN y DN; signo predicho en las dos moscas; T1 con su nulo; agregar H_CABLEADO_NUCLEO; aclarar W contra MOSCA_L; Betzel larval y probabilidad contra peso; c2 desde n = 96.
3. Reescribir la diferencia propia con los tres antecedentes y reordenar el §5: leerlos antes de sellar, usar el SBM anidado como G0 y el cuello de botella genómico como rival de B.
4. Anotar como pendiente H_REUSO por superclase (S sensorial o VPN; X central o ascendente).

## Las 27 afirmaciones, una por una

| # | Afirmación | Instrumento | ¿Podía dar rojo? | Veredicto |
|---|---|---|---|---|
| 1 | H_REUSO: 88,35 % y 82,60 %; 698 y 419 contra 128,6 y 11,0; Holm 0,0199 | `reuso.log` (blob `ef631e9`) y la `holm()` del instrumento, recorrida en el sandbox | sí | CONFIRMADO |
| 2 | El código leído es el que corrió | historia de `reuso_mosca.py` en su rama: un solo commit, `613317d` | sí | CONFIRMADO |
| 3 | El nulo baraja destinos dentro de bloques de lado y no conserva la salida de cada X a la clase descendente | `nulo()` y `guarda_nulo()` | sí | CONFIRMADO |
| 4 | «un sensor conecta con una descendente» | `armar()`: S es visual_projection; Schlegel 2024 la separa de sensory | sí | REFUTADO en lo literal; el rótulo «sensores» es del propio log |
| 5 | «una interneurona inhibitoria» | `xs = inh & ~excl` | sí | NO MEDIDO: el instrumento no exige interneurona |
| 6 | «el signo en BANC es una convención basada en neurotransmisor predicho» | `cargar_banc()` y Shiu 2024 | sí | CONFIRMADO, incompleto: el de FlyWire también es predicho |
| 7 | Embudo: +15,20 sobre PCA, +9,04 sobre proyección, +4,01 sobre crudo, curva 6 a 768, dos condiciones | `agregado.log` de H_PARES_DATOS (blob `66c19d1`) | sí | CONFIRMADO |
| 8 | R2 tiene 33.489 neuronas y 4.031.897 aristas | CONTEXTO (factorial 2) y `SELLO-NUCLEO.md` | sí | CONFIRMADO |
| 9 | «con 2.400 ejemplos el crudo y PCA lo superan en c2» | curva c2 recorrida en el sandbox | sí | CONFIRMADO, corto: el crudo lo iguala o supera desde n = 96 y PCA desde 768 |
| 10 | Factorial 4: +0,01 puntos, IC90 [−0,01; +0,04], equivalente | `agregado.log` (blob `77ee160`) | sí | CONFIRMADO; medido con W |
| 11 | Núcleo: −4,59 puntos, IC90 [−5,07; −4,10], pierde en 600 de 600 | `agregado.log` (blob `86ce131`) | sí | CONFIRMADO; medido con W |
| 12 | «Retener conexiones fuertes no bastó»; en el chat, «núcleo fuerte» y «podar por fuerza» | `SELLO-NUCLEO.md` (blob `2a8190e`) | sí | CONFIRMADO; lo sospeché como rojo y lo descarto |
| 13 | MN9: cambiar la célula cambia qué nulos pasan | Docs de las respuestas 051, 055 y 056 (títulos y fragmentos) | sí | CONFIRMADO por los Docs; no releí sus logs |
| 14 | Topo v0.2: 800 de 800 iguales, DNp06 comparadas, H_COMPARADOR pendiente | `TOPO-v0.2-diferencial.md` (blob `5c47150`) | sí | CONFIRMADO |
| 15 | H_REUSO_ESTRICTO es el control pendiente | Doc del 15-oct sobre la auditoría de Fable | sí | CONFIRMADO que existía; NO MEDIDO que el §5.1 sea el mismo diseño |
| 16 | DBC-RT-AUTO1 ROJO, cubeta INVÁLIDA, auto-modelo SELF | respuesta 2026-11-01-02 de mojo-absoluto (blob `7a047d5`) | sí | CONFIRMADO |
| 17 | FlyVis: 64 tipos, 26 estudios, 45.669 neuronas, 1.513.231 conexiones, 734 parámetros | resumen de Nature, releído hoy | sí, para 64 y 26 | CONFIRMADO 64 y 26; NO MEDIDO hoy las otras tres |
| 18 | Karahan: predictor rápido y verificación por otra vía | resumen y fragmentos de Nature Communications | sí | CONFIRMADO; NO MEDIDO hoy «circuitos fabricados» |
| 19 | Péntek y Ercsey-Ravasz: regla de distancia entre regiones | fragmento del artículo | sí | CONFIRMADO |
| 20 | Betzel: «a escala celular, distancia entre somas y costo por arborizaciones no son intercambiables» | PMC11420166 | sí | CONFIRMADO en lo literal; es la larva y ahí la probabilidad de conexión sí decae con la distancia |
| 21 | El cargador no lee geometría ni solapamientos | `cargar_flywire()` y `cargar_banc()` | sí | CONFIRMADO |
| 22 | Una tabla beta por pares de tipos puede memorizar tanto como una matriz | 8.453² en el sandbox | sí | CONFIRMADO, y se queda corto: 71.453.209 celdas, 4,73 veces las aristas |
| 23 | «La diferencia defendible sería aprender y comparar las reglas de generación» | Shuvaev 2024, Betzel 2025 y Barabási 2020 | sí | REFUTADO en su forma general |
| 24 | Sin mediciones nuevas, sin código, sin merge | commit `a5a1752`: un archivo de docs, 212 líneas | sí | CONFIRMADO |
| 25 | Archivo commiteado y leído de vuelta | lectura en la rama: blob `f1caeac` | sí | CONFIRMADO en la rama; en main no está (R1) |
| 26 | El contexto canónico no cambió y no había estado nuevo | commits de main: el último es `3aa1a17`, del 19-oct | sí | CONFIRMADO |
| 27 | El chat nombró el archivo y el Doc | los mensajes del turno | sí | CONFIRMADO; NO MEDIDO que el link haya llegado clickeable |

## Evidencia cruda

- **main sin la respuesta.** Leer la ruta con `ref=refs/heads/main` devolvió, tal cual: «Failed to get file contents. The path does not point to a file or directory, or the file does not exist in the repository.» La rama tiene `a5a1752` (2026-11-01T08:05:20Z) encima de `3aa1a17` y nada más.
- **Blobs leídos:** `reuso.log` `ef631e911155afbc468658c410f552681264d78f`; `reuso_mosca.py` `37b358353ccac46c4b84766f1a63df556dfe531d`; agregado de H_PARES_DATOS `66c19d19aacb904b4c45b650c78fb19177999b4b`; factorial 4 `77ee1609cc478358f2f7f36d8e11eb9c2120ccbe`; núcleo `86ce1311ea8d7bf8e4a1d99d8846729093543f3f`; `SELLO-NUCLEO.md` `2a8190e03b47e34e999706e4b4b03b9a12fcde3e`; `TOPO-v0.2-diferencial.md` `5c4715094fc89fe4bc11d04135f8a14245e8eeec`; protocolo de bitácora `cd94baba05d4b41678e854008f75a43180469d43`; `generar_indice.py` `ef57d55941a1807fd5fb9e6354ebb8ca0717e7a9`; respuesta auditada `f1caeac0ea856f45035465608373452c8f35b3fe`; AUTO1 en mojo-absoluto `7a047d5177a1c8e964eacec7dfb6baf201fec106`.
- **Del log del núcleo (R4), tal cual:**

```
NULOS SL n=50 media=0.5913 max=0.7570 W=0.9135 iguales_o_mejores=0 p_sup=0.0196
NULOS T n=50 media=0.6869 max=0.7680 W=0.9135 iguales_o_mejores=0 p_sup=0.0196
NULOS Holm SL=0.0392 T=0.0392
HIPOTESIS H_CABLEADO_NUCLEO -> SOSTENIDA
HIPOTESIS H_CONSENSO -> REFUTADA
```

- **De `reuso.log` (R3 y R7b), tal cual:**

```
FLYWIRE UNIDADES sensores=652 descendentes=925 pares_cableados=996 | 0.1 s
FLYWIRE T1 fraccion_con_plantilla=0.8835 nulo media=0.6823 max=0.7462 p=0.0050
FLYWIRE COMPARTIDA AN_multi_11 tipos_de_descendente=24 DNa01,DNa03,DNa11,DNa13,DNae010,DNb01,DNb09,DNbe001,DNg82,DNg94,DNge041,DNp05
BANC COMPARTIDA AN_multi_11 tipos_de_descendente=19 DNa01,DNa03,DNa09,DNa11,DNa13,DNae007,DNae010,DNb01,DNb09,DNg01,DNg82,DNp09
```

- **Pizarrón** (`nexus.db` por el gateway, solo `SELECT`): ningún mensaje con `ts >= '2026-10-25'` ni sin leer sobre conectoma, Topo o reuso; 11 filas de `trabajos_vivos` con `resultado_leido=0` (ids 3, 9 y 13 a 21), todas con `lanzado_ts` vacío.
- **Recomputo en el sandbox de ClickUp** (Python 3.12, exit 0): `docs/auditorias/evidencia/2026-11-01-01/recomputo.py` (5.256 B, md5 `f8bf3cd4e1fa3a6240dd6cbc12f48062`, blob calculado `a2fe2a64b5dca9ffcc271e41bd5b785988e1e41e`) y su salida `recomputo.log` (2.544 B, md5 `5bba15a75e950441228bf6d8ff6430ca`, blob calculado `a6c5209e5495292825091be5d05c3c73009e319a`). Copia tal cual las dos regex de `generar_indice.py`, la `holm()` de `reuso_mosca.py` y las líneas de la curva c2. La tercera línea de la prueba de regex no es control positivo aunque el script la rotule así: reproduce el encabezado de la auditoría 2026-10-19-01, donde `Doc:` va a mitad de renglón, y tampoco matchea; los controles positivos son las dos líneas que empiezan con `Doc`. El cotejo de esos blobs contra los que devuelve GitHub se hace después del push; si no coinciden, la copia de git no es byte a byte la que corrió.
- **Fuentes web:** Shuvaev 2024, https://www.pnas.org/doi/10.1073/pnas.2409160121; Betzel 2025, https://www.biorxiv.org/content/10.64898/2025.12.10.689094v2; Barabási 2020, https://doi.org/10.1016/j.neuron.2019.10.031; Betzel 2024, https://pmc.ncbi.nlm.nih.gov/articles/PMC11420166/; Shiu 2024, https://www.nature.com/articles/s41586-024-07763-9; Schlegel 2024, https://www.nature.com/articles/s41586-024-07686-5; Lappalainen 2024, https://www.nature.com/articles/s41586-024-07939-3; Karahan 2024, https://www.nature.com/articles/s41467-024-54178-1.

## NO MEDIDO por esta auditoría

- El md5 de `reuso_mosca.py` contra el `e9a07a7c` del log: me apoyé en que hay un solo commit.
- La superclase de `AN_multi_11` en la tabla de anotaciones.
- El «88 % de la ventaja» post hoc del núcleo que recuerda el CONTEXTO: mis dos lecturas del CONTEXTO se cortaron antes de esa sección.
- FlyVis 45.669, 1.513.231 y 734, y los circuitos fabricados de Karahan: los resúmenes no los traen y no releí el texto completo.
- El texto completo de Betzel 2025, Shuvaev 2024 y Barabási 2020: leí resúmenes y fragmentos.
- Si el link del chat llegó clickeable, y los checks de CI de `a5a1752`.
- La prueba de regex usa la línea real del §8 con una URL sintética de ClickUp; el resultado de `RE_DOC` no depende de la URL.

## Rúbrica de la respuesta auditada

| Criterio | Score | Evidencia |
|---|---|---|
| Completitud | 7/10 | los seis campos están; faltan H_CABLEADO_NUCLEO, el nulo de T1, el alcance larval y los antecedentes (R2, R4, R5, R7) |
| Razonamiento | 7/10 | separa propuesta de medición y pone falsadores; falla en las categorías y en la cantidad de Betzel (R3, R5, R6) |
| Documentación | 7/10 | todo con SHA y link exacto; sin línea Doc:, sin E1 ni E2, Doc y git con texto distinto (R8) |
| Innovación | 7/10 | Topo inverso, G0 contra G1 y elegir experimentos por desacuerdo; B sin reconocer su antecedente (R2) |
| Proceso QA | 8/10 | cada número rastreado a su blob y confirmado hoy; testigo único (W-01) y una fuente vista sin leer |
| Entrega en repo | 4/10 | commiteado y leído de vuelta, pero fuera de main (R1) |

N/A: ejecutabilidad, seguridad, testing y DevOps, porque no hay código. Total 40/60, o sea 66,7/100: no llega a 90.

--- METODO PROMETEO ---

Rol: auditor (no BRAIN). Delicado: no; auditoría y evidencia a main, sin tocar lo auditado.  
Máquina: sandbox de ClickUp (recomputo, exit 0), conector de GitHub (lectura y push), búsqueda web y lectura de fuentes, buscador de ClickUp, `nexus.db` por el gateway (solo lectura). brain-env, Actions y Kaggle: no usados.  
Independencia: NO, misma instancia que escribió la respuesta.  
Rúbrica de esta auditoría: completitud 8/10, razonamiento 8/10, documentación 8/10, proceso 6/10; promedio 7,5: sirve como chequeo contra el repo, no como auditoría independiente.  
Artefactos: `docs/auditorias/2026-11-01-01-topo-inverso-numeros-bien-bitacora-fuera-de-main.md` en main y https://app.clickup.com/90171457413/docs/2kza6fw5-26177
