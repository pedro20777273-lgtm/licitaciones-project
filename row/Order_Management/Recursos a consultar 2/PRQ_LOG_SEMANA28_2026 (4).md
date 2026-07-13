> **Autor:** Pedro Moronta
> **Fecha registro:** 10/07/2026
> **Ámbito:** Resoluciones de PRQ tramitadas durante la semana del 07-11/07/2026
> **Formato:** listo para copiar/pegar en tabla del huddle semanal

---

## 📋 Tabla resumen para huddle

| Pending Reason | Division | Order Number | PO Number | Order-Blanket | BillTo Name | BillTo Number | Why 1 | Why 2 | Why 3 | Why 4 | Why 5 | Root cause | Action to be done | Deadline | Comments | Status |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **PTWP** | DIAGNOSTIC | 3129051 | 4421567499 | 3127305 | PLAT. LOG. APROVISIONAMIENTO INTEGR. SERV. MURCIANO SALUD | 195002 | BSA 3127305 no dispara auto en 70793-001 | Sales Agreement vacío en línea 2.1 | Oracle aplica List Price (1.240 €) en vez de contract price (331 €) | Ref no mapeada en modifier para este ShipTo | Recurrencia con esta cta+ref | Modifier del BSA 3127305 no incluye la ref. 70793-001 en su List Qualifier | M.O. de 1.240 € → 331 €; book; escalar CDQ ampliar mapping | 10/07/2026 | Email enviado a eOrdersIberia. Escalar CDQ pendiente | solved |
| **PTBA** | DIAGNOSTIC | 3129178 | AC26124102 | – (stand-alone Grupo Quirón) | IDCQ SERVICIOS Y MANTENIMIENTO, S.L.U. (ShipTo Infanta Sofía) | 3084786 | Ref. 301154C no triggea a 0 € del stand-alone Grupo Quirón | ShipTo Infanta Sofía sin mapear para 301154C | Modelo reactivo por determinación (0 € pedido + contralbarán) | Mismo patrón SO 3128988 (PRD-03568/PRD-03000) | Recurrencia mapping incompleto post-migración Servicios Personas y Salud → IDCQ | Stand-alone modifier grupo Quirón vigente pero sin ShipTo Infanta Sofía mapeado para 301154C en List Qualifier | 1) M.O. a 0 € y bookear. 2) CC&T amplía ticket abierto SO 3128988 con 301154C | 10/07/2026 | Email enviado a eOrdersIberia | solved |
| **PTWP** | DIAGNOSTIC | 3129112 | 1060082/26 (POs orig. 958020671 / 958020277) | 3112009 | CENTRAL PROVINCIAL DE COMPRAS DE GRANADA | 152691 | BSA 3112009 con precio 105 €/caja vs contractual 109,09 € | Cliente aplica precio de la quote nueva | Quote GMC.ES.Cyto.T.26.037336 pendiente de cargar | KAM Pablo no ha respondido a los pendientes desde 25/06 | Recurrencia con esta cta (Week 37 SO 3117868) | BSA desactualizado; quote nueva emitida pero sin fechas efectivas ni H1 | 1) M.O. 105 → 109,09 €/caja. 2) Book. 3) Recordar a Pablo pendientes (H1, fechas, duración) | 10/07/2026 | Email a eOrdersIberia con CC Pablo y Santiago | solved |
| **SEC** | DIAGNOSTIC | 3129008 | 4503174518 | 3111851 | HOSPITAL UNIV. NTRA. SRA. DE LA CANDELARIA | 132743 | BSA 3111851 precios contrato anterior (825 y 250 €) | Prórroga expediente 23-22-SU-DG-A-E001 vencida marzo/2026 | Quote GMC.ES.Cyto.Q.22.004091 pendiente renovación | KAM Pablo Lorenzo — sin GMC actualizado | IGIC 7% Canarias no IVA 21% | Contrato Servicio Canario Salud expirado sin renovación cargada en Oracle | 1) M.O. 70098-002 825 → 760 €; 70671-001 250 → 0 € FOC. 2) Book. 3) Pablo emitir GMC actualizado con fechas | 10/07/2026 | Email enviado a eOrdersIberia con CC Pablo, Maite, Santiago. Maite ya envió consulta a Pablo esta mañana | solved |
| **PTBA** | BREAST HEALTH | 3129214 | AC26125151 | – (BSA 3123233) | IDCQ SERVICIOS Y MANTENIMIENTO, S.L.U. (ShipTo Clínica Esperanza de Triana Sevilla) | 3084786 | BSA 3123233 no triggea ATEC-CANISTER auto | Sales Agreement vacío en línea 3.1 | Oracle aplica List Price 90 € vs contract 35 € | BSA tiene auto-renew 12M y precios correctos, pero modifier no dispara | Ticket OT1286446 (Maite 02/07) cerrado sin fix; 3 PRQs desde entonces | Bug técnico Oracle en modifier del BSA 3123233 — ticket cerrado prematuramente | 1) M.O. 90 € → 35 € solo línea 3.1. 2) Book. 3) Reabrir OT1286446 con evidencia recurrencia (3 SOs) | 10/07/2026 | Email a eOrdersIberia + escalado paralelo CDQ (nuevo ticket con exigencia de fix definitivo) | solved |
| **PTBA** | DIAGNOSTIC | 3129219 | AC26125206 | 40409338 (IBR-Grupo Quirón S / GMC.ES.Cyto.Q.22.011871) | IDCQ SERVICIOS Y MANTENIMIENTO, S.L.U. (ShipTo H. Quirón Santa Cristina Albacete) | 3084786 | Stand-alone modifier Grupo Quirón no triggea para 70098-002 en este ShipTo | Oracle aplica List Price 1.020 € vs contractual 0 € | Modelo reactivo por determinación | Mismo patrón SO 3128988 y 3129178 | ShipTo Albacete no mapeado en List Qualifier del modifier | Stand-alone modifier IBR-Grupo Quirón S vigente hasta 08-JUL-2027 pero sin ShipTo Albacete mapeado para 70098-002 | 1) Aplicar Modifier List Line 40409338 manualmente → 0 €. 2) Book. 3) CC&T ampliar ticket abierto | 10/07/2026 | Email enviado. Confirmado por pantallazo SO 3129180 (mismo modifier funcionando correctamente) | solved |
| **CWPU** | DIAGNOSTIC | 3129095 | 5502705734 | 3120473 (líneas 1-5) + 3121436 (líneas 6-10) | HOSPITAL UNIV. INFANTA SOFÍA (S. Sebastián Reyes) | 131588 | Cliente pidió 12 UN 70408-002 a 86,40 €/UN | Malinterpretó precio pack como precio botella | Cytolyt 70408-002 es pack indivisible 4 botellas | Discrepancia 1.036,80 vs 259,20 € (Oracle correcto) | Mismo patrón CWPU que SO 3129047 Getafe | Cliente ordena Cytolyt en UN sueltas al precio de pack completo | 1) NO bookear. 2) CS contactar ndmartin@salud.madrid.org para PO corregido: 3 packs = 12 botellas, 259,20 € s/IVA. 3) Bookear cuando llegue PO corregido | – | Email enviado a eOrdersIberia. Esperando PO corregido cliente | pending |
| **CWPU** | (multi: Breast+Surgical+Diagnostic) | 3129236 | 4500336787 | 3115183 / 3111797 / 3111846 | CORPORACIÓ SANITÀRIA PARC TAULÍ | 258149 | Cliente Parc Taulí siempre expresa cantidades en UN sueltas | Oracle correctamente reagrupa en packs | List Price 1.950 € del Orbit engañó al primer análisis | Selling Price real 1.669,50 €/pack coincide con contrato | Recurrencia: SO 3128343, SO 3128880 | Patrón EDI estándar Parc Taulí (UN sueltas → packs) | Book Order directo (todos los precios coinciden Oracle=PO) | 10/07/2026 | Email OK a eOrdersIberia | solved |
| **PTWP** (por confirmar) | DIAGNOSTIC | 3129175 | MGC-4500297792 | 3124409 | CORPORACIÓ DE SALUT DEL MARESME I LA SELVA | 408937 | BSA 3124409 aplica precios inferiores al PO cliente | 70671-001: Oracle 24 € vs PO 120 € (ratio 5x) | 70098-002: Oracle 230 € vs PO 575 € (ratio 2,5x) | Ratios de discrepancia inconsistentes | Sospecha error de carga precios al crear BSA en abril/2026 | Probable error conversión unit/pack al crear BSA 3124409 desde GMC.ES.Cyto.Q.25.027998 | 1) NO bookear. 2) Escalado KAM Monica Martinez para confirmar precio real. 3) Con OK, M.O. a 120/575 €/pack + tramitar CDQ corrección BSA | – | Email enviado a Monica.Martinez + CC eOrdersIberia, Santiago, Maite | pending |

---

## 🔄 Tickets CDQ abiertos / seguimientos externos

| Ticket / Escalado | SO / BSA | Estado | Siguiente acción |
|---|---|---|---|
| **OT1286446 (Maite 02/07 → cerrado sin fix)** | BSA 3123233 ATEC CANISTER — cta 3084786 | Reabierto 10/07 con evidencia 3 PRQs recurrentes (3128688, 3129090, 3129214) | Esperar respuesta CDQ con root-cause analysis técnico |
| **OT1287779 (Pedro 06/07)** | SO 3128880 Parc Taulí 10-403FC | Abierto | Seguimiento con CDQ mapping BSA 3111846/3112119 |
| **OT1289132 (Pedro 08/07)** | SO 3129047 Getafe 70408-002 CWPU | Abierto | Esperar PO corregido cliente Getafe |
| **OT1289211 (Pedro 08/07)** | SO 3128977 Quirón Barcelona SEC | Abierto | Seguimiento auto-renew BSA con equipo contratos |
| **OT1289305 (Pedro 09/07)** | SO 3128988 IDCQ Infanta Sofía PRD-03568/PRD-03000 | Abierto | Ampliar con SO 3129178 y 3129219 para mapping global grupo Quirón |
| **OT1283672 (Pedro 25/06)** | SO 3128373 Quirón Huelva GMC.ES.GSS.Q.26.033464 | Abierto | Carga BSA con la quote |

---

## 🚨 Pendientes con KAMs / Sales Reps

| KAM | Pendiente | Desde | Cuentas afectadas | Estado |
|---|---|---|---|---|
| **Pablo Lorenzo** | Datos H1 + fechas efectivas + duración GMC.ES.Cyto.T.26.037336 | 25/06/2026 | 152691 (CPC Granada) | Sin respuesta |
| **Pablo Lorenzo** | Confirmar precio 70098-002 SO 3128647 CPC Huelva | Maite 01/07/2026 | 152711 (CPC Huelva) | Sin respuesta |
| **Pablo Lorenzo** | GMC actualizado Candelaria expediente 23-22-SU-DG-A-E001 | 10/07/2026 | 132743 (Candelaria) | Iniciado hoy |
| **Monica Martinez** | Confirmar precio real GMC.ES.Cyto.Q.25.027998 (posible error carga BSA 3124409) | 10/07/2026 | 408937 (Maresme) | Iniciado hoy |
| **Nathalia Oliveira / Nat** | Aportar GMC para corregir precio 10-403FC en BSA 3112012 Consorci Clínic | Maite 09/07/2026 | 134361 (Consorci Clínic BCN) | Sin respuesta |

---

## 📈 Métricas semana 28

- **Total PRQs tramitadas:** 9
- **Solved (book confirmado):** 7 (3129051, 3129178, 3129112, 3129008, 3129214, 3129219, 3129236)
- **Pending (esperando cliente/KAM):** 2 (3129095, 3129175)
- **Escalados CDQ:** 2 (OT1286446 reabierto, ampliación OT1289305)
- **Divisiones:** Diagnostic 7 · Breast 1 · Multi 1
- **Categorías más frecuentes:** PTBA (3), PTWP (3), CWPU (2), SEC (1)

---

## 🎯 Puntos clave para el huddle de viernes

1. **Grupo IDCQ 3084786 (Quirón)** sigue siendo la cuenta con más incidencias — 3 SOs esta semana con el mismo patrón de mapping incompleto. **Escalar a Santiago/Ben** para acción estructural con CDQ.
2. **Pablo Lorenzo** acumula 3 pendientes sin respuesta que están bloqueando cargas de BSA en 3 cuentas distintas (Granada, Huelva, Candelaria). **Escalar a Santiago**.
3. **CDQ cerró OT1286446 sin fix técnico** → hay que exigir SLA de respuesta técnica antes de cerrar tickets.
4. **Patrón Cytolyt (70408-002) CWPU recurrente** en Madrid pública (Getafe, Infanta Sofía). Proponer comunicación con Sonia Duque para educar al comprador o cambiar la descripción del pedido.
5. **Sospecha de error de carga BSA 3124409** (Maresme) — si se confirma, revisar todos los BSAs creados en abril/2026 por si hay otros con el mismo bug.

---

*Documento generado 10/07/2026. Actualizar cada viernes antes del huddle.*