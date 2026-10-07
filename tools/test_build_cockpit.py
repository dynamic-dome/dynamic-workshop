"""Cockpit build: sanitising, link rewriting, script safety."""
from pathlib import Path
import importlib.util
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "tools" / "fixtures" / "library"


def _load(name):
    spec = importlib.util.spec_from_file_location(name, ROOT / "tools" / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


bc = _load("build_cockpit")
IDS = {"s2-07-demo-events.md": "S2.7", "s2-08-demo-hook.md": "S2.8"}


def html_of(extra=""):
    text = (FIXTURES / "s2-08-demo-hook.md").read_text(encoding="utf-8") + extra
    return bc.chapter_html(text, IDS)


def test_front_matter_meta_h1_and_quiz_are_removed():
    html = html_of()
    assert "id: S2.8" not in html and "alter generierter Block" not in html
    assert "<h1" not in html and "Quizfrage" not in html and "Exit-Code 2 blockt den Aufruf" not in html
    assert "<h2>Auf einen Blick</h2>" in html


def test_dangerous_markup_is_dropped():
    html = html_of("\n\n<script>alert(1)</script>\n\n<p onclick=\"x()\" style=\"color:red\">Hi</p>\n\n"
                   "<iframe src=\"https://evil\"></iframe>\n\n[x](javascript:alert(1))\n")
    assert "<script" not in html and "alert(1)" not in html.replace("javascript", "")
    assert "onclick" not in html and "style=" not in html and "<iframe" not in html
    assert "javascript:" not in html


def test_self_closing_or_void_dropped_tags_do_not_swallow_the_rest():
    for markup in ("<svg/>", '<iframe src="x"/>', "<embed src=\"x\">", "<math/>"):
        html = bc.chapter_html(f"# T\n\n{markup}TEXT1 and more\n\nNext paragraph\n", IDS)
        assert "TEXT1 and more" in html and "Next paragraph" in html, markup
        assert "<svg" not in html and "<iframe" not in html and "<embed" not in html


def test_script_data_cannot_open_an_html_comment_and_checks_see_escaped_markup():
    text = bc.script_safe_json({"t": "<!-- <SCRIPT>", "u": "</script>"})
    assert "<!--" not in text and "</" not in text
    assert bc.json.loads(text) == {"t": "<!-- <SCRIPT>", "u": "</script>"}
    art = '<script>const LIBRARY = {"d":"<svg onload=\\"x()\\" style=\\"a:b\\">"};</script>'
    problems = bc.artefact_problems(art)
    assert "Inline-Event-Handler" in problems and "Inline-style-Attribut" in problems
    assert "nicht genau ein <script>" in bc.artefact_problems(art + "<SCRIPT>")


def test_links_are_rewritten_for_the_export():
    html = html_of("\n\n[Karte](../reference/karte-hooks.md#exit) und [intern](#check) und [Kapitel](s2-07-demo-events.md#x)\n")
    assert 'href="?run=S2.7" data-chapter="S2.7"' in html
    assert 'href="https://github.com/dynamic-dome/dynamic-workshop/blob/main/resources/reference/karte-hooks.md#exit"' in html
    assert 'href="#check"' in html
    assert 'rel="noopener noreferrer"' in html
    hrefs = [h for h in __import__("re").findall(r'href="([^"]*)"', html)]
    assert all(h.startswith(("?run=", "#", "https://")) for h in hrefs), hrefs


def test_details_blocks_render_inner_markdown():
    html = html_of("\n\n<details><summary>Für Moderierende</summary>\n\n- **fett**\n\n</details>\n")
    assert "<summary>Für Moderierende</summary>" in html and "<strong>fett</strong>" in html


def test_mermaid_becomes_source_or_diagram_placeholder():
    text = (FIXTURES / "s2-08-demo-hook.md").read_text(encoding="utf-8")
    plain = bc.chapter_html(text, IDS)
    assert 'class="diagram-source"' in plain and "--&gt;" in plain
    source = text.split("```mermaid\n", 1)[1].split("```", 1)[0]
    key = bc.diagram_key(source)
    with_svg = bc.chapter_html(text, IDS, diagrams={key: "<svg/>"})
    assert f'data-diagram="{key}"' in with_svg


def test_diagrams_keep_their_natural_width_so_wide_charts_scroll_instead_of_shrinking():
    svg = '<svg id="d1" width="100%" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1572.66 293.97"><g/></svg>'
    sized = bc.natural_size(svg)
    assert 'width="1573"' in sized and 'height="294"' in sized and 'width="100%"' not in sized
    assert bc.natural_size("<svg><g/></svg>") == "<svg><g/></svg>"  # no viewBox: untouched


FLOW_STYLE = ("<style>#d{k}{{font-size:15px;fill:#e9edf1;}}#d{k} .node rect{{fill:#222a31;}}"
              "#d{k} [data-look=neo].node rect{{stroke:url(#d{k}-gradient);}}</style>")


def _svg(key, extra=""):
    return (f'<svg id="d{key}" width="100%" class="flowchart" viewBox="0 0 400.123456 100.5">'
            f'{FLOW_STYLE.format(k=key)}<path d="M 1.23456789 2.5"/>{extra}</svg>')


def test_diagram_styles_are_shipped_once_and_numbers_are_rounded():
    shared, css = bc.share_diagram_styles({"aaaa1111": _svg("aaaa1111"), "bbbb2222": _svg("bbbb2222")})
    assert len(css) == 1
    [(cls, rules)] = css.items()
    assert rules.startswith(f".{cls}{{font-size:15px") and f".{cls} .node rect" in rules and "#d" not in rules
    for key, svg in shared.items():
        assert "<style" not in svg and f'class="flowchart {cls}"' in svg and f'id="d{key}"' in svg
        assert 'd="M 1.23 2.5"' in svg and 'width="400"' in svg


def _fixture_render(monkeypatch, max_bytes, diagram_bytes):
    lm = _load("library_model")
    lg = _load("library_generate")
    lib = lm.load_library(FIXTURES)
    cat = lg.catalog(lib)
    text = (FIXTURES / "s2-08-demo-hook.md").read_text(encoding="utf-8")
    key = bc.diagram_key(text.split("```mermaid\n", 1)[1].split("```", 1)[0])
    monkeypatch.setattr(bc, "MAX_BYTES", max_bytes)
    art = bc.render(lib, cat, diagrams={key: _svg(key, "<g>" + "x" * diagram_bytes + "</g>")})
    start = art.index("const LIBRARY = ") + len("const LIBRARY = ")
    return json.JSONDecoder().raw_decode(art[start:])[0]


def test_oversized_artefact_drops_diagrams_before_the_full_text(monkeypatch):
    roomy = _fixture_render(monkeypatch, 10_000_000, 400_000)
    assert roomy["diagrams"] and all(c["html"] for c in roomy["chapters"])
    tight = _fixture_render(monkeypatch, 300_000, 400_000)
    assert tight["diagrams"] == {} and all(c["html"] for c in tight["chapters"])
    assert 'class="diagram-source"' in next(c["html"] for c in tight["chapters"] if c["id"] == "S2.8")
    tiny = _fixture_render(monkeypatch, 1_000, 400_000)
    assert all(c["html"] is None and c["full_url"].startswith("https://") for c in tiny["chapters"])



def test_quiz_reasons_reach_the_cockpit_as_html_in_answer_order(monkeypatch):
    data = _fixture_render(monkeypatch, 10_000_000, 10)
    by_id = {c["id"]: c for c in data["chapters"]}
    why = by_id["S2.8"]["quiz_html"]["why"]
    assert "<code>exit 2</code>" in why["correct"]
    assert len(why["wrong"]) == 3 and why["wrong"][1].startswith("Exit-Code 1 ")
    assert "why" not in by_id["S2.7"]["quiz_html"]  # no reasons in the chapter, no field

def test_script_safe_json_cannot_close_the_script():
    text = bc.script_safe_json({"x": "</script><script>alert(1)</script>", "y": "a b"})
    assert "</script" not in text and " " not in text
    assert json.loads(text) == {"x": "</script><script>alert(1)</script>", "y": "a b"}
