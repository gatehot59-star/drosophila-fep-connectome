# 2026-10-14-039 · H_TAU_LIBRE sellado: el control de la tau elegida, con taus que nadie eligio para el real ni para los nulos

## Pedido

- 15-oct 18:41, ClickKit `sellar_control_tau_039`: sellar el control de tau que propuso la 038.

## Veredicto primero

- [CONCLUSION] Sellado `tools/taulibre/SELLO-TAU-LIBRE.md` en la rama `titan/taulibre-2026-10-15` (desde `8d305e9`), commit `fec8472`, md5 3886aa58449dfff9a3f9dac88015b5a4. Solo el documento: ningun script escrito ni corrido.
- [MEDIDO] Por que hace falta, de los json de H_TAU (`results/htau_2026-10-14/htau_c0` a `c5`): con las lineas sin entrenar, la tau elegida (10) le saca a la peor (14) de 2,2 a 4,2 puntos en prueba (0,9413 a 0,9467 contra 0,9043 a 0,9218), y a la mediana de validacion de 0,6 a 1,0 puntos. El delta mas chico de H_LECTOR_CABLEADO (SL c2, +3,4) es de ese orden.
- [NO MEDIDO] H_TAU_LIBRE entero, y cuanto pesa la eleccion de tau con el lector entrenado.

## Que fija el sello

- Real y nulos con taus frescas (semillas 20 a 29): nadie elige tau en ningun brazo.
- Los mismos 40 nulos SL y T de H_LECTOR en c2 y c5, prueba 12, mismo lector L. El nulo k usa la tau 20 + (k mod 10) y se compara con la red real de esa misma tau.
- p apareado = (1 + nulos que igualan o superan a su real) / 41; delta = media de real menos nulo. SUPERA con p <= 0,05 y delta > 0,01; SOSTENIDA si SUPERA en las 4 (interseccion-union); REFUTADA si algun delta < 0,01 o algun p > 0,10.
- Controles nuevos: REPRO_LECTOR (con tau 10 se reproduce el real de H_LECTOR caracter por caracter), NULOS_IGUAL_LECTOR (mismos grafos nulos) y TAU_FRESCA (20 a 29 sin uso previo).
- Expectativa declarada: c5 probablemente sobrevive; c2 queda abierta.
- Costo estimado: 20 trabajos en Actions (el tope de simultaneos), unas 2 horas. Humo ciego antes del CORRER.

## Herramientas y maquina

- brain-env: lectura de `lector_mosca.py`, `htau_mosca.py`, `factorial2_mosca.py` y de los json de H_TAU en `8d305e9`; busqueda de semillas de tau usadas (0 a 9 en los factoriales, 10 a 19 en H_TAU, 1 y 2 en la entrada por tipos).
- GitHub: rama nueva y commit del sello.

## Archivos

| Archivo | md5 | Donde |
|---|---|---|
| `tools/taulibre/SELLO-TAU-LIBRE.md` | 3886aa58449dfff9a3f9dac88015b5a4 | `titan/taulibre-2026-10-15`, `fec8472` |
| esta respuesta | (en el chat y el Doc) | `main` |
| `tools/contexto/actualizar_contexto_2026-10-14-039.py` | a667385d876e51988e704b5bee2a8957 | `main` |

## NO MEDIDO

- H_TAU_LIBRE, su humo y su costo real.
- Si la busqueda de semillas usadas fue completa: la hice con grep sobre `tools/` y los sellos; el control TAU_FRESCA la repite sobre los json.

## Antes de firmar

- El sello puede dar rojo: si c2 cae por debajo de 1 punto en una sola familia, H_TAU_LIBRE sale REFUTADA y H_LECTOR_CABLEADO queda como dependiente de la tau elegida.
- La hora del sello: commit 18:43:36; el documento no trae hora propia.
- No toca la primaria de H_LECTOR (CERCA y PAGA), que sigue con tau 10 (limitacion 4 del sello).

--- METODO PROMETEO ---
Rol: investigacion (pre-registro). Delicado: no, documento solo.
Maquina: brain-env.
Artefactos: sello en `titan/taulibre-2026-10-15` (`fec8472`); esta respuesta y el parche del CONTEXTO en `main`; Doc de ClickUp de la 039.
