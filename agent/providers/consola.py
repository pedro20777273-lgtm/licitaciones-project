# agent/providers/consola.py — Proveedor de prueba (imprime en terminal)

"""
Proveedor falso para desarrollo local: en lugar de enviar mensajes reales
por WhatsApp, los imprime en la terminal. Permite probar todo el asistente
sin credenciales de Twilio ni de Meta.
"""

import logging
from fastapi import Request
from agent.providers.base import ProveedorWhatsApp, MensajeEntrante

logger = logging.getLogger("asistente")


class ProveedorConsola(ProveedorWhatsApp):
    """Simula WhatsApp imprimiendo los mensajes salientes en la terminal."""

    # Registro de mensajes "enviados", útil para tests
    enviados: list[dict] = []

    async def parsear_webhook(self, request: Request) -> list[MensajeEntrante]:
        """Acepta un JSON simple: {"telefono": "...", "texto": "..."}"""
        body = await request.json()
        if not body.get("texto"):
            return []
        return [MensajeEntrante(
            telefono=body.get("telefono", "desconocido"),
            texto=body.get("texto", ""),
            mensaje_id=body.get("id", "consola-msg"),
            es_propio=False,
        )]

    async def enviar_mensaje(self, telefono: str, mensaje: str) -> bool:
        registro = {"telefono": telefono, "mensaje": mensaje}
        ProveedorConsola.enviados.append(registro)
        print(f"\n📤 [WhatsApp simulado → {telefono}]\n{mensaje}\n")
        logger.info(f"[consola] Mensaje a {telefono}: {mensaje[:80]}")
        return True
