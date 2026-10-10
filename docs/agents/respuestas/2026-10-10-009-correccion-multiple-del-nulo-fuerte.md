# Respuesta 009 · corrección por comparaciones múltiples del nulo fuerte (006): las 41 firmes aguantan FDR, 34 aguantan Holm y 11 max-T; lo que fallaba era la ubicación

**Fecha:** 2026-10-10, tarde (America/Buenos_Aires) · **Máquina:** brain-env · **Rama:** `titan/tabla7-reconstruida-2026-10-10` (PR #26, sin merge), commit `95e8d6c47cd4eea5cd20432d3fab6146e5d31ed2`

**F-01, veredicto:** el instrumento da **PASS** (el nulo regenerado es idéntico al de la 006, la consistencia y el control negativo dan verde y R ≥ 500). La cantidad de tests no tumba a la 006: de sus 41 afirmaciones firmes, Benjamini-Yekutieli (BY, falsos descubrimientos con cualquier dependencia) deja las 41, Holm (cero falsos positivos, por rangos) deja 34 y max-T de Westfall y Young deja 11. Pero corregir controla cuántas veces se probó, no lo que el nulo deja afuera: central → descendentes y ascendentes → descendentes aguantan hasta max-T acá, y la 007, con la zona del cerebro fija, ya mostró que eran ubicación. Lo que aguanta FWER con los dos nulos (009 y 008) es lo de las descendentes (→ descendentes, → motoras, → cuello y → antena) y el óptico ▼ descendentes. BY agrega 2 afirmaciones nuevas al borde y BH 13: no se firman.

## 1. Pedido

"Correct the 006 null for multiple comparisons" (Abraham, 2026-10-10). Estaba en el NO MEDIDO de la 008: la 006 marcaba cada test con p ≤ 0,001 de cada lado sin corregir por la cantidad de tests (242 con ≥1 y 231 con ≥5, para D1 y para D2, con dos nulos).

## 2. Herramientas

- brain-env por el gateway (2 núcleos, 7,8 GB): tests, corrida completa (778,3 s), md5 de todo y verificación de los push.
- Sandbox de Brain: script, tests, reconstrucción del log (md5 igual al de brain-env antes de subir), el cruce con la 007 y la 008 contado sobre sus logs, y cuatro cuentas (cuantil normal del máximo, pisos de Holm, BH y BY, binomiales del control negativo y max-T a 0,025), que se citan como cuentas y no como corridas.
- GitHub MCP: push a la rama y a `main` (brain-env no tiene credencial de push para este repo).
- ClickUp: Doc público en el Space.

## 3. Qué se midió

- **Mismo nulo, regenerado:** `correr_nulo` de la 006 con semillas [20261011, umbral, modo], R = 10.000 y 100 estratos de fuerza pedidos (quedan 86 con ≥1 y 80 con ≥5), con los parámetros leídos del JSON de la 006. Estratos, D1, D2, p, flags, conservación y las 11 líneas de firmes de la 006 tienen que salir idénticos (CRUCE_006): la diferencia máxima fue 0.
- **Familias:** ocho, una por umbral (≥1, ≥5), nulo (perm, estr) y estadístico (D1, D2), de 228 a 242 tests: los que tienen desvío exacto mayor a 1e-12 y un nulo que varía. Las afirmaciones firmes de la 006 son de D1 con el nulo estr, así que perm y D2 no les cobran tests; esas familias se corrigen igual y se reportan.
- **Métodos:** los de la 008 con sus mismas funciones (max-T step-down de Westfall y Young sobre |z| = |D1 - E| / sd con E y sd exactas; BH y BY sobre el p bilateral de permutación, mín(1, 2 × mín(p_sobre, p_bajo))) y además Holm sobre ese mismo p. Con R = 10.000 el p bilateral más chico es 0,0002 y Bonferroni pide 0,05 / 242 = 0,000207: Holm ya puede rechazar (línea RESOLUCION). En la 008, con 5.000, no podía.
- **Firme corregido:** la regla de la 006 (nulo estr, D1; SOBRE en ≥1 y en ≥5 en cualquier conjunto válido en los dos; BAJO en los dos sólo en los de nivel 1) con p ajustado ≤ 0,05 en las dos familias. Se firma con BY, como en la 008. El subconjunto FWER es el que aguantan max-T y Holm a la vez. Las dos cosas se fijaron en el script antes de correr.
- **Chequeos que pueden dar rojo:** CRUCE_006; CONSISTENCIA (step-down ≤ single-step, ajustados monótonos, BY ≥ BH, Holm ≥ BH y Holm monótono); CONTROL_NEGATIVO (20 etiquetados falsos por umbral y nulo, sacados del mismo nulo con semilla [seed, umbral, modo, 98] y corregidos en las dos familias de estadístico: 160 por método, con tope máx(3, 3 × 0,05 × 160) = 24); R_PEDIDO_500 (R ≥ 500 y la 006 en PASS). El test extremo a extremo mueve un p del JSON de la 006 en 1e-6, o toca una línea de firmes, y el cruce da FAIL; con R = 300 da INCOMPLETO.
- **Chequeo que puede dar verde:** un efecto plantado sale SOBRE con los cuatro métodos, con perm y con estr.
- Una sola corrida completa.

### Lectura

- **Aguantan todo (max-T y Holm en ≥1 y ≥5), 11:** descendentes → descendentes (max-T máximo 0,0015), → motoras (0,0061), → cuello (0,0055), → proboscis (0,011) y → antena (0,0061); óptico ▼ descendentes (0,0051) y ▼ motoras (0,021); ascendentes → descendentes (0,011); central → descendentes (0,0175); motoras → motoras de ingestión (0,033); sensorial ascendente → DMS (0,039).
- **Aguantan Holm y no max-T, 23:** el resto del central (→ motoras, → neurosecretoras y 10 conjuntos finos: ingestión, proboscis, antena, buche, ojo, haustelo, IPC, mNSC, DH31 y DH44; max-T 0,076 a 0,57); ascendentes → motoras, → neurosecretoras, → antena y → Hugin-RG (0,080 a 0,34); sensorial ascendente → descendentes (0,079); óptico ▼ neurosecretoras (0,12); visual centrífuga ▼ descendentes y motoras (0,88 y 0,98); proyección visual ▼ las tres salidas (0,44 a 0,95).
- **Caen con Holm y aguantan BY, 7, todas en conjuntos finos:** descendentes → motoras de ingestión, de ojo y de haustelo (Holm 0,10 a 0,33; BY 0,013 a 0,042); ascendentes → motoras sin subclase y lNSC (Holm 0,068 y 0,060; BY 0,0091 y 0,0064); sensorial → motoras de ingestión y CRZ (Holm 0,068 y 0,12; BY 0,0091 y 0,012).
- **Lo que importa:** corregir controla cuántas veces se probó, no lo que el nulo deja afuera. El nulo de la 006 iguala la fuerza de salida, no la zona. Central → descendentes (z = +30,3 / +21,5) y ascendentes → descendentes (z = +34,0 / +28,0) aguantan max-T, y en la 007, con la zona fija, el central quedó en ×1,07 con k = 40 y ×1,01 con k = 120, y las ascendentes en ×0,90 / ×0,98 con ≥1 y ×0,92 / ×0,99 con ≥5.
- **Cruce con la 007 y la 008 (contado sobre sus logs):** 16 de las 41 firmes de la 006 eran firmes también en la 007. BY en la 008 deja 15 de esas 16 (cae motoras → ingestión). FWER con los dos nulos (max-T y Holm acá, max-T en la 008) deja 5: descendentes → descendentes, → motoras, → cuello y → antena, y óptico ▼ descendentes. Descendentes → proboscis y óptico ▼ motoras aguantan FWER acá y no en la 008 (max-T 0,054 y 0,094).
- **Las nuevas:** BY agrega 2 al borde, ascendentes → cuello (0,046) y central → motoras salivales (0,049), y BH agrega 13 (0,0076 a 0,048). No las firmo: no estaban en la 006, y con la zona fija (007) ascendentes → cuello pasa a BAJO con k = 40 (×0,58 / ×0,54) y central → salivales, con 2 neuronas de destino, a azar (×1,34 / ×1,23 con ≥1). Esa decisión no estaba escrita en el script antes de correr: es posterior y la declaro.
- **Por qué max-T es tan duro:** su z crítico da de 11,4 a 15,3 en las ocho familias. Con 228 a 242 |z| normales independientes, el 95% del máximo estaría en 3,69 a 3,70 (cuenta en sandbox). Hay tests con colas mucho más pesadas que una normal y max-T paga por ellos: central → motoras, con z = +15,7 / +12,6, da 0,048 / 0,076 y no llega. Cuáles son esos tests no está medido.
- **El corte de la 006 ya era casi BY:** sobre + bajo en las familias estr D1, 104 y 65 sin corregir contra 110 y 67 con BY. Igual que en la 008.
- **Para el paper:** la 006 dice "más que neuronas del mismo tamaño" y la 007 "más que vecinas de la misma zona y el mismo tamaño", las dos con BY como criterio y marcado lo que aguanta FWER. Lo que aguanta FWER con los dos nulos es lo de las descendentes y el óptico ▼ descendentes. Decide Abraham.

### Calibración

- **Control negativo:** tuvieron algún rechazo 10 de 160 etiquetados falsos con max-T, 8 con Holm, 9 con BH y 0 con BY, contra 8 esperados con un FWER del 5% (tope 24). Con 10.000 permutaciones es una prueba real para max-T, Holm y BH, porque alcanza un test en el piso para rechazar. BY necesita al menos 6 tests en el piso (cuenta en sandbox), así que 0 de 160 es lo esperable y sólo detecta un error grueso, como no ajustar.
- **Lo que el control negativo no ve:** el tope de 24 detecta errores gruesos, no inflaciones chicas. Con un FWER real del 10% pasaría el 98% de las veces, y con uno del 20%, el 7% (binomial, cuenta en sandbox). Además, los rechazos de Holm y BH se juntan en ≥1 estr (4 y 3 de 20, en D1 y D2): que una de ocho familias dé 4 de 20 pasa más o menos el 12% de las veces con un FWER del 5% (cuenta, suponiendo familias independientes, que no lo son del todo). No lo leo como descalibración, pero tampoco está descartada.
- **Resolución:** los pisos a R = 10.000 son max-T 0,0001, Holm 0,046 a 0,048, BH 0,0005 a 0,0008 y BY 0,0033 a 0,0048. Las 34 que aguantan Holm son exactamente las que tienen el p mínimo posible en los dos umbrales (contado en el log). Con 88 tests en el piso con ≥1 y 57 con ≥5 (cuenta: reproduce los pisos de BH y BY del log), el p bilateral siguiente, 0,0004, ya da Holm 0,060 y 0,068, que son los valores del log. O sea: con 10.000 permutaciones, Holm sólo separa "ninguna permutación llegó al observado" de "alguna llegó", y entre las 34 no puede ordenar cuál está más lejos del azar.
- **Cota para las dos familias juntas** (0,025 cada una, criterio conservador: una afirmación es falsa si cualquiera de sus dos nulos es cierto): con max-T solo quedan 9 (contado en el log); se caen motoras → ingestión (0,033) y sensorial ascendente → DMS (0,039).

### Errores propios

- **Llamadas en paralelo al gateway:** puse tres en el mismo bloque y dos fallaron por timeout de la cola del gateway. La corrida de fondo no se afectó y seguí consultando de a una. No tocó archivos, pero la regla de no hacerlo ya estaba y la incumplí.
- **Test de FWER de Holm flojo:** la primera versión usaba 2.000 repeticiones y tope 0,065. En el caso correlacionado dio 0,058 y pasaba; con 40.000 repeticiones dio 0,046, así que era ruido, pero con ese tope el test casi no podía dar rojo ante una inflación chica. Lo reescribí antes de commitear: 20.000 repeticiones y tope 0,056 (dio 0,0488 y 0,0473).
- **Métrica degenerada en el RESUMEN:** "con alfa/2=0.025 quedan=0" exige Holm ≤ 0,025, y el piso de Holm a R = 10.000 es 0,046 a 0,048. Ese 0 no podía dar otra cosa: es un límite del instrumento, no un resultado. La cuenta útil es la de max-T solo (9). El script no se tocó después de correr; queda declarado acá y en el Doc.
- **Módulo faltante en el sandbox:** los tests fallaron primero por `ModuleNotFoundError` de `test_output_control_by_class`, que usan los datos chicos de la 006; copié ese archivo al sandbox. En brain-env ya estaba.

## 4. Evidencia cruda (verbatim)

`results/output_control_permcorr_2026-10-10/tests.log`:

```text
TEST test_holm_contra_la_definicion -> Holm = definicion max_{j<=i} (m - j + 1) p_(j) en 50 casos con empates; BH <= Holm <= Bonferroni
TEST test_holm_controla_fwer_y_resolucion -> FWER de Holm 0.0488 independientes y 0.0473 correlacionados en 20.000 repeticiones (tope 0,056); con R = 10.000 rechaza en el piso con 250 tests y no con 251
TEST test_corregir_agrega_holm_y_detecta_lo_plantado -> con perm y con estr el efecto plantado sale SOBRE con max-T, Holm, BH y BY; la clase sin mezcla sale de la familia solo en estr (m = 4 contra 6)
TEST test_regla_de_firmes_de_la_006 -> SOBRE en los dos umbrales en cualquier conjunto, BAJO en los dos solo en nivel 1, nada sin entrada en los dos
TEST test_extremo_a_extremo_006_a_009 -> extremo a extremo: 005 -> 006 -> 009, el nulo regenerado da los mismos p y las mismas firmes, R=300 da INCOMPLETO, y un p movido 1e-6 o una linea de firmes tocada en el JSON de la 006 dan FAIL
TESTS_OK 5
```

`results/output_control_permcorr_2026-10-10/run.log`, líneas 1 a 26 (encabezado, resolución, cruce de cada nulo con la 006, las ocho familias y los falsos):

```text
== output_control_permutation_correction.py :: correccion por comparaciones multiples del nulo fuerte (006) ==
ENTORNO python=3.12.14 numpy=2.5.3 scipy=1.18.1 pandas=3.0.5 maquina=brain-env
PARAMETROS_006 seed=20261011 r=10000 n_estratos=100 veredicto_006=PASS | alfa=0.05 n_falsos=20 factor_control=3
INPUT parquet /workspace/connectivity.parquet md5=3d802fd542b5d18570ba1ba0bb0abed9 pin_ok=True
INPUT annotations /workspace/annotations.tsv md5=719904abad876c68ace1b5690c9b9b63 pin_ok=True
INPUT json_006 results/output_control_permnull_2026-10-10/output_control_permutation_null.json md5=ec64172711d7d18040f6f09335d7521b pin_ok=True
GRAFO n_nodos=138639 n_aristas=15091983 mapeo_biyectivo=True
RESOLUCION r=10000 p_min_bilateral=0.000200 tests_por_familia=242 bonferroni=0.000207 holm_puede_rechazar=True
ESTRATOS [>=1] n=86 iguales_006=True
NULO [>=1] perm R=10000 segundos=181.5 d_igual_006=True p_iguales_006=True flags_iguales_006=True
FAMILIA [>=1] perm D1 m=241 z_crit=14.96 | 006 SOBRE=44 BAJO=49 | maxT SOBRE=13 BAJO=5 | Holm SOBRE=35 BAJO=46 | BH SOBRE=56 BAJO=54 | BY SOBRE=46 BAJO=49
FAMILIA [>=1] perm D2 m=242 z_crit=12.16 | 006 SOBRE=65 BAJO=66 | maxT SOBRE=51 BAJO=19 | Holm SOBRE=64 BAJO=61 | BH SOBRE=80 BAJO=73 | BY SOBRE=65 BAJO=66
FALSOS [>=1] perm n=20 con_rechazo D1 maxT=1 Holm=1 BH=2 BY=0 | D2 maxT=0 Holm=0 BH=0 BY=0
NULO [>=1] estr R=10000 segundos=181.2 d_igual_006=True p_iguales_006=True flags_iguales_006=True
FAMILIA [>=1] estr D1 m=239 z_crit=15.25 | 006 SOBRE=55 BAJO=49 | maxT SOBRE=18 BAJO=3 | Holm SOBRE=42 BAJO=46 | BH SOBRE=72 BAJO=52 | BY SOBRE=61 BAJO=49
FAMILIA [>=1] estr D2 m=242 z_crit=11.38 | 006 SOBRE=85 BAJO=62 | maxT SOBRE=66 BAJO=18 | Holm SOBRE=76 BAJO=62 | BH SOBRE=101 BAJO=63 | BY SOBRE=89 BAJO=62
FALSOS [>=1] estr n=20 con_rechazo D1 maxT=1 Holm=4 BH=4 BY=0 | D2 maxT=1 Holm=3 BH=3 BY=0
ESTRATOS [>=5] n=80 iguales_006=True
NULO [>=5] perm R=10000 segundos=187.4 d_igual_006=True p_iguales_006=True flags_iguales_006=True
FAMILIA [>=5] perm D1 m=231 z_crit=14.43 | 006 SOBRE=33 BAJO=36 | maxT SOBRE=10 BAJO=3 | Holm SOBRE=27 BAJO=30 | BH SOBRE=39 BAJO=43 | BY SOBRE=33 BAJO=36
FAMILIA [>=5] perm D2 m=231 z_crit=13.26 | 006 SOBRE=50 BAJO=56 | maxT SOBRE=26 BAJO=10 | Holm SOBRE=43 BAJO=53 | BH SOBRE=58 BAJO=65 | BY SOBRE=51 BAJO=58
FALSOS [>=5] perm n=20 con_rechazo D1 maxT=1 Holm=0 BH=0 BY=0 | D2 maxT=1 Holm=0 BH=0 BY=0
NULO [>=5] estr R=10000 segundos=182.8 d_igual_006=True p_iguales_006=True flags_iguales_006=True
FAMILIA [>=5] estr D1 m=228 z_crit=14.62 | 006 SOBRE=33 BAJO=32 | maxT SOBRE=9 BAJO=2 | Holm SOBRE=27 BAJO=30 | BH SOBRE=46 BAJO=37 | BY SOBRE=35 BAJO=32
FAMILIA [>=5] estr D2 m=231 z_crit=14.37 | 006 SOBRE=58 BAJO=56 | maxT SOBRE=19 BAJO=8 | Holm SOBRE=52 BAJO=50 | BH SOBRE=68 BAJO=62 | BY SOBRE=60 BAJO=57
FALSOS [>=5] estr n=20 con_rechazo D1 maxT=3 Holm=0 BH=0 BY=0 | D2 maxT=2 Holm=0 BH=0 BY=0
```

Líneas 27 a 60 (nivel 1 corregido con el nulo estr y D1; cada campo en el orden ≥1, ≥5):

```text
-- NIVEL1 corregido (nulo estr, D1; orden: >=1, >=5) --
NIVEL1 descending ascending           z=+34.0/+28.0 maxT=0.0045/0.0109 Holm=0.0478/0.0456 BH=0.0005/0.0008 BY=0.0033/0.0048
NIVEL1 descending central             z=+30.3/+21.5 maxT=0.0075/0.0175 Holm=0.0478/0.0456 BH=0.0005/0.0008 BY=0.0033/0.0048
NIVEL1 descending descending          z=+86.4/+60.2 maxT=0.0001/0.0015 Holm=0.0478/0.0456 BH=0.0005/0.0008 BY=0.0033/0.0048
NIVEL1 descending endocrine           z=+0.1/+0.0 maxT=1.0000/1.0000 Holm=1.0000/1.0000 BH=0.7138/0.6739 BY=1.0000/1.0000
NIVEL1 descending motor               z=+0.7/-0.7 maxT=1.0000/1.0000 Holm=1.0000/1.0000 BH=0.4699/0.5060 BY=1.0000/1.0000
NIVEL1 descending optic               z=-60.5/-43.2 maxT=0.0007/0.0051 Holm=0.0478/0.0456 BH=0.0005/0.0008 BY=0.0033/0.0048
NIVEL1 descending sensory             z=-0.9/+0.5 maxT=0.9997/1.0000 Holm=1.0000/1.0000 BH=0.5257/0.9759 BY=1.0000/1.0000
NIVEL1 descending sensory_ascending   z=+31.7/+11.9 maxT=0.0069/0.0790 Holm=0.0478/0.0456 BH=0.0005/0.0008 BY=0.0033/0.0048
NIVEL1 descending visual_centrifugal  z=-3.5/-2.8 maxT=0.7731/0.8840 Holm=0.0478/0.0456 BH=0.0005/0.0008 BY=0.0033/0.0048
NIVEL1 descending visual_projection   z=-5.3/-4.6 maxT=0.3746/0.4787 Holm=0.0478/0.0456 BH=0.0005/0.0008 BY=0.0033/0.0048
NIVEL1 descending sin_anotacion       z=-0.5/-0.2 maxT=1.0000/1.0000 Holm=1.0000/1.0000 BH=0.3301/1.0000 BY=1.0000/1.0000
NIVEL1 motor      ascending           z=+8.2/+5.7 maxT=0.1445/0.3440 Holm=0.0478/0.0456 BH=0.0005/0.0008 BY=0.0033/0.0048
NIVEL1 motor      central             z=+15.7/+12.6 maxT=0.0477/0.0757 Holm=0.0478/0.0456 BH=0.0005/0.0008 BY=0.0033/0.0048
NIVEL1 motor      descending          z=+47.2/+41.8 maxT=0.0017/0.0061 Holm=0.0478/0.0456 BH=0.0005/0.0008 BY=0.0033/0.0048
NIVEL1 motor      endocrine           z=+6.7/-0.4 maxT=0.2371/1.0000 Holm=0.1692/1.0000 BH=0.0029/1.0000 BY=0.0175/1.0000
NIVEL1 motor      motor               z=+13.5/+7.0 maxT=0.0563/0.2369 Holm=0.0478/1.0000 BH=0.0005/0.0284 BY=0.0033/0.1708
NIVEL1 motor      optic               z=-24.5/-20.2 maxT=0.0145/0.0209 Holm=0.0478/0.0456 BH=0.0005/0.0008 BY=0.0033/0.0048
NIVEL1 motor      sensory             z=-3.4/-1.5 maxT=0.7747/0.9981 Holm=0.0478/1.0000 BH=0.0005/0.1999 BY=0.0033/1.0000
NIVEL1 motor      sensory_ascending   z=+9.1/+4.5 maxT=0.1128/0.4985 Holm=0.0478/1.0000 BH=0.0005/0.0483 BY=0.0033/0.2905
NIVEL1 motor      visual_centrifugal  z=-2.0/-2.1 maxT=0.9693/0.9802 Holm=0.0478/0.0456 BH=0.0005/0.0008 BY=0.0033/0.0048
NIVEL1 motor      visual_projection   z=-5.5/-4.9 maxT=0.3592/0.4389 Holm=0.0478/0.0456 BH=0.0005/0.0008 BY=0.0033/0.0048
NIVEL1 motor      sin_anotacion       z=-0.2/-0.2 maxT=1.0000/1.0000 Holm=1.0000/1.0000 BH=1.0000/1.0000 BY=1.0000/1.0000
NIVEL1 endocrine  ascending           z=+15.1/+11.4 maxT=0.0493/0.0828 Holm=0.0478/0.0456 BH=0.0005/0.0008 BY=0.0033/0.0048
NIVEL1 endocrine  central             z=+12.1/+6.8 maxT=0.0681/0.2442 Holm=0.0478/0.0456 BH=0.0005/0.0008 BY=0.0033/0.0048
NIVEL1 endocrine  descending          z=+4.7/+3.3 maxT=0.4876/0.7813 Holm=0.6143/1.0000 BH=0.0102/0.0922 BY=0.0620/0.5537
NIVEL1 endocrine  endocrine           z=+31.8/-0.0 maxT=0.0069/1.0000 Holm=0.0478/1.0000 BH=0.0005/1.0000 BY=0.0033/1.0000
NIVEL1 endocrine  motor               z=-0.0/-0.1 maxT=1.0000/1.0000 Holm=1.0000/1.0000 BH=0.4897/1.0000 BY=1.0000/1.0000
NIVEL1 endocrine  optic               z=-14.6/-9.6 maxT=0.0504/0.1249 Holm=0.0478/0.0456 BH=0.0005/0.0008 BY=0.0033/0.0048
NIVEL1 endocrine  sensory             z=+0.3/+1.1 maxT=1.0000/0.9997 Holm=1.0000/1.0000 BH=0.9122/0.5130 BY=1.0000/1.0000
NIVEL1 endocrine  sensory_ascending   z=+4.3/+2.5 maxT=0.5980/0.9263 Holm=1.0000/1.0000 BH=0.0650/0.1390 BY=0.3935/0.8355
NIVEL1 endocrine  visual_centrifugal  z=-1.1/-0.8 maxT=0.9993/1.0000 Holm=0.0604/1.0000 BH=0.0011/0.3600 BY=0.0064/1.0000
NIVEL1 endocrine  visual_projection   z=-3.4/-2.4 maxT=0.7751/0.9480 Holm=0.0478/0.0456 BH=0.0005/0.0008 BY=0.0033/0.0048
NIVEL1 endocrine  sin_anotacion       z=-0.1/-0.1 maxT=1.0000/1.0000 Holm=1.0000/1.0000 BH=1.0000/1.0000 BY=1.0000/1.0000
```

Líneas 61 a 117 (las 41 firmes de la 006 con corrección, y las nuevas de BH y de BY):

```text
-- FIRMES DE LA 006 CON CORRECCION (nulo estr, D1, regla de la 006; p ajustado maximo entre >=1 y >=5; queda = <= 0.05 en los dos) --
FIRME_006 ascending           -> descending                               SOBRE | p_max maxT=0.01090 Holm=0.04780 BH=0.00080 BY=0.00481 | queda maxT=SI Holm=SI BH=SI BY=SI
FIRME_006 ascending           -> motor                                    SOBRE | p_max maxT=0.34397 Holm=0.04780 BH=0.00080 BY=0.00481 | queda maxT=NO Holm=SI BH=SI BY=SI
FIRME_006 ascending           -> endocrine                                SOBRE | p_max maxT=0.08279 Holm=0.04780 BH=0.00080 BY=0.00481 | queda maxT=NO Holm=SI BH=SI BY=SI
FIRME_006 ascending           -> motor:antennal_motor_neuron              SOBRE | p_max maxT=0.09119 Holm=0.04780 BH=0.00080 BY=0.00481 | queda maxT=NO Holm=SI BH=SI BY=SI
FIRME_006 ascending           -> motor:sin_subclase                       SOBRE | p_max maxT=0.10409 Holm=0.06839 BH=0.00152 BY=0.00913 | queda maxT=NO Holm=NO BH=SI BY=SI
FIRME_006 ascending           -> endocrine:lNSC_unknown                   SOBRE | p_max maxT=0.08929 Holm=0.06039 BH=0.00105 BY=0.00636 | queda maxT=NO Holm=NO BH=SI BY=SI
FIRME_006 ascending           -> endocrine:Hugin-RG                       SOBRE | p_max maxT=0.07969 Holm=0.04780 BH=0.00080 BY=0.00481 | queda maxT=NO Holm=SI BH=SI BY=SI
FIRME_006 central             -> descending                               SOBRE | p_max maxT=0.01750 Holm=0.04780 BH=0.00080 BY=0.00481 | queda maxT=SI Holm=SI BH=SI BY=SI
FIRME_006 central             -> motor                                    SOBRE | p_max maxT=0.07569 Holm=0.04780 BH=0.00080 BY=0.00481 | queda maxT=NO Holm=SI BH=SI BY=SI
FIRME_006 central             -> endocrine                                SOBRE | p_max maxT=0.24418 Holm=0.04780 BH=0.00080 BY=0.00481 | queda maxT=NO Holm=SI BH=SI BY=SI
FIRME_006 central             -> motor:ingestion_motor_neuron             SOBRE | p_max maxT=0.11169 Holm=0.04780 BH=0.00080 BY=0.00481 | queda maxT=NO Holm=SI BH=SI BY=SI
FIRME_006 central             -> motor:proboscis_motor_neuron             SOBRE | p_max maxT=0.22978 Holm=0.04780 BH=0.00080 BY=0.00481 | queda maxT=NO Holm=SI BH=SI BY=SI
FIRME_006 central             -> motor:antennal_motor_neuron              SOBRE | p_max maxT=0.37406 Holm=0.04780 BH=0.00080 BY=0.00481 | queda maxT=NO Holm=SI BH=SI BY=SI
FIRME_006 central             -> motor:crop_motor_neuron                  SOBRE | p_max maxT=0.35516 Holm=0.04780 BH=0.00080 BY=0.00481 | queda maxT=NO Holm=SI BH=SI BY=SI
FIRME_006 central             -> motor:eye_motor_neuron                   SOBRE | p_max maxT=0.36446 Holm=0.04780 BH=0.00080 BY=0.00481 | queda maxT=NO Holm=SI BH=SI BY=SI
FIRME_006 central             -> motor:haustellum_motor_neuron            SOBRE | p_max maxT=0.27887 Holm=0.04780 BH=0.00080 BY=0.00481 | queda maxT=NO Holm=SI BH=SI BY=SI
FIRME_006 central             -> endocrine:IPC                            SOBRE | p_max maxT=0.57064 Holm=0.04780 BH=0.00080 BY=0.00481 | queda maxT=NO Holm=SI BH=SI BY=SI
FIRME_006 central             -> endocrine:mNSC_unknown                   SOBRE | p_max maxT=0.39726 Holm=0.04780 BH=0.00080 BY=0.00481 | queda maxT=NO Holm=SI BH=SI BY=SI
FIRME_006 central             -> endocrine:DH31                           SOBRE | p_max maxT=0.39716 Holm=0.04780 BH=0.00080 BY=0.00481 | queda maxT=NO Holm=SI BH=SI BY=SI
FIRME_006 central             -> endocrine:DH44                           SOBRE | p_max maxT=0.14409 Holm=0.04780 BH=0.00080 BY=0.00481 | queda maxT=NO Holm=SI BH=SI BY=SI
FIRME_006 descending          -> descending                               SOBRE | p_max maxT=0.00150 Holm=0.04780 BH=0.00080 BY=0.00481 | queda maxT=SI Holm=SI BH=SI BY=SI
FIRME_006 descending          -> motor                                    SOBRE | p_max maxT=0.00610 Holm=0.04780 BH=0.00080 BY=0.00481 | queda maxT=SI Holm=SI BH=SI BY=SI
FIRME_006 descending          -> motor:ingestion_motor_neuron             SOBRE | p_max maxT=0.29277 Holm=0.10079 BH=0.00224 BY=0.01347 | queda maxT=NO Holm=NO BH=SI BY=SI
FIRME_006 descending          -> motor:neck_motor_neuron                  SOBRE | p_max maxT=0.00550 Holm=0.04780 BH=0.00080 BY=0.00481 | queda maxT=SI Holm=SI BH=SI BY=SI
FIRME_006 descending          -> motor:proboscis_motor_neuron             SOBRE | p_max maxT=0.01090 Holm=0.04780 BH=0.00080 BY=0.00481 | queda maxT=SI Holm=SI BH=SI BY=SI
FIRME_006 descending          -> motor:antennal_motor_neuron              SOBRE | p_max maxT=0.00610 Holm=0.04780 BH=0.00080 BY=0.00481 | queda maxT=SI Holm=SI BH=SI BY=SI
FIRME_006 descending          -> motor:eye_motor_neuron                   SOBRE | p_max maxT=0.18278 Holm=0.32797 BH=0.00701 BY=0.04215 | queda maxT=NO Holm=NO BH=SI BY=SI
FIRME_006 descending          -> motor:haustellum_motor_neuron            SOBRE | p_max maxT=0.28057 Holm=0.13359 BH=0.00294 BY=0.01768 | queda maxT=NO Holm=NO BH=SI BY=SI
FIRME_006 motor               -> motor:ingestion_motor_neuron             SOBRE | p_max maxT=0.03280 Holm=0.04780 BH=0.00080 BY=0.00481 | queda maxT=SI Holm=SI BH=SI BY=SI
FIRME_006 optic               -> descending                               BAJO  | p_max maxT=0.00510 Holm=0.04780 BH=0.00080 BY=0.00481 | queda maxT=SI Holm=SI BH=SI BY=SI
FIRME_006 optic               -> motor                                    BAJO  | p_max maxT=0.02090 Holm=0.04780 BH=0.00080 BY=0.00481 | queda maxT=SI Holm=SI BH=SI BY=SI
FIRME_006 optic               -> endocrine                                BAJO  | p_max maxT=0.12489 Holm=0.04780 BH=0.00080 BY=0.00481 | queda maxT=NO Holm=SI BH=SI BY=SI
FIRME_006 sensory             -> motor:ingestion_motor_neuron             SOBRE | p_max maxT=0.36396 Holm=0.06839 BH=0.00152 BY=0.00913 | queda maxT=NO Holm=NO BH=SI BY=SI
FIRME_006 sensory             -> endocrine:CRZ                            SOBRE | p_max maxT=0.14439 Holm=0.11679 BH=0.00201 BY=0.01219 | queda maxT=NO Holm=NO BH=SI BY=SI
FIRME_006 sensory_ascending   -> descending                               SOBRE | p_max maxT=0.07899 Holm=0.04780 BH=0.00080 BY=0.00481 | queda maxT=NO Holm=SI BH=SI BY=SI
FIRME_006 sensory_ascending   -> endocrine:DMS                            SOBRE | p_max maxT=0.03890 Holm=0.04780 BH=0.00080 BY=0.00481 | queda maxT=SI Holm=SI BH=SI BY=SI
FIRME_006 visual_centrifugal  -> descending                               BAJO  | p_max maxT=0.88401 Holm=0.04780 BH=0.00080 BY=0.00481 | queda maxT=NO Holm=SI BH=SI BY=SI
FIRME_006 visual_centrifugal  -> motor                                    BAJO  | p_max maxT=0.98020 Holm=0.04780 BH=0.00080 BY=0.00481 | queda maxT=NO Holm=SI BH=SI BY=SI
FIRME_006 visual_projection   -> descending                               BAJO  | p_max maxT=0.47865 Holm=0.04780 BH=0.00080 BY=0.00481 | queda maxT=NO Holm=SI BH=SI BY=SI
FIRME_006 visual_projection   -> motor                                    BAJO  | p_max maxT=0.43886 Holm=0.04780 BH=0.00080 BY=0.00481 | queda maxT=NO Holm=SI BH=SI BY=SI
FIRME_006 visual_projection   -> endocrine                                BAJO  | p_max maxT=0.94801 Holm=0.04780 BH=0.00080 BY=0.00481 | queda maxT=NO Holm=SI BH=SI BY=SI
NUEVO_CORREGIDO BH   ascending           -> motor:neck_motor_neuron                  SOBRE | p_max=0.00760
NUEVO_CORREGIDO BH   ascending           -> endocrine:IPC                            SOBRE | p_max=0.04671
NUEVO_CORREGIDO BH   central             -> motor:neck_motor_neuron                  SOBRE | p_max=0.00977
NUEVO_CORREGIDO BH   central             -> motor:salivary_motor_neuron              SOBRE | p_max=0.00817
NUEVO_CORREGIDO BH   descending          -> endocrine:CAPA                           SOBRE | p_max=0.01602
NUEVO_CORREGIDO BH   motor               -> motor                                    SOBRE | p_max=0.02842
NUEVO_CORREGIDO BH   sensory             -> motor:crop_motor_neuron                  SOBRE | p_max=0.03521
NUEVO_CORREGIDO BH   sensory             -> endocrine:DMS                            SOBRE | p_max=0.02128
NUEVO_CORREGIDO BH   sensory_ascending   -> motor                                    SOBRE | p_max=0.04834
NUEVO_CORREGIDO BH   sensory_ascending   -> motor:neck_motor_neuron                  SOBRE | p_max=0.00872
NUEVO_CORREGIDO BH   sensory_ascending   -> motor:salivary_motor_neuron              SOBRE | p_max=0.03876
NUEVO_CORREGIDO BH   sensory_ascending   -> endocrine:CRZ                            SOBRE | p_max=0.02923
NUEVO_CORREGIDO BH   sensory_ascending   -> endocrine:CAPA                           SOBRE | p_max=0.01602
NUEVO_CORREGIDO BY   ascending           -> motor:neck_motor_neuron                  SOBRE | p_max=0.04566
NUEVO_CORREGIDO BY   central             -> motor:salivary_motor_neuron              SOBRE | p_max=0.04907
```

Líneas 118 a 125 (cierre):

```text
RESUMEN firmes_006=41 (SOBRE=33 BAJO=8) | maxT quedan=11 nuevos=0 | Holm quedan=34 nuevos=0 | BH quedan=41 nuevos=13 | BY quedan=41 nuevos=2 | FWER (maxT y Holm) quedan=11, con alfa/2=0.025 quedan=0
CRUCE_006 PASS clases=True estratos=True d=True p=True flags=True conservacion=True firmes=True max_dif_d=0 max_dif_p=0
CONSISTENCIA PASS stepdown_le_singlestep=True monotono=True by_ge_bh=True holm_ge_bh=True holm_monotono=True
CONTROL_NEGATIVO maxT=10/160 Holm=8/160 BH=9/160 BY=0/160 esperado=8.0 tope=24.0 OK=True
R_PEDIDO_500 r=10000 veredicto_006=PASS ok=True
JSON results/output_control_permcorr_2026-10-10/output_control_permutation_correction.json md5=91c602099e533a962c889efe8516ef70
VEREDICTO_CORRECCION PASS
FIN_CORRECCION segundos=778.3
```

## 5. Archivos

| Archivo | Dónde | Bytes | md5 |
|---|---|---|---|
| `tools/output_control_permutation_correction.py` | rama, `95e8d6c` | 20.004 | `b1e0a0d312f843c015990c779871c130` |
| `tests/test_output_control_permutation_correction.py` | rama, `95e8d6c` | 8.120 | `e02910cb1d684d95f3a3b5c110e62607` |
| `results/output_control_permcorr_2026-10-10/run.log` | rama, `95e8d6c` | 16.524 | `23433cf56742e172f65ea0e4e5365940` |
| `results/output_control_permcorr_2026-10-10/tests.log` | rama, `95e8d6c` | 934 | `c8d4d2da927060328fd2e36e311a3efd` |
| `results/output_control_permcorr_2026-10-10/output_control_permutation_correction.json` | sólo brain-env | 420.891 | `91c602099e533a962c889efe8516ef70` |
| `results/output_control_permcorr_2026-10-10/progress.log` | sólo brain-env | 1.700 | `e59170078a329744211f8d516ecfcafb` |

Entradas: `connectivity.parquet` `3d802fd542b5d18570ba1ba0bb0abed9`, `annotations.tsv` (pin 17fc577) `719904abad876c68ace1b5690c9b9b63` y el JSON de la 006 `ec64172711d7d18040f6f09335d7521b`. Módulos que reusa, iguales a los de la rama (3/3, re-medidos en brain-env al cerrar): `tools/output_control_by_class.py` `5c6a6accd3b1d06e4a9c19cf65348ee3`, `tools/output_control_permutation_null.py` `393300a4ff47bcc14111d33d56b6dbb3` y `tools/output_control_region_correction.py` `fc7082b8a27b12736368d36a79af4907`.

Verificación del push: `git show FETCH_HEAD:<archivo> | md5sum` contra el archivo de brain-env, 4/4 iguales; el padre del commit es `2093d57` (la 008).

El cruce con la 007 y la 008 se contó en sandbox sobre `results/output_control_regionnull_2026-10-10/run.log` y `results/output_control_regioncorr_2026-10-10/run.log`, los dos en la rama.

Doc público: [Corrección múltiple del nulo fuerte (006): las 41 firmes aguantan FDR, 34 aguantan Holm y 11 max-T; lo que fallaba era la ubicación](https://app.clickup.com/90171457413/docs/2kza6fw5-20957).

## 6. NO MEDIDO

- La 007 con R = 10.000, para que Holm también pueda corregirla (en la 008 no podía).
- Holm con muchas más permutaciones (del orden de 100.000) para ordenar las 34 que hoy están todas en el piso.
- Qué tests de cola pesada fijan el z crítico de max-T (11,4 a 15,3 acá; 7,9 a 11,7 en la 008), y min-P, el FWER por rangos que aprovecha la dependencia entre tests.
- Si la concentración de rechazos falsos de Holm y BH en ≥1 estr es ruido o una inflación chica: haría falta un control negativo más grande en esa familia.
- Las afirmaciones de D2: la 006 no las firmó y acá tampoco; sus familias se corrigieron y se reportan.
- Lo que ya estaba NO MEDIDO: D2 con el nulo regional, el neuropilo de cada sinapsis, otras k y regiones anatómicas.
- Signo fisiológico, función de cada descendente en el cuerpo y causalidad.

--- METODO PROMETEO ---
Máquina: brain-env (2 núcleos), corrida de 778,3 s; tests 5/5 en sandbox y en brain-env.
Artefactos: `docs/agents/respuestas/2026-10-10-009-correccion-multiple-del-nulo-fuerte.md` + Doc https://app.clickup.com/90171457413/docs/2kza6fw5-20957
