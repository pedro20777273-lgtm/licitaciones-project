---
tipo: skill
tags: [quotes, bsh, gmc, docx, kam, presupuestos]
fuentes: [row/SKILL_hologic_quote_creation_bsh.md]
actualizado: 2026-07-14
---

# Skill Quote Creation BSH v1.0

## Propósito
Generar presupuestos (.docx + .pdf) de la división [BSH](../entidades/divisiones-hologic.md) a
partir de datos GMC (Global Management Console), usando el template del
[KAM](../entidades/kams.md) correspondiente. Cubre **Equipment Purchase** (4 columnas) e
**IBS Consumables** (5 columnas con EAN y presentación). Diagnostics (DX) queda para una skill
futura — gap en [mejoras](../mejoras.md).

## Flujo operativo
1. Analizar el GMC (nº, Sales Rep→template, cliente, contacto, garantía, ítems, FOC, comments).
2. Confirmar template con Pedro (checkpoint humano).
3. Informar comentarios del KAM. 4. Preguntar dirección si falta.
5. Generar .docx+.pdf (unpack XML → editar → pack → convertir → preview visual).
6. Trigger "envía el correo" → email con asunto `[GMC] — [Cliente] — [Versión]`.

## Reglas no negociables (selección)
- Equipment: **nunca precios individuales** (solo Total), 3 filas resumen Subtotal/IVA 21%/TOTAL,
  FOC con precio **en blanco**, excluir ítems `GMC_` e installation costs (internos), garantía
  SIEMPRE del GMC, eliminar "Dirección de entrega" y resaltados amarillos, **T&C intactos**.
- IBS: 5 columnas con EAN del Excel `CODIGOS_EAN_BREAST`, presentación "Caja de X uds",
  **sin filas de resumen**.
- Template Carlos Hernández es especial (filas resumen preexistentes — solo rellenar "€").

## Conocimiento acumulado
- **6 templates por KAM** con quirks documentados (bookmarks, grids, bCs vs b).
- Histórico de 17 quotes generados como referencia.
- Tabla de **errores comunes y soluciones** (7 patrones XML) — el mejor log de errores del arsenal
  junto a [PRQ Resolver](prq-resolver.md). Ver [patrón de diseño](../conceptos/patron-diseno-skills.md).

## Estado y recursos
🟢 v1.0 muy afinada. ⚠️ Los templates .doc de los KAMs y el Excel de EANs **no están en el repo**.
El email de trigger apunta a `pedro2777273@gmail.com` (¿typo por pedro20777273? verificar).

## Conexiones
- La quote es la base de la **oferta económica** del [ciclo](../conceptos/ciclo-vida-licitacion.md)
  y del [GMC/quote como fuente de verdad de precios](../conceptos/gmc-quote-bsa.md): de aquí salen
  los BSAs de Oracle cuya mala carga genera los PRQs de [PRQ Resolver](prq-resolver.md).
- Principio "editar, no regenerar" compartido con [DEUC](deuc.md) y [3.1](requerimientos-documentacion.md).
