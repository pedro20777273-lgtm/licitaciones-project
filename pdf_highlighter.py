import logging
from pathlib import Path

import fitz  # PyMuPDF

logger = logging.getLogger(__name__)

HIGHLIGHT_COLOR = (0.8, 1.0, 0.0)  # #CCFF00


def _highlight_phrase(page: fitz.Page, phrase: str) -> int:
    hits = page.search_for(phrase)
    if not hits:
        # Fallback: try first 8 space-separated tokens
        tokens = phrase.split()[:8]
        if tokens:
            hits = page.search_for(" ".join(tokens))
    count = 0
    for rect in hits:
        annot = page.add_highlight_annot(rect)
        annot.set_colors(stroke=HIGHLIGHT_COLOR)
        annot.update()
        count += 1
    return count


def highlight_pdfs(
    pdf_paths: list[str],
    frases_clave: list[str],
    output_dir: str,
) -> list[str]:
    output_path = Path(output_dir)
    results = []

    for pdf_path in pdf_paths:
        p = Path(pdf_path)
        if not p.exists() or p.suffix.lower() != ".pdf":
            continue

        out_name = p.stem + "_RESALTADO.pdf"
        out_path = str(output_path / out_name)
        total_hits = 0

        try:
            doc = fitz.open(pdf_path)
            for phrase in frases_clave:
                if not phrase or len(phrase) < 5:
                    continue
                for page in doc:
                    total_hits += _highlight_phrase(page, phrase)
            doc.save(out_path, garbage=4, deflate=True)
            doc.close()
            logger.info(f"PASO 4: {p.name} → {out_name} ({total_hits} resaltados)")
            results.append(out_path)
        except Exception as e:
            logger.error(f"PASO 4: Error resaltando {p.name}: {e}")

    return results
