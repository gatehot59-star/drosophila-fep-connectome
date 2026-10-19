# 2026-10-14-060 · ARRANQUE para un chat nuevo: relevamiento completo del proyecto y bateria de links

**Fecha:** 19-oct-2026, 14:30 (America/Buenos_Aires). **Doc:** https://app.clickup.com/90171457413/docs/2kza6fw5-23857

## Pedido

Abraham, 19-oct 13:23: repetir la respuesta y generar una bateria de links de los documentos de git y de ClickUp del proyecto (conectoma, DualBrain, DBC3, SparseLTC, los tres papers y los derivados), y un .md que explique todo lo desarrollado desde agosto, los recursos y como seguir, para arrancar un chat nuevo pegando solo ese .md.

## Veredicto primero

- [HECHO] `docs/agents/ARRANQUE-NUEVO-CHAT.md` en main: instrucciones para el agente, repos y archivos clave, cronologia desde el 21-ago, resultados por hipotesis, tres papers, derivados, maquinas y datos, estado y pasos siguientes, bateria de links. Mismo texto en el Doc de esta respuesta.
- [HECHO] Indice de git: `tools/arranque/generar_indice.py` y el workflow `arranque-2026-10-14-060`, que escribe `docs/agents/INDICE-COMPLETO-GIT.md` (respuestas de main y de ramas con su Doc, ramas, sellos, otros .md y links de ClickUp) y se borra solo.
- [MEDIDO] Indice de Docs de ClickUp (adjunto al Doc, INDICE-CLICKUP-PROYECTO-2026-10-19.md, md5 5df747f2): 578 del proyecto y 271 sin clasificar, con 849 links; 470 registros de otras lineas no se listan.
- [MEDIDO] Repeticion de la 059: humo 2 en ccf8d19 con prueba 6/6 VALIDO en Actions, mosca identica byte a byte al humo 1 y crudo VALIDO; CORRER disparado en 1f04d2c (19-oct 14:15).
- [NO MEDIDO] La curva de H_PARES_DATOS (corriendo) y el primer indice que escriba Actions.

## Herramientas y maquina

Conector de GitHub (lectura del CONTEXTO, listados, PR y push), sandbox de ClickUp (generador probado en un repo de prueba con main y dos ramas: dos corridas iguales, md5 del script 1c8e36b1; armado del indice de ClickUp), cuatro agentes de lectura que enumeraron los Docs con el buscador del workspace, Actions (humo 2, CORRER y el indice). brain-env respondio 530 todo el turno (tunel de Cloudflare, error 1033): nada corrio ahi.

## Evidencia

- Enumeracion de Docs por fecha de creacion: agosto 942 accesibles (896 unicos), 1 al 5-sep uno por uno y 6 al 30-sep por barrido de terminos del proyecto (universo 736), 1 al 9-oct 464, 10 al 19-oct 292. Clasificacion por titulo con reglas.
- Humo 2: `results/pares_datos_2026-10-18_humo/actions/` en ccf8d19 (humo_prueba.log: PRUEBAS 6/6 VALIDO, EXIT_RUN=0, md5 de los scripts iguales a brain-env).

## Archivos

- `docs/agents/ARRANQUE-NUEVO-CHAT.md`
- `tools/arranque/generar_indice.py` (md5 1c8e36b1 en el sandbox; el de git lo imprime el bot)
- `.github/workflows/arranque-2026-10-14-060.yml` (se borra al correr)
- `docs/agents/INDICE-COMPLETO-GIT.md` (lo escribe el bot)

## NO MEDIDO

La curva de H_PARES_DATOS; la clasificacion fina de los 271 Docs sin clasificar; el CONTEXTO no se toco (la 059 y la 060 entran en el proximo parche, probado en copia); la cola del CONTEXTO que el conector trunca.

## Antes de firmar

| Afirmacion | Instrumento | Podia dar rojo |
|---|---|---|
| Humo 2 VALIDO | prueba_pares.py y controles en Actions | si: el humo 1 dio rojo en la prueba |
| Generador deterministico | dos corridas sobre el mismo HEAD con cmp | si |
| 578 Docs del proyecto | conteo sobre los JSONL de los agentes | si, pero la clase sale de reglas sobre el titulo |

--- METODO PROMETEO ---
Rol: sintesis e indice (grande). Delicado: no.
Maquinas: conector GitHub, sandbox de ClickUp, agentes de lectura, Actions. brain-env: 530.
Archivo: docs/agents/respuestas/2026-10-14-060-arranque-nuevo-chat-relevamiento-completo.md
Doc: https://app.clickup.com/90171457413/docs/2kza6fw5-23857
