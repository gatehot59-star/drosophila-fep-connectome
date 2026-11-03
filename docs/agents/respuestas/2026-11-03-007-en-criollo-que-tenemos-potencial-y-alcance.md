# 2026-11-03-007 · En criollo: qué tenemos entre manos, potencial y alcance

**Doc:** [Topo inverso](https://app.clickup.com/90171457413/docs/2kza6fw5-26157), página «2026-11-03-007 · En criollo».
**Base:** `main` en `b65dd59b`, con la [respuesta 006](2026-11-03-006-corrida-a1-8540-de-8540-sellada-sin-leer.md) y su [página](https://app.clickup.com/90171457413/docs/2kza6fw5-26157/2kza6fw5-29657).

Pone al día a la [2026-11-03-001](2026-11-03-001-en-criollo-que-tenemos-y-potencial.md), de otro agente, escrita antes de 002, 005 y 006. No la contradice: la prueba que pedía primero (verificar que el ejecutor de 009-A1 corta lo previsto y detecta cortes mal hechos) ya está hecha, y la corrida también.

## La respuesta corta

Tenemos entre manos la prueba que decide si lo de DNp04 era una anécdota o una regla.

La regla candidata es simple: **un descendente prende a una inhibitoria, y esa inhibitoria frena a otros descendentes** (D→X⊣D′). Los descendentes bajan las órdenes del cerebro al cuerpo; la regla sería una forma de elegir una acción apagando las otras.

En el modelo del cerebro entero ya vale para un caso, DNp04→PVLP010. Ahora corrimos 8.540 cortes sobre 16 relevos y 6 hubs para ver si vale en general. Corrieron todos y son válidos, pero el resultado está en un sobre cerrado: nadie lo miró, y primero va el código que lo va a leer.

Si aguanta, es la primera pieza de gramática con muchos casos y no con uno. Si no aguanta, sabemos que DNp04 era especial. Las dos salidas sirven. Todo pasa dentro del modelo de Shiu, con una sola mosca con función (FlyWire) y sin hardware.

## Qué tenemos, en cinco escalones

1. **El mapa, en dos moscas.** La plantilla «sensor visual → descendente, y el mismo sensor → inhibitoria que vuelve sobre ese descendente» aparece mucho más que en sus nulos, en FlyWire y otra vez en BANC (H_REUSO_CIERRE).
   - FlyWire: el 88,35 % de los pares sensor-descendente tiene la plantilla, contra 49,66 % de media en los nulos; 698 inhibitorias la arman para dos o más tipos de descendente, contra 286,04.
   - BANC: 82,60 % contra 35,01 %, y 419 contra 76,515.
   - p = 1/201 en las cuatro pruebas, Holm 0,0199.

   Es anatomía: dice dónde mirar, no qué hace.
2. **El freno existe en el modelo, pero no por donde creíamos.** En el LIF de Shiu con el cerebro entero, silenciar a las inhibitorias sube a los descendentes entre 40 y 237 % (H_MECANISMO). El cable directo del sensor a la inhibitoria carga solo entre 23 y 49 % del freno: MIXTA.
3. **Lo que sí frena, en un caso.** Con LC4, el sensor de looming, cortar solo el cable DNp04→PVLP010 (190 sinapsis) devuelve el 40,6 % del freno. Silenciar PVLP010 devuelve el 74,6 %, y sin sus otras entradas PVLP010 conserva el 96,8 % de su actividad (H_MECANISMO_DNp04, SOSTENIDA_EN_MODELO). De ahí sale la regla candidata: inhibición recurrente entre descendentes.
4. **Los candidatos para generalizarla.**
   - Argon propuso 17 relevos descendente→inhibitoria conservados entre FlyWire y BANC (008). Astra los sostuvo contra un nulo de grados y dejó su predictor 7/7 como ajuste retrospectivo.
   - 009 diseñó el corte sobre 16 relevos y 010 lo enmendó: t pareada unilateral, con las familias F_B, F_C y F_R01 y Holm < 0,01.
   - Recalculé con instrumento propio las 314 guardas anatómicas de 009 y 010: 314 de 314 iguales (2026-11-03-002).
5. **La prueba grande, corrida y sellada.**
   - El runner corre el cerebro entero de Shiu, un ensayo por proceso, y sus 11 pruebas pueden dar rojo (005).
   - Los 8.540 ensayos corrieron en 30 minutos en 20 máquinas de 6 tipos de CPU. La validación da 8.540 de 8.540 y los testigos 200 de 200 idénticos (006).
   - Ningún estimando calculado.

Hoy también hubo un error mío, ya corregido en público: la 003 publicó un runner que no simulaba. La 004 lo dijo y la 005 lo rehizo de verdad.

## Cómo voy a leer el sobre, fijado antes de abrirlo

No cambia nada de 010: solo dice en criollo qué significaría cada salida.

| Si sale... | Quiere decir | Para la gramática |
|---|---|---|
| ΔQ2 activo en un relevo o hub | con el circuito encendido, cortar los cables de la inhibitoria hacia los frenados los libera al menos 5 Hz: ahí el freno existe | la cuenta de cuántos de los 22 dice cuánto generaliza «X frena a D′» |
| T1 pasa en R01, R02 y R03 | el descendente solo alcanza para prender a su inhibitoria (sin sus otras entradas, la inhibitoria conserva al menos la mitad), y cortar ese cable devuelve al menos el 35 % del freno, como DNp04 | el relevo uno a uno D→X⊣D′ generaliza |
| T2 pasa en 3 de los 4 tipos de hub | cortar todos los descendentes que entran al hub le baja la actividad al menos un 40 %, devuelve al menos el 40 % del freno y libera más que cortar uno solo | segunda forma de la regla: el hub que junta varios descendentes |
| F_C pasa | el hub dispara más con las espigas de sus descendentes sincronizadas que corridas en el tiempo | se puede hablar de compuerta, solo en el banco artificial C |
| ΔQ2 activo, pero T1 y T2 caen | hay freno, pero no lo prende el descendente | la regla se achica a «X frena», sin saber quién la prende, como en la MIXTA |
| NO_INFORMATIVO_EN_B o SIN_DECIDIR | la entrada de B no reclutó ese circuito, o el dato no alcanza | no cuenta ni a favor ni en contra; si son muchos, hay que cambiar el estímulo, no la anatomía |
| el verificador independiente da INVALIDO | algún recibo no cierra | no se lee nada: se corrige y se vuelve a correr |

F_R01, la cascada ZA de R01, habla de un solo relevo. El régimen A es descriptivo.

## Potencial (opinión, no medición)

- **Ciencia, lo más concreto.** Si aguanta, pasamos de un caso a una regla con hasta 22 instancias, predicha desde el cableado y probada con cortes en el cerebro entero simulado, con nulos y controles. Si no aguanta, también es publicable, porque el diseño estaba sellado antes de correr. El experimento en la mosca viva ya está propuesto para DNp04: silenciarlo y registrar GF y DNp06 ante looming. Ese no lo podemos hacer nosotros.
- **Método, el activo que ya existe.** Es un banco de cortes causales sobre el cerebro entero, sellado antes de mirar y reproducible bit a bit en 6 tipos de CPU. Corre 8.540 ensayos en 30 minutos sin costo, en Actions de repo público. Sirve para probar cualquier otra regla candidata con el mismo rigor.
- **Ingeniería.** Una biblioteca de piezas comprobadas, como frenos y selectores entre comandos, para control. NO MEDIDO: H_PARES enseñó que la ventaja contra redes artificiales del mismo tamaño se mide aparte, y acá no se midió.
- **Ingresos.** No esta semana. Lo vendible hoy es el método, la evaluación sellada y reproducible, no la mosca. Valor comercial NO MEDIDO.

## Alcance: lo que esto no es

- **Es el modelo, no la mosca.** El LIF de Shiu usa los mismos parámetros para todas las neuronas, signo por neurotransmisor predicho y solo sinapsis químicas. No tiene neuromodulación ni plasticidad.
- **Una sola mosca con función.** El mecanismo se mide en FlyWire v783. BANC aporta solo la conservación anatómica; BANC dentro del modelo está NO MEDIDO.
- **Entradas artificiales.** B mete Poisson a 50 Hz al descendente y a 25 Hz a los frenados. A (150 Hz) es solo descriptivo, y C es un replay artificial.
- **Una familia elegida, no una muestra del cerebro.** Los 16 relevos y 6 hubs salieron de un filtro anatómico. Si la regla aguanta, generaliza dentro de esa familia.
- **20 semillas por condición.** La potencia con n = 20 está NO MEDIDA.
- **Todavía no es gramática.** Una gramática tiene que predecir combinaciones no vistas. A1 prueba si una regla se repite, no si se combina. La prueba de composición (predecir el corte conjunto de dos relevos contra la suma de los cortes sueltos) está sin diseñar.
- **Cero hardware y cero producto.**

## Qué sigue, en orden

1. El código de la estadística de 010 §7, commiteado y probado con datos sintéticos que puedan dar rojo, antes de tocar los recibos.
2. El verificador independiente, a cargo de otro agente.
3. Abrir el sobre: correr la estadística y leer los veredictos con la tabla de arriba.
4. Documentación: el CONTEXTO, atrasado desde la 002, y la sección 15, que espera que pegues el texto de 003.

## 1. Pedido

«en criollo que tenemos entre manos, potencial y alcance» (3-nov 15:01), llegado mientras cerraba la 006.

## 2. Herramientas declaradas

- **brain-env** (gateway python): bajé de raw en `b65dd59b` la evidencia y la respuesta de 006, y comparé sha256 contra `/workspace/a1/v2/evid6/`. Solo escribí una copia de la respuesta en `/workspace/a1/v2/resp006.md`.
- **GitHub MCP:** lectura del CONTEXTO y de la 2026-11-03-001 en `main`, y este commit.
- **ClickUp:** lectura de la página de 005 para copiar el formato, y las páginas 006 y 007 del Doc Topo inverso.
- Sin Actions, sin simulación y sin abrir recibos de A1.

## 3. Qué se midió

| # | Afirmación | Instrumento | ¿Podía dar rojo? | Veredicto |
|---|---|---|---|---|
| 1 | La evidencia de 006 en `main` es la que se produjo en brain-env | sha256 de los 8 archivos bajados de raw en `b65dd59b` contra `/workspace/a1/v2/evid6/` | Sí: un byte distinto da DISTINTO | PASS, 8/8 IGUAL. El README se escribió en el push y no tiene copia local |
| 2 | Los números de los cinco escalones son los de git | lectura del CONTEXTO (blob `ff447c0c`) y de la respuesta 006 (sha256 `d6d9207f…`, 11.087 bytes) en `b65dd59b` | Sí: un número distinto aparece en el cotejo | PASS, cotejo a mano, no con script |
| 3 | Para escribir esto no se calculó ni se leyó ningún estimando de A1 | no se abrió ningún `bloque_KK.jsonl` ni `ensayos.log`; de la corrida solo se leyeron `RESULTADO.txt` y `juntar.log`, que son técnicos | No: lo declara el productor y nadie lo puede comprobar | DECLARADO, no medido |
| 4 | La lectura del sobre quedó fijada antes de abrirlo | este commit, anterior a cualquier commit de estadística o de lectura de A1 | Sí: el orden de commits lo muestra | PASS al commitear |

## 4. Evidencia cruda (verbatim)

Cotejo en brain-env. Columnas: archivo, bytes en raw, sha256 en raw, bytes locales y comparación. `RESP` es la respuesta 006 en `main`.

```
LOCAL: ['__pycache__', 'comparar_corrida_a1.exit', 'comparar_corrida_a1.log', 'comparar_corrida_a1.py', 'control_negativo_corrida.log', 'juntar_prueba.log', 'plan_prueba.log', 'testigos_contra_si_mismo.log', 'workflow_sintaxis.log']
README.md 4248 10915a936aed0c5b0ecf8e502cc756e5caf921897dbe41139580ce39e111f8e7 -1 SIN_LOCAL
plan_prueba.log 1080 b301a1a1233f28ae8c35c5b0e15efef99ad46db9f4c60d661b75b993411827f0 1080 IGUAL
juntar_prueba.log 2486 0973bf60d6519f0be9fdaa8cdfeca70e8619d8e83324560ec6642e2c363d287c 2486 IGUAL
testigos_contra_si_mismo.log 314 34ef0ae08a2f31b53c02a5e68e08e6459180930c0b1696521b4d17917e7a4285 314 IGUAL
workflow_sintaxis.log 1238 1661f4074b0e9804d0e49bd4ae272b5047e1cddd020a0cbe0fc2f3514c06a18a 1238 IGUAL
comparar_corrida_a1.py 7342 113713c30e9ed4328d9ea028b0c2a9fb7766b6cb2c8c1653d7563ab25dcf0f88 7342 IGUAL
comparar_corrida_a1.log 1014 8f06d31c6d9dd0c883e552bb5c03a90a18372fbc0c53107b96728c3d70201eb8 1014 IGUAL
comparar_corrida_a1.exit 2 9a271f2a916b0b6ee6cecb2426f0b3206ef074578be55d9bc94f6f3fe3ab86aa 2 IGUAL
control_negativo_corrida.log 1209 6bb5b623edd4a49c1999108e43498cda8fcce419a12618be031dbee424d5ad5c 1209 IGUAL
RESP 11087 d6d9207ff403bf18560746b9fbb3397fe09e3c7c574b253b6e7de4df52a4f032
```

## 5. Archivos

- `docs/agents/respuestas/2026-11-03-007-en-criollo-que-tenemos-potencial-y-alcance.md`, este archivo, en `main`.
- Sin código, sin evidencia aparte de la de arriba y sin cambios en la rama.

## 6. NO MEDIDO

- Los estimandos, intervalos y veredictos de A1: el sobre sigue cerrado.
- La potencia con n = 20, BANC dentro del modelo, la composición de reglas y la mosca viva.
- La ventaja de estas piezas contra pares artificiales del mismo tamaño, y su valor comercial.
- El CONTEXTO, que sigue sin 005, 006 ni esta.
- La sección 15 de la página maestra.
- Si el token de Zenodo de octubre ya está revocado: el CONTEXTO lo sigue listando como pendiente.

--- METODO PROMETEO ---
Modo: LIGERO (síntesis en criollo, sin instrumento científico nuevo). Rol: lectura e interpretación del mismo productor de 005 y 006; no es una revisión independiente.
Máquinas: brain-env (cotejo sha256 de la evidencia de 006) y GitHub MCP (lecturas y este commit).
Artefactos: este archivo y la página 2026-11-03-007 del Doc Topo inverso.
QA: la rúbrica no se aplica en modo ligero; hechos, opinión y NO MEDIDO van separados.
