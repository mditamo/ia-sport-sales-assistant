from __future__ import annotations

from agente.nodes import analyze_node, rag_node, mcp_router_node, client_mcp_node, product_mcp_node, sales_mcp_node, sale_validation_node, unknown_node, compose_answer_node, route_to_rag_or_mcp, route_after_rag, route_mcp_domain
from agente.state import SalesAssistantState
from langgraph.graph import END, START, StateGraph

def build_sales_graph():
    graph = StateGraph(SalesAssistantState)

    graph.add_node("analyze", analyze_node)
    graph.add_node("rag", rag_node)
    graph.add_node("mcp_router", mcp_router_node)
    graph.add_node("client_mcp", client_mcp_node)
    graph.add_node("product_mcp", product_mcp_node)
    graph.add_node("sales_mcp", sales_mcp_node)
    graph.add_node("sale_validation", sale_validation_node)
    graph.add_node("unknown", unknown_node)
    graph.add_node("compose_answer", compose_answer_node)

    graph.add_edge(START, "analyze")

    graph.add_conditional_edges(
        "analyze",
        route_to_rag_or_mcp,
        {
            "rag": "rag",
            "mcp_router": "mcp_router",
            "unknown": "unknown",
        },
    )

    graph.add_conditional_edges(
        "rag",
        route_after_rag,
        {
            "mcp_router": "mcp_router",
            "compose_answer": "compose_answer",
        },
    )

    graph.add_conditional_edges(
        "mcp_router",
        route_mcp_domain,
        {
            "clientes": "client_mcp",
            "productos": "product_mcp",
            "ventas": "sales_mcp",
            "validar_venta": "sale_validation",
            "none": "compose_answer",
        },
    )

    graph.add_edge("client_mcp", "compose_answer")
    graph.add_edge("product_mcp", "compose_answer")
    graph.add_edge("sales_mcp", "compose_answer")
    graph.add_edge("sale_validation", "compose_answer")
    graph.add_edge("compose_answer", END)
    graph.add_edge("unknown", END)

    return graph.compile()

def run_sales_assistant(question: str) -> SalesAssistantState:
    app = build_sales_graph()

    return app.invoke(
        {
            "question": question,
            "errors": [],
            "debug": {},
        }
    )