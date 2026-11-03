# 2026-11-02-010 · Enmienda 009-A1: cortes selectivos y decisiones separadas, sin modificar el sello original

**El diseño 009 queda enmendado mediante este documento nuevo. El original, su JSON de sello y su generador se conservan byte por byte. No se ejecutó ninguna simulación nueva.**

La enmienda corrige poblaciones, intervenciones, unidades, inferencia y alcance. Conserva los 16 relevos, sus estratos, las guardas Q1 a Q4 y los umbrales mecánicos principales. Retira del plan confirmatorio la fórmula predictiva dimensionalmente incompatible, sin declararla refutada ni cambiar retrospectivamente el 009.

Ruta del Doc espejo: **Space > 2026-11-02-010 · Enmienda 009-A1: cortes selectivos y decisiones separadas, sin modificar el sello original**, sin carpeta intermedia.

## 1. Pedido, alcance y precedencia

Pedido literal: «Enmienda el diseño 009 sin tocar su sello».

Identificador nuevo: **H_MECANISMO_RELEVOS16 / 009-A1**. Fecha: 2-nov-2026, America/Buenos_Aires. Es una enmienda prospectiva para las intervenciones nuevas, informada por resultados históricos ya vistos. No es un prerregistro ciego de todo el proyecto.

Orden de lectura:

1. [Diseño 009 original, fijado en su commit](https://github.com/gatehot59-star/drosophila-fep-connectome/blob/c3b718dbdb69c9d0ad25e5a729f1d06cf2ed297a/docs/agents/respuestas/2026-11-02-009-diseno-corte-causal-16-relevos-recurrentes.md): registro histórico, inmutable.
2. [Auditoría que motiva la enmienda](https://github.com/gatehot59-star/drosophila-fep-connectome/blob/7c4b1cb15accb8d5fa8f25dfd9c4e02cbd930d73/docs/auditorias/2026-11-02-02-astra-topo-relevos-conservados-predictor-no-validado.md): evidencia y límites de las correcciones.
3. Este documento: manda únicamente sobre las cláusulas futuras que enumera. Una corrida deberá identificarse como **009-A1**, no como ejecución literal del 009.

Se autoriza aquí la documentación de la enmienda. No se emite una orden a otro agente, no se inicia una corrida y no se autoriza un merge. La implementación, su prueba y el manifiesto de ejecución son entregas posteriores. No se editaron el Doc 009 ni el Doc maestro de Topo inverso.

### Anclas que no deben cambiar

Base de trabajo re-leída: `main@7c4b1cb15accb8d5fa8f25dfd9c4e02cbd930d73`.

- Diseño 009: `docs/agents/respuestas/2026-11-02-009-diseno-corte-causal-16-relevos-recurrentes.md`; 30.215 bytes; blob `8f29a044acc06bc9fd5b1e981727ad1bf7b42b50`; SHA-256 `61ab66b7839bc38f1ad6caaee43e60e7f0524fddb3e37ff58ff49acb5c48f1ea`.
- Sello publicado: `docs/auditorias/evidencia/2026-11-02-02/sello_diseno_16_relevos.json`; 31.673 bytes; blob `4fe9ac1e5ba418dbb39470ae703797b311f59a4a`; SHA-256 `210b581792d183517d1e4e7771b8435e4a6acb537bc1ad383e5725c500073e93`.
- Generador original: `docs/auditorias/evidencia/2026-11-02-02/armar_sello_16_relevos.py`; 4.455 bytes; blob `ee7ce82e5fb2251a0c24286fcb252323f14505ab`; SHA-256 `f60624380e6344f21be5cc8608ba6ea913bf1971687c2d683eb91b3f845b2f62`.

**Precisión de integridad, no cambio del sello:** el JSON local citado por el 009 tiene 31.672 bytes y SHA-256 `00bf832c3697d76c70d6d5594b44b550217e5bb4540e1c898b4b6d950341f8bb`. El publicado contiene exactamente esos bytes más un LF final. Se comprobó que ya era así en `ddb62475470c863a7d2389a2612052f3e425e8a9`. Ambos JSON son iguales como datos. Para preservar Git se verifica el hash de 31.673 bytes, sin normalizar ni quitar el LF.

## 2. Qué cambia y qué se conserva

**Se conserva:** FlyWire v783; los sujetos R01 a R16 y sus raíces; estratos T1/T2/T3; cortes originales Q1/Q2/Q3/Q4, Q1 conjunto y Q4 conjunto; n=20, ensayos de 1.000 ms; tasas nominales A=150 Hz y B=50/25 Hz; umbrales T1 de 0,35 y 0,50; T2 de 0,40 y 40 %. Los resultados DNp04 y H_REUSO_CIERRE no se recalifican.

**Se enmienda:**

- §1 y procedencia de 009: el BANC usado es **v888**, no v626. DNp04→PVLP010 tiene máximo BANC **123**, no 138. BANC intervino en seleccionar los relevos; no es un holdout anatómico virgen.
- §3.2 y §6.4: sumar pesos no demuestra coincidencia temporal; el índice de ablaciones no identifica por sí solo OR o AND.
- §3.3: B es **entrada Poisson directa**, no clamp de salida ni garantía de tasas >10 Hz.
- §4 y §6.5: colaterales se cuentan y cortan sobre el D′ exacto. Q1 menos Q3 no aísla colaterales.
- §6 y §7: se fijan estimandos, familias estadísticas, denominadores y estados no informativos. A no se reemplaza por B cuando falla.
- §7, predicción tercera: **retirada como primaria en A1** por no fijar una predicción en la escala del efecto que pretendía contrastar. No se sustituye silenciosamente por otra fórmula.
- CN1: una arista débil con efecto grande es un resultado posible de la red, no prueba automática de un instrumento inválido.

Los rótulos «supraliminar» y «subumbral» designan el cálculo nominal de una espiga aislada en ese LIF. No garantizan disparo, coactivación ni transmisión en la red completa. El signo es el convenio por neurotransmisor del modelo; incluye glutamato inhibitorio, también en R15. No se afirma fisiología confirmada.

## 3. Sujetos y máscaras: el blanco no cambia entre condiciones

Se usa el mismo conjunto elegible de descendentes, `D = {j: flywire_units.D[j] >= 0}`. No se amplía a neuronas sin la anotación exigida.

Para un relevo, `G={d_idx}`. Para un hub conjunto, G contiene **todos** los drivers de esa instancia, incluidos los espejos expresamente listados en el 009. Se fija:

`D′(x,G) = {j en D: existe fila x→j con peso firmado negativo} \ G`.

D′ se calcula una sola vez desde el grafo intacto y no se filtra por tasa, efecto observado o intervención. La selección de brazos no puede cambiar D′. Para comparar cortes individuales con el conjunto de un hub se vuelve a leer cada brazo sobre **el mismo D′ conjunto**, no se mezclan los D′ de las filas R.

Máscaras nuevas, aplicadas sobre una copia de los pesos originales:

- **QCOL:** filas excitatorias con origen en G y destino en D′.
- **QXD:** filas inhibitorias desde x hacia D′.
- **Q1∪QCOL** y **Q1∪QXD:** uniones de filas, sin doble conteo.
- **ZA:** sólo `6128→59804`, AVLP080→DNp35.
- **ZA∪Q1_R01:** sólo `6128→59804` y `59804→30887`.
- **SHAM:** copia y procesamiento idénticos con máscara vacía.

Q2 y Q3 siguen anulando transmisión saliente, no la integración ni las espigas internas de la neurona. Q4 elimina otras entradas anatómicas al hub; no fuerza las salidas del driver. Una unión aplica cada fila una vez; fuera de la máscara los pesos deben quedar idénticos.

### Guardas nuevas por relevo, medidas sobre el parquet

Cada tupla es `(filas no nulas, suma absoluta de pesos sinápticos)`. Las 64 guardas originales no se reemplazan.

<table>
<tr><th>Relevo</th><th>n D′</th><th>QCOL</th><th>Q1∪QCOL</th><th>QXD</th><th>Q1∪QXD</th></tr>
<tr><td>R01</td><td>137</td><td>(27,935)</td><td>(28,1170)</td><td>(137,2672)</td><td>(138,2907)</td></tr>
<tr><td>R02</td><td>25</td><td>(6,135)</td><td>(7,315)</td><td>(25,271)</td><td>(26,451)</td></tr>
<tr><td>R03</td><td>40</td><td>(19,452)</td><td>(20,617)</td><td>(40,410)</td><td>(41,575)</td></tr>
<tr><td>R04</td><td>75</td><td>(35,566)</td><td>(36,721)</td><td>(75,907)</td><td>(76,1062)</td></tr>
<tr><td>R05</td><td>63</td><td>(20,237)</td><td>(21,391)</td><td>(63,770)</td><td>(64,924)</td></tr>
<tr><td>R06</td><td>113</td><td>(11,69)</td><td>(12,222)</td><td>(113,1318)</td><td>(114,1471)</td></tr>
<tr><td>R07</td><td>64</td><td>(19,84)</td><td>(20,212)</td><td>(64,775)</td><td>(65,903)</td></tr>
<tr><td>R08</td><td>70</td><td>(27,1527)</td><td>(28,1653)</td><td>(70,404)</td><td>(71,530)</td></tr>
<tr><td>R09</td><td>56</td><td>(17,307)</td><td>(18,427)</td><td>(56,608)</td><td>(57,728)</td></tr>
<tr><td>R10</td><td>138</td><td>(11,27)</td><td>(12,142)</td><td>(138,1928)</td><td>(139,2043)</td></tr>
<tr><td>R11</td><td>192</td><td>(41,670)</td><td>(42,781)</td><td>(192,2330)</td><td>(193,2441)</td></tr>
<tr><td>R12</td><td>62</td><td>(28,750)</td><td>(29,846)</td><td>(62,655)</td><td>(63,751)</td></tr>
<tr><td>R13</td><td>113</td><td>(8,10)</td><td>(9,103)</td><td>(113,979)</td><td>(114,1072)</td></tr>
<tr><td>R14</td><td>139</td><td>(8,70)</td><td>(9,161)</td><td>(139,1963)</td><td>(140,2054)</td></tr>
<tr><td>R15</td><td>173</td><td>(22,118)</td><td>(23,206)</td><td>(173,1818)</td><td>(174,1906)</td></tr>
<tr><td>R16</td><td>75</td><td>(32,734)</td><td>(33,822)</td><td>(75,917)</td><td>(76,1005)</td></tr>
</table>

Así se corrige la columna colateral de 009. Por ejemplo, R03 tiene **452** sinapsis excitatorias directas sobre su D′, no 1.944. Sus 410 sinapsis inhibitorias son sobre ese mismo D′. La comparación de conteos todavía no decide el balance funcional.

### Cuatro tipos de hub, seis instancias neuronales

<table>
<tr><th>Instancia</th><th>x</th><th>Drivers G</th><th>n D′ conjunto</th><th>QCOL conjunto</th><th>QXD conjunto</th></tr>
<tr><td>H1, CB0580</td><td>33912</td><td>41594,104203,19410</td><td>137</td><td>(29,147)</td><td>(137,1904)</td></tr>
<tr><td>H1b, CB0580</td><td>58129</td><td>58878,71368</td><td>113</td><td>(12,271)</td><td>(113,979)</td></tr>
<tr><td>H2, CB0534</td><td>19257</td><td>111205,130297</td><td>63</td><td>(39,321)</td><td>(63,770)</td></tr>
<tr><td>H3, CB0172</td><td>122969</td><td>27878,20277</td><td>74</td><td>(67,1300)</td><td>(74,896)</td></tr>
<tr><td>H4, PS100</td><td>45293</td><td>129110,53975</td><td>191</td><td>(68,750)</td><td>(191,2329)</td></tr>
<tr><td>H4b, PS100</td><td>112031</td><td>84751,69226</td><td>172</td><td>(53,446)</td><td>(172,1784)</td></tr>
</table>

Las uniones conjuntas y hashes de D′ están en la evidencia cruda de esta entrega. En particular, H3 tiene 74 blancos comunes, no los 75 de cada fila individual.

Para la cascada: **ZA=(1,388)** y **ZA∪Q1_R01=(2,623)**. Q6 histórico sigue siendo `(1677,18623)` y su unión con Q1 `(1678,18858)`. No son intervenciones equivalentes.

## 4. Entradas, condiciones y pareado

### Régimen A: reclutamiento por una entrada anatómica seleccionada

Se aplican 150 Hz de entrada Poisson a cada miembro de la población fijada, durante 1 s. No significa una tasa de salida garantizada ni un estímulo natural validado en la mosca.

- R01: LPLC1_right, 72 neuronas.
- R02: LTe65_left, 3.
- R03, R08 y R11: LPT04_HST_right, 1.
- R04 y R09: presinápticas excitatorias directas de tipos LAL014 o CB0132 sobre el driver, índices 61826 y 70277.
- R05: LC9_right, 92.
- R06 y R13: LTe49_right, 14.
- R07: presinápticas excitatorias directas de tipos PVLP137 o CB0529, índices 29603,29939,61559,116669.
- R10: LPT52_right, índice 47682.
- R12: LTe42b_right, índice 71560.
- R14: presinápticas excitatorias directas de tipos CL215 o CL095, índices 23917,48054,52007,84088,113573,118025.
- R15: Nod5_left, índice 113236.
- R16: LTe42c_right, índice 138092.

Para las visuales: tipo y lado exactos, `S>=0` e `inh=False` en las anotaciones fijadas. Los índices completos y hashes ya están en la evidencia. No se elige después otra entrada porque encienda mejor. LC4_right y LC11_right en R01 quedan como sensibilidades planificadas separadas, no sustituyen LPLC1_right.

### Régimen B: estimulación directa estandarizada, no clamp

50 Hz de entrada Poisson al driver y 25 Hz a cada miembro del D′ fijo. En cada instancia conjunta se estimulan simultáneamente todos sus drivers a 50 Hz, con fuentes independientes, y el D′ conjunto a 25 Hz.

Se conserva explícitamente la semántica de [model.py de Shiu, versión usada](https://github.com/philshiu/Drosophila_brain_model/blob/91bdd1e7/model.py): la entrada suma `0,275 mV × 250 = 68,75 mV` a `v` y fija el refractario de las neuronas estimuladas en cero. Las demás conservan 2,2 ms. Por eso B tampoco se describe como «biofísica pura» ni como simple incremento de tasa con propiedades celulares intactas. Estas condiciones se mantienen iguales entre los brazos comparados.

Las ecuaciones, signos, retardo 1,8 ms, constantes 20/5 ms, reposo y reset −52 mV y umbral −45 mV siguen esa referencia. A1 fija explícitamente paso de 0,1 ms, integración `linear` y lectura en `[0,1000 ms)`. El código futuro debe registrar sus versiones efectivas y demostrar la equivalencia de la rutina de entrada con esta semántica.

**No hay adaptación de intensidad para conseguir un resultado informativo.** Si un driver, hub o blanco queda silente, se informa. No se descarta ese blanco ni se cambian 25/50/150 Hz después de mirar.

### Brazos y semillas

Por cada R y régimen A/B: C0, Q1, Q2, Q3, Q4, QCOL, Q1∪QCOL, QXD, Q1∪QXD, QWEAK y SHAM. Los cuatro brazos C0/Q1/QCOL/Q1∪QCOL forman el factorial de colaterales; C0/Q1/QXD/Q1∪QXD, el de transmisión directa del hub.

En cada hub conjunto B: C0, Q2 del hub, Q4 conjunto, cada Q1 individual y Q1 conjunto. Todos usan la misma estimulación conjunta y el mismo D′ conjunto. No se comparan con los cortes individuales medidos estimulando un solo driver.

Se mantienen 20 réplicas, etiquetadas `s=0..19`, sin parada opcional ni ampliación posterior por significación. Cada réplica arranca del mismo estado inicial. El pareado exige **los mismos eventos externos por neurona y semilla entre condiciones**, no sólo llamar `seed(s)` en un orden de objetos distinto. Se conserva un hash del flujo de entrada; el identificador de brazo no entra en su derivación.

Contrato de semilla por fuente: primeros 16 hexadecimales de SHA-256 del texto UTF-8 `009-A1|grupo|s|indice|rol`, interpretados en base 16 (64 bits, sin truncado posterior a 32). `grupo` es `A_<poblacion>`, `B_R01` a `B_R16`, `B_H1` a `B_H4b`, o `C_<hub>`; `rol` es `aferente`, `driver`, `blanco` o `replay`. A/B usan fuentes Bernoulli independientes por tick de 0,1 ms, probabilidad `tasa_Hz × 0,0001`, con PCG64 por fuente: la discretización N=1 de la entrada Poisson especificada. El manifiesto guarda el texto exacto y eventos y rechaza colisiones entre claves distintas. La selección de entradas A compartidas conserva el mismo nombre de población entre los R correspondientes. La implementación debe conservar también el orden temporal de aplicación de la entrada de Shiu y se fija antes de producir resultados funcionales.

No se reutilizan los 20 ensayos históricos de otro régimen como réplicas de A1. Las 20 semillas representan variación de entrada dentro de un modelo, no 20 moscas.

## 5. Estimandos: efectos de intervención, no porcentajes exclusivos de mediación

Para semilla s: `Y_s(C)=sum_j espigas_j(C)/1 s`, j en el D′ fijo; `H_s(C)=espigas_x(C)/1 s`. Y se expresa en **Hz poblacionales**, no Hz por neurona. Se publican además las tasas por neurona.

Las métricas son cocientes de medias, no promedios de cocientes por semilla:

- `ΔQ = media_s[Y_s(Q)-Y_s(C0)]`.
- `r_Q1 = ΔQ1/ΔQ2`.
- `c_X = [media H(C0)-media H(Q1)]/media H(C0)`.
- `s4 = media H(Q4)/media H(C0)`.
- Para el hub conjunto se reemplaza Q1 por Q1 conjunto y se conserva su D′ común.

No se introduce un epsilon para ocultar un denominador nulo o negativo. No se recortan los cocientes a `[0,1]`: efectos negativos o mayores a uno son posibles en una red recurrente. Los nombres autorizados son «efecto relativo al bloqueo de salidas del hub», «caída relativa de actividad» y «actividad conservada tras Q4». Ninguno es por definición una fracción exclusiva de mediación.

El `r_Q1_global` histórico no es primario de A1: su población X de referencia no estaba definida para todas las nuevas entradas. No se inventa un C1 diferente por fila y se presenta como la misma variable.

### Colaterales y ruta directa

En el factorial de colaterales, con Q1 intacta o cortada:

- Efecto de quitar colaterales con relevo intacto: `Y(QCOL)-Y(C0)`.
- Efecto de quitar colaterales con relevo cortado: `Y(Q1∪QCOL)-Y(Q1)`.
- Interacción: diferencia entre esos dos efectos.

Para estudiar Q1 con la salida directa X→D′ anulada, se compara `Y(Q1∪QXD)-Y(QXD)` con `Y(Q1)-Y(C0)`. Se reportan diferencias y sus intervalos, sin convertir la interacción en una proporción exclusiva de una ruta. Q1−Q3 se conserva sólo como **diferencia entre dos bloqueos distintos de la red**.

## 6. Hubs y cascada: qué experimento permite qué nombre

### T2 primario: ablaciones bajo coactivación B

Se prueban seis instancias, no cuatro observaciones intercambiables. El corte conjunto se compara con la **media de los efectos de los cortes individuales bajo esa misma coactivación**. Superar esa media no demuestra sinergia; puede ser simplemente acumulación de contribuciones.

Se conserva el índice original de ablación sólo como descriptivo, con denominador declarado y sin epsilon. Se retiran los nombres automáticos OR/AND asociados a 1,25 y 0,80.

### Banco C separado: tabla de respuesta y sensibilidad al tiempo

Para hablar de compuertas se agrega un banco de transferencia explícitamente artificial:

1. Se impone la salida de los drivers, no su entrada Poisson: una fuente de espigas reemplaza los eventos salientes de cada driver sobre sus mismas aristas, con pesos y retardos intactos; se suprimen sus eventos endógenos para no duplicarlos. No se suman espigas forzadas y espontáneas.
2. Se aplica Q4 conjunto, de modo que X sólo recibe las entradas anatómicas de esos drivers; X no recibe Poisson directo. No se afirma que éste sea el contexto nativo.
3. Se ensayan todos los subconjuntos de drivers encendidos: 8 para H1 y 4 para cada una de las otras cinco instancias. Se fija el orden de drivers exactamente como en §3.
4. Por semilla se sortean sin reemplazo 50 ticks entre los 10.000 de 0,1 ms, con PCG64 y la semilla de §4 usando `indice=x_idx` y `rol=replay`; se ordenan los ticks. Todos los drivers encendidos reciben esa misma secuencia en la condición sincronizada. Cada uno emite exactamente 50 espigas en 1 s.
5. Con todos encendidos, el control temporal desplaza circularmente las secuencias, conservando sus conteos: 0/10 ms para dos drivers, 0/5/10 ms para tres. Se comparan sincronizado y desplazado con la misma semilla. Esto prueba sensibilidad a esos retardos, no a cualquier forma de coincidencia.

En la tabla descriptiva, una respuesta media de X ≥10 Hz se marca ON, ≤2 Hz OFF y el intervalo intermedio queda indeterminado. **OR compatible en C:** vacío OFF y todos los subconjuntos no vacíos ON. **AND compatible en C:** conjunto completo ON y todos los subconjuntos propios OFF. Lo demás es otra transferencia o un caso indeterminado; no se fuerza una etiqueta.

La prueba temporal es `H_sync-H_desplazado>0`, una por instancia, familia F_C de seis contrastes. Un resultado positivo permite «sensibilidad temporal en C». No convierte el rótulo descriptivo de la tabla en función fisiológica ni en prueba de integración nativa.

### R01: desinhibición específica

Bajo LPLC1_right se fija el factorial **ZA × Q1_R01 × QCOL_R01**: ocho brazos y un solo D′ de 137 neuronas. ZA afecta únicamente AVLP080→DNp35, no las otras 1.676 filas de Q6.

Tres contrastes planificados, familia F_R01:

- Sin Q1 y sin QCOL en ambos brazos: `tasa_DNp35(ZA)-tasa_DNp35(C0)>0`.
- Sin QCOL en los cuatro brazos y con Q1 sólo donde se nombra: `[H(ZA)-H(C0)]-[H(ZA∪Q1)-H(Q1)]>0`.
- Con QCOL presente en los cuatro términos: `[Y(ZA∪Q1∪QCOL)-Y(Q1∪QCOL)]-[Y(ZA∪QCOL)-Y(QCOL)]>0`.

Son una firma compatible con el eslabón propuesto en el modelo. QCOL controla esas colaterales directas, no todas las rutas alternativas de la red. No se llama «mediación completa». El contraste amplio Q6 frente a Q6∪Q1 puede conservarse como sensibilidad histórica, nunca como sustituto del ZA específico.

## 7. Decisión estadística cerrada para A1

### Activación y denominadores

En B, un caso es interpretable para r_Q1 primario si las tasas medias C0 de cada driver estimulado y del hub son ≥10 Hz; `ΔQ2≥5 Hz poblacionales`; el IC95 de ΔQ2 excluye cero; y la prueba de ΔQ2 positivo pasa F_B a Holm <0,01. Este umbral único reemplaza el 0,05 de activación del 009.

En A se publican esos criterios de magnitud y el intervalo del freno como perfil descriptivo, sin trasladarle los p ajustados de B ni inventar una familia A. Sus cocientes secundarios requieren denominador positivo e IC95 que excluya cero y no sostienen un claim confirmatorio.

Se reporta la fracción de blancos con C0≤2 Hz y con C0>10 Hz, pero no se excluye ninguno por ello. No se exige artificialmente que todos superen 10 Hz.

- Fallo de identidad, integridad, pareado, máscara, SHAM o plan completo: **INVALIDO_TECNICO**.
- Entrada A que no satisface activación: **NO_RECLUTADO_EN_A**, con la causa medida. No se diagnostica automáticamente «bloqueo aguas arriba».
- B no activado o sin freno de referencia informativo: **NO_INFORMATIVO_EN_B**. No se aumenta la entrada para rescatarlo.
- Denominador ≤0 o evidencia insuficiente de freno positivo: cociente primario `null`, con numerador, denominador y motivo. No equivale a r=0.
- Guardas válidas pero criterios estadísticos insuficientes: **SIN_DECIDIR**.

### Un solo test primario, familias explícitas

Se fija **t pareada unilateral sobre contrastes por semilla**, no «Wilcoxon/t» a elección posterior. Los márgenes se prueban antes de dividir:

- T1: `a_s=(Y_Q1-Y_C0)-0,35*(Y_Q2-Y_C0)` y `b_s=H_Q4-0,50*H_C0`.
- T2: `a_s=(Y_Q1conj-Y_C0)-0,40*(Y_Q2-Y_C0)`; `b_s=(H_C0-H_Q1conj)-0,40*H_C0`; `c_s=Y_Q1conj-media_i(Y_Q1i)`.

**F_B contiene 46 pruebas fijas:** 16 ΔQ2 de relevos, 6 ΔQ2 conjuntos, 6 contrastes T1 y 18 contrastes T2. Se aplica una sola corrección Holm sobre las 46 posiciones, con umbral <0,01 para todas, incluidas las 22 pruebas del freno de referencia. Los casos no evaluables conservan su posición: `p_observado=null`, `p_para_familia=1`, estado y motivo explícitos. Ese 1 es un centinela conservador para el ajuste, no un p obtenido ni evidencia de ausencia de efecto. Un fallo técnico conserva INVALIDO_TECNICO y bloquea el veredicto afectado; no se transforma en derrota científica. F_C tiene seis pruebas temporales y F_R01 tres, cada una a Holm <0,01. No se ofrece un único «p global» del proyecto.

La t implica un supuesto sobre la distribución de las diferencias; n=20 no lo elimina. Se publica como sensibilidad el test exacto de inversión de signos de las diferencias, sin elegir el más favorable ni sustituir la primaria. Este test no es un simple conteo binomial de signos: conserva magnitudes; cuando todas las diferencias no nulas comparten signo llega al piso histórico bilateral `2/2^20`.

IC95: bootstrap **BCa de 20.000 remuestreos pareados de semillas**, misma selección de filas para todos los brazos de un contraste. Semilla del remuestreo: `2026110209`, con PCG64; orden de contrastes lexicográfico por identificador. Se recalculan cocientes de medias en cada remuestreo. No se desechan remuestreos con denominador no positivo: en ese caso el intervalo del cociente queda **INDEFINIDO**. BCa degenerado no se convierte en certeza: intervalo no definido y SIN_DECIDIR para el criterio que lo necesite, aunque una t calculable se conserve como dato. Si la t tiene varianza cero, `p_observado=null` y `p_para_familia=1`; no se inventa un p. No se cambia de test para rescatar ese caso.

Los intervalos de cocientes T1 y T2 deben tener su límite inferior por encima de sus márgenes para sostener esas predicciones; el IC95 de `c_s` en T2 debe tener límite inferior >0. Los IC95 reportados son marginales; la corrección de afirmaciones positivas procede de las familias Holm, no de atribuirles simultaneidad a esos intervalos. F_B, F_C y F_R01 son preguntas distintas. Un claim conjunto sólo puede usar las decisiones de sus componentes; no se elige después la familia que haya salido positiva.

### Veredictos que no se intercambian

- **P_T1_B:** los tres casos R01/R02/R03 pasan activación, ambos márgenes, intervalos y F_B. B no salva una afirmación sobre A.
- **P_T2_B:** una instancia pasa los tres contrastes T2 y sus intervalos correspondientes. CB0580 pasa como tipo sólo si pasan H1 **y** H1b; PS100, sólo si pasan H4 **y** H4b; CB0534 usa H2 y CB0172 usa H3. Se sostiene si pasan al menos tres de esos cuatro tipos. No se elige el mejor hemisferio.
- **T3:** se informan efectos y activación, sin inventar una victoria por estrato que el 009 no definió.
- **A, colaterales y QXD:** perfiles secundarios planificados con estimaciones e IC; no se usan como nueva familia de descubrimientos significativos sin corrección predefinida.
- **F_C y F_R01:** cada contraste se informa por separado con su ajuste. Una firma completa exige que pasen todos sus componentes requeridos.

No cumplir p<0,01 no refuta una hipótesis. Si los datos no sostienen los márgenes, el resultado primario es SIN_DECIDIR; se muestran los intervalos que acotan o contradicen la predicción. Un fallo técnico no cuenta como derrota científica.

## 8. Predictor y controles: no trasladar el 7/7 a otro objetivo

El ajuste 008, R²=0,9065 y 7/7, queda como **descriptivo reproducido sobre siete combinaciones ya vistas**. La auditoría encontró que los controles de asignación de tasas a blancos no sostienen una validación mecanística: p publicado≈0,104 y control compartido por estímulo≈0,140.

La fórmula de 009, `r_X * sum_d w_Xd * r_d/(r_d+10 Hz)`, produce un score en Hz·sinapsis, no una fracción calibrada; r_Q1 es adimensional. Además, el score 008 evaluaba quitar salidas de X respecto de una referencia global; Q1 corta una entrada D→X y aquí se normaliza contra Q2. No son la misma intervención ni el mismo objetivo.

Por ello **P_ESTRATOS, punto 3, no puede dar SOSTENIDA en 009-A1**. Estado: RETIRADA_COMO_PRIMARIA_EN_A1; evaluación literal histórica NO MEDIDA. No se evalúa la fórmula con un D′ distinto, no se añade una normalización retrospectiva y no se le atribuyen los números de la exploración B009 que la auditoría retiró.

Una futura hipótesis predictiva necesita su propio mapeo a la variable objetivo, calibración independiente, referencia de inhibición explícita y reserva por familias de hub/driver/estímulo. Si las dependencias conectan todos los casos, no se fabrica un test independiente barajando filas. Ese proyecto queda fuera de esta enmienda, no bloquea la pregunta causal T1/T2 y no se presenta como implementado.

**QWEAK** se fija por anatomía: fila excitatoria D elegible→x de peso entre 1 y 5, fuera de G; elegir mayor peso, desempatar por menor índice de origen. Las filas elegidas están en la evidencia. |r_weak|<0,05 es pequeño; 0,05≤|r_weak|<0,10, intermedio; ≥0,10, sensibilidad alta a una arista débil. Si el denominador no es informativo, se reporta Δweak sin ratio. Ningún rango invalida por sí solo el instrumento.

Los negativos que sí invalidan una medición son verificables: SHAM idéntico a C0 espiga por espiga; máscara vacía realmente vacía; pesos fuera del objetivo intactos; rechazo de índice/root incorrecto, signo invertido, flujo de entrada desigual, ensayo faltante o duplicado. Antes de la corrida, el verificador debe rechazar recibos deliberadamente corruptos. La suma de pesos y el número de filas solos no bastan si se cortaron otras filas de igual peso.

## 9. Contrato de ejecución futura y organización

Árbol de esta entrega:

- `docs/agents/respuestas/2026-11-02-010-enmienda-009-a1-sello-original-intacto.md`: enmienda canónica, decisiones y recibo.
- `docs/agents/evidencia/2026-11-02-010-guardas-enmienda-009-a1.md`: instrumento estructural ejecutado, stdout completo, hashes y procedencia.
- Los tres archivos originales indicados en §1: sólo lectura, no reemplazados.

No se crea ahora un runner, un contenedor ni un workflow. Tampoco se presenta un diseño en prosa como código compilado.

Flujo: **sello histórico + enmienda → manifiesto de identidades/entradas/máscaras → implementación fijada y prueba con corruptos → autorización de corrida → datos por semilla → verificador distinto del productor → decisiones por familia**.

El manifiesto posterior debe materializar índices y roots, D′ y sus hashes, fuentes de entrada, máscaras con filas exactas, plan completo, condiciones, semillas, parámetros y versiones efectivas del runtime. Debe quedar commiteado antes de generar actividad nueva. Para los datos se conservan estas huellas ya medidas:

- `connectivity.parquet`: SHA-256 `efeb23fb99098e9c390f6869969b2a121a2ee92c833cfc45ecb2c1d8e1af0347`.
- `flywire_units.npz`: SHA-256 `fa92fcd493162db96b7d185af4231c701bb30ec6a413ab913b401829d3a1e2df`.

Cada registro futuro debe contener: `protocol_id`, `code_commit`, `input_hashes`, `subject_id`, `regime`, `condition`, `seed`, `input_events_hash`, `mask_hash`, `Dprime_hash`, conteos por neurona, duración, exit y estado técnico. El agregado contiene todos los casos previstos, n esperado/recibido, numeradores, denominadores, estimandos, IC, p sin ajustar, p ajustado y motivos de null. No se rellenan ensayos faltantes con ceros ni se borra un brazo fallido para cerrar.

Riesgos concretos y mitigaciones:

- **Cambio de sujeto o población:** comprobar índice y root más hash de D′, no sólo nombres de tipo.
- **Pareado falso por consumo distinto de RNG:** materializar eventos externos y verificar igualdad entre brazos.
- **Frontera entre estimulación y clamp:** A/B conservan semántica de entrada; C tiene contrato de reemplazo de salida y debe probar que no duplica eventos.
- **Selección por activación:** publicar A y B completos; no seleccionar sólo relevos que respondan.
- **Familias relacionadas e incertidumbre del modelo:** Holm soporta dependencia entre pruebas, pero no convierte réplicas técnicas en individuos ni cubre incertidumbre biológica.
- **Costo al escalar:** ejecución por celda/semilla y reanudación sólo de faltantes con huellas idénticas. No se estima aquí un tiempo total no medido ni se pide GPU por intuición.

Decisiones rechazadas: editar el sello para hacerlo coincidir con el nuevo plan; rescatar A con B; declarar OR/AND con un cociente de ablaciones; probar freno de Q1 con un predictor de Q2; invalidar toda la red porque una arista débil tenga efecto. Cada rechazo responde a una ambigüedad concreta de 009, no a una preferencia de estilo.

## 10. Medición de esta entrega, método y NO MEDIDO

Herramientas: conexión GitHub para lecturas y alta documental; MUDH Gateway/build para lectura de datos y diagnóstico estructural en **brain-env**; ClickUp para el Doc espejo; Nexus para el cierre. Ningún dataset ni parámetro de simulación fue modificado. No se gastó GPU ni se disparó Actions. El sandbox separado sólo se usó para redactar y revisar texto.

Instrumento nuevo ejecutado: `python3 /workspace/astra_009_a1_20261102/medir_guardas_a1.py`, **exit 0**, stderr vacío. Fuente SHA-256 `f511075d67eee8e8730cee05e020fb34247d74aefb06254cd8b4bbfa20c7e3e0`. Host `6c09d8604b07`, Python 3.12.14, NumPy 2.5.3. Escaneó las 15.091.983 filas. La fuente y el stdout sin recortes quedan en el archivo de evidencia; contienen hashes de poblaciones, índices A y todas las guardas nuevas. Esta medición prueba máscaras e identidades, **no causalidad dinámica**.

Se comprobaron los 16 tamaños D′, las 32 raíces driver/hub, las 16 poblaciones A no vacías y los 12 pesos de entrada visual; se midieron QCOL/QXD y sus uniones en los 16 relevos y seis instancias. Se distinguieron explícitamente ZA de Q6 y QCOL de Q3. La verificación histórica de las guardas originales se cita desde la auditoría previa, no se presenta como una corrida nueva.

**NO MEDIDO:** implementación y pruebas del runner A1, equivalencia ejecutada del nuevo replay C, nuevas tasas o efectos funcionales, potencia estadística de n=20, duración/costo de la corrida completa, robustez a parámetros neuronales, predicción fuera de muestra y causalidad biológica. Una enmienda documentada no es un experimento listo ni ganado.

Cambio de rol declarado: la auditoría previa era un dictamen; en este turno se redacta el diseño solicitado. No se presenta esta autorrevisión documental como una auditoría independiente de nuevos resultados.

Errores/incidentes propios: la copia local del informe previo ya no estaba en el sandbox; se trabajó con las fuentes Git y el taller preservado. El hash local del sello no se usó como hash de su blob publicado: se midió y documentó el LF adicional ya presente desde el commit original.

### QA documental y bloque de método

Un revisor de sólo lectura del diseño anterior examinó la enmienda y señaló tres precisiones: alfa de F_B, p centinela frente a p observado y brazos exactos de R01. Quedaron corregidas y releídas. Su evaluación final fue **45/45**: completitud 15/15 (§§2 a 8), razonamiento 10/10 (§§5 a 8), documentación 10/10 (§§1,3,4,7,10), innovación de diseño 5/5 (§6) y proceso 5/5 (§§3,4,7,9,10). No es una certificación del runner ni una medición funcional.

Se excluyen **55 puntos N/A**: ejecutabilidad de producto, seguridad de producto, testing de producto y DevOps. No se entregó software de producción. El ajuste final a semillas de 64 bits evita truncarlas a 32 y exige detectar colisiones; no cambia estimandos. El control local de texto detectó falsamente la palabra castellana «todo» como marcador TODO por buscar sin distinguir mayúsculas; se corrigió el control, no se ocultó contenido.

--- METODO PROMETEO / TITAN ---

- Acción delicada: **NO**, documentación y evidencia nuevas, append-only; ningún archivo histórico sobrescrito.
- Modo: **TITAN FULL**, GITHUB → ARCHITECT documental → DOCS → QA.
- Rúbrica documental: **45/45 = 100/100; 55 puntos N/A** por tipo de entrega.
- Revisión externa: de sólo lectura, tres precisiones cerradas; no auditó una corrida nueva.
- Instrumento: diagnóstico estructural nuevo, exit 0; fuente y stdout íntegros en el archivo de evidencia.
- Máquina: brain-env para datos y hashes; sandbox separado para redacción.
- Resultado entregado: enmienda 009-A1 y evidencia; ejecución experimental **NO MEDIDA**.

[Evidencia completa publicada](https://github.com/gatehot59-star/drosophila-fep-connectome/blob/main/docs/agents/evidencia/2026-11-02-010-guardas-enmienda-009-a1.md), commit `08072b85ac1989971c09f7dc5ca7433884f937d2`: tres bloques re-leídos y comparados contra los originales, **3/3 idénticos byte a byte**. En ese commit se re-leyeron los tres archivos protegidos: **3/3 hashes SHA-256 sin cambios**. El cierre verifica nuevamente esos tres archivos después de publicar la enmienda.

Doc espejo publicado: [2026-11-02-010 · Enmienda 009-A1: cortes selectivos y decisiones separadas, sin modificar el sello original](https://app.clickup.com/90171457413/docs/2kza6fw5-26337).
