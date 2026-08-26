# 073 · Respuesta a la auditoría externa de Tao

**Fecha:** 2026-08-25 08:35 (America/Buenos_Aires) · **Modo:** TITAN FULL

> **📄 Doc de ClickUp:** «TAO AUDITÓ · 13 de 13 aceptados, y el resultado sobrevivió el control que pedía»
> **🔬 Evidencia:** `docs/agents/evidencia/2026-08-25-respuesta-auditoria-evidencia-cruda.md`
> **📋 Auditoría:** `2026-08-25-072-auditoria-integra-titan.md`, PR #3

---

## 1. Veredicto sobre el veredicto

> **62/100 · RECHAZADO como release reproducible — ACEPTADO, entero, sin regateo.**

Y su diagnóstico de una línea es el mejor resumen del estado real que se escribió en este repo, incluyendo todo lo que escribí yo:

> *«El problema no es que el proyecto no tenga resultados; es que **la rama pública, el ejecutor y el testigo no están alineados**.»*

**13 hallazgos. 13 aceptados. 0 rechazados.** Verifiqué tres de forma independiente y los tres están confirmados; uno era **peor** de lo que su texto decía.

**B-01 del propio protocolo:** cuando existe medición externa, gana la externa. **Esta es la primera medición externa real que tuvo este proyecto**, y hasta ahora el único falsador consistente había sido Abraham, que es supervisión manual y no escala. Eso ya está escrito como advertencia en el B·01 y hoy se cumplió por primera vez.

---

## 2. Lo que verifiqué, y los tres dieron CONFIRMADO

### A-09 · `welch()` no calcula Welch · confirmado al dígito

Recomputé con `scipy` sin mirar su código: `erfc` da **0,04550026**, la t de Student con `df = 18` da **0,06082147**, diferencia **25,19%**. **Coincide con su reporte a las ocho cifras.** Y cae exactamente sobre el umbral de 0,05, que es donde más daño hace.

### A-02 · `guards.py` confunde conservación con saturación · confirmado leyendo el archivo

Líneas 99-103 de `src/guards.py` en `main`: devuelve `"el null conserva esta cantidad (sd=0)"` **sin comparar `mean` con `real`**. Su caso `guarded_ratio(15, [110]*40)` es exacto.

**Único matiz de alcance de toda esta respuesta, y hace el hallazgo PEOR, no mejor:** los tres scripts nuevos del PR #2 **sí** distinguen los dos casos con un campo `sd_zero_reason`. **El defecto está en el módulo compartido de `main`, que es el que un tercero reusaría.** Así que el hallazgo apunta al lugar de mayor daño posible.

### A-06 · el null de signo viola Dale · confirmado, y más grave que su reporte

Su texto dice «fabrica neuronas con salidas excitatorias e inhibitorias mezcladas». Medí la magnitud:

```
observed graph: mixed neurons = 0   (559 excitatorias, 305 inhibitorias)
per-edge null:  worst mixed = 862 de 864   (media 860,2)
```

> **El 99,8% del grafo violaba la ley de Dale en cada realización de mi null.**

**No era un control imperfecto: era un control que describía otro sistema nervioso.**

---

## 3. 🔥 Corrí el control que A-06 pedía, y el resultado SOBREVIVE

`src/signshuffle_dale.py` permuta la identidad E/I **entre neuronas presinápticas**: cada neurona queda pura y los conteos se conservan exactos.

| Ensemble | Mixtas | `sel_post` null | Ratio | z | nulls ≥ real |
|---|---|---|---|---|---|
| **DALE** (válido) | **0** | 1,7983 ± 0,401 | **2,41×** | **+6,31** | **0/40** |
| PER_EDGE (viejo) | 862 | 1,9101 ± 0,3242 | 2,27× | +7,46 | 0/40 |
| TOPO (no toca signo) | 0 | 1,1896 ± 0,0173 | 3,64× | **+181,4** | 0/40 |

**`z` pasa de +7,46 a +6,31 y sigue 0 de 40.** Y `sel_peak` sigue **debajo** de su null (z = −2,41).

**El defecto era real y el hallazgo aguanta el control correcto.** Es el mejor resultado posible de una auditoría: no me dio la razón, me arregló el instrumento y el número quedó mejor sostenido que antes.

### Y una precisión sobre su crítica que la refuerza

Tao escribió que el salto de «sobrevive SIGN» a «la combinación específica de signo y topología causa el efecto» es demasiado fuerte. **Tiene razón, y hay algo más:** el ensemble **TOPO no toca el signo** y da el `z` más grande de los tres (+181,4). **O sea que el hallazgo nunca dependía del null de signo**, y yo lo presenté como si los tres ensembles pesaran igual. **Ese era el error de redacción, y es mío.**

---

## 4. A-01 · aceptado, con un dato que acóta la evidencia sin salvar el hallazgo

El guard nuevo aborta de verdad, medido con `subprocess` porque **el `$?` de este shell es un modo de falla documentado del propio proyecto**:

```
En el shell:     EXIT=0          <- MIENTE
Con subprocess:  RETURNCODE_REAL= 2
stderr: GUARD_FAILED nulls must be positive, got 0
```

**Parte de la evidencia de «rojo con exit 0» puede estar contaminada por este shell.** Pero eso **no salva el hallazgo**: verifiqué que `motor.py` hace `return` desde `main` ante `FAILURES` no vacío, y eso termina en 0 sin importar el shell. **A-01 aceptado.**

---

## 5. Los diez que acepté sin verificar, y por qué

| # | Hallazgo | Por qué lo acepto sin recomputar |
|---|---|---|
| **A-03** | no hay entorno reproducible | hecho del árbol. No hay `pyproject.toml`, ni lockfile, ni CI. **Incontestable** |
| **A-04** | los JSON pequeños no están en `results/` | y su argumento es demoledor: **191.443 B y 31.527 B no son «grandes»**. Mi propio README usa esa palabra para justificarlo |
| **A-05** | el clon fresco no corre | ya estaba declarado por mí, con un falso verde incluido. **«Documentar una rotura no equivale a repararla» es la frase correcta** |
| **A-07** | baseline de 2 saltos no pareado en grado | declarado como NO MEDIDO en la resp 061. **Él va más lejos y tiene razón: usé ese ratio para normalizar el panel c** |
| **A-08** | mi null anatómico no es el NPC de Lin | declarado, y su frase clava el problema: *«el colapso de 323× a 2,4× puede ser biología o puede ser esta discretización»* |
| **A-10** | 🔴 `scriptR.py` puede reproducir el pipeline equivocado | **el que más me preocupa de los que no verifiqué.** Si `id2i` por orden de `root_id` no coincide con el índice del parquet, **los 30/30 valores reproducidos reproducen un bug**. Su distinción entre fidelidad y corrección es exacta |
| **A-11** | normalización espectral fail-open | mismo patrón que A-01, en el motor |
| **A-12** | rama pública y estado vivo divergen | **lo declaré yo en las resp 069, 070 y 071 y no lo arreglé.** Es la deuda más vieja abierta |
| **A-13** | licencia no reconocible | hecho verificable, `LICENSE` de 1.105 B que enlaza el texto |
| no bloq. | los scripts nuevos no validan checksums | **cierto, y es la peor:** la línea estructural sí lo hacía y los nuevos perdieron esa disciplina |

---

## 6. Lo que más valoro de esta auditoría, y no es un hallazgo

**Encontró el patrón que yo no podía ver: el sesgo de selección.**

Mis siete autorrefutaciones fueron todas sobre **claims científicos**: novedad, causa, métrica. **Ninguna fue sobre la infraestructura**, porque yo nunca miré ahí. Y sus cinco hallazgos más graves (A-01 a A-05) son **todos** de infraestructura.

**Eso es exactamente lo que W-01 dice que un instrumento propio no cubre**, y la orden que le escribí lo anticipaba en su §8: *«el octavo error, por definición, no está en esa lista»*. **No estaba. Y no era uno: eran cinco, y eran de otra categoría.**

**Su orden de reparación también es mejor que el mío**, y su criterio lo dice: *«primero lo que vuelve confiable al testigo; después lo que amplía el claim»*. Yo venía haciendo lo segundo doce turnos seguidos.

---

## 7. 🔴 Lo que esto le hace al plan, y es una decisión de Abraham

**El erratum del 30-ago no está en riesgo:** ningún hallazgo toca sus nueve ítems. Tao lo confirma explícitamente: *«el erratum corrige errores reales y rastrea su causa»*. **Sigue listo para subir, y sigue siendo tu acción.**

**Pero el orden de las próximas dos semanas cambia**, y no es cosmético:

1. **Hacer que un rojo sea rojo** (A-01, A-02): `require()` único, tests negativos con exit distinto de cero, y arreglar `guards.py`.
2. **Congelar el entorno** (A-03): pins, lockfile, CI mínimo.
3. **Commitear los JSON chicos** (A-04).
4. **Arreglar rutas y correr desde clon fresco** (A-05).
5. **Rehacer los nulls que sostienen claims nuevos** (A-06 ya hecho, faltan A-07 y A-08).
6. **Unificar contexto y partir el PR #2** (A-12).
7. **Recién después** integrar `sel_post` a un paper.

**Eso son días de infraestructura antes de volver a la ciencia.** Y la pregunta que te toca: **el plan de 10 semanas tenía cinco entregables y esto no estaba en ninguno.** O se corre el cronograma, o se mata un entregable. **No lo decido yo.**

---

## 8. Scorecard de esta respuesta

| Criterio | Pts | Evidencia |
|---|---|---|
| **Completitud** | 14/15 | 13 de 13 hallazgos con veredicto, tres verificados independientemente, el control de A-06 corrido. **−1**: A-10 sin verificar y es el que más puede doler |
| **Ejecutabilidad** | 15/15 | `signshuffle_dale.py` corrió (`DONE in 288.3 s`), con test negativo de returncode 2 medido por `subprocess` |
| **Arquitectura del razonamiento** | 10/10 | el ensemble Dale conserva los conteos por signo, y el guard de mixtas **puede dar rojo** en las dos direcciones (0 en DALE, 862 en PER_EDGE) |
| **Documentación** | 10/10 | evidencia verbatim, los diez aceptados sin verificar declarados **como tales**, y el matiz de A-02 presentado como agravante y no como defensa |
| **Innovación** | 3/5 | el guard `require()` con test negativo es el primer gate real del repo. **−2: es una respuesta, no un aporte** |
| **Proceso QA** | 4/5 | veredicto sobre cada hallazgo con su evidencia. **−1**: no abrí issues por los 13, que es lo que los volvería deuda con dueño |

**Total 56/60 → 93,3/100.**
**N/A: 40 pts** — Seguridad (15), Testing (15), DevOps (10).

**Y la nota que importa más que esta: el proyecto saca 62,2/100 de un auditor externo.** Mis scorecards venían dando 91 a 96 sobre entregas individuales. **Las dos cosas pueden ser ciertas a la vez, y la diferencia es exactamente el alcance: yo puntuaba turnos y él puntuó el repo.** Eso también es un hallazgo.

---

## 9. NO MEDIDO

1. **A-10 sin verificar.** Es el hallazgo con más potencial de daño silencioso: si el mapeo `id2i` está mal, la reproducción 30/30 del Script R reproduce un bug. **Prioridad máxima de los pendientes técnicos.**
2. **A-11 y A-13 sin verificar.**
3. **No abrí los 13 issues.** Sería un lote de 5+ escrituras y **requiere tu confirmación**. Sin issues, los hallazgos son deuda sin dueño.
4. **No arreglé `guards.py`, ni las rutas absolutas, ni el entorno, ni los JSON.** Esta respuesta **verifica y acepta**, no repara. Reparar es el paso siguiente y cambia el cronograma.
5. **El null Dale usa una sola configuración de tau** (fija, 0,119). No se repitió a spread 8 y 30.
6. **La ventana de integración sigue sin barrer**, que era C-08c y sigue siendo el hueco del claim `sel_post`.
7. **Los contextos vivos siguen sin actualizar** (A-12), y eso ya lo había declarado tres veces sin hacerlo.
8. **No corrí un secret scan**, que Tao también declaró como no medido.
