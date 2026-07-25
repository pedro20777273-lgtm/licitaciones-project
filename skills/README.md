# skills/ — arsenal ejecutable en formato Agent Skills

Migración de las skills de Pedro desde documentos sueltos (SharePoint/OneDrive) a **una carpeta
por skill** con `SKILL.md` + `references/` + `scripts/` + `assets/`, versionada en git.
Contexto y análisis: ver [wiki/skills/mapa-skills.md](../wiki/skills/mapa-skills.md).

## Estado (2026-07-14)

| Skill | SKILL.md | Recursos | Ejecutable desde el repo |
|---|---|---|---|
| `verificador-ofertas/` | ✅ original | ✅ 3 references completas | ✅ (skill de análisis, no necesita scripts) |
| `prq-resolver/` | ✅ original | ✅ reason_codes + knowledge_base + bsa_vs_standalone + prompt · ✅ **find_item_v2.py extraído y probado** (334 ítems) | 🟡 falta: manual PDF y catálogos (en `row/`), acceso Oracle/IBR |
| `deuc/` | ✅ original (v4.0) | ✅ **rellenar_deuc.py RECONSTRUIDO** + JSON ejemplo | 🟡 validar con un ESPDResponse real antes de producción |
| `analisis-pliegos/` | 🟡 **RECONSTRUIDO** desde la plantilla | ✅ plantilla Excel | 🟡 sustituir por el original si aparece |
| `screening-tc-pliegos/` | ✅ original | 🟡 comparison-dimensions RECONSTRUIDO · 🔴 hologic-tcs/ vacío (0 T&C) | 🟡 funciona en modo GRIS |
| `check-aval/` | ✅ original (v1.1) | 🟡 contactos y log inicializados · 🔴 0/17 modelos CCAA | 🔴 necesita modelos oficiales |
| `requerimientos-documentacion/` | ✅ original | 🔴 faltan 3 plantillas .docx + 3 scripts + reglas_extraccion (ver assets/README) | 🔴 |
| `quote-creation-bsh/` | ✅ original (v1.0) | 🔴 faltan 6 templates .doc + Excel EAN (ver assets/README) | 🔴 |

## Regla de datos fijos
Todos los datos de empresa salen de **`_shared/datos_fijos_hologic.md`** (fuente única). No
duplicar en skills nuevas.

## Piezas reconstruidas
Los archivos marcados RECONSTRUIDO llevan aviso en cabecera: son reimplementaciones fieles a la
especificación disponible, **no** los originales. Al recuperar un original, sustituir y quitar el aviso.
