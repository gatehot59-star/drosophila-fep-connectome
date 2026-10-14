# SELLO · H_FRENO: qué frena el giro de DNp06 ante el looming frontal (respuesta 2026-10-14-023)

**Pedido.** Abraham, 14-oct 19:57, ClickKit `sellar_frena_giro_022`: «Sellá qué frena el giro en la mosca».

## Por qué
H_TOPO_FIEL salió REFUTADA en brain-env (2026-10-14-022). Sin la resta contralateral, un looming de frente enciende las dos DNp06 y la mosca gira en vez de aterrizar. La resta no tiene vía directa en FlyWire v783 (2026-10-14-020). Si la mosca frena ese giro con algo cableado, tiene que verse como entrada **inhibitoria** sobre DNp06.

## Orden del sello (verificable en git)
| Paso | Commit | Qué | md5 |
|---|---|---|---|
| A | `d59913c` | Instrumento, prueba y workflows, antes de mirar DNp06 | `freno_mosca.py` 1318fefb8dbac3ce56bc56c9a439ea26; `prueba_freno.py` 9b095a1534f9a3ef6f4906e75d570a1d; `freno-mosca.yml` 45f988be173857944875a84e929c90e0; `freno-humo.yml` 341b9e421c2faaeca13f694be3bd913d |

## Mecanismos pre-registrados (no son excluyentes)
| Mecanismo | Qué es |
|---|---|
| M1_DNP07 | DNp07, el comando de aterrizaje, inhibe directo a DNp06 |
| M1_DNP01 | DNp01, el comando de despegue, inhibe directo a DNp06 |
| M2_OPUESTA | Inhibición mutua directa entre la DNp06 izquierda y la derecha |
| M3_CONTRA | Interneurona inhibitoria alimentada por LPLC1 y LPLC2 del otro lado: la resta, a dos saltos |
| M4_LPLC4 | Interneurona inhibitoria alimentada por LPLC4, el detector de aterrizaje |
| M5_DNP07 | Interneurona inhibitoria alimentada por DNp07 |
| M6_BILATERAL | Interneurona inhibitoria alimentada por LPLC2 o LC4 de los dos lados: un detector de frente |

A dos saltos, la interneurona tiene que recibir al menos 5 sinapsis de la fuente.

## Métrica y veredictos
- **Cuota:** sinapsis inhibitorias por el mecanismo sobre las sinapsis inhibitorias totales de DNp06, por lado.
- **Percentil:** contra las otras unidades descendentes del mismo lado (tipo y lado, con al menos 100 sinapsis inhibitorias de entrada), sin contar el objetivo.
- **A dos saltos:**
  - CANDIDATO si la cuota es al menos 0,05 y el percentil al menos 0,90, en los dos lados.
  - DESCARTADO si en los dos lados la cuota es menor que 0,05 o el percentil menor que 0,50.
  - Si no, DUDOSO.
- **Directos:** PRESENTE con al menos 5 sinapsis inhibitorias en los dos lados; AUSENTE si hay menos de 5 en los dos; si no, ASIMETRICO.
- **H_FRENO:**
  - SOSTENIDA si algún mecanismo es CANDIDATO o PRESENTE.
  - REFUTADA si todos son DESCARTADO o AUSENTE.
  - Si no, SIN_DECIDIR.
  - Son 7 mecanismos sin corrección por multiplicidad: un CANDIDATO es un candidato, no una prueba.
- **Control positivo:** la cuota excitatoria directa desde LPLC1 y LPLC2 del mismo lado tiene que dar percentil de al menos 0,90 en los dos lados. Si falla, el resultado es INVALIDO.
- **Signo:** la columna Excitatory del parquet, con la convención de Shiu (GABA y glutamato cuentan como inhibitorios). Descriptivo: GABA y glutamato por separado, y los 10 tipos inhibitorios que más le dan a DNp06, con sus entradas.
- **Lo que no puede ver:** vías a más de dos saltos, inhibición aguas abajo de DNp06 (en el cordón nervioso) y dinámica.

## Prueba
- `prueba_freno.py` da 6/6 en brain-env y desde un clon limpio. Usa grafos de juguete que cubren CANDIDATO, DESCARTADO, ASIMETRICO, AUSENTE, REFUTADA, INVALIDO y objetivo inexistente.
- **Puede dar rojo, y dio rojo:** la primera versión contaba al objetivo dentro de su propia referencia, y E1_CUOTA_EXACTA falló (percentil 0,957 en vez de 1,0). Se corrigió antes de cualquier corrida con datos reales.

## Humo (DNp06 ciega)
- brain-env, 20:03, **con objetivo DNp01** (DNp06 no se miró). Log `results/frena_giro_2026-10-14_humo/brain-env-humo.log`, md5 f8aa6f3b4de134c84e2d143ff5eb3d2a; JSON 8e5edf17e84b7453f0dea4507b2af399; 17,6 s.
- El control positivo PASA (percentil 0,993 y 0,995) y hay 927 unidades descendentes de referencia.
- **Declarado:** miré los números de DNp01. Lo único que toqué después fue el texto del SELLO; el instrumento no cambió.
- **Letra chica que vi en el humo:** con el umbral de 5 sinapsis, los conjuntos X de M3 y M4 son grandes (917 a 1.366 neuronas), así que la cuota de base es alta y el que discrimina es el percentil. Lo dejo como está, sellado.
- **Actions x64:** se dispara con `results/frena_giro_2026-10-14_humo/HUMO`, en este mismo commit.

## Disparo
La corrida con DNp06 (segundos, un solo trabajo) **solo** se dispara al pushear `results/frena_giro_2026-10-14/CORRER`, con el sí de Abraham.
