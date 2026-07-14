---
tipo: concepto
tags: [order-management, prq, reason-codes, oracle]
fuentes: [row/Order_Management/PRQ RESOLVER (URL CON CONOCIMIENTOS)/REASON_CODES_PRQ_v3_OFICIAL.md, row/Order_Management/PRQ RECURSOS/6. Price Queries (PRQs).md]
actualizado: 2026-07-14
---

# PRQ y reason codes — el lenguaje del order management

## Qué es una PRQ
Un **Price Query** surge cuando Customer Service detecta discrepancia entre el precio del PO del
cliente y Oracle. Actúa como **bloqueo**: el pedido no se bookea hasta resolverla. `PRQ` es el
código genérico inicial — Sales Support (Pedro) **debe reclasificar** con el código exacto.

## Los códigos que Pedro usa a diario (de 70+ oficiales)

| Código | Significado | Owner | Patrón típico |
|---|---|---|---|
| **CWPP** | Customer Wrong Price (el más común) | CS+CC&T | Cliente puso precio viejo/erróneo en su PO |
| **CWPU** | Customer Wrong Unit | CS+CC&T | Pide unidades sueltas cuando el ítem va en Box of X (Cytolyt, Parc Taulí) |
| **CWPV** | PO con IVA incluido | CS+CC&T | |
| **CWPI** | Item code obsoleto | CS+CC&T | |
| **CWNC** | Cliente reincidente que no corrige | CC&T | |
| **PTWP** | Pricing Team cargó mal el precio | CC&T | BSA con precio ≠ quote |
| **PTBA** | BSA vigente pero no dispara | CC&T | ShipTo/ref sin mapear en el List Qualifier |
| **PTNP** | Pricing no cargado aún | CC&T | Quote firmada pero BSA no creado |
| **SEC** | Contrato expirado | CC&T | Prórroga vencida sin GMC nuevo |
| **SMI** | Ítem falta en el contrato | CC&T | |
| **SNC** | No existe contrato | CC&T | |

Diccionario completo (CS, Customers, Pricing, Sales, Data, EDI, Stock, Customs, Finance, Manual
Override, Returns, Third Party, Credit Notes) en la fuente v3 — verificado **palabra por palabra**
tras descartar 2 versiones con códigos inventados.

## Reglas críticas
- El **Owner** del código decide quién actúa (CC&T=Pedro / CS / ambos) y a quién va el email.
- En Oracle: attachment en el header, categoría PENDING REASON, **CAPS, selección de catálogo,
  nunca texto libre** (si no, Qlik no lo reconoce). Una vez attachado no se modifica (borrar y repetir).
- SNC vs SEC: no aparece BSA → SNC; aparece pero expirado → SEC.
- Verificar **Box of X** antes de asumir CWPP (puede ser CWPU).
- **List Price ≠ Selling Price** — el Orbit Report puede confundir.

## La lectura estratégica
SEC, PTBA, PTNP y SMI son **fallos de proceso interno** (contratos sin renovar, BSAs sin cargar o
mal mapeados) — prevenibles desde el ciclo de tender. CWPP/CWPU son **fallos del cliente** —
mitigables con educación del comprador. Ver [síntesis](../sintesis.md) y [mejoras](../mejoras.md).

Usado por [PRQ Resolver](../skills/prq-resolver.md). Conceptos hermanos:
[BSA vs Standalone](bsa-vs-standalone.md), [GMC → quote → BSA](gmc-quote-bsa.md).
