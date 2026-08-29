# graphify — instalación, memoria y contexto

Notas de la instalación de `graphify` v0.9.52 (paquete PyPI `graphifyy`) y de cómo
encaja su modelo de memoria y contexto.

## Instalación

```bash
uv tool install graphifyy      # o: pipx install graphifyy
graphify install               # registra la skill en el asistente (~/.claude, ~/.codex, ...)
```

En este repo la skill quedó registrada a nivel de proyecto en
`.claude/skills/graphify/` (SKILL.md + `references/`), por lo que `/graphify`
está disponible sin tocar la configuración global del usuario.

El CLI expone dos ejecutables: `graphify` y `graphify-mcp` (servidor MCP para
que un agente consulte el grafo como herramienta).

## El pipeline

```
detect() → extract() → build() → cluster() → analyze → report.generate() → export.to_*()
```

Cada etapa vive en su propio módulo y se comunica con dicts de Python y grafos
de NetworkX. No hay estado compartido ni efectos fuera de `graphify-out/`.
`graphify/cli.py::dispatch_command()` es el punto único que orquesta todas las
etapas (119 aristas salientes en el grafo: llama a `extract()`, `cluster()`,
`generate()`, `build_merge()`, `to_json()`, `install()`…).

El código se parsea con tree-sitter en local (~40 lenguajes, sin LLM, nada sale
de la máquina). Solo el pase semántico sobre docs/PDFs/imágenes/vídeo usa un
backend LLM, y únicamente si se configura una API key.

## Qué queda "en memoria" — los cuatro almacenes

Todo persiste en `graphify-out/`, y son cuatro cosas distintas:

| Ruta | Qué es | Quién la escribe |
|---|---|---|
| `graph.json` | El grafo completo: nodos, aristas, comunidades. Es *el contexto* consultable. | `build()` / `cluster()` |
| `cache/ast/<versión>/<sha>.json` | Caché de extracción por fichero, con clave de hash de contenido. | `extract()` |
| `manifest.json` | `mtime` + `ast_hash` + `semantic_hash` por fichero; es la puerta incremental que decide qué re-extraer. | `save_manifest()` |
| `memory/*.md` + `reflections/LESSONS.md` | Memoria de trabajo: preguntas, respuestas y si sirvieron. | `save-result` / `reflect` |

`graph.json` es contexto estructural (qué existe y cómo se conecta).
`memory/` es contexto episódico (qué se preguntó y qué resultó útil).
`cache/` y `manifest.json` no son conocimiento: son solo la maquinaria para no
recalcular lo que no cambió.

## El bucle de memoria

```
graphify query "..."  ->  graphify save-result --question ... --answer ... --outcome useful|dead_end|corrected
                                      |
                                      v
                          graphify-out/memory/<fecha>_<slug>.md   (markdown con front-matter)
                                      |
                                      v
                          graphify reflect  ->  reflections/LESSONS.md
```

`reflect()` es determinista, sin LLM: `load_memory_docs()` lee los docs ordenados
por fecha, `aggregate_lessons()` los agrupa por comunidad del grafo y
`render_lessons_md()` escribe el resumen. Aplica decaimiento temporal
(`--half-life-days`, 30 por defecto) y exige corroboración
(`--min-corroboration`, 2 por defecto) antes de marcar un nodo como fiable;
por debajo de ese umbral lo etiqueta **Tentative**. `report.py::load_learning_for_report()`
reinyecta esas lecciones en el informe, cerrando el bucle.

## Cómo se consulta el contexto

- `graphify query "<pregunta>"` — recorrido BFS (o `--dfs`) con presupuesto de tokens (`--budget`).
- `graphify path "A" "B"` — camino más corto entre dos conceptos (por defecto dirigido; `--undirected` si no hay camino).
- `graphify explain "X"` — el nodo, su comunidad, su grado y sus vecinos.
- `graphify affected "X"` — recorrido inverso: qué se rompe si cambias X.
- `graphify god-nodes` — los hubs arquitectónicos por grado.

Cada arista lleva su etiqueta de confianza: `EXTRACTED` (explícito en el código),
`INFERRED` (deducido en el segundo pase) o `AMBIGUOUS` (marcado para revisión).

## Resultado sobre el propio código de graphify

Ejecutado con `graphify extract <ruta> --code-only` + `cluster-only --no-label`:

- 458 ficheros de código → **12.006 nodos, 24.951 aristas, 610 comunidades**
- 97% EXTRACTED · 3% INFERRED (778 aristas, confianza media 0,85) · 0% AMBIGUOUS
- Coste LLM: 0 tokens de entrada y salida (solo AST local)
- Benchmark: ~800.400 tokens si se leyera el corpus entero frente a ~17.261 por
  consulta contra el grafo → **46,4x menos tokens**
- God nodes: `extract()` (548), `build_from_json()` (210), `_rebuild_code()` (158),
  `detect()` (126), `dispatch_command()` (119)

Los nombres de comunidad quedaron como `Community N` porque el etiquetado usa un
LLM y no hay backend configurado; se resuelve con `graphify label <ruta>` una vez
haya API key.

## Notas de esta instalación

- Extras opcionales no instalados: `sql`, `dm`, `commonlisp` — 9 ficheros del
  corpus de prueba no aportaron nodos por eso. Se arreglan con
  `pip install "graphifyy[sql]"` y equivalentes.
- Este repo (`licitaciones-project`) todavía no tiene código: `graphify extract .`
  encuentra 0 ficheros de código y el grafo sale vacío. Volverá a tener sentido
  en cuanto haya fuentes.
