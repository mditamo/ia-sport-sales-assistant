# Manual funcional del módulo de ventas

## Objetivo del módulo

El módulo de ventas permite registrar operaciones comerciales realizadas a clientes dentro del sistema de ventas de indumentaria deportiva.

Una venta representa una operación en la que un cliente compra uno o más productos, como remeras, calzas, camperas, zapatillas, shorts, buzos u otros artículos deportivos.

El módulo permite:

- crear ventas;
- asociar una venta a un cliente;
- agregar productos a la venta;
- validar disponibilidad de stock;
- calcular el total de la venta;
- registrar el estado de la operación;
- registrar pagos;
- cancelar ventas;
- consultar ventas históricas.

## Entidades principales

### Venta

Una venta es el registro principal de la operación comercial.

Una venta contiene:

- cliente asociado;
- fecha de creación;
- productos incluidos;
- cantidades;
- precios unitarios;
- descuentos aplicados;
- total de la venta;
- estado de la venta;
- estado de pago;
- observaciones.

### Ítem de venta

Un ítem de venta representa un producto incluido dentro de una venta.

Cada ítem contiene:

- producto;
- talle;
- color;
- cantidad;
- precio unitario;
- subtotal.

Ejemplo:

Una venta puede incluir:

- 1 campera running talle M color negro;
- 2 remeras dry-fit talle L color azul;
- 1 calza deportiva talle S color gris.

## Estados de una venta

### Pendiente

Una venta queda en estado pendiente cuando fue creada pero todavía no fue confirmada.

En este estado, la venta puede modificarse. Se pueden agregar o quitar productos, cambiar cantidades o cancelar la operación.

Una venta pendiente no descuenta stock de forma definitiva.

### Confirmada

Una venta queda confirmada cuando el usuario valida que los datos son correctos y desea avanzar con la operación.

Al confirmar una venta, el sistema debe validar que exista stock suficiente para todos los productos incluidos.

Si no hay stock suficiente, la venta no puede confirmarse hasta corregir los productos o cantidades.

Según la configuración del sistema, una venta confirmada puede reservar stock.

### Pagada

Una venta queda pagada cuando se registra el pago total de la operación.

El pago puede realizarse por diferentes medios, como efectivo, transferencia, tarjeta de crédito, tarjeta de débito o billetera virtual.

Una venta puede estar confirmada pero no pagada.

### Despachada

Una venta queda despachada cuando los productos fueron preparados y enviados o entregados al cliente.

En este estado, el sistema descuenta definitivamente el stock de los productos vendidos si no fue descontado antes.

### Entregada

Una venta queda entregada cuando el cliente recibió los productos.

Este estado indica que la operación comercial fue completada desde el punto de vista logístico.

### Cancelada

Una venta queda cancelada cuando la operación no se concreta.

Una venta cancelada no debe descontar stock.

Si la venta había reservado stock, el sistema debe liberar las unidades reservadas.

Si la venta tenía pagos registrados, se debe revisar manualmente si corresponde devolución de dinero.

## Flujo normal de una venta

El flujo habitual de una venta es:

1. Crear una venta.
2. Seleccionar o crear el cliente.
3. Agregar productos.
4. Validar stock.
5. Calcular total.
6. Confirmar venta.
7. Registrar pago.
8. Despachar productos.
9. Marcar venta como entregada.

## Creación de una venta

Para crear una venta, el usuario debe indicar al menos:

- cliente;
- uno o más productos;
- cantidad de cada producto.

El sistema debe validar que los productos existan y que las cantidades sean mayores a cero.

Ejemplo de solicitud:

"Crear una venta para Sofía Ramírez con 1 campera deportiva talle S y 2 remeras dry-fit talle M."

El sistema debe buscar el cliente, buscar los productos, validar stock y calcular el total antes de confirmar la operación.

## Validación de stock en ventas

Antes de confirmar una venta, el sistema debe verificar que exista stock suficiente para cada producto solicitado.

Ejemplo:

Si el usuario quiere vender 3 remeras talle M y el stock disponible es 2, el sistema debe informar que no hay stock suficiente.

Respuesta esperada:

"No se puede confirmar la venta porque el producto Remera Dry-Fit talle M tiene stock disponible de 2 unidades y se solicitaron 3 unidades."

## Cálculo del total de venta

El total de la venta se calcula sumando los subtotales de cada ítem.

El subtotal de cada ítem se calcula así:

cantidad × precio unitario

Ejemplo:

- 2 remeras a $18.000 cada una = $36.000
- 1 campera a $55.000 = $55.000

Total de la venta: $91.000

Si existen descuentos, deben aplicarse antes de mostrar el total final.

## Registro de pago

El pago puede registrarse luego de confirmar la venta.

Datos mínimos del pago:

- venta asociada;
- medio de pago;
- monto;
- fecha de pago.

Si el monto pagado cubre el total de la venta, el estado de pago pasa a pagada.

Si el monto pagado es menor al total, la venta queda con pago parcial.

## Cancelación de una venta

Una venta puede cancelarse si todavía no fue entregada.

Al cancelar una venta:

- la venta pasa a estado cancelada;
- no se debe descontar stock;
- si había stock reservado, debe liberarse;
- si había pago registrado, debe quedar asentado para revisión.

No se recomienda eliminar ventas, porque se pierde trazabilidad.

## Consultas frecuentes sobre ventas

### ¿Una venta pendiente descuenta stock?

No. Una venta pendiente no descuenta stock definitivo. Solo representa una operación iniciada.

### ¿Cuándo se valida el stock?

El stock se valida antes de confirmar la venta.

### ¿Se puede modificar una venta confirmada?

Una venta confirmada debería modificarse con restricciones. Si los cambios afectan productos o cantidades, el sistema debe volver a validar stock.

### ¿Qué pasa si cancelo una venta confirmada?

La venta pasa a estado cancelada. Si había stock reservado, debe liberarse.

### ¿Qué pasa si la venta ya fue entregada?

Si la venta ya fue entregada, no debería cancelarse directamente. En ese caso corresponde iniciar una devolución.

## Ejemplos de preguntas que puede responder el asistente

- ¿Cómo creo una venta?
- ¿Qué estados tiene una venta?
- ¿Cuándo se descuenta el stock?
- ¿Puedo cancelar una venta pagada?
- ¿Qué pasa si no hay stock suficiente?
- ¿Cómo registro el pago de una venta?
- ¿Qué diferencia hay entre venta confirmada y venta entregada?
