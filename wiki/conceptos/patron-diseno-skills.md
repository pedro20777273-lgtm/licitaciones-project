---
tipo: concepto
tags: [meta, skills, diseno, progressive-disclosure, versionado]
fuentes: [derivado de todas las skills; row/Order_Management/PRQ RESOLVER (PROMPT DE INVOCACION)/GUIA LOGICA.md]
actualizado: 2026-07-14
---

# El patrón de diseño de skills de Pedro (meta-conocimiento)

Al cruzar las 9 skills emerge un **método propio** de construcción, refinado durante ~1 año.
Documentarlo importa: es lo que hace escalable el sistema y transferible a un equipo.

## Los 8 patrones recurrentes

1. **Versionado con historia de errores.** Cada skill lleva versión e historial (DEUC v4 explica
   por qué v3 falló; PRQ v1.5 lista 10 lecciones de 5 versiones). El log de errores es parte de la
   skill (`ERRORES_SKILL_*.md`), se lee antes de ejecutar y se actualiza después.
2. **Editar el artefacto real, nunca regenerarlo.** [DEUC](../skills/deuc.md) edita el XML del
   visor; [quote BSH](../skills/quote-creation-bsh.md) y [3.1](../skills/requerimientos-documentacion.md)
   clonan párrafos de templates conservando el formato. Regenerar desde cero = rechazo o pérdida
   de formato corporativo.
3. **Progressive disclosure / lazy loading** (adoptado del skill-creator de Anthropic en PRQ v1.5):
   metadata siempre → cuerpo al invocar → recursos solo si hacen falta. Catálogo por división,
   nunca los 3.
4. **Scripts empaquetados para evitar cargar documentos** (`find_item_v2.py` con BD de 334 ítems
   resuelve ~60% de casos sin abrir PDFs; `rellenar_*.py` para docx; `rellenar_deuc.py` para XML).
5. **Inputs mínimos obligatorios o PARAR.** PRQ exige Account ID; Check Aval exige sus 3
   documentos. Evita búsquedas a ciegas y alucinaciones.
6. **Nunca inventar datos de sistemas.** Reason codes solo del diccionario verificado (2 versiones
   se descartaron por códigos inventados); verificación "palabra por palabra" contra documentos
   oficiales; "si falta un modelo/contacto/documento, DECIRLO".
7. **Prompt de invocación copy-paste** con URLs fijas y campos a rellenar + versión ultra-corta
   para sesiones con contexto.
8. **QC como parte del flujo**: checklist visual post-generación (quote BSH), control de calidad
   con todos-True (DEUC), veredicto global tipificado (Check Aval, verificador).

## Clasificación por gravedad — la firma de la casa
Todas las skills de verificación usan la misma escala mental: 🔴 bloqueante/exclusión ·
🟠/🟡 corregir/confirmar · 🟢/⚪ cosmético o no comparable. Coherente entre
[verificador](../skills/verificador-ofertas.md), [Check Aval](../skills/check-aval.md) y
[screening A1](../skills/screening-tc-pliegos.md).

## Debilidades del patrón actual (→ [mejoras](../mejoras.md))
- Nombres inconsistentes (SKILL_5/6/A1/A2/3_1 vs nombres descriptivos) y sin repositorio único.
- Datos fijos de Hologic duplicados en 4+ skills.
- Los assets (templates, modelos CCAA, scripts) viven en SharePoint/OneDrive con URLs frágiles y
  no están junto a la skill.
- Solo [verificador-ofertas](../skills/verificador-ofertas.md) y parcialmente 3.1/A1 usan el
  formato estándar Agent Skill (frontmatter name/description + references/).
