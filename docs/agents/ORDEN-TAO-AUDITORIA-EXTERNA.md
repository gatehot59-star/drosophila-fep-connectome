# ORDEN DE AUDITORÍA EXTERNA · para TITAN Tao

**Emitida:** 2026-08-25 01:45 (America/Buenos_Aires) por BRAIN, a pedido de Abraham.
**Repo bajo auditoría:** `gatehot59-star/drosophila-fep-connectome`
**Rama con el trabajo reciente:** `titan/twohop-nulls` · **PR abierto:** #2, **sin mergear**.

---

## 0. Por qué existés en este trabajo

Abraham pidió un veedor externo con estas palabras: *«necesitamos un veedor externo, no sea para dónde estás yendo»*. No pidió una revisión de código. Pidió que alguien que no escribió esto diga **si la dirección del proyecto es la correcta**.

**El problema concreto, y es medible:** en las últimas cuatro horas BRAIN se refutó a sí mismo **siete veces**, y las siete tienen la misma forma: **midió bien y después afirmó mal sobre la NOVEDAD o la CAUSA de lo medido.** Las siete las encontró BRAIN, no un tercero. Eso suena a autocorrección sana y **también** es exactamente lo que se ve cuando alguien es el único testigo de su propio trabajo: no hay forma de saber cuántas quedaron sin encontrar.

**Tu mandato es adversarial. No busques confirmar. Buscá el octavo error.**

Y el segundo mandato, que es el que Abraham pidió primero: **decir si el proyecto está yendo a alguna parte.** Tenés permiso explícito para concluir que no.

---

## 1. Contexto mínimo del proyecto, para que no tengas que preguntar

**Quién:** Jorge Abraham Mendieta, trabaja solo. El workspace figura con otro nombre; no es él.

**Qué hay:** tres líneas que se mezclaron durante días y ahora están separadas.

| Línea | Qué es | Estado |
|---|---|---|
| **Paper 1** | *Signal Propagation Properties in the Drosophila melanogaster Connectome*, Mendieta 2026a, en Zenodo desde el 20-mar-2026 | publicado **con errores**; hay un erratum listo que vence el **30-ago** |
| **El motor** | SparseLTC / DualBrain, C99, 1.336 B de `.text` medidos en ESP32 | **es el activo monetizable** |
| **La biblioteca** | hoja de datos de circuitos neuronales con función verificada | **1 entrada**, y hacen falta 3-4 |

**El objetivo declarado:** que el motor no necesite entrenamiento porque su topología viene cableada de fábrica, y que la biblioteca de topologías sea el activo cedible. **El conectoma es la fuente de calibración, no el producto.**

**El deadline duro:** ARC Prize, papers el **8-nov-2026**. Y el erratum a Zenodo, **antes del 30-ago**.

**El riesgo real declarado en el propio plan:** cinco entregables en diez semanas de **una persona**.

---

## 2. Qué leer, y en este orden

No leas todo. Este orden está armado para que a la mitad ya puedas emitir veredictos.

**Bloque A · el estado vivo (empezá acá, son dos archivos)**
1. `docs/agents/CONTEXTO-drosophila-fep.md` — secciones §3 (VALIDADO), §4 (REFUTADO), §5 (NO MEDIDO), §8 (modos de falla).
2. `docs/agents/CONTEXTO-motor.md` — §0.bis, §3 y §4.

**Bloque B · lo que se publica y no se puede arreglar después**
3. `docs/ERRATUM.md` — nueve ítems, va a Zenodo en cinco días.
4. `docs/PIVOTE-RECIPROCIDAD.md` y `docs/SECCION-V2-DOS-SALTOS.md`.

**Bloque C · los instrumentos, con su evidencia al lado**
5. `src/twohop_nulls.py` + `docs/agents/evidencia/2026-08-24-null-anatomico-evidencia-cruda.md`
6. `src/escape_neuropil_null.py` + `docs/agents/evidencia/2026-08-25-escape-neuropil-null-evidencia-cruda.md`
7. `src/compile_gf_full.py` + `docs/agents/evidencia/2026-08-25-compilacion-gf-completo-evidencia-cruda.md`
8. `docs/BIBLIOTECA-01-giant-fiber.md`

**Bloque D · la cronología de los errores, si te queda presupuesto**
9. `docs/agents/respuestas/2026-08-24-057-*` hasta `2026-08-25-069-*`. **Son las siete autorrefutaciones.** Leé los títulos primero y abrí solo las que te sirvan.

**Datos, si vas a re-medir:** el conectoma no está en el repo (política: nada de datasets grandes). `connectivity.parquet` md5 `3d802fd542b5d18570ba1ba0bb0abed9`, `annotations.tsv` md5 `719904abad876c68ace1b5690c9b9b63`, FlyWire FAFB v783. La asignación a neuropilos es pública sin login: **Zenodo 10676866**, archivos `per_neuron_neuropil_count_pre/post_783.feather`.

---

## 3. Los doce claims a atacar, cada uno en forma falsable

Para cada uno: **SOSTENIDO / NO SOSTENIDO / NO MEDIBLE CON LO QUE HAY**, y por qué.

### Prioridad 1 · lo que se publica en cinco días

**C-01. El erratum no le atribuye a nadie un defecto que no tiene.**
Este erratum ya tuvo **dos versiones con ese error exacto**: una corrigía un «1.559×» que no existe en el paper, y otra acusaba a Lin et al. de reportar reciprocidad «solo como cifra global» cuando su Fig. 5c y su Extended Data Fig. 6c la desglosan por neuropilo.
*Cómo atacarlo:* por cada afirmación del erratum sobre un trabajo de terceros, verificarla **en la lista de figuras y suplementos de ese trabajo**, no en su abstract. **Buscar la tercera.**

**C-02. Los nueve ítems del erratum son todos correcciones reales de v1.0.**
*Cómo atacarlo:* cualquier ítem que corrija algo que el paper publicado **no dice** es un error del erratum, no del paper.

**C-03. El erratum no omite un error que sí está en el paper.**
*Cómo atacarlo:* esto es lo más valioso que podés hacer y es donde BRAIN es más ciego. Buscar en el PDF publicado errores que el erratum **no** lista.

### Prioridad 2 · los claims científicos

**C-04. La densidad publicada (0,0074) es un overflow de `int32`.**
Se afirma reproducida a 8 cifras: `15.091.983 / 2.040.764.498 = 0,007395259`.
*Cómo atacarlo:* es aritmética pura y se verifica en un minuto. **Si esto falla, se cae medio erratum.**

**C-05. El resultado de acceso motor a 2 saltos está establecido contra grado y NO contra anatomía.**
Contra un null de grado el spread entre modalidades es 323×; contra uno de neuropilos colapsa a 2,4× y **tres de cuatro signos se invierten**.
*Cómo atacarlo:* el null de neuropilos de BRAIN asigna **un** neuropilo dominante por neurona, cuando el NPC de Lin lo hace **por sinapsis**. ¿Esa simplificación produce el colapso, o el colapso es real? **Es la pregunta técnica más importante de todo el repo.**

**C-06. Lo que sobrevive al null anatómico es que gustativa contacta 10 motoras donde su co-localización predice 102 (z −78,9).**
*Cómo atacarlo:* ¿el null retiene margen real de movimiento en ese bloque? **BRAIN declaró que NO midió la pureza de bloque**, o sea qué fracción de las aristas del bloque pertenece a la clase medida. Sin eso, un `sd > 0` global no garantiza que el estadístico sea testeable **para esa clase**.

**C-07. `LC6 → Giant Fiber = 0` es una exclusión y no geometría.**
Se apoya en que LC6 tiene **5.335** sitios compartidos con el GF contra **4.523** de LC4, que sí conecta con 104, y en que el null predice 17,2 ± 3,1 con mínimo de 40 = 12.
*Cómo atacarlo:* `shared_min_sites` es una **cota de coincidencia de neuropilo**, no de contacto físico. Dos neuronas pueden compartir neuropilo y estar a decenas de micrones. **Las coordenadas están en `annotations.tsv` y BRAIN no las usó.** Un control de distancia puede tumbar esto.

**C-08. La topología define ruteo y ganancia, pero no selectividad temporal.**
Compilado el circuito completo (45.687 aristas con signo): selectividad **1,0631**, el recorte excitatorio da **1,1128**, y el ensemble con signo barajado da **1,1131 ± 0,0185 con 19 de 20 por encima del real**.
*Cómo atacarlo:* `tau = 0,119` es **fijo y único para las 864 neuronas**, y el motor real usa τ **heterogénea**. **La τ heterogénea es el parámetro con más chance de generar selectividad temporal y no se barrió.** Este claim puede ser un artefacto de un modelo demasiado pobre, y si lo es, es una buena noticia que BRAIN no vio.

### Prioridad 3 · el motor, que es el activo

**C-09. La ablación del gate mejora el error entre 21,9× y 108,1× en 4 de 4 tareas.**
Se declara iso-corrida, iso-arquitectura, iso-celda, iso-encoder, 10 semillas.
*Cómo atacarlo:* está en `results/dualbrain_bench.log`. **Verificar que sea realmente la misma corrida** y no dos kernels distintos, que es un error que este proyecto ya cometió.

**C-10. La hipótesis del «96% fijo» NO está testeada, y el brazo W no la testeaba.**
Es la deuda más vieja del proyecto. El brazo W congeló 26 nodos del motor **denso** y **no congeló τ**.
*Cómo atacarlo:* al revés de los otros. **Verificar que el «NO MEDIDO» sea honesto y no una forma de no cerrar algo incómodo.** ¿Se puede testear con lo que hay? Si sí, **el estado correcto es «pendiente barato» y no «no medible».**

### Prioridad 4 · la dirección, que es lo que Abraham pidió

**C-11. El aporte del proyecto es el NULL, no el número.**
El 24-ago BRAIN descubrió que existe un **Cell Type Explorer del snapshot `flywire-fafb:v783b`**, o sea el mismo dataset, que publica la conectividad **completa** por tipo celular hasta socios de una sola conexión. Y concluyó: *«medir un conteo sobre un conectoma público no puede ser el aporte, porque el conteo ya está publicado»*.
*Cómo atacarlo, y acá quiero que seas brutal:*
- ¿Es cierto que el método (null anatómico + métrica de oportunidad + distinción entre tipos de cero) **no está publicado**? Ocho búsquedas de BRAIN no lo encontraron, **y BRAIN ya se equivocó tres veces con esta misma pregunta.**
- Y la pregunta que importa: **¿a alguien le sirve?** Un método para decidir si un cero en un conectoma es sorprendente, ¿es un paper, una nota metodológica, o nada?

**C-12. El plan de 10 semanas es ejecutable por una persona.**
*Cómo atacarlo:* cinco papers, un agente de ARC, tres motivos nuevos de biblioteca y un mecanismo de aprendizaje. Contra el ritmo real observable en el log de git. **Si tu conclusión es que hay que matar tres de los cinco entregables, decilo y decidí cuáles.** Es la clase de decisión que un veedor externo puede tomar y BRAIN no.

---

## 4. Los doce modos de falla conocidos, como checklist

Están en `CONTEXTO-drosophila-fep.md` §8 con su costo medido. **Usá esta lista para barrer el repo: cada uno reincidió al menos una vez después de estar escrito.**

1. Una lista hecha de lo que está a mano solo contiene lo que está a mano.
2. Un null cuyos invariantes incluyen la cantidad medida es un espejo, no un control. **Con su primo: un `sd = 0` por saturación no es lo mismo que por conservación.**
3. Una explicación que encaja no es una explicación medida.
4. Un archivo que no se abrió en el turno no recibe veredicto de vigencia.
5. **Comparar dos cantidades medidas con criterios distintos. Seis veces.** Última: `cell_type` contra `hemibrain_type` para DNp09, que da 32 aristas contra 170.
6. **Un test que no puede dar rojo no es un test. Cuatro veces.**
7. Lo que no está commiteado se pierde justo cuando más falta hace.
8. Un erratum aritmético no arregla un problema de framing.
9. Una referencia incompleta se completa mal en el turno siguiente.
10. **Un claim de novedad se verifica contra las FIGURAS del trabajo previo, no contra su abstract.**
11. **Verificar el sujeto no alcanza: hay que verificar la ESCALA a la que la explicación rival es cierta.**
12. Un ratio contra un null necesita saber cuánto da un sujeto **cualquiera** contra ese mismo null.

**Y el que no está en la lista y debería:** el 24-ago BRAIN leyó una columna de **localización anatómica** de una tabla ajena como si fuera de **origen de señal**, y de ahí sacó que el Giant Fiber recibe más entrada mecanosensorial que visual. La entrada sensorial directa es el **2,0%**. **Fijáte si ese patrón — leer mal una columna de una fuente externa — aparece en otro lugar del repo.**

---

## 5. Formato obligatorio de tu informe

Un solo archivo, en la rama `titan/auditoria-tao`, en `docs/agents/AUDITORIA-EXTERNA-TAO.md`. **No toques `main`. No mergees el PR #2. No borres ni sobreescribas ningún archivo existente.**

```
# AUDITORIA EXTERNA · <fecha>

## 0. VEREDICTO EN UNA LINEA
<¿este proyecto va a alguna parte? si / no / va pero no adonde cree>

## 1. LO QUE HAY QUE PARAR AHORA
<solo lo que se rompe si se publica el 30-ago. Si no hay nada, decirlo.>

## 2. TABLA DE VEREDICTOS
| claim | veredicto | evidencia | como lo verifique |
<los doce, sin saltear ninguno. Si no pudiste, poner NO MEDIBLE y por que.>

## 3. EL OCTAVO ERROR
<lo que BRAIN no encontro. Si no encontraste ninguno, decirlo explicitamente:
 eso tambien es informacion, y vale.>

## 4. SOBRE LA DIRECCION
<C-11 y C-12. Que matar, que priorizar, en que orden, con criterio nombrado.>

## 5. LO QUE NO PUDE AUDITAR
<y por que. Un hueco declarado vale mas que un veredicto inventado.>

## 6. EVIDENCIA CRUDA
<comandos, salidas verbatim, sin resumir. Si no corriste nada, decirlo.>
```

**Reglas del informe, y son las mismas que BRAIN incumplió:**

- **Cada veredicto lleva su evidencia citada:** archivo y línea, comando y salida, o URL exacta. **Un veredicto sin evidencia se descarta entero**, no se descuenta.
- **Si corrés algo, la salida cruda va verbatim y sin recortar.** Un resumen de una corrida no es un recibo.
- **Distinguí «mal» de «no medido».** Son estados distintos y confundirlos es el error más caro de este proyecto.
- **No arregles nada.** Sos auditor. Si ves un fix obvio, escribilo como recomendación y no lo apliques.
- **Tenés permiso explícito para decir que BRAIN se equivocó en la dirección entera.** Ese es el trabajo.

---

## 6. Lo que NO tenés que hacer

- **No mergear nada.** El merge es decisión de Abraham, siempre.
- **No publicar en Zenodo.** Eso es de Abraham y solo de Abraham.
- **No tocar `main`**, ni borrar, ni sobreescribir trabajo de BRAIN.
- **No gastar cuota de Kaggle** sin decirlo antes en el informe.
- **No auditar MUDH-Mobile ni icca-engine.** Son otros proyectos, otro repo, fuera de alcance.
- **No reescribir el paper ni el erratum.** Señalá y pará.

---

## 7. Presupuesto y prioridad

Si solo podés hacer una cosa: **C-01, C-02 y C-03**, el erratum, porque vence en cinco días y una vez en Zenodo tiene DOI y no se borra.

Si podés hacer dos: agregá **C-05**, el null anatómico, porque de eso depende si la sección nueva del paper se publica o se tira.

Si podés hacer tres: **C-11**, la dirección, porque es lo que Abraham pidió y nadie más puede contestarlo.

**Lo demás es bonus.** Y un informe corto con tres veredictos bien fundados vale más que doce veredictos flojos.

---

## 8. Una advertencia sobre mí, para que la uses

BRAIN escribió esta orden. **Eso la hace sospechosa por construcción:** está armada eligiendo qué mirar, y el sesgo de selección es precisamente el hueco que un instrumento propio no cubre.

**Los doce claims son los que BRAIN cree que son atacables. El octavo error, por definición, no está en esa lista.**

Así que tenés permiso, y de hecho el pedido explícito, de **ignorar la §3 entera y auditar lo que te parezca**. Si al final tu hallazgo más importante es algo que esta orden no menciona, **eso solo es la prueba de que la auditoría valía la pena.**
