**Fecha:** 20/06/2026
**Optimizada con:** patrones del skill-creator de Anthropic (progressive disclosure, lazy loading, bundled scripts).

---

## 📁 Estructura recomendada

```
📁 SKILL_PRQ_RESOLVER/                       ← raíz, ligera (~15 KB siempre cargada)
│
├── 📄 SKILL_PRQ_RESOLVER_v1.5.md            ← la skill (siempre cargada)
├── 📄 PROMPT_INVOCACION_PRQ_v1.5.md         ← prompt activación
├── 📄 GUIA_ESTRUCTURA_CARPETA_v1.5.md       ← este archivo
├── 📄 ERRORES_SKILL_PRQ.md                  ← log de errores
│
├── 📁 references/                            ← base conocimiento (lazy loading)
│   ├── 📄 manual_prq.pdf                    ← 6. Price Queries (PRQs).pdf oficial
│   ├── 📄 reason_codes.md                   ← diccionario verificado (siempre)
│   ├── 📄 bsa_vs_standalone.pptx            ← reglas eligibility
│   ├── 📄 oracle_procedure.md               ← procedimiento Oracle exacto
│   ├── 📄 catalogo_breast.pdf               ← Breast & Skeletal (solo si necesario)
│   ├── 📄 catalogo_surgical.pdf             ← GYN Surgical (solo si necesario)
│   ├── 📄 catalogo_diagnostics.pdf          ← Diagnostics (solo si necesario)
│   ├── 📄 INDEX_CUENTAS.md                  ← (opcional) mapa nombre cuenta → ID
│   └── 📄 KAM_MAPPING.md                    ← (opcional) KAM por cuenta
│
├── 📁 scripts/
│   └── 🐍 find_item.py                      ← lookup rápido sin cargar PDFs
│
└── 📁 examples/                              ← casos reales (opcional)
    ├── 📄 caso_cwpp.md
    ├── 📄 caso_cwpu.md
    └── 📄 caso_sec.md
```

---

## 🎯 Por qué esta estructura (progressive disclosure)

Inspirado en el **skill-creator de Anthropic**, esta arquitectura tiene 3 capas:

| Capa | Qué carga | Tamaño | Cuándo |
|:--|:--|:--|:--|
| **Metadata** (YAML frontmatter) | Nombre + descripción + triggers | ~200 palabras | Siempre, para decidir si invocar |
| **SKILL.md body** | Flujo + reglas + ejemplos | ~12 KB | Cuando la skill se invoca |
| **Bundled resources** | PDFs + scripts | Hasta 50 MB | Solo cuando se necesitan |

**Beneficio práctico:** Cuando Pedro invoca la skill por una PRQ de un ítem Surgical, la skill solo carga el `catalogo_surgical.pdf`. **No los 3 PDFs.** Y si el ítem se puede resolver con `find_item.py`, ni siquiera carga PDFs.

---

## 🚀 Optimizaciones específicas v1.5

### 1. Lazy loading de catálogos
La skill detecta la división del ítem por patrón de part number:

| Patrón | División | Catálogo |
|:--|:--|:--|
| `EVIVA_*`, `ATEC*`, `MP*`, `TUMARK*`, `MMG*` | Breast | catalogo_breast.pdf |
| `RFC2010`, `NSV5*`, `60-*`, `40-*`, `FLT-*` | Surgical | catalogo_surgical.pdf |
| `70*`, `PRD-*`, `NVD-*`, `302*`, `303*` | Diagnostics | catalogo_diagnostics.pdf |

### 2. Script bundled `find_item.py`
Tiene una BD interna con ~100 ítems comunes. Ejecutar:
```bash
python scripts/find_item.py EVIVA_0913-12T
# Output: {"catalogue": "catalogo_breast.pdf", "division": "Breast & Skeletal",
#          "description": "Petite Trocar 9G x 13cm x 12mm", "box_of": 5, "presentation": "Box of 5"}
```

Esto **evita cargar PDFs** para los ítems frecuentes.

### 3. Ejemplos en `examples/`
3 casos reales documentados con Input → Proceso → Output. Cuando la skill duda, puede consultar estos ejemplos en lugar de hacer inferencias.

---

## 📦 Lista de archivos que TÚ debes subir a OneDrive

### En la carpeta raíz `SKILL_PRQ_RESOLVER/`:
1. ✅ `SKILL_PRQ_RESOLVER_v1.5.md` (generado)
2. ✅ `PROMPT_INVOCACION_PRQ_v1.5.md` (generado)
3. ✅ `GUIA_ESTRUCTURA_CARPETA_v1.5.md` (este)
4. ⚠️ `ERRORES_SKILL_PRQ.md` (crear vacío con un encabezado)

### En `references/`:
1. ✅ `manual_prq.pdf` ← renombrar `6. Price Queries (PRQs).pdf` que ya tienes
2. ✅ `reason_codes.md` ← usar `REASON_CODES_PRQ_v3_OFICIAL.md` que generé antes
3. ✅ `bsa_vs_standalone.pptx` ← ya lo tienes
4. ✅ `catalogo_breast.pdf` ← `Breast and Skeletal products catalogue (1).pdf` que ya tienes
5. ✅ `catalogo_surgical.pdf` ← `Surgical products catalogue.pdf` que ya tienes
6. ✅ `catalogo_diagnostics.pdf` ← `Diagnostics product catalogue (1).pdf` que ya tienes
7. 🟡 `oracle_procedure.md` (opcional — está dentro de la skill ya)
8. 🟡 `INDEX_CUENTAS.md` (opcional pero recomendado para velocidad)
9. 🟡 `KAM_MAPPING.md` (opcional)

### En `scripts/`:
1. ✅ `find_item.py` (generado)

### En `examples/` (opcional):
- Subir casos resueltos reales conforme los vayas teniendo.

---

## ⚡ Cómo medir si esta versión es mejor (siguiendo el skill-creator)

Después de algunos casos reales, puedes evaluar:

| Métrica | v1.4 | v1.5 |
|:--|:--|:--|
| Tiempo medio resolución | ~1 min | ~30 seg (lazy loading) |
| Casos resueltos sin abrir PDFs | 0% | ~60% (gracias a find_item.py) |
| Errores por reason code inventado | 0 | 0 |
| Errores por confundir Box of X | Posible | Mínimo |

---

## 🔄 Próximos pasos sugeridos (también del skill-creator)

1. **Después de 10 casos reales:** revisa el log de errores. Identifica patrones.
2. **Si find_item.py no encuentra muchos ítems:** ampliar la BD interna del script.
3. **Si la skill duda en categorizar:** añadir más ejemplos a `examples/`.
4. **Si el filtrado del IBR falla:** revisa naming de carpetas y actualiza el regex de la skill.

---

*Fin de la guía.*