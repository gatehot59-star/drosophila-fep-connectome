# resp 002 · Configurar el procedimiento: git como memoria, contexto por proyecto

**Fecha:** 2026-08-23 20:37–20:47 (America/Buenos_Aires)

## 1. Pedido

> «METER CADA RESPUESTA QUE DES EN UN ARCHIVO EN GIT, ACOMPAÑADA DEL CONTEXTO Y LOS ARCHIVOS Y/O CÓDIGO GENERADO EN ESA RESPUESTA. OBVIAMENTE DEBE HABER UN ARCHIVO DE CONTEXTO POR PROYECTO, SI VISITAS GIT CREO QUE YA HICIMOS ALGO DE ESO PARA EL PROYECTO DE MUDH MOBILE. LO SEGUNDO: CONFIGURAR AQUÍ EN CLICKUP ESE PROCEDIMIENTO, DONDE POR CADA RESPUESTA QUE DAS, ANTES VIAJAS A GIT, LEES EL ARCHIVO DE MEMORIA O CONTEXTO, VUELVES, RESUELVES LO QUE TE PIDIERON Y ANTES DE ENTREGAR LA RESPUESTA VUELVES A GIT PARA ENTREGAR AHÍ LA RESPUESTA Y DEMÁS.»

Pedido **dos veces**, la segunda idéntico. Se trata como confirmación y como señal de que la primera entrega no cerró el círculo: faltaban dos de los tres contextos.

## 2. Herramientas declaradas (C-03)

- GitHub: lectura de `mudh-mobile/docs/agents/` y de `01-GIT-COMO-BUS.md`; lectura del árbol de `drosophila-fep-connectome`.
- GitHub: **escritura** de 2 commits a `main` de `drosophila-fep-connectome` (6 archivos en total, ninguno sobreescribe código).
- Memoria de ClickUp: escritura de la regla de arranque.
- Cero cuota de Kaggle, cero kernels tocados, nada mergeado.

## 3. Qué se midió

**Tenía razón sobre MUDH.** El patrón ya existía y esto lo hereda en vez de inventarlo:

```
mudh-mobile/docs/agents/01-GIT-COMO-BUS.md   6801 B
  «un resultado que no está commiteado no existe»
  «el repo pasa a ser memoria compartida, no solo almacén de código»
  contrato de 7 campos por experimento · etiquetas for:tao / for:tachi / for:brain / for:ci
```

Estado del repo del conectoma antes de esto:

```
main: 1 commit (55aeba4), README.md de 206 B, nada más
PR #1: ABIERTO desde 2026-08-23T11:46:32Z, sin mergear
```

## 4. Evidencia cruda (W-01)

```
commit 6770542990d65a257e93cd3236647dcb7ab57366  -> refs/heads/main
  docs/agents/00-PROTOCOLO-BITACORA-DE-RESPUESTAS.md   4050 B
  docs/agents/CONTEXTO-drosophila-fep.md               5967 B
  docs/agents/respuestas/2026-08-23-001-motor-ltc-complejo.md

segundo commit (este):
  docs/agents/CONTEXTO-motor.md
  docs/agents/respuestas/2026-08-23-002-protocolo-bitacora.md
```

## 5. Archivos generados

Los cinco de arriba. Un archivo de contexto por proyecto, como se pidió:

| Proyecto | Contexto canónico |
|---|---|
| Conectoma / FEP / papers | `CONTEXTO-drosophila-fep.md` |
| Motor / DualBrain / embebido | `CONTEXTO-motor.md` |
| MUDH-Mobile / AURA / SIAO | `mudh-mobile/docs/agents/00-METODO-DE-TRABAJO.md` §8 + `01-GIT-COMO-BUS.md` |

## 6. NO MEDIDO, declarado

- **El paso 1 del lazo no es exigible mecánicamente.** No hay hook que me obligue a leer el contexto antes de contestar. El control real es que cada respuesta nombre el archivo commiteado: si no lo nombra, es incumplimiento verificable.
- **No se tocó `mudh-mobile`.** Ese repo ya tiene su protocolo y su estado vivo; agregarle un archivo redundante sería ruido. Si se quiere el mismo formato de `respuestas/` allá, es una decisión aparte.
- **`motor.py` y los otros 16 `.py` siguen sin commitear.** El protocolo existe, el código sigue en un solo disco.
- No se verificó que el PR #1 no entre en conflicto con estos commits a `main`.
