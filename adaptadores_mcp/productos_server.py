"""
mcp_servers/productos_server.py

Servidor MCP para productos y stock.
Ejecutar: python mcp_servers/productos_server.py
"""
from __future__ import annotations
from typing import Any, Dict, Optional
from tools import get_connection, _build_where_clause, _rows_to_dicts, _response, _logger
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("productos-mcp")
logger = _logger()

# Inicialización inmediata al importar el módulo.
get_connection()

@mcp.tool()
def listar_productos(categoria: Optional[str] = None, estado: Optional[str] = "Activo", limite: int = 20) -> Dict[str, Any]:
    """Lista productos/variantes. Puede filtrar por categoría y estado."""
    conn = get_connection()
    query_where, params = _build_where_clause(conn, 'productos', {'categoria': categoria, 'estado': estado})
    sql = f"SELECT * FROM productos {query_where} ORDER BY productos.nombre ASC LIMIT {limite}"
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
def buscar_producto(nombre: Optional[str] = None, categoria: Optional[str] = None, talle: Optional[str] = None, color: Optional[str] = None, estado: Optional[str] = "Activo", limite: int = 10) -> Dict[str, Any]:
    """Busca productos por nombre, categoría, marca, talle, color o línea."""
    conn = get_connection()
    query_where, params = _build_where_clause(conn, 'productos', {'nombre': nombre, 'categoria': categoria, 'talle': talle, 'color': color, 'estado': estado})
    sql = f"SELECT * FROM productos {query_where} ORDER BY productos.nombre ASC LIMIT {limite}"
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
def obtener_producto(producto_id: str) -> Dict[str, Any]:
    """Obtiene un producto/variante exacto por producto_id. Ejemplo: PROD016."""
    conn = get_connection()
    query_where, params = _build_where_clause(conn, 'productos', {'producto_id': producto_id})
    sql = f"SELECT * FROM productos {query_where}"
    logger.info("SQL: %s", sql)
    logger.info("filtros: %s", params)
    cursor = conn.execute(sql, params)
    row = dict(cursor.fetchone())
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
def consultar_stock(producto_id: str) -> Dict[str, Any]:
    """Consulta stock físico, reservado, disponible, mínimo y alerta de stock."""
    conn = get_connection()
    sql = f"SELECT productos.*, CASE WHEN productos.estado='Activo' AND productos.stock_disponible>0  THEN 'SI' ELSE 'NO' END as puede_venderse FROM productos WHERE productos.producto_id=?"
    params = (producto_id,)
    logger.info("SQL: %s", sql)
    logger.info("filtros: %s", params)
    cursor = conn.execute(sql, params)
    row = dict(cursor.fetchone())
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
def productos_bajo_stock(limite: int = 20) -> Dict[str, Any]:
    """Lista productos activos con bajo stock o sin stock."""
    conn = get_connection()
    sql=f"SELECT * FROM productos WHERE productos.alerta_stock IN ('Bajo stock', 'Sin stock') AND productos.estado='Activo' ORDER BY productos.stock_disponible ASC LIMIT {limite}"
    logger.info("SQL: %s", sql)
    cursor = conn.execute(sql,[])
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
def listar_categorias() -> Dict[str, Any]:
    """Lista categorías existentes en productos.csv."""
    conn = get_connection()
    sql=f"SELECT categoria FROM productos GROUP BY categoria"
    logger.info("SQL: %s", sql)
    cursor = conn.execute(sql,[])
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
def productos_por_categoria(categoria: str, limite: int = 20) -> Dict[str, Any]:
    """Lista productos activos de una categoría."""
    return listar_productos(categoria=categoria, estado="Activo", limite=limite)


if __name__ == "__main__":
    mcp.run()
