---
tipo: analisis
tags: [skills, mapa, ciclo-de-vida]
fuentes: [todas las skills de row/]
actualizado: 2026-07-14
---

# Mapa de skills — el arsenal completo sobre el ciclo de vida

Las 9 skills de Pedro, ordenadas según la fase del [ciclo de vida de una licitación](../conceptos/ciclo-vida-licitacion.md)
y su continuación en order management. Leyenda de madurez: 🟢 madura (versionada, con log de
errores) · 🟡 funcional · 🔴 incompleta o ilegible.

## Fase PRE-OFERTA (decidir si ir y con qué)

| # | Skill | Fase | Qué hace | Madurez |
|---|---|---|---|---|
| 1 | [Análisis de pliegos (A2)](analisis-pliegos.md) | Análisis | Extrae del pliego un Excel estructurado: resumen, cronograma, criterios, solvencias, penalidades, sobres | 🔴 solo se conserva la plantilla Excel; falta el SKILL.md |
| 2 | [Screening T&C vs pliegos (A1)](screening-tc-pliegos.md) | Análisis de riesgo | Compara T&C estándar Hologic contra el pliego → semáforo 🟢🟡🔴 de riesgos contractuales | 🟡 |
| 3 | [Creación de quotes BSH](quote-creation-bsh.md) | Oferta económica | Genera presupuestos .docx/.pdf desde datos GMC con templates por KAM | 🟢 v1.0, reglas muy afinadas |

## Fase OFERTA (preparar y presentar)

| # | Skill | Fase | Qué hace | Madurez |
|---|---|---|---|---|
| 4 | [Rellenado del DEUC (SKILL 6)](deuc.md) | Documentación administrativa | Rellena quirúrgicamente el XML ESPDResponse del visor español | 🟢 v4.0 (aprendió de 3 versiones fallidas) |
| 5 | [Verificador de ofertas](verificador-ofertas.md) | Chequeo final | Revisión exhaustiva anti-exclusión antes de subir al portal (9 bloques A-I, por lote) | 🟢 formato Agent Skill completo con references |

## Fase POST-ADJUDICACIÓN

| # | Skill | Fase | Qué hace | Madurez |
|---|---|---|---|---|
| 6 | [Requerimientos de documentación (SKILL 3.1)](requerimientos-documentacion.md) | Adjudicación | Genera índice de documentación + ficha de aval + declaraciones responsables (.docx con formato corporativo) | 🟢 formato Agent Skill con assets/scripts |
| 7 | [Check Aval (v1.1)](check-aval.md) | Garantía definitiva | Verifica palabra por palabra el borrador de aval bancario vs modelo oficial CCAA + requerimiento; genera email de bastanteo | 🟢 v1.1, aplicable a toda CCAA |

## Fase PEDIDOS / ORDER MANAGEMENT (post-contrato)

| # | Skill | Fase | Qué hace | Madurez |
|---|---|---|---|---|
| 8 | [PRQ Resolver (v1.5)](prq-resolver.md) | Pedidos | Diagnostica y resuelve Price Queries en Oracle: reason code oficial, BSA, emails, registro en huddle | 🟢 la más madura: 5 versiones, KB por cuenta, script, log semanal |

## Sin clasificar

| # | Skill | Estado |
|---|---|---|
| 9 | [SKILL 5 (PDF ilegible)](skill-5-pendiente.md) | 🔴 texto vectorizado, pendiente de OCR o re-subida |

## Flujo completo (cómo encajan)

```
DETECCIÓN* → [A2 Análisis pliegos] → [A1 Screening T&C] → decisión go/no-go
                                                              │
              [Quote BSH] + memoria técnica* + [DEUC] ────────┤
                                                              ▼
                                   [Verificador de ofertas] → PRESENTAR
                                                              │ (adjudicación)
              [Requerimientos 3.1] → [Check Aval] ────────────┤
                                                              ▼
                     CONTRATO → BSA en Oracle* → pedidos → [PRQ Resolver]
                                                              │
                          renovaciones / expiración* ◄────────┘
* = fase SIN skill (gap) — ver mejoras.md
```

Los gaps marcados con `*` se analizan en [mejoras.md](../mejoras.md). Nota clave: la fase
"BSA en Oracle" sin automatizar es la que genera la mayoría de los PRQs (SEC, PTBA, PTNP) que
luego la skill 8 tiene que apagar — ver [síntesis](../sintesis.md).
