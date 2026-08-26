# 096 · ¿La corrida de Kaggle y el DBC3 aportan a ARC-3? La corrida no. El código sí

**Fecha:** 2026-08-25 23:35 (America/Buenos_Aires) · **Modo:** TITAN FULL

**La distinción que ordena todo:** hay que separar **la corrida** de **el código**. La corrida de los 39 nulls no aporta nada a ARC-3. El código de `motor_v2` aporta una pieza crítica que nadie había contado.

<hr/>

## 1. 🔴 La corrida de los 39 nulls: aporte DIRECTO a ARC-3 = CERO

**Estado medido ahora mismo:**

```plain
CP 15/39     t=11423.4s   rdi(Wc,tauC)=0.0940  vent_tau=-0.0714  vent_W=-0.0010
CP 16/39     t=11890.1s   rdi(Wc,tauC)=0.1236  vent_tau=-0.1018  vent_W=-0.0043
proceso 9604: VIVO
```

**16 de 39 nulls, 3 h 18 min de máquina, faltan ~4,9 h.**

Lo que esa corrida cierra es **el `p` del paper del conectoma**. Y hay que decirlo sin vueltas: **ninguno de los cinco ejes de ARC-3 se mueve con ese número.** No aporta memoria, no aporta exploración, no aporta priors, no aporta planificación.

> **Veredicto:** que siga corriendo sola en el container es **gratis** y no hay que matarla. Que ocupe la cabeza o el turno, **no**.

**Y el dato colateral que sí vale, porque es un patrón en 16 nulls:** `vent_W` es **negativa en los 16** (−0,0010 a −0,0096) mientras en el grafo REAL era **+0,0021**. El signo se mantiene separado. Eso es información sobre el paper, no sobre el agente, pero es consistente.

<hr/>

## 2. 🔥 PERO el código de `motor_v2` es el instrumento que habilita el brazo S

**Esto no estaba contado como activo de ARC, y es el hallazgo del turno.**

El brazo `S` del 96% fijo necesita, **textual del `CONTEXTO-motor.md`**:

> *"máscara **shuffle** (mismo grado, misma sparsity), congelado"* → ¿es el conectoma, o cualquier grafo disperso?

Y `null_maslov_sneppen` de `motor_v2.py` (línea 466) hace **exactamente** eso:

> *"Preserva grado entrante Y saliente exactos. Sin auto-lazos ni duplicados."*

**Y ya está verificado hoy sobre el conectoma real, en la misma corrida que está andando:**

```plain
ms_preserva_grado_entrante   0 nodos alterados de 138.639
ms_preserva_grado_saliente   0 nodos alterados
ms_no_crea_multi_aristas     0 multi-aristas
el_metodo_uniforme_ROMPE_el_grado  106.948 nodos -> el test anterior PUEDE fallar
```

> **O sea: el brazo `S`, que es el único que impide que `W` sea una demo, ya tiene su generador escrito, testeado, con su control del control y corriendo sobre el grafo real.** Lo que en el `CONTEXTO-motor` figuraba como *"el único trabajo nuevo es la máscara desde el parquet"* está **más avanzado de lo que ese archivo cree**: la máscara shuffle con grado preservado **ya existe y ya pasó sus tests**.

**Eso convierte al brazo W+S de "90 minutos más escribir la máscara" en "90 minutos".** Y el brazo W+S está en el camino crítico de ARC-3, no del paper.

<hr/>

## 3. 🟢 Qué aporta el DBC3-v3: una decisión de diseño, medida

**El gate escalar se satura abierto** (`gmean` 0,970 / 0,970 / 0,964 en 3 de 4 tareas), o sea **aprende a NO gatear**. El vectorial **nunca colapsa a escalar** (4/4).

> **Traducido a un agente: un árbitro que aprende a no arbitrar nunca alterna de estrategia.** En ARC-3, donde el score **es** la eficiencia de adquisición, eso es fatal.

**Decisión cerrada y barata: gate vectorial, no escalar.** No hay que medirlo de nuevo.

<hr/>

## 4. 🟢 Qué aporta el DBC3-v4: el resultado más relevante para un agente, con su precio

```plain
VENTAJA SOBRE EL PISO MEDIDO, en puntos
  tarea                    v3           v4         LSTM | v4 vs v3 (pareado)
  XORMemory             +0.5       +16.4        -0.4 | +16.0 pts, t=0.97, n=3
  DelayedClass         +89.2       +78.5        -2.3 | -10.8 pts, t=-1.63, n=3
```

**Lo que compra el gate simétrico es poder APAGAR EL REFLEJO.** La v3 podía silenciar la memoria pero **nunca** la vía rápida; la v4 puede las dos.

> **Para ARC-3 eso es literalmente "ignorar el frame actual cuando es ruido", que es la mitad de explorar/explotar.** Un agente que no puede ignorar la percepción inmediata no puede sostener un plan a través de jugadas irrelevantes.

**Y el precio apareció exactamente donde se esperaba:** pagó el gate nuevo bajando `h_m` de 20 a 13, y perdió **10,8 puntos** en la tarea donde hacía falta **ancho de memoria**. Eso no es un fracaso del fix: **es el fix funcionando y su costo hecho visible.**

**Con `n=3` ningún `t` es concluyente y NO se declara significancia.** El `+16,0` tiene `t=0,97`: efecto grande, muestra chica.

<hr/>

## 5. 🔴 Lo que NINGUNO de los tres aporta

**Planificación. World model. Goal acquisition.**

Los tres rojos del mapeo contra ARC-3 **siguen rojos**, y ni la corrida del conectoma ni el DBC3-v3 ni el v4 los tocan. Ninguna de estas mediciones acerca un milímetro a *"build internal models of environment dynamics and plan effective action sequences"*.

<hr/>

## 6. El balance, en una tabla

| pieza | aporte a ARC-3 | valor |
|---|---|---|
| **la corrida de 39 nulls** | 🔴 **cero directo** | cierra el `p` del paper. Dejarla correr sola |
| **el código de `motor_v2`** | 🟢 **alto y no contado** | `null_maslov_sneppen` **es** el generador del brazo `S`, ya testeado sobre el grafo real |
| **DBC3-v3** | 🟢 **una decisión cerrada** | gate vectorial, no escalar. El escalar aprende a no gatear |
| **DBC3-v4** | 🟢 **el más relevante** | poder apagar el reflejo: +16,0 pts donde la v3 estaba en el piso |
| **los tres juntos** | 🔴 **no dan planificación** | sigue siendo la mitad faltante del problema |

<hr/>

## 7. Qué haría con esto, en orden

**Criterio: qué pone algo en el tablero de ARC-3.**

1. **Dejar la corrida del conectoma andando y no mirarla.** Cierra el paper mientras dormimos.
2. **Correr el brazo W+S**, que ahora cuesta menos de lo que el contexto creía porque su generador ya existe y ya pasó tests. **Es la validación de "funciona sin entrenar", que es la tesis entera.**
3. **Fijar el diseño del agente con lo ya medido:** gate **vectorial** y **simétrico**, `τ` heterogénea, `h_m` alto (DelayedClass mostró que el ancho de memoria se cobra).
4. **Y no auto-engañarse con el punto 3:** sin planificador, eso es un reactor muy bueno. **Falta la mitad.**

<hr/>

## 8. NO MEDIDO, declarado

1. **El brazo S no se corrió.** Se identificó que su generador existe y está testeado. **Eso no es lo mismo que tener el resultado.**
2. **La corrida de 39 nulls no cerró:** van 16, faltan ~4,9 h.
3. **Los 4 kernels de Kaggle siguen sin monitoreo** por el `403 kernels.get`. **No sé si arrancaron.**
4. **`n=3` semillas en el A/B del v4.** Ningún `t` concluyente.
5. **La traducción "apagar el reflejo" → "ignorar el frame" es MI interpretación.** Medido sobre regresión continua, no sobre decisión de acción en grillas.
6. **No se midió nada sobre grillas ni sobre el entorno de ARC-3.** Cero corridas del starter.
7. **La sección 7 es juicio, no medición.** Contradecible.
