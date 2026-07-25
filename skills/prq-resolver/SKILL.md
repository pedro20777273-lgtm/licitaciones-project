---
name: prq-resolver-hologic
description: Resuelve Price Queries (PRQ) de CC&T Hologic. Cuando Pedro mencione "PRQ", "price query", "discrepancia de precio", "Oracle SO con problema", "cliente puso precio mal", o adjunte pantallazo de Oracle + PO del cliente, usa esta skill para diagnosticar, categorizar con reason code oficial, verificar presentación contra catálogo (Box of X), localizar BSA vigente sin leer todo el IBR, y generar emails resolutivos. Aplicable a cualquier división Hologic (Breast, Surgical, Diagnostics, Skeletal). Úsala incluso si no menciona "PRQ" explícitamente pero hay discrepancia de precio entre PO y Oracle.
version: 1.5
author: Pedro Moronta — Tender Specialist — Hologic Iberia
date: 20/06/2026
---

# SKILL PRQ RESOLVER v1.5 — Final con catálogos completos

> Optimizada según patrones del **skill-creator de Anthropic**: progressive disclosure, lazy loading de catálogos por división, ejemplos reales, script bundled.

---

## 1. OBJETIVO

Resolver Price Queries (PRQ) en CC&T Hologic en menos de 1 minuto, generando: diagnóstico, reason code oficial, procedimiento Oracle, emails y sugerencia preventiva. **Cubre las 3 divisiones** (Breast, Surgical, Diagnostics).

---

## 2. URLs FIJAS

| Recurso | URL |
|:--|:--|
| 📘 Esta skill | https://hologic-my.sharepoint.com/:f:/r/personal/pedro_moronta_hologic_com/Documents/Habilidades%20Order%20Management/PRQ%20RESOLVER%20(URL%20CON%20CONOCIMIENTOS)?csf=1&web=1&e=gqbCNt |
| 📚 Recursos doctrinales | https://hologic-my.sharepoint.com/:f:/r/personal/pedro_moronta_hologic_com/Documents/Habilidades%20Order%20Management/PRQ%20RECURSOS?csf=1&web=1&e=v3YQxt |
| 📂 Repositorio BSAs (IBR) | https://hologic.sharepoint.com/:f:/r/sites/commercialcontractsandtendersemea/Shared%20Documents/General/Iberia/Tenders/Test/IBR?csf=1&web=1&e=SfZn7E |
| 📊 Qlik PRQ Reporting | https://qliksense.hologic.com/sense/app/ede09209-b7a6-4dbf-a32c-8bf1f30eeacc |

---

## 3. INPUTS MÍNIMOS

| # | Input | Obligatorio | Por qué |
|:--|:--|:--|:--|
| A | **Nº de cuenta / Account ID** | ✅ | Sin esto la skill buscaría a ciegas en 200+ carpetas del IBR |
| B | Pantallazo Oracle (líneas SO) | ✅ | Para ver precios cargados |
| C | PO del cliente | ✅ | Para comparar con lo que el cliente pidió |
| D | Nº BSA conocido | 🟡 | Salta el filtrado, va directo |
| E | Nº SO Oracle | 🟡 | Para buscar histórico de correos |

### Cómo obtener el PO si Pedro no lo tiene
- **EDI** → GHX Portal: https://login.ghx.com/portal
- **Non-EDI** → eubeosticket: https://eubeosticket.hologic.corp/scp/login.php (user `FINANCE-SO` / pass `FINANCE-SOVIEW`, requiere VPN)

---

## 4. RECURSOS DE LA CARPETA (lazy loading)

> 💡 **Progressive disclosure:** No cargues todo a la vez. Lee solo lo que necesites para cada caso.

| Recurso | Cuándo cargarlo |
|:--|:--|
| `references/manual_prq.pdf` | Si dudas sobre el Process Flow oficial |
| `references/reason_codes.md` | **SIEMPRE** — diccionario verificado |
| `references/bsa_vs_standalone.pptx` | Si el setup parece raro y dudas BSA vs Standalone |
| `references/catalogo_breast.pdf` | **SOLO** si el ítem es de Breast/Skeletal (ver §5.2) |
| `references/catalogo_surgical.pdf` | **SOLO** si el ítem es de GYN Surgical |
| `references/catalogo_diagnostics.pdf` | **SOLO** si el ítem es de Cytology/Molecular |
| `scripts/find_item.py` | Ejecutar para buscar un item code rápido sin cargar PDFs |
| `references/oracle_procedure.md` | Si vas a explicar cómo asignar el código en Oracle |

> ⚡ **Truco clave:** El script `find_item.py` busca un part number en una BD interna y te devuelve división + Box of X **sin cargar PDFs**. Úsalo primero, los PDFs solo si falla.

---

## 5. FLUJO (paso a paso)

### 5.1 Verificar inputs mínimos

Si falta Account ID → **PARAR** y pedirlo. *(Razón: sin él, la skill buscaría carpetas a ciegas en el IBR — irresponsable.)*

Si falta Oracle o PO → **PARAR** y pedirlo / indicar cómo obtenerlo (§3).

### 5.2 Identificar división del ítem

Mira el patrón del part number en el SO/PO:

| Patrón | División | Catálogo a usar |
|:--|:--|:--|
| `EVIVA_*`, `ATEC*`, `MMG-*`, `MMJ-*`, `MMM-*`, `MP*`, `TUMARK-*`, `TRIMARK-*`, `SMARK-*` | Breast | `catalogo_breast.pdf` |
| `RFC2010`, `NSV5-*`, `60-*`, `40-*`, `50-*`, `10-*`, `20-*`, `30-*`, `FLT-*`, `OLK-*`, `52124-*`, `8140*`, `81501*` | Surgical | `catalogo_surgical.pdf` |
| `70*`, `71*`, `ASY-1*`, `PRD-0*`, `NVD-*`, `MD-NAT*`, `30210*`, `30292*`, `30310*`, `30313*`, `50440*`, `50450*`, `90273*`, `MTL-*`, `CMP-*`, `CBL-*` | Diagnostics | `catalogo_diagnostics.pdf` |

> 💡 **Si tienes duda**: ejecuta `python scripts/find_item.py <part_number>`. Devuelve división, presentación y Box of X sin abrir ningún PDF.

> 💡 **Si el ítem aparece en más de una división** (caso raro): carga 2 catálogos máximo. Nunca los 3.

### 5.3 Localización del BSA en IBR (estricto)

> ⚡ **REGLA DE ORO:** No leas el IBR completo. Hay 200+ carpetas.

**Si Pedro proporciona Nº BSA:**
- Buscar directamente `BSA - XXXXXXX`. Leer y solo eso.

**Si solo proporciona Nº cuenta:**
1. Listar nombres de carpetas del IBR (sin entrar)
2. Buscar la que termine en `-XXXXXX` (Nº cuenta)
3. Si no se encuentra → **PARAR**, pedir confirmación
4. Entrar SOLO en esa carpeta. Listar BSAs. Elegir vigente.
5. Leer **únicamente** ese BSA.

### 5.4 Validar elegibilidad BSA vs Standalone

| Setup correcto | Cuándo |
|:--|:--|
| **BSA** | Único Bill-To · Pricing no restringido por Bill-To/Ship-To · Buying group con commitment |
| **Standalone Modifier** | Múltiples Bill-To/Ship-To específicos · Estructura compleja |

Si el setup actual contradice → reason code **PTBA** o **SBR**.

### 5.5 Verificar presentación contra catálogo

Para CADA ítem del PO:
1. Busca el part number en el catálogo identificado en §5.2
2. Verifica la columna **"Quantity: Box of X"**
3. Compara con la cantidad del PO

Casos derivados:

| Síntoma | Reason Code |
|:--|:--|
| Cliente pide unidades sueltas pero catálogo dice Box of X | **CWPU** |
| PO incluye VAT en el precio | **CWPV** |
| Item code obsoleto/no existe en catálogo | **CWPI** |

### 5.6 Categorizar con reason code OFICIAL

> ⛔ **NO inventes reason codes.** Usa solo los de `references/reason_codes.md`.

### 5.7 Generar emails según Owner

| Owner | Quién resuelve | Destinatario del email |
|:--|:--|:--|
| **CC&T** | Pedro directamente | Cliente / KAM / CDQ según el código |
| **CS** | Equipo CS | Notificar a CS para que actúen |
| **CS + CC&T** | Coordinación | Ambos |

---

## 6. ÁRBOL DE DECISIÓN OFICIAL

```
[¿Hay BSA en Oracle?]
   │
   ├── NO → ¿Hay quote firmada en H1/Box?
   │       ├── NO → ¿Item existe en algún contrato?
   │       │       ├── NO → SNC (Sales No Contract)
   │       │       └── Solo falta este → SMI
   │       └── SÍ → ¿Cargada en Oracle?
   │              ├── NO → PTNP
   │              └── SÍ pero no triggers → PTBA
   │
   └── SÍ → ¿BSA vigente?
          ├── NO → SEC (expirado)
          └── SÍ → ¿Precio Oracle = Precio BSA?
                 ├── NO → PTWP
                 └── SÍ → ¿Precio PO = Precio Oracle?
                        ├── SÍ → No es PRQ, revisar
                        └── NO → ⚠️ CWPP
                                ├── Reincidente → CWNC
                                ├── Unidades vs cajas → CWPU
                                ├── PO con VAT → CWPV
                                ├── Item obsoleto → CWPI
                                └── PO sin precio → CWNP
```

---

## 7. PROCEDIMIENTO ORACLE (asignar reason code)

### NEW pending reason:
1. Open attachment tool on order header
2. Add new attachment line → select **Catalog**. ⚠️ **DO NOT TYPE ANY TEXT**
3. Category: **PENDING REASON** (CAPS)
4. Title (root cause): ej. **SALES** (CAPS)
5. Click **Find**
6. Select reason code
7. Click **Attach**

### AMEND:
1. Delete original
2. Save
3. Repeat NEW process

> *Razón de los CAPS:* Oracle exige formato estricto para que el reporting Qlik reconozca el código. Texto libre se ignora.

---

## 8. EJEMPLOS REALES

### Ejemplo 1 — Caso CWPP típico (Breast)

**Input:**
- Cuenta: 214505 (CLISUR MADRID)
- SO: 3127877
- Ítem: `EVIVA_0913-12T` cantidad: 5
- Precio PO: 230,00 €/und
- Precio Oracle: 250,00 €/und
- BSA 3111881 vigente, precio: 250,00 €/und

**Proceso:**
1. División detectada: **Breast** (patrón `EVIVA_*`)
2. Cargar `catalogo_breast.pdf` (o ejecutar `find_item.py EVIVA_0913-12T`)
3. Catálogo confirma: **Box of 5**, Eviva Breast Biopsy Device Petite Trocar
4. Cliente pide 5 cajas (correcto) pero a 230 €/caja
5. Oracle = BSA = 250 €/caja → cliente puso precio mal

**Output:**
- Reason code: **CWPP** (Customer Wrong PO Price)
- Owner: CS + CC&T
- Email al cliente: *"Estimados, su PO refleja 230,00 €/caja para el ítem EVIVA_0913-12T. El contrato vigente nº 3111881 establece 250,00 €/caja. Favor corregir el PO y reenviar."*
- Procedimiento Oracle: assignar **CWPP** con root cause **CUSTOMERS**

### Ejemplo 2 — Caso CWPU típico (Breast)

**Input:**
- Ítem: `ATEC 0909-20` cantidad: **100**
- Precio PO: 5,00 €/und
- Precio Oracle: 250,00 €/und

**Proceso:**
1. División: **Breast** (patrón `ATEC*`)
2. `find_item.py ATEC 0909-20` → **Box of 5**
3. Cliente pide 100 unidades sueltas a 5 €/und (cree que el precio es por unidad)
4. Realidad: el ítem se vende en **cajas de 5 unidades** a 250 €/caja
5. Debería haber pedido **20 cajas a 250 €/caja**

**Output:**
- Reason code: **CWPU** (Customer Wrong Unit)
- Email al cliente: *"Su PO indica 100 unidades sueltas de ATEC 0909-20. La presentación oficial de este ítem es 'Caja de 5 unidades' a 250,00 €/caja. Favor corregir el PO a 20 cajas en lugar de 100 unidades sueltas."*

### Ejemplo 3 — Caso SEC típico (Diagnostics)

**Input:**
- Ítem: `302929` (Aptima HPV Assay Kit 100 Test)
- BSA encontrado pero expirado en 31/12/2025

**Output:**
- Reason code: **SEC** (Sales Expired Contract)
- Owner: CC&T → Pedro escala a KAM para renewal GMC
- Email al KAM solicitando renovación del contrato

---

## 9. REGLAS GENERALES (con razón)

1. **Owner del reason code determina destinatario.** *Razón:* si lo gestiona CS, Pedro pierde tiempo escribiendo al cliente directamente cuando CS debe hacerlo.
2. **No leas más de 1 BSA por caso** (salvo petición explícita). *Razón:* el IBR tiene 200+ carpetas, cargar todas explotaría el contexto.
3. **No inventes reason codes.** *Razón:* los códigos van a Oracle y a Qlik. Un código inventado rompe el reporting.
4. **Verifica Box of X siempre antes de asumir CWPP.** *Razón:* CWPU se confunde con CWPP. La diferencia: en CWPU el cliente no entendió el formato, no que el precio esté mal.
5. **Adjunta siempre la quote/contrato firmado** cuando confirmas un precio. *Razón:* CS necesita evidencia para defender la posición ante el cliente.
6. **Importes con 2 decimales en €.**

---

## 10. LOG DE ERRORES (evolución)

| # | Lección | Versión |
|:--|:--|:--|
| 1 | SBC = SALES BOOK CONFIRMATION (no "Confusion") | v1.2 |
| 2 | Verificar Box of X del catálogo antes de CWPP | v1.2 |
| 3 | BSA vs Standalone tiene reglas oficiales | v1.2 |
| 4 | El Owner del reason code es lo que importa | v1.2 |
| 5 | Oracle: CAPS + Catalog, NO texto libre | v1.2 |
| 6 | v1.2 inventó codes → corregido en v1.3/1.4 | v1.3 |
| 7 | PRQ es genérico, hay que reclasificar | v1.3 |
| 8 | CWPP es el más común — probar primero | v1.3 |
| 9 | Lazy loading de catálogos por división (no cargar 3) | v1.5 |
| 10 | Script `find_item.py` para evitar cargar PDFs grandes | v1.5 |

---

## 11. HISTORIAL DE VERSIONES

| Versión | Cambios |
|:--|:--|
| 1.0 | Esqueleto inicial |
| 1.1 | URLs fijas + filtrado IBR estricto |
| 1.2 | Manual oficial + BSA/Standalone (con codes inventados) |
| 1.3 | REASON_CODES verificados (v2) |
| 1.4 | Verificación palabra por palabra contra docs oficiales |
| **1.5** | **Final con 3 catálogos completos (Breast + Surgical + Diagnostics) + script find_item.py + progressive disclosure + ejemplos reales basados en skill-creator de Anthropic** |

---

*Fin de la skill v1.5.*