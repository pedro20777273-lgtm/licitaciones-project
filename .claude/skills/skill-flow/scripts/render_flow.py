#!/usr/bin/env python3
"""Render a skill map plus a procedure diagram into one standalone HTML page.

Mermaid is inlined from ``assets/mermaid.min.js`` rather than pulled from a CDN,
so the page renders on a locked-down network and keeps working months later
when the CDN version has moved on. The diagrams also stay as readable source in
the page: the point of /skill-flow is understanding a skill well enough to
change it, and a picture whose source you cannot read does not help with that.
"""
from __future__ import annotations

import argparse
import html
import json
from pathlib import Path

PAGE = """<!doctype html>
<html lang="es"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Flujo de la skill: {name}</title>
<script>{mermaid_js}</script>
<style>
  :root {{ color-scheme: light dark; --bg:#fbfbfa; --fg:#1a1a18; --mut:#5f5f57;
           --line:#dcdcd6; --card:#fff; --warn:#b26a00; }}
  @media (prefers-color-scheme: dark) {{
    :root {{ --bg:#16161a; --fg:#ececea; --mut:#a0a09a; --line:#32323a;
             --card:#1e1e24; --warn:#e0a458; }} }}
  * {{ box-sizing:border-box }}
  body {{ margin:0; background:var(--bg); color:var(--fg); font:15px/1.6
          ui-sans-serif,system-ui,-apple-system,"Segoe UI",sans-serif; }}
  main {{ max-width:1100px; margin:0 auto; padding:32px 20px 80px }}
  h1 {{ font-size:26px; margin:0 0 4px }}
  h2 {{ font-size:19px; margin:38px 0 10px; padding-bottom:6px;
        border-bottom:1px solid var(--line) }}
  .sub {{ color:var(--mut); margin:0 0 22px }}
  .card {{ background:var(--card); border:1px solid var(--line);
           border-radius:10px; padding:18px; overflow-x:auto }}
  .grid {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(150px,1fr));
           gap:10px; margin:16px 0 }}
  .stat {{ background:var(--card); border:1px solid var(--line);
           border-radius:8px; padding:12px 14px }}
  .stat b {{ display:block; font-size:22px }}
  .stat span {{ color:var(--mut); font-size:12px }}
  .warn {{ border-left:3px solid var(--warn); padding-left:12px; color:var(--warn) }}
  details {{ margin-top:14px }}
  summary {{ cursor:pointer; color:var(--mut) }}
  pre {{ background:var(--bg); border:1px solid var(--line); border-radius:8px;
         padding:12px; overflow-x:auto; font-size:12.5px }}
  code {{ font-family:ui-monospace,SFMono-Regular,Menlo,monospace }}
  ul {{ margin:8px 0; padding-left:20px }}
  .desc {{ font-size:13.5px; color:var(--mut); border-left:3px solid var(--line);
           padding-left:12px; margin:10px 0 }}
</style></head><body><main>
<h1>{name}</h1>
<p class="sub"><code>{path}</code></p>
<div class="desc">{description}</div>
<div class="grid">
  <div class="stat"><b>{lines}</b><span>líneas en SKILL.md</span></div>
  <div class="stat"><b>{sections}</b><span>secciones (H2)</span></div>
  <div class="stat"><b>{nfiles}</b><span>ficheros empaquetados</span></div>
  <div class="stat"><b>{norphans}</b><span>no citados</span></div>
</div>
{orphan_note}
<h2>Flujo de trabajo</h2>
<div class="card"><pre class="mermaid">{procedure}</pre></div>
<details><summary>Ver el origen Mermaid</summary><pre><code>{procedure_src}</code></pre></details>
<h2>Cómo se carga (divulgación progresiva)</h2>
<div class="card"><pre class="mermaid">{assets}</pre></div>
<details><summary>Ver el origen Mermaid</summary><pre><code>{assets_src}</code></pre></details>
<h2>Secciones de SKILL.md</h2>
<div class="card">{toc}</div>
<script>
  mermaid.initialize({{ startOnLoad:true, securityLevel:'strict',
    theme: matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'default' }});
</script>
</main></body></html>
"""


def load_mermaid() -> str:
    """Return the vendored mermaid bundle, or a CDN tag if it is missing.

    Falling back rather than failing matters because the diagram source is the
    real deliverable; a page that needs the network is still better than no page.
    """
    vendored = Path(__file__).resolve().parent.parent / "assets" / "mermaid.min.js"
    if vendored.is_file():
        js = vendored.read_text(encoding="utf-8")
        # A literal </script> inside a JS string would close the inline block
        # early and leave the rest of the bundle rendered as page text.
        return js.replace("</script", "<\\/script")
    return ('document.write(\'<script src="https://cdnjs.cloudflare.com/ajax/'
            'libs/mermaid/11.4.1/mermaid.min.js"><\\/script>\');')


def build(data: dict, procedure: str) -> str:
    esc = html.escape
    res = data.get("resources", {})
    nfiles = sum(len(v) for v in res.values())
    orphans = data.get("orphans", [])
    note = ""
    if orphans:
        items = "".join(f"<li><code>{esc(o)}</code></li>" for o in orphans)
        note = ('<p class="warn">Ficheros que SKILL.md nunca menciona — al adaptar, '
                f'comprueba si sobran o si falta el enlace:</p><ul>{items}</ul>')
    toc = "".join(
        f'<div style="margin-left:{(h["level"] - 1) * 18}px">'
        f'<code>L{h["line"]}</code> {esc(h["title"])}</div>'
        for h in data["skill_md"]["headings"] if h["level"] <= 3
    ) or "<em>sin encabezados</em>"
    return PAGE.format(
        name=esc(data["name"]), path=esc(data["path"]),
        description=esc(data.get("description", "")) or "<em>sin descripción</em>",
        lines=data["skill_md"]["lines"],
        sections=sum(1 for h in data["skill_md"]["headings"] if h["level"] == 2),
        nfiles=nfiles, norphans=len(orphans), orphan_note=note,
        procedure=esc(procedure), procedure_src=esc(procedure),
        assets=esc(data["mermaid_assets"]), assets_src=esc(data["mermaid_assets"]),
        toc=toc, mermaid_js=load_mermaid(),
    )


def main() -> int:
    ap = argparse.ArgumentParser(description="Render a skill map to HTML.")
    ap.add_argument("map_json", help="map.json produced by map_skill.py")
    ap.add_argument("--procedure", required=True,
                    help="file holding the procedure flowchart in Mermaid")
    ap.add_argument("--out", required=True, help="HTML output path")
    args = ap.parse_args()

    data = json.loads(Path(args.map_json).read_text(encoding="utf-8"))
    procedure = Path(args.procedure).read_text(encoding="utf-8").strip()
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(build(data, procedure), encoding="utf-8")
    print(f"escrito {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
