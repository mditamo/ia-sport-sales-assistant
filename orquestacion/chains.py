import os


def build_chat_model():
    """
    Devuelve un chat model listo para usar.
    Preferimos ChatOpenAI por el requerimiento del módulo.
    """
    try:
        try:
              from langchain_openai import ChatOpenAI
        except Exception as exc:
              raise RuntimeError("Falta langchain-openai.") from exc
         
        openai_api_base = os.getenv("OPENAI_API_BASE", "http://127.0.0.1:1234/v1")
        openai_api_key = os.getenv("OPENAI_API_KEY", "lm-studio")
        openai_model= os.getenv("OPENAI_MODEL", "qwen2.5-7b-instruct")

        llm_timeout_seconds = int(os.getenv("LLM_TIMEOUT_SECONDS", "180"))
        llm_max_retries = int(os.getenv("LLM_MAX_RETRIES", "2"))

        return ChatOpenAI(
                model=openai_model,
                base_url=openai_api_base,
                api_key=openai_api_key,
                timeout=llm_timeout_seconds,
                max_retries=llm_max_retries,
                temperature=0.2,
            )

    except Exception as exc:  # pragma: no cover
        #logger.warning("No se pudo inicializar ChatOpenAI: %s", exc)
        return _fallback_chat_model()


def _fallback_chat_model():
    """
    Modelo de respaldo offline.
    Sirve para mantener la demo funcionando aun sin acceso externo.
    """
    try:
        from langchain_core.language_models.fake import FakeListChatModel
    except Exception as exc:  # pragma: no cover
        raise RuntimeError("No se pudo cargar un modelo de fallback.") from exc

    responses = [
        "Respuesta de respaldo: el sistema está listo, pero el modelo ChatOpenAI no pudo inicializarse.",
        "Respuesta de respaldo: consulta registrada.",
        "Respuesta de respaldo: herramienta ejecutada.",
    ]
    return FakeListChatModel(responses=responses)

