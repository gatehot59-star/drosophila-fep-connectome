# 2026-10-14-028 · La misma plantilla en distintas acciones: hay un primer indicio, BANC sirve de puente y la prueba se puede sellar

## Pedido
Abraham, 14-oct 21:14: «creo que comparando banc con los otros dos conectomas podremos obtener más que solo el reflejo. Podemos descifrar más de la mosca, y creo que hay mucho que solo es lo mismo aplicado de distintas formas para distintas acciones».

## Veredicto primero
- [CONCLUSIÓN] **La idea es buena, y es la más fuerte que tiene el proyecto para el Paper 3.** Comparar animales separa lo que es de la mosca de lo que es de un individuo, y «lo mismo aplicado distinto» es una hipótesis que se puede falsar.
- [MEDIDO, descriptivo] **Ya hay un primer indicio, de los logs de la 023 y la 024.** LHAD1g1 (GABA) y PVLP010 (glutamato) están entre las inhibitorias mayores de DNp01, el comando de despegue: juntas le dan el 10,9 % y el 10,5 % de su inhibición. Y son las dos mayores de DNp06, el comando de giro: 20,1 % y 18,7 %. El mismo módulo de inhibición de avance les sirve a dos acciones distintas.
- [MEDIDO] **BANC 888 hace de piedra Rosetta.** Trae pareja de tipo con FlyWire para 64.789 neuronas, con MANC para 24.277 y con hemibrain para 6.768. Es el único de los cuatro que tiene cerebro y cordón en el mismo animal.
- [NO MEDIDO] MANC y hemibrain no están bajados; en brain-env hay FlyWire v783 y BANC 888.

## Dónde ayuda y dónde engaña
- **Ayuda:** lo que se repite en dos animales distintos no es ruido de un individuo. Ya lo vimos en la 2026-10-14-002: el 92,4 % de las conexiones de R2 con 20 sinapsis o más está en BANC, contra el 28,9 % de las de 1 a 4. Falta el nulo de parejas al azar.
- **Engaña si no se sella antes:** buscando motivos se encuentran motivos. La plantilla, el umbral y el nulo se escriben antes de mirar; si no, es pareidolia.
- **Los cruces tienen límites:**
  - El cordón solo se compara entre BANC (hembra) y MANC (macho), así que el sexo se mezcla con el animal.
  - Hemibrain es medio cerebro.
  - Las parejas de tipo no cubren todo: en la 002, el 51,6 % de las entradas de nuestras descendentes tenía pareja por `fafb_match`.
- **Tres animales no son una población.** Se puede decir «se conserva en 2 de 2» o «en 3 de 3», no hacer estadística entre animales.

## La prueba que propongo: H_REUSO (sin sellar)
- **Plantilla, escrita antes de mirar:**
  - un sensor S excita a una descendente D de su mismo lado;
  - el mismo S excita a una inhibitoria X;
  - X inhibe a esa misma D.
  - Umbrales fijos; el signo, con la convención de siempre.
- **Qué se cuenta:** en cuántos pares sensor-descendente del cerebro aparece la plantilla, y cuántas X se comparten entre descendentes de acciones distintas. Contra los nulos SL, que conservan grados y lados.
- **Dónde:** primero en FlyWire y después otra vez en BANC, con las parejas de tipo.
- **Falsador:** no supera al nulo, o no se replica en BANC.
- **Para Topo, v0.3 con plantillas:** si el repertorio de escape, aterrizaje y giro se escribe con pocas plantillas con parámetros, cuánto se comprime es la medida del reuso.

## Orden que recomiendo
1. H_COMPARADOR en BANC, que ya está pensado y le da el falsador a Topo v0.2.
2. H_REUSO en FlyWire y BANC.
3. Bajar MANC solo si H_REUSO pasa y hace falta el cordón de otro animal.

Sin descuidar el Paper 2: falta el token de Zenodo.

## Herramientas y máquina
- brain-env: lectura de `banc_888_meta.feather` (columnas y cuentas de parejas) y aritmética sobre los logs ya commiteados de la 023 (humo, DNp01) y la 024 (DNp06).
- Sin código nuevo ni corridas nuevas.
- Acción delicada: ninguna.

## Archivos
| Archivo | md5 |
|---|---|
| `tools/contexto/actualizar_contexto_2026-10-14-028.py` | 2823da8dfd0bfc906c631f0dc9b1edf8 |
| Fuente del indicio: `results/frena_giro_2026-10-14_humo/brain-env-humo.log` (DNp01) | f8aa6f3b4de134c84e2d143ff5eb3d2a |
| Fuente del indicio: `results/frena_giro_2026-10-14_brainenv/freno.log` (DNp06) | c474e1f3f360a0cf84d398375aa4c698 |

## NO MEDIDO
- H_REUSO y H_COMPARADOR.
- Si LHAD1g1 y PVLP010 inhiben a DNp01 del mismo lado, como a DNp06.
- Si el módulo compartido se conserva en BANC.
- MANC y hemibrain.

## Antes de firmar
| Afirmación | Fuente | Fuerza |
|---|---|---|
| LHAD1g1 y PVLP010 inhiben a DNp01 y a DNp06 | logs de la 023 y la 024 | Medido, descriptivo, post hoc; dos descendentes, no un patrón |
| BANC tiene parejas con FlyWire, MANC y hemibrain | meta de BANC 888 | Medido: cuentas de columnas no vacías |
| Hay reuso de plantillas | ninguna | CONCLUSIÓN posible; la decide H_REUSO |

--- METODO PROMETEO ---
Investigar antes de opinar: qué conectomas hay de verdad en la máquina y qué parejas trae BANC. Distinguir el indicio de la prueba. Proponer el falsador antes de buscar.
