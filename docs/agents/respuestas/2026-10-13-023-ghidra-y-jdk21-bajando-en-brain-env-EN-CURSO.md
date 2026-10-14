# 2026-10-13-023 · Ghidra 12.1.4 y JDK 21 bajando en brain-env, en segundo plano: la red de la máquina da ~145 KB/s y termina cerca de las 00:20 · EN CURSO

## Veredicto

- **[MEDIDO] Está corriendo.** `install.sh` (md5 `12dc164d82786f965e9f02d348c3662d`) arrancó a las 01:39:48Z (22:39:48 ART) en segundo plano. El JDK crece en disco: 6.918.144 B a las 01:40:26Z, 12.595.200 B a las 01:41:06Z, 15.085.568 B a las 01:41:24Z.
- **[MEDIDO] La red de brain-env es lenta:** ~142 KB/s entre las dos primeras lecturas (5.677.056 B en 40 s), ~1,1 Mbit/s. Es la primera vez que se mide la velocidad; el inventario solo decía que había salida.
- **[CUENTA] Cuándo termina.** Hay que bajar 207.473.347 B del JDK y 569.649.598 B de Ghidra, unos 777 MB. A ~145 KB/s son ~22 min de JDK y ~65 min de Ghidra, más la extracción en el Celeron: **cerca de las 00:20 ART**, entre 00:00 y 00:45 según la red. Coincide con el factorial 4.
- **[DISEÑO] Qué hace el script, sin que nadie lo toque:**
  1. JDK Temurin 21.0.12.1+1: baja el `.tar.gz` y su `.sha256.txt`, verifica con `sha256sum -c` y **corta si no coincide**.
  2. Ghidra 12.1.4: baja el zip y compara con el SHA-256 publicado (`ddac49f9...2d4db`, el mismo en el cuerpo de la release y en el `digest` del asset); **corta si no coincide**.
  3. Extrae con Python conservando los permisos (no hay `unzip`), borra los dos archivos ya verificados y guarda el lanzador viejo como `rea.sin-motor`.
  4. Reescribe `/workspace/rea/rea` con `JAVA_HOME` y `GHIDRA_INSTALL_DIR`, y corre `rea doctor`.
- **[PENDIENTE] La prueba que puede dar rojo,** cuando termine: pedirle a REA con Ghidra que encuentre en la caja sin nombres la regla que conocemos («MDH-» más 5 dígitos que suman 21) y generar un código que abra. Si no la encuentra, o el host Debian 13 lo frena, se dice.

## Pedido

22:38: botón «Instalá Ghidra 12.1.4» de la respuesta 022.

## Herramientas y máquina

- **brain-env** por el gateway, 5 llamadas: consulta de las releases (API de GitHub con `curl`), memoria y disco, lanzamiento en segundo plano y tres lecturas de avance.
- **Escritura:** solo bajo `/workspace/rea/engines` y, al final, el lanzador `/workspace/rea/rea` (con copia `rea.sin-motor`).
- **Red:** github.com (Adoptium y NSA), unos 777 MB. Sin cuota de Kaggle ni de GPU.
- Este archivo y el Doc de ClickUp 2026-10-13-023.

## Evidencia cruda

Releases (desde brain-env):

```
== ghidra assets
"name": "Ghidra 12.1.4"
"name": "ghidra_12.1.4_PUBLIC_20260921.zip"
"size": 569649598
"digest": "sha256:ddac49f903da9d5bac833e5cc79395098b9c33cfd3279be5f31bd00387d2d4db"
"browser_download_url": "https://github.com/NationalSecurityAgency/ghidra/releases/download/Ghidra_12.1.4_build/ghidra_12.1.4_PUBLIC_20260921.zip"
== temurin 21 latest
"tag_name": "jdk-21.0.12.1+1"
"browser_download_url": "https://github.com/adoptium/temurin21-binaries/releases/download/jdk-21.0.12.1%2B1/OpenJDK21U-jdk_x64_linux_hotspot_21.0.12.1_1.tar.gz"
"browser_download_url": "https://github.com/adoptium/temurin21-binaries/releases/download/jdk-21.0.12.1%2B1/OpenJDK21U-jdk_x64_linux_hotspot_21.0.12.1_1.tar.gz.sha256.txt"
== memoria
MemTotal:        7989556 kB
MemFree:          362820 kB
MemAvailable:    2863980 kB
2
/dev/sda4       406G  301G   86G  78% /workspace
```

Lanzamiento y avance:

```
12dc164d82786f965e9f02d348c3662d  /workspace/rea/engines/install.sh
== inicio 2026-10-14T01:39:48Z
== JDK 21: descarga

01:40:26   6918144 OpenJDK21U-jdk_x64_linux_hotspot_21.0.12.1_1.tar.gz
01:41:06  12595200 OpenJDK21U-jdk_x64_linux_hotspot_21.0.12.1_1.tar.gz
content-length: 207473347
01:41:24  15085568 OpenJDK21U-jdk_x64_linux_hotspot_21.0.12.1_1.tar.gz
/proc/29970/cmdline
/proc/29996/cmdline
/proc/30010/cmdline
```

## El instrumento, verbatim

`/workspace/rea/engines/install.sh` (md5 `12dc164d82786f965e9f02d348c3662d`); el log queda en `/workspace/rea/engines/install.log`:

```bash
#!/usr/bin/env bash
# Instala JDK 21 (Temurin 21.0.12.1+1) y Ghidra 12.1.4 en /workspace/rea/engines, con sha256 verificado,
# y apunta el lanzador de REA a los dos (2026-10-13-023).
set -u
R=/workspace/rea
E=$R/engines
LOG=$E/install.log
mkdir -p "$E"
cd "$E" || exit 1
exec > "$LOG" 2>&1
JDK_URL='https://github.com/adoptium/temurin21-binaries/releases/download/jdk-21.0.12.1%2B1/OpenJDK21U-jdk_x64_linux_hotspot_21.0.12.1_1.tar.gz'
JDK_TGZ=OpenJDK21U-jdk_x64_linux_hotspot_21.0.12.1_1.tar.gz
GH_URL='https://github.com/NationalSecurityAgency/ghidra/releases/download/Ghidra_12.1.4_build/ghidra_12.1.4_PUBLIC_20260921.zip'
GH_ZIP=ghidra_12.1.4_PUBLIC_20260921.zip
GH_SHA=ddac49f903da9d5bac833e5cc79395098b9c33cfd3279be5f31bd00387d2d4db
echo "== inicio $(date -u +%FT%TZ)"
echo "== JDK 21: descarga"
curl -fsSL -o "$JDK_TGZ" "$JDK_URL"; echo "exit_curl_jdk=$?"
curl -fsSL -o "$JDK_TGZ.sha256.txt" "$JDK_URL.sha256.txt"; echo "exit_curl_jdk_sha=$?"
cat "$JDK_TGZ.sha256.txt"
if sha256sum -c "$JDK_TGZ.sha256.txt"; then echo "JDK_SHA_OK"; else echo "JDK_SHA_FALLA"; exit 2; fi
tar -xzf "$JDK_TGZ"; echo "exit_tar=$?"
JDK_DIR=$(ls -d "$E"/jdk-21* | head -1)
echo "JDK_DIR=$JDK_DIR"
"$JDK_DIR/bin/java" -version
echo "== Ghidra 12.1.4: descarga $(date -u +%FT%TZ)"
curl -fsSL -o "$GH_ZIP" "$GH_URL"; echo "exit_curl_ghidra=$?"
ls -l "$GH_ZIP"
GOT=$(sha256sum "$GH_ZIP" | cut -d' ' -f1)
echo "sha256 esperado: $GH_SHA"
echo "sha256 obtenido: $GOT"
if [ "$GOT" = "$GH_SHA" ]; then echo "GHIDRA_SHA_OK"; else echo "GHIDRA_SHA_FALLA"; exit 3; fi
echo "== extraccion con permisos $(date -u +%FT%TZ)"
python3 - "$GH_ZIP" "$E" <<'PY'
import os, sys, zipfile
zpath, dest = sys.argv[1], sys.argv[2]
n = ex = 0
with zipfile.ZipFile(zpath) as z:
    for info in z.infolist():
        out = z.extract(info, dest)
        mode = (info.external_attr >> 16) & 0o777
        if mode and not info.is_dir():
            os.chmod(out, mode)
            if mode & 0o111:
                ex += 1
        n += 1
print('entradas extraidas:', n, '| con bit ejecutable:', ex)
PY
echo "exit_unzip=$?"
GH_DIR=$(ls -d "$E"/ghidra_12.1.4_PUBLIC | head -1)
echo "GH_DIR=$GH_DIR"
ls -l "$GH_DIR/support/analyzeHeadless" "$GH_DIR/ghidraRun"
ls -l "$GH_DIR/Ghidra/Features/Decompiler/os/linux_x86_64/" 2>&1
file "$GH_DIR/Ghidra/Features/Decompiler/os/linux_x86_64/decompile" 2>&1
grep -E '^application\.version|^application\.release\.name' "$GH_DIR/Ghidra/application.properties"
grep -E '^application\.java\.min' "$GH_DIR/Ghidra/application.properties"
echo "== limpieza de los archivos ya verificados"
rm -f "$GH_ZIP" "$JDK_TGZ"
du -sh "$JDK_DIR" "$GH_DIR"
echo "== lanzador de REA con motor"
cp "$R/rea" "$R/rea.sin-motor"
printf '%s\n' '#!/bin/sh' '# REA 6.4.0 aislado, con JDK 21 y Ghidra 12.1.4 (2026-10-13-023).' '# Uso: /workspace/rea/rea <comando> [opciones]' "exec env -i HOME=$R/home JAVA_HOME=$JDK_DIR GHIDRA_INSTALL_DIR=$GH_DIR PATH=$JDK_DIR/bin:/home/estudiante/.nvm/versions/node/v24.18.0/bin:/usr/bin:/bin $R/node_modules/.bin/rea \"\$@\"" > "$R/rea"
chmod +x "$R/rea"
cat "$R/rea"; md5sum "$R/rea"
echo "== doctor"
"$R/rea" doctor 2>&1 | head -60
echo "== fin $(date -u +%FT%TZ)"
```

## NO MEDIDO

- Que las dos descargas terminen y que las huellas coincidan: corre solo y se lee después.
- La firma GPG del JDK (`.sig`): se verifica integridad con el sha256 de la misma release, no autoría.
- Que Ghidra arranque con la RAM disponible (2,86 GB al medir) en un Celeron de 2 núcleos.
- Que REA acepte Ghidra en Debian 13, que `doctor` marca como no soportado.
- Que REA encuentre la regla de la caja.

## Antes de firmar

| afirmación | instrumento | ¿podía dar rojo? | veredicto |
|---|---|---|---|
| la descarga está avanzando | tamaño del archivo en tres momentos | sí, si no creciera | medido, bien |
| la red da ~145 KB/s | dos tamaños y `date -u` | sí | medido (ventana de 40 s) |
| termina cerca de las 00:20 | cuenta sobre esa velocidad | no | estimación, no medición |
| lo que se instale va a ser lo oficial | el script corta si el sha256 no coincide | sí, por diseño | se mide al terminar |

## Archivos

- Este archivo. El instrumento está copiado arriba; el log se lee al cierre en una respuesta nueva.

```
--- METODO PROMETEO ---
Accion delicada: si (baja e instala binarios de terceros en una maquina con credenciales: JDK de Adoptium y Ghidra de la NSA, releases oficiales con sha256 verificado; autorizado con el clic instalar_ghidra_1214)
Maquina: brain-env (gateway build.run, 5 llamadas; escritura en /workspace/rea/engines y el lanzador) | github.com (descargas)
QA: al cierre, cuando termine la instalacion
Artefactos: docs/agents/respuestas/2026-10-13-023-ghidra-y-jdk21-bajando-en-brain-env-EN-CURSO.md + Doc de ClickUp 2026-10-13-023
```
