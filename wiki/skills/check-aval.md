---
tipo: skill
tags: [licitaciones, aval, garantia-definitiva, bastanteo, ccaa]
fuentes: [row/SKILL_CHECK_AVAL_v1_1.md]
actualizado: 2026-07-14
---

# Skill Check Aval v1.1 — verificación de avales bancarios

## Propósito
Verificar **palabra por palabra** que el borrador de aval emitido por el banco se ajusta al modelo
oficial de la CCAA correspondiente, cruzar todos los datos con el requerimiento/PCAP, clasificar
discrepancias y generar el email de bastanteo. Aplicable a **cualquier CCAA**, no solo Canarias
(donde nació: Expte. 23/S/25/SU/DG/A/AM35 del SCS).

## Flujo
1. **3 inputs obligatorios** (si falta uno, PARAR): borrador del aval, modelo oficial CCAA
   (carpeta `Modelos_Oficiales_CCAA/`), requerimiento/PCAP.
2. Identificar CCAA y modelo; identificar impuesto (**IVA 21% península/Baleares, IGIC 7%
   Canarias** — regla compartida con [PRQ Resolver](prq-resolver.md)).
3. **13 campos** verificados uno a uno (entidad avalista, apoderados, cláusula de poderes,
   normativa, obligación garantizada con LOTE, beneficiario+NIF, importe en cifra y letra
   = 5% × adjudicado sin impuestos, solidaridad/primer requerimiento, validez INDEFINIDA,
   carácter ejecutivo, registro de avales, verificación de representación, bastanteo EN BLANCO).
4. Comparación textual frase por frase → clasificar: 🔴 BLOQUEANTE / 🟡 MENOR / ⚪ COSMÉTICA.
5. Tabla resumen + veredicto global (🟢 correcto / 🟡 con observaciones / 🔴 bloqueantes).
6. **Email de bastanteo** al Servicio Jurídico + Caja de Depósitos de la CCAA (contactos en
   `CONTACTOS_BASTANTEO.md`), con preguntas explícitas si hay observaciones.

## Trampas documentadas
- "S.L." vs "S.L.U." en la razón social — verificar qué usa el órgano y qué tiene el banco.
- La sección de bastanteo la rellena el Servicio Jurídico, **no el banco** — si viene rellenada, señalar.
- Caja de Depósitos propia de la CCAA vs Caja General del Estado.

## Estado y recursos
🟢 v1.1 con log de errores previsto. ⚠️ **Faltan en el repo**: los modelos oficiales por CCAA
(17 PDFs), `CONTACTOS_BASTANTEO.md` y el log `ERRORES_SKILL_CHECK_AVAL.md`. Gap en [mejoras](../mejoras.md).

## Conexiones
- Recibe el borrador que el banco emite desde la ficha de [requerimientos 3.1](requerimientos-documentacion.md).
- Concepto: [garantía definitiva y aval](../conceptos/garantia-definitiva-aval.md).
- Última fase administrativa del [ciclo](../conceptos/ciclo-vida-licitacion.md) antes de formalizar contrato.
