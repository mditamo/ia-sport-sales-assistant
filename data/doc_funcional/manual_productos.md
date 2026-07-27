# Manual funcional del módulo de productos

## Objetivo del módulo

El módulo de productos permite registrar, consultar y administrar los artículos disponibles para la venta dentro del sistema de indumentaria deportiva.

Un producto representa un artículo comercializable, como remeras, calzas, camperas, buzos, shorts, medias, zapatillas, tops deportivos, accesorios u otros productos relacionados.

El módulo permite:

- crear productos;
- clasificar productos por categoría;
- definir variantes;
- registrar talles y colores;
- consultar precios;
- consultar stock;
- actualizar información comercial;
- identificar productos activos o inactivos;
- analizar productos más vendidos.

## Entidad producto

Un producto es el registro principal de un artículo que puede ser vendido.

Un producto puede contener:

- nombre;
- descripción;
- categoría;
- marca;
- género o línea;
- precio de venta;
- costo estimado;
- margen esperado;
- estado;
- variantes;
- stock;
- imagen o referencia visual;
- observaciones.

## Ejemplos de productos

Ejemplos de productos en una tienda de ropa deportiva:

- Remera Dry-Fit;
- Calza Training;
- Campera Running;
- Short Deportivo;
- Buzo Oversize;
- Top Deportivo;
- Zapatilla Running;
- Media Deportiva;
- Mochila Deportiva;
- Gorra Training.

## Categorías de productos

Las categorías permiten ordenar los productos y facilitar búsquedas, reportes y navegación.

Categorías posibles:

- remeras;
- calzas;
- camperas;
- buzos;
- shorts;
- zapatillas;
- accesorios;
- medias;
- tops;
- conjuntos deportivos.

Ejemplo:

El producto "Remera Dry-Fit" puede pertenecer a la categoría "remeras".

## Variantes de producto

Una variante representa una combinación específica de atributos del producto.

En indumentaria deportiva, las variantes suelen definirse por:

- talle;
- color;
- modelo;
- género;
- temporada;
- material.

Ejemplo:

Producto: Remera Dry-Fit  
Variantes:

- talle S color negro;
- talle M color negro;
- talle L color azul;
- talle XL color blanco.

Cada variante puede tener stock y precio propio si el sistema lo permite.

## Talles

Los talles permiten diferenciar unidades disponibles de un mismo producto.

Talles posibles para indumentaria:

- XS;
- S;
- M;
- L;
- XL;
- XXL.

Talles posibles para calzado:

- 35;
- 36;
- 37;
- 38;
- 39;
- 40;
- 41;
- 42;
- 43;
- 44;
- 45.

Regla importante:

El stock debe controlarse por talle cuando el producto tiene variantes de talle.

## Colores

Los colores permiten diferenciar variantes visuales del producto.

Ejemplos de colores:

- negro;
- blanco;
- azul;
- gris;
- rojo;
- verde;
- rosa;
- violeta.

Regla importante:

Si un mismo producto existe en varios colores, el stock debe diferenciarse por color.

## Precio de venta

El precio de venta es el importe al que se ofrece el producto al cliente.

El precio puede definirse a nivel producto o a nivel variante, según la configuración del sistema.

Ejemplo:

Producto: Campera Running  
Precio de venta: $55.000

Si el producto tiene variantes con precios distintos, cada variante debe indicar su precio.

## Costo del producto

El costo del producto representa cuánto le cuesta al negocio adquirir o producir ese producto.

El costo puede utilizarse para calcular margen de ganancia.

Ejemplo:

Precio de venta: $40.000  
Costo: $24.000  
Margen bruto: $16.000

## Margen de ganancia

El margen permite analizar la rentabilidad de un producto.

Fórmula conceptual:

margen = precio de venta - costo

Ejemplo:

Si una calza cuesta $18.000 y se vende a $32.000, el margen bruto es $14.000.

## Estado del producto

### Activo

Un producto activo puede venderse y aparecer en búsquedas comerciales.

### Inactivo

Un producto inactivo no debería ofrecerse en nuevas ventas.

Puede mantenerse en el sistema para conservar historial de ventas.

### Sin stock

Un producto sin stock no tiene unidades disponibles para vender.

Puede seguir activo, pero el sistema debe advertir que no hay disponibilidad.

### Discontinuado

Un producto discontinuado ya no se comercializa.

No debería aparecer como opción principal para nuevas ventas, pero debe conservarse para reportes históricos.

## Alta de producto

Para crear un producto, el usuario debería indicar al menos:

- nombre;
- categoría;
- precio de venta;
- variantes, si corresponde;
- stock inicial, si corresponde.

Ejemplo:

Crear producto:

- nombre: Remera Dry-Fit;
- categoría: remeras;
- precio de venta: $18.000;
- variantes: talle S, M, L en color negro;
- stock inicial: 10 unidades por talle.

## Modificación de producto

El sistema debe permitir modificar datos de productos existentes.

Ejemplos de modificación:

- cambiar precio;
- actualizar descripción;
- agregar talle;
- agregar color;
- marcar como inactivo;
- actualizar categoría;
- corregir costo.

Regla importante:

Si el producto ya tiene ventas asociadas, no se recomienda eliminarlo. Conviene marcarlo como inactivo o discontinuado.

## Eliminación de productos

Un producto no debería eliminarse si tiene ventas asociadas.

Eliminar productos con historial puede afectar reportes, devoluciones y trazabilidad.

En lugar de eliminar, se recomienda usar estado inactivo o discontinuado.

## Consulta de stock de producto

El sistema debe permitir consultar stock por producto y variante.

Ejemplo de consulta:

"Consultar stock de Remera Dry-Fit talle M color negro."

Respuesta esperada:

"Remera Dry-Fit talle M color negro tiene 8 unidades disponibles."

Si el producto no existe o la variante no está registrada, el sistema debe informarlo claramente.

## Productos con bajo stock

Un producto tiene bajo stock cuando su stock disponible es menor o igual al stock mínimo definido.

Ejemplo:

Producto: Top Deportivo talle S color negro  
Stock disponible: 2  
Stock mínimo: 3  

Resultado: producto con bajo stock.

## Productos más vendidos

El sistema puede identificar productos más vendidos a partir del historial de ventas.

Criterios posibles:

- cantidad de unidades vendidas;
- monto total vendido;
- frecuencia de venta;
- ventas por período;
- ventas por categoría.

Ejemplo de consulta:

"Mostrame los productos más vendidos del último mes."

El sistema debería consultar las ventas del período y ordenar los productos por cantidad vendida o monto vendido.

## Productos por categoría

El sistema debe permitir listar productos filtrando por categoría.

Ejemplo:

"Mostrame todos los productos de la categoría zapatillas."

Respuesta esperada:

Listado de productos activos pertenecientes a la categoría zapatillas, incluyendo precio y disponibilidad si corresponde.

## Productos por atributo

El sistema puede permitir búsquedas por atributos.

Ejemplos:

- "remeras talle M";
- "calzas negras";
- "zapatillas running talle 40";
- "camperas impermeables";
- "productos para mujer";
- "buzos oversize".

El sistema debe interpretar estos atributos para encontrar productos o variantes relacionadas.

## Reglas importantes

1. Todo producto debe tener nombre y categoría.
2. Los productos con talles deben controlar stock por talle.
3. Los productos con colores deben controlar stock por color.
4. No se recomienda eliminar productos con ventas asociadas.
5. Los productos inactivos no deberían aparecer como opción principal de venta.
6. El stock debe consultarse sobre la variante específica.
7. El precio de venta puede definirse por producto o variante.
8. Los productos discontinuados deben conservarse para historial.
9. Un producto sin stock no debería confirmarse en una venta.
10. Los cambios de precio no deben alterar ventas históricas ya registradas.

## Consultas frecuentes sobre productos

### ¿Qué diferencia hay entre producto y variante?

El producto es el artículo general. La variante es una combinación específica de talle, color u otro atributo.

Ejemplo:

Producto: Remera Dry-Fit.  
Variante: Remera Dry-Fit talle M color negro.

### ¿Puedo vender un producto inactivo?

No se recomienda. Un producto inactivo debería quedar fuera de nuevas ventas.

### ¿Puedo cambiar el precio de un producto?

Sí. El cambio de precio debe afectar ventas futuras, pero no debería modificar ventas históricas ya registradas.

### ¿Qué pasa si un producto no tiene stock?

El sistema debe advertirlo y no debería permitir confirmar una venta con ese producto.

### ¿Puedo eliminar un producto vendido anteriormente?

No se recomienda. Debe conservarse para mantener el historial. En su lugar, puede marcarse como inactivo o discontinuado.

## Ejemplos de preguntas que puede responder el asistente

- ¿Cómo creo un producto?
- ¿Qué es una variante?
- ¿Cómo cargo talles y colores?
- ¿Cómo consulto stock de una variante?
- ¿Qué significa producto discontinuado?
- ¿Puedo eliminar un producto con ventas?
- ¿Cómo cambio el precio de un producto?
- ¿Cómo veo productos con bajo stock?
- ¿Cómo busco productos por categoría?
- ¿Cómo identifico los productos más vendidos?
