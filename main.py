import argparse
import logging
import re
import sys
from datetime import datetime
from pathlib import Path

from config import OUTPUT_DIR


def _setup_logging(log_path: str) -> None:
    fmt = "%(asctime)s  %(levelname)-8s  %(message)s"
    logging.basicConfig(
        level=logging.INFO,
        format=fmt,
        handlers=[
            logging.FileHandler(log_path, encoding="utf-8"),
            logging.StreamHandler(sys.stdout),
        ],
    )


def _safe_exp(analysis: dict) -> str:
    exp = analysis.get("identificacion", {}).get("expediente", "licitacion")
    return re.sub(r'[^\w\-]', '_', exp)[:60]


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Procesador automático de documentos de licitación — Hologic Iberia"
    )
    parser.add_argument("--carpeta", required=True, help="Ruta a la carpeta con los documentos PDF/DOCX")
    args = parser.parse_args()

    carpeta = args.carpeta
    if not Path(carpeta).is_dir():
        print(f"ERROR: La carpeta no existe: {carpeta}")
        sys.exit(1)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_path = str(OUTPUT_DIR / f"log_{timestamp}.txt")
    _setup_logging(log_path)
    logger = logging.getLogger(__name__)

    logger.info("=" * 60)
    logger.info("HOLOGIC IBERIA — Procesador de Licitaciones")
    logger.info(f"Carpeta: {carpeta}")
    logger.info("=" * 60)

    errors: list[str] = []
    files_info: list[dict] = []
    analysis: dict = {}
    output_dir: str = str(OUTPUT_DIR)
    attachments: list[str] = []

    # ── PASO 0: Conversión ──────────────────────────────────────────────────
    try:
        from converter import convert_folder
        files_info = convert_folder(carpeta)
        logger.info(f"PASO 0: {len(files_info)} archivos convertidos")
    except Exception as e:
        msg = f"PASO 0 FALLIDO: {e}"
        logger.error(msg)
        errors.append(msg)
        logger.error("Sin documentos no es posible continuar. Abortando.")
        sys.exit(1)

    # ── PASO 1: Análisis ────────────────────────────────────────────────────
    try:
        from analyzer import analyze
        analysis = analyze(files_info)

        safe_exp = _safe_exp(analysis)
        exp_dir = OUTPUT_DIR / safe_exp
        if exp_dir.exists():
            logger.warning(f"Ya existe el directorio de salida {exp_dir}. Saltando procesamiento.")
            sys.exit(0)
        exp_dir.mkdir(parents=True, exist_ok=True)
        output_dir = str(exp_dir)
        logger.info(f"PASO 1: OK. Directorio de salida: {output_dir}")
    except Exception as e:
        msg = f"PASO 1 FALLIDO: {e}"
        logger.error(msg)
        errors.append(msg)

    # ── PASO 2: Resumen + PDF ───────────────────────────────────────────────
    summary_pdf: str = ""
    try:
        from summarizer import generate_summary
        _, summary_pdf = generate_summary(analysis, files_info, output_dir)
        attachments.append(summary_pdf)
        logger.info(f"PASO 2: OK → {summary_pdf}")
    except Exception as e:
        msg = f"PASO 2 FALLIDO: {e}"
        logger.error(msg)
        errors.append(msg)

    # ── PASO 3: Excel ───────────────────────────────────────────────────────
    try:
        from excel_generator import generate_excel
        xlsx_path = generate_excel(analysis, output_dir)
        attachments.append(xlsx_path)
        logger.info(f"PASO 3: OK → {xlsx_path}")
    except Exception as e:
        msg = f"PASO 3 FALLIDO: {e}"
        logger.error(msg)
        errors.append(msg)

    # ── PASO 4: Resaltado PDF ───────────────────────────────────────────────
    try:
        from pdf_highlighter import highlight_pdfs
        pdf_paths = [
            info["path"] for info in files_info
            if info["path"].endswith(".pdf") and not info.get("native_pdf_b64")
        ]
        # Also include image-heavy PDFs for highlighting
        pdf_paths += [
            info["path"] for info in files_info
            if info["path"].endswith(".pdf") and info.get("native_pdf_b64")
        ]
        pdf_paths = list(dict.fromkeys(pdf_paths))  # deduplicate preserving order

        frases = analysis.get("frases_clave", [])
        highlighted = highlight_pdfs(pdf_paths, frases, output_dir)
        attachments.extend(highlighted)
        logger.info(f"PASO 4: OK → {len(highlighted)} PDFs resaltados")
    except Exception as e:
        msg = f"PASO 4 FALLIDO: {e}"
        logger.error(msg)
        errors.append(msg)

    # ── PASO 5a: Declaraciones del propio pliego ────────────────────────────
    try:
        from declaration_filler import fill_declarations, fill_from_templates
        declaraciones = analysis.get("declaraciones_a_rellenar", [])
        file_map = {info["name"]: info["path"] for info in files_info}
        if declaraciones:
            docx_files = fill_declarations(declaraciones, file_map, analysis, output_dir)
            attachments.extend(docx_files)
            logger.info(f"PASO 5a: OK → {len(docx_files)} declaraciones del pliego")
        else:
            logger.info("PASO 5a: Sin declaraciones explícitas en el pliego")
    except Exception as e:
        msg = f"PASO 5a FALLIDO: {e}"
        logger.error(msg)
        errors.append(msg)

    # ── PASO 5b: Plantillas genéricas del usuario ───────────────────────────
    try:
        from declaration_filler import fill_from_templates
        tpl_files = fill_from_templates(analysis, output_dir)
        attachments.extend(tpl_files)
        if tpl_files:
            logger.info(f"PASO 5b: OK → {len(tpl_files)} plantillas genéricas rellenadas")
    except Exception as e:
        msg = f"PASO 5b FALLIDO: {e}"
        logger.error(msg)
        errors.append(msg)

    # ── PASO 6: Email ───────────────────────────────────────────────────────
    attachments.append(log_path)
    try:
        from email_sender import send_results
        send_results(analysis, attachments)
        logger.info("PASO 6: OK → Email enviado")
    except Exception as e:
        msg = f"PASO 6 FALLIDO: {e}"
        logger.error(msg)
        errors.append(msg)

    # ── Resumen final ───────────────────────────────────────────────────────
    logger.info("=" * 60)
    if errors:
        logger.warning(f"Proceso completado CON {len(errors)} ERROR(ES):")
        for err in errors:
            logger.warning(f"  • {err}")
    else:
        logger.info("Proceso completado SIN errores.")
    logger.info(f"Log guardado en: {log_path}")
    logger.info("=" * 60)


if __name__ == "__main__":
    main()
