from __future__ import annotations

from email import message
import re
from typing import Any, Dict, List, Optional, Literal
from agente.state import SalesAssistantState

from langchain_core.prompts import ChatPromptTemplate

from orquestacion.chains import build_chat_model
from orquestacion.prompts import SYSTEM_PROMPT

from orquestacion.tools import (
    rag_retrieve_context,
    obtener_cliente,
    resumen_cliente, 
    clientes_frecuentes,
    listar_productos,
    obtener_producto,
    consultar_stock,
    productos_bajo_stock,
    listar_categorias,
    obtener_venta,
    listar_ventas_cliente,
    resumen_ventas_por_periodo,
    ticket_promedio,
    productos_mas_vendidos,
    ventas_por_cliente,
    
    validar_venta_simulada,
)
from observabilidad.persistence import save_state
from observabilidad.audit import log_transition


McpDomain = Literal["clientes", "productos", "ventas", "validar_venta", "none"]

def normalize(text: str) -> str:
    return text.lower().strip()


def extract_cliente_id(text: str) -> Optional[str]:
    match = re.search(r"\bCLI\d{3}\b", text, re.IGNORECASE)
    return match.group(0).upper() if match else None


def extract_venta_id(text: str) -> Optional[str]:
    match = re.search(r"\bVTA\d{4}\b", text, re.IGNORECASE)
    return match.group(0).upper() if match else None


def extract_producto_id(text: str) -> Optional[str]:
    match = re.search(r"\bPROD\d{3}\b", text, re.IGNORECASE)
    return match.group(0).upper() if match else None


def extract_product_items(text: str) -> List[Dict[str, Any]]:
    """
    Extrae productos con cantidades desde texto.

    Soporta:
    - PROD001 x2
    - 2 PROD001
    - PROD001
    """
    items: List[Dict[str, Any]] = []

    for match in re.finditer(r"\b(PROD\d{3})\b\s*x\s*(\d+)", text, re.IGNORECASE):
        items.append(
            {
                "producto_id": match.group(1).upper(),
                "cantidad": int(match.group(2)),
            }
        )

    for match in re.finditer(r"\b(\d+)\s+(PROD\d{3})\b", text, re.IGNORECASE):
        candidate = {
            "producto_id": match.group(2).upper(),
            "cantidad": int(match.group(1)),
        }
        if candidate not in items:
            items.append(candidate)

    for match in re.finditer(r"\b(PROD\d{3})\b", text, re.IGNORECASE):
        product_id = match.group(1).upper()

        if not any(item["producto_id"] == product_id for item in items):
            items.append(
                {
                    "producto_id": product_id,
                    "cantidad": 1,
                }
            )

    return items


def extract_year_range(text: str) -> Dict[str, str]:
    """
    El dataset simulado trabaja con año calendario 2025.
    Si el usuario no indica año, usamos 2025.
    """
    match = re.search(r"\b(20\d{2})\b", text)
    year = match.group(1) if match else "2025"

    return {
        "fecha_desde": f"{year}-01-01",
        "fecha_hasta": f"{year}-12-31",
    }


def analyze_question(question: str) -> Dict[str, Any]:
    """
    Analiza la consulta y decide:
    - si necesita RAG;
    - si necesita MCP;
    - qué dominio MCP usar.

    Esta función reemplaza al clasificador rígido.
    """
    q = normalize(question)

    functional_keywords = [
        "cómo",
        "como",
        "qué significa",
        "que significa",
        "que",
        "qué",
        "cuándo",
        "cuando",
        "por qué",
        "porque",
        "diferencia",
        "política",
        "politica",
        "regla",
        "funciona",
        "manual",
        "devolución",
        "devolucion",
        "cambio",
        "estado",
        "stock reservado",
        "stock disponible",
        "stock físico",
        "stock fisico",
        "venta confirmada",
        "venta pendiente",
        "venta entregada",
        "cliente frecuente",
        "variante",
        "cual",
        "cuál",
        "cuales"
        "cuáles",
    ]

    client_keywords = [
        "cliente",
        "clientes",
        "buscar cliente",
        "obtener cliente",
        "resumen cliente",
        "clientes frecuentes",
    ]

    product_keywords = [
        "categorias de productos"
        "categorías de productos",
        "productos de categoria",
        "productos de categoría"
        "producto",
        "productos",
        "stock",
        "bajo stock",
        "sin stock",
        "remera",
        "zapatilla",
        "calza",
        "campera",
        "talle",
        "color",
    ]

    sales_keywords = [
        "ventas",
        "venta",
        "resumen ventas por periodo",
        "ventas del periodo",
        "ventas por cliente",
        "ventas del cliente",
        "ticket promedio",
        "más vendidos",
        "mas vendidos",
        "total vendido",
        "reporte",
        "vta",
        "facturación",
        "facturacion",
    ]

    sale_validation_keywords = [
        "validar venta",
        "crear venta",
        "nueva venta",
        "vender",
        "vendé",
        "vende",
        "venta para",
    ]

    has_functional = any(kw in q for kw in functional_keywords)

    has_cliente_id = extract_cliente_id(question) is not None
    has_producto_id = extract_producto_id(question) is not None
    has_venta_id = extract_venta_id(question) is not None

    is_sale_validation = any(kw in q for kw in sale_validation_keywords)

    mentions_client = any(kw in q for kw in client_keywords) or has_cliente_id
    mentions_product = any(kw in q for kw in product_keywords) or has_producto_id
    mentions_sales = any(kw in q for kw in sales_keywords) or has_venta_id

    # Reglas de RAG:
    # 1. Si pregunta cómo funciona algo, usa RAG.
    # 2. Si habla de devolución, cambio, estados o stock conceptual, usa RAG.
    # 3. Si pide validar/crear venta, conviene traer reglas funcionales también.
    needs_rag = has_functional or is_sale_validation

    # Reglas de MCP:
    # Si hay IDs reales o pide búsqueda/reporte/stock, usa MCP.
    needs_mcp = (
        has_cliente_id
        or has_producto_id
        or has_venta_id
        or mentions_client
        or mentions_product
        or mentions_sales
        or is_sale_validation
    )

    mcp_domain: McpDomain = "none"

    if is_sale_validation:
        mcp_domain = "validar_venta"
    elif has_venta_id or mentions_sales:
        mcp_domain = "ventas"
    elif has_producto_id or mentions_product:
        mcp_domain = "productos"
    elif has_cliente_id or mentions_client:
        mcp_domain = "clientes"

    if needs_rag and needs_mcp:
        intent = "mixed"
    elif needs_rag:
        intent = "functional"
    elif needs_mcp:
        intent = f"mcp_{mcp_domain}"
    else:
        intent = "unknown"

    return {
        "intent": intent,
        "needs_rag": needs_rag,
        "needs_mcp": needs_mcp,
        "mcp_domain": mcp_domain,
        "signals": {
            "has_functional": has_functional,
            "is_sale_validation": is_sale_validation,
            "has_cliente_id": has_cliente_id,
            "has_producto_id": has_producto_id,
            "has_venta_id": has_venta_id,
            "mentions_client": mentions_client,
            "mentions_product": mentions_product,
            "mentions_sales": mentions_sales,
        },
    }


def analyze_node(state: SalesAssistantState) -> SalesAssistantState:
    log_transition("ANALIZANDO CONSULTA")
    analysis = analyze_question(state["question"])

    return {
        **state,
        "intent": analysis["intent"],
        "needs_rag": analysis["needs_rag"],
        "needs_mcp": analysis["needs_mcp"],
        "mcp_domain": analysis["mcp_domain"],
        "errors": state.get("errors", []),
        "debug": {
            **state.get("debug", {}),
            "analysis": analysis,
        },
    }


def route_to_rag_or_mcp(state: SalesAssistantState) -> str:
    log_transition("DETERMINANDO SI ES RAG O MCP")
    """
    Primer routing:
    - si necesita RAG, va a RAG;
    - si no necesita RAG pero necesita MCP, salta a MCP;
    - si no necesita nada, unknown.
    """
    if state.get("needs_rag"):
        return "rag"

    if state.get("needs_mcp"):
        return "mcp_router"

    return "unknown"


def route_after_rag(state: SalesAssistantState) -> str:
    log_transition("DETERMINANDO SI DESPUES DEL RAG HAY QUE IR A MCP O COMPOSE_ANSWER")
    """
    Después de RAG:
    - si también necesita MCP, sigue hacia MCP;
    - si no, compone respuesta.
    """
    if state.get("needs_mcp"):
        return "mcp_router"

    return "compose_answer"


def route_mcp_domain(state: SalesAssistantState) -> str:
    log_transition("DETERMINANDO DOMINIO MCP")
    return state.get("mcp_domain", "none")


def rag_node(state: SalesAssistantState) -> SalesAssistantState:
    log_transition("EJECUTANDO RAG")
        
    question = state["question"]
    rag_result = rag_retrieve_context(question)
    state["rag"] = rag_result
    state["debug"] = {
        **state.get("debug", {}),
        "rag_called": True,
        "rag_ok": rag_result.get("ok"),
    }

    save_state(state)
    return state


def mcp_router_node(state: SalesAssistantState) -> SalesAssistantState:
    log_transition("EJECUTANDO MCP ROUTER")
    return state


def client_mcp_node(state: SalesAssistantState) -> SalesAssistantState:
    log_transition("EJECUTANDO MCP - CLIENTE")
    question = state["question"]
    q = normalize(question)
    
    cliente_id = extract_cliente_id(question)
    
    if "resumen" in q and cliente_id is not None:
        result = resumen_cliente(cliente_id)
    elif "clientes frecuentes" in q and cliente_id is None:        
        result = clientes_frecuentes(limite=10)
    elif cliente_id is not None:
        result = obtener_cliente(cliente_id)
    else:
        result = {
            "status_code": 400,
            "status": "bad_request",
            "message": "No se encontraron coincidencias para los filtros indicados.",
            "data": [],
        }
    state["mcp"] = result
    save_state(state)
    return state


def product_mcp_node(state: SalesAssistantState) -> SalesAssistantState:
    log_transition("EJECUTANDO MCP - PRODUCTO")
    
    question = state["question"]
    q = normalize(question)

    producto_id = extract_producto_id(question)

    if ("categorias" in q) and producto_id is None:
        result = listar_categorias()
    elif ("productos de categoria" in q) and producto_id is None:
        categoria = (
            question.replace("productos de categoria", "")
                .strip()
        )
        result = listar_productos(categoria)
    elif ("bajo stock" in q or "sin stock" in q) and producto_id is None:
        result = productos_bajo_stock(limite=10)        
    elif "stock" in q and producto_id is not None:
        result = consultar_stock(producto_id)
    elif producto_id is not None:
        result = obtener_producto(producto_id)
    else:
        result = {
            "status_code": 400,
            "status": "bad_request",
            "message": "No se encontraron coincidencias para los filtros indicados.",
            "data": [],
        }
    
    state["mcp"] = result
    save_state(state)
    return state


def sales_mcp_node(state: SalesAssistantState) -> SalesAssistantState:
    log_transition("EJECUTANDO MCP - VENTA")
    question = state["question"]
    q = normalize(question)

    venta_id = extract_venta_id(question)
    if venta_id is not None:
        result = obtener_venta(venta_id)
    elif "ticket promedio" in q:
        dates = extract_year_range(question)
        result = ticket_promedio(
            fecha_desde=dates["fecha_desde"],
            fecha_hasta=dates["fecha_hasta"],
            excluir_canceladas=True,
        )
    elif "más vendidos" in q or "mas vendidos" in q:
        dates = extract_year_range(question)
        result = productos_mas_vendidos(
            fecha_desde=dates["fecha_desde"],
            fecha_hasta=dates["fecha_hasta"],
            limite=10,
        )
    elif "resumen ventas por periodo" in q or "resumen ventas del periodo" in q:
        dates = extract_year_range(question)
        result = resumen_ventas_por_periodo(
            fecha_desde=dates["fecha_desde"],
            fecha_hasta=dates["fecha_hasta"],
            excluir_canceladas=True,
        )
    elif "ventas del cliente" in q:
        cliente_id = extract_cliente_id(question)
        if cliente_id is not None:
            dates = extract_year_range(question)
            result = listar_ventas_cliente(
                cliente_id=cliente_id,
                fecha_desde=dates["fecha_desde"],
                fecha_hasta=dates["fecha_hasta"],
                limite=10,
            )
    elif "ventas por cliente" in q:
        dates = extract_year_range(question)
        result = ventas_por_cliente(
            fecha_desde=dates["fecha_desde"],
            fecha_hasta=dates["fecha_hasta"],
        )
    else:
        result = {
            "status_code": 400,
            "status": "bad_request",
            "message": "No se encontraron coincidencias para los filtros indicados.",
            "data": [],
        }
        
    state["mcp"] = result
    save_state(state)
    return state


def sale_validation_node(state: SalesAssistantState) -> SalesAssistantState:
    log_transition("EJECUTANDO VALIDACIÓN DE VENTA")
    question = state["question"]

    cliente_id = extract_cliente_id(question)
    items = extract_product_items(question)

    errors = list(state.get("errors", []))

    if not cliente_id:
        errors.append("Para validar una venta necesito el cliente_id. Ejemplo: CLI010.")

    if not items:
        errors.append("Para validar una venta necesito productos. Ejemplo: PROD001 x2 y PROD010 x1.")

    if errors:
        log_transition("ERRORES EN VALIDACIÓN DE VENTA")
        state["mcp"] = None
        state["errors"] = errors
        save_state(state)
        return state

    result = validar_venta_simulada(cliente_id=cliente_id, items=items)

    state["mcp"] = result
    save_state(state)
    return state


def unknown_node(state: SalesAssistantState) -> SalesAssistantState:
    log_transition("CONSULTA DESCONOCIDA")
    state["answer"] = (
        "No pude determinar qué herramienta usar. Probá con una consulta más específica, "
        "por ejemplo: '¿Cómo creo una venta?', 'Buscar cliente Laura', "
        "'Consultar stock PROD001', 'Productos más vendidos de 2025' o "
        "'Validar venta para CLI010 con PROD001 x2'."
    )
    save_state(state)
    return state
    

def compose_answer_node(state: SalesAssistantState) -> SalesAssistantState:
    log_transition("COMPONIENDO RESPUESTA FINAL")
    rag = state.get("rag")
    mcp = state.get("mcp")
    errors = state.get("errors", [])
    needs_rag = state.get("needs_rag", False)
    needs_mcp = state.get("needs_mcp", False)

    if errors:
        return {
            **state,
            "answer": "No pude completar la operación:\n- " + "\n- ".join(errors),
        }

    parts: List[str] = []

    if needs_rag:
        if rag and rag.get("ok"):
            sources = ", ".join(rag.get("sources", [])) or "sin fuentes detectadas"
            parts.append(
                "Respuesta funcional basada en RAG:\n"
                #f"{rag.get('answer')}\n\n"
                f"Documentos consultados: {sources}."
            )
        else:
            parts.append(
                "Intenté consultar el RAG, pero falló.\n"
                f"Error: {rag.get('error') if rag else 'sin detalle'}"
            )

    if needs_mcp:
        if mcp and mcp.get("ok"):
            parts.append(
                "Datos operativos consultados con MCP:\n"
                f"Servidor: {mcp.get('server')}\n"
                f"Tool: {mcp.get('tool')}\n"
                f"Resultado:\n{mcp.get('raw_text')}"
            )
        else:
            parts.append(
                "Intenté consultar MCP, pero falló.\n"
                f"Error: {mcp.get('error') if mcp else 'sin detalle'}"
            )

    if not parts:
        parts.append("No se generó respuesta porque no se detectó RAG ni MCP.")

    state["answer"] =_invoke_agent(
        question=state["question"],
        context="\n\n---\n\n".join(parts),
    )
    save_state(state)
    return state


def _invoke_agent(
    *,
    question: str,
    context: str,
)-> str:

    model = build_chat_model()

    prompt = ChatPromptTemplate.from_messages(
                [
                    ("system", SYSTEM_PROMPT),
                    (
                        "human",
                        """Pregunta del usuario:
    {question}

    Contexto recuperado:
    {context}

    Respondé de forma útil, ordenada y breve, pero sin perder precisión.""",
                    ),
                ]
            )

    messages = prompt.format_messages(
                question=question,
                context=context if context else "Sin contexto recuperado.",
            )

    # Primera pasada del modelo.
    response = model.invoke(messages)
    
    return response.content