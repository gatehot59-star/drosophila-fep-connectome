# resp 010 · Sí, los Docs los leo enteros. Y el plan maestro arranca mañana

**Fecha:** 2026-08-23 23:01 (America/Buenos_Aires) · **Modo:** TITAN LIGERO

## 1. Pedido

> «Varios documentos así fueron copiados en los chats que te pegué. ¿Los podés ir a ver o tampoco? Porque si no podés ya no sé qué es lo que podés hacer.» + link al PLAN MAESTRO 10 SEMANAS.

## 2. La respuesta: SÍ, y la distinción importa

| Tipo de asset | ¿Se lee? |
|---|---|
| **Docs de ClickUp** | **SÍ, completos.** Leí el plan entero: 6 secciones, las 10 semanas con método y criterio de aborto, el inventario de 13 hallazgos con su null, los 7 riesgos y el scorecard |
| **PDF adjuntos** | **SÍ.** El Paper 1 se leyó verbatim (resp 007) |
| **Tareas de ClickUp** | SÍ |
| **HTML de Arena** | **NO.** Es la cáscara de la página; el texto vive en los `.js` que no vinieron (resp 008) |

O sea: **lo único que no puedo abrir son los exports de Arena.** Todo lo que esté copiado dentro de un Doc de ClickUp lo leo.

## 3. Lo urgente del plan: arranca MAÑANA

**S1 va del lunes 24 al domingo 30 de agosto.** Hoy es domingo 23. Mañana empieza.

Y los dos deadlines duros: **2 de noviembre** (código a Kaggle) y **8 de noviembre** (papers). Diez semanas exactas.

## 4. Tres items del plan que las corridas de agosto ya movieron

### 4.1 S2 pide 21 nulls más por el motivo equivocado

El plan dice: *«Continuar las semillas `1000 + 7·i` desde i=9. Piso de p a dos colas pasa de 0,20 a 0,0488»*, con criterio de aborto *«si con 40 nulls la ventaja de τ compleja no llega a 0/40, sale del paper de ARC»*.

**El problema no es el piso.** Bajé el log hoy (`results/motor_ltc_complejo.log`):

```
TEST GLOBAL sobre 6 de 6 estadisticos
  S_real=38.0  S_null_mu=32.4  sd=5.4  min=27.0
  nulls por debajo=8/9   p dos colas=0.6000   piso alcanzable=0.2000

ventaja_compleja_t120     real=-0.02973  null_mu=-0.04066  n_ge=4/9  p2=1.0000
ventaja_compleja_t60      real=+0.00150  null_mu=+0.00856  n_ge=9/9  p2=0.2000
```

**El test global da 0,6000, muy por encima de su piso de 0,20.** Y el `0/9` que el plan cita vale solo en `t=199`: en `t=120` la ventaja real es **negativa** y en `t=60` los nueve nulls superan al real.

**Consecuencia:** más nulls no arreglan esto, porque el problema es **consistencia temporal**, no potencia. El criterio de aborto de S2 ya se cumplió con 9 nulls. Correr 21 más es gastar cuota para confirmar algo que ya sabemos, **salvo** que se reformule la pregunta a un solo snapshot declarado de antemano, y eso sería post-hoc.

### 4.2 El plan cierra con una deuda que ya no existe

> `NO cerrado: titan-tres-brazos sigue en running.`

Cerró, y el brazo W también. Los dos leídos. Y el resultado del brazo W **no refuta la hipótesis del 96% fijo**: midió el motor denso de 8 unidades sobre 26 nodos y no congeló τ. Eso deja la predicción falsable de **S8** (*«`react` congelado debería alcanzar a `react` entrenable»*) todavía **sin medir**, no refutada.

### 4.3 S1: el item del erratum queda cerrado por decisión, no por verificación

S1 pide *«verificar el erratum contra el PDF publicado»* con criterio de aborto *«si difiere en más de dos números, parar»*. Hice esa verificación (resp 007) y **difiere en más de dos**: Table 7 es otra tabla, el 1.559× no aparece en las cuatro secciones citadas, y el DOI del PDF es un placeholder.

**Pero Abraham declara el erratum ya resuelto con las corridas de agosto.** Así que el item se cierra por su decisión. Lo registro como tal y no vuelvo sobre marzo.

## 5. Lo que el plan confirma y no había registrado

Dos cosas del plan que son mejores que mi estado y las adopto:

1. **El producto son TRES capas, no un motor:** la fuente de calibración (conectoma + priors), el motor (SparseLTC/DualBrain), y **la biblioteca**, que es donde está el activo. Hoy la biblioteca tiene **1 de 3-4** motivos que hacen falta.
2. **El pitch no es «derivado del cerebro de la mosca»:** son microsegundos, miliwatts y costo de materiales. El conectoma es el currículum, no el pitch.

## 6. NO MEDIDO

- **Las 11 tareas de ClickUp del plan siguen sin crear.** Son 11 escrituras y requieren tu OK.
- No verifiqué las fechas ni los premios de ARC en esta pasada: el plan las declara verificadas en vivo el 23-ago.
- No sé con qué números exactos quedó el erratum corregido en agosto.
