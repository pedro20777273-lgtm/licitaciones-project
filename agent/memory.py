# agent/memory.py — Memoria del asistente con SQLite

"""
Persistencia del asistente personal:
- mensajes: historial de conversación por número de teléfono
- tareas: pendientes del dueño (con fecha límite y prioridad)
- recordatorios: avisos programados que se envían por WhatsApp
- acciones_pendientes: mensajes a terceros que esperan autorización del dueño
"""

import os
import json
from datetime import datetime
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String, Text, DateTime, select, Integer, delete
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./asistente.db")

# Si es PostgreSQL en producción, ajustar el esquema de URL
if DATABASE_URL.startswith("postgresql://"):
    DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://", 1)

engine = create_async_engine(DATABASE_URL, echo=False)
async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


class Base(DeclarativeBase):
    pass


class Mensaje(Base):
    """Historial de conversación (con el dueño y con negocios)."""
    __tablename__ = "mensajes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    telefono: Mapped[str] = mapped_column(String(50), index=True)
    role: Mapped[str] = mapped_column(String(20))  # "user" o "assistant"
    content: Mapped[str] = mapped_column(Text)
    timestamp: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class Tarea(Base):
    """Pendiente del dueño."""
    __tablename__ = "tareas"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    descripcion: Mapped[str] = mapped_column(Text)
    fecha_limite: Mapped[str] = mapped_column(String(50), default="")   # texto libre ISO o vacío
    prioridad: Mapped[str] = mapped_column(String(20), default="media")  # alta | media | baja
    estado: Mapped[str] = mapped_column(String(20), default="pendiente")  # pendiente | completada
    creada: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class Recordatorio(Base):
    """Aviso programado que se envía al dueño por WhatsApp."""
    __tablename__ = "recordatorios"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    mensaje: Mapped[str] = mapped_column(Text)
    fecha_hora: Mapped[datetime] = mapped_column(DateTime, index=True)
    estado: Mapped[str] = mapped_column(String(20), default="pendiente")  # pendiente | enviado
    creado: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class AccionPendiente(Base):
    """Acción hacia un tercero que espera autorización explícita del dueño."""
    __tablename__ = "acciones_pendientes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    tipo: Mapped[str] = mapped_column(String(50))   # ej: "whatsapp_negocio"
    datos: Mapped[str] = mapped_column(Text)        # JSON: {telefono, mensaje, motivo}
    estado: Mapped[str] = mapped_column(String(20), default="pendiente")  # pendiente | ejecutada | rechazada
    creada: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


async def inicializar_db():
    """Crea las tablas si no existen."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


# ─────────────────────────── Mensajes ───────────────────────────

async def guardar_mensaje(telefono: str, role: str, content: str):
    """Guarda un mensaje en el historial de conversación."""
    async with async_session() as session:
        session.add(Mensaje(telefono=telefono, role=role, content=content))
        await session.commit()


async def obtener_historial(telefono: str, limite: int = 30) -> list[dict]:
    """Recupera los últimos N mensajes de una conversación en orden cronológico."""
    async with async_session() as session:
        query = (
            select(Mensaje)
            .where(Mensaje.telefono == telefono)
            .order_by(Mensaje.timestamp.desc(), Mensaje.id.desc())
            .limit(limite)
        )
        result = await session.execute(query)
        mensajes = list(result.scalars().all())
        mensajes.reverse()
        return [{"role": m.role, "content": m.content} for m in mensajes]


async def limpiar_historial(telefono: str):
    """Borra todo el historial de una conversación."""
    async with async_session() as session:
        await session.execute(delete(Mensaje).where(Mensaje.telefono == telefono))
        await session.commit()


# ─────────────────────────── Tareas ───────────────────────────

async def crear_tarea(descripcion: str, fecha_limite: str = "", prioridad: str = "media") -> int:
    """Crea una tarea pendiente y retorna su ID."""
    async with async_session() as session:
        tarea = Tarea(descripcion=descripcion, fecha_limite=fecha_limite, prioridad=prioridad)
        session.add(tarea)
        await session.commit()
        await session.refresh(tarea)
        return tarea.id


async def listar_tareas(estado: str = "pendiente") -> list[dict]:
    """Lista tareas por estado ('pendiente', 'completada' o 'todas')."""
    async with async_session() as session:
        query = select(Tarea).order_by(Tarea.creada.asc())
        if estado != "todas":
            query = query.where(Tarea.estado == estado)
        result = await session.execute(query)
        return [
            {
                "id": t.id,
                "descripcion": t.descripcion,
                "fecha_limite": t.fecha_limite,
                "prioridad": t.prioridad,
                "estado": t.estado,
            }
            for t in result.scalars().all()
        ]


async def completar_tarea(tarea_id: int) -> bool:
    """Marca una tarea como completada. Retorna False si no existe."""
    async with async_session() as session:
        tarea = await session.get(Tarea, tarea_id)
        if tarea is None:
            return False
        tarea.estado = "completada"
        await session.commit()
        return True


# ─────────────────────────── Recordatorios ───────────────────────────

async def crear_recordatorio(mensaje: str, fecha_hora: datetime) -> int:
    """Programa un recordatorio y retorna su ID."""
    async with async_session() as session:
        rec = Recordatorio(mensaje=mensaje, fecha_hora=fecha_hora)
        session.add(rec)
        await session.commit()
        await session.refresh(rec)
        return rec.id


async def listar_recordatorios(solo_pendientes: bool = True) -> list[dict]:
    """Lista recordatorios ordenados por fecha."""
    async with async_session() as session:
        query = select(Recordatorio).order_by(Recordatorio.fecha_hora.asc())
        if solo_pendientes:
            query = query.where(Recordatorio.estado == "pendiente")
        result = await session.execute(query)
        return [
            {
                "id": r.id,
                "mensaje": r.mensaje,
                "fecha_hora": r.fecha_hora.isoformat(),
                "estado": r.estado,
            }
            for r in result.scalars().all()
        ]


async def obtener_recordatorios_vencidos(ahora: datetime) -> list[dict]:
    """Recordatorios pendientes cuya hora ya pasó (para el scheduler)."""
    async with async_session() as session:
        query = (
            select(Recordatorio)
            .where(Recordatorio.estado == "pendiente")
            .where(Recordatorio.fecha_hora <= ahora)
        )
        result = await session.execute(query)
        return [
            {"id": r.id, "mensaje": r.mensaje, "fecha_hora": r.fecha_hora.isoformat()}
            for r in result.scalars().all()
        ]


async def marcar_recordatorio_enviado(recordatorio_id: int):
    """Marca un recordatorio como enviado."""
    async with async_session() as session:
        rec = await session.get(Recordatorio, recordatorio_id)
        if rec is not None:
            rec.estado = "enviado"
            await session.commit()


# ─────────────────────────── Acciones pendientes ───────────────────────────

async def crear_accion_pendiente(tipo: str, datos: dict) -> int:
    """Registra una acción que espera autorización del dueño. Retorna su ID."""
    async with async_session() as session:
        accion = AccionPendiente(tipo=tipo, datos=json.dumps(datos, ensure_ascii=False))
        session.add(accion)
        await session.commit()
        await session.refresh(accion)
        return accion.id


async def obtener_accion_pendiente(accion_id: int) -> dict | None:
    """Recupera una acción pendiente por ID."""
    async with async_session() as session:
        accion = await session.get(AccionPendiente, accion_id)
        if accion is None:
            return None
        return {
            "id": accion.id,
            "tipo": accion.tipo,
            "datos": json.loads(accion.datos),
            "estado": accion.estado,
        }


async def actualizar_estado_accion(accion_id: int, estado: str) -> bool:
    """Cambia el estado de una acción (ejecutada / rechazada)."""
    async with async_session() as session:
        accion = await session.get(AccionPendiente, accion_id)
        if accion is None:
            return False
        accion.estado = estado
        await session.commit()
        return True
