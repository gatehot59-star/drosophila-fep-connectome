# 2026-10-14-040 · Instrumento y humo de H_TAU_LIBRE: todo VALIDO, la tau 10 reproduce H_LECTOR exacto, y el CORRER listo para disparar

## Pedido

- 15-oct 18:47, ClickKit `instrumento_taulibre_040`: escribir el instrumento y el humo de H_TAU_LIBRE (sello `fec8472`).

## Veredicto primero

- [MEDIDO] Humo en Actions x64 (run 38816081787, disparado por `930f0d7`, bot `c3e07cd`): las 5 partes en verde y VALIDO.
- [MEDIDO] REPRO_LECTOR: con tau 10, el instrumento nuevo reproduce el real de H_LECTOR caracter por caracter en c2 (WL 0,9910, lambda 0,001) y en c5 (WL 0,9930, lambda 0,01). El instrumento lee la misma red con el mismo lector.
- [MEDIDO] NULOS_IGUAL_LECTOR: los 40 grafos SL de c2 y los 40 T de c5 dan los mismos destinos o tipos cambiados (y el mismo radio en SL) que en H_LECTOR. Los nulos son los mismos; solo cambia la tau.
- [MEDIDO] TAU_FRESCA: las semillas usadas antes son 0 a 19; 20 a 29 estan libres. CONTROL_NEGATIVO 0,5000 contra azar 0,5000 en c2 y c5. Prueba del agregador 11/11 (con un rojo a proposito).
- [CONCLUSION] El instrumento esta listo. Ningun acierto con tau fresca se imprimio: H_TAU_LIBRE sigue sin medir.
- [NO MEDIDO] La corrida completa (`results/taulibre_2026-10-15/CORRER`), que espera el si de Abraham.

## Herramientas y maquina

- brain-env (Python 3.12.14, numpy 2.5.3), antes de commitear: prueba 11/11; reales c2 tau 20 en modo local VALIDO (log md5 1013c01f, 401 s); humo de nulos T c5 VALIDO, 40 de 40 grafos iguales (7ead4a41, 397 s); humo de nulos SL c2 con 3 grafos VALIDO (f5373de2, 406 s). El REPRO_LECTOR a tamano completo corre tambien en brain-env, en curso.
- GitHub Actions x64: el humo.

## Archivos

En la rama `titan/taulibre-2026-10-15`, verificados desde un clon fresco:

| Archivo | md5 | Commit |
|---|---|---|
| `tools/taulibre/SELLO-TAU-LIBRE.md` | 3886aa58449dfff9a3f9dac88015b5a4 | `fec8472` (sin editar) |
| `tools/taulibre/taulibre_mosca.py` | c65bebe270da1e0526a212cff29830fd | `930f0d7` |
| `tools/taulibre/agregar_taulibre.py` | 340dc41aa6fde80166121c5db6c9b095 | `930f0d7` |
| `tools/taulibre/prueba_taulibre.py` | 9f74f63d405ce5eaea322d2923a2cf6d | `930f0d7` |
| `.github/workflows/taulibre-humo.yml` | 9eb2a2332511ea521fcca25bf8271cba | `930f0d7` |
| `.github/workflows/taulibre-mosca.yml` | c94e9eeb4baa7e438ed312b9eaf0ed23 | `930f0d7` |
| `results/taulibre_2026-10-15_humo/actions/MD5SUMS.txt` | 28db6857380f74b80405d67408b9e11f (14 de 14 OK) | `c3e07cd` |

Logs del humo:

| Parte | log md5 | duracion |
|---|---|---|
| reales c2 (REPRO + ruta tau 20) | 9a90db5043c601755aa9b17c88422bac | 576,5 s |
| reales c5 (REPRO + ruta tau 20) | bd045e8a603d8eab2cf1696990697813 | 712,8 s |
| nulos SL c2 (40 grafos + ruta) | 59bc8a79dac1ca5fc679947a877bc0bb | 134,5 s |
| nulos T c5 (40 grafos + ruta) | bc535ada6a6ed4884c4929912d05d0bd | 120,0 s |
| prueba | 86aae61655e1bb326cf7a4d919ea688f | |

En `main`: esta respuesta, `tools/contexto/actualizar_contexto_2026-10-14-040.py` y `.github/workflows/contexto-2026-10-14-040.yml` (se borra solo al aplicar).

## Desvios declarados

1. El sello pedia los controles de H_LECTOR por corrida. CONTROL_NEGATIVO corre una vez por trabajo de reales (con la primera tau), no en cada nulo, como en H_LECTOR.
2. El instrumento importa `lector_mosca.py` y copia de alli la construccion de los nulos (SL y T) en dos funciones; NULOS_IGUAL_LECTOR la controla grafo por grafo.
3. REPRO_LECTOR a tamano completo no se corrio en brain-env antes del commit (tarda una hora con la replica de H_RIVAL en la misma maquina): su primera corrida fue este humo. Dio exacto en las dos celdas.

## NO MEDIDO

- H_TAU_LIBRE: aciertos con tau fresca, deltas y p.
- La duracion de la corrida completa. Estimacion desde H_LECTOR: unos 10 minutos por corrida; reales de 50 a 60 min (los de tau 20 con REPRO, una corrida mas) y nulos de unas 2 horas.

## Antes de firmar

- REPRO_LECTOR podia dar rojo: cualquier cambio en la red, los datos, el lector o la tau rompe la cadena de 2000 predicciones. Dio igual.
- NULOS_IGUAL_LECTOR podia dar rojo: con otra semilla de barajado los destinos cambiados difieren. Dio 80 de 80.
- La prueba incluye el caso de apareo: un real que cae con una tau y sus 4 nulos que lo superan refuta aunque el promedio sin aparear le ganaria. Los dos brazos no son la misma funcion.
- Expectativa del sello, sin cambios: c5 probablemente sobrevive, c2 abierta.

--- METODO PROMETEO ---
Rol: implementacion del sello y humo. Delicado: no (sin corrida completa).
Maquina: brain-env y GitHub Actions x64.
Artefactos: rama `titan/taulibre-2026-10-15` (instrumento `930f0d7`, humo `c3e07cd`); esta respuesta y el parche del CONTEXTO en `main`; Doc de ClickUp de la 040.
