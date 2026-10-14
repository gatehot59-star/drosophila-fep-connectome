# Qué construir primero: cobros para pymes, no otra billetera

Fecha de consulta: 2026-10-14. Autor de la síntesis: BRAIN.

[Doc de ClickUp: Qué construir primero: cobros para pymes, no otra billetera](https://app.clickup.com/90171457413/docs/2kza6fw5-22577).
Ruta del Doc: [Space](https://app.clickup.com/90171457413/v/o/s/90176846840) > Qué construir primero: cobros para pymes, no otra billetera.

## Veredicto

Sí se puede diseñar un producto original que combine funciones de belo, Wise, Bridge y Revolut. No se obtienen sus servidores, bancos, liquidez, contratos, permisos ni aprobación comercial descompilando una app. Para la prioridad de llegar antes a clientes pagos, recomiendo otra entrada: seguimiento de facturas y conciliación para un rubro de pymes, inspirado en Chaser, sin custodiar ni mover dinero.

La plataforma regional de pagos queda como segunda etapa condicionada a demanda y socios autorizados. La visión puede ser integral; el primer producto debe resolver una sola pérdida concreta. Esto es una recomendación para validar, no una oportunidad comercial demostrada ni una implementación.

Pregunta respondida: ¿hibridar los cuatro proveedores en un sistema de transacciones sudamericano o adaptar una aplicación probada con menos dependencias? Alcance: Argentina, Bolivia, Brasil, Chile, Paraguay, Uruguay y Perú. No se abrió ninguna cuenta, contactó a proveedores, envió mensajes comerciales ni ejecutó transacciones.

## 1. Qué significa combinar las fintechs

Una experiencia propia podría reunir cotización transparente, estados, cuentas por moneda y conectores. Implementación original, marca propia e integraciones autorizadas: no copiar código, activos ni identidad ajenos.

La [comparación previa](2026-10-14-comparativa-belo-wise-bridge-revolut.md) y su [Doc](https://app.clickup.com/90171457413/docs/2kza6fw5-22517) siguen siendo la base. Entre los cuatro, belo presenta la mayor cobertura publicada de cripto a moneda local; Wise no es una infraestructura genérica para compraventa de cripto; Bridge publica BRL/Pix entre las siete monedas analizadas; Revolut tiene alta local confirmada en Brasil. Cobertura del servicio de consumo no prueba disponibilidad contractual para nuestra aplicación.

[Bridge](https://apidocs.bridge.xyz/platform/customers/customers/endorsements) exige KYC, aceptación de términos y aprobaciones por vía de pago. La habilitación USD no es la habilitación Pix. No se verificó un contrato comercial, white-label ni acceso productivo para nosotros.

Si se eligiera pagos, el piloto sería un caso de uso y un corredor con socio aprobado, con conciliación, prevención de operaciones duplicadas y tratamiento de fallos. No siete países a la vez. La viabilidad legal y comercial permanece NO MEDIDA; no custodiar fondos no concede por sí solo una exención regulatoria.

## 2. Alternativas contrastadas y criterio de elección

Criterio: minimizar dependencias externas para resolver un problema por el que alguien pague. No se asignan fechas ficticias de lanzamiento ni una puntuación numérica disfrazada de medición.

| Camino | Evidencia del modelo | Dependencia inicial | Decisión |
|---|---|---|---|
| Plataforma regional de pagos | Comparación previa de belo, Wise, Bridge y Revolut | Proveedores, contratos, cumplimiento, costos y liquidación | No elegirla para un lanzamiento rápido |
| Facturas y conciliación, tipo Chaser | Planes y casos de clientes publicados | Puede empezar con archivos autorizados y revisión humana | Primera hipótesis a validar |
| Gestión de servicios, tipo Jobber | El proveedor anuncia más de 100.000 clientes y más de 400.000 profesionales usuarios | Agenda, presupuestos, órdenes de trabajo, equipo y adopción operativa | Segunda opción, no el primer alcance |

[Chaser](https://www.chaserhq.com/chaser-pricing) anuncia Compact desde USD 259 por mes y publica [casos de clientes](https://www.chaserhq.com/case-studies). Eso acredita una oferta comercial, no el precio aceptable para nuestro nicho. [Jobber](https://www.getjobber.com/about/media/) publica su escala y funciones. Los números son afirmaciones comerciales de los proveedores, no auditorías nuestras.

## 3. El problema existe, pero no es un mercado vacío

[Coface, encuesta 2025](https://www.coface.com.br/noticias-economia-e-insights/pesquisa-de-pagamentos-e-inadimplencias-na-america-latina-2025-prazos-de-pagamento-mais-longos-e-aumento-nos-atrasos): 77% de las empresas encuestadas experimentó pagos atrasados. La muestra incluye Argentina, Brasil, Chile, Colombia, Ecuador y Perú. No se extrapola a Bolivia, Paraguay, Uruguay ni a un rubro específico. Tampoco se confunde dolor con demanda de una app nueva.

[Moonflow](https://www.moonflow.ai/casos-de-exito) y [Duemint](https://www.duemint.com/recursos/casos-de-exito) ya ofrecen cobranzas y conciliación. [Colppy](https://colppy.com/gestion-clientes-proveedores) publica recordatorios, conciliación, bancos y funciones multimoneda en Argentina. [Auvo](https://www.auvo.com/es-ar/field-service) ya ofrece gestión de técnicos y órdenes de trabajo para la región.

Traducir una app extranjera no es una ventaja demostrada. La hipótesis es una implementación asistida, de alcance reducido, que no reemplace al contador ni al sistema contable. Si el producto que el cliente ya paga resuelve el problema, configurar lo existente podría ser una mejor venta de servicio que desarrollar otro software.

El producto aborda conciliación, trabajo manual y visibilidad; un recordatorio no crea liquidez ni cura la insolvencia del deudor.

## 4. Primera oferta propuesta

Cliente propuesto: pequeñas empresas argentinas de mantenimiento o servicios B2B que cobran por transferencia y cruzan facturas con movimientos a mano. La elección inicial de Argentina es foco para reducir dispersión, no evidencia de mayor mercado ni de acceso comercial ya disponible.

Promesa: saber qué pago corresponde a qué factura y qué sigue pendiente, sin cambiar de banco ni de contador. Modelo propuesto: configuración más suscripción, no custodia, cambio de moneda ni porcentaje por recuperar deuda.

Alcance del piloto:

- Importar facturas existentes y movimientos CSV/Excel exportados por el cliente. Sin claves bancarias ni emisión fiscal propia.
- Sugerir coincidencias por referencia, importe, moneda, fecha e identificador disponible. Tratar pagos parciales, retenciones, duplicados y diferencias como excepciones visibles.
- Confirmación humana cuando la evidencia no alcanza. Una captura no acredita un pago; reimportar un archivo no debe duplicarlo.
- Separar saldos por moneda y conservar la procedencia de cada dato. Registrar monedas no equivale a convertirlas.
- Preparar seguimiento de facturas propias por email bajo revisión del cliente. Detener ante pago, disputa o solicitud de no contacto. No campañas masivas ni cobro judicial.
- Exportar estado de cuenta trazable y definir accesos, permisos, retención y borrado de datos.

Quedan fuera billetera, cripto, préstamos, compra de deudas, transferencias automáticas y emisión fiscal en siete países. Menos superficie no significa ausencia de obligaciones de privacidad, seguridad o reglas locales.

### WhatsApp no puede ser la dependencia central

La [política oficial](https://business.whatsapp.com/policy) exige consentimiento y contempla plantillas aprobadas, y restringe expresamente debt collection. No se concluye que todo aviso de factura esté prohibido; se concluye que no se puede prometer una plataforma de cobranza por WhatsApp sin validar el caso exacto.

Por eso el alcance propuesto no depende de WhatsApp. Email y revisión humana tampoco eliminan las obligaciones aplicables. No se enviaron mensajes ni se pidió acceso a ninguna cuenta.

## 5. Prueba de negocio propuesta, no ejecutada

1. Conversar con diez empresas de un mismo rubro usando ejemplos autorizados o anonimizados. Verificar su sistema actual, el hueco concreto y el tiempo que pierden.
2. Conseguir tres pilotos pagos antes de ampliar desarrollo. No hay precio validado todavía.
3. Medir tiempo administrativo antes y durante el piloto con tareas equivalentes. Umbral propuesto: reducir al menos a la mitad el tiempo de conciliación en dos de tres pilotos sin marcar como pagado nada sin respaldo.
4. Revisar uso y renovación tras un ciclo mensual. La compra inicial y una demo no prueban retención.
5. Frenar o cambiar la oferta si diez conversaciones no dan pilotos pagos, si el sistema actual basta o si las integraciones particulares cuestan más que lo que ingresa. Un resultado negativo chico descarta esa oferta o segmento, no todo Sudamérica.

Los tamaños y umbrales son decisiones de diseño para limitar gasto, no estimaciones estadísticas de mercado. Adquisición, soporte, margen y costos unitarios no se midieron. No se remitió esta prueba como orden a otro ejecutor.

## 6. Camino a la visión regional

Orden recomendado por dependencia: resolver registros y pendientes; automatizar formatos que se repitan; evaluar pagos integrados sólo si hay necesidad pagada, contratos y revisión de obligaciones. No hace falta REA para esta primera apuesta.

Argentina, Bolivia, Brasil, Chile, Paraguay, Uruguay y Perú son el horizonte, no siete lanzamientos simultáneos. Idioma, formatos bancarios, datos, impuestos y reglas no se unifican por compartir código. Brasil requiere portugués; cada expansión tiene su propia validación.

## 7. Estado de evidencia y límites

VERIFICADO DOCUMENTALMENTE: modelos comerciales extranjeros, competencia regional, dato de pagos tardíos de Coface y restricciones publicadas de Bridge y WhatsApp.

RECOMENDACIÓN: priorizar facturas y conciliación sin mover fondos por su menor dependencia inicial.

NO MEDIDO: demanda del nicho, entrevistas, disposición a pagar, precio, retención, costos, margen, plazo real de desarrollo, contratos o autorización por país. No hay implementación, benchmark, prueba financiera ni dictamen legal.

Una recomendación no se etiqueta PASS de producto. Las fuentes permiten elegir una prueba, no prometer ingresos ni declarar un nicho vacío.

## 8. Método y preservación

Base documental antes de esta escritura: d9cd4959452cfa92b3ee47b19d7c86d4b5dd6963 en titan/comparativa-pagos-latam-2026-10-14. Las consultas de historial para estas dos rutas nuevas no devolvieron commits; no había PR abierto con esa rama como origen. No se modifica la comparación anterior ni código del repositorio. Este repositorio se usa sólo como archivo de conversación en la rama de investigación.

--- METODO TITAN ---
Accion delicada: NO.
Modo aplicado: TITAN LIGERO, investigacion documental acotada.
Rubrica: N/A (modo ligero; no es implementacion).
N/A declarados: no hay medicion de producto, seguridad implementada, mercado ni pagos.
Review externo: no solicitado; sin PR ni merge, sin validacion independiente de mercado.
Instrumento: ninguno de ejecucion. Lectura de fuentes oficiales; citas breves y limites en evidencia separada.
Maquina: no aplica; no se ejecuto codigo ni runtime.
Artefactos: este archivo, ../evidencia/2026-10-14-estrategia-producto-latam-fuentes.md y https://app.clickup.com/90171457413/docs/2kza6fw5-22577.

## Fuentes

Catálogo, citas breves y límites: [evidencia documental](../evidencia/2026-10-14-estrategia-producto-latam-fuentes.md). Base anterior: [comparación en ClickUp](https://app.clickup.com/90171457413/docs/2kza6fw5-22517).
