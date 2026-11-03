# 2026-11-03-002 · Apuesta de producto: verificación de resultados de conectoma por entrega

Fecha: 3-nov-2026, ART. Pedido: «Traducí esto en una apuesta de producto realista».

## Decisión

Arrancaría con un servicio de alcance y precio fijos: verificar una afirmación cuantitativa de un modelo de conectoma, antes de que un laboratorio apoye un paper o una inversión de cómputo en ella. El primer producto es un paquete de evidencia reproducible, no otro simulador, un visor ni un cerebro artificial.

Propuesta de valor: «Traé un resultado y sus datos. Te entregamos qué se reproduce, si la comparación es justa, qué conclusiones soporta y qué falta medir, con archivos que tu equipo puede volver a ejecutar».

Es una hipótesis comercial. No hay compradores, pedidos, disposición a pagar ni ahorro de tiempo validados en este trabajo. No se ofrece una certificación científica ni un resultado favorable garantizado.

## Cliente inicial, dolor y momento de compra

- Usuario: investigador que ya analiza circuitos derivados de conectomas de Drosophila y tiene resultados en archivos accesibles.
- Pagador a probar: responsable de un laboratorio de neurociencia computacional con presupuesto para apoyo técnico externo. No estudiantes sin presupuesto ni compradores de robótica general como primer mercado.
- Momento: antes de enviar un paper, responder una revisión o dedicar más recursos a una supuesta ventaja del modelo.
- Dolor supuesto: un resultado que parece sólido puede depender de una comparación injusta, una transcripción, un instrumento que no detecta errores o una interpretación más amplia que los datos.
- Sustituto real: que el laboratorio lo verifique internamente o use herramientas abiertas. No hay exclusividad sobre el método. El cliente pagaría por trabajo acotado, trazabilidad y una decisión clara, si percibe que le conviene tercerizarlo.

El nicho es estrecho y la compra institucional puede ser lenta. Esto es una primera vía plausible de monetización de esta línea, no una promesa de caja rápida ni una estimación del mercado total.

## Oferta piloto propuesta

Precio a probar: **USD 1.000 por entrega**, 50% al aceptar el alcance y 50% contra la entrega pactada. Es un precio experimental, no un precio de mercado observado. Plazo propuesto: 7 días hábiles desde que los datos compatibles estén completos y el alcance aceptado. Ese plazo aún no se midió con clientes.

Entrada aceptada:

- Una pregunta cuantitativa concreta y una revisión fija de código/datos.
- Un circuito o modelo compatible con las herramientas actuales.
- Resultados brutos de una tarea y un comparador ya disponibles; definición de las métricas, semillas y particiones necesarias para interpretarlos.
- Permiso para acceder a los datos y condiciones de uso verificadas. Si faltan datos esenciales, se acuerda explícitamente un alcance menor o no se acepta el encargo.

Entrega cerrada:

1. Recomputación de la métrica acordada desde los datos disponibles, con identificación exacta de versiones y exclusiones. No se afirma haber recomputado etiquetas o simulaciones si no se hizo.
2. Un comparador simple pertinente y controles acordados. Si requiere producir resultados o implementar un modelo nuevo, queda fuera del piloto.
3. Un verificador que pase un caso conocido y falle ante una corrupción relevante, sin usar el propio veredicto del productor como oráculo.
4. Un repositorio o paquete privado con instrucciones, archivos de evidencia, salida íntegra y una devolución breve: SOSTENIDO EN ESTE ALCANCE, REFUTADO EN ESTE ALCANCE o NO EVALUABLE, más el siguiente experimento recomendado.

Se cobra por la verificación, aunque el resultado sea negativo. La aceptación comercial es que se entreguen los controles, archivos y respuesta acordados; nunca que el modelo del cliente gane. No se vende independencia biológica, revisión por pares ni ausencia garantizada de todos los errores.

## Qué tenemos y qué falta para venderlo

Tenemos experiencia y verificadores ejecutados sobre datos propios: reagrupación de resultados, cotejo de réplicas almacenadas, controles negativos, contraste con alternativas simples y evidencia fijada en Git. La reauditoría identificó tanto resultados útiles como errores reales. Eso sirve como caso demostrable, no como validación de un servicio externo.

Falta empaquetar una demostración reejecutable, definir un formato de entrada y probar el costo de adaptar un caso ajeno. La portabilidad de los scripts a clientes no está demostrada. El primer alcance debe aceptar únicamente casos compatibles, no prometer «cualquier red».

009-A1 no necesita estar ejecutado para ofrecer verificación de resultados ya existentes. Sí sería necesario validar su ejecutor y el diseño pertinente antes de ofrecer nuevos cortes causales como prestación confiable. El piloto no incluye esas corridas.

No haría todavía: SaaS, panel web, integración con robots, hardware, entrenamiento de una arquitectura nueva, simulación integral a demanda, experimentos biológicos ni promesas de ahorro 94x. Mantendría esta oferta separada de las otras líneas de negocio.

## Diferenciación que sí probaría

No vender acceso al conectoma ni la mera posibilidad de ejecutar circuitos. [neuPrint](https://www.frontiersin.org/journals/neuroinformatics/articles/10.3389/fninf.2022.896292/full) ya ofrece consulta y análisis mediante web y APIs. [FlyBrainLab](https://flybrainlab.github.io/FlyBrainLabWeb/) ya presenta exploración, construcción y ejecución de circuitos, además de herramientas relacionadas.

La apuesta es una capa de verificación por encargo sobre herramientas existentes: pregunta acotada, contraste, instrumento capaz de fallar y evidencia entregable. Las fuentes externas justifican no competir como otro visor/simulador; no prueban que nadie ofrezca esta verificación ni que exista demanda paga. Lectura acotada, no estudio sistemático de competencia.

## Experimento comercial de 30 días

Cronograma propuesto desde una futura autorización de ejecución, no actividades ya iniciadas.

- Días 1 a 5: preparar una sola demo con resultados propios ya públicos, controles positivos/negativos y límites visibles. Probarla con instrucciones limpias. Tope de inversión inicial propuesto: 20 horas de trabajo y USD 100 de gasto directo; no es gasto autorizado ahora.
- Días 6 a 15: presentar la misma oferta a 20 grupos calificados con proyecto activo y posible presupuesto. Proceso preferentemente asíncrono. No regalar auditorías completas. Antes de enviar, validar destinatario, pertinencia y permiso de contacto. No se seleccionó ni contactó a nadie en este turno.
- Días 16 a 30: intentar cerrar y entregar dos pilotos pagos bajo el mismo contrato. Registrar horas de adaptación, ejecución, comunicación y retrabajo; gasto directo; objeciones de compra; y si el cliente pudo reproducir el resultado. Dos pilotos serían USD 2.000 de facturación bruta potencial, no ingreso esperado ni dinero obtenido.

Criterio propuesto para continuar: dos pilotos efectivamente pagos y entregados dentro del alcance, con como máximo 16 horas totales de trabajo por piloto y USD 50 de costo directo por piloto, y reproducción por el cliente del resultado pactado. Estos son objetivos de decisión, no datos existentes.

Con esos supuestos, USD 1.000 menos USD 50 deja USD 950 antes de remunerar el trabajo, comisiones, impuestos y adquisición. A 16 horas son USD 59,38 por hora antes de esos conceptos; no es margen neto. El tiempo de crear la demo y conseguir clientes debe contarse por separado. Si cada cliente exige rehacer todo, el precio o el alcance no funcionan.

Condición de pausa: sin ventas o con adaptación mayor que el presupuesto, no construir la plataforma. Si la oferta no llegó al decisor, no había presupuesto o compras institucionales impidió cobrar en plazo, registrar prueba comercial inconclusa, no «mercado refutado». Pedidos de publicación, elogios o interés sin pago no cuentan como validación comercial. La investigación puede seguir aunque esta oferta se pause.

## Camino al producto de software

Sólo si aparecen encargos repetidos que comparten entradas y pruebas, extraer el ejecutor común: una herramienta que ejecute comparaciones y entregue un paquete de evidencia, con soporte pago. Antes de invertir en autoservicio, exigir al menos una recompra o repetición concreta del mismo trabajo y medir qué parte se reutiliza.

La biblioteca de circuitos para percepción/control queda como segunda apuesta científica y técnica, no como promesa para vender el piloto. Necesita predicciones reservadas, transferencia a tareas reales y costos completos. Cobrar verificación sería capturar valor del método actual, no demostrar que esa biblioteca ya existe.

## Salvaguardas y registro

- Datos y código de clientes no van al repositorio público del proyecto. Se necesita un entorno, permisos de acceso, confidencialidad y entrega acordados; la propuesta no acredita hoy una infraestructura comercial segura.
- Revisar licencias de datos, código y modelos antes de redistribuir o cobrar su integración. Que un recurso sea público no significa que tenga cualquier uso comercial permitido.
- No usar manuscritos no publicados como material promocional sin autorización. La demo propuesta se limita a resultados ya públicos.
- Fuente propia: [Reauditoría de Papers 1-3 y Topo](https://github.com/gatehot59-star/drosophila-fep-connectome/blob/main/docs/auditorias/2026-11-02-03-astra-reauditoria-papers-topo-replica-y-rutas-visuales.md) y [síntesis de potencial](https://app.clickup.com/90171457413/docs/2kza6fw5-26397). Base main consultada: c1845fa0452389c9373dc4f8e212de5e55d6fc70. La nota anterior se recuperó exacta: 7.732 bytes, SHA256 5f46575267d170cd293d4ca2cd78b80a6c905f1fd84739c2001dca524a38b40e. Inventario de capacidades leído en el turno previo; no se afirman nuevas capacidades ni costos medidos.
- Herramientas de este turno: GitHub, consulta web, lectura y registro en brain-env por gateway, continuidad SQLite y Doc de ClickUp. Sin agentes adicionales ni evaluación externa de esta apuesta.
- PASS documental: fuente y alcance contrastados. FAIL nuevo: ninguno medido; se propone una condición de pausa, no un fracaso observado. NO MEDIDO: demanda, precio aceptado, clientes, tiempos de entrega, costos reales, portabilidad externa, renovación y seguridad comercial. Gate I experimental: N/A. Gate II: propuesta con hipótesis y criterios de decisión. Gate III: su cierre final se registra en la continuidad del proyecto después de verificar Git y leer el Doc publicado.
- No se implementó software, no se lanzó cómputo científico, no se contactó a nadie, no se cobró ni se comprometió un presupuesto. Sin cambios a papers, sellos, 009-A1 o código. Esta nota es la apuesta solicitada, no su ejecución.
