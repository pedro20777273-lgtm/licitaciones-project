#!/usr/bin/env python3
"""Renderiza un diagrama de flujo (SVG, fondo oscuro) a partir de un spec JSON.

Uso:
    python3 render_flow.py spec.json -o diagrama.svg

El spec describe el funcionamiento interno de una skill como nodos y aristas.
El script se encarga del layout, del ruteo ortogonal de las flechas y de la
paleta, para que quien lo usa solo tenga que pensar en la lógica, no en las
coordenadas. Ver la cabecera de SKILL.md para el esquema del spec.
"""

import argparse
import json
import sys
from collections import defaultdict, deque

# --- Paleta (fondo oscuro) -------------------------------------------------
BG = "#0d1117"
GRID = "#161d29"
TEXT = "#e6edf3"
MUTED = "#8b97a8"
EDGE = "#5b6b82"

TIPOS = {
    # tipo:        (color, relleno, forma)
    "trigger":  ("#a78bfa", "#1e1b34", "stadium"),
    "proceso":  ("#38bdf8", "#0e2233", "rect"),
    "decision": ("#fbbf24", "#2b2410", "hex"),
    "recurso":  ("#34d399", "#0e2a22", "doc"),
    "salida":   ("#f472b6", "#2c1424", "stadium"),
    "riesgo":   ("#f87171", "#2c1517", "warn"),
}

W = 250          # ancho de caja
PAD_X = 46       # separación horizontal entre columnas
PAD_Y = 74       # separación vertical entre filas
MARGIN = 46
LH = 17          # alto de línea del texto principal
LH_N = 14        # alto de línea de la nota
CHAR = 6.55      # ancho medio de carácter a 12.5px


def wrap(texto, ancho_px, char=CHAR):
    max_chars = max(8, int(ancho_px / char))
    palabras, lineas, actual = texto.split(), [], ""
    for p in palabras:
        prueba = f"{actual} {p}".strip()
        if len(prueba) <= max_chars:
            actual = prueba
        else:
            if actual:
                lineas.append(actual)
            actual = p
    if actual:
        lineas.append(actual)
    return lineas or [""]


def esc(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


def rank_nodes(ids, edges):
    """Asigna una fila a cada nodo por camino más largo desde las raíces.

    Las aristas de retorno (bucles) se ignoran para el ranking; se detectan con
    un DFS y se rutean aparte, porque si no el layout se vuelve circular.
    """
    hijos = defaultdict(list)
    for e in edges:
        hijos[e["de"]].append(e["a"])

    estado, back = {}, set()

    def dfs(n):
        estado[n] = 1
        for h in hijos[n]:
            if estado.get(h) == 1:
                back.add((n, h))
            elif estado.get(h) is None:
                dfs(h)
        estado[n] = 2

    con_padre = {e["a"] for e in edges if (e["de"], e["a"]) not in back}
    raices = [n for n in ids if n not in {e["a"] for e in edges}] or [ids[0]]
    for r in raices:
        if estado.get(r) is None:
            dfs(r)
    for n in ids:
        if estado.get(n) is None:
            dfs(n)

    fwd = [e for e in edges if (e["de"], e["a"]) not in back]
    indeg = {n: 0 for n in ids}
    for e in fwd:
        indeg[e["a"]] += 1
    orden, cola = [], deque([n for n in ids if indeg[n] == 0])
    while cola:
        n = cola.popleft()
        orden.append(n)
        for h in [e["a"] for e in fwd if e["de"] == n]:
            indeg[h] -= 1
            if indeg[h] == 0:
                cola.append(h)
    orden += [n for n in ids if n not in orden]

    fila = {n: 0 for n in ids}
    for n in orden:
        for e in fwd:
            if e["de"] == n:
                fila[e["a"]] = max(fila[e["a"]], fila[n] + 1)
    con_padre  # noqa: B018  (documental)
    return fila, back


def layout(nodos, edges):
    ids = [n["id"] for n in nodos]
    byid = {n["id"]: n for n in nodos}
    fila, back = rank_nodes(ids, edges)

    for n in nodos:
        color, fill, forma = TIPOS.get(n.get("tipo", "proceso"), TIPOS["proceso"])
        n["_lineas"] = wrap(n["texto"], W - 34)
        n["_nota"] = wrap(n["nota"], W - 34, char=5.9) if n.get("nota") else []
        alto = 26 + LH * len(n["_lineas"]) + (LH_N * len(n["_nota"]) + 6 if n["_nota"] else 0)
        n["_h"] = max(52, alto)
        n["_color"], n["_fill"], n["_forma"] = color, fill, forma

    filas = defaultdict(list)
    for n in nodos:
        filas[fila[n["id"]]].append(n)

    # Ordena cada fila por el baricentro de sus padres: menos cruces de flechas.
    padres = defaultdict(list)
    for e in edges:
        if (e["de"], e["a"]) not in back:
            padres[e["a"]].append(e["de"])
    pos_en_fila = {}
    for f in sorted(filas):
        grupo = filas[f]
        if f > 0:
            grupo.sort(key=lambda n: (
                sum(pos_en_fila.get(p, 0) for p in padres[n["id"]]) / len(padres[n["id"]])
                if padres[n["id"]] else 99))
        for i, n in enumerate(grupo):
            pos_en_fila[n["id"]] = i

    max_cols = max(len(g) for g in filas.values())
    total_w = max_cols * W + (max_cols - 1) * PAD_X
    y = MARGIN
    for f in sorted(filas):
        grupo = filas[f]
        ancho = len(grupo) * W + (len(grupo) - 1) * PAD_X
        x0 = MARGIN + (total_w - ancho) / 2
        alto_fila = max(n["_h"] for n in grupo)
        for i, n in enumerate(grupo):
            n["_x"] = x0 + i * (W + PAD_X)
            n["_y"] = y + (alto_fila - n["_h"]) / 2
        y += alto_fila + PAD_Y

    return byid, back, MARGIN * 2 + total_w, y - PAD_Y + MARGIN


def forma_path(n):
    x, y, h = n["_x"], n["_y"], n["_h"]
    f = n["_forma"]
    if f == "stadium":
        return f'<rect x="{x}" y="{y}" width="{W}" height="{h}" rx="{h/2}" ry="{h/2}"'
    if f == "hex":
        c = 18
        pts = f"{x+c},{y} {x+W-c},{y} {x+W},{y+h/2} {x+W-c},{y+h} {x+c},{y+h} {x},{y+h/2}"
        return f'<polygon points="{pts}"'
    if f == "doc":
        return f'<rect x="{x}" y="{y}" width="{W}" height="{h}" rx="6" ry="6"'
    if f == "warn":
        return f'<rect x="{x}" y="{y}" width="{W}" height="{h}" rx="6" ry="6"'
    return f'<rect x="{x}" y="{y}" width="{W}" height="{h}" rx="12" ry="12"'


def dibuja_nodo(n):
    dash = ' stroke-dasharray="6 4"' if n["_forma"] in ("doc", "warn") else ""
    o = [f'{forma_path(n)} fill="{n["_fill"]}" stroke="{n["_color"]}" stroke-width="1.8"{dash}/>']
    cx = n["_x"] + W / 2
    ty = n["_y"] + 14 + (n["_h"] - (LH * len(n["_lineas"]) + (LH_N * len(n["_nota"]) + 6 if n["_nota"] else 0))) / 2
    for ln in n["_lineas"]:
        o.append(f'<text x="{cx}" y="{ty}" fill="{TEXT}" font-size="12.5" font-weight="600" '
                 f'text-anchor="middle" font-family="ui-sans-serif,system-ui,sans-serif">{esc(ln)}</text>')
        ty += LH
    if n["_nota"]:
        ty += 4
        for ln in n["_nota"]:
            o.append(f'<text x="{cx}" y="{ty}" fill="{MUTED}" font-size="11" text-anchor="middle" '
                     f'font-family="ui-sans-serif,system-ui,sans-serif">{esc(ln)}</text>')
            ty += LH_N
    return "\n".join(o)


def anclas(n):
    return {
        "top": (n["_x"] + W / 2, n["_y"]),
        "bottom": (n["_x"] + W / 2, n["_y"] + n["_h"]),
        "left": (n["_x"], n["_y"] + n["_h"] / 2),
        "right": (n["_x"] + W, n["_y"] + n["_h"] / 2),
    }


def dibuja_arista(e, byid, es_back, max_x, orden=0):
    a, b = byid[e["de"]], byid[e["a"]]
    color = {"si": "#34d399", "no": "#f87171", "bucle": "#a78bfa"}.get(e.get("tipo"), EDGE)
    marker = {"si": "ok", "no": "no", "bucle": "loop"}.get(e.get("tipo"), "d")
    puntos, lx, ly = [], 0, 0

    if es_back:
        x1, y1 = anclas(a)["right"]
        x2, y2 = anclas(b)["right"]
        canal = max_x + 26
        d = f"M {x1} {y1} H {canal} V {y2} H {x2}"
        puntos = [(x1, y1)]
        lx, ly = canal + 8, (y1 + y2) / 2
        anchor = "start"
    else:
        x1, y1 = anclas(a)["bottom"]
        x2, y2 = anclas(b)["top"]
        puntos = [(x1, y1)]
        # La etiqueta va pegada al nodo de destino: en el punto medio de la
        # flecha chocaria con las etiquetas de sus hermanas.
        lx, ly, anchor = x2, y2 - 9, "middle"
        if abs(x1 - x2) < 2:
            d = f"M {x1} {y1} V {y2}"
        else:
            # El codo va siempre en el hueco justo debajo del origen: si se
            # pusiera en el punto medio, una flecha que salta dos filas
            # dejaria su etiqueta encima de las cajas intermedias.
            # Escalona el codo entre las flechas que salen del mismo nodo: si
            # todas giran a la misma altura, sus etiquetas se pisan.
            my = min(y1 + PAD_Y / 2 - (orden % 3) * 11, y2 - 12)
            r = 10
            sx = 1 if x2 > x1 else -1
            d = (f"M {x1} {y1} V {my - r} Q {x1} {my} {x1 + sx*r} {my} "
                 f"H {x2 - sx*r} Q {x2} {my} {x2} {my + r} V {y2}")

    o = [f'<path d="{d}" fill="none" stroke="{color}" stroke-width="1.7" '
         f'marker-end="url(#f-{marker})" opacity="0.95"/>']
    for px, py in puntos:
        o.append(f'<circle cx="{px}" cy="{py}" r="3.2" fill="{color}"/>')
    if e.get("texto"):
        t = esc(e["texto"])
        o.append(f'<text x="{lx}" y="{ly}" fill="{color}" font-size="10.5" font-weight="600" '
                 f'text-anchor="{anchor}" font-family="ui-sans-serif,system-ui,sans-serif" '
                 f'paint-order="stroke" stroke="{BG}" stroke-width="4">{t}</text>')
    return "\n".join(o)


def leyenda(tipos_usados, x, y):
    o, cx = [], x
    etiquetas = {"trigger": "Disparador", "proceso": "Paso", "decision": "Decisión",
                 "recurso": "Carga recurso", "salida": "Salida", "riesgo": "Riesgo / punto ciego"}
    for t in tipos_usados:
        color = TIPOS[t][0]
        o.append(f'<rect x="{cx}" y="{y-9}" width="12" height="12" rx="3" fill="{TIPOS[t][1]}" '
                 f'stroke="{color}" stroke-width="1.6"/>')
        o.append(f'<text x="{cx+18}" y="{y+1}" fill="{MUTED}" font-size="11.5" '
                 f'font-family="ui-sans-serif,system-ui,sans-serif">{etiquetas[t]}</text>')
        cx += 26 + len(etiquetas[t]) * 6.6
    return "\n".join(o), cx


def render(spec):
    nodos, edges = spec["nodos"], spec["aristas"]
    ids = {n["id"] for n in nodos}
    for e in edges:
        for k in ("de", "a"):
            if e[k] not in ids:
                sys.exit(f"ERROR: la arista apunta a un nodo inexistente: {e[k]}")

    conectados = {e["de"] for e in edges} | {e["a"] for e in edges}
    sueltos = [i for i in ids if i not in conectados]
    if sueltos and len(nodos) > 1:
        print("AVISO: nodos sin ninguna flecha (el diagrama quedara desconectado): "
              + ", ".join(sueltos), file=sys.stderr)

    byid, back, w, h = layout(nodos, edges)
    max_x = max(n["_x"] + W for n in nodos)
    labels_back = [e.get("texto", "") for e in edges if (e["de"], e["a"]) in back]
    if labels_back:
        # El canal de retorno va por la derecha; reserva sitio para su etiqueta.
        w = max(w, max_x + 60 + int(max(len(t) for t in labels_back) * 6.4))

    tipos_usados = [t for t in TIPOS if any(n.get("tipo", "proceso") == t for n in nodos)]
    h_leyenda = 34 if tipos_usados else 0
    y_leyenda = h + 4
    h += h_leyenda

    defs = "".join(
        f'<marker id="f-{k}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" '
        f'orient="auto-start-reverse"><path d="M 0 0 L 10 5 L 0 10 z" fill="{c}"/></marker>'
        for k, c in (("d", EDGE), ("ok", "#34d399"), ("no", "#f87171"), ("loop", "#a78bfa")))

    partes = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w:.0f} {h:.0f}" '
        f'width="100%" role="img" aria-label="{esc(spec.get("titulo", "Diagrama de flujo"))}">',
        f'<defs>{defs}<pattern id="rejilla" width="26" height="26" patternUnits="userSpaceOnUse">'
        f'<path d="M 26 0 L 0 0 0 26" fill="none" stroke="{GRID}" stroke-width="1"/></pattern></defs>',
        f'<rect width="{w:.0f}" height="{h:.0f}" fill="{BG}"/>',
        f'<rect width="{w:.0f}" height="{h:.0f}" fill="url(#rejilla)"/>',
    ]
    hermanas = defaultdict(int)
    for e in edges:
        k = e["de"]
        partes.append(dibuja_arista(e, byid, (e["de"], e["a"]) in back, max_x, hermanas[k]))
        hermanas[k] += 1
    for n in nodos:
        partes.append(dibuja_nodo(n))
    if tipos_usados:
        leg, _ = leyenda(tipos_usados, MARGIN, y_leyenda + 12)
        partes.append(leg)
    partes.append("</svg>")
    return "\n".join(partes)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("spec")
    ap.add_argument("-o", "--out", default="-")
    a = ap.parse_args()
    with open(a.spec, encoding="utf-8") as f:
        svg = render(json.load(f))
    if a.out == "-":
        print(svg)
    else:
        with open(a.out, "w", encoding="utf-8") as f:
            f.write(svg)
        print(f"OK -> {a.out}")


if __name__ == "__main__":
    main()
