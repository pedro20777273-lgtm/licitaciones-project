# agent/brain.py — Cerebro del asistente: Claude API con herramientas

"""
Lógica de IA del asistente. Lee el system prompt de config/prompts.yaml y genera
respuestas con Claude usando tool use: Claude decide cuándo crear tareas,
programar recordatorios, buscar citas o proponer mensajes a negocios.
"""

import os
import yaml
import logging
from datetime import datetime
from anthropic import AsyncAnthropic
from dotenv import load_dotenv

from agent.tools import DEFINICION_HERRAMIENTAS, ejecutar_herramienta

load_dotenv()
logger = logging.getLogger("asistente")

client = AsyncAnthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

MODELO = "claude-sonnet-4-6"
MAX_ITERACIONES_HERRAMIENTAS = 8  # tope de vueltas del loop agéntico por mensaje


def cargar_config_prompts() -> dict:
    """Lee toda la configuración desde config/prompts.yaml."""
    try:
        with open("config/prompts.yaml", "r", encoding="utf-8") as f:
            return yaml.safe_load(f) or {}
    except FileNotFoundError:
        logger.error("config/prompts.yaml no encontrado")
        return {}


def cargar_system_prompt() -> str:
    """System prompt + fecha/hora actual (para que entienda 'mañana', 'en 2 horas', etc.)."""
    config = cargar_config_prompts()
    base = config.get("system_prompt", "Eres un asistente personal útil. Responde en español.")
    ahora = datetime.now().strftime("%A %d/%m/%Y %H:%M")
    return f"{base}\n\n## Fecha y hora actual\n{ahora}"


def obtener_mensaje_error() -> str:
    config = cargar_config_prompts()
    return config.get("error_message", "Lo siento, tengo un problema técnico. Intenta de nuevo en unos minutos.")


def obtener_mensaje_fallback() -> str:
    config = cargar_config_prompts()
    return config.get("fallback_message", "Disculpa, no entendí tu mensaje. ¿Podrías reformularlo?")


async def generar_respuesta(mensaje: str, historial: list[dict]) -> str:
    """
    Genera la respuesta del asistente para un mensaje del dueño.
    Corre un loop agéntico: si Claude pide herramientas, se ejecutan y se le
    devuelven los resultados hasta que produce la respuesta final en texto.
    """
    if not mensaje or len(mensaje.strip()) < 2:
        return obtener_mensaje_fallback()

    system_prompt = cargar_system_prompt()

    mensajes = [{"role": m["role"], "content": m["content"]} for m in historial]
    mensajes.append({"role": "user", "content": mensaje})

    try:
        for _ in range(MAX_ITERACIONES_HERRAMIENTAS):
            response = await client.messages.create(
                model=MODELO,
                max_tokens=1024,
                system=system_prompt,
                messages=mensajes,
                tools=DEFINICION_HERRAMIENTAS,
            )

            if response.stop_reason != "tool_use":
                # Respuesta final en texto
                textos = [b.text for b in response.content if b.type == "text"]
                return "\n".join(textos).strip() or obtener_mensaje_fallback()

            # Claude pidió una o más herramientas: ejecutarlas y devolver resultados
            mensajes.append({"role": "assistant", "content": response.content})
            resultados = []
            for bloque in response.content:
                if bloque.type == "tool_use":
                    logger.info(f"Herramienta: {bloque.name}({bloque.input})")
                    resultado = await ejecutar_herramienta(bloque.name, bloque.input)
                    resultados.append({
                        "type": "tool_result",
                        "tool_use_id": bloque.id,
                        "content": resultado,
                    })
            mensajes.append({"role": "user", "content": resultados})

        return "Hice varias operaciones pero me quedé sin turnos para responder. ¿Me repites qué necesitas?"

    except Exception as e:
        logger.error(f"Error Claude API: {e}")
        return obtener_mensaje_error()
