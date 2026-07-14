---
tipo: skill
tags: [licitaciones, verificacion, exclusion, sobres, chequeo-final]
fuentes: [row/verificador-ofertas/SKILL.md, row/verificador-ofertas/references/]
actualizado: 2026-07-14
---

# Verificador de ofertas — chequeo antes de presentar

## Propósito
Revisión exhaustiva de la oferta completa contra los pliegos **antes de subirla al portal**, con
criterio de experto en contratación pública (LCSP 9/2017, RGLCAP). Objetivo: **cero causas de
exclusión**. No genera documentos: lee, analiza y reporta por gravedad.

## Principios (los más transferibles de todo el arsenal)
1. **Re-derivar, no confiar**: no dar por bueno el resumen IA previo (el de
   [A2](analisis-pliegos.md)); re-derivar sobres y requisitos del PCAP+CR+PPT y contrastar.
2. **Todo por lote** — mezclar lotes es causa frecuente de exclusión.
3. **Jerarquía documental**: PCAP > PPT; el Cuadro Resumen concreta el PCAP.
4. **Subsanable vs. no subsanable** (art. 141 LCSP): solo lo no subsanable es 🔴 NO ENVIAR.
   Ver [checklist de exclusión](../conceptos/causas-exclusion.md).
5. **Declarar lo no verificable** (firma criptográfica → AutoFirma/VALIDe; juicio de ingeniería).

## Flujo
Paso 0 mapa del expediente → Paso 1 contraste con resumen IA → Pasos 2-10: **bloques A-I**
(documentos presentes, idioma, formato/firma, coherencia de datos, cumplimiento económico POR LOTE,
cumplimiento técnico documental, criterios/mejoras, red flags, discrepancias entre pliegos) →
Paso 11 informe.

## Output
Estado general (✅ LISTO / ⚠️ CORREGIR / 🔴 NO ENVIAR, por lote) + tabla de hallazgos
(gravedad·lote·documento·página·problema·referencia·corrección) + checks superados + acción
inmediata ordenada.

## Recursos (formato Agent Skill completo — el mejor ejemplo del repo)
- `references/checklist_exclusion.md` → destilado en [causas de exclusión](../conceptos/causas-exclusion.md)
- `references/taxonomia_sobres.md` → destilado en [contaminación de sobres](../conceptos/contaminacion-sobres.md)
- `references/bloques_chequeo.md` — detalle operativo A-I.

## Estado
🟢 Único con estructura skill+references empaquetada (llegó como ZIP renombrado a `.txt`).
Es el modelo de formato al que migrar las demás — ver [patrón de diseño](../conceptos/patron-diseno-skills.md).

## Conexiones
- Es la **puerta de calidad** entre preparar ([DEUC](deuc.md), [quote BSH](quote-creation-bsh.md),
  memoria técnica) y presentar. Última línea de defensa del [ciclo](../conceptos/ciclo-vida-licitacion.md).
- Si la oferta pasa y se adjudica → [requerimientos 3.1](requerimientos-documentacion.md).
