---
tipo: analisis
tags: [mejoras, gaps, escalado, roadmap]
fuentes: [síntesis de todas]
actualizado: 2026-07-14
---

# Áreas de mejora y plan de escalado

Página **viva**: se actualiza en cada ingesta/lint. Organizada en 4 bloques: gaps de cobertura,
deuda técnica del arsenal, automatizaciones de alto retorno, y escalado.

> ⚡ **Regla de esta página** (del contrato de interacción de Pedro): antes de proponer o construir
> un sistema nuevo, ejecutar lo pendiente de aquí. Máximo 2 opciones por decisión, con
> recomendación. Ver [pedro-moronta](entidades/pedro-moronta.md).

## ✅ Ejecutado el 2026-07-14 (con lo disponible en el repo)
- **`skills/` creado en formato Agent Skills** (carpeta por skill) — ver `skills/README.md` con
  el semáforo de ejecutabilidad por skill.
- **`find_item_v2.py` extraído a script ejecutable real** y probado (4/4 casos, BD de 334 ítems).
- **`rellenar_deuc.py` reconstruido** desde la especificación de SKILL 6 v4.0 y probado con XML
  sintético (rellena 11 campos, QC todo-True, aborta ante un Request). ⚠️ Validar con un
  ESPDResponse real antes de producción.
- **SKILL.md de A2 reconstruido** desde la plantilla Excel (contrato de 10 hojas documentado).
- **`comparison-dimensions.md` de A1 reconstruido**; estructura `hologic-tcs/` lista para poblar.
- **Check Aval operativizado**: contactos de bastanteo (plantilla), log de errores inicializado,
  carpeta de modelos CCAA con instrucciones.
- **Fuente única de datos fijos**: `skills/_shared/datos_fijos_hologic.md` (§2.3 resuelto para
  skills nuevas; las viejas se migran al tocarlas).
- **OCR de SKILL_5.pdf: intentado y NO viable** en este entorno (sin tesseract/poppler/PyPI).
  Confirmado: necesita re-subida en texto (§ preguntas abiertas 1).
- **Master prompt de Pedro ingerido** → contrato de interacción en `CLAUDE.md` y perfil en
  [pedro-moronta](entidades/pedro-moronta.md).

## 1. Gaps de cobertura del ciclo de vida

Del [mapa de skills](skills/mapa-skills.md), las fases sin skill:

| Gap | Impacto | Propuesta |
|---|---|---|
| **Detección de oportunidades** (fase 1) | Se depende de vigilancia manual de PLACSP/perfiles | Skill de vigilancia: filtrar publicaciones por CPV/palabras clave de las 3 divisiones, y volcarlas directo a [A2](skills/analisis-pliegos.md) |
| **Memoria técnica** (fase 4) | Hoy la hace el KAM; es el documento más laborioso del sobre B | Skill asistente: esqueleto desde los criterios de A2 + biblioteca de textos aprobados por producto, con chequeo anti-[contaminación](conceptos/contaminacion-sobres.md) integrado |
| **Carga y verificación de BSA** (fase 8) | ⚠️ **El gap más caro**: origen de la mayoría de PRQs internos (PTWP/PTNP/PTBA) — ver [cadena GMC→quote→BSA](conceptos/gmc-quote-bsa.md) | Skill "BSA Loader/Checker": comparar BSA cargado vs quote firmada línea a línea (precio, unidad, pack, vigencia, ShipTos mapeados) antes de darlo por bueno. El caso Maresme (BSA 3124409, error unit/pack) se habría evitado |
| **Radar de renovaciones** (fase 10) | Los SEC nacen de prórrogas vencidas sin GMC nuevo (Candelaria: vencida en marzo, detectada en julio vía PRQ) | Informe periódico de BSAs/contratos que expiran en 30-60-90 días con owner (KAM) y estado |
| **Subsanaciones y plazos** | Sin skill que gestione requerimientos de subsanación ni calendarice plazos del [cronograma de A2](skills/analisis-pliegos.md) | Integrar cronograma → recordatorios (calendario) |
| **Quotes DX (Diagnostics)** | Reconocido como pendiente en la propia [skill BSH](skills/quote-creation-bsh.md); DX es la división con más volumen de PRQs (7 de 9 en semana 28) | Crear `hologic-quote-creation-dx` con templates de los KAMs DX y regla de doble precio (€/test y €/pack) |

## 2. Deuda técnica del arsenal

1. **Assets ausentes**: casi todas las skills referencian archivos que no están en el repo —
   scripts (`rellenar_deuc.py`, `rellenar_indice/aval/declaracion.py`, `find_item_v2.py` completo),
   plantillas .docx, templates de KAM, modelos de aval por CCAA (17 PDFs), `CONTACTOS_BASTANTEO.md`,
   T&C de referencia de [A1](skills/screening-tc-pliegos.md), logs de errores. **Sin ellos las
   skills no son ejecutables desde aquí.** Acción: inventariar y traer a `row/` (o a un directorio
   `skills/` ejecutable).
2. **SKILL_5 ilegible** y **SKILL_A2 sin definición** (solo la plantilla Excel) — ver
   [skill-5-pendiente](skills/skill-5-pendiente.md) y [analisis-pliegos](skills/analisis-pliegos.md).
3. **Datos fijos duplicados** en 4+ skills (razón social, CIF, apoderado, domicilio con 2
   redacciones distintas). Acción: fuente única (ya canónica en
   [hologic-iberia](entidades/hologic-iberia.md)) que las skills referencien.
4. **Nombres y formatos inconsistentes**: SKILL_5/6/A1/A2/3_1 conviven con nombres descriptivos;
   solo 3 skills usan el formato estándar Agent Skill (frontmatter + references/). Acción: migrar
   todas al formato de [verificador-ofertas](skills/verificador-ofertas.md), una carpeta por skill.
5. **URLs frágiles de SharePoint/OneDrive** incrustadas en prompts (con parámetros `e=` de acceso).
   Acción: rutas relativas dentro del repo; SharePoint solo para lo que debe vivir allí (IBR).
6. **Extensiones erróneas al exportar** (xlsx como .md, pdf como .md, zip como .txt) — revisar el
   flujo de exportación/subida.
7. **Posible typo**: el email de trigger de quote BSH dice `pedro2777273@gmail.com` (el real parece
   `pedro20777273@gmail.com`). ⚠️ pendiente de confirmar con Pedro.
8. **Duplicados en `row/`**: `GUIA LOGICA.md` = `Guia de logica.md`; dos copias idénticas de la
   skill BSH se redujeron a una en la ingesta inicial.

## 3. Automatizaciones de alto retorno (nuevas, detectadas al cruzar fuentes)

1. **KAM chaser** — los pendientes con KAMs (Pablo Lorenzo: 3 sin respuesta desde 25/06) bloquean
   BSAs y generan PRQs. Recordatorio automático + escalado a Santiago a los X días. Ver [KAMs](entidades/kams.md).
2. **Tracker de tickets CDQ** — CDQ cierra tickets sin fix (OT1286446). Registro con estado,
   evidencia de recurrencia y regla "no cerrar sin root-cause analysis".
3. **Generador del log semanal de huddle** — la tabla de `PRQ_LOG_SEMANA_XX` (con 5-whys) se puede
   generar desde las resoluciones de la semana; hoy es manual. Métricas acumuladas → dashboard.
4. **Educación del comprador** — patrón CWPU Cytolyt recurrente en Madrid pública: plantilla de
   comunicación vía KAM (Sonia Duque) para cortar la causa raíz.
5. **Auditoría de BSAs de abril/2026** — si se confirma el error de carga del BSA 3124409, revisar
   todos los BSAs creados ese mes (misma mano, mismo posible bug).

## 4. Escalado

- **De prompts personales a repositorio versionado** (este repo): git da historial, revisión y
  colaboración. Siguiente paso natural: usar las skills como **Agent Skills de Claude Code**
  (carpeta por skill + SKILL.md + scripts ejecutables) para invocarlas por nombre en vez de pegar URLs.
- **Del individuo al equipo**: Maite (Sales Support) y el equipo CC&T podrían ejecutar las skills
  maduras (PRQ, verificador) si los recursos viven en el repo compartido. El
  [patrón de diseño](conceptos/patron-diseno-skills.md) documentado es la guía de onboarding.
- **Métrica de valor**: la propia skill PRQ ya define KPIs (tiempo de resolución ~30s, % resuelto
  sin abrir PDFs, 0 codes inventados). Extender la idea a tenders: tiempo de análisis de pliego,
  hallazgos del verificador por oferta, % de requerimientos sin subsanación.
- **Este cerebro como memoria compartida**: ingestas semanales (log de huddle → wiki) mantienen
  [cuentas clave](entidades/cuentas-clave.md) al día; el lint mensual detecta contradicciones.

## Preguntas abiertas para Pedro
1. ¿Qué contiene SKILL_5? (re-subir en texto)
2. ¿Existe el SKILL.md de A2 (análisis de pliegos)? (re-subir)
3. ¿Confirmas el typo del email en quote BSH (§2.7)?
4. ¿Quieres traer los assets/scripts al repo para que las skills sean ejecutables desde aquí?
5. ¿"Logic Tiberia" en tu nota era "Hologic Iberia"? (asumido que sí en toda la wiki)
