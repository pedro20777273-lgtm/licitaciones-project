# Assets de la skill requerimientos-documentacion — INVENTARIO DE FALTANTES ⚠️

SKILL.md referencia estos archivos que **no llegaron al repo** (viven en OneDrive/entorno original).
Sin ellos la skill no es ejecutable desde aquí. Traer cuando sea posible:

| Archivo | Qué es |
|---|---|
| `plantilla_indice.docx` | Índice de documentación (Proxima Nova, pie azul #0F206C) |
| `plantilla_aval.docx` | Ficha base de solicitud de aval bancario |
| `plantilla_declaracion.docx` | Declaración responsable genérica (firma S. Sánchez de Torres) |
| `rolece_hologic.pdf` | Certificado ROLECE vigente de referencia |
| `../references/datos_fijos_hologic.md` | → **cubierto**: usar `skills/_shared/datos_fijos_hologic.md` |
| `../references/reglas_extraccion.md` | Reglas de extracción por entregable — **pendiente** |
| `../scripts/rellenar_indice.py` | Rellena el índice clonando párrafos-plantilla |
| `../scripts/rellenar_aval.py` | Rellena la ficha de aval |
| `../scripts/rellenar_declaracion.py` | Genera declaraciones responsables |

Los scripts se pueden reconstruir (patrón: clonar párrafo-plantilla conservando `rPr`, como
documenta SKILL.md), pero **solo tiene sentido con las plantillas .docx reales delante** — sin
ellas no hay contra qué validar el formato.
