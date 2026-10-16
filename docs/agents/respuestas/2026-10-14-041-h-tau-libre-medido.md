# 2026-10-14-041 · H_TAU_LIBRE SOSTENIDA: con taus que nadie eligio, la mosca le sigue ganando a sus 80 barajados, y la tau 10 ni siquiera la ayudaba

## Pedido

- 15-oct 19:38: "Dispara CORRER de H_TAU_LIBRE".
- 15-oct 21:32, ClickKit `leer_taulibre_041`: leer el resultado y escribir la 041.

## Veredicto primero

- [MEDIDO] Actions x64, run 38818583858, CORRER `291a2f2`, bot `e7ada46`: 20 trabajos y el agregado. 20 de 20 json VALIDO; MISMO_SCRIPT, REPRO_LECTOR (exacto en c2 y c5), PLAN_REALES y PLAN_NULOS en True: VALIDO.
- [MEDIDO] **H_TAU_LIBRE SOSTENIDA.** Cada nulo comparado con la red real de su misma tau fresca; ningun nulo iguala a su real en ninguna combinacion (p = 1/41 = 0,0244, el minimo):

| Familia y celda | real medio | nulo medio | delta | delta en H_LECTOR (tau 10) |
|---|---|---|---|---|
| SL c2 | 0,9943 | 0,9581 | +0,0362 | +0,0337 |
| SL c5 | 0,9952 | 0,8733 | +0,1219 | +0,1194 |
| T c2 | 0,9943 | 0,9466 | +0,0476 | +0,0450 |
| T c5 | 0,9952 | 0,8825 | +0,1127 | +0,1111 |

- [MEDIDO, descriptivo] Con el lector entrenado, la tau 10 no le daba ventaja al real: quedo por debajo de las 10 taus frescas en las dos celdas (c2: 0,9910 contra 0,9930 a 0,9955; c5: 0,9930 contra 0,9940 a 0,9955). La eleccion de H_TAU se hizo con las lineas sin entrenar; con L no se traslada.
- [MEDIDO, descriptivo] Delta por tau: el mas chico es +0,0145 (SL c2, tau 26); en c5 el mas chico es +0,0821 (SL, tau 26). Ninguna tau fresca deja al real por debajo del margen de 1 punto en promedio de sus 4 nulos.
- [CONCLUSION] La asimetria que dejo abierta la 038 no explica la ventaja: con lector entrenado, el cableado real de la mosca lee mejor que sus barajados SL y T, con cualquier tau de las 10 probadas. H_LECTOR_CABLEADO queda reforzada.
- [MEDIDO] REPRO_LECTOR de c2 tambien exacto en brain-env (otra maquina, 1933 s): las 2000 predicciones de H_LECTOR con tau 10 se repiten fuera de Actions.
- [NO MEDIDO] La replica completa de la primaria de H_LECTOR (CERCA y PAGA, 6 celdas, 10 pruebas) en brain-env; nulos en otras celdas o pruebas.

## Herramientas y maquina

- GitHub Actions x64: la corrida. Reales de 3040 a 3847 s; los 20 trabajos entraron juntos (tope de 20).
- brain-env (Python 3.12.14, numpy 2.5.3): lectura desde un clon fresco, REPRO_LECTOR de c2 a tamano completo (log de humo, VALIDO), prueba del parche.

## Archivos

| Archivo | md5 |
|---|---|
| `results/taulibre_2026-10-15/agregado.log` | 64f17f1a4a4b0cf77efc1157e1b10db0 |
| `results/taulibre_2026-10-15/agregado.json` | 7265beca3bb7d13b37e0df9222f4d5e6 |
| `results/taulibre_2026-10-15/MD5SUMS.txt` | 89ebc30bdf307e9c071168fb3584379f (62 de 62 OK) |
| `tools/taulibre/SELLO-TAU-LIBRE.md` | 3886aa58449dfff9a3f9dac88015b5a4 (sin editar) |
| `tools/taulibre/taulibre_mosca.py` | c65bebe270da1e0526a212cff29830fd |
| `tools/taulibre/agregar_taulibre.py` | 340dc41aa6fde80166121c5db6c9b095 |

En `main`: esta respuesta, `tools/contexto/actualizar_contexto_2026-10-14-041.py` y `.github/workflows/contexto-2026-10-14-041.yml` (se borra solo al aplicar).

## Errores declarados

- El commit del bot dice `medicion(2026-10-14-040)`: el workflow se escribio en la 040. La corrida es la de la 041.
- La expectativa del sello (c2 abierta) no se cumplio: c2 tambien supera, con mas margen que con tau 10.

## Antes de firmar

- El instrumento podia dar rojo: la prueba del apareo muestra que un real que cae con una tau refuta aunque el promedio le gane; REPRO_LECTOR y NULOS_IGUAL_LECTOR pudieron romperse y no se rompieron. Ningun nulo de 160 igualo a su real.
- Sigue valiendo lo de H_LECTOR: una sola red por celda, nulos en 2 celdas y solo la prueba 12. Lo que cambia es que la tau no era la explicacion.
- La primaria de H_LECTOR (CERCA y PAGA) sigue con tau 10 y sin replica completa fuera de Actions.

--- METODO PROMETEO ---
Rol: lectura de la medicion. Delicado: no.
Maquina: Actions x64 (medicion) y brain-env (lectura, REPRO_LECTOR y parche).
Artefactos: `results/taulibre_2026-10-15/` en `titan/taulibre-2026-10-15` (bot `e7ada46`); esta respuesta y el parche del CONTEXTO en `main`; Doc de ClickUp de la 041.
