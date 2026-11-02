# Auditoría Astra: los 17 relevos se sostienen; el 7/7 no valida el mecanismo y el diseño 009 requiere enmienda

**Veredicto: conservar el hallazgo anatómico, bajar el alcance del predictor y corregir el diseño antes de ejecutar RELEVOS16.** No encontré una gramática funcional demostrada. Encontré un candidato anatómico fuerte, un ajuste retrospectivo reproducible y errores concretos que cambiarían la interpretación del experimento siguiente.

Pedido: auditar, explorar, contrastar, mejorar e innovar sobre los seis adjuntos. Fecha: 2-nov-2026. Repositorio auditado en vivo: `gatehot59-star/drosophila-fep-connectome`, base `c3b718dbdb69c9d0ad25e5a729f1d06cf2ed297a`. La auditoría es nueva; no reemplaza ni modifica los sellos anteriores.

Los [instrumentos ejecutados y sus salidas completas](https://github.com/gatehot59-star/drosophila-fep-connectome/blob/main/docs/auditorias/evidencia/2026-11-02-03-astra-topo/evidencia-verbatim.md) quedaron separados de este dictamen. Releí desde Git las tres fuentes y los tres stdout: los seis coinciden byte por byte con los originales.

## 1. El 7/7 existe; su explicación todavía no está validada

Recalculé el predictor de 008 desde las cuentas neuronales y el parquet, sin importar las funciones del productor:

- Predictor lineal anterior: R² = **0,4984535**, MAE = **0,1312026**, 4/7 errores ≤ 0,15.
- Predictor rectificado de 008: R² = **0,9065287**, MAE = **0,0608423**, 7/7 errores ≤ 0,15.

Hasta ahí, PASS. El problema aparece al preguntar qué demuestra ese ajuste. El [archivo crudo de la auditoría 008](https://github.com/gatehot59-star/drosophila-fep-connectome/blob/main/docs/auditorias/evidencia/2026-11-02-01/auditoria_e_innovacion_2026_11_02.json) contiene dos controles distintos:

- Barajar las predicciones entre los siete pares: p = **0,0015**. Pregunta si el emparejamiento global es mejor que mezclarlo.
- Barajar las actividades basales entre blancos dentro del estímulo: p = **0,1043** para el MAE. Pregunta más directamente si importa asignar la actividad al blanco correcto.

El resumen destaca el primero y no presenta el segundo. No son pruebas intercambiables. Implementé además una permutación compartida por estímulo, para que los pares que comparten blancos reciban la misma barajada: **1.396/10.000** resultados igualan o mejoran el MAE observado; p Monte Carlo con corrección +1 = **0,139686**. Este nulo es condicional: las barajadas de distintos estímulos son independientes, por lo que no conserva adicionalmente la identidad de blancos compartidos entre estímulos. La enumeración global exacta da **7/5.040 = 0,0013889**, consistente con la prueba global publicada.

**Conclusión:** el ajuste descriptivo se reproduce, pero estos controles no establecen que la localización correcta del estado basal explique su ventaja. Eso no refuta universalmente el predictor; impide presentarlo como mecanismo validado o como predicción fuera de muestra.

Hay sólo siete combinaciones, con tres estímulos y tres tipos de X repetidos, no siete circuitos biológicos independientes. La fórmula se construyó después de observar sus errores: no tener coeficientes ajustados no elimina la selección retrospectiva de la fórmula.

## 2. El diseño 009 cambia la fórmula y no fija el puente hacia el efecto que quiere predecir

En 008, la predicción es una fracción adimensional:

`p_i = Σ_j [(r_i · w_ij / Σ_l r_l · w_lj) · (r_j / Σ_j r_j)]`

Las tasas son basales C0; los denominadores corresponden a las poblaciones X y D′ de cada estímulo.

La sección 7 del [009 completo en Git](https://github.com/gatehot59-star/drosophila-fep-connectome/blob/c3b718dbdb69c9d0ad25e5a729f1d06cf2ed297a/docs/agents/respuestas/2026-11-02-009-diseno-corte-causal-16-relevos-recurrentes.md) introduce otra cantidad:

`B_eff = r_X · Σ_d [w_Xd · min(1, r_d / (r_d + 10))]`

No es una reformulación equivalente: desaparecen las normalizaciones, entra una escala fija de 10 Hz y el resultado ya no es una fracción. Para tasas no negativas, el `min(1, ...)` es redundante. Tampoco queda definido cómo convertir esa cantidad a la liberación que se evaluará.

Además, 008 predice el efecto de quitar las salidas de una X relativo a quitar las del conjunto X. En 009, `r_Q1` compara quitar una arista D→X con quitar las salidas de su X. Son contrastes distintos; una fórmula validada para uno no queda validada para el otro.

La evidencia conserva una exploración propia rotulada en el código `B009_raw` y `B009_norm_exploratory`. Esos nombres son demasiado amplios: el cálculo usa la población D del banco de 008, no el D′ específico de cada relevo de 009, y su normalización por el total sobre X no está sellada. **No uso sus R² para evaluar el predictor literal de 009.** La revisión crítica detectó esta diferencia de sujeto antes del cierre; los números quedan como exploración, no como prueba a favor ni en contra del nuevo predictor.

Se puede calcular matemáticamente un R² entre esas columnas, pero sin un mapeo fijado a la escala del efecto no mide la predicción causal que se pretende evaluar. El problema no es una operación matemática prohibida: es la falta de especificación y de comparabilidad.

Corrección necesaria: congelar fórmula, unidades, población, denominador y variable objetivo antes de la corrida. Conservar 008 como baseline descriptivo reproducido; cualquier variante de 009 necesita nombre y evaluación propios.

## 3. Las colaterales están atribuidas al conjunto equivocado en los 16 relevos

El diseño define D′ como los descendentes inhibidos directamente por X, excluyendo el driver. Pero el cálculo de `collateral_w_D_to_Dp` suma la excitación del driver hacia **todos los otros descendentes**, no sólo hacia ese D′.

Recalculé las dos máscaras sobre las 15.091.983 filas. En los 16 casos, el valor publicado coincide con la población amplia. La comparación correcta, restringida al D′ definido, es:

<table>
<tr><th>Relevo</th><th>Publicado</th><th>Hacia su D′ real</th></tr>
<tr><td>R01 DNp35→CB0527</td><td>1.192</td><td>935</td></tr>
<tr><td>R02 DNpe016→cL22c</td><td>405</td><td>135</td></tr>
<tr><td>R03 DNa03→PLP060</td><td>1.944</td><td>452</td></tr>
<tr><td>R04 DNpe023→CB0172</td><td>772</td><td>566</td></tr>
<tr><td>R05 DNp71→CB0534</td><td>913</td><td>237</td></tr>
<tr><td>R06 DNp104→CB0626</td><td>218</td><td>69</td></tr>
<tr><td>R07 DNg100→CB0534</td><td>725</td><td>84</td></tr>
<tr><td>R08 DNa03→VES041</td><td>1.944</td><td>1.527</td></tr>
<tr><td>R09 DNpe023→cL22b</td><td>772</td><td>307</td></tr>
<tr><td>R10 DNp47→CB0580</td><td>575</td><td>27</td></tr>
<tr><td>R11 DNa06→PS100</td><td>937</td><td>670</td></tr>
<tr><td>R12 DNae007→PS065</td><td>1.222</td><td>750</td></tr>
<tr><td>R13 DNp104→CB0580</td><td>218</td><td>10</td></tr>
<tr><td>R14 DNp101→CB0580</td><td>1.135</td><td>70</td></tr>
<tr><td>R15 DNge148→PS100</td><td>237</td><td>118</td></tr>
<tr><td>R16 DNae005→CB0172</td><td>1.025</td><td>734</td></tr>
</table>

Esto importa especialmente en R03: la comparación anatómica presentada como 1.944 sinapsis excitatorias contra 410 inhibitorias debe ser **452 contra 410** para esos mismos blancos. Ninguno de esos cocientes anatómicos demuestra todavía cuál efecto funcional domina.

También hay un problema causal separado: `F(Q1) - F(Q3)` no aísla la colateral directa D→D′. Q3 elimina todas las salidas de D y modifica otras rutas. Para identificar esa rama hace falta cortarla selectivamente, no atribuirle la diferencia entre dos intervenciones globalmente distintas.

## 4. El resultado fuerte sobrevive: 17 relevos, incluso después de corregir el nulo

Reconté los pares desde FlyWire y BANC: **7.052** pares tipados en FlyWire, **5.867** en BANC, **2.701** compartidos y **17** con al menos 80 sinapsis en una arista individual en ambos. Spearman de los máximos compartidos: **0,6120192**.

La entrada BANC utilizada es **v888**, no v626: se leen `banc_888_meta.feather`, `root_888` y `banc_888_edgelist_simple_v3.feather`. El escaneo recorrió **13.620.865** filas y verificó **cero identificadores de extremo sin correspondencia**. El peso BANC de DNp04→PVLP010 es **123**; el 138 que aparece en el 009 completo corresponde a DNpe016→cL22c.

El nulo descrito como conservador de grado baraja extremos y luego convierte las parejas en un conjunto. Si hay duplicados, los colapsa. Reproduje su media de **2,3173** coincidencias, pero **3.403/10.000** muestras pierden aristas únicas: no conservan exactamente los grados del subgrafo bipartito simple de **31 parejas pesadas BANC**.

La mejora ejecutada rechaza esas muestras antes de aceptarlas, preservando los grados simples de ese subgrafo pesado BANC:

- **10.000** muestras válidas en **15.332** intentos.
- Grados simples verificados en las **10.000**.
- Media **2,4183** coincidencias, máximo **9**, frente a **17** reales.
- **0/10.000** alcanzan al real; p Monte Carlo con +1 = **1/10.001**.
- Un caso negativo sintético conserva los grados de los extremos repetidos pero pierde grados simples: el control lo detecta.

Es muestreo independiente con rechazo, no una cadena de swaps cuya mezcla se da por supuesta. Conserva los márgenes simples del subgrafo pesado BANC; no los grados ponderados, los del conectoma completo ni simultáneamente los de FlyWire. Bajo ese nulo corregido y con FlyWire fijo, la conservación anatómica sigue siendo fuerte. El error del nulo original **no derrumba el resultado**.

El alcance sigue siendo condicional al vocabulario, al umbral y a las X de cierre heredadas. No controlamos geometría ni todos los sesgos de anotación. BANC participó en seleccionar estos 17 candidatos: no es un conjunto reservado para una nueva validación funcional. El p extremadamente pequeño de Spearman tampoco vuelve independientes a los pares que comparten tipos.

## 5. El documento maestro introdujo números incorrectos de H_REUSO_CIERRE

La sección 15 del [adjunto maestro más reciente](https://t90171457413.p.clickup-attachments.com/t90171457413/31e8f5e3-303e-4930-9940-0c955197bec9/2026-11-01-001%20%C2%B7%20Topo%20inverso_%20tenemos%20piezas%20para%20buscar%20una%20gram%C3%A1tica%20funcional%20del%20conectoma%2C%20todav%C3%ADa%20no%20la%20gram%C3%A1tica-20261102185950.md) dice que las medias nulas son 80,26 % y 74,31 % para T1, y 539,86 y 328,99 para T2.

Reagregué los 200 nulos por conectoma del [JSON original de cierre](https://github.com/gatehot59-star/drosophila-fep-connectome/blob/7f3cbc1b1ff2243149ba45d10c18abb4ce5311e4/results/reuso_cierre_2026-11-01/cierre.json):

<table>
<tr><th>Métrica</th><th>FlyWire real / media nula</th><th>BANC real / media nula</th></tr>
<tr><td>T1, proporción de pares con cierre</td><td>88,3534 % / 49,6606 %</td><td>82,6029 % / 35,0106 %</td></tr>
<tr><td>T2, X compartidas</td><td>698 / 286,04</td><td>419 / 76,515</td></tr>
</table>

Los cuatro p ajustados por Holm siguen siendo **0,0199005**. El resultado archivado no falla: falla su nueva transcripción. No volví a generar los 400 nulos; comprobé sus agregados.

## 6. Lo que sí quedó confirmado y lo que falta para identificar mecanismos

PASS medido en esta auditoría:

- **64/64** guardas individuales Q1 a Q4 correctas.
- Las **seis** instancias concretas de hub tienen Q1 y Q4 conjuntos correctos. Cuatro tipos de hub no son cuatro neuronas.
- Unión de la cascada R01: **1.678 filas, 18.858,0** de peso absoluto.
- DNp04, sobre resultados existentes: efecto Q1 **102,45**, efecto Q2 **188,35**, referencia global **252,6**; las fracciones **40,56 %** y **74,56 %** se reproducen. `s4 = 0,9676664`.

Eso verifica las selecciones y los números, no las compuertas ni la causalidad de la mosca. Antes de ejecutar el diseño, corregiría estos puntos:

1. **Poisson no es un clamp de salida.** Inyectar actividad no fija el tren de espigas emitido. Poner las salidas en cero tampoco apaga el disparo interno. Nombrar por separado corte de conexiones, estímulo externo, silencio celular y reproducción forzada de un tren.
2. **OR/AND requiere coactivación.** Medir ningún driver, cada uno por separado y todos juntos; luego retirar aristas bajo coactivación. Una OR saturada no tiene por qué superar al máximo individual. Coincidencia exige además controlar el desfase temporal a iguales tasas.
3. **R01 necesita una intervención específica.** Q6 retira todas las salidas de AVLP080. Compararlo con Q6∪Q1 prueba la dependencia del relevo en esa red alterada, no la mediación exclusiva AVLP080→DNp35. Añadir el corte de esa arista y controles de actividad de DNp35.
4. **El ratio r_Q1 es legítimo como efecto relativo, no necesariamente como fracción exclusiva.** Reportar numerador y denominador con unidades e intervalos. Definir qué pasa si el denominador es pequeño o no positivo; `max(denominador, 1e-9)` no lo vuelve interpretable.
5. **No esconder los fallos del régimen nativo con el artificial.** A mide reclutamiento por la aferencia elegida; B, transmisión bajo activación impuesta. Un relevo no reclutado en A sigue siendo un resultado de A, aunque responda en B.
6. **Cerrar el plan estadístico.** Elegir una prueba primaria, familias Holm exactas y tratamiento de ceros antes de mirar resultados. Veinte semillas cuantifican variación de la estimulación en un modelo fijo, no veinte animales ni incertidumbre del modelo. Los BCa no eliminan esa limitación.

Los estratos T1/T2/T3 son hipótesis útiles dentro de la parametrización elegida. El umbral aislado de 162 sinapsis no garantiza disparo en todos los estados de una red recurrente. El signo glutamatérgico de R15 no es un rojo contra el modelo: allí se declara inhibitorio; su fisiología real sigue NO MEDIDA.

## 7. Mejora ejecutada e innovación que vale la próxima corrida

No dejé sólo recomendaciones. Quedaron implementados y ejecutados cuatro controles nuevos: permutación compartida por estímulo, enumeración global exacta, nulo de grados simples del subgrafo pesado BANC con rechazo y conteo de colaterales restringido al D′ correcto.

**Mi apuesta: una gramática que prediga respuestas a intervenciones reservadas en distintos estados, no sólo que genere motivos parecidos.** Una regla debería especificar quién conecta con quién, bajo qué estado se recluta y qué cambia al cortar una rama. La equivalencia funcional sola no identifica esa regla.

La extensión concreta que propongo, todavía NO EJECUTADA, tiene tres partes:

- **Susceptibilidad, no sólo actividad basal.** Comparar 008 contra un predictor basado en la sensibilidad local del blanco a pequeñas perturbaciones independientes. Una tasa basal pequeña no significa automáticamente que quitar inhibición tenga poco efecto: puede haber un blanco silenciado cerca de una transición. Falsador: la sensibilidad no mejora la predicción de cortes reservados frente al baseline de actividad. Medir esa sensibilidad en un conjunto de calibración separado, sin usar la respuesta al corte que se quiere predecir.
- **Biblioteca de firmas causales.** Empezar con H2/CB0534 y H3/CB0172: dos drivers de distinta procedencia sobre la misma X permiten un factorial pequeño y discriminante. Agregar R01 con corte específico y control temporal. Falsador: las firmas de relevo, redundancia o coincidencia no se distinguen de un modelo por tipo/grado sin esa regla.
- **Reserva por familias, no por filas mezcladas.** Separar hubs, drivers compartidos, homólogos y estímulos antes de ajustar. Purgar del entrenamiento las dependencias del bloque de prueba; si esa agrupación deja un solo bloque, reservar circuitos o estímulos nuevos en vez de fingir validación cruzada independiente. Falsador: la ventaja desaparece al hacer esa separación.

El orden propuesto responde a un criterio: gastar simulación sólo cuando las intervenciones puedan distinguir explicaciones. Primero fijar fórmula, sujetos y estimandos; después dos hubs y R01; recién después extender a los 16. Es una recomendación técnica, no una orden emitida ni una enmienda activa del sello.

## 8. Contraste externo: la novedad posible es más precisa que “descubrir la gramática”

La revisión focalizada de cinco textos primarios deja una frontera clara:

- **Shiu:** habilita hipótesis mecanísticas en un LIF; sus simplificaciones y tasas basales no sustituyen la fisiología del relevo estudiado.
- **FlyVis:** combina estructura compartida y tarea, y muestra modelos con desempeño parecido pero parámetros distintos. Es un antecedente directo contra la idea de mecanismo único.
- **Shuvaev:** un generador compacto puede producir pesos útiles, pero la expansión de la red sigue costando. Compresión de descripción no equivale a aceleración.
- **Barabási:** las reglas generadoras y los motivos composicionales ya tienen antecedentes; no corresponde reclamar esa idea general como nueva.
- **Pospisil:** el conectoma especifica caminos posibles, no la fuerza de sus efectos en vivo. Su trabajo sobre el effectome es el puente conceptual pertinente; la validación del estimador que se discutió es mediante simulaciones, no un effectome completo medido en la mosca.

Lo defendible como proyecto propio es combinar anatomía reservada, intervenciones reservadas, función del embudo y costo total. Contar reglas, parámetros, etiquetas, excepciones y decodificador por un lado; memoria, tiempo y energía de ejecución por otro. La prioridad global de esa combinación sigue NO MEDIDA: esto no fue una revisión sistemática.

## 9. Procedencia, reproducibilidad y límites de esta auditoría

Los tres adjuntos más antiguos son idénticos: 83.267 bytes y el mismo SHA-256. Hay cuatro contenidos distintos entre seis archivos, no seis verificaciones independientes. La autoría no se deduce del orden de adjuntos: el historial de 008 y los reportes 144/145 atribuyen 008/009 a Argon. Por eso este dictamen identifica archivos y afirmaciones, no puntúa marcas de modelo.

En el main fijado faltan seis auxiliares usados o referidos por el proceso: `conservar_relevos_dx.py`, `disenar_16_relevos.py`, `diseno_corte_16_relevos.json`, `censo_g1_recurrente.py`, `censo_g1_recurrente.json` y `chequear_16_en_4estimulos.py`. No afirmo que falten en todas las ramas. El sellador publicado serializa un JSON previo; por sí solo no vuelve a medir el parquet. Las copias locales relevantes se leyeron y sus hashes quedaron registrados.

NO MEDIDO en este turno:

- Una nueva corrida LIF de los 16 relevos y la sensibilidad a otras parametrizaciones o simuladores.
- Generalización del predictor y comparación G1 contra G0 en datos reservados.
- Regeneración independiente de las poblaciones X de cierre y de los mapas de unidades heredados.
- Causalidad en animales, eficacia sináptica real y signos fisiológicos.
- Reproducción integral de los trabajos externos, geometría y prioridad bibliográfica sistemática.
- Una corrección de los documentos o sellos originales: se preservaron intactos.

Herramientas y máquina: lectura de GitHub, inspección de PRs y contexto, servicio del pizarrón, Python en brain-env, sandbox separado para adjuntos y contraste bibliográfico con dos revisores de sólo lectura. Se crearon instrumentos diagnósticos aislados, no código de producto. No se gastó cuota de Actions ni Kaggle, no se instaló software y no se lanzó trabajo prolongado.

Errores propios registrados: un alta de archivo falló inicialmente por directorio inexistente; se creó y se ejecutó correctamente. Un agregado preliminar consultó `real` donde el JSON usa `observed`; el instrumento definitivo lo corrige. El git nativo no tenía credencial de escritura: no publicó nada y se recuperó por la integración de GitHub. Un borrador de instrumento quedó sólo compilado y no se usa como evidencia. La revisión causal retiró objeciones excesivas sobre ratios, OR saturada y glutamato. La revisión final detectó que mi exploración `B009` no usa el sujeto completo de 009; retiré su atribución como evaluación del predictor, sin borrar la salida cruda.

## 10. Método y cierre

TITAN FULL, acción no delicada: altas documentales append-only, sin merge, borrado, despliegue, cambio de permisos ni reemplazo de trabajo ajeno. Roles efectivos: auditoría de repositorio, análisis cuantitativo, crítica de diseño, contraste externo, documentación y QA.

Gate aplicado:

- “Los números se reproducen” → lectura de cuentas y parquet mediante instrumento independiente → podía discrepar → PASS en las magnitudes y guardas indicadas.
- “El nulo conserva grados simples del subgrafo pesado BANC” → comparación de grados por muestra → podía fallar y falló en 3.403/10.000 muestras originales → FAIL de esa afirmación; control corregido ejecutado.
- “El predictor generaliza o identifica mecanismo biológico” → las siete combinaciones retrospectivas no pueden demostrarlo → NO MEDIDO.
- “El maestro transcribe correctamente el cierre” → reagregación del JSON archivado → podía discrepar y discrepó en las cuatro medias → FAIL documental.

Rúbrica final de un revisor de sólo lectura: **42/45 = 93,3/100**. Completitud 14/15 (cobertura y límites, fuentes y stdout); razonamiento 9/10 (control condicional, estimandos y corrección de mi exploración B009); documentación 10/10 (hashes y lectura de vuelta exacta); innovación 4/5 (controles ejecutados, extensión científica aún no probada); proceso QA 5/5 (revisión crítica con correcciones y caso negativo que detecta el fallo). **55 puntos N/A:** ejecutabilidad de producto, seguridad de producto, cobertura de una suite de producto y DevOps; esta entrega es un dictamen, no un despliegue. La nota no aprueba un producto ni un experimento futuro.

Archivos de la entrega: dictamen `docs/auditorias/2026-11-02-02-astra-topo-relevos-conservados-predictor-no-validado.md` y evidencia `docs/auditorias/evidencia/2026-11-02-03-astra-topo/evidencia-verbatim.md`. Por ser una auditoría independiente, el dictamen se publica en auditorías, no bajo la voz de BRAIN en respuestas. Su espejo de ClickUp vive directamente en Space.

Control de publicación de la evidencia: commit `1a9604393637e5cdad80bb33d1c3e1826a17ff8d`, 44.688 bytes, SHA-256 `c22ddf094d9eb2a99e285401185de4ddf924504b247cdc3472e1a4f3bfdb148b`. Las tres fuentes y los tres stdout extraídos del archivo publicado dieron igualdad exacta con sus originales. No se commitearon datasets grandes ni binarios derivados.

<details>
<summary>Fuentes externas leídas</summary>

- [Shiu et al., modelo de cerebro entero](https://www.nature.com/articles/s41586-024-07763-9).
- [Lappalainen et al., FlyVis](https://www.nature.com/articles/s41586-024-07939-3).
- [Shuvaev et al., genomic bottleneck](https://pmc.ncbi.nlm.nih.gov/articles/PMC11420173/).
- [Barabási y Barabási, modelo genético del conectoma](https://doi.org/10.1016/j.neuron.2019.10.031).
- [Pospisil et al., camino del conectoma al effectome](https://www.nature.com/articles/s41586-024-07982-0).
</details>

Espejo público en el Workspace: [2026-11-02 · Auditoría Astra: los 17 relevos se sostienen; el 7/7 no valida el mecanismo y 009 requiere enmienda](https://app.clickup.com/90171457413/docs/2kza6fw5-26317). Ruta: Space > este Doc.
