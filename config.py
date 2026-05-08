import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).parent
PROMPTS_DIR = BASE_DIR / "prompts"
OUTPUT_DIR = BASE_DIR / "output"
OUTPUT_DIR.mkdir(exist_ok=True)

ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")
GMAIL_USER = os.environ.get("GMAIL_USER", "morontap4@gmail.com")
GMAIL_APP_PASSWORD = os.environ.get("GMAIL_APP_PASSWORD", "")
DELIVERY_EMAIL = "pedro.moronta@hologic.com"

MODEL_DEEP = "claude-opus-4-6"
MODEL_FAST = "claude-sonnet-4-6"

EMPRESA = "HOLOGIC IBERIA, S.L.U."
CIF = "B83279331"
DOMICILIO = "C/ Arequipa nº1, Esc. 2, 3º - 28043 Madrid"
APODERADO = "Sergio Sánchez de Torres"
DNI_APODERADO = "01930648M"
NOTARIO = "D. Javier García Ruiz"
FECHA_PODER = "25/10/2022"
PROTOCOLO = "3.340"
REGISTRO_MERCANTIL = "Barcelona / Tomo 34.833 / Folio 177 / Hoja B-251465 / Inscripción 2"

DATOS_EMPRESA = {
    "empresa": EMPRESA,
    "cif": CIF,
    "domicilio": DOMICILIO,
    "apoderado": APODERADO,
    "dni_apoderado": DNI_APODERADO,
    "notario": NOTARIO,
    "fecha_poder": FECHA_PODER,
    "protocolo": PROTOCOLO,
    "registro_mercantil": REGISTRO_MERCANTIL,
}

TEXT_DENSITY_THRESHOLD = 100  # avg chars/page below this → image-heavy PDF
