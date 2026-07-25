---
name: screening-pliegos
description: "Screen and compare Hologic standard Terms & Conditions against public tender requirements, producing a traffic-light (red/amber/green) compliance report. Use this skill whenever the user wants to compare Hologic T&Cs vs tender terms, screen a tender for contractual risks, check payment terms or service commitments against a pliego, do a pre-bid compliance review, or mentions: screening, comparar términos, T&C check, semáforo, red flags, condiciones contractuales vs pliego, revisión administrativa, payment terms, facturación, penalidades. Triggers on phrases like 'revisa los T&C contra este pliego', 'screening de esta licitación', 'compara nuestras condiciones con el pliego', 'hay algún red flag', 'chequeo previo'."
---

# Screening de Pliegos — Comparación T&C Hologic vs Pliego

## Purpose

Compare Hologic's standard contractual terms (stored in `references/hologic-tcs/`) against the terms and conditions found in a public tender, producing a traffic-light compliance report that flags mismatches, risks, and items requiring commercial decision.

## When to Use

- User uploads tender documents and asks to check for contractual risks
- User wants to compare Hologic T&Cs vs tender requirements
- User asks for a pre-bid screening or compliance review
- User mentions: screening, semáforo, red flags, T&C check, comparar condiciones

## Trigger Phrases

- "Screening de esta licitación"
- "Compara nuestras condiciones con este pliego"
- "Revisa los T&C contra el pliego"
- "Hay algún red flag en este pliego?"
- "Chequeo previo de [expediente]"
- "Semáforo de esta licitación"

---

## Step 1 — Determine Contract Type and Division

From the tender documents, identify:

1. **Contract type** (tipo de contrato):
   - `suministro` — supply of equipment, consumables, reagents
   - `servicio` — maintenance, service contracts, outsourced services
   - `mixto` — combined supply + service

2. **Division** (división Hologic):
   - `bsh` — Breast & Skeletal Health (mammography, bone densitometry)
   - `dx` — Diagnostics (ThinPrep, Panther, Aptima, Genius)
   - `gss` — GYN Surgical Solutions
   - `surgical` — Surgical (if distinct from GSS in the region)

3. **Commercial model** (modelo comercial):
   - Instrument rental + consumable purchase
   - Reagent rental (cost of instrument embedded in consumable price)
   - Capital purchase (outright sale)
   - Service-only contract (maintenance)

Based on this determination, load the appropriate Hologic T&C file:

```
references/hologic-tcs/{division}/{contract_type}/terms.md
```

If multiple T&C files could apply (e.g., mixed contract), load all relevant ones.

**If the T&C file doesn't exist yet**: inform the user which file is missing and which folder to place it in. Continue the analysis using any available T&C files, noting gaps.

---

## Step 2 — Extract Comparison Dimensions

Read the reference file `references/comparison-dimensions.md` for the full list of dimensions to compare. In summary, the key categories are:

### Financial / Administrative
- Payment terms (plazo de pago)
- Billing frequency (periodicidad facturación)
- Billing format (factura electrónica, plataforma)
- Price revision / escalation
- Guarantees (provisional, definitiva)
- Penalties for late payment (by either party)
- Currency, taxes (IVA/IGIC)

### Service / Maintenance
- SLA response times
- SLA resolution times
- Preventive maintenance frequency
- Spare parts (original vs compatible)
- Coverage scope (what's included/excluded)
- Uptime / availability commitments
- Reporting obligations
- Personnel requirements (certifications, accreditation)

### Legal / Contractual
- Contract duration
- Renewal / extension terms
- Termination clauses
- Penalty regime (types, caps, accumulation)
- Liability caps
- Insurance requirements (RC minimum)
- IP / data ownership
- Confidentiality
- Subcontracting rules
- Force majeure
- Applicable law and jurisdiction

### Compliance / Regulatory
- Data protection (RGPD)
- Environmental (waste management)
- Labor law compliance
- Equality plans
- Language requirements (Catalan, Basque, etc.)

---

## Step 3 — Perform the Comparison

For each dimension found in the tender documents:

1. **Extract the tender requirement** — exact text or summary with article reference
2. **Extract the Hologic standard term** — from the loaded T&C file
3. **Classify the match**:

| Color | Meaning | Criteria |
|-------|---------|----------|
| 🟢 VERDE | Compatible | Hologic T&C meets or exceeds the tender requirement |
| 🟡 ÁMBAR | Attention needed | Partial match, minor deviation, or requires internal confirmation |
| 🔴 ROJO | Conflict / Risk | Hologic T&C contradicts or cannot meet the tender requirement |
| ⚪ GRIS | Not comparable | Dimension present in tender but absent from Hologic T&Cs (or vice versa) |

**Classification rules:**
- Payment terms: RED if tender demands shorter payment than Hologic standard (e.g., tender says 30 days but Hologic standard is 60 days)
- Penalties: RED if tender penalties exceed caps Hologic typically accepts; AMBER if within range but aggressive
- SLAs: RED if tender SLAs are stricter than what Hologic commits to in standard service contracts
- Insurance: RED if tender minimum exceeds Hologic standard coverage
- Subcontracting: AMBER if tender restricts subcontracting in ways that could affect Hologic operations
- Language: AMBER if tender requires documentation/communications in a regional language not currently covered
- Price revision: AMBER if tender explicitly prohibits price revision on multi-year contracts

---

## Step 4 — Generate Output

### Primary output: Excel workbook

Read the xlsx skill first:
```
view /mnt/skills/public/xlsx/SKILL.md
```

Generate an Excel with the following sheets:

#### Sheet 1: Resumen ejecutivo
Columns: Categoría (w=25) | Total ítems (w=12) | 🟢 Verde (w=10) | 🟡 Ámbar (w=10) | 🔴 Rojo (w=10) | ⚪ Gris (w=10)

Summary counts per category (Financial, Service, Legal, Compliance).

#### Sheet 2: Detalle comparación
Columns: Nº (w=5) | Categoría (w=18) | Dimensión (w=25) | Requisito del pliego (w=55) | Ref. pliego (w=15) | Condición Hologic (w=55) | Ref. T&C (w=15) | Semáforo (w=10) | Comentario / Riesgo (w=50)

Use conditional formatting:
- Column "Semáforo": cell fill green/amber/red/gray based on classification
- Font colors: dark green (006100), dark yellow (9C5700), dark red (9C0006), gray (595959)

#### Sheet 3: Acciones requeridas
Only RED and AMBER items.
Columns: Nº (w=5) | Dimensión (w=25) | Semáforo (w=10) | Riesgo identificado (w=60) | Acción propuesta (w=60) | Responsable sugerido (w=20)

Suggested owners: Commercial, Legal, Finance, Service/FSE, Tender Specialist.

#### Sheet 4: Datos del pliego
Basic tender identification: expediente, órgano, objeto, importes, plazo, procedimiento. (Abbreviated version of resumen-pliegos output.)

### Secondary output: In-chat summary

After presenting the Excel, provide a brief in-chat summary:
- Total items compared
- Count by traffic light
- Top 3 RED items with one-line explanation
- Overall risk assessment: LOW / MEDIUM / HIGH / CRITICAL

---

## Step 5 — Save and Present

```python
filename = f"Screening_{expediente}_{organismo}.xlsx"
wb.save(f'/mnt/user-data/outputs/{filename}')
```

Present with `present_files` and provide the in-chat summary.

---

## T&C File Format

Each T&C file in `references/hologic-tcs/` should be a markdown file with this structure:

```markdown
# Hologic T&C — [Division] — [Contract Type] — [Region]

## Payment Terms
- Standard payment term: [X] days from invoice date
- Billing frequency: [monthly/quarterly/upon delivery]
- ...

## Service Commitments
- Response time: [X] hours
- Resolution time: [X] hours
- ...

## Penalties
- ...

## [Other sections as needed]
```

If T&C files are not yet loaded, the skill will:
1. Inform the user which files are missing
2. Tell them the exact path to place the files
3. Still perform the comparison using GRAY for all Hologic-side items
4. Offer to extract T&Cs from uploaded quote/contract documents

---

## Edge Cases

- **No T&C file available**: Run analysis anyway, flag all as GRAY on Hologic side, still extract tender requirements
- **Multiple divisions in one tender**: Load all relevant T&C files, note which applies to each lot
- **Tender in regional language**: Extract and translate to Spanish for the comparison
- **Mixed contract (supply + service)**: Load both T&C types, compare each section against the relevant T&C
- **User uploads a Hologic quote/contract**: Offer to extract T&Cs from it and save to the appropriate reference folder for future use
