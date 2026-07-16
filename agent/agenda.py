# agent/agenda.py — Motor de citas del asistente
# Generado por AgentKit

"""
Gestión de la agenda de citas: disponibilidad, agendar, listar y cancelar.
Las citas se guardan en la misma base de datos que la memoria (SQLite/PostgreSQL).
La configuración del horario vive en config/business.yaml.
"""

import logging
from datetime import datetime, date, time, timedelta
from zoneinfo import ZoneInfo

import yaml
from sqlalchemy import String, Integer, Date, Time, DateTime, select
from sqlalchemy.orm import Mapped, mapped_column

from agent.memory import Base, async_session

logger = logging.getLogger("agentkit")

# Días de la semana en español, en el orden de date.weekday() (0 = lunes)
DIAS_SEMANA = ["lunes", "martes", "miercoles", "jueves", "viernes", "sabado", "domingo"]


class Cita(Base):
    """Modelo de cita en la base de datos."""
    __tablename__ = "citas"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    telefono: Mapped[str] = mapped_column(String(50), index=True)
    nombre: Mapped[str] = mapped_column(String(120))
    fecha: Mapped[date] = mapped_column(Date, index=True)
    hora: Mapped[time] = mapped_column(Time)
    motivo: Mapped[str] = mapped_column(String(300))
    estado: Mapped[str] = mapped_column(String(20), default="confirmada")  # confirmada | cancelada
    creado: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


# ── Configuración ──────────────────────────────────────────────

def cargar_config_agenda() -> dict:
    """Lee la sección 'agenda' de config/business.yaml con defaults seguros."""
    try:
        with open("config/business.yaml", "r", encoding="utf-8") as f:
            config = yaml.safe_load(f) or {}
    except FileNotFoundError:
        logger.error("config/business.yaml no encontrado, usando agenda por defecto")
        config = {}
    agenda = config.get("agenda") or {}
    agenda.setdefault("zona_horaria", "America/Mexico_City")
    agenda.setdefault("duracion_cita_minutos", 60)
    agenda.setdefault("dias_maximos_anticipacion", 30)
    agenda.setdefault("horario", {
        "lunes": ["09:00", "18:00"],
        "martes": ["09:00", "18:00"],
        "miercoles": ["09:00", "18:00"],
        "jueves": ["09:00", "18:00"],
        "viernes": ["09:00", "18:00"],
        "sabado": None,
        "domingo": None,
    })
    return agenda


def ahora_local() -> datetime:
    """Fecha y hora actual en la zona horaria configurada."""
    agenda = cargar_config_agenda()
    return datetime.now(ZoneInfo(agenda["zona_horaria"]))


def _parsear_hora(valor: str) -> time:
    """Convierte 'HH:MM' a time. Lanza ValueError si el formato es inválido."""
    return datetime.strptime(valor.strip(), "%H:%M").time()


def _parsear_fecha(valor: str) -> date:
    """Convierte 'YYYY-MM-DD' a date. Lanza ValueError si el formato es inválido."""
    return datetime.strptime(valor.strip(), "%Y-%m-%d").date()


def _slots_del_dia(fecha: date, config: dict) -> list[time]:
    """Genera todos los slots posibles de un día según el horario configurado."""
    dia_nombre = DIAS_SEMANA[fecha.weekday()]
    rango = (config.get("horario") or {}).get(dia_nombre)
    if not rango:
        return []
    inicio = _parsear_hora(rango[0])
    fin = _parsear_hora(rango[1])
    duracion = timedelta(minutes=int(config["duracion_cita_minutos"]))

    slots = []
    cursor = datetime.combine(fecha, inicio)
    limite = datetime.combine(fecha, fin)
    while cursor + duracion <= limite:
        slots.append(cursor.time())
        cursor += duracion
    return slots


# ── Operaciones de agenda ──────────────────────────────────────

async def obtener_slots_disponibles(fecha_str: str) -> dict:
    """
    Retorna los horarios disponibles para una fecha (formato YYYY-MM-DD).
    Excluye slots ya reservados y horas pasadas si la fecha es hoy.
    """
    config = cargar_config_agenda()
    try:
        fecha = _parsear_fecha(fecha_str)
    except ValueError:
        return {"ok": False, "error": "Formato de fecha inválido, usa YYYY-MM-DD"}

    hoy = ahora_local().date()
    if fecha < hoy:
        return {"ok": False, "error": "La fecha ya pasó, no se puede agendar en el pasado"}
    if fecha > hoy + timedelta(days=int(config["dias_maximos_anticipacion"])):
        return {"ok": False, "error": f"Solo se agenda con máximo {config['dias_maximos_anticipacion']} días de anticipación"}

    slots = _slots_del_dia(fecha, config)
    if not slots:
        return {"ok": True, "fecha": fecha_str, "disponibles": [],
                "nota": f"No se atiende los {DIAS_SEMANA[fecha.weekday()]}"}

    # Descartar horas que ya pasaron si es hoy
    if fecha == hoy:
        hora_actual = ahora_local().time()
        slots = [s for s in slots if s > hora_actual]

    # Descartar slots ya reservados
    async with async_session() as session:
        query = select(Cita.hora).where(Cita.fecha == fecha, Cita.estado == "confirmada")
        result = await session.execute(query)
        ocupados = {h for (h,) in result.all()}

    disponibles = [s.strftime("%H:%M") for s in slots if s not in ocupados]
    return {"ok": True, "fecha": fecha_str, "disponibles": disponibles}


async def agendar_cita(telefono: str, nombre: str, fecha_str: str, hora_str: str, motivo: str) -> dict:
    """Agenda una cita si el slot existe y está libre."""
    config = cargar_config_agenda()
    try:
        fecha = _parsear_fecha(fecha_str)
        hora = _parsear_hora(hora_str)
    except ValueError:
        return {"ok": False, "error": "Formato inválido. Fecha: YYYY-MM-DD, hora: HH:MM"}

    disponibilidad = await obtener_slots_disponibles(fecha_str)
    if not disponibilidad.get("ok"):
        return disponibilidad
    if hora.strftime("%H:%M") not in disponibilidad["disponibles"]:
        return {
            "ok": False,
            "error": "Ese horario no está disponible",
            "alternativas": disponibilidad["disponibles"][:5],
        }

    async with async_session() as session:
        cita = Cita(
            telefono=telefono,
            nombre=nombre.strip(),
            fecha=fecha,
            hora=hora,
            motivo=motivo.strip(),
            estado="confirmada",
        )
        session.add(cita)
        await session.commit()
        await session.refresh(cita)

    logger.info(f"Cita #{cita.id} agendada: {nombre} — {fecha_str} {hora_str} — {motivo}")
    return {
        "ok": True,
        "cita_id": cita.id,
        "nombre": cita.nombre,
        "fecha": fecha_str,
        "hora": hora_str,
        "motivo": cita.motivo,
        "mensaje": "Cita confirmada",
    }


async def listar_citas(telefono: str) -> dict:
    """Lista las citas confirmadas (de hoy en adelante) de un número de teléfono."""
    hoy = ahora_local().date()
    async with async_session() as session:
        query = (
            select(Cita)
            .where(
                Cita.telefono == telefono,
                Cita.estado == "confirmada",
                Cita.fecha >= hoy,
            )
            .order_by(Cita.fecha, Cita.hora)
        )
        result = await session.execute(query)
        citas = result.scalars().all()

    return {
        "ok": True,
        "citas": [
            {
                "cita_id": c.id,
                "nombre": c.nombre,
                "fecha": c.fecha.isoformat(),
                "hora": c.hora.strftime("%H:%M"),
                "motivo": c.motivo,
            }
            for c in citas
        ],
    }


async def cancelar_cita(telefono: str, cita_id: int) -> dict:
    """Cancela una cita. Solo el teléfono que la agendó puede cancelarla."""
    async with async_session() as session:
        cita = await session.get(Cita, cita_id)
        if cita is None or cita.telefono != telefono:
            return {"ok": False, "error": "No encontré esa cita asociada a este número"}
        if cita.estado == "cancelada":
            return {"ok": False, "error": "Esa cita ya estaba cancelada"}
        cita.estado = "cancelada"
        await session.commit()
        datos = {
            "fecha": cita.fecha.isoformat(),
            "hora": cita.hora.strftime("%H:%M"),
            "motivo": cita.motivo,
        }

    logger.info(f"Cita #{cita_id} cancelada por {telefono}")
    return {"ok": True, "cita_id": cita_id, "mensaje": "Cita cancelada", **datos}
