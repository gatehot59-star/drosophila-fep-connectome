# 2026-10-14-011 · Topo v0 ya corre: el escape en 18 renglones da exactamente lo mismo que la regla sellada y baja al mismo cableado de 46 neuronas

**Pedido.** 14-oct 12:47: ClickKit `lenguaje_sellar_010` («Diseñá el lenguaje y su falsador»). 12:48: «Diseñá el lenguaje topológico ejecutable». Viene de la 2026-10-14-010.

## Veredicto primero
- **[HECHO] Topo v0, en la rama `titan/topo-lenguaje-2026-10-14` (`b34924d`, desde `titan/factorial3-mosca-2026-10-13`).**
  - Un reflejo se escribe como tipo × lado × signo → comando.
  - Tiene un intérprete con dos backends: regla (entradas crudas) y cableado (subgrafo de FlyWire).
  - Gramática en `docs/topo/TOPO-v0.md`.
- **[MEDIDO] F1 EQUIV_REGLA PASA, 12 de 12 casos (6 celdas × 40 y 564 entradas).**
  - Diferencia 0 en las señales y en los umbrales, y 400/400 decisiones iguales en cada caso.
  - La comparación es contra la regla sellada: `media` y `lc` de `factorial2_mosca.py` (798a824c), compiladas desde su árbol sintáctico sin copiarlas a mano, más `lineas`, `umbrales` y `carrera` de `tarea_mosca.py` (40d64e07).
- **[MEDIDO] F2 CONTROL_NEGATIVO PASA.**
  - Con el aterrizaje leyendo LPLC1 en lugar de LPLC4 cambian 127 de 400 decisiones, y el acierto cae de 0,9075 a 0,6550.
  - Los 3 programas mal escritos se rechazan: tipo fuera del vocabulario, falta de lado, acción desconocida.
- **[MEDIDO] F3 REPRODUCE_M46 PASA.**
  - El backend cableado da exactamente la misma selección y las mismas aristas que `tarea_mosca.construir`: 46 neuronas, 187 aristas, 0 inhibitorias y 1.149 sinapsis, como en la 2026-10-12-015.
  - Insumos fijados por md5: conn 3d802fd5, annot 719904ab.
- **[MEDIDO]** Las tres pruebas se corrieron desde un clon limpio de la rama. Registro `results/topo_2026-10-14/prueba_topo.log`, md5 `f1008c67`, igual en brain-env y en git.
- **[NO MEDIDO] H_TOPO_NUEVO, que decide si es un lenguaje y no una transcripción:** un reflejo nuevo, escrito solo en Topo antes de ver datos, que pague en el banco. También faltan H_TOPO_C99 y H_TOPO_ESCALA.

## Herramientas y máquina
- brain-env (CPU, numpy 2.5.3, pandas 3.0.5):
  - escritura del intérprete y la prueba;
  - lectura de los módulos sellados con md5 verificado;
  - corrida de la prueba en la copia de trabajo y después en un clon limpio.
- GitHub (conector): `create_branch` y dos `push_files` en la rama titan; esta respuesta en main.

## Qué se midió
1. Que el backend regla de `escape.topo` da los mismos números que la regla sellada, con ensayos generados por la tarea sellada (`tm.generar` y `tm.sintonias`).
2. Que un programa mutado da decisiones distintas y que los programas inválidos se rechazan.
3. Que el backend cableado reproduce el motivo M46.

## Evidencia cruda
```
PRUEBA EQUIV_REGLA casos=12 -> PASA   (max_dif_senal=0 max_dif_umbral=0 decisiones_iguales=400/400 en cada caso)
NEGATIVO aterrizaje con LPLC1: decisiones_distintas=127/400 acierto 0.9075 -> 0.6550
PRUEBA CONTROL_NEGATIVO -> PASA
CABLEADO topo: neuronas=46 aristas=187 inhibitorias=0 sinapsis=1149 | sellado: neuronas=46 aristas=187
PRUEBA REPRODUCE_M46 -> PASA
VEREDICTO_TOPO -> PASA
md5: topo.py 9abefe9d | escape.topo dae4967d | prueba_topo.py ee5f4fa8 | prueba_topo.log f1008c67
```

## Archivos
- Rama `titan/topo-lenguaje-2026-10-14`: `tools/topo/topo.py`, `tools/topo/escape.topo`, `tools/topo/prueba_topo.py`, `docs/topo/TOPO-v0.md`, `results/topo_2026-10-14/prueba_topo.log`.
- Esta respuesta.
- `tools/contexto/actualizar_contexto_2026-10-14-011.py` (md5 `7f0a52ea`).
- `.github/workflows/contexto-2026-10-14-011.yml`.
- Doc público: https://app.clickup.com/90171457413/docs/2kza6fw5-22277

## NO MEDIDO
- H_TOPO_NUEVO: necesita un reflejo nuevo y su generador de estímulos. Candidatos: «la barra pide aterrizaje» (2026-10-12-014) o LC6→GF.
- H_TOPO_C99: costo y equivalencia en microcontrolador.
- H_TOPO_ESCALA: bajar a R1 y R2.
- Que el backend cableado simule: hoy solo arma el subgrafo, y la dinámica es la del banco.

## Antes de firmar
| Afirmación | Instrumento | ¿Podía dar rojo? | Veredicto |
|---|---|---|---|
| Topo equivale a la regla sellada | Diferencia exacta de señales, umbrales y decisiones contra las funciones selladas, no contra una copia | Sí: el mismo comparador marcó 127/400 distintas con el programa mutado | PASA |
| Los dos lados del A/B no son la misma función | Topo tiene su propio `umbrales` y su propia `carrera`, escritos de nuevo; no llama a `tm.umbrales` ni a `tm.carrera` | Sí | PASA |
| Baja al mismo cableado | Igualdad de listas contra `tm.construir`, con insumos por md5 | Sí: falla si cambia una neurona o una arista | PASA |
| Corre como está en git | Clon limpio y md5 del registro igual en los dos lados | Sí | PASA |
| Es un lenguaje y no una transcripción | H_TOPO_NUEVO | — | NO MEDIDO |

--- METODO PROMETEO ---
Accion delicada: no (código nuevo en una rama titan sin PR; nada sellado cambió; ninguna corrida en Actions).
Maquina: brain-env CPU + conector GitHub.
Artefactos: `titan/topo-lenguaje-2026-10-14` `b34924d`; esta respuesta en main; Doc https://app.clickup.com/90171457413/docs/2kza6fw5-22277
