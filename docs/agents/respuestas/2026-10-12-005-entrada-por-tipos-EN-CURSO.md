# 2026-10-12-005 · Entrada visual por tipo de neurona (EN CURSO, parcial)

Doc: https://app.clickup.com/90171457413/docs/2kza6fw5-21377

**Veredicto parcial (4 de 6 celdas primarias, 9 de 12 de robustez, p crudo sin Holm):** con lector entrenado sobre las 4 descendentes, el cableado de la mosca (W) no queda arriba de SL ni de T en ninguna celda. Con LPLC4 SILENCIOSA, W queda debajo de las 300 T (p inferior 0,0033 con ruido 0,15 y 0,0066 con 0,45). Con MOVIMIENTO (robustez) W le gana a T pero no a SL. El veredicto con Holm, los controles y los rivales los escribe el log completo, que sigue corriendo y no está leído.

## 1. Pedido

Abraham escribió «PASAR A LA ENTRADA VISUAL POR TIPO DE NURONSAS» (07:36) y apretó «Entrada por tipos visuales» (08:01): la opción de la 004 (estado de vuelo a lo clásico y cada tipo visual con su entrada).

## 2. Herramientas y máquina

- brain-env (Celeron N4020, Python 3.12.14, numpy 2.5.3, torch 2.14.1 CPU): humo, calibración (parte C) y corrida desde clon fresco (partes A y B en paralelo, un hilo cada una; A desde 11:13:36 UTC, B desde 11:19:06 UTC).
- Sandbox de ClickUp: escribir el script y probar la entrada en seco.
- GitHub: rama `titan/entrada-por-tipos-2026-10-12` (desde la de la 003), pre-registro `75ca27c`; main para esta respuesta y el contexto.
- Web: una búsqueda (LPLC4 sin fisiología encontrada; Kim 2023 y Dombrovski 2025).
- Sin cuota ajena.

## 3. Qué se midió

Diseño sellado en `75ca27c` (detalle en el mensaje del commit y en el docstring del script): motivo de la 003 sin cambios; entrada por tipo (LC4 velocidad, LPLC2 tamaño y punto que pasa, LPLC4 en tres variantes declaradas); tarea de robot (amenaza: escapar; acercamiento: aterrizar en vuelo y nada en el piso; objeto que pasa: nada); lector ridge por estado de vuelo sobre las 4 descendentes; nulos SL y T (300 cada uno); Holm sobre 12 pruebas por cola; ruido 0,15 y 0,45 (calibrado sobre el rival crudo antes del sellado).

Cableado medido (log): DNp01 en W = LC4 0,498, LPLC2 0,502, LPLC4 0; DNp07 en W = 0,003, 0, 0,997; en SL (media) DNp01 = 0,209, 0,306, 0,485 y DNp07 = 0,228, 0,326, 0,445.

## 4. Evidencia cruda (verbatim, `/workspace/e005/run/A.log` y `B.log`, 11:50:25 UTC)

```
# md5 script = e060c4bffb685aa550dadc19eda3dd02   (clon fresco de 75ca27c; módulo 003 4d40477d87406c31672acfb6e6e8f5a2)
CALIBRACION ruido=0.45 rival_ridge_crudo(COMO_LPLC2,SILENCIOSA,MOVIMIENTO)=(0.8978,0.8750,0.9472) media=0.9067
CALIBRACION ruido=0.60 rival_ridge_crudo(COMO_LPLC2,SILENCIOSA,MOVIMIENTO)=(0.8439,0.7956,0.8950) media=0.8448
CALIBRACION ruido_dificil=0.45 (el mas alto de la grilla con rival ridge crudo medio >= 0.90)
CELDA PRIMARIA tau_semilla=0 variante=COMO_LPLC2 ruido=0.15 W=0.7861 por_clase(nada,esc_izq,esc_der,aterr)=0.800,0.737,0.770,0.810 | SL media=0.8509 max=0.9567 igualan=278/300 p_sup=0.9269 p_inf=0.0797 | T media=0.7910 max=0.8289 igualan=214/300 p_sup=0.7143 p_inf=0.3123 | 329.0 s
CELDA PRIMARIA tau_semilla=0 variante=COMO_LPLC2 ruido=0.45 W=0.6956 por_clase(nada,esc_izq,esc_der,aterr)=0.740,0.560,0.607,0.787 | SL media=0.7330 max=0.8250 igualan=266/300 p_sup=0.8870 p_inf=0.1262 | T media=0.7057 max=0.7244 igualan=264/300 p_sup=0.8804 p_inf=0.1395 | 622.3 s
CELDA PRIMARIA tau_semilla=0 variante=SILENCIOSA ruido=0.15 W=0.7722 por_clase(nada,esc_izq,esc_der,aterr)=0.779,0.730,0.757,0.810 | SL media=0.8399 max=0.9572 igualan=278/300 p_sup=0.9269 p_inf=0.0764 | T media=0.8468 max=0.8894 igualan=300/300 p_sup=1.0000 p_inf=0.0033 | 547.4 s
CELDA PRIMARIA tau_semilla=0 variante=SILENCIOSA ruido=0.45 W=0.6878 por_clase(nada,esc_izq,esc_der,aterr)=0.756,0.557,0.577,0.727 | SL media=0.6794 max=0.8078 igualan=138/300 p_sup=0.4618 p_inf=0.5482 | T media=0.7156 max=0.7444 igualan=299/300 p_sup=0.9967 p_inf=0.0066 | 607.5 s
CELDA ROBUSTEZ tau_semilla=1 variante=COMO_LPLC2 ruido=0.15 W=0.8167 | SL media=0.8521 igualan=81/100 | T media=0.7988 igualan=8/100
CELDA ROBUSTEZ tau_semilla=1 variante=COMO_LPLC2 ruido=0.45 W=0.7133 | SL media=0.7335 igualan=75/100 | T media=0.7156 igualan=68/100
CELDA ROBUSTEZ tau_semilla=1 variante=SILENCIOSA ruido=0.15 W=0.7833 | SL media=0.8396 igualan=91/100 | T media=0.8533 igualan=100/100 p_inf=0.0099
CELDA ROBUSTEZ tau_semilla=1 variante=SILENCIOSA ruido=0.45 W=0.6944 | SL media=0.6822 igualan=45/100 | T media=0.7174 igualan=100/100 p_inf=0.0099
CELDA ROBUSTEZ tau_semilla=1 variante=MOVIMIENTO ruido=0.15 W=0.8806 | SL media=0.8953 igualan=64/100 | T media=0.8074 igualan=0/100 p_sup=0.0099
CELDA ROBUSTEZ tau_semilla=1 variante=MOVIMIENTO ruido=0.45 W=0.7506 | SL media=0.7578 igualan=58/100 | T media=0.7192 igualan=2/100 p_sup=0.0297
CELDA ROBUSTEZ tau_semilla=2 variante=COMO_LPLC2 ruido=0.15 W=0.7978 | SL media=0.8544 igualan=91/100 | T media=0.7894 igualan=25/100
CELDA ROBUSTEZ tau_semilla=2 variante=COMO_LPLC2 ruido=0.45 W=0.6772 | SL media=0.7358 igualan=99/100 p_inf=0.0198 | T media=0.6992 igualan=100/100 p_inf=0.0099
CELDA ROBUSTEZ tau_semilla=2 variante=SILENCIOSA ruido=0.15 W=0.7733 | SL media=0.8448 igualan=96/100 p_inf=0.0495 | T media=0.8475 igualan=100/100 p_inf=0.0099
```

(Las líneas de robustez están recortadas a W, medias, igualan y la p relevante; las completas quedan en `B.log`.)

## 5. Archivos

- `tools/escape_aterrizaje/entrada_por_tipos.py` en la rama (`75ca27c`, md5 `e060c4bf…`).
- Esta respuesta. Los logs `A.log` y `B.log` se commitean a la rama al terminar.

## 6. NO MEDIDO

- El veredicto con Holm y el global; MOVIMIENTO en el primario; los controles (paridad, reproduce, negativo AGNOSTICA, positivo de 28 estados); el rival crudo y H3 en la corrida completa (en el humo ganaba por lejos); I2 (MLP); el resto de la robustez.
- La lectura de líneas etiquetadas (cada descendente con su umbral dispara su acción, como en la mosca), que es donde el cableado por tipos podría pagar.
- DBC3: no entra (no hay memoria que sostener).

## Antes de firmar

Nada se firma: el instrumento todavía no dio su CHEQUEO. El instrumento puede dar rojo (W debajo de T con p 0,0033) y verde (W arriba de T con MOVIMIENTO en robustez).

--- METODO PROMETEO ---
Máquina: brain-env (corrida en curso); sandbox de ClickUp para escribir
Artefactos: docs/agents/respuestas/2026-10-12-005-entrada-por-tipos-EN-CURSO.md + https://app.clickup.com/90171457413/docs/2kza6fw5-21377
