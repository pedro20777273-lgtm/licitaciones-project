---
tipo: skill
tags: [licitaciones, pliegos, analisis, excel]
fuentes: [row/SKILL_A2_analisis_de_pliegos.xlsx]
actualizado: 2026-07-14
---

# Skill A2 — Análisis de pliegos

## Propósito
Convertir los pliegos de una licitación (PCAP, PPT, Cuadro Resumen) en un **Excel estructurado**
que resume todo lo que Pedro necesita para decidir y preparar la oferta.

## Estado ⚠️
**Solo se conserva el producto, no la receta.** El archivo subido a `row/` es la plantilla/output
Excel (llegó con extensión `.md` errónea; se guardó como `.xlsx`). El documento SKILL con las
instrucciones de extracción **no está en el repo** → gap registrado en [mejoras](../mejoras.md).
La skill [A1 de screening](screening-tc-pliegos.md) la referencia como "resumen-pliegos" (su hoja 4
es una versión abreviada de este output), lo que confirma que existe como skill separada.

## Estructura del Excel (10 hojas)
1. **Resumen licitación** — órgano, expediente, objeto, CPV, PBL sin IVA / IVA / total, valor
   estimado, lotes, procedimiento, revisión de precios, garantías, financiación UE, NUTS, lugar y
   plazo de entrega, garantía de suministros, idiomas, validez de oferta, variantes, muestras.
2. **Cronograma** — publicación, límite de consultas, límite de respuesta, límite de presentación.
3. **Datos de contacto** · 4. **Procedimiento** · 5. **Criterios** (criterio, ponderación, fórmula)
6. **Solvencias** · 7. **Penalidades** · 8. **Condiciones especiales** · 9. **Notificaciones**
10. **Sobre único** (estructura de sobres).

## Conexiones
- Alimenta el go/no-go junto con [A1 screening T&C](screening-tc-pliegos.md).
- Su output es el "resumen exhaustivo generado por IA" que el
  [verificador de ofertas](verificador-ofertas.md) exige **re-derivar y contrastar** (no confiar).
- Las hojas Criterios y Sobre único conectan con [contaminación de sobres](../conceptos/contaminacion-sobres.md).
- Primera fase del [ciclo de vida](../conceptos/ciclo-vida-licitacion.md).

## Acción pendiente
Recuperar/reescribir el SKILL.md de A2 (las columnas del Excel ya definen el contrato de salida).
