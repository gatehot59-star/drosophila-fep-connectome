# 2026-11-04-001 · G1 arrancado: la primera prueba de la gramática pregunta si el freno apunta a los competidores del descendente que lo prende · diseño de G1-A listo para sellar y censo de las dos moscas

**Veredicto del pedido:** «SIGUE», después de la 012, se lee como seguir por G1, que fue lo que recomendé. Queda escrito el diseño de G1-A, la primera prueba de la gramática (anatómica), con el universo medido en FlyWire 783 y BANC 888. **Todavía no se probó nada:** el censo cuenta cada pieza por separado y nunca cruza lo que se va a probar. Lo que falta para sellar es calibrar el instrumento con grafos sintéticos y fijar los márgenes con esa calibración.

Doc: [2026-11-04-001 · G1 arrancado](https://app.clickup.com/90171457413/docs/2kza6fw5-26157/2kza6fw5-29817)

## En criollo

La 012 dejó dos reglas: «X frena a D′» (17 de 22 circuitos) y «a veces el propio descendente prende el freno». Para que eso sea gramática y no sólo una lista de casos, el freno tiene que tener puntería. La pregunta de G1-A es: cuando un descendente le da un relevo pesado a una inhibitoria, ¿esa inhibitoria frena justo a los descendentes que compiten con él, los que reciben la misma entrada visual? Si sí, hay una frase corta que predice cableado que un modelo de bloques no ve. Si no, el freno existe pero apunta a cualquiera, y la regla se queda en «X frena».

## La regla que se prueba: H_G1_VETO

**Definiciones**, iguales a H_REUSO salvo donde se dice (reuso_mosca.py, sha256 3650fc74…):

- S: unidad tipo y lado de proyección visual. D: unidad tipo y lado de descendente. X: neurona inhibitoria (signo por neurotransmisor predicho) que no es S ni D.
- **Relevo pesado:** una sola fila D→X con 80 sinapsis o más (el umbral de los 17 relevos conservados).
- **Competidor:** D′ distinto de D que comparte con D una misma unidad S cableada a los dos (20 sinapsis o más y mismo lado, la definición de cableado de H_REUSO).
- **Y(x, D′) = 1** si x le da 5 sinapsis o más a la unidad D′ (el umbral X→D de H_REUSO).
- **M(x, D′) = 1** si D′ es competidor de algún driver pesado de x. **L(x, D′) = 1** si D′ está del mismo lado que algún driver de x. M está contenido en L.
- **Pares:** cada x con relevo pesado contra cada unidad D′ que no sea su driver.

**Modelos** (logístico sobre los pares):

- **G0:** logit P(Y = 1) = θ_x + φ_D′ + γ·L. Propensión de cada X y de cada D′, más «mismo lado que el driver». Es la corrección de grado por nodo.
- **G1 = G0 + β·M.** Un solo parámetro más: el mismo presupuesto más uno, y se cobra en la longitud de descripción.
- Se descartan las X y las D′ sin ningún Y = 1: con efectos fijos por nodo no informan β. Se informa cuántas.

**Estadístico primario:** β̃, la estimación de β con θ, φ y γ fijados en su ajuste de G0 (el ajuste de G0 no mira M). **Nulo:** 1.000 recableados por mosca de la tabla S→D cableada, conservando el grado de cada S y de cada D dentro de cada lado; se recalcula M y se re-estima β̃ igual. p = (k + 1)/(1.000 + 1), Holm sobre las dos moscas. **Tamaño del efecto:** OR = e^β con β del ajuste conjunto, IC95 por bootstrap de las X (2.000 remuestreos).

**Moscas:** FlyWire 783 entera (es sólo cerebro). **BANC 888 sólo cerebro**, X con region distinta de ventral_nerve_cord: el censo mostró que 225 de las 293 X con relevo pesado de BANC están en el cordón, y FlyWire no tiene cordón. BANC entero queda como análisis secundario.

## Lectura fijada antes de mirar (H_G1_VETO, margen OR 1,5)

| Si sale | Veredicto | Quiere decir | Para la gramática |
|---|---|---|---|
| en las dos moscas: p Holm < 0,01, OR ≥ 1,5 e IC sin el 1 | SOSTENIDA | el freno apunta a los competidores del descendente que lo prende | primera regla con dirección: «D veta a sus competidores por X» |
| FlyWire pasa; en BANC el IC incluye el 1,5 pero no pasa | SOSTENIDA_EN_FLYWIRE | una mosca sí, la otra no alcanza a decidir | regla de una mosca, falta réplica |
| FlyWire pasa; en BANC el IC queda entero debajo de 1,5 | NO_REPLICA | no se repite en la otra mosca | no es gramática todavía |
| en las dos el IC queda entero debajo de 1,5 | REFUTADA | el freno no apunta a competidores más allá de los grados | la regla se queda en «X frena»; G0 alcanza para el cableado |
| cualquier otra combinación | SIN_DECIDIR | el dato no alcanza | no suma ni resta |
| falla un control de la calibración | INVALIDO | el instrumento no distingue | no se lee nada |

**Secundarias, también fijadas ahora:**

1. **Dosis:** β de relevos livianos (20 a 79 sinapsis, X sin ningún pesado) menor que β de pesados. La auditoría 2026-11-02-01 (B-01) encontró que el cierre agregado con umbral 20 no supera a un nulo de etiquetas D; si livianos y pesados dan igual, el peso no es lo que importa.
2. **Especificidad:** β de X excitatorias con relevo pesado menor que β de inhibitorias. Si dan igual, es homofilia de cableado (los parecidos se conectan entre sí), no veto.
3. **Transferencia:** el β de FlyWire mejora la verosimilitud de BANC (bits por arista positiva) frente a β = 0, con θ y φ reajustados en BANC. Condicionada a los grados de BANC, y se rotula así.
4. **Descripción:** diferencia de bits entre G1 y G0, con el costo del parámetro.
5. **Costo:** segundos y memoria del ajuste.

**Calibración antes del sello, sin cruzar Y con M reales:** grafos sintéticos con los marginales de este censo, Y generada desde el G0 ajustado y un β plantado de 0; 0,4; 0,7 y 1,1 sobre el M real. Pasa si recupera β con sesgo menor a 0,1, el IC95 cubre entre 93 y 97 % y con β = 0 da p < 0,01 en a lo sumo el 1 % de 200 réplicas. Con eso se fija la potencia a OR 1,5 en cada mosca; si en BANC cerebro queda debajo de 0,8, el sello lo dice antes de correr.

## Censo del universo (sólo marginales)

| | FlyWire 783 | BANC 888 |
|---|---|---|
| neuronas / aristas | 138.639 / 15.091.983 | 188.508 / 13.620.865 |
| unidades S / D | 652 / 925 | 842 / 901 |
| pares S→D cableados | **996**, igual a H_REUSO | **753**, igual a H_REUSO |
| pares de descendentes co-impulsados | 2.866 | 1.996 |
| X inhibitorias con relevo pesado | 121 (176 filas) | 293, de las cuales 68 en el cerebro |
| pares x, D′ · Y = 1 · M = 1 (pesadas inhibitorias) | 111.751 · 2.189 · 1.828 | cerebro: 61.149 · 985 · 864 |
| X excitatorias con relevo pesado (control) | 104: 96.032 · 859 · 762 | cerebro 36: 32.385 · 400 · 125 |
| X livianas sin pesado (dosis) | 703: 648.930 · 7.534 · 10.785 | cerebro 526: 472.839 · 4.892 · 6.797 |

Si Y y M fueran independientes, en FlyWire caerían unas 36 aristas en los pares competidores (2.189 × 1.828 / 111.751) y en BANC cerebro unas 14. Es la escala de la prueba: alcanza para OR grandes y queda justa para 1,5 en BANC. La calibración lo dirá con número.

## Semilla para G1-F (descriptivo, post hoc sobre la 012)

G1-F es la parte funcional y viene después de G1-A. Para elegir su regla de encendido medí, en los 17 circuitos con freno de la 012, qué parte de la entrada excitatoria de X viene de sus drivers. La correlación con c_X en B es Spearman 0,65 (p 0,004) y con r_Q1, 0,60 (p 0,011). Pero las fracciones son chicas, de 1,6 a 18 %: en R01 el descendente pone 6,6 % de la entrada de CB0527 y en B le explica el 99 % de la actividad. O sea, quién prende el freno depende de qué entradas están activas en ese régimen, no de cuánto pesa la anatomía sola. G1-F va a necesitar una regla por régimen.

## Qué sigue

1. **Instrumento de G1-A y calibración sintética** en brain-env, con pruebas que puedan fallar.
2. **Sello:** márgenes y potencia con la calibración, antes de cruzar Y con M reales.
3. **Corrida en Actions x64**, testigo limpio (H_REUSO costó de 400 a 650 s y 2,9 GiB ahí), con las entradas fijadas por md5. Armar ese workflow es acción delicada y va con su rúbrica.

## 1. Pedido

«SIGUE» (Abraham, chat, 4-nov-2026). La 012 ofrecía cerrar R02 con otro sobre o arrancar G1, y recomendaba G1; se sigue por G1.

## 2. Herramientas

- brain-env por el gateway (servicio build, python): lectura de la 001, la auditoría 2026-11-02-01, la 008 y CONTEXTO desde raw; censo con g1_censo.py sobre /workspace/connectivity.parquet, /workspace/annotations.tsv y /workspace/banc_888/; chequeo del signo de los drivers de la semilla sobre connectivity.parquet. Escribió sólo en /workspace/a1/v2/g1/.
- ClickUp: lectura de la página madre de Topo inverso y la página nueva del Doc.
- GitHub MCP: este commit.
- Sin Actions, sin GPU, sin merge, sin tocar trabajo ajeno.

## 3. Qué se midió

| # | Afirmación | Instrumento | ¿Podía dar rojo? | Veredicto |
|---|---|---|---|---|
| 1 | El censo usa las definiciones de H_REUSO | pares S→D cableados: 996 en FlyWire y 753 en BANC | sí: una definición distinta cambia el número | PASS, iguales a los denominadores de H_REUSO |
| 2 | Los datos de FlyWire son los fijados | md5 de connectivity.parquet (3d802fd5…) y annotations.tsv (719904ab…) contra el PIN de reuso_mosca.py | sí | PASS |
| 3 | En BANC, la mayoría de las X con relevo pesado está en el cordón | columna region del meta de BANC | sí | medido: 225 de 293 |
| 4 | El censo no cruza Y con M | lectura de g1_censo.py: Y y M se cuentan en bucles separados y nunca se alinean par a par | el código, sí; lo que yo haya hecho fuera de él, no | DECLARADO |
| 5 | La parte anatómica de la entrada ordena el encendido | Spearman de scipy, n = 17 | sí | descriptivo: 0,65 con c_X, 0,60 con r_Q1 |
| 6 | La fracción de la semilla es parte de la entrada excitatoria de X | signo FlyWire (alguna arista saliente con Excitatory < 0) de los drivers y las X de las 22 filas | sí: un driver inhibitorio la volvería otra cosa | PASS: 0 de 29 drivers inhibitorios (con repeticiones), 22 de 22 X inhibitorias |

## 4. Evidencia cruda

En docs/agents/evidencia/2026-11-04-001-g1-censo/, verbatim: g1_censo.py, g1_censo.log y g1_censo.json (con las huellas de las cuatro entradas y la tabla de la semilla). Comando: python3 g1_censo.py /workspace/a1/v2/g1/censo, lanzado en segundo plano; terminó con FIN a los 47,4 s y sin nada en la salida de error. Entradas:

| Archivo | Bytes | md5 |
|---|---|---|
| connectivity.parquet | 100.804.642 | 3d802fd542b5d18570ba1ba0bb0abed9 |
| annotations.tsv | 31.718.505 | 719904abad876c68ace1b5690c9b9b63 |
| banc_888_meta.feather | 57.503.026 | 8c2b93a608c7163ec9d94d68e0756ff4 |
| banc_888_edgelist_simple_v3.feather | 359.161.658 | 08542b0771db7418ed474be60dc9886c |

Chequeo del signo de los drivers, corrido después del censo por el gateway, sin archivo propio. Código entero:

```plain
import json, numpy as np, pyarrow.parquet as pq
conn='/workspace/connectivity.parquet'
t=pq.read_table(conn,columns=['Presynaptic_Index','Excitatory'])
pre=t.column('Presynaptic_Index').to_numpy().astype(np.int32)
exc=t.column('Excitatory').to_numpy().astype(np.int8)
del t
n=138639
inh=np.zeros(n,bool); inh[pre[exc<0]]=True
print('n_inh',int(inh.sum()))
j=json.load(open('/workspace/a1/v2/g1/censo/g1_censo.json'))
mal=0
for f in j['semilla_g1f']['filas']:
    G=f['drivers']; gi=[bool(inh[g]) for g in G]
    mal+=sum(gi)
    print(f['sujeto'], f['x'], 'x_inh', bool(inh[f['x']]), 'G_inh', gi, f['estado_B'], f['fraccion_exc_de_drivers'])
print('drivers_inhibitorios', mal)
```

Salida, verbatim (exit 0, stderr vacío):

```plain
n_inh 41333
H1 33912 x_inh True G_inh [False, False, False] ACTIVADO 0.0543
H1b 58129 x_inh True G_inh [False, False] NO_INFORMATIVO_EN_B 0.0423
H2 19257 x_inh True G_inh [False, False] ACTIVADO 0.1812
H3 122969 x_inh True G_inh [False, False] ACTIVADO 0.1292
H4 45293 x_inh True G_inh [False, False] ACTIVADO 0.0398
H4b 112031 x_inh True G_inh [False, False] ACTIVADO 0.0488
R01 30887 x_inh True G_inh [False] ACTIVADO 0.0656
R02 80081 x_inh True G_inh [False] NO_INFORMATIVO_EN_B 0.0694
R03 116067 x_inh True G_inh [False] ACTIVADO 0.0569
R04 122969 x_inh True G_inh [False] ACTIVADO 0.0824
R05 19257 x_inh True G_inh [False] ACTIVADO 0.099
R06 676 x_inh True G_inh [False] ACTIVADO 0.0269
R07 19257 x_inh True G_inh [False] ACTIVADO 0.0823
R08 117221 x_inh True G_inh [False] ACTIVADO 0.0156
R09 86580 x_inh True G_inh [False] NO_INFORMATIVO_EN_B 0.0309
R10 33912 x_inh True G_inh [False] ACTIVADO 0.0225
R11 45293 x_inh True G_inh [False] ACTIVADO 0.0223
R12 83980 x_inh True G_inh [False] NO_INFORMATIVO_EN_B 0.029
R13 58129 x_inh True G_inh [False] NO_INFORMATIVO_EN_B 0.0219
R14 33912 x_inh True G_inh [False] ACTIVADO 0.0178
R15 112031 x_inh True G_inh [False] ACTIVADO 0.026
R16 122969 x_inh True G_inh [False] ACTIVADO 0.0468
drivers_inhibitorios 0
```

Nota para leer el JSON: en liviano_inh_sin_pesado, n_aristas_relevo cuenta las filas livianas antes de sacar las X que también tienen relevo pesado (1.913 en FlyWire). No entra en ninguna cifra de esta respuesta.

## 5. Archivos

- Este archivo.
- docs/agents/evidencia/2026-11-04-001-g1-censo/g1_censo.py, g1_censo.log y g1_censo.json.

## 6. NO MEDIDO

- La prueba misma: el cruce de Y con M no se calculó.
- Márgenes de potencia y cobertura de los intervalos: dependen de la calibración sintética.
- Geometría y neuropilo: la homofilia espacial sólo la cubre el control con excitatorias.
- Las huellas de BANC contra un pin: quedaron registradas, no cotejadas.
- El exit code del censo: corrió en segundo plano y no quedó registrado.
- El inventario de máquinas: no lo reabrí hoy; se re-mide al armar el workflow.
- La mosca, y la parte funcional (G1-F).

## Estado vigente que CONTEXTO todavía no refleja

Suma a lo de la 012. CONTEXTO sigue en la 2026-11-03-002; partirlo espera a Abraham.

- **G1:** arrancado. Diseño de G1-A con definiciones, modelos, nulo, lectura y controles fijados en este commit, antes de cruzar Y con M. Falta calibración, sello y corrida.
- **Decisión que espera a Abraham:** ninguna nueva para seguir; siguen abiertas cerrar T1 de 009-A1, la sección 15 del Doc maestro y partir CONTEXTO.

## QA (PROMETEO-QA, tipo «ADR o reporte»)

| Criterio | Puntos | Evidencia |
|---|---|---|
| Completitud | 14/15 | definiciones, modelos, nulo, lectura, secundarias, calibración y censo en las dos moscas; −1 porque los márgenes de potencia dependen de la calibración |
| Arquitectura del razonamiento | 9/10 | G1 anidado en G0 con un parámetro, mismo lado dentro de G0, controles de dosis y de signo, criterio que puede refutar; −1 porque la geometría no entra |
| Documentación | 9/10 | respuesta, Doc y evidencia verbatim; −1 porque CONTEXTO sigue atrasado |
| Innovación | 4/5 | BANC recortado al cerebro por medición, criterio de refutación por intervalo y semilla de G1-F; −1, el instrumento todavía no existe |
| Proceso QA | 5/5 | 996 y 753 iguales a H_REUSO; md5 igual al PIN; signo de los drivers medido (0 de 29 inhibitorios); verificación post-push |
| **Total** | **41/45 → 91/100** | N/A: 55 puntos (Ejecutabilidad, Seguridad, Testing y DevOps), porque se entrega un diseño y un censo, no el instrumento de prueba |

```plain
--- METODO PROMETEO ---
Accion delicada: NO (diseño y censo; evidencia append-only)
Modo aplicado:   FULL
Maquina:         brain-env (host 6c09d8604b07, Python 3.12.14, NumPy 2.5.3, pandas 3.0.5, pyarrow 25.0.1)
Rubrica:         41/45 -> 91/100 (ADR o reporte)
N/A declarados:  55 (Ejecutabilidad, Seguridad, Testing, DevOps: no se entrega el instrumento de prueba)
Review externo:  no pedido (deuda)
Instrumento:     g1_censo.py en brain-env, FIN a los 47,4 s; salida cruda en docs/agents/evidencia/2026-11-04-001-g1-censo/
Artefactos:      docs/agents/respuestas/2026-11-04-001-g1-arrancado-diseno-g1a-y-censo.md
                 + https://app.clickup.com/90171457413/docs/2kza6fw5-26157/2kza6fw5-29817
```
