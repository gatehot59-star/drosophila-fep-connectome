# 2026-11-03-009 · Verificador independiente de 009-A1: orden lista para otro agente y ensayo general medido en brain-env, con 010 tal cual y el sobre cerrado

**Veredicto del pedido («Dejá 010 tal cual y prepará el verificador independiente»).**

*   **010 queda tal cual:**
    *   no hay enmienda;
    *   la regla del BCa degenerado de 010 §7 sigue;
    *   `estadistica_a1.py` no cambia (5c9492ff).
*   **El verificador quedó preparado como orden para otro agente, y BRAIN no lo escribe.** Lo dice el docstring de `validar_a1.py` desde 005. Además, W-01 pide que elija qué medir alguien que no escribió el productor.
*   **La orden ya trae su ensayo general:** un sobre sintético con la estructura del manifiesto real. En brain-env, sobre los bytes publicados, pasó 13 de 13 y mató 7 de 7 mutantes.
*   **El sobre real sigue cerrado.**

**Lo que encontró el ensayo de paso**

*   **Hay seis huecos medidos.** El control del productor (`validar_a1`) no ve estas corrupciones:
    *   `cuenta_x` o `cuentas_G` que no coinciden con `cuentas_mirar`;
    *   una cuenta negativa;
    *   un `runner_version` distinto;
    *   `input_hashes` alterado;
    *   `espigas_total` menor que la suma.
*   **Dos de ellas mueven estimandos sin que nadie lo marque:**
    *   `B|R15|c_X`, de 0,8973 a 0,8853;
    *   `A|R16|DQ4`, de 34,9 a 34,5 Hz.
*   **Una mueve un veredicto.** Si se invalida `B|H4b`, P_T2_B pasa de SOSTENIDA a INVALIDO_TECNICO.
*   **En la corrida real no hay indicio de que pase.** El runner arma esos campos desde el mismo arreglo de cuentas. No se corrige el control ahora porque ya validó la corrida. Lo cubre la fase T7 del verificador.

## 1. Pedido

«Dejá 010 tal cual y prepará el verificador independiente» (3-nov, 18:36). Contestaba a la pregunta de la 008: ¿se deja 010 como está o se escribe una enmienda antes de abrir?

Interpretación:
*   no enmendar 010 ni tocar `5c9492ff`;
*   dejar listo el verificador distinto del productor de 010 §9 sin abrir el sobre.

Como el productor es de BRAIN, preparar quiere decir tres cosas:
*   una orden que otro agente pueda ejecutar sin preguntar;
*   un ensayo general ya corrido;
*   la medición de los huecos del control del productor.

## 2. Herramientas

*   **brain-env (oficial):** por MUDH Gateway/build. Host `6c09d8604b07`, `/usr/local/bin/python3` 3.12.14, NumPy 2.5.3 y SciPy 1.18.1.
*   **Taller sin red:** sólo para desarrollo, con un manifiesto de juguete armado con la forma medida del real. No es evidencia.
*   **GitHub MCP:** lectura de 010, del runner y del control; push a la rama y a `main`.
*   **API pública de GitHub desde brain-env:** para ver qué workflows disparó el push.
*   **ClickUp:** el Doc espejo.

## 3. Qué se midió

| Afirmación | Instrumento | ¿Podía dar rojo? | Veredicto |
| --- | --- | --- | --- |
| Los bytes probados son los publicados | sha256 de raw en `801487ca`, contra el taller y contra las huellas previas | sí | PASA, 8 de 8 IGUAL |
| El generador es determinista | S01: dos generaciones comparadas byte a byte | sí, M03 lo rompe | PASA |
| No escribe en una ruta de corrida | S02 | sí | PASA, exit 2 y nada escrito |
| El limpio pasa el control del productor con el manifiesto real | S03 | sí, M01 y M02 lo rompen | PASA: 8.540 recibos, 0 fallos |
| El control marca exactamente las 13 corrupciones detectables | S04 | sí, M05 y M07 lo rompen | PASA, 15 pares de 15 |
| El control no ve las 6 ciegas | S05 | sí | PASA; el hueco quedó medido |
| Global: una línea ilegible, sin celda | S06 | sí | PASA |
| La estadística del productor es determinista sobre el sintético | S07, dos corridas | sí | PASA, `bf8e90b8…` en las dos |
| Invalidación según D13 | S08 | sí | PASA, 13 celdas |
| D4: los ids inválidos no corren el flujo | S09 | sí, M06 lo rompe | PASA: 450 intervalos idénticos y 2 contaminados por las ciegas |
| Global invalida las 44 celdas | S10 | sí | PASA |
| La trampa sale como dice 010 | S11 | sí, M04 la rompe | PASA: B\|R02 y B\|H3 DEGENERADO, P_T1_B SIN_DECIDIR |
| Cada rama sembrada aparece en el agregado | S12 | sí | PASA, 21 de 21 |
| Registro de 722 ids igual en los tres escenarios | S13 | sí, M06 lo rompe | PASA, `7c6dadc1…` |
| La prueba puede dar rojo | 7 mutantes | sí, un mutante vivo es un rojo | PASA, 7 de 7 muertos |
| Mutantes de la 008 en brain-env | `mutantes_estadistica_a1.py` | sí | PASA: 28 de 28, control 21/21 |
| El push no disparó la corrida | API de runs | sí | PASA: sólo corrió H4 integrated regression (run 41728204681, success) |
| La orden cita bytes exactos | sha256 de raw de 010, 009, el sello, la 008, el manifiesto, SHA256SUMS, la validación, RESULTADO y HUELLAS | sí | PASA, en `descarga.log` |

## 4. Evidencia cruda

Está en `docs/agents/evidencia/2026-11-03-009-verificador-a1/`:
*   `descarga.log`, `prueba.log`, `mutantes.log`, `estadistica_limpio.log` y `mutantes_008_brain_env.log`. Son byte a byte iguales a los de brain-env; el README trae su sha256.
*   Del sucio y el global, el README trae sólo las líneas VALIDACION y VEREDICTO, con el sha256 de los logs completos.

## 5. Archivos

*   **Rama `titan/a1-runner-2026-11-03`, commit `801487ca`:**
    *   `tools/a1/sobre_sintetico_a1.py`;
    *   `tools/a1/prueba_sobre_sintetico_a1.py`;
    *   `tools/a1/mutantes_sobre_sintetico_a1.py`.
*   **`main`:**
    *   la orden, en `docs/agents/ordenes/2026-11-03-009-verificador-independiente-a1.md`;
    *   esta respuesta;
    *   la evidencia;
    *   una adenda al final de la 008.
*   **brain-env:** `/workspace/a1/v2/evid9/`, con los sobres sintéticos, los agregados, los logs y los mutantes.

## 6. NO MEDIDO

*   **Estimandos reales:** ninguno; el sobre sigue cerrado.
*   **El verificador independiente:** no existe hasta que otro agente lo escriba.
*   **Los huecos del control en la corrida real:** no medido, porque no se leyeron recibos.
*   **La trampa en la corrida real:** es una inferencia.
*   **El sobre sintético en otra versión de NumPy:** el generador sólo usa `PCG64.random()`, pero no se corrió en otra versión.
*   **El modelo sembrado:** aproxima Poisson, y con tasas muy chicas sesga hacia abajo. B\|R05 sembró 0,05 Hz por neurona y dio un DQ2 de 0,8 Hz poblacional. Toca el diseño del ensayo, no al productor ni al verificador.
*   **Pendientes:**
    *   CONTEXTO desactualizado (003 a 009);
    *   la sección 15, que espera el pegado de Abraham;
    *   los issues de la deuda de QA, sin abrir.

## 7. Para lanzar al verificador

Texto para pegar en otra instancia:

> Ejecutá la orden `docs/agents/ordenes/2026-11-03-009-verificador-independiente-a1.md` del repo `gatehot59-star/drosophila-fep-connectome` (rama `main`). No sos BRAIN. No abras `results/a1_2026-11-03/corrida_1/` hasta que Abraham lo autorice por escrito. Empezá por el ensayo general de la sección 7 y commiteá tu verificador con evidencia cruda antes de pedir la apertura.

## QA

El tipo de entrega es una orden para otro ejecutor con un instrumento de diagnóstico. Aplican cuatro criterios que suman 45 puntos. Quedan 55 puntos N/A (Seguridad, Testing, Arquitectura, DevOps e Innovación), porque la tabla de PROMETEO-QA no los asigna a esos dos tipos. Las pruebas del kit cuentan como evidencia de Ejecutabilidad.

| Criterio | Puntos | Evidencia |
| --- | --- | --- |
| Completitud | 14/15 | La orden trae §0 a §10 y los anexos A a C; el kit son 3 archivos sin placeholders en `801487ca`. Resta 1 por dos cosas: el cotejo de D′ contra la evidencia de 010 queda como opcional, sin medir su formato, y la lista de los 722 ids no está en git, sólo su regla y su sha256. |
| Ejecutabilidad | 15/15 | Desde los bytes de raw en brain-env: la prueba dio 13/13 con exit 0 (22:09:53Z a 22:10:58Z) y los mutantes 7/7 con exit 0 (22:19:15Z). |
| Documentación | 9/10 | Esquemas, fases, ensayo y apertura, con los seis campos y el Doc espejo. Resta 1 porque la orden es larga (33 KB) y CONTEXTO sigue 7 respuestas atrasado. |
| Proceso QA | 5/5 | Cada puntaje cita commit, archivo, sha256 o log. |

**Total: 43/45, o sea 96/100.**

Doc: página 2026-11-03-009 en Topo inverso, https://app.clickup.com/90171457413/docs/2kza6fw5-26157

--- METODO PROMETEO ---
Accion delicada: SI (emite una orden dirigida a otro ejecutor)
Modo aplicado:   FULL
Maquina:         brain-env sobre los bytes de 801487ca bajados de raw; taller sin red sólo para desarrollar
Rubrica:         43/45 -> 96/100
N/A declarados:  55 (Seguridad, Testing, Arquitectura, DevOps, Innovacion: orden más instrumento)
Review externo:  la orden lo pide al verificador; hasta que lo haga es deuda
Instrumento:     prueba_sobre_sintetico_a1.py (exit 0) y mutantes_sobre_sintetico_a1.py (exit 0) en brain-env; evidencia en docs/agents/evidencia/2026-11-03-009-verificador-a1/
Artefactos:      docs/agents/respuestas/2026-11-03-009-verificador-independiente-orden-y-ensayo-general.md + https://app.clickup.com/90171457413/docs/2kza6fw5-26157
