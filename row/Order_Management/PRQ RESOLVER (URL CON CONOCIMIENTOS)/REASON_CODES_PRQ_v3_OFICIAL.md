**Fuente:** `Pending reason codes improved process and list.xlsx` (Hologic CC&T Oficial)
**Manual de referencia:** `6. Price Queries (PRQs).pdf` (Frances Owens / Fabien Pinet, Release 01/10/2025)
**Fecha actualización:** 20/06/2026

> ✅ **VERSIÓN DEFINITIVA VERIFICADA** — Todos los códigos extraídos PALABRA POR PALABRA del Excel oficial.
> ⛔ Versiones anteriores (v1, v2) contenían códigos inventados — DESCARTADAS.

---

## 🟢 CUSTOMER SERVICE (4 codes — Owner: CS)

| Code | Description | Owner | Used by | When to use |
|:--|:--|:--|:--|:--|
| **CSC** | CS CHECK | CS | CS | CS needs to verify/check something internally |
| **CSE** | CS ERROR | CS + CC&T | CS | CS made an error that prevents booking the order |
| **CSM** | CS MISS | CS + CC&T | CS | CS missed booking the order same day |
| **CSN** | CS NEW HIRE | CS | CS | New CS hire entered order that requires checking |

---

## 🔴 CUSTOMERS (16 codes — Owner: CS or CC&T)

| Code | Description | Owner | Used by | When to use |
|:--|:--|:--|:--|:--|
| **CSL** | CUST SHELF LIFE | CS | CS | Customer requires specific shelf life, CS waiting approval |
| **CWDC** | CUST CHANGE/DELAY/CANCELLATION | CS | CS | Customer requested delay/change/cancellation |
| **CWLC** | CUST WAIT LC | CS | CS | Customer needs to provide LC document |
| **CWLO** | CUST CONFIRM LOGI | CS | CS | Customer needs to confirm logistic details |
| **CWNP** | CUSTOMER NO PRICE | CS + CC&T | CS | Customer ordering without any pricing |
| **CWPA** | CUSTOMER WRONG ADDRESS | CS | CS | Missing or wrong address |
| **CWPI** | CUSTOMER WRONG ITEM CODE | CS + CC&T | CS | Customer using superseded/non-existing item codes |
| **CWPP** | CUSTOMER WRONG PRICE ⚠️ | CS + CC&T | CS | **MÁS COMÚN** — Prices on PO not matching Oracle |
| **CWPU** | CUSTOMER WRONG UNIT | CS + CC&T | CS | Customer ordering in units instead of boxes per contract |
| **CWPV** | CUSTOMER WRONG VAT | CS + CC&T | CS | Prices on PO with VAT included |
| **CWSP** | CUSTOMER SPARE SERVICE OPS | CC&T | CS | PO parts are spare parts not loaded on BSA |
| **CWPF** | CUSTOMER WRONG FORM (DACH) | CS + CC&T | CS (DACH only) | Customer using old order form template (DACH only) |
| **CWPT** | CUSTOMER WRONG TEMPLATE | CS | CS | PO template unreadable (light, dark, handwriting) |
| **CWNC** | CUSTOMER NOT COMPLIANT | CC&T | CC&T | Previous CWPP orders, customer failed to amend |
| **CWBP** | CUSTOMER BANDED PRICING (UK) | CC&T | CC&T (UK only) | Customer on banded pricing 1-2-3 (UK only) |
| **CWNPO** | CUSTOMER WRONG NO PO | CS | CS | Installation: customer did not present PO |

---

## 🟠 PRICING TEAM (4 codes — Owner: CC&T)

| Code | Description | Owner | Used by | When to use |
|:--|:--|:--|:--|:--|
| **PTBA** | PT BSA AUTOMATIC | CC&T | CC&T | BSA applicable but not triggered, or multiple BSAs none correct |
| **PTNP** | PT NEW PRICING | CC&T | CC&T | Pricing not set up yet (no signed contract or no pre-load) |
| **PTPI** | PT PRICE INCREASE SET UP | CC&T | CC&T | Price increase not set up in system |
| **PTWP** | PT WRONG PRICING | CC&T | CC&T | Pricing set up incorrectly or with delay, or FOC list issue |

---

## 🟡 SALES (8 codes — Owner: CC&T or CS)

| Code | Description | Owner | Used by | When to use |
|:--|:--|:--|:--|:--|
| **SAC** | SALES APPS CONFIG (Africa) | CS (Africa) | CS (Africa) | Sales App confirmation of KITS configuration split |
| **SBC** | SALES BOOK CONFIRMATION | CS | CS | Order entered, waiting Sales confirmation to book |
| **SCPR** | SALES CPR | CS | CS | CPR orders entered, waiting Sales approval |
| **SEC** | SALES EXPIRED CONTRACT | CC&T | CC&T | Sales hasn't provided signed contract; existing one expired |
| **SMI** | SALES MISSING ITEM | CC&T | CC&T | Priced/FOC item missing from contract |
| **SNC** | SALES NO CONTRACT | CC&T | CC&T | No contract at all, item never quoted |
| **SPI** | SALES PRICE INCREASE | CC&T | CC&T | Price increase project causing discrepancies |
| **SBR** | SALES BUSINESS RULES | CC&T | CC&T | Contract setup not compliant with system |

---

## ⚪ CC&T (1 code — Owner: CC&T)

| Code | Description | Owner | Used by | When to use |
|:--|:--|:--|:--|:--|
| **SSM** | SALES SUPPORT MISS | CC&T | CC&T | Sales Support missed to add items to BSA form |

---

## 🔵 CUSTOMER DATA (4 codes)

| Code | Description | Owner | Used by | When to use |
|:--|:--|:--|:--|:--|
| **DNA** | DT NEW/AMEND ADDRESS | CS | CS | New shipping/billing address needs setup |
| **DNR** | DT NEW RELATIONSHIP/ACCOUNT | CS | CS | New relationship between accounts needed |
| **DWA** | DT WRONG ACCOUNT | CC&T | CS | CS chose wrong bill-to/sold-to → generates PRQ |
| **DFR** | DATA WRONG FREIGHT | CC&T | CS | Freight charged/not charged or wrong amount |

---

## 📦 EDI (4 codes)

| Code | Description | Owner | Used by | When to use |
|:--|:--|:--|:--|:--|
| **EDE** | EDI ERROR | CS | CS | GHX (GFAX) pushed order incorrectly |
| **EDL** | EDI LATE | CS | CS | PO arrived/pushed after 16h |
| **EDM** | EDI WRONG MAPPING | CS + CC&T | CS | EDI wrong due to incorrect mapping by CS or CC&T |
| **EDS** | EDI SPLIT | CS + CC&T | CS | PO split in 2 — one ticketing, other EDI touchless |

---

## 🚢 STOCK (4 codes — Owner: CS)

| Code | Description | Owner | Used by | When to use |
|:--|:--|:--|:--|:--|
| **SAL** | STOCK ALLOCATION | CS | CS | Item not available, ready to release |
| **SAP** | STOCK APPROVAL | CS | CS | Short shelf life or Upper Management approval needed |
| **SBA** | STOCK ALTERNATIVE ITEM | CS | CS | Not in stock, waiting customer alternative |
| **SBO** | STOCK BACKORDER | CS | CS | Master Lot on backorder, waiting stock |

---

## 🛃 CUSTOMS (2 codes — Owner: CS)

| Code | Description | Owner | Used by | When to use |
|:--|:--|:--|:--|:--|
| **CTA** | APPROVAL TO SHIP | CS | CS | Awaiting approval to ship (customs clearance) |
| **CTI** | CUSTOMS ITTQ | CS | CS | Awaiting Legal/Regulatory/Compliance for IITQ |

---

## 💰 FINANCE (1 code — Owner: CS)

| Code | Description | Owner | Used by | When to use |
|:--|:--|:--|:--|:--|
| **FCC** | FINANCE CREDIT CHECK | CS | CS | Customer order auto-held in Oracle (Payment) |

---

## 🔧 MANUAL OVERRIDE (4 codes — Owner: CS)

| Code | Description | Owner | Used by | When to use |
|:--|:--|:--|:--|:--|
| **MONP** | NO PRICE LIST | CS | CS | No price list available |
| **MOPL** | FOC PRICE LIST | CS | CS | Manual override for FOC item showing price (CDQ list issue) |
| **MOPM** | FOC PROMO MODIFIER | CS | CS | Manual override for FOC item with promo modifier |
| **MOU** | URGENT NO PRICE | CS | CS | Manual override: incorrect price, urgent shipment |

---

## 🔄 RETURNS (2 codes — Owner: CS)

| Code | Description | Owner | Used by | When to use |
|:--|:--|:--|:--|:--|
| **RCE** | CUST ERROR - UOM | CS | CS | Customer ordering EA qty not orderable (e.g. 3x NS2013 instead of 1) |
| **RIN** | INVESTIGATION NEEDED | CS | CS | Return created by another dept, needs investigation |

---

## ⚖️ REGULATORY & COMPLIANCE (1 code — Owner: CS)

| Code | Description | Owner | Used by | When to use |
|:--|:--|:--|:--|:--|
| **REC** | RA EXPORT COMPLIANCE HOLD | CS | CS | Items blocked by export compliance |

---

## 🏢 THIRD PARTY (4 codes)

| Code | Description | Owner | Used by | When to use |
|:--|:--|:--|:--|:--|
| **TPI** | INTEGRATION | CS | CS | Orders entered, can't book — integration project |
| **TPM** | MASTER DATA | CS | CS | Master Data (item, etc.) not setup correctly |
| **TPS** | SYSTEM ERROR | CS + CC&T | CS | Oracle issue needing IT (e.g. BSA not triggering due to dates) |
| **TPSA** | SITE ASSESSMENT | CS | CS | Installation: site assessment missing/incorrect |

---

## ❓ PRICE QUERY (1 code — generic initial)

| Code | Description | Owner | Used by | When to use |
|:--|:--|:--|:--|:--|
| **PRQ** | PRICE QUERY (genérico) | CS → CC&T | CS (inicial) | Generic initial code; **Sales Support MUST reclassify with exact code** |

---

## 💳 CREDIT NOTES (14 codes — Only in Credit Order Type)

| Code | Description |
|:--|:--|
| **CNAL** | ALBARAN |
| **CNAS** | CS ERROR - ACCOUNT SETUP |
| **CNCO** | COVID |
| **CND** | CS ERROR - DUPLICATE ORDER |
| **CNE** | CS ERROR - BILL TO |
| **CNEP** | CS ERROR - WRONG PRICING |
| **CNEX** | EXPIRY DATE |
| **CNFB** | FINANCE CREDIT BOOK HOLD |
| **CNFO** | FOC |
| **CNFR** | FREIGHT/HANDLING COST |
| **CNM** | MISSING DELIVERY |
| **CNPI** | PRICE INCREASE |
| **CNPT** | PRICING TEAM ERROR |
| **CNQ** | CS ERROR - QUANTITY |

---

# 🌳 ÁRBOL DE DECISIÓN OFICIAL — RECLASIFICACIÓN DE PRQ

> Cuando una orden llega marcada como **PRQ** genérico, Sales Support debe reclasificar con el código correcto. Este árbol sigue el Process Flow del manual oficial.

```
[¿Hay BSA en Oracle?]
        │
        ├── NO → [¿Hay quote firmada en H1/Box?]
        │              │
        │              ├── NO → [¿El item existe en algún contrato?]
        │              │              ├── NO → 🟡 SNC (Sales No Contract)
        │              │              └── Solo falta este item → 🟡 SMI
        │              │
        │              └── SÍ → [¿Cargada en Oracle?]
        │                             ├── NO → 🟠 PTNP (PT New Pricing)
        │                             └── SÍ pero no triggers → 🟠 PTBA (PT BSA Automatic)
        │
        └── SÍ → [¿BSA vigente?]
                       │
                       ├── NO (expired/terminated) → 🟡 SEC (Sales Expired Contract)
                       │
                       └── SÍ → [¿Precio Oracle = Precio BSA?]
                                      │
                                      ├── NO → 🟠 PTWP (PT Wrong Pricing)
                                      │
                                      └── SÍ → [¿Precio PO = Precio Oracle?]
                                                     │
                                                     ├── SÍ → No es PRQ real, revisar otros datos
                                                     └── NO → ⚠️ 🔴 CWPP (Customer Wrong Price)
                                                              │
                                                              └── Casos derivados de CWPP:
                                                                     ├── Reincidente → 🔴 CWNC
                                                                     ├── Unidades vs cajas → 🔴 CWPU
                                                                     ├── PO con VAT → 🔴 CWPV
                                                                     ├── Item obsoleto → 🔴 CWPI
                                                                     └── PO sin precio → 🔴 CWNP
```

---

# 👥 REGLAS DE OWNERSHIP

| Owner | Quién resuelve |
|:--|:--|
| **CC&T** | Pedro (o equipo CC&T) gestiona directamente |
| **CS** | Notificar al equipo CS para que ellos gestionen |
| **CS + CC&T** | Coordinación entre ambos equipos |

---

# 🔧 PROCEDIMIENTO ORACLE PARA ASIGNAR REASON CODE

### NEW Pending Reason (paso a paso EXACTO del Excel oficial):

1. **Open attachment tool** on the **header of the order**
2. **Click to add a new attachment line** and select the **catalog**
   > ⚠️ **DO NOT TYPE ANY TEXT IN THE NEW LINE!**
3. **Choose category "PENDING REASON"** and **ALWAYS USE CAPS**
4. **Choose root cause (e.g. SALES)** and **ALWAYS USE CAPS to fill into Title**
5. Click **Find**
6. **Select applicable pending reason code** from the list
7. Click **Attach**

> ✅ Pending reason code is **now attached** and **CANNOT be amended**.

### AMEND Pending Reason (modificar después):

1. **Delete original** attachment
2. Click **Save**
3. **Click add new attachment line + Catalog** (NO TEXT)
4. **Repeat NEW process** from step 1

> ⚠️ **REGLA CRÍTICA:** NUNCA escribir texto libre. SIEMPRE seleccionar del catálogo en CAPS.

---

# 📊 REPORTING

| Recurso | URL |
|:--|:--|
| **Qlik PRQ Dashboard** | https://qliksense.hologic.com/sense/app/ede09209-b7a6-4dbf-a32c-8bf1f30eeacc |

---

# 📌 LECCIONES APRENDIDAS

1. ✅ **SBC** = **SALES BOOK CONFIRMATION** (no "Sales Booking Confusion").
2. ⚠️ **CWPP** es el más común — siempre probar esa hipótesis primero.
3. 🔍 Cuando hay CWPP, **verificar si es reincidencia** (CWNC), **error de unidad** (CWPU), **VAT** (CWPV) o **item code** (CWPI).
4. 📂 **Si no hay BSA pero hay quote → PTNP/PTBA**, no SNC.
5. 🟢 **SNC vs SEC:** No aparece BSA en absoluto → SNC. Aparece pero expirado → SEC.
6. 👤 **Codes con Owner CS** se notifican al equipo CS — Pedro **NO los resuelve** directamente.
7. ⚙️ Oracle exige **CAPS + selección del catálogo**, **NO texto libre**.
8. 📦 **Verificar Box of X** del catálogo de productos ANTES de asumir CWPP — puede ser CWPU.
9. 🎯 **PRQ es código GENÉRICO inicial** — Sales Support DEBE reclasificar siempre con el código exacto.
10. 🔄 Una vez attachado, el código **NO se puede modificar** sin hacer AMEND completo.

---

*Fin del diccionario v3.0 — VERIFICADO contra docs oficiales.*