from __future__ import annotations

import asyncio
import json
import os
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional
from langchain.tools import tool

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from retrieval.retriever import retrieve_context, format_documents
  
PROJECT_ROOT = Path(__file__).resolve().parents[1]
MCP_DATA_DIR =  Path(os.getenv("MCP_DATA_DIR", "data/mcp")).resolve()

MCP_SERVERS = {
    "clientes": PROJECT_ROOT / "adaptadores_mcp" / "clientes_server.py",
    "productos": PROJECT_ROOT / "adaptadores_mcp" / "productos_server.py",
    "ventas": PROJECT_ROOT / "adaptadores_mcp" / "ventas_server.py",
}


def _extract_text_from_mcp_result(result: Any) -> str:
    if hasattr(result, "content"):
        parts = []
        for item in result.content:
            parts.append(getattr(item, "text", str(item)))
        return "\n".join(parts)
    return str(result)


def _parse_json_if_possible(text: str) -> Any:
    try:
        return json.dumps(text, ensure_ascii=False, default=str)
    except Exception:
        return json.dumps({"error": "No se pudo serializar el resultado."}, ensure_ascii=False)

async def call_mcp_tool_async(
    server_name: str,
    tool_name: str,
    arguments: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    if server_name not in MCP_SERVERS:
        return {"ok": False, "error": f"Servidor MCP desconocido: {server_name}"}

    server_path = MCP_SERVERS[server_name]

    if not server_path.exists():
        return {"ok": False, "error": f"No existe el servidor MCP: {server_path}"}

    if not MCP_DATA_DIR.exists():
        return {"ok": False, "error": f"No existe la carpeta data: {MCP_DATA_DIR}"}

    server_params = StdioServerParameters(
        command=sys.executable,
        args=[str(server_path)],
        env=os.environ.copy(),
    )

    try:
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                result = await session.call_tool(tool_name, arguments=arguments or {})
                text = _extract_text_from_mcp_result(result)

                return {
                    "ok": True,
                    "server": server_name,
                    "tool": tool_name,
                    "arguments": arguments or {},
                    "raw_text": text,
                    "data": _parse_json_if_possible(text),
                }

    except Exception as exc:
        return {
            "ok": False,
            "server": server_name,
            "tool": tool_name,
            "arguments": arguments or {},
            "error": repr(exc),
        }


def call_mcp_tool(
    server_name: str,
    tool_name: str,
    arguments: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    return asyncio.run(call_mcp_tool_async(server_name, tool_name, arguments))


def rag_retrieve_context(question: str, top_k: int = 4) -> Dict[str, Any]:
    """
    Ejecuta el RAG funcional con diagnóstico claro.
    """
    from pathlib import Path
    CHROMA_DIR = Path(
        os.getenv("PERSIST_DIRECTORY", "chroma_db")
    ).resolve()
    try:
    
        if not CHROMA_DIR.exists():
            return {
                "ok": False,
                "question": question,
                "error": f"No existe chroma_db: {str(CHROMA_DIR)}",
                "hint": "Ejecutá primero: python -m retrieval.ingest",
            }

        result = retrieve_context(query=question, top_k=top_k)
        
        return {
            "ok": True,
            "question": question,
            "sources": format_documents(result),
        }

    except Exception as exc:
        return {
            "ok": False,
            "question": question,
            "error": repr(exc),
            "hint": (
                "Probá primero: python test/test_rag_retriever.py. "
                "Si ese test falla, el problema está en RAG y no en LangGraph."
            ),
        }

def listar_clientes(estado: str, limite: int = 20) -> Dict[str, Any]:
    return call_mcp_tool("clientes", "listar_clientes", {"estado": estado, "limite": limite})
def buscar_cliente(nombre: Optional[str] = None, apellido: Optional[str] = None, documento: Optional[str] = None, telefono: Optional[str] = None, email: Optional[str] = None, ciudad: Optional[str] = None, provincia: Optional[str] = None, estado: Optional[str] = None, limite: int = 10) -> Dict[str, Any]:
    return call_mcp_tool("clientes", "buscar_cliente", {"nombre": nombre, "apellido": apellido, "documento": documento, "telefono": telefono, "email": email, "ciudad": ciudad, "provincia": provincia, "estado": estado, "limite": limite})
def obtener_cliente(cliente_id: str) -> Dict[str, Any]:
    return call_mcp_tool("clientes", "obtener_cliente", {"cliente_id": cliente_id})
def resumen_cliente(cliente_id: str) -> Dict[str, Any]:
    return call_mcp_tool("clientes", "resumen_cliente", {"cliente_id": cliente_id})
def clientes_frecuentes(limite: int = 10) -> Dict[str, Any]:
    return call_mcp_tool("clientes", "clientes_frecuentes", {"limite": limite})

def listar_productos(categoria: Optional[str] = None, estado: Optional[str] = "Activo", limite: int = 20) -> Dict[str, Any]:
    return call_mcp_tool("productos", "listar_productos", {"categoria": categoria, "estado": estado, "limite": limite}) 
def buscar_producto(nombre: Optional[str] = None, categoria: Optional[str] = None, talle: Optional[str] = None, color: Optional[str] = None, estado: Optional[str] = "Activo", limite: int = 10) -> Dict[str, Any]:
    return call_mcp_tool("productos", "buscar_producto", {"nombre": nombre, "categoria": categoria, "talle": talle, "color": color, "estado": estado, "limite": limite})
def obtener_producto(producto_id: str) -> Dict[str, Any]:
    return call_mcp_tool("productos", "obtener_producto", {"producto_id": producto_id})
def consultar_stock(producto_id: str) -> Dict[str, Any]:
    return call_mcp_tool("productos", "consultar_stock", {"producto_id": producto_id})
def productos_bajo_stock(limite: int = 10) -> Dict[str, Any]:
    return call_mcp_tool("productos", "productos_bajo_stock", {"limite": limite})
def listar_categorias() -> Dict[str, Any]:
    return call_mcp_tool("productos", "listar_categorias")
def productos_por_categoria(categoria: str, limite: int = 20) -> Dict[str, Any]:
    return call_mcp_tool("productos", "productos_por_categoria", {"categoria": categoria, "limite": limite})

def obtener_venta(venta_id: str) -> Dict[str, Any]:
    return call_mcp_tool("ventas", "obtener_venta", {"venta_id": venta_id})
def listar_ventas(fecha_desde: str, fecha_hasta: str, estado_venta: Optional[str] = None, limite: int = 20) -> Dict[str, Any]:
    return call_mcp_tool("ventas", "listar_ventas", {"fecha_desde": fecha_desde, "fecha_hasta": fecha_hasta, "estado_venta": estado_venta, "limite": limite})
def listar_ventas_cliente(cliente_id: str, fecha_desde: str, fecha_hasta: str, limite: int = 20) -> Dict[str, Any]:
    return call_mcp_tool("ventas", "listar_ventas_cliente", {"cliente_id": cliente_id, "fecha_desde": fecha_desde, "fecha_hasta": fecha_hasta, "limite": limite})
def resumen_ventas_por_periodo(fecha_desde: str, fecha_hasta: str) -> Dict[str, Any]:
    return call_mcp_tool("ventas","resumen_ventas_por_periodo",{"fecha_desde": fecha_desde, "fecha_hasta": fecha_hasta, "excluir_canceladas": True})
def ticket_promedio(fecha_desde: str, fecha_hasta: str, excluir_canceladas: bool = True)-> Dict[str, Any]:
    return call_mcp_tool("ventas","ticket_promedio",{"fecha_desde": fecha_desde, "fecha_hasta": fecha_hasta, "excluir_canceladas": excluir_canceladas})
def productos_mas_vendidos(fecha_desde: str, fecha_hasta: str, limite: int = 10) -> Dict[str, Any]:
    return call_mcp_tool("ventas","productos_mas_vendidos",{"fecha_desde": fecha_desde, "fecha_hasta": fecha_hasta, "limite": limite})
def ventas_por_cliente(fecha_desde: str, fecha_hasta: str, limite: int = 10) -> Dict[str, Any]:
    return call_mcp_tool("ventas","ventas_por_cliente",{"fecha_desde": fecha_desde, "fecha_hasta": fecha_hasta, "limite": limite, "ordenar_por": "total"})
def validar_venta_simulada(cliente_id: str, items: List[Dict[str, Any]]) -> Dict[str, Any]:
    return call_mcp_tool("ventas", "validar_venta_simulada", {"cliente_id": cliente_id, "items": items})
 