# 2026-11-01-003 · En criollo: tenemos piezas probadas y un laboratorio, todavía no la receta generadora

Doc: https://app.clickup.com/90171457413/docs/2kza6fw5-26157

## 1. Pedido

«EN CRIOLLO QUE ES LO QUE TENEMOS». Alcance: el trabajo de Topo inverso y conectoma del Doc seleccionado, no un inventario de todos los proyectos.

## 2. En criollo

**Tenemos más que una idea: un banco de pruebas con resultados, patrones de cableado identificados y un lenguaje para escribir circuitos. Todavía no tenemos la receta que genere automáticamente otras redes útiles.**

- **El plano y el banco de pruebas.** Trabajamos con mapas reales de conexiones de la mosca y código que permite probar circuitos en simulación. Podemos comparar el cableado real con versiones alteradas y medir qué cambia. El mapa anatómico es real; la función que evaluamos acá es simulada, no una mosca viva.
- **Un indicio de piezas reutilizadas.** Encontramos una plantilla de conexiones entre proyección visual, descendentes y una vía inhibitoria predicha que se repite en FlyWire y BANC, más que en los barajados probados. Es un indicio anatómico concreto. Falta el control más exigente para descartar que parte de la diferencia venga de qué clases de neuronas conectan entre sí; no equivale a haber demostrado una ley del cerebro.
- **Una utilidad concreta, acotada.** Un recorte del cableado prepara señales visuales para un clasificador. En promedio sobre la curva ensayada, le ayuda a aprender con pocos ejemplos mejor que las alternativas comparadas. No gana en todos los puntos. Y entregar solo 240 números al lector no lo vuelve barato: por detrás siguen calculándose 33.489 neuronas y 4.031.897 conexiones.
- **Topo, una manera propia de escribir esas reglas.** Ya podemos describir y ejecutar circuitos con reglas que escribimos nosotros. Topo no descubre todavía esas reglas solo. Topo inverso es el nombre de la propuesta de buscar programas que generen redes, no una herramienta ya implementada.

**El salto que falta es pasar de copiar y estudiar el plano a encontrar una receta corta que fabrique otros circuitos y conserve lo útil.** Para demostrarlo, la receta tiene que rendir en datos no usados para ajustarla y justificar su costo frente a alternativas simples. Producir un dibujo parecido no alcanza.

Mi lectura: lo más valioso hoy es la combinación de piezas medidas y un banco que puede mostrar cuándo una idea falla. No hay todavía una gramática funcional aprendida, un cerebro artificial terminado ni una superioridad general frente a redes artificiales. Tampoco es una idea sin antecedentes: hay trabajos cercanos que leer completos antes de sellar nuestra siguiente prueba.

El parche de recién no agregó inteligencia ni resultados científicos: dejó este estado y sus pendientes correctamente anotados.

## 3. Herramientas y máquina

Lectura del Doc corregido, de la cabecera vigente del CONTEXTO y de la respuesta 002. Estado leído: main `97f13af671305cdfeca1a0f13f7e81a92aa17574`. GitHub API pública desde brain-env para la lectura; conector GitHub para este archivo; ClickUp para añadir la explicación al Doc existente. Sin cómputo científico, GPU, instalaciones ni cambios de código.

## 4. Evidencia y qué se midió

Ninguna medición científica nueva. Se traduce el alcance de resultados históricos ya auditados, sin ampliarlo.

- [Respuesta corregida 001](https://github.com/gatehot59-star/drosophila-fep-connectome/blob/e65ec936522d5151237ef63f7e716a641078d71d/docs/agents/respuestas/2026-11-01-001-topo-inverso-gramatica-funcional-por-medir.md), sección 2: Topo manual, enriquecimiento anatómico, curva de pocos datos y costo del extractor.
- [Log de H_REUSO](https://github.com/gatehot59-star/drosophila-fep-connectome/blob/c74509ac461bb1aa129f1a42dc9645d26b22f444/results/reuso_2026-10-14/reuso.log). Citas históricas verbatim, no ejecución de hoy:

```text
FLYWIRE T1 fraccion_con_plantilla=0.8835 nulo media=0.6823 max=0.7462 p=0.0050
BANC T1 fraccion_con_plantilla=0.8260 nulo media=0.3472 max=0.4744 p=0.0050
```

- [Agregado de H_PARES_DATOS](https://github.com/gatehot59-star/drosophila-fep-connectome/blob/e5db87062e6dfeb1a370e53c11926660f1dc0bc8/results/pares_datos_2026-10-18/agregado.log): la respuesta corregida registra +4,01 puntos medios frente al lector crudo, +15,20 frente a PCA y +9,04 frente a proyección aleatoria, sobre la curva de 6 a 768 ejemplos y dos condiciones. En c2 el crudo alcanza o supera al embudo desde 96; PCA, desde 768. Por eso esta explicación dice «en promedio», no «siempre».
- [Topo v0.2](https://github.com/gatehot59-star/drosophila-fep-connectome/blob/a817ad361982b1db92e12fd67bc1da590e0e00f8/docs/topo/TOPO-v0.2-diferencial.md): reglas manuales y 800/800 decisiones equivalentes con el programa anterior. Eso no identifica por sí solo el mecanismo biológico.

## 5. Archivos generados

Este archivo, `docs/agents/respuestas/2026-11-01-003-en-criollo-que-tenemos.md`, y la sección 12 del Doc de Topo inverso, en Space. No se modifica CONTEXTO: esta explicación no cambia el estado científico ni las decisiones del proyecto.

## 6. NO MEDIDO

Gramática aprendida; control estricto y análisis por superclase; conservación funcional por redes generadas; ahorro real de cálculo o energía; novedad global; validación fisiológica; superioridad general o producto terminado. Revisión independiente no realizada.

--- METODO PROMETEO ---
Rol: explicación documental.
Acción delicada: NO. Modo: LIGERO. Rúbrica: N/A.
Instrumento: lectura del estado vivo y de la síntesis corregida; sin nueva ejecución experimental.
Máquina: brain-env para lectura, GitHub y ClickUp para publicación.
Review externo: no realizado; no se presenta esta síntesis como auditoría independiente.
Archivo: docs/agents/respuestas/2026-11-01-003-en-criollo-que-tenemos.md
Doc: https://app.clickup.com/90171457413/docs/2kza6fw5-26157
