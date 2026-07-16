# tests/test_agenda.py — Pruebas del motor de citas (sin API key)
# Generado por AgentKit

"""
Verifica la lógica de la agenda sin necesitar ANTHROPIC_API_KEY ni WhatsApp:
disponibilidad, agendar, doble reserva, listar y cancelar.

Ejecutar:  python tests/test_agenda.py
"""

import asyncio
import os
import sys
import tempfile
from datetime import timedelta

# Usar una base de datos temporal ANTES de importar los módulos del agente
_db_temporal = os.path.join(tempfile.mkdtemp(), "test_agenda.db")
os.environ["DATABASE_URL"] = f"sqlite+aiosqlite:///{_db_temporal}"

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agent.memory import inicializar_db  # noqa: E402
from agent import agenda  # noqa: E402

TELEFONO = "+5215500000001"
OTRO_TELEFONO = "+5215500000002"


def _proximo_dia_habil() -> str:
    """Retorna el próximo día (mañana en adelante) con horario de atención."""
    config = agenda.cargar_config_agenda()
    fecha = agenda.ahora_local().date() + timedelta(days=1)
    for _ in range(14):
        if config["horario"].get(agenda.DIAS_SEMANA[fecha.weekday()]):
            return fecha.isoformat()
        fecha += timedelta(days=1)
    raise RuntimeError("No hay días hábiles configurados en business.yaml")


async def main():
    await inicializar_db()
    fecha = _proximo_dia_habil()
    print(f"Probando agenda con fecha: {fecha}\n")

    # 1. Disponibilidad inicial
    disp = await agenda.obtener_slots_disponibles(fecha)
    assert disp["ok"] and disp["disponibles"], f"Sin slots disponibles: {disp}"
    hora = disp["disponibles"][0]
    print(f"[OK] Disponibilidad: {len(disp['disponibles'])} slots (primero: {hora})")

    # 2. Agendar
    cita = await agenda.agendar_cita(TELEFONO, "Cliente Prueba", fecha, hora, "Reunión de prueba")
    assert cita["ok"], f"No se pudo agendar: {cita}"
    print(f"[OK] Cita agendada: #{cita['cita_id']} — {cita['fecha']} {cita['hora']}")

    # 3. Doble reserva rechazada
    doble = await agenda.agendar_cita(OTRO_TELEFONO, "Otro Cliente", fecha, hora, "Choque")
    assert not doble["ok"] and doble.get("alternativas"), f"Doble reserva no rechazada: {doble}"
    print(f"[OK] Doble reserva rechazada, con {len(doble['alternativas'])} alternativas")

    # 4. El slot ya no aparece disponible
    disp2 = await agenda.obtener_slots_disponibles(fecha)
    assert hora not in disp2["disponibles"], "El slot reservado sigue apareciendo"
    print("[OK] El slot reservado ya no aparece disponible")

    # 5. Listar citas (solo las del teléfono correcto)
    citas = await agenda.listar_citas(TELEFONO)
    assert len(citas["citas"]) == 1, f"Listado incorrecto: {citas}"
    citas_otro = await agenda.listar_citas(OTRO_TELEFONO)
    assert len(citas_otro["citas"]) == 0, "Se filtran citas de otro teléfono"
    print("[OK] Listado por teléfono correcto (privacidad entre clientes)")

    # 6. Otro teléfono NO puede cancelar la cita
    ajeno = await agenda.cancelar_cita(OTRO_TELEFONO, cita["cita_id"])
    assert not ajeno["ok"], "Un tercero pudo cancelar una cita ajena"
    print("[OK] Cancelación por terceros rechazada")

    # 7. Cancelar y liberar el slot
    cancelada = await agenda.cancelar_cita(TELEFONO, cita["cita_id"])
    assert cancelada["ok"], f"No se pudo cancelar: {cancelada}"
    disp3 = await agenda.obtener_slots_disponibles(fecha)
    assert hora in disp3["disponibles"], "El slot no se liberó al cancelar"
    print("[OK] Cita cancelada y slot liberado")

    # 8. Validaciones de formato y fechas
    invalida = await agenda.obtener_slots_disponibles("fecha-mala")
    assert not invalida["ok"]
    pasada = await agenda.obtener_slots_disponibles("2020-01-01")
    assert not pasada["ok"]
    print("[OK] Fechas inválidas y pasadas rechazadas")

    print("\nTodas las pruebas de agenda pasaron.")


if __name__ == "__main__":
    asyncio.run(main())
