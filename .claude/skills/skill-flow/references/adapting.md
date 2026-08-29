# Adaptar una skill sin romperla

Se lee cuando el usuario ya sabe qué quiere cambiar. Hasta entonces basta con
el diagrama.

## Primero: no edites la instalada

Las skills sincronizadas de claude.ai viven bajo
`~/.claude/skills/synced/<uuid>/` y **se sobrescriben al sincronizar**. Cualquier
cambio ahí se pierde sin aviso. Copia siempre a un sitio que tú controles:

```bash
cp -r ~/.claude/skills/synced/<uuid>/<nombre> .claude/skills/<nombre>-custom
```

Renombra también el campo `name` del frontmatter. Dos skills con el mismo nombre
en ámbitos distintos hacen ambigua la resolución, y acabas depurando cuál se
cargó en vez del cambio que querías.

## El orden que menos rompe

1. **Cambia la `description` la última.** Gobierna cuándo se dispara la skill,
   así que tocarla mientras pruebas el cuerpo mezcla dos variables: no sabrás si
   falló el flujo o si la skill ni siquiera se invocó.
2. **Recorta antes de añadir.** Quitar una rama que no usas hace el flujo más
   fácil de razonar, y las secciones que sobran gastan contexto en cada
   invocación.
3. **Mueve a `references/` lo que no se necesita siempre.** Si una sección solo
   aplica a un caso, sácala del cuerpo y apúntala desde él. Eso es divulgación
   progresiva y es la palanca real sobre el coste.
4. **Verifica los huérfanos.** Antes de borrar un fichero no citado, busca su
   nombre en todo el directorio: puede que lo importe otro script y no el
   `SKILL.md`.

## Qué se rompe con más frecuencia

- **Rutas relativas en los scripts.** Muchas skills asumen que el directorio de
  trabajo es el de la skill. Al copiarla a otro sitio, comprueba cada `python3
  scripts/...` del cuerpo.
- **Encabezados que el cuerpo referencia por nombre.** Renombrar una sección
  rompe los punteros internos del tipo "ve a la sección X".
- **Bloques específicos de entorno.** Las ramas de Claude.ai, Cowork o sin
  navegador suelen estar al final y se pasan por alto; si tu entorno cae en una
  de ellas, es la primera que hay que adaptar.

## Comprobar el cambio

Vuelve a pasar `/skill-flow` sobre tu copia y compara el diagrama con el
original. Si la forma cambió donde no esperabas, el cambio hizo más de lo que
creías. Es una comprobación barata y detecta justo lo que una lectura del diff
no ve: que una rama se quedó huérfana o que un bucle se volvió lineal.
