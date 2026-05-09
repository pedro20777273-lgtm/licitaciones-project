import base64
import logging
from pathlib import Path

import fitz  # PyMuPDF

from config import TEXT_DENSITY_THRESHOLD

logger = logging.getLogger(__name__)


def _is_image_heavy(pdf_path: str) -> bool:
    doc = fitz.open(pdf_path)
    total_chars = sum(len(page.get_text()) for page in doc)
    avg_chars = total_chars / max(len(doc), 1)
    doc.close()
    return avg_chars < TEXT_DENSITY_THRESHOLD


def _to_base64(path: str) -> str:
    with open(path, "rb") as f:
        return base64.standard_b64encode(f.read()).decode("utf-8")


def _convert_with_markitdown(path: str) -> str:
    from markitdown import MarkItDown
    return MarkItDown().convert(path).text_content


def convert_file(path: str) -> dict:
    p = Path(path)
    suffix = p.suffix.lower()
    name = p.name
    result = {
        "name": name,
        "path": str(p),
        "content_md": None,
        "native_pdf_b64": None,
    }

    if suffix == ".pdf":
        if _is_image_heavy(path):
            logger.info(f"{name}: imagen-denso → enviando como PDF nativo")
            result["native_pdf_b64"] = _to_base64(path)
        else:
            try:
                result["content_md"] = _convert_with_markitdown(path)
                logger.info(f"{name}: convertido a Markdown ({len(result['content_md'])} chars)")
            except Exception as e:
                logger.warning(f"{name}: markitdown falló ({e}), usando PDF nativo como fallback")
                result["native_pdf_b64"] = _to_base64(path)
    elif suffix in (".docx", ".doc"):
        try:
            result["content_md"] = _convert_with_markitdown(path)
            logger.info(f"{name}: DOCX convertido a Markdown ({len(result['content_md'])} chars)")
        except Exception as e:
            # Fallback 1: python-docx (works for .docx even if markitdown fails)
            try:
                from docx import Document as _Doc
                doc = _Doc(path)
                text = "\n".join(p.text for p in doc.paragraphs if p.text.strip())
                if text:
                    result["content_md"] = text
                    logger.info(f"{name}: leído con python-docx ({len(text)} chars)")
                    return result
            except Exception:
                pass

            # Fallback 2: catdoc (binary .doc / Word 97-2003)
            try:
                import subprocess
                r = subprocess.run(["catdoc", path], capture_output=True, timeout=30)
                text = r.stdout.decode("latin-1", errors="replace").strip()
                if text:
                    result["content_md"] = text
                    logger.info(f"{name}: .doc leído con catdoc ({len(text)} chars)")
                    return result
            except Exception as e3:
                logger.debug(f"{name}: catdoc falló: {e3}")

            logger.error(f"{name}: no se pudo convertir .doc: {e}")
    else:
        logger.warning(f"{name}: formato no soportado ({suffix}), ignorando")

    return result


def convert_folder(folder: str) -> list[dict]:
    folder_path = Path(folder)
    files = sorted(
        [f for f in folder_path.iterdir() if f.suffix.lower() in (".pdf", ".docx", ".doc")]
    )
    if not files:
        raise ValueError(f"No se encontraron PDFs o DOCX en: {folder}")

    logger.info(f"Encontrados {len(files)} archivos en {folder}")
    results = []
    for f in files:
        try:
            info = convert_file(str(f))
            if info["content_md"] or info["native_pdf_b64"]:
                results.append(info)
        except Exception as e:
            logger.error(f"Error convirtiendo {f.name}: {e}")

    return results
