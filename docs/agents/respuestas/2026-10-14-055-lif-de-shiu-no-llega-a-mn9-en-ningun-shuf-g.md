# 2026-10-14-055 · Corrido: el LIF de Shiu no llega a MN9 en ninguno de los 40 barajados de destinos, k32 incluido; el atajo de k32 era de nuestra neurona de tasa

**Fecha:** 2026-10-16, 15:52 (America/Buenos_Aires)
**Doc:** https://app.clickup.com/90171457413/docs/2kza6fw5-23757

## Pedido

«Implement and run the sealed SHUF_G experiment» (Abraham, 16-oct 15:00): instrumento, prueba, humo y CORRER del sello H_LIF_SHUFG (`tools/mosca_entera/SELLO-LIF-SHUFG-054.md`, 307db84, md5 9e7e25f7).

## Veredicto primero

- **[MEDIDO] Corrido entero en Actions con el instrumento sellado.** Instrumento f505fa3; prueba 12 de 12 (bot 733e958); humo completo (bot 1e46f15); CORRER en el run 38948072997, 18:32 a 18:48 UTC, bot bd37336. MD5SUMS 30 de 30 desde un clon fresco.
- **[MEDIDO] Los tres controles pasan.** PIN (blob 5ba7083c, brian2 2.10.1, md5 de datos en los 9 trabajos); CTRL_REAL (MN9 en 30 de 30 ensayos reales, 62,5 Hz; la 049 dio 61,6); NULO_MISMO 40 de 40 (diferencia relativa máxima 1,0e-10 contra los radios de la 049).
- **[MEDIDO] H_LIF_G_SHIU SOSTENIDA.** Ningún SHUF_G llega a MN9: 0 de 10 ensayos en cada uno de los 40, ni una espiga de MN9 en 400 ensayos.
- **[MEDIDO] H_LIF_G_VARA SOSTENIDA.** Ningún nulo con tasa de MN9 igual o mayor que la del real (máximo 0,0 Hz contra 62,5).
- **[MEDIDO] H_LIF_K32 NO_LLEGA.** k32, el único de 80 nulos que con nuestra tasa pasaba al real en la 049 y la 051, da 0 de 10 en el LIF.
- **[MEDIDO, descriptivo] El atajo de k32 existe y es único.** Es el único de los 40 con una arista directa de azúcar a MN9 (n1 = 1), de exactamente 11 sinapsis (D1+ = 11), lo que había inferido el sello. El real no tiene ninguna arista directa (n1 = 0) y llega por caminos más largos.
- **[CONCLUSION, lectura sellada]** El atajo de k32 es de nuestra celda de tasa; el LIF no lo toma. El freno de H_UMB_MN9 es de la neurona, no del barajado. H_UMB_MN9 y H_ENTERA_MN9_G1 siguen SIN_DECIDIR: el sello dejó escrito que esto atribuye y no cambia veredictos.
- **[CONCLUSION] Qué quiere decir.** Con el mismo cableado y los mismos 40 barajados, el modelo de Shiu (espigas y umbral) separa el real de todos y el nuestro no. La tasa suma una entrada directa chica de 11 sinapsis y la pone arriba del real; el LIF necesita convergencia (11 sinapsis dan 1,5 mV de los 7 que faltan). Para la motora fina hace falta un umbral que integre en el tiempo; la 051 ya mostró que un umbral global sobre la tasa no alcanza.
- **[MEDIDO] Las siete apuestas escritas en el sello salieron** (k32 no llega 80%, H_LIF_G_SHIU 75%, H_LIF_G_VARA 90%, CTRL_REAL 95%, NULO_MISMO 95%, k32 con arista directa 80%, única 65%).
- **Propuesta, sin sellar:** una celda de SparseLTC que integre en el tiempo con umbral y reinicio, contra los mismos 80 nulos.

## Herramientas y máquina

- Sandbox de ClickUp: escritura del instrumento; prueba 10 de 10 sin brian2.
- brain-env: venv aparte con brian2 2.10.1 y el `model.py` de Shiu; prueba 12 de 12 (sin g++, brian2 usó numpy en vez de Cython); clones frescos para md5 y lectura.
- Actions (ubuntu-latest, 4 vCPU, 16 GB): prueba 12 de 12 con Cython, humo (2 trabajos) y CORRER (9 trabajos: el real de 30 ensayos y 8 de 5 nulos).
- Conector GitHub: pushes a la rama y a `main`.

## Evidencia cruda

De `results/lif_shufg_2026-10-16/actions_correr/agregado_lif_shufg.log` (md5 9b8634f483904b6d627715335b538058), en la rama:

```
CONTROL PIN PASA
CONTROL CTRL_REAL PASA (30 de 30, minimo 27)
REAL E_MN9=30 de 30 F_MN9=62.5000 Hz activas=406 espigas=270242 K=327 atajo n1=0 D1+=0.0 D2+=261.0
NULO k=32 E_MN9=0 F_MN9=0.0000 activas=79 K=36 J=0.0000 n1=1 D1+=11.0 D2+=20.0 radio=372.813237 desbocado=False | 103 s
CONTROL NULO_MISMO PASA en 40 de 40 (otros estados 0, sin archivo 0)
NULOS medidos=40 faltan=0 llegan=[] ge_real=[] desbocados=[]
VEREDICTO H_LIF_G_SHIU SOSTENIDA (llegan=0, faltan=0)
VEREDICTO H_LIF_G_VARA SOSTENIDA (con F_MN9 >= real=0, faltan=0, F_real=62.5000 Hz)
VEREDICTO H_LIF_K32 NO_LLEGA (foco k=32)
LECTURA K32 NO_LLEGA: el atajo de k32 es de nuestra celda de tasa; el LIF no lo toma. El freno de H_UMB_MN9 es de la neurona, no del barajado.
DESCRIPTIVO nulos con n1>=1: [32] | foco n1=1 D1+=11.0 D2+=20.0 | foco unico con n1>=1: True
DESCRIPTIVO activas mediana=89 max=142 | J mediana=0.0000 max=0.0028 | F_MN9 max=0.0000 Hz
```

Releido en brain-env desde un clon fresco en bd37336: MD5SUMS 30 de 30 OK (humo 9 de 9, prueba 2 de 2); NULO_MISMO maximo 1,03e-10; nulos de 91 a 210 s (5.830 s en total); real 506,5 s y 3,6 GB. Los 40 nulos dan E_MN9 0 de 10, con 74 a 142 activas (real 406). La S_LIF de este real contiene las 321 de la 049 (J 0,982). k39 tiene mas peso en caminos de dos pasos que el real (D2+ 482 contra 261) y MN9 tampoco dispara: que haya caminos no alcanza. Humo: k 99 con NULO_MISMO a 1,8e-11, 0 de 10, 202 s.

## Archivos

| Archivo | Dónde | md5 |
|---|---|---|
| `tools/mosca_entera/lif_shufg.py` | rama, f505fa3 | cfe86b4785bcdd61704c77057b9f360f |
| `tools/mosca_entera/agregar_lif_shufg.py` | rama, f505fa3 | 941ff6fd466281eb4825323cad334b68 |
| `tools/mosca_entera/prueba_lif_shufg.py` | rama, f505fa3 | 864ba0d6069f2a9cc38550cb2c8870a5 |
| `.github/workflows/lif-shufg-correr.yml` | rama, f505fa3 | c674647292ded7289347f0a2b4786949 |
| `results/lif_shufg_2026-10-16/actions_correr/MD5SUMS.txt` | rama, bd37336 | d8ffe2245df650d9f7646749bbaaf99f |
| `results/lif_shufg_2026-10-16/actions_correr/agregado_lif_shufg.json` | rama, bd37336 | 2a83c5ed05fabdc55288a0ef70bf83b2 |
| `results/lif_shufg_2026-10-16/actions_correr/lif_shufg_real.json` | rama, bd37336 | 926d07cb5a00323f8222a5b2aab6189f |
| `results/lif_shufg_2026-10-16_humo/actions_prueba/prueba.log` | rama, 733e958 | 59927806913ecbf1dbd45f870dab1e74 |

## NO MEDIDO

- Por qué camino concreto llega el real a MN9 sin arista directa.
- Una celda de SparseLTC con integración en el tiempo (sin sellar).
- SHUF_W 20 a 39 en el LIF, otros estímulos y el nulo de los suplementos de Shiu.
- El CONTEXTO no se actualizó en esta respuesta: el parche 055 queda pendiente.
- La réplica de H_LECTOR en brain-env terminó (6 de 6 celdas); el cotejo no se hizo.

## Antes de firmar

| Afirmación | Instrumento | ¿Podía dar rojo? | Veredicto |
|---|---|---|---|
| LIF de Shiu sin cambios | PIN en cada trabajo y en el agregado | Sí: la prueba aborta con un model.py ajeno | medido |
| Nulos = los de la 049 | NULO_MISMO 40 de 40 | Sí: rojo a 2e-6 en la prueba | medido |
| El real reproduce a Shiu | CTRL_REAL 30 de 30 | Sí: 26 de 30 da rojo | medido |
| Ningún nulo llega | E_MN9 de los 40 JSON, releído en brain-env | Sí | medido |
| k32 con 11 sinapsis directas | atajo() sobre el parquet que leyó Shiu | Sí | medido |
| El freno de k32 es de nuestra neurona | lectura fijada en el sello | No | CONCLUSION |
| Independencia (W-01) | el LIF es código de Shiu; nulos y atajo son nuestros | Parcial | declarado |

--- METODO PROMETEO ---
Rol: implementa y mide. Delicado: no.
Máquinas: sandbox de ClickUp, brain-env, Actions, conector GitHub.
Archivo: `docs/agents/respuestas/2026-10-14-055-lif-de-shiu-no-llega-a-mn9-en-ningun-shuf-g.md` en `main`.
Sello 307db84. Instrumento f505fa3. Medición bd37336.
Doc: https://app.clickup.com/90171457413/docs/2kza6fw5-23757
