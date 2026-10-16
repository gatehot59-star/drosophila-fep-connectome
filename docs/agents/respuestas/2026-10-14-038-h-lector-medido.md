# 2026-10-14-038 · H_LECTOR medido en Actions: con lector entrenado, la mosca empata al ridge crudo, le gana a sus lineas sin entrenar y le gana a sus 80 barajados

## Pedido

- 15-oct 13:50, ClickKit `correr_lector_038`: disparar el CORRER de H_LECTOR.
- 15-oct 16:49, ClickKit `leer_lector_038`: leer el resultado y escribir la 038.

## Veredicto primero

- [MEDIDO] Actions x64, run 38772392125, CORRER `2df0961`, bot `8d305e9`: 22 trabajos en verde y el agregado. Controles de las 6 celdas, CONTROL_LECTOR_CRUDO, NULOS, PLAN_COMPLETO y REAL_EN_NULOS en True: VALIDO.
- [MEDIDO] **H_LECTOR_CERCA SOSTENIDA.** D1 = WL - RIDGE = -0,0029, IC [-0,0038, -0,0020], umbral -0,01. L (240 rasgos de las 6 descendentes) queda a 0,3 puntos del ridge crudo (22.560 rasgos). No le gana: el techo es negativo.
- [MEDIDO] **H_LECTOR_PAGA SOSTENIDA.** D2 = WL - W_elegida = +0,0474, IC [+0,0454, +0,0493], umbral +0,01. Entrenar el lector suma 4,7 puntos sobre las lineas sin entrenar.
- [MEDIDO] **H_LECTOR_CABLEADO SOSTENIDA.** Con el mismo lector reentrenado en cada nulo, la red real le gana a los 40 nulos de cada familia en las 4 combinaciones, todas con p = 1/41 = 0,0244 (el minimo posible):

| Familia y celda | real | media de nulos | maximo de nulos | delta |
|---|---|---|---|---|
| SL c2 | 0,9910 | 0,9573 | 0,9835 | +0,0337 |
| SL c5 | 0,9930 | 0,8736 | 0,9270 | +0,1194 |
| T c2 | 0,9910 | 0,9460 | 0,9770 | +0,0450 |
| T c5 | 0,9930 | 0,8819 | 0,9135 | +0,1111 |

- [CONCLUSION] Sale contra la expectativa declarada en el sello (CABLEADO probablemente REFUTADA). Con un lector entrenado sobre sus 6 descendentes, el cableado real de la mosca lee mejor que sus barajados SL y T, sobre todo con ruido alto (c5). Las tres son etiquetas de Actions solamente: el sello pide la replica de la primaria en brain-env y, si difiere, pasan a SIN_DECIDIR (NO_SE_REPLICA).
- [NO MEDIDO] La replica en brain-env; los nulos en las otras 4 celdas y en otras semillas de prueba.

## Por celda (media de las pruebas 12 a 21)

| Celda | WL | RIDGE | W_elegida |
|---|---|---|---|
| c0 (0,0 y 0,15) | 0,9914 | 0,9988 | 0,9463 |
| c1 (0,0 y 0,45) | 0,9929 | 0,9924 | 0,9431 |
| c2 (0,3 y 0,15) | 0,9915 | 0,9986 | 0,9466 |
| c3 (0,3 y 0,45) | 0,9918 | 0,9899 | 0,9416 |
| c4 (0,6 y 0,15) | 0,9911 | 0,9987 | 0,9467 |
| c5 (0,6 y 0,45) | 0,9917 | 0,9894 | 0,9413 |

Descriptivo, no decide: con ruido 0,45 (c1, c3, c5) L queda apenas arriba del ridge crudo; con ruido 0,15, apenas abajo.

## Herramientas y maquina

- GitHub Actions x64 (ubuntu-latest, Python 3.12, DEPS fijadas): la corrida. Primarias de 2207 a 3813 s; trabajos de nulos de unos 98 a 111 min (unos 10 min por nulo), y el T c5 k020 arranco 50 min tarde por el tope de 20 trabajos simultaneos.
- brain-env: clon fresco de la rama, lectura del agregado y de los logs, prueba del parche.

## Archivos

| Archivo | md5 |
|---|---|
| `results/lector_2026-10-15/agregado.log` | 8f2f4392ea804c8d637d3d79f4c2f6fd |
| `results/lector_2026-10-15/agregado.json` | 9e974d6688808043b2af168b4347372b |
| `results/lector_2026-10-15/MD5SUMS.txt` | 22f65b263669ddc8ba611e5b3632eb4a (68 de 68 OK) |
| `tools/lector/SELLO-LECTOR.md` | 6e587be69bbffcdc25b98b4899579edd (sin editar) |
| `tools/lector/lector_mosca.py` | 5b7fb79e55ab2b695c9751698c8205c4 |
| `tools/lector/agregar_lector.py` | 8b003a443596f5c225c2ce419c1c14f7 |

En `main`: esta respuesta, `tools/contexto/actualizar_contexto_2026-10-14-038.py` y `.github/workflows/contexto-2026-10-14-038.yml` (se borra solo al aplicar).

## Errores declarados

- El mensaje del commit del bot dice `medicion(2026-10-14-037)`: el workflow se escribio en la 037. La corrida es la de la 038.

## Antes de firmar

- El instrumento podia dar rojo: en el humo, la prueba cayo; en la prueba, un caso con un nulo igual al real da SIN_DECIDIR y uno con medio punto de delta refuta. Aca no hubo un solo nulo de 160 que igualara al real.
- Abierto para la auditoria: la tau de semilla 10 se eligio en H_TAU mirando la red real, y los nulos la heredan sin una eleccion propia. Esa asimetria juega a favor del real y el sello no la declaro como limitacion. Tambien: una sola red por celda, nulos en 2 celdas y solo la prueba 12 (limitaciones 1 y 2 del sello).
- El antecedente del 12-oct (entrada por tipos) dio lo contrario con otra entrada y otro lector. No es el mismo experimento; las dos cosas pueden ser ciertas.

--- METODO PROMETEO ---
Rol: lectura de la medicion. Delicado: no.
Maquina: Actions x64 (medicion) y brain-env (lectura y parche).
Artefactos: `results/lector_2026-10-15/` en `titan/lector-2026-10-15` (bot `8d305e9`); esta respuesta y el parche del CONTEXTO en `main`; Doc de ClickUp de la 038.
