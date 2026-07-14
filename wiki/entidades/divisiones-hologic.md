---
tipo: entidad
tags: [divisiones, bsh, diagnostics, gss, catalogo]
fuentes: [row/SKILL_A1_tc_vs_pliegos.md, row/SKILL_hologic_quote_creation_bsh.md, row/Order_Management/]
actualizado: 2026-07-14
---

# Divisiones de Hologic (y cómo detectarlas por part number)

| División | Alias | Productos | Patrones de part number |
|---|---|---|---|
| **BSH** — Breast & Skeletal Health | Breast / Sk | Mamografía, densitometría (Horizon DXA), workstations (SecurView), biopsia (ATEC, Eviva, Brevera), marcadores (Tumark, SecurMark), MammoPad, agujas Somatex | `EVIVA_*`, `ATEC*`, `MMG-*`, `MP*`, `TUMARK-*`, `SMARK-*` |
| **DX** — Diagnostics | Cyto / Molecular | ThinPrep (PreservCyt, CytoLyt, filtros, tinciones), Panther/Fusion (Aptima HPV, HIV, HSV…), Genius Digital, Novodiag | `70*`, `71*`, `PRD-*`, `NVD-*`, `302*`, `303*`, `ASY-*` |
| **GSS** — GYN Surgical Solutions | Surgical | MyoSure, NovaSure, Fluent, Omni | `10-*`…`60-*`, `NSV5-*`, `FLT-*`, `RFC2010`, `815*` |

## Por qué importa la división
- Determina el **T&C** a cargar en [screening A1](../skills/screening-tc-pliegos.md).
- Determina el **template de quote** ([quote BSH](../skills/quote-creation-bsh.md) solo cubre BSH;
  DX pendiente).
- Determina el **catálogo** a cargar en [PRQ Resolver](../skills/prq-resolver.md) (lazy loading) y
  el [KAM](kams.md) al que escalar.
- Los catálogos oficiales (Breast 31 ítems clave, Surgical 53, Diagnostics 250) están en
  `row/Order_Management/PRQ RECURSOS/` y volcados en la BD de `find_item_v2.py`.

## Dato operativo
Los pedidos multi-división (ej. Parc Taulí: Breast+Surgical+Diagnostic en un mismo PO) usan
**BSAs distintos por división** — ver [cuentas clave](cuentas-clave.md).
