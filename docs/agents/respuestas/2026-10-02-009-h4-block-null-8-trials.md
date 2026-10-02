# Recibo 009: null por bouts en ocho trials

## Pedido

Continuar la materialización H4 y ejecutar el primer rerun con nulls por bouts/trials, sin unir por `Frame` y sin llamar cross-animal a los ocho trials.

## Herramientas y máquina

- `mcp_gateway__gateway_call_tool`, servicio `build`, máquina `brain-env` persistente.
- Instrumento: `tools/h4_block_null.py`, Python estándar, sin dependencias nuevas.
- Entrada: ocho JSONL ROI-preserving alineados. El trial 7 fue regenerado desde sus fuentes porque su metadata antigua no llevaba `verdict=BIEN`; la regeneración oficial devolvió `BIEN`.
- No se modificó `main`, no se cambió el workflow CI y no se gastó runtime ajeno.

## Qué se midió

- Scope: `within_animal_across_trials`.
- Animal: `R65D11-tdTomGC6fopt-fly1`.
- Trials: 8/8, todos del mismo animal, por lo tanto **no es cross-animal**.
- Contexto: `co2_off`.
- ROI: `ROI_0`, `ROI_1`.
- Null: permutación de tokens completos `(label, longitud)` dentro de cada segmento contiguo de contexto; 999 permutaciones, seed `20261002`.
- Labels solicitados: `walking`, `resting`, `head_grooming`, `foreleg_grooming`, `hind_grooming`.
- Métrica: eta-cuadrado multivariado sobre medias por bout, con ROI normalizadas por trial y peso igual por bout.

Resultado pooled:

```text
verdict=BIEN
observed=0.35831155721189717
null_n=999
null_mean=0.06104563938527175
null_sd=0.017371858516985278
p_greater_equal=0.001
z=17.11192372053771
```

Por trial, `(trial, observed, p)`:

```text
1 0.32087984719448054 0.001
2 0.42592557617483967 0.006
3 0.29626814956153763 0.004
4 0.21797499585609062 0.014
5 0.4906898012211563 0.001
6 0.3909456431837279 0.001
7 0.42004061756022093 0.001
8 0.30376782694312376 0.002
```

## Evidencia cruda verbatim

```text
COMMAND=PYTHONDONTWRITEBYTECODE=1 python3 -S tools/h4_block_null.py --input trial_1 --input trial_2 --input trial_3 --input trial_4 --input trial_5 --input trial_6 --input trial_7_regenerated --input trial_8 --context co2_off --labels walking,resting,head_grooming,foreleg_grooming,hind_grooming --min-bouts 2 --permutations 999 --seed 20261002 --out results/h4_block_null_co2_off_8_trials.json
EXIT_CODE=0
```

Suite local del instrumento: `5 tests OK`. Mutación que desactivó el rechazo de `Frame`: rojo real; código restaurado: `5 tests OK`.

## Veredicto derivado

El primer rerun descriptivo detecta separación ROI-label por encima de este null bloqueado en los ocho trials. Esto **no confirma H4 fuerte**: sigue siendo señal descriptiva/decodificable de dos ROI dentro de un animal. No identifica rutas anatómicas, no demuestra activación/desactivación causal y no prueba generalización entre animales.

Estado científico: **H4 fuerte NO MEDIDA**.

## Deuda explícita

- El resultado completo con los 999 scores individuales queda generado en `brain-env`, pero el push automático del commit local falló porque ese checkout no tiene credencial HTTPS. El recibo conserva el comando, exit code y resumen recomputable; la copia íntegra de la distribución debe volver a publicarse antes de tratarla como release reproducible.
- El test todavía no está agregado al workflow CI: cambiar workflows requiere aprobación separada.
- Falta mapping ROI→cell type/FlyWire, null anatómico pareado y silenciamiento causal.

--- METODO PROMETEO ---
Accion delicada: NO
Modo aplicado: FULL
Maquina: brain-env
Rubrica: N/A (instrumento y recibo; no deployment)
N/A declarados: CI, mapping anatómico y causalidad no aplican a este bloque
Review externo: pendiente; silencio no es aprobación
Instrumento: `python3 -S`, 5 tests + mutación negativa + 999 permutaciones; fuente de salida en brain-env y métricas arriba
Artefactos: `tools/h4_block_null.py` + `tests/test_h4_block_null.py` + `docs/adr/2026-10-02-h4-block-null.md` + este recibo
