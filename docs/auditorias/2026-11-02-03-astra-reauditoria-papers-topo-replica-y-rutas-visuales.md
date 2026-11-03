# Reauditoría de Papers 1-3, Topo inverso, 008 y 009-A1

Fecha de trabajo: 2-nov-2026, ART (UTC-3). Revisión base de main: `871ebac94fe0b219d954f135625bbfba4c3cbdb8`. Encargo: «pues vuelve a auditar y ponte listo». Auditoría documental y verificación computacional de resultados archivados, no nuevas simulaciones neuronales. Operador: ClickUp Brain, modelo declarado por el entorno GPT-6 Astra.

## 1. Veredicto corregido

**La línea propia ya tiene evidencia funcional computacional en un banco sintético. No se reduce a encontrar motivos anatómicos.** La auditoría anterior omitió contrastar directamente los tres textos y por eso presentó una contextualización incompleta. La rectificación 011 deja ese error en la historia; este informe aporta la reauditoría y mediciones nuevas, sin reescribir la anterior.

- **CONFIRMADO:** el cotejo primario de H_LECTOR entre Actions y la réplica archivada en brain-env coincide en 6/6 JSON byte a byte y 120.000/120.000 predicciones. CERCA y PAGA se recuperan con el bootstrap sellado. Los nulos no se replicaron en esta comprobación.
- **CONFIRMADO, condicionado:** la ventaja media de MOSCA_L con pocos datos en H_PARES se reproduce desde los 12 JSON originales. **REFUTADA como afirmación universal:** no gana en toda celda ni en todo tamaño de entrenamiento.
- **REFUTADO:** el enunciado del Paper 3 «Vision has no shortcut to the motor neurons: it has to pass through descending neurons». Hay una ruta anatómica optic → visual_projection → motoneurona del cuello, incluso exigiendo al menos 5 sinapsis en ambos enlaces.
- **CONFIRMADO como ajuste retrospectivo:** el 7/7 y R²≈0,91 de 008. **NO MEDIDO:** su predicción causal fuera de los casos ya observados. Nuevos baselines separan mejor qué aporta ponderar las tasas de los destinos.
- **Se conserva el alcance del resultado anatómico previo:** 17 pares pesados compartidos, sostenidos frente al nulo condicional corregido. No convierte BANC en un holdout virgen ni demuestra transferencia funcional.
- **009-A1 sigue siendo un protocolo prospectivo, no un runner validado ni resultados nuevos.** Se preservaron 009, su sello, su generador y A1.

No se editaron manuscritos, protocolos, sellos ni código de producto; no se fusionó ningún PR ni se lanzaron las simulaciones pendientes.

## 2. Corpus exacto y procedencia

Se leyó directamente el corpus organizado en octubre:

1. **Paper 1 v2.0:** *Signal Propagation Properties in the Drosophila melanogaster Connectome: Intermodal Isolation, Differential Motor Access, and Non-Trivial Temporal Amplification*, junto con el erratum. Fuente de v2.0: `docs/v2/paper1-v2.0.md`; blob `5c590f1e82b0233adbe520f8860f220ead050df1`. Erratum: blob `ce57657757c27dbc6f38299f39354aba30e644ba`.
2. **Paper 2:** *The connectome as a blueprint: a sealed functional benchmark of the Drosophila looming-escape pathway across three scales and two flies*. `docs/paper2/paper2-esqueleto.md`, revisión `4652c8138c52333ae04b5ed91b026ee758385e5e`.
3. **Paper 3:** *Who drives the outputs of the fly brain? A null-controlled input map of descending, motor and neurosecretory neurons in FlyWire v783*. `docs/paper3/paper3-esqueleto.md`, revisión `c4c8549e67359cedda1943fb56e314a85ed901ef`.

Los dos últimos archivos se identifican como **SKELETON, not a draft for submission**. Son los textos sucesores disponibles en esas ramas, no artículos ya enviados. Se contrastaron con resultados posteriores de H_CONSENSO, H_RIVAL, H_LECTOR, H_TAU_LIBRE y H_PARES_DATOS, además de Topo, 008, el diseño 009 y A1.

El Paper 1 corregido figura publicado el 15-oct-2026, DOI `10.5281/zenodo.23393412`, como preprint, no artículo revisado por pares. En el turno inmediatamente anterior se verificó la API pública de Zenodo y la concordancia de los MD5 del manifiesto con las fuentes y los PDF declarados. No se descargaron y compararon de nuevo los PDF renderizados en esta reauditoría.

**Límite de identidad:** el antiguo «Paper 2» de agosto, *Topological Retention and Selective Convergence*, y el manuscrito embedded/DualBrain no se sustituyen silenciosamente por estos textos. Se leyeron sus índices históricos, no esos dos manuscritos completos. Este informe cubre el trío de octubre y su cadena experimental.

## 3. Qué cambia al integrar la línea propia

La pregunta ya venía evolucionando desde propiedades de propagación, pasando por acceso a salidas y un benchmark funcional, hasta un embudo de lectura y sus mecanismos. No corresponde vender esa evolución como una idea nueva de esta auditoría.

### 3.1 Resultados negativos que no se deben generalizar

- **H_RIVAL:** el lector W sin entrenamiento de pesos queda por debajo de ridge y MLP entrenados sobre las entradas crudas en el banco evaluado. W−ridge = −0,0503; W−MLP = −0,0479, según los resultados archivados revisados. Contra REGLA_TAU quedó SIN_DECIDIR. No significa «los métodos clásicos siempre ganan» ni «las trazas del conectoma no sirven».
- **H_CONSENSO:** el núcleo de conexiones fuertes pierde frente a R2 cuando lo lee W: Δ≈−0,0459. Es un fallo de suficiencia de ese núcleo bajo ese lector, no una prueba contra cualquier lector entrenado. El núcleo real todavía supera sus barajados estructurales en el contraste distinto H_CABLEADO_NUCLEO.
- Estos resultados se revisaron documentalmente en sus sellos, agregadores y registros. **No se reejecutaron sus simulaciones en este turno.**

### 3.2 Resultado positivo que sí merece el centro del relato

**MOSCA_L/WL utiliza 6 neuronas descendentes × 40 instantes = 240 rasgos, frente a 564 entradas × 40 instantes = 22.560 rasgos del lector crudo.** Es una interfaz de lectura 94 veces más estrecha. La red R2 que produce esas trazas sigue teniendo 33.489 neuronas y 4.031.897 aristas.

Por tanto, se sostiene una representación útil y una reducción de dimensionalidad de la interfaz en el banco modelado. **No se midieron 94 veces menos cómputo, latencia, RAM, energía ni costo total.** Confundir esos objetos arruinaría un resultado real por exagerarlo.

H_TAU_LIBRE, revisado como evidencia histórica, extiende el contraste frente a nulos a tau 20-29 no elegidos como el tau 10 inicial, en c2/c5 y el test 12. Eso limita la explicación de «sólo acertó por elegir tau 10» dentro de ese alcance; no prueba robustez universal.

## 4. H_LECTOR: cotejo pendiente ahora verificado

### Propiedad e instrumento

Se compararon los seis JSON de `results/lector_2026-10-15/` en `8d305e97d40ef89385317c3579bfc6d1090c57ca` contra los seis JSON ya existentes de la réplica en brain-env. Se comprobaron celdas, semillas 12-21, 2.000 predicciones por celda/semilla, metadatos, guardas y las tres series de aciertos almacenados. Se revisaron los logs de ambas ejecuciones.

El instrumento propio `verify_lector.py` no importa el agregador del autor. Recalcula los dos primarios con 20.000 remuestreos y PCG64, semilla 2041, remuestreando conjuntamente las diez semillas de prueba entre celdas.

| Contraste primario | Media | IC95% | Margen sellado | Resultado |
| --- | ---: | --- | ---: | --- |
| WL−RIDGE | −0,002875 | [−0,00378333; −0,00198333] | −0,01 | CERCA SOSTENIDA |
| WL−W | +0,04744167 | [+0,04540833; +0,04932500] | +0,01 | PAGA SOSTENIDA |

- **6/6 JSON idénticos byte a byte.** También coincide el objeto JSON completo, no sólo la etiqueta del veredicto.
- **120.000 predicciones coincidentes**, 6 celdas × 10 semillas × 2.000 ensayos.
- Diferencia numérica con el agregado publicado: **0** en medias y extremos de los dos intervalos.
- Los logs no son iguales: registran el runner de Actions con Python 3.12.15 y brain-env con Python 3.12.14, ambos NumPy 2.5.3, además de duraciones distintas y salida 0. Se conservan completos o por referencia Git inmutable verificada.

### ¿El cotejador podía detectar una discrepancia?

Sí. La misma comparación que pasa sobre los datos válidos rechaza cuatro mutantes locales: un carácter de predicción, una semilla ausente, un acierto alterado y una guarda PIN falsa. Un fixture analítico del agregador sostiene los dos márgenes; al degradar únicamente WL, ambos quedan REFUTADOS. Se conserva el cambio y la salida de cada control.

**Alcance del cierre:** comparación nueva de dos ejecuciones históricas, no una nueva simulación. No se recalcularon los aciertos desde etiquetas originales. Los nulos de H_LECTOR_CABLEADO siguen siendo de Actions solamente. La igualdad entre ejecuciones del mismo productor no equivale a una implementación neuronal independiente.

## 5. H_PARES: resultado medio confirmado, universalidad descartada

`verify_pares.py` reconstruyó las matrices desde los 12 JSON en `e5db87062e6dfeb1a370e53c11926660f1dc0bc8`, sin importar el agregador del autor. Rehizo los seis estadísticos D/E y sus intervalos con 20.000 remuestreos, PCG64 semilla 2063, preservando el orden de remuestreo de subconjuntos, tau y proyecciones.

La discrepancia máxima con lo publicado fue **3,47×10⁻¹⁶**, redondeo de coma flotante.

| Ventaja media de MOSCA_L, n=6 a 768 | Diferencia de acierto | IC95% |
| --- | ---: | --- |
| frente a CRUDO | +0,040096875 | [+0,02871999; +0,05079000] |
| frente a PCA_L | +0,152000000 | [+0,14250431; +0,16155867] |
| frente a PROY_L | +0,0903565625 | [+0,08064937; +0,09997268] |

Esto resume ocho tamaños de entrenamiento y dos celdas. No significa una victoria en cada punto:

- En **c2, n=96**, CRUDO=0,9347 supera a MOSCA_L=0,92979 y también a W=0,92765. CRUDO sigue por encima de MOSCA_L en los tamaños evaluados 192, 384, 768 y 2.400.
- En **c2, n=768**, PCA_L=0,992975 supera a MOSCA_L=0,9897075; también lo supera en n=2.400.
- En **c5, n=96**, MOSCA_L=0,9214575 frente a CRUDO=0,838625. La diferencia entre celdas importa, no se debe ocultar detrás del promedio.
- La afirmación histórica sobre no alcanzar a W en n=96 corresponde al **promedio de c2/c5**, no a cada celda por separado.

Los veinte subconjuntos son anidados y salen de un único pool fijo de 2.400 ensayos. El test es el mismo conjunto de 2.000 ensayos, semilla 12. Los IC remuestrean índices de subconjuntos, tau y proyecciones; **son condicionales al pool y al test, no intervalos sobre nuevos animales, nuevas tareas o nuevas poblaciones de prueba**.

Controles propios: fixture constante con estadísticos analíticos; degradación del único brazo MOSCA_L; rechazo de una tau ausente y una guarda falsa. No se entrenó ni simuló nada nuevo.

## 6. Paper 3: contraejemplo anatómico a la obligación de pasar por DN

### Afirmación exacta

§3.5: **“Vision has no shortcut to the motor neurons: it has to pass through descending neurons.”**

La ausencia de un enlace directo no prueba la identidad de todos los intermediarios. Ahora el chequeo no se limita a señalar esa inferencia: encontró un contraejemplo en los mismos datos del productor.

### Datos y equivalencia con el cálculo original

Se recorrieron las 15.091.983 filas de conectividad. MD5 del grafo: `3d802fd542b5d18570ba1ba0bb0abed9`; MD5 de anotaciones: `719904abad876c68ace1b5690c9b9b63`, coincidentes con el productor `output_control_by_class.py` de `95e8d6c47cd4eea5cd20432d3fab6146e5d31ed2`.

Se usó su definición de clases por `super_class` y su D2 sin signo: suma de productos de fracciones de entrada en dos saltos, promediada sobre motoneuronas con entrada positiva. Se separó la contribución por clase del intermediario, sin importar el código del productor.

| Umbral por arista | D1 optic→motor | D2 optic→motor | Parte de ese D2 vía no-DN |
| --- | ---: | ---: | ---: |
| ≥1 sinapsis | 0,001689355% | 0,371296648% | 98,755% aproximadamente |
| ≥5 sinapsis | 0% exacto | 0,269285028% | 99,505% aproximadamente |

Los D2 reproducen el 0,37% y 0,27% redondeados de los logs originales. En el primer umbral hay seis aristas directas de una sinapsis; su pequeño D1 se imprime como 0,00%. **0,00% no era cero exacto.** En ≥5 quedan 109 de las 110 motoneuronas con entrada; ése es el denominador usado, como en el productor.

### Testigo que sobrevive ≥5 en ambos enlaces

**LPi14 → H2 → CB0705, motoneurona del cuello.**

- LPi14: `root_id=720575940627190556`, `super_class=optic`.
- H2: `root_id=720575940632427603`, `super_class=visual_projection`, **no descending**.
- CB0705: `root_id=720575940622008560`, `super_class=motor`, `cell_sub_class=neck_motor_neuron`.
- LPi14→H2: **1.121 sinapsis**.
- H2→CB0705: **10 sinapsis**.

Las dos filas se recuperaron además mediante un filtro directo de PyArrow, separado de la agregación D2. El primer enlace tiene signo inhibitorio en los datos del modelo y el segundo excitatorio. **Se prueba un camino anatómico, no que LPi14 active a la motoneurona.**

### Qué refuta y qué conserva

- **Refuta la universalidad anatómica** de «tiene que pasar por neuronas descendentes» para las motoneuronas cerebrales estudiadas.
- No refuta el cero directo a umbral ≥5, ni convierte ese D2 pequeño en control conductual importante.
- No dice nada equivalente sobre todas las motoneuronas del VNC, locomoción o músculos de las patas.
- No invalida por sí mismo los otros contrastes del Paper 3 con nulos de tamaño/región y corrección múltiple.
- No se reclama descubrir una ruta desconocida para la neurobiología: es un contraejemplo a una frase de este manuscrito.

**Redacción sugerida, no aplicada:** «El acceso optic→motor directo es nulo con umbral ≥5. Existen rutas anatómicas de dos saltos hacia motoneuronas cerebrales, incluidas rutas con intermediarios visual_projection no descendentes; este análisis no mide su eficacia funcional».

### Controles y errores propios conservados

Un grafo manual tiene D2=0,375 y un intermediario descending. Al cambiar sólo su clase a central, D2 sigue siendo 0,375 y la misma aserción de paso universal por DN falla. El filtro directo del testigo también se probó contra una copia que reclasifica H2 como descending.

Hubo dos falsos rojos del instrumento, no del producto: v1 rechazaba los 14 índices sin anotación, que el productor conserva; v2 comparaba 0,00% publicado con cero exacto. Se preservan fuentes y salidas completas de ambos intentos. v3 conserva la categoría sin anotación y compara el redondeo correctamente; el contraejemplo no cambia.

## 7. Paper 1 y Paper 2: correcciones de lectura y de énfasis

### Paper 1 corregido

La v2.0 ya distingue señal con signo, propagación multisalto, acceso condicionado por neuropilo y límites de amplificación. **Su §4.4 y Tabla 11 ya posicionan la contribución frente a trabajos anteriores.** No correspondía presentar esa diferenciación como innovación aportada ahora por un auditor externo.

Queda una tensión de redacción: §6 llama «Central finding» a que la modularidad produce separación y el cableado fino produce persistencia. El mismo documento declara Tabla 8 no reproducida desde el código archivado, N=5 para el nulo CP y el hecho de que Linear también amplifica mientras LIF-soft no. El abstract sí contiene la salvedad; acusarlo de ocultarla sería falso.

**Dictamen acotado:** no se verificó aquí la atribución causal fuerte de esa frase. Conviene alinear la conclusión con el resultado provisional y condicionado al modelo que el propio texto ya reconoce. No se reejecutó Tabla 8, ni se declara refutado todo el Paper 1.

### Paper 2 sucesor

El esqueleto no incorpora todavía toda la cadena posterior; conserva pendientes históricos de H_CONSENSO/H_TAU. No deben confundirse con el estado actual de los experimentos. Su relato actualizado tendría que separar:

1. W no supera a ridge/MLP en la comparación sellada.
2. Un lector entrenado sobre las trazas del embudo sí recupera un desempeño cercano con 240 rasgos.
3. La ventaja de pocos datos es media y condicionada, con cruces de curvas explícitos.
4. La conservación anatómica entre moscas no equivale a transferencia funcional de ese lector.

No se modificó ese esqueleto. Tampoco se considera error el 76 frente a 73 del Paper 3: hay 76 neuronas endocrine en la población, 73 con entrada sin umbral y 69 con entrada a ≥5. El filtro por entrada positiva explica esos denominadores.

## 8. Topo, 008 y los 17 relevos: qué se sostiene ahora

La auditoría anterior verificó las cuentas archivadas del mecanismo DNp04→PVLP010 en el modelo y la conservación de 17 pares D→X pesados entre FlyWire y BANC. Esos resultados no desaparecen por el error de alcance documental. Tampoco se elevan a biología demostrada por incorporarlos a esta narrativa.

### Baselines nuevos sobre los siete casos de 008

Se fijaron cuatro comparadores antes de esta reagrupación, sin ajustar parámetros: repartir por igual entre hubs; promediar la cuota sináptica de cada hub entre todos los destinos; promediar sólo los destinos con tasa positiva; usar la ponderación por tasa de 008.

| Predictor | R² | MAE | Casos con error ≤0,15 |
| --- | ---: | ---: | ---: |
| Reparto igual entre hubs | −1,2214 | 0,26842 | 2/7 |
| Cuotas, destinos uniformes | 0,7977 | 0,08070 | 5/7 |
| Cuotas, destinos activos uniformes | 0,8623 | 0,07187 | 6/7 |
| 008, ponderado por tasa | 0,9065 | 0,06084 | 7/7 |

**008 mejora descriptivamente a estos comparadores en esos datos.** El baseline de destinos activos ya logra 6/7; el incremento hasta 7/7 no basta para demostrar que el detalle de las tasas identifica el mecanismo fuera de muestra. Los baselines de cuotas todavía usan tasas de hubs y pesos sinápticos: no son baselines puramente anatómicos.

Es una comparación exploratoria posterior a observar los siete resultados, que comparten tres estímulos y neuronas. No es validación reservada. Se usaron las cuotas y efectos extraídos en la primera auditoría, no una nueva corrida neuronal. El instrumento excluye expresamente los campos B009 exploratorios que fueron retirados como evaluación de la fórmula literal 009.

El nulo previo que permuta conjuntamente destinos dentro de cada estímulo dio p≈0,1397. Eso no rechaza ese nulo a 0,05; tampoco prueba que las tasas no aporten nada. El contraste global p≈0,00139 responde una pregunta distinta y no reemplaza al nulo condicionado por estímulo.

### Conservación anatómica

Se mantiene, como medición de la auditoría anterior no repetida aquí, el resultado de 17 pares pesados compartidos (entre 37 candidatos FlyWire y 31 BANC) y su contraste con el nulo simple corregido: 10.000 aceptados, cero solapamientos ≥17, p_MC=1/10.001. Es un nulo condicionado al subgrafo bipartito pesado de BANC con FlyWire fijo, no un barajado ponderado y geométrico del conectoma entero.

BANC ya participó en descubrimiento/selección. Sus correspondencias de tipos también se apoyan en procedimientos anatómicos y de conectividad. **No se puede denominar holdout intacto ni concluir circularidad total sólo por eso.** Falta medir transferencia funcional y sensibilidad a la definición de correspondencias.

## 9. Contraste externo sin borrar la contribución propia

- **Braun et al., 2024:** redes de neuronas descendentes que reclutan poblaciones y relaciones inhibitorias entre grupos ya forman parte de la literatura. «Hay recurrencia y reclutamiento entre DN» no es por sí solo una novedad.
- **Bates et al., BANC 2026:** controles distribuidos/locales y análisis de influencia ya están tratados; el emparejamiento de tipos utiliza morfología y conectividad. Eso obliga a delimitar independencia y selección, no a decir que el trabajo propio no aporta nada.
- El incremento defendible de esta línea sería la relación entre **anatomía, representación de lectura y respuestas a intervenciones específicas**, con condiciones de estado y pruebas reservadas. Los papers propios ya suministran parte de esa cadena.

Se revisaron las secciones accesibles del texto principal de esos dos trabajos, no todos sus Methods ni todos sus suplementos. No se emite un dictamen de prioridad mundial. El posicionamiento ya escrito en Paper 1 §4.4/Tabla 11 forma parte de la base, no una idea atribuible a esta auditoría.

## 10. 009-A1: válido como diseño acotado, no como resultado

La relectura no convierte su anterior 45/45 documental en evidencia experimental. A1 fija poblaciones D′, máscaras selectivas, entradas pareadas explícitas, familias de pruebas, reglas para denominadores no positivos y un banco C artificial. Separa OR/AND compatible en C de función natural y retira la fórmula no calibrada de 009 como primaria.

**NO MEDIDO:** runner, reproducción del replay, potencia con n=20, costo/duración, robustez paramétrica, efectos nuevos de los otros 16 relevos, transferencia de función a BANC y eficacia biológica.

Las guardas estructurales previas prueban qué filas se cortarían, no qué efecto produciría cortarlas. Tampoco retirar transmisión saliente equivale a silenciar la generación interna de espigas. La entrada Poisson no es un clamp de salida.

### Mejora siguiente propuesta, no ejecutada

1. **Antes de una corrida grande:** implementar y verificar el runner contra fixtures pequeños, SHAM, signos, conservación de poblaciones, eventos pareados y replay. Publicar sus pruebas positivas y falsadores; recién después evaluar una corrida autorizada.
2. **Predicción causal reservada:** separar descubrimiento, selección de correspondencias y evaluación; reservar familias de tipos/condiciones antes de ver sus cortes. Comparar el predictor con cuotas uniformes, destinos activos y baselines de grado/peso. No llamar reservado a volver a usar los siete casos de 008.
3. **Composición, no cambio de nombre:** una gramática debería anticipar la respuesta de combinaciones reservadas de relevos a partir de componentes, frente a una predicción aditiva y controles de interacción. Los cortes de A1 son piezas para esa prueba, no la gramática ya encontrada.
4. **Contabilidad separada:** informar neuronas/aristas simuladas, rasgos del lector, datos etiquetados, entrenamiento, inferencia, memoria y energía. No convertir 240 rasgos en ahorro total sin medirlo.

La prioridad es cerrar una predicción intervenida y reservada, no bautizar otro «lenguaje» sobre un ajuste retrospectivo.

## 11. Instrumentos, custodia y gates

Máquina de ejecución: brain-env `6c09d8604b07`, Python 3.12.14, NumPy 2.5.3, dos CPU. Se midieron RAM y disco al inicio; se trabajó en una carpeta de auditoría aislada, por lotes para el grafo. No se encendió GPU, VM ni Actions. Los procesos propios finalizaron; stdout/stderr y códigos de salida quedaron en archivos.

| Instrumento ejecutado | SHA256 de fuente | Estado de su versión final |
| --- | --- | --- |
| verify_lector.py | de6d0cecf97be9b1dc7ff33cf10c8ffb382e93aa70838616403831ac1300b18f | PASA |
| verify_pares.py | aa48e513ef74d4afa57bf66e45f57a9e4f434f13a3e8324db5ed794d6c2b4300 | PASA |
| verify_motor_paths.py v3 | 883cca69629adf7aa3cda89c0251b45d2add2e22a3dd249f1805473cb393851d | PASA |
| verify_predictor_baselines.py | 1e5b20b36bad07f51ac02f086ca8430ce5932bc4a87e88abe36f07e7bcb45f23 | PASA, exploratorio |
| verify_direct_witness.py | fb5a27d2d98b9d1211deb35e8900551101bee97fba6e38e0f9ed9408cf3bb6d7 | PASA |

**Gate I, instrumento:** PASA en las versiones finales para las propiedades acotadas. Se conservan los fallos propios v1/v2, no se transforman en fallos del producto ni se ocultan en un promedio. Los agregadores nuevos no importan los del autor. Sus remuestreos replican el contrato estadístico; eso es verificación aritmética, no un nuevo diseño experimental independiente.

**Gate II, informe:** revisión completada con sujetos, estados, límites y correcciones de falsos positivos. Dos revisores asistidos aportaron lectura de manuscritos/productores; no ejecutaron estas mediciones ni constituyen una réplica biológica o dos instrumentos independientes adicionales. Se retiraron sus propuestas erróneas sobre la salvedad del abstract, el estado actual de H_TAU y el denominador 76/73.

**Gate III, entrega:** el cierre de publicación y lectura remota se añade al final después de verificar Git y el Doc. No se usa una nota numérica para certificar el programa de investigación.

Evidencia íntegra: [bloque 2 y referencias](https://github.com/gatehot59-star/drosophila-fep-connectome/blob/main/docs/auditorias/evidencia/2026-11-02-03-reauditoria-papers/evidencia-parte2.b64), combinado con el bloque 1 del apéndice técnico de este informe. Contiene fuentes ejecutadas, salidas completas, versiones fallidas, controles, procedencia y referencias inmutables de inputs. El empaquetado es reversible y verifica longitud/SHA256. Los JSON canónicos ya publicados y los logs de Actions no se duplican innecesariamente: se referencian por SHA, URL inmutable y hash; los seis JSON de la réplica usan aliases byte-idénticos comprobados. Los logs locales de la réplica sí quedan incluidos. No se capturaron credenciales ni variables secretas.

### Protegidos, verificados antes de publicar

- Diseño 009: SHA256 `61ab66b7839bc38f1ad6caaee43e60e7f0524fddb3e37ff58ff49acb5c48f1ea`, 30.215 bytes.
- Sello JSON: `210b581792d183517d1e4e7771b8435e4a6acb537bc1ad383e5725c500073e93`, 31.673 bytes.
- Generador original: `f60624380e6344f21be5cc8608ba6ea913bf1971687c2d683eb91b3f845b2f62`, 4.455 bytes.
- Enmienda A1: `e10b7756ecf5e1bfebdf285e3e37c1af901256327d3e08f0a4abbc8551611127`, 34.776 bytes.

## 12. Qué no se midió que importaba

No se ejecutaron nuevos ensayos neuronales, ni nuevos entrenamientos. No se cerró la reproducción de Tabla 8 del Paper 1, la exactitud de aciertos contra etiquetas originales, los nulos de H_LECTOR en una segunda ejecución, un test nuevo de H_PARES, la evaluación funcional en otra mosca, la gramática composicional, el costo total, la potencia y robustez de A1 ni ninguna validación conductual/biológica. No se revisó exhaustivamente toda la literatura ni los manuscritos históricos de agosto.

Esas ausencias no anulan la representación útil medida ni el contraejemplo anatómico. Sí limitan qué se puede prometer con ellos.

## 13. Fuentes principales

- [Paper 1 v2.0, fuente fijada](https://github.com/gatehot59-star/drosophila-fep-connectome/blob/871ebac94fe0b219d954f135625bbfba4c3cbdb8/docs/v2/paper1-v2.0.md).
- [Erratum, fuente fijada](https://github.com/gatehot59-star/drosophila-fep-connectome/blob/871ebac94fe0b219d954f135625bbfba4c3cbdb8/docs/ERRATUM.md).
- [Publicación v2.0 en Zenodo](https://zenodo.org/record/23393412).
- [Paper 2, esqueleto exacto](https://github.com/gatehot59-star/drosophila-fep-connectome/blob/4652c8138c52333ae04b5ed91b026ee758385e5e/docs/paper2/paper2-esqueleto.md).
- [Paper 3, esqueleto exacto](https://github.com/gatehot59-star/drosophila-fep-connectome/blob/c4c8549e67359cedda1943fb56e314a85ed901ef/docs/paper3/paper3-esqueleto.md).
- [H_LECTOR, agregado original](https://github.com/gatehot59-star/drosophila-fep-connectome/blob/8d305e97d40ef89385317c3579bfc6d1090c57ca/results/lector_2026-10-15/agregado.json).
- [H_PARES_DATOS, agregado original](https://github.com/gatehot59-star/drosophila-fep-connectome/blob/e5db87062e6dfeb1a370e53c11926660f1dc0bc8/results/pares_datos_2026-10-18/agregado.json).
- [Productor del mapa de salidas, PR26](https://github.com/gatehot59-star/drosophila-fep-connectome/blob/95e8d6c47cd4eea5cd20432d3fab6146e5d31ed2/tools/output_control_by_class.py).
- [Enmienda 009-A1, revisión auditada](https://github.com/gatehot59-star/drosophila-fep-connectome/blob/871ebac94fe0b219d954f135625bbfba4c3cbdb8/docs/agents/respuestas/2026-11-02-010-enmienda-009-a1-sello-original-intacto.md).
- [Auditoría inicial de Topo, antecedente acotado](https://github.com/gatehot59-star/drosophila-fep-connectome/blob/main/docs/auditorias/2026-11-02-02-astra-topo-relevos-conservados-predictor-no-validado.md).
- [Rectificación de alcance 011](https://github.com/gatehot59-star/drosophila-fep-connectome/blob/main/docs/agents/respuestas/2026-11-02-011-rectificacion-alcance-lectura-papers-propios.md).
- [Braun et al., 2024](https://www.nature.com/articles/s41586-024-07523-9).
- [Bates et al., BANC 2026](https://www.nature.com/articles/s41586-026-10735-w).

## 14. Apéndice técnico: evidencia reversible, bloque 1 de 2

El bloque 2 está en el archivo hermano citado en §11, commit `6f6109e9868f4b60fa47bb7a2572a7988097ee5b`. No es un segundo experimento. Se concatenan los caracteres Base64 del bloque 1 (16.000) y del bloque 2 (37.256), se decodifica Base64 y luego Brotli. El resultado es JSON UTF-8 con 43 archivos íntegros y 33 referencias Git inmutables. Los hashes de los archivos referenciados también están incluidos. El mapa `files` conserva los bytes UTF-8 de cada fuente y captura; `immutable_references` permite reconstruir los inputs externos verificando tamaño y SHA256.

- Brotli: 39.941 bytes; SHA256 `340b79b0bd49b4ccfee340a000dbccf78dddabe34aec8d1472e7614410066232`.
- JSON reconstruido: 802.987 bytes; SHA256 `08a49331f7e29841d5ada986ef3e47a4c5f84dd2d11e6e79a689670f4181b35b`.
- Archivo bloque 2, incluido LF final: 37.257 bytes; SHA256 `60db6fd390afc9711946baf3ad9555bf144f29e43ca126d512605607206cfa9d`.
- El bloque 1, incluido un LF final al extraerlo, tiene SHA256 `fab507a3c4bcf7c540a8c99fe0024c9146f3417e1f0e49a2449e480debce8b17`.

La reconstrucción se ejecutó antes de publicar. Tras publicar se repite contra ambos archivos remotos. No se publican binarios derivados, credenciales ni variables secretas.

<details><summary>Bloque 1, Base64 de evidencia comprimida</summary>

<!-- EVIDENCE-PART-1 -->
```text
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
```
<!-- /EVIDENCE-PART-1 -->
</details>
