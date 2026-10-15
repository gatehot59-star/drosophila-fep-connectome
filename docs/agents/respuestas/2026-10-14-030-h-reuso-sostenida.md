# 2026-10-14-030 · H_REUSO SOSTENIDA en FlyWire y otra vez en BANC: la misma pieza inhibitoria sirve a muchas acciones; H_DEBILES dio INVALIDO porque Actions perdió 2 de 60 celdas

## Pedido
Abraham, 14-oct 22:09, ClickKit `correr_reuso_029`: «Correr H_REUSO», tal como quedó sellado en la 2026-10-14-029 (`5ef2a63`).

## Veredicto primero
- [MEDIDO] **H_REUSO -> SOSTENIDA.** Pasa en FlyWire y otra vez en BANC, que es otro animal, otra reconstrucción y otra predicción de neurotransmisor.
- [MEDIDO] **FlyWire.**
  - T1: el 88,35 % de los 996 pares sensor a descendente tiene la plantilla inhibitoria. El nulo da 68,2 % de media y 74,6 % como máximo.
  - T2: 698 inhibitorias hacen la plantilla para dos o más tipos de descendente, contra 128,6 de media y 154 como máximo.
- [MEDIDO] **BANC.**
  - T1: 82,6 % de 753 pares, contra 34,7 % de media y 47,4 % como máximo.
  - T2: 419 inhibitorias, contra 11,0 de media y 23 como máximo.
- [MEDIDO] p = 0,005 en las cuatro pruebas, que es el piso con 200 nulos: ningún barajado llegó al valor real. Holm da 0,0199 en las cuatro, con alfa 0,05.
- [MEDIDO] **Las dos máquinas dan lo mismo.** Actions (bot `f12c95a`) y brain-env (`c74509a`) coinciden en 59 de 59 líneas, sin contar los tiempos.
- [MEDIDO, descriptivo, sin veredicto] 346 tipos de X compartidas en FlyWire y 246 en BANC; **203 aparecen en los dos**.
  - Algunas se repiten en lo más alto de las dos listas: AN_multi_11 (24 y 19 tipos de descendente), AOTU019 (20 y 16), AVLP080 (16 y 14), AVLP016 (18 y 13), PS106 (15 y 13), PVLP015 (16 y 12), CB3587 (16 y 12) y PLP034 (21 y 14).
  - LHAD1g1, la pieza de la 024, sirve a 17 tipos de descendente en FlyWire.
- [CONCLUSIÓN] La idea de Abraham de la 028 («mucho es lo mismo aplicado de distintas formas para distintas acciones») pasa su primera prueba con falsador y se replica en BANC. Hay una inhibitoria que se mete entre el sensor y la descendente, y la misma pieza se reutiliza para muchas descendentes, mucho más de lo que da el azar.
- [NO MEDIDO, es el límite principal] **Contra qué gana.**
  - El nulo SL baraja los destinos entre todas las neuronas del mismo lado. Conserva cuántas sinapsis manda y recibe cada neurona, pero no conserva cuánto le manda cada X a las descendentes como clase.
  - Entonces una parte del exceso puede ser solamente que «hay inhibitorias que hablan con descendentes», y no que la plantilla se arme para cada par.
  - El nulo estricto, que baraja solo entre descendentes las salidas que ya iban a descendentes (y lo mismo con las entradas desde sensores), es el falsador siguiente: H_REUSO_ESTRICTO. Si con ese nulo T2 sigue arriba, el reuso es de la pieza y no de la clase.
- [MEDIDO] **H_DEBILES -> INVALIDO, por infraestructura y no por el instrumento.**
  - Run 38635900391: 63 de 65 trabajos dieron bien.
  - La celda t3c3 murió a los 79 minutos porque «el runner perdió comunicación con el servidor». La celda t8c0 terminó, pero su artefacto no subió («Failed to CreateArtifact … Request timeout»).
  - El agregador vio que faltaban 20 de 600 corridas y frenó la lectura como debía: PLAN_GRILLA False, LECTURA NO_SE_LEE, VEREDICTO_GLOBAL INVALIDO (bot `3bc5432`, `agregado.log` 634e762a).
  - Todos los demás chequeos pasan: los reales exactos (0,9465 y 0,9135), la misma mezcla y el núcleo sellado.
  - Descriptivo de una corrida INVÁLIDA, que no se cita como resultado: las mezclas dan n = 20, media 0,9171 (0,9105 a 0,9280), contra 0,9465 de R2 y 0,9135 del núcleo en la misma celda. No se lee hasta que la corrida sea válida.
  - Falta relanzar t3c3 y t8c0 con los mismos comandos y volver a agregar.

## Herramientas y máquina
- **GitHub.** Push del `CORRER` (`6bec7cf`) y del log de brain-env (`c74509a`), con md5 verificado desde un clon limpio. Estado de los runs y anotaciones de los trabajos por la API pública.
- **Actions.** Run 38664286449 (`reuso-mosca`, x64), 205 s.
- **brain-env.** Linux 4.19, Python 3.12.14, numpy 2.5.3, pandas 3.0.5, 7,8 GB. Clon limpio de `6bec7cf`, nohup, 1266 s (BANC tardó 707 s en cargar, con swap).
- Acción delicada: ninguna. No toqué nada sellado.

## Archivos
| Archivo | md5 |
|---|---|
| `results/reuso_2026-10-14/reuso.log` (rama `titan/reuso-2026-10-14`, bot `f12c95a`) | 6e12152aa771012a1f57f528212515a0 |
| `results/reuso_2026-10-14/reuso.json` | 87a3f437c094c4047c2c73b113f0359d |
| `results/reuso_2026-10-14/prueba.log` (7/7, igual al humo) | 0ca00af277704ee493cf927366d726c7 |
| `results/reuso_2026-10-14_brainenv/brain-env.log` (`c74509a`) | b008f8e9e59780dfb5cf746f407aba13 |
| `tools/reuso/reuso_mosca.py` (sin cambios) | e9a07a7c58d926c00fec9c64cf4eb253 |
| `results/debiles_2026-10-14/agregado.log` (rama `titan/debiles-2026-10-14`, bot `3bc5432`) | 634e762a9258be42c3c07ba06d3a1308 |
| CONTEXTO | se actualiza en un solo parche junto con la 031 y la 032 (`tools/contexto/actualizar_contexto_2026-10-14-032.py`, en main) |

## NO MEDIDO
- H_REUSO_ESTRICTO, con el nulo que conserva la clase del destino.
- Otras plantillas: el comparador izquierda-derecha en el cordón (H_COMPARADOR) y la convergencia bilateral.
- MANC y hemibrain.
- Si los nombres compartidos entre FlyWire y BANC son la misma neurona. Los tipos de BANC salen de `fafb_cell_type`, así que coinciden por construcción en parte; los 203 son descriptivos.
- H_DEBILES: las celdas t3c3 y t8c0, y por lo tanto E1, E2 y su veredicto.

## Antes de firmar
| Afirmación | Instrumento | ¿Podía dar rojo? |
|---|---|---|
| SOSTENIDA en los dos | reuso_mosca.py sellado en `613317d`, sin tocar | Sí: la prueba 7/7 incluye un grafo sin plantilla que da p = 1, y REFUTADA si ninguna p cruda baja de 0,05 |
| Gana al azar | nulo SL con guarda | Sí contra ese nulo. **No** contra un nulo de clase: declarado arriba |
| Las dos máquinas coinciden | cotejar_logs.py | Sí: da DISTINTO con una sola línea cambiada |
| H_DEBILES no se lee | agregador sellado | Sí, y dio rojo: INVALIDO |
| La falla de H_DEBILES es de infraestructura | anotaciones de los dos trabajos | Las dos son de GitHub (runner y artefactos), no del script |

--- METODO PROMETEO ---
Correr solo con el `CORRER` de Abraham y sin tocar lo sellado. Correr en dos máquinas y cotejar línea por línea. Leer el veredicto tal como salió. Decir contra qué nulo gana y cuál falta. Mirar los trabajos caídos antes de dar por bueno un agregado, y no leer descriptivos de una corrida inválida.
