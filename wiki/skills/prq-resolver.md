---
tipo: skill
tags: [order-management, prq, oracle, reason-codes, bsa, ccyt]
fuentes: [row/Order_Management/ (completo)]
actualizado: 2026-07-14
---

# Skill PRQ Resolver v1.5 — la más madura del arsenal

## Propósito
Resolver **Price Queries** (discrepancias de precio entre el PO del cliente y Oracle que bloquean
el booking del pedido) en menos de 1 minuto: diagnóstico, [reason code oficial](../conceptos/prq-reason-codes.md),
verificación de presentación (Box of X), localización del BSA vigente, emails resolutivos y
registro en el huddle semanal. Cubre las 3 divisiones ([Breast, Surgical, Diagnostics](../entidades/divisiones-hologic.md)).

## Arquitectura (3 capas, progressive disclosure)
Optimizada con los patrones del skill-creator de Anthropic — ver [patrón de diseño](../conceptos/patron-diseno-skills.md):
- **Metadata** (frontmatter, siempre) → **SKILL.md** (al invocar) → **recursos** (solo si hacen falta).
- **Lazy loading de catálogos**: detecta la división por patrón del part number (`EVIVA_*`→Breast,
  `70*`→Diagnostics…) y carga SOLO ese catálogo.
- **Script `find_item_v2.py`**: BD interna de 334 ítems (31 Breast, 53 Surgical, 250 Diagnostics)
  → resuelve división + Box of X sin abrir PDFs (~60% de casos).

## Flujo
1. Inputs mínimos o PARAR: Account ID + pantallazo Oracle + PO del cliente.
2. Identificar división → 3. Localizar BSA en el IBR (**regla de oro: no leer más de 1 BSA**;
   200+ carpetas) → 4. Validar [BSA vs Standalone](../conceptos/bsa-vs-standalone.md) →
5. Verificar Box of X contra catálogo → 6. Categorizar con reason code oficial (**nunca inventar**;
   van a Oracle y Qlik) → 7. Email según Owner (CC&T=Pedro / CS / ambos) → 8. Registrar en huddle.

## Árbol de decisión (resumen)
¿Hay BSA? No→(¿quote en H1/Box? No→SNC/SMI; Sí→PTNP/PTBA) · Sí→(¿vigente? No→SEC;
¿Oracle=BSA? No→PTWP; ¿PO=Oracle? No→**CWPP** y derivados CWPU/CWPV/CWPI/CWNC/CWNP).

## Ecosistema de conocimiento (lo que la hace única)
1. **Diccionario de reason codes v3** — 70+ códigos verificados palabra por palabra del Excel
   oficial, tras descartar 2 versiones con códigos inventados. Ver [reason codes](../conceptos/prq-reason-codes.md).
2. **PRQ_KNOWLEDGE_BASE** — patrones por [cuenta](../entidades/cuentas-clave.md) (Quirón/IDCQ,
   CPC Granada, SMS Murcia, Infanta Sofía, Candelaria, Parc Taulí, Maresme), reglas de producto
   (Cytolyt = pack indivisible de 4), [contactos KAM](../entidades/kams.md) y plantillas de email.
   Se actualiza cada vez que aparece un patrón nuevo.
3. **Logs semanales** (`PRQ_LOG_SEMANA_XX`) — tabla huddle con 5-whys, root cause, tickets CDQ y
   métricas (semana 28: 9 PRQs, 7 resueltas, PTBA/PTWP dominan).
4. **Log de errores** de la propia skill (10 lecciones, 5 versiones).

## Lecciones operativas clave
- List Price ≠ Selling Price (el Orbit engaña) · La **quote es la fuente suprema de verdad** del
  precio · Canarias = IGIC 7% · Parc Taulí siempre pide en unidades sueltas · CDQ cierra tickets
  sin fix → reabrir con evidencia de recurrencia · Oracle exige CAPS + catálogo, nunca texto libre.

## Conexiones (la más importante del cerebro)
Los PRQs recurrentes son **síntomas de fallos aguas arriba del ciclo de tender**: contratos
expirados sin renovar (SEC ← renovación no automatizada), BSAs sin cargar o mal mapeados
(PTBA/PTNP ← carga post-[quote](quote-creation-bsh.md) manual), KAMs sin responder. Ver
[síntesis](../sintesis.md) y las propuestas preventivas en [mejoras](../mejoras.md).
