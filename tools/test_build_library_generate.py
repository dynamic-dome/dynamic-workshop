"""Generator tests on the fixture library: outputs, meta blocks, check, CRLF, catalog."""
from pathlib import Path
import importlib.util
import json
import shutil
import sys

import pytest

ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "tools" / "fixtures" / "library"


def _load(name):
    spec = importlib.util.spec_from_file_location(name, ROOT / "tools" / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


lm = _load("library_model")
bl = _load("build_library")
gen = _load("library_generate")


@pytest.fixture
def lib_dir(tmp_path):
    target = tmp_path / "library"
    shutil.copytree(FIXTURES, target)
    return target


def test_build_writes_expected_files_and_check_is_clean(lib_dir):
    assert bl.build(lib_dir, write=True) == 0
    base = lib_dir.parent
    for rel in ["library/catalog.json", "library/README.md", "library/einstufung.md", "paths/README.md",
                "paths/live-workshop.md", "paths/schnellstart.md", "paths/ziel-alltag.md", "reference/analogien.md",
                "claude-code-workshop-ui.html"]:
        assert (base / rel).exists(), rel
    assert bl.build(lib_dir, write=False) == 0


def test_meta_block_is_inserted_once_and_updated(lib_dir):
    bl.build(lib_dir, write=True)
    text = (lib_dir / "s2-08-demo-hook.md").read_text(encoding="utf-8")
    assert text.count("<!-- meta:start -->") == 1
    assert "**Voraussetzungen:** [S2.7 Hook-Events landkarten](s2-07-demo-events.md)" in text
    assert "🛡 **Sicherheitsboden**" in text
    assert "← [S2.7 Hook-Events landkarten](s2-07-demo-events.md)" in text
    assert "alter generierter Block" not in text
    assert bl.build(lib_dir, write=True) == 0
    assert (lib_dir / "s2-08-demo-hook.md").read_text(encoding="utf-8").count("<!-- meta:start -->") == 1


def test_title_change_makes_outputs_stale(lib_dir, capsys):
    bl.build(lib_dir, write=True)
    path = lib_dir / "s2-07-demo-events.md"
    path.write_text(path.read_text(encoding="utf-8").replace("Hook-Events landkarten", "Hook-Ereignisse"),
                    encoding="utf-8")
    assert bl.build(lib_dir, write=False) == 1
    out = capsys.readouterr().out
    for name in ("library/README.md", "library/catalog.json", "s2-08-demo-hook.md"):
        assert name in out, name


def test_crlf_working_copy_is_clean(lib_dir):
    bl.build(lib_dir, write=True)
    for path in list(lib_dir.parent.rglob("*.md")) + [lib_dir / "catalog.json"]:
        path.write_bytes(path.read_bytes().replace(b"\r\n", b"\n").replace(b"\n", b"\r\n"))
    assert bl.build(lib_dir, write=False) == 0


def test_build_refuses_invalid_library(lib_dir, capsys):
    path = lib_dir / "s2-08-demo-hook.md"
    path.write_text(path.read_text(encoding="utf-8").replace("<!-- cockpit:example -->\n", ""), encoding="utf-8")
    assert bl.build(lib_dir, write=True) == 1
    assert "example-count" in capsys.readouterr().out
    assert not (lib_dir / "catalog.json").exists()


def test_catalog_fields(lib_dir):
    bl.build(lib_dir, write=True)
    cat = json.loads((lib_dir / "catalog.json").read_text(encoding="utf-8"))
    by_id = {c["id"]: c for c in cat["chapters"]}
    assert [c["id"] for c in cat["chapters"]] == ["S2.7", "S2.8", "X.1", "S2.20"]
    hook = by_id["S2.8"]
    assert hook["requires_all"] == ["S2.7"] and hook["area"] == "hooks" and hook["safety_floor"] is True
    assert hook["quiz"]["correct"] == "Exit-Code 2 blockt den Aufruf"
    assert hook["example"] == '{"hooks": {"PreToolUse": []}}' and hook["file"] == "s2-08-demo-hook.md"
    assert by_id["S2.20"]["offers"] == ["S2.8"]
    assert cat["placement"]["version"] == 1 and cat["shelves"][0]["zone"] == "Erweitern"


def test_paths_use_the_engine(lib_dir):
    bl.build(lib_dir, write=True)
    quick = (lib_dir.parent / "paths" / "schnellstart.md").read_text(encoding="utf-8")
    assert "## Etappe 1" in quick and "S2.7 Hook-Events landkarten" in quick and "S2.20" not in quick
    live = (lib_dir.parent / "paths" / "live-workshop.md").read_text(encoding="utf-8")
    assert "## Session 2" in live and "Außerhalb der Sessions" in live and "X.1" in live


def test_analogies_are_generated_from_chapters(lib_dir):
    bl.build(lib_dir, write=True)
    text = (lib_dir.parent / "reference" / "analogien.md").read_text(encoding="utf-8")
    assert text.count("Wie ein Türsensor") == 1 and text.count("Wie Meldepunkte") == 1


def test_einstufung_does_not_reveal_answer_position(lib_dir):
    placement = lib_dir / "_placement.yaml"
    placement.write_text(placement.read_text(encoding="utf-8").replace("scenarios: []", (
        "scenarios:\n"
        "  - id: hook-exit\n"
        "    area: hooks\n"
        "    chapter: S2.8\n"
        "    question: Welcher Code blockt?\n"
        "    options:\n"
        "      - {id: a, text: \"Zwei blockt den Aufruf\"}\n"
        "      - {id: b, text: \"Eins blockt den Aufruf\"}\n"
        "      - {id: c, text: \"Alle Codes blocken\"}\n"
        "      - {id: d, text: \"Kein Code blockt\"}\n"
        "    correct: a\n"
        "    explanation: Nur exit 2 blockt.\n")), encoding="utf-8")
    bl.build(lib_dir, write=True)
    text = (lib_dir / "einstufung.md").read_text(encoding="utf-8")
    assert "a) Alle Codes blocken" in text and "Richtig ist d)" in text


def test_cockpit_artefact_contains_the_library(lib_dir):
    bl.build(lib_dir, write=True)
    html = (lib_dir.parent / "claude-code-workshop-ui.html").read_text(encoding="utf-8")
    assert html.count("<script") == 1 and "@@LIBRARY_DATA@@null" not in html
    assert "Einen Hook konfigurieren" in html and '\\u003c' not in html[:0]
    assert "<title>Claude Code Workshop Lern-Cockpit</title>" in html


def test_catalog_and_live_path_point_to_the_demos_that_exist(lib_dir):
    demos = lib_dir.parent / "moderation" / "vorfuehren"
    demos.mkdir(parents=True)
    (demos / "s2-08-demo-hook.md").write_text("# Vorführen: S2.8 · Einen Hook konfigurieren" + chr(10), encoding="utf-8")
    lib = lm.load_library(lib_dir)
    cat = gen.catalog(lib)
    by_id = {c["id"]: c for c in cat["chapters"]}
    assert by_id["S2.8"]["demo"] == "../moderation/vorfuehren/s2-08-demo-hook.md"
    assert by_id["S2.7"]["demo"] is None
    live = gen.paths(lib, cat)["live-workshop.md"]
    assert "(../moderation/vorfuehren/s2-08-demo-hook.md)" in live
    assert live.count("moderation/vorfuehren/") == 1
