# Manual funcional del módulo de clientes

## Objetivo del módulo

El módulo de clientes permite registrar, consultar y administrar la información de las personas que compran productos dentro del sistema de ventas de indumentaria deportiva.

Un cliente representa a una persona o entidad que realiza compras, solicita presupuestos, registra devoluciones o mantiene historial comercial con el negocio.

El módulo permite:

- crear clientes;
- buscar clientes existentes;
- actualizar datos personales;
- consultar historial de compras;
- registrar datos de contacto;
- asociar ventas al cliente;
- consultar devoluciones o cambios realizados;
- identificar clientes frecuentes.

## Entidad cliente

Un cliente es el registro principal de una persona compradora dentro del sistema.

Un cliente puede contener:

- nombre;
- apellido;
- documento o identificación;
- teléfono;
- correo electrónico;
- dirección;
- ciudad;
- provincia;
- fecha de alta;
- estado;
- observaciones;
- historial de compras.

## Datos mínimos para crear un cliente

Para crear un cliente, el sistema debería solicitar al menos:

- nombre;
- apellido;
- teléfono o correo electrónico.

El documento puede ser opcional, salvo que el negocio lo requiera para facturación, envíos o control administrativo.

Ejemplo:

Para registrar a una clienta llamada Sofía Ramírez, se puede cargar:

- nombre: Sofía;
- apellido: Ramírez;
- teléfono: 11-5555-1234;
- email: sofia.ramirez@email.com.

## Estados de un cliente

### Activo

Un cliente activo puede realizar compras, recibir comunicaciones y figurar en reportes comerciales.

Este es el estado habitual de un cliente registrado.

### Inactivo

Un cliente inactivo es aquel que no realiza compras desde hace un período prolongado o que fue marcado manualmente por el usuario.

Un cliente inactivo no se elimina del sistema, porque debe conservarse su historial de compras.

### Bloqueado

Un cliente bloqueado es aquel que no debería realizar nuevas compras sin revisión previa.

Motivos posibles:

- deuda pendiente;
- comportamiento comercial problemático;
- operaciones fraudulentas;
- solicitud administrativa interna.

El sistema debería advertir al usuario si intenta crear una venta para un cliente bloqueado.

## Búsqueda de clientes

El sistema debe permitir buscar clientes por diferentes criterios:

- nombre;
- apellido;
- documento;
- teléfono;
- correo electrónico;
- ciudad;
- historial de compras.

Ejemplo de búsqueda:

"Buscar cliente Laura Gómez."

El sistema debería devolver coincidencias posibles y permitir seleccionar la correcta.

## Clientes duplicados

Un cliente duplicado ocurre cuando una misma persona fue cargada más de una vez.

Ejemplo:

- Laura Gómez con teléfono 11-2222-3333;
- Laura G. con el mismo teléfono;
- Laura Gómez con el mismo correo electrónico.

El sistema debería advertir posibles duplicados antes de crear un nuevo cliente.

Regla recomendada:

Antes de crear un cliente, buscar coincidencias por teléfono, correo electrónico y documento.

## Historial de compras

El historial de compras permite consultar todas las ventas asociadas a un cliente.

El historial puede mostrar:

- fecha de la venta;
- productos comprados;
- total de la venta;
- estado de la venta;
- estado de pago;
- devoluciones asociadas;
- cambios realizados.

Ejemplo de consulta:

"Mostrame las compras de Sofía Ramírez en los últimos 60 días."

El sistema debería buscar a la clienta y listar las ventas correspondientes al período solicitado.

## Cliente frecuente

Un cliente puede considerarse frecuente cuando realiza compras de manera repetida.

Criterios posibles:

- cantidad de compras en un período;
- monto total comprado;
- frecuencia de compra;
- fecha de última compra.

Ejemplo:

Un cliente que compró 5 veces en los últimos 90 días puede ser marcado como cliente frecuente.

## Segmentación de clientes

El sistema puede segmentar clientes para análisis o acciones comerciales.

Segmentos posibles:

- clientes frecuentes;
- clientes nuevos;
- clientes inactivos;
- clientes con mayor facturación;
- clientes con devoluciones recientes;
- clientes que compraron una categoría específica;
- clientes que no compran hace más de 90 días.

Ejemplo de consulta:

"Listá clientes que compraron zapatillas running en los últimos 30 días."

El sistema debería consultar el historial de ventas y devolver clientes que cumplan esa condición.

## Datos de contacto

Los datos de contacto permiten comunicarse con el cliente para confirmar ventas, coordinar envíos o enviar información comercial.

Datos posibles:

- teléfono;
- WhatsApp;
- correo electrónico;
- dirección;
- ciudad;
- código postal;
- redes sociales.

Regla importante:

No se recomienda eliminar datos históricos de contacto si están asociados a ventas anteriores. En esos casos, conviene actualizar el cliente manteniendo trazabilidad.

## Dirección del cliente

La dirección del cliente puede utilizarse para envíos o entregas.

Una dirección puede contener:

- calle;
- número;
- piso;
- departamento;
- ciudad;
- provincia;
- código postal;
- referencias de entrega.

Un cliente puede tener más de una dirección registrada.

Ejemplo:

- dirección particular;
- dirección laboral;
- dirección de envío alternativa.

## Asociación entre cliente y venta

Toda venta puede estar asociada a un cliente.

Esto permite:

- consultar historial comercial;
- analizar comportamiento de compra;
- gestionar cambios y devoluciones;
- generar reportes;
- contactar al cliente por problemas de pago o envío.

Regla recomendada:

Una venta debería asociarse a un cliente antes de ser confirmada.

## Edición de datos del cliente

El sistema debe permitir actualizar datos de un cliente cuando cambian.

Ejemplos:

- cambiar teléfono;
- actualizar correo electrónico;
- modificar dirección;
- agregar observaciones;
- cambiar estado del cliente.

No se recomienda eliminar clientes con ventas asociadas, porque se pierde trazabilidad.

## Eliminación de clientes

Un cliente no debería eliminarse si tiene ventas asociadas.

En lugar de eliminarlo, el sistema puede marcarlo como inactivo.

Esto permite conservar el historial comercial y evitar inconsistencias en reportes.

## Observaciones del cliente

El campo observaciones permite registrar información útil para atención o gestión comercial.

Ejemplos:

- "Prefiere contacto por WhatsApp."
- "Retira los pedidos por el local."
- "Suele comprar productos de running."
- "Tiene devolución pendiente de revisión."

Las observaciones deben ser claras, breves y relevantes.

## Consultas frecuentes sobre clientes

### ¿Puedo crear una venta sin cliente?

Depende de la configuración del sistema. Para operaciones trazables, se recomienda asociar siempre una venta a un cliente.

### ¿Qué pasa si el cliente ya existe?

El sistema debería evitar duplicados. Antes de crear un cliente nuevo, conviene buscarlo por nombre, teléfono, email o documento.

### ¿Puedo eliminar un cliente con ventas?

No se recomienda. Si el cliente tiene ventas asociadas, debería marcarse como inactivo en lugar de eliminarse.

### ¿Para qué sirve el historial de compras?

Sirve para consultar compras anteriores, analizar comportamiento, gestionar devoluciones y detectar clientes frecuentes.

### ¿Qué significa cliente bloqueado?

Significa que el cliente no debería realizar nuevas compras sin revisión previa.

## Ejemplos de preguntas que puede responder el asistente

- ¿Cómo creo un cliente?
- ¿Qué datos necesito para registrar un cliente?
- ¿Cómo busco un cliente por teléfono?
- ¿Puedo eliminar un cliente con ventas?
- ¿Cómo veo el historial de compras de un cliente?
- ¿Qué significa cliente inactivo?
- ¿Cómo identifico clientes frecuentes?
- ¿Cómo evito clientes duplicados?
- ¿Puedo asociar varias direcciones a un cliente?
