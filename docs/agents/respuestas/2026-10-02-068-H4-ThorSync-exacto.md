# H4: validación con alineamiento ThorSync exacto

## Pedido
Seguir con el falsador H4 usando actividad neural y conducta reales.

## Qué cambió
El pretest anterior interpolaba directamente 1.067 frames de DFF a 7.440 frames conductuales. Ahora ejecuté el procedimiento equivalente al repositorio oficial de Aymanns/utils2p, leído en vivo:

1. Basler: 7.469 pulsos de cámara; se recortan a los 7.440 frames declarados por `capture_metadata.json`.
2. Frame Counter: `Streaming zFastEnable=1`, `flybackFrames=1`, `n_z=2`, por tanto `steps_per_frame=3`; 3.201 pasos crudos se convierten en 1.067 frames 2P.
3. ThorSync: frecuencia `30.000 Hz`? No: la metadata `ThorRealTimeDataSettings.xml` fija `30.000 Hz` como **30 kHz** (`rate=30000`).
4. Se interpolan las dos trazas DFF a los tiempos exactos de los frames de cámara.

Trial: R65D11, trial 007, el mismo fly/genotipo del pretest.

## Evidencia cruda verbatim
```text
{
  "n_h5_camera_rises": 7469,
  "n_camera_frames": 7440,
  "n_2p_frames": 1067,
  "n_behavior_frames": 7440,
  "classes": {
    "foreleg_grooming": 70,
    "head_grooming": 315,
    "hind_grooming": 20,
    "resting": 2046,
    "walking": 4952
  },
  "accuracy": 0.6860746938701023,
  "shuffled_accuracy": 0.6689180064602077,
  "accuracy_delta": 0.017156687409894622,
  "pair_cosine_min": 0.9743657513881696,
  "pair_cosine_max": 0.9999756360877589,
  "method": "official utils2p-equivalent ThorSync processing"
}
```

Resultado crudo local: `/workspace/h4_data/aymanns/h4_neural_behavior_sync.json`, 1.631 bytes, md5 `4784a6687f9e841cb58ce2b2f25b93fc`.

## Contexto compartido
Se alineó también `CO2_Stim` del mismo ThorSync. En los 7.440 frames, 7.215 fueron sin CO2 y 225 con CO2. Pero el contexto CO2 tuvo únicamente `resting=85` y `walking=140`; no hubo grooming alternativo en ese contexto. Por lo tanto este trial no satisface el falsador fuerte de “mismo contexto, dos acciones alternativas”.

## Veredicto
La alineación oficial no cambia la lectura: la señal neural permite una separación pequeña sobre el shuffle (`Δ accuracy=0,01716`), pero los centroides de acción son casi colineales (`cosine 0,9744 a 0,99998`). El trial confirma que el instrumento y el dataset son utilizables, no que H4 esté apoyada.

**H4 fuerte sigue NO MEDIDA.** Para medirla hacen falta varios trials con el mismo contexto/estímulo y dos acciones alternativas dentro de ese contexto, más la identidad anatómica de las ROIs y el contraste contra conectividad real/null. El CO2 del trial 007 no alcanza ese criterio.

## Archivos
- Runner exacto: `tools/h4_neural_behavior_sync.py`, commit `657fcbcbbd876fff560af65bc82a70a93877bece`.
- Runner previo: `tools/h4_neural_behavior.py`, commit `959a4100a56f7e7e727d10859e48db61fee5cd83`.
- Este recibo.

--- METODO TITAN ---
Accion delicada: NO
Modo aplicado: TITAN FULL
Rubrica: N/A (medición científica)
N/A declarados: deployment/security/CI no aplican; identidad FlyWire y null topológico siguen NO MEDIDOS
Review externo: no pedido
Instrumento: build.run + fuente oficial utils2p leída en vivo; JSON resumido y md5 arriba
