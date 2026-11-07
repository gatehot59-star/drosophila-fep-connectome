# 2026-11-07-002 · G1-A corrida y SOSTENIDA en las dos moscas: lo que recibe de un descendente le habla a sus competidores (OR 2,3 en FlyWire y 3,0 en BANC cerebro) · pero las excitatorias y los relevos livianos hacen lo mismo: es homofilia de cableado, no veto

**Veredicto del pedido:** no perdí el hilo, pero sí se frenó. Del 4 al 7 de noviembre G1-A no avanzó porque cerré pidiendo un «dale» en vez de seguir. En este turno se hizo todo lo que faltaba de G1-A: instrumento con 8 de 8 pruebas que podían fallar, enmiendas fijadas antes de calibrar, calibración que pasa en las dos moscas, sello y cruce real. **H_G1_VETO: SOSTENIDA** por la tabla fijada el 4-nov. Los controles fijados en ese mismo diseño dicen que no es un veto: es una regla de cableado con los dos signos.

Doc: [2026-11-07-002 · G1-A sostenida en las dos moscas](https://app.clickup.com/90171457413/docs/2kza6fw5-26157/2kza6fw5-30777)

## En criollo

Lo que tenemos entre manos, en tres capas:

1. **El freno existe** (012, función en el LIF): en 17 de 22 circuitos, X frena a D′.
2. **La primera regla de la gramática** (esta respuesta, anatomía): si un descendente D le da un relevo a una interneurona X, esa X se conecta con los descendentes que compiten con D por la misma entrada visual casi el doble de lo que espera un modelo que sólo sabe cuánto conecta cada neurona (152 conexiones contra 88 esperadas en FlyWire, 88 contra 46 en BANC). Pasa en las dos moscas con el mismo tamaño; el número de FlyWire le explica a BANC el 94 % de lo que BANC se explica solo; y la regla cuesta un parámetro y ahorra unos 30 bits por mosca.
3. **Lo que la regla no es:** no es un veto. Las excitatorias con relevo pesado hacen lo mismo o más (OR 6,0 en FlyWire), y los relevos livianos igual que los pesados. El diseño ya decía qué significa eso: homofilia de cableado, no freno dirigido. Si funciona como veto lo deciden el signo y la actividad, y eso se prueba en G1-F, no en la anatomía.

## El resultado (sellado en f98cd9d3, leído con la tabla de 2026-11-04-001)

| | FlyWire 783 | BANC 888 cerebro |
|---|---|---|
| β̂ ± error robusto | 0,842 ± 0,284 | 1,096 ± 0,353 |
| OR [IC95] | **2,32 [1,33; 4,05]** | **2,99 [1,50; 5,98]** |
| p del nulo de 1.000 recableados (Holm) | 0,001 (0,002): ningún recableado llegó | 0,001 (0,002): ninguno llegó |
| β̃ observado contra el nulo | 0,629; nulo 0,110 ± 0,110, percentil 99 = 0,346 | 0,766; nulo 0,159 ± 0,143, percentil 99 = 0,446 |
| pares competidores con Y = 1 | 152, donde G0 esperaba 88,5 | 88, donde G0 esperaba 46,2 |
| pasa (p Holm < 0,01, OR ≥ 1,5, IC sin el 1) | sí | sí |

**Veredicto: SOSTENIDA.** BANC entero (secundaria) da lo mismo: OR 2,87 [1,52; 5,40], p 0,001, 91 contra 45,7.

## Los controles fijados el 4-nov

| Control | FlyWire 783 | BANC 888 cerebro | Qué dice |
|---|---|---|---|
| Dosis: relevos livianos (20 a 79 sinapsis, X sin pesado) | OR 3,21 [2,51; 4,12]; Δβ pesado − liviano −0,32 [−0,93; 0,29] | OR 2,63 [1,98; 3,50]; Δβ +0,13 [−0,62; 0,88] | no se distinguen: **el peso no importa** |
| Especificidad: X excitatorias con relevo pesado | OR 5,98 [2,76; 12,9], p 0,001; Δβ inh − exc −0,95 [−1,90; +0,01] | OR 5,02 [0,98; 25,7], p 0,18 (sólo 32 pares M informativos); Δβ −0,52 [−2,29; 1,25] | no se distinguen y la estimación va al revés: **homofilia, no veto** |
| Transferencia: el β de FlyWire puesto en BANC | | +33,0 bits, 0,0335 bits por par positivo, contra 0,0355 del β propio de BANC | el número viaja: 94 % |
| Descripción: G1 menos G0, con el costo del parámetro | +32,7 bits | +27,6 bits | G1 comprime |
| Costo del cruce | 58,1 s, pico 1,06 GiB | 60,7 s, pico 1,42 GiB | brain-env alcanza |

## La calibración que habilitó el cruce (f98cd9d3)

Pasó en las dos moscas con los cortes fijados antes, en d365b545: sesgo de β̂ entre −0,033 y +0,039, cobertura del IC95 entre 184 y 195 de 200, falsos positivos con β = 0 de 1 y 3 de 200 en FlyWire (p < 0,01 y p < 0,05) y de 2 y 11 en BANC, y 1.600 de 1.600 ajustes convergidos. Potencia a OR 1,5, dicha antes de cruzar: 0,60 en FlyWire y 0,23 en BANC cerebro; con OR 2 sube a 1,0 y 0,74. Los efectos medidos (OR 2,3 y 3,0) caen donde la prueba ve.

## Lo que hay que leer con cuidado

- **En los datos reales el error robusto es 2,7 veces (FlyWire) y 2,4 veces (BANC) el del modelo**, sobre todo por la agrupación por X (Vx domina): algunas X concentran la puntería. La calibración no podía ver eso, porque su Y sintética es independiente dado G0. Por eso el IC que se usa es el robusto, más ancho, y el p sale de recablear la anatomía con la Y real fija, que conserva esa dependencia. Los dos instrumentos coinciden: z de Wald 2,96 y 3,10, y p del nulo mínimo en las dos moscas.
- **Homofilia espacial sin medir.** G0 no sabe de neuropilo ni de posición. Si D, sus competidores y X comparten neuropilo, la regla podría ser cercanía y no lógica de circuito. El control con excitatorias apunta para ese lado, pero no lo prueba.
- El nulo recablea sólo la tabla S→D, y los recableados tienen más pares M = 1 que el real (2.077 contra 1.828 en FlyWire): los competidores reales están más concentrados que al azar. β̃ es un efecto medio por par, así que esa diferencia mueve más la varianza que el centro.

## Qué cambia para la gramática

Es la primera regla compacta que genera cableado más allá de los grados y se repite en otra mosca: **«las interneuronas que reciben de D se conectan con los competidores visuales de D»**, con un parámetro, unos 30 bits por mosca, y viaja de FlyWire a BANC. No es la regla que apostamos («D veta a sus competidores por X»): el veto necesita signo, y la anatomía dice que el signo no elige con quién se conecta.

## Qué sigue

1. **G1-F en el LIF:** si prender D apaga a sus competidores más que a los no competidores cuando el camino pasa por X inhibitorias, y los prende cuando pasa por excitatorias. Ahí vive el veto.
2. **Control de geometría para G1-A:** sumar a G0 un término de neuropilo compartido, si el dato está en brain-env (no lo miré todavía).
3. Deuda: réplica en Actions x64, CONTEXTO e issues de la deuda.

## 1. Pedido

«en criollo que tenemos entre manos, veo que no avanzamos o perdite el hilo?» (Abraham, chat, 7-nov-2026 16:41 ART). Se contesta en criollo y se lleva G1-A hasta su veredicto en el mismo turno.

## 2. Herramientas y máquina

- brain-env por el gateway (servicio build, python), host 6c09d8604b07: escribió sólo en /workspace/a1/v2/g1/a/ y leyó las cuatro entradas fijadas por md5 sin tocarlas. Procesos en segundo plano con correr_g1a.py, que deja el exit code de cada uno.
- Sandbox: prueba de la matemática con datos de juguete, sin datos de las moscas.
- GitHub MCP: tres commits a main (d365b545, f98cd9d3 y el de esta respuesta). Sin ramas, sin PR, sin merge.
- ClickUp: la página nueva del Doc de Topo inverso.
- Sin Actions, sin Kaggle, sin GPU, sin tocar trabajo ajeno.

## 3. Qué se midió

| # | Afirmación | Instrumento | ¿Podía dar rojo? | Veredicto |
|---|---|---|---|---|
| 1 | El instrumento usa las definiciones del censo | 6 conteos por grupo contra g1_censo.json: 3 grupos en las pruebas y 7 en el cruce | sí: aborta si uno no cuadra | PASS, 10 de 10 grupos |
| 2 | El ajuste por bloques es correcto | contra un ajuste completo independiente: G0 con Y real (4,6e-9) y G1 con Y sintética (2e-11); errores del modelo y Vx, Vd, V0 contra un sándwich denso | sí, y el control con L permutada dio 0,127 | PASS |
| 3 | El β̃ vectorizado es correcto | contra un Newton escalar en 21 listas | sí | PASS, 5e-15 |
| 4 | El banco es válido y determinista | grados, unicidad y lado en 1.000 de 1.000 por mosca; misma semilla, mismo sha | sí | PASS |
| 5 | El instrumento distingue | calibración, 800 réplicas por mosca, cortes fijados antes | sí: seis cortes por mosca | PASS en las dos |
| 6 | El cruce corrió con lo sellado | g1a.py verifica su sha256, la calibración y el sha del banco antes de cruzar | sí: aborta | PASS: a1c5ec69, f98cd9d3, 982cc13b y 1a2cef42 |
| 7 | H_G1_VETO | tabla de lectura de 2026-11-04-001, aplicada por el modo leer | sí: podía dar REFUTADA, NO_REPLICA o SIN_DECIDIR | **SOSTENIDA** |
| 8 | La puntería es propia de las inhibitorias | Δβ inh − exc con IC95 | sí | **no sostenido**: −0,95 [−1,90; +0,01] y −0,52 [−2,29; 1,25] |
| 9 | Depende del peso del relevo | Δβ pesado − liviano con IC95 | sí | **no sostenido**: −0,32 [−0,93; 0,29] y +0,13 [−0,62; 0,88] |
| 10 | El IC cubre bien con la dependencia real | calibración con Y independiente | **no**: no podía ver la dependencia de los datos reales | NO MEDIDO; se usa el error robusto, 2,4 a 2,7 veces el del modelo |

## 4. Evidencia cruda

Todo en docs/agents/evidencia/2026-11-07-002-g1a/, verbatim salvo las filas de la calibración, que van por sha256:

- 00-enmienda-antes-de-calibrar.md, g1a.py (a1c5ec69…), pruebas_g1a.py (e8e4b5b0…), correr_g1a.py (247d4b0d…) y 01-pruebas/, con el intento fallido en intento1/ (commit d365b545).
- 02-sello-antes-de-cruzar.md y 03-calibracion/ (commit f98cd9d3).
- 04-cruce/: cruce_flywire.json, cruce_banc.json, lectura_g1a.json, lectura_g1a.txt, cruce_flywire.log, cruce_banc.log y corrida.log (este commit).
- verificacion_post_push_1.log (9 de 9 iguales) y verificacion_post_push_2.log (8 de 8).

Comando del cruce: python3 /workspace/a1/v2/g1/a/correr_g1a.py /workspace/a1/v2/g1/a/corrida cruzar a1c5ec691636ca57763fd3a37b78a59fd0acc27f14a8b47d948ac1a3db6dcd5e f98cd9d36e8ae1a886442865592bac9745167525. Exit codes: cruce_flywire 0 (58,1 s), cruce_banc 0 (60,7 s), lectura 0 (3,3 s); salidas de error vacías.

lectura_g1a.txt, verbatim:

```plain
VEREDICTO H_G1_VETO: SOSTENIDA
flywire: beta 0.8422, OR 2.321 [1.330; 4.053], p 0.000999, p Holm 0.001998, Y1 en M 152 (G0 espera 88.5), pasa True
banc: beta 1.0962, OR 2.993 [1.497; 5.982], p 0.000999, p Holm 0.001998, Y1 en M 88 (G0 espera 46.2), pasa True
flywire dosis: delta -0.3247 [-0.9348; 0.2854] no_distinguible
flywire especificidad: delta -0.9457 [-1.8984; 0.0069] no_distinguible
flywire descripcion: 32.69 bits
banc dosis: delta 0.1284 [-0.6205; 0.8773] no_distinguible
banc especificidad: delta -0.5180 [-2.2904; 1.2544] no_distinguible
banc descripcion: 27.64 bits
banc entero: {"OR": 2.8692815214635123, "OR_hi": 5.402153392099796, "OR_lo": 1.5239805040433922, "beta_hat": 1.0540616574775226, "esperado_G0_en_M": 45.685863013612334, "n_Y1_en_M": 91, "p_nulo": 0.000999000999000999, "se_robusto": 0.3228304182670096}
transferencia: {"beta_flywire": 0.8421899074187019, "bits": 32.96726278111286, "bits_G1_propio_por_positivo": 0.03552436849405289, "bits_por_positivo": 0.033469302315850616, "conv": true, "it": 5, "ll_G0": -3767.855276042571, "ll_con_beta_flywire": -3745.0041107950638}
```

## 5. Archivos

Este archivo y la carpeta de evidencia de arriba.

## 6. NO MEDIDO

- La cobertura del IC con la dependencia real de los datos: la calibración usa Y independiente.
- Geometría y neuropilo: G0 no los tiene.
- Si la regla funciona como veto: es G1-F.
- La réplica en Actions x64 (enmienda 9).
- Qué parte del código tocan las pruebas: son 8 y pueden fallar, pero la cobertura de líneas no se midió.
- La calibración de las secundarias: sólo se calibraron los dos grupos primarios.
- Las huellas de BANC contra un pin externo: se cotejan contra las registradas en el censo.

## Estado vigente que CONTEXTO todavía no refleja

Suma a lo de 2026-11-04-001 y 2026-11-07-001. CONTEXTO sigue en la 2026-11-03-002; partirlo espera a Abraham.

- **G1-A: SOSTENIDA** (sello f98cd9d3 y este commit), con los dos controles en contra del veto: la regla que queda es de homofilia de cableado, con los dos signos.
- **Próximo:** G1-F en el LIF y control de geometría para G1-A.
- **Decisiones que esperan a Abraham:** cerrar T1 de 009-A1, la sección 15 del Doc maestro y partir CONTEXTO.

## QA (PROMETEO-QA)

Tipo: instrumento de diagnóstico más reporte con veredicto. Aplican Completitud, Ejecutabilidad, Arquitectura del razonamiento, Documentación, Innovación y Proceso QA (60 puntos).

| Criterio | Puntos | Evidencia |
|---|---|---|
| Completitud | 14/15 | instrumento, pruebas, enmiendas, calibración, sello, cruce, lectura y cinco secundarias, en d365b545, f98cd9d3 y este commit; −1 porque el bootstrap de X del diseño se reemplazó (enmienda 2) y la geometría no entra |
| Ejecutabilidad | 14/15 | correr_g1a.py reproduce todo con el comando del sello; rc 0 en pruebas, dos calibraciones, dos cruces y la lectura (03-calibracion/corrida.log y 04-cruce/corrida.log); −1 porque las rutas de las entradas son de brain-env |
| Arquitectura del razonamiento | 9/10 | G1 anidado en G0 con un parámetro, nulo condicional por recableado, cortes de calibración fijados antes de calibrar, sello antes de cruzar, y controles de dosis y signo que dieron en contra; −1 porque la calibración no podía ver la dependencia real |
| Documentación | 9/10 | respuesta, Doc y evidencia verbatim con sha256; −1 porque CONTEXTO sigue atrasado |
| Innovación | 5/5 | Newton por bloques 4,5 veces más rápido y verificado contra el completo (T3); nulo de 1.000 recableados vectorizado (T6); instrumento con candados de sha, calibración y banco; transferencia en bits |
| Proceso QA | 5/5 | cada número con archivo y sha; verificaciones post-push de 9 de 9 y 8 de 8, más la de este commit |
| **Total** | **56/60 → 93/100** | N/A: 40 puntos. Seguridad (15): sin superficie de ataque ni servicio. Testing (15): no aplica al tipo instrumento de diagnóstico; igual hay 8 pruebas que pueden fallar. DevOps (10): sin despliegue |

```plain
--- METODO PROMETEO ---
Accion delicada: NO (evidencia append-only; prueba sellada antes de cruzar)
Modo aplicado:   FULL
Maquina:         brain-env (host 6c09d8604b07, Python 3.12.14, NumPy 2.5.3, SciPy 1.18.1, pandas 3.0.5, pyarrow 25.0.1)
Rubrica:         56/60 -> 93/100 (instrumento de diagnostico + reporte)
N/A declarados:  40 (Seguridad, Testing, DevOps)
Review externo:  no pedido (deuda)
Instrumento:     g1a.py a1c5ec69, sello f98cd9d3; salida cruda en docs/agents/evidencia/2026-11-07-002-g1a/
Artefactos:      docs/agents/respuestas/2026-11-07-002-g1a-sostenida-en-las-dos-moscas-pero-es-homofilia-no-veto.md
                 + https://app.clickup.com/90171457413/docs/2kza6fw5-26157/2kza6fw5-30777
```
