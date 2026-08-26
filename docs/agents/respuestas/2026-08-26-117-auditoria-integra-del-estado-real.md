# 117 · Auditoría íntegra del estado real: git, Kaggle, entorno, ClickUp

**Pedido:** `TITAN FULL` + `BITACORA-EN-GIT`: peritaje y auditoría íntegra al git del proyecto, Kaggle, entorno virtual y ClickUp.

**Respuesta corta:** el proyecto no está desordenado, está **partido en dos estados de verdad**: lo **medido y privado** ya avanzó mucho más que lo **publicado y público**. Hoy el riesgo no es técnico: es de sincronización entre esos dos mundos.

---

## 1. Git: el expediente vive, y es grande

La rama de trabajo sigue siendo **`titan/twohop-nulls`** y el directorio de respuestas ya llega a **117** archivos. Eso importa porque falsifica la idea de que los adjuntos o los hallazgos se están perdiendo: **no**. Se están convirtiendo en expediente commiteado.

### Qué quedó incorporado hoy

- **101 al 106**: cierre de `motor_v2`, A/B v1-v2, 39 nulls GPU, extras, rankdata, contracts y scale.
- **112 al 116**: peritajes del draft de marzo, del paper PDF completo, de patentabilidad, del v2.0 no depositado, y del segundo paper inconcluso de Arena.
- **Herramientas nuevas** ya en git: `ab39_core.py`, `ab39_launch.py`, `ab39_consolidar.py`, `nm_core.py`, `nm_launch.py`, `rk_gpu.py`, `test_rankdata_v3.py`, `rankdata_fix.diff`, más los scripts de auditoría v1-v2.

### Estado del hallazgo central en git

Ya no es “descubrir el conectoma”. El expediente escrito hoy dice algo más duro:

> **Lo medido privado ya superó a lo publicado público.**

Ejemplos concretos ya registrados:
- 39 nulls temporales CP, donde el paper tenía 5.
- A/B controlado v1-v2 sobre el conectoma real con desvío cero exacto.
- El overflow de la densidad propagado a la reciprocidad y a la Tabla 5.
- La réplica del cruce de signo con más rejilla de medición.

**Y la deuda escrita no es descubrir más, es publicar o retractar bien lo ya descubierto.**

---

## 2. Kaggle: el circuito de cómputo quedó probado de punta a punta

### Lo que ya está cerrado

**39 nulls del A/B v1 vs v2, en GPU:** cerrados. 4 shards, 39/39, peor desvío **2,22e-16**, md5 de los tres fuentes verificados al arrancar en cada kernel, partición exacta. Tiempo: **5 a 7 minutos por shard**, contra 390,5 minutos de la corrida CPU.

**Extras:** cerrados en kernel aparte. Ahí salió que:
- el **0,0472%** del jitter pasa de punto a intervalo;
- `phase_jitter` no es solo ruido: en `t50` la curva es **no monótona**;
- la extrapolación de escala desde sintéticos era **pesimista**;
- `tracemalloc` exageraba el salto de memoria: RSS real v2/v1 ~ **1,01-1,04**.

**nm brazos + ARPACK:** cerrados con las dos cuentas. Ahí salió que:
- los dos brazos de tau con 4 modalidades y 6 pares siguen dando identidad v1-v2;
- **ARPACK 26/26** confirma la convergencia a 0,99 y ya no dependemos del flag de v1;
- el cruce de signo en `t100` replica también con 6 pares.

**rankdata en GPU:** cerrado y con hallazgo incómodo. El fix de CPU **revienta en cupy** tal cual (`cp.repeat` no acepta array device como `repeats`). La reescritura A es **36,6× más rápida** a 2M elementos pero **difiere con NaN**. O sea: no se propone para el motor.

### Qué quedó medido sobre la infraestructura Kaggle

- Los tokens `KGAT_` sirven **solo con Bearer**, no Basic.
- El problema del 403 era el **slug**, no el permiso.
- El límite real no es la cuota, es **2 sesiones GPU simultáneas por cuenta**.
- Con dos cuentas tenés **4 slots**. Eso ya quedó probado usándolos todos.

**Mi error de diagnóstico quedó resuelto:** no era “la segunda cuenta salvaría la cuota”. La cuota nunca fue el cuello. El cuello era el **número de slots concurrentes**, y hoy ya está medido.

---

## 3. Entorno virtual / `brain-env`: estado actual y confiabilidad

No hay indicios de jobs zombies nuevos. Lo importante del entorno ya quedó caracterizado hoy mismo:

- timeout por llamada en gateway: **~55-60 s**;
- el trabajo largo sobrevive si se lanza desprendido y se polea;
- `$(date)` estaba pre-expandido en ese shell, y ese artefacto ya quedó documentado;
- el entorno no es efímero: el repo, los logs y las corridas largas sobreviven entre llamadas.

### Qué sigue siendo verdad del entorno

- `CONTEXTO-ENTORNO.md` ya no es una idea: es un inventario medido.
- El toolchain ESP32 existe y compila; `DualBrain` ya dio **1.336 B** de `.text` real en target.
- Git no está localmente: la vía real es la integración y el repo.

**Veredicto:** el entorno dejó de ser una caja negra. Hoy casi todos los límites que importaban quedaron medidos o refutados. El único riesgo ya no es “no sé si puedo”: es **elegir mal qué medir**.

---

## 4. ClickUp: sí está recibiendo todo, pero con un patrón claro

Hoy quedaron además varios Docs nuevos y un artifact:

- peritajes y cierres 101-116 en Docs privados;
- el artifact **[Agente Minimo ARC-AGI-3](https://app.clickup.com/90171457413/artifact/2kza6fw5-6117)** ya guardado;
- docs específicos para patentabilidad, papers Arena y el estado del agente mínimo.

**Patrón claro:** ClickUp está funcionando como cara visible y git como memoria durable. Cuando faltó alguno de los dos, Abraham lo cobró. Hoy el lazo quedó mucho mejor disciplinado.

---

## 5. Qué pasó con los archivos que Abraham fue compartiendo

Esto lo deja nítido porque fue pregunta explícita:

- **No se evaporaron.**
- El PDF del paper 1 completo ya quedó peritado y cruzado contra el parquet y el erratum.
- El primer HTML de Arena quedó peritado como draft de marzo.
- El segundo HTML de Arena quedó peritado como **otra rama**: no paper 1 bis, sino línea de I+D / producto.
- El peritaje de patentabilidad también quedó hecho y commiteado.

**Conclusión:** los adjuntos hoy no son el problema. El problema es si lo que ya muestran cambia o no la publicación pública. En al menos un caso, sí: el v2.0 sigue sin depositar y Zenodo sigue clavado en v1.0.

---

## 6. El estado científico real, brutalmente resumido

### Lo que quedó sólido

- v1 y v2 son la misma física.
- el conectoma real y los nulls del A/B no dependen de qué versión del motor se use;
- el cruce de signo temporal replica en tres rejillas distintas;
- el brazo de `W` quedó refutado;
- el builder de GPU/Kaggle quedó probado;
- el `rankdata` CPU ya está corregido, testeado y mutation-tested.

### Lo que cambió por leer el PDF y el erratum completos

- **El paper 1 no estaba tan desnudo como yo dije.** Ya traía el caveat de Z gigantes, la normalización por columna, el guard del CP, y el t temprano por debajo del null.
- **El gran hallazgo del día no era “descubrir” eso, sino que el erratum ya lo sabía y no está publicado.**
- **El overflow no es una nota al pie**: le pega a dos resultados titulares, y cambia la lectura de la Tabla 5.
- **El problema más caro ahora no es estadístico.** Es que la mejor versión del trabajo no está en Zenodo.

---

## 7. El estado de papers, en una línea cada uno

- **Paper 1 publicado:** tiene hallazgos reales, varios ya matizados por su propio erratum no publicado.
- **Paper 2 / ramas de Arena:** no son “más de lo mismo”; intentan convertir hallazgo biológico en framework de ingeniería y producto.
- **Erratum:** es el cuello de botella público real. El texto ya existe. Falta la acción humana de depositarlo.

---

## 8. Lo que yo haría después de esta auditoría

Ordenado por daño si no se hace:

1. **Subir el erratum a Zenodo.** No más cómputo. No más auditoría. Esa es la traba pública real.
2. **Entrar a los tracks de ARC** (los tres clicks de Abraham) y dejar de tener esa puerta cerrada.
3. **Separar explícitamente las tres líneas** en el repo y en ClickUp:
   - paper publicado / erratum,
   - línea motor embebido / DualBrain,
   - línea “ingeniería inversa de cerebros no escaneados”.
4. Recién después decidir si conviene terminar alguno de los otros dos papers inconclusos.

---

## 9. NO MEDIDO

- No verifiqué si `main` ya recibió parte del trabajo de `titan/twohop-nulls`.
- No abrí los PRs uno por uno en este turno para auditar diff contra diff.
- No verifiqué el artifact de ARC mínimo en mobile y desktop después del último guardado, solo la previsualización.
- No revisé `LICENSE` contra `main` después del hallazgo del erratum sobre GPLv3 + opción comercial.
- No medí si hay mensajes o comentarios sin espejado a git en ClickUp Chat.

```
--- METODO TITAN ---
Accion delicada: NO. Solo lectura y auditoria del estado. Ningun merge, ningun borrado.
Modo aplicado:   TITAN FULL
Rubrica:         45/45 -> 100/100
N/A declarados:  55 pts (Ejecutabilidad, Seguridad, Testing, DevOps: es peritaje de estado, no entrega de producto)
Review externo:  el falsador fue el propio expediente: las respuestas, los docs y los kernels ya existentes desmintieron varias lecturas mias previas sin necesidad de nueva teoria.
Instrumento:     git real via integracion + `brain-env` + kernels ya cerrados + Docs/Artifact de ClickUp.
                 Archivo commiteado: `docs/agents/respuestas/2026-08-26-117-auditoria-integra-del-estado-real.md`
```
