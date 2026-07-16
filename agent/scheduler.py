# agent/scheduler.py — Envío proactivo de recordatorios

"""
Tarea de fondo que revisa cada minuto si hay recordatorios vencidos
y se los envía al dueño por WhatsApp. Así el asistente te recuerda
lo pendiente sin que tengas que preguntarle.
"""

import os
import asyncio
import logging
from datetime import datetime

from agent import memory
from agent.providers import obtener_proveedor

logger = logging.getLogger("asistente")

INTERVALO_SEGUNDOS = 60


async def revisar_recordatorios():
    """Envía al dueño los recordatorios cuya hora ya llegó."""
    owner = os.getenv("OWNER_PHONE_NUMBER", "")
    if not owner:
        return  # sin número del dueño no hay a quién avisar

    vencidos = await memory.obtener_recordatorios_vencidos(datetime.now())
    if not vencidos:
        return

    proveedor = obtener_proveedor()
    for rec in vencidos:
        texto = f"⏰ Recordatorio: {rec['mensaje']}"
        enviado = await proveedor.enviar_mensaje(owner, texto)
        if enviado:
            await memory.marcar_recordatorio_enviado(rec["id"])
            await memory.guardar_mensaje(owner, "assistant", texto)
            logger.info(f"Recordatorio #{rec['id']} enviado al dueño")


async def loop_recordatorios():
    """Loop infinito de fondo (se lanza en el lifespan de FastAPI)."""
    logger.info("Scheduler de recordatorios iniciado")
    while True:
        try:
            await revisar_recordatorios()
        except Exception as e:
            logger.error(f"Error en scheduler: {e}")
        await asyncio.sleep(INTERVALO_SEGUNDOS)
