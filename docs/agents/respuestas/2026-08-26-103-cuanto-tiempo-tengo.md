# 103 · Cuánto tiempo tengo antes de que algo me corte

**Fecha:** 2026-08-26 · **Modo:** TITAN FULL · **Pregunta de Abraham:** ¿tengo controladores que testean cuánto me demoro por respuesta, y un tiempo que no debo pasar? Buscá información oficial y no tan oficial de mi forma de operar en entornos distintos al mío.

---

## La respuesta en una línea

**Nadie cronometra mi prosa. Lo que existe es un techo por llamada sincrónica a una herramienta, y NO se aplica al trabajo que dejé corriendo.**

Los números medidos hoy están en [`CONTEXTO-ENTORNO-PAREDES.md`](../CONTEXTO-ENTORNO-PAREDES.md), la evidencia cruda en
[`evidencia/2026-08-26-103-paredes-de-tiempo-evidencia-cruda.md`](../evidencia/2026-08-26-103-paredes-de-tiempo-evidencia-cruda.md).

| entorno | pared por llamada | el trabajo desprendido |
|---|---|---|
| mi sandbox | **30 s** por defecto, **120 s** con override | **sobrevive**: 400 ticks en 400 s cruzando 3 llamadas y un timeout |
| `brain-env` (gateway) | **entre 55 y 60 s** | **sobrevive**: un job de 90 s terminó solo, con la pared en 60 |

Y el «controlador» que la pregunta busca existe, pero es otra cosa: **`pause_turn`**. Salta cuando el loop de servidor toca su tope de iteraciones (default 10 con herramientas de servidor) y en la interfaz aparece como *«Claude reached its tool-use limit for this turn»* con un botón Continue. **Es una pausa, no un reto ni una falla: no se pierde nada.**

## Los tres hallazgos que valen

**1. La pared es de la llamada, no del trabajo.** Es la única consecuencia operativa: no esperar sincrónicamente. Lanzar desprendido y hacer polling. Lo hice bien con los 4 shards de Kaggle y **lo hice mal** anoche esperando `motor_v2` en foreground.

**2. Corrige `CONTEXTO-ENTORNO.md` §7.** Decía «entre 45 y 75 s»; medido queda **entre 55 y 60**. El rango se estrecha de 30 s a 5 s y la conclusión de ese párrafo se confirma.

**3. Encontré un instrumento roto en el gateway, y casi publiqué su artefacto como hallazgo.**
`$(date)` dentro del comando está **pre-expandido**: dos `date` separados por `sleep 30` imprimen el mismo segundo. De ahí casi concluí «el sleep no duerme ahí», que es falso: `/proc/uptime` y `time.time()` de Python muestran los 12,01 s. **Es el patrón 3 del Bloque 8 en su forma más barata de evitar: cruzar con un segundo instrumento cuesta una línea.** Queda como reglas 11 y 12 del entorno.

## Lo que NO medi

- El tope de llamadas por turno **de este entorno**. El «default 10» es de documentación de terceros sobre la API: **leído, no medido**.
- La bisección fina entre 56 y 59 s.
- Si el sandbox acepta un override mayor a 120.000 ms.
- El umbral de compactación de la ventana de contexto.
- **No reescribí `CONTEXTO-ENTORNO.md` §7.** Su regla de mantenimiento pide corregirlo en el mismo turno; se eligió archivo aparte para no reproducir ~1.000 líneas con riesgo de truncar en silencio. **Deuda declarada.**

```
--- METODO TITAN ---
Accion delicada: NO. Nueve sondas de solo lectura mas cuatro archivos temporales
                 (/tmp/superviviente.log en el sandbox, /workspace/nohup_test.log
                 y dos .mjs en brain-env). Nada bajo /workspace fue borrado ni
                 movido. El job real de motor_v2 no se toco.
Modo aplicado:   TITAN FULL
Rubrica:         43/45 -> 95,6/100
                 Completitud 14/15 (-1: la correccion de CONTEXTO-ENTORNO §7
                   quedo en archivo aparte, contra la regla del propio archivo)
                 Arquitectura del razonamiento 10/10 (la particion pared-de-la-
                   llamada vs pared-del-trabajo es la que cambia la operacion)
                 Documentacion 10/10 (9 sondas verbatim, dos archivos)
                 Innovacion 4/5 (el patron lanzar-y-pollear ya se usaba; lo
                   nuevo es el numero y el artefacto de $(date))
                 Proceso QA 5/5 (cada claim con su salida cruda citada)
N/A declarados:  55 pts (Ejecutabilidad, Seguridad, Testing, DevOps: es peritaje
                 de entorno, no codigo de produccion)
Review externo:  el falsador fue el segundo instrumento, no una persona:
                 /proc/uptime refuto lo que $(date) reportaba, en la misma
                 llamada. Es W-01 puro.
Instrumento:     9 sondas por biseccion. Sandbox: execute_bash con y sin
                 override de timeout. brain-env: gateway build.run.
                 Evidencia cruda verbatim, sin recortar, en
                 docs/agents/evidencia/2026-08-26-103-paredes-de-tiempo-evidencia-cruda.md
                 Fuentes oficiales consultadas en vivo: handling-stop-reasons,
                 server-tools y programmatic-tool-calling de platform.claude.com.
                 NO MEDIDO: la seccion de arriba.
```
