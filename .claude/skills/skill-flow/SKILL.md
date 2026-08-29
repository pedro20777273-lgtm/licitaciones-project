---
name: skill-flow
description: "Dibuja el flujo de una skill instalada como diagrama Mermaid + página HTML: qué pasos ejecuta, qué ficheros carga y cuándo, y qué recursos no cita nadie. Úsala siempre que el usuario quiera ver, entender, auditar, comparar, documentar o adaptar cómo funciona una skill por dentro — incluidas frases como «cómo funciona la skill X», «enséñame el flujo de X», «quiero adaptar X», «diagrama de X», «qué hace X paso a paso» o «compara estas dos skills». También aplica cuando pregunten qué skills hay instaladas y en qué se diferencian."
---

# skill-flow

Una skill instalada es una caja negra: su `SKILL.md` puede tener cientos de
líneas de prosa y arrastrar `references/`, `scripts/` y `agents/` que se cargan
en momentos distintos. Para adaptarla hace falta ver primero **la forma**: qué
decide, en qué orden, y qué ficheros entran en contexto en cada paso.

Esta skill produce esa vista en dos diagramas complementarios y una página HTML.

## Reparto del trabajo: qué es medido y qué es interpretado

Esto importa porque el usuario va a **modificar** la skill a partir del diagrama,
y necesita saber de qué puede fiarse:

- `scripts/map_skill.py` lee el disco y no adivina nada: frontmatter, jerarquía
  de encabezados, inventario de ficheros y qué recursos cita el cuerpo. Es
  **medido**.
- El diagrama de procedimiento lo escribes tú leyendo el `SKILL.md`, porque
  extraer un flujo de prosa exige comprensión, no expresiones regulares. Es
  **interpretado**.

Di siempre cuál es cuál. Si un paso del flujo es una lectura tuya y no algo
literal del texto, márcalo en el propio nodo o en el resumen.

## Procedimiento

### 1. Localiza la skill

```bash
python3 scripts/map_skill.py --list
```

Busca en `.claude/skills/` del proyecto, en `~/.claude/skills/`, y en los
directorios sincronizados de claude.ai y de plugins. Si el usuario nombra una
skill que no aparece, muéstrale la lista en vez de suponer cuál quería.

### 2. Extrae el mapa estructural

```bash
python3 scripts/map_skill.py <nombre> --out skill-flow-out/<nombre>/map.json
```

El JSON trae `resources`, `reference_edges` (cuántas veces cita el cuerpo cada
fichero) y `orphans` (los que no cita nadie). Acepta también una ruta directa a
un directorio de skill, útil para una copia descomprimida que aún no está
instalada.

### 3. Lee el SKILL.md y escribe el flujo

Lee el `SKILL.md` completo. Guíate por los encabezados del mapa para saltar a
las secciones que describen el procedimiento, pero léelas de verdad: el flujo
real suele estar en la prosa, no en los títulos.

Escribe un `flowchart TD` de Mermaid en `skill-flow-out/<nombre>/procedure.mmd`
que capture:

- **Los pasos en orden**, con el verbo que usa la skill (`Ejecuta el script X`,
  no `Paso 3`). Un diagrama que solo numera pasos no ayuda a adaptar nada.
- **Los puntos de decisión** como rombos. Son lo primero que mira quien va a
  bifurcar la skill, así que no los aplanes en una secuencia recta.
- **Los bucles**, con una arista de vuelta y la condición de salida en la
  etiqueta. Muchas skills iteran hasta que el usuario da el visto bueno; un
  diagrama lineal esconde justo eso.
- **Dónde entra cada recurso**, conectando el paso con el fichero que carga.
  Es la unión entre los dos diagramas y lo que revela el coste real de contexto.

Mantén las etiquetas cortas y en el idioma del usuario. Si un paso solo aplica
en un entorno concreto (Claude.ai, Cowork, sin navegador), dilo en la etiqueta:
esas ramas son las que más a menudo hay que retocar al adaptar.

### 4. Renderiza la página

```bash
python3 scripts/render_flow.py skill-flow-out/<nombre>/map.json \
  --procedure skill-flow-out/<nombre>/procedure.mmd \
  --out skill-flow-out/<nombre>/flow.html
```

La página lleva los dos diagramas, las estadísticas, los huérfanos y el índice
de secciones, y deja visible el origen Mermaid para que se pueda editar y
versionar. Entrégasela al usuario con la herramienta de envío de ficheros si la
tienes; si no, dile la ruta.

### 5. Resume lo que sirve para adaptar

Tres o cuatro frases, no un volcado del diagrama. Lo que de verdad busca quien
va a modificar una skill:

- **Dónde está la decisión principal** y qué la gobierna.
- **Qué recursos son opcionales** frente a los que siempre se cargan, porque
  eso decide qué se puede quitar sin romperla.
- **Qué está sin citar.** Un fichero huérfano es dinero perdido o un enlace que
  falta, y en cualquier caso es lo primero que hay que resolver antes de tocar
  nada.
- **Qué asumiste.** Si el `SKILL.md` era ambiguo en un punto del flujo, dilo,
  para que el usuario no construya encima de una lectura tuya sin saberlo.

Si el usuario ya dijo qué quiere cambiar, lee `references/adapting.md` y
continúa; no lo cargues antes, porque solo aplica cuando la adaptación es el
objetivo y no la comprensión.

## Comparar dos skills

Ejecuta los pasos 1-3 con cada una y ponlas en una tabla: líneas de `SKILL.md`,
ficheros empaquetados, huérfanos, y en una frase la forma del flujo (lineal,
ramificado, iterativo). Las diferencias de forma explican por qué una dispara
en contextos donde la otra no, que suele ser la pregunta de fondo.

## Cuando el mapa y el texto no cuadran

`map_skill.py` cuenta menciones con coincidencia de texto y reconoce tres
formas de cita: ruta relativa, nombre de fichero suelto y forma de módulo
(`python -m scripts.foo`). Aun así puede errar: un recurso citado solo de
manera indirecta ("el script de agregación") saldrá como huérfano.

Antes de decirle al usuario que le sobra un fichero, comprueba en el `SKILL.md`
si se menciona en prosa. Reportar un huérfano falso es peor que no reportarlo:
le lleva a borrar algo que sí se usa.
