# Estado real y próximo corte

**Doc público asociado:** [Estado real al 3-oct: de investigación dispersa a producto temporal verificable](https://app.clickup.com/90171457413/docs/2kza6fw5-18917)

## 1. Pedido

Explicar por dónde vamos, qué se logró y qué sigue, sin mezclar evidencia medida con potencial.

## 2. Estado en una frase

Estamos pasando de un taller de investigación a un stack de producto: fuente temporal → SparseLTC → DBC3 → frontera Linux verificable. Todavía no es una lengua universal, una mosca digital completa ni un sistema edge validado en hardware.

## 3. Qué se logró

- FlyWire v783 medido: aproximadamente 138.639 neuronas, 15.091.983 aristas dirigidas agregadas y 54.492.922 contactos; loader con checksums, IDs, annotations y CSR.
- H4 corregida con 41 contratos. El resultado ROI-label dentro del animal es descriptivo; H4 fuerte sigue `NO MEDIDA`.
- Anatomía R65D11 medida en confocal: Brain 40x `145.494×145.494×116.160 µm`; VNC 40x `320.087×320.087×116.490 µm`.
- `ROI_0` y `ROI_1` quedaron correctamente `UNMAPPED`; el stress regional pasó 10/10 y bloquea inferencias anatómicas falsas.
- SparseLTC real corre sobre CSR y estados temporales; el adaptador SparseLTC→DBC3 compila, pero el end-to-end biológico sigue pendiente.
- DBC3 tiene ventaja selectiva en memoria diferida y cambio de contexto, no superioridad universal. `dbc3-link` Linux tiene wire de 296 bytes, HMAC, digest, replay, MEMFD/POSIX_SHM y fallback; smoke 13/13.
- `ComplexVectorLTC` obtuvo `PASS_WITH_SCOPE` como productor de semántica de fase en una tarea controlada: 100% de accuracy en 16 muestras. No superó todavía a dos canales reales y no entra al producto.

## 4. Qué se midió y qué no

**Medido:** arquitectura, contratos, loader, nulls H4, geometría confocal, wire Linux y varias tareas DBC3. **NO MEDIDO:** mapping funcional ROI→root ID, null anatómico real, causalidad, SparseLTC→DBC3 con señal y pesos biológicos reales, hardware edge, energía, interoperabilidad A2A/MCP externa y superioridad de la célula compleja.

## 5. Próximo orden

1. Cerrar el benchmark global DBC3-live con recibo cuantitativo.
2. Cargar pesos reales y ejecutar SparseLTC→DBC3 end-to-end con LIF, CTRNN, ESN/LSM y lineales.
3. Medir latencia, memoria, bytes y energía en Actions x64/arm64 y hardware real.
4. Probar receptores nuevos y heterogéneos bajo pérdida, delay, replay y deriva.
5. Reabrir mapping anatómico solo con raw 2P privado o provenance experimental explícita.

La decisión fuerte es no agregar otra variante de neurona ahora: la próxima evidencia que compra valor es utilidad reproducible, coste real y adopción.

## 6. Rama y artefactos

La actualización anatómica y este estado están en la rama `titan/paso-1-identidad-roi-2026-10-03`; todavía no se mergearon a `main`.

- `docs/agents/CONTEXTO-drosophila-fep.md`.
- `docs/agents/respuestas/2026-10-03-006-anatomia-confocal-medida.md`.
- `docs/agents/evidencia/2026-10-03-006-r65d11-confocal-anatomy-geometry.json`.
- Este archivo.
- [Doc público](https://app.clickup.com/90171457413/docs/2kza6fw5-18917).

--- METODO PROMETEO ---
Accion delicada: NO
Modo: diagnóstico de estado, sin merge ni release
Instrumentos: GitHub API, ClickUp Docs y evidencia versionada de brain-env/Actions/Kaggle
Maquina: brain-env + GitHub API + ClickUp
Artefactos: contexto + respuesta + evidencia + [Doc público](https://app.clickup.com/90171457413/docs/2kza6fw5-18917)
NO MEDIDO: hardware, causalidad, mapping funcional, backend DBC3 histórico completo y superioridad compleja