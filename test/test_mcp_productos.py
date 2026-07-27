import asyncio
import os
import sys
from pathlib import Path

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


PROJECT_ROOT = Path(__file__).resolve().parents[1]

SERVER_PATH = PROJECT_ROOT / "adaptadores_mcp" / "productos_server.py"
MCP_DATA_DIR =  Path(os.getenv("MCP_DATA_DIR", "data/mcp")).resolve()


async def run_mcp_productos_checks():
    print("PROJECT_ROOT:", PROJECT_ROOT)
    print("SERVER_PATH:", SERVER_PATH)
    print("MCP_DATA_DIR:", MCP_DATA_DIR)

    if not SERVER_PATH.exists():
        raise FileNotFoundError(f"No existe el servidor: {SERVER_PATH}")

    if not MCP_DATA_DIR.exists():
        raise FileNotFoundError(f"No existe la carpeta data: {MCP_DATA_DIR}")

    env = os.environ.copy()
    env["MCP_DATA_DIR"] = str(MCP_DATA_DIR)

    server_params = StdioServerParameters(
        command=sys.executable,
        args=[str(SERVER_PATH)],
        env=env,
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            print("\nTools disponibles:")
            tools = await session.list_tools()

            for tool in tools.tools:
                print(f"- {tool.name}")

            print("\nProbando listar_categorias...")
            result = await session.call_tool(
                "listar_categorias",
                arguments={},
            )
            print(result)

            print("\nProbando listar_productos...")
            result = await session.call_tool(
                "listar_productos",
                arguments={
                    "estado": "Activo",
                    "limite": 5,
                },
            )
            print(result)

            print("\nProbando buscar_producto...")
            result = await session.call_tool(
                "buscar_producto",
                arguments={
                    "nombre": "remera",
                    "limite": 5,
                },
            ) 
            print(result)

            print("\nProbando buscar_producto con filtros...")
            result = await session.call_tool(
                "buscar_producto",
                arguments={
                    "nombre": "zapatilla",
                    "talle": "40",
                    "color": "Negro",
                    "limite": 5,
                },
            )
            print(result)

            print("\nProbando obtener_producto...")
            result = await session.call_tool(
                "obtener_producto",
                arguments={
                    "producto_id": "PROD001",
                },
            )
            print(result)

            print("\nProbando consultar_stock...")
            result = await session.call_tool(
                "consultar_stock",
                arguments={
                    "producto_id": "PROD001",
                },
            )
            print(result)
            '''
            print("\nProbando validar_stock...")
            result = await session.call_tool(
                "validar_stock",
                arguments={
                    "producto_id": "PROD001",
                    "cantidad": 2,
                },
            )
            print(result)
            '''
            print("\nProbando productos_bajo_stock...")
            result = await session.call_tool(
                "productos_bajo_stock",
                arguments={
                    "limite": 10,
                },
            )
            print(result)

            print("\nProbando productos_por_categoria...")
            result = await session.call_tool(
                "productos_por_categoria",
                arguments={
                    "categoria": "remeras",
                    "limite": 10,
                },
            )
            print(result)


def test_mcp_productos():
    asyncio.run(run_mcp_productos_checks())


if __name__ == "__main__":
    test_mcp_productos()
