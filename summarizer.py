import json
import logging
import re
from pathlib import Path

import anthropic
import markdown as md_lib
from fpdf import FPDF, HTMLMixin

from config import ANTHROPIC_API_KEY, MODEL_DEEP, PROMPTS_DIR

logger = logging.getLogger(__name__)
client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)


def _load_prompt() -> str:
    return (PROMPTS_DIR / "resumen.txt").read_text(encoding="utf-8")


def _build_content_blocks(analysis: dict, files_info: list[dict]) -> list[dict]:
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

    if doc_blocks:
        doc_blocks[-1]["cache_control"] = {"type": "ephemeral"}
        blocks.extend(doc_blocks)

    blocks.append({
        "type": "text",
        "text": (
            f"ANÁLISIS JSON PREVIO:\n```json\n{json.dumps(analysis, ensure_ascii=False, indent=2)}\n```\n\n"
            + _load_prompt()
        ),
    })
    return blocks


class _PDF(FPDF, HTMLMixin):
    def header(self):
        self.set_font("Helvetica", "B", 9)
        self.set_text_color(40, 40, 40)
        self.cell(0, 6, "HOLOGIC IBERIA, S.L.U. — Resumen de Licitación", align="C")
        self.ln(4)

    def footer(self):
        self.set_y(-12)
        self.set_font("Helvetica", "", 8)
        self.set_text_color(120, 120, 120)
        self.cell(0, 6, f"Página {self.page_no()}", align="C")


def _markdown_to_pdf(markdown_text: str, output_path: str) -> None:
    html = md_lib.markdown(
        markdown_text,
        extensions=["tables", "fenced_code"],
    )
    # fpdf2 HTMLMixin requires simplified HTML
    html = re.sub(r"<pre><code[^>]*>(.*?)</code></pre>", r"<p>\1</p>", html, flags=re.DOTALL)

    pdf = _PDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Helvetica", size=10)
    pdf.write_html(html)
    pdf.output(output_path)


def generate_summary(analysis: dict, files_info: list[dict], output_dir: str) -> tuple[str, str]:
    logger.info("PASO 2: Generando resumen estructurado con Claude Opus…")
    content = _build_content_blocks(analysis, files_info)

    with client.messages.stream(
        model=MODEL_DEEP,
        max_tokens=16384,
        thinking={"type": "adaptive"},
        system="Eres un experto en licitaciones públicas españolas. Genera el resumen en Markdown según las instrucciones.",
        messages=[{"role": "user", "content": content}],
    ) as stream:
        msg = stream.get_final_message()

    markdown_text = "".join(
        block.text for block in msg.content if hasattr(block, "text")
    )
    logger.info(f"PASO 2: Resumen generado ({len(markdown_text)} chars). Convirtiendo a PDF…")

    expediente = analysis.get("identificacion", {}).get("expediente", "licitacion")
    safe_exp = re.sub(r'[^\w\-]', '_', expediente)[:50]

    md_path = str(Path(output_dir) / f"resumen_{safe_exp}.md")
    pdf_path = str(Path(output_dir) / f"resumen_{safe_exp}.pdf")

    Path(md_path).write_text(markdown_text, encoding="utf-8")

    try:
        _markdown_to_pdf(markdown_text, pdf_path)
        logger.info(f"PASO 2: PDF generado en {pdf_path}")
    except Exception as e:
        logger.error(f"PASO 2: Error generando PDF: {e}. Se conserva el Markdown.")
        pdf_path = md_path

    return markdown_text, pdf_path
