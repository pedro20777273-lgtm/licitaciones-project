---
tipo: concepto
tags: [deuc, espd, xml, documentacion-administrativa]
fuentes: [row/SKILL_6.md]
actualizado: 2026-07-14
---

# DEUC / ESPD — Documento Europeo Único de Contratación

Declaración responsable estandarizada europea que sustituye (en fase de oferta) a los certificados
que acreditan que el licitador no está en causa de prohibición de contratar y cumple los criterios
de selección.

## Piezas
- **ESPDRequest** — el XML que publica el órgano de contratación con sus preguntas.
- **ESPDResponse** — el XML de respuesta del licitador. Es lo que genera y rellena la
  [skill DEUC](../skills/deuc.md).
- **Visor español**: visor.registrodelicitadores.gob.es (importar Request como operador económico
  → exportar Response). También existe espd.eu.

## Respuestas estándar de Hologic
Exclusiones = No · Criterios de selección `ALL_SATISFIED` = Sí · UTE = No · Subcontratación /
medios externos = No · No PYME (SMEIndicator=false) · Inscrita en **ROLECSP** (código 43522,
primera inscripción 2018-10-16) — la inscripción ROLECE permite simplificar la acreditación.

## Trampas conocidas
- Cada órgano puede publicar **variantes del esquema** → partir siempre del Response exportado del
  visor para esa licitación concreta.
- Un DEUC mal cumplimentado es defecto **subsanable** ([causas de exclusión](causas-exclusion.md)),
  pero genera requerimientos que consumen plazo.
- El PDF final debe ir **firmado electrónicamente por el apoderado** (Sergio Sánchez de Torres,
  ver [Hologic Iberia](../entidades/hologic-iberia.md)).
