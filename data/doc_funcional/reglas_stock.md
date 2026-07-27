# Reglas funcionales de stock

## Objetivo del control de stock

El control de stock permite conocer la cantidad disponible de cada producto dentro del sistema de ventas de indumentaria deportiva.

El stock representa la cantidad de unidades disponibles para vender, reservar, despachar o reponer.

El sistema debe evitar que se confirmen ventas con productos sin disponibilidad suficiente.

## Productos con stock

Cada producto del sistema puede tener stock por combinación de atributos.

En indumentaria deportiva, el stock normalmente se controla por:

- producto;
- talle;
- color;
- variante;
- depósito o sucursal, si corresponde.

Ejemplo:

El producto "Remera Dry-Fit" puede tener stock separado para:

- talle S color negro;
- talle M color negro;
- talle L color negro;
- talle M color azul.

Cada combinación debe considerarse una variante diferente a efectos de stock.

## Stock disponible

El stock disponible representa las unidades que pueden venderse.

Fórmula conceptual:

stock disponible = stock físico - stock reservado

Ejemplo:

Si hay 10 remeras en stock físico y 3 están reservadas para ventas confirmadas, el stock disponible es 7.

## Stock físico

El stock físico representa las unidades reales existentes en depósito, local o sucursal.

El stock físico puede aumentar por compras, ingresos manuales o devoluciones aceptadas.

El stock físico puede disminuir por ventas despachadas, ajustes manuales o pérdidas.

## Stock reservado

El stock reservado representa unidades comprometidas para ventas confirmadas pero todavía no despachadas.

El objetivo del stock reservado es evitar sobrevender productos.

Ejemplo:

Si se confirma una venta de 2 camperas, esas unidades pueden quedar reservadas hasta que la venta sea despachada.

## Stock mínimo

El stock mínimo indica la cantidad mínima deseada para un producto o variante.

Cuando el stock disponible es igual o menor al stock mínimo, el sistema puede marcar el producto como bajo stock.

Ejemplo:

Producto: Calza Training talle M color negro  
Stock disponible: 2  
Stock mínimo: 3  

Resultado: producto con bajo stock.

## Producto sin stock

Un producto se considera sin stock cuando su stock disponible es igual a cero.

Si un producto no tiene stock disponible, el sistema no debe permitir confirmar nuevas ventas de ese producto.

## Bajo stock

Un producto se considera con bajo stock cuando su stock disponible es menor o igual al stock mínimo definido.

El bajo stock no impide necesariamente vender, pero debe generar una advertencia.

Ejemplo de advertencia:

"El producto Zapatilla Running talle 40 tiene bajo stock. Stock disponible: 1 unidad."

## Validación de stock antes de confirmar una venta

Antes de confirmar una venta, el sistema debe revisar el stock disponible de cada producto incluido.

La venta solo puede confirmarse si todos los productos tienen stock suficiente.

Ejemplo:

Venta solicitada:

- 2 remeras dry-fit talle M;
- 1 campera running talle L.

Stock disponible:

- remera dry-fit talle M: 5 unidades;
- campera running talle L: 0 unidades.

Resultado:

La venta no puede confirmarse porque no hay stock disponible de campera running talle L.

## Reserva de stock

Cuando una venta pasa al estado confirmada, el sistema puede reservar el stock de los productos incluidos.

La reserva reduce el stock disponible, pero no necesariamente reduce el stock físico.

Ejemplo:

Antes de confirmar:

- stock físico: 10
- stock reservado: 0
- stock disponible: 10

Después de confirmar una venta por 3 unidades:

- stock físico: 10
- stock reservado: 3
- stock disponible: 7

## Descuento definitivo de stock

El descuento definitivo de stock ocurre cuando la venta se despacha o entrega, según la configuración del sistema.

En ese momento, el stock físico debe disminuir.

Ejemplo:

Antes de despachar:

- stock físico: 10
- stock reservado: 3
- stock disponible: 7

Después de despachar 3 unidades:

- stock físico: 7
- stock reservado: 0
- stock disponible: 7

## Cancelación de venta y stock

Si una venta confirmada se cancela antes del despacho, el sistema debe liberar el stock reservado.

Ejemplo:

Venta confirmada por 2 unidades de una remera.

Antes de cancelar:

- stock físico: 10
- stock reservado: 2
- stock disponible: 8

Después de cancelar:

- stock físico: 10
- stock reservado: 0
- stock disponible: 10

## Devolución y stock

Cuando se acepta una devolución, el sistema puede aumentar nuevamente el stock físico del producto devuelto.

Esto solo debe ocurrir si el producto vuelve en condiciones aptas para la venta.

Si el producto no vuelve en condiciones aptas, la devolución no debe aumentar el stock disponible.

## Ajustes manuales de stock

El sistema puede permitir ajustes manuales de stock para corregir diferencias.

Motivos posibles:

- error de carga;
- pérdida;
- rotura;
- inventario físico;
- ingreso manual;
- devolución no asociada a venta;
- corrección administrativa.

Todo ajuste manual debe registrar:

- producto;
- variante;
- cantidad;
- tipo de ajuste;
- motivo;
- usuario responsable;
- fecha.

## Reglas importantes

1. No se debe confirmar una venta sin stock suficiente.
2. El stock disponible debe considerar el stock reservado.
3. Una venta cancelada debe liberar stock reservado.
4. Una devolución aceptada puede aumentar stock físico si el producto está apto para la venta.
5. Los ajustes manuales deben dejar trazabilidad.
6. El stock mínimo sirve para alertas, no necesariamente para bloquear ventas.
7. Cada variante de producto debe controlar su propio stock.

## Ejemplos de preguntas que puede responder el asistente

- ¿Qué significa stock disponible?
- ¿Qué diferencia hay entre stock físico y stock reservado?
- ¿Cuándo se descuenta el stock?
- ¿Qué pasa con el stock si cancelo una venta?
- ¿Qué pasa si una devolución vuelve apta para la venta?
- ¿Cuándo un producto se considera con bajo stock?
- ¿Puedo vender un producto con bajo stock?
