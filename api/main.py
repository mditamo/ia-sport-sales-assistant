from __future__ import annotations

from typing import Any
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from dotenv import load_dotenv

load_dotenv()

from observabilidad.langsmith_config import configure_langsmith

configure_langsmith()

from agente.graph import run_sales_assistant

app = FastAPI(
    title="Sport Sales Assistant API",
    version="1.0.0",
    description="Asistente de ventas con RAG, LangGraph y herramientas MCP.",
)


class ChatRequest(BaseModel):
    question: str = Field(
        min_length=1,
        description="Consulta que debe procesar el asistente.",
        examples=["Consultar stock PROD001"],
    )


class ChatResponse(BaseModel):
    question: str
    intent: str | None = None
    needs_rag: bool | None = None
    needs_mcp: bool | None = None
    mcp_domain: str | None = None
    answer: str | None = None
    debug: Any = None


@app.get("/health", tags=["status"])
def health() -> dict[str, str]:
    """Confirma que el proceso HTTP está disponible."""
    return {"status": "ok"}


@app.post("/chat", response_model=ChatResponse, tags=["assistant"])
def chat(request: ChatRequest) -> ChatResponse:
    """Procesa una consulta mediante el grafo del asistente de ventas."""
    try:
        result = run_sales_assistant(request.question)
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail="No se pudo procesar la consulta.",
        ) from exc

    return ChatResponse(
        question=result.get("question", request.question),
        intent=result.get("intent"),
        needs_rag=result.get("needs_rag"),
        needs_mcp=result.get("needs_mcp"),
        mcp_domain=result.get("mcp_domain"),
        answer=result.get("answer"),
        debug=result.get("debug"),
    )
