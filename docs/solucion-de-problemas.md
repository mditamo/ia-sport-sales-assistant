# Solución de problemas

## `python` abre Microsoft Store o no se encuentra

Instalá Python 3.11 y desactivá los alias de ejecución de aplicaciones de Windows si interfieren. Después comprobá:

```powershell
python --version
Get-Command python
```

## PowerShell bloquea la activación

Aplicá una excepción solo para la terminal actual:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

También podés ejecutar sin activar:

```powershell
.\.venv\Scripts\python.exe -m pytest -v
```

## No existe la documentación funcional

Revisá:

```env
DOC_FUNCIONAL_DATA_DIR=data/doc_funcional
```

El directorio debe existir y contener archivos Markdown directamente dentro de él.

## Falla o demora la primera ingesta

El modelo `intfloat/multilingual-e5-base` puede descargarse durante la primera ejecución. Verificá acceso a internet, espacio en disco y permisos sobre `PERSIST_DIRECTORY`.

La ingesta elimina la base anterior antes de recrearla. Si se interrumpe, volvé a ejecutar:

```bash
python -m retrieval.ingest
```

## La API responde 500

Consultá la salida de Uvicorn o los logs de Docker:

```bash
docker compose logs -f api
```

Comprobá por separado:

```bash
python -m retrieval.ingest
python -m pytest test/test_mcp_clientes.py -v -s
python -m pytest test/test_api.py -v
```

## Docker no alcanza LM Studio

No uses `127.0.0.1` para acceder desde el contenedor al host. En Docker Desktop configurá:

```env
OPENAI_API_BASE=http://host.docker.internal:1234/v1
```

Confirmá además que LM Studio acepte conexiones y tenga cargado el modelo indicado por `OPENAI_MODEL`.

## No aparecen trazas en LangSmith

Revisá:

```env
LANGSMITH_TRACING=true
LANGSMITH_API_KEY=...
LANGSMITH_PROJECT=ai-sport-sales
```

Reiniciá la API después de cambiar `.env`, porque la configuración se carga al iniciar el proceso.

## Los logs o checkpoints no se generan

Verificá que las rutas configuradas sean escribibles:

```env
LOGS_DIR=logs
```

El código crea estos directorios automáticamente cuando importa los módulos de observabilidad.

