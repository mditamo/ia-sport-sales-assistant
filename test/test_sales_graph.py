from __future__ import annotations

import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from agente.graph import run_sales_assistant


QUESTIONS = [
    # Solo RAG
    "¿Cómo creo una venta?",
    "¿Qué significa stock reservado?",
    "¿Cuál es la diferencia entre cambio y devolución?",

    # Solo MCP
    "Buscar cliente CLI010",
    "Consultar stock PROD001",
    "Productos más vendidos de 2025",

    # RAG + MCP
    "Consultar stock PROD001 y explicame qué significa stock reservado",
    "Necesito devolver un producto de la venta VTA0001. ¿Se puede?",
    "Validar venta para CLI010 con PROD001 x2 y cual es el total estimado",
]


def test_sales_graph() -> None:
    for question in QUESTIONS:
        print("\n" + "=" * 100)
        print("Pregunta:")
        print(question)

        result = run_sales_assistant(question)

        print("\nIntent:")
        print(result.get("intent"))

        print("\nNeeds RAG:")
        print(result.get("needs_rag"))

        print("\nNeeds MCP:")
        print(result.get("needs_mcp"))

        print("\nMCP Domain:")
        print(result.get("mcp_domain"))

        print("\nRAG OK:")
        rag = result.get("rag")
        print(rag.get("ok") if rag else None)

        print("\nMCP OK:")
        mcp = result.get("mcp")
        print(mcp.get("ok") if isinstance(mcp, dict) and "ok" in mcp else None)

        print("\nRespuesta:")
        print(result.get("answer"))

        if result.get("needs_rag"):
            assert result.get("rag") is not None, "La consulta requería RAG pero no se ejecutó rag_node."

        if result.get("needs_mcp"):
            assert result.get("mcp") is not None, "La consulta requería MCP pero no se ejecutó MCP."

    print("\nTests finalizados correctamente.")


if __name__ == "__main__":
    test_sales_graph()
