# tests/test_local.py — Simulador de chat en terminal

"""
Prueba tu asistente sin necesitar WhatsApp: simula que TÚ (el dueño)
le escribes por WhatsApp. Los mensajes que el asistente "envía" a negocios
se imprimen en la terminal (proveedor consola).

Requiere ANTHROPIC_API_KEY en .env.
"""

import asyncio
import sys
import os

# Agregar el directorio raíz al path y forzar proveedor consola
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("WHATSAPP_PROVIDER", "consola")

from agent.brain import generar_respuesta
from agent.memory import inicializar_db, guardar_mensaje, obtener_historial, limpiar_historial
from agent.scheduler import revisar_recordatorios

TELEFONO_TEST = os.getenv("OWNER_PHONE_NUMBER") or "test-local-001"


async def main():
    """Loop principal del chat de prueba."""
    await inicializar_db()

    print()
    print("=" * 55)
    print("   Asistente Personal — Test Local")
    print("=" * 55)
    print()
    print("  Escribe como si le hablaras a tu asistente por WhatsApp.")
    print("  Prueba cosas como:")
    print("    'recuérdame mañana a las 9 llamar al dentista'")
    print("    'busca un dermatólogo en Ciudad de México'")
    print("    'qué tengo pendiente?'")
    print("  Comandos especiales:")
    print("    'limpiar'  — borra el historial")
    print("    'salir'    — termina el test")
    print()
    print("-" * 55)
    print()

    while True:
        try:
            mensaje = input("Tú: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n\nTest finalizado.")
            break

        if not mensaje:
            continue

        if mensaje.lower() == "salir":
            print("\nTest finalizado.")
            break

        if mensaje.lower() == "limpiar":
            await limpiar_historial(TELEFONO_TEST)
            print("[Historial borrado]\n")
            continue

        # Simular el paso del scheduler (por si hay recordatorios vencidos)
        await revisar_recordatorios()

        historial = await obtener_historial(TELEFONO_TEST)

        print("\nAria: ", end="", flush=True)
        respuesta = await generar_respuesta(mensaje, historial)
        print(respuesta)
        print()

        await guardar_mensaje(TELEFONO_TEST, "user", mensaje)
        await guardar_mensaje(TELEFONO_TEST, "assistant", respuesta)


if __name__ == "__main__":
    asyncio.run(main())
