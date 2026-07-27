
from __future__ import annotations

from typing import List

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

def split_documents(documents: List[Document]) -> List[Document]:
    """
    Divide los documentos en chunks.

    Para documentación funcional en Markdown conviene usar chunks medianos:
    - suficientemente grandes para conservar contexto;
    - suficientemente chicos para recuperar secciones específicas.
    """
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=900,
        chunk_overlap=150,
        separators=[
            "\n## ",
            "\n### ",
            "\n\n",
            "\n",
            ". ",
            " ",
            "",
        ],
    )

    chunks = splitter.split_documents(documents)

    for index, chunk in enumerate(chunks):
        chunk.metadata["chunk_id"] = index

    return chunks

