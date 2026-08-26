# EVIDENCIA CRUDA · 2026-08-26 · entrar a los tres tracks de ARC Prize 2026

**Pedido:** «Sí, entrá a los tres tracks ahora.»

**Resultado: NO se puede por API, y está medido, no supuesto.** Abajo las cuatro
mediciones, incluida la que falsa mi propia hipótesis intermedia.

**Instrumento:** `gateway build.run` sobre `brain-env` (API de Kaggle v1, Bearer) y
`gateway playwright` (navegador real).

---

## 1. Los tres tracks, con slug exacto y deadline

```
GET /competitions/list?search=arc-prize-2026   HTTP 200
  https://www.kaggle.com/competitions/arc-prize-2026-arc-agi-3     2026-11-02  entered=false
  https://www.kaggle.com/competitions/arc-prize-2026-arc-agi-2     2026-11-02  entered=false
  https://www.kaggle.com/competitions/arc-prize-2026-paper-track   2026-11-09  entered=false
```

**Los tres existen, están abiertos, y `entered=false`.** Los slugs quedan fijados aquí
para no volver a adivinarlos: `arc-prize-2026-arc-agi-3`, `arc-prize-2026-arc-agi-2`,
`arc-prize-2026-paper-track`.

Y el deadline del paper track es **7 días después** que los otros dos: 9 de noviembre
contra 2 de noviembre.

---

## 2. ¿Hay endpoint de entrada? Se prueban las vías plausibles

```
POST  /competitions/arc-prize-2026-arc-agi-3/join           HTTP 404  (html de Kaggle)
POST  /competitions/join/arc-prize-2026-arc-agi-3           HTTP 404  (html de Kaggle)
POST  /competitions/arc-prize-2026-arc-agi-3/rules          HTTP 404  (html de Kaggle)
PUT   /competitions/arc-prize-2026-arc-agi-3/rules/accept   HTTP 400  (cuerpo vacio)
GET   /competitions/data/list/arc-prize-2026-arc-agi-3      HTTP 200  (lista los archivos)
```

El **400** del `PUT` parecía un hallazgo: un 400 y no un 404 sugiere que el endpoint
existe y que la request estaba mal armada. Se probó con cuerpo JSON, con query param y
con otra forma de ruta: **400 en las cuatro**.

## 3. 🔍 EL CONTROL, que falsa mi propia hipótesis

```
PUT /competitions/inventado-xyz-123/rules/accept    HTTP 400
PUT /competitions/pepe/nada/de/nada                 HTTP 400
PUT /xyz/abc                                        HTTP 400
```

**`PUT` a CUALQUIER path devuelve 400.** No es un endpoint que existe con la request mal
armada: es que la API no acepta `PUT` y responde 400 genérico. **Mi lectura del 400 era
falsa, y el control la mató en una llamada.**

Sin ese control habría reportado «hay un endpoint de aceptación y le falta el cuerpo
correcto», que habría mandado a alguien a buscar una firma de API que no existe.

## 4. La prueba POSITIVA: Kaggle lo dice con todas las letras

```
GET /competitions/data/download-all/arc-prize-2026-arc-agi-3
HTTP 403
{"code":403,"message":"You must accept this competition's rules before you'll be able to download files."}
```

Esto no es una inferencia por ausencia de endpoint: es Kaggle **declarando el requisito**.
Aceptar las reglas es previo a todo, y la API no expone cómo hacerlo.

## 5. La última vía: el navegador real

```js
await page.goto('https://www.kaggle.com/competitions/arc-prize-2026-arc-agi-3/rules');
// Page Title: ARC Prize 2026 - ARC-AGI-3 | Kaggle
```

```json
{ "logueado": false,
  "tieneJoin": true,
  "primeros": "... search Sign In Register Kaggle uses cookies from Google ..." }
```

**El navegador del gateway NO tiene sesión de Kaggle.** El botón de aceptar está en la
página (`tieneJoin: true`) y no hay usuario con el cual apretarlo.

---

## 6. Y el límite que NO es técnico

Hay que distinguir «no tengo la herramienta» de «el método me lo prohibe», y acá son
**las dos cosas**:

- **Técnico:** no hay endpoint de API y el navegador no tiene sesión.
- **De método:** aceptar los términos de una competencia es una **declaración legal de la
  persona**. El texto de las reglas abre con *«ENTRY IN THIS COMPETITION CONSTITUTES YOUR
  ACCEPTANCE OF THESE OFFICIAL COMPETITION RULES»*. Aun con sesión disponible, **no se
  acepta en nombre de nadie.** Es el caso 1 de P-01: acción irreversible que compromete a
  un tercero.

**Así que el límite es correcto y no se busca la vuelta.** Son tres clicks de Abraham.

---

## 7. Los tres links exactos, para que sean tres clicks y no una búsqueda

```
https://www.kaggle.com/competitions/arc-prize-2026-arc-agi-3/rules
https://www.kaggle.com/competitions/arc-prize-2026-arc-agi-2/rules
https://www.kaggle.com/competitions/arc-prize-2026-paper-track/rules
```

En cada una: botón **Join Competition** o **I Understand and Accept**.

**Con qué cuenta:** las dos tienen los tokens vivos y 27,9 h / 29,3 h de GPU libres. Si
va a haber una sola cuenta oficial de evidencia, conviene **`abrahammendieta`**, que es la
que lleva su nombre. La otra sirve igual como capacidad de cómputo.

**Cómo verifico que quedó hecho, sin preguntarle:** el flag `userHasEntered` pasa a `true`
en `/competitions/list?search=<slug>`, y `download-all` deja de dar 403. Los dos son
medibles desde acá en una llamada.

---

## 8. NO MEDIDO

- **No se probó hacer login en el navegador del gateway.** Se descarta por método, no por
  incapacidad: implicaría manejar sus credenciales de sesión de Kaggle, que es distinto de
  usar un token de API de solo trabajo.
- No se buscó un endpoint de aceptación en la API **v2** de Kaggle, si existe.
- El requisito de aceptar reglas se midió sobre **arc-agi-3**; se asume igual para los
  otros dos por ser la misma plataforma, pero **no se midió en cada uno**.
- No se verificó si hay restricción de país o de edad en las reglas que pudiera bloquear
  la entrada. Eso vive en el texto legal y **no se leyó completo**.
