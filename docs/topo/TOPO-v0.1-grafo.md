# Topo v0.1: el programa como grafo, chequeado contra el conectoma (2026-10-14-020)

Pedido: ClickKit `topo_y_debiles_019` (Abraham, 14-oct 17:53), «Topo v0.1 + H_DEBILES de fondo». Es el paso 2 de la hoja de ruta de la 2026-10-14-013: un compilador que revise el programa contra el conectoma.

## Qué agrega a v0
`topo.py` (md5 `9abefe9d`) no cambia: `tools/topo/topo_grafo.py` lo importa y se niega a correr si el md5 no es el sellado.

1. **El grafo.** Cada programa se dibuja solo, en Mermaid (GitHub lo dibuja): sensores por lado, líneas (las descendentes) y acciones, con el signo y el peso que el programa le da a cada flecha.
2. **El chequeo.** Cada flecha sensor@lado a descendente@lado se busca en FlyWire v783: sinapsis directas de todas las neuronas de ese tipo y lado, su signo real (fracción excitatoria por neurotransmisor) e intermediarias a dos saltos (5 o más sinapsis en cada tramo). Veredictos:
   - CABLEADA: hay sinapsis directas y el signo coincide con el del programa.
   - SIGNO_CONTRARIO: hay sinapsis directas con el signo opuesto.
   - SIN_VIA_DIRECTA: cero sinapsis directas; esa cuenta la hace la regla, no la mosca.
   - TIPO_INEXISTENTE: el tipo no tiene neuronas de ese lado.
   - SIN_BLANCO: la línea no nombra una descendente; no se chequea.

## Uso
```
python3 tools/topo/topo_grafo.py tools/topo/escape.topo
python3 tools/topo/topo_grafo.py tools/topo/escape.topo --conn connectivity.parquet --annot annotations.tsv --md docs/topo/grafos/escape.md
python3 tools/topo/prueba_grafo.py --conn connectivity.parquet --annot annotations.tsv
```

## Pruebas (brain-env, insumos pineados 3d802fd5 y 719904ab): VEREDICTO_GRAFO PASA 5/5
- ESTRUCTURA: 14 flechas en el escape, 16 en el aterrizaje por dirección; una arista de Mermaid por flecha y por línea.
- REPRODUCE_014: los seis totales por tipo sobre cada descendente son exactos los de la 2026-10-12-014 (por ejemplo LPLC2 a DNp01, 1.080 sinapsis de 189 neuronas; LPLC1 a DNp07, 0).
- PUEDE_DAR_ROJO: LPLC1 a DNp07 da SIN_VIA_DIRECTA de los dos lados y LC4 a DNp01 da CABLEADA.
- SIGNO_CONTRARIO: restar LC4 en DNp01 (una vía excitatoria) da SIGNO_CONTRARIO.
- TIPO_INEXISTENTE: un tipo inventado no rompe el chequeo.

## Lo que mostró (descriptivo, post hoc, no decide nada)
- **Escape:** 10 de 14 flechas cableadas; todas las que suman tienen sinapsis directas y son 100 % excitatorias. Las 4 que restan (el lado contrario sobre DNp06, para girar) no tienen vía directa, y a dos saltos esa vía es casi toda excitatoria (0 a 5 % inhibitoria en el segundo tramo): la mosca no resta ahí; la resta la hace la regla.
- **Aterrizaje por dirección:** la única flecha nueva del programa (restar LPLC1 en DNp07) no tiene vía directa (a dos saltos, 2 y 4 intermediarias con 55 y 114 sinapsis). Es el programa que perdió contra la regla vieja en 5 de 6 celdas (2026-10-14-015). Coincidencia, no causa probada.

## Lo que no dice
- SIN_VIA_DIRECTA no dice que la cuenta esté mal: la regla puede rendir mejor que la mosca.
- A dos saltos solo mira el signo del segundo tramo y un umbral de 5 sinapsis.
- El signo es la predicción por neurotransmisor del parquet, no fisiología.

## Lo que sigue (hoja de ruta de la 2026-10-14-013)
3. Sensores reales y salida a C99/Q15 (H_TOPO_C99). 4. Recortes grandes y BANC (H_TOPO_ESCALA). 5. Estados explícitos.
