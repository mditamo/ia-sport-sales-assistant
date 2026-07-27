# Pruebas

## Preparación

Instalá las dependencias dentro del entorno virtual:

```bash
python -m pip install -r requirements.txt
python -m pytest --version
```

## Ejecutar todas las pruebas

```bash
python -m pytest -v
```

Para mostrar las salidas generadas por las verificaciones integrales:

```bash
python -m pytest -v -s
```

## Pruebas rápidas de la API

```bash
python -m pytest test/test_api.py -v
```

Estas pruebas sustituyen el grafo por una implementación simulada y cubren:

- respuesta de `/health`;
- respuesta correcta de `/chat`;
- rechazo de una pregunta vacía;
- conversión de errores internos a HTTP 500.

No requieren una base vectorial inicializada ni un modelo de chat activo.

## Pruebas integrales

### RAG

```bash
python -m pytest test/test_rag_retriever.py -v -s
```

Carga el modelo de embeddings y consulta ChromaDB. Si la colección está vacía, el código intenta ejecutar la ingesta automáticamente. Para un resultado predecible, ejecutá antes:

```bash
python -m retrieval.ingest
```

### Servidores MCP

```bash
python -m pytest test/test_mcp_clientes.py -v -s
python -m pytest test/test_mcp_productos.py -v -s
python -m pytest test/test_mcp_ventas.py -v -s
```

Cada prueba inicia el servidor MCP correspondiente como subproceso y consulta los CSV de `MCP_DATA_DIR`.

### Grafo completo

```bash
python -m pytest test/test_sales_graph.py -v -s
```

Recorre consultas de tipo RAG, MCP y mixtas. Requiere:

- documentos funcionales disponibles;
- ChromaDB o posibilidad de reconstruirlo;
- CSV MCP;
- endpoint del modelo accesible, salvo que se active el modelo de respaldo por un error de inicialización.

## Ejecutar un archivo como script

Los archivos conservan una entrada directa. Por ejemplo:

```bash
python test/test_rag_retriever.py
python test/test_sales_graph.py
```

La forma recomendada para automatización es `python -m pytest`.

## Alcance actual

Las verificaciones integrales comprueban principalmente que el flujo se complete y produzca resultados. Todavía no aíslan todas las dependencias ni validan exhaustivamente el contenido semántico de cada respuesta.

