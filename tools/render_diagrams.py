# -*- coding: utf-8 -*-
"""Optional step: render the Mermaid diagrams of all chapters to SVG for the cockpit (spec section 11).

  python tools/render_diagrams.py            # renders missing/changed diagrams, removes orphans
  python tools/render_diagrams.py --check    # exit 1 if an SVG is missing for a Mermaid block
  python tools/render_diagrams.py --force    # re-render every diagram (after changing THEME or the config)

Uses Playwright (Chromium) and Mermaid; Mermaid is downloaded once to tools/.cache/ (not committed). The SVGs are
committed in resources/library/diagrams/<key>.svg, key = build_cockpit.diagram_key(source), so builds stay offline and
reproducible. Labels are plain SVG text (no HTML, no foreignObject), style attributes and scripts are stripped.
Render errors exit 1 and name the chapter.
"""
from __future__ import annotations

from pathlib import Path
import argparse
import re
import sys
import urllib.request

TOOLS = Path(__file__).resolve().parent
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

import build_cockpit  # noqa: E402
import library_model as lm  # noqa: E402

ROOT = TOOLS.parent
LIBRARY = ROOT / "resources" / "library"
OUT = LIBRARY / "diagrams"
CACHE = TOOLS / ".cache" / "mermaid.min.js"
MERMAID_URL = "https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.min.js"
THEME = {
    "background": "#1b2127", "primaryColor": "#222a31", "primaryTextColor": "#e9edf1", "primaryBorderColor": "#4a5663",
    "lineColor": "#8995a1", "secondaryColor": "#2a333c", "tertiaryColor": "#1b2127", "fontFamily": "Segoe UI, sans-serif",
    "fontSize": "15px", "clusterBkg": "#1b2127", "clusterBorder": "#4a5663", "edgeLabelBackground": "#1b2127",
}


def diagrams(lib):
    """key -> (chapter id, source) for every Mermaid block in the library."""
    found = {}
    for ch in lib.chapters:
        for source in ch.mermaid:
            found.setdefault(build_cockpit.diagram_key(source), (ch.id, source))
    return found


def clean_svg(svg: str) -> str:
    svg = re.sub(r"<script\b.*?</script>", "", svg, flags=re.S | re.I)
    svg = re.sub(r"\son[a-z]+\s*=\s*\"[^\"]*\"", "", svg, flags=re.I)
    svg = re.sub(r"\sstyle=\"[^\"]*\"", "", svg)
    svg = re.sub(r"<foreignObject\b.*?</foreignObject>", "", svg, flags=re.S | re.I)
    return svg.strip() + "\n"


def mermaid_js():
    if not CACHE.exists():
        CACHE.parent.mkdir(parents=True, exist_ok=True)
        with urllib.request.urlopen(MERMAID_URL, timeout=60) as resp:  # noqa: S310 - fixed https URL, build time only
            CACHE.write_bytes(resp.read())
    return CACHE


def render(items):
    """items: {key: (chapter id, source)} -> {key: svg}; raises RuntimeError naming the chapter on a render error."""
    from playwright.sync_api import sync_playwright
    import json

    out = {}
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.set_content("<!doctype html><html><body></body></html>")
        page.add_script_tag(path=str(mermaid_js()))
        page.evaluate("cfg => mermaid.initialize(cfg)", {
            "startOnLoad": False, "securityLevel": "strict", "theme": "base", "themeVariables": THEME,
            "flowchart": {"htmlLabels": False, "curve": "basis", "wrappingWidth": 320}, "htmlLabels": False,
        })
        for n, (key, (cid, source)) in enumerate(sorted(items.items())):
            result = page.evaluate("""async ([id, src]) => {
                try { const r = await mermaid.render(id, src); return {ok: true, svg: r.svg}; }
                catch (e) { return {ok: false, error: String(e && e.message || e)}; }
            }""", [f"d{key}", source])
            if not result["ok"]:
                browser.close()
                raise RuntimeError(f"{cid}: Mermaid-Fehler: {result['error'][:300]}")
            out[key] = clean_svg(result["svg"])
        browser.close()
    return out


def main(argv=None):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:  # pragma: no cover
        pass
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--force", action="store_true", help="alle Diagramme neu rendern (nach einer Theme-Änderung)")
    parser.add_argument("--root", type=Path, default=LIBRARY)
    args = parser.parse_args(argv)
    lib = lm.load_library(args.root)
    wanted = diagrams(lib)
    folder = args.root / "diagrams"
    have = {p.stem for p in folder.glob("*.svg")} if folder.exists() else set()
    missing = {k: v for k, v in wanted.items() if args.force or k not in have}
    orphans = have - set(wanted)
    if args.check:
        for k, (cid, _) in sorted(missing.items()):
            print(f"fehlt: {k}.svg ({cid})")
        print(f"{len(wanted)} Diagramme, {len(missing)} fehlen, {len(orphans)} verwaist")
        return 1 if missing else 0
    try:
        rendered = render(missing) if missing else {}
    except RuntimeError as err:
        print(err)
        return 1
    folder.mkdir(parents=True, exist_ok=True)
    for key, svg in rendered.items():
        (folder / f"{key}.svg").write_text(svg, encoding="utf-8", newline="\n")
    for key in orphans:
        (folder / f"{key}.svg").unlink()
    print(f"{len(rendered)} gerendert, {len(orphans)} verwaiste entfernt, {len(wanted)} insgesamt")
    return 0


if __name__ == "__main__":
    sys.exit(main())
