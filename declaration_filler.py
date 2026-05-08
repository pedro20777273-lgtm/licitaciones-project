import json
import logging
import re
from pathlib import Path

import anthropic
import fitz  # PyMuPDF
from docx import Document
from docx.shared import Pt

from config import ANTHROPIC_API_KEY, DATOS_EMPRESA, MODEL_FAST, TEMPLATES_DIR

logger = logging.getLogger(__name__)
client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)


# ── helpers ──────────────────────────────────────────────────────────────────

def _extract_page_text(pdf_path: str, page_num: int) -> str:
    try:
        doc = fitz.open(pdf_path)
        idx = max(0, page_num - 1)
        pages = [doc[i].get_text() for i in range(max(0, idx - 1), min(len(doc), idx + 3))]
        doc.close()
        return "\n".join(pages)
    except Exception as e:
        logger.warning(f"Error extrayendo página {page_num} de {pdf_path}: {e}")
        return ""


def _extract_docx_text(docx_path: str) -> str:
    doc = Document(docx_path)
    parts = [p.text for p in doc.paragraphs]
    for table in doc.tables:
        for row in table.rows:
            parts.append(" | ".join(cell.text for cell in row.cells))
    return "\n".join(line for line in parts if line.strip())


def _contract_context(analysis: dict) -> str:
    ident = analysis.get("identificacion", {})
    return (
        f"Expediente: {ident.get('expediente', 'N/A')}\n"
        f"Objeto: {ident.get('objeto', 'N/A')}\n"
        f"Órgano de contratación: {ident.get('organo_contratacion', 'N/A')}\n"
        f"Tipo de contrato: {ident.get('tipo_contrato', 'N/A')}\n"
        f"Presupuesto base (sin IVA): {ident.get('presupuesto_base', 'N/A')}\n"
        f"Valor estimado: {ident.get('valor_estimado', 'N/A')}\n"
        f"Duración: {ident.get('duracion', 'N/A')}\n"
    )


def _save_docx(filled_text: str, output_path: str, title: str) -> None:
    doc = Document()
    doc.add_heading(title, level=1)
    for line in filled_text.split("\n"):
        p = doc.add_paragraph(line)
        for run in p.runs:
            run.font.size = Pt(11)
    doc.save(output_path)


def _extract_json(text: str) -> dict:
    m = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", text, re.DOTALL)
    if m:
        return json.loads(m.group(1))
    text = text.strip()
    if text.startswith("{"):
        return json.loads(text)
    start, end = text.find("{"), text.rfind("}")
    if start != -1 and end != -1:
        return json.loads(text[start:end + 1])
    raise ValueError("No se encontró JSON en la respuesta")


# ── PASO 5a: declaraciones del propio pliego ─────────────────────────────────

def _fill_with_claude(template_text: str, campos: list[str], analysis: dict) -> str:
    prompt = (
        f"Eres un especialista en licitaciones públicas españolas.\n\n"
        f"DATOS DE LA EMPRESA:\n{json.dumps(DATOS_EMPRESA, ensure_ascii=False, indent=2)}\n\n"
        f"DATOS DEL CONTRATO:\n{_contract_context(analysis)}\n"
        f"CAMPOS A COMPLETAR:\n{json.dumps(campos, ensure_ascii=False)}\n\n"
        f"TEXTO ORIGINAL DE LA DECLARACIÓN:\n{template_text}\n\n"
        f"Devuelve el texto completo con todos los campos en blanco rellenados. "
        f"Mantén el formato original. Sin explicaciones adicionales."
    )
    with client.messages.stream(
        model=MODEL_FAST,
        max_tokens=4096,
        messages=[{"role": "user", "content": prompt}],
    ) as stream:
        msg = stream.get_final_message()
    return "".join(block.text for block in msg.content if hasattr(block, "text"))


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

        logger.info(f"PASO 5a: Rellenando '{nombre}' desde '{doc_origen}'…")

        template_text = ""
        pdf_path = file_map.get(doc_origen)
        if pdf_path and Path(pdf_path).suffix.lower() == ".pdf":
            template_text = _extract_page_text(pdf_path, pagina)
        if not template_text:
            logger.warning(f"PASO 5a: Sin texto para '{nombre}', usando descripción")
            template_text = decl.get("descripcion", nombre)

        try:
            filled = _fill_with_claude(template_text, campos, analysis)
        except Exception as e:
            logger.error(f"PASO 5a: Error rellenando '{nombre}': {e}")
            continue

        safe_name = re.sub(r'[^\w\-]', '_', nombre)[:60]
        docx_path = str(output_path / f"declaracion_{safe_name}.docx")
        try:
            _save_docx(filled, docx_path, nombre)
            logger.info(f"PASO 5a: Guardado {docx_path}")
            results.append(docx_path)
        except Exception as e:
            logger.error(f"PASO 5a: Error guardando DOCX '{nombre}': {e}")

    return results


# ── PASO 5b: plantillas genéricas del usuario ─────────────────────────────────

def fill_from_templates(analysis: dict, output_dir: str) -> list[str]:
    """Rellena las plantillas DOCX de templates/declaraciones/ que apliquen al contrato."""
    templates_dir = TEMPLATES_DIR / "declaraciones"
    template_files = sorted(templates_dir.glob("*.docx"))
    if not template_files:
        logger.info("PASO 5b: No hay plantillas en templates/declaraciones/ — omitiendo")
        return []

    logger.info(f"PASO 5b: Evaluando {len(template_files)} plantillas genéricas…")

    # Build template list for Claude (filename + text content)
    templates_payload = []
    for tpl in template_files:
        try:
            text = _extract_docx_text(str(tpl))
            templates_payload.append({"filename": tpl.name, "contenido": text[:3000]})
        except Exception as e:
            logger.warning(f"PASO 5b: No se pudo leer '{tpl.name}': {e}")

    if not templates_payload:
        return []

    prompt = (
        f"Eres un especialista en licitaciones públicas españolas.\n\n"
        f"DATOS DEL CONTRATO:\n{_contract_context(analysis)}\n"
        f"DATOS DE LA EMPRESA:\n{json.dumps(DATOS_EMPRESA, ensure_ascii=False, indent=2)}\n\n"
        f"PLANTILLAS DISPONIBLES:\n{json.dumps(templates_payload, ensure_ascii=False, indent=2)}\n\n"
        f"Para cada plantilla determina si es aplicable a este contrato. "
        f"Si aplica, rellena TODOS los campos en blanco con los datos correctos de la empresa y del contrato. "
        f"Devuelve ÚNICAMENTE este JSON sin texto adicional:\n"
        f'{{"plantillas": ['
        f'{{"filename": "nombre.docx", "aplicable": true, "razon": "breve motivo", "texto_rellenado": "texto completo"}}'
        f']}}'
    )

    with client.messages.stream(
        model=MODEL_FAST,
        max_tokens=8192,
        messages=[{"role": "user", "content": prompt}],
    ) as stream:
        msg = stream.get_final_message()

    raw = "".join(block.text for block in msg.content if hasattr(block, "text"))

    try:
        data = _extract_json(raw)
    except Exception as e:
        logger.error(f"PASO 5b: Error parseando respuesta de Claude: {e}")
        return []

    output_path = Path(output_dir)
    results = []

    for item in data.get("plantillas", []):
        fname = item.get("filename", "")
        if not item.get("aplicable"):
            logger.info(f"PASO 5b: '{fname}' → no aplica ({item.get('razon', '')})")
            continue

        filled_text = item.get("texto_rellenado", "")
        if not filled_text:
            continue

        # Try to preserve the original DOCX structure, just update text
        tpl_path = templates_dir / fname
        safe_name = re.sub(r'[^\w\-]', '_', Path(fname).stem)[:60]
        out_path = str(output_path / f"plantilla_{safe_name}_rellenada.docx")

        try:
            if tpl_path.exists():
                _fill_docx_preserving_format(str(tpl_path), filled_text, out_path)
            else:
                _save_docx(filled_text, out_path, Path(fname).stem)
            logger.info(f"PASO 5b: '{fname}' aplica → {out_path} ({item.get('razon', '')})")
            results.append(out_path)
        except Exception as e:
            logger.error(f"PASO 5b: Error guardando '{fname}': {e}")

    return results


def _fill_docx_preserving_format(template_path: str, filled_text: str, out_path: str) -> None:
    """Opens the original DOCX and replaces paragraph text keeping styles."""
    doc = Document(template_path)
    filled_lines = [l for l in filled_text.split("\n")]
    line_iter = iter(filled_lines)

    for para in doc.paragraphs:
        if not para.text.strip():
            continue
        new_line = next(line_iter, None)
        if new_line is None:
            break
        # Clear runs and set new text preserving first run's style
        if para.runs:
            style = para.runs[0]
            for run in para.runs:
                run.text = ""
            style.text = new_line
        else:
            para.text = new_line

    doc.save(out_path)
