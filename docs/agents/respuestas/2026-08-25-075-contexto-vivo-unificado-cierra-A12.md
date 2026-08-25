# 075 · Contexto vivo unificado · cierra A-12 (a medias, y lo declaro)

**Fecha:** 2026-08-25 08:45 (America/Buenos_Aires) · **Modo:** TITAN LIGERO (operación documental, cero mediciones nuevas)

> **📄 Doc de ClickUp:** «CERRÉ A-12 · el contexto vivo del conectoma ya no está vencido (y el del motor sí)»
> **🛠 Instrumento:** ninguno (declarado). Todo número entra desde artefactos commiteados, leídos en este turno.

---

## 1. Pedido

Abraham pegó en un chat nuevo el link a `docs/agents/respuestas/2026-08-25-074-handoff-para-chat-nuevo.md`. **Sin texto adicional.** Leído como: cargá el estado real y arrancá. **No pidió una medición.**

## 2. Herramientas declaradas (C-03)

| Llamada | Escribe | Cuota ajena |
|---|---|---|
| `githubmcp_get_file_contents` × 5 (handoff 074, contexto viejo, resp 063, listado de `docs/agents/`, listado de `respuestas/`) | no | no |
| `githubmcp_list_commits` × 1 (8 últimos de la rama) | no | no |
| `create_document` × 1 (ClickUp) | sí | no |
| `githubmcp_push_files` × 1 → **rama `titan/twohop-nulls`** | sí | no |

**Cero Kaggle. Cero gateway. Cero runtime de Tachi. Nada borrado. Ningún merge. `main` intacta.**

Primer intento de lectura del handoff con `ref: refs/heads/titan/twohop-nulls` → **SSE error 405**. Reintento con `ref: titan/twohop-nulls` → OK. **Registrado porque es el modo de falla de no cerrar en el primer obstáculo.**

## 3. Qué se midió, y el defecto que cierra

**A-12 de la auditoría externa de Tao: los contextos vivos estaban vencidos.** Declarado cuatro veces sin hacerse.

| Medición | Número | Instrumento |
|---|---|---|
| Fecha del encabezado del contexto reemplazado | **2026-08-24 23:45** | lectura del blob |
| Última respuesta que el contexto citaba | **resp 061** | lectura del blob |
| Respuestas de retraso | **12** (063 a 074) | listado del directorio |
| Archivos en `docs/agents/respuestas/` | **74** | listado del directorio |
| Existencia de una resp **072** | **NO EXISTE.** Correlativo faltante, no pérdida | listado del directorio |

**Corroboración cruzada de los números que entran al contexto nuevo:** la tabla de la resp 074 contra los **mensajes de commit** `2d8f19d`, `a040c21`, `04bebb5`, `72d0b52`, `ccf8155`, `814f53b`. **Dos artefactos independientes, mismos números.** El null anatómico y sus tablas se tomaron de la **resp 063 leída completa**, no del resumen del handoff.

## 4. Evidencia cruda verbatim

```
blob e4d55bc36a538ccac195f8b00a3c9c731e64a36f  docs/agents/respuestas/2026-08-25-074-handoff-para-chat-nuevo.md
blob ad44b59f1fcd554755281aa9a946d882e6b569f2  docs/agents/CONTEXTO-drosophila-fep.md  (version REEMPLAZADA en este commit)
blob 3e2739c80275320920d36220c4b3f03f45db4507  docs/agents/respuestas/2026-08-24-063-el-null-anatomico-refuta-la-seccion-y-deja-un-resultado-mejor.md
HEAD antes de este commit:
  5955471b89bbf43017e970854c7330092d5fd79b  "resp: handoff para chat nuevo, estado al 2026-08-25 08:40"

encabezado del contexto reemplazado, verbatim:
  # CONTEXTO VIVO - conectoma / FEP / papers
  **Ultima actualizacion:** 2026-08-24 23:45 (America/Buenos_Aires) - **Se sobreescribe, no se acumula.**

listing docs/agents/  (13 entradas)
  00-PROTOCOLO-BITACORA-DE-RESPUESTAS.md  AUDITORIA-DEL-HILO.md  CONTEXTO-ENTORNO.md
  CONTEXTO-drosophila-fep.md  CONTEXTO-motor.md  INDICE-DE-ENLACES.md
  INDICE-REAL-POR-ENUMERACION.md  MANIFIESTO-KAGGLE.md
  ORDEN-TAO-ADDENDUM-01-tau-y-post-estimulo.md  ORDEN-TAO-AUDITORIA-EXTERNA.md
  evidencia/  respuestas/

cola del listado de docs/agents/respuestas/  (74 archivos en total)
  2026-08-24-061-null-de-grado-sobre-los-2-saltos.md
  2026-08-24-062-seccion-de-2-saltos-redactada.md
  2026-08-24-063-el-null-anatomico-refuta-la-seccion-y-deja-un-resultado-mejor.md
  2026-08-25-064-en-criollo-que-fue-la-entrega-del-null-anatomico.md
  2026-08-25-065-el-LC6-GF-sobrevive-el-null-anatomico-y-aparece-una-tabla-de-ruteo.md
  2026-08-25-066-barrido-de-literatura-la-tabla-de-ruteo-YA-esta-publicada.md
  2026-08-25-067-el-Cell-Type-Explorer-de-FAFB-publica-la-tabla-entera.md
  2026-08-25-068-entrada-de-biblioteca-corregida-y-el-AMMC-retirado.md
  2026-08-25-069-compilacion-completa-refuta-mi-prediccion-y-orden-para-tao.md
  2026-08-25-070-tau-barrida-y-la-metrica-estaba-mal-elegida.md
  2026-08-25-071-el-selpost-sobrevive-y-es-el-mejor-resultado-del-expediente.md
  2026-08-25-073-respuesta-a-la-auditoria-de-tao.md
  2026-08-25-074-handoff-para-chat-nuevo.md
  --> 072 AUSENTE (verificado en el listado, no inferido)

numeros corroborados por DOS artefactos (resp 074 + mensajes de commit):
  04bebb5 / a040c21 : sel_post 4,3287 | SIGN 1,9101 +/- 0,3242 z=+7,46 | TOPO 1,1896 +/- 0,0173 z=+181,4
                      post_looming observado 2,77 contra 16,09 del null de topologia
                      sel_peak POR DEBAJO de su null en 6 de 7 configuraciones
                      instrumento src/signshuffle_selpost.py md5 5a292cbc4f0a6b2d445405ad5c86ad80
  72d0b52 / ccf8155 : null que preserva Dale -> 1,7983 +/- 0,401  z=+6,31  0/40
                      A-06 verificado: 862 de 864 neuronas quedaban mixtas con el shuffle por arista
                      instrumento src/signshuffle_dale.py md5 d6f43b30050d192c6f3ae32956d92858
                      DONE in 288.3 s
  814f53b           : 13 de 13 hallazgos aceptados, 0 rechazados. 62/100 RECHAZADO como release
```

## 5. Lo que el contexto nuevo dice y el viejo no

1. **Cambió el activo.** El resultado más fuerte ya no es el spread de 323× de 2 saltos: es **`sel_post` = 4,3287 contra dos nulls independientes** (topología z = +181,4; signo con Dale preservado z = +6,31), con `sel_peak` **debajo** de su null en la misma corrida. Sección propia (§3).
2. **El null anatómico entra completo** (§3.bis) con la tabla de cruce de signos, el `SALIDA_DOM` de las cuatro clases y el enunciado invertido: el cero de olfatorio y visual es **geometría predicha**; el blindaje real es **gustativa, 10 socios motores contra 101,6 ± 1,2 (z = −78,9)**.
3. **Las ocho autorrefutaciones** quedan juntas en §4 **con su forma común**: medir bien y después afirmar sobre la **novedad** o la **causa** sin medir eso.
4. **La auditoría de Tao es sección nueva** (§5): 62/100, RECHAZADO como release, los cinco bloqueantes y **A-10 como prioridad técnica máxima**.
5. **Se retira el ítem 13 del viejo** («el null anatómico no es testeable»): los neuropilos estaban en **Zenodo `10676866` v783.0**.
6. **Tres modos de falla nuevos** en §9: prior art **antes** de medir · catálogo navegable del snapshot antes de contar un par · **un instrumento propio no cubre el sesgo de selección de su dueño**.
7. **Se corrigió el reloj:** el viejo decía «hoy es el 24-ago». Hoy es el **25-ago**, día 2 de la S1, y **quedan 5 días de erratum**.

## 6. Archivos generados en este turno

| Archivo | Qué |
|---|---|
| `docs/agents/CONTEXTO-drosophila-fep.md` | **sobrescrito.** Estado vivo al 25-ago 08:45, cubre hasta la resp 075 |
| `docs/agents/respuestas/2026-08-25-075-contexto-vivo-unificado-cierra-A12.md` | este |
| Doc de ClickUp | «CERRÉ A-12 · el contexto vivo del conectoma ya no está vencido (y el del motor sí)» |

## 7. NO MEDIDO, declarado

1. **`CONTEXTO-motor.md` NO se abrió en este turno.** **A-12 queda cerrado A LA MITAD**: el contexto del conectoma está unificado, el del motor sigue vencido y **no recibe veredicto de vigencia** (modo de falla 4). Está declarado así en el encabezado del contexto nuevo, para que un chat nuevo no lo lea como vigente.
2. **`CONTEXTO-ENTORNO.md` no se re-midió.** El §8 conserva lo declarado el 24-ago **con la advertencia explícita**. El entorno **se re-mide, no se recuerda**.
3. **Las respuestas 064 a 073 no se releyeron línea por línea.** Sus números entran vía resp 074 + mensajes de commit: **dos artefactos independientes, pero ninguno es una re-corrida.** Cualquier número de §3, §4 y §5 del contexto nuevo traza a esos artefactos, no a una medición de este turno.
4. **A-10 (el mapeo `id2i` de `scriptR.py`) sigue sin verificar** y es la prioridad técnica máxima: si falla, los 30/30 valores reproducen un bug.
5. **Los 13 issues de la auditoría no se abrieron:** son 5+ escrituras y esperan el OK de Abraham.
6. **Ningún guard corrió en este turno.** Nada de lo que se escribió acá se declara verde por medición nueva; el contexto solo reordena veredictos ya emitidos y commiteados.
7. **El review automático del PR no emitió hallazgos sobre estos dos archivos.** **K-02: deuda declarada, no aprobación.**
