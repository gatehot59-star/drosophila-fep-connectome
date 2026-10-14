# Topo v0 · un lenguaje topológico ejecutable para reflejos

**Respuesta 2026-10-14-011.** Pedido de Abraham, 14-oct 12:47 a 12:48: ClickKit `lenguaje_sellar_010` («Diseñá el lenguaje y su falsador») y «Diseñá el lenguaje topológico ejecutable».

## Idea
Un reflejo se escribe con el vocabulario del conectoma: **tipo de neurona × lado × signo → comando**. El significado está en quién se conecta con quién, no en la geometría: por eso es topológico y no gráfico. El mismo programa tiene dos formas ejecutables:
- **regla**: lee las entradas crudas (media por tipo y lado, umbral por línea, carrera);
- **cableado**: baja el programa a un subgrafo real de FlyWire, con sus neuronas y sus aristas con signo.

La regla a mano es la frase y el cableado es su forma compilada. En el banco empatan: +0,85 puntos, IC90 [+0,08; +1,51] (2026-10-13-010).

## Gramática v0
```
reflejo NOMBRE
tipos T1 T2 ...                      # vocabulario: tipos de celda del conectoma
estados E1 E2 ...                    # contexto (posada, vuelo)
acciones A0 A1 ...                   # A0 = no hacer nada
via TIPO -> BLANCO top N por lado    # cableado: las N de TIPO con más sinapsis sobre BLANCO
salida B1 B2 ...                     # cableado: las descendentes, izquierda y derecha
linea NOMBRE = EXPR en ESTADO -> ACCION
    EXPR    := TERMINO { (+|-) TERMINO }
    TERMINO := [NUMERO *] media(TIPO@LADO, ...)
umbral falsas P sobre A0             # cuantil 1 - P del máximo cuando la respuesta es A0
decide carrera                       # primera línea que cruza; empate, mayor exceso; nadie, A0
```

## El reflejo de escape en Topo (`tools/topo/escape.topo`, 18 renglones útiles)
```
reflejo escape
tipos LC4 LPLC2 LPLC4 LPLC1
estados posada vuelo
acciones nada despegar aterrizar girar_der girar_izq
via LC4   -> DNp01 top 4 por lado
via LPLC2 -> DNp01 top 4 por lado
via LPLC4 -> DNp07 top 4 por lado
via LPLC1 -> DNp06 top 4 por lado
via LPLC2 -> DNp06 top 4 por lado
salida DNp01 DNp07 DNp06
linea DNp01@L = media(LC4@L, LPLC2@L) en posada -> despegar
linea DNp01@R = media(LC4@R, LPLC2@R) en posada -> despegar
linea DNp07@L = media(LPLC4@L) en vuelo -> aterrizar
linea DNp07@R = media(LPLC4@R) en vuelo -> aterrizar
linea DNp06@L = media(LPLC1@L, LPLC2@L) - media(LPLC1@R, LPLC2@R) en vuelo -> girar_der
linea DNp06@R = media(LPLC1@R, LPLC2@R) - media(LPLC1@L, LPLC2@L) en vuelo -> girar_izq
umbral falsas 0.05 sobre nada
decide carrera
```

## Medido hoy (`results/topo_2026-10-14/prueba_topo.log`, desde un clon limpio de esta rama)
| Prueba | Qué compara | Resultado |
|---|---|---|
| F1 EQUIV_REGLA | El backend regla contra la regla sellada: `media` y `lc` de `factorial2_mosca.py` (798a824c), extraídas del archivo por su árbol sintáctico, más `lineas`, `umbrales` y `carrera` de `tarea_mosca.py` (40d64e07). 6 celdas × 2 tamaños (40 y 564 entradas) | **PASA**: 12/12 casos, diferencia de señal 0, de umbral 0, 400/400 decisiones iguales en cada caso |
| F2 CONTROL_NEGATIVO | El aterrizaje leyendo LPLC1 en lugar de LPLC4; tres programas mal escritos | **PASA**: 127/400 decisiones distintas (acierto 0,9075 → 0,6550); los 3 rechazados con mensaje |
| F3 REPRODUCE_M46 | El backend cableado contra `tarea_mosca.construir`, con insumos fijados por md5 (conn 3d802fd5, annot 719904ab) | **PASA**: las mismas 46 neuronas en el mismo orden, 187 aristas, 0 inhibitorias, 1.149 sinapsis (igual que la 2026-10-12-015) |

## Falsadores pre-registrados que faltan (NO MEDIDO)
- **H_TOPO_NUEVO.** Un reflejo nuevo escrito solo en Topo, antes de ver datos y bajado a los dos backends.
  - Se sostiene si (a) su cableado, con la dinámica del banco, le gana a 50 SL y 50 T con Holm < 0,05, y (b) su regla no pierde más de 1 punto contra su cableado (IC90, margen 0,01).
  - Se refuta si falla (a) o (b).
  - Hace falta un generador de estímulos propio para la tarea nueva; el lenguaje no lo trae.
  - Candidatos: «la barra pide aterrizaje» (2026-10-12-014) o LC6→GF.
- **H_TOPO_C99.** La regla compilada a C99 en punto fijo Q15 da las mismas decisiones que el backend numpy en 10.000 ensayos y cabe en un microcontrolador. Costo NO MEDIDO.
- **H_TOPO_ESCALA.** Una sentencia `alcance N saltos` que baje a recortes tipo R1 y R2 y reproduzca su huella exacta.

## Límites de v0
- Una sola forma de decidir (`carrera`) y un solo agregado (`media`). No hay memoria ni estado interno: lo que medimos de memoria no le ganó a lo clásico (2026-10-12-004).
- El backend cableado arma el subgrafo pero no lo simula: la dinámica es la del banco, no del lenguaje.
- El vocabulario son los tipos de FlyWire; para un robot, «tipo» tiene que mapearse a un sensor.

## Encaje
Es candidato a dialecto de la IR semántica y MLIR de Mojo Absoluto, con bajada a SparseLTC o a C99. Lo más cercano que existe es NIR (Pedersen et al., *Nature Communications* 15:8122, 2024), una representación intermedia común para hardware neuromórfico. NIR no toma su vocabulario de un conectoma ni verifica programas contra barajados. La búsqueda fue acotada.
