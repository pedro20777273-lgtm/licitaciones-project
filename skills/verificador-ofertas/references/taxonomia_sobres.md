# Taxonomía de sobres y contaminación cruzada

La estructura de sobres CAMBIA en cada licitación: re-derívala del PCAP/CR (no asumas plantilla).
Estructuras típicas:
- **Sobre único** (procedimientos sin fases separadas).
- **Dos sobres:** Administrativo + Único de criterios (o Admin + Económico).
- **Tres sobres:** Administrativo (A) + Técnico/juicio de valor (B) + Económico/fórmula (C).
- Variantes con sobre de "criterios evaluables automáticamente" separado del económico.

Identifica del pliego: cuántos sobres, qué documentos van en cada uno, y qué criterios son de
**juicio de valor** vs. **evaluables mediante fórmula**. La contaminación se juzga contra ESA
estructura concreta.

## Regla central: el secreto de la evaluación
El motivo de fondo es que el órgano evalúa los criterios de juicio de valor (sobre técnico)
**antes** y **sin conocer** la oferta económica ni los criterios automáticos. Si el sobre técnico
deja inferir el precio, se rompe ese secreto → exclusión (no subsanable).

## Qué contamina cada sobre

### Sobre Administrativo (A)
NO debe contener:
- Contenido técnico valorable (memoria, soluciones, mejoras).
- Cualquier dato económico (precios, importes, descuentos, tarifas).
Sí contiene: DEUC/declaraciones, poder, solvencia, garantías formales, índice administrativo.

### Sobre Técnico / juicio de valor (B)
NO debe contener **ninguna referencia directa NI indirecta** a la oferta económica:
- Precios, importes, descuentos, % de baja, tarifas.
- Tablas, presupuestos, condiciones de pago que permitan **inferir** el importe.
- Datos que reconstruyan el económico (p. ej. "ahorro de X €", coste por unidad).
- También: criterios evaluables por **fórmula** que deban ir en el económico.
Detección: buscar símbolos de moneda (€, EUR), cifras con formato de importe, palabras como
"precio", "importe", "coste", "tarifa", "descuento", "baja", "presupuesto", "IVA".

### Sobre Económico / fórmula (C)
NO debe contener:
- Documentación técnica valorable por juicio de valor (memorias, descripciones cualitativas que
  deban puntuarse en B).
Sí contiene: oferta económica en el modelo exigido, anexos de criterios automáticos.

## Contaminación cruzada criterios automáticos ↔ juicio de valor
Incluso en sobres distintos: un criterio que el pliego define como **automático/fórmula** no puede
aparecer como contenido a valorar en el sobre de **juicio de valor**, ni a la inversa. Verifica que
cada criterio del pliego está en el sobre que le corresponde según su naturaleza.

## Chequeo de contaminación (ejecutar por sobre y por lote)
1. Para cada documento, determina a qué sobre pertenece según el pliego.
2. Confirma que está físicamente en ese sobre y no en otro.
3. Escanea el sobre técnico (B) en busca de cualquier rastro económico (directo o inferible).
4. Escanea el sobre económico (C) en busca de contenido técnico de juicio de valor.
5. Verifica coherencia automático/juicio de valor entre sobres.
6. Cualquier documento, tabla, anexo o mención ubicado en sobre que no le corresponde → hallazgo.

Gravedad por defecto: rastro económico en sobre técnico de juicio de valor → 🔴 (exclusión).
Otros cruces → 🟠/🔴 según afecten al secreto de evaluación o sean reordenación subsanable.
