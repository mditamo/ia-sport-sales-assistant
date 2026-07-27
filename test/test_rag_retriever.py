import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))


def test_rag_retriever():
    from retrieval.retriever import retrieve_context, format_documents

    questions = [
        "¿Cuándo se descuenta el stock?",
        "¿Cómo registro una devolución?",
        "¿Qué es una variante de producto?",
        "¿Puedo eliminar un cliente con ventas?",
        "¿Qué significa venta confirmada?",
    ]

    for question in questions:
        print("\n" + "=" * 80)
        print("Pregunta:")
        print(question)

        docs = retrieve_context(question, top_k=4)

        print(f"\nChunks recuperados: {len(docs)}")
        print(format_documents(docs))

        if not docs:
            raise AssertionError("No se recuperaron documentos.")


if __name__ == "__main__":
    test_rag_retriever()
