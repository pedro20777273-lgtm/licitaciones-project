---
tipo: skill
tags: [licitaciones, deuc, espd, xml, documentacion-administrativa]
fuentes: [row/SKILL_6.md]
actualizado: 2026-07-14
---

# Skill 6 — Rellenado del DEUC (ESPDResponse) v4.0

## Propósito
Rellenar el [DEUC](../conceptos/deuc-espd.md) del licitador editando **quirúrgicamente** el XML
`ESPDResponse` exportado del visor español (visor.registrodelicitadores.gob.es), sin regenerarlo,
para que el visor y espd.eu lo acepten al reimportar.

## La lección clave (v3 → v4)
La v3 transformaba el `ESPDRequest` del órgano e insertaba bloques con estructura/namespace que el
visor español no usa → **rechazado**. La v4 parte del **Response ya exportado del visor**, que trae
la estructura real y todas las respuestas correctas, y el script **solo rellena los huecos** (los
campos con "."). No toca estructura, namespaces, UUIDs ni orden. Principio generalizable: *editar
el artefacto real del sistema de destino, no regenerarlo desde cero* — el mismo principio que usa
[quote BSH](quote-creation-bsh.md) con los templates docx.

## Flujo
1. Verificar que el input es un `ESPDResponse` (si Pedro solo tiene el Request o el PDF: pasar
   antes por el visor como operador económico y exportar).
2. `python3 scripts/rellenar_deuc.py response_visor.xml RESPONSE_<EXPEDIENTE>.xml --datos datos_licitacion.json`
   (JSON mínimo: `expediente`, `organo`; opcional lotes y nacimiento del apoderado).
3. QC automático: XML bien formado, empresa (HOLOGIC + B83279331), apoderado (Sergio), SMEIndicator
   false, ROLECSP true, 0 placeholders "." restantes.
4. Entrega + reimportar en visor + generar PDF oficial + **firma electrónica del apoderado**.

## Datos fijos embebidos (fuente ROLECE)
Ver [Hologic Iberia](../entidades/hologic-iberia.md): razón social, NIF, domicilio, apoderado
Sergio Sánchez de Torres, código ROLECSP 43522. Respuestas estándar: exclusiones=No,
ALL_SATISFIED=Sí, UTE=No, medios externos=No, no PYME, inscrita en ROLECSP.

## Depuración
Si el visor rechaza: pedir el **mensaje de error exacto**, comparar raíz/namespaces con el Response
original. Cada órgano puede publicar variantes de esquema → **siempre partir del Response del visor
de ESA licitación**, nunca de plantilla genérica. Plan B: rellenar a mano en el visor (~5 min).

## Estado y recursos
🟢 Madura (v4.0, con historia de errores documentada). ⚠️ El script `rellenar_deuc.py` **no está
en el repo** — solo el documento skill. Gap en [mejoras](../mejoras.md).

## Conexiones
- Documento del sobre administrativo → lo revisa el [verificador de ofertas](verificador-ofertas.md)
  (DEUC mal cumplimentado = defecto subsanable 🟠, no exclusión).
- Sistema: visor DEUC en [sistemas](../entidades/sistemas.md).
- El apoderado firma también las declaraciones de [requerimientos 3.1](requerimientos-documentacion.md).
