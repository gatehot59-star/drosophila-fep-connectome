# EVIDENCIA CRUDA · el arnés que corre el CI en local

**Fecha:** 2026-08-25 12:35 (America/Buenos_Aires)
**Instrumento:** sandbox propio. **git 2.39.5, python 3.12.13, SIN RED** (medido).
**Sujeto:** `tools/run_ci_local.py` md5 `93a43e58fb4f63f361ca1d38ffbccb9a`

---

## 0. El planteo de Abraham, y qué parte es correcta

> *«Pero si tenés entorno local para esas pruebas, no usamos git.»*

**La parte correcta, y es la que importa:** el **ciclo de descubrimiento** estaba mal. Para saber **por qué** fallaba el CI usé `push → esperar el runner → consultar la API`, cuatro veces. Ese último paso quemó **60 llamadas de una cuota compartida** y **nunca dijo la causa**: las cuatro causas las encontré reproduciendo en local, **después** de gastar la cuota. **El local era el instrumento de diagnóstico y lo usé último.**

**La parte que no se sostiene:** que el CI sobre. **Tres de los cuatro rojos fueron cosas que funcionaban en local y se rompían en una máquina limpia** — checkout fresco, sin paquetes preinstalados, sin archivos residuales. **El local dice si el código funciona; el CI dice si funciona en una máquina que no es la mía.** Son dos preguntas distintas.

> **El arreglo no es elegir uno: es que el local REPRODUZCA lo que el CI mide.** Eso es lo que mi banco de pruebas no hacía, y es la causa común de los cuatro rojos.

---

## 1. Corrida normal · el arnés reproduce el verde del CI

```
=== run_ci_local  ---  corre el job de CI leyendo el workflow real ===
workflow = .github/workflows/guards.yml
env del job: PYTHONDONTWRITEBYTECODE=1
pasos leidos: 9  (run: 8, uses: 1)
repo fresco en (temporal) con 6 archivos trackeados, arbol limpio

  OMITIDO (uses:)  checkout
  OK   rc=0  python del runner, medido y no supuesto
  OK   rc=0  la bateria NO importa nada fuera de la stdlib
  OK   rc=0  1 - bateria de guards, sin site-packages (exige VERDE)
  OK   rc=0  2 - mutar guards.py a proposito
  OK   rc=0  3 - la bateria DEBE dar rojo sobre el archivo mutado
  OK   rc=0  4 - restaurar guards.py
  OK   rc=0  5 - la bateria vuelve a dar verde con el archivo restaurado
  OK   rc=0  6 - el arbol de trabajo quedo limpio

=== RESUMEN ===
pasos run corridos: 8   en rojo: 0

VEREDICTO: el job pasa en local. El CI sigue siendo el testigo.
RC_TOTAL=0
```

**Calibración contra la medición externa:** el CI real dio **verde** en los dos check runs a las 14:58. **El arnés da verde también. Coinciden.**

---

## 2. 🔥 Reintroduciendo el BUG 1 · el arnés lo detecta sin pushear

Se volvió a poner el heredoc indentado en el paso 2 del workflow:

```
BUG 1 REINTRODUCIDO en el workflow
        | tests corridos : 28
        | fallados       : 0
        | TODOS VERDES, y los controles negativos demuestran que podian dar rojo
  ROJO rc=2  4 - restaurar guards.py
        | GUARD_FAILED no existe el respaldo src/guards.py.orig: no se puede restaurar
  OK   rc=0  5 - la bateria vuelve a dar verde con el archivo restaurado
  OK   rc=0  6 - el arbol de trabajo quedo limpio

=== RESUMEN ===
pasos run corridos: 8   en rojo: 2
   ROJO: 3 - la bateria DEBE dar rojo sobre el archivo mutado
   ROJO: 4 - restaurar guards.py

VEREDICTO: el job fallaria en el CI. Arreglar antes de pushear.
RC=1
```

**Y restaurado el archivo, vuelve a verde:**

```
=== RESUMEN ===
pasos run corridos: 8   en rojo: 0
VEREDICTO: el job pasa en local. El CI sigue siendo el testigo.
```

> **El arnés puede dar rojo y puede volver a verde. Sin push, sin runner, sin una sola llamada a la API.**

**Y da un diagnóstico mejor que el CI:** señala que la mutación no se aplicó (paso 3) **y** que por eso no hay respaldo para restaurar (paso 4). Dos síntomas de una causa.

---

## 3. 🔥🔥 La autoprueba FALLÓ, y eso descubrió que mi fix era redundante

`--break-pycache` quita `PYTHONDONTWRITEBYTECODE` para reproducir el bug 4. **Dio VERDE**, y el arnés **no se declaró exitoso**:

```
*** AUTOPRUEBA --break-pycache: se quita PYTHONDONTWRITEBYTECODE (valia 1)
*** se espera que el arnes detecte ROJO en el paso del arbol limpio
  ...
  OK   rc=0  6 - el arbol de trabajo quedo limpio
=== RESUMEN ===
pasos run corridos: 8   en rojo: 0
RC=2
GUARD_FAILED AUTOPRUEBA FALLIDA: con el bug 4 reintroducido el arnes dio VERDE.
              Un arnes que no puede dar rojo no adelanta nada.
```

**La causa, aislada quitando UNA defensa a la vez:**

| `.gitignore` | `PYTHONDONTWRITEBYTECODE` | resultado del paso 6 |
|---|---|---|
| **no** | **no** | 🔴 **ROJO**: `?? src/__pycache__/` → *AUTOPRUEBA OK, el arnés detecta el bug* |
| **sí** | no | 🟢 verde → la autoprueba aborta con 2 |
| sí | sí | 🟢 verde (el estado actual) |

```
--- prueba: sin la variable Y sin el .gitignore ---
  ROJO rc=1  6 - el arbol de trabajo quedo limpio
        | GUARD_FAILED el job dejo el arbol sucio:
        | ?? src/__pycache__/
AUTOPRUEBA OK: el arnes detecta el bug 4 EN LOCAL. Puede dar rojo.
RC=0
```

> **El `.gitignore` que agregué tapa el `__pycache__` por su cuenta: la variable de entorno es REDUNDANTE.** Mi «cinturón y tirantes» era **tirantes solos**, y lo supe porque **el guard de la autoprueba del arnés me dijo que no podía medir**.

**Las dos defensas se quedan** — la redundancia en algo que ya falló cuatro veces es barata — **pero ahora está MEDIDO cuál sostiene y cuál sobra, en vez de supuesto.**

**Y hay una tercera capa funcionando acá, que vale nombrar:** un test (`test_guards_negativo`), un test del test (la mutación), y un test del test del test (el guard de la autoprueba del arnés). **El tercero es el que atrapó el error, y era sobre mí.**

---

## 4. Los tres guards del parser, y por qué cada uno

Un parser de YAML casero **miente en silencio**: lee de menos y sigue. Los tres:

1. **cero pasos → aborta.** Un arnés que corre nada y dice verde es peor que no tenerlo.
2. **cuenta los `- name:` del archivo y exige que coincidan con los pasos leídos.** Medido: **9 declarados, 9 leídos.** Si el parser se comiera uno, aborta.
3. **un paso `run:` con script vacío → aborta.**

Y uno más en el armado del repo: **si el repo fresco arranca sucio, aborta**, porque entonces el paso del árbol limpio no mediría nada.

---

## 5. Qué NO reproduce el arnés, declarado

1. **Los pasos `uses:`** (checkout, setup-python). Se listan como **OMITIDO** y no se simulan.
2. **La versión de python del runner ni su sistema operativo.** El arnés corre con python 3.12.13 y el runner con el suyo.
3. **🔴 Nada que dependa de la RED.** Mi sandbox **no tiene red** (medido). Si el job instalara dependencias, un paso de `pip` daría rojo **por falta de red y no por el pin inexistente**: el arnés **lo catchea** (rojo es rojo, no se pushea) pero **no lo diagnostica**. En `brain-env`, que sí tiene red, sí lo diagnosticaría. **El job actual no instala nada, así que hoy no aplica** — pero si vuelve a instalar algo, hay que correr el arnés desde el container y no desde el sandbox.

> **Un verde local NO sustituye al CI: lo ADELANTA.** El CI sigue siendo el testigo; el arnés es el ensayo. Confundirlos sería repetir el error de origen al revés.

---

## 6. El costo, comparado

| | ciclo viejo | con el arnés |
|---|---|---|
| descubrir una causa | push + esperar runner + **consultar API** + reproducir en local | **una corrida local** |
| llamadas a la API | hasta agotar 60 y llegar a 403 | **cero** |
| cuándo aparece el rojo | después del push, en el historial público | **antes del push** |
| qué dice el rojo | «`failure`» | el paso, su `rc` y sus últimas 8 líneas |

---

## 7. NO MEDIDO, declarado

1. **El arnés no se corrió dentro de `brain-env`**, solo en el sandbox propio. **No está verificado que `git` exista en el container**, y el arnés lo necesita.
2. **No se reprodujeron los bugs 2 y 3** (los pins de `pip`) porque el job ya no instala nada y el sandbox no tiene red. **Quedan cubiertos por descripción, no por reproducción.**
3. **El parser cubre el subconjunto de sintaxis de ESTE workflow.** Si alguien agrega `strategy`, `matrix`, `if:`, `continue-on-error` o `working-directory`, **el arnés los ignora en silencio** — salvo que rompa el conteo de pasos, que sí aborta. **Esa es su línea de fragilidad y no está cubierta por un guard.**
4. **El CI no volvió a correr después de este commit**: el arnés vive en `tools/` y no toca el workflow.
