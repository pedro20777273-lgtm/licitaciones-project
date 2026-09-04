# everything-claude-code — instalación selectiva

Origen: https://github.com/affaan-m/everything-claude-code (MIT, Affaan Mustafa)
Fecha de instalación: 2026-09-04
Modo: **selectivo** — se instala todo el contenido, pero solo se activan los hooks no intrusivos.

## Qué está activo (`.claude/settings.json`)

| Evento | Script | Función |
|---|---|---|
| SessionStart | `scripts/hooks/session-start.js` | Informa de sesiones previas y skills aprendidas |
| PreCompact | `scripts/hooks/pre-compact.js` | Registra el evento antes de compactar contexto |
| SessionEnd | `scripts/hooks/session-end.js` | Persiste el estado de la sesión en `~/.claude/sessions/` |
| SessionEnd | `scripts/hooks/evaluate-session.js` | Sugiere extraer patrones reutilizables de la sesión |

Los cuatro scripts se han probado en este entorno: salida correcta, `exit=0`, sin red ni escritura fuera de `~/.claude/sessions/` y `~/.claude/skills/learned/`.

## Qué NO se ha activado (y por qué)

Están en `reference/hooks-full.example.json` por si algún día se quieren:

- **Bloqueo de ficheros `.md`** — impide crear cualquier `.md` salvo README/CLAUDE/AGENTS/CONTRIBUTING. Incompatible con un proyecto documental de licitaciones.
- **Bloqueo de `npm run dev` fuera de tmux** y avisos de tmux — irrelevante aquí.
- **Prettier + `tsc --noEmit` automáticos** tras cada edición `.ts/.js` — ejecutan `npx` (descarga de paquetes) en cada edición.
- **Avisos de `console.log`** en PreToolUse/Stop — ruido sin proyecto JS.
- **`suggest-compact.js`** en PreToolUse — lanza un proceso node en cada edición para un aviso cada 50 llamadas.

## Contenido instalado

- `agents/` (9): architect, build-error-resolver, code-reviewer, doc-updater, e2e-runner, planner, refactor-cleaner, security-reviewer, tdd-guide
- `commands/` (14): `/plan`, `/verify`, `/checkpoint`, `/code-review`, `/tdd`, `/orchestrate`, `/learn`, `/e2e`, `/eval`, `/build-fix`, `/refactor-clean`, `/test-coverage`, `/update-docs`, `/update-codemaps`, `/setup-pm`
- `skills/` (11): backend-patterns, clickhouse-io, coding-standards, continuous-learning, eval-harness, frontend-patterns, project-guidelines-example, security-review, strategic-compact, tdd-workflow, verification-loop
- `rules/` (8) y `contexts/` (3)
- `reference/`: configuración MCP de ejemplo, hooks completos, README original, plugin.json

### Correcciones aplicadas
Tres skills (`eval-harness`, `project-guidelines-example`, `verification-loop`) venían sin frontmatter YAML y por tanto Claude Code no las habría cargado. Se les ha añadido `name` + `description`.

### Nota de pertinencia
El paquete está orientado a desarrollo de software (TypeScript, tests, ClickHouse, frontend). Para el trabajo de licitaciones son directamente útiles: `/plan`, `/verify`, `/checkpoint`, `/learn`, `continuous-learning`, `verification-loop` y `strategic-compact`. El resto queda como referencia.

### MCP
`reference/mcp-servers.example.json` **no está activo**: contiene marcadores `YOUR_*_HERE`. No pongas ahí tokens reales — este fichero está versionado en git.
