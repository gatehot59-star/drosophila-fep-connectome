# 2026-10-12-005 · Entrada visual por tipo de neurona: NO PAGA (y resumen de la 004 y la 005)

Doc: https://app.clickup.com/90171457413/docs/2kza6fw5-21397

**Veredicto:** con un lector entrenado sobre las 4 descendentes, el cableado de la mosca nunca le gana a SL (6/6 primarias, 12/12 de robustez, 3/3 con MLP). Contra T depende de LPLC4: muda pierde (Holm 0,0399), MOVIMIENTO le gana sin pasar Holm (0,1196 y 0,1462) y COMO_LPLC2 empata. VEREDICTO_GLOBAL pre-registrado: **NO PAGA (PIERDE en SILENCIOSA)**. El rival clásico crudo le gana en 6 de 6. Instrumento VALIDO.

## 0. Resumen en criollo de la 004 y la 005 (pedido de las 10:14)

**La 004 (memoria dura).** Mismo escape o aterrizaje de la 003 con la señal de vuelo al principio, cambio de contexto en la mitad de los ensayos, cuatro pulsos de engaño y el estímulo recién en el paso 90 de 120. Ni DBC3 (0,658 a 0,743) ni LSTM (0,658 a 0,672) aprenden a recordar; el lector sin memoria saca 0,656 (techo 2/3). DBC3 contra LSTM: empate en los dos tamaños. La máquina de estados clásica les gana (0,7663). Por eso el estado de vuelo va a lo clásico.

**La 005 (esta).** Cada tipo visual recibe su señal de literatura (LC4 velocidad, LPLC2 tamaño; LPLC4 en tres variantes porque no tiene fisiología publicada encontrada). El cableado de la mosca no le gana a sus barajados y el rival clásico le gana por lejos (0,88 a 0,99 contra 0,69 a 0,86). La información está en los 28 estados (0,87 a 0,99): se pierde en el embudo de 4 descendentes, porque la mosca junta LC4 y LPLC2 mitad y mitad en el GF y deja a DNp07 sólo con LPLC4. Para el robot, en esta tarea y con lector entrenado, va lo clásico; queda probar líneas etiquetadas.

## 1. Pedido

- 07:36: «PASAR A LA ENTRADA VISUAL POR TIPO DE NURONSAS»; 08:01: botón «Entrada por tipos visuales» (004). Mismo pedido.
- 10:14: «HAZ UN RESUMN DE LOS DOS ULTIMOS OUTPUT NO SE LOGRAN VER». La corrida ya había terminado: el resumen sale con la 005 cerrada (sección 0).

## 2. Herramientas y máquina

- brain-env (Celeron N4020, Python 3.12.14, numpy 2.5.3, torch 2.14.1 CPU): humo, calibración (parte C) y corrida desde clon fresco de `75ca27c` (A 60,0 min y B 53,5 min en paralelo, un hilo cada una); md5 4/4 en clon fresco de `f7844be`.
- Sandbox de ClickUp: escribir el script y probar la entrada en seco (sin torch).
- GitHub: rama `titan/entrada-por-tipos-2026-10-12` (pre-registro `75ca27c`, logs `f7844be`) y main.
- Web: LPLC4 sin fisiología encontrada; Kim 2023 (Curr Biol): LPLC2 responde a un punto que se traslada; Dombrovski 2025 (Nature): el GF recibe entrada visual directa sólo de LC4 y LPLC2.
- Sin cuota ajena.

## 3. Qué se midió

- Sujeto: el motivo de la 003 (28 neuronas, 73 aristas excitatorias e ipsilaterales, SparseLTC con τ fija heterogénea), construido con su módulo importado sin cambios.
- Entrada (E1): LC4 = velocidad de expansión saturada (von Reyn 2017; Ache 2019); LPLC2 = gaussiana del tamaño mientras hay expansión (Ache 2019; Klapoetke 2017) y 0,6 de esa gaussiana ante el punto que pasa (Kim 2023; el 0,6 es supuesto); LPLC4 = COMO_LPLC2, SILENCIOSA o MOVIMIENTO (declaradas).
- Tarea de robot (no afirma conducta de la mosca): amenaza (l/v 10 a 30 ms) → escapar al otro lado; acercamiento (150 a 300 ms) → aterrizar en vuelo, nada en el piso; objeto que pasa → nada. 2400 y 1800 ensayos; azar 0,50.
- Lector I1: ridge por estado de vuelo (mux clásico) sobre la serie de las 4 descendentes (160 rasgos). I2: MLP (descriptivo).
- Nulos: SL (función de la 003) y T (sintonías barajadas dentro de cada lado, cableado intacto), 300 cada uno en el primario y 100 en robustez.
- Reglas pre-registradas en `75ca27c`: p de rango, Holm sobre 12 pruebas por cola, GANA / PIERDE / EMPATE por celda y por variante, y global PAGA / DEPENDE DE LPLC4 / NO PAGA.
- Cambios después del humo, declarados en el pre-registro: tamaño (por tiempo), segundo ruido 0,30 → 0,45 (regla de calibración escrita antes de correr) y lugar de I2.

## 4. Evidencia cruda (verbatim de `results/entrada_por_tipos_2026-10-12/` en `f7844be`)

```
COMPOSICION dn=DNp01 fraccion_de_sinapsis(LC4,LPLC2,LPLC4) W=(0.498,0.502,0.000) SL_media=(0.209,0.306,0.485)
COMPOSICION dn=DNp07 fraccion_de_sinapsis(LC4,LPLC2,LPLC4) W=(0.003,0.000,0.997) SL_media=(0.228,0.326,0.445)
CELDA PRIMARIA tau_semilla=0 variante=COMO_LPLC2 ruido=0.15 W=0.7861 por_clase(nada,esc_izq,esc_der,aterr)=0.800,0.737,0.770,0.810 | SL media=0.8509 max=0.9567 igualan=278/300 p_sup=0.9269 p_inf=0.0797 | T media=0.7910 max=0.8289 igualan=214/300 p_sup=0.7143 p_inf=0.3123 | 329.0 s
CELDA PRIMARIA tau_semilla=0 variante=COMO_LPLC2 ruido=0.45 W=0.6956 por_clase(nada,esc_izq,esc_der,aterr)=0.740,0.560,0.607,0.787 | SL media=0.7330 max=0.8250 igualan=266/300 p_sup=0.8870 p_inf=0.1262 | T media=0.7057 max=0.7244 igualan=264/300 p_sup=0.8804 p_inf=0.1395 | 622.3 s
CELDA PRIMARIA tau_semilla=0 variante=SILENCIOSA ruido=0.15 W=0.7722 por_clase(nada,esc_izq,esc_der,aterr)=0.779,0.730,0.757,0.810 | SL media=0.8399 max=0.9572 igualan=278/300 p_sup=0.9269 p_inf=0.0764 | T media=0.8468 max=0.8894 igualan=300/300 p_sup=1.0000 p_inf=0.0033 | 547.4 s
CELDA PRIMARIA tau_semilla=0 variante=SILENCIOSA ruido=0.45 W=0.6878 por_clase(nada,esc_izq,esc_der,aterr)=0.756,0.557,0.577,0.727 | SL media=0.6794 max=0.8078 igualan=138/300 p_sup=0.4618 p_inf=0.5482 | T media=0.7156 max=0.7444 igualan=299/300 p_sup=0.9967 p_inf=0.0066 | 607.5 s
CELDA PRIMARIA tau_semilla=0 variante=MOVIMIENTO ruido=0.15 W=0.8628 por_clase(nada,esc_izq,esc_der,aterr)=0.933,0.787,0.770,0.820 | SL media=0.8901 max=0.9606 igualan=221/300 p_sup=0.7375 p_inf=0.2658 | T media=0.8028 max=0.8644 igualan=2/300 p_sup=0.0100 p_inf=0.9967 | 568.9 s
CELDA PRIMARIA tau_semilla=0 variante=MOVIMIENTO ruido=0.45 W=0.7517 por_clase(nada,esc_izq,esc_der,aterr)=0.859,0.643,0.640,0.650 | SL media=0.7543 max=0.8406 igualan=157/300 p_sup=0.5249 p_inf=0.4817 | T media=0.7131 max=0.7578 igualan=3/300 p_sup=0.0133 p_inf=0.9934 | 601.4 s
CONTROL_NEGATIVO entrada=AGNOSTICA W=0.7656 T_identicos=30/30 -> True | SL descriptivo (como la 003) media=0.8437 max=0.8917 igualan=99/100 p_sup=0.9901 p_inf=0.0198
RIVAL variante=COMO_LPLC2 ruido=0.15 W_ridge_4DN=0.7861 control_positivo_ridge_28=0.9844 rival_ridge_crudo_24=0.9867 rival_mlp_crudo_24=0.9789 | H3 W contra ridge crudo 2 contra 363 p=1.78e-105 -> PEOR
RIVAL variante=COMO_LPLC2 ruido=0.45 W_ridge_4DN=0.6956 control_positivo_ridge_28=0.9028 rival_ridge_crudo_24=0.8978 rival_mlp_crudo_24=0.8617 | H3 W contra ridge crudo 41 contra 405 p=2.3e-76 -> PEOR
RIVAL variante=SILENCIOSA ruido=0.15 W_ridge_4DN=0.7722 control_positivo_ridge_28=0.9750 rival_ridge_crudo_24=0.9783 rival_mlp_crudo_24=0.9700 | H3 W contra ridge crudo 5 contra 376 p=2.68e-104 -> PEOR
RIVAL variante=SILENCIOSA ruido=0.45 W_ridge_4DN=0.6878 control_positivo_ridge_28=0.8717 rival_ridge_crudo_24=0.8750 rival_mlp_crudo_24=0.8256 | H3 W contra ridge crudo 48 contra 385 p=1.97e-66 -> PEOR
RIVAL variante=MOVIMIENTO ruido=0.15 W_ridge_4DN=0.8628 control_positivo_ridge_28=0.9867 rival_ridge_crudo_24=0.9906 rival_mlp_crudo_24=0.9878 | H3 W contra ridge crudo 1 contra 231 p=6.75e-68 -> PEOR
RIVAL variante=MOVIMIENTO ruido=0.45 W_ridge_4DN=0.7517 control_positivo_ridge_28=0.9300 rival_ridge_crudo_24=0.9472 rival_mlp_crudo_24=0.9094 | H3 W contra ridge crudo 13 contra 365 p=1.41e-90 -> PEOR
CHEQUEO INSTRUMENTO guarda_SL=True guarda_T=True paridad_simulacion=True reproduce_ridge=True control_negativo(T identico con entrada AGNOSTICA)=True control_positivo(ridge 28 estados >= 0.75 con ruido 0.15)=True -> VALIDO
VEREDICTO_CELDA variante=SILENCIOSA ruido=0.15 holm_sup(SL,T)=(1.0000,1.0000) holm_inf(SL,T)=(0.7641,0.0399) -> PIERDE
VEREDICTO_CELDA variante=SILENCIOSA ruido=0.45 holm_sup(SL,T)=(1.0000,1.0000) holm_inf(SL,T)=(1.0000,0.0731) -> EMPATE
VEREDICTO_CELDA variante=MOVIMIENTO ruido=0.15 holm_sup(SL,T)=(1.0000,0.1196) holm_inf(SL,T)=(1.0000,1.0000) -> EMPATE
VEREDICTO_CELDA variante=MOVIMIENTO ruido=0.45 holm_sup(SL,T)=(1.0000,0.1462) holm_inf(SL,T)=(1.0000,1.0000) -> EMPATE
VEREDICTO_GLOBAL -> NO PAGA (PIERDE en SILENCIOSA)
I2_MLP variante=COMO_LPLC2 ruido=0.15 W(semillas 0,1,2)=0.8650,0.8694,0.8717 | SL media=0.8754 max=0.9633 igualan_W0=19/30 p_sup=0.6452 p_inf=0.3871 | T media=0.8302 max=0.8844 igualan_W0=3/30 p_sup=0.1290 p_inf=0.9032 | 282.8 s
I2_MLP variante=SILENCIOSA ruido=0.15 W(semillas 0,1,2)=0.7728,0.7556,0.7672 | SL media=0.8360 max=0.9550 igualan_W0=25/30 p_sup=0.8387 p_inf=0.1935 | T media=0.8851 max=0.9283 igualan_W0=30/30 p_sup=1.0000 p_inf=0.0323 | 270.3 s
I2_MLP variante=MOVIMIENTO ruido=0.15 W(semillas 0,1,2)=0.9322,0.9333,0.9206 | SL media=0.9037 max=0.9583 igualan_W0=7/30 p_sup=0.2581 p_inf=0.7742 | T media=0.8393 max=0.9106 igualan_W0=0/30 p_sup=0.0323 p_inf=1.0000 | 270.3 s
CHEQUEO INSTRUMENTO (parte B, descriptiva) guarda_SL=True guarda_T=True reproduce_mlp=True -> VALIDO
```

Robustez (B.log, τ semillas 1 y 2, 100 SL y 100 T): SL iguala o supera a la mosca en 81, 75, 91, 45, 64, 58, 91, 99, 96, 61, 74 y 62 de 100; T, con SILENCIOSA, en 100/100 las cuatro veces; con MOVIMIENTO en 0, 2, 0 y 3 de 100.

## 5. Archivos

- `tools/escape_aterrizaje/entrada_por_tipos.py` (rama, `75ca27c`, md5 `e060c4bffb685aa550dadc19eda3dd02`).
- `results/entrada_por_tipos_2026-10-12/A.log` (md5 `58f795d409164278f765e9cad619e8c7`, 63 líneas), `B.log` (`8060990236765e559ab2af5490f8cef2`, 54) y `calibracion.log` (`82c971ae293fe8320a962b0ec9a0ba57`, 45), en `f7844be`; md5 4/4 en clon fresco.
- `resultados.json` derivados sin commitear: A `513876aae46f36975ea7433a22731e0c`, B `0fe63b301b8810e29a01567a79d45c19`, C `7cc5fd1ac1d4dcc01868828702f3cf1c`.
- Esta respuesta, el contexto reescrito y los punteros en `2026-10-12-005-entrada-por-tipos-EN-CURSO.md` y `docs/agents/CONTEXTO-005-EN-CURSO.md`.

## 6. NO MEDIDO

- Líneas etiquetadas (cada descendente con su umbral dispara su acción), que es donde el cableado por tipos podría pagar.
- Fisiología de LPLC4; la amplitud 0,6 del punto en LPLC2 es supuesto.
- Otras sintonías y otros circuitos (LC6, LC9 → DNp09, LPLC1).
- DBC3 como lector con esta entrada (no hay memoria que sostener).
- Señal biológica registrada, hardware, condiciones fuera de las entrenadas y una segunda máquina.

## Antes de firmar

El instrumento podía dar rojo y verde: dio PIERDE contra T con LPLC4 muda y casi gana con MOVIMIENTO (2/300). El control negativo es exacto (30/30 idénticos). Los rivales usan exactamente las mismas 24 entradas que recibe el motivo. Lo que no se firma: que el cableado «no sirve» en general; sólo que no paga con lector entrenado en esta tarea.

## QA

VALIDO en A y en B; EXIT_RUN=0 en las dos; md5 4/4 en clon fresco; review externo no pedido (deuda, no hay PR).

--- METODO PROMETEO ---
Máquina: brain-env (Celeron N4020, torch 2.14.1 CPU, 2 procesos de 1 hilo), 60,0 y 53,5 min; sandbox de ClickUp para escribir
Artefactos: docs/agents/respuestas/2026-10-12-005-entrada-por-tipos.md + https://app.clickup.com/90171457413/docs/2kza6fw5-21397
