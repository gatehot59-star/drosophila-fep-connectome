# 2026-10-14-016: REA y Ghidra instalados y probados por consola

## 1. Pedido

«REVISA COMO QUEDO INSTALADO REA Y GHIDRA».

## 2. Herramientas y maquina

GitHub conectado: lectura de inventario, metodo, recibos 022/023 del 13-oct y ultima respuesta 015 del 14-oct, con HEAD `3576311e2569ae5cdeebab68fac75f75d328af87`. ClickUp: documentos previos y nuevo Doc. Gateway MUDH: lectura de estado compartido y ejecucion directa en brain-env mediante Python/subprocess y shell. Sin mensajes pendientes para BRAIN; sin entrada especifica de REA/Ghidra en estado. No se lanzaron experimentos en Actions/Kaggle ni agentes auxiliares.

Se crearon temporales de diagnostico en `/tmp/rea-ghidra-audit-20261014-uz33o6wd`, un snapshot y los proyectos efimeros del proveedor. No se ejecuto setup, no se reinstalo ni se edito el lanzador. Los procesos de inspeccion y descompilacion terminaron. Hubo fallos transitorios del canal de ejecucion; se recuperaron los resultados existentes sin relanzar las dos corridas largas.

## 3. Que se midio

PASS: REA 6.4.0, JDK 21.0.12.1+1 y Ghidra 12.1.4 funcionan juntos por CLI sobre la caja propia. `inspect` exit 0: 29 procedimientos, 31 segmentos, 43 cadenas; `decompile` exit 0: recupera pseudocodigo de la regla MDH- y suma 21. Control de comportamiento: exit 0 para MDH-90093 y exit 1 para MDH-90092 y MDH-90A93. Objetivo inexistente: exit 1.

FAIL global: doctor general exit 1 por host Debian 13, Hopper, IDA e identidad del skill. PASS seleccionado: doctor con `--provider ghidra --target` exit 0 y healthy true, aunque environment_healthy sigue false.

Lectura historica: `install2.log` registra cierre 2026-10-14T02:11:59Z, equivalente a 13-oct 23:11:59 ART. No se revalidaron hoy los paquetes comprimidos originales.

## 4. Evidencia cruda

Las salidas de los comandos que sustentan el veredicto se preservan debajo, sin corregir sus advertencias. Los codigos de salida son de `subprocess.returncode`, no una expansion de `$?` por el transporte.

### A. Identidad y lanzador, leidos a 2026-10-14T19:45:44.020681+00:00

```text
uid: 1000
cpu_count: 2
MemTotal:        7989556 kB
MemAvailable:    2626640 kB
```

Comando: `/workspace/rea/rea --version`

```text
exit_code: 0
stdout: 6.4.0
stderr: vacio
```

Comando: `/workspace/rea/engines/jdk-21.0.12.1+1/bin/java -version`

```text
exit_code: 0
stdout: vacio
stderr:
openjdk version "21.0.12.1" 2026-08-18 LTS
OpenJDK Runtime Environment Temurin-21.0.12.1+1 (build 21.0.12.1+1-LTS)
OpenJDK 64-Bit Server VM Temurin-21.0.12.1+1 (build 21.0.12.1+1-LTS, mixed mode, sharing)
```

Contenido de `/workspace/rea/rea` (425 bytes, modo 0755, sha256 `0774630ce80f8ba1e3b90e60679e1ffa59d0e84eadbee3eb42b2d98cac2f8366`):

```sh
#!/bin/sh
# REA 6.4.0 aislado, con JDK 21 y Ghidra 12.1.4 (2026-10-13-023).
# Uso: /workspace/rea/rea <comando> [opciones]
exec env -i HOME=/workspace/rea/home JAVA_HOME=/workspace/rea/engines/jdk-21.0.12.1+1 GHIDRA_INSTALL_DIR=/workspace/rea/engines/ghidra_12.1.4_PUBLIC PATH=/workspace/rea/engines/jdk-21.0.12.1+1/bin:/home/estudiante/.nvm/versions/node/v24.18.0/bin:/usr/bin:/bin /workspace/rea/node_modules/.bin/rea "$@"
```

Contenido de `/workspace/rea/package.json` (73 bytes):

```json
{"name":"rea-local","private":true,"dependencies":{"rea-agents":"6.4.0"}}
```

### B. Doctor especifico, exit 0

Comando exacto:

```sh
/workspace/rea/rea doctor --provider ghidra --target /workspace/rea/smoke/caja.stripped --format json --filter-output healthy,environment_healthy,scope,scope_checks,providerInspections
```

stdout completo del comando con el filtro declarado; stderr vacio:

```json
{"healthy":true,"environment_healthy":false,"scope":{"mode":"explicit","clients":[],"providers":["ghidra"],"skill":false,"target":"/workspace/rea/smoke/caja.stripped"},"scope_checks":[{"name":"node","ok":true,"classification":"healthy","detail":"24.18.0"},{"name":"target","ok":true,"classification":"healthy","detail":"/workspace/rea/smoke/caja.stripped"},{"name":"ghidra","ok":true,"classification":"healthy","detail":"/workspace/rea/engines/ghidra_12.1.4_PUBLIC"},{"name":"ghidra-platform","ok":true,"classification":"healthy","detail":"linux"},{"name":"ghidra-architecture","ok":true,"classification":"healthy","detail":"x64"},{"name":"ghidra-installation","ok":true,"classification":"healthy","detail":"/workspace/rea/engines/ghidra_12.1.4_PUBLIC/Ghidra/application.properties"},{"name":"ghidra-version","ok":true,"classification":"healthy","detail":"12.1.4"},{"name":"ghidra-headless","ok":true,"classification":"healthy","detail":"/workspace/rea/engines/ghidra_12.1.4_PUBLIC/support/analyzeHeadless"},{"name":"ghidra-native_decompiler","ok":true,"classification":"healthy","detail":"/workspace/rea/engines/ghidra_12.1.4_PUBLIC/Ghidra/Features/Decompiler/os/linux_x86_64/decompile reports elf x86_64, which matches linux/x64"},{"name":"ghidra-java","ok":true,"classification":"healthy","detail":"21.0.12.1; 64-bit; JDK; /workspace/rea/engines/jdk-21.0.12.1+1; accepted a 64-bit full JDK 21 or newer"}],"providerInspections":[{"id":"ghidra","configured":true,"available":true,"providerVersion":"12.1.4","registrationEnvironment":{"GHIDRA_INSTALL_DIR":"/workspace/rea/engines/ghidra_12.1.4_PUBLIC","JAVA_HOME":"/workspace/rea/engines/jdk-21.0.12.1+1"},"checks":[{"name":"configuration","ok":true,"code":null,"detail":"/workspace/rea/engines/ghidra_12.1.4_PUBLIC","remediation":null,"classification":"config_drift"},{"name":"platform","ok":true,"code":null,"detail":"linux","remediation":null,"classification":"unsupported_host"},{"name":"architecture","ok":true,"code":null,"detail":"x64","remediation":null,"classification":"unsupported_host"},{"name":"installation","ok":true,"code":null,"detail":"/workspace/rea/engines/ghidra_12.1.4_PUBLIC/Ghidra/application.properties","remediation":null,"classification":"config_drift"},{"name":"version","ok":true,"code":null,"detail":"12.1.4","remediation":null,"classification":"config_drift"},{"name":"headless","ok":true,"code":null,"detail":"/workspace/rea/engines/ghidra_12.1.4_PUBLIC/support/analyzeHeadless","remediation":null,"classification":"config_drift"},{"name":"native_decompiler","ok":true,"code":null,"detail":"/workspace/rea/engines/ghidra_12.1.4_PUBLIC/Ghidra/Features/Decompiler/os/linux_x86_64/decompile reports elf x86_64, which matches linux/x64","remediation":null,"classification":"config_drift"},{"name":"java","ok":true,"code":null,"detail":"21.0.12.1; 64-bit; JDK; /workspace/rea/engines/jdk-21.0.12.1+1; accepted a 64-bit full JDK 21 or newer","remediation":null,"classification":"config_drift"}]},{"id":"ida","configured":false,"available":false,"providerVersion":null,"registrationEnvironment":{},"checks":[{"name":"registration","ok":false,"code":"not_configured","detail":"IDA MCP registration is not configured.","remediation":"Set REA_IDA_MCP_CONFIG to your upstream IDA MCP registration JSON; see docs/ida-provider.md.","classification":"missing_analysis_engine"}]}]}
```

### C. Inspeccion real con Ghidra

```sh
/workspace/rea/rea inspect /workspace/rea/smoke/caja.stripped --provider ghidra --snapshot /tmp/rea-ghidra-audit-20261014-uz33o6wd/caja.snapshot.json --format json
```

```text
started_utc: 2026-10-14T19:47:20.326691+00:00
ended_utc: 2026-10-14T19:48:10.810369+00:00
exit_code: 0
timed_out: false
stderr: vacio
```

stdout completo:

```json
{"evidence_id":"ev_118e277833e0ae09f7238a5c16e495b29edad90a268f987e176b8c70ed81e08b","subject":{"name":"caja.stripped","digest":{"sha256":"51c020e6b3f176552bdabe424e8898619588d9446873ac8d8120787d1a71e38e"},"format":"elf","architecture":"x86_64","local_path":"/workspace/rea/smoke/caja.stripped"},"provider":{"id":"rea-workflow","name":"REA composed investigation workflow","version":"1"},"analysis_profile":{"provider":{"id":"rea-workflow","name":"REA composed investigation workflow","version":"1"},"parameters":{"upstream_analysis_profile":{"provider":{"id":"ghidra","name":"Ghidra","version":"12.1.4"},"parameters":{"target_kind":"executable","target_format":"elf","architecture":"x86_64","available_architectures":["x86_64"],"import_mode":"ephemeral-source-immutable","annotation_policy":"atomic-function-entry-metadata-v1","load_image_observations":"source-mappings-entry-context-v2","function_body_evidence":"complete-inclusive-ranges-v1","function_references":"complete-body-and-entry-reference-manager-v2","string_inventory_evidence":"defined-data-coverage-v1","location_resolution":"explicit-address-exact-entry-symbol-first-v3","instruction_flow_evidence":"decoded-return-pcode-v1","function_boundary_observations":"ghidra-terminal-call-limitations-v1","no_return_repair":"returning-imports-decoded-return-v2","process_launch":"inspected-jvm-launch-support-v1","jump_table_evidence":"typed-case-default-blocks-v1","decompiler_jump_loads":true,"loader":"auto-from-header","language_id":"auto-from-header","compiler_spec_id":"auto-default","analyzer_preset":"ghidra-default"},"digest":"a04af771c3a78edf03c11c3b8652d4812dfce76da00d380345526a333361b5c9"},"workflow_revision":2},"digest":"068cf897494a9e2cc52ffa0cf75e27960f5ae322062fafcdb7ba78b19bcf8b9f"},"predicate_type":"rea.analysis","operation":"binary_overview","parameters":{},"raw_result":null,"normalized_result":{"document":"target-51c020e6b3f1.stripped","segments":[{"name":"segment_2.1","start":"0x100000","end":"0x100350","length":848},{"name":".note.gnu.property","start":"0x100350","end":"0x100370","length":32},{"name":".note.gnu.build-id","start":"0x100370","end":"0x100394","length":36},{"name":".interp","start":"0x100394","end":"0x1003b0","length":28},{"name":".gnu.hash","start":"0x1003b0","end":"0x1003d4","length":36},{"name":".dynsym","start":"0x1003d8","end":"0x1004b0","length":216},{"name":".dynstr","start":"0x1004b0","end":"0x10054c","length":156},{"name":".gnu.version","start":"0x10054c","end":"0x10055e","length":18},{"name":".gnu.version_r","start":"0x100560","end":"0x100590","length":48},{"name":".rela.dyn","start":"0x100590","end":"0x100650","length":192},{"name":".rela.plt","start":"0x100650","end":"0x100698","length":72},{"name":".init","start":"0x101000","end":"0x101017","length":23},{"name":".plt","start":"0x101020","end":"0x101060","length":64},{"name":".plt.got","start":"0x101060","end":"0x101068","length":8},{"name":".text","start":"0x101070","end":"0x1011e9","length":377},{"name":".fini","start":"0x1011ec","end":"0x1011f5","length":9},{"name":".rodata","start":"0x102000","end":"0x10202d","length":45},{"name":".eh_frame_hdr","start":"0x102030","end":"0x10205c","length":44},{"name":".eh_frame","start":"0x102060","end":"0x102114","length":180},{"name":".note.ABI-tag","start":"0x102114","end":"0x102134","length":32},{"name":".init_array","start":"0x103dd0","end":"0x103dd8","length":8},{"name":".fini_array","start":"0x103dd8","end":"0x103de0","length":8},{"name":".dynamic","start":"0x103de0","end":"0x103fc0","length":480},{"name":".got","start":"0x103fc0","end":"0x103fe8","length":40},{"name":".got.plt","start":"0x103fe8","end":"0x104018","length":48},{"name":".data","start":"0x104018","end":"0x104028","length":16},{"name":".bss","start":"0x104028","end":"0x104030","length":8},{"name":"EXTERNAL","start":"0x105000","end":"0x105040","length":64},{"name":".comment","start":".comment:0x0","end":".comment:0x1f","length":31},{"name":".shstrtab","start":".shstrtab:0x0","end":".shstrtab:0x10a","length":266},{"name":"_elfSectionHeaders","start":"_elfSectionHeaders:0x0","end":"_elfSectionHeaders:0x740","length":1856}],"segment_count":31,"procedure_count":29,"string_count":43},"confidence":"derived","authority":"shipped-artifact","environment":null,"limitations":["Derived by an REA composed workflow."],"locations":[],"evidence_links":[]}
```

### D. Descompilacion real

```sh
/workspace/rea/rea decompile /workspace/rea/smoke/caja.stripped 0x101070 --provider ghidra --snapshot /tmp/rea-ghidra-audit-20261014-uz33o6wd/caja.snapshot.json --format json
```

```text
started_utc: 2026-10-14T19:49:32.276037+00:00
ended_utc: 2026-10-14T19:51:30.033203+00:00
exit_code: 0
timed_out: false
stderr: vacio
```

stdout completo:

```json
{"evidence_id":"ev_59da9b31c0b4cc9989c80842cad29700409c4e93823e181e369f9bd4cf48c598","subject":{"name":"caja.stripped","digest":{"sha256":"51c020e6b3f176552bdabe424e8898619588d9446873ac8d8120787d1a71e38e"},"format":"elf","architecture":"x86_64","local_path":"/workspace/rea/smoke/caja.stripped"},"provider":{"id":"ghidra","name":"Ghidra","version":"12.1.4"},"analysis_profile":{"provider":{"id":"ghidra","name":"Ghidra","version":"12.1.4"},"parameters":{"target_kind":"executable","target_format":"elf","architecture":"x86_64","available_architectures":["x86_64"],"import_mode":"ephemeral-source-immutable","annotation_policy":"atomic-function-entry-metadata-v1","load_image_observations":"source-mappings-entry-context-v2","function_body_evidence":"complete-inclusive-ranges-v1","function_references":"complete-body-and-entry-reference-manager-v2","string_inventory_evidence":"defined-data-coverage-v1","location_resolution":"explicit-address-exact-entry-symbol-first-v3","instruction_flow_evidence":"decoded-return-pcode-v1","function_boundary_observations":"ghidra-terminal-call-limitations-v1","no_return_repair":"returning-imports-decoded-return-v2","process_launch":"inspected-jvm-launch-support-v1","jump_table_evidence":"typed-case-default-blocks-v1","decompiler_jump_loads":true,"loader":"auto-from-header","language_id":"auto-from-header","compiler_spec_id":"auto-default","analyzer_preset":"ghidra-default"},"digest":"a04af771c3a78edf03c11c3b8652d4812dfce76da00d380345526a333361b5c9"},"predicate_type":"rea.analysis","operation":"procedure_pseudo_code","parameters":{"procedure":"0x101070"},"raw_result":{"value":"\nundefined4 FUN_00101070(int param_1,long param_2)\n\n{\n  char cVar1;\n  char *__s;\n  int iVar2;\n  size_t sVar3;\n  char *pcVar4;\n  \n  if (1 < param_1) {\n    __s = *(char **)(param_2 + 8);\n    sVar3 = strlen(__s);\n    if ((sVar3 == 9) && (iVar2 = strncmp(__s,\"MDH-\",4), iVar2 == 0)) {\n      pcVar4 = __s + 4;\n      iVar2 = 0;\n      do {\n        cVar1 = *pcVar4;\n        if (9 < (byte)(cVar1 - 0x30U)) goto LAB_001010e0;\n        pcVar4 = pcVar4 + 1;\n        iVar2 = iVar2 + -0x30 + (int)cVar1;\n      } while (pcVar4 != __s + 9);\n      if (iVar2 == 0x15) {\n        puts(\"CAJA-021: abierta\");\n        return 0;\n      }\n    }\n  }\nLAB_001010e0:\n  puts(\"CAJA-021: cerrada\");\n  return 1;\n}\n\n","limitations":[]},"normalized_result":"\nundefined4 FUN_00101070(int param_1,long param_2)\n\n{\n  char cVar1;\n  char *__s;\n  int iVar2;\n  size_t sVar3;\n  char *pcVar4;\n  \n  if (1 < param_1) {\n    __s = *(char **)(param_2 + 8);\n    sVar3 = strlen(__s);\n    if ((sVar3 == 9) && (iVar2 = strncmp(__s,\"MDH-\",4), iVar2 == 0)) {\n      pcVar4 = __s + 4;\n      iVar2 = 0;\n      do {\n        cVar1 = *pcVar4;\n        if (9 < (byte)(cVar1 - 0x30U)) goto LAB_001010e0;\n        pcVar4 = pcVar4 + 1;\n        iVar2 = iVar2 + -0x30 + (int)cVar1;\n      } while (pcVar4 != __s + 9);\n      if (iVar2 == 0x15) {\n        puts(\"CAJA-021: abierta\");\n        return 0;\n      }\n    }\n  }\nLAB_001010e0:\n  puts(\"CAJA-021: cerrada\");\n  return 1;\n}\n\n","confidence":"observed","authority":"shipped-artifact","environment":null,"limitations":["The session serves operations only after Ghidra reports default auto-analysis complete; incomplete analysis does not expose partial results.","The imported Program and temporary project are ephemeral and deleted on close. Annotation operations edit session database metadata; original executable bytes are never written.","Cancelling an active Ghidra request terminates its ephemeral database and discards session annotations. The selected target remains open; the next provider query imports the original artifact again.","Default-space addresses use lowercase 0x-prefixed hexadecimal; other address spaces use <percent-encoded-space>:0x<hex>.","Pseudocode is Ghidra decompiler output, not original source and not text-equivalent to Hopper output.","External functions and functions without an analyzable body return null; other decompiler failures remain explicit."],"locations":[],"evidence_links":[]}
```

### E. Caso que debe fallar: archivo inexistente

```sh
/workspace/rea/rea inspect /tmp/rea-ghidra-audit-20261014-uz33o6wd/no-existe.bin --provider ghidra --format json
```

Exit 1, stderr vacio, stdout completo:

```json
{"error":"Analysis failed","code":"target_unavailable","category":"unavailable","message":"Cannot open artifact: target does not exist or a path component is not a directory: ENOENT: no such file or directory, access '/tmp/rea-ghidra-audit-20261014-uz33o6wd/no-existe.bin'. Check that the path exists, is readable, and points to a supported file.","retryable":false,"remediation":{"action":"Cannot open artifact: target does not exist or a path component is not a directory: ENOENT: no such file or directory, access '/tmp/rea-ghidra-audit-20261014-uz33o6wd/no-existe.bin'. Check that the path exists, is readable, and points to a supported file."},"details":{"path":"/tmp/rea-ghidra-audit-20261014-uz33o6wd/no-existe.bin","reason":"target does not exist or a path component is not a directory: ENOENT: no such file or directory, access '/tmp/rea-ghidra-audit-20261014-uz33o6wd/no-existe.bin'"}}
```

### F. La regla recuperada frente al ejecutable

Instrumento ejecutado:

```sh
python3 -c 'import subprocess,json; a=["/workspace/rea/smoke/caja.stripped","MDH-90093"]; b=["/workspace/rea/smoke/caja.stripped","MDH-90092"]; c=["/workspace/rea/smoke/caja.stripped","MDH-90A93"]; rs=[subprocess.run(x,capture_output=True,text=True,timeout=5) for x in [a,b,c]]; print(json.dumps([dict(argv=x.args,exit_code=x.returncode,stdout=x.stdout,stderr=x.stderr) for x in rs],indent=2))'
```

Salida completa (instrumento exit 0):

```json
[
  {
    "argv": [
      "/workspace/rea/smoke/caja.stripped",
      "MDH-90093"
    ],
    "exit_code": 0,
    "stdout": "CAJA-021: abierta\n",
    "stderr": ""
  },
  {
    "argv": [
      "/workspace/rea/smoke/caja.stripped",
      "MDH-90092"
    ],
    "exit_code": 1,
    "stdout": "CAJA-021: cerrada\n",
    "stderr": ""
  },
  {
    "argv": [
      "/workspace/rea/smoke/caja.stripped",
      "MDH-90A93"
    ],
    "exit_code": 1,
    "stdout": "CAJA-021: cerrada\n",
    "stderr": ""
  }
]
```

### G. Hashes posteriores y doctor general: rojo real

Comando completo:

```sh
sha256sum /workspace/rea/rea /workspace/rea/smoke/caja.stripped; /workspace/rea/rea doctor --format json --filter-output healthy,environment_healthy,scope_checks
```

Exit 1, por el doctor. stderr vacio. stdout completo:

```text
0774630ce80f8ba1e3b90e60679e1ffa59d0e84eadbee3eb42b2d98cac2f8366  /workspace/rea/rea
51c020e6b3f176552bdabe424e8898619588d9446873ac8d8120787d1a71e38e  /workspace/rea/smoke/caja.stripped
{"healthy":false,"environment_healthy":false,"scope_checks":[{"name":"node","ok":true,"classification":"healthy","detail":"24.18.0"},{"name":"host","ok":false,"classification":"unsupported_host","detail":"debian 13","remediation":"REA supports macOS 12+, Ubuntu 24.04+, Fedora 41+, Nobara 44+, 64-bit Arch Linux, CachyOS, Omarchy, and the experimental Windows x64 Ghidra P0 boundary."},{"name":"hopper","ok":false,"classification":"missing_analysis_engine","remediation":"Run rea setup to install Hopper, or set HOPPER_LAUNCHER_PATH."},{"name":"ghidra","ok":true,"classification":"healthy","detail":"/workspace/rea/engines/ghidra_12.1.4_PUBLIC"},{"name":"ghidra-platform","ok":true,"classification":"healthy","detail":"linux"},{"name":"ghidra-architecture","ok":true,"classification":"healthy","detail":"x64"},{"name":"ghidra-installation","ok":true,"classification":"healthy","detail":"/workspace/rea/engines/ghidra_12.1.4_PUBLIC/Ghidra/application.properties"},{"name":"ghidra-version","ok":true,"classification":"healthy","detail":"12.1.4"},{"name":"ghidra-headless","ok":true,"classification":"healthy","detail":"/workspace/rea/engines/ghidra_12.1.4_PUBLIC/support/analyzeHeadless"},{"name":"ghidra-native_decompiler","ok":true,"classification":"healthy","detail":"/workspace/rea/engines/ghidra_12.1.4_PUBLIC/Ghidra/Features/Decompiler/os/linux_x86_64/decompile reports elf x86_64, which matches linux/x64"},{"name":"ghidra-java","ok":true,"classification":"healthy","detail":"21.0.12.1; 64-bit; JDK; /workspace/rea/engines/jdk-21.0.12.1+1; accepted a 64-bit full JDK 21 or newer"},{"name":"ida-registration","ok":false,"classification":"missing_analysis_engine","detail":"IDA MCP registration is not configured.","remediation":"Set REA_IDA_MCP_CONFIG to your upstream IDA MCP registration JSON; see docs/ida-provider.md."},{"name":"skill:identity","ok":false,"classification":"config_drift","detail":"Installed REA skill identity is missing.","remediation":"Run rea setup to update the installed REA skill."}]}
```

Los dos hashes coinciden con la lectura previa a las corridas. No se deriva integridad de toda la instalacion de esos dos archivos.

### H. Captura historica de la instalacion y archivos de medicion

Lectura real de `/workspace/rea/engines/install.log` (51 bytes, sha256 `79b483092afa38ecf683984730bb06b1b90c88e778666ee0c37b73d79b5f7fae`):

```text
== inicio 2026-10-14T01:39:48Z
== JDK 21: descarga
```

El archivo leido a continuacion fue `install2.log`, 13.620 bytes, sha256 `dcd6278dfb3e58a43803e312bfd42bff2b4a2229d94d95f4094ae7fdb470b0d8`. Su cierre historico, citado como extracto y no como nueva medicion:

```text
== fin 2026-10-14T02:11:59Z
```

El script de ese instalador `install2.sh` mide 3.520 bytes y tiene sha256 `518c4b14162ba4c1c5e828075d1f286ed645b3cb1405dfe4b9c15a5b5a0f0d41`. No se ejecuto de nuevo. La captura completa local de esa lectura esta en `stage2.json`; no sustituye el veredicto basado en las corridas nuevas C y D.

Los procesos largos se ejecutaron una sola vez, con un limite de 180 s y un proceso de supervision que guardo stdout/stderr y timestamps. Scripts ejecutados: `run-inspect.py`, sha256 `9c8b3a5b6f002e70b051a4b2ec528b0aac6003263c7530f4ebf98c5af5bf7fb9`; `run-decompile.py`, sha256 `9699145eaa4db9bb3cd73f5c4724df2c7caa48d3f6118348b610d710ad1beda2`. Ambos finalizaron antes del limite; no hubo cancelacion. A 2026-10-14T19:52:02.053530+00:00 la salida de descompilacion ya existia y el proceso supervisor 2413 no seguia vivo.

## 5. Archivos generados y destino

En este mismo commit se agregan:

- `docs/auditorias/2026-10-14-01-rea-ghidra-operativos-por-cli.md`: veredicto separado.
- Este archivo: `docs/agents/respuestas/2026-10-14-016-rea-ghidra-instalados-y-probados.md`.

[Doc de ClickUp](https://app.clickup.com/90171457413/docs/2kza6fw5-22377), ruta `Space > REA y Ghidra funcionan juntos por consola: la caja se descompila; el chequeo general sigue con avisos (14-oct, 016)`.

No se commitean binarios derivados, snapshots ni instalaciones. Las fuentes de la caja ya estaban registradas en la respuesta 022 del 13-oct.

## 6. NO MEDIDO

GUI; registro en un cliente/agente; otros binarios y arquitecturas; CVE actuales; firma GPG; seguridad frente a credenciales del mismo usuario; integridad completa de los directorios instalados contra los archivos originales. Tampoco es una prueba ciega: el recibo anterior contenia la fuente de la caja y se leyo antes de este diagnostico.

## Antes de firmar

- «REA y JDK arrancan»: ejecutables exactos, exit 0. Podian fallar: PASS.
- «Ghidra importa este ELF»: proveedor real, operacion binary_overview, exit 0 y sujeto con hash exacto. Podia fallar: PASS.
- «Ghidra descompila esta funcion»: proveedor real, procedure_pseudo_code en 0x101070, exit 0. Podia fallar: PASS.
- «La regla es coherente con la caja»: salida del descompilador y tres ejecuciones del mismo binario. Podian contradecirse: PASS en los tres casos.
- «El doctor general esta verde»: instrumento exacto devuelve false, exit 1. REFUTADO.
- «Integracion con agentes lista» o «seguridad integral verificada»: no hubo instrumento para eso. NO MEDIDO.

```text
--- METODO TITAN ---
Accion delicada: NO. Revision de instalacion, pruebas sobre caja propia y documentacion nueva.
Modo aplicado: TITAN FULL, auditoria acotada.
Rubrica: 37/40 -> 92,5/100 para el informe; desglose en la auditoria.
N/A declarados: 60 puntos, por tipo de entrega; no es codigo nuevo ni auditoria integral de seguridad.
Review externo: no solicitado; sin PR ni codigo de producto nuevo.
Instrumento: REA 6.4.0 + Ghidra 12.1.4, subprocess.returncode, sha256sum; evidencia cruda A-G.
Maquina: brain-env, Debian 13 x86-64, uid 1000, 2 CPU.
Artefactos: esta respuesta + docs/auditorias/2026-10-14-01-rea-ghidra-operativos-por-cli.md + https://app.clickup.com/90171457413/docs/2kza6fw5-22377
```
