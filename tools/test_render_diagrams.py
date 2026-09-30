"""render_diagrams: SVG cleaning and diagram keys (rendering itself needs Chromium and is run by hand)."""
from pathlib import Path
import importlib.util
import sys

ROOT = Path(__file__).resolve().parents[1]


def _load(name):
    spec = importlib.util.spec_from_file_location(name, ROOT / "tools" / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


rd = _load("render_diagrams")
bc = _load("build_cockpit")
lm = _load("library_model")


def test_clean_svg_removes_scripts_handlers_styles_and_foreign_objects():
    dirty = ('<svg onload="x()"><script>alert(1)</script><g style="fill:red" onclick="y()">'
             '<foreignObject><div>html</div></foreignObject><text>ok</text></g></svg>')
    clean = rd.clean_svg(dirty)
    for bad in ("<script", "onload", "onclick", "style=", "foreignObject"):
        assert bad not in clean
    assert "<text>ok</text>" in clean


def test_diagram_keys_match_the_cockpit_placeholder():
    lib = lm.load_library(ROOT / "tools" / "fixtures" / "library")
    found = rd.diagrams(lib)
    assert len(found) == 1
    key, (cid, source) = next(iter(found.items()))
    assert cid == "S2.8" and key == bc.diagram_key(source)
    html = bc.chapter_html((ROOT / "tools" / "fixtures" / "library" / "s2-08-demo-hook.md").read_text(encoding="utf-8"),
                           {}, diagrams={key: "<svg/>"})
    assert f'data-diagram="{key}"' in html
