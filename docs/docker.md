# Ejecución con Docker

## Preparación

Docker Compose construye la imagen definida en `despliegue/docker/Dockerfile`, publica el puerto `8000` y carga las variables desde `.env`.

Creá y revisá el archivo antes de construir:

```powershell
Copy-Item .env.example .env
```

### Acceso al modelo desde el contenedor

Dentro de un contenedor, `127.0.0.1` identifica al propio contenedor. Si LM Studio se ejecuta sobre Windows o macOS, usá:

```env
OPENAI_API_BASE=http://host.docker.internal:1234/v1
```

Para un proveedor remoto, configurá su URL HTTPS y credencial correspondiente.

## Construir y levantar

```bash
docker compose up --build -d
```

Verificá el estado y los logs:

```bash
docker compose ps
docker compose logs -f api
```

## Inicializar Chroma dentro del contenedor

Con el servicio activo:

```bash
docker compose exec api python -m retrieval.ingest
```

La base se escribe dentro del sistema de archivos del contenedor. Sobrevive a un reinicio del mismo contenedor, pero puede perderse cuando Docker Compose lo recrea, por ejemplo tras otra construcción. La configuración actual no declara un volumen para `chroma_db`.

Para una demo también es posible ejecutar la ingesta local antes de construir. Como el contexto de Docker actual copia el repositorio completo, la base local puede incorporarse a la imagen; esta alternativa aumenta el tamaño de la imagen y no es recomendable para un despliegue productivo.

## Comprobar el servicio

PowerShell:

```powershell
Invoke-RestMethod http://localhost:8000/health
```

Bash:

```bash
curl http://localhost:8000/health
```

Consulta desde PowerShell:

```powershell
Invoke-RestMethod `
  -Method Post `
  -Uri http://localhost:8000/chat `
  -ContentType "application/json" `
  -Body '{"question":"¿Qué significa stock reservado?"}'
```

## Detener y reconstruir

```bash
docker compose down
docker compose up --build -d
```

Para borrar también volúmenes declarados en futuras versiones:

```bash
docker compose down --volumes
```

## Limitaciones del Compose actual

- No persiste `chroma_db` mediante un volumen.
- No incluye un healthcheck de Docker.
- No monta documentos o CSV desde el host; quedan incorporados durante la construcción.
- El Dockerfile copia todo el contexto y todavía no existe `.dockerignore`. Esto puede incorporar `.env`, logs y otros archivos locales a la imagen. No publiques la imagen actual en un registro: agregá `.dockerignore` y gestioná los secretos externamente antes de usarla fuera de una demostración.
