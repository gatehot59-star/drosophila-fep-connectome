# 2026-10-14-050 · H_ENTERA_UMBRAL sellada: un umbral que deja 321 neuronas activas en cada grafo

**Fecha:** 2026-10-16, 10:30 (America/Buenos_Aires)
**Sello:** `tools/mosca_entera/SELLO-UMBRAL-050.md` en `titan/mosca-entera-2026-10-15` (commit `868ded6`, md5 680abca839bd6c80367c9b434af7d800)
**Doc:** https://app.clickup.com/90171457413/docs/2kza6fw5-23557

## Pedido

Botón `sellar_umbral_050` de Abraham (16-oct), sobre la propuesta de la 049.

## Veredicto primero

- **[MEDIDO] El sello está en git antes del instrumento** (`868ded6`). Nada de UMB corrió; no hay un solo número nuevo.
- **[CONCLUSION] Qué se prueba.** La 049 dio el conjunto de Shiu SOSTENIDO y MN9 REFUTADA. El LIF prende 321 neuronas; la tasa con tanh, 48.407. El brazo UMB es la misma dinámica TASA con tanh(max(0, Wz + x − θ)) y un θ global calibrado en cada grafo para que queden 321 activas: el real a radio 0,9 y los mismos 80 nulos de la 049 con el factor del real (G1).
- **[CONCLUSION] Hipótesis.** H_UMB_MN9 y H_UMB_CONJUNTO con las bandas de la 046. H_UMB_GANA: J(UMB) − J(TASA) ≥ +0,05 SOSTENIDA, ≤ 0 REFUTADA. Controles: CALIB_REAL (321 ± 32) y TASA_049 (J 0,3659574468 ± 1e-9).
- **[CONCLUSION] Lectura fijada.** MN9 SOSTENIDA: la falla de la 049 era la no linealidad, no el cableado, y con CONJUNTO SOSTENIDA se puede sellar la destilación. MN9 REFUTADA con r = 0: el reflejo del LIF depende de algo que la tasa no tiene. REFUTADA por nulos: el umbral no es específico. SIN_DECIDIR: no se agregan nulos después de ver.
- **[CONCLUSION] Expectativa escrita:** H_UMB_MN9 REFUTADA con r = 0 (70%), H_UMB_CONJUNTO SOSTENIDA (85%), H_UMB_GANA incierta (50%).
- **[MEDIDO] Corrección de la 049.** La lectura de la ventana no depende de τ: es el punto fijo (J idéntico a 16 cifras en los 10 τ de CORRER). Por eso el humo de la 049 con τ 99 ya mostró el brazo real antes de CORRER (MN9 0,00202666, el mismo valor). Las bandas estaban selladas desde la 046 y la 048 y no cambiaron, pero la frase «semillas fuera de CORRER» no escondía el real. El humo de UMB corre el real con otro estímulo.

## Herramientas y máquina

Sandbox de ClickUp para escribir; GitHub MCP para los pushes; brain-env para la prueba del parche del CONTEXTO. Nada corrido para UMB.

## Archivos

| Archivo | md5 |
|---|---|
| `tools/mosca_entera/SELLO-UMBRAL-050.md` (rama) | 680abca839bd6c80367c9b434af7d800 |
| `tools/contexto/actualizar_contexto_2026-10-14-050.py` (`main`) | 054c7e3079ce90553f7270378fbe5384 |

## NO MEDIDO

- Todo veredicto de H_ENTERA_UMBRAL.
- El tiempo de la calibración: estimado unos 30 min de pared en 8 trabajos.
- Que Activas(θ) baje en forma monótona con θ: con inhibición puede saltar; por eso la tolerancia de ±32 y el conteo aparte de los nulos que no calibran.

## Antes de firmar

- **¿El sello puede dar rojo?** Sí: MN9 en cero o 5 nulos iguales o mayores refutan H_UMB_MN9; H_UMB_GANA refuta con diferencia ≤ 0.
- **¿Se movió el arco?** No: el sello 046 y la enmienda 048 no cambian, y los veredictos de la 049 quedan como están.
- **El parche del CONTEXTO** se probó en brain-env sobre una copia de `main` en `caf6469` (d85cad07 a 28cf15fc; la segunda pasada aborta sin escribir).
- **El CONTEXTO de la 049 quedó verificado** desde un clon nuevo: bot `caf6469`, md5 d85cad07, workflow borrado. En la 049 no se había probado antes sobre una copia; aplicó igual.

--- METODO PROMETEO ---
Rol: implementa (sello). Delicado: no.
Máquinas: sandbox de ClickUp, brain-env (prueba del parche).
Archivo: `docs/agents/respuestas/2026-10-14-050-sello-umbral-calibrado-al-presupuesto-del-lif.md` en `main`.
Doc: https://app.clickup.com/90171457413/docs/2kza6fw5-23557
