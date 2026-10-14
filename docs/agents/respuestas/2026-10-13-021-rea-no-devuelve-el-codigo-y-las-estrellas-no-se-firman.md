# 2026-10-13-021 · REA es real pero no devuelve el código fuente; las estrellas no se firman y para nosotros vale como prueba sobre un binario propio

## Veredicto

- **[MEDIDO] Existe y es lo que cuenta el video.** `morluto/rea`, licencia MIT, TypeScript, creado el 14-abr-2026, web rea.tools. Es un servidor MCP más una CLI que le da al agente (Claude Code, Codex, Cursor y otros) las herramientas de ingeniería inversa de siempre.
  - Binarios nativos con Ghidra, Hopper o IDA, y en modo offline con objdump o Rizin.
  - Además JS/Electron, .NET, APK de Android (JADX), firmware, webs, WASM, bytecode EVM y capturas de red.
- **[FUENTE: README] No devuelve tu código fuente.** Devuelve pseudocódigo, ensamblador, cadenas, símbolos, llamadas y referencias, cada hallazgo con su evidencia y sus límites. Con eso el agente escribe una versión propia y la prueba. Lo dice el video con la imagen de la cocina: la libreta del cocinero no sale del plato.
- **[MEDIDO] Las estrellas no se firman como adopción.** 207.707 hoy por la API de GitHub contra 141.304 que el video leyó el 12-oct: **+66.403**. El README todavía agradece 180.000. El propio autor del video avisa que huele a bots.
- **[FUENTE: release] La actividad sí es real.** La 6.4.0 del 11-oct declara 336 commits y 163 PRs mergeados, y suma inspección de dispositivos Android por ADB, como dice el video.
- **[FUENTE: video] Su prueba está bien diseñada.** Binario propio, optimizado y sin nombres: 242 funciones y pico, todas `FUN_` más la dirección. El agente encontró la verificación y escribió un generador; el código `ANT-11001` abrió la caja. Lo valioso no es el truco: el que prueba conoce la respuesta, así que el instrumento podía dar rojo.

## Qué significa para nosotros

- **[CONCLUSIÓN] Para el conectoma, nada.** Todo lo nuestro tiene fuente.
- **[CONCLUSIÓN] El método ya es el nuestro.** Su esquema «código, referencias e incógnitas» es nuestro MEDIDO, CONCLUSIÓN y NO MEDIDO. Y su caso DX-Ball pasa 3.205 casos contra el x86 original y reproduce los 63 bytes compilados: oráculo byte a byte. Esa es la vara que a HC-5 todavía le falta (vectores golden cross-language, issue #12 de mojo-absoluto).
- **[PROPUESTA] La única prueba que vale la pena, con falsador.** Compilar dbc3-link sin símbolos y pedirle a REA, sin fuente, el formato del frame (296 B, align 8), el HMAC-SHA256 y el anti-replay.
  - Sabemos la respuesta, así que puede dar rojo.
  - Si lo saca: REA anda sobre nuestro stack, y cualquiera puede leer nuestro protocolo en un binario de edge (HC-6). La seguridad tiene que estar en las claves, no en que cueste leer el binario.
  - Si encuentra una clave embebida, el FAIL es nuestro.
  - Idea lateral para HC-5: REA lee de un binario Rust las dependencias que embebe `cargo-auditable`. Compilando la parte Rust con eso, la procedencia queda verificable desde el binario con un instrumento ajeno (W-01).
- **[MEDIDO] Dónde no correrlo: brain-env.** Tiene Node 24.18 y objdump, que alcanzan para la inspección offline, pero tiene `kaggle.json` en el home: no es un sandbox sin credenciales. Ghidra, Rizin, JADX, rustc y mojo no están en el PATH del gateway.
- **[CONCLUSIÓN] Plata, separado.** Cash probable: ninguno. Bounty: programas de apps móviles o de escritorio que permitan ingeniería inversa en su alcance. Premio especulativo: CTF.
- **[CONCLUSIÓN] Riesgo antes de instalar.**
  - `npx rea-agents setup` reescribe la configuración MCP de tus agentes.
  - El README avisa que hay copias con nombre parecido que no son oficiales.
  - Un binario ajeno puede traer instrucciones escondidas para el agente; el video lo advierte.
  - Si se prueba: entorno descartable sin credenciales, versión fija `rea-agents@6.4.0` y sólo binarios nuestros. Con binarios ajenos hay además tema legal (el video cita el artículo 6 de la directiva europea, interoperabilidad); con uno propio, no.
- **[OPINIÓN] Hoy no.** El Paper 1 v2 espera el merge y el token de Zenodo (Doc 014) y el factorial 4 está corriendo (Doc 016). REA no mueve ninguna de las dos. Queda anotado para cuando el readout vaya a edge.

## Pedido

22:01: «rea mira esto https://youtu.be/GitbDhOPBGs»

## Herramientas y máquina

- Web: página del video (texto y transcripción), oEmbed de YouTube (título y canal), dos búsquedas (una por el ID del video, que vino con ruido, y otra por REA).
- API de GitHub, sólo lectura: ficha de `morluto/rea`, su `README.md` y la última release; en nuestros repos, el listado de respuestas, la 020, los últimos commits y el CONTEXTO de mojo-absoluto.
- brain-env por el gateway (servicio `build`, herramienta `run`): dos sondas de sólo lectura. Versiones de Node y npm, motores en el PATH, existencia de credenciales sin leer valores, archivos de dbc3-link. La primera tuvo un bug y se descartó en parte (ver evidencia).
- Escrituras: este archivo y el Doc de ClickUp 2026-10-13-021. Nada instalado ni corrido. Sin cuota de Kaggle ni de GPU.

## Qué se midió

| dato | número | instrumento |
|---|---|---|
| estrellas de morluto/rea | 207.707 | API de GitHub, `repo:morluto/rea`, 13-oct ~22:05 ART |
| forks | 50.718 | ídem |
| issues abiertos | 558 | ídem |
| creado | 2026-04-14T00:51:32Z | ídem |
| estrellas según el video (12-oct) | 141.304 | transcripción |
| diferencia | +66.403 | resta |
| estrellas según el README | 180.000 | `README.md`, blob `0088640d` |
| última release | rea-agents-6.4.0, 2026-10-11T03:58:03Z | API de releases |
| Node y npm en brain-env | v24.18.0 y 11.16.0 (REA pide >=24.11) | `node --version`, `npm --version` |
| objdump en brain-env | `/usr/bin/objdump` | `command -v` en el gateway |
| credenciales en brain-env | `kaggle.json` presente | `test -e ~/.kaggle/kaggle.json` |

## Evidencia cruda

API de GitHub, `search_repositories` con `repo:morluto/rea` (campos seleccionados, valores sin editar):

```
"created_at":"2026-04-14T00:51:32Z","description":"Reverse engineer anything with agents, from app behavior down to native binaries.","forks_count":50718,"full_name":"morluto/rea","homepage":"https://rea.tools","language":"TypeScript","license":{"key":"mit","name":"MIT License","spdx_id":"MIT"},"open_issues_count":558,"pushed_at":"2026-10-14T00:51:46Z","stargazers_count":207707,"updated_at":"2026-10-14T01:02:43Z"
```

oEmbed del video:

```
{"title":"El Repositorio Que M\u00e1s R\u00e1pido Sube En GitHub Da Un Poco De Miedo: REA","author_name":"Jorge Marfil","author_url":"https://www.youtube.com/@jorgemarfil_ia","type":"video", ...}
```

Transcripción (texto de la página de youtu.be/GitbDhOPBGs):

```
«Yo he mirado la ficha del repositorio hoy, 12 de octubre y marca 141,304 estrellas y 32,407 forks en un proyecto que se creó el 14 de abril.»
«alguien contestó que eso olía a bots y yo no sé cuántas de esas estrellas son personas»
«Lo primero que le vuelve es una lista de 242 funciones y pico y ninguna tiene nombre.»
«Me escribió un pequeño generador de códigos y me dio uno. ANT-11001. Lo tecleé en la caja fuerte, me dejó pasar»
«de instrucciones escondidas en el binario no dice nada, así que esa precaución corre de vuestra cuenta»
```

`README.md` de morluto/rea (blob `0088640d077ed92f5dfb6cc60321dcc0724f7c26`, commit `41a2e846470bd2af40dd298d975b1a1d2fef5786`):

```
Native analysis returns pseudocode and assembly. JavaScript/Electron analysis
recovers modules and their relationships.

A similar repository name or copied README does not establish that a download is official.

The reconstruction passes 3,205 original-x86 cases and reproduces all 63 compiled function bytes.

| Rust binaries | Embedded cargo-auditable crate names, versions, sources and dependency edges |

REA requires Node.js 22.x (>=22.19), 24.x (>=24.11), or 26+, plus npm.

For offline native-binary inspection, REA also supports caller-supplied GNU objdump and Rizin.

🎉 **180,000 GitHub stars — thank you!**
```

Última release:

```
"name":"rea-agents: v6.4.0","published_at":"2026-10-11T03:58:03Z","tag_name":"rea-agents-6.4.0"
- Android: added device inspection, split-APK acquisition, logs, screenshots, file transfers and explicit app lifecycle actions through ADB, plus manifest and localized-string decoding with Apktool.
Full contribution record: [336 commits and 163 merged PRs]
```

brain-env, sonda 1 (exit=0). El bucle `for` salió roto: las variables se expandieron vacías antes de llegar al container (`: : :` y `ausente: ` sin nombre). Esa parte se descartó; máquina, Node, npm y Java no dependían del bucle:

```
== maquina
x86_64
PRETTY_NAME="Debian GNU/Linux 13 (trixie)"
== node/npm
v24.18.0
11.16.0
== motores
: : : : : : : : : openjdk version "17.0.20" 2026-07-21
== credenciales (solo existencia)
ausente: 
ausente: 
ausente: 
== dbc3-link
/workspace/mojo-absoluto
/workspace/mojo-absoluto/contracts/dbc3_link_frame.mojo
/workspace/mojo-absoluto/contracts/dbc3_link_manifest.json
/workspace/mojo-absoluto/contracts/dbc3_link_frame.rs
/workspace/mojo-absoluto/src/dbc3_link_wire.py
(...)
```

brain-env, sonda 2 (exit=0), sin variables:

```
== motores y compiladores
/usr/bin/objdump
rizin: NO
ghidraRun: NO
analyzeHeadless: NO
ghidra en /opt: NO
jadx: NO
/usr/bin/strip
cargo: NO
rustc: NO
/usr/bin/gcc
g++: NO
cmake: NO
mojo: NO
== credenciales (solo existencia, sin valores)
/workspace/homebrain
kaggle.json: presente
git-credentials: ausente
gh hosts.yml: ausente
remotes con credencial embebida: 0
nombres de variables con TOKEN/KEY/SECRET:
GPG_KEY
```

## Archivos

- Este archivo. El CONTEXTO no cambia de estado.

## NO MEDIDO

- REA corriendo sobre cualquier binario: no se instaló ni se corrió nada.
- Que REA, con sólo objdump, saque el formato del frame de dbc3-link: sin Ghidra no hay pseudocódigo.
- Si dbc3-link embebe alguna clave en su binario.
- Si cmake, g++, rustc o mojo existen en brain-env fuera del PATH del gateway. El CONTEXTO de mojo-absoluto dice que CTest corrió ahí, así que el `NO` de la sonda puede ser sólo PATH.
- Cuántas de las 207.707 estrellas son personas.
- La prueba de la caja fuerte: es el relato del video, no la repetimos.
- Si `DISCLAIMER.md` o `SECURITY.md` de REA hablan de instrucciones escondidas en binarios (el video dice que el aviso legal no).
- Qué programas de bounty permiten ingeniería inversa y pagan a Argentina.

## Antes de firmar

| afirmación | instrumento | ¿podía dar rojo? |
|---|---|---|
| REA existe, MIT, creado el 14-abr | API de GitHub | sí: si el repo no existiera o la fecha no coincidiera con el video |
| 207.707 estrellas, +66.403 desde el video | API de GitHub contra la cifra del video | sí: si la API diera 141.304 o menos |
| no devuelve el código fuente | README, FAQ «What code does REA return?» | sí, si dijera que reconstruye la fuente; pero es la palabra del proyecto, no un instrumento ajeno |
| la 6.4.0 del 11-oct suma Android por ADB | release de GitHub | sí: si fecha o contenido no coincidieran con el video |
| brain-env no es sandbox sin credenciales | `test -e ~/.kaggle/kaggle.json` | sí: si diera ausente |
| motores ausentes en brain-env | `command -v` en el gateway | parcial: mide el PATH del gateway, no la máquina; la primera sonda ni eso y se descartó |
| las estrellas no son adopción | resta y aviso del propio video | no: la resta mide velocidad, no bots |
| la prueba de dbc3-link vale la pena | propuesta | no es medición |

```
--- METODO PROMETEO ---
Accion delicada: no (lectura; nada instalado ni corrido; dos sondas de solo lectura en brain-env)
Maquina: web (pagina del video, oEmbed, 2 busquedas) | API de GitHub (lectura de morluto/rea) | brain-env (2 sondas: node, motores en el PATH, existencia de credenciales sin valores)
Artefactos: docs/agents/respuestas/2026-10-13-021-rea-no-devuelve-el-codigo-y-las-estrellas-no-se-firman.md + Doc de ClickUp 2026-10-13-021
```
