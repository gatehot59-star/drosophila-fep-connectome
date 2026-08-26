# Evidencia cruda · 4 shards GPU lanzados en Kaggle para los 39 nulls restantes

**Fecha:** 2026-08-25 21:16 (America/Buenos_Aires)

## 1. Lo que Tachi había dejado, y hacía falta leer

`docs/agents/MANIFIESTO-KAGGLE.md` dice textual:

> **Los tokens llevan prefijo `KGAT_` y solo funcionan con `Authorization: Bearer <token>`.** Las otras cinco formas probadas dan `401` en las dos cuentas. El helper `kauth.mjs` usa `Basic` y por eso falla; `klib.mjs` usa `Bearer` y funciona.

Eso cambió el método entero: el problema no era "las credenciales están rotas", era **que estábamos llamando mal**.

## 2. Verificación del camino correcto, medido

### Helpers encontrados en `/workspace`

```plain
/workspace/kpush.mjs
/workspace/kwatch.mjs
/workspace/klib.mjs
/workspace/kauth.mjs
```

### `klib.mjs`, verbatim

```javascript
import fs from "node:fs";
export const CR=JSON.parse(fs.readFileSync("/workspace/kaggle.json","utf8"));
export const H=(c)=>({Authorization:"Bearer "+c.token});
export const api=async(c,path,opt={})=>{
  const r=await fetch("https://www.kaggle.com/api/v1"+path,{...opt,headers:{...H(c),...(opt.headers||{})}});
  const t=await r.text();
  let j=null; try{j=JSON.parse(t);}catch(e){}
  return {status:r.status,text:t,json:j};
};
```

### Tokens medidos

```plain
fabiomurillohot -> prefijo KGAT_ largo 37
abrahammendieta -> prefijo KGAT_ largo 37
```

### Push de un kernel existente con Bearer: la via funciona

```plain
kpush.mjs usa CR[1], Bearer y /kernels/push
```

## 3. El corredor montado

Se montaron en `/workspace`:

```plain
/workspace/gpu_shard.py      11K
/workspace/kernel_shard.py   75K
/workspace/kpush39.mjs       2.8K
/workspace/kwatch39.mjs      701 B
```

### Qué hace el runner, resumido a lo medible

- reparte 39 nulls en 4 shards intercalados
- verifica **GPU contra CPU sobre el grafo REAL** antes de usar la GPU
- si la GPU no reproduce, **la rechaza** y cae a CPU declarado
- guarda parcial en JSON por shard
- el shard 0 mide además el grafo REAL, para que baste un pedazo para reconstruir

## 4. Push de los 4 kernels, verbatim

```plain
shard 0 -> abrahammendieta/titan-motorv2-gpu-shard0 | HTTP 200 | GPU=on | https://www.kaggle.com/code/abrahammendieta/titan-motor-v2-gpu-shard-0-4
shard 1 -> abrahammendieta/titan-motorv2-gpu-shard1 | HTTP 200 | GPU=on | https://www.kaggle.com/code/abrahammendieta/titan-motor-v2-gpu-shard-1-4
shard 2 -> fabiomurillohot/titan-motorv2-gpu-shard2 | HTTP 200 | GPU=on | https://www.kaggle.com/code/fabiomurillohot/titan-motor-v2-gpu-shard-2-4
shard 3 -> fabiomurillohot/titan-motorv2-gpu-shard3 | HTTP 200 | GPU=on | https://www.kaggle.com/code/fabiomurillohot/titan-motor-v2-gpu-shard-3-4
```

## 5. Intento de monitoreo por API, y límite real encontrado

```plain
shard 0 | abrahammendieta/titan-motorv2-gpu-shard0 | {"code":403,"message":"Permission 'kernels.get' was denied"}
shard 1 | abrahammendieta/titan-motorv2-gpu-shard1 | {"code":403,"message":"Permission 'kernels.get' was denied"}
shard 2 | fabiomurillohot/titan-motorv2-gpu-shard2 | {"code":403,"message":"Permission 'kernels.get' was denied"}
shard 3 | fabiomurillohot/titan-motorv2-gpu-shard3 | {"code":403,"message":"Permission 'kernels.get' was denied"}
```

**Lectura correcta:** las credenciales **sí pueden empujar** (`HTTP 200` en `/kernels/push`) pero **no pueden leer estado** (`403 kernels.get`). Eso limita el monitoreo por API; **no invalida el lanzamiento**.

## 6. NO MEDIDO, declarado

1. **No se pudo leer `status` ni `output` por API** después del push, por `403 kernels.get denied`.
2. **No se sabe todavía si Kaggle asignó GPU real o si el runner cayó a CPU**, porque esa decisión vive dentro del log del kernel y hoy el API no lo devuelve.
3. **No se sabe si los 4 arrancaron o quedaron en cola.** El push fue 200, pero el estado de ejecución sigue opaco.
4. **No se hizo shard 0..3 contra la cuota disponible antes del push.** El usuario pidió explícitamente lanzar; se ejecutó y se declara esa omisión.
5. **La corrida larga del container (CP 2/39 del conectoma real) sigue viva en paralelo** y no se tocó en este turno.

## 7. Qué sí queda establecido

- la vía correcta de auth es **Bearer con `KGAT_`**, no Basic
- los 4 kernels privados **fueron creados/actualizados** con GPU encendida
- el reparto de nulls quedó horneado por shard y no depende de argumentos externos
- cada shard verifica GPU vs CPU antes de medir, así que si devuelve un número, va a ser el mismo sujeto
