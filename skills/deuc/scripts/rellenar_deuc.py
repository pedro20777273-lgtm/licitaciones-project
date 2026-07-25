#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
rellenar_deuc.py — Rellena el DEUC (ESPDResponse) de Hologic Iberia.

⚠️ RECONSTRUCCIÓN v4.0-r1 (2026-07-14): el script original no llegó al repositorio.
Este es una reimplementación fiel de la especificación de SKILL.md (v4.0):
  - Parte del ESPDResponse EXPORTADO DEL VISOR (visor.registrodelicitadores.gob.es).
  - Edita QUIRÚRGICAMENTE a nivel de texto: no re-serializa el XML, no toca
    estructura, namespaces, UUIDs ni orden. Solo sustituye los huecos "." que el
    visor deja en los datos de empresa y firmante.
  - VALIDAR con un ESPDResponse real antes de usar en producción; ante cualquier
    rechazo del visor, seguir la sección DEPURACIÓN de SKILL.md.

Uso:
    python3 rellenar_deuc.py response_visor.xml RESPONSE_<EXPEDIENTE>.xml [--datos datos_licitacion.json]
"""

import json
import re
import sys
import unicodedata
from xml.dom import minidom

# ── Datos fijos de Hologic (fuente: ROLECE — ver skills/_shared/datos_fijos_hologic.md) ──
DATOS_FIJOS = {
    # localname del elemento XML → valor a escribir cuando su contenido es "."
    "Name": "HOLOGIC IBERIA, S.L.U.",
    "RegistrationName": "HOLOGIC IBERIA, S.L.U.",
    "CompanyID": "B83279331",
    "WebsiteURI": "https://www.hologic.com",
    "ElectronicMail": "concursos@hologic.com",
    "Telephone": "+34 913446990",
    "StreetName": "CALLE AREQUIPA Nº 1, PLANTA 3, ESC. 2,3 Y 4, EDIFICIO MAR DE CRISTAL",
    "CityName": "MADRID",
    "PostalZone": "28043",
    # Apoderado (representante). NUNCA inventar fecha/lugar de nacimiento:
    # solo se rellenan si vienen en el JSON (rep_birthdate / rep_birthplace).
    "FirstName": "SERGIO",
    "FamilyName": "SÁNCHEZ DE TORRES",
    "Position": "Apoderado",
    "RoleDescription": "Apoderado",
}

PLACEHOLDER = "."


def leer(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def localname(tag):
    return tag.split(":")[-1]


def texto_elemento(xml, nombre):
    """Primer contenido de texto de un elemento por localname (best-effort, solo lectura)."""
    m = re.search(r"<[\w-]*:?%s(?:\s[^>]*)?>([^<]+)</[\w-]*:?%s>" % (nombre, nombre), xml)
    return m.group(1).strip() if m else None


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if len(args) < 2:
        print(__doc__)
        sys.exit(1)
    entrada, salida = args[0], args[1]
    datos = {}
    if "--datos" in sys.argv:
        datos_path = sys.argv[sys.argv.index("--datos") + 1]
        with open(datos_path, "r", encoding="utf-8") as f:
            datos = json.load(f)

    xml = leer(entrada)

    # ── PASO 1: verificar que el input es un ESPDResponse ──
    m_root = re.search(r"<\s*([\w-]+:)?(\w+)[\s>]", xml.lstrip().lstrip("﻿").split("?>")[-1])
    raiz = None
    for m in re.finditer(r"<([\w-]+:)?(\w+)[\s>]", xml):
        if m.group(2) not in ("xml",):
            raiz = m.group(2)
            break
    if raiz != "ESPDResponse":
        print(f"❌ ABORTADO: la raíz del XML es <{raiz}>, no un ESPDResponse.")
        print("   Importa el ESPDRequest del órgano en el visor como operador económico")
        print("   y exporta el documento como Response. Ese XML es el input correcto.")
        sys.exit(2)

    organo = texto_elemento(xml, "ContractingPartyName") or texto_elemento(xml, "PartyName") or "?"
    expediente_xml = texto_elemento(xml, "ContractFolderID") or "?"
    n_criterios = len(re.findall(r"<[\w-]+:?Criterion[\s>]", xml)) or len(
        re.findall(r"TenderingCriterion[\s>]", xml)
    )
    print(f"✔ ESPDResponse detectado · Órgano: {organo} · Expediente: {expediente_xml} · Criterios: {n_criterios}")
    if datos.get("expediente"):
        print(f"  Expediente (JSON): {datos['expediente']} · Órgano (JSON): {datos.get('organo','—')}"
              f" · Lotes: {datos.get('lotes','—')}")

    # ── PASO 2: rellenar los huecos "." SIN tocar estructura ──
    mapa = dict(DATOS_FIJOS)
    if datos.get("rep_birthdate"):
        mapa["BirthDate"] = datos["rep_birthdate"]
    if datos.get("rep_birthplace"):
        mapa["BirthplaceName"] = datos["rep_birthplace"]

    sustituidos, sin_mapear = [], []

    def reemplazo(m):
        pre, tag, contenido, post = m.group(1), m.group(2), m.group(3), m.group(4)
        ln = localname(tag)
        if contenido.strip() == PLACEHOLDER:
            if ln in mapa:
                sustituidos.append(ln)
                return f"{pre}{mapa[ln]}{post}"
            sin_mapear.append(ln)
        return m.group(0)

    # <tag ...>.</tag> — mismo tag de cierre, contenido exactamente "."
    patron = re.compile(r"(<([\w:.-]+)(?:\s[^>]*)?>)(\s*\.\s*)(</\2>)")
    xml_nuevo = patron.sub(reemplazo, xml)

    with open(salida, "w", encoding="utf-8") as f:
        f.write(xml_nuevo)

    # ── PASO 3: control de calidad ──
    print("\n── CONTROL DE CALIDAD ──")
    try:
        minidom.parseString(xml_nuevo.encode("utf-8"))
        bien_formado = True
    except Exception as e:
        bien_formado = False
        print(f"   detalle error XML: {e}")
    restantes = len(patron.findall(xml_nuevo))
    checks = {
        "XML BIEN FORMADO": bien_formado,
        "Empresa OK (HOLOGIC + B83279331)": ("HOLOGIC" in xml_nuevo and "B83279331" in xml_nuevo),
        "Apoderado OK (SERGIO)": ("SERGIO" in unicodedata.normalize("NFC", xml_nuevo)),
        "SMEIndicator false": bool(re.search(r"SMEIndicator[^>]*>\s*false\s*<", xml_nuevo)),
        'Placeholders "." restantes = 0': (restantes == 0),
    }
    for k, v in checks.items():
        print(f"  {k}: {v}")
    print(f"\n  Campos rellenados ({len(sustituidos)}): {', '.join(sorted(set(sustituidos))) or '—'}")
    if sin_mapear:
        print(f"  ⚠️ Placeholders sin mapear ({len(sin_mapear)}): {', '.join(sorted(set(sin_mapear)))}")
        print("     Revisar a mano en el visor o ampliar DATOS_FIJOS.")
    if all(checks.values()):
        print(f"\n✅ {salida} listo. Reimportar en el visor, revisar en pantalla, generar el PDF")
        print("   oficial y firmarlo con la firma electrónica del apoderado antes de subirlo.")
    else:
        print("\n❌ QC con fallos — NO entregar. Ver sección DEPURACIÓN de SKILL.md.")
        sys.exit(3)


if __name__ == "__main__":
    main()
