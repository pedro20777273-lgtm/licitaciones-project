---
tipo: fuente
tags: [catalogo, fuentes, ingesta]
actualizado: 2026-07-14
---

# Catálogo de fuentes (`row/`) y estado de ingesta

| Archivo en `row/` | Qué es | Estado | Páginas wiki alimentadas |
|---|---|---|---|
| `SKILL_6.md` | Skill DEUC v4.0 | ✅ ingerido | [deuc](../skills/deuc.md), [deuc-espd](../conceptos/deuc-espd.md), [hologic-iberia](../entidades/hologic-iberia.md) |
| `SKILL_3_1.md` | Skill requerimientos de documentación | ✅ ingerido | [requerimientos-documentacion](../skills/requerimientos-documentacion.md), [garantia-definitiva-aval](../conceptos/garantia-definitiva-aval.md) |
| `SKILL_CHECK_AVAL_v1_1.md` | Skill verificación de avales v1.1 | ✅ ingerido | [check-aval](../skills/check-aval.md), [garantia-definitiva-aval](../conceptos/garantia-definitiva-aval.md) |
| `SKILL_A1_tc_vs_pliegos.md` | Skill screening T&C | ✅ ingerido | [screening-tc-pliegos](../skills/screening-tc-pliegos.md) |
| `SKILL_A2_analisis_de_pliegos.xlsx` | Plantilla Excel del análisis de pliegos (llegó como .md; es xlsx) | ⚠️ parcial — falta el SKILL.md | [analisis-pliegos](../skills/analisis-pliegos.md) |
| `SKILL_5.pdf` | PDF 3 págs, texto vectorizado (llegó como .md) | 🔴 **no ingerible** sin OCR | [skill-5-pendiente](../skills/skill-5-pendiente.md) |
| `SKILL_hologic_quote_creation_bsh.md` | Skill quotes BSH v1.0 (se subieron 2 copias idénticas; se conservó 1) | ✅ ingerido | [quote-creation-bsh](../skills/quote-creation-bsh.md) |
| `verificador-ofertas/` (SKILL.md + 3 references) | Skill verificador (llegó como ZIP `.txt`) | ✅ ingerido | [verificador-ofertas](../skills/verificador-ofertas.md), [contaminacion-sobres](../conceptos/contaminacion-sobres.md), [causas-exclusion](../conceptos/causas-exclusion.md) |
| `Order_Management/PRQ RESOLVER (URL CON CONOCIMIENTOS)/` | Skill PRQ v1.5 + reason codes v3 + guía + prompt + changelog script | ✅ ingerido | [prq-resolver](../skills/prq-resolver.md), [prq-reason-codes](../conceptos/prq-reason-codes.md), [patron-diseno-skills](../conceptos/patron-diseno-skills.md) |
| `Order_Management/PRQ RESOLVER (PROMPT DE INVOCACION)/` | Prompts de invocación (GUIA LOGICA duplica "Guia de logica"; Untitled.md es plantilla vacía) | ✅ ingerido | [prq-resolver](../skills/prq-resolver.md) |
| `Order_Management/PRQ RECURSOS/6. Price Queries (PRQs).md` | Manual oficial CC&T (Owens/Pinet, 10/2025) | ✅ ingerido | [prq-reason-codes](../conceptos/prq-reason-codes.md), [sistemas](../entidades/sistemas.md) |
| `Order_Management/PRQ RECURSOS/BSA vs Standalone...md` | Reglas de elección de acuerdo de precios | ✅ ingerido | [bsa-vs-standalone](../conceptos/bsa-vs-standalone.md) |
| `Order_Management/PRQ RECURSOS/` catálogos (Breast, Surgical, Diagnostics) | Catálogos de producto (96K/16K/69K) | 🟡 indexados, no leídos línea a línea (su contenido vive en `find_item_v2.py`, 334 ítems) | [divisiones-hologic](../entidades/divisiones-hologic.md) |
| `Order_Management/PRQ RECURSOS/Pending reason codes...md` | Excel oficial de reason codes (fuente del diccionario v3) | 🟡 cubierto vía diccionario v3 | [prq-reason-codes](../conceptos/prq-reason-codes.md) |
| `Order_Management/Recursos a consultar 2/PRQ_KNOWLEDGE_BASE (1).md` | KB por cuenta (10/07/2026) | ✅ ingerido | [cuentas-clave](../entidades/cuentas-clave.md), [kams](../entidades/kams.md) |
| `Order_Management/Recursos a consultar 2/PRQ_LOG_SEMANA28_2026 (4).md` | Log huddle semana 28 | ✅ ingerido | [cuentas-clave](../entidades/cuentas-clave.md), [gmc-quote-bsa](../conceptos/gmc-quote-bsa.md) |
| `Order_Management/Recursos a consultar 2/New CC&T Huddle tracker.md` | Export crudo del Excel del huddle (732 KB, mayormente celdas vacías) | 🟡 revisado por muestreo; bajo valor como texto | [prq-resolver](../skills/prq-resolver.md) (contexto huddle) |

## Convención para próximas ingestas
Depositar la fuente en `row/` (idealmente con la extensión correcta) y pedir «ingesta <archivo>».
Se actualizarán las páginas afectadas, este catálogo, el [index](../index.md) y el [log](../log.md).
