# Sport Sales Assistant

Asistente de ventas en Python que combina documentación funcional mediante RAG, datos operativos expuestos por servidores MCP y un flujo de decisión construido con LangGraph. El servicio HTTP está implementado con FastAPI.

## Funcionalidades

- Recuperación semántica sobre documentos Markdown con Hugging Face y ChromaDB.
- Consultas de clientes, productos, stock y ventas mediante herramientas MCP.
- Enrutamiento entre RAG y MCP con LangGraph.
- Generación de respuestas mediante una API compatible con OpenAI, como OpenAI o LM Studio.
- Trazas opcionales con LangSmith.
- API HTTP, cliente de consola y ejecución con Docker Compose.

## Inicio rápido

Requisitos: Python 3.11, `pip` y, para la ejecución contenerizada, Docker con Docker Compose.

### 1. Preparar el entorno

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

### 2. Configurar las variables

PowerShell:

```powershell
Copy-Item .env.example .env
```

Linux o macOS:

```bash
cp .env.example .env
```

Editá `.env` y configurá como mínimo el endpoint, la clave y el nombre del modelo. Si usás LM Studio localmente, su servidor compatible con OpenAI debe estar iniciado.

### 3. Inicializar ChromaDB

Desde la raíz del repositorio:

```bash
python -m retrieval.ingest
```

La primera ejecución puede descargar el modelo de embeddings. La ingesta lee `data/doc_funcional/*.md` y **reemplaza completamente** la base indicada por `PERSIST_DIRECTORY`.

### 4. Levantar la API local

```bash
python -m uvicorn api.main:app --reload
```

Abrí:

- API: `http://127.0.0.1:8000`
- Swagger: `http://127.0.0.1:8000/docs`
- Salud: `http://127.0.0.1:8000/health`

Consulta de ejemplo en PowerShell:

```powershell
Invoke-RestMethod `
  -Method Post `
  -Uri http://127.0.0.1:8000/chat `
  -ContentType "application/json" `
  -Body '{"question":"Consultar stock PROD001"}'
```

La interfaz de consola se ejecuta con:

```bash
python cli.py
```

### 5. Ejecutar con Docker

```bash
docker compose up --build -d
docker compose ps
```

Si la imagen no contiene una base inicializada, generala dentro del contenedor activo:

```bash
docker compose exec api python -m retrieval.ingest
```

Comprobá el servicio:

```bash
curl http://localhost:8000/health
```

Para detenerlo:

```bash
docker compose down
```

Si el modelo corre en LM Studio sobre la máquina anfitriona, configurá para Docker:

```env
OPENAI_API_BASE=http://host.docker.internal:1234/v1
```

### 6. Ejecutar las pruebas

Todas las pruebas:

```bash
python -m pytest -v
```

Solo las pruebas rápidas de la API:

```bash
python -m pytest test/test_api.py -v
```

Las demás pruebas son integrales y pueden usar ChromaDB, el modelo de embeddings, servidores MCP y el modelo de chat.

## Estructura principal

```text
sport_sales/
├── adaptadores_mcp/   # Servidores MCP para clientes, productos y ventas
├── agente/            # Estado, nodos y grafo LangGraph
├── api/               # Aplicación FastAPI
├── data/              # Documentación funcional y CSV operativos
├── despliegue/        # Docker, Kubernetes y ejemplo serverless
├── observabilidad/    # Auditoría, persistencia de estado y LangSmith
├── orquestacion/      # Modelo, prompts y clientes de herramientas
├── ranking/           # Reranking de resultados RAG
├── retrieval/         # Ingesta, embeddings, ChromaDB y recuperación
├── test/              # Pruebas unitarias e integrales
├── cli.py             # Interfaz interactiva de consola
└── docker-compose.yml # Servicio local contenerizado
```

## Documentación

- [Configuración y ejecución](docs/configuracion-y-ejecucion.md)
- [Arquitectura y estructura](docs/arquitectura.md)
- [Docker](docs/docker.md)
- [Pruebas](docs/pruebas.md)
- [Solución de problemas](docs/solucion-de-problemas.md)

