---
tipo: skill
tags: [licitaciones, screening, tc, semaforo, riesgo-contractual]
fuentes: [row/SKILL_A1_tc_vs_pliegos.md]
actualizado: 2026-07-14
---

# Skill A1 — Screening T&C Hologic vs pliegos

## Propósito
Comparar las condiciones estándar de Hologic (T&C por división y tipo de contrato) contra lo que
exige el pliego, y producir un **informe semáforo** de riesgos contractuales antes de ofertar.
Es el filtro de riesgo del go/no-go.

## Cómo se invoca
Triggers: "screening de esta licitación", "compara nuestras condiciones con el pliego",
"¿hay algún red flag?", "semáforo", "chequeo previo". Formato Agent Skill con frontmatter YAML.

## Flujo
1. **Determinar tipo de contrato** (suministro/servicio/mixto), **división**
   ([BSH/DX/GSS](../entidades/divisiones-hologic.md)) y **modelo comercial** (venta, reagent
   rental, solo servicio) → carga el T&C de `references/hologic-tcs/{division}/{tipo}/terms.md`.
2. **Comparar dimensiones** (4 categorías): financieras (plazo de pago, facturación, revisión de
   precios, garantías), servicio (SLAs, mantenimiento, repuestos, uptime), legales (duración,
   penalidades, responsabilidad, seguros, subcontratación, jurisdicción) y compliance (RGPD,
   residuos, idiomas cooficiales).
3. **Clasificar**: 🟢 compatible · 🟡 atención · 🔴 conflicto · ⚪ no comparable.
   Reglas concretas (ej.: plazo de pago del pliego menor que estándar Hologic → 🔴).
4. **Output Excel** de 4 hojas: resumen ejecutivo, detalle, acciones requeridas (solo 🔴🟡 con
   responsable sugerido), datos del pliego. + resumen en chat con riesgo global LOW→CRITICAL.

## Datos que necesita
- **T&C por división/tipo en `references/hologic-tcs/`** — ⚠️ la estructura está definida pero los
  archivos de T&C reales **no están en el repo**. La skill degrada a ⚪ GRIS si faltan, y ofrece
  extraerlos de quotes/contratos subidos. Gap en [mejoras](../mejoras.md).

## Conexiones
- Se apoya en el output de [A2 análisis de pliegos](analisis-pliegos.md) (su hoja 4 lo abrevia).
- Sus 🔴 anticipan cláusulas que después aparecerán en el contrato y en los
  [T&C de las quotes](quote-creation-bsh.md).
- Fase de análisis del [ciclo de vida](../conceptos/ciclo-vida-licitacion.md).

## Notas
- Los "responsables sugeridos" (Commercial, Legal, Finance, Service, Tender Specialist) implican
  que el output sirve como herramienta de coordinación interna, no solo análisis.
