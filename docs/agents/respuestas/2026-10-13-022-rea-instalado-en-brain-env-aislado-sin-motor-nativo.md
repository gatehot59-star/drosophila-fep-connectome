# 2026-10-13-022 · REA 6.4.0 quedó instalado en brain-env, aislado y verificado; inventaría artefactos pero todavía no mira adentro de un binario: falta Ghidra

## Veredicto

- **[MEDIDO] Instalado.** `rea-agents@6.4.0` en `/workspace/rea`, con el lanzador `/workspace/rea/rea`, que lo corre con HOME propio y entorno mínimo. `rea --version` devuelve `6.4.0`.
- **[MEDIDO] Es el paquete oficial y al instalar no corrió código de terceros.**
  - Registry oficial (`https://registry.npmjs.org/`), `latest` = `6.4.0`, repositorio declarado `github.com/morluto/rea`, procedencia SLSA v1.
  - La integridad sha512 del lock es la misma que publica el registry.
  - `144 packages have verified registry signatures` y `32 packages have verified attestations`.
  - Se instaló con `--ignore-scripts`, y el escaneo encontró 0 paquetes con scripts de instalación: no había nada que saltear.
  - `npm audit --omit=dev`: `found 0 vulnerabilities`.
- **[MEDIDO] Anda y puede dar rojo.** Sobre una caja de juguete nuestra (C, gcc `-O2`, sin símbolos) devolvió formato `elf` y el mismo sha256 que `sha256sum`. Sobre un archivo inexistente falló con `target_unavailable`.
- **[MEDIDO] Todavía no mira adentro de un binario.** `rea doctor` da `healthy: false`: Debian 13 figura como `unsupported_host` y no hay motor (ni Hopper, ni Ghidra 12.1.x, ni IDA). El propio REA lo declara en su salida: `open_binary was not run by provider-neutral artifact inspection`. Sin Ghidra no hay funciones ni pseudocódigo, y la prueba de dbc3-link de la 021 sigue sin poder correrse.
- **[DECISIÓN] No corrí `rea setup`.** En brain-env hay un Claude Code instalado, y setup le reescribe la configuración MCP y le instala instrucciones de trabajo: cambia cómo trabaja otro agente en esa máquina. Eso lo decide Abraham.
- **[MEDIDO] Riesgo residual.** REA corre con el mismo usuario dueño del home donde está `kaggle.json`. El HOME aislado evita una lectura casual, no una por ruta absoluta.
- **[DATO] Siguiente paso posible:** Ghidra 12.1.4 es la última release (2026-09-21, SHA-256 publicado `ddac49f903da9d5bac833e5cc79395098b9c33cfd3279be5f31bd00387d2d4db`), y REA pide 12.1.x más un JDK 21; brain-env tiene JDK 17.

## De paso: el inventario de las tres máquinas quedó viejo

Medido hoy contra `00-ENTORNOS-Y-CAPACIDADES.md`, que se mantiene idéntico en los cuatro repos:

| dice el inventario | medido hoy |
|---|---|
| «Soy root (`uid=0`)» | `uid=1000(estudiante)`, HOME `/workspace/homebrain` |
| credencial de Kaggle en `/root/.kaggle/kaggle.json` | `kaggle.json` presente en `~/.kaggle` de ese HOME; `/root` no se miró |
| falta `gcc`; el de conda compila pero el binario no corre | `/usr/bin/gcc`: `gcc (Debian 14.2.0-19) 14.2.0`; compiló la caja y **el binario corrió**: exit 0 con el código bueno y 1 con el malo |
| 156 GB libres en `/workspace` | 86 GB libres (406 G, 301 G usados, 78 %) |
| (no figura) | `/workspace/tools` es de root y no se puede escribir; `/workspace` sí |
| (no figura) | Claude Code en `/home/estudiante/.nvm/versions/node/v24.18.0/bin/claude` |

**El que más pesa:** con el gcc 14.2 del sistema, C nativo compila **y corre** en brain-env. El inventario manda eso solo a Actions, así que para los tests nativos del C99 de DualBrain cambia la máquina posible. Medido con una caja de 18 líneas, no con el C99 real.

**No se corrigió en este turno:** son cuatro copias del mismo archivo en cuatro repos, dos privados. Queda pendiente.

## Pedido

22:14: «pues instala rea en brain-env»

## Herramientas y máquina

- **brain-env** por el gateway (servicio `build`, herramienta `run`), 12 llamadas.
  - Lectura: registry de npm, rutas, agentes instalados, disco, permisos, `doctor`, `providers` y ayudas.
  - Escritura, todo bajo `/workspace/rea` (directorio nuevo): `npm install`, el lanzador `rea`, la caja de prueba en `smoke/`, los scripts y los logs. Fuera de ahí, solo `/tmp`.
  - **El primer intento falló** por permisos (`/workspace/tools` es de root) y no escribió nada; se movió a `/workspace/rea`.
- **Red desde brain-env:** registry de npm (instalación, firmas y `npm audit`, que manda el árbol de dependencias a npm).
- **API de GitHub:** lectura de la última release de Ghidra; escritura de este archivo.
- **Sin cuota de Kaggle ni de GPU.** `rea setup` no se corrió y ninguna configuración de agentes se tocó.

## Qué se midió

| dato | valor | instrumento |
|---|---|---|
| versión instalada | 6.4.0 | `rea --version`, directo y por el lanzador |
| paquetes | 144 instalados, 149 entradas en el lock | `npm install`, lock |
| firmas del registry | 144 de 144 verificadas | `npm audit signatures` |
| attestations de procedencia | 32 verificadas | ídem |
| integridad de rea-agents | igual a la del registry | lock contra `npm view` |
| scripts de instalación | 0 | escaneo de `package.json` y `binding.gyp` en `node_modules` |
| vulnerabilidades | 0 | `npm audit --omit=dev` |
| tamaño | 96 MB de `node_modules`, 97 MB en total | `du -sh` |
| tiempo de instalación | 1 min 42 s (01:18:26Z a 01:20:08Z) | `date -u` en el log |
| sha256 de la caja según REA | `51c020e6...a71e38e` | `rea inspect-artifact` |
| sha256 de la caja, testigo | `51c020e6...a71e38e` | `sha256sum` |
| salud | `healthy: false` | `rea doctor` |

## Evidencia cruda

Antes de instalar (registry, rutas, agentes, disco). Los scripts del paquete se cortaron con `head -80`; el instrumento sobre los scripts de instalación es el escaneo posterior, no esta lista:

```
== registry
https://registry.npmjs.org/
== dist-tags
{
  "latest": "6.4.0"
}
== 6.4.0
{
  "name": "rea-agents",
  "version": "6.4.0",
  "repository.url": "git+https://github.com/morluto/rea.git",
  "dist.integrity": "sha512-Vj1zWfSlna5bphGoaoI/TcVBuYvze9u+OyPC3Shz8YkBqaCTqB4COnnRoX7XDwMpwI24ZlFEel2yEj0k8LTWEQ==",
  "dist.tarball": "https://registry.npmjs.org/rea-agents/-/rea-agents-6.4.0.tgz",
  "dist.attestations": {
    "url": "https://registry.npmjs.org/-/npm/v1/attestations/rea-agents@6.4.0",
    "provenance": {
      "predicateType": "https://slsa.dev/provenance/v1"
    }
  },
  "scripts": {
(...)
== rutas
/home/estudiante/.nvm/versions/node/v24.18.0/bin/node
/home/estudiante/.nvm/versions/node/v24.18.0/bin/npm
/usr/bin/bash
/usr/local/bin/python3
== agentes
/home/estudiante/.nvm/versions/node/v24.18.0/bin/claude
codex: NO
gemini: NO
cursor-agent: NO
== disco
/dev/sda4       406G  301G   86G  78% /workspace
== fecha
Wed Oct 14 01:15:54 UTC 2026
```

Primer intento, en `/workspace/tools`, y los permisos que lo explican:

```
--- STDERR ---
sh: 1: cannot create /workspace/tools/rea-install.sh: Permission denied
md5sum: /workspace/tools/rea-install.sh: No such file or directory
md5sum: /workspace/tools/rea-install.sh: No such file or directory

uid=1000(estudiante) gid=1000(estudiante) groups=1000(estudiante),106
drwxrwxrwt   1 root       root       12288 Oct 13 23:16 /tmp
drwxr-xr-x 494 estudiante estudiante 69632 Oct 13 23:22 /workspace
drwxr-xr-x  18 estudiante estudiante  4096 Oct  7 12:36 /workspace/homebrain
drwxr-xr-x   6 root       root        4096 Aug 27 11:02 /workspace/tools
homebrain: escribible
workspace raiz: escribible

ls: cannot access '/workspace/rea': No such file or directory
```

Lanzamiento (md5 del script decodificado igual al generado) y `install.log` completo:

```
5a992c670fc19531ca12dbd25e338461  /workspace/rea/install.sh

== inicio 2026-10-14T01:18:26Z
node v24.18.0 npm 11.16.0 registry https://registry.npmjs.org/
== npm install rea-agents@6.4.0 --save-exact --ignore-scripts

added 144 packages in 1m
exit_install=0
== npm audit signatures
audited 144 packages in 11s

144 packages have verified registry signatures

32 packages have verified attestations
(use --json --include-attestations to view attestation details)

exit_signatures=0
== lock, integridad y scripts de instalacion omitidos
rea-agents version lock   : 6.4.0
rea-agents integrity lock : sha512-Vj1zWfSlna5bphGoaoI/TcVBuYvze9u+OyPC3Shz8YkBqaCTqB4COnnRoX7XDwMpwI24ZlFEel2yEj0k8LTWEQ==
rea-agents integrity match: True
paquetes en el lock       : 149
con scripts de instalacion (omitidos): 0
== tamano
96M	node_modules
== version, con HOME aislado
6.4.0
exit_version=0
== fin 2026-10-14T01:20:08Z
```

`rea doctor`, con HOME aislado (primeras líneas):

```
healthy: false
environment_healthy: false
scope:
  mode: audit-wide
  clients: []
  providers: []
  skill: false
  target: null
scope_checks[6]:
  - name: node
    ok: true
    classification: healthy
    detail: 24.18.0
  - name: host
    ok: false
    classification: unsupported_host
    detail: debian 13
    remediation: "REA supports macOS 12+, Ubuntu 24.04+, Fedora 41+, Nobara 44+, 64-bit Arch Linux, CachyOS, Omarchy, and the experimental Windows x64 Ghidra P0 boundary."
  - name: hopper
    ok: false
    classification: missing_analysis_engine
    remediation: "Run rea setup to install Hopper, or set HOPPER_LAUNCHER_PATH."
  - name: ghidra
    ok: false
    classification: missing_analysis_engine
    detail: GHIDRA_INSTALL_DIR is not set
    remediation: Set GHIDRA_INSTALL_DIR to an extracted Ghidra 12.1.x release directory.
  - name: ida-registration
    ok: false
    classification: missing_analysis_engine
    detail: IDA MCP registration is not configured.
    remediation: Set REA_IDA_MCP_CONFIG to your upstream IDA MCP registration JSON; see docs/ida-provider.md.
  - name: "skill:identity"
    ok: false
    classification: config_drift
    detail: Installed REA skill identity is missing.
    remediation: Run rea setup to update the installed REA skill.
```

Prueba de humo sobre la caja (`smoke.sh`, md5 verificado antes de correr):

```
677d9e63529455e22a005c5436e58b86  /workspace/rea/smoke.sh
== fuente
4a978651ac1ac459d89487d4546a8ae2  caja.c
== compilar
exit_gcc=0
exit_strip=0
== testigo independiente
51c020e6b3f176552bdabe424e8898619588d9446873ac8d8120787d1a71e38e  caja.stripped
caja.stripped: ELF 64-bit LSB pie executable, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, BuildID[sha1]=5893807b74ef82776d03263224c3d322b19f07f0, for GNU/Linux 3.2.0, stripped
CAJA-021: abierta
exit_bueno=0
CAJA-021: cerrada
exit_malo=1
== rea inspect-artifact (HOME aislado)
exit_rea=0
5499 inspect.json
   0 inspect.err
5499 total
sha256 en la salida de REA: ['05377881adde09fac541493b78d11ddf5912a6fd7d412d25431ec86fba32cafd', '1ea127c54c90998a2ba81a3c45d5a71c5d064deab153d7fa7888c855c8e6bf8c', '33040c776221af5a7f2617d8df9ceec399361083a4d724819ffc94de2781a722', '51c020e6b3f176552bdabe424e8898619588d9446873ac8d8120787d1a71e38e', '5268367f73c0bf3bf7bdb49f7cf9a560324e227877e6155349babd6f39794896']
'ELF'        aparece 0 veces
'elf'        aparece 7 veces
'x86_64'     aparece 0 veces
'x86-64'     aparece 0 veces
'amd64'      aparece 0 veces
'CAJA-021'   aparece 0 veces
'MDH-'       aparece 0 veces
claves de primer nivel: ['evidence_id', 'subject', 'provider', 'analysis_profile', 'predicate_type', 'operation', 'parameters', 'raw_result', 'normalized_result', 'confidence', 'authority', 'environment', 'limitations', 'locations', 'evidence_links']
== stderr de REA (primeras lineas)
== soporte objdump en el paquete
```

Lo que dijo REA de la caja (fragmentos de `inspect.json`, sin editar):

```
"subject":{"name":"caja.stripped","digest":{"sha256":"51c020e6b3f176552bdabe424e8898619588d9446873ac8d8120787d1a71e38e"},"format":"elf","architecture":null,"local_path":"/workspace/rea/smoke/caja.stripped"},"provider":{"id":"rea-artifact-graph","name":"REA safe artifact graph provider","version":"1"}
"format":"elf","sha256":"51c020e6b3f176552bdabe424e8898619588d9446873ac8d8120787d1a71e38e","size":14488,"media_type":null,"architecture":null,"content_state":"materialized"
"executable":true,"encrypted":false,"hash_status":"verified"
"unexplored_branches":[{"branch_id":"aib_a23a2d1a105d845c928dba5af188c7593f1cf4cad59cfd14bb54af81b7bd969b","reason":"format-specific-analysis-required","detail":"open_binary was not run by provider-neutral artifact inspection.","next_probe":{"operation":"open_binary","rationale":"Bind one deep native provider before function-level analysis.","authority":"native-analysis-provider"}
"limitations":["Artifact has no child container entries.","Inspection derives bounded static hypotheses and next probes; it does not execute the artifact or claim format-specific semantics."]
```

La búsqueda de soporte para objdump o Rizin en el paquete 6.4.0 no devolvió nada; el README de `main` lo menciona. Con un `grep` que dio vacío, eso queda NO MEDIDO (puede ser que no esté publicado en npm o que el código no lo nombre así).

Cierre (`check.sh`, md5 verificado antes de correr):

```
bfe52ce0a10050ede8d4e7dd94acb1d8  /workspace/rea/check.sh
== wrapper
#!/bin/sh
# REA 6.4.0 aislado: HOME propio y entorno minimo (2026-10-13-022).
# Uso: /workspace/rea/rea <comando> [opciones]
exec env -i HOME=/workspace/rea/home PATH=/home/estudiante/.nvm/versions/node/v24.18.0/bin:/usr/bin:/bin /workspace/rea/node_modules/.bin/rea "$@"
ea2c60edb1289c5d77a3b81ce712ea02  /workspace/rea/rea
== wrapper --version
6.4.0
== puede dar rojo: archivo inexistente
ROJO (bien: fallo como debia)
error: Analysis failed
code: target_unavailable
category: unavailable
message: "Cannot open artifact: target does not exist or a path component is not a directory: ENOENT: no such file or directory, access '/workspace/rea/no-existe.bin'. Check that the path exists, is readable, and points to a supported file."
retryable: false
remediation:
  action: "Cannot open artifact: target does not exist or a path component is not a directory: ENOENT: no such file or directory, access '/workspace/rea/no-existe.bin'. Check that the path exists, is readable, and points to a supported file."
details:
  path
== puede dar verde con el wrapper: la caja
VERDE
"root_sha256":"51c020e6b3f176552bdabe424e8898619588d9446873ac8d8120787d1a71e38e"
51c020e6b3f176552bdabe424e8898619588d9446873ac8d8120787d1a71e38e  /workspace/rea/smoke/caja.stripped
== gcc
gcc (Debian 14.2.0-19) 14.2.0
== npm audit (CVE en vivo, dependencias de produccion)
found 0 vulnerabilities
== md5 y tamano
fee8b769540ec5bf30bdca4e894925c5  package-lock.json
3d191771eeeb84264daf341d7ead9c54  package.json
5a992c670fc19531ca12dbd25e338461  install.sh
677d9e63529455e22a005c5436e58b86  smoke.sh
97M	/workspace/rea
```

Última release de Ghidra (API de GitHub):

```
"name":"Ghidra 12.1.4","published_at":"2026-09-21T17:38:59Z","tag_name":"Ghidra_12.1.4_build"
* SHA-256: `ddac49f903da9d5bac833e5cc79395098b9c33cfd3279be5f31bd00387d2d4db`
```

## Instrumentos, verbatim y ejecutados

Cada uno viajó en base64 y se verificó por md5 antes de correr, porque el shell del gateway pre-expande `$`.

`install.sh` (md5 `5a992c670fc19531ca12dbd25e338461`):

```bash
#!/usr/bin/env bash
# Instala REA (rea-agents 6.4.0) en brain-env, aislado en /workspace/rea.
# Sin scripts de instalacion, version exacta, verificacion de firmas y de integridad.
set -u
NODE_BIN=/home/estudiante/.nvm/versions/node/v24.18.0/bin
DEST=/workspace/rea
LOG=/workspace/rea/install.log
EXPECTED='sha512-Vj1zWfSlna5bphGoaoI/TcVBuYvze9u+OyPC3Shz8YkBqaCTqB4COnnRoX7XDwMpwI24ZlFEel2yEj0k8LTWEQ=='
export PATH="$NODE_BIN:/usr/local/bin:/usr/bin:/bin"
mkdir -p "$DEST/home"
cd "$DEST" || exit 1
exec > "$LOG" 2>&1
echo "== inicio $(date -u +%FT%TZ)"
echo "node $(node --version) npm $(npm --version) registry $(npm config get registry)"
[ -f package.json ] || printf '{"name":"rea-local","private":true}\n' > package.json
echo "== npm install rea-agents@6.4.0 --save-exact --ignore-scripts"
npm install rea-agents@6.4.0 --save-exact --ignore-scripts --no-fund --no-audit
echo "exit_install=$?"
echo "== npm audit signatures"
npm audit signatures
echo "exit_signatures=$?"
echo "== lock, integridad y scripts de instalacion omitidos"
EXPECTED="$EXPECTED" python3 - <<'PY'
import json, os
lock = json.load(open('package-lock.json'))
pk = lock['packages']
got = pk.get('node_modules/rea-agents', {}).get('integrity')
print('rea-agents version lock   :', pk.get('node_modules/rea-agents', {}).get('version'))
print('rea-agents integrity lock :', got)
print('rea-agents integrity match:', got == os.environ['EXPECTED'])
print('paquetes en el lock       :', len([k for k in pk if k]))
skipped = []
for k in pk:
    if not k:
        continue
    pj = os.path.join(k, 'package.json')
    try:
        s = json.load(open(pj)).get('scripts', {}) or {}
    except Exception:
        continue
    hooks = [h for h in ('preinstall', 'install', 'postinstall') if h in s]
    if os.path.exists(os.path.join(k, 'binding.gyp')):
        hooks.append('binding.gyp')
    if hooks:
        skipped.append((k, hooks))
print('con scripts de instalacion (omitidos):', len(skipped))
for k, h in skipped:
    print('  ', k, h)
PY
echo "== tamano"
du -sh node_modules
echo "== version, con HOME aislado"
env -i HOME="$DEST/home" PATH="$NODE_BIN:/usr/bin:/bin" "$DEST/node_modules/.bin/rea" --version
echo "exit_version=$?"
echo "== fin $(date -u +%FT%TZ)"
```

`smoke.sh` (md5 `677d9e63529455e22a005c5436e58b86`), que recibe `caja.c` en base64 como argumento:

```bash
#!/usr/bin/env bash
# Prueba de humo de REA 6.4.0 en brain-env: binario propio, regla conocida.
set -u
NODE_BIN=/home/estudiante/.nvm/versions/node/v24.18.0/bin
R=/workspace/rea
S=$R/smoke
mkdir -p "$S"
cd "$S" || exit 1
printf '%s' "$1" | base64 -d > caja.c
echo "== fuente"; md5sum caja.c
echo "== compilar"; /usr/bin/gcc -O2 -o caja caja.c; echo "exit_gcc=$?"
cp caja caja.stripped && /usr/bin/strip caja.stripped; echo "exit_strip=$?"
echo "== testigo independiente"
sha256sum caja.stripped; file caja.stripped 2>/dev/null || echo "file: no esta"
./caja.stripped MDH-12369; echo "exit_bueno=$?"
./caja.stripped MDH-12368; echo "exit_malo=$?"
echo "== rea inspect-artifact (HOME aislado)"
env -i HOME="$R/home" PATH="$NODE_BIN:/usr/bin:/bin" "$R/node_modules/.bin/rea" inspect-artifact "$S/caja.stripped" --format json > inspect.json 2> inspect.err
echo "exit_rea=$?"
wc -c inspect.json inspect.err
python3 - <<'PY'
import json, re
raw = open('inspect.json').read()
print('sha256 en la salida de REA:', sorted(set(re.findall(r'[0-9a-f]{64}', raw)))[:5])
for k in ('ELF', 'elf', 'x86_64', 'x86-64', 'amd64', 'CAJA-021', 'MDH-'):
    print(f'{k!r:12} aparece {raw.count(k)} veces')
try:
    d = json.loads(raw)
    print('claves de primer nivel:', list(d)[:15] if isinstance(d, dict) else type(d).__name__)
except Exception as e:
    print('json invalido:', e)
PY
echo "== stderr de REA (primeras lineas)"; head -5 inspect.err
echo "== soporte objdump en el paquete"
grep -rhoE 'REA_[A-Z_]*(OBJDUMP|RIZIN)[A-Z_]*' "$R/node_modules/rea-agents/dist" "$R/node_modules/rea-agents/skills" 2>/dev/null | sort -u | head
grep -rlE 'objdump' "$R/node_modules/rea-agents/skills" 2>/dev/null | head -5
```

`caja.c` (md5 `4a978651ac1ac459d89487d4546a8ae2`), la caja con la regla conocida:

```c
#include <stdio.h>
#include <string.h>
/* Caja fuerte de juguete para la prueba de humo de REA (2026-10-13-022).
   Regla conocida: "MDH-" + 5 digitos que suman 21. */
static int ok(const char *s) {
    if (strlen(s) != 9 || strncmp(s, "MDH-", 4) != 0) return 0;
    int sum = 0;
    for (int i = 4; i < 9; i++) {
        if (s[i] < '0' || s[i] > '9') return 0;
        sum += s[i] - '0';
    }
    return sum == 21;
}
int main(int argc, char **argv) {
    if (argc > 1 && ok(argv[1])) { puts("CAJA-021: abierta"); return 0; }
    puts("CAJA-021: cerrada");
    return 1;
}
```

`check.sh` (md5 `bfe52ce0a10050ede8d4e7dd94acb1d8`), que además escribe el lanzador `rea`:

```bash
#!/usr/bin/env bash
# Cierre de la instalacion de REA en brain-env: wrapper aislado, prueba de rojo, gcc y CVE en vivo.
set -u
R=/workspace/rea
cd "$R" || exit 1
printf '%s\n' '#!/bin/sh' '# REA 6.4.0 aislado: HOME propio y entorno minimo (2026-10-13-022).' '# Uso: /workspace/rea/rea <comando> [opciones]' 'exec env -i HOME=/workspace/rea/home PATH=/home/estudiante/.nvm/versions/node/v24.18.0/bin:/usr/bin:/bin /workspace/rea/node_modules/.bin/rea "$@"' > "$R/rea"
chmod +x "$R/rea"
echo "== wrapper"; cat "$R/rea"; md5sum "$R/rea"
echo "== wrapper --version"; "$R/rea" --version
echo "== puede dar rojo: archivo inexistente"
if "$R/rea" inspect-artifact /workspace/rea/no-existe.bin > /tmp/rea_rojo.out 2>&1; then echo "VERDE (mal: tenia que fallar)"; else echo "ROJO (bien: fallo como debia)"; fi
head -c 600 /tmp/rea_rojo.out; echo
echo "== puede dar verde con el wrapper: la caja"
if "$R/rea" inspect-artifact "$R/smoke/caja.stripped" --format json > /tmp/rea_verde.json 2>&1; then echo "VERDE"; else echo "ROJO"; fi
grep -o '"root_sha256":"[0-9a-f]*"' /tmp/rea_verde.json | head -1
sha256sum "$R/smoke/caja.stripped"
echo "== gcc"; /usr/bin/gcc --version | head -1
echo "== npm audit (CVE en vivo, dependencias de produccion)"
export PATH=/home/estudiante/.nvm/versions/node/v24.18.0/bin:/usr/bin:/bin
npm audit --omit=dev 2>&1 | tail -12
echo "== md5 y tamano"; md5sum package-lock.json package.json install.sh smoke.sh; du -sh "$R"
```

## QA (configuración)

Aplican Completitud, Ejecutabilidad, Seguridad, Documentación y Proceso QA: 60 puntos. Testing, Arquitectura, DevOps e Innovación (40 puntos) quedan N/A porque es una instalación, no código ni deployment.

| criterio | puntos | evidencia |
|---|---|---|
| Completitud | 14/15 | instalado y verificado (`exit_install=0`, `6.4.0`, lanzador `ea2c60ed`); −1 porque `doctor` da `healthy: false` |
| Ejecutabilidad | 14/15 | `/workspace/rea/rea <comando>` funciona tal cual: VERDE sobre la caja, ROJO sobre un inexistente; −1 porque solo corrió el camino sin motor y el host figura como no soportado |
| Seguridad | 13/15 | versión exacta, integridad, 144 firmas, 32 attestations, 0 scripts, 0 vulnerabilidades, HOME aislado, sin `setup`; −2 por el aislamiento parcial frente a `kaggle.json` y 112 paquetes sin attestation |
| Documentación | 9/10 | este archivo y su Doc; −1 porque el inventario canónico quedó sin corregir |
| Proceso QA | 5/5 | cada puntaje cita una salida o un md5 de esta página |
| **total** | **55/60 = 91,7 %** | sobre el umbral de 90 |

## NO MEDIDO

- Que REA saque funciones, llamadas o pseudocódigo en esta máquina: sin motor nativo no se corrió.
- Que REA con Ghidra funcione en Debian 13: `doctor` lo marca como host no soportado.
- Que ningún paquete del árbol lea `kaggle.json`: el aislamiento es por HOME, no por usuario.
- Si `/root/.kaggle/kaggle.json` sigue existiendo: sin root no se puede mirar.
- Que el gcc del sistema sirva para el C99 real de DualBrain: se probó con la caja de 18 líneas.
- El soporte de objdump o Rizin en 6.4.0: el `grep` dio vacío y no se probó contra un positivo.
- `rea setup` y su efecto sobre el Claude Code de brain-env.

## Antes de firmar

| afirmación | instrumento | ¿podía dar rojo? | veredicto |
|---|---|---|---|
| REA 6.4.0 instalado | `npm install` y `rea --version` | sí | medido, bien |
| es el paquete oficial | integridad del lock y `npm audit signatures` | sí | medido, bien |
| no corrió código ajeno al instalar | `--ignore-scripts` y escaneo de hooks | sí, si hubiera hooks | medido, bien (0) |
| sin vulnerabilidades conocidas | `npm audit --omit=dev` | sí | medido, bien (0) |
| REA analiza acá | `inspect-artifact` contra `sha256sum`, más un caso inexistente | sí, y dio rojo donde debía | medido, bien |
| REA mira funciones acá | ninguno | no se corrió | NO MEDIDO |
| las credenciales están a salvo | HOME aislado | no | NO MEDIDO |
| C nativo corre en brain-env | gcc 14.2 y ejecución de la caja | sí: exit 0 y 1 según el código | medido, bien (programa chico) |

## Archivos

- Este archivo.
- En brain-env, sin commitear porque son derivados: `/workspace/rea` (97 MB), con `package.json` `3d191771eeeb84264daf341d7ead9c54`, `package-lock.json` `fee8b769540ec5bf30bdca4e894925c5`, `install.log`, `smoke/` y el lanzador `rea` `ea2c60edb1289c5d77a3b81ce712ea02`.
- El CONTEXTO del proyecto no cambia. `CONTEXTO-ENTORNO.md` y `00-ENTORNOS-Y-CAPACIDADES.md` quedan pendientes de corregir (ver «De paso»).

```
--- METODO PROMETEO ---
Accion delicada: si (instala codigo de terceros en una maquina con credenciales; autorizado por el pedido explicito de Abraham a las 22:14). Mitigacion: version exacta, registry oficial, firmas e integridad verificadas, --ignore-scripts, npm audit, HOME aislado, sin rea setup
Maquina: brain-env (gateway build.run, 12 llamadas; escritura solo en /workspace/rea y /tmp) | registry de npm (desde brain-env) | API de GitHub (lectura de la release de Ghidra; escritura de este archivo)
QA: 55/60 = 91,7% sobre los criterios aplicables; 40 pts N/A (Testing, Arquitectura, DevOps, Innovacion: es configuracion)
Artefactos: docs/agents/respuestas/2026-10-13-022-rea-instalado-en-brain-env-aislado-sin-motor-nativo.md + Doc de ClickUp 2026-10-13-022
```
