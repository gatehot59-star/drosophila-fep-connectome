# 2026-10-11-005 · En criollo: qué tenemos entre manos con el conectoma

**Fecha:** 2026-10-11, madrugada (America/Buenos_Aires).
**Base:** `main` en `41fa8bc6ba18d6f39a5b887681f7053b75d0afa3`; fe de erratas v2 con el pin `17fc577`.
**Doc de ClickUp (público):** https://app.clickup.com/90171457413/docs/2kza6fw5-21057

## 1. Pedido

> en criollo, que tenemos entre manos?

## 2. Herramientas declaradas

- **Gateway a brain-env, sólo lectura:** `git fetch` de `main`, `git show` del CONTEXTO y de la 004, y `md5sum` y `grep` del log de la 003. Después del push, la verificación de md5 y de las citas de este archivo. Nada pesado ni cuota ajena.
- **GitHub MCP:** un commit a `main` con este archivo. No toca ramas, PRs ni el CONTEXTO, porque el estado no cambió.
- **ClickUp:** un Doc público nuevo, y un aviso de «superado» arriba de los Docs de la 001 y la 002.
- **Sin mediciones nuevas:** es la síntesis de lo commiteado hasta `41fa8bc`, más el log de la 003 que vive en brain-env.

## 3. Qué se midió

### Lectura, en criollo

**En corto:** el paper de marzo ya tiene sus errores corregidos en una fe de erratas, pero esa v2 nunca se subió a Zenodo. Debajo hay seis hallazgos que aguantan el azar más exigente, casi todos guardados en ramas y no en `main`. La prueba por circuito dice que la caída de la ida y vuelta hacia el motor la explica el azar, y todavía no está firmada.

**Lo firme.** Firme quiere decir que aguanta un azar que respeta lo que ya se sabe del cableado.

1. **La ida y vuelta es real:** 20,6 veces más pares recíprocos que en el azar CP, que respeta cuántos cables tiene cada neurona y entre qué clases van. Ningún nulo llega. Ya no se dice 36×.
2. **El detector de «algo se me viene encima» no le habla directo al botón de escape:** LC6→GF da 0 contra 17,2 esperados con el azar anatómico (z = −5,61, 40/40).
3. **El que recibe elige con quién:** sel_post aguanta el azar de topología y el de signo (z = +181 y +6,31; 0/40).
4. **El gusto llega pobre a dos saltos:** con el azar anatómico hay 10 contra 101,6 esperados (z = −78,9).
5. **El circuito donde la mosca aprende sale muy por encima del azar CP:** KC→MBON 7,81×, DAN→KC 8,71× y KC→KC 7,26×, 0/40.
6. **Quién manda en la salida:** con los dos nulos y FWER quedan cinco cosas. Las descendentes se mandan entre ellas y les mandan a las motoras, al cuello y a la antena, y el óptico casi no les habla a las descendentes.

**Lo que se cayó**, y está bien que se haya caído:

- el 36× (venía de un desborde de enteros) y el 1.559×, retirados en el erratum;
- el 323× a dos saltos, que era co-localización: con el azar anatómico baja a 2,4×;
- la tabla de ruteo como descubrimiento propio, porque ya había prior art;
- la entrada AMMC directa a la fibra gigante;
- el efecto temporal global (p = 0,25 con 39 nulos) y la ventaja de la tau compleja (p = 0,60);
- H4 débil, refutada en su alcance estrecho. H4 fuerte no se puede medir con datos públicos y está estacionada.

**La prueba «que importaba» (003):**

- **Las cuentas cruzan con la base del erratum:** Tabla 7 8/8 con el pin, y el azar CP reproduce el del erratum (20,60× contra 20,59×).
- **Lo que dice:** cada circuito tiene entre 3,67× y 9,57× más ida y vuelta que el azar CP, pero la caída hacia el motor la reproduce el azar. Hay menos cables de vuelta entre esas clases; no es que la red elija devolver menos.
- **El nulo CM, que sólo respeta grados, no vale:** da «más allá del nulo» con ≥5, pero espera tan pocas recíprocas que la cuenta la domina el seudoconteo de 0,5.
- **Por qué no se firma:** de 20 grafos falsos que no deberían dar nada, la prueba principal rechazó 0 con ≥1 y 6 con ≥5, justo en el tope de 6. La secundaria, con ≥1, rechazó 8 con un tope de 5,94: FAIL. Hasta explicarlo, es lectura y no veredicto.
- **Opinión:** si se confirma, la caída por circuito no es lo que hace que el paper demuestre. Lo que demuestra ya está medido: los seis puntos de arriba.

**Lo que traba, y no es ciencia:**

1. **Lo bueno está en ramas y `main` muestra lo viejo:** la SECCION-V2 de `main` todavía es la del 323×, y las respuestas 063 a 124 no están en `main`. Decide Abraham: traer el linaje (PR #1, #2 y #3) o un PR sólo de documentos.
2. **La v2 no está en Zenodo:** el que entra por el DOI lee el 36×. Depositar lo hace Abraham.
3. **También esperan decisión** el PR #26 de la Tabla 7 y pasar al erratum el 8,6 y el ítem 9.

**Lo que sigue de este lado:**

1. Arreglar el instrumento de la 003, volver a correrla y firmarla. Recién ahí sube a la rama.
2. Medir lo que falta para la v2:
   - el azar por neuropilo de cada sinapsis;
   - la ventana y la tau de sel_post;
   - Lin región por región;
   - Betzel arista por arista;
   - la fila AN de la Tabla 5.

### Calibración

- Cada número de la lectura sale de una línea citada en el punto 4, verbatim, de tres fuentes con md5.
- Después del push, en brain-env se verifica que:
  - el md5 de este archivo en `main` sea el del sandbox;
  - ninguna línea citada falte en su fuente (`grep -F -x -v -f fuente citas | wc -l` tiene que dar 0);
  - el instrumento pueda dar rojo: con una línea perturbada agregada a las citas tiene que dar 1.

### Errores propios

- **La 001 y la 002 de esta madrugada no contemplaban la fe de erratas v2 ni el expediente de ramas.** Decían que la caída hacia el motor «sigue en pie» y que faltaba «una sola prueba». Esa prueba se corrió en la 003 y apunta a lo contrario. Sus Docs quedan con un aviso de superado; sus archivos de git no se tocan, porque las respuestas son append-only.

## 4. Evidencia cruda (verbatim)

**Fuente A.** `docs/agents/CONTEXTO-drosophila-fep.md` en `main` `41fa8bc`: md5 `25661a94b5987bfeeec4d16260972979`, 136 líneas, 9874 B.

```text
**Base vigente del paper:** `docs/ERRATUM.md` (9 ítems) con anotaciones pinneadas a `17fc577`. **Zenodo tiene sólo la v1.0** (20-mar): la v2 con el erratum no está depositada.
- **El expediente de agosto vive en ramas sin mergear:** las respuestas 063 a 124, 47 evidencias y unos 44 scripts. Lo esencial está en `titan/twohop-nulls`, contenida en `titan/auditoria-hipotesis-2026-10-01`, contenida en `titan/materializacion-h4-guard-2026-10-02`. Incluye:
- **`docs/SECCION-V2-DOS-SALTOS.md` de main es la versión anterior al null anatómico** (323× contra el null de grado). La de la rama dice que el 323× era co-localización: el spread cae a 2,4× y queda la depleción gustativa (10 contra 101,6, z = −78,9).
  - La Tabla 7 es reproducible: 8/8 con el pin `17fc577` (respuesta 003). El script está reconstruido en el PR #26, sin merge.
  - El nulo CP propio reproduce el del erratum: media de 194.890,4 contra 194.974,2, o sea 20,60× con 0/100.
  - **Con ese nulo, la caída de la reciprocidad hacia la salida motora queda explicada por el nulo:** el exceso es 4,30× / 3,67× / 5,55× con ≥1 y 5,11× / 9,57× / 3,94× con ≥5, sin orden. Pero el instrumento dio FAIL (control negativo de la prueba secundaria, 8/20 con CP y ≥1) y **no se firma**.
  - **FWER con los dos nulos:** descendentes → descendentes, → motoras, → cuello y → antena, y óptico ▼ descendentes.
- **H4 fuerte: NO MEDIDA.** La búsqueda pública de ROI 2P está agotada (16/16 sin mapear, rama ROI). H4 débil queda refutada sólo en su alcance estrecho.
  - con CM no vale, porque el seudoconteo domina;
  - pasar el ítem 9 y el 8,6 a `docs/ERRATUM.md` y a `docs/PIVOTE-RECIPROCIDAD.md`;
  - sel_post sobrevive a los nulos de topología y de signo (z = +181 y +6,31; 0/40);
  - el efecto temporal global no sobrevive (39 nulos, p = 0,25);
  - la ventaja de tau compleja no se sostiene (p = 0,60).
1. **Consolidar git:** el linaje de ramas a main (PR #1, #2, #3) o un PR sólo de documentos, y la SECCION-V2 posterior al null anatómico. Decide Abraham.
2. **Cerrar el 003:**
   Depositar en Zenodo lo hace Abraham.
4. **Abiertos para la v2:** NPC por sinapsis o null combinado de grado y neuropilo; ventana y tau de sel_post; Lin región por región; Betzel arista por arista; fila AN y décima clase de la Tabla 5.
```

**Fuente B.** `docs/agents/respuestas/2026-10-11-004-el-repo-del-conectoma-de-punta-a-punta.md` en `main` `41fa8bc`: md5 `8f388b22ceb0ccab01062fe3cfd42034`, 191 líneas, 12996 B. Líneas 71, 72, 83, 85, 91, 93 y 94.

```text
  - el 36× se retira y la reciprocidad pasa a reportarse como rango contra CP (20,59×, 0/40) y MS (47,27×);
  - el 1.559× se retira;
- **LC6 → Giant Fiber:** 0 contra 17,2 ± 3,1 con el null anatómico, z = −5,61, 40/40 (respuesta 065, `docs/BIBLIOTECA-01-giant-fiber.md`).
- **Circuito de plasticidad contra CP:** KC→MBON 7,81×, DAN→KC 8,71×, KC→KC 7,26×, 0/40.
- el 36× (overflow) y el 1.559×;
- la tabla de ruteo como descubrimiento propio (ya había prior art);
- la entrada AMMC directa al GF;
```

**Fuente C.** `results/table7_circuit_null_2026-10-11/run.log` en brain-env (`/workspace/dfc-t7`), sin push: md5 `875295b9888b54f25f91ed7c36b318c7`, 125 líneas. Líneas 3, 19, 57, 63, 67, 105, 111, 114, 120, 121 y 123. El bloque del umbral 1 va de la línea 19 a la 66 y el del umbral 5 arranca en la 67.

```text
[    0.5s] PARAMETROS umbrales=1,5 K=100 falsos=20 seed=20261011 alfa=0.05 pseudo=0.5
[   61.6s] --- nulos umbral=1 ---
[ 1997.6s]   TENDENCIA_PRINCIPAL CP delta=log(rho1/rho3)=-0.2026 IC95=[-0.8201, 0.6345] p_mas=0.6767 p_menos=0.3238 B=2000 rho=4.30x/3.67x/5.55x ordenado=False -> EXPLICADO_POR_EL_NULO
[ 1997.6s]   CONTROL_NEGATIVO CP falsos=20 principal: rechazos=0 esperado=2.00 tope=6.00 | ensemble: rechazos=8 esperado=1.98 tope=5.94 -> FAIL
[ 1997.6s] --- nulos umbral=5 ---
[ 2288.2s]   TENDENCIA_PRINCIPAL CP delta=log(rho1/rho3)=0.4968 IC95=[-0.7549, 3.0829] p_mas=0.1914 p_menos=0.8091 B=2000 rho=5.11x/9.57x/3.94x ordenado=False -> EXPLICADO_POR_EL_NULO
[ 2288.2s]   CONTROL_NEGATIVO CP falsos=20 principal: rechazos=6 esperado=2.00 tope=6.00 | ensemble: rechazos=2 esperado=1.98 tope=5.94 -> PASS
[ 2288.2s] CHEQUEO CONTROL_NEGATIVO FAIL todos los umbrales y nulos
[ 2288.2s] VEREDICTO_TENDENCIA umbral=1 principal: CM=PARCIAL_SIN_ORDEN CP=EXPLICADO_POR_EL_NULO | ensemble: CM=PARCIAL_SIN_ORDEN CP=EXPLICADO_POR_EL_NULO
[ 2288.2s] VEREDICTO_TENDENCIA umbral=5 principal: CM=MAS_ALLA_DEL_NULO CP=EXPLICADO_POR_EL_NULO | ensemble: CM=MAS_ALLA_DEL_NULO CP=EXPLICADO_POR_EL_NULO
[ 2288.2s] VEREDICTO_INSTRUMENTO=FAIL
```

## 5. Archivos generados

- Este archivo. Su md5 va en el Doc y en el chat, porque un archivo no puede contener su propio md5.
- Doc de ClickUp público: https://app.clickup.com/90171457413/docs/2kza6fw5-21057
- Sin cambios en el CONTEXTO ni en ramas.

## 6. NO MEDIDO

- Nada nuevo se midió en esta respuesta.
- La 003 está corrida y sin firmar (FAIL de instrumento). Su script, sus tests y sus logs siguen sólo en brain-env.
- H4 fuerte, el azar por neuropilo de cada sinapsis, Lin región por región, Betzel arista por arista, la fila AN, la causalidad y SparseLTC→DBC3 sobre señal real.
- Review externo del pipeline. Silencio no es aprobación.

--- METODO PROMETEO ---
Máquina: brain-env (lectura de git y del log de la 003; verificación posterior al push); GitHub MCP para el commit.
Artefactos: `docs/agents/respuestas/2026-10-11-005-en-criollo-que-tenemos-entre-manos.md` + Doc de ClickUp https://app.clickup.com/90171457413/docs/2kza6fw5-21057
