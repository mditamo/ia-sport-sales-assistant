from __future__ import annotations


from typing import Any, Dict, List, Literal, Optional, TypedDict

McpDomain = Literal["clientes", "productos", "ventas", "validar_venta", "none"]

class SalesAssistantState(TypedDict, total=False):
    question: str

    # análisis de intención
    intent: str
    needs_rag: bool
    needs_mcp: bool
    mcp_domain: McpDomain

    # resultados
    rag: Optional[Dict[str, Any]]
    mcp: Optional[Dict[str, Any]]

    # respuesta
    answer: str

    # control
    errors: List[str]
    debug: Dict[str, Any]
