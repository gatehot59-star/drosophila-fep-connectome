# 2026-10-14-047 · Instrumento de H_MOSCA_ENTERA: prueba 8 de 8, humo completo, y el humo agarró dos fallas del sello

**Fecha:** 2026-10-16, 00:30 (America/Buenos_Aires)
**Rama del instrumento:** `titan/mosca-entera-2026-10-15` (instrumento `194ba1e`, arreglo de la prueba `4d14723`; commits del bot `ef8c6b4`, `1603190` y `d0f5385`)
**Sello:** `tools/mosca_entera/SELLO-MOSCA-ENTERA.md` (`500f66d`, md5 55bc4c76657e35f341300d0e082c7ebe), respuesta 2026-10-14-046
**Doc:** https://app.clickup.com/90171457413/docs/2kza6fw5-23477

## Pedido

«Escribí el instrumento con prueba y humo en Actions» (Abraham, 16-oct 00:01, el texto del botón `instrumento_mosca_entera_047` de la 046).

## Veredicto primero

- **[MEDIDO] El instrumento está escrito, probado y con humo.** Cuatro scripts y dos workflows en la rama. La prueba da **8 de 8 en Actions** (bot `d0f5385`, `EXIT_PRUEBA=0`) y **7 de 7 en brain-env** (sin brian2, la del LIF se saltea).
- **[MEDIDO] La primera prueba cayó, y se declara.** En Actions (bot `ef8c6b4`) y en brain-env, `t_celda` pedía el radio espectral igual al bit contra el `factorial2_mosca.py` sellado. ARPACK arranca de un vector al azar en las dos implementaciones y el radio coincide a ~1e-11 relativo (brain-env: dif_r 8,1e-11, dif_W 2,4e-12). Arreglo: tolerancia de 1e-8 relativa y un tercer testigo, el radio denso de numpy. La trayectoria contra `sim()` del factorial 2 sigue exigida a ≤ 1e-12.
- **[MEDIDO] El humo terminó entero** (run 38844388719, bot `1603190`, 18 de 18 md5 cierran desde un clon nuevo). El LIF de Shiu corre el cerebro entero en el runner: 2 ensayos de 1000 ms en 65 s, con un pico de 3,07 GB. MN9 dispara en 2 de 2 ensayos reales (62 Hz) y en 0 de 2 con los pesos barajados (k0). La líquida tarda unos 2 s por brazo y ocupa 2,25 GB.
- **[MEDIDO] Falla 1 del sello: en la ventana de lectura, LIQ y TASA dan lo mismo.** Con τ 30, pasos 151 a 200: MN9 0,0020266595 contra 0,0020266592 (diferencia 3,2e-10), los mismos 48.407 positivos y máximos a 3,5e-12.
- **[CONCLUSION] Es por construcción.** Con entrada constante, el punto fijo de z ← (1−θ)z + θ·tanh(Wz + u) es z = tanh(Wz + u) para cualquier θ > 0. La compuerta líquida y τ sólo cambian la velocidad con que se llega; la ventana 151 a 200 lee el punto fijo. H_ENTERA_LIQ va a dar diferencia ≈ 0 en las 10 τ y caer en REFUTADA por teorema, no por evidencia. Por lo mismo, las 10 τ no aportan variación: en la ventana sellada, la mosca líquida es una red de tasas en reposo.
- **[CONCLUSION] La prueba miró el sujeto equivocado (E-01).** El control «LIQ y TASA no son la misma función» miró la trayectoria entera de un grafo de 60 neuronas en 40 pasos, donde difieren en más de 1e-3. El sello lee el final, y ahí no difieren.
- **[MEDIDO] Falla 2 del sello: la normalización le cambia la ganancia a los nulos.** Radio espectral crudo: real 2164,29; SHUF_W k0 267,52; SHUF_G k0 339,68. Al llevar cada grafo a 0,9, cada sinapsis de los nulos pesa 8,1 y 6,4 veces lo que pesa en el real.
- **[CONCLUSION] Contra los nulos, MN9 y CONJUNTO mezclan arreglo con ganancia.** El LIF de Shiu no normaliza: usa los pesos crudos, así que sus nulos quedan a ganancia igual. Los dos brazos no comparan lo mismo.
- **[MEDIDO, HUMO] Un nulo de cada tipo, ya visto.** MN9 de SHUF_W k0 (0,00205822) queda arriba del real (0,00202666); SHUF_G k0 queda abajo (−0,00004804). Son dos de los 80 nulos líquidos de CORRER (misma semilla), y τ 30 es una de las 10 τ: quedan vistos y declarados. Las bandas no cambian.
- **[NO MEDIDO] Ningún veredicto de H_MOSCA_ENTERA.** Falta CORRER.

## Herramientas y máquina

- **Sandbox de ClickUp:** escritura de los scripts y las 6 pruebas que no piden la rama de referencia ni brian2.
- **brain-env (MUDH Gateway):** la prueba con `--ref` sobre el clon de `titan/lector-2026-10-15` en `8d305e9` dio 7 de 7; clon nuevo de la rama para los md5. La réplica de H_LECTOR sigue corriendo ahí y no se tocó.
- **Actions** (runner de 4 núcleos y 16 GB): prueba 8 de 8 y humo de cinco partes más el agregado.
- **GitHub MCP:** push y lectura de resultados.

## Archivos

md5 desde un clon nuevo de la rama en `d0f5385`.

| Archivo | md5 | Qué es |
|---|---|---|
| `tools/mosca_entera/liq_entera.py` | 3efe1176915f3d8df4cb710045214f6d | LIQ, TASA y PROX en las 138.639 neuronas; nulos SHUF_W y SHUF_G |
| `tools/mosca_entera/lif_shiu.py` | 9012bd4cb0961f0d74c3b39ca9575dbd | `model.py` de Shiu sin cambios (blob 5ba7083c), 100 Hz, real y SHUF_W |
| `tools/mosca_entera/agregar_mosca_entera.py` | b835f7f8028f78b11c8e0a7526ee5083 | bandas del sello y veredictos |
| `tools/mosca_entera/prueba_mosca_entera.py` | bd53654e9da0de555077a2b59cf2ca3f | 8 pruebas (antes del arreglo: 12f2a3c086b185398ca6183096156b39) |
| `.github/workflows/mosca-entera-prueba.yml` | 019c863afdc51d9eb6449b0223ce38b6 | prueba en Actions, la dispara `PRUEBA` |
| `.github/workflows/mosca-entera-humo.yml` | 15cd3c2be88651d834ca5032e78fdade | humo de cinco partes y agregado, lo dispara `HUMO` |
| `results/mosca_entera_2026-10-15_humo/PRUEBA` | 058fb2960493b89d1b05e9143e8090f1 | disparador del reintento |
| `results/mosca_entera_2026-10-15_humo/HUMO` | 918f0f70264c0a1af63c764f2b621a53 | disparador del humo |
| `results/mosca_entera_2026-10-15_humo/actions_prueba/prueba.log` | b0933d59aa3db32c9dc03bd15c2fc488 | salida cruda de la prueba, 8 de 8 |
| `results/mosca_entera_2026-10-15_humo/actions_prueba/versiones_prueba.txt` | 23a9b0e83d3612559e92a4ec4cd71c71 | versiones y md5 en el runner |
| `results/mosca_entera_2026-10-15_humo/actions_humo/agregado.log` | c2cbabef08909306585f54fbb2277350 | agregado del humo, `VEREDICTO_HUMO` |
| `results/mosca_entera_2026-10-15_humo/actions_humo/liq_real.json` | a223b8fabee97825c4d77a8e1b355025 | LIQ, TASA y PROX con τ 30, todos los decimales |
| `results/mosca_entera_2026-10-15_humo/actions_humo/lif_real.json` | 341405df3e1a1b433cfc57f3c844e9fb | LIF real, 2 ensayos |
| `tools/contexto/actualizar_contexto_2026-10-14-047.py` (en `main`) | b40358641dd4807ef2fc96cee2a423b6 | parche del CONTEXTO |

## Tiempos y memoria del humo

| Parte | Qué corrió | Tiempo | Pico de memoria |
|---|---|---|---|
| lif_real | LIF de Shiu, 2 ensayos de 1000 ms, 2 procesos | 65 s (70 s de reloj) | 3,07 GB |
| lif_shuf | lo mismo con SHUF_W k0 | 59,6 s | 2,80 GB |
| liq_real | LIQ, TASA y PROX con τ 30 | 6,4 s | 2,25 GB |
| liq_W | un nulo SHUF_W | 8,9 s | 2,36 GB |
| liq_G | un nulo SHUF_G | 4,8 s | 2,37 GB |

**[CONCLUSION, extrapolado de 2 ensayos]** CORRER entra holgado en Actions: el LIF real de 30 ensayos, unos 16 min; los 20 SHUF_W de 10 ensayos, unos 100 min en un job o 25 min partidos en 4; la líquida entera (10 τ y 80 nulos), unos 8 min. Unos 30 min de reloj con 6 jobs.

## Lo que el humo deja ver (números sin valor)

S_LIF sale de 2 ensayos (K = 326); con 30 va a cambiar. J contra S_LIF: LIQ 0,3726, TASA 0,3726, PROX 0,2660, SHUF_W k0 0,1941, SHUF_G k0 0,0031. MN9: LIQ 0,00202666, PROX 0,00048603, SHUF_W k0 0,00205822, SHUF_G k0 −0,00004804.

## Qué propongo

Dos caminos; decide Abraham.

1. **Enmienda antes de CORRER (recomendada).** Un sello aparte, escrito antes de ver un solo número de CORRER. (a) LIQ contra TASA leídos donde pueden diferir: la latencia de cada neurona de S_LIF (primera espiga en el LIF; mitad del valor final en LIQ y TASA), en vez del punto fijo. (b) Nulos a ganancia igual: cada nulo con el factor del real (0,9/2164,29) en vez del propio, que es lo que hace el LIF al no normalizar; sus radios quedan en 0,111 y 0,141. Las hipótesis de la 046 se reportan igual, con sus bandas. Los brazos LIF, que son lo caro, no cambian.
2. **CORRER como está sellado.** Más rápido: REPRO_SHIU, MN9, CONJUNTO y RIVAL salen esta noche, con las dos advertencias escritas acá antes de ver los números, y H_ENTERA_LIQ marcada como degenerada por construcción.

Recomiendo la 1 porque, si corremos primero, cualquier enmienda posterior parece mover el arco, y un MN9 perdido contra SHUF_W quedaría sin interpretar.

## NO MEDIDO

- Todos los veredictos de H_MOSCA_ENTERA: REPRO_SHIU, K_SANO, MN9, CONJUNTO, RIVAL y LIQ.
- Los tiempos de CORRER: extrapolados de 2 ensayos y de un nulo por tipo.
- Que el punto fijo sea el mismo con las otras 9 τ: lo dice la cuenta, medido sólo con τ 30.
- Cuánto cambia MN9 contra los nulos con la ganancia igualada: propuesto, no corrido.
- La latencia en el LIF: `lif_shiu.py` guarda conteos por neurona y no tiempos de primera espiga; los tiempos sólo están en el parquet de espigas, que va a artifacts. La enmienda tendría que agregarlos.

## Antes de firmar

- **¿La prueba podía dar rojo?** Sí, y dio rojo: la primera vez cayó en `t_celda`. El arreglo afloja sólo la igualdad del radio de ARPACK (de 1e-12 a 1e-8 relativo) y agrega el radio denso como testigo independiente; la trayectoria sigue exigida a ≤ 1e-12 contra el factorial 2 sellado.
- **¿El humo podía mostrar LIQ distinta de TASA?** En la ventana sellada no: ahí las dos leen el mismo punto fijo. La falla es del sello; el humo la hizo visible.
- **El parche del CONTEXTO** se probó en brain-env sobre una copia (85fc5639 a 26b57643; la segunda pasada aborta sin escribir) con la hora 00:50; la versión subida sólo cambia esa hora.
- **¿Los md5 son del sujeto exacto?** Sí: clon nuevo de la rama en `d0f5385`, no la copia del sandbox.
- **El MD5SUMS de la prueba se lista a sí mismo** (glob `*.txt` en el workflow): esa línea no puede cerrar; las otras dos cierran. Es un defecto del workflow, sin efecto en los resultados; el de CORRER no lo va a repetir.
- **Lo visto antes de CORRER:** τ 30 de LIQ y TASA, PROX, SHUF_W k0 y SHUF_G k0 en la líquida, y SHUF_W k0 del LIF con 2 ensayos. Lo no visto: los 30 ensayos LIF reales, los otros 19 nulos LIF, los otros 78 nulos líquidos y las otras 9 τ.
- **Expectativa del sello contra el humo:** la 046 esperaba que MN9 le ganara a SHUF_W y dudaba con SHUF_G; el único nulo de cada tipo dice lo contrario. Un nulo no decide nada; queda anotado para cotejar.

--- METODO PROMETEO ---
Rol: implementa. Delicado: no.
Máquinas: sandbox de ClickUp (escritura y 6 pruebas), brain-env (prueba 7 de 7 y md5 desde clon nuevo), Actions (prueba 8 de 8 y humo).
Archivo: `docs/agents/respuestas/2026-10-14-047-instrumento-de-la-mosca-entera-prueba-8-de-8-y-el-humo-agarro-dos-fallas-del-sello.md` en `main`.
Doc: https://app.clickup.com/90171457413/docs/2kza6fw5-23477
