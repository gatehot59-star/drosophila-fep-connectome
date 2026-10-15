# 2026-10-14-031 · La auditoría de Fable, revisada contra el repo: acierta en lo grave, se equivoca en siete puntos que se pueden chequear, y el plan son cinco sellos

## Pedido
Abraham, 15-oct 00:06: pegó la auditoría que hizo Fable 5.1 (Abacus.AI) sobre el expediente de las 23:06 (`EXPEDIENTE-AUDITORIA-FABLE-2026-10-14.md`). No hay un pedido explícito. Lo leo así: revisarla contra el repo, porque Fable no lo abrió, y decir qué cambia.

**Revisión (15-oct, 00:17, pedido de Abraham):**
- aclaré a qué cifra de Fable se refiere la elección de τ;
- marqué INVÁLIDA cada mención del descriptivo de H_DEBILES.

Abraham aprobó subir la 030 y esta respuesta como un commit de documentos, sin código ni corridas.

## Veredicto primero
- [CONCLUSIÓN] **Fable acierta en lo grave.** Lo acepto y cambia cómo escribimos:
  - **El rival es débil para una afirmación de producto.** El banco nunca enfrentó al cableado contra ridge ni contra un MLP chico. En `tarea_mosca` y `lineas_etiquetadas`, ridge crudo saca 0,9935 y 0,9867, contra 0,9005 del cableado. NO MEDIDO en los factoriales: lo confirmé con una búsqueda de «ridge» en `factorial2_mosca.py`, que da 0 líneas.
  - **La elección de τ hace el trabajo.**
    - La τ elegida le gana a la regla por +1,78 puntos. La peor de las candidatas (la semilla 14) pierde contra la regla en promedio en las 6 celdas, por 0,3 a 2,5 puntos. Por ejemplo, en 0,0|0,15 da 0,9088 contra 0,9267 de media sobre las 10 pruebas.
    - Fable estimó que elegir la τ vale unos 0,9 puntos: los +1,78 de H_TAU menos los +0,85 de F3, que promedia las semillas de τ 0 a 9.
    - La validación cruzada lo confirma por otro camino. La τ elegida le saca a la candidata media entre 0,66 y 1,52 puntos de validación según la celda, cerca de 1 en promedio (`htau_c*.json`).
  - **SL no aísla el cableado fino.** Hace falta un nulo que baraje solo entre interneuronas y conserve lo que sale de los sensores y lo que llega a las descendentes.
  - **BANC.** El 92,4 % está calculado sobre aristas evaluables (los dos extremos con pareja en BANC): 782.453 de las 4.031.897 de R2, el 19,4 %. Eso sesga hacia tipos estereotipados, y los tipos de BANC heredan nombres de FlyWire. Falta el nulo de parejas al azar dentro del tipo.
  - **H_REUSO** sigue con los límites que señala:
    - el nulo de clase;
    - p en el piso;
    - pares que no son independientes;
    - el signo del glutamato;
    - la circularidad de los tipos;
    - falta un control negativo.
  - **H_ESCALA.** R2 es R1 más las presinápticas con 5 sinapsis o más sobre R1 (`factorial2_mosca.py`, línea 19). El cerebro entero agrega el resto, con las mismas 564 entradas y las mismas 6 descendentes. Vale **para esta tarea**, no como ley de escala.
  - **Wording.** Hay que corregir cómo lo dijimos:
    - F3 y F4 no son un «empate técnico»: son superiores por menos del margen (el IC90 excluye el 0).
    - En H_TOPO_NUEVO es la regla nueva la que le gana al cableado, por +1,68.
    - H_FRENO no prueba que «a dos saltos nada frena»: no hay freno **específico del looming frontal** entre los 7 mecanismos. LHAD1g1 sí frena del mismo lado.
    - No escribir «la mosca resta».
    - Reportar razones y no z para los z de −78,9 y +181.
    - No citar los p por ensayo (McNemar 1e-34, 1e-59, 1e-155).
  - **Paper 1.** Z_CP sobre 5 realizaciones y la RDI sin reproducir no deberían ir en el título ni sostener el resumen. Decide Abraham: reproducir antes de depositar o sacarlos.
  - **Dos máquinas prueban determinismo, no corrección.** De acuerdo (W-01).
- [MEDIDO] **Siete puntos en los que Fable se equivoca o queda corto, chequeados en el repo:**
  1. **Pseudo-replicación en F2 a F4.**
     - Los intervalos son bootstrap de dos vías sobre las 10 semillas de τ y las 10 de prueba, con la media por corrida (`agregar_factorial3.py`, líneas 9 y 46). No son por ensayo.
     - El «482/600» es un conteo descriptivo.
     - En H_TAU el bootstrap es sobre las 10 semillas de prueba con la τ elegida (`SELLO-HTAU.md`, línea 18).
     - **Sí tiene razón** en dos cosas: el IC de H_TAU no cubre la variación entre redes, y los McNemar de ES-012 a ES-014, RB-004 y RB-012 son por ensayo.
  2. **«El estadístico del nulo no está definido».**
     - Está definido y sellado: celda 0,3|0,15, semilla de τ 0 y prueba 2 (`nulos_r2.py`, líneas 6, 7 y 37).
     - El real en esa celda es 0,9465, y lo controla REPRO_R2. Es una comparación pareada, no un W puntual contra una media.
     - **Sí tiene razón** en que es una sola red: n = 1 semilla de τ para la prueba de nulos.
  3. **«Empates en la validación cruzada de H_TAU».**
     - No hubo. La semilla 10 es estrictamente la mejor en las 6 celdas, con una brecha sobre la segunda de 0,04 a 0,63 puntos (`htau_c*.json`, el campo `validacion` por candidata).
     - En 0,3|0,15 y 0,3|0,45 la segunda (la semilla 15) queda a 0,04 puntos: casi empate, pero no empate.
     - Las candidatas (semillas de τ 10 a 19) y las pruebas (semillas de ensayo 12 a 21) son corrientes distintas, como sospechaba.
  4. **«El núcleo no reajustó la ganancia».**
     - Reajustó dos cosas: el radio espectral vuelve a 0,9 sobre el núcleo y los umbrales del lector se recalibran en el entrenamiento (`nucleo_mosca.py`, líneas 10, 165 y 190).
     - Lo que **no** se reajustó: la ganancia de entrada y la τ. La prueba barata es el núcleo con τ elegida por validación cruzada, como H_TAU.
  5. **«H_DEBILES apunta a que importan las aristas fuertes».**
     - Los números descriptivos de una corrida INVÁLIDA, que no se citan como resultado, dicen otra cosa para los últimos 3 puntos (misma celda):
       - núcleo, 0,9135;
       - núcleo más las débiles barajadas, 0,9171 (de la corrida INVÁLIDA);
       - núcleo más las débiles reales (R2), 0,9465.
     - Barajadas, las débiles suman 0,4 puntos; reales, 3,3. Si se confirma con la corrida válida, importa **cuáles** son, no cuántas.
     - La corrida es INVÁLIDA y no la leo como resultado. Lo que sí vale de su punto: la mayor parte de la ventaja sobre los nulos ya está en el núcleo (0,9135 contra un máximo SL de 0,757).
  6. **«El umbral de H_FRENO no está».**
     - Está en el sello (`SELLO-FRENO.md`, líneas 30 y 31). CANDIDATO pide cuota de 0,05 o más y percentil de 0,90 o más, en los dos lados. DESCARTADO, cuota menor que 0,05 o percentil menor que 0,50, en los dos lados.
     - M6 tiene cuota de 0,06 % y 0,03 %: lo descarta la cuota, no el percentil. El expediente no lo traía; la falta era mía.
  7. **«RB-004 da EMPATE con p de 3e-5».**
     - Es por diseño: MEJOR y PEOR piden el mismo signo en **todas** las semillas, además de p menor que 0,05 (`memoria_dura.py`, líneas 168 y 169). Es la semilla como unidad que Fable pide en otras filas.
     - Que DBC3 quede debajo de 2/3 no contradice H2: DBC3 da de 0,658 a 0,664 y sin memoria, de 0,655 a 0,657. Los dos quedan debajo del techo teórico.
- [MEDIDO, menores]
  - En RB-002, «anillo de rumbo, de memoria» describe la función del anillo (memoria del rumbo); no quiere decir que las predicciones se eligieran de memoria. La crítica de fondo vale: falta una tasa base con pares al azar.
  - En ES-011, Q1 era el contraste declarado de su veredicto (`escape_dificil.py`, líneas 39 y 46), uno por veredicto. Fable tiene razón en que no hay control del error entre veredictos.
  - En F1 hay nulos de 20 (LIF, p 0,0476) y de 50 (p 0,0196). Confirmado; hay que homogeneizar.
- [NO MEDIDO]
  - El 91,11 % del piloto de `mojo-absoluto`: la búsqueda de código no lo encontró. Acepto no citarlo como ganancia: es una raíz de 90.
  - El esperado de LC6 → GF (5,8 contra 17,2) con la hipergeométrica exacta.

## Qué cambia en lo que afirmamos
Adopto su lista de afirmaciones que no se sostienen, con dos ajustes:
- La 3 («el cableado exacto como unidad causal») queda en suspenso hasta que H_DEBILES sea válido. El descriptivo de la corrida INVÁLIDA apunta a que las débiles importan por cuáles son, y no se cita.
- La 4 («el núcleo no alcanza») se prueba con τ por validación cruzada, porque el radio y los umbrales ya se reajustaron.

## Plan: cinco sellos, por valor sobre costo
Primero va lo que decide si hay producto (O-01).

| # | Sello | Falsador | Costo |
|---|---|---|---|
| 1 | **H_RIVAL** (incluye H_TAU_JUSTO): ridge, MLP chico y la regla con perillas (umbral o ganancia por tipo, 10 candidatas por validación cruzada, el mismo presupuesto que la τ), sobre las mismas 564 entradas y los mismos ensayos de R2 | Si el mejor rival queda a 1 punto o menos del cableado (o arriba), la tesis de producto cae y queda la científica | CPU, minutos a pocas horas en brain-env o Actions |
| 2 | **H_INTERIOR** y **H_REUSO_ESTRICTO**: barajar solo las aristas entre interneuronas; SL por clase del destino; 300 nulos o más. Para H_REUSO: solo GABA como sensibilidad, un par que no debería tener plantilla y tipos de BANC sin `fafb_cell_type` | W cae dentro de la distribución del nulo interior, o T2 no supera al nulo de clase | Actions, horas |
| 3 | **Estadística re-sellada**: W sobre 30 semillas de τ o más, nulos en varias semillas y bootstrap por semilla | El IC de F3 o de H_TAU toca el 0 o el margen | Unas 3 veces F3 |
| 4 | **Núcleo**: relanzar las 2 celdas de H_DEBILES y probar el núcleo con τ por validación cruzada | Con τ elegida, el núcleo sigue más de 1 punto abajo de R2 | 2 celdas y una grilla chica |
| 5 | **Paper 1**: reproducir Z_CP y la RDI con 100 realizaciones CP o más antes de depositar, o sacarlos del título y del resumen | Z_CP menor que 3 con 100 realizaciones | CPU, horas (NO MEDIDO) |

La demo de cámara a vibración empieza por el baseline clásico (tiempo al choque, τ de Lee). C99/Q15 va con paridad contra numpy antes que latencia, como propone Fable.

## Herramientas y máquina
- **brain-env.** Lectura de las ramas con `git show` desde el clon de main con todas las ramas. Scripts de lectura `verif1` a `verif8` en `/workspace/fable/`. No se corrió ningún modelo.
- **GitHub.** Búsqueda de código en `mojo-absoluto`, sin resultado.
- **Acción delicada:** ninguna. Esta respuesta y la 030 suben juntas, como un commit de documentos aprobado por Abraham a las 00:17.

## Archivos
- Este archivo, en `docs/agents/respuestas/` de main, en el mismo commit de documentos que la 030. El CONTEXTO se actualiza en un parche aparte, junto con la 032.
- Evidencia leída, sin cambios:
  - `results/htau_2026-10-14/htau_c0.json` a `htau_c5.json`;
  - `tools/factorial3/agregar_factorial3.py` y `nulos_r2.py`;
  - `tools/nucleo/nucleo_mosca.py`;
  - `tools/frena_giro/SELLO-FRENO.md`;
  - `tools/escape_aterrizaje/memoria_dura.py`;
  - `tools/escape_motivo/escape_dificil.py`;
  - `tools/factorial2/factorial2_mosca.py`.

## NO MEDIDO
- Los cinco sellos del plan.
- El denominador del piloto de `mojo-absoluto`.
- El esperado exacto de LC6 → GF.
- Las inferencias que Fable marcó como suyas y no chequeé:
  - la sensibilidad a la partición en OC-3;
  - el número de permutaciones de P1-b (los métodos dicen N = 100 para MS estático; el p mínimo posible es 0,0099).

## Antes de firmar
| Afirmación | Instrumento | ¿Podía dar rojo? |
|---|---|---|
| No hubo empates en la validación cruzada de H_TAU | `validacion` por candidata en los 6 json | Sí: un empate se ve como dos valores iguales |
| Los IC de F3 son por semilla, no por ensayo | la función `bootstrap` de `agregar_factorial3.py` | Sí: remuestrea índices de semillas de τ y de prueba |
| El nulo está definido y es pareado | `nulos_r2.py`, constantes CELDA, TAU y PRUEBA | Sí |
| El núcleo reajusta el radio y los umbrales | `nucleo_mosca.py` | Sí |
| El umbral de H_FRENO existe | `SELLO-FRENO.md` | Sí |
| El EMPATE de RB-004 sale de la regla de signos | `memoria_dura.py`, líneas 168 y 169 | Sí |
| El piloto da 91,11 % | ninguno | No: NO MEDIDO |

--- METODO PROMETEO ---
Leer la auditoría entera. Chequear contra el repo cada punto que se puede chequear, antes de aceptarlo o de discutirlo. Decir dónde se equivoca el auditor y dónde nos equivocamos nosotros. Convertir lo que queda en sellos con falsador. No escribir en git hasta tener el visto bueno, que llegó a las 00:17.
