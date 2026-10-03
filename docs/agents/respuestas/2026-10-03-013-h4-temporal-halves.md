# Recibo 013: estabilidad temporal por mitades, auditoría TITAN FULL

## Pedido

Auditar el proyecto en esta instancia, corregir, mejorar e innovar bajo TITAN FULL, y reintentar la medición temporal usando GitHub como canal de transferencia.

## Hallazgo crítico corregido

La primera versión del null barajaba pares `label+length` entre slots, pero conservaba el vector ROI calculado para el slot original. Eso violaba el contrato: un registro podía declarar una longitud distinta de la usada para calcular su media. El falsador reprodujo el rojo:

```text
before vectors=[(1.5,), (4.0,)]
after=[('resting', 3, (1.5,)), ('walking', 2, (4.0,))]
length-vector-mismatch=True
```

Corrección: dentro de cada mitad y cada segmento `co2_off` se permutan **solo labels**; cada slot conserva su longitud y vector ROI. Se agregó el contrato que verifica ambos invariantes.

## Ejecución real corregida

- Instrumento transferido por GitHub a `titan/h4-temporal-halves-2026-10-02`.
- Commit del instrumento corregido: `acb88d0ba6cd177684bd46cd3d73679e26c2fd06`.
- Commit de tests falsadores: `b6b085128a49755b8b503fc8c302f8a34beb1224`.
- Suite completa: **34 tests OK**.
- Corrida real: 8 trials, un animal, `walking/resting`, `co2_off`, 999 permutaciones, seed `20261002`.
- Repetición real byte a byte idéntica.

## Resultado

```text
animal=R65D11-tdTomGC6fopt-fly1
n_trials=8
observed_bidirectional_transfer=0.5327595514498719
null_mean=0.5018239610724393
null_sd=0.019476626168946264
p_greater_equal=0.055
z=1.588344413918904
raw_result_sha256=c2c0e2f2093bc85650daa6bb487b8dcd4bf1ae38278d64de24fd040abb202d98
```

El resultado numérico no cambió porque el defecto anterior afectaba metadata que el score no consultaba; el arreglo era obligatorio porque el instrumento debe cumplir el contrato que afirma.

## Auditoría ejecutiva del proyecto

- **H4 fuerte:** NO MEDIDA. No hay evidencia causal de activación/desactivación de rutas.
- **H4 débil:** refutada solo en su operacionalización anatómica estrecha ya documentada.
- **Alineación:** pasa con guard negativo; `Frame` rechazado.
- **Features:** ROI-preserving y bouts válidos en 8/8 trials.
- **Null temporal:** corregido, segment-preserving, slot-length/vector-preserving.
- **Generalización entre trials:** no evidenciada por encima del null, `p=0.623`.
- **Estabilidad temporal:** sugestiva pero no positiva, `p=0.055`.
- **Mapping ROI→FlyWire/cell type/neuropilo:** NO MEDIDO.
- **Null anatómico pareado:** NO MEDIDO.
- **SparseLTC sobre subgrafos biológicos y silenciamiento causal:** NO MEDIDOS.
- **Producto end-to-end SparseLTC→DBC3 sobre señal real:** NO MEDIDO.

## Evidencia publicada

- `tools/h4_temporal_halves.py`
- `tests/test_h4_temporal_halves.py`
- `results/h4_temporal_halves_summary.json`
- `results/h4_temporal_halves_run.log`
- `docs/adr/2026-10-03-h4-temporal-halves.md`
- este recibo

--- METODO TITAN ---
Accion delicada: SI, porque se cambió workflow y evidencia pública en un PR; no se tocó `main` ni se mergeó.
Modo aplicado: TITAN FULL
Rubrica: pendiente de cierre QA en el Doc público
N/A declarados: deployment, ABI, seguridad de runtime y performance de producto no aplican a este instrumento científico
Review externo: checks GitHub verdes; review automático de código externo no emitió hallazgos, estado NO MEDIDO y no aprobación
Instrumento: brain-env vía servicio build; contratos Python stdlib; 34 tests OK; corrida real 999 permutaciones; evidencia cruda en `results/h4_temporal_halves_run.log`
