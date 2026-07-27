# Política funcional de cambios y devoluciones

## Objetivo

La política de cambios y devoluciones define cómo debe operar el sistema cuando un cliente desea devolver o cambiar un producto comprado.

Estas reglas permiten mantener trazabilidad de las operaciones, actualizar correctamente el stock y evitar inconsistencias en las ventas.

## Diferencia entre cambio y devolución

### Devolución

Una devolución ocurre cuando el cliente retorna un producto comprado y solicita anular total o parcialmente la operación.

La devolución puede generar:

- reintegro de dinero;
- nota de crédito;
- devolución parcial;
- ingreso del producto al stock, si corresponde.

### Cambio

Un cambio ocurre cuando el cliente devuelve un producto y recibe otro producto a cambio.

El cambio puede ser:

- por talle;
- por color;
- por modelo;
- por falla;
- por error de despacho.

Ejemplo:

El cliente compró una remera talle M y solicita cambiarla por talle L.

## Condiciones para aceptar una devolución

Una devolución puede aceptarse si cumple las siguientes condiciones:

1. La venta existe en el sistema.
2. La venta está en estado entregada o despachada.
3. El producto devuelto pertenece a la venta original.
4. La devolución se solicita dentro del plazo permitido.
5. El producto está en condiciones válidas según la política comercial.
6. El producto no fue marcado como no retornable.

## Plazo de devolución

El plazo estándar para solicitar una devolución es de 30 días desde la fecha de entrega.

Si la venta fue entregada hace más de 30 días, el sistema debe advertir que la devolución se encuentra fuera de plazo.

Ejemplo de respuesta:

"La venta fue entregada hace más de 30 días. Según la política funcional, la devolución no puede aprobarse automáticamente y requiere revisión manual."

## Estados de una devolución

### Solicitada

La devolución queda solicitada cuando el usuario registra la intención del cliente de devolver un producto.

En este estado todavía no se modifica el stock.

### En revisión

La devolución queda en revisión cuando se debe validar el estado del producto, la fecha de compra o las condiciones comerciales.

### Aprobada

La devolución queda aprobada cuando cumple las condiciones definidas por la política.

Al aprobar una devolución, el sistema debe definir si corresponde reintegro, nota de crédito o cambio.

### Rechazada

La devolución queda rechazada cuando no cumple las condiciones necesarias.

Motivos posibles:

- venta inexistente;
- producto no pertenece a la venta;
- plazo vencido;
- producto usado o dañado;
- producto no retornable.

### Finalizada

La devolución queda finalizada cuando ya se completaron las acciones correspondientes:

- actualización de stock, si corresponde;
- reintegro o nota de crédito;
- registro administrativo final.

## Impacto de una devolución en el stock

Una devolución no debe aumentar stock automáticamente en todos los casos.

El stock solo debe aumentar si el producto vuelve en condiciones aptas para la venta.

Ejemplo:

Si el cliente devuelve una campera sin uso y en buen estado, puede volver al stock disponible.

Si el cliente devuelve una zapatilla usada o dañada, no debe volver al stock disponible.

## Devolución parcial

Una devolución parcial ocurre cuando el cliente devuelve solo algunos productos de la venta original.

Ejemplo:

Venta original:

- 1 campera deportiva;
- 2 remeras dry-fit;
- 1 calza training.

El cliente devuelve solo 1 remera dry-fit.

En ese caso, la devolución afecta únicamente ese ítem de venta.

## Cambio por talle

El cambio por talle requiere dos movimientos:

1. Ingreso del producto devuelto, si está apto para la venta.
2. Egreso del nuevo producto entregado al cliente.

Ejemplo:

El cliente devuelve una remera talle M y recibe una remera talle L.

El sistema debe:

- validar que la remera talle M pertenece a la venta original;
- validar estado del producto devuelto;
- consultar stock disponible de remera talle L;
- registrar el cambio;
- actualizar stock según corresponda.

## Cambio por producto diferente

Si el cliente cambia un producto por otro de distinto precio, el sistema debe calcular la diferencia.

Ejemplo:

El cliente cambia una remera de $18.000 por una campera de $55.000.

Diferencia a pagar:

$55.000 - $18.000 = $37.000

Si el nuevo producto es más barato, puede generarse saldo a favor o nota de crédito.

## Devolución con reintegro

Una devolución puede generar reintegro de dinero si la política comercial lo permite.

El sistema debe registrar:

- venta original;
- producto devuelto;
- monto a reintegrar;
- medio de reintegro;
- fecha;
- usuario responsable.

## Devolución con nota de crédito

Una nota de crédito puede usarse cuando no se devuelve dinero directamente, sino que se genera saldo a favor del cliente.

La nota de crédito debe quedar asociada al cliente y a la venta original.

## Casos que requieren revisión manual

Los siguientes casos requieren revisión manual:

- devolución fuera de plazo;
- producto dañado;
- producto sin etiqueta;
- producto usado;
- venta con pago parcial;
- venta con promociones especiales;
- producto no retornable;
- compra no encontrada;
- diferencia entre producto físico y producto registrado.

## Flujo normal de devolución

1. El usuario solicita registrar una devolución.
2. El sistema busca la venta original.
3. El sistema valida que el producto pertenezca a la venta.
4. El sistema revisa la fecha de entrega.
5. El sistema consulta la política de devolución.
6. El usuario indica el estado físico del producto.
7. El sistema determina si puede aprobarse o requiere revisión.
8. Si se aprueba, se define reintegro, nota de crédito o cambio.
9. El sistema actualiza stock si corresponde.
10. La devolución queda finalizada.

## Ejemplo de solicitud

Usuario:

"Necesito devolver una remera de la venta 238."

Respuesta esperada del asistente:

"Voy a validar la venta 238, verificar si la remera pertenece a esa operación y revisar si la venta se encuentra dentro del plazo de devolución. Si el producto está en condiciones aptas, la devolución podrá aprobarse y el stock podrá actualizarse."

## Reglas importantes

1. No se puede devolver un producto que no pertenece a la venta original.
2. No se debe actualizar stock hasta aprobar la devolución.
3. El stock solo aumenta si el producto está apto para la venta.
4. Las devoluciones fuera de plazo requieren revisión manual.
5. Los cambios por talle deben validar stock del nuevo talle.
6. Los cambios por producto diferente deben calcular diferencia de precio.
7. Toda devolución debe quedar asociada a una venta original.
8. No se recomienda eliminar ventas para representar devoluciones.

## Ejemplos de preguntas que puede responder el asistente

- ¿Cómo registro una devolución?
- ¿Cuál es el plazo para devolver un producto?
- ¿Qué pasa con el stock cuando hay una devolución?
- ¿Puedo cambiar un producto por otro más caro?
- ¿Qué diferencia hay entre cambio y devolución?
- ¿Cuándo una devolución requiere revisión manual?
- ¿Puedo devolver solo un producto de una venta?
