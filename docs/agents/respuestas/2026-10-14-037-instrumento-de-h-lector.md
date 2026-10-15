# 2026-10-14-037 · Instrumento y humo de H_LECTOR: las 8 partes de medicion VALIDO, la prueba 13/13 al reintento, y el CORRER listo para disparar

## Pedido

- 15-oct 10:44, ClickKit `instrumento_lector_037`: escribir el instrumento de H_LECTOR y su humo ciego. 10:45: "Run the H_LECTOR smoke test".
- 15-oct 11:36, ClickKit `cerrar_037`: "Cerra la 037 y lee el humo" (subir `lector-mosca.yml`, leer el humo, re-correr la prueba si cayo, escribir la 037 y pedir el CORRER solo con el humo verde).
- 15-oct 13:45: "Lee el resultado de la prueba y cerra la 037".

## Veredicto primero

- [MEDIDO] Humo en Actions x64 (run 38752555880, disparado por `a00681b`, bot `b1cb491`): las 6 celdas VALIDO. En cada una REPRO_W 10/10, REPRO_RIDGE 10/10, CONTROL_NEGATIVO 0,5000 contra azar 0,5000 (tope 0,5500), GUARDA_FUGA, PIN, HTAU_CELDA y RIVAL_CELDA en True.
- [MEDIDO] En c0, CONTROL_LECTOR_CRUDO: el ridge sobre las 22.560 entradas crudas da 2000/2000 predicciones iguales al RIDGE de H_RIVAL en la prueba 12, con el mismo lambda (10). El lector reutiliza el ridge sin cambios.
- [MEDIDO] Rutas de nulos: SL en c2 VALIDO (4.030.551 destinos cambiados, igual al factorial 3); T en c5 VALIDO (423 tipos cambiados, igual al factorial 3). NULOS_IGUAL_F3 y NULOS_VALIDOS en True.
- [MEDIDO] La prueba del instrumento cayo en ese run con exit 2 porque `tools/lector/prueba_lector.py` no estaba en `a00681b`. Reintentada sola (`lector-prueba.yml`, commit `7e6a09f`, bot `c6b1a63`): PRUEBA_LECTOR 13/13 OK, EXIT_PRUEBA=0, con los mismos md5 de los tres scripts que corrieron en brain-env.
- [CONCLUSION] El instrumento esta listo: el humo da verde completo. Ningun acierto de L se imprimio ni se guardo; H_LECTOR_CERCA, H_LECTOR_PAGA y H_LECTOR_CABLEADO siguen sin medir.
- [NO MEDIDO] La corrida completa (`results/lector_2026-10-15/CORRER`), que espera el si de Abraham.

## Herramientas y maquina

- brain-env (Python 3.12.14, numpy 2.5.3): escritura y ejecucion previa del instrumento en `/workspace/fable/l036`. Prueba 13/13; ruta SL c2 VALIDO (log md5 22ad209c, 1108 s); ruta T VALIDO (03917b3d); c0 en modo `--local` de 600/200 ensayos VALIDO (08a448da, 561 s, no decide nada).
- GitHub Actions x64 (ubuntu-latest, Python 3.12, DEPS fijadas): el humo y el reintento de la prueba.
- La consulta del estado de los trabajos uso la API publica de GitHub; desde brain-env se agoto el limite sin token y se leyo desde otra salida.

## Archivos

En la rama `titan/lector-2026-10-15`:

| Archivo | md5 | Commit |
|---|---|---|
| `tools/lector/SELLO-LECTOR.md` | 6e587be69bbffcdc25b98b4899579edd | `8e65e05` (sin editar) |
| `tools/lector/lector_mosca.py` | 5b7fb79e55ab2b695c9751698c8205c4 | `a00681b` |
| `tools/lector/agregar_lector.py` | 8b003a443596f5c225c2ce419c1c14f7 | `0961e3f` |
| `tools/lector/prueba_lector.py` | d697ed3200cb89c073606639ea499e5d | `0961e3f` |
| `.github/workflows/lector-humo.yml` | 5fed78b0b64c70c2a7568504df39cddb | `a00681b` |
| `.github/workflows/lector-mosca.yml` | 612745d3166f1030705661fb3c3ac427 | `8e80f0b` |
| `.github/workflows/lector-prueba.yml` | 0f7a0fcd63451d0c9260f5a2119447a6 | `7e6a09f` |
| `results/lector_2026-10-15_humo/actions/MD5SUMS.txt` | 4bb869813d5c0118d427482574ea27a9 (26 de 26 OK) | `b1cb491` |
| `results/lector_2026-10-15_humo/actions_prueba/humo_prueba.log` | a3b800b562c778b36e8230b1a2b8cd3e | `c6b1a63` |
| `results/lector_2026-10-15_humo/actions_prueba/MD5SUMS.txt` | 3c81b150a43910e55d676f817ad451e9 (2 de 2 OK) | `c6b1a63` |

Logs del humo (md5 y duracion medida):

| Parte | log md5 | duracion |
|---|---|---|
| c0 | bb7ffb213872af25f9375c0488874590 | 3623,7 s |
| c1 | 330a975dccad6a01fed10cb70cdabde1 | 3134,3 s |
| c2 | 0a9309dd40cb1fb3267a626bb8706e35 | 3091,5 s |
| c3 | f46c867f5e90f7940e35ff5b513ba613 | 3012,1 s |
| c4 | d8088c9feb8b2a0c8017de2638c812e0 | 3395,4 s |
| c5 | 06802666d7a029612aa179984dc8b1d5 | 3491,6 s |
| nulo SL (c2, 600/200) | 0378be9638aaded7ef91ef71422a7434 | 218,4 s |
| nulo T (c5, 600/200) | 86d1de6758071013b88d2c56a003843e | 129,6 s |

En `main`: esta respuesta, `tools/contexto/actualizar_contexto_2026-10-14-037.py` y `.github/workflows/contexto-2026-10-14-037.yml` (se borra solo al aplicar).

## Desvios y errores declarados

1. La permutacion de tipos (T) de `nulos_r2.py` vive en su `main()`; se copio linea por linea en `lector_mosca.py`. NULOS_IGUAL_F3 la controla: los tipos cambiados (T) y los destinos cambiados y el radio (SL) coinciden con el json del factorial 3.
2. Se agrego el modo `--local` (600/200 ensayos, semilla 99): solo prueba codigo y nunca decide.
3. Orden de push equivocado: `21063a6` subio solo HUMO (no disparo nada, el workflow no existia); `a00681b` trajo `lector_mosca.py` y `lector-humo.yml` y disparo el humo sin `prueba_lector.py` ni `agregar_lector.py`, que llegaron en `0961e3f`. El mensaje de `0961e3f` dice que traia `lector-mosca.yml` y no lo traia: llego en `8e80f0b`.
4. En vez de re-disparar el humo entero (otra hora en las 6 celdas que ya habian dado VALIDO) se agrego `lector-prueba.yml`, que repite solo el paso de prueba de `lector-humo.yml` con las mismas DEPS. No toca el sello, HUMO, CORRER ni `lector-mosca.yml`.

## NO MEDIDO

- Los aciertos de L, D1 (WL menos RIDGE), D2 (WL menos W elegida) y los 160 nulos: nada de H_LECTOR esta medido.
- La duracion de la corrida completa. Estimacion: primarias de 50 a 60 min (como el humo, que ya hace todas las trazas); cada trabajo de nulos, unos 10 nulos de unos 10 min, cerca de 2 h, dentro del tope de 340 min. No esta medido.
- La replica de H_LECTOR en brain-env (despues de la de H_RIVAL, que sigue corriendo).

## Antes de firmar

- El humo podia dar rojo y lo dio: la prueba cayo en el primer run. Prueba con un rojo a proposito (CASO_HUMO_INVALIDO, CASO_FALTA_INVALIDO, NULO_DOS_IGUALES sin decidir, NULO_MEDIO_PUNTO refuta).
- REPRO_W y REPRO_RIDGE comparan contra predicciones guardadas de H_TAU y H_RIVAL en otra corrida: un cambio de semilla o de red los pone en False.
- CONTROL_NEGATIVO con etiquetas permutadas podia pasar el tope de 0,55 y quedo en el azar.
- Expectativa declarada en el sello, sin cambios: H_LECTOR_CABLEADO probablemente REFUTADA (antecedente de la entrada por tipos del 12-oct).

--- METODO PROMETEO ---
Rol: implementacion del sello y humo. Delicado: no (sin corrida completa).
Maquina: brain-env y GitHub Actions x64.
Artefactos: rama `titan/lector-2026-10-15` (instrumento, humo `b1cb491`, prueba `c6b1a63`); esta respuesta y el parche del CONTEXTO en `main`; Doc de ClickUp de la 037.
