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

## [2026-07-14] build | skills/ ejecutable + reconstrucciones ("haz lo que puedas y ejecuta")
- Creada la capa `skills/` (formato Agent Skills, 8 skills migradas + `_shared/datos_fijos`).
- `find_item_v2.py` extraído del markdown a script real y probado (4/4).
- `rellenar_deuc.py` reconstruido desde la spec v4.0 y probado con XML sintético (pendiente
  validación con ESPDResponse real). SKILL.md de A2 y comparison-dimensions de A1 reconstruidos.
- OCR de SKILL_5.pdf intentado y no viable en este entorno (sin tesseract/PyPI) → re-subir en texto.
- `mejoras.md` actualizado con lo ejecutado. `CLAUDE.md` amplía la arquitectura con la capa skills/.

## [2026-07-14] ingest | master_prompt_pedro_julio2026.md 🔒
Perfil personal completo de Pedro (sensible). Actualiza `entidades/pedro-moronta.md`, añade el
"contrato de interacción" a `CLAUDE.md` (foco, cierre, 2 opciones+recomendación, acción con fecha,
anti-evitación) y la regla de acción-primero en `mejoras.md`. Aviso registrado: mantener repo privado.
