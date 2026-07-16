# agent/tools.py — Herramientas del agente
# Generado por AgentKit

"""
Herramientas que Claude puede usar durante la conversación (tool use).
Aquí se definen los esquemas que se envían a la API y el despachador
que ejecuta cada herramienta contra el motor de agenda.
"""

import os
import json
import logging

import yaml

from agent import agenda

logger = logging.getLogger("agentkit")

# Esquemas de herramientas para la API de Anthropic
HERRAMIENTAS = [
    {
        "name": "consultar_disponibilidad",
        "description": (
            "Consulta los horarios disponibles para agendar una cita en una fecha. "
            "Úsala SIEMPRE antes de proponer o confirmar un horario."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "fecha": {
                    "type": "string",
                    "description": "Fecha a consultar en formato YYYY-MM-DD",
                },
            },
            "required": ["fecha"],
        },
    },
    {
        "name": "agendar_cita",
        "description": (
            "Agenda una cita confirmada. Solo úsala cuando ya tengas nombre, "
            "fecha, hora y motivo, y la persona haya confirmado el horario."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "nombre": {"type": "string", "description": "Nombre de la persona"},
                "fecha": {"type": "string", "description": "Fecha en formato YYYY-MM-DD"},
                "hora": {"type": "string", "description": "Hora en formato HH:MM (24h)"},
                "motivo": {"type": "string", "description": "Motivo o asunto de la cita"},
            },
            "required": ["nombre", "fecha", "hora", "motivo"],
        },
    },
    {
        "name": "listar_citas",
        "description": "Lista las citas próximas que esta persona ya tiene agendadas.",
        "input_schema": {"type": "object", "properties": {}},
    },
    {
        "name": "cancelar_cita",
        "description": (
            "Cancela una cita existente por su ID. Usa listar_citas primero "
            "para identificar la cita correcta y confirma con la persona antes de cancelar."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "cita_id": {"type": "integer", "description": "ID de la cita a cancelar"},
            },
            "required": ["cita_id"],
        },
    },
]


async def ejecutar_herramienta(nombre: str, entrada: dict, telefono: str) -> str:
    """
    Ejecuta la herramienta pedida por Claude y retorna el resultado como JSON.
    El teléfono viene de la sesión (no de Claude) para que nadie pueda
    consultar o cancelar citas de otra persona.
    """
    try:
        if nombre == "consultar_disponibilidad":
            resultado = await agenda.obtener_slots_disponibles(entrada.get("fecha", ""))
        elif nombre == "agendar_cita":
            resultado = await agenda.agendar_cita(
                telefono=telefono,
                nombre=entrada.get("nombre", ""),
                fecha_str=entrada.get("fecha", ""),
                hora_str=entrada.get("hora", ""),
                motivo=entrada.get("motivo", ""),
            )
            if resultado.get("ok"):
                await _notificar_dueno(
                    f"Nueva cita agendada:\n"
                    f"- {resultado['nombre']} ({telefono})\n"
                    f"- {resultado['fecha']} a las {resultado['hora']}\n"
                    f"- Motivo: {resultado['motivo']}"
                )
        elif nombre == "listar_citas":
            resultado = await agenda.listar_citas(telefono)
        elif nombre == "cancelar_cita":
            resultado = await agenda.cancelar_cita(telefono, int(entrada.get("cita_id", 0)))
            if resultado.get("ok"):
                await _notificar_dueno(
                    f"Cita cancelada por {telefono}:\n"
                    f"- {resultado['fecha']} a las {resultado['hora']}\n"
                    f"- Motivo: {resultado['motivo']}"
                )
        else:
            resultado = {"ok": False, "error": f"Herramienta desconocida: {nombre}"}
    except Exception as e:
        logger.error(f"Error ejecutando herramienta {nombre}: {e}")
        resultado = {"ok": False, "error": "Error interno ejecutando la herramienta"}

    return json.dumps(resultado, ensure_ascii=False)


async def _notificar_dueno(mensaje: str):
    """
    Avisa al dueño por WhatsApp cuando hay movimientos en su agenda.
    Solo si NUMERO_DUENO está configurado en .env; nunca rompe el flujo si falla.
    """
    numero = os.getenv("NUMERO_DUENO", "").strip()
    if not numero:
        return
    try:
        from agent.providers import obtener_proveedor
        proveedor = obtener_proveedor()
        await proveedor.enviar_mensaje(numero, mensaje)
    except Exception as e:
        logger.warning(f"No se pudo notificar al dueño: {e}")


def cargar_info_negocio() -> dict:
    """Carga la información del negocio desde business.yaml."""
    try:
        with open("config/business.yaml", "r", encoding="utf-8") as f:
            return yaml.safe_load(f) or {}
    except FileNotFoundError:
        logger.error("config/business.yaml no encontrado")
        return {}
