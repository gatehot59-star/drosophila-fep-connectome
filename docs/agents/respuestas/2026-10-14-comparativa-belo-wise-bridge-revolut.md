# belo, Wise, Bridge y Revolut: comparacion por pais para pagos y cripto

Fecha de consulta: 2026-10-14. Pedido: comparar los cuatro proveedores para Argentina, Bolivia, Brasil, Chile, Paraguay, Uruguay y Peru. Autor de la sintesis: ClickUp Brain. Alcance: documentacion publica, no transacciones.

## Conclusion

**Para cripto a moneda local, belo es el candidato mas completo de estos cuatro en los siete paises. Para construir una app, Bridge es infraestructura util, pero entre las siete monedas consultadas solo publica BRL/Pix. Wise compite en transferencias fiat, no como rampa cripto. Revolut tiene alta personal local confirmada en Brasil, mientras Argentina y Peru siguen con lista de espera.**

Mayor cobertura no significa menor precio. No se abrio ninguna cuenta, no se aprobo un KYC, no se pidio una cotizacion autenticada y no se movio dinero.

[Doc de ClickUp](https://app.clickup.com/90171457413/docs/2kza6fw5-22517). Ruta: Space > belo, Wise, Bridge y Revolut: comparacion por pais para pagos y cripto (14-oct-2026).

[Evidencia y fuentes](../evidencia/2026-10-14-pagos-latam-fuentes.md). La evidencia contiene extractos breves de fuentes oficiales y sus limites; esta respuesta contiene la interpretacion.

## Como leer la matriz

- Alta belo: documentos de identidad emitidos por el pais segun su matriz, sujeta a requisitos y aprobacion.
- Wise: elegibilidad publicada para mantener saldo segun residencia. No equivale a poder fondear en la moneda local.
- Salida local: dinero acreditado en un banco o billetera del pais. Recibir una remesa no exige que el destinatario tenga cuenta del proveedor.
- Bridge: admision de clientes a traves de una empresa integradora, no app de consumo ni aceptacion automatica.
- Revolut: alta para residentes, no posibilidad de usar una tarjeta extranjera como turista.
- Publicado no significa medido: todos los corredores requieren validar perfil, cuenta receptora y cotizacion antes de ejecutar.

## Comparacion por pais

| Pais | belo | Wise | Bridge | Revolut |
|---|---|---|---|---|
| Argentina, ARS | Alta publicada; conversion de saldo a ARS; salida a CBU/CVU/alias. Con documento argentino, recepcion de pesos. [B1,B2] | Residencia habilitada para saldo; salida ARS a bancos; no fondeo ARS externo, aunque admite conversion de otro saldo a ARS. [W1,W3] | Clientes admitidos; sin riel ARS publicado. [G1,G2] | Lista de espera local. [R2] |
| Bolivia, BOB | Alta publicada; salida BOB a bancos personales propios o de terceros. [B1,B3] | No figura para mantener saldo. Pagina comercial publica EE.UU. USD a BOB: validar cotizacion, no confundir con cuenta boliviana. [W1,W6] | Clientes admitidos con clasificacion interna High Risk y diligencia adicional; sin riel BOB publicado. [G1,G2] | No figura entre residencias admitidas. [R1] |
| Brasil, BRL | Alta publicada; salida BRL a bancos; deposito local marcado en matriz. Funciones Pix dependen del perfil. [B1,B4] | Saldo y transferencias BRL de entrada/salida; mantener BRL exige residencia brasilena. [W1,W2,W10] | BRL/Pix documentado; es la salida local clara entre los siete. [G1,G2] | Alta y Pix entrada/salida documentados; cripto interno, retiro cripto externo prohibido por sus terminos brasilenos. [R1,R4,R5] |
| Chile, CLP | Alta publicada; salida CLP a bancos personales y deposito local segun matriz. [B1,B5] | Saldo y salida CLP; guia especifica admite fondeo desde bancos chilenos con identificacion chilena valida. [W1,W4] | Clientes admitidos; sin riel CLP publicado. [G1,G2] | No figura entre residencias admitidas. [R1] |
| Paraguay, PYG | Alta publicada; SI hay salida PYG a bancos personales, aunque lo omite la lista general. Depositos locales personales no habilitados en matriz. [B1,B6] | No figura para mantener saldo. Pagina comercial publica EE.UU. USD a PYG: validar cotizacion y perfil remitente. [W1,W7] | Clientes admitidos; sin riel PYG publicado. [G1,G2] | No figura entre residencias admitidas. [R1] |
| Uruguay, UYU | Alta publicada; salida UYU a bancos personales; deposito local personal no habilitado en matriz. [B1,B7] | Residencia habilitada para saldo; salida UYU; no fondeo externo UYU, aunque admite conversion de otro saldo a UYU. [W1,W5] | Clientes admitidos; sin riel UYU publicado. [G1,G2] | No figura entre residencias admitidas. [R1] |
| Peru, PEN | Alta publicada; salida PEN o USD a bancos personales. Deposito local no habilitado en matriz personal, distinto de Business. [B1,B8,B10] | Residencia habilitada para saldo. Pagina EE.UU. a Peru anuncia PEN local; no extrapolar a todo origen ni a fondeo PEN. [W1,W8] | Clientes admitidos; sin riel PEN publicado. [G1,G2] | Lista de espera local. [R3] |

Las referencias B/W/G/R se resuelven en el archivo de evidencia, con URL y extracto.

## Diferencias que deciden el producto

### belo: mas cercano al caso cripto regional

La matriz personal habilita deposito/retiro de cripto y cambio de monedas en los siete paises. Sus guias locales documentan conversion automatica desde el saldo. La Mastercard figura habilitada solo en Argentina entre estos siete. Depositos personales en moneda local figuran en Argentina, Bolivia, Brasil y Chile, no en Paraguay, Uruguay ni Peru. Esa matriz esta fechada 4-may-2026; no se realizo un alta actual. [B1]

Las guias internacionales advierten que la transferencia no llega a nombre del usuario. Si el banco receptor exige mismo titular remitente, puede rechazarla. No se extrapola esa advertencia al flujo domestico argentino, que tiene reglas propias. [B2-B8]

### Wise: fiat, no infraestructura de nuestro exchange

La politica no admite utilizar la cuenta para comprar/vender cripto ni recibir ventas P2P; tampoco admite negocios de intercambio cripto en Wise Business. Existen excepciones acotadas, por ejemplo ciertos pagos profesionales, y la politica de tarjeta es distinta. Por tanto, no afirmar que todo pago relacionado con cripto esta prohibido ni que una excepcion permite operar nuestra rampa. [W9]

Argentina, Brasil, Chile, Peru y Uruguay aparecen para mantener saldo; Bolivia y Paraguay no. Esto no impide que un remitente elegible envie a un banco de esos destinos. La posibilidad de recibir USD por Swift es otra cosa, no retiro en BOB o PYG. [W1,W11]

### Bridge: backend util, no salida local universal

Documenta ACH/FedNow/wire en USD, SEPA en EUR, Faster Payments en GBP, SPEI en MXN, Pix en BRL y Bre-B/banco en COP. Entre las siete monedas solicitadas, solo aparece BRL. La lista de residencias admite clientes de los siete, con diligencia reforzada en Bolivia segun su clasificacion interna. La propia fuente distingue residencia de capacidad transaccional. No se verificaron acuerdos privados o rieles no publicados. [G1,G2]

Para una app propia en los otros seis paises hace falta otra salida local, o confirmacion contractual de una capacidad adicional. Tener un proveedor no elimina automaticamente obligaciones de nuestra empresa, licencias o identificacion.

### Revolut: Brasil real; no importar condiciones del Reino Unido

Brasil tiene alta y transferencias Pix documentadas. Puede comprar y vender cripto dentro de Revolut, pero sus terminos locales prohíben el retiro externo y las transferencias cripto fuera de la app. La recepcion on-chain desde billeteras externas para Brasil quedo NO VERIFICADA. No se uso la ayuda britanica como prueba de capacidades brasilenas. [R1,R4,R5,R6]

Argentina y Peru publican listas de espera; Bolivia, Chile, Paraguay y Uruguay no figuran en el listado de altas. Esto no es una afirmacion de que no se pueda enviarles una transferencia desde otro pais, ni de que una tarjeta ya emitida no funcione alli. [R1-R3]

## Discrepancias que se conservaron

1. **Paraguay en belo:** la pagina general de destinos no lo enumera; la guia especifica de 5-ago-2026 si explica PYG. Se prioriza la guia especifica para salida local, no para deposito. [B6,B9]
2. **Wise, listas vs guias:** la lista general de monedas omite rutas presentes en guias especificas (CLP/UYU) y paginas comerciales (BOB/PYG/PEN). Se mantienen las primeras como documentadas y las ultimas como publicadas pendientes de cotizacion con un perfil elegible. No se declaran inexistentes por ausencia del listado ni operativas desde cualquier origen por una landing. [W2,W4-W8]
3. **belo personal vs Business en Peru:** matriz personal sin deposito local; oferta Business anuncia cobros locales. No se mezclan productos. [B1,B10]
4. **Wise, precios de landing:** los bloques de precio y tablas por metodo no siempre coinciden en su afirmacion de menor costo. No se usaron esas cifras para declarar un ganador de precio. [W6-W8]

## Recomendacion para la idea del usuario

Si se trata de usar una solucion existente, evaluar primero belo para cripto a moneda local; comparar Wise para fiat internacional y Revolut para residentes brasilenos. Elegir despues por neto recibido, no por publicidad de cobertura.

Si se trata de construir, estudiar Wise y Revolut como experiencia de usuario, Bridge como infraestructura y belo como competidor/posible socio API. belo Business publica acceso API, pero no demuestra por si solo una oferta de marca blanca aprobada ni todas las rutas para nuestro modelo. [B10]

Para un primer piloto tecnico, priorizar un solo corredor con salida ARS o BRL, sujeto a aprobacion de socios, antes que siete lanzamientos simultaneos. El criterio es reducir integraciones; la demanda, rentabilidad y mejor pais comercial NO ESTAN MEDIDOS.

Descompilar una app no entrega su servidor, liquidez, contratos bancarios o autorizaciones. La investigacion propone experiencia y operacion propias mediante integraciones autorizadas, no copiar software propietario.

## Costos y siguiente comprobacion

No hay un ganador de precio medido. Para comparar correctamente hacen falta cotizaciones del mismo importe, momento, origen y destino; no mezclar transferencia bancaria USD con venta USDT.

| Proveedor | Costo que se debe medir |
|---|---|
| belo | Cripto debitada, moneda neta acreditada, conversion, comision y red. |
| Wise | Pais remitente, metodo de fondeo, par de monedas, monto y posibles intermediarios Swift. |
| Bridge | Tarifa comercial, identificacion, conversion, blockchain, socio local y operacion propia. |
| Revolut | Plan Brasil, conversion fiat, comision cripto y cargos o impuestos de la ruta. |

Antes de operar, verificar contrato e identidad del beneficiario, pares token/red autorizados, tratamiento de errores/devoluciones y obligaciones locales. No se recomienda transferir dinero basandose solo en esta matriz.

## NO MEDIDO

Altas reales, KYC aprobado, aceptacion de nuestra sociedad, precios autenticados o negociados, transferencias reales, tiempos de liquidacion, disponibilidad por banco/red, tratamiento fiscal y permisos de nuestra empresa. No es un dictamen legal ni una garantia transaccional.

## Entrega y metodo

La rama es documental y no modifica main, codigo, workflows ni experimentos. El repositorio aloja la bitacora del hilo; la comparacion no forma parte del producto del conectoma. No se continua aqui la prueba pendiente de REA sobre el ejecutable sin simbolos.

--- METODO TITAN ---
Accion delicada: NO. Investigacion publica y dos archivos nuevos en rama separada.
Modo aplicado: TITAN LIGERO.
Rubrica: N/A (modo ligero; sin implementacion).
Review externo: no solicitado; no PR ni merge.
Instrumento: lectura de documentacion oficial; evidencia citada por separado.
Artefactos: este informe + ../evidencia/2026-10-14-pagos-latam-fuentes.md + https://app.clickup.com/90171457413/docs/2kza6fw5-22517
