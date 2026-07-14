---
tipo: concepto
tags: [sobres, exclusion, secreto-evaluacion]
fuentes: [row/verificador-ofertas/references/taxonomia_sobres.md]
actualizado: 2026-07-14
---

# Contaminación de sobres

## La regla central: el secreto de la evaluación
El órgano evalúa los criterios de **juicio de valor** (sobre técnico) *antes* y *sin conocer* la
oferta económica. Si el sobre técnico permite **inferir el precio**, se rompe ese secreto →
**exclusión no subsanable** ([causas de exclusión](causas-exclusion.md)).

## Estructuras típicas (re-derivar SIEMPRE del pliego, nunca asumir plantilla)
Sobre único · dos sobres (Admin + Único/Económico) · tres sobres (A administrativo, B técnico
juicio de valor, C económico/fórmula) · variantes con sobre de criterios automáticos separado.

## Qué contamina cada sobre
- **A (administrativo):** nada técnico valorable ni ningún dato económico.
- **B (técnico/juicio de valor):** ninguna referencia directa NI indirecta al precio — importes,
  descuentos, % de baja, "ahorro de X €", coste por unidad, condiciones de pago. Detección: buscar
  €, EUR, "precio", "importe", "coste", "tarifa", "descuento", "baja", "presupuesto", "IVA".
  Tampoco criterios de fórmula que van en C.
- **C (económico):** nada valorable por juicio de valor.
- **Cruzado:** cada criterio del pliego debe estar en el sobre que corresponde a su naturaleza
  (automático ↔ juicio de valor), incluso estando en sobres distintos.

## Gravedad
Rastro económico en el sobre técnico de juicio de valor → 🔴 exclusión. Otros cruces → 🟠/🔴 según
afecten al secreto o sean reordenación subsanable.

## Dónde se aplica
Bloque H del [verificador de ofertas](../skills/verificador-ofertas.md), ejecutado **por sobre y
por lote**.
