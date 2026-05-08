import json
import logging
import re
from pathlib import Path

import anthropic
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.table import Table, TableStyleInfo

from config import ANTHROPIC_API_KEY, MODEL_FAST, PROMPTS_DIR, TEMPLATES_DIR

logger = logging.getLogger(__name__)
client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

HEADER_FILL = PatternFill(start_color="1F3864", end_color="1F3864", fill_type="solid")
HEADER_FONT = Font(name="Arial", size=10, bold=True, color="FFFFFF")
CELL_FONT = Font(name="Arial", size=10)
CRITICAL_FONT = Font(name="Arial", size=10, color="FF0000")
WRAP = Alignment(wrap_text=True, vertical="top")


def _load_prompt() -> str:
    return (PROMPTS_DIR / "excel.txt").read_text(encoding="utf-8")


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
    raise ValueError("No se encontró JSON válido en la respuesta de Excel")


def _call_claude(analysis: dict) -> dict:
    prompt = (
        f"ANÁLISIS JSON:\n```json\n{json.dumps(analysis, ensure_ascii=False, indent=2)}\n```\n\n"
        + _load_prompt()
    )
    with client.messages.stream(
        model=MODEL_FAST,
        max_tokens=8192,
        messages=[{"role": "user", "content": prompt}],
    ) as stream:
        msg = stream.get_final_message()
    raw = "".join(block.text for block in msg.content if hasattr(block, "text"))
    return _extract_json(raw)


def _unique_table_name(wb: openpyxl.Workbook, base: str) -> str:
    existing = set()
    for ws in wb.worksheets:
        for tbl in ws.tables.values():
            existing.add(tbl.displayName)
    name = base[:20]
    if name not in existing:
        return name
    i = 2
    while f"{name}_{i}" in existing:
        i += 1
    return f"{name}_{i}"


def _write_sheet(wb: openpyxl.Workbook, sheet_data: dict) -> None:
    name = sheet_data["nombre"][:31]
    # Avoid duplicate sheet names
    base_name = name
    suffix = 2
    while name in [ws.title for ws in wb.worksheets]:
        name = f"{base_name[:28]}_{suffix}"
        suffix += 1
    ws = wb.create_sheet(title=name)
    filas = sheet_data.get("filas", [])

    ws.append(["Campo", "Detalle"])
    header_row = ws[1]
    for cell in header_row:
        cell.font = HEADER_FONT
        cell.fill = HEADER_FILL
        cell.alignment = WRAP

    for row_data in filas:
        campo = str(row_data.get("campo", ""))
        detalle = str(row_data.get("detalle", ""))
        es_critico = bool(row_data.get("es_critico", False))
        ws.append([campo, detalle])
        row_idx = ws.max_row
        font = CRITICAL_FONT if es_critico else CELL_FONT
        for col in (1, 2):
            cell = ws.cell(row=row_idx, column=col)
            cell.font = font
            cell.alignment = WRAP

    # Table style
    if ws.max_row > 1:
        table_ref = f"A1:{get_column_letter(2)}{ws.max_row}"
        tbl_name = _unique_table_name(wb, f"Tabla_{name.replace(' ', '_')}")
        table = Table(displayName=tbl_name, ref=table_ref)
        table.tableStyleInfo = TableStyleInfo(
            name="TableStyleMedium2",
            showFirstColumn=False,
            showLastColumn=False,
            showRowStripes=True,
            showColumnStripes=False,
        )
        ws.add_table(table)

    ws.column_dimensions["A"].width = 35
    ws.column_dimensions["B"].width = 100
    ws.row_dimensions[1].height = 20


def _load_base_workbook() -> openpyxl.Workbook | None:
    """Returns the user's Excel template if it exists, else None."""
    tpl = TEMPLATES_DIR / "excel" / "plantilla.xlsx"
    if tpl.exists():
        logger.info(f"PASO 3: Usando plantilla Excel base: {tpl}")
        return openpyxl.load_workbook(str(tpl))
    return None


def generate_excel(analysis: dict, output_dir: str) -> str:
    logger.info("PASO 3: Generando Excel con Claude Sonnet…")
    excel_data = _call_claude(analysis)
    logger.info(f"PASO 3: Datos recibidos ({len(excel_data.get('hojas', []))} hojas). Construyendo Excel…")

    wb = _load_base_workbook()
    if wb is None:
        wb = openpyxl.Workbook()
        wb.remove(wb.active)
    # If template was loaded, generated sheets are appended after existing ones

    for sheet_data in excel_data.get("hojas", []):
        try:
            _write_sheet(wb, sheet_data)
        except Exception as e:
            logger.warning(f"PASO 3: Error en hoja '{sheet_data.get('nombre')}': {e}")

    expediente = analysis.get("identificacion", {}).get("expediente", "licitacion")
    safe_exp = re.sub(r'[^\w\-]', '_', expediente)[:50]
    xlsx_path = str(Path(output_dir) / f"seguimiento_{safe_exp}.xlsx")
    wb.save(xlsx_path)
    logger.info(f"PASO 3: Excel guardado en {xlsx_path}")
    return xlsx_path
