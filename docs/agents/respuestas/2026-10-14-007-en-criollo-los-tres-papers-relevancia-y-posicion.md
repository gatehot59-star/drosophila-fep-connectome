# 2026-10-14-007 · En criollo: de qué trata cada paper, si importa y dónde estás parado

**Pedido.** 14-oct 12:24: «En criollo que trata cada papaer. Son de relevancia losndescubrimint9s. Donde me posicionando?»

## Veredicto primero
- **[CONCLUSIÓN] Paper 1 v2:** describe cómo viaja la señal por el cerebro entero. Relevancia **modesta**; su mayor valor es haberse corregido en público.
- **[CONCLUSIÓN] Paper 2:** prueba si el cableado real sirve para un reflejo. Es **el fuerte**: relevancia media a alta para un preprint, por el método y por una respuesta sobria.
- **[CONCLUSIÓN] Paper 3:** quién alimenta las salidas del cerebro. Relevancia **baja a media**: un mapa de consulta con nulos serios.
- **[CONCLUSIÓN, opinión] Posición:** independiente con un método que pocos tienen, todavía sin revisión de pares ni validación en moscas vivas. El escalón siguiente es el Paper 2 revisado por pares.

## Paper 1 (v2, en main, falta el token de Zenodo)
Con el cerebro entero (138.639 neuronas, 15.091.983 conexiones), sin entrenar nada, mide tres cosas [docs/v2/paper1-v2.0.md, resumen]:
1. **Los sentidos van separados.** La inhibición dirigida los mantiene aparte (cancelación contralateral 1,37). Durante el estímulo, la separación se explica en buena parte por la estructura en módulos.
2. **Quién llega a los músculos.** Contra nulos de grado, lo somatosensorial tiene acceso privilegiado (Δ = +0,365). Cuando el nulo conserva el neurópilo, el orden por modalidad se invierte: era ubicación. Lo que sobrevive es una restricción: el gusto toca 10 motoras donde la ubicación predice 101,6 (z = −78,9).
3. **Amplificación después del estímulo.** Depende del modelo: el lineal la reproduce y el LIF suave no.

**Relevancia.** Es descriptivo, en un terreno donde ya publicaron los del consorcio (Lin et al., 2024). Lo que lo distingue es la honestidad: un erratum, el error de 32 bits corregido y un nulo anatómico que dio vuelta la interpretación de la v1. Eso suma credibilidad, no impacto.

## Paper 2 (esqueleto en `titan/paper2-esqueleto-2026-10-14`)
Simula el reflejo de escape (despegar posada, aterrizar o girar en vuelo) sobre el cableado real y lo enfrenta a dos rivales: el mismo cableado barajado y el diseño de la mosca escrito como regla, con los mismos sensores.
- Contra los barajados, el real gana en todas las escalas; los barajados caen 28 y 19 puntos en R2 [2026-10-13-010].
- Contra la regla, el real la alcanza (+0,85 puntos, IC90 [+0,08; +1,51]) pero no la supera por el margen sellado [2026-10-13-010].
- El cerebro entero da lo mismo que R2 (99,913 % de predicciones iguales) [2026-10-14-001].
- En BANC, otra mosca, se repite el 92,4 % de las conexiones de 20 sinapsis o más; falta el nulo [2026-10-14-002].
- Pendiente: H_CONSENSO (si la parte conservada alcanza sola) y H_TAU, corriendo desde las 11:30.

**Relevancia.** Pocos trabajos con modelos de conectoma se enfrentan a la vez a barajados y a una regla con los mismos sensores, todo sellado antes de correr (búsqueda acotada, sin revisión sistemática; NO MEDIDO). El resultado es sobrio: el cableado lleva la función y, simulado, iguala al diseño. No está validado en moscas vivas, como Shiu et al. (2024) y Lappalainen et al. (2024) [2026-10-13-013]. Si H_CONSENSO se sostiene, suma algo que no encontramos hecho: que la parte que se repite entre moscas es la que carga el reflejo.

## Paper 3 (sin esqueleto; decidido en la 006)
Quién alimenta a las descendentes, las motoras y las neurosecretoras [2026-10-10-005 a 009]:
- El cerebro central pone 60 a 73 % de su entrada.
- El óptico casi nada directo (0,45 % de la entrada de las descendentes).
- Lo sensorial directo es marginal (3 a 6 %).
- Con corrección múltiple y nulo regional, lo que aguanta es lo de las descendentes (hacia motoras, cuello y antena). Varias señales resultaron ser ubicación.
- Suma LC6→GF y sel_post (que sobrevive a los nulos de topología y de signo).

**Relevancia.** Es un mapa de consulta útil, no un descubrimiento.

## Dónde estás parado (opinión)
- **Lo que te distingue es el método:** sellar antes de correr, nulos fuertes, regla a mano como rival, git como bitácora y corregirte en público. Eso vale más que cualquier número suelto.
- **Lo que te frena:** sos autor solo, independiente, sin institución, con preprints sin revisión de pares y sin datos de moscas vivas. Hoy el campo te leería como «un independiente serio, a leer con cuidado».
- **El escalón siguiente:**
  1. Depositar la v2.
  2. Cerrar el Paper 2 y mandarlo a bioRxiv y a una revista con revisión (por ejemplo PLOS Computational Biology).
  3. Mostrarles el banco a los autores de FlyWire y BANC.
  4. Una demo chica del reflejo.
- **Para ingresos:** este rigor ya es portafolio para trabajos remotos de evaluación de modelos, datos y reproducibilidad.

## Herramientas y máquina
- brain-env: lectura del resumen de la v2, de la 2026-10-13-013, de 2026-10-10-005 y 009 y del CONTEXTO (md5 `2cfe4814`).
- Sin mediciones nuevas.

## NO MEDIDO
- Una revisión sistemática de la literatura (la afirmación de «pocos trabajos» es de búsqueda acotada).
- H_CONSENSO, H_TAU y el nulo BANC.
- Cómo recibiría el campo los papers.

## Antes de firmar
| Afirmación | Instrumento | ¿Podía dar rojo? | Veredicto |
|---|---|---|---|
| Los números citados son los de git | Lectura de cada fuente citada | Sí | PASA |
| «Pocos trabajos hacen esto» | Búsqueda acotada | Parcial | CONCLUSIÓN, no medición |
| Relevancia y posición | Opinión | No | OPINIÓN declarada |

--- METODO PROMETEO ---
Accion delicada: no (explicación, sin mediciones ni cambios de código).
Maquina: brain-env CPU + conector GitHub.
Artefactos: esta respuesta en main; Doc https://app.clickup.com/90171457413/docs/2kza6fw5-22197
