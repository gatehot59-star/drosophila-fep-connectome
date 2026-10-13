# 2026-10-13-006 · Factorial 2 corriendo en Actions; F01, F06 y F07 corregidos y probados, con el parche en cola en el PR #27

## Veredicto

- **[MEDIDO] El factorial 2 está corriendo.** El commit `9f8b848` pushea `results/factorial2_2026-10-13/CORRER` sobre el sello `9442fdf`, sin tocar el instrumento. Es la corrida `38396946950`, con 29 trabajos.
  - Estado a las 09:29 (12:29 UTC): **3 terminados con éxito** (ANCLA_015, M46_TASA y M46_LIQ, de 1:00 a 1:18 min), **20 corriendo** y **6 en cola** por el límite de 20 trabajos simultáneos.
  - **El resultado está NO MEDIDO**, y el bot lo commitea en la rama cuando termine.
- **[MEDIDO] F01, F06 y F07 corregidos y probados.** La prueba se hizo en brain-env sobre una copia de `f19a9c7`, la cabeza del PR #27.
  - **El parche:** `tools/v2/fix_v2_2026-10-13.py`, md5 `5299df9a…`. Hace 8 reemplazos, cada uno con exactamente una aparición: 5 en el manuscrito y 3 en la sección de dos saltos.
  - **El manuscrito** pasa de md5 `e5fb86dc…` a `2fa575c4…`, y la sección de dos saltos de `cbe02457…` a `23db9cac…`. Los metadatos de Zenodo no cambian.
  - **El render da PASS:** 14 de 14 cadenas en el manuscrito y 5 de 5 en el erratum, con dos compilaciones iguales. El PDF del manuscrito pasa de 17 a **18 páginas**, md5 `a22515e9…`. El del erratum no cambia: `05052e6e…`.
- **[MEDIDO] El parche está en el PR #27, pero el texto del PR todavía no cambió.**
  - El commit `07afb2b` sube la herramienta y un workflow que la aplica en Actions y se retira, igual que en la 018.
  - El workflow (corrida `38397952384`) quedó **en cola detrás del factorial**, que ocupa los 20 lugares. Se aplica solo cuando se libere uno.
  - No se mergeó ni se depositó nada.
- **[CONCLUSIÓN] Qué dice ahora cada punto:**
  - **F01:** el ensemble de neuropilo permuta destinos sólo entre conexiones del mismo bloque. El multiconjunto de destinos se conserva en cada bloque y por lo tanto en total, así que **preserva todo in-degree exacto**. Ya es el ensemble combinado de grado y neuropilo.
    - Se corrigió en la §3.4 y en la limitación 7, donde además sale "no combined degree-and-neuropil ensemble".
    - También en la sección de dos saltos, donde "a combined ensemble ... was not constructed" pasa a "is already a combined degree-and-neuropil ensemble".
  - **F06:** con N = 5 el p de permutación más chico posible, (r + 1)/(N + 1), es 1/6 ≈ 0,17. La limitación 2 ya no dice "Sufficient", y aclara que Z = +14,8σ se apoya en una aproximación normal con la varianza estimada de cinco valores, y que hacen falta N ≥ 20 para p < 0,05 y N ≥ 100 para p < 0,01. Como el "Sufficient" ya estaba en la v1.0 (texto del PDF, línea 449), entra como **cambio 15** en "Changes from version 1.0".
  - **F07:** cita 138.140, la corrida que produjo las Tablas 5b y 5c (evidencia cruda del 2026-08-25, la misma que tiene los cocientes 0,022797 y 7,364619), y nombra 138.142 como una segunda extracción independiente.
- **[CONCLUSIÓN] Lo que no se tocó:**
  - **F05**, el +14,8σ y el "survives the community-preserving control" del resumen, espera tu decisión. F06 no cambia el número.
  - **El docstring de `src/twohop_nulls.py`** en la rama de agosto sigue diciendo lo contrario de lo que hace el código.
  - **El erratum** no suma el "Sufficient" de la v1.0.

## Pedido

"correr el factorial 2 en Actions mintras tanto, arreglar F01/F06/F07 del paper" (13-oct, 09:22). La aprobación pendiente de la 005 no se tocó: sigue esperando tu decisión.

## Herramientas y máquina

- **GitHub MCP:**
  - `create_or_update_file` del CORRER en `titan/factorial2-mosca-2026-10-13`;
  - `pull_request_read` del PR #27;
  - `push_files` de la herramienta y el workflow en `titan/v2-cierre-2026-10-12`.

  No se mergeó nada.
- **brain-env:**
  - clones de `titan/v2-cierre-2026-10-12` (`f19a9c7`) y de `titan/materializacion-h4-guard-2026-10-02` (evidencia de agosto);
  - prueba del parche sobre una copia;
  - render con pandoc 3.10.2 y typst 0.15.0;
  - consultas a la API pública de Actions.
- **Actions:** la corrida del factorial y la del parche, que está en cola. Sin cuota ajena.

## Qué se midió

| Qué | Instrumento | Dato |
|---|---|---|
| Disparo del factorial 2 | API de runs | `38396946950`, 29 trabajos, head `9f8b848` |
| Avance a las 12:29 UTC | API de jobs | 3 completados con éxito, 20 corriendo, 6 en cola |
| De dónde sale el 138.140 | evidencia del 2026-08-25 (md5 `d2ea7615…`) | línea 52: `"nodes_with_in_degree_broken_by_uniform": 138140`; líneas 104 y 106: cocientes de la Tabla 5b |
| El "Sufficient" ya estaba en la v1.0 | `v1.0.txt` (texto del PDF v1.0) | línea 449: "2.N=5 for temporal CP.Sufficient for Z=" |
| El parche aplica limpio | `fix_v2_2026-10-13.py` sobre una copia de `f19a9c7` | 8 de 8 con una aparición; los controles positivo y negativo pasan |
| El manuscrito renderiza | `tools/v2/render_v2.py` | PASS, determinista, 18 páginas, md5 `a22515e9…` |
| El parche está en cola | API de runs de la rama del PR | `aplicar-fix-v2-2026-10-13` queued en `07afb2b` |

## Evidencia cruda

```
# disparo
commit 9f8b8486b423ca006bd18aaaad03771c6aa84dfc  results/factorial2_2026-10-13/CORRER
38396946950 factorial2-mosca queued None 9f8b848 2026-10-13T12:23:34Z
correr (ANCLA_015, ...) completed success 12:23:39 12:24:39
correr (M46_LIQ, ...)   completed success 12:24:00 12:25:18
correr (M46_TASA, ...)  completed success 12:23:38 12:24:45
(20 in_progress; queued: R1_SIN_LIQ_tb, R1_SIN_TASA_ta, R2_t0c1, R2_t1c5, R2_t2c1, R2_t2c2)
# prueba del parche (brain-env, copia de f19a9c7)
5299df9a477741c85e9287d7d0ae4060  fix_v2_prueba.py
ANTES docs/v2/paper1-v2.0.md e5fb86dcf79867e77434df33269ad745
ANTES docs/SECCION-V2-DOS-SALTOS.md cbe0245750c4ae1810eda829e391ba7a
ANTES docs/v2/zenodo-v2.0-metadata.json 375853474c9148e92aacdd0945b69e42
REEMPLAZO F01 seccion 3.4 apariciones=1
REEMPLAZO F07 seccion 3.4 apariciones=1
REEMPLAZO F06 limitacion 2 apariciones=1
REEMPLAZO F01 limitacion 7 apariciones=1
REEMPLAZO F06 cambio 15 apariciones=1
REEMPLAZO F01 seccion de dos saltos, ensemble apariciones=1
REEMPLAZO F07 seccion de dos saltos apariciones=1
REEMPLAZO F01 seccion de dos saltos, limitacion apariciones=1
DESPUES docs/v2/paper1-v2.0.md 2fa575c41926fdc790cecbb5965ba2a1
DESPUES docs/SECCION-V2-DOS-SALTOS.md 23db9cacbcae29fdb355ade871cea540
PARCHE OK: 8 reemplazos (5 en el manuscrito, 3 en la seccion de dos saltos); metadatos sin cambios
# render (log md5 071e20a9…)
ENTORNO pandoc 3.10.2 | typst 0.15.0
FUENTE docs/v2/paper1-v2.0.md 56298 2fa575c41926fdc790cecbb5965ba2a1
PDF Mendieta2026_Paper1_v2.0.pdf 330511 a22515e9e2e7bb02e8d3fd824217dfc7 paginas 18 determinista True
FUENTE docs/ERRATUM.md 41121 f2ad05072086258a8ce76b9d650ed26d
PDF Mendieta2026_Paper1_Erratum_v1.0.pdf 191172 05052e6e7e0dd79cee584c9d285b1b93 paginas 15 determinista True
VEREDICTO_RENDER PASS
# parche en el PR
07afb2b herramienta(v2): parche de F01, F06 y F07 de la auditoria de Tao y workflow que lo aplica ...
38397952384 aplicar-fix-v2-2026-10-13 queued None 07afb2b
```

## Archivos

- **Rama `titan/v2-cierre-2026-10-12` (PR #27), commit `07afb2b`:**
  - `tools/v2/fix_v2_2026-10-13.py` (md5 `5299df9a…`);
  - `.github/workflows/aplicar-fix-v2-2026-10-13.yml` (md5 `3ef4741b…`).

  El bot va a sumar `docs/v2/fix-v2-2026-10-13.log` y los dos textos corregidos.
- **Rama `titan/factorial2-mosca-2026-10-13`:** `results/factorial2_2026-10-13/CORRER` (`9f8b848`).
- **main:** este archivo.
- **PDF de prueba** (binarios derivados, no se commitean): `/workspace/v2cierre_2026-10-12/deposito_2026-10-13/` en brain-env.

## NO MEDIDO

- **Los resultados del factorial 2.**
- **La aplicación del parche en Actions.** Está en cola, y el texto del PR #27 sigue siendo el de `f19a9c7`.
- **El paso siguiente de la v2, que espera a que el bot aplique:**
  1. render desde el commit del bot, que debe dar `a22515e9…` porque la fuente tiene el mismo md5 y el render es determinista;
  2. `archivos-deposito-v2.0.json` con 18 páginas y los md5 nuevos;
  3. `depositar_v2.py --verificar`.
- **Nadie miró la maquetación del PDF nuevo.** Sólo se comprobaron cadenas sobre el texto extraído.

## Antes de firmar

| Afirmación | Instrumento | ¿Podía dar rojo? |
|---|---|---|
| El factorial corre con el instrumento sellado | El CORRER sólo agrega un archivo de texto; el workflow corre `9442fdf` + CORRER | Sí: un cambio en `tools/` aparecería en el diff |
| El parche hace lo que dice | Conteo de apariciones = 1 y controles de frases viejas y nuevas | Sí: aborta si un ancla no aparece o aparece dos veces |
| El 138.140 es el de las tablas | Mismo archivo de evidencia que los cocientes de la Tabla 5b | Sí: podía estar en otra corrida |
| El PDF compila | `render_v2.py` con 19 cadenas y doble compilación | Sí: da FAIL si falta una cadena o no es determinista |
| El PR ya está corregido | **No se afirma** | Está en cola: NO MEDIDO |

```
--- METODO PROMETEO ---
Accion delicada: no (rama titan del factorial y rama del PR #27; sin merge ni deposito)
Maquina: Actions x64 (factorial 2 y, en cola, el parche) | brain-env (prueba del parche, render, vigia)
Artefactos: docs/agents/respuestas/2026-10-13-006-factorial-2-corriendo-y-el-arreglo-de-f01-f06-f07-en-cola-en-el-pr-27.md + Doc de ClickUp 2026-10-13-006
```
