# 2026-11-03-008 · Estadística de 009-A1 escrita y probada sin abrir el sobre

**Veredicto del pedido.** El código de la estadística de 010 (§5 a §7) está escrito, probado y commiteado en la rama `titan/a1-runner-2026-11-03`, commit `5c9492ff3de94e6ec1f27fb970205a19687674a0`. La suite sintética pasa **23/23 en brain-env** contra el manifiesto real `267ca1d0`, corriendo los bytes bajados de raw (sha256 iguales a `HUELLAS_ESTADISTICA.sha256`). Los 8.540 recibos de la corrida 1 **siguen sin abrir**: ningún estimando real se calculó.

**Lo que hay que decidir antes de abrir.** El runner aplica cada máscara poniendo pesos en cero. Si Q1 apaga a x en las 20 semillas (en el humo de R01 B pasó de 30 a 0 y de 16 a 0), Q1 y Q2 dejan la red idéntica fuera de x, así que `Y(Q1) = Y(Q2)` semilla por semilla y `r_Q1 = 1` exacto en todos los remuestreos. El BCa queda DEGENERADO y 010 §7 manda SIN_DECIDIR para ese criterio: P_T1_B no pasaría justo con el efecto máximo. Lo mismo vale para `r_Q1conj` y `c_Xconj` si Q1conj apaga al hub (T2), y para `s4` si Q4 no cambia a x en ninguna semilla. El código sigue la letra de 010. Cambiarlo exige una enmienda escrita **antes** de abrir; la decisión es de Abraham. Este razonamiento sale de cómo el runner edita pesos y del humo ya publicado en 005, no de los recibos sellados (NO MEDIDO sobre la corrida).

## 1. Pedido
«arranca el codigo» (3-nov 15:18), respuesta a «¿Arranco con el código de la estadística de 010 §7, commiteado antes de tocar los recibos?». Interpretación: escribir la estadística de 010 §5 a §7, probarla con datos sintéticos que puedan dar rojo y commitearla antes de leer recibos. No correrla sobre la corrida: 010 §9 pide antes el verificador distinto del productor.

## 2. Herramientas
- Taller sin red (desarrollo): Python 3.12.15, numpy 2.4.6, scipy 1.18.0, manifiesto de juguete con la forma medida del real y stubs de los módulos del runner. No es evidencia oficial.
- brain-env (oficial): Intel Celeron N4020 (2 en cpuinfo, `nproc --all` 4), 7.989.580 kB de RAM con 1.263.212 kB disponibles, Python 3.12.14, numpy 2.5.3, scipy 1.18.1, kernel 4.19.0-27-amd64.
- GitHub MCP para empujar; ClickUp para el Doc.

## 3. Qué se midió (afirmación → instrumento → ¿podía dar rojo? → veredicto)
| Afirmación | Instrumento | Rojo posible | Veredicto |
|---|---|---|---|
| Los bytes probados son los subidos | sha256 de raw en 5c9492ff contra HUELLAS | sí, cualquier byte distinto | PASA, 3/3 OK |
| t unilateral correcta | E01 contra `scipy.stats.ttest_1samp(greater)` en 300 vectores | sí, el bilateral difiere 0,338 | PASA, dif 3,1e-16 |
| Inversión de signos exacta | E02 contra la enumeración directa de 2^20 signos | sí, la cuenta unilateral difiere | PASA, 6/6 cuentas iguales; piso 2/2^20 |
| Holm correcto | E03 contra Holm aparte y la regla secuencial, 500 vectores de 46 | sí, Bonferroni rechaza 1 donde Holm rechaza 2 | PASA, 0 diferencias |
| BCa igual al de scipy | E04, mismo flujo PCG64, 20.000 remuestreos, media y cociente pareado | sí, percentil difiere ≥ 2,4 % del ancho y BCa sin aceleración ≥ 2 % | PASA, dif 4,4e-15 del ancho |
| Estados INDEFINIDO, SIN_ESTIMADO, DEGENERADO | E05 | sí, el caso común da OK | PASA |
| Familias 46, 6 y 3 en posiciones fijas | E06 | sí, sin H3 aborta | PASA |
| Reglas de 010 sobre veredictos | E07 a E15, E19, E20, E22, E23 | sí, cada escenario cambia el veredicto esperado | PASA |
| Estimandos con la fórmula de 010 | E21, 23 estimandos recalculados aparte | sí, T2c con el máximo da 116,40 y no 238,95 | PASA, dif 0 |
| Lectura de recibos y mapeo de fallas | E16, 8.540 recibos sintéticos con basura fuera del D′ | sí, leer posiciones corridas cambia 44/44 celdas | PASA |
| Determinismo a 20.000 | E17 | sí, otra semilla cambia 622 intervalos | PASA, agregado idéntico |
| Guardas del CLI | E18 | sí | PASA: sin `--abrir-sobre` exit 2; sha mala exit 2; sin recibos exit 1 con 44 celdas inválidas |
| La suite ve errores plausibles | 28 mutantes de `estadistica_a1.py` | sí, un mutante vivo es un rojo | Taller: 27/28 y el vivo (M17) murió al reforzar E15. brain-env: en curso, NO MEDIDO al commitear |

Decisiones de implementación donde 010 no fija el detalle: D1 a D15, dentro del agregado. Las que el verificador tiene que mirar primero: **D1** (Holm usa el p observado también en casos NO_INFORMATIVO, porque si no la activación queda circular), **D8** (en A cada cociente exige su propio denominador positivo y con IC95 que excluye cero, como dice 010), **D12** (el índice de ablación no se implementa: su definición no está en 009, 010 ni el sello) y **D13** (una falla invalida su celda; una sin celda invalida las 44).

## 4. Evidencia cruda
Verbatim en `docs/agents/evidencia/2026-11-03-008-estadistica-a1/README.md`: bajada y huellas, entorno y las 25 líneas de la suite en brain-env.

## 5. Archivos
- Rama `titan/a1-runner-2026-11-03`, commit `5c9492ff`: `tools/a1/estadistica_a1.py` (36.891 B, 37ab63d7…), `tools/a1/prueba_estadistica_a1.py` (48.950 B, 74aec761…), `tools/a1/mutantes_estadistica_a1.py` (8.976 B, 86c5e4f7…), `tools/a1/HUELLAS_ESTADISTICA.sha256`.
- main: esta respuesta y su evidencia.
- brain-env: `/workspace/a1/v2/evid8/` con los logs completos y la corrida de mutantes.

## 6. NO MEDIDO
- Ningún estimando real: el sobre sigue cerrado.
- Mutantes en brain-env sobre los bytes finales: corriendo al commitear.
- Si `Y(Q1) = Y(Q2)` exacto ocurre en la corrida: es una inferencia del código del runner y del humo.
- Verificador independiente: falta. Actualización de CONTEXTO: falta. Sección 15 del Doc maestro: sigue esperando el pegado de Abraham.

## QA (módulo sin deployment propio; DevOps N/A, 10 puntos fuera del denominador)
Completitud 14/15 (−1 por D12). Ejecutabilidad 15/15 (23/23 desde raw en brain-env). Seguridad 13/15 (−2: entorno sin hashes de pip ni chequeo de CVE). Testing 14/15 (−1: mutantes en brain-env sin cerrar). Arquitectura 9/10 (−1: un archivo de 727 líneas). Documentación 9/10 (−1: líneas de más de 120 columnas y CONTEXTO atrasado). Innovación 5/5 (mutantes, BCa bit a bit contra scipy, estimandos recalculados aparte, guarda del sobre). Proceso QA 5/5. **84/90 = 93/100.** Deuda: issues sin abrir todavía.

Doc: página 2026-11-03-008 en Topo inverso, https://app.clickup.com/90171457413/docs/2kza6fw5-26157

--- METODO PROMETEO ---
Máquina: brain-env sobre los bytes de 5c9492ff bajados de raw; desarrollo en el taller sin red.
Código: https://github.com/gatehot59-star/drosophila-fep-connectome/tree/titan/a1-runner-2026-11-03/tools/a1
Respuesta: docs/agents/respuestas/2026-11-03-008-estadistica-a1-escrita-y-probada-sin-abrir-el-sobre.md
Doc: https://app.clickup.com/90171457413/docs/2kza6fw5-26157
