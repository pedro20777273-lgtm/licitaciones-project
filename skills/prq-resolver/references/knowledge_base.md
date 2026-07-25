> **Propósito:** Base de conocimiento centralizada para la Skill "PRQ Resolver".
> Este archivo debe **consultarse SIEMPRE al inicio** de cada resolución de PRQ para
> aplicar patrones ya conocidos, evitar reinventar diagnósticos y mantener coherencia.
>
> **Autor:** Pedro Moronta (Iberia Tender Specialist)
> **Última actualización:** 10/07/2026
> **Ámbito:** Cuentas Iberia (España + Portugal), Oracle HOLX_IBR_OU

---

## 📖 Cómo usar este archivo

Cuando llegue una nueva PRQ, seguir este orden:

1. **Identificar cuenta BillTo** → buscar en sección "Patrones por cuenta".
2. **Identificar referencia** → verificar reglas de presentación en "Reglas de producto".
3. **Comparar Oracle vs PO** → aplicar workflow estándar.
4. **Categorizar** con la taxonomía oficial.
5. **Redactar email** siguiendo la plantilla correspondiente.
6. **Registrar en huddle semanal**.

---

## 🏷️ Taxonomía oficial de Pending Reasons

| Código | Nombre | Cuándo aplica |
|---|---|---|
| **PTWP** | PT Wrong Pricing | BSA activo pero con precio incorrecto vs contrato real |
| **PTBA** | PT BSA Automatic | BSA vigente pero no dispara automáticamente (ShipTo/ref no mapeado) |
| **SEC** | Sales Expired Contract | BSA/contrato expirado; prórroga vencida |
| **SSM** | Sales Signed Modifier | Quote en record pero BSA no cargado en Oracle |
| **SNC** | Sales No Contract | No hay BSA ni quote — pedido sin cobertura contractual |
| **CWPU** | Customer Wrong Pack Unit | Cliente pide en UN sueltas sin considerar Box of X |
| **CWPP** | Customer Wrong Price | Cliente pone precio incorrecto en su PO |
| **CWNP** | Customer No Price | PO sin precio (blank) → validar si es 0 € contractual o falta info |
| **DNA** | DT New/Amend Address | Problema con ShipTo (dirección nueva o a modificar) |
| **DWA** | DT Wrong Account | CS seleccionó cuenta incorrecta |
| **CSE** | CS Error | Error de Customer Service al capturar el pedido |
| **SBR** | Sales Business Rules | Violación de reglas de negocio (validación bloqueada) |

---

## 📦 Reglas de producto (Presentaciones y precios estándar)

### Diagnostic — Citología (Cyto)

| Ref. | Descripción | Presentación estándar | Notas críticas |
|---|---|---|---|
| **70408-002** | CYTOLYT 32 OZ 4 PACK | **PACK INDIVISIBLE de 4 botellas de 946 ml** | ⚠️ **NUNCA se vende por botella suelta**. Precio por pack (86,40 € Infanta Sofía). Error CWPU muy recurrente. |
| **70671-001** | ROVERS CERVEX-BRUSH KIT | CAJA de 20 BOLSAS de 25 = 500 unidades/pack | Precio por pack: 109,09 € (CPC Granada), 120 € (Maresme), 180 € (Infanta Sofía), 250 € (Candelaria antes = 0 € FOC en nuevo tender) |
| **70098-002** | PRESERVCYT INTL SOLUTION KIT | ENV/250 unidades | Precio varía por cuenta. Cuidado con IGIC 7% en Canarias |
| **70099-001** | FILTER THINPREP PAP TEST | 500 PACK | Precio contractual: 1.074-1.155 €/pack |
| **70205-001** | FILTER THINPREP NON-GYN | 100 PACK | Precio contractual ~304 €/pack |
| **70303-001** | THINPREP SLIDE KIT | 500 PACK (portaobjetos) | Puede ir a 0 € (FOC) en algunos contratos |
| **70780-001** | THINPREP NUCLEAR STAIN | 4L | Precio típico: 82,40 €/pack |
| **70779-001** | THINPREP RINSE SOLUTION | 4L | Precio típico: 82,40 €/pack |
| **70781-002** | THINPREP ORANGE G | 4L | Precio típico: 82,40 €/pack |
| **70782-002** | THINPREP EA SOLUTION | 4L | Precio típico: 82,40 €/pack |
| **70793-001** | THINPREP BLUING SOLUTION | 4L | Precio típico: 82,40 €/pack |
| **ASY-14753** | 100 PACK PRESERVCYT VIAL NON-GYN | 100 viales/pack | Precio típico: 323-352 €/pack |
| **70825-001** | SLIDE KIT THINPREP IMAGING SMS | 500 láminas/pack | |
| **70372-001** | THINPREP MICROSCOPE SLIDES NON-GYN | 100 pack | |

### Surgical (GSS)

| Ref. | Descripción | Presentación | Notas |
|---|---|---|---|
| **10-403FC** | MyoSure REACH Tissue Removal Device | **C/3 (pack de 3 uds)** | Precio contractual ~1.669,50 €/pack (556,50 €/UN). Recurrente en Parc Taulí y Consorci Clínic. |
| **30-403LITE** | MyoSure LITE Tissue Removal | C/3 (3 pack) | ~1.410-1.470 €/pack |
| **50-503XL** | MyoSure XL Tissue Removal | C/3 (3 pack) | ~1.950-2.067 €/pack |
| **40-902** | Scope Seal Sets | C/10 (10 per box) | ~130-159 €/pack |
| **60-5FR** | 5Fr Seal | C/10 | ~200 €/pack |
| **FLT-212** | Fluent Pro Disposable Pack | 6-pack | ~1.320 €/pack |
| **FLT-112** | Fluent Disposable Pack | 6-pack | ~1.200 €/pack |
| **60-250-1** | OMNI Hysteroscope STANDARD Set | – | ~4.500 € |
| **60-903-1** | OMNI Instrument Tray | – | ~1.000 € |
| **NSV5-003** | NovaSure V5 INTL 3-pack | C/3 | ~2.100-2.226 €/pack |
| **815012** | CO2 Gas Cartridges x 5 | – | ~150 €/pack |

### Breast Health

| Ref. | Descripción | Presentación | Notas |
|---|---|---|---|
| **TUMARK-E13-S** | TUMARK VISION Marcador mama nitinol esférico | C/10 | 980 €/pack Parc Taulí |
| **ATEC-CANISTER** | Canister aguja biopsia | C/10 | Precio contractual grupo Quirón: **35,00 €** — BSA 3123233 no triggea (ticket OT1286446 pendiente) |
| **EVIVA-0913-12T** | Set aguja estéril 9GX12CMX12MM | C/5 | 1.044,65 €/pack IDCQ |
| **EVIVA-NG09L** | Guía aguja estéril 9G | C/5 | 38,90 €/pack IDCQ |
| **EVIVA_0913-12T** | (variante EVIVA_ vs EVIVA-) | idem | Diferente escritura del código en Oracle vs PO cliente |

### Diagnostic — Molecular (Panther/Aptima)

| Ref. | Descripción | Notas |
|---|---|---|
| **PRD-03568** | HSV Assay Aptima 100T | Modelo "reactivo por determinación" grupo Quirón — 0 € en pedido, facturación por contralbarán |
| **PRD-03000** | HIV Viral Load Assay 100T | Idem — modelo reactivo por determinación |
| **301154** | APTIMA LIQUID PAP TR | Componente BOM (0 € en pedido) |
| **301154C** | TUBO TRANSFERENCIA APTIMA 2,9ML C/100 | Modelo reactivo por determinación — 0 € Quirón |
| **301040 / 301040-01** | – | Grupo Quirón — 0 € reactivo por determinación |
| **70303-001** | ThinPrep Slide Kit | Puede ir 0 € FOC en algunos contratos Quirón |

### Otros (Emsor / distribución)

| Ref. | Descripción | Notas |
|---|---|---|
| **3-255-0004** | Sterile Pack Closed Needle Guide 14G | Marca Emsor. C/1 mín. 5. Precio 9,50 €/EA |

---

## 🏥 Patrones por cuenta (Casos recurrentes)

### 🔵 IDCQ Servicios y Mantenimiento SL (BillTo 3084786) — Grupo Quirónsalud

- **Nueva cuenta paraguas** que sustituyó a la antigua "Servicios Personas y Salud" (159646). CDQ pidió al equipo de pricing transferir los BSAs y stand-alone modifiers — pero el mapping por ShipTo × Ref sigue **incompleto**.
- **Modelo de negocio "reactivo por determinación":** consumibles Molecular (Aptima, HSV, HIV) y kits van a **0 €** en el pedido, se facturan después por contralbarán según nº de tests Panther.
- **Stand-alone modifier del Grupo Quirón:**
  - **List Line 40409338** — Description: **GMC.ES.Cyto.Q.22.011871** — G Quirón
  - Effective Date: **10-JUL-2023 → 08-JUL-2027**
  - Type: Discount → deja precio a **0 €**
- **BSAs específicos por ref:**
  - **BSA 3123233** — ATEC CANISTER a 35 €/pack — auto-renew 12M activo pero **modifier no triggea** — **Ticket CDQ OT1286446 abierto 02/07 pero cerrado sin fix** → reabierto 10/07/2026.
  - **BSA 3126757** — EVIVA_0913-12T y EVIVA_NG09L — funciona correctamente.
- **ShipTos con problemas de mapping conocidos:**
  - Hospital Público Infanta Sofía (San Sebastián de los Reyes, 28702)
  - Clínica Esperanza de Triana (Sevilla, 41011)
  - Hospital Quirón Santa Cristina Albacete (02003)
  - Quirón Barcelona
  - Quirón Huelva
  - Lab Hospital A Coruña (site: 159646)
- **PO patrón:** enviado desde `pedidos.ceco@quironsalud.es` (Portal proveedores Quirón), formato AC26XXXXX.
- **Acción estándar:** M.O. a 0 € (o al precio contractual) + escalar CC&T para añadir ShipTo/ref al List Qualifier del modifier.

### 🟢 Central Provincial de Compras de Granada (BillTo 152691)

- **Servicio Andaluz de Salud (SAS)** — contratos CPR (Central Provincial).
- **BSA activo:** 3112009 — pero con **precio DESACTUALIZADO** (105 €/caja para 70671-001) vs precio real contractual (109,09 €/caja).
- **Quote pendiente de cargar:** **GMC.ES.Cyto.T.26.037336** (30/06/2026, KAM **Pablo Lorenzo**).
  - Precio confirmado: 70671-001 = **0,22 €/Unidad = 109,09 €/pack** (500 uds).
  - Fecha en la quote: 18/05/2022–18/05/2024 (expiradas — Pablo debe emitir fechas efectivas nuevas).
- **Pendientes con Pablo desde 25/06/2026 (no respondidos):**
  1. Enlace de H1 (campo H1 Opportunity name vacío).
  2. Fechas efectivas reales.
  3. Duración del contrato (¿extender o nuevo GMC?).
- **PO patrón:** `siglo.sspa@juntadeandalucia.es` — formato XXXXXXX/26.
- **Acción estándar:** M.O. a 109,09 €/pack citando la quote y confirmación de Pablo por email.

### 🟠 Plataforma Logística Servicio Murciano de Salud (BillTo 195002)

- **BSA principal:** 3127305 (GMC.ES.Cyto.Q.26.036844 aceptada — 07/06/2026 KAM Carlos Gabaldón).
- **Precio contractual referencias tinción (70780-001, 70781-002, 70793-001):** **331,00 €/pack**.
- **Problema recurrente:** el BSA 3127305 no dispara automáticamente en **70793-001** (BLUING) para esta cuenta — mapeo incompleto.
- **Otros patrones históricos:**
  - Week 37 (junio) → miscalculación de decimales Oracle vs cliente. Solved.
  - Week 38-40 → múltiples PRQs recurrentes por PTWP en la referencia 70793-001.
- **PO patrón:** enviado desde `carolina.escobedo@carm.es` — formato 44215XXXXX.
- **Acción estándar:** M.O. a 331 €/pack para 70793-001 (aplicar modifier del BSA 3127305 manualmente) + escalar CDQ.

### 🟡 Hospital Universitario Infanta Sofía (BillTo 131588)

- **Cliente:** Empresa Pública Hospital del Norte — CIF S2800537I.
- **NO confundir con la cuenta IDCQ/Quirón Infanta Sofía (Lab Público Infanta Sofía ShipTo=3084786).** Esta es la pública **131588**.
- **Quote activa:** **GMC.ES.Cyto.Q.26.034054** (08/02/2026, KAM **Sonia Duque**, ACCEPTED). Vigencia **08/02/2026 → 07/02/2030**.
- **BSAs cargados:** 3120473 (líneas 1-5) y 3121436 (líneas tinción 6-10). Ambos triggean correctamente.
- **Precios contractuales confirmados quote:**
  - 70098-002 = 950,00 €/pack (12 cajas anuales)
  - 70099-001 = 1.074,00 €/pack
  - 70303-001 = 107,50 €/pack
  - ASY-14753 = 323,00 €/pack
  - 70205-001 = 304,50 €/pack
  - 70372-001 = 23,37 €/pack
  - **70408-002 = 86,40 €/pack (PACK INDIVISIBLE 4 botellas)**
  - 70671-001 = 180,00 €/pack
  - Tinciones (70779, 70780, 70781, 70782, 70793) = 82,40 €/pack cada una
- **PO patrón:** `ndmartin@salud.madrid.org` — formato 5502XXXXXX + expediente CM-A/SUM-XXXXXXXXXX/2026.
- **Error CWPU recurrente:** cliente pide en UN sueltas 70408-002 (Cytolyt) al precio del pack → siempre pedir PO corregido (mismo criterio SO 3129047 Getafe).

### 🟣 Hospital Universitario Ntra. Sra. de la Candelaria (BillTo 132743)

- **Cliente:** Servicio Canario de la Salud (Q9150013B).
- ⚠️ **Canarias usa IGIC 7%, NO IVA 21%.**
- **BSA activo:** 3111851 — **precios DESACTUALIZADOS**.
- **Quote de referencia:** **GMC.ES.Cyto.Q.22.004091** (Expediente 23-22-SU-DG-A-E001). **Prórroga venció en marzo/2026** — pendiente renovación por KAM Pablo Lorenzo.
- **Precios del concurso vigente (aún aplicados por el cliente):**
  - 70098-002 = 760,00 €/pack
  - 70671-001 = **0,00 €/pack (FOC — cepillos gratis en este concurso)**
- **PO patrón:** `sumhunsc.scs@gobiernodecanarias.org` — formato 4503XXXXXX.
- **ShipTo:** Almacén Suministros "La Nave", Polígono La Campana, 38109 El Rosario (Tenerife).
- **Acción estándar:** M.O. a precios del concurso (760 € y 0 €) + escalar Pablo para GMC actualizado.

### 🔴 Corporació Sanitària Parc Taulí (BillTo 258149)

- **Cliente:** Consorci Corporació Sanitària Parc Taulí de Sabadell — CIF Q5850005I.
- **Divisiones cruzadas** en el mismo pedido: Breast + Surgical + Diagnostic. Los BSAs son distintos por división:
  - **BSA 3115183** — TUMARK-E13-S — 980 €/pack
  - **BSA 3111797** — 3-255-0004 — 9,50 €/EA
  - **BSA 3111846** — 10-403FC — 1.669,50 €/pack (556,50 €/UN)
  - **BSA 3112119** — (a nombre del ICS Institut Català de la Salut) — cobertura Surgical
- **Patrón recurrente CWPU:** cliente Parc Taulí siempre expresa cantidades en **UN sueltas**, Oracle reagrupa correctamente en packs. Precios coinciden después de conversión.
- **PO patrón:** `compracomandes@tauli.cat` — formato 4500XXXXXX.
- **Precedentes:**
  - SO 3128343 (PO 4500334053) — CWPU/PTBA.
  - SO 3128880 (PO 4500335972, 06/07) — CWPU — ticket OT1287779.
  - SO 3129236 (PO 4500336787, 10/07) — CWPU — sin discrepancia real (Oracle=PO). Bookear directo.
- **Acción estándar:** verificar que Oracle reagrupó bien las UN en packs → si Extended coincide con PO base → bookear directo. Categoría CWPU.

### 🟤 Corporació de Salut del Maresme i la Selva (BillTo 408937)

- **Cliente:** Corporació de Salut del Maresme i la Selva — CIF G-62743125.
- **BSA 3124409** — creado 16/04/2026 por Pedro Moronta a partir de quote **GMC.ES.Cyto.Q.25.027998** (KAM Monica Martinez). Vigencia 21/10/2025 → 31/07/2026 (auto-renew 12M).
- ⚠️ **Sospecha de error de carga en el BSA 3124409** — Oracle aplica precios notablemente inferiores al PO del cliente:
  - 70671-001: Oracle 24 €/pack vs PO 120 €/pack (ratio 5x)
  - 70098-002: Oracle 230 €/pack vs PO 575 €/pack (ratio 2,5x)
- Los ratios inconsistentes sugieren error de unidad/pack al cargar los precios.
- **PO patrón:** `sgonzalez@salutms.cat` — formato MGC-4500XXXXXX.
- **ShipTo:** MAGATZEM CENTRAL, Primer de Maig 3 (2-5) Nau 9, 17300 Blanes.
- **Acción estándar:** ESCALAR A MONICA MARTINEZ (KAM) antes de bookear — verificar precio real de la quote GMC.ES.Cyto.Q.25.027998.

### ⚪ Otros clientes referenciados

- **Consorci Hospital Clínic de Barcelona (134361):**
  - **BSA 3112012** — 10-403FC con precio 1.575 € pero debería ser 1.725 € — necesitan GMC para corregir (Maite, 09/07).
  - Necesita nuevo GMC de Nat o del concurso vigente.
- **Hospital Universitario de Getafe:**
  - Mismo error CWPU en 70408-002 (SO 3129047, ticket OT1289132).
- **Central Provincial de Compras de Huelva (152711):**
  - CWNP en 70098-002 histórico 875 € — Maite escaló a Pablo el 01/07, sin respuesta.

---

## 🔧 Workflow estándar de resolución

```
1. RECIBIR PRQ
   ├── Identificar BillTo → consultar sección "Patrones por cuenta"
   ├── Identificar ShipTo → verificar mapping
   └── Identificar refs → consultar "Reglas de producto"

2. VERIFICAR ORACLE
   ├── Selling Price (NO List Price — Orbit puede confundir)
   ├── Sales Agreement field (¿vacío o rellenado?)
   ├── Extended Price
   └── UOM y Qty

3. VERIFICAR PO CLIENTE
   ├── Precio por unidad × unidades = importe base
   ├── ¿Precio unitario × pack size = precio Oracle pack? (regla CWPU)
   ├── IVA 21% o IGIC 7% (Canarias)
   └── ShipTo mencionado en el PO

4. COMPARAR
   ├── Match total c/IVA → bookear directo (aún si el Selling Price/UN difiere)
   ├── Oracle < PO → INFRAFACTURACIÓN (peligro) → NO bookear, escalar KAM
   ├── Oracle > PO → sobrefacturación potencial → M.O. bajar
   └── Falta línea → CSE, pedir corrección CS

5. CATEGORIZAR (tabla taxonomía)

6. REDACTAR EMAIL (plantillas)
   ├── OK bookear → M.O. + justificación + categorización
   ├── NO bookear → pedir PO corregido / esperar KAM / escalar CDQ
   └── Escalar CDQ → recurrencia, evidencia histórica, exigir fix estructural

7. REGISTRAR EN HUDDLE (PRQ_LOG_SEMANA_XX.md)
```

---

## ⚠️ Errores comunes / Lessons learned

1. **NUNCA confundir List Price con Selling Price.** El Orbit Report a veces muestra List. Verificar siempre en la extracción TSV o en el pantallazo real de Oracle.
2. **Cytolyt 70408-002 = PACK INDIVISIBLE de 4 botellas.** Nunca se vende por botella suelta. Si el cliente pide "12 UN a 86,40 €/UN" quiere 12 botellas físicas = 3 packs = 259,20 €, NO 1.036,80 €.
3. **PO Price "(blank)" en Orbit NO significa CWNP automáticamente.** Puede ser un 0 € contractual explícito (modelo reactivo por determinación Quirón).
4. **Grupo Quirón (IDCQ 3084786) tiene el modifier stand-alone Grupo Quirón** (List Line 40409338 / GMC.ES.Cyto.Q.22.011871) que debe aplicarse manualmente cuando no triggea. Nombre del modifier en Oracle: "IBR - Grupo Quirón S".
5. **Canarias = IGIC 7%**, no IVA 21%. Cuidado con los totales.
6. **Parc Taulí siempre pide en UN sueltas** — Oracle reagrupa en packs. Si el Extended de Oracle coincide con el importe del PO, **no hay discrepancia real** aunque el precio unitario difiera.
7. **CDQ cierra tickets sin resolver.** Cuando se detecte un ticket cerrado sin fix técnico (como OT1286446), REABRIR con evidencia de recurrencia. Exigir que el ticket permanezca abierto hasta que haya "technical root-cause analysis posted".
8. **Auto-renew de BSAs no siempre funciona en Oracle.** Cuando el BSA tiene auto-renew activo pero sigue sin triggear, es un bug conocido — no cerrar el ticket sin fix.
9. **La quote es la SUPREMA fuente de verdad** para el precio contractual — si Oracle no coincide con la quote es error de carga del BSA.
10. **KAMs con historial de tardanza en responder:** Pablo Lorenzo (varias PRQs pendientes desde 25/06 sobre Granada y Huelva). Escalar a Santiago si silencio prolongado.

---

## 📞 Contactos clave

### KAMs por división y zona

| KAM | División | Zona/Cuentas | Email |
|---|---|---|---|
| **Pablo Lorenzo** | Diagnostic | Andalucía (Granada, Huelva, Almería, Cádiz), Canarias | pablo.lorenzo@hologic.com |
| **Sonia Duque** | Diagnostic Cyto | Madrid pública (Infanta Sofía 131588) | sonia.duque@hologic.com |
| **Carlos Gabaldón** | Diagnostic Cyto | Murcia (Plataforma Logística 195002) | carlos.gabaldoncaballero@hologic.com |
| **Monica Martinez** | Diagnostic Cyto | Cataluña (Maresme 408937) | monica.martinez@hologic.com |
| **María Fernanda Mena** | GSS | Quirón Huelva | mariafernanda.mena@hologic.com |
| **Roberto Vega** | GSS | Asturias | roberto.vegagutierrez@hologic.com |
| **Alejandro Miralles** | GSS | Valencia | alejandro.miralles@hologic.com |
| **Hugo Gómez** | GSS | Puertollano | hugo.gomez@hologic.com |

### Interno Hologic

- **Customer Service (bookeo):** eOrdersIberia@hologic.com
- **CDQ (correcciones BSA/modifier):** EUCDQ@hologic.com
- **Manager (escalado):** Santiago Perala Vicente — santiago.peralavicente@hologic.com
- **Skip Manager:** Ben Thomas — ben.thomas@hologic.com
- **Team support Iberia:** Maite Vélez (Sales Support) — maite.velez@hologic.com
- **Team CC&T Iberia:**
  - Marisa Plaza Martín
  - Luca Cianchetti
  - Francesca Salvi
  - Vittoria Marranzini
  - Maite Vélez

### Externos (portales cliente)

| Cliente | Portal / Contacto pedidos |
|---|---|
| Grupo Quirónsalud | pedidos.ceco@quironsalud.es (portal proveedores.quironsalud.es) |
| SAS Andalucía | siglo.sspa@juntadeandalucia.es |
| SMS Murcia | carolina.escobedo@carm.es |
| SCS Canarias | sumhunsc.scs@gobiernodecanarias.org |
| Infanta Sofía (Madrid pública) | ndmartin@salud.madrid.org |
| Getafe (Madrid pública) | pedidos.hugf@salud.madrid.org |
| Maresme i Selva | sgonzalez@salutms.cat |
| Parc Taulí | compracomandes@tauli.cat |

---

## 📝 Plantillas de email por categoría

### PTWP / SEC — M.O. hacia arriba con quote pendiente de cargar
> Subject: SO [XXX] — [Cliente] — OK para bookear vía M.O. a [precio] (quote [GMC.XX.YY])
> Body: verificación tabla + origen precio + M.O. instructions + CC KAM pendientes

### PTBA — M.O. + escalado CC&T
> Subject: SO [XXX] — [Cliente]/[ShipTo] — OK para bookear vía M.O. al precio del cliente
> Body: BSA no triggea, aplicar modifier manualmente, ampliar ticket CC&T con este ShipTo/ref

### CWPU — Pedir PO corregido al cliente
> Subject: SO [XXX] — [Cliente] — Pedir PO corregido para línea [ref] (CWPU)
> Body: explicar pack indivisible, comparación importes, acción CS contactar cliente

### CSE — CS añadir línea faltante
> Subject: SO [XXX] — [Cliente] — Añadir línea [ref] faltante en el SO
> Body: PO trae X líneas, Oracle solo Y, falta ref [XXX], añadirla y bookear

### Escalado CDQ — Recurrencia sin fix
> Subject: Reopen [ticket] — [BSA] [ref] still not triggering — X PRQs since closure
> Body: inglés, evidencia recurrencia, exigir root-cause analysis y fix permanente

---

## 📊 Métricas y seguimiento

- **Huddle semanal:** viernes. Registrar todas las PRQs en `PRQ_LOG_SEMANA_XX_2026.md`.
- **Formato tabla huddle:** Pending Reason | División | Order Number | PO Number | Blanket | BillTo Name | BillTo Number | Why 1-5 | Root Cause | Action | Deadline | Comments | Status.

---

*Este archivo debe actualizarse cada vez que se detecte un nuevo patrón, un nuevo BSA relevante, o una nueva regla de producto. La consistencia en su mantenimiento es la clave para acelerar la resolución de futuras PRQs.*