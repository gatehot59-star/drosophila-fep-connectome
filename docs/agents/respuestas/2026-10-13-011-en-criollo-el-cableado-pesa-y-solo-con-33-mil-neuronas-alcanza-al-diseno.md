# 2026-10-13-011 · En criollo: el cableado real de la mosca pesa en las tres escalas, y sólo con 33.489 neuronas su simulación alcanza al diseño; para un robot conviene el plano

Reemplaza a la síntesis 2026-10-13-003, que decía que alcanzaba con 1.504 neuronas (lo corrigió la 007).

## Veredicto

- **[MEDIDO] El cableado real importa, en las tres escalas.** En las tres, la red con el cableado real le gana a la misma red con los cables barajados (SL) o con los tipos mal asignados (T):
  - **M46 (46 neuronas, 015):** les gana a 300 SL y 300 T en 6 de 6 celdas, Holm 0,0399.
  - **R1 (1.504, factorial 1):** 0,937 contra 0,774 (SL) y 0,742 (T).
  - **R2 (33.489, factorial 3):** 0,9465 contra 0,666 (SL) y 0,760 (T). Ninguno de los 100 barajados lo iguala.
- **[MEDIDO] Contra el diseño de la mosca, sólo la escala grande lo alcanza.** El diseño es la regla tipo de sensor → comando, con los mismos sensores:
  - **M46:** −0,62 con tasa y −1,83 con líquida.
  - **R1:** entre −1,02 y −1,48 (factorial 2).
  - **R2:** +0,85, IC90 [+0,08; +1,51]. Es NO_INFERIOR y no pasa el margen de +1 punto (factorial 3).
- **[CONCLUSIÓN] Dónde estamos.** La mosca da el plano, y con suficiente cableado real su simulación lo reproduce. **No lo mejora.**
- **[CONCLUSIÓN] Para un robot conviene el plano, no el cableado completo.** La regla rinde casi lo mismo (0,9268 contra 0,9353) y no necesita simular 4.031.897 conexiones.
- **[LITERATURA] En el campo, la pregunta es otra.**
  - Shiu et al. (Nature 2024, doi 10.1038/s41586-024-07763-9) simulan el cerebro entero de la mosca con LIF y validan sus predicciones en moscas reales. Nuestro banco baja su mismo archivo de conectividad.
  - Lappalainen et al. (Nature 2024) entrenan τ por tipo sobre 45.669 neuronas del sistema visual y predicen actividad.
  - Nosotros preguntamos si el cableado le gana a su propio diseño con los mismos sensores, con nulos y rival sellados. Ellos tienen validación in vivo; nosotros, cero fuera de simulación.
- **[MEDIDO] Corrección a la 010.** El «15 a 28 puntos» mezclaba dos cosas:
  - sobre el promedio de los barajados son 19 (T) y 28 (SL) puntos;
  - sobre el mejor barajado, 11 (T) y 15 (SL).

## Pedido

Abraham, 13-oct 15:57: «EN CRIOLLO QUE LOGRAMOS, DONDE ESTAMOS POSICINADOS».

## Qué logramos

1. **El mapa funciona y se reproduce.** FlyWire v783 tiene 138.639 neuronas y 15.091.983 conexiones. Da las mismas huellas en brain-env y en Actions, y las 90 corridas comunes entre el factorial 2 y el 3 dieron números idénticos.
2. **El cableado lleva el comportamiento.** En escapar, aterrizar y girar, barajarlo cuesta entre 19 y 28 puntos de acierto en R2. Pasa en las tres escalas.
3. **El rival que nos ganaba era la mosca misma, idealizada.** Con los mismos sensores, M46 y R1 quedan alrededor de un punto abajo. Con 33.489 neuronas la simulación lo alcanza y queda +0,85 arriba, sin pasar el margen.
4. **El método aguanta.** Todo se selló antes de correr, el ancla reprodujo exacto, la réplica corrió en Actions a costo cero y la auditoría de Tao se verificó punto por punto. Los resultados viejos se corrigieron cuando hubo más semillas (002 y 003 por la 007; el +1,28 de la 007 por la 010).
5. **El posicionamiento es honesto (005).** No hay neurona nueva. Lo propio es la dinámica líquida sobre el cableado exacto, el banco sellado y el resultado de la líquida entrenada (013 y 014).

## Dónde estamos posicionados

| Frente | Estado | Qué falta |
|---|---|---|
| Ciencia | Resultado propio y reproducible en tres escalas: el cableado contra sus barajados y contra su propio diseño | Otro conectoma, otra tarea, validación in vivo (no hay) |
| Paper 1 | v1.0 en Zenodo; v2.0 en el PR #27 con F01, F06 y F07 aplicados | Render desde `1f4a2e0`, decidir F05 (Tabla 8), merge, token |
| Paper 2 | Material listo: el banco y las tres escalas | Escribirlo; nulos de R2 en las 6 celdas si se quiere más robustez |
| Robots | Nada medido fuera de simulación. El plano es lo que conviene llevar | Enjambre: enteros que desbordan y un test que no puede dar rojo (Tao), después lazo cerrado y hardware |

## Hacia dónde

1. **Cerrar la v2 del Paper 1.** Es lo único depositable ya.
2. **Escribir el Paper 2 con las tres escalas.** No hace falta otra corrida para el borrador.
3. **Arreglar el enjambre y llevar el plano a lazo cerrado.**
4. **Contestarle a Tao.**

## Herramientas y máquina

- **brain-env:**
  - clon de main en `dd583e2`;
  - lectura del CONTEXTO (md5 `b06c5c62…`, 441 líneas) y del listado de `respuestas/` (la última es la 010);
  - prueba del parche del CONTEXTO en una copia.
- **ClickUp:** lectura del Doc de la 003.
- **Web:** una búsqueda para confirmar Shiu et al. 2024.
- **GitHub MCP:** este commit.
- No se corrió nada nuevo ni se gastó cuota ajena.

## Evidencia cruda

```
# CONTEXTO leído antes de responder (brain-env, clon de main)
dd583e2 contexto(2026-10-13-010): CONTEXTO al dia con el factorial 3 leido, aplicado en Actions
b06c5c625352bdc84b59ed4a1ae7ba16  docs/agents/CONTEXTO-drosophila-fep.md (441 lineas)
ultima respuesta: 2026-10-13-010-factorial-3-r2-alcanza-a-su-regla-y-le-gana-a-sus-barajados.md
# líneas del CONTEXTO usadas
"El cableado paga dentro de R1: 0,937 contra 50 SL (media 0,774) y 50 T (0,742), p por rango 0,0196."
"M46_TASA −0,62 puntos (NO_SUPERIOR); M46_LIQ −1,83 (PIERDE)."
"R1, las cuatro configuraciones, entre −1,02 y −1,48 puntos (NO_SUPERIOR)"
"W les gana a 300 SL y 300 T en 6/6 celdas (Holm 0,0399)"
# factorial 3, agregado.log del bot (09ffbc1)
PRIMARIA R2_CON_TASA W=0.9353 regla_propia=0.9268 dif=+0.0085 IC90=[+0.0008, +0.0151] corridas=600 -> NO_INFERIOR
NULOS SL n=50 media=0.6659 max=0.7955 W=0.9465 iguales_o_mejores=0 p_sup=0.0196
NULOS T n=50 media=0.7598 max=0.8390 W=0.9465 iguales_o_mejores=0 p_sup=0.0196
CHEQUEO REPRODUCE_F2 corridas_comparadas=90 tolerancia=True exacto=True -> True
# cuentas de la corrección
0,9465 − 0,6659 = 0,2806 | 0,9465 − 0,7598 = 0,1867 | 0,9465 − 0,7955 = 0,1510 | 0,9465 − 0,8390 = 0,1075
# conectividad del banco (workflow factorial3-mosca.yml, 6a7b4cb)
CONN_URL: https://raw.githubusercontent.com/philshiu/Drosophila_brain_model/main/Connectivity_783.parquet
# literatura
Shiu et al., "A Drosophila computational brain model reveals sensorimotor processing", Nature 2024, doi 10.1038/s41586-024-07763-9 (LIF del cerebro entero, validado con optogenética y conducta)
# parche del CONTEXTO (copia en brain-env)
9560f3384cc4a299ea665c7f8243c803  parche.py | md5 antes b06c5c62… -> despues acf55ada… PARCHE OK
```

## Archivos

- **main:**
  - este archivo;
  - `tools/contexto/actualizar_contexto_2026-10-13-011.py` (`9560f338…`);
  - `.github/workflows/contexto-2026-10-13-011.yml`.

## NO MEDIDO

- **Nada fuera de simulación:** ni robot, ni dron, ni mosca real.
- **Otro conectoma.** El banco lee columnas de FlyWire v783.
- **Que el plano gane en hardware.** «Conviene el plano» es costo y acierto en simulación, no una prueba en hardware.
- **Los nulos de R2 en las 6 celdas, y R2 con LIQ o sin inhibición.**
- **El depósito del Paper 2.** No existe: es material, no manuscrito.

## Antes de firmar

| Afirmación | Instrumento | ¿Podía dar rojo? |
|---|---|---|
| El cableado pesa en las tres escalas | nulos SL y T sellados en 015, factorial 1 y factorial 3 | Sí: en las tres podía dar p alto |
| Sólo R2 alcanza al diseño | factorial 2 y 3, misma regla con los mismos sensores, margen 0,01 | Sí: R1 podía dar NO_INFERIOR y no lo dio |
| La corrección del 15 a 28 | cuentas sobre `agregado.log` | Sí |
| Shiu usa el mismo archivo | CONN_URL del workflow | Sí |

```
--- METODO PROMETEO ---
Accion delicada: no (sintesis)
Maquina: brain-env (lectura y prueba del parche) | web
Artefactos: docs/agents/respuestas/2026-10-13-011-en-criollo-el-cableado-pesa-y-solo-con-33-mil-neuronas-alcanza-al-diseno.md + Doc de ClickUp 2026-10-13-011
```
