# 2026-10-12-012: líneas etiquetadas no pagan; la auditoría externa de la 011 tiene errores propios

**Doc espejo:** https://app.clickup.com/90171457413/docs/2kza6fw5-21517
**Rama:** `titan/lineas-etiquetadas-2026-10-12`: sello `debfd05` (script md5 `b9c139c8c17894efaa5bfd9bb86c93ed`), logs `72b7fa4`. Sin PR.

## Veredicto (conclusión)

- [MEDIDO] Con líneas etiquetadas el cableado de la mosca **NO PAGA**: PIERDE en SILENCIOSA y MOVIMIENTO (Holm inferior 0,0399), EMPATE en COMO_LPLC2 (Holm 0,0797). 283 a 300 de 300 nulos la igualan o superan en cada celda.
- [MEDIDO] La regla a mano sobre las entradas crudas le gana 6 de 6 (0,6094 a 0,7894 contra 0,3383 a 0,3778; McNemar p ≤ 6e-62).
- [MEDIDO, descriptivo] En W, DNp01 responde más al acercamiento lento (0,9123) que a la amenaza (0,8092), y al objeto que pasa casi igual (0,7625).
- [MEDIDO, post hoc] Sin la respuesta de LPLC2 al punto (supuesto de la 005), W sube a 0,6206 y empata con SL; con ruido 0,45, 0,5989, empate.
- [CONCLUSIÓN] Lo que decide hoy no es la neurona ni el lector: es un supuesto de entrada no medido (LPLC2 al punto, amplitud 0,6).

## 1. Pedido

17:06: botón `correr_lineas_etiquetadas` (la 008). 17:37: Abraham pega una auditoría externa de la 011 con «versión mejorada» y una evaluación de «qué tenés en las manos».

## 2. Herramientas y máquina

brain-env: dos humos, la corrida completa desde un clon en el sello (2139,3 s) y el diagnóstico (148,1 s). Sandbox de ClickUp: escritura del script, prueba unitaria de la carrera (`[1 2 3 1 0]` esperado y obtenido) y reconstrucción de logs (md5 iguales: run.log `24fbe259bd7aaa4cbf3c8db85eef1fd9`, diag.log `fe211829cf7b30df3517f6dfa59989f3`). Web: Dorkenwald 2024 y Lappalainen 2024. Escrituras: la rama, este archivo y el Doc.

## 3. Qué se midió

Motivo de 28 de la 003, entrada por tipos de la 005, mismos 300 SL y 300 T, τ semilla 0, ruidos 0,15 y 0,45. Lector sin entrenar: DNp01 izq./der. → escape, DNp07 → aterrizaje si vuela, gana la primera línea que cruza. **Cambio declarado sobre la 008 tras el humo y antes del sello:** umbral = cuantil 0,95 del máximo de cada línea sobre los 800 ensayos de entrenamiento con el objeto que pasa. Motivo: en el humo (log md5 `4a8cc1ae3e3ab98b637584486a6ebd09`) con umbral de sólo ruido el objeto que pasa cruzaba siempre y la regla a mano fallaba su control positivo. En la corrida completa, la 008 literal (descriptiva) da W 0,2883 a 0,3378 con falsa alarma 0,935 a 1,000.

| Variante | Ruido | W | SL media | T media | Regla | Veredicto |
|---|---|---|---|---|---|---|
| COMO_LPLC2 | 0,15 | 0,3433 | 0,4261 | 0,3965 | 0,7894 | EMPATE |
| COMO_LPLC2 | 0,45 | 0,3672 | 0,4211 | 0,4029 | 0,7300 | EMPATE |
| SILENCIOSA | 0,15 | 0,3472 | 0,4532 | 0,4337 | 0,6094 | PIERDE |
| SILENCIOSA | 0,45 | 0,3778 | 0,4721 | 0,4379 | 0,6228 | PIERDE |
| MOVIMIENTO | 0,15 | 0,3383 | 0,4799 | 0,4804 | 0,6239 | PIERDE |
| MOVIMIENTO | 0,45 | 0,3583 | 0,4710 | 0,4701 | 0,6322 | PIERDE |

Controles: negativo AGNOSTICA 30/30 idénticos; positivo 0,7894 ≥ 0,60; reproduce True; guardas True → VALIDO. Logs completos: `results/lineas_etiquetadas_2026-10-12/run.log` y `diag.log` en la rama.

## 4. La auditoría externa de la 011

**Se acepta:** distinguir `AutoDiffAdjoint` (gradiente exacto de la solución discretizada) de `BacksolveAdjoint` (ahorra memoria, error numérico); etiquetas MEDIDO/CONCLUSIÓN (aplicadas arriba); definir ADR; «octopamina sin clase» en la 011 quería decir sin signo **en el mapeo DCMT**.

**Se rechaza, verificado:** la 011 no usa 140.000 ni 127.400 (usa 138.005 y 139.248; FlyWire: 139.255 neuronas y 54,5 M sinapsis, Dorkenwald 2024; Shiu: «more than 125,000»); el veredicto de la 011 no dice «tiempo discreto»; el 95% sale del análisis DCMT pegado, no de la respuesta 010; «166.000» sólo está en NO MEDIDO; **ADR es el Architecture Decision Record `docs/adr/2026-10-01-sparseltc-dbc3-adapter.md` de `mojo-absoluto`**, no «activity-dependent rate» (inventado); la octopamina **sí** es clase de `top_nt` en FlyWire (193 neuronas); el veredicto va primero por F-01.

**La evaluación infla:** la máquina de estados ganó a DBC3 y LSTM, no a un LIF; la líquida plena se validó en 26 neuronas, no en el conectoma completo; Shiu corre el cerebro entero, así que el 2,96% es un límite nuestro y no un mérito; FlyVis sí entrena («we then optimized the values of these unknown parameters using techniques from deep learning») y se valida contra 26 estudios de actividad medida; no tenemos validación biológica.

## 5. Propuesta (decide Abraham)

1. Resolver la respuesta de LPLC2 a objetos que se trasladan (literatura o datos) antes de más corridas.
2. Después, el motivo ampliado con inhibición.

## 6. Archivos

Este archivo; en la rama: `tools/escape_aterrizaje/lineas_etiquetadas.py`, `results/lineas_etiquetadas_2026-10-12/run.log`, `diag.log`. En brain-env sin commit: `resultados.json` (md5 `0ca277cd02dd9f07652500a0e977d791`, 89.766 B), `diagnostico_lineas.py` (md5 `16c234bc6b880389f594d2ff15f4512a`), humo.log y humo2.log (md5 `5d3c1b6fc23aaa1f64049df052ab1650`).

## 7. NO MEDIDO

D2 post hoc (50 nulos, sin Holm); fisiología de LPLC2 y LPLC4; motivo ampliado; DCMT; segunda máquina; cotejo raw del commit `72b7fa4` contra brain-env (los md5 de los logs se cotejaron en el sandbox). CONTEXTO sin reescribir.

--- METODO PROMETEO ---
Acción delicada: NO
Máquina: brain-env + sandbox de ClickUp + GitHub y web
Artefactos: docs/agents/respuestas/2026-10-12-012-lineas-etiquetadas-no-pagan-y-auditoria-de-la-auditoria.md + https://app.clickup.com/90171457413/docs/2kza6fw5-21517
