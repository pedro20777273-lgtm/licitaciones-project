# CLAUDE.md — Esquema del Segundo Cerebro de Pedro Moronta

Este repositorio es un **segundo cerebro** construido con el patrón **LLM Wiki** (Karpathy):
una wiki persistente, interconectada y mantenida por el LLM, que compila el conocimiento de
Pedro Moronta — **Tender Specialist en Hologic Iberia, S.L.U.** (~1 año en el puesto) — sobre
**automatización de licitaciones públicas (tenders), order management y diseño de skills**.

El objetivo: tener disponible todo el conocimiento creado, entender cada skill y su propósito,
detectar áreas de mejora y formas de escalar, y hacer el trabajo más eficiente y gestionable.

## Arquitectura (3 capas)

| Capa | Ruta | Quién la escribe | Regla |
|---|---|---|---|
| **Fuentes crudas** | `row/` | Pedro (sube archivos) | **INMUTABLE**. El LLM lee, nunca modifica. |
| **La wiki** | `wiki/` | El LLM (siempre) | El LLM crea, actualiza y enlaza páginas. Pedro la lee. |
| **El esquema** | `CLAUDE.md` | LLM + Pedro (co-evoluciona) | Este archivo. Define convenciones y flujos. |

## Estructura de la wiki

```
wiki/
├── index.md            ← catálogo de TODAS las páginas (actualizar en cada ingesta)
├── log.md              ← registro cronológico append-only (ingestas, consultas, lint)
├── sintesis.md         ← visión general: qué es este cerebro y su tesis
├── mejoras.md          ← áreas de mejora, gaps y plan de escalado (página viva)
├── skills/             ← una página por skill (qué hace, cómo se usa, estado, conexiones)
│   └── mapa-skills.md  ← hub: todas las skills sobre el ciclo de vida de una licitación
├── conceptos/          ← conceptos de dominio (DEUC, aval, sobres, PRQ, BSA...)
├── entidades/          ← personas, empresa, divisiones, cuentas, sistemas
└── fuentes/
    └── catalogo-fuentes.md  ← mapeo archivo de row/ → páginas wiki + estado de ingesta
```

## Convenciones de página

- **Idioma:** español (términos técnicos en inglés cuando son los oficiales: BSA, PO, reason code).
- **Frontmatter YAML** en cada página: `tipo` (skill | concepto | entidad | analisis | fuente),
  `tags`, `fuentes` (archivos de `row/` de los que deriva), `actualizado` (YYYY-MM-DD).
- **Enlaces:** markdown relativo (`[DEUC](../conceptos/deuc-espd.md)`) — funcionan en GitHub y Obsidian.
  Toda página debe tener enlaces entrantes y salientes: **ninguna página huérfana**.
- **Páginas de skill** siguen la plantilla: Propósito · Cómo se invoca · Flujo · Datos/recursos que
  necesita · Estado y madurez · Conexiones · Riesgos y notas.
- No inventar datos. Lo no verificable se marca `⚠️ pendiente de verificar` o se registra como gap
  en `mejoras.md`.

## Operaciones

### Ingesta (nueva fuente)
1. Pedro deposita el archivo en `row/` (o una subcarpeta) y pide procesarlo.
2. Leer la fuente completa. Comentar con Pedro los puntos clave si hay ambigüedad.
3. Actualizar/crear las páginas afectadas de `wiki/` (una fuente puede tocar 5-15 páginas).
4. Señalar contradicciones con conocimiento previo **explícitamente** en la página afectada.
5. Actualizar `index.md`, `fuentes/catalogo-fuentes.md` y añadir entrada en `log.md`.

### Consulta
1. Leer `index.md` primero para localizar páginas relevantes; después profundizar.
2. Responder citando páginas de la wiki (y fuente original si aplica).
3. Si la respuesta genera síntesis valiosa (comparación, análisis, decisión), **archivarla como
   página nueva** en la wiki — las exploraciones también componen.

### Lint (salud de la wiki)
Periódicamente revisar: contradicciones entre páginas, datos obsoletos, páginas huérfanas,
conceptos mencionados sin página propia, enlaces rotos, gaps de datos. Registrar el pase en `log.md`.

## Formato del log

Entradas append-only con prefijo grep-able:
```
## [2026-07-14] ingest | Nombre de la fuente
## [2026-07-14] query | Pregunta resumida
## [2026-07-14] lint  | Resultado del chequeo
```
(`grep "^## \[" wiki/log.md | tail -5` da las últimas 5 operaciones.)

## Contexto fijo del dominio

- **Pedro Moronta** — Tender Specialist, Hologic Iberia S.L.U. (CC&T Iberia: España + Portugal).
  Ver `wiki/entidades/pedro-moronta.md`.
- Dos áreas de trabajo: **licitaciones públicas españolas (LCSP 9/2017)** y **order management
  (Price Queries / PRQ, Oracle)**. Las skills cubren fases de ambos ciclos:
  ver `wiki/skills/mapa-skills.md`.
- Datos fijos de empresa (CIF, domicilio, apoderado) en `wiki/entidades/hologic-iberia.md` —
  **fuente única de verdad** dentro de la wiki; las skills los duplican y eso es un gap conocido.

## Git

- Fuentes nuevas y actualizaciones de wiki se commitean juntas con mensaje
  `wiki: ingesta <fuente>` / `wiki: lint` / `wiki: consulta <tema>`.
- Nunca commitear cambios que modifiquen archivos existentes de `row/` (solo se añaden).
