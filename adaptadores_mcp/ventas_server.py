"""
mcp_servers/ventas_server.py

Servidor MCP para ventas y reportes. 
Ejecutar: python mcp_servers/ventas_server.py
"""
from __future__ import annotations

from typing import Any, Dict, List, Optional
from tools import get_connection, _build_where_clause, _rows_to_dicts, _response, _logger
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("ventas-mcp")
logger = _logger()

# Inicialización inmediata al importar el módulo.
get_connection()

def get_venta_items(venta_id: str) -> List[Dict[str, Any]]:
    """Obtiene los items de una venta por venta_id."""
    conn = get_connection()
    query_where, params = _build_where_clause(conn, 'ventas_productos', {'venta_id': venta_id})
    sql = f"SELECT * FROM ventas_productos {query_where}"
    logger.info("SQL: %s", sql)
    logger.info("filtros: %s", params)
    cursor = conn.execute(sql, params)
    return _rows_to_dicts(cursor.fetchall())

@mcp.tool()
def obtener_venta(venta_id: str) -> Dict[str, Any]:
    """Consulta una venta por venta_id e incluye el detalle de productos."""
    conn = get_connection()
    query_where, params = _build_where_clause(conn, 'ventas', {'venta_id': venta_id})
    sql = f"SELECT * FROM ventas {query_where}"
    logger.info("SQL: %s", sql)
    logger.info("filtros: %s", params)
    cursor = conn.execute(sql, params)
    row = dict(cursor.fetchone())
    row["items"] = get_venta_items(venta_id)
    logger.info("ROW: %s", row)
    if not row:
        return _response(
            status_code=404,
            status="not_found",
            message="No se encontraron coincidencias para los filtros indicados.",
            data=[],
        )

    return _response(
        status_code=200,
        status="ok",
        message="Consulta exitosa.",
        data=row,
    )

@mcp.tool()
def listar_ventas(fecha_desde: str, fecha_hasta: str, estado_venta: Optional[str] = None, limite: int = 20) -> Dict[str, Any]:
    """Lista ventas con filtros opcionales de fecha y estado."""
    conn = get_connection()
    sql = f"SELECT * FROM ventas WHERE ventas.fecha BETWEEN ? and ?"
    if estado_venta:
        sql += " AND ventas.estado_venta=?"
    sql += " ORDER BY ventas.fecha DESC LIMIT ?"
    params = (fecha_desde, fecha_hasta, estado_venta, limite) if estado_venta else (fecha_desde, fecha_hasta, limite)
    logger.info("SQL: %s", sql)
    logger.info("filtros: %s", params)
    cursor = conn.execute(sql, params)
    rows = _rows_to_dicts(cursor.fetchall())
    logger.info("ROWS: %s", rows)
    if not rows:
        return _response(
            status_code=404,
            status="not_found",
            message="No se encontraron coincidencias para los filtros indicados.",
            data=[],
        )

    return _response(
        status_code=200,
        status="ok",
        message="Consulta exitosa.",
        data=rows,
    )

@mcp.tool()
def listar_ventas_cliente(cliente_id: str, fecha_desde: str, fecha_hasta: str, limite: int = 20) -> Dict[str, Any]:
    """Lista ventas de un cliente."""
    conn = get_connection()
    sql = f"SELECT * FROM ventas WHERE ventas.cliente_id = ? AND ventas.fecha BETWEEN ? and ? ORDER BY ventas.fecha DESC LIMIT ?"
    params = (cliente_id, fecha_desde, fecha_hasta, limite)
    logger.info("SQL: %s", sql)
    logger.info("filtros: %s", params)
    cursor = conn.execute(sql, params)
    rows = _rows_to_dicts(cursor.fetchall())
    logger.info("ROWS: %s", rows)
    if not rows:
        return _response(
            status_code=404,
            status="not_found",
            message="No se encontraron coincidencias para los filtros indicados.",
            data=[],
        )

    return _response(
        status_code=200,
        status="ok",
        message="Consulta exitosa.",
        data=rows,
    )

@mcp.tool()
def resumen_ventas_por_periodo(fecha_desde: str, fecha_hasta: str, excluir_canceladas: bool = True) -> Dict[str, Any]:
    """Resume cantidad de ventas, total vendido, total pagado, saldo y agrupaciones de un período."""
    
    params = (fecha_desde, fecha_hasta)
    
    conn = get_connection()
    sql = f"SELECT COUNT(*) as cantidad_ventas, SUM(ventas.total_venta) as total_vendido, SUM(ventas.monto_pagado) as total_pagado, SUM(ventas.saldo_pendiente) as saldo_pendiente, ROUND( SUM(ventas.total_venta)/COUNT(*),2) as ticket_promedio FROM ventas WHERE ventas.fecha BETWEEN ? and ?"
    if excluir_canceladas:
        sql += " AND ventas.estado_venta!='Cancelada'"
    
    logger.info("SQL: %s", sql)
    logger.info("filtros: %s", params)
    cursor = conn.execute(sql, (fecha_desde, fecha_hasta))
    row_resumen = dict(cursor.fetchone())
    logger.info("ROW RESUMEN: %s", row_resumen)
    
    sql_ventas_por_estado = f"SELECT ventas.estado_venta, COUNT(*) as cantidad FROM ventas WHERE ventas.fecha BETWEEN ? and ?"
    if excluir_canceladas:
       sql_ventas_por_estado += " AND ventas.estado_venta!='Cancelada'"
    sql_ventas_por_estado += " GROUP BY ventas.estado_venta"
    logger.info("SQL: %s", sql_ventas_por_estado)
    logger.info("filtros: %s", params)
    cursor = conn.execute(sql_ventas_por_estado, params)
    ventas_por_estado = _rows_to_dicts(cursor.fetchall())
    logger.info("VENTAS POR ESTADO: %s", ventas_por_estado)
    
    sql_ventas_por_medio_pago = f"SELECT ventas.medio_pago, COUNT(*) as cantidad FROM ventas WHERE ventas.fecha BETWEEN ? and ?"
    if excluir_canceladas:
       sql_ventas_por_medio_pago += " AND ventas.estado_venta!='Cancelada'"
    sql_ventas_por_medio_pago += " GROUP BY ventas.medio_pago"
    logger.info("SQL: %s", sql_ventas_por_medio_pago)
    logger.info("filtros: %s", params)
    cursor = conn.execute(sql_ventas_por_medio_pago, params)
    ventas_por_medio_pago = _rows_to_dicts(cursor.fetchall())
    logger.info("VENTAS POR MEDIO DE PAGO: %s", ventas_por_medio_pago)

    sql_ventas_por_canal = f"SELECT ventas.canal_venta, COUNT(*) as cantidad FROM ventas WHERE ventas.fecha BETWEEN ? and ?"
    if excluir_canceladas:
        sql_ventas_por_canal += " AND ventas.estado_venta!='Cancelada'"
    sql_ventas_por_canal += " GROUP BY ventas.canal_venta"
    logger.info("SQL: %s", sql_ventas_por_canal)
    logger.info("filtros: %s", params)
    cursor = conn.execute(sql_ventas_por_canal, params)
    ventas_por_canal = _rows_to_dicts(cursor.fetchall())
    logger.info("VENTAS POR CANAL: %s", ventas_por_canal)
            
    return {
        "fecha_desde": fecha_desde,
        "fecha_hasta": fecha_hasta,
        "cantidad_ventas": row_resumen["cantidad_ventas"],
        "total_vendido": row_resumen["total_vendido"],
        "total_pagado": row_resumen["total_pagado"],
        "saldo_pendiente": row_resumen["saldo_pendiente"],
        "ticket_promedio": row_resumen["ticket_promedio"],
        "ventas_por_estado": ventas_por_estado,
        "ventas_por_medio_pago": ventas_por_medio_pago,
        "ventas_por_canal": ventas_por_canal,
    }


@mcp.tool()
def ticket_promedio(fecha_desde: str, fecha_hasta: str, excluir_canceladas: bool = True) -> Dict[str, Any]:
    """Calcula ticket promedio de ventas en un período."""
    resumen = resumen_ventas_por_periodo(fecha_desde, fecha_hasta, excluir_canceladas)
    return {"fecha_desde": fecha_desde, "fecha_hasta": fecha_hasta, "cantidad_ventas": resumen["cantidad_ventas"], "total_vendido": resumen["total_vendido"], "ticket_promedio": resumen["ticket_promedio"]}

@mcp.tool()
def productos_mas_vendidos(fecha_desde: str, fecha_hasta: str, limite: int = 10) -> Dict[str, Any]:
    """Lista productos más vendidos de un período. ordenar_por puede ser cantidad o monto."""
    conn = get_connection()
    sql=f"SELECT ventas_productos.producto_id, ventas_productos.producto_nombre, ventas_productos.categoria, SUM(ventas_productos.cantidad) as cantidad_vendida, SUM(ventas_productos.total_item) as monto_vendido FROM ventas  JOIN ventas_productos ON ventas.venta_id=ventas_productos.venta_id WHERE ventas.fecha BETWEEN ? and ? AND ventas.estado_venta!='Cancelada' GROUP BY ventas_productos.producto_id ORDER BY cantidad_vendida DESC , monto_vendido DESC LIMIT ?"
    
    params = (fecha_desde, fecha_hasta, limite)
    logger.info("SQL: %s", sql)
    logger.info("filtros: %s", params)
    cursor = conn.execute(sql, params)
    rows = _rows_to_dicts(cursor.fetchall())
    logger.info("ROWS: %s", rows)
    if not rows:
        return _response(
            status_code=404,
            status="not_found",
            message="No se encontraron coincidencias para los filtros indicados.",
            data=[],
        )

    return _response(
        status_code=200,
        status="ok",
        message="Consulta exitosa.",
        data=rows,
    )

@mcp.tool()
def ventas_por_cliente(fecha_desde: str, fecha_hasta: str, limite: int = 10) -> Dict[str, Any]:
    """Ranking de clientes por monto comprado en un período."""
    conn = get_connection()
    sql = f"SELECT ventas.cliente_id, ventas.cliente_nombre, count(*) as cantidad_ventas, SUM(ventas.total_venta) as total_comprado FROM ventas WHERE ventas.fecha BETWEEN ? and ? AND ventas.estado_venta!='Cancelada' GROUP BY ventas.cliente_id ORDER BY total_comprado DESC LIMIT ?"
    params = (fecha_desde, fecha_hasta, limite)
    logger.info("SQL: %s", sql)
    logger.info("filtros: %s", params)
    cursor = conn.execute(sql, params)
    rows = _rows_to_dicts(cursor.fetchall())
    logger.info("ROWS: %s", rows)
    if not rows:
        return _response(
            status_code=404,
            status="not_found",
            message="No se encontraron coincidencias para los filtros indicados.",
            data=[],
        )

    return _response(
        status_code=200,
        status="ok",
        message="Consulta exitosa.",
        data=rows,
    )


@mcp.tool()
def validar_venta_simulada(cliente_id: str, items: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Valida una venta sin escribir en la DB. Items: [{'producto_id': 'PROD001', 'cantidad': 2}]."""
    conn = get_connection()
    query_where, params = _build_where_clause(conn, 'clientes', {'cliente_id': cliente_id})
    sql_cliente = f"SELECT * FROM clientes {query_where}"
    logger.info("SQL: %s", sql_cliente)
    logger.info("filtros: %s", params)
    cursor = conn.execute(sql_cliente, params)
    row_cliente = dict(cursor.fetchone())
    logger.info("ROW CLIENTE: %s", row_cliente)

    if not row_cliente:
        return {"venta_valida": False, "mensaje": f"No se encontró el cliente {cliente_id}."}
    if row_cliente.get("estado") == "Bloqueado":
        return {"venta_valida": False, "mensaje": "El cliente está bloqueado y requiere revisión.", "cliente": row_cliente}
    
    errores = []
    detalle = []
    total = 0.0
    for item in items:
        pid = item.get("producto_id")
        cantidad = int(item.get("cantidad", 0))
        
        query_where, params = _build_where_clause(conn, 'productos', {'producto_id': pid})
        sql_producto = f"SELECT * FROM productos {query_where}"
        logger.info("SQL: %s", sql_producto)
        logger.info("filtros: %s", params)
        cursor = conn.execute(sql_producto, params)
        row_producto = dict(cursor.fetchone())
        logger.info("ROW PRODUCTO: %s", row_producto)
        
        if not row_producto:
            errores.append({"producto_id": item.get("producto_id"), "error": "Producto inexistente."})
            continue
        if cantidad <= 0:
            errores.append({"producto_id": row_producto.get("producto_id"), "error": "La cantidad debe ser mayor a cero."})
            continue
        if row_producto.get("estado") != "Activo":
            errores.append({"producto_id": row_producto.get("producto_id"), "producto_nombre": row_producto.get("nombre"), "error": "El producto no está activo."})
            continue
        disponible = int(row_producto.get("stock_disponible"))
        if disponible < cantidad:
            errores.append({"producto_id": row_producto.get("producto_id"), "producto_nombre": row_producto.get("nombre"), "talle": row_producto.get("talle"), "color": row_producto.get("color"), "stock_disponible": disponible, "cantidad_solicitada": cantidad, "error": "Stock insuficiente."})
            continue
        precio = float(row_producto.get("precio_venta"))
        subtotal = precio * cantidad
        total += subtotal
        detalle.append({"producto_id": row_producto.get("producto_id"), "producto_nombre": row_producto.get("nombre"), "talle": row_producto.get("talle"), "color": row_producto.get("color"), "cantidad": cantidad, "precio_unitario": precio, "subtotal": subtotal})
    venta_valida = len(errores) == 0 and len(detalle) > 0
    respuesta= {"venta_valida": venta_valida, "cliente": {"cliente_id": row_cliente.get("cliente_id"), "nombre_completo": f"{row_cliente.get('nombre')} {row_cliente.get('apellido')}", "estado": row_cliente.get("estado")}, "detalle": detalle, "errores": errores, "total_estimado": total, "mensaje": "La venta puede crearse según la validación simulada." if venta_valida else "La venta no puede crearse porque existen errores de validación."}
    logger.info("RESPUESTA: %s", respuesta)
    return respuesta


if __name__ == "__main__":
    mcp.run()
