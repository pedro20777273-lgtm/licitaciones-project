import json
import logging
import re
from pathlib import Path

import anthropic
import fitz  # PyMuPDF
from docx import Document
from docx.shared import Pt

from config import ANTHROPIC_API_KEY, DATOS_EMPRESA, MODEL_FAST

logger = logging.getLogger(__name__)
client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)


def _extract_page_text(pdf_path: str, page_num: int) -> str:
    try:
        doc = fitz.open(pdf_path)
        # page_num may be 1-indexed or approximate; try ±1
        idx = max(0, page_num - 1)
        pages = []
        for i in range(max(0, idx - 1), min(len(doc), idx + 3)):
            pages.append(doc[i].get_text())
        doc.close()
        return "\n".join(pages)
    except Exception as e:
        logger.warning(f"Error extrayendo página {page_num} de {pdf_path}: {e}")
        return ""


def _fill_with_claude(template_text: str, campos: list[str], analysis: dict) -> str:
    prompt = (
        f"Eres un especialista en licitaciones públicas españolas. "
        f"Debes rellenar el siguiente formulario/declaración con los datos de la empresa licitadora.\n\n"
        f"DATOS DE LA EMPRESA:\n{json.dumps(DATOS_EMPRESA, ensure_ascii=False, indent=2)}\n\n"
        f"DATOS DEL CONTRATO (del análisis):\n"
        f"- Expediente: {analysis.get('identificacion', {}).get('expediente', 'N/A')}\n"
        f"- Objeto: {analysis.get('identificacion', {}).get('objeto', 'N/A')}\n"
        f"- Órgano: {analysis.get('identificacion', {}).get('organo_contratacion', 'N/A')}\n"
        f"- Presupuesto base: {analysis.get('identificacion', {}).get('presupuesto_base', 'N/A')}\n\n"
        f"CAMPOS A COMPLETAR:\n{json.dumps(campos, ensure_ascii=False)}\n\n"
        f"TEXTO ORIGINAL DE LA DECLARACIÓN:\n{template_text}\n\n"
        f"INSTRUCCIÓN: Devuelve el texto completo de la declaración con todos los campos en blanco "
        f"rellenados con los datos correctos de la empresa. "
        f"Mantén el formato original. Solo devuelve el texto rellenado, sin explicaciones adicionales."
    )

    with client.messages.stream(
        model=MODEL_FAST,
        max_tokens=4096,
        messages=[{"role": "user", "content": prompt}],
    ) as stream:
        msg = stream.get_final_message()

    return "".join(block.text for block in msg.content if hasattr(block, "text"))


def _save_docx(filled_text: str, output_path: str, title: str) -> None:
    doc = Document()
    doc.add_heading(title, level=1)
    for line in filled_text.split("\n"):
        p = doc.add_paragraph(line)
        for run in p.runs:
            run.font.size = Pt(11)
    doc.save(output_path)


def fill_declarations(
    declaraciones: list[dict],
    file_map: dict,
    analysis: dict,
    output_dir: str,
) -> list[str]:
    output_path = Path(output_dir)
    results = []

    for decl in declaraciones:
        nombre = decl.get("nombre", "declaracion")
        doc_origen = decl.get("documento_origen", "")
        pagina = int(decl.get("pagina", 1) or 1)
        campos = decl.get("campos_a_rellenar", [])

        logger.info(f"PASO 5: Rellenando '{nombre}' desde '{doc_origen}'…")

        template_text = ""
        pdf_path = file_map.get(doc_origen)
        if pdf_path and Path(pdf_path).suffix.lower() == ".pdf":
            template_text = _extract_page_text(pdf_path, pagina)

        if not template_text:
            logger.warning(f"PASO 5: No se pudo extraer texto para '{nombre}', usando descripción")
            template_text = decl.get("descripcion", nombre)

        try:
            filled = _fill_with_claude(template_text, campos, analysis)
        except Exception as e:
            logger.error(f"PASO 5: Error rellenando '{nombre}': {e}")
            continue

        safe_name = re.sub(r'[^\w\-]', '_', nombre)[:60]
        docx_path = str(output_path / f"declaracion_{safe_name}.docx")
        try:
            _save_docx(filled, docx_path, nombre)
            logger.info(f"PASO 5: Guardado {docx_path}")
            results.append(docx_path)
        except Exception as e:
            logger.error(f"PASO 5: Error guardando DOCX '{nombre}': {e}")

    return results
