# Log de la wiki (append-only)

Formato: `## [YYYY-MM-DD] operacion | descripción`. Últimas entradas: `grep "^## \[" wiki/log.md | tail -5`

## [2026-07-14] setup | Creación del segundo cerebro
Se instancia el patrón LLM Wiki (Karpathy): `CLAUDE.md` (esquema), estructura `wiki/`
(skills/conceptos/entidades/fuentes), index y este log. Fuentes: 18 archivos ya cargados en `row/`.

## [2026-07-14] ingest | Lote inicial completo de row/ (18 fuentes)
- 7 skills de licitaciones + 1 de order management ingeridas → 9 páginas en `skills/`.
- Conceptos destilados: ciclo de vida, DEUC, contaminación de sobres, causas de exclusión,
  garantía/aval, PRQ/reason codes, BSA vs standalone, cadena GMC→quote→BSA, patrón de diseño de skills.
- Entidades: Pedro, Hologic Iberia (datos fijos canónicos), divisiones, KAMs, cuentas clave, sistemas.
- Análisis inicial: `sintesis.md` (3 tesis) y `mejoras.md` (6 gaps de cobertura, 8 puntos de deuda
  técnica, 5 automatizaciones nuevas, plan de escalado, 5 preguntas abiertas a Pedro).
- Incidencias de ingesta: `SKILL_5.pdf` ilegible (texto vectorizado, pendiente OCR/re-subida);
  `SKILL_A2` solo trae la plantilla Excel (falta el SKILL.md); huddle tracker es export crudo de
  Excel con bajo valor textual; duplicados detectados (GUIA LOGICA, skill BSH ×2).
