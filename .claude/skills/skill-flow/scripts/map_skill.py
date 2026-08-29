#!/usr/bin/env python3
"""Map an installed skill's structure into JSON + a Mermaid asset graph.

Deterministic half of /skill-flow: everything here is read straight off disk,
so it never guesses. The procedural flowchart (what the skill actually tells
Claude to *do*) needs reading comprehension and is left to the model, which
builds it from this map.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

def _search_roots() -> list[Path]:
    """Where installed skills can live, most-editable first.

    A project copy is the one the user can actually change, so it wins over the
    synced ones. Walking up from the cwd matters because this script is normally
    invoked from inside its own skill directory (``python3 scripts/map_skill.py``),
    where a bare ``cwd/.claude/skills`` resolves to nothing and the script would
    fail to find even its own siblings. The script's own location is included
    for the same reason.
    """
    roots: list[Path] = []
    here = Path.cwd().resolve()
    for d in (here, *here.parents):
        candidate = d / ".claude" / "skills"
        if candidate.is_dir():
            roots.append(candidate)
    # scripts/map_skill.py -> <skill>/scripts -> <skill> -> <skills root>
    roots.append(Path(__file__).resolve().parent.parent.parent)
    roots.append(Path.home() / ".claude" / "skills")
    roots.extend(sorted((Path.home() / ".claude" / "skills" / "synced").glob("*")))
    roots.extend(sorted((Path.home() / ".claude" / "plugins" / "synced").glob("*/skills")))
    seen, out = set(), []
    for r in roots:
        if r.is_dir() and r not in seen:
            seen.add(r)
            out.append(r)
    return out


SEARCH_ROOTS = _search_roots()

RESOURCE_DIRS = ("references", "scripts", "assets", "agents", "evals")


def find_skill(name: str) -> Path | None:
    """Return the directory of the first skill matching ``name``."""
    for root in SEARCH_ROOTS:
        candidate = root / name
        if (candidate / "SKILL.md").is_file():
            return candidate
    # Fall back to a shallow scan, so a skill nested one level deeper still resolves.
    for root in SEARCH_ROOTS:
        if not root.is_dir():
            continue
        for child in sorted(root.glob("*/*/SKILL.md")):
            if child.parent.name == name:
                return child.parent
    return None


def list_skills() -> list[dict]:
    seen, out = set(), []
    for root in SEARCH_ROOTS:
        if not root.is_dir():
            continue
        for skill_md in sorted(root.glob("*/SKILL.md")):
            d = skill_md.parent
            if d.name in seen:
                continue
            seen.add(d.name)
            out.append({"name": d.name, "path": str(d)})
    return out


def parse_frontmatter(text: str) -> tuple[dict, str]:
    """Split YAML frontmatter from the body.

    Deliberately a minimal key: value reader rather than a YAML dependency —
    skill frontmatter is a flat handful of scalars, and a hard dependency here
    would make the skill fail on machines that lack it.
    """
    if not text.startswith("---"):
        return {}, text
    end = text.find("\n---", 3)
    if end == -1:
        return {}, text
    raw, body = text[3:end], text[end + 4:]
    meta: dict[str, str] = {}
    for line in raw.splitlines():
        if ":" not in line or line.lstrip().startswith("#"):
            continue
        key, _, value = line.partition(":")
        meta[key.strip()] = value.strip().strip('"').strip("'")
    return meta, body.lstrip("\n")


def parse_headings(body: str) -> list[dict]:
    """Heading tree, skipping anything inside fenced code blocks."""
    out, fenced = [], False
    for i, line in enumerate(body.splitlines(), start=1):
        if line.lstrip().startswith("```"):
            fenced = not fenced
            continue
        if fenced:
            continue
        m = re.match(r"^(#{1,6})\s+(.*)$", line)
        if m:
            out.append({"level": len(m.group(1)), "title": m.group(2).strip(), "line": i})
    return out


def inventory(skill_dir: Path) -> dict[str, list[dict]]:
    res: dict[str, list[dict]] = {}
    # Plenty of skills keep a companion doc at the root (REFERENCE.md,
    # FORMS.md) instead of under references/. Missing those hides part of the
    # loading structure and makes the asset diagram look emptier than it is.
    root_docs = [
        {"name": f.name, "bytes": f.stat().st_size, "path": f.name}
        for f in sorted(skill_dir.glob("*.md"))
        if f.name != "SKILL.md"
    ]
    if root_docs:
        res["root-docs"] = root_docs
    for sub in RESOURCE_DIRS:
        d = skill_dir / sub
        if not d.is_dir():
            continue
        files = [
            {"name": str(f.relative_to(d)), "bytes": f.stat().st_size,
             "path": str(f.relative_to(skill_dir))}
            for f in sorted(d.rglob("*")) if f.is_file()
        ]
        if files:
            res[sub] = files
    return res


def companion_text(skill_dir: Path) -> str:
    """Every bundled markdown doc concatenated, for indirect-citation checks."""
    parts = []
    for f in sorted(skill_dir.rglob("*.md")):
        if f.name == "SKILL.md" and f.parent == skill_dir:
            continue
        try:
            parts.append(f.read_text(encoding="utf-8", errors="replace"))
        except OSError:
            continue
    return "\n".join(parts)


def find_references(body: str, resources: dict[str, list[dict]],
                    companions: str = "") -> list[dict]:
    """Edges from SKILL.md to bundled files it actually names.

    Three link styles show up in real skills and all three count as a citation:
    the relative path (``references/query.md``), the bare filename, and the
    Python module form (``python -m scripts.aggregate_benchmark``), which drops
    both the directory slash and the extension. Missing that last form makes
    every script in a well-formed skill look orphaned, so match the stem too.

    A resource that still matches nothing is worth surfacing: it is either dead
    weight or a file the body forgot to point at.
    """
    def count(text: str, rel: str, base: str, stem: str, sub: str) -> int:
        hits = text.count(rel)
        if hits == 0 and len(base) > 4:
            hits = len(re.findall(rf"(?<![\w/]){re.escape(base)}", text))
        if (hits == 0 and sub == "scripts" and len(stem) > 4
                and not stem.startswith("__")):
            hits = len(re.findall(rf"(?<![\w]){re.escape(stem)}(?![\w])", text))
        return hits

    edges = []
    for sub, files in resources.items():
        for f in files:
            rel = f["path"]
            base = Path(f["name"]).name
            stem = Path(base).stem
            hits = body.count(rel)
            if hits == 0 and len(base) > 4:
                hits = len(re.findall(rf"(?<![\w/]){re.escape(base)}", body))
            # The module form is a scripts-only idiom, and the lookbehind must
            # allow a leading dot -- `scripts.aggregate_benchmark` is precisely
            # the shape being matched. Restricting it to scripts/ keeps a
            # reference whose stem is a common word (references/query.md ->
            # "query") from being credited by unrelated prose.
            # Dunder files (__init__.py) are packaging scaffolding, never cited
            # by name; counting them as orphans is noise, not a finding.
            if (hits == 0 and sub == "scripts" and len(stem) > 4
                    and not stem.startswith("__")):
                hits = len(re.findall(rf"(?<![\w]){re.escape(stem)}(?![\w])", body))
            # A file can be reached one hop out -- SKILL.md points at a
            # reference doc, and that doc names the script. That is still wired
            # in, so it must not be reported as dead weight.
            indirect = 0
            if hits == 0 and companions:
                indirect = count(companions, rel, base, stem, sub)
            edges.append({"target": rel, "kind": sub, "mentions": hits,
                          "mentions_indirect": indirect,
                          "scaffolding": stem.startswith("__")})
    return edges


def mermaid_assets(name: str, meta: dict, resources: dict, edges: list[dict]) -> str:
    """Asset-wiring diagram: how progressive disclosure loads this skill."""
    by_target = {e["target"]: e for e in edges}
    lines = [
        "flowchart LR",
        "  classDef entry fill:#1f6feb,stroke:#0d419d,color:#fff",
        "  classDef ref fill:#e6f0ff,stroke:#1f6feb,color:#0b2a5b",
        "  classDef script fill:#e8f5e9,stroke:#2e7d32,color:#14351a",
        "  classDef orphan fill:#fff4e5,stroke:#b26a00,color:#5c3600,stroke-dasharray:4 3",
        f'  META["metadata<br/><small>name + description<br/>siempre en contexto</small>"]:::entry',
        f'  SKILL["SKILL.md<br/><small>{len(meta.get("description", ""))} car. de descripción</small>"]:::entry',
        "  META -->|el modelo decide invocar| SKILL",
    ]
    style_for = {"scripts": "script", "agents": "ref", "references": "ref",
                 "assets": "ref", "evals": "ref"}
    for i, (sub, files) in enumerate(resources.items()):
        for j, f in enumerate(files):
            nid = f"N{i}_{j}"
            edge = by_target.get(f["path"], {"mentions": 0})
            cls = style_for.get(sub, "ref") if edge["mentions"] else "orphan"
            label = f'{f["path"]}<br/><small>{f["bytes"]} B</small>'
            lines.append(f'  {nid}["{label}"]:::{cls}')
            if edge["mentions"]:
                arrow = f'-->|citado {edge["mentions"]}x|'
            else:
                arrow = "-.->|no citado|"
            lines.append(f"  SKILL {arrow} {nid}")
    return "\n".join(lines)


def build_map(skill_dir: Path) -> dict:
    text = (skill_dir / "SKILL.md").read_text(encoding="utf-8", errors="replace")
    meta, body = parse_frontmatter(text)
    resources = inventory(skill_dir)
    edges = find_references(body, resources, companion_text(skill_dir))
    headings = parse_headings(body)
    return {
        "name": meta.get("name", skill_dir.name),
        "path": str(skill_dir),
        "description": meta.get("description", ""),
        "frontmatter": meta,
        "skill_md": {
            "bytes": len(text.encode("utf-8")),
            "lines": text.count("\n") + 1,
            "headings": headings,
        },
        "resources": resources,
        "reference_edges": edges,
        "orphans": [e["target"] for e in edges
                    if e["mentions"] == 0 and e["mentions_indirect"] == 0
                    and not e["scaffolding"]],
        "mermaid_assets": mermaid_assets(skill_dir.name, meta, resources, edges),
    }


def main() -> int:
    ap = argparse.ArgumentParser(description="Map an installed skill's structure.")
    ap.add_argument("skill", nargs="?", help="skill name or path to its directory")
    ap.add_argument("--list", action="store_true", help="list installed skills and exit")
    ap.add_argument("--out", help="write the JSON map here (default: stdout)")
    args = ap.parse_args()

    if args.list or not args.skill:
        for s in list_skills():
            print(f'{s["name"]}\t{s["path"]}')
        return 0

    p = Path(args.skill)
    skill_dir = p if (p / "SKILL.md").is_file() else find_skill(args.skill)
    if skill_dir is None:
        print(f"skill no encontrada: {args.skill}\nprueba: map_skill.py --list", file=sys.stderr)
        return 1

    data = build_map(skill_dir)
    out = json.dumps(data, indent=2, ensure_ascii=False)
    if args.out:
        Path(args.out).parent.mkdir(parents=True, exist_ok=True)
        Path(args.out).write_text(out, encoding="utf-8")
        print(f"escrito {args.out}")
    else:
        print(out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
