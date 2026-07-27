# Arquitectura y estructura

## Flujo general

```text
Cliente HTTP o CLI
        │
        ▼
   LangGraph (agente)
        │
        ├── RAG ──► ChromaDB ──► reranking
        │
        ├── MCP ──► clientes / productos / ventas
        │
        ▼
 Modelo de chat compatible con OpenAI
        │
        ▼
 Respuesta + auditoría + checkpoint
```

El nodo de análisis inspecciona la consulta y decide si requiere documentación funcional, datos operativos o ambos. Después, el nodo de composición entrega el contexto recuperado al modelo de chat.

## Directorios

### `api/`

Contiene la aplicación FastAPI. `api/main.py` expone `app`, `GET /health` y `POST /chat`. Uvicorn, Docker y los ejemplos de despliegue importan este objeto.

### `agente/`

- `state.py`: contrato del estado compartido.
- `nodes.py`: análisis, routing, ejecución RAG/MCP y composición de respuesta.
- `graph.py`: construcción y ejecución del grafo LangGraph.

### `retrieval/`

- `ingest.py`: entrada para reconstruir la base vectorial.
- `chunking.py`: fragmentación de documentos.
- `embeddings.py`: modelo Hugging Face.
- `vector_store.py`: creación persistente de ChromaDB.
- `retriever.py`: búsqueda semántica y preparación de resultados.

### `ranking/`

Aplica un reranking heurístico basado en coincidencias léxicas y posición inicial. No utiliza otro LLM.

### `adaptadores_mcp/`

Implementa tres servidores MCP por entrada/salida estándar:

- clientes;
- productos y stock;
- ventas y validación simulada.

Los servidores consultan CSV dentro de `MCP_DATA_DIR`. No modifican esos archivos durante las consultas actuales.

### `orquestacion/`

- `chains.py`: construye el cliente `ChatOpenAI` contra el endpoint configurado.
- `prompts.py`: prompt del sistema.
- `tools.py`: cliente MCP y adaptador del retriever para el agente.

### `observabilidad/`

- `audit.py`: registra transiciones en `audit.log`.
- `persistence.py`: guarda el último estado en `checkpoint.json`.
- `langsmith_config.py`: carga `.env` y normaliza variables de LangSmith.

Los archivos locales representan auditoría y último estado; no constituyen un sistema de persistencia concurrente o distribuido.

### `data/`

- `doc_funcional/`: Markdown utilizado para RAG.
- `mcp/`: CSV operativos utilizados por MCP.

### `test/`

Contiene pruebas rápidas de FastAPI y verificaciones integrales de RAG, MCP y el grafo completo.

### `despliegue/`

Incluye un Dockerfile, manifiestos Kubernetes y un ejemplo serverless. Docker Compose es el mecanismo local directamente configurado y descrito en esta documentación.

## Datos generados

- `chroma_db/`: base vectorial local.
- `logs/audit.log`: transiciones ejecutadas.
- `logs/checkpoint.json`: último estado serializado.

Estas rutas están excluidas de Git mediante `.gitignore`.

