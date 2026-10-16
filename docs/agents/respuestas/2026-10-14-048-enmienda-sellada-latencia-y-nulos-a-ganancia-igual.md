# 2026-10-14-048 · Enmienda sellada de H_MOSCA_ENTERA: latencia y nulos a ganancia igual

**Fecha:** 2026-10-16, 00:52 (America/Buenos_Aires)
**Enmienda:** `tools/mosca_entera/ENMIENDA-048.md` en `titan/mosca-entera-2026-10-15` (commit `778dc10`, md5 022dbbdd87ce206e9f33efc62d8e7ee7)
**Doc:** https://app.clickup.com/90171457413/docs/2kza6fw5-23497

## Pedido

Botón `enmienda_mosca_entera_048` de la 047 (Abraham, 16-oct 00:48): «Sellá la enmienda y después CORRER».

## Veredicto primero

- **[MEDIDO] La enmienda está sellada en git antes de CORRER** (`778dc10`, 00:50). CORRER no corrió; no hay un solo número nuevo.
- **[CONCLUSION] Agrega, no mueve.** Las cuatro hipótesis de la 046 se corren y se reportan con sus bandas. Se suman tres cosas:
  - **Marca `REFUTADA_DEGENERADA`** para H_ENTERA_LIQ si LIQ y TASA dan lo mismo en la ventana (mediana de max|Δr| < 1e-6): ese veredicto no cuenta como evidencia.
  - **H_ENTERA_LAT:** Spearman entre la latencia del LIF (primera espiga, mediana sobre ensayos) y la del brazo (primer paso con z ≥ la mitad de su valor final), sobre las neuronas de S_LIF. D_LAT = mediana sobre τ 30 a 39 de ρ(LIQ) − ρ(TASA): ≥ +0,05 SOSTENIDA, ≤ 0 REFUTADA. Si con τ 30 menos del 1% de las neuronas cambia de latencia entre brazos, NO_MEDIDO.
  - **Nulos G1:** los mismos 80 nulos de la 046, escalados con el factor del real (0,9/r_real) en vez del propio, como hace el LIF con pesos crudos. H_ENTERA_MN9_G1 y _CONJUNTO_G1 usan las bandas de la 046.
- **[CONCLUSION] La lectura conjunta quedó fijada antes de ver.** Si MN9 pierde contra los nulos a 0,9 y gana contra los G1, la ventaja del real es ganancia concentrada en lazos, no ruteo hacia MN9. Es la fila que espero.
- **[NO MEDIDO] Todo veredicto.** Falta el instrumento de la enmienda, su prueba y su humo, y después CORRER.

## Herramientas y máquina

Sandbox de ClickUp para escribir; GitHub MCP para el push; brain-env para los md5 desde clon nuevo y la prueba del parche del CONTEXTO. Nada corrido para la enmienda.

## Archivos

| Archivo | md5 |
|---|---|
| `tools/mosca_entera/ENMIENDA-048.md` (rama) | 022dbbdd87ce206e9f33efc62d8e7ee7 |
| `tools/contexto/actualizar_contexto_2026-10-14-048.py` (`main`) | d6dbdc3fe1735f3cde1c059122a70b05 |

## NO MEDIDO

- Todo veredicto de H_MOSCA_ENTERA y de la enmienda.
- Que la latencia LIQ difiera de la TASA en el cerebro entero: la cuenta dice que sí (la compuerta depende de |Wz + u| en todas las neuronas), pero no se midió.
- Los radios de los nulos G1: esperados de ~0,11 y ~0,14 por los dos nulos del humo.

## Antes de firmar

- **¿La enmienda puede dar rojo?** Sí: H_ENTERA_LAT tiene banda de REFUTADA (D_LAT ≤ 0) y una precondición que la deja NO_MEDIDO si los brazos vuelven a ser iguales; las G1 tienen las bandas de la 046, que refutan con 5 nulos iguales o mayores.
- **¿Se movió el arco?** No: la enmienda no toca bandas ni brazos de la 046 y se escribió antes de CORRER. Lo visto en el humo está listado en la enmienda; ninguna latencia ni ningún nulo G1 se vio.
- **El parche del CONTEXTO** se probó en brain-env sobre una copia de `main` (9f4135e4 a 87ebfe56, la segunda pasada aborta sin escribir) con la hora 01:00; la versión subida sólo cambia esa hora a 00:52.
- **El CONTEXTO de la 047 quedó verificado** desde un clon nuevo de `main` (md5 9f4135e4, workflow borrado); en la 047 había quedado sin verificar.
- **Expectativa escrita:** LIQ degenerada casi seguro; D_LAT chico; G1 SOSTENIDA.

--- METODO PROMETEO ---
Rol: implementa (sello). Delicado: no.
Máquinas: sandbox de ClickUp, brain-env (md5 y prueba del parche).
Archivo: `docs/agents/respuestas/2026-10-14-048-enmienda-sellada-latencia-y-nulos-a-ganancia-igual.md` en `main`.
Doc: https://app.clickup.com/90171457413/docs/2kza6fw5-23497
