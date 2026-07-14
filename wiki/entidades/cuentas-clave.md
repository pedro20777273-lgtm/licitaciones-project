---
tipo: entidad
tags: [cuentas, clientes, patrones, prq]
fuentes: [row/Order_Management/Recursos a consultar 2/PRQ_KNOWLEDGE_BASE (1).md, row/Order_Management/Recursos a consultar 2/PRQ_LOG_SEMANA28_2026 (4).md]
actualizado: 2026-07-14
---

# Cuentas clave y sus patrones (Iberia)

Resumen de la PRQ_KNOWLEDGE_BASE (actualizada 10/07/2026). Cada cuenta tiene un patrón de fallo
característico — conocerlo resuelve la PRQ en minutos.

| Cuenta (BillTo) | Quién es | Patrón característico | Acción estándar |
|---|---|---|---|
| **IDCQ Servicios y Mantenimiento (3084786)** | Grupo Quirónsalud (cuenta paraguas nueva) | ⚠️ La más problemática: mapping ShipTo×ref incompleto tras migración desde la cuenta antigua (159646). Modelo "reactivo por determinación" (consumibles a 0 €, facturación por contralbarán). Modifier "IBR - Grupo Quirón S" (List Line 40409338, vigente→08/07/2027). BSA 3123233 (ATEC CANISTER 35 €) con bug de auto-renew — ticket OT1286446 cerrado sin fix y reabierto | M.O. a 0 €/precio contractual + escalar CDQ para ampliar mapping. Escalar a Santiago/Ben para fix estructural |
| **CPC Granada (152691)** | SAS — Central Provincial de Compras | BSA 3112009 con precio desactualizado (105 vs 109,09 €); quote nueva GMC.ES.Cyto.T.26.037336 sin cargar por pendientes del KAM Pablo | M.O. a 109,09 €/pack + perseguir a Pablo |
| **SMS Murcia (195002)** | Plataforma Logística Servicio Murciano | BSA 3127305 no dispara en la ref 70793-001 (BLUING) — mapeo incompleto | M.O. a 331 €/pack + escalar CDQ |
| **Infanta Sofía (131588)** | Madrid pública (⚠️ NO confundir con el ShipTo Infanta Sofía de Quirón) | CWPU recurrente: pide Cytolyt 70408-002 en unidades sueltas (es **pack indivisible de 4 botellas**, 86,40 €/pack). Quote Sonia Duque vigente→2030, BSAs OK | NO bookear; pedir PO corregido al cliente |
| **Candelaria (132743)** | Servicio Canario de Salud | SEC: prórroga del expediente 23-22-SU-DG-A-E001 vencida en marzo/2026 sin GMC nuevo. **IGIC 7%**, no IVA. 70671-001 va a 0 € (FOC del concurso) | M.O. a precios del concurso + perseguir GMC a Pablo |
| **Parc Taulí (258149)** | Consorci Sanitari (Sabadell) | Siempre pide en **unidades sueltas**; Oracle reagrupa en packs. Si el Extended coincide con el PO → no hay discrepancia real. Multi-división con BSAs separados (3115183/3111797/3111846/3112119) | Verificar reagrupación → bookear directo |
| **Maresme i la Selva (408937)** | Corporació de Salut | Sospecha de **error de carga** en BSA 3124409 (creado por Pedro 16/04/2026): ratios Oracle/PO inconsistentes (5x, 2,5x) sugieren error unit/pack | NO bookear; esperar confirmación de la KAM Monica Martinez |
| Otros | Consorci Clínic BCN (134361), Getafe, CPC Huelva (152711) | Precio 10-403FC a corregir · CWPU Cytolyt · CWNP histórico | — |

## Lecciones transversales
1. La migración de cuentas (Quirón) sin migrar el mapping de pricing = meses de PRQs.
2. Los patrones por cuenta convierten diagnósticos de horas en minutos — **esta KB es el activo
   más valioso del área de order management** y debe seguir alimentándose semanalmente.
3. Los emails/formatos de PO por cliente (quironsalud, juntadeandalucia, carm, salud.madrid…)
   permiten identificar la cuenta al vuelo.

Ver [PRQ Resolver](../skills/prq-resolver.md) · [reason codes](../conceptos/prq-reason-codes.md) ·
[KAMs](kams.md).
