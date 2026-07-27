from __future__ import annotations

import os
import sys
from pathlib import Path
from typing import List

from langchain_core.documents import Document
from langchain_community.document_loaders import TextLoader
from dotenv import load_dotenv

load_dotenv()

from retrieval.chunking import split_documents
from retrieval.vector_store import create_vectorstore

DOCS_DIR = Path(
    os.getenv("DOC_FUNCIONAL_DATA_DIR", "data/doc_funcional")
).resolve()

CHROMA_DIR = Path(
    os.getenv("PERSIST_DIRECTORY", "chroma_db")
).resolve()
COLLECTION_NAME = "sport_sales_functional_docs"

def load_markdown_documents(docs_dir: Path = DOCS_DIR) -> List[Document]:
    """
    Lee todos los archivos .md dentro de docs_dir.
    Agrega metadata útil para poder mostrar fuentes luego.
    """
    if not docs_dir.exists():
        raise FileNotFoundError(
            f"No existe la carpeta {docs_dir.resolve()}. "
            "Creá la carpeta data/doc_funcional y agregá los archivos .md funcionales."
        )

    markdown_files = sorted(docs_dir.glob("*.md"))

    if not markdown_files:
        raise FileNotFoundError(
            f"No se encontraron archivos .md en {docs_dir.resolve()}."
        )

    documents: List[Document] = []

    for file_path in markdown_files:
        loader = TextLoader(str(file_path), encoding="utf-8")
        loaded_docs = loader.load()

        for doc in loaded_docs:
            doc.metadata.update(
                {
                    "source": str(file_path),
                    "file_name": file_path.name,
                    "document_type": "functional_documentation",
                }
            )
            documents.append(doc)

    return documents

def get_vector_store():
    print("Iniciando ingesta RAG...")

    documents = load_markdown_documents()
    print(f"Documentos cargados: {len(documents)}")

    chunks = split_documents(documents)
    print(f"Chunks generados: {len(chunks)}")

    vector_store = create_vectorstore(chunks)
    print(f"Vector store creado en: {CHROMA_DIR.resolve()}")
    print(f"Colección: {COLLECTION_NAME}")
    print("Ingesta finalizada correctamente.")
    return vector_store
    
def main():
    get_vector_store()
    print("Ingestión completada.")

if __name__ == "__main__":
    main()
