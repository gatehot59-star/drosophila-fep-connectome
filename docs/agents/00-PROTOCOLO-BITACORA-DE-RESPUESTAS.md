# Protocolo: cada respuesta va a git

**Vigente desde:** 2026-08-23 · **Pedido por:** Jorge Abraham Mendieta · **Hereda de:** `mudh-mobile/docs/agents/01-GIT-COMO-BUS.md`

El repo de MUDH ya usa git como bus de órdenes y resultados. Esto extiende la misma idea a un problema distinto y peor: **la conversación se corta por tamaño y con ella se pierden las decisiones**, no solo los datos.

---

## 1. El lazo, en tres pasos y sin excepciones

```
1. ANTES de responder  -> leer  docs/agents/CONTEXTO-<proyecto>.md
                           y el último archivo de docs/agents/respuestas/
2. Resolver lo pedido  -> con la herramienta que corresponda, midiendo
3. ANTES de entregar   -> commitear docs/agents/respuestas/<fecha>-<nnn>-<slug>.md
                           + los archivos o código generados en esa respuesta
                           + actualizar CONTEXTO-<proyecto>.md si cambió el estado
```

Si el paso 1 no se hizo, la respuesta es sospechosa por construcción: está escrita desde memoria de modelo, que es exactamente lo que falló.

Si el paso 3 no se hizo, la respuesta **no existe**. Misma regla que en MUDH: un resultado que no está commiteado no existe.

---

## 2. Un archivo de contexto por proyecto

| Proyecto | Archivo canónico |
|---|---|
| Conectoma / FEP / papers | `docs/agents/CONTEXTO-drosophila-fep.md` (este repo) |
| MUDH-Mobile / AURA / SIAO | `mudh-mobile/docs/agents/00-METODO-DE-TRABAJO.md` §8 |
| DualBrain / SparseLTC embebido | `docs/agents/CONTEXTO-motor.md` (pendiente) |

El contexto es **estado vivo**, no narrativa: qué está medido, qué está refutado, qué está sin medir, qué está corriendo y sin leer, y qué decisión está esperando a Abraham. Se sobreescribe, no se acumula.

La acumulación va en `respuestas/`, que es append-only.

---

## 3. Contrato de un archivo de respuesta

Seis campos, sin excepción:

1. **Pedido** — qué preguntó, verbatim o resumido sin interpretar.
2. **Herramientas declaradas** — qué se llamó, y si escribió algo o gastó cuota ajena (C-03).
3. **Qué se midió** — con el número y el instrumento. Nada verde sin número.
4. **Evidencia cruda** — salida verbatim, md5, rutas, líneas de log (W-01).
5. **Archivos generados** — rutas commiteadas en ese mismo commit.
6. **NO MEDIDO** — lo que quedó afuera, declarado. Tres estados: bien, mal, y no medido.

Numeración: `YYYY-MM-DD-NNN-slug.md`, `NNN` correlativo del día.

---

## 4. Qué se commitea y qué no

- **Sí:** el archivo de respuesta, el código generado, los `.json`/`.log` de resultado, y el diff del contexto.
- **No:** binarios derivados (`.i32`, `.f32`, parquet). Van referenciados por md5 y tamaño, no commiteados. Regla clean-room INC-002.
- **Respuestas triviales** (un "dale", un ack) se agrupan al final del día en un solo archivo. El criterio es si produjeron una medición, una decisión o código.

---

## 5. Convenciones de commit

| Prefijo | Uso |
|---|---|
| `resp(NNN):` | archivo de respuesta + lo que generó |
| `estado:` | actualización de un `CONTEXTO-*.md` |
| `medida(objeto):` | resultado de una corrida, con su evidencia |
| `refuta(claim):` | algo que se cayó, con el número que lo tumbó |

Con esto `git log` es la bitácora real del proyecto y sobrevive al cierre de cualquier chat.

---

## 6. Por qué existe: la falla medida

- 2026-08-23: la tarea automática *"Conversation exceeded size"* (01:42) confirma que los cortes son por **tamaño**, no por pérdida de memoria. Pasaban siempre al cargar un PDF entero.
- El mismo día, `titan-brazo-w` terminó a las 18:44:50Z y quedó **completo y sin leer cerca de una hora** mientras se reportaba otra cosa.
- Peor que perder un número: se perdieron **formulaciones y prioridades mejores que el estado desde el que se siguió trabajando** (el motor ya estaba nombrado y priorizado al inicio del mismo chat, y después se lo trató como genérico).

Regla derivada: **nunca cargar un paper o PDF completo al chat.** Se extrae la tabla o sección, se escribe acá, se sigue.
