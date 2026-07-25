# Bloques de chequeo A–I (detalle operativo)

Ejecutar todos. Aplicar **por lote** donde proceda. Para cada hallazgo: gravedad + documento +
página + cláusula del pliego + corrección.

## A. Documentos presentes
- ¿Están todos los documentos exigidos por el pliego para cada sobre (según mapa del Paso 0)?
- Lista los que faltan.
- ¿Hay documentos de más, no pedidos, que puedan generar problema (p. ej. dato económico colado)?

## B. Idioma
- ¿Todo en castellano (u oficial exigido)? El PCAP suele exigirlo.
- Catálogos o partes en otra lengua: ¿llevan traducción oficial/jurada cuando se exige?
  (Falta de traducción exigida = subsanable, 🟠.)

## C. Formato y forma  (si los documentos no vienen firmados, marcar este bloque "pendiente tras firmar")
- Formato de archivo aceptado por el portal (PDF, XSIG, ZIP).
- Tamaño dentro del máximo del portal.
- Firma electrónica presente donde se requiere (presencia y firmante; NO validación criptográfica).
- Mismo firmante autorizado en todos los documentos que lo requieren.
- El firmante coincide con el poder de representación aportado.
- No faltan páginas, anexos referenciados, sellos ni fechas.

## D. Coherencia de datos entre documentos
- CIF, razón social y domicilio idénticos en TODOS los documentos.
- Nº de expediente correcto y consistente.
- Nombre del órgano de contratación correcto.
- Objeto del contrato consistente.
- Fechas coherentes entre sí (y dentro de plazo).

## E. Cumplimiento económico  (POR LOTE)
- ¿El precio total ofertado supera el PBL del lote? (🔴 exclusión.)
- ¿Los precios unitarios cuadran con el total ofertado? (aritmética.)
- ¿IVA desglosado como partida independiente si se exige?
- ¿Cantidad ofertada = cantidad solicitada?
- ¿Algún precio unitario supera el máximo unitario del pliego? (🔴.)
- ¿La oferta económica respeta el FORMATO exigido: nº de decimales, importe en letra y número,
  modelo/anexo obligatorio, redondeo? (desviación de formato esencial puede excluir.)

## F. Cumplimiento técnico  (documental; POR LOTE)
- ¿La oferta cumple TODAS las prescripciones mínimas del PPT (compatibilidad, especificaciones,
  accesorios, filtros, consumibles, etc.) según lo declarado en memoria/fichas?
- ¿Faltan declaraciones técnicas exigidas?
- ¿Plazo de entrega/ejecución ofertado encaja con el del pliego? (por debajo del mínimo = 🔴.)
- ¿Plazo de garantía ofertado ≥ mínimo del pliego?

## G. Criterios de adjudicación / aspectos de negociación
- ¿Cada criterio o aspecto evaluable está cubierto en la oferta?
- ¿Las mejoras son verificables y concretas, no meras declaraciones de intenciones?

## H. Red flags de exclusión
- Datos en blanco en anexos obligatorios.
- Anexos con texto incorrecto/inconsistente (ej.: dice "acuerdo marco" siendo contrato de
  suministro; tipo de procedimiento equivocado).
- **Contaminación de sobres** (ver `taxonomia_sobres.md`): cada sobre contiene exclusivamente lo
  suyo; sin rastro económico en técnico de juicio de valor; sin técnica valorable en económico;
  coherencia automático↔juicio de valor; ningún documento/tabla/mención fuera de su sobre.
- Marcas, logos y datos de Hologic consistentes y presentes en las declaraciones.
- Confidencialidad: si se declara info confidencial, ¿está marcada como tal y sin contradicciones?
- Faltas de firma donde se requiere.
- Errores tipográficos en correos, CIF, importes.

## I. Discrepancias entre pliegos
- Si hay discrepancia PCAP / PPT / CR: indica cuál prevalece (normalmente PCAP > PPT; CR concreta
  el PCAP, salvo regla específica del propio pliego) y cómo afecta a la oferta presentada.
