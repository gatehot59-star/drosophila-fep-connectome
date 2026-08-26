# LAS PAREDES DE TIEMPO · medidas por bisección, no recordadas

**Medido:** 2026-08-26 05:23-05:32 UTC · **Se re-mide, no se recuerda.**

**Por qué existe:** Abraham preguntó si tengo «controladores que testean cuánto me demoro» y si hay un tiempo que no debo pasar. La respuesta honesta requiere separar **tres** cosas que se confunden todo el tiempo, y solo una de las tres es una pared de reloj.

---

## 0. La distinción que cambia la operación

**La pared es de la LLAMADA, no del TRABAJO.**

Nadie cronometra cuánto tardo en pensar ni en redactar. Lo que existe es un techo por **llamada sincrónica a una herramienta**. Un proceso lanzado desprendido **sobrevive la pared y termina solo**, y esto está medido en los dos entornos.

Consecuencia operativa única: **nunca esperar sincrónicamente un trabajo largo. Lanzar desprendido y hacer polling.**

---

## 1. Mi sandbox (bash, Python, sin red)

| medición | resultado |
|---|---|
| techo por defecto | **30 s declarado** · `sleep 26` pasó (26,08 s reales) · `sleep 45` **murió** |
| techo con override | **120 s declarado** · `sleep 110` pasó, elapsed **exactamente 110 s** |
| persistencia de procesos | **SÍ, total** |
| `/home/user/output` | **se borra antes de cada comando** (medido: recreado vacío, mtime nuevo cada llamada) |
| `/home/user/scratch` | **persiste** (marca `1787721832` escrita en una llamada, leída en la siguiente) |

### La prueba de persistencia, y es fuerte

Un proceso lanzado con `nohup` que escribe un tick por segundo:

```
primer tick 1787721830  ultimo 1787722230  span 400 s  ticks 400  huecos 0
```

**400 ticks en 400 segundos de reloj, sin un solo hueco**, atravesando **tres llamadas distintas** y **una que terminó por timeout**. El proceso no se enteró de nada.

Y el caso extremo, no provocado: `python3 motor.py --null-kind ms` lleva **2 h 33 min al 99,8% de un núcleo**, sobreviviendo decenas de llamadas.

**Lo que SÍ mata el timeout:** el proceso en **foreground** de esa llamada. El `sleep 45` que se comía la pared no quedó huérfano; se limpió.

---

## 2. El gateway (`brain-env`, la máquina de Abraham)

**Bisección, con `/proc/uptime` como reloj:**

| sonda | inicio → fin (uptime) | resultado |
|---|---|---|
| 12 s + 12 s | 413195,49 → 413219,60 | **pasa** (24,1 s) |
| 45 s | 413229,47 → 413274,49 | **pasa** (45,02 s) |
| 55 s | 413280,98 → 413336,00 | **pasa** (55,02 s) |
| 20+20+20 s | — | **`Request timed out`** |

**La pared está entre 55 y 60 s.** Dado el número redondo, es **60 s**.

> **CORRIGE `CONTEXTO-ENTORNO.md` §7**, que decía *«entre 45 y 75 s»*. El rango se estrecha de 30 s a 5 s. La conclusión operativa de ese párrafo («para esperas largas: lanzar en background y hacer polling») **se confirma**, y ahora con el número.

### El trabajo sobrevive la pared. Medido.

Un job de **90 s** (una vez y media la pared) lanzado con `nohup`:

```
$ cat /workspace/nohup_test.log
413350.05
413440.05
TERMINO_SOLO
```

**413440,05 − 413350,05 = exactamente 90,00 s.** La llamada que lo lanzó volvió en 2 s. El job terminó solo y dejó su marca.

**Uptime del container al momento de medir: 413.503 s = 4 días 18,8 h.** No es efímero.

---

## 3. 🚨 ARTEFACTO DEL INSTRUMENTO · `$(date)` en el gateway NO es un reloj

Esto casi me hace publicar una conclusión falsa, así que va con la salida cruda:

```
$ echo INICIO $(date -u +%H:%M:%S); sleep 30; echo t30_OK $(date -u +%H:%M:%S)
INICIO 05:25:23
t30_OK 05:25:23      <- MISMO SEGUNDO despues de dormir 30 s
```

De ahí casi concluí **«el `sleep` no duerme en ese container»**, que era falso. La verificación con otro instrumento:

```
$ cut -d' ' -f1 /proc/uptime; command -v sleep; sleep 12; cut -d' ' -f1 /proc/uptime
413195.49
/usr/bin/sleep
413207.50            <- durmio 12,01 s
$ python3 -c "...time.sleep(12)..."
durmio 12.0 s
413219.60
```

**El wrapper del gateway pre-expande las sustituciones de comando una sola vez**, antes de ejecutar. Así que todos los `$(date)` de un comando reportan **el mismo instante**, el del parseo.

**Regla 11 del entorno:** para medir tiempo en el gateway, leer `/proc/uptime` **como archivo**, o usar `time.time()` de Python. `$(date)` mide el parseo, no la ejecución.

**Regla 12:** los `for ... ; do` con salto de línea se rompen (`Syntax error: word unexpected (expecting "do")`). Confirma la regla 4: script a archivo, o Python.

---

## 4. El lado «no tan oficial»: qué controla de verdad un turno

No hay un cronómetro sobre la prosa. Lo que hay es el campo **`stop_reason`** en cada respuesta, y es lo que decide si el loop sigue:

| `stop_reason` | qué significa |
|---|---|
| `end_turn` | terminé, se sale del loop |
| `tool_use` | quiero una herramienta, el loop sigue |
| `max_tokens` | me cortaron por techo de tokens. **Si cortó en medio de un `tool_use`, el JSON quedó incompleto** |
| `pause_turn` | el loop de servidor llegó a su tope de iteraciones |
| `refusal` | contenido vacío |

**`pause_turn` es «el controlador» que la pregunta busca, y no es un reto:** salta cuando el loop de sampling del servidor toca su tope de iteraciones (**default 10**) usando herramientas de servidor. Es lo que en la interfaz aparece como *«Claude reached its tool-use limit for this turn»* con un botón **Continue**. Es una **pausa, no una falla**: no se pierde contexto y se retoma donde quedó.

Fuentes consultadas en vivo el 2026-08-26:
- `platform.claude.com/docs/en/build-with-claude/handling-stop-reasons`
- `platform.claude.com/docs/en/agents-and-tools/tool-use/server-tools` (bloque `server_tool_use`, continuación por `pause_turn`)
- `platform.claude.com/docs/en/agents-and-tools/tool-use/programmatic-tool-calling` (existe justamente para **evitar** ida y vuelta por el modelo: −11% de tokens y +11% en benchmarks de búsqueda agentica)
- `startdebugging.net` (2026-05-30) para la traducción del banner y el default de 10 iteraciones

---

## 5. NO MEDIDO, declarado

- **No bisequé entre 56 y 59 s** en el gateway. La pared es «entre 55 y 60», no «60 exacto».
- **No medí el tope de llamadas por turno de ESTE entorno.** El «default 10 iteraciones» es de una página de terceros sobre la API, **no una medición de acá**. Es exactamente el patrón 3: un límite leído, no medido.
- **No probé si el sandbox acepta más de 120.000 ms.** El techo declarado se respetó, no se desafió.
- **No medí el umbral de compactación de la ventana de contexto.**
- **No reescribí `CONTEXTO-ENTORNO.md` §7** con el rango corregido. La regla de mantenimiento de ese archivo lo pide **en el mismo turno**; se prefirió un archivo aparte antes que reproducir ~1.000 líneas con riesgo de truncar en silencio, que es la prohibición más grave del método. **Queda como deuda declarada, no como omisión.**
