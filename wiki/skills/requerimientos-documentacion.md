---
tipo: skill
tags: [licitaciones, adjudicacion, requerimiento, docx, plantillas]
fuentes: [row/SKILL_3_1.md]
actualizado: 2026-07-14
---

# Skill 3.1 — Requerimientos de documentación previa a la adjudicación

## Propósito
Cuando Hologic es **propuesto adjudicatario**, el órgano emite un requerimiento de documentación
previa. Esta skill convierte el expediente (requerimiento + PCAP + CRC/Anexo I + PPT) en
**3 entregables .docx listos para presentar**, preservando exactamente el formato corporativo.

## Los 3 entregables
1. **Índice de documentación** (`rellenar_indice.py`) — todos los documentos exigidos al
   adjudicatario, con desgloses de solvencia. Plantilla con fuente Proxima Nova, pie azul #0F206C.
2. **Ficha de aval** (`rellenar_aval.py`) — solicitud de aval bancario para la
   [garantía definitiva](../conceptos/garantia-definitiva-aval.md). El avalado es siempre Hologic;
   el órgano disponente es el ente superior (no el hospital).
3. **Tabla de localización** + **declaraciones responsables** que falten
   (`rellenar_declaracion.py`, firma Sergio Sánchez de Torres). Acciones: PREPARAR / DESCARGAR /
   SOLICITAR.

## Regla de oro
Los scripts **clonan párrafos-plantilla y sustituyen solo el texto conservando el `rPr`** (fuente,
negrita, tamaño). NUNCA regenerar el documento desde cero — mismo principio "editar, no regenerar"
que [DEUC](deuc.md) y [quote BSH](quote-creation-bsh.md).

## Entradas
Dos URLs de carpeta general (pliegos del expediente + documentos corporativos). La skill localiza
dentro los archivos concretos. references obligatorias: `datos_fijos_hologic.md` y
`reglas_extraccion.md`.

## Estado y recursos
🟢 Formato Agent Skill con frontmatter y triggers. ⚠️ **Assets no incluidos en el repo**: las 3
plantillas .docx, el certificado ROLECE de referencia, los 2 archivos de references y los 3 scripts.
Gap en [mejoras](../mejoras.md).

## Conexiones
- Fase post-adjudicación del [ciclo](../conceptos/ciclo-vida-licitacion.md): se activa tras pasar el
  [verificador](verificador-ofertas.md) y ganar.
- La ficha de aval alimenta directamente a [Check Aval](check-aval.md) (el banco emite el borrador
  a partir de ella).
- Datos fijos → [Hologic Iberia](../entidades/hologic-iberia.md) (duplicados aquí; gap de fuente única).
