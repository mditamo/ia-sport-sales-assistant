import os
from typing import List
from pathlib import Path
from langchain_core.documents import Document
from langchain_chroma import Chroma
from retrieval.embeddings import get_embeddings

CHROMA_DIR = Path(
    os.getenv("PERSIST_DIRECTORY", "chroma_db")
).resolve()

COLLECTION_NAME = "sport_sales_functional_docs"

def create_vectorstore(chunks: List[Document]) -> Chroma:
    """
    Crea o reemplaza el vector store local en chroma_db/.
    """
    embeddings = get_embeddings()

    # Si ya existe una base anterior, Chroma agregaría documentos.
    # Para una ingesta limpia, eliminamos la carpeta antes de recrearla.
    if CHROMA_DIR.exists():
        import shutil

        shutil.rmtree(CHROMA_DIR)

    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        collection_name=COLLECTION_NAME,
        persist_directory=str(CHROMA_DIR),
    )

    return vectorstore


