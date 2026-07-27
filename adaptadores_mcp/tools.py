import csv
from pathlib import Path
import sqlite3
from typing import Any, Dict, List, Iterable, Optional
import pandas as pd
import logging
import os
import sys

# Conexión global a SQLite en memoria.
# Importante: si cerramos esta conexión, la base desaparece.
_CONN: Optional[sqlite3.Connection] = None


MCP_DATA_DIR = Path(os.getenv("MCP_DATA_DIR", "data/mcp")).resolve()    
CLIENTES_CSV = MCP_DATA_DIR / "clientes.csv"
VENTAS_CSV = MCP_DATA_DIR / "ventas.csv"
PRODUCTOS_CSV = MCP_DATA_DIR / "productos.csv"
VENTAS_PRODUCTOS_CSV = MCP_DATA_DIR / "ventas_productos.csv"

LOGS_DIR = Path(os.getenv("LOGS_DIR", "logs")).resolve()
LOGS_DIR.mkdir(parents=True, exist_ok=True)
LOG_FILE = LOGS_DIR / "mcp.log"


def _logger() -> logging.Logger:
    # Configurar logging para stderr para no interferir con stdio
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[
            logging.StreamHandler(sys.stderr),
            logging.FileHandler(LOG_FILE, encoding="utf-8")
        ]
    )
    return logging.getLogger("MCP")


logger = _logger()

# -------------------------------------------------------------------
# Datos de respaldo para que el módulo sea ejecutable aunque los CSV
# aún no existan en el equipo del alumno.
# -------------------------------------------------------------------
def _sample_productos() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "producto_id": "PROD001",
                "nombre": "Remera Dry-Fit",
                "categoria": "remeras",
                "marca": "Sportiva",
                "genero_linea": "Unisex",
                "talle": "S",
                "color": "Negro",
                "estado": "Activo",
                "precio_venta": 17800,
                "costo_estimado": 9400,
                "margen_bruto": 8400,
                "margen_porcentaje": 47.19,
                "stock_fisico": 36,
                "stock_reservado": 0,
                "stock_disponible": 36,
                "stock_minimo": 2,
                "alerta_stock": "Stock normal"
            }
        ]
    )


def _sample_clientes() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "cliente_id": "CLI001",
                "nombre": "Sofía",
                "apellido": "Ramírez",
                "documento": "28735650",
                "telefono": "11-1409-5506",
                "email": "sofia.ramirez@email.com",
                "ciudad": "CABA",
                "provincia": "Buenos Aires",
                "estado": "Activo",
                "fecha_alta": "2025-10-16",
                "observaciones": "Prefiere contacto por WhatsApp."
            }
        ]
    )


def _sample_ventas() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "venta_id":"VTA0265",
                "fecha": "2025-01-02", 
                "cliente_id": "CLI001", 
                "cliente_nombre": "Sofía Ramírez", 
                "estado_venta": "Despachada", 
                "estado_pago": "Pago parcial",
                "medio_pago": "Billetera virtual", 
                "canal_venta": "Web",
                "vendedor": "Diego",
                "subtotal_venta": 16800, 
                "descuento_venta": 0, 
                "total_venta": 16800, 
                "monto_pagado": 13000, 
                "saldo_pendiente": 3800,
                "observaciones": ""
            }
        ]
    )


def _sample_ventas_productos() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "venta_producto_id": "VPI00001",
                "venta_id": "VTA0001",
                "producto_id": "PROD001",
                "producto_nombre": "Remera Dry-Fit",
                "categoria": "remeras",
                "talle": "S",
                "color": "Negro",
                "cantidad": 1,
                "precio_unitario": 17800,
                "descuento_item": 1000,
                "subtotal_item": 17800,
                "total_item": 16800
            }
        ]
    )

# -------------------------------------------------------------------
# Utilidades de carga y normalización.
# -------------------------------------------------------------------
def _read_csv_with_fallback(path: Path, fallback_df: pd.DataFrame) -> pd.DataFrame:
    """
    Intenta leer un CSV con separador ';' como pide el enunciado.
    Si no existe o falla, devuelve datos simulados para mantener la demo viva.
    """
    try:
        if path.exists():
            df = pd.read_csv(path, sep=",")
            logger.info("CSV cargado correctamente: %s", path)
            return df
        logger.warning("CSV no encontrado en %s. Usando datos simulados.", path)
        return fallback_df.copy()
    except Exception as exc:
        logger.exception("Error leyendo %s. Se usarán datos simulados. %s", path,exc)
        return fallback_df.copy()


def _normalize_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Normaliza valores faltantes para que SQLite los reciba bien.
    """
    clean_df = df.copy()
    # Convertimos NaN/NaT a None para insertarlos de forma segura en SQLite.
    clean_df = clean_df.where(pd.notnull(clean_df), None)
    return clean_df


def _df_to_sqlite(conn: sqlite3.Connection, table_name: str, df: pd.DataFrame) -> None:
    """
    Vuelca un DataFrame a SQLite usando pandas.
    Se reemplaza la tabla completa para simplificar el flujo educativo.
    """
    normalized = _normalize_dataframe(df)
    normalized.to_sql(table_name, conn, if_exists="replace", index=False)
    
    
def _initialize_database() -> sqlite3.Connection:
    """
    Crea la base en memoria y carga las dos tablas pedidas.
    """
    conn = sqlite3.connect("db/sport_sales.sqlite3", check_same_thread=False)
    conn.row_factory = sqlite3.Row  # Facilita convertir resultados a dict.

    productos_df = _read_csv_with_fallback(PRODUCTOS_CSV, _sample_productos())
    clientes_df = _read_csv_with_fallback(CLIENTES_CSV, _sample_clientes())
    ventas_df = _read_csv_with_fallback(VENTAS_CSV, _sample_ventas())
    ventas_productos_df = _read_csv_with_fallback(VENTAS_PRODUCTOS_CSV, _sample_ventas_productos())

    _df_to_sqlite(conn, "productos", productos_df)
    _df_to_sqlite(conn, "clientes", clientes_df)
    _df_to_sqlite(conn, "ventas", ventas_df)
    _df_to_sqlite(conn, "ventas_productos", ventas_productos_df)

    logger.info("Base de datos SQLite en memoria inicializada con éxito.")
    return conn


def get_connection() -> sqlite3.Connection:
    """
    Devuelve la conexión global, inicializándola si todavía no existe.
    """
    global _CONN
    if _CONN is None:
        _CONN = _initialize_database()
    return _CONN

def _rows_to_dicts(rows: Iterable[sqlite3.Row]) -> List[Dict[str, Any]]:
    """
    Convierte filas SQLite a lista de diccionarios nativos de Python.
    """
    return [dict(row) for row in rows]

def _build_where_clause(conn: sqlite3.Connection, tabla: str, filtros: Dict[str, Any]) -> tuple[str, List[Any]]:
    """
    Construye un WHERE dinámico inspeccionando las columnas reales de la base de datos.
    Esto evita crasheos si el LLM envía 'Estado' pero la columna en el CSV se llama 'estado',
    y usa LIKE para mejorar la tolerancia en las búsquedas de texto.
    """
    if not filtros:
        return "", []

    # 1. Introspección: Obtenemos cómo se llaman realmente las columnas en la DB
    cursor = conn.execute(f"PRAGMA table_info({tabla})")
    columnas_reales = {row["name"].lower(): row["name"] for row in cursor.fetchall()}

    clauses: List[str] = []
    params: List[Any] = []

    for key, value in filtros.items():
        col_lower = key.lower()
        
        # 2. Solo aplicamos el filtro si la columna existe en la tabla real
        if col_lower in columnas_reales:
            col_exacta = columnas_reales[col_lower]
            
            # 3. Flexibilidad: Si es texto, usamos LIKE para tolerar nombres incompletos
            if isinstance(value, str):
                clauses.append(f"{col_exacta} LIKE ?")
                params.append(f"%{value}%")
            elif value is not None:
                clauses.append(f"{col_exacta} = ?")
                params.append(value)
        else:
            logger.warning(f"Filtro ignorado: El agente intentó usar una columna inexistente '{key}'.")

    if not clauses:
        return "", []

    return " WHERE " + " AND ".join(clauses), params



def _response(
    status_code: int,
    status: str,
    data: Any = None,
    message: str = "",
) -> Dict[str, Any]:
    """
    Envoltorio estándar de respuestas.
    Sirve para que el LLM y la UI sepan interpretar el resultado sin ambigüedad.
    """
    payload = {
        "status_code": status_code,
        "status": status,
        "message": message,
        "data": data,
    }
    return payload
