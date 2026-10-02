# Auditoría por hipótesis del conectoma

## Pedido

Auditar el trabajo anterior por hipótesis, no por archivos, usando criterio de falsación: cada hipótesis debe tener predicción, falsador, control, resultado y límites.

## Veredicto ejecutivo

La línea no queda descartada. Queda partida en capas: la hipótesis de que la topología impone ruteo tiene evidencia fuerte; la hipótesis de que el 96% puede quedar fijo queda refutada como analogía funcional; la hipótesis de activación y desactivación según acción todavía no fue testeada sobre el conectoma adulto; y la amplificación temporal con signo es prometedora, pero no debe venderse como dos propiedades independientes hasta separar sus métricas.

## H1 · El cableado por sí solo impone aislamiento y ruteo diferencial

**Predicción:** con dinámica fija, signos y pesos observados, las clases sensoriales muestran acceso diferencial a regiones motoras y al centro de aprendizaje; un null que preserve grados y destruya la identidad de las aristas elimina el patrón.

**Resultado:** sostenida para el ruteo medido. Los 40 nulls con grado entrante y saliente exacto dieron 0/40 en las cuatro clases de acceso diferencial. El centro de aprendizaje mostró cero conexiones sensoriales directas a KC mientras los nulls producían entre 1.533 y 2.640. [40 nulls](https://app.clickup.com/90171457413/docs/2kza6fw5-3957/2kza6fw5-5937)

**Límite:** demuestra ruteo en el grafo y poblaciones elegidas, no que la topología explique por sí sola la conducta. El acceso motor medido era a motoras/descendentes cerebrales, no a músculo periférico.

**Falsador pendiente:** umbral de ≥5 conexiones, null anatómico por neuropilos y tarea conductual independiente.

**Veredicto:** **sostenida, acotada a ruteo estructural**.

## H2 · La plasticidad es mínima y está encerrada por la topología

**Predicción:** el circuito plástico es pequeño, sus entradas y salidas están restringidas y los nulls pareados por grado destruyen ese patrón.

**Resultado:** sostenida en la capa estructural. KC→MBON, DAN→KC, KC→KC y DAN→MBON aparecen enriquecidos frente a 40 nulls; las entradas sensoriales directas a KC son cero y MBON→motor está depletado. [Resultado estructural](https://app.clickup.com/90171457413/docs/2kza6fw5-3957/2kza6fw5-5937)

**Límite:** “la plasticidad ocupa poco cableado” no equivale a “el cerebro necesita poco entrenamiento”. El primero es estructural; el segundo requiere ablación de aprendizaje en tareas reales.

**Veredicto:** **sostenida como arquitectura de plasticidad; no prueba todavía entrenamiento mínimo**.

## H3 · El 96% del sistema puede quedar fijo sin perder función

**Predicción:** una vía reactiva congelada desde el cableado real alcanza al sistema entrenable en al menos 3/4 tareas; una máscara shuffle con igual grado rinde peor.

**Resultado:** refutada. El experimento corregido W/S probó el sujeto correcto: el conectoma congelado ganó al ruido congelado en 0/4, y W y S fueron indistinguibles en 3/4. [Tres brazos](https://app.clickup.com/90171457413/docs/2kza6fw5-4157/2kza6fw5-6137) · [W/S](https://app.clickup.com/90171457413/docs/2kza6fw5-4317/2kza6fw5-6297)

**Qué sobrevive:** la arquitectura de dos vías y el gate pueden ser útiles; no sobrevive que la máscara biológica congelada aporte ventaja funcional demostrada frente a un grafo disperso pareado.

**Veredicto:** **refutada; retirar la analogía del 96% fijo**.

## H4 · El cerebro activa y desactiva rutas según la acción

**Predicción:** al cambiar acción o contexto con conectoma fijo, cambian de forma reproducible las rutas activas, la ganancia o la participación de módulos; silenciar el módulo activado cambia la salida correspondiente.

**Resultado:** no medido en el conectoma adulto. El gate DBC3 fue medido en tareas sintéticas; eso demuestra utilidad del gate en el controlador, no que la mosca use ese mecanismo.

**Falsador correcto:** cuatro acciones sensoriomotoras, mismas entradas salvo contexto, actividad por módulo/neuropilo, silenciados cruzados y null de rutas.

**Veredicto:** **NO MEDIDA**.

## H5 · La dinámica con signo amplifica después de terminar el estímulo

**Predicción:** la separación o RDI post-estímulo supera la del periodo de estímulo en el real y no en nulls, con suficientes controles y sin reutilizar el mismo estadístico para otra propiedad.

**Resultado:** señal fuerte pero mal empaquetada en el paper. El cruce temporal se replica: durante el estímulo el real puede quedar por debajo del null y después invertir el signo. La auditoría detectó que las Propiedades 1 y 3 compartían la misma celda temporal, por lo que no son dos demostraciones independientes. [Auditoría del paper](https://app.clickup.com/90171457413/docs/2kza6fw5-3097/2kza6fw5-5077)

**Falsador pendiente:** curva completa con instrumento común, nulls temporales suficientes y separación formal entre aislamiento y amplificación.

**Veredicto:** **prometedora y parcialmente sostenida; claim independiente aún no cerrado**.

## H6 · La reciprocidad es cableado específico, no solo distribución de grados

**Predicción:** conservar in-degree y out-degree exactos debe producir reciprocidad comparable si el efecto es solo grado.

**Resultado:** sostenida contra el null de grado: 4.014.518 aristas recíprocas reales frente a ~84.932 en los nulls; 0/40 superan al real. [40 nulls](https://app.clickup.com/90171457413/docs/2kza6fw5-3957/2kza6fw5-5937)

**Límite:** no es correcto llamarla distintiva de la mosca entre especies; el claim propio es excedencia frente al null pareado y distribución por circuitos.

**Veredicto:** **sostenida contra grado; no distintiva a escala comparativa**.

## H7 · Los signos y la Ley de Dale son funcionalmente necesarios

**Predicción:** conservar o destruir signos cambia propagación, cancelación y separación temporal; una versión unsigned o con signos permutados pierde la señal.

**Resultado:** la Ley de Dale estructural está establecida: cero neuronas mixtas entre 138.005 con salidas. La dinámica con signo muestra cruces temporales. Falta un A/B aislado de signos conservados versus destruidos con la misma tarea, readout y múltiples semillas.

**Veredicto:** **estructura sostenida; causalidad funcional de los signos NO MEDIDA de forma aislada**.

## H8 · La dinámica SparseLTC compleja agrega valor sobre la real

**Predicción:** en una tarea donde fase o acoplamiento IQ sea necesario, la versión compleja supera a la real y a una dinámica continua equivalente.

**Resultado:** no sostenida en la tarea disponible: FlyVis-like real 72,22%, SparseLTC real 66,67%, SparseLTC complejo 47,22%. Eso refuta superioridad general en esa tarea, no utilidad futura en tareas de fase. [Benchmark](https://app.clickup.com/90171457413/docs/2kza6fw5-16997/2kza6fw5-19577)

**Veredicto:** **refutada como claim general; experimental como arquitectura de producto**.

## H9 · La topología puede traducirse directamente en un producto embebido

**Predicción:** loader, dinámica, extracción temporal y readout cierran en una cadena reproducible con tamaño, latencia y memoria medidos en hardware o emulación válida.

**Resultado:** parcial. Dataset, checksums, loader y piezas del runtime están verificadas; el puente SparseLTC→DBC3 está diseñado. El sistema completo con tarea real y readout reproducible todavía no está medido en hardware embebido.

**Veredicto:** **arquitectura plausible; producto NO MEDIDO**.

## Conclusión editorial

El descubrimiento más sólido no es “la mosca casi no entrena”. Es más preciso: **el conectoma impone prohibiciones y rutas selectivas, y encierra físicamente el módulo plástico**. La hipótesis de entrenamiento mínimo debe reformularse como pregunta experimental. El siguiente falsador que más cambia el estado del proyecto es H4/H7: acciones y signos, con rutas activas, silenciados, curvas temporales y controles que puedan dar rojo.

## Evidencia y límites

La auditoría se apoyó en el expediente histórico de hipótesis y resultados, los 40 nulls, los tres brazos, W/S y el benchmark matched. No lanzó nuevos kernels ni modificó datos. Quedan NO MEDIDOS: activación por acción, causalidad aislada de signos, null anatómico, tarea conductual completa y hardware end-to-end.

--- METODO TITAN ---
Accion delicada: NO
Modo aplicado: TITAN FULL
Rubrica: N/A (informe de auditoría por hipótesis; evidencia citada)
Review externo: no pedido
Instrumento: lectura cruzada del expediente ClickUp, resultados históricos Kaggle y estado documentado de Git; sin lanzar nuevos kernels en este turno
NO MEDIDO: activación por acción, causalidad aislada de signos, hardware end-to-end, null anatómico y tarea conductual completa.
