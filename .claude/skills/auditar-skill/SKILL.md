---
name: auditar-skill
description: Audita una skill existente y dibuja su funcionamiento interno como diagrama de flujo (cajas, rombos de decisión y flechas conectadas, sobre fondo oscuro y con colores) publicado como artifact, junto a una ficha de auditoría con disparadores, entradas, salidas, recursos y puntos ciegos. Úsala siempre que el usuario pregunte cómo funciona una skill por dentro, pida "auditar", "revisar", "explicar", "verificar", "renderizar" o "dibujar" una skill, quiera un diagrama de flujo / flowchart / esquema de un SKILL.md, o diga cosas como "¿qué hace realmente esta skill?", "enséñame el flujo de la skill X", "audit this skill", "diagram how this skill works". Aplícala aunque el usuario no diga la palabra "diagrama" — si quiere entender el mecanismo de una skill, esta es la herramienta.
---

# Auditar una skill y dibujar su flujo

El objetivo es que alguien que no ha leído el `SKILL.md` entienda, mirando un
solo dibujo, **qué dispara la skill, qué decide por dentro, qué ficheros carga
y qué produce** — y que además vea lo que un auditor vería: los puntos donde la
skill es ambigua, frágil o depende de algo no declarado.

Un diagrama genérico de cuatro cajas ("Leer → Procesar → Generar → Entregar")
no sirve para nada: eso ya se lo imagina cualquiera. El valor está en dibujar
el mecanismo **real** de esa skill concreta, con sus condiciones literales.

## 1. Localiza la skill

Si el usuario da un nombre y no una ruta, búscala en este orden:

```bash
find ./.claude/skills ~/.claude/skills ~/.claude/plugins \
     -maxdepth 5 -name SKILL.md 2>/dev/null | grep -i "<nombre>"
```

Si hay varias coincidencias, o ninguna, pregunta antes de seguir en vez de
adivinar: auditar la skill equivocada desperdicia todo el trabajo.

## 2. Léela de verdad

1. Lee el `SKILL.md` **entero**, incluido el frontmatter. La `description` es
   el disparador real de la skill, así que es el primer nodo del diagrama.
2. Inventaría los recursos: `ls -R` sobre la carpeta. Anota `scripts/`,
   `references/` y `assets/`.
3. Abre los recursos que **condicionan el flujo** (los que el SKILL.md manda
   leer según un caso, y los scripts que ejecuta). No hace falta leer enteros
   los ficheros de referencia largos: basta con saber qué contienen y en qué
   punto se cargan.

## 3. Extrae el mecanismo

Antes de dibujar nada, ten identificado:

- **Disparo**: qué frases o contextos activan la skill (de la `description`).
- **Entradas**: qué espera recibir (fichero, ruta, texto, nada).
- **Decisiones**: cada punto donde la skill bifurca, con su criterio literal
  ("¿el PDF tiene campos AcroForm?", "¿el usuario pidió assertions?").
- **Cargas diferidas**: qué reference o script se lee, y bajo qué condición.
  Esto es lo que más se le escapa a quien lee la skill por encima.
- **Bucles**: iteraciones y reintentos (revisión → feedback → reescritura).
- **Salidas**: qué queda al final y dónde.
- **Puntos ciegos**: pasos sin criterio de decisión, dependencias no
  declaradas, instrucciones contradictorias, casos que la skill no cubre.

## 4. Escribe el spec del diagrama

Guarda un JSON en el scratchpad con esta forma:

```json
{
  "titulo": "nombre-de-la-skill",
  "nodos": [
    {"id": "t",  "tipo": "trigger",  "texto": "Frase que activa la skill", "nota": "matiz opcional"},
    {"id": "p1", "tipo": "proceso",  "texto": "Paso concreto que ejecuta"},
    {"id": "d1", "tipo": "decision", "texto": "¿Criterio literal de la bifurcación?"},
    {"id": "r1", "tipo": "recurso",  "texto": "Carga references/x.md", "nota": "solo si ..."},
    {"id": "s1", "tipo": "salida",   "texto": "Qué entrega y dónde"},
    {"id": "x1", "tipo": "riesgo",   "texto": "Punto ciego detectado"}
  ],
  "aristas": [
    {"de": "t",  "a": "p1"},
    {"de": "d1", "a": "r1", "texto": "sí", "tipo": "si"},
    {"de": "d1", "a": "s1", "texto": "no", "tipo": "no"},
    {"de": "x1", "a": "p1", "texto": "reintenta", "tipo": "bucle"}
  ]
}
```

Tipos de nodo: `trigger`, `proceso`, `decision`, `recurso`, `salida`, `riesgo`.
Tipos de arista: normal (omítelo), `si`, `no`, `bucle` — cambian el color de la
flecha para que las ramas se distingan de un vistazo.

Reglas que mantienen el diagrama legible:

- Entre 8 y 18 nodos. Por debajo es un dibujo vacío; por encima nadie lo lee.
  Si la skill es enorme, dibuja el flujo principal y menciona las ramas
  secundarias en la ficha de texto.
- El texto de cada nodo es una acción o una pregunta concreta, en 4-9 palabras.
  Usa `nota` para la condición o el matiz, no alargues el texto principal.
- **Todo nodo conectado**: sin cajas sueltas. El script avisa si detecta alguna.
- Las decisiones salen siempre con sus dos ramas etiquetadas (`sí` / `no`), o
  el lector no sabe qué camino se toma.

## 5. Renderiza

```bash
python3 <carpeta-skill>/scripts/render_flow.py spec.json -o diagrama.svg
```

El script coloca los nodos por capas, ordena cada fila para minimizar cruces,
rutea las flechas en ortogonal con codos redondeados y saca los bucles por un
canal a la derecha. No toques las coordenadas a mano: si el dibujo no queda
bien, arregla el spec (menos nodos, textos más cortos) y vuelve a lanzarlo.

Comprueba el SVG antes de publicarlo — un diagrama con flechas cruzadas o
etiquetas solapadas es peor que ninguno:

```bash
/opt/pw-browsers/chromium --headless --no-sandbox --disable-gpu \
  --screenshot=check.png --window-size=1000,900 --hide-scrollbars diagrama.svg
```

y mira el PNG. (Fuera de este entorno, usa el visor de imágenes que tengas.)

## 6. Publica el artifact

Escribe un HTML que embeba el SVG **inline** (no lo enlaces: un `<img src>` a
un fichero local no carga en el artifact) y publícalo con la herramienta
Artifact. Estructura, en este orden:

1. **Cabecera**: nombre de la skill, su ruta, y una línea de qué hace.
2. **El diagrama**, dentro de un contenedor con `overflow-x: auto`.
3. **Ficha de auditoría**, en secciones cortas:
   - *Cuándo se dispara* — cita literal de la `description`.
   - *Entradas y salidas*.
   - *Recursos* — tabla fichero / para qué / cuándo se carga.
   - *Puntos ciegos* — lo que has detectado en el paso 3, cada uno con una
     frase de por qué importa. Esta sección es la que justifica la palabra
     "auditoría"; si la dejas vacía, di explícitamente que no encontraste
     nada, en vez de omitirla.

Mantén el artifact en fondo oscuro para que case con el diagrama, y usa la
misma paleta que el SVG:

| elemento | color |
|---|---|
| fondo | `#0d1117` |
| texto | `#e6edf3` / apagado `#8b97a8` |
| disparador | `#a78bfa` |
| paso | `#38bdf8` |
| decisión | `#fbbf24` |
| recurso | `#34d399` |
| salida | `#f472b6` |
| riesgo | `#f87171` |

## Qué no hacer

- No inventes pasos que la skill no tiene para "cuadrar" el dibujo. Si algo no
  está claro en el SKILL.md, eso **es** un hallazgo: dibújalo como `riesgo`.
- No resumas la skill en prosa larga. El texto acompaña al diagrama, no lo
  sustituye.
- No uses mermaid aquí. Se renderiza, pero no permite el control de color,
  forma y ruteo que hace legible una auditoría en fondo oscuro.
