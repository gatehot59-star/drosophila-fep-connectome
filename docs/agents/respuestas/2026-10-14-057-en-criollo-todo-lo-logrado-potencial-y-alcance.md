# 2026-10-14-057 · En criollo, todo: el cableado de la mosca importa y lo medimos sin trampa, pero no le gana a un lector clásico; el potencial está en el método, los papers y los reflejos chicos, y el alcance es la simulación

**Fecha:** 2026-10-17, 09:25 (America/Buenos_Aires)
**Doc:** https://app.clickup.com/90171457413/docs/2kza6fw5-23797

## Pedido

«en criollo todoo lo que lograste potencial y alcance» (Abraham, 17-oct 09:06), con el Doc de la 2026-10-12-011 («No es la neurona…») seleccionado. Lo leo como la síntesis completa del laboratorio del conectoma: Paper 1, el banco de la mosca, la mosca entera, la estructura y la línea SparseLTC/DBC3. Pide qué potencial tiene y hasta dónde llegan las afirmaciones. En potencial reemplaza a la 2026-10-14-018, y amplía la 056, que cubría sólo la mosca entera. Sin corridas nuevas.

## Veredicto primero

- **[CONCLUSION] En una frase:** el cableado exacto de la mosca importa, y lo medimos sin trampa.
  - Les gana a sus barajados en cuatro escalas, y su patrón de inhibición se repite en dos moscas distintas.
  - Pero no es un cerebro mejor que lo clásico: un lector clásico entrenado sobre las mismas entradas le gana por 5 puntos, y la motora del azúcar sólo salió con la neurona de Shiu, que dispara.
  - El potencial está en el método, en tres papers y en reflejos chicos. El alcance, por ahora, es la simulación.
- **[MEDIDO] Lo publicado:** el Paper 1 v2.0 está en Zenodo (DOI 10.5281/zenodo.23393412, 15-oct), con el erratum de la v1.0 adentro.
- **[NO MEDIDO] Lo que no tenemos:** nada fuera de simulación (ni cámara, ni placa, ni robot) y ninguna validación propia contra moscas vivas.

## Lo logrado, en seis bloques

### 1. Paper 1, publicado

- [MEDIDO] La v2.0 está en Zenodo con DOI propio, como versión 2.0 del concepto de la v1.0. El PDF y el erratum tienen md5 sellados (6e849bf2 y 05052e6e).
- [MEDIDO] La v2.0 corrigió en público errores de la v1.0: el erratum los lista, entre ellos cinco referencias con datos mal.
- [MEDIDO] Su sección nueva de dos saltos pasó por el nulo anatómico antes de salir:
  - el 323× del borrador era ubicación, y quedó en 4,2×;
  - lo firme es la depleción gustativa (10 contra 101,6 esperadas).
- [CONCLUSION] Letra chica que dejó la auditoría de Fable: el título lleva la amplificación temporal, que descansa en cinco realizaciones y en una Tabla 8 que no se reprodujo. Decidís vos si va una v2.1 que la reproduzca o la saque del título.

### 2. El banco sellado (el método)

- [HECHO] **Cómo trabaja:**
  - cada pregunta se escribe y se sella en git antes de tener el instrumento;
  - después van prueba, humo y corrida;
  - se lee con las bandas selladas.
- [HECHO] **Los rivales fijos:**
  - barajados del cableado (de pesos, de destinos, de grado y de tipos);
  - la regla a mano, que es el plano de la mosca con los mismos sensores;
  - lectores clásicos entrenados;
  - en la mosca entera, el modelo de Shiu.
- [HECHO] Se repite en dos o tres máquinas (brain-env, Actions, Kaggle). Pasó por dos auditorías externas (Tao y Fable 5.1): las dos encontraron cosas, y cambiaron cómo escribimos.
- [CONCLUSION] Varias veces dio en contra de lo que yo esperaba (H_LECTOR_CABLEADO, H_UMB_MN9) y en contra de lo que nos convenía (H_RIVAL, H_CONSENSO). Por eso le creo cuando da a favor.

### 3. Si el cableado sirve (material del Paper 2)

- [MEDIDO] **El cableado real pesa en las cuatro escalas.** Con 46 neuronas, 1.504, 33.489 y el cerebro entero de 138.639, les gana a sus barajados.
  - En R2 (33.489 neuronas) acierta 0,9465; el mejor de 100 barajados, 0,839.
  - Barajado, pierde de 19 a 28 puntos en promedio.
- [MEDIDO] **Contra el plano de la mosca, lo alcanza.**
  - R2 queda +0,85 puntos arriba, por menos del margen de 1.
  - El cerebro entero decide igual que R2 en el 99,913 % de los ensayos.
  - Lo supera (+1,78) sólo eligiendo las constantes de tiempo con el entrenamiento. Si a la regla le das la misma perilla, la ventaja baja a +1,19 y queda SIN_DECIDIR.
- [MEDIDO] **Contra un lector clásico, pierde.** Un ridge o una red chica entrenados sobre las mismas 564 entradas aciertan de 0,988 a 0,999; la mosca, de 0,941 a 0,947 (H_RIVAL).
- [MEDIDO] **Pero sus 6 descendentes comprimen casi todo.**
  - El mismo ridge, leyendo sólo las trazas de las 6 descendentes, usa 240 rasgos contra 22.560 del ridge crudo y queda a 0,3 puntos (H_LECTOR_CERCA).
  - Con ese lector, el cableado real les gana a sus 80 barajados, también con constantes de tiempo que nadie eligió (H_LECTOR_CABLEADO y H_TAU_LIBRE).
- [MEDIDO] **Las conexiones fuertes solas** (15 % de las aristas, 57 % de las sinapsis) les ganan a sus barajados, pero pierden 4,59 puntos contra R2 entero: las débiles ponen algo. La corrida de H_DEBILES, que mide si eso es por cuáles son o por cuántas, quedó INVALIDA por infraestructura (Actions perdió 2 de 60 celdas) y falta relanzarla.

### 4. La mosca entera contra Shiu (045 a 055)

- [MEDIDO] Reprodujimos exacto el modelo de Shiu (Nature 2024): azúcar → MN9, la motora de la trompa, en 30 de 30 ensayos, dos veces.
- [MEDIDO] Con nuestra neurona sale su mapa, pero no su motora:
  - prende 172 de sus 321 neuronas (J 0,366), y ningún barajado de 80 pasa de 103;
  - la compuerta líquida no aportó, porque el estado es estable;
  - un umbral global tampoco.
- [MEDIDO] El modelo de Shiu pasa limpio los 40 barajados de destinos que nos frenaban: 0 espigas en 400 ensayos. Eso incluye a k32, el único con un atajo directo de 11 sinapsis del azúcar a MN9.
- [CONCLUSION] A la motora parece faltarle una neurona que acumule y dispare. Es lectura, no medición: la prueba es sellar una celda propia así.

### 5. Estructura y reuso (material del Paper 3)

- [MEDIDO] **Quién manda las salidas.** Con nulos de tamaño y de región, la corrección más dura deja dos cosas en pie:
  - las descendentes mandan a descendentes, motoras, cuello y antena;
  - lo óptico casi no llega directo a las descendentes.
- [MEDIDO] **H_REUSO, en dos moscas:** el mismo módulo de inhibición sirve a varios comandos distintos.
  - En FlyWire, 698 inhibitorias contra 128,6 del nulo.
  - En BANC, otra vez: 419 contra 11,0.
  - Falta el nulo más estricto, el que conserva la clase del destino.
- [MEDIDO] BANC conserva las conexiones fuertes de R2: el 92,4 % de las de 20 sinapsis o más. Letra chica: sólo se pudo evaluar el 19,4 % de las aristas.
- [CONCLUSION] La pregunta grande del Paper 3 ya la contesta BANC (Bates, Nature 2026). Lo propio es el nulo regional, así que conviene reencuadrarlo; la decisión es tuya y está pendiente.

### 6. Herramientas y la línea SparseLTC/DBC3

- [MEDIDO] **Topo:** un reflejo se escribe en renglones (el escape, en 18) y da exacto lo mismo que la regla (12 de 12). Cada flecha se chequea contra FlyWire.
- [MEDIDO] **Reflejo chico de escape (26 neuronas):**
  - entrenando sólo las constantes de tiempo líquidas llega a 0,98;
  - le gana a su control con los mismos parámetros (0,985 contra 0,945);
  - contra sus barajados gana en promedio (88 %), pero no en cada entrenamiento;
  - el reflejo escrito a mano saca de 0,91 a 0,92 sin entrenar.
- [MEDIDO] **SparseLTC y DBC3:**
  - SparseLTC corre el cerebro entero en Actions, con su ecuación en numpy disperso (no el runtime de Mojo/C++).
  - En `mojo-absoluto`, SparseLTC empata 48 de 48 con el control lineal (HC-2), y DBC3 aprende más rápido en una tarea (AULC 0,823 contra 0,635, HC-3b).
  - En la mosca, el acople SparseLTC → DBC3 anduvo (1,0000), pero empató con una LSTM.
  - En memoria larga ninguna red aprendió, y una máquina de estados de dos líneas les ganó.
- [CONCLUSION] DBC3 y DualBrain todavía no se ganaron un lugar en la cadena de la mosca; la líquida plena sí, en el reflejo chico.

## Por qué no choca con «No es la neurona», el Doc que seleccionaste

- [MEDIDO] El 12-oct (2026-10-12-011), en el motivo de 28 neuronas, lo que fallaba no era la neurona.
  - El recorte llevaba el 2,96 % de la entrada de sus descendentes y nada de su inhibición.
  - Los factoriales lo confirmaron: con más cableado real, la simulación alcanza al plano (R2).
  - La inhibición, en cambio, no quedó clara: en el primer factorial ayudó sólo con una amplitud, y en el segundo no tuvo efecto claro.
- [CONCLUSION] Ayer, en el cerebro entero (sin recorte), queda otra cosa: para la motora del azúcar, el tipo de neurona.
  - Son sujetos distintos: un reflejo visual con lector entrenado, contra el reclutamiento del azúcar sin lector. Las dos lecturas pueden ser ciertas a la vez.
  - El orden fue: primero se arregló el recorte, y lo que queda ahora es la neurona.

## Potencial (opinión, no medición)

- **Ciencia, lo más firme:**
  - **Paper 1:** publicado.
  - **Paper 2:** un mensaje honesto y defendible. El cableado exacto es necesario para sus reflejos (barajado pierde de 19 a 28 puntos) y sus descendentes comprimen la tarea casi sin pérdida, pero no es el mejor lector de sus entradas. Se suma el capítulo de la mosca entera. Es publicable en un nicho, por el método.
  - **Paper 3:** reencuadrado como prueba de los lazos locales de BANC con nulo regional.
  - **H_REUSO** es lo más biológico que tenemos: un módulo que se repite entre comandos y entre moscas.
- **Herramientas:**
  - El banco sellado sirve para evaluar cualquier modelo contra sus barajados y contra una regla simple. Es un servicio vendible: evaluación y reproducibilidad.
  - Topo sirve para escribir y chequear planos de reflejos.
- **Aplicaciones:**
  - **Producto.** El banco ya dijo qué conviene: lo clásico. Un lector lineal sobre los sensores gana en acierto, y la regla del plano es la más barata. La mosca aporta el plano (qué sensor va a qué comando), no la pieza.
  - **Portero sensorial.** Con eso se arma un aviso de choque por lado entre el sensor y la IA. Su costo en placa (bytes, energía, latencia) está NO MEDIDO.
  - **Simulador barato.** Corre el cerebro entero en segundos por corrida, para filtrar hipótesis antes de ir al modelo de espigas.
- **Para vos, profesionalmente:** te posiciona como ingeniero de evaluación de modelos y reproducibilidad (pre-registro, nulos, réplica). Los papers no pagan a corto plazo (2026-10-14-008).

## Alcance (hasta dónde llega lo que afirmamos)

- **Todo es simulación:** entradas sintéticas por tipo de neurona, nunca un píxel, y cero hardware.
- **Un solo conectoma con función** (FlyWire v783). BANC entra sólo para estructura y reuso; MANC y hemibrain no están bajados.
- **La vara externa es el modelo de Shiu**, que él validó con optogenética. Nosotros coincidimos con un modelo validado, no con una mosca viva. El único contacto con datos vivos (H4, los registros de Aymanns) no mostró generalización: balanced accuracy 0,50.
- **Pocos reflejos:** escape, aterrizaje, giro y azúcar → trompa.
- **Estadística:** muchas p están en el piso de sus nulos (1/41, 1/201), y repetir en dos máquinas prueba determinismo, no corrección.
- **Lo que no es:** ni un cerebro de mosca que aprende mejor que lo clásico, ni una neurona nueva (la líquida es de la familia LTC), ni una IA nueva.
- **Cómputo:** el cerebro entero corre gratis y en minutos en Actions (el repo es público) y a 0,026 s por ensayo en una T4 de Kaggle. brain-env es lento: tiene 2 núcleos.

## Qué destraba más (el orden de la 056)

1. El cotejo de la réplica de H_LECTOR: ya terminó y es condición para Zenodo (2026-10-14-042).
2. Sellar una celda de SparseLTC que acumule y dispare, contra los mismos 80 barajados.
3. Reescribir el Paper 2 alrededor de H_RIVAL, H_LECTOR y la mosca entera.
4. Revocar el token de Zenodo.

## Herramientas y máquina

- **Conector GitHub:**
  - commits de `main`: nada nuevo desde 0db0a79;
  - commits de `mojo-absoluto`: el último es 613bf49, del 11-oct;
  - CONTEXTO completo, md5 2da204c6.
- **brain-env:** clon fresco de `main`; lectura de las respuestas 018, 009, 031 y 035 y del `00-ENTORNOS-Y-CAPACIDADES.md`; sondeo del taller; prueba del parche en una copia.
- **ClickUp:** lectura del Doc de la 2026-10-12-011.
- **Sandbox de ClickUp:** redacción y parche.
- **Actions y Kaggle:** nada. No se gastó cuota ajena.
- **Escrituras:** este archivo, el parche del CONTEXTO con su workflow, y el Doc.

## Qué se midió hoy

- **Sondeo de máquinas** (17-oct, 09:07):
  - brain-env: x86_64, 2 núcleos, 7 GB de RAM con 4 disponibles, `/workspace` de 406 GB con 78 GB libres (80 % usado), Python 3.12.14, gcc sí, g++ no;
  - sandbox de ClickUp: 4 núcleos, 7 GB, Python 3.12.15, gcc, g++ y node, sin internet.
- **Contra el inventario:** `00-ENTORNOS-Y-CAPACIDADES.md` (foto del 26-ago) dice 156 GB libres, y gana lo medido. El archivo dice ser idéntico en los cuatro repos y actualizarse en los cuatro a la vez, así que no lo toqué en esta síntesis: queda anotado en el CONTEXTO y propuesto.
- **Corrección al CONTEXTO:** su encabezado todavía decía que Zenodo tenía sólo la v1.0. El parche lo pone al día con la v2.0 publicada (2026-10-14-035) y el PR #27 mergeado (2026-10-14-004).
- **Ningún número científico nuevo:** todos salen del CONTEXTO y de las respuestas citadas.

## Evidencia cruda

Sondeo en brain-env (`date -u; uname -m; nproc; free -g; df -h /workspace; python3 --version; which gcc g++ git curl`), exit 0:

```
Sat Oct 17 12:07:33 UTC 2026
x86_64
2
               total        used        free      shared  buff/cache   available
Mem:               7           3           1           0           3           4
/dev/sda4       406G  309G   78G  80% /workspace
Python 3.12.14
/usr/bin/gcc /usr/bin/git /opt/mamba/bin/curl
0db0a79 2026-10-16 23:41:09 +0000
2da204c6a3982aea4c448f6d466c8efe  docs/agents/CONTEXTO-drosophila-fep.md
```

Sondeo en el sandbox de ClickUp (`nproc; free -g; python3 --version; which gcc g++ git node npm javac`), exit 0: `4`, `Mem: 7 0 6 0 0 7`, `Python 3.12.15`, `/usr/bin/gcc /usr/bin/g++ /usr/bin/git /usr/local/bin/node`.

Inventario, líneas 34 y 35 de `00-ENTORNOS-Y-CAPACIDADES.md` (md5 63cbc77c3f46f8281f73cae234f29e41), sin las negritas: la fila de RAM dice «8 GB (~1,7 GB disponible)» y la de disco, «156 GB libres, PERSISTENTE».

Parche del CONTEXTO, probado en una copia del de `main` (0db0a79) en brain-env, con el mismo md5 del script en los dos lados (8bf9c90c342b52982256d1c8eed08841):

- primera pasada: `md5 antes 2da204c6a3982aea4c448f6d466c8efe`, cinco anclas con `ANCLA apariciones=1`, `md5 despues 3ebec5a8dad3c2ae537e6d16037e651c`, `PARCHE OK`;
- segunda pasada: `ANCLA apariciones=0` y `ABORTA: ancla no unica`, con el md5 sin cambios (3ebec5a8);
- la línea 5 queda: «**Base vigente del paper:** la v2.0 está publicada en Zenodo (DOI 10.5281/zenodo.23393412, 15-oct, 2026-10-14-035)…».

## Fuentes

- CONTEXTO (md5 2da204c6a3982aea4c448f6d466c8efe, `main` 0db0a79).
- Respuestas:
  - 2026-10-12-011: no es la neurona;
  - 2026-10-13-002, 005, 007 y 010: los factoriales y el posicionamiento;
  - 2026-10-14-001: el cerebro entero;
  - 015: núcleo y H_TAU;
  - 018: la síntesis anterior;
  - 030: H_REUSO;
  - 031: la auditoría de Fable;
  - 034: H_RIVAL;
  - 035: la v2 publicada y la auditoría de los papers;
  - 038: H_LECTOR;
  - 041: H_TAU_LIBRE;
  - 044: Paper 3;
  - 049 a 056: la mosca entera.
- En `mojo-absoluto`: el estado medido que cita el CONTEXTO (HC-2 y HC-3b).

## Archivos

| Archivo | Dónde | md5 |
|---|---|---|
| `docs/agents/respuestas/2026-10-14-057-en-criollo-todo-lo-logrado-potencial-y-alcance.md` | `main` | este archivo |
| `tools/contexto/actualizar_contexto_2026-10-14-057.py` | `main` | 8bf9c90c342b52982256d1c8eed08841 |
| `.github/workflows/contexto-2026-10-14-057.yml` | `main`, se borra solo al aplicar | fb27ac8d9917f8e551e68b955a656287 |

## NO MEDIDO

- Hardware, cámara, placa, y energía y latencia en microcontrolador.
- La neurona que acumula, el cotejo de H_LECTOR, una H_DEBILES válida, H_REUSO_ESTRICTO, H_COMPARADOR y el nulo del emparejado BANC.
- La novedad frente a la literatura, como revisión sistemática.
- La demanda pagada de cualquier aplicación.
- Actions y Kaggle no se re-midieron hoy. Actions dio 4 núcleos y 16 GB en las corridas del 16-oct.
- El `00-ENTORNOS` de los otros tres repos.

## Antes de firmar

| Afirmación | Instrumento | ¿Podía dar rojo? | Veredicto |
|---|---|---|---|
| Los números citados son los del CONTEXTO y sus respuestas | CONTEXTO completo leído en esta sesión (md5 2da204c6) | Sí: un número mal copiado se ve contra la fuente | medido (copia) |
| Nada nuevo en git desde la 056 | `list_commits` de `main` | Sí | medido |
| brain-env tiene 78 GB libres, no 156 | `df -h /workspace` hoy | Sí | medido |
| «No choca con la 011» | lectura de los dos sujetos | No: es lectura | CONCLUSION |
| «Para un producto conviene lo clásico» | H_RIVAL (acierto); costo NO MEDIDO | Sí en acierto, no en costo | medido a medias |
| Potencial y orden | ninguno | No | opinión |
| El parche del CONTEXTO aplica | copia del de `main` en brain-env; la segunda pasada aborta | Sí | medido |

--- METODO PROMETEO ---
Rol: síntesis (chica). Delicado: no.
Máquinas: conector GitHub y brain-env (lectura, sondeo y parche), ClickUp (lectura del Doc 011), sandbox de ClickUp (redacción). Actions y Kaggle: nada.
Archivo: `docs/agents/respuestas/2026-10-14-057-en-criollo-todo-lo-logrado-potencial-y-alcance.md` en `main`.
Doc: https://app.clickup.com/90171457413/docs/2kza6fw5-23797
