import asyncio
import os
import sys
from pathlib import Path

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

PROJECT_ROOT = Path(__file__).resolve().parents[1]

SERVER_PATH = PROJECT_ROOT / "adaptadores_mcp" / "clientes_server.py"
MCP_DATA_DIR =  Path(os.getenv("MCP_DATA_DIR", "data/mcp")).resolve()

async def run_mcp_clientes_checks():
    print("PROJECT_ROOT:", PROJECT_ROOT)
    print("SERVER_PATH:", SERVER_PATH)
    print("MCP_DATA_DIR:", MCP_DATA_DIR)

    if not SERVER_PATH.exists():
        raise FileNotFoundError(f"No existe el servidor: {SERVER_PATH}")

    if not MCP_DATA_DIR.exists():
        raise FileNotFoundError(f"No existe la carpeta data: {MCP_DATA_DIR}")

    server_params = StdioServerParameters(
        command=sys.executable,
        args=[str(SERVER_PATH)],
        env={
            "MCP_DATA_DIR": str(MCP_DATA_DIR),
        },
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            print("\nTools disponibles:")
            tools = await session.list_tools()

            for tool in tools.tools:
                print(f"- {tool.name}")

            print("\nProbando buscar_cliente...")
            result = await session.call_tool(
                "buscar_cliente",
                arguments={
                    "nombre": "Laura",
                    "limite": 5,
                }, 
            )
            print(result)
            
            
            print("\nProbando obtener_cliente...")
            result = await session.call_tool(
                "obtener_cliente",
                arguments={
                    "cliente_id": "CLI010",
                },
            )
            print(result)
            
            print("\nProbando clientes_frecuentes...")
            result = await session.call_tool(
                "clientes_frecuentes",
                arguments={
                    "limite": 10,
                },
            )
            print(result)            
            
            print("\nProbando resumen_cliente...")
            result = await session.call_tool(
                "resumen_cliente",
                arguments={
                    "cliente_id": "CLI006",
                },
            )
            print(result)
            

def test_mcp_clientes():
    asyncio.run(run_mcp_clientes_checks())


if __name__ == "__main__":
    test_mcp_clientes()
