from __future__ import annotations

from fastapi.testclient import TestClient

import api.main as api_main

client = TestClient(api_main.app)

def test_health() -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_chat(monkeypatch) -> None:
    def fake_run_sales_assistant(question: str) -> dict:
        return {
            "question": question,
            "intent": "mcp_productos",
            "needs_rag": False,
            "needs_mcp": True,
            "mcp_domain": "productos",
            "answer": "Stock disponible.",
            "debug": {"mocked": True},
        }

    monkeypatch.setattr(api_main, "run_sales_assistant", fake_run_sales_assistant)

    response = client.post(
        "/chat",
        json={"question": "Consultar stock PROD001"},
    )

    assert response.status_code == 200
    assert response.json() == {
        "question": "Consultar stock PROD001",
        "intent": "mcp_productos",
        "needs_rag": False,
        "needs_mcp": True,
        "mcp_domain": "productos",
        "answer": "Stock disponible.",
        "debug": {"mocked": True},
    }


def test_chat_rejects_empty_question() -> None:
    response = client.post("/chat", json={"question": ""})

    assert response.status_code == 422


def test_chat_handles_agent_error(monkeypatch) -> None:
    def failing_agent(_question: str) -> dict:
        raise RuntimeError("Falla simulada")

    monkeypatch.setattr(api_main, "run_sales_assistant", failing_agent)

    response = client.post("/chat", json={"question": "Consulta válida"})

    assert response.status_code == 500
    assert response.json() == {"detail": "No se pudo procesar la consulta."}
