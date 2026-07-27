import asyncio
import os
import sys
from pathlib import Path

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


PROJECT_ROOT = Path(__file__).resolve().parents[1]

SERVER_PATH = PROJECT_ROOT / "adaptadores_mcp" / "ventas_server.py"
MCP_DATA_DIR =  Path(os.getenv("MCP_DATA_DIR", "data/mcp")).resolve()


async def run_mcp_ventas_checks():
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

            print("\nProbando obtener_venta...")
            result = await session.call_tool(
                "obtener_venta",
                arguments={
                    "venta_id": "VTA0001",
                },
            )
            print(result)

            print("\nProbando listar_ventas...")
            result = await session.call_tool(
                "listar_ventas",
                arguments={
                    "fecha_desde": "2025-01-01",
                    "fecha_hasta": "2025-12-31",
                    "limite": 5,
                },
            )
            print(result)

            print("\nProbando listar_ventas por estado...")
            result = await session.call_tool(
                "listar_ventas",
                arguments={
                    "fecha_desde": "2025-01-01",
                    "fecha_hasta": "2025-12-31",
                    "estado_venta": "Entregada",
                    "limite": 5,
                },
            )
            print(result)

            print("\nProbando listar_ventas_cliente...")
            result = await session.call_tool(
                "listar_ventas_cliente",
                arguments={
                    "cliente_id": "CLI010",
                    "fecha_desde": "2025-01-01",
                    "fecha_hasta": "2025-12-31",
                    "limite": 10,
                },
            )
            print(result)

            print("\nProbando resumen_ventas_por_periodo...")
            result = await session.call_tool(
                "resumen_ventas_por_periodo",
                arguments={
                    "fecha_desde": "2025-01-01",
                    "fecha_hasta": "2025-12-31",
                    "excluir_canceladas": True,
                },
            )
            print(result)

            print("\nProbando ticket_promedio...")
            result = await session.call_tool(
                "ticket_promedio",
                arguments={
                    "fecha_desde": "2025-01-01",
                    "fecha_hasta": "2025-12-31",
                    "excluir_canceladas": True,
                },
            )
            print(result)

            print("\nProbando productos_mas_vendidos por cantidad_vendida...")
            result = await session.call_tool(
                "productos_mas_vendidos",
                arguments={
                    "fecha_desde": "2025-01-01",
                    "fecha_hasta": "2025-12-31",
                    "limite": 10,
                    "ordenar_por": "cantidad_vendida",
                },
            )
            print(result)

            print("\nProbando productos_mas_vendidos por monto_vendido...")
            result = await session.call_tool(
                "productos_mas_vendidos",
                arguments={
                    "fecha_desde": "2025-01-01",
                    "fecha_hasta": "2025-12-31",
                    "limite": 10,
                    "ordenar_por": "monto_vendido",
                },
            )
            print(result)

            print("\nProbando ventas_por_cliente...")
            result = await session.call_tool(
                "ventas_por_cliente",
                arguments={
                    "fecha_desde": "2025-01-01",
                    "fecha_hasta": "2025-12-31",
                    "limite": 10,
                },
            )
            print(result)

            print("\nProbando validar_venta_simulada...")
            result = await session.call_tool(
                "validar_venta_simulada",
                arguments={
                    "cliente_id": "CLI010",
                    "items": [
                        {
                            "producto_id": "PROD001",
                            "cantidad": 2,
                        },
                        {
                            "producto_id": "PROD010",
                            "cantidad": 1,
                        },
                    ],
                },
            )
            print(result)


def test_mcp_ventas():
    asyncio.run(run_mcp_ventas_checks())


if __name__ == "__main__":
    test_mcp_ventas()
