from __future__ import annotations

from observabilidad.langsmith_config import configure_langsmith

configure_langsmith()

from agente.graph import run_sales_assistant

def main() -> None:
    """Ejecuta el asistente mediante una consola interactiva."""
    question = input("Ingrese una consulta: ").strip()

    if not question:
        print("Debe ingresar una consulta.")
        return

    result = run_sales_assistant(question)

    print("\nPregunta:")
    print(result.get("question"))

    print("\nIntención:")
    print(result.get("intent"))

    print("\nNeeds RAG:")
    print(result.get("needs_rag"))

    print("\nNeeds MCP:")
    print(result.get("needs_mcp"))

    print("\nMCP Domain:")
    print(result.get("mcp_domain"))

    print("\nRespuesta:")
    print(result.get("answer"))

    print("\nDebug:")
    print(result.get("debug"))


if __name__ == "__main__":
    main()
