# agent/providers/__init__.py — Factory de proveedores

"""
Selecciona el proveedor de WhatsApp según la variable WHATSAPP_PROVIDER en .env.
"""

import os
from agent.providers.base import ProveedorWhatsApp

_proveedor_cache: ProveedorWhatsApp | None = None


def obtener_proveedor() -> ProveedorWhatsApp:
    """Retorna el proveedor de WhatsApp configurado en .env (singleton)."""
    global _proveedor_cache
    if _proveedor_cache is not None:
        return _proveedor_cache

    proveedor = os.getenv("WHATSAPP_PROVIDER", "consola").lower()

    if proveedor == "meta":
        from agent.providers.meta import ProveedorMeta
        _proveedor_cache = ProveedorMeta()
    elif proveedor == "twilio":
        from agent.providers.twilio import ProveedorTwilio
        _proveedor_cache = ProveedorTwilio()
    elif proveedor == "consola":
        from agent.providers.consola import ProveedorConsola
        _proveedor_cache = ProveedorConsola()
    else:
        raise ValueError(f"Proveedor no soportado: {proveedor}. Usa: meta, twilio o consola")

    return _proveedor_cache
