# 2026-11-02-007 · La evaluación externa acierta en lo grueso, pero se quedó en H_REUSO_ESTRICTO

**Veredicto.** Bien en lo grueso: el proyecto es un banco de ingeniería inversa con nulos y falsadores, no un cerebro ni una gramática, y el abismo que falta es G1 contra G0 en una tarea ciega. Pero la evaluación se quedó en H_REUSO_ESTRICTO, infla tres cosas (el p, el alcance del nulo y la ventaja con pocos datos) y no ve lo de hoy: **en el modelo, el motivo anatómico S→X→D no es el camino que hace el trabajo.** S→X directo carga solo 23 a 49 % del freno, y con LC4 el 40,6 % del freno de X viaja de salida a salida por una sola fila, DNp04→PVLP010⊣D.

Doc: https://app.clickup.com/90171457413/docs/2kza6fw5-26157/2kza6fw5-29397

## 1. Pedido

Abraham pegó una evaluación del proyecto sin pedido explícito (2-nov-2026, 17:05 ART). Interpretación declarada: contrastarla con el repo y decir qué se sostiene.

## 2. Herramientas declaradas

- brain-env (gateway python): lectura de docs/agents/CONTEXTO-drosophila-fep.md en main (sha256 64b5f6f38c3c6e1d…, 131.355 bytes) con búsqueda de patrones. Sin escrituras.
- GitHub MCP push_files: este archivo.
- ClickUp: página 2026-11-02-007 en el Doc Topo inverso.

## 3. Qué se contrastó

| Lo que dice el texto | Lo que dice el repo | Veredicto |
|---|---|---|
| El último hito es H_REUSO_ESTRICTO | Después vinieron H_REUSO_CIERRE (SOSTENIDA en FlyWire y BANC, 2026-11-02-001), H_MECANISMO (MIXTA en el modelo, 004) y H_MECANISMO_DNp04 (SOSTENIDA_EN_MODELO, 006) | desactualizado |
| «Demostración matemática y estadística» | Evidencia estadística contra un nulo explícito; no hay demostración matemática | inflado |
| 400 nulos y p = 0,0199 | Cero superaciones por prueba: p = 1/201 (200 nulos por prueba) y Holm = 4/201 = 0,0199. Es el piso que permite ese número de nulos, no un p fino | número bien, lectura imprecisa |
| No es azar ni distribución de grados o superclases | El nulo conserva filas y pesos salientes por origen y clase/lado; no conserva fuerza entrante, vecinos únicos, tipo fino ni geometría. En FlyWire el exceso es de proporción y reuso, no de cantidad | vale solo contra ese nulo |
| Inhibición de avance S→D más S→X→D | En la anatomía sí. En el modelo, S→X directo carga 23 a 49 % del freno (ΔSX/ΔX 0,289 / 0,260 / 0,232 / 0,487); con LC4 el freno principal es recurrente: cortar DNp04→PVLP010 suelta el 40,6 % del freno de X | la forma es de avance; el mecanismo dominante en LC4, no |
| El embudo mantiene ventajas con pocos datos | La ventaja sellada de H_PARES_DATOS es agregada, no universal: en c2 el lector crudo alcanza o supera al embudo desde n = 96, y PCA desde n = 768 | parcial |
| Compresión no es eficiencia de cálculo (Shuvaev) | Respuesta 2026-11-01-004: Shuvaev comprime una inicialización que luego se expande, sin demostrar ahorro de ejecución | correcto |
| El abismo es G1 contra G0 en tarea ciega | G1 sigue sin diseño, implementación ni corrida; una ventaja funcional, de compresión o de novedad sigue NO MEDIDA | correcto |
| Núcleo de una IA neuromórfica que resuelve el cuello de botella de los Transformers | Ninguna medición del repo lo toca | especulación, NO MEDIDO |

**Qué cambia para la gramática.**

- MEDIDO modelo: el proxy anatómico (espigas por sinapsis) predijo el efecto causal donde un relevo domina y falló en 3 de 7 pares donde el freno se reparte. Una gramática que solo describa cableado no alcanza para asignar roles: necesita la dinámica.
- MEDIDO modelo: con LC4 el freno es inhibición recurrente entre descendentes. Regla candidata nueva para G1: D→X⊣D' (una salida frena a sus vecinas a través de un relevo), además del motivo S→D más S→X→D.
- NO MEDIDO: que esa regla sirva fuera del modelo, en la mosca o en una tarea.

## 4. Evidencia cruda verbatim

Líneas del CONTEXTO de main (sha256 64b5f6f38c3c6e1d…), tal como las devolvió la búsqueda:

- «Cero superaciones en cada prueba; p = 1/201, Holm = 4/201 = 0,0199004975, no p = 0.»
- «en FlyWire el exceso ESTRICTO es de proporción y reuso, no cantidad: 880 pares con plantilla reales frente a 932…»
- «No conserva vecinos únicos tras agregar duplicados, fuerza entrante, tipo fino ni geometría; […] El control no demuestra causalidad, función, gramática ni ahorro.»
- «la ventaja sellada de H_PARES_DATOS es agregada, no universal. En c2, el lector crudo alcanza o supera al embudo desde n = 96; PCA, desde n = 768.»
- «Shuvaev comprime una inicialización que luego se expande, sin demostrar ahorro de ejecución.»
- «conserva su candidatura anatómica frente al nulo por clase/lado/signo/rol con S→D fijo, no una gramática funcional ni ventaja sobre G0.»
- «G1 sigue sin diseño, implementación ni corrida.»
- «Una ventaja funcional, de compresión o de novedad de la propuesta sigue **NO MEDIDA**.»
- «S→X directo carga solo 23 a 49 % del freno (ΔSX/ΔX 0,289 / 0,260 / 0,232 / 0,487, debajo de 0,5 en los cuatro)»

De la respuesta 2026-11-02-006 (agregar_stdout.log de run 41481727412):

```
PROXY_VEREDICTO PROXY_PARCIAL 4/7
H_MECANISMO_DNp04 SOSTENIDA_EN_MODELO r_Q1=0.4056 r_Q2=0.7456 s4=0.9677
```

## 5. Archivos generados

Este archivo, en main. Doc: página 2026-11-02-007 del Doc Topo inverso.

## 6. NO MEDIDO

- No se corrió nada nuevo: es un contraste de texto contra el repo.
- El suplemento de Shuvaev sigue sin leer.
- El CONTEXTO todavía no incluye la 006 ni esta lectura.

```
--- METODO PROMETEO ---
Accion delicada: NO
Modo aplicado:   LIGERO
Maquina:         brain-env (lectura del CONTEXTO de main)
Rubrica:         N/A (modo ligero)
N/A declarados:  todos (modo ligero)
Review externo:  no pedido
Instrumento:     busqueda de patrones sobre CONTEXTO-drosophila-fep.md de main, lineas citadas verbatim
Artefactos:      docs/agents/respuestas/2026-11-02-007-evaluacion-externa-contrastada.md + Doc https://app.clickup.com/90171457413/docs/2kza6fw5-26157/2kza6fw5-29397
```
