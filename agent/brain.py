# agent/brain.py — Cerebro del agente: conexión con Claude API
# Generado por AgentKit

"""
Lógica de IA del agente. Lee el system prompt de prompts.yaml, incorpora
los archivos de /knowledge y genera respuestas con la API de Anthropic,
usando herramientas (tool use) para gestionar la agenda de citas.
"""

import os
import yaml
import logging
from anthropic import AsyncAnthropic
from dotenv import load_dotenv

from agent.agenda import ahora_local, DIAS_SEMANA
from agent.tools import HERRAMIENTAS, ejecutar_herramienta

load_dotenv()
logger = logging.getLogger("agentkit")

# Cliente de Anthropic
client = AsyncAnthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

MODELO = os.getenv("CLAUDE_MODEL", "claude-sonnet-5")
MAX_ITERACIONES_HERRAMIENTAS = 8
MAX_CHARS_KNOWLEDGE = 20000


def cargar_config_prompts() -> dict:
    """Lee toda la configuración desde config/prompts.yaml."""
    try:
        with open("config/prompts.yaml", "r", encoding="utf-8") as f:
            return yaml.safe_load(f) or {}
    except FileNotFoundError:
        logger.error("config/prompts.yaml no encontrado")
        return {}


def cargar_knowledge() -> str:
    """
    Lee los archivos de texto de /knowledge y los concatena para
    incorporarlos al system prompt (menú, precios, FAQ, etc.).
    """
    knowledge_dir = "knowledge"
    if not os.path.isdir(knowledge_dir):
        return ""

    partes = []
    total = 0
    for archivo in sorted(os.listdir(knowledge_dir)):
        ruta = os.path.join(knowledge_dir, archivo)
        if archivo.startswith(".") or not os.path.isfile(ruta):
            continue
        try:
            with open(ruta, "r", encoding="utf-8") as f:
                contenido = f.read().strip()
        except (UnicodeDecodeError, IOError):
            continue  # Ignorar binarios (PDF, imágenes) — convertir a .txt/.md
        if not contenido:
            continue
        fragmento = f"### {archivo}\n{contenido}"
        if total + len(fragmento) > MAX_CHARS_KNOWLEDGE:
            fragmento = fragmento[: MAX_CHARS_KNOWLEDGE - total]
        partes.append(fragmento)
        total += len(fragmento)
        if total >= MAX_CHARS_KNOWLEDGE:
            break
    return "\n\n".join(partes)


def construir_system_prompt() -> str:
    """System prompt = base de prompts.yaml + fecha actual + knowledge."""
    config = cargar_config_prompts()
    base = config.get("system_prompt", "Eres un asistente útil. Responde en español.")

    ahora = ahora_local()
    contexto_fecha = (
        f"\n## Contexto actual\n"
        f"- Fecha y hora actual: {DIAS_SEMANA[ahora.weekday()]} "
        f"{ahora.strftime('%Y-%m-%d %H:%M')} ({ahora.tzinfo})\n"
        f"- Usa esta fecha para interpretar expresiones como 'mañana' o 'el próximo martes'."
    )

    knowledge = cargar_knowledge()
    seccion_knowledge = f"\n## Información adicional\n{knowledge}" if knowledge else ""

    return base + contexto_fecha + seccion_knowledge


def obtener_mensaje_error() -> str:
    """Retorna el mensaje de error configurado en prompts.yaml."""
    config = cargar_config_prompts()
    return config.get("error_message", "Lo siento, estoy teniendo problemas técnicos. Por favor intenta de nuevo en unos minutos.")


def obtener_mensaje_fallback() -> str:
    """Retorna el mensaje de fallback configurado en prompts.yaml."""
    config = cargar_config_prompts()
    return config.get("fallback_message", "Disculpa, no entendí tu mensaje. ¿Podrías reformularlo?")


async def generar_respuesta(mensaje: str, historial: list[dict], telefono: str = "desconocido") -> str:
    """
    Genera una respuesta usando Claude API con tool use.

    Args:
        mensaje: El mensaje nuevo del usuario
        historial: Mensajes anteriores [{"role": "user/assistant", "content": "..."}]
        telefono: Número del remitente (identifica sus citas en las herramientas)

    Returns:
        La respuesta generada por Claude
    """
    # Si el mensaje es muy corto o vacío, usar fallback
    if not mensaje or len(mensaje.strip()) < 2:
        return obtener_mensaje_fallback()

    system_prompt = construir_system_prompt()

    # Construir mensajes para la API: historial + mensaje actual
    mensajes = [{"role": m["role"], "content": m["content"]} for m in historial]
    mensajes.append({"role": "user", "content": mensaje})

    try:
        for _ in range(MAX_ITERACIONES_HERRAMIENTAS):
            response = await client.messages.create(
                model=MODELO,
                max_tokens=1024,
                system=system_prompt,
                tools=HERRAMIENTAS,
                messages=mensajes,
            )

            if response.stop_reason != "tool_use":
                textos = [b.text for b in response.content if b.type == "text"]
                respuesta = "\n".join(textos).strip()
                logger.info(
                    f"Respuesta generada ({response.usage.input_tokens} in / "
                    f"{response.usage.output_tokens} out)"
                )
                return respuesta or obtener_mensaje_fallback()

            # Claude pidió usar herramientas: ejecutarlas y devolver resultados
            mensajes.append({"role": "assistant", "content": response.content})
            resultados = []
            for bloque in response.content:
                if bloque.type == "tool_use":
                    logger.info(f"Herramienta: {bloque.name} — {bloque.input}")
                    salida = await ejecutar_herramienta(bloque.name, bloque.input, telefono)
                    resultados.append({
                        "type": "tool_result",
                        "tool_use_id": bloque.id,
                        "content": salida,
                    })
            mensajes.append({"role": "user", "content": resultados})

        logger.warning("Se alcanzó el máximo de iteraciones de herramientas")
        return obtener_mensaje_error()

    except Exception as e:
        logger.error(f"Error Claude API: {e}")
        return obtener_mensaje_error()
