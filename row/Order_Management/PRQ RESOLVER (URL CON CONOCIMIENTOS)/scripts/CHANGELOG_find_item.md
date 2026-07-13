## v2.0 (20/06/2026) — VERIFICADO con 3 catálogos oficiales

### Total items
- **v1.0:** ~80 items (mayormente estimados)
- **v2.0:** **334 items** extraídos directamente de los catálogos PDF oficiales

### Cambios principales

| Categoría | v1.0 | v2.0 |
|:--|:--|:--|
| Breast & Skeletal | 30 items | 31 items |
| GYN Surgical | 50 items | 53 items |
| Diagnostics | 50 items | 250 items |

### Nuevas categorías añadidas en v2.0
- **ThinPrep Processors** (Genesis, 5000, AutoLoader): 15 items
- **Genius Digital** (Imager, Review Station, IMS): 7 items
- **Panther Fusion** (assays + open access + accesorios): 50+ items
- **Transplant Solutions** (EBV, BKV, CMV quants): 8 items
- **Novodiag** (instruments + cartridges): 13 items
- **Tomcat** (sample prep): 5 items
- **Aptima Viral Load** (HIV, HCV, HBV quants): 9 items
- **Sample Collection Kits**: 15 items

### Casos de uso reales que ahora resuelve sin abrir PDFs

```bash
$ python find_item_v2.py EVIVA_0913-12T
{
  "found": true,
  "item_code": "EVIVA_0913-12T",
  "catalogue": "catalogo_breast.pdf",
  "division": "Breast & Skeletal",
  "description": "Petite Trocar 9G x 13cm x 12mm",
  "box_of": 5,
  "presentation": "Box of 5"
}

$ python find_item_v2.py 302929
{
  "found": true,
  "item_code": "302929",
  "catalogue": "catalogo_diagnostics.pdf",
  "division": "Diagnostics",
  "description": "Aptima HPV Assay Kit 100T",
  "box_of": 100
}

$ python find_item_v2.py NVD-CD-012
{
  "found": true,
  "item_code": "NVD-CD-012",
  "catalogue": "catalogo_diagnostics.pdf",
  "division": "Diagnostics",
  "description": "Novodiag C. difficile Cartridges",
  "box_of": 12
}
```

### Patrón de detección de división mejorado
- **Breast:** EVIVA_, ATEC, MP\d, TUMARK, TRIMARK, SMARK, BREV
- **Surgical:** RFC2010, NSV5, 60-, 40-, 50-, 10-, 20-, 30-, FLT-, OLK-, 52124, ASY-051xx, ASY-156xx
- **Diagnostics:** 70xxx, 71xxx, ASY-1xxxx, PRD-0xxxx, NVD-, MD-NAT, 302xxx, 303xxx, 105xxx, 504xxx, 902xxx, 903xxx, etc.

### Próximos pasos
1. Cada nuevo caso de PRQ debería verificarse contra este script primero
2. Si el ítem NO está en la BD interna → añadirlo (pequeña tarea de mantenimiento)
3. Revisar trimestralmente los catálogos para nuevos productos

---
*Generado: 20/06/2026*