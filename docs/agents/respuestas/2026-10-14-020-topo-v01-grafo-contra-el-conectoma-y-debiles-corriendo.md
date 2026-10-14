# 2026-10-14-020 · Topo v0.1: cada programa se dibuja como grafo y cada flecha se chequea contra la mosca; H_DEBILES corriendo de fondo

**Pedido:** ClickKit `topo_y_debiles_019` (Abraham, 14-oct 17:53), «Topo v0.1 + H_DEBILES de fondo».

## Veredicto primero
- [HECHO] **H_DEBILES corriendo:** `results/debiles_2026-10-14/CORRER` en `84e225c` (rama `titan/debiles-2026-10-14`), run 38635900391 de Actions desde las 17:53, 64 trabajos; se estiman unas 3 h. Nada sellado cambió.
- [MEDIDO] **Segunda máquina:** los reales completos también dieron exacto en brain-env (R2 0,9465, núcleo 0,9135, REAL_R2_IGUAL y REAL_NUCLEO_IGUAL True, 2.911 s), igual que en Actions (2026-10-14-017).
- [HECHO] **Topo v0.1, el lenguaje de grafo:** rama `titan/topo-grafo-2026-10-14` (`3d7010a`), desde la rama de la barra. `tools/topo/topo_grafo.py` dibuja cada programa como grafo (Mermaid, GitHub lo dibuja) y chequea cada flecha contra FlyWire v783: sinapsis directas, signo real e intermediarias a dos saltos. Veredictos: CABLEADA, SIGNO_CONTRARIO, SIN_VIA_DIRECTA, TIPO_INEXISTENTE, SIN_BLANCO. `topo.py` no cambió (md5 `9abefe9d`, la herramienta se niega a correr si cambia).
- [MEDIDO] **Pruebas 5 de 5** (`tools/topo/prueba_grafo.py`), en brain-env y otra vez desde un clon limpio: ESTRUCTURA; REPRODUCE_014 (los seis totales por tipo sobre cada descendente, exactos los de la 2026-10-12-014); PUEDE_DAR_ROJO (LPLC1 a DNp07 da rojo, LC4 a DNp01 da verde); SIGNO_CONTRARIO; TIPO_INEXISTENTE. Los dos grafos regenerados desde git dan el mismo md5.
- [MEDIDO, descriptivo] **Escape:** las 10 flechas que suman están cableadas (374 a 810 sinapsis cada una, 100 % excitatorias). Las 4 que restan (el lado contrario sobre DNp06, para girar) no tienen vía directa; a dos saltos son 5 a 7 intermediarias con 0 a 5 % de entrada inhibitoria: la mosca no resta ahí, la resta la hace la regla.
- [MEDIDO, descriptivo] **Aterrizaje por dirección:** la única flecha nueva del programa, restar LPLC1 en DNp07, no tiene vía directa de ningún lado (a dos saltos, 2 y 4 intermediarias). Es el programa que perdió contra la regla vieja en 5 de 6 celdas (2026-10-14-015). [CONCLUSIÓN] Coincide, pero no prueba que esa sea la causa.

## Herramientas y máquina
- brain-env (Python 3.12.14, numpy 2.5.3) con los insumos pineados (3d802fd5, 719904ab): escritura, corridas, pruebas y verificación desde clon limpio.
- GitHub: dos ramas (`CORRER` en la de débiles, rama nueva para Topo); estado del run por la API pública.
- Acción delicada: disparar H_DEBILES, pedido explícito de Abraham.

## Evidencia
```
PRUEBA ESTRUCTURA escape=14 aterrizaje=16 mermaid=20/22 -> PASA
PRUEBA REPRODUCE_014 6 pares, iguales=6 -> PASA
PRUEBA PUEDE_DAR_ROJO SIN_VIA_DIRECTA SIN_VIA_DIRECTA CABLEADA -> PASA
PRUEBA SIGNO_CONTRARIO SIGNO_CONTRARIO -> PASA
PRUEBA TIPO_INEXISTENTE TIPO_INEXISTENTE -> PASA
VEREDICTO_GRAFO PASA 5/5
CHEQUEO escape CABLEADA=10 SIN_VIA_DIRECTA=4
CHEQUEO aterrizaje_dir CABLEADA=10 SIN_VIA_DIRECTA=6
REAL R2=0.9465 nucleo=0.9135 | 2911.1 s   (brain-env)
```

## Archivos (md5 desde clon limpio)
| archivo | md5 |
|---|---|
| tools/topo/topo_grafo.py | 0ea687824a45456e0a02b0b197f57a8a |
| tools/topo/prueba_grafo.py | 2e8042df69a8933a492ca53179e9bbae |
| docs/topo/grafos/escape.md | bd4e8073dc3303600a13fa6ba2d44455 |
| docs/topo/grafos/aterrizaje_dir.md | 5fbbf08f6522bc7f40252a758eb5308b |
| docs/topo/grafo-2026-10-14.log | ff36b60ea99fab65ee91e7b5708804bc |
| docs/topo/TOPO-v0.1-grafo.md | (en la rama) |
| tools/topo/topo.py (sin cambios) | 9abefe9d620e9f94f4a68ed75108d6be |

## NO MEDIDO
- H_DEBILES: corriendo, sin resultado.
- Que la falta de la flecha LPLC1 a DNp07 explique la derrota del programa nuevo.
- SIN_VIA_DIRECTA no dice que la cuenta esté mal: la regla puede rendir mejor que la mosca.
- A dos saltos mira solo el signo del segundo tramo y un umbral de 5 sinapsis; el signo es la predicción por neurotransmisor.
- Los pasos 3 a 5 de Topo (C99/Q15, escala y BANC, estados).

## Nota de numeración
Otra instancia (línea REA) usó también el número 2026-10-14-019 en esta carpeta (`2026-10-14-019-rea-binario-ajeno-64bits-en-jaula.md`). Las dos 019 se distinguen por el nombre; la de esta línea es `2026-10-14-019-paper3-esqueleto-y-estado-de-topo.md`.

## Antes de firmar
| afirmación | instrumento | ¿podía dar rojo? |
|---|---|---|
| el chequeo cuenta bien | REPRODUCE_014 contra totales medidos antes por otro script | sí: un total distinto la tumba |
| el chequeo puede marcar ausencias | PUEDE_DAR_ROJO sobre LPLC1 a DNp07 | sí, y también tiene que dar verde en LC4 a DNp01 |
| detecta signos opuestos | SIGNO_CONTRARIO con un programa alterado | sí |
| git tiene lo probado | md5 y re-corrida desde clon limpio | sí |
| H_DEBILES arrancó | API pública: 64 trabajos, en curso | sí |

--- METODO PROMETEO ---
Inventario: brain-env y Actions. Contexto vivo: CONTEXTO md5 311ff360 (bot 87eb942); main en 97951bb (commit de otra instancia, sin tocar el CONTEXTO).
