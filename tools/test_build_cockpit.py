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


def test_script_safe_json_cannot_close_the_script():
    text = bc.script_safe_json({"x": "</script><script>alert(1)</script>", "y": "a b"})
    assert "</script" not in text and " " not in text
    assert json.loads(text) == {"x": "</script><script>alert(1)</script>", "y": "a b"}
