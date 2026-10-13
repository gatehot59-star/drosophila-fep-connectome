# 2026-10-13-003 · En criollo: la mosca da el plano, y con suficiente cableado real su simulación lo alcanza (13-oct, 08:08)

Sigue a la 2026-10-13-002. Síntesis: no hay mediciones nuevas; cada número sale de un recibo commiteado (tabla al final).

**Veredicto primero.**

- [CONCLUSIÓN] **Qué logramos.** Probamos, con instrumentos que podían dar rojo, que el cableado real de la mosca lleva el comportamiento. En la tarea de escapar, aterrizar y girar les gana a 600 versiones barajadas (015). Con 1.504 neuronas reales, alcanza al diseño idealizado de la propia mosca (002). La brecha que veíamos anoche era nuestro recorte, no la mosca.
- [CONCLUSIÓN] **Qué no logramos.** No tenemos un cerebro que supere a su plano ni a la ingeniería: con los mismos sensores, empata. Todo es simulación.
- [CONCLUSIÓN] **Potencial.** Lo valioso es el plano: qué tipo de sensor va a qué comando. Cabe en pocos KB y no se entrena. El conectoma sirve para encontrar y validar planos; para un robot, el plano idealizado ya rinde lo mismo.
- [CONCLUSIÓN] **Hacia dónde.** Revancha sellada con sensores iguales y varias semillas; cerrar la v2 con los cuatro hallazgos abiertos de Tao; arreglar el enjambre antes de tocar hardware.

## Lo que logramos, en criollo y con número
1. **El mapa funciona y es reproducible.** FlyWire v783 completo (138.639 neuronas, 15.091.983 conexiones), bajado de fuentes públicas con el mismo md5 en brain-env y en Actions. Las 10 predicciones de la literatura del catálogo están en el cableado (2026-10-12-002), como aristas, no como función.
2. **El cableado importa, medido (015).** Con las etiquetas de la mosca (LC4 y LPLC2 a DNp01 para escapar, LPLC4 a DNp07 para aterrizar, LPLC1 y LPLC2 a DNp06 para girar) y sin entrenar nada, el cableado real les gana a 300 barajados de conexiones y 300 de sintonias en 6 de 6 condiciones.
3. **La "regla a mano" que nos ganaba era la mosca misma, idealizada (018).** Nuestro motivo de 46 neuronas llevaba el 2,18 % de lo que reciben las seis descendentes y nada de su inhibición (36,3 %).
4. **Con más mosca, alcanza a la mosca (002).** Con 1.504 neuronas reales y su inhibición, la simulación empata con el diseño idealizado cuando los dos miran los mismos 418 sensores (6 de 6 condiciones) y les gana a sus barajados (0,937 contra 0,774 y 0,742). La inhibición ayuda cuando el estímulo es fuerte. La neurona líquida nativa no agrega nada sobre la de tasa; nuestro LIF empeora.
5. **El método aguanta auditorías.** Sellos antes de correr, un ancla que reproduce exacto en dos máquinas, una auditoría externa (Tao) verificada punto por punto (2026-10-13-001) y la fábrica corriendo 9 trabajos en paralelo en 46 minutos a costo cero.

## Lo que no hay que vender
- No es un cerebro entrenable mejor que lo clásico (2026-10-12-006 y 017; Tao coincide).
- "Alcanza" no es "supera" ni "equivalente": es un empate sin margen pre-registrado, con una sola tirada de semillas, y el chequeo de los sensores fue post-hoc.
- Todo es simulación. El código del enjambre tiene desbordes y un test que no puede fallar.
- La v2 del paper tiene cuatro hallazgos abiertos (F01, F05, F06, F07): todavía no se deposita.

## Potencial
- **Reflejos para robots y drones.** Escape, aterrizaje y giro ante algo que se agranda, con el plano de la mosca: sensores tipados, un promedio por tipo y lado, y una carrera de umbrales. Es chico (KB), no se entrena, y ahora sabemos que la red real con cableado suficiente rinde lo mismo que ese plano.
- **Un método para decir qué parte del cableado importa.** El factorial muestra que el recorte decide. Con la revancha sellada, eso es un paper 2.
- **El paper 1 v2,** que cierra con las correcciones que faltan.
- **El laboratorio como verificador.** Sello, nulos, ancla y fábrica sirven para otros conectomas, por ejemplo BANC para la parte motora.

## Hacia dónde vamos, en orden
1. **Revancha sellada (factorial 2).** La regla con los mismos sensores que la red, varias semillas de τ y de prueba, margen de equivalencia pre-registrado y R2 (33.489 neuronas) en Kaggle con GPU. Falsador: si con sensores iguales y varias semillas la red pierde con el plano, la mosca simulada no le agrega nada al plano.
2. **Cerrar la v2.** Aplicar F01, F06 y F07 (texto) y decidir F05: recuperar el productor de la Tabla 8 o sacar Z_CP del resumen. Después, merge del PR #27 y token de Zenodo (de Abraham).
3. **Robótica.** Primero enteros seguros y tests que puedan fallar en el enjambre; después el reflejo en lazo cerrado en simulación, con el plano y la red R1 como rivales; recién ahí hardware.
4. **Más adelante.** El factorial topología por semilla de la líquida entrenada (P1 de Tao).

## Pedido
"een criollo que logramos, potencial, acia donde vamos" (13-oct, 08:08).

## Herramientas y máquina
- brain-env: clon de main en `009d880`; lectura del CONTEXTO (md5 9429c509833ce877d02cb67155d9b38d, 385 líneas); prueba del parche del CONTEXTO sobre una copia (md5 después 6bc1a251853f92ed4cc5326cef22dc8f, 402 líneas).
- ClickUp: búsqueda de novedades desde la 01:30 (nada nuevo de Tao); Doc de esta respuesta.
- GitHub MCP: este commit en main (respuesta, herramienta y workflow del CONTEXTO).
- Actions x64: aplica el parche del CONTEXTO y se retira.

## Qué se midió
Nada nuevo. Cada número viene de un recibo:

| Número | Recibo |
|---|---|
| 138.639 neuronas, 15.091.983 conexiones, md5 de insumos | 2026-10-13-001 (F01) y 2026-10-13-002 (versiones) |
| 10/10 predicciones como aristas | 2026-10-12-002 |
| 6/6 contra 300 SL y 300 T | 2026-10-12-018 (lectura de la 015) |
| 2,18 % de la entrada y 0 de la inhibición | 2026-10-12-018 |
| R1 iguala a la regla de 418 en 6/6; 0,937 contra 0,774 y 0,742 | 2026-10-13-002 |
| F01, F05, F06 y F07 abiertos | 2026-10-13-001 |
| 9 trabajos, 46 minutos | 2026-10-13-002 (run 38346117181) |

## Evidencia cruda
La de los recibos citados. Parche del CONTEXTO probado en brain-env:
```
md5 antes 9429c509833ce877d02cb67155d9b38d
ANCLA apariciones=1 (x4)
md5 despues 6bc1a251853f92ed4cc5326cef22dc8f
PARCHE OK
```

## Archivos
- Este archivo.
- `tools/contexto/actualizar_contexto_2026-10-13.py` (md5 ce53d77a4169972c7355df703698a592) y `.github/workflows/contexto-2026-10-13.yml`, que lo aplica y se borra.

## NO MEDIDO
- Todo lo que dicen los NO MEDIDO de la 2026-10-13-001 y la 002: equivalencia, otras semillas, otro LIF, R2, hardware.
- Que el bot aplique el parche con el mismo md5 que brain-env: se verifica después de este commit.

--- METODO PROMETEO ---
Accion delicada: no
Maquina: brain-env | Actions x64
Artefactos: docs/agents/respuestas/2026-10-13-003-en-criollo-la-mosca-da-el-plano-y-con-cableado-suficiente-su-simulacion-lo-alcanza.md + Doc de ClickUp 2026-10-13-003
