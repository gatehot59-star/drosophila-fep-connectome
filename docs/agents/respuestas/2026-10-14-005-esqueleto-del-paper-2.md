# 2026-10-14-005 · El esqueleto del Paper 2: una pregunta, cinco resultados medidos y dos huecos para H_CONSENSO y H_TAU

**Pedido.** 14-oct 11:22: «antes cerremos paper 1 v2 y el paper 2». 12:13: ClickKit `esqueleto_paper2_004` («Armá el esqueleto del Paper 2»).

## Veredicto primero
- **[HECHO] El esqueleto está en git:** `docs/paper2/paper2-esqueleto.md`, rama `titan/paper2-esqueleto-2026-10-14`, commit `753d4d5` (desde main `955dfc1`). No tiene PR. Es un esqueleto, no un borrador para enviar.
- **[CONCLUSIÓN] La pregunta es una sola:** ¿el cableado exacto de la mosca carga la función del reflejo de escape, más allá de su diseño y de sus barajados, y esa parte se conserva en otra mosca?
- **[MEDIDO, transcripto] §3.1 a §3.5 llevan números, cada uno con su respuesta fuente:** 2026-10-12-018, 2026-10-13-007, 2026-10-13-010, 2026-10-14-001 y 2026-10-14-002.
- **[MEDIDO] Cotejo:**
  - 73 de 74 cadenas numéricas del esqueleto aparecen tal cual en su respuesta fuente.
  - La que falta (`291/564`) está en `results/banc_2026-10-14/emparejar_banc.log`, línea 21.
  - Las cuatro cifras de «5 sinapsis o más» (4,0; 20,6; 43,3; 79,0 %) están en las líneas 24 a 27 del mismo log.
- **[PENDIENTE]** §3.6 H_CONSENSO y §3.7 H_TAU son huecos; los dos están corriendo desde las 11:30 (2026-10-14-004). Los dos desenlaces de H_CONSENSO quedan escritos de antemano en el esqueleto.
- **[NO MEDIDO] Bloquean un borrador:**
  - el nulo del emparejado BANC (sin él, §3.5 no se escribe como resultado);
  - la revisión de literatura del hueco funcional;
  - la ecuación y el modelo de entrada exactos, que salen del código sellado;
  - las figuras, con script commiteado;
  - las referencias verificadas una por una.
- **[CONCLUSIÓN, recomendación] Alcance:** el control de las salidas (2026-10-10-005 a 009), LC6→GF y sel_post salieron de la v2 «para el Paper 2» (V2-CIERRE.md). Recomiendo dejarlos para un Paper 3 estructural: son otra pregunta, con otros nulos. Decide Abraham.
- **[CONCLUSIÓN]** El negativo de las líneas etiquetadas (2026-10-12-012 y 013) entra como §3.8: la tarea mal etiquetada daba NO PAGA, y corregirla con la literatura es lo que hizo pagar al cableado.

## Herramientas y máquina
- GitHub (conector): `create_branch` y dos `push_files` (el esqueleto en la rama titan; esta respuesta en main).
- brain-env (CPU): lectura de los veredictos de 2026-10-12-015 a 2026-10-14-002, el cotejo de números (`cotejar.py`, sin commitear porque es un chequeo de una vez sobre texto) y la prueba del parche en una copia.

## Qué se midió
Nada del experimento: es un trabajo de escritura. Lo único medido es el cotejo de cada cifra contra su fuente.

## Evidencia cruda
```
cotejar.py: FALTA 2026-10-14-002 :: 291/564 | FALTAN 1 (de 74)
emparejar_banc.log:21 RESUMEN entradas con pareja fafb_match=291/564 (51.6 %) alguna=363/564 (64.4 %)
emparejar_banc.log:24-27 en_BANC_5 = 4.0 / 20.6 / 43.3 / 79.0 %
parche: md5 antes b0d8d742 -> despues 5f3fbff6; segunda aplicacion ABORTA
```

## Archivos
- Rama `titan/paper2-esqueleto-2026-10-14`: `docs/paper2/paper2-esqueleto.md`.
- Esta respuesta.
- `tools/contexto/actualizar_contexto_2026-10-14-005.py`: md5 `8a66dbe2`.
- `.github/workflows/contexto-2026-10-14-005.yml`.
- Doc público: https://app.clickup.com/90171457413/docs/2kza6fw5-22157

## NO MEDIDO
- H_CONSENSO y H_TAU.
- El nulo BANC.
- La literatura del hueco funcional.
- Las figuras.

## Antes de firmar
| Afirmación | Instrumento | ¿Podía dar rojo? | Veredicto |
|---|---|---|---|
| Los números del esqueleto son los de git | `cotejar.py`, búsqueda literal en la fuente citada | Sí: marcó 1 FALTA, que se resolvió en el log | PASA |
| No se inventaron resultados para 3.6 y 3.7 | Lectura: los dos dicen PENDIENTE | Sí, si tuvieran cifras | PASA |
| El parche no rompe el CONTEXTO | Prueba en copia con md5 y doble aplicación | Sí, aborta si un ancla no es única | PASA |
| La tabla de BANC es un resultado | Falta el nulo | — | NO: queda marcada como bloqueada |

--- METODO PROMETEO ---
Accion delicada: no (escritura en una rama titan sin PR; nada corrido ni mergeado).
Maquina: conector GitHub + brain-env CPU.
Artefactos: `titan/paper2-esqueleto-2026-10-14` `753d4d5`; esta respuesta en main; Doc https://app.clickup.com/90171457413/docs/2kza6fw5-22157
