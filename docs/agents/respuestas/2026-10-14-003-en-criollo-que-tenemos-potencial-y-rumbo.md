# 2026-10-14-003 · En criollo: tenemos un reflejo de mosca copiado del cableado real, que se repite en otra mosca; lo que falta saber es si la pieza chica alcanza y si le gana a la regla a mano

**Pedido.** 14-oct 11:17: «Primero explica en criollo que tenemos entre manos. El potencial y hacia donde vamos».

## Veredicto primero
- **[MEDIDO] Tenemos un reflejo de mosca que funciona copiado del cableado real.** Es el reflejo de escapar o aterrizar según si la mosca vuela: recibe lo que ven 4 tipos de neuronas de los ojos y decide por 6 neuronas de salida. Con el cableado real acierta unas 93 o 94 de cada 100 veces en promedio.
- **[MEDIDO] El cableado importa.** Si se barajan las conexiones o los sensores, cae a unas 65 a 76 de cada 100 en promedio (factoriales 3 y 4).
- **[MEDIDO] No hace falta el cerebro entero.** El cerebro entero (138.639 neuronas) da la misma respuesta que un recorte de 33.489 en el 99,9 % de los ensayos (2026-10-14-001).
- **[MEDIDO] Lo que se repite en otra mosca son las conexiones fuertes.** En BANC está el 92,4 % de nuestras conexiones de 20 sinapsis o más, contra el 28,9 % de las de 1 a 4 (2026-10-14-002).
- **[MEDIDO] La pieza conservada es chica:** el 15 % de las conexiones carga el 57 % de las sinapsis.
- **[MEDIDO] Lo que todavía no ganamos:** una regla escrita a mano con los mismos sensores rinde casi igual. La red le saca +0,86 puntos, sin decidir (IC90 +0,11 a +1,51). Y depende de la semilla de tau: en 8 de 10 gana y en 2 pierde.
- **[CONCLUSIÓN] El potencial es una fábrica de reflejos chicos, copiados de la mosca, que se repiten entre animales.** Sirven para robots y para hacer de portero entre un sensor y una IA (el aviso de choque de la 020). No es un cerebro entrenable ni un reemplazo de los modelos de lenguaje.
- **[CONCLUSIÓN] Lo que decide si hay producto son dos pruebas ya selladas.** H_CONSENSO dice si la pieza chica alcanza. H_TAU dice si, eligiendo bien los tiempos, el cableado le gana a la regla.

## Lo que tenemos, sin jerga
1. **El mapa.** FlyWire es el mapa completo de un cerebro de mosca hembra: quién se conecta con quién y con cuántas sinapsis. BANC es otro mapa, de otra mosca hembra, con cerebro y médula.
2. **El banco de pruebas.** Le mandamos a la red estímulos visuales simulados (algo que se acerca, de un lado o del otro, con ruido) y miramos qué hacen las 6 neuronas de salida. Aprende solo un umbral por salida; el cableado queda tal cual viene de la mosca.
3. **Los controles.** Cada resultado se compara con la misma red barajada y con una regla a mano que usa los mismos sensores. Todo se sella antes de correr y queda en git con su md5.
4. **Lo nuevo de hoy.** Las conexiones que sostienen el reflejo son, en buena parte, las que se repiten en otra mosca. Eso sugiere que la pieza no es un accidente de un individuo.

## El potencial (lo que vale y lo que no)
- **Vale:** una pieza acotada (603.219 conexiones en vez de los 15 millones del cerebro) que hace un reflejo concreto, con cableado auditado y repetido entre animales. Se puede exportar a un robot o a un sensor barato.
- **Vale:** un método reproducible (sello, nulos, paridad, md5) que sirve para un paper y para cada pieza nueva.
- **No vale todavía:** decir que la pieza le gana a una regla simple. Hoy empata. Si sigue empatando, el producto honesto es la regla sacada de la mosca, que también sirve y es más barata.
- **No vale:** venderlo como cerebro artificial general o como sustituto de un LLM. Es un reflejo, no un pensamiento.

## Hacia dónde vamos (en orden)
1. **H_CONSENSO** (sellado, unas 1,5 h): ¿la pieza del 15 % hace el reflejo igual que R2 entero y le gana a sus barajados? Si sí, la pieza existe. Si no, el reflejo necesita también las conexiones débiles.
2. **H_TAU** (sellado, unas 2,6 h): ¿eligiendo los tiempos solo con el entrenamiento, el cableado le gana a la regla por más de 1 punto? Si sí, la red aporta algo que la regla no tiene.
3. **El nulo de BANC:** comparar el 92,4 % contra parejas al azar, para saber cuánto de la conservación es real.
4. **H_OTRA_MOSCA:** correr el mismo banco sobre el cableado de BANC. Si el reflejo funciona en otra mosca, la pieza es de la especie y no del individuo.
5. **Si todo eso aguanta:** Paper 2 (núcleo conservado que carga la función) y la primera demo: cámara → pieza de mosca → vibración de aviso.

## Herramientas y máquina
Lectura de la 2026-10-13-015 a la 2026-10-14-002 en git (main `8867004`, rama `titan/htau-nucleo-banc-2026-10-14` `4f4e672`). Sin máquinas nuevas ni corridas en esta respuesta.

## Qué se midió
Nada nuevo. Esta respuesta resume lo medido y sellado en las respuestas citadas.

## Evidencia cruda
- Factorial 4 leído: `results/factorial4_2026-10-13/agregado.log` (`539733b9`), rama `titan/factorial4-cerebro-entero-2026-10-13`.
- BANC y el núcleo: `results/banc_2026-10-14/emparejar_banc.log` (`b39df7f9`) y `nucleo_construir.log` (`66e62422`), rama `titan/htau-nucleo-banc-2026-10-14`.
- Sellos: `tools/htau/SELLO-HTAU.md` (`8fbd0abd`) y `tools/nucleo/SELLO-NUCLEO.md` (`3ddb3414`).

## Archivos
- Este archivo: `docs/agents/respuestas/2026-10-14-003-en-criollo-que-tenemos-potencial-y-rumbo.md`.
- Doc de ClickUp: https://app.clickup.com/90171457413/docs/2kza6fw5-22117

## NO MEDIDO
- Si la pieza chica hace el reflejo (H_CONSENSO), si eligiendo tau se le gana a la regla (H_TAU) y si el reflejo funciona en BANC (H_OTRA_MOSCA).
- El nulo de la conservación en BANC.
- El costo real de la pieza en un microcontrolador y la demo de cámara a vibración.
- Que nadie haya probado antes una pieza conservada en un banco funcional: la búsqueda de la 018 fue acotada.

## Antes de firmar
| afirmación | instrumento | ¿podía dar rojo? | veredicto |
|---|---|---|---|
| el cableado importa | 50 SL + 50 T por recorte, Holm | sí | verde (factoriales 3 y 4) |
| no hace falta el cerebro entero | CE contra R2, equivalencia ±1 punto | sí | verde (H_ESCALA refutada) |
| se repiten las conexiones fuertes | presencia en BANC por tramo | sí, podía dar plano | verde, sin nulo |
| la red le gana a la regla | IC90 contra +1 punto | sí | NO: sin decidir |
| la pieza chica alcanza | H_CONSENSO | sí | NO MEDIDO (sellado) |

--- METODO PROMETEO ---
Accion delicada: no (solo explicación; nada corrió ni se mergeó).
Maquina: ninguna nueva; lectura de git.
Artefactos: docs/agents/respuestas/2026-10-14-003-en-criollo-que-tenemos-potencial-y-rumbo.md + Doc de ClickUp https://app.clickup.com/90171457413/docs/2kza6fw5-22117
