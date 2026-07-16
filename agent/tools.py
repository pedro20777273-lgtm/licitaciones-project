# agent/tools.py — Herramientas del asistente personal

"""
Capacidades reales del asistente, expuestas a Claude via tool use:
- Tareas: crear, listar, completar
- Recordatorios: programar y listar (el scheduler los envía por WhatsApp)
- Citas médicas: búsqueda en plataformas configuradas (Doctoralia, etc.)
- Mensajes a negocios: SIEMPRE en dos pasos (proponer → autorización del dueño → ejecutar)
"""

import logging
import urllib.parse
from datetime import datetime

import httpx
import yaml
from bs4 import BeautifulSoup

from agent import memory

logger = logging.getLogger("asistente")


def cargar_config_asistente() -> dict:
    """Carga la configuración desde config/asistente.yaml."""
    try:
        with open("config/asistente.yaml", "r", encoding="utf-8") as f:
            return yaml.safe_load(f) or {}
    except FileNotFoundError:
        logger.error("config/asistente.yaml no encontrado")
        return {}


# ─────────────────────────── Definición de herramientas (schema para Claude) ───────────────────────────

DEFINICION_HERRAMIENTAS = [
    {
        "name": "crear_tarea",
        "description": "Crea una tarea pendiente para el dueño. Úsala cuando mencione algo que debe hacer.",
        "input_schema": {
            "type": "object",
            "properties": {
                "descripcion": {"type": "string", "description": "Qué hay que hacer"},
                "fecha_limite": {"type": "string", "description": "Fecha límite en formato YYYY-MM-DD (opcional)"},
                "prioridad": {"type": "string", "enum": ["alta", "media", "baja"], "description": "Prioridad de la tarea"},
            },
            "required": ["descripcion"],
        },
    },
    {
        "name": "listar_tareas",
        "description": "Lista las tareas del dueño. Úsala para revisar pendientes o planificar el día.",
        "input_schema": {
            "type": "object",
            "properties": {
                "estado": {"type": "string", "enum": ["pendiente", "completada", "todas"], "description": "Filtro de estado (default: pendiente)"},
            },
        },
    },
    {
        "name": "completar_tarea",
        "description": "Marca una tarea como completada usando su ID.",
        "input_schema": {
            "type": "object",
            "properties": {
                "tarea_id": {"type": "integer", "description": "ID de la tarea a completar"},
            },
            "required": ["tarea_id"],
        },
    },
    {
        "name": "crear_recordatorio",
        "description": "Programa un recordatorio que le llegará al dueño por WhatsApp en la fecha y hora indicadas.",
        "input_schema": {
            "type": "object",
            "properties": {
                "mensaje": {"type": "string", "description": "Texto del recordatorio"},
                "fecha_hora": {"type": "string", "description": "Fecha y hora en formato ISO: YYYY-MM-DDTHH:MM"},
            },
            "required": ["mensaje", "fecha_hora"],
        },
    },
    {
        "name": "listar_recordatorios",
        "description": "Lista los recordatorios programados pendientes de enviar.",
        "input_schema": {"type": "object", "properties": {}},
    },
    {
        "name": "buscar_citas_medicas",
        "description": "Busca doctores y citas médicas en las plataformas configuradas (Doctoralia, Top Doctors) por especialidad y ciudad. Retorna resultados encontrados y enlaces directos de búsqueda.",
        "input_schema": {
            "type": "object",
            "properties": {
                "especialidad": {"type": "string", "description": "Especialidad médica, ej: dermatólogo, dentista"},
                "ciudad": {"type": "string", "description": "Ciudad donde buscar"},
            },
            "required": ["especialidad", "ciudad"],
        },
    },
    {
        "name": "proponer_mensaje_whatsapp",
        "description": "PASO 1 para contactar a un negocio/tercero: registra el mensaje propuesto y retorna un ID de acción. El mensaje NO se envía todavía — debes mostrarle al dueño el texto exacto y el número, y esperar su confirmación explícita.",
        "input_schema": {
            "type": "object",
            "properties": {
                "telefono": {"type": "string", "description": "Número de WhatsApp del negocio en formato internacional, ej: +5215512345678"},
                "mensaje": {"type": "string", "description": "Texto exacto que se enviará"},
                "motivo": {"type": "string", "description": "Por qué se contacta al negocio (contexto para el dueño)"},
            },
            "required": ["telefono", "mensaje", "motivo"],
        },
    },
    {
        "name": "ejecutar_accion_pendiente",
        "description": "PASO 2: envía el mensaje registrado con proponer_mensaje_whatsapp. SOLO usar después de que el dueño confirmó explícitamente en su último mensaje.",
        "input_schema": {
            "type": "object",
            "properties": {
                "accion_id": {"type": "integer", "description": "ID de la acción a ejecutar"},
            },
            "required": ["accion_id"],
        },
    },
    {
        "name": "rechazar_accion_pendiente",
        "description": "Descarta una acción propuesta cuando el dueño dice que no o pide cambios.",
        "input_schema": {
            "type": "object",
            "properties": {
                "accion_id": {"type": "integer", "description": "ID de la acción a descartar"},
            },
            "required": ["accion_id"],
        },
    },
]


# ─────────────────────────── Implementación ───────────────────────────

async def _buscar_en_doctoralia(url: str) -> list[str]:
    """
    Intenta extraer nombres de doctores de una página de resultados de Doctoralia.
    El scraping de sitios externos es frágil: si la estructura cambia o el sitio
    bloquea la petición, retornamos lista vacía y el asistente ofrece los enlaces.
    """
    try:
        async with httpx.AsyncClient(timeout=15, follow_redirects=True) as client:
            r = await client.get(url, headers={"User-Agent": "Mozilla/5.0 (asistente personal)"})
            if r.status_code != 200:
                return []
            soup = BeautifulSoup(r.text, "html.parser")
            resultados = []
            for enlace in soup.select("a[data-id='result-item-doctor-name'], h3 a, [itemprop='name']"):
                nombre = enlace.get_text(strip=True)
                href = enlace.get("href", "")
                if nombre and len(nombre) > 3:
                    resultados.append(f"{nombre} — {href}" if href else nombre)
                if len(resultados) >= 5:
                    break
            return resultados
    except Exception as e:
        logger.warning(f"Búsqueda en plataforma falló: {e}")
        return []


async def buscar_citas_medicas(especialidad: str, ciudad: str) -> str:
    """Busca doctores en las plataformas configuradas y arma un resumen."""
    config = cargar_config_asistente()
    plataformas = config.get("plataformas_medicas", [])
    if not plataformas:
        return "No hay plataformas médicas configuradas en config/asistente.yaml."

    esp = urllib.parse.quote(especialidad)
    ciu = urllib.parse.quote(ciudad)
    lineas = [f"Búsqueda: {especialidad} en {ciudad}\n"]

    for plataforma in plataformas:
        url = plataforma["url_busqueda"].format(especialidad=esp, ciudad=ciu)
        encontrados = []
        if "doctoralia" in url:
            encontrados = await _buscar_en_doctoralia(url)
        if encontrados:
            lineas.append(f"✅ {plataforma['nombre']} — resultados:")
            lineas.extend(f"   • {r}" for r in encontrados)
        else:
            lineas.append(f"🔗 {plataforma['nombre']}: {url}")

    lineas.append(
        "\nNota: si algún consultorio tiene WhatsApp, puedo escribirle para "
        "preguntar disponibilidad (con tu autorización)."
    )
    return "\n".join(lineas)


async def ejecutar_herramienta(nombre: str, entrada: dict) -> str:
    """
    Despachador: ejecuta la herramienta pedida por Claude y retorna el
    resultado como texto (que Claude usa para responder al dueño).
    """
    try:
        if nombre == "crear_tarea":
            tarea_id = await memory.crear_tarea(
                descripcion=entrada["descripcion"],
                fecha_limite=entrada.get("fecha_limite", ""),
                prioridad=entrada.get("prioridad", "media"),
            )
            return f"Tarea #{tarea_id} creada: {entrada['descripcion']}"

        if nombre == "listar_tareas":
            tareas = await memory.listar_tareas(entrada.get("estado", "pendiente"))
            if not tareas:
                return "No hay tareas con ese filtro."
            return "\n".join(
                f"#{t['id']} [{t['prioridad']}] {t['descripcion']}"
                + (f" (límite: {t['fecha_limite']})" if t["fecha_limite"] else "")
                + (f" — {t['estado']}" if t["estado"] != "pendiente" else "")
                for t in tareas
            )

        if nombre == "completar_tarea":
            ok = await memory.completar_tarea(entrada["tarea_id"])
            return f"Tarea #{entrada['tarea_id']} completada." if ok else f"No existe la tarea #{entrada['tarea_id']}."

        if nombre == "crear_recordatorio":
            fecha = datetime.fromisoformat(entrada["fecha_hora"])
            rec_id = await memory.crear_recordatorio(entrada["mensaje"], fecha)
            return f"Recordatorio #{rec_id} programado para {fecha.strftime('%d/%m/%Y %H:%M')}."

        if nombre == "listar_recordatorios":
            recs = await memory.listar_recordatorios()
            if not recs:
                return "No hay recordatorios pendientes."
            return "\n".join(f"#{r['id']} {r['fecha_hora']} — {r['mensaje']}" for r in recs)

        if nombre == "buscar_citas_medicas":
            return await buscar_citas_medicas(entrada["especialidad"], entrada["ciudad"])

        if nombre == "proponer_mensaje_whatsapp":
            accion_id = await memory.crear_accion_pendiente("whatsapp_negocio", {
                "telefono": entrada["telefono"],
                "mensaje": entrada["mensaje"],
                "motivo": entrada["motivo"],
            })
            return (
                f"Acción #{accion_id} registrada (NO enviada). "
                f"Muestra al dueño el número {entrada['telefono']} y el texto exacto, "
                f"y espera su confirmación antes de ejecutar."
            )

        if nombre == "ejecutar_accion_pendiente":
            accion = await memory.obtener_accion_pendiente(entrada["accion_id"])
            if accion is None:
                return f"No existe la acción #{entrada['accion_id']}."
            if accion["estado"] != "pendiente":
                return f"La acción #{accion['id']} ya está {accion['estado']} — no se reenvía."
            # Import tardío para evitar dependencia circular
            from agent.providers import obtener_proveedor
            proveedor = obtener_proveedor()
            datos = accion["datos"]
            exito = await proveedor.enviar_mensaje(datos["telefono"], datos["mensaje"])
            if exito:
                await memory.actualizar_estado_accion(accion["id"], "ejecutada")
                await memory.guardar_mensaje(datos["telefono"], "assistant", datos["mensaje"])
                return f"Mensaje enviado a {datos['telefono']}. Te aviso cuando respondan."
            return "El envío falló (revisa la configuración del proveedor de WhatsApp)."

        if nombre == "rechazar_accion_pendiente":
            ok = await memory.actualizar_estado_accion(entrada["accion_id"], "rechazada")
            return f"Acción #{entrada['accion_id']} descartada." if ok else f"No existe la acción #{entrada['accion_id']}."

        return f"Herramienta desconocida: {nombre}"

    except Exception as e:
        logger.error(f"Error ejecutando herramienta {nombre}: {e}")
        return f"Error al ejecutar {nombre}: {e}"
