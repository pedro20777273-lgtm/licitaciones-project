# agent/main.py — Servidor FastAPI + Webhook de WhatsApp

"""
Servidor principal del asistente personal.

Dos tipos de mensajes entrantes:
- Del DUEÑO (OWNER_PHONE_NUMBER): órdenes al asistente → pasan por el cerebro (Claude)
- De TERCEROS (negocios contactados): se guardan y se reenvían al dueño como aviso
"""

import os
import logging
from contextlib import asynccontextmanager

import asyncio
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import PlainTextResponse
from dotenv import load_dotenv

from agent.brain import generar_respuesta
from agent.memory import inicializar_db, guardar_mensaje, obtener_historial
from agent.providers import obtener_proveedor
from agent.scheduler import loop_recordatorios

load_dotenv()

ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
logging.basicConfig(level=logging.DEBUG if ENVIRONMENT == "development" else logging.INFO)
logger = logging.getLogger("asistente")

proveedor = obtener_proveedor()
PORT = int(os.getenv("PORT", 8000))
OWNER = os.getenv("OWNER_PHONE_NUMBER", "")


def _normalizar(numero: str) -> str:
    """Normaliza un número para comparar (quita espacios, guiones y prefijo whatsapp:)."""
    return numero.replace("whatsapp:", "").replace(" ", "").replace("-", "").lstrip("+")


def es_dueno(telefono: str) -> bool:
    """True si el mensaje viene del dueño del asistente."""
    return bool(OWNER) and _normalizar(telefono) == _normalizar(OWNER)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Inicializa la base de datos y arranca el scheduler de recordatorios."""
    await inicializar_db()
    logger.info("Base de datos inicializada")
    tarea_scheduler = asyncio.create_task(loop_recordatorios())
    logger.info(f"Servidor del asistente corriendo en puerto {PORT}")
    logger.info(f"Proveedor de WhatsApp: {proveedor.__class__.__name__}")
    if not OWNER:
        logger.warning("OWNER_PHONE_NUMBER no configurado: nadie podrá darle órdenes al asistente")
    yield
    tarea_scheduler.cancel()


app = FastAPI(
    title="Asistente Personal — WhatsApp AI Agent",
    version="1.0.0",
    lifespan=lifespan,
)


@app.get("/")
async def health_check():
    """Endpoint de salud para Railway/monitoreo."""
    return {"status": "ok", "service": "asistente-personal"}


@app.get("/webhook")
async def webhook_verificacion(request: Request):
    """Verificación GET del webhook (requerido por Meta Cloud API)."""
    resultado = await proveedor.validar_webhook(request)
    if resultado is not None:
        return PlainTextResponse(str(resultado))
    return {"status": "ok"}


@app.post("/webhook")
async def webhook_handler(request: Request):
    """Recibe mensajes de WhatsApp y los procesa según quién escribe."""
    try:
        mensajes = await proveedor.parsear_webhook(request)

        for msg in mensajes:
            if msg.es_propio or not msg.texto:
                continue

            if es_dueno(msg.telefono):
                # El dueño da una orden → cerebro con herramientas
                logger.info(f"Mensaje del dueño: {msg.texto}")
                historial = await obtener_historial(msg.telefono)
                respuesta = await generar_respuesta(msg.texto, historial)
                await guardar_mensaje(msg.telefono, "user", msg.texto)
                await guardar_mensaje(msg.telefono, "assistant", respuesta)
                await proveedor.enviar_mensaje(msg.telefono, respuesta)
            else:
                # Un tercero responde (ej. el consultorio contactado) →
                # guardar y reenviar el aviso al dueño
                logger.info(f"Respuesta de tercero {msg.telefono}: {msg.texto}")
                await guardar_mensaje(msg.telefono, "user", msg.texto)
                if OWNER:
                    aviso = f"📩 Respuesta de {msg.telefono}:\n\n{msg.texto}"
                    await proveedor.enviar_mensaje(OWNER, aviso)
                    await guardar_mensaje(OWNER, "assistant", aviso)

        return {"status": "ok"}

    except Exception as e:
        logger.error(f"Error en webhook: {e}")
        raise HTTPException(status_code=500, detail=str(e))
