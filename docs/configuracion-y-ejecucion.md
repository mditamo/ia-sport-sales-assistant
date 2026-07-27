# Configuración y ejecución

## Requisitos

- Python 3.11 recomendado, en línea con la imagen Docker del proyecto.
- `pip`.
- Acceso a internet durante la primera descarga del modelo de embeddings, salvo que ya esté en caché.
- Un servidor de chat compatible con la API de OpenAI.
- Docker y Docker Compose, únicamente para la ejecución contenerizada.

Todos los comandos deben ejecutarse desde la raíz del repositorio.

## Entorno virtual y dependencias

PowerShell:

```powershell
python -m venv .venv
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Linux o macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Para verificar el intérprete y Pytest:

```bash
python --version
python -m pytest --version
```

## Archivo `.env`

Creá el archivo local a partir de la plantilla versionada:

```powershell
Copy-Item .env.example .env
```

No subas `.env` al repositorio. El archivo está excluido mediante `.gitignore`.

### Variables del modelo de chat

| Variable | Uso | Ejemplo |
| --- | --- | --- |
| `OPENAI_API_BASE` | Endpoint compatible con OpenAI | `http://127.0.0.1:1234/v1` |
| `OPENAI_API_KEY` | Credencial del proveedor; LM Studio admite un valor local | `lm-studio` |
| `OPENAI_MODEL` | Modelo publicado por el endpoint | `qwen2.5-7b-instruct` |
| `LLM_TIMEOUT_SECONDS` | Tiempo máximo de una llamada | `180` |
| `LLM_MAX_RETRIES` | Reintentos del cliente | `2` |

Para OpenAI, usá el endpoint y un modelo disponibles en tu cuenta. Para LM Studio, cargá el modelo e iniciá el servidor local antes de consultar el asistente.

### Variables de RAG y datos

| Variable | Uso | Valor predeterminado |
| --- | --- | --- |
| `RAG_EMBEDDING_MODEL` | Modelo Hugging Face para embeddings | `intfloat/multilingual-e5-base` |
| `PERSIST_DIRECTORY` | Directorio persistente de ChromaDB | `chroma_db` |
| `DOC_FUNCIONAL_DATA_DIR` | Markdown utilizado por la ingesta | `data/doc_funcional` |
| `MCP_DATA_DIR` | CSV consultados por los servidores MCP | `data/mcp` |
| `LOGS_DIR` | Archivo de auditoría y Checkpoint JSON del último estado | `logs` |

Las rutas relativas se resuelven respecto del directorio desde el que se inicia el proceso. Por eso se recomienda ejecutar siempre desde la raíz.

### Variables de LangSmith

| Variable | Uso |
| --- | --- |
| `LANGSMITH_API_KEY` | Credencial de LangSmith |
| `LANGSMITH_TRACING` | Activa o desactiva trazas (`true`/`false`) |
| `LANGSMITH_PROJECT` | Proyecto que agrupa las trazas |
| `LANGSMITH_ENDPOINT` | Endpoint alternativo, opcional |
| `LANGSMITH_WORKSPACE_ID` | Workspace, si la clave requiere seleccionarlo |

Para ejecución sin LangSmith:

```env
LANGSMITH_TRACING=false
```

El proyecto admite como compatibilidad las variables históricas `LANGCHAIN_API_KEY`, `LANGCHAIN_TRACING_V2` y `LANGCHAIN_PROJECT`.

## Inicializar la base vectorial

La fuente de la ingesta son los archivos Markdown ubicados en `DOC_FUNCIONAL_DATA_DIR`.

```bash
python -m retrieval.ingest
```

El proceso:

1. Carga todos los archivos `*.md` del directorio funcional.
2. Divide su contenido en fragmentos de 900 caracteres, con 150 de solapamiento.
3. Genera embeddings con el modelo configurado.
4. Elimina la base Chroma anterior, si existe.
5. Crea la colección `sport_sales_functional_docs` en `PERSIST_DIRECTORY`.

La operación es destructiva para el directorio configurado. No apuntes `PERSIST_DIRECTORY` a una carpeta que contenga otros archivos.

Una salida correcta incluye mensajes similares a:

```text
Iniciando ingesta RAG...
Documentos cargados: 7
Chunks generados: ...
Vector store creado en: .../chroma_db
Colección: sport_sales_functional_docs
Ingestión completada.
```

También puede ejecutarse el archivo directamente:

```bash
python retrieval/ingest.py
```

Se recomienda la forma modular (`python -m retrieval.ingest`) porque conserva de manera más predecible las importaciones del paquete.

## Ejecutar la aplicación

API con recarga para desarrollo:

```bash
python -m uvicorn api.main:app --reload
```

API sin recarga:

```bash
python -m uvicorn api.main:app --host 0.0.0.0 --port 8000
```

Consola interactiva:

```bash
python cli.py
```

## Endpoints

### `GET /health`

Comprueba que el proceso HTTP responde:

```json
{"status": "ok"}
```

Este endpoint no verifica por sí solo el modelo, ChromaDB o los servidores MCP.

### `POST /chat`

Solicitud:

```json
{"question": "Consultar stock PROD001"}
```

Respuesta aproximada:

```json
{
  "question": "Consultar stock PROD001",
  "intent": "mcp_productos",
  "needs_rag": false,
  "needs_mcp": true,
  "mcp_domain": "productos",
  "answer": "...",
  "debug": {}
}
```

