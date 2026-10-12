# 2026-10-12-006 · En criollo: la mosca sirve de mapa y de reflejo chico, no de cerebro entrenable

Doc: https://app.clickup.com/90171457413/docs/2kza6fw5-21417

**Veredicto (síntesis, sin corrida nueva):** tenemos un laboratorio honesto que saca circuitos de la mosca, los prueba contra sus barajados y dice cuándo sirven. Ya dio un paper casi listo para la v2 y un reflejo de escape que anda en simulación. El potencial existe pero es más angosto que «todas las capacidades son reutilizables»: la mosca sirve de mapa y de reflejo chico y fijo, no (hasta ahora) de cerebro entrenable mejor que lo clásico. Orden propuesto: la v2 del paper, líneas etiquetadas en Actions y, si pagan, el reflejo en C99/Q15.

## 1. Pedido

«EN CRIOLLO QUE TENEMOS ENTRE MANOS , TIENE PORENCIAL, ACIA DONDE VAmos???» (10:35).

## 2. Herramientas y máquina

- GitHub, lectura: lista de commits de main (HEAD `5405f03`, sin cambios desde el cierre de la 005) y `00-ENTORNOS-Y-CAPACIDADES.md` en `5405f03` (foto medida el 26 y 27-ago).
- El CONTEXTO y la 005 son los de `5405f03`.
- Skills ANDROMEDA y BITACORA-EN-GIT recargados y aplicados.
- Ninguna corrida y ninguna máquina de cómputo. Sin cuota ajena.
- ClickUp: un Doc nuevo.

## 3. Qué se midió

Nada nuevo. Es síntesis de lo medido, cada punto con su respuesta de origen.

**Qué tenemos (medido):**
1. Paper casi listo para la v2: Tabla 7 reproducible 8/8 con el pin `17fc577`; erratum de 9 ítems; control de las salidas con cinco afirmaciones que aguantan FWER con los dos nulos (10-oct, 005 a 009). Zenodo tiene sólo la v1.0.
2. Reflejo de escape de 26 neuronas de FlyWire: sin entrenar ya escapa (010); con la τ líquida plena entrenada llega a 0,98 (014); le gana a su barajado por lateralidad (010) y por cableado fino fuera del techo (011); con la plena gana en promedio (88%, p 0,0002) pero no en cada entrenamiento (015). 1.378 parámetros, unos 5,5 KB en float32.
3. Catálogo: 10 de 10 predicciones de literatura en el cableado; aterrizaje y escape hablan directo a las descendentes con 4.000 y 3.520 B internos (2026-10-12-002).
4. Tubería SparseLTC → DBC3 de punta a punta (003), sin ventaja medida sobre LSTM ni sobre la máquina de estados (003 y 004).
5. Método con falsadores: barajados SL, S y T, controles, pre-registro y md5 en clon fresco (010 a 015 y 2026-10-12-002 a 005).

**Qué no anduvo (medido):** en tareas genéricas paga la sparsity, no la mosca (008); nadie aprende memoria de 90 pasos y la máquina de estados gana (004); con entrada por tipo y lector entrenado el cableado no paga y el rival clásico gana 6 de 6 (005); el reflejo a mano rinde 0,9167 sin entrenar (011); `swarm/` no sale del conectoma y escapa hacia la amenaza (007).

**Potencial (opinión, no medición):** la mosca como mapa (qué circuito, a qué descendente, cuántos bytes) y como reflejo chico y fijo donde importan el lado y el cableado fino; la receta de certificar contra el barajado antes de usar; un nicho posible de reflejos de pocos KB en microcontrolador sin entrenar en el dispositivo (NO MEDIDO en hardware). DualBrain y DBC3 no se ganaron todavía un lugar en la cadena de la mosca.

**Hacia dónde (recomendación, decide Abraham):**
1. La v2 del paper: depositar en Zenodo es una llamada de API con un token `deposit:write` que genera Abraham.
2. Líneas etiquetadas (cada descendente con su umbral dispara su acción) con la entrada de la 005, contra SL y T, en Actions (repo público: gratis, 11,6× más rápido, VM limpia; instalar numpy con `setup-python`).
3. Si pagan: el reflejo en C99/Q15 con paridad contra numpy, `.text` y latencia en Actions x64 y arm64, y tamaño para ESP32 con el cross del taller; antes, arreglar `swarm/`.
4. Estacionar: DBC3 contra LSTM con entrenamiento largo, antimisiles y «todas las capacidades son reutilizables» como afirmación.

## 4. Evidencia cruda (verbatim)

Del CONTEXTO en `5405f03`:

```
- **FWER con los dos nulos:** descendentes → descendentes, → motoras, → cuello y → antena, y óptico ▼ descendentes.
- **En criollo (015):** tenemos un reflejo de escape de 26 neuronas sacado de FlyWire que funciona en simulación desde el día cero y llega a 0,98 entrenando sólo la τ líquida plena.
**En tareas genéricas paga la sparsity, no la mosca.**
- **Letra chica:** el reflejo escrito a mano sin LC6 le gana a la mosca (0,9167; latencia 10 contra 14).
**H3: la máquina de estados (0,7663) le gana a DBC3 en los dos.**
- **VEREDICTO_GLOBAL: NO PAGA (PIERDE en SILENCIOSA).**
- **El rival clásico crudo (ridge sobre las 24 entradas) le gana en 6 de 6** (0,8750 a 0,9906 contra 0,6878 a 0,8628; p ≤ 1e-66).
```

De `00-ENTORNOS-Y-CAPACIDADES.md` en `5405f03`:

```
- **`xtensa-esp32-elf-gcc`** en `/opt/xtensa-esp-elf/bin`: el compilador cruzado de ESP32
**El runner es 11,6 veces más rápido que `brain-env` en el mismo trabajo, con el mismo script, medido.**
> **Actions con runners estándar es GRATIS e ILIMITADO en repositorios PÚBLICOS.**
1. **Compilar C/C++ nativo Y EJECUTARLO**
5. **Depositar el erratum en Zenodo.** `POST /api/deposit/depositions` responde 403 sin token: es **una llamada de API**, no una tarde. Falta solo un token con `deposit:write`.
```

## 5. Archivos

- Esta respuesta.
- `docs/agents/CONTEXTO-drosophila-fep.md` reescrito: encabezado, «En criollo (2026-10-12-006)», espera de decisión, próximos pasos 7, fuentes, NO MEDIDO y método.

## 6. NO MEDIDO

- Hardware: placa, energía y latencia en ESP32. Ninguna placa figura en el inventario; un emulador de Espressif en el taller no se probó.
- El inventario no se re-midió hoy (foto del 26 y 27-ago), incluido el cross de ESP32.
- Líneas etiquetadas; señal biológica registrada; fisiología de LPLC4; condiciones fuera de las entrenadas.
- El potencial de producto es opinión.

## Antes de firmar

No se firma ningún verde nuevo: los números son de respuestas ya cerradas y el potencial va marcado como opinión.

## QA

CONTEXTO leído (HEAD verificado), inventario abierto con una llamada real, respuesta y contexto commiteados antes del chat, Doc creado. Review externo no pedido.

--- METODO PROMETEO ---
Máquina: ninguna corrida (síntesis; lecturas en GitHub)
Artefactos: docs/agents/respuestas/2026-10-12-006-en-criollo-la-mosca-sirve-de-mapa-y-de-reflejo-chico-no-de-cerebro-entrenable.md + https://app.clickup.com/90171457413/docs/2kza6fw5-21417
