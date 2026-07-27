"""
mcp_servers/clientes_server.py

Servidor MCP para clientes.
Ejecutar: python mcp_servers/clientes_server.py
"""
from __future__ import annotations
from typing import Any, Dict, Optional
from tools import get_connection, _build_where_clause, _rows_to_dicts, _response, _logger
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("clientes-mcp")
logger = _logger()

# Inicialización inmediata al importar el módulo.
get_connection()

@mcp.tool()
def listar_clientes(estado: Optional[str] = None, limite: int = 20) -> Dict[str, Any]:
    """Lista clientes registrados. Puede filtrar por estado: Activo, Inactivo o Bloqueado."""
    conn = get_connection()
    query_where, params = _build_where_clause(conn, 'clientes', {'estado': estado})
    sql = f"SELECT * FROM clientes {query_where} ORDER BY clientes.nombre ASC LIMIT {limite}"
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
def buscar_cliente(nombre: Optional[str] = None, apellido: Optional[str] = None, documento: Optional[str] = None, telefono: Optional[str] = None, email: Optional[str] = None, ciudad: Optional[str] = None, provincia: Optional[str] = None, estado: Optional[str] = None, limite: int = 10) -> Dict[str, Any]:
    """Busca clientes por nombre, apellido, documento, teléfono, email, ciudad o provincia."""
    conn = get_connection()
    query_where, params = _build_where_clause(conn, 'clientes', {'nombre': nombre, 'apellido': apellido, 'documento': documento, 'telefono': telefono, 'email': email, 'ciudad': ciudad, 'provincia': provincia, 'estado': estado})
    sql = f"SELECT * FROM clientes {query_where} ORDER BY clientes.nombre ASC LIMIT {limite}"
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
def obtener_cliente(cliente_id: str) -> Dict[str, Any]:
    """Obtiene un cliente exacto por cliente_id. Ejemplo: CLI010."""
    conn = get_connection()
    query_where, params = _build_where_clause(conn, 'clientes', {'cliente_id': cliente_id})
    sql = f"SELECT * FROM clientes {query_where}"
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
def resumen_cliente(cliente_id: str) -> Dict[str, Any]:
    """Resume cantidad de ventas, total comprado, última compra y si el cliente es frecuente."""
    conn = get_connection()
    sql=f"SELECT clientes.*, sum(ventas.total_venta) as total_comprado, count(*) as cantidad_compras, max(ventas.fecha) as fecha_ultima_compra, CASE WHEN count(*) > 5 THEN 'SI' ELSE 'NO' END  as frecuente FROM clientes JOIN ventas ON clientes.cliente_id=ventas.cliente_id WHERE ventas.estado_venta!='Cancelada' AND clientes.cliente_id=? GROUP BY clientes.cliente_id"
    params=(cliente_id,)
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
def clientes_frecuentes(limite: int = 10) -> Dict[str, Any]:
    """Lista clientes frecuentes: 5 o más ventas no canceladas."""
    conn = get_connection()
    sql= f"SELECT clientes.* FROM clientes  JOIN ventas ON clientes.cliente_id=ventas.cliente_id WHERE ventas.estado_venta!='Cancelada' GROUP BY clientes.cliente_id HAVING count(*)>5 ORDER BY count(*) DESC LIMIT {limite}"
    logger.info("SQL: %s", sql)
    cursor = conn.execute(sql, [])
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
    
if __name__ == "__main__":
    mcp.run()
