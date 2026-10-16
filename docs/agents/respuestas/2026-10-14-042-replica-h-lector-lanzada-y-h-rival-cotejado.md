# 2026-10-14-042 · La replica completa de H_LECTOR corre en brain-env, y H_RIVAL ya dio lo mismo en las dos maquinas

## Pedido

- 15-oct 21:51: "Lanza la replica completa de H_LECTOR".

## Veredicto primero

- [MEDIDO] **H_RIVAL replicado.** La replica en brain-env (6 celdas, de 4210 a 4365 s cada una; empezo el 15-oct 08:18 y termino a las 15:56) coteja con Actions (`agregar_rival.py --cotejar`):

| Rival | etiqueta Actions / brain-env | aciertos iguales | diferencia maxima |
|---|---|---|---|
| RIDGE | NO_SUPERA / NO_SUPERA | 120 de 120 | 0,0000 |
| MLP | NO_SUPERA / NO_SUPERA | 40 de 120 | 0,0045 |
| REGLA_TAU | SIN_DECIDIR / SIN_DECIDIR | 120 de 120 | 0,0000 |

  VEREDICTO_COTEJADO: H_RIVAL REFUTADA y H_TAU_JUSTO SIN_DECIDIR. El MLP (torch) no es bit a bit igual entre maquinas, pero su D en brain-env (-0,0478, IC [-0,0494, -0,0463]) da la misma etiqueta que en Actions.
- [CONCLUSION] La replica de la primaria de H_LECTOR esta lanzada en brain-env: desde el clon de `8d305e9` (`lector_mosca.py` 5b7fb79e, sin cambios), 6 celdas en dos grupos de 3 que corren a la vez (c0, c2, c4 y c1, c3, c5), salida en `/workspace/fable/rl041/out_brain`. Al terminar: `agregar_lector.py --dir` con los nulos de Actions copiados (el sello no replica los nulos) y `--cotejar` contra el agregado de Actions.
- [NO MEDIDO] La replica de H_LECTOR y su duracion. Estimacion desde el humo local: unas 4 h por celda con la maquina compartida, unas 12 h en total. Si una etiqueta difiere, pasa a SIN_DECIDIR (NO_SE_REPLICA).

## Herramientas y maquina

- brain-env (Python 3.12.14, numpy 2.5.3, torch 2.14.1 cpu, 2 nucleos, 7 GB): las dos replicas.
- El gateway pidio una confirmacion que no llego en algunos intentos de escribir un script de corrida; la replica se lanzo con dos comandos `nohup sh -c` sin script nuevo (los mismos argumentos que el workflow `lector-mosca.yml`).

## Archivos (brain-env, no commiteados: son resultados de una replica en curso o ya cotejada)

| Archivo | md5 |
|---|---|
| `r034/out_brain/agregado.log` (H_RIVAL, brain-env) | 1716836061febd55404d8cdea5b195b1 |
| `r034/out_brain/agregado.json` | 3de3468ba19c09a846e7f883cb0c9cc9 |
| `r034/out_brain/rival_c0.json` a `c5` | 7de36b3a, 83a32c26, f8f79bc1, 3cf5905c, 781deca8, 873d6f3a |

En `main`: esta respuesta, `tools/contexto/actualizar_contexto_2026-10-14-042.py` y `.github/workflows/contexto-2026-10-14-042.yml` (se borra solo al aplicar).

## Antes de firmar

- El cotejo de H_RIVAL podia dar rojo: con una etiqueta distinta el veredicto pasaba a SIN_DECIDIR. No paso.
- El cotejo de H_LECTOR solo puede confirmar CERCA y PAGA; CABLEADO y H_TAU_LIBRE quedan como resultados de Actions (los nulos no se replican).

--- METODO PROMETEO ---
Rol: replica. Delicado: no.
Maquina: brain-env.
Artefactos: replica de H_RIVAL en `/workspace/fable/r034/out_brain`; replica de H_LECTOR en curso en `/workspace/fable/rl041/out_brain`; esta respuesta y el parche del CONTEXTO en `main`; Doc de ClickUp de la 042.
