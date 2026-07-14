---
tipo: concepto
tags: [order-management, oracle, bsa, pricing]
fuentes: [row/Order_Management/PRQ RECURSOS/BSA vs Standalone price modifiers V1.md]
actualizado: 2026-07-14
---

# BSA vs Standalone Price Modifier

En EMEA los acuerdos de precio en Oracle se montan de dos formas. Elegir mal al inicio produce
PRQs (PTWP), retrasos, y trabajo extra del Pricing Team (terminar y recrear el acuerdo).

## BSA (Blanket Sales Agreement) — usar cuando:
- Hay **un único Bill-To** (los Ship-To pueden variar pero deben estar vinculados en Oracle/H1).
- El precio **no** está restringido a combinaciones específicas Bill-To/Ship-To.
- Es un **buying group**: cada miembro paga sus facturas y tiene su propio commitment → un BSA por
  miembro.

Capacidades que SOLO tiene el BSA: seguimiento de commitment (Fulfillment), grace period,
**auto-renew** (⚠️ con bugs conocidos: BSA 3123233 no triggea pese a auto-renew — ver
[cuentas clave](../entidades/cuentas-clave.md)), y almacenamiento de adjuntos (PRF, quotes, notas).

## Standalone Price Modifier — usar cuando:
- El precio aplica a **múltiples combinaciones específicas** Bill-To/Ship-To.
- La estructura de cuentas es demasiado compleja para un BSA a nivel cliente.

No soporta commitment, grace period, auto-renew ni adjuntos. Ejemplo real: el modifier
"IBR - Grupo Quirón S" (List Line 40409338) que deja a 0 € los consumibles del modelo
"reactivo por determinación" del grupo Quirón.

## Síntoma de mala elección o mal mapeo
Reason codes **PTBA** (no dispara) o **SBR** (setup no conforme). El mapeo incompleto de
ShipTo × referencia en el List Qualifier es la causa nº 1 de PRQs recurrentes en
[IDCQ/Quirón](../entidades/cuentas-clave.md).

Usado por [PRQ Resolver](../skills/prq-resolver.md) §5.4. Contexto: [GMC → quote → BSA](gmc-quote-bsa.md).
