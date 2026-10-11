# 2026-10-11-001 · Resumen técnico del conectoma: qué está medido, con qué pruebas y hacia dónde vamos

**Fecha:** 2026-10-11, madrugada (America/Buenos_Aires) · **Máquina:** brain-env, sólo lectura de git · **main:** `d082819` · **Rama:** `titan/tabla7-reconstruida-2026-10-10` en `95e8d6c` (PR #26 abierto, sin merge)

**F-01, veredicto:** resumen, no medición nueva. Está medido y en git: la Tabla 7 reproducible (002) y quién controla las salidas contra tres nulos con corrección múltiple (005 a 009), con 33 tests en verde en 6 herramientas. Lo único que aguanta todo es lo de las descendentes (→ descendentes, → motoras, → cuello y → antena) y el óptico ▼ descendentes. Para cerrar el paper falta una medición: el nulo por circuito con test de tendencia. H4 fuerte sigue NO MEDIDA.

## 1. Pedido

"haz un resumen tecnico de todos los logrso pruebas y acia donde vamos" (Abraham, 2026-10-11).

## 2. Herramientas

- brain-env por el gateway: `git fetch` de `main` y de la rama, conteo de tests y veredictos en los logs de la rama y en las `results/` locales. Las dos salidas quedaron en `/tmp/inv10.txt` y `/tmp/inv10b.txt`, y se citan verbatim en la sección 4.
- GitHub MCP: estado del PR #26.
- ClickUp: Doc público en el Space.
- Sin corridas nuevas: los números salen de las respuestas 001 a 009 y del CONTEXTO de `main`, que no cambió desde la 009.

## 3. Qué se midió (re-lectura)

### Logros por respuesta

| N° | Pedido | Resultado | Estado y pruebas |
|---|---|---|---|
| 001 | Revisar el corpus de marzo (6 chats de Arena y 3 PDF de Gemini) | Herramientas y hallazgos que sostienen la hipótesis y los que no; de ahí salió la salida L3 de marzo que la 002 usó de referencia | Lectura |
| 002 | Reconstruir el script perdido de la Tabla 7 | L3 de marzo 16/16 con las anotaciones de marzo (`c03ad46`) y Tabla 7 publicada 8/8; con el pin de mayo, 10/16 por recambio de root_id; el 8,7% publicado es doble redondeo (2.104 / 24.327 = 8,6488%); con ≥5, 2.700.513 aristas y 13,98% | PASS, 4 tests (log sólo en brain-env) |
| 003 | Hacia dónde vamos, en criollo | Cerrar el paper sobre el cableado; la neurona líquida no paga | Síntesis |
| 004 | Qué hay al final de cada cable | El 97,6% de los cables es el cerebro hablándose a sí mismo; embudo de 1.485 neuronas (1,07%) que recibe el 2,37% de los cables; el 61% de lo que llega a las descendentes viene del central; vuelta 13,19 / 9,83 / 3,58% contra 26,60% global | Descriptivo, sin nulo ni tests |
| 005 | Qué salida controla cada clase | D1: el central pone 60 a 73% de la entrada de las tres salidas; las descendentes, 21 a 22% de la de las motoras; las ascendentes, 16 a 20% de la de las neurosecretoras; el óptico, menos de 0,5%; cruce exacto con la Tabla 7 | PASS, 5 tests |
| 006 | Nulo fuerte de 500 o más permutaciones | R = 10.000, plano y por estratos de fuerza de salida; 41 afirmaciones firmes; control negativo 7/4.840 y 4/4.620 contra 9,7 y 9,2 | PASS en la 2ª corrida, 7 tests |
| 007 | Nulo que conserva la región | k-medias sobre posición (k = 40 y 120) × 30 estratos de tamaño, R = 5.000; 33 firmes; el central sobre descendentes y neurosecretoras era ubicación (×1,07 / ×1,01 y ×1,09 / ×1,03); las ascendentes caen a azar | PASS, 6 tests |
| 008 | Corrección múltiple del nulo regional | BY deja 31 de 33; max-T, 5; Holm no puede con R = 5.000 | PASS, 6 tests |
| 009 | Corrección múltiple del nulo fuerte | BY deja 41 de 41, Holm 34, max-T 11; a la 006 le fallaba la ubicación, no la cantidad de tests | PASS, 5 tests |

### Qué quedó establecido

- **Aguanta todo** (FWER con el nulo de tamaño en la 009 y con el de zona y tamaño en la 008): descendentes → descendentes, → motoras, → cuello y → antena; óptico ▼ descendentes.
- **Aguanta FDR con la zona** (BY, 008): el plus propio del central hacia las motoras de la boca (ingestión, proboscis, haustelo) y DH44; descendentes → proboscis; óptico, sensorial y visual centrífuga por debajo de sus vecinas hacia descendentes y motoras; proyección visual por debajo hacia las motoras.
- **Sólo contra el tamaño** (006 y 009): central → descendentes y → neurosecretoras, ascendentes → las tres salidas y sensorial ascendente → DMS. Con la zona fija (007) fueron ubicación o no llegaron a firmes.
- **Cayó:** motoras → motoras de ingestión y visual centrífuga ▼ ingestión, firmes sin corregir en la 007 y afuera con BY (0,062 y 0,051).
- **Paper:** la Tabla 7 es reproducible, el gradiente hacia el motor sobrevive a ≥5 y el 8,7 es 8,6. Sin nulo por circuito, el gradiente sigue siendo descriptivo.

### Pruebas

- 33 tests en 6 herramientas, todos en verde en brain-env (los logs de la sección 4): Tabla 7, 4; salidas, 5; nulo fuerte, 7; nulo regional, 6; corrección regional, 6; corrección fuerte, 5. La 004 no tiene tests. El `tests_v1.log` de la 006, con 6, es la versión anterior al arreglo del chequeo.
- Chequeos que pueden dar rojo en cada corrida: cruce exacto con la corrida anterior (diferencia 0 o ≤ 1e-12), conservación de tamaños por estrato, media y varianza del nulo contra su valor exacto, control negativo con etiquetas falsas, R ≥ 500 y consistencia de los ajustes. Tests que pueden dar verde: efectos plantados que el instrumento tiene que encontrar.
- Controles negativos: 006, 7/4.840 y 4/4.620 contra 9,7 y 9,2; 007, 11, 1, 5 y 2 contra 9,7 y 9,2; 008, max-T 5/80 contra 4; 009, max-T 10, Holm 8, BH 9 y BY 0 de 160 contra 8.
- Lo que no ven: el tope del control negativo detecta errores gruesos, no inflaciones chicas (con un FWER real del 10%, el de la 009 pasaría el 98% de las veces; cuenta de la 009). En la 008, BH y BY sólo se prueban contra su definición.
- Errores míos cazados y escritos: la 1ª corrida de la 006 dio FAIL por un chequeo mío (z infinito con desvío 0); el Doc de la 008 decía "4 esperados" para BH y BY; en la 009, dos llamadas en paralelo fallaron, un test de FWER era flojo y una cuenta del RESUMEN no podía dar otra cosa que 0.

### H4 y producto (del CONTEXTO, no re-medido hoy)

- H4 fuerte NO MEDIDA. Instrumentos auditados (34 contratos, 36/40); generalización entre trials, balanced accuracy 0,5019 (p = 0,623); estabilidad temporal, 0,5328 (p = 0,055), sugestiva y no positiva.
- SparseLTC empata 48/48 con el control lineal en HC-2; DBC3 aprende más rápido en HC-3b (AULC 0,823 contra 0,635), con el LR de LSTM/GRU NO MEDIDO; ComplexVectorLTC congelada.
- La línea Mojo Absoluto tiene su propio contexto y no entra acá.

### Hacia dónde vamos

1. Nulo por circuito y test de tendencia de la Tabla 7, en brain-env con `src/cp40.py`: es lo único que le falta al claim central del paper para dejar de ser descriptivo.
2. Decisiones de Abraham: el ítem 9 y el 8,6 al erratum; si el control de las salidas entra al paper (propuesta: suplementario, la 006 como "más que neuronas del mismo tamaño" y la 007 como "más que vecinas de la misma zona", BY como criterio y marcado lo que aguanta FWER); y el PR #26, que tiene 7 commits y 27 archivos pero una descripción que habla sólo de la Tabla 7: actualizarla o partirlo antes de mergear.
3. Subir las `results/` de la Tabla 7 y los JSON de la 005 a la 009.
4. Opcionales, si el paper los pide: la 007 con R = 10.000 para Holm (unos 23 minutos de brain-env, porque la 007 tardó 679,5 s con 5.000; cuenta, no corrida), D2 con el nulo regional, nulo por neuropilo de cada sinapsis y min-P.
5. H4 estacionada hasta cerrar el paper.

## 4. Evidencia cruda (verbatim)

`/tmp/inv10.txt` en brain-env (38 líneas, md5 `9f1abfc17fd274b19f4607dcba96368e`), líneas 1 a 33. Las 34 a 38 son las líneas F-01 de la 005 a la 009 cortadas a 260 bytes y no se citan:

```text
main d082819a72d4cadd5ea22c3c1bb3d4d5aa0dd4ce 2026-10-10 18:33:32 -0300 docs(respuestas): 009 correccion multiple del nulo fuerte (006), PASS; CONTEXTO al dia
rama 95e8d6c47cd4eea5cd20432d3fab6146e5d31ed2 2026-10-10 18:16:53 -0300 medicion(salidas): correccion por comparaciones multiples del nulo fuerte (respuesta 009), PASS
95e8d6c medicion(salidas): correccion por comparaciones multiples del nulo fuerte (respuesta 009), PASS
2093d57 medicion(salidas): correccion por comparaciones multiples del nulo regional (respuesta 008), PASS
f436f21 medicion(salidas): nulo que conserva region y tamano (respuesta 007), R=5000 por modo, PASS
c99494f medicion(nulo): nulo fuerte por permutacion de etiquetas para la 005, R=10000; calibrado y PASS en la 2a corrida
7e75cde medicion(salidas): que salida controla cada clase; cruce exacto con Tabla 7, control negativo y 5 tests
1877f56 medicion(cables): que hay al final de cada cable; embudo de salida y ida y vuelta por clase
1f66456 medicion(tabla7): script reconstruido de reciprocidad por clase, tests y diff de anotaciones
origin/t7:results/output_control_2026-10-10/tests.log:5
origin/t7:results/output_control_permcorr_2026-10-10/tests.log:5
origin/t7:results/output_control_permnull_2026-10-10/tests.log:7
origin/t7:results/output_control_regioncorr_2026-10-10/tests.log:6
origin/t7:results/output_control_regionnull_2026-10-10/tests.log:6
origin/t7:results/output_control_2026-10-10/tests.log:TESTS_OK 5
origin/t7:results/output_control_permcorr_2026-10-10/tests.log:TESTS_OK 5
origin/t7:results/output_control_permnull_2026-10-10/tests.log:TESTS_OK 7
origin/t7:results/output_control_regioncorr_2026-10-10/tests.log:TESTS_OK 6
origin/t7:results/output_control_regionnull_2026-10-10/tests.log:TESTS_OK 6
origin/t7:results/output_control_2026-10-10/run.log:VEREDICTO_MEDICION PASS
origin/t7:results/output_control_permcorr_2026-10-10/run.log:VEREDICTO_CORRECCION PASS
origin/t7:results/output_control_permnull_2026-10-10/run.log:VEREDICTO_NULO PASS
origin/t7:results/output_control_regioncorr_2026-10-10/run.log:VEREDICTO_CORRECCION PASS
origin/t7:results/output_control_regionnull_2026-10-10/run.log:VEREDICTO_NULO PASS
docs/agents/respuestas/2026-10-10-001-corpus-marzo-herramientas-y-hallazgos.md
docs/agents/respuestas/2026-10-10-002-tabla7-reconstruida.md
docs/agents/respuestas/2026-10-10-003-hacia-donde-vamos-conectoma-y-celulas-liquidas.md
docs/agents/respuestas/2026-10-10-004-que-hay-al-final-de-cada-cable.md
docs/agents/respuestas/2026-10-10-005-que-salida-controla-cada-clase.md
docs/agents/respuestas/2026-10-10-006-nulo-fuerte-por-permutacion.md
docs/agents/respuestas/2026-10-10-007-nulo-que-conserva-la-region.md
docs/agents/respuestas/2026-10-10-008-correccion-multiple-del-nulo-regional.md
docs/agents/respuestas/2026-10-10-009-correccion-multiple-del-nulo-fuerte.md
```

`/tmp/inv10b.txt` en brain-env (md5 `7908a904479d089ec19ab9d8117a14f7`), sus últimas 20 líneas: los tests de cada herramienta en las `results/` locales, y las herramientas y tests de la rama.

```text
results/output_control_2026-10-10/tests.log:TESTS_OK 5
results/output_control_permcorr_2026-10-10/tests.log:TESTS_OK 5
results/output_control_permnull_2026-10-10/tests.log:TESTS_OK 7
results/output_control_permnull_2026-10-10/tests_v1.log:TESTS_OK 6
results/output_control_regioncorr_2026-10-10/tests.log:TESTS_OK 6
results/output_control_regionnull_2026-10-10/tests.log:TESTS_OK 6
results/table7_reconstruida_2026-10-10/tests.log:TESTS_OK 4
tests/test_output_control_by_class.py
tests/test_output_control_permutation_correction.py
tests/test_output_control_permutation_null.py
tests/test_output_control_region_correction.py
tests/test_output_control_region_null.py
tests/test_table7_reciprocity.py
tools/cable_ends_summary.py
tools/output_control_by_class.py
tools/output_control_permutation_correction.py
tools/output_control_permutation_null.py
tools/output_control_region_correction.py
tools/output_control_region_null.py
tools/table7_reciprocity_by_class.py
```

PR #26 por la API de GitHub: `state` open, `merged` false, `commits` 7, `changed_files` 27, head `95e8d6c47cd4eea5cd20432d3fab6146e5d31ed2`, base `main`.

## 5. Archivos

- Las 9 respuestas del 10-oct listadas en la sección 4, en `main`.
- `docs/agents/CONTEXTO-drosophila-fep.md` en `main`, md5 `44f61392e29323661b211067a28b2057` (el de la 009, sin cambios).
- Herramientas y tests en la rama: los 13 archivos listados en la sección 4.
- Doc público: [Resumen técnico del conectoma al 11-oct: logros, pruebas y hacia dónde vamos](https://app.clickup.com/90171457413/docs/2kza6fw5-20977).

## 6. NO MEDIDO

- Nulo por circuito y test de tendencia (Tabla 7 y embudo de salida).
- La 007 con R = 10.000 (Holm), min-P y qué tests de cola pesada fijan el z crítico de max-T.
- D2 con el nulo regional, otras k y regiones anatómicas, y el neuropilo de cada sinapsis.
- Signo fisiológico, cruce con la reciprocidad por neuropilo de Lin 2024, corrida biológica end-to-end post-merge, mapping anatómico, null anatómico y causalidad.
- SparseLTC → DBC3 sobre señal real, y un review externo del pipeline.
- Este resumen no re-midió nada: si un número de acá no coincide con su respuesta, manda la respuesta.

--- METODO PROMETEO ---
Máquina: brain-env, sólo lectura de git (main d082819, rama 95e8d6c) y estado del PR por GitHub; sin corridas nuevas.
Artefactos: `docs/agents/respuestas/2026-10-11-001-resumen-tecnico-logros-pruebas-y-rumbo.md` + Doc https://app.clickup.com/90171457413/docs/2kza6fw5-20977
