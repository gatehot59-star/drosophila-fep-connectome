# 2026-10-14-043 · Paper 3 empujado: la discrepancia de LC6 a GF eran dos nulos, la tabla ya estaba publicada y el aporte es la expectativa

**Fecha:** 2026-10-15, 22:22 (America/Buenos_Aires) · **Método:** PROMETEO

## Pedido

Abraham, ClickKit `empujar_paper3_043`, 15-oct 22:08: «Empujá el Paper 3 mientras corre la réplica».

## Veredicto primero

- [MEDIDO] La discrepancia del nulo de LC6 a GF (5,8 contra 17,2 esperadas) no es un error: son dos nulos distintos. La 2026-08-24-060 usa el nulo CP, que baraja destinos dentro de bloques de `super_class` (la 060 lo dice en su línea 61): 5,8 esperadas. La 2026-08-25-065 usa un nulo que preserva neuropilo (`src/escape_neuropil_null.py`, md5 `c04ddd4282ada4f9df462f87d84d85ba`, rama `titan/twohop-nulls`): 17,2 ± 3,1, z −5,61, y la mínima de 40 realizaciones da 12. Encerrar el barajado en el neuropilo que LC6 y la GF comparten sube la expectativa, así que el segundo es la prueba más dura. El esqueleto ahora la pone primero y deja el CP como filtro.
- [MEDIDO, 065] La geometría a escala de neuropilo ya estaba medida: el neuropilo dominante de salida de LC6 es PVLP (68.082 sitios) y el de entrada de la GF también (4.085 sitios). LC6 comparte 5.335 sitios con la GF, más que LC4 (4.523), que hace 104 aristas. El cero de LC6 no lo explica la ubicación; el de LPLC1 a la GF sí (su nulo espera 0,2).
- [CONCLUSIÓN, 066 y 067] Los conteos no son hallazgo. Kind et al. 2024 (bioRxiv, eLife Reviewed Preprint 99277) y el Cell Type Explorer de FAFB ya publican la matriz de las proyecciones visuales a las descendentes, sin LC6 a DNp01 (que es la GF). El aporte del §3.5 es la expectativa contra la que se compara el conteo. Eso estaba en git desde el 25-ago y el esqueleto del 14-oct no lo decía: corregido.
- [MEDIDO] Esqueleto cotejado en Actions: 127 de 127 números en su fuente (antes 106) y el control negativo marca 2 de 2 cambios. Commit del bot `7f8b331` (22:16), verificado desde un clon fresco.
- [PENDIENTE] El vínculo con el Paper 2 en la Discusión usa H_LECTOR de Actions (D1 −0,0029, D2 +0,0474, de la 2026-10-14-038) y queda marcado hasta leer el cotejo de la réplica en brain-env.
- [NO MEDIDO] Distancia entre árboles (glomérulo de LC6 contra dendritas de la GF), pureza de los bloques del nulo de neuropilo, ese nulo con umbral de sinapsis y con la DNp09 de 4 neuronas. La 060 da LPLC2 a DNp09 = 170 y la 065 da 32 porque usan definiciones distintas de DNp09: no se mezclan hasta re-correr.

## Herramientas y máquina

- brain-env (gateway, servicio `build`, `run` y `write_file`, una llamada por vez): lectura de la 060, 065, 066, 067 y 038; edición del esqueleto, prueba del parche en copia (resultado `a904026e`, la segunda aplicación aborta), cotejo y control.
- GitHub: `push_files` a `titan/paper3-esqueleto-2026-10-14` (`333f1ea`, parche y workflow) y a `main` (esta respuesta, el parche del CONTEXTO y su workflow).
- Actions: `paper3-fuentes-2026-10-14-043.yml` trae la 065, 066 y 067 desde `titan/materializacion-h4-guard-2026-10-02` y la 038 desde `main` con `git show`, verifica sus md5 (falla cerrado), aplica el parche, verifica el md5 del esqueleto, coteja, corre el control y se borra en el mismo commit.
- ClickUp: Doc público de la 043.
- Delicado: no. Ningún merge, nada a Zenodo, nada a Kaggle. La réplica de H_LECTOR siguió corriendo en brain-env sin tocarla (empezó 21:55; a las 22:18 las celdas c0 y c1 estaban en la etapa RED).

## Archivos

Rama `titan/paper3-esqueleto-2026-10-14`, head `7f8b331`, verificados desde un clon fresco (`md5sum -c` del MD5SUMS da OK en todo):

| Archivo | md5 |
|---|---|
| `docs/paper3/paper3-esqueleto.md` | `a904026e345d0284b8e0196d6eb767fb` |
| `tools/paper3/editar_esqueleto_2026-10-14-043.py` | `a35a2b93ad207c22ff77efbb1d146f10` |
| `results/paper3_2026-10-15/cotejo.log` | `914dbc49e1ad715cf1b6c0e663a2248e` |
| `results/paper3_2026-10-15/control.log` | `e74c93cbaaa4b915280cd5003f25b3ca` |
| `results/paper3_2026-10-15/MD5SUMS` | `231f3efd38c39abb133cb20c056b73ab` |
| copia de `2026-08-25-065-el-LC6-GF-sobrevive-el-null-anatomico-y-aparece-una-tabla-de-ruteo.md` | `53a81e9dbc23469499ccd55295cf3986` |
| copia de `2026-08-25-066-barrido-de-literatura-la-tabla-de-ruteo-YA-esta-publicada.md` | `f1a0f562379c74b5663d7d2b874190ae` |
| copia de `2026-08-25-067-el-Cell-Type-Explorer-de-FAFB-publica-la-tabla-entera.md` | `09b5a5ad67a6454d0682c8a26638800b` |
| copia de `2026-10-14-038-h-lector-medido.md` | `db387286da41865d99d011d3d94f50ce` |

En `main`: esta respuesta, `tools/contexto/actualizar_contexto_2026-10-14-043.py` y `.github/workflows/contexto-2026-10-14-043.yml` (se borra al aplicarse).

## Qué cambió en el esqueleto

- §1: la revisión de literatura del caso de escape está hecha y cerró una puerta; la del mapa de salidas entero sigue pendiente.
- §2.5: el segundo nulo y la cota de oportunidad (`shared_min_sites`), con sus límites declarados.
- §2.6: dónde vive el nulo de neuropilo y por qué hay copias verbatim de la 065 a la 067.
- §3.5: los dos nulos fijados, geometría a escala de neuropilo, ruteo por canal (LC9 excluido de la GF y 7,6 veces enriquecido hacia DNp09), prior art y NO MEDIDO.
- §4: vínculo con H_LECTOR marcado pendiente; el límite de neuropilo corregido (por neurona, no por sinapsis).
- Checklist: discrepancia cerrada; tres ítems nuevos (distancia entre árboles, re-correr el nulo de neuropilo, cotejo de la réplica de H_LECTOR).

## PR #26

Leído: tiene el código y los logs de la 005 a la 009 del Paper 3, con los controles en PASS en `results/output_control_*`. En esa rama faltan algunas carpetas `results/` que su cuerpo nombra. El merge es decisión de Abraham; mientras no se mergee, el §2.6 apunta a una rama sin review.

## Lo que sigue (recomendación)

1. Decidir el PR #26.
2. Sellar la réplica del mapa de salidas en BANC v888: es lo que más le suma al Paper 3. Es pesada y brain-env está ocupada con la réplica de H_LECTOR, así que iría a Actions.
3. 16-oct 10:00: cotejo de la réplica de H_LECTOR.

## NO MEDIDO

1. Distancia entre árboles de LC6 y la GF.
2. Pureza de los bloques del nulo de neuropilo.
3. Nulo de neuropilo con umbral de 5 sinapsis y con la DNp09 de 4 neuronas.
4. Réplica del mapa de salidas en BANC v888.
5. Revisión de literatura del mapa de salidas entero (§1).
6. Cotejo de la réplica de H_LECTOR (corriendo).

## Antes de firmar

- El cotejo prueba que cada número de 3 o más caracteres está en alguna fuente de su sección, no que la frase diga lo mismo ni que esté en la fuente justa. Lo leí a mano para LC6, LC9, LPLC1, el 170 de la 060 y los números de H_LECTOR.
- Los números de dos cifras (12, 40) no los coteja: los leí en la 065 («la MÍNIMA de las 40 da 12»).
- Que el nulo CP baraja dentro de `super_class` lo verifiqué en la 060, no de memoria.
- Las copias son verbatim: el workflow las sacó de sus ramas con `git show` y verificó los md5 antes de seguir.
- Este instrumento podía dar rojo: el control negativo cambia dos números y el cotejo los marca (2 de 2).
- El parche del esqueleto aborta en una segunda aplicación y no escribe nada si algún reemplazo falla (escribe al final).

--- METODO PROMETEO ---
Rol: implementa. Delicado: no.
Máquinas: brain-env (prueba), Actions (aplicación y cotejo).
Artefactos: esta respuesta, el parche del CONTEXTO y su workflow; en la rama del Paper 3, el parche del esqueleto, el cotejo y su control; Doc de ClickUp de la 043.
