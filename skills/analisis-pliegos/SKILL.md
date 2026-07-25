---
name: analisis-pliegos
description: Analiza los pliegos de una licitación pública española (PCAP, PPT, Cuadro Resumen/Anexo I) y produce un Excel estructurado de 10 hojas con el resumen completo del expediente. Úsala cuando el usuario adjunte pliegos y pida "analiza esta licitación", "resumen del pliego", "resumen-pliegos", "extrae los datos del expediente", o antes de un screening o verificación. El Excel resultante alimenta el screening T&C (A1) y sirve de referencia (a re-derivar) al verificador de ofertas.
---

> ⚠️ **RECONSTRUCCIÓN (2026-07-14).** El SKILL.md original de A2 no llegó al repositorio; solo la
> plantilla Excel de salida. Este documento se ha reconstruido desde esa plantilla
> (`assets/plantilla_analisis_pliegos.xlsx`) y desde las referencias cruzadas en la skill A1.
> Cuando aparezca el original, sustituir este archivo y quitar este aviso.

# Análisis de pliegos (A2) — resumen estructurado en Excel

## Propósito
Convertir los pliegos de una licitación en un Excel de 10 hojas que responde, sin releer el pliego,
a: qué se licita, cuánto, cuándo, con qué criterios, qué solvencia piden, qué penalidades hay y qué
va en cada sobre.

## Entradas
- PCAP + PPT + Cuadro Resumen/Anexo I (PDF o URL de la carpeta del expediente).
- Si falta alguno, indicarlo y continuar con lo disponible marcando los campos como "no consta".

## Reglas de extracción
1. **Literalidad**: importes, plazos y fórmulas se copian literales del pliego, citando cláusula.
2. **No inventar**: campo no encontrado = "no consta" (nunca en blanco ni estimado).
3. **Jerarquía**: ante discrepancia, PCAP > PPT; el Cuadro Resumen concreta el PCAP. Señalar la
   discrepancia en Observaciones.
4. **Por lote**: si hay lotes, desglosar PBL, criterios y garantías por lote.

## Salida: Excel con 10 hojas (contrato de columnas de la plantilla)

| # | Hoja | Columnas / campos |
|---|---|---|
| 1 | **Resumen licitación** | Campo·Valor: órgano de contratación, expediente (tipo), objeto, CPV principal, PBL sin IVA, IVA (21%), importe total con IVA, valor estimado, nº de lotes, procedimiento, revisión de precios, garantías (provisional/definitiva), financiación UE, código NUTS, lugar de entrega, plazo de entrega por pedido, garantía de los suministros, idiomas de la oferta, validez de la oferta, variantes, muestras, lugar de presentación, órgano (titular) |
| 2 | **Cronograma** | Hito·Fecha/Hora: publicación, límite para elevar consulta, límite de respuesta, límite de presentación de ofertas |
| 3 | **Datos de contacto** | organismo, departamento/unidad, dirección, oficinas, teléfono, fax, email, perfil del contratante, horario de información |
| 4 | **Procedimiento** | publicidad, subasta electrónica, presentación de ofertas, apertura, incidencias técnicas del último día, plazo de subsanación, requerimientos justificativos, ofertas anormalmente bajas, adjudicación, formalización, desempate |
| 5 | **Criterios** | Criterio de adjudicación · Ponderación máxima · Regla/Fórmula (distinguir juicio de valor vs fórmula) |
| 6 | **Solvencias** | Tipo · Exigencia · Observaciones |
| 7 | **Penalidades** | Ámbito · Supuesto · Consecuencia/Importe |
| 8 | **Condiciones especiales** | Ámbito · Condición |
| 9 | **Notificaciones** | Aspecto · Detalle |
| 10 | **Sobre único** (o una hoja por sobre) | Bloque · Documento/Requisito · Detalle — la estructura de sobres se re-deriva del pliego concreto |

Usar `assets/plantilla_analisis_pliegos.xlsx` como base de formato.
Nombre de salida sugerido: `Analisis_[expediente].xlsx`.

## Conexiones
- El Excel alimenta el screening A1 (`../screening-tc-pliegos/`) — su hoja "Datos del pliego" es la
  versión abreviada de la hoja 1.
- El verificador de ofertas (`../verificador-ofertas/`) usa este resumen como referencia pero
  **re-deriva** sobres e importes del pliego (principio "re-derivar, no confiar").
- La hoja Cronograma es el insumo natural de un futuro sistema de recordatorios de plazos.
