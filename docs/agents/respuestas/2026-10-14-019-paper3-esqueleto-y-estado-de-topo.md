# 2026-10-14-019 · Dónde quedaron el Paper 3 y el lenguaje de grafo: el esqueleto del Paper 3 no existía y ya está; Topo v0 existe y pasó su primera prueba, pero la parte de grafo no está hecha

**Pedido:** «¿Y dónde quedó el Paper 3, que ibas a armar el esqueleto, y el lenguaje de grafo, que es lo que creí que hacíamos?» (Abraham, 14-oct 17:39).

## Veredicto primero
- [CONCLUSIÓN] **Tenés razón: el esqueleto del Paper 3 no estaba hecho.** Quedó decidido en la 006 (12:19) y lo anoté como NO MEDIDO («El Paper 3 no tiene esqueleto»), pero nunca te lo puse como opción en los botones; después de la 015 seguí con H_DEBILES. Error mío de prioridad.
- [HECHO] **Esqueleto del Paper 3 armado:** `docs/paper3/paper3-esqueleto.md` en la rama `titan/paper3-esqueleto-2026-10-14` (`5b2e5ee`), sin PR. Una sola pregunta: qué clases de neuronas alimentan cada salida del cerebro (descendentes, motoras y neurosecretoras) más allá de lo que explican el tamaño, la ubicación y la cantidad de pruebas.
- [MEDIDO] **Cotejo:** los 106 números del esqueleto están escritos en las respuestas de git que cita cada sección (`tools/paper3/cotejar_paper3.py`, PASA). Con dos números cambiados a propósito, marca los dos (control negativo PASA). Reproducido desde un clon limpio.
- [CONCLUSIÓN] **El resultado del Paper 3, en criollo:** a primera vista el cerebro central manda todas las salidas, pero casi todo era tamaño y ubicación. Lo que aguanta los tres nulos y todas las correcciones son cinco cosas: las descendentes mandan a otras descendentes, a las motoras, al cuello y a la antena, y lo óptico casi no llega a las descendentes. El escape visual es el ejemplo: la vista no tiene atajo a los músculos, tiene que pasar por las descendentes.
- [MEDIDO] **El lenguaje de grafo es Topo (2026-10-14-011).** Un reflejo se escribe como flechas (tipo de sensor × lado × signo → comando) y corre como regla o sobre el cableado real. Pasó sus tres pruebas (12 de 12 exacto contra la regla, control negativo, reproduce M46) y su primera prueba real (H_TOPO_NUEVO SOSTENIDA, 2026-10-14-015), con letra chica: el programa nuevo de aterrizaje pierde contra la regla vieja en 5 de 6 celdas.
- [NO HECHO] **La parte de grafo propiamente dicha** (paso 2 de la 2026-10-14-013): dibujar cada programa como grafo y chequear cada flecha contra el conectoma, por ejemplo marcar que LPLC1 no tiene sinapsis directas sobre DNp07 (2026-10-12-014). Tampoco la v2 del programa de la barra. Es lo próximo que propongo.

## Herramientas y máquina
- brain-env: escritura del esqueleto y del cotejo, corridas del cotejo y del control negativo, md5 y verificación desde clon limpio.
- GitHub: rama nueva y push; estado del PR #26 por la API pública (abierto, sin merge, head `95e8d6c`).
- Lectura: respuestas 2026-10-10-005 a 009, 2026-08-24-060, 2026-10-02-004, 2026-10-11-005, 2026-10-11-007 y 2026-10-14-006, 007, 009, 011, 013 y 015.
- Acción delicada: ninguna (rama nueva sin PR).

## Evidencia
```
COTEJO numeros=106 en_su_fuente=106 faltan=0 fuentes_sin_archivo=0
COTEJO_PAPER3 -> PASA
FALTA linea=57 numero=61.23 fuentes=2026-10-10-005
FALTA linea=82 numero=265.3 fuentes=2026-08-24-060,2026-10-11-007,2026-10-10-005
CONTROL_NEGATIVO cambios=2 marcados=2 -> PASA
```

## Archivos
| archivo | md5 |
|---|---|
| docs/paper3/paper3-esqueleto.md | d939bd8d36e7bb000e51fa7cd4523cf8 |
| tools/paper3/cotejar_paper3.py | 7ffbffd509abbc1d52cab457ed76b1ca |
| docs/paper3/cotejo-2026-10-14.log | e16216e73e1f2af91233cb504eb5f62c |

## Lo que encontré al armarlo (para decidir)
- **Discrepancia en LC6 a GF:** un nulo esperaba 5,8 aristas (2026-08-24-060) y otro 17,2 ± 3,1 (2026-10-11-007). Hay que fijar cuál y por qué antes de escribir.
- **El cero de LC6 a GF puede ser geometría** (un glomérulo que no toca las dendritas de la GF): se escribe «ausencia de vía», no «exclusión activa» (2026-08-24-060).
- **El código de la 005 a la 009 vive en el PR #26**, abierto y sin review.
- **sel_post es dinámica, no estructura**, y no tiene el barrido hecho: recomiendo apéndice o afuera.
- **Lo que más le suma:** repetir el mapa de salidas en BANC v888, que ya está bajado.

## NO MEDIDO
- La réplica en BANC, la literatura del hueco y el solapamiento de LC6 con la GF.
- El cotejo prueba que cada número está en su fuente, no que la frase que lo rodea diga lo mismo.
- Topo: el grafo chequeado contra el conectoma, la salida a C99/Q15, la escala y BANC.

## Antes de firmar
| afirmación | instrumento | ¿podía dar rojo? |
|---|---|---|
| los números del esqueleto salen de git | cotejar_paper3.py | sí: con dos números cambiados da dos faltantes |
| el esqueleto en git es el cotejado | md5 desde clon limpio y cotejo re-corrido ahí | sí |
| el PR #26 sigue abierto | API pública de GitHub | sí |
| la vista pasa por las descendentes | 005 (óptico 0,00 % de las motoras) y 060 (GF a motoras, 0 aristas) | sí; es conclusión sobre dos mediciones |
| Topo pasó su primera prueba | agregado sellado de H_TOPO_NUEVO (bot `46929db`) | sí |

--- METODO PROMETEO ---
Inventario: brain-env y GitHub; sin corridas de experimento. brain-env sigue con los reales de H_DEBILES (en Actions ya dieron exacto, 2026-10-14-017). Contexto vivo: CONTEXTO md5 20fb2b11 (bot 0ede17f).
