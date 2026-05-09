import logging
import mimetypes
import smtplib
import socket
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path

from config import DELIVERY_EMAIL, GMAIL_APP_PASSWORD, GMAIL_USER

# Force IPv4 — some servers don't support IPv6 SMTP
_orig_getaddrinfo = socket.getaddrinfo
def _ipv4_only(*args, **kwargs):
    return [r for r in _orig_getaddrinfo(*args, **kwargs) if r[0] == socket.AF_INET]
socket.getaddrinfo = _ipv4_only

logger = logging.getLogger(__name__)

SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 587


def _build_subject(analysis: dict) -> str:
    expediente = analysis.get("identificacion", {}).get("expediente", "SIN-EXP")
    objeto_corto = analysis.get("identificacion", {}).get("objeto_corto", "Licitación")
    return f"RESUMEN IBR — {expediente} — {objeto_corto}"


def _build_body(analysis: dict) -> str:
    ident = analysis.get("identificacion", {})
    alertas = analysis.get("restricciones_excluyentes", [])
    errores = analysis.get("errores_detectados", [])
    resumen = analysis.get("resumen_ejecutivo", "")

    lines = [
        "Estimado Pedro,",
        "",
        "Adjunto encontrarás el análisis automático de la licitación.",
        "",
        "── DATOS PRINCIPALES ──────────────────────────────",
        f"Expediente:    {ident.get('expediente', 'N/A')}",
        f"Objeto:        {ident.get('objeto', 'N/A')}",
        f"Órgano:        {ident.get('organo_contratacion', 'N/A')}",
        f"Presupuesto:   {ident.get('presupuesto_base', 'N/A')} (sin IVA)",
        f"Límite oferta: {ident.get('fecha_limite_oferta', 'N/A')}",
        "",
        "── RESUMEN EJECUTIVO ──────────────────────────────",
        resumen,
        "",
    ]

    if alertas:
        lines.append("── ⚠️ ALERTAS / RESTRICCIONES EXCLUYENTES ────────")
        for a in alertas:
            impacto = a.get("impacto", "").upper()
            lines.append(f"[{impacto}] {a.get('descripcion', '')}")
        lines.append("")

    if errores:
        lines.append("── 🔍 ERRORES / CONTRADICCIONES DETECTADAS ───────")
        for e in errores:
            lines.append(f"• [{e.get('tipo', '').upper()}] {e.get('descripcion', '')}")
            if e.get("recomendacion"):
                lines.append(f"  → {e.get('recomendacion')}")
        lines.append("")

    lines += [
        "──────────────────────────────────────────────────",
        "Este análisis ha sido generado automáticamente.",
        "Revisa siempre los documentos originales antes de presentar oferta.",
        "",
        "Un saludo,",
        "Sistema de Análisis de Licitaciones — Hologic Iberia",
    ]

    return "\n".join(lines)


def send_results(
    analysis: dict,
    attachments: list[str],
) -> None:
    subject = _build_subject(analysis)
    body = _build_body(analysis)

    msg = MIMEMultipart()
    msg["From"] = GMAIL_USER
    msg["To"] = DELIVERY_EMAIL
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain", "utf-8"))

    attached_count = 0
    for file_path in attachments:
        p = Path(file_path)
        if not p.exists():
            logger.warning(f"Adjunto no encontrado: {file_path}")
            continue
        mime_type, _ = mimetypes.guess_type(str(p))
        if mime_type is None:
            mime_type = "application/octet-stream"
        main_type, sub_type = mime_type.split("/", 1)
        with open(p, "rb") as f:
            part = MIMEApplication(f.read(), _subtype=sub_type)
        part.add_header("Content-Disposition", "attachment", filename=p.name)
        msg.attach(part)
        attached_count += 1

    logger.info(f"PASO 6: Enviando email a {DELIVERY_EMAIL} con {attached_count} adjuntos…")

    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(GMAIL_USER, GMAIL_APP_PASSWORD)
        server.sendmail(GMAIL_USER, DELIVERY_EMAIL, msg.as_string())

    logger.info(f"PASO 6: Email enviado correctamente. Asunto: {subject}")
