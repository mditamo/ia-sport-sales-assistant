from __future__ import annotations

import os
from langchain_huggingface import HuggingFaceEmbeddings

EMBEDDING_MODEL_NAME = os.getenv(
    "RAG_EMBEDDING_MODEL",
    "intfloat/multilingual-e5-base",
)

def get_embeddings() -> HuggingFaceEmbeddings:
    """
    Crea el modelo de embeddings.

    intfloat/multilingual-e5-base funciona bien para español y consultas semánticas.
    normalize_embeddings=True ayuda a mejorar búsquedas por similitud coseno.
    """
    return HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL_NAME,
        encode_kwargs={"normalize_embeddings": True},
    )
