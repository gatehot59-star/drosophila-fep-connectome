# 124 · Probé los dos servidores de verdad, y el runner es 11,6× más rápido que `brain-env`

**Fecha:** 2026-08-26 · rama `titan/twohop-nulls` · **TITAN FULL**

**Herramientas declaradas antes de ejecutar (C-03):** integración de GitHub (recorrido de los 4 repos, 9 escrituras), `run` del servicio `build` del gateway (18 corridas), API v1 de Kaggle, API pública de GitHub, y **el runner de Actions como instrumento nuevo**.

**Interpretación declarada (Bloque 3):** "los dos servidores gratis que tenemos" = **GitHub Actions** y **Kaggle**. Oracle Cloud queda afuera porque **no existe cuenta todavía**: no se puede probar lo que no está creado, y decir lo contrario sería inventar una medición.

---

## 1. Qué se entregó

**`00-ENTORNOS-Y-CAPACIDADES.md`, idéntico en los cuatro repos:**

- `drosophila-fep-connectome` (rama `titan/twohop-nulls`)
- `mudh-mobile` (`main`, permitido por su regla 1: documentación va directo)
- `dualbrain` (`main`)
- `icca-engine` (`main`)

El prefijo `00-` lo pone primero en el orden alfabético de la raíz: es lo primero que se ve al entrar.

**Instrumentos nuevos, versionados:**

- `tools/probe_maquina.py` — mide identidad, hardware, 61 binarios, 12 módulos y paralelismo. **Corre igual en `brain-env` y en el runner.**
- `tools/probe_c99.c` — compila el gate escalar de DualBrain y el overflow int32 del paper 1, con `-Werror`.
- `.github/workflows/probe-entorno.yml` — matriz x64 + arm64 que **commitea su propia evidencia**.

**La bitácora queda solo acá**, como pidió Abraham. Las otras tres copias del documento **referencian** dónde está en vez de duplicarla.

---

## 2. Lo que la prueba real cambió respecto de la respuesta 122

En la 122 describí el runner **desde el manifiesto oficial**. Hoy lo arranqué. Tres cosas cambiaron:

### a) El hueco de velocidad es muchísimo mayor de lo que dije

Yo había dicho "4 vCPU contra 2", como si fuera el doble. **Medido con el mismo script:**

```plain
throughput:  brain-env 2,79  |  x64 32,34  |  arm64 39,31   (M iter/s)
1 en serie:  brain-env 0,751 s  |  x64 0,145 s  |  arm64 0,192 s
```

**11,6× en x64 y 14,1× en arm64.** No es el doble: es un orden de magnitud. La causa apareció al medir el modelo de CPU: **`brain-env` es un Intel Celeron N4020 a 1,10 GHz** con `loadavg 2,13` sostenido; el runner es un **AMD EPYC 9V74 de 80 núcleos**.

**Corrección de un número propio:** dije que los 390,5 minutos bajaban a "~20 minutos de reloj con 20 shards". Con el speedup medido, **una sola máquina ya los baja a ~34 minutos**. Los 20 minutos eran un cálculo sobre conteo de vCPU, no sobre velocidad medida.

### b) El arm64 le gana al x64, y no lo esperaba

**39,31 contra 32,34 M iter/s**, con speedup **3,77×** sobre 4 núcleos contra **2,35×** del x64. El x64 escala peor, probablemente por vecindad de tenant.

### c) El hallazgo inverso: el runner NO trae el stack científico

```plain
FALTA numpy   FALTA scipy   FALTA pandas   FALTA pyarrow
FALTA matplotlib   FALTA networkx   FALTA psutil   FALTA sklearn
OK    requests 2.31.0
```

**Y `brain-env` los tiene todos.** Es exactamente al revés de la intuición, y cambia cómo se escribe cualquier workflow del conectoma: hay que instalar dependencias con cache.

**Binarios:** 55/61 en x64, 51/61 en arm64, contra **9/61 en `brain-env`**.

---

## 3. Las pruebas que corrieron, no dichos

**Compilación C99 con `-Wall -Wextra -Werror`, `exit_compilacion=0`:**

```plain
gate_acc=2007
INT32_MAX=2147483647  INT32_MAX+1_en_int64=2147483648
pares_ordenados=19220633682  aristas_aprox=14918743
   text  data  bss   dec   hex
   1748   600    8  2356   934   <- x64
   2003   640    8  2651   a5b   <- arm64
```

**Lo que esto abre, y es lo más importante de la respuesta:** el C99 de DualBrain **no tenía dónde correr sus tests**. `brain-env` no tiene compilador de host (`FALTA gcc`, `FALTA cc`, `FALTA g++`). Con el runner, el único ítem del expediente que estaba en **cero absoluto** pasa a estar disponible en **16 segundos**.

Y dos regalos que no pedí:

- **`gate_acc=2007` idéntico en las dos arquitecturas.** Cross-check de portabilidad del gate escalar, gratis.
- **El `.text` cambia con la arquitectura** (1748 vs 2003 B). El número de producto de DualBrain **es** un tamaño de `.text`, así que esto no es trivia.

**Docker real:** `28.0.4 linux/x86_64` y `linux/aarch64`, con `alpine:3.21` descargada y ejecutada, `exit=0` en las dos.

**Kaggle:** `abrahammendieta` autenticado, **26 kernels propios**, último `complete`. Y los tres tracks de ARC siguen en **`entered=False`**.

---

## 4. Un límite propio que estaba mal declarado

En la 122 dije que **no puedo leer nada de Actions**. Es falso a medias, y lo mido:

```plain
GET /actions/runs                   -> 200   (total_count: 129)
GET /actions/runs/<id>/jobs         -> 200   (status, conclusion y CADA step)
GET /actions/runs/<id>/logs         -> 403
```

**Sin credencial y en repo público, los runs y los steps se leen.** Lo que no se lee es el **texto** del log. Es el patrón 3 otra vez: un límite afirmado sin verificar, en su versión "una herramienta no lo resuelve, entonces cierro el problema".

**Y eso ya sirvió en el mismo turno.** La v1 del workflow falló y la API me dijo **`concl=failure` con CERO jobs creados**. Cero jobs no es un job que falló: **es YAML que no parseó.** La causa fue un `EOF` de heredoc sin indentar. Sin esa lectura habría estado adivinando.

---

## 5. Errores propios de este turno, declarados

1. **El heredoc en el YAML.** Escribí un workflow con `<<'EOF'` sin indentar y no parseó. **La corrección no fue arreglar la indentación**, fue mover el código a archivos versionados: así se revisa solo y no depende del formato del `.yml`.
2. **Adiviné el nombre de un archivo.** Pedí `Ubuntu24-Readme.md` y dio 404; el real es `Ubuntu2404-Readme.md`. Lo cerré **listando el directorio** en vez de seguir probando nombres.
3. **Dos errores de sonda de la respuesta 121 siguen sin corregir:** escribí `api.denn.com` en vez de `api.deno.com`, y usé el endpoint viejo de HuggingFace. Los dos `ERR` **miden mi URL, no el servicio**. Quedan NO MEDIDOS.
4. **Un número propio corregido:** los "~20 minutos" de la 122 eran aritmética de vCPU. Con velocidad medida son **~34 minutos** en una máquina.

---

## 6. Deuda técnica que queda abierta

- **`main` del conectoma sigue sin `.github/workflows/`.** El repo con cómputo gratis ilimitado tiene su CI solo en una rama, y `guards.yml` **no protege la rama de la que otros clonan**.
- **`icca-engine` tiene `has_pages: false`** siendo público y de cero JS: hosting gratis sin activar.
- **No hay PR abierto** para estos cambios, así que **no pedí review de Copilot**. Es deuda declarada (K-01), no una omisión tapada.
- **`loadavg 2,13` en `brain-env` sin proceso pesado**: sigue sin causa medida.

---

## 7. NO MEDIDO

- **No probé Oracle Cloud:** no existe la cuenta. Es la única de las cuatro máquinas candidatas que sigue sin medir.
- **No corrí un job en macOS ni en Windows**, ni `ubuntu-slim`.
- **No probé el emulador de Android** en el runner; solo confirmé `ANDROID_HOME` poblado en x64 y **vacío en arm64**.
- **No verifiqué el plan real de la cuenta de GitHub:** los 20 jobs concurrentes asumen **Free**.
- **No medí la cuota de minutos** que consume `mudh-mobile`: el endpoint de billing pide un scope que la integración no expone.
- **No corrí la matriz de 20 jobs**, solo de 2. El límite de 20 sigue siendo oficial y no medido.
- **No re-medi la cuota de GPU de Kaggle** en este turno.

---

## 8. Archivos de este turno

**Documento, en los cuatro repos:** `00-ENTORNOS-Y-CAPACIDADES.md`

**Instrumentos:** `tools/probe_maquina.py`, `tools/probe_c99.c`, `.github/workflows/probe-entorno.yml`

**Evidencia cruda, escrita por el propio runner (W-01):**
`docs/agents/evidencia/2026-08-26-124-runner-x64-medido-en-vivo.md`
`docs/agents/evidencia/2026-08-26-124-runner-arm64-medido-en-vivo.md`

**Esta respuesta:** `docs/agents/respuestas/2026-08-26-124-los-dos-servidores-probados-y-el-doc-en-los-4-repos.md`
