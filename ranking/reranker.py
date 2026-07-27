
from typing import List, Tuple
import re
from langchain_core.documents import Document

# -----------------------------------------------------------------------------
# 6) Reranking básico (educativo)
# -----------------------------------------------------------------------------
#
# El vector search recupera candidatos semánticamente relevantes, pero en una
# demo educativa conviene añadir una segunda capa muy simple de ranking para
# explicar por qué algunos fragmentos quedan arriba.
#
# Este reranking NO usa LLM. Solo mezcla:
# - orden inicial de recuperación,
# - solapamiento léxico con la query,
# - bonus por coincidencias de términos importantes.
# -----------------------------------------------------------------------------

def tokenize(text: str) -> List[str]:
    tokens = re.findall(r"[a-záéíóúñ0-9]+", text.lower())
    # Filtro mínimo de stopwords para que el score sea más útil en la demo.
    stopwords = {
        "de",
        "la",
        "el",
        "y",
        "o",
        "a",
        "en",
        "un",
        "una",
        "los",
        "las",
        "del",
        "por",
        "para",
        "con",
        "sin",
        "que",
        "se",
        "al",
        "lo",
        "su",
        "sus",
        "es",
        "son",
        "como",
        "más",
        "menos",
        "sobre",
        "cuando",
        "si",
        "no",
    }
    return [t for t in tokens if t not in stopwords and len(t) > 2]


def rerank_documents(query: str, docs: List[Document]) -> List[Tuple[Document, float]]:
    """Ordena documentos recuperados usando una heurística simple.

    El score final es una mezcla de:
    - score por solapamiento de tokens,
    - bonus por términos clave de la query,
    - bonus por aparecer antes en la recuperación inicial.
    """
    query_tokens = set(tokenize(query))
    ranked: List[Tuple[Document, float]] = []

    if not query_tokens:
        # Si la query está vacía o casi vacía, devolvemos el orden original.
        return [(doc, 1.0 / (idx + 1)) for idx, doc in enumerate(docs)]

    for idx, doc in enumerate(docs):
        text_tokens = set(tokenize(doc.page_content))
        overlap = len(query_tokens & text_tokens)
        coverage = overlap / max(len(query_tokens), 1)

        # Bonus pequeño por presencia de palabras del título/categoría.
        title = str(doc.metadata.get("source_title", "")) + " " + str(doc.metadata.get("category", ""))
        title_tokens = set(tokenize(title))
        title_bonus = 0.15 if query_tokens & title_tokens else 0.0

        # Bonus decreciente por el orden de recuperación inicial.
        position_bonus = 1.0 / (idx + 1)

        final_score = (coverage * 0.7) + title_bonus + (position_bonus * 0.05)
        ranked.append((doc, final_score))

    ranked.sort(key=lambda item: item[1], reverse=True)
    return ranked
