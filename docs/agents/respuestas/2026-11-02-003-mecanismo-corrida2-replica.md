# 2026-11-02-003 · La corrida 2 de H_MECANISMO replica a la corrida 1 espiga por espiga: 330 ensayos, 646.130 cuentas y 6.640.717 espigas de la red entera, idénticas · el veredicto todavía no está leído

Doc: https://app.clickup.com/90171457413/docs/2kza6fw5-26157/2kza6fw5-29317
Rama: titan/mecanismo-2026-11-02, sin merge.
Corrida 1: run 41410027436, evidencia en results/mecanismo_2026-11-02/actions_correr (f323befc7cc07b86c43ed284188e966ac898711c).
Corrida 2: run 41459331354 (completed/success, 22 de 22 trabajos), fuente b3b398d, evidencia en results/mecanismo_2026-11-02/actions_correr2 (8ffdfc6a30cf7f91e07617a576c106bfd277b497), 76 archivos, MD5SUMS sin discrepancias.
Comparador: results/mecanismo_2026-11-02/verificacion_replica/ (b64fde07c1b9c91d8dc168dc7fca95e079a79141).

## 1. Pedido

«Verificá que la corrida 2 replique la corrida 1» (2-nov-2026, 11:27 ART). Es el chequeo que la enmienda ENMIENDA-MECANISMO-2026-11-02.md puso antes de leer cualquier veredicto.

## 2. Herramientas declaradas

- brain-env (MUDH gateway, python): bajé los 76 archivos del commit 8ffdfc6a por raw.githubusercontent, chequeé MD5SUMS y corrí un comparador propio (verificar_replica.py), que no importa nada del instrumento.
- API pública de GitHub sin token: estado del run y lista de archivos del commit (unas 5 llamadas).
- GitHub MCP: push del comparador y su salida a titan/mecanismo-2026-11-02 (b64fde0) y de este archivo a main.
- ClickUp: una página nueva en el Doc Topo inverso.
- Cuota ajena: ninguna nueva en Actions.

## 3. Qué se midió

- «La corrida 2 replica a la corrida 1» → comparador de todo el JSON de cada celda salvo tiempos de reloj (semillas, cuentas de todas las neuronas observadas, espigas totales de la red entera, neuronas activas, primera espiga de D, espigas tempranas, conjuntos, pines, filas tocadas) → sí podía dar rojo: el control negativo detecta 1 espiga de más en una neurona, 1 espiga de menos en el total de la red y una semilla corrida → **IDENTICA** en las 9 celdas comunes (ctrl_mn9 y las 8 de tasas): 330 ensayos, 646.130 cuentas, 6.640.717 espigas de la red.
- «Los dos C0 de cada celda principal partida son iguales» → el mismo comparador, sin usar unir_celdas.py → sí → **IDENTICO** en las 4 (20 ensayos cada una). Coincide con lo que registró unir_celdas.py: cuatro UNIDA, EXIT_UNIR=0.
- «Cada trabajo corrió el código de la enmienda sobre los datos fijados» → líneas OK de sha256sum/md5sum en cada log, PINES y SOURCE_COMMIT → sí → 21 de 21 logs con 14 OK, pines true, fuente b3b398d y FIN.
- «La corrida 2 es cómputo nuevo, no una copia de la 1» → tiempos de reloj por ensayo y por celda → sí → distintos. Ejemplos: t20_LC4_right 1.091 s en la corrida 1 y 236 s en la 2 (primer ensayo de C0: 76,6 s contra 100,0 s); t150_LPLC2_right 3.218 s contra 369 s; ctrl_mn9 216 s contra 100 s.

Conclusión: el aislamiento por proceso de la enmienda no cambió ni una espiga, y el modelo de Shiu es determinista dada la semilla en estas máquinas. La corrida 2 queda en condiciones de leerse. No hay en esta respuesta ninguna lectura del veredicto.

Dato de costado: con un proceso nuevo por ensayo las celdas tardaron entre 2 y 9 veces menos. Encaja con la memoria acumulada como causa de la caída de la corrida 1; la causa sigue NO MEDIDA.

## 4. Evidencia cruda

Comando (brain-env, Python 3.12): `python3 verificar_replica.py --c1 actions_correr --c2 actions_correr2`. Salida completa (verificacion_replica.log; el script publicado, vuelto a correr, da exactamente esta salida):

```text
CONTROL_NEGATIVO detecta_1_espiga=True detecta_espigas_red=True detecta_semilla=True identico_consigo=True
REPLICA ctrl_mn9 IDENTICA ensayos=10 cuentas=210 espigas_red=89142 pines=True target=auto/auto
REPLICA t20_LC4_right IDENTICA ensayos=40 cuentas=75080 espigas_red=79080 pines=True target=auto/auto
REPLICA t20_LPLC2_right IDENTICA ensayos=40 cuentas=85320 espigas_red=315640 pines=True target=auto/auto
REPLICA t20_LPLC1_right IDENTICA ensayos=40 cuentas=72520 espigas_red=455729 pines=True target=auto/auto
REPLICA t20_LPLC4_right IDENTICA ensayos=40 cuentas=90040 espigas_red=256971 pines=True target=auto/auto
REPLICA t150_LC4_right IDENTICA ensayos=40 cuentas=75080 espigas_red=695642 pines=True target=auto/auto
REPLICA t150_LPLC2_right IDENTICA ensayos=40 cuentas=85320 espigas_red=1689854 pines=True target=auto/auto
REPLICA t150_LPLC1_right IDENTICA ensayos=40 cuentas=72520 espigas_red=1569905 pines=True target=auto/auto
REPLICA t150_LPLC4_right IDENTICA ensayos=40 cuentas=90040 espigas_red=1488754 pines=True target=auto/auto
TOTAL ensayos=330 cuentas=646130 espigas_red=6640717
C0_A_B p_LC4_right IDENTICO ensayos=20
C0_A_B p_LPLC2_right IDENTICO ensayos=20
C0_A_B p_LPLC1_right IDENTICO ensayos=20
C0_A_B p_LPLC4_right IDENTICO ensayos=20
LOG medir_ctrl_mn9.log ok_lines=14 pines=True fuente=b3b398d fin=True
LOG medir_i_LC4_left.log ok_lines=14 pines=True fuente=b3b398d fin=True
LOG medir_i_LPLC1_left.log ok_lines=14 pines=True fuente=b3b398d fin=True
LOG medir_i_LPLC2_left.log ok_lines=14 pines=True fuente=b3b398d fin=True
LOG medir_i_LPLC4_left.log ok_lines=14 pines=True fuente=b3b398d fin=True
LOG medir_p_LC4_right_a.log ok_lines=14 pines=True fuente=b3b398d fin=True
LOG medir_p_LC4_right_b.log ok_lines=14 pines=True fuente=b3b398d fin=True
LOG medir_p_LPLC1_right_a.log ok_lines=14 pines=True fuente=b3b398d fin=True
LOG medir_p_LPLC1_right_b.log ok_lines=14 pines=True fuente=b3b398d fin=True
LOG medir_p_LPLC2_right_a.log ok_lines=14 pines=True fuente=b3b398d fin=True
LOG medir_p_LPLC2_right_b.log ok_lines=14 pines=True fuente=b3b398d fin=True
LOG medir_p_LPLC4_right_a.log ok_lines=14 pines=True fuente=b3b398d fin=True
LOG medir_p_LPLC4_right_b.log ok_lines=14 pines=True fuente=b3b398d fin=True
LOG medir_t150_LC4_right.log ok_lines=14 pines=True fuente=b3b398d fin=True
LOG medir_t150_LPLC1_right.log ok_lines=14 pines=True fuente=b3b398d fin=True
LOG medir_t150_LPLC2_right.log ok_lines=14 pines=True fuente=b3b398d fin=True
LOG medir_t150_LPLC4_right.log ok_lines=14 pines=True fuente=b3b398d fin=True
LOG medir_t20_LC4_right.log ok_lines=14 pines=True fuente=b3b398d fin=True
LOG medir_t20_LPLC1_right.log ok_lines=14 pines=True fuente=b3b398d fin=True
LOG medir_t20_LPLC2_right.log ok_lines=14 pines=True fuente=b3b398d fin=True
LOG medir_t20_LPLC4_right.log ok_lines=14 pines=True fuente=b3b398d fin=True
REPLICA_CORRIDA2 PASS
```

unir_stdout.log de la corrida 2:

```text
UNION p_LC4_right {"C0_igual": true, "a": "p_LC4_right_a", "b": "p_LC4_right_b", "estado": "UNIDA", "indices_igual": true, "pines_igual": true}
UNION p_LPLC2_right {"C0_igual": true, "a": "p_LPLC2_right_a", "b": "p_LPLC2_right_b", "estado": "UNIDA", "indices_igual": true, "pines_igual": true}
UNION p_LPLC1_right {"C0_igual": true, "a": "p_LPLC1_right_a", "b": "p_LPLC1_right_b", "estado": "UNIDA", "indices_igual": true, "pines_igual": true}
UNION p_LPLC4_right {"C0_igual": true, "a": "p_LPLC4_right_a", "b": "p_LPLC4_right_b", "estado": "UNIDA", "indices_igual": true, "pines_igual": true}
EXIT_UNIR=0
```

RESULTADO.txt de la corrida 2: `censo=success medir=success fuente=b3b398d8e50a548fa5df5ee4ecc7946bd19c0191 run=41459331354`.

## 5. Archivos generados

- titan/mecanismo-2026-11-02: results/mecanismo_2026-11-02/verificacion_replica/verificar_replica.py (sha256 20bf8c2a…) y verificacion_replica.log (c7b52b8a…).
- main: este archivo.

## 6. NO MEDIDO

- El veredicto de H_MECANISMO: no lo leí ni lo verifiqué en esta respuesta.
- Las celdas principales y la réplica izquierda no tienen contraparte en la corrida 1; esta comparación no las toca (salvo que los dos C0 de cada principal coinciden entre sí).
- La causa de la caída de la corrida 1.
- CONTEXTO-drosophila-fep.md sigue sin actualizar; se actualiza con la lectura del veredicto.

--- METODO PROMETEO ---
Accion delicada: NO. Comparacion de evidencia ya publicada, sin relanzar nada.
Modo aplicado: FULL.
Maquina: brain-env (2 CPU).
Instrumento con capacidad de dar rojo: comparador estructural con control negativo de 1 espiga, semilla y total de red.
NO MEDIDO declarado: veredicto de la hipotesis y causa de la caida de la corrida 1.
Review externo: no
