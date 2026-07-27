"""
rag/retriever.py

Carga el vector store persistente y expone un retriever reutilizable.

Uso rápido:
    python -m retrieval.retriever "¿Cuándo se descuenta el stock?"
"""

from __future__ import annotations

import os
import sys
from pathlib import Path
from typing import List

from langchain_core.documents import Document
from langchain_chroma import Chroma

from retrieval.embeddings import get_embeddings
from retrieval.ingest import get_vector_store
from ranking.reranker import rerank_documents

CHROMA_DIR = Path(
    os.getenv("PERSIST_DIRECTORY", "chroma_db")
).resolve()

COLLECTION_NAME = "sport_sales_functional_docs"

EMBEDDING_MODEL_NAME = os.getenv(
    "RAG_EMBEDDING_MODEL",
    "intfloat/multilingual-e5-base",
)

def retrieve_context(query: str, top_k: int = 3) -> list[Document]:
    """Recupera contexto relevante como texto consolidado.

    Parámetros
    ----------
    query:
        Consulta del usuario o del agente.
    top_k:
        Número de fragmentos finales a devolver después del reranking.

    Retorna
    -------
    list[Document]
        Lista de documentos recuperados.
    """
    clean_query = (query or "").strip()
    if not clean_query:
        return "Contexto recuperado: no se recibió una consulta válida."

    embeddings = get_embeddings()
      
    CHROMA_DIR.mkdir(parents=True, exist_ok=True)
      
    vector_store = Chroma(
        collection_name=COLLECTION_NAME,
        persist_directory=str(CHROMA_DIR),
        embedding_function=embeddings,
    )

    try:
        count = vector_store._collection.count()
    except Exception:
        count = 0

    if count == 0:
        vector_store = get_vector_store()

    # Recuperación inicial por similitud semántica.
    # Pedimos un poco más de resultados para que el reranking tenga material.
    candidate_k = max(top_k * 2, top_k)

    # La mayoría de los vector stores de LangChain soportan similarity_search.
    candidates = vector_store.similarity_search(clean_query, k=candidate_k)

    # Segunda capa: reranking didáctico.
    ranked = rerank_documents(clean_query, candidates)
    selected = ranked[:top_k]

    if not selected:
        return "Contexto recuperado: no se encontraron fragmentos relevantes."
     
    return [doc for doc, _score in selected[:top_k]]

def format_documents(docs: List[Document]) -> List[str]:
    """
    Formatea resultados para ver qué chunks recuperó el RAG.
    """
    lines = []

    for i, doc in enumerate(docs, start=1):
        source = doc.metadata.get("file_name") or doc.metadata.get("source", "sin_fuente")
        chunk_id = doc.metadata.get("chunk_id", "sin_chunk")
        preview = doc.page_content.replace("\n", " ").strip()

        lines.append(
            f"\n--- Resultado {i} ---\n"
            f"Fuente: {source}\n"
            f"Chunk: {chunk_id}\n"
            f"Contenido: {preview}..."
        )

    return lines


def main() -> None:
    query = " ".join(sys.argv[1:]).strip()

    if not query:
        query = "¿Cuándo se descuenta el stock de una venta?"

    docs = retrieve_context(query)
    print(format_documents(docs))


if __name__ == "__main__":
    main()
