# Respuesta 008 · corrección por comparaciones múltiples del nulo regional: con FDR quedan 31 de 33 firmes, con FWER sólo las descendentes y el óptico

**Fecha:** 2026-10-10, tarde (America/Buenos_Aires) · **Máquina:** brain-env · **Rama:** `titan/tabla7-reconstruida-2026-10-10` (PR #26, sin merge), commit `2093d57a4c5dd4969d573484f70f11e175e0cfb9`

**F-01, veredicto:** el instrumento da **PASS** (el nulo regenerado es idéntico al de la 007, la consistencia y el control negativo dan verde y R ≥ 500). De las 33 afirmaciones firmes de la 007, la tasa de falsos descubrimientos que vale con cualquier dependencia entre tests (Benjamini-Yekutieli, BY) deja 31, y la exigencia de ni un solo falso positivo por familia (FWER, max-T de Westfall y Young) deja 5: descendentes → descendentes, → motoras, → cuello y → antena, y óptico ▼ descendentes. El plus del central hacia las motoras de la boca y hacia DH44 aguanta BY (0,014 a 0,040) pero no max-T (0,58 a 0,91). Con BY caen las dos que eran sobre las motoras de ingestión: motoras → ingestión (0,062) y visual centrífuga ▼ ingestión (0,051). BH agrega 11 afirmaciones nuevas y ninguna aguanta BY: no se firman.

## 1. Pedido

"Apply multiple-comparisons correction to the regional null" (Abraham, 2026-10-10). Estaba en el NO MEDIDO de la 007: lo firme exigía cuatro flags concordantes con p ≤ 0,001 de cada lado, pero no estaba corregido por la cantidad de tests.

## 2. Herramientas

- brain-env por el gateway (2 núcleos, 7,8 GB): tests, corrida completa (676,3 s), md5 y verificación de los push.
- Sandbox de Brain: script, tests, reconstrucción del log (md5 igual al de brain-env antes de subir) y dos cuentas de resolución, que se citan como cuentas y no como corridas.
- GitHub MCP: push a la rama y a `main` (brain-env no tiene credencial de push para este repo).
- ClickUp: Doc público en el Space.

## 3. Qué se midió

- **Mismo nulo, regenerado:** semillas y parámetros leídos del JSON de la 007 (seed 20261012, R = 5.000, k = 40 y 120, 30 estratos de tamaño). Regiones, D1, p y flags de cada test tienen que salir idénticos (CRUCE_007): la diferencia máxima fue 0.
- **Familias:** cuatro, una por umbral (≥1 y ≥5) y granularidad (k = 40 y k = 120). Cada una tiene los tests clase × conjunto de salida cuyo nulo varía y cuyo desvío exacto es mayor a 1e-12: 214, 212, 199 y 186.
- **FWER:** max-T de Westfall y Young, step-down, sobre |z| = |D1 - E| / sd, con E y sd exactas del nulo. El observado cuenta como una permutación más. Usa la distribución conjunta de las 5.000 permutaciones, así que vale con cualquier dependencia (y la hay: las 11 clases de un conjunto suman 1).
- **FDR:** Benjamini-Hochberg (BH) y Benjamini-Yekutieli (BY) sobre el p bilateral de permutación, mín(1, 2 × mín(p_sobre, p_bajo)). BY vale con dependencia arbitraria; BH, sólo con dependencia positiva.
- **Firme corregido:** el mismo sentido con p ajustado ≤ 0,05 en las cuatro familias. Además se cuenta max-T con 0,05 / 4 = 0,0125 por familia, que da un FWER del 5% para las cuatro juntas.
- **Holm y Bonferroni no sirven acá:** con R = 5.000 el p bilateral mínimo es 0,0004 y Bonferroni pide 0,05 / 242 = 0,0002. No pueden rechazar nada por construcción (línea RESOLUCION), así que no se usan.
- **Chequeos que pueden dar rojo:** CRUCE_007; CONSISTENCIA (step-down ≤ single-step, ajustados monótonos en el orden de |z|, BY ≥ BH); CONTROL_NEGATIVO (20 etiquetados falsos por familia, sacados del mismo nulo con semilla [seed, umbral, índice del modo, 98] y corregidos igual que el real: los que tienen algún rechazo no pueden pasar de máx(3, 3 × 0,05 × 80) = 12 por método); R_PEDIDO_500 (R ≥ 500 y la 007 en PASS). El test extremo a extremo mueve un p del JSON de la 007 en 1e-6 y el cruce da FAIL; con R = 300 da INCOMPLETO.
- Todos los parámetros se fijaron en el script antes de correr, y hubo una sola corrida completa.

### Lectura

- **Aguanta todo (max-T en las cuatro familias):** descendentes → descendentes (p ajustado máximo 0,0002), → motoras (0,022), → cuello (0,037) y → antena (0,010); óptico ▼ descendentes (0,012). Descendentes → proboscis queda al borde (0,054).
- **Con FWER del 5% para las cuatro familias juntas (0,0125 cada una):** quedan 3, descendentes → descendentes, → antena y óptico ▼ descendentes.
- **Aguanta BY (31 de 33):** el resto de lo firme de la 007. El plus del central hacia las motoras, las de ingestión, proboscis y haustelo, y hacia DH44 (BY 0,014 a 0,040; max-T 0,58 a 0,91), y lo sensorial, la visual centrífuga, la proyección visual y el óptico por debajo de sus vecinas.
- **Caen con BY:** motoras → motoras de ingestión (0,062) y visual centrífuga ▼ motoras de ingestión (0,051). Las dos son sobre las motoras de ingestión.
- **BH agrega 11** (p ajustado máximo de 0,0096 a 0,047), y ninguna aguanta BY. No se firman.
- **El corte de la 007 ya era casi BY:** sobre + bajo por familia, 82, 57, 55 y 35 sin corregir contra 85, 57, 55 y 32 con BY.
- **Por qué max-T es tan duro acá:** su z crítico da de 7,85 a 11,73. Con unos 200 |z| normales independientes, el 95% del máximo estaría entre 3,64 y 3,67 (cuenta en sandbox). Entonces hay tests con colas mucho más pesadas que una normal, y max-T paga por ellos: el central → motoras, con z de +4,1 a +9,9, no llega. Cuáles son esos tests no está medido.
- **El óptico:** su mezcla es de 0,09 a 0,14 (007), así que se compara contra pocas vecinas no ópticas de su zona y su tamaño. Que aguante max-T dice que esas vecinas les mandan a las descendentes más que las ópticas de su mismo estrato; no dice cuáles son.
- **Para el paper:** FDR con BY como criterio, y marcado el subconjunto que aguanta max-T. Lo único que sobrevive a todo es lo de las descendentes, y el óptico casi sin hablarles.

### Calibración

- **Control negativo:** tuvieron algún rechazo 5 de 80 etiquetados falsos con max-T, 0 con BH y 0 con BY, contra 4 esperados con un FWER del 5% (tope 12). Para max-T es una prueba real: 5 de 80 es lo que da un FWER del 5%. Para BH y BY sólo detecta un error grueso, como no ajustar: con R = 5.000 y el nulo completo, BH necesita al menos 2 tests en el piso de 0,0004 y BY entre 9 y 11 (cuenta en sandbox), así que 0 de 80 es lo esperable. Que BH y BY estén bien implementados lo prueba el test contra la definición, con empates.
- **Resolución:** ningún test puede tener un BY máximo menor a 0,0139 ni un BH máximo menor a 0,0024, porque ese es el mínimo de la familia ≥5 con k = 120 a 5.000 permutaciones. 29 de las 33 firmes dan exactamente ese piso: entre ellas, el instrumento no puede ordenar cuál está más lejos del azar.

### Errores propios

- Ninguno en la corrida. En el Doc, el control negativo decía "contra 4 esperados" para los tres métodos; para BH y BY ese 4 es un techo, no lo esperable. Lo corregí en el Doc al cargar los commits.

## 4. Evidencia cruda (verbatim)

`results/output_control_regioncorr_2026-10-10/tests.log`:

```text
TEST test_bh_y_by_contra_la_definicion -> BH = definicion q_i = min_{j>=i} m p_(j) / j en 50 casos con empates; BY = BH x c(m)
TEST test_maxt_contra_fuerza_bruta -> step-down y single-step = fuerza bruta en 20 casos con empates; step-down <= single-step
TEST test_maxt_controla_fwer_con_dependencia_y_tiene_poder -> FWER empirico 0.048 (tope 0,085) con 12 tests correlacionados que suman cero; un efecto de 8 sd se detecta en el 100%
TEST test_resolucion_de_holm -> con R = 5.000 y 242 tests Holm no puede rechazar nada (0,0004 > 0,05/242); con 100 tests o R = 100.000 si
TEST test_familia_excluye_degenerados_y_detecta_lo_plantado -> la clase sin mezcla queda afuera de la familia (m = 4 de 6); el efecto plantado sale SOBRE y su vecina BAJO con maxT, BH y BY
TEST test_extremo_a_extremo_007_a_008 -> extremo a extremo: 005 -> 006 -> 007 -> 008, el nulo regenerado da los mismos p, R=300 da INCOMPLETO y un p movido 1e-6 en el JSON de la 007 da FAIL
TESTS_OK 6
```

`results/output_control_regioncorr_2026-10-10/run.log`, líneas 1 a 22 (encabezado, cruce, resolución y las cuatro familias):

```text
== output_control_region_correction.py :: correccion por comparaciones multiples del nulo regional (007) ==
ENTORNO python=3.12.14 numpy=2.5.3 scipy=1.18.1 pandas=3.0.5 maquina=brain-env
PARAMETROS_007 seed=20261012 r=5000 k_regiones=40,120 n_tam=30 veredicto_007=PASS | alfa=0.05 n_falsos=20 factor_control=3
INPUT parquet /workspace/connectivity.parquet md5=3d802fd542b5d18570ba1ba0bb0abed9 pin_ok=True
INPUT annotations /workspace/annotations.tsv md5=719904abad876c68ace1b5690c9b9b63 pin_ok=True
INPUT json_007 results/output_control_regionnull_2026-10-10/output_control_region_null.json md5=72427fdc69a583ca796f448f6aaae0a5 pin_ok=True
GRAFO n_nodos=138639 n_aristas=15091983 mapeo_biyectivo=True
REGIONES k=40 iteraciones=74 iguales_007=True
REGIONES k=120 iteraciones=100 iguales_007=True
RESOLUCION r=5000 p_min_bilateral=0.000400 tests_por_familia=242 bonferroni=0.000207 holm_puede_rechazar=False
NULO [>=1] reg40 R=5000 segundos=146.2 d1_igual_007=True p_iguales_007=True flags_iguales_007=True
FAMILIA [>=1] reg40 m=214 z_crit=9.56 | 007 SOBRE=21 BAJO=61 | maxT SOBRE=6 BAJO=3 | BH SOBRE=31 BAJO=72 | BY SOBRE=23 BAJO=62
FALSOS [>=1] reg40 n=20 con_rechazo maxT=2 BH=0 BY=0
NULO [>=1] reg120 R=5000 segundos=146.6 d1_igual_007=True p_iguales_007=True flags_iguales_007=True
FAMILIA [>=1] reg120 m=212 z_crit=8.04 | 007 SOBRE=16 BAJO=41 | maxT SOBRE=5 BAJO=4 | BH SOBRE=28 BAJO=60 | BY SOBRE=16 BAJO=41
FALSOS [>=1] reg120 n=20 con_rechazo maxT=0 BH=0 BY=0
NULO [>=5] reg40 R=5000 segundos=143.5 d1_igual_007=True p_iguales_007=True flags_iguales_007=True
FAMILIA [>=5] reg40 m=199 z_crit=11.73 | 007 SOBRE=17 BAJO=38 | maxT SOBRE=4 BAJO=1 | BH SOBRE=20 BAJO=46 | BY SOBRE=17 BAJO=38
FALSOS [>=5] reg40 n=20 con_rechazo maxT=2 BH=0 BY=0
NULO [>=5] reg120 R=5000 segundos=143.8 d1_igual_007=True p_iguales_007=True flags_iguales_007=True
FAMILIA [>=5] reg120 m=186 z_crit=7.85 | 007 SOBRE=11 BAJO=24 | maxT SOBRE=5 BAJO=2 | BH SOBRE=13 BAJO=36 | BY SOBRE=10 BAJO=22
FALSOS [>=5] reg120 n=20 con_rechazo maxT=1 BH=0 BY=0
```

Líneas 23 a 56 (nivel 1 corregido; cada campo en el orden ≥1 k=40, ≥1 k=120, ≥5 k=40, ≥5 k=120):

```text
-- NIVEL1 corregido (orden: >=1 reg40, >=1 reg120, >=5 reg40, >=5 reg120) --
NIVEL1 descending ascending           z=-4.6/-2.1/-2.5/-0.5 maxT=0.4067/0.9922/0.9254/1.0000 BH=0.0012/0.0890/0.0482/0.9696 BY=0.0071/0.5282/0.2833/1.0000
NIVEL1 descending central             z=+7.3/+0.9/+5.5/+0.8 maxT=0.1280/1.0000/0.3225/1.0000 BH=0.0012/0.4747/0.0018/0.7567 BY=0.0071/1.0000/0.0106/1.0000
NIVEL1 descending descending          z=+35.1/+28.9/+24.3/+21.5 maxT=0.0002/0.0002/0.0002/0.0002 BH=0.0012/0.0017/0.0018/0.0024 BY=0.0071/0.0101/0.0106/0.0139
NIVEL1 descending endocrine           z=-1.1/-0.8/-0.5/-0.4 maxT=0.9998/1.0000/1.0000/1.0000 BH=0.2019/0.3640/0.8594/1.0000 BY=1.0000/1.0000/1.0000/1.0000
NIVEL1 descending motor               z=-0.7/-1.4/-1.0/-0.7 maxT=1.0000/1.0000/1.0000/1.0000 BH=0.6399/0.2145/0.0889/0.0387 BY=1.0000/1.0000/0.5220/0.2249
NIVEL1 descending optic               z=-24.8/-18.4/-16.0/-11.6 maxT=0.0008/0.0002/0.0122/0.0002 BH=0.0012/0.0017/0.0018/0.0024 BY=0.0071/0.0101/0.0106/0.0139
NIVEL1 descending sensory             z=-13.5/-10.5/-9.7/-7.6 maxT=0.0066/0.0156/0.1010/0.0750 BH=0.0012/0.0017/0.0018/0.0024 BY=0.0071/0.0101/0.0106/0.0139
NIVEL1 descending sensory_ascending   z=-3.4/-1.6/-3.6/-2.8 maxT=0.7143/0.9994/0.6629/0.9180 BH=0.0012/0.1688/0.0018/0.0088 BY=0.0071/1.0000/0.0106/0.0508
NIVEL1 descending visual_centrifugal  z=-4.7/-5.3/-4.0/-3.9 maxT=0.3979/0.3045/0.5897/0.6255 BH=0.0012/0.0017/0.0018/0.0024 BY=0.0071/0.0101/0.0106/0.0139
NIVEL1 descending visual_projection   z=-1.3/-0.6/-1.8/-0.9 maxT=0.9998/1.0000/0.9978/1.0000 BH=0.3192/0.6891/0.1724/0.6868 BY=1.0000/1.0000/1.0000/1.0000
NIVEL1 descending sin_anotacion       z=-/-/-/- maxT=-/-/-/- BH=-/-/-/- BY=-/-/-/-
NIVEL1 motor      ascending           z=-4.8/-0.6/-3.5/-0.1 maxT=0.3915/1.0000/0.6919/1.0000 BH=0.0012/0.7135/0.0018/1.0000 BY=0.0071/1.0000/0.0106/1.0000
NIVEL1 motor      central             z=+9.9/+5.9/+7.5/+4.1 maxT=0.0362/0.2210/0.1606/0.5785 BH=0.0012/0.0017/0.0018/0.0024 BY=0.0071/0.0101/0.0106/0.0139
NIVEL1 motor      descending          z=+18.3/+17.2/+14.5/+14.4 maxT=0.0044/0.0002/0.0224/0.0002 BH=0.0012/0.0017/0.0018/0.0024 BY=0.0071/0.0101/0.0106/0.0139
NIVEL1 motor      endocrine           z=+1.4/-0.0/-0.3/-0.7 maxT=0.9996/1.0000/1.0000/1.0000 BH=0.1387/0.7645/1.0000/1.0000 BY=0.8248/1.0000/1.0000/1.0000
NIVEL1 motor      motor               z=+6.4/+4.0/+4.5/+3.9 maxT=0.2204/0.5379/0.4915/0.6279 BH=0.0081/0.0104/0.0546/0.0651 BY=0.0479/0.0619/0.3205/0.3779
NIVEL1 motor      optic               z=-12.5/-9.6/-10.5/-8.2 maxT=0.0074/0.0214/0.0936/0.0290 BH=0.0012/0.0017/0.0018/0.0024 BY=0.0071/0.0101/0.0106/0.0139
NIVEL1 motor      sensory             z=-7.8/-6.6/-6.6/-5.9 maxT=0.1018/0.1300/0.2050/0.2785 BH=0.0012/0.0017/0.0018/0.0024 BY=0.0071/0.0101/0.0106/0.0139
NIVEL1 motor      sensory_ascending   z=-1.9/-1.3/-1.5/-1.2 maxT=0.9930/1.0000/0.9988/1.0000 BH=0.0203/0.2646/0.0549/0.3959 BY=0.1207/1.0000/0.3226/1.0000
NIVEL1 motor      visual_centrifugal  z=-2.4/-2.6/-2.1/-2.2 maxT=0.9452/0.9358/0.9734/0.9786 BH=0.0012/0.0017/0.0018/0.0024 BY=0.0071/0.0101/0.0106/0.0139
NIVEL1 motor      visual_projection   z=-5.1/-5.9/-4.6/-4.5 maxT=0.3453/0.2186/0.4801/0.4693 BH=0.0012/0.0017/0.0018/0.0024 BY=0.0071/0.0101/0.0106/0.0139
NIVEL1 motor      sin_anotacion       z=-/-/-/- maxT=-/-/-/- BH=-/-/-/- BY=-/-/-/-
NIVEL1 endocrine  ascending           z=+0.1/+1.6/+1.4/+1.8 maxT=1.0000/0.9994/1.0000/0.9972 BH=1.0000/0.0220/0.3168/0.0248 BY=1.0000/0.1307/1.0000/0.1440
NIVEL1 endocrine  central             z=+2.1/+1.0/+0.4/+0.2 maxT=0.9872/1.0000/1.0000/1.0000 BH=0.0734/0.4524/1.0000/1.0000 BY=0.4361/1.0000/1.0000/1.0000
NIVEL1 endocrine  descending          z=+0.6/+0.7/+0.2/+0.6 maxT=1.0000/1.0000/1.0000/1.0000 BH=0.5981/0.5468/1.0000/0.8182 BY=1.0000/1.0000/1.0000/1.0000
NIVEL1 endocrine  endocrine           z=+6.7/+4.1/-0.5/-0.1 maxT=0.1694/0.5227/1.0000/1.0000 BH=0.0147/0.0017/1.0000/1.0000 BY=0.0875/0.0101/1.0000/1.0000
NIVEL1 endocrine  motor               z=-0.2/-0.4/-0.2/-0.3 maxT=1.0000/1.0000/1.0000/1.0000 BH=0.6192/0.8599/1.0000/1.0000 BY=1.0000/1.0000/1.0000/1.0000
NIVEL1 endocrine  optic               z=-2.8/-2.2/-2.1/-1.5 maxT=0.8800/0.9788/0.9744/1.0000 BH=0.0012/0.0017/0.0018/0.0137 BY=0.0071/0.0101/0.0106/0.0796
NIVEL1 endocrine  sensory             z=-1.6/-1.2/-0.9/-0.8 maxT=0.9980/1.0000/1.0000/1.0000 BH=0.1465/0.3789/0.7105/0.8034 BY=0.8712/1.0000/1.0000/1.0000
NIVEL1 endocrine  sensory_ascending   z=-0.7/-0.5/-0.8/-0.8 maxT=1.0000/1.0000/1.0000/1.0000 BH=0.7138/0.8775/0.9705/0.9595 BY=1.0000/1.0000/1.0000/1.0000
NIVEL1 endocrine  visual_centrifugal  z=-1.1/-1.1/-0.7/-0.7 maxT=0.9998/1.0000/1.0000/1.0000 BH=0.0022/0.0061/0.5202/0.4414 BY=0.0132/0.0359/1.0000/1.0000
NIVEL1 endocrine  visual_projection   z=-1.7/-1.4/-1.4/-1.1 maxT=0.9976/1.0000/1.0000/1.0000 BH=0.0097/0.0553/0.2647/0.2917 BY=0.0578/0.3280/1.0000/1.0000
NIVEL1 endocrine  sin_anotacion       z=-/-/-/- maxT=-/-/-/- BH=-/-/-/- BY=-/-/-/-
```

Líneas 57 a 101 (las 33 firmes de la 007 con corrección y las 11 nuevas de BH):

```text
-- FIRMES DE LA 007 CON CORRECCION (p ajustado maximo entre las cuatro familias; queda = <= 0.05 en las cuatro) --
FIRME_007 central             -> motor                                    SOBRE | p_max maxT=0.57848 BH=0.00240 BY=0.01393 | queda maxT=NO BH=SI BY=SI
FIRME_007 central             -> motor:ingestion_motor_neuron             SOBRE | p_max maxT=0.57848 BH=0.00240 BY=0.01393 | queda maxT=NO BH=SI BY=SI
FIRME_007 central             -> motor:proboscis_motor_neuron             SOBRE | p_max maxT=0.82763 BH=0.00697 BY=0.04049 | queda maxT=NO BH=SI BY=SI
FIRME_007 central             -> motor:haustellum_motor_neuron            SOBRE | p_max maxT=0.58388 BH=0.00240 BY=0.01393 | queda maxT=NO BH=SI BY=SI
FIRME_007 central             -> endocrine:DH44                           SOBRE | p_max maxT=0.90982 BH=0.00240 BY=0.01393 | queda maxT=NO BH=SI BY=SI
FIRME_007 descending          -> descending                               SOBRE | p_max maxT=0.00020 BH=0.00240 BY=0.01393 | queda maxT=SI BH=SI BY=SI
FIRME_007 descending          -> motor                                    SOBRE | p_max maxT=0.02240 BH=0.00240 BY=0.01393 | queda maxT=SI BH=SI BY=SI
FIRME_007 descending          -> motor:neck_motor_neuron                  SOBRE | p_max maxT=0.03679 BH=0.00240 BY=0.01393 | queda maxT=SI BH=SI BY=SI
FIRME_007 descending          -> motor:proboscis_motor_neuron             SOBRE | p_max maxT=0.05419 BH=0.00240 BY=0.01393 | queda maxT=NO BH=SI BY=SI
FIRME_007 descending          -> motor:antennal_motor_neuron              SOBRE | p_max maxT=0.00960 BH=0.00240 BY=0.01393 | queda maxT=SI BH=SI BY=SI
FIRME_007 motor               -> motor:ingestion_motor_neuron             SOBRE | p_max maxT=0.35013 BH=0.01063 BY=0.06169 | queda maxT=NO BH=SI BY=NO
FIRME_007 optic               -> descending                               BAJO  | p_max maxT=0.01220 BH=0.00240 BY=0.01393 | queda maxT=SI BH=SI BY=SI
FIRME_007 optic               -> motor                                    BAJO  | p_max maxT=0.09358 BH=0.00240 BY=0.01393 | queda maxT=NO BH=SI BY=SI
FIRME_007 optic               -> motor:ingestion_motor_neuron             BAJO  | p_max maxT=0.45591 BH=0.00240 BY=0.01393 | queda maxT=NO BH=SI BY=SI
FIRME_007 optic               -> motor:neck_motor_neuron                  BAJO  | p_max maxT=0.39912 BH=0.00240 BY=0.01393 | queda maxT=NO BH=SI BY=SI
FIRME_007 optic               -> motor:proboscis_motor_neuron             BAJO  | p_max maxT=0.35913 BH=0.00240 BY=0.01393 | queda maxT=NO BH=SI BY=SI
FIRME_007 optic               -> motor:antennal_motor_neuron              BAJO  | p_max maxT=0.51630 BH=0.00240 BY=0.01393 | queda maxT=NO BH=SI BY=SI
FIRME_007 optic               -> motor:eye_motor_neuron                   BAJO  | p_max maxT=0.99620 BH=0.00240 BY=0.01393 | queda maxT=NO BH=SI BY=SI
FIRME_007 optic               -> motor:haustellum_motor_neuron            BAJO  | p_max maxT=0.95901 BH=0.00240 BY=0.01393 | queda maxT=NO BH=SI BY=SI
FIRME_007 sensory             -> descending                               BAJO  | p_max maxT=0.10098 BH=0.00240 BY=0.01393 | queda maxT=NO BH=SI BY=SI
FIRME_007 sensory             -> motor                                    BAJO  | p_max maxT=0.27854 BH=0.00240 BY=0.01393 | queda maxT=NO BH=SI BY=SI
FIRME_007 sensory             -> motor:neck_motor_neuron                  BAJO  | p_max maxT=0.26295 BH=0.00240 BY=0.01393 | queda maxT=NO BH=SI BY=SI
FIRME_007 sensory             -> motor:proboscis_motor_neuron             BAJO  | p_max maxT=0.82783 BH=0.00240 BY=0.01393 | queda maxT=NO BH=SI BY=SI
FIRME_007 sensory             -> motor:antennal_motor_neuron              BAJO  | p_max maxT=0.51130 BH=0.00240 BY=0.01393 | queda maxT=NO BH=SI BY=SI
FIRME_007 sensory             -> motor:eye_motor_neuron                   BAJO  | p_max maxT=0.95521 BH=0.00240 BY=0.01393 | queda maxT=NO BH=SI BY=SI
FIRME_007 sensory_ascending   -> motor:proboscis_motor_neuron             BAJO  | p_max maxT=0.99840 BH=0.00346 BY=0.02032 | queda maxT=NO BH=SI BY=SI
FIRME_007 visual_centrifugal  -> descending                               BAJO  | p_max maxT=0.62547 BH=0.00240 BY=0.01393 | queda maxT=NO BH=SI BY=SI
FIRME_007 visual_centrifugal  -> motor                                    BAJO  | p_max maxT=0.97860 BH=0.00240 BY=0.01393 | queda maxT=NO BH=SI BY=SI
FIRME_007 visual_centrifugal  -> motor:ingestion_motor_neuron             BAJO  | p_max maxT=1.00000 BH=0.00875 BY=0.05081 | queda maxT=NO BH=SI BY=NO
FIRME_007 visual_projection   -> motor                                    BAJO  | p_max maxT=0.48010 BH=0.00240 BY=0.01393 | queda maxT=NO BH=SI BY=SI
FIRME_007 visual_projection   -> motor:ingestion_motor_neuron             BAJO  | p_max maxT=0.80664 BH=0.00240 BY=0.01393 | queda maxT=NO BH=SI BY=SI
FIRME_007 visual_projection   -> motor:proboscis_motor_neuron             BAJO  | p_max maxT=0.64647 BH=0.00240 BY=0.01393 | queda maxT=NO BH=SI BY=SI
FIRME_007 visual_projection   -> motor:antennal_motor_neuron              BAJO  | p_max maxT=0.85503 BH=0.00240 BY=0.01393 | queda maxT=NO BH=SI BY=SI
NUEVO_CORREGIDO BH   ascending           -> motor:ingestion_motor_neuron             BAJO  | p_max=0.02975
NUEVO_CORREGIDO BH   ascending           -> motor:neck_motor_neuron                  BAJO  | p_max=0.04706
NUEVO_CORREGIDO BH   central             -> endocrine:Hugin-RG                       BAJO  | p_max=0.02941
NUEVO_CORREGIDO BH   central             -> endocrine:CAPA                           BAJO  | p_max=0.02046
NUEVO_CORREGIDO BH   optic               -> endocrine                                BAJO  | p_max=0.01370
NUEVO_CORREGIDO BH   sensory             -> motor:haustellum_motor_neuron            BAJO  | p_max=0.02046
NUEVO_CORREGIDO BH   sensory             -> endocrine:DH44                           BAJO  | p_max=0.02177
NUEVO_CORREGIDO BH   sensory_ascending   -> motor:ingestion_motor_neuron             BAJO  | p_max=0.03482
NUEVO_CORREGIDO BH   sensory_ascending   -> motor:antennal_motor_neuron              BAJO  | p_max=0.01240
NUEVO_CORREGIDO BH   sensory_ascending   -> endocrine:CAPA                           SOBRE | p_max=0.01489
NUEVO_CORREGIDO BH   visual_projection   -> motor:haustellum_motor_neuron            BAJO  | p_max=0.00960
```

Líneas 102 a 109 (cierre):

```text
RESUMEN firmes_007=33 (SOBRE=11 BAJO=22) | maxT quedan=5 nuevos=0 | BH quedan=33 nuevos=11 | BY quedan=31 nuevos=0 | maxT con alfa/4=0.0125 quedan=3
CRUCE_007 PASS regiones=True d1=True p=True flags=True conservacion=True max_dif_d1=0 max_dif_p=0
CONSISTENCIA PASS stepdown_le_singlestep=True monotono=True by_ge_bh=True
CONTROL_NEGATIVO maxT=5/80 BH=0/80 BY=0/80 esperado=4.0 tope=12.0 OK=True
R_PEDIDO_500 r=5000 veredicto_007=PASS ok=True
JSON results/output_control_regioncorr_2026-10-10/output_control_region_correction.json md5=1ede492395bf7d2f6cb6b1c28ad41ed9
VEREDICTO_CORRECCION PASS
FIN_CORRECCION segundos=676.3
```

## 5. Archivos

| Archivo | Dónde | Bytes | md5 |
|---|---|---|---|
| `tools/output_control_region_correction.py` | rama, `2093d57` | 19.898 | `fc7082b8a27b12736368d36a79af4907` |
| `tests/test_output_control_region_correction.py` | rama, `2093d57` | 8.806 | `4fd4429c3cb9f57b7ddfba91cb5111b1` |
| `results/output_control_regioncorr_2026-10-10/run.log` | rama, `2093d57` | 13.919 | `5d84c64f284047929b8468c8d12fa263` |
| `results/output_control_regioncorr_2026-10-10/tests.log` | rama, `2093d57` | 962 | `188f32012c9749368de2d52bebaa1e66` |
| `results/output_control_regioncorr_2026-10-10/output_control_region_correction.json` | sólo brain-env | 166.564 | `1ede492395bf7d2f6cb6b1c28ad41ed9` |
| `results/output_control_regioncorr_2026-10-10/progress.log` | sólo brain-env | 878 | `7e6fd3ebe354ef2805c1d7938d3f3349` |

Entradas: `connectivity.parquet` `3d802fd542b5d18570ba1ba0bb0abed9`, `annotations.tsv` (pin 17fc577) `719904abad876c68ace1b5690c9b9b63` y el JSON de la 007 `72427fdc69a583ca796f448f6aaae0a5`. Módulos que reusa, iguales a los de la rama: `tools/output_control_by_class.py` `5c6a6accd3b1d06e4a9c19cf65348ee3`, `tools/output_control_permutation_null.py` `393300a4ff47bcc14111d33d56b6dbb3` y `tools/output_control_region_null.py` `cc4a494a53a3b8b27bd340ee268ff114`.

Verificación del push: `git show FETCH_HEAD:<archivo> | md5sum` contra el archivo de brain-env, 4/4 iguales; los tres módulos de brain-env, 3/3 iguales a los de la rama.

Doc público: [Corrección múltiple del nulo regional: con FDR quedan 31 de 33 firmes, con FWER sólo las descendentes y el óptico](https://app.clickup.com/90171457413/docs/2kza6fw5-20937).

## 6. NO MEDIDO

- Qué tests de cola pesada fijan el z crítico de max-T (7,85 a 11,73).
- FWER por rangos (min-P): con 5.000 permutaciones no puede rechazar nada. Harían falta al menos unas 10.000 por familia, y del orden de 100.000 para tener poder (cuenta, no corrida).
- La corrección múltiple de la 006: acá se corrigió sólo la 007.
- Lo que ya estaba NO MEDIDO en la 007: el neuropilo de cada sinapsis, D2 con el nulo regional, otras k y regiones anatómicas.
- Signo fisiológico, función de cada descendente en el cuerpo y causalidad.

--- METODO PROMETEO ---
Máquina: brain-env (2 núcleos), corrida de 676,3 s; tests 6/6 en sandbox y en brain-env.
Artefactos: `docs/agents/respuestas/2026-10-10-008-correccion-multiple-del-nulo-regional.md` + Doc https://app.clickup.com/90171457413/docs/2kza6fw5-20937
