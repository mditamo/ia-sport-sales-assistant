from __future__ import annotations

import os

def configure_langsmith():
    os.environ.setdefault("LANGCHAIN_TRACING_V2", "true")
    os.environ.setdefault("LANGCHAIN_PROJECT", "ai-sport-sales")