# EVIDENCIA CRUDA · revisión de los tres documentos de campo de Tachi

**Fecha:** 2026-08-25 10:20 (America/Buenos_Aires)
**Instrumento:** `gateway build.run` sobre `brain-env`, 4 corridas. Lectura de `mudh-mobile` vía integración GitHub.
**Sujetos:** `gatehot59-star/mudh-mobile` blobs `9a226be16b19ba094367134643b19ed1174d135d` (HANDOFF), `5a207c71f2f602725ee42cec3f906452d05e4f63` (informe cortés) y `f36909828e1def21b2a8626f33c4fe592eb3fe82` (informe incisivo).

---

## 0. Los tres documentos, identificados

| Commit | Hora UTC | Archivo | Qué es |
|---|---|---|---|
| `05a4d40c` | 24-ago 15:30 | `HANDOFF-ARRAQUE.md` | punto de restauración de Tachi. **64 adiciones, 70 borrados** |
| `73d022fb` | 25-ago 11:08 | `docs/campo/resultados/AUDITORIA-drosophila-fep-connectome-2026-08-25.md` | informe **cortés**, 65 líneas, `status: added` |
| `5d5806c4` | 25-ago 11:14 | **el mismo path** | informe **incisivo**, 50 adiciones y 44 borrados, `status: modified` |

**Los dos informes son el mismo archivo:** el incisivo **sobrescribió** al cortés seis minutos después. El cortés solo existe en el historial. **Eso importa para leerlos: no son dos auditorías, son una auditoría y su retractación de tono.**

---

## 1. 🔴 T-4 · «el activo comercial no está en el repo» · **CONFIRMADO**

```
$ curl -sS 'https://api.github.com/repos/gatehot59-star/drosophila-fep-connectome/git/trees/main?recursive=1'
HTTP=200 BYTES=41565
ARCHIVOS_TOTALES 113
ARCHIVOS_C_H_CPP 0 []
EXTENSIONES: ['(sin ext)', '.diff', '.json', '.log', '.md', '.mjs', '.py']
exit=0
```

**113 archivos y cero `.c`, `.h`, `.cpp` o `.ino`.** No es que el C esté incompleto: **no existe en el árbol.**

**Las dos consecuencias, y la segunda no la dice Tachi:**
1. El `README` ofrece **licencia dual comercial** sobre un motor que el repo no contiene.
2. **El `CONTEXTO-motor` declara «1.336 B de `.text` medidos en ESP32» y la fuente que produjo ese número no está acá.** O sea que ese número **no es reproducible desde este repo por nadie**, incluido yo. Está en la tabla de VALIDADO del contexto y su instrumento no es público.

---

## 2. 🟢 T-3 · «el README imprime p=0.0244 sin la advertencia» · **REFUTADO midiendo**

```
README_bytes 7844  METHODS_bytes 8386
  0.0244                 README=6   METHODS=3
  floor                  README=1   METHODS=1
  n = 40                 README=1   METHODS=1
  40 null                README=2   METHODS=6
  Bonferroni             README=0   METHODS=1
  not a measurement      README=0   METHODS=1
  ZZQQXX_CTRL_NEG        README=0   METHODS=0   <- control negativo

--- lineas del README que mencionan p ---
  L39: multi-edges created). `p = 0.0244` is the permutation floor with n = 40, i.e. no null
  L44: | Reciprocal edges | 4,014,518 | 84,932 +- 401 | **47.3x** | 0.0244 |
  L45: | Kenyon cell -> MBON edges | 62,261 | 2,568 +- 48 | **24.3x** | 0.0244 |
  L46: | Dopaminergic -> Kenyon cell | 47,404 | 1,735 +- 39 | **27.3x** | 0.0244 |
  L47: | Sensory -> Kenyon cell (direct) | **0** | 1,533 to 2,640 | **0.00x** | 0.0244 |
  L48: | MBON -> motor | 364 | 891 +- 34 | 0.41x | 0.0244 |
exit=0
```

**La advertencia está en la línea 39, inmediatamente antes de la tabla que empieza en la 44.** La acusación de la versión incisiva es falsa, y **la versión cortés del propio Tachi lo había leído bien** («p=0.0244 es el *piso* con n=40 (no una medición)»).

> **Al ponerse adversarial, el auditor afirmó sobre la presentación sin releer el archivo.** Es el modo de falla 3 de este proyecto, cometido por el auditor externo. Vale registrarlo sin sarcasmo: es exactamente lo que me pasa a mí cuando subo la intensidad.

**Lo que de T-3 SÍ queda en pie:** que con `n = 40` **ningún** `p` de las tablas puede bajar de 0,0244, así que **el `p` no discrimina entre un efecto de 47× y uno de 1,7×** — los cinco de la tabla muestran el mismo número. Para eso sirve el `z`, y el `z` sí está reportado. **Y su pregunta «¿por qué 40 y no 4000?» sigue sin respuesta medida.**

---

## 3. 🔴 EL HALLAZGO QUE SALE DE AHÍ Y ES MÍO · dos pisos distintos en el mismo repo

```
piso exacto con n = 40:
  one_sided  1/(40+1) = 0.02439
  two_sided  2/(40+1) = 0.04878
```

- El **`README` línea 39** declara el piso como **0,0244**, o sea **one-sided**.
- **`src/guards.py`** computa, en el mismo repo: `"p_floor": 2.0 / (n + 1.0)` y `"p_two": min(1.0, 2.0 * min(ge+1, le+1) / (n+1))` → para 0/40 da **0,0488**, **el doble**.

> **Dos criterios distintos para el mismo número, en el mismo repo, con factor 2 entre ellos.** Es el **modo de falla 5** («comparar dos cantidades medidas con criterios distintos»), **sexta reincidencia**, y toca **todas** las tablas publicadas.

**No se corrige acá:** elegir one-sided o two-sided es una decisión científica sobre la hipótesis que se está testeando, no un bug. **Se declara y espera a Abraham.**

---

## 4. 🔴 EL HALLAZGO QUE NINGUNA AUDITORÍA VIO · un token en el árbol de git

`HANDOFF-ARRAQUE.md`, sección 0, en un bloque `bash`:

```
export GITHUB_TOKEN="github_pat_11CJMT7JQ..."   (token completo en el archivo)
export JAVA_HOME=/home/estudiante/jdk17
```

**Y tres secciones más abajo, el mismo archivo tiene un título que dice «5. SECRETOS (NO en git)».** El documento declara la política y la viola en su propia sección 0. Es el **patrón 2 del Bloque 8**: la constante declarada que ningún camino respeta, en versión documental.

**Acotado ANTES de alarmar, porque la severidad depende de la exposición:**

```
=== EXPOSICION: se baja el HANDOFF SIN NINGUNA CREDENCIAL? ===
HTTP=404 BYTES=14
--- CONTROL: repo del conectoma tambien publico? ---
HTTP_conectoma=200
exit=0
```

**`mudh-mobile` da 404 sin credencial → es PRIVADO. Este repo da 200 → es público.** El control discrimina, así que la medición vale.

**Veredicto calibrado:** **el token NO está expuesto públicamente.** Pero está **en el historial de git de forma permanente** y lo ve cualquiera con acceso al repo, presente o futuro. **Severidad alta, urgencia media.**

**Lo que NO se hizo, a propósito:** no se probó el token. Usar una credencial ajena para medir su validez **no está autorizado**, y P-01 pone rotar credenciales del lado de Abraham. **El scanner de secretos se intentó y falló:** `Repository does not have GitHub Advanced Security enabled`. Se sustituyó por la medición de exposición vía HTTP, que responde la pregunta que importaba.

---

## 5. 🟡 T-6 · «la auditoría es circular» · **ACEPTADO, y corrige una frase mía**

Tachi: *«El que audita es el mismo sistema (Opus 5) que escribió el código. Tao es otro agente del mismo ecosistema.»*

**Correcto, y obliga a corregir la resp 073, donde escribí que la auditoría de Tao era «la primera medición externa real que tuvo este proyecto».** Tao es externo **al autor**, no **al ecosistema**. Los dos corren sobre el mismo modelo y el mismo método. Eso no anula sus 13 hallazgos — cinco eran de infraestructura y yo no los veía — pero **sí anula la palabra «externa» tal como la usé**.

**Y el propio Tachi cae en su versión del problema:** él también es del ecosistema. **El único falsador verdaderamente externo sigue siendo Abraham, que es supervisión manual y no escala.** Eso está escrito en B-01 como advertencia y hoy se cumple por tercera vez.

---

## 6. Los otros hallazgos de Tachi, con su veredicto

| # | Hallazgo | Veredicto |
|---|---|---|
| T-1 | los dos `.mjs` con paths absolutos, el clon limpio no reproduce | 🟢 **CONFIRMADO.** Coincide con **A-05** de Tao. **Dos auditores independientes, mismo defecto** |
| T-2 | «media parte del título se retiró» (la *temporal amplification*) | 🟡 **CIERTO AL 25-ago 11:08, YA NO.** El `sel_post` (z = +181,4 y z = +6,31 con Dale) se commiteó a las **11:12**, cuatro minutos antes de su informe incisivo, **en otra rama**. Auditó `main`, y `main` no tiene ese resultado. **No es un error suyo: es A-12, mi rama pública desalineada** |
| T-5 | «si se escapó un overflow, ¿cuántos errores más hay?» | 🟡 **PREGUNTA VÁLIDA, NO MEDIBLE como está.** No es falsable en la forma en que está escrita. Su forma útil: **el barrido de overflow cubrió un solo patrón (`N*(N-1)`) y `N**2` sigue sin barrer** |
| T-7 | «el enemigo no es un bug, es la velocidad» | 🟢 **ACEPTADO.** Y es el mismo diagnóstico que Tao por otra vía: ocho autorrefutaciones en dos días **no** son sólo autocorrección sana |

---

## 7. NO MEDIDO, declarado

1. **No se probó el token** y no se va a probar. Su validez es **NO MEDIDA**.
2. **No se buscaron más secretos** en `mudh-mobile`: se leyó **un** archivo. El scanner no está disponible (sin GHAS) y un `grep` sobre un repo privado entero no se corrió. **Puede haber más.**
3. **`grep -c` volvió a mentir en el `$?`** dentro de esta misma corrida: sin match imprime `0` y el shell reportó `exit 0`. El veredicto de exposición **no** descansa en ese `grep`, descansa en `HTTP=404 BYTES=14`.
4. **No se leyó `mudh-mobile` completo**, sólo los tres documentos y sus dos versiones.
5. **No se midió si el número de 1.336 B es correcto**, sólo que **su fuente no está en este repo**.
6. **La pregunta de Tachi «¿por qué 40 nulls y no 4000?» no se contestó midiendo.** El costo declarado en el repo es 180 min por corrida de 40.
7. **Nada se tocó en `mudh-mobile`.** Es el repo de otro proyecto y de otro ejecutor.
