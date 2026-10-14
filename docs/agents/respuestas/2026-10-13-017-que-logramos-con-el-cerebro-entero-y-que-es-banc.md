# 2026-10-13-017 · En criollo: qué logramos con el cerebro entero en el banco, y qué es BANC

## Veredicto

- **[MEDIDO] Lo logrado hasta ahora es de instrumento, no de ciencia.** El cerebro entero de la mosca entra al banco sin recortes: 138.639 neuronas y 15.091.983 conexiones. Corre gratis en una GPU T4 de Kaggle a 0,026 s por ensayo, unas 124 veces más rápido que el taller, y ocupa 3,1 GB de 15.
- **[MEDIDO] Es la misma cuenta.** Torch en GPU y numpy en CPU coinciden a 1e-16. En R2 la T4 da exacto el 0,9465 del factorial 3.
- **[MEDIDO] La respuesta científica todavía no está.** Los dos kernels estaban RUNNING a las 00:19 UTC; terminan entre las 00:30 y la 01:00 de Buenos Aires. El 0,975 contra 0,95 del humo sale de 80 ensayos y no vale nada.
- **[CONCLUSIÓN] Cualquier resultado sirve.**
  - Si el cerebro entero le gana a su regla o a R2 por más de un punto, el resto del cerebro aporta a esta tarea.
  - Si empata, R2 (un cuarto del cerebro) ya tiene lo que importa, y para un robot alcanza con menos.
  - Si pierde, el resto del cerebro mete ruido para esta tarea.
- **[LITERATURA] BANC** es el conectoma de cerebro y cordón nervioso juntos de una mosca hembra adulta (Bates et al., Nature 2026). Es una segunda mosca y trae el cordón que mueve el cuerpo. **«Natural» lo dijimos nosotros:** es el próximo conectoma obvio para probar el banco, no un tipo de conectoma.

## Pedido

21:18: «QUE LOGRAMOS CON HACER CORRER EL CERBRO COMPLETO EN EL BANCO?. QUE ES EL CONECTOMA NATURAL BANC?»

## Herramientas y máquina

- **brain-env:** `kaggle kernels status` de los dos kernels del factorial 4. Lectura de la respuesta 013 (lo que ya habíamos dicho de BANC).
- **Web:** una búsqueda para verificar BANC (Nature, PubMed, bioRxiv).
- **Sin escritura fuera de este commit.** Sin cuota gastada.

## Qué se midió

- Estado de los kernels a las 00:19:07 UTC: `f4-ce-a-2026-10-13` y `f4-ce-b-2026-10-13` RUNNING.
- Lo demás del instrumento está medido en la 2026-10-13-015: paridad, REPRO_R2, tiempos y memoria.

## En criollo: qué logramos con el cerebro entero

1. **Antes probamos con pedazos.** M46 (46 neuronas), R1 (unas 1.500) y R2 (33.489, un cuarto del cerebro). Las tres le ganan a sus barajados. Contra la regla de la mosca con los mismos sensores, sólo R2 la alcanza (+0,85 puntos, sin pasar el margen de 1).
2. **Faltaba la pregunta obvia:** ¿y con el cerebro entero? Hasta hoy era una cuenta, «3,7 veces R2», NO MEDIDO.
3. **Hoy quedó resuelto el cómo.** El cerebro entero entra en una GPU gratis y la cuenta es la misma que la de CPU. Lo prueba que R2 da el mismo número en las dos máquinas. El banco escala al conectoma completo sin costo: unas 7 h de cuota y 3,6 h de reloj para 600 corridas y 100 barajados.
4. **Esta noche llega el qué.** Las tres preguntas selladas son si le gana a su regla, si suma sobre R2 y si le sigue ganando a los barajados.
5. **Posición [LITERATURA]:** correr el cerebro entero de FlyWire no es nuevo. Shiu et al. (Nature 2024) lo simularon entero para predecir actividad. Lo nuestro es meterlo en un banco que lo compara contra su propio diseño y contra versiones barajadas, con los mismos sensores. La novedad sigue NO MEDIDA hasta una revisión sistemática.

## En criollo: qué es BANC

- **Qué es [LITERATURA].**
  - «Brain And Nerve Cord»: el mapa neurona por neurona del cerebro y del cordón nervioso ventral, el equivalente de la médula espinal, de **una misma mosca hembra adulta**.
  - Se cortó en 7.010 láminas, se fotografió con microscopio electrónico (4 × 4 × 45 nm) y se reconstruyó con redes neuronales y corrección a mano, con el método de FlyWire.
  - Esperan unas 160.000 neuronas: unas 140.000 en el cerebro y 20.000 en el cordón. Los une el cuello, con unas 1.300 descendentes y 1.800 a 1.900 ascendentes.
- **Qué encontraron [LITERATURA].**
  - Los músculos, las glándulas y las vísceras reciben sobre todo de los sensores de la misma parte del cuerpo: lazos locales.
  - Las descendentes y ascendentes los unen en módulos por conducta (escape, alimentación y otros).
  - Las regiones de aprendizaje y navegación supervisan, pero no hacen falta para actuar.
  - Lo describen como control distribuido, parecido a un sistema de ingeniería.
- **Por qué es nuestro próximo conectoma [CONCLUSIÓN].**
  - **Es otra mosca.** Todo lo nuestro sale de un solo animal, el de FlyWire. Si el cableado le gana a sus barajados también en BANC, deja de ser una casualidad de un individuo.
  - **Trae el cuerpo.** FlyWire termina en las descendentes, que son nuestra salida. BANC sigue hasta las neuronas motoras: es el camino del reflejo al robot.
  - **Se puede portar.** Según la documentación de su paquete (bancr), trae la columna `fafb_783_match_id`, que empareja sus neuronas con los IDs de FlyWire 783 que usa el banco. En los datos no se verificó.

## Evidencia cruda

```
abrahammendieta/f4-ce-a-2026-10-13 has status "KernelWorkerStatus.RUNNING"
abrahammendieta/f4-ce-b-2026-10-13 has status "KernelWorkerStatus.RUNNING"
Wed Oct 14 00:19:07 UTC 2026
```

- Bates, Phelps, Kim, Yang, Matsliah … Wilson, Lee. «Distributed control circuits across a brain-and-cord connectome». Nature (2026). doi 10.1038/s41586-026-10735-w. Preprint: bioRxiv doi 10.1101/2025.07.31.667571.
  - Del texto: «adult female D. melanogaster at synapse-level resolution (4 × 4 × 45 nm3)»; «7,010 serial sections»; «the expected approximately 160,000 neurons».
  - También: «brain and VNC … (140,000 and 20,000 neurons, respectively)» y «connected by about 1,300 descending neurons (DNs) and around 1,800 ascending neurons» (1.900 en el preprint).
  - Y: «Brain regions involved in learning and navigation supervise these circuits».
- Shiu et al., Nature 2024 (el mismo archivo de conectividad), ya citado con doi en la 2026-10-13-013.

## Archivos

- Esta respuesta. No cambia el estado del CONTEXTO: el factorial 4 sigue corriendo y sin leer, como dejó la 016.

## NO MEDIDO

- Cualquier resultado del cerebro entero en la tarea.
- Que BANC traiga `fafb_783_match_id` en sus datos, y cuántas de nuestras 564 entradas y 6 descendentes tienen pareja en BANC.
- El tamaño exacto de BANC en su versión pública: las fuentes dan de 160.000 a 188.000 neuronas.
- Que el banco portado a BANC dé lo mismo que en FlyWire.

## Antes de firmar

| afirmación | instrumento | ¿podía dar rojo? |
|---|---|---|
| el cerebro entero entra y la cuenta es la misma | paridad y REPRO_R2 de la 015 | sí: umbrales 1e-9 y 0,001 |
| los kernels están corriendo | `kaggle kernels status` a las 00:19 | sí: podía dar ERROR o COMPLETE temprano |
| qué es BANC | el artículo en Nature y su preprint | es literatura, no medición nuestra |
| «natural» no es un tipo de conectoma | la frase del CONTEXTO («es el segundo conectoma natural») | sí: si la palabra viniera de la literatura |

```
--- METODO PROMETEO ---
Accion delicada: no (síntesis con referencias)
Maquina: brain-env (kaggle kernels status) | web (1 búsqueda)
Artefactos: docs/agents/respuestas/2026-10-13-017-que-logramos-con-el-cerebro-entero-y-que-es-banc.md + Doc de ClickUp 2026-10-13-017
```
