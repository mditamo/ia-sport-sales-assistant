# Glosario funcional del sistema de ventas de indumentaria deportiva

## Objetivo del glosario

Este glosario define los conceptos principales utilizados por el sistema de ventas de indumentaria deportiva.

Su objetivo es ayudar al asistente inteligente a interpretar correctamente preguntas de usuarios, recuperar documentación relevante mediante RAG y responder con vocabulario consistente.

## Cliente

Persona o entidad que realiza compras dentro del sistema.

Un cliente puede tener datos de contacto, direcciones, historial de compras, devoluciones, cambios y observaciones comerciales.

Ejemplo de pregunta:

"¿Cómo busco un cliente?"

## Cliente activo

Cliente habilitado para realizar compras y aparecer en reportes comerciales.

Es el estado normal de un cliente registrado.

## Cliente inactivo

Cliente que se conserva en el sistema, pero que no se utiliza habitualmente para nuevas operaciones.

No debe eliminarse si tiene historial de ventas.

## Cliente bloqueado

Cliente que no debería realizar nuevas compras sin revisión previa.

Puede bloquearse por deuda, problemas administrativos o comportamiento comercial riesgoso.

## Cliente frecuente

Cliente que realiza compras repetidas en un período determinado.

Puede identificarse por cantidad de compras, frecuencia o monto total comprado.

## Producto

Artículo comercializable dentro del sistema.

Ejemplos:

- remera deportiva;
- calza training;
- campera running;
- zapatilla;
- short;
- buzo;
- top deportivo;
- accesorio.

## Variante

Combinación específica de atributos de un producto.

Ejemplo:

Producto: Remera Dry-Fit  
Variante: talle M color negro.

La variante es importante porque el stock suele controlarse por talle y color.

## Categoría

Clasificación utilizada para ordenar productos.

Ejemplos:

- remeras;
- calzas;
- camperas;
- zapatillas;
- accesorios;
- shorts;
- buzos.

## Talle

Atributo de una variante que indica tamaño.

Ejemplos de talles de indumentaria:

- XS;
- S;
- M;
- L;
- XL;
- XXL.

Ejemplos de talles de calzado:

- 38;
- 39;
- 40;
- 41;
- 42.

## Color

Atributo visual de una variante.

Ejemplos:

- negro;
- blanco;
- azul;
- gris;
- rojo.

## Stock

Cantidad de unidades disponibles o existentes de un producto o variante.

El stock debe controlarse especialmente por producto, talle y color.

## Stock físico

Cantidad real de unidades existentes en depósito, local o sucursal.

El stock físico puede diferir del stock disponible si existen unidades reservadas.

## Stock reservado

Cantidad de unidades comprometidas para ventas confirmadas pero todavía no despachadas.

El stock reservado reduce el stock disponible.

## Stock disponible

Cantidad de unidades que realmente pueden venderse.

Fórmula conceptual:

stock disponible = stock físico - stock reservado

## Stock mínimo

Cantidad mínima deseada para un producto o variante.

Cuando el stock disponible es menor o igual al stock mínimo, el producto puede marcarse como bajo stock.

## Bajo stock

Estado de advertencia que indica que un producto o variante tiene pocas unidades disponibles.

El bajo stock no necesariamente bloquea la venta, pero alerta al usuario.

## Sin stock

Estado que indica que no hay unidades disponibles para vender.

Un producto sin stock no debería permitir confirmar una venta.

## Venta

Operación comercial en la que un cliente compra uno o más productos.

Una venta contiene cliente, productos, cantidades, precios, estado, pagos y total.

## Ítem de venta

Producto específico incluido dentro de una venta.

Ejemplo:

En una venta con 2 remeras y 1 campera, cada producto incluido es un ítem de venta.

## Subtotal

Importe parcial de un ítem de venta.

Fórmula:

subtotal = cantidad × precio unitario

## Total de venta

Importe final de una venta.

Se calcula sumando los subtotales de todos los ítems y aplicando descuentos si corresponde.

## Venta pendiente

Venta creada pero todavía no confirmada.

Puede modificarse y no descuenta stock definitivo.

## Venta confirmada

Venta validada por el usuario.

Antes de confirmarse, el sistema debe verificar stock suficiente.

Según la configuración del sistema, puede reservar stock.

## Venta pagada

Venta que tiene registrado el pago total.

Una venta puede estar pagada pero todavía no despachada ni entregada.

## Venta con pago parcial

Venta en la que el cliente pagó solo una parte del total.

El sistema debe registrar el monto pagado y el saldo pendiente.

## Venta despachada

Venta cuyos productos fueron preparados y enviados o entregados al cliente.

En este estado puede descontarse definitivamente el stock.

## Venta entregada

Venta que el cliente ya recibió.

Una venta entregada no debería cancelarse directamente. Si hay un problema, corresponde iniciar una devolución o cambio.

## Venta cancelada

Venta que no se concreta.

No debe descontar stock. Si había stock reservado, debe liberarse.

## Pago

Registro del dinero recibido por una venta.

Puede realizarse mediante efectivo, transferencia, tarjeta, billetera virtual u otro medio.

## Medio de pago

Forma en que el cliente realiza el pago.

Ejemplos:

- efectivo;
- transferencia;
- tarjeta de crédito;
- tarjeta de débito;
- billetera virtual.

## Devolución

Operación en la que el cliente retorna un producto comprado.

Puede generar reintegro, nota de crédito o devolución parcial.

## Devolución parcial

Devolución que afecta solo algunos productos de la venta original.

No necesariamente anula toda la venta.

## Cambio

Operación en la que el cliente devuelve un producto y recibe otro a cambio.

Puede ser por talle, color, modelo, falla o error de despacho.

## Cambio por talle

Cambio en el que el cliente devuelve una variante y recibe otra del mismo producto con talle diferente.

Ejemplo:

Devuelve una remera talle M y recibe una remera talle L.

## Cambio por producto diferente

Cambio en el que el cliente devuelve un producto y recibe otro distinto.

Si hay diferencia de precio, el sistema debe calcular saldo a favor o monto a pagar.

## Nota de crédito

Saldo a favor del cliente generado por una devolución o diferencia comercial.

Puede utilizarse para compras futuras, según la política del negocio.

## Reintegro

Devolución de dinero al cliente.

Debe quedar registrado con venta original, monto, medio de reintegro, fecha y usuario responsable.

## Producto apto para la venta

Producto devuelto que se encuentra en condiciones de volver al stock disponible.

Ejemplo:

Producto sin uso, limpio, completo y en buen estado.

## Producto no apto para la venta

Producto devuelto que no puede volver al stock disponible.

Ejemplo:

Producto usado, dañado, incompleto o sin condiciones comerciales válidas.

## Producto activo

Producto habilitado para venderse.

Debe aparecer en búsquedas comerciales y operaciones de venta.

## Producto inactivo

Producto que no debería ofrecerse en nuevas ventas.

Se mantiene para conservar historial.

## Producto discontinuado

Producto que ya no se comercializa, pero se conserva en el sistema por trazabilidad.

## Reporte

Vista o consulta que resume información del sistema.

Ejemplos:

- ventas por período;
- productos más vendidos;
- clientes frecuentes;
- productos con bajo stock;
- devoluciones por período.

## Ticket promedio

Monto promedio de las ventas en un período.

Fórmula conceptual:

ticket promedio = total vendido / cantidad de ventas

## RAG

Técnica que permite responder preguntas usando documentación externa recuperada desde una base de conocimiento.

En este sistema, el RAG se usa para responder preguntas funcionales sobre ventas, clientes, productos, stock, cambios y devoluciones.

Ejemplo:

"¿Cuándo se descuenta el stock?"

## MCP

Protocolo o capa de herramientas que permite al asistente conectarse con sistemas externos o módulos del negocio de forma controlada.

En este sistema, MCP puede exponer herramientas para clientes, productos, ventas, stock y reportes.

Ejemplo:

"Consultar stock de Remera Dry-Fit talle M."

## Agente

Componente inteligente que decide qué hacer ante una solicitud del usuario.

Puede elegir entre consultar el RAG, usar una herramienta MCP, pedir más datos o ejecutar un flujo.

## Consulta funcional

Pregunta sobre cómo funciona el sistema.

Ejemplo:

"¿Cómo se registra una devolución?"

Debe responderse principalmente con RAG.

## Consulta operativa

Solicitud que requiere consultar o modificar datos reales.

Ejemplo:

"Buscá el cliente Laura Gómez."

Debe resolverse mediante herramientas MCP.

## Consulta mixta

Solicitud que combina explicación funcional y operación sobre datos reales.

Ejemplo:

"Necesito devolver una remera de la venta 238. ¿Se puede?"

Debe usar RAG para revisar reglas y MCP para consultar la venta.

## LangChain

Framework que permite conectar modelos, prompts, recuperadores, herramientas y cadenas de procesamiento.

En este proyecto se usa para integrar el LLM con el RAG y las herramientas.

## LangGraph

Framework que permite modelar flujos con estado, pasos, decisiones y validaciones.

En este proyecto se puede usar para flujos como creación de venta, devolución o cambio.

## LLM

Modelo de lenguaje capaz de interpretar texto, razonar sobre instrucciones y generar respuestas.

En este proyecto se usa para interpretar la intención del usuario y redactar respuestas finales.

## Modelo de embeddings

Modelo que transforma texto en vectores numéricos para permitir búsqueda semántica.

Se usa para indexar documentos funcionales y recuperarlos desde el RAG.

## Vector store

Base de datos o almacenamiento donde se guardan los embeddings de los documentos.

Ejemplos:

- FAISS;
- Chroma;
- Milvus.

## Retriever

Componente que busca los fragmentos más relevantes dentro del vector store ante una pregunta del usuario.

## Chunk

Fragmento de documento usado por el RAG.

Los documentos se dividen en chunks para mejorar la recuperación de información.

## Ejemplos de preguntas relacionadas con este glosario

- ¿Qué es stock reservado?
- ¿Qué diferencia hay entre producto y variante?
- ¿Qué significa venta confirmada?
- ¿Qué es una devolución parcial?
- ¿Qué diferencia hay entre RAG y MCP?
- ¿Qué es una consulta mixta?
- ¿Qué es ticket promedio?
- ¿Qué hace un agente en este sistema?
