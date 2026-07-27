# Preguntas frecuentes del sistema de ventas

## Objetivo del documento

Este documento reúne preguntas frecuentes sobre el uso general del sistema de ventas de indumentaria deportiva.

Su objetivo es ayudar al asistente inteligente a responder dudas funcionales frecuentes de los usuarios.

## Preguntas generales

### ¿Para qué sirve el sistema?

El sistema sirve para gestionar ventas, clientes, productos, stock, pagos, cambios, devoluciones y reportes comerciales de una tienda de indumentaria deportiva.

Permite ordenar la operación diaria y mantener trazabilidad de las transacciones.

### ¿Qué módulos principales tiene el sistema?

El sistema cuenta con los siguientes módulos principales:

- clientes;
- productos;
- ventas;
- stock;
- pagos;
- cambios y devoluciones;
- reportes.

### ¿Qué puede hacer el asistente inteligente?

El asistente inteligente puede ayudar a:

- explicar cómo funciona el sistema;
- responder preguntas funcionales;
- buscar clientes;
- consultar productos;
- validar stock;
- iniciar ventas;
- explicar estados;
- guiar cambios y devoluciones;
- generar reportes simples;
- detectar inconsistencias.

## Preguntas sobre ventas

### ¿Cómo creo una venta?

Para crear una venta, se debe seleccionar un cliente, agregar productos, validar stock y confirmar la operación.

Flujo recomendado:

1. Buscar o crear cliente.
2. Agregar productos.
3. Indicar cantidades.
4. Validar stock.
5. Revisar total.
6. Confirmar venta.
7. Registrar pago, si corresponde.

### ¿Puedo crear una venta sin cliente?

Depende de la configuración del sistema.

Para mantener trazabilidad, se recomienda que toda venta esté asociada a un cliente.

### ¿Cuándo se confirma una venta?

Una venta se confirma cuando el usuario revisa los datos, valida productos y decide avanzar con la operación.

Antes de confirmar, el sistema debe validar stock suficiente.

### ¿Qué pasa si no hay stock suficiente?

Si no hay stock suficiente, la venta no debe confirmarse.

El sistema debe informar qué producto o variante no tiene disponibilidad suficiente.

Ejemplo:

"No se puede confirmar la venta porque Remera Dry-Fit talle M color negro tiene 1 unidad disponible y se solicitaron 3."

### ¿Puedo modificar una venta pendiente?

Sí. Una venta pendiente puede modificarse porque todavía no fue confirmada.

Se pueden cambiar productos, cantidades, cliente u observaciones.

### ¿Puedo modificar una venta confirmada?

Sí, pero con restricciones.

Si se modifican productos o cantidades, el sistema debe volver a validar stock.

### ¿Puedo cancelar una venta?

Sí, una venta puede cancelarse si todavía no fue entregada.

Si la venta tenía stock reservado, debe liberarse.

Si la venta tenía pagos registrados, debe quedar pendiente de revisión administrativa.

## Preguntas sobre pagos

### ¿Cuándo registro un pago?

El pago puede registrarse luego de crear o confirmar una venta, según la política del negocio.

Lo habitual es registrar el pago antes del despacho o entrega.

### ¿Qué medios de pago puede registrar el sistema?

El sistema puede registrar diferentes medios de pago:

- efectivo;
- transferencia;
- tarjeta de crédito;
- tarjeta de débito;
- billetera virtual;
- otro medio definido por el negocio.

### ¿Qué pasa si el cliente paga solo una parte?

La venta queda con pago parcial.

El sistema debe registrar el monto abonado y dejar pendiente el saldo restante.

### ¿Una venta pagada se entrega automáticamente?

No necesariamente.

El pago y la entrega son estados distintos. Una venta puede estar pagada pero todavía no despachada o entregada.

## Preguntas sobre productos

### ¿Cómo creo un producto?

Para crear un producto, se debe indicar nombre, categoría, precio de venta y variantes si corresponde.

Ejemplo:

Producto: Remera Dry-Fit  
Categoría: remeras  
Precio: $18.000  
Variantes: talle S, M y L en color negro.

### ¿Qué es una variante de producto?

Una variante es una combinación específica de atributos de un producto.

Ejemplo:

Producto: Calza Training  
Variante: talle M color negro.

El stock debería controlarse por variante.

### ¿Puedo cambiar el precio de un producto?

Sí. El cambio de precio afecta ventas futuras.

Las ventas históricas no deberían modificarse automáticamente por cambios posteriores de precio.

### ¿Puedo eliminar un producto?

No se recomienda eliminar productos que tienen ventas asociadas.

En esos casos, conviene marcarlos como inactivos o discontinuados.

### ¿Qué significa producto discontinuado?

Un producto discontinuado es un producto que ya no se comercializa, pero se mantiene en el sistema para conservar historial.

## Preguntas sobre stock

### ¿Qué significa stock disponible?

El stock disponible representa la cantidad de unidades que pueden venderse.

Conceptualmente:

stock disponible = stock físico - stock reservado

### ¿Qué significa stock reservado?

El stock reservado representa unidades comprometidas en ventas confirmadas pero todavía no despachadas.

### ¿Cuándo se descuenta el stock?

El stock puede descontarse definitivamente cuando la venta se despacha o se entrega, según la configuración del sistema.

### ¿Qué pasa con el stock si cancelo una venta?

Si la venta tenía stock reservado, el sistema debe liberar esa reserva.

Si la venta no había reservado stock, no hay impacto sobre stock.

### ¿Qué significa bajo stock?

Un producto tiene bajo stock cuando su stock disponible es menor o igual al stock mínimo definido.

El bajo stock genera una advertencia, pero no necesariamente bloquea la venta.

### ¿Puedo vender un producto con bajo stock?

Sí, si todavía tiene stock disponible.

No se debería confirmar una venta si el stock disponible es cero o insuficiente para la cantidad solicitada.

## Preguntas sobre clientes

### ¿Cómo creo un cliente?

Para crear un cliente, se deben registrar al menos nombre, apellido y un dato de contacto como teléfono o email.

### ¿Cómo busco un cliente?

Se puede buscar por nombre, apellido, teléfono, email o documento.

Ejemplo:

"Buscar cliente Laura Gómez."

### ¿Qué pasa si el cliente ya existe?

El sistema debería advertir posibles duplicados.

Antes de crear un cliente nuevo, se recomienda buscar coincidencias por teléfono, email o documento.

### ¿Puedo eliminar un cliente?

No se recomienda eliminar clientes con ventas asociadas.

En ese caso, conviene marcar el cliente como inactivo.

### ¿Qué es un cliente frecuente?

Un cliente frecuente es aquel que realiza compras de manera repetida.

Puede identificarse por cantidad de compras, monto total comprado o frecuencia de compra.

## Preguntas sobre cambios y devoluciones

### ¿Cuál es la diferencia entre cambio y devolución?

Una devolución ocurre cuando el cliente retorna un producto y solicita reintegro, nota de crédito o anulación parcial.

Un cambio ocurre cuando el cliente devuelve un producto y recibe otro a cambio.

### ¿Cuál es el plazo para una devolución?

El plazo estándar es de 30 días desde la fecha de entrega.

Las devoluciones fuera de plazo requieren revisión manual.

### ¿Puedo devolver solo un producto de una venta?

Sí. Eso se llama devolución parcial.

La devolución afecta solo el producto devuelto, no necesariamente toda la venta.

### ¿Una devolución aumenta el stock automáticamente?

No siempre.

El stock solo debe aumentar si el producto devuelto vuelve en condiciones aptas para la venta.

### ¿Qué pasa si el cliente cambia por un producto más caro?

El sistema debe calcular la diferencia de precio.

Ejemplo:

Producto devuelto: $18.000  
Producto nuevo: $25.000  
Diferencia a pagar: $7.000

### ¿Qué pasa si el cliente cambia por un producto más barato?

El sistema puede generar saldo a favor, nota de crédito o reintegro parcial, según la política comercial.

## Preguntas sobre reportes

### ¿Qué reportes puede generar el sistema?

El sistema puede generar reportes como:

- ventas por período;
- productos más vendidos;
- clientes frecuentes;
- productos con bajo stock;
- ventas por medio de pago;
- devoluciones por período;
- ticket promedio.

### ¿Qué es el ticket promedio?

El ticket promedio es el monto promedio de las ventas en un período.

Fórmula conceptual:

ticket promedio = total vendido / cantidad de ventas

### ¿Cómo veo los productos más vendidos?

El sistema debe consultar las ventas del período y agrupar los productos por cantidad vendida o monto vendido.

### ¿Cómo identifico clientes frecuentes?

El sistema puede analizar cantidad de compras, frecuencia y monto total comprado por cada cliente.

## Preguntas sobre el asistente inteligente

### ¿El asistente puede consultar datos reales?

Sí, si está conectado a herramientas o servidores MCP que permitan consultar clientes, productos, stock y ventas.

### ¿El asistente puede modificar datos?

Sí, pero solo si tiene herramientas habilitadas para hacerlo y si el flujo solicita confirmación antes de ejecutar cambios importantes.

### ¿El asistente puede responder preguntas del manual?

Sí. Para eso utiliza RAG sobre la documentación funcional del sistema.

### ¿Qué diferencia hay entre consultar el RAG y usar MCP?

El RAG sirve para responder preguntas sobre cómo funciona el sistema.

MCP sirve para consultar o ejecutar acciones sobre datos reales del sistema.

Ejemplo de RAG:

"¿Cuándo se descuenta el stock?"

Ejemplo de MCP:

"Consultá el stock de Remera Dry-Fit talle M color negro."

### ¿Cuándo una consulta es mixta?

Una consulta es mixta cuando requiere explicación funcional y consulta o acción sobre datos reales.

Ejemplo:

"Necesito devolver una remera de la venta 238. ¿Se puede?"

El asistente debe consultar la política de devoluciones con RAG y también consultar la venta 238 mediante MCP.

## Ejemplos de preguntas completas para probar el RAG

- ¿Cómo creo una venta?
- ¿Qué estados tiene una venta?
- ¿Cuándo se descuenta el stock?
- ¿Qué diferencia hay entre stock físico y stock reservado?
- ¿Cómo registro una devolución?
- ¿Puedo cambiar un producto por otro más caro?
- ¿Qué datos necesito para crear un cliente?
- ¿Qué es una variante de producto?
- ¿Puedo eliminar un producto con ventas?
- ¿Qué significa cliente frecuente?
- ¿Qué pasa si una venta está pagada pero no entregada?
- ¿Qué hace el sistema si no hay stock suficiente?
- ¿Cuál es la diferencia entre RAG y MCP en este asistente?
