# 2026-10-14-004 · La v2 del paper está en main; H_TAU y el núcleo corren en Actions; para depositar falta el token de Zenodo

**Pedido.** 14-oct 11:22: «Justamente lo hecho a mano es una buena opción y barata [...] Pero antes cerremos paper 1 v2 y el paper 2». 11:28: ClickKit `merge_y_correr_004` («Mergear la v2 y correr los dos»).

## Veredicto primero
- **[MEDIDO] El PR #27 está mergeado en main:** merge commit `67853168fb9da47b75f2ce2f23ddad8480c1e224`, cabeza del PR `e7fd3594ad7d7f9ebfc1ada83d0a63cebb00c1ad`. Antes del merge, `git merge-tree` contra main `7eec778` dio limpio (árbol `05d731e2`, sin conflictos).
- **[MEDIDO] La v2 en main pasa su verificación de depósito.** `tools/zenodo/depositar_v2.py --verificar` da `VEREDICTO_VERIFICAR PASS`: 8 metadatos OK, `Mendieta2026_Paper1_v2.0.pdf` (332.607 bytes, md5 `6e849bf2`) y `Mendieta2026_Paper1_Erratum_v1.0.pdf` (191.172 bytes, md5 `05052e6e`) OK. `docs/v2/paper1-v2.0.md` md5 `a4d09d2c`.
- **[MEDIDO] H_TAU y el núcleo están corriendo.** El commit `9545af4` en `titan/htau-nucleo-banc-2026-10-14` agrega solo `results/htau_2026-10-14/CORRER` y `results/nucleo_2026-10-14/CORRER`; nada de lo sellado en `4f4e672` cambió. Los workflows `htau-mosca` (run 38581126995) y `nucleo-mosca` (run 38581127132) arrancaron a las 14:30 UTC.
- **[CONCLUSIÓN] Cuándo vuelven:** el núcleo hacia las **13:30** y H_TAU hacia las **14:30** (Buenos Aires). La estimación sale de la velocidad medida en el humo (núcleo 0,045 s por ensayo, R2 0,146 s). Actions corre unos 20 trabajos a la vez, y H_TAU ocupa 6 de esos lugares durante unas 2,6 h.
- **[NO MEDIDO] El depósito en Zenodo.** Falta el token con `deposit:write` y `deposit:actions`. Con el token se arma primero `--borrador` (no publica); `--publicar` es irreversible y va solo con el sí de Abraham.

## Herramientas y máquina
- GitHub (conector): merge del PR #27 y push de los `CORRER` y de esta respuesta.
- brain-env (CPU): la prueba de mezcla, `--verificar` sobre main, la consulta del estado de Actions y la prueba del parche de CONTEXTO en una copia.
- GitHub Actions x64: corre los dos sellos.

## Qué se midió
1. La cabeza del PR (SHA completo) y que la mezcla con main fuera limpia.
2. El merge y `--verificar` sobre main ya mergeado.
3. Que los dos workflows se dispararan con el commit de los `CORRER`.

## Evidencia cruda
- Merge: `{"merged":true,"sha":"67853168fb9da47b75f2ce2f23ddad8480c1e224"}`.
- Actions, 14:30 UTC: `nucleo-mosca` en estado queued y `htau-mosca` en estado in_progress, los dos con `head_sha 9545af4f`.
- Cada `CORRER` cita el pedido, el SELLO (`8fbd0abd` y `3ddb3414`) y el md5 de su código y su workflow.

## Archivos
- Esta respuesta.
- `tools/contexto/actualizar_contexto_2026-10-14-004.py`: probado en una copia, pasa el CONTEXTO de `48d5f67d` a `b0d8d742` y aborta si se aplica dos veces.
- `.github/workflows/contexto-2026-10-14-004.yml`: aplica el parche y se borra solo.
- Doc público: https://app.clickup.com/90171457413/docs/2kza6fw5-22137

## Qué sigue
1. Leer los agregados de H_TAU y del núcleo apenas el bot los commitee.
2. Hacer el esqueleto del Paper 2 (tres escalas, BANC, H_CONSENSO y H_TAU).
3. Hacer el nulo del emparejado BANC.
4. Con el token: borrador de Zenodo.
5. Responderle a Tao en el PR #28.

## NO MEDIDO
- Ningún resultado de H_TAU ni del núcleo.
- Las horas de llegada son una estimación.
- El depósito en Zenodo.
- El Paper 2 todavía no tiene borrador.

## Antes de firmar
| Afirmación | Instrumento | ¿Podía dar rojo? | Veredicto |
|---|---|---|---|
| La mezcla era limpia | `git merge-tree --write-tree` | Sí, lista conflictos y sale con error | PASA |
| El PR quedó mergeado | Respuesta del merge con SHA esperado | Sí, rechaza si la cabeza cambió (ya rechazó un SHA corto) | PASA |
| La v2 en main está lista para depositar | `--verificar` (md5 y metadatos) | Sí, marca cada archivo o campo que falte o difiera | PASA |
| Los dos sellos están corriendo | API de Actions, runs con `head_sha 9545af4f` | Sí, sin runs o con otro SHA | PASA (estado al arrancar; el final NO MEDIDO) |
| Nada sellado cambió | El commit `9545af4` solo agrega dos `CORRER` | Sí, el diff mostraría otros archivos | PASA |
| Horas de llegada | Velocidad del humo y límite de concurrencia | No: es una estimación | CONCLUSIÓN, no medición |

--- METODO PROMETEO ---
Accion delicada: sí (merge a main y disparo de dos experimentos sellados, los dos autorizados por Abraham con `merge_y_correr_004`).
Maquina: conector GitHub + brain-env CPU + GitHub Actions x64.
Artefactos: main `6785316` (merge) y esta respuesta; rama `titan/htau-nucleo-banc-2026-10-14` `9545af4`; Doc https://app.clickup.com/90171457413/docs/2kza6fw5-22137
