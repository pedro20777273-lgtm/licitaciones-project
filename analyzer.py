import json
import logging
import re
from pathlib import Path

import anthropic

from config import ANTHROPIC_API_KEY, MODEL_DEEP, PROMPTS_DIR

logger = logging.getLogger(__name__)
client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)


def _load_prompt() -> str:
    return (PROMPTS_DIR / "analisis.txt").read_text(encoding="utf-8")


def _build_content_blocks(files_info: list[dict]) -> list[dict]:
    blocks = []
    doc_blocks = []

    for info in files_info:
        if info.get("native_pdf_b64"):
            doc_blocks.append({
                "type": "document",
                "source": {
                    "type": "base64",
                    "media_type": "application/pdf",
                    "data": info["native_pdf_b64"],
                },
                "title": info["name"],
            })
        elif info.get("content_md"):
            doc_blocks.append({
                "type": "text",
                "text": f"=== DOCUMENTO: {info['name']} ===\n\n{info['content_md']}\n\n=== FIN: {info['name']} ===",
            })

    if not doc_blocks:
        raise ValueError("No hay contenido de documentos para analizar")

    # Apply cache_control to the last document block
    doc_blocks[-1]["cache_control"] = {"type": "ephemeral"}
    blocks.extend(doc_blocks)

    # Task instruction as final block (not cached so it can vary)
    blocks.append({"type": "text", "text": _load_prompt()})
    return blocks


def _extract_json(text: str) -> dict:
    # Try code block first
    m = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", text, re.DOTALL)
    if m:
        return json.loads(m.group(1))

    # Try direct JSON parse
    text = text.strip()
    if text.startswith("{"):
        return json.loads(text)

    # Brace search fallback
    start = text.find("{")
    end = text.rfind("}")
    if start != -1 and end != -1:
        return json.loads(text[start:end + 1])

    raise ValueError("No se encontró JSON válido en la respuesta")


def analyze(files_info: list[dict]) -> dict:
    logger.info("PASO 1: Iniciando análisis profundo con Claude Opus…")
    content = _build_content_blocks(files_info)

    with client.messages.stream(
        model=MODEL_DEEP,
        max_tokens=8192,
        thinking={"type": "adaptive"},
        system="Eres un experto en licitaciones públicas españolas. Responde ÚNICAMENTE con JSON válido, sin texto adicional.",
        messages=[{"role": "user", "content": content}],
    ) as stream:
        msg = stream.get_final_message()

    raw = "".join(
        block.text for block in msg.content if hasattr(block, "text")
    )
    logger.info(f"PASO 1: Respuesta recibida ({len(raw)} chars). Extrayendo JSON…")

    analysis = _extract_json(raw)
    logger.info(
        "PASO 1: Análisis completado. Expediente: "
        + analysis.get("identificacion", {}).get("expediente", "desconocido")
    )
    return analysis
