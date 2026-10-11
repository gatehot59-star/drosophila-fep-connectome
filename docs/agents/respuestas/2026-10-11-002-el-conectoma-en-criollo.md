# 2026-10-11-002 · El conectoma en criollo: qué sabemos, qué probamos y para dónde vamos

**Fecha:** 2026-10-11, madrugada (America/Buenos_Aires) · **Máquina:** ninguna corrida · **Base:** `docs/agents/respuestas/2026-10-11-001-resumen-tecnico-logros-pruebas-y-rumbo.md` (main `c8e066a`)

**Veredicto en criollo:** rearmamos la cuenta del paper y da igual que en marzo; medimos quién les da órdenes a las neuronas de salida y, comparando bien, lo único que aguanta todo es que las descendentes se mandan entre ellas y a las motoras, y que el óptico casi no les habla. Para cerrar el paper falta una sola prueba.

## 1. Pedido

"en criollo el resumen" (Abraham, 2026-10-11), sobre la 2026-10-11-001.

## 2. Herramientas

- Ninguna corrida: es la 2026-10-11-001 contada sin jerga, y los números salen de ahí.
- GitHub MCP para subir; brain-env sólo para verificar el push.
- ClickUp: Doc público en el Space.

## 3. En criollo

### Qué hicimos

- **La cuenta perdida del paper (Tabla 7).** La rearmamos y da exactamente lo mismo que en marzo: 16 de 16. De paso apareció un error chiquito: el 8,7% del paper es un 8,6% redondeado dos veces. Y lo central del paper sigue en pie: la ida y vuelta de los cables baja a medida que la señal se acerca a los músculos, aunque se exija que cada cable tenga 5 sinapsis o más.
- **Qué hay al final de los cables.** Casi todo el cerebro se habla a sí mismo: el 97,6% de los cables. Las órdenes salen por un embudo chiquito de 1.485 neuronas, el 1%: las que bajan al cuerpo (descendentes), las motoras de la cabeza y las que largan hormonas (neurosecretoras). Y ese último tramo es casi de una sola mano: tiene poca vuelta.
- **Quién les da órdenes.** Contando cables, el cerebro central parece el jefe: pone entre el 60 y el 73% de lo que les llega a las tres salidas.

### La trampa de contar cables

Contar cables no alcanza: hay que comparar contra un azar bien hecho. Lo hicimos tres veces, cada vez más exigente.

1. **Contra destinos al azar (005).** Era un azar flojo: con etiquetas inventadas daba un 3% de falsos.
2. **Contra neuronas del mismo tamaño (006, 10.000 sorteos).** Se sostenía bastante y el central seguía arriba.
3. **Contra vecinas del mismo tamaño y de la misma zona del cerebro (007).** Acá se cayó más de la mitad de lo que parecía firme. El central les habla a las descendentes y a las neurosecretoras porque está cerca, no por un cableado especial, y con las ascendentes pasa lo mismo. Lo que sí es propio del central es un plus hacia las motoras de la boca.

Es como querer saber quién manda en una oficina contando quién le habla más al gerente: el que se sienta al lado siempre gana. Para saber quién manda de verdad hay que compararlo con los otros que también se sientan cerca.

### Lo que aguanta todo

Con la vara más dura (ni un solo falso positivo) y contra los dos azares:

- las descendentes se hablan entre ellas y les mandan a las motoras, sobre todo a las del cuello y las antenas;
- el óptico casi no les habla a las descendentes: mucho menos que sus vecinas.

Con una vara razonable (que acepta que hasta un 5% de lo firmado sea falso) se suman el plus del central hacia las motoras de la boca, y que lo sensorial y lo visual les hablan a las salidas menos que sus vecinas.

### ¿Hacer tantas pruebas no infla los resultados?

Lo medimos (008 y 009). Con la vara razonable no cambia casi nada, porque el corte que usábamos ya era así de exigente. Con la vara más dura quedan pocas. Conclusión: el problema nunca fue la cantidad de pruebas, sino contra qué comparábamos.

### Cómo sabemos que no nos estamos mintiendo

- 33 tests automáticos en 6 herramientas, todos en verde.
- Cada análisis estadístico tiene su prueba trampa: le damos etiquetas inventadas y no puede encontrar más cosas de las que daría el azar. No encontró.
- Cada vez que regeneramos un análisis tiene que dar idéntico al anterior, hasta el último decimal. Dio.
- Mis errores quedaron escritos: una primera corrida que falló por un chequeo mal hecho, una frase mal puesta en un Doc, un test flojo y una cuenta que no podía dar otra cosa que cero.

### Lo que todavía no sabemos

- **Si la caída de la ida y vuelta hacia los músculos es más que casualidad.** Falta compararla contra el azar circuito por circuito, con un test de tendencia. Eso es lo que decide el paper.
- **H4**, que la actividad del modelo corresponda a la anatomía real: no está medido. Con comportamiento real, la generalización entre ensayos dio azar y la estabilidad en el tiempo quedó al borde.
- **Producto:** SparseLTC empata con un modelo lineal; DBC3 aprende más rápido en una tarea, pero falta probar que los rivales estaban bien ajustados.

### Para dónde vamos

1. **Una sola prueba que importa:** la del azar por circuito con test de tendencia. Con eso el paper deja de describir y pasa a demostrar.
2. **Tres cosas que decidís vos:** qué va al erratum (el 8,6 y el ítem 9), si lo de quién manda en las salidas entra como anexo, y el PR #26, que nació para la Tabla 7, hoy tiene 7 commits y hay que ordenarlo antes de mergear.
3. **Subir los resultados** que hoy viven sólo en brain-env.
4. **Lo demás es opcional:** más sorteos para la 007, la cuenta de dos saltos con la zona fija y la zona de cada sinapsis. Sólo si el paper lo pide.

**Mi opinión:** cerrar, no abrir. Cada análisis nuevo mejora un anexo; la prueba del punto 1 decide el paper.

## 4. Evidencia

La de la 2026-10-11-001, que cita verbatim el inventario de tests y veredictos, y la de las respuestas 001 a 009 del 10-oct. Acá no hay números nuevos: si alguno no coincide con su respuesta, manda la respuesta.

## 5. Archivos

- Base: `docs/agents/respuestas/2026-10-11-001-resumen-tecnico-logros-pruebas-y-rumbo.md` (md5 `570160b74bd1c50eba6a656f3caa0882`) y su Doc técnico: https://app.clickup.com/90171457413/docs/2kza6fw5-20977
- Doc público de esta respuesta: [El conectoma en criollo: qué sabemos, qué probamos y para dónde vamos (11-oct)](https://app.clickup.com/90171457413/docs/2kza6fw5-20997).

## 6. NO MEDIDO

- El azar por circuito con test de tendencia, que es lo que decide el paper.
- H4 fuerte: la actividad del modelo contra la anatomía real.
- Que los rivales de DBC3 estuvieran bien ajustados.
- Todo lo que ya figura como NO MEDIDO en la 2026-10-11-001.

--- METODO PROMETEO ---
Máquina: ninguna corrida; brain-env sólo para verificar el push.
Artefactos: `docs/agents/respuestas/2026-10-11-002-el-conectoma-en-criollo.md` + Doc https://app.clickup.com/90171457413/docs/2kza6fw5-20997
