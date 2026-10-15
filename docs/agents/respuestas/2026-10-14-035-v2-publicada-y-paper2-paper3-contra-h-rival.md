# 2026-10-14-035 · La v2 del Paper 1 está publicada (10.5281/zenodo.23393412); contra H_RIVAL, el Paper 2 quedó viejo en tres apuestas y omite un ridge que su propia fuente ya medía, y el Paper 3 casi no se toca

## Pedido
- Abraham, 15-oct 09:41, ClickKit `v2_publicar_asi`: «Publicá la v2 así».
- 09:41: «Auditá Paper 2 y Paper 3 contra H_RIVAL».

## Veredicto primero
- [HECHO] **La v2 está publicada.** `tools/zenodo/depositar_v2.py --publicar 23393412` desde un clon limpio de main (`06872d0`), 09:42: POST publish 202, DOI **10.5281/zenodo.23393412**, registro https://zenodo.org/record/23393412. Un primer intento a las 09:42 no llegó a Zenodo (el `git pull` previo falló y la cadena se cortó).
- [MEDIDO] **Chequeo aparte, sin token:** el registro público da 200, versión 2.0, fecha 2026-10-15, concepto 10.5281/zenodo.19136947; los dos PDF con el md5 sellado (6e849bf2 y 05052e6e); la última versión del concepto es 23393412. Va con el título que incluye «Non-Trivial Temporal Amplification», como eligió Abraham; la Limitación 5 (Tabla 8 no reproducible) va dentro del PDF.
- [SEGURIDAD] El token se usó una tercera vez, como variable de entorno de un proceso; no está en el recibo ni en git. Ya no hace falta: hay que revocarlo.
- [AUDITORÍA] **Paper 2** (`docs/paper2/paper2-esqueleto.md`, rama `titan/paper2-esqueleto-2026-10-14`, `4652c81`, md5 1c2912ff13d1f589514cd0128b0a69ab):
  - **P2-1 FAIL, omisión.** La fuente del banco (2026-10-12-015) ya imprimía `ridge_crudo_entrenado(descriptivo)` de 0,9475 a 0,9875 por celda. El esqueleto no lo nombra: §1 dice que casi nadie prueba contra barajados y regla, y §2.4 lista sólo regla, SL y T. Con H_RIVAL (ridge 0,9894 a 0,9988 contra la mosca 0,9413 a 0,9467), el lector entrenado tiene que entrar en §2.4, §3 y el resumen.
  - **P2-2 FAIL, viejo.** §3.6 tiene H_CONSENSO como pendiente; está REFUTADA (el núcleo pierde 4,59 puntos contra R2). La frase de §4 «If H_CONSENSO holds, this supports a parts factory» se cae. Queda H_CABLEADO_NUCLEO SOSTENIDA.
  - **P2-3 FAIL, viejo.** §3.7 tiene H_TAU como pendiente; está SOSTENIDA (+1,78 sobre la regla), pero H_TAU_JUSTO da +1,19 contra la regla con τ, SIN_DECIDIR. Hay que escribirlos juntos: «supera al diseño» depende de que la regla no tenga perilla.
  - **P2-4 OK.** El slot 4 del resumen («reaches but does not exceed, by the pre-registered margin, an idealised hand rule») vuelve a ser la lectura justa tras H_TAU_JUSTO. Falta un slot para H_RIVAL.
  - **P2-5 sin respaldo.** §4: «Our model of the synapses is what falls short, not the fly». Ninguna corrida separa el modelo de la mosca, y H_RIVAL tampoco. Sacarlo o marcarlo como hipótesis.
  - **P2-6 cambiar.** §4: «The cheapest export may be the hand rule; the bench decides which». En acierto, el banco ya decidió: un ridge sobre las entradas crudas. El costo (tamaño, energía, latencia) es NO MEDIDO; sin él, el cableado no se puede vender como pieza exportable.
  - **P2-7 cambiar.** El título «The connectome as a blueprint» no sobrevive a H_RIVAL y H_CONSENSO. Lo medido: el cableado exacto es necesario (los barajados pierden 19 a 28 puntos) pero no es el mejor lector de sus propias entradas.
  - **P2-8 declarar.** Según §2.1, la mosca lee con umbrales sin entrenar sobre tres líneas; ridge y MLP entrenan un lector sobre las 564 entradas. Es lo sellado y la pregunta justa para un producto, pero el texto tiene que decirlo. Pregunta siguiente, NO MEDIDA: la mosca con lector entrenado sobre sus descendentes.
- [AUDITORÍA] **Paper 3** (`docs/paper3/paper3-esqueleto.md`, rama `titan/paper3-esqueleto-2026-10-14`, `5b2e5ee`, md5 d939bd8d36e7bb000e51fa7cd4523cf8):
  - **P3-1 sin impacto.** La pregunta es estructural (quién alimenta cada salida, contra nulos de tamaño y región); H_RIVAL mide lectores. Ningún número de §3.1 a §3.4 cambia.
  - **P3-2 acotar.** §3.5 «vision has to pass through descending neurons» sigue en pie como estructura, pero no puede leerse como «el embudo es el mejor lugar para leer la visión»: un lector entrenado sobre las 564 entradas sensoriales, que se saltea el embudo, acierta 5 puntos más que la mosca. Una frase en §3.5 o §4.
  - **P3-3 cambiar.** §4 enlaza con el banco del Paper 2 «that reads exactly these descending neurons»: citar el resultado completo, con H_RIVAL.
  - **P3-4 pendientes propios**, no de H_RIVAL: el PR #26 sin mergear, la discrepancia de LC6 a GF (5,8 contra 17,2 esperadas) y la réplica en BANC.
- [CONCLUSIÓN] El Paper 2 hay que repensarlo, no parcharlo: tres de sus apuestas (núcleo, τ, export) ya tienen veredicto y dos le juegan en contra. El Paper 3 aguanta con dos frases. Ninguno está para Zenodo.
- [NO TOCADO] No edité ningún esqueleto: esto es auditoría.

## Herramientas y máquina
- **brain-env.** Clon limpio de main (`06872d0`) para publicar; `verif_pub035.py` para el chequeo público sin token; lectura de los dos esqueletos con `git show` de sus ramas; grep de la 2026-10-12-015 y del CONTEXTO; prueba del parche en copia.
- **Zenodo.** Una llamada a publish; después, sólo lectura pública.
- **GitHub.** Push de esta respuesta, el recibo, el parche y su workflow; md5 desde clon limpio.
- Acción delicada: la publicación en Zenodo, irreversible, con el sí de Abraham (09:41).

## Archivos
| Archivo | md5 |
|---|---|
| `docs/v2/recibo-publicacion-v2.0.json` (main, este commit) | 36f66584243aae882b6ec76d59d636e6 |
| `docs/paper2/paper2-esqueleto.md` (`4652c81`) | 1c2912ff13d1f589514cd0128b0a69ab |
| `docs/paper3/paper3-esqueleto.md` (`5b2e5ee`) | d939bd8d36e7bb000e51fa7cd4523cf8 |
| `tools/contexto/actualizar_contexto_2026-10-14-035.py` (main, este commit) | be3553a245ce6ca64b8d90c1aa6b539e |
| `.github/workflows/contexto-2026-10-14-035.yml` (se borra al aplicarse) | c11fb2a68a0f3d14ea1cd2fe002ee5e7 |
| CONTEXTO antes y después del parche (probado en copia; la segunda aplicación aborta) | e8b496276efc8eaaf45a818e45e9831f y 933a87e30d03272e3525d35ad56a9a71 |

Doc de ClickUp: [035](https://app.clickup.com/90171457413/docs/2kza6fw5-22937).

## NO MEDIDO
- La mosca con lector entrenado sobre sus descendentes, en esta tarea.
- Costo de cada lector en un microcontrolador.
- La revisión de literatura de los huecos de §1 de los dos papers.
- La réplica de H_RIVAL en brain-env: c0 terminó bien (4.210 s), sigue c1.
- H_CONSENSO y H_TAU se leyeron en el CONTEXTO, no en sus agregados.

## Antes de firmar
| Afirmación | Instrumento | ¿Podía dar rojo? |
|---|---|---|
| La v2 está publicada | GET sin token al registro público | Sí: en borrador daba 404; dio 200 |
| Los PDF publicados son los sellados | md5 que publica Zenodo | Sí |
| El ridge ya estaba en la 015 | grep en la respuesta 2026-10-12-015 | Sí: podía no estar; está en 5 líneas |
| El esqueleto no nombra al ridge | lectura completa del esqueleto | Sí |
| H_CONSENSO y H_TAU tienen veredicto | CONTEXTO, que cita los agregados sellados | Sí, pero es una lectura de segunda mano |

--- METODO PROMETEO ---
Publicar sólo con el sí de Abraham y verificar el registro público con otro script. Auditar contra el texto de los esqueletos y contra los veredictos sellados, sin editar lo auditado.
Máquina: brain-env. Artefactos: este archivo en main, el recibo de la publicación y su Doc en ClickUp.
